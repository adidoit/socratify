#!/usr/bin/env python3
"""
Check for missing companies across major categories
Based on analysis of potential gaps in our 8,220+ company collection
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

def get_major_missing_categories():
    """Major company categories that might have gaps"""
    return {
        "Internet_Platforms_Social": [
            # High probability missing after Quora gap
            "Reddit", "Discord", "Twitch", "Pinterest", "Snapchat", "Signal", "Telegram",
            "TikTok", "ByteDance", "WeChat", "Line", "KakaoTalk", "WhatsApp", "Viber"
        ],
        
        "Professional_Productivity_Tools": [
            # Major workplace/productivity platforms
            "Slack Technologies", "Notion", "Zoom Video Communications", "Dropbox",
            "Box Inc", "Atlassian", "GitHub", "GitLab", "Stack Overflow", "Figma",
            "Canva", "Miro", "Monday.com", "Asana", "Trello", "DocuSign"
        ],
        
        "Major_Airlines_Transportation": [
            # Top global airlines - often overlooked but major employers
            "Delta Air Lines", "American Airlines", "United Airlines", "Southwest Airlines",
            "JetBlue Airways", "Alaska Airlines", "Emirates", "Lufthansa", "British Airways",
            "Singapore Airlines", "Air France", "KLM", "Qatar Airways", "Cathay Pacific",
            "FedEx", "UPS", "DHL", "Uber", "Lyft", "Didi Chuxing", "Grab", "Gojek"
        ],
        
        "Insurance_Giants": [
            # Major insurers - huge employers often forgotten
            "State Farm", "Geico", "Progressive", "Allstate", "USAA", "Liberty Mutual",
            "Travelers", "Farmers Insurance", "Nationwide", "AIG", "Prudential Financial",
            "MetLife", "Aon", "Marsh McLennan", "Willis Towers Watson", "Zurich Insurance"
        ],
        
        "Telecommunications": [
            # Major telcos globally
            "Verizon", "AT&T", "T-Mobile US", "Comcast", "Charter Communications",
            "Vodafone", "Orange", "Deutsche Telekom", "BT Group", "Telefonica",
            "China Mobile", "China Telecom", "China Unicom", "NTT", "SoftBank Corp"
        ],
        
        "Energy_Oil_Gas": [
            # Energy giants - major employers
            "ExxonMobil", "Chevron", "Shell", "BP", "TotalEnergies", "ConocoPhillips",
            "Schlumberger", "Halliburton", "Baker Hughes", "Kinder Morgan",
            "Enbridge", "TC Energy", "Suncor Energy", "Imperial Oil", "Equinor"
        ],
        
        "Hospitality_Travel": [
            # Hotel chains and travel
            "Marriott International", "Hilton Worldwide", "Hyatt Hotels", "IHG",
            "Wyndham Hotels", "Choice Hotels", "Airbnb", "Booking.com", "Expedia Group",
            "TripAdvisor", "Priceline", "Kayak", "Trivago", "Hotels.com"
        ],
        
        "Utilities_Power": [
            # Major utility companies
            "Duke Energy", "NextEra Energy", "Dominion Energy", "Exelon",
            "American Electric Power", "Southern Company", "PG&E", "Con Edison",
            "Sempra Energy", "Xcel Energy", "Eversource Energy", "Public Service Enterprise"
        ],
        
        "Defense_Government_Contractors": [
            # Defense and government contractors
            "Lockheed Martin", "Raytheon Technologies", "General Dynamics", "Northrop Grumman",
            "Boeing Defense", "L3Harris Technologies", "Huntington Ingalls", "Palantir Technologies",
            "Booz Allen Hamilton", "CACI", "SAIC", "Leidos", "BAE Systems", "Airbus Defence"
        ],
        
        "Real_Estate": [
            # Major real estate companies
            "CBRE Group", "Cushman Wakefield", "JLL", "Colliers International",
            "Marcus Millichap", "Redfin", "Zillow Group", "Compass", "Realogy",
            "RE/MAX", "Coldwell Banker", "Century 21", "Keller Williams"
        ],
        
        "Media_Publishing": [
            # Major media companies
            "The New York Times", "Wall Street Journal", "Washington Post", "USA Today",
            "Bloomberg LP", "Thomson Reuters", "Dow Jones", "Financial Times",
            "The Guardian", "BBC", "CNN", "Fox News", "MSNBC", "Condé Nast"
        ],
        
        "Fashion_Luxury_Retail": [
            # Fashion and luxury brands
            "LVMH", "Kering", "Chanel", "Hermès", "Prada", "Burberry", "Gucci",
            "Louis Vuitton", "Coach", "Michael Kors", "Ralph Lauren", "Calvin Klein",
            "Tommy Hilfiger", "Hugo Boss", "Armani", "Versace", "Balenciaga"
        ],
        
        "Gaming_Entertainment_Extended": [
            # Gaming companies that might be missing
            "Epic Games", "Roblox Corporation", "Unity Technologies", "Riot Games",
            "Blizzard Entertainment", "Electronic Arts", "Take-Two Interactive", "Ubisoft",
            "Activision", "Nintendo", "Sony Interactive", "Valve Corporation", "Steam"
        ]
    }

def check_missing_categories():
    """Check what major companies are missing by category"""
    existing, existing_names = get_existing_companies()
    categories = get_major_missing_categories()
    
    print(f"Current collection size: {len(existing)} companies")
    print(f"🔍 CHECKING FOR MISSING MAJOR COMPANY CATEGORIES 🔍")
    print(f"Based on analysis of potential gaps...")
    print(f"=" * 80)
    
    all_missing = {}
    total_missing_companies = []
    
    for category, company_list in categories.items():
        missing_in_category = []
        found_in_category = []
        
        for company in company_list:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(company)
                found = True
            else:
                # Check in original names with flexible matching
                for exist_name in existing_names:
                    # Extract key terms
                    company_terms = [word for word in company_lower.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'corp', 'ltd', 'llc', 'group', 'company']]
                    
                    if company_terms:
                        # Check if main company name appears
                        main_term = company_terms[0] if company_terms else company_lower
                        
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms
                            if main_term not in ['air', 'new', 'big', 'one', 'pro', 'max', 'red', 'blue']:
                                found_in_category.append(f"{company} (found as: {exist_name})")
                                found = True
                                break
                        
                        # Check for brand combinations
                        if len(company_terms) >= 2:
                            combo = f"{company_terms[0]} {company_terms[1]}"
                            if combo in exist_name and len(combo) >= 6:
                                found_in_category.append(f"{company} (found as: {exist_name})")
                                found = True
                                break
                    
                    if found:
                        break
                    
                    # Also check full substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        if len(company_lower) >= 6:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # Partial matches for longer names
                if not found:
                    for exist in existing:
                        if len(normalized) > 4 and len(exist) > 4:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.7:
                                    found_in_category.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(company)
                total_missing_companies.append((company, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(company_list) * 100 if company_list else 0
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(company_list)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print(f"🚨 MISSING: {', '.join(missing_in_category[:8])}" + ("..." if len(missing_in_category) > 8 else ""))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🔍 MAJOR CATEGORIES ANALYSIS COMPLETE!")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Show biggest gaps
    print(f"\n📊 BIGGEST GAPS BY MISSING COUNT:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps[:10]:
        print(f"🔥 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Priority missing companies
    print(f"\n🎯 TOP 50 MISSING COMPANIES (Highest Priority):")
    
    # Prioritize by category importance
    category_priority = {
        'Internet_Platforms_Social': 10,
        'Professional_Productivity_Tools': 9,
        'Major_Airlines_Transportation': 9,
        'Insurance_Giants': 8,
        'Telecommunications': 8,
        'Energy_Oil_Gas': 8,
        'Hospitality_Travel': 7,
        'Defense_Government_Contractors': 7,
        'Real_Estate': 6,
        'Media_Publishing': 6,
        'Fashion_Luxury_Retail': 6,
        'Gaming_Entertainment_Extended': 5,
        'Utilities_Power': 5
    }
    
    priority_missing = []
    for company, category in total_missing_companies:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((company, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    for i, (company, category, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {company} ({category.replace('_', ' ')})")
    
    # Save analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_major_categories.txt', 'w') as f:
        f.write("MISSING MAJOR COMPANY CATEGORIES ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_checked}\n")
        f.write(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for company in data['missing']:
                    f.write(f"  - {company}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (company, category, score) in enumerate(priority_missing[:100], 1):
            f.write(f"{i:3d}. {company} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved analysis to missing_major_categories.txt")
    print(f"🚀 Ready to download missing companies and fill major gaps!")
    
    return priority_missing[:100]

if __name__ == "__main__":
    check_missing_categories()