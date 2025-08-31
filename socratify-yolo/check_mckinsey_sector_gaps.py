#!/usr/bin/env python3
"""
Check McKinsey-style sector analysis for missing companies
Comprehensive sector-by-sector analysis of what we're missing
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

def get_mckinsey_sector_companies():
    """McKinsey-style comprehensive sector analysis"""
    return {
        "Advanced_Industries": [
            # Aerospace & Defense
            "Airbus", "Boeing", "Lockheed Martin", "Northrop Grumman", "Raytheon Technologies",
            "General Dynamics", "L3Harris", "BAE Systems", "Thales", "Leonardo",
            "Safran", "Rolls-Royce Holdings", "MTU Aero Engines", "Spirit AeroSystems",
            
            # Industrial Automation & Robotics
            "ABB", "Siemens", "Schneider Electric", "Rockwell Automation", "Emerson Electric",
            "Honeywell", "Mitsubishi Electric", "Omron", "Fanuc", "KUKA",
            "Universal Robots", "Boston Dynamics", "Intuitive Surgical", "Teradyne",
            
            # Semiconductors & Electronics
            "TSMC", "Samsung", "Intel", "NVIDIA", "Qualcomm", "Broadcom", "AMD",
            "Marvell Technology", "Analog Devices", "Micron Technology", "SK Hynix",
            "Applied Materials", "ASML", "KLA Corporation", "Lam Research"
        ],
        
        "Automotive_Mobility": [
            # Traditional Auto OEMs
            "Toyota", "Volkswagen Group", "General Motors", "Ford", "Stellantis",
            "Hyundai Motor", "Nissan", "Honda", "BMW", "Mercedes-Benz", "Audi",
            "Volvo Cars", "Jaguar Land Rover", "Mazda", "Subaru", "Suzuki",
            
            # EV & New Mobility
            "Tesla", "BYD", "NIO", "XPeng", "Li Auto", "Rivian", "Lucid Motors",
            "Polestar", "VinFast", "Canoo", "Fisker", "Lordstown Motors",
            
            # Auto Suppliers
            "Bosch", "Continental", "Magna International", "Denso", "ZF Friedrichshafen",
            "Aptiv", "Lear Corporation", "Valeo", "Faurecia", "Autoliv"
        ],
        
        "Chemicals_Materials": [
            # Diversified Chemicals
            "BASF", "Dow", "DuPont", "SABIC", "Evonik Industries", "Huntsman",
            "Eastman Chemical", "Celanese", "Covestro", "Solvay",
            
            # Specialty Chemicals
            "Sherwin-Williams", "PPG Industries", "AkzoNobel", "Clariant", "Arkema",
            "Wacker Chemie", "Henkel", "3M", "Corning", "Johnson Matthey",
            
            # Materials & Mining
            "BHP", "Rio Tinto", "Vale", "Glencore", "Freeport-McMoRan",
            "Newmont", "Barrick Gold", "Anglo American", "Teck Resources"
        ],
        
        "Consumer_Packaged_Goods": [
            # Food & Beverage
            "Nestlé", "Unilever", "Procter & Gamble", "PepsiCo", "Coca-Cola",
            "Mondelez International", "Mars", "General Mills", "Kellogg", "Kraft Heinz",
            "Danone", "Tyson Foods", "JBS", "Cargill", "Archer Daniels Midland",
            
            # Personal Care & Household
            "L'Oréal", "Estée Lauder", "Coty", "Beiersdorf", "Kao Corporation",
            "Shiseido", "Colgate-Palmolive", "Church & Dwight", "Henkel",
            
            # Tobacco & Alternative Products
            "Philip Morris International", "Altria", "British American Tobacco",
            "Japan Tobacco", "Imperial Brands", "JUUL Labs"
        ],
        
        "Energy_Power_Materials": [
            # Oil & Gas Majors
            "Saudi Aramco", "ExxonMobil", "Royal Dutch Shell", "BP", "Chevron",
            "TotalEnergies", "Eni", "Equinor", "ConocoPhillips", "Suncor Energy",
            
            # Oil Services
            "Schlumberger", "Halliburton", "Baker Hughes", "Weatherford International",
            "NOV Inc", "TechnipFMC", "Saipem", "Subsea 7",
            
            # Renewables & Clean Energy
            "NextEra Energy", "Iberdrola", "Ørsted", "Vestas", "Siemens Gamesa",
            "First Solar", "SunPower", "Canadian Solar", "JinkoSolar", "Trina Solar",
            
            # Power Generation & Utilities
            "China State Grid", "State Grid Corporation", "Enel", "E.ON", "RWE",
            "Duke Energy", "Southern Company", "Dominion Energy", "American Electric Power"
        ],
        
        "Financial_Services": [
            # Global Investment Banks
            "JPMorgan Chase", "Goldman Sachs", "Morgan Stanley", "Bank of America",
            "Wells Fargo", "Citigroup", "Deutsche Bank", "UBS", "Credit Suisse",
            "Barclays", "HSBC", "BNP Paribas", "Société Générale", "ING Group",
            
            # Asset Management
            "BlackRock", "Vanguard", "State Street", "Fidelity Investments",
            "T. Rowe Price", "Capital Group", "Invesco", "Franklin Templeton",
            
            # Insurance
            "Berkshire Hathaway", "Ping An", "Allianz", "AXA", "China Life",
            "Prudential Financial", "MetLife", "Generali", "Zurich Insurance",
            
            # Fintech & Payments
            "Visa", "Mastercard", "PayPal", "Block", "Stripe", "Klarna", "Adyen",
            "Ant Group", "Tencent FinTech", "Paytm", "Razorpay"
        ],
        
        "Healthcare_Pharma_Medtech": [
            # Big Pharma
            "Johnson & Johnson", "Pfizer", "Roche", "Novartis", "Merck KGaA",
            "Sanofi", "GlaxoSmithKline", "AbbVie", "Bristol Myers Squibb", "AstraZeneca",
            "Eli Lilly", "Amgen", "Gilead Sciences", "Biogen", "Regeneron",
            
            # Biotech
            "Moderna", "BioNTech", "Illumina", "Vertex Pharmaceuticals", "Alexion",
            "Genmab", "Alnylam Pharmaceuticals", "Incyte", "BioMarin",
            
            # Medical Devices
            "Medtronic", "Abbott", "Danaher", "Thermo Fisher Scientific", "Boston Scientific",
            "Stryker", "Becton Dickinson", "Zimmer Biomet", "Edwards Lifesciences",
            
            # Healthcare Services
            "UnitedHealth Group", "CVS Health", "Anthem", "Humana", "Cigna",
            "Aetna", "Centene", "Molina Healthcare", "WellCare", "Kaiser Permanente"
        ],
        
        "Public_Social_Sector": [
            # Government Contractors
            "Booz Allen Hamilton", "CACI", "Science Applications International",
            "General Dynamics Information Technology", "Leidos", "MITRE Corporation",
            "Raytheon Intelligence & Information Systems", "ManTech International",
            
            # Education & Training
            "Pearson", "McGraw Hill", "Cengage Learning", "Wiley", "Elsevier",
            "Coursera", "Udacity", "Pluralsight", "MasterClass", "Khan Academy",
            
            # Non-Profit & Social Impact
            "United Nations", "World Bank", "International Monetary Fund",
            "Red Cross", "Doctors Without Borders", "Oxfam", "UNICEF", "WHO"
        ],
        
        "Real_Estate_Infrastructure": [
            # Commercial Real Estate
            "Brookfield Asset Management", "Simon Property Group", "Prologis",
            "American Tower", "Crown Castle", "Equinix", "Digital Realty Trust",
            "Boston Properties", "Vornado Realty Trust", "SL Green Realty",
            
            # Construction & Infrastructure
            "China Communications Construction", "Vinci", "Bouygues", "Skanska",
            "Fluor", "Jacobs Engineering", "AECOM", "KBR", "Wood Group",
            
            # Materials & Building Products
            "CRH", "LafargeHolcim", "Cemex", "HeidelbergCement", "Vulcan Materials",
            "Martin Marietta", "Owens Corning", "Masco", "Fortune Brands"
        ],
        
        "Retail_Consumer_Services": [
            # E-commerce & Digital
            "Amazon", "Alibaba", "JD.com", "Shopify", "MercadoLibre", "Sea Limited",
            "Rakuten", "eBay", "Etsy", "Zalando", "Delivery Hero", "DoorDash",
            
            # Traditional Retail
            "Walmart", "Costco", "The Home Depot", "Target", "Lowe's",
            "Best Buy", "Macy's", "Nordstrom", "TJX Companies", "Ross Stores",
            
            # Luxury & Fashion
            "LVMH", "Hermès", "Chanel", "Kering", "Richemont", "Burberry",
            "Ralph Lauren", "PVH", "Tapestry", "Capri Holdings",
            
            # Hospitality & Travel
            "Marriott International", "Hilton", "Hyatt", "InterContinental Hotels",
            "Airbnb", "Booking Holdings", "Expedia", "TripAdvisor", "Uber", "Lyft"
        ],
        
        "Technology_Media_Telecom": [
            # Big Tech
            "Apple", "Microsoft", "Alphabet", "Amazon", "Meta", "Tesla",
            "NVIDIA", "Taiwan Semiconductor", "Broadcom", "Oracle", "Salesforce",
            
            # Cloud & Enterprise Software
            "ServiceNow", "Snowflake", "Palantir", "CrowdStrike", "Zoom",
            "DocuSign", "Workday", "Splunk", "VMware", "Citrix",
            
            # Telecom & Infrastructure
            "Verizon", "AT&T", "T-Mobile", "China Mobile", "Vodafone", "Orange",
            "Deutsche Telekom", "NTT", "SoftBank", "Telefónica",
            
            # Media & Entertainment
            "Disney", "Netflix", "Comcast", "Charter Communications", "Warner Bros Discovery",
            "Paramount", "Sony", "Universal Music Group", "Spotify", "Roku",
            
            # Gaming
            "Tencent", "Sony Interactive", "Microsoft Xbox", "Nintendo", "Electronic Arts",
            "Activision Blizzard", "Take-Two Interactive", "Ubisoft", "Epic Games"
        ],
        
        "Travel_Logistics_Infrastructure": [
            # Airlines
            "American Airlines", "Delta Air Lines", "United Airlines", "Southwest Airlines",
            "Lufthansa", "Air France-KLM", "British Airways", "Emirates", "Qatar Airways",
            "Singapore Airlines", "Cathay Pacific", "ANA", "JAL",
            
            # Logistics & Shipping
            "FedEx", "UPS", "DHL", "Maersk", "MSC", "COSCO Shipping", "Hapag-Lloyd",
            "C.H. Robinson", "Expeditors", "DSV", "Kuehne + Nagel", "DB Schenker",
            
            # Transportation Infrastructure
            "Union Pacific", "CSX", "Norfolk Southern", "Canadian National Railway",
            "BNSF Railway", "Kansas City Southern", "Canadian Pacific Railway"
        ]
    }

def check_sector_gaps():
    """Check for sector-by-sector gaps"""
    existing, existing_names = get_existing_companies()
    sector_companies = get_mckinsey_sector_companies()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Checking McKinsey-style sector analysis for gaps...")
    print(f"=" * 60)
    
    all_missing = {}
    total_missing_companies = []
    
    for sector, companies in sector_companies.items():
        missing_in_sector = []
        found_in_sector = []
        
        for company in companies:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_sector.append(company)
                found = True
            else:
                # Check in original names with flexible matching
                for exist_name in existing_names:
                    # Split company name into key terms
                    company_terms = [word for word in company_lower.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'llc', 'ltd', 'co', 'corp', 'company', 'group', 'holdings']]
                    
                    if company_terms:
                        main_term = company_terms[0]
                        # More flexible matching for sector analysis
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms
                            if main_term not in ['app', 'web', 'data', 'cloud', 'smart', 'digital', 'global', 'international', 'american', 'china', 'new', 'first']:
                                found_in_sector.append(f"{company} (found as: {exist_name})")
                                found = True
                                break
                    
                    # Also check full substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        if len(company_lower) >= 4:
                            found_in_sector.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 4 and len(exist) > 4:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.75:  # High confidence matching
                                    found_in_sector.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_sector.append(company)
                total_missing_companies.append((company, sector))
        
        all_missing[sector] = {
            'missing': missing_in_sector,
            'found': found_in_sector,
            'coverage': len(found_in_sector) / len(companies) * 100 if companies else 0
        }
        
        print(f"\n=== {sector.upper().replace('_', ' ')} ===")
        print(f"Total: {len(companies)} | Found: {len(found_in_sector)} ({all_missing[sector]['coverage']:.1f}%) | Missing: {len(missing_in_sector)}")
        
        if missing_in_sector:
            print("🚨 MISSING:", ', '.join(missing_in_sector[:10]) + ("..." if len(missing_in_sector) > 10 else ""))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🏭 MCKINSEY SECTOR ANALYSIS SUMMARY")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Prioritize by sector importance and company size
    sector_priority = {
        'Technology_Media_Telecom': 10,      # Highest demand sector
        'Financial_Services': 9,             # High-paying sector
        'Healthcare_Pharma_Medtech': 9,      # Major growth sector
        'Consumer_Packaged_Goods': 8,        # Major brands
        'Advanced_Industries': 8,            # High-tech manufacturing
        'Automotive_Mobility': 7,            # Major transformation
        'Energy_Power_Materials': 7,         # Essential sector
        'Retail_Consumer_Services': 6,       # Consumer-facing
        'Chemicals_Materials': 6,            # Industrial base
        'Travel_Logistics_Infrastructure': 5, # Essential services
        'Real_Estate_Infrastructure': 4,     # Construction/RE
        'Public_Social_Sector': 3            # Government/non-profit
    }
    
    priority_missing = []
    for company, sector in total_missing_companies:
        priority_score = sector_priority.get(sector, 3)
        priority_missing.append((company, sector, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 100 MISSING BY SECTOR PRIORITY:")
    for i, (company, sector, score) in enumerate(priority_missing[:100], 1):
        print(f"{i:3d}. {company} ({sector.replace('_', ' ')})")
    
    # Show sector gaps summary
    print(f"\n📊 SECTOR GAPS RANKED BY MISSING COUNT:")
    sector_gaps = [(sector, len(data['missing']), data['coverage']) 
                   for sector, data in all_missing.items() if data['missing']]
    sector_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for sector, missing_count, coverage in sector_gaps:
        print(f"📉 {sector.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Save comprehensive sector analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_mckinsey_sectors.txt', 'w') as f:
        f.write("MCKINSEY SECTOR ANALYSIS - MISSING COMPANIES\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_checked}\n")
        f.write(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%\n\n")
        
        for sector, data in all_missing.items():
            if data['missing']:
                f.write(f"### {sector.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for company in data['missing']:
                    f.write(f"  - {company}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (company, sector, score) in enumerate(priority_missing[:150], 1):
            f.write(f"{i:3d}. {company} ({sector.replace('_', ' ')})\n")
    
    print(f"\nSaved sector analysis to missing_mckinsey_sectors.txt")
    print(f"🎯 These are the gaps in our world-class business logo collection!")
    
    return priority_missing[:150]  # Return top 150

if __name__ == "__main__":
    check_sector_gaps()