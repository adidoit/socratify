import os
import time
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Read the truly missing schools
with open('logos/truly_missing_business_schools.txt', 'r') as f:
    missing_schools = [line.strip() for line in f if line.strip()]

print(f"Found {len(missing_schools)} missing business school logos to download")

# Enhanced function to get the best search term for each school
def get_school_search_terms(school_name):
    """Return multiple search terms to try for a school"""
    school_lower = school_name.lower()
    search_terms = []
    
    # Try the full school name first
    search_terms.append(school_name)
    
    # Extract university name if present
    if 'university' in school_lower:
        # Pattern: "University of X" or "X University"
        import re
        univ_match = re.search(r'university of (\w+)', school_lower)
        if univ_match:
            search_terms.append(univ_match.group(1))
        
        univ_match2 = re.search(r'(\w+) university', school_lower)
        if univ_match2:
            search_terms.append(univ_match2.group(1))
    
    # Extract business school name
    parts = school_name.split(' - ')
    if len(parts) > 1:
        search_terms.append(parts[0])  # Business school name
        search_terms.append(parts[1])  # University name
    
    # Special cases and known patterns
    special_mappings = {
        'boston college carroll': 'bc',
        'michigan state broad': 'msu',
        'georgia terry': 'uga',
        'maryland smith': 'umd',
        'rochester simon': 'rochester',
        'boston university questrom': 'bu',
        'smu cox': 'smu',
        'uc davis': 'ucdavis',
        'colorado leeds': 'colorado',
        'fordham gabelli': 'fordham',
        'miami business school': 'miami',
        'temple fox': 'temple',
        'texas a&m mays': 'tamu',
        'tulane freeman': 'tulane',
        'pepperdine graziadio': 'pepperdine',
        'thunderbird': 'thunderbird',
        # International schools
        'insead': 'insead',
        'london business school': 'lbs london',
        'hec paris': 'hec paris',
        'iese': 'iese barcelona',
        'imd': 'imd lausanne',
        'ie business': 'ie university',
        'sda bocconi': 'bocconi',
        'esade': 'esade barcelona',
        'cambridge judge': 'cambridge',
        'oxford said': 'oxford',
        'imperial college': 'imperial',
        'warwick business': 'warwick',
        'manchester alliance': 'manchester',
        'essec': 'essec',
        'escp': 'escp europe',
        'rotterdam school': 'rsm erasmus',
        'st. gallen': 'unisg',
        'whu otto': 'whu',
        'copenhagen business': 'cbs dk',
        'stockholm school': 'hhs se',
        'nhh norwegian': 'nhh no'
    }
    
    # Check for special mappings
    for pattern, term in special_mappings.items():
        if pattern in school_lower:
            search_terms.append(term)
    
    # Remove duplicates while preserving order
    seen = set()
    unique_terms = []
    for term in search_terms:
        if term not in seen:
            seen.add(term)
            unique_terms.append(term)
    
    return unique_terms

# Download function
def download_school_logo(school, index, total):
    safe_filename = "".join(c for c in school if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename.replace(' ', '_')[:100]
    
    # Check if already exists
    for ext in ['.png', '.jpg', '.svg']:
        filepath = f"logos/business_school_logos/{safe_filename}{ext}"
        if os.path.exists(filepath):
            return {'school': school, 'status': 'skipped', 'filepath': filepath}
    
    print(f"[{index}/{total}] Downloading: {school}")
    
    search_terms = get_school_search_terms(school)
    
    # Try different methods for each search term
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for search_term in search_terms:
        clean_term = search_term.lower().replace(' ', '').replace('&', 'and')
        
        # Try multiple domains
        domains = ['.edu', '.com', '.org', '.net', '.ac.uk', '.ca', '.fr', '.es', '.it', '.ch', '.dk', '.se', '.no', '.edu.sg', '.ac.in']
        
        for domain in domains:
            methods = [
                {
                    'name': f'Clearbit-{domain}',
                    'url': f"https://logo.clearbit.com/{urllib.parse.quote(clean_term)}{domain}",
                    'params': {'size': '512', 'format': 'png'}
                },
                {
                    'name': f'Logo.dev-{domain}',
                    'url': f"https://img.logo.dev/{urllib.parse.quote(clean_term)}{domain}",
                    'params': {'token': 'pk_X8wlC2LJQkCG3ibQQDeQ_g', 'size': '512'}
                }
            ]
            
            for method in methods:
                try:
                    response = requests.get(method['url'], headers=headers, params=method['params'], timeout=5)
                    
                    if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
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
                        
                        print(f"  ✓ Success! ({search_term}{domain})")
                        return {'school': school, 'status': 'success', 'method': method['name'], 'filepath': filepath}
                        
                except Exception:
                    continue
    
    print(f"  ✗ Failed")
    return {'school': school, 'status': 'failed'}

# Test with a few first
print("\nTesting with first 5 schools...")
test_schools = missing_schools[:5]

for i, school in enumerate(test_schools, 1):
    result = download_school_logo(school, i, len(test_schools))
    time.sleep(0.5)

# Run full download if --all flag is provided
import sys
if '--all' in sys.argv:
    print(f"\nDownloading all {len(missing_schools)} missing school logos...")
    
    all_results = []
    batch_size = 25
    
    for i in range(0, len(missing_schools), batch_size):
        batch = missing_schools[i:i+batch_size]
        print(f"\nBatch {i//batch_size + 1}/{(len(missing_schools) + batch_size - 1)//batch_size}")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            for j, school in enumerate(batch):
                future = executor.submit(download_school_logo, school, i+j+1, len(missing_schools))
                futures[future] = school
                time.sleep(0.1)
            
            for future in as_completed(futures):
                result = future.result()
                all_results.append(result)
        
        if i + batch_size < len(missing_schools):
            time.sleep(2)
    
    # Save results
    with open('logos/final_business_school_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    successful = sum(1 for r in all_results if r['status'] == 'success')
    failed = sum(1 for r in all_results if r['status'] == 'failed')
    skipped = sum(1 for r in all_results if r['status'] == 'skipped')
    
    print(f"\n=== FINAL RESULTS ===")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")
    print(f"Success rate: {successful/(successful+failed)*100:.1f}%")
else:
    print("\nRun with --all flag to download all missing logos")