#!/usr/bin/env python3
"""
Intelligent duplicate detection and management system
Identifies duplicates using multiple strategies and moves them to a duplicates folder
"""

import os
import shutil
import hashlib
from PIL import Image
import imagehash
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

# Known company variations
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
    
    # Other common variations
    '3m': ['3m', 'three_m', 'mmm'],
    'ge': ['ge', 'general_electric', 'generalelectric'],
    'pg': ['pg', 'procter_gamble', 'procter_and_gamble', 'pandg'],
    'jnj': ['jnj', 'johnson_johnson', 'johnson_and_johnson', 'jandj'],
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

def get_image_hash(filepath):
    """Calculate perceptual hash of image for visual similarity"""
    try:
        # Use different hash types for better detection
        img = Image.open(filepath)
        
        # Convert to RGB if necessary
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Calculate multiple hash types
        hashes = {
            'average': str(imagehash.average_hash(img)),
            'perceptual': str(imagehash.phash(img)),
            'difference': str(imagehash.dhash(img)),
            'wavelet': str(imagehash.whash(img))
        }
        return hashes
    except:
        return None

def normalize_company_name(filename):
    """Normalize company name for comparison"""
    # Remove extension and lowercase
    name = filename.lower()
    for ext in ['.png', '.jpg', '.jpeg', '.svg', '.gif']:
        name = name.replace(ext, '')
    
    # Replace common separators with underscore
    name = name.replace('-', '_').replace(' ', '_').replace('.', '_')
    
    # Remove common suffixes
    suffixes = ['_logo', '_inc', '_corp', '_corporation', '_limited', '_ltd', '_llc', '_plc', '_ag', '_sa', '_gmbh']
    for suffix in suffixes:
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    
    # Check if it's a known variation
    for canonical, variations in COMPANY_VARIATIONS.items():
        if name in variations:
            return canonical
    
    return name

def find_duplicates():
    """Find duplicates using multiple strategies"""
    print("=" * 80)
    print("INTELLIGENT DUPLICATE DETECTION")
    print("=" * 80)
    
    # Storage for different types of duplicates
    exact_duplicates = defaultdict(list)  # By file hash
    visual_duplicates = defaultdict(list)  # By image similarity
    name_duplicates = defaultdict(list)    # By normalized name
    
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
    
    # 1. Detect exact duplicates by file hash
    print("\n1. Checking for exact duplicates (identical files)...")
    file_hashes = {}
    for file_info in all_files:
        file_hash = get_file_hash(file_info['path'])
        if file_hash:
            file_info['hash'] = file_hash
            if file_hash in file_hashes:
                exact_duplicates[file_hash].append(file_info)
                if len(exact_duplicates[file_hash]) == 2:
                    # Add the first occurrence when we find the second
                    exact_duplicates[file_hash].insert(0, file_hashes[file_hash])
            else:
                file_hashes[file_hash] = file_info
    
    # 2. Detect visual duplicates by image hash (skip SVGs)
    print("\n2. Checking for visual duplicates (similar looking images)...")
    image_hashes = {}
    for file_info in all_files:
        if not file_info['name'].endswith('.svg'):
            img_hashes = get_image_hash(file_info['path'])
            if img_hashes:
                file_info['image_hashes'] = img_hashes
                
                # Check perceptual hash for visual similarity
                phash = img_hashes['perceptual']
                found_similar = False
                
                for existing_hash, existing_file in image_hashes.items():
                    # Calculate Hamming distance
                    distance = sum(c1 != c2 for c1, c2 in zip(phash, existing_hash))
                    if distance <= 5:  # Threshold for similarity
                        visual_duplicates[existing_hash].append(file_info)
                        if len(visual_duplicates[existing_hash]) == 2:
                            visual_duplicates[existing_hash].insert(0, existing_file)
                        found_similar = True
                        break
                
                if not found_similar:
                    image_hashes[phash] = file_info
    
    # 3. Detect name-based duplicates
    print("\n3. Checking for name-based duplicates...")
    name_groups = defaultdict(list)
    for file_info in all_files:
        normalized = file_info['normalized']
        name_groups[normalized].append(file_info)
    
    for normalized, files in name_groups.items():
        if len(files) > 1:
            name_duplicates[normalized] = files
    
    # Remove exact duplicates from visual and name duplicates to avoid double counting
    exact_hash_set = set()
    for hash_val, files in exact_duplicates.items():
        for f in files:
            exact_hash_set.add(f['path'])
    
    # Clean up visual duplicates
    visual_duplicates_clean = {}
    for key, files in visual_duplicates.items():
        cleaned = [f for f in files if f['path'] not in exact_hash_set]
        if len(cleaned) > 1:
            visual_duplicates_clean[key] = cleaned
    
    # Clean up name duplicates
    name_duplicates_clean = {}
    for key, files in name_duplicates.items():
        cleaned = [f for f in files if f['path'] not in exact_hash_set]
        if len(cleaned) > 1:
            name_duplicates_clean[key] = cleaned
    
    return exact_duplicates, visual_duplicates_clean, name_duplicates_clean

