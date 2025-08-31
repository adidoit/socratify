#!/usr/bin/env python3
"""
Check for Fortune 1000 companies that we're missing
Big companies people definitely want to work for
"""

import os
import re

def normalize_name(name: str) -> str:
    """Normalize company name for comparison"""
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)
    return name

def get_existing_companies() -> set:
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
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa)$', '', normalized)
                if clean_name != normalized and len(clean_name) > 2:
                    existing.add(clean_name)
    
    return existing, existing_names

def get_fortune_1000_missing():
    """Major Fortune 1000 companies that are missing"""
    return {
        "Manufacturing_Industrial": [
            # Major Industrial Companies
            "Caterpillar", "Deere & Company", "Parker-Hannifin", "Illinois Tool Works",
            "Emerson Electric", "Eaton", "Danaher", "Honeywell", "3M", "General Dynamics",
            "Lockheed Martin", "Raytheon", "Boeing", "Northrop Grumman", "L3Harris",
            
            # Steel & Materials
            "Nucor", "Steel Dynamics", "Commercial Metals", "Reliance Steel",
            "Alcoa", "Freeport-McMoRan", "Newmont", "Southern Copper",
            
            # Chemical Companies
            "DowDuPont", "LyondellBasell", "PPG Industries", "Sherwin-Williams",
            "Air Products", "Linde", "Praxair", "Eastman Chemical"
        ],
        
        "Energy_Utilities": [
            # Oil & Gas
            "ExxonMobil", "Chevron", "ConocoPhillips", "Phillips 66", "Valero Energy",
            "Marathon Petroleum", "Kinder Morgan", "Enterprise Products", "Plains All American",
            
            # Electric Utilities
            "NextEra Energy", "Duke Energy", "Southern Company", "Dominion Energy",
            "American Electric Power", "Exelon", "Sempra Energy", "Public Service Enterprise",
            "Edison International", "Consolidated Edison", "Entergy", "FirstEnergy"
        ],
        
        "Healthcare_Pharma": [
            # Major Pharma
            "Pfizer", "Johnson & Johnson", "Merck", "AbbVie", "Bristol-Myers Squibb",
            "Amgen", "Gilead Sciences", "Biogen", "Regeneron", "Vertex Pharmaceuticals",
            
            # Medical Devices
            "Medtronic", "Abbott Laboratories", "Danaher", "Thermo Fisher Scientific",
            "Becton Dickinson", "Stryker", "Boston Scientific", "Zimmer Biomet",
            
            # Health Insurance
            "UnitedHealth Group", "Anthem", "Aetna", "Cigna", "Humana"
        ],
        
        "Financial_Investment": [
            # Investment Banking
            "Goldman Sachs", "Morgan Stanley", "JPMorgan Chase", "Bank of America",
            "Citigroup", "Wells Fargo", "Charles Schwab", "BlackRock", "State Street",
            
            # Insurance
            "Berkshire Hathaway", "AIG", "Prudential Financial", "MetLife", "Aflac",
            "Travelers", "Progressive", "Allstate", "Chubb", "Marsh & McLennan",
            
            # Credit Cards & Payments
            "American Express", "Visa", "Mastercard", "PayPal", "Square"
        ],
        
        "Retail_Consumer": [
            # Department Stores
            "Walmart", "Target", "Costco", "Home Depot", "Lowe's", "Macy's",
            "Nordstrom", "Kohl's", "JCPenney", "TJX Companies",
            
            # Specialty Retail
            "Best Buy", "AutoZone", "O'Reilly Automotive", "Advance Auto Parts",
            "GameStop", "Dick's Sporting Goods", "Bed Bath & Beyond",
            
            # E-commerce
            "Amazon", "eBay", "Etsy", "Wayfair", "Overstock.com"
        ],
        
        "Food_Beverage_Consumer": [
            # Food Companies
            "Tyson Foods", "JBS USA", "Cargill", "Archer Daniels Midland", "General Mills",
            "Kellogg", "Campbell Soup", "ConAgra Foods", "Hormel Foods", "Smithfield Foods",
            
            # Beverages
            "Coca-Cola", "PepsiCo", "Monster Beverage", "Dr Pepper Snapple",
            
            # Consumer Products
            "Procter & Gamble", "Unilever", "Colgate-Palmolive", "Kimberly-Clark",
            "Church & Dwight", "Clorox Company"
        ],
        
        "Media_Entertainment": [
            # Media Conglomerates
            "Disney", "Comcast", "AT&T", "Verizon", "Charter Communications",
            "ViacomCBS", "Fox Corporation", "Discovery", "Sony Pictures",
            
            # Publishing & News
            "News Corporation", "New York Times", "Gannett", "Tribune Media"
        ],
        
        "Transportation_Logistics": [
            # Airlines
            "American Airlines", "Delta Air Lines", "United Airlines", "Southwest Airlines",
            "JetBlue", "Alaska Airlines", "Spirit Airlines", "Frontier Airlines",
            
            # Shipping & Logistics
            "FedEx", "UPS", "CH Robinson", "Expeditors International",
            
            # Railroads
            "Union Pacific", "CSX", "Norfolk Southern", "BNSF Railway"
        ],
        
        "Real_Estate_Construction": [
            # Real Estate
            "Simon Property Group", "Boston Properties", "Equity Residential",
            "AvalonBay Communities", "Public Storage", "Welltower",
            
            # Construction
            "Fluor", "Jacobs Engineering", "AECOM", "Quanta Services"
        ],
        
        "Services_Professional": [
            # Consulting
            "McKinsey & Company", "Boston Consulting Group", "Bain & Company",
            "Deloitte", "PwC", "EY", "KPMG", "Accenture",
            
            # Staffing
            "ManpowerGroup", "Robert Half", "Kelly Services"
        ]
    }

