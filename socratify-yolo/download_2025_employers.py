#!/usr/bin/env python3
"""
Download logos for 2025 top employers including Australian companies,
hot startups, and missing global employers
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from top_employers_2025 import get_all_new_companies, AUSTRALIAN_BUSINESS_SCHOOLS, AUSTRALIAN_COMPANIES, HOT_COMPANIES_2025, MISSING_GLOBAL_EMPLOYERS

# Create output directory
OUTPUT_DIR = 'logos/employers_2025'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check existing logos across all directories
existing_logos = set()
check_dirs = [
    'logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos',
    'logos/business_school_logos', 'logos/comprehensive_fix', 
    'logos/expanded_business_schools', 'logos/employers_2025'
]

for dir_path in check_dirs:
    if os.path.exists(dir_path):
        for f in os.listdir(dir_path):
            if f.endswith(('.png', '.jpg', '.svg')):
                # Normalize for comparison
                name_parts = f.lower().replace('.png', '').replace('.jpg', '').replace('.svg', '').split('_')
                existing_logos.update(name_parts)

def check_if_exists(company_name):
    """Check if we already have this company's logo"""
    name_lower = company_name.lower().replace(' ', '').replace('&', '').replace('.', '')
    
    # Check exact match
    if name_lower in existing_logos:
        return True
    
    # Check partial matches
    for existing in existing_logos:
        if name_lower in existing or existing in name_lower:
            return True
        # Check key parts
        if len(name_lower) > 5 and len(existing) > 5:
            if name_lower[:5] == existing[:5]:
                return True
    
    return False

def download_company_logo(company_name, domain):
    """Download logo for a single company"""
    # Quick existence check
    if check_if_exists(company_name):
        return {
            'company': company_name,
            'status': 'already_exists',
            'domain': domain
        }
    
    # Clean filename
    filename_base = company_name.replace(' ', '_').replace('/', '_').replace(':', '').replace('&', 'and')
    
    # Try multiple strategies
    strategies = [
        # Direct domain
        {'url': f"https://logo.clearbit.com/{domain}", 'name': 'clearbit_direct'},
        # Try without www
        {'url': f"https://logo.clearbit.com/{domain.replace('www.', '')}", 'name': 'clearbit_nowww'},
        # Logo.dev
        {'url': f"https://img.logo.dev/{domain}?token=pk_X-1ZO13GSgeOoUrIuCGGfw", 'name': 'logodev'},
        # Try company name as domain
        {'url': f"https://logo.clearbit.com/{company_name.lower().replace(' ', '').replace('&', 'and')}.com", 'name': 'clearbit_guess'},
    ]
    
    # Special handling for known difficult cases
    if company_name == "Anthropic":
        strategies.insert(0, {'url': "https://logo.clearbit.com/anthropic.com", 'name': 'clearbit_special'})
    elif company_name == "OpenAI":
        strategies.insert(0, {'url': "https://logo.clearbit.com/openai.com", 'name': 'clearbit_special'})
    elif company_name == "Canva":
        strategies.insert(0, {'url': "https://logo.clearbit.com/canva.com", 'name': 'clearbit_special'})
    
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
    all_companies = get_all_new_companies()
    
    print("=" * 80)
    print("DOWNLOADING 2025 TOP EMPLOYERS & COMPANIES")
    print("=" * 80)
    print(f"Total organizations to process: {len(all_companies)}")
    print(f"- Australian Business Schools: {len(AUSTRALIAN_BUSINESS_SCHOOLS)}")
    print(f"- Australian Companies: {len(AUSTRALIAN_COMPANIES)}")
    print(f"- Hot Companies 2025: {len(HOT_COMPANIES_2025)}")
    print(f"- Missing Global Employers: {len(MISSING_GLOBAL_EMPLOYERS)}")
    print()
    
    # Process by category
    categories = [
        ("AUSTRALIAN BUSINESS SCHOOLS", AUSTRALIAN_BUSINESS_SCHOOLS),
        ("AUSTRALIAN COMPANIES", AUSTRALIAN_COMPANIES),
        ("HOT COMPANIES 2025", HOT_COMPANIES_2025),
        ("GLOBAL EMPLOYERS", MISSING_GLOBAL_EMPLOYERS)
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
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(download_company_logo, company, domain): company 
                          for company, domain in batch}
                
                for future in as_completed(futures):
                    result = future.result()
                    category_results.append(result)
                    
                    if result['status'] == 'success':
                        success_count += 1
                        print(f"✓ {result['company']:<45} [{result['method']}]")
                    elif result['status'] == 'already_exists':
                        exists_count += 1
                        print(f"◆ {result['company']:<45} [cached]")
                    else:
                        print(f"✗ {result['company']:<45} [failed]")
            
            # Rate limiting
            if i + batch_size < len(company_items):
                time.sleep(1)
        
        # Category summary
        failed_count = len(companies) - success_count - exists_count
        print(f"\n{category_name} Summary:")
        print(f"  New downloads: {success_count}")
        print(f"  Already exist: {exists_count}")
        print(f"  Failed: {failed_count}")
        print(f"  Coverage: {(success_count + exists_count)/len(companies)*100:.1f}%")
        
        all_results.extend(category_results)
    
    # Save results
    with open('logos/employers_2025_results.json', 'w') as f:
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
    
    # Show top failures
    if total_failed > 0:
        failures = [r for r in all_results if r['status'] == 'failed']
        print(f"\n{'='*80}")
        print("TOP FAILURES (showing first 20)")
        print(f"{'='*80}")
        for r in failures[:20]:
            print(f"  • {r['company']} ({r['domain']})")
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")
    
    print(f"\nResults saved to: logos/employers_2025_results.json")
    print(f"Logos saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()