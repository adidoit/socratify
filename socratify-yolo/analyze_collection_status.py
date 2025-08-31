#!/usr/bin/env python3
"""
Analyze current logo collection status:
1. Check for potential duplicates
2. Verify filename cleanliness
3. Generate current inventory
4. Identify what major categories we might still be missing
"""

import os
import re
import hashlib
from collections import defaultdict, Counter

def normalize_company_name(filename):
    """Normalize company name for duplicate detection"""
    # Remove extension
    name = os.path.splitext(filename)[0]
    
    # Remove common suffixes
    name = re.sub(r'(_logo|_icon|_favicon|_clearbit|_downloaded|_\d+)$', '', name, flags=re.IGNORECASE)
    
    # Normalize to lowercase and remove special chars
    name = name.lower()
    name = re.sub(r'[^a-z0-9]', '', name)
    
    return name

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

def analyze_collection():
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    
    if not os.path.exists(base_dir):
        print(f"Directory {base_dir} does not exist")
        return
    
    files = []
    for file in os.listdir(base_dir):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
            files.append(file)
    
    print(f"COLLECTION ANALYSIS")
    print(f"===================")
    print(f"Total files: {len(files)}")
    
    # Check for messy filenames
    messy_files = []
    for file in files:
        if re.search(r'(_logo|_icon|_favicon|_clearbit|_downloaded|_\d+)', file, re.IGNORECASE):
            messy_files.append(file)
    
    print(f"Messy filenames: {len(messy_files)}")
    if messy_files:
        print("Examples of messy filenames:")
        for file in messy_files[:10]:
            print(f"  - {file}")
    
    # Check for potential name duplicates
    normalized_names = defaultdict(list)
    for file in files:
        normalized = normalize_company_name(file)
        normalized_names[normalized].append(file)
    
    potential_duplicates = {k: v for k, v in normalized_names.items() if len(v) > 1}
    print(f"Potential name duplicates: {len(potential_duplicates)}")
    
    if potential_duplicates:
        print("Examples of potential duplicates:")
        for normalized, file_list in list(potential_duplicates.items())[:10]:
            print(f"  {normalized}: {', '.join(file_list)}")
    
    # Check file hash duplicates (sample)
    print(f"\nChecking for identical files (MD5 hash)...")
    hash_groups = defaultdict(list)
    
    # Check first 100 files for performance
    sample_files = files[:100]
    for file in sample_files:
        filepath = os.path.join(base_dir, file)
        file_hash = get_file_hash(filepath)
        if file_hash:
            hash_groups[file_hash].append(file)
    
    identical_files = {k: v for k, v in hash_groups.items() if len(v) > 1}
    print(f"Identical files in sample: {len(identical_files)}")
    
    # Analyze company types in collection
    print(f"\nCOMPANY TYPE ANALYSIS")
    print(f"=====================")
    
    # Look for patterns in company names
    tech_companies = []
    financial_companies = []
    energy_companies = []
    healthcare_companies = []
    retail_companies = []
    
    for file in files[:200]:  # Sample for analysis
        name = os.path.splitext(file)[0].lower()
        
        if any(keyword in name for keyword in ['tech', 'software', 'data', 'ai', 'cloud', 'digital']):
            tech_companies.append(file)
        elif any(keyword in name for keyword in ['bank', 'financial', 'capital', 'fund', 'investment']):
            financial_companies.append(file)
        elif any(keyword in name for keyword in ['energy', 'oil', 'gas', 'power', 'electric']):
            energy_companies.append(file)
        elif any(keyword in name for keyword in ['health', 'medical', 'pharma', 'bio']):
            healthcare_companies.append(file)
        elif any(keyword in name for keyword in ['retail', 'store', 'shop', 'market']):
            retail_companies.append(file)
    
    print(f"Tech companies (sample): {len(tech_companies)}")
    print(f"Financial companies (sample): {len(financial_companies)}")
    print(f"Energy companies (sample): {len(energy_companies)}")
    print(f"Healthcare companies (sample): {len(healthcare_companies)}")
    print(f"Retail companies (sample): {len(retail_companies)}")
    
    # Generate unique company list
    unique_companies = set()
    for file in files:
        normalized = normalize_company_name(file)
        unique_companies.add(normalized)
    
    print(f"\nUNIQUE COMPANIES")
    print(f"================")
    print(f"Approximate unique companies: {len(unique_companies)}")
    
    # Save detailed analysis
    with open('/Users/adi/code/socratify/socratify-yolo/collection_analysis.txt', 'w') as f:
        f.write("LOGO COLLECTION ANALYSIS REPORT\n")
        f.write("=" * 35 + "\n\n")
        f.write(f"Total files: {len(files)}\n")
        f.write(f"Messy filenames: {len(messy_files)}\n")
        f.write(f"Potential name duplicates: {len(potential_duplicates)}\n")
        f.write(f"Approximate unique companies: {len(unique_companies)}\n\n")
        
        if messy_files:
            f.write("MESSY FILENAMES:\n")
            for file in messy_files:
                f.write(f"- {file}\n")
            f.write("\n")
        
        if potential_duplicates:
            f.write("POTENTIAL DUPLICATES:\n")
            for normalized, file_list in potential_duplicates.items():
                f.write(f"{normalized}: {', '.join(file_list)}\n")
            f.write("\n")
        
        f.write("SAMPLE COMPANIES BY TYPE:\n")
        f.write(f"Tech: {len(tech_companies)}\n")
        f.write(f"Financial: {len(financial_companies)}\n")
        f.write(f"Energy: {len(energy_companies)}\n")
        f.write(f"Healthcare: {len(healthcare_companies)}\n")
        f.write(f"Retail: {len(retail_companies)}\n")
    
    print(f"\nDetailed analysis saved to collection_analysis.txt")
    
    return {
        'total_files': len(files),
        'messy_files': len(messy_files),
        'potential_duplicates': len(potential_duplicates),
        'unique_companies': len(unique_companies)
    }

if __name__ == "__main__":
    analyze_collection()