#!/usr/bin/env python3
"""
Find 800 actually missing companies by expanding search beyond Fortune 500
"""

import os
import json
import glob
from typing import Set, List, Dict

def normalize_name(name: str) -> str:
    """Normalize company name for comparison"""
    name = name.lower().replace('.png', '').replace('.jpg', '').replace('.svg', '')
    
    # Remove common suffixes
    suffixes = ['inc', 'corporation', 'corp', 'company', 'co', 'ltd', 'limited', 'llc', 'plc', 
                'group', 'holdings', 'international', 'global', 'partners', 'associates',
                'enterprises', 'solutions', 'systems', 'services', 'technologies', 'tech']
    
    for suffix in suffixes:
        name = name.replace(f' {suffix}', '').replace(f'_{suffix}', '')
    
    # Remove special characters and normalize spaces
    name = ''.join(c if c.isalnum() else ' ' for c in name)
    name = ' '.join(name.split())
    
    return name.strip()

def load_existing_logos() -> Set[str]:
    """Load all existing logo filenames"""
    existing = set()
    
    # Load from all_unique_logos
    unique_path = '/Users/adi/code/socratify/socratify-yolo/logos/all_unique_logos/'
    if os.path.exists(unique_path):
        for file in glob.glob(os.path.join(unique_path, '*.png')):
            basename = os.path.basename(file)
            existing.add(normalize_name(basename))
    
    # Load from downloads folder
    downloads_path = '/Users/adi/code/socratify/socratify-yolo/logos/downloads_20250807_175600/'
    if os.path.exists(downloads_path):
        for file in glob.glob(os.path.join(downloads_path, '**/*.png'), recursive=True):
            basename = os.path.basename(file)
            existing.add(normalize_name(basename))
    
    return existing

