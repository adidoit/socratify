#!/usr/bin/env python3
import csv
import os
import requests
import time
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Thread-safe counter
download_counter = threading.Lock()
stats = {'downloaded': 0, 'exists': 0, 'failed': 0}

def clean_filename(name):
    """Clean company name for filename"""
    clean = name.replace('&amp;', 'and').replace('&', 'and')
    clean = re.sub(r'[^\w\s-]', '', clean)
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean.strip('_')

def try_download(company_name):
    """Try to download from clearbit"""
    # Simple domain generation
    clean = company_name.lower()
    clean = re.sub(r'[^\w\s]', '', clean)
    words = clean.split()
    
    if not words:
        return None
    
    # Try a few domain variations
    domains = []
    
    # First word
    if len(words[0]) > 2:
        domains.append(f"{words[0]}.com")
    
    # All words combined
    combined = ''.join(words)
    if len(combined) < 25:
        domains.append(f"{combined}.com")
    
    # Try each domain
    for domain in domains[:3]:
        try:
            url = f"https://logo.clearbit.com/{domain}"
            response = requests.get(url, timeout=2)
            if response.status_code == 200 and len(response.content) > 100:
                return response.content
        except:
            pass
    
    return None

def process_company(company, existing_logos, output_dir):
    """Process a single company"""
    name = company['name']
    rank = company['rank']
    
    # Quick check if exists
    clean_name = name.lower().replace(' ', '').replace('&', '')
    for logo in existing_logos:
        if clean_name in logo or logo in clean_name:
            with download_counter:
                stats['exists'] += 1
            return {'name': name, 'rank': rank, 'status': 'exists'}
    
    # Try to download
    logo_data = try_download(name)
    
    if logo_data:
        filename = f"{clean_filename(name)}.png"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'wb') as f:
                f.write(logo_data)
            
            with download_counter:
                stats['downloaded'] += 1
            
            return {'name': name, 'rank': rank, 'status': 'downloaded'}
        except:
            pass
    
    with download_counter:
        stats['failed'] += 1
    
    return {'name': name, 'rank': rank, 'status': 'failed'}

def main():
    print("="*80)
    print("PARALLEL DOWNLOAD OF ALL COMPANY LOGOS")
    print("="*80)
    
    # Read companies
    print("\n1. Reading companies...")
    companies = []
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append({
                'name': row['Name'],
                'rank': int(row['Rank']),
                'country': row['country']
            })
    
    print(f"   Total companies: {len(companies):,}")
    
    # Get existing logos (simplified)
    print("\n2. Checking existing logos...")
    logos_path = '../socratify-images/logos/images/companies/'
    existing_logos = set()
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            existing_logos.add(filename[:-4].lower().replace('_', ''))
    
    print(f"   Current logos: {len(os.listdir(logos_path)):,}")
    
    # Create output dir
    output_dir = 'parallel_download'
    os.makedirs(output_dir, exist_ok=True)
    
    # Process with thread pool
    print("\n3. Downloading logos (parallel processing)...")
    print("   This will take several minutes...")
    
    max_workers = 10  # Reasonable parallel downloads
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        futures = []
        for company in companies:
            future = executor.submit(process_company, company, existing_logos, output_dir)
            futures.append(future)
        
        # Process as they complete
        for i, future in enumerate(as_completed(futures), 1):
            result = future.result()
            results.append(result)
            
            # Print progress every 100 companies
            if i % 100 == 0:
                print(f"   Processed {i:,}/{len(companies):,} - Downloaded: {stats['downloaded']}, Exists: {stats['exists']}, Failed: {stats['failed']}")
            
            # Save progress periodically
            if i % 500 == 0:
                with open('parallel_progress.json', 'w') as f:
                    json.dump(stats, f)
    
    # Final results
    print("\n" + "="*80)
    print("COMPLETE!")
    print("="*80)
    print(f"Total companies: {len(companies):,}")
    print(f"✅ Already had: {stats['exists']:,}")
    print(f"✅ Downloaded: {stats['downloaded']:,}")
    print(f"❌ Failed: {stats['failed']:,}")
    
    total_logos = stats['exists'] + stats['downloaded']
    coverage = total_logos / len(companies) * 100
    
    print(f"\nTotal coverage: {total_logos:,} / {len(companies):,} ({coverage:.1f}%)")
    
    if stats['downloaded'] > 0:
        print(f"\n📁 Downloaded {stats['downloaded']:,} new logos to: {output_dir}/")
        print("To move to main folder:")
        print(f"  cp {output_dir}/*.png ../socratify-images/logos/images/companies/")
    
    # Save complete results
    with open('parallel_results.json', 'w') as f:
        json.dump({
            'stats': stats,
            'total_companies': len(companies),
            'coverage_percent': coverage
        }, f, indent=2)

if __name__ == "__main__":
    main()