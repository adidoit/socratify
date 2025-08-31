#!/usr/bin/env python3
"""
Master Global Business Expansion Database
Combining ALL research from Task agents + Russian research
US + Japan + South Korea + Southeast Asia + Latin America + Australia/NZ + Russia
"""

def get_us_companies():
    """US Business Ecosystem - From Task Research"""
    return {
        "S&P_500_Major": [
            "Apple", "Microsoft", "Amazon", "Nvidia", "Alphabet", "Tesla", "Meta",
            "Taiwan Semiconductor", "Berkshire Hathaway", "Eli Lilly", "Broadcom",
            "JPMorgan Chase", "Visa", "UnitedHealth", "Exxon Mobil", "Mastercard",
            "Procter & Gamble", "Johnson & Johnson", "Home Depot", "Netflix",
            "Bank of America", "Chevron", "Pfizer", "AbbVie", "Salesforce",
            "Coca-Cola", "Merck", "Costco", "McDonald's", "Cisco Systems",
            "Oracle", "Walt Disney", "Thermo Fisher", "Wells Fargo", "Danaher",
            "Verizon", "Comcast", "Intel", "Nike", "Pepsico"
        ],
        
        "NASDAQ_100_Tech": [
            "Apple", "Microsoft", "Amazon", "Nvidia", "Meta", "Tesla", "Alphabet",
            "Netflix", "Adobe", "Salesforce", "PayPal", "Intuit", "Qualcomm",
            "Advanced Micro Devices", "Micron Technology", "Marvell Technology",
            "Applied Materials", "KLA Corporation", "Lam Research", "Synopsys",
            "Cadence Design", "Analog Devices", "Texas Instruments", "Broadcom",
            "ASML Holding", "Taiwan Semiconductor"
        ],
        
        "US_Unicorns_2024": [
            "SpaceX", "Stripe", "Epic Games", "Instacart", "Databricks", "Revolut",
            "Chime", "Checkout.com", "Canva", "Figma", "Discord", "Roblox",
            "Coinbase", "Robinhood", "SoFi", "Affirm", "Plaid", "Snowflake",
            "Palantir", "Airbnb", "DoorDash", "Uber", "Lyft", "WeWork",
            "23andMe", "Peloton", "Beyond Meat", "Impossible Foods"
        ],
        
        "Fortune_500_Energy": [
            "Exxon Mobil", "Chevron", "ConocoPhillips", "Marathon Petroleum",
            "Phillips 66", "Valero Energy", "Enterprise Products Partners",
            "Plains GP Holdings", "Kinder Morgan", "Energy Transfer"
        ],
        
        "Fortune_500_Healthcare": [
            "UnitedHealth Group", "Anthem", "Humana", "Centene Corporation",
            "Molina Healthcare", "Cardinal Health", "AmerisourceBergen",
            "McKesson Corporation", "CVS Health", "Walgreens Boots Alliance"
        ],
        
        "Major_Banks_Financial": [
            "JPMorgan Chase", "Bank of America", "Wells Fargo", "Citigroup",
            "Goldman Sachs", "Morgan Stanley", "American Express", "Capital One",
            "PNC Financial", "Truist Financial", "Charles Schwab", "Fidelity",
            "BlackRock", "Vanguard", "State Street", "Northern Trust"
        ]
    }

def get_japanese_companies():
    """Japanese Business Ecosystem - From Task Research"""
    return {
        "Nikkei_225_Major": [
            "Toyota Motor", "Sony Group", "Nintendo", "SoftBank Group", "Keyence",
            "ASML Holding", "Recruit Holdings", "Tokyo Electron", "Shin-Etsu Chemical",
            "KDDI", "NTT", "Japan Tobacco", "Murata Manufacturing", "Daikin Industries",
            "Shionogi", "TDK", "Hoya", "Advantest", "Fast Retailing", "Uniqlo",
            "Seven & i Holdings", "Rakuten Group", "Mercari", "MonotaRO",
            "Nintendo", "Capcom", "Square Enix", "Bandai Namco", "Konami"
        ],
        
        "Major_Conglomerates": [
            "Mitsubishi Corporation", "Mitsui & Co", "Itochu Corporation",
            "Sumitomo Corporation", "Marubeni Corporation", "Toyota Tsusho",
            "Sojitz Corporation", "Hitachi", "Panasonic", "Toshiba",
            "Fujitsu", "NEC Corporation", "Sharp Corporation"
        ],
        
        "Automotive_Giants": [
            "Toyota Motor", "Honda Motor", "Nissan Motor", "Suzuki Motor",
            "Mazda Motor", "Subaru Corporation", "Mitsubishi Motors",
            "Isuzu Motors", "Hino Motors", "UD Trucks"
        ],
        
        "Technology_Electronics": [
            "Sony Group", "Nintendo", "SoftBank", "Rakuten", "Yahoo Japan",
            "Mercari", "CyberAgent", "DeNA", "Gree", "Mixi", "Cookpad",
            "Freee", "Sansan", "SmartNews", "Preferred Networks"
        ],
        
        "Banking_Financial": [
            "Mitsubishi UFJ Financial", "Sumitomo Mitsui Financial", "Mizuho Financial",
            "Japan Post Bank", "Resona Holdings", "Shinsei Bank", "Aozora Bank",
            "Nomura Holdings", "Daiwa Securities", "SBI Holdings", "Monex Group"
        ]
    }

