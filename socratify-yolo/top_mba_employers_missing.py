#!/usr/bin/env python3
"""
Top MBA employers we're missing - Essential companies for business school students
"""

def get_missing_top_employers():
    return {
        # TOP CONSULTING FIRMS (MUST HAVE!)
        "Management Consulting": [
            "McKinsey & Company", "Boston Consulting Group", "Bain & Company",
            "Oliver Wyman", "Strategy&", "Booz Allen Hamilton", "Kearney",
            "Roland Berger", "LEK Consulting", "Simon-Kucher", "ZS Associates",
            "Parthenon-EY", "Monitor Deloitte", "Strategy& (PwC)", "BCG Digital Ventures",
            "McKinsey Digital", "BCG GAMMA", "Bain Vector", "OC&C Strategy Consultants",
            "Marakon", "Cornerstone Research", "Charles River Associates",
            "NERA Economic Consulting", "Brattle Group", "FTI Consulting",
            "Huron Consulting", "West Monroe", "North Highland", "Slalom Consulting",
            "Prophet", "Innosight", "Clayton Christensen Institute", "IDEO",
            "Frog Design", "Doblin", "Fahrenheit 212", "R/GA", "Huge",
            "Sapient", "Publicis Sapient", "Capgemini Invent", "PA Consulting"
        ],
        
        # INVESTMENT BANKS & PRIVATE EQUITY
        "Investment Banking": [
            "Lazard", "Evercore", "Centerview Partners", "Moelis & Company",
            "Perella Weinreb Partners", "PJT Partners", "Qatalyst Partners",
            "Greenhill & Co", "Rothschild & Co", "Jefferies", "Guggenheim Partners",
            "Houlihan Lokey", "William Blair", "Robert W. Baird", "Piper Sandler",
            "Raymond James", "Stifel", "RBC Capital Markets", "BMO Capital Markets",
            "TD Securities", "CIBC Capital Markets", "Scotiabank", "Macquarie",
            "Nomura", "Mizuho", "SMBC Nikko", "Daiwa", "CLSA", "Citic Securities"
        ],
        
        "Private Equity & Venture Capital": [
            "Blackstone", "KKR", "Carlyle Group", "Apollo Global Management",
            "TPG Capital", "Warburg Pincus", "Silver Lake", "Vista Equity Partners",
            "Thoma Bravo", "Francisco Partners", "Hellman & Friedman", "Leonard Green",
            "CVC Capital Partners", "EQT", "Permira", "Cinven", "Bridgepoint",
            "Advent International", "Bain Capital", "BC Partners", "CD&R",
            "General Atlantic", "Insight Partners", "Tiger Global", "Coatue",
            "Andreessen Horowitz", "Benchmark", "Greylock Partners", "Bessemer",
            "Lightspeed Venture Partners", "Menlo Ventures", "Norwest Venture Partners"
        ],
        
        # BIG TECH & EMERGING TECH
        "Tech Giants & Unicorns": [
            "Databricks", "Snowflake", "Palantir", "Roblox", "Unity",
            "Epic Games", "Discord", "Notion", "Figma", "Miro", "Airtable",
            "Zapier", "Calendly", "Grammarly", "Canva", "Atlassian",
            "Twilio", "SendGrid", "Segment", "Amplitude", "Mixpanel",
            "Heap", "FullStory", "Optimizely", "LaunchDarkly", "PagerDuty",
            "Datadog", "New Relic", "Splunk", "Elastic", "Grafana",
            "HashiCorp", "GitLab", "JFrog", "CircleCI", "Travis CI",
            "Vercel", "Netlify", "Heroku", "DigitalOcean", "Linode",
            "Cloudflare", "Fastly", "Akamai", "Imperva", "Palo Alto Networks",
            "CrowdStrike", "SentinelOne", "Zscaler", "Okta", "Auth0",
            "1Password", "LastPass", "Dashlane", "NordVPN", "ExpressVPN"
        ],
        
        # FAANG+ AND MAJOR TECH
        "Major Tech Companies": [
            "ByteDance", "TikTok", "Baidu", "Alibaba Cloud", "Tencent Cloud",
            "Xiaomi", "Oppo", "Vivo", "OnePlus", "Nothing", "Realme",
            "DJI", "Huawei", "Honor", "ZTE", "Lenovo", "ASUS", "MSI",
            "Razer", "Logitech", "Corsair", "SteelSeries", "HyperX",
            "Western Digital", "Seagate", "Kingston", "Crucial", "G.Skill",
            "AMD", "Intel", "Qualcomm", "Broadcom", "Marvell", "MediaTek",
            "Texas Instruments", "Analog Devices", "Maxim Integrated", "Xilinx"
        ],
        
        # CPG & RETAIL GIANTS
        "Consumer Goods & Retail": [
            "Unilever", "Procter & Gamble", "Nestle", "PepsiCo", "Coca-Cola",
            "Diageo", "Heineken", "AB InBev", "Carlsberg", "Pernod Ricard",
            "Brown-Forman", "Constellation Brands", "Molson Coors", "Kirin",
            "Asahi", "Suntory", "Red Bull", "Monster Energy", "Celsius",
            "L'Oreal", "Estee Lauder", "Shiseido", "Coty", "Revlon",
            "LVMH", "Kering", "Hermes", "Chanel", "Richemont", "Swatch Group",
            "Tiffany & Co", "Cartier", "Bulgari", "Van Cleef & Arpels",
            "Nike", "Adidas", "Puma", "Under Armour", "New Balance",
            "ASICS", "Reebok", "Converse", "Vans", "The North Face",
            "Patagonia", "Columbia", "Arc'teryx", "Mammut", "Black Diamond"
        ],
        
        # PHARMA & HEALTHCARE
        "Pharmaceutical & Healthcare": [
            "Johnson & Johnson", "Pfizer", "Merck", "AbbVie", "Amgen",
            "Gilead Sciences", "Biogen", "Regeneron", "Vertex", "Alexion",
            "Bristol Myers Squibb", "Eli Lilly", "AstraZeneca", "GSK", "Sanofi",
            "Novartis", "Roche", "Bayer", "Takeda", "Astellas", "Daiichi Sankyo",
            "Novo Nordisk", "Teva", "Mylan", "Sandoz", "Dr. Reddy's",
            "Sun Pharma", "Cipla", "Lupin", "Aurobindo", "Glenmark",
            "UnitedHealth", "Anthem", "Aetna", "Cigna", "Humana",
            "Centene", "Molina", "WellCare", "Oscar Health", "Clover Health"
        ],
        
        # AUTOMOTIVE & MOBILITY
        "Automotive & Future Mobility": [
            "Tesla", "Rivian", "Lucid Motors", "Nio", "Xpeng", "Li Auto",
            "BYD", "Geely", "Great Wall Motors", "Stellantis", "Renault",
            "Peugeot", "Citroen", "Fiat", "Alfa Romeo", "Maserati", "Ferrari",
            "Lamborghini", "Bentley", "Rolls-Royce", "McLaren", "Aston Martin",
            "Porsche", "Audi", "Mercedes-Benz", "BMW", "Volkswagen",
            "Volvo", "Polestar", "Lynk & Co", "Genesis", "Hyundai", "Kia",
            "Waymo", "Cruise", "Argo AI", "Aurora", "Zoox", "Nuro",
            "TuSimple", "Embark", "Plus", "Kodiak Robotics", "Einride"
        ],
        
        # FINTECH & DIGITAL FINANCE
        "Fintech & Digital Banking": [
            "Stripe", "Square", "PayPal", "Adyen", "Klarna", "Afterpay",
            "Affirm", "Sezzle", "Quadpay", "Splitit", "Wise", "Revolut",
            "N26", "Monzo", "Starling Bank", "Chime", "Varo", "Current",
            "Dave", "Albert", "Brigit", "Earnin", "MoneyLion", "SoFi",
            "Robinhood", "Webull", "eToro", "Plus500", "IG Group",
            "Coinbase", "Binance", "Kraken", "Gemini", "FTX", "Crypto.com",
            "BlockFi", "Celsius", "Nexo", "Ledn", "Ripple", "Circle"
        ],
        
        # AEROSPACE & DEFENSE
        "Aerospace & Defense": [
            "SpaceX", "Blue Origin", "Virgin Galactic", "Rocket Lab",
            "Relativity Space", "Firefly Aerospace", "Astra", "ABL Space",
            "Boeing", "Airbus", "Lockheed Martin", "Northrop Grumman",
            "Raytheon Technologies", "General Dynamics", "L3Harris",
            "BAE Systems", "Thales", "Leonardo", "Saab", "Dassault",
            "Embraer", "Bombardier", "Gulfstream", "Cessna", "Beechcraft",
            "Bell", "Sikorsky", "Leonardo Helicopters", "Airbus Helicopters"
        ],
        
        # ENERGY & SUSTAINABILITY
        "Clean Energy & Sustainability": [
            "NextEra Energy", "Orsted", "Iberdrola", "Enel Green Power",
            "EDF Renewables", "Engie", "RWE", "E.ON", "Vattenfall",
            "First Solar", "SunPower", "Canadian Solar", "JinkoSolar",
            "Trina Solar", "LONGi Solar", "Enphase Energy", "SolarEdge",
            "Vestas", "Siemens Gamesa", "GE Renewable Energy", "Nordex",
            "Goldwind", "Suzlon", "Enercon", "Senvion", "Tesla Energy",
            "Sunrun", "Vivint Solar", "Sunnova", "ChargePoint", "EVgo",
            "Electrify America", "Ionity", "Fastned", "Allego", "EVBox"
        ],
        
        # MEDIA & ENTERTAINMENT
        "Media & Entertainment": [
            "Netflix", "Disney+", "HBO Max", "Paramount+", "Peacock",
            "Apple TV+", "Amazon Prime Video", "Hulu", "Discovery+",
            "Spotify", "Apple Music", "YouTube Music", "Tidal", "Deezer",
            "SoundCloud", "Bandcamp", "Audiomack", "TuneIn", "iHeartRadio",
            "Activision Blizzard", "Electronic Arts", "Take-Two", "Ubisoft",
            "Epic Games", "Valve", "Riot Games", "Supercell", "Zynga",
            "Roblox Corporation", "Unity Technologies", "Unreal Engine"
        ],
        
        # LOGISTICS & SUPPLY CHAIN
        "Logistics & Supply Chain": [
            "DHL", "FedEx", "UPS", "Maersk", "MSC", "CMA CGM", "Hapag-Lloyd",
            "ONE", "Evergreen", "COSCO", "Yang Ming", "HMM", "ZIM",
            "DB Schenker", "Kuehne + Nagel", "DSV", "C.H. Robinson",
            "Expeditors", "XPO Logistics", "J.B. Hunt", "Schneider National",
            "Knight-Swift", "Old Dominion", "Saia", "Estes Express",
            "YRC Worldwide", "ABF Freight", "R+L Carriers", "Southeastern Freight"
        ],
        
        # REAL ESTATE & CONSTRUCTION
        "Real Estate & PropTech": [
            "CBRE", "JLL", "Cushman & Wakefield", "Colliers", "Newmark",
            "Marcus & Millichap", "Eastdil Secured", "HFF", "Savills",
            "Prologis", "Public Storage", "Welltower", "Equity Residential",
            "AvalonBay", "Essex Property Trust", "UDR", "Mid-America",
            "WeWork", "IWG", "Industrious", "Knotel", "Convene",
            "Zillow", "Redfin", "Opendoor", "Offerpad", "Compass",
            "Airbnb", "Vrbo", "Booking.com", "Expedia", "Tripadvisor"
        ],
        
        # INSURANCE & FINANCIAL SERVICES
        "Insurance & Asset Management": [
            "AIG", "Chubb", "Travelers", "Hartford", "Progressive", "Geico",
            "State Farm", "Allstate", "Liberty Mutual", "Nationwide",
            "MetLife", "Prudential", "New York Life", "Northwestern Mutual",
            "MassMutual", "Guardian Life", "Principal", "Lincoln Financial",
            "BlackRock", "Vanguard", "Fidelity", "State Street", "Invesco",
            "Franklin Templeton", "T. Rowe Price", "AllianceBernstein",
            "Schroders", "Aberdeen", "Janus Henderson", "Legg Mason"
        ]
    }

def main():
    companies = get_missing_top_employers()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = list(set(all_companies))
    
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Categories: {len(companies)}")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/top_mba_employers_list.txt', 'w') as f:
        for category, company_list in companies.items():
            f.write(f"\n## {category}\n")
            for company in company_list:
                f.write(f"{company}\n")
    
    print("Saved to top_mba_employers_list.txt")
    
    return unique_companies

if __name__ == "__main__":
    main()