#!/usr/bin/env python3
"""
Check for other "obvious" internet platforms that might be missing like Quora was
Focus on major sites, platforms, and well-known internet companies
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

def get_obvious_internet_platforms():
    """Major internet platforms and sites that should obviously be included"""
    return {
        "Major_Q&A_Knowledge_Platforms": [
            # Since Quora was missing, check similar platforms
            "Stack Overflow", "Yahoo Answers", "Ask.com", "Answers.com", "Chegg", 
            "Course Hero", "Brainly", "Slader", "StudyBlue", "Khanacademy"
        ],
        
        "Major_Social_Platforms": [
            # Core social media that should definitely be there
            "Facebook", "Instagram", "Twitter", "LinkedIn", "YouTube", "TikTok",
            "Snapchat", "Pinterest", "Reddit", "Discord", "Twitch", "WhatsApp"
        ],
        
        "News_Information_Sites": [
            # Major news and information platforms
            "Wikipedia", "CNN", "BBC", "Fox News", "MSNBC", "Reuters", "Associated Press",
            "Buzzfeed", "Vox Media", "Vice", "Medium", "Substack", "WordPress"
        ],
        
        "Search_Web_Services": [
            # Major search and web service platforms  
            "Google", "Bing", "Yahoo", "DuckDuckGo", "Baidu", "Yandex",
            "Internet Archive", "Archive.org", "Wayback Machine"
        ],
        
        "E-commerce_Marketplaces": [
            # Major e-commerce and marketplace platforms
            "Amazon", "eBay", "Etsy", "Craigslist", "Facebook Marketplace", "Mercari",
            "Poshmark", "Depop", "Vinted", "Reverb", "StockX", "GOAT"
        ],
        
        "Streaming_Entertainment": [
            # Major streaming and entertainment platforms
            "Netflix", "Spotify", "Apple Music", "YouTube Music", "Pandora", "SoundCloud",
            "Twitch", "OnlyFans", "Patreon", "Substack", "Cameo"
        ],
        
        "Dating_Social_Apps": [
            # Major dating and social connection apps
            "Tinder", "Bumble", "Hinge", "Match.com", "eHarmony", "OkCupid",
            "Plenty of Fish", "Grindr", "Coffee Meets Bagel", "The League"
        ],
        
        "Travel_Local_Services": [
            # Major travel and local service platforms
            "Yelp", "TripAdvisor", "Foursquare", "OpenTable", "Resy", "Tock",
            "Groupon", "LivingSocial", "Eventbrite", "Meetup", "Nextdoor"
        ],
        
        "Financial_Crypto_Platforms": [
            # Major fintech and crypto platforms
            "PayPal", "Venmo", "Cash App", "Zelle", "Coinbase", "Binance", "Kraken",
            "Robinhood", "Webull", "TD Ameritrade", "E*TRADE", "Fidelity", "Schwab"
        ],
        
        "Developer_Tech_Platforms": [
            # Major developer and tech platforms
            "GitHub", "GitLab", "Stack Overflow", "CodePen", "JSFiddle", "Replit",
            "Heroku", "Vercel", "Netlify", "Digital Ocean", "Linode", "Vultr"
        ],
        
        "Communication_Messaging": [
            # Major communication platforms
            "Slack", "Microsoft Teams", "Zoom", "Skype", "Google Meet", "WebEx",
            "Signal", "Telegram", "WhatsApp", "Discord", "Clubhouse", "Twitter Spaces"
        ],
        
        "File_Cloud_Storage": [
            # Major file storage and cloud platforms
            "Google Drive", "Dropbox", "OneDrive", "iCloud", "Box", "AWS", "Google Cloud",
            "Microsoft Azure", "WeTransfer", "Send Anywhere", "Firefox Send"
        ]
    }

def check_obvious_platforms():
    """Check what obvious internet platforms might be missing"""
    existing, existing_names = get_existing_companies()
    categories = get_obvious_internet_platforms()
    
    print(f"Current collection size: {len(existing)} companies")
    print(f"🔍 CHECKING FOR OTHER 'OBVIOUS' MISSING PLATFORMS (Like Quora) 🔍")
    print(f"Focusing on major internet platforms and well-known sites...")
    print(f"=" * 80)
    
    all_missing = {}
    total_missing_companies = []
    
    for category, platform_list in categories.items():
        missing_in_category = []
        found_in_category = []
        
        for platform in platform_list:
            normalized = normalize_name(platform)
            platform_lower = platform.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(platform)
                found = True
            else:
                # Check in original names with flexible matching
                for exist_name in existing_names:
                    # Extract key terms
                    platform_terms = [word for word in platform_lower.split() 
                                    if len(word) > 2 and word not in ['the', 'inc', 'corp', 'ltd', 'llc', 'group', 'company', 'com', 'org']]
                    
                    if platform_terms:
                        # Check if main platform name appears
                        main_term = platform_terms[0] if platform_terms else platform_lower
                        
                        if main_term in exist_name and len(main_term) >= 3:
                            # Skip overly common terms
                            if main_term not in ['app', 'web', 'net', 'one', 'pro', 'max', 'new', 'big']:
                                found_in_category.append(f"{platform} (found as: {exist_name})")
                                found = True
                                break
                        
                        # Check for brand combinations
                        if len(platform_terms) >= 2:
                            combo = f"{platform_terms[0]} {platform_terms[1]}"
                            if combo in exist_name and len(combo) >= 6:
                                found_in_category.append(f"{platform} (found as: {exist_name})")
                                found = True
                                break
                    
                    if found:
                        break
                    
                    # Also check full substring match
                    if platform_lower in exist_name or exist_name in platform_lower:
                        if len(platform_lower) >= 4:
                            found_in_category.append(f"{platform} (found as: {exist_name})")
                            found = True
                            break
                
                # Partial matches for well-known brands
                if not found:
                    for exist in existing:
                        if len(normalized) > 3 and len(exist) > 3:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.8:  # High threshold for obvious platforms
                                    found_in_category.append(f"{platform} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(platform)
                total_missing_companies.append((platform, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(platform_list) * 100 if platform_list else 0
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(platform_list)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print(f"🚨 MISSING: {', '.join(missing_in_category[:6])}" + ("..." if len(missing_in_category) > 6 else ""))
    
    # Summary
    total_missing = len(total_missing_companies)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🔍 OBVIOUS PLATFORMS ANALYSIS COMPLETE!")
    print(f"Total platforms checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Show categories with most gaps
    print(f"\n📊 CATEGORIES WITH MOST MISSING PLATFORMS:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps[:8]:
        print(f"🔍 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Priority missing platforms
    print(f"\n🚨 TOP 30 MISSING 'OBVIOUS' PLATFORMS:")
    
    # Prioritize by how obvious/well-known they are
    category_priority = {
        'Major_Social_Platforms': 10,           # These should definitely be there
        'Major_Q&A_Knowledge_Platforms': 9,     # Like Quora that was missing
        'Search_Web_Services': 9,               # Major search engines
        'E-commerce_Marketplaces': 8,           # Major shopping platforms  
        'Streaming_Entertainment': 8,           # Major entertainment platforms
        'News_Information_Sites': 7,            # Major news sites
        'Financial_Crypto_Platforms': 7,        # Major fintech platforms
        'Communication_Messaging': 6,           # Major communication tools
        'Dating_Social_Apps': 6,                # Major dating apps
        'Travel_Local_Services': 5,             # Local service platforms
        'Developer_Tech_Platforms': 5,          # Developer tools
        'File_Cloud_Storage': 4                 # Cloud storage
    }
    
    priority_missing = []
    for platform, category in total_missing_companies:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((platform, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    for i, (platform, category, score) in enumerate(priority_missing[:30], 1):
        print(f"{i:2d}. {platform} ({category.replace('_', ' ')})")
    
    # Save analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_obvious_platforms.txt', 'w') as f:
        f.write("MISSING 'OBVIOUS' INTERNET PLATFORMS ANALYSIS\n")
        f.write("Inspired by the fact that Quora was missing\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_checked}\n")
        f.write(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for platform in data['missing']:
                    f.write(f"  - {platform}\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (platform, category, score) in enumerate(priority_missing[:50], 1):
            f.write(f"{i:3d}. {platform} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved analysis to missing_obvious_platforms.txt")
    
    if total_missing > 20:
        print(f"🤔 Found {total_missing} potentially missing obvious platforms!")
        print(f"Some of these might be legitimately missing like Quora was!")
    else:
        print(f"✅ Only {total_missing} missing - collection is very comprehensive!")
    
    return priority_missing[:30]

if __name__ == "__main__":
    check_obvious_platforms()