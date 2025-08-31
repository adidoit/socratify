#!/usr/bin/env python3
"""
Download ALL 109 missing a16z investment universe companies
Complete coverage of cutting-edge startup ecosystem
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 40
RATE_LIMIT = threading.Semaphore(30)
RATE_LIMIT_DELAY = 0.02

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(company_name):
    """Generate domain variations for a16z portfolio companies"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Massive special cases for a16z universe companies
    special_cases = {
        # AI ML Foundation Models (5)
        'hopsworks': ['hopsworks.ai'],
        'seldon': ['seldon.io'],
        'bentoml': ['bentoml.ai', 'bentoml.com'],
        'determined ai': ['determined.ai'],
        'grid.ai': ['grid.ai'],
        'gridai': ['grid.ai'],
        
        # Crypto Web3 DeFi (6)
        'aptos': ['aptoslabs.com', 'aptos.dev'],
        'livepeer': ['livepeer.org', 'livepeer.com'],
        'tensor': ['tensor.trade', 'tensor.so'],
        'taxbit': ['taxbit.com'],
        'cointracker': ['cointracker.io'],
        'blockdaemon': ['blockdaemon.com'],
        
        # Consumer Social Creator (21) - MASSIVE gap
        'luma': ['lu.ma'],
        'poparazzi': ['poparazzi.com'],
        'dispo': ['dispo.fun'],
        'vsco': ['vsco.co'],
        'locket': ['locket.camera'],
        'sendit': ['senditapp.com'],
        'summer': ['summer.com'],
        'beehiiv': ['beehiiv.com'],
        'revue': ['revue.com', 'getrevue.co'],
        'starsona': ['starsona.com'],
        'koji': ['koji.com', 'withkoji.com'],
        'bio.fm': ['bio.fm'],
        'carrd': ['carrd.co'],
        'guilded': ['guilded.gg'],
        'altspacevr': ['altvr.com'],
        'riverside.fm': ['riverside.fm'],
        'squadcast': ['squadcast.fm'],
        'zencastr': ['zencastr.com'],
        'hindenburg': ['hindenburg.com'],
        'descript': ['descript.com'],
        'sonix': ['sonix.ai'],
        
        # Developer Tools Infrastructure (16)
        'xata': ['xata.io'],
        'edgedb': ['edgedb.com'],
        'tidb': ['pingcap.com'],
        'hasura': ['hasura.io'],
        'prisma': ['prisma.io'],
        'drizzle': ['drizzle.team'],
        'appwrite': ['appwrite.io'],
        'back4app': ['back4app.com'],
        'directus': ['directus.io'],
        'sanity': ['sanity.io'],
        'rudderstack': ['rudderstack.com'],
        'snowplow': ['snowplowanalytics.com'],
        'sonarqube': ['sonarqube.org', 'sonar.io'],
        'semgrep': ['semgrep.dev'],
        'prisma cloud': ['prismacloud.io'],
        'twistlock': ['twistlock.com', 'prismacloud.io'],
        
        # Fintech B2B Payments (20) - MASSIVE gap  
        'checkout.com': ['checkout.com'],
        'dlocal': ['dlocal.com'],
        'concur': ['concur.com', 'sap.com'],
        'tripactions': ['tripactions.com', 'navan.com'],
        'synctera': ['synctera.com'],
        'bond': ['bond.tech'],
        'column': ['column.com'],
        'moov': ['moov.io'],
        'yodlee': ['yodlee.com', 'envestnet.com'],
        'truelayer': ['truelayer.com'],
        'belvo': ['belvo.com'],
        'fintoc': ['fintoc.com'],
        'pluggy': ['pluggy.ai'],
        'commonbond': ['commonbond.co'],
        'homebot': ['homebot.ai'],
        'trueusd': ['trueusd.com'],
        'usdc': ['centre.io', 'coinbase.com'],
        'busd': ['binance.com'],
        'liquity': ['liquity.org'],
        'tokemak': ['tokemak.xyz'],
        
        # Healthcare Biotech Digital (9)
        'wisp': ['hellowisp.com'],
        'celmatix': ['celmatix.com'],
        'cerebral': ['cerebral.com'],
        'sanvello': ['sanvello.com'],
        'daylio': ['daylio.com'],
        'woebot': ['woebot.io'],
        'x2ai': ['x2ai.com'],
        'v2food': ['v2food.com'],
        'redox': ['redoxengine.com'],
        
        # Marketplace Commerce B2B (13)
        'orderchamp': ['orderchamp.com'],
        'creoate': ['creoate.com'],
        'handshake': ['joinhandshake.com'],
        'freshsales': ['freshsales.io', 'freshworks.com'],
        'shippeo': ['shippeo.com'],
        'parcellab': ['parcellab.com'],
        'formlabs': ['formlabs.com'],
        'materialise': ['materialise.com'],
        'xometry': ['xometry.com'],
        'shapeways': ['shapeways.com'],
        'jonas construction': ['jonassoftware.com'],
        'hcss': ['hcss.com'],
        'ineight': ['ineight.com'],
        
        # Future Computing Hardware (8)
        'menten ai': ['menten.ai'],
        'rahko': ['rahko.ai'],
        'augury': ['augury.com'],
        'uptake': ['uptake.com'],
        'c3.ai': ['c3.ai'],
        'blaize': ['blaize.com'],
        'syntiant': ['syntiant.com'],
        'deci ai': ['deci.ai'],
        
        # Climate ESG Impact (11)
        'ebb carbon': ['ebbcarbon.com'],
        'carboncure': ['carboncure.com'],
        'amcs': ['amcsgroup.com'],
        'enevo': ['enevo.com'],
        'bigbelly': ['bigbelly.com'],
        'terracycle': ['terracycle.com'],
        'taranis': ['taranis.com'],
        'farmlogs': ['farmlogs.com'],
        'geltor': ['geltor.com'],
        'quidnet': ['quidnetenergy.com'],
        'ohmium': ['ohmium.com']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback for a16z-style companies
        words = base.split()
        if len(words) == 1:
            domains.extend([
                f"{words[0]}.com",
                f"{words[0]}.ai",
                f"{words[0]}.io",
                f"{words[0]}.co",
                f"{words[0]}.app",
                f"{words[0]}.xyz"
            ])
        elif len(words) == 2:
            domains.extend([
                f"{words[0]}{words[1]}.com",
                f"{words[0]}.com",
                f"{words[0]}.ai",
                f"{words[0]}.io"
            ])
        else:
            domains.extend([
                f"{words[0]}.com",
                f"{words[0]}.ai",
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
                        return f"🚀 {sector} | {company_name} -> {filename} (domain: {domain})"
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
    # ALL 109 MISSING A16Z INVESTMENT UNIVERSE COMPANIES
    a16z_missing = [
        # AI ML Foundation Models (5) - Highest priority
        ("Hopsworks", "AI_ML"),
        ("Seldon", "AI_ML"),
        ("BentoML", "AI_ML"),
        ("Determined AI", "AI_ML"),
        ("Grid.ai", "AI_ML"),
        
        # Crypto Web3 DeFi (6) - Highest priority
        ("Aptos", "CRYPTO"),
        ("Livepeer", "CRYPTO"),
        ("Tensor", "CRYPTO"),
        ("TaxBit", "CRYPTO"),
        ("CoinTracker", "CRYPTO"),
        ("Blockdaemon", "CRYPTO"),
        
        # Consumer Social Creator (21) - MASSIVE GAP
        ("Luma", "CONSUMER"),
        ("Poparazzi", "CONSUMER"),
        ("Dispo", "CONSUMER"),
        ("VSCO", "CONSUMER"),
        ("Locket", "CONSUMER"),
        ("Sendit", "CONSUMER"),
        ("Summer", "CONSUMER"),
        ("Beehiiv", "CONSUMER"),
        ("Revue", "CONSUMER"),
        ("Starsona", "CONSUMER"),
        ("Koji", "CONSUMER"),
        ("Bio.fm", "CONSUMER"),
        ("Carrd", "CONSUMER"),
        ("Guilded", "CONSUMER"),
        ("AltspaceVR", "CONSUMER"),
        ("Riverside.fm", "CONSUMER"),
        ("SquadCast", "CONSUMER"),
        ("Zencastr", "CONSUMER"),
        ("Hindenburg", "CONSUMER"),
        ("Descript", "CONSUMER"),
        ("Sonix", "CONSUMER"),
        
        # Developer Tools Infrastructure (16) - High priority
        ("Xata", "DEVTOOLS"),
        ("EdgeDB", "DEVTOOLS"),
        ("TiDB", "DEVTOOLS"),
        ("Hasura", "DEVTOOLS"),
        ("Prisma", "DEVTOOLS"),
        ("Drizzle", "DEVTOOLS"),
        ("Appwrite", "DEVTOOLS"),
        ("Back4App", "DEVTOOLS"),
        ("Directus", "DEVTOOLS"),
        ("Sanity", "DEVTOOLS"),
        ("Rudderstack", "DEVTOOLS"),
        ("Snowplow", "DEVTOOLS"),
        ("SonarQube", "DEVTOOLS"),
        ("Semgrep", "DEVTOOLS"),
        ("Prisma Cloud", "DEVTOOLS"),
        ("Twistlock", "DEVTOOLS"),
        
        # Fintech B2B Payments (20) - MASSIVE GAP
        ("Checkout.com", "FINTECH"),
        ("dLocal", "FINTECH"),
        ("Concur", "FINTECH"),
        ("TripActions", "FINTECH"),
        ("Synctera", "FINTECH"),
        ("Bond", "FINTECH"),
        ("Column", "FINTECH"),
        ("Moov", "FINTECH"),
        ("Yodlee", "FINTECH"),
        ("TrueLayer", "FINTECH"),
        ("Belvo", "FINTECH"),
        ("Fintoc", "FINTECH"),
        ("Pluggy", "FINTECH"),
        ("CommonBond", "FINTECH"),
        ("Homebot", "FINTECH"),
        ("TrueUSD", "FINTECH"),
        ("USDC", "FINTECH"),
        ("BUSD", "FINTECH"),
        ("Liquity", "FINTECH"),
        ("Tokemak", "FINTECH"),
        
        # Healthcare Biotech Digital (9)
        ("Wisp", "HEALTHCARE"),
        ("Celmatix", "HEALTHCARE"),
        ("Cerebral", "HEALTHCARE"),
        ("Sanvello", "HEALTHCARE"),
        ("Daylio", "HEALTHCARE"),
        ("Woebot", "HEALTHCARE"),
        ("X2AI", "HEALTHCARE"),
        ("v2food", "HEALTHCARE"),
        ("Redox", "HEALTHCARE"),
        
        # Marketplace Commerce B2B (13)
        ("Orderchamp", "B2B"),
        ("Creoate", "B2B"),
        ("Handshake", "B2B"),
        ("Freshsales", "B2B"),
        ("Shippeo", "B2B"),
        ("ParcelLab", "B2B"),
        ("Formlabs", "B2B"),
        ("Materialise", "B2B"),
        ("Xometry", "B2B"),
        ("Shapeways", "B2B"),
        ("Jonas Construction", "B2B"),
        ("HCSS", "B2B"),
        ("InEight", "B2B"),
        
        # Future Computing Hardware (8)
        ("Menten AI", "FUTURE_TECH"),
        ("Rahko", "FUTURE_TECH"),
        ("Augury", "FUTURE_TECH"),
        ("Uptake", "FUTURE_TECH"),
        ("C3.ai", "FUTURE_TECH"),
        ("Blaize", "FUTURE_TECH"),
        ("Syntiant", "FUTURE_TECH"),
        ("Deci AI", "FUTURE_TECH"),
        
        # Climate ESG Impact (11)
        ("Ebb Carbon", "CLIMATE"),
        ("CarbonCure", "CLIMATE"),
        ("AMCS", "CLIMATE"),
        ("Enevo", "CLIMATE"),
        ("Bigbelly", "CLIMATE"),
        ("TerraCycle", "CLIMATE"),
        ("Taranis", "CLIMATE"),
        ("FarmLogs", "CLIMATE"),
        ("Geltor", "CLIMATE"),
        ("Quidnet", "CLIMATE"),
        ("Ohmium", "CLIMATE")
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🚀💥 COMPLETE A16Z UNIVERSE DOWNLOAD 💥🚀")
    print(f"Downloading ALL {len(a16z_missing)} missing a16z companies")
    print(f"Target: 80.5% -> 100% a16z investment universe coverage")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print(f"🔥 CUTTING-EDGE STARTUP ECOSYSTEM COMPLETION! 🔥\n")
    
    downloaded_count = 0
    failed_count = 0
    sector_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, sector): (company, sector)
            for company, sector in a16z_missing
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company, sector = future_to_company[future]
            print(result)
            
            if result.startswith("🚀") or result.startswith("🔍"):
                downloaded_count += 1
                if sector not in sector_success:
                    sector_success[sector] = 0
                sector_success[sector] += 1
            else:
                failed_count += 1
    
    print(f"\n✅ A16Z UNIVERSE COMPLETION DONE!")
    print(f"Total a16z companies: {len(a16z_missing)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(a16z_missing) > 0:
        print(f"Success rate: {(downloaded_count/len(a16z_missing)*100):.1f}%")
    
    # Calculate new a16z coverage
    total_a16z_companies = 560
    remaining_missing = 109 - downloaded_count
    new_coverage = ((total_a16z_companies - remaining_missing) / total_a16z_companies * 100)
    
    # Update collection count
    previous_total = 8378  # From Goldman completion
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"🚀 a16z investment universe coverage: {new_coverage:.1f}%")
    print(f"✅ CUTTING-EDGE STARTUP ECOSYSTEM DOMINANCE!")
    
    # Show sector success breakdown
    print(f"\n🎯 Downloads by sector:")
    for sector, count in sorted(sector_success.items()):
        print(f"  {sector}: {count} companies")
    
    # Show key a16z gaps filled
    if downloaded_count >= 80:  # If we got most of them
        print(f"\n🔥 Major a16z investment gaps filled:")
        print(f"  • AI/ML Infrastructure: Hopsworks, Seldon, BentoML")
        print(f"  • Web3/Crypto: Aptos, Livepeer, TaxBit") 
        print(f"  • Consumer Social: VSCO, Dispo, Luma, Beehiiv")
        print(f"  • Developer Tools: Hasura, Prisma, Sanity, Xata")
        print(f"  • FinTech B2B: Checkout.com, dLocal, TripActions")
        print(f"  • Future Computing: C3.ai, Augury, Uptake")
        
    print(f"\n🌟 THE MOST CUTTING-EDGE BUSINESS LOGO COLLECTION!")

if __name__ == "__main__":
    main()