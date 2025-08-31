import os
import time
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import re

# Create directory for business school logos
os.makedirs('logos/business_school_logos', exist_ok=True)

# Read the list of missing business schools
with open('logos/missing_business_schools.txt', 'r') as f:
    business_schools = [line.strip() for line in f if line.strip()]

# Function to clean school name for better logo search
def clean_school_name(name):
    # Extract key identifiers
    name_lower = name.lower()
    
    # Special mappings for business schools
    if 'wharton' in name_lower:
        return 'wharton'
    elif 'mit sloan' in name_lower:
        return 'mit'
    elif 'chicago booth' in name_lower:
        return 'chicagobooth'
    elif 'yale' in name_lower and 'management' in name_lower:
        return 'som.yale'
    elif 'berkeley' in name_lower and 'haas' in name_lower:
        return 'haas.berkeley'
    elif 'dartmouth' in name_lower and 'tuck' in name_lower:
        return 'tuck.dartmouth'
    elif 'carnegie mellon' in name_lower and 'tepper' in name_lower:
        return 'tepper.cmu'
    elif 'unc' in name_lower and 'kenan' in name_lower:
        return 'kenan-flagler.unc'
    elif 'ut austin' in name_lower and 'mccombs' in name_lower:
        return 'mccombs.utexas'
    elif 'usc' in name_lower and 'marshall' in name_lower:
        return 'marshall.usc'
    elif 'indiana' in name_lower and 'kelley' in name_lower:
        return 'kelley.indiana'
    elif 'uva' in name_lower and 'darden' in name_lower:
        return 'darden.virginia'
    elif 'emory' in name_lower and 'goizueta' in name_lower:
        return 'goizueta.emory'
    elif 'rice' in name_lower and 'jones' in name_lower:
        return 'business.rice'
    elif 'notre dame' in name_lower and 'mendoza' in name_lower:
        return 'mendoza.nd'
    elif 'washington university' in name_lower and 'olin' in name_lower:
        return 'olin.wustl'
    elif 'georgia tech' in name_lower and 'scheller' in name_lower:
        return 'scheller.gatech'
    elif 'vanderbilt' in name_lower and 'owen' in name_lower:
        return 'owen.vanderbilt'
    elif 'ohio state' in name_lower and 'fisher' in name_lower:
        return 'fisher.osu'
    elif 'penn state' in name_lower and 'smeal' in name_lower:
        return 'smeal.psu'
    
    # Canadian schools
    elif 'rotman' in name_lower:
        return 'rotman.utoronto'
    elif 'ivey' in name_lower:
        return 'ivey.uwo'
    elif 'desautels' in name_lower:
        return 'mcgill'
    elif 'sauder' in name_lower:
        return 'sauder.ubc'
    elif 'smith' in name_lower and 'queen' in name_lower:
        return 'smith.queensu'
    elif 'schulich' in name_lower:
        return 'schulich.yorku'
    elif 'degroote' in name_lower:
        return 'degroote.mcmaster'
    elif 'hec montreal' in name_lower:
        return 'hec'
    
    # Indian schools
    elif 'iim ahmedabad' in name_lower:
        return 'iima'
    elif 'iim bangalore' in name_lower:
        return 'iimb'
    elif 'iim calcutta' in name_lower:
        return 'iimc'
    elif 'iim lucknow' in name_lower:
        return 'iiml'
    elif 'iim kozhikode' in name_lower:
        return 'iimk'
    elif 'iim indore' in name_lower:
        return 'iimi'
    elif 'isb hyderabad' in name_lower:
        return 'isb'
    elif 'xlri' in name_lower:
        return 'xlri'
    elif 'fms delhi' in name_lower:
        return 'fms'
    elif 'mdi' in name_lower:
        return 'mdi'
    elif 'spjimr' in name_lower:
        return 'spjimr'
    elif 'jbims' in name_lower:
        return 'jbims'
    elif 'iift' in name_lower:
        return 'iift'
    elif 'nmims' in name_lower:
        return 'nmims'
    elif 'sibm' in name_lower:
        return 'sibm'
    elif 'scmhrd' in name_lower:
        return 'scmhrd'
    elif 'ximb' in name_lower or 'xim' in name_lower:
        return 'ximb'
    elif 'imt' in name_lower:
        return 'imt'
    elif 'imi' in name_lower:
        return 'imi'
    elif 'tapmi' in name_lower:
        return 'tapmi'
    elif 'great lakes' in name_lower:
        return 'greatlakes'
    
    # European schools
    elif 'insead' in name_lower:
        return 'insead'
    elif 'london business school' in name_lower:
        return 'london'
    elif 'hec paris' in name_lower:
        return 'hec'
    elif 'iese' in name_lower:
        return 'iese'
    elif 'imd' in name_lower:
        return 'imd'
    elif 'ie business' in name_lower:
        return 'ie'
    elif 'sda bocconi' in name_lower:
        return 'unibocconi'
    elif 'esade' in name_lower:
        return 'esade'
    elif 'cambridge' in name_lower and 'judge' in name_lower:
        return 'jbs.cam'
    elif 'oxford' in name_lower and 'said' in name_lower:
        return 'sbs.ox'
    elif 'imperial' in name_lower:
        return 'imperial'
    elif 'warwick' in name_lower:
        return 'wbs.warwick'
    elif 'manchester' in name_lower:
        return 'manchester'
    elif 'essec' in name_lower:
        return 'essec'
    elif 'escp' in name_lower:
        return 'escp'
    elif 'rotterdam' in name_lower:
        return 'rsm'
    elif 'st. gallen' in name_lower or 'st gallen' in name_lower:
        return 'unisg'
    elif 'whu' in name_lower:
        return 'whu'
    elif 'mannheim' in name_lower:
        return 'mannheim'
    elif 'edhec' in name_lower:
        return 'edhec'
    elif 'emlyon' in name_lower:
        return 'em-lyon'
    elif 'grenoble' in name_lower:
        return 'grenoble-em'
    elif 'copenhagen' in name_lower:
        return 'cbs'
    elif 'stockholm' in name_lower:
        return 'hhs'
    elif 'nhh' in name_lower or 'norwegian' in name_lower:
        return 'nhh'
    
    # Default: try to extract the main identifier
    else:
        # Remove common suffixes
        clean = re.sub(r'\s*-?\s*(school|college|faculty|graduate|business|management|university|of|the|at)\s*', ' ', name_lower)
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        # Take first significant word
        words = clean.split()
        if words:
            return words[0]
    
    return name

