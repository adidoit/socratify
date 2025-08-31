#!/usr/bin/env python3
"""
Comprehensive Sector-Specific Companies Logo Downloader
Focus on Media & Entertainment, Food Tech, PropTech, EdTech, HR Tech, InsurTech, LegalTech, Supply Chain, and Travel Tech
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

class SectorSpecificCompaniesDownloader:
    def __init__(self, download_dir="sector_specific_companies"):
        self.download_dir = download_dir
        self.downloaded_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.progress_file = "sector_specific_progress.json"
        self.results_file = "sector_specific_results.json"
        
        # Ensure download directory exists
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Load progress if exists
        self.downloaded_companies = self.load_progress()
        
        # Comprehensive sector-specific companies database
        self.sector_companies = {
            # Media & Entertainment Companies
            "media_entertainment": {
                "streaming_services": [
                    "Viu", "Hotstar", "Zee5", "SonyLiv", "Voot", "MX Player",
                    "ALTBalaji", "Eros Now", "Sun NXT", "Hoichoi", "Addatimes",
                    "Lionsgate Play", "Apple TV+", "Peacock", "Paramount+", "HBO Max",
                    "Discovery+", "Crunchyroll", "Funimation", "VRV", "Tubi",
                    "Pluto TV", "Roku Channel", "IMDb TV", "Vudu", "Crackle",
                    "iQiyi", "Youku", "Bilibili", "Tencent Video", "Mango TV",
                    "KOCOWA", "Viki", "AsianCrush", "Hi-YAH!", "Dekkoo"
                ],
                "gaming_studios": [
                    "Epic Games", "Riot Games", "Valve", "Blizzard Entertainment",
                    "Activision", "Electronic Arts", "Ubisoft", "Take-Two Interactive",
                    "Rockstar Games", "2K Games", "Square Enix", "Capcom",
                    "Konami", "Bandai Namco", "Sega", "Nintendo", "Sony Interactive",
                    "Supercell", "King Digital", "Zynga", "Rovio", "Gameloft",
                    "Glu Mobile", "Machine Zone", "Playrix", "Moon Active",
                    "Peak Games", "Voodoo", "Hyper Casual Games", "PlatinumGames",
                    "FromSoftware", "CD Projekt", "Naughty Dog", "Santa Monica Studio"
                ],
                "podcast_networks": [
                    "Spotify Podcasts", "Anchor", "Gimlet Media", "The Ringer",
                    "Parcast", "Wondery", "Midroll Media", "Podcast One",
                    "Earwolf", "Maximum Fun", "Radiotopia", "NPR", "BBC Sounds",
                    "iHeartRadio", "Stitcher", "Luminary", "Himalaya", "Castbox",
                    "Pocket Casts", "Overcast", "Castro", "Breaker", "Podchaser"
                ],
                "newsletter_media": [
                    "Morning Brew", "The Hustle", "Axios", "Punchbowl News",
                    "The Information", "Stratechery", "Benedict Evans", "Not Boring",
                    "Lenny's Newsletter", "The Diff", "Platformer", "Casey Newton",
                    "Matt Levine", "Heather Cox Richardson", "Sinocism", "China Law Blog",
                    "The Margins", "Technically", "The Download", "AI News"
                ],
                "creator_tools": [
                    "Patreon", "Substack", "ConvertKit", "Mailchimp", "Ghost",
                    "Beehiiv", "Revue", "Buttondown", "Curated", "Newsletter Glue",
                    "Gumroad", "Teachable", "Thinkific", "Kajabi", "Podia",
                    "Circle", "Mighty Networks", "Skool", "School", "Heartbeat"
                ]
            },
            
            # Food Tech & AgTech
            "foodtech_agtech": {
                "alternative_proteins": [
                    "Beyond Meat", "Impossible Foods", "Oatly", "Just Egg",
                    "Perfect Day", "Upside Foods", "Eat Just", "Memphis Meats",
                    "Wild Type", "BlueNalu", "Finless Foods", "New Wave Foods",
                    "Ocean Hugger Foods", "Good Catch", "Alpha Foods", "Lightlife",
                    "Gardein", "Morningstar Farms", "Boca", "Quorn", "Field Roast",
                    "Tofurky", "Daiya", "Follow Your Heart", "So Delicious", "Silk"
                ],
                "vertical_farming": [
                    "AeroFarms", "Plenty", "Bowery Farming", "Gotham Greens",
                    "BrightFarms", "AppHarvest", "Iron Ox", "Freight Farms",
                    "Square Roots", "Vertical Harvest", "Green Sense Farms",
                    "CropOne", "Caliber Biotherapeutics", "Infarm", "Plantagon",
                    "Sky Greens", "Spread", "Mirai", "Panasonic", "Signify"
                ],
                "food_delivery": [
                    "Gopuff", "Getir", "Gorillas", "Flink", "Jiffy", "Jokr",
                    "1520", "Buyk", "Yango Deli", "Glovo", "Deliveroo", "Just Eat",
                    "Takeaway.com", "Delivery Hero", "Foodpanda", "Wolt", "Bolt Food",
                    "Rappi", "iFood", "Cornershop", "Postmates", "Caviar"
                ],
                "restaurant_tech": [
                    "Toast", "Square for Restaurants", "Resy", "OpenTable",
                    "Yelp Reservations", "Tock", "TouchBistro", "Lightspeed",
                    "NCR Aloha", "Oracle Micros", "Clover", "Shopify POS",
                    "Upserve", "Breadcrumb", "Cake", "ShiftPlanning", "7shifts",
                    "When I Work", "Deputy", "Homebase", "TSheets", "Clockwise"
                ],
                "agricultural_robotics": [
                    "John Deere", "CNH Industrial", "AGCO", "Kubota", "Mahindra",
                    "Blue River Technology", "Abundant Robotics", "Harvest CROO",
                    "Root AI", "Soft Robotics", "Iron Ox", "FarmWise", "ecoRobotix",
                    "Naïo Technologies", "Naio Technologies", "Small Robot Company",
                    "SwarmFarm", "Fendt", "Claas", "Lemken"
                ]
            },
            
            # PropTech & Construction Tech
            "proptech_construction": {
                "real_estate_platforms": [
                    "Compass", "Redfin", "Zillow", "Opendoor", "OfferPad",
                    "Knock", "Flyhomes", "Ribbon Home", "Accept.inc", "Better.com",
                    "Rocket Mortgage", "LoanDepot", "Movement Mortgage", "CrossCountry",
                    "Guild Mortgage", "Finance of America", "AmeriSave", "NewRez",
                    "PennyMac", "Caliber Home Loans", "Mr. Cooper", "Servicing"
                ],
                "construction_management": [
                    "Procore", "PlanGrid", "Autodesk Construction Cloud", "Fieldwire",
                    "BuilderTrend", "CoConstruct", "Buildertrend", "JobNimbus",
                    "CompanyCam", "Raken", "Fieldlens", "FINALCAD", "iFieldSmart",
                    "e-Builder", "Aconex", "4Projects", "BuildingConnected", "Levelset",
                    "Contractor Foreman", "RedTeam", "Sage Construction", "Viewpoint"
                ],
                "smart_buildings": [
                    "View", "Matterport", "JLL Technologies", "WeWork", "Katerra",
                    "Fifth Wall", "MetaProp", "Camber Creek", "Moderne Ventures",
                    "Second Century Ventures", "Navitas Capital", "RET Ventures",
                    "Pi Labs", "Taronga Ventures", "Zico Ventures", "Urban Us"
                ],
                "property_management": [
                    "AppFolio", "Buildium", "Yardi", "RealPage", "Rent Manager",
                    "Property Boulevard", "TenantCloud", "Cozy", "Rentberry",
                    "SparkRental", "DoorLoop", "Hemlane", "RentSpree", "Zego",
                    "SimplifyEm", "Rental Tools", "Property Matrix", "Innago"
                ]
            },
            
            # EdTech Companies
            "edtech": {
                "online_learning": [
                    "Coursera", "Udemy", "edX", "Khan Academy", "MasterClass",
                    "Skillshare", "Pluralsight", "LinkedIn Learning", "Udacity",
                    "Codecademy", "DataCamp", "Treehouse", "FreeCodeCamp", "The Odin Project",
                    "Lambda School", "General Assembly", "Flatiron School", "Springboard",
                    "Thinkful", "Bloc", "Ironhack", "Le Wagon", "42 School"
                ],
                "corporate_training": [
                    "Cornerstone OnDemand", "Docebo", "TalentLMS", "LearnUpon",
                    "Absorb LMS", "Bridge", "Litmos", "iSpring", "Adobe Captivate Prime",
                    "Blackboard Learn", "Canvas", "Moodle", "D2L Brightspace",
                    "Schoology", "Google Classroom", "Microsoft Teams for Education",
                    "Zoom for Education", "Webex Education", "GoToTraining"
                ],
                "language_learning": [
                    "Duolingo", "Babbel", "Rosetta Stone", "Memrise", "Busuu",
                    "HelloTalk", "Tandem", "italki", "Preply", "Cambly",
                    "Lingoda", "FluentU", "Yabla", "LingQ", "Anki",
                    "Quizlet", "StudyBlue", "Flashcard Machine", "Cram.com"
                ],
                "skill_development": [
                    "Coursera for Business", "Udemy for Business", "LinkedIn Learning",
                    "Pluralsight", "O'Reilly Learning", "Safari Books Online",
                    "A Cloud Guru", "Linux Academy", "Cloud Academy", "Whizlabs",
                    "ExamPro", "Tutorial Dojo", "Mapt", "PacktPub", "Manning"
                ]
            },
            
            # HR Tech & Future of Work
            "hrtech_futureofwork": {
                "remote_work_tools": [
                    "Slack", "Microsoft Teams", "Discord", "Zoom", "Google Meet",
                    "WebEx", "GoToMeeting", "BlueJeans", "Whereby", "Around",
                    "Mmhmm", "Loom", "Notion", "Airtable", "Monday.com",
                    "Asana", "Trello", "ClickUp", "Linear", "Height",
                    "Coda", "Roam Research", "Obsidian", "Logseq", "RemNote"
                ],
                "recruitment_platforms": [
                    "Workday", "BambooHR", "Greenhouse", "Lever", "Jobvite",
                    "SmartRecruiters", "iCIMS", "Workable", "JazzHR", "Breezy HR",
                    "Zoho Recruit", "Recruiterbox", "Newton", "Freshteam", "Personio",
                    "Namely", "Gusto", "Rippling", "Justworks", "TriNet"
                ],
                "employee_engagement": [
                    "Culture Amp", "Glint", "TINYpulse", "15Five", "Officevibe",
                    "Bonusly", "Kudos", "Achievers", "Reward Gateway", "Motivosity",
                    "Blueboard", "Nectar", "Assembly", "Fond", "Bucketlist",
                    "Snappy Gifts", "Cooleaf", "Workstars", "YouEarnedIt", "Globoforce"
                ],
                "payroll_benefits": [
                    "ADP", "Paychex", "Paycom", "Paylocity", "Ultimate Software",
                    "Ceridian", "Workday HCM", "SuccessFactors", "Oracle HCM",
                    "Kronos", "Deputy", "When I Work", "TSheets", "TimeClock Plus",
                    "BambooHR", "Namely", "Zenefits", "Gusto", "Justworks"
                ]
            },
            
            # InsurTech & LegalTech
            "insurtech_legaltech": {
                "digital_insurance": [
                    "Lemonade", "Root", "Metromile", "Next Insurance", "Pie Insurance",
                    "Steady", "Haven Life", "Ladder", "Ethos", "Bestow",
                    "Fabric", "Quotacy", "PolicyGenius", "Coverwallet", "Simply Business",
                    "Zego", "Cuvva", "By Miles", "Trov", "Slice Labs",
                    "Oscar Health", "Bright Health", "Clover Health", "Devoted Health", "Alignment Healthcare"
                ],
                "legal_automation": [
                    "LegalZoom", "Rocket Lawyer", "Nolo", "UpCounsel", "Avvo",
                    "Justia", "FindLaw", "Martindale-Hubbell", "Super Lawyers", "Best Lawyers",
                    "Clio", "MyCase", "PracticePanther", "LawPay", "TimeSolv",
                    "CosmoLex", "Smokeball", "Actionstep", "LexisNexis", "Westlaw"
                ],
                "contract_management": [
                    "DocuSign", "PandaDoc", "HelloSign", "Adobe Sign", "SignRequest",
                    "eversign", "SignNow", "RightSignature", "SignEasy", "Docusaurus",
                    "Ironclad", "ContractWorks", "Concord", "Agiloft", "ContractPodAI",
                    "Outlaw", "SpringCM", "Apttus", "Icertis", "Zycus"
                ],
                "compliance_software": [
                    "Thomson Reuters", "Wolters Kluwer", "Compliance.ai", "RegTech Solutions",
                    "NICE Actimize", "SAS", "IBM OpenPages", "MetricStream", "ServiceNow GRC",
                    "Resolver", "LogicGate", "Workiva", "Reciprocity", "OneTrust",
                    "TrustArc", "DataGuidance", "Privacyera", "BigID", "Varonis"
                ]
            },
            
            # Supply Chain & Manufacturing
            "supply_chain_manufacturing": {
                "industrial_iot": [
                    "GE Digital", "Siemens", "Schneider Electric", "ABB", "Honeywell",
                    "Emerson", "Rockwell Automation", "Yokogawa", "Omron", "Mitsubishi Electric",
                    "Fanuc", "KUKA", "Universal Robots", "Cognex", "Keyence",
                    "Sick", "Banner Engineering", "Pepperl+Fuchs", "Turck", "IFM"
                ],
                "warehouse_automation": [
                    "Amazon Robotics", "Fetch Robotics", "GreyOrange", "Locus Robotics",
                    "6 River Systems", "Geek+", "IAM Robotics", "inVia Robotics",
                    "Magazino", "Vecna Robotics", "Mobile Industrial Robots", "AutoStore",
                    "Dematic", "Swisslog", "Vanderlande", "Daifuku", "Honeywell Intelligrated"
                ],
                "last_mile_delivery": [
                    "Nuro", "Starship Technologies", "Marble", "Dispatch", "Kiwi",
                    "Robby Technologies", "Savioke", "TeleRetail", "BoxBot", "Postmates X",
                    "Amazon Scout", "FedEx SameDay Bot", "Kiwibot", "Serve Robotics", "Coco"
                ],
                "manufacturing_software": [
                    "Autodesk", "SolidWorks", "PTC", "Siemens PLM", "Dassault Systemes",
                    "Ansys", "Altair", "MSC Software", "COMSOL", "MATLAB",
                    "LabVIEW", "Wonderware", "Ignition", "GE iFIX", "Rockwell FactoryTalk"
                ]
            },
            
            # Travel & Hospitality Tech
            "travel_hospitality": {
                "alternative_accommodation": [
                    "Airbnb", "Vrbo", "HomeAway", "RedAwning", "FlipKey",
                    "Vacasa", "AvantStay", "Sonder", "Lyric", "Domio",
                    "WhyHotel", "Blueground", "Stay Alfred", "Corporate Housing by Oakwood", "BridgeStreet"
                ],
                "travel_planning": [
                    "TripAdvisor", "Expedia", "Booking.com", "Kayak", "Priceline",
                    "Skyscanner", "Momondo", "Google Travel", "Hopper", "Scott's Cheap Flights",
                    "The Flight Deal", "Secret Flying", "Airfarewatchdog", "FareCompare", "CheapOair"
                ],
                "experience_booking": [
                    "Viator", "GetYourGuide", "Klook", "Musement", "Tiqets",
                    "Peek", "Bokun", "FareHarbor", "Rezdy", "Checkfront",
                    "Regiondo", "Ventrata", "Palisis", "Orioly", "Xola"
                ],
                "business_travel": [
                    "Concur", "Expensify", "Ramp", "Brex", "Divvy",
                    "Airbase", "Coupa", "Chrome River", "Certify", "Zoho Expense",
                    "Receipt Bank", "Shoeboxed", "Wave Accounting", "FreshBooks", "QuickBooks"
                ]
            }
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
                f"{company_name.lower().replace(' ', '').replace('.', '')}.com"
            ]
            
            for domain in domain_variations:
                clearbit_url = f"https://logo.clearbit.com/{domain}?size=200&format=png"
                response = requests.head(clearbit_url, timeout=10)
                if response.status_code == 200:
                    return clearbit_url
        except:
            pass
        
        # Method 3: Try direct domain favicon
        try:
            domain_variations = [
                f"{company_name.lower().replace(' ', '')}.com",
                f"{company_name.lower().replace(' ', '')}.io"
            ]
            
            for domain in domain_variations:
                favicon_url = f"https://{domain}/favicon.ico"
                response = requests.head(f"https://{domain}", timeout=10)
                if response.status_code == 200:
                    return favicon_url
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
        """Download all logos from the sector companies database"""
        all_companies = []
        
        # Collect all companies from all sectors
        for sector_name, categories in self.sector_companies.items():
            logger.info(f"Processing {sector_name}...")
            for category_name, companies in categories.items():
                logger.info(f"  - {category_name}: {len(companies)} companies")
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
            'sectors_processed': list(self.sector_companies.keys()),
            'completion_time': datetime.now().isoformat()
        }
        
        with open(self.results_file, 'w') as f:
            json.dump(results, f, indent=2)

def main():
    downloader = SectorSpecificCompaniesDownloader()
    downloader.download_all_logos(max_workers=15)

if __name__ == "__main__":
    main()