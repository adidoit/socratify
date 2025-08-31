#!/usr/bin/env python3
import csv
import os
import re

def clean_for_matching(name):
    """Clean name for matching"""
    clean = name.lower()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    clean = ' '.join(clean.split())
    return clean

def main():
    print("="*80)
    print("FINAL LOGO INVENTORY REPORT")
    print("="*80)
    
    # Read all companies from CSV
    companies = []
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append({
                'name': row['Name'],
                'rank': int(row['Rank']),
                'country': row['country']
            })
    
    # Count existing logos
    logos_path = '../socratify-images/logos/images/companies/'
    logo_count = 0
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            logo_count += 1
    
    print(f"\n📊 STATISTICS:")
    print(f"   Total companies in CSV: {len(companies):,}")
    print(f"   Total logos in folder: {logo_count:,}")
    
    # Quick match check for top companies
    print(f"\n🏆 TOP 50 COMPANIES STATUS:")
    print("   Checking which of the top 50 have logos...")
    
    existing_logos = set()
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            clean_logo = clean_for_matching(filename[:-4])
            existing_logos.add(clean_logo)
    
    missing_top_50 = []
    have_top_50 = []
    
    for company in companies[:50]:
        clean_name = clean_for_matching(company['name'])
        found = False
        
        # Check various matching strategies
        if clean_name in existing_logos:
            found = True
        else:
            # Check partial matches
            for logo in existing_logos:
                if len(clean_name) > 5 and len(logo) > 5:
                    if clean_name in logo or logo in clean_name:
                        found = True
                        break
                # Check first word match for companies
                if clean_name.split()[0] == logo.split()[0] and len(clean_name.split()[0]) > 3:
                    found = True
                    break
        
        if found:
            have_top_50.append(company)
        else:
            missing_top_50.append(company)
    
    print(f"   ✅ Have logos: {len(have_top_50)}/50")
    print(f"   ❌ Missing logos: {len(missing_top_50)}/50")
    
    if missing_top_50:
        print(f"\n   Missing from top 50:")
        for company in missing_top_50:
            print(f"      {company['rank']:2d}. {company['name']} ({company['country']})")
    
    # Check top 100
    missing_top_100 = []
    have_top_100 = []
    
    for company in companies[:100]:
        clean_name = clean_for_matching(company['name'])
        found = False
        
        if clean_name in existing_logos:
            found = True
        else:
            for logo in existing_logos:
                if len(clean_name) > 5 and len(logo) > 5:
                    if clean_name in logo or logo in clean_name:
                        found = True
                        break
                if clean_name.split()[0] == logo.split()[0] and len(clean_name.split()[0]) > 3:
                    found = True
                    break
        
        if found:
            have_top_100.append(company)
        else:
            missing_top_100.append(company)
    
    print(f"\n🥈 TOP 100 COMPANIES:")
    print(f"   ✅ Have logos: {len(have_top_100)}/100")
    print(f"   ❌ Missing logos: {len(missing_top_100)}/100")
    
    # Summary by rank brackets
    print(f"\n📈 COVERAGE BY RANK:")
    brackets = [(1, 50), (51, 100), (101, 250), (251, 500), (501, 1000)]
    
    for start, end in brackets:
        bracket_companies = [c for c in companies if start <= c['rank'] <= end]
        have_count = 0
        
        for company in bracket_companies:
            clean_name = clean_for_matching(company['name'])
            found = False
            
            if clean_name in existing_logos:
                found = True
            else:
                for logo in existing_logos:
                    if len(clean_name) > 5 and len(logo) > 5:
                        if clean_name in logo or logo in clean_name:
                            found = True
                            break
            
            if found:
                have_count += 1
        
        coverage = (have_count / len(bracket_companies) * 100) if bracket_companies else 0
        print(f"   Rank {start:4d}-{end:4d}: {have_count:3d}/{len(bracket_companies):3d} ({coverage:.1f}%)")
    
    print(f"\n✨ SUMMARY:")
    print(f"   Started with: 8,194 logos")
    print(f"   Now have: {logo_count:,} logos")
    print(f"   Added: {logo_count - 8194:,} new logos")
    
    # Save missing top 100 for reference
    with open('final_missing_top100.txt', 'w') as f:
        f.write("Missing logos from top 100 companies:\n")
        f.write("="*50 + "\n")
        for company in missing_top_100:
            f.write(f"{company['rank']:3d}. {company['name']} ({company['country']})\n")
    
    if missing_top_100:
        print(f"\n📝 List of missing top 100 companies saved to: final_missing_top100.txt")

if __name__ == "__main__":
    main()