def select_best_version(duplicate_group):
    """Select the best version to keep based on multiple criteria"""
    # Criteria for selecting the best version:
    # 1. Prefer newer directories (later in our list = newer)
    # 2. Prefer larger file size (usually better quality)
    # 3. Prefer PNG over JPG over SVG
    # 4. Prefer shorter filenames (usually cleaner)
    
    dir_priority = {dir_path: i for i, dir_path in enumerate(LOGO_DIRECTORIES)}
    
    def score_file(file_info):
        score = 0
        
        # Directory priority (newer is better)
        score += dir_priority.get(file_info['dir'], 0) * 1000
        
        # File size (larger is better, within reason)
        if file_info['size'] < 1000000:  # Less than 1MB
            score += file_info['size'] / 1000
        
        # File type preference
        if file_info['name'].endswith('.png'):
            score += 100
        elif file_info['name'].endswith('.jpg') or file_info['name'].endswith('.jpeg'):
            score += 50
        elif file_info['name'].endswith('.svg'):
            score += 25
        
        # Shorter names are usually cleaner
        score -= len(file_info['name']) * 0.1
        
        return score
    
    # Sort by score (highest first)
    sorted_files = sorted(duplicate_group, key=score_file, reverse=True)
    return sorted_files[0], sorted_files[1:]

def move_duplicates(exact_duplicates, visual_duplicates, name_duplicates):
    """Move duplicates to the duplicates folder"""
    os.makedirs(DUPLICATES_DIR, exist_ok=True)
    
    # Create subdirectories for different types
    exact_dir = os.path.join(DUPLICATES_DIR, 'exact_duplicates')
    visual_dir = os.path.join(DUPLICATES_DIR, 'visual_duplicates')
    name_dir = os.path.join(DUPLICATES_DIR, 'name_duplicates')
    
    os.makedirs(exact_dir, exist_ok=True)
    os.makedirs(visual_dir, exist_ok=True)
    os.makedirs(name_dir, exist_ok=True)
    
    moved_files = set()
    duplicate_report = {
        'timestamp': datetime.now().isoformat(),
        'exact_duplicates': [],
        'visual_duplicates': [],
        'name_duplicates': []
    }
    
    # Process exact duplicates
    print("\nProcessing exact duplicates...")
    for hash_val, files in exact_duplicates.items():
        if len(files) > 1:
            keep, remove = select_best_version(files)
            
            group_info = {
                'kept': f"{keep['dir']}/{keep['name']}",
                'removed': []
            }
            
            for file_to_remove in remove:
                if file_to_remove['path'] not in moved_files:
                    # Create unique filename for duplicate
                    base_name = file_to_remove['name']
                    new_name = f"{file_to_remove['dir'].replace('/', '_')}_{base_name}"
                    new_path = os.path.join(exact_dir, new_name)
                    
                    try:
                        shutil.move(file_to_remove['path'], new_path)
                        moved_files.add(file_to_remove['path'])
                        group_info['removed'].append(f"{file_to_remove['dir']}/{file_to_remove['name']}")
                        print(f"  Moved: {file_to_remove['name']} -> exact_duplicates/")
                    except Exception as e:
                        print(f"  Error moving {file_to_remove['name']}: {e}")
            
            if group_info['removed']:
                duplicate_report['exact_duplicates'].append(group_info)
    
    # Process visual duplicates
    print("\nProcessing visual duplicates...")
    for key, files in visual_duplicates.items():
        if len(files) > 1:
            # Filter out already moved files
            remaining = [f for f in files if f['path'] not in moved_files]
            if len(remaining) > 1:
                keep, remove = select_best_version(remaining)
                
                group_info = {
                    'kept': f"{keep['dir']}/{keep['name']}",
                    'removed': []
                }
                
                for file_to_remove in remove:
                    if file_to_remove['path'] not in moved_files:
                        base_name = file_to_remove['name']
                        new_name = f"{file_to_remove['dir'].replace('/', '_')}_{base_name}"
                        new_path = os.path.join(visual_dir, new_name)
                        
                        try:
                            shutil.move(file_to_remove['path'], new_path)
                            moved_files.add(file_to_remove['path'])
                            group_info['removed'].append(f"{file_to_remove['dir']}/{file_to_remove['name']}")
                            print(f"  Moved: {file_to_remove['name']} -> visual_duplicates/")
                        except Exception as e:
                            print(f"  Error moving {file_to_remove['name']}: {e}")
                
                if group_info['removed']:
                    duplicate_report['visual_duplicates'].append(group_info)
    
    # Process name duplicates (be more careful here)
    print("\nProcessing name-based duplicates...")
    for normalized, files in name_duplicates.items():
        if len(files) > 1:
            # Filter out already moved files
            remaining = [f for f in files if f['path'] not in moved_files]
            if len(remaining) > 1:
                # For name duplicates, only move if they're from different directories
                # and look reasonably similar in size
                keep, remove = select_best_version(remaining)
                
                group_info = {
                    'kept': f"{keep['dir']}/{keep['name']}",
                    'removed': []
                }
                
                for file_to_remove in remove:
                    # Only move if significantly different in size or from much older directory
                    size_ratio = file_to_remove['size'] / keep['size'] if keep['size'] > 0 else 1
                    if 0.5 <= size_ratio <= 2.0:  # Similar size
                        if file_to_remove['path'] not in moved_files:
                            base_name = file_to_remove['name']
                            new_name = f"{file_to_remove['dir'].replace('/', '_')}_{base_name}"
                            new_path = os.path.join(name_dir, new_name)
                            
                            try:
                                shutil.move(file_to_remove['path'], new_path)
                                moved_files.add(file_to_remove['path'])
                                group_info['removed'].append(f"{file_to_remove['dir']}/{file_to_remove['name']}")
                                print(f"  Moved: {file_to_remove['name']} -> name_duplicates/")
                            except Exception as e:
                                print(f"  Error moving {file_to_remove['name']}: {e}")
                
                if group_info['removed']:
                    duplicate_report['name_duplicates'].append(group_info)
    
    # Save duplicate report
    report_path = os.path.join(DUPLICATES_DIR, 'duplicate_report.json')
    with open(report_path, 'w') as f:
        json.dump(duplicate_report, f, indent=2)
    
    return len(moved_files), duplicate_report

