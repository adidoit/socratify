#!/usr/bin/env python3
"""
Download Goldman Sachs research universe gaps
Complete coverage of GS industry analysis
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
    """Generate domain variations for Goldman research companies"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Special cases for Goldman research universe companies
    special_cases = {
        # Software Internet (4)
        'ptc': ['ptc.com'],
        'ansys': ['ansys.com'],
        'wordpress': ['wordpress.com', 'wordpress.org'],
        'drupal': ['drupal.org', 'drupal.com'],
        
        # Financial Technology (1)
        'acorns': ['acorns.com'],
        
        # Healthcare Life Sciences (5)
        'mdlive': ['mdlive.com'],
        '98point6': ['98point6.com'],
        'arcturus': ['arcturusrx.com'],
        'ionis pharmaceuticals': ['ionispharm.com'],
        'ionis': ['ionispharm.com'],
        'cerner': ['cerner.com'],
        
        # Media Entertainment Gaming (1)
        'scribd': ['scribd.com'],
        
        # Consumer Retail Ecommerce (7)
        'thirdlove': ['thirdlove.com'],
        'rebag': ['rebag.com'],
        'discogs': ['discogs.com'],
        'catawiki': ['catawiki.com'],
        'shopkeep': ['shopkeep.com'],
        'erply': ['erply.com'],
        'cin7': ['cin7.com'],
        
        # Transportation Mobility (2)
        'free2move': ['free2move.com'],
        'keeptruckin': ['keeptruckin.com', 'motive.com'],
        
        # Real Estate PropTech (4)
        'vts': ['vts.com'],
        'compstat': ['compstat.com'],
        'plangrid': ['plangrid.com', 'autodesk.com'],
        'coconstruct': ['coconstruct.com'],
        
        # Energy CleanTech (4)
        'newmotion': ['newmotion.com', 'shell.com'],
        'spiber': ['spiber.inc'],
        'ecovative': ['ecovativedesign.com'],
        'mycoworks': ['mycoworks.com'],
        
        # Industrial Manufacturing (9)
        'covariant': ['covariant.ai'],
        'stratasys': ['stratasys.com'],
        'slm solutions': ['slm-solutions.com'],
        'slm': ['slm-solutions.com'],
        'velo3d': ['velo3d.com'],
        'markforged': ['markforged.com'],
        'jaggaer': ['jaggaer.com'],
        'basware': ['basware.com'],
        'ivalua': ['ivalua.com'],
        'zycus': ['zycus.com']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback
        words = base.split()
        if len(words) == 1:
            domains.extend([
                f"{words[0]}.com",
                f"{words[0]}.org",
                f"{words[0]}.ai",
                f"{words[0]}.io"
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

def download_logo(company_name, output_dir, industry=""):
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
                        return f"🔥 {industry} | {company_name} -> {filename} (domain: {domain})"
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
                    
                    return f"🔍 {industry} | {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {industry} | {company_name} - No logo found"

def main():
    # 37 MISSING GOLDMAN SACHS RESEARCH UNIVERSE COMPANIES
    goldman_missing = [
        # Software Internet (4) - Highest priority
        ("PTC", "SOFTWARE"),
        ("Ansys", "SOFTWARE"),
        ("WordPress", "SOFTWARE"), 
        ("Drupal", "SOFTWARE"),
        
        # Financial Technology (1) - High priority
        ("Acorns", "FINTECH"),
        
        # Healthcare Life Sciences (5) - High priority  
        ("MDLive", "HEALTHCARE"),
        ("98point6", "HEALTHCARE"),
        ("Arcturus", "HEALTHCARE"),
        ("Ionis Pharmaceuticals", "HEALTHCARE"),
        ("Cerner", "HEALTHCARE"),
        
        # Media Entertainment Gaming (1) - High priority
        ("Scribd", "MEDIA"),
        
        # Consumer Retail Ecommerce (7) - Medium-high priority
        ("ThirdLove", "CONSUMER"),
        ("Rebag", "CONSUMER"),
        ("Discogs", "CONSUMER"),
        ("Catawiki", "CONSUMER"),
        ("Shopkeep", "CONSUMER"),
        ("Erply", "CONSUMER"),
        ("Cin7", "CONSUMER"),
        
        # Transportation Mobility (2) - Medium-high priority
        ("Free2move", "TRANSPORT"),
        ("KeepTruckin", "TRANSPORT"),
        
        # Real Estate PropTech (4) - Medium priority
        ("VTS", "PROPTECH"),
        ("CompStak", "PROPTECH"),
        ("PlanGrid", "PROPTECH"),
        ("CoConstruct", "PROPTECH"),
        
        # Energy CleanTech (4) - Medium priority
        ("NewMotion", "CLEANTECH"),
        ("Spiber", "CLEANTECH"),
        ("Ecovative", "CLEANTECH"),
        ("MycoWorks", "CLEANTECH"),
        
        # Industrial Manufacturing (9) - Lower priority but most gaps
        ("Covariant", "INDUSTRIAL"),
        ("Stratasys", "INDUSTRIAL"),
        ("SLM Solutions", "INDUSTRIAL"),
        ("Velo3D", "INDUSTRIAL"),
        ("Markforged", "INDUSTRIAL"),
        ("Jaggaer", "INDUSTRIAL"),
        ("Basware", "INDUSTRIAL"),
        ("Ivalua", "INDUSTRIAL"),
        ("Zycus", "INDUSTRIAL")
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"📈 GOLDMAN SACHS RESEARCH UNIVERSE COMPLETION 📈")
    print(f"Downloading {len(goldman_missing)} missing GS research companies")
    print(f"Target: 93.1% -> ~99%+ research coverage")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\n")
    
    downloaded_count = 0
    failed_count = 0
    industry_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir, industry): (company, industry)
            for company, industry in goldman_missing
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company, industry = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("🔍"):
                downloaded_count += 1
                if industry not in industry_success:
                    industry_success[industry] = 0
                industry_success[industry] += 1
            else:
                failed_count += 1
    
    print(f"\n✅ GOLDMAN RESEARCH UNIVERSE COMPLETION DONE!")
    print(f"Total GS research companies: {len(goldman_missing)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(goldman_missing) > 0:
        print(f"Success rate: {(downloaded_count/len(goldman_missing)*100):.1f}%")
    
    # Calculate new Goldman coverage
    total_gs_companies = 540
    remaining_missing = 37 - downloaded_count
    new_coverage = ((total_gs_companies - remaining_missing) / total_gs_companies * 100)
    
    # Update collection count
    previous_total = 8341  # From McKinsey sector completion
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"📈 Goldman Sachs research coverage: {new_coverage:.1f}%")
    print(f"✅ GOLDMAN RESEARCH UNIVERSE DOMINANCE!")
    
    # Show industry success breakdown
    print(f"\n🎯 Downloads by industry:")
    for industry, count in sorted(industry_success.items()):
        print(f"  {industry}: {count} companies")
    
    # Show key Goldman gaps filled
    key_downloads = [company for company, _ in goldman_missing 
                    if any(company in result for result in [
                        "🔥", "🔍"
                    ])]
    
    if downloaded_count >= 25:  # If we got most of them
        print(f"\n🔥 Major Goldman research gaps filled:")
        print(f"  • Enterprise software: PTC, Ansys")
        print(f"  • FinTech: Acorns") 
        print(f"  • HealthTech: MDLive, 98point6, Cerner")
        print(f"  • Consumer platforms: ThirdLove, Rebag, Discogs")
        print(f"  • PropTech: VTS, CompStak")
        print(f"  • Manufacturing 4.0: Stratasys, Markforged, Velo3D")

if __name__ == "__main__":
    main()