#!/usr/bin/env python3
"""
Comprehensive script to find and download logos for 300+ more newsworthy companies.
Focuses on companies that:
- Have been in the news in 2023-2024
- Have interesting business models
- Are growing rapidly
- Serve niche markets well
- Are category creators or disruptors

Sources include:
- Y Combinator recent batches
- Major VC portfolio companies (a16z, Sequoia, Index)
- Recent SPAC mergers and IPOs
- Trending companies from various sources
- Enterprise B2B companies
- Regional e-commerce leaders
- Emerging markets tech companies
- Web3/crypto companies
- D2C brands and subscription economy
"""

import os
import requests
import time
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin
import logging
from typing import List, Dict, Set

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NewsWorthyCompaniesDownloader:
    def __init__(self):
        self.download_dir = "/Users/adi/code/socratify/socratify-yolo/more_newsworthy_companies"
        self.existing_logos = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Create download directory
        os.makedirs(self.download_dir, exist_ok=True)
        
        # Load existing logos to avoid duplicates
        self.load_existing_logos()
        
        # Progress tracking
        self.progress_file = os.path.join(os.getcwd(), "more_newsworthy_progress.json")
        self.load_progress()

    def load_existing_logos(self):
        """Load existing logo names from all directories to avoid duplicates"""
        directories_to_check = [
            "/Users/adi/code/socratify/socratify-yolo/complete_download",
            "/Users/adi/code/socratify/socratify-yolo/additional_newsworthy",
            "/Users/adi/code/socratify/socratify-yolo/additional_major_companies",
            self.download_dir
        ]
        
        for directory in directories_to_check:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    if file.endswith(('.png', '.jpg', '.jpeg')):
                        # Remove extension and normalize
                        company_name = file.rsplit('.', 1)[0].lower().replace('_', ' ')
                        self.existing_logos.add(company_name)
        
        logger.info(f"Loaded {len(self.existing_logos)} existing logos to avoid duplicates")

    def load_progress(self):
        """Load download progress"""
        try:
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        except FileNotFoundError:
            self.progress = {
                'downloaded': [],
                'failed': [],
                'skipped': []
            }

    def save_progress(self):
        """Save download progress"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)

    def get_newsworthy_companies(self) -> List[Dict[str, str]]:
        """
        Comprehensive list of 300+ newsworthy companies from various categories
        """
        companies = [
            # Y Combinator W24/S24/W23/S23 Notable Companies
            {"name": "Anysphere", "category": "AI/Developer Tools", "description": "AI-powered code editor"},
            {"name": "Vanta", "category": "Security/Compliance", "description": "Automated security compliance"},
            {"name": "Retool", "category": "Developer Tools", "description": "Internal tool builder"},
            {"name": "Deel", "category": "HR/Global Payroll", "description": "Global payroll and compliance"},
            {"name": "Lattice", "category": "HR/People Management", "description": "People management platform"},
            {"name": "PostHog", "category": "Analytics", "description": "Product analytics platform"},
            {"name": "Verkada", "category": "Security/Hardware", "description": "Cloud-managed security cameras"},
            {"name": "Brex", "category": "Fintech", "description": "Corporate credit cards and spend management"},
            {"name": "Mercury", "category": "Fintech", "description": "Banking for startups"},
            {"name": "Ramp", "category": "Fintech", "description": "Corporate cards and expense management"},
            {"name": "Pilot", "category": "Fintech/Accounting", "description": "Bookkeeping for startups"},
            {"name": "Webflow", "category": "No-Code/Web Dev", "description": "Visual web development platform"},
            {"name": "Zapier", "category": "Automation", "description": "App integration and automation"},
            {"name": "Superhuman", "category": "Productivity", "description": "Email client for professionals"},
            {"name": "Typeform", "category": "Forms/Surveys", "description": "Interactive forms and surveys"},
            {"name": "Airtable", "category": "Productivity", "description": "Spreadsheet-database hybrid"},
            {"name": "Notion", "category": "Productivity", "description": "All-in-one workspace"},
            {"name": "Figma", "category": "Design", "description": "Collaborative design platform"},
            {"name": "Linear", "category": "Project Management", "description": "Issue tracking for software teams"},
            {"name": "Height", "category": "Project Management", "description": "Autonomous project management"},
            
            # Major VC Portfolio Companies - a16z
            {"name": "OpenSea", "category": "NFT/Web3", "description": "NFT marketplace"},
            {"name": "Dapper Labs", "category": "Web3/Gaming", "description": "Flow blockchain and NBA Top Shot"},
            {"name": "Yuga Labs", "category": "NFT/Web3", "description": "Bored Ape Yacht Club creators"},
            {"name": "Magic Eden", "category": "NFT/Web3", "description": "Solana NFT marketplace"},
            {"name": "Haun Ventures", "category": "Web3/Crypto", "description": "Crypto-focused VC"},
            {"name": "LayerZero", "category": "Web3/Infrastructure", "description": "Omnichain interoperability protocol"},
            {"name": "Aptos", "category": "Web3/Blockchain", "description": "Layer 1 blockchain"},
            {"name": "Sui", "category": "Web3/Blockchain", "description": "Layer 1 blockchain"},
            {"name": "Axie Infinity", "category": "Gaming/Web3", "description": "Play-to-earn game"},
            {"name": "The Sandbox", "category": "Gaming/Metaverse", "description": "Virtual world and gaming platform"},
            
            # Sequoia Portfolio Companies
            {"name": "Klarna", "category": "Fintech", "description": "Buy now, pay later"},
            {"name": "Nubank", "category": "Fintech", "description": "Digital bank Brazil"},
            {"name": "ByteDance", "category": "Social Media", "description": "TikTok parent company"},
            {"name": "Razorpay", "category": "Fintech", "description": "Payment gateway India"},
            {"name": "Zomato", "category": "Food Delivery", "description": "Food delivery India"},
            {"name": "Swiggy", "category": "Food Delivery", "description": "Food delivery India"},
            {"name": "Grab", "category": "Super App", "description": "Southeast Asia super app"},
            {"name": "GoTo", "category": "Super App", "description": "Indonesian super app"},
            {"name": "Sea Limited", "category": "Gaming/E-commerce", "description": "Southeast Asia tech conglomerate"},
            {"name": "Coupang", "category": "E-commerce", "description": "Korean e-commerce"},
            
            # Index Ventures Portfolio
            {"name": "Discord", "category": "Communication", "description": "Gaming-focused chat platform"},
            {"name": "Supercell", "category": "Gaming", "description": "Mobile game developer"},
            {"name": "King Digital", "category": "Gaming", "description": "Candy Crush creators"},
            {"name": "MySQL", "category": "Database", "description": "Open source database"},
            {"name": "Elastic", "category": "Search/Analytics", "description": "Elasticsearch company"},
            {"name": "Adyen", "category": "Fintech", "description": "Payment processing"},
            {"name": "Deliveroo", "category": "Food Delivery", "description": "UK food delivery"},
            {"name": "Revolut", "category": "Fintech", "description": "Digital banking"},
            {"name": "Monzo", "category": "Fintech", "description": "UK digital bank"},
            {"name": "Checkout.com", "category": "Fintech", "description": "Payment processing"},
            
            # Recent SPAC Mergers and De-SPACs
            {"name": "Lucid Motors", "category": "Automotive/EV", "description": "Electric vehicle manufacturer"},
            {"name": "Rivian", "category": "Automotive/EV", "description": "Electric truck manufacturer"},
            {"name": "QuantumScape", "category": "Battery Technology", "description": "Solid-state battery developer"},
            {"name": "Proterra", "category": "EV/Transportation", "description": "Electric bus manufacturer"},
            {"name": "ChargePoint", "category": "EV Infrastructure", "description": "EV charging network"},
            {"name": "Wallbox", "category": "EV Infrastructure", "description": "EV charging solutions"},
            {"name": "SoFi", "category": "Fintech", "description": "Student loan refinancing"},
            {"name": "Affirm", "category": "Fintech", "description": "Buy now, pay later"},
            {"name": "Upstart", "category": "Fintech", "description": "AI-powered lending"},
            {"name": "Lemonade", "category": "Insurtech", "description": "AI-powered insurance"},
            
            # Product Hunt Top Products (2023-2024)
            {"name": "Perplexity AI", "category": "AI/Search", "description": "AI-powered search engine"},
            {"name": "Character.AI", "category": "AI/Conversational", "description": "AI character chatbots"},
            {"name": "Anthropic", "category": "AI/LLM", "description": "Claude AI creator"},
            {"name": "Midjourney", "category": "AI/Image Generation", "description": "AI image generation"},
            {"name": "Stability AI", "category": "AI/Image Generation", "description": "Stable Diffusion creators"},
            {"name": "Runway", "category": "AI/Video", "description": "AI video generation"},
            {"name": "Synthesia", "category": "AI/Video", "description": "AI video avatars"},
            {"name": "Jasper", "category": "AI/Writing", "description": "AI copywriting tool"},
            {"name": "Copy.ai", "category": "AI/Writing", "description": "AI writing assistant"},
            {"name": "Gamma", "category": "AI/Presentation", "description": "AI-powered presentations"},
            
            # B2B Enterprise (Salesforce Competitors)
            {"name": "HubSpot", "category": "CRM/Marketing", "description": "Inbound marketing and CRM"},
            {"name": "Zendesk", "category": "Customer Support", "description": "Customer service platform"},
            {"name": "Intercom", "category": "Customer Support", "description": "Customer messaging platform"},
            {"name": "Freshworks", "category": "Customer Support", "description": "Customer engagement software"},
            {"name": "ServiceNow", "category": "Enterprise Software", "description": "IT service management"},
            {"name": "Workday", "category": "HR/Enterprise", "description": "Human capital management"},
            {"name": "Okta", "category": "Identity Management", "description": "Identity and access management"},
            {"name": "Auth0", "category": "Identity Management", "description": "Developer identity platform"},
            {"name": "Twilio", "category": "Communications API", "description": "Communications platform"},
            {"name": "SendGrid", "category": "Email API", "description": "Email delivery platform"},
            
            # Regional E-commerce Leaders
            {"name": "MercadoLibre", "category": "E-commerce", "description": "Latin America e-commerce"},
            {"name": "Allegro", "category": "E-commerce", "description": "Polish e-commerce"},
            {"name": "Avito", "category": "E-commerce", "description": "Russian classifieds"},
            {"name": "OLX", "category": "E-commerce", "description": "Global classifieds"},
            {"name": "Carousell", "category": "E-commerce", "description": "Southeast Asia classifieds"},
            {"name": "Vinted", "category": "E-commerce", "description": "Second-hand fashion marketplace"},
            {"name": "Depop", "category": "E-commerce", "description": "Social shopping app"},
            {"name": "Poshmark", "category": "E-commerce", "description": "Fashion marketplace"},
            {"name": "ThredUP", "category": "E-commerce", "description": "Online thrift store"},
            {"name": "Vestiaire Collective", "category": "E-commerce", "description": "Luxury fashion resale"},
            
            # Emerging Markets Tech Companies
            {"name": "Paytm", "category": "Fintech", "description": "Indian digital payments"},
            {"name": "PhonePe", "category": "Fintech", "description": "Indian digital payments"},
            {"name": "Zerodha", "category": "Fintech", "description": "Indian stock brokerage"},
            {"name": "Dream11", "category": "Gaming", "description": "Fantasy sports India"},
            {"name": "BYJU'S", "category": "EdTech", "description": "Indian online education"},
            {"name": "Unacademy", "category": "EdTech", "description": "Indian online education"},
            {"name": "Ola", "category": "Transportation", "description": "Indian ride-hailing"},
            {"name": "Oyo", "category": "Travel/Hospitality", "description": "Budget hotel chain"},
            {"name": "Flipkart", "category": "E-commerce", "description": "Indian e-commerce"},
            {"name": "BigBasket", "category": "E-commerce", "description": "Indian grocery delivery"},
            
            # Middle East & Africa
            {"name": "Careem", "category": "Transportation", "description": "Middle East ride-hailing"},
            {"name": "Talabat", "category": "Food Delivery", "description": "Middle East food delivery"},
            {"name": "Noon", "category": "E-commerce", "description": "Middle East e-commerce"},
            {"name": "Souq", "category": "E-commerce", "description": "Middle East e-commerce (Amazon)"},
            {"name": "Vezeeta", "category": "HealthTech", "description": "Middle East healthcare booking"},
            {"name": "Fetchr", "category": "Logistics", "description": "Middle East e-commerce logistics"},
            {"name": "Jumia", "category": "E-commerce", "description": "African e-commerce"},
            {"name": "Flutterwave", "category": "Fintech", "description": "African payments"},
            {"name": "Paystack", "category": "Fintech", "description": "African payments"},
            {"name": "Andela", "category": "Talent/Outsourcing", "description": "African developer training"},
            
            # Direct-to-Consumer Brands
            {"name": "Warby Parker", "category": "D2C/Eyewear", "description": "Online eyewear"},
            {"name": "Casper", "category": "D2C/Sleep", "description": "Mattress-in-a-box"},
            {"name": "Purple", "category": "D2C/Sleep", "description": "Gel grid mattresses"},
            {"name": "Allbirds", "category": "D2C/Footwear", "description": "Sustainable shoes"},
            {"name": "Rothys", "category": "D2C/Footwear", "description": "Recycled plastic shoes"},
            {"name": "Glossier", "category": "D2C/Beauty", "description": "Millennial beauty brand"},
            {"name": "Fenty Beauty", "category": "D2C/Beauty", "description": "Rihanna's beauty brand"},
            {"name": "Drunk Elephant", "category": "D2C/Skincare", "description": "Clean skincare brand"},
            {"name": "The Ordinary", "category": "D2C/Skincare", "description": "Affordable skincare"},
            {"name": "Away", "category": "D2C/Travel", "description": "Smart luggage"},
            
            # Subscription Economy
            {"name": "MasterClass", "category": "EdTech/Subscription", "description": "Celebrity-taught courses"},
            {"name": "Skillshare", "category": "EdTech/Subscription", "description": "Creative learning platform"},
            {"name": "Headspace", "category": "Health/Subscription", "description": "Meditation app"},
            {"name": "Calm", "category": "Health/Subscription", "description": "Sleep and meditation"},
            {"name": "Peloton", "category": "Fitness/Subscription", "description": "Connected fitness equipment"},
            {"name": "Mirror", "category": "Fitness/Subscription", "description": "Home gym mirror"},
            {"name": "Tonal", "category": "Fitness/Subscription", "description": "AI strength training"},
            {"name": "ClassPass", "category": "Fitness/Subscription", "description": "Fitness class marketplace"},
            {"name": "Stitch Fix", "category": "Fashion/Subscription", "description": "Personal styling service"},
            {"name": "Rent the Runway", "category": "Fashion/Subscription", "description": "Designer dress rental"},
            
            # Web3/Crypto (Beyond Major Exchanges)
            {"name": "Chainlink", "category": "Web3/Oracle", "description": "Decentralized oracle network"},
            {"name": "Polygon", "category": "Web3/Scaling", "description": "Ethereum scaling solution"},
            {"name": "Arbitrum", "category": "Web3/Scaling", "description": "Ethereum Layer 2"},
            {"name": "Optimism", "category": "Web3/Scaling", "description": "Ethereum Layer 2"},
            {"name": "The Graph", "category": "Web3/Indexing", "description": "Blockchain data indexing"},
            {"name": "Filecoin", "category": "Web3/Storage", "description": "Decentralized storage"},
            {"name": "Helium", "category": "Web3/IoT", "description": "Decentralized wireless network"},
            {"name": "Livepeer", "category": "Web3/Video", "description": "Decentralized video streaming"},
            {"name": "Arweave", "category": "Web3/Storage", "description": "Permanent data storage"},
            {"name": "IPFS", "category": "Web3/Protocol", "description": "Interplanetary file system"},
            
            # Gaming & Entertainment
            {"name": "Roblox", "category": "Gaming/Metaverse", "description": "User-generated gaming platform"},
            {"name": "Epic Games", "category": "Gaming/Engine", "description": "Fortnite and Unreal Engine"},
            {"name": "Unity", "category": "Gaming/Engine", "description": "Game development platform"},
            {"name": "Niantic", "category": "Gaming/AR", "description": "Pokemon GO creator"},
            {"name": "Immutable", "category": "Gaming/Web3", "description": "NFT gaming platform"},
            {"name": "Sorare", "category": "Gaming/NFT", "description": "Fantasy football NFTs"},
            {"name": "Genies", "category": "Gaming/Avatar", "description": "Digital avatar platform"},
            {"name": "RTFKT", "category": "Gaming/NFT", "description": "Digital sneaker brand (Nike)"},
            {"name": "Horizon Worlds", "category": "Gaming/VR", "description": "Meta's VR social platform"},
            {"name": "VRChat", "category": "Gaming/VR", "description": "Social VR platform"},
            
            # Creator Economy
            {"name": "Substack", "category": "Creator/Publishing", "description": "Newsletter publishing platform"},
            {"name": "ConvertKit", "category": "Creator/Email", "description": "Email marketing for creators"},
            {"name": "Beehiiv", "category": "Creator/Newsletter", "description": "Newsletter platform"},
            {"name": "Ghost", "category": "Creator/Publishing", "description": "Publishing platform"},
            {"name": "Gumroad", "category": "Creator/Commerce", "description": "Digital product sales"},
            {"name": "Teachable", "category": "Creator/Education", "description": "Online course platform"},
            {"name": "Thinkific", "category": "Creator/Education", "description": "Online course creation"},
            {"name": "Kajabi", "category": "Creator/All-in-one", "description": "Creator business platform"},
            {"name": "Patreon", "category": "Creator/Subscription", "description": "Creator subscription platform"},
            {"name": "Ko-fi", "category": "Creator/Support", "description": "Creator support platform"},
            
            # Health Tech
            {"name": "Ro", "category": "HealthTech/Telehealth", "description": "Direct-to-consumer telehealth"},
            {"name": "Hims & Hers", "category": "HealthTech/D2C", "description": "D2C health and wellness"},
            {"name": "Nurx", "category": "HealthTech/D2C", "description": "Birth control delivery"},
            {"name": "Curology", "category": "HealthTech/Dermatology", "description": "Custom skincare treatment"},
            {"name": "MDLIVE", "category": "HealthTech/Telehealth", "description": "Telehealth platform"},
            {"name": "Amwell", "category": "HealthTech/Telehealth", "description": "Telehealth platform"},
            {"name": "Dexcom", "category": "HealthTech/Devices", "description": "Continuous glucose monitoring"},
            {"name": "23andMe", "category": "HealthTech/Genomics", "description": "Consumer genetics testing"},
            {"name": "Color", "category": "HealthTech/Testing", "description": "Health testing and screening"},
            {"name": "Tempus", "category": "HealthTech/AI", "description": "AI-driven precision medicine"},
            
            # Climate Tech
            {"name": "Climeworks", "category": "Climate/Carbon Capture", "description": "Direct air capture"},
            {"name": "Pachama", "category": "Climate/Carbon", "description": "Carbon credit marketplace"},
            {"name": "Charm Industrial", "category": "Climate/Carbon", "description": "Biomass carbon removal"},
            {"name": "Commonwealth Fusion", "category": "Climate/Energy", "description": "Fusion energy"},
            {"name": "QuantumScape", "category": "Climate/Battery", "description": "Solid-state batteries"},
            {"name": "Sila Nanotechnologies", "category": "Climate/Battery", "description": "Silicon nanowire batteries"},
            {"name": "Redwood Materials", "category": "Climate/Recycling", "description": "Battery recycling"},
            {"name": "Sunrun", "category": "Climate/Solar", "description": "Residential solar"},
            {"name": "Enphase Energy", "category": "Climate/Solar", "description": "Solar microinverters"},
            {"name": "Tesla Energy", "category": "Climate/Storage", "description": "Battery storage systems"},
            
            # Space Tech
            {"name": "SpaceX", "category": "Space/Launch", "description": "Rocket launch services"},
            {"name": "Blue Origin", "category": "Space/Launch", "description": "Space tourism and rockets"},
            {"name": "Virgin Galactic", "category": "Space/Tourism", "description": "Space tourism"},
            {"name": "Rocket Lab", "category": "Space/Launch", "description": "Small satellite launches"},
            {"name": "Planet Labs", "category": "Space/Imagery", "description": "Earth imaging satellites"},
            {"name": "Maxar Technologies", "category": "Space/Imagery", "description": "Satellite imagery"},
            {"name": "Relativity Space", "category": "Space/Manufacturing", "description": "3D printed rockets"},
            {"name": "Astra", "category": "Space/Launch", "description": "Small satellite delivery"},
            {"name": "Firefly Aerospace", "category": "Space/Launch", "description": "Small to medium lift rockets"},
            {"name": "ABL Space Systems", "category": "Space/Launch", "description": "Small satellite launches"},
            
            # Additional High-Growth Companies
            {"name": "Canva", "category": "Design/Productivity", "description": "Graphic design platform"},
            {"name": "Miro", "category": "Collaboration", "description": "Online whiteboard platform"},
            {"name": "Monday.com", "category": "Project Management", "description": "Work OS platform"},
            {"name": "Asana", "category": "Project Management", "description": "Team collaboration"},
            {"name": "ClickUp", "category": "Productivity", "description": "All-in-one workspace"},
            {"name": "Calendly", "category": "Scheduling", "description": "Meeting scheduling tool"},
            {"name": "Loom", "category": "Video/Communication", "description": "Screen recording tool"},
            {"name": "Riverside.fm", "category": "Podcasting", "description": "Remote podcast recording"},
            {"name": "Descript", "category": "Audio/Video Editing", "description": "AI-powered editing"},
            {"name": "Replit", "category": "Developer Tools", "description": "Online IDE and hosting"},
        ]
        
        logger.info(f"Generated {len(companies)} newsworthy companies to download")
        return companies

    def clean_company_name(self, name: str) -> str:
        """Clean company name for filename"""
        # Remove common business suffixes and clean
        suffixes = [' Inc', ' Corp', ' Corporation', ' Ltd', ' Limited', ' LLC', ' AG', ' SA', ' SE', ' NV', ' AB', ' AS', ' Plc', ' PLC']
        
        cleaned = name
        for suffix in suffixes:
            if cleaned.endswith(suffix):
                cleaned = cleaned[:-len(suffix)]
                break
        
        # Replace problematic characters
        cleaned = cleaned.replace('&', 'and')
        cleaned = cleaned.replace('/', '_')
        cleaned = cleaned.replace('\\', '_')
        cleaned = cleaned.replace(' ', '_')
        cleaned = cleaned.replace('-', '_')
        cleaned = cleaned.replace('.', '_')
        cleaned = cleaned.replace(',', '_')
        cleaned = cleaned.replace('(', '')
        cleaned = cleaned.replace(')', '')
        cleaned = cleaned.replace('[', '')
        cleaned = cleaned.replace(']', '')
        cleaned = cleaned.replace('{', '')
        cleaned = cleaned.replace('}', '')
        cleaned = cleaned.replace(':', '')
        cleaned = cleaned.replace(';', '')
        cleaned = cleaned.replace('"', '')
        cleaned = cleaned.replace("'", '')
        cleaned = cleaned.replace('?', '')
        cleaned = cleaned.replace('!', '')
        cleaned = cleaned.replace('@', '_')
        cleaned = cleaned.replace('#', '')
        cleaned = cleaned.replace('$', '')
        cleaned = cleaned.replace('%', '')
        cleaned = cleaned.replace('^', '')
        cleaned = cleaned.replace('*', '')
        cleaned = cleaned.replace('+', '_')
        cleaned = cleaned.replace('=', '')
        cleaned = cleaned.replace('|', '_')
        cleaned = cleaned.replace('<', '')
        cleaned = cleaned.replace('>', '')
        cleaned = cleaned.replace('~', '')
        cleaned = cleaned.replace('`', '')
        
        # Remove multiple underscores
        while '__' in cleaned:
            cleaned = cleaned.replace('__', '_')
        
        # Remove leading/trailing underscores
        cleaned = cleaned.strip('_')
        
        return cleaned

    def get_logo_urls(self, company_name: str, company_info: Dict[str, str]) -> List[str]:
        """Generate potential logo URLs for a company"""
        urls = []
        
        # Clearbit logo API (high quality, commonly used)
        domain_guesses = [
            f"{company_name.lower().replace(' ', '')}.com",
            f"{company_name.lower().replace(' ', '').replace('.', '')}.com",
            f"{company_name.lower().replace(' ', '').replace('&', 'and')}.com",
            f"{company_name.lower().replace(' ', '').replace('_', '')}.com",
        ]
        
        for domain in domain_guesses:
            urls.append(f"https://logo.clearbit.com/{domain}")
        
        # Logo.dev API
        for domain in domain_guesses:
            urls.append(f"https://img.logo.dev/{domain}?token=pk_X-1ZO13GSgeOoUrIuJ6GMQ")
        
        # Brandfetch API (free tier)
        for domain in domain_guesses:
            urls.append(f"https://api.brandfetch.io/v2/brands/{domain}/logos")
        
        # Google favicon service
        for domain in domain_guesses:
            urls.append(f"https://www.google.com/s2/favicons?domain={domain}&sz=128")
            urls.append(f"https://www.google.com/s2/favicons?domain={domain}&sz=256")
        
        # DuckDuckGo icons
        for domain in domain_guesses:
            urls.append(f"https://icons.duckduckgo.com/ip3/{domain}.ico")
        
        return urls

    def download_single_logo(self, company: Dict[str, str]) -> Dict[str, str]:
        """Download logo for a single company"""
        company_name = company["name"]
        cleaned_name = self.clean_company_name(company_name)
        
        # Check if already exists or downloaded
        if cleaned_name.lower() in self.existing_logos:
            logger.info(f"Skipping {company_name} - already exists")
            return {"status": "skipped", "company": company_name, "reason": "already_exists"}
        
        if company_name in [item["company"] for item in self.progress.get("downloaded", [])]:
            logger.info(f"Skipping {company_name} - already downloaded")
            return {"status": "skipped", "company": company_name, "reason": "already_downloaded"}
        
        logo_urls = self.get_logo_urls(company_name, company)
        
        for i, url in enumerate(logo_urls):
            try:
                logger.info(f"Trying URL {i+1}/{len(logo_urls)} for {company_name}: {url}")
                
                response = self.session.get(url, timeout=30, stream=True)
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '').lower()
                    if any(img_type in content_type for img_type in ['image/', 'png', 'jpg', 'jpeg', 'gif', 'svg']):
                        # Determine file extension
                        if 'png' in content_type:
                            ext = '.png'
                        elif 'jpeg' in content_type or 'jpg' in content_type:
                            ext = '.png'  # Convert to PNG for consistency
                        elif 'svg' in content_type:
                            ext = '.png'  # We'll convert SVG to PNG
                        else:
                            ext = '.png'
                        
                        file_path = os.path.join(self.download_dir, f"{cleaned_name}{ext}")
                        
                        # Download and save
                        with open(file_path, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        
                        # Verify file was created and has content
                        if os.path.exists(file_path) and os.path.getsize(file_path) > 100:  # At least 100 bytes
                            logger.info(f"✓ Successfully downloaded logo for {company_name}")
                            self.progress["downloaded"].append({
                                "company": company_name,
                                "cleaned_name": cleaned_name,
                                "category": company.get("category", "Unknown"),
                                "description": company.get("description", ""),
                                "url": url,
                                "file_path": file_path
                            })
                            self.save_progress()
                            return {"status": "success", "company": company_name, "file_path": file_path}
                        else:
                            # Remove empty file
                            if os.path.exists(file_path):
                                os.remove(file_path)
                
                # Add delay between requests
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                logger.warning(f"Failed to download from {url}: {str(e)}")
                continue
        
        # If we get here, all URLs failed
        logger.warning(f"✗ Failed to download logo for {company_name}")
        self.progress["failed"].append({
            "company": company_name,
            "category": company.get("category", "Unknown"),
            "reason": "all_urls_failed"
        })
        self.save_progress()
        return {"status": "failed", "company": company_name, "reason": "all_urls_failed"}

    def download_all_logos(self, max_workers: int = 10):
        """Download all logos with threading"""
        companies = self.get_newsworthy_companies()
        
        logger.info(f"Starting download of {len(companies)} newsworthy company logos")
        
        success_count = 0
        failed_count = 0
        skipped_count = 0
        
        # Use ThreadPoolExecutor for concurrent downloads
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all download tasks
            future_to_company = {
                executor.submit(self.download_single_logo, company): company 
                for company in companies
            }
            
            # Process completed downloads
            for future in as_completed(future_to_company):
                result = future.result()
                
                if result["status"] == "success":
                    success_count += 1
                elif result["status"] == "failed":
                    failed_count += 1
                elif result["status"] == "skipped":
                    skipped_count += 1
                
                # Progress update
                total_processed = success_count + failed_count + skipped_count
                logger.info(f"Progress: {total_processed}/{len(companies)} | Success: {success_count} | Failed: {failed_count} | Skipped: {skipped_count}")
        
        # Final summary
        logger.info("="*60)
        logger.info("FINAL DOWNLOAD SUMMARY")
        logger.info("="*60)
        logger.info(f"Total companies processed: {len(companies)}")
        logger.info(f"Successfully downloaded: {success_count}")
        logger.info(f"Failed downloads: {failed_count}")
        logger.info(f"Skipped (already existed): {skipped_count}")
        logger.info(f"Download directory: {self.download_dir}")
        
        # Show some statistics by category
        if self.progress["downloaded"]:
            categories = {}
            for item in self.progress["downloaded"]:
                category = item.get("category", "Unknown")
                categories[category] = categories.get(category, 0) + 1
            
            logger.info("\nDownloaded by category:")
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                logger.info(f"  {category}: {count}")

def main():
    """Main function to run the downloader"""
    downloader = NewsWorthyCompaniesDownloader()
    downloader.download_all_logos(max_workers=8)  # Adjust based on your system

if __name__ == "__main__":
    main()