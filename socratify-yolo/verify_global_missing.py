#!/usr/bin/env python3
"""
Verify all global regional companies against existing collection
UK, Canada, EU, China, Africa, Middle East comprehensive check
"""

import os
import re
from uk_companies_database import get_uk_companies
from canadian_companies_database import get_canadian_companies  
from eu_companies_database import get_eu_companies
from chinese_companies_database import get_chinese_companies
from african_companies_database import get_african_companies
from middle_east_companies_database import get_middle_east_companies

def normalize_name(name: str) -> str:
    """Normalize company name for comparison"""
    # Convert to lowercase and remove special characters
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)  # Remove all spaces
    return name

def get_existing_companies() -> set:
    """Get all companies we already have"""
    existing = set()
    base_dirs = [
        '/Users/adi/code/socratify/socratify-images/logos/images/companies',
        '/Users/adi/code/socratify/socratify-images/logos/images/universities', 
        '/Users/adi/code/socratify/socratify-images/logos/images/business_schools'
    ]
    
    for base_dir in base_dirs:
        if os.path.exists(base_dir):
            for file in os.listdir(base_dir):
                if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                    # Remove extension and normalize
                    name = os.path.splitext(file)[0]
                    normalized = normalize_name(name)
                    existing.add(normalized)
                    
                    # Also add partial matches for common variations
                    clean_name = re.sub(r'(_\d+|_logo|_icon|_favicon|_inc|_corp|_corporation|_company|_group|_ltd|_llc|_limited|_holdings|_plc|_ag|_se|_sa)$', '', name.lower())
                    existing.add(normalize_name(clean_name))
    
    return existing

def verify_regional_companies(region_name, companies_dict, existing_companies):
    """Verify companies from a specific region"""
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    actually_missing = []
    already_have = []
    
    for company in unique_companies:
        normalized = normalize_name(company)
        
        # Check if exists
        found = False
        
        # Exact match
        if normalized in existing_companies:
            already_have.append(f"{company} (exact)")
            found = True
        else:
            # Partial match check
            for exist in existing_companies:
                if len(normalized) > 2 and len(exist) > 2:
                    if normalized in exist or exist in normalized:
                        if len(normalized) >= 3 and len(exist) >= 3:
                            match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                            if match_ratio > 0.5:  # At least 50% overlap
                                already_have.append(f"{company} (partial)")
                                found = True
                                break
        
        if not found:
            actually_missing.append(company)
    
    print(f"\n=== {region_name.upper()} VERIFICATION ===")
    print(f"Total companies checked: {len(unique_companies)}")
    print(f"Actually missing: {len(actually_missing)}")
    print(f"Already have: {len(already_have)}")
    print(f"Coverage: {len(already_have)}/{len(unique_companies)} = {(len(already_have)/len(unique_companies)*100):.1f}%")
    
    return actually_missing, already_have, companies_dict

def main():
    existing = get_existing_companies()
    print(f"Existing companies in collection: {len(existing)}")
    
    # Get all regional databases
    regions = {
        "UK": get_uk_companies(),
        "Canada": get_canadian_companies(),
        "EU": get_eu_companies(),
        "China": get_chinese_companies(),
        "Africa": get_african_companies(),
        "Middle East": get_middle_east_companies()
    }
    
    all_missing = {}
    all_stats = {}
    
    # Verify each region
    for region_name, companies_dict in regions.items():
        missing, have, categories = verify_regional_companies(region_name, companies_dict, existing)
        all_missing[region_name] = {
            'missing': missing,
            'have': have,
            'categories': categories
        }
        all_stats[region_name] = {
            'total': len(set([c for cat_list in companies_dict.values() for c in cat_list])),
            'missing': len(missing),
            'coverage': (len(have) / len(set([c for cat_list in companies_dict.values() for c in cat_list]))) * 100
        }
    
    # Save comprehensive results
    with open('/Users/adi/code/socratify/socratify-yolo/global_companies_verified_missing.txt', 'w') as f:
        f.write("GLOBAL COMPANIES - COMPREHENSIVE VERIFICATION\\n")
        f.write("=" * 50 + "\\n\\n")
        
        total_missing = sum(len(region['missing']) for region in all_missing.values())
        f.write(f"TOTAL VERIFIED MISSING ACROSS ALL REGIONS: {total_missing}\\n\\n")
        
        f.write("REGIONAL SUMMARY:\\n")
        f.write("=" * 20 + "\\n")
        for region, stats in all_stats.items():
            f.write(f"{region}: {stats['missing']} missing / {stats['total']} total ({stats['coverage']:.1f}% coverage)\\n")
        
        f.write("\\n" + "=" * 50 + "\\n")
        f.write("DETAILED BREAKDOWN BY REGION:\\n")
        f.write("=" * 35 + "\\n\\n")
        
        for region_name, data in all_missing.items():
            f.write(f"### {region_name.upper()} ###\\n")
            f.write(f"Missing: {len(data['missing'])}\\n")
            f.write(f"Coverage: {((len(data['have']) / (len(data['missing']) + len(data['have']))) * 100):.1f}%\\n\\n")
            
            # Categorize missing by original categories
            missing_by_category = {}
            for category, companies in data['categories'].items():
                missing_in_category = [c for c in companies if c in data['missing']]
                if missing_in_category:
                    missing_by_category[category] = missing_in_category
            
            f.write("Missing by category:\\n")
            for category, missing_companies in missing_by_category.items():
                f.write(f"  {category} ({len(missing_companies)} missing)\\n")
                for company in missing_companies:
                    f.write(f"    - {company}\\n")
            
            f.write("\\nAll missing companies (alphabetical):\\n")
            for i, company in enumerate(sorted(data['missing']), 1):
                f.write(f"{i:3d}. {company}\\n")
            
            f.write("\\n" + "-" * 30 + "\\n\\n")
    
    print(f"\\n=== GLOBAL SUMMARY ===")
    print(f"Total missing across all regions: {total_missing}")
    print(f"\\nTop regions by missing companies:")
    sorted_regions = sorted(all_stats.items(), key=lambda x: x[1]['missing'], reverse=True)
    for region, stats in sorted_regions:
        print(f"{region}: {stats['missing']} missing ({stats['coverage']:.1f}% coverage)")
    
    print(f"\\nSaved comprehensive verification to global_companies_verified_missing.txt")
    
    return all_missing

if __name__ == "__main__":
    main()