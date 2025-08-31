#!/usr/bin/env python3
import csv
import os
import re
from difflib import SequenceMatcher
import json

def normalize_name(name):
    """Normalize company name for comparison"""
    # Remove special characters and convert to lowercase
    normalized = name.lower()
    # Remove common business suffixes
    suffixes = [
        ' inc', ' corp', ' corporation', ' company', ' limited', ' ltd', ' llc',
        ' group', ' holdings', ' international', ' global', ' worldwide',
        ' ag', ' sa', ' ab', ' nv', ' plc', ' gmbh', ' spa', ' asa', ' bhd'
    ]
    for suffix in suffixes:
        if normalized.endswith(suffix):
            normalized = normalized[:-len(suffix)]
    
    # Remove special characters but keep spaces
    normalized = re.sub(r'[^\w\s]', '', normalized)
    # Remove extra spaces
    normalized = ' '.join(normalized.split())
    return normalized

def get_name_variations(name):
    """Generate possible variations of a company name"""
    variations = set()
    variations.add(normalize_name(name))
    
    # Handle parenthetical content
    if '(' in name:
        # Add version without parentheses
        base = name.split('(')[0].strip()
        variations.add(normalize_name(base))
        # Add content within parentheses
        if ')' in name:
            inner = name.split('(')[1].split(')')[0].strip()
            variations.add(normalize_name(inner))
    
    # Handle ampersands
    if '&' in name or 'and' in name.lower():
        variations.add(normalize_name(name.replace('&', 'and')))
        variations.add(normalize_name(name.replace('and', '&')))
    
    # Handle common abbreviations
    abbreviations = {
        'united parcel service': ['ups'],
        'international business machines': ['ibm'],
        'hewlett packard': ['hp'],
        'deutsche post': ['dhl'],
        'federal express': ['fedex'],
        'nippon telegraph': ['ntt'],
        'volkswagen': ['vw'],
        'bayerische motoren werke': ['bmw'],
        'mercedes benz': ['mercedes', 'daimler'],
        'procter gamble': ['pg', 'p&g'],
        'johnson johnson': ['jnj', 'j&j'],
        'berkshire hathaway': ['berkshire'],
        'jpmorgan chase': ['jpmorgan', 'jp morgan', 'chase'],
        'bank of america': ['bofa', 'boa'],
        'wells fargo': ['wells'],
        'goldman sachs': ['goldman'],
        'morgan stanley': ['morgan'],
        'american express': ['amex'],
        'coca cola': ['coke', 'coca-cola'],
        'pepsi': ['pepsico'],
        'mcdonalds': ['mcd'],
        'starbucks': ['sbux'],
        'walmart': ['wal-mart'],
        'target': ['tgt'],
        'home depot': ['hd'],
        'lowes': ['lowe'],
        'costco': ['cost'],
        'cvs health': ['cvs'],
        'walgreens': ['wag'],
        'unitedhealth': ['united health', 'unitedhealthgroup'],
        'alphabet': ['google'],
        'meta platforms': ['facebook', 'meta'],
        'amazon': ['amzn'],
        'microsoft': ['msft'],
        'apple': ['aapl'],
        'tesla': ['tsla'],
        'general electric': ['ge'],
        'general motors': ['gm'],
        'ford motor': ['ford'],
        'exxon mobil': ['exxon', 'xom'],
        'chevron': ['cvx'],
        'conocophillips': ['cop'],
        'at&t': ['att'],
        'verizon': ['vz'],
        'comcast': ['cmcsa'],
        'disney': ['walt disney', 'dis'],
        'netflix': ['nflx'],
        'nike': ['nke'],
        'adidas': ['addidas'],
        'industrial commercial bank china': ['icbc'],
        'china construction bank': ['ccb'],
        'agricultural bank china': ['abc'],
        'bank china': ['boc'],
        'ping an': ['pingan'],
        'tencent': ['tcehy'],
        'alibaba': ['baba'],
        'samsung': ['samsung electronics'],
        'taiwan semiconductor': ['tsmc'],
        'nestle': ['nestlé'],
        'unilever': ['ul'],
        'kraft heinz': ['kraft'],
        '3m': ['mmm'],
        'caterpillar': ['cat'],
        'deere company': ['john deere'],
        'boeing': ['ba'],
        'airbus': ['eadsy'],
        'lockheed martin': ['lmt'],
        'raytheon': ['rtx'],
        'northrop grumman': ['noc'],
        'general dynamics': ['gd']
    }
    
    normalized = normalize_name(name)
    for key, values in abbreviations.items():
        if key in normalized:
            variations.update([normalize_name(v) for v in values])
        for value in values:
            if normalize_name(value) == normalized:
                variations.add(key)
    
    return variations

