#!/usr/bin/env python3
"""
Download Master Global Expansion Companies
288 companies from 7 regions: US, Japan, South Korea, Southeast Asia, Latin America, Australia/NZ, Russia
Final comprehensive expansion to complete global business ecosystem coverage
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 30
RATE_LIMIT = threading.Semaphore(20)  # Max 20 concurrent requests
RATE_LIMIT_DELAY = 0.03  # 30ms delay between requests

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)  # Keep only alphanumeric, spaces, hyphens
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with single underscore
    filename = re.sub(r'_+', '_', filename)  # Replace multiple underscores with single
    filename = filename.strip('_')  # Remove leading/trailing underscores
    return filename

def generate_domains(company_name):
    """Generate possible domain variations for global companies"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    base = base.replace('|', '')
    
    # Split into words
    words = base.split()
    
    domains = []
    
    if len(words) == 1:
        domains.extend([
            f"{words[0]}.com",
            f"{words[0]}.co.jp",
            f"{words[0]}.co.kr", 
            f"{words[0]}.com.sg",
            f"{words[0]}.com.br",
            f"{words[0]}.com.au",
            f"{words[0]}.ru",
            f"{words[0]}.co.uk"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com",
            f"{words[1]}.com"
        ])
    elif len(words) >= 3:
        # First two words
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}.com"
        ])
        
        # Try acronym (first letters)
        acronym = ''.join(word[0] for word in words if word)
        if len(acronym) >= 2:
            domains.extend([
                f"{acronym}.com",
                f"{acronym}.co.jp",
                f"{acronym}.co.kr"
            ])
    
    # Comprehensive special domain mappings for expansion companies
    special_cases = {
        # US Companies
        'apple': ['apple.com'],
        'microsoft': ['microsoft.com'],
        'amazon': ['amazon.com'],
        'nvidia': ['nvidia.com'],
        'alphabet': ['abc.xyz', 'google.com'],
        'tesla': ['tesla.com'],
        'meta': ['meta.com'],
        'taiwan semiconductor': ['tsmc.com'],
        'berkshire hathaway': ['berkshirehathaway.com'],
        'eli lilly': ['lilly.com'],
        'broadcom': ['broadcom.com'],
        'jpmorgan chase': ['jpmorgan.com', 'jpmorganchase.com'],
        'visa': ['visa.com'],
        'unitedhealth': ['unitedhealthgroup.com'],
        'exxon mobil': ['exxonmobil.com'],
        'mastercard': ['mastercard.com'],
        'spacex': ['spacex.com'],
        'stripe': ['stripe.com'],
        
        # Japanese Companies  
        'toyota motor': ['toyota.com'],
        'sony group': ['sony.com'],
        'nintendo': ['nintendo.com'],
        'softbank group': ['softbank.com'],
        'keyence': ['keyence.com'],
        'recruit holdings': ['recruit.co.jp'],
        'tokyo electron': ['tel.com'],
        'shin-etsu chemical': ['shinetsu.co.jp'],
        'kddi': ['kddi.com'],
        'ntt': ['ntt.com'],
        'japan tobacco': ['jt.com'],
        'murata manufacturing': ['murata.com'],
        'daikin industries': ['daikin.com'],
        'fast retailing': ['fastretailing.com'],
        'uniqlo': ['uniqlo.com'],
        'rakuten group': ['rakuten.com'],
        'mercari': ['mercari.com'],
        'mitsubishi corporation': ['mitsubishi.com'],
        'mitsui & co': ['mitsui.com'],
        'itochu corporation': ['itochu.com'],
        'sumitomo corporation': ['sumitomo.com'],
        'honda motor': ['honda.com'],
        'nissan motor': ['nissan-global.com'],
        'suzuki motor': ['globalsuzuki.com'],
        'mazda motor': ['mazda.com'],
        
        # South Korean Companies
        'samsung electronics': ['samsung.com'],
        'sk hynix': ['skhynix.com'],
        'samsung sdi': ['samsungsdi.com'],
        'lg energy solution': ['lgensol.com'],
        'naver corporation': ['navercorp.com'],
        'kakao': ['kakaocorp.com'],
        'celltrion': ['celltrion.com'],
        'samsung biologics': ['samsungbiologics.com'],
        'lg electronics': ['lge.com'],
        'lg chem': ['lgchem.com'],
        'posco': ['posco.com'],
        'hyundai motor': ['hyundai.com'],
        'kia corporation': ['kia.com'],
        'hybe corporation': ['hybecorp.com'],
        'sm entertainment': ['smtown.com'],
        'yg entertainment': ['ygfamily.com'],
        'jyp entertainment': ['jype.com'],
        'netmarble': ['netmarble.com'],
        'ncsoft': ['ncsoft.com'],
        'nexon': ['nexon.com'],
        
        # Southeast Asian Companies
        'dbs group': ['dbs.com'],
        'ocbc bank': ['ocbc.com'],
        'united overseas bank': ['uob.com.sg'],
        'singapore airlines': ['singaporeair.com'],
        'singapore technologies engineering': ['stengg.com'],
        'keppel corporation': ['kepcorp.com'],
        'capitaland': ['capitaland.com'],
        'grab': ['grab.com'],
        'sea limited': ['sea.com'],
        'razer': ['razer.com'],
        'bank central asia': ['bca.co.id'],
        'bank rakyat indonesia': ['bri.co.id'],
        'bank mandiri': ['bankmandiri.co.id'],
        'telkom indonesia': ['telkom.co.id'],
        'astra international': ['astra.co.id'],
        'goto group': ['goto.com'],
        'traveloka': ['traveloka.com'],
        'tokopedia': ['tokopedia.com'],
        
        # Latin American Companies
        'vale': ['vale.com'],
        'petrobras': ['petrobras.com.br'],
        'itau unibanco': ['itau.com.br'],
        'banco bradesco': ['bradesco.com.br'],
        'ambev': ['ambev.com.br'],
        'magazine luiza': ['magazineluiza.com.br'],
        'jbs': ['jbs.com.br'],
        'nubank': ['nubank.com.br'],
        'ifood': ['ifood.com.br'],
        'stone': ['stone.com.br'],
        'mercado libre': ['mercadolibre.com'],
        'america movil': ['americamovil.com'],
        'grupo televisa': ['televisa.com'],
        'walmart mexico': ['walmart.com.mx'],
        'cemex': ['cemex.com'],
        
        # Australian/NZ Companies
        'bhp group': ['bhp.com'],
        'commonwealth bank': ['commbank.com.au'],
        'csl limited': ['csl.com'],
        'westpac banking corporation': ['westpac.com.au'],
        'australia and new zealand banking group': ['anz.com'],
        'national australia bank': ['nab.com.au'],
        'woolworths group': ['woolworthsgroup.com.au'],
        'telstra corporation': ['telstra.com.au'],
        'rio tinto': ['riotinto.com'],
        'macquarie group': ['macquarie.com'],
        'canva': ['canva.com'],
        'atlassian': ['atlassian.com'],
        'afterpay': ['afterpay.com'],
        'xero': ['xero.com'],
        
        # Russian Companies
        'sberbank': ['sberbank.com'],
        'gazprom': ['gazprom.com'],
        'rosneft': ['rosneft.com'],
        'lukoil': ['lukoil.com'],
        'novatek': ['novatek.ru'],
        'vtb bank': ['vtb.com'],
        'norilsk nickel': ['nornickel.com'],
        'yandex': ['yandex.com'],
        'nlmk': ['nlmk.com'],
        'mmk': ['mmk.ru'],
        'severstal': ['severstal.com'],
        'alrosa': ['alrosa.ru'],
        'magnit': ['magnit.com'],
        'mts': ['mts.ru'],
        'sistema': ['sistema.com'],
        'vk': ['vk.company'],
        'kaspersky lab': ['kaspersky.com'],
        'jetbrains': ['jetbrains.com'],
        'ozon': ['ozon.ru'],
        'megafon': ['megafon.ru'],
        'rostelecom': ['rostelecom.ru'],
        'avtovaz': ['lada.ru'],
        'gaz group': ['gazgroup.ru'],
        'kamaz': ['kamaz.ru'],
        'x5 retail group': ['x5.ru'],
        'aeroflot': ['aeroflot.com'],
        's7 airlines': ['s7.ru']
    }
    
    if base in special_cases:
        domains = special_cases[base] + domains
    
    return list(dict.fromkeys(domains))  # Remove duplicates while preserving order

