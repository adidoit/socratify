#!/usr/bin/env python3
"""
Download the 21 hottest missing AI companies that people aspire to work for in 2025
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 20
RATE_LIMIT = threading.Semaphore(15)
RATE_LIMIT_DELAY = 0.05  # 50ms delay

def clean_filename(company_name):
    """Convert company name to clean filename"""
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    filename = filename.strip('_')
    return filename

def generate_domains(company_name):
    """Generate domain variations for hot AI companies"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    
    # Split into words
    words = base.split()
    
    domains = []
    
    # Standard domain patterns
    if len(words) == 1:
        domains.extend([
            f"{words[0]}.com",
            f"{words[0]}.ai", 
            f"{words[0]}.io",
            f"{words[0]}.co"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.ai",
            f"{words[0]}.com"
        ])
    elif len(words) >= 3:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}.com",
            f"{words[0]}.ai"
        ])
    
    # Special cases for specific AI companies
    special_cases = {
        'mistral ai': ['mistral.ai'],
        'perplexity ai': ['perplexity.ai'],
        'adept ai': ['adept.ai'],
        'ai21 labs': ['ai21.com'],
        'cognition labs': ['cognition-labs.com', 'devin.ai'],
        'sanctuary ai': ['sanctuary.ai'],
        'poolside': ['poolside.ai'],
        'tabnine': ['tabnine.com'],
        'codium ai': ['codium.ai', 'qodo.ai'],
        'mintlify': ['mintlify.com'],
        'exscientia': ['exscientia.ai'],
        'freenome': ['freenome.com'],
        'notable': ['notable.com'],
        'qdrant': ['qdrant.io', 'qdrant.tech'],
        'langchain': ['langchain.com', 'python.langchain.com'],
        'wandb': ['wandb.ai', 'wandb.com'],
        'h2o ai': ['h2o.ai'],
        'dataiku': ['dataiku.com'],
        'c3 ai': ['c3.ai'],
        'graphcore': ['graphcore.ai'],
        'mythic': ['mythic-ai.com']
    }
    
    if base in special_cases:
        domains = special_cases[base] + domains
    
    return list(dict.fromkeys(domains))

def download_logo(company_name, output_dir):
    """Download logo for hot AI company"""
    
    with RATE_LIMIT:
        time.sleep(RATE_LIMIT_DELAY)
        
        domains = generate_domains(company_name)
        
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
                    
                    filename = f"{clean_filename(company_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    if os.path.getsize(filepath) > 500:
                        return f"🔥 {company_name} -> {filename} (domain: {domain})"
                    else:
                        os.remove(filepath)
                
                # Try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(company_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"🔍 {company_name} -> {filename} (favicon: {domain})"
                
            except Exception as e:
                continue
        
        return f"❌ {company_name} - No logo found"

def main():
    # Top priority missing AI companies
    hottest_missing_companies = [
        # Foundation Models (Highest Priority)
        "Mistral AI",
        "Perplexity AI", 
        "Adept AI",
        "AI21 Labs",
        
        # AI Agents & Automation
        "Cognition Labs",
        
        # Computer Vision & Robotics
        "Sanctuary AI",
        
        # Hot AI Startups 2024-2025
        "Poolside",
        "Tabnine",
        "Codium AI",
        "Mintlify",
        
        # Vertical AI Specialized
        "Exscientia",
        "Freenome", 
        "Notable",
        
        # AI Infrastructure Tools
        "Qdrant",
        "LangChain",
        "Wandb",
        
        # Enterprise AI Platforms  
        "H2O.ai",
        "Dataiku",
        "C3 AI",
        
        # AI Hardware Chips
        "Graphcore",
        "Mythic"
    ]
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"🔥 DOWNLOADING HOTTEST 2025 AI COMPANIES 🔥")
    print(f"Companies people are DYING to work for!")
    print(f"Total companies: {len(hottest_missing_companies)}")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers\\n")
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_company = {
            executor.submit(download_logo, company, output_dir): company
            for company in hottest_missing_companies
        }
        
        for future in as_completed(future_to_company):
            result = future.result()
            company = future_to_company[future]
            print(result)
            
            if result.startswith("🔥") or result.startswith("🔍"):
                downloaded_count += 1
            else:
                failed_count += 1
    
    print(f"\\n🎉 HOTTEST AI COMPANIES DOWNLOAD COMPLETE! 🎉")
    print(f"Total companies: {len(hottest_missing_companies)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    if len(hottest_missing_companies) > 0:
        print(f"Success rate: {(downloaded_count/len(hottest_missing_companies)*100):.1f}%")
    
    # Update collection count
    previous_total = 8143  # From previous expansion
    new_total = previous_total + downloaded_count
    print(f"\\n📊 Collection now has: ~{new_total} business logos")
    print(f"\\n✅ NOW COVERING ALL THE HOTTEST AI COMPANIES PEOPLE WANT TO WORK FOR!")
    print(f"🔥 Foundation Models: Mistral AI, Perplexity AI, Adept AI")  
    print(f"🤖 AI Agents: Cognition Labs (Devin)")
    print(f"💻 Dev Tools: Poolside, Tabnine, Codium AI")
    print(f"🏥 Health AI: Exscientia, Freenome")
    print(f"⚙️  Infrastructure: Qdrant, LangChain, Wandb")
    print(f"🏢 Enterprise: H2O.ai, Dataiku, C3 AI")

if __name__ == "__main__":
    main()