def main():
    try:
        # Install required package if not available
        import imagehash
    except ImportError:
        print("Installing required package: imagehash")
        os.system("pip install imagehash pillow")
        import imagehash
    
    # Find duplicates
    exact_duplicates, visual_duplicates, name_duplicates = find_duplicates()
    
    # Report findings
    print("\n" + "=" * 80)
    print("DUPLICATE DETECTION RESULTS")
    print("=" * 80)
    
    exact_count = sum(len(files) - 1 for files in exact_duplicates.values() if len(files) > 1)
    visual_count = sum(len(files) - 1 for files in visual_duplicates.values() if len(files) > 1)
    name_count = sum(len(files) - 1 for files in name_duplicates.values() if len(files) > 1)
    
    print(f"\nFound duplicates:")
    print(f"  Exact duplicates: {exact_count} files")
    print(f"  Visual duplicates: {visual_count} files")
    print(f"  Name-based duplicates: {name_count} files")
    print(f"  Total potential duplicates: {exact_count + visual_count + name_count} files")
    
    if exact_count + visual_count + name_count > 0:
        response = input("\nMove duplicates to 'logos/duplicates' folder? (y/n): ")
        if response.lower() == 'y':
            moved_count, report = move_duplicates(exact_duplicates, visual_duplicates, name_duplicates)
            
            print("\n" + "=" * 80)
            print("DUPLICATE MANAGEMENT COMPLETE")
            print("=" * 80)
            print(f"Moved {moved_count} duplicate files")
            print(f"Duplicate report saved to: {DUPLICATES_DIR}/duplicate_report.json")
            
            # Show summary
            print("\nSummary by type:")
            print(f"  Exact duplicates moved: {len(report['exact_duplicates'])} groups")
            print(f"  Visual duplicates moved: {len(report['visual_duplicates'])} groups")
            print(f"  Name duplicates moved: {len(report['name_duplicates'])} groups")
    else:
        print("\nNo duplicates found!")

if __name__ == "__main__":
    main()