#!/usr/bin/env python3
"""
Download logos for MASSIVE list of startups, private companies, and funds
"""

import os
import json
import time
import requests
import concurrent.futures
from typing import List, Dict, Tuple
from datetime import datetime
import threading
import glob

# Configuration
MAX_WORKERS = 25  # Aggressive parallelization
RATE_LIMIT_DELAY = 0.02  # Faster rate
TIMEOUT = 8

rate_limiter = threading.Semaphore(MAX_WORKERS)
last_request_time = threading.Lock()
last_time = [0]

def load_existing_logos() -> set:
    """Load all existing logos to avoid duplicates"""
    existing = set()
    logo_dirs = [
        '/Users/adi/code/socratify/socratify-yolo/logos/all_unique_logos/',
        '/Users/adi/code/socratify/socratify-yolo/logos/downloads_20250807_175600/',
        '/Users/adi/code/socratify/socratify-yolo/logos/verified_downloads_20250807_184645/',
        '/Users/adi/code/socratify/socratify-yolo/logos/final_downloads_20250807_190319/',
        '/Users/adi/code/socratify/socratify-yolo/logos/institutional_logos_20250807_191623/'
    ]
    
    for directory in logo_dirs:
        if os.path.exists(directory):
            for file in glob.glob(os.path.join(directory, '**/*'), recursive=True):
                if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico')):
                    basename = os.path.basename(file).lower()
                    # Normalize name
                    name = basename.replace('.png', '').replace('.jpg', '').replace('.svg', '').replace('_', ' ')
                    existing.add(name)
    
    return existing

