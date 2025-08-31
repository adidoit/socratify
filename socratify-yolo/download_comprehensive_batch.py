#!/usr/bin/env python3
"""
Batch version of comprehensive logo download - processes in smaller chunks to avoid timeouts
"""

import os
import json
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from typing import Dict, List, Tuple, Optional

# Create output directory
OUTPUT_DIR = 'logos/comprehensive_fix'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Check what's already downloaded
existing_logos = set()
if os.path.exists(OUTPUT_DIR):
    existing_logos = {f.split('_')[0] for f in os.listdir(OUTPUT_DIR) if f.endswith(('.png', '.jpg', '.svg'))}

def clean_company_name(name: str) -> List[str]:
    """Generate multiple variations of company names for better matching."""
    variations = []
    
    # Original name
    variations.append(name)
    
    # Replace & with and
    if '&' in name:
        variations.append(name.replace('&', 'and'))
        variations.append(name.replace(' & ', ''))
    
    # Common abbreviations for special cases
    special_cases = {
        'Goldman Sachs & Company': ['goldmansachs.com', 'gs.com'],
        'Ernst & Young': ['ey.com'],
        'Alvarez & Marsal': ['alvarezandmarsal.com'],
        'PwC Strategy&': ['strategyand.pwc.com', 'pwc.com'],
        'Eli Lilly & Company': ['lilly.com'],
        'H&M': ['hm.com', 'hennes-mauritz.com'],
        'Larsen & Toubro': ['larsentoubro.com', 'lntinfotech.com'],
        'Mahindra & Mahindra': ['mahindra.com'],
        'Marks & Spencer': ['marksandspencer.com'],
        'Pratt & Whitney': ['prattwhitney.com'],
        'Legal & General': ['legalandgeneral.com'],
        'Moelis & Company': ['moelis.com'],
        'Hellman & Friedman': ['hf.com'],
        'Take-Two Interactive': ['take2games.com'],
        'Toronto-Dominion Bank': ['td.com']
    }
    
    if name in special_cases:
        variations.extend(special_cases[name])
    
    # Basic variations
    clean = name.lower().replace(' ', '').replace('&', 'and').replace('-', '')
    variations.append(clean)
    
    return variations[:5]  # Limit variations

def download_logo_simple(name: str) -> Optional[Dict]:
    """Simple, fast logo download."""
    
    # Skip if already downloaded
    if name.replace(' ', '') in existing_logos:
        return {
            'name': name,
            'status': 'already_exists',
            'method': 'cached'
        }
    
    variations = clean_company_name(name)
    
    # Try Clearbit first (most reliable)
    for variation in variations:
        try:
            # Add .com if no domain
            if '.' not in variation:
                variation = f"{variation}.com"
            
            url = f"https://logo.clearbit.com/{urllib.parse.quote(variation)}"
            response = requests.get(url, timeout=3)
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                filename = f"{name.replace('/', '_').replace(' ', '_')}_clearbit.png"
                filepath = os.path.join(OUTPUT_DIR, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return {
                    'name': name,
                    'status': 'success',
                    'method': f"clearbit_{variation}",
                    'filename': filename
                }
        except:
            continue
    
    return {
        'name': name,
        'status': 'failed',
        'error': 'All attempts failed'
    }

def main():
    # Load all targets
    all_targets = []
    
    # Fixable failures
    with open('logos/fixable_failures.txt', 'r') as f:
        all_targets.extend([line.strip() for line in f if line.strip()])
    
    # Missing schools
    if os.path.exists('logos/truly_missing_business_schools.txt'):
        with open('logos/truly_missing_business_schools.txt', 'r') as f:
            all_targets.extend([line.strip() for line in f if line.strip()])
    
    # Remove duplicates
    all_targets = list(set(all_targets))
    
    print(f"Total targets: {len(all_targets)}")
    print(f"Already downloaded: {len(existing_logos)}")
    
    # Process in batches of 50
    batch_size = 50
    all_results = []
    
    for batch_start in range(0, len(all_targets), batch_size):
        batch_end = min(batch_start + batch_size, len(all_targets))
        batch = all_targets[batch_start:batch_end]
        
        print(f"\nProcessing batch {batch_start//batch_size + 1}/{(len(all_targets) + batch_size - 1)//batch_size}")
        
        batch_results = []
        successful = 0
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(download_logo_simple, name): name for name in batch}
            
            for future in as_completed(futures):
                result = future.result()
                batch_results.append(result)
                
                if result['status'] == 'success':
                    successful += 1
                    print(f"  ✓ {result['name']}")
                elif result['status'] == 'already_exists':
                    print(f"  ◆ {result['name']} (already exists)")
                else:
                    print(f"  ✗ {result['name']}")
        
        all_results.extend(batch_results)
        
        # Save intermediate results
        with open('logos/comprehensive_batch_results.json', 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print(f"Batch complete: {successful} new downloads")
        
        # Small delay between batches
        if batch_end < len(all_targets):
            time.sleep(2)
    
    # Final summary
    total_success = sum(1 for r in all_results if r['status'] == 'success')
    total_exists = sum(1 for r in all_results if r['status'] == 'already_exists')
    total_failed = sum(1 for r in all_results if r['status'] == 'failed')
    
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Total processed: {len(all_results)}")
    print(f"New downloads: {total_success}")
    print(f"Already existed: {total_exists}")
    print(f"Failed: {total_failed}")
    print(f"Success rate (new): {total_success/(total_success + total_failed)*100:.1f}%")
    
    # List remaining failures
    still_failed = [r['name'] for r in all_results if r['status'] == 'failed']
    if still_failed:
        print(f"\n=== STILL FAILED ({len(still_failed)}) ===")
        for name in still_failed[:20]:
            print(f"  • {name}")
        if len(still_failed) > 20:
            print(f"  ... and {len(still_failed) - 20} more")
        
        # Save failures
        with open('logos/final_failures.txt', 'w') as f:
            for name in still_failed:
                f.write(f"{name}\n")

if __name__ == "__main__":
    main()