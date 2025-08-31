#!/usr/bin/env python3
"""
Check coverage of the TOP 3,500 websites globally
Extended analysis beyond the initial 2,500 to find more missing platforms
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

def get_extended_top_3500_websites():
    """Extended list covering ranks 2,500 to 3,500+ in global web traffic"""
    return {
        "Extended_E_Commerce": [
            # More e-commerce platforms
            "Wish", "DHgate", "Banggood", "Gearbest", "LightInTheBox", "MiniInTheBox",
            "Newegg", "Overstock", "Wayfair", "Chewy", "Petco", "PetSmart",
            "1688.com", "Made-in-China", "GlobalSources", "TradeIndia", "IndiaMART"
        ],
        
        "Regional_Social_Platforms": [
            # More regional social media
            "Odnoklassniki", "LiveJournal", "Friendster", "Orkut", "Hi5", "Bebo",
            "Xing", "Renren", "Douban", "Tianya", "Momo", "Tantan", "Soul",
            "MeetMe", "Tagged", "Badoo", "Skout", "LOVOO", "Zoosk"
        ],
        
        "Extended_News_Media": [
            # More news and media sites
            "Al Jazeera", "RT", "Xinhua", "CGTN", "NHK", "France24", "Deutsche Welle",
            "Sputnik", "Press TV", "TRT World", "Channel NewsAsia", "SCMP",
            "The Times of India", "Hindustan Times", "The Hindu", "Indian Express",
            "Dawn", "The Express Tribune", "Gulf News", "Arab News"
        ],
        
        "Specialized_Platforms": [
            # Specialized interest platforms
            "DeviantArt", "Behance", "Dribbble", "99designs", "Fiverr", "Upwork",
            "Freelancer", "Guru", "PeoplePerHour", "Toptal", "Odesk", "Elance",
            "AngelList", "Product Hunt", "Hacker News", "Slashdot", "Digg"
        ],
        
        "Extended_Gaming": [
            # More gaming platforms
            "Miniclip", "Armor Games", "Kongregate", "Newgrounds", "AddictingGames",
            "Y8", "Pogo", "Big Fish Games", "King", "Supercell", "Rovio",
            "Gameloft", "Glu Mobile", "Zynga", "Machine Zone", "Kabam"
        ],
        
        "Regional_Search_Portals": [
            # Regional search engines and portals
            "Naver", "Daum", "Seznam", "Rambler", "Yahoo Japan", "Goo", "Excite",
            "Lycos", "Altavista", "HotBot", "WebCrawler", "InfoSeek", "Northern Light"
        ],
        
        "Extended_Streaming": [
            # More streaming and media
            "Dailymotion", "Metacafe", "Break", "Funny or Die", "College Humor",
            "9GAG", "Imgur", "Flickr", "PhotoBucket", "ImageShack", "TinyPic",
            "Last.fm", "Grooveshark", "Rdio", "Deezer", "Tidal", "Qobuz"
        ],
        
        "Business_B2B_Platforms": [
            # B2B and business platforms
            "Alibaba.com", "DHgate", "Made-in-China", "Global Sources", "TradeIndia",
            "ThomasNet", "Kompass", "Europages", "Export.gov", "HKTDC", "Canton Fair",
            "Reed Exhibitions", "Informa", "UBM", "Messe Frankfurt", "Hannover Messe"
        ],
        
        "Extended_Travel_Local": [
            # More travel and local services
            "Yelp", "Zomato", "Urbanspoon", "Chomp", "Seamless", "GrubHub",
            "DoorDash", "Uber Eats", "Postmates", "Caviar", "Eat24", "Delivery.com",
            "OpenRice", "Dianping", "Meituan", "Ele.me", "Swiggy", "Zomato India"
        ],
        
        "Extended_Education": [
            # More educational platforms
            "Blackboard", "Moodle", "Canvas", "Schoology", "Google Classroom",
            "Khan Academy", "Coursera", "edX", "Udacity", "Pluralsight", "Lynda",
            "Skillshare", "MasterClass", "Udemy", "Codecademy", "FreeCodeCamp"
        ],
        
        "Productivity_Tools_Extended": [
            # More productivity platforms
            "Evernote", "OneNote", "Notion", "Obsidian", "Roam Research",
            "Airtable", "Zapier", "IFTTT", "Microsoft Power Automate", "Integromat",
            "Buffer", "Hootsuite", "Sprout Social", "Later", "SocialBee"
        ],
        
        "Extended_Finance": [
            # More financial platforms
            "Mint", "Personal Capital", "YNAB", "Quicken", "QuickBooks", "FreshBooks",
            "Wave Accounting", "Xero", "Sage", "Zoho Books", "Invoice2go", "Square"
        ],
        
        "Forums_Communities": [
            # Forums and community platforms
            "4chan", "8kun", "Something Awful", "NeoGAF", "GameFAQs", "IGN Boards",
            "Reddit", "Voat", "Gab", "Parler", "MeWe", "Minds", "Diaspora",
            "Mastodon", "Pleroma", "GNU Social", "Hubzilla", "Friendica"
        ],
        
        "Regional_Giants_Extended": [
            # More regional platforms
            "Rakuten", "Yahoo Japan", "Mercari Japan", "Cookpad", "Mixi", "Ameba",
            "FC2", "Nico Nico Douga", "Pixiv", "Hatena", "Gree", "DeNA", "CyberAgent",
            "Line Corporation", "Kakao", "Naver Corporation", "Coupang", "11Street"
        ],
        
        "Technology_Developer_Extended": [
            # More tech/developer platforms
            "SourceForge", "CodeProject", "Planet Source Code", "DZone", "InfoQ",
            "TechCrunch", "VentureBeat", "ReadWrite", "Mashable", "The Next Web",
            "Ars Technica", "Engadget", "Gizmodo", "The Verge", "CNET", "ZDNet"
        ],
        
        "Extended_Health_Medical": [
            # More health platforms
            "Mayo Clinic", "WebMD", "Healthline", "Medical News Today", "Medscape",
            "Drugs.com", "RxList", "Patient.info", "Everyday Health", "Health.com",
            "Verywell Health", "Healthgrades", "Vitals", "Zocdoc", "MDLive"
        ]
    }

def check_top_3500_coverage():
    """Check coverage of extended top 3,500 websites"""
    existing, existing_names = get_existing_companies()
    extended_categories = get_extended_top_3500_websites()
    
    print(f"Current collection size: {len(existing)} companies")
    print(f"🌐 CHECKING COVERAGE OF TOP 3,500 GLOBAL WEBSITES (Extended Analysis) 🌐")
    print(f"Analyzing additional website categories from ranks 2,500-3,500+...")
    print(f"=" * 90)
    
    all_missing = {}
    total_missing_websites = []
    total_websites_checked = 0
    
    for category, website_list in extended_categories.items():
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
                            if main_term not in ['web', 'net', 'app', 'one', 'pro', 'max', 'new', 'big', 'top', 'best', 'news']:
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
                    website_clean = website_lower.replace('.com', '').replace('.org', '').replace('.net', '').replace('.co', '').replace('.jp', '')
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
                                if match_ratio > 0.80:  # High threshold for top websites
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
            print(f"🚨 MISSING: {', '.join(missing_in_category[:6])}" + ("..." if len(missing_in_category) > 6 else ""))
    
    # Summary
    total_missing = len(total_missing_websites)
    
    print(f"\n🌐 TOP 3,500 WEBSITES EXTENDED ANALYSIS COMPLETE!")
    print(f"Extended websites checked: {total_websites_checked}")
    print(f"Total missing from extended list: {total_missing}")
    print(f"Extended categories coverage: {((total_websites_checked - total_missing) / total_websites_checked * 100):.1f}%")
    
    # Show categories with most gaps
    print(f"\n📊 EXTENDED CATEGORIES WITH MOST MISSING WEBSITES:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps[:12]:
        print(f"🌐 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Priority missing websites from extended analysis
    print(f"\n🚨 TOP 50 MISSING WEBSITES FROM EXTENDED 3,500 ANALYSIS:")
    
    # Prioritize by traffic/importance for extended list
    category_priority = {
        'Extended_E_Commerce': 9,               # E-commerce platforms
        'Regional_Social_Platforms': 8,         # Regional social media
        'Extended_News_Media': 8,               # International news
        'Specialized_Platforms': 7,             # Creative/freelance platforms  
        'Extended_Gaming': 7,                   # Gaming platforms
        'Regional_Search_Portals': 6,           # Regional search engines
        'Extended_Streaming': 6,                # Media platforms
        'Business_B2B_Platforms': 6,           # B2B platforms
        'Extended_Travel_Local': 5,             # Travel/local services
        'Extended_Education': 5,                # Educational platforms
        'Productivity_Tools_Extended': 5,       # Productivity tools
        'Extended_Finance': 4,                  # Financial tools
        'Forums_Communities': 4,                # Forums
        'Regional_Giants_Extended': 4,          # Regional platforms
        'Technology_Developer_Extended': 3,     # Tech news/dev platforms
        'Extended_Health_Medical': 3            # Health platforms
    }
    
    priority_missing = []
    for website, category in total_missing_websites:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((website, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    for i, (website, category, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {website} ({category.replace('_', ' ')})")
    
    # Save comprehensive extended analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_top_3500_websites_extended.txt', 'w') as f:
        f.write("TOP 3,500 GLOBAL WEBSITES EXTENDED COVERAGE ANALYSIS\n")
        f.write("Extended analysis beyond initial top 2,500\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Extended websites missing: {total_missing}\n")
        f.write(f"Extended websites checked: {total_websites_checked}\n")
        f.write(f"Extended coverage: {((total_websites_checked - total_missing) / total_websites_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for website in data['missing']:
                    f.write(f"  - {website}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING FROM EXTENDED ANALYSIS ###\n")
        for i, (website, category, score) in enumerate(priority_missing[:100], 1):
            f.write(f"{i:3d}. {website} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved extended analysis to missing_top_3500_websites_extended.txt")
    
    # Combined summary
    original_missing = 34  # From first analysis
    original_checked = 316  # From first analysis
    combined_missing = original_missing + total_missing - 19  # Subtract what we already downloaded
    combined_checked = original_checked + total_websites_checked
    combined_coverage = ((combined_checked - combined_missing) / combined_checked * 100)
    
    print(f"\n🎯 COMBINED TOP 3,500 WEBSITES ANALYSIS:")
    print(f"Combined websites checked: {combined_checked}")
    print(f"Combined missing: {combined_missing}")
    print(f"Combined coverage: {combined_coverage:.1f}%")
    
    if total_missing > 50:
        print(f"🌐 Found {total_missing} additional missing websites in extended analysis!")
        print(f"📈 Major opportunity to expand global web coverage further!")
    else:
        print(f"✅ Extended analysis shows excellent coverage - only {total_missing} additional missing!")
    
    return priority_missing[:50]

if __name__ == "__main__":
    check_top_3500_coverage()