def get_south_korean_companies():
    """South Korean Business Ecosystem - From Task Research"""
    return {
        "KOSPI_Major": [
            "Samsung Electronics", "SK Hynix", "Samsung SDI", "LG Energy Solution",
            "NAVER Corporation", "Kakao", "Celltrion", "Samsung Biologics",
            "LG Electronics", "LG Chem", "POSCO", "Hyundai Motor", "Kia Corporation"
        ],
        
        "Chaebols_Samsung": [
            "Samsung Electronics", "Samsung SDI", "Samsung Biologics", "Samsung C&T",
            "Samsung Life Insurance", "Samsung Fire & Marine Insurance", "Samsung Heavy Industries"
        ],
        
        "Chaebols_LG": [
            "LG Electronics", "LG Chem", "LG Energy Solution", "LG Display",
            "LG Innotek", "LG Hausys", "LG Corp"
        ],
        
        "Chaebols_SK": [
            "SK Hynix", "SK Innovation", "SK Telecom", "SK Biopharmaceuticals",
            "SK Holdings", "SK Networks", "SK Gas"
        ],
        
        "Chaebols_Hyundai": [
            "Hyundai Motor", "Kia Corporation", "Hyundai Mobis", "Hyundai Steel",
            "Hyundai Heavy Industries", "Hyundai Engineering & Construction"
        ],
        
        "K_Pop_Gaming_Entertainment": [
            "HYBE Corporation", "SM Entertainment", "YG Entertainment", "JYP Entertainment",
            "Netmarble", "NCsoft", "Nexon", "Kakao Games", "Pearl Abyss", "Krafton"
        ],
        
        "Technology_Internet": [
            "NAVER Corporation", "Kakao", "Kakao Bank", "Coupang", "Woowa Brothers",
            "Viva Republica", "Toss", "Yanolja", "Market Kurly", "Sendbird"
        ]
    }

def get_southeast_asian_companies():
    """Southeast Asian Business Ecosystem - From Task Research"""
    return {
        "Singapore_STI": [
            "DBS Group", "OCBC Bank", "United Overseas Bank", "Singapore Airlines",
            "Singapore Technologies Engineering", "Keppel Corporation", "Sembcorp Industries",
            "CapitaLand", "City Developments", "Wilmar International", "Golden Agri-Resources",
            "Olam Group", "Jardine Matheson", "Jardine Cycle & Carriage", "Dairy Farm International"
        ],
        
        "Singapore_Unicorns": [
            "Grab", "Sea Limited", "Razer", "Trax", "PatSnap", "Ninja Van", "Carousell"
        ],
        
        "Indonesia_IDX": [
            "Bank Central Asia", "Bank Rakyat Indonesia", "Bank Mandiri", "Bank Negara Indonesia",
            "Telkom Indonesia", "Astra International", "Unilever Indonesia", "Indofood Sukses Makmur",
            "Gudang Garam", "Sampoerna", "Indocement Tunggal Prakarsa", "United Tractors"
        ],
        
        "Indonesia_Unicorns": [
            "GoTo Group", "Traveloka", "Ovo", "Tokopedia", "Bukalapak", "Blibli"
        ],
        
        "Thailand_SET": [
            "PTT", "CP Group", "Siam Cement Group", "Bangkok Bank", "Kasikornbank",
            "Krung Thai Bank", "Advanced Info Service", "True Corporation", "CP Foods",
            "Central Pattana", "Central Retail Corporation"
        ],
        
        "Malaysia_KLCI": [
            "Maybank", "Public Bank", "CIMB Group", "Genting", "Axiata Group",
            "IHH Healthcare", "Sime Darby Plantation", "Kuala Lumpur Kepong",
            "IOI Corporation", "Top Glove"
        ],
        
        "Philippines_PSEi": [
            "SM Investments", "Ayala Corporation", "BDO Unibank", "Bank of the Philippine Islands",
            "Jollibee Foods Corporation", "Globe Telecom", "PLDT", "Aboitiz Equity Ventures",
            "San Miguel Corporation", "Metropolitan Bank"
        ],
        
        "Vietnam_VN30": [
            "Vinhomes", "VinGroup", "Vinamilk", "Hoa Phat Group", "FPT Corporation",
            "Mobile World Group", "Masan Group", "Vincom Retail", "Techcombank"
        ]
    }

