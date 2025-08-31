#!/usr/bin/env python3
"""
Download logos for comprehensive university list
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from comprehensive_universities import get_all_universities
from comprehensive_universities import (
    US_UNIVERSITIES, CANADIAN_UNIVERSITIES, UK_UNIVERSITIES,
    EUROPEAN_UNIVERSITIES, INDIAN_UNIVERSITIES, AUSTRALIAN_UNIVERSITIES,
    GLOBAL_TOP_UNIVERSITIES
)

# Create output directory
OUTPUT_DIR = 'logos/universities_comprehensive'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check existing logos (including the consolidated folder)
existing_logos = set()
check_dirs = [
    'logos/all_unique_logos',  # Check the consolidated folder
    'logos/institution_logos',
    'logos/business_school_logos',
    'logos/universities_comprehensive'
]

print("Loading existing logos...")
for dir_path in check_dirs:
    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            if f.endswith(('.png', '.jpg', '.svg')):
                # Multiple ways to identify
                normalized = f.lower().replace('.png', '').replace('.jpg', '').replace('.svg', '')
                existing_logos.add(normalized)
                # Also add parts
                for part in normalized.split('_'):
                    if len(part) > 3:
                        existing_logos.add(part)

def university_already_exists(uni_name):
    """Check if we already have this university"""
    # Quick checks
    name_clean = uni_name.lower().replace(' ', '').replace('&', '').replace('.', '').replace('-', '').replace("'", "")
    
    if name_clean in existing_logos:
        return True
    
    # Check key parts
    parts = uni_name.lower().split()
    for part in parts:
        if len(part) > 4 and part in existing_logos:
            # Special cases where part match is not enough
            if part in ['university', 'college', 'institute', 'school', 'academy']:
                continue
            # Check if it's a distinctive part
            if part in ['harvard', 'yale', 'stanford', 'oxford', 'cambridge', 'toronto', 'mcgill']:
                return True
    
    return False

def download_university_logo(uni_name, domain):
    """Download logo for a university"""
    # Check existence
    if university_already_exists(uni_name):
        return {
            'university': uni_name,
            'status': 'already_exists',
            'domain': domain
        }
    
    # Clean filename
    filename_base = uni_name.replace(' ', '_').replace('/', '_').replace(':', '').replace('&', 'and').replace("'", "").replace('.', '')
    
    # Strategies
    strategies = []
    
    # Direct domain
    strategies.append({'url': f"https://logo.clearbit.com/{domain}", 'name': 'clearbit_direct'})
    
    # For .edu domains, also try without subdomain
    if domain.endswith('.edu') and domain.count('.') > 1:
        parent = '.'.join(domain.split('.')[-2:])
        strategies.append({'url': f"https://logo.clearbit.com/{parent}", 'name': 'clearbit_parent'})
    
    # For international domains
    if domain.endswith(('.ac.uk', '.edu.au', '.ac.in', '.ca', '.ac.nz')):
        # Try the main domain
        strategies.append({'url': f"https://logo.clearbit.com/{domain}", 'name': 'clearbit_intl'})
    
    # Logo.dev
    strategies.append({'url': f"https://img.logo.dev/{domain}?token=pk_X-1ZO13GSgeOoUrIuCGGfw", 'name': 'logodev'})
    
    # Special handling for some universities
    special_mappings = {
        "Massachusetts Institute of Technology": "mit.edu",
        "University of California Berkeley": "berkeley.edu",
        "University of California Los Angeles": "ucla.edu",
        "London School of Economics": "lse.ac.uk",
        "ETH Zurich": "ethz.ch",
        "Indian Institute of Science": "iisc.ac.in"
    }
    
    if uni_name in special_mappings:
        strategies.insert(0, {'url': f"https://logo.clearbit.com/{special_mappings[uni_name]}", 'name': 'clearbit_special'})
    
    for strategy in strategies:
        try:
            response = requests.get(strategy['url'], timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                ext = 'png'
                content_type = response.headers.get('content-type', '')
                if 'svg' in content_type:
                    ext = 'svg'
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    ext = 'jpg'
                
                filename = f"{filename_base}.{ext}"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return {
                    'university': uni_name,
                    'status': 'success',
                    'method': strategy['name'],
                    'domain': domain,
                    'filepath': filepath,
                    'size': len(response.content)
                }
        except:
            continue
    
    return {
        'university': uni_name,
        'status': 'failed',
        'domain': domain
    }

def main():
    all_universities = get_all_universities()
    
    print("=" * 80)
    print("COMPREHENSIVE UNIVERSITY LOGO DOWNLOAD")
    print("=" * 80)
    print(f"Total universities to process: {len(all_universities)}")
    print()
    
    # Categories
    categories = [
        ("US UNIVERSITIES", US_UNIVERSITIES),
        ("CANADIAN UNIVERSITIES", CANADIAN_UNIVERSITIES),
        ("UK UNIVERSITIES", UK_UNIVERSITIES),
        ("EUROPEAN UNIVERSITIES", EUROPEAN_UNIVERSITIES),
        ("INDIAN UNIVERSITIES", INDIAN_UNIVERSITIES),
        ("AUSTRALIAN UNIVERSITIES", AUSTRALIAN_UNIVERSITIES),
        ("GLOBAL TOP UNIVERSITIES", GLOBAL_TOP_UNIVERSITIES)
    ]
    
    all_results = []
    
    for category_name, universities in categories:
        print(f"\n{'='*60}")
        print(f"{category_name} ({len(universities)} universities)")
        print(f"{'='*60}")
        
        category_results = []
        success_count = 0
        exists_count = 0
        
        # Process in batches
        batch_size = 10
        university_items = list(universities.items())
        
        for i in range(0, len(university_items), batch_size):
            batch = university_items[i:i+batch_size]
            batch_num = i//batch_size + 1
            total_batches = (len(university_items) + batch_size - 1)//batch_size
            
            print(f"\nBatch {batch_num}/{total_batches}:")
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(download_university_logo, uni, domain): uni 
                          for uni, domain in batch}
                
                for future in as_completed(futures):
                    result = future.result()
                    category_results.append(result)
                    
                    if result['status'] == 'success':
                        success_count += 1
                        print(f"✓ {result['university']:<40} [{result['method']}]")
                    elif result['status'] == 'already_exists':
                        exists_count += 1
                        print(f"◆ {result['university']:<40} [cached]")
                    else:
                        print(f"✗ {result['university']:<40} [failed]")
            
            # Rate limiting
            if i + batch_size < len(university_items):
                time.sleep(1)
        
        # Summary
        failed_count = len(universities) - success_count - exists_count
        print(f"\n{category_name} Summary:")
        print(f"  New: {success_count}, Exists: {exists_count}, Failed: {failed_count}")
        print(f"  Coverage: {(success_count + exists_count)/len(universities)*100:.1f}%")
        
        all_results.extend(category_results)
        
        # Save progress
        with open('logos/university_download_results.json', 'w') as f:
            json.dump(all_results, f, indent=2)
    
    # Final summary
    print("\n" + "=" * 80)
    print("UNIVERSITY DOWNLOAD COMPLETE")
    print("=" * 80)
    
    total_success = sum(1 for r in all_results if r['status'] == 'success')
    total_exists = sum(1 for r in all_results if r['status'] == 'already_exists')
    total_failed = sum(1 for r in all_results if r['status'] == 'failed')
    
    print(f"Total processed: {len(all_results)}")
    print(f"New downloads: {total_success}")
    print(f"Already existed: {total_exists}")
    print(f"Failed: {total_failed}")
    print(f"Coverage: {(total_success + total_exists)/len(all_results)*100:.1f}%")
    
    # Show some failures
    if total_failed > 0:
        failures = [r for r in all_results if r['status'] == 'failed']
        print(f"\nTop failures ({len(failures)} total):")
        for r in failures[:20]:
            print(f"  • {r['university']} ({r['domain']})")
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")
    
    print(f"\nResults: logos/university_download_results.json")
    print(f"Logos: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()