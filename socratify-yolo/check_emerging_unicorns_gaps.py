#!/usr/bin/env python3
"""
Check for emerging unicorns, hot startups, and cutting-edge companies we might have missed
Focus on 2023-2025 breakout companies, stealth mode companies, and international hot startups
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

def get_emerging_hot_companies():
    """Emerging unicorns, hot startups, and cutting-edge companies (2023-2025 breakouts)"""
    return {
        "2024_2025_AI_Breakouts": [
            # Latest AI Unicorns & Hot Startups
            "Perplexity AI", "Harvey AI", "Glean", "Sierra", "Cognition AI", "Devin AI",
            "Magic AI", "Codeium", "Cursor", "Replit", "Vercel v0", "Bolt", "Lovable",
            "Phind", "You.com", "Perplexity", "Claude AI", "Poe", "Character.AI", "Replika",
            
            # AI Agents & Automation
            "LangChain", "LlamaIndex", "Semantic Kernel", "AutoGPT", "BabyAGI", "AgentGPT",
            "Superagent", "Fixie", "Multi-On", "Adept AI", "Imbue", "Thesis",
            
            # AI Video & Creative Tools  
            "RunwayML", "Pika Labs", "Gen-2", "Stable Video", "Kaiber", "D-ID",
            "Synthesia", "Hour One", "Colossyan", "Elai.io", "Pictory", "InVideo",
            "Luma AI", "LeiaPix", "Immersity AI", "Neural Love", "Topaz Labs",
            
            # AI Code & Development
            "GitHub Copilot X", "Tabnine", "Amazon CodeWhisperer", "Sourcegraph Cody",
            "Pieces", "Mintlify", "Sweep AI", "CodeT5", "StarCoder", "WizardCoder"
        ],
        
        "International_Breakouts_2024": [
            # European Hot Startups
            "Mistral AI", "Hugging Face", "DeepL", "UiPath", "Celonis", "GetYourGuide",
            "Personio", "SumUp", "Trade Republic", "N26", "Revolut", "Monzo", "Starling Bank",
            "Curve", "Klarna", "Afterpay", "GoCardless", "Adyen", "Mollie", "Checkout.com",
            
            # UK Unicorns & Scale-ups
            "Deliveroo", "Just Eat", "Cazoo", "Octopus Energy", "Bulb", "Monzo", 
            "Revolut", "Wise", "Zopa", "MarketFinance", "iwoca", "Funding Circle",
            "Darktrace", "Improbable", "DeepMind", "Graphcore", "Onfido", "Benevolent AI",
            
            # German/DACH Unicorns
            "SAP Concur", "TeamViewer", "Wirecard", "Auto1", "FlixBus", "HelloFresh",
            "Zalando", "Rocket Internet", "SoundCloud", "ResearchGate", "Adjust",
            
            # French Tech Champions
            "BlaBlaCar", "Criteo", "Deezer", "Dailymotion", "OVHcloud", "Doctolib",
            "Alan", "Qonto", "Ledger", "Sorare", "Shift Technology", "Dataiku",
            
            # Nordic Unicorns
            "Spotify", "Klarna", "King", "Mojang", "Supercell", "Rovio", "Unity",
            "Epidemic Sound", "Sinch", "Truecaller", "Voi Technology", "Oda"
        ],
        
        "Asian_Tech_Giants_2024": [
            # Indian Unicorns (latest wave)
            "BYJU'S", "Paytm", "Zomato", "Swiggy", "Flipkart", "PhonePe", "Razorpay",
            "Freshworks", "Chargebee", "Postman", "InMobi", "Ola", "Oyo", "Udaan",
            "Unacademy", "Vedantu", "WhiteHat Jr", "Eruditus", "upGrad", "Simplilearn",
            
            # Southeast Asian Unicorns
            "Grab", "Gojek", "Sea Limited", "Shopee", "Garena", "Tokopedia", "Bukalapak",
            "Traveloka", "RedDoorz", "PropertyGuru", "Carousell", "Ninja Van",
            
            # Chinese New Economy (post-2020)
            "ByteDance Global", "TikTok Shop", "CapCut", "Lemon8", "Resso", "Helo",
            "Perfect Diary", "Genki Forest", "Luckin Coffee", "XPeng Motors", "Li Auto",
            "NIO", "BYD", "Xpeng", "Zeekr", "Human Horizons", "WM Motor",
            
            # Japanese Tech Scale-ups
            "Mercari", "SmartHR", "freee", "MoneyForward", "Sansan", "ChatWork",
            "Base", "JMDC", "Medley", "BrainPad", "PKSHA Technology", "Preferred Networks"
        ],
        
        "Vertical_SaaS_Champions": [
            # Construction Tech
            "Procore", "Autodesk Construction Cloud", "PlanGrid", "Buildertrend", "CoConstruct",
            "eSUB", "RedTeam", "ComputerEase", "STACK", "Sage Construction", "Trimble Connect",
            
            # Legal Tech
            "Relativity", "Exterro", "Onna", "Logikcull", "Everlaw", "Disco", "Lexis+",
            "Thomson Reuters", "Clio", "PracticePanther", "TimeSolv", "Bill4Time",
            
            # Real Estate Tech
            "Compass", "Zillow Premier Agent", "Redfin Direct", "Opendoor", "Offerpad",
            "Flyhomes", "Ribbon", "Homeward", "Better.com", "Rocket Mortgage", "Blend",
            
            # Restaurant Tech
            "Toast", "Resy", "OpenTable", "TouchBistro", "Lightspeed Restaurant", "Square for Restaurants",
            "ChowNow", "Grubhub for Restaurants", "DoorDash for Business", "Uber Eats Manager",
            
            # Fitness & Wellness Tech
            "ClassPass", "Mindbody", "Glofox", "Zen Planner", "TeamUp", "Vagaro", "Booker",
            "WellnessLiving", "Pike13", "Omnify", "FitSW", "TrueCoach", "MyFitnessPal Premium"
        ],
        
        "Creator_Economy_2024": [
            # Creator Platforms (latest)
            "Stan Store", "Gumroad", "Teachable", "Thinkific", "Kajabi", "Podia", "Circle",
            "Mighty Networks", "Skool", "Geneva", "Discord Nitro", "Patreon", "OnlyFans",
            
            # Content Creation Tools
            "Canva Pro", "Figma", "Framer", "Webflow", "Notion", "Obsidian", "Roam Research",
            "RemNote", "Craft", "Bear", "Ulysses", "iA Writer", "Scrivener", "Grammarly",
            
            # Video & Audio Creation
            "Riverside.fm", "Descript", "Loom", "Mmhmm", "Camtasia", "ScreenFlow", "OBS Studio",
            "Streamlabs", "Restream", "StreamYard", "Ecamm Live", "Wirecast", "XSplit",
            
            # Creator Monetization
            "ConvertKit", "Mailchimp", "Substack Pro", "Ghost Pro", "Medium Partner Program",
            "YouTube Premium Revenue", "Twitch Affiliate", "TikTok Creator Fund", "Instagram Reels Play"
        ],
        
        "Web3_Native_2024": [
            # Latest Layer 1s & L2s
            "Sui", "Aptos", "Sei", "Celestia", "Arbitrum", "Optimism", "Polygon zkEVM",
            "StarkNet", "Scroll", "Base", "Linea", "zkSync Era", "Mantle", "Blast",
            
            # DeFi 2.0 & Real Yield
            "GMX", "GLP", "Gains Network", "Radiant Capital", "Vela Exchange", "Vertex Protocol",
            "Drift Protocol", "Jupiter", "Orca", "Raydium", "Marinade", "Jito",
            
            # NFT & Gaming Platforms
            "Blur", "LooksRare", "X2Y2", "Gem", "Genie", "Reservoir", "Holograph",
            "Immutable X", "Polygon Studios", "Flow", "WAX", "Enjin", "Ultra",
            
            # Web3 Social & Creator
            "Farcaster", "Lens Protocol", "Cyberconnect", "XMTP", "Push Protocol", "Unlock Protocol",
            "Rally", "BitClout", "DeSo", "Minds", "Diaspora", "Mastodon"
        ],
        
        "Climate_Tech_2024": [
            # Carbon Removal & DAC
            "Climeworks", "Carbon Engineering", "Heirloom", "Sustaera", "Mission Zero",
            "Running Tide", "Project Vesta", "Ebb Carbon", "AspiraDAC", "Airhive",
            
            # Clean Energy Storage
            "Form Energy", "Sila Nanotechnologies", "QuantumScape", "Solid Power", "StoreDot",
            "Amprius", "SES", "Cuberg", "Enevate", "Sakti3", "Seeo", "Polyplus",
            
            # Sustainable Materials
            "Bolt Threads", "Modern Meadow", "Spiber", "Biofabricate", "MycoWorks", "Ecovative",
            "AlgiKnit", "Orange Fiber", "Piñatex", "MuSkin", "Vegea", "Desserto",
            
            # Precision Agriculture  
            "Indigo Agriculture", "Plenty", "AeroFarms", "Bowery Farming", "Gotham Greens",
            "AppHarvest", "Iron Ox", "Farmers Business Network", "Granular", "Climate Corporation"
        ]
    }

def check_emerging_gaps():
    """Check for emerging companies and hot startups we're missing"""
    existing, existing_names = get_existing_companies()
    emerging_companies = get_emerging_hot_companies()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Checking emerging unicorns & hot startups for gaps...")
    print(f"🔥 HUNTING FOR THE HOTTEST COMPANIES WE'VE MISSED! 🔥")
    print(f"=" * 75)
    
    all_missing = {}
    total_missing_companies = []
    
    for category, companies in emerging_companies.items():
        missing_in_category = []
        found_in_category = []
        
        for company in companies:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(company)
                found = True
            else:
                # Check in original names with emerging company matching
                for exist_name in existing_names:
                    # Split company name into key terms
                    company_terms = [word for word in company_lower.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'llc', 'ltd', 'co', 'corp', 'company', 'group', 'holdings', 'labs', 'systems', 'technologies', 'protocol', 'pro', 'premium']]
                    
                    if company_terms:
                        main_term = company_terms[0]
                        # Flexible matching for emerging companies
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms but allow tech terms
                            if main_term not in ['app', 'web', 'data', 'smart', 'digital', 'global', 'international', 'american', 'new', 'first', 'solutions', 'services', 'tech']:
                                found_in_category.append(f"{company} (found as: {exist_name})")
                                found = True
                                break
                    
                    # Also check full substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        if len(company_lower) >= 4:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 4 and len(exist) > 4:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.75:  # High confidence matching
                                    found_in_category.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(company)
                total_missing_companies.append((company, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(companies) * 100 if companies else 0
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(companies)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print("🚨 HOT MISSING:", ', '.join(missing_in_category[:12]) + ("..." if len(missing_in_category) > 12 else ""))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🔥 EMERGING UNICORNS & HOT STARTUPS ANALYSIS")
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Prioritize by hotness and growth potential
    category_priority = {
        '2024_2025_AI_Breakouts': 10,        # Hottest AI startups
        'International_Breakouts_2024': 9,   # Global unicorns
        'Asian_Tech_Giants_2024': 9,         # Asian tech leaders
        'Web3_Native_2024': 8,               # Web3 natives
        'Vertical_SaaS_Champions': 8,        # B2B SaaS leaders
        'Creator_Economy_2024': 7,           # Creator platforms
        'Climate_Tech_2024': 7               # Climate tech leaders
    }
    
    priority_missing = []
    for company, category in total_missing_companies:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((company, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 150 HOTTEST MISSING COMPANIES:")
    for i, (company, category, score) in enumerate(priority_missing[:150], 1):
        print(f"{i:3d}. {company} ({category.replace('_', ' ')})")
    
    # Show category gaps summary
    print(f"\n📊 HOTTEST GAPS RANKED BY MISSING COUNT:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps:
        print(f"🔥 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Save comprehensive emerging companies analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_emerging_unicorns.txt', 'w') as f:
        f.write("EMERGING UNICORNS & HOT STARTUPS - MISSING COMPANIES\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_checked}\n")
        f.write(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for company in data['missing']:
                    f.write(f"  - {company}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY HOTTEST MISSING ###\n")
        for i, (company, category, score) in enumerate(priority_missing[:200], 1):
            f.write(f"{i:3d}. {company} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved emerging companies analysis to missing_emerging_unicorns.txt")
    print(f"🔥 These are the HOTTEST companies we're missing!")
    print(f"🚀 Time to add the cutting-edge unicorns and breakout startups!")
    
    return priority_missing[:200]  # Return top 200

if __name__ == "__main__":
    check_emerging_gaps()