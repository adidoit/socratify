#!/usr/bin/env python3
"""
Comprehensive Modern Companies Database 2025
200+ AI, tech startups, and modern companies people want to work for
"""

def get_comprehensive_modern_companies():
    """Comprehensive list of modern companies across all categories"""
    return {
        # AI & Machine Learning - Foundation Models & LLMs
        "AI_Foundation_Models": [
            "Cohere", "AI21 Labs", "Adept", "Inflection AI", "Character AI", "Stability AI",
            "Runway", "Midjourney", "Leonardo AI", "Jasper", "Copy AI", "Writesonic",
            "Claude AI", "Poe", "You.com", "Phind", "Perplexity AI", "Mistral AI",
            "Together AI", "Fireworks AI", "Replicate", "Modal", "Banana", "OctoML"
        ],
        
        # AI Agents & Automation
        "AI_Agents_Automation": [
            "Cognition Labs", "Devin AI", "Magic AI", "Poolside", "Cursor", "Replit",
            "GitHub Copilot", "Tabnine", "Sourcegraph", "CodeWhisperer", "Codium AI",
            "Mintlify", "Sweep AI", "Codeium", "Continue", "Aider", "SWE-agent",
            "Agent GPT", "LangChain", "LlamaIndex", "Semantic Kernel", "CrewAI"
        ],
        
        # AI Infrastructure & MLOps
        "AI_Infrastructure_MLOps": [
            "Weights & Biases", "MLflow", "Neptune AI", "ClearML", "Comet ML", "Dagster",
            "Prefect", "Airflow", "Great Expectations", "DVC", "Feast", "Tecton",
            "Qdrant", "Pinecone", "Weaviate", "Chroma", "Milvus", "Vald", "LanceDB",
            "Modal", "RunPod", "Lambda Labs", "CoreWeave", "Together AI", "Anyscale"
        ],
        
        # Developer Tools & Productivity
        "Developer_Tools": [
            "Linear", "Height", "Notion", "Obsidian", "Roam Research", "Logseq",
            "Figma", "Framer", "Webflow", "Bubble", "Retool", "Internal", "Airplane",
            "GitLab", "GitKraken", "Sourcetree", "Tower", "Fork", "SmartGit",
            "Vercel", "Netlify", "Railway", "Render", "Fly.io", "PlanetScale", "Supabase"
        ],
        
        # Fintech & Payments
        "Fintech_Payments": [
            "Stripe", "Plaid", "Dwolla", "Circle", "Ripple", "Paxos", "Anchorage",
            "Fireblocks", "BitGo", "Chainalysis", "Elliptic", "TRM Labs", "Coinbase",
            "Binance US", "Kraken", "Gemini", "FTX", "Robinhood", "Webull", "M1 Finance",
            "SoFi", "Chime", "Current", "Varo", "Dave", "MoneyLion", "Credit Karma"
        ],
        
        # Healthcare & Biotech
        "Healthcare_Biotech": [
            "23andMe", "Color Genomics", "Invitae", "Myriad Genetics", "Foundation Medicine",
            "Guardant Health", "Natera", "Veracyte", "10x Genomics", "Illumina",
            "Oxford Nanopore", "Pacific Biosciences", "Twist Bioscience", "Synthetic Genomics",
            "Ginkgo Bioworks", "Modern Meadow", "Perfect Day", "Memphis Meats", "Impossible Foods"
        ],
        
        # Climate Tech & Sustainability
        "Climate_Tech": [
            "Tesla Energy", "Rivian", "Lucid Motors", "Canoo", "Fisker", "Polestar",
            "QuantumScape", "Solid Power", "Sila Nanotechnologies", "StoreDot", "CATL",
            "Northvolt", "Form Energy", "ESS Tech", "Ambri", "Malta", "Energy Vault",
            "Commonwealth Fusion", "Helion Energy", "TAE Technologies", "General Fusion"
        ],
        
        # Consumer & Social
        "Consumer_Social": [
            "Discord", "Clubhouse", "BeReal", "Lemon8", "Mastodon", "Bluesky", "Post",
            "Substack", "ConvertKit", "Ghost", "Medium", "LinkedIn Creator", "Patreon",
            "OnlyFans", "Cameo", "Gumroad", "Teachable", "Thinkific", "Circle",
            "Mighty Networks", "Geneva", "Partiful", "IRL", "Punchbowl", "Evite"
        ],
        
        # Enterprise Software & Productivity
        "Enterprise_Software": [
            "Monday.com", "Asana", "Clickup", "Airtable", "Smartsheet", "Coda", "Basecamp",
            "Slack", "Microsoft Teams", "Zoom", "Google Workspace", "Atlassian", "JetBrains",
            "IntelliJ", "DataDog", "New Relic", "Splunk", "Elastic", "Grafana", "PagerDuty"
        ],
        
        # E-commerce & Marketplaces
        "Ecommerce_Marketplaces": [
            "Shopify", "BigCommerce", "WooCommerce", "Magento", "Squarespace", "Wix",
            "Amazon Seller Central", "Etsy", "eBay", "Facebook Marketplace", "Instagram Shopping",
            "TikTok Shop", "Pinterest Business", "Snapchat Ads", "Twitter Commerce", "YouTube Shopping"
        ],
        
        # Gaming & Entertainment
        "Gaming_Entertainment": [
            "Unity", "Unreal Engine", "Godot", "GameMaker", "Construct", "Defold",
            "Roblox", "Minecraft", "Fortnite", "Among Us", "Fall Guys", "Apex Legends",
            "PUBG", "Call of Duty", "Overwatch", "League of Legends", "Dota 2", "Counter-Strike"
        ],
        
        # European Tech Unicorns
        "European_Tech": [
            "Revolut", "Monzo", "Starling Bank", "N26", "Bunq", "Qonto", "Penta",
            "Klarna", "Afterpay", "Sezzle", "Affirm", "Zip", "Tabby", "Tamara",
            "Spotify", "SoundCloud", "Deezer", "Tidal", "Bandcamp", "DistroKid",
            "UiPath", "Automation Anywhere", "Blue Prism", "WorkFusion", "Kryon", "NICE"
        ],
        
        # Asian Tech Companies
        "Asian_Tech": [
            "ByteDance", "TikTok", "Douyin", "Toutiao", "Lark", "CapCut", "Resso",
            "Grab", "Gojek", "Sea Limited", "Shopee", "Garena", "Tokopedia", "Bukalapak",
            "Traveloka", "OYO", "RedDoorz", "Agoda", "Booking.com", "Expedia"
        ],
        
        # Indian Tech Unicorns
        "Indian_Tech": [
            "Flipkart", "Paytm", "Zomato", "Swiggy", "Ola", "Uber India", "Rapido",
            "BYJU'S", "Unacademy", "Vedantu", "WhiteHat Jr", "Toppr", "Doubtnut",
            "Dream11", "MPL", "WinZO", "Ludo King", "Teen Patti Gold", "RummyCircle"
        ],
        
        # Israeli Tech Companies
        "Israeli_Tech": [
            "Wix", "Monday.com", "Fiverr", "JFrog", "Check Point", "CyberArk", "Palo Alto Networks",
            "SentinelOne", "Snyk", "Armis", "Claroty", "Cybereason", "Guardicore", "Aqua Security",
            "Mobileye", "OrCam", "Vayyar", "UVeye", "Cognata", "Innoviz", "AImotive"
        ],
        
        # Canadian Tech Companies  
        "Canadian_Tech": [
            "Shopify", "Corel", "BlackBerry", "OpenText", "CGI", "Constellation Software",
            "Nuvei", "Mogo", "Paymi", "MorningStar", "Wave", "FreshBooks", "Hootsuite"
        ],
        
        # Australian Tech Companies
        "Australian_Tech": [
            "Canva", "Atlassian", "Xero", "Campaign Monitor", "99designs", "Envato",
            "SafetyCulture", "Deputy", "Employment Hero", "Culture Amp", "Procurify", "Koala"
        ],
        
        # Latin American Tech
        "Latin_American_Tech": [
            "MercadoLibre", "PagSeguro", "Stone", "StoneCo", "Nubank", "Banco Inter",
            "Rappi", "iFood", "Cornershop", "Loggi", "99", "Cabify", "Beat", "Didi"
        ],
        
        # African Tech Companies
        "African_Tech": [
            "Jumia", "Konga", "Flutterwave", "Paystack", "Interswitch", "OPay", "PalmPay",
            "M-Pesa", "Tala", "Branch", "Carbon", "FairMoney", "Renmoney", "Cowrywise"
        ],
        
        # Crypto & Web3
        "Crypto_Web3": [
            "OpenSea", "LooksRare", "Magic Eden", "Foundation", "SuperRare", "Async Art",
            "Uniswap", "SushiSwap", "PancakeSwap", "dYdX", "Compound", "Aave", "Curve",
            "Chainlink", "The Graph", "Polygon", "Arbitrum", "Optimism", "StarkWare", "zkSync"
        ],
        
        # AR/VR & Spatial Computing
        "AR_VR_Spatial": [
            "Meta Reality Labs", "Apple Vision Pro", "Microsoft HoloLens", "Magic Leap",
            "Varjo", "Pico Interactive", "Nreal", "Vuzix", "Epson Moverio", "RealWear",
            "Unity XR", "Unreal Engine VR", "WebXR", "A-Frame", "8th Wall", "Niantic"
        ],
        
        # Quantum Computing
        "Quantum_Computing": [
            "IBM Quantum", "Google Quantum AI", "Microsoft Azure Quantum", "Amazon Braket",
            "IonQ", "Rigetti", "PsiQuantum", "Xanadu", "D-Wave", "Cambridge Quantum Computing",
            "Pasqal", "QuEra", "Atom Computing", "Alpine Quantum Technologies", "IQM"
        ],
        
        # Space Tech
        "Space_Tech": [
            "SpaceX", "Blue Origin", "Virgin Galactic", "Virgin Orbit", "Rocket Lab",
            "Relativity Space", "Firefly Aerospace", "Astra", "Vector Launch", "ABL Space",
            "Planet Labs", "Maxar", "BlackSky", "Capella Space", "Iceye", "Spire Global"
        ],
        
        # Autonomous Vehicles & Transportation  
        "Autonomous_Transportation": [
            "Waymo", "Cruise", "Aurora", "Argo AI", "Motional", "Zoox", "Nuro", "Embark",
            "Plus", "TuSimple", "Kodiak Robotics", "Einride", "Gatik", "May Mobility",
            "Optimus Ride", "Local Motors", "EasyMile", "Navya", "2getthere", "Sensible 4"
        ],
        
        # IoT & Connected Devices
        "IoT_Connected": [
            "Ring", "Nest", "Ecobee", "Honeywell", "SmartThings", "Hubitat", "Wink",
            "Philips Hue", "LIFX", "Nanoleaf", "TP-Link Kasa", "Wyze", "Arlo", "SimpliSafe"
        ],
        
        # Food Tech & Agriculture
        "Food_AgTech": [
            "Beyond Meat", "Impossible Foods", "Oatly", "NotCo", "Perfect Day", "Clara Foods",
            "Memphis Meats", "GOOD Meat", "Eat Just", "New Wave Foods", "Ocean Hugger Foods",
            "John Deere", "CNH Industrial", "AGCO", "Trimble", "Raven Industries", "Precision Planting"
        ],
        
        # Travel & Hospitality Tech
        "Travel_Hospitality": [
            "Airbnb", "VRBO", "HomeAway", "Sonder", "RedAwning", "TurnKey", "AvantStay",
            "Expedia", "Booking.com", "Agoda", "Hotels.com", "Trivago", "Kayak", "Skyscanner"
        ],
        
        # Real Estate & PropTech
        "Real_Estate_PropTech": [
            "Zillow", "Redfin", "Compass", "Opendoor", "iBuyer", "Offerpad", "RedfinNow",
            "Divvy Homes", "Landed", "Point", "Haus", "Ribbon", "Flyhomes", "Better.com"
        ],
        
        # HR Tech & People Analytics
        "HR_Tech": [
            "BambooHR", "Workday", "ADP", "Paycom", "Paychex", "Gusto", "Rippling",
            "Lattice", "15Five", "Culture Amp", "Glint", "TinyPulse", "Officevibe", "Bonusly"
        ],
        
        # Marketing & AdTech
        "Marketing_AdTech": [
            "HubSpot", "Marketo", "Pardot", "Eloqua", "Mailchimp", "Constant Contact",
            "ConvertKit", "ActiveCampaign", "Drip", "GetResponse", "AWeber", "Campaign Monitor"
        ],
        
        # Legal Tech
        "Legal_Tech": [
            "LegalZoom", "Rocket Lawyer", "LawDepot", "Nolo", "Avvo", "Martindale-Hubbell",
            "Clio", "MyCase", "PracticePanther", "TimeSolv", "CosmoLex", "Smokeball"
        ],
        
        # Education Tech
        "Education_Tech": [
            "Coursera", "Udemy", "edX", "Khan Academy", "Skillshare", "MasterClass",
            "Pluralsight", "LinkedIn Learning", "Udacity", "Treehouse", "CodePen", "Repl.it"
        ],
        
        # Supply Chain & Logistics
        "Supply_Chain_Logistics": [
            "Flexport", "Convoy", "Uber Freight", "C.H. Robinson", "J.B. Hunt", "Schneider",
            "FedEx", "UPS", "DHL", "Amazon Logistics", "ShipBob", "Shippo", "EasyShip"
        ],
        
        # Security & Compliance
        "Security_Compliance": [
            "Okta", "Auth0", "Ping Identity", "OneLogin", "SailPoint", "CyberArk",
            "1Password", "LastPass", "Bitwarden", "Dashlane", "Keeper", "RoboForm"
        ],
        
        # Data & Analytics  
        "Data_Analytics": [
            "Snowflake", "Databricks", "Palantir", "Tableau", "Power BI", "Looker",
            "Qlik", "Sisense", "ThoughtSpot", "Domo", "Chartio", "Periscope Data"
        ]
    }

def main():
    companies_dict = get_comprehensive_modern_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"COMPREHENSIVE MODERN COMPANIES DATABASE 2025")
    print(f"=" * 50)
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    # Save comprehensive list
    with open('/Users/adi/code/socratify/socratify-yolo/comprehensive_modern_companies_2025.txt', 'w') as f:
        f.write("COMPREHENSIVE MODERN COMPANIES DATABASE 2025\\n")
        f.write("=" * 60 + "\\n\\n")
        f.write(f"Total unique companies: {len(unique_companies)}\\n")
        f.write(f"Categories: {len(companies_dict)}\\n\\n")
        
        for category, companies in companies_dict.items():
            f.write(f"\\n### {category.upper().replace('_', ' ')} ###\\n")
            for company in companies:
                f.write(f"  - {company}\\n")
        
        f.write(f"\\n\\n### ALPHABETICAL MASTER LIST ###\\n")
        for i, company in enumerate(unique_companies, 1):
            f.write(f"{i:4d}. {company}\\n")
    
    print("Saved to comprehensive_modern_companies_2025.txt")
    return unique_companies

if __name__ == "__main__":
    main()