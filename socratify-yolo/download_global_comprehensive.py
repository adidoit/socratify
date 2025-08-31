#!/usr/bin/env python3
"""
Download comprehensive global companies from all regions
UK, Canada, EU, China, Africa, Middle East - 365 companies total
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
            f"{words[0]}.co.uk",
            f"{words[0]}.ca", 
            f"{words[0]}.eu",
            f"{words[0]}.cn",
            f"{words[0]}.com.cn",
            f"{words[0]}.co.za",
            f"{words[0]}.ae",
            f"{words[0]}.sa"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}{words[1]}.co.uk",
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
                f"{acronym}.co.uk",
                f"{acronym}.ca"
            ])
    
    # Comprehensive special domain mappings for global companies
    special_cases = {
        # UK Companies
        'hsbc holdings': ['hsbc.com'],
        'british american tobacco': ['bat.com'],
        'rio tinto group': ['riotinto.com'],
        'relx': ['relx.com'],
        'legal & general': ['legalandgeneral.com'],
        'admiral group': ['admiral.com'],
        'sage group': ['sage.com'],
        'rolls-royce holdings': ['rolls-royce.com'],
        'bae systems': ['baesystems.com'],
        'marks & spencer': ['marksandspencer.com'],
        'jd sports': ['jdsports.com'],
        "sainsbury's": ['sainsburys.co.uk'],
        'bt group': ['bt.com'],
        'itv': ['itv.com'],
        'starling bank': ['starlingbank.com'],
        'zopa': ['zopa.com'],
        'oaknorth bank': ['oaknorth.com'],
        'lighthouse': ['lighthousehq.com'],
        'mews': ['mews.com'],
        'wayve': ['wayve.ai'],
        'elevenlabs': ['elevenlabs.io'],
        'unitary': ['unitary.ai'],
        'games workshop': ['games-workshop.com'],
        
        # Canadian Companies
        'brookfield corporation': ['brookfield.com'],
        'bank of montreal': ['bmo.com'],
        'thomson reuters corporation': ['thomsonreuters.com'],
        'bank of nova scotia': ['scotiabank.com'],
        'alimentation couche-tard': ['couche-tard.com'],
        'manulife financial corporation': ['manulife.com'],
        'tc energy corporation': ['tcenergy.com'],
        'suncor energy': ['suncor.com'],
        'sun life financial': ['sunlife.com'],
        'intact financial corporation': ['intact.ca'],
        'national bank of canada': ['nbc.ca'],
        'restaurant brands international': ['rbi.com'],
        'barrick gold corporation': ['barrick.com'],
        'canadian natural resources': ['cnrl.com'],
        'cenovus energy': ['cenovus.com'],
        'imperial oil': ['imperialoil.ca'],
        'pembina corporation': ['pembina.com'],
        'parkland corporation': ['parkland.ca'],
        'royal bank of canada': ['rbc.com'],
        'toronto-dominion bank': ['td.com'],
        'canadian imperial bank of commerce': ['cibc.com'],
        'rogers communications': ['rogers.com'],
        'bell canada': ['bell.ca'],
        'telus corporation': ['telus.com'],
        'canadian national railway': ['cn.ca'],
        'canadian pacific kansas city': ['cpr.ca'],
        'air canada': ['aircanada.com'],
        
        # EU Companies
        'deutsche telekom': ['telekom.com'],
        'deutsche bank': ['db.com'],
        'munich re': ['munichre.com'],
        'hermes international': ['hermes.com'],
        'loreal': ['loreal.com'],
        'schneider electric': ['se.com'],
        'bnp paribas': ['bnpparibas.com'],
        'dassault systemes': ['3ds.com'],
        'societe generale': ['societegenerale.com'],
        'bureau veritas': ['bureauveritas.com'],
        'asml holding': ['asml.com'],
        'ahold delhaize': ['aholddelhaize.com'],
        'ing group': ['ing.com'],
        'just eat takeaway': ['justeattakeaway.com'],
        'intesa sanpaolo': ['intesasanpaolo.com'],
        'salvatore ferragamo': ['ferragamo.com'],
        'aena': ['aena.es'],
        'telefonica': ['telefonica.com'],
        'cellnex telecom': ['cellnextelecom.com'],
        'volvo group': ['volvogroup.com'],
        'atlas copco': ['atlascopco.com'],
        'investor ab': ['investorab.com'],
        'nokia corporation': ['nokia.com'],
        'kone corporation': ['kone.com'],
        'sampo group': ['sampo.com'],
        'upm-kymmene': ['upm.com'],
        'novo nordisk': ['novonordisk.com'],
        'danske bank': ['danskebank.com'],
        'roche holding': ['roche.com'],
        'ubs group': ['ubs.com'],
        'zurich insurance group': ['zurich.com'],
        'swiss re': ['swissre.com'],
        'lonza group': ['lonza.com'],
        'holcim': ['holcim.com'],
        'alcon': ['alcon.com'],
        
        # Chinese Companies
        'tencent holdings': ['tencent.com'],
        'didi chuxing': ['didiglobal.com'],
        'zhipu ai': ['zhipuai.cn'],
        'minimax': ['minimax.chat'],
        'baichuan ai': ['baichuan-ai.com'],
        'moonshot': ['moonshot.cn'],
        'stepfun': ['stepfun.com'],
        '01.ai': ['01.ai'],
        'iflytek': ['iflytek.com'],
        'industrial and commercial bank of china': ['icbc.com.cn'],
        'china construction bank': ['ccb.com'],
        'agricultural bank of china': ['abchina.com'],
        'bank of china': ['boc.cn'],
        'state grid corporation of china': ['sgcc.com.cn'],
        'china national petroleum corporation': ['cnpc.com.cn'],
        'china mobile': ['chinamobile.com'],
        'china unicom': ['chinaunicom.com'],
        'contemporary amperex technology': ['catl.com'],
        'geely': ['geely.com'],
        'saic motor': ['saicmotor.com'],
        'great wall motors': ['gwm.com.cn'],
        
        # African Companies
        'bhp billiton': ['bhp.com'],
        'sibanye-stillwater': ['sibanyestillwater.com'],
        'impala platinum': ['implats.co.za'],
        'northam platinum': ['northam.co.za'],
        'kumba iron ore': ['kumba.co.za'],
        'standard bank group': ['standardbank.co.za'],
        'absa group': ['absa.africa'],
        'nedbank group': ['nedbank.co.za'],
        'old mutual': ['oldmutual.com'],
        'mtn group': ['mtn.com'],
        'shoprite holdings': ['shoprite.co.za'],
        'pick n pay': ['picknpay.co.za'],
        'massmart holdings': ['massmart.co.za'],
        'imperial holdings': ['imperiallogistics.com'],
        'guaranty trust holding co': ['gtbank.com'],
        'united bank for africa': ['ubagroup.com'],
        'first bank of nigeria': ['firstbanknigeria.com'],
        'bua cement': ['buacement.com'],
        'bua foods': ['buagroup.com'],
        'seplat energy': ['seplatpetroleum.com'],
        'total nigeria': ['total.com.ng'],
        'airtel africa': ['africa.airtel.com'],
        'nigerian breweries': ['nbplc.com'],
        'nestle nigeria': ['nestle.com.ng'],
        'commercial international bank': ['cibeg.com'],
        'qnb alahli': ['qnbalahli.com'],
        'talaat moustafa group': ['tmg.com.eg'],
        'palm hills development': ['palmhillsdevelopments.com'],
        'eastern company': ['eastern.com.eg'],
        'suez cement': ['suezcement.com.eg'],
        'juhayna food industries': ['juhayna.com'],
        'equity group': ['equitybank.co.ke'],
        'kcb group': ['kcbgroup.com'],
        'im holdings': ['imbank.co.ke'],
        'east african breweries limited': ['eabl.co.ke'],
        'british american tobacco kenya': ['batkenya.com'],
        'bamburi cement': ['bamburi.co.ke'],
        'kenya airways': ['kenya-airways.com'],
        'liberty kenya holdings': ['libertylife.co.ke'],
        'attijariwafa bank': ['attijariwafabank.com'],
        'banque centrale populaire': ['gbp.ma'],
        'bmce bank': ['bmcebank.ma'],
        'managem group': ['managemgroup.com'],
        'ocp group': ['ocpgroup.ma'],
        'addoha group': ['addohagroup.com'],
        'mtn ghana': ['mtn.com.gh'],
        'anglogold ashanti': ['anglogoldashanti.com'],
        'tullow oil': ['tullowoil.com'],
        'gold fields ghana': ['goldfields.com'],
        'fan milk': ['fanmilk.com'],
        'guinness ghana breweries': ['guinness-ghana.com'],
        'opay': ['opayweb.com'],
        'chipper cash': ['chippercash.com'],
        'mnt-halan': ['mnthalan.com'],
        'moniepoint': ['moniepoint.com'],
        'tymebank': ['tymebank.co.za'],
        
        # Middle East Companies
        'al rajhi bank': ['alrajhibank.com.sa'],
        'saudi telecom company': ['stc.com.sa'],
        'dr sulaiman al habib medical': ['drsulaimanalhabib.com'],
        'riyad bank': ['riyadbank.com'],
        'saudi electricity company': ['se.com.sa'],
        'almarai company': ['almarai.com'],
        'saudi basic industries corporation': ['sabic.com'],
        'first abu dhabi bank': ['fab.ae'],
        'emaar properties': ['emaar.com'],
        'emirates airlines': ['emirates.com'],
        'lulu retail': ['luluhypermarket.com'],
        'air arabia': ['airarabiagroup.com'],
        'salik': ['salik.ae'],
        'qatar national bank': ['qnb.com'],
        'industries qatar': ['iq.com.qa'],
        'qatar islamic bank': ['qib.com.qa'],
        'qatar insurance company': ['qic.com.qa'],
        'nakilat': ['nakilat.com.qa'],
        'qatarenergy': ['qatarenergy.qa'],
        'qatar airways': ['qatarairways.com'],
        'kuwait finance house': ['kfh.com'],
        'national bank of kuwait': ['nbk.com'],
        'agility public warehousing': ['agility.com'],
        'kuwait oil company': ['kockw.com'],
        'gulf international bank': ['gibonline.com'],
        'arab banking corporation': ['bank-abc.com'],
        'ahli united bank': ['ahliunited.com'],
        'bank muscat': ['bankmuscat.com'],
        'oq gas networks': ['oq.com'],
        'oq base industries': ['oq.com'],
        'renaissance services': ['rsi.om'],
        'ominvest': ['ominvest.com'],
        'teva pharmaceutical': ['tevapharm.com'],
        'bank hapoalim': ['bankhapoalim.co.il'],
        'bank leumi': ['leumi.co.il'],
        'cyberark software': ['cyberark.com'],
        'wix.com': ['wix.com'],
        'turkish airlines': ['turkishairlines.com'],
        'tupras': ['tupras.com.tr'],
        'koc holding': ['koc.com.tr'],
        'sabanci holding': ['sabanci.com'],
        'garanti bbva': ['garantibbva.com.tr'],
        'olayan group': ['olayan.com'],
        'al-futtaim group': ['alfuttaim.com'],
        'majid al futtaim group': ['majidalfuttaim.com'],
        'oq group': ['oq.com'],
        'almosafer': ['almosafer.com'],
        'foodics': ['foodics.com'],
        'tamara': ['tamara.co'],
        'swvl': ['swvl.com'],
        'trukker': ['trukker.com']
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
    # Parse the global missing companies file
    with open('/Users/adi/code/socratify/socratify-yolo/global_companies_verified_missing.txt', 'r') as f:
        content = f.read()
    
    # Handle both actual newlines and escaped newlines
    content = content.replace('\\n', '\n')
    
    # Extract missing companies by region
    regions_missing = {}
    current_region = None
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('### ') and line.endswith(' ###'):
            current_region = line.replace('### ', '').replace(' ###', '')
            regions_missing[current_region] = []
        elif line and len(line) > 0 and line[0].isdigit() and '. ' in line:
            # Extract company name after the number
            parts = line.split('. ', 1)
            if len(parts) > 1:
                company_name = parts[1]
                if current_region:
                    regions_missing[current_region].append(company_name)
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    # Flatten all companies with region info
    all_companies_with_region = []
    for region, companies in regions_missing.items():
        for company in companies:
            all_companies_with_region.append((company, region))
    
    print(f"Starting download of {len(all_companies_with_region)} global companies...")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("COMPREHENSIVE GLOBAL COVERAGE:")
    print("- UK: FTSE 100/250, unicorns, private companies")
    print("- Canada: TSX 60, Big 6 banks, crown corporations") 
    print("- EU: DAX, CAC, AEX, FTSE MIB, IBEX, Nordic")
    print("- China: Tech giants, SOEs, unicorns")
    print("- Africa: JSE, NSE, major exchanges, unicorns")
    print("- Middle East: GCC, Israel, Turkey\n")
    
    # Track by region
    regional_stats = {}
    for region in regions_missing.keys():
        regional_stats[region] = {'downloaded': 0, 'failed': 0}
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks
        future_to_company = {
            executor.submit(download_logo, company, output_dir, region): (company, region)
            for company, region in all_companies_with_region
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
    
    print(f"\n=== GLOBAL COMPREHENSIVE DOWNLOAD COMPLETE ===")
    print(f"Total companies: {len(all_companies_with_region)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(all_companies_with_region) > 0:
        print(f"Success rate: {(downloaded_count/len(all_companies_with_region)*100):.1f}%")
    
    print(f"\n=== REGIONAL BREAKDOWN ===")
    for region, stats in regional_stats.items():
        total = stats['downloaded'] + stats['failed']
        success_rate = (stats['downloaded'] / total * 100) if total > 0 else 0
        print(f"{region}: {stats['downloaded']}/{total} ({success_rate:.1f}%)")
    
    # Update collection count
    previous_total = 7508  # Count after Indian download
    new_total = previous_total + downloaded_count
    print(f"\nCollection now has approximately: {new_total} logos")
    print(f"Global business ecosystem now comprehensively covered!")
    print(f"Covers: North America, Europe, Asia, Africa, Middle East")

if __name__ == "__main__":
    main()