def get_latin_american_companies():
    """Latin American Business Ecosystem - From Task Research"""
    return {
        "Brazil_Bovespa": [
            "Vale", "Petrobras", "Itau Unibanco", "Banco Bradesco", "Ambev",
            "Magazine Luiza", "JBS", "Banco do Brasil", "Santander Brasil", "B3",
            "Localiza", "Suzano", "WEG", "Natura", "Embraer", "Gerdau", "CSN"
        ],
        
        "Brazil_Unicorns": [
            "Nubank", "iFood", "Stone", "Rappi", "Loggi", "Gympass", "QuintoAndar",
            "99", "Mercado Bitcoin", "Creditas", "Loft", "Ebanx", "PagSeguro"
        ],
        
        "Mexico_BMV": [
            "America Movil", "Grupo Televisa", "Walmart Mexico", "Fomento Economico Mexicano",
            "Grupo Mexico", "Cemex", "Alfa", "Grupo Bimbo", "Banorte", "Grupo Financiero Inbursa",
            "Arca Continental", "Grupo Aeroportuario del Pacifico", "Kimberly-Clark de Mexico"
        ],
        
        "Argentina_MERVAL": [
            "Mercado Libre", "YPF", "Banco Macro", "Telecom Argentina", "Grupo Financiero Galicia",
            "Pampa Energia", "Central Puerto", "Aluar", "Ternium Argentina"
        ],
        
        "Chile_IPSA": [
            "Enel Chile", "Banco de Chile", "Banco Santander Chile", "Copec",
            "SQM", "Falabella", "Cencosud", "LATAM Airlines", "BancoEstado", "Colbun"
        ],
        
        "Colombia_COLCAP": [
            "Ecopetrol", "Bancolombia", "Grupo Aval", "ISA", "Nutresa", "EPM",
            "Avianca", "Almacenes Exito", "Cemex Colombia", "Bavaria"
        ],
        
        "Peru_S&P_Lima": [
            "Southern Copper Corporation", "Credicorp", "Volcan Compania Minera",
            "Ferreycorp", "Alicorp", "Intercorp Financial Services", "InRetail Peru"
        ]
    }

def get_australian_nz_companies():
    """Australian/NZ Business Ecosystem - From Task Research"""
    return {
        "ASX_200_Major": [
            "BHP Group", "Commonwealth Bank", "CSL Limited", "Westpac Banking Corporation",
            "Australia and New Zealand Banking Group", "National Australia Bank",
            "Woolworths Group", "Telstra Corporation", "Rio Tinto", "Macquarie Group",
            "Fortescue Metals", "Wesfarmers", "Goodman Group", "Transurban Group",
            "Aristocrat Leisure", "ResMed", "Cochlear", "James Hardie", "Brambles"
        ],
        
        "Australian_Unicorns": [
            "Canva", "Atlassian", "SafetyCulture", "Afterpay", "Culture Amp", "Deputy"
        ],
        
        "New_Zealand_NZX": [
            "Fisher & Paykel Healthcare", "Spark New Zealand", "a2 Milk Company",
            "Auckland International Airport", "Meridian Energy", "Contact Energy",
            "Fletcher Building", "Mainfreight", "The Warehouse Group", "Ryman Healthcare"
        ],
        
        "Mining_Resources": [
            "BHP Group", "Rio Tinto", "Fortescue Metals Group", "Newcrest Mining",
            "Northern Star Resources", "Evolution Mining", "South32", "Santos"
        ],
        
        "Banking_Financial": [
            "Commonwealth Bank", "Westpac Banking Corporation", "Australia and New Zealand Banking Group",
            "National Australia Bank", "Macquarie Group", "Suncorp Group", "Bank of Queensland"
        ],
        
        "Technology_Software": [
            "Atlassian", "Canva", "Xero", "WiseTech Global", "Technology One", "Pro Medicus",
            "Altium", "Appen", "Nuix", "Life360"
        ]
    }

