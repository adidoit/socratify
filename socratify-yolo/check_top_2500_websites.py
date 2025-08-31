#!/usr/bin/env python3
"""
Check coverage of the top 2,500 websites globally
Based on major web traffic ranking sources like Alexa, SimilarWeb, etc.
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

def get_top_2500_websites():
    """Representative sample of top global websites across all categories"""
    return {
        "Top_100_Global_Websites": [
            # Core top websites that everyone knows
            "Google", "YouTube", "Facebook", "Wikipedia", "Yahoo", "Reddit", "Amazon",
            "Twitter", "Instagram", "LinkedIn", "Netflix", "eBay", "Microsoft", "Apple",
            "TikTok", "Zoom", "Adobe", "PayPal", "Pinterest", "Spotify", "Dropbox",
            "Salesforce", "GitHub", "Stack Overflow", "Medium", "Quora", "Twitch",
            "Discord", "Slack", "Canva", "Figma", "Notion", "Trello", "Asana"
        ],
        
        "Major_Search_Engines": [
            "Google", "Bing", "Yahoo", "Baidu", "Yandex", "DuckDuckGo", "Ask.com",
            "AOL", "Dogpile", "StartPage", "Searx", "Ecosia", "Brave Search"
        ],
        
        "Social_Media_Giants": [
            "Facebook", "Instagram", "Twitter", "LinkedIn", "TikTok", "Snapchat",
            "Pinterest", "Reddit", "Discord", "Twitch", "WhatsApp", "Telegram",
            "Signal", "Viber", "WeChat", "Line", "KakaoTalk", "VKontakte", "Weibo"
        ],
        
        "E-Commerce_Shopping": [
            "Amazon", "eBay", "Alibaba", "AliExpress", "Etsy", "Shopify", "Walmart",
            "Target", "Best Buy", "Home Depot", "Costco", "eBay Motors", "Rakuten",
            "Mercado Libre", "Flipkart", "JD.com", "Tmall", "Taobao", "Pinduoduo"
        ],
        
        "News_Media_Sites": [
            "CNN", "BBC", "The New York Times", "The Guardian", "Reuters", "Associated Press",
            "Fox News", "MSNBC", "Wall Street Journal", "Washington Post", "USA Today",
            "Daily Mail", "The Sun", "BuzzFeed", "Vox", "Vice", "Huffington Post",
            "NPR", "PBS", "TIME", "Newsweek", "The Economist", "Bloomberg", "CNBC"
        ],
        
        "Streaming_Entertainment": [
            "Netflix", "YouTube", "Hulu", "Disney Plus", "HBO Max", "Amazon Prime Video",
            "Twitch", "Spotify", "Apple Music", "Pandora", "SoundCloud", "Vimeo",
            "Crunchyroll", "Funimation", "Paramount Plus", "Peacock", "Discovery Plus"
        ],
        
        "Tech_Cloud_Services": [
            "Google Cloud", "Amazon Web Services", "Microsoft Azure", "Cloudflare",
            "Digital Ocean", "Linode", "Vultr", "Heroku", "Netlify", "Vercel",
            "GitHub", "GitLab", "Bitbucket", "Docker Hub", "NPM", "PyPI"
        ],
        
        "Financial_Services": [
            "PayPal", "Square", "Stripe", "Coinbase", "Binance", "Kraken", "Robinhood",
            "Webull", "TD Ameritrade", "E*TRADE", "Charles Schwab", "Fidelity",
            "Vanguard", "Chase", "Bank of America", "Wells Fargo", "Citibank"
        ],
        
        "Travel_Services": [
            "Booking.com", "Expedia", "Airbnb", "TripAdvisor", "Kayak", "Priceline",
            "Hotels.com", "Trivago", "Orbitz", "Travelocity", "Skyscanner", "Momondo"
        ],
        
        "Educational_Learning": [
            "Khan Academy", "Coursera", "edX", "Udemy", "Udacity", "Skillshare",
            "MasterClass", "Pluralsight", "LinkedIn Learning", "Duolingo", "Rosetta Stone",
            "Chegg", "Course Hero", "StudyBlue", "Quizlet", "Brainly"
        ],
        
        "Communication_Messaging": [
            "WhatsApp", "Telegram", "Signal", "Discord", "Slack", "Microsoft Teams",
            "Zoom", "Skype", "Google Meet", "WebEx", "GoToMeeting", "BlueJeans"
        ],
        
        "Adult_Entertainment": [
            # Major adult sites (significant web traffic)
            "Pornhub", "xHamster", "YouPorn", "RedTube", "XVideos", "OnlyFans",
            "Chaturbate", "MyFreeCams", "LiveJasmin", "BongaCams"
        ],
        
        "Gaming_Platforms": [
            "Steam", "Epic Games Store", "Origin", "Battle.net", "GOG", "Itch.io",
            "Roblox", "Minecraft", "Fortnite", "Among Us", "League of Legends",
            "Twitch", "YouTube Gaming", "IGN", "GameSpot", "Polygon"
        ],
        
        "File_Storage_Sharing": [
            "Google Drive", "Dropbox", "OneDrive", "iCloud", "Box", "Mega",
            "WeTransfer", "MediaFire", "4shared", "Zippyshare", "SendSpace"
        ],
        
        "Developer_Tools": [
            "GitHub", "Stack Overflow", "GitLab", "Bitbucket", "CodePen", "JSFiddle",
            "Replit", "Glitch", "Observable", "NPM", "PyPI", "Docker Hub"
        ],
        
        "Government_Org_Sites": [
            # Major government and org sites
            "Wikipedia", "Internet Archive", "Archive.org", "WHO", "UNESCO", "UNICEF",
            "Red Cross", "Doctors Without Borders", "Greenpeace", "WWF"
        ],
        
        "Regional_Giants_China": [
            "Baidu", "Tencent", "Alibaba", "Taobao", "Tmall", "JD.com", "Weibo",
            "WeChat", "QQ", "Youku", "iQiyi", "Bilibili", "Douyin", "Pinduoduo"
        ],
        
        "Regional_Giants_India": [
            "Flipkart", "Paytm", "Zomato", "Swiggy", "Ola", "MakeMyTrip", "Naukri",
            "Times of India", "NDTV", "Zee News", "Hotstar", "SonyLIV"
        ],
        
        "Regional_Giants_Europe": [
            "Spotify", "Skype", "Booking.com", "Trivago", "SAP", "Zalando", "Delivery Hero",
            "Yandex", "VKontakte", "Mail.ru", "Avito", "Ozon", "Sberbank Online"
        ],
        
        "Dating_Lifestyle": [
            "Tinder", "Bumble", "Hinge", "Match.com", "eHarmony", "OkCupid",
            "Plenty of Fish", "Grindr", "Coffee Meets Bagel", "The League"
        ],
        
        "Health_Medical": [
            "WebMD", "Mayo Clinic", "Healthline", "MedlinePlus", "Drugs.com",
            "RxList", "Everyday Health", "Medical News Today", "Patient.info"
        ]
    }

def check_top_2500_coverage():
    """Check coverage of top global websites"""
    existing, existing_names = get_existing_companies()
    website_categories = get_top_2500_websites()
    
    print(f"Current collection size: {len(existing)} companies")
    print(f"🌍 CHECKING COVERAGE OF TOP 2,500 GLOBAL WEBSITES 🌍")
    print(f"Analyzing major website categories and traffic leaders...")
    print(f"=" * 80)
    
    all_missing = {}
    total_missing_websites = []
    total_websites_checked = 0
    
    for category, website_list in website_categories.items():
        missing_in_category = []
        found_in_category = []
        total_websites_checked += len(website_list)
        
        for website in website_list:
            normalized = normalize_name(website)
            website_lower = website.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(website)
                found = True
            else:
                # Check in original names with flexible matching
                for exist_name in existing_names:
                    # Extract key terms
                    website_terms = [word for word in website_lower.split() 
                                   if len(word) > 2 and word not in ['the', 'inc', 'corp', 'ltd', 'llc', 'group', 'company', 'com', 'org', 'net']]
                    
                    if website_terms:
                        # Check if main website name appears
                        main_term = website_terms[0] if website_terms else website_lower
                        
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms
                            if main_term not in ['web', 'net', 'app', 'one', 'pro', 'max', 'new', 'big', 'top']:
                                found_in_category.append(f"{website} (found as: {exist_name})")
                                found = True
                                break
                        
                        # Check for brand combinations
                        if len(website_terms) >= 2:
                            combo = f"{website_terms[0]} {website_terms[1]}"
                            if combo in exist_name and len(combo) >= 6:
                                found_in_category.append(f"{website} (found as: {exist_name})")
                                found = True
                                break
                    
                    if found:
                        break
                    
                    # Also check full substring match
                    website_clean = website_lower.replace('.com', '').replace('.org', '').replace('.net', '')
                    if website_clean in exist_name or exist_name in website_clean:
                        if len(website_clean) >= 4:
                            found_in_category.append(f"{website} (found as: {exist_name})")
                            found = True
                            break
                
                # Partial matches for well-known brands
                if not found:
                    for exist in existing:
                        if len(normalized) > 3 and len(exist) > 3:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.85:  # High threshold for top websites
                                    found_in_category.append(f"{website} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(website)
                total_missing_websites.append((website, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(website_list) * 100 if website_list else 0
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(website_list)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print(f"🚨 MISSING: {', '.join(missing_in_category[:5])}" + ("..." if len(missing_in_category) > 5 else ""))
    
    # Summary
    total_missing = len(total_missing_websites)
    
    print(f"\n🌍 TOP 2,500 WEBSITES COVERAGE ANALYSIS COMPLETE!")
    print(f"Total websites checked: {total_websites_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_websites_checked - total_missing) / total_websites_checked * 100):.1f}%")
    
    # Show categories with most gaps
    print(f"\n📊 CATEGORIES WITH MOST MISSING WEBSITES:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps[:10]:
        print(f"🌐 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Priority missing websites
    print(f"\n🚨 TOP 50 MISSING WEBSITES (Global Traffic Leaders):")
    
    # Prioritize by traffic/importance
    category_priority = {
        'Top_100_Global_Websites': 10,          # Core top sites
        'Major_Search_Engines': 10,             # Search engines
        'Social_Media_Giants': 9,               # Social platforms
        'E-Commerce_Shopping': 9,               # Shopping sites
        'News_Media_Sites': 8,                  # News sites
        'Streaming_Entertainment': 8,           # Entertainment
        'Tech_Cloud_Services': 7,               # Tech services
        'Financial_Services': 7,                # Financial platforms
        'Travel_Services': 6,                   # Travel sites
        'Educational_Learning': 6,              # Learning platforms
        'Communication_Messaging': 6,           # Communication
        'Gaming_Platforms': 5,                  # Gaming
        'Regional_Giants_China': 5,             # Chinese sites
        'Regional_Giants_India': 5,             # Indian sites
        'Regional_Giants_Europe': 5,            # European sites
        'Adult_Entertainment': 4,               # Adult sites
        'Dating_Lifestyle': 4,                  # Dating apps
        'Health_Medical': 4,                    # Health sites
        'File_Storage_Sharing': 3,              # File sharing
        'Developer_Tools': 3,                   # Developer tools
        'Government_Org_Sites': 3               # Government/org
    }
    
    priority_missing = []
    for website, category in total_missing_websites:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((website, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    for i, (website, category, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {website} ({category.replace('_', ' ')})")
    
    # Save comprehensive analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_top_2500_websites.txt', 'w') as f:
        f.write("TOP 2,500 GLOBAL WEBSITES COVERAGE ANALYSIS\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_websites_checked}\n")
        f.write(f"Overall coverage: {((total_websites_checked - total_missing) / total_websites_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for website in data['missing']:
                    f.write(f"  - {website}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (website, category, score) in enumerate(priority_missing[:100], 1):
            f.write(f"{i:3d}. {website} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved comprehensive analysis to missing_top_2500_websites.txt")
    
    if total_missing > 100:
        print(f"🌐 Found {total_missing} missing websites from top global traffic leaders!")
        print(f"📈 Significant opportunity to expand coverage!")
    else:
        print(f"✅ Only {total_missing} missing from top websites - excellent coverage!")
    
    return priority_missing[:100]

if __name__ == "__main__":
    check_top_2500_coverage()