#!/usr/bin/env python3
"""
Final aggressive cleanup - handle all edge cases
"""

import os
import re

def aggressive_clean(filepath):
    """Very aggressive filename cleaning"""
    
    directory = os.path.dirname(filepath)
    filename = os.path.basename(filepath)
    name, ext = os.path.splitext(filename)
    
    # First, handle files that START with problematic patterns
    prefixes_to_remove = [
        'universities_comprehensive_',
        'business_school_logos_',
        'expanded_business_schools_',
        'ultimate_final_',
        'static_assets_prod_',
        'expanded_business_',
        'business_schools_',
        'epicgames_',
    ]
    
    cleaned = name
    for prefix in prefixes_to_remove:
        if cleaned.startswith(prefix):
            cleaned = cleaned[len(prefix):]
    
    # Remove any remaining problematic patterns anywhere in the name
    patterns = [
        r'_universities_comprehensive',
        r'_business_school_logos',
        r'_expanded_business_schools',
        r'_ultimate_final',
        r'_static_assets_prod',
        r'universities_comprehensive_',
        r'business_school_logos_',
        r'expanded_business_schools_',
        r'ultimate_final_',
        r'static_assets_prod_',
    ]
    
    for pattern in patterns:
        cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
    
    # Remove any numbers at the end (like _1, _2, etc) EXCEPT for duplicates (_2, _3, etc)
    # Keep _2 and higher, remove _1
    if cleaned.endswith('_1'):
        cleaned = cleaned[:-2]
    
    # Clean up
    cleaned = re.sub(r'__+', '_', cleaned)
    cleaned = cleaned.strip('_')
    
    # If we have nothing left, keep original
    if not cleaned or cleaned.isdigit():
        return None
    
    new_filename = cleaned + ext
    
    if new_filename != filename:
        return os.path.join(directory, new_filename)
    return None

def main():
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images'
    
    renamed = 0
    errors = 0
    
    print("Final aggressive cleanup...")
    
    # Find all problematic files
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if any(pattern in file.lower() for pattern in 
                   ['universities_comprehensive', 'business_school', 'ultimate_final', 
                    'static_assets', 'expanded_business']):
                
                filepath = os.path.join(root, file)
                new_path = aggressive_clean(filepath)
                
                if new_path:
                    try:
                        # Handle duplicates
                        if os.path.exists(new_path):
                            base, ext = os.path.splitext(new_path)
                            counter = 2
                            while os.path.exists(f"{base}_{counter}{ext}"):
                                counter += 1
                            new_path = f"{base}_{counter}{ext}"
                        
                        os.rename(filepath, new_path)
                        renamed += 1
                        
                        if renamed % 50 == 0:
                            print(f"  Cleaned {renamed} files...")
                            
                    except Exception as e:
                        print(f"Error: {e}")
                        errors += 1
    
    print(f"\n✅ Cleaned: {renamed} files")
    print(f"❌ Errors: {errors} files")

if __name__ == "__main__":
    main()