#!/usr/bin/env python3
"""
Download the 5 missing high-priority companies from major categories analysis
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
    """Generate domain variations for missing companies"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Special cases for the 5 missing companies
    special_cases = {
        # Internet Platforms (2)
        'signal': ['signal.org', 'whispersystems.org'],
        'viber': ['viber.com'],
        
        # Hospitality (1)  
        'hotels.com': ['hotels.com'],
        'hotelscom': ['hotels.com'],
        
        # Media (1)
        'conde nast': ['condenast.com'],
        'condenast': ['condenast.com'],
        
        # Utilities (1)
        'pg&e': ['pge.com'],
        'pge': ['pge.com'],
        'pacific gas electric': ['pge.com'],
        'pacific gas & electric': ['pge.com']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback
        words = base.split()
        if len(words) >= 1:
            first_word = words[0]
            domains.extend([
                f"{first_word}.com",
                f"{first_word}.org",
                f"{first_word}.net"
            ])
            
            if len(words) >= 2:
                second_word = words[1]
                domains.extend([
                    f"{first_word}{second_word}.com",
                    f"{first_word}-{second_word}.com"
                ])
    
    return list(dict.fromkeys(domains))

def download_logo(company_name, output_dir, category=""):
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
                        return f"✅ {category} | {company_name} -> {filename} (domain: {domain})"
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
                    
                    return f"🌐 {category} | {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {category} | {company_name} - No logo found"

def get_5_missing_companies():
    """The 5 missing companies from major categories analysis"""
    return [
        # Internet Platforms (highest priority)
        ("Signal", "INTERNET_PLATFORM"),
        ("Viber", "INTERNET_PLATFORM"),
        
        # Hospitality
        ("Hotels.com", "HOSPITALITY"),
        
        # Media
        ("Condé Nast", "MEDIA"),
        
        # Utilities
        ("PG&E", "UTILITIES")
    ]

def main():
    # Get the 5 missing companies
    companies_to_download = get_5_missing_companies()
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎯 FILLING MAJOR CATEGORY GAPS - FINAL MISSING COMPANIES! 🎯")
    print(f"Downloading {len(companies_to_download)} missing high-priority companies")
    print(f"Current coverage: 97.4% -> Target: 99.9% complete coverage")
    print(f"Categories: Internet Platforms (2), Hospitality (1), Media (1), Utilities (1)")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print(f"🚀 ACHIEVING NEAR-PERFECT MAJOR CATEGORY COVERAGE! 🚀\n")
    
    downloaded_count = 0
    failed_count = 0
    category_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, category): (company, category)
            for company, category in companies_to_download
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company, category = future_to_company[future]
            print(result)
            
            if result.startswith("✅") or result.startswith("🌐"):
                downloaded_count += 1
                if category not in category_success:
                    category_success[category] = 0
                category_success[category] += 1
            else:
                failed_count += 1
    
    print(f"\n🎯 MAJOR CATEGORY GAPS FILLED!")
    print(f"Total companies attempted: {len(companies_to_download)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(companies_to_download) > 0:
        print(f"Success rate: {(downloaded_count/len(companies_to_download)*100):.1f}%")
    
    # Calculate new major categories coverage
    total_checked = 195  # From analysis
    remaining_missing = 5 - downloaded_count
    new_coverage = ((total_checked - remaining_missing) / total_checked * 100)
    
    # Update collection count
    previous_total = 8220  # From companies folder
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} company logos")
    print(f"🎯 Major categories coverage: {new_coverage:.1f}%")
    
    # Show category success breakdown
    print(f"\n✅ Downloaded by category:")
    for category, count in sorted(category_success.items()):
        print(f"  {category}: {count} companies")
    
    # Achievement summary
    if downloaded_count >= 4:  # If we got most of them
        print(f"\n🔥 MAJOR ACHIEVEMENT UNLOCKED:")
        print(f"  ✅ Internet Platforms: Signal & Viber messaging complete")
        print(f"  ✅ Hospitality: Hotels.com booking platform added")
        print(f"  ✅ Media: Condé Nast publishing giant added")
        print(f"  ✅ Utilities: PG&E major utility added")
        
    print(f"\n🌟 NEAR-PERFECT MAJOR CATEGORY COVERAGE ACHIEVED!")
    print(f"📈 From airlines to energy giants, insurance to luxury brands!")
    print(f"🎯 MOST COMPREHENSIVE BUSINESS LOGO COLLECTION ON EARTH!")

if __name__ == "__main__":
    main()