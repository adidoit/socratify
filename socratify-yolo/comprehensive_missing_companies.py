#!/usr/bin/env python3
"""
Comprehensive list of 500+ additional companies that may be missing
Based on Task analysis of gaps in current collection
"""

def get_comprehensive_missing_list():
    """500+ potentially missing high-value companies"""
    return {
        "Fortune 500 Energy": [
            "Chevron", "ExxonMobil", "ConocoPhillips", "Marathon Petroleum", 
            "Phillips 66", "Valero Energy", "Enterprise Products Partners",
            "Plains GP Holdings", "Kinder Morgan", "Energy Transfer"
        ],
        
        "Fortune 500 Retail": [
            "Target", "Home Depot", "Kroger", "Costco", "Lowes", "CVS Health",
            "Walgreens Boots Alliance", "Best Buy", "TJX Companies", "Dollar General",
            "Dollar Tree", "Ross Stores", "Nordstrom", "Macys", "Kohls"
        ],
        
        "Fortune 500 Healthcare": [
            "UnitedHealth Group", "Anthem", "Humana", "Centene Corporation",
            "Molina Healthcare", "WellCare Health Plans", "Cardinal Health",
            "AmerisourceBergen", "McKesson Corporation"
        ],
        
        "Fortune 500 Industrials": [
            "General Electric", "Caterpillar", "Honeywell", "3M", "Illinois Tool Works",
            "Emerson Electric", "Danaher", "Parker-Hannifin", "Eaton Corporation",
            "Deere & Company", "CNH Industrial", "AGCO Corporation", "Ingersoll Rand",
            "Stanley Black & Decker", "Textron", "Dover Corporation"
        ],
        
        "Fortune 500 Food & Consumer": [
            "Procter & Gamble", "PepsiCo", "Mondelez International", "General Mills",
            "Kellogg Company", "Campbell Soup", "Tyson Foods", "JM Smucker",
            "Hormel Foods", "ConAgra Brands", "McCormick & Company"
        ],
        
        "Major Consulting Firms": [
            "Oliver Wyman", "A.T. Kearney", "Roland Berger", "Strategy&", 
            "L.E.K. Consulting", "Accenture Strategy", "IBM Consulting",
            "Capgemini Consulting", "Cognizant", "Infosys Consulting", "TCS",
            "Alvarez & Marsal", "FTI Consulting", "Huron Consulting",
            "Navigant Consulting", "Parthenon-EY", "Monitor Deloitte",
            "NERA Economic Consulting", "Analysis Group", "Charles River Associates"
        ],
        
        "Investment Banks": [
            "Credit Suisse", "Deutsche Bank", "Barclays", "UBS", "HSBC",
            "BNP Paribas", "Societe Generale", "Jefferies", "William Blair",
            "Piper Sandler", "Raymond James", "Stephens Inc", "Harris Williams",
            "Lincoln International", "Houlihan Lokey", "Evercore", "Lazard",
            "Centerview Partners", "Moelis & Company"
        ],
        
        "Asset Management": [
            "Northern Trust", "Franklin Templeton", "Invesco", "KKR",
            "Apollo Global Management", "Carlyle Group", "TPG", "Warburg Pincus",
            "Vista Equity Partners", "Leonard Green & Partners", "Hellman & Friedman",
            "Francisco Partners", "CVC Capital Partners", "EQT Partners", "Permira"
        ],
        
        "Pharma & Biotech": [
            "Pfizer", "Merck & Co", "Bristol Myers Squibb", "Eli Lilly", "Amgen",
            "Gilead Sciences", "Biogen", "Regeneron Pharmaceuticals", "Vertex Pharmaceuticals",
            "Alexion Pharmaceuticals", "Moderna", "BioNTech", "Illumina", "10x Genomics",
            "Genmab", "Seagen", "BioMarin", "Incyte", "Exact Sciences"
        ],
        
        "Medical Devices": [
            "Medtronic", "Abbott Laboratories", "Boston Scientific", "Stryker",
            "Zimmer Biomet", "Edwards Lifesciences", "Intuitive Surgical",
            "Danaher Corporation", "Becton Dickinson", "Baxter International"
        ],
        
        "Healthcare Services": [
            "HCA Healthcare", "Tenet Healthcare", "Community Health Systems",
            "Universal Health Services", "Labcorp", "Quest Diagnostics",
            "DaVita", "Fresenius Medical Care", "Encompass Health"
        ],
        
        "European Giants": [
            "Nestle", "Unilever", "SAP", "ASML", "LVMH", "L'Oreal", "Hermes",
            "Adidas", "Puma", "Volkswagen", "BMW", "Mercedes-Benz", "Airbus",
            "Total Energies", "Shell", "BP", "Roche", "Novartis", "Sanofi",
            "AstraZeneca", "GlaxoSmithKline", "Diageo", "AB InBev", "Heineken",
            "ING Group", "ABN AMRO", "Deutsche Bank", "Credit Suisse", "UBS"
        ],
        
        "Asian Corporations": [
            "Toyota", "Sony", "Nintendo", "SoftBank", "TSMC", "Samsung",
            "Hyundai", "LG Electronics", "Mitsubishi", "Mitsui", "Sumitomo",
            "Honda", "Panasonic", "Sharp", "Toshiba", "Fujitsu", "NEC",
            "Rakuten", "Softbank", "KDDI", "NTT DoCoMo"
        ],
        
        "Chinese Tech Giants": [
            "Alibaba", "Tencent", "Baidu", "JD.com", "Meituan", "Pinduoduo",
            "NetEase", "Xiaomi", "ByteDance", "BYD", "CATL", "SMIC",
            "Lenovo", "Huawei", "ZTE", "Oppo", "Vivo", "OnePlus"
        ],
        
        "Indian Corporations": [
            "Reliance Industries", "Tata Consultancy Services", "Infosys",
            "Wipro", "HCL Technologies", "HDFC Bank", "ICICI Bank",
            "State Bank of India", "Bharti Airtel", "Tech Mahindra"
        ],
        
        "High-Growth Fintech": [
            "Stripe", "Klarna", "Revolut", "Chime", "Robinhood", "Coinbase",
            "Binance", "Square", "PayPal", "Adyen", "Affirm", "Afterpay",
            "SoFi", "Lending Club", "LendingTree", "Credit Karma", "Mint",
            "Personal Capital", "Betterment", "Wealthfront"
        ],
        
        "Enterprise Software": [
            "Snowflake", "Databricks", "Figma", "Notion", "Monday.com",
            "DocuSign", "Workday", "ServiceNow", "Splunk", "New Relic",
            "Datadog", "PagerDuty", "Okta", "Auth0", "Ping Identity",
            "CyberArk", "Fortinet", "Check Point", "Palo Alto Networks"
        ],
        
        "E-commerce & Marketplaces": [
            "Shopify", "Mercado Libre", "Sea Limited", "Grab", "GoTo Group",
            "Flipkart", "Instacart", "DoorDash", "Delivery Hero", "Just Eat Takeaway",
            "Grubhub", "Postmates", "Caviar", "Seamless", "Eat24"
        ],
        
        "Consumer Brands": [
            "Nike", "H&M", "Zara", "Uniqlo", "Gap", "Levi Strauss",
            "Under Armour", "lululemon", "Patagonia", "The North Face",
            "Columbia Sportswear", "Timberland", "Converse", "Vans"
        ],
        
        "Luxury Brands": [
            "Kering", "Richemont", "Burberry", "Prada", "Gucci",
            "Louis Vuitton", "Chanel", "Tiffany & Co", "Cartier",
            "Bulgari", "Rolex", "Patek Philippe", "Audemars Piguet"
        ],
        
        "Consumer Electronics": [
            "Dell Technologies", "HP Inc", "Lenovo", "Asus", "Canon",
            "Nikon", "GoPro", "Fitbit", "Garmin", "TomTom", "Roku",
            "Sonos", "Bose", "Beats", "Sennheiser"
        ],
        
        "Home & Retail": [
            "Williams-Sonoma", "Bed Bath & Beyond", "Wayfair", "Overstock.com",
            "Pottery Barn", "West Elm", "CB2", "Restoration Hardware",
            "Room & Board", "Crate & Barrel"
        ],
        
        "Aerospace & Defense": [
            "Boeing", "Lockheed Martin", "Raytheon Technologies", "Northrop Grumman",
            "General Dynamics", "L3Harris", "BAE Systems", "Thales",
            "Leonardo", "Saab", "Dassault Aviation", "Embraer", "Bombardier"
        ],
        
        "Materials & Chemicals": [
            "DuPont", "Dow Inc", "PPG Industries", "Sherwin-Williams",
            "Air Products & Chemicals", "Linde", "Ecolab", "Eastman Chemical",
            "LyondellBasell", "Celanese", "Huntsman Corporation"
        ],
        
        "Transportation & Logistics": [
            "FedEx", "UPS", "Union Pacific", "CSX Transportation", "Norfolk Southern",
            "BNSF Railway", "Kansas City Southern", "Canadian National Railway",
            "Canadian Pacific Railway", "Deutsche Post DHL", "Royal Mail"
        ],
        
        "Insurance": [
            "AIG", "Prudential Financial", "MetLife", "Travelers Companies",
            "Progressive Corporation", "Allstate", "State Farm", "GEICO",
            "Liberty Mutual", "Nationwide", "USAA", "Farmers Insurance"
        ],
        
        "Regional Banks": [
            "PNC Financial", "Truist Financial", "Bank of New York Mellon",
            "Charles Schwab Corporation", "US Bancorp", "TD Ameritrade",
            "E*TRADE", "Interactive Brokers", "Fidelity Investments"
        ],
        
        "Payment Processors": [
            "Visa", "Mastercard", "American Express", "Discover Financial Services",
            "Western Union", "MoneyGram", "Remitly", "Wise", "Remit2India"
        ],
        
        "Media & Entertainment": [
            "Disney", "Netflix", "Warner Bros Discovery", "Paramount Global",
            "NBCUniversal", "Fox Corporation", "Sony Pictures", "Lionsgate",
            "MGM", "A24", "Blumhouse", "Marvel Entertainment"
        ],
        
        "Telecommunications": [
            "Verizon", "AT&T", "T-Mobile", "Sprint", "Charter Communications",
            "Comcast", "Cox Communications", "Altice USA", "Frontier Communications",
            "CenturyLink", "Windstream", "TDS Telecom"
        ],
        
        "Utilities": [
            "NextEra Energy", "Duke Energy", "Southern Company", "Exelon",
            "American Electric Power", "Pacific Gas & Electric", "Consolidated Edison",
            "Sempra Energy", "Public Service Enterprise Group", "Xcel Energy"
        ],
        
        "Real Estate": [
            "CBRE Group", "Jones Lang LaSalle", "Cushman & Wakefield",
            "Colliers International", "Marcus & Millichap", "Newmark",
            "Prologis", "Public Storage", "Welltower", "Equity Residential",
            "AvalonBay Communities", "Boston Properties", "Vornado Realty Trust"
        ],
        
        "Food & Beverage": [
            "Coca-Cola", "PepsiCo", "Nestlé", "Unilever", "Mars",
            "Ferrero", "Mondelez", "General Mills", "Kellogg", "Campbell Soup",
            "Kraft Heinz", "ConAgra", "Hormel", "Tyson Foods", "JBS"
        ],
        
        "Airlines": [
            "American Airlines", "Delta Air Lines", "United Airlines",
            "Southwest Airlines", "JetBlue Airways", "Alaska Airlines",
            "Spirit Airlines", "Frontier Airlines", "Hawaiian Airlines"
        ],
        
        "Hospitality & Travel": [
            "Marriott International", "Hilton", "InterContinental Hotels Group",
            "Hyatt", "Wyndham Hotels", "Choice Hotels", "Best Western",
            "Expedia Group", "Booking Holdings", "Airbnb", "TripAdvisor"
        ],
        
        "Automotive": [
            "General Motors", "Ford", "Stellantis", "Tesla", "Rivian",
            "Lucid Motors", "Toyota", "Honda", "Nissan", "Hyundai",
            "Kia", "Volkswagen", "BMW", "Mercedes-Benz", "Audi", "Porsche"
        ]
    }

def main():
    companies_dict = get_comprehensive_missing_list()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"Total unique companies to check: {len(unique_companies)}")
    print(f"Categories: {len(companies_dict)}")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/comprehensive_companies_to_check.txt', 'w') as f:
        f.write("COMPREHENSIVE COMPANIES TO CHECK\n")
        f.write("=" * 35 + "\n\n")
        f.write(f"Total companies: {len(unique_companies)}\n\n")
        
        for i, company in enumerate(unique_companies, 1):
            f.write(f"{i:3d}. {company}\n")
    
    print("Saved to comprehensive_companies_to_check.txt")
    return unique_companies

if __name__ == "__main__":
    main()