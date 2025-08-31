#!/usr/bin/env python3
"""
Analyze what's missing from a GLOBAL JOB SEEKER perspective
Focus on companies/organizations people actually want to work for worldwide
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

def get_global_job_seeker_missing_categories():
    """Categories job seekers globally need but might be missing"""
    return {
        "Major_Government_Employers": [
            # Government agencies and public sector jobs
            "US Department of Defense", "US State Department", "CIA", "FBI", "NSA",
            "UK Civil Service", "UK Ministry of Defence", "GCHQ", "MI5", "MI6",
            "European Commission", "European Parliament", "NATO", "OECD", "World Bank",
            "International Monetary Fund", "United Nations", "WHO", "UNESCO", "UNICEF",
            "Canada Public Service", "Australian Public Service", "Singapore Civil Service"
        ],
        
        "Top_Universities_Employers": [
            # Universities are major employers globally
            "Harvard University", "Stanford University", "MIT", "Yale University", "Princeton University",
            "Oxford University", "Cambridge University", "Imperial College London", "UCL", "King's College London",
            "University of Toronto", "McGill University", "University of British Columbia",
            "ETH Zurich", "TU Munich", "University of Tokyo", "Kyoto University", "NUS", "NTU Singapore",
            "Peking University", "Tsinghua University", "University of Melbourne", "Australian National University"
        ],
        
        "Major_Hospitals_Healthcare": [
            # Healthcare is massive employer category
            "Mayo Clinic", "Cleveland Clinic", "Johns Hopkins Hospital", "Massachusetts General Hospital",
            "Kaiser Permanente", "HCA Healthcare", "Tenet Healthcare", "Community Health Systems",
            "NHS England", "NHS Scotland", "Charité Berlin", "Assistance Publique Paris",
            "Toronto General Hospital", "Vancouver General Hospital", "Singapore General Hospital",
            "All India Institute of Medical Sciences", "Apollo Hospitals", "Fortis Healthcare"
        ],
        
        "Major_Law_Firms": [
            # Legal services - high-paying careers
            "Baker McKenzie", "Clifford Chance", "Allen & Overy", "Linklaters", "Freshfields",
            "Skadden Arps", "Kirkland & Ellis", "Latham & Watkins", "Sullivan & Cromwell",
            "Wachtell Lipton", "Cravath Swaine", "Simpson Thacher", "Davis Polk", "White & Case"
        ],
        
        "Top_Consulting_Extended": [
            # More consulting firms beyond MBB
            "Accenture", "Deloitte Consulting", "EY Advisory", "KPMG Advisory", "PwC Consulting",
            "IBM Consulting", "Capgemini", "Tata Consultancy Services", "Infosys", "Wipro",
            "Oliver Wyman", "Roland Berger", "AT Kearney", "Strategy&", "L.E.K. Consulting"
        ],
        
        "Major_NGOs_Nonprofits": [
            # Nonprofits are major employers for mission-driven job seekers
            "Red Cross", "Doctors Without Borders", "Oxfam", "Save the Children", "CARE",
            "World Wildlife Fund", "Greenpeace", "Amnesty International", "Human Rights Watch",
            "Teach for America", "Peace Corps", "AmeriCorps", "United Way", "Salvation Army"
        ],
        
        "Regional_Conglomerates_Missing": [
            # Major conglomerates job seekers want to work for
            "Berkshire Hathaway", "General Electric", "3M", "Honeywell", "Caterpillar",
            "Samsung Group", "LG Group", "Hyundai Group", "SK Group", "Lotte Group",
            "Mitsubishi Group", "Mitsui Group", "Sumitomo Group", "Softbank Group",
            "Tata Group", "Reliance Industries", "Aditya Birla Group", "Mahindra Group"
        ],
        
        "Major_Retail_Employers": [
            # Retail is one of the largest employment sectors
            "Walmart", "Amazon", "Costco", "Home Depot", "Target", "Lowe's", "Best Buy",
            "Kroger", "Publix", "H-E-B", "Meijer", "Wegmans", "Whole Foods",
            "IKEA", "H&M", "Zara", "Uniqlo", "Marks & Spencer", "John Lewis"
        ],
        
        "Transportation_Logistics_Major": [
            # Major employers in transportation
            "UPS", "FedEx", "DHL", "USPS", "Canada Post", "Royal Mail",
            "Union Pacific", "BNSF Railway", "Canadian National Railway", "Deutsche Bahn",
            "JR East", "JR Central", "Singapore Airlines", "Cathay Pacific", "Qantas"
        ],
        
        "Energy_Utilities_Extended": [
            # Energy sector major employers
            "Saudi Aramco", "Gazprom", "China National Petroleum", "Sinopec", "CNPC",
            "Petrobras", "Equinor", "Eni", "Repsol", "Total Energies", "Schlumberger",
            "National Grid", "E.ON", "RWE", "Iberdrola", "Enel", "Engie"
        ],
        
        "Major_Banks_Extended": [
            # More banks beyond what we have
            "State Bank of India", "ICICI Bank", "HDFC Bank", "Kotak Mahindra Bank",
            "DBS Bank", "OCBC Bank", "UOB", "Bangkok Bank", "Kasikornbank",
            "Bank of China", "Agricultural Bank of China", "Ping An Bank", "China Merchants Bank",
            "Sumitomo Mitsui Banking", "Mizuho Bank", "Bank of Tokyo-Mitsubishi"
        ],
        
        "Telecommunications_Extended": [
            # More telecom companies globally
            "Reliance Jio", "Bharti Airtel", "Singtel", "Telstra", "Optus",
            "Rogers Communications", "Bell Canada", "Telus", "SK Telecom", "KT Corporation",
            "NTT DoCoMo", "Rakuten Mobile", "China Mobile", "China Unicom", "China Telecom"
        ],
        
        "Food_Beverage_Giants": [
            # F&B is major employer category
            "Nestle", "PepsiCo", "Coca-Cola", "Unilever", "Procter & Gamble",
            "Mars Inc", "Mondelez", "General Mills", "Kellogg's", "Kraft Heinz",
            "Tyson Foods", "JBS", "Cargill", "Archer Daniels Midland",
            "McDonald's", "Starbucks", "Yum! Brands", "Restaurant Brands International"
        ],
        
        "Pharmaceutical_Biotech_Extended": [
            # More pharma companies
            "Roche", "Novartis", "Sanofi", "GlaxoSmithKline", "AstraZeneca", "Merck KGaA",
            "Takeda", "Astellas", "Daiichi Sankyo", "Eisai", "Sumitomo Dainippon",
            "Sun Pharma", "Dr. Reddy's", "Cipla", "Lupin", "Aurobindo Pharma"
        ],
        
        "Manufacturing_Industrial_Giants": [
            # Major industrial employers
            "Siemens", "ABB", "Schneider Electric", "Emerson", "Rockwell Automation",
            "Mitsubishi Heavy Industries", "Kawasaki Heavy Industries", "IHI Corporation",
            "Doosan", "Hyundai Heavy Industries", "POSCO", "Nucor", "ArcelorMittal"
        ],
        
        "Aerospace_Defense_Extended": [
            # More aerospace companies
            "Airbus", "Boeing", "Bombardier", "Embraer", "Rolls-Royce", "Safran",
            "Leonardo", "Thales", "BAE Systems", "General Dynamics", "Raytheon",
            "Mitsubishi Heavy Industries Aerospace", "Kawasaki Aerospace"
        ],
        
        "Media_Entertainment_Extended": [
            # More media companies
            "Disney", "Warner Bros Discovery", "Comcast NBCUniversal", "ViacomCBS",
            "Sony Pictures", "Universal Music Group", "Warner Music Group",
            "BBC", "ITV", "Sky", "RTL Group", "Bertelsmann", "Vivendi"
        ]
    }

def check_global_job_seeker_gaps():
    """Check what's missing from a global job seeker perspective"""
    existing, existing_names = get_existing_companies()
    job_categories = get_global_job_seeker_missing_categories()
    
    print(f"Current collection size: {len(existing)} companies")
    print(f"👥 ANALYZING GAPS FOR GLOBAL JOB SEEKERS 👥")
    print(f"Focusing on major employers worldwide across all sectors...")
    print(f"=" * 80)
    
    all_missing = {}
    total_missing_employers = []
    total_employers_checked = 0
    
    for category, employer_list in job_categories.items():
        missing_in_category = []
        found_in_category = []
        total_employers_checked += len(employer_list)
        
        for employer in employer_list:
            normalized = normalize_name(employer)
            employer_lower = employer.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(employer)
                found = True
            else:
                # Check in original names with flexible matching
                for exist_name in existing_names:
                    # Extract key terms
                    employer_terms = [word for word in employer_lower.split() 
                                    if len(word) > 2 and word not in ['the', 'inc', 'corp', 'ltd', 'llc', 'group', 'company', 'of', 'and', 'for']]
                    
                    if employer_terms:
                        # Check if main employer name appears
                        main_term = employer_terms[0] if employer_terms else employer_lower
                        
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms
                            if main_term not in ['bank', 'group', 'corp', 'company', 'international', 'global', 'national', 'general']:
                                found_in_category.append(f"{employer} (found as: {exist_name})")
                                found = True
                                break
                        
                        # Check for brand combinations
                        if len(employer_terms) >= 2:
                            combo = f"{employer_terms[0]} {employer_terms[1]}"
                            if combo in exist_name and len(combo) >= 8:
                                found_in_category.append(f"{employer} (found as: {exist_name})")
                                found = True
                                break
                    
                    if found:
                        break
                    
                    # Also check full substring match
                    if employer_lower in exist_name or exist_name in employer_lower:
                        if len(employer_lower) >= 6:
                            found_in_category.append(f"{employer} (found as: {exist_name})")
                            found = True
                            break
                
                # Partial matches for well-known employers
                if not found:
                    for exist in existing:
                        if len(normalized) > 4 and len(exist) > 4:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.75:
                                    found_in_category.append(f"{employer} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(employer)
                total_missing_employers.append((employer, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(employer_list) * 100 if employer_list else 0
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(employer_list)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print(f"🚨 MISSING: {', '.join(missing_in_category[:6])}" + ("..." if len(missing_in_category) > 6 else ""))
    
    # Summary
    total_missing = len(total_missing_employers)
    
    print(f"\n👥 GLOBAL JOB SEEKER ANALYSIS COMPLETE!")
    print(f"Total major employers checked: {total_employers_checked}")
    print(f"Total missing employers: {total_missing}")
    print(f"Job seeker employer coverage: {((total_employers_checked - total_missing) / total_employers_checked * 100):.1f}%")
    
    # Show categories with most gaps (biggest employer opportunities)
    print(f"\n📊 BIGGEST EMPLOYMENT GAPS FOR JOB SEEKERS:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps[:12]:
        print(f"💼 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Priority missing employers for job seekers
    print(f"\n🎯 TOP 50 MISSING EMPLOYERS FOR GLOBAL JOB SEEKERS:")
    
    # Prioritize by job seeker importance
    category_priority = {
        'Major_Government_Employers': 10,       # Government jobs are huge
        'Top_Universities_Employers': 9,        # Universities are major employers
        'Major_Hospitals_Healthcare': 9,        # Healthcare is massive sector
        'Major_Law_Firms': 8,                   # High-paying legal careers
        'Top_Consulting_Extended': 8,           # Premium consulting careers
        'Regional_Conglomerates_Missing': 8,    # Major conglomerates
        'Major_Retail_Employers': 7,           # Retail is largest employment sector
        'Food_Beverage_Giants': 7,             # F&B major employers
        'Pharmaceutical_Biotech_Extended': 7,   # Pharma high-paying jobs
        'Energy_Utilities_Extended': 6,        # Energy sector jobs
        'Transportation_Logistics_Major': 6,    # Transportation jobs
        'Major_Banks_Extended': 6,             # More banking jobs
        'Telecommunications_Extended': 6,       # Telecom jobs
        'Manufacturing_Industrial_Giants': 5,   # Industrial jobs
        'Aerospace_Defense_Extended': 5,        # Aerospace jobs
        'Media_Entertainment_Extended': 4,      # Media jobs
        'Major_NGOs_Nonprofits': 4            # Mission-driven careers
    }
    
    priority_missing = []
    for employer, category in total_missing_employers:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((employer, category, priority_score))
    
    # Sort by priority for job seekers
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    for i, (employer, category, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {employer} ({category.replace('_', ' ')})")
    
    # Save job seeker analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_global_job_seeker_employers.txt', 'w') as f:
        f.write("MISSING EMPLOYERS FOR GLOBAL JOB SEEKERS ANALYSIS\n")
        f.write("Focus on companies people actually want to work for\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total missing employers: {total_missing}\n")
        f.write(f"Total employers checked: {total_employers_checked}\n")
        f.write(f"Job seeker coverage: {((total_employers_checked - total_missing) / total_employers_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for employer in data['missing']:
                    f.write(f"  - {employer}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING FOR JOB SEEKERS ###\n")
        for i, (employer, category, score) in enumerate(priority_missing[:100], 1):
            f.write(f"{i:3d}. {employer} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved job seeker analysis to missing_global_job_seeker_employers.txt")
    
    # Key insights for job seekers
    print(f"\n💡 KEY INSIGHTS FOR GLOBAL JOB SEEKERS:")
    if total_missing > 100:
        print(f"🎯 Found {total_missing} major employers missing from collection!")
        print(f"📈 Significant opportunity to serve job seekers better!")
        print(f"🏢 Focus on: Government, Universities, Healthcare, Law Firms, Consulting")
        print(f"🌍 Geographic gaps: Asia-Pacific, European conglomerates, regional banks")
    else:
        print(f"✅ Excellent job seeker coverage - only {total_missing} major employers missing!")
        print(f"🎯 Collection serves global job market exceptionally well!")
    
    return priority_missing[:100]

if __name__ == "__main__":
    check_global_job_seeker_gaps()