def find_similar_names(name, name_list, threshold=0.85):
    """Find similar names using fuzzy matching"""
    similar = []
    variations = get_name_variations(name)
    
    for existing_name in name_list:
        existing_normalized = normalize_name(existing_name)
        
        # Check exact matches with variations
        for variation in variations:
            if variation == existing_normalized:
                return [(existing_name, 1.0)]
            
            # Check if one contains the other
            if len(variation) > 3 and len(existing_normalized) > 3:
                if variation in existing_normalized or existing_normalized in variation:
                    similar.append((existing_name, 0.9))
        
        # Fuzzy matching
        for variation in variations:
            ratio = SequenceMatcher(None, variation, existing_normalized).ratio()
            if ratio >= threshold:
                similar.append((existing_name, ratio))
    
    # Return best match if found
    if similar:
        similar.sort(key=lambda x: x[1], reverse=True)
        return similar[:1]
    
    return []

def main():
    print("="*70)
    print("COMPREHENSIVE LOGO ANALYSIS")
    print("="*70)
    
    # Read all companies from CSV
    print("\n1. Reading companies from CSV...")
    companies_from_csv = {}
    with open('list.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies_from_csv[row['Name']] = {
                'rank': int(row['Rank']),
                'country': row['country']
            }
    print(f"   Found {len(companies_from_csv)} companies in CSV")
    
    # Get all existing logos
    print("\n2. Scanning existing logos...")
    logos_path = '../socratify-images/logos/images/companies/'
    existing_logos = []
    if os.path.exists(logos_path):
        for filename in os.listdir(logos_path):
            if filename.endswith('.png'):
                logo_name = filename[:-4]  # Remove .png
                existing_logos.append(logo_name)
    print(f"   Found {len(existing_logos)} logo files")
    
    # Match companies to logos
    print("\n3. Matching companies to existing logos...")
    matched = {}
    unmatched = []
    
    for company_name, info in companies_from_csv.items():
        matches = find_similar_names(company_name, existing_logos, threshold=0.8)
        if matches:
            matched[company_name] = {
                'logo_file': matches[0][0],
                'confidence': matches[0][1],
                'rank': info['rank']
            }
        else:
            unmatched.append({
                'name': company_name,
                'rank': info['rank'],
                'country': info['country']
            })
    
    # Sort unmatched by rank
    unmatched.sort(key=lambda x: x['rank'])
    
    # Print results
    print(f"\n   ✓ Matched: {len(matched)} companies")
    print(f"   ✗ Missing: {len(unmatched)} companies")
    
    # Show some examples of matches
    print("\n4. Sample matches (showing confidence < 1.0):")
    sample_matches = [(k, v) for k, v in matched.items() if v['confidence'] < 1.0]
    sample_matches.sort(key=lambda x: x[1]['confidence'], reverse=True)
    for company, match_info in sample_matches[:10]:
        print(f"   '{company}' → '{match_info['logo_file']}' (confidence: {match_info['confidence']:.2f})")
    
    # Show top missing companies
    print(f"\n5. Top 50 missing companies (by rank):")
    for i, company in enumerate(unmatched[:50], 1):
        print(f"   {company['rank']:4d}. {company['name']} ({company['country']})")
    
    # Save detailed results
    print("\n6. Saving detailed results...")
    
    # Save matched companies
    with open('matched_logos.json', 'w') as f:
        json.dump(matched, f, indent=2)
    print(f"   Saved matched companies to matched_logos.json")
    
    # Save missing companies
    with open('missing_logos.json', 'w') as f:
        json.dump(unmatched, f, indent=2)
    print(f"   Saved missing companies to missing_logos.json")
    
    # Create a simple list of missing company names for download script
    with open('missing_companies.txt', 'w') as f:
        for company in unmatched:
            f.write(f"{company['name']}\n")
    print(f"   Saved simple list to missing_companies.txt")
    
    # Summary statistics
    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)
    print(f"Total companies in CSV: {len(companies_from_csv)}")
    print(f"Total existing logos: {len(existing_logos)}")
    print(f"Successfully matched: {len(matched)} ({len(matched)/len(companies_from_csv)*100:.1f}%)")
    print(f"Missing logos: {len(unmatched)} ({len(unmatched)/len(companies_from_csv)*100:.1f}%)")
    
    # By rank brackets
    print("\nMissing logos by rank:")
    brackets = [(1, 100), (101, 500), (501, 1000), (1001, 5000), (5001, 100000)]
    for start, end in brackets:
        count = len([c for c in unmatched if start <= c['rank'] <= end])
        if count > 0:
            print(f"  Rank {start:5d}-{end:5d}: {count:4d} missing")

if __name__ == "__main__":
    main()