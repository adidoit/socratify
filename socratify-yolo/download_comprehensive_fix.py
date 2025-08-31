#!/usr/bin/env python3
"""
Comprehensive logo download script with enhanced strategies for failed downloads.
This script addresses the patterns identified in the failure analysis:
1. Special character handling (& becomes "and", removing special chars)
2. Domain-based searches for educational institutions
3. Multiple API fallbacks with better error handling
4. Company name variations and abbreviations
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Dict, List, Tuple, Optional

# Create output directory
OUTPUT_DIR = 'logos/comprehensive_fix'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Enhanced name cleaning strategies
def clean_company_name(name: str) -> List[str]:
    """Generate multiple variations of company names for better matching."""
    variations = []
    
    # Original name
    variations.append(name)
    
    # Replace & with and
    if '&' in name:
        variations.append(name.replace('&', 'and'))
        variations.append(name.replace(' & ', ''))  # Remove & entirely
        variations.append(name.replace(' & ', '-'))  # Replace with dash
    
    # Handle common suffixes
    suffixes = [' Inc.', ' Inc', ' LLC', ' Ltd', ' Limited', ' Corporation', ' Corp', ' Company', ' Co.', ' Co',
                ' Group', ' Holdings', ' Partners', ' Capital', ' Ventures', ' Associates', ' Technologies',
                ' Financial', ' Services', ' Bank', ' Insurance', ' Global', ' International', ' USA',
                ' plc', ' PLC', ' AG', ' GmbH', ' SA', ' SpA', ' NV', ' BV']
    
    clean_name = name
    for suffix in suffixes:
        if name.endswith(suffix):
            clean_name = name[:-len(suffix)].strip()
            variations.append(clean_name)
            break
    
    # Handle parentheses
    if '(' in name:
        base_name = name.split('(')[0].strip()
        variations.append(base_name)
    
    # Common abbreviations
    abbreviations = {
        'Goldman Sachs & Company': ['goldmansachs', 'gs'],
        'Ernst & Young': ['ey', 'ernstandyoung'],
        'Alvarez & Marsal': ['alvarezmarsal', 'am'],
        'PwC Strategy&': ['pwc', 'strategyand', 'strategy'],
        'Eli Lilly & Company': ['lilly', 'elililly'],
        'H&M': ['hm', 'handm', 'hennes'],
        'Larsen & Toubro': ['larsentoubro', 'lt', 'lnt'],
        'Mahindra & Mahindra': ['mahindra', 'mm'],
        'Marks & Spencer': ['marksandspencer', 'ms', 'mands'],
        'Pratt & Whitney': ['prattwhitney', 'pw'],
        'Legal & General': ['legalandgeneral', 'lg'],
        'Moelis & Company': ['moelis'],
        'Hellman & Friedman': ['hellmanfriedman', 'hf'],
        'Take-Two Interactive': ['taketwo', 't2', 'ttwo'],
        'Toronto-Dominion Bank': ['td', 'tdbank', 'torontodominion']
    }
    
    for full_name, abbrevs in abbreviations.items():
        if full_name.lower() in name.lower():
            variations.extend(abbrevs)
    
    # Handle hyphenated names
    if '-' in name:
        variations.append(name.replace('-', ''))
        variations.append(name.replace('-', '_'))
    
    # Remove spaces
    variations.append(name.replace(' ', ''))
    variations.append(name.replace(' ', '-'))
    variations.append(name.replace(' ', '_'))
    
    # Lowercase versions
    variations.extend([v.lower() for v in variations])
    
    # Remove duplicates while preserving order
    seen = set()
    unique_variations = []
    for v in variations:
        if v and v not in seen:
            seen.add(v)
            unique_variations.append(v)
    
    return unique_variations

def get_business_school_domains() -> Dict[str, str]:
    """Return known domains for business schools."""
    return {
        # US Business Schools
        "Boston College Carroll School of Management": "bc.edu",
        "Michigan State Broad College of Business": "broad.msu.edu",
        "Maryland Smith School of Business": "smith.umd.edu",
        "Rochester Simon Business School": "simon.rochester.edu",
        "SMU Cox School of Business": "cox.smu.edu",
        "UC Davis Graduate School of Management": "gsm.ucdavis.edu",
        "Colorado Leeds School of Business": "leeds.colorado.edu",
        "Connecticut School of Business": "business.uconn.edu",
        "Fordham Gabelli School of Business": "gabelli.fordham.edu",
        "George Washington School of Business": "business.gwu.edu",
        "Miami Business School": "bus.miami.edu",
        "Missouri Trulaske College of Business": "business.missouri.edu",
        "Northeastern D'Amore-McKim School of Business": "damore-mckim.northeastern.edu",
        "Rutgers Business School": "business.rutgers.edu",
        "Temple Fox School of Business": "fox.temple.edu",
        "Tennessee Haslam College of Business": "haslam.utk.edu",
        "Texas A&M Mays Business School": "mays.tamu.edu",
        "Tulane Freeman School of Business": "freeman.tulane.edu",
        "Arkansas Walton College of Business": "walton.uark.edu",
        "Auburn Harbert College of Business": "harbert.auburn.edu",
        "Baylor Hankamer School of Business": "baylor.edu/business",
        "Case Western Weatherhead School of Management": "weatherhead.case.edu",
        "Cincinnati Lindner College of Business": "business.uc.edu",
        "American Kogod School of Business": "kogod.american.edu",
        
        # Canadian Business Schools
        "Ivey Business School - Western University": "ivey.uwo.ca",
        "Smith School of Business - Queen's University": "smith.queensu.ca",
        "Schulich School of Business - York University": "schulich.yorku.ca",
        "DeGroote School of Business - McMaster University": "degroote.mcmaster.ca",
        "HEC Montreal": "hec.ca",
        "Beedie School of Business - Simon Fraser University": "beedie.sfu.ca",
        
        # Indian Business Schools
        "IIM Ahmedabad": "iima.ac.in",
        "IIM Bangalore": "iimb.ac.in",
        "IIM Calcutta": "iimcal.ac.in",
        "IIM Lucknow": "iiml.ac.in",
        "IIM Kozhikode": "iimk.ac.in",
        "IIM Indore": "iimidr.ac.in",
        "ISB Hyderabad": "isb.edu",
        "FMS Delhi": "fms.edu",
        "XLRI Jamshedpur": "xlri.ac.in",
        "JBIMS Mumbai": "jbims.edu",
        
        # European Business Schools
        "INSEAD": "insead.edu",
        "London Business School": "london.edu",
        "HEC Paris": "hec.edu",
        "IESE Business School": "iese.edu",
        "IMD Business School": "imd.org",
        "IE Business School": "ie.edu",
        "SDA Bocconi School of Management": "unibocconi.it",
        "Cambridge Judge Business School": "jbs.cam.ac.uk",
        "Oxford Said Business School": "sbs.ox.ac.uk",
        "ESSEC Business School": "essec.edu",
        "ESCP Business School": "escp.eu"
    }

def download_logo_with_retries(name: str, variations: List[str], is_school: bool = False) -> Optional[Dict]:
    """Try multiple APIs and name variations to download a logo."""
    
    # If it's a school, check if we have a known domain
    school_domains = get_business_school_domains()
    if is_school and name in school_domains:
        domain = school_domains[name]
        # Add domain-based variations
        variations.insert(0, domain)
        if '.' in domain:
            variations.insert(1, domain.split('.')[0])
    
    # API endpoints with different strategies
    api_strategies = [
        {
            'name': 'Clearbit_Domain',
            'url_template': 'https://logo.clearbit.com/{query}',
            'needs_domain': True
        },
        {
            'name': 'Logo.dev_Domain',
            'url_template': 'https://img.logo.dev/{query}?token=pk_X-1ZO13GSgeOoUrIuCGGfw',
            'needs_domain': True
        },
        {
            'name': 'Brandfetch',
            'url_template': 'https://cdn.brandfetch.io/{query}/w/512/h/512',
            'needs_domain': True
        },
        {
            'name': 'Company_Logos',
            'url_template': 'https://logo.uplead.com/{query}',
            'needs_domain': True
        }
    ]
    
    # Try each variation with each API
    for variation in variations[:10]:  # Limit to first 10 variations
        for api in api_strategies:
            try:
                # Prepare the query
                if api['needs_domain'] and not ('.' in variation):
                    # Try common TLDs
                    for tld in ['.com', '.org', '.net', '.edu', '.co', '.io']:
                        domain_query = f"{variation}{tld}"
                        url = api['url_template'].format(query=urllib.parse.quote(domain_query))
                        
                        response = requests.get(url, timeout=5, headers={
                            'User-Agent': 'Mozilla/5.0 (compatible; LogoDownloader/1.0)'
                        })
                        
                        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                            # Save the logo
                            ext = 'png'
                            if 'svg' in response.headers.get('content-type', ''):
                                ext = 'svg'
                            elif 'jpeg' in response.headers.get('content-type', '') or 'jpg' in response.headers.get('content-type', ''):
                                ext = 'jpg'
                            
                            filename = f"{name.replace('/', '_').replace(' ', '_')}_{api['name']}.{ext}"
                            filepath = os.path.join(OUTPUT_DIR, filename)
                            
                            with open(filepath, 'wb') as f:
                                f.write(response.content)
                            
                            return {
                                'name': name,
                                'status': 'success',
                                'method': f"{api['name']}_{domain_query}",
                                'filename': filename,
                                'size': len(response.content)
                            }
                else:
                    # Direct query
                    url = api['url_template'].format(query=urllib.parse.quote(variation))
                    
                    response = requests.get(url, timeout=5, headers={
                        'User-Agent': 'Mozilla/5.0 (compatible; LogoDownloader/1.0)'
                    })
                    
                    if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                        # Save the logo
                        ext = 'png'
                        if 'svg' in response.headers.get('content-type', ''):
                            ext = 'svg'
                        elif 'jpeg' in response.headers.get('content-type', '') or 'jpg' in response.headers.get('content-type', ''):
                            ext = 'jpg'
                        
                        filename = f"{name.replace('/', '_').replace(' ', '_')}_{api['name']}.{ext}"
                        filepath = os.path.join(OUTPUT_DIR, filename)
                        
                        with open(filepath, 'wb') as f:
                            f.write(response.content)
                        
                        return {
                            'name': name,
                            'status': 'success',
                            'method': f"{api['name']}_{variation}",
                            'filename': filename,
                            'size': len(response.content)
                        }
                        
            except Exception as e:
                continue
    
    return {
        'name': name,
        'status': 'failed',
        'error': 'All download attempts failed'
    }

def main():
    # Load fixable failures
    fixable_failures = []
    with open('logos/fixable_failures.txt', 'r') as f:
        fixable_failures = [line.strip() for line in f if line.strip()]
    
    # Load missing business schools
    missing_schools = []
    if os.path.exists('logos/truly_missing_business_schools.txt'):
        with open('logos/truly_missing_business_schools.txt', 'r') as f:
            missing_schools = [line.strip() for line in f if line.strip()]
    
    # Combine all targets
    all_targets = []
    
    # Add fixable failures
    for name in fixable_failures:
        all_targets.append((name, False))  # Not a school
    
    # Add missing schools
    for name in missing_schools:
        all_targets.append((name, True))  # Is a school
    
    print(f"Total targets to download: {len(all_targets)}")
    print(f"- Fixable failures: {len(fixable_failures)}")
    print(f"- Missing schools: {len(missing_schools)}")
    
    # Download logos with progress tracking
    results = []
    successful = 0
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        
        for name, is_school in all_targets:
            variations = clean_company_name(name)
            future = executor.submit(download_logo_with_retries, name, variations, is_school)
            futures[future] = name
        
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            results.append(result)
            
            if result['status'] == 'success':
                successful += 1
                print(f"[{i+1}/{len(all_targets)}] ✓ {result['name']} - {result['method']}")
            else:
                print(f"[{i+1}/{len(all_targets)}] ✗ {result['name']}")
            
            # Rate limiting
            if i % 50 == 0:
                time.sleep(1)
    
    # Save results
    with open('logos/comprehensive_fix_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n=== DOWNLOAD COMPLETE ===")
    print(f"Total attempts: {len(all_targets)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(all_targets) - successful}")
    print(f"Success rate: {successful/len(all_targets)*100:.1f}%")
    print(f"\nLogos saved to: {OUTPUT_DIR}")
    print(f"Results saved to: logos/comprehensive_fix_results.json")
    
    # Analyze remaining failures
    still_failed = [r for r in results if r['status'] == 'failed']
    if still_failed:
        print(f"\n=== STILL FAILED ({len(still_failed)}) ===")
        for r in still_failed[:20]:
            print(f"  • {r['name']}")
        if len(still_failed) > 20:
            print(f"  ... and {len(still_failed) - 20} more")

if __name__ == "__main__":
    main()