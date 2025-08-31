#!/usr/bin/env python3
"""
Quick summary of duplicate situation
"""

import json

# Load the duplicate analysis report
with open('logos/duplicate_analysis_report.json', 'r') as f:
    report = json.load(f)

print("=" * 80)
print("DUPLICATE ANALYSIS SUMMARY")
print("=" * 80)

print(f"\nTotal files scanned: {report['total_files']:,}")
print(f"Exact duplicates: {report['exact_duplicates_count']} files in {report['exact_duplicate_groups']} groups")
print(f"Name-based duplicates: {report['name_duplicates_count']} files in {report['name_duplicate_groups']} groups")

# Analyze which directories have most duplicates
dir_duplicates = {}
for hash_val, files in report['exact_duplicates'].items():
    for file_info in files:
        dir_name = file_info['path'].split('/')[1]  # Get directory name
        dir_duplicates[dir_name] = dir_duplicates.get(dir_name, 0) + 1

print("\n\nDuplicates by directory:")
for dir_name, count in sorted(dir_duplicates.items(), key=lambda x: x[1], reverse=True):
    print(f"  {dir_name:<30} {count:>4} duplicate files")

# Show the most duplicated files
print("\n\nMost duplicated files (by exact match):")
sorted_groups = sorted(report['exact_duplicates'].items(), 
                      key=lambda x: len(x[1]), reverse=True)[:10]

for i, (hash_val, files) in enumerate(sorted_groups):
    print(f"\n{i+1}. {len(files)} identical copies:")
    # Get the filename from the first file
    filename = files[0]['path'].split('/')[-1]
    print(f"   File: {filename}")
    print(f"   Size: {files[0]['size']:,} bytes")
    print("   Locations:")
    for f in files[:5]:
        print(f"     - {f['path']}")
    if len(files) > 5:
        print(f"     ... and {len(files) - 5} more locations")

# Estimate collection after deduplication
estimated_unique = report['total_files'] - report['exact_duplicates_count']
print(f"\n\nEstimated unique files after removing exact duplicates: {estimated_unique:,}")
print(f"Space that could be saved: ~{report['exact_duplicates_count'] * 50 / 1024:.1f} MB")

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)
print("\n1. Move the 304 exact duplicates to a 'duplicates' folder")
print("2. This will reduce the collection from 3,172 to ~2,868 files")
print("3. The name-based duplicates (122 files) need manual review")
print("4. Final collection would have ~2,800-2,850 unique organization logos")
print("\nRun 'python manage_duplicates.py' to safely move duplicates")