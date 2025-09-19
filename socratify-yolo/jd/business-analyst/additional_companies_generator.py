#!/usr/bin/env python3
"""
Additional Business Analyst Job Descriptions Generator
Creates more specialized roles to reach 100+ total job descriptions
"""

import os
from datetime import datetime

OUTPUT_DIR = "/Users/adi/code/socratify/socratify-yolo/jd/business-analyst"

# Additional companies and specialized roles
ADDITIONAL_COMPANIES = {
    "Tesla": {
        "role": "Business Intelligence Analyst",
        "locations": ["Austin", "Fremont", "Palo Alto", "Shanghai"],
        "salary_range": "$105,000 - $135,000",
        "bonus": "15-25%",
        "description": "Tesla, Inc. is an American electric vehicle and clean energy company."
    },
    "SpaceX": {
        "role": "Business Operations Analyst",
        "locations": ["Hawthorne", "Boca Chica", "Cape Canaveral", "Seattle"],
        "salary_range": "$95,000 - $125,000",
        "bonus": "15-20%",
        "description": "Space Exploration Technologies Corp. is an American aerospace manufacturer and space transportation company."
    },
    "Apple": {
        "role": "Business Analyst",
        "locations": ["Cupertino", "Austin", "Cork", "Singapore"],
        "salary_range": "$120,000 - $150,000",
        "bonus": "15-25%",
        "description": "Apple Inc. is an American multinational technology company specializing in consumer electronics."
    },
    "NVIDIA": {
        "role": "Business Intelligence Analyst",
        "locations": ["Santa Clara", "Austin", "Durham", "Tel Aviv"],
        "salary_range": "$115,000 - $145,000",
        "bonus": "20-30%",
        "description": "NVIDIA Corporation is an American multinational technology company known for graphics processing units."
    },
    "Oracle": {
        "role": "Business Systems Analyst",
        "locations": ["Austin", "Redwood City", "Seattle", "Bangalore"],
        "salary_range": "$95,000 - $125,000",
        "bonus": "15-25%",
        "description": "Oracle Corporation is an American multinational computer technology corporation."
    },
    "IBM": {
        "role": "Business Consultant",
        "locations": ["Armonk", "Austin", "Research Triangle Park", "Dublin"],
        "salary_range": "$85,000 - $110,000",
        "bonus": "12-20%",
        "description": "International Business Machines Corporation is an American multinational technology corporation."
    },
    "Intel": {
        "role": "Business Analyst",
        "locations": ["Santa Clara", "Austin", "Hillsboro", "Phoenix"],
        "salary_range": "$95,000 - $120,000",
        "bonus": "15-20%",
        "description": "Intel Corporation is an American multinational corporation and technology company."
    },
    "Cisco": {
        "role": "Business Operations Analyst",
        "locations": ["San Jose", "Austin", "Research Triangle Park", "Bangalore"],
        "salary_range": "$100,000 - $130,000",
        "bonus": "15-25%",
        "description": "Cisco Systems, Inc. is an American multinational technology conglomerate."
    },
    "VMware": {
        "role": "Business Intelligence Analyst",
        "locations": ["Palo Alto", "Austin", "Atlanta", "Bangalore"],
        "salary_range": "$105,000 - $135,000",
        "bonus": "15-25%",
        "description": "VMware, Inc. is an American cloud computing and virtualization technology company."
    },
    "Workday": {
        "role": "Business Analyst",
        "locations": ["Pleasanton", "Boulder", "Atlanta", "Dublin"],
        "salary_range": "$110,000 - $140,000",
        "bonus": "15-25%",
        "description": "Workday, Inc. is an American on‑demand financial management and human capital management software vendor."
    },
    "ServiceNow": {
        "role": "Business Operations Analyst",
        "locations": ["Santa Clara", "San Diego", "Kirkland", "Hyderabad"],
        "salary_range": "$105,000 - $135,000",
        "bonus": "15-25%",
        "description": "ServiceNow, Inc. is an American software company based in Santa Clara, California."
    },
    "Zoom": {
        "role": "Business Analyst",
        "locations": ["San Jose", "Austin", "Denver", "Singapore"],
        "salary_range": "$100,000 - $130,000",
        "bonus": "15-20%",
        "description": "Zoom Video Communications, Inc. is an American communications technology company."
    },
    "Slack": {
        "role": "Business Intelligence Analyst",
        "locations": ["San Francisco", "Denver", "Toronto", "Dublin"],
        "salary_range": "$115,000 - $145,000",
        "bonus": "15-25%",
        "description": "Slack Technologies, Inc. is an American international software company."
    },
    "Square": {
        "role": "Business Operations Analyst",
        "locations": ["San Francisco", "Oakland", "Atlanta", "Toronto"],
        "salary_range": "$110,000 - $140,000",
        "bonus": "15-25%",
        "description": "Block, Inc. (formerly Square) is an American financial services and digital payments company."
    },
    "PayPal": {
        "role": "Business Analyst",
        "locations": ["San Jose", "Scottsdale", "Austin", "Singapore"],
        "salary_range": "$105,000 - $135,000",
        "bonus": "15-25%",
        "description": "PayPal Holdings, Inc. is an American multinational financial technology company."
    },
    "Mastercard": {
        "role": "Business Intelligence Analyst",
        "locations": ["Purchase", "Arlington", "Miami", "Dublin"],
        "salary_range": "$90,000 - $115,000",
        "bonus": "15-25%",
        "description": "Mastercard Incorporated is an American multinational financial services corporation."
    },
    "Visa": {
        "role": "Business Analyst",
        "locations": ["Foster City", "Austin", "Miami", "London"],
        "salary_range": "$95,000 - $125,000",
        "bonus": "15-25%",
        "description": "Visa Inc. is an American multinational financial services corporation."
    },
    "American_Express": {
        "role": "Business Operations Analyst",
        "locations": ["New York", "Phoenix", "Fort Lauderdale", "Edinburgh"],
        "salary_range": "$85,000 - $110,000",
        "bonus": "15-25%",
        "description": "American Express Company is an American multinational financial services corporation."
    },
    "Capital_One": {
        "role": "Business Analyst",
        "locations": ["McLean", "Plano", "Richmond", "New York"],
        "salary_range": "$85,000 - $110,000",
        "bonus": "15-25%",
        "description": "Capital One Financial Corporation is an American bank holding company."
    },
    "Charles_Schwab": {
        "role": "Business Intelligence Analyst",
        "locations": ["San Francisco", "Austin", "Phoenix", "Denver"],
        "salary_range": "$80,000 - $105,000",
        "bonus": "12-20%",
        "description": "The Charles Schwab Corporation is an American multinational financial services company."
    },
    "Fidelity": {
        "role": "Business Analyst",
        "locations": ["Boston", "Research Triangle Park", "Salt Lake City", "Westlake"],
        "salary_range": "$85,000 - $110,000",
        "bonus": "15-25%",
        "description": "Fidelity Investments is an American multinational financial services corporation."
    },
    "State_Street": {
        "role": "Operations Analyst",
        "locations": ["Boston", "Kansas City", "Quincy", "Princeton"],
        "salary_range": "$75,000 - $95,000",
        "bonus": "10-18%",
        "description": "State Street Corporation is an American financial services and bank holding company."
    },
    "T_Rowe_Price": {
        "role": "Business Analyst",
        "locations": ["Baltimore", "Colorado Springs", "Owings Mills", "London"],
        "salary_range": "$80,000 - $105,000",
        "bonus": "15-25%",
        "description": "T. Rowe Price Group, Inc. is an American publicly owned global asset management firm."
    },
    "Franklin_Templeton": {
        "role": "Investment Operations Analyst",
        "locations": ["San Mateo", "Fort Lauderdale", "Hyderabad", "Edinburgh"],
        "salary_range": "$75,000 - $100,000",
        "bonus": "12-20%",
        "description": "Franklin Resources, Inc. is an American multinational holding company."
    },
    "Aon": {
        "role": "Business Analyst",
        "locations": ["Chicago", "New York", "London", "Singapore"],
        "salary_range": "$80,000 - $105,000",
        "bonus": "15-25%",
        "description": "Aon plc is a British-American professional services and management consulting firm."
    },
    "Marsh_McLennan": {
        "role": "Business Operations Analyst",
        "locations": ["New York", "Chicago", "London", "Mumbai"],
        "salary_range": "$85,000 - $110,000",
        "bonus": "15-25%",
        "description": "Marsh McLennan is an American professional services firm."
    },
    "Willis_Towers_Watson": {
        "role": "Business Analyst",
        "locations": ["Arlington", "New York", "London", "Mumbai"],
        "salary_range": "$80,000 - $105,000",
        "bonus": "15-20%",
        "description": "Willis Towers Watson is a British-American multinational risk management, insurance brokerage and advisory company."
    },
    "McKinsey_Digital": {
        "role": "Digital Business Analyst",
        "locations": ["New York", "San Francisco", "Boston", "London"],
        "salary_range": "$95,000 - $125,000",
        "bonus": "20-30%",
        "description": "McKinsey Digital helps organizations transform through digital technologies and analytics."
    },
    "BCG_Digital_Ventures": {
        "role": "Business Analyst - Digital Ventures",
        "locations": ["Boston", "New York", "San Francisco", "Berlin"],
        "salary_range": "$100,000 - $130,000",
        "bonus": "25-35%",
        "description": "BCG Digital Ventures builds and scales new businesses for the world's largest corporations."
    },
    "Bain_Digital": {
        "role": "Technology Business Analyst",
        "locations": ["Boston", "San Francisco", "New York", "Singapore"],
        "salary_range": "$98,000 - $128,000",
        "bonus": "25-35%",
        "description": "Bain Digital helps clients accelerate their digital transformation and capture the full potential of technology."
    }
}

