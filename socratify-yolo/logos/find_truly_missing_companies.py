#!/usr/bin/env python3
"""
Comprehensive analysis to find what we're REALLY missing - be exhaustive!
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
                'enterprises', 'solutions', 'systems', 'services', 'technologies', 'tech',
                'sa', 'ag', 'gmbh', 'bv', 'nv', 'spa', 'srl', 'as', 'ab', 'oy', 'a/s']
    
    for suffix in suffixes:
        name = name.replace(f' {suffix}', '').replace(f'_{suffix}', '')
    
    # Remove special characters and normalize spaces
    name = ''.join(c if c.isalnum() else ' ' for c in name)
    name = ' '.join(name.split())
    
    return name.strip()

def load_all_existing_logos() -> Set[str]:
    """Load ALL existing logo filenames from all directories"""
    existing = set()
    
    # Check all logo directories
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

def get_comprehensive_global_companies() -> Dict[str, List[str]]:
    """Get TRULY comprehensive list of global companies across all sectors and regions"""
    
    companies = {
        # NORTH AMERICA - USA
        "US Fortune 500 Missing": [
            "Berkshire Hathaway", "Johnson & Johnson", "UnitedHealth Group", "Exxon Mobil",
            "CVS Health", "Alphabet", "McKesson", "AmerisourceBergen", "Chevron Corporation",
            "Cardinal Health", "Costco Wholesale", "Cigna", "Marathon Petroleum", "Phillips 66",
            "Valero Energy", "Fannie Mae", "General Electric", "Ford Motor", "Centene",
            "Verizon Communications", "General Motors", "AT&T", "Comcast", "Walgreens Boots Alliance",
            "Elevance Health", "Kroger", "Home Depot", "JPMorgan Chase", "Boeing",
            "Wells Fargo", "Citigroup", "Abbott Laboratories", "Humana", "Raytheon Technologies",
            "Energy Transfer", "HCA Healthcare", "AbbVie", "ConocoPhillips", "Progressive",
            "Albertsons", "Bank of America", "Lowe's", "Lockheed Martin", "StoneX Group",
            "ADM", "FedEx", "TJX Companies", "General Dynamics", "American Express"
        ],
        
        "US Tech Unicorns": [
            "Anduril Industries", "Anthropic", "Canva", "Databricks", "Epic Games",
            "Instacart", "Miro", "OpenAI", "Rippling", "Samsara",
            "ServiceTitan", "Stripe", "Tanium", "Thought Machine", "Toast",
            "Verkada", "Zipline", "Airtable", "Amplitude", "Benchling",
            "Brex", "Carta", "Chime", "Clearco", "Cockroach Labs",
            "Convoy", "Databricks", "Discord", "DoorDash", "Faire",
            "Fanatics", "Figma", "Flexport", "Gong", "Gopuff",
            "Grammarly", "Gusto", "HashiCorp", "Hopin", "Ironclad",
            "Kong", "Lacework", "LaunchDarkly", "Loom", "Lucid",
            "MessageBird", "Mural", "Nextdoor", "Notion", "Outreach",
            "PagerDuty", "Personio", "Pipe", "Plaid", "Podium",
            "Postman", "Rec Room", "Redis Labs", "Relativity Space",
            "Roblox", "Scale AI", "Segment", "Sentry", "Shield AI",
            "Snyk", "Sourcegraph", "SpaceX", "Tekion", "Tempo",
            "TripActions", "Vanta", "Vercel", "Verkada", "Webflow"
        ],
        
        "US Regional Banks & Credit Unions": [
            "Navy Federal Credit Union", "State Employees' Credit Union", "Pentagon Federal Credit Union",
            "SchoolsFirst Federal Credit Union", "Golden 1 Credit Union", "Alliant Credit Union",
            "First Tech Federal Credit Union", "America First Credit Union", "Randolph-Brooks Federal Credit Union",
            "Security Service Federal Credit Union", "Bethpage Federal Credit Union", "Star One Credit Union",
            "Suncoast Credit Union", "BECU", "Logix Federal Credit Union",
            "Silicon Valley Bank", "First Republic Bank", "Signature Bank", "PacWest Bancorp",
            "Western Alliance Bancorporation", "Comerica", "Zions Bancorporation", "First Horizon",
            "Synovus", "Webster Bank", "Associated Banc-Corp", "UMB Financial", "Commerce Bancshares",
            "First National Bank of Omaha", "Pinnacle Financial Partners", "Hancock Whitney",
            "Texas Capital Bancshares", "BankUnited", "East West Bancorp", "SVB Financial"
        ],
        
        "US Retail Chains": [
            "Menards", "Fleet Farm", "Meijer", "H-E-B", "Wegmans",
            "Publix", "WinCo Foods", "Hy-Vee", "ShopRite", "Giant Eagle",
            "Food Lion", "Harris Teeter", "Winn-Dixie", "Save Mart", "Raley's",
            "Big Lots", "Ocean State Job Lot", "Ollie's Bargain Outlet", "Gabriel Brothers",
            "Burlington Coat Factory", "Century 21", "Stein Mart", "Bealls", "Boscov's",
            "Von Maur", "Dillard's", "Belk", "Stage Stores", "Elder-Beerman"
        ],
        
        # CANADA
        "Canadian Companies": [
            "Thomson Reuters", "Alimentation Couche-Tard", "George Weston Limited",
            "Empire Company", "Metro Inc.", "Loblaws", "Canadian Tire", "Hudson's Bay Company",
            "Roots Canada", "Lululemon", "Arc'teryx", "Canada Goose", "Aritzia",
            "MEC", "Tim Hortons", "Second Cup", "Boston Pizza", "Swiss Chalet",
            "Harvey's", "Mary Brown's", "New York Fries", "Pita Pit", "Booster Juice"
        ],
        
        # EUROPE
        "European Industrial Giants": [
            "Airbus", "BAE Systems", "Rolls-Royce Holdings", "Safran", "Thales",
            "Leonardo", "Rheinmetall", "Dassault Aviation", "Naval Group", "Fincantieri",
            "ThyssenKrupp", "Salzgitter", "Voestalpine", "ArcelorMittal", "Outokumpu",
            "SSAB", "Norsk Hydro", "Alcoa", "Constellium", "Novelis",
            "LafargeHolcim", "HeidelbergCement", "CRH", "Buzzi Unicem", "Vicat",
            "Wienerberger", "Imerys", "Saint-Gobain", "Kingspan", "Rockwool"
        ],
        
        "European Banks": [
            "BNP Paribas", "Crédit Agricole", "Société Générale", "Groupe BPCE",
            "Crédit Mutuel", "La Banque Postale", "Deutsche Bank", "Commerzbank",
            "DZ Bank", "KfW", "Landesbank Baden-Württemberg", "BayernLB",
            "UniCredit", "Intesa Sanpaolo", "Banco BPM", "BPER Banca",
            "Banco Santander", "BBVA", "CaixaBank", "Banco Sabadell",
            "ING Group", "Rabobank", "ABN AMRO", "KBC Group",
            "Belfius", "Nordea", "Danske Bank", "SEB", "Swedbank", "Handelsbanken"
        ],
        
        "European Retailers": [
            "Schwarz Group (Lidl/Kaufland)", "Aldi", "Edeka", "Rewe Group",
            "Metro AG", "dm-drogerie markt", "Rossmann", "Müller",
            "MediaMarktSaturn", "Otto Group", "Zalando", "About You",
            "Carrefour", "E.Leclerc", "Intermarché", "Système U",
            "Casino Group", "Auchan", "Decathlon", "Leroy Merlin",
            "Fnac Darty", "El Corte Inglés", "Mercadona", "Eroski",
            "Inditex", "Mango", "Desigual", "Tous", "Pronovias"
        ],
        
        # ASIA-PACIFIC
        "Chinese Tech Giants": [
            "ByteDance", "Tencent", "Alibaba", "Baidu", "JD.com",
            "Meituan", "Pinduoduo", "Xiaomi", "NetEase", "Kuaishou",
            "Didi Chuxing", "Bilibili", "iQIYI", "Youku", "Douyin",
            "WeChat", "QQ", "Alipay", "WeChat Pay", "UnionPay",
            "Huawei", "ZTE", "Oppo", "Vivo", "OnePlus",
            "Lenovo", "Haier", "Midea", "Gree", "TCL",
            "BYD", "Nio", "Xpeng", "Li Auto", "Geely"
        ],
        
        "Japanese Conglomerates": [
            "Mitsubishi Corporation", "Mitsui & Co.", "Itochu", "Marubeni", "Sumitomo Corporation",
            "Sojitz", "Toyota Tsusho", "Kanematsu", "Mitsubishi Heavy Industries",
            "Kawasaki Heavy Industries", "IHI Corporation", "Hitachi", "Toshiba",
            "Panasonic", "Sony", "Sharp", "Fujitsu", "NEC", "Oki Electric",
            "Konica Minolta", "Ricoh", "Canon", "Nikon", "Olympus",
            "Bridgestone", "Yokohama Rubber", "Sumitomo Rubber", "Toyo Tire",
            "AGC Inc.", "Nippon Sheet Glass", "TOTO", "LIXIL", "YKK"
        ],
        
        "Korean Chaebols": [
            "Samsung Group", "SK Group", "LG Group", "Lotte Group", "Hyundai Motor Group",
            "POSCO", "Hanwha Group", "GS Group", "Hyundai Heavy Industries", "Doosan Group",
            "CJ Group", "Shinsegae", "Kumho Asiana", "Hanjin Group", "LS Group",
            "Kolon Industries", "OCI", "Taekwang Group", "Daesung Group", "Booyoung Group",
            "Samsung C&T", "Samsung Engineering", "Samsung SDS", "Samsung Biologics",
            "LG Chem", "LG Energy Solution", "SK Hynix", "SK Innovation", "SK Telecom"
        ],
        
        "Indian Conglomerates": [
            "Reliance Industries", "Tata Group", "Adani Group", "Aditya Birla Group",
            "Mahindra Group", "Larsen & Toubro", "Wipro", "Infosys", "HCL Technologies",
            "Tech Mahindra", "Bharti Enterprises", "Bajaj Group", "Godrej Group",
            "ITC Limited", "Vedanta Resources", "JSW Group", "Essar Group",
            "Piramal Group", "Hinduja Group", "RPG Group", "Murugappa Group",
            "TVS Group", "Kirloskar Group", "Future Group", "Raymond Group"
        ],
        
        "Southeast Asian Giants": [
            "CP Group (Thailand)", "PTT (Thailand)", "Siam Cement Group", "Central Group",
            "True Corporation", "Thai Beverage", "Bangkok Bank", "Kasikornbank",
            "Siam Commercial Bank", "Krung Thai Bank", "Wilmar International (Singapore)",
            "Olam International", "Keppel Corporation", "Sembcorp", "CapitaLand",
            "Jardine Matheson", "DFI Retail Group", "Mandarin Oriental", "Dairy Farm",
            "San Miguel Corporation (Philippines)", "SM Investments", "Ayala Corporation",
            "JG Summit", "Aboitiz Group", "PLDT", "Globe Telecom", "Jollibee Foods",
            "Lippo Group (Indonesia)", "Sinar Mas", "Salim Group", "Astra International"
        ],
        
        "Australian Companies": [
            "BHP", "Rio Tinto", "Fortescue Metals", "Woodside Petroleum", "Santos",
            "Commonwealth Bank", "Westpac", "ANZ Bank", "National Australia Bank",
            "Macquarie Group", "QBE Insurance", "Suncorp Group", "Insurance Australia Group",
            "Woolworths Group", "Coles Group", "Wesfarmers", "Harvey Norman", "JB Hi-Fi",
            "Telstra", "Optus", "TPG Telecom", "Qantas", "Virgin Australia",
            "Transurban", "Lendlease", "Stockland", "Mirvac", "Goodman Group"
        ],
        
        # LATIN AMERICA
        "Mexican Companies": [
            "América Móvil", "Grupo Carso", "Grupo México", "Cemex", "FEMSA",
            "Grupo Modelo", "Grupo Bimbo", "Televisa", "TV Azteca", "Grupo Salinas",
            "Arca Continental", "Alfa", "Banorte", "Grupo Financiero Inbursa",
            "Cinépolis", "Alsea", "Liverpool", "Palacio de Hierro", "Sanborns",
            "Oxxo", "7-Eleven México", "Circle K México", "Soriana", "Chedraui"
        ],
        
        "Brazilian Companies": [
            "Petrobras", "Vale", "Itaú Unibanco", "Banco Bradesco", "Banco do Brasil",
            "AmBev", "JBS", "BRF", "Marfrig", "Minerva Foods",
            "WEG", "Embraer", "Gerdau", "CSN", "Usiminas",
            "Suzano", "Klabin", "Braskem", "Ultra", "Cosan",
            "Natura &Co", "O Boticário", "Magazine Luiza", "Via Varejo", "Lojas Americanas",
            "GPA", "Carrefour Brasil", "Assaí", "Raia Drogasil", "DPSP"
        ],
        
        "Other Latin American": [
            "Ecopetrol (Colombia)", "Grupo Argos", "Avianca", "Bancolombia", "Grupo Nutresa",
            "LATAM Airlines (Chile)", "Cencosud", "Falabella", "Banco de Chile", "ENAP",
            "YPF (Argentina)", "Mercado Libre", "Globant", "Tenaris", "Adecoagro",
            "Copa Airlines (Panama)", "Banco General", "Cable & Wireless Panama",
            "Grupo Financiero Banorte", "Banco Nacional de Costa Rica"
        ],
        
        # MIDDLE EAST & AFRICA
        "Middle Eastern Companies": [
            "Saudi Aramco", "SABIC", "Saudi Telecom Company", "Mobily", "Zain Saudi",
            "Saudi Electricity Company", "Ma'aden", "Yanbu Aramco Sinopec", "SAFCO",
            "Almarai", "Savola Group", "Jarir Marketing", "Extra Stores", "Panda Retail",
            "Emirates Group", "Etisalat", "du", "ADNOC", "Mubadala",
            "Dubai Holding", "Emaar Properties", "Dubai World", "DP World", "DAMAC",
            "Qatar Petroleum", "Qatar Airways", "Ooredoo", "Qatar National Bank",
            "Industries Qatar", "Qatar Islamic Bank", "Masraf Al Rayan",
            "National Bank of Kuwait", "Kuwait Finance House", "Zain Kuwait"
        ],
        
        "African Companies": [
            "Sonatrach (Algeria)", "OCP Group (Morocco)", "Attijariwafa Bank", "Royal Air Maroc",
            "Maroc Telecom", "Egypt Telecom", "Commercial International Bank Egypt", "Orascom",
            "MTN Group", "Vodacom", "Cell C", "Telkom SA", "MultiChoice",
            "Naspers", "Prosus", "Standard Bank", "FirstRand", "Absa Group",
            "Nedbank", "Investec", "Old Mutual", "Sanlam", "Discovery",
            "Shoprite", "Pick n Pay", "Woolworths", "Clicks", "Dis-Chem",
            "Sasol", "Anglo American", "Gold Fields", "Harmony Gold", "Sibanye-Stillwater",
            "Dangote Group (Nigeria)", "Access Bank", "Zenith Bank", "GTBank", "UBA"
        ],
        
        # SPECIALIZED SECTORS
        "Global Shipping Lines": [
            "Maersk", "MSC", "CMA CGM", "COSCO", "Hapag-Lloyd",
            "ONE", "Evergreen", "Yang Ming", "HMM", "Zim",
            "PIL", "Wan Hai Lines", "X-Press Feeders", "Matson", "OOCL",
            "NYK Line", "MOL", "K Line", "Hamburg Süd", "Safmarine"
        ],
        
        "Global Logistics": [
            "DHL", "FedEx", "UPS", "TNT", "DB Schenker",
            "Kuehne + Nagel", "DSV", "C.H. Robinson", "XPO Logistics", "Expeditors",
            "GEODIS", "Bolloré Logistics", "DACHSER", "Nippon Express", "Yusen Logistics",
            "Kerry Logistics", "Agility", "CEVA Logistics", "Panalpina", "Hellmann Worldwide"
        ],
        
        "Global Law Firms": [
            "Kirkland & Ellis", "Latham & Watkins", "DLA Piper", "Baker McKenzie", "Dentons",
            "Skadden", "Clifford Chance", "Allen & Overy", "Linklaters", "Freshfields",
            "White & Case", "Jones Day", "Hogan Lovells", "Norton Rose Fulbright", "CMS",
            "Sidley Austin", "Gibson Dunn", "Simpson Thacher", "Davis Polk", "Sullivan & Cromwell",
            "Weil Gotshal", "Paul Weiss", "Cravath", "Cleary Gottlieb", "Debevoise & Plimpton"
        ],
        
        "Global Accounting Firms": [
            "PwC", "Deloitte", "EY", "KPMG", "Grant Thornton",
            "BDO", "RSM", "Mazars", "Baker Tilly", "Crowe",
            "Moore Global", "HLB International", "Nexia", "PKF", "UHY",
            "MGI Worldwide", "AGN International", "PrimeGlobal", "Allinial Global", "BKR International"
        ],
        
        "Private Equity Mega Funds": [
            "Blackstone", "KKR", "EQT", "Thoma Bravo", "Silver Lake",
            "TPG", "Warburg Pincus", "Carlyle", "Apollo", "Ares",
            "CVC Capital", "Advent International", "Bain Capital", "Permira", "Nordic Capital",
            "Cinven", "Bridgepoint", "Apax Partners", "General Atlantic", "Vista Equity"
        ],
        
        "Sovereign Wealth Funds": [
            "Norway Government Pension Fund", "China Investment Corporation", "ADIA", "Kuwait Investment Authority",
            "GIC Singapore", "Temasek", "Qatar Investment Authority", "Mubadala", "PIF Saudi Arabia",
            "RDIF Russia", "National Wealth Fund Russia", "Samruk-Kazyna", "Khazanah Malaysia",
            "Future Fund Australia", "NZ Super Fund", "Alaska Permanent Fund", "CalPERS", "CalSTRS",
            "CPPIB", "CDPQ", "OMERS", "Ontario Teachers", "ABP Netherlands"
        ],
        
        "Global Hotel Chains": [
            "Marriott International", "Hilton Worldwide", "IHG", "Wyndham", "Choice Hotels",
            "Accor", "Hyatt", "Radisson Hotel Group", "Best Western", "BWH Hotel Group",
            "Jin Jiang", "Huazhu", "BTG Homeinns", "OYO", "RedDoorz",
            "Meliá Hotels", "NH Hotel Group", "Barceló", "Iberostar", "RIU Hotels",
            "Kempinski", "Jumeirah", "Rotana", "Shangri-La", "Mandarin Oriental"
        ],
        
        "Global Airlines": [
            "American Airlines", "Delta Air Lines", "United Airlines", "Southwest Airlines", "Alaska Airlines",
            "Air Canada", "WestJet", "Aeroméxico", "Copa Airlines", "Avianca",
            "LATAM", "Gol", "Azul", "British Airways", "Lufthansa",
            "Air France-KLM", "IAG", "Ryanair", "easyJet", "Wizz Air",
            "Turkish Airlines", "Emirates", "Qatar Airways", "Etihad", "Saudia",
            "EgyptAir", "Royal Air Maroc", "Ethiopian Airlines", "Kenya Airways", "South African Airways",
            "Air India", "IndiGo", "SpiceJet", "AirAsia", "Singapore Airlines",
            "Cathay Pacific", "ANA", "JAL", "Korean Air", "Asiana Airlines",
            "China Southern", "China Eastern", "Air China", "Hainan Airlines", "Qantas"
        ],
        
        "Streaming & Digital Media": [
            "Netflix", "Disney+", "Hulu", "HBO Max", "Paramount+",
            "Peacock", "Apple TV+", "Amazon Prime Video", "YouTube TV", "Sling TV",
            "fuboTV", "Philo", "Discovery+", "ESPN+", "DAZN",
            "Spotify", "Apple Music", "Amazon Music", "YouTube Music", "Tidal",
            "Deezer", "SoundCloud", "Pandora", "iHeartRadio", "TuneIn",
            "Twitch", "YouTube", "TikTok", "Instagram", "Snapchat"
        ],
        
        "Gaming Companies": [
            "Tencent Games", "Sony Interactive", "Microsoft Gaming", "Nintendo", "Activision Blizzard",
            "Electronic Arts", "Take-Two Interactive", "Ubisoft", "Epic Games", "Valve",
            "Roblox", "Unity", "Embracer Group", "CD Projekt", "Paradox Interactive",
            "Bandai Namco", "Square Enix", "Capcom", "Sega", "Konami",
            "NetEase Games", "miHoYo", "Garena", "Nexon", "NCSoft",
            "Supercell", "King", "Zynga", "Scopely", "Playrix"
        ],
        
        "Cryptocurrency Exchanges": [
            "Binance", "Coinbase", "Kraken", "Bitfinex", "Huobi",
            "OKX", "KuCoin", "Bybit", "Gate.io", "Crypto.com",
            "Gemini", "Bitstamp", "Bittrex", "Poloniex", "BitMEX",
            "Deribit", "FTX", "BlockFi", "Celsius", "Nexo",
            "Paxos", "Circle", "Tether", "MicroStrategy", "Galaxy Digital"
        ],
        
        "Electric Vehicle Companies": [
            "Tesla", "Rivian", "Lucid Motors", "Fisker", "Canoo",
            "Lordstown Motors", "Nikola", "Arrival", "Proterra", "Lion Electric",
            "BYD", "Nio", "Xpeng", "Li Auto", "Geely",
            "Polestar", "Volkswagen ID", "Mercedes EQ", "BMW i", "Audi e-tron",
            "Porsche Taycan", "Ford Mustang Mach-E", "GM Ultium", "Stellantis STLA", "Hyundai Ioniq"
        ],
        
        "Space Companies": [
            "SpaceX", "Blue Origin", "Virgin Galactic", "Rocket Lab", "Relativity Space",
            "Firefly Aerospace", "Astra", "ABL Space Systems", "Momentus", "Orbit Fab",
            "Planet Labs", "Spire Global", "BlackSky", "Capella Space", "ICEYE",
            "Maxar Technologies", "L3Harris", "Ball Aerospace", "Northrop Grumman Space", "Boeing Space",
            "Airbus Defence and Space", "Thales Alenia Space", "OHB", "AVIO", "ArianeGroup"
        ],
        
        "Renewable Energy Companies": [
            "NextEra Energy", "Enel Green Power", "Iberdrola", "Ørsted", "EDP Renewables",
            "Vestas", "Siemens Gamesa", "GE Renewable Energy", "Goldwind", "Envision Energy",
            "First Solar", "SunPower", "Canadian Solar", "JinkoSolar", "LONGi Solar",
            "Enphase Energy", "SolarEdge", "Sunrun", "Sunnova", "Vivint Solar",
            "ChargePoint", "EVgo", "Electrify America", "Ionity", "Fastned"
        ],
        
        "Biotech & Pharma": [
            "Roche", "Novartis", "Pfizer", "Johnson & Johnson", "Merck",
            "AbbVie", "Bristol-Myers Squibb", "Sanofi", "GSK", "AstraZeneca",
            "Eli Lilly", "Amgen", "Gilead Sciences", "Moderna", "BioNTech",
            "Regeneron", "Vertex", "Biogen", "CSL", "Novo Nordisk",
            "Takeda", "Astellas", "Daiichi Sankyo", "Otsuka", "Eisai",
            "Bayer", "Boehringer Ingelheim", "Merck KGaA", "Teva", "Mylan"
        ],
        
        "Food & Beverage Giants": [
            "Nestlé", "PepsiCo", "Coca-Cola", "Unilever", "Mondelez",
            "Danone", "General Mills", "Kellogg's", "Mars", "Ferrero",
            "Kraft Heinz", "ConAgra", "Campbell Soup", "J.M. Smucker", "Hormel Foods",
            "Tyson Foods", "JBS", "WH Group", "BRF", "Perdue Farms",
            "Lactalis", "Arla Foods", "FrieslandCampina", "Fonterra", "Yili",
            "Mengniu", "Bright Food", "Want Want", "Uni-President", "Master Kong"
        ]
    }
    
    return companies

def check_if_missing(company: str, existing: Set[str]) -> bool:
    """Check if a company is actually missing"""
    normalized = normalize_name(company)
    
    # Direct match
    if normalized in existing:
        return False
    
    # Check partial matches
    for existing_name in existing:
        # If the normalized name is contained in existing
        if normalized in existing_name or existing_name in normalized:
            return False
        
        # Check if first word matches (for companies with multiple words)
        if ' ' in normalized:
            first_word = normalized.split()[0]
            if len(first_word) > 3 and first_word in existing_name:
                return False
    
    return True

def main():
    print("Loading ALL existing logos from all directories...")
    existing = load_all_existing_logos()
    print(f"Found {len(existing)} total existing logo files\n")
    
    print("Analyzing comprehensive global company list...")
    companies = get_comprehensive_global_companies()
    
    all_missing = []
    category_stats = {}
    
    for category, company_list in companies.items():
        missing_in_category = []
        for company in company_list:
            if check_if_missing(company, existing):
                missing_in_category.append(company)
                all_missing.append((company, category))
        
        category_stats[category] = {
            'total': len(company_list),
            'missing': len(missing_in_category),
            'companies': missing_in_category
        }
        
        if missing_in_category:
            print(f"{category}: {len(missing_in_category)}/{len(company_list)} missing")
    
    print(f"\n{'='*60}")
    print(f"TOTAL MISSING: {len(all_missing)} companies")
    print(f"{'='*60}\n")
    
    # Save comprehensive results
    with open('/Users/adi/code/socratify/socratify-yolo/logos/comprehensive_missing_analysis.json', 'w') as f:
        json.dump({
            'total_existing': len(existing),
            'total_checked': sum(s['total'] for s in category_stats.values()),
            'total_missing': len(all_missing),
            'categories': category_stats
        }, f, indent=2)
    
    # Create downloadable list of 800+ companies
    with open('/Users/adi/code/socratify/socratify-yolo/logos/missing_800_plus_companies.txt', 'w') as f:
        f.write("# 800+ Actually Missing Global Companies\n\n")
        
        # Group by region for better organization
        regions = {
            'North America': [],
            'Europe': [],
            'Asia-Pacific': [],
            'Latin America': [],
            'Middle East & Africa': [],
            'Global/Specialized': []
        }
        
        for company, category in all_missing:
            if any(x in category for x in ['US ', 'Canadian', 'Fortune 500']):
                regions['North America'].append((company, category))
            elif any(x in category for x in ['European', 'German', 'French', 'British']):
                regions['Europe'].append((company, category))
            elif any(x in category for x in ['Chinese', 'Japanese', 'Korean', 'Indian', 'Southeast', 'Australian']):
                regions['Asia-Pacific'].append((company, category))
            elif any(x in category for x in ['Mexican', 'Brazilian', 'Latin American']):
                regions['Latin America'].append((company, category))
            elif any(x in category for x in ['Middle Eastern', 'African']):
                regions['Middle East & Africa'].append((company, category))
            else:
                regions['Global/Specialized'].append((company, category))
        
        count = 0
        for region, companies in regions.items():
            if companies:
                f.write(f"\n## {region}\n\n")
                current_category = ""
                for company, category in companies:
                    if category != current_category:
                        f.write(f"\n### {category}\n")
                        current_category = category
                    f.write(f"{company}\n")
                    count += 1
                    
                    if count >= 800:
                        break
            if count >= 800:
                break
    
    print(f"Analysis complete! Files created:")
    print(f"1. comprehensive_missing_analysis.json - Full detailed analysis")
    print(f"2. missing_800_plus_companies.txt - List of 800+ missing companies for download")
    
    # Print top missing by category
    print(f"\nTop categories with most missing companies:")
    sorted_cats = sorted(category_stats.items(), key=lambda x: x[1]['missing'], reverse=True)
    for cat, stats in sorted_cats[:10]:
        if stats['missing'] > 0:
            print(f"  {cat}: {stats['missing']} missing")

if __name__ == "__main__":
    main()