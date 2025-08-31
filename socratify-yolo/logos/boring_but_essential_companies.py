#!/usr/bin/env python3
"""
The BORING BUT ESSENTIAL companies - The hidden economy runners
"""

def get_boring_but_essential_companies():
    return {
        # REGIONAL RETAIL DOMINATORS
        "Regional Grocery Chains": [
            "Piggly Wiggly", "Food City", "Ingles Markets", "The Fresh Market", "Sprouts Farmers Market",
            "WinCo Foods", "Smart & Final", "Stater Bros", "Ralphs", "Vons",
            "Jewel-Osco", "Mariano's", "Pete's Fresh Market", "Tony's Fresh Market", "Caputo's",
            "Woodman's Markets", "Festival Foods", "Pick 'n Save", "Metro Market", "Copps",
            "Dierbergs", "Schnucks", "Shop 'n Save", "Fresh Thyme", "Lucky's Market",
            "Bristol Farms", "Gelson's", "Mollie Stone's", "Nugget Markets", "Raley's",
            "Bel Air", "Nob Hill Foods", "Save Mart", "FoodMaxx", "Lucky Supermarkets",
            "Bashas'", "Food 4 Less", "Ralphs", "Smith's Food and Drug", "Fry's Food",
            "King Soopers", "City Market", "QFC", "Fred Meyer", "Harris Teeter",
            "Lowes Foods", "Food Lion", "Bi-Lo", "Harveys", "Winn-Dixie",
            "Rouses Markets", "Brookshire's", "Super 1 Foods", "Market Street", "United Supermarkets"
        ],
        
        "Regional Gas Stations & Convenience": [
            "Kum & Go", "Stewart's Shops", "Turkey Hill", "Sunoco", "Marathon",
            "Speedway", "Circle K", "ampm", "Maverik", "Sinclair",
            "Phillips 66", "Conoco", "Citgo", "Valero", "Murphy USA",
            "RaceTrac", "RaceWay", "QuikTrip", "Kwik Trip", "Kwik Star",
            "Casey's General Store", "Sheetz", "Wawa", "Royal Farms", "Rutter's",
            "GetGo", "Speedway", "Thorntons", "Huck's", "Krist",
            "Holiday Stationstores", "Cenex", "Clark Brands", "Irving Oil", "Ultramar",
            "Esso", "Petro-Canada", "Husky", "Co-op", "UDF",
            "Duchess", "Allsup's", "Stripes", "Buc-ee's", "OnCue"
        ],
        
        "Regional Hardware & Home": [
            "Aubuchon Hardware", "Orgill", "Sutherlands", "Bomgaars", "Runnings",
            "Blain's Farm & Fleet", "Fleet Farm", "Tractor Supply", "Rural King", "Orscheln Farm & Home",
            "Atwoods", "Buchheit", "Big R", "North 40 Outfitters", "Coastal Farm & Ranch",
            "Wilco", "Bi-Mart", "Jerry's Home Improvement", "McCoy's Building Supply", "84 Lumber",
            "Carter Lumber", "Builders FirstSource", "ProBuild", "Stock Building Supply", "BMC",
            "ABC Supply", "Beacon Roofing Supply", "Allied Building Products", "Harvey Building Products", "Norandex",
            "Pacific Coast Building Products", "Huttig Building Products", "Rugby Building Products", "Klauer Manufacturing", "Ply Gem"
        ],
        
        "Regional Restaurant Chains": [
            "Waffle House", "Whataburger", "Culver's", "Bojangles", "Zaxby's",
            "Cook Out", "Raising Cane's", "Church's Chicken", "Golden Chick", "Chicken Express",
            "El Pollo Loco", "Del Taco", "Jack in the Box", "Carl's Jr", "Hardee's",
            "Rally's", "Checkers", "Krystal", "White Castle", "Steak 'n Shake",
            "Freddy's Frozen Custard", "Andy's Frozen Custard", "Braum's", "Dairy Queen", "Orange Julius",
            "A&W", "Long John Silver's", "Captain D's", "Joe's Crab Shack", "Red Lobster",
            "Olive Garden", "LongHorn Steakhouse", "Yard House", "The Capital Grille", "Eddie V's",
            "Seasons 52", "Bahama Breeze", "Bonefish Grill", "Carrabba's", "Fleming's",
            "Outback Steakhouse", "Texas Roadhouse", "Logan's Roadhouse", "Black Bear Diner", "Coco's Bakery"
        ],
        
        # B2B HIDDEN GIANTS
        "Industrial Distributors": [
            "W.W. Grainger", "Ferguson Enterprises", "HD Supply", "Watsco", "Anixter",
            "WESCO International", "Graybar Electric", "Rexel", "Sonepar", "CED",
            "Border States Electric", "Crescent Electric", "Platt Electric", "Wholesale Electric", "Elliott Electric",
            "MSC Industrial Direct", "Applied Industrial Technologies", "Motion Industries", "Kaman Distribution", "DXP Enterprises",
            "Fastenal", "Lawson Products", "Kimball Midwest", "Wurth Group", "Bossard",
            "SteelMaster", "Reliance Steel & Aluminum", "Ryerson", "Metal Supermarkets", "Online Metals",
            "McMaster-Carr", "Reid Supply", "Zoro", "Global Industrial", "Uline"
        ],
        
        "Food Service Distributors": [
            "Sysco", "US Foods", "Performance Food Group", "Gordon Food Service", "Reinhart Foodservice",
            "Ben E. Keith", "Shamrock Foods", "Cheney Brothers", "Nicholas & Company", "Zanios Foods",
            "Martin-Brower", "Golden State Foods", "Keystone Foods", "OSI Group", "JBS",
            "Smithfield Foods", "Hormel Foods", "Conagra Brands", "General Mills", "Kellogg's",
            "J.M. Smucker", "McCormick & Company", "Hershey", "Mondelez International", "PepsiCo",
            "Dr Pepper Snapple", "Monster Beverage", "Red Bull", "Vita Coco", "Harmless Harvest"
        ],
        
        "Uniform & Facility Services": [
            "Cintas", "UniFirst", "Aramark", "G&K Services", "AmeriPride",
            "Alsco", "Prudential Overall Supply", "Mission Linen Supply", "ImageFIRST", "CLEAN",
            "ABM Industries", "ISS Facility Services", "Compass Group", "Sodexo", "Elior Group",
            "SSP Group", "Delaware North", "Centerplate", "Levy Restaurants", "Wolfgang Puck Catering",
            "Ecolab", "Diversey", "Spartan Chemical", "Betco", "Hillyard",
            "Georgia-Pacific Professional", "Kimberly-Clark Professional", "SCA", "von Drehle", "Hospeco"
        ],
        
        "Packaging & Containers": [
            "Crown Holdings", "Ball Corporation", "Berry Global", "Sealed Air", "Sonoco",
            "WestRock", "International Paper", "Georgia-Pacific", "Domtar", "Clearwater Paper",
            "Graphic Packaging", "Reynolds Group", "Bemis Company", "AeroCanada", "CCL Industries",
            "Amcor", "Orora", "Huhtamaki", "Tetra Pak", "SIG Combibloc",
            "Berlin Packaging", "TricorBraun", "Vetropack", "O-I Glass", "Anchor Glass",
            "Ardagh Group", "Gerresheimer", "Schott", "Corning", "Nipro"
        ],
        
        # CRITICAL INFRASTRUCTURE
        "Payment Processing": [
            "First Data", "Global Payments", "Fiserv", "Jack Henry", "FIS",
            "TSYS", "Worldpay", "Adyen", "Square", "Stripe",
            "PayPal", "Braintree", "Authorize.Net", "2Checkout", "Skrill",
            "Payoneer", "Dwolla", "WePay", "Paysafe", "Nuvei",
            "Shift4 Payments", "Priority Payment Systems", "Paya", "Repay", "i3 Verticals",
            "NCR", "Diebold Nixdorf", "Ingenico", "Verifone", "PAX Technology"
        ],
        
        "Data Centers & Cloud Infrastructure": [
            "Equinix", "Digital Realty", "CyrusOne", "QTS Realty Trust", "CoreSite",
            "Flexential", "DataBank", "TierPoint", "Aligned Data Centers", "Stack Infrastructure",
            "Vantage Data Centers", "EdgeConneX", "Iron Mountain Data Centers", "365 Data Centers", "Cologix",
            "Interxion", "Global Switch", "NTT Communications", "KDDI", "China Telecom",
            "Keppel Data Centres", "ST Telemedia", "AirTrunk", "NEXTDC", "Digital Realty Trust",
            "Switch", "DuPont Fabros", "Sentinel Data Centers", "RagingWire", "IO Data Centers"
        ],
        
        "Cell Tower & Fiber": [
            "American Tower", "Crown Castle", "SBA Communications", "Cellnex Telecom", "IHS Towers",
            "Helios Towers", "Phoenix Tower International", "Vertical Bridge", "DigitalBridge", "Tillman Infrastructure",
            "Zayo Group", "CenturyLink", "Level 3 Communications", "Cogent Communications", "GTT Communications",
            "Windstream", "Consolidated Communications", "Cincinnati Bell", "Frontier Communications", "Lumen Technologies",
            "Uniti Group", "ExteNet Systems", "Mobilitie", "InSite Wireless", "Everywhere Wireless"
        ],
        
        # THE BORING BILLIONAIRE MAKERS
        "Auto Parts Retail": [
            "AutoZone", "O'Reilly Auto Parts", "Advance Auto Parts", "Genuine Parts Company", "NAPA",
            "Pep Boys", "Monro", "Midas", "Meineke", "Jiffy Lube",
            "Valvoline Instant Oil Change", "Firestone Complete Auto Care", "Goodyear Auto Service", "Discount Tire", "Tire Kingdom",
            "NTB - National Tire & Battery", "Mavis Discount Tire", "Belle Tire", "Conrad's", "Les Schwab",
            "Big O Tires", "Tire Discounters", "Town Fair Tire", "Sullivan Tire", "Merchant's Tire",
            "Car-X", "Tuffy Tire & Auto Service", "Precision Tune Auto Care", "AAMCO", "Cottman Transmission"
        ],
        
        "Dollar Stores & Discount": [
            "Family Dollar", "99 Cents Only Stores", "Dollar Tree", "Dollar General", "Five Below",
            "Big Lots", "Ollie's Bargain Outlet", "Ocean State Job Lot", "Christmas Tree Shops", "Tuesday Morning",
            "dd's Discounts", "Grocery Outlet", "United Grocery Outlet", "Sharp Shopper", "BB's Grocery Outlet",
            "NPS Store", "Roses Discount Stores", "Maxway", "Fred's", "Bargain Hunt",
            "Dirt Cheap", "Hudson's Treasure Rooms", "Gabriel Brothers", "Rugged Wearhouse", "Citi Trends"
        ],
        
        "Self Storage": [
            "Public Storage", "Extra Space Storage", "CubeSmart", "Life Storage", "U-Haul",
            "National Storage Affiliates", "Simply Self Storage", "Prime Storage", "Storage King", "YourSpace",
            "iStorage", "Metro Self Storage", "Compass Self Storage", "Devon Self Storage", "Great Value Storage",
            "AAA Storage", "Security Public Storage", "Guardian Storage", "Space Shop", "Storage Mart",
            "StoragePRO", "A-1 Self Storage", "Price Self Storage", "Pogoda Companies", "Strategic Storage Trust",
            "Move It Self Storage", "Storage Rentals of America", "Northwest Self Storage", "Storage Solutions", "EZ Storage"
        ],
        
        "Car Wash Chains": [
            "Mister Car Wash", "International Car Wash Group", "Autobell Car Wash", "Zips Car Wash", "Take 5 Car Wash",
            "Quick Quack Car Wash", "Tidal Wave Auto Spa", "Splash Car Wash", "Prime Car Wash", "Hoffman Car Wash",
            "Delta Sonic", "Terrible Herbst", "Cobblestone Auto Spa", "Goo Goo Express", "Wash Depot",
            "Tommy's Express", "Rocket Carwash", "Club Car Wash", "Soapy Joe's", "WhiteWater Express",
            "Blue Wave Express", "Wiggy Wash", "Boomerang Car Wash", "Crew Carwash", "Mike's Carwash"
        ],
        
        # GOVERNMENT CONTRACTORS
        "Defense Contractors": [
            "General Dynamics", "L3Harris Technologies", "CACI International", "SAIC", "Leidos",
            "Booz Allen Hamilton", "CSRA", "DynCorp", "PAE", "Vectrus",
            "KBR", "Fluor", "Jacobs Engineering", "AECOM", "Parsons Corporation",
            "Bechtel", "Huntington Ingalls Industries", "BWX Technologies", "Aerojet Rocketdyne", "Orbital ATK",
            "MITRE Corporation", "Aerospace Corporation", "IDA", "RAND Corporation", "Battelle",
            "SRI International", "Applied Research Associates", "Southwest Research Institute", "Georgia Tech Research Institute", "APL"
        ],
        
        "IT Services Contractors": [
            "GDIT", "Peraton", "Vencore", "KeyW", "CACI",
            "ManTech", "Engility", "STG", "NCI", "Salient CRGT",
            "Pragmatics", "Sotera Defense Solutions", "MacAulay-Brown", "Alion Science", "QinetiQ North America",
            "Camber Corporation", "Cobham", "Ultra Electronics", "MAG Aerospace", "AAR Corp",
            "VSE Corporation", "Kratos Defense", "Mercury Systems", "Comtech Telecommunications", "ViaSat"
        ],
        
        # SUPPLY CHAIN MIDDLEMEN
        "Freight Brokers": [
            "C.H. Robinson", "Echo Global Logistics", "Total Quality Logistics", "XPO Logistics", "Coyote Logistics",
            "Transplace", "GlobalTranz", "Mode Transportation", "Arrive Logistics", "Uber Freight",
            "Convoy", "Redwood Logistics", "BlueGrace Logistics", "Trinity Logistics", "Nolan Transportation Group",
            "Allen Lund Company", "Sunset Transportation", "ATS Logistics", "Armstrong Transport Group", "Johanson Transportation",
            "England Logistics", "PLS Logistics", "Ascent Global Logistics", "ROAR Logistics", "Zipline Logistics"
        ],
        
        "Chemical Distributors": [
            "Univar Solutions", "Brenntag", "Nexeo Solutions", "Azelis", "IMCD",
            "Omya", "Safic-Alcan", "Biesterfeld", "Stockmeier", "Quimidroga",
            "Caldic", "Lehmann & Voss", "Nordmann", "Ter Chemicals", "ChemPoint",
            "Palmer Holland", "Maroon Group", "Special Materials Company", "Buckley Oil", "Tilley Chemical",
            "Hall Technologies", "Essential Ingredients", "Prinova", "Barentz", "Connell Brothers"
        ],
        
        "Electronic Components": [
            "Arrow Electronics", "Avnet", "Future Electronics", "Digi-Key", "Mouser Electronics",
            "Newark", "Allied Electronics", "RS Components", "TTI Inc", "Heilind Electronics",
            "Master Electronics", "Richardson Electronics", "Sager Electronics", "Symmetry Electronics", "PUI Audio",
            "Marsh Electronics", "Carlton-Bates", "Powell Electronics", "Chip1Stop", "CoreStaff",
            "Fusion Worldwide", "Smith", "Converge", "NewPower Worldwide", "Rutronik"
        ],
        
        # FRANCHISE EMPIRES
        "Restaurant Mega-Franchisees": [
            "Flynn Restaurant Group", "NPC International", "Carrols Restaurant Group", "Sun Holdings", "GPS Hospitality",
            "Dhanani Group", "Luihn VantEdge Partners", "Guillory Group", "Harman Management", "Sizzling Platter",
            "Apple Core Enterprises", "TOMS King", "KBP Brands", "Meridian Restaurants Unlimited", "Summit Restaurant Group",
            "Tacala Companies", "Valenti Management", "Ampler Group", "Border Foods", "JIB Management"
        ],
        
        "Hotel Management Companies": [
            "Aimbridge Hospitality", "Interstate Hotels & Resorts", "White Lodging", "Pyramid Hotel Group", "Remington Hotels",
            "Crescent Hotels & Resorts", "Davidson Hospitality", "Highgate", "HEI Hotels", "Sage Hospitality",
            "Commune Hotels", "Two Roads Hospitality", "Benchmark Global Hospitality", "Noble House Hotels", "Omni Hotels",
            "Marcus Hotels", "Destination Hotels", "Rosewood Hotel Group", "Langham Hospitality", "Mandarin Oriental"
        ],
        
        "Fitness Franchises": [
            "Planet Fitness", "Anytime Fitness", "OrangeTheory Fitness", "F45 Training", "9Round",
            "Snap Fitness", "Crunch Fitness", "LA Fitness", "24 Hour Fitness", "Gold's Gym",
            "Equinox", "Life Time Fitness", "UFC Gym", "Title Boxing Club", "CycleBar",
            "Pure Barre", "Club Pilates", "YogaSix", "StretchLab", "The Bar Method",
            "SoulCycle", "Barry's Bootcamp", "Solidcore", "Row House", "AKT"
        ],
        
        # THE TRULY INVISIBLE
        "Title & Escrow Companies": [
            "First American Title", "Old Republic Title", "Stewart Title", "Fidelity National Title", "Chicago Title",
            "Commonwealth Land Title", "WFG National Title", "Title Resources Group", "Investors Title", "North American Title",
            "Attorneys' Title", "Security Title", "Ticor Title", "Transnation Title", "DataTrace",
            "Amrock", "ServiceLink", "Westcor Land Title", "Title365", "States Title"
        ],
        
        "Payroll & HR Services": [
            "ADP", "Paychex", "Paycom", "Paylocity", "Ceridian",
            "Ultimate Software", "Kronos", "Workday", "Namely", "Gusto",
            "Rippling", "Zenefits", "TriNet", "Insperity", "Paycor",
            "Bamboo HR", "Justworks", "Deel", "Remote", "Papaya Global",
            "Personio", "HiBob", "Lattice", "Culture Amp", "15Five"
        ],
        
        "Background Check Companies": [
            "Sterling", "HireRight", "First Advantage", "GoodHire", "Checkr",
            "Accurate Background", "InfoMart", "PreCheck", "Verified Credentials", "IntelliCorp",
            "ScreeningWorks", "Employment Screening Services", "Orange Tree", "DISA", "ClearStar",
            "TalentWise", "Asurint", "backgroundchecks.com", "Universal Background Screening", "Shield Screening"
        ],
        
        "Debt Collection Agencies": [
            "Encore Capital Group", "Portfolio Recovery Associates", "Alorica", "Convergent Outsourcing", "MRS Associates",
            "Transworld Systems", "IC System", "CBE Group", "Weltman Weinberg", "AllianceOne",
            "National Credit Systems", "Professional Finance Company", "Hunter Warfield", "Plaza Services", "Credit Management LP",
            "Harris & Harris", "GC Services", "Pioneer Credit Recovery", "Coast Professional", "Van Ru Credit"
        ]
    }

def main():
    companies = get_boring_but_essential_companies()
    
    # Count total
    total = sum(len(v) for v in companies.values())
    print(f"Total boring but essential companies: {total}")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/logos/boring_essential_list.txt', 'w') as f:
        for category, company_list in companies.items():
            f.write(f"\n## {category}\n")
            for company in company_list:
                f.write(f"{company}\n")
    
    print("Saved to boring_essential_list.txt")

if __name__ == "__main__":
    main()