#!/usr/bin/env python3
"""
Canadian Companies Database
Comprehensive coverage: TSX 60, unicorns, crown corporations, sectors
"""

def get_canadian_companies():
    """Complete database of Canadian companies across all categories"""
    return {
        "TSX_60_Major": [
            "Enbridge", "Brookfield Corporation", "Bank of Montreal", "Thomson Reuters Corporation",
            "Bank of Nova Scotia", "Alimentation Couche-Tard", "Manulife Financial Corporation",
            "TC Energy Corporation", "Suncor Energy", "Waste Connections", "Sun Life Financial",
            "Intact Financial Corporation", "National Bank of Canada", "Restaurant Brands International",
            "Barrick Gold Corporation", "Canadian Natural Resources", "Cenovus Energy",
            "Imperial Oil", "Pembina Corporation", "Parkland Corporation"
        ],
        
        "Big_Six_Banks": [
            "Royal Bank of Canada", "Toronto-Dominion Bank", "Bank of Nova Scotia",
            "Bank of Montreal", "Canadian Imperial Bank of Commerce", "National Bank of Canada"
        ],
        
        "Insurance_Major": [
            "Manulife Financial", "Sun Life Financial", "Intact Financial", "Great-West Lifeco"
        ],
        
        "Fintech_Digital": [
            "Wealthsimple", "KOHO Financial", "Baseline", "Quickly"
        ],
        
        "Oil_Energy": [
            "Canadian Natural Resources", "Suncor Energy", "Cenovus Energy", "Imperial Oil",
            "TC Energy", "Enbridge", "Pembina Corporation", "Parkland Corporation"
        ],
        
        "Mining_Resources": [
            "Nutrien", "Agnico Eagle Mines", "Barrick Gold", "Newmont Corporation",
            "Teck Resources", "First Quantum Minerals", "West Fraser Timber Co",
            "Canfor Corporation", "Resolute Forest Products"
        ],
        
        "Technology_Companies": [
            "Shopify", "Cohere", "Element AI", "Waabi", "Deep Genomics", "integrate.ai",
            "Hopper", "Clio", "BlackBerry", "Open Text Corporation", "Constellation Software"
        ],
        
        "Telecommunications": [
            "Rogers Communications", "Bell Canada", "Telus Corporation", "SaskTel", "Videotron"
        ],
        
        "Healthcare_Pharma": [
            "Shoppers Drug Mart", "Wellwise by Shoppers", "Apotex", "Bausch Health Companies", "Tilray"
        ],
        
        "Media_Entertainment": [
            "Bell Media", "Corus Entertainment", "Rogers Media", "Canadian Broadcasting Corporation",
            "DHX Media", "Lionsgate Entertainment"
        ],
        
        "Manufacturing_Industrial": [
            "Bombardier", "Magna International", "Celestica", "BRP"
        ],
        
        "Agriculture_Food": [
            "Maple Leaf Foods", "McCain Foods", "Saputo", "Alimentation Couche-Tard", "Nutrien"
        ],
        
        "Real_Estate": [
            "Brookfield Asset Management", "Canadian Apartment Properties REIT",
            "RioCan REIT", "First Capital REIT"
        ],
        
        "Transportation_Logistics": [
            "Canadian National Railway", "Canadian Pacific Kansas City", "Air Canada",
            "WestJet", "Purolator", "Canada Post"
        ],
        
        "Crown_Corporations": [
            "Canada Post Corporation", "Canadian Broadcasting Corporation", "VIA Rail Canada",
            "Bank of Canada", "Export Development Canada", "Hydro-Québec", "Ontario Power Generation",
            "BC Hydro", "SaskPower", "Manitoba Hydro", "LCBO", "SAQ", "ICBC"
        ],
        
        "Canadian_Unicorns": [
            "The Sandbox", "Shopify", "Cohere", "Dapper Labs", "1Password", "Hopper",
            "Wealthsimple", "Clio", "Lightspeed", "Nuvei"
        ]
    }

def main():
    companies_dict = get_canadian_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"CANADIAN COMPANIES DATABASE")
    print(f"=" * 35)
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    return unique_companies

if __name__ == "__main__":
    main()