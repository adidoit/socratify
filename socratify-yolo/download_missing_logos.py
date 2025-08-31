#!/usr/bin/env python3
"""
Script to download missing major company logos using Clearbit Logo API
"""

import requests
import os
import time
from urllib.parse import urlparse
from typing import List, Dict

def create_output_directory(directory_name: str = "additional_major_companies") -> str:
    """Create output directory for downloaded logos"""
    output_dir = os.path.join(os.getcwd(), directory_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    return output_dir

def download_logo(company_name: str, domain: str, output_dir: str) -> bool:
    """
    Download company logo from Clearbit API
    
    Args:
        company_name: Name of the company (for filename)
        domain: Company domain for Clearbit API
        output_dir: Directory to save the logo
        
    Returns:
        bool: True if download successful, False otherwise
    """
    # Clearbit Logo API URL
    clearbit_url = f"https://logo.clearbit.com/{domain}"
    
    try:
        print(f"Downloading logo for {company_name} from {domain}...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(clearbit_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Save the logo
            filename = f"{company_name.replace(' ', '_').replace('.', '_')}.png"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ Successfully downloaded: {filename}")
            return True
            
        elif response.status_code == 404:
            print(f"✗ Logo not found for {company_name} ({domain})")
            return False
            
        else:
            print(f"✗ Error downloading {company_name}: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Network error downloading {company_name}: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error downloading {company_name}: {str(e)}")
        return False

def main():
    """Main function to download missing company logos"""
    
    # List of potentially missing major companies with their domains
    # Based on analysis of recent unicorns, IPOs, and major tech companies
    missing_companies = [
        # Major AI Unicorns that might be missing
        {"name": "xAI", "domain": "x.ai"},
        {"name": "Scale_AI", "domain": "scale.com"},
        {"name": "Speak", "domain": "speak.com"},
        {"name": "Harvey_AI", "domain": "harvey.ai"},
        {"name": "Infinite_Reality", "domain": "infinitereality.com"},
        {"name": "Quantinuum", "domain": "quantinuum.com"},
        
        # Recent IPOs and major tech companies
        {"name": "Circle", "domain": "circle.com"},
        {"name": "Chime", "domain": "chime.com"},
        {"name": "MNTN", "domain": "mntn.com"},
        {"name": "Medline_Industries", "domain": "medline.com"},
        {"name": "Plaid", "domain": "plaid.com"},
        {"name": "SeatGeek", "domain": "seatgeek.com"},
        
        # Major Private Companies
        {"name": "Epic_Games", "domain": "epicgames.com"},
        {"name": "Instacart", "domain": "instacart.com"},
        {"name": "Shein", "domain": "shein.com"},
        {"name": "Bytedance_TikTok", "domain": "bytedance.com"},
        
        # Other notable companies that might be missing
        {"name": "Notion", "domain": "notion.so"},
        {"name": "Miro", "domain": "miro.com"},
        {"name": "Linear", "domain": "linear.app"},
        {"name": "Vercel", "domain": "vercel.com"},
        {"name": "Supabase", "domain": "supabase.com"},
        {"name": "Replicate", "domain": "replicate.com"},
        {"name": "Hugging_Face", "domain": "huggingface.co"},
        {"name": "Midjourney", "domain": "midjourney.com"},
        {"name": "Stability_AI", "domain": "stability.ai"},
        {"name": "Runway", "domain": "runwayml.com"},
        {"name": "Character_AI", "domain": "character.ai"},
        {"name": "Cohere", "domain": "cohere.ai"},
        
        # Financial Services
        {"name": "Robinhood", "domain": "robinhood.com"},
        {"name": "Affirm", "domain": "affirm.com"},
        {"name": "Zip_Pay", "domain": "zip.co"},
        
        # Recent Notable Companies
        {"name": "Telegram", "domain": "telegram.org"},
        {"name": "Signal", "domain": "signal.org"},
        {"name": "Mastodon", "domain": "mastodon.social"},
        {"name": "Bluesky", "domain": "bsky.app"},
        {"name": "Threads", "domain": "threads.net"},
    ]
    
    print("Starting logo download process...")
    print(f"Total companies to check: {len(missing_companies)}")
    
    # Create output directory
    output_dir = create_output_directory()
    
    # Track download results
    successful_downloads = 0
    failed_downloads = 0
    
    # Download each logo with a small delay between requests
    for i, company in enumerate(missing_companies, 1):
        print(f"\n[{i}/{len(missing_companies)}] Processing {company['name']}...")
        
        success = download_logo(company['name'], company['domain'], output_dir)
        
        if success:
            successful_downloads += 1
        else:
            failed_downloads += 1
        
        # Small delay to be respectful to the API
        time.sleep(0.5)
    
    # Print summary
    print(f"\n{'='*50}")
    print("DOWNLOAD SUMMARY")
    print(f"{'='*50}")
    print(f"Total companies processed: {len(missing_companies)}")
    print(f"Successfully downloaded: {successful_downloads}")
    print(f"Failed downloads: {failed_downloads}")
    print(f"Success rate: {(successful_downloads/len(missing_companies)*100):.1f}%")
    print(f"Logos saved to: {output_dir}")
    
    if successful_downloads > 0:
        print(f"\n✓ {successful_downloads} new company logos have been downloaded!")
    
    return successful_downloads, failed_downloads

if __name__ == "__main__":
    main()