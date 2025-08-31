#!/usr/bin/env python3
"""
Download logos for expanded business school list
Top 100 US, Top 50 Europe, Top 50 India, Top 50 Canada
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from expanded_business_schools import get_all_schools_with_domains, US_BUSINESS_SCHOOLS, EUROPEAN_BUSINESS_SCHOOLS, INDIAN_BUSINESS_SCHOOLS, CANADIAN_BUSINESS_SCHOOLS

# Create output directory
OUTPUT_DIR = 'logos/expanded_business_schools'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check what we already have across all directories
existing_logos = set()
check_dirs = ['logos/business_school_logos', 'logos/expanded_business_schools', 'logos/institution_logos']
for dir_path in check_dirs:
    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            if f.endswith(('.png', '.jpg', '.svg')):
                # Normalize the filename for comparison
                existing_logos.add(f.lower())

def download_school_logo(school_name, domain):
    """Download logo for a single school"""
    # Check if we already have it
    school_clean = school_name.replace(' ', '_').replace('/', '_').replace(':', '')
    if any(school_clean.lower() in existing for existing in existing_logos):
        return {
            'school': school_name,
            'status': 'already_exists',
            'domain': domain
        }
    
    # Try multiple strategies
    strategies = [
        # Direct domain
        {'url': f"https://logo.clearbit.com/{domain}", 'name': 'clearbit_direct'},
        # Parent domain (for subdomains)
        {'url': f"https://logo.clearbit.com/{'.'.join(domain.split('.')[-2:])}", 'name': 'clearbit_parent'},
        # Logo.dev
        {'url': f"https://img.logo.dev/{domain}?token=pk_X-1ZO13GSgeOoUrIuCGGfw", 'name': 'logodev'},
        # Try without subdomain
        {'url': f"https://logo.clearbit.com/{'.'.join(domain.split('.')[-2:])}", 'name': 'clearbit_nodomain'},
    ]
    
    # Special handling for .ac.in domains (Indian schools)
    if domain.endswith('.ac.in'):
        # Try the institution name without .ac.in
        base_domain = domain.replace('.ac.in', '')
        strategies.insert(0, {'url': f"https://logo.clearbit.com/{base_domain}.edu", 'name': 'clearbit_edu'})
        strategies.insert(0, {'url': f"https://logo.clearbit.com/{base_domain}.com", 'name': 'clearbit_com'})
    
    for strategy in strategies:
        try:
            response = requests.get(strategy['url'], timeout=5, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; LogoDownloader/1.0)'
            })
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                # Determine extension
                ext = 'png'
                content_type = response.headers.get('content-type', '')
                if 'svg' in content_type:
                    ext = 'svg'
                elif 'jpeg' in content_type or 'jpg' in content_type:
                    ext = 'jpg'
                
                filename = f"{school_clean}.{ext}"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return {
                    'school': school_name,
                    'status': 'success',
                    'method': strategy['name'],
                    'domain': domain,
                    'filepath': filepath,
                    'size': len(response.content)
                }
        except:
            continue
    
    return {
        'school': school_name,
        'status': 'failed',
        'domain': domain
    }

def main():
    all_schools = get_all_schools_with_domains()
    
    print("=" * 80)
    print("DOWNLOADING EXPANDED BUSINESS SCHOOL LOGOS")
    print("=" * 80)
    print(f"Total schools to process: {len(all_schools)}")
    print(f"- US schools: {len(US_BUSINESS_SCHOOLS)}")
    print(f"- European schools: {len(EUROPEAN_BUSINESS_SCHOOLS)}")
    print(f"- Indian schools: {len(INDIAN_BUSINESS_SCHOOLS)}")
    print(f"- Canadian schools: {len(CANADIAN_BUSINESS_SCHOOLS)}")
    print()
    
    # Process by region for better tracking
    regions = [
        ("US", US_BUSINESS_SCHOOLS),
        ("EUROPE", EUROPEAN_BUSINESS_SCHOOLS),
        ("INDIA", INDIAN_BUSINESS_SCHOOLS),
        ("CANADA", CANADIAN_BUSINESS_SCHOOLS)
    ]
    
    all_results = []
    
    for region_name, schools in regions:
        print(f"\n{'='*60}")
        print(f"PROCESSING {region_name} SCHOOLS ({len(schools)} schools)")
        print(f"{'='*60}")
        
        region_results = []
        success_count = 0
        exists_count = 0
        
        # Process in batches to avoid overwhelming
        batch_size = 10
        school_items = list(schools.items())
        
        for i in range(0, len(school_items), batch_size):
            batch = school_items[i:i+batch_size]
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(download_school_logo, school, domain): school 
                          for school, domain in batch}
                
                for future in as_completed(futures):
                    result = future.result()
                    region_results.append(result)
                    
                    if result['status'] == 'success':
                        success_count += 1
                        print(f"✓ {result['school']:<50} [{result['method']}]")
                    elif result['status'] == 'already_exists':
                        exists_count += 1
                        print(f"◆ {result['school']:<50} [cached]")
                    else:
                        print(f"✗ {result['school']:<50} [failed]")
            
            # Rate limiting between batches
            if i + batch_size < len(school_items):
                time.sleep(1)
        
        # Region summary
        failed_count = len(schools) - success_count - exists_count
        print(f"\n{region_name} Summary:")
        print(f"  New downloads: {success_count}")
        print(f"  Already exist: {exists_count}")
        print(f"  Failed: {failed_count}")
        print(f"  Coverage: {(success_count + exists_count)/len(schools)*100:.1f}%")
        
        all_results.extend(region_results)
    
    # Save all results
    with open('logos/expanded_schools_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    
    total_success = sum(1 for r in all_results if r['status'] == 'success')
    total_exists = sum(1 for r in all_results if r['status'] == 'already_exists')
    total_failed = sum(1 for r in all_results if r['status'] == 'failed')
    
    print(f"Total schools processed: {len(all_results)}")
    print(f"New downloads: {total_success}")
    print(f"Already existed: {total_exists}")
    print(f"Failed: {total_failed}")
    print(f"Overall coverage: {(total_success + total_exists)/len(all_results)*100:.1f}%")
    
    # List failures by region
    if total_failed > 0:
        print("\n" + "=" * 80)
        print("FAILED DOWNLOADS BY REGION")
        print("=" * 80)
        
        for region_name, schools in regions:
            region_failures = [r for r in all_results 
                             if r['status'] == 'failed' and r['school'] in schools]
            if region_failures:
                print(f"\n{region_name} ({len(region_failures)} failures):")
                for r in region_failures[:10]:
                    print(f"  • {r['school']} ({r['domain']})")
                if len(region_failures) > 10:
                    print(f"  ... and {len(region_failures) - 10} more")
    
    print(f"\nResults saved to: logos/expanded_schools_results.json")
    print(f"Logos saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()