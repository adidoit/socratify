#!/usr/bin/env python3
"""
Verify master Indian database against existing collection
Check which of the 416 companies we actually don't have
"""

import os
import re
from master_indian_database import get_master_indian_companies

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
                    clean_name = re.sub(r'(_\d+|_logo|_icon|_favicon|_inc|_corp|_corporation|_company|_group|_ltd|_llc|_limited|_india|_technologies)$', '', name.lower())
                    existing.add(normalize_name(clean_name))
    
    return existing

def main():
    existing = get_existing_companies()
    companies_dict = get_master_indian_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"Existing companies in collection: {len(existing)}")
    print(f"Master Indian companies to check: {len(unique_companies)}")
    
    actually_missing = []
    already_have = []
    
    for company in unique_companies:
        normalized = normalize_name(company)
        
        # Check if exists
        found = False
        
        # Exact match
        if normalized in existing:
            already_have.append(f"{company} (exact)")
            found = True
        else:
            # Partial match check - be more lenient for Indian companies
            for exist in existing:
                # Only consider it a match if one contains the other and both are reasonably long
                if len(normalized) > 2 and len(exist) > 2:
                    if normalized in exist or exist in normalized:
                        # Additional validation - must be a substantial match
                        if len(normalized) >= 3 and len(exist) >= 3:
                            match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                            if match_ratio > 0.5:  # At least 50% overlap for Indian companies
                                already_have.append(f"{company} (partial)")
                                found = True
                                break
        
        if not found:
            actually_missing.append(company)
    
    print(f"\n=== MASTER INDIAN COMPANIES VERIFICATION ===")
    print(f"Actually missing: {len(actually_missing)}")
    print(f"Already have: {len(already_have)}")
    print(f"Coverage: {len(already_have)}/{len(unique_companies)} = {(len(already_have)/len(unique_companies)*100):.1f}%")
    
    # Categorize missing companies
    missing_by_category = {}
    for category, companies in companies_dict.items():
        missing_in_category = [c for c in companies if c in actually_missing]
        if missing_in_category:
            missing_by_category[category] = missing_in_category
    
    # Save results
    with open('/Users/adi/code/socratify/socratify-yolo/master_indian_verified_missing.txt', 'w') as f:
        f.write("MASTER INDIAN COMPANIES - VERIFIED MISSING\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Total verified missing: {len(actually_missing)}\n")
        f.write(f"Coverage: {(len(already_have)/len(unique_companies)*100):.1f}% already in collection\n\n")
        
        f.write("MISSING BY CATEGORY:\n")
        f.write("=" * 20 + "\n\n")
        
        for category, missing_companies in missing_by_category.items():
            f.write(f"## {category} ({len(missing_companies)} missing)\n")
            for company in missing_companies:
                f.write(f"- {company}\n")
            f.write("\n")
        
        f.write("\n" + "=" * 45 + "\n")
        f.write("ALL MISSING COMPANIES (ALPHABETICAL):\n")
        f.write("=" * 35 + "\n\n")
        
        for i, company in enumerate(sorted(actually_missing), 1):
            f.write(f"{i:3d}. {company}\n")
        
        f.write(f"\n\n=== SAMPLE ALREADY HAVE ({len(already_have)} companies) ===\n")
        for company in already_have[:50]:  # Show first 50
            f.write(f"✅ {company}\n")
        if len(already_have) > 50:
            f.write(f"... and {len(already_have) - 50} more\n")
    
    print(f"\nSaved verification results to master_indian_verified_missing.txt")
    print(f"\nTop 30 still missing Indian companies:")
    for i, company in enumerate(sorted(actually_missing)[:30], 1):
        print(f"{i:2d}. {company}")
    
    print(f"\nCategories with most missing companies:")
    for category, companies in sorted(missing_by_category.items(), key=lambda x: len(x[1]), reverse=True)[:15]:
        print(f"{category}: {len(companies)} missing")
    
    return actually_missing

if __name__ == "__main__":
    main()