#!/usr/bin/env python3
"""
Hottest 2025 AI Companies Database
Companies people aspire to work for - focus on what we're missing
"""

def get_hottest_2025_ai_companies():
    """Most sought-after AI companies in 2025"""
    return {
        "Foundation_Models_LLM": [
            # We have: OpenAI, Anthropic, Cohere, Together AI
            "xAI",  # Elon Musk's $113B AI company
            "Mistral AI",  # European AI champion  
            "Perplexity AI",  # Answer engine unicorn
            "Character AI",  # Conversational AI platform
            "Inflection AI",  # Personal AI assistant Pi
            "Adept AI",  # Action-oriented AI
            "AI21 Labs",  # Enterprise LLM platform
            "Stability AI",  # Open source generative AI
            "Writer",  # Enterprise writing AI
            "Jasper AI",  # AI content platform
        ],
        
        "AI_Agents_Automation": [
            # We have: Harvey (but wrong Harvey - building products, not legal AI)
            "Cognition Labs",  # Devin AI software engineer - $4B valuation  
            "Harvey AI",  # Legal AI platform - $3B valuation
            "Multi",  # AI agents for workflows
            "Hebbia",  # AI search and analysis
            "Sierra",  # Conversational AI agents
            "Glean",  # Enterprise search AI
            "Vanta",  # Security compliance automation
            "Magic",  # AI coding assistant
            "Cursor",  # AI code editor
            "Replit",  # AI programming platform
        ],
        
        "AI_Infrastructure_Tools": [
            # We have: Scale AI, Databricks, CoreWeave, Weights & Biases, Hugging Face
            "Modal",  # Serverless cloud for AI
            "RunPod",  # GPU cloud platform
            "Lambda Labs",  # AI infrastructure
            "Replicate",  # ML model hosting
            "Anyscale",  # Ray distributed computing
            "Pinecone",  # Vector database
            "Weaviate",  # Vector search engine
            "Qdrant",  # Vector similarity search
            "LangChain",  # LLM application framework
            "Wandb",  # ML experiment tracking
        ],
        
        "Computer_Vision_Robotics": [
            # We have: Figure (but need to check if it's Figure AI)
            "Figure AI",  # Humanoid robots - $39.5B valuation target
            "Physical Intelligence",  # Robotics foundation models
            "Boston Dynamics AI",  # Advanced robotics with ML
            "1X Technologies",  # Humanoid robots (NEO)
            "Agility Robotics",  # Digit humanoid robot
            "Sanctuary AI",  # General-purpose humanoid robots
            "Tesla Bot",  # Tesla's humanoid robot division
            "Waymo",  # Autonomous driving AI
            "Cruise",  # GM's self-driving unit
            "Aurora",  # Autonomous trucking AI
        ],
        
        "Vertical_AI_Specialized": [
            # We have: Grammarly, Tempus, Abridge, Synthesia
            "AssemblyAI",  # Speech-to-text API platform
            "PathAI",  # Healthcare AI diagnostics  
            "Exscientia",  # AI drug discovery
            "DeepMind Health",  # Google's healthcare AI
            "Freenome",  # AI cancer detection
            "Guardant Health",  # Liquid biopsy AI
            "Clara Health",  # Clinical trial AI
            "Benchling",  # Life sciences R&D platform
            "Notable",  # Healthcare AI automation
            "Regard",  # Clinical AI assistant
        ],
        
        "AI_Research_Labs": [
            # We have: Anthropic, OpenAI
            "DeepMind",  # Google's AI research lab
            "FAIR",  # Facebook AI Research
            "Allen Institute for AI",  # Non-profit AI research
            "Redwood Research",  # AI alignment research
            "Center for AI Safety",  # AI safety research
            "Machine Intelligence Research Institute",  # AI safety
            "Future of Humanity Institute",  # AI safety research
            "Partnership on AI",  # AI research collaboration
            "Element AI",  # Applied AI research
            "Mila Quebec",  # AI research institute
        ],
        
        "Hot_AI_Startups_2024_2025": [
            "Poolside",  # AI coding platform
            "Magic AI",  # AI software engineer
            "Augment",  # AI coding assistant  
            "Tabnine",  # AI code completion
            "Sourcegraph Cody",  # AI coding assistant
            "GitHub Copilot",  # Microsoft's AI coding
            "Amazon CodeWhisperer",  # AWS AI coding
            "Replit Ghostwriter",  # AI pair programmer
            "Codium AI",  # AI testing platform
            "Mintlify",  # AI documentation
        ],
        
        "Enterprise_AI_Platforms": [
            "DataRobot",  # Automated machine learning
            "H2O.ai",  # Open source ML platform
            "Dataiku",  # Data science platform
            "Palantir Foundry",  # Big data analytics AI
            "C3 AI",  # Enterprise AI applications
            "SAS Viya",  # Analytics and AI platform
            "Alteryx",  # Analytics automation
            "Domino Data Lab",  # MLOps platform
            "neptune.ai",  # ML experiment management
            "Feast",  # Feature store for ML
        ],
        
        "AI_Hardware_Chips": [
            "Cerebras Systems",  # AI chip startup
            "SambaNova Systems",  # AI chip platform
            "Graphcore",  # Intelligence Processing Units
            "Habana Labs",  # Intel's AI chip division
            "Groq",  # AI inference chips
            "Tenstorrent",  # AI processor architecture
            "Mythic",  # AI edge computing chips
            "BrainChip",  # Neuromorphic AI chips
            "Rain AI",  # Memristive AI chips
            "Untether AI",  # At-memory computing
        ]
    }

def main():
    companies_dict = get_hottest_2025_ai_companies()
    
    # Flatten all companies
    all_companies = []
    for category, company_list in companies_dict.items():
        all_companies.extend(company_list)
    
    # Remove duplicates
    unique_companies = sorted(list(set(all_companies)))
    
    print(f"HOTTEST 2025 AI COMPANIES DATABASE")
    print(f"=" * 40)
    print(f"Total unique companies: {len(unique_companies)}")
    print(f"Total categories: {len(companies_dict)}")
    
    # Show category breakdown
    print(f"\nCategory breakdown:")
    for category, companies in companies_dict.items():
        print(f"{category}: {len(companies)} companies")
    
    # Save comprehensive list
    with open('/Users/adi/code/socratify/socratify-yolo/hottest_2025_ai_companies_list.txt', 'w') as f:
        f.write("HOTTEST 2025 AI COMPANIES - COMPREHENSIVE LIST\\n")
        f.write("=" * 50 + "\\n\\n")
        f.write(f"Total unique companies: {len(unique_companies)}\\n")
        f.write(f"Categories: {len(companies_dict)}\\n\\n")
        
        for category, companies in companies_dict.items():
            f.write(f"\\n### {category.upper().replace('_', ' ')} ###\\n")
            for company in companies:
                f.write(f"  - {company}\\n")
        
        f.write(f"\\n\\n### ALPHABETICAL MASTER LIST ###\\n")
        for i, company in enumerate(unique_companies, 1):
            f.write(f"{i:3d}. {company}\\n")
    
    print("Saved to hottest_2025_ai_companies_list.txt")
    return unique_companies

if __name__ == "__main__":
    main()