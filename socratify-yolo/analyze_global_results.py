import json
import os

# Load the results
with open('logos/global_download_results.json', 'r') as f:
    results = json.load(f)

# Load the categorized employers
with open('logos/global_mba_employers_categorized.json', 'r') as f:
    categorized = json.load(f)

# Count by status
status_counts = {}
for result in results:
    status = result['status']
    status_counts[status] = status_counts.get(status, 0) + 1

# Success by category
category_success = {}
category_total = {}

# Create reverse mapping of company to category
company_to_category = {}
for category, companies in categorized.items():
    for company in companies:
        company_to_category[company] = category
        category_total[category] = category_total.get(category, 0) + 1

# Count successes by category
for result in results:
    if result['status'] == 'success':
        company = result['employer']
        if company in company_to_category:
            category = company_to_category[company]
            category_success[category] = category_success.get(category, 0) + 1

print("=== GLOBAL MBA EMPLOYERS LOGO DOWNLOAD SUMMARY ===")
print(f"Total companies processed: {len(results)}")
print(f"Successfully downloaded: {status_counts.get('success', 0)}")
print(f"Failed: {status_counts.get('failed', 0)}")
print(f"Skipped: {status_counts.get('skipped', 0)}")
print(f"Success rate: {status_counts.get('success', 0)/len(results)*100:.1f}%")

print("\n=== SUCCESS BY CATEGORY ===")
for category in sorted(category_total.keys()):
    success = category_success.get(category, 0)
    total = category_total[category]
    print(f"{category:<30} {success:>3}/{total:<3} ({success/total*100:.0f}%)")

print("\n=== GEOGRAPHIC DISTRIBUTION ===")
# Count by region
region_mapping = {
    'us_canada_specific': 'US/Canada',
    'europe_uk_specific': 'Europe/UK',
    'india_specific': 'India',
    'asia_pacific_specific': 'Asia-Pacific',
    'global_consulting': 'Global',
    'global_finance': 'Global',
    'global_tech': 'Global',
    'global_consumer': 'Global',
    'global_healthcare': 'Global',
    'global_industrial': 'Global',
    'global_energy': 'Global',
    'private_equity_venture': 'Global'
}

region_counts = {}
for result in results:
    if result['status'] == 'success':
        company = result['employer']
        if company in company_to_category:
            category = company_to_category[company]
            region = region_mapping.get(category, 'Other')
            region_counts[region] = region_counts.get(region, 0) + 1

for region, count in sorted(region_counts.items()):
    print(f"{region:<15} {count:>3} logos")

# List some failed companies
failed_companies = [r['employer'] for r in results if r['status'] == 'failed']
if failed_companies:
    print(f"\n=== SAMPLE FAILED DOWNLOADS ({len(failed_companies)} total) ===")
    for company in sorted(failed_companies)[:20]:
        print(f"- {company}")
    if len(failed_companies) > 20:
        print(f"... and {len(failed_companies) - 20} more")

# File size statistics
print("\n=== LOGO FILE STATISTICS ===")
total_size = 0
file_count = 0
for filename in os.listdir('logos/global_mba_logos'):
    filepath = os.path.join('logos/global_mba_logos', filename)
    if os.path.isfile(filepath):
        size = os.path.getsize(filepath)
        total_size += size
        file_count += 1

if file_count > 0:
    avg_size = total_size / file_count / 1024  # KB
    total_size_mb = total_size / (1024 * 1024)  # MB
    print(f"Total files: {file_count}")
    print(f"Total size: {total_size_mb:.1f} MB")
    print(f"Average file size: {avg_size:.1f} KB")