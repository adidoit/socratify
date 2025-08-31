#!/usr/bin/env python3
"""
Manage duplicates with detailed analysis and safe moving
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

def find_exact_duplicates():
    """Find exact duplicates by file hash"""
    print("=" * 80)
    print("FINDING EXACT DUPLICATES")
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
                        'size': filesize
                    })
    
    print(f"Found {len(all_files)} total logo files")
    
    # Find exact duplicates by file hash
    print("\nCalculating file hashes...")
    exact_duplicates = defaultdict(list)
    
    for i, file_info in enumerate(all_files):
        if i % 100 == 0:
            print(f"  Processed {i}/{len(all_files)} files...", end='\r')
        
        file_hash = get_file_hash(file_info['path'])
        if file_hash:
            file_info['hash'] = file_hash
            exact_duplicates[file_hash].append(file_info)
    
    print(f"  Processed {len(all_files)}/{len(all_files)} files")
    
    # Filter to only groups with duplicates
    exact_duplicates = {k: v for k, v in exact_duplicates.items() if len(v) > 1}
    
    return exact_duplicates

def move_exact_duplicates(exact_duplicates):
    """Move exact duplicates keeping the best version"""
    
    # Create duplicate directories
    os.makedirs(DUPLICATES_DIR, exist_ok=True)
    exact_dir = os.path.join(DUPLICATES_DIR, 'exact_duplicates')
    os.makedirs(exact_dir, exist_ok=True)
    
    # Directory priority (newer directories have higher priority)
    dir_priority = {dir_path: i for i, dir_path in enumerate(LOGO_DIRECTORIES)}
    
    moved_count = 0
    kept_files = []
    moved_files = []
    
    print("\n" + "=" * 80)
    print("MOVING EXACT DUPLICATES")
    print("=" * 80)
    
    for hash_val, files in exact_duplicates.items():
        if len(files) > 1:
            # Sort by directory priority (newer first) and then by size
            files_sorted = sorted(files, 
                                key=lambda x: (dir_priority.get(x['dir'], 0), x['size']), 
                                reverse=True)
            
            keep = files_sorted[0]
            kept_files.append(keep)
            
            # Move duplicates
            for f in files_sorted[1:]:
                # Create subdirectory based on original location
                subdir = f['dir'].replace('logos/', '')
                target_subdir = os.path.join(exact_dir, subdir)
                os.makedirs(target_subdir, exist_ok=True)
                
                new_path = os.path.join(target_subdir, f['name'])
                
                # Handle filename conflicts
                if os.path.exists(new_path):
                    base, ext = os.path.splitext(f['name'])
                    counter = 1
                    while os.path.exists(new_path):
                        new_path = os.path.join(target_subdir, f"{base}_{counter}{ext}")
                        counter += 1
                
                try:
                    shutil.move(f['path'], new_path)
                    moved_files.append({
                        'original': f['path'],
                        'new': new_path,
                        'kept': keep['path']
                    })
                    moved_count += 1
                    
                    if moved_count % 10 == 0:
                        print(f"  Moved {moved_count} files...")
                except Exception as e:
                    print(f"\n  Error moving {f['path']}: {e}")
    
    # Save movement report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_groups': len(exact_duplicates),
        'total_moved': moved_count,
        'movements': moved_files
    }
    
    report_path = os.path.join(DUPLICATES_DIR, 'movement_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n✓ Moved {moved_count} exact duplicate files")
    print(f"✓ Kept {len(kept_files)} best versions")
    print(f"✓ Movement report saved to: {report_path}")
    
    return moved_count

def analyze_remaining():
    """Analyze what's left after moving duplicates"""
    print("\n" + "=" * 80)
    print("ANALYZING REMAINING COLLECTION")
    print("=" * 80)
    
    remaining_count = 0
    dir_counts = {}
    
    for dir_path in LOGO_DIRECTORIES:
        if os.path.exists(dir_path):
            count = len([f for f in os.listdir(dir_path) 
                        if f.endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))])
            dir_counts[dir_path] = count
            remaining_count += count
    
    print(f"\nRemaining files by directory:")
    for dir_path, count in sorted(dir_counts.items(), key=lambda x: x[1], reverse=True):
        dir_name = dir_path.split('/')[-1]
        print(f"  {dir_name:<30} {count:>6} files")
    
    print(f"\nTotal remaining: {remaining_count:,} files")
    
    # Calculate unique organizations (rough estimate)
    unique_estimate = remaining_count - 100  # Assume ~100 more duplicates by name
    print(f"Estimated unique organizations: ~{unique_estimate:,}")

def main():
    # Find exact duplicates
    exact_duplicates = find_exact_duplicates()
    
    # Show summary
    duplicate_count = sum(len(files) - 1 for files in exact_duplicates.values())
    
    print("\n" + "=" * 80)
    print("DUPLICATE SUMMARY")
    print("=" * 80)
    print(f"\nFound {duplicate_count} exact duplicate files in {len(exact_duplicates)} groups")
    
    # Show examples
    if exact_duplicates:
        print("\nExample duplicate groups:")
        for i, (hash_val, files) in enumerate(list(exact_duplicates.items())[:5]):
            print(f"\n  Group {i+1} ({len(files)} identical files):")
            for f in files[:3]:
                print(f"    - {f['dir']}/{f['name']} ({f['size']:,} bytes)")
            if len(files) > 3:
                print(f"    ... and {len(files) - 3} more")
    
    print("\n" + "=" * 80)
    print("OPTIONS:")
    print("=" * 80)
    print("1. Move exact duplicates to 'logos/duplicates/exact_duplicates/'")
    print("2. Just analyze (no changes)")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1/2/3): ")
    
    if choice == '1':
        moved = move_exact_duplicates(exact_duplicates)
        analyze_remaining()
    elif choice == '2':
        print("\nNo files moved. Analysis complete.")
    else:
        print("\nExiting.")

if __name__ == "__main__":
    main()