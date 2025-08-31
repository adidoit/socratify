#!/usr/bin/env python3
"""
Regional Newsworthy Companies Logo Downloader
Focus on companies from specific regions that have been featured in tech news
Companies from Europe, Asia-Pacific, Latin America, Middle East, and Africa
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

class RegionalNewsworthyDownloader:
    def __init__(self, download_dir="regional_newsworthy_companies"):
        self.download_dir = download_dir
        self.downloaded_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.progress_file = "regional_newsworthy_progress.json"
        self.results_file = "regional_newsworthy_results.json"
        
        # Ensure download directory exists
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Load progress if exists
        self.downloaded_companies = self.load_progress()
        
        # Regional companies by geography that have been newsworthy
        self.regional_companies = {
            # European Unicorns & High-Growth Companies
            "europe": {
                "uk_ireland": [
                    "Revolut", "Monzo", "Starling Bank", "GoCardless", "TransferWise",
                    "Deliveroo", "Just Eat", "Zopa", "Funding Circle", "WorldRemit",
                    "Skyscanner", "FanDuel", "King Digital", "Mind Candy", "Improbable",
                    "DeepMind", "Swiftkey", "Shazam", "Hailo", "Citymapper",
                    "Photobox", "Zoopla", "Rightmove", "PureGym", "Gymshark"
                ],
                "germany_austria": [
                    "SAP", "Zalando", "Rocket Internet", "N26", "GetYourGuide",
                    "FlixBus", "AUTO1", "Delivery Hero", "HelloFresh", "Wirecard",
                    "SoundCloud", "ResearchGate", "6Wunderkinder", "EyeEm", "Readmill",
                    "Celonis", "UiPath", "Personio", "Mambu", "solarisBank",
                    "Trade Republic", "BITA", "Blinkist", "Contentful", "GoEuro"
                ],
                "france": [
                    "BlaBlaCar", "Criteo", "Deezer", "Dailymotion", "Viadeo",
                    "PriceMinister", "Showroomprive", "Sigfox", "Algolia", "Docker",
                    "Mirakl", "Talend", "Dataiku", "Shift Technology", "Ledger",
                    "Qonto", "Alan", "PayFit", "Front", "Aircall",
                    "Sendinblue", "Contentsquare", "Back Market", "ManoMano", "Veepee"
                ],
                "nordics": [
                    "Spotify", "Skype", "King", "Mojang", "iZettle", "Klarna",
                    "Unity Technologies", "Rovio", "Supercell", "Angry Birds",
                    "Wolt", "Sennheiser", "Tidal", "Opera", "NordicTrack",
                    "Kahoot", "AutoStore", "Schibsted", "Telenor", "Ericsson",
                    "Nokia", "Novo Nordisk", "IKEA", "H&M", "Maersk"
                ],
                "netherlands_belgium": [
                    "Booking.com", "TomTom", "Adyen", "Just Eat Takeaway", "Coolblue",
                    "bol.com", "Picnic", "Travix", "WeTransfer", "Layar",
                    "Catawiki", "Treatwell", "Collibra", "Materialise", "Option",
                    "Showpad", "Teamleader", "Procurios", "MessageBird", "Mollie"
                ],
                "spain_portugal": [
                    "Cabify", "Glovo", "Wallapop", "LetGo", "Red Points",
                    "Typeform", "TravelPerk", "Factorial", "Coverfy", "Jobandtalent",
                    "OutSystems", "Farfetch", "Talkdesk", "Feedzai", "Codacy",
                    "Unbabel", "Veniam", "Aptoide", "Mindera", "Critical Software"
                ],
                "italy_switzerland": [
                    "Bending Spoons", "Musixmatch", "Rocket Internet", "Prima Assicurazioni", "Scalapay",
                    "Credimi", "Satispay", "Casavo", "Tannico", "Depop",
                    "Logitech", "Mindmaze", "GetYourGuide", "Sportradar", "Avaloq",
                    "Temenos", "u-blox", "Sensirion", "VAT Group", "Bystronic"
                ]
            },
            
            # Asian Companies (excluding China/India which are covered elsewhere)
            "asia_pacific": {
                "southeast_asia": [
                    "Grab", "Gojek", "Sea Limited", "Shopee", "Lazada",
                    "Tokopedia", "Bukalapak", "Traveloka", "RedDoorz", "OYO",
                    "Foodpanda", "Zomato", "Swiggy", "PolicyBazaar", "Paytm",
                    "Ola", "Uber", "Careem", "Noon", "Souq"
                ],
                "japan": [
                    "SoftBank", "Rakuten", "LINE", "Mercari", "CyberAgent",
                    "DeNA", "Gree", "Mixi", "Cookpad", "Wantedly",
                    "SmartNews", "Freee", "Money Forward", "Sansan", "ChatWork",
                    "Crowdworks", "Lancers", "Base", "Stores", "Minne"
                ],
                "south_korea": [
                    "Kakao", "Naver", "Coupang", "Baemin", "Yanolja",
                    "Toss", "Viva Republica", "Woowa Brothers", "Market Kurly", "Kurly",
                    "Zigbang", "Carrot", "Danggeun Market", "Ridibooks", "Watcha"
                ],
                "australia_nz": [
                    "Atlassian", "Canva", "Afterpay", "SafetyCulture", "Campaign Monitor",
                    "99designs", "Freelancer", "BigCommerce", "WiseTech", "Tyro",
                    "Zip Co", "Sezzle", "Deputy", "Employment Hero", "Culture Amp",
                    "Xero", "TradeMe", "Pushpay", "Rocket Lab", "Vista Group"
                ]
            },
            
            # Latin American Companies
            "latin_america": {
                "brazil": [
                    "Nubank", "Stone", "PagSeguro", "iFood", "Magazine Luiza",
                    "Via Varejo", "B2W", "Mercado Libre", "GetNinjas", "Loggi",
                    "99", "Easy Taxi", "Cabify", "Rappi", "Cornershop",
                    "Loft", "QuintoAndar", "Creditas", "GuiaBolso", "Conta Azul"
                ],
                "argentina": [
                    "Mercado Libre", "Globant", "Auth0", "Satellogic", "Ualá",
                    "Increase", "Tienda Nube", "Properati", "OLX", "Navent",
                    "Despegar", "Almundo", "EducationUSA", "Workana", "Freelancer"
                ],
                "mexico": [
                    "Kavak", "Bitso", "Konfío", "Clip", "AlphaCredit",
                    "Kueski", "Clara", "Conekta", "OpenPay", "Credijusto",
                    "Cornershop", "Rappi", "Sin Delantal", "Jüsto", "Frubana"
                ],
                "colombia_chile": [
                    "Rappi", "Platzi", "Tpaga", "Chiper", "Mesfix",
                    "NotCo", "Fintonic", "Cornershop", "Yapo", "Chileautos",
                    "Falabella", "Ripley", "Paris", "La Polar", "Hites"
                ]
            },
            
            # Middle East & Africa
            "middle_east_africa": {
                "uae_saudi": [
                    "Careem", "Noon", "Souq", "Fetchr", "Talabat",
                    "Zomato", "Swiggy", "Dubizzle", "Bayut", "Property Finder",
                    "Hungerstation", "Jahez", "Mrsool", "Salla", "Moyasar"
                ],
                "egypt": [
                    "Fawry", "Paymob", "Vezeeta", "Swvl", "Yalla",
                    "Elmenus", "Otlob", "Jumia", "MaxAB", "MoneyFellows",
                    "Aman", "Halan", "Trella", "Breadfast", "Rabbit"
                ],
                "south_africa": [
                    "Naspers", "Takealot", "Mr D Food", "SnapScan", "Yoco",
                    "Luno", "OVEX", "Wonga", "African Bank", "Discovery",
                    "Momentum", "Sanlam", "Old Mutual", "Standard Bank", "FirstRand"
                ],
                "nigeria_kenya": [
                    "Jumia", "Konga", "Flutterwave", "Paystack", "Interswitch",
                    "Paga", "Opay", "PalmPay", "Carbon", "FairMoney",
                    "M-Pesa", "Safaricom", "Equity Bank", "KCB", "Tala",
                    "Branch", "BitPesa", "Cellulant", "iPay", "JamboPay"
                ]
            },
            
            # Canadian Companies
            "canada": [
                "Shopify", "Wealthsica", "Mogo", "Paymi", "Nuvei",
                "Coinsquare", "Bitbuy", "CoinSmart", "Wealthsimple", "Questrade",
                "FreshBooks", "Wave Accounting", "Hootsuite", "Later", "Buffer",
                "Slack", "Zoom", "BambooHR", "Deputy", "Workday"
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
        
        # Method 2: Try Clearbit Logo API with various domain extensions
        try:
            domain_variations = [
                f"{company_name.lower().replace(' ', '')}.com",
                f"{company_name.lower().replace(' ', '')}.io",
                f"{company_name.lower().replace(' ', '')}.co",
                f"{company_name.lower().replace(' ', '')}.co.uk",
                f"{company_name.lower().replace(' ', '')}.de",
                f"{company_name.lower().replace(' ', '')}.fr",
                f"{company_name.lower().replace(' ', '')}.nl",
                f"{company_name.lower().replace(' ', '')}.com.au",
                f"{company_name.lower().replace(' ', '')}.ca",
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
        """Download all logos from the regional companies database"""
        all_companies = []
        
        # Collect all companies from all regions
        for region_name, region_data in self.regional_companies.items():
            if isinstance(region_data, dict):
                # Nested structure (e.g., Europe with sub-regions)
                for sub_region, companies in region_data.items():
                    logger.info(f"Processing {region_name} - {sub_region}: {len(companies)} companies")
                    all_companies.extend(companies)
            else:
                # Flat structure (e.g., Canada)
                logger.info(f"Processing {region_name}: {len(region_data)} companies")
                all_companies.extend(region_data)
        
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

def main():
    downloader = RegionalNewsworthyDownloader()
    downloader.download_all_logos(max_workers=15)

if __name__ == "__main__":
    main()