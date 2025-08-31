#!/usr/bin/env python3
"""
Download final 294 comprehensive Indian companies
Complete coverage: Stock indexes, unicorns, startups, private companies
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
    """Generate possible domain variations for comprehensive Indian companies"""
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
            f"{words[0]}.in", 
            f"{words[0]}.co.in",
            f"{words[0]}.net",
            f"{words[0]}.org"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}{words[1]}.in",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com",
            f"{words[1]}.com"
        ])
    elif len(words) >= 3:
        # First two words
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}{words[1]}.in",
            f"{words[0]}.com"
        ])
        
        # Try acronym (first letters)
        acronym = ''.join(word[0] for word in words if word)
        if len(acronym) >= 2:
            domains.extend([
                f"{acronym}.com",
                f"{acronym}.in",
                f"{acronym}.co.in"
            ])
    
    # Extensive special domain mappings for comprehensive Indian companies
    special_cases = {
        # Major Listed Companies
        'adani enterprises': ['adani.com'],
        'adani ports & sez': ['adaniports.com'],
        'apollo hospitals': ['apollohospitals.com'],
        'asian paints': ['asianpaints.com'],
        'axis bank': ['axisbank.com'],
        'bajaj auto': ['bajajauto.com'],
        'bajaj finance': ['bajajfinserv.in'],
        'bajaj finserv': ['bajajfinserv.in'],
        'bharat electronics': ['bel-india.in'],
        'bharti airtel': ['airtel.in'],
        'cipla': ['cipla.com'],
        'coal india': ['coalindia.in'],
        'dr reddys laboratories': ['drreddys.com'],
        'eicher motors': ['eichermotors.com'],
        'grasim industries': ['grasim.com'],
        'hcltech': ['hcltech.com'],
        'hdfc bank': ['hdfcbank.com'],
        'hdfc life': ['hdfclife.com'],
        'hero motocorp': ['heromotocorp.com'],
        'hindalco industries': ['hindalco.com'],
        'hindustan unilever': ['hul.co.in'],
        'icici bank': ['icicibank.com'],
        'indusind bank': ['indusind.com'],
        'infosys': ['infosys.com'],
        'itc': ['itcportal.com'],
        'jio financial services': ['jio.com'],
        'jsw steel': ['jsw.in'],
        'kotak mahindra bank': ['kotak.com'],
        'larsen & toubro': ['larsentoubro.com'],
        'mahindra & mahindra': ['mahindra.com'],
        'maruti suzuki': ['marutisuzuki.com'],
        'nestle india': ['nestle.in'],
        'ntpc': ['ntpc.co.in'],
        'oil & natural gas corporation': ['ongcindia.com'],
        'power grid corporation': ['powergridindia.com'],
        'reliance industries': ['ril.com'],
        'shriram finance': ['shriramcity.com'],
        'state bank of india': ['sbi.co.in'],
        'sun pharmaceutical': ['sunpharma.com'],
        'tata consultancy services': ['tcs.com'],
        'tata consumer products': ['tataconsumer.com'],
        'tata motors': ['tatamotors.com'],
        'tata steel': ['tatasteel.com'],
        'tech mahindra': ['techmahindra.com'],
        'titan company': ['titan.co.in'],
        'trent': ['trent-tata.com'],
        'ultratech cement': ['ultratechcement.com'],
        'upl': ['upl-ltd.com'],
        'wipro': ['wipro.com'],
        'zomato': ['zomato.com'],
        
        # Banking Complete
        'au small finance bank': ['aubank.in'],
        'federal bank': ['federalbank.co.in'],
        'bandhan bank': ['bandhanbank.com'],
        'bank of baroda': ['bankofbaroda.in'],
        'union bank of india': ['unionbankofindia.co.in'],
        'canara bank': ['canarabank.com'],
        'indian bank': ['indianbank.in'],
        'indian overseas bank': ['iob.in'],
        'bank of india': ['bankofindia.co.in'],
        'bank of maharashtra': ['bankofmaharashtra.in'],
        'uco bank': ['ucobank.com'],
        'central bank of india': ['centralbankofindia.co.in'],
        'punjab & sind bank': ['psbindia.com'],
        'rbl bank': ['rblbank.com'],
        'karnataka bank': ['karnatakabank.com'],
        'south indian bank': ['southindianbank.com'],
        'karur vysya bank': ['kvb.co.in'],
        'city union bank': ['cityunionbank.com'],
        'dhanlaxmi bank': ['dhanbank.com'],
        'nainital bank': ['nainitalbank.co.in'],
        'icici prudential life': ['iciciprulife.com'],
        'max life insurance': ['maxlifeinsurance.com'],
        
        # IT Services
        'l&t infotech': ['lntinfotech.com'],
        'mindtree': ['mindtree.com'],
        'mphasis': ['mphasis.com'],
        'persistent systems': ['persistent.com'],
        'cyient': ['cyient.com'],
        'kpit technologies': ['kpit.com'],
        'hexaware technologies': ['hexaware.com'],
        'zensar technologies': ['zensar.com'],
        'tata elxsi': ['tataelxsi.co.in'],
        'eclerx services': ['eclerx.com'],
        'l&t technology services': ['ltts.com'],
        'coforge': ['coforge.com'],
        'firstsource solutions': ['firstsource.com'],
        'sonata software': ['sonata-software.com'],
        
        # Pharma & Healthcare
        'divis laboratories': ['divis.com'],
        'torrent pharmaceuticals': ['torrentpharma.com'],
        'zydus life sciences': ['zyduslife.com'],
        'alkem laboratories': ['alkem.com'],
        'biocon': ['biocon.com'],
        'cadila healthcare': ['zyduslife.com'],
        'mankind pharma': ['mankindpharma.com'],
        'ipca laboratories': ['ipcalabs.com'],
        'abbott india': ['abbott.co.in'],
        'pfizer india': ['pfizer.co.in'],
        'glaxosmithkline india': ['gsk.in'],
        'sanofi india': ['sanofi.in'],
        'novartis india': ['novartis.in'],
        'apollo hospitals': ['apollohospitals.com'],
        'max healthcare': ['maxhealthcare.in'],
        'fortis healthcare': ['fortishealthcare.com'],
        'narayana hrudayalaya': ['narayanahealth.org'],
        'aster dm healthcare': ['asterdmhealthcare.com'],
        
        # Major Unicorns
        'flipkart': ['flipkart.com'],
        'phonepe': ['phonepe.com'],
        'paytm': ['paytm.com'],
        "byju's": ['byjus.com'],
        'swiggy': ['swiggy.com'],
        'zomato': ['zomato.com'],
        'ola': ['olacabs.com'],
        'oyo rooms': ['oyorooms.com'],
        'freshworks': ['freshworks.com'],
        'dream11': ['dream11.com'],
        'nykaa': ['nykaa.com'],
        'policybazaar': ['policybazaar.com'],
        'makemytrip': ['makemytrip.com'],
        'razorpay': ['razorpay.com'],
        'zerodha': ['zerodha.com'],
        'groww': ['groww.in'],
        'cred': ['cred.club'],
        'meesho': ['meesho.com'],
        'urban company': ['urbancompany.com'],
        'lenskart': ['lenskart.com'],
        'pine labs': ['pinelabs.com'],
        'bharatpe': ['bharatpe.com'],
        'coindcx': ['coindcx.com'],
        'digit insurance': ['godigit.com'],
        'mobikwik': ['mobikwik.com'],
        'slice': ['slice.it'],
        'kreditbee': ['kreditbee.in'],
        'earlysalary': ['earlysalary.com'],
        'capital float': ['capitalfloat.com'],
        'lendingkart': ['lendingkart.com'],
        'unacademy': ['unacademy.com'],
        'eruditus': ['eruditus.com'],
        'upgrad': ['upgrad.com'],
        'vedantu': ['vedantu.com'],
        'bigbasket': ['bigbasket.com'],
        'grofers': ['grofers.com'],
        'delhivery': ['delhivery.com'],
        'blackbuck': ['blackbuck.com'],
        'rivigo': ['rivigo.com'],
        'udaan': ['udaan.com'],
        'ofbusiness': ['ofbusiness.com'],
        'moglix': ['moglix.com'],
        
        # New Unicorns
        'krutrim': ['krutrim.ai'],
        'perfios': ['perfios.com'],
        'rapido': ['rapido.bike'],
        'ather energy': ['atherenergy.com'],
        'moneyview': ['moneyview.in'],
        'porter': ['porter.in'],
        'netradyne': ['netradyne.com'],
        'drools': ['drools.in'],
        
        # Fintech Soonicorns
        'pension box': ['pensionbox.in'],
        'viva money': ['vivamoney.in'],
        'kivi': ['kivi.in'],
        'zaggle': ['zaggle.in'],
        'm2p fintech': ['m2pfintech.com'],
        'niyo': ['goniyo.com'],
        'jar': ['jar.app'],
        'freo': ['freo.in'],
        'fi money': ['fi.money'],
        'jupiter': ['jupiter.money'],
        'navi': ['navi.com'],
        'instantpay': ['instantpay.in'],
        'payme india': ['paymeindia.in'],
        'moneytap': ['moneytap.com'],
        'lazypay': ['lazypay.in'],
        'simpl': ['getsimpl.com'],
        'zestmoney': ['zestmoney.in'],
        'paysense': ['paysense.com'],
        'cashe': ['cashe.co.in'],
        'flexiloans': ['flexiloans.com'],
        
        # E-commerce & Marketplaces
        'the souled store': ['thesouledstore.com'],
        'boat': ['boat-lifestyle.com'],
        'mamaearth': ['mamaearth.in'],
        'sugar cosmetics': ['sugarcosmetics.com'],
        'purplle': ['purplle.com'],
        'bewakoof': ['bewakoof.com'],
        'fabindia': ['fabindia.com'],
        'myntra': ['myntra.com'],
        'snapdeal': ['snapdeal.com'],
        'amazon india': ['amazon.in'],
        'firstcry': ['firstcry.com'],
        'hopscotch': ['hopscotch.in'],
        'limeroad': ['limeroad.com'],
        'jabong': ['jabong.com'],
        'koovs': ['koovs.com'],
        'voonik': ['voonik.com'],
        'stayhalo': ['stayhalo.com'],
        'craftsvilla': ['craftsvilla.com'],
        'shopclues': ['shopclues.com'],
        'paytm mall': ['paytmmall.com'],
        
        # MNC Subsidiaries
        'google india': ['google.co.in'],
        'microsoft india': ['microsoft.com'],
        'amazon india': ['amazon.in'],
        'apple india': ['apple.com'],
        'meta india': ['meta.com'],
        'samsung india': ['samsung.com'],
        'ibm india': ['ibm.com'],
        'oracle india': ['oracle.com'],
        'sap india': ['sap.com'],
        'adobe india': ['adobe.com'],
        'salesforce india': ['salesforce.com'],
        'cisco india': ['cisco.com'],
        'intel india': ['intel.com'],
        'qualcomm india': ['qualcomm.com'],
        'nvidia india': ['nvidia.com'],
        'dell technologies india': ['dell.com'],
        'hp india': ['hp.com'],
        'lenovo india': ['lenovo.com'],
        'sony india': ['sony.co.in'],
        'lg electronics india': ['lg.com'],
        
        # Government PSUs
        'ongc': ['ongcindia.com'],
        'ntpc': ['ntpc.co.in'],
        'coal india': ['coalindia.in'],
        'ioc': ['iocl.com'],
        'bpcl': ['bharatpetroleum.in'],
        'hpcl': ['hindustanpetroleum.com'],
        'sail': ['sail.co.in'],
        'gail': ['gailonline.com'],
        'power grid corporation': ['powergridindia.com'],
        'bhel': ['bhel.com'],
        'bel': ['bel-india.in'],
        'hal': ['hal-india.co.in'],
        'mazagon dock shipbuilders': ['mazagondock.in'],
        'garden reach shipbuilders': ['grse.in'],
        'cochin shipyard': ['cochinshipyard.in'],
        'beml': ['bemlindia.in'],
        'hmt': ['hmtmachinetools.com'],
        'iti limited': ['itiltd-india.com'],
        'mtnl': ['mtnl.in'],
        'bsnl': ['bsnl.co.in'],
        'air india': ['airindia.in'],
        'indian railways': ['indianrailways.gov.in'],
        'food corporation of india': ['fci.gov.in'],
        
        # Cooperatives
        'amul': ['amul.com'],
        'iffco': ['iffco.in'],
        'kribhco': ['kribhco.net'],
        'nafed': ['nafed-india.org'],
        'gujarat cooperative milk marketing federation': ['amul.com'],
        'saraswat cooperative bank': ['saraswatbank.com'],
        'mumbai district central cooperative bank': ['mdccbank.com'],
        'karnataka milk federation': ['kmfnandini.com'],
        'aarey milk': ['aarey.co.in'],
        'verka milk': ['milkfed.punjab.gov.in']
    }
    
    if base in special_cases:
        domains = special_cases[base] + domains
    
    return list(dict.fromkeys(domains))  # Remove duplicates while preserving order

def download_logo(company_name, output_dir):
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
                        return f"✅ {company_name} -> {filename}"
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
                    
                    return f"🔍 {company_name} -> {filename}"
                
            except Exception as e:
                continue
        
        return f"❌ {company_name} - No logo found"

def main():
    # Get the 294 verified missing comprehensive Indian companies
    with open('/Users/adi/code/socratify/socratify-yolo/master_indian_verified_missing.txt', 'r') as f:
        lines = f.readlines()
    
    # Extract company names - all lines starting with "- "
    missing_companies = []
    
    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            # Extract company name after the dash
            company_name = line[2:].strip()
            missing_companies.append(company_name)
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting download of {len(missing_companies)} comprehensive Indian companies...")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("COMPLETE COVERAGE:")
    print("- All NSE/BSE stock market indexes")
    print("- All current Indian unicorns")
    print("- Major soonicorns and high-growth startups") 
    print("- Private companies and family businesses")
    print("- MNC subsidiaries with Indian operations")
    print("- Government PSUs and cooperatives\n")
    
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
    
    print(f"\n=== COMPREHENSIVE INDIAN DOWNLOAD COMPLETE ===")
    print(f"Total companies: {len(missing_companies)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(missing_companies) > 0:
        print(f"Success rate: {(downloaded_count/len(missing_companies)*100):.1f}%")
    
    # Update collection count
    previous_total = 7183  # Count after previous Indian download
    new_total = previous_total + downloaded_count
    print(f"Collection now has approximately: {new_total} logos")
    print(f"Indian business ecosystem now comprehensively covered!")

if __name__ == "__main__":
    main()