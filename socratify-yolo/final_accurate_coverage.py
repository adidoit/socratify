import os
import json

# Load the business schools
with open('logos/top_business_schools.json', 'r') as f:
    categorized = json.load(f)

# Count all logo files in business_school_logos directory
logo_dir = 'logos/business_school_logos'
logo_files = []
if os.path.exists(logo_dir):
    logo_files = [f for f in os.listdir(logo_dir) if f.endswith(('.png', '.jpg', '.svg'))]

print(f"Total logo files in business_school_logos directory: {len(logo_files)}")

# Also check other directories for business school logos
all_dirs = ['logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos', 'logos/business_school_logos']
all_logo_files = set()

for dir_path in all_dirs:
    if os.path.exists(dir_path):
        for file in os.listdir(dir_path):
            if file.endswith(('.png', '.jpg', '.svg')):
                all_logo_files.add(file.lower())

print(f"Total unique logo files across all directories: {len(all_logo_files)}")

# Detailed mapping to check coverage
found_schools = {}
missing_schools = {}

for region, schools in categorized.items():
    found_schools[region] = []
    missing_schools[region] = []
    
    for school in schools:
        found = False
        
        # Check various name patterns
        school_lower = school.lower()
        key_words = []
        
        # Extract key identifiers
        if 'harvard' in school_lower:
            key_words.append('harvard')
        if 'stanford' in school_lower:
            key_words.append('stanford')
        if 'wharton' in school_lower:
            key_words.append('wharton')
        if 'mit' in school_lower or 'sloan' in school_lower:
            key_words.append('mit')
        if 'chicago' in school_lower and 'booth' in school_lower:
            key_words.append('chicago')
        if 'kellogg' in school_lower:
            key_words.append('kellogg')
        if 'columbia' in school_lower:
            key_words.append('columbia')
        if 'yale' in school_lower:
            key_words.append('yale')
        if 'berkeley' in school_lower or 'haas' in school_lower:
            key_words.append('haas')
            key_words.append('berkeley')
        if 'tuck' in school_lower:
            key_words.append('tuck')
        if 'fuqua' in school_lower:
            key_words.append('duke')
        if 'ross' in school_lower:
            key_words.append('michigan')
        if 'stern' in school_lower:
            key_words.append('nyu')
        if 'anderson' in school_lower:
            key_words.append('ucla')
        if 'marshall' in school_lower:
            key_words.append('usc')
        if 'mcdonough' in school_lower:
            key_words.append('georgetown')
        if 'darden' in school_lower:
            key_words.append('virginia')
        if 'owen' in school_lower:
            key_words.append('vanderbilt')
        if 'fisher' in school_lower:
            key_words.append('ohio')
        if 'smeal' in school_lower:
            key_words.append('penn_state')
        
        # Also check the school name itself
        school_clean = school.replace(' - ', '_').replace(' ', '_').lower()
        
        # Check if we have a logo
        for logo_file in all_logo_files:
            if school_clean in logo_file:
                found = True
                break
            
            for key_word in key_words:
                if key_word in logo_file:
                    found = True
                    break
            
            if found:
                break
        
        if found:
            found_schools[region].append(school)
        else:
            missing_schools[region].append(school)

# Print detailed results
print("\n" + "="*70)
print("COMPREHENSIVE BUSINESS SCHOOL LOGO COVERAGE REPORT")
print("="*70)

total_found = 0
total_schools = 0

for region in categorized.keys():
    region_name = region.replace('_', ' ').upper()
    found_count = len(found_schools[region])
    total_count = len(categorized[region])
    percentage = (found_count / total_count * 100) if total_count > 0 else 0
    
    print(f"\n{region_name}:")
    print(f"Coverage: {found_count}/{total_count} ({percentage:.1f}%)")
    
    if found_count > 0:
        print(f"\n✓ Schools with logos ({found_count}):")
        for school in found_schools[region][:10]:
            print(f"  • {school}")
        if found_count > 10:
            print(f"  ... and {found_count - 10} more")
    
    if len(missing_schools[region]) > 0:
        print(f"\n✗ Missing logos ({len(missing_schools[region])}):")
        for school in missing_schools[region][:5]:
            print(f"  • {school}")
        if len(missing_schools[region]) > 5:
            print(f"  ... and {len(missing_schools[region]) - 5} more")
    
    total_found += found_count
    total_schools += total_count

print("\n" + "="*70)
print(f"OVERALL COVERAGE: {total_found}/{total_schools} ({total_found/total_schools*100:.1f}%)")
print("="*70)

# Count logos by directory
print("\n=== LOGO FILES BY DIRECTORY ===")
for dir_path in all_dirs:
    if os.path.exists(dir_path):
        count = len([f for f in os.listdir(dir_path) if f.endswith(('.png', '.jpg', '.svg'))])
        print(f"{dir_path}: {count} files")