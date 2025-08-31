import json
import os

# Check if results file exists
results_file = 'logos/institution_download_results.json'
if os.path.exists(results_file):
    with open(results_file, 'r') as f:
        results = json.load(f)
else:
    print("Results file not found yet. Script may still be running.")
    exit()

# Count by status
status_counts = {}
for result in results:
    status = result['status']
    status_counts[status] = status_counts.get(status, 0) + 1

# Count total logos across all directories
total_logo_count = 0
logo_dirs = ['logos/downloaded', 'logos/global_mba_logos', 'logos/institution_logos']
all_logos = set()

for dir_path in logo_dirs:
    if os.path.exists(dir_path):
        for file in os.listdir(dir_path):
            if file.endswith(('.png', '.jpg', '.svg')):
                base_name = os.path.splitext(file)[0].lower()
                all_logos.add(base_name)
                total_logo_count += 1

print("=== INSTITUTION LOGOS DOWNLOAD SUMMARY ===")
print(f"Total institutions in list: 1,669")
print(f"Already had logos: 193")
print(f"Attempted to download: {len(results)}")
print(f"Successfully downloaded: {status_counts.get('success', 0)}")
print(f"Failed: {status_counts.get('failed', 0)}")
print(f"Skipped: {status_counts.get('skipped', 0)}")

if len(results) > 0:
    success_rate = status_counts.get('success', 0) / len(results) * 100
    print(f"Success rate: {success_rate:.1f}%")

print(f"\n=== TOTAL LOGO COLLECTION ===")
print(f"Total unique logos across all directories: {len(all_logos)}")
print(f"Total logo files: {total_logo_count}")
print(f"Average logos per institution: {total_logo_count / 1669:.1f}")

# Categorize by type
categories = {
    'universities': 0,
    'companies': 0,
    'organizations': 0,
    'financial': 0,
    'tech': 0,
    'media': 0,
    'other': 0
}

# Sample categorization based on institution names
for result in results[:500]:  # Sample first 500
    inst = result['institution'].lower()
    
    if any(word in inst for word in ['university', 'college', 'school', 'edu', 'iim', 'iit', 'institute']):
        categories['universities'] += 1
    elif any(word in inst for word in ['bank', 'capital', 'finance', 'invest', 'venture', 'fund']):
        categories['financial'] += 1
    elif any(word in inst for word in ['tech', 'software', 'data', 'cloud', 'digital', 'ai', 'net', 'web']):
        categories['tech'] += 1
    elif any(word in inst for word in ['news', 'media', 'tv', 'radio', 'times', 'post']):
        categories['media'] += 1
    elif any(word in inst for word in ['corp', 'inc', 'ltd', 'llc', 'company']):
        categories['companies'] += 1
    elif any(word in inst for word in ['org', 'foundation', 'association', 'society', 'council']):
        categories['organizations'] += 1
    else:
        categories['other'] += 1

print("\n=== INSTITUTION TYPES (sample of 500) ===")
for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    if count > 0:
        print(f"{cat.capitalize():<15} {count:>4} ({count/5:.0f}%)")

# List some successful downloads
successful = [r for r in results if r['status'] == 'success']
if successful:
    print(f"\n=== SAMPLE SUCCESSFUL DOWNLOADS ===")
    for result in successful[:20]:
        print(f"✓ {result['institution']}")
    if len(successful) > 20:
        print(f"... and {len(successful) - 20} more")

# List some failed downloads
failed = [r for r in results if r['status'] == 'failed']
if failed:
    print(f"\n=== SAMPLE FAILED DOWNLOADS ({len(failed)} total) ===")
    for result in failed[:20]:
        print(f"✗ {result['institution']}")
    if len(failed) > 20:
        print(f"... and {len(failed) - 20} more")

# File size statistics
print("\n=== FILE SIZE STATISTICS ===")
total_size = 0
file_count = 0

for dir_path in logo_dirs:
    if os.path.exists(dir_path):
        dir_size = 0
        dir_count = 0
        for file in os.listdir(dir_path):
            if file.endswith(('.png', '.jpg', '.svg')):
                filepath = os.path.join(dir_path, file)
                size = os.path.getsize(filepath)
                dir_size += size
                dir_count += 1
                total_size += size
                file_count += 1
        
        if dir_count > 0:
            print(f"{dir_path:<30} {dir_count:>4} files, {dir_size/1024/1024:>6.1f} MB")

if file_count > 0:
    print(f"\nTotal across all directories:   {file_count:>4} files, {total_size/1024/1024:>6.1f} MB")
    print(f"Average file size: {total_size/file_count/1024:.1f} KB")