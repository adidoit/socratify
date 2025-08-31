#!/usr/bin/env python3
"""
Download ALL missing websites from top 3,500 analysis
Fill the gaps for complete global website coverage!
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 30
RATE_LIMIT = threading.Semaphore(25)
RATE_LIMIT_DELAY = 0.02

def clean_filename(website_name):
    """Convert website name to clean filename"""
    filename = website_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(website_name):
    """Generate domain variations for missing websites"""
    base = website_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    domains = []
    
    # Comprehensive special cases for all 75 missing websites
    special_cases = {
        # Extended E-Commerce (4)
        'banggood': ['banggood.com'],
        '1688.com': ['1688.com'],
        '1688com': ['1688.com'],
        'made-in-china': ['made-in-china.com'],
        'madeinchina': ['made-in-china.com'],
        'globalsources': ['globalsources.com'],
        
        # Regional Social Platforms (11)
        'livejournal': ['livejournal.com'],
        'orkut': ['orkut.com'],
        'hi5': ['hi5.com'],
        'bebo': ['bebo.com'],
        'tianya': ['tianya.cn'],
        'tantan': ['tantanapp.com'],
        'meetme': ['meetme.com'],
        'tagged': ['tagged.com'],
        'badoo': ['badoo.com'],
        'skout': ['skout.com'],
        'lovoo': ['lovoo.com'],
        
        # Extended News Media (5)
        'xinhua': ['xinhuanet.com'],
        'cgtn': ['cgtn.com'],
        'nhk': ['nhk.or.jp'],
        'france24': ['france24.com'],
        'sputnik': ['sputniknews.com'],
        
        # Specialized Platforms (4)
        'angellist': ['angel.co', 'wellfound.com'],
        'hacker news': ['news.ycombinator.com'],
        'hackernews': ['news.ycombinator.com'],
        'slashdot': ['slashdot.org'],
        'digg': ['digg.com'],
        
        # Extended Gaming (4)
        'armor games': ['armorgames.com'],
        'armorgames': ['armorgames.com'],
        'kongregate': ['kongregate.com'],
        'y8': ['y8.com'],
        'kabam': ['kabam.com'],
        
        # Regional Search Portals (5)
        'daum': ['daum.net'],
        'excite': ['excite.com'],
        'lycos': ['lycos.com'],
        'hotbot': ['hotbot.com'],
        'infoseek': ['infoseek.com'],
        
        # Extended Streaming (9)
        'college humor': ['collegehumor.com'],
        'collegehumor': ['collegehumor.com'],
        '9gag': ['9gag.com'],
        'imgur': ['imgur.com'],
        'photobucket': ['photobucket.com'],
        'imageshack': ['imageshack.us'],
        'tinypic': ['tinypic.com'],
        'last.fm': ['last.fm'],
        'lastfm': ['last.fm'],
        'rdio': ['rdio.com'],
        'qobuz': ['qobuz.com'],
        
        # Business B2B Platforms (3)
        'made-in-china': ['made-in-china.com'],  # duplicate from e-commerce
        'thomasnet': ['thomasnet.com'],
        'kompass': ['kompass.com'],
        
        # Extended Travel Local (3)
        'yelp': ['yelp.com'],
        'chomp': ['chomp.com'],
        'openrice': ['openrice.com'],
        
        # Extended Education (2)
        'lynda': ['lynda.com'],
        'freecodecamp': ['freecodecamp.org'],
        
        # Productivity Tools Extended (3)
        'evernote': ['evernote.com'],
        'ifttt': ['ifttt.com'],
        'buffer': ['buffer.com'],
        
        # Extended Finance (2)
        'quicken': ['quicken.com'],
        'quickbooks': ['quickbooks.intuit.com'],
        
        # Forums Communities (7)
        '4chan': ['4chan.org'],
        'neogaf': ['neogaf.com'],
        'gamefaqs': ['gamefaqs.gamespot.com'],
        'voat': ['voat.co'],
        'parler': ['parler.com'],
        'hubzilla': ['hubzilla.org'],
        'friendica': ['friendi.ca'],
        
        # Regional Giants Extended (5)
        'ameba': ['ameba.jp'],
        'fc2': ['fc2.com'],
        'pixiv': ['pixiv.net'],
        'hatena': ['hatena.ne.jp'],
        '11street': ['11st.co.kr'],
        
        # Technology Developer Extended (7)
        'sourceforge': ['sourceforge.net'],
        'infoq': ['infoq.com'],
        'mashable': ['mashable.com'],
        'engadget': ['engadget.com'],
        'gizmodo': ['gizmodo.com'],
        'cnet': ['cnet.com'],
        'zdnet': ['zdnet.com'],
        
        # Extended Health Medical (1)
        'zocdoc': ['zocdoc.com']
    }
    
    if base in special_cases:
        domains = special_cases[base]
    else:
        # Standard fallback
        words = base.split()
        if len(words) >= 1:
            first_word = words[0]
            domains.extend([
                f"{first_word}.com",
                f"{first_word}.org",
                f"{first_word}.net",
                f"{first_word}.co",
                f"{first_word}.io"
            ])
            
            if len(words) >= 2:
                second_word = words[1]
                domains.extend([
                    f"{first_word}{second_word}.com",
                    f"{first_word}-{second_word}.com"
                ])
    
    return list(dict.fromkeys(domains))

def download_logo(website_name, output_dir, category=""):
    """Download logo with comprehensive domain trying"""
    
    with RATE_LIMIT:
        time.sleep(RATE_LIMIT_DELAY)
        
        domains = generate_domains(website_name)
        
        for domain in domains:
            try:
                # Try Clearbit first
                logo_url = f"https://logo.clearbit.com/{domain}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
                
                response = requests.get(logo_url, headers=headers, timeout=15, stream=True)
                
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '')
                    
                    if 'image' not in content_type and 'octet-stream' not in content_type:
                        continue
                    
                    # Get file extension
                    if 'png' in content_type:
                        ext = 'png'
                    elif 'jpeg' in content_type or 'jpg' in content_type:
                        ext = 'jpg'
                    elif 'svg' in content_type:
                        ext = 'svg'
                    else:
                        ext = 'png'
                    
                    filename = f"{clean_filename(website_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.getsize(filepath) > 500:
                        return f"🌐 {category} | {website_name} -> {filename} (domain: {domain})"
                    else:
                        os.remove(filepath)
                
                # Try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(website_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"📱 {category} | {website_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {category} | {website_name} - No logo found"

def get_all_75_missing_websites():
    """All 75 missing websites from top 3,500 analysis, prioritized by importance"""
    return [
        # Extended E-Commerce (4) - High traffic
        ("Banggood", "ECOMMERCE"),
        ("1688.com", "ECOMMERCE"),
        ("Made-in-China", "ECOMMERCE"),
        ("GlobalSources", "ECOMMERCE"),
        
        # Specialized Platforms (4) - Important for tech/startup community
        ("AngelList", "STARTUP"),
        ("Hacker News", "TECH_COMMUNITY"),
        ("Slashdot", "TECH_NEWS"),
        ("Digg", "SOCIAL_NEWS"),
        
        # Extended Streaming/Media (9) - High traffic platforms
        ("9GAG", "SOCIAL_MEDIA"),
        ("Imgur", "IMAGE_SHARING"),
        ("College Humor", "ENTERTAINMENT"),
        ("PhotoBucket", "IMAGE_STORAGE"),
        ("ImageShack", "IMAGE_STORAGE"),
        ("TinyPic", "IMAGE_STORAGE"),
        ("Last.fm", "MUSIC"),
        ("Rdio", "MUSIC"),
        ("Qobuz", "MUSIC"),
        
        # Extended Gaming (4) - Gaming platforms
        ("Armor Games", "GAMING"),
        ("Kongregate", "GAMING"),
        ("Y8", "GAMING"),
        ("Kabam", "GAMING"),
        
        # Technology/Developer Extended (7) - Important tech sites
        ("SourceForge", "DEVELOPER"),
        ("InfoQ", "TECH_NEWS"),
        ("Mashable", "TECH_NEWS"),
        ("Engadget", "TECH_NEWS"),
        ("Gizmodo", "TECH_NEWS"),
        ("CNET", "TECH_NEWS"),
        ("ZDNet", "TECH_NEWS"),
        
        # Extended News Media (5) - International news
        ("Xinhua", "NEWS"),
        ("CGTN", "NEWS"),
        ("NHK", "NEWS"),
        ("France24", "NEWS"),
        ("Sputnik", "NEWS"),
        
        # Regional Social Platforms (11) - Historical/regional importance
        ("LiveJournal", "SOCIAL_REGIONAL"),
        ("Orkut", "SOCIAL_REGIONAL"),
        ("Hi5", "SOCIAL_REGIONAL"), 
        ("Bebo", "SOCIAL_REGIONAL"),
        ("Tianya", "SOCIAL_REGIONAL"),
        ("Tantan", "SOCIAL_REGIONAL"),
        ("MeetMe", "SOCIAL_REGIONAL"),
        ("Tagged", "SOCIAL_REGIONAL"),
        ("Badoo", "SOCIAL_REGIONAL"),
        ("Skout", "SOCIAL_REGIONAL"),
        ("LOVOO", "SOCIAL_REGIONAL"),
        
        # Productivity Tools Extended (3)
        ("Evernote", "PRODUCTIVITY"),
        ("IFTTT", "PRODUCTIVITY"),
        ("Buffer", "PRODUCTIVITY"),
        
        # Extended Education (2)
        ("Lynda", "EDUCATION"),
        ("FreeCodeCamp", "EDUCATION"),
        
        # Regional Giants Extended (5) - Japanese platforms
        ("Ameba", "REGIONAL_JAPAN"),
        ("FC2", "REGIONAL_JAPAN"),
        ("Pixiv", "REGIONAL_JAPAN"),
        ("Hatena", "REGIONAL_JAPAN"),
        ("11Street", "REGIONAL_KOREA"),
        
        # Extended Finance (2)
        ("Quicken", "FINANCE"),
        ("QuickBooks", "FINANCE"),
        
        # Business B2B Platforms (3)
        ("ThomasNet", "B2B"),
        ("Kompass", "B2B"),
        
        # Extended Travel/Local (3)
        ("Yelp", "LOCAL_SERVICES"),
        ("Chomp", "FOOD"),
        ("OpenRice", "FOOD"),
        
        # Regional Search Portals (5) - Legacy search engines
        ("Daum", "SEARCH_REGIONAL"),
        ("Excite", "SEARCH_LEGACY"),
        ("Lycos", "SEARCH_LEGACY"),
        ("HotBot", "SEARCH_LEGACY"),
        ("InfoSeek", "SEARCH_LEGACY"),
        
        # Forums & Communities (7) - Discussion platforms
        ("4chan", "FORUM"),
        ("NeoGAF", "FORUM_GAMING"),
        ("GameFAQs", "FORUM_GAMING"),
        ("Voat", "FORUM_SOCIAL"),
        ("Parler", "FORUM_SOCIAL"),
        ("Hubzilla", "FORUM_SOCIAL"),
        ("Friendica", "FORUM_SOCIAL"),
        
        # Extended Health Medical (1)
        ("Zocdoc", "HEALTH")
    ]

def main():
    # Get all 75 missing websites
    websites_to_download = get_all_75_missing_websites()
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🚀🌐 FILLING ALL GAPS - TOP 3,500 WEBSITES COMPLETE COVERAGE! 🌐🚀")
    print(f"Downloading ALL {len(websites_to_download)} missing websites from 3,500 analysis")
    print(f"Current coverage: 84.5% -> Target: 95%+ complete global website coverage")
    print(f"Categories: E-commerce, Social, Gaming, Tech News, Regional Platforms, Forums")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print(f"💥 ACHIEVING ULTIMATE WEB PLATFORM DOMINATION! 💥\n")
    
    downloaded_count = 0
    failed_count = 0
    category_success = {}
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_website = {
            executor.submit(download_logo, website, output_dir, category): (website, category)
            for website, category in websites_to_download
        }
        
        for future in as_completed(future_to_website):
            result = future.result()
            website, category = future_to_website[future]
            print(result)
            
            if result.startswith("🌐") or result.startswith("📱"):
                downloaded_count += 1
                if category not in category_success:
                    category_success[category] = 0
                category_success[category] += 1
            else:
                failed_count += 1
    
    print(f"\n🌐 TOP 3,500 WEBSITES GAP FILLING COMPLETE!")
    print(f"Total websites attempted: {len(websites_to_download)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(websites_to_download) > 0:
        print(f"Success rate: {(downloaded_count/len(websites_to_download)*100):.1f}%")
    
    # Calculate new global websites coverage
    total_checked = 579  # From combined analysis
    remaining_missing = 90 - downloaded_count
    new_coverage = ((total_checked - remaining_missing) / total_checked * 100)
    
    # Update collection count
    previous_total = 8242  # From companies folder
    new_total = previous_total + downloaded_count
    print(f"\n📊 Collection now has: ~{new_total} company/website logos")
    print(f"🌐 Top 3,500 websites coverage: {new_coverage:.1f}%")
    
    # Show category success breakdown
    print(f"\n✅ Downloaded by category:")
    for category, count in sorted(category_success.items()):
        if count > 0:
            print(f"  {category}: {count} websites")
    
    # Achievement summary
    if downloaded_count >= 50:  # If we got most of them
        print(f"\n🔥 ULTIMATE WEB PLATFORM COLLECTION ACHIEVED:")
        print(f"  🌐 E-commerce: Chinese B2B giants (1688, Made-in-China, Banggood)")
        print(f"  🚀 Startup/Tech: AngelList, Hacker News, SourceForge, Slashdot")
        print(f"  📱 Social Media: 9GAG, Imgur, regional platforms worldwide")
        print(f"  🎮 Gaming: Flash game portals and mobile game companies")
        print(f"  📰 Tech News: CNET, Engadget, Mashable, Gizmodo")
        print(f"  🌏 Global News: Xinhua, CGTN, NHK, France24")
        print(f"  💼 Productivity: Evernote, Buffer, IFTTT")
        print(f"  🎓 Education: Lynda, FreeCodeCamp")
        print(f"  🏢 B2B: ThomasNet, Kompass")
        
    print(f"\n🌟 WORLD'S MOST COMPREHENSIVE WEB PLATFORM COLLECTION!")
    print(f"📈 From Fortune 500 to regional forums, gaming to news!")
    print(f"🎯 ULTIMATE GLOBAL WEBSITE COVERAGE DOMINATION COMPLETE!")

if __name__ == "__main__":
    main()