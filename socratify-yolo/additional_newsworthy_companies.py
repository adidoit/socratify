#!/usr/bin/env python3
"""
Additional Newsworthy Companies - Supplement to main downloader
Focus on companies that frequently appear in business news but might not be in the main script.
"""

import requests
import os
import time
import json
from typing import List, Dict

def get_additional_newsworthy_companies() -> List[Dict]:
    """Additional companies frequently in business news"""
    
    return [
        # Recent unicorns and hot startups
        {"name": "Epic_Games", "domain": "epicgames.com"},
        {"name": "Discord", "domain": "discord.com"},
        {"name": "Notion", "domain": "notion.so"},
        {"name": "Figma", "domain": "figma.com"},
        {"name": "Miro", "domain": "miro.com"},
        {"name": "Canva", "domain": "canva.com"},
        {"name": "Telegram", "domain": "telegram.org"},
        {"name": "Signal", "domain": "signal.org"},
        {"name": "Mastodon", "domain": "mastodon.social"},
        {"name": "Bluesky", "domain": "bsky.app"},
        {"name": "Threads", "domain": "threads.net"},
        
        # Hot AI companies 2024-2025
        {"name": "xAI", "domain": "x.ai"},
        {"name": "Cursor", "domain": "cursor.sh"},
        {"name": "v0", "domain": "v0.dev"},
        {"name": "Replit", "domain": "replit.com"},
        {"name": "Supabase", "domain": "supabase.com"},
        {"name": "Vercel", "domain": "vercel.com"},
        {"name": "Linear", "domain": "linear.app"},
        {"name": "Height", "domain": "height.app"},
        
        # Crypto and Web3 that make headlines
        {"name": "OpenSea", "domain": "opensea.io"},
        {"name": "Uniswap", "domain": "uniswap.org"},
        {"name": "Magic_Eden", "domain": "magiceden.io"},
        {"name": "Solana", "domain": "solana.com"},
        {"name": "Polygon", "domain": "polygon.technology"},
        {"name": "Arbitrum", "domain": "arbitrum.io"},
        {"name": "Optimism", "domain": "optimism.io"},
        
        # Indian unicorns frequently in news
        {"name": "BYJU_S", "domain": "byjus.com"},
        {"name": "Unacademy", "domain": "unacademy.com"},
        {"name": "Dream11", "domain": "dream11.com"},
        {"name": "Zomato", "domain": "zomato.com"},
        {"name": "Swiggy", "domain": "swiggy.com"},
        {"name": "Flipkart", "domain": "flipkart.com"},
        {"name": "Paytm", "domain": "paytm.com"},
        {"name": "Ola", "domain": "olacabs.com"},
        {"name": "PhonePe", "domain": "phonepe.com"},
        {"name": "Razorpay", "domain": "razorpay.com"},
        {"name": "Zerodha", "domain": "zerodha.com"},
        {"name": "Freshworks", "domain": "freshworks.com"},
        
        # Southeast Asian tech making news
        {"name": "GoTo", "domain": "goto.com"},
        {"name": "Garena", "domain": "garena.com"},
        {"name": "Lazada", "domain": "lazada.com"},
        {"name": "LINE", "domain": "line.me"},
        {"name": "Kakao", "domain": "kakaocorp.com"},
        {"name": "Naver", "domain": "navercorp.com"},
        
        # Middle Eastern tech champions
        {"name": "Careem", "domain": "careem.com"},
        {"name": "Noon", "domain": "noon.com"},
        {"name": "Souq", "domain": "souq.com"},
        {"name": "Talabat", "domain": "talabat.com"},
        {"name": "Fetchr", "domain": "fetchr.us"},
        {"name": "Vezeeta", "domain": "vezeeta.com"},
        
        # Gaming companies making headlines
        {"name": "Roblox", "domain": "roblox.com"},
        {"name": "Unity", "domain": "unity.com"},
        {"name": "Unreal_Engine", "domain": "unrealengine.com"},
        {"name": "Riot_Games", "domain": "riotgames.com"},
        {"name": "Valve", "domain": "valvesoftware.com"},
        {"name": "Twitch", "domain": "twitch.tv"},
        {"name": "Steam", "domain": "steampowered.com"},
        
        # Productivity and work tools trending
        {"name": "Slack", "domain": "slack.com"},
        {"name": "Zoom", "domain": "zoom.us"},
        {"name": "Calendly", "domain": "calendly.com"},
        {"name": "Loom", "domain": "loom.com"},
        {"name": "Grammarly", "domain": "grammarly.com"},
        {"name": "Typeform", "domain": "typeform.com"},
        {"name": "Mailchimp", "domain": "mailchimp.com"},
        
        # E-commerce and marketplaces trending
        {"name": "Instacart", "domain": "instacart.com"},
        {"name": "DoorDash", "domain": "doordash.com"},
        {"name": "Uber_Eats", "domain": "ubereats.com"},
        {"name": "Postmates", "domain": "postmates.com"},
        {"name": "Grubhub", "domain": "grubhub.com"},
        {"name": "Deliveroo", "domain": "deliveroo.com"},
        
        # Fashion and lifestyle newsworthy
        {"name": "Shein", "domain": "shein.com"},
        {"name": "Temu", "domain": "temu.com"},
        {"name": "Wish", "domain": "wish.com"},
        {"name": "StitchFix", "domain": "stitchfix.com"},
        {"name": "Rent_the_Runway", "domain": "renttherunway.com"},
        
        # Travel tech making headlines  
        {"name": "Airbnb", "domain": "airbnb.com"},
        {"name": "Booking_com", "domain": "booking.com"},
        {"name": "Expedia", "domain": "expedia.com"},
        {"name": "Kayak", "domain": "kayak.com"},
        {"name": "Skyscanner", "domain": "skyscanner.com"},
        {"name": "TripAdvisor", "domain": "tripadvisor.com"},
        
        # Health tech getting attention
        {"name": "Teladoc", "domain": "teladoc.com"},
        {"name": "Ro", "domain": "ro.co"},
        {"name": "Hims", "domain": "hims.com"},
        {"name": "Maven", "domain": "maven.com"},
        {"name": "Headspace", "domain": "headspace.com"},
        {"name": "Calm", "domain": "calm.com"},
        
        # EdTech making news
        {"name": "Coursera", "domain": "coursera.org"},
        {"name": "Udemy", "domain": "udemy.com"},
        {"name": "Skillshare", "domain": "skillshare.com"},
        {"name": "MasterClass", "domain": "masterclass.com"},
        {"name": "Khan_Academy", "domain": "khanacademy.org"},
        {"name": "Duolingo", "domain": "duolingo.com"},
        
        # Fintech darlings in news
        {"name": "Stripe", "domain": "stripe.com"},
        {"name": "Plaid", "domain": "plaid.com"},
        {"name": "Square", "domain": "squareup.com"},
        {"name": "PayPal", "domain": "paypal.com"},
        {"name": "Venmo", "domain": "venmo.com"},
        {"name": "Zelle", "domain": "zellepay.com"},
        
        # B2B SaaS frequently mentioned
        {"name": "Salesforce", "domain": "salesforce.com"},
        {"name": "HubSpot", "domain": "hubspot.com"},
        {"name": "Zendesk", "domain": "zendesk.com"},
        {"name": "Intercom", "domain": "intercom.com"},
        {"name": "Segment", "domain": "segment.com"},
        {"name": "Twilio", "domain": "twilio.com"},
        
        # Data and analytics in headlines
        {"name": "Snowflake", "domain": "snowflake.com"},
        {"name": "Databricks", "domain": "databricks.com"},
        {"name": "Palantir", "domain": "palantir.com"},
        {"name": "MongoDB", "domain": "mongodb.com"},
        {"name": "Elasticsearch", "domain": "elastic.co"},
        
        # Cloud infrastructure newsworthy
        {"name": "DigitalOcean", "domain": "digitalocean.com"},
        {"name": "Linode", "domain": "linode.com"},
        {"name": "Vultr", "domain": "vultr.com"},
        {"name": "PlanetScale", "domain": "planetscale.com"},
        {"name": "Neon", "domain": "neon.tech"},
        
        # Security companies in spotlight
        {"name": "CrowdStrike", "domain": "crowdstrike.com"},
        {"name": "SentinelOne", "domain": "sentinelone.com"},
        {"name": "Okta", "domain": "okta.com"},
        {"name": "Auth0", "domain": "auth0.com"},
        {"name": "1Password", "domain": "1password.com"},
        
        # Development tools trending
        {"name": "GitHub", "domain": "github.com"},
        {"name": "GitLab", "domain": "gitlab.com"},
        {"name": "JetBrains", "domain": "jetbrains.com"},
        {"name": "Docker", "domain": "docker.com"},
        {"name": "Kubernetes", "domain": "kubernetes.io"},
        
        # Marketing tech in news
        {"name": "Shopify", "domain": "shopify.com"},
        {"name": "WooCommerce", "domain": "woocommerce.com"},
        {"name": "BigCommerce", "domain": "bigcommerce.com"},
        {"name": "Magento", "domain": "magento.com"},
        {"name": "Squarespace", "domain": "squarespace.com"},
        {"name": "Wix", "domain": "wix.com"}
    ]

def download_logo(company: Dict, output_dir: str) -> bool:
    """Download individual company logo"""
    company_name = company['name']
    domain = company['domain']
    
    clearbit_url = f"https://logo.clearbit.com/{domain}"
    
    try:
        print(f"Downloading {company_name} ({domain})...")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        
        response = requests.get(clearbit_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
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
    """Main function"""
    output_dir = "additional_newsworthy"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    
    companies = get_additional_newsworthy_companies()
    
    print(f"Starting download of {len(companies)} additional newsworthy companies...")
    print(f"Output directory: {output_dir}")
    print("="*60)
    
    successful = 0
    failed = 0
    
    for i, company in enumerate(companies, 1):
        print(f"\n[{i}/{len(companies)}] ", end="")
        success = download_logo(company, output_dir)
        
        if success:
            successful += 1
        else:
            failed += 1
        
        # Small delay to be respectful
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print("DOWNLOAD COMPLETE")
    print(f"{'='*60}")
    print(f"Total processed: {len(companies)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")
    print(f"Success rate: {(successful/len(companies)*100):.1f}%")
    print(f"Files saved in: {output_dir}/")

if __name__ == "__main__":
    main()