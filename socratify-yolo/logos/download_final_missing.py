#!/usr/bin/env python3
"""
Download ALL remaining missing logos - final comprehensive pass
"""

import os
import json
import time
import requests
import concurrent.futures
from typing import List, Dict, Tuple
from datetime import datetime
import threading

# Configuration
MAX_WORKERS = 20  # Maximum parallel downloads
RATE_LIMIT_DELAY = 0.03  # Faster rate
RETRY_ATTEMPTS = 3
TIMEOUT = 10

# Rate limiting
rate_limiter = threading.Semaphore(MAX_WORKERS)
last_request_time = threading.Lock()
last_time = [0]

def sanitize_filename(name: str) -> str:
    """Sanitize company name for filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.replace(' ', '_').replace('&', 'and').replace('.', '')
    return name[:100]

def rate_limited_request():
    """Rate limiting between requests"""
    with last_request_time:
        current_time = time.time()
        time_since_last = current_time - last_time[0]
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        last_time[0] = time.time()

def get_domain_variations(company_name: str) -> List[str]:
    """Generate domain variations for a company"""
    clean_name = company_name.split('(')[0].strip()
    clean_name = clean_name.replace('&', 'and').replace('.', '').replace("'", '')
    
    variations = []
    
    # Basic variations
    no_space = clean_name.replace(' ', '').lower()
    with_dash = clean_name.replace(' ', '-').lower()
    first_word = clean_name.split()[0].lower() if ' ' in clean_name else no_space
    
    # Different TLDs
    tlds = ['.com', '.org', '.net', '.io', '.co', '.ai', '.app', '.dev', '.biz', '.info']
    
    for base in [no_space, with_dash, first_word]:
        for tld in tlds:
            variations.append(base + tld)
    
    # Industry-specific patterns
    if any(word in company_name.lower() for word in ['bank', 'financial', 'capital']):
        variations.extend([no_space + 'bank.com', no_space + 'financial.com'])
    
    if any(word in company_name.lower() for word in ['tech', 'software', 'digital']):
        variations.extend([no_space + 'tech.com', no_space + '.io', no_space + '.dev'])
    
    if 'airlines' in company_name.lower() or 'airways' in company_name.lower():
        variations.extend([first_word + 'air.com', first_word + 'airlines.com'])
    
    # Remove duplicates
    seen = set()
    unique = []
    for v in variations:
        if v not in seen:
            seen.add(v)
            unique.append(v)
    
    return unique[:15]

def download_logo(company_info: Tuple[str, str], output_dir: str) -> Dict:
    """Download a company logo with multiple strategies"""
    company_name, category = company_info
    result = {
        'company': company_name,
        'category': category,
        'success': False,
        'error': None,
        'file_path': None,
        'source': None
    }
    
    try:
        domain_attempts = get_domain_variations(company_name)
        
        # Strategy 1: Clearbit Logo API
        for domain in domain_attempts:
            try:
                rate_limited_request()
                
                logo_url = f"https://logo.clearbit.com/{domain}"
                response = requests.get(
                    logo_url,
                    timeout=TIMEOUT,
                    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                )
                
                if response.status_code == 200 and len(response.content) > 1000:
                    filename = f"{sanitize_filename(company_name)}.png"
                    file_path = os.path.join(output_dir, category, filename)
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
        
        # Strategy 2: Google Favicons (high quality)
        for domain in domain_attempts[:5]:
            try:
                rate_limited_request()
                
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, timeout=TIMEOUT)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{sanitize_filename(company_name)}_favicon.png"
                    file_path = os.path.join(output_dir, category, filename)
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
        
        # Strategy 3: DuckDuckGo icons
        for domain in domain_attempts[:3]:
            try:
                rate_limited_request()
                
                ddg_url = f"https://icons.duckduckgo.com/ip3/{domain}.ico"
                response = requests.get(ddg_url, timeout=TIMEOUT)
                
                if response.status_code == 200 and response.content:
                    filename = f"{sanitize_filename(company_name)}_ddg.ico"
                    file_path = os.path.join(output_dir, category, filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    result['success'] = True
                    result['file_path'] = file_path
                    result['domain'] = domain
                    result['source'] = 'duckduckgo'
                    return result
            except:
                continue
        
        result['error'] = 'All strategies failed'
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def load_all_missing_companies() -> List[Tuple[str, str]]:
    """Load all missing companies from various analyses"""
    companies = []
    seen = set()
    
    # Load from niche missing
    if os.path.exists('niche_missing_800.txt'):
        with open('niche_missing_800.txt', 'r') as f:
            current_category = 'General'
            for line in f:
                line = line.strip()
                if line.startswith('##'):
                    current_category = line.replace('##', '').strip()
                elif line and not line.startswith('#'):
                    if line not in seen:
                        companies.append((line, current_category))
                        seen.add(line)
    
    # Load from comprehensive analysis
    if os.path.exists('comprehensive_missing_analysis.json'):
        with open('comprehensive_missing_analysis.json', 'r') as f:
            data = json.load(f)
            for category, info in data.get('categories', {}).items():
                for company in info.get('companies', []):
                    if company not in seen:
                        companies.append((company, category))
                        seen.add(company)
    
    # Load from expanded missing
    if os.path.exists('expanded_missing_companies.json'):
        with open('expanded_missing_companies.json', 'r') as f:
            data = json.load(f)
            for category, company_list in data.get('missing_by_category', {}).items():
                for company in company_list:
                    if company not in seen:
                        companies.append((company, category))
                        seen.add(company)
    
    return companies

def process_batch(companies: List[Tuple[str, str]], output_dir: str, batch_name: str) -> List[Dict]:
    """Process a batch of companies in parallel"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir): company 
            for company in companies
        }
        
        completed = 0
        total = len(companies)
        
        for future in concurrent.futures.as_completed(future_to_company):
            result = future.result()
            results.append(result)
            completed += 1
            
            if completed % 10 == 0 or completed == total:
                successful = sum(1 for r in results if r['success'])
                print(f"{batch_name}: {completed}/{total} ({successful} successful)")
    
    return results

