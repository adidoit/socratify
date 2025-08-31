#!/usr/bin/env python3
import csv
import os
import re
from collections import defaultdict

def normalize_for_matching(name):
    """Aggressive normalization for matching"""
    # Remove special characters and make lowercase
    clean = name.lower()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    
    # Remove common words that might differ
    remove_words = [
        'the', 'inc', 'corp', 'corporation', 'company', 'limited', 'ltd', 
        'llc', 'group', 'holdings', 'international', 'global', 'ag', 'sa', 
        'ab', 'nv', 'plc', 'gmbh', 'spa', 'se', 'co', 'of', 'and', 'amp'
    ]
    
    words = clean.split()
    words = [w for w in words if w not in remove_words]
    
    return ' '.join(words).strip()

def get_all_possible_matches(name):
    """Generate all possible name variations"""
    variations = set()
    
    # Original normalized
    variations.add(normalize_for_matching(name))
    
    # Remove parenthetical content
    if '(' in name:
        base = name.split('(')[0].strip()
        variations.add(normalize_for_matching(base))
        if ')' in name:
            inner = name.split('(')[1].split(')')[0].strip()
            variations.add(normalize_for_matching(inner))
    
    # Handle ampersands
    if '&amp;' in name:
        variations.add(normalize_for_matching(name.replace('&amp;', 'and')))
        variations.add(normalize_for_matching(name.replace('&amp;', '')))
    
    # Common abbreviations/mappings
    mappings = {
        'deutsche post': 'dhl',
        'united parcel service': 'ups',
        'federal express': 'fedex',
        'international business machines': 'ibm',
        'bayerische motoren werke': 'bmw',
        'volkswagen': 'vw',
        'mcdonalds': 'mcd',
        'coca cola': 'coke',
        'berkshire hathaway': 'berkshire',
        'jpmorgan chase': 'jpmorgan',
        'bank america': 'bofa',
        'procter gamble': 'pg',
        'johnson johnson': 'jnj',
        'general electric': 'ge',
        'general motors': 'gm',
        'att': 'at t',
        'exxon mobil': 'exxon',
        'john deere': 'deere',
        'northrop grumman': 'northrop',
        'lockheed martin': 'lockheed',
        'raytheon technologies': 'rtx',
        'nestle': 'nestlé',
        'loreal': "l'oréal",
        'mercedes benz': 'mercedes',
        'nippon telegraph telephone': 'ntt',
        'taiwan semiconductor': 'tsmc',
        'industrial commercial bank china': 'icbc',
        'agricultural bank china': 'abc',
        'china construction bank': 'ccb',
        'bank china': 'boc'
    }
    
    norm = normalize_for_matching(name)
    for key, value in mappings.items():
        if key in norm:
            variations.add(value)
        if value in norm:
            variations.add(key)
    
    # First word only (for companies often known by first name)
    words = norm.split()
    if words and len(words[0]) > 2:
        variations.add(words[0])
    
    return variations

