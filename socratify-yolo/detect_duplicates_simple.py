#!/usr/bin/env python3
"""
Simple duplicate detection based on file hash and name matching
No external dependencies required
"""

import os
import shutil
import hashlib
from collections import defaultdict
import json
from datetime import datetime

# Logo directories to check
LOGO_DIRECTORIES = [
    'logos/downloaded',
    'logos/global_mba_logos',
    'logos/institution_logos',
    'logos/business_school_logos',
    'logos/comprehensive_fix',
    'logos/expanded_business_schools',
    'logos/employers_2025',
    'logos/comprehensive_global',
    'logos/final_expansion',
    'logos/ultimate_final',
    'logos/final_supplementary'
]

# Directory for duplicates
DUPLICATES_DIR = 'logos/duplicates'

# Known company variations - comprehensive list
COMPANY_VARIATIONS = {
    # Tech companies
    'google': ['google', 'alphabet', 'google_inc', 'alphabet_inc'],
    'facebook': ['facebook', 'meta', 'meta_platforms', 'facebook_inc'],
    'microsoft': ['microsoft', 'microsoft_corporation', 'msft'],
    'amazon': ['amazon', 'amazon_com', 'aws', 'amazon_web_services'],
    'apple': ['apple', 'apple_inc', 'apple_computer'],
    
    # Consulting
    'mckinsey': ['mckinsey', 'mckinsey_and_company', 'mckinsey_company'],
    'bcg': ['bcg', 'boston_consulting_group', 'boston_consulting'],
    'bain': ['bain', 'bain_and_company', 'bain_company'],
    'deloitte': ['deloitte', 'deloitte_touche', 'deloitte_consulting'],
    'pwc': ['pwc', 'pricewaterhousecoopers', 'price_waterhouse_coopers'],
    'ey': ['ey', 'ernst_young', 'ernst_and_young'],
    'kpmg': ['kpmg', 'kpmg_international'],
    
    # Banks
    'jpmorgan': ['jpmorgan', 'jp_morgan', 'jpmorgan_chase', 'jpm', 'chase'],
    'goldman': ['goldman', 'goldman_sachs', 'gs'],
    'morgan_stanley': ['morgan_stanley', 'morganstanley', 'ms'],
    'citi': ['citi', 'citibank', 'citigroup', 'citicorp'],
    'bofa': ['bofa', 'bank_of_america', 'bankofamerica', 'boa'],
    
    # Airlines variations
    'american_airlines': ['american_airlines', 'american', 'aa'],
    'united': ['united', 'united_airlines', 'ual'],
    'delta': ['delta', 'delta_air_lines', 'delta_airlines'],
    
    # Other common variations
    '3m': ['3m', 'three_m', 'mmm'],
    'ge': ['ge', 'general_electric', 'generalelectric'],
    'pg': ['pg', 'procter_gamble', 'procter_and_gamble', 'pandg'],
    'jnj': ['jnj', 'johnson_johnson', 'johnson_and_johnson', 'jandj'],
    'att': ['att', 'at_t', 'at_and_t'],
}

def get_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def normalize_company_name(filename):
    """Normalize company name for comparison"""
    # Remove extension and lowercase
    name = filename.lower()
    for ext in ['.png', '.jpg', '.jpeg', '.svg', '.gif']:
        name = name.replace(ext, '')
    
    # Replace common separators with underscore
    name = name.replace('-', '_').replace(' ', '_').replace('.', '_').replace('&', 'and')
    
    # Remove common suffixes
    suffixes = ['_logo', '_inc', '_corp', '_corporation', '_limited', '_ltd', '_llc', '_plc', '_ag', '_sa', '_gmbh', '_co']
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    
    # Check if it's a known variation
    for canonical, variations in COMPANY_VARIATIONS.items():
        if name in variations:
            return canonical
    
    return name

