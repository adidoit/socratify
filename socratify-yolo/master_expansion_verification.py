#!/usr/bin/env python3
"""
Master Global Expansion Verification System
Check all 496 companies from 7-region research against existing collection
"""

import os
import re
from master_global_expansion_companies import get_master_global_expansion

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

def verify_expansion_companies(existing_companies):
    """Verify all expansion companies against existing collection"""
    master_db = get_master_global_expansion()
    
    all_missing = {}
    all_stats = {}
    
    for region_name, categories in master_db.items():
        # Flatten all companies for this region
        all_companies = []
        for category, company_list in categories.items():
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
        
        print(f"\n=== {region_name.upper()} VERIFICATION ==")
        print(f"Total companies checked: {len(unique_companies)}")
        print(f"Actually missing: {len(actually_missing)}")
        print(f"Already have: {len(already_have)}")
        print(f"Coverage: {len(already_have)}/{len(unique_companies)} = {(len(already_have)/len(unique_companies)*100):.1f}%")
        
        all_missing[region_name] = {
            'missing': actually_missing,
            'have': already_have,
            'categories': categories
        }
        all_stats[region_name] = {
            'total': len(unique_companies),
            'missing': len(actually_missing),
            'coverage': (len(already_have) / len(unique_companies)) * 100
        }
    
    return all_missing, all_stats

def main():
    existing = get_existing_companies()
    print(f"Existing companies in collection: {len(existing)}")
    
    all_missing, all_stats = verify_expansion_companies(existing)
    
    # Save comprehensive results
    with open('/Users/adi/code/socratify/socratify-yolo/master_expansion_verified_missing.txt', 'w') as f:
        f.write("MASTER GLOBAL EXPANSION - COMPREHENSIVE VERIFICATION\\n")
        f.write("=" * 60 + "\\n\\n")
        
        total_missing = sum(len(region['missing']) for region in all_missing.values())
        f.write(f"TOTAL VERIFIED MISSING ACROSS ALL EXPANSION REGIONS: {total_missing}\\n\\n")
        
        f.write("REGIONAL SUMMARY:\\n")
        f.write("=" * 20 + "\\n")
        for region, stats in all_stats.items():
            f.write(f"{region}: {stats['missing']} missing / {stats['total']} total ({stats['coverage']:.1f}% coverage)\\n")
        
        f.write("\\n" + "=" * 60 + "\\n")
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
            
            f.write("\\n" + "-" * 50 + "\\n\\n")
    
    print(f"\n=== MASTER EXPANSION SUMMARY ===")
    print(f"Total missing across all expansion regions: {total_missing}")
    print(f"\nTop regions by missing companies:")
    sorted_regions = sorted(all_stats.items(), key=lambda x: x[1]['missing'], reverse=True)
    for region, stats in sorted_regions:
        print(f"{region}: {stats['missing']} missing ({stats['coverage']:.1f}% coverage)")
    
    print(f"\nSaved comprehensive verification to master_expansion_verified_missing.txt")
    
    # Also create a simple list for downloading
    with open('/Users/adi/code/socratify/socratify-yolo/expansion_companies_to_download.txt', 'w') as f:
        f.write("MASTER EXPANSION COMPANIES TO DOWNLOAD\\n")
        f.write("=" * 45 + "\\n\\n")
        f.write(f"Total companies: {total_missing}\\n\\n")
        
        all_companies_to_download = []
        for region_name, data in all_missing.items():
            for company in data['missing']:
                all_companies_to_download.append((company, region_name))
        
        # Sort alphabetically
        all_companies_to_download.sort(key=lambda x: x[0])
        
        for i, (company, region) in enumerate(all_companies_to_download, 1):
            f.write(f"{i:3d}. {company} ({region})\\n")
    
    print(f"Created download list: expansion_companies_to_download.txt")
    print(f"Ready to download {total_missing} missing companies!")
    
    return all_missing

if __name__ == "__main__":
    main()