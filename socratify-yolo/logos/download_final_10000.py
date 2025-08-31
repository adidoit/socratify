#!/usr/bin/env python3
"""
FINAL PUSH TO 10,000 LOGOS - The Ultimate Download
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
MAX_WORKERS = 30
RATE_LIMIT_DELAY = 0.01
TIMEOUT = 5
BATCH_SIZE = 50

rate_limiter = threading.Semaphore(MAX_WORKERS)
last_request_time = threading.Lock()
last_time = [0]

def load_existing_logos() -> set:
    """Load all existing logos to check for duplicates"""
    existing = set()
    logo_dirs = glob.glob('/Users/adi/code/socratify/socratify-yolo/logos/*/')
    
    for directory in logo_dirs:
        if os.path.exists(directory):
            for file in glob.glob(os.path.join(directory, '**/*'), recursive=True):
                if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico')):
                    basename = os.path.basename(file).lower()
                    name = basename.replace('.png', '').replace('.jpg', '').replace('.svg', '')
                    name = name.replace('_', ' ').replace('-', ' ')
                    existing.add(name)
                    existing.add(name.replace(' ', ''))
    
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

def get_company_domains(company_name: str, category: str) -> List[str]:
    """Generate domain variations for companies based on category"""
    clean = company_name.lower().replace(' ', '').replace('.', '').replace("'", '').replace('&', 'and')
    dash = company_name.lower().replace(' ', '-').replace('.', '').replace("'", '').replace('&', 'and')
    
    # Remove common words for cleaner domains
    for word in ['the', 'corporation', 'company', 'inc', 'llc', 'ltd', 'group', 'holdings']:
        clean = clean.replace(word, '')
        dash = dash.replace(word, '')
    
    variations = []
    
    # Category-specific patterns
    if any(x in category for x in ['Chinese', 'Japanese', 'Korean', 'Indian']):
        # Asian companies
        variations.extend([
            f"{clean}.com", f"{clean}.cn", f"{clean}.jp", f"{clean}.kr", 
            f"{clean}.in", f"{clean}.asia", f"{clean}corp.com"
        ])
    
    elif any(x in category for x in ['Brazilian', 'Mexican', 'Saudi', 'UAE', 'Turkish']):
        # Regional companies
        variations.extend([
            f"{clean}.com", f"{clean}.com.br", f"{clean}.com.mx", 
            f"{clean}.sa", f"{clean}.ae", f"{clean}.com.tr"
        ])
    
    elif 'NFL' in category or 'NBA' in category or 'MLB' in category or 'NHL' in category:
        # Sports teams
        variations.extend([
            f"{clean}.com", f"{dash}.com", f"the{clean}.com",
            f"{clean}football.com", f"{clean}basketball.com"
        ])
    
    elif 'Soccer' in category:
        # Soccer clubs
        variations.extend([
            f"{clean}fc.com", f"{clean}.com", f"{dash}.com",
            f"{clean}football.com", f"{clean}fc.co.uk"
        ])
    
    elif any(x in category for x in ['Charity', 'Foundation', 'Advocacy', 'Religious']):
        # Non-profits
        variations.extend([
            f"{clean}.org", f"{clean}.com", f"{clean}foundation.org",
            f"{clean}charity.org", f"{clean}.net"
        ])
    
    elif any(x in category for x in ['Hospital', 'School', 'University']):
        # Educational/Medical
        variations.extend([
            f"{clean}.edu", f"{clean}.org", f"{clean}.com",
            f"{clean}health.org", f"{clean}medical.com"
        ])
    
    elif any(x in category for x in ['State', 'Federal', 'City']):
        # Government
        variations.extend([
            f"{clean}.gov", f"{clean}.org", f"{clean}.com",
            f"{clean}state.gov", f"{clean}city.gov"
        ])
    
    elif 'Blockchain' in category or 'DeFi' in category or 'NFT' in category:
        # Web3
        variations.extend([
            f"{clean}.io", f"{clean}.xyz", f"{clean}.finance",
            f"{clean}protocol.com", f"{clean}.org", f"{clean}.network"
        ])
    
    else:
        # Generic patterns
        variations.extend([
            f"{clean}.com", f"{dash}.com", f"{clean}.net",
            f"{clean}.org", f"{clean}.io", f"{clean}usa.com"
        ])
    
    # Add some without spaces/dashes
    first_word = company_name.split()[0].lower() if ' ' in company_name else clean
    if len(first_word) > 3:
        variations.append(f"{first_word}.com")
    
    # Remove duplicates
    seen = set()
    unique = []
    for v in variations:
        if v not in seen and len(v) > 5:
            seen.add(v)
            unique.append(v)
    
    return unique[:12]

def download_logo(company_info: Tuple[str, str], output_dir: str, existing_logos: set) -> Dict:
    """Download logo for company"""
    company_name, category = company_info
    
    # Check if exists
    check_name = sanitize_filename(company_name).lower().replace('_', ' ')
    if check_name in existing_logos or check_name.replace(' ', '') in existing_logos:
        return {
            'company': company_name,
            'category': category,
            'success': False,
            'skipped': True
        }
    
    result = {
        'company': company_name,
        'category': category,
        'success': False,
        'error': None,
        'skipped': False
    }
    
    try:
        domains = get_company_domains(company_name, category)
        
        # Try Clearbit
        for domain in domains:
            try:
                rate_limited_request()
                response = requests.get(
                    f"https://logo.clearbit.com/{domain}",
                    timeout=TIMEOUT,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                if response.status_code == 200 and len(response.content) > 800:
                    filename = f"{sanitize_filename(company_name)}.png"
                    file_path = os.path.join(output_dir, category.replace(' ', '_').replace('&', 'and'), filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    result['success'] = True
                    result['source'] = 'clearbit'
                    result['domain'] = domain
                    return result
            except:
                pass
        
        # Try Google favicon
        for domain in domains[:5]:
            try:
                rate_limited_request()
                response = requests.get(
                    f"https://www.google.com/s2/favicons?domain={domain}&sz=256",
                    timeout=3
                )
                if response.status_code == 200 and len(response.content) > 400:
                    filename = f"{sanitize_filename(company_name)}_favicon.png"
                    file_path = os.path.join(output_dir, category.replace(' ', '_').replace('&', 'and'), filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    result['success'] = True
                    result['source'] = 'google'
                    result['domain'] = domain
                    return result
            except:
                pass
        
        result['error'] = 'No logo found'
        
    except Exception as e:
        result['error'] = str(e)[:50]
    
    return result

def process_batch(batch: List[Tuple[str, str]], output_dir: str, existing_logos: set, batch_num: int) -> List[Dict]:
    """Process batch with parallel downloads"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(download_logo, company, output_dir, existing_logos)
            for company in batch
        ]
        
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                result = future.result(timeout=10)
                results.append(result)
                
                if i % 10 == 0 or i == len(batch):
                    success = sum(1 for r in results if r.get('success'))
                    skipped = sum(1 for r in results if r.get('skipped'))
                    failed = len(results) - success - skipped
                    print(f"    Batch {batch_num}: {i}/{len(batch)} | ✅ {success} | ⏭️ {skipped} | ❌ {failed}")
            except:
                results.append({'success': False, 'error': 'timeout'})
    
    return results

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/Users/adi/code/socratify/socratify-yolo/logos/final_10000_{timestamp}"
    
    print("🚀 FINAL PUSH TO 10,000 LOGOS!")
    print("The Ultimate Collection - Every Company That Matters")
    print("="*60)
    
    print("Loading existing logos...")
    existing_logos = load_existing_logos()
    print(f"Found {len(existing_logos)} existing logos\n")
    
    print("Loading final company list...")
    companies = {}
    current_category = "General"
    
    with open('/Users/adi/code/socratify/socratify-yolo/logos/final_10000_list.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('##'):
                current_category = line.replace('##', '').strip()
                if current_category not in companies:
                    companies[current_category] = []
            elif line and not line.startswith('#'):
                companies[current_category].append(line)
    
    # Flatten
    all_companies = []
    for category, company_list in companies.items():
        for company in company_list:
            all_companies.append((company, category))
    
    print(f"Total companies to process: {len(all_companies)}")
    print(f"Output: {output_dir}")
    print(f"Workers: {MAX_WORKERS} parallel threads")
    print("="*60 + "\n")
    
    all_results = []
    
    # Process in batches
    for i in range(0, len(all_companies), BATCH_SIZE):
        batch = all_companies[i:i+BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(all_companies) + BATCH_SIZE - 1) // BATCH_SIZE
        
        category_name = batch[0][1] if batch else "Mixed"
        print(f"📦 Batch {batch_num}/{total_batches}: {category_name[:30]}... ({len(batch)} companies)")
        
        batch_results = process_batch(batch, output_dir, existing_logos, batch_num)
        all_results.extend(batch_results)
        
        # Running totals
        total_success = sum(1 for r in all_results if r.get('success'))
        total_skipped = sum(1 for r in all_results if r.get('skipped'))
        total_failed = len(all_results) - total_success - total_skipped
        
        if batch_num % 5 == 0 or batch_num == total_batches:
            print(f"   📊 Running Total: ✅ {total_success} | ⏭️ {total_skipped} | ❌ {total_failed}\n")
    
    # Final report
    successful = [r for r in all_results if r.get('success')]
    skipped = [r for r in all_results if r.get('skipped')]
    failed = [r for r in all_results if not r.get('success') and not r.get('skipped')]
    
    # Group by source
    by_source = {}
    for r in successful:
        source = r.get('source', 'unknown')
        by_source[source] = by_source.get(source, 0) + 1
    
    # Save report
    report_path = os.path.join(output_dir, 'final_10000_report.json')
    os.makedirs(output_dir, exist_ok=True)
    with open(report_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total': len(all_results),
            'successful': len(successful),
            'skipped': len(skipped),
            'failed': len(failed),
            'success_rate': f"{(len(successful)/(len(successful)+len(failed))*100):.1f}%" if (successful or failed) else "0%",
            'sources': by_source,
            'categories_processed': list(companies.keys())
        }, f, indent=2)
    
    # Save failed list
    if failed:
        failed_path = os.path.join(output_dir, 'failed_companies.txt')
        with open(failed_path, 'w') as f:
            for item in failed:
                f.write(f"{item['company']} ({item['category']})\n")
    
    print("\n" + "="*60)
    print("🏁 FINAL DOWNLOAD COMPLETE!")
    print(f"Total processed: {len(all_results)}")
    print(f"✅ NEW LOGOS: {len(successful)}")
    print(f"⏭️ Already existed: {len(skipped)}")
    print(f"❌ Failed: {len(failed)}")
    
    if successful:
        print(f"\n📊 Download sources:")
        for source, count in by_source.items():
            print(f"  {source}: {count}")
    
    # Estimate total collection
    estimated_previous = 7600  # From previous downloads
    estimated_total = estimated_previous + len(successful)
    
    print(f"\n🏆 COLLECTION STATUS:")
    print(f"Previous: ~{estimated_previous} logos")
    print(f"Added: {len(successful)} new logos")
    print(f"ESTIMATED TOTAL: ~{estimated_total} LOGOS!")
    
    if estimated_total >= 10000:
        print("\n🎉 WE DID IT! 10,000+ LOGOS ACHIEVED!")
        print("The most comprehensive business logo collection ever assembled!")
    else:
        remaining = 10000 - estimated_total
        print(f"\nAlmost there! Only ~{remaining} logos to go for 10,000!")
    
    print("="*60)

if __name__ == "__main__":
    main()