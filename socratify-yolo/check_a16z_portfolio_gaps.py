#!/usr/bin/env python3
"""
Check Andreessen Horowitz (a16z) portfolio style analysis for missing companies
Deep dive into a16z investment thesis and portfolio coverage
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

def get_a16z_investment_universe():
    """Andreessen Horowitz investment thesis and portfolio universe - sector by sector"""
    return {
        "AI_ML_Foundation_Models": [
            # Foundation Models & Infrastructure
            "OpenAI", "Anthropic", "Cohere", "AI21 Labs", "Hugging Face", "Stability AI",
            "Midjourney", "Runway ML", "Jasper", "Copy.ai", "Writesonic", "Lex",
            "Character.AI", "Replika", "Inflection AI", "Adept", "You.com",
            
            # AI Infrastructure & MLOps
            "Weights & Biases", "Neptune.ai", "ClearML", "MLflow", "Kubeflow",
            "Feast", "Tecton", "Hopsworks", "Seldon", "BentoML", "Cortex Labs",
            "Run:ai", "Determined AI", "Grid.ai", "Domino Data Lab", "Dataiku",
            
            # Computer Vision & Robotics AI
            "Scale AI", "Labelbox", "Supervisely", "Roboflow", "Segments.ai",
            "Humanloop", "Snorkel AI", "Aquarium Learning", "Ango AI", "Toloka",
            "Boston Dynamics", "Agility Robotics", "1X Technologies", "Figure AI"
        ],
        
        "Crypto_Web3_DeFi": [
            # Layer 1 Blockchains & Protocols
            "Ethereum", "Solana", "Avalanche", "Polygon", "Near Protocol", "Aptos",
            "Sui", "Flow", "Algorand", "Cosmos", "Polkadot", "Chainlink",
            "The Graph", "Livepeer", "Helium", "Arweave", "Filecoin", "IPFS",
            
            # DeFi Protocols & DEXs
            "Uniswap", "Aave", "Compound", "MakerDAO", "Curve Finance", "Balancer",
            "1inch", "0x Protocol", "SushiSwap", "PancakeSwap", "Trader Joe",
            "dYdX", "GMX", "Perpetual Protocol", "Synthetix", "Yearn Finance",
            
            # NFTs & Digital Collectibles
            "OpenSea", "Blur", "LooksRare", "Foundation", "SuperRare", "AsyncArt",
            "KnownOrigin", "MakersPlace", "Nifty Gateway", "NBA Top Shot", "Dapper Labs",
            "Immutable X", "Magic Eden", "Tensor", "Hic et Nunc", "FxHash",
            
            # Crypto Infrastructure & Tools
            "Coinbase", "FTX", "Binance", "Kraken", "Gemini", "Circle", "Tether",
            "Chainalysis", "Elliptic", "TaxBit", "CoinTracker", "Blockdaemon",
            "Alchemy", "Infura", "QuickNode", "Moralis", "Thirdweb", "WalletConnect"
        ],
        
        "Consumer_Social_Creator": [
            # Social Media & Communities
            "Discord", "Clubhouse", "Geneva", "Luma", "Partiful", "IRL",
            "BeReal", "Poparazzi", "Dispo", "VSCO", "Retro", "Locket",
            "Gas", "NGL", "Sendit", "Summer", "Peanut", "Wizz",
            
            # Creator Economy & Tools
            "Substack", "ConvertKit", "Ghost", "Beehiiv", "Revue", "Buttondown",
            "Patreon", "OnlyFans", "Cameo", "Memmo", "Starsona", "Tealfeed",
            "Creator.co", "Koji", "Linktree", "Bio.fm", "Milkshake", "Carrd",
            
            # Gaming & Entertainment
            "Roblox", "Discord", "Twitch", "YouTube Gaming", "Kick", "Trovo",
            "Guilded", "Steam", "Epic Games", "Unity", "Core", "Rec Room",
            "VRChat", "Horizon Worlds", "AltspaceVR", "Mozilla Hubs",
            
            # Audio & Podcasting
            "Clubhouse", "Twitter Spaces", "Spotify Greenroom", "Discord Stage",
            "Anchor", "Spotify for Podcasters", "Riverside.fm", "SquadCast",
            "Zencastr", "Hindenburg", "Descript", "Otter.ai", "Sonix", "Rev"
        ],
        
        "Developer_Tools_Infrastructure": [
            # Cloud & Infrastructure
            "Fly.io", "Railway", "Render", "Supabase", "PlanetScale", "Neon",
            "Xata", "Convex", "EdgeDB", "FaunaDB", "CockroachDB", "TiDB",
            "Hasura", "Prisma", "Drizzle", "PostgREST", "Postgraphile",
            
            # Developer Platforms & APIs
            "Vercel", "Netlify", "Cloudflare Pages", "GitHub Pages", "GitLab Pages",
            "Heroku", "AWS Amplify", "Firebase", "Appwrite", "Back4App",
            "Parse Server", "Strapi", "Directus", "Sanity", "Contentful",
            
            # DevOps & Monitoring
            "Datadog", "New Relic", "Sentry", "LogRocket", "FullStory", "Hotjar",
            "PostHog", "Mixpanel", "Amplitude", "Segment", "Rudderstack",
            "Snowplow", "mParticle", "Tealium", "Adobe Analytics", "Google Analytics",
            
            # Security & Compliance
            "Snyk", "Veracode", "Checkmarx", "SonarQube", "GitGuardian", "Semgrep",
            "Bridgecrew", "Prisma Cloud", "Aqua Security", "Twistlock", "StackRox",
            "Falco", "Sysdig", "Lacework", "Orca Security", "Wiz"
        ],
        
        "Fintech_B2B_Payments": [
            # B2B Payments & Banking
            "Stripe", "Adyen", "Checkout.com", "GoCardless", "Razorpay", "PayU",
            "Paymi", "dLocal", "Flutterwave", "Paystack", "Chipper Cash", "Wave",
            "Mercury", "Brex", "Ramp", "Divvy", "Expensify", "Concur", "TripActions",
            
            # Embedded Finance & Banking-as-a-Service
            "Unit", "Synctera", "Treasury Prime", "Bond", "Column", "Moov",
            "Modern Treasury", "Increase", "Method", "Plaid", "Yodlee", "Tink",
            "Open Banking", "TrueLayer", "Belvo", "Fintoc", "Pluggy",
            
            # Lending & Credit
            "Affirm", "Klarna", "Afterpay", "Sezzle", "Zip", "Tabby", "Tamara",
            "Upstart", "LendingClub", "Prosper", "SoFi", "CommonBond", "Earnest",
            "Credible", "LendingTree", "Rocket Mortgage", "Better.com", "Homebot",
            
            # Crypto Finance & DeFi
            "Circle", "Centre", "Paxos", "Gemini Dollar", "TrueUSD", "Dai",
            "USDC", "BUSD", "FRAX", "Liquity", "Reflexer", "RAI", "FEI",
            "OlympusDAO", "Tokemak", "Convex Finance", "Frax Finance"
        ],
        
        "Healthcare_Biotech_Digital": [
            # Digital Health & Telemedicine
            "Ro", "Hims", "Nurx", "Pill Club", "SimpleHealth", "Wisp",
            "Maven", "Kindbody", "Celmatix", "Carrot Fertility", "Progyny",
            "Spring Fertility", "Extend Fertility", "CCRM Fertility",
            
            # Mental Health & Therapy
            "Headspace", "Calm", "BetterHelp", "Talkspace", "Cerebral", "Mindstrong",
            "Ginger", "Lyra Health", "Modern Health", "Spring Health", "Sanvello",
            "Daylio", "Moodpath", "Youper", "Woebot", "X2AI", "Ellipsis Health",
            
            # Biotech & Drug Discovery
            "Ginkgo Bioworks", "Zymergen", "Twist Bioscience", "Synthetic Genomics",
            "Modern Meadow", "Perfect Day", "Clara Foods", "Memphis Meats", "JUST",
            "Impossible Foods", "Beyond Meat", "NotCo", "v2food", "Redefine Meat",
            
            # Healthcare Infrastructure & Data
            "Veracyte", "10x Genomics", "Oxford Nanopore", "Pacific Biosciences",
            "Illumina", "Guardant Health", "Foundation Medicine", "Tempus",
            "Flatiron Health", "Ciox Health", "Health Gorilla", "Redox", "1up Health"
        ],
        
        "Marketplace_Commerce_B2B": [
            # Vertical B2B Marketplaces
            "Faire", "Ankorstore", "Orderchamp", "Creoate", "Bundled", "Handshake",
            "NuOrder", "Joor", "LeadGenius", "ZoomInfo", "Apollo", "Outreach",
            "Salesloft", "HubSpot", "Pipedrive", "Copper", "Close", "Freshsales",
            
            # Supply Chain & Procurement
            "Flexport", "Freightos", "Convoy", "Uber Freight", "Transfix", "Loadsmart",
            "project44", "FourKites", "Shippeo", "Route4Me", "OptimoRoute", "Onfleet",
            "Bringg", "Shippo", "EasyShip", "AfterShip", "TrackingMore", "ParcelLab",
            
            # Manufacturing & Industrial
            "Formlabs", "Carbon", "Desktop Metal", "Markforged", "HP Multi Jet",
            "Stratasys", "3D Systems", "Materialise", "Proto Labs", "Xometry",
            "Hubs", "Craftcloud", "Treatstock", "3D Hubs", "Sculpteo", "Shapeways",
            
            # Construction & Real Estate B2B
            "Procore", "Buildertrend", "CoConstruct", "BuilderTREND", "Jonas Construction",
            "Sage Construction", "Viewpoint", "HCSS", "B2W Software", "InEight",
            "Oracle Primavera", "Microsoft Project", "Smartsheet", "Monday.com"
        ],
        
        "Future_Computing_Hardware": [
            # AR/VR & Spatial Computing
            "Magic Leap", "Microsoft HoloLens", "Apple Vision Pro", "Meta Quest",
            "Pico Interactive", "HTC Vive", "Valve Index", "Varjo", "Nreal",
            "Vuzix", "Epson Moverio", "RealWear", "ThirdEye Gen", "Mad Gaze",
            
            # Quantum Computing
            "IonQ", "Rigetti Computing", "PsiQuantum", "Xanadu", "Cambridge Quantum",
            "Zapata Computing", "ProteinQure", "Menten AI", "QC Ware", "Rahko",
            "Cambridge Quantum Computing", "Quantum Machines", "QM Technologies",
            
            # Edge Computing & IoT
            "Particle", "Helium", "Samsara", "Augury", "Uptake", "C3.ai", "Palantir",
            "DataRobot", "H2O.ai", "Dataiku", "Alteryx", "Tableau", "Looker",
            "Sisense", "ThoughtSpot", "Qlik", "Microsoft Power BI", "Domo",
            
            # Semiconductors & Hardware
            "Cerebras Systems", "Graphcore", "SambaNova Systems", "Groq", "Mythic",
            "BrainChip", "GreenWaves Technologies", "Hailo", "Kneron", "Blaize",
            "Syntiant", "Edge Impulse", "OctoML", "Neural Magic", "Deci AI"
        ],
        
        "Climate_ESG_Impact": [
            # Carbon & Climate Tech
            "Climeworks", "Carbon Engineering", "Global Thermostat", "Heirloom",
            "Charm Industrial", "Running Tide", "Project Vesta", "Ebb Carbon",
            "CarbonCure", "Solidia", "Carbon Clean", "Carbon Collect", "Noya",
            
            # Circular Economy & Waste
            "Recycle Track Systems", "Rubicon", "Waste Management", "Republic Services",
            "Samsara", "Routeware", "AMCS", "Enevo", "Compology", "Bigbelly",
            "TerraCycle", "Loop Industries", "Closed Loop Partners", "Ellen MacArthur",
            
            # Sustainable Agriculture & Food
            "Indigo Agriculture", "Gro Intelligence", "Climate Corporation", "Farmers Edge",
            "Taranis", "aWhere", "Cropin", "FarmLogs", "Granular", "AgriWebb",
            "Perfect Day", "Impossible Foods", "Beyond Meat", "Memphis Meats",
            "JUST", "Clara Foods", "Geltor", "Modern Meadow", "Bolt Threads",
            
            # Energy Storage & Grid
            "Form Energy", "ESS Inc", "Ambri", "Malta", "Antora Energy", "Quidnet",
            "Advanced Ionics", "Electric Hydrogen", "Ohmium", "Nel Hydrogen",
            "ITM Power", "Plug Power", "Ballard Power", "FuelCell Energy"
        ]
    }

def check_a16z_gaps():
    """Check for a16z investment thesis gaps"""
    existing, existing_names = get_existing_companies()
    a16z_companies = get_a16z_investment_universe()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Checking a16z investment thesis universe for gaps...")
    print(f"=" * 70)
    
    all_missing = {}
    total_missing_companies = []
    
    for sector, companies in a16z_companies.items():
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
                # Check in original names with a16z-specific matching
                for exist_name in existing_names:
                    # Split company name into key terms
                    company_terms = [word for word in company_lower.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'llc', 'ltd', 'co', 'corp', 'company', 'group', 'holdings', 'labs', 'systems', 'technologies', 'protocol']]
                    
                    if company_terms:
                        main_term = company_terms[0]
                        # More flexible matching for a16z analysis
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms but allow crypto/web3 terms
                            if main_term not in ['app', 'web', 'data', 'cloud', 'smart', 'digital', 'global', 'international', 'american', 'new', 'first', 'solutions', 'services']:
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
            print("🚨 MISSING:", ', '.join(missing_in_sector[:12]) + ("..." if len(missing_in_sector) > 12 else ""))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🚀 ANDREESSEN HOROWITZ INVESTMENT UNIVERSE ANALYSIS")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Prioritize by a16z investment focus areas
    sector_priority = {
        'AI_ML_Foundation_Models': 10,      # Core a16z thesis
        'Crypto_Web3_DeFi': 10,            # Major a16z focus
        'Consumer_Social_Creator': 9,       # Traditional a16z strength
        'Developer_Tools_Infrastructure': 9, # Dev-first approach
        'Fintech_B2B_Payments': 8,        # Growth area
        'Healthcare_Biotech_Digital': 8,    # Bio fund focus
        'Marketplace_Commerce_B2B': 7,      # B2B focus
        'Future_Computing_Hardware': 7,     # Future tech
        'Climate_ESG_Impact': 6             # Newer focus area
    }
    
    priority_missing = []
    for company, sector in total_missing_companies:
        priority_score = sector_priority.get(sector, 5)
        priority_missing.append((company, sector, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 150 MISSING BY A16Z INVESTMENT PRIORITY:")
    for i, (company, sector, score) in enumerate(priority_missing[:150], 1):
        print(f"{i:3d}. {company} ({sector.replace('_', ' ')})")
    
    # Show sector gaps summary
    print(f"\n📊 SECTOR GAPS RANKED BY MISSING COUNT:")
    sector_gaps = [(sector, len(data['missing']), data['coverage']) 
                   for sector, data in all_missing.items() if data['missing']]
    sector_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for sector, missing_count, coverage in sector_gaps:
        print(f"📉 {sector.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Save comprehensive a16z analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_a16z_investment_universe.txt', 'w') as f:
        f.write("ANDREESSEN HOROWITZ INVESTMENT UNIVERSE - MISSING COMPANIES\n")
        f.write("=" * 65 + "\n\n")
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
        for i, (company, sector, score) in enumerate(priority_missing[:200], 1):
            f.write(f"{i:3d}. {company} ({sector.replace('_', ' ')})\n")
    
    print(f"\nSaved a16z investment universe analysis to missing_a16z_investment_universe.txt")
    print(f"🚀 These are the gaps in a16z-style investment universe coverage!")
    
    return priority_missing[:200]  # Return top 200

if __name__ == "__main__":
    check_a16z_gaps()