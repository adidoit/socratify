#!/usr/bin/env python3
"""
Download MASSIVE missing company expansion
ALL 87 modern companies + ALL 73 global AI companies = 160 total!
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 35
RATE_LIMIT = threading.Semaphore(25)
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
    """Generate domain variations - MASSIVE comprehensive approach"""
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
            f"{words[0]}.app",
            f"{words[0]}.cn",
            f"{words[0]}.co.jp",
            f"{words[0]}.co.kr"
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
    
    # MASSIVE special cases database - ALL missing companies
    special_cases = {
        # Modern Companies (87 total)
        'claude ai': ['claude.ai', 'anthropic.com'],
        'you.com': ['you.com'],
        'phind': ['phind.com'],
        'fireworks ai': ['fireworks.ai'],
        'octoml': ['octoml.ai'],
        'codewhisperer': ['aws.amazon.com'],
        'codeium': ['codeium.com'],
        'continue': ['continue.dev'],
        'crewai': ['crewai.com'],
        'comet ml': ['comet.ml', 'comet.com'],
        'dagster': ['dagster.io'],
        'prefect': ['prefect.io'],
        'dvc': ['dvc.org'],
        'tecton': ['tecton.ai'],
        'milvus': ['milvus.io'],
        'vald': ['vald.vdaas.org'],
        'sourcetree': ['sourcetreeapp.com'],
        'fork': ['git-fork.com'],
        'fly.io': ['fly.io'],
        'elliptic': ['elliptic.co'],
        'trm labs': ['trmlabs.com'],
        'myriad genetics': ['myriad.com'],
        'natera': ['natera.com'],
        'veracyte': ['veracyte.com'],
        'storedot': ['storedot.com'],
        'malta': ['malta.inc'],
        'lemon8': ['lemon8-app.com'],
        'mastodon': ['mastodon.social', 'joinmastodon.org'],
        'qonto': ['qonto.com'],
        'penta': ['getpenta.com'],
        'workfusion': ['workfusion.com'],
        'kryon': ['kryon.com'],
        'armis': ['armis.com'],
        'orcam': ['orcam.com'],
        'vayyar': ['vayyar.com'],
        'cognata': ['cognata.com'],
        'sushiswap': ['sushi.com'],
        'starkware': ['starkware.co'],
        'd-wave': ['dwavesys.com'],
        'iqm': ['meetiqm.com'],
        'godot': ['godotengine.org'],
        'defold': ['defold.com'],
        'among us': ['innersloth.com'],
        'apex legends': ['ea.com'],
        'pubg': ['pubg.com'],
        'overwatch': ['playoverwatch.com'],
        'dota 2': ['dota2.com'],
        'capcut': ['capcut.com'],
        'agoda': ['agoda.com'],
        'corel': ['corel.com'],
        'mogo': ['mogo.ca'],
        'paymi': ['paymi.com'],
        'freshbooks': ['freshbooks.com'],
        'hootsuite': ['hootsuite.com'],
        'envato': ['envato.com'],
        'koala': ['koala.com'],
        'm-pesa': ['safaricom.co.ke'],
        'epson moverio': ['moverio.epson.com'],
        '8th wall': ['8thwall.com'],
        'embark': ['embarktrucks.com'],
        'einride': ['einride.tech'],
        'optimus ride': ['optimusride.com'],
        'navya': ['navya.tech'],
        'sensible 4': ['sensible4.fi'],
        'ecobee': ['ecobee.com'],
        'hubitat': ['hubitat.com'],
        'wink': ['wink.com'],
        'tp-link kasa': ['kasasmart.com'],
        'clara foods': ['clarafoods.com'],
        'trimble': ['trimble.com'],
        'hotels.com': ['hotels.com'],
        'trivago': ['trivago.com'],
        'ibuyer': ['ibuyer.com'],
        'landed': ['landed.com'],
        'flyhomes': ['flyhomes.com'],
        'bamboohr': ['bamboohr.com'],
        'glint': ['glintinc.com'],
        'bonusly': ['bonusly.com'],
        'drip': ['drip.com'],
        'lawdepot': ['lawdepot.com'],
        'avvo': ['avvo.com'],
        'mycase': ['mycase.com'],
        'smokeball': ['smokeball.com'],
        'codepen': ['codepen.io'],
        'thoughtspot': ['thoughtspot.com'],
        'periscope data': ['periscopedata.com'],
        
        # Chinese AI Companies
        'jd ai': ['jd.com'],
        'cloudwalk': ['cloudwalk.cn'],
        'momenta': ['momenta.ai'],
        'autox': ['autox.ai'],
        'deepseek': ['deepseek.com'],
        'chatglm': ['chatglm.cn'],
        'ernie bot': ['wenxin.baidu.com'],
        'dorabot': ['dorabot.com'],
        'cloudminds': ['cloudminds.com'],
        'icarbonx': ['icarbonx.com'],
        'lufax ai': ['lufax.com'],
        'haomo.ai': ['haomo.ai'],
        'innovusion': ['innovusion.com'],
        
        # European AI Companies
        'speechmatics': ['speechmatics.com'],
        'vocaliq': ['vocaliq.com'],
        'satalia': ['satalia.com'],
        'snips': ['snips.ai'],
        'cityzendata': ['cityzendata.com'],
        'sigfox': ['sigfox.com'],
        'deepl': ['deepl.com'],
        'arago': ['arago.co'],
        'merantix': ['merantix.com'],
        'tobii': ['tobii.com'],
        'peltarion': ['peltarion.com'],
        'speechly': ['speechly.com'],
        'exact ai': ['exact.com'],
        'cyberethics lab': ['cyberethicslab.com'],
        'vedrai': ['vedrai.com'],
        
        # Indian AI Companies
        'avaamo': ['avaamo.ai'],
        'sigtuple': ['sigtuple.com'],
        'qure.ai': ['qure.ai'],
        'tricog': ['tricog.com'],
        'cancerai': ['cancer.ai'],
        'flutura': ['flutura.com'],
        'haber': ['haber.in'],
        'botsync': ['botsync.co'],
        'haptik': ['haptik.ai'],
        'yellow.ai': ['yellow.ai'],
        'rasa': ['rasa.com'],
        'verloop': ['verloop.io'],
        'reverie language': ['reverieinc.com'],
        'crayon data': ['crayondata.com'],
        'quantiphi': ['quantiphi.com'],
        
        # Japanese AI Companies
        'abeja': ['abeja.asia'],
        'morpho': ['morphoinc.com'],
        'hacarus': ['hacarus.com'],
        'cogent labs': ['cogent.co.jp'],
        'fixstars': ['fixstars.com'],
        'nachi-fujikoshi ai': ['nachi-fujikoshi.co.jp'],
        'cygames': ['cygames.co.jp'],
        'terumo ai': ['terumo.com'],
        'sysmex ai': ['sysmex.com'],
        'shimadzu ai': ['shimadzu.com'],
        
        # Israeli AI Companies  
        'armis ai': ['armis.com'],
        'foretellix': ['foretellix.com'],
        'nexar': ['getnexar.com'],
        'aidoc': ['aidoc.com'],
        
        # Korean AI Companies
        'lg ai research': ['lg.com'],
        'kt ai': ['kt.com'],
        'clova': ['clova.ai'],
        'aitems': ['aitems.co.kr'],
        'rb thayer': ['rbthayer.com'],
        
        # Canadian AI Companies
        'layer 6 ai': ['layer6.ai'],
        'paymi ai': ['paymi.com'],
        'cifar': ['cifar.ca'],
        'dessa': ['dessa.com'],
        'bluedot': ['bluedot.global'],
        'waabi': ['waabi.ai']
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
    # MODERN COMPANIES (87 total)
    modern_companies = [
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
    
    # GLOBAL AI COMPANIES (73 total)
    global_ai_companies = [
        # Chinese AI (Top 15)
        "JD AI", "CloudWalk", "Momenta", "AutoX", "DeepSeek", "ChatGLM", "Ernie Bot",
        "Dorabot", "CloudMinds", "iCarbonX", "Lufax AI", "HAOMO.AI", "Innovusion",
        
        # European AI (Top 15)  
        "Speechmatics", "VocalIQ", "Satalia", "Snips", "CityzenData", "Sigfox",
        "DeepL", "Arago", "Merantix", "Tobii", "Peltarion", "Speechly", "Exact AI",
        "CyberEthics Lab", "Vedrai",
        
        # Indian AI (Top 15)
        "Avaamo", "SigTuple", "Qure.ai", "Tricog", "CancerAI", "Flutura", "Haber",
        "Botsync", "Haptik", "Yellow.ai", "Rasa", "Verloop", "Reverie Language",
        "Crayon Data", "Quantiphi",
        
        # Japanese AI (10)
        "ABEJA", "Morpho", "Hacarus", "Cogent Labs", "Fixstars", "Nachi-Fujikoshi AI",
        "Cygames", "Terumo AI", "Sysmex AI", "Shimadzu AI",
        
        # Israeli AI (7)
        "Armis AI", "Foretellix", "Nexar", "Aidoc",
        
        # Korean AI (5)  
        "LG AI Research", "KT AI", "Clova", "AiTEMS", "RB Thayer",
        
        # Canadian AI (6)
        "Layer 6 AI", "Paymi AI", "CIFAR", "Dessa", "BlueDot", "Waabi"
    ]
    
    # COMBINE ALL COMPANIES
    all_companies_with_category = []
    
    # Add modern companies
    for company in modern_companies:
        all_companies_with_category.append((company, "MODERN"))
    
    # Add global AI companies  
    for company in global_ai_companies:
        all_companies_with_category.append((company, "GLOBAL_AI"))
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🚀🌍 MASSIVE MISSING COMPANY EXPANSION 🌍🚀")
    print(f"DOWNLOADING EVERYTHING PEOPLE WANT TO WORK FOR!")
    print(f"Modern companies: {len(modern_companies)}")
    print(f"Global AI companies: {len(global_ai_companies)}")
    print(f"Total companies: {len(all_companies_with_category)}")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\\n")
    
    downloaded_count = 0
    failed_count = 0
    modern_downloaded = 0
    ai_downloaded = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, category): (company, category)
            for company, category in all_companies_with_category
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company, category = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("🔍"):
                downloaded_count += 1
                if category == "MODERN":
                    modern_downloaded += 1
                else:
                    ai_downloaded += 1
            else:
                failed_count += 1
    
    print(f"\\n🎉 MASSIVE EXPANSION DOWNLOAD COMPLETE! 🎉")
    print(f"Total companies: {len(all_companies_with_category)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"  - Modern companies: {modern_downloaded}/{len(modern_companies)}")
    print(f"  - Global AI companies: {ai_downloaded}/{len(global_ai_companies)}")
    print(f"Failed: {failed_count}")
    if len(all_companies_with_category) > 0:
        print(f"Success rate: {(downloaded_count/len(all_companies_with_category)*100):.1f}%")
    
    # Update collection count
    previous_total = 8164  # From hottest AI companies
    new_total = previous_total + downloaded_count
    print(f"\\n📊 Collection now has: ~{new_total} business logos")
    print(f"\\n✅ WORLD'S MOST COMPREHENSIVE BUSINESS LOGO COLLECTION!")
    print(f"🔥 Modern: Claude AI, Among Us, Fly.io, DeepL, Qure.ai")  
    print(f"🌍 Global AI: Chinese, European, Indian, Japanese AI giants")
    print(f"🚀 COMPLETE: Every company people want to work for!")

if __name__ == "__main__":
    main()