# Function to download logo
def download_logo(school, index, total):
    clean_name = clean_school_name(school)
    safe_filename = "".join(c for c in school if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename.replace(' ', '_')[:100]  # Limit filename length
    
    # Check if already downloaded
    existing_files = [
        f"logos/business_school_logos/{safe_filename}.png",
        f"logos/business_school_logos/{safe_filename}.jpg",
        f"logos/business_school_logos/{safe_filename}.svg"
    ]
    
    for file in existing_files:
        if os.path.exists(file):
            return {'school': school, 'status': 'skipped', 'reason': 'already_exists', 'filepath': file}
    
    print(f"[{index}/{total}] Downloading logo for: {school} (cleaned: {clean_name})")
    
    # Try multiple domains
    domains = ['.edu', '.com', '.org', '.net', '.ac.uk', '.ca', '.ac.in', '.edu.sg', '.fr']
    
    methods = []
    for domain in domains:
        # Clearbit
        methods.append({
            'name': f'Clearbit{domain}',
            'url': f"https://logo.clearbit.com/{urllib.parse.quote(clean_name)}{domain}",
            'params': {'size': '512', 'format': 'png'}
        })
        
        # Logo.dev
        methods.append({
            'name': f'Logo.dev{domain}',
            'url': f"https://img.logo.dev/{urllib.parse.quote(clean_name)}{domain}",
            'params': {'token': 'pk_X8wlC2LJQkCG3ibQQDeQ_g', 'size': '512'}
        })
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for method in methods:
        try:
            response = requests.get(method['url'], headers=headers, params=method['params'], timeout=5)
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                # Determine file extension
                content_type = response.headers.get('content-type', '')
                if 'png' in content_type:
                    ext = 'png'
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    ext = 'jpg'
                elif 'svg' in content_type:
                    ext = 'svg'
                else:
                    ext = 'png'
                
                filepath = f"logos/business_school_logos/{safe_filename}.{ext}"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"  ✓ Successfully downloaded using {method['name']}")
                return {'school': school, 'status': 'success', 'method': method['name'], 'filepath': filepath}
                
        except Exception as e:
            continue
    
    return {'school': school, 'status': 'failed', 'error': 'All methods failed'}

# Test with a few schools first
print("Testing with a few schools first...")
test_schools = business_schools[:5]

for i, school in enumerate(test_schools, 1):
    result = download_logo(school, i, len(test_schools))
    time.sleep(0.5)

print("\nTest complete. Check the logos/business_school_logos directory.")
print("If satisfied, run with --all flag to download all logos")

# Check if --all flag is provided
import sys
if '--all' in sys.argv:
    print(f"\nDownloading all {len(business_schools)} business school logos...")
    
    all_results = []
    
    # Process in batches
    batch_size = 25
    
    for i in range(0, len(business_schools), batch_size):
        batch = business_schools[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(business_schools) + batch_size - 1)//batch_size}")
        
        # Use ThreadPoolExecutor for parallel downloads
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            for j, school in enumerate(batch):
                future = executor.submit(download_logo, school, i+j+1, len(business_schools))
                futures[future] = school
                time.sleep(0.1)
            
            # Collect results
            for future in as_completed(futures):
                result = future.result()
                all_results.append(result)
        
        # Pause between batches
        if i + batch_size < len(business_schools):
            time.sleep(2)
    
    # Save results
    with open('logos/business_school_download_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    successful = sum(1 for r in all_results if r['status'] == 'success')
    failed = sum(1 for r in all_results if r['status'] == 'failed')
    skipped = sum(1 for r in all_results if r['status'] == 'skipped')
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Total processed: {len(all_results)}")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Success rate: {successful/len(all_results)*100:.1f}%")