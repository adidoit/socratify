#!/usr/bin/env python3
"""
Clean up the logo collection:
1. Remove messy filename suffixes
2. Remove duplicate files (keep PNG over other formats)
3. Standardize naming
"""

import os
import re
import hashlib
from collections import defaultdict

def clean_filename(filename):
    """Clean filename to just company name"""
    # Remove extension first
    name, ext = os.path.splitext(filename)
    
    # Remove messy suffixes
    name = re.sub(r'(_logo|_icon|_favicon|_clearbit|_downloaded)', '', name, flags=re.IGNORECASE)
    name = re.sub(r'_\d+$', '', name)  # Remove trailing numbers like _2, _7
    name = re.sub(r'_\([^)]+\)$', '', name)  # Remove parenthetical suffixes
    
    # Clean up extra underscores
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    
    return name + ext

def get_file_hash(filepath):
    """Get MD5 hash of file"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def main():
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} does not exist")
        return
    
    # Get all files
    all_files = []
    for file in os.listdir(base_dir):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
            all_files.append(file)
    
    print(f"Processing {len(all_files)} files...")
    
    # Step 1: Group files by normalized company name
    company_groups = defaultdict(list)
    
    for file in all_files:
        cleaned_name = clean_filename(file)
        company_name = os.path.splitext(cleaned_name)[0]
        company_groups[company_name.lower()].append(file)
    
    print(f"Found {len(company_groups)} unique company names")
    
    # Step 2: For each company, pick the best file and remove duplicates
    files_to_remove = []
    files_to_rename = []
    
    for company_name, file_list in company_groups.items():
        if len(file_list) == 1:
            # Single file - just rename if needed
            original_file = file_list[0]
            clean_name = clean_filename(original_file)
            if original_file != clean_name:
                files_to_rename.append((original_file, clean_name))
        else:
            # Multiple files - pick the best one and remove others
            print(f"Company '{company_name}' has {len(file_list)} files: {file_list}")
            
            # Preference order: PNG > JPG > SVG > WEBP > ICO
            format_priority = {'.png': 0, '.jpg': 1, '.jpeg': 1, '.svg': 2, '.webp': 3, '.ico': 4}
            
            # Sort by format priority, then by filename length (shorter is better)
            sorted_files = sorted(file_list, key=lambda f: (
                format_priority.get(os.path.splitext(f)[1].lower(), 5),
                len(f),
                f
            ))
            
            best_file = sorted_files[0]
            duplicates = sorted_files[1:]
            
            # Rename best file if needed
            clean_name = clean_filename(best_file)
            if best_file != clean_name:
                files_to_rename.append((best_file, clean_name))
            
            # Mark duplicates for removal
            files_to_remove.extend(duplicates)
    
    print(f"Files to rename: {len(files_to_rename)}")
    print(f"Duplicate files to remove: {len(files_to_remove)}")
    
    # Step 3: Execute renames and removals
    renamed_count = 0
    removed_count = 0
    
    # Rename files
    for old_name, new_name in files_to_rename:
        old_path = os.path.join(base_dir, old_name)
        new_path = os.path.join(base_dir, new_name)
        
        if os.path.exists(old_path):
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
                if renamed_count <= 10:  # Show first 10 examples
                    print(f"Renamed: {old_name} -> {new_name}")
            except Exception as e:
                print(f"Error renaming {old_name}: {e}")
    
    # Remove duplicates
    for file_to_remove in files_to_remove:
        file_path = os.path.join(base_dir, file_to_remove)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                removed_count += 1
                if removed_count <= 10:  # Show first 10 examples
                    print(f"Removed: {file_to_remove}")
            except Exception as e:
                print(f"Error removing {file_to_remove}: {e}")
    
    # Final count
    final_files = []
    for file in os.listdir(base_dir):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
            final_files.append(file)
    
    print(f"\n=== CLEANUP COMPLETE ===")
    print(f"Original files: {len(all_files)}")
    print(f"Files renamed: {renamed_count}")
    print(f"Duplicate files removed: {removed_count}")
    print(f"Final files: {len(final_files)}")
    print(f"Unique companies: {len(company_groups)}")

if __name__ == "__main__":
    main()