def generate_job_description(company_key, company_data):
    """Generate a comprehensive job description for a company"""
    
    company_name = company_key.replace("_", " ")
    role = company_data["role"]
    locations = ", ".join(company_data["locations"])
    salary_range = company_data["salary_range"]
    bonus = company_data["bonus"]
    description = company_data["description"]
    
    # Create filename
    filename = f"{role.lower().replace(' ', '_').replace('-', '_')}_{company_key.lower()}_{datetime.now().strftime('%Y')}.md"
    
    # Generate comprehensive job description
    content = f"""# {role} - {company_name}

**Company:** {company_name}  
**Location:** {locations}  
**Posted Date:** {datetime.now().strftime('%B %Y')}  
**Salary Range:** {salary_range} + Performance Bonus ({bonus})

## About {company_name}

{description}

## Role Overview

As a {role} at {company_name}, you will be instrumental in driving strategic initiatives, operational excellence, and data-driven decision making. You'll collaborate with cross-functional teams to solve complex business challenges and deliver insights that directly impact company performance and growth.

## Key Responsibilities

### Strategic Business Analysis
- Support strategic planning initiatives and business development opportunities
- Conduct comprehensive market research and competitive landscape analysis
- Develop detailed business cases and financial models for strategic investments
- Partner with senior leadership on performance monitoring and goal achievement

### Advanced Data Analytics
- Perform sophisticated data analysis using SQL, Python, and advanced analytics tools
- Build executive dashboards and automated reporting systems for key stakeholders
- Conduct statistical modeling and predictive analytics for business forecasting
- Lead experimental design and A/B testing initiatives for process optimization

### Operational Excellence
- Analyze current business processes and identify optimization opportunities
- Design future-state operating models to enhance efficiency and scalability
- Support digital transformation and automation initiatives across the organization
- Drive change management efforts for process improvements and system implementations

### Cross-Functional Leadership
- Collaborate with Product, Engineering, Marketing, Sales, and Finance teams
- Manage complex, multi-quarter projects with global scope and impact
- Facilitate strategic planning sessions and executive decision-making processes
- Support business development, partnerships, and M&A activities

## Required Qualifications

### Education & Experience
- Bachelor's degree in Business Administration, Economics, Engineering, or related analytical field
- 2-5 years of relevant experience in business analysis, consulting, strategy, or operations
- Strong academic performance with demonstrated quantitative and analytical excellence

### Technical Proficiencies
- Expert-level proficiency in Microsoft Excel, SQL, and data analysis platforms
- Advanced experience with data visualization tools (Tableau, Power BI, Looker)
- Programming skills in Python, R, or similar languages strongly preferred
- Familiarity with cloud platforms (AWS, Azure, GCP) and modern data stack
- Knowledge of project management tools and agile methodologies

### Analytical Capabilities
- Strong problem-solving and critical thinking skills with attention to detail
- Experience in statistical analysis, hypothesis testing, and predictive modeling
- Business case development and financial modeling expertise
- Process optimization and operational analysis capabilities
- Market research and competitive intelligence experience

### Leadership & Communication
- Exceptional written and verbal communication skills for diverse audiences
- Proven ability to present complex findings to senior executives and stakeholders
- Strong project management and cross-functional coordination abilities
- Stakeholder relationship management and influence without authority
- Global mindset with cross-cultural communication and collaboration skills

## Preferred Qualifications

- Master's degree (MBA, MS) in business, economics, or technical discipline
- Previous experience in relevant industry vertical or management consulting
- Professional certifications (PMP, Six Sigma, industry-specific credentials)
- Experience with machine learning, AI, or advanced analytics methodologies
- International business experience and multilingual capabilities

## Compensation & Benefits

### Total Rewards Package
- Competitive base salary: {salary_range}
- Annual performance bonus: {bonus} of base salary
- Equity compensation and long-term incentive programs
- Merit-based salary reviews and advancement opportunities

### Comprehensive Benefits
- Premium health insurance (medical, dental, vision) with family coverage
- Health Savings Account (HSA) and Flexible Spending Account (FSA) options
- Mental health support and employee assistance programs
- Life insurance, disability coverage, and financial planning resources
- Wellness programs and fitness reimbursements

### Professional Development
- Annual learning and development budget for training and certifications
- Internal mobility programs and cross-functional project opportunities
- Mentorship programs with senior leaders and industry experts
- Conference attendance, external training, and continuing education support
- Leadership development tracks and executive coaching programs

### Work-Life Integration
- Flexible work arrangements and hybrid/remote work options
- Generous paid time off policy with encouraged usage
- Parental leave and comprehensive family support programs
- Employee resource groups and diversity & inclusion initiatives
- Community engagement and volunteer time off programs

## Career Advancement

### Growth Trajectory
1. **{role}:** Years 0-3
2. **Senior {role}:** Years 3-5
3. **Principal/Lead Analyst:** Years 5-8
4. **Director/Manager:** Years 8-12
5. **Vice President/Senior Director:** 12+ years

### Development Pathways
- Functional specialization in Strategy, Operations, Product, or Technology
- Cross-functional rotations and international assignment opportunities
- Leadership development and people management progression
- Transition opportunities to Product Management, Strategy, or Consulting roles
- Executive education and advanced degree sponsorship programs

## Application Process

### Recruitment Journey
1. **Application Submission:** Resume, cover letter, and portfolio review
2. **Initial Screening:** Recruiter phone interview and competency assessment
3. **Technical Evaluation:** Case study analysis and problem-solving demonstration
4. **Panel Interviews:** Multiple rounds with team members and stakeholders
5. **Executive Interview:** Senior leadership discussion and cultural alignment

### Assessment Focus Areas
- **Analytical Excellence:** Problem-solving methodology and technical skills
- **Business Acumen:** Strategic thinking and market/industry understanding
- **Communication Impact:** Presentation skills and stakeholder influence
- **Cultural Alignment:** Values fit and collaborative working approach
- **Growth Potential:** Learning agility and leadership development trajectory

## Success Metrics & Impact

### Key Performance Indicators
- Quality and business impact of analytical insights and strategic recommendations
- Stakeholder satisfaction scores and cross-functional collaboration effectiveness
- Contribution to revenue growth, cost optimization, and operational efficiency
- Innovation in analytical methodologies and process improvement initiatives
- Professional development progress and team mentorship contributions

### Success Factors
- Customer-centric mindset with focus on value creation and impact
- Data-driven approach to decision making with strong analytical rigor
- Collaborative leadership style with effective stakeholder management
- Continuous learning orientation and adaptation to emerging technologies
- Results-focused execution with attention to quality and deadlines

## Company Culture & Environment

### Core Values & Principles
- Excellence and innovation in everything we do
- Customer obsession and market-focused solutions
- Integrity, transparency, and ethical business practices
- Diversity, equity, inclusion, and belonging for all employees
- Continuous learning, growth, and professional development

### Work Environment
- Fast-paced, dynamic culture with high growth opportunities
- Collaborative, inclusive workplace with global perspective
- Innovation-driven environment with access to cutting-edge technologies
- Entrepreneurial mindset with emphasis on ownership and accountability
- Strong commitment to work-life balance and employee well-being

## Global Impact & Opportunities

### Business Influence
- Drive strategic initiatives affecting millions of customers/users globally
- Shape product development and go-to-market strategies for key business areas
- Optimize operations and processes that impact company-wide performance
- Support international expansion and market development activities

### Innovation & Technology
- Work with emerging technologies including AI, machine learning, and automation
- Participate in digital transformation and technology adoption initiatives
- Collaborate with leading technology partners and industry innovators
- Contribute to thought leadership and industry best practice development

**Ready to drive business excellence and innovation?** Join {company_name} as a {role} and help shape the future while building an exceptional career with one of the world's leading organizations.

---

*{company_name} is an equal opportunity employer committed to creating an inclusive environment where all employees can thrive. We celebrate diversity and welcome applications from qualified candidates of all backgrounds.*"""

    return filename, content

def main():
    """Generate additional job descriptions"""
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    created_files = []
    
    for company_key, company_data in ADDITIONAL_COMPANIES.items():
        try:
            filename, content = generate_job_description(company_key, company_data)
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            created_files.append(filename)
            print(f"Created: {filename}")
            
        except Exception as e:
            print(f"Error creating job description for {company_key}: {e}")
    
    print(f"\nAdditional Report: Business Analyst Job Descriptions")
    print(f"Additional Files Generated: {len(created_files)}")
    print(f"Companies Added: {len(ADDITIONAL_COMPANIES)}")

if __name__ == "__main__":
    main()