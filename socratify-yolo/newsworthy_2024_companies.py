#!/usr/bin/env python3
"""
Newsworthy 2024-2025 Companies Logo Downloader
Focus on companies that have been featured in TechCrunch, VentureBeat, Forbes in 2023-2024
Companies with Series A+ funding, significant growth, or unique business models
"""

import requests
import os
import json
import time
import random
from urllib.parse import urljoin, urlparse
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Newsworthy2024Downloader:
    def __init__(self, download_dir="newsworthy_2024_companies"):
        self.download_dir = download_dir
        self.downloaded_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.progress_file = "newsworthy_2024_progress.json"
        self.results_file = "newsworthy_2024_results.json"
        
        # Ensure download directory exists
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Load progress if exists
        self.downloaded_companies = self.load_progress()
        
        # Newsworthy companies that have been in the news in 2023-2024
        self.newsworthy_companies = {
            # AI & Machine Learning (hot in 2024)
            "ai_ml_2024": [
                "Perplexity AI", "Character.AI", "Anthropic", "Cohere", "Hugging Face",
                "Runway ML", "Stability AI", "MidJourney", "Jasper AI", "Copy.ai",
                "Writesonic", "Synthesia", "ElevenLabs", "Murf AI", "Pictory",
                "Luma AI", "Leonardo.AI", "Tome", "Beautiful.AI", "Gamma",
                "Otter.ai", "Rev.com", "Descript", "Resemble AI", "Speechify",
                "DeepL", "Grammarly", "Notion AI", "Zapier", "Make.com"
            ],
            
            # Fintech Unicorns & Recent Funding
            "fintech_2024": [
                "Klarna", "Afterpay", "Affirm", "Zip", "Sezzle", "Quadpay",
                "Revolut", "N26", "Monzo", "Starling Bank", "Chime", "Current",
                "SoFi", "Credit Karma", "NerdWallet", "Personal Capital", "Mint",
                "Robinhood", "Webull", "Public", "Freetrade", "Trading 212",
                "Wise", "Remitly", "Western Union", "MoneyGram", "WorldRemit",
                "Ramp", "Brex", "Expensify", "Mercury", "Novo Bank"
            ],
            
            # E-commerce & Marketplace (high growth)
            "ecommerce_2024": [
                "Shein", "Temu", "AliExpress", "Wish", "Mercari", "Poshmark",
                "ThredUp", "The RealReal", "Vestiaire Collective", "Rebag",
                "StockX", "GOAT", "Grailed", "Depop", "Vinted", "Kidizen",
                "Facebook Marketplace", "OfferUp", "Letgo", "5miles", "VarageSale",
                "Pinkoi", "Etsy", "Amazon Handmade", "Bonanza", "Aftcra",
                "Gumtree", "Craigslist", "Kijiji", "OLX", "Avito"
            ],
            
            # Health Tech & Telemedicine
            "healthtech_2024": [
                "Teladoc", "Amwell", "MDLive", "Doctor on Demand", "PlushCare",
                "Ro", "Hims", "Lemonstand", "Curology", "Nurx", "Simple Health",
                "Everlywell", "23andMe", "AncestryDNA", "MyHeritage", "FamilyTreeDNA",
                "Headspace", "Calm", "BetterHelp", "Talkspace", "Cerebral",
                "Ginger", "Lyra Health", "Spring Health", "Modern Health", "Mindstrong",
                "Oscar Health", "Clover Health", "Bright Health", "Devoted Health", "Alignment Healthcare"
            ],
            
            # Crypto & Web3 (despite volatility)
            "crypto_web3_2024": [
                "Coinbase", "Binance", "FTX", "Kraken", "Gemini", "KuCoin",
                "Crypto.com", "BlockFi", "Celsius", "Nexo", "BitPay", "Circle",
                "Ripple", "Chainlink", "Uniswap", "Aave", "Compound", "MakerDAO",
                "OpenSea", "Rarible", "SuperRare", "Foundation", "Async Art",
                "Axie Infinity", "The Sandbox", "Decentraland", "Enjin", "Immutable X",
                "Dapper Labs", "NBA Top Shot", "CryptoKitties", "Sorare", "Gods Unchained"
            ],
            
            # Climate Tech & Sustainability
            "climate_tech_2024": [
                "Tesla Energy", "Rivian", "Lucid Motors", "Fisker", "Canoo",
                "ChargePoint", "EVgo", "Electrify America", "Volta", "Blink Charging",
                "Sunrun", "Sunnova", "Vivint Solar", "Tesla Solar", "Enphase",
                "SolarEdge", "First Solar", "Canadian Solar", "JinkoSolar", "LONGi",
                "Vestas", "Siemens Gamesa", "GE Renewable Energy", "Nordex", "Goldwind",
                "Beyond Meat", "Impossible Foods", "Oatly", "Perfect Day", "Upside Foods"
            ],
            
            # Social Media & Creator Economy
            "social_creator_2024": [
                "TikTok", "BeReal", "Clubhouse", "Discord", "Telegram", "Signal",
                "Mastodon", "Threads", "Bluesky", "Post", "Hive Social", "Vero",
                "Patreon", "OnlyFans", "Ko-fi", "Buy Me a Coffee", "Gumroad",
                "Substack", "Ghost", "ConvertKit", "Mailchimp", "Beehiiv",
                "Kajabi", "Teachable", "Thinkific", "Mighty Networks", "Circle",
                "Twitch", "YouTube", "Kick", "Rumble", "Odysee"
            ],
            
            # Gaming & Metaverse
            "gaming_metaverse_2024": [
                "Epic Games", "Roblox", "Unity", "Unreal Engine", "Godot", "GameMaker",
                "Discord", "Steam", "Epic Games Store", "Itch.io", "Game Jolt",
                "Meta Quest", "PICO", "HTC Vive", "Valve Index", "PlayStation VR",
                "Microsoft HoloLens", "Magic Leap", "Nreal", "Rokid", "Varjo",
                "Horizon Worlds", "VRChat", "RecRoom", "AltspaceVR", "Mozilla Hubs",
                "Nvidia Omniverse", "Unity Reflect", "Autodesk Maya", "Blender", "Cinema 4D"
            ],
            
            # DevTools & Infrastructure
            "devtools_2024": [
                "GitHub", "GitLab", "Bitbucket", "SourceForge", "CodeCommit",
                "Vercel", "Netlify", "Heroku", "Railway", "Render", "Fly.io",
                "Supabase", "Firebase", "PlanetScale", "Neon", "Xata", "Upstash",
                "Linear", "Height", "Asana", "Monday.com", "ClickUp", "Notion",
                "Figma", "Sketch", "Adobe XD", "InVision", "Framer", "Principle",
                "Cursor", "Replit", "CodeSandbox", "Glitch", "Observable", "RunKit"
            ],
            
            # Productivity & Collaboration
            "productivity_2024": [
                "Notion", "Obsidian", "Roam Research", "LogSeq", "RemNote", "Craft",
                "Bear", "Ulysses", "iA Writer", "Typora", "Mark Text", "Zettlr",
                "Slack", "Microsoft Teams", "Discord", "Zoom", "Google Meet", "Webex",
                "Loom", "Mmhmm", "Around", "Whereby", "Jitsi", "BigBlueButton",
                "Calendly", "Acuity Scheduling", "YouCanBookMe", "ScheduleOnce", "Doodle",
                "Typeform", "Jotform", "Google Forms", "Microsoft Forms", "Paperform"
            ],
            
            # Food Delivery & Quick Commerce
            "food_delivery_2024": [
                "DoorDash", "Uber Eats", "Grubhub", "Postmates", "Caviar",
                "Gopuff", "Getir", "Gorillas", "Flink", "Jiffy", "Jokr",
                "Instacart", "Shipt", "Amazon Fresh", "Whole Foods", "Target+",
                "Zomato", "Swiggy", "Dunzo", "BigBasket", "Grofers", "Blinkit",
                "Deliveroo", "Just Eat", "Takeaway.com", "Glovo", "Wolt",
                "iFood", "Rappi", "PedidosYa", "Cornershop", "Mercado Envios"
            ],
            
            # Remote Work & Digital Nomad Tools
            "remote_work_2024": [
                "Zoom", "Google Meet", "Microsoft Teams", "Webex", "GoToMeeting",
                "Slack", "Discord", "Telegram", "WhatsApp Business", "Signal",
                "Notion", "Airtable", "Monday.com", "Asana", "Trello", "ClickUp",
                "Miro", "Mural", "Figma", "FigJam", "Conceptboard", "Lucidchart",
                "Time Doctor", "RescueTime", "Toggl", "Clockify", "Harvest",
                "Nomad List", "Remote Year", "WiFi Tribe", "Outsite", "Selina"
            ]
        }
    
    def load_progress(self):
        """Load previously downloaded companies"""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r') as f:
                    data = json.load(f)
                    return data.get('downloaded_companies', [])
            except:
                return []
        return []
    
    def save_progress(self):
        """Save current progress"""
        progress_data = {
            'downloaded_companies': self.downloaded_companies,
            'downloaded_count': self.downloaded_count,
            'failed_count': self.failed_count,
            'last_update': datetime.now().isoformat()
        }
        with open(self.progress_file, 'w') as f:
            json.dump(progress_data, f, indent=2)
    
    def clean_filename(self, name):
        """Clean filename for safe file system storage"""
        # Replace problematic characters
        replacements = {
            '&': '_and_',
            '+': '_plus_',
            '/': '_',
            '\\': '_',
            ':': '_',
            '*': '_',
            '?': '_',
            '"': '_',
            '<': '_',
            '>': '_',
            '|': '_',
            ' ': '_',
            '.': '_',
            "'": '_',
            ',': '_',
            '(': '_',
            ')': '_',
            '[': '_',
            ']': '_',
            '{': '_',
            '}': '_'
        }
        
        cleaned = name
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        # Remove multiple underscores
        while '__' in cleaned:
            cleaned = cleaned.replace('__', '_')
        
        # Remove leading/trailing underscores
        cleaned = cleaned.strip('_')
        
        return cleaned
    
    def get_company_logo_url(self, company_name):
        """Get company logo URL using various methods"""
        # Method 1: Try Logo.dev API
        try:
            logo_dev_url = f"https://img.logo.dev/{company_name.lower().replace(' ', '')}.com?token=pk_X1ripnHDSdWEpYRKWjWUVQ&format=png&size=200"
            response = requests.head(logo_dev_url, timeout=10)
            if response.status_code == 200:
                return logo_dev_url
        except:
            pass
        
        # Method 2: Try Clearbit Logo API
        try:
            domain_variations = [
                f"{company_name.lower().replace(' ', '')}.com",
                f"{company_name.lower().replace(' ', '')}.io",
                f"{company_name.lower().replace(' ', '')}.co",
                f"{company_name.lower().replace(' ', '').replace('.', '')}.com",
                f"{company_name.lower().replace(' ', '')}.ai",
                f"{company_name.lower().replace(' ', '')}.app"
            ]
            
            for domain in domain_variations:
                clearbit_url = f"https://logo.clearbit.com/{domain}?size=200&format=png"
                response = requests.head(clearbit_url, timeout=10)
                if response.status_code == 200:
                    return clearbit_url
        except:
            pass
        
        return None
    
    def download_logo(self, company_name, logo_url):
        """Download a single logo"""
        try:
            if company_name in self.downloaded_companies:
                logger.info(f"⏭️ Skipping {company_name} (already downloaded)")
                return True
            
            clean_name = self.clean_filename(company_name)
            file_path = os.path.join(self.download_dir, f"{clean_name}.png")
            
            if os.path.exists(file_path):
                logger.info(f"⏭️ Skipping {company_name} (file exists)")
                with self.lock:
                    self.downloaded_companies.append(company_name)
                return True
            
            # Add random delay
            time.sleep(random.uniform(1, 3))
            
            response = requests.get(logo_url, timeout=15, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            })
            
            if response.status_code == 200 and len(response.content) > 100:
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                
                with self.lock:
                    self.downloaded_count += 1
                    self.downloaded_companies.append(company_name)
                
                logger.info(f"✅ Downloaded {company_name} ({self.downloaded_count} total)")
                return True
            else:
                with self.lock:
                    self.failed_count += 1
                logger.warning(f"❌ Failed to download {company_name}: Invalid response")
                return False
                
        except Exception as e:
            with self.lock:
                self.failed_count += 1
            logger.error(f"❌ Error downloading {company_name}: {str(e)}")
            return False
    
    def process_company(self, company_name):
        """Process a single company - find and download logo"""
        try:
            logo_url = self.get_company_logo_url(company_name)
            
            if logo_url:
                return self.download_logo(company_name, logo_url)
            else:
                with self.lock:
                    self.failed_count += 1
                logger.warning(f"❌ No logo URL found for {company_name}")
                return False
                
        except Exception as e:
            with self.lock:
                self.failed_count += 1
            logger.error(f"❌ Error processing {company_name}: {str(e)}")
            return False
    
    def download_all_logos(self, max_workers=10):
        """Download all logos from the newsworthy companies database"""
        all_companies = []
        
        # Collect all companies from all categories
        for category_name, companies in self.newsworthy_companies.items():
            logger.info(f"Processing {category_name}: {len(companies)} companies")
            all_companies.extend(companies)
        
        # Remove duplicates while preserving order
        unique_companies = []
        seen = set()
        for company in all_companies:
            if company not in seen:
                unique_companies.append(company)
                seen.add(company)
        
        logger.info(f"📊 Total unique companies to process: {len(unique_companies)}")
        logger.info(f"📊 Already downloaded: {len(self.downloaded_companies)}")
        
        # Filter out already downloaded
        companies_to_process = [c for c in unique_companies if c not in self.downloaded_companies]
        logger.info(f"📊 Companies remaining to download: {len(companies_to_process)}")
        
        if not companies_to_process:
            logger.info("🎉 All companies already downloaded!")
            return
        
        # Download with threading
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_company = {
                executor.submit(self.process_company, company): company 
                for company in companies_to_process
            }
            
            for i, future in enumerate(as_completed(future_to_company)):
                company = future_to_company[future]
                try:
                    result = future.result()
                    
                    # Save progress every 10 downloads
                    if i % 10 == 0:
                        self.save_progress()
                    
                    if i % 50 == 0:
                        logger.info(f"📊 Progress: {i}/{len(companies_to_process)} processed, {self.downloaded_count} successful, {self.failed_count} failed")
                        
                except Exception as exc:
                    logger.error(f"Company {company} generated an exception: {exc}")
        
        # Final save
        self.save_progress()
        
        # Summary
        logger.info("="*50)
        logger.info("🎯 FINAL SUMMARY")
        logger.info("="*50)
        logger.info(f"✅ Successfully downloaded: {self.downloaded_count}")
        logger.info(f"❌ Failed: {self.failed_count}")
        logger.info(f"📁 Logos saved in: {self.download_dir}")
        
        # Save detailed results
        results = {
            'total_processed': len(companies_to_process),
            'successful_downloads': self.downloaded_count,
            'failed_downloads': self.failed_count,
            'download_directory': self.download_dir,
            'categories_processed': list(self.newsworthy_companies.keys()),
            'completion_time': datetime.now().isoformat()
        }
        
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)

def main():
    downloader = Newsworthy2024Downloader()
    downloader.download_all_logos(max_workers=15)

if __name__ == "__main__":
    main()