def get_expanded_company_list() -> Dict[str, List[str]]:
    """Get expanded list of important companies across all categories"""
    
    companies = {
        # Global Tech Companies (Expanded)
        "Global Tech Leaders": [
            "Oracle Corporation", "LinkedIn", "YouTube", "Reddit", "Pinterest",
            "Snapchat", "TikTok", "ByteDance", "WeChat", "Tencent", 
            "Alibaba", "Baidu", "JD.com", "Xiaomi", "Huawei",
            "Samsung Electronics", "LG Electronics", "Sony Corporation",
            "Panasonic", "Sharp", "Toshiba", "Fujitsu", "NEC",
            "Rakuten", "Line Corporation", "Naver", "Kakao",
            "Spotify", "SoundCloud", "Pandora", "Tidal", "Deezer"
        ],
        
        # Unicorn Startups & Scale-ups
        "Unicorn Companies": [
            "Stripe", "SpaceX", "Instacart", "Databricks", "Canva",
            "Revolut", "Nubank", "Chime", "Klarna", "Checkout.com",
            "Epic Games", "Discord", "Figma", "Notion", "Miro",
            "Grammarly", "Duolingo", "Coursera", "Udacity", "Udemy",
            "Byju's", "Gojek", "Grab", "Ola", "Didi Chuxing",
            "DoorDash", "Postmates", "Gopuff", "Getir", "Gorillas",
            "Rivian", "Lucid Motors", "Waymo", "Cruise", "Aurora",
            "Nuro", "Zoox", "Argo AI", "Pony.ai", "TuSimple",
            "UiPath", "Celonis", "Automation Anywhere", "Blue Prism",
            "Snowflake", "Confluent", "HashiCorp", "GitLab", "JFrog"
        ],
        
        # European Companies
        "European Corporations": [
            "Volkswagen Group", "Daimler AG", "BMW Group", "Stellantis",
            "Renault Group", "Volvo Cars", "Ferrari", "Porsche",
            "Total Energies", "Shell", "BP", "Eni", "Equinor",
            "Repsol", "OMV", "Neste", "Orlen", "MOL Group",
            "Nestle", "Unilever", "Danone", "Ferrero", "Lindt",
            "ABB", "Schneider Electric", "Legrand", "Siemens Energy",
            "E.ON", "RWE", "Iberdrola", "Enel", "EDF",
            "Telefonica", "Orange", "Deutsche Telekom", "Vodafone",
            "BT Group", "Swisscom", "KPN", "Proximus", "Elisa"
        ],
        
        # Asian Conglomerates
        "Asian Giants": [
            "Mitsubishi", "Mitsui", "Sumitomo", "Itochu", "Marubeni",
            "Toyota", "Honda", "Nissan", "Mazda", "Subaru",
            "Hyundai", "Kia", "SK Group", "LG Group", "Lotte",
            "Reliance Industries", "Tata Group", "Adani Group", "Wipro",
            "Infosys", "HCL Technologies", "Tech Mahindra", "Larsen & Toubro",
            "State Bank of India", "HDFC Bank", "ICICI Bank",
            "Industrial Bank of China", "China Construction Bank",
            "Agricultural Bank of China", "Bank of China", "Ping An"
        ],
        
        # Latin American Leaders
        "Latin American Companies": [
            "Petrobras", "Vale", "Itau Unibanco", "Banco Bradesco",
            "AmBev", "JBS", "WEG", "Embraer", "Natura", "Magazine Luiza",
            "America Movil", "Cemex", "Femsa", "Grupo Bimbo", "Televisa",
            "Grupo Carso", "Banorte", "Grupo Elektra", "Arca Continental",
            "Avianca", "LATAM Airlines", "Copa Airlines", "Azul",
            "Mercado Libre", "Globant", "Rappi", "Nubank", "PagSeguro"
        ],
        
        # Middle Eastern Companies
        "Middle East Leaders": [
            "Saudi Aramco", "SABIC", "Saudi Telecom", "Al Rajhi Bank",
            "National Commercial Bank", "Dubai Islamic Bank", "Emirates NBD",
            "Etisalat", "Du", "Ooredoo", "Zain", "Mobily",
            "Qatar Airways", "Emirates", "Etihad Airways", "Saudia",
            "ADNOC", "Qatar Petroleum", "Kuwait Petroleum", "Socar"
        ],
        
        # African Companies
        "African Leaders": [
            "MTN Group", "Vodacom", "Safaricom", "Airtel Africa",
            "Naspers", "Prosus", "Standard Bank", "FirstRand",
            "Sasol", "Anglo American", "Gold Fields", "AngloGold",
            "Shoprite", "Pick n Pay", "Woolworths", "Massmart",
            "Ethiopian Airlines", "Kenya Airways", "South African Airways",
            "Dangote Group", "Access Bank", "Zenith Bank", "GT Bank"
        ],
        
        # Pharmaceuticals & Healthcare
        "Pharma & Healthcare": [
            "Johnson & Johnson", "Pfizer", "Roche", "Novartis",
            "Merck", "GSK", "Sanofi", "AstraZeneca", "AbbVie",
            "Bristol Myers Squibb", "Eli Lilly", "Amgen", "Gilead",
            "Moderna", "BioNTech", "Regeneron", "Vertex", "Biogen",
            "HCA Healthcare", "Universal Health Services", "Tenet",
            "Community Health Systems", "LifePoint Health", "Encompass"
        ],
        
        # Private Equity & Asset Management
        "Private Equity & Asset Managers": [
            "Blackstone", "KKR", "Apollo", "Carlyle", "TPG",
            "Warburg Pincus", "Silver Lake", "Vista Equity", "Thoma Bravo",
            "Advent International", "CVC Capital", "EQT", "Permira",
            "Bain Capital", "Clayton Dubilier & Rice", "Leonard Green",
            "BlackRock", "Vanguard", "State Street", "Fidelity",
            "T. Rowe Price", "Franklin Templeton", "Invesco", "Schroders"
        ],
        
        # Luxury & Fashion
        "Luxury & Fashion": [
            "LVMH", "Kering", "Hermes", "Chanel", "Richemont",
            "Prada", "Burberry", "Versace", "Armani", "Dolce & Gabbana",
            "Gucci", "Louis Vuitton", "Dior", "Balenciaga", "Saint Laurent",
            "Bottega Veneta", "Celine", "Fendi", "Givenchy", "Valentino",
            "Rolex", "Omega", "Tag Heuer", "Breitling", "IWC",
            "Patek Philippe", "Audemars Piguet", "Richard Mille",
            "Ferrari", "Lamborghini", "Maserati", "Bentley", "Rolls-Royce",
            "Aston Martin", "McLaren", "Bugatti", "Pagani", "Koenigsegg"
        ],
        
        # Retail & E-commerce
        "Retail & E-commerce": [
            "Amazon", "Alibaba", "JD.com", "Pinduoduo", "Mercado Libre",
            "Shopify", "eBay", "Etsy", "Wayfair", "Chewy",
            "Walmart", "Target", "Costco", "Home Depot", "Lowe's",
            "CVS", "Walgreens", "Rite Aid", "Dollar General", "Dollar Tree",
            "Kroger", "Albertsons", "Publix", "H-E-B", "Wegmans",
            "Whole Foods", "Trader Joe's", "Aldi", "Lidl", "Tesco",
            "Carrefour", "Metro", "Casino", "Auchan", "E.Leclerc"
        ],
        
        # Media & Entertainment
        "Media & Entertainment": [
            "Disney", "Warner Bros Discovery", "Paramount Global", "NBCUniversal",
            "Sony Pictures", "Netflix", "Apple TV+", "Amazon Prime", "HBO Max",
            "Peacock", "Paramount+", "Discovery+", "Hulu", "ESPN+",
            "Spotify", "Apple Music", "YouTube Music", "Amazon Music", "Tidal",
            "Universal Music", "Sony Music", "Warner Music", "Live Nation",
            "Electronic Arts", "Activision Blizzard", "Take-Two", "Ubisoft",
            "Epic Games", "Valve", "Roblox", "Unity", "Zynga", "Supercell"
        ],
        
        # Airlines & Travel
        "Airlines & Travel": [
            "American Airlines", "Delta Air Lines", "United Airlines", "Southwest",
            "JetBlue", "Alaska Airlines", "Spirit", "Frontier", "Allegiant",
            "Air Canada", "WestJet", "Aeromexico", "Avianca", "LATAM",
            "British Airways", "Lufthansa", "Air France-KLM", "IAG", "Ryanair",
            "EasyJet", "Wizz Air", "Turkish Airlines", "Emirates", "Qatar Airways",
            "Singapore Airlines", "Cathay Pacific", "ANA", "JAL", "Korean Air",
            "Marriott", "Hilton", "Hyatt", "IHG", "Wyndham",
            "Accor", "Choice Hotels", "Best Western", "Radisson", "NH Hotels",
            "Booking.com", "Expedia", "Airbnb", "TripAdvisor", "Kayak"
        ],
        
        # Food & Beverage
        "Food & Beverage": [
            "Coca-Cola", "PepsiCo", "Red Bull", "Monster Energy", "Dr Pepper",
            "McDonald's", "Starbucks", "Subway", "KFC", "Burger King",
            "Pizza Hut", "Domino's", "Papa John's", "Wendy's", "Taco Bell",
            "Chipotle", "Chick-fil-A", "Dunkin'", "Tim Hortons", "Panera",
            "Nestle", "Unilever", "Mondelez", "General Mills", "Kellogg's",
            "Kraft Heinz", "Campbell's", "Hershey", "Mars", "Ferrero",
            "Danone", "Lactalis", "Yili", "Mengniu", "Fonterra",
            "Tyson Foods", "JBS", "WH Group", "BRF", "Perdue"
        ],
        
        # Telecommunications
        "Telecommunications": [
            "AT&T", "Verizon", "T-Mobile", "Sprint", "US Cellular",
            "Bell Canada", "Rogers", "Telus", "Shaw", "Quebecor",
            "America Movil", "Telefonica", "Claro", "Vivo", "TIM",
            "China Mobile", "China Telecom", "China Unicom", "NTT", "KDDI",
            "SoftBank", "SK Telecom", "KT", "LG U+", "Singtel",
            "Telstra", "Optus", "Vodafone", "Orange", "Deutsche Telekom",
            "BT", "Virgin Media O2", "Three", "TalkTalk", "Sky"
        ],
        
        # Energy & Utilities
        "Energy & Utilities": [
            "ExxonMobil", "Chevron", "ConocoPhillips", "Marathon", "Phillips 66",
            "Valero", "Occidental", "EOG Resources", "Pioneer", "Devon",
            "Shell", "BP", "Total", "Eni", "Equinor", "Repsol",
            "Saudi Aramco", "ADNOC", "Kuwait Petroleum", "Petrobras", "Pemex",
            "Gazprom", "Rosneft", "Lukoil", "Sinopec", "PetroChina",
            "NextEra Energy", "Duke Energy", "Southern Company", "Dominion",
            "Exelon", "AEP", "Xcel Energy", "ConEd", "PG&E", "Edison International",
            "National Grid", "E.ON", "RWE", "Enel", "Iberdrola", "EDF"
        ],
        
        # Real Estate
        "Real Estate": [
            "CBRE", "JLL", "Cushman & Wakefield", "Colliers", "Newmark",
            "Brookfield", "Blackstone Real Estate", "Prologis", "Public Storage",
            "Equity Residential", "AvalonBay", "Simon Property", "Realty Income",
            "American Tower", "Crown Castle", "SBA Communications", "Digital Realty",
            "Equinix", "Welltower", "Ventas", "Healthpeak", "Medical Properties",
            "Boston Properties", "Vornado", "SL Green", "Kilroy", "Hudson Pacific",
            "WeWork", "IWG", "Knotel", "Industrious", "Spaces"
        ],
        
        # Logistics & Shipping
        "Logistics & Shipping": [
            "UPS", "FedEx", "DHL", "USPS", "Amazon Logistics",
            "XPO Logistics", "C.H. Robinson", "J.B. Hunt", "Schneider",
            "Swift Transportation", "Werner", "Old Dominion", "YRC",
            "Maersk", "MSC", "CMA CGM", "Hapag-Lloyd", "ONE",
            "Evergreen", "COSCO", "Yang Ming", "HMM", "Zim",
            "DP World", "PSA International", "Hutchison Ports", "APM Terminals",
            "China Merchants", "HHLA", "Eurogate", "ICTSI", "SSA Marine"
        ],
        
        # Insurance
        "Insurance Companies": [
            "AXA", "Allianz", "Zurich", "Munich Re", "Swiss Re",
            "Berkshire Hathaway", "State Farm", "GEICO", "Progressive", "Allstate",
            "Liberty Mutual", "Travelers", "Chubb", "AIG", "Hartford",
            "MetLife", "Prudential", "New York Life", "Northwestern Mutual",
            "MassMutual", "John Hancock", "Principal", "Lincoln Financial",
            "Aflac", "Unum", "Guardian", "Anthem", "Centene", "Humana", "Cigna"
        ],
        
        # Automotive Suppliers
        "Auto Suppliers": [
            "Bosch", "Continental", "Denso", "Magna", "Aisin",
            "ZF Friedrichshafen", "Hyundai Mobis", "Lear", "Aptiv",
            "Valeo", "Faurecia", "BorgWarner", "Autoliv", "Garrett",
            "Visteon", "Adient", "Tenneco", "Dana", "American Axle",
            "Bridgestone", "Michelin", "Goodyear", "Continental Tire", "Pirelli"
        ],
        
        # Defense & Aerospace
        "Defense & Aerospace": [
            "Lockheed Martin", "Boeing Defense", "Raytheon", "Northrop Grumman",
            "General Dynamics", "L3Harris", "BAE Systems", "Airbus Defence",
            "Thales", "Leonardo", "Saab", "Dassault", "Rheinmetall",
            "Elbit Systems", "IAI", "Rafael", "MBDA", "Kongsberg",
            "Rolls-Royce Defence", "Safran", "MTU Aero", "GE Aviation",
            "Pratt & Whitney", "Honeywell Aerospace", "Collins Aerospace"
        ],
        
        # Construction & Engineering
        "Construction & Engineering": [
            "Bechtel", "Fluor", "Kiewit", "Turner Construction", "Walsh Group",
            "Skanska", "Bouygues", "Vinci", "ACS Group", "Ferrovial",
            "Balfour Beatty", "Kier Group", "Laing O'Rourke", "Strabag",
            "Hochtief", "Kajima", "Obayashi", "Shimizu", "Taisei",
            "China State Construction", "China Railway Construction",
            "China Communications Construction", "Power Construction Corp of China"
        ],
        
        # Semiconductors
        "Semiconductor Companies": [
            "Intel", "AMD", "NVIDIA", "Qualcomm", "Broadcom",
            "Texas Instruments", "Analog Devices", "Microchip", "Xilinx",
            "Marvell", "MediaTek", "Realtek", "Infineon", "STMicroelectronics",
            "NXP", "ON Semiconductor", "Skyworks", "Qorvo", "Cirrus Logic",
            "TSMC", "Samsung Foundry", "GlobalFoundries", "UMC", "SMIC",
            "ASML", "Applied Materials", "Lam Research", "KLA", "Tokyo Electron"
        ],
        
        # Venture Capital
        "Venture Capital": [
            "Sequoia Capital", "Andreessen Horowitz", "Accel", "Benchmark",
            "Kleiner Perkins", "Greylock", "Bessemer", "NEA", "Lightspeed",
            "General Catalyst", "GGV Capital", "Insight Partners", "Battery Ventures",
            "Index Ventures", "Balderton", "Atomico", "Northzone", "Creandum",
            "Tiger Global", "Coatue", "DST Global", "SoftBank Vision Fund",
            "GIC", "Temasek", "Khosla Ventures", "Founders Fund", "Thrive Capital"
        ],
        
        # Fintech
        "Fintech Companies": [
            "Square", "Block", "Cash App", "Stripe", "Adyen",
            "PayPal", "Venmo", "Zelle", "Wise", "Revolut",
            "N26", "Monzo", "Starling Bank", "Chime", "Current",
            "SoFi", "Affirm", "Klarna", "Afterpay", "Zip",
            "Robinhood", "eToro", "Plus500", "Interactive Brokers", "Charles Schwab",
            "Plaid", "Marqeta", "Bill.com", "Brex", "Ramp"
        ],
        
        # Cloud & Enterprise Software
        "Cloud & Enterprise": [
            "Salesforce", "ServiceNow", "Workday", "SAP", "Oracle",
            "Microsoft Azure", "Google Cloud", "AWS", "IBM Cloud", "Alibaba Cloud",
            "Snowflake", "Databricks", "Palantir", "Splunk", "Elastic",
            "MongoDB", "Redis", "Confluent", "HashiCorp", "GitLab",
            "Atlassian", "Slack", "Zoom", "Teams", "Box",
            "Dropbox", "DocuSign", "Okta", "CrowdStrike", "Palo Alto Networks"
        ],
        
        # Cybersecurity
        "Cybersecurity": [
            "Palo Alto Networks", "CrowdStrike", "Fortinet", "Check Point",
            "Zscaler", "Okta", "SentinelOne", "Cyberark", "Rapid7",
            "Qualys", "Tenable", "Darktrace", "Proofpoint", "Mimecast",
            "FireEye", "Mandiant", "McAfee", "Norton", "Kaspersky",
            "Trend Micro", "Sophos", "ESET", "Bitdefender", "Avast"
        ],
        
        # Sports & Entertainment
        "Sports & Entertainment": [
            "NFL", "NBA", "MLB", "NHL", "MLS",
            "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
            "UEFA", "FIFA", "Olympics", "Formula 1", "NASCAR",
            "Nike", "Adidas", "Under Armour", "Puma", "New Balance",
            "ESPN", "Fox Sports", "NBC Sports", "CBS Sports", "DAZN",
            "Manchester United", "Real Madrid", "Barcelona", "Liverpool", "Bayern Munich",
            "Yankees", "Lakers", "Cowboys", "Patriots", "Warriors"
        ],
        
        # Education Technology
        "EdTech": [
            "Coursera", "Udacity", "edX", "Khan Academy", "Duolingo",
            "Chegg", "Course Hero", "Quizlet", "Brainly", "Photomath",
            "Blackboard", "Canvas", "Moodle", "Google Classroom", "Schoology",
            "2U", "Pluralsight", "LinkedIn Learning", "Skillshare", "MasterClass",
            "Byju's", "Yuanfudao", "Zuoyebang", "VIPKid", "GSX Techedu"
        ],
        
        # Agricultural & Food Tech
        "AgTech & FoodTech": [
            "John Deere", "AGCO", "CNH Industrial", "Kubota", "Mahindra",
            "Bayer Crop Science", "Corteva", "Syngenta", "BASF Agricultural",
            "Nutrien", "Mosaic", "CF Industries", "Yara", "ICL Group",
            "Beyond Meat", "Impossible Foods", "Oatly", "Perfect Day", "Memphis Meats",
            "AppHarvest", "Plenty", "AeroFarms", "Bowery Farming", "Infarm"
        ],
        
        # Space & Satellite
        "Space & Satellite": [
            "SpaceX", "Blue Origin", "Virgin Galactic", "Rocket Lab", "Astra",
            "Relativity Space", "Firefly Aerospace", "Sierra Space", "Axiom Space",
            "Planet Labs", "Spire Global", "BlackSky", "Maxar", "Capella Space",
            "OneWeb", "Starlink", "Amazon Kuiper", "Telesat", "Viasat",
            "Intelsat", "SES", "Eutelsat", "Inmarsat", "Iridium"
        ],
        
        # Blockchain & Crypto
        "Blockchain & Crypto": [
            "Coinbase", "Binance", "Kraken", "Gemini", "FTX",
            "Crypto.com", "Huobi", "OKX", "Bybit", "Bitfinex",
            "Circle", "Tether", "Paxos", "BitGo", "Anchorage",
            "BlockFi", "Celsius", "Nexo", "Genesis", "Galaxy Digital",
            "Grayscale", "MicroStrategy", "Riot Blockchain", "Marathon Digital",
            "Ethereum Foundation", "Cardano", "Solana Labs", "Avalanche", "Polygon"
        ],
        
        # Gaming & Esports
        "Gaming & Esports": [
            "Activision Blizzard", "Electronic Arts", "Take-Two Interactive",
            "Ubisoft", "Epic Games", "Valve", "Riot Games", "Roblox",
            "Unity", "Zynga", "Supercell", "King", "Rovio", "Glu Mobile",
            "Team SoloMid", "Cloud9", "FaZe Clan", "100 Thieves", "G2 Esports",
            "Fnatic", "Evil Geniuses", "OpTic Gaming", "NRG Esports", "Gen.G"
        ],
        
        # Renewable Energy
        "Renewable Energy": [
            "NextEra Energy", "Orsted", "Iberdrola", "Enel Green Power", "EDP Renewables",
            "Vestas", "Siemens Gamesa", "GE Renewable Energy", "Goldwind", "Envision",
            "First Solar", "SunPower", "Canadian Solar", "JinkoSolar", "Trina Solar",
            "Enphase Energy", "SolarEdge", "Sunrun", "Tesla Energy", "Fluence",
            "ChargePoint", "EVgo", "Electrify America", "Blink Charging", "Volta"
        ],
        
        # Biotech & Life Sciences
        "Biotech & Life Sciences": [
            "Amgen", "Gilead Sciences", "Biogen", "Regeneron", "Vertex",
            "Moderna", "BioNTech", "CureVac", "Novavax", "Inovio",
            "Illumina", "Thermo Fisher", "Danaher", "Waters", "PerkinElmer",
            "Agilent", "Bio-Rad", "IQVIA", "Charles River", "Lonza",
            "WuXi AppTec", "Samsung Biologics", "Celltrion", "Biocon", "Dr. Reddy's"
        ]
    }
    
    return companies

