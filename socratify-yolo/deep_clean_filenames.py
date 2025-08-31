#!/usr/bin/env python3
"""
Deep clean logo filenames - remove ALL unnecessary suffixes and prefixes
"""

import os
import re
import shutil

def deep_clean_filename(filepath):
    """Aggressively remove all unwanted patterns from filename"""
    
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    # Replace hyphens with underscores first (for consistency)
    cleaned = name.replace('-', '_')
    
    # Patterns to remove (order matters - most specific first)
    patterns_to_remove = [
        # Collection and category patterns (with both - and _)
        r'_universities_comprehensive',
        r'_business_school_logos',
        r'_expanded_business_schools',
        r'_global_mba_logos',
        r'_comprehensive_global',
        r'_ultimate_final',
        r'_final_expansion',
        r'_final_supplementary',
        r'_downloaded',
        r'_all_unique_logos',
        r'_clearbit',
        r'_favicon',
        r'_ddg',
        
        # Prefixes
        r'^organized_collection_',
        r'^final_collection_',
        r'^all_unique_logos_',
        r'^business_school_logos_',
        r'^massive_downloads_\d+_',
        r'^ultimate_downloads_\d+_',
        r'^verified_downloads_\d+_',
        r'^boring_essential_\d+_',
        r'^final_\d+_\d+_',
        r'^downloads_\d+_',
        r'^institutional_logos_\d+_',
        r'^\d{6}_',  # 6-digit timestamps
        r'^\d{8}_\d{6}_',  # Full timestamps
        
        # Country suffixes in parentheses or underscores
        r'_\([A-Za-z_\s]+\)$',  # Like _(USA) or _(South_Africa)
        r'_USA$', r'_UK$', r'_Canada$', r'_France$', r'_Germany$',
        r'_Spain$', r'_Italy$', r'_Japan$', r'_China$', r'_India$',
        r'_Brazil$', r'_Mexico$', r'_Australia$', r'_Singapore$',
        r'_Malaysia$', r'_UAE$', r'_Saudi_Arabia$', r'_Israel$',
        r'_Egypt$', r'_Nigeria$', r'_Kenya$', r'_Lebanon$',
        r'_South_Africa$', r'_Denmark$', r'_Netherlands$',
        
        # Domain-related suffixes
        r'_Clearbit_Domain$',
        r'_clearbit_domain$',
        
        # Remove _1 suffix (but keep _2, _3 etc for duplicates)
        r'_1$',
    ]
    
    # Apply all removal patterns
    for pattern in patterns_to_remove:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up any double underscores that might have been created
    cleaned = re.sub(r'__+', '_', cleaned)
    
    # Remove leading/trailing underscores
    cleaned = cleaned.strip('_')
    
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
    
    print("Deep cleaning filenames...")
    print("Scanning for files to rename...")
    
    # Collect all renames needed
    renames_needed = []
    
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                filepath = os.path.join(root, file)
                new_path = deep_clean_filename(filepath)
                
                if new_path and new_path != filepath:
                    renames_needed.append((filepath, new_path))
    
    print(f"Found {len(renames_needed)} files that need renaming")
    
    # Perform renames
    print("\nRenaming files...")
    for old_path, new_path in renames_needed:
        try:
            # Handle duplicates by adding a number
            if os.path.exists(new_path):
                base, ext = os.path.splitext(new_path)
                counter = 2
                # Skip if it's already numbered
                while os.path.exists(f"{base}_{counter}{ext}"):
                    counter += 1
                new_path = f"{base}_{counter}{ext}"
            
            os.rename(old_path, new_path)
            renamed_count += 1
            
            if renamed_count % 100 == 0:
                print(f"  Renamed {renamed_count} files...")
                
        except Exception as e:
            print(f"Error renaming {old_path}: {e}")
            error_count += 1
    
    # Final report
    print("\n" + "="*60)
    print("DEEP FILENAME CLEANUP COMPLETE!")
    print(f"✅ Renamed: {renamed_count} files")
    print(f"❌ Errors: {error_count} files")
    print("="*60)
    
    # Show some examples of cleaned names
    print("\nExample cleaned filenames:")
    example_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files[:5]:  # Just show first 5 from each dir
            if file.endswith(('.png', '.jpg', '.jpeg')):
                example_files.append(os.path.join(root.split('/')[-1], file))
        if len(example_files) >= 15:
            break
    
    for example in example_files[:15]:
        print(f"  {example}")

if __name__ == "__main__":
    main()