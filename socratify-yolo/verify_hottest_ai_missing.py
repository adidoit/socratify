#!/usr/bin/env python3
"""
Verify which of the hottest 2025 AI companies we're missing
"""

import os
import re
from hottest_2025_ai_companies import get_hottest_2025_ai_companies

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
                
                # Also add without common suffixes
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa|ai|labs|systems)$', '', normalized)
                if clean_name != normalized:
                    existing.add(clean_name)
    
    return existing, existing_names

def verify_ai_companies():
    """Verify which hottest AI companies we're missing"""
    existing, existing_names = get_existing_companies()
    companies_dict = get_hottest_2025_ai_companies()
    
    print(f"Total companies in collection: {len(existing)}")
    
    all_missing = {}
    
    for category, companies in companies_dict.items():
        missing_in_category = []
        found_in_category = []
        
        for company in companies:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match in normalized names
            if normalized in existing:
                found_in_category.append(company)
                found = True
            else:
                # Check in original names
                for exist_name in existing_names:
                    # For AI companies, check key terms
                    company_key_terms = [word for word in company_lower.split() if len(word) > 2 and word not in ['ai', 'the', 'inc', 'llc']]
                    
                    if company_key_terms:
                        main_term = company_key_terms[0]  # Use first significant word
                        if main_term in exist_name and len(main_term) >= 3:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                    
                    # Also check full substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        if len(company_lower) >= 3:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 3 and len(exist) > 3:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.7:  # Stricter matching for AI companies
                                    found_in_category.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(company)
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(companies) * 100
        }
        
        print(f"\\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total companies checked: {len(companies)}")
        print(f"Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%)")
        print(f"Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print("🔥 MISSING HOT AI COMPANIES:")
            for company in missing_in_category:
                print(f"  - {company}")
    
    # Summary
    total_missing = sum(len(data['missing']) for data in all_missing.values())
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\\n=== 🔥 HOTTEST AI COMPANIES SUMMARY ===")
    print(f"Total AI companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Create prioritized missing list
    priority_missing = []
    for category, data in all_missing.items():
        for company in data['missing']:
            # Prioritize based on category importance
            priority_score = 0
            if 'Foundation_Models' in category or 'AI_Agents' in category:
                priority_score = 10  # Highest priority
            elif 'Hot_AI_Startups' in category or 'Computer_Vision' in category:
                priority_score = 8
            elif 'Vertical_AI' in category or 'Research_Labs' in category:
                priority_score = 6
            else:
                priority_score = 4
            
            priority_missing.append((company, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\\n=== 🎯 TOP PRIORITY MISSING AI COMPANIES ===")
    for i, (company, category, score) in enumerate(priority_missing[:20], 1):
        print(f"{i:2d}. {company} ({category.replace('_', ' ')})")
    
    # Save results
    with open('/Users/adi/code/socratify/socratify-yolo/missing_hottest_ai_companies.txt', 'w') as f:
        f.write("MISSING HOTTEST 2025 AI COMPANIES\\n")
        f.write("=" * 40 + "\\n\\n")
        f.write(f"Total missing: {total_missing}\\n\\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.upper().replace('_', ' ')} ###\\n")
                f.write(f"Coverage: {data['coverage']:.1f}%\\n")
                f.write(f"Missing ({len(data['missing'])}):\\n")
                for company in data['missing']:
                    f.write(f"  - {company}\\n")
                f.write("\\n")
        
        f.write("\\n### TOP PRIORITY MISSING (Top 20) ###\\n")
        for i, (company, category, score) in enumerate(priority_missing[:20], 1):
            f.write(f"{i:2d}. {company} ({category.replace('_', ' ')})\\n")
    
    print(f"\\nSaved detailed results to missing_hottest_ai_companies.txt")
    return priority_missing

if __name__ == "__main__":
    verify_ai_companies()