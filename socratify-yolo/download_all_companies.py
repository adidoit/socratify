#!/usr/bin/env python3
import csv
import os
import requests
import time
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_filename(name):
    """Clean company name for filename"""
    clean = name.replace('&amp;', 'and').replace('&', 'and')
    clean = re.sub(r'[^\w\s-]', '', clean)
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean.strip('_')

def normalize_for_check(name):
    """Normalize name for checking if logo exists"""
    clean = name.lower()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    clean = ' '.join(clean.split())
    return clean

def get_domain_options(company_name):
    """Generate possible domains for a company"""
    clean = company_name.lower()
    clean = re.sub(r'[^\w\s]', '', clean)
    words = clean.split()
    
    domains = []
    
    # Try various combinations
    if words:
        # First word
        if len(words[0]) > 2:
            domains.append(f"{words[0]}.com")
        
        # All words together
        joined = ''.join(words)
        if len(joined) < 30:
            domains.extend([
                f"{joined}.com",
                f"{joined}.net",
                f"{joined}.org",
                f"{joined}.io"
            ])
        
        # First two words
        if len(words) > 1:
            two_words = words[0] + words[1]
            if len(two_words) < 20:
                domains.append(f"{two_words}.com")
        
        # Acronym for long names
        if len(words) > 2:
            acronym = ''.join([w[0] for w in words if len(w) > 2])
            if 2 < len(acronym) < 10:
                domains.append(f"{acronym}.com")
    
    return domains[:5]  # Limit to 5 attempts

def download_logo(company_name):
    """Try to download a logo"""
    domains = get_domain_options(company_name)
    
    for domain in domains:
        url = f"https://logo.clearbit.com/{domain}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200 and len(response.content) > 100:
                return response.content
        except:
            pass
    
    return None

def process_batch(companies_batch, existing_logos, output_dir):
    """Process a batch of companies"""
    results = []
    
    for company in companies_batch:
        name = company['name']
        rank = company['rank']
        
        # Check if we already have it
        norm_name = normalize_for_check(name)
        exists = False
        
        for logo in existing_logos:
            if norm_name in logo or logo in norm_name:
                exists = True
                break
        
        if exists:
            results.append({'name': name, 'rank': rank, 'status': 'exists'})
            continue
        
        # Try to download
        logo_data = download_logo(name)
        
        if logo_data:
            filename = f"{clean_filename(name)}.png"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(logo_data)
            
            results.append({'name': name, 'rank': rank, 'status': 'downloaded', 'file': filename})
        else:
            results.append({'name': name, 'rank': rank, 'status': 'failed'})
    
    return results

def main():
    print("="*80)
    print("DOWNLOADING ALL MISSING COMPANY LOGOS")
    print("="*80)
    
    # Read ALL companies
    print("\n1. Reading all companies from CSV...")
    all_companies = []
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_companies.append({
                'name': row['Name'],
                'rank': int(row['Rank']),
                'country': row['country']
            })
    
    print(f"   Total companies: {len(all_companies):,}")
    
    # Get existing logos for quick check
    print("\n2. Checking existing logos...")
    logos_path = '../socratify-images/logos/images/companies/'
    existing_logos = set()
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            existing_logos.add(normalize_for_check(filename[:-4]))
    
    print(f"   Current logos: {len(existing_logos):,}")
    
    # Create output directory
    output_dir = 'complete_download'
    os.makedirs(output_dir, exist_ok=True)
    
    # Process in batches
    print("\n3. Processing companies in batches...")
    batch_size = 100
    total_downloaded = 0
    total_exists = 0
    total_failed = 0
    
    all_results = []
    
    for i in range(0, len(all_companies), batch_size):
        batch = all_companies[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(all_companies) + batch_size - 1) // batch_size
        
        print(f"   Batch {batch_num}/{total_batches} (companies {i+1}-{min(i+batch_size, len(all_companies))})...", end='', flush=True)
        
        results = process_batch(batch, existing_logos, output_dir)
        all_results.extend(results)
        
        # Count results
        batch_downloaded = sum(1 for r in results if r['status'] == 'downloaded')
        batch_exists = sum(1 for r in results if r['status'] == 'exists')
        batch_failed = sum(1 for r in results if r['status'] == 'failed')
        
        total_downloaded += batch_downloaded
        total_exists += batch_exists
        total_failed += batch_failed
        
        print(f" Downloaded: {batch_downloaded}, Already have: {batch_exists}, Failed: {batch_failed}")
        
        # Save progress
        if batch_num % 10 == 0:
            with open('download_progress.json', 'w') as f:
                json.dump({
                    'processed': i + len(batch),
                    'total': len(all_companies),
                    'downloaded': total_downloaded,
                    'exists': total_exists,
                    'failed': total_failed
                }, f)
        
        # Rate limiting
        if batch_downloaded > 0:
            time.sleep(2)
    
    # Save final results
    with open('complete_download_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL RESULTS")
    print("="*80)
    print(f"Total companies processed: {len(all_companies):,}")
    print(f"✅ Already had logos: {total_exists:,}")
    print(f"✅ Successfully downloaded: {total_downloaded:,}")
    print(f"❌ Failed to download: {total_failed:,}")
    print(f"\nTotal logos now: {total_exists + total_downloaded:,} / {len(all_companies):,}")
    print(f"Coverage: {(total_exists + total_downloaded) / len(all_companies) * 100:.1f}%")
    
    if total_downloaded > 0:
        print(f"\n📁 New logos saved in: {output_dir}/")
        print("To move to main folder:")
        print(f"  cp {output_dir}/*.png ../socratify-images/logos/images/companies/")
    
    # Show some failed companies
    failed_companies = [r for r in all_results if r['status'] == 'failed']
    if failed_companies:
        print(f"\nSample of companies that need manual download:")
        for company in failed_companies[:20]:
            print(f"  Rank {company['rank']:5d}: {company['name']}")

if __name__ == "__main__":
    main()