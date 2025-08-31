#!/usr/bin/env python3
"""
ULTIMATE logo downloader - Maximum aggressive parallel downloading
"""

import os
import json
import time
import requests
import concurrent.futures
from typing import List, Dict, Tuple
from datetime import datetime
import threading
import glob

# AGGRESSIVE Configuration
MAX_WORKERS = 30  # Maximum parallelization
RATE_LIMIT_DELAY = 0.01  # Minimal delay
TIMEOUT = 5  # Faster timeout
BATCH_SIZE = 50  # Process in batches

rate_limiter = threading.Semaphore(MAX_WORKERS)
last_request_time = threading.Lock()
last_time = [0]

def load_existing_logos() -> set:
    """Load all existing logos"""
    existing = set()
    logo_dirs = [
        '/Users/adi/code/socratify/socratify-yolo/logos/all_unique_logos/',
        '/Users/adi/code/socratify/socratify-yolo/logos/downloads_20250807_175600/',
        '/Users/adi/code/socratify/socratify-yolo/logos/verified_downloads_20250807_184645/',
        '/Users/adi/code/socratify/socratify-yolo/logos/final_downloads_20250807_190319/',
        '/Users/adi/code/socratify/socratify-yolo/logos/institutional_logos_20250807_191623/',
        '/Users/adi/code/socratify/socratify-yolo/logos/massive_downloads_20250807_192116/'
    ]
    
    for directory in logo_dirs:
        if os.path.exists(directory):
            for file in glob.glob(os.path.join(directory, '**/*'), recursive=True):
                if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico')):
                    basename = os.path.basename(file).lower()
                    name = basename.replace('.png', '').replace('.jpg', '').replace('.svg', '')
                    name = name.replace('_', ' ').replace('-', ' ')
                    existing.add(name)
                    # Also add without spaces
                    existing.add(name.replace(' ', ''))
    
    return existing

def sanitize_filename(name: str) -> str:
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        name = name.replace(char, '')
    name = name.replace(' ', '_').replace('&', 'and').replace('.', '').replace("'", '')
    return name[:100]

def rate_limited_request():
    with last_request_time:
        current_time = time.time()
        time_since_last = current_time - last_time[0]
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        last_time[0] = time.time()

def get_aggressive_domain_variations(company_name: str, category: str) -> List[str]:
    """Generate aggressive domain variations"""
    clean = company_name.lower().replace(' ', '').replace('.', '').replace("'", '').replace('&', 'and')
    dash = company_name.lower().replace(' ', '-').replace('.', '').replace("'", '').replace('&', 'and')
    underscore = company_name.lower().replace(' ', '_').replace('.', '').replace("'", '').replace('&', 'and')
    
    # Get first word
    first = company_name.split()[0].lower() if ' ' in company_name else clean
    
    variations = []
    
    # Category-specific patterns
    if 'Web3' in category or 'Crypto' in category or 'DeFi' in category or 'NFT' in category:
        extensions = ['.io', '.xyz', '.fi', '.finance', '.exchange', '.protocol', '.network', '.chain', '.eth']
        for base in [clean, dash, first]:
            for ext in extensions:
                variations.append(base + ext)
    
    elif 'Creator' in category or 'Gig' in category:
        for base in [clean, dash]:
            variations.extend([
                f"{base}.com", f"{base}.io", f"{base}.co", f"{base}.app",
                f"get{base}.com", f"join{base}.com", f"my{base}.com"
            ])
    
    elif 'Gaming' in category or 'Esports' in category:
        for base in [clean, dash, first]:
            variations.extend([
                f"{base}.com", f"{base}.gg", f"{base}.tv", f"{base}.live",
                f"{base}gaming.com", f"{base}esports.com", f"team{base}.com"
            ])
    
    elif 'Union' in category or 'Labor' in category:
        variations.extend([
            f"{clean}.org", f"{dash}.org", f"{clean}union.org",
            f"{clean}.union", f"local{clean}.org"
        ])
    
    elif 'Cannabis' in category:
        for base in [clean, dash]:
            variations.extend([
                f"{base}.com", f"{base}.co", f"{base}cannabis.com",
                f"{base}dispensary.com", f"get{base}.com"
            ])
    
    elif 'Dating' in category:
        for base in [clean, dash]:
            variations.extend([
                f"{base}.com", f"{base}.dating", f"{base}app.com",
                f"meet{base}.com", f"find{base}.com"
            ])
    
    # Standard variations for all
    variations.extend([
        f"{clean}.com", f"{dash}.com", f"{underscore}.com",
        f"{clean}.net", f"{clean}.org", f"{clean}.co",
        f"{clean}.io", f"{clean}.ai", f"{clean}.app"
    ])
    
    # Remove common suffixes and retry
    for suffix in ['inc', 'corp', 'llc', 'ltd', 'group', 'company']:
        if suffix in clean:
            base = clean.replace(suffix, '').strip()
            if base:
                variations.append(f"{base}.com")
    
    # Unique only
    seen = set()
    unique = []
    for v in variations:
        if v not in seen and len(v) > 5:
            seen.add(v)
            unique.append(v)
    
    return unique[:20]  # More attempts

