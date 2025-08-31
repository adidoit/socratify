#!/usr/bin/env python3
"""
Middle East Companies Database  
Comprehensive coverage: GCC, Israel, Turkey, major exchanges
"""

def get_middle_east_companies():
    """Complete database of Middle East companies across all categories"""
    return {
        "Saudi_Arabia_Tadawul": [
            "Saudi Aramco", "SABIC", "Al Rajhi Bank", "Saudi Telecom Company", "Ma'aden",
            "Dr. Sulaiman Al Habib Medical", "Riyad Bank", "Saudi Electricity Company",
            "Almarai Company", "Saudi Basic Industries Corporation"
        ],
        
        "UAE_ADX_DFM": [
            "ADNOC", "First Abu Dhabi Bank", "Emaar Properties", "Emirates Airlines",
            "Etisalat", "Talabat", "Lulu Retail", "Air Arabia", "Salik"
        ],
        
        "Qatar_QSE": [
            "Qatar National Bank", "Industries Qatar", "Qatar Islamic Bank", "Ooredoo",
            "Qatar Insurance Company", "Nakilat", "QatarEnergy", "Qatar Airways"
        ],
        
        "Kuwait_Boursa": [
            "Kuwait Finance House", "National Bank of Kuwait", "Boubyan Bank",
            "Zain", "Agility Public Warehousing", "Kuwait Oil Company"
        ],
        
        "Bahrain_Bourse": [
            "Gulf International Bank", "Arab Banking Corporation", "Ahli United Bank"
        ],
        
        "Oman_MSM": [
            "Bank Muscat", "OQ Gas Networks", "OQ Base Industries", "Omantel",
            "Renaissance Services", "Ominvest"
        ],
        
        "Israel_TASE": [
            "Teva Pharmaceutical", "Bank Hapoalim", "Bank Leumi", "Check Point Software",
            "Monday.com", "CyberArk Software", "Wix.com"
        ],
        
        "Turkey_BIST": [
            "Turkish Airlines", "Tüpraş", "BIM", "Akbank", "Koç Holding", "Sabancı Holding",
            "Turkcell", "İşbank", "Garanti BBVA"
        ],
        
        "Saudi_Conglomerates": [
            "Olayan Group", "Almarai Company", "Saudi Aramco", "SABIC"
        ],
        
        "UAE_Conglomerates": [
            "Al-Futtaim Group", "Majid Al Futtaim Group", "ADNOC", "Emirates Airlines"
        ],
        
        "Oil_Gas_Giants": [
            "Saudi Aramco", "ADNOC", "QatarEnergy", "OQ Group", "Kuwait Oil Company"
        ],
        
        "Banking_Financial": [
            "Qatar National Bank", "National Bank of Kuwait", "First Abu Dhabi Bank",
            "Al Rajhi Bank", "Bank Hapoalim", "Bank Leumi", "Akbank", "Garanti BBVA"
        ],
        
        "Technology_Companies": [
            "Check Point Software", "Monday.com", "CyberArk Software", "Wix.com",
            "Saudi Telecom Company", "Etisalat", "Ooredoo", "Turkcell"
        ],
        
        "Aviation_Logistics": [
            "Emirates Airlines", "Qatar Airways", "Turkish Airlines", "Air Arabia",
            "Agility Public Warehousing"
        ],
        
        "Real_Estate_Construction": [
            "Emaar Properties", "Majid Al Futtaim", "Talaat Moustafa Group"
        ],
        
        "Regional_Unicorns": [
            "Careem", "Kitopi", "Swvl", "Tabby", "TruKKer", "Okadoc"
        ],
        
        "Sovereign_Fund_Companies": [
            "NEOM", "Almosafer", "FOODICS", "Tamara", "Tabby", "TruKKer", "Okadoc"
        ]
    }

def main():
    companies_dict = get_middle_east_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"MIDDLE EAST COMPANIES DATABASE")
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