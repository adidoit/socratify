import os
import time
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Create directory for global logos
os.makedirs('logos/global_mba_logos', exist_ok=True)

# Read the list of employers
with open('logos/global_mba_employers.txt', 'r') as f:
    employers = [line.strip() for line in f if line.strip()]

# Function to clean company name for better logo search
def clean_company_name(name):
    # Remove common suffixes and clean up
    suffixes_to_remove = [
        ' Corporation', ' Corp', ' Inc.', ' Inc', ' LLC', ' LLP', ' Ltd', ' Limited',
        ' Group', ' Company', ' & Company', ' & Co.', ' & Co', ' Holdings',
        ' International', ' Global', ' Worldwide', ' Systems', ' Technologies',
        ' Partners', ' Ventures', ' Capital', ' Financial', ' Bank', ' Securities'
    ]
    
    clean_name = name
    for suffix in suffixes_to_remove:
        if clean_name.endswith(suffix):
            clean_name = clean_name[:-len(suffix)]
            break
    
    # Special cases and mappings
    replacements = {
        # Already downloaded companies from CSV - skip
        'Amazon.com': 'Amazon',
        'McKinsey & Company': 'McKinsey',
        'Boston Consulting Group': 'BCG',
        'The Boston Consulting Group': 'BCG',
        'Bain & Company': 'Bain',
        'JPMorgan Chase': 'JPMorgan',
        'Goldman Sachs': 'GoldmanSachs',
        'Morgan Stanley': 'MorganStanley',
        'Bank of America': 'BankofAmerica',
        'Wells Fargo': 'WellsFargo',
        'Credit Suisse': 'CreditSuisse',
        'Deutsche Bank': 'DeutscheBank',
        'Procter & Gamble': 'PG',
        'Johnson & Johnson': 'JNJ',
        'Eli Lilly': 'LillyUSA',
        'Bristol Myers Squibb': 'BMS',
        'L\'Oreal': 'Loreal',
        'LVMH': 'LVMH',
        'Societe Generale': 'SocGen',
        'BNP Paribas': 'BNPParibas',
        'Standard Chartered': 'StandardChartered',
        'Rolls-Royce': 'RollsRoyce',
        'Mercedes-Benz': 'MercedesBenz',
        'Tata Consultancy Services': 'TCS',
        'State Bank of India': 'SBI',
        'Industrial and Commercial Bank of China': 'ICBC',
        'China Construction Bank': 'CCB',
        'Agricultural Bank of China': 'ABC',
        'Bank of China': 'BOC',
        'Seven & i Holdings': '7Eleven',
        'CK Hutchison': 'CKHutchison',
        'Sun Hung Kai Properties': 'SHKP',
        'Commonwealth Bank': 'CommBank',
        'National Australia Bank': 'NAB',
        'SoftBank Vision Fund': 'SoftBank',
        'First Round Capital': 'FirstRound',
        'Union Square Ventures': 'USV',
        'Battery Ventures': 'Battery',
        'Lightspeed Venture Partners': 'Lightspeed'
    }
    
    if name in replacements:
        clean_name = replacements[name]
    
    return clean_name.strip()

