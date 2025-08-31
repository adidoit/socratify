#!/usr/bin/env python3
"""
Check Goldman Sachs industry report style analysis for missing companies
Deep dive into GS research coverage universe
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

def get_goldman_sachs_research_universe():
    """Goldman Sachs research coverage universe - detailed industry analysis"""
    return {
        "Software_Internet": [
            # Cloud Infrastructure & SaaS
            "Microsoft", "Amazon Web Services", "Google Cloud", "Salesforce", "ServiceNow",
            "Snowflake", "Databricks", "MongoDB", "Elastic", "Confluent", "HashiCorp",
            "GitLab", "JFrog", "Okta", "Auth0", "Ping Identity", "SentinelOne",
            
            # Enterprise Software  
            "Oracle", "SAP", "Workday", "Adobe", "Intuit", "Autodesk", "PTC",
            "Ansys", "Synopsys", "Cadence Design", "Atlassian", "Asana", "Monday.com",
            "Notion", "Airtable", "Figma", "Canva", "Slack", "Zoom", "Microsoft Teams",
            
            # E-commerce & Digital Platforms
            "Shopify", "WooCommerce", "BigCommerce", "Magento", "Squarespace", "Wix",
            "WordPress", "Drupal", "Webflow", "Bubble", "OutSystems",
            
            # Cybersecurity
            "CrowdStrike", "Palo Alto Networks", "Fortinet", "Check Point", "Zscaler",
            "Okta", "Ping Identity", "Rapid7", "Qualys", "Tenable", "Varonis",
            "Cyberark", "Proofpoint", "Mimecast", "Symantec", "McAfee", "Trend Micro"
        ],
        
        "Financial_Technology": [
            # Digital Payments
            "PayPal", "Block", "Stripe", "Adyen", "Worldpay", "Fiserv", "Global Payments",
            "Klarna", "Affirm", "Afterpay", "Sezzle", "Zip Co", "Paymi", "Zelle",
            
            # Digital Banking & Lending
            "Chime", "Current", "Varo", "Dave", "MoneyLion", "SoFi", "Upstart",
            "LendingClub", "Prosper", "Funding Circle", "Kabbage", "OnDeck",
            "Revolut", "N26", "Monzo", "Starling Bank", "Nubank", "Neon",
            
            # Crypto & Blockchain
            "Coinbase", "Binance", "Kraken", "FTX", "Gemini", "Bitfinex", "Huobi",
            "Chainalysis", "Circle", "Ripple", "ConsenSys", "Alchemy", "Infura",
            
            # WealthTech & InsurTech
            "Robinhood", "E*TRADE", "TD Ameritrade", "Charles Schwab", "Fidelity",
            "Betterment", "Wealthfront", "Acorns", "Stash", "M1 Finance",
            "Lemonade", "Root Insurance", "Metromile", "Oscar Health", "Clover Health"
        ],
        
        "Healthcare_Life_Sciences": [
            # Digital Health & Telemedicine
            "Teladoc", "Amwell", "MDLive", "PlushCare", "Doctor on Demand", "98point6",
            "Babylon Health", "Ping An Good Doctor", "JD Health", "Alibaba Health",
            
            # Health Tech Platforms
            "Veracyte", "10x Genomics", "Illumina", "Pacific Biosciences", "Oxford Nanopore",
            "Guardant Health", "Foundation Medicine", "Tempus", "Flatiron Health",
            "Livongo", "Dexcom", "Abbott FreeStyle", "Medtronic MiniMed",
            
            # Biotech & Pharma Tools
            "Moderna", "BioNTech", "Novavax", "CureVac", "Translate Bio", "Arcturus",
            "Alnylam", "Ionis Pharmaceuticals", "Sarepta", "Biogen", "Genmab",
            "Seagen", "Gilead", "Vertex", "BioMarin", "Alexion", "Regeneron",
            
            # Medical Devices & Equipment
            "Intuitive Surgical", "Stryker", "Zimmer Biomet", "Smith & Nephew",
            "Boston Scientific", "Edwards Lifesciences", "Abbott", "Medtronic",
            "Becton Dickinson", "Danaher", "Thermo Fisher", "Agilent", "Waters",
            
            # Healthcare Services & HCIT
            "UnitedHealth", "Anthem", "Cigna", "Humana", "Centene", "Molina",
            "Epic Systems", "Cerner", "Allscripts", "athenahealth", "Veeva Systems"
        ],
        
        "Media_Entertainment_Gaming": [
            # Streaming & Content
            "Netflix", "Disney+", "HBO Max", "Amazon Prime Video", "Apple TV+",
            "Paramount+", "Peacock", "Hulu", "YouTube TV", "Sling TV", "fuboTV",
            "Spotify", "Apple Music", "Amazon Music", "YouTube Music", "Pandora",
            "SiriusXM", "Audible", "Scribd", "MasterClass", "Skillshare",
            
            # Gaming & Interactive
            "Unity Technologies", "Unreal Engine", "Roblox", "Epic Games", "Valve",
            "Electronic Arts", "Activision Blizzard", "Take-Two Interactive", "Ubisoft",
            "CD Projekt", "Bungie", "Riot Games", "Supercell", "King Digital",
            "Zynga", "Glu Mobile", "Playtika", "AppLovin", "ironSource",
            
            # Social Media & Creator Economy
            "Meta", "TikTok", "Snapchat", "Twitter", "Pinterest", "Reddit",
            "Discord", "Clubhouse", "Twitch", "YouTube", "OnlyFans", "Patreon",
            "Substack", "Medium", "Ghost", "ConvertKit", "Mailchimp"
        ],
        
        "Consumer_Retail_Ecommerce": [
            # E-commerce Platforms
            "Amazon", "Alibaba", "JD.com", "Pinduoduo", "Shopee", "Lazada",
            "MercadoLibre", "Flipkart", "Myntra", "BigBasket", "Instacart",
            "DoorDash", "Uber Eats", "Grubhub", "Deliveroo", "Just Eat Takeaway",
            
            # Direct-to-Consumer Brands
            "Warby Parker", "Casper", "Allbirds", "Away", "Glossier", "Dollar Shave Club",
            "Harry's", "Bombas", "Outdoor Voices", "Everlane", "Reformation",
            "ThirdLove", "Fenty Beauty", "Kylie Cosmetics", "Honest Company",
            
            # Marketplace & Platforms
            "Etsy", "eBay", "Poshmark", "Depop", "Vinted", "TheRealReal",
            "Vestiaire Collective", "StockX", "GOAT", "Grailed", "Rebag",
            "1stDibs", "Chairish", "Reverb", "Discogs", "Catawiki",
            
            # Retail Technology
            "Toast", "Square", "Lightspeed", "Clover", "Revel Systems",
            "Vend", "Shopkeep", "Erply", "Cin7", "TradeGecko", "Brightpearl"
        ],
        
        "Transportation_Mobility": [
            # Ride Sharing & Mobility Services  
            "Uber", "Lyft", "Didi Chuxing", "Grab", "Gojek", "Ola", "99", "Cabify",
            "Free2move", "Share Now", "Zipcar", "Turo", "Getaround", "HyreCar",
            
            # Electric Vehicles & Charging
            "Tesla", "BYD", "NIO", "XPeng", "Li Auto", "Lucid Motors", "Rivian",
            "ChargePoint", "EVgo", "Blink Charging", "Wallbox", "SemaConnect",
            
            # Autonomous Vehicles
            "Waymo", "Cruise", "Argo AI", "Aurora", "Motional", "Zoox", "Nuro",
            "TuSimple", "Plus", "Embark", "Kodiak Robotics", "Gatik",
            
            # Logistics & Delivery
            "FedEx", "UPS", "DHL", "Amazon Logistics", "Shopify Fulfillment",
            "ShipBob", "Flexport", "Freightos", "project44", "FourKites",
            "Convoy", "Uber Freight", "Transfix", "Loadsmart", "KeepTruckin"
        ],
        
        "Real_Estate_PropTech": [
            # Residential Real Estate
            "Zillow", "Redfin", "Compass", "Realogy", "RE/MAX", "Coldwell Banker",
            "Century 21", "Keller Williams", "Sotheby's International", "Douglas Elliman",
            
            # PropTech & Real Estate Tech
            "Opendoor", "Offerpad", "RedfinNow", "Zillow Instant Offers", "iBuyer",
            "Flyhomes", "Ribbon", "Homeward", "Divvy Homes", "Landed",
            "VTS", "Hightower", "Reonomy", "CompStak", "Cherre", "Skyline AI",
            
            # REITs & Real Estate Investment
            "Blackstone Real Estate", "Brookfield Asset Management", "Prologis",
            "Simon Property Group", "Realty Income", "Digital Realty Trust",
            "American Tower", "Crown Castle", "SBA Communications", "Equinix",
            
            # Construction Tech
            "Procore", "Autodesk Construction Cloud", "PlanGrid", "Buildertrend",
            "CoConstruct", "BuilderTREND", "Sage Construction", "Oracle Aconex"
        ],
        
        "Energy_CleanTech": [
            # Solar & Renewable Energy
            "First Solar", "SunPower", "Enphase Energy", "SolarEdge", "Sunrun",
            "Tesla Energy", "Vivint Solar", "Sunnova", "Canadian Solar", "JinkoSolar",
            "Trina Solar", "JA Solar", "LONGi Solar", "Hanwha Q Cells",
            
            # Energy Storage & Grid
            "Tesla Energy Storage", "Fluence", "QuantumScape", "Solid Power",
            "Sila Nanotechnologies", "StoreDot", "Form Energy", "ESS Inc",
            
            # Electric Vehicle Infrastructure
            "ChargePoint", "EVgo", "Electrify America", "Shell Recharge", "BP Pulse",
            "Ionity", "Fastned", "Allego", "Pod Point", "NewMotion",
            
            # Clean Technology & ESG
            "Beyond Meat", "Impossible Foods", "Oatly", "Perfect Day", "Memphis Meats",
            "Apeel Sciences", "Indigo Agriculture", "Ginkgo Bioworks", "Modern Meadow",
            "Bolt Threads", "Spiber", "Biofabrica", "Ecovative", "MycoWorks"
        ],
        
        "Industrial_Manufacturing": [
            # Industry 4.0 & Smart Manufacturing
            "Siemens Digital Industries", "GE Digital", "Schneider Electric", "ABB",
            "Rockwell Automation", "Emerson", "Honeywell Process Solutions",
            "Aveva", "PTC ThingWorx", "Dassault Systemes", "Autodesk Fusion",
            
            # Robotics & Automation
            "Boston Dynamics", "Universal Robots", "Collaborative Robotics", "Rethink Robotics",
            "Soft Robotics", "RightHand Robotics", "Osaro", "Vicarious", "Covariant",
            
            # 3D Printing & Additive Manufacturing
            "Stratasys", "3D Systems", "HP 3D Printing", "EOS", "SLM Solutions",
            "Renishaw", "ExOne", "Velo3D", "Desktop Metal", "Markforged",
            
            # Supply Chain & Logistics Tech
            "Oracle Supply Chain", "SAP Ariba", "Coupa", "Jaggaer", "GEP SMART",
            "Tradeshift", "Basware", "Ivalua", "Zycus", "BirchStreet Systems"
        ],
        
        "Emerging_Technologies": [
            # Artificial Intelligence & ML
            "OpenAI", "Anthropic", "DeepMind", "Hugging Face", "Stability AI",
            "Midjourney", "Runway ML", "Scale AI", "Labelbox", "Snorkel AI",
            "DataRobot", "H2O.ai", "Databricks", "Weights & Biases", "Wandb",
            
            # Quantum Computing
            "IBM Quantum", "Google Quantum AI", "IonQ", "Rigetti Computing",
            "PsiQuantum", "Xanadu", "Cambridge Quantum Computing", "Zapata Computing",
            
            # AR/VR & Metaverse
            "Meta Reality Labs", "Microsoft HoloLens", "Magic Leap", "Niantic",
            "Unity XR", "Epic Games Metaverse", "Roblox", "VRChat", "Horizon Worlds",
            "Oculus", "HTC Vive", "Pico Interactive", "Varjo", "Nreal",
            
            # Web3 & Decentralized Tech
            "Ethereum Foundation", "Solana Labs", "Polygon", "Avalanche", "Chainlink",
            "Uniswap", "Aave", "Compound", "MakerDAO", "OpenSea", "LooksRare",
            "Foundation", "SuperRare", "Async Art", "KnownOrigin", "Nifty Gateway"
        ]
    }

def check_goldman_industry_gaps():
    """Check for Goldman Sachs research universe gaps"""
    existing, existing_names = get_existing_companies()
    gs_companies = get_goldman_sachs_research_universe()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Checking Goldman Sachs research universe for gaps...")
    print(f"=" * 70)
    
    all_missing = {}
    total_missing_companies = []
    
    for industry, companies in gs_companies.items():
        missing_in_industry = []
        found_in_industry = []
        
        for company in companies:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_industry.append(company)
                found = True
            else:
                # Check in original names with Goldman-specific matching
                for exist_name in existing_names:
                    # Split company name into key terms
                    company_terms = [word for word in company_lower.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'llc', 'ltd', 'co', 'corp', 'company', 'group', 'holdings', 'labs', 'systems', 'technologies']]
                    
                    if company_terms:
                        main_term = company_terms[0]
                        # More flexible matching for GS analysis
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms
                            if main_term not in ['app', 'web', 'data', 'cloud', 'smart', 'digital', 'global', 'international', 'american', 'china', 'new', 'first', 'solutions', 'services']:
                                found_in_industry.append(f"{company} (found as: {exist_name})")
                                found = True
                                break
                    
                    # Also check full substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        if len(company_lower) >= 4:
                            found_in_industry.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 4 and len(exist) > 4:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.75:  # High confidence matching
                                    found_in_industry.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_industry.append(company)
                total_missing_companies.append((company, industry))
        
        all_missing[industry] = {
            'missing': missing_in_industry,
            'found': found_in_industry,
            'coverage': len(found_in_industry) / len(companies) * 100 if companies else 0
        }
        
        print(f"\n=== {industry.upper().replace('_', ' ')} ===")
        print(f"Total: {len(companies)} | Found: {len(found_in_industry)} ({all_missing[industry]['coverage']:.1f}%) | Missing: {len(missing_in_industry)}")
        
        if missing_in_industry:
            print("🚨 MISSING:", ', '.join(missing_in_industry[:12]) + ("..." if len(missing_in_industry) > 12 else ""))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n📈 GOLDMAN SACHS RESEARCH UNIVERSE ANALYSIS")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Prioritize by Goldman Sachs coverage importance
    industry_priority = {
        'Software_Internet': 10,           # Core Goldman coverage
        'Financial_Technology': 10,        # Major GS focus area
        'Healthcare_Life_Sciences': 9,     # High-growth sector
        'Media_Entertainment_Gaming': 9,   # Digital transformation
        'Consumer_Retail_Ecommerce': 8,   # Consumer discretionary
        'Transportation_Mobility': 8,      # Mobility revolution
        'Emerging_Technologies': 8,        # Future technologies
        'Real_Estate_PropTech': 7,        # Real estate innovation
        'Energy_CleanTech': 7,            # ESG & clean energy
        'Industrial_Manufacturing': 6      # Traditional industrials
    }
    
    priority_missing = []
    for company, industry in total_missing_companies:
        priority_score = industry_priority.get(industry, 5)
        priority_missing.append((company, industry, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 100 MISSING BY GOLDMAN RESEARCH PRIORITY:")
    for i, (company, industry, score) in enumerate(priority_missing[:100], 1):
        print(f"{i:3d}. {company} ({industry.replace('_', ' ')})")
    
    # Show industry gaps summary
    print(f"\n📊 INDUSTRY GAPS RANKED BY MISSING COUNT:")
    industry_gaps = [(industry, len(data['missing']), data['coverage']) 
                     for industry, data in all_missing.items() if data['missing']]
    industry_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for industry, missing_count, coverage in industry_gaps:
        print(f"📉 {industry.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Save comprehensive Goldman analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_goldman_research_universe.txt', 'w') as f:
        f.write("GOLDMAN SACHS RESEARCH UNIVERSE - MISSING COMPANIES\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_checked}\n")
        f.write(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%\n\n")
        
        for industry, data in all_missing.items():
            if data['missing']:
                f.write(f"### {industry.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for company in data['missing']:
                    f.write(f"  - {company}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (company, industry, score) in enumerate(priority_missing[:200], 1):
            f.write(f"{i:3d}. {company} ({industry.replace('_', ' ')})\n")
    
    print(f"\nSaved Goldman research universe analysis to missing_goldman_research_universe.txt")
    print(f"📈 These are the gaps in Goldman Sachs research coverage universe!")
    
    return priority_missing[:200]  # Return top 200

if __name__ == "__main__":
    check_goldman_industry_gaps()