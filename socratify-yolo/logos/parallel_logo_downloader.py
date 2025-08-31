#!/usr/bin/env python3
"""
Parallel Logo Downloader using Clearbit Logo API
Downloads company logos in parallel with rate limiting and error handling
"""

import os
import json
import time
import requests
import concurrent.futures
from typing import List, Dict, Tuple
from urllib.parse import quote
from datetime import datetime
import threading

# Configuration
MAX_WORKERS = 10  # Number of parallel download threads
RATE_LIMIT_DELAY = 0.1  # Delay between requests in seconds
RETRY_ATTEMPTS = 3
TIMEOUT = 10

# Create rate limiter
rate_limiter = threading.Semaphore(MAX_WORKERS)
last_request_time = threading.Lock()
last_time = [0]

def sanitize_filename(name: str) -> str:
    """Sanitize company name for use as filename"""
    # Remove special characters and replace spaces with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.replace(' ', '_').replace('&', 'and').replace('.', '')
    return name[:100]  # Limit length

def rate_limited_request():
    """Ensure rate limiting between requests"""
    with last_request_time:
        current_time = time.time()
        time_since_last = current_time - last_time[0]
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        last_time[0] = time.time()

def download_logo(company_info: Tuple[str, str], output_dir: str) -> Dict:
    """
    Download a single company logo
    Returns a dict with status information
    """
    company_name, category = company_info
    result = {
        'company': company_name,
        'category': category,
        'success': False,
        'error': None,
        'file_path': None
    }
    
    try:
        # Clean company name for domain search
        clean_name = company_name.split('(')[0].strip()
        
        # Try different domain variations
        domain_attempts = [
            f"{clean_name.replace(' ', '').lower()}.com",
            f"{clean_name.replace(' ', '-').lower()}.com",
            f"{clean_name.split()[0].lower()}.com" if ' ' in clean_name else None,
            f"{clean_name.replace(' ', '').lower()}.org",
            f"{clean_name.replace(' ', '').lower()}.net"
        ]
        
        logo_downloaded = False
        
        for domain in domain_attempts:
            if domain is None:
                continue
                
            try:
                # Rate limiting
                rate_limited_request()
                
                # Try Clearbit Logo API
                logo_url = f"https://logo.clearbit.com/{domain}"
                
                response = requests.get(
                    logo_url,
                    timeout=TIMEOUT,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                
                if response.status_code == 200 and response.content:
                    # Save the logo
                    filename = f"{sanitize_filename(company_name)}.png"
                    file_path = os.path.join(output_dir, category, filename)
                    
                    # Create category directory if it doesn't exist
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    result['success'] = True
                    result['file_path'] = file_path
                    result['domain'] = domain
                    logo_downloaded = True
                    break
                    
            except Exception as e:
                continue
        
        if not logo_downloaded:
            # Try alternative logo sources as fallback
            try:
                # Try Google's favicon service as fallback
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain_attempts[0]}&sz=128"
                response = requests.get(favicon_url, timeout=TIMEOUT)
                
                if response.status_code == 200 and response.content:
                    filename = f"{sanitize_filename(company_name)}_favicon.png"
                    file_path = os.path.join(output_dir, category, filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    result['success'] = True
                    result['file_path'] = file_path
                    result['note'] = 'favicon_fallback'
            except:
                result['error'] = 'All download attempts failed'
                
    except Exception as e:
        result['error'] = str(e)
    
    return result

def process_batch(companies: List[Tuple[str, str]], output_dir: str, batch_name: str) -> List[Dict]:
    """Process a batch of companies in parallel"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all tasks
        future_to_company = {
            executor.submit(download_logo, company, output_dir): company 
            for company in companies
        }
        
        # Process completed tasks with progress bar
        completed = 0
        total = len(companies)
        
        for future in concurrent.futures.as_completed(future_to_company):
            result = future.result()
            results.append(result)
            completed += 1
            
            # Print progress
            if completed % 10 == 0 or completed == total:
                print(f"{batch_name}: {completed}/{total} processed "
                      f"({sum(1 for r in results if r['success'])}/{completed} successful)")
    
    return results

def parse_company_list(file_path: str) -> Dict[str, List[str]]:
    """Parse the company list file and organize by category"""
    categories = {}
    current_category = "Uncategorized"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Detect category headers (lines starting with ##)
            if line.startswith('##'):
                current_category = line.replace('##', '').strip()
                if current_category not in categories:
                    categories[current_category] = []
            # Skip main headers (lines starting with single #)
            elif line.startswith('#'):
                continue
            # Add company to current category
            else:
                categories[current_category].append(line)
    
    return categories

def main():
    """Main execution function"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/Users/adi/code/socratify/socratify-yolo/logos/downloads_{timestamp}"
    
    # Parse both company lists
    all_companies = {}
    
    # Parse first file (500 companies)
    if os.path.exists("/Users/adi/code/socratify/socratify-yolo/logos/missing_500_institutions.txt"):
        companies_500 = parse_company_list("/Users/adi/code/socratify/socratify-yolo/logos/missing_500_institutions.txt")
        for category, companies in companies_500.items():
            if category not in all_companies:
                all_companies[category] = []
            all_companies[category].extend(companies)
    
    # Parse second file (1000 companies)
    if os.path.exists("/Users/adi/code/socratify/socratify-yolo/logos/missing_1000_additional_institutions.txt"):
        companies_1000 = parse_company_list("/Users/adi/code/socratify/socratify-yolo/logos/missing_1000_additional_institutions.txt")
        for category, companies in companies_1000.items():
            if category not in all_companies:
                all_companies[category] = []
            all_companies[category].extend(companies)
    
    print(f"Starting parallel download to: {output_dir}")
    print(f"Total categories: {len(all_companies)}")
    print(f"Total companies: {sum(len(companies) for companies in all_companies.values())}")
    
    # Process each category
    all_results = []
    
    for category, companies in all_companies.items():
        print(f"\nProcessing category: {category} ({len(companies)} companies)")
        
        # Create list of tuples (company, category) for processing
        company_tuples = [(company, category) for company in companies]
        
        # Process batch
        results = process_batch(company_tuples, output_dir, category)
        all_results.extend(results)
    
    # Generate summary report
    successful = [r for r in all_results if r['success']]
    failed = [r for r in all_results if not r['success']]
    
    # Save detailed results
    report_path = os.path.join(output_dir, 'download_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': timestamp,
            'total_companies': len(all_results),
            'successful_downloads': len(successful),
            'failed_downloads': len(failed),
            'success_rate': f"{(len(successful)/len(all_results)*100):.1f}%" if all_results else "0%",
            'results': all_results
        }, f, indent=2)
    
    # Save failed companies list for retry
    if failed:
        failed_path = os.path.join(output_dir, 'failed_downloads.txt')
        with open(failed_path, 'w', encoding='utf-8') as f:
            for item in failed:
                f.write(f"{item['company']} ({item['category']}): {item['error']}\n")
    
    print("\n" + "="*50)
    print(f"Download Complete!")
    print(f"Total: {len(all_results)} companies")
    print(f"Success: {len(successful)} ({(len(successful)/len(all_results)*100):.1f}%)")
    print(f"Failed: {len(failed)}")
    print(f"Report saved to: {report_path}")
    if failed:
        print(f"Failed list saved to: {failed_path}")

if __name__ == "__main__":
    main()