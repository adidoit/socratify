#!/usr/bin/env python3
"""
Find niche and specialized companies we're missing - be EXTREMELY expansive
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
    
    name = ''.join(c if c.isalnum() else ' ' for c in name)
    name = ' '.join(name.split())
    
    return name.strip()

def load_all_existing_logos() -> Set[str]:
    """Load ALL existing logo filenames"""
    existing = set()
    
    logo_dirs = [
        '/Users/adi/code/socratify/socratify-yolo/logos/all_unique_logos/',
        '/Users/adi/code/socratify/socratify-yolo/logos/downloads_20250807_175600/',
        '/Users/adi/code/socratify/socratify-yolo/logos/verified_downloads_20250807_184645/',
    ]
    
    for directory in logo_dirs:
        if os.path.exists(directory):
            for file in glob.glob(os.path.join(directory, '**/*'), recursive=True):
                if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico')):
                    basename = os.path.basename(file)
                    existing.add(normalize_name(basename))
    
    return existing

def get_ultra_comprehensive_companies() -> Dict[str, List[str]]:
    """Get ULTRA comprehensive list including niche sectors"""
    
    companies = {
        # SPORTS LEAGUES & TEAMS
        "Major Sports Leagues": [
            "NFL", "NBA", "MLB", "NHL", "MLS", "WNBA", "NWSL", "XFL", "USFL",
            "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
            "UEFA", "FIFA", "Olympics", "Formula 1", "NASCAR", "IndyCar",
            "PGA Tour", "LPGA", "ATP Tour", "WTA", "UFC", "WWE", "AEW",
            "IPL", "Big Bash League", "The Hundred", "CPL", "PSL"
        ],
        
        "Top Sports Teams": [
            "Dallas Cowboys", "New England Patriots", "Los Angeles Rams", "New York Giants",
            "Los Angeles Lakers", "Boston Celtics", "Golden State Warriors", "Chicago Bulls",
            "New York Yankees", "Los Angeles Dodgers", "Boston Red Sox", "Chicago Cubs",
            "Montreal Canadiens", "Toronto Maple Leafs", "New York Rangers", "Chicago Blackhawks",
            "Manchester United", "Real Madrid", "Barcelona", "Liverpool", "Manchester City",
            "Bayern Munich", "Borussia Dortmund", "Juventus", "AC Milan", "Inter Milan",
            "Paris Saint-Germain", "Olympique Marseille", "Ajax", "Benfica", "Celtic"
        ],
        
        # FASHION & LUXURY
        "High Fashion Houses": [
            "Chanel", "Hermès", "Louis Vuitton", "Gucci", "Prada", "Dior", "Balenciaga",
            "Saint Laurent", "Givenchy", "Valentino", "Versace", "Armani", "Dolce & Gabbana",
            "Bottega Veneta", "Fendi", "Celine", "Loewe", "Balmain", "Lanvin", "Chloe",
            "Alexander McQueen", "Stella McCartney", "Off-White", "Vetements", "Jacquemus"
        ],
        
        "Watch Brands": [
            "Rolex", "Patek Philippe", "Audemars Piguet", "Vacheron Constantin", "A. Lange & Söhne",
            "Omega", "Tag Heuer", "Breitling", "IWC", "Cartier", "Jaeger-LeCoultre",
            "Panerai", "Hublot", "Richard Mille", "Tudor", "Grand Seiko", "Zenith",
            "Girard-Perregaux", "Ulysse Nardin", "Blancpain", "Breguet", "Chopard",
            "Montblanc", "Longines", "Tissot", "Hamilton", "Oris", "Bell & Ross"
        ],
        
        "Jewelry Brands": [
            "Tiffany & Co", "Cartier", "Van Cleef & Arpels", "Bulgari", "Harry Winston",
            "Graff", "Chopard", "Piaget", "Boucheron", "Chaumet", "Mikimoto",
            "David Yurman", "John Hardy", "Lagos", "Pandora", "Swarovski",
            "De Beers", "Forevermark", "Hearts on Fire", "Leo Schachter", "Blue Nile"
        ],
        
        # ENTERTAINMENT & MEDIA
        "Film Studios": [
            "Warner Bros", "Universal Pictures", "Paramount Pictures", "Sony Pictures",
            "20th Century Studios", "Walt Disney Pictures", "Pixar", "DreamWorks",
            "Lionsgate", "MGM", "New Line Cinema", "Focus Features", "A24",
            "Blumhouse", "Legendary Pictures", "Village Roadshow", "Studio Ghibli",
            "Toho", "Toei", "Shaw Brothers", "Golden Harvest", "Gaumont", "Pathé"
        ],
        
        "Music Labels": [
            "Universal Music Group", "Sony Music", "Warner Music Group", "EMI",
            "Columbia Records", "Atlantic Records", "Capitol Records", "Epic Records",
            "Def Jam", "Interscope", "Republic Records", "Island Records", "Motown",
            "Blue Note", "Verve", "Deutsche Grammophon", "Decca", "RCA Records",
            "Sub Pop", "Matador", "4AD", "XL Recordings", "Ninja Tune", "Warp Records"
        ],
        
        "Streaming Platforms": [
            "Netflix", "Disney+", "HBO Max", "Paramount+", "Peacock", "Apple TV+",
            "Amazon Prime Video", "Hulu", "Discovery+", "ESPN+", "DAZN", "FuboTV",
            "Sling TV", "YouTube TV", "Philo", "Crunchyroll", "Funimation",
            "BritBox", "Acorn TV", "MHz Choice", "Shudder", "Criterion Channel"
        ],
        
        # RESTAURANTS & HOSPITALITY
        "Fast Food Chains": [
            "McDonald's", "Burger King", "Wendy's", "KFC", "Popeyes", "Chick-fil-A",
            "Taco Bell", "Chipotle", "Five Guys", "In-N-Out", "Whataburger", "Carl's Jr",
            "Jack in the Box", "Sonic", "Arby's", "Hardee's", "White Castle", "Krystal",
            "Subway", "Jimmy John's", "Jersey Mike's", "Firehouse Subs", "Quiznos"
        ],
        
        "Coffee Chains": [
            "Starbucks", "Dunkin'", "Tim Hortons", "Costa Coffee", "Peet's Coffee",
            "Caribou Coffee", "Dutch Bros", "The Coffee Bean", "Gloria Jean's",
            "Lavazza", "Illy", "Blue Bottle Coffee", "Intelligentsia", "Stumptown",
            "La Colombe", "Philz Coffee", "Death Wish Coffee", "Black Rifle Coffee"
        ],
        
        "Restaurant Groups": [
            "Darden Restaurants", "Brinker International", "Bloomin' Brands", "Dine Brands",
            "Yum! Brands", "Restaurant Brands International", "Inspire Brands", "Focus Brands",
            "The Cheesecake Factory", "BJ's Restaurants", "Texas Roadhouse", "Cracker Barrel",
            "Red Lobster", "Olive Garden", "Applebee's", "TGI Friday's", "Chili's",
            "Outback Steakhouse", "Carrabba's", "Ruth's Chris", "Morton's", "STK"
        ],
        
        # CONSUMER GOODS
        "Household Brands": [
            "Procter & Gamble", "Unilever", "Colgate-Palmolive", "Henkel", "Reckitt",
            "SC Johnson", "Clorox", "Church & Dwight", "Kimberly-Clark", "Georgia-Pacific",
            "Seventh Generation", "Method", "Mrs. Meyer's", "Lysol", "Tide",
            "Dove", "Axe", "Old Spice", "Head & Shoulders", "Pantene", "Olay"
        ],
        
        "Beverage Brands": [
            "Coca-Cola", "Pepsi", "Dr Pepper", "Mountain Dew", "Sprite", "Fanta",
            "Red Bull", "Monster Energy", "Rockstar", "Bang Energy", "Celsius",
            "Gatorade", "Powerade", "Vitamin Water", "Snapple", "Arizona",
            "Lipton", "Nestea", "Pure Leaf", "Gold Peak", "Honest Tea",
            "La Croix", "Perrier", "San Pellegrino", "Evian", "Fiji Water"
        ],
        
        "Snack Brands": [
            "Lay's", "Doritos", "Cheetos", "Pringles", "Ruffles", "Fritos",
            "Oreo", "Chips Ahoy", "Ritz", "Wheat Thins", "Triscuit", "Goldfish",
            "Cheez-It", "Pop-Tarts", "Nature Valley", "Clif Bar", "KIND",
            "Quest", "RXBAR", "Larabar", "Luna Bar", "PowerBar", "Gatorade Bar"
        ],
        
        # FINANCIAL SERVICES
        "Investment Banks": [
            "Goldman Sachs", "Morgan Stanley", "JPMorgan Chase", "Bank of America Merrill Lynch",
            "Citigroup", "Barclays", "Credit Suisse", "Deutsche Bank", "UBS",
            "BNP Paribas", "Societe Generale", "HSBC", "RBC Capital Markets",
            "Jefferies", "Lazard", "Evercore", "Centerview Partners", "Moelis",
            "Guggenheim Partners", "Greenhill", "Perella Weinberg", "PJT Partners"
        ],
        
        "Asset Managers": [
            "BlackRock", "Vanguard", "State Street", "Fidelity", "JP Morgan Asset Management",
            "BNY Mellon", "Capital Group", "PIMCO", "Invesco", "Wellington Management",
            "T. Rowe Price", "Franklin Templeton", "Schroders", "AllianceBernstein",
            "Nuveen", "Federated Hermes", "Principal", "MFS", "Eaton Vance", "Janus Henderson"
        ],
        
        "Insurance Companies": [
            "Berkshire Hathaway", "Ping An", "Allianz", "AXA", "MetLife",
            "Prudential", "China Life", "Munich Re", "Zurich", "Generali",
            "State Farm", "GEICO", "Progressive", "Allstate", "Liberty Mutual",
            "Farmers", "USAA", "Nationwide", "Travelers", "The Hartford",
            "Chubb", "AIG", "Aflac", "Principal", "Lincoln Financial"
        ],
        
        # REAL ESTATE
        "Real Estate Developers": [
            "Brookfield", "Related Companies", "Tishman Speyer", "Hines", "Lendlease",
            "Skanska", "Bouygues", "Vinci", "China Vanke", "Country Garden",
            "Evergrande", "Greenland Holdings", "Poly Developments", "China Resources Land",
            "Sun Hung Kai Properties", "Henderson Land", "New World Development",
            "CapitaLand", "City Developments", "UOL Group", "Keppel Land"
        ],
        
        "REITs": [
            "American Tower", "Prologis", "Crown Castle", "Equinix", "Public Storage",
            "Welltower", "Simon Property Group", "Realty Income", "Digital Realty",
            "Ventas", "Alexandria", "AvalonBay", "Equity Residential", "Essex",
            "Mid-America", "UDR", "Camden", "Boston Properties", "Vornado", "SL Green"
        ],
        
        # INDUSTRIAL & MANUFACTURING
        "Industrial Conglomerates": [
            "General Electric", "Siemens", "ABB", "Honeywell", "3M",
            "United Technologies", "Raytheon", "Emerson", "Schneider Electric",
            "Eaton", "Parker Hannifin", "Illinois Tool Works", "Ingersoll Rand",
            "Johnson Controls", "Fortive", "Roper Technologies", "Dover",
            "Textron", "Danaher", "Rockwell Automation", "Ametek", "Xylem"
        ],
        
        "Aerospace & Defense": [
            "Boeing", "Airbus", "Lockheed Martin", "Raytheon", "Northrop Grumman",
            "General Dynamics", "BAE Systems", "L3Harris", "Thales", "Leonardo",
            "Safran", "Rolls-Royce", "MTU Aero", "Spirit AeroSystems", "Triumph Group",
            "TransDigm", "Hexcel", "Woodward", "Moog", "Curtiss-Wright",
            "Elbit Systems", "Rafael", "IAI", "Saab", "Rheinmetall"
        ],
        
        # EDUCATION
        "Online Education Platforms": [
            "Coursera", "Udemy", "edX", "Udacity", "Khan Academy",
            "LinkedIn Learning", "Pluralsight", "Skillshare", "MasterClass", "Domestika",
            "FutureLearn", "DataCamp", "Codecademy", "Treehouse", "Brilliant",
            "Duolingo", "Babbel", "Rosetta Stone", "Busuu", "Memrise"
        ],
        
        "Test Prep Companies": [
            "Kaplan", "Princeton Review", "Manhattan Prep", "Magoosh", "PrepScholar",
            "Barron's", "McGraw-Hill", "Pearson", "ETS", "College Board",
            "ACT Inc", "GMAC", "LSAC", "AAMC", "CFA Institute",
            "TestMasters", "PowerScore", "Veritas Prep", "Target Test Prep", "ScoreMore"
        ],
        
        "Educational Publishers": [
            "Pearson", "McGraw-Hill", "Cengage", "Wiley", "Houghton Mifflin Harcourt",
            "Scholastic", "Macmillan", "Oxford University Press", "Cambridge University Press",
            "Elsevier", "Springer", "Taylor & Francis", "SAGE Publications", "Wolters Kluwer"
        ],
        
        # HEALTHCARE
        "Hospital Systems": [
            "HCA Healthcare", "CommonSpirit Health", "Ascension", "Trinity Health",
            "Community Health Systems", "Tenet Healthcare", "Universal Health Services",
            "Providence", "Advocate Aurora", "Atrium Health", "Spectrum Health",
            "Intermountain Healthcare", "Kaiser Permanente", "Sutter Health", "Dignity Health",
            "Mayo Clinic", "Cleveland Clinic", "Johns Hopkins", "Mass General Brigham",
            "NYU Langone", "Mount Sinai", "Cedars-Sinai", "UCLA Health", "UCSF Health"
        ],
        
        "Medical Device Companies": [
            "Medtronic", "Abbott", "Johnson & Johnson", "GE Healthcare", "Siemens Healthineers",
            "Philips Healthcare", "Boston Scientific", "Stryker", "Becton Dickinson",
            "Baxter", "Edwards Lifesciences", "Zimmer Biomet", "Smith & Nephew",
            "Intuitive Surgical", "Danaher", "Thermo Fisher", "Roche Diagnostics",
            "Dexcom", "ResMed", "Align Technology", "Insulet", "Tandem Diabetes"
        ],
        
        "Pharmacy Chains": [
            "CVS", "Walgreens", "Rite Aid", "Boots", "Walmart Pharmacy",
            "Kroger Pharmacy", "Publix Pharmacy", "H-E-B Pharmacy", "Meijer Pharmacy",
            "Costco Pharmacy", "Sam's Club Pharmacy", "Target Pharmacy", "Albertsons Pharmacy",
            "Express Scripts", "OptumRx", "Prime Therapeutics", "Caremark", "MedImpact"
        ],
        
        # LOGISTICS & SUPPLY CHAIN
        "3PL Providers": [
            "DHL Supply Chain", "XPO Logistics", "C.H. Robinson", "DSV", "Kuehne + Nagel",
            "DB Schenker", "Nippon Express", "Expeditors", "UPS Supply Chain", "FedEx Logistics",
            "GEODIS", "CEVA Logistics", "Penske Logistics", "Ryder", "J.B. Hunt",
            "Schneider", "Werner", "Swift", "Knight Transportation", "Landstar"
        ],
        
        "Freight Forwarders": [
            "Flexport", "Freightos", "Forto", "Sennder", "Convoy",
            "Uber Freight", "Echo Global", "Coyote Logistics", "Total Quality Logistics",
            "Transplace", "GlobalTranz", "Mode Transportation", "Arrive Logistics",
            "Redwood Logistics", "BlueGrace Logistics", "Trinity Logistics", "Nolan Transportation"
        ],
        
        # AGRICULTURE & FOOD PRODUCTION
        "Agribusiness Giants": [
            "Cargill", "ADM", "Bunge", "Louis Dreyfus", "COFCO",
            "Wilmar", "Olam", "Glencore Agriculture", "Viterra", "CHS Inc",
            "Nutrien", "Mosaic", "CF Industries", "Yara", "ICL Group",
            "Corteva", "Bayer Crop Science", "Syngenta", "BASF Agricultural", "FMC",
            "John Deere", "AGCO", "CNH Industrial", "Kubota", "Mahindra Tractors"
        ],
        
        "Food Processors": [
            "Tyson Foods", "JBS", "WH Group", "Perdue Farms", "Pilgrim's Pride",
            "Sanderson Farms", "Hormel", "Smithfield Foods", "Maple Leaf Foods",
            "Danish Crown", "Vion", "Tönnies", "BRF", "Marfrig", "Minerva",
            "Fonterra", "Arla Foods", "FrieslandCampina", "Dairy Farmers of America",
            "Land O'Lakes", "Dean Foods", "Saputo", "Lactalis", "Danone", "Yili"
        ],
        
        # UTILITIES
        "Electric Utilities": [
            "NextEra Energy", "Duke Energy", "Southern Company", "Dominion Energy",
            "Exelon", "American Electric Power", "Sempra Energy", "Xcel Energy",
            "ConEd", "PG&E", "Edison International", "Entergy", "FirstEnergy",
            "Eversource", "DTE Energy", "WEC Energy", "CenterPoint", "Ameren",
            "PPL", "CMS Energy", "NiSource", "Alliant Energy", "Evergy"
        ],
        
        "Water Utilities": [
            "American Water", "Veolia", "Suez", "United Utilities", "Severn Trent",
            "Thames Water", "Anglian Water", "Yorkshire Water", "Southern Water",
            "Northumbrian Water", "Essential Utilities", "California Water Service",
            "American States Water", "SJW Group", "Middlesex Water", "York Water"
        ],
        
        # MINING & RESOURCES
        "Mining Companies": [
            "BHP", "Rio Tinto", "Vale", "Glencore", "Anglo American",
            "Freeport-McMoRan", "Newmont", "Barrick Gold", "Agnico Eagle", "Kinross Gold",
            "Gold Fields", "AngloGold Ashanti", "Newcrest", "Polyus", "Polymetal",
            "First Quantum", "Teck Resources", "Alcoa", "Norsk Hydro", "Rusal",
            "Norilsk Nickel", "Antofagasta", "Southern Copper", "Grupo México", "KGHM"
        ],
        
        # EMERGING SECTORS
        "Quantum Computing": [
            "IBM Quantum", "Google Quantum AI", "Microsoft Azure Quantum", "Amazon Braket",
            "Rigetti Computing", "IonQ", "D-Wave", "Quantum Computing Inc", "Xanadu",
            "PsiQuantum", "Silicon Quantum Computing", "Universal Quantum", "Pasqal",
            "Atom Computing", "ColdQuanta", "QuEra Computing", "Quantum Machines"
        ],
        
        "Robotics Companies": [
            "Boston Dynamics", "ABB Robotics", "FANUC", "KUKA", "Yaskawa",
            "Universal Robots", "Rethink Robotics", "Fetch Robotics", "Mobile Industrial Robots",
            "Locus Robotics", "6 River Systems", "Vecna Robotics", "inVia Robotics",
            "Geek+", "GreyOrange", "Clearpath Robotics", "Agility Robotics", "ANYbotics"
        ],
        
        "Vertical Farming": [
            "AeroFarms", "Plenty", "Bowery Farming", "BrightFarms", "AppHarvest",
            "Gotham Greens", "Little Leaf Farms", "80 Acres Farms", "Kalera",
            "Vertical Harvest", "Sky Greens", "Urban Crop Solutions", "InFarm",
            "Agricool", "Growing Underground", "Jones Food Company", "Nordic Harvest"
        ],
        
        "Alternative Protein": [
            "Beyond Meat", "Impossible Foods", "Oatly", "Perfect Day", "Memphis Meats",
            "Mosa Meat", "Aleph Farms", "Future Meat", "Wild Type", "BlueNalu",
            "Finless Foods", "Good Catch", "Sophie's Kitchen", "Ocean Hugger Foods",
            "Eat Just", "Clara Foods", "The Better Meat Co", "Rebellyous Foods"
        ]
    }
    
    return companies

def main():
    print("Loading ALL existing logos...")
    existing = load_all_existing_logos()
    print(f"Found {len(existing)} total existing logos\n")
    
    companies = get_ultra_comprehensive_companies()
    
    all_missing = []
    
    for category, company_list in companies.items():
        missing = []
        for company in company_list:
            normalized = normalize_name(company)
            
            found = False
            for existing_name in existing:
                if normalized in existing_name or existing_name in normalized:
                    found = True
                    break
                if ' ' in normalized:
                    first_word = normalized.split()[0]
                    if len(first_word) > 3 and first_word in existing_name:
                        found = True
                        break
            
            if not found:
                missing.append(company)
                all_missing.append((company, category))
        
        if missing:
            print(f"{category}: {len(missing)}/{len(company_list)} missing")
    
    print(f"\n{'='*60}")
    print(f"TOTAL NICHE/SPECIALIZED MISSING: {len(all_missing)} companies")
    print(f"{'='*60}\n")
    
    # Save the comprehensive list
    with open('/Users/adi/code/socratify/socratify-yolo/logos/niche_missing_800.txt', 'w') as f:
        f.write("# 800+ Niche and Specialized Missing Companies\n\n")
        
        current_cat = ""
        count = 0
        for company, category in all_missing:
            if category != current_cat:
                f.write(f"\n## {category}\n")
                current_cat = category
            f.write(f"{company}\n")
            count += 1
            
            if count >= 800:
                break
    
    print(f"Created niche_missing_800.txt with {min(800, len(all_missing))} companies")

if __name__ == "__main__":
    main()