def check_fortune_gaps():
    """Check for Fortune 1000 gaps"""
    existing, existing_names = get_existing_companies()
    fortune_companies = get_fortune_1000_missing()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Checking Fortune 1000 companies for gaps...")
    
    all_missing = {}
    total_missing_companies = []
    
    for category, companies in fortune_companies.items():
        missing_in_category = []
        found_in_category = []
        
        for company in companies:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(company)
                found = True
            else:
                # Check in original names
                for exist_name in existing_names:
                    # Split company name into key terms
                    company_terms = [word for word in company_lower.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'llc', 'ltd', 'co', 'corp', 'company']]
                    
                    if company_terms:
                        main_term = company_terms[0]
                        if main_term in exist_name and len(main_term) >= 4:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                    
                    # Also check full substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        if len(company_lower) >= 4:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 4 and len(exist) > 4:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.8:  # High confidence matching
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
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(companies)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print("🚨 MISSING:", ', '.join(missing_in_category[:8]) + ("..." if len(missing_in_category) > 8 else ""))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n💼 FORTUNE 1000 GAPS SUMMARY")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Prioritize by importance
    category_priority = {
        'Financial_Investment': 10,     # High-paying finance jobs
        'Healthcare_Pharma': 9,        # Major pharma companies
        'Services_Professional': 9,     # Consulting firms
        'Retail_Consumer': 8,          # Major retailers
        'Food_Beverage_Consumer': 8,   # CPG companies
        'Energy_Utilities': 7,         # Energy sector
        'Manufacturing_Industrial': 7,  # Industrial companies
        'Media_Entertainment': 6,      # Media companies
        'Transportation_Logistics': 5, # Transport companies
        'Real_Estate_Construction': 4  # Real estate
    }
    
    priority_missing = []
    for company, category in total_missing_companies:
        priority_score = category_priority.get(category, 3)
        priority_missing.append((company, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 50 MISSING FORTUNE 1000 COMPANIES:")
    for i, (company, category, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {company} ({category.replace('_', ' ')})")
    
    # Save all missing Fortune companies
    with open('/Users/adi/code/socratify/socratify-yolo/missing_fortune_1000.txt', 'w') as f:
        f.write("MISSING FORTUNE 1000 COMPANIES\n")
        f.write("=" * 35 + "\n\n")
        f.write(f"Total missing: {total_missing}\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}%\n")
                f.write(f"Missing ({len(data['missing'])}):\n")
                for company in data['missing']:
                    f.write(f"  - {company}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (company, category, score) in enumerate(priority_missing[:100], 1):
            f.write(f"{i:3d}. {company} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved all {total_missing} missing Fortune companies to missing_fortune_1000.txt")
    print(f"🏢 These are major companies people definitely want to work for!")
    
    return priority_missing[:100]  # Return top 100

if __name__ == "__main__":
    check_fortune_gaps()