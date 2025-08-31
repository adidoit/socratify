#!/usr/bin/env python3
"""
Check what major companies we're missing from our collection
Focus on categories people actually want to work for
"""

import os
import re

def normalize_name(name: str) -> str:
    """Normalize company name for comparison"""
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)
    return name

def get_existing_companies() -> set:
    """Get all companies we currently have"""
    existing = set()
    existing_names = set()  # Keep original names for better matching
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                # Remove extension
                name = os.path.splitext(file)[0]
                original_name = name.replace('_', ' ')
                existing_names.add(original_name.lower())
                
                # Normalize for matching
                normalized = normalize_name(name)
                existing.add(normalized)
                
                # Also add without common suffixes
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa)$', '', normalized)
                if clean_name != normalized:
                    existing.add(clean_name)
    
    return existing, existing_names

def check_missing_categories():
    """Check what we're missing in key categories"""
    existing, existing_names = get_existing_companies()
    print(f"Total companies in collection: {len(existing)}")
    
    missing_companies = {}
    
    # Major categories to check
    categories = {
        "Government_International": [
            "United Nations", "World Bank", "International Monetary Fund", "World Health Organization",
            "NATO", "European Union", "Federal Reserve", "European Central Bank", "Bank of England",
            "Bank of Japan", "NASA", "European Space Agency", "Central Intelligence Agency",
            "Federal Bureau of Investigation", "Interpol", "World Trade Organization", "OECD"
        ],
        
        "Latest_Unicorns_2024": [
            "Perplexity AI", "xAI", "Mistral AI", "Cohere", "Harvey", "Poolside", "ElevenLabs",
            "Character AI", "Glean", "Sierra", "Writer", "Hebbia", "Vanta", "Ramp", "Brex",
            "Deel", "Lattice", "Notion", "Linear", "Retool", "Vercel", "Supabase", "PlanetScale"
        ],
        
        "Climate_Tech": [
            "Tesla Energy", "Rivian", "Lucid Motors", "QuantumScape", "Solid Power", "Sila Nanotechnologies",
            "Commonwealth Fusion", "Helion Energy", "Form Energy", "Eos Energy", "Sunrun", "Enphase Energy",
            "First Solar", "SunPower", "NextEra Energy", "Brookfield Renewable", "Orsted", "Vestas",
            "General Fusion", "TAE Technologies", "Carbon Engineering", "Climeworks", "Global Thermostat"
        ],
        
        "Quantum_Computing": [
            "IBM Quantum", "Google Quantum", "IonQ", "Rigetti Computing", "PsiQuantum", "Xanadu",
            "D-Wave Systems", "Cambridge Quantum Computing", "Pasqal", "Atos Quantum", "Honeywell Quantum"
        ],
        
        "Space_Economy": [
            "SpaceX", "Blue Origin", "Virgin Galactic", "Rocket Lab", "Planet Labs", "Relativity Space",
            "Astra Space", "Firefly Aerospace", "Vector Launch", "Virgin Orbit", "Northrop Grumman Space",
            "Lockheed Martin Space", "Boeing Defense Space Security", "Sierra Space", "Axiom Space"
        ],
        
        "Biotech_Gene_Therapy": [
            "CRISPR Therapeutics", "Editas Medicine", "Intellia Therapeutics", "Beam Therapeutics",
            "Prime Medicine", "Mammoth Biosciences", "Sherlock Biosciences", "Ginkgo Bioworks",
            "Synthetic Genomics", "Twist Bioscience", "10x Genomics", "Pacific Biosciences",
            "Oxford Nanopore", "Illumina", "Thermo Fisher Scientific"
        ],
        
        "Digital_Health": [
            "Teladoc Health", "Amwell", "Doxy.me", "MDLive", "Doctor on Demand", "Babylon Health",
            "Ro", "Hims", "Nurx", "Pill Club", "Capsule", "Alto Pharmacy", "23andMe", "Color Genomics",
            "Guardant Health", "Foundation Medicine", "Tempus", "Flatiron Health", "Veracyte"
        ],
        
        "Gaming_Entertainment": [
            "Roblox Corporation", "Unity Technologies", "Epic Games", "Riot Games", "Valve Corporation",
            "Discord", "Twitch", "YouTube Gaming", "Spotify Gaming", "Sony Interactive Entertainment",
            "Microsoft Gaming", "Nintendo of America", "Activision Blizzard", "Electronic Arts",
            "Take-Two Interactive", "Ubisoft", "CD Projekt", "Supercell", "King Digital Entertainment"
        ],
        
        "Cybersecurity_Defense": [
            "CrowdStrike", "SentinelOne", "Darktrace", "Okta", "Zscaler", "Palo Alto Networks",
            "Fortinet", "Check Point", "CyberArk", "Rapid7", "Qualys", "Tenable", "Splunk",
            "Carbon Black", "FireEye", "Mandiant", "Tanium", "Cylance", "Symantec", "McAfee"
        ],
        
        "Neobanks_Fintech": [
            "Chime", "Dave", "Varo Bank", "Current", "Ally Bank", "Marcus by Goldman Sachs",
            "SoFi", "Lending Club", "Prosper", "Upgrade", "Avant", "LendingTree", "Credit Karma",
            "NerdWallet", "Mint", "Personal Capital", "Betterment", "Wealthfront", "Robinhood",
            "Webull", "TD Ameritrade", "E*TRADE", "Charles Schwab", "Fidelity Investments"
        ],
        
        "Consulting_Strategy": [
            "McKinsey & Company", "Boston Consulting Group", "Bain & Company", "Deloitte Consulting",
            "PwC Strategy", "EY Strategy", "KPMG Strategy", "Accenture Strategy", "Oliver Wyman",
            "A.T. Kearney", "Roland Berger", "Strategy&", "L.E.K. Consulting", "Parthenon-EY",
            "Monitor Deloitte", "IBM Consulting", "Capgemini Consulting"
        ]
    }
    
    # Check each category
    for category, companies in categories.items():
        missing_in_category = []
        found_in_category = []
        
        for company in companies:
            normalized = normalize_name(company)
            company_lower = company.lower()
            found = False
            
            # Check exact match in normalized names
            if normalized in existing:
                found_in_category.append(company)
                found = True
            else:
                # Check in original names (better for things like "McKinsey & Company")
                for exist_name in existing_names:
                    # Direct substring match
                    if company_lower in exist_name or exist_name in company_lower:
                        # Check if it's a meaningful match (not just "a" in "apple")
                        if len(company_lower) >= 3 and len(exist_name) >= 3:
                            found_in_category.append(f"{company} (found as: {exist_name})")
                            found = True
                            break
                
                # If still not found, check normalized partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 3 and len(exist) > 3:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.6:
                                    found_in_category.append(f"{company} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(company)
        
        missing_companies[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(companies) * 100
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total companies checked: {len(companies)}")
        print(f"Found: {len(found_in_category)} ({missing_companies[category]['coverage']:.1f}%)")
        print(f"Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print("Missing companies:")
            for company in missing_in_category:
                print(f"  - {company}")
    
    # Summary
    print(f"\n=== SUMMARY ===")
    total_missing = sum(len(data['missing']) for data in missing_companies.values())
    total_checked = sum(len(data['missing']) + len(data['found']) for data in missing_companies.values())
    
    print(f"Total companies checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    # Save results
    with open('/Users/adi/code/socratify/socratify-yolo/missing_analysis_results.txt', 'w') as f:
        f.write("MISSING COMPANIES ANALYSIS\\n")
        f.write("=" * 30 + "\\n\\n")
        f.write(f"Total companies in collection: {len(existing)}\\n")
        f.write(f"Total missing: {total_missing}\\n\\n")
        
        for category, data in missing_companies.items():
            f.write(f"### {category.upper().replace('_', ' ')} ###\\n")
            f.write(f"Coverage: {data['coverage']:.1f}%\\n")
            f.write(f"Missing ({len(data['missing'])}):\\n")
            for company in data['missing']:
                f.write(f"  - {company}\\n")
            f.write("\\n")
    
    print(f"\\nSaved detailed results to missing_analysis_results.txt")
    return missing_companies

if __name__ == "__main__":
    check_missing_categories()