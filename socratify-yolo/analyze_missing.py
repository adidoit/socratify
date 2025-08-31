#!/usr/bin/env python3
import os
import json

def analyze_missing():
    print("="*80)
    print("ANALYZING WHAT'S STILL MISSING")
    print("="*80)
    
    # Categories of companies we should have
    critical_missing = {
        "AI/ML Companies": [
            "OpenAI", "Anthropic", "Perplexity", "Inflection AI", "Adept AI",
            "Runway ML", "Stability AI", "Jasper AI", "Copy.ai", "Glean",
            "Databricks", "Weights & Biases", "Anyscale", "Pinecone", "Weaviate"
        ],
        "Major Unicorns ($10B+)": [
            "SpaceX", "Stripe", "Canva", "Shein", "Bytedance", "Instacart",
            "Databricks", "Revolut", "Nubank", "Klarna", "Epic Games",
            "Fanatics", "Chime", "Grammarly", "Discord"
        ],
        "Crypto/Web3": [
            "Coinbase", "Binance", "Kraken", "Crypto.com", "OpenSea",
            "Uniswap", "Chainlink", "Polygon", "Solana", "Avalanche",
            "FTX (defunct)", "Gemini", "BlockFi", "Celsius", "Nexo"
        ],
        "Recent IPOs 2023-2024": [
            "Arm Holdings", "Instacart", "Klaviyo", "Birkenstock", "VinFast",
            "Cava Group", "Oddity Tech", "Maplebear", "Kenvue", "Savers Value Village",
            "Reddit", "Astera Labs", "Rubrik", "Ibotta", "Viking Holdings"
        ],
        "Defense/Space": [
            "SpaceX", "Blue Origin", "Anduril", "Shield AI", "Relativity Space",
            "Rocket Lab", "Planet Labs", "Astra", "Virgin Galactic", "Firefly Aerospace",
            "Palantir", "Raytheon", "General Dynamics", "Northrop Grumman", "L3Harris"
        ],
        "Healthcare/Biotech": [
            "Moderna", "BioNTech", "Regeneron", "Vertex", "Illumina",
            "23andMe", "Tempus", "Flatiron Health", "Oscar Health", "Ro",
            "Hims & Hers", "Carbon Health", "Forward", "One Medical", "Oak Street Health"
        ],
        "Electric Vehicles/Clean Energy": [
            "Rivian", "Lucid Motors", "Polestar", "NIO", "XPeng", "Li Auto",
            "ChargePoint", "EVgo", "Blink Charging", "Proterra", "Arrival",
            "Canoo", "Fisker", "Lordstown Motors", "Nikola"
        ],
        "Gaming/Entertainment": [
            "Roblox", "Unity", "Unreal Engine", "Steam", "Discord",
            "Twitch", "Kick", "Rumble", "DraftKings", "FanDuel",
            "Activision Blizzard", "Electronic Arts", "Take-Two", "Ubisoft", "Square Enix"
        ],
        "Food Delivery/Quick Commerce": [
            "DoorDash", "Uber Eats", "Grubhub", "Postmates", "Gopuff",
            "Getir", "Gorillas", "Deliveroo", "Just Eat", "Swiggy",
            "Zomato", "Meituan", "Rappi", "iFood", "Glovo"
        ],
        "Social Media/Creator Economy": [
            "BeReal", "Clubhouse", "Truth Social", "Parler", "Gab",
            "OnlyFans", "Patreon", "Substack", "Medium", "Ghost",
            "ConvertKit", "Mailchimp", "Constant Contact", "Kajabi", "Teachable"
        ],
        "Enterprise SaaS": [
            "Snowflake", "Databricks", "Confluent", "HashiCorp", "GitLab",
            "JFrog", "Elastic", "Splunk", "Datadog", "New Relic",
            "PagerDuty", "Okta", "Auth0", "Twilio", "SendGrid"
        ],
        "Regional Tech Giants": [
            "Grab (Southeast Asia)", "Gojek (Indonesia)", "Sea Limited (Singapore)",
            "Mercado Libre (Latin America)", "Rappi (Latin America)", "Nubank (Brazil)",
            "Flipkart (India)", "Ola (India)", "Paytm (India)", "Razorpay (India)",
            "Kakao (South Korea)", "Naver (South Korea)", "LINE (Japan)", "Rakuten (Japan)"
        ]
    }
    
    # Check existing logos
    logos_path = '../socratify-images/logos/images/companies/'
    existing_logos = set()
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            # Normalize the name
            logo_name = filename[:-4].lower().replace('_', ' ').replace('-', ' ')
            existing_logos.add(logo_name)
    
    print(f"\nCurrent logo count: {len(existing_logos)}\n")
    
    # Check each category
    missing_by_category = {}
    total_missing = 0
    
    for category, companies in critical_missing.items():
        missing = []
        for company in companies:
            company_normalized = company.lower().replace('.', '').replace('-', ' ')
            found = False
            
            # Check various matching strategies
            for logo in existing_logos:
                if company_normalized in logo or logo in company_normalized:
                    found = True
                    break
                # Check first word match
                if company_normalized.split()[0] == logo.split()[0]:
                    found = True
                    break
            
            if not found:
                missing.append(company)
        
        if missing:
            missing_by_category[category] = missing
            total_missing += len(missing)
            print(f"❌ {category}: Missing {len(missing)}/{len(companies)}")
            for comp in missing[:5]:  # Show first 5
                print(f"   - {comp}")
            if len(missing) > 5:
                print(f"   ... and {len(missing)-5} more")
            print()
    
    print("="*80)
    print(f"TOTAL POTENTIALLY MISSING: ~{total_missing} important companies")
    print("="*80)
    
    # Save detailed list
    with open('critical_missing_companies.json', 'w') as f:
        json.dump(missing_by_category, f, indent=2)
    
    print("\nDetailed list saved to: critical_missing_companies.json")
    
    return missing_by_category

if __name__ == "__main__":
    analyze_missing()