#!/usr/bin/env python3
"""
Download final 9 missing McKinsey sector companies
Complete sector-by-sector coverage
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
RATE_LIMIT_DELAY = 0.05

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(company_name):
    """Generate domain variations for sector companies"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Special cases for the 9 missing sector companies
    special_cases = {
        # Technology Media Telecom (2)
        'citrix': ['citrix.com'],
        'telefónica': ['telefonica.com', 'movistar.com'],
        'telefonica': ['telefonica.com', 'movistar.com'],
        
        # Healthcare Pharma Medtech (1)
        'alnylam pharmaceuticals': ['alnylam.com'],
        'alnylam': ['alnylam.com'],
        
        # Consumer Packaged Goods (1)
        "l'oréal": ['loreal.com', 'loreal.fr'],
        'loreal': ['loreal.com', 'loreal.fr'],
        
        # Energy Power Materials (1)
        'saipem': ['saipem.com', 'saipem.it'],
        
        # Chemicals Materials (1)
        'wacker chemie': ['wacker.com'],
        'wacker': ['wacker.com'],
        
        # Retail Consumer Services (1)
        'pvh': ['pvh.com'],
        'pvh corp': ['pvh.com'],
        
        # Real Estate Infrastructure (1)
        'masco': ['masco.com'],
        'masco corporation': ['masco.com'],
        
        # Public Social Sector (1)
        'mitre corporation': ['mitre.org'],
        'mitre': ['mitre.org']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback
        words = base.split()
        if len(words) == 1:
            domains.extend([
                f"{words[0]}.com",
                f"{words[0]}.org"
            ])
        elif len(words) == 2:
            domains.extend([
                f"{words[0]}{words[1]}.com",
                f"{words[0]}.com",
                f"{words[1]}.com"
            ])
        else:
            domains.extend([
                f"{words[0]}.com",
                f"{words[0]}{words[1]}.com"
            ])
    
    return list(dict.fromkeys(domains))

def download_logo(company_name, output_dir, sector=""):
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
                        return f"🔥 {sector} | {company_name} -> {filename} (domain: {domain})"
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
                    
                    return f"🔍 {sector} | {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {sector} | {company_name} - No logo found"

def main():
    # 9 MISSING MCKINSEY SECTOR COMPANIES
    sector_missing = [
        # Technology Media Telecom (2) - Highest priority
        ("Citrix", "TECH"),
        ("Telefónica", "TECH"),
        
        # Healthcare Pharma Medtech (1)
        ("Alnylam Pharmaceuticals", "HEALTHCARE"),
        
        # Consumer Packaged Goods (1)
        ("L'Oréal", "CONSUMER"),
        
        # Energy Power Materials (1)
        ("Saipem", "ENERGY"),
        
        # Chemicals Materials (1)
        ("Wacker Chemie", "CHEMICALS"),
        
        # Retail Consumer Services (1)
        ("PVH", "RETAIL"),
        
        # Real Estate Infrastructure (1)
        ("Masco", "REAL_ESTATE"),
        
        # Public Social Sector (1)
        ("MITRE Corporation", "PUBLIC")
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🏭 MCKINSEY SECTOR GAPS COMPLETION 🏭")
    print(f"Downloading {len(sector_missing)} final sector companies")
    print(f"Target: 98.0% -> 100.0% sector coverage")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\n")
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, sector): (company, sector)
            for company, sector in sector_missing
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company, sector = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("🔍"):
                downloaded_count += 1
            else:
                failed_count += 1
    
    print(f"\n✅ MCKINSEY SECTOR COMPLETION DONE!")
    print(f"Total sector companies: {len(sector_missing)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(sector_missing) > 0:
        print(f"Success rate: {(downloaded_count/len(sector_missing)*100):.1f}%")
    
    # Calculate new sector coverage
    total_sector_companies = 440
    remaining_missing = failed_count
    new_coverage = ((total_sector_companies - remaining_missing) / total_sector_companies * 100)
    
    # Update collection count
    previous_total = 8333  # From Fortune completion
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"🏭 McKinsey sector coverage: {new_coverage:.1f}%")
    print(f"✅ SECTOR-BY-SECTOR DOMINANCE ACHIEVED!")
    
    # Show what we accomplished
    sectors_completed = set()
    for company, sector in sector_missing:
        if company in [r.split(' -> ')[0].split(' | ')[1] for r in [result] if r.startswith("🔥") or r.startswith("🔍")]:
            sectors_completed.add(sector)
    
    print(f"\n🎯 Completed sectors: {', '.join(sorted(sectors_completed))}")

if __name__ == "__main__":
    main()