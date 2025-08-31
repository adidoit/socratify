#!/usr/bin/env python3
"""
Check which top MBA employers we're actually missing
"""

import os
import re
from typing import Set, Dict, List

def normalize_name(name: str) -> str:
    """Normalize company name for comparison"""
    # Convert to lowercase and remove special characters
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)  # Remove all spaces
    return name

def get_existing_companies() -> Set[str]:
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

def check_top_employers():
    """Check which top MBA employers we're missing"""
    
    # Get existing companies
    existing = get_existing_companies()
    print(f"Found {len(existing)} existing company variations\n")
    
    # Top MBA employers to check
    top_employers = {
        "Top Consulting": [
            "McKinsey & Company", "McKinsey", "Boston Consulting Group", "BCG", 
            "Bain & Company", "Bain", "Oliver Wyman", "Strategy&", "Booz Allen Hamilton",
            "Kearney", "A.T. Kearney", "Roland Berger", "LEK Consulting", "L.E.K.",
            "Simon-Kucher", "ZS Associates", "ZS", "Parthenon-EY", "Monitor Deloitte"
        ],
        
        "Big 4 Consulting": [
            "Deloitte", "PwC", "PricewaterhouseCoopers", "EY", "Ernst & Young", 
            "KPMG", "Accenture", "Capgemini", "Cognizant", "Infosys", "TCS", "Wipro"
        ],
        
        "Top Investment Banks": [
            "Goldman Sachs", "Morgan Stanley", "J.P. Morgan", "JPMorgan", "Bank of America",
            "Citigroup", "Citi", "Barclays", "Credit Suisse", "Deutsche Bank", "UBS",
            "Lazard", "Evercore", "Centerview Partners", "Moelis", "Perella Weinreb"
        ],
        
        "Private Equity": [
            "Blackstone", "KKR", "Carlyle Group", "Apollo", "TPG", "Warburg Pincus",
            "Silver Lake", "Vista Equity", "Thoma Bravo", "Francisco Partners",
            "Bain Capital", "Advent International", "CVC Capital", "EQT", "Permira"
        ],
        
        "Big Tech": [
            "Google", "Amazon", "Meta", "Facebook", "Apple", "Microsoft", "Netflix",
            "Salesforce", "Adobe", "Oracle", "IBM", "SAP", "VMware", "ServiceNow",
            "Workday", "Snowflake", "Databricks", "Palantir", "Stripe", "Square"
        ],
        
        "Consumer Goods": [
            "Procter & Gamble", "P&G", "Unilever", "Nestle", "PepsiCo", "Coca-Cola",
            "Diageo", "AB InBev", "L'Oreal", "Estee Lauder", "Nike", "Adidas",
            "LVMH", "Kering", "Hermes", "Richemont"
        ],
        
        "Pharma/Healthcare": [
            "Johnson & Johnson", "J&J", "Pfizer", "Merck", "Novartis", "Roche",
            "AbbVie", "Bristol Myers Squibb", "BMS", "Eli Lilly", "AstraZeneca",
            "GSK", "GlaxoSmithKline", "Sanofi", "Bayer", "Amgen", "Gilead"
        ]
    }
    
    # Check each category
    missing_companies = {}
    found_companies = {}
    
    for category, companies in top_employers.items():
        missing = []
        found = []
        
        for company in companies:
            normalized = normalize_name(company)
            
            # Check if exists
            if normalized in existing:
                found.append(company)
            else:
                # Try partial match
                partial_found = False
                for exist in existing:
                    if normalized in exist or exist in normalized:
                        found.append(f"{company} (partial match)")
                        partial_found = True
                        break
                
                if not partial_found:
                    missing.append(company)
        
        missing_companies[category] = missing
        found_companies[category] = found
        
        print(f"{category}:")
        print(f"  ✅ Found: {len(found)}/{len(companies)}")
        print(f"  ❌ Missing: {len(missing)}/{len(companies)}")
        if missing and len(missing) <= 10:
            print(f"  Missing: {', '.join(missing)}")
        print()
    
    # Count totals
    total_missing = sum(len(m) for m in missing_companies.values())
    total_checked = sum(len(companies) for companies in top_employers.values())
    
    print(f"\nSUMMARY:")
    print(f"Total checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    return missing_companies, found_companies

if __name__ == "__main__":
    missing, found = check_top_employers()
    
    # Save missing companies to file
    with open('/Users/adi/code/socratify/socratify-yolo/actually_missing_employers.txt', 'w') as f:
        f.write("ACTUALLY MISSING TOP MBA EMPLOYERS\n")
        f.write("===================================\n\n")
        
        for category, companies in missing.items():
            if companies:
                f.write(f"## {category}\n")
                for company in companies:
                    f.write(f"{company}\n")
                f.write("\n")
    
    print("\nSaved actually missing companies to actually_missing_employers.txt")