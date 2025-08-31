#!/usr/bin/env python3
"""
Consolidate all unique logos into a single folder
Removes duplicates and creates a clean, organized collection
"""

import os
import shutil
import hashlib
from collections import defaultdict
import json
from datetime import datetime

# Logo directories to consolidate
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

# Output directory for consolidated unique logos
UNIQUE_LOGOS_DIR = 'logos/all_unique_logos'
DUPLICATES_DIR = 'logos/duplicates_archive'

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

def normalize_filename(filename):
    """Normalize filename for consistency"""
    # Remove extra spaces and underscores
    name = filename.replace('  ', ' ').replace('__', '_')
    # Replace spaces with underscores
    name = name.replace(' ', '_')
    # Remove duplicate underscores
    while '__' in name:
        name = name.replace('__', '_')
    return name

def consolidate_logos():
    """Consolidate all unique logos into a single folder"""
    print("=" * 80)
    print("CONSOLIDATING UNIQUE LOGOS")
    print("=" * 80)
    
    # Create output directories
    os.makedirs(UNIQUE_LOGOS_DIR, exist_ok=True)
    os.makedirs(DUPLICATES_DIR, exist_ok=True)
    
    # Track all files and their hashes
    all_files = []
    file_hashes = {}
    hash_to_file = {}
    
    # Collect all files
    print("\nScanning all logo directories...")
    total_scanned = 0
    
    for dir_path in LOGO_DIRECTORIES:
        if os.path.exists(dir_path):
            dir_files = 0
            for filename in os.listdir(dir_path):
                if filename.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif')):
                    filepath = os.path.join(dir_path, filename)
                    filesize = os.path.getsize(filepath)
                    
                    file_info = {
                        'path': filepath,
                        'name': filename,
                        'dir': dir_path,
                        'size': filesize
                    }
                    
                    # Calculate hash
                    file_hash = get_file_hash(filepath)
                    if file_hash:
                        file_info['hash'] = file_hash
                        all_files.append(file_info)
                        dir_files += 1
                        total_scanned += 1
            
            if dir_files > 0:
                print(f"  {dir_path}: {dir_files} files")
    
    print(f"\nTotal files scanned: {total_scanned}")
    
    # Directory priority (newer directories have higher priority)
    dir_priority = {dir_path: i for i, dir_path in enumerate(LOGO_DIRECTORIES)}
    
    # Process files and copy unique ones
    print("\nProcessing and copying unique logos...")
    unique_count = 0
    duplicate_count = 0
    copied_hashes = set()
    consolidation_log = []
    
    # Sort files by priority (newer directories first) and size (larger first)
    all_files.sort(key=lambda x: (dir_priority.get(x['dir'], 0), x['size']), reverse=True)
    
    for file_info in all_files:
        file_hash = file_info.get('hash')
        
        if file_hash and file_hash not in copied_hashes:
            # This is a unique file - copy it
            source_path = file_info['path']
            
            # Normalize the filename
            normalized_name = normalize_filename(file_info['name'])
            dest_path = os.path.join(UNIQUE_LOGOS_DIR, normalized_name)
            
            # Handle filename conflicts
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(normalized_name)
                counter = 1
                while os.path.exists(dest_path):
                    dest_path = os.path.join(UNIQUE_LOGOS_DIR, f"{base}_{counter}{ext}")
                    counter += 1
            
            try:
                shutil.copy2(source_path, dest_path)
                copied_hashes.add(file_hash)
                unique_count += 1
                
                consolidation_log.append({
                    'source': source_path,
                    'destination': dest_path,
                    'size': file_info['size'],
                    'hash': file_hash
                })
                
                if unique_count % 100 == 0:
                    print(f"  Copied {unique_count} unique logos...")
                    
            except Exception as e:
                print(f"\nError copying {source_path}: {e}")
        else:
            # This is a duplicate
            duplicate_count += 1
    
    print(f"\n✓ Copied {unique_count} unique logos")
    print(f"✓ Skipped {duplicate_count} duplicates")
    
    # Save consolidation report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_scanned': total_scanned,
        'unique_logos': unique_count,
        'duplicates_skipped': duplicate_count,
        'source_directories': LOGO_DIRECTORIES,
        'consolidation_log': consolidation_log[:100]  # Save first 100 for reference
    }
    
    report_path = os.path.join(UNIQUE_LOGOS_DIR, 'consolidation_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Create a summary file
    summary_path = os.path.join(UNIQUE_LOGOS_DIR, 'SUMMARY.txt')
    with open(summary_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("CONSOLIDATED UNIQUE LOGO COLLECTION\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total unique logos: {unique_count:,}\n")
        f.write(f"Duplicates removed: {duplicate_count:,}\n")
        f.write(f"Original files scanned: {total_scanned:,}\n")
        f.write(f"Space saved: ~{duplicate_count * 50 / 1024:.1f} MB\n\n")
        f.write("This collection contains logos from:\n")
        f.write("- Business schools (400+ globally)\n")
        f.write("- Employers (Fortune 500, startups, etc.)\n")
        f.write("- Consulting firms\n")
        f.write("- Law firms\n")
        f.write("- Financial institutions\n")
        f.write("- Technology companies\n")
        f.write("- Healthcare organizations\n")
        f.write("- And many more categories\n\n")
        f.write("All duplicates have been removed, keeping the best quality version of each logo.\n")
    
    return unique_count, duplicate_count

def verify_collection():
    """Verify the consolidated collection"""
    print("\n" + "=" * 80)
    print("VERIFYING CONSOLIDATED COLLECTION")
    print("=" * 80)
    
    if os.path.exists(UNIQUE_LOGOS_DIR):
        files = [f for f in os.listdir(UNIQUE_LOGOS_DIR) 
                if f.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))]
        
        # Check file types
        file_types = defaultdict(int)
        total_size = 0
        
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            file_types[ext] += 1
            filepath = os.path.join(UNIQUE_LOGOS_DIR, filename)
            total_size += os.path.getsize(filepath)
        
        print(f"\nCollection statistics:")
        print(f"  Total unique logos: {len(files):,}")
        print(f"  Total size: {total_size / (1024 * 1024):.1f} MB")
        print(f"\nFile types:")
        for ext, count in sorted(file_types.items()):
            print(f"  {ext}: {count:,} files")
        
        # Sample some filenames
        print(f"\nSample logos (first 10):")
        for filename in sorted(files)[:10]:
            print(f"  - {filename}")
        
        print(f"\n✓ All unique logos consolidated in: {UNIQUE_LOGOS_DIR}")

def main():
    print("This will consolidate all logos into a single folder with no duplicates.")
    print("The original files will not be deleted.\n")
    
    response = input("Proceed with consolidation? (y/n): ")
    if response.lower() != 'y':
        print("Consolidation cancelled.")
        return
    
    # Consolidate logos
    unique_count, duplicate_count = consolidate_logos()
    
    # Verify the collection
    verify_collection()
    
    print("\n" + "=" * 80)
    print("CONSOLIDATION COMPLETE!")
    print("=" * 80)
    print(f"\n✓ Created clean collection with {unique_count:,} unique logos")
    print(f"✓ Location: {UNIQUE_LOGOS_DIR}")
    print(f"✓ Report: {UNIQUE_LOGOS_DIR}/consolidation_report.json")
    print(f"✓ Summary: {UNIQUE_LOGOS_DIR}/SUMMARY.txt")

if __name__ == "__main__":
    main()