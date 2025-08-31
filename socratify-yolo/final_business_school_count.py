#!/usr/bin/env python3
"""
Final count of all business school logos across all directories
"""

import os
from collections import defaultdict

# All directories containing logos
logo_directories = [
    'logos/downloaded',
    'logos/global_mba_logos', 
    'logos/institution_logos',
    'logos/business_school_logos',
    'logos/comprehensive_fix',
    'logos/expanded_business_schools'
]

# Count logos by directory and overall
all_logos = set()
directory_counts = {}
business_school_logos = set()

# Keywords that identify business schools
business_keywords = [
    'business', 'school', 'college', 'mba', 'management', 'iim', 'insead', 
    'wharton', 'booth', 'sloan', 'kellogg', 'ross', 'stern', 'haas', 
    'anderson', 'fuqua', 'tuck', 'darden', 'johnson', 'tepper', 'owen',
    'fisher', 'smeal', 'marshall', 'mcdonough', 'kenan', 'goizueta'
]

for dir_path in logo_directories:
    if os.path.exists(dir_path):
        files = [f for f in os.listdir(dir_path) if f.endswith(('.png', '.jpg', '.svg'))]
        directory_counts[dir_path] = len(files)
        
        for file in files:
            all_logos.add(file.lower())
            
            # Check if it's likely a business school
            file_lower = file.lower()
            if any(keyword in file_lower for keyword in business_keywords):
                business_school_logos.add(file)

# Count total unique logos
print("=" * 80)
print("COMPREHENSIVE BUSINESS SCHOOL LOGO COUNT")
print("=" * 80)

print("\n📁 LOGOS BY DIRECTORY:")
total_files = 0
for dir_path, count in sorted(directory_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{dir_path:<45} {count:>6} files")
    total_files += count

print(f"\nTotal logo files (including duplicates): {total_files:,}")
print(f"Total unique logos: {len(all_logos):,}")
print(f"Likely business school logos: {len(business_school_logos):,}")

# Check coverage of our expanded list
from expanded_business_schools import get_all_schools_with_domains

all_target_schools = get_all_schools_with_domains()
found_schools = []
missing_schools = []

for school_name, domain in all_target_schools.items():
    school_clean = school_name.replace(' ', '_').replace('/', '_').replace(':', '').lower()
    
    # Check if we have this school
    found = False
    for logo in all_logos:
        if school_clean in logo or domain.split('.')[0] in logo:
            found = True
            break
    
    if found:
        found_schools.append(school_name)
    else:
        missing_schools.append((school_name, domain))

print("\n📊 EXPANDED BUSINESS SCHOOL COVERAGE:")
print(f"Target schools: {len(all_target_schools)}")
print(f"Found: {len(found_schools)} ({len(found_schools)/len(all_target_schools)*100:.1f}%)")
print(f"Missing: {len(missing_schools)} ({len(missing_schools)/len(all_target_schools)*100:.1f}%)")

# Show missing schools by region
if missing_schools:
    print("\n❌ STILL MISSING SCHOOLS:")
    
    # Categorize by region
    us_missing = []
    europe_missing = []
    india_missing = []
    canada_missing = []
    
    for school, domain in missing_schools:
        if domain.endswith('.edu') or 'US' in school:
            us_missing.append((school, domain))
        elif domain.endswith('.ac.in') or 'IIM' in school or 'India' in school:
            india_missing.append((school, domain))
        elif domain.endswith('.ca') or 'Canada' in school or 'University' in school and domain.endswith('.ca'):
            canada_missing.append((school, domain))
        else:
            europe_missing.append((school, domain))
    
    if us_missing:
        print(f"\nUS ({len(us_missing)} missing):")
        for school, domain in us_missing[:5]:
            print(f"  • {school} ({domain})")
        if len(us_missing) > 5:
            print(f"  ... and {len(us_missing) - 5} more")
    
    if europe_missing:
        print(f"\nEurope ({len(europe_missing)} missing):")
        for school, domain in europe_missing[:5]:
            print(f"  • {school} ({domain})")
        if len(europe_missing) > 5:
            print(f"  ... and {len(europe_missing) - 5} more")
    
    if india_missing:
        print(f"\nIndia ({len(india_missing)} missing):")
        for school, domain in india_missing[:5]:
            print(f"  • {school} ({domain})")
        if len(india_missing) > 5:
            print(f"  ... and {len(india_missing) - 5} more")
    
    if canada_missing:
        print(f"\nCanada ({len(canada_missing)} missing):")
        for school, domain in canada_missing[:5]:
            print(f"  • {school} ({domain})")
        if len(canada_missing) > 5:
            print(f"  ... and {len(canada_missing) - 5} more")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"✅ Successfully collected {len(found_schools)} out of {len(all_target_schools)} target business schools")
print(f"✅ Overall coverage: {len(found_schools)/len(all_target_schools)*100:.1f}%")
print(f"✅ Total unique logo files: {len(all_logos):,}")
print("=" * 80)