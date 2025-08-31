#!/usr/bin/env python3
"""
THE FINAL PUSH TO 10,000 LOGOS - Everything we're still missing!
"""

def get_final_10000_companies():
    return {
        # INTERNATIONAL GIANTS (NON-ENGLISH)
        "Chinese Tech & Commerce": [
            "Tencent", "Alibaba", "Baidu", "JD.com", "Meituan", "ByteDance", "TikTok", "Douyin",
            "Xiaomi", "Huawei", "Oppo", "Vivo", "OnePlus", "Realme", "Honor",
            "BYD", "Nio", "Xpeng", "Li Auto", "Geely", "Great Wall Motors", "Changan",
            "Pinduoduo", "Kuaishou", "Bilibili", "NetEase", "Sina Weibo", "Sohu", "Toutiao",
            "Didi Chuxing", "Ele.me", "Cainiao", "Ant Group", "WeChat Pay", "Alipay",
            "China Mobile", "China Telecom", "China Unicom", "ZTE", "Lenovo", "TCL"
        ],
        
        "Japanese Corporations": [
            "Toyota", "Honda", "Nissan", "Mazda", "Subaru", "Suzuki", "Mitsubishi Motors",
            "Sony", "Panasonic", "Sharp", "Toshiba", "Hitachi", "Fujitsu", "NEC",
            "Nintendo", "Sega", "Bandai Namco", "Konami", "Capcom", "Square Enix",
            "SoftBank", "Rakuten", "Line Corporation", "Mercari", "DMM", "CyberAgent",
            "Seven & i Holdings", "FamilyMart", "Lawson", "Ministop", "Aeon", "Ito-Yokado",
            "Mitsubishi UFJ", "Sumitomo Mitsui", "Mizuho", "Nomura", "Daiwa Securities",
            "All Nippon Airways", "Japan Airlines", "JR East", "JR Central", "JR West"
        ],
        
        "Korean Companies": [
            "Samsung Electronics", "Samsung C&T", "Samsung SDI", "Samsung SDS", "Samsung Heavy",
            "LG Electronics", "LG Chem", "LG Display", "LG Energy Solution", "LG Innotek",
            "SK Hynix", "SK Telecom", "SK Innovation", "SK Energy", "SK Chemicals",
            "Hyundai Motor", "Kia", "Genesis", "Hyundai Mobis", "Hyundai Heavy Industries",
            "Lotte Group", "Lotte Chemical", "Lotte Shopping", "Lotte Confectionery",
            "CJ Group", "CJ CheilJedang", "CJ Logistics", "CJ ENM", "CJ Olive Networks",
            "Naver", "Kakao", "Coupang", "Baemin", "Toss", "Krafton", "NCSoft", "Nexon"
        ],
        
        "European Hidden Champions": [
            "Bosch", "Siemens", "ThyssenKrupp", "BASF", "Bayer", "Continental", "SAP",
            "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Porsche", "MAN", "Scania",
            "Airbus", "Safran", "Thales", "Leonardo", "BAE Systems", "Rolls-Royce",
            "Nestle", "Novartis", "Roche", "ABB", "Glencore", "Trafigura", "Vitol",
            "Shell", "BP", "TotalEnergies", "Eni", "Repsol", "Equinor", "OMV",
            "Carrefour", "Auchan", "Casino", "E.Leclerc", "Intermarche", "Lidl", "Aldi"
        ],
        
        "Indian Giants": [
            "Reliance Industries", "Reliance Jio", "Reliance Retail", "Reliance Energy",
            "Tata Motors", "Tata Steel", "Tata Consultancy", "Tata Power", "Titan",
            "Adani Enterprises", "Adani Ports", "Adani Green Energy", "Adani Power",
            "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "L&T Infotech",
            "State Bank of India", "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra",
            "Bharti Airtel", "Vodafone Idea", "BSNL", "Jio", "Vi",
            "Maruti Suzuki", "Mahindra", "Bajaj Auto", "Hero MotoCorp", "TVS Motors"
        ],
        
        # HISTORICAL/DEFUNCT COMPANIES
        "Dead But Important": [
            "Blockbuster", "Circuit City", "RadioShack", "Borders Books", "Tower Records",
            "Toys R Us", "Babies R Us", "Sports Authority", "Payless ShoeSource", "Gymboree",
            "Lehman Brothers", "Bear Stearns", "Washington Mutual", "Wachovia", "Countrywide",
            "Arthur Andersen", "Enron", "WorldCom", "Adelphia", "Tyco International",
            "Pan Am", "TWA", "Eastern Air Lines", "Continental Airlines", "US Airways",
            "Northwest Airlines", "America West", "AirTran", "Virgin America", "Midwest Airlines",
            "Compaq", "Sun Microsystems", "Palm", "BlackBerry", "Motorola Mobility",
            "Netscape", "AOL", "Yahoo!", "AltaVista", "Friendster", "MySpace", "Vine"
        ],
        
        # SPORTS TEAMS & LEAGUES
        "NFL Teams": [
            "Dallas Cowboys", "New England Patriots", "Los Angeles Rams", "New York Giants",
            "Chicago Bears", "Green Bay Packers", "San Francisco 49ers", "Las Vegas Raiders",
            "Philadelphia Eagles", "Washington Commanders", "New York Jets", "Miami Dolphins",
            "Buffalo Bills", "Kansas City Chiefs", "Denver Broncos", "Los Angeles Chargers",
            "Seattle Seahawks", "Arizona Cardinals", "Minnesota Vikings", "Detroit Lions",
            "Tampa Bay Buccaneers", "New Orleans Saints", "Atlanta Falcons", "Carolina Panthers",
            "Pittsburgh Steelers", "Baltimore Ravens", "Cleveland Browns", "Cincinnati Bengals",
            "Houston Texans", "Indianapolis Colts", "Tennessee Titans", "Jacksonville Jaguars"
        ],
        
        "NBA Teams": [
            "Los Angeles Lakers", "Boston Celtics", "Golden State Warriors", "Chicago Bulls",
            "Miami Heat", "San Antonio Spurs", "Philadelphia 76ers", "New York Knicks",
            "Brooklyn Nets", "Los Angeles Clippers", "Phoenix Suns", "Milwaukee Bucks",
            "Denver Nuggets", "Dallas Mavericks", "Houston Rockets", "Portland Trail Blazers",
            "Utah Jazz", "Oklahoma City Thunder", "Memphis Grizzlies", "New Orleans Pelicans",
            "Sacramento Kings", "Minnesota Timberwolves", "Atlanta Hawks", "Charlotte Hornets",
            "Washington Wizards", "Indiana Pacers", "Detroit Pistons", "Cleveland Cavaliers",
            "Toronto Raptors", "Orlando Magic"
        ],
        
        "MLB Teams": [
            "New York Yankees", "Boston Red Sox", "Los Angeles Dodgers", "Chicago Cubs",
            "St. Louis Cardinals", "San Francisco Giants", "Philadelphia Phillies", "New York Mets",
            "Atlanta Braves", "Houston Astros", "Washington Nationals", "Oakland Athletics",
            "Los Angeles Angels", "San Diego Padres", "Seattle Mariners", "Texas Rangers",
            "Toronto Blue Jays", "Baltimore Orioles", "Tampa Bay Rays", "Chicago White Sox",
            "Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins",
            "Milwaukee Brewers", "Cincinnati Reds", "Pittsburgh Pirates", "Colorado Rockies",
            "Arizona Diamondbacks", "Miami Marlins"
        ],
        
        "NHL Teams": [
            "Montreal Canadiens", "Toronto Maple Leafs", "Boston Bruins", "New York Rangers",
            "Chicago Blackhawks", "Detroit Red Wings", "Pittsburgh Penguins", "Philadelphia Flyers",
            "Edmonton Oilers", "Colorado Avalanche", "New Jersey Devils", "New York Islanders",
            "Tampa Bay Lightning", "Washington Capitals", "Calgary Flames", "Vancouver Canucks",
            "St. Louis Blues", "Dallas Stars", "Los Angeles Kings", "San Jose Sharks",
            "Anaheim Ducks", "Vegas Golden Knights", "Seattle Kraken", "Minnesota Wild",
            "Winnipeg Jets", "Nashville Predators", "Carolina Hurricanes", "Florida Panthers",
            "Columbus Blue Jackets", "Ottawa Senators", "Buffalo Sabres", "Arizona Coyotes"
        ],
        
        "Soccer Clubs": [
            "Manchester United", "Liverpool", "Arsenal", "Chelsea", "Manchester City",
            "Tottenham Hotspur", "Leicester City", "West Ham United", "Everton", "Newcastle United",
            "Real Madrid", "Barcelona", "Atletico Madrid", "Sevilla", "Valencia",
            "Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Bayer Leverkusen", "Schalke 04",
            "Juventus", "AC Milan", "Inter Milan", "AS Roma", "Napoli",
            "Paris Saint-Germain", "Olympique Marseille", "Lyon", "Monaco", "Lille",
            "Ajax", "PSV Eindhoven", "Feyenoord", "Benfica", "Porto", "Sporting CP",
            "Celtic", "Rangers", "Galatasaray", "Fenerbahce", "Besiktas"
        ],
        
        # NGOs & NONPROFITS
        "Major Charities": [
            "Red Cross", "Red Crescent", "United Way", "Salvation Army", "Goodwill",
            "Habitat for Humanity", "Make-A-Wish", "St. Jude Children's Research Hospital",
            "Doctors Without Borders", "CARE International", "Oxfam", "Save the Children",
            "World Vision", "Feed the Children", "Feeding America", "Food Bank",
            "American Cancer Society", "American Heart Association", "March of Dimes",
            "Susan G. Komen", "Leukemia & Lymphoma Society", "Alzheimer's Association"
        ],
        
        "Foundations": [
            "Bill & Melinda Gates Foundation", "Ford Foundation", "Robert Wood Johnson Foundation",
            "W.K. Kellogg Foundation", "MacArthur Foundation", "Rockefeller Foundation",
            "Carnegie Foundation", "Open Society Foundations", "Clinton Foundation",
            "Carter Center", "Obama Foundation", "Bush Foundation", "Reagan Foundation",
            "Chan Zuckerberg Initiative", "Walton Family Foundation", "Bloomberg Philanthropies",
            "Howard Hughes Medical Institute", "Wellcome Trust", "Novo Nordisk Foundation"
        ],
        
        "Advocacy Groups": [
            "ACLU", "Human Rights Watch", "Amnesty International", "Human Rights Campaign",
            "NAACP", "National Urban League", "Anti-Defamation League", "Southern Poverty Law Center",
            "NRA", "Brady Campaign", "Everytown for Gun Safety", "Moms Demand Action",
            "Sierra Club", "Greenpeace", "NRDC", "Environmental Defense Fund",
            "PETA", "ASPCA", "Humane Society", "WWF", "National Audubon Society",
            "Planned Parenthood", "NARAL", "National Right to Life", "Focus on the Family"
        ],
        
        # RELIGIOUS ORGANIZATIONS
        "Religious Organizations": [
            "Vatican", "Catholic Church", "Episcopal Church", "Methodist Church",
            "Baptist Convention", "Presbyterian Church", "Lutheran Church", "Assemblies of God",
            "LDS Church", "Jehovah's Witnesses", "Seventh-day Adventist", "Scientology",
            "Hillsong Church", "Lakewood Church", "Saddleback Church", "Life.Church",
            "North Point Ministries", "Elevation Church", "Gateway Church", "Willow Creek"
        ],
        
        "Religious Schools": [
            "Liberty University", "Brigham Young University", "Notre Dame", "Georgetown",
            "Boston College", "Villanova", "Fordham", "Marquette", "Loyola Chicago",
            "Baylor", "TCU", "SMU", "Pepperdine", "Gonzaga", "Creighton",
            "Yeshiva University", "Brandeis", "Bob Jones University", "Oral Roberts",
            "Regent University", "Biola University", "Wheaton College", "Calvin University"
        ],
        
        # HEALTHCARE SYSTEMS
        "Major Hospital Systems": [
            "Mayo Clinic", "Cleveland Clinic", "Johns Hopkins Medicine", "Mass General Brigham",
            "NYU Langone", "Mount Sinai", "Cedars-Sinai", "UCLA Health", "UCSF Health",
            "Stanford Health Care", "Duke Health", "Emory Healthcare", "Vanderbilt Health",
            "Northwestern Medicine", "University of Chicago Medicine", "UPMC", "Penn Medicine",
            "Jefferson Health", "Northwell Health", "NewYork-Presbyterian", "Memorial Sloan Kettering",
            "MD Anderson", "Dana-Farber", "St. Jude Children's Research Hospital"
        ],
        
        "Hospital Chains": [
            "HCA Healthcare", "CommonSpirit Health", "Ascension", "Trinity Health",
            "Providence", "Advocate Aurora", "Atrium Health", "Spectrum Health",
            "Intermountain Healthcare", "Kaiser Permanente", "Sutter Health", "Dignity Health",
            "Tenet Healthcare", "Community Health Systems", "Universal Health Services",
            "LifePoint Health", "Prime Healthcare", "Steward Health Care"
        ],
        
        # EDUCATION SYSTEMS
        "School Districts": [
            "New York City Public Schools", "Los Angeles Unified", "Chicago Public Schools",
            "Miami-Dade County Public Schools", "Clark County School District", "Broward County Public Schools",
            "Houston Independent School District", "Hillsborough County Public Schools", "Orange County Public Schools",
            "Hawaii Department of Education", "Fairfax County Public Schools", "Philadelphia School District",
            "San Diego Unified", "Dallas Independent School District", "Charlotte-Mecklenburg Schools"
        ],
        
        "Charter Networks": [
            "KIPP", "Success Academy", "IDEA Public Schools", "Uncommon Schools",
            "Achievement First", "Aspire Public Schools", "Green Dot Public Schools",
            "YES Prep", "Uplift Education", "Noble Network", "Mastery Charter Schools",
            "Rocketship Public Schools", "Alliance College-Ready Public Schools"
        ],
        
        "Private School Networks": [
            "Catholic Schools", "Montessori Schools", "Waldorf Schools", "International Schools",
            "British Schools", "French Schools", "German Schools", "Japanese Schools",
            "Phillips Academy", "Phillips Exeter", "Choate Rosemary Hall", "Deerfield Academy",
            "Hotchkiss School", "Lawrenceville School", "St. Paul's School", "Groton School"
        ],
        
        # UTILITIES BY REGION
        "Electric Utilities": [
            "Con Edison", "Pacific Gas & Electric", "Southern California Edison", "Florida Power & Light",
            "Duke Energy", "Southern Company", "Dominion Energy", "American Electric Power",
            "Exelon", "NextEra Energy", "Sempra Energy", "Xcel Energy", "WEC Energy",
            "DTE Energy", "Eversource", "National Grid", "PPL Corporation", "FirstEnergy",
            "Entergy", "CenterPoint Energy", "Ameren", "CMS Energy", "Alliant Energy"
        ],
        
        "Water Utilities": [
            "American Water", "California Water Service", "Aqua America", "United Water",
            "SUEZ Water", "Veolia Water", "NYC Water", "LA Department of Water", "Chicago Water",
            "Philadelphia Water", "DC Water", "Boston Water", "Denver Water", "Seattle Public Utilities",
            "San Francisco PUC", "East Bay MUD", "Metropolitan Water District", "Miami-Dade Water"
        ],
        
        "Natural Gas": [
            "Dominion Energy", "National Grid", "NiSource", "Atmos Energy", "ONE Gas",
            "Spire", "Southwest Gas", "Northwest Natural", "UGI Corporation", "New Jersey Natural Gas",
            "CenterPoint Energy", "Southern California Gas", "Pacific Gas & Electric", "Peoples Gas"
        ],
        
        # CRYPTO/DEFI EXPANSION
        "Blockchain Projects": [
            "Bitcoin", "Ethereum", "Binance Smart Chain", "Solana", "Cardano", "Polkadot",
            "Avalanche", "Polygon", "Arbitrum", "Optimism", "Cosmos", "Near Protocol",
            "Algorand", "Tezos", "EOS", "TRON", "Stellar", "Ripple", "Hedera",
            "Internet Computer", "Filecoin", "Chainlink", "The Graph", "Arweave"
        ],
        
        "DeFi Protocols": [
            "Uniswap", "SushiSwap", "PancakeSwap", "Curve Finance", "Balancer",
            "Aave", "Compound", "MakerDAO", "Synthetix", "Yearn Finance",
            "1inch", "dYdX", "GMX", "Lido", "Rocket Pool", "Convex Finance",
            "Frax", "Olympus DAO", "Wonderland", "Abracadabra", "Spell Token"
        ],
        
        "NFT Projects": [
            "CryptoPunks", "Bored Ape Yacht Club", "Mutant Ape Yacht Club", "Azuki", "Doodles",
            "Clone X", "Moonbirds", "Cool Cats", "World of Women", "VeeFriends",
            "Art Blocks", "Pudgy Penguins", "Meebits", "CryptoKitties", "NBA Top Shot"
        ],
        
        # GOVERNMENT ENTITIES
        "US Federal Departments": [
            "Department of Defense", "Department of State", "Department of Treasury", "Department of Justice",
            "Department of Interior", "Department of Agriculture", "Department of Commerce", "Department of Labor",
            "Department of Health and Human Services", "Department of Housing and Urban Development",
            "Department of Transportation", "Department of Energy", "Department of Education",
            "Department of Veterans Affairs", "Department of Homeland Security"
        ],
        
        "US Federal Agencies": [
            "FBI", "CIA", "NSA", "DEA", "ATF", "Secret Service", "US Marshals",
            "FDA", "CDC", "NIH", "EPA", "NASA", "NOAA", "USGS",
            "FCC", "FTC", "SEC", "CFTC", "FDIC", "Federal Reserve",
            "IRS", "Social Security Administration", "Medicare", "Medicaid"
        ],
        
        "State Governments": [
            "California", "Texas", "Florida", "New York", "Pennsylvania",
            "Illinois", "Ohio", "Georgia", "North Carolina", "Michigan",
            "New Jersey", "Virginia", "Washington", "Arizona", "Massachusetts",
            "Tennessee", "Indiana", "Missouri", "Maryland", "Wisconsin",
            "Colorado", "Minnesota", "South Carolina", "Alabama", "Louisiana",
            "Kentucky", "Oregon", "Oklahoma", "Connecticut", "Utah"
        ],
        
        "Major Cities": [
            "New York City", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Austin", "Jacksonville", "Fort Worth", "Columbus", "Indianapolis",
            "Charlotte", "San Francisco", "Seattle", "Denver", "Washington DC",
            "Boston", "Nashville", "Detroit", "Oklahoma City", "Portland",
            "Las Vegas", "Memphis", "Baltimore", "Milwaukee", "Atlanta"
        ],
        
        # ENTERTAINMENT INFRASTRUCTURE
        "Movie Theater Chains": [
            "AMC Theatres", "Regal Cinemas", "Cinemark", "Marcus Theatres", "Harkins Theatres",
            "Showcase Cinemas", "Bow Tie Cinemas", "Malco Theatres", "B&B Theatres", "Galaxy Theatres",
            "Alamo Drafthouse", "iPic Theaters", "ArcLight Cinemas", "Landmark Theatres", "Angelika Film Center"
        ],
        
        "Music Venues": [
            "Madison Square Garden", "Radio City Music Hall", "Carnegie Hall", "Lincoln Center",
            "Hollywood Bowl", "Greek Theatre", "Red Rocks Amphitheatre", "Gorge Amphitheatre",
            "The Fillmore", "House of Blues", "The Roxy", "Troubadour", "Blue Note",
            "Apollo Theater", "Grand Ole Opry", "Ryman Auditorium", "Fox Theatre"
        ],
        
        "Casino Chains": [
            "Caesars Entertainment", "MGM Resorts", "Las Vegas Sands", "Wynn Resorts",
            "Boyd Gaming", "Penn National Gaming", "Red Rock Resorts", "Golden Entertainment",
            "Churchill Downs", "Eldorado Resorts", "Station Casinos", "Mohegan Gaming",
            "Seminole Gaming", "Foxwoods", "Pechanga", "WinStar", "Choctaw"
        ],

        # EMERGING MARKETS - INTERNATIONAL EXPANSION
        "Brazil Companies": [
            "Vale", "Petrobras", "Itaú Unibanco", "Banco do Brasil", "Bradesco",
            "Ambev", "JBS", "BRF", "Magazine Luiza", "Via Varejo",
            "B3", "Weg", "Suzano", "Klabin", "Gerdau",
            "Embraer", "Azul", "GOL", "LATAM Airlines", "TAM",
            "Natura", "Boticário", "Americanas", "Submarino", "Mercado Livre",
            "Stone", "PagSeguro", "Nubank", "Inter", "XP Inc",
            "Globo", "Record", "SBT", "Folha", "Estado",
            "Braskem", "Ultrapar", "Cosan", "Raízen", "Vibra"
        ],

        "Mexico Companies": [
            "América Móvil", "Cemex", "Grupo Bimbo", "Walmart Mexico", "Femsa",
            "Grupo Carso", "Alfa", "Grupo México", "Televisa", "TV Azteca",
            "Banco Santander México", "BBVA México", "Banorte", "Banamex", "Scotiabank México",
            "Pemex", "CFE", "Grupo Modelo", "Corona", "Tecate",
            "Aeromexico", "Volaris", "Interjet", "VivaAerobus", "Magnicharters",
            "Liverpool", "El Palacio de Hierro", "Soriana", "Chedraui", "Bodega Aurrera",
            "Telmex", "Telcel", "AT&T Mexico", "Movistar México", "Unefon",
            "Grupo Financiero Banorte", "Grupo Financiero Inbursa", "ActinVer"
        ],

        "Indonesia Companies": [
            "Bank Central Asia", "Bank Mandiri", "Bank Rakyat Indonesia", "Bank Negara Indonesia",
            "Telkom Indonesia", "Indosat", "XL Axiata", "Smartfren", "3 Indonesia",
            "Astra International", "Sinar Mas", "Lippo Group", "Salim Group", "Bakrie Group",
            "Garuda Indonesia", "Lion Air", "Sriwijaya Air", "Citilink", "Batik Air",
            "Pertamina", "PLN", "Adaro Energy", "Bumi Resources", "Indo Tambangraya",
            "Indomaret", "Alfamart", "Matahari", "Centro", "Ramayana",
            "GoTo Group", "Gojek", "Tokopedia", "Bukalapak", "Shopee Indonesia",
            "Indofood", "Mayora", "Unilever Indonesia", "Kalbe Farma", "Kimia Farma"
        ],

        "Thailand Companies": [
            "PTT", "CP Group", "Siam Cement Group", "Bangkok Bank", "Kasikornbank",
            "Krung Thai Bank", "Siam Commercial Bank", "TMB Bank", "Kiatnakin Bank",
            "Thai Airways", "Bangkok Airways", "Nok Air", "Thai AirAsia", "Thai Lion Air",
            "Central Group", "Big C", "Lotus", "7-Eleven Thailand", "Family Mart Thailand",
            "Advanced Info Service", "True Corporation", "dtac", "CAT Telecom", "TOT",
            "Thai Union", "Charoen Pokphand", "Minor International", "Dusit Thani", "Centara",
            "Berli Jucker", "Thai Beverage", "Singha", "Chang Beer", "Leo Beer"
        ],

        "Turkey Companies": [
            "Turkish Airlines", "Pegasus Airlines", "Onur Air", "SunExpress", "AtlasGlobal",
            "Turkcell", "Vodafone Turkey", "Türk Telekom", "BiP", "Turk.net",
            "İş Bankası", "Garanti BBVA", "Yapı Kredi", "Akbank", "Halkbank",
            "Koç Holding", "Sabancı Holding", "Doğuş Group", "Eczacıbaşı", "Borusan",
            "Arçelik", "Vestel", "Beko", "Profilo", "Altus",
            "Tesco Kipa", "Migros", "BIM", "A101", "Şok",
            "TAV", "İGA", "Sabiha Gökçen", "Antalya Airport", "İzmir Airport",
            "Petkim", "Tüpraş", "BOTAŞ", "TCDD", "THY Teknik"
        ],

        "Saudi Arabia Companies": [
            "Saudi Aramco", "SABIC", "Al Rajhi Bank", "National Commercial Bank", "Riyad Bank",
            "Saudi Telecom", "Mobily", "Zain Saudi Arabia", "Virgin Mobile Saudi", "Lebara",
            "Saudia", "flynas", "Flyadeal", "Sky Prime", "Alpha Star",
            "Almarai", "Savola", "Herfy", "Al Baik", "Kudu",
            "Jarir", "Extra", "Lulu", "Panda", "Tamimi",
            "Ma'aden", "SEC", "SWCC", "Marafiq", "Taqa",
            "Alinma Bank", "Bank Al Bilad", "Arab National Bank", "Banque Saudi Fransi", "SABB",
            "Red Sea Global", "NEOM", "Qiddiya", "Diriyah Gate", "King Abdullah Economic City"
        ],

        "UAE Companies": [
            "Emirates", "Etihad Airways", "flydubai", "Air Arabia", "Wizz Air Abu Dhabi",
            "Etisalat", "du", "Virgin Mobile UAE", "Salam Mobile", "Lebara UAE",
            "First Abu Dhabi Bank", "Emirates NBD", "ADCB", "Mashreq", "CBD",
            "DP World", "ADNOC", "ENOC", "EPPCO", "ADGAS",
            "Emaar", "Damac", "Nakheel", "Aldar", "Majid Al Futtaim",
            "Carrefour UAE", "Lulu UAE", "Spinneys", "Union Coop", "ADCOOP",
            "Jumeirah", "Atlantis", "Rotana", "Shangri-La", "Four Seasons UAE",
            "Dubai Airports", "Abu Dhabi Airports", "ADAC", "RTA", "DEWA"
        ],

        "Egypt Companies": [
            "Commercial International Bank", "National Bank of Egypt", "Banque Misr", "QNB ALAHLI", "HSBC Egypt",
            "Orange Egypt", "Vodafone Egypt", "Etisalat Misr", "WE", "Nile Sat",
            "EgyptAir", "Air Cairo", "AlMasria Universal Airlines", "Nile Air", "AMC Airlines",
            "Talaat Moustafa Group", "Palm Hills", "SODIC", "Madinet Nasr", "New Urban Communities",
            "Orascom Construction", "Hassan Allam", "Arab Contractors", "Petrojet", "ENPPI",
            "Egyptian General Petroleum", "EGPC", "EGAS", "GANOPE", "GUPCO",
            "Ezz Steel", "SUMED", "Alexandria Container", "Suez Canal Authority", "SCZONE",
            "Juhayna", "Edita Food", "MNHD", "Raya", "Fawry"
        ],

        "Nigeria Companies": [
            "Dangote Group", "BUA Group", "Flour Mills", "Nigerian Breweries", "Guinness Nigeria",
            "GTBank", "Access Bank", "First Bank", "UBA", "Zenith Bank",
            "MTN Nigeria", "Airtel Nigeria", "Globacom", "9mobile", "Ntel",
            "Arik Air", "Air Peace", "Dana Air", "Azman Air", "Max Air",
            "Nigerian National Petroleum", "Chevron Nigeria", "Shell Nigeria", "ExxonMobil Nigeria", "Total Nigeria",
            "Shoprite Nigeria", "Jumia Nigeria", "Konga", "Slot", "3C Hub",
            "Nestlé Nigeria", "Unilever Nigeria", "Procter & Gamble Nigeria", "Reckitt Nigeria", "GSK Nigeria",
            "Lafarge Africa", "Cement Company of Northern Nigeria", "BUA Cement", "Ibeto Cement", "Ashaka Cement"
        ],

        "South Africa Companies": [
            "Naspers", "Prosus", "MTN Group", "Vodacom", "Cell C",
            "Standard Bank", "FirstRand", "Absa", "Nedbank", "Capitec",
            "Sasol", "Anglo American", "BHP Billiton", "Impala Platinum", "Sibanye-Stillwater",
            "South African Airways", "Comair", "FlySafair", "Kulula", "Mango Airlines",
            "Shoprite", "Pick n Pay", "Woolworths", "Spar", "Massmart",
            "Eskom", "Transnet", "Telkom", "SAPO", "SAA",
            "Old Mutual", "Sanlam", "Discovery", "Momentum", "Liberty",
            "Tiger Brands", "Pioneer Foods", "RCL Foods", "Astral Foods", "Clover"
        ],

        # US STATE UNIVERSITIES - MAJOR STATE SCHOOLS
        "California State Universities": [
            "UC Berkeley", "UCLA", "UC San Diego", "UC Davis", "UC Santa Barbara",
            "UC Irvine", "UC Santa Cruz", "UC Riverside", "UC Merced", "UCSF",
            "Cal State Long Beach", "Cal State Fullerton", "Cal State Northridge", "Cal State LA", "San Diego State",
            "San Jose State", "Cal Poly San Luis Obispo", "Cal State Sacramento", "Cal State San Bernardino", "Fresno State",
            "Cal State Chico", "Cal State Bakersfield", "Cal State Dominguez Hills", "Cal State East Bay", "Cal State Monterey Bay"
        ],

        "Texas State Universities": [
            "University of Texas at Austin", "Texas A&M University", "University of Houston", "Texas Tech University", "UT Dallas",
            "UT San Antonio", "UT Arlington", "UT El Paso", "Texas State University", "University of North Texas",
            "Sam Houston State", "Texas Southern University", "Prairie View A&M", "Tarleton State", "West Texas A&M",
            "Stephen F. Austin", "Lamar University", "Texas A&M Commerce", "Texas A&M Corpus Christi", "UT Tyler"
        ],

        "Florida State Universities": [
            "University of Florida", "Florida State University", "University of South Florida", "Florida International University", "UCF",
            "Florida Atlantic University", "Florida Institute of Technology", "Florida A&M University", "Nova Southeastern", "Florida Tech",
            "Florida Gulf Coast University", "Florida Polytechnic", "New College of Florida", "Florida Agricultural and Mechanical"
        ],

        "New York State Universities": [
            "SUNY Buffalo", "SUNY Stony Brook", "SUNY Albany", "SUNY Binghamton", "SUNY New Paltz",
            "SUNY Geneseo", "SUNY Oswego", "SUNY Plattsburgh", "SUNY Oneonta", "SUNY Cortland",
            "SUNY Fredonia", "SUNY Potsdam", "SUNY Purchase", "SUNY Old Westbury", "SUNY Farmingdale"
        ],

        "Pennsylvania State Universities": [
            "Penn State University", "Temple University", "University of Pittsburgh", "Drexel University", "Villanova University",
            "Carnegie Mellon University", "Duquesne University", "Saint Joseph's University", "La Salle University", "West Chester University",
            "Indiana University of Pennsylvania", "Kutztown University", "Millersville University", "Bloomsburg University", "Shippensburg University"
        ],

        "Illinois State Universities": [
            "University of Illinois Urbana-Champaign", "University of Illinois Chicago", "Illinois State University", "Northern Illinois University", "Southern Illinois University",
            "Eastern Illinois University", "Western Illinois University", "Governors State University", "Chicago State University", "Northeastern Illinois University"
        ],

        "Ohio State Universities": [
            "Ohio State University", "University of Cincinnati", "Kent State University", "Ohio University", "Miami University",
            "Bowling Green State University", "Wright State University", "Cleveland State University", "Youngstown State University", "Central State University"
        ],

        "Michigan State Universities": [
            "University of Michigan", "Michigan State University", "Wayne State University", "Western Michigan University", "Eastern Michigan University",
            "Central Michigan University", "Northern Michigan University", "Grand Valley State", "Oakland University", "Ferris State University"
        ],

        "Georgia State Universities": [
            "University of Georgia", "Georgia Tech", "Georgia State University", "Georgia Southern University", "Kennesaw State University",
            "Georgia College & State University", "Valdosta State University", "Albany State University", "Columbus State University", "Fort Valley State University"
        ],

        "North Carolina State Universities": [
            "UNC Chapel Hill", "NC State University", "UNC Charlotte", "East Carolina University", "Appalachian State University",
            "UNC Greensboro", "UNC Wilmington", "Western Carolina University", "Fayetteville State University", "NC A&T State University"
        ],

        "Virginia State Universities": [
            "University of Virginia", "Virginia Tech", "James Madison University", "George Mason University", "Virginia Commonwealth University",
            "Old Dominion University", "Norfolk State University", "Radford University", "Longwood University", "Virginia State University"
        ],

        # REGIONAL COMPANIES BY US STATE
        "California Regional Companies": [
            "In-N-Out Burger", "California Pizza Kitchen", "Panda Express", "Del Taco", "Jack in the Box",
            "Round Table Pizza", "Jamba Juice", "Noah's Bagels", "Peet's Coffee", "Blue Bottle Coffee",
            "Ghirardelli", "See's Candies", "Clif Bar", "KIND", "Wonderful Company",
            "Driscoll's", "Sun-Maid", "Diamond Foods", "Blue Diamond", "Ocean Spray",
            "Kaiser Permanente", "Sutter Health", "UCSF Health", "Cedars-Sinai", "Scripps Health",
            "PG&E", "SoCal Edison", "San Diego Gas & Electric", "Sacramento Municipal", "LADWP"
        ],

        "Texas Regional Companies": [
            "H-E-B", "Whataburger", "Torchy's Tacos", "Freebirds", "Shipley Do-Nuts",
            "Buc-ee's", "QuikTrip", "Stripes", "7-Eleven Texas", "Valero",
            "Southwest Airlines", "American Airlines", "Spirit Airlines", "Frontier Airlines", "JSX",
            "AT&T", "Dell Technologies", "Texas Instruments", "ExxonMobil", "Phillips 66",
            "Kimberly-Clark", "Dr Pepper Snapple", "Frito-Lay", "Mission Foods", "Cinemark"
        ],

        "Florida Regional Companies": [
            "Publix", "Winn-Dixie", "Sedano's", "Presidente", "BrandsMart USA",
            "Checkers", "PDQ", "Tijuana Flats", "Bahama Breeze", "Bonefish Grill",
            "Spirit Airlines", "JetBlue Airways", "Allegiant Air", "Silver Airways", "GoJet",
            "NextEra Energy", "Florida Power & Light", "Duke Energy Florida", "TECO Energy", "Florida Public Utilities",
            "Carnival Corporation", "Royal Caribbean", "Norwegian Cruise Line", "MSC Cruises", "Virgin Voyages"
        ],

        "New York Regional Companies": [
            "Wegmans", "Price Chopper", "ShopRite", "Stop & Shop", "Key Food",
            "Nathan's Famous", "Junior's", "Shake Shack", "Joe Coffee", "Ess-a-Bagel",
            "JetBlue Airways", "Republic Airways", "Envoy Air", "Piedmont Airlines", "PSA Airlines",
            "ConEd", "National Grid", "NYSEG", "Central Hudson", "Orange & Rockland",
            "M&T Bank", "KeyBank", "Citizens Bank", "Community Bank", "Tompkins Trust"
        ],

        # MEDIA COMPANIES AND NEWS ORGANIZATIONS
        "Major News Organizations": [
            "CNN", "Fox News", "MSNBC", "BBC", "Sky News",
            "Associated Press", "Reuters", "Bloomberg News", "Wall Street Journal", "Financial Times",
            "New York Times", "Washington Post", "USA Today", "Los Angeles Times", "Chicago Tribune",
            "Boston Globe", "Philadelphia Inquirer", "Miami Herald", "Dallas Morning News", "Houston Chronicle",
            "Denver Post", "Seattle Times", "San Francisco Chronicle", "Atlanta Journal-Constitution", "Detroit Free Press",
            "NPR", "PBS", "C-SPAN", "Voice of America", "BBC World Service"
        ],

        "Digital Media": [
            "BuzzFeed", "Vice Media", "Vox Media", "Politico", "Axios",
            "The Daily Beast", "HuffPost", "Salon", "Slate", "The Intercept",
            "ProPublica", "Mother Jones", "The Nation", "The New Republic", "National Review",
            "Breitbart", "Daily Wire", "TheBlaze", "Newsmax", "OAN",
            "Substack", "Medium", "LinkedIn Publishing", "Ghost", "ConvertKit"
        ],

        "Magazine Publishers": [
            "Condé Nast", "Hearst Magazines", "Meredith Corporation", "Time Inc", "Forbes Media",
            "National Geographic", "Smithsonian Magazine", "Scientific American", "Popular Science", "Wired",
            "The Atlantic", "Harper's Magazine", "The New Yorker", "Vanity Fair", "GQ",
            "Vogue", "Elle", "Cosmopolitan", "Good Housekeeping", "Better Homes & Gardens",
            "People", "Entertainment Weekly", "Rolling Stone", "Variety", "The Hollywood Reporter"
        ],

        "Radio Networks": [
            "iHeartMedia", "Cumulus Media", "Entercom", "Salem Media", "Townsquare Media",
            "Educational Media Foundation", "American Family Radio", "Westwood One", "Premiere Networks", "United Stations",
            "SiriusXM", "Pandora Radio", "Spotify", "Apple Music", "Amazon Music"
        ],

        # LAW FIRMS AND ACCOUNTING FIRMS
        "Big Law Firms": [
            "Kirkland & Ellis", "Latham & Watkins", "Baker McKenzie", "DLA Piper", "Skadden Arps",
            "Clifford Chance", "Freshfields", "Linklaters", "Allen & Overy", "Magic Circle",
            "Sullivan & Cromwell", "Cravath Swaine & Moore", "Davis Polk", "Simpson Thacher", "Wachtell Lipton",
            "Gibson Dunn", "Paul Weiss", "Cleary Gottlieb", "Debevoise & Plimpton", "Shearman & Sterling",
            "White & Case", "Jones Day", "Hogan Lovells", "Norton Rose Fulbright", "King & Spalding"
        ],

        "Regional Law Firms": [
            "Greenberg Traurig", "Morgan Lewis", "McDermott Will", "Foley & Lardner", "Hunton Andrews Kurth",
            "Perkins Coie", "Fenwick & West", "Wilson Sonsini", "Cooley LLP", "Gunderson Dettmer",
            "Orrick Herrington", "Pillsbury Winthrop", "Morrison & Foerster", "Goodwin Procter", "Ropes & Gray",
            "WilmerHale", "Fish & Richardson", "Finnegan Henderson", "Knobbe Martens", "Sterne Kessler"
        ],

        "Big Four Accounting": [
            "Deloitte", "PwC", "EY", "KPMG", "Grant Thornton",
            "BDO", "RSM", "CliftonLarsonAllen", "Crowe", "Mazars",
            "Baker Tilly", "CBIZ", "Moss Adams", "WithumSmith+Brown", "CohnReznick",
            "Marcum", "Cherry Bekaert", "BKD", "Plante Moran", "Wipfli"
        ],

        # FOOD BRANDS AND RESTAURANT CHAINS
        "Fast Food Chains": [
            "McDonald's", "Subway", "Starbucks", "KFC", "Burger King",
            "Pizza Hut", "Domino's", "Taco Bell", "Wendy's", "Dunkin'",
            "Chick-fil-A", "Popeyes", "Arby's", "Sonic", "Carl's Jr",
            "Hardee's", "White Castle", "In-N-Out", "Five Guys", "Shake Shack",
            "Chipotle", "Qdoba", "Moe's", "Panda Express", "Pei Wei",
            "Papa John's", "Little Caesars", "Papa Murphy's", "Casey's", "QuikTrip"
        ],

        "Casual Dining": [
            "Applebee's", "Chili's", "TGI Friday's", "Olive Garden", "Red Lobster",
            "Outback Steakhouse", "Texas Roadhouse", "LongHorn Steakhouse", "Cracker Barrel", "Denny's",
            "IHOP", "Perkins", "Bob Evans", "Buffalo Wild Wings", "Hooters",
            "Dave & Buster's", "Chuck E. Cheese", "California Pizza Kitchen", "P.F. Chang's", "Cheesecake Factory",
            "Ruth's Chris", "Morton's", "The Capital Grille", "Fleming's", "Eddie V's"
        ],

        "Coffee Chains": [
            "Starbucks", "Dunkin'", "Tim Hortons", "Costa Coffee", "Peet's Coffee",
            "Caribou Coffee", "The Coffee Bean", "Blue Bottle", "Intelligentsia", "Counter Culture",
            "Stumptown", "La Colombe", "Philz Coffee", "Dutch Bros", "Scooter's Coffee",
            "Biggby Coffee", "Gloria Jean's", "Second Cup", "Coffee Beanery", "It's a Grind"
        ],

        "Food Brands": [
            "Coca-Cola", "PepsiCo", "Nestlé", "Unilever", "Kraft Heinz",
            "General Mills", "Kellogg's", "Campbell Soup", "ConAgra", "Tyson Foods",
            "Hormel", "Oscar Mayer", "Hebrew National", "Ball Park", "Hillshire Farm",
            "Sara Lee", "Wonder Bread", "Pepperidge Farm", "Entenmann's", "Hostess",
            "Frito-Lay", "Doritos", "Cheetos", "Ruffles", "Lay's",
            "Oreo", "Nabisco", "Chips Ahoy!", "Ritz", "Triscuit"
        ],

        # AUTOMOTIVE BRANDS AND DEALERS
        "Luxury Car Brands": [
            "Mercedes-Benz", "BMW", "Audi", "Lexus", "Acura",
            "Infiniti", "Cadillac", "Lincoln", "Genesis", "Volvo",
            "Jaguar", "Land Rover", "Porsche", "Maserati", "Alfa Romeo",
            "Bentley", "Rolls-Royce", "Aston Martin", "Ferrari", "Lamborghini",
            "McLaren", "Bugatti", "Koenigsegg", "Pagani", "Tesla"
        ],

        "Mass Market Auto": [
            "Toyota", "Honda", "Nissan", "Ford", "Chevrolet",
            "Hyundai", "Kia", "Volkswagen", "Mazda", "Subaru",
            "Chrysler", "Dodge", "Jeep", "Ram", "GMC",
            "Buick", "Mitsubishi", "Suzuki", "Isuzu", "Fiat"
        ],

        "Auto Dealers": [
            "AutoNation", "Penske Automotive", "Lithia Motors", "Group 1 Automotive", "Sonic Automotive",
            "Hendrick Automotive", "Van Tuyl", "Berkshire Hathaway Automotive", "Asbury Automotive", "CarMax",
            "Carvana", "Vroom", "Shift", "Cars.com", "AutoTrader",
            "TrueCar", "CarGurus", "Edmunds", "KBB", "NADA"
        ],

        # INSURANCE COMPANIES
        "Property & Casualty Insurance": [
            "State Farm", "GEICO", "Progressive", "Allstate", "USAA",
            "Liberty Mutual", "Farmers", "Nationwide", "American Family", "Travelers",
            "Auto-Owners", "Erie Insurance", "Cincinnati Financial", "Safeco", "MetLife Auto",
            "Mercury Insurance", "Esurance", "The General", "Direct General", "Safe Auto"
        ],

        "Life Insurance": [
            "MetLife", "Prudential", "Northwestern Mutual", "New York Life", "MassMutual",
            "Guardian Life", "Lincoln Financial", "Principal Financial", "Aflac", "Unum",
            "Transamerica", "AIG", "John Hancock", "Pacific Life", "Penn Mutual",
            "Mutual of Omaha", "Genworth", "Primerica", "American General", "Banner Life"
        ],

        "Health Insurance": [
            "UnitedHealth", "Anthem", "Aetna", "Cigna", "Humana",
            "Kaiser Permanente", "Blue Cross Blue Shield", "Molina Healthcare", "Centene", "WellCare",
            "Health Net", "Medicaid", "Medicare", "Tricare", "VA Healthcare",
            "Oscar Health", "Bright Health", "Clover Health", "Alignment Healthcare", "Devoted Health"
        ],

        # TELECOMS GLOBALLY
        "Global Telecom Giants": [
            "Verizon", "AT&T", "T-Mobile", "China Mobile", "China Telecom",
            "Vodafone", "Orange", "Deutsche Telekom", "Telefónica", "América Móvil",
            "NTT", "SoftBank", "KDDI", "SK Telecom", "KT Corporation",
            "Bharti Airtel", "Reliance Jio", "Vodafone Idea", "MTN Group", "Safaricom",
            "Turkcell", "Tele2", "Telenor", "Telia", "Swisscom"
        ],

        "Regional Telecoms": [
            "Sprint", "US Cellular", "Cricket", "Boost Mobile", "Metro by T-Mobile",
            "Visible", "Mint Mobile", "Google Fi", "Xfinity Mobile", "Spectrum Mobile",
            "Consumer Cellular", "Straight Talk", "TracFone", "Net10", "Simple Mobile",
            "Total Wireless", "Walmart Family Mobile", "H2O Wireless", "Ultra Mobile", "Red Pocket"
        ],

        # REAL ESTATE COMPANIES
        "Real Estate Development": [
            "Brookfield Properties", "Related Companies", "Tishman Speyer", "Boston Properties", "Simon Property Group",
            "Equity Residential", "AvalonBay", "Essex Property Trust", "UDR", "Camden Property Trust",
            "Prologis", "Public Storage", "Equity LifeStyle", "Sun Communities", "Manufactured Housing",
            "Toll Brothers", "Pulte Homes", "D.R. Horton", "Lennar", "KB Home",
            "NVR", "Ryan Homes", "Centex", "Beazer Homes", "M/I Homes"
        ],

        "Real Estate Services": [
            "Realogy", "Keller Williams", "RE/MAX", "Coldwell Banker", "Century 21",
            "Sotheby's International", "Compass", "eXp Realty", "Redfin", "Zillow",
            "Trulia", "Realtor.com", "LoopNet", "CoStar", "CBRE",
            "JLL", "Cushman & Wakefield", "Colliers", "Marcus & Millichap", "Newmark",
            "Savills", "Knight Frank", "Avison Young", "Transwestern", "NAI Global"
        ],

        "Property Management": [
            "Greystar", "Lincoln Property Company", "Bozzuto", "Camden", "Equity Residential",
            "AvalonBay", "Essex", "UDR", "MAA", "Post Properties",
            "Fairfield Residential", "ZRS Management", "Alliance Residential", "Mill Creek Residential", "Wood Partners",
            "Pinnacle", "BH Management", "Cushman & Wakefield", "CBRE", "JLL"
        ],

        # ADDITIONAL STATE UNIVERSITIES
        "Washington State Universities": [
            "University of Washington", "Washington State University", "Western Washington University", "Central Washington University", "Eastern Washington University",
            "The Evergreen State College", "University of Washington Tacoma", "University of Washington Bothell", "Seattle University", "Pacific Lutheran University"
        ],

        "Wisconsin State Universities": [
            "University of Wisconsin-Madison", "University of Wisconsin-Milwaukee", "Marquette University", "University of Wisconsin-La Crosse", "University of Wisconsin-Oshkosh",
            "University of Wisconsin-Eau Claire", "University of Wisconsin-Green Bay", "University of Wisconsin-Platteville", "University of Wisconsin-Stevens Point", "University of Wisconsin-Whitewater"
        ],

        "Colorado State Universities": [
            "University of Colorado Boulder", "Colorado State University", "University of Colorado Denver", "University of Colorado Colorado Springs", "Colorado School of Mines",
            "University of Northern Colorado", "Metropolitan State University", "Colorado Mesa University", "Western State Colorado University", "Fort Lewis College"
        ],

        "Minnesota State Universities": [
            "University of Minnesota Twin Cities", "University of Minnesota Duluth", "Minnesota State University Mankato", "St. Cloud State University", "Winona State University",
            "Bemidji State University", "Minnesota State University Moorhead", "Southwest Minnesota State", "Metropolitan State University", "Saint John's University"
        ],

        "Arizona State Universities": [
            "Arizona State University", "University of Arizona", "Northern Arizona University", "Arizona Western College", "Cochise College",
            "Estrella Mountain Community College", "GateWay Community College", "Glendale Community College", "Mesa Community College", "Paradise Valley Community College"
        ],

        # MORE REGIONAL COMPANIES BY STATE
        "Illinois Regional Companies": [
            "Jewel-Osco", "Mariano's", "Ultra Foods", "Tony's Fresh Market", "Pete's Fresh Market",
            "Portillo's", "Lou Malnati's", "Giordano's", "Uno Pizzeria", "Italian Beef & Sausage Co",
            "United Airlines", "Boeing Chicago", "Abbott Laboratories", "Caterpillar", "John Deere",
            "ComEd", "Nicor Gas", "Peoples Gas", "North Shore Gas", "Ameren Illinois"
        ],

        "Ohio Regional Companies": [
            "Kroger", "Giant Eagle", "Meijer", "Marc's", "IGA",
            "Skyline Chili", "Gold Star Chili", "LaRosa's Pizza", "Marion's Piazza", "Donatos Pizza",
            "Nationwide Airlines", "NetJets", "Flexjet", "Flight Options", "Airshare",
            "Ohio Edison", "Cleveland Electric", "Toledo Edison", "AEP Ohio", "Duke Energy Ohio"
        ],

        "Michigan Regional Companies": [
            "Meijer", "Spartan Stores", "Family Fare", "VG's Food Centers", "Fresh Thyme",
            "Buddy's Pizza", "Jet's Pizza", "Little Caesars", "Hungry Howie's", "Blaze Pizza",
            "Delta Air Lines Detroit", "Spirit Airlines", "Frontier Airlines", "Southwest Airlines", "United Airlines",
            "DTE Energy", "Consumers Energy", "Upper Peninsula Power", "Indiana Michigan Power", "Cloverland Electric"
        ],

        "Washington Regional Companies": [
            "Fred Meyer", "QFC", "Safeway", "Top Foods", "Thriftway",
            "Dick's Drive-In", "Ivar's", "Ezell's Famous Chicken", "Taco Time", "Burgerville",
            "Alaska Airlines", "Delta Air Lines", "United Airlines", "American Airlines", "Southwest Airlines",
            "Puget Sound Energy", "Seattle City Light", "Tacoma Power", "Snohomish County PUD", "Avista"
        ],

        "Oregon Regional Companies": [
            "Fred Meyer", "Safeway", "Albertsons", "WinCo Foods", "Market of Choice",
            "Burgerville", "McMenamins", "Voodoo Doughnut", "Blue Star Donuts", "Pine State Biscuits",
            "Alaska Airlines", "Delta Air Lines", "United Airlines", "American Airlines", "Southwest Airlines",
            "Portland General Electric", "Pacific Power", "Eugene Water & Electric", "Clark Public Utilities", "NW Natural"
        ],

        # MORE FOOD BRANDS AND RESTAURANT CHAINS
        "International Food Chains": [
            "Nando's", "Wagamama", "Pret A Manger", "Greggs", "Costa Coffee",
            "Tim Hortons", "Harvey's", "Swiss Chalet", "The Keg", "Boston Pizza",
            "Jollibee", "Mang Inasal", "Chowking", "Red Ribbon", "Greenwich Pizza",
            "Yoshinoya", "Sukiya", "Matsuya", "Ootoya", "Tenya"
        ],

        "Regional Pizza Chains": [
            "Casey's General Store", "Godfather's Pizza", "Happy Joe's", "Quad City Style", "Mazzio's",
            "Rosati's", "Aurelio's Pizza", "Villa Italian Kitchen", "Sbarro", "Blaze Pizza",
            "MOD Pizza", "Pieology", "Pizza Rev", "Your Pie", "Uncle Maddio's"
        ],

        "Bakery Chains": [
            "Panera Bread", "Corner Bakery Cafe", "Au Bon Pain", "Paris Baguette", "85°C Bakery",
            "Great Harvest Bread", "Einstein Bros. Bagels", "Bruegger's Bagels", "Manhattan Bagel", "Noah's New York Bagels",
            "Nothing Bundt Cakes", "Crumbl Cookies", "Insomnia Cookies", "Tiff's Treats", "Levain Bakery"
        ],

        # MORE AUTOMOTIVE COMPANIES
        "Auto Parts Retailers": [
            "AutoZone", "Advance Auto Parts", "O'Reilly Auto Parts", "NAPA Auto Parts", "Pep Boys",
            "CarQuest", "Genuine Parts Company", "Parts Authority", "AutoCare", "4 Wheel Parts",
            "Discount Tire", "Tire Rack", "America's Tire", "Big O Tires", "Firestone Complete Auto Care"
        ],

        "Car Rental Companies": [
            "Enterprise Rent-A-Car", "Hertz", "Avis", "Budget", "National Car Rental",
            "Alamo", "Dollar Car Rental", "Thrifty", "Sixt", "Zipcar",
            "Turo", "Getaround", "HyreCar", "Maven", "ReachNow"
        ],

        # MORE INSURANCE COMPANIES
        "Regional Insurance Companies": [
            "Farm Bureau Insurance", "Country Financial", "Ohio Mutual", "Shelter Insurance", "Auto Club Insurance",
            "California State Auto Association", "AAA", "CSAA", "Interinsurance Exchange", "Texas Farm Bureau",
            "Florida Farm Bureau", "Georgia Farm Bureau", "Tennessee Farm Bureau", "Kentucky Farm Bureau", "Illinois Farm Bureau"
        ],

        # MORE RETAIL COMPANIES
        "Department Stores": [
            "Macy's", "Nordstrom", "Bloomingdale's", "Saks Fifth Avenue", "Neiman Marcus",
            "Dillard's", "JCPenney", "Kohl's", "Belk", "Von Maur",
            "Lord & Taylor", "Bergdorf Goodman", "Barneys New York", "Century 21", "Loehmann's"
        ],

        "Discount Retailers": [
            "Walmart", "Target", "Costco", "Sam's Club", "BJ's Wholesale Club",
            "Dollar General", "Dollar Tree", "Family Dollar", "99 Cents Only", "Five Below",
            "Big Lots", "Ollie's Bargain Outlet", "Ocean State Job Lot", "Tuesday Morning", "Christmas Tree Shops"
        ],

        "Specialty Retailers": [
            "Home Depot", "Lowe's", "Menards", "Ace Hardware", "True Value",
            "Best Buy", "Fry's Electronics", "Micro Center", "B&H Photo", "Adorama",
            "Dick's Sporting Goods", "Sports Authority", "Big 5 Sporting Goods", "Modell's", "Dunham's Sports"
        ],

        # ADDITIONAL TECH COMPANIES
        "Software Companies": [
            "Salesforce", "Oracle", "SAP", "Adobe", "VMware",
            "ServiceNow", "Workday", "Splunk", "Tableau", "Slack",
            "Zoom", "DocuSign", "Dropbox", "Box", "Atlassian",
            "Shopify", "Square", "PayPal", "Stripe", "Intuit"
        ],

        # FINANCIAL SERVICES
        "Investment Banks": [
            "Goldman Sachs", "Morgan Stanley", "JPMorgan Chase", "Bank of America Merrill Lynch", "Citigroup",
            "Wells Fargo Securities", "Credit Suisse", "Deutsche Bank", "Barclays", "UBS",
            "Jefferies", "Piper Sandler", "Raymond James", "Stifel", "William Blair"
        ],

        "Asset Management": [
            "BlackRock", "Vanguard", "Fidelity", "State Street", "T. Rowe Price",
            "Franklin Templeton", "Capital Group", "BNY Mellon", "Northern Trust", "Invesco",
            "Schroders", "Allianz", "Prudential", "MetLife", "AXA"
        ],

        # HEALTHCARE AND BIOTECH
        "Pharmaceutical Companies": [
            "Johnson & Johnson", "Pfizer", "Roche", "Novartis", "Merck",
            "AbbVie", "Bristol Myers Squibb", "AstraZeneca", "GlaxoSmithKline", "Sanofi",
            "Gilead Sciences", "Amgen", "Biogen", "Celgene", "Moderna"
        ],

        "Medical Device Companies": [
            "Medtronic", "Abbott", "Boston Scientific", "Stryker", "Becton Dickinson",
            "Danaher", "Zimmer Biomet", "Edwards Lifesciences", "Intuitive Surgical", "Baxter",
            "3M Health Care", "GE Healthcare", "Siemens Healthineers", "Philips Healthcare", "Canon Medical"
        ],

        # ENTERTAINMENT AND GAMING
        "Video Game Companies": [
            "Electronic Arts", "Activision Blizzard", "Take-Two Interactive", "Ubisoft", "Epic Games",
            "Valve", "Riot Games", "Bungie", "2K Games", "Rockstar Games",
            "Bethesda", "BioWare", "Respawn Entertainment", "Treyarch", "Infinity Ward"
        ],

        "Streaming Services": [
            "Netflix", "Disney+", "Amazon Prime Video", "HBO Max", "Hulu",
            "Apple TV+", "Paramount+", "Peacock", "Discovery+", "ESPN+",
            "YouTube TV", "Sling TV", "FuboTV", "Philo", "AT&T TV"
        ],

        # ENERGY COMPANIES
        "Oil and Gas Companies": [
            "ExxonMobil", "Chevron", "ConocoPhillips", "Marathon Petroleum", "Phillips 66",
            "Valero Energy", "Kinder Morgan", "Enterprise Products Partners", "Energy Transfer", "Plains All American",
            "Shell", "BP", "TotalEnergies", "Eni", "Equinor"
        ],

        "Renewable Energy": [
            "NextEra Energy", "Brookfield Renewable", "First Solar", "SunPower", "Enphase Energy",
            "Tesla Energy", "Vestas", "General Electric Renewable", "Siemens Gamesa", "Orsted",
            "Canadian Solar", "JinkoSolar", "Trina Solar", "LONGi Solar", "JA Solar"
        ],

        # FINAL COMPANIES TO REACH 2,500
        "Additional Airlines": [
            "Air France", "British Airways", "Lufthansa", "KLM", "Swiss International Air Lines",
            "Austrian Airlines", "Brussels Airlines", "Scandinavian Airlines", "Finnair", "Icelandair",
            "Virgin Atlantic", "Virgin Australia", "Qatar Airways", "Etihad Airways", "Singapore Airlines",
            "Cathay Pacific", "ANA", "JAL", "Korean Air", "Asiana Airlines",
            "China Southern Airlines", "China Eastern Airlines", "Air China", "Hainan Airlines", "Xiamen Airlines",
            "IndiGo", "SpiceJet", "Air India", "Vistara", "GoAir",
            "LATAM Airlines", "Avianca", "Copa Airlines", "Azul Brazilian Airlines", "GOL Linhas Aereas",
            "Air Canada", "WestJet", "Porter Airlines", "Flair Airlines", "Sunwing Airlines",
            "Qantas", "Jetstar", "Virgin Australia", "Tigerair Australia", "Rex Airlines",
            "South African Airways", "Kenya Airways", "Ethiopian Airlines", "Royal Air Maroc", "EgyptAir",
            "El Al", "Royal Jordanian", "Middle East Airlines", "Oman Air", "Kuwait Airways",
            "Saudia", "flydubai", "Air Arabia", "Wizz Air", "Ryanair",
            "easyJet", "Norwegian Air", "Vueling", "Eurowings", "Condor",
            "TUI Airways", "Thomas Cook Airlines", "Jet2.com", "Monarch Airlines", "Flybe"
        ],

        "Final Miscellaneous": [
            "Hertz Global Holdings", "Avis Budget Group", "Dollar Tree Inc", "Family Dollar Stores", "GameStop Corp"
        ]
    }

def main():
    companies = get_final_10000_companies()
    
    # Count total
    total = sum(len(v) for v in companies.values())
    print(f"Total companies in final 10,000 push: {total}")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/logos/final_10000_list.txt', 'w') as f:
        for category, company_list in companies.items():
            f.write(f"\n## {category}\n")
            for company in company_list:
                f.write(f"{company}\n")
    
    print("Saved to final_10000_list.txt")

if __name__ == "__main__":
    main()