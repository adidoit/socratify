#!/usr/bin/env python3
"""
Final expansion download - 659 additional companies
Making this the most comprehensive collection possible
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from final_expansion_companies import get_all_final_expansion_companies
from final_expansion_companies import (
    EASTERN_EUROPE_COMPANIES, NORDIC_COMPANIES, DEFENSE_AEROSPACE_COMPANIES,
    SEMICONDUCTOR_HARDWARE_COMPANIES, LOGISTICS_SUPPLY_CHAIN_COMPANIES,
    INSURANCE_COMPANIES, EMERGING_TECH_COMPANIES, REGIONAL_CHAMPIONS,
    ALTERNATIVE_INVESTMENTS, CREATOR_ECONOMY_B2B, IMPACT_ESG_COMPANIES,
    CRYPTO_WEB3_COMPANIES
)

# Create output directory
OUTPUT_DIR = 'logos/final_expansion'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check existing logos
existing_logos = set()
check_dirs = [
    'logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos',
    'logos/business_school_logos', 'logos/comprehensive_fix', 
    'logos/expanded_business_schools', 'logos/employers_2025',
    'logos/comprehensive_global', 'logos/final_expansion'
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

def company_already_exists(company_name):
    """Check if we already have this company"""
    # Quick checks
    name_clean = company_name.lower().replace(' ', '').replace('&', '').replace('.', '').replace('-', '').replace("'", "")
    
    if name_clean in existing_logos:
        return True
    
    # Check key parts
    parts = company_name.lower().split()
    for part in parts:
        if len(part) > 4 and part in existing_logos:
            # Special cases where part match is not enough
            if part in ['bank', 'group', 'capital', 'digital', 'global', 'international']:
                continue
            return True
    
    # Known mappings
    known_mappings = {
        "H&M": "hm",
        "IKEA": "ikea", 
        "LEGO": "lego",
        "Maersk": "maersk",
        "DHL": "dhl",
        "FedEx": "fedex",
        "UPS": "ups",
        "Boeing": "boeing",
        "Airbus": "airbus",
        "TSMC": "tsmc",
        "ASML": "asml"
    }
    
    if company_name in known_mappings and known_mappings[company_name] in existing_logos:
        return True
    
    return False

def download_company_logo(company_name, domain):
    """Download logo for a company"""
    # Check existence
    if company_already_exists(company_name):
        return {
            'company': company_name,
            'status': 'already_exists',
            'domain': domain
        }
    
    # Clean filename
    filename_base = company_name.replace(' ', '_').replace('/', '_').replace(':', '').replace('&', 'and').replace("'", "").replace('.', '')
    
    # Strategies
    strategies = []
    
    # Direct domain
    strategies.append({'url': f"https://logo.clearbit.com/{domain}", 'name': 'clearbit_direct'})
    
    # Remove subdomain
    if domain.count('.') > 1:
        parent = '.'.join(domain.split('.')[-2:])
        strategies.append({'url': f"https://logo.clearbit.com/{parent}", 'name': 'clearbit_parent'})
    
    # For .gov/.org try .com
    if domain.endswith(('.gov', '.org', '.mil', '.edu')):
        base = domain.split('.')[0]
        strategies.append({'url': f"https://logo.clearbit.com/{base}.com", 'name': 'clearbit_com'})
    
    # Special cases
    special_domains = {
        "Novo Nordisk": "novonordisk.com",
        "H&M": "hm.com",
        "LEGO": "lego.com",
        "Maersk": "maersk.com",
        "Ørsted": "orsted.com",
        "IKEA": "ikea.com",
        "DHL": "dhl.com",
        "FedEx": "fedex.com",
        "UPS": "ups.com"
    }
    
    if company_name in special_domains:
        strategies.insert(0, {'url': f"https://logo.clearbit.com/{special_domains[company_name]}", 'name': 'clearbit_special'})
    
    # Logo.dev
    strategies.append({'url': f"https://img.logo.dev/{domain}?token=pk_X-1ZO13GSgeOoUrIuCGGfw", 'name': 'logodev'})
    
    # Try simplified name
    simple_name = company_name.split()[0].lower() if ' ' in company_name else company_name.lower()
    strategies.append({'url': f"https://logo.clearbit.com/{simple_name}.com", 'name': 'clearbit_simple'})
    
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
    all_companies = get_all_final_expansion_companies()
    
    print("=" * 80)
    print("FINAL EXPANSION DOWNLOAD - MAKING IT COMPREHENSIVE")
    print("=" * 80)
    print(f"Total new organizations: {len(all_companies)}")
    print()
    
    # Categories
    categories = [
        ("EASTERN EUROPE", EASTERN_EUROPE_COMPANIES),
        ("NORDIC", NORDIC_COMPANIES),
        ("DEFENSE & AEROSPACE", DEFENSE_AEROSPACE_COMPANIES),
        ("SEMICONDUCTORS", SEMICONDUCTOR_HARDWARE_COMPANIES),
        ("LOGISTICS", LOGISTICS_SUPPLY_CHAIN_COMPANIES),
        ("INSURANCE", INSURANCE_COMPANIES),
        ("EMERGING TECH", EMERGING_TECH_COMPANIES),
        ("REGIONAL CHAMPIONS", REGIONAL_CHAMPIONS),
        ("ALT INVESTMENTS", ALTERNATIVE_INVESTMENTS),
        ("CREATOR/B2B", CREATOR_ECONOMY_B2B),
        ("IMPACT/ESG", IMPACT_ESG_COMPANIES),
        ("CRYPTO/WEB3", CRYPTO_WEB3_COMPANIES)
    ]
    
    all_results = []
    
    for category_name, companies in categories:
        print(f"\n{'='*60}")
        print(f"{category_name} ({len(companies)} companies)")
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
                        print(f"✓ {result['company']:<35} [{result['method']}]")
                    elif result['status'] == 'already_exists':
                        exists_count += 1
                        print(f"◆ {result['company']:<35} [cached]")
                    else:
                        print(f"✗ {result['company']:<35} [failed]")
            
            # Rate limiting
            if i + batch_size < len(company_items):
                time.sleep(1)
        
        # Summary
        failed_count = len(companies) - success_count - exists_count
        print(f"\n{category_name} Summary:")
        print(f"  New: {success_count}, Exists: {exists_count}, Failed: {failed_count}")
        print(f"  Coverage: {(success_count + exists_count)/len(companies)*100:.1f}%")
        
        all_results.extend(category_results)
        
        # Save progress
        with open('logos/final_expansion_results.json', 'w') as f:
            json.dump(all_results, f, indent=2)
    
    # Final summary
    print("\n" + "=" * 80)
    print("FINAL EXPANSION COMPLETE")
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
        for r in failures[:15]:
            print(f"  • {r['company']} ({r['domain']})")
        if len(failures) > 15:
            print(f"  ... and {len(failures) - 15} more")
    
    print(f"\nResults: logos/final_expansion_results.json")
    print(f"Logos: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()