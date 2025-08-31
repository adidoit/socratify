#!/usr/bin/env python3
"""
Chinese Companies Database
Comprehensive coverage: Tech giants, SOEs, unicorns, major sectors
"""

def get_chinese_companies():
    """Complete database of Chinese companies across all categories"""
    return {
        "Tech_Giants_BAT_Plus": [
            "ByteDance", "Tencent Holdings", "Alibaba Group", "Baidu", "Xiaomi",
            "Meituan", "Pinduoduo", "JD.com", "Didi Chuxing"
        ],
        
        "AI_Unicorns": [
            "Zhipu AI", "MiniMax", "Baichuan AI", "Moonshot", "StepFun", "01.AI",
            "SenseTime", "iFlytek", "DJI"
        ],
        
        "Big_Four_Banks": [
            "Industrial and Commercial Bank of China", "China Construction Bank",
            "Agricultural Bank of China", "Bank of China"
        ],
        
        "Major_SOEs": [
            "State Grid Corporation of China", "Sinopec Group", "China National Petroleum Corporation",
            "China Mobile", "China Telecom", "China Unicom"
        ],
        
        "Manufacturing_Auto": [
            "BYD", "Contemporary Amperex Technology", "Geely", "SAIC Motor", "Great Wall Motors"
        ],
        
        "Electronics_Semiconductors": [
            "Huawei", "Xiaomi", "BOE Technology", "SMIC", "Lenovo", "TCL Technology"
        ],
        
        "Heavy_Industry": [
            "China State Construction Engineering", "China Railway Group", "CRRC",
            "China Communications Construction"
        ],
        
        "Energy_Oil_Gas": [
            "China National Petroleum Corporation", "Sinopec", "China National Offshore Oil Corporation",
            "China National Nuclear Corporation", "China General Nuclear Power Group"
        ],
        
        "Financial_Services": [
            "Ant Group", "Tencent Financial", "Ping An Insurance", "China Life Insurance",
            "CITIC Group", "CITIC Securities", "China International Capital Corporation", "Haitong Securities"
        ],
        
        "Telecommunications": [
            "China Mobile", "China Telecom", "China Unicom", "Huawei"
        ],
        
        "Healthcare_Pharma": [
            "Sinopharm", "WuXi AppTec", "BGI Genomics", "WuXi Biologics"
        ],
        
        "Consumer_Ecommerce": [
            "Alibaba", "Pinduoduo", "JD.com", "Douyin", "Kweichow Moutai", "Wuliangye"
        ],
        
        "Sports_Apparel": [
            "Anta Sports", "Li-Ning", "Peak Sport", "361 Degrees"
        ],
        
        "Real_Estate": [
            "Evergrande", "Country Garden", "Vanke", "Poly Real Estate"
        ],
        
        "Transportation_Logistics": [
            "SF Holdings", "ZTO Express", "Didi Chuxing", "China Railway"
        ],
        
        "Food_Beverage": [
            "Yili Group", "China Mengniu Dairy", "Haidilao"
        ],
        
        "Major_Private": [
            "Huawei", "BYD", "Geely", "Xiaomi", "ByteDance", "Tencent", "Alibaba"
        ]
    }

def main():
    companies_dict = get_chinese_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"CHINESE COMPANIES DATABASE")
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