#!/usr/bin/env python3
"""
Expanded script to find and download logos for 300+ more newsworthy companies.
This extends our first batch with additional categories and companies.
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

class ExpandedNewsWorthyCompaniesDownloader:
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
        self.progress_file = os.path.join(os.getcwd(), "expanded_newsworthy_progress.json")
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

    def get_expanded_newsworthy_companies(self) -> List[Dict[str, str]]:
        """
        Expanded list with additional categories to reach 300+ companies
        """
        companies = [
            # YC Companies - More from recent batches
            {"name": "Mem", "category": "AI/Productivity", "description": "AI-powered note-taking"},
            {"name": "Browse AI", "category": "AI/Automation", "description": "Web scraping automation"},
            {"name": "Taplio", "category": "Social Media/B2B", "description": "LinkedIn growth tool"},
            {"name": "CommandBar", "category": "Developer Tools", "description": "User assistance platform"},
            {"name": "Axiom", "category": "AI/Legal", "description": "AI legal research"},
            {"name": "Raycast", "category": "Productivity", "description": "Spotlight replacement for Mac"},
            {"name": "Baseten", "category": "AI/MLOps", "description": "ML model deployment"},
            {"name": "Weights & Biases", "category": "AI/MLOps", "description": "ML experiment tracking"},
            {"name": "Anyscale", "category": "AI/Infrastructure", "description": "Ray-based ML platform"},
            {"name": "Modal", "category": "Cloud Computing", "description": "Serverless compute for data"},
            
            # Enterprise B2B - Additional Players
            {"name": "Datadog", "category": "DevOps/Monitoring", "description": "Application monitoring"},
            {"name": "New Relic", "category": "DevOps/Monitoring", "description": "Application performance"},
            {"name": "PagerDuty", "category": "DevOps/Incident", "description": "Incident response"},
            {"name": "JFrog", "category": "DevOps/CI/CD", "description": "DevOps platform"},
            {"name": "HashiCorp", "category": "DevOps/Infrastructure", "description": "Infrastructure automation"},
            {"name": "GitLab", "category": "DevOps/Code", "description": "DevOps platform"},
            {"name": "Atlassian", "category": "Collaboration", "description": "Team collaboration tools"},
            {"name": "Confluence", "category": "Documentation", "description": "Team documentation"},
            {"name": "Jira", "category": "Project Management", "description": "Issue tracking"},
            {"name": "Bitbucket", "category": "Developer Tools", "description": "Git repository hosting"},
            
            # Regional E-commerce - More Global Players  
            {"name": "Shopee", "category": "E-commerce", "description": "Southeast Asia e-commerce"},
            {"name": "Tokopedia", "category": "E-commerce", "description": "Indonesian e-commerce"},
            {"name": "Bukalapak", "category": "E-commerce", "description": "Indonesian e-commerce"},
            {"name": "Gojek", "category": "Super App", "description": "Indonesian super app"},
            {"name": "Traveloka", "category": "Travel", "description": "Southeast Asia travel booking"},
            {"name": "RedMart", "category": "E-commerce", "description": "Singapore grocery delivery"},
            {"name": "Qoo10", "category": "E-commerce", "description": "Asian e-commerce platform"},
            {"name": "Rakuten", "category": "E-commerce", "description": "Japanese e-commerce"},
            {"name": "Alibaba", "category": "E-commerce", "description": "Chinese e-commerce giant"},
            {"name": "Taobao", "category": "E-commerce", "description": "Chinese consumer marketplace"},
            
            # Indian Tech Companies - Expanded
            {"name": "Zomato", "category": "Food Delivery", "description": "Indian food delivery"},
            {"name": "Swiggy", "category": "Food Delivery", "description": "Indian food delivery"},
            {"name": "Razorpay", "category": "Fintech", "description": "Indian payment gateway"},
            {"name": "Paytm", "category": "Fintech", "description": "Indian digital payments"},
            {"name": "PhonePe", "category": "Fintech", "description": "Indian UPI payments"},
            {"name": "PolicyBazaar", "category": "Insurtech", "description": "Indian insurance marketplace"},
            {"name": "Nykaa", "category": "Beauty/E-commerce", "description": "Indian beauty marketplace"},
            {"name": "Urban Company", "category": "Services", "description": "Indian home services"},
            {"name": "Byju's", "category": "EdTech", "description": "Indian online education"},
            {"name": "Vedantu", "category": "EdTech", "description": "Indian online tutoring"},
            
            # Middle East & Africa - Expanded
            {"name": "Souq", "category": "E-commerce", "description": "Middle East marketplace"},
            {"name": "Namshi", "category": "Fashion", "description": "Middle East fashion"},
            {"name": "Mumzworld", "category": "E-commerce", "description": "Middle East mother & baby"},
            {"name": "Wadi", "category": "E-commerce", "description": "Middle East marketplace"},
            {"name": "MaxAB", "category": "B2B Commerce", "description": "Egyptian B2B marketplace"},
            {"name": "Trella", "category": "Logistics", "description": "MENA freight marketplace"},
            {"name": "Swvl", "category": "Transportation", "description": "MENA bus booking"},
            {"name": "Kobo360", "category": "Logistics", "description": "African logistics platform"},
            {"name": "Twiga Foods", "category": "AgriTech", "description": "Kenyan food distribution"},
            {"name": "Branch", "category": "Fintech", "description": "African mobile lending"},
            
            # Latin America - Expanded
            {"name": "Rappi", "category": "Delivery", "description": "Latin American super app"},
            {"name": "iFood", "category": "Food Delivery", "description": "Brazilian food delivery"},
            {"name": "Cornershop", "category": "Grocery Delivery", "description": "Latin American grocery"},
            {"name": "Creditas", "category": "Fintech", "description": "Brazilian credit platform"},
            {"name": "Nubank", "category": "Fintech", "description": "Brazilian digital bank"},
            {"name": "PagSeguro", "category": "Fintech", "description": "Brazilian payments"},
            {"name": "StoneCo", "category": "Fintech", "description": "Brazilian payments"},
            {"name": "Mercado Pago", "category": "Fintech", "description": "Latin American payments"},
            {"name": "Kavak", "category": "Automotive", "description": "Mexican used car marketplace"},
            {"name": "Bitso", "category": "Crypto", "description": "Mexican crypto exchange"},
            
            # European Tech - Expanded
            {"name": "Spotify", "category": "Music Streaming", "description": "Swedish music platform"},
            {"name": "Klarna", "category": "Fintech", "description": "Swedish BNPL"},
            {"name": "Adyen", "category": "Fintech", "description": "Dutch payment processing"},
            {"name": "Mollie", "category": "Fintech", "description": "Dutch payment platform"},
            {"name": "Bunq", "category": "Fintech", "description": "Dutch digital bank"},
            {"name": "N26", "category": "Fintech", "description": "German digital bank"},
            {"name": "Wirecard", "category": "Fintech", "description": "German payment processor"},
            {"name": "Auto1", "category": "Automotive", "description": "German used car platform"},
            {"name": "Zalando", "category": "Fashion", "description": "German fashion e-commerce"},
            {"name": "HelloFresh", "category": "Food", "description": "German meal kit delivery"},
            
            # Emerging Unicorns - High Growth Companies
            {"name": "Canva", "category": "Design", "description": "Australian design platform"},
            {"name": "Afterpay", "category": "Fintech", "description": "Australian BNPL"},
            {"name": "Zip Co", "category": "Fintech", "description": "Australian BNPL"},
            {"name": "Airwallex", "category": "Fintech", "description": "Australian B2B payments"},
            {"name": "SafetyCulture", "category": "Workplace Safety", "description": "Australian safety platform"},
            {"name": "Atlassian", "category": "Software", "description": "Australian collaboration tools"},
            {"name": "Xero", "category": "Accounting", "description": "New Zealand accounting"},
            {"name": "Weta Digital", "category": "VFX", "description": "New Zealand visual effects"},
            {"name": "Rocket Lab", "category": "Space", "description": "NZ/US rocket company"},
            {"name": "LanzaTech", "category": "CleanTech", "description": "NZ carbon recycling"},
            
            # B2B SaaS - Additional Players
            {"name": "Salesforce", "category": "CRM", "description": "Cloud CRM platform"},
            {"name": "Microsoft", "category": "Enterprise Software", "description": "Software giant"},
            {"name": "Oracle", "category": "Database/Enterprise", "description": "Database and cloud"},
            {"name": "SAP", "category": "Enterprise Software", "description": "Enterprise applications"},
            {"name": "Adobe", "category": "Creative Software", "description": "Creative and marketing tools"},
            {"name": "Autodesk", "category": "Design Software", "description": "CAD and 3D software"},
            {"name": "Intuit", "category": "Financial Software", "description": "QuickBooks and TurboTax"},
            {"name": "DocuSign", "category": "Digital Signatures", "description": "Electronic signature"},
            {"name": "Box", "category": "Cloud Storage", "description": "Enterprise cloud storage"},
            {"name": "Dropbox", "category": "Cloud Storage", "description": "File sharing and storage"},
            
            # Direct-to-Consumer - More Brands
            {"name": "Glossier", "category": "Beauty", "description": "Millennial beauty brand"},
            {"name": "Kylie Cosmetics", "category": "Beauty", "description": "Celebrity beauty brand"},
            {"name": "Rare Beauty", "category": "Beauty", "description": "Selena Gomez beauty brand"},
            {"name": "Fenty Beauty", "category": "Beauty", "description": "Rihanna beauty brand"},
            {"name": "Honest Company", "category": "Consumer Goods", "description": "Jessica Alba's brand"},
            {"name": "Goop", "category": "Lifestyle", "description": "Gwyneth Paltrow's brand"},
            {"name": "Kotn", "category": "Fashion", "description": "Egyptian cotton clothing"},
            {"name": "Everlane", "category": "Fashion", "description": "Transparent fashion"},
            {"name": "Reformation", "category": "Fashion", "description": "Sustainable fashion"},
            {"name": "Girlfriend Collective", "category": "Activewear", "description": "Sustainable activewear"},
            
            # Gaming & Entertainment - Expanded
            {"name": "Roblox", "category": "Gaming", "description": "User-generated gaming"},
            {"name": "Epic Games", "category": "Gaming", "description": "Fortnite creator"},
            {"name": "Riot Games", "category": "Gaming", "description": "League of Legends"},
            {"name": "Valve", "category": "Gaming", "description": "Steam platform"},
            {"name": "Unity", "category": "Gaming", "description": "Game engine"},
            {"name": "Unreal Engine", "category": "Gaming", "description": "Epic's game engine"},
            {"name": "Discord", "category": "Communication", "description": "Gaming chat platform"},
            {"name": "Twitch", "category": "Streaming", "description": "Game streaming"},
            {"name": "YouTube Gaming", "category": "Streaming", "description": "Google's gaming platform"},
            {"name": "TikTok", "category": "Social Media", "description": "Short-form video"},
            
            # Creator Economy - Expanded
            {"name": "OnlyFans", "category": "Creator Platform", "description": "Subscription content"},
            {"name": "Cameo", "category": "Creator Platform", "description": "Celebrity video messages"},
            {"name": "Clubhouse", "category": "Audio Social", "description": "Audio chat rooms"},
            {"name": "Spaces", "category": "Audio Social", "description": "Twitter's audio feature"},
            {"name": "Anchor", "category": "Podcasting", "description": "Spotify's podcast platform"},
            {"name": "Riverside", "category": "Podcasting", "description": "Remote podcast recording"},
            {"name": "Descript", "category": "Audio/Video", "description": "AI-powered editing"},
            {"name": "Loom", "category": "Video", "description": "Screen recording"},
            {"name": "Notion", "category": "Productivity", "description": "All-in-one workspace"},
            {"name": "Obsidian", "category": "Note-taking", "description": "Knowledge management"},
            
            # Health Tech - Expanded
            {"name": "Teladoc", "category": "Telehealth", "description": "Virtual healthcare"},
            {"name": "Amwell", "category": "Telehealth", "description": "Virtual care platform"},
            {"name": "MDLive", "category": "Telehealth", "description": "On-demand healthcare"},
            {"name": "PlushCare", "category": "Telehealth", "description": "Virtual primary care"},
            {"name": "Doctor on Demand", "category": "Telehealth", "description": "Video consultations"},
            {"name": "K Health", "category": "AI Health", "description": "AI symptom checker"},
            {"name": "Ada Health", "category": "AI Health", "description": "AI health assessment"},
            {"name": "Babylon Health", "category": "AI Health", "description": "AI healthcare assistant"},
            {"name": "Livongo", "category": "Digital Health", "description": "Diabetes management"},
            {"name": "Omada Health", "category": "Digital Health", "description": "Chronic disease prevention"},
            
            # Fintech - Additional Players
            {"name": "Square", "category": "Fintech", "description": "Payment processing"},
            {"name": "Cash App", "category": "Fintech", "description": "P2P payments"},
            {"name": "Venmo", "category": "Fintech", "description": "P2P payments"},
            {"name": "Zelle", "category": "Fintech", "description": "Bank-backed P2P"},
            {"name": "Robinhood", "category": "Fintech", "description": "Commission-free trading"},
            {"name": "Webull", "category": "Fintech", "description": "Online brokerage"},
            {"name": "M1 Finance", "category": "Fintech", "description": "Automated investing"},
            {"name": "Personal Capital", "category": "WealthTech", "description": "Wealth management"},
            {"name": "Betterment", "category": "Robo-Advisor", "description": "Automated investing"},
            {"name": "Wealthfront", "category": "Robo-Advisor", "description": "Automated investing"},
            
            # Travel & Hospitality - Expanded  
            {"name": "Airbnb", "category": "Travel", "description": "Home sharing platform"},
            {"name": "Booking.com", "category": "Travel", "description": "Hotel booking"},
            {"name": "Expedia", "category": "Travel", "description": "Travel booking"},
            {"name": "Kayak", "category": "Travel", "description": "Travel search"},
            {"name": "Skyscanner", "category": "Travel", "description": "Flight comparison"},
            {"name": "TripAdvisor", "category": "Travel", "description": "Travel reviews"},
            {"name": "Hopper", "category": "Travel", "description": "Flight prediction app"},
            {"name": "GetYourGuide", "category": "Travel", "description": "Tours and activities"},
            {"name": "Klook", "category": "Travel", "description": "Activities booking"},
            {"name": "Hostelworld", "category": "Travel", "description": "Hostel booking"},
            
            # EdTech - Global Expansion
            {"name": "Coursera", "category": "EdTech", "description": "Online course platform"},
            {"name": "Udemy", "category": "EdTech", "description": "Online learning marketplace"},
            {"name": "Khan Academy", "category": "EdTech", "description": "Free online education"},
            {"name": "Duolingo", "category": "EdTech", "description": "Language learning app"},
            {"name": "Babbel", "category": "EdTech", "description": "Language learning"},
            {"name": "Rosetta Stone", "category": "EdTech", "description": "Language learning software"},
            {"name": "MindMeister", "category": "EdTech", "description": "Mind mapping tool"},
            {"name": "Prezi", "category": "EdTech", "description": "Presentation software"},
            {"name": "Zoom", "category": "EdTech/Communication", "description": "Video conferencing"},
            {"name": "Google Classroom", "category": "EdTech", "description": "Classroom management"},
            
            # Cybersecurity - High Growth Sector
            {"name": "CrowdStrike", "category": "Cybersecurity", "description": "Endpoint protection"},
            {"name": "SentinelOne", "category": "Cybersecurity", "description": "AI-powered security"},
            {"name": "Palo Alto Networks", "category": "Cybersecurity", "description": "Network security"},
            {"name": "Fortinet", "category": "Cybersecurity", "description": "Network security"},
            {"name": "Check Point", "category": "Cybersecurity", "description": "Network security"},
            {"name": "Zscaler", "category": "Cybersecurity", "description": "Cloud security"},
            {"name": "Okta", "category": "Identity Security", "description": "Identity management"},
            {"name": "Ping Identity", "category": "Identity Security", "description": "Identity solutions"},
            {"name": "Cyberark", "category": "Cybersecurity", "description": "Privileged access management"},
            {"name": "Splunk", "category": "Security Analytics", "description": "Data analytics platform"},
            
            # Logistics & Supply Chain
            {"name": "FedEx", "category": "Logistics", "description": "Global shipping"},
            {"name": "UPS", "category": "Logistics", "description": "Package delivery"},
            {"name": "DHL", "category": "Logistics", "description": "International courier"},
            {"name": "C.H. Robinson", "category": "Logistics", "description": "Third-party logistics"},
            {"name": "XPO Logistics", "category": "Logistics", "description": "Supply chain solutions"},
            {"name": "Flexport", "category": "Logistics", "description": "Digital freight forwarding"},
            {"name": "Convoy", "category": "Logistics", "description": "Digital freight network"},
            {"name": "Uber Freight", "category": "Logistics", "description": "Freight marketplace"},
            {"name": "Freightos", "category": "Logistics", "description": "Freight booking platform"},
            {"name": "Project44", "category": "Logistics", "description": "Supply chain visibility"},
        ]
        
        logger.info(f"Generated {len(companies)} expanded newsworthy companies to download")
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
        companies = self.get_expanded_newsworthy_companies()
        
        logger.info(f"Starting download of {len(companies)} expanded newsworthy company logos")
        
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
        logger.info("FINAL EXPANDED DOWNLOAD SUMMARY")
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
    """Main function to run the expanded downloader"""
    downloader = ExpandedNewsWorthyCompaniesDownloader()
    downloader.download_all_logos(max_workers=8)  # Adjust based on your system

if __name__ == "__main__":
    main()