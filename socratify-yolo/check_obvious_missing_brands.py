#!/usr/bin/env python3
"""
Check for obvious missing major brands and Fortune 500 companies
The brands everyone knows that we somehow missed
"""

import os
import re

def normalize_name(name: str) -> str:
    """Normalize company name for comparison"""
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)
    return name

def get_existing_companies() -> set:
    """Get all companies we currently have"""
    existing = set()
    existing_names = set()
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                # Remove extension
                name = os.path.splitext(file)[0]
                original_name = name.replace('_', ' ')
                existing_names.add(original_name.lower())
                
                # Normalize for matching
                normalized = normalize_name(name)
                existing.add(normalized)
                
                # Also add without common suffixes
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa)$', '', normalized)
                if clean_name != normalized and len(clean_name) > 2:
                    existing.add(clean_name)
    
    return existing, existing_names

def check_obvious_missing():
    """Check for obvious missing brands everyone knows"""
    existing, existing_names = get_existing_companies()
    
    # Obvious brands everyone knows
    obvious_brands = {
        "Athletic_Apparel": [
            "Reebok", "New Balance", "Under Armour", "Converse", "Fila", "Champion",
            "The North Face", "Columbia Sportswear", "Timberland", "Skechers", "ASICS",
            "Puma", "Adidas", "Nike", "Lululemon", "Patagonia", "Vans"  # Include existing ones too
        ],
        
        "Food_Beverage_Giants": [
            "Coca-Cola", "Burger King", "Taco Bell", "Dunkin", "Chipotle", "Wendy's",
            "In-N-Out Burger", "Five Guys", "Chick-fil-A", "Panera Bread", "Papa John's",
            "McDonald's", "KFC", "Starbucks", "Domino's", "Subway", "Pizza Hut", "PepsiCo"
        ],
        
        "Major_Retailers": [
            "Best Buy", "Home Depot", "Walgreens", "CVS", "Rite Aid", "Bed Bath & Beyond",
            "Dick's Sporting Goods", "GameStop", "Barnes & Noble", "Office Depot", "Staples",
            "Walmart", "Target", "Costco", "Lowe's", "Macy's", "Nordstrom", "TJ Maxx"
        ],
        
        "Automotive_Missing": [
            "General Motors", "Chevrolet", "Cadillac", "Buick", "GMC", "Chrysler", "Dodge",
            "Ram", "Jeep", "Fiat", "Alfa Romeo", "Maserati", "Bentley", "Rolls-Royce",
            "Lamborghini", "McLaren", "Aston Martin", "Jaguar", "Land Rover", "Mini",
            "Volvo", "Saab", "Infiniti", "Acura", "Lexus", "Genesis", "Maybach"
        ],
        
        "Luxury_Fashion": [
            "Gucci", "Louis Vuitton", "Prada", "Chanel", "Hermès", "Dior", "Versace",
            "Armani", "Dolce & Gabbana", "Valentino", "Givenchy", "Saint Laurent",
            "Balenciaga", "Bottega Veneta", "Fendi", "Burberry", "Ralph Lauren", "Calvin Klein"
        ],
        
        "Tech_Hardware": [
            "Dell", "HP", "Lenovo", "Asus", "Acer", "MSI", "Razer", "Corsair", "Logitech",
            "Canon", "Nikon", "Sony", "Panasonic", "Samsung", "LG", "Philips", "JBL",
            "Bose", "Beats", "Audio-Technica", "Sennheiser", "Shure"
        ],
        
        "Airlines_Major": [
            "American Airlines", "Delta Air Lines", "United Airlines", "Southwest Airlines",
            "JetBlue", "Alaska Airlines", "Spirit Airlines", "Frontier Airlines",
            "British Airways", "Lufthansa", "Air France", "KLM", "Emirates", "Qatar Airways"
        ],
        
        "Hotels_Hospitality": [
            "Marriott", "Hilton", "Hyatt", "InterContinental", "Sheraton", "Westin",
            "W Hotels", "St. Regis", "Ritz-Carlton", "Four Seasons", "Mandarin Oriental",
            "Peninsula Hotels", "Waldorf Astoria", "Conrad Hotels", "DoubleTree", "Hampton Inn"
        ],
        
        "Financial_Services": [
            "American Express", "Visa", "Mastercard", "Discover", "Capital One", "Chase",
            "Bank of America", "Wells Fargo", "Citibank", "U.S. Bank", "PNC Bank",
            "TD Bank", "Fifth Third Bank", "KeyBank", "Regions Bank", "SunTrust", "BB&T"
        ],
        
        "Telecom_Major": [
            "Verizon", "AT&T", "T-Mobile", "Sprint", "Comcast", "Charter Spectrum",
            "Cox Communications", "Altice USA", "Frontier Communications", "CenturyLink"
        ],
        
        "Consumer_Brands": [
            "Procter & Gamble", "Unilever", "Johnson & Johnson", "Colgate-Palmolive",
            "Kimberly-Clark", "3M", "SC Johnson", "Clorox", "Reckitt", "Henkel",
            "L'Oréal", "Estée Lauder", "Revlon", "Maybelline", "CoverGirl", "MAC Cosmetics"
        ],
        
        "Entertainment_Media": [
            "Disney", "Warner Bros", "Universal Studios", "Paramount", "Sony Pictures",
            "20th Century Studios", "Lionsgate", "MGM", "DreamWorks", "Pixar",
            "Marvel", "DC Comics", "ESPN", "CNN", "Fox News", "MSNBC", "BBC", "NBC"
        ]
    }
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"Checking {sum(len(brands) for brands in obvious_brands.values())} obvious major brands...")
    
    all_missing = {}
    total_missing_brands = []
    
    for category, brands in obvious_brands.items():
        missing_in_category = []
        found_in_category = []
        
        for brand in brands:
            normalized = normalize_name(brand)
            brand_lower = brand.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(brand)
                found = True
            else:
                # Check in original names
                for exist_name in existing_names:
                    # For brand matching, be more flexible
                    brand_key_terms = [word for word in brand_lower.split() 
                                     if len(word) > 2 and word not in ['the', 'inc', 'llc', 'ltd', 'co', 'corp']]
                    
                    if brand_key_terms:
                        main_term = brand_key_terms[0]
                        if main_term in exist_name and len(main_term) >= 3:
                            found_in_category.append(f"{brand} (found as: {exist_name})")
                            found = True
                            break
                    
                    # Also check full substring match
                    if brand_lower in exist_name or exist_name in brand_lower:
                        if len(brand_lower) >= 3:
                            found_in_category.append(f"{brand} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 3 and len(exist) > 3:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.7:
                                    found_in_category.append(f"{brand} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(brand)
                total_missing_brands.append((brand, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(brands) * 100 if brands else 0
        }
        
        print(f"\\n=== {category.replace('_', ' ').upper()} ===")
        print(f"Total: {len(brands)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print("🚨 MISSING OBVIOUS BRANDS:", ', '.join(missing_in_category[:10]))
    
    # Summary
    total_missing = len(total_missing_brands)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\\n🚨 OBVIOUS BRANDS SUMMARY")
    print(f"Total obvious brands checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Show top missing by category importance
    category_priority = {
        'Athletic_Apparel': 10,
        'Food_Beverage_Giants': 10,
        'Major_Retailers': 9,
        'Automotive_Missing': 9,
        'Tech_Hardware': 8,
        'Financial_Services': 8,
        'Luxury_Fashion': 7,
        'Airlines_Major': 6,
        'Hotels_Hospitality': 6,
        'Consumer_Brands': 5,
        'Entertainment_Media': 5,
        'Telecom_Major': 4
    }
    
    priority_missing = []
    for brand, category in total_missing_brands:
        priority_score = category_priority.get(category, 3)
        priority_missing.append((brand, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\\n🔥 TOP 50 MISSING OBVIOUS BRANDS:")
    for i, (brand, category, score) in enumerate(priority_missing[:50], 1):
        print(f"{i:2d}. {brand} ({category.replace('_', ' ')})")
    
    # Save all missing obvious brands for download
    with open('/Users/adi/code/socratify/socratify-yolo/missing_obvious_brands.txt', 'w') as f:
        f.write("MISSING OBVIOUS MAJOR BRANDS\\n")
        f.write("=" * 35 + "\\n\\n")
        f.write(f"Total missing: {total_missing}\\n\\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\\n")
                f.write(f"Coverage: {data['coverage']:.1f}%\\n")
                f.write(f"Missing ({len(data['missing'])}):\\n")
                for brand in data['missing']:
                    f.write(f"  - {brand}\\n")
                f.write("\\n")
        
        f.write("\\n### TOP PRIORITY MISSING ###\\n")
        for i, (brand, category, score) in enumerate(priority_missing[:100], 1):
            f.write(f"{i:3d}. {brand} ({category.replace('_', ' ')})\\n")
    
    print(f"\\nSaved all {total_missing} missing obvious brands to missing_obvious_brands.txt")
    print(f"🚨 We're missing some REALLY obvious ones that people definitely want to work for!")
    
    return priority_missing[:100]  # Return top 100 for download

if __name__ == "__main__":
    check_obvious_missing()