# Function to download logo using multiple methods
def download_logo(employer, index, total):
    clean_name = clean_company_name(employer)
    safe_filename = "".join(c for c in employer if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename.replace(' ', '_')
    
    # Check if already downloaded
    existing_files = [
        f"logos/global_mba_logos/{safe_filename}.png",
        f"logos/global_mba_logos/{safe_filename}.jpg",
        f"logos/global_mba_logos/{safe_filename}.svg"
    ]
    
    for file in existing_files:
        if os.path.exists(file):
            print(f"[{index}/{total}] Skipping {employer} - already downloaded")
            return {'employer': employer, 'status': 'skipped', 'reason': 'already_exists', 'filepath': file}
    
    print(f"[{index}/{total}] Downloading logo for: {employer} (cleaned: {clean_name})")
    
    # Try multiple logo sources
    methods = [
        # Method 1: Clearbit Logo API
        {
            'name': 'Clearbit',
            'url': f"https://logo.clearbit.com/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.com",
            'params': {'size': '512', 'format': 'png'}
        },
        # Method 2: Logo.dev API
        {
            'name': 'Logo.dev',
            'url': f"https://img.logo.dev/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.com",
            'params': {'token': 'pk_X8wlC2LJQkCG3ibQQDeQ_g', 'size': '512'}
        },
        # Method 3: Brandfetch
        {
            'name': 'Brandfetch',
            'url': f"https://cdn.brandfetch.io/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.com/w/512/h/512",
            'params': {}
        },
        # Method 4: Try with .co.uk for UK companies
        {
            'name': 'Clearbit-UK',
            'url': f"https://logo.clearbit.com/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.co.uk",
            'params': {'size': '512', 'format': 'png'}
        },
        # Method 5: Try with .in for Indian companies
        {
            'name': 'Clearbit-IN',
            'url': f"https://logo.clearbit.com/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.in",
            'params': {'size': '512', 'format': 'png'}
        }
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for method in methods:
        try:
            response = requests.get(method['url'], headers=headers, params=method['params'], timeout=10)
            
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
                
                filepath = f"logos/global_mba_logos/{safe_filename}.{ext}"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"  ✓ Successfully downloaded using {method['name']}")
                return {'employer': employer, 'status': 'success', 'method': method['name'], 'filepath': filepath}
                
        except Exception as e:
            continue
    
    print(f"  ✗ Failed to download logo for: {employer}")
    return {'employer': employer, 'status': 'failed', 'error': 'All methods failed'}

# Load previous results if exists
results_file = 'logos/global_download_results.json'
if os.path.exists(results_file):
    with open(results_file, 'r') as f:
        all_results = json.load(f)
else:
    all_results = []

# Create a set of already processed companies
processed = {r['employer'] for r in all_results}

# Filter out already processed companies
employers_to_process = [emp for emp in employers if emp not in processed]

print(f"Total employers: {len(employers)}")
print(f"Already processed: {len(processed)}")
print(f"To process: {len(employers_to_process)}")

if employers_to_process:
    print(f"\nDownloading logos for {len(employers_to_process)} companies...")
    
    # Process in batches to avoid overwhelming the APIs
    batch_size = 50
    
    for i in range(0, len(employers_to_process), batch_size):
        batch = employers_to_process[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1}/{(len(employers_to_process) + batch_size - 1)//batch_size}")
        
        # Use ThreadPoolExecutor for parallel downloads
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {}
            for j, employer in enumerate(batch):
                future = executor.submit(download_logo, employer, i+j+1, len(employers_to_process))
                futures[future] = employer
                time.sleep(0.1)  # Small delay between submissions
            
            # Collect results
            for future in as_completed(futures):
                result = future.result()
                all_results.append(result)
        
        # Save results after each batch
        with open(results_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        # Pause between batches
        if i + batch_size < len(employers_to_process):
            print("Pausing between batches...")
            time.sleep(2)

# Final summary
successful = sum(1 for r in all_results if r['status'] == 'success')
failed = sum(1 for r in all_results if r['status'] == 'failed')
skipped = sum(1 for r in all_results if r['status'] == 'skipped')

print(f"\n=== FINAL SUMMARY ===")
print(f"Total processed: {len(all_results)}")
print(f"Successfully downloaded: {successful}")
print(f"Failed: {failed}")
print(f"Skipped (already exists): {skipped}")

# Save failed companies for reference
failed_companies = [r['employer'] for r in all_results if r['status'] == 'failed']
if failed_companies:
    with open('logos/global_failed_companies.txt', 'w') as f:
        for company in sorted(failed_companies):
            f.write(f"{company}\n")
    print(f"\nFailed companies saved to: logos/global_failed_companies.txt")