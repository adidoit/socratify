#!/usr/bin/env python3
"""
MASSIVE list of startups, mid-sized companies, private companies, family businesses, and funds
"""

def get_massive_company_list():
    return {
        # UNICORN STARTUPS (2023-2024)
        "Global Unicorns": [
            # Fintech
            "Stripe", "Plaid", "Chime", "Brex", "Ramp", "Mercury", "Carta",
            "Deel", "Remote", "Gusto", "Rippling", "Justworks", "Papaya Global",
            "Tipalti", "Bill.com", "Navan", "Divvy", "Expensify", "Coupa",
            "Zip", "Sezzle", "Affirm", "Afterpay", "Klarna", "Revolut",
            "N26", "Monzo", "Starling Bank", "Wise", "TransferWise", "Nubank",
            "SoFi", "Upgrade", "Dave", "MoneyLion", "Current", "Varo",
            "Albert", "Brigit", "Earnin", "Tala", "Branch", "Petal",
            
            # Enterprise SaaS
            "Canva", "Figma", "Miro", "Notion", "Airtable", "Monday.com",
            "ClickUp", "Asana", "Linear", "Height", "Coda", "Craft",
            "Obsidian", "Roam Research", "Logseq", "RemNote", "Dendron",
            "Retool", "Bubble", "Webflow", "Framer", "Plasmic", "Builder.io",
            "Zapier", "Make", "n8n", "Pipedream", "Parabola", "Tray.io",
            "Segment", "Amplitude", "Mixpanel", "Heap", "PostHog", "June",
            "Pendo", "FullStory", "LogRocket", "Hotjar", "Crazy Egg",
            "Datadog", "New Relic", "Grafana Labs", "Honeycomb", "Lightstep",
            
            # AI/ML Companies
            "OpenAI", "Anthropic", "Cohere", "Stability AI", "Midjourney",
            "Character.AI", "Replika", "Jasper", "Copy.ai", "Writer",
            "Grammarly", "Mem", "Otter.ai", "Fireflies", "Gong", "Chorus",
            "Scale AI", "Labelbox", "Snorkel AI", "Weights & Biases",
            "Hugging Face", "Lightning AI", "Anyscale", "Modal", "Banana",
            "RunPod", "Lambda Labs", "CoreWeave", "Together AI", "Baseten",
            
            # Developer Tools
            "GitLab", "GitHub", "Bitbucket", "LinearB", "Jellyfish",
            "Docker", "HashiCorp", "Terraform", "Pulumi", "Spacelift",
            "CircleCI", "Travis CI", "Jenkins", "Buildkite", "Semaphore",
            "Vercel", "Netlify", "Render", "Railway", "Fly.io", "Deno",
            "Supabase", "PlanetScale", "Neon", "CockroachDB", "SingleStore",
            "MongoDB", "Redis", "Elastic", "Algolia", "Meilisearch",
            
            # Cybersecurity
            "CrowdStrike", "SentinelOne", "Cybereason", "Darktrace", "Vectra",
            "Snyk", "Checkmarx", "Veracode", "WhiteSource", "Black Duck",
            "1Password", "Bitwarden", "Dashlane", "LastPass", "Keeper",
            "Okta", "Auth0", "Ping Identity", "ForgeRock", "FusionAuth",
            "Cloudflare", "Fastly", "Akamai", "Imperva", "F5",
            
            # E-commerce/Marketplace
            "Faire", "Ankorstore", "Joor", "NuOrder", "Tundra", "Abound",
            "StockX", "GOAT", "Grailed", "Depop", "Vinted", "Poshmark",
            "Mercari", "OfferUp", "Letgo", "5miles", "Wallapop",
            "Etsy", "Reverb", "Ruby Lane", "Bonanza", "Storenvy",
            "BigCommerce", "WooCommerce", "Magento", "PrestaShop",
            "Shopify Plus", "CommerceTools", "Elastic Path", "Spryker",
            
            # Logistics/Delivery
            "Flexport", "Shippo", "EasyPost", "ShipBob", "ShipMonk",
            "Deliverr", "Flowspace", "Stord", "Ware2Go", "Darkstore",
            "GoPuff", "Gorillas", "Getir", "Jokr", "Buyk", "1520",
            "DoorDash", "Uber Eats", "Grubhub", "Seamless", "Caviar",
            "Toast", "ChowNow", "Olo", "Slice", "EatStreet",
            
            # PropTech
            "Compass", "Redfin", "Zillow", "Trulia", "Realtor.com",
            "Opendoor", "Offerpad", "Knock", "Orchard", "Ribbon",
            "Roofstock", "Fundrise", "RealtyMogul", "YieldStreet", "CrowdStreet",
            "WeWork", "Industrious", "Knotel", "Breather", "Convene",
            "Sonder", "Lyric", "Zeus Living", "Landing", "Blueground",
            
            # HealthTech
            "Oscar Health", "Clover Health", "Bright Health", "Devoted Health",
            "Ro", "Hims", "Curology", "Keeps", "Nurx", "Pill Club",
            "Carbon Health", "One Medical", "Forward", "Crossover Health",
            "Headspace", "Calm", "BetterHelp", "Talkspace", "Lyra Health",
            "Modern Health", "Spring Health", "Ginger", "Wysa", "Youper",
            "23andMe", "Color", "Invitae", "Tempus", "Foundation Medicine",
            
            # EdTech
            "Course Hero", "Chegg", "Quizlet", "Brainly", "Photomath",
            "Duolingo", "Babbel", "Busuu", "Memrise", "Drops",
            "MasterClass", "Skillshare", "Domestika", "CreativeLive",
            "Outschool", "Juni Learning", "Synthesis", "Primer", "Galileo",
            "Guild Education", "InStride", "Section4", "Reforge", "Maven"
        ],
        
        # MID-SIZED PRIVATE COMPANIES
        "Mid-Size Private Companies": [
            # Manufacturing
            "Bose Corporation", "Kohler Co.", "SC Johnson", "Hallmark Cards",
            "Levi Strauss & Co.", "LL Bean", "Patagonia", "REI Co-op",
            "Lands' End", "Eddie Bauer", "Carhartt", "Dickies", "Wrangler",
            "Lee Jeans", "Dockers", "Champion", "Hanes", "Fruit of the Loom",
            "Russell Athletic", "Jockey", "Maidenform", "Playtex", "Bali",
            
            # Food & Beverage
            "Amy's Kitchen", "Annie's Homegrown", "Clif Bar", "KIND Snacks",
            "RXBAR", "Larabar", "Epic Provisions", "Krave Jerky", "Bai",
            "Vita Coco", "Harmless Harvest", "Health-Ade", "GT's Kombucha",
            "Blue Bottle Coffee", "Intelligentsia", "Stumptown", "La Colombe",
            "Death Wish Coffee", "Black Rifle Coffee", "Bulletproof", "Four Sigmatic",
            "Athletic Brewing", "Heineken 0.0", "Budweiser Zero", "Corona Cero",
            
            # Retail
            "Trader Joe's", "Aldi US", "Lidl US", "Save-A-Lot", "Food 4 Less",
            "WinCo Foods", "Brookshire's", "Weis Markets", "Giant Eagle",
            "Hy-Vee", "Meijer", "Wegmans", "Publix", "H-E-B", "Market Basket",
            "Menards", "Fleet Farm", "Blain's Farm & Fleet", "Rural King",
            "Tractor Supply", "Ace Hardware", "True Value", "Do it Best",
            "Harbor Freight", "Northern Tool", "Grainger", "Fastenal", "MSC",
            
            # Professional Services
            "Booz Allen Hamilton", "MITRE", "Battelle", "SRI International",
            "RAND Corporation", "IHS Markit", "Dun & Bradstreet", "Moody's Analytics",
            "Burns & McDonnell", "Black & Veatch", "CH2M Hill", "HDR Inc",
            "Parsons Corporation", "AECOM", "Jacobs Engineering", "Fluor Corporation",
            "KBR Inc", "Wood Group", "Worley", "McDermott", "TechnipFMC",
            
            # Technology Services
            "EPAM Systems", "Globant", "TTEC", "Concentrix", "Sykes",
            "Teleperformance", "Alorica", "Sitel", "Convergys", "West Corporation",
            "CDW", "Insight", "Connection", "SHI International", "Zones",
            "World Wide Technology", "Presidio", "Datalink", "Optiv", "Trace3",
            "Rackspace", "Liquid Web", "WP Engine", "Kinsta", "SiteGround",
            "Bluehost", "HostGator", "GoDaddy", "Namecheap", "Hover"
        ],
        
        # FAMILY-OWNED BUSINESSES
        "Family Businesses": [
            # Retail Dynasties
            "Wegmans", "Publix", "H-E-B", "Meijer", "Wawa", "Sheetz",
            "QuikTrip", "Casey's General Stores", "Kwik Trip", "Cumberland Farms",
            "RaceTrac", "Pilot Flying J", "Love's Travel Stops", "TravelCenters",
            "Buc-ee's", "Rutter's", "Royal Farms", "GetGo", "Speedway",
            
            # Food Empires
            "Mars Inc", "Ferrero Group", "McCain Foods", "Barilla", "Lavazza",
            "Dr. Oetker", "Bahlsen", "Perfetti Van Melle", "Haribo", "Albanese",
            "Jelly Belly", "See's Candies", "Russell Stover", "Whitman's",
            "Godiva", "Lindt & Sprüngli", "Ghirardelli", "Guittard", "Scharffen Berger",
            
            # Industrial/Manufacturing
            "Koch Industries", "Cargill", "Continental Grain", "Louis Dreyfus",
            "Archer Daniels Midland", "Bunge", "COFCO", "Wilmar", "Olam",
            "Barry Callebaut", "Cémoi", "Valrhona", "Callebaut", "Cacao Barry",
            "Puratos", "Dawn Foods", "Rich Products", "Schwan's Company",
            
            # Construction/Real Estate
            "Bechtel", "Fluor", "Kiewit", "Turner Construction", "Walsh Group",
            "Mortenson", "Gilbane", "Suffolk", "Structure Tone", "Plaza Construction",
            "Related Companies", "Tishman Speyer", "Hines", "JBG Smith",
            "Boston Properties", "Vornado", "SL Green", "Kilroy", "Hudson Pacific",
            
            # Media/Entertainment
            "Advance Publications", "Cox Enterprises", "Hearst Corporation",
            "Tribune Publishing", "McClatchy", "Gannett", "Sinclair Broadcast",
            "Gray Television", "Nexstar", "Tegna", "Meredith Corporation",
            "Rodale", "Houghton Mifflin", "Scholastic", "Chronicle Books"
        ],
        
        # INVESTMENT FUNDS & PRIVATE EQUITY
        "Private Equity Firms": [
            # Mega Buyout Funds
            "Blackstone", "KKR", "Apollo", "Carlyle", "TPG", "Warburg Pincus",
            "Silver Lake", "Vista Equity", "Thoma Bravo", "Francisco Partners",
            "Hellman & Friedman", "Leonard Green", "Providence Equity", "Advent",
            "CVC Capital", "EQT", "Permira", "Apax", "Cinven", "BC Partners",
            "Bain Capital", "Clayton Dubilier & Rice", "GTCR", "Madison Dearborn",
            "Welsh Carson", "New Mountain", "Insight Partners", "General Atlantic",
            
            # Growth Equity
            "Summit Partners", "TA Associates", "Great Hill Partners", "Spectrum Equity",
            "Accel-KKR", "Marlin Equity", "Vector Capital", "Clearlake Capital",
            "Court Square", "Riverside Company", "Audax Group", "Genstar Capital",
            "American Securities", "Arsenal Capital", "Berkshire Partners", "Charlesbank",
            
            # Mid-Market PE
            "H.I.G. Capital", "Sun Capital", "Cerberus", "Platinum Equity",
            "American Industrial Partners", "Wynnchurch Capital", "Spell Capital",
            "Revelstoke Capital", "Shore Capital", "Linden Capital", "Water Street",
            "Frazier Healthcare", "Beecken Petty", "RoundTable Healthcare", "Varsity Healthcare",
            
            # Venture Growth
            "Insight Partners", "Tiger Global", "Coatue", "General Catalyst",
            "IVP", "Bessemer", "Battery Ventures", "Scale Venture Partners",
            "Norwest", "Oak HC/FT", "GGV Capital", "Iconiq Capital",
            "Index Ventures", "Balderton Capital", "Northzone", "Creandum"
        ],
        
        # VENTURE CAPITAL FIRMS
        "Venture Capital": [
            # Tier 1 Silicon Valley
            "Sequoia Capital", "Andreessen Horowitz", "Benchmark", "Greylock",
            "Kleiner Perkins", "Accel", "NEA", "Lightspeed", "Founders Fund",
            "Khosla Ventures", "First Round Capital", "Initialized Capital",
            "Y Combinator", "500 Startups", "Techstars", "Plug and Play",
            
            # Seed/Early Stage
            "Uncork Capital", "Floodgate", "Cowboy Ventures", "Homebrew",
            "Forerunner Ventures", "Primary Ventures", "BBG Ventures",
            "Female Founders Fund", "Backstage Capital", "Precursor Ventures",
            "Hustle Fund", "Pear VC", "Tandem Capital", "Boost VC",
            "Social Capital", "Craft Ventures", "8VC", "Ribbit Capital",
            
            # Vertical Focused
            "Lux Capital", "DCVC", "Fifty Years", "Obvious Ventures",
            "DBL Partners", "Energy Impact Partners", "Clean Energy Ventures",
            "Breakthrough Energy Ventures", "Climate Capital", "Lowercarbon Capital",
            "Rock Health", "7wireVentures", "Healthbox", "StartUp Health",
            "F-Prime Capital", "Venrock", "Third Rock Ventures", "Arch Venture",
            
            # International VCs
            "Atomico", "Balderton", "Index Ventures", "Accel Europe",
            "Northzone", "Creandum", "Point Nine", "HV Capital", "Earlybird",
            "Partech", "Idinvest", "Bpifrance", "Station F", "The Family",
            "LocalGlobe", "Seedcamp", "Episode 1", "Passion Capital", "Mosaic Ventures"
        ],
        
        # HEDGE FUNDS
        "Hedge Funds": [
            # Macro/Multi-Strategy
            "Bridgewater Associates", "Man Group", "Renaissance Technologies",
            "Two Sigma", "Millennium Management", "Citadel", "DE Shaw",
            "Elliott Management", "Baupost Group", "Farallon Capital",
            "Viking Global", "Tiger Global", "Coatue Management", "Lone Pine",
            "Maverick Capital", "Matrix Capital", "Steadfast Capital", "Whale Rock",
            
            # Activist
            "Third Point", "Pershing Square", "ValueAct", "Trian Partners",
            "Starboard Value", "Engine No. 1", "Sachem Head", "Corvex Management",
            "Land & Buildings", "Ancora Advisors", "Legion Partners", "Engaged Capital",
            
            # Quant/Systematic
            "AQR Capital", "PDT Partners", "Jump Trading", "Jane Street",
            "Susquehanna", "DRW Trading", "Optiver", "IMC Trading",
            "Flow Traders", "Virtu Financial", "Tower Research", "Hudson River Trading",
            
            # Credit/Distressed
            "Oaktree Capital", "Ares Management", "Apollo Credit", "Blackstone Credit",
            "GSO Capital", "Avenue Capital", "Fortress Investment", "Angelo Gordon",
            "Davidson Kempner", "Centerbridge Partners", "Silver Point Capital"
        ],
        
        # ACCELERATORS & INCUBATORS
        "Accelerators & Incubators": [
            # Global Programs
            "Y Combinator", "Techstars", "500 Global", "Plug and Play",
            "MassChallenge", "Startupbootcamp", "Founder Institute", "Entrepreneurs Roundtable",
            "AngelPad", "Launchpad LA", "Mucker Capital", "Amplify LA",
            "Science Inc", "Atomic", "Human Ventures", "Expa",
            
            # Corporate Accelerators
            "Google for Startups", "Microsoft for Startups", "AWS Activate",
            "Oracle for Startups", "IBM Ventures", "SAP.iO", "Salesforce Ventures",
            "Adobe for Startups", "NVIDIA Inception", "Intel Ignite", "Qualcomm Ventures",
            "Samsung NEXT", "Sony Innovation Fund", "Comcast Ventures", "Disney Accelerator",
            
            # University Programs
            "Stanford StartX", "Harvard Innovation Labs", "MIT delta v",
            "Berkeley SkyDeck", "Columbia Startup Lab", "NYU Tandon Future Labs",
            "Cornell Tech", "Penn Wharton Entrepreneurship", "Yale Ventures",
            "Princeton Entrepreneurship", "Northwestern Garage", "Duke Innovation",
            
            # Vertical Specific
            "IndieBio", "SOSV", "HAX", "Orbit Startups", "Food-X",
            "Techstars Farm to Fork", "Yield Lab", "Terra Accelerator",
            "Rock Health", "Dreamit Health", "Healthbox", "Blueprint Health",
            "FinTech Innovation Lab", "Barclays Accelerator", "Wells Fargo Accelerator"
        ],
        
        # CONSULTING FIRMS (MID-TIER)
        "Mid-Tier Consulting": [
            # Strategy Boutiques
            "OC&C Strategy", "Simon-Kucher", "Analysis Group", "Cornerstone Research",
            "Charles River Associates", "NERA Economic", "Brattle Group", "Compass Lexecon",
            "FTI Consulting", "Alvarez & Marsal", "AlixPartners", "Ankura",
            "Berkeley Research Group", "Kroll", "Duff & Phelps", "Houlihan Lokey",
            
            # Operations/Implementation
            "North Highland", "West Monroe", "Slalom Consulting", "Point B",
            "Pariveda Solutions", "Credera", "Logic20/20", "Avanade",
            "Sogeti", "CGI", "Fujitsu Consulting", "NTT Data",
            "Stefanini", "UST Global", "Virtusa", "Mindtree",
            
            # Industry Specific
            "ZS Associates", "IQVIA", "Trinity Life Sciences", "Putnam Associates",
            "Campbell Alliance", "Navigant", "Guidehouse", "ICF International",
            "Tetra Tech", "Cadmus Group", "ERG", "Abt Associates",
            "Mathematica", "RAND Corporation", "Urban Institute", "RTI International"
        ],
        
        # REAL ESTATE INVESTMENT
        "Real Estate Investment": [
            # REITs
            "American Tower", "Prologis", "Crown Castle", "Equinix",
            "Public Storage", "Welltower", "Simon Property", "Realty Income",
            "Digital Realty", "Alexandria", "Ventas", "AvalonBay",
            "Equity Residential", "Essex", "MAA", "UDR", "Camden",
            "Boston Properties", "Vornado", "SL Green", "Kilroy", "Douglas Emmett",
            
            # Private Real Estate
            "Blackstone Real Estate", "Brookfield Properties", "Starwood Capital",
            "Colony Capital", "Fortress Real Estate", "Apollo Real Estate",
            "KKR Real Estate", "Carlyle Real Estate", "TPG Real Estate",
            "Lone Star Funds", "Cerberus Real Estate", "Oaktree Real Estate",
            
            # Development Firms
            "Related Companies", "Tishman Speyer", "Hines", "Trammell Crow",
            "Lincoln Property", "JBG Smith", "Forest City", "Mack-Cali",
            "Vornado", "SL Green", "Boston Properties", "Kilroy",
            "Howard Hughes Corporation", "Brookfield Properties", "Silverstein Properties"
        ],
        
        # SPECIALTY FINANCE
        "Specialty Finance": [
            # Alternative Lenders
            "Ares Capital", "FS KKR Capital", "Owl Rock Capital", "Golub Capital",
            "Barings BDC", "Main Street Capital", "Hercules Capital", "TriplePoint",
            "PennantPark", "BlackRock TCP Capital", "Apollo Investment", "Prospect Capital",
            
            # Fintech Lenders
            "SoFi", "Upstart", "Affirm", "Avant", "LendingClub",
            "Prosper", "Funding Circle", "OnDeck", "Kabbage", "BlueVine",
            "Fundbox", "PayPal Working Capital", "Square Capital", "Stripe Capital",
            
            # Equipment Finance
            "GATX", "Trinity Industries", "AerCap", "Air Lease Corporation",
            "Textainer", "Triton International", "CAI International", "Element Fleet",
            "Ryder", "Penske Truck Leasing", "AMERCO", "United Rentals",
            
            # Mortgage REITs
            "Annaly Capital", "AGNC Investment", "Starwood Property Trust",
            "Blackstone Mortgage Trust", "Arbor Realty Trust", "Ladder Capital",
            "Granite Point Mortgage", "Ready Capital", "Redwood Trust", "Two Harbors"
        ],
        
        # ENERGY & CLEANTECH
        "Energy & CleanTech": [
            # Renewable Energy Developers
            "NextEra Energy Resources", "Pattern Energy", "Avangrid Renewables",
            "Invenergy", "EDF Renewables", "Enel Green Power", "Iberdrola Renewables",
            "Orsted", "RWE Renewables", "Engie Green", "Brookfield Renewable",
            "Clearway Energy", "Cypress Creek Renewables", "Pine Gate Renewables",
            
            # Solar Companies
            "Sunrun", "Sunnova", "Vivint Solar", "Tesla Solar", "SunPower",
            "First Solar", "Enphase Energy", "SolarEdge", "Array Technologies",
            "Shoals Technologies", "FTC Solar", "Nextracker", "Maxeon Solar",
            
            # Energy Storage
            "Fluence", "Wartsila Energy", "Tesla Energy", "LG Energy Solution",
            "BYD Energy", "Saft", "Nidec", "Stem", "Plus Power",
            "Form Energy", "ESS Inc", "Energy Vault", "Ambri",
            
            # EV Infrastructure
            "ChargePoint", "EVgo", "Electrify America", "Blink Charging",
            "Volta", "FreeWire", "Beam Global", "Wallbox", "Allego",
            "Ionity", "Fastned", "Greenlots", "EV Connect", "SemaConnect"
        ],
        
        # BIOTECH & LIFE SCIENCES
        "Biotech & Life Sciences": [
            # Biotech Leaders
            "Genentech", "Amgen", "Gilead", "Biogen", "Regeneron",
            "Vertex", "Alexion", "BioMarin", "Incyte", "Alkermes",
            "Nektar", "Exelixis", "United Therapeutics", "Jazz Pharmaceuticals",
            "Horizon Therapeutics", "Catalent", "Charles River Labs", "ICON",
            
            # Emerging Biotech
            "Moderna", "BioNTech", "CureVac", "Novavax", "Valneva",
            "Beam Therapeutics", "Intellia", "CRISPR Therapeutics", "Editas Medicine",
            "Bluebird Bio", "Sangamo", "Rocket Pharmaceuticals", "Krystal Biotech",
            
            # Medical Devices
            "Intuitive Surgical", "Edwards Lifesciences", "Boston Scientific",
            "Stryker", "Zimmer Biomet", "Smith & Nephew", "ConMed",
            "Globus Medical", "NuVasive", "Alphatec", "SI-Bone", "Orthofix",
            "AtriCure", "Axonics", "Nevro", "Inspire Medical", "Tandem Diabetes",
            
            # Diagnostics
            "Illumina", "Thermo Fisher", "Danaher", "Roche Diagnostics",
            "Abbott Diagnostics", "Bio-Rad", "Waters", "Agilent",
            "PerkinElmer", "Bruker", "Mettler Toledo", "Sartorius"
        ]
    }

def main():
    companies = get_massive_company_list()
    
    # Count total
    total = sum(len(v) for v in companies.values())
    print(f"Total companies in massive list: {total}")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/logos/massive_company_list.txt', 'w') as f:
        for category, company_list in companies.items():
            f.write(f"\n## {category}\n")
            for company in company_list:
                f.write(f"{company}\n")
    
    print("Saved to massive_company_list.txt")

if __name__ == "__main__":
    main()