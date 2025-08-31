import os
import time
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Create logos directory if it doesn't exist
os.makedirs('logos/downloaded', exist_ok=True)

# Read the list of employers
with open('logos/unique_employers.txt', 'r') as f:
    employers = [line.strip() for line in f if line.strip()]

# Function to clean company name for better logo search
def clean_company_name(name):
    # Remove common suffixes and clean up
    suffixes_to_remove = [
        ' Corporation', ' Corp', ' Inc.', ' Inc', ' LLC', ' LLP', ' Ltd', ' Limited',
        ' Group', ' Company', ' & Company', ' & Co.', ' & Co', ' Holdings',
        ' International', ' Global', ' Worldwide', ' Systems', ' Technologies'
    ]
    
    clean_name = name
    for suffix in suffixes_to_remove:
        if clean_name.endswith(suffix):
            clean_name = clean_name[:-len(suffix)]
            break
    
    # Special cases
    replacements = {
        'Amazon.com': 'Amazon',
        'Nike, Inc.': 'Nike',
        'Citigroup, Inc.': 'Citigroup',
        'Meta (Facebook)': 'Meta',
        'PricewaterhouseCoopers': 'PwC',
        'PricewaterhouseCoopers International Ltd': 'PwC',
        'AT&T': 'ATT',
        'EY-Parthenon': 'EY',
        'EY Parthenon': 'EY',
        'EY-P': 'EY',
        'The Boston Consulting Group': 'BCG',
        'JP Morgan Chase': 'JPMorgan',
        'J.P. Morgan': 'JPMorgan',
        'J.P. Morgan Chase': 'JPMorgan',
        'JP Morgan': 'JPMorgan',
        'JPMorgan Chase & Co.': 'JPMorgan',
        'Goldman Sachs & Company': 'Goldman Sachs',
        'Goldman Sachs Group': 'Goldman Sachs',
        'McKinsey & Company': 'McKinsey',
        'Bain & Company': 'Bain',
        'A.T. Kearney': 'Kearney',
        'AB InBev': 'ABInBev',
        'ABInBev': 'ABInBev',
        'Wells Fargo Corporate & Investment Banking': 'Wells Fargo',
        'Bank of America Merrill Lynch': 'Bank of America',
        'Bank of America Securities': 'Bank of America',
        'Bank of America Corporation': 'Bank of America',
        'The Walt Disney Company': 'Disney',
        'The Home Depot': 'HomeDepot',
        'The Blackstone Group': 'Blackstone',
        'The Clorox Company': 'Clorox',
        'The Hershey Company': 'Hershey',
        'The Cigna Group': 'Cigna',
        'Employer1': 'skip',
        'Employer2': 'skip',
        'Employer3': 'skip',
        'Employer4': 'skip',
        'Employer5': 'skip',
        'Employer6': 'skip',
        'Employer7': 'skip',
        'Employer8': 'skip',
        'Employer9': 'skip',
        'Employer10': 'skip'
    }
    
    if clean_name in replacements:
        clean_name = replacements[clean_name]
    
    return clean_name.strip()

# Function to download logo using multiple methods
def download_logo(employer, index, total):
    clean_name = clean_company_name(employer)
    
    # Skip placeholder employer names
    if clean_name == 'skip':
        return {'employer': employer, 'status': 'skipped', 'reason': 'placeholder'}
    
    safe_filename = "".join(c for c in employer if c.isalnum() or c in (' ', '-', '_')).rstrip()
    
    print(f"[{index}/{total}] Downloading logo for: {employer} (cleaned: {clean_name})")
    
    # Try multiple logo sources
    methods = [
        # Method 1: Clearbit Logo API (free, no key required)
        {
            'name': 'Clearbit',
            'url': f"https://logo.clearbit.com/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.com",
            'params': {'size': '512'}
        },
        # Method 2: Logo.dev API (free tier)
        {
            'name': 'Logo.dev',
            'url': f"https://img.logo.dev/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.com",
            'params': {'token': 'pk_X8wlC2LJQkCG3ibQQDeQ_g', 'size': '512'}  # Free public token
        },
        # Method 3: Brandfetch API
        {
            'name': 'Brandfetch',
            'url': f"https://cdn.brandfetch.io/{urllib.parse.quote(clean_name.lower().replace(' ', ''))}.com/w/512/h/512",
            'params': {}
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
                
                filepath = f"logos/downloaded/{safe_filename}.{ext}"
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"  ✓ Successfully downloaded using {method['name']}: {filepath}")
                return {'employer': employer, 'status': 'success', 'method': method['name'], 'filepath': filepath}
                
        except Exception as e:
            continue
    
    print(f"  ✗ Failed to download logo for: {employer}")
    return {'employer': employer, 'status': 'failed', 'error': 'All methods failed'}

# Test with a few companies first
print("Testing with a few companies first...")
test_companies = employers[:5]

for i, employer in enumerate(test_companies, 1):
    result = download_logo(employer, i, len(test_companies))
    time.sleep(0.5)  # Be respectful to APIs

print("\nTest complete. Check the logos/downloaded directory to verify quality.")
print("If satisfied, run with --all flag to download all logos")

# Save results
results_file = 'logos/download_results.json'
if os.path.exists(results_file):
    with open(results_file, 'r') as f:
        all_results = json.load(f)
else:
    all_results = []

# Check if --all flag is provided
import sys
if '--all' in sys.argv:
    print(f"\nDownloading all {len(employers)} logos...")
    
    # Use ThreadPoolExecutor for parallel downloads
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for i, employer in enumerate(employers, 1):
            future = executor.submit(download_logo, employer, i, len(employers))
            futures[future] = employer
            time.sleep(0.1)  # Small delay between submissions
        
        # Collect results
        for future in as_completed(futures):
            result = future.result()
            all_results.append(result)
    
    # Save results
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Summary
    success_count = sum(1 for r in all_results if r['status'] == 'success')
    print(f"\n✓ Downloaded {success_count}/{len(employers)} logos successfully")
    
    # List failed downloads
    failed = [r['employer'] for r in all_results if r['status'] == 'failed']
    if failed:
        print(f"\n✗ Failed to download logos for {len(failed)} companies:")
        for company in failed[:10]:
            print(f"  - {company}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")