def analyze_duplicates():
    """Analyze duplicates without moving files"""
    print("=" * 80)
    print("DUPLICATE ANALYSIS")
    print("=" * 80)
    
    all_files = []
    
    # Collect all files
    print("\nScanning directories...")
    for dir_path in LOGO_DIRECTORIES:
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')):
                    filepath = os.path.join(dir_path, filename)
                    filesize = os.path.getsize(filepath)
                    all_files.append({
                        'path': filepath,
                        'name': filename,
                        'dir': dir_path,
                        'size': filesize,
                        'normalized': normalize_company_name(filename)
                    })
    
    print(f"Found {len(all_files)} total logo files")
    
    # 1. Find exact duplicates by file hash
    print("\n1. Analyzing exact duplicates (identical files)...")
    exact_duplicates = defaultdict(list)
    file_hashes = {}
    
    for file_info in all_files:
        file_hash = get_file_hash(file_info['path'])
        if file_hash:
            file_info['hash'] = file_hash
            exact_duplicates[file_hash].append(file_info)
    
    # Filter to only groups with duplicates
    exact_duplicates = {k: v for k, v in exact_duplicates.items() if len(v) > 1}
    
    # 2. Find name-based duplicates
    print("\n2. Analyzing name-based duplicates...")
    name_duplicates = defaultdict(list)
    
    for file_info in all_files:
        normalized = file_info['normalized']
        name_duplicates[normalized].append(file_info)
    
    # Filter to only groups with duplicates
    name_duplicates = {k: v for k, v in name_duplicates.items() if len(v) > 1}
    
    # Calculate statistics
    exact_count = sum(len(files) - 1 for files in exact_duplicates.values())
    name_count = sum(len(files) - 1 for files in name_duplicates.values())
    
    # Show detailed results
    print("\n" + "=" * 80)
    print("ANALYSIS RESULTS")
    print("=" * 80)
    
    print(f"\nEXACT DUPLICATES: {exact_count} duplicate files in {len(exact_duplicates)} groups")
    if exact_duplicates:
        print("\nTop 10 exact duplicate groups:")
        for i, (hash_val, files) in enumerate(list(exact_duplicates.items())[:10]):
            print(f"\n  Group {i+1} ({len(files)} files):")
            for f in files:
                print(f"    - {f['dir']}/{f['name']} ({f['size']:,} bytes)")
    
    print(f"\n\nNAME-BASED DUPLICATES: {name_count} potential duplicates in {len(name_duplicates)} groups")
    if name_duplicates:
        print("\nTop 10 name-based duplicate groups:")
        for i, (name, files) in enumerate(list(name_duplicates.items())[:10]):
            if len(files) > 1:
                print(f"\n  '{name}' ({len(files)} files):")
                for f in files:
                    print(f"    - {f['dir']}/{f['name']} ({f['size']:,} bytes)")
    
    # Save detailed report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_files': len(all_files),
        'exact_duplicates_count': exact_count,
        'name_duplicates_count': name_count,
        'exact_duplicate_groups': len(exact_duplicates),
        'name_duplicate_groups': len(name_duplicates),
        'exact_duplicates': {},
        'name_duplicates': {}
    }
    
    # Add details to report
    for hash_val, files in exact_duplicates.items():
        report['exact_duplicates'][hash_val] = [
            {'path': f['path'], 'size': f['size']} for f in files
        ]
    
    for name, files in name_duplicates.items():
        if len(files) > 1:
            report['name_duplicates'][name] = [
                {'path': f['path'], 'size': f['size']} for f in files
            ]
    
    # Save report
    os.makedirs('logos', exist_ok=True)
    report_path = 'logos/duplicate_analysis_report.json'
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n\nDetailed report saved to: {report_path}")
    
    return exact_duplicates, name_duplicates

def move_duplicates_interactive(exact_duplicates, name_duplicates):
    """Interactively move duplicates to organized folders"""
    print("\n" + "=" * 80)
    print("DUPLICATE MANAGEMENT")
    print("=" * 80)
    
    response = input("\nWould you like to move duplicates to organized folders? (y/n): ")
    if response.lower() != 'y':
        print("No files moved.")
        return
    
    # Create duplicate directories
    os.makedirs(DUPLICATES_DIR, exist_ok=True)
    exact_dir = os.path.join(DUPLICATES_DIR, 'exact_duplicates')
    name_dir = os.path.join(DUPLICATES_DIR, 'name_duplicates')
    os.makedirs(exact_dir, exist_ok=True)
    os.makedirs(name_dir, exist_ok=True)
    
    moved_count = 0
    
    # Directory priority (newer directories have higher priority)
    dir_priority = {dir_path: i for i, dir_path in enumerate(LOGO_DIRECTORIES)}
    
    # Move exact duplicates
    print("\nMoving exact duplicates...")
    for hash_val, files in exact_duplicates.items():
        if len(files) > 1:
            # Keep the one from the newest directory or largest size
            files_sorted = sorted(files, key=lambda x: (dir_priority.get(x['dir'], 0), x['size']), reverse=True)
            keep = files_sorted[0]
            
            print(f"\nKeeping: {keep['dir']}/{keep['name']}")
            
            for f in files_sorted[1:]:
                # Create unique filename
                new_name = f"{f['dir'].replace('/', '_')}_{f['name']}"
                new_path = os.path.join(exact_dir, new_name)
                
                try:
                    shutil.move(f['path'], new_path)
                    print(f"  Moved: {f['path']} -> {new_path}")
                    moved_count += 1
                except Exception as e:
                    print(f"  Error moving {f['path']}: {e}")
    
    # Move name-based duplicates (more conservative)
    print("\nMoving name-based duplicates...")
    for name, files in name_duplicates.items():
        if len(files) > 1:
            # Only move if files are very similar in size
            files_sorted = sorted(files, key=lambda x: (dir_priority.get(x['dir'], 0), x['size']), reverse=True)
            keep = files_sorted[0]
            
            similar_files = []
            for f in files_sorted[1:]:
                size_ratio = f['size'] / keep['size'] if keep['size'] > 0 else 1
                if 0.8 <= size_ratio <= 1.2:  # Within 20% size difference
                    similar_files.append(f)
            
            if similar_files:
                print(f"\nKeeping: {keep['dir']}/{keep['name']} for '{name}'")
                
                for f in similar_files:
                    new_name = f"{f['dir'].replace('/', '_')}_{f['name']}"
                    new_path = os.path.join(name_dir, new_name)
                    
                    try:
                        shutil.move(f['path'], new_path)
                        print(f"  Moved: {f['path']} -> {new_path}")
                        moved_count += 1
                    except Exception as e:
                        print(f"  Error moving {f['path']}: {e}")
    
    print(f"\n\nMoved {moved_count} duplicate files to {DUPLICATES_DIR}")

def main():
    # First analyze
    exact_duplicates, name_duplicates = analyze_duplicates()
    
    # Then offer to move
    if exact_duplicates or name_duplicates:
        move_duplicates_interactive(exact_duplicates, name_duplicates)
    else:
        print("\nNo duplicates found!")

if __name__ == "__main__":
    main()