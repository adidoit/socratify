#!/usr/bin/env python3
"""
Download 189 verified missing Indian companies with clean filenames
All tiers from Nifty 50 to startups
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 25
RATE_LIMIT = threading.Semaphore(15)  # Max 15 concurrent requests
RATE_LIMIT_DELAY = 0.05  # 50ms delay between requests

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)  # Keep only alphanumeric, spaces, hyphens
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with single underscore
    filename = re.sub(r'_+', '_', filename)  # Replace multiple underscores with single
    filename = filename.strip('_')  # Remove leading/trailing underscores
    return filename

def generate_domains(company_name):
    """Generate possible domain variations for Indian companies"""
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
    
    if len(words) == 1:
        domains.extend([
            f"{words[0]}.com",
            f"{words[0]}.in", 
            f"{words[0]}.co.in",
            f"{words[0]}.net"
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
    
    # Comprehensive special domain mappings for Indian companies
    special_cases = {
        # Top Tier Nifty 50
        'infosys limited': ['infosys.com'],
        'wipro limited': ['wipro.com'],
        'hcl technologies': ['hcltech.com'],
        'tech mahindra': ['techmahindra.com'],
        'icici bank': ['icicibank.com'],
        'kotak mahindra bank': ['kotak.com'],
        'indusind bank': ['indusind.com'],
        'yes bank': ['yesbank.in'],
        'punjab national bank': ['pnbindia.in'],
        'bank of baroda': ['bankofbaroda.in'],
        'canara bank': ['canarabank.com'],
        'union bank of india': ['unionbankofindia.co.in'],
        'hindustan unilever': ['hul.co.in'],
        'nestle india': ['nestle.in'],
        'britannia industries': ['britannia.co.in'],
        'godrej consumer products': ['godrejcp.com'],
        'emami limited': ['emami.in'],
        'bajaj finance': ['bajajfinserv.in'],
        'bajaj finserv': ['bajajfinserv.in'],
        'bajaj auto': ['bajajauto.com'],
        'maruti suzuki india': ['marutisuzuki.com'],
        'mahindra & mahindra': ['mahindra.com'],
        'tvs motor company': ['tvsmotor.com'],
        'eicher motors': ['eichermotors.com'],
        'jsw steel': ['jsw.in'],
        'vedanta limited': ['vedantalimited.com'],
        'nalco': ['nalcoindia.com'],
        'nmdc': ['nmdc.co.in'],
        'sail': ['sail.co.in'],
        'grasim industries': ['grasim.com'],
        'upl limited': ['upl-ltd.com'],
        'ongc': ['ongcindia.com'],
        'bpcl': ['bharatpetroleum.in'],
        'gail': ['gailonline.com'],
        'ntpc': ['ntpc.co.in'],
        'bhel': ['bhel.com'],
        'bel': ['bel-india.in'],
        'ambuja cement': ['ambujacement.com'],
        'shree cement': ['shreecement.com'],
        "divi's laboratories": ['divis.com'],
        'dr reddy\'s laboratories': ['drreddys.com'],
        'lupin limited': ['lupin.com'],
        'aurobindo pharma': ['aurobindo.com'],
        'biocon limited': ['biocon.com'],
        'cadila healthcare': ['zyduslife.com'],
        'titan company': ['titan.co.in'],
        'page industries': ['pageindustries.com'],
        'avenue supermarts': ['dmart.in'],
        'pidilite industries': ['pidilite.com'],
        
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
        
        # Banking & Finance
        'hdfc life insurance': ['hdfclife.com'],
        'sbi life insurance': ['sbilife.co.in'],
        'lic': ['licindia.in'],
        'icici prudential life': ['iciciprulife.com'],
        'max life insurance': ['maxlifeinsurance.com'],
        'muthoot finance': ['muthootfinance.com'],
        'shriram transport finance': ['shriramtransport.in'],
        'bajaj finance': ['bajajfinserv.in'],
        'l&t finance holdings': ['ltfs.com'],
        'cholamandalam investment': ['cholams.com'],
        
        # Startups & Unicorns
        'flipkart': ['flipkart.com'],
        'paytm': ['paytm.com'],
        "byju's": ['byjus.com'],
        'ola electric': ['olaelectric.com'],
        'zomato': ['zomato.com'],
        'swiggy': ['swiggy.com'],
        'phonepe': ['phonepe.com'],
        'slice': ['slice.it'],
        'jupiter': ['jupiter.money'],
        'fi money': ['fi.money'],
        'navi': ['navi.com'],
        'bharatpe': ['bharatpe.com'],
        'myntra': ['myntra.com'],
        'snapdeal': ['snapdeal.com'],
        'urban company': ['urbancompany.com'],
        'unacademy': ['unacademy.com'],
        'vedantu': ['vedantu.com'],
        'toppr': ['toppr.com'],
        'whitehat jr': ['whitehatjr.com'],
        'practo': ['practo.com'],
        '1mg': ['1mg.com'],
        'docsapp': ['docsapp.in'],
        'portea medical': ['portea.com'],
        'uber india': ['uber.com'],
        'blackbuck': ['blackbuck.com'],
        
        # Fintech
        'pine labs': ['pinelabs.com'],
        'instamojo': ['instamojo.com'],
        'cashfree': ['cashfree.com'],
        'payu india': ['payu.in'],
        'ccavenue': ['ccavenue.com'],
        'mobikwik': ['mobikwik.com'],
        'freecharge': ['freecharge.in'],
        'policybazaar': ['policybazaar.com'],
        'bankbazaar': ['bankbazaar.com'],
        'lendingkart': ['lendingkart.com'],
        
        # FMCG
        'parle products': ['parleproducts.com'],
        "haldiram's": ['haldirams.com'],
        'amul': ['amul.com'],
        'mother dairy': ['motherdairy.com'],
        'patanjali ayurved': ['patanjali.in'],
        'himalaya drug company': ['himalayawellness.in'],
        'colgate-palmolive india': ['colgate.co.in'],
        'procter & gamble india': ['in.pg.com'],
        'reckitt benckiser india': ['reckitt.com'],
        'johnson & johnson india': ['jnj.com'],
        
        # State Owned
        'indian railways': ['indianrailways.gov.in'],
        'food corporation of india': ['fci.gov.in'],
        'hindustan aeronautics limited': ['hal-india.co.in'],
        'mazagon dock shipbuilders': ['mazagondock.in'],
        'garden reach shipbuilders': ['grse.in'],
        'cochin shipyard limited': ['cochinshipyard.in'],
        'rashtriya ispat nigam limited': ['vizagsteel.com'],
        'neyveli lignite corporation': ['nlcindia.com'],
        'oil india limited': ['oil-india.com'],
        'engineers india limited': ['engineersindia.com'],
        
        # Regional Banks
        'karnataka bank': ['karnatakabank.com'],
        'south indian bank': ['southindianbank.com'],
        'karur vysya bank': ['kvb.co.in'],
        'city union bank': ['cityunionbank.com'],
        'federal bank': ['federalbank.co.in'],
        'dhanlaxmi bank': ['dhanbank.com'],
        'nainital bank': ['nainitalbank.co.in'],
        'punjab & sind bank': ['psbindia.com'],
        'indian overseas bank': ['iob.in'],
        'central bank of india': ['centralbankofindia.co.in'],
        
        # Infrastructure
        'gammon india': ['gammonindia.com'],
        'hcc': ['hccindia.com'],
        'punj lloyd': ['punjlloyd.com'],
        'ivrcl infrastructure': ['ivrclinfra.com'],
        'gmr infrastructure': ['gmrgroup.in'],
        'gvk group': ['gvk.com'],
        'irb infrastructure': ['irbinfra.com'],
        'sadbhav engineering': ['sadbhav.co.in'],
        'ncc limited': ['nccltd.in'],
        
        # Automotive
        'force motors': ['forcemotors.com'],
        'hero electric': ['heroelectric.in'],
        'ather energy': ['atherenergy.com'],
        'bosch india': ['bosch.in'],
        'motherson sumi systems': ['mssl.co.in'],
        'bharat forge': ['bharatforge.com'],
        
        # Pharma
        'torrent pharmaceuticals': ['torrentpharma.com'],
        'alkem laboratories': ['alkem.com'],
        'glenmark pharmaceuticals': ['glenmarkpharma.com'],
        'ipca laboratories': ['ipcalabs.com'],
        'mankind pharma': ['mankindpharma.com'],
        'abbott india': ['abbott.co.in'],
        'pfizer india': ['pfizer.co.in'],
        'glaxosmithkline india': ['gsk.in'],
        'sanofi india': ['sanofi.in'],
        'novartis india': ['novartis.in']
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
    # Get the 189 verified missing Indian companies
    with open('/Users/adi/code/socratify/socratify-yolo/indian_verified_missing.txt', 'r') as f:
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
    
    print(f"Starting download of {len(missing_companies)} verified missing Indian companies...")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("Covers: Nifty 50, banks, IT, pharma, FMCG, startups, unicorns, heritage companies\n")
    
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
    
    print(f"\n=== INDIAN COMPANIES DOWNLOAD COMPLETE ===")
    print(f"Total companies: {len(missing_companies)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(missing_companies) > 0:
        print(f"Success rate: {(downloaded_count/len(missing_companies)*100):.1f}%")
    
    # Update collection count
    previous_total = 6998  # Current clean collection count
    new_total = previous_total + downloaded_count
    print(f"Collection now has approximately: {new_total} logos")

if __name__ == "__main__":
    main()