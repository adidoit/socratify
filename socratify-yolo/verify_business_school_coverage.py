import os
import json
import re

# Load the business schools
with open('logos/top_business_schools.json', 'r') as f:
    categorized = json.load(f)

# Get all logo files from all directories
all_logo_files = []
logo_dirs = ['logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos', 'logos/business_school_logos']

for dir_path in logo_dirs:
    if os.path.exists(dir_path):
        for file in os.listdir(dir_path):
            if file.endswith(('.png', '.jpg', '.svg')):
                all_logo_files.append((file.lower(), os.path.join(dir_path, file)))

print(f"Total logo files found: {len(all_logo_files)}")

# Function to check if we have a logo for a school
def find_logo_for_school(school_name, logo_files):
    school_lower = school_name.lower()
    
    # Direct mappings for common patterns
    mappings = {
        'harvard business school': 'harvard',
        'stanford graduate school of business': 'stanford',
        'wharton school': 'wharton',
        'mit sloan': 'mit',
        'chicago booth': 'chicagobooth',
        'northwestern kellogg': 'kellogg',
        'columbia business school': 'columbia',
        'yale school of management': 'yale',
        'berkeley haas': 'haas',
        'dartmouth tuck': 'tuck',
        'duke fuqua': 'duke',
        'michigan ross': 'ross',
        'nyu stern': 'stern',
        'cornell johnson': 'johnson',
        'ucla anderson': 'anderson',
        'carnegie mellon tepper': 'tepper',
        'unc kenan-flagler': 'kenan',
        'ut austin mccombs': 'mccombs',
        'usc marshall': 'marshall',
        'georgetown mcdonough': 'georgetown',
        'indiana kelley': 'kelley',
        'uva darden': 'darden',
        'emory goizueta': 'goizueta',
        'rice jones': 'rice',
        'notre dame mendoza': 'mendoza',
        'washington university olin': 'olin',
        'georgia tech scheller': 'scheller',
        'vanderbilt owen': 'owen',
        'ohio state fisher': 'fisher',
        'penn state smeal': 'smeal'
    }
    
    # Check mappings first
    for pattern, search_term in mappings.items():
        if pattern in school_lower:
            for file_name, file_path in logo_files:
                if search_term in file_name:
                    return file_path
    
    # Extract key words from school name
    key_words = []
    # Look for distinctive school names
    distinctive_names = re.findall(r'\b(harvard|stanford|wharton|sloan|booth|kellogg|columbia|yale|haas|tuck|fuqua|ross|stern|johnson|anderson|tepper|kenan|flagler|mccombs|marshall|kelley|darden|goizueta|jones|mendoza|olin|scheller|owen|fisher|smeal|carlson|wisconsin|carey|warrington|terry|gies|marriott|questrom|cox|katz|tippie|krannert|merage|rady|manderson|babson)\b', school_lower)
    
    if distinctive_names:
        key_words.extend(distinctive_names)
    
    # Also try university name
    university_names = re.findall(r'university of (\w+)', school_lower)
    if university_names:
        key_words.extend(university_names)
    
    # Search for matches
    for key_word in key_words:
        if len(key_word) > 3:  # Skip short words
            for file_name, file_path in logo_files:
                if key_word in file_name:
                    return file_path
    
    return None

# Check each school
print("\n=== DETAILED COVERAGE BY REGION ===\n")

overall_found = 0
overall_total = 0

for region, schools in categorized.items():
    print(f"\n{region.upper().replace('_', ' ')}:")
    print("-" * 60)
    
    found = 0
    missing_schools = []
    
    for school in schools:
        logo_path = find_logo_for_school(school, all_logo_files)
        if logo_path:
            found += 1
            print(f"✓ {school}")
        else:
            missing_schools.append(school)
    
    print(f"\nMissing ({len(missing_schools)}):")
    for school in missing_schools:
        print(f"✗ {school}")
    
    print(f"\nRegion Summary: {found}/{len(schools)} ({found/len(schools)*100:.1f}%)")
    
    overall_found += found
    overall_total += len(schools)

print("\n" + "="*60)
print(f"OVERALL COVERAGE: {overall_found}/{overall_total} ({overall_found/overall_total*100:.1f}%)")
print("="*60)

# Save the truly missing schools
all_missing = []
for region, schools in categorized.items():
    for school in schools:
        if not find_logo_for_school(school, all_logo_files):
            all_missing.append(school)

with open('logos/truly_missing_business_schools.txt', 'w') as f:
    for school in all_missing:
        f.write(f"{school}\n")

print(f"\nSaved {len(all_missing)} truly missing schools to: logos/truly_missing_business_schools.txt")