def download_logo(company_name, output_dir, region=""):
    """Download logo for a company with clean filename"""
    
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
                    
                    # Clean filename - just the company name
                    filename = f"{clean_filename(company_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Download and save
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Check if file is valid (non-empty)
                    if os.path.getsize(filepath) > 500:  # At least 500 bytes
                        return f"✅ {region} | {company_name} -> {filename}"
                    else:
                        os.remove(filepath)
                
                # Also try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(company_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"🔍 {region} | {company_name} -> {filename}"
                
            except Exception as e:
                continue
        
        return f"❌ {region} | {company_name} - No logo found"

def main():
    # Parse the expansion missing companies file
    with open('/Users/adi/code/socratify/socratify-yolo/expansion_companies_to_download.txt', 'r') as f:
        content = f.read()
    
    # Handle both actual newlines and escaped newlines
    content = content.replace('\\n', '\n')
    
    # Extract companies with regions
    companies_with_regions = []
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and len(line) > 0 and line[0].isdigit() and '. ' in line:
            # Extract company name and region
            parts = line.split('. ', 1)
            if len(parts) > 1:
                rest = parts[1]
                if ' (' in rest and rest.endswith(')'):
                    company_name = rest[:rest.rfind(' (')]
                    region = rest[rest.rfind(' (') + 2:-1]
                    companies_with_regions.append((company_name, region))
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting download of {len(companies_with_regions)} expansion companies...")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("MASTER GLOBAL EXPANSION COVERAGE:")
    print("- United States: S&P 500, NASDAQ, Fortune 500, Unicorns")
    print("- Japan: Nikkei 225, Conglomerates, Tech Giants")
    print("- South Korea: KOSPI, Chaebols, K-pop/Gaming")
    print("- Southeast Asia: Singapore, Indonesia, Thailand, Malaysia, Philippines, Vietnam")
    print("- Latin America: Brazil, Mexico, Argentina, Chile, Colombia, Peru") 
    print("- Australia/NZ: ASX 200, Tech Unicorns")
    print("- Russia: MOEX, Energy Giants, Tech Companies\\n")
    
    # Track by region
    regional_stats = {}
    for company, region in companies_with_regions:
        if region not in regional_stats:
            regional_stats[region] = {'downloaded': 0, 'failed': 0}
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks
        future_to_company = {
            executor.submit(download_logo, company, output_dir, region): (company, region)
            for company, region in companies_with_regions
        }
        
        # Process completed tasks
        for future in as_completed(future_to_company):
            result = future.result()
            company, region = future_to_company[future]
            print(result)
            
            if result.startswith("✅") or result.startswith("🔍"):
                downloaded_count += 1
                regional_stats[region]['downloaded'] += 1
            else:
                failed_count += 1
                regional_stats[region]['failed'] += 1
    
    print(f"\\n=== MASTER GLOBAL EXPANSION DOWNLOAD COMPLETE ===")
    print(f"Total companies: {len(companies_with_regions)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(companies_with_regions) > 0:
        print(f"Success rate: {(downloaded_count/len(companies_with_regions)*100):.1f}%")
    
    print(f"\\n=== REGIONAL BREAKDOWN ===")
    for region, stats in regional_stats.items():
        total = stats['downloaded'] + stats['failed']
        success_rate = (stats['downloaded'] / total * 100) if total > 0 else 0
        print(f"{region}: {stats['downloaded']}/{total} ({success_rate:.1f}%)")
    
    # Update collection count
    previous_total = 7864  # Count after global regional download (UK, Canada, EU, China, Africa, Middle East)
    new_total = previous_total + downloaded_count
    print(f"\\nCollection now has approximately: {new_total} logos")
    print(f"🎉 WORLD'S MOST COMPREHENSIVE BUSINESS LOGO COLLECTION COMPLETE!")
    print(f"Covers ALL major business ecosystems globally:")
    print(f"✅ North America (US, Canada)")
    print(f"✅ Europe (UK, EU, Russia)")
    print(f"✅ Asia-Pacific (Japan, South Korea, Southeast Asia, China, Australia/NZ)")
    print(f"✅ Latin America (Brazil, Mexico, Argentina, Chile, Colombia, Peru)")
    print(f"✅ Africa (South Africa, Nigeria, Egypt, Kenya, Morocco, Ghana)")
    print(f"✅ Middle East (GCC, Israel, Turkey)")

if __name__ == "__main__":
    main()