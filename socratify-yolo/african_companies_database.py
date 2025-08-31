#!/usr/bin/env python3
"""
African Companies Database
Comprehensive coverage: JSE, NSE, major exchanges, unicorns
"""

def get_african_companies():
    """Complete database of African companies across all categories"""
    return {
        "South_Africa_JSE_Top40": [
            "Anglo American", "BHP Billiton", "Glencore", "Sibanye-Stillwater", "Harmony Gold",
            "Impala Platinum", "Northam Platinum", "Kumba Iron Ore", "Standard Bank Group",
            "FirstRand", "Absa Group", "Nedbank Group", "Capitec Bank", "Old Mutual", "Sanlam",
            "Discovery", "MTN Group", "Vodacom Group", "Naspers", "Prosus", "Shoprite Holdings",
            "Woolworths Holdings", "Pick n Pay", "Massmart Holdings", "Bidvest Group",
            "Imperial Holdings", "Barloworld", "Growthpoint Properties", "Redefine Properties",
            "Life Healthcare", "Netcare", "Aspen Pharmacare"
        ],
        
        "Nigeria_NSE_Major": [
            "Zenith Bank", "Guaranty Trust Holding Co", "United Bank for Africa", "Access Bank",
            "First Bank of Nigeria", "Fidelity Bank", "Dangote Cement", "BUA Cement", "BUA Foods",
            "Seplat Energy", "Total Nigeria", "Oando", "Airtel Africa", "Nigerian Breweries",
            "Unilever Nigeria", "Nestlé Nigeria", "African Alliance Insurance"
        ],
        
        "Egypt_EGX_Major": [
            "Commercial International Bank", "QNB ALAHLI", "Arab African International Bank",
            "Talaat Moustafa Group", "Palm Hills Development", "SODIC", "Telecom Egypt",
            "Eastern Company", "Suez Cement", "Juhayna Food Industries"
        ],
        
        "Kenya_NSE_Major": [
            "Safaricom", "Equity Group", "KCB Group", "I&M Holdings", "Standard Chartered Kenya",
            "East African Breweries Limited", "British American Tobacco Kenya", "Bamburi Cement",
            "Kenya Airways", "Liberty Kenya Holdings"
        ],
        
        "Morocco_Casablanca": [
            "Attijariwafa Bank", "Banque Centrale Populaire", "BMCE Bank", "Maroc Telecom",
            "Managem Group", "OCP Group", "Addoha Group", "LafargeHolcim Morocco"
        ],
        
        "Ghana_GSE_Major": [
            "MTN Ghana", "AngloGold Ashanti", "Tullow Oil", "Gold Fields Ghana", "GCB Bank",
            "Ecobank Ghana", "CalBank", "Unilever Ghana", "Fan Milk", "Guinness Ghana Breweries"
        ],
        
        "African_Fintech_Unicorns": [
            "Flutterwave", "OPay", "Chipper Cash", "Wave", "Interswitch", "MNT-Halan", "Moniepoint"
        ],
        
        "African_Other_Unicorns": [
            "Andela", "Jumia", "TymeBank"
        ],
        
        "South_Africa_Mining": [
            "Anglo American", "BHP Billiton", "Glencore", "Sibanye-Stillwater", "Harmony Gold",
            "Impala Platinum", "Northam Platinum", "Kumba Iron Ore"
        ],
        
        "South_Africa_Banking": [
            "Standard Bank Group", "FirstRand", "Absa Group", "Nedbank Group", "Capitec Bank"
        ],
        
        "Nigeria_Banking_Oil": [
            "Zenith Bank", "Guaranty Trust Holding Co", "United Bank for Africa", "Access Bank",
            "First Bank of Nigeria", "Dangote Group", "BUA Group", "Seplat Energy"
        ],
        
        "Kenya_Telecom_Banking": [
            "Safaricom", "Equity Group", "KCB Group", "I&M Holdings"
        ],
        
        "Morocco_Banking_Mining": [
            "Attijariwafa Bank", "Banque Centrale Populaire", "BMCE Bank", "OCP Group"
        ],
        
        "African_Conglomerates": [
            "Dangote Group", "BUA Group", "Bidvest Group", "Imperial Holdings", "Naspers",
            "Prosus", "Talaat Moustafa Group", "OCP Group"
        ],
        
        "African_Telecommunications": [
            "MTN Group", "Vodacom Group", "Airtel Africa", "Safaricom", "Maroc Telecom",
            "Telecom Egypt", "MTN Ghana"
        ]
    }

def main():
    companies_dict = get_african_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"AFRICAN COMPANIES DATABASE")
    print(f"=" * 30)
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    return unique_companies

if __name__ == "__main__":
    main()