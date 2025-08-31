#!/usr/bin/env python3
"""
European Union Companies Database
Comprehensive coverage: DAX, CAC, AEX, FTSE MIB, IBEX, Nordic, unicorns
"""

def get_eu_companies():
    """Complete database of EU companies across all categories"""
    return {
        "Germany_DAX_40": [
            "SAP", "Linde", "Siemens", "Volkswagen", "Allianz", "Mercedes-Benz Group",
            "Deutsche Telekom", "BMW", "Porsche", "BASF", "Bayer", "Deutsche Bank",
            "Munich Re", "Adidas"
        ],
        
        "France_CAC_40": [
            "LVMH", "Hermès International", "L'Oréal", "Schneider Electric", "TotalEnergies",
            "Sanofi", "BNP Paribas", "Airbus", "Dassault Systèmes", "Renault", "Orange",
            "Société Générale", "Bureau Veritas"
        ],
        
        "Netherlands_AEX_25": [
            "Shell", "ASML Holding", "Unilever", "ArcelorMittal", "Ahold Delhaize",
            "Heineken", "Philips", "ING Group", "Just Eat Takeaway"
        ],
        
        "Italy_FTSE_MIB": [
            "Ferrari", "Prada", "UniCredit", "Intesa Sanpaolo", "Eni", "Enel",
            "Stellantis", "Moncler", "Salvatore Ferragamo"
        ],
        
        "Spain_IBEX_35": [
            "Inditex", "Iberdrola", "Banco Santander", "BBVA", "CaixaBank", "Aena",
            "Telefónica", "Repsol", "Cellnex Telecom"
        ],
        
        "Nordic_Major": [
            "Ericsson", "Volvo Group", "H&M", "Atlas Copco", "Investor AB", "Nokia Corporation",
            "Nordea Bank", "Kone Corporation", "Sampo Group", "UPM-Kymmene", "Novo Nordisk",
            "Maersk", "Carlsberg", "Danske Bank"
        ],
        
        "Switzerland_SMI": [
            "Nestlé", "Roche Holding", "Novartis", "UBS Group", "ABB", "Zurich Insurance Group",
            "Richemont", "Swiss Re", "Lonza Group", "Holcim", "Alcon"
        ],
        
        "EU_Unicorns_2024": [
            "DataSnipper", "Mews", "Bending Spoons", "Pennylane", "Pigment", "N26",
            "Celonis", "Trade Republic", "Northvolt", "Klarna", "Bolt"
        ],
        
        "Germany_Tech_Industrial": [
            "SAP", "Siemens", "BASF", "Bayer", "BMW", "Mercedes-Benz", "Volkswagen",
            "Porsche", "Continental", "ThyssenKrupp", "Bosch", "Infineon Technologies"
        ],
        
        "France_Luxury_Energy": [
            "LVMH", "Hermès", "Kering", "Chanel", "L'Oréal", "TotalEnergies", "Airbus",
            "Safran", "Danone", "Michelin", "Peugeot", "Carrefour"
        ],
        
        "Netherlands_Tech_Consumer": [
            "ASML Holding", "Philips", "Shell", "Unilever", "Heineken", "Royal Vopak"
        ],
        
        "Nordic_Telecom_Fintech": [
            "Ericsson", "Nokia", "Telenor", "Ørsted", "Vestas", "Northvolt", "Klarna", "Lunar"
        ],
        
        "Italy_Fashion_Auto": [
            "Ferrari", "Prada", "Salvatore Ferragamo", "Moncler", "Brunello Cucinelli",
            "Stellantis", "Ferrero Group", "Benetton Group"
        ],
        
        "Spain_Banking_Energy": [
            "Banco Santander", "BBVA", "CaixaBank", "Iberdrola", "Repsol", "Telefónica"
        ],
        
        "EU_Family_Private": [
            "Robert Bosch", "Aldi", "Lidl", "Schwarz Group", "C&A", "Michelin",
            "Ferrero Group", "Benetton Group", "Heineken"
        ]
    }

def main():
    companies_dict = get_eu_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"EU COMPANIES DATABASE")
    print(f"=" * 25)
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    return unique_companies

if __name__ == "__main__":
    main()