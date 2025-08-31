#!/usr/bin/env python3
"""
Download logos for verified missing companies from the analysis
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
MAX_WORKERS = 15  # Increased for faster processing
RATE_LIMIT_DELAY = 0.05  # Faster rate
RETRY_ATTEMPTS = 3
TIMEOUT = 10

# Rate limiting
rate_limiter = threading.Semaphore(MAX_WORKERS)
last_request_time = threading.Lock()
last_time = [0]

def sanitize_filename(name: str) -> str:
    """Sanitize company name for use as filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.replace(' ', '_').replace('&', 'and').replace('.', '')
    return name[:100]

def rate_limited_request():
    """Ensure rate limiting between requests"""
    with last_request_time:
        current_time = time.time()
        time_since_last = current_time - last_time[0]
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        last_time[0] = time.time()

def get_domain_variations(company_name: str) -> List[str]:
    """Generate multiple domain variations for a company"""
    clean_name = company_name.split('(')[0].strip()
    clean_name = clean_name.replace('&', 'and').replace('.', '')
    
    # Generate variations
    variations = []
    
    # Basic variations
    no_space = clean_name.replace(' ', '').lower()
    with_dash = clean_name.replace(' ', '-').lower()
    first_word = clean_name.split()[0].lower() if ' ' in clean_name else no_space
    
    # Add variations with different TLDs
    tlds = ['.com', '.org', '.net', '.io', '.co', '.ai', '.app', '.dev']
    
    for base in [no_space, with_dash, first_word]:
        for tld in tlds:
            variations.append(base + tld)
    
    # Special cases for known patterns
    if 'Corporation' in company_name or 'Inc' in company_name:
        corp_name = clean_name.replace('Corporation', '').replace('Inc', '').strip()
        variations.append(corp_name.replace(' ', '').lower() + '.com')
    
    if 'Group' in company_name:
        group_name = clean_name.replace('Group', '').strip()
        variations.append(group_name.replace(' ', '').lower() + '.com')
        variations.append(group_name.replace(' ', '').lower() + 'group.com')
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variations = []
    for v in variations:
        if v not in seen:
            seen.add(v)
            unique_variations.append(v)
    
    return unique_variations[:10]  # Limit to 10 variations

def download_logo(company_info: Tuple[str, str], output_dir: str) -> Dict:
    """Download a single company logo with multiple strategies"""
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
        
        # Strategy 1: Try Clearbit Logo API
        for domain in domain_attempts:
            try:
                rate_limited_request()
                
                logo_url = f"https://logo.clearbit.com/{domain}"
                response = requests.get(
                    logo_url,
                    timeout=TIMEOUT,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                
                if response.status_code == 200 and response.content and len(response.content) > 1000:
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
        
        # Strategy 2: Try Google Favicons (higher quality)
        for domain in domain_attempts[:3]:  # Try first 3 variations
            try:
                rate_limited_request()
                
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, timeout=TIMEOUT)
                
                if response.status_code == 200 and response.content and len(response.content) > 500:
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
        
        # Strategy 3: Try DuckDuckGo favicon service
        for domain in domain_attempts[:2]:
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
        
        result['error'] = 'All download strategies failed'
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

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
            
            if completed % 5 == 0 or completed == total:
                successful = sum(1 for r in results if r['success'])
                print(f"{batch_name}: {completed}/{total} processed ({successful} successful)")
    
    return results

def main():
    """Main execution function"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/Users/adi/code/socratify/socratify-yolo/logos/verified_downloads_{timestamp}"
    
    # Load the verified missing companies
    with open('/Users/adi/code/socratify/socratify-yolo/logos/expanded_missing_companies.json', 'r') as f:
        data = json.load(f)
    
    missing_by_category = data['missing_by_category']
    
    # Also load from the 800 list file if it exists
    additional_companies = {}
    if os.path.exists('/Users/adi/code/socratify/socratify-yolo/logos/missing_800_companies.txt'):
        current_category = "Additional"
        with open('/Users/adi/code/socratify/socratify-yolo/logos/missing_800_companies.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('##'):
                    current_category = line.replace('##', '').strip()
                elif line and not line.startswith('#'):
                    if current_category not in additional_companies:
                        additional_companies[current_category] = []
                    if line not in additional_companies[current_category]:
                        additional_companies[current_category].append(line)
    
    # Merge the lists
    all_companies = missing_by_category.copy()
    for cat, companies in additional_companies.items():
        if cat in all_companies:
            # Add only unique companies
            existing = set(all_companies[cat])
            for company in companies:
                if company not in existing:
                    all_companies[cat].append(company)
        else:
            all_companies[cat] = companies
    
    total_companies = sum(len(companies) for companies in all_companies.values())
    
    print(f"Starting parallel download to: {output_dir}")
    print(f"Total categories: {len(all_companies)}")
    print(f"Total companies to download: {total_companies}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("="*50)
    
    # Process each category
    all_results = []
    
    for category, companies in all_companies.items():
        if not companies:
            continue
            
        print(f"\nProcessing {category}: {len(companies)} companies")
        
        # Create list of tuples for processing
        company_tuples = [(company, category) for company in companies]
        
        # Process batch
        results = process_batch(company_tuples, output_dir, category)
        all_results.extend(results)
    
    # Generate summary report
    successful = [r for r in all_results if r['success']]
    failed = [r for r in all_results if not r['success']]
    
    # Group by source
    by_source = {}
    for r in successful:
        source = r.get('source', 'unknown')
        if source not in by_source:
            by_source[source] = 0
        by_source[source] += 1
    
    # Save detailed results
    report_path = os.path.join(output_dir, 'download_report.json')
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
    
    # Save failed companies for retry
    if failed:
        failed_path = os.path.join(output_dir, 'failed_downloads.txt')
        with open(failed_path, 'w', encoding='utf-8') as f:
            for item in failed:
                f.write(f"{item['company']} ({item['category']})\n")
    
    print("\n" + "="*50)
    print(f"Download Complete!")
    print(f"Total: {len(all_results)} companies")
    print(f"Success: {len(successful)} ({(len(successful)/len(all_results)*100):.1f}%)")
    print(f"Failed: {len(failed)}")
    print(f"\nDownload sources:")
    for source, count in by_source.items():
        print(f"  {source}: {count}")
    print(f"\nReport saved to: {report_path}")
    if failed:
        print(f"Failed list saved to: {failed_path}")

if __name__ == "__main__":
    main()