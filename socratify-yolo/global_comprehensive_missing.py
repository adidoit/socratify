#!/usr/bin/env python3
"""
Comprehensive global missing companies based on 4 Task analyses
Companies frequently mentioned in FT, WSJ, Bloomberg, business media
"""

def get_comprehensive_global_missing():
    """Master list of globally significant companies from business media"""
    return {
        "AI_ML_Unicorns": [
            "Safe Superintelligence", "Groq", "Lambda", "Celestial AI", "Figure",
            "Abridge", "Synthesia", "AnySphere", "The Bot Company", "Krutrim",
            "Anthropic", "Character.AI", "Stability AI", "Hugging Face", "Midjourney",
            "Runway", "Jasper", "Copy.ai", "Notion AI", "Linear", "Miro",
            "Figma", "Canva", "Airtable", "Monday.com", "Asana", "ClickUp",
            "Retool", "Webflow", "Zapier", "GitLab", "HashiCorp", "Databricks",
            "Snowflake", "Confluent", "JetBrains", "Postman", "Vercel"
        ],
        
        "Global_Fintech": [
            "Revolut", "Klarna", "Checkout.com", "N26", "Trade Republic", "Rapyd",
            "SumUp", "Monzo", "Pennylane", "Wise", "MoneyView", "Perfios",
            "Sygnum", "Airwallex", "Momo", "Coda Payments", "Chime", "Robinhood",
            "Affirm", "Marqeta", "Plaid"
        ],
        
        "Climate_Tech": [
            "Form Energy", "24M Technologies", "Twelve", "Helion Energy",
            "Commonwealth Fusion", "Stegra", "X-energy", "Pacific Fusion",
            "Rivian", "Lucid Motors", "Polestar", "Arrival", "Canoo"
        ],
        
        "Healthcare_Biotech": [
            "Flo Health", "Ro", "Hims & Hers", "Mindstrong", "Livongo",
            "Teladoc", "Moderna", "10x Genomics", "Ginkgo Bioworks", "Zymergen"
        ],
        
        "Food_Tech": [
            "Impossible Foods", "Beyond Meat", "Perfect Day", "Apeel Sciences",
            "Plenty", "Memphis Meats", "NotCo"
        ],
        
        "Gaming_Entertainment": [
            "Epic Games", "Discord", "Roblox", "Unity", "Niantic"
        ],
        
        "Indian_Giants": [
            "Tata Consultancy Services", "Reliance Industries", "Adani Group",
            "Mahindra Group", "Bajaj Group", "Aditya Birla Group", "Larsen & Toubro",
            "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "State Bank of India",
            "HDFC Bank", "ICICI Bank", "Axis Bank", "Kotak Mahindra Bank",
            "Sun Pharmaceutical", "Dr Reddys Laboratories", "Cipla", "Lupin",
            "Oil and Natural Gas Corporation", "Indian Oil Corporation", "Coal India"
        ],
        
        "Chinese_Giants": [
            "Industrial and Commercial Bank of China", "Bank of China",
            "China Construction Bank", "Agricultural Bank of China", "Alibaba Group",
            "Tencent Holdings", "Baidu", "JD.com", "ByteDance", "China National Petroleum Corporation",
            "Sinopec", "State Grid Corporation of China", "China Mobile", "China Telecom",
            "China Unicom", "BYD", "SAIC Motor", "China Railway Group",
            "China Communications Construction"
        ],
        
        "Brazilian_Giants": [
            "Vale SA", "Petrobras", "Itau Unibanco", "Banco do Brasil",
            "Bradesco", "JBS", "BRF", "Ambev", "Embraer",
            "CSN", "Suzano", "Localiza"
        ],
        
        "Korean_Chaebols": [
            "LG Group", "LG Electronics", "LG Chem", "LG Energy Solution",
            "Hyundai Motor Group", "Hyundai Motor", "Kia", "SK Group",
            "SK Hynix", "SK Telecom", "SK Innovation", "Lotte Group",
            "Hanwha Group", "POSCO"
        ],
        
        "Indonesian_Conglomerates": [
            "Astra International", "Sinar Mas Group", "Salim Group",
            "Lippo Group", "Bank Central Asia", "Bank Mandiri",
            "Bank Rakyat Indonesia", "PT Freeport Indonesia", "Sinar Mas Agro"
        ],
        
        "Middle_East_Giants": [
            "Emirates Airlines", "Abu Dhabi National Oil Company", "Etisalat",
            "Dubai Electricity and Water Authority", "DP World", "Saudi Aramco",
            "Saudi Basic Industries Corporation", "Al Rajhi Bank", "Saudi National Bank",
            "Qatar Airways", "Qatar National Bank", "Ooredoo"
        ],
        
        "Turkish_Companies": [
            "Turkish Airlines", "Akbank", "Turkcell", "Koc Holding",
            "Sabanci Holding", "Garanti BBVA", "Arcеlik"
        ],
        
        "Mexican_Companies": [
            "America Movil", "FEMSA", "Grupo Bimbo", "Cemex",
            "Televisa", "Banorte", "Grupo Mexico"
        ],
        
        "South_African_Companies": [
            "Anglo American", "Naspers", "Shoprite", "MTN Group",
            "Standard Bank", "Sasol", "Gold Fields"
        ],
        
        "Southeast_Asian_Companies": [
            "CP Group", "PTT", "Bangkok Bank", "Genting Group",
            "Petronas", "Public Bank", "Sime Darby", "DBS Bank",
            "Singapore Airlines", "Wilmar International"
        ],
        
        "Commodity_Traders": [
            "Vitol Group", "Glencore International", "Trafigura Group",
            "Gunvor Group", "Mercuria Energy", "Cargill Inc", "ADM",
            "Louis Dreyfus Company", "Bunge Limited", "COFCO International"
        ],
        
        "Hedge_Funds_PE": [
            "Bridgewater Associates", "Renaissance Technologies", "Citadel LLC",
            "Elliott Management", "Pershing Square Capital", "Two Sigma Investments",
            "DE Shaw & Co", "Millennium Management", "Point72 Asset Management",
            "Lone Pine Capital"
        ],
        
        "Family_Owned_Empires": [
            "Koch Industries", "Mars Inc", "Ferrero Group", "Hermes International",
            "BMW Group", "Walmart", "Samsung Group", "Tata Group",
            "Reliance Industries", "Alibaba Group"
        ],
        
        "Infrastructure_Engineering": [
            "Bechtel Corporation", "Fluor Corporation", "Turner Construction",
            "Skanska AB", "Vinci SA", "Bouygues Group",
            "China Communications Construction Company", "Larsen & Toubro"
        ],
        
        "Shipping_Maritime": [
            "Maersk Group", "Mediterranean Shipping Company", "CMA CGM Group",
            "Hapag-Lloyd", "COSCO Shipping", "Evergreen Marine", "Yang Ming Marine Transport"
        ],
        
        "Mining_Materials": [
            "BHP Group", "Rio Tinto", "Vale", "Southern Copper Corporation",
            "Glencore", "Anglo American", "ArcelorMittal", "Nucor Corporation",
            "POSCO International", "BASF SE"
        ],
        
        "Oil_Gas_Giants": [
            "Saudi Aramco", "ExxonMobil", "Chevron", "TotalEnergies",
            "ConocoPhillips", "China National Offshore Oil Corporation", "Petrobras",
            "Baker Hughes", "SLB", "Halliburton", "Alyeska Pipeline Service Company",
            "Kinder Morgan"
        ],
        
        "Utilities_Power": [
            "NextEra Energy", "Duke Energy", "Southern Company", "Exelon Corporation",
            "Iberdrola", "Orsted", "TotalEnergies", "Constellation Energy",
            "EDF", "Westinghouse Electric"
        ],
        
        "Transportation": [
            "United Airlines", "Delta Air Lines", "American Airlines",
            "BNSF Railway", "SNCF Group", "Canadian National Railway",
            "FedEx Corporation", "UPS", "XPO Logistics", "JB Hunt Transport Services",
            "CH Robinson", "Amazon Logistics"
        ],
        
        "Telecommunications": [
            "Comcast", "Verizon", "AT&T", "China Mobile",
            "NTT", "American Tower", "Crown Castle", "SBA Communications"
        ],
        
        "Healthcare_Specialized": [
            "GE Healthcare", "Abbott", "Intuitive Surgical", "Masimo",
            "McKesson", "AmerisourceBergen", "Cardinal Health", "UnitedHealth Group",
            "Centene", "HCA Healthcare"
        ],
        
        "Industrial_Manufacturing": [
            "Siemens AG", "ABB Ltd", "Rockwell Automation", "Schneider Electric",
            "Honeywell International", "Caterpillar", "KUKA AG", "Mitsubishi Electric",
            "Emerson Electric", "Omron"
        ],
        
        "Financial_Services_Specialized": [
            "PayNearMe", "Remitly", "Payoneer", "First American Financial",
            "Alliant Specialty", "Electronic Payments", "Block", "CME Group",
            "Intercontinental Exchange"
        ],
        
        "Media_Entertainment": [
            "Comcast", "Walt Disney", "Sony Entertainment", "Sony Music Entertainment",
            "Universal Music Group", "Thomson Reuters", "ESPN", "Fox Sports"
        ],
        
        "Retail_Consumer": [
            "Walmart", "Kroger", "Costco", "Albertsons", "Publix",
            "H-E-B", "Aldi", "Target", "The Home Depot", "TJX Companies",
            "McDonalds", "Starbucks"
        ],
        
        "Private_Luxury": [
            "Chanel", "Patek Philippe", "Rolex", "Prada Group", "Burberry Group"
        ],
        
        "Tech_Unicorns_Additional": [
            "Epic Games", "SpaceX", "Stripe", "ByteDance", "Grab Holdings"
        ]
    }

def main():
    companies_dict = get_comprehensive_global_missing()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"Total unique companies across all categories: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/global_comprehensive_list.txt', 'w') as f:
        f.write("COMPREHENSIVE GLOBAL COMPANIES FROM BUSINESS MEDIA\n")
        f.write("=" * 55 + "\n\n")
        f.write(f"Total unique companies: {len(unique_companies)}\n")
        f.write(f"Categories: {len(companies_dict)}\n\n")
        
        f.write("Based on analysis of companies frequently mentioned in:\n")
        f.write("- Financial Times\n- Wall Street Journal\n- Bloomberg\n")
        f.write("- TechCrunch\n- Regional business media\n\n")
        
        for i, company in enumerate(unique_companies, 1):
            f.write(f"{i:3d}. {company}\n")
    
    print(f"\nSaved to global_comprehensive_list.txt")
    return unique_companies

if __name__ == "__main__":
    main()