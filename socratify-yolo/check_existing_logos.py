import os
import re

# Read institution list
with open('logos/institutions_list.txt', 'r') as f:
    institutions = [line.strip() for line in f if line.strip()]

# Check existing logos in both directories
existing_logos = set()

# Check logos/downloaded directory
if os.path.exists('logos/downloaded'):
    for file in os.listdir('logos/downloaded'):
        if file.endswith(('.png', '.jpg', '.svg')):
            # Extract base name without extension
            base_name = os.path.splitext(file)[0].lower().replace('_', '').replace('-', '').replace(' ', '')
            existing_logos.add(base_name)

# Check logos/global_mba_logos directory
if os.path.exists('logos/global_mba_logos'):
    for file in os.listdir('logos/global_mba_logos'):
        if file.endswith(('.png', '.jpg', '.svg')):
            # Extract base name without extension
            base_name = os.path.splitext(file)[0].lower().replace('_', '').replace('-', '').replace(' ', '')
            existing_logos.add(base_name)

# Check which institutions we already have
already_have = []
need_to_download = []

for inst in institutions:
    # Normalize institution name for comparison
    inst_normalized = inst.lower().replace('_', '').replace('-', '').replace(' ', '')
    
    if inst_normalized in existing_logos:
        already_have.append(inst)
    else:
        need_to_download.append(inst)

print(f"Total institutions: {len(institutions)}")
print(f"Already have logos: {len(already_have)}")
print(f"Need to download: {len(need_to_download)}")

# Show some examples of what we already have
print("\nSample of existing logos:")
for inst in already_have[:20]:
    print(f"✓ {inst}")

print("\nSample of logos to download:")
for inst in need_to_download[:20]:
    print(f"✗ {inst}")

# Save the list of institutions to download
with open('logos/institutions_to_download.txt', 'w') as f:
    for inst in need_to_download:
        f.write(f"{inst}\n")