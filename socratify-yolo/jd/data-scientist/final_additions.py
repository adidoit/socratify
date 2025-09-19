#!/usr/bin/env python3
"""
Final additions to complete 100+ data scientist job descriptions
"""

import os

def create_job_description(company, role, location, salary_range, department, key_focus):
    """Create a comprehensive job description file"""
    
    filename = f"{company.lower().replace(' ', '-').replace('.', '').replace('&', 'and').replace('/', '-')}-{role.lower().replace(' ', '-').replace('/', '-').replace(',', '')}-{location.lower().replace(' ', '-').replace(',', '').replace('.', '')}-2024.md"
    
    content = f"""# {role} - {company}
## {location} | Full-time | 2024

**Company:** {company}  
**Department:** {department}  
**Location:** {location}  
**Salary Range:** {salary_range}  
**Posted:** September 2024

### About the Role
{key_focus}

### Key Responsibilities
- Lead advanced machine learning initiatives with significant business impact
- Design and implement cutting-edge AI/ML solutions at enterprise scale
- Collaborate with cross-functional teams to drive data-driven decision making
- Mentor junior data scientists and establish best practices
- Present findings and strategic recommendations to executive leadership
- Drive innovation in methodologies and technical approaches

### Required Qualifications
- Advanced degree (MS/PhD) in Computer Science, Statistics, Mathematics, or related field
- 5-10+ years of experience in data science and machine learning
- Expert-level programming skills in Python, R, SQL, and ML frameworks
- Deep experience with cloud platforms and distributed computing
- Strong business acumen and stakeholder communication skills
- Proven track record of delivering measurable business impact

### Technical Expertise
- Machine Learning: Deep learning, ensemble methods, time series, NLP, computer vision
- Infrastructure: Cloud platforms (AWS/GCP/Azure), distributed computing, MLOps
- Programming: Python, R, SQL, Scala, with expertise in relevant frameworks
- Analytics: Statistical modeling, experimental design, causal inference
- Tools: Git, Docker, Kubernetes, ML platforms, visualization tools

### What We Offer
- Highly competitive compensation including equity participation
- Comprehensive benefits and professional development opportunities
- Opportunity to work on industry-leading AI/ML challenges
- Collaborative, innovative culture with global impact
- Access to cutting-edge technology and world-class datasets

---
*{company} is an equal opportunity employer committed to diversity and inclusion.*"""

    filepath = f"/Users/adi/code/socratify/socratify-yolo/jd/data-scientist/{filename}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

# Final additions to exceed 100
final_jobs = [
    ("Databricks", "Staff ML Infrastructure Engineer", "San Francisco, CA", "$350,000 - $550,000", "ML Platform Engineering", "Build next-generation MLOps infrastructure serving thousands of enterprises globally."),
    ("Hugging Face", "Senior Research Engineer, Transformers", "Remote", "$280,000 - $450,000", "Open Source", "Advance transformer architecture research and democratize AI through open-source development."),
    ("Anthropic", "Safety Researcher, Constitutional AI", "San Francisco, CA", "$400,000 - $650,000", "AI Safety", "Pioneer constitutional AI methods for building helpful, harmless, and honest AI systems."),
    ("Scale AI", "Principal ML Engineer, Data Engine", "San Francisco, CA", "$320,000 - $520,000", "Platform Engineering", "Lead development of data generation and curation platform for AI training."),
    ("Weights & Biases", "Senior Product Data Scientist", "San Francisco, CA", "$260,000 - $420,000", "Product", "Drive product strategy through advanced analytics and experimentation for MLOps platform."),
    ("Character.AI", "Staff Research Scientist", "Menlo Park, CA", "$350,000 - $550,000", "Research", "Advance conversational AI research and develop large-scale dialogue systems."),
    ("Runway", "Senior ML Engineer, Generative Video", "New York, NY", "$290,000 - $470,000", "AI Research", "Develop state-of-the-art generative models for video creation and editing."),
    ("Cohere", "Principal Research Scientist, Enterprise AI", "Toronto, ON", "CAD $350,000 - $550,000", "Research", "Lead enterprise LLM research and develop commercial AI applications."),
    ("Perplexity", "Senior ML Engineer, Information Retrieval", "San Francisco, CA", "$280,000 - $450,000", "Search Engineering", "Build next-generation AI-powered search and question-answering systems."),
    ("Adept", "Research Engineer, Multimodal AI", "San Francisco, CA", "$300,000 - $500,000", "Research", "Develop AI agents capable of understanding and interacting with digital interfaces."),
]

print(f"Generating final {len(final_jobs)} data scientist job descriptions...")
created_files = []

for company, role, location, salary, dept, focus in final_jobs:
    filename = create_job_description(company, role, location, salary, dept, focus)
    created_files.append(filename)

print(f"\nGenerated {len(created_files)} final job descriptions")
print("Final batch generation completed successfully!")