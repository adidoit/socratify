#!/usr/bin/env python3
"""
Analyze results from comprehensive global download
"""

import json
import os
from collections import defaultdict

# Load results
if os.path.exists('logos/comprehensive_global_results.json'):
    with open('logos/comprehensive_global_results.json', 'r') as f:
        results = json.load(f)
    
    # Analyze by status
    status_counts = defaultdict(int)
    category_stats = defaultdict(lambda: defaultdict(int))
    
    # Import categories
    from global_employers_comprehensive import (
        ASIA_PACIFIC_COMPANIES, MIDDLE_EAST_COMPANIES, LATIN_AMERICAN_COMPANIES,
        AFRICAN_COMPANIES, LUXURY_RETAIL_COMPANIES, PHARMA_HEALTHCARE_COMPANIES,
        ENERGY_INFRASTRUCTURE_COMPANIES, GOVERNMENT_MULTILATERAL_ORGS,
        BOUTIQUE_FIRMS, MEDIA_ENTERTAINMENT_COMPANIES, REAL_ESTATE_COMPANIES
    )
    
    categories = [
        ("ASIA-PACIFIC", ASIA_PACIFIC_COMPANIES),
        ("MIDDLE EAST", MIDDLE_EAST_COMPANIES),
        ("LATIN AMERICA", LATIN_AMERICAN_COMPANIES),
        ("AFRICA", AFRICAN_COMPANIES),
        ("LUXURY/RETAIL", LUXURY_RETAIL_COMPANIES),
        ("PHARMA/HEALTHCARE", PHARMA_HEALTHCARE_COMPANIES),
        ("ENERGY/INFRASTRUCTURE", ENERGY_INFRASTRUCTURE_COMPANIES),
        ("GOVERNMENT/MULTILATERAL", GOVERNMENT_MULTILATERAL_ORGS),
        ("BOUTIQUE FIRMS", BOUTIQUE_FIRMS),
        ("MEDIA/ENTERTAINMENT", MEDIA_ENTERTAINMENT_COMPANIES),
        ("REAL ESTATE", REAL_ESTATE_COMPANIES)
    ]
    
    # Count statuses
    for result in results:
        status_counts[result['status']] += 1
        
        # Find category
        company = result['company']
        for cat_name, cat_companies in categories:
            if company in cat_companies:
                category_stats[cat_name][result['status']] += 1
                break
    
    # Print summary
    print("=" * 80)
    print("COMPREHENSIVE GLOBAL DOWNLOAD ANALYSIS")
    print("=" * 80)
    print(f"\nTotal companies processed: {len(results)}")
    print(f"Success: {status_counts['success']}")
    print(f"Already exists: {status_counts['already_exists']}")
    print(f"Failed: {status_counts['failed']}")
    print(f"Overall coverage: {(status_counts['success'] + status_counts['already_exists'])/len(results)*100:.1f}%")
    
    print("\n" + "=" * 80)
    print("BREAKDOWN BY CATEGORY")
    print("=" * 80)
    
    for cat_name, cat_companies in categories:
        stats = category_stats[cat_name]
        total = sum(stats.values())
        if total > 0:
            coverage = (stats['success'] + stats['already_exists']) / total * 100
            print(f"\n{cat_name}:")
            print(f"  Total: {total}")
            print(f"  New downloads: {stats['success']}")
            print(f"  Already existed: {stats['already_exists']}")
            print(f"  Failed: {stats['failed']}")
            print(f"  Coverage: {coverage:.1f}%")
    
    # Check logo directory
    if os.path.exists('logos/comprehensive_global'):
        logo_count = len([f for f in os.listdir('logos/comprehensive_global') 
                         if f.endswith(('.png', '.jpg', '.svg'))])
        print(f"\n\nNew logos downloaded to comprehensive_global: {logo_count}")
    
    # List some failures
    failures = [r for r in results if r['status'] == 'failed']
    if failures:
        print(f"\n\nFAILED DOWNLOADS ({len(failures)} total):")
        for r in failures[:20]:
            print(f"  • {r['company']} ({r['domain']})")
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more")
else:
    print("Results file not found!")