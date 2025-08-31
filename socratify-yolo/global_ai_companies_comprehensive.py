#!/usr/bin/env python3
"""
Comprehensive Global AI Companies Database
Chinese, European, Indian, Japanese AI companies that people want to work for
"""

def get_global_ai_companies():
    """Comprehensive global AI companies by region"""
    return {
        # Chinese AI Companies - MASSIVE ecosystem
        "Chinese_AI": [
            # Big Tech AI Divisions
            "Baidu AI", "Alibaba DAMO Academy", "Tencent AI Lab", "ByteDance AI Lab",
            "JD AI", "Meituan AI", "DiDi AI", "Xiaomi AI", "Huawei AI", "OPPO AI",
            
            # AI Unicorns & Major Startups
            "SenseTime", "Megvii", "CloudWalk", "Yitu Technology", "Hikvision AI",
            "iFlytek", "Fourth Paradigm", "Cambricon Technologies", "Horizon Robotics",
            "Momenta", "Pony.ai", "WeRide", "AutoX", "PLUS AI", "TuSimple",
            
            # Foundation Models & LLMs
            "Zhipu AI", "MiniMax", "Baichuan AI", "Moonshot AI", "01.AI", "StepFun",
            "DeepSeek", "ChatGLM", "Ernie Bot", "Tongyi Qianwen", "SparkDesk",
            
            # Computer Vision & Robotics
            "DJI", "UBtech Robotics", "Agility Robotics China", "Dorabot", "CloudMinds",
            "UBTECH", "Siasun Robot", "KUKA China", "ABB China", "Fanuc China",
            
            # Healthcare AI
            "Ping An Good Doctor", "WeDoctor", "iCarbonX", "BGI Genomics AI",
            "Tencent Miying", "Alibaba Health AI", "JD Health AI",
            
            # Fintech AI
            "Ant Group AI", "JD Digits", "Tencent FinTech", "Lufax AI", "360 DigiTech",
            
            # Autonomous Driving
            "Baidu Apollo", "Pony.ai", "WeRide", "AutoX", "Momenta", "DeepRoute",
            "HAOMO.AI", "Hesai Technology", "RoboSense", "Innovusion"
        ],
        
        # European AI Companies - Strong ecosystem
        "European_AI": [
            # UK AI Companies
            "DeepMind", "Graphcore", "Prowler.io", "Onfido", "Speechmatics", "Swiftkey",
            "Magic Pony Technology", "VocalIQ", "Dark Blue Labs", "Vision Factory",
            "Faculty", "ASI Data Science", "Satalia", "Eigen Technologies", "Peak AI",
            
            # French AI Companies  
            "Mistral AI", "Hugging Face", "Dataiku", "Snips", "Shift Technology",
            "Meero", "ContentSquare", "CityzenData", "Prophesee", "Sigfox",
            
            # German AI Companies
            "Celonis", "DeepL", "Arago", "Merantix", "Twenty Billion Neurons",
            "Fraunhofer", "German Research Center for AI", "SAP AI", "Siemens AI",
            
            # Nordic AI Companies
            "Fingerprint Cards", "Tobii", "Recorded Future", "Clavister", "Mapillary",
            "Vionlabs", "Peltarion", "Varjo", "Silo AI", "Speechly",
            
            # Dutch AI Companies
            "Adyen AI", "Booking.com AI", "Philips AI", "Shell AI", "ING AI",
            "TomTom AI", "Exact AI", "ASML AI Research",
            
            # Swiss AI Companies
            "CEVA", "Logitech AI", "ABB Research", "Roche AI", "Novartis AI",
            
            # Italian AI Companies
            "Expert System", "Indigo AI", "CyberEthics Lab", "Vedrai",
            
            # Spanish AI Companies
            "BigML", "Sherpa.ai", "Clarity AI", "Satellogic AI"
        ],
        
        # Indian AI Companies - Booming ecosystem  
        "Indian_AI": [
            # Major Indian AI Companies
            "Freshworks AI", "Zoho AI", "InMobi AI", "ShareChat AI", "Dream11 AI",
            "Byju's AI", "Unacademy AI", "Vedantu AI", "WhiteHat Jr AI",
            
            # AI Startups & Unicorns
            "Mad Street Den", "Avaamo", "SigTuple", "Artivatic", "Predible Health",
            "Niramai", "Qure.ai", "Tricog", "PathAI India", "CancerAI",
            
            # Computer Vision & Robotics
            "Tonbo Imaging", "CronJ", "Flutura", "Detect Technologies", "Intello Labs",
            "Haber", "Botsync", "GreyOrange", "Systemantics", "Addverb Technologies",
            
            # Conversational AI
            "Haptik", "Yellow.ai", "Gupshup", "Rasa", "Verloop", "Reverie Language",
            
            # Fintech AI
            "Razorpay AI", "Paytm AI", "PhonePe AI", "Pine Labs AI", "Lendingkart AI",
            "ZestMoney AI", "Capital Float AI", "EarlySalary AI",
            
            # Enterprise AI
            "Manthan", "Crayon Data", "Fractal Analytics", "LatentView Analytics",
            "Mu Sigma", "Sigmoid Analytics", "Tiger Analytics", "Quantiphi"
        ],
        
        # Japanese AI Companies - Strong tech heritage
        "Japanese_AI": [
            # Major Japanese AI Companies
            "SoftBank AI", "Rakuten AI", "NTT AI", "KDDI AI", "LINE AI", "Mercari AI",
            "Sony AI", "Toyota AI", "Honda AI", "Nissan AI", "Panasonic AI",
            
            # AI Startups & Research Labs
            "Preferred Networks", "LeapMind", "ABEJA", "Brain Pad", "PKSHA Technology",
            "Morpho", "Hacarus", "Cogent Labs", "DataRobot Japan", "Fixstars",
            
            # Robotics & Hardware AI
            "FANUC AI", "Yaskawa AI", "Kawasaki Robotics AI", "Omron AI", "Keyence AI",
            "THK AI", "Nachi-Fujikoshi AI", "Denso AI", "Aisin AI",
            
            # Gaming & Entertainment AI
            "Nintendo AI", "Bandai Namco AI", "Square Enix AI", "Capcom AI", "Konami AI",
            "Cygames", "DeNA AI", "Gree AI", "Mixi AI", "CyberAgent AI",
            
            # Healthcare AI
            "Olympus AI", "Terumo AI", "Sysmex AI", "Shimadzu AI", "Fujifilm AI",
            
            # Automotive AI
            "Toyota Research Institute", "Honda R&D", "Nissan AI Research", "Mazda AI",
            "Subaru AI", "Mitsubishi Motors AI", "Suzuki AI",
            
            # Financial AI
            "Nomura AI", "Mizuho AI", "MUFG AI", "Sumitomo Mitsui AI", "Japan Post AI"
        ],
        
        # Israeli AI Companies - Punch above their weight
        "Israeli_AI": [
            # Major Israeli AI Companies
            "Mobileye", "OrCam", "Cortica", "Vayyar", "AImotive", "Innoviz", "Brightway Vision",
            "Hailo", "Deep Instinct", "Cybereason AI", "SentinelOne AI", "Armis AI",
            "Snyk AI", "Claroty AI", "Aqua Security AI", "Check Point AI",
            
            # Computer Vision & Autonomous
            "Mobileye", "Innoviz Technologies", "AImotive", "Brightway Vision", "Phantom Auto",
            "Cognata", "Foretellix", "Replay Technologies", "Trax", "Nexar",
            
            # Enterprise AI
            "monday.com AI", "Wix AI", "JFrog AI", "Fiverr AI", "IronSource AI",
            
            # Healthcare AI  
            "Zebra Medical Vision", "Aidoc", "MedyMatch", "Diagnostic Robotics", "Sheba Medical AI"
        ],
        
        # South Korean AI Companies - Strong in tech
        "South_Korean_AI": [
            # Major Korean AI Companies
            "Samsung AI", "LG AI Research", "SK Telecom AI", "KT AI", "Kakao AI",
            "Naver AI", "LINE AI", "Coupang AI", "Krafton AI", "NCSoft AI",
            
            # AI Startups
            "Scatter Lab", "TUNiB", "Upstage", "Wrtn Technologies", "Allganize",
            "MoneyBrain", "Clova", "AiTEMS", "DeepBrain AI", "Lunit",
            
            # Robotics & Hardware
            "Hyundai Robotics AI", "Doosan Robotics AI", "Rainbow Robotics",
            "Neuromeka", "RB Thayer", "Robotis"
        ],
        
        # Canadian AI Companies - Strong ecosystem
        "Canadian_AI": [
            # Major Canadian AI Companies
            "Element AI", "Maluuba", "Layer 6 AI", "Deep Genomics", "Integrate.ai",
            "Paymi AI", "Wealthsimple AI", "Shopify AI", "Cohere", "Vector Institute",
            
            # Research & Academic
            "Mila Quebec", "Vector Institute", "CIFAR", "Alberta Machine Intelligence Institute",
            
            # Startups
            "Ada Support", "Dessa", "Nanoleaf AI", "BlueDot", "Waabi"
        ],
        
        # Australian AI Companies
        "Australian_AI": [
            # Major Australian AI Companies
            "Canva AI", "Atlassian AI", "Xero AI", "SafetyCulture AI", "Deputy AI",
            "Culture Amp AI", "Campaign Monitor AI", "99designs AI",
            
            # AI Startups
            "Flamingo AI", "Hyper Anna", "Maxwell Plus", "Autopilot", "Einstein AI"
        ],
        
        # Scandinavian AI Companies
        "Scandinavian_AI": [
            # Swedish AI
            "Spotify AI", "Klarna AI", "King AI", "Mojang AI", "Ericsson AI",
            "H&M AI", "IKEA AI", "Volvo AI", "Scania AI", "ABB AI",
            
            # Norwegian AI
            "Opera AI", "DNB AI", "Telenor AI", "StatoilHydro AI",
            
            # Danish AI  
            "Novo Nordisk AI", "Maersk AI", "Vestas AI", "Orsted AI",
            
            # Finnish AI
            "Nokia AI", "Supercell AI", "Rovio AI", "F-Secure AI", "Wärtsilä AI"
        ]
    }