def main():
    """Main execution"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/Users/adi/code/socratify/socratify-yolo/logos/final_downloads_{timestamp}"
    
    print("Loading all missing companies from various analyses...")
    all_companies = load_all_missing_companies()
    
    print(f"Starting final comprehensive download to: {output_dir}")
    print(f"Total companies to download: {len(all_companies)}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("="*60)
    
    # Group by category for organized processing
    by_category = {}
    for company, category in all_companies:
        if category not in by_category:
            by_category[category] = []
        by_category[category].append((company, category))
    
    all_results = []
    
    for category, companies in by_category.items():
        if not companies:
            continue
        
        print(f"\nProcessing {category}: {len(companies)} companies")
        results = process_batch(companies, output_dir, category)
        all_results.extend(results)
    
    # Generate final report
    successful = [r for r in all_results if r['success']]
    failed = [r for r in all_results if not r['success']]
    
    # Group by source
    by_source = {}
    for r in successful:
        source = r.get('source', 'unknown')
        if source not in by_source:
            by_source[source] = 0
        by_source[source] += 1
    
    # Save report
    report_path = os.path.join(output_dir, 'final_download_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'total_companies': len(all_results),
            'successful_downloads': len(successful),
            'failed_downloads': len(failed),
            'success_rate': f"{(len(successful)/len(all_results)*100):.1f}%" if all_results else "0%",
            'sources': by_source,
            'results': all_results
        }, f, indent=2)
    
    # Save failed list
    if failed:
        failed_path = os.path.join(output_dir, 'final_failed.txt')
        with open(failed_path, 'w', encoding='utf-8') as f:
            for item in failed:
                f.write(f"{item['company']} ({item['category']})\n")
    
    print("\n" + "="*60)
    print("FINAL DOWNLOAD COMPLETE!")
    print(f"Total attempted: {len(all_results)}")
    print(f"Successful: {len(successful)} ({(len(successful)/len(all_results)*100):.1f}%)")
    print(f"Failed: {len(failed)}")
    print(f"\nDownload sources:")
    for source, count in by_source.items():
        print(f"  {source}: {count}")
    print(f"\nReport: {report_path}")
    if failed:
        print(f"Failed list: {failed_path}")
    
    # Summary statistics
    print(f"\n{'='*60}")
    print("COLLECTION STATISTICS:")
    print(f"Previous logos: ~4,735")
    print(f"New downloads: {len(successful)}")
    print(f"Total collection: ~{4735 + len(successful)} logos")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()