def check_missing(companies: Dict[str, List[str]], existing: Set[str]) -> Dict[str, List[str]]:
    """Check which companies are actually missing"""
    missing = {}
    
    for category, company_list in companies.items():
        missing_in_category = []
        for company in company_list:
            normalized = normalize_name(company)
            
            # Check if exists
            found = False
            for existing_name in existing:
                if normalized in existing_name or existing_name in normalized:
                    found = True
                    break
                # Check partial matches
                if len(normalized) > 5:
                    normalized_parts = normalized.split()
                    if normalized_parts and normalized_parts[0] in existing_name:
                        if len(normalized_parts) == 1 or (len(normalized_parts) > 1 and normalized_parts[1] in existing_name):
                            found = True
                            break
            
            if not found:
                missing_in_category.append(company)
        
        if missing_in_category:
            missing[category] = missing_in_category
    
    return missing

def main():
    print("Loading existing logos...")
    existing = load_existing_logos()
    print(f"Found {len(existing)} existing logo files")
    
    print("\nGetting expanded company list...")
    companies = get_expanded_company_list()
    total_companies = sum(len(c) for c in companies.values())
    print(f"Checking {total_companies} companies across {len(companies)} categories")
    
    print("\nFinding actually missing companies...")
    missing = check_missing(companies, existing)
    
    # Count missing
    total_missing = sum(len(c) for c in missing.values())
    print(f"\nFound {total_missing} actually missing companies")
    
    # Save results
    output = {
        'total_checked': total_companies,
        'total_existing': len(existing),
        'total_missing': total_missing,
        'missing_by_category': missing,
        'coverage_rate': f"{((total_companies - total_missing) / total_companies * 100):.1f}%"
    }
    
    with open('/Users/adi/code/socratify/socratify-yolo/logos/expanded_missing_companies.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    # Create downloadable list
    with open('/Users/adi/code/socratify/socratify-yolo/logos/missing_800_companies.txt', 'w') as f:
        f.write("# 800+ Actually Missing Companies for Download\n\n")
        
        count = 0
        for category, companies in missing.items():
            f.write(f"\n## {category}\n")
            for company in companies:
                f.write(f"{company}\n")
                count += 1
                if count >= 800:
                    break
            if count >= 800:
                break
    
    print(f"\nResults saved to:")
    print("- expanded_missing_companies.json (detailed analysis)")
    print("- missing_800_companies.txt (list for download)")
    
    # Print summary
    print("\n" + "="*50)
    print("SUMMARY OF MISSING COMPANIES BY CATEGORY:")
    print("="*50)
    for category, companies in missing.items():
        print(f"{category}: {len(companies)} missing")
    
    print(f"\nTotal coverage rate: {output['coverage_rate']}")

if __name__ == "__main__":
    main()