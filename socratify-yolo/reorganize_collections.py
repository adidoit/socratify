#!/usr/bin/env python3
"""
Reorganize logo collections into proper categories
Keeping business schools separate from universities
"""

import os
import shutil
import json
from collections import defaultdict

# Define categories and keywords
CATEGORIES = {
    'business_schools': {
        'keywords': ['business_school', 'school_of_management', 'school_of_business', 
                    'college_of_business', 'haas', 'wharton', 'kellogg', 'booth', 
                    'sloan', 'tuck', 'ross', 'stern', 'darden', 'fuqua', 'anderson',
                    'marshall', 'mccombs', 'owen', 'simon', 'tepper', 'yale_som',
                    'johnson', 'olin', 'kenan_flagler', 'fisher', 'broad', 'smeal',
                    'carlson', 'iim', 'isb', 'xlri', 'fms', 'insead', 'lbs',
                    'hec', 'iese', 'esade', 'said', 'judge', 'imperial', 'warwick'],
        'dirs': ['logos/business_school_logos', 'logos/expanded_business_schools']
    },
    'universities': {
        'keywords': ['university', 'college', 'institute', 'iit', 'nit', 'academy',
                    'école', 'universität', 'universidad', 'universidade', 'università'],
        'exclude': ['business_school', 'school_of_management', 'school_of_business'],
        'dirs': ['logos/institution_logos', 'logos/universities_comprehensive']
    },
    'companies': {
        'keywords': [],  # Everything else
        'dirs': ['logos/downloaded', 'logos/global_mba_logos', 'logos/comprehensive_global',
                'logos/final_expansion', 'logos/ultimate_final', 'logos/final_supplementary']
    }
}

# New organized structure
OUTPUT_BASE = 'logos/organized_collection'
BUSINESS_SCHOOLS_DIR = os.path.join(OUTPUT_BASE, 'business_schools')
UNIVERSITIES_DIR = os.path.join(OUTPUT_BASE, 'universities')
COMPANIES_DIR = os.path.join(OUTPUT_BASE, 'companies')

def create_directories():
    """Create organized directory structure"""
    for directory in [BUSINESS_SCHOOLS_DIR, UNIVERSITIES_DIR, COMPANIES_DIR]:
        os.makedirs(directory, exist_ok=True)
        
        # Create subdirectories for regions
        for region in ['north_america', 'europe', 'asia', 'other']:
            os.makedirs(os.path.join(directory, region), exist_ok=True)

def categorize_file(filename):
    """Determine category for a file based on name"""
    name_lower = filename.lower()
    
    # Check for business school first (highest priority)
    for keyword in CATEGORIES['business_schools']['keywords']:
        if keyword in name_lower:
            return 'business_schools'
    
    # Check for university (but exclude business schools)
    for keyword in CATEGORIES['universities']['keywords']:
        if keyword in name_lower:
            # Make sure it's not a business school
            is_business = False
            for exclude in CATEGORIES['universities']['exclude']:
                if exclude in name_lower:
                    is_business = True
                    break
            if not is_business:
                return 'universities'
    
    # Default to companies
    return 'companies'

def get_region(filename):
    """Determine region based on filename patterns"""
    name_lower = filename.lower()
    
    # North America patterns
    na_patterns = ['harvard', 'stanford', 'mit', 'yale', 'princeton', 'columbia',
                   'wharton', 'kellogg', 'booth', 'sloan', 'mcgill', 'toronto',
                   'ubc', 'waterloo', 'queens', 'ivey', 'rotman', 'schulich']
    
    # Europe patterns  
    eu_patterns = ['insead', 'lbs', 'london', 'oxford', 'cambridge', 'imperial',
                   'warwick', 'manchester', 'hec', 'essec', 'escp', 'iese', 'esade',
                   'bocconi', 'eth', 'epfl', 'copenhagen', 'rotterdam', 'amsterdam']
    
    # Asia patterns
    asia_patterns = ['iim', 'isb', 'xlri', 'iit', 'nit', 'nus', 'ntu', 'hkust',
                     'cuhk', 'ceibs', 'fudan', 'tsinghua', 'peking', 'tokyo',
                     'keio', 'waseda', 'seoul', 'kaist', 'nanyang']
    
    for pattern in na_patterns:
        if pattern in name_lower:
            return 'north_america'
    
    for pattern in eu_patterns:
        if pattern in name_lower:
            return 'europe'
    
    for pattern in asia_patterns:
        if pattern in name_lower:
            return 'asia'
    
    return 'other'

