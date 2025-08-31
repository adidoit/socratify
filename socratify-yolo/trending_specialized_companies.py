#!/usr/bin/env python3
"""
Trending & Specialized Companies Logo Downloader
Focus on specialized sectors and trending companies from specific industries
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

class TrendingSpecializedDownloader:
    def __init__(self, download_dir="trending_specialized_companies"):
        self.download_dir = download_dir
        self.downloaded_count = 0
        self.failed_count = 0
        self.lock = threading.Lock()
        self.progress_file = "trending_specialized_progress.json"
        self.results_file = "trending_specialized_results.json"
        
        # Ensure download directory exists
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Load progress if exists
        self.downloaded_companies = self.load_progress()
        
        # Trending and specialized companies database
        self.specialized_companies = {
            # B2B SaaS & Enterprise Software
            "b2b_enterprise": [
                "Monday.com", "ClickUp", "Linear", "Height", "Coda", "Roam Research",
                "Obsidian", "LogSeq", "RemNote", "Craft", "Bear", "Ulysses",
                "Segment", "Mixpanel", "Amplitude", "FullStory", "Hotjar", "LogRocket",
                "Intercom", "Crisp", "Drift", "Zendesk", "Freshworks", "HubSpot",
                "Salesforce", "Pipedrive", "Close", "Copper", "Airtable", "Notion"
            ],
            
            # Cybersecurity & Data Protection
            "cybersecurity": [
                "CrowdStrike", "SentinelOne", "Okta", "Auth0", "1Password", "Bitwarden",
                "LastPass", "Dashlane", "NordPass", "Keeper Security", "RoboForm", "LogMeOnce",
                "Palo Alto Networks", "Fortinet", "Check Point", "FireEye", "Symantec", "McAfee",
                "Trend Micro", "Kaspersky", "Bitdefender", "ESET", "Avast", "AVG",
                "Malwarebytes", "Norton", "Webroot", "F-Secure", "G DATA", "Sophos"
            ],
            
            # DevOps & Cloud Infrastructure
            "devops_cloud": [
                "HashiCorp", "DataDog", "New Relic", "Splunk", "Elastic", "MongoDB",
                "Redis", "InfluxDB", "TimescaleDB", "CockroachDB", "PlanetScale", "Xata",
                "Supabase", "Firebase", "AWS", "Google Cloud", "Microsoft Azure", "DigitalOcean",
                "Linode", "Vultr", "Hetzner", "OVH", "Scaleway", "UpCloud",
                "Railway", "Render", "Fly.io", "Heroku", "Vercel", "Netlify"
            ],
            
            # Design & Creative Tools
            "design_creative": [
                "Figma", "Sketch", "Adobe XD", "InVision", "Framer", "Principle",
                "ProtoPie", "Marvel", "Zeplin", "Abstract", "Avocode", "Sympli",
                "Canva", "Piktochart", "Venngage", "Crello", "DesignBold", "Adobe Creative Cloud",
                "Affinity", "CorelDRAW", "PaintShop Pro", "GIMP", "Inkscape", "Blender",
                "Cinema 4D", "Maya", "3ds Max", "ZBrush", "Substance", "Houdini"
            ],
            
            # No-Code & Low-Code Platforms
            "nocode_lowcode": [
                "Webflow", "Bubble", "Adalo", "Glide", "AppGyver", "OutSystems",
                "Mendix", "Appian", "Salesforce Platform", "Microsoft Power Platform", "Google AppSheet", "Airtable",
                "Zapier", "Integromat", "Microsoft Power Automate", "IFTTT", "Workato", "Tray.io",
                "Retool", "Tooljet", "Appsmith", "Budibase", "UI Bakery", "DronaHQ",
                "FlutterFlow", "Draftbit", "BuildFire", "Appy Pie", "AppMachine", "GoodBarber"
            ],
            
            # Data & Analytics Platforms
            "data_analytics": [
                "Snowflake", "Databricks", "Palantir", "Tableau", "Power BI", "Looker",
                "Qlik", "Sisense", "ThoughtSpot", "Domo", "Chartio", "Periscope Data",
                "Mode Analytics", "Metabase", "Apache Superset", "Grafana", "Observable", "Plotly",
                "Jupyter", "RStudio", "Anaconda", "H2O.ai", "DataRobot", "MLflow",
                "Weights & Biases", "Neptune.ai", "Comet.ml", "Domino Data Lab", "Algorithmia", "Seldon"
            ],
            
            # Customer Success & Support
            "customer_success": [
                "Gainsight", "ChurnZero", "Totango", "ClientSuccess", "UserIQ", "Planhat",
                "Vitally", "Catalyst", "SmartKarrot", "CustomerGauge", "Medallia", "Qualtrics",
                "SurveyMonkey", "Typeform", "JotForm", "Google Forms", "Microsoft Forms", "Paperform",
                "Help Scout", "Front", "Groove", "Kayako", "LiveAgent", "Freshdesk",
                "Zoho Desk", "ServiceNow", "Jira Service Management", "Remedy", "Cherwell", "ManageEngine"
            ],
            
            # Sales & Marketing Automation
            "sales_marketing": [
                "HubSpot", "Marketo", "Pardot", "Eloqua", "Act-On", "SharpSpring",
                "Mailchimp", "Constant Contact", "Campaign Monitor", "AWeber", "GetResponse", "ConvertKit",
                "ActiveCampaign", "Drip", "Klaviyo", "Omnisend", "SendinBlue", "Mailjet",
                "Outreach", "SalesLoft", "Apollo", "ZoomInfo", "LinkedIn Sales Navigator", "Lusha",
                "Clearbit", "FullContact", "Hunter.io", "FindThatLead", "Voila Norbert", "Snov.io"
            ],
            
            # Real Estate Technology
            "proptech_extended": [
                "Zillow", "Redfin", "Compass", "Opendoor", "OfferPad", "RedfinNow",
                "Knock", "Flyhomes", "Accept.inc", "Ribbon Home", "Better.com", "Rocket Mortgage",
                "Quicken Loans", "LoanDepot", "CrossCountry Mortgage", "Guild Mortgage", "Movement Mortgage", "AmeriSave",
                "DocuSign", "PandaDoc", "HelloSign", "Adobe Sign", "SignRequest", "eversign",
                "Matterport", "Asteroom", "Cupix", "InsideMaps", "Immoviewer", "YouVisit"
            ],
            
            # Financial Services & Payments
            "finserv_payments": [
                "Stripe", "Square", "PayPal", "Adyen", "Worldpay", "Authorize.Net",
                "Braintree", "2Checkout", "Razorpay", "Payu", "Mollie", "Checkout.com",
                "Klarna", "Afterpay", "Affirm", "Zip", "Sezzle", "Quadpay",
                "Plaid", "Yodlee", "MX", "Finicity", "Akoya", "TrueLayer",
                "Coinbase", "Binance", "Kraken", "Gemini", "FTX", "Crypto.com",
                "Circle", "Ripple", "Chainlink", "Uniswap", "Aave", "Compound"
            ],
            
            # Health & Wellness Technology
            "healthtech_extended": [
                "Peloton", "Mirror", "Tonal", "Hydrow", "NordicTrack", "Bowflex",
                "MyFitnessPal", "Strava", "Garmin Connect", "Fitbit", "Apple Health", "Samsung Health",
                "Calm", "Headspace", "Ten Percent Happier", "Insight Timer", "Waking Up", "Simple Habit",
                "WHOOP", "Oura", "Withings", "Polar", "Suunto", "Coros",
                "23andMe", "AncestryDNA", "MyHeritage DNA", "FamilyTreeDNA", "Living DNA", "Nebula Genomics"
            ],
            
            # Media & Content Platforms
            "media_content": [
                "Substack", "Medium", "Ghost", "WordPress.com", "Squarespace", "Wix",
                "Webflow", "Framer", "Carrd", "Linktree", "Beacons.ai", "Milkshake",
                "Patreon", "Ko-fi", "Buy Me a Coffee", "Gumroad", "Teachable", "Thinkific",
                "Circle", "Discord", "Slack", "Telegram", "WhatsApp Business", "Signal",
                "Clubhouse", "Twitter Spaces", "LinkedIn Live", "Facebook Live", "YouTube Live", "Twitch"
            ],
            
            # E-learning & Skills Development
            "elearning_skills": [
                "Coursera", "Udemy", "edX", "Khan Academy", "MasterClass", "Skillshare",
                "Pluralsight", "LinkedIn Learning", "Udacity", "Codecademy", "DataCamp", "Treehouse",
                "FreeCodeCamp", "The Odin Project", "Lambda School", "General Assembly", "Flatiron School", "Springboard",
                "Thinkful", "Bloc", "Ironhack", "Le Wagon", "42 School", "Holberton School",
                "App Academy", "Hack Reactor", "DevMountain", "Tech Elevator", "Nashville Software School", "The Tech Academy"
            ],
            
            # Gaming & Entertainment
            "gaming_entertainment_extended": [
                "Roblox", "Minecraft", "Fortnite", "Among Us", "Fall Guys", "Valheim",
                "Steam", "Epic Games Store", "GOG", "Origin", "Uplay", "Battle.net",
                "Xbox Game Pass", "PlayStation Now", "Google Stadia", "NVIDIA GeForce Now", "Amazon Luna", "Shadow",
                "Twitch", "YouTube Gaming", "Facebook Gaming", "Mixer", "DLive", "Trovo",
                "Discord", "TeamSpeak", "Mumble", "Ventrilo", "Curse Voice", "RaidCall"
            ],
            
            # Emerging Technologies
            "emerging_tech": [
                "Neuralink", "Magic Leap", "Microsoft HoloLens", "Apple Vision Pro", "Meta Quest", "PICO",
                "OpenAI", "Anthropic", "Cohere", "AI21 Labs", "Hugging Face", "Scale AI",
                "DataRobot", "H2O.ai", "Databricks", "C3.ai", "Palantir", "Snowflake",
                "Unity", "Unreal Engine", "Godot", "GameMaker Studio", "Construct", "RPG Maker",
                "Tesla", "SpaceX", "Blue Origin", "Virgin Galactic", "Rocket Lab", "Relativity Space"
            ],
            
            # Sustainability & Clean Tech
            "cleantech_sustainability": [
                "Tesla", "Rivian", "Lucid Motors", "NIO", "XPeng", "Li Auto",
                "ChargePoint", "EVgo", "Electrify America", "Volta Charging", "Blink Charging", "Wallbox",
                "Sunrun", "Sunnova", "Vivint Solar", "SunPower", "First Solar", "Canadian Solar",
                "Vestas", "Siemens Gamesa", "GE Renewable Energy", "Ørsted", "NextEra Energy", "Enel",
                "Beyond Meat", "Impossible Foods", "Oatly", "Perfect Day", "Just Egg", "Memphis Meats",
                "Climeworks", "Carbon Engineering", "Global Thermostat", "Carbfix", "Running Tide", "Charm Industrial"
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
                f"{company_name.lower().replace(' ', '')}.ai",
                f"{company_name.lower().replace(' ', '')}.app",
                f"{company_name.lower().replace(' ', '').replace('.', '')}.com",
                f"{company_name.lower().replace(' ', '')}.tech",
                f"{company_name.lower().replace(' ', '')}.dev"
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
        """Download all logos from the specialized companies database"""
        all_companies = []
        
        # Collect all companies from all categories
        for category_name, companies in self.specialized_companies.items():
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

def main():
    downloader = TrendingSpecializedDownloader()
    downloader.download_all_logos(max_workers=15)

if __name__ == "__main__":
    main()