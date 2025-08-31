import re

# Read the list file
with open('logos/list.txt', 'r') as f:
    lines = f.readlines()

# Extract institution names (remove .json and clean up)
institutions = []
for line in lines:
    line = line.strip()
    if line and '.json' in line:
        # Remove .json extension
        name = line.replace('.json', '')
        # Skip metadata files
        if name not in ['favicon_metadata_bulk', 'favicon_metadata_bulk.jsonl']:
            institutions.append(name)

# Sort and save
institutions.sort()

print(f"Found {len(institutions)} institutions")

# Save to file
with open('logos/institutions_list.txt', 'w') as f:
    for inst in institutions:
        f.write(f"{inst}\n")

# Show first 20 as sample
print("\nSample institutions:")
for inst in institutions[:20]:
    print(f"- {inst}")