def main():
    print("="*80)
    print("COMPLETE VERIFICATION OF ALL COMPANIES")
    print("="*80)
    
    # Read ALL companies from CSV
    print("\n1. Reading entire CSV file...")
    all_companies = []
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            all_companies.append({
                'name': row['Name'],
                'rank': int(row['Rank']),
                'country': row['country']
            })
    
    print(f"   Total companies in CSV: {len(all_companies)}")
    
    # Get ALL existing logos
    print("\n2. Reading all logo files...")
    logos_path = '../socratify-images/logos/images/companies/'
    existing_logos = {}
    logo_normalized = defaultdict(list)
    
    for filename in os.listdir(logos_path):
        if filename.endswith('.png'):
            logo_name = filename[:-4]
            existing_logos[logo_name] = filename
            
            # Create normalized versions for matching
            normalized = normalize_for_matching(logo_name)
            logo_normalized[normalized].append(logo_name)
    
    print(f"   Total logo files: {len(existing_logos)}")
    
    # Match each company
    print("\n3. Matching ALL companies to logos...")
    matched = []
    unmatched = []
    
    for company in all_companies:
        variations = get_all_possible_matches(company['name'])
        found = False
        
        for variation in variations:
            if variation in logo_normalized:
                matched.append(company)
                found = True
                break
            
            # Partial match
            for logo_norm in logo_normalized.keys():
                if len(variation) > 3 and len(logo_norm) > 3:
                    if variation in logo_norm or logo_norm in variation:
                        matched.append(company)
                        found = True
                        break
            
            if found:
                break
        
        if not found:
            unmatched.append(company)
    
    # Sort unmatched by rank
    unmatched.sort(key=lambda x: x['rank'])
    
    # Statistics
    print(f"\n4. RESULTS:")
    print(f"   ✓ Matched: {len(matched):,} companies ({len(matched)/len(all_companies)*100:.1f}%)")
    print(f"   ✗ Unmatched: {len(unmatched):,} companies ({len(unmatched)/len(all_companies)*100:.1f}%)")
    
    # Coverage by rank brackets
    print(f"\n5. COVERAGE BY RANK:")
    brackets = [
        (1, 50, "Top 50"),
        (51, 100, "51-100"),
        (101, 200, "101-200"),
        (201, 500, "201-500"),
        (501, 1000, "501-1000"),
        (1001, 2000, "1001-2000"),
        (2001, 5000, "2001-5000"),
        (5001, 10000, "5001-10000"),
        (10001, 20000, "10000+")
    ]
    
    for start, end, label in brackets:
        bracket_companies = [c for c in all_companies if start <= c['rank'] <= end]
        bracket_matched = [c for c in matched if start <= c['rank'] <= end]
        
        if bracket_companies:
            coverage = len(bracket_matched) / len(bracket_companies) * 100
            missing = len(bracket_companies) - len(bracket_matched)
            print(f"   {label:12s}: {len(bracket_matched):5,}/{len(bracket_companies):5,} ({coverage:5.1f}%) - Missing: {missing:,}")
    
    # Show ALL unmatched from top 100
    print(f"\n6. ALL UNMATCHED FROM TOP 100:")
    top_100_unmatched = [c for c in unmatched if c['rank'] <= 100]
    
    if top_100_unmatched:
        print(f"   Found {len(top_100_unmatched)} unmatched in top 100:")
        for company in top_100_unmatched:
            print(f"     {company['rank']:3d}. {company['name']} ({company['country']})")
    else:
        print("   ✓ All top 100 companies have logos!")
    
    # Show sample of unmatched from different ranges
    print(f"\n7. SAMPLE OF UNMATCHED BY RANK RANGE:")
    
    ranges = [(101, 500), (501, 1000), (1001, 5000)]
    for start, end in ranges:
        range_unmatched = [c for c in unmatched if start <= c['rank'] <= end]
        if range_unmatched:
            print(f"\n   Rank {start}-{end} (showing first 5 of {len(range_unmatched)}):")
            for company in range_unmatched[:5]:
                print(f"     {company['rank']:4d}. {company['name']}")
    
    # Save complete unmatched list
    with open('complete_unmatched_list.txt', 'w') as f:
        f.write(f"Complete list of unmatched companies ({len(unmatched)} total)\n")
        f.write("="*60 + "\n\n")
        
        current_bracket = None
        for company in unmatched:
            rank = company['rank']
            
            # Add section headers
            if rank <= 100 and current_bracket != "TOP 100":
                current_bracket = "TOP 100"
                f.write(f"\n{'='*40}\nTOP 100 COMPANIES\n{'='*40}\n")
            elif 101 <= rank <= 500 and current_bracket != "101-500":
                current_bracket = "101-500"
                f.write(f"\n{'='*40}\nRANK 101-500\n{'='*40}\n")
            elif 501 <= rank <= 1000 and current_bracket != "501-1000":
                current_bracket = "501-1000"
                f.write(f"\n{'='*40}\nRANK 501-1000\n{'='*40}\n")
            elif 1001 <= rank <= 5000 and current_bracket != "1001-5000":
                current_bracket = "1001-5000"
                f.write(f"\n{'='*40}\nRANK 1001-5000\n{'='*40}\n")
            elif rank > 5000 and current_bracket != "5000+":
                current_bracket = "5000+"
                f.write(f"\n{'='*40}\nRANK 5000+\n{'='*40}\n")
            
            f.write(f"{rank:5d}. {company['name']} ({company['country']})\n")
    
    print(f"\n8. SAVED:")
    print(f"   Complete unmatched list saved to: complete_unmatched_list.txt")
    
    # Final summary
    print(f"\n{'='*80}")
    print("FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"Total companies in your list: {len(all_companies):,}")
    print(f"Companies with logos: {len(matched):,} ({len(matched)/len(all_companies)*100:.1f}%)")
    print(f"Companies without logos: {len(unmatched):,} ({len(unmatched)/len(all_companies)*100:.1f}%)")
    
    if len(matched) == len(all_companies):
        print("\n🎉 COMPLETE COVERAGE! All companies have logos!")
    else:
        print(f"\n📋 To get remaining {len(unmatched):,} logos:")
        print("   1. Check 'complete_unmatched_list.txt' for full list")
        print("   2. Priority: Focus on top-ranked companies first")
        print("   3. Many may be subsidiaries or regional variants of companies you already have")

if __name__ == "__main__":
    main()