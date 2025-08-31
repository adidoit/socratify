#!/usr/bin/env python3
import csv
import os
import time
import requests
from urllib.parse import quote

def clean_company_name(name):
    """Clean company name for filename"""
    return (name.replace(' ', '_')
                .replace('&', 'and')
                .replace('&amp;', 'and')
                .replace('(', '')
                .replace(')', '')
                .replace(',', '')
                .replace('.', '')
                .replace('/', '_')
                .replace('"', '')
                .replace("'", '')
                .replace(':', '')
                .replace('?', '')
                .replace('*', '')
                .replace('<', '')
                .replace('>', '')
                .replace('|', '')
                .replace('\\', ''))

def get_company_variations(company_name):
    """Generate variations of company name for searching"""
    variations = []
    
    # Original name
    variations.append(company_name)
    
    # Remove parenthetical content
    if '(' in company_name:
        base_name = company_name.split('(')[0].strip()
        variations.append(base_name)
    
    # Common variations
    replacements = {
        'United Parcel Service': 'UPS',
        'DHL Group': 'DHL',
        'Deutsche Post': 'DHL',
        'Jingdong Mall': 'JD',
        'JD Logistics': 'JD',
        'UnitedHealth': 'UnitedHealthGroup',
        'Fomento Económico Mexicano': 'FEMSA',
        'FEMSA': 'FEMSA',
        'NTT': 'NTT',
        'Nippon Telegraph & Telephone': 'NTT',
        'Cognizant Technology Solutions': 'Cognizant',
        'Securitas AB': 'Securitas',
        'Foxconn': 'Foxconn',
        'Hon Hai Precision Industry': 'Foxconn',
        'Pepsico': 'Pepsi'
    }
    
    for original, replacement in replacements.items():
        if original.lower() in company_name.lower():
            variations.append(replacement)
    
    # Remove common suffixes
    suffixes = [' Group', ' Corporation', ' Company', ' Inc', ' Limited', ' Ltd', ' AB', ' AG', ' SA', ' NV', ' Holdings']
    for suffix in suffixes:
        if company_name.endswith(suffix):
            variations.append(company_name[:-len(suffix)].strip())
    
    return list(set(variations))  # Remove duplicates

def get_logo_url(company_name):
    """Try to find logo URL using various sources"""
    variations = get_company_variations(company_name)
    
    for variation in variations:
        # Clean variation for URL
        clean_variation = variation.lower().replace(' ', '').replace('&', '')
        
        # Try different domains
        domains = ['.com', '.org', '.net', '.io', '.co']
        
        for domain in domains:
            url = f"https://logo.clearbit.com/{clean_variation}{domain}"
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    return url
            except:
                pass
    
    return None

def download_logo(url, filepath):
    """Download logo from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        if response.status_code == 200 and len(response.content) > 100:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"    Error: {e}")
    return False

def main():
    # Read companies from CSV
    companies_to_download = []
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rank = int(row['Rank'])
            if rank <= 100:  # Top 100 companies
                companies_to_download.append({
                    'rank': rank,
                    'name': row['Name'],
                    'clean_name': clean_company_name(row['Name'])
                })
    
    # Check which logos are missing
    logos_path = '../socratify-images/logos/images/companies/'
    existing_logos = set()
    if os.path.exists(logos_path):
        for filename in os.listdir(logos_path):
            if filename.endswith('.png'):
                existing_logos.add(filename[:-4])
    
    # Also check downloaded logos
    download_dir = 'downloaded_logos'
    if os.path.exists(download_dir):
        for filename in os.listdir(download_dir):
            if filename.endswith('.png'):
                existing_logos.add(filename[:-4])
    
    # Find missing logos
    missing_companies = []
    for company in companies_to_download:
        if company['clean_name'] not in existing_logos:
            missing_companies.append(company)
    
    print(f"Checking top {len(companies_to_download)} companies...")
    print(f"Found {len(missing_companies)} missing logos\n")
    
    # Create download directory
    os.makedirs(download_dir, exist_ok=True)
    
    # Download missing logos
    print("Attempting to download missing logos...")
    downloaded = []
    failed = []
    
    for i, company in enumerate(missing_companies, 1):
        print(f"\n[{i}/{len(missing_companies)}] {company['name']}...")
        
        # Try to find and download logo
        logo_url = get_logo_url(company['name'])
        
        if logo_url:
            print(f"  Found URL: {logo_url}")
            filepath = os.path.join(download_dir, f"{company['clean_name']}.png")
            if download_logo(logo_url, filepath):
                print(f"  ✓ Downloaded: {company['clean_name']}.png")
                downloaded.append(company)
            else:
                print(f"  ✗ Failed to download")
                failed.append(company)
        else:
            print(f"  ✗ No logo URL found")
            failed.append(company)
        
        # Rate limiting
        if i < len(missing_companies):
            time.sleep(0.5)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  Total checked: {len(companies_to_download)} companies")
    print(f"  Already have: {len(companies_to_download) - len(missing_companies)} logos")
    print(f"  Downloaded: {len(downloaded)} new logos")
    print(f"  Failed: {len(failed)} logos")
    
    if downloaded:
        print(f"\n✓ Successfully downloaded {len(downloaded)} logos to '{download_dir}/'")
        print("\nTo move them to the main logos folder, run:")
        print(f"  cp {download_dir}/*.png {logos_path}")
    
    if failed:
        print(f"\n✗ Could not download {len(failed)} logos:")
        for comp in failed[:10]:  # Show first 10
            print(f"  - {comp['name']}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")

if __name__ == "__main__":
    main()