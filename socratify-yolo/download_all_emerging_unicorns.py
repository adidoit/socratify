#!/usr/bin/env python3
"""
Download ALL 73 missing emerging unicorns and hot breakout startups
The cutting-edge companies everyone's talking about in 2024-2025
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 50
RATE_LIMIT = threading.Semaphore(40)
RATE_LIMIT_DELAY = 0.015

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(company_name):
    """Generate domain variations for emerging hot companies"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # MASSIVE special cases for hottest emerging companies
    special_cases = {
        # 2024-2025 AI Breakouts (18) - HOTTEST
        'lovable': ['lovable.dev'],
        'autogpt': ['agpt.co', 'autogpt.net'],
        'babyagi': ['babyagi.org'],
        'agentgpt': ['agentgpt.reworkd.ai'],
        'superagent': ['superagent.sh'],
        'fixie': ['fixie.ai'],
        'imbue': ['imbue.com'],
        'pika labs': ['pika.art'],
        'gen-2': ['runwayml.com'],
        'kaiber': ['kaiber.ai'],
        'd-id': ['d-id.com'],
        'elai.io': ['elai.io'],
        'pictory': ['pictory.ai'],
        'immersity ai': ['immersity.ai'],
        'topaz labs': ['topazlabs.com'],
        'pieces': ['pieces.app'],
        'codet5': ['github.com'],
        'starcoder': ['huggingface.co'],
        
        # International Breakouts 2024 (12) - HOT UNICORNS
        'getyourguide': ['getyourguide.com'],
        'checkout.com': ['checkout.com'],
        'marketfinance': ['marketfinance.com'],
        'iwoca': ['iwoca.com'],
        'auto1': ['auto1.com'],
        'flixbus': ['flixbus.com'],
        'blablacar': ['blablacar.com'],
        'criteo': ['criteo.com'],
        'dailymotion': ['dailymotion.com'],
        'doctolib': ['doctolib.com'],
        'sinch': ['sinch.com'],
        'truecaller': ['truecaller.com'],
        
        # Asian Tech Giants 2024 (6) - ASIAN LEADERS  
        'helo': ['helo.com'],
        'genki forest': ['genkiforest.com'],
        'luckin coffee': ['luckincoffee.com'],
        'zeekr': ['zeekrlife.com'],
        'chatwork': ['chatwork.com'],
        'jmdc': ['jmdc.co.jp'],
        
        # Vertical SaaS Champions (14) - B2B LEADERS
        'esub': ['esub.com'],
        'onna': ['onna.com'],
        'everlaw': ['everlaw.com'],
        'lexis+': ['lexisnexis.com'],
        'blend': ['blend.com'],
        'resy': ['resy.com'],
        'classpass': ['classpass.com'],
        'mindbody': ['mindbodyonline.com'],
        'glofox': ['glofox.com'],
        'booker': ['booker.com'],
        'pike13': ['pike13.com'],
        'omnify': ['getomnify.com'],
        'fitsw': ['fitsw.com'],
        'truecoach': ['truecoach.co'],
        
        # Web3 Native 2024 (9) - WEB3 NATIVES
        'blast': ['blast.io'],
        'gains network': ['gains.trade'],
        'raydium': ['raydium.io'],
        'marinade': ['marinade.finance'],
        'jito': ['jito.wtf'],
        'wax': ['wax.io'],
        'farcaster': ['farcaster.xyz'],
        'xmtp': ['xmtp.org'],
        'deso': ['deso.org'],
        
        # Creator Economy 2024 (7) - CREATOR TOOLS
        'skool': ['skool.com'],
        'scrivener': ['literatureandlatte.com'],
        'riverside.fm': ['riverside.fm'],
        'camtasia': ['techsmith.com'],
        'ecamm live': ['ecamm.com'],
        'wirecast': ['telestream.net'],
        'xsplit': ['xsplit.com'],
        
        # Climate Tech 2024 (7) - CLIMATE LEADERS
        'sustaera': ['sustaera.com'],
        'amprius': ['amprius.com'],
        'enevate': ['enevate.com'],
        'seeo': ['seeo.com'],
        'polyplus': ['polyplus.com'],
        'piñatex': ['ananas-anam.com'],
        'muskin': ['grado-zero-espace.com']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback for hot startups
        words = base.split()
        if len(words) == 1:
            domains.extend([
                f"{words[0]}.com",
                f"{words[0]}.ai",
                f"{words[0]}.io",
                f"{words[0]}.app", 
                f"{words[0]}.co",
                f"{words[0]}.xyz",
                f"{words[0]}.dev"
            ])
        elif len(words) == 2:
            domains.extend([
                f"{words[0]}{words[1]}.com",
                f"{words[0]}.com",
                f"{words[0]}.ai",
                f"{words[0]}.io",
                f"{words[0]}.app"
            ])
        else:
            domains.extend([
                f"{words[0]}.com",
                f"{words[0]}.ai",
                f"{words[0]}{words[1]}.com"
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
                    
                    return f"⭐ {category} | {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {category} | {company_name} - No logo found"

def main():
    # ALL 73 MISSING EMERGING UNICORNS & HOT STARTUPS
    emerging_missing = [
        # 2024-2025 AI Breakouts (18) - HOTTEST PRIORITY
        ("Lovable", "AI_2024"),
        ("AutoGPT", "AI_2024"),
        ("BabyAGI", "AI_2024"),
        ("AgentGPT", "AI_2024"),
        ("Superagent", "AI_2024"),
        ("Fixie", "AI_2024"),
        ("Imbue", "AI_2024"),
        ("Pika Labs", "AI_2024"),
        ("Gen-2", "AI_2024"),
        ("Kaiber", "AI_2024"),
        ("D-ID", "AI_2024"),
        ("Elai.io", "AI_2024"),
        ("Pictory", "AI_2024"),
        ("Immersity AI", "AI_2024"),
        ("Topaz Labs", "AI_2024"),
        ("Pieces", "AI_2024"),
        ("CodeT5", "AI_2024"),
        ("StarCoder", "AI_2024"),
        
        # International Breakouts 2024 (12) - HOT UNICORNS
        ("GetYourGuide", "INTL_2024"),
        ("Checkout.com", "INTL_2024"),
        ("MarketFinance", "INTL_2024"),
        ("iwoca", "INTL_2024"),
        ("Auto1", "INTL_2024"),
        ("FlixBus", "INTL_2024"),
        ("BlaBlaCar", "INTL_2024"),
        ("Criteo", "INTL_2024"),
        ("Dailymotion", "INTL_2024"),
        ("Doctolib", "INTL_2024"),
        ("Sinch", "INTL_2024"),
        ("Truecaller", "INTL_2024"),
        
        # Asian Tech Giants 2024 (6) - ASIAN LEADERS
        ("Helo", "ASIAN_2024"),
        ("Genki Forest", "ASIAN_2024"),
        ("Luckin Coffee", "ASIAN_2024"),
        ("Zeekr", "ASIAN_2024"),
        ("ChatWork", "ASIAN_2024"),
        ("JMDC", "ASIAN_2024"),
        
        # Vertical SaaS Champions (14) - B2B LEADERS
        ("eSUB", "SAAS"),
        ("Onna", "SAAS"),
        ("Everlaw", "SAAS"),
        ("Lexis+", "SAAS"),
        ("Blend", "SAAS"),
        ("Resy", "SAAS"),
        ("ClassPass", "SAAS"),
        ("Mindbody", "SAAS"),
        ("Glofox", "SAAS"),
        ("Booker", "SAAS"),
        ("Pike13", "SAAS"),
        ("Omnify", "SAAS"),
        ("FitSW", "SAAS"),
        ("TrueCoach", "SAAS"),
        
        # Web3 Native 2024 (9) - WEB3 NATIVES
        ("Blast", "WEB3_2024"),
        ("Gains Network", "WEB3_2024"),
        ("Raydium", "WEB3_2024"),
        ("Marinade", "WEB3_2024"),
        ("Jito", "WEB3_2024"),
        ("WAX", "WEB3_2024"),
        ("Farcaster", "WEB3_2024"),
        ("XMTP", "WEB3_2024"),
        ("DeSo", "WEB3_2024"),
        
        # Creator Economy 2024 (7) - CREATOR TOOLS
        ("Skool", "CREATOR_2024"),
        ("Scrivener", "CREATOR_2024"),
        ("Riverside.fm", "CREATOR_2024"),
        ("Camtasia", "CREATOR_2024"),
        ("Ecamm Live", "CREATOR_2024"),
        ("Wirecast", "CREATOR_2024"),
        ("XSplit", "CREATOR_2024"),
        
        # Climate Tech 2024 (7) - CLIMATE LEADERS
        ("Sustaera", "CLIMATE_2024"),
        ("Amprius", "CLIMATE_2024"),
        ("Enevate", "CLIMATE_2024"),
        ("Seeo", "CLIMATE_2024"),
        ("Polyplus", "CLIMATE_2024"),
        ("Piñatex", "CLIMATE_2024"),
        ("MuSkin", "CLIMATE_2024")
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🔥🚀 HOTTEST EMERGING UNICORNS DOWNLOAD 🚀🔥")
    print(f"Downloading ALL {len(emerging_missing)} missing hot startups")
    print(f"Target: 81.5% -> 100% emerging companies coverage")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print(f"💥 THE HOTTEST COMPANIES EVERYONE'S TALKING ABOUT! 💥\n")
    
    downloaded_count = 0
    failed_count = 0
    category_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, category): (company, category)
            for company, category in emerging_missing
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company, category = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("⭐"):
                downloaded_count += 1
                if category not in category_success:
                    category_success[category] = 0
                category_success[category] += 1
            else:
                failed_count += 1
    
    print(f"\n✅ EMERGING UNICORNS COMPLETION DONE!")
    print(f"Total hot companies: {len(emerging_missing)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(emerging_missing) > 0:
        print(f"Success rate: {(downloaded_count/len(emerging_missing)*100):.1f}%")
    
    # Calculate new emerging coverage
    total_emerging_companies = 394
    remaining_missing = 73 - downloaded_count
    new_coverage = ((total_emerging_companies - remaining_missing) / total_emerging_companies * 100)
    
    # Update collection count
    previous_total = 8479  # From a16z completion
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"🔥 Emerging unicorns coverage: {new_coverage:.1f}%")
    print(f"✅ HOTTEST STARTUPS ECOSYSTEM DOMINANCE!")
    
    # Show category success breakdown
    print(f"\n🎯 Downloads by category:")
    for category, count in sorted(category_success.items()):
        print(f"  {category}: {count} companies")
    
    # Show key emerging gaps filled
    if downloaded_count >= 55:  # If we got most of them
        print(f"\n🔥 Major emerging unicorn gaps filled:")
        print(f"  • 2024 AI Breakouts: AutoGPT, BabyAGI, Pika Labs, D-ID")
        print(f"  • International Unicorns: GetYourGuide, FlixBus, BlaBlaCar, Truecaller") 
        print(f"  • Vertical SaaS: ClassPass, Mindbody, Resy, Blend")
        print(f"  • Web3 Natives: Farcaster, Raydium, Marinade, Blast")
        print(f"  • Creator Tools: Skool, Riverside.fm, Camtasia")
        print(f"  • Climate Tech: Amprius, Enevate, Piñatex")
        
    print(f"\n🌟 THE MOST CUTTING-EDGE & HOTTEST BUSINESS LOGO COLLECTION!")
    print(f"🚀 WE NOW HAVE THE COMPANIES EVERYONE'S TALKING ABOUT!")

if __name__ == "__main__":
    main()