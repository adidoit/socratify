#!/usr/bin/env python3
"""
Download obvious missing major brands + Fortune 1000 expansion
Reebok, Converse, JBL, DC Comics, etc.
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 25
RATE_LIMIT = threading.Semaphore(20)
RATE_LIMIT_DELAY = 0.03

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(company_name):
    """Generate domain variations for major brands"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    # Split into words
    words = base.split()
    
    domains = []
    
    # Standard domain patterns
    if len(words) == 1:
        domains.extend([
            f"{words[0]}.com",
            f"{words[0]}.net", 
            f"{words[0]}.org",
            f"{words[0]}.co",
            f"{words[0]}.io",
            f"www.{words[0]}.com"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com",
            f"{words[1]}.com"
        ])
    elif len(words) >= 3:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}.com",
            f"{words[-1]}.com"
        ])
    
    # Special cases for major brands
    special_cases = {
        # Athletic Apparel
        'reebok': ['reebok.com'],
        'converse': ['converse.com'],
        'fila': ['fila.com'],
        'asics': ['asics.com'],
        
        # Food & Beverage
        'in-n-out burger': ['in-n-out.com'],
        'chick-fil-a': ['chick-fil-a.com'],
        
        # Automotive
        'maybach': ['mercedes-maybach.com', 'maybach.com'],
        
        # Tech Hardware
        'msi': ['msi.com'],
        'jbl': ['jbl.com', 'harman.com'],
        'shure': ['shure.com'],
        
        # Financial Services
        'bb&t': ['bbt.com', 'truist.com'],
        
        # Hotels
        'st. regis': ['marriott.com', 'stregis.com'],
        'waldorf astoria': ['waldorfastoria.com', 'hilton.com'],
        'doubletree': ['doubletree.com', 'hilton.com'],
        'hampton inn': ['hamptoninn.com', 'hilton.com'],
        
        # Consumer Brands
        "l'oréal": ['loreal.com'],
        'estée lauder': ['esteelauder.com'],
        'maybelline': ['maybelline.com'],
        
        # Entertainment
        'dc comics': ['dccomics.com', 'dc.com'],
        
        # Telecom
        'altice usa': ['alticeusa.com', 'optimum.net']
    }
    
    if base in special_cases:
        domains = special_cases[base] + domains
    
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
                        return f"🔥 {category} | {company_name} -> {filename} (domain: {domain})"
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
                    
                    return f"🔍 {category} | {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {category} | {company_name} - No logo found"

def main():
    # OBVIOUS MISSING BRANDS (20 total)
    obvious_missing_brands = [
        # Athletic Apparel (4)
        ("Reebok", "ATHLETIC"),
        ("Converse", "ATHLETIC"),  
        ("Fila", "ATHLETIC"),
        ("ASICS", "ATHLETIC"),
        
        # Food & Beverage (2)
        ("In-N-Out Burger", "FOOD"),
        ("Chick-fil-A", "FOOD"),
        
        # Automotive (1)
        ("Maybach", "AUTOMOTIVE"),
        
        # Tech Hardware (3)
        ("MSI", "TECH"),
        ("JBL", "TECH"),
        ("Shure", "TECH"),
        
        # Financial Services (1)
        ("BB&T", "FINANCIAL"),
        
        # Hotels (4)
        ("St. Regis", "HOTELS"),
        ("Waldorf Astoria", "HOTELS"),
        ("DoubleTree", "HOTELS"), 
        ("Hampton Inn", "HOTELS"),
        
        # Consumer Brands (3)
        ("L'Oréal", "CONSUMER"),
        ("Estée Lauder", "CONSUMER"),
        ("Maybelline", "CONSUMER"),
        
        # Entertainment (1)
        ("DC Comics", "ENTERTAINMENT"),
        
        # Telecom (1) 
        ("Altice USA", "TELECOM")
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🎯 OBVIOUS MISSING BRANDS DOWNLOAD 🎯")
    print(f"Downloading {len(obvious_missing_brands)} obvious major brands")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\n")
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, category): (company, category)
            for company, category in obvious_missing_brands
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company, category = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("🔍"):
                downloaded_count += 1
            else:
                failed_count += 1
    
    print(f"\n✅ OBVIOUS BRANDS DOWNLOAD COMPLETE!")
    print(f"Total brands: {len(obvious_missing_brands)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(obvious_missing_brands) > 0:
        print(f"Success rate: {(downloaded_count/len(obvious_missing_brands)*100):.1f}%")
    
    # Update collection count
    previous_total = 8312  # From massive expansion
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"🎯 Added obvious major brands: Reebok, Converse, JBL, DC Comics!")

if __name__ == "__main__":
    main()