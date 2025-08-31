#!/usr/bin/env python3
"""
Verify which global AI companies we're missing
Chinese, European, Indian, Japanese, Israeli, etc.
"""

import os
import re
from global_ai_companies_comprehensive import get_global_ai_companies

def normalize_name(name: str) -> str:
    """Normalize company name for comparison"""
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)
    return name

def get_existing_companies() -> tuple:
    """Get all companies we currently have"""
    existing = set()
    existing_names = set()
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                # Remove extension
                name = os.path.splitext(file)[0]
                original_name = name.replace('_', ' ')
                existing_names.add(original_name.lower())
                
                # Normalize for matching
                normalized = normalize_name(name)
                existing.add(normalized)
                
                # Also add without common suffixes including AI
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa|ai|labs|systems|tech|technologies|research|lab|academy)$', '', normalized)
                if clean_name != normalized and len(clean_name) > 2:
                    existing.add(clean_name)
    
    return existing, existing_names

def verify_global_ai_companies():
    """Verify which global AI companies we're missing"""
    existing, existing_names = get_existing_companies()
    companies_dict = get_global_ai_companies()
    
    print(f"Total companies in collection: {len(existing)}")
    
    all_missing = {}
    total_missing_companies = []
    
    for region, companies in companies_dict.items():
        missing_in_region = []
        found_in_region = []
        
        for company in companies:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match in normalized names
            if normalized in existing:
                found_in_region.append(company)
                found = True
            else:
                # Check in original names with AI-specific matching
                for exist_name in existing_names:
                    # For AI companies, remove AI suffix for better matching
                    company_without_ai = company_lower.replace(' ai', '').replace(' lab', '').replace(' research', '').strip()
                    exist_without_ai = exist_name.replace(' ai', '').replace(' lab', '').replace(' research', '').strip()
                    
                    # Split company name into key terms
                    company_terms = [word for word in company_without_ai.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'llc', 'ltd', 'labs', 'systems', 'tech', 'technologies']]
                    
                    if company_terms:
                        # Check if main term appears in existing name
                        main_term = company_terms[0] if company_terms else company_without_ai
                        if main_term in exist_without_ai and len(main_term) >= 3:
                            # Additional verification for common words
                            if main_term not in ['app', 'web', 'data', 'cloud', 'smart', 'digital', 'global', 'group', 'company']:
                                found_in_region.append(f"{company} (found as: {exist_name})")
                                found = True
                                break
                    
                    # Also check full substring match
                    if company_without_ai in exist_without_ai or exist_without_ai in company_without_ai:
                        if len(company_without_ai) >= 4:
                            found_in_region.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # Normalized partial matches with AI-specific handling
                if not found:
                    for exist in existing:
                        # Remove AI-related suffixes for comparison
                        normalized_clean = re.sub(r'(ai|lab|research|academy)$', '', normalized).strip()
                        exist_clean = re.sub(r'(ai|lab|research|academy)$', '', exist).strip()
                        
                        if len(normalized_clean) > 4 and len(exist_clean) > 4:
                            if (normalized_clean in exist_clean or exist_clean in normalized_clean):
                                match_ratio = min(len(normalized_clean), len(exist_clean)) / max(len(normalized_clean), len(exist_clean))
                                if match_ratio > 0.75:  # High confidence matching
                                    found_in_region.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_region.append(company)
                total_missing_companies.append((company, region))
        
        all_missing[region] = {
            'missing': missing_in_region,
            'found': found_in_region,
            'coverage': len(found_in_region) / len(companies) * 100 if companies else 0
        }
        
        print(f"\\n=== {region.upper().replace('_', ' ')} ===")
        print(f"Total: {len(companies)} | Found: {len(found_in_region)} ({all_missing[region]['coverage']:.1f}%) | Missing: {len(missing_in_region)}")
        
        if len(missing_in_region) <= 10:  # Show missing if not too many
            print("Missing companies:", ', '.join(missing_in_region[:10]))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\\n🌍 GLOBAL AI COMPANIES SUMMARY")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Create prioritized missing list
    region_priorities = {
        'Chinese_AI': 10,      # Huge market, lots of innovation
        'European_AI': 9,      # Strong ecosystem
        'Indian_AI': 8,        # Booming market
        'Japanese_AI': 8,      # Tech powerhouse
        'Israeli_AI': 7,       # Punch above weight
        'South_Korean_AI': 6,  # Strong in tech
        'Canadian_AI': 5,      # Good ecosystem
        'Scandinavian_AI': 4,  # Innovative but smaller
        'Australian_AI': 3     # Emerging
    }
    
    priority_missing = []
    for company, region in total_missing_companies:
        priority_score = region_priorities.get(region, 3)
        priority_missing.append((company, region, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\\n🔥 TOP 50 MISSING GLOBAL AI COMPANIES:")
    for i, (company, region, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {company} ({region.replace('_', ' ')})")
    
    # Save all missing global AI companies for download
    with open('/Users/adi/code/socratify/socratify-yolo/missing_global_ai_companies.txt', 'w') as f:
        f.write("MISSING GLOBAL AI COMPANIES\\n")
        f.write("=" * 35 + "\\n\\n")
        f.write(f"Total missing: {total_missing}\\n\\n")
        
        for i, (company, region, score) in enumerate(priority_missing, 1):
            f.write(f"{i:3d}. {company} ({region.replace('_', ' ')})\\n")
    
    print(f"\\nSaved all {total_missing} missing global AI companies to missing_global_ai_companies.txt")
    print(f"Ready to download MASSIVE global AI company expansion!")
    
    return priority_missing

if __name__ == "__main__":
    verify_global_ai_companies()