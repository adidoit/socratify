#!/usr/bin/env python3
"""
Verify master missing list against existing collection
"""

import os
import re
from master_missing_mba_employers import get_master_missing_list

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
                
                # Also add partial matches
                # Remove common suffixes
                clean_name = re.sub(r'(_\d+|_logo|_icon|_favicon)$', '', name.lower())
                existing.add(normalize_name(clean_name))
    
    return existing

def main():
    existing = get_existing_companies()
    missing_list = get_master_missing_list()
    
    print(f"Existing companies: {len(existing)}")
    print(f"Master missing list: {len(missing_list)}")
    
    actually_missing = []
    already_have = []
    
    for company in missing_list:
        normalized = normalize_name(company)
        
        # Check if exists
        found = False
        
        # Exact match
        if normalized in existing:
            already_have.append(f"{company} (exact)")
            found = True
        else:
            # Partial match check
            for exist in existing:
                if normalized in exist or exist in normalized:
                    # Additional checks for common variations
                    if len(normalized) > 3 and len(exist) > 3:
                        already_have.append(f"{company} (partial: {exist})")
                        found = True
                        break
        
        if not found:
            actually_missing.append(company)
    
    print(f"\n=== VERIFICATION RESULTS ===")
    print(f"Actually missing: {len(actually_missing)}")
    print(f"Already have: {len(already_have)}")
    print(f"Coverage: {len(already_have)}/{len(missing_list)} = {(len(already_have)/len(missing_list)*100):.1f}%")
    
    # Save results
    with open('/Users/adi/code/socratify/socratify-yolo/verified_missing_companies.txt', 'w') as f:
        f.write("VERIFIED MISSING COMPANIES FOR DOWNLOAD\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total verified missing: {len(actually_missing)}\n\n")
        
        for i, company in enumerate(actually_missing, 1):
            f.write(f"{i:3d}. {company}\n")
        
        f.write("\n\n=== ALREADY HAVE (NO DOWNLOAD NEEDED) ===\n")
        for company in already_have[:50]:  # Show first 50
            f.write(f"✅ {company}\n")
        if len(already_have) > 50:
            f.write(f"... and {len(already_have) - 50} more\n")
    
    print(f"\nSaved verification results to verified_missing_companies.txt")
    
    return actually_missing

if __name__ == "__main__":
    main()