#!/usr/bin/env python3
"""
MASSIVE US & Canada Business Schools Database
Go Go Power Rangers! Find ALL 250+ business schools we're missing!
"""

import os
import re

def normalize_name(name: str) -> str:
    """Normalize school name for comparison"""
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
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa|university|school|college|institute|academy)$', '', normalized)
                if clean_name != normalized and len(clean_name) > 2:
                    existing.add(clean_name)
    
    return existing, existing_names

def get_all_us_canada_business_schools():
    """MASSIVE database of ALL US & Canada business schools - Go Go Power Rangers!"""
    return {
        "US_State_Flagship_Business": [
            # All 50 state flagship universities with business programs
            "University of Alabama Business School", "University of Alaska Business School",
            "Arizona State University W.P. Carey", "University of Arkansas Business School",
            "UC Berkeley Haas", "University of Colorado Boulder Leeds",
            "University of Connecticut Business School", "University of Delaware Business School",
            "University of Florida Warrington", "University of Georgia Terry",
            "University of Hawaii Business School", "University of Idaho Business School",
            "University of Illinois Gies", "Indiana University Kelley",
            "University of Iowa Tippie", "University of Kansas Business School",
            "University of Kentucky Gatton", "Louisiana State University Business School",
            "University of Maine Business School", "University of Maryland Smith",
            "University of Massachusetts Amherst Isenberg", "University of Michigan Ross",
            "University of Minnesota Carlson", "University of Mississippi Business School",
            "University of Missouri Business School", "University of Montana Business School",
            "University of Nebraska Business School", "University of Nevada Las Vegas Business School",
            "University of New Hampshire Business School", "Rutgers Business School",
            "University of New Mexico Business School", "University of North Carolina Kenan-Flagler",
            "University of North Dakota Business School", "Ohio State University Fisher",
            "University of Oklahoma Business School", "University of Oregon Business School",
            "Penn State Smeal", "University of Rhode Island Business School",
            "University of South Carolina Moore", "University of South Dakota Business School",
            "University of Tennessee Business School", "UT Austin McCombs",
            "University of Utah Business School", "University of Vermont Business School",
            "University of Virginia Darden", "University of Washington Foster",
            "West Virginia University Business School", "University of Wisconsin Madison Business School",
            "University of Wyoming Business School"
        ],
        
        "US_Major_Public_Universities": [
            # Major public universities with strong business programs
            "Virginia Tech Pamplin", "NC State Poole", "Penn State Smeal",
            "Florida State University Business School", "Georgia Tech Scheller",
            "University of Pittsburgh Business School", "Michigan State Broad",
            "Ohio University Business School", "University of Cincinnati Business School",
            "University of Kentucky Gatton", "University of Louisville Business School",
            "University of Memphis Business School", "University of Alabama Birmingham Business School",
            "University of Central Florida Business School", "Florida International University Business School",
            "University of South Florida Business School", "University of Houston Bauer",
            "Texas A&M Mays Business School", "Texas Tech Rawls", "University of North Texas Business School",
            "Arizona State University Downtown", "University of Nevada Reno Business School",
            "San Diego State University Business School", "Cal State Long Beach Business School",
            "Cal Poly San Luis Obispo Business School", "University of Oregon Lundquist",
            "Portland State University Business School", "University of Idaho Business School",
            "Boise State University Business School", "Colorado State University Business School",
            "University of Wyoming Business School", "University of New Mexico Anderson"
        ],
        
        "US_Major_Private_Universities": [
            # Major private universities with business schools
            "Northeastern University Business School", "Boston University Questrom",
            "Bentley University Business School", "Babson College", "Suffolk University Business School",
            "Fordham University Gabelli", "Pace University Lubin", "St. John's University Business School",
            "Syracuse University Whitman", "Rochester Institute of Technology Saunders",
            "University of Rochester Simon", "Rensselaer Polytechnic Institute Business School",
            "Drexel University LeBow", "Temple University Fox", "Villanova University Business School",
            "Lehigh University Business School", "Lafayette College Business School",
            "Bucknell University Business School", "American University Kogod",
            "George Washington University Business School", "Georgetown McDonough",
            "Catholic University Business School", "Howard University Business School",
            "Johns Hopkins Carey Business School", "Loyola University Maryland Business School",
            "University of Miami Business School", "Nova Southeastern University Business School",
            "Florida Institute of Technology Business School", "Rollins College Crummer",
            "Stetson University Business School", "Emory University Goizueta",
            "Georgia Southern University Business School", "Mercer University Business School"
        ],
        
        "US_Regional_Strong_Business": [
            # Strong regional business schools
            "Marquette University Business School", "DePaul University Driehaus",
            "Loyola University Chicago Quinlan", "Illinois Institute of Technology Stuart",
            "Bradley University Foster", "Southern Illinois University Business School",
            "Butler University Business School", "Valparaiso University Business School",
            "Ball State University Miller", "Indiana State University Business School",
            "University of Dayton Business School", "Xavier University Williams",
            "Miami University Farmer", "Bowling Green State University Business School",
            "Kent State University Business School", "Cleveland State University Business School",
            "University of Akron Business School", "Youngstown State University Business School",
            "Wright State University Raj Soin", "Capital University Business School",
            "Otterbein University Business School", "Denison University Business School",
            "Kenyon College Business Program", "Oberlin College Business Program",
            "Case Western Reserve Weatherhead", "John Carroll University Boler",
            "Baldwin Wallace University Business School", "University of Toledo Business School",
            "Eastern Michigan University Business School", "Western Michigan University Haworth",
            "Central Michigan University Business School", "Northern Michigan University Business School"
        ],
        
        "US_Specialized_Business_Schools": [
            # Specialized business and MBA programs
            "Thunderbird School of Global Management", "Hult International Business School",
            "Golden Gate University Business School", "University of San Francisco Business School",
            "Santa Clara University Leavey", "Pepperdine Graziadio Business School",
            "Loyola Marymount University Business School", "University of San Diego Business School",
            "Chapman University Argyros", "California Lutheran University Business School",
            "Claremont McKenna College Business School", "Harvey Mudd College Business Program",
            "Pomona College Business Program", "Occidental College Business Program",
            "Whittier College Business School", "University of La Verne Business School",
            "Azusa Pacific University Business School", "Biola University Business School",
            "Point Loma Nazarene University Business School", "University of Redlands Business School",
            "Mills College Business Program", "Dominican University Business School",
            "Saint Mary's College Business School", "Holy Names University Business School"
        ],
        
        "US_Community_College_Business": [
            # Major community colleges with strong business programs
            "Miami Dade College Business School", "Valencia College Business School",
            "Broward College Business School", "Palm Beach State College Business School",
            "Santa Monica College Business School", "Pasadena City College Business School",
            "Los Angeles City College Business School", "Orange Coast College Business School",
            "De Anza College Business School", "Foothill College Business School",
            "Diablo Valley College Business School", "College of Marin Business School",
            "Skyline College Business School", "College of San Mateo Business School",
            "Cañada College Business School", "West Valley College Business School",
            "Mission College Business School", "Evergreen Valley College Business School",
            "San Jose City College Business School", "Gavilan College Business School",
            "Hartnell College Business School", "Monterey Peninsula College Business School",
            "Cabrillo College Business School", "Watsonville College Business School",
            "Northern Virginia Community College Business School", "Montgomery College Business School",
            "Prince George's Community College Business School", "Anne Arundel Community College Business School",
            "Howard Community College Business School", "Carroll Community College Business School"
        ],
        
        "Canada_All_Universities_Business": [
            # ALL Canadian universities with business programs
            "University of Toronto Rotman", "York University Schulich", "Ryerson University Business School",
            "University of Waterloo Business School", "Wilfrid Laurier University Business School",
            "McMaster University DeGroote", "Brock University Goodman", "University of Windsor Business School",
            "Carleton University Sprott", "University of Ottawa Telfer", "Concordia University Business School",
            "McGill University Desautels", "HEC Montreal", "Université de Sherbrooke Business School",
            "Université du Québec à Montréal Business School", "Université Laval Business School",
            "University of New Brunswick Business School", "Dalhousie University Rowe",
            "Saint Mary's University Sobey", "Cape Breton University Business School",
            "Memorial University Business School", "University of Prince Edward Island Business School",
            "University of Manitoba Asper", "University of Winnipeg Business School",
            "University of Saskatchewan Edwards", "University of Regina Business School",
            "University of Calgary Haskayne", "University of Alberta Business School",
            "SAIT Business School", "Mount Royal University Business School",
            "University of British Columbia Sauder", "Simon Fraser University Beedie",
            "University of Victoria Business School", "Thompson Rivers University Business School",
            "University of Northern British Columbia Business School", "Vancouver Island University Business School",
            "Capilano University Business School", "Emily Carr University Business Program",
            "Kwantlen Polytechnic University Business School", "Douglas College Business School"
        ],
        
        "Canada_Colleges_Business": [
            # Canadian colleges and institutes with business programs
            "Seneca College Business School", "Centennial College Business School",
            "George Brown College Business School", "Humber College Business School",
            "Sheridan College Business School", "Algonquin College Business School",
            "La Cité Collégiale Business School", "Canadore College Business School",
            "Georgian College Business School", "Loyalist College Business School",
            "St. Lawrence College Business School", "Mohawk College Business School",
            "Niagara College Business School", "Conestoga College Business School",
            "Fanshawe College Business School", "Lambton College Business School",
            "St. Clair College Business School", "Cambrian College Business School",
            "Confederation College Business School", "Northern College Business School",
            "Sault College Business School", "Boreal College Business School",
            "Red River College Business School", "Assiniboine Community College Business School",
            "Saskatchewan Polytechnic Business School", "SIAST Business School",
            "NAIT Business School", "SAIT Business School", "Bow Valley College Business School",
            "Lethbridge College Business School", "Medicine Hat College Business School",
            "Grande Prairie Regional College Business School", "Keyano College Business School",
            "Lakeland College Business School", "Olds College Business School",
            "Portage College Business School", "BCIT Business School",
            "Camosun College Business School", "College of New Caledonia Business School",
            "College of the Rockies Business School", "Okanagan College Business School",
            "Selkirk College Business School", "Vancouver Community College Business School"
        ],
        
        "US_HBCU_Business_Schools": [
            # Historically Black Colleges and Universities with business programs
            "Howard University Business School", "Spelman College Business Program",
            "Morehouse College Business School", "Clark Atlanta University Business School",
            "Morris Brown College Business School", "Paine College Business School",
            "Albany State University Business School", "Fort Valley State University Business School",
            "Savannah State University Business School", "Florida A&M University Business School",
            "Bethune-Cookman University Business School", "Edward Waters College Business School",
            "Florida Memorial University Business School", "North Carolina A&T Business School",
            "North Carolina Central University Business School", "Bennett College Business Program",
            "Johnson C. Smith University Business School", "Livingstone College Business School",
            "Shaw University Business School", "Winston-Salem State University Business School",
            "South Carolina State University Business School", "Claflin University Business School",
            "Benedict College Business School", "Allen University Business School",
            "Tennessee State University Business School", "Fisk University Business School",
            "Meharry Medical College Business Program", "Lane College Business School",
            "LeMoyne-Owen College Business School", "Knoxville College Business School",
            "Alabama A&M University Business School", "Alabama State University Business School",
            "Miles College Business School", "Oakwood University Business School",
            "Stillman College Business School", "Talladega College Business School",
            "Tuskegee University Business School", "Jackson State University Business School",
            "Alcorn State University Business School", "Mississippi Valley State University Business School",
            "Tougaloo College Business School", "Rust College Business School"
        ]
    }

