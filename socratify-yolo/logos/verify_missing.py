#!/usr/bin/env python3
"""
Logo Collection Analysis Script

This script analyzes existing logo collections and identifies what major companies are truly missing.
It normalizes company names for comparison and checks against a comprehensive list of important companies.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from typing import Set, List, Dict, Tuple

def normalize_company_name(name: str) -> str:
    """
    Normalize company names for comparison by:
    - Converting to lowercase
    - Removing file extensions
    - Removing special characters and common corporate suffixes
    - Standardizing spacing
    """
    # Remove file extension
    name = re.sub(r'\.(png|jpg|jpeg|gif|svg)$', '', name, flags=re.IGNORECASE)
    
    # Convert to lowercase
    name = name.lower()
    
    # Remove common corporate suffixes
    suffixes = [
        r'\s+(inc|corp|corporation|company|ltd|limited|llc|group|holdings?|international|enterprises?|industries?|systems?|solutions?|technologies?|services?|sa|se|ag|nv|plc|spa|gmbh|co|&\s*co)',
        r'\s+clearbit.*',
        r'\s+favicon.*',
        r'\s+domain.*',
        r'\s+\d+$',  # Remove trailing numbers
    ]
    
    for suffix in suffixes:
        name = re.sub(suffix, '', name)
    
    # Replace various separators with spaces
    name = re.sub(r'[_\-\.]+', ' ', name)
    
    # Remove extra spaces and parenthetical content
    name = re.sub(r'\([^)]*\)', '', name)  # Remove content in parentheses
    name = re.sub(r'\s+', ' ', name).strip()
    
    # Handle special cases and common variations
    replacements = {
        'mcdonalds': 'mcdonald',
        'att': 'at&t',
        'jp morgan': 'jpmorgan',
        'bank of america': 'bofa',
        'goldman sachs': 'goldman',
        'morgan stanley': 'morgan',
        'wells fargo': 'wells',
        'american express': 'amex',
    }
    
    for old, new in replacements.items():
        if old in name:
            name = name.replace(old, new)
    
    return name

def get_existing_logos(directory: str) -> Set[str]:
    """Get all existing logo filenames from a directory and normalize them."""
    logos = set()
    
    if not os.path.exists(directory):
        print(f"Warning: Directory {directory} does not exist")
        return logos
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.svg')):
                normalized = normalize_company_name(file)
                if normalized:  # Only add non-empty normalized names
                    logos.add(normalized)
    
    return logos

def load_major_companies() -> Dict[str, List[str]]:
    """
    Load a comprehensive list of major companies organized by category.
    This includes Fortune 500, Global 2000, and other significant companies.
    """
    major_companies = {
        "Fortune 100 Tech": [
            "Apple", "Microsoft", "Google", "Amazon", "Meta", "Tesla", "Netflix", "Adobe",
            "Salesforce", "Intel", "Oracle", "IBM", "Cisco", "HP", "Dell", "Nvidia",
            "PayPal", "eBay", "Twitter", "Zoom", "Slack", "Dropbox", "Box", "Shopify",
            "Uber", "Lyft", "Airbnb", "SpaceX", "Twitter", "LinkedIn", "YouTube",
            "Snapchat", "TikTok", "Discord", "Reddit", "Pinterest", "Instacart"
        ],
        "Fortune 100 Finance": [
            "JPMorgan Chase", "Bank of America", "Wells Fargo", "Citigroup", "Goldman Sachs",
            "Morgan Stanley", "American Express", "Charles Schwab", "BlackRock", "Visa",
            "Mastercard", "Berkshire Hathaway", "Aon", "Marsh McLennan", "Prudential",
            "MetLife", "AIG", "Travelers", "Progressive", "Allstate", "State Farm",
            "USAA", "Capital One", "Discover", "Synchrony Financial", "Fidelity",
            "Vanguard", "T. Rowe Price", "Franklin Templeton", "KKR", "Apollo",
            "Blackstone", "Carlyle Group", "TPG", "Warburg Pincus", "Silver Lake"
        ],
        "Fortune 100 Healthcare": [
            "UnitedHealth Group", "Johnson & Johnson", "Pfizer", "AbbVie", "Merck",
            "Bristol Myers Squibb", "Abbott", "Eli Lilly", "Amgen", "Gilead Sciences",
            "Moderna", "Regeneron", "Biogen", "Vertex Pharmaceuticals", "Illumina",
            "Danaher", "Thermo Fisher", "Agilent", "PerkinElmer", "Waters Corporation",
            "CVS Health", "Anthem", "Humana", "Cigna", "Aetna", "Kaiser Permanente",
            "HCA Healthcare", "Tenet Healthcare", "Universal Health Services",
            "Community Health Systems", "LifePoint Health", "Encompass Health"
        ],
        "Fortune 100 Retail & Consumer": [
            "Walmart", "Amazon", "Costco", "Home Depot", "Target", "Lowe's", "Best Buy",
            "TJX Companies", "Macy's", "Kohl's", "Nordstrom", "Gap", "Ross Stores",
            "Dollar General", "Dollar Tree", "AutoZone", "Advance Auto Parts",
            "O'Reilly Automotive", "Starbucks", "McDonald's", "Subway", "Domino's",
            "Yum! Brands", "Restaurant Brands", "Chipotle", "Shake Shack",
            "Coca-Cola", "PepsiCo", "Nestle", "Unilever", "Procter & Gamble",
            "Colgate-Palmolive", "Kimberly-Clark", "Clorox", "Nike", "Adidas",
            "Under Armour", "Lululemon", "Ralph Lauren", "Coach", "Kate Spade"
        ],
        "Fortune 100 Energy": [
            "Exxon Mobil", "Chevron", "ConocoPhillips", "Marathon Petroleum",
            "Phillips 66", "Valero Energy", "Enterprise Products Partners",
            "Kinder Morgan", "Enbridge", "TC Energy", "NextEra Energy", "Duke Energy",
            "Dominion Energy", "Southern Company", "American Electric Power",
            "Exelon", "Xcel Energy", "NiSource", "CenterPoint Energy", "PPL",
            "Consolidated Edison", "Public Service Enterprise", "WEC Energy",
            "Entergy", "Ameren", "FirstEnergy", "Eversource Energy", "DTE Energy"
        ],
        "Fortune 100 Industrial": [
            "General Electric", "Boeing", "Lockheed Martin", "Raytheon", "Northrop Grumman",
            "General Dynamics", "Honeywell", "3M", "Caterpillar", "Deere", "Illinois Tool Works",
            "Emerson Electric", "Parker-Hannifin", "Eaton", "Cummins", "Paccar",
            "Textron", "L3Harris", "TransDigm", "Howmet Aerospace", "Spirit AeroSystems",
            "United Technologies", "Otis", "Carrier", "Ingersoll Rand", "Stanley Black & Decker",
            "Snap-on", "Fastenal", "W.W. Grainger", "MSC Industrial", "Cintas"
        ],
        "Fortune 100 Media & Telecom": [
            "Verizon", "AT&T", "T-Mobile", "Comcast", "Charter Communications",
            "Walt Disney", "Netflix", "ViacomCBS", "Fox Corporation", "Discovery",
            "WarnerMedia", "NBCUniversal", "Sony Pictures", "Lionsgate", "MGM",
            "AMC Networks", "Crown Media", "Scripps Networks", "A&E Networks",
            "Turner Broadcasting", "CNN", "ESPN", "HBO", "Showtime", "Starz",
            "New York Times", "Washington Post", "Wall Street Journal", "USA Today",
            "Time Magazine", "Forbes", "Bloomberg", "Reuters", "Associated Press"
        ],
        "Fortune 100 Transportation": [
            "FedEx", "UPS", "Union Pacific", "CSX", "Norfolk Southern", "BNSF Railway",
            "Kansas City Southern", "Canadian National", "Canadian Pacific",
            "J.B. Hunt", "Schneider", "Werner Enterprises", "Swift Transportation",
            "Knight Transportation", "Landstar", "Old Dominion", "Saia", "XPO Logistics",
            "C.H. Robinson", "Expeditors", "American Airlines", "Delta Air Lines",
            "United Airlines", "Southwest Airlines", "JetBlue", "Alaska Airlines",
            "Spirit Airlines", "Frontier Airlines", "Hawaiian Airlines", "Allegiant"
        ],
        "Global Luxury Brands": [
            "LVMH", "Hermès", "Chanel", "Gucci", "Prada", "Burberry", "Tiffany & Co",
            "Cartier", "Rolex", "Patek Philippe", "Audemars Piguet", "Omega",
            "Tag Heuer", "Breitling", "Ferrari", "Lamborghini", "Porsche", "Bentley",
            "Rolls-Royce", "Maserati", "Aston Martin", "McLaren", "Bugatti"
        ],
        "Major Consulting": [
            "McKinsey & Company", "Boston Consulting Group", "Bain & Company",
            "Deloitte", "PwC", "EY", "KPMG", "Accenture", "IBM Consulting",
            "Capgemini", "Infosys", "Tata Consultancy Services", "Wipro", "HCL Technologies",
            "Cognizant", "DXC Technology", "Atos", "NTT Data", "Tech Mahindra", "L&T Infotech"
        ],
        "Major Universities": [
            "Harvard University", "Stanford University", "MIT", "Princeton University",
            "Yale University", "Columbia University", "University of Pennsylvania",
            "Duke University", "Northwestern University", "University of Chicago",
            "Johns Hopkins University", "Caltech", "Cornell University", "Brown University",
            "Dartmouth College", "Vanderbilt University", "Rice University",
            "University of Notre Dame", "Georgetown University", "Carnegie Mellon University"
        ]
    }
    
    return major_companies

def find_missing_companies(existing_logos: Set[str], major_companies: Dict[str, List[str]]) -> Dict[str, List[Tuple[str, str]]]:
    """
    Find companies that are missing from the existing logo collection.
    Returns a dictionary with category as key and list of (original_name, normalized_name) tuples as values.
    """
    missing_by_category = {}
    
    for category, companies in major_companies.items():
        missing_companies = []
        
        for company in companies:
            normalized_company = normalize_company_name(company)
            
            # Check if this company exists in our collection
            found = False
            for existing_logo in existing_logos:
                # Use fuzzy matching - if normalized names share significant overlap
                if (normalized_company in existing_logo or 
                    existing_logo in normalized_company or
                    len(set(normalized_company.split()) & set(existing_logo.split())) > 0):
                    found = True
                    break
            
            if not found:
                missing_companies.append((company, normalized_company))
        
        if missing_companies:
            missing_by_category[category] = missing_companies
    
    return missing_by_category

def generate_statistics(existing_unique: Set[str], existing_downloads: Set[str], missing_companies: Dict[str, List[Tuple[str, str]]]) -> Dict:
    """Generate comprehensive statistics about the logo collection."""
    stats = {
        "existing_logos": {
            "unique_logos": len(existing_unique),
            "downloaded_logos": len(existing_downloads),
            "total_combined": len(existing_unique | existing_downloads),
            "overlap": len(existing_unique & existing_downloads)
        },
        "missing_analysis": {
            "categories_with_missing": len(missing_companies),
            "total_missing_companies": sum(len(companies) for companies in missing_companies.values()),
            "missing_by_category": {category: len(companies) for category, companies in missing_companies.items()}
        }
    }
    
    return stats

def main():
    """Main function to run the logo analysis."""
    print("🔍 Logo Collection Analysis")
    print("=" * 50)
    
    # Define paths
    unique_logos_dir = "/Users/adi/code/socratify/socratify-yolo/logos/all_unique_logos"
    downloads_dir = "/Users/adi/code/socratify/socratify-yolo/logos/downloads_20250807_175600"
    
    # Load existing logos
    print("📁 Loading existing logos...")
    existing_unique = get_existing_logos(unique_logos_dir)
    existing_downloads = get_existing_logos(downloads_dir)
    all_existing = existing_unique | existing_downloads
    
    print(f"   • Unique logos: {len(existing_unique):,}")
    print(f"   • Downloaded logos: {len(existing_downloads):,}")
    print(f"   • Combined total: {len(all_existing):,}")
    print(f"   • Overlap: {len(existing_unique & existing_downloads):,}")
    
    # Load major companies list
    print("\n🏢 Loading major companies list...")
    major_companies = load_major_companies()
    total_companies = sum(len(companies) for companies in major_companies.values())
    print(f"   • Total categories: {len(major_companies)}")
    print(f"   • Total major companies: {total_companies:,}")
    
    # Find missing companies
    print("\n🔍 Analyzing missing companies...")
    missing_companies = find_missing_companies(all_existing, major_companies)
    
    # Generate statistics
    stats = generate_statistics(existing_unique, existing_downloads, missing_companies)
    
    # Print results
    print("\n📊 ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Total existing logos: {stats['existing_logos']['total_combined']:,}")
    print(f"Total missing companies: {stats['missing_analysis']['total_missing_companies']:,}")
    print(f"Coverage rate: {((total_companies - stats['missing_analysis']['total_missing_companies']) / total_companies * 100):.1f}%")
    
    # Print missing companies by category
    if missing_companies:
        print("\n🚫 MISSING COMPANIES BY CATEGORY")
        print("=" * 50)
        
        for category, companies in sorted(missing_companies.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n📂 {category} ({len(companies)} missing):")
            for original_name, normalized_name in sorted(companies):
                print(f"   • {original_name}")
    else:
        print("\n🎉 No missing companies found! Complete coverage achieved.")
    
    # Save detailed results to JSON
    output_file = "/Users/adi/code/socratify/socratify-yolo/logos/missing_companies_analysis.json"
    detailed_results = {
        "timestamp": "2025-08-07",
        "statistics": stats,
        "missing_companies": {
            category: [{"original_name": orig, "normalized_name": norm} for orig, norm in companies]
            for category, companies in missing_companies.items()
        },
        "existing_logos": {
            "unique_collection": sorted(list(existing_unique)),
            "downloads_collection": sorted(list(existing_downloads))
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(detailed_results, f, indent=2, sort_keys=True)
    
    print(f"\n💾 Detailed analysis saved to: {output_file}")
    
    # Print top priority missing companies
    if missing_companies:
        print("\n🎯 TOP PRIORITY MISSING COMPANIES")
        print("=" * 50)
        
        high_priority_categories = ["Fortune 100 Tech", "Fortune 100 Finance", "Major Consulting", "Global Luxury Brands"]
        priority_missing = []
        
        for category in high_priority_categories:
            if category in missing_companies:
                for original_name, _ in missing_companies[category]:
                    priority_missing.append(f"{original_name} ({category})")
        
        if priority_missing:
            for company in priority_missing[:20]:  # Show top 20
                print(f"   • {company}")
            
            if len(priority_missing) > 20:
                print(f"   ... and {len(priority_missing) - 20} more high-priority companies")
        else:
            print("   • All high-priority companies are covered!")

if __name__ == "__main__":
    main()