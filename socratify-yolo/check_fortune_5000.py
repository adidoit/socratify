#!/usr/bin/env python3
import csv
import os
import re

def normalize(name):
    """Simple normalization"""
    clean = name.lower()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    clean = ' '.join(clean.split())
    return clean

def main():
    print("="*80)
    print("FORTUNE 5000 COVERAGE CHECK")
    print("="*80)
    
    # Read companies
    companies = []
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rank = int(row['Rank'])
            if rank <= 5000:  # Fortune 5000
                companies.append({
                    'name': row['Name'],
                    'rank': rank,
                    'country': row['country']
                })
    
    print(f"\nTotal Fortune 5000 companies: {len(companies)}")
    
    # Get logos
    logos_path = '../socratify-images/logos/images/companies/'
    logo_count = len([f for f in os.listdir(logos_path) if f.endswith('.png')])
    print(f"Total logos in database: {logo_count}")
    
    # Quick coverage check by rank brackets
    print("\nFORTUNE 5000 COVERAGE BY BRACKET:")
    print("-" * 50)
    
    brackets = [
        (1, 100, "Fortune 100"),
        (1, 500, "Fortune 500"),
        (1, 1000, "Fortune 1000"),
        (1001, 2000, "1001-2000"),
        (2001, 3000, "2001-3000"),
        (3001, 4000, "3001-4000"),
        (4001, 5000, "4001-5000"),
        (1, 5000, "TOTAL Fortune 5000")
    ]
    
    # Get all logo names for matching
    existing_logos = set()
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            logo_name = filename[:-4]
            existing_logos.add(normalize(logo_name))
    
    for start, end, label in brackets:
        bracket_companies = [c for c in companies if start <= c['rank'] <= end]
        
        # Estimate coverage (simplified matching)
        matched = 0
        for company in bracket_companies:
            norm_name = normalize(company['name'])
            # Check various matching strategies
            if norm_name in existing_logos:
                matched += 1
            else:
                # Check partial matches
                words = norm_name.split()
                if words and words[0] in existing_logos:
                    matched += 1
                else:
                    # Check if any logo contains the company name
                    for logo in existing_logos:
                        if len(norm_name) > 5 and (norm_name in logo or logo in norm_name):
                            matched += 1
                            break
        
        coverage = (matched / len(bracket_companies) * 100) if bracket_companies else 0
        missing = len(bracket_companies) - matched
        
        if label == "TOTAL Fortune 5000":
            print("-" * 50)
        
        print(f"{label:20s}: {matched:4d}/{len(bracket_companies):4d} ({coverage:5.1f}%) - Missing: ~{missing:4d}")
    
    print("\n" + "="*80)
    print("SUMMARY:")
    print("="*80)
    
    # Calculate overall Fortune 5000 coverage
    fortune_5000 = [c for c in companies if c['rank'] <= 5000]
    estimated_matched = 0
    
    for company in fortune_5000:
        norm_name = normalize(company['name'])
        if norm_name in existing_logos:
            estimated_matched += 1
        else:
            words = norm_name.split()
            if words and len(words[0]) > 2:
                for logo in existing_logos:
                    if words[0] in logo or norm_name in logo or logo in norm_name:
                        estimated_matched += 1
                        break
    
    coverage = (estimated_matched / len(fortune_5000) * 100) if fortune_5000 else 0
    
    print(f"✅ Fortune 5000 companies with logos: ~{estimated_matched:,} ({coverage:.1f}%)")
    print(f"❌ Fortune 5000 companies missing logos: ~{len(fortune_5000) - estimated_matched:,}")
    
    if coverage >= 90:
        print("\n🎉 EXCELLENT! Over 90% of Fortune 5000 companies have logos!")
    elif coverage >= 75:
        print("\n👍 GOOD! Over 75% of Fortune 5000 companies have logos!")
    elif coverage >= 60:
        print("\n📈 SOLID! Over 60% of Fortune 5000 companies have logos!")
    else:
        print(f"\n📊 Current coverage is {coverage:.1f}% - room for improvement")
    
    print("\nNOTE: This is an estimated coverage based on name matching.")
    print("Some companies may have logos under slightly different names.")

if __name__ == "__main__":
    main()