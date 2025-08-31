#!/usr/bin/env python3
import csv
import os
import re
import json

def clean_name_for_comparison(name):
    """Clean company name for comparison"""
    # Convert to lowercase and remove special characters
    clean = name.lower()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    clean = ' '.join(clean.split())
    
    # Remove common suffixes
    suffixes = ['inc', 'corp', 'corporation', 'company', 'limited', 'ltd', 'llc',
                'group', 'holdings', 'international', 'global', 'ag', 'sa', 'ab', 
                'nv', 'plc', 'gmbh', 'spa', 'the']
    words = clean.split()
    filtered = [w for w in words if w not in suffixes]
    return ' '.join(filtered) if filtered else clean

def main():
    print("="*70)
    print("FAST LOGO ANALYSIS")
    print("="*70)
    
    # Read companies from CSV
    print("\n1. Reading companies from CSV...")
    companies = []
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append({
                'original_name': row['Name'],
                'clean_name': clean_name_for_comparison(row['Name']),
                'rank': int(row['Rank']),
                'country': row['country']
            })
    print(f"   Found {len(companies)} companies")
    
    # Get existing logos
    print("\n2. Reading existing logo files...")
    logos_path = '../socratify-images/logos/images/companies/'
    existing_logos = set()
    existing_logo_files = {}
    
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            logo_name = filename[:-4]
            clean_logo = clean_name_for_comparison(logo_name)
            existing_logos.add(clean_logo)
            existing_logo_files[clean_logo] = filename
    
    print(f"   Found {len(existing_logos)} logo files")
    
    # Quick matching
    print("\n3. Matching companies to logos...")
    matched = []
    unmatched = []
    
    # Also check for common name mappings
    name_mappings = {
        'walmart': ['wal mart', 'walmex'],
        'amazon': ['amazon com'],
        'foxconn': ['hon hai', 'foxconn industrial'],
        'deutsche post': ['dhl'],
        'ups': ['united parcel service'],
        'jpmorgan': ['jpmorgan chase', 'jp morgan'],
        'bank america': ['bank of america', 'bofa'],
        'wells fargo': ['wells'],
        'unitedhealth': ['united health', 'unitedhealthgroup'],
        'alphabet': ['google'],
        'meta': ['facebook', 'meta platforms'],
        'coca cola': ['coke', 'coca cola femsa'],
        'pepsico': ['pepsi'],
        'starbucks': ['sbux'],
        'microsoft': ['msft'],
        'apple': ['aapl'],
        'general electric': ['ge'],
        'general motors': ['gm'],
        'ford': ['ford motor'],
        'att': ['at t'],
        'verizon': ['vz'],
        'disney': ['walt disney'],
        'nestle': ['nestlé'],
        'icbc': ['industrial commercial bank china'],
        'volkswagen': ['vw'],
        'mercedes': ['mercedes benz', 'daimler'],
        'bmw': ['bayerische motoren werke'],
        'toyota': ['toyota industries', 'toyota tsusho'],
        'honda': ['honda motor'],
        'nissan': ['nissan motor'],
        'tencent': ['tencent holdings'],
        'alibaba': ['alibaba group'],
        'samsung': ['samsung electronics'],
        'tsmc': ['taiwan semiconductor'],
        'johnson johnson': ['j j', 'jnj'],
        'procter gamble': ['p g', 'pg'],
        'caterpillar': ['cat'],
        'john deere': ['deere company'],
        'nike': ['nke'],
        'adidas': ['addidas'],
        '3m': ['mmm'],
        'fedex': ['federal express'],
        'berkshire': ['berkshire hathaway'],
        'goldman': ['goldman sachs'],
        'morgan stanley': ['morgan'],
        'tesla': ['tsla'],
        'chevron': ['cvx'],
        'exxon': ['exxon mobil', 'exxonmobil'],
        'boeing': ['ba'],
        'lockheed': ['lockheed martin'],
        'raytheon': ['rtx'],
        'northrop': ['northrop grumman']
    }
    
    # Create reverse mappings
    reverse_mappings = {}
    for key, values in name_mappings.items():
        for value in values:
            reverse_mappings[value] = key
    
    for company in companies:
        clean = company['clean_name']
        found = False
        
        # Direct match
        if clean in existing_logos:
            matched.append(company)
            found = True
        # Check mappings
        elif clean in reverse_mappings and reverse_mappings[clean] in existing_logos:
            matched.append(company)
            found = True
        else:
            # Check if any existing logo contains the company name or vice versa
            for logo_name in existing_logos:
                if len(clean) > 3 and len(logo_name) > 3:
                    if clean in logo_name or logo_name in clean:
                        matched.append(company)
                        found = True
                        break
                # Check mapped names
                if clean in name_mappings:
                    for variant in name_mappings[clean]:
                        if variant in logo_name or logo_name in variant:
                            matched.append(company)
                            found = True
                            break
                if found:
                    break
        
        if not found:
            unmatched.append(company)
    
    # Sort unmatched by rank
    unmatched.sort(key=lambda x: x['rank'])
    
    print(f"   ✓ Matched: {len(matched)} companies")
    print(f"   ✗ Missing: {len(unmatched)} companies")
    
    # Show top missing
    print(f"\n4. Top 100 missing companies:")
    for company in unmatched[:100]:
        print(f"   {company['rank']:4d}. {company['original_name']}")
    
    # Save results
    with open('missing_logos_fast.json', 'w') as f:
        json.dump(unmatched, f, indent=2)
    
    # Save simple text list
    with open('missing_companies_list.txt', 'w') as f:
        for company in unmatched:
            f.write(f"{company['rank']},{company['original_name']}\n")
    
    print(f"\n5. Summary:")
    print(f"   Total companies: {len(companies)}")
    print(f"   Have logos: {len(matched)} ({len(matched)/len(companies)*100:.1f}%)")
    print(f"   Missing logos: {len(unmatched)} ({len(unmatched)/len(companies)*100:.1f}%)")
    
    # By rank
    print(f"\n   Missing by rank:")
    print(f"   Rank 1-100: {len([c for c in unmatched if c['rank'] <= 100])}")
    print(f"   Rank 1-500: {len([c for c in unmatched if c['rank'] <= 500])}")
    print(f"   Rank 1-1000: {len([c for c in unmatched if c['rank'] <= 1000])}")

if __name__ == "__main__":
    main()