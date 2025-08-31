#!/usr/bin/env python3
"""
Sector-Specific Companies Collection Summary
Analyze and summarize all the logos collected from various specialized sectors
"""

import os
import json
from datetime import datetime
from collections import defaultdict
import glob

def analyze_collection():
    """Analyze the collected logos across all directories"""
    
    base_path = "/Users/adi/code/socratify/socratify-yolo"
    
    # Define directories to analyze
    directories = {
        "sector_specific_companies": "Media & Entertainment, Food Tech, PropTech, EdTech, HR Tech, InsurTech, Supply Chain, Travel Tech",
        "newsworthy_2024_companies": "AI/ML, Fintech, E-commerce, Health Tech, Crypto/Web3, Climate Tech, Social/Creator, Gaming/Metaverse",
        "regional_newsworthy_companies": "European, Asian, Latin American, Middle Eastern, African, Canadian companies",
        "trending_specialized_companies": "B2B SaaS, Cybersecurity, DevOps, Design, No-Code, Data Analytics, Clean Tech"
    }
    
    total_logos = 0
    results = {}
    
    print("="*80)
    print("🎯 SECTOR-SPECIFIC COMPANIES COLLECTION SUMMARY")
    print("="*80)
    print()
    
    for directory, description in directories.items():
        dir_path = os.path.join(base_path, directory)
        if os.path.exists(dir_path):
            png_files = glob.glob(os.path.join(dir_path, "*.png"))
            count = len(png_files)
            total_logos += count
            results[directory] = {
                'count': count,
                'description': description,
                'files': [os.path.basename(f) for f in png_files]
            }
            print(f"📁 {directory.upper()}")
            print(f"   Description: {description}")
            print(f"   Logos collected: {count}")
            print()
        else:
            print(f"📁 {directory.upper()}: Directory not found")
            print()
    
    print("="*80)
    print("📊 OVERALL SUMMARY")
    print("="*80)
    print(f"Total logos collected: {total_logos}")
    print(f"Categories covered: {len([k for k, v in results.items() if v['count'] > 0])}")
    print(f"Collection date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Sector breakdown
    print("🏢 SECTOR BREAKDOWN:")
    print("-" * 40)
    sector_mapping = {
        "sector_specific_companies": [
            "Media & Entertainment (133 companies)",
            "Food Tech & AgTech (110 companies)", 
            "PropTech & Construction (78 companies)",
            "EdTech (76 companies)",
            "HR Tech & Future of Work (84 companies)",
            "InsurTech & LegalTech (84 companies)",
            "Supply Chain & Manufacturing (67 companies)",
            "Travel & Hospitality (60 companies)"
        ],
        "newsworthy_2024_companies": [
            "AI & Machine Learning (30 companies)",
            "Fintech (32 companies)",
            "E-commerce & Marketplace (31 companies)",
            "Health Tech & Telemedicine (31 companies)",
            "Crypto & Web3 (33 companies)",
            "Climate Tech & Sustainability (30 companies)",
            "Social Media & Creator Economy (32 companies)",
            "Gaming & Metaverse (31 companies)",
            "DevTools & Infrastructure (35 companies)",
            "Productivity & Collaboration (34 companies)",
            "Food Delivery & Quick Commerce (32 companies)",
            "Remote Work & Digital Nomad (32 companies)"
        ],
        "regional_newsworthy_companies": [
            "European companies (160 companies)",
            "Asian Pacific companies (75 companies)", 
            "Latin American companies (65 companies)",
            "Middle East & African companies (65 companies)",
            "Canadian companies (20 companies)"
        ],
        "trending_specialized_companies": [
            "B2B SaaS & Enterprise (30 companies)",
            "Cybersecurity & Data Protection (30 companies)",
            "DevOps & Cloud Infrastructure (30 companies)",
            "Design & Creative Tools (30 companies)",
            "No-Code & Low-Code Platforms (30 companies)",
            "Data & Analytics Platforms (30 companies)",
            "Customer Success & Support (30 companies)",
            "Sales & Marketing Automation (30 companies)",
            "Extended PropTech (30 companies)",
            "Financial Services & Payments (36 companies)",
            "Extended Health & Wellness Tech (30 companies)",
            "Media & Content Platforms (30 companies)",
            "E-learning & Skills Development (30 companies)",
            "Extended Gaming & Entertainment (30 companies)",
            "Emerging Technologies (30 companies)",
            "Clean Tech & Sustainability (36 companies)"
        ]
    }
    
    for directory, sectors in sector_mapping.items():
        if directory in results and results[directory]['count'] > 0:
            print(f"\n{directory.upper().replace('_', ' ')} ({results[directory]['count']} logos):")
            for sector in sectors:
                print(f"  • {sector}")
    
    # Notable companies collected
    print("\n🌟 NOTABLE COMPANIES INCLUDED:")
    print("-" * 40)
    notable_examples = [
        "Media & Entertainment: Netflix competitors, Gaming studios, Podcast networks",
        "Food Tech: Beyond Meat, Impossible Foods, Vertical farming startups",
        "PropTech: Compass, Redfin, Zillow, Construction management tools",
        "EdTech: Coursera, Udemy, Corporate training platforms",
        "HR Tech: Slack, Zoom, Remote work tools, Recruitment platforms", 
        "FinTech: Klarna, Stripe, Revolut, Digital payment solutions",
        "AI/ML: OpenAI, Anthropic, Hugging Face, Generative AI tools",
        "Regional: European unicorns, Asian tech giants, LatAm fintech",
        "Specialized: B2B SaaS, Cybersecurity leaders, DevOps platforms"
    ]
    
    for example in notable_examples:
        print(f"  • {example}")
    
    # Business case study potential
    print("\n💼 BUSINESS CASE STUDY POTENTIAL:")
    print("-" * 40)
    case_study_categories = [
        "Unicorn startups with unique business models",
        "Companies that raised Series A+ funding in 2023-2024",
        "High-growth companies featured in TechCrunch, Forbes",
        "Regional success stories from emerging markets", 
        "Vertical SaaS companies disrupting traditional industries",
        "Platform businesses with network effects",
        "Subscription-based recurring revenue models",
        "Direct-to-consumer brands and marketplaces"
    ]
    
    for category in case_study_categories:
        print(f"  • {category}")
    
    # Save detailed results
    results_summary = {
        'collection_date': datetime.now().isoformat(),
        'total_logos': total_logos,
        'directories': results,
        'sector_breakdown': sector_mapping,
        'notable_examples': notable_examples,
        'case_study_categories': case_study_categories
    }
    
    with open(os.path.join(base_path, 'sector_specific_collection_summary.json'), 'w') as f:
        json.dump(results_summary, f, indent=2)
    
    print(f"\n📁 Detailed summary saved to: sector_specific_collection_summary.json")
    print("="*80)

if __name__ == "__main__":
    analyze_collection()