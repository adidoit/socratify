#!/usr/bin/env python3
"""
Download ALL 87 missing modern companies + find even more
Go AGGRESSIVE on coverage - download everything people want to work for
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 30
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
    """Generate domain variations for modern companies - AGGRESSIVE approach"""
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
            f"{words[0]}.ai", 
            f"{words[0]}.io",
            f"{words[0]}.co",
            f"{words[0]}.tech",
            f"{words[0]}.app"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com",
            f"{words[1]}.com",
            f"{words[0]}.ai",
            f"{words[0]}.io"
        ])
    elif len(words) >= 3:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}.com",
            f"{words[0]}.ai",
            f"{words[0]}.io"
        ])
    
    # COMPREHENSIVE special cases - EVERY modern company we know
    special_cases = {
        # AI Foundation Models
        'claude ai': ['claude.ai', 'anthropic.com'],
        'you.com': ['you.com'],
        'phind': ['phind.com'],
        'fireworks ai': ['fireworks.ai'],
        'octoml': ['octoml.ai'],
        
        # AI Agents & Automation
        'codewhisperer': ['aws.amazon.com'],
        'codeium': ['codeium.com'],
        'continue': ['continue.dev'],
        'crewai': ['crewai.com'],
        
        # AI Infrastructure & MLOps
        'comet ml': ['comet.ml', 'comet.com'],
        'dagster': ['dagster.io'],
        'prefect': ['prefect.io'],
        'dvc': ['dvc.org'],
        'tecton': ['tecton.ai'],
        'milvus': ['milvus.io'],
        'vald': ['vald.vdaas.org'],
        
        # Developer Tools
        'sourcetree': ['sourcetreeapp.com'],
        'fork': ['git-fork.com'],
        'fly.io': ['fly.io'],
        
        # Fintech & Payments
        'elliptic': ['elliptic.co'],
        'trm labs': ['trmlabs.com'],
        
        # Healthcare & Biotech
        'myriad genetics': ['myriad.com'],
        'natera': ['natera.com'],
        'veracyte': ['veracyte.com'],
        
        # Climate Tech
        'storedot': ['storedot.com'],
        'malta': ['malta.inc'],
        
        # Consumer & Social
        'lemon8': ['lemon8-app.com'],
        'mastodon': ['mastodon.social', 'joinmastodon.org'],
        
        # European Tech
        'qonto': ['qonto.com'],
        'penta': ['getpenta.com'],
        'workfusion': ['workfusion.com'],
        'kryon': ['kryon.com'],
        
        # Israeli Tech
        'armis': ['armis.com'],
        'orcam': ['orcam.com'],
        'vayyar': ['vayyar.com'],
        'cognata': ['cognata.com'],
        
        # Crypto & Web3
        'sushiswap': ['sushi.com'],
        'starkware': ['starkware.co'],
        
        # Quantum Computing
        'd-wave': ['dwavesys.com'],
        'iqm': ['meetiqm.com'],
        
        # Gaming & Entertainment
        'godot': ['godotengine.org'],
        'defold': ['defold.com'],
        'among us': ['innersloth.com'],
        'apex legends': ['ea.com'],
        'pubg': ['pubg.com'],
        'overwatch': ['playoverwatch.com'],
        'dota 2': ['dota2.com'],
        
        # Asian Tech
        'capcut': ['capcut.com'],
        'agoda': ['agoda.com'],
        
        # Canadian Tech
        'corel': ['corel.com'],
        'mogo': ['mogo.ca'],
        'paymi': ['paymi.com'],
        'freshbooks': ['freshbooks.com'],
        'hootsuite': ['hootsuite.com'],
        
        # Australian Tech
        'envato': ['envato.com'],
        'koala': ['koala.com'],
        
        # African Tech
        'm-pesa': ['safaricom.co.ke'],
        
        # AR/VR & Spatial
        'epson moverio': ['moverio.epson.com'],
        '8th wall': ['8thwall.com'],
        
        # Autonomous Transportation
        'embark': ['embarktrucks.com'],
        'einride': ['einride.tech'],
        'optimus ride': ['optimusride.com'],
        'navya': ['navya.tech'],
        'sensible 4': ['sensible4.fi'],
        
        # IoT & Connected
        'ecobee': ['ecobee.com'],
        'hubitat': ['hubitat.com'],
        'wink': ['wink.com'],
        'tp-link kasa': ['kasasmart.com'],
        
        # Food & AgTech
        'clara foods': ['clarafoods.com'],
        'trimble': ['trimble.com'],
        
        # Travel & Hospitality
        'hotels.com': ['hotels.com'],
        'trivago': ['trivago.com'],
        
        # Real Estate & PropTech
        'ibuyer': ['ibuyer.com'],
        'landed': ['landed.com'],
        'flyhomes': ['flyhomes.com'],
        
        # HR Tech
        'bamboohr': ['bamboohr.com'],
        'glint': ['glintinc.com'],
        'bonusly': ['bonusly.com'],
        
        # Marketing & AdTech
        'drip': ['drip.com'],
        
        # Legal Tech
        'lawdepot': ['lawdepot.com'],
        'avvo': ['avvo.com'],
        'mycase': ['mycase.com'],
        'smokeball': ['smokeball.com'],
        
        # Education Tech
        'codepen': ['codepen.io'],
        
        # Data & Analytics
        'thoughtspot': ['thoughtspot.com'],
        'periscope data': ['periscopedata.com']
    }
    
    if base in special_cases:
        domains = special_cases[base] + domains
    
    return list(dict.fromkeys(domains))

def download_logo(company_name, output_dir):
    """Download logo for modern company with aggressive domain trying"""
    
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
                        return f"🔥 {company_name} -> {filename} (domain: {domain})"
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
                    
                    return f"🔍 {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {company_name} - No logo found"

def main():
    # ALL 87 missing modern companies
    all_missing_companies = [
        # AI Foundation Models
        "Claude AI", "You.com", "Phind", "Fireworks AI", "OctoML",
        
        # AI Agents & Automation  
        "CodeWhisperer", "Codeium", "Continue", "CrewAI",
        
        # AI Infrastructure & MLOps
        "Comet ML", "Dagster", "Prefect", "DVC", "Tecton", "Milvus", "Vald",
        
        # Developer Tools
        "Sourcetree", "Fork", "Fly.io",
        
        # Fintech & Payments
        "Elliptic", "TRM Labs",
        
        # Healthcare & Biotech
        "Myriad Genetics", "Natera", "Veracyte",
        
        # Climate Tech
        "StoreDot", "Malta",
        
        # Consumer & Social
        "Lemon8", "Mastodon",
        
        # European Tech
        "Qonto", "Penta", "WorkFusion", "Kryon",
        
        # Israeli Tech
        "Armis", "OrCam", "Vayyar", "Cognata",
        
        # Crypto & Web3
        "SushiSwap", "StarkWare",
        
        # Quantum Computing
        "D-Wave", "IQM",
        
        # Gaming & Entertainment
        "Godot", "Defold", "Among Us", "Apex Legends", "PUBG", "Overwatch", "Dota 2",
        
        # Asian Tech
        "CapCut", "Agoda",
        
        # Canadian Tech
        "Corel", "Mogo", "Paymi", "FreshBooks", "Hootsuite",
        
        # Australian Tech
        "Envato", "Koala",
        
        # African Tech
        "M-Pesa",
        
        # AR/VR & Spatial
        "Epson Moverio", "8th Wall",
        
        # Autonomous Transportation
        "Embark", "Einride", "Optimus Ride", "Navya", "Sensible 4",
        
        # IoT & Connected
        "Ecobee", "Hubitat", "Wink", "TP-Link Kasa",
        
        # Food & AgTech
        "Clara Foods", "Trimble",
        
        # Travel & Hospitality
        "Hotels.com", "Trivago",
        
        # Real Estate & PropTech
        "iBuyer", "Landed", "Flyhomes",
        
        # HR Tech
        "BambooHR", "Glint", "Bonusly",
        
        # Marketing & AdTech
        "Drip",
        
        # Legal Tech
        "LawDepot", "Avvo", "MyCase", "Smokeball",
        
        # Education Tech
        "CodePen",
        
        # Data & Analytics
        "ThoughtSpot", "Periscope Data"
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🚀 DOWNLOADING ALL MISSING MODERN COMPANIES 🚀")
    print(f"AGGRESSIVE COMPREHENSIVE COVERAGE!")
    print(f"Total companies: {len(all_missing_companies)}")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\\n")
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir): company
            for company in all_missing_companies
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("🔍"):
                downloaded_count += 1
            else:
                failed_count += 1
    
    print(f"\\n🎉 ALL MISSING MODERN COMPANIES DOWNLOAD COMPLETE! 🎉")
    print(f"Total companies: {len(all_missing_companies)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(all_missing_companies) > 0:
        print(f"Success rate: {(downloaded_count/len(all_missing_companies)*100):.1f}%")
    
    # Update collection count
    previous_total = 8164  # From hottest AI companies
    new_total = previous_total + downloaded_count
    print(f"\\n📊 Collection now has: ~{new_total} business logos")
    print(f"\\n✅ AGGRESSIVE MODERN COMPANY COVERAGE COMPLETE!")
    print(f"🔥 AI: Claude AI, You.com, Phind, CodeWhisperer, Codeium")  
    print(f"🎮 Gaming: Among Us, Apex Legends, PUBG, Overwatch, Dota 2")
    print(f"💻 Dev Tools: Fly.io, Dagster, Prefect, Sourcetree")
    print(f"🚀 Modern: All the companies people are dying to work for!")

if __name__ == "__main__":
    main()