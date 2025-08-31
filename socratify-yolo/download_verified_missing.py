#!/usr/bin/env python3
"""
Download verified missing MBA employer logos
83 companies that we definitely don't have
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import hashlib

# Configuration
MAX_WORKERS = 12
RATE_LIMIT = threading.Semaphore(8)  # Max 8 concurrent requests
RATE_LIMIT_DELAY = 0.15  # 150ms delay between requests

def generate_domains(company_name):
    """Generate possible domain variations"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    base = base.replace('[', '').replace(']', '')
    base = base.replace('{', '').replace('}', '')
    
    # Split into words
    words = base.split()
    
    domains = []
    
    if len(words) == 1:
        domains.extend([
            f"{words[0]}.com",
            f"{words[0]}.io", 
            f"{words[0]}.co",
            f"{words[0]}.net"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com",
            f"{words[1]}.com",
            f"{words[0]}{words[1]}.io",
            f"{words[0]}-{words[1]}.io"
        ])
    elif len(words) >= 3:
        # First two words
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com"
        ])
        
        # Try acronym (first letters)
        acronym = ''.join(word[0] for word in words if word)
        if len(acronym) >= 2:
            domains.extend([
                f"{acronym}.com",
                f"{acronym}.io"
            ])
    
    # Special cases
    special_cases = {
        'johnson & johnson': ['jnj.com', 'jandj.com'],
        'bristol myers squibb': ['bms.com', 'bmymellon.com'],
        'eli lilly': ['lilly.com'],
        'ab inbev': ['ab-inbev.com', 'anheuser-busch.com'],
        'estee lauder': ['esteelauder.com', 'elcompanies.com'],
        'bcg': ['bcg.com'],
        'booz allen hamilton': ['boozallen.com'],
        'warburg pincus': ['warburgpincus.com'],
        'silver lake': ['silverlake.com'],
        'thoma bravo': ['thomabravo.com'],
        'autodesk': ['autodesk.com'],
        'calendly': ['calendly.com'],
        'clearbit': ['clearbit.com'],
        'clubhouse': ['clubhouse.com'],
        'datarobot': ['datarobot.com'],
        'digitalocean': ['digitalocean.com'],
        'gocardless': ['gocardless.com'],
        'klaviyo': ['klaviyo.com'],
        'launchdarkly': ['launchdarkly.com'],
        'lime': ['li.me', 'lime.bike'],
        'postman': ['postman.com', 'getpostman.com'],
        'sendgrid': ['sendgrid.com'],
        'wiz': ['wiz.io'],
        'lucid motors': ['lucidmotors.com'],
        'rocket lab': ['rocketlabusa.com'],
        'relativity space': ['relativityspace.com'],
        'iheartradio': ['iheartradio.com', 'iheart.com'],
        'bandcamp': ['bandcamp.com'],
        'soundcloud': ['soundcloud.com'],
        'take-two': ['take2games.com'],
        'riot games': ['riotgames.com'],
        'unity technologies': ['unity.com', 'unity3d.com'],
        'cma cgm': ['cma-cgm.com'],
        'hapag-lloyd': ['hapag-lloyd.com'],
        'db schenker': ['dbschenker.com'],
        'kuehne + nagel': ['kuehne-nagel.com'],
        'c.h. robinson': ['chrobinson.com'],
        'xpo logistics': ['xpo.com'],
        'j.b. hunt': ['jbhunt.com'],
        'schneider national': ['schneider.com'],
        'cushman & wakefield': ['cushmanwakefield.com'],
        'marcus & millichap': ['marcusmillichap.com'],
        'public storage': ['publicstorage.com'],
        'equity residential': ['equityresidential.com']
    }
    
    if base in special_cases:
        domains = special_cases[base] + domains
    
    return list(dict.fromkeys(domains))  # Remove duplicates while preserving order

def download_logo(company_name, output_dir):
    """Download logo for a company"""
    
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
                    
                    # Skip if not an image
                    if 'image' not in content_type and 'octet-stream' not in content_type:
                        continue
                    
                    # Get file extension
                    if 'png' in content_type:
                        ext = 'png'
                    elif 'jpeg' in content_type or 'jpg' in content_type:
                        ext = 'jpg'
                    elif 'svg' in content_type:
                        ext = 'svg'
                    elif 'webp' in content_type:
                        ext = 'webp'
                    else:
                        ext = 'png'  # Default
                    
                    # Clean filename
                    clean_name = company_name.replace('&', 'and').replace(' ', '_').replace('.', '').replace(',', '').replace("'", '').replace('"', '')
                    filename = f"{clean_name}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Download and save
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Check if file is valid (non-empty)
                    if os.path.getsize(filepath) > 500:  # At least 500 bytes
                        return f"✅ {company_name} -> {filename} ({domain})"
                    else:
                        os.remove(filepath)
                
                # Also try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    clean_name = company_name.replace('&', 'and').replace(' ', '_').replace('.', '').replace(',', '').replace("'", '').replace('"', '')
                    filename = f"{clean_name}_favicon.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"🔍 {company_name} -> {filename} (favicon from {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {company_name} - No logo found"

def main():
    # List of 83 verified missing companies
    missing_companies = [
        "BCG", "Booz Allen Hamilton", "Warburg Pincus", "Silver Lake", "Thoma Bravo",
        "AB InBev", "Estee Lauder", "Johnson & Johnson", "Bristol Myers Squibb", "Eli Lilly",
        "AutoDesk", "Benchling", "Calendly", "Clearbit", "Clubhouse", "DataRobot",
        "DigitalOcean", "GoCardless", "Klaviyo", "LaunchDarkly", "Lime", "Postman",
        "SendGrid", "Wiz", "Lucid Motors", "Rocket Lab", "Relativity Space",
        "iHeartRadio", "Bandcamp", "SoundCloud", "Take-Two", "Riot Games",
        "Unity Technologies", "CMA CGM", "Hapag-Lloyd", "DB Schenker", "Kuehne + Nagel",
        "C.H. Robinson", "XPO Logistics", "J.B. Hunt", "Schneider National",
        "Cushman & Wakefield", "Marcus & Millichap", "Public Storage", "Equity Residential",
        "AvalonBay", "WeWork", "IWG", "Industrious", "Zillow", "Redfin", "Opendoor",
        "Compass", "Vrbo", "Booking.com", "Tripadvisor", "AIG", "Chubb", "Travelers",
        "Progressive", "Geico", "State Farm", "Allstate", "Liberty Mutual", "MetLife",
        "Prudential Financial", "New York Life", "Northwestern Mutual", "BlackRock",
        "Vanguard", "State Street", "Invesco", "Franklin Templeton", "T. Rowe Price",
        "Stellantis", "Renault", "Peugeot", "Citroen", "Maserati", "Lamborghini",
        "Bentley", "Rolls-Royce Motor Cars", "McLaren", "Aston Martin", "Volvo Cars",
        "Polestar", "Genesis", "Waymo", "Cruise"
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting download of {len(missing_companies)} verified missing MBA employer logos...")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\n")
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks
        future_to_company = {
            executor.submit(download_logo, company, output_dir): company 
            for company in missing_companies
        }
        
        # Process completed tasks
        for future in as_completed(future_to_company):
            result = future.result()
            print(result)
            
            if result.startswith("✅") or result.startswith("🔍"):
                downloaded_count += 1
            else:
                failed_count += 1
    
    print(f"\n=== DOWNLOAD COMPLETE ===")
    print(f"Total companies: {len(missing_companies)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    print(f"Success rate: {(downloaded_count/len(missing_companies)*100):.1f}%")

if __name__ == "__main__":
    main()