def get_russian_companies():
    """Russian Business Ecosystem - From Task Research"""
    return {
        "MOEX_Blue_Chip": [
            "Sberbank", "Gazprom", "Rosneft", "Lukoil", "Novatek", "VTB Bank",
            "Norilsk Nickel", "Yandex", "NLMK", "MMK", "Severstal", "Alrosa",
            "Magnit", "MTS", "Sistema"
        ],
        
        "Energy_Oil_Gas": [
            "Gazprom", "Rosneft", "Lukoil", "Novatek", "Transneft", "Gazprom Neft", "Tatneft"
        ],
        
        "Mining_Metals": [
            "Norilsk Nickel", "Alrosa", "Severstal", "NLMK", "MMK", "Evraz",
            "Metalloinvest", "Mechel", "Polyus"
        ],
        
        "Banking_Financial": [
            "Sberbank", "VTB Bank", "Gazprombank", "Alfa-Bank", "Tinkoff Bank",
            "Rosselkhozbank", "Promsvyazbank", "Bank Rossiya"
        ],
        
        "Technology_Internet": [
            "Yandex", "VK", "Kaspersky Lab", "ABBYY", "JetBrains", "Ozon"
        ],
        
        "Telecommunications": [
            "MTS", "MegaFon", "Rostelecom", "VimpelCom", "Tele2 Russia"
        ],
        
        "Automotive_Manufacturing": [
            "AvtoVAZ", "GAZ Group", "UAZ", "KAMAZ", "Sollers JSC"
        ],
        
        "Retail_Consumer": [
            "X5 Retail Group", "Magnit", "Lenta", "Baltika Breweries", "Wimm-Bill-Dann"
        ],
        
        "Transportation_Airlines": [
            "Aeroflot", "S7 Airlines", "Pobeda", "Ural Airlines", "UTair",
            "Russian Railways"
        ]
    }

def get_master_global_expansion():
    """Master combined database of ALL regional expansions"""
    return {
        "United States": get_us_companies(),
        "Japan": get_japanese_companies(),
        "South Korea": get_south_korean_companies(),
        "Southeast Asia": get_southeast_asian_companies(),
        "Latin America": get_latin_american_companies(),
        "Australia/New Zealand": get_australian_nz_companies(),
        "Russia": get_russian_companies()
    }

def main():
    master_db = get_master_global_expansion()
    
    total_companies = 0
    for region, categories in master_db.items():
        region_count = 0
        for category, companies in categories.items():
            region_count += len(companies)
        total_companies += region_count
        print(f"{region}: {region_count} companies")
    
    print(f"\nTotal companies in master expansion database: {total_companies}")
    print(f"Regions covered: {len(master_db)}")
    
    # Flatten all unique companies
    all_companies = set()
    for region, categories in master_db.items():
        for category, companies in categories.items():
            all_companies.update(companies)
    
    print(f"Unique companies (deduplicated): {len(all_companies)}")
    
    # Save comprehensive list
    with open('/Users/adi/code/socratify/socratify-yolo/master_expansion_companies_list.txt', 'w') as f:
        f.write("MASTER GLOBAL BUSINESS EXPANSION DATABASE\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total unique companies: {len(all_companies)}\n")
        f.write(f"Regions: {len(master_db)}\n\n")
        
        for region, categories in master_db.items():
            f.write(f"\n### {region.upper()} ###\n")
            for category, companies in categories.items():
                f.write(f"\n{category}:\n")
                for company in companies:
                    f.write(f"  - {company}\n")
        
        f.write(f"\n\n### ALPHABETICAL MASTER LIST ###\n")
        for i, company in enumerate(sorted(all_companies), 1):
            f.write(f"{i:4d}. {company}\n")
    
    print("Saved to master_expansion_companies_list.txt")
    return master_db

if __name__ == "__main__":
    main()