def reorganize_logos():
    """Reorganize all logos into proper categories"""
    print("=" * 80)
    print("REORGANIZING LOGO COLLECTIONS")
    print("=" * 80)
    
    # Create directory structure
    create_directories()
    
    # Track statistics
    stats = defaultdict(lambda: defaultdict(int))
    all_files_processed = []
    
    # Process all existing directories
    source_dirs = []
    for category_info in CATEGORIES.values():
        source_dirs.extend(category_info['dirs'])
    
    # Also include the consolidated directory
    source_dirs.append('logos/all_unique_logos')
    
    # Remove duplicates
    source_dirs = list(set(source_dirs))
    
    print("\nProcessing logos from:")
    for dir_path in source_dirs:
        if os.path.exists(dir_path):
            print(f"  • {dir_path}")
    
    print("\nCategorizing and organizing...")
    
    # Process each source directory
    for source_dir in source_dirs:
        if not os.path.exists(source_dir):
            continue
        
        dir_name = os.path.basename(source_dir)
        print(f"\nProcessing {dir_name}...")
        
        for filename in os.listdir(source_dir):
            if not filename.endswith(('.png', '.jpg', '.jpeg', '.svg')):
                continue
            
            source_path = os.path.join(source_dir, filename)
            
            # Categorize the file
            category = categorize_file(filename)
            region = get_region(filename)
            
            # Determine destination
            if category == 'business_schools':
                dest_base = BUSINESS_SCHOOLS_DIR
            elif category == 'universities':
                dest_base = UNIVERSITIES_DIR
            else:
                dest_base = COMPANIES_DIR
            
            dest_dir = os.path.join(dest_base, region)
            dest_path = os.path.join(dest_dir, filename)
            
            # Handle duplicates by adding source directory to filename
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(filename)
                new_filename = f"{base}_{dir_name}{ext}"
                dest_path = os.path.join(dest_dir, new_filename)
            
            # Copy file
            try:
                shutil.copy2(source_path, dest_path)
                stats[category][region] += 1
                all_files_processed.append({
                    'source': source_path,
                    'destination': dest_path,
                    'category': category,
                    'region': region
                })
            except Exception as e:
                print(f"  Error copying {filename}: {e}")
    
    # Print statistics
    print("\n" + "=" * 80)
    print("REORGANIZATION COMPLETE")
    print("=" * 80)
    
    for category in ['business_schools', 'universities', 'companies']:
        total = sum(stats[category].values())
        print(f"\n{category.upper().replace('_', ' ')} ({total} total):")
        for region in ['north_america', 'europe', 'asia', 'other']:
            count = stats[category][region]
            if count > 0:
                print(f"  {region.replace('_', ' ').title()}: {count}")
    
    # Create summary report
    report = {
        'timestamp': os.path.getmtime('logos/all_unique_logos/SUMMARY.txt') if os.path.exists('logos/all_unique_logos/SUMMARY.txt') else None,
        'statistics': dict(stats),
        'total_files': len(all_files_processed),
        'structure': {
            'business_schools': "Separate logos for business schools (Wharton, Kellogg, INSEAD, etc.)",
            'universities': "Parent university logos (Harvard, MIT, Oxford, etc.)",
            'companies': "All employer logos (consulting, finance, tech, etc.)"
        }
    }
    
    report_path = os.path.join(OUTPUT_BASE, 'organization_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    # Create README
    readme_path = os.path.join(OUTPUT_BASE, 'README.md')
    with open(readme_path, 'w') as f:
        f.write("# Organized Logo Collection\n\n")
        f.write("This collection is organized into three main categories:\n\n")
        f.write("## 1. Business Schools\n")
        f.write("Separate logos for business schools, which often have distinct branding from their parent universities.\n")
        f.write("Examples: Wharton, Kellogg, Booth, Sloan, INSEAD, LBS, etc.\n\n")
        f.write("## 2. Universities\n")
        f.write("Logos for parent universities and educational institutions.\n")
        f.write("Examples: Harvard University, MIT, Oxford, Cambridge, IITs, etc.\n\n")
        f.write("## 3. Companies\n")
        f.write("All employer and company logos including:\n")
        f.write("- Consulting firms (McKinsey, BCG, Bain, etc.)\n")
        f.write("- Financial institutions (Goldman Sachs, JPMorgan, etc.)\n")
        f.write("- Technology companies (Google, Microsoft, startups, etc.)\n")
        f.write("- Law firms, airlines, healthcare, energy, and more\n\n")
        f.write("## Regional Organization\n")
        f.write("Within each category, logos are organized by region:\n")
        f.write("- `north_america/` - US and Canada\n")
        f.write("- `europe/` - UK, EU, and other European countries\n")
        f.write("- `asia/` - India, China, Japan, Southeast Asia, etc.\n")
        f.write("- `other/` - Rest of world and unclassified\n\n")
        f.write(f"Total logos: {len(all_files_processed)}\n")
    
    print(f"\n✅ Organized collection created in: {OUTPUT_BASE}")
    print(f"✅ Report saved to: {report_path}")
    print(f"✅ README saved to: {readme_path}")

if __name__ == "__main__":
    reorganize_logos()