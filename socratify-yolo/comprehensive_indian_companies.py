#!/usr/bin/env python3
"""
Comprehensive Indian companies based on Task analysis
All tiers: Top tier (Nifty 50), Middle tier, Bottom tier, Startups, Heritage companies
"""

def get_comprehensive_indian_companies():
    """Master list of Indian companies across all tiers and sectors"""
    return {
        "Top_Tier_Nifty50": [
            "Infosys Limited", "Wipro Limited", "HCL Technologies", "Tech Mahindra",
            "ICICI Bank", "Kotak Mahindra Bank", "IndusInd Bank", "Yes Bank",
            "Punjab National Bank", "Bank of Baroda", "Canara Bank", "Union Bank of India",
            "Hindustan Unilever", "Nestle India", "Britannia Industries",
            "Godrej Consumer Products", "Emami Limited", "Bajaj Finance",
            "Bajaj Finserv", "Bajaj Auto", "Maruti Suzuki India",
            "Mahindra & Mahindra", "TVS Motor Company", "Eicher Motors",
            "JSW Steel", "Vedanta Limited", "NALCO", "NMDC", "SAIL",
            "Grasim Industries", "UPL Limited", "ONGC", "BPCL", "GAIL",
            "NTPC", "BHEL", "BEL", "Ambuja Cement", "Shree Cement",
            "Divi's Laboratories", "Dr Reddy's Laboratories", "Lupin Limited",
            "Aurobindo Pharma", "Biocon Limited", "Cadila Healthcare",
            "Titan Company", "Page Industries", "Avenue Supermarts", "Pidilite Industries"
        ],
        
        "IT_Services_Technology": [
            "L&T Infotech", "Mindtree", "Mphasis", "Persistent Systems",
            "Cyient", "KPIT Technologies", "Hexaware Technologies", "Zensar Technologies",
            "Tata Elxsi", "eClerx Services"
        ],
        
        "Pharmaceuticals_Healthcare": [
            "Torrent Pharmaceuticals", "Alkem Laboratories", "Glenmark Pharmaceuticals",
            "Ipca Laboratories", "Mankind Pharma", "Abbott India", "Pfizer India",
            "GlaxoSmithKline India", "Sanofi India", "Novartis India"
        ],
        
        "Banking_Financial_Services": [
            "HDFC Life Insurance", "SBI Life Insurance", "LIC", "ICICI Prudential Life",
            "Max Life Insurance", "Muthoot Finance", "Shriram Transport Finance",
            "Bajaj Finance", "L&T Finance Holdings", "Cholamandalam Investment"
        ],
        
        "FMCG_Consumer_Goods": [
            "Parle Products", "Haldiram's", "Amul", "Mother Dairy",
            "Patanjali Ayurved", "Himalaya Drug Company", "Colgate-Palmolive India",
            "Procter & Gamble India", "Reckitt Benckiser India", "Johnson & Johnson India"
        ],
        
        "Automotive_Auto_Components": [
            "Force Motors", "Hero Electric", "Ather Energy", "Bosch India",
            "Motherson Sumi Systems", "Bharat Forge"
        ],
        
        "State_Owned_Enterprises": [
            "Indian Railways", "Food Corporation of India", "Hindustan Aeronautics Limited",
            "Mazagon Dock Shipbuilders", "Garden Reach Shipbuilders", "Cochin Shipyard Limited",
            "Rashtriya Ispat Nigam Limited", "Neyveli Lignite Corporation", "Oil India Limited",
            "Engineers India Limited"
        ],
        
        "Regional_Banks": [
            "Karnataka Bank", "South Indian Bank", "Karur Vysya Bank",
            "City Union Bank", "Federal Bank", "Dhanlaxmi Bank",
            "Nainital Bank", "Punjab & Sind Bank", "Indian Overseas Bank",
            "Central Bank of India"
        ],
        
        "Infrastructure_Construction": [
            "Gammon India", "HCC", "Punj Lloyd", "IVRCL Infrastructure",
            "GMR Infrastructure", "GVK Group", "IRB Infrastructure",
            "Sadbhav Engineering", "NCC Limited"
        ],
        
        "Textile_Apparel": [
            "Arvind Limited", "Welspun India", "Trident Limited",
            "Vardhman Textiles", "Indo Count Industries", "Bombay Dyeing",
            "Raymond Limited", "Aditya Birla Fashion and Retail", "Future Retail",
            "V-Mart Retail"
        ],
        
        "Major_Unicorns_Startups": [
            "Flipkart", "Paytm", "Byju's", "Ola Electric", "Zomato",
            "Swiggy", "PhonePe", "Slice", "Jupiter", "Fi Money",
            "Navi", "BharatPe", "Myntra", "Snapdeal", "Urban Company",
            "Unacademy", "Vedantu", "Toppr", "WhiteHat Jr", "Practo",
            "1mg", "DocsApp", "Portea Medical", "Uber India", "BlackBuck"
        ],
        
        "Fintech_Companies": [
            "Pine Labs", "Instamojo", "Cashfree", "PayU India",
            "CCAvenue", "Mobikwik", "Freecharge", "PolicyBazaar",
            "BankBazaar", "Lendingkart"
        ],
        
        "Birla_Group_Companies": [
            "Aditya Birla Group", "Ultratech Cement", "Hindalco Industries",
            "Aditya Birla Fashion and Retail", "Aditya Birla Capital", "Birla Corporation",
            "Century Textiles"
        ],
        
        "Godrej_Group": [
            "Godrej & Boyce", "Godrej Properties", "Godrej Agrovet", "Godrej Industries"
        ],
        
        "Heritage_Companies": [
            "Kirloskar Group", "Thermax Limited", "Crompton Greaves",
            "Havells India", "Voltas Limited", "Blue Star Limited",
            "Whirlpool of India", "Videocon Industries"
        ],
        
        "E_commerce_Digital": [
            "Meesho", "CRED", "ShareChat", "InMobi", "Hike Messenger",
            "Ola Money", "Amazon India", "Flipkart Internet"
        ],
        
        "Renewable_Energy": [
            "Suzlon Energy", "Inox Wind", "ReNew Power", "Azure Power",
            "Hero Future Energies", "Greenko Group", "Acme Solar"
        ],
        
        "Food_Agriculture": [
            "ITC Foods Division", "Future Consumer", "Britannia Foods",
            "Nestle India Foods", "PepsiCo India", "Coca-Cola India", "Marico Foods"
        ],
        
        "Real_Estate_Housing": [
            "DLF Limited", "Godrej Properties", "Prestige Estates",
            "Brigade Enterprises", "Sobha Limited", "HDFC Bank Housing Finance",
            "LIC Housing Finance"
        ],
        
        "Regional_Business_Hubs": [
            "Bombay Stock Exchange", "National Stock Exchange"
        ]
    }

def main():
    companies_dict = get_comprehensive_indian_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"Total unique Indian companies across all categories: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    # Save to file
    with open('/Users/adi/code/socratify/socratify-yolo/comprehensive_indian_list.txt', 'w') as f:
        f.write("COMPREHENSIVE INDIAN COMPANIES - ALL TIERS\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Total unique companies: {len(unique_companies)}\n")
        f.write(f"Categories: {len(companies_dict)}\n\n")
        
        f.write("Covers all tiers:\n")
        f.write("- Top tier: Nifty 50 and major conglomerates\n")
        f.write("- Middle tier: Established players across sectors\n")
        f.write("- Bottom tier: Regional players and specialized companies\n")
        f.write("- Startups: Unicorns and high-growth companies\n")
        f.write("- Heritage: Old industrial houses\n\n")
        
        for i, company in enumerate(unique_companies, 1):
            f.write(f"{i:3d}. {company}\n")
    
    print(f"\nSaved to comprehensive_indian_list.txt")
    return unique_companies

if __name__ == "__main__":
    main()