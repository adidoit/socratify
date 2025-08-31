#!/usr/bin/env python3
"""
Download missing websites from top 2,500 analysis
Focus on categories 2,3,4,5: Health/Medical, Chinese E-commerce, Developer Tools, Indian Regional
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 20
RATE_LIMIT = threading.Semaphore(15)
RATE_LIMIT_DELAY = 0.05

def clean_filename(website_name):
    """Convert website name to clean filename"""
    filename = website_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(website_name):
    """Generate domain variations for missing websites"""
    base = website_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Special cases for the missing websites
    special_cases = {
        # Health/Medical Sites (4)
        'medlineplus': ['medlineplus.gov'],
        'drugs.com': ['drugs.com'],
        'drugscom': ['drugs.com'],
        'rxlist': ['rxlist.com'],
        'patient.info': ['patient.info'],
        'patientinfo': ['patient.info'],
        
        # Chinese E-commerce (3)
        'aliexpress': ['aliexpress.com'],
        'tmall': ['tmall.com'],
        'taobao': ['taobao.com'],
        
        # Developer Tools (3)
        'jsfiddle': ['jsfiddle.net'],
        'npm': ['npmjs.com'],
        'pypi': ['pypi.org'],
        
        # Indian Regional Sites (3)
        'naukri': ['naukri.com'],
        'ndtv': ['ndtv.com'],
        'hotstar': ['hotstar.com', 'disney.com'],
        
        # Others from analysis (2)
        'orbitz': ['orbitz.com'],
        'travelocity': ['travelocity.com'],
        'gamespot': ['gamespot.com'],
        '4shared': ['4shared.com'],
        'sendspace': ['sendspace.com'],
        'archive.org': ['archive.org'],
        'studyblue': ['studyblue.com'],
        'qq': ['qq.com']
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
                f"{first_word}.net",
                f"{first_word}.gov"
            ])
            
            if len(words) >= 2:
                second_word = words[1]
                domains.extend([
                    f"{first_word}{second_word}.com",
                    f"{first_word}-{second_word}.com"
                ])
    
    return list(dict.fromkeys(domains))

def download_logo(website_name, output_dir, category=""):
    """Download logo with comprehensive domain trying"""
    
    with RATE_LIMIT:
        time.sleep(RATE_LIMIT_DELAY)
        
        domains = generate_domains(website_name)
        
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
                    
                    filename = f"{clean_filename(website_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.getsize(filepath) > 500:
                        return f"🌐 {category} | {website_name} -> {filename} (domain: {domain})"
                    else:
                        os.remove(filepath)
                
                # Try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(website_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"📱 {category} | {website_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {category} | {website_name} - No logo found"

def get_priority_missing_websites():
    """Priority missing websites from top 2,500 analysis"""
    return [
        # Health/Medical Sites (4) - Category 2
        ("MedlinePlus", "HEALTH_MEDICAL"),
        ("Drugs.com", "HEALTH_MEDICAL"), 
        ("RxList", "HEALTH_MEDICAL"),
        ("Patient.info", "HEALTH_MEDICAL"),
        
        # Chinese E-commerce (3) - Category 3  
        ("AliExpress", "CHINESE_ECOMMERCE"),
        ("Tmall", "CHINESE_ECOMMERCE"),
        ("Taobao", "CHINESE_ECOMMERCE"),
        
        # Developer Tools (3) - Category 4
        ("JSFiddle", "DEVELOPER_TOOLS"),
        ("NPM", "DEVELOPER_TOOLS"),
        ("PyPI", "DEVELOPER_TOOLS"),
        
        # Indian Regional Sites (3) - Category 5
        ("Naukri", "INDIAN_REGIONAL"),
        ("NDTV", "INDIAN_REGIONAL"),
        ("Hotstar", "INDIAN_REGIONAL"),
        
        # Other High-Traffic Sites
        ("Archive.org", "GOVERNMENT_ORG"),
        ("StudyBlue", "EDUCATIONAL"),
        ("GameSpot", "GAMING"),
        ("Orbitz", "TRAVEL"),
        ("Travelocity", "TRAVEL"),
        ("4shared", "FILE_STORAGE"),
        ("SendSpace", "FILE_STORAGE"),
        ("QQ", "CHINESE_SOCIAL")
    ]

def main():
    # Get priority missing websites
    websites_to_download = get_priority_missing_websites()
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🌐 DOWNLOADING MISSING TOP GLOBAL WEBSITES! 🌐")
    print(f"Downloading {len(websites_to_download)} missing high-traffic websites")
    print(f"Priority Categories: Health/Medical, Chinese E-commerce, Developer Tools, Indian Regional")
    print(f"Current coverage: 89.2% -> Target: 95%+ global website coverage")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print(f"🚀 EXPANDING GLOBAL WEB COVERAGE! 🚀\n")
    
    downloaded_count = 0
    failed_count = 0
    category_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_website = {
            executor.submit(download_logo, website, output_dir, category): (website, category)
            for website, category in websites_to_download
        }
        
        for future in as_completed(future_to_website):
            result = future.result()
            website, category = future_to_website[future]
            print(result)
            
            if result.startswith("🌐") or result.startswith("📱"):
                downloaded_count += 1
                if category not in category_success:
                    category_success[category] = 0
                category_success[category] += 1
            else:
                failed_count += 1
    
    print(f"\n🌐 TOP WEBSITES DOWNLOAD COMPLETE!")
    print(f"Total websites attempted: {len(websites_to_download)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(websites_to_download) > 0:
        print(f"Success rate: {(downloaded_count/len(websites_to_download)*100):.1f}%")
    
    # Calculate new global websites coverage
    total_checked = 316  # From analysis
    remaining_missing = 34 - downloaded_count
    new_coverage = ((total_checked - remaining_missing) / total_checked * 100)
    
    # Update collection count
    previous_total = 8223  # From companies folder
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} company/website logos")
    print(f"🌐 Global websites coverage: {new_coverage:.1f}%")
    
    # Show category success breakdown
    print(f"\n✅ Downloaded by category:")
    for category, count in sorted(category_success.items()):
        print(f"  {category}: {count} websites")
    
    # Achievement summary
    if downloaded_count >= 15:  # If we got most of them
        print(f"\n🔥 MAJOR WEB COVERAGE EXPANSION:")
        print(f"  ✅ Health/Medical: Medical reference platforms")
        print(f"  ✅ Chinese E-commerce: Alibaba ecosystem (AliExpress, Tmall, Taobao)")
        print(f"  ✅ Developer Tools: Package managers and code tools")
        print(f"  ✅ Indian Regional: Job portal, news, streaming")
        
    print(f"\n🌟 ENHANCED GLOBAL WEB PRESENCE!")
    print(f"📈 From top US sites to Chinese giants to Indian platforms!")
    print(f"🎯 PREPARING FOR TOP 3,500 WEBSITES ANALYSIS!")

if __name__ == "__main__":
    main()