import os
import time
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import re

# Create directory for institution logos
os.makedirs('logos/institution_logos', exist_ok=True)

# Read the list of institutions to download
with open('logos/institutions_to_download.txt', 'r') as f:
    institutions = [line.strip() for line in f if line.strip()]

# Function to clean institution name for better logo search
def clean_institution_name(name):
    # Remove common suffixes and clean up
    name = name.lower()
    
    # Handle special patterns
    patterns_to_clean = [
        r'-cdn$', r'-asset[s]?$', r'-static$', r'-media$',
        r'^cdn-', r'^static-', r'^assets-',
        r'-cloudfront$', r'-akamaized$',
        r'-business-school$', r'-university$', r'-college$',
        r'\.com\.(br|cn|ar|mx|co|pe|hk|tw|sg|my|id|ph|th|vn|za|ke|ng|eg|sa|qa|ae|il|tr|ru|ua|pl|cz|hu|ro|bg|hr|si|sk|lt|lv|ee)$',
        r'com(br|cn|ar|mx|co|pe|hk|tw|sg|my|id|ph|th|vn|za|ke|ng|eg|sa|qa|ae|il|tr|ru|ua|pl|cz|hu|ro|bg|hr|si|sk|lt|lv|ee)$',
        r'edu(cn|sg|hk|my|ph|th|au|nz|uk|ca|mx|br|ar|co|pe|cl|za|eg|sa|qa|ae|il|tr|ru|ua|pl|cz|hu|ro|bg|hr|si|sk|lt|lv|ee)$',
        r'ac(id|th|uk|nz|za|il|jp|kr|cn|in)$',
        r'org(uk|au|nz|za|br|ar|mx|co|pe|cl|eg|sa|qa|ae|il|tr|ru|ua|pl|cz|hu|ro|bg|hr|si|sk|lt|lv|ee)$',
        r'go-jp$', r'gov-cn$', r'-gov$', r'gov$',
        r'cojp$', r'coin$', r'coza$', r'comau$', r'couk$',
        r'nl$', r'de$', r'fr$', r'it$', r'es$', r'pt$', r'ch$', r'at$', r'be$', r'dk$', r'se$', r'no$', r'fi$',
        r'jp$', r'kr$', r'cn$', r'hk$', r'tw$', r'sg$', r'my$', r'id$', r'ph$', r'th$', r'vn$',
        r'in$', r'pk$', r'bd$', r'lk$',
        r'au$', r'nz$',
        r'za$', r'ke$', r'ng$', r'eg$', r'ma$', r'tn$', r'dz$',
        r'sa$', r'ae$', r'qa$', r'kw$', r'om$', r'bh$', r'jo$', r'lb$', r'il$', r'tr$',
        r'ru$', r'ua$', r'pl$', r'cz$', r'sk$', r'hu$', r'ro$', r'bg$', r'hr$', r'si$',
        r'lt$', r'lv$', r'ee$',
        r'br$', r'ar$', r'mx$', r'co$', r'pe$', r'cl$', r've$', r'ec$', r'uy$', r'py$', r'bo$',
        r'ca$', r'us$'
    ]
    
    cleaned = name
    for pattern in patterns_to_clean:
        cleaned = re.sub(pattern, '', cleaned)
    
    # Remove numbers at the end
    cleaned = re.sub(r'-?\d+$', '', cleaned)
    
    # Special institution mappings
    replacements = {
        # Universities and schools
        'harvard-business-school': 'harvard',
        'stanford-business-school': 'stanford',
        'london-business-school': 'lbs',
        'kellogg-northwestern': 'kellogg',
        'duke-fuqua': 'fuqua',
        'cornell-johnson': 'johnson.cornell',
        'columbia': 'columbia',
        'yale-som': 'yale',
        'michigan-state-broad': 'broad.msu',
        'georgia-tech-scheller': 'scheller.gatech',
        'florida-warrington': 'warrington.ufl',
        'texas-mccombs': 'mccombs.utexas',
        'ucla-anderson': 'anderson.ucla',
        'nyu-stern': 'stern.nyu',
        'iim-bangalore': 'iimb',
        'iim-calcutta': 'iimc',
        'iim-lucknow': 'iiml',
        'indian-school-business': 'isb',
        
        # Tech companies
        'google-maps': 'google',
        'google-ventures': 'gv',
        'facebook': 'meta',
        'reality-labs': 'meta',
        'copilot-microsoft': 'microsoft',
        'teamsmicrosoft': 'microsoft',
        'activisionblizzard': 'activisionblizzard',
        'epic': 'epicgames',
        
        # Financial
        'jpmorgan': 'jpmorganchase',
        'goldman': 'goldmansachs',
        'blackrock': 'blackrock',
        'state-bank-india': 'sbi',
        'hdfc': 'hdfcbank',
        'icici': 'icicibank',
        'kotak': 'kotak',
        
        # CDN and static assets - try parent company
        'cdn-doordash': 'doordash',
        'cdn-shopify': 'shopify',
        'static-cdninstagram': 'instagram',
        'static-licdn': 'linkedin',
        'assets-nflxext': 'netflix',
        
        # Special cases
        'ernst-young': 'ey',
        'tata-consultancy': 'tcs',
        'andreessen-horowitz': 'a16z',
        'sequoia-capital': 'sequoiacap',
        'benchmark-capital': 'benchmark',
        'lightspeed-venture': 'lsvp',
        'new-enterprise-associates': 'nea',
        'kleiner-perkins': 'kleinerperkins',
        'matrix-partners': 'matrixpartners',
        'balderton-capital': 'balderton',
        'greylock-partners': 'greylock'
    }
    
    # Apply replacements
    for old, new in replacements.items():
        if old in cleaned:
            cleaned = new
            break
    
    # Remove hyphens and underscores for some cases
    if len(cleaned) < 5 and '-' in cleaned:
        cleaned = cleaned.replace('-', '')
    
    return cleaned.strip()

