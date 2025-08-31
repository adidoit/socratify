#!/usr/bin/env python3
"""
Check for top business schools, especially US and Canada MBA programs
Focus on M7, T15, T25, and top international programs
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
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa|university|school|college)$', '', normalized)
                if clean_name != normalized and len(clean_name) > 2:
                    existing.add(clean_name)
    
    return existing, existing_names

def get_top_business_schools():
    """Top business schools globally, with emphasis on US and Canada"""
    return {
        "M7_Elite_US": [
            # Magic 7 - The absolute top tier
            "Harvard Business School", "Stanford Graduate School of Business", 
            "Wharton School", "MIT Sloan School of Management", "Northwestern Kellogg",
            "Chicago Booth School of Business", "Columbia Business School"
        ],
        
        "T15_Top_US": [
            # Top 15 US Business Schools
            "Yale School of Management", "UC Berkeley Haas", "Dartmouth Tuck",
            "NYU Stern", "Michigan Ross", "Duke Fuqua", "UCLA Anderson",
            "Cornell Johnson", "Carnegie Mellon Tepper"
        ],
        
        "T25_Strong_US": [
            # Top 25 completion
            "UVA Darden", "Georgetown McDonough", "UT Austin McCombs", "UNC Kenan-Flagler",
            "Washington University Olin", "Vanderbilt Owen", "Rice Jones",
            "Emory Goizueta", "Indiana Kelley", "Georgia Tech Scheller"
        ],
        
        "Regional_Strong_US": [
            # Strong regional programs
            "USC Marshall", "University of Washington Foster", "BYU Marriott",
            "University of Wisconsin Madison", "Ohio State Fisher", "Penn State Smeal",
            "University of Florida Warrington", "Arizona State W.P. Carey",
            "University of Minnesota Carlson", "University of Illinois Gies",
            "Purdue Krannert", "Michigan State Broad", "University of Iowa Tippie",
            "Boston University Questrom", "Boston College Carroll"
        ],
        
        "Canada_Top_MBA": [
            # Top Canadian Business Schools
            "Rotman School of Management", "Ivey Business School", "Sauder School of Business",
            "McGill Desautels", "Queen's Smith School of Business", "Schulich School of Business",
            "HEC Montreal", "Alberta School of Business", "Haskayne School of Business",
            "Sobey School of Business", "Telfer School of Management", "DeGroote School of Business",
            "Beedie School of Business", "Sprott School of Business"
        ],
        
        "European_Elite": [
            # Top European Business Schools
            "INSEAD", "London Business School", "IESE Business School", "IE Business School",
            "HEC Paris", "ESADE Business School", "SDA Bocconi", "IMD Business School",
            "Cambridge Judge", "Oxford Saïd", "Imperial College Business School",
            "Warwick Business School", "Manchester Business School", "City Business School",
            "Rotterdam School of Management", "ESMT Berlin", "Frankfurt School"
        ],
        
        "Asia_Pacific_Top": [
            # Top Asia-Pacific Business Schools
            "China Europe International Business School", "Indian School of Business",
            "Hong Kong University of Science and Technology", "National University of Singapore",
            "Melbourne Business School", "Australian Graduate School of Management",
            "Indian Institutes of Management", "Korea University Business School",
            "Yonsei School of Business", "Tokyo Institute of Technology",
            "Chinese University of Hong Kong", "City University of Hong Kong"
        ],
        
        "Specialized_Programs": [
            # Specialized and Executive Programs
            "Thunderbird School of Global Management", "Babson College",
            "Hult International Business School", "IE University",
            "ESCP Business School", "Grenoble Ecole de Management",
            "EDHEC Business School", "EMLYON Business School",
            "Cranfield School of Management", "Durham Business School"
        ],
        
        "Online_Executive_MBA": [
            # Top Online and Executive MBA Programs
            "Kellogg Executive MBA", "Booth Executive MBA", "Wharton Executive MBA",
            "Columbia Executive MBA", "MIT Sloan Executive MBA", "Stanford Executive MBA",
            "Harvard Business School Executive Education", "London Business School Executive MBA",
            "INSEAD Executive MBA", "IE Executive MBA", "Arizona State Online MBA",
            "Penn State World Campus MBA", "University of Illinois Online MBA"
        ]
    }

def check_business_school_gaps():
    """Check for missing business schools"""
    existing, existing_names = get_existing_companies()
    schools = get_top_business_schools()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Checking top business schools for gaps...")
    print(f"🎓 HUNTING FOR TOP MBA PROGRAMS & BUSINESS SCHOOLS! 🎓")
    print(f"=" * 75)
    
    all_missing = {}
    total_missing_schools = []
    
    for category, school_list in schools.items():
        missing_in_category = []
        found_in_category = []
        
        for school in school_list:
            normalized = normalize_name(school)
            school_lower = school.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(school)
                found = True
            else:
                # Check in original names with school-specific matching
                for exist_name in existing_names:
                    # Extract key terms for schools (university, business school names, etc.)
                    school_terms = [word for word in school_lower.split() 
                                  if len(word) > 2 and word not in ['the', 'of', 'at', 'for', 'and', 'in', 'school', 'business', 'management', 'graduate', 'university', 'college']]
                    
                    if school_terms:
                        # Check if main institution name appears
                        main_term = school_terms[0] if school_terms else school_lower
                        
                        # Special handling for common school abbreviations and names
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms but allow school-specific ones
                            if main_term not in ['mba', 'phd', 'masters', 'program', 'degree', 'online', 'executive']:
                                found_in_category.append(f"{school} (found as: {exist_name})")
                                found = True
                                break
                        
                        # Also check for school nicknames and abbreviations
                        school_mappings = {
                            'wharton': ['wharton', 'upenn', 'pennsylvania'],
                            'kellogg': ['kellogg', 'northwestern'],
                            'booth': ['booth', 'chicago'],
                            'sloan': ['sloan', 'mit'],
                            'haas': ['haas', 'berkeley', 'cal'],
                            'stern': ['stern', 'nyu'],
                            'anderson': ['anderson', 'ucla'],
                            'ross': ['ross', 'michigan'],
                            'tuck': ['tuck', 'dartmouth'],
                            'fuqua': ['fuqua', 'duke'],
                            'johnson': ['johnson', 'cornell'],
                            'tepper': ['tepper', 'carnegie'],
                            'rotman': ['rotman', 'toronto'],
                            'ivey': ['ivey', 'western ontario'],
                            'sauder': ['sauder', 'ubc', 'british columbia'],
                            'desautels': ['desautels', 'mcgill'],
                            'smith': ['smith', 'queens'],
                            'schulich': ['schulich', 'york']
                        }
                        
                        for key, variations in school_mappings.items():
                            if main_term == key:
                                for variation in variations:
                                    if variation in exist_name:
                                        found_in_category.append(f"{school} (found as: {exist_name})")
                                        found = True
                                        break
                                if found:
                                    break
                    
                    if found:
                        break
                    
                    # Also check full substring match for school names
                    if school_lower in exist_name or exist_name in school_lower:
                        if len(school_lower) >= 5:  # Longer match for schools
                            found_in_category.append(f"{school} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 5 and len(exist) > 5:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.7:  # High confidence matching for schools
                                    found_in_category.append(f"{school} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(school)
                total_missing_schools.append((school, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(school_list) * 100 if school_list else 0
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(school_list)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print("🚨 MISSING SCHOOLS:", ', '.join(missing_in_category[:8]) + ("..." if len(missing_in_category) > 8 else ""))
    
    # Summary
    total_missing = len(total_missing_schools)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🎓 TOP BUSINESS SCHOOLS ANALYSIS")
    print(f"Total schools checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Prioritize by business school ranking and importance
    category_priority = {
        'M7_Elite_US': 10,              # Magic 7 - highest priority
        'T15_Top_US': 9,                # Top 15 US schools
        'Canada_Top_MBA': 9,            # Top Canadian schools (user emphasis)
        'T25_Strong_US': 8,             # Top 25 US completion
        'European_Elite': 8,            # Top European programs
        'Regional_Strong_US': 7,        # Strong regional US programs
        'Asia_Pacific_Top': 7,          # Top Asian programs
        'Online_Executive_MBA': 6,      # Executive and online programs
        'Specialized_Programs': 5       # Specialized programs
    }
    
    priority_missing = []
    for school, category in total_missing_schools:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((school, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 100 MISSING BUSINESS SCHOOLS BY PRIORITY:")
    for i, (school, category, score) in enumerate(priority_missing[:100], 1):
        print(f"{i:3d}. {school} ({category.replace('_', ' ')})")
    
    # Show category gaps summary
    print(f"\n📊 BUSINESS SCHOOL GAPS RANKED BY MISSING COUNT:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps:
        print(f"📚 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Save comprehensive business schools analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_business_schools.txt', 'w') as f:
        f.write("TOP BUSINESS SCHOOLS - MISSING PROGRAMS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_checked}\n")
        f.write(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for school in data['missing']:
                    f.write(f"  - {school}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (school, category, score) in enumerate(priority_missing[:150], 1):
            f.write(f"{i:3d}. {school} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved business schools analysis to missing_business_schools.txt")
    print(f"🎓 These are the top MBA programs we're missing!")
    print(f"📚 Focus on M7, T15, and top Canadian schools!")
    
    return priority_missing[:150]  # Return top 150

if __name__ == "__main__":
    check_business_school_gaps()