#!/usr/bin/env python3
"""
UK Companies Database
Comprehensive coverage: FTSE 100/250, unicorns, private companies, sectors
"""

def get_uk_companies():
    """Complete database of UK companies across all categories"""
    return {
        "FTSE_100_Major": [
            "AstraZeneca", "Shell", "HSBC Holdings", "Unilever", "British American Tobacco",
            "BP", "Rio Tinto Group", "RELX", "GSK", "Vodafone Group", "Prudential",
            "Legal & General", "Admiral Group", "Sage Group", "Auto Trader Group",
            "Rolls-Royce Holdings", "BAE Systems", "Next", "Marks & Spencer", "ASOS",
            "JD Sports", "Tesco", "Sainsbury's", "BT Group", "ITV"
        ],
        
        "FTSE_250_Notable": [
            "Carnival Corporation", "Endeavour Mining", "Babcock International Group",
            "Games Workshop Group", "LondonMetric Property", "Hiscox", "IG Group Holdings",
            "Oxford Nanopore Technologies", "Jet2", "Fevertree", "Mortgage Advice Bureau",
            "SigmaRoc", "ITM Power", "Renalytix"
        ],
        
        "UK_Unicorns_Fintech": [
            "Revolut", "Monzo", "Starling Bank", "Zopa", "OakNorth Bank", "SumUp",
            "Rapyd", "1Password", "Wise"
        ],
        
        "UK_Unicorns_Other": [
            "Deliveroo", "Lighthouse", "Mews", "Wayve", "ElevenLabs", "Unitary"
        ],
        
        "Banking_Financial": [
            "HSBC", "Barclays", "Lloyds Banking Group", "NatWest Group", "Standard Chartered",
            "Revolut", "Monzo", "Starling Bank", "Chase UK", "Prudential", "Legal & General",
            "Admiral Group", "Hiscox"
        ],
        
        "Technology_Software": [
            "Sage Group", "Auto Trader Group", "AVEVA Group", "DeepMind", "ElevenLabs",
            "Unitary", "Games Workshop", "Wayve", "Oxford Nanopore Technologies"
        ],
        
        "Healthcare_Pharma": [
            "AstraZeneca", "GSK", "Oxford Nanopore Technologies", "Bicycle Therapeutics",
            "Amgen UK", "Microbiotica", "Artios Pharma", "Storm Therapeutics", "Mogrify"
        ],
        
        "Energy_Companies": [
            "Shell", "BP", "SSE", "National Grid", "Centrica"
        ],
        
        "Retail_Ecommerce": [
            "Tesco", "Sainsbury's", "ASDA", "Morrisons", "Next", "Marks & Spencer",
            "ASOS", "JD Sports", "Boohoo Group", "The Hut Group"
        ],
        
        "Manufacturing_Industrial": [
            "BAE Systems", "Rolls-Royce Holdings", "Babcock International", "Rio Tinto",
            "Anglo American", "Glencore", "Barratt Developments", "Taylor Wimpey", "Persimmon"
        ],
        
        "Real_Estate_Property": [
            "SEGRO", "Land Securities", "British Land", "Derwent London"
        ],
        
        "Media_Telecommunications": [
            "BT Group", "Vodafone UK", "VodafoneThree", "ITV", "Sky UK", "BBC"
        ],
        
        "Government_Public": [
            "Network Rail", "UK Government Investments", "Channel 4", "BBC"
        ]
    }

def main():
    companies_dict = get_uk_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"UK COMPANIES DATABASE")
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