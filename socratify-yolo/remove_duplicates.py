#!/usr/bin/env python3
"""
Remove duplicate logos based on file content (MD5 hash)
Keep the file with the simplest name (no numbers if possible)
"""

import os
import hashlib
from collections import defaultdict
import re

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

def get_base_name(filename):
    """Extract base name without number suffix"""
    # Remove extension
    name = os.path.splitext(filename)[0]
    # Remove _2, _3, etc. suffixes
    base = re.sub(r'_\d+$', '', name)
    return base

def priority_score(filename):
    """Lower score = higher priority to keep"""
    name = os.path.splitext(filename)[0]
    
    # Prefer files without numbers
    if not re.search(r'_\d+$', name):
        return 0
    
    # Otherwise prefer lower numbers
    match = re.search(r'_(\d+)$', name)
    if match:
        return int(match.group(1))
    
    return 999

def main():
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images'
    
    print("Scanning for duplicates...")
    
    # Group files by hash
    hash_to_files = defaultdict(list)
    total_files = 0
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                filepath = os.path.join(root, file)
                file_hash = get_file_hash(filepath)
                if file_hash:
                    hash_to_files[file_hash].append(filepath)
                    total_files += 1
                    
                    if total_files % 1000 == 0:
                        print(f"  Processed {total_files} files...")
    
    print(f"\nTotal files scanned: {total_files}")
    
    # Find duplicates
    duplicates_to_remove = []
    unique_count = 0
    
    for file_hash, file_list in hash_to_files.items():
        if len(file_list) > 1:
            # Sort by priority (keep the best name)
            file_list.sort(key=lambda x: (
                priority_score(os.path.basename(x)),
                len(os.path.basename(x)),  # Prefer shorter names
                os.path.basename(x)  # Alphabetical as tiebreaker
            ))
            
            # Keep first, remove rest
            keeper = file_list[0]
            for duplicate in file_list[1:]:
                duplicates_to_remove.append(duplicate)
        else:
            unique_count += 1
    
    print(f"Unique files: {unique_count}")
    print(f"Duplicate files to remove: {len(duplicates_to_remove)}")
    
    # Show examples
    print("\nExample duplicates to be removed (showing first 10):")
    for dup in duplicates_to_remove[:10]:
        print(f"  {os.path.basename(dup)}")
    
    # Confirm before removing
    if duplicates_to_remove:
        print(f"\nRemoving {len(duplicates_to_remove)} duplicate files...")
        
        if True:  # Auto-confirm
            removed_count = 0
            for filepath in duplicates_to_remove:
                try:
                    os.remove(filepath)
                    removed_count += 1
                    
                    if removed_count % 100 == 0:
                        print(f"  Removed {removed_count} files...")
                        
                except Exception as e:
                    print(f"Error removing {filepath}: {e}")
            
            print(f"\n✅ Successfully removed {removed_count} duplicate files!")
            
            # Final count
            remaining = 0
            for root, dirs, files in os.walk(base_dir):
                for file in files:
                    if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                        remaining += 1
            
            print(f"📊 Files remaining: {remaining}")
            print(f"📉 Space saved: ~{(removed_count * 50) / 1024:.1f} MB (estimated)")
        else:
            print("Deletion cancelled.")
    else:
        print("\nNo duplicates found!")

if __name__ == "__main__":
    main()