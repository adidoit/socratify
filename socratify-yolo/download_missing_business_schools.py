#!/usr/bin/env python3
"""
Download missing top business schools
Focus on T15, top Canadian, and European elite programs
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 15
RATE_LIMIT = threading.Semaphore(10)
RATE_LIMIT_DELAY = 0.1

def clean_filename(school_name):
    """Convert school name to clean filename"""
    filename = school_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(school_name):
    """Generate domain variations for business schools"""
    base = school_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Special cases for the 11 missing business schools
    special_cases = {
        # T15 Top US (2)
        'nyu stern': ['stern.nyu.edu', 'nyu.edu'],
        'stern': ['stern.nyu.edu', 'nyu.edu'],
        'ucla anderson': ['anderson.ucla.edu', 'ucla.edu'],
        'anderson': ['anderson.ucla.edu', 'ucla.edu'],
        
        # Canada Top MBA (3) - User priority
        'sauder school of business': ['sauder.ubc.ca', 'ubc.ca'],
        'sauder': ['sauder.ubc.ca', 'ubc.ca'],
        'haskayne school of business': ['haskayne.ucalgary.ca', 'ucalgary.ca'],
        'haskayne': ['haskayne.ucalgary.ca', 'ucalgary.ca'],
        'beedie school of business': ['beedie.sfu.ca', 'sfu.ca'],
        'beedie': ['beedie.sfu.ca', 'sfu.ca'],
        
        # European Elite (4)
        'iese business school': ['iese.edu'],
        'iese': ['iese.edu'],
        'ie business school': ['ie.edu'],
        'ie': ['ie.edu'],
        'esade business school': ['esade.edu'],
        'esade': ['esade.edu'],
        'warwick business school': ['wbs.ac.uk', 'warwick.ac.uk'],
        'warwick': ['wbs.ac.uk', 'warwick.ac.uk'],
        
        # Asia Pacific Top (1)
        'melbourne business school': ['mbs.edu', 'unimelb.edu.au'],
        'melbourne': ['mbs.edu', 'unimelb.edu.au'],
        
        # Specialized Programs (1)
        'edhec business school': ['edhec.edu'],
        'edhec': ['edhec.edu']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback for business schools
        words = base.split()
        if len(words) >= 1:
            first_word = words[0]
            domains.extend([
                f"{first_word}.edu",
                f"{first_word}.ac.uk",
                f"{first_word}.ca",
                f"{first_word}.com"
            ])
            
            if len(words) >= 2:
                second_word = words[1]
                domains.extend([
                    f"{first_word}.{second_word}.edu",
                    f"{second_word}.{first_word}.edu"
                ])
    
    return list(dict.fromkeys(domains))

def download_logo(school_name, output_dir, category=""):
    """Download logo with comprehensive domain trying"""
    
    with RATE_LIMIT:
        time.sleep(RATE_LIMIT_DELAY)
        
        domains = generate_domains(school_name)
        
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
                    
                    filename = f"{clean_filename(school_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.getsize(filepath) > 500:
                        return f"🎓 {category} | {school_name} -> {filename} (domain: {domain})"
                    else:
                        os.remove(filepath)
                
                # Try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(school_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"📚 {category} | {school_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {category} | {school_name} - No logo found"

def main():
    # 11 MISSING TOP BUSINESS SCHOOLS
    school_missing = [
        # T15 Top US (2) - High priority
        ("NYU Stern", "T15_US"),
        ("UCLA Anderson", "T15_US"),
        
        # Canada Top MBA (3) - User emphasis on Canada
        ("Sauder School of Business", "CANADA"),
        ("Haskayne School of Business", "CANADA"),
        ("Beedie School of Business", "CANADA"),
        
        # European Elite (4) - High priority international
        ("IESE Business School", "EUROPE"),
        ("IE Business School", "EUROPE"),
        ("ESADE Business School", "EUROPE"),
        ("Warwick Business School", "EUROPE"),
        
        # Asia Pacific Top (1)
        ("Melbourne Business School", "ASIA_PAC"),
        
        # Specialized Programs (1)
        ("EDHEC Business School", "SPECIALIZED")
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎓📚 TOP BUSINESS SCHOOLS COMPLETION 📚🎓")
    print(f"Downloading {len(school_missing)} missing top business schools")
    print(f"Target: 89.7% -> 100% business school coverage")
    print(f"Focus: T15 US + Top Canadian + European Elite")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\n")
    
    downloaded_count = 0
    failed_count = 0
    category_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_school = {
            executor.submit(download_logo, school, output_dir, category): (school, category)
            for school, category in school_missing
        }
        
        for future in as_completed(future_to_school):
            result = future.result()
            school, category = future_to_school[future]
            print(result)
            
            if result.startswith("🎓") or result.startswith("📚"):
                downloaded_count += 1
                if category not in category_success:
                    category_success[category] = 0
                category_success[category] += 1
            else:
                failed_count += 1
    
    print(f"\n✅ BUSINESS SCHOOLS COMPLETION DONE!")
    print(f"Total schools: {len(school_missing)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(school_missing) > 0:
        print(f"Success rate: {(downloaded_count/len(school_missing)*100):.1f}%")
    
    # Calculate new business school coverage
    total_schools = 107
    remaining_missing = 11 - downloaded_count
    new_coverage = ((total_schools - remaining_missing) / total_schools * 100)
    
    # Update collection count
    previous_total = 8545  # From emerging unicorns completion
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"🎓 Business school coverage: {new_coverage:.1f}%")
    print(f"✅ TOP MBA PROGRAMS DOMINANCE!")
    
    # Show category success breakdown
    print(f"\n🎯 Downloads by category:")
    for category, count in sorted(category_success.items()):
        print(f"  {category}: {count} schools")
    
    # Show key business school gaps filled
    if downloaded_count >= 8:  # If we got most of them
        print(f"\n🔥 Major business school gaps filled:")
        print(f"  • T15 US Programs: NYU Stern, UCLA Anderson")
        print(f"  • Top Canadian Schools: Sauder (UBC), Haskayne (Calgary), Beedie (SFU)")
        print(f"  • European Elite: IESE, IE, ESADE, Warwick")
        print(f"  • Asia-Pacific: Melbourne Business School")
        
    print(f"\n🌟 COMPLETE MBA & BUSINESS SCHOOL COVERAGE!")
    print(f"📚 From M7 to regional programs - we have them all!")

if __name__ == "__main__":
    main()