def download_logo_aggressive(company_info: Tuple[str, str], output_dir: str, existing_logos: set) -> Dict:
    """Aggressively download logo with multiple strategies"""
    company_name, category = company_info
    
    # Quick check if exists
    check_name = sanitize_filename(company_name).lower().replace('_', ' ')
    if check_name in existing_logos or check_name.replace(' ', '') in existing_logos:
        return {
            'company': company_name,
            'category': category,
            'success': False,
            'skipped': True
        }
    
    result = {
        'company': company_name,
        'category': category,
        'success': False,
        'error': None,
        'skipped': False
    }
    
    try:
        domains = get_aggressive_domain_variations(company_name, category)
        
        # Try multiple services in parallel
        for domain in domains:
            # Clearbit
            try:
                rate_limited_request()
                response = requests.get(
                    f"https://logo.clearbit.com/{domain}",
                    timeout=TIMEOUT,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                if response.status_code == 200 and len(response.content) > 800:
                    filename = f"{sanitize_filename(company_name)}.png"
                    file_path = os.path.join(output_dir, category.replace(' ', '_'), filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    result['success'] = True
                    result['source'] = 'clearbit'
                    return result
            except:
                pass
            
            # Google Favicon (parallel attempt)
            if len(domains) > 5 and domains.index(domain) < 5:
                try:
                    rate_limited_request()
                    response = requests.get(
                        f"https://www.google.com/s2/favicons?domain={domain}&sz=256",
                        timeout=3
                    )
                    if response.status_code == 200 and len(response.content) > 400:
                        filename = f"{sanitize_filename(company_name)}_favicon.png"
                        file_path = os.path.join(output_dir, category.replace(' ', '_'), filename)
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        result['success'] = True
                        result['source'] = 'google'
                        return result
                except:
                    pass
        
        result['error'] = 'No logo found'
        
    except Exception as e:
        result['error'] = str(e)[:50]
    
    return result

def process_batch_ultra_parallel(batch: List[Tuple[str, str]], output_dir: str, existing_logos: set, batch_num: int) -> List[Dict]:
    """Process batch with ultra parallelization"""
    results = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [
            executor.submit(download_logo_aggressive, company, output_dir, existing_logos)
            for company in batch
        ]
        
        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            try:
                result = future.result(timeout=10)
                results.append(result)
                
                if i % 10 == 0:
                    success = sum(1 for r in results if r.get('success'))
                    skipped = sum(1 for r in results if r.get('skipped'))
                    print(f"    Batch {batch_num}: {i}/{len(batch)} | ✅ {success} | ⏭️ {skipped}")
            except:
                results.append({'success': False, 'error': 'timeout'})
    
    return results

def main():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"/Users/adi/code/socratify/socratify-yolo/logos/ultimate_downloads_{timestamp}"
    
    print("🚀 ULTIMATE LOGO DOWNLOAD - MAXIMUM AGGRESSION MODE")
    print("="*60)
    
    print("Loading existing logos...")
    existing_logos = load_existing_logos()
    print(f"Found {len(existing_logos)} existing logos\n")
    
    print("Loading ultimate company list...")
    companies = {}
    current_category = "General"
    
    with open('/Users/adi/code/socratify/socratify-yolo/logos/ultimate_missing_list.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('##'):
                current_category = line.replace('##', '').strip()
                if current_category not in companies:
                    companies[current_category] = []
            elif line and not line.startswith('#'):
                companies[current_category].append(line)
    
    # Flatten
    all_companies = []
    for category, company_list in companies.items():
        for company in company_list:
            all_companies.append((company, category))
    
    print(f"Total companies to process: {len(all_companies)}")
    print(f"Output: {output_dir}")
    print(f"Workers: {MAX_WORKERS} parallel threads")
    print("="*60 + "\n")
    
    all_results = []
    
    # Process in batches for better progress tracking
    for i in range(0, len(all_companies), BATCH_SIZE):
        batch = all_companies[i:i+BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (len(all_companies) + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"📦 Processing Batch {batch_num}/{total_batches} ({len(batch)} companies)")
        
        batch_results = process_batch_ultra_parallel(batch, output_dir, existing_logos, batch_num)
        all_results.extend(batch_results)
        
        # Quick stats
        total_success = sum(1 for r in all_results if r.get('success'))
        total_skipped = sum(1 for r in all_results if r.get('skipped'))
        total_failed = len(all_results) - total_success - total_skipped
        
        print(f"   Cumulative: ✅ {total_success} | ⏭️ {total_skipped} | ❌ {total_failed}\n")
    
    # Final report
    successful = [r for r in all_results if r.get('success')]
    skipped = [r for r in all_results if r.get('skipped')]
    failed = [r for r in all_results if not r.get('success') and not r.get('skipped')]
    
    # Save report
    report_path = os.path.join(output_dir, 'ultimate_report.json')
    with open(report_path, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total': len(all_results),
            'successful': len(successful),
            'skipped': len(skipped),
            'failed': len(failed),
            'success_rate': f"{(len(successful)/(len(successful)+len(failed))*100):.1f}%" if (successful or failed) else "0%"
        }, f, indent=2)
    
    print("\n" + "="*60)
    print("🏁 ULTIMATE DOWNLOAD COMPLETE!")
    print(f"Total processed: {len(all_results)}")
    print(f"✅ NEW LOGOS: {len(successful)}")
    print(f"⏭️ Already existed: {len(skipped)}")
    print(f"❌ Failed: {len(failed)}")
    print(f"\n🏆 FINAL COLLECTION:")
    print(f"Previous: ~6,400 logos")
    print(f"Added: {len(successful)} new logos")
    print(f"TOTAL: ~{6400 + len(successful)} LOGOS!")
    print("="*60)

if __name__ == "__main__":
    main()