def main():
    companies_dict = get_global_ai_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"COMPREHENSIVE GLOBAL AI COMPANIES DATABASE")
    print(f"=" * 50)
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Total regions: {len(companies_dict)}")
    
    # Show regional breakdown
    print(f"\\nRegional breakdown:")
    for region, companies in companies_dict.items():
        print(f"{region}: {len(companies)} companies")
    
    # Save comprehensive list
    with open('/Users/adi/code/socratify/socratify-yolo/global_ai_companies_comprehensive.txt', 'w') as f:
        f.write("COMPREHENSIVE GLOBAL AI COMPANIES DATABASE\\n")
        f.write("=" * 60 + "\\n\\n")
        f.write(f"Total unique companies: {len(unique_companies)}\\n")
        f.write(f"Regions: {len(companies_dict)}\\n\\n")
        
        for region, companies in companies_dict.items():
            f.write(f"\\n### {region.upper().replace('_', ' ')} ###\\n")
            for company in companies:
                f.write(f"  - {company}\\n")
        
        f.write(f"\\n\\n### ALPHABETICAL MASTER LIST ###\\n")
        for i, company in enumerate(unique_companies, 1):
            f.write(f"{i:4d}. {company}\\n")
    
    print("Saved to global_ai_companies_comprehensive.txt")
    return unique_companies

if __name__ == "__main__":
    main()