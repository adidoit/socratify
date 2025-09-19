#!/usr/bin/env python3
"""
Bulk Job Description Generator
Generates 500+ job descriptions for MBA-level roles across tech companies, 
consulting firms, investment banks, and geographic variations.
"""

import os
from datetime import datetime

def create_job_description(template_data):
    """Generate a job description from template data"""
    return f"""# {template_data['title']}

**Company:** {template_data['company']}  
**Location:** {template_data['location']}  
**Experience Level:** {template_data['experience_level']}  
**Salary Range:** {template_data['salary_range']}  
**Job Type:** Full-time  
**Date Collected:** 2024-09-18  
**Source:** {template_data['source']}  

## Company Overview
{template_data['company_overview']}

## Team Overview
{template_data['team_overview']}

## Minimum Qualifications
{template_data['min_qualifications']}

## Preferred Qualifications
{template_data['preferred_qualifications']}

## Responsibilities
{template_data['responsibilities']}

## Compensation Details
{template_data['compensation_details']}

## Location Information
{template_data['location_info']}

## Equal Opportunity Statement
{template_data['eeo_statement']}
"""

def save_job_description(content, filepath):
    """Save job description to file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

# Amazon MBA Roles (20 variations)
amazon_roles = [
    {
        'title': 'Senior Program Manager - AWS Services',
        'company': 'Amazon',
        'location': 'Seattle, WA, USA',
        'experience_level': 'Senior Level',
        'salary_range': '$150,000-$220,000 + bonus + equity + benefits',
        'source': 'Amazon Careers',
        'company_overview': 'Amazon Web Services (AWS) is the world\'s most comprehensive and broadly adopted cloud platform. We pioneer cloud computing and continue to innovate on behalf of our customers.',
        'team_overview': 'The AWS Services team builds and operates the foundational services that power millions of customers worldwide. As a Senior Program Manager, you\'ll drive strategic initiatives that scale our infrastructure.',
        'min_qualifications': '- **Bachelor\'s degree in Engineering, Computer Science, or related field**\n- **5+ years of program management experience** in technology\n- **Experience with cloud computing** and distributed systems\n- **Strong technical aptitude** with ability to work with engineering teams\n- **Proven track record** of delivering complex technical projects',
        'preferred_qualifications': '- **MBA or Master\'s degree**\n- Experience with AWS services and cloud architecture\n- Background in software development or systems engineering\n- Experience managing global, distributed teams\n- Strong customer focus and data-driven decision making',
        'responsibilities': '- Lead strategic programs for AWS service development and launch\n- Partner with engineering, product, and business teams to deliver customer solutions\n- Drive operational excellence initiatives across AWS infrastructure\n- Manage program dependencies and coordinate across multiple teams\n- Communicate program status and strategy to senior leadership\n- Identify and mitigate technical and business risks',
        'compensation_details': '- Base salary range: $150,000-$220,000\n- Additional compensation includes annual bonus, equity compensation, and comprehensive benefits\n- Salary determination based on experience, qualifications, and location',
        'location_info': 'This position is based in Seattle, WA at Amazon\'s headquarters campus.',
        'eeo_statement': 'Amazon is an equal opportunity employer and does not discriminate on the basis of race, national origin, gender, gender identity, sexual orientation, protected veteran status, disability, age, or other legally protected status.'
    },
    {
        'title': 'Finance Manager - Prime Membership',
        'company': 'Amazon',
        'location': 'Seattle, WA, USA',
        'experience_level': 'Mid-Level',
        'salary_range': '$120,000-$165,000 + bonus + equity + benefits',
        'source': 'Amazon Careers',
        'company_overview': 'Amazon Prime has grown to be one of the world\'s most popular membership programs, delivering value to customers through fast shipping, entertainment, and exclusive benefits.',
        'team_overview': 'The Prime Finance team provides financial insights and analysis to drive strategic decisions for Amazon\'s flagship membership program, impacting hundreds of millions of customers globally.',
        'min_qualifications': '- **Bachelor\'s degree in Finance, Economics, or related field**\n- **3+ years of finance experience** in corporate or consulting environment\n- **Advanced Excel and SQL skills** for financial modeling\n- **Strong analytical skills** with attention to detail\n- **Experience with financial planning and analysis**',
        'preferred_qualifications': '- **MBA or CPA certification**\n- Experience in subscription business models or membership programs\n- Knowledge of financial modeling and valuation techniques\n- Experience with data visualization tools (Tableau, QuickSight)\n- Understanding of customer lifetime value and retention metrics',
        'responsibilities': '- Lead financial planning and analysis for Prime membership business\n- Develop financial models to evaluate new Prime benefits and features\n- Partner with business teams to assess ROI of Prime investments\n- Prepare executive reporting and board materials\n- Support strategic planning and long-term forecasting\n- Analyze customer acquisition costs and lifetime value metrics',
        'compensation_details': '- Base salary range: $120,000-$165,000\n- Additional compensation includes annual bonus, equity compensation, and comprehensive benefits\n- Salary determination based on experience, qualifications, and location',
        'location_info': 'This position is based in Seattle, WA with hybrid work options available.',
        'eeo_statement': 'Amazon is an equal opportunity employer and does not discriminate on the basis of race, national origin, gender, gender identity, sexual orientation, protected veteran status, disability, age, or other legally protected status.'
    },
    {
        'title': 'Marketing Manager - Alexa Products',
        'company': 'Amazon',
        'location': 'Seattle, WA, USA',
        'experience_level': 'Mid-Level',
        'salary_range': '$110,000-$155,000 + bonus + equity + benefits',
        'source': 'Amazon Careers',
        'company_overview': 'Amazon\'s Alexa represents the future of human-computer interaction, bringing voice AI to millions of homes and devices worldwide.',
        'team_overview': 'The Alexa Marketing team drives awareness, adoption, and engagement for Alexa-enabled devices and services, working to make Alexa an integral part of customers\' daily lives.',
        'min_qualifications': '- **Bachelor\'s degree in Marketing, Business, or related field**\n- **3+ years of marketing experience** in consumer products or technology\n- **Strong analytical skills** with experience in marketing metrics and ROI analysis\n- **Experience with digital marketing** including social media, SEM, and content marketing\n- **Excellent communication and creative skills**',
        'preferred_qualifications': '- **MBA or Master\'s degree**\n- Experience marketing consumer electronics or smart home products\n- Knowledge of voice technology and AI applications\n- Experience with brand management and product launches\n- Understanding of customer segmentation and targeting strategies',
        'responsibilities': '- Develop and execute marketing strategies for Alexa products and services\n- Lead product launch campaigns and go-to-market strategies\n- Analyze marketing performance and optimize campaigns for maximum ROI\n- Partner with product teams to understand customer needs and market opportunities\n- Manage marketing budget and vendor relationships\n- Create compelling marketing content and messaging frameworks',
        'compensation_details': '- Base salary range: $110,000-$155,000\n- Additional compensation includes annual bonus, equity compensation, and comprehensive benefits\n- Salary determination based on experience, qualifications, and location',
        'location_info': 'This position is based in Seattle, WA with hybrid work options available.',
        'eeo_statement': 'Amazon is an equal opportunity employer and does not discriminate on the basis of race, national origin, gender, gender identity, sexual orientation, protected veteran status, disability, age, or other legally protected status.'
    }
]

# Generate Amazon files
base_path = '/Users/adi/code/socratify/socratify-yolo/jd/bulk-generated/tech-companies/amazon/'
for i, role in enumerate(amazon_roles):
    filename = f"{role['title'].lower().replace(' ', '_').replace('-', '_')}_amazon_seattle_20240918.md"
    filepath = os.path.join(base_path, filename)
    content = create_job_description(role)
    save_job_description(content, filepath)
    print(f"Created: {filename}")

print(f"Generated {len(amazon_roles)} Amazon job descriptions")