def check_massive_business_school_gaps():
    """Check for MASSIVE business school gaps - Go Go Power Rangers!"""
    existing, existing_names = get_existing_companies()
    all_schools = get_all_us_canada_business_schools()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"🚀🎓 GO GO POWER RANGERS! MASSIVE BUSINESS SCHOOL HUNT! 🎓🚀")
    print(f"Checking HUNDREDS of US & Canada business schools...")
    print(f"=" * 80)
    
    all_missing = {}
    total_missing_schools = []
    
    for category, school_list in all_schools.items():
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
                # Check in original names with flexible school matching
                for exist_name in existing_names:
                    # Extract key terms for schools
                    school_terms = [word for word in school_lower.split() 
                                  if len(word) > 2 and word not in ['the', 'of', 'at', 'for', 'and', 'in', 'school', 'business', 'management', 'graduate', 'university', 'college', 'institute', 'academy', 'program']]
                    
                    if school_terms:
                        # Check if main institution name appears
                        main_term = school_terms[0] if school_terms else school_lower
                        
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms
                            if main_term not in ['mba', 'phd', 'masters', 'degree', 'online', 'executive', 'state', 'community']:
                                found_in_category.append(f"{school} (found as: {exist_name})")
                                found = True
                                break
                        
                        # Check for common university abbreviations
                        if len(school_terms) >= 2:
                            combo = f"{school_terms[0]} {school_terms[1]}"
                            if combo in exist_name and len(combo) >= 6:
                                found_in_category.append(f"{school} (found as: {exist_name})")
                                found = True
                                break
                    
                    if found:
                        break
                    
                    # Also check full substring match for school names
                    if school_lower in exist_name or exist_name in school_lower:
                        if len(school_lower) >= 8:  # Longer match for schools
                            found_in_category.append(f"{school} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 6 and len(exist) > 6:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.6:  # Lower threshold for more schools
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
            print("🚨 MISSING SCHOOLS:", ', '.join(missing_in_category[:10]) + ("..." if len(missing_in_category) > 10 else ""))
    
    # Summary
    total_missing = len(total_missing_schools)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🚀🎓 MASSIVE BUSINESS SCHOOL ANALYSIS - POWER RANGERS STYLE! 🎓🚀")
    print(f"Total schools checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Prioritize by category importance
    category_priority = {
        'US_State_Flagship_Business': 10,        # State flagships - high priority
        'Canada_All_Universities_Business': 10,  # All Canadian universities - user emphasis
        'US_Major_Private_Universities': 9,      # Major private universities
        'US_Major_Public_Universities': 9,       # Major public universities
        'Canada_Colleges_Business': 8,           # Canadian colleges
        'US_Regional_Strong_Business': 8,        # Strong regional programs
        'US_Specialized_Business_Schools': 7,    # Specialized programs
        'US_HBCU_Business_Schools': 7,          # HBCUs - important for diversity
        'US_Community_College_Business': 6       # Community colleges
    }
    
    priority_missing = []
    for school, category in total_missing_schools:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((school, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 200 MISSING BUSINESS SCHOOLS BY PRIORITY:")
    for i, (school, category, score) in enumerate(priority_missing[:200], 1):
        print(f"{i:3d}. {school} ({category.replace('_', ' ')})")
    
    # Show category gaps summary
    print(f"\n📊 MASSIVE BUSINESS SCHOOL GAPS RANKED BY MISSING COUNT:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps:
        print(f"📚 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Save MASSIVE business schools analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_massive_business_schools.txt', 'w') as f:
        f.write("MASSIVE US & CANADA BUSINESS SCHOOLS - MISSING PROGRAMS\n")
        f.write("GO GO POWER RANGERS STYLE!\n")
        f.write("=" * 70 + "\n\n")
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
        for i, (school, category, score) in enumerate(priority_missing[:300], 1):
            f.write(f"{i:3d}. {school} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved MASSIVE business schools analysis to missing_massive_business_schools.txt")
    print(f"🚀 GO GO POWER RANGERS! These are HUNDREDS of business schools we're missing!")
    print(f"🎓 From state flagships to community colleges to Canadian universities!")
    
    if total_missing >= 250:
        print(f"\n💥 POWER RANGERS SUCCESS! Found {total_missing} missing business schools!")
        print(f"🔥 Time to download them all and dominate the education sector!")
    
    return priority_missing[:300]  # Return top 300

if __name__ == "__main__":
    check_massive_business_school_gaps()