# Function to download logo using multiple methods
def download_logo(institution, index, total):
    clean_name = clean_institution_name(institution)
    safe_filename = "".join(c for c in institution if c.isalnum() or c in ('-', '_')).rstrip()
    
    # Check if already downloaded
    existing_files = [
        f"logos/institution_logos/{safe_filename}.png",
        f"logos/institution_logos/{safe_filename}.jpg",
        f"logos/institution_logos/{safe_filename}.svg"
    ]
    
    for file in existing_files:
        if os.path.exists(file):
            return {'institution': institution, 'status': 'skipped', 'reason': 'already_exists', 'filepath': file}
    
    print(f"[{index}/{total}] Downloading logo for: {institution} (cleaned: {clean_name})")
    
    # Try multiple logo sources with different domain extensions
    methods = []
    
    # Common domain extensions to try
    domains = ['.com', '.org', '.net', '.io', '.co', '.ai', '.app', '.dev', '.edu']
    
    # For each domain, try multiple logo services
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
        
        # Brandfetch
        methods.append({
            'name': f'Brandfetch{domain}',
            'url': f"https://cdn.brandfetch.io/{urllib.parse.quote(clean_name)}{domain}/w/512/h/512",
            'params': {}
        })
    
    # Also try without domain for single-word names
    if '.' not in clean_name and '-' not in clean_name:
        methods.insert(0, {
            'name': 'Direct-Clearbit',
            'url': f"https://logo.clearbit.com/{urllib.parse.quote(clean_name)}",
            'params': {'size': '512', 'format': 'png'}
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
                    ext = 'png'  # default
                
                filepath = f"logos/institution_logos/{safe_filename}.{ext}"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"  ✓ Successfully downloaded using {method['name']}")
                return {'institution': institution, 'status': 'success', 'method': method['name'], 'filepath': filepath}
                
        except Exception as e:
            continue
    
    return {'institution': institution, 'status': 'failed', 'error': 'All methods failed'}

# Test with a few institutions first
print("Testing with a few institutions first...")
test_institutions = institutions[:5]

for i, inst in enumerate(test_institutions, 1):
    result = download_logo(inst, i, len(test_institutions))
    time.sleep(0.5)

print("\nTest complete. Check the logos/institution_logos directory.")
print("If satisfied, run with --all flag to download all logos")

# Check if --all flag is provided
import sys
if '--all' in sys.argv:
    print(f"\nDownloading all {len(institutions)} institution logos...")
    
    # Load previous results if exists
    results_file = 'logos/institution_download_results.json'
    if os.path.exists(results_file):
        with open(results_file, 'r') as f:
            all_results = json.load(f)
        processed = {r['institution'] for r in all_results}
        institutions_to_process = [inst for inst in institutions if inst not in processed]
    else:
        all_results = []
        institutions_to_process = institutions
    
    print(f"Already processed: {len(institutions) - len(institutions_to_process)}")
    print(f"To process: {len(institutions_to_process)}")
    
    # Process in batches
    batch_size = 50
    
    for i in range(0, len(institutions_to_process), batch_size):
        batch = institutions_to_process[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(institutions_to_process) + batch_size - 1)//batch_size}")
        
        # Use ThreadPoolExecutor for parallel downloads
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            for j, inst in enumerate(batch):
                future = executor.submit(download_logo, inst, i+j+1, len(institutions_to_process))
                futures[future] = inst
                time.sleep(0.1)
            
            # Collect results
            for future in as_completed(futures):
                result = future.result()
                all_results.append(result)
        
        # Save results after each batch
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        # Pause between batches
        if i + batch_size < len(institutions_to_process):
            time.sleep(2)
    
    # Final summary
    successful = sum(1 for r in all_results if r['status'] == 'success')
    failed = sum(1 for r in all_results if r['status'] == 'failed')
    skipped = sum(1 for r in all_results if r['status'] == 'skipped')
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Total processed: {len(all_results)}")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped}")