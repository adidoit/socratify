#!/usr/bin/env python3
"""
Verify comprehensive missing list against existing collection
Check which of the 485 companies we actually don't have
"""

import os
import re
from comprehensive_missing_companies import get_comprehensive_missing_list

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
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                # Remove extension and normalize
                name = os.path.splitext(file)[0]
                normalized = normalize_name(name)
                existing.add(normalized)
                
                # Also add partial matches for common variations
                clean_name = re.sub(r'(_\d+|_logo|_icon|_favicon|_inc|_corp|_corporation|_company|_group|_ltd|_llc)$', '', name.lower())
                existing.add(normalize_name(clean_name))
    
    return existing

def main():
    existing = get_existing_companies()
    companies_dict = get_comprehensive_missing_list()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"Existing companies: {len(existing)}")
    print(f"Companies to check: {len(unique_companies)}")
    
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
            # Partial match check - be more strict to avoid false positives
            for exist in existing:
                # Only consider it a match if one contains the other and both are reasonably long
                if len(normalized) > 2 and len(exist) > 2:
                    if normalized in exist or exist in normalized:
                        # Additional validation - must be a substantial match
                        if len(normalized) >= 4 and len(exist) >= 4:
                            match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                            if match_ratio > 0.6:  # At least 60% overlap
                                already_have.append(f"{company} (partial: {exist[:20]}...)")
                                found = True
                                break
        
        if not found:
            actually_missing.append(company)
    
    print(f"\n=== VERIFICATION RESULTS ===")
    print(f"Actually missing: {len(actually_missing)}")
    print(f"Already have: {len(already_have)}")
    print(f"Coverage: {len(already_have)}/{len(unique_companies)} = {(len(already_have)/len(unique_companies)*100):.1f}%")
    
    # Save results
    with open('/Users/adi/code/socratify/socratify-yolo/final_verified_missing.txt', 'w') as f:
        f.write("FINAL VERIFIED MISSING COMPANIES FOR DOWNLOAD\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total verified missing: {len(actually_missing)}\n\n")
        
        for i, company in enumerate(actually_missing, 1):
            f.write(f"{i:3d}. {company}\n")
        
        f.write(f"\n\n=== ALREADY HAVE ({len(already_have)} companies) ===\n")
        for company in already_have[:30]:  # Show first 30
            f.write(f"✅ {company}\n")
        if len(already_have) > 30:
            f.write(f"... and {len(already_have) - 30} more\n")
    
    print(f"\nSaved verification results to final_verified_missing.txt")
    print(f"\nTop 20 actually missing companies:")
    for i, company in enumerate(actually_missing[:20], 1):
        print(f"{i:2d}. {company}")
    
    return actually_missing

if __name__ == "__main__":
    main()