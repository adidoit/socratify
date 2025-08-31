import json

# Load the results
with open('logos/download_results.json', 'r') as f:
    results = json.load(f)

# Count by status
status_counts = {}
for result in results:
    status = result['status']
    status_counts[status] = status_counts.get(status, 0) + 1

# Extract failed companies
failed_companies = [r['employer'] for r in results if r['status'] == 'failed']
skipped_companies = [r['employer'] for r in results if r['status'] == 'skipped']
successful_companies = [r['employer'] for r in results if r['status'] == 'success']

print("=== DOWNLOAD SUMMARY ===")
print(f"Total companies: {len(results)}")
print(f"Successful downloads: {status_counts.get('success', 0)}")
print(f"Failed downloads: {status_counts.get('failed', 0)}")
print(f"Skipped (placeholders): {status_counts.get('skipped', 0)}")

print("\n=== FAILED DOWNLOADS ===")
print(f"Total failed: {len(failed_companies)}")
for company in sorted(failed_companies):
    print(f"- {company}")

# Save failed companies to a separate file for manual handling
with open('logos/failed_companies.txt', 'w') as f:
    for company in sorted(failed_companies):
        f.write(f"{company}\n")

print(f"\nFailed companies saved to: logos/failed_companies.txt")