#!/usr/bin/env python3
"""
Download university logos in batches with progress tracking
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from comprehensive_universities import get_all_universities

# Create output directory
OUTPUT_DIR = 'logos/universities_comprehensive'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check existing logos
existing_logos = set()
check_dirs = ['logos/all_unique_logos', 'logos/institution_logos', 'logos/business_school_logos']

print("Loading existing logos...")
for dir_path in check_dirs:
    if os.path.exists(dir_path):
        count = 0
        for f in os.listdir(dir_path):
            if f.endswith(('.png', '.jpg', '.svg')):
                normalized = f.lower().replace('.png', '').replace('.jpg', '').replace('.svg', '')
                existing_logos.add(normalized)
                count += 1
        if count > 0:
            print(f"  Found {count} logos in {dir_path}")

def download_logo(uni_name, domain):
    """Download a single university logo"""
    # Check if exists
    name_clean = uni_name.lower().replace(' ', '_').replace('university', '').replace('college', '').strip('_')
    if name_clean in existing_logos:
        return {'university': uni_name, 'status': 'exists', 'domain': domain}
    
    # Clean filename
    filename_base = uni_name.replace(' ', '_').replace('/', '_').replace('&', 'and')
    
    # Try Clearbit
    url = f"https://logo.clearbit.com/{domain}"
    try:
        response = requests.get(url, timeout=5, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
            filename = f"{filename_base}.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return {
                'university': uni_name,
                'status': 'success',
                'domain': domain,
                'size': len(response.content)
            }
    except:
        pass
    
    return {'university': uni_name, 'status': 'failed', 'domain': domain}

def main():
    all_universities = get_all_universities()
    total = len(all_universities)
    
    print(f"\n{'='*60}")
    print(f"DOWNLOADING {total} UNIVERSITY LOGOS")
    print(f"{'='*60}\n")
    
    results = []
    success = 0
    exists = 0
    failed = 0
    
    # Process in smaller batches
    batch_size = 20
    items = list(all_universities.items())
    
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        batch_num = i//batch_size + 1
        total_batches = (len(items) + batch_size - 1)//batch_size
        
        print(f"Processing batch {batch_num}/{total_batches}...")
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(download_logo, uni, domain): uni 
                      for uni, domain in batch}
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                if result['status'] == 'success':
                    success += 1
                elif result['status'] == 'exists':
                    exists += 1
                else:
                    failed += 1
        
        # Progress update every 5 batches
        if batch_num % 5 == 0:
            print(f"  Progress: {i+batch_size}/{total} - Success: {success}, Exists: {exists}, Failed: {failed}")
        
        # Rate limiting
        time.sleep(0.5)
    
    # Save results
    with open('logos/university_results.json', 'w') as f:
        json.dump({
            'total': total,
            'success': success,
            'exists': exists,
            'failed': failed,
            'coverage': (success + exists) / total * 100,
            'results': results
        }, f, indent=2)
    
    print(f"\n{'='*60}")
    print("DOWNLOAD COMPLETE")
    print(f"{'='*60}")
    print(f"Total universities: {total}")
    print(f"Successfully downloaded: {success}")
    print(f"Already existed: {exists}")
    print(f"Failed: {failed}")
    print(f"Coverage: {(success + exists)/total*100:.1f}%")
    print(f"\nResults saved to: logos/university_results.json")
    print(f"Logos saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()