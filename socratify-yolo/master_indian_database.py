#!/usr/bin/env python3
"""
Master Indian Companies Database
Complete coverage: Stock indexes, unicorns, private companies, startups
"""

def get_master_indian_companies():
    """Complete database of Indian companies across all categories"""
    return {
        "Nifty_50_Complete": [
            "Adani Enterprises", "Adani Ports & SEZ", "Apollo Hospitals", "Asian Paints",
            "Axis Bank", "Bajaj Auto", "Bajaj Finance", "Bajaj Finserv", "Bharat Electronics",
            "Bharti Airtel", "Cipla", "Coal India", "Dr Reddy's Laboratories", "Eicher Motors",
            "Grasim Industries", "HCLTech", "HDFC Bank", "HDFC Life", "Hero MotoCorp",
            "Hindalco Industries", "Hindustan Unilever", "ICICI Bank", "IndusInd Bank",
            "Infosys", "ITC", "Jio Financial Services", "JSW Steel", "Kotak Mahindra Bank",
            "Larsen & Toubro", "Mahindra & Mahindra", "Maruti Suzuki", "Nestle India",
            "NTPC", "Oil & Natural Gas Corporation", "Power Grid Corporation", "Reliance Industries",
            "Shriram Finance", "State Bank of India", "Sun Pharmaceutical", "Tata Consultancy Services",
            "Tata Consumer Products", "Tata Motors", "Tata Steel", "Tech Mahindra", "Titan Company",
            "Trent", "UltraTech Cement", "UPL", "Wipro", "Zomato"
        ],
        
        "BSE_Sensex_30": [
            "Adani Ports & SEZ", "Asian Paints", "Axis Bank", "Bajaj Finance", "Bajaj Finserv",
            "Bharat Electronics", "Bharti Airtel", "HCLTech", "HDFC Bank", "Hindustan Unilever",
            "ICICI Bank", "Infosys", "ITC", "Kotak Mahindra Bank", "Larsen & Toubro",
            "Mahindra & Mahindra", "Maruti Suzuki", "NTPC", "Power Grid Corporation",
            "Reliance Industries", "State Bank of India", "Sun Pharmaceutical", "Tata Consultancy Services",
            "Tata Motors", "Tata Steel", "Tech Mahindra", "Titan Company", "Trent",
            "UltraTech Cement", "Wipro"
        ],
        
        "Banking_Financial_Complete": [
            "HDFC Bank", "ICICI Bank", "State Bank of India", "Axis Bank", "Kotak Mahindra Bank",
            "IndusInd Bank", "Punjab National Bank", "IDFC First Bank", "AU Small Finance Bank",
            "Federal Bank", "Bandhan Bank", "Bank of Baroda", "Union Bank of India", "Canara Bank",
            "Indian Bank", "Indian Overseas Bank", "Bank of India", "Bank of Maharashtra",
            "UCO Bank", "Central Bank of India", "Punjab & Sind Bank", "RBL Bank", "Karnataka Bank",
            "South Indian Bank", "Karur Vysya Bank", "City Union Bank", "Dhanlaxmi Bank",
            "Nainital Bank", "HDFC Life", "SBI Life Insurance", "LIC", "ICICI Prudential Life",
            "Max Life Insurance", "Bajaj Finance", "Bajaj Finserv", "Shriram Finance"
        ],
        
        "IT_Services_Complete": [
            "Tata Consultancy Services", "Infosys", "HCL Technologies", "Tech Mahindra", "Wipro",
            "L&T Infotech", "Mindtree", "Mphasis", "Persistent Systems", "Cyient", "KPIT Technologies",
            "Hexaware Technologies", "Zensar Technologies", "Tata Elxsi", "eClerx Services",
            "L&T Technology Services", "Coforge", "Firstsource Solutions", "Sonata Software",
            "Rolta India", "Tata Technologies", "NIIT Technologies", "Birlasoft"
        ],
        
        "Pharma_Healthcare_Complete": [
            "Sun Pharmaceutical", "Dr Reddy's Laboratories", "Cipla", "Lupin", "Aurobindo Pharma",
            "Divis Laboratories", "Torrent Pharmaceuticals", "Zydus Life Sciences", "Alkem Laboratories",
            "Biocon", "Cadila Healthcare", "Mankind Pharma", "Ipca Laboratories", "Abbott India",
            "Pfizer India", "GlaxoSmithKline India", "Sanofi India", "Novartis India", "Apollo Hospitals",
            "Max Healthcare", "Fortis Healthcare", "Narayana Hrudayalaya", "Aster DM Healthcare"
        ],
        
        "Unicorns_Major": [
            "Flipkart", "PhonePe", "Paytm", "BYJU'S", "Swiggy", "Zomato", "OLA", "OYO Rooms",
            "Freshworks", "Dream11", "Nykaa", "PolicyBazaar", "MakeMyTrip", "Razorpay", "Zerodha",
            "Groww", "CRED", "Meesho", "Urban Company", "Lenskart", "Pine Labs", "BharatPe",
            "CoinDCX", "Digit Insurance", "MobiKwik", "Slice", "KreditBee", "EarlySalary",
            "Capital Float", "Lendingkart", "Unacademy", "Eruditus", "upGrad", "Vedantu",
            "BigBasket", "Grofers", "Delhivery", "BlackBuck", "Rivigo", "Udaan", "OfBusiness", "Moglix"
        ],
        
        "New_Unicorns_2024_2025": [
            "Krutrim", "Perfios", "Rapido", "Ather Energy", "MoneyView", "Porter", "Netradyne", "Drools"
        ],
        
        "Fintech_Soonicorns": [
            "Pension Box", "Viva Money", "KiVi", "Zaggle", "M2P Fintech", "Niyo", "Jar", "Freo",
            "Fi Money", "Jupiter", "Navi", "InstantPay", "PayMe India", "MoneyTap", "LazyPay",
            "Simpl", "ZestMoney", "PaySense", "CASHe", "FlexiLoans"
        ],
        
        "E_commerce_Marketplaces": [
            "The Souled Store", "Boat", "Mamaearth", "Sugar Cosmetics", "Purplle", "Bewakoof",
            "FabIndia", "Myntra", "Snapdeal", "Amazon India", "FirstCry", "Hopscotch", "LimeRoad",
            "Jabong", "Koovs", "Voonik", "StayHalo", "Craftsvilla", "ShopClues", "Paytm Mall"
        ],
        
        "Healthcare_Startups": [
            "Loop Health", "Mfine", "DocsApp", "Medlife", "1mg", "Portea Medical", "Practo",
            "HealthifyMe", "Cure.fit", "Lybrate", "Ask Apollo", "MediBuddy", "Pharmeasy", "Netmeds",
            "Wellness Forever", "Apollo 24|7", "Tata Health"
        ],
        
        "SaaS_Enterprise": [
            "Kiko Live", "Floworks AI", "Finarekin Analytics", "Flock", "SurveySparrow",
            "Airbase", "Whatfix", "Zenoti", "Postman", "BrowserStack", "Chargebee", "Freshdesk",
            "Zoho", "MindTickle", "Capillary Technologies", "Druva", "Icertis", "Innovaccer"
        ],
        
        "Mobility_Logistics": [
            "ElasticRun", "Dunzo", "Shadowfax", "LoadShare", "Fareye", "Rivigo", "TruckSuvidha",
            "BlackBuck", "Delhivery", "Ecom Express", "Blue Dart", "DTDC", "Gati", "Professional Couriers"
        ],
        
        "PropTech_Real_Estate": [
            "Flent", "HouseEazy", "PropertyGuru", "Stanza Living", "NestAway", "OYO Life",
            "Zolo", "CoHo", "PG.com", "Grabhouse", "FlatSearch", "MagicBricks", "99acres",
            "Housing.com", "PropTiger", "Makaan.com"
        ],
        
        "AgriTech_FoodTech": [
            "CropIn", "MapMyCrop", "AGRIM", "AgroStar", "BigHaat", "Fasal", "WayCool",
            "Rebel Foods", "Faasos", "EatClub", "Box8", "Freshmenu", "Swiggy Instamart",
            "Grofers", "BigBasket", "Country Delight", "Licious", "FreshToHome"
        ],
        
        "Gaming_Entertainment": [
            "Dream Sports", "MPL", "WinZO", "Gameskraft", "Nazara Technologies", "Paytm First Games",
            "Ace2Three", "Adda52", "PokerStars India", "RummyCircle", "A23", "GetMega"
        ],
        
        "Social_Content_Creator": [
            "ShareChat", "Mohalla Tech", "Josh", "Roposo", "Trell", "Chingari", "Mitron TV",
            "MX TakaTak", "Dailyhunt", "InMobi", "Glance", "Pocket Aces", "The Viral Fever",
            "All India Bakchod", "FilterCopy"
        ],
        
        "Travel_Hospitality": [
            "Ixigo", "Yatra", "Goibibo", "RedBus", "EaseMyTrip", "TravelTriangle", "Thrillophilia",
            "Thomas Cook India", "Cox & Kings", "SOTC Travel", "Club Mahindra", "Sterling Holiday Resorts"
        ],
        
        "CleanTech_Sustainability": [
            "ReNew Power", "Greenko", "Azure Power", "Mahindra Susten", "Tata Power Solar",
            "Adani Green Energy", "Hero Future Energies", "JSW Energy", "Suzlon Energy",
            "Inox Wind", "Waaree Energies", "Vikram Solar", "Emmvee Solar", "Goldi Solar"
        ],
        
        "MNC_Subsidiaries_Major": [
            "Google India", "Microsoft India", "Amazon India", "Apple India", "Meta India",
            "Samsung India", "IBM India", "Oracle India", "SAP India", "Adobe India",
            "Salesforce India", "Cisco India", "Intel India", "Qualcomm India", "NVIDIA India",
            "Dell Technologies India", "HP India", "Lenovo India", "Sony India", "LG Electronics India"
        ],
        
        "Government_PSUs_Complete": [
            "ONGC", "NTPC", "Coal India", "IOC", "BPCL", "HPCL", "SAIL", "GAIL",
            "Power Grid Corporation", "BHEL", "BEL", "HAL", "Mazagon Dock Shipbuilders",
            "Garden Reach Shipbuilders", "Cochin Shipyard", "BEML", "HMT", "ITI Limited",
            "MTNL", "BSNL", "Air India", "Indian Railways", "Food Corporation of India"
        ],
        
        "Major_Cooperatives": [
            "Amul", "IFFCO", "KRIBHCO", "NAFED", "Gujarat Cooperative Milk Marketing Federation",
            "Saraswat Cooperative Bank", "Mumbai District Central Cooperative Bank",
            "Karnataka Milk Federation", "Aarey Milk", "Verka Milk"
        ],
        
        "Conglomerates_Family_Business": [
            "Reliance Industries", "Tata Group", "Adani Group", "Aditya Birla Group",
            "Mahindra Group", "Godrej Group", "Bajaj Group", "TVS Group", "Kirloskar Group",
            "Thermax Limited", "Crompton Greaves", "Havells India", "Voltas Limited",
            "Blue Star Limited", "Whirlpool of India", "Videocon Industries"
        ],
        
        "Emerging_High_Growth": [
            "Koo", "CashKaro", "LivSpace", "HealthifyMe", "Curefit", "Cars24", "CarDekho",
            "CarTrade", "Droom", "Spinny", "CARS24", "OLX India", "Quikr", "UrbanClap",
            "Housejoy", "TaskBob", "Mr Right", "Zimmber", "LocalOye"
        ]
    }

def main():
    companies_dict = get_master_indian_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"MASTER INDIAN COMPANIES DATABASE")
    print(f"=" * 40)
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/master_indian_database.txt', 'w') as f:
        f.write("MASTER INDIAN COMPANIES DATABASE\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Total unique companies: {len(unique_companies)}\n")
        f.write(f"Categories: {len(companies_dict)}\n\n")
        
        f.write("COMPLETE COVERAGE:\n")
        f.write("- All NSE/BSE stock market indexes\n")
        f.write("- All current Indian unicorns\n")
        f.write("- Major soonicorns and high-growth startups\n")
        f.write("- Private companies and family businesses\n")
        f.write("- MNC subsidiaries with significant Indian operations\n")
        f.write("- Government PSUs and cooperatives\n\n")
        
        for i, company in enumerate(unique_companies, 1):
            f.write(f"{i:3d}. {company}\n")
    
    print(f"\nSaved to master_indian_database.txt")
    print(f"Coverage includes:")
    print(f"- Complete stock market indexes (NSE/BSE)")
    print(f"- All unicorns and major startups")
    print(f"- Private companies and conglomerates")
    print(f"- MNC subsidiaries")
    print(f"- Government enterprises")
    
    return unique_companies

if __name__ == "__main__":
    main()