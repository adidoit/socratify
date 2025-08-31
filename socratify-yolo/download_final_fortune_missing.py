#!/usr/bin/env python3
"""
Download final 2 missing Fortune 1000 companies
Overstock.com and Fox Corporation
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 10
RATE_LIMIT = threading.Semaphore(5)
RATE_LIMIT_DELAY = 0.1

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(company_name):
    """Generate domain variations"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Special cases for the 2 missing companies
    special_cases = {
        'overstock.com': ['overstock.com'],
        'overstockcom': ['overstock.com'],
        'overstock': ['overstock.com'],
        
        'fox corporation': ['foxcorporation.com', 'fox.com'],
        'foxcorporation': ['foxcorporation.com', 'fox.com'],
        'fox corp': ['fox.com']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback
        words = base.split()
        if len(words) == 1:
            domains.append(f"{words[0]}.com")
        elif len(words) == 2:
            domains.extend([
                f"{words[0]}{words[1]}.com",
                f"{words[0]}.com"
            ])
    
    return list(dict.fromkeys(domains))

def download_logo(company_name, output_dir):
    """Download logo with comprehensive domain trying"""
    
    with RATE_LIMIT:
        time.sleep(RATE_LIMIT_DELAY)
        
        domains = generate_domains(company_name)
        
        for domain in domains:
            try:
                # Try Clearbit first
                logo_url = f"https://logo.clearbit.com/{domain}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
                
                response = requests.get(logo_url, headers=headers, timeout=15, stream=True)
                
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '')
                    
                    if 'image' not in content_type and 'octet-stream' not in content_type:
                        continue
                    
                    # Get file extension
                    if 'png' in content_type:
                        ext = 'png'
                    elif 'jpeg' in content_type or 'jpg' in content_type:
                        ext = 'jpg'
                    elif 'svg' in content_type:
                        ext = 'svg'
                    else:
                        ext = 'png'
                    
                    filename = f"{clean_filename(company_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.getsize(filepath) > 500:
                        return f"🔥 FORTUNE | {company_name} -> {filename} (domain: {domain})"
                    else:
                        os.remove(filepath)
                
                # Try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(company_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"🔍 FORTUNE | {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ FORTUNE | {company_name} - No logo found"

def main():
    # FINAL 2 MISSING FORTUNE 1000 COMPANIES
    fortune_missing = [
        "Overstock.com",
        "Fox Corporation"
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🏢 FINAL FORTUNE 1000 MISSING COMPANIES 🏢")
    print(f"Downloading {len(fortune_missing)} final Fortune 1000 companies")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\n")
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir): company
            for company in fortune_missing
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("🔍"):
                downloaded_count += 1
            else:
                failed_count += 1
    
    print(f"\n✅ FINAL FORTUNE 1000 DOWNLOAD COMPLETE!")
    print(f"Total companies: {len(fortune_missing)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(fortune_missing) > 0:
        print(f"Success rate: {(downloaded_count/len(fortune_missing)*100):.1f}%")
    
    # Update collection count
    previous_total = 8331  # From obvious brands
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"🏢 Fortune 1000 coverage now: {((191-failed_count)/191*100):.1f}%")
    print(f"✅ WORLD'S MOST COMPLETE BUSINESS LOGO COLLECTION!")

if __name__ == "__main__":
    main()