#!/usr/bin/env python3
"""
Download critical institutional logos - government, international orgs, infrastructure
"""

import os
import json
import time
import requests
import concurrent.futures
from typing import List, Dict, Tuple
from datetime import datetime
import threading

MAX_WORKERS = 20
RATE_LIMIT_DELAY = 0.03
rate_limiter = threading.Semaphore(MAX_WORKERS)
last_request_time = threading.Lock()
last_time = [0]

def sanitize_filename(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.replace(' ', '_').replace('&', 'and').replace('.', '')
    return name[:100]

def rate_limited_request():
    with last_request_time:
        current_time = time.time()
        time_since_last = current_time - last_time[0]
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        last_time[0] = time.time()

def get_institution_domains(name: str) -> List[str]:
    """Get domain variations for institutions"""
    clean_name = name.lower().replace(' ', '').replace('.', '').replace("'", '')
    
    # Special mappings for known institutions
    special_mappings = {
        'fbi': ['fbi.gov'],
        'cia': ['cia.gov'],
        'nsa': ['nsa.gov'],
        'fda': ['fda.gov'],
        'epa': ['epa.gov'],
        'sec': ['sec.gov'],
        'federal reserve': ['federalreserve.gov', 'fed.gov'],
        'european central bank': ['ecb.europa.eu', 'ecb.int'],
        'world bank': ['worldbank.org'],
        'imf': ['imf.org'],
        'united nations': ['un.org'],
        'who': ['who.int'],
        'unesco': ['unesco.org'],
        'unicef': ['unicef.org'],
        'wto': ['wto.org'],
        'nyse': ['nyse.com'],
        'nasdaq': ['nasdaq.com'],
        'london stock exchange': ['londonstockexchange.com', 'lseg.com'],
        'brookings': ['brookings.edu'],
        'rand': ['rand.org'],
        'heritage foundation': ['heritage.org'],
        'bbc': ['bbc.com', 'bbc.co.uk'],
        'npr': ['npr.org'],
        'pbs': ['pbs.org'],
        'kaiser permanente': ['kaiserpermanente.org', 'kp.org'],
        'mayo clinic': ['mayoclinic.org', 'mayo.edu'],
        'cleveland clinic': ['clevelandclinic.org'],
        'johns hopkins': ['jhu.edu', 'hopkinsmedicine.org'],
        'nhs': ['nhs.uk'],
        'iso': ['iso.org'],
        'ieee': ['ieee.org'],
    }
    
    # Check for special mapping
    for key, domains in special_mappings.items():
        if key in name.lower():
            return domains
    
    # Generate standard variations
    variations = []
    base_name = clean_name.replace('&', 'and')
    
    # Government domains
    if any(word in name.lower() for word in ['agency', 'department', 'federal', 'administration']):
        variations.extend([f"{base_name}.gov", f"{base_name}.gov.uk", f"{base_name}.gc.ca"])
    
    # International organizations
    if any(word in name.lower() for word in ['united nations', 'world', 'international']):
        variations.extend([f"{base_name}.org", f"{base_name}.int"])
    
    # Educational/research
    if any(word in name.lower() for word in ['institute', 'foundation', 'university', 'college']):
        variations.extend([f"{base_name}.edu", f"{base_name}.org"])
    
    # Standard commercial/organizational
    variations.extend([
        f"{base_name}.com",
        f"{base_name}.org",
        f"{base_name}.net",
        f"{base_name}.gov",
        f"{base_name}.edu"
    ])
    
    # Remove duplicates
    seen = set()
    unique = []
    for v in variations:
        if v not in seen:
            seen.add(v)
            unique.append(v)
    
    return unique[:10]

def download_logo(company_info: Tuple[str, str], output_dir: str) -> Dict:
    """Download institutional logo"""
    institution_name, category = company_info
    result = {
        'institution': institution_name,
        'category': category,
        'success': False,
        'error': None,
        'file_path': None,
        'source': None
    }
    
    try:
        domains = get_institution_domains(institution_name)
        
        # Try Clearbit
        for domain in domains:
            try:
                rate_limited_request()
                logo_url = f"https://logo.clearbit.com/{domain}"
                response = requests.get(logo_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                
                if response.status_code == 200 and len(response.content) > 1000:
                    filename = f"{sanitize_filename(institution_name)}.png"
                    file_path = os.path.join(output_dir, category, filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    result['success'] = True
                    result['file_path'] = file_path
                    result['domain'] = domain
                    result['source'] = 'clearbit'
                    return result
            except:
                continue
        
        # Try Google Favicons
        for domain in domains[:3]:
            try:
                rate_limited_request()
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{sanitize_filename(institution_name)}_favicon.png"
                    file_path = os.path.join(output_dir, category, filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    
                    result['success'] = True
                    result['file_path'] = file_path
                    result['domain'] = domain
                    result['source'] = 'google_favicon'
                    return result
            except:
                continue
        
        result['error'] = 'All download attempts failed'
        
    except Exception as e:
        result['error'] = str(e)
    
    return result

def get_critical_institutions() -> Dict[str, List[str]]:
    """Get list of critical missing institutions"""
    return {
        "US Government Agencies": [
            "FBI", "CIA", "NSA", "FDA", "EPA", "SEC", "FCC", "FDIC",
            "Federal Trade Commission", "Department of Justice", "Department of State",
            "Department of Defense", "Department of Treasury", "IRS", "USDA",
            "Department of Energy", "Department of Commerce", "NOAA", "NASA"
        ],
        
        "International Organizations": [
            "United Nations", "World Bank", "International Monetary Fund", "WHO",
            "UNESCO", "UNICEF", "UNHCR", "WTO", "ILO", "OECD",
            "World Economic Forum", "Bank for International Settlements",
            "Asian Development Bank", "African Development Bank", "OPEC"
        ],
        
        "Stock Exchanges": [
            "New York Stock Exchange", "NASDAQ", "London Stock Exchange",
            "Tokyo Stock Exchange", "Shanghai Stock Exchange", "Hong Kong Exchange",
            "Euronext", "Deutsche Börse", "TMX Group", "ASX",
            "BSE India", "NSE India", "Johannesburg Stock Exchange"
        ],
        
        "Central Banks": [
            "Federal Reserve", "European Central Bank", "Bank of Japan",
            "People's Bank of China", "Bank of England", "Bank of Canada",
            "Reserve Bank of Australia", "Reserve Bank of India", "Bundesbank",
            "Banque de France", "Bank of Italy", "Swiss National Bank"
        ],
        
        "Think Tanks": [
            "Brookings Institution", "RAND Corporation", "Heritage Foundation",
            "Council on Foreign Relations", "American Enterprise Institute",
            "Cato Institute", "Urban Institute", "Hoover Institution",
            "Carnegie Endowment", "Atlantic Council", "Chatham House",
            "International Institute for Strategic Studies"
        ],
        
        "Major Cities": [
            "New York City", "London", "Tokyo", "Singapore", "Hong Kong",
            "Shanghai", "Beijing", "Dubai", "Paris", "Frankfurt",
            "San Francisco", "Los Angeles", "Chicago", "Toronto", "Sydney"
        ],
        
        "Healthcare Systems": [
            "Kaiser Permanente", "Mayo Clinic", "Cleveland Clinic", "Johns Hopkins",
            "Mass General", "UCLA Health", "UCSF Health", "NYU Langone",
            "Mount Sinai", "Cedars-Sinai", "NHS", "Charité Berlin"
        ],
        
        "Broadcasting": [
            "BBC", "NPR", "PBS", "CBC", "NHK", "France Télévisions",
            "ARD", "ZDF", "RAI", "RTVE", "VRT", "Al Jazeera",
            "Deutsche Welle", "Voice of America", "RT"
        ],
        
        "Standards Bodies": [
            "ISO", "IEEE", "ANSI", "BSI", "DIN", "AFNOR",
            "UL", "TÜV", "Underwriters Laboratories", "CE Marking",
            "Energy Star", "FCC Certification", "FDA Approval"
        ],
        
        "Major Airports": [
            "Heathrow Airport", "LAX", "JFK Airport", "O'Hare Airport",
            "Dubai International", "Changi Airport", "Hong Kong International",
            "Charles de Gaulle", "Frankfurt Airport", "Amsterdam Schiphol",
            "Tokyo Haneda", "Beijing Capital", "Shanghai Pudong"
        ],
        
        "Major Ports": [
            "Port of Singapore", "Port of Shanghai", "Port of Rotterdam",
            "Port of Los Angeles", "Port of Long Beach", "Port of Hamburg",
            "Port of Antwerp", "Port of Dubai", "Port of Hong Kong",
            "Port of Busan", "Port of Tokyo", "Port of New York"
        ],
        
        "Rating Agencies": [
            "Moody's", "S&P Global", "Fitch Ratings", "DBRS Morningstar",
            "A.M. Best", "JCR", "CRISIL", "China Chengxin"
        ],
        
        "Professional Associations": [
            "American Medical Association", "American Bar Association",
            "AICPA", "CFA Institute", "PMI", "SHRM", "AMA",
            "Institute of Directors", "Chartered Institute", "ACCA"
        ],
        
        "Museums & Cultural": [
            "Smithsonian", "Louvre", "British Museum", "Metropolitan Museum",
            "MoMA", "National Gallery", "Tate Modern", "Guggenheim",
            "Getty Center", "Vatican Museums", "Hermitage", "Prado"
        ]
    }

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/Users/adi/code/socratify/socratify-yolo/logos/institutional_logos_{timestamp}"
    
    institutions = get_critical_institutions()
    
    # Flatten into list
    all_institutions = []
    for category, inst_list in institutions.items():
        for inst in inst_list:
            all_institutions.append((inst, category))
    
    print(f"Downloading critical institutional logos")
    print(f"Output directory: {output_dir}")
    print(f"Total institutions: {len(all_institutions)}")
    print("="*60)
    
    all_results = []
    
    # Process by category
    for category, inst_list in institutions.items():
        print(f"\nProcessing {category}: {len(inst_list)} institutions")
        
        companies = [(inst, category) for inst in inst_list]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(download_logo, company, output_dir) for company in companies]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                all_results.append(result)
        
        successful = sum(1 for r in all_results if r['success'] and r['category'] == category)
        print(f"  Completed: {successful}/{len(inst_list)} successful")
    
    # Generate report
    successful = [r for r in all_results if r['success']]
    failed = [r for r in all_results if not r['success']]
    
    report_path = os.path.join(output_dir, 'institutional_report.json')
    with open(report_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total': len(all_results),
            'successful': len(successful),
            'failed': len(failed),
            'success_rate': f"{(len(successful)/len(all_results)*100):.1f}%",
            'results': all_results
        }, f, indent=2)
    
    if failed:
        failed_path = os.path.join(output_dir, 'failed_institutions.txt')
        with open(failed_path, 'w') as f:
            for item in failed:
                f.write(f"{item['institution']} ({item['category']})\n")
    
    print("\n" + "="*60)
    print("INSTITUTIONAL DOWNLOAD COMPLETE!")
    print(f"Total: {len(all_results)}")
    print(f"Success: {len(successful)} ({(len(successful)/len(all_results)*100):.1f}%)")
    print(f"Failed: {len(failed)}")
    print(f"Report: {report_path}")

if __name__ == "__main__":
    main()