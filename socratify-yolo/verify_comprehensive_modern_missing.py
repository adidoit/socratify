#!/usr/bin/env python3
"""
Verify which of the 598 comprehensive modern companies we're missing
"""

import os
import re
from comprehensive_modern_companies_2025 import get_comprehensive_modern_companies

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
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa|ai|labs|systems|tech|technologies)$', '', normalized)
                if clean_name != normalized and len(clean_name) > 2:
                    existing.add(clean_name)
    
    return existing, existing_names

def verify_modern_companies():
    """Verify which modern companies we're missing"""
    existing, existing_names = get_existing_companies()
    companies_dict = get_comprehensive_modern_companies()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Total existing names: {len(existing_names)}")
    
    all_missing = {}
    total_missing_companies = []
    
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
                # Check in original names with better matching
                for exist_name in existing_names:
                    # Split company name into key terms
                    company_terms = [word for word in company_lower.split() 
                                   if len(word) > 2 and word not in ['ai', 'the', 'inc', 'llc', 'ltd', 'labs', 'systems', 'tech']]
                    
                    if company_terms:
                        # Check if main term appears in existing name
                        main_term = company_terms[0] if company_terms else company_lower
                        if main_term in exist_name and len(main_term) >= 3:
                            # Additional verification for common words
                            if main_term not in ['app', 'web', 'data', 'cloud', 'smart', 'digital', 'global']:
                                found_in_category.append(f"{company} (found as: {exist_name})")
                                found = True
                                break
                    
                    # Full substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        if len(company_lower) >= 4:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # Normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 4 and len(exist) > 4:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.75:  # High confidence matching
                                    found_in_category.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(company)
                total_missing_companies.append((company, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(companies) * 100 if companies else 0
        }
        
        print(f"\\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(companies)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\\n🎯 COMPREHENSIVE MODERN COMPANIES SUMMARY")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Create prioritized missing list based on category importance
    priority_missing = []
    category_priorities = {
        'AI_Foundation_Models': 10,
        'AI_Agents_Automation': 10, 
        'AI_Infrastructure_MLOps': 9,
        'Developer_Tools': 9,
        'Fintech_Payments': 8,
        'Healthcare_Biotech': 8,
        'Climate_Tech': 8,
        'Consumer_Social': 7,
        'Enterprise_Software': 7,
        'European_Tech': 6,
        'Israeli_Tech': 6,
        'Indian_Tech': 6,
        'Crypto_Web3': 6,
        'Space_Tech': 5,
        'Quantum_Computing': 5
    }
    
    for company, category in total_missing_companies:
        priority_score = category_priorities.get(category, 4)
        priority_missing.append((company, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\\n🔥 TOP 50 PRIORITY MISSING MODERN COMPANIES:")
    for i, (company, category, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {company} ({category.replace('_', ' ')})")
    
    # Save top priority companies for download
    with open('/Users/adi/code/socratify/socratify-yolo/top_priority_missing_companies.txt', 'w') as f:
        f.write("TOP PRIORITY MISSING MODERN COMPANIES\\n")
        f.write("=" * 45 + "\\n\\n")
        f.write(f"Total missing companies: {total_missing}\\n")
        f.write(f"Showing top 200 by priority\\n\\n")
        
        for i, (company, category, score) in enumerate(priority_missing[:200], 1):
            f.write(f"{i:3d}. {company} ({category.replace('_', ' ')})\\n")
    
    # Also save by category
    with open('/Users/adi/code/socratify/socratify-yolo/missing_companies_by_category.txt', 'w') as f:
        f.write("MISSING MODERN COMPANIES BY CATEGORY\\n")
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
    
    print(f"\\nSaved top 200 priority companies to top_priority_missing_companies.txt")
    print(f"Saved detailed breakdown to missing_companies_by_category.txt")
    
    return priority_missing[:200]  # Return top 200 for download

if __name__ == "__main__":
    verify_modern_companies()