def sanitize_filename(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.replace(' ', '_').replace('&', 'and').replace('.', '').replace("'", '')
    return name[:100]

def rate_limited_request():
    with last_request_time:
        current_time = time.time()
        time_since_last = current_time - last_time[0]
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        last_time[0] = time.time()

def get_smart_domain_variations(company_name: str, category: str) -> List[str]:
    """Generate smart domain variations based on company type"""
    clean_name = company_name.lower().replace(' ', '').replace('.', '').replace("'", '').replace('&', 'and')
    with_dash = company_name.lower().replace(' ', '-').replace('.', '').replace("'", '').replace('&', 'and')
    first_word = company_name.split()[0].lower() if ' ' in company_name else clean_name
    
    variations = []
    
    # Category-specific patterns
    if 'Fund' in category or 'Capital' in company_name or 'Ventures' in company_name:
        # Investment firms often use .com
        variations.extend([
            f"{clean_name}.com",
            f"{clean_name}capital.com",
            f"{clean_name}ventures.com",
            f"{clean_name}partners.com",
            f"{first_word}capital.com"
        ])
    
    elif 'Accelerator' in category or 'Incubator' in category:
        variations.extend([
            f"{clean_name}.com",
            f"{clean_name}.io",
            f"{clean_name}.co",
            f"{with_dash}.com",
            f"{first_word}.vc"
        ])
    
    elif 'Tech' in category or 'Unicorn' in category or 'SaaS' in company_name:
        # Tech companies love .io, .ai, .app
        variations.extend([
            f"{clean_name}.com",
            f"{clean_name}.io",
            f"{clean_name}.ai",
            f"{clean_name}.app",
            f"{clean_name}.dev",
            f"{clean_name}.co",
            f"get{clean_name}.com",
            f"try{clean_name}.com",
            f"use{clean_name}.com"
        ])
    
    elif 'Health' in category or 'Bio' in category:
        variations.extend([
            f"{clean_name}.com",
            f"{clean_name}health.com",
            f"{clean_name}bio.com",
            f"{clean_name}therapeutics.com",
            f"{clean_name}pharma.com"
        ])
    
    else:
        # Standard variations
        variations.extend([
            f"{clean_name}.com",
            f"{with_dash}.com",
            f"{clean_name}.net",
            f"{clean_name}.org",
            f"{clean_name}.co",
            f"{first_word}.com"
        ])
    
    # Add some without common suffixes
    for suffix in ['inc', 'corp', 'llc', 'ltd', 'group', 'company', 'co']:
        if suffix in clean_name:
            base = clean_name.replace(suffix, '')
            variations.append(f"{base}.com")
    
    # Remove duplicates
    seen = set()
    unique = []
    for v in variations:
        if v not in seen and len(v) > 5:  # Minimum domain length
            seen.add(v)
            unique.append(v)
    
    return unique[:12]

def download_logo(company_info: Tuple[str, str], output_dir: str, existing_logos: set) -> Dict:
    """Download a company logo"""
    company_name, category = company_info
    
    # Check if already exists
    check_name = sanitize_filename(company_name).lower()
    if check_name in existing_logos or company_name.lower() in existing_logos:
        return {
            'company': company_name,
            'category': category,
            'success': False,
            'error': 'Already exists',
            'skipped': True
        }
    
    result = {
        'company': company_name,
        'category': category,
        'success': False,
        'error': None,
        'file_path': None,
        'source': None,
        'skipped': False
    }
    
    try:
        domains = get_smart_domain_variations(company_name, category)
        
        # Try Clearbit first
        for domain in domains:
            try:
                rate_limited_request()
                logo_url = f"https://logo.clearbit.com/{domain}"
                response = requests.get(logo_url, timeout=TIMEOUT, 
                                      headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
                
                if response.status_code == 200 and len(response.content) > 1000:
                    filename = f"{sanitize_filename(company_name)}.png"
                    file_path = os.path.join(output_dir, category.replace(' ', '_'), filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    result['success'] = True
                    result['file_path'] = file_path
                    result['domain'] = domain
                    result['source'] = 'clearbit'
                    return result
            except:
                continue
        
        # Try Google Favicons
        for domain in domains[:4]:
            try:
                rate_limited_request()
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, timeout=TIMEOUT)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{sanitize_filename(company_name)}_favicon.png"
                    file_path = os.path.join(output_dir, category.replace(' ', '_'), filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    result['success'] = True
                    result['file_path'] = file_path
                    result['domain'] = domain
                    result['source'] = 'google_favicon'
                    return result
            except:
                continue
        
        result['error'] = 'No valid logo found'
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def load_companies_from_file() -> Dict[str, List[str]]:
    """Load companies from the generated text file"""
    companies = {}
    current_category = "General"
    
    with open('/Users/adi/code/socratify/socratify-yolo/logos/massive_company_list.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('##'):
                current_category = line.replace('##', '').strip()
                if current_category not in companies:
                    companies[current_category] = []
            elif line and not line.startswith('#'):
                companies[current_category].append(line)
    
    return companies

def process_batch_parallel(companies: List[Tuple[str, str]], output_dir: str, existing_logos: set) -> List[Dict]:
    """Process companies in parallel batches"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, existing_logos): company 
            for company in companies
        }
        
        completed = 0
        total = len(companies)
        successful = 0
        skipped = 0
        
        for future in concurrent.futures.as_completed(future_to_company):
            result = future.result()
            results.append(result)
            completed += 1
            
            if result.get('skipped'):
                skipped += 1
            elif result['success']:
                successful += 1
            
            if completed % 20 == 0 or completed == total:
                print(f"  Progress: {completed}/{total} | Success: {successful} | Skipped: {skipped} | Failed: {completed - successful - skipped}")
    
    return results

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/Users/adi/code/socratify/socratify-yolo/logos/massive_downloads_{timestamp}"
    
    print("Loading existing logos to avoid duplicates...")
    existing_logos = load_existing_logos()
    print(f"Found {len(existing_logos)} existing logos")
    
    print("\nLoading massive company list...")
    companies = load_companies_from_file()
    
    # Flatten into list
    all_companies = []
    for category, company_list in companies.items():
        for company in company_list:
            all_companies.append((company, category))
    
    print(f"Total companies to process: {len(all_companies)}")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("="*60)
    
    all_results = []
    
    # Process by category for better organization
    for category, company_list in companies.items():
        if not company_list:
            continue
            
        print(f"\n📦 Processing {category}: {len(company_list)} companies")
        
        batch = [(company, category) for company in company_list]
        results = process_batch_parallel(batch, output_dir, existing_logos)
        all_results.extend(results)
    
    # Generate comprehensive report
    successful = [r for r in all_results if r['success']]
    failed = [r for r in all_results if not r['success'] and not r.get('skipped')]
    skipped = [r for r in all_results if r.get('skipped')]
    
    # Group by source
    by_source = {}
    for r in successful:
        source = r.get('source', 'unknown')
        if source not in by_source:
            by_source[source] = 0
        by_source[source] += 1
    
    # Save detailed report
    report_path = os.path.join(output_dir, 'massive_download_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'total_processed': len(all_results),
            'successful_downloads': len(successful),
            'failed_downloads': len(failed),
            'skipped_existing': len(skipped),
            'success_rate': f"{(len(successful)/(len(successful)+len(failed))*100):.1f}%" if (successful or failed) else "0%",
            'sources': by_source,
            'results': all_results
        }, f, indent=2)
    
    # Save failed companies for retry
    if failed:
        failed_path = os.path.join(output_dir, 'failed_companies.txt')
        with open(failed_path, 'w', encoding='utf-8') as f:
            for item in failed:
                f.write(f"{item['company']} ({item['category']}): {item.get('error', 'Unknown')}\n")
    
    print("\n" + "="*60)
    print("🎉 MASSIVE DOWNLOAD COMPLETE!")
    print(f"Total processed: {len(all_results)}")
    print(f"✅ Successful: {len(successful)}")
    print(f"⏭️  Skipped (already exist): {len(skipped)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n📊 Download sources:")
        for source, count in by_source.items():
            print(f"  {source}: {count}")
    
    print(f"\n📁 Report: {report_path}")
    if failed:
        print(f"📁 Failed list: {failed_path}")
    
    print(f"\n🏆 FINAL COLLECTION STATS:")
    print(f"Previous collection: ~5,700 logos")
    print(f"New unique downloads: {len(successful)}")
    print(f"TOTAL COLLECTION: ~{5700 + len(successful)} logos!")

if __name__ == "__main__":
    main()