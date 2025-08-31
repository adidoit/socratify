import os
import json
import re

# Load business schools list
with open('logos/all_business_schools.txt', 'r') as f:
    business_schools = [line.strip() for line in f if line.strip()]

# Check existing logos in all directories
existing_logos = {}
logo_dirs = ['logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos']

for dir_path in logo_dirs:
    if os.path.exists(dir_path):
        for file in os.listdir(dir_path):
            if file.endswith(('.png', '.jpg', '.svg')):
                # Extract base name without extension
                base_name = os.path.splitext(file)[0].lower()
                # Clean it up
                clean_name = base_name.replace('_', ' ').replace('-', ' ')
                existing_logos[clean_name] = os.path.join(dir_path, file)

# Function to normalize school names for matching
def normalize_name(name):
    # Remove common words and punctuation
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    
    # Remove common words
    remove_words = [
        'school', 'of', 'business', 'management', 'graduate', 'college',
        'university', 'faculty', 'the', 'at', 'and', 'administration'
    ]
    
    words = name.split()
    words = [w for w in words if w not in remove_words]
    
    return ' '.join(words)

# Check which schools we have logos for
have_logos = []
missing_logos = []

for school in business_schools:
    found = False
    school_normalized = normalize_name(school)
    
    # Check exact matches first
    if school.lower() in existing_logos:
        have_logos.append((school, existing_logos[school.lower()]))
        found = True
    else:
        # Check normalized matches
        for logo_name, logo_path in existing_logos.items():
            logo_normalized = normalize_name(logo_name)
            
            # Check if key words match
            if school_normalized and logo_normalized:
                school_words = set(school_normalized.split())
                logo_words = set(logo_normalized.split())
                
                # If significant overlap, consider it a match
                common_words = school_words & logo_words
                if len(common_words) >= 2 or (len(common_words) >= 1 and len(school_words) <= 2):
                    have_logos.append((school, logo_path))
                    found = True
                    break
    
    if not found:
        missing_logos.append(school)

# Load categorized schools
with open('logos/top_business_schools.json', 'r') as f:
    categorized = json.load(f)

# Analyze by region
print("=== BUSINESS SCHOOL LOGOS STATUS ===")
print(f"Total business schools: {len(business_schools)}")
print(f"Have logos: {len(have_logos)}")
print(f"Missing logos: {len(missing_logos)}")
print(f"Coverage: {len(have_logos)/len(business_schools)*100:.1f}%")

print("\n=== COVERAGE BY REGION ===")
for region, schools in categorized.items():
    have_count = sum(1 for school in schools if school not in missing_logos)
    total = len(schools)
    print(f"{region:<20} {have_count:>3}/{total:<3} ({have_count/total*100:>5.1f}%)")

print("\n=== SAMPLE OF SCHOOLS WITH LOGOS ===")
for school, path in have_logos[:10]:
    filename = os.path.basename(path)
    print(f"✓ {school:<50} → {filename}")

print("\n=== MISSING LOGOS BY REGION ===")
for region, schools in categorized.items():
    region_missing = [s for s in schools if s in missing_logos]
    if region_missing:
        print(f"\n{region.upper()} ({len(region_missing)} missing):")
        for school in region_missing[:5]:
            print(f"  - {school}")
        if len(region_missing) > 5:
            print(f"  ... and {len(region_missing) - 5} more")

# Save missing schools list
with open('logos/missing_business_schools.txt', 'w') as f:
    for school in missing_logos:
        f.write(f"{school}\n")

print(f"\nMissing schools saved to: logos/missing_business_schools.txt")