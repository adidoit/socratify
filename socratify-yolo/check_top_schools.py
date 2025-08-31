#!/usr/bin/env python3
"""
Check which top business schools we're actually missing
"""

import os
import json

# Top US business schools that should definitely have logos
top_schools = [
    "Harvard Business School",
    "Stanford Graduate School of Business", 
    "Wharton School",
    "MIT Sloan School of Management",
    "Chicago Booth School of Business",
    "Northwestern Kellogg School of Management",
    "Columbia Business School",
    "UC Berkeley Haas School of Business",
    "Yale School of Management",
    "Dartmouth Tuck School of Business",
    "Michigan Ross School of Business",
    "Duke Fuqua School of Business",
    "NYU Stern School of Business",
    "Cornell Johnson School of Management",
    "UCLA Anderson School of Management",
    "USC Marshall School of Business",
    "Georgetown McDonough School of Business",
    "UNC Kenan-Flagler Business School",
    "Carnegie Mellon Tepper School of Business",
    "Emory Goizueta Business School"
]

# Get all logo files
all_logo_files = []
logo_dirs = ['logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos', 
             'logos/business_school_logos', 'logos/comprehensive_fix']

for dir_path in logo_dirs:
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        all_logo_files.extend([f.lower() for f in files if f.endswith(('.png', '.jpg', '.svg'))])

print("=" * 70)
print("TOP 20 US BUSINESS SCHOOLS - LOGO COVERAGE CHECK")
print("=" * 70)

found = []
missing = []

for school in top_schools:
    # Check various name patterns
    school_lower = school.lower()
    key_words = []
    
    # Extract key identifiers
    if 'harvard' in school_lower:
        key_words.extend(['harvard', 'hbs'])
    elif 'stanford' in school_lower:
        key_words.extend(['stanford', 'gsb'])
    elif 'wharton' in school_lower:
        key_words.extend(['wharton', 'upenn', 'pennsylvania'])
    elif 'sloan' in school_lower:
        key_words.extend(['mit', 'sloan'])
    elif 'booth' in school_lower:
        key_words.extend(['chicago', 'booth', 'uchicago'])
    elif 'kellogg' in school_lower:
        key_words.extend(['northwestern', 'kellogg'])
    elif 'columbia' in school_lower:
        key_words.extend(['columbia'])
    elif 'haas' in school_lower:
        key_words.extend(['berkeley', 'haas', 'ucb', 'cal'])
    elif 'yale' in school_lower:
        key_words.extend(['yale', 'som'])
    elif 'tuck' in school_lower:
        key_words.extend(['dartmouth', 'tuck'])
    elif 'ross' in school_lower:
        key_words.extend(['michigan', 'ross', 'umich'])
    elif 'fuqua' in school_lower:
        key_words.extend(['duke', 'fuqua'])
    elif 'stern' in school_lower:
        key_words.extend(['nyu', 'stern'])
    elif 'johnson' in school_lower:
        key_words.extend(['cornell', 'johnson'])
    elif 'anderson' in school_lower:
        key_words.extend(['ucla', 'anderson'])
    elif 'marshall' in school_lower:
        key_words.extend(['usc', 'marshall'])
    elif 'mcdonough' in school_lower:
        key_words.extend(['georgetown', 'mcdonough'])
    elif 'kenan-flagler' in school_lower:
        key_words.extend(['unc', 'kenan', 'flagler', 'carolina'])
    elif 'tepper' in school_lower:
        key_words.extend(['carnegie', 'mellon', 'tepper', 'cmu'])
    elif 'goizueta' in school_lower:
        key_words.extend(['emory', 'goizueta'])
    
    # Check if we have any matching logo
    logo_found = False
    matching_file = None
    
    for logo_file in all_logo_files:
        for keyword in key_words:
            if keyword in logo_file:
                logo_found = True
                matching_file = logo_file
                break
        if logo_found:
            break
    
    if logo_found:
        found.append((school, matching_file))
        print(f"✓ {school:<50} → {matching_file}")
    else:
        missing.append(school)
        print(f"✗ {school:<50} → NOT FOUND")

print("\n" + "=" * 70)
print(f"SUMMARY: {len(found)}/{len(top_schools)} logos found ({len(found)/len(top_schools)*100:.1f}%)")
print(f"Missing: {len(missing)} critical business school logos")
print("=" * 70)

if missing:
    print("\nMISSING SCHOOLS:")
    for school in missing:
        print(f"  • {school}")

# Check what files contain "Michigan" or "Ross"
print("\n" + "=" * 70)
print("SPECIFIC CHECK: Files containing 'Michigan' or 'Ross'")
print("=" * 70)

michigan_files = [f for f in all_logo_files if 'michigan' in f or 'ross' in f]
if michigan_files:
    for f in michigan_files:
        print(f"  • {f}")
else:
    print("  No files found containing 'Michigan' or 'Ross'")

# Let's also check the actual download results
print("\n" + "=" * 70)
print("CHECKING DOWNLOAD RESULTS FOR MICHIGAN/ROSS")
print("=" * 70)

result_files = [
    'logos/download_results.json',
    'logos/business_school_download_results.json', 
    'logos/domain_download_results.json',
    'logos/final_business_school_results.json'
]

for result_file in result_files:
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            results = json.load(f)
        
        for result in results:
            name = result.get('school', result.get('employer', result.get('institution', '')))
            if 'michigan' in name.lower() or 'ross' in name.lower():
                status = result.get('status', 'unknown')
                print(f"{result_file}: {name} - Status: {status}")
                if status == 'success':
                    print(f"  → File: {result.get('filepath', result.get('filename', 'N/A'))}")