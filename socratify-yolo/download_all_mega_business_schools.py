#!/usr/bin/env python3
"""
Download ALL 47 missing mega business schools
GLOBAL EDUCATION DOMINATION!
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 60
RATE_LIMIT = threading.Semaphore(50)
RATE_LIMIT_DELAY = 0.01

def clean_filename(school_name):
    """Convert school name to clean filename"""
    filename = school_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(school_name):
    """Generate domain variations for mega business schools"""
    base = school_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # MEGA special cases for missing business schools
    special_cases = {
        # US Regional Universities (6)
        'new england college business': ['nec.edu'],
        'ithaca college business': ['ithaca.edu'],
        'marist college business': ['marist.edu'],
        'rhode island college business': ['ric.edu'],
        'college of charleston business': ['cofc.edu'],
        'middlebury college business': ['middlebury.edu'],
        
        # US Community Colleges (15)
        'richland college business': ['richlandcollege.edu'],
        'angelina college business': ['angelina.edu'],
        'el camino college business': ['elcamino.edu'],
        'cerritos college business': ['cerritos.edu'],
        'compton college business': ['compton.edu'],
        'cypress college business': ['cypresscollege.edu'],
        'santiago canyon college business': ['sccollege.edu'],
        'norco college business': ['norcocollege.edu'],
        'rio hondo college business': ['riohondo.edu'],
        'citrus college business': ['citruscollege.edu'],
        'st petersburg college business': ['spcollege.edu'],
        'malcolm x college business': ['ccc.edu'],
        'wilbur wright college business': ['ccc.edu'],
        'lackawanna college business': ['lackawanna.edu'],
        'gaston college business': ['gaston.edu'],
        
        # International Business Schools (26)
        'warwick business school': ['wbs.ac.uk', 'warwick.ac.uk'],
        'whu otto beisheim school': ['whu.edu'],
        'gisma business school': ['gisma.com'],
        'hec paris': ['hec.edu', 'hec.fr'],
        'edhec business school': ['edhec.edu'],
        'montpellier business school': ['montpellier-bs.com'],
        'iese business school': ['iese.edu'],
        'ie business school': ['ie.edu'],
        'esade business school': ['esade.edu'],
        'tilburg school of economics': ['tilburguniversity.edu'],
        'hec lausanne': ['unil.ch'],
        'salzburg business school': ['fh-salzburg.ac.at'],
        'vlerick business school': ['vlerick.com'],
        'copenhagen business school': ['cbs.dk'],
        'aarhus school of business': ['au.dk'],
        'gothenburg school of business': ['gu.se'],
        'oslo business school': ['oslomet.no'],
        'melbourne business school': ['mbs.edu', 'unimelb.edu.au'],
        'waseda business school': ['waseda.jp'],
        'keio business school': ['keio.ac.jp'],
        'sogang business school': ['sogang.ac.kr'],
        'nanyang business school': ['ntu.edu.sg'],
        'instituto de empresa madrid': ['ie.edu'],
        'incae business school': ['incae.edu'],
        'lagos business school': ['lbs.edu.ng'],
        'strathmore business school': ['strathmore.edu']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Smart pattern matching for business schools
        words = base.split()
        
        # Remove common words
        filtered_words = [word for word in words if word not in ['school', 'business', 'college', 'university', 'of', 'the', 'and', 'for', 'graduate', 'management']]
        
        if filtered_words:
            first_word = filtered_words[0]
            domains.extend([
                f"{first_word}.edu",
                f"{first_word}.ac.uk",
                f"{first_word}.com",
                f"{first_word}.fr",
                f"{first_word}.de",
                f"{first_word}.dk",
                f"{first_word}.se",
                f"{first_word}.no",
                f"{first_word}.jp",
                f"{first_word}.sg",
                f"{first_word}.edu.au"
            ])
            
            if len(filtered_words) >= 2:
                second_word = filtered_words[1]
                domains.extend([
                    f"{second_word}.{first_word}.edu",
                    f"{first_word}.{second_word}.edu",
                    f"{first_word}{second_word}.edu"
                ])
        else:
            # Fallback
            domains.extend([
                f"{words[0]}.edu",
                f"{words[0]}.com"
            ])
    
    return list(dict.fromkeys(domains))

def download_logo(school_name, output_dir, category=""):
    """Download logo with comprehensive domain trying"""
    
    with RATE_LIMIT:
        time.sleep(RATE_LIMIT_DELAY)
        
        domains = generate_domains(school_name)
        
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
                    
                    filename = f"{clean_filename(school_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.getsize(filepath) > 500:
                        return f"🎓 {category} | {school_name} -> {filename} (domain: {domain})"
                    else:
                        os.remove(filepath)
                
                # Try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(school_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"📚 {category} | {school_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {category} | {school_name} - No logo found"

def get_all_47_missing_mega_schools():
    """All 47 missing schools from mega database analysis"""
    return [
        # US Regional Universities (6) - Highest Priority
        ("New England College Business", "US_REGIONAL"),
        ("Ithaca College Business", "US_REGIONAL"),
        ("Marist College Business", "US_REGIONAL"),
        ("Rhode Island College Business", "US_REGIONAL"),
        ("College of Charleston Business", "US_REGIONAL"),
        ("Middlebury College Business", "US_REGIONAL"),
        
        # US Community Colleges (15) - High Priority
        ("Richland College Business", "US_COMMUNITY"),
        ("Angelina College Business", "US_COMMUNITY"),
        ("El Camino College Business", "US_COMMUNITY"),
        ("Cerritos College Business", "US_COMMUNITY"),
        ("Compton College Business", "US_COMMUNITY"),
        ("Cypress College Business", "US_COMMUNITY"),
        ("Santiago Canyon College Business", "US_COMMUNITY"),
        ("Norco College Business", "US_COMMUNITY"),
        ("Rio Hondo College Business", "US_COMMUNITY"),
        ("Citrus College Business", "US_COMMUNITY"),
        ("St. Petersburg College Business", "US_COMMUNITY"),
        ("Malcolm X College Business", "US_COMMUNITY"),
        ("Wilbur Wright College Business", "US_COMMUNITY"),
        ("Lackawanna College Business", "US_COMMUNITY"),
        ("Gaston College Business", "US_COMMUNITY"),
        
        # International Business Schools (26) - Elite Programs
        ("Warwick Business School", "EUROPE_ELITE"),
        ("WHU Otto Beisheim School", "EUROPE_ELITE"),
        ("GISMA Business School", "EUROPE_ELITE"),
        ("HEC Paris", "EUROPE_ELITE"),
        ("EDHEC Business School", "EUROPE_ELITE"),
        ("Montpellier Business School", "EUROPE_ELITE"),
        ("IESE Business School", "EUROPE_ELITE"),
        ("IE Business School", "EUROPE_ELITE"),
        ("ESADE Business School", "EUROPE_ELITE"),
        ("Tilburg School of Economics", "EUROPE_ELITE"),
        ("HEC Lausanne", "EUROPE_ELITE"),
        ("Salzburg Business School", "EUROPE_ELITE"),
        ("Vlerick Business School", "EUROPE_ELITE"),
        ("Copenhagen Business School", "EUROPE_ELITE"),
        ("Aarhus School of Business", "EUROPE_ELITE"),
        ("Gothenburg School of Business", "EUROPE_ELITE"),
        ("Oslo Business School", "EUROPE_ELITE"),
        ("Melbourne Business School", "ASIA_PAC"),
        ("Waseda Business School", "ASIA_PAC"),
        ("Keio Business School", "ASIA_PAC"),
        ("Sogang Business School", "ASIA_PAC"),
        ("Nanyang Business School", "ASIA_PAC"),
        ("Instituto de Empresa Madrid", "EUROPE_ELITE"),
        ("INCAE Business School", "AMERICAS"),
        ("Lagos Business School", "AFRICA"),
        ("Strathmore Business School", "AFRICA")
    ]

def main():
    # Get all 47 missing mega schools
    schools_to_download = get_all_47_missing_mega_schools()
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🚀🌍 MEGA BUSINESS SCHOOLS DOWNLOAD - GLOBAL DOMINATION! 🌍🚀")
    print(f"Downloading ALL {len(schools_to_download)} missing mega business schools")
    print(f"Coverage: 94.2% -> Target: 100% complete coverage")
    print(f"Categories: US Regional (6) + US Community (15) + International Elite (26)")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print(f"💥 TOTAL EDUCATION DOMINATION! 💥\n")
    
    downloaded_count = 0
    failed_count = 0
    category_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_school = {
            executor.submit(download_logo, school, output_dir, category): (school, category)
            for school, category in schools_to_download
        }
        
        for future in as_completed(future_to_school):
            result = future.result()
            school, category = future_to_school[future]
            print(result)
            
            if result.startswith("🎓") or result.startswith("📚"):
                downloaded_count += 1
                if category not in category_success:
                    category_success[category] = 0
                category_success[category] += 1
            else:
                failed_count += 1
    
    print(f"\n✅ MEGA BUSINESS SCHOOLS DOWNLOAD COMPLETE!")
    print(f"Total schools attempted: {len(schools_to_download)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(schools_to_download) > 0:
        print(f"Success rate: {(downloaded_count/len(schools_to_download)*100):.1f}%")
    
    # Calculate new mega coverage
    total_mega_schools = 804  # From analysis
    remaining_missing = 47 - downloaded_count
    new_coverage = ((total_mega_schools - remaining_missing) / total_mega_schools * 100)
    
    # Update collection count
    previous_total = 8594  # From business schools completion
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} business logos")
    print(f"🌍 MEGA business schools coverage: {new_coverage:.1f}%")
    
    # Show category success breakdown
    print(f"\n🎯 Downloads by category:")
    for category, count in sorted(category_success.items()):
        print(f"  {category}: {count} schools")
    
    # Major achievements
    if downloaded_count >= 40:  # If we got most of them
        print(f"\n🔥 MEGA BUSINESS SCHOOL EMPIRE ACHIEVED:")
        print(f"  • US Regional Universities: Elite liberal arts business programs")
        print(f"  • US Community Colleges: Complete local business education")
        print(f"  • European Elite: HEC Paris, IESE, IE, ESADE, Warwick")
        print(f"  • Asia-Pacific: Waseda, Keio, Nanyang, Melbourne")
        print(f"  • Global Coverage: Africa, Americas, Nordic countries")
        
    print(f"\n🌟 GLOBAL BUSINESS EDUCATION DOMINATION COMPLETE!")
    print(f"📚 From Ivy League to community colleges, Europe to Asia!")
    print(f"🚀 WORLD'S MOST COMPLETE BUSINESS SCHOOL LOGO COLLECTION!")

if __name__ == "__main__":
    main()