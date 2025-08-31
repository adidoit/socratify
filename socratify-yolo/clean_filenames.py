#!/usr/bin/env python3
"""
Clean up logo filenames by removing prefixes and suffixes
"""

import os
import re
import shutil

def clean_filename(filepath):
    """Remove unwanted prefixes and suffixes from filename"""
    
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    # Patterns to remove (order matters - most specific first)
    patterns_to_remove = [
        # Prefixes from collection folders
        r'^organized_collection_',
        r'^final_collection_',
        r'^all_unique_logos_',
        r'^massive_downloads_\d+_',
        r'^ultimate_downloads_\d+_',
        r'^verified_downloads_\d+_',
        r'^boring_essential_\d+_',
        r'^final_\d+_\d+_',
        r'^downloads_\d+_',
        r'^institutional_logos_\d+_',
        # Timestamp prefixes
        r'^\d{6}_',  # 6-digit timestamps like 175600_
        r'^\d{8}_\d{6}_',  # Full timestamps
        
        # Suffixes from categories
        r'_universities_comprehensive$',
        r'_business_school_logos$',
        r'_expanded_business_schools$',
        r'_global_mba_logos$',
        r'_comprehensive_global$',
        r'_ultimate_final$',
        r'_final_expansion$',
        r'_final_supplementary$',
        r'_downloaded$',
        r'_all_unique_logos$',
        r'_ultimate_final$',
        r'_ddg$',
        r'_clearbit$',
        r'_favicon$',
        r'_Clearbit_Domain$',
        
        # Special case patterns
        r'_\(USA\)$',
        r'_\(UK\)$',
        r'_\(Canada\)$',
        r'_\(France\)$',
        r'_\(Germany\)$',
        r'_\(Spain\)$',
        r'_\(Italy\)$',
        r'_\(Japan\)$',
        r'_\(China\)$',
        r'_\(India\)$',
        r'_\(Brazil\)$',
        r'_\(Mexico\)$',
        r'_\(Australia\)$',
        r'_\(South_Africa\)$',
        r'_\(Singapore\)$',
        r'_\(Malaysia\)$',
        r'_\(UAE\)$',
        r'_\(Saudi_Arabia\)$',
        r'_\(Israel\)$',
        r'_\(Egypt\)$',
        r'_\(Nigeria\)$',
        r'_\(Kenya\)$',
        r'_\(Lebanon\)$',
    ]
    
    # Clean the name
    cleaned = name
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, '', cleaned)
    
    # If we removed everything or ended up with just numbers, use original
    if not cleaned or cleaned.isdigit():
        cleaned = name
    
    # Add extension back
    new_filename = cleaned + ext
    
    # Return new path if changed
    if new_filename != filename:
        return os.path.join(directory, new_filename)
    return None

def main():
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images'
    
    # Track statistics
    renamed_count = 0
    skipped_count = 0
    error_count = 0
    duplicates = {}
    
    print("Scanning for files to rename...")
    
    # First pass - collect all renames needed
    renames_needed = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico')):
                filepath = os.path.join(root, file)
                new_path = clean_filename(filepath)
                
                if new_path and new_path != filepath:
                    renames_needed.append((filepath, new_path))
    
    print(f"Found {len(renames_needed)} files that need renaming")
    
    # Second pass - perform renames
    print("\nRenaming files...")
    for old_path, new_path in renames_needed:
        try:
            # Handle duplicates by adding a number
            if os.path.exists(new_path):
                base, ext = os.path.splitext(new_path)
                counter = 2
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                new_path = f"{base}_{counter}{ext}"
                
                # Track duplicates
                original_name = os.path.basename(new_path).replace(f"_{counter}", "")
                if original_name not in duplicates:
                    duplicates[original_name] = []
                duplicates[original_name].append(os.path.basename(old_path))
            
            os.rename(old_path, new_path)
            renamed_count += 1
            
            if renamed_count % 100 == 0:
                print(f"  Renamed {renamed_count} files...")
                
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
            error_count += 1
    
    # Final report
    print("\n" + "="*60)
    print("FILENAME CLEANUP COMPLETE!")
    print(f"✅ Renamed: {renamed_count} files")
    print(f"⏭️ Skipped: {skipped_count} files")
    print(f"❌ Errors: {error_count} files")
    
    if duplicates:
        print(f"\n⚠️ Found {len(duplicates)} entities with duplicate logos")
        print("Top 10 duplicates:")
        for name, sources in list(duplicates.items())[:10]:
            print(f"  {name}: {len(sources)+1} versions")
    
    print("="*60)

if __name__ == "__main__":
    main()