#!/usr/bin/env python3
"""
Download comprehensive global employer logos
805 organizations across all regions and industries
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from global_employers_comprehensive import get_all_comprehensive_companies
from global_employers_comprehensive import (
    ASIA_PACIFIC_COMPANIES, MIDDLE_EAST_COMPANIES, LATIN_AMERICAN_COMPANIES,
    AFRICAN_COMPANIES, LUXURY_RETAIL_COMPANIES, PHARMA_HEALTHCARE_COMPANIES,
    ENERGY_INFRASTRUCTURE_COMPANIES, GOVERNMENT_MULTILATERAL_ORGS,
    BOUTIQUE_FIRMS, MEDIA_ENTERTAINMENT_COMPANIES, REAL_ESTATE_COMPANIES
)

# Create output directory
OUTPUT_DIR = 'logos/comprehensive_global'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check existing logos
existing_logos = set()
check_dirs = [
    'logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos',
    'logos/business_school_logos', 'logos/comprehensive_fix', 
    'logos/expanded_business_schools', 'logos/employers_2025',
    'logos/comprehensive_global'
]

for dir_path in check_dirs:
    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            if f.endswith(('.png', '.jpg', '.svg')):
                # Multiple ways to identify same company
                name_parts = f.lower().replace('.png', '').replace('.jpg', '').replace('.svg', '')
                existing_logos.add(name_parts)
                # Also add individual words
                for part in name_parts.split('_'):
                    if len(part) > 3:
                        existing_logos.add(part)

def company_exists(company_name):
    """Check if company already exists"""
    name_lower = company_name.lower().replace(' ', '').replace('&', '').replace('.', '').replace('-', '')
    
    # Direct check
    if name_lower in existing_logos:
        return True
    
    # Check key parts
    key_parts = company_name.lower().split()
    for part in key_parts:
        if len(part) > 4 and part in existing_logos:
            return True
    
    # Special cases
    special_mappings = {
        "L'Oréal": "loreal",
        "Moët Hennessy": "lvmh",
        "Richemont": "cartier",
        "Swatch Group": "omega",
        "Yum! Brands": "yum",
        "AB InBev": "budweiser",
        "Mondelez": "kraft",
        "Publicis": "publicisgroupe"
    }
    
    if company_name in special_mappings:
        if special_mappings[company_name] in existing_logos:
            return True
    
    return False

def download_company_logo(company_name, domain):
    """Download logo for a company"""
    # Quick existence check
    if company_exists(company_name):
        return {
            'company': company_name,
            'status': 'already_exists',
            'domain': domain
        }
    
    # Clean filename
    filename_base = company_name.replace(' ', '_').replace('/', '_').replace(':', '').replace('&', 'and').replace("'", "")
    
    # Try multiple strategies
    strategies = []
    
    # Strategy 1: Direct domain
    strategies.append({'url': f"https://logo.clearbit.com/{domain}", 'name': 'clearbit_direct'})
    
    # Strategy 2: Remove www
    if domain.startswith('www.'):
        strategies.append({'url': f"https://logo.clearbit.com/{domain[4:]}", 'name': 'clearbit_nowww'})
    
    # Strategy 3: For .gov/.org domains, try .com
    if domain.endswith('.gov') or domain.endswith('.org'):
        base = domain.split('.')[0]
        strategies.append({'url': f"https://logo.clearbit.com/{base}.com", 'name': 'clearbit_com'})
    
    # Strategy 4: Parent company domain for subsidiaries
    parent_mappings = {
        "hm.com": "hennes-mauritz.com",
        "zara.com": "inditex.com",
        "cartier.com": "richemont.com",
        "louisvuitton.com": "lvmh.com",
        "gucci.com": "kering.com",
        "rolex.com": "rolex.ch",
        "omega.com": "omegawatches.com"
    }
    
    if domain in parent_mappings:
        strategies.insert(0, {'url': f"https://logo.clearbit.com/{parent_mappings[domain]}", 'name': 'clearbit_parent'})
    
    # Strategy 5: Logo.dev
    strategies.append({'url': f"https://img.logo.dev/{domain}?token=pk_X-1ZO13GSgeOoUrIuCGGfw", 'name': 'logodev'})
    
    # Strategy 6: Try variations
    if ' ' in company_name:
        simplified = company_name.split()[0].lower()
        strategies.append({'url': f"https://logo.clearbit.com/{simplified}.com", 'name': 'clearbit_simple'})
    
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
                    'company': company_name,
                    'status': 'success',
                    'method': strategy['name'],
                    'domain': domain,
                    'filepath': filepath,
                    'size': len(response.content)
                }
        except:
            continue
    
    return {
        'company': company_name,
        'status': 'failed',
        'domain': domain
    }

def main():
    all_companies = get_all_comprehensive_companies()
    
    print("=" * 80)
    print("DOWNLOADING COMPREHENSIVE GLOBAL EMPLOYER LOGOS")
    print("=" * 80)
    print(f"Total organizations to process: {len(all_companies)}")
    print()
    
    # Process by region/category
    categories = [
        ("ASIA-PACIFIC", ASIA_PACIFIC_COMPANIES),
        ("MIDDLE EAST", MIDDLE_EAST_COMPANIES),
        ("LATIN AMERICA", LATIN_AMERICAN_COMPANIES),
        ("AFRICA", AFRICAN_COMPANIES),
        ("LUXURY/RETAIL", LUXURY_RETAIL_COMPANIES),
        ("PHARMA/HEALTHCARE", PHARMA_HEALTHCARE_COMPANIES),
        ("ENERGY/INFRASTRUCTURE", ENERGY_INFRASTRUCTURE_COMPANIES),
        ("GOVERNMENT/MULTILATERAL", GOVERNMENT_MULTILATERAL_ORGS),
        ("BOUTIQUE FIRMS", BOUTIQUE_FIRMS),
        ("MEDIA/ENTERTAINMENT", MEDIA_ENTERTAINMENT_COMPANIES),
        ("REAL ESTATE", REAL_ESTATE_COMPANIES)
    ]
    
    all_results = []
    
    for category_name, companies in categories:
        print(f"\n{'='*60}")
        print(f"PROCESSING {category_name} ({len(companies)} organizations)")
        print(f"{'='*60}")
        
        category_results = []
        success_count = 0
        exists_count = 0
        
        # Process in batches
        batch_size = 10
        company_items = list(companies.items())
        
        for i in range(0, len(company_items), batch_size):
            batch = company_items[i:i+batch_size]
            batch_num = i//batch_size + 1
            total_batches = (len(company_items) + batch_size - 1)//batch_size
            
            print(f"\nBatch {batch_num}/{total_batches}:")
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(download_company_logo, company, domain): company 
                          for company, domain in batch}
                
                for future in as_completed(futures):
                    result = future.result()
                    category_results.append(result)
                    
                    if result['status'] == 'success':
                        success_count += 1
                        print(f"✓ {result['company']:<40} [{result['method']}]")
                    elif result['status'] == 'already_exists':
                        exists_count += 1
                        print(f"◆ {result['company']:<40} [cached]")
                    else:
                        print(f"✗ {result['company']:<40} [failed]")
            
            # Rate limiting
            if i + batch_size < len(company_items):
                time.sleep(2)
        
        # Category summary
        failed_count = len(companies) - success_count - exists_count
        print(f"\n{category_name} Summary:")
        print(f"  New downloads: {success_count}")
        print(f"  Already exist: {exists_count}")
        print(f"  Failed: {failed_count}")
        print(f"  Coverage: {(success_count + exists_count)/len(companies)*100:.1f}%")
        
        all_results.extend(category_results)
        
        # Save intermediate results
        with open('logos/comprehensive_global_results.json', 'w') as f:
            json.dump(all_results, f, indent=2)
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL SUMMARY")
    print("=" * 80)
    
    total_success = sum(1 for r in all_results if r['status'] == 'success')
    total_exists = sum(1 for r in all_results if r['status'] == 'already_exists')
    total_failed = sum(1 for r in all_results if r['status'] == 'failed')
    
    print(f"Total organizations processed: {len(all_results)}")
    print(f"New downloads: {total_success}")
    print(f"Already existed: {total_exists}")
    print(f"Failed: {total_failed}")
    print(f"Overall coverage: {(total_success + total_exists)/len(all_results)*100:.1f}%")
    
    # Show failures by category
    if total_failed > 0:
        print(f"\n{'='*80}")
        print("FAILURES BY CATEGORY")
        print(f"{'='*80}")
        
        for category_name, companies in categories:
            category_failures = [r for r in all_results 
                               if r['status'] == 'failed' and r['company'] in companies]
            if category_failures:
                print(f"\n{category_name} ({len(category_failures)} failures):")
                for r in category_failures[:5]:
                    print(f"  • {r['company']} ({r['domain']})")
                if len(category_failures) > 5:
                    print(f"  ... and {len(category_failures) - 5} more")
    
    print(f"\nResults saved to: logos/comprehensive_global_results.json")
    print(f"Logos saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()