#!/usr/bin/env python3
"""
Comprehensive Bulk Job Description Generator
Generates 500+ job descriptions for MBA-level roles across:
- Tech companies (Amazon, Google, Microsoft, Meta, Apple)
- Consulting firms (McKinsey, BCG, Bain, Deloitte) 
- Investment banks (Goldman Sachs, JPMorgan, Morgan Stanley)
- Geographic variations
"""

import os
import json
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

# Company templates
company_templates = {
    'amazon': {
        'company_overview': 'Amazon is Earth\'s Most Customer-Centric Company, where customers can find and discover anything they might want to buy online. Amazon\'s evolution from website to e-commerce partner to development platform is driven by the spirit of innovation that is part of the company\'s DNA.',
        'eeo_statement': 'Amazon is an equal opportunity employer and does not discriminate on the basis of race, national origin, gender, gender identity, sexual orientation, protected veteran status, disability, age, or other legally protected status.',
        'source': 'Amazon Careers'
    },
    'google': {
        'company_overview': 'Google\'s mission is to organize the world\'s information and make it universally accessible and useful. Since 1998, Google has grown by leaps and bounds and continues to expand our reach and impact globally.',
        'eeo_statement': 'Google is proud to be an equal opportunity and affirmative action employer. We are committed to building a workforce that is representative of the users we serve, creating a culture of belonging, and providing an equal employment opportunity regardless of race, creed, color, religion, gender, sexual orientation, gender identity/expression, national origin, disability, age, genetic information, veteran status, marital status, pregnancy or related condition.',
        'source': 'Google Careers'
    },
    'microsoft': {
        'company_overview': 'At Microsoft, our mission is to empower every person and every organization on the planet to achieve more. We create technology that transforms the way people work, play, and connect across devices and platforms.',
        'eeo_statement': 'Microsoft is an equal opportunity employer. All qualified applicants will receive consideration for employment without regard to age, ancestry, color, family or medical care leave, gender identity or expression, genetic information, marital status, medical condition, national origin, physical or mental disability, political affiliation, protected veteran status, race, religion, sex (including pregnancy), sexual orientation, or any other characteristic protected by applicable laws.',
        'source': 'Microsoft Careers'
    },
    'meta': {
        'company_overview': 'Meta builds technologies that help people connect, find communities, and grow businesses. When Facebook launched in 2004, it changed the way people connect. Apps and services like Messenger, Instagram, WhatsApp, and Horizon are furthering our vision of social technology.',
        'eeo_statement': 'Meta is committed to providing reasonable accommodations for qualified individuals with disabilities and disabled veterans in our job application procedures. If you need assistance or an accommodation due to a disability, you may contact us at accommodations-ext@fb.com.',
        'source': 'Meta Careers'
    },
    'apple': {
        'company_overview': 'Apple revolutionized personal technology with the introduction of the Macintosh in 1984. Today, Apple leads the world in innovation with iPhone, iPad, Mac, Apple Watch, and Apple TV.',
        'eeo_statement': 'Apple is an equal opportunity employer that is committed to inclusion and diversity. We take affirmative action to ensure equal opportunity for all applicants without regard to race, color, religion, sex, sexual orientation, gender identity, national origin, disability, Veteran status, or other legally protected characteristics.',
        'source': 'Apple Careers'
    }
}

# Role templates for tech companies
tech_roles = [
    {
        'title_template': 'Senior Program Manager - {}',
        'specializations': ['Product Development', 'Operations', 'Strategy', 'Platform Engineering', 'Customer Experience'],
        'experience_level': 'Senior Level',
        'salary_range': '$150,000-$220,000 + bonus + equity + benefits',
        'team_overview_template': 'The {} team drives strategic initiatives that scale our operations and enhance customer satisfaction. As a Senior Program Manager, you\'ll lead cross-functional efforts to deliver impactful results.',
        'min_qualifications': '- **Bachelor\'s degree in Engineering, Business, or related field**\n- **5+ years of program management experience** in technology\n- **Experience leading cross-functional teams** and complex projects\n- **Strong analytical and problem-solving skills**\n- **Excellent communication and leadership abilities**',
        'preferred_qualifications': '- **MBA or Master\'s degree**\n- Experience in technology product development\n- Knowledge of Agile/Scrum methodologies\n- Background in data analysis and metrics-driven decision making\n- Experience with stakeholder management and executive communication',
        'responsibilities': '- Lead end-to-end program management for strategic initiatives\n- Collaborate with engineering, product, and business teams to deliver projects\n- Develop program roadmaps, timelines, and success metrics\n- Drive operational excellence and process improvements\n- Manage stakeholder expectations and communicate with leadership\n- Identify and mitigate program risks and dependencies'
    },
    {
        'title_template': 'Business Analyst - {}',
        'specializations': ['Operations', 'Finance', 'Strategy', 'Product Analytics', 'Marketing Analytics'],
        'experience_level': 'Mid-Level',
        'salary_range': '$95,000-$140,000 + bonus + equity + benefits',
        'team_overview_template': 'The {} team leverages data and analytics to drive business insights and strategic decision-making. As a Business Analyst, you\'ll work with large datasets to optimize operations and improve customer outcomes.',
        'min_qualifications': '- **Bachelor\'s degree in Business, Economics, Mathematics, or related field**\n- **2+ years of business analysis experience**\n- **Advanced Excel and SQL skills**\n- **Strong analytical and quantitative skills**\n- **Experience with data visualization tools**',
        'preferred_qualifications': '- **MBA or Master\'s degree in analytical field**\n- Experience with Python, R, or statistical programming\n- Knowledge of business intelligence and reporting tools\n- Understanding of statistical methods and A/B testing\n- Experience in technology or consulting industry',
        'responsibilities': '- Analyze complex datasets to identify trends and business opportunities\n- Create detailed reports and presentations for leadership\n- Partner with cross-functional teams to implement data-driven solutions\n- Develop and maintain key performance indicators and metrics\n- Conduct market research and competitive analysis\n- Support strategic planning initiatives with quantitative insights'
    },
    {
        'title_template': 'Marketing Manager - {}',
        'specializations': ['Product Marketing', 'Digital Marketing', 'Brand Marketing', 'Growth Marketing', 'Customer Marketing'],
        'experience_level': 'Mid-Level',
        'salary_range': '$110,000-$160,000 + bonus + equity + benefits',
        'team_overview_template': 'The {} Marketing team drives customer acquisition, engagement, and retention through data-driven marketing strategies. As a Marketing Manager, you\'ll lead campaigns that connect with customers and drive business growth.',
        'min_qualifications': '- **Bachelor\'s degree in Marketing, Business, or related field**\n- **3+ years of marketing experience** in technology or consumer products\n- **Experience with digital marketing** and analytics platforms\n- **Strong project management and communication skills**\n- **Data-driven approach** to marketing optimization',
        'preferred_qualifications': '- **MBA or Master\'s degree**\n- Experience with marketing automation and CRM platforms\n- Knowledge of SEO, SEM, and social media marketing\n- Understanding of customer segmentation and targeting\n- Experience with brand management and product launches',
        'responsibilities': '- Develop and execute comprehensive marketing strategies\n- Lead product launch campaigns and go-to-market plans\n- Analyze marketing performance and optimize for ROI\n- Manage marketing budget and vendor relationships\n- Create compelling content and messaging frameworks\n- Collaborate with product and sales teams on market positioning'
    },
    {
        'title_template': 'Finance Manager - {}',
        'specializations': ['Corporate Finance', 'FP&A', 'Business Finance', 'Strategic Finance', 'Operations Finance'],
        'experience_level': 'Mid-Level',
        'salary_range': '$120,000-$170,000 + bonus + equity + benefits',
        'team_overview_template': 'The {} Finance team provides strategic financial guidance and analysis to support business decision-making and growth initiatives across the organization.',
        'min_qualifications': '- **Bachelor\'s degree in Finance, Economics, or related field**\n- **3+ years of finance experience** in corporate or consulting environment\n- **Advanced financial modeling and Excel skills**\n- **Strong analytical and problem-solving abilities**\n- **Experience with financial planning and analysis**',
        'preferred_qualifications': '- **MBA or CPA certification**\n- Experience in technology industry or high-growth companies\n- Knowledge of financial systems and reporting tools\n- Understanding of business valuation and investment analysis\n- Experience with budget planning and variance analysis',
        'responsibilities': '- Lead financial planning and analysis for business units\n- Develop financial models and business cases for new initiatives\n- Partner with business teams to provide financial insights\n- Prepare executive reporting and board materials\n- Support M&A activities and strategic planning\n- Manage financial controls and compliance requirements'
    },
    {
        'title_template': 'Strategy Manager - {}',
        'specializations': ['Corporate Strategy', 'Business Development', 'Operations Strategy', 'Product Strategy', 'Market Strategy'],
        'experience_level': 'Mid to Senior Level',
        'salary_range': '$140,000-$190,000 + bonus + equity + benefits',
        'team_overview_template': 'The {} Strategy team drives long-term strategic planning and business development initiatives. As a Strategy Manager, you\'ll work on high-impact projects that shape the future direction of the company.',
        'min_qualifications': '- **Bachelor\'s degree in Business, Economics, or related field**\n- **4+ years of strategy consulting or corporate strategy experience**\n- **Strong analytical and strategic thinking skills**\n- **Experience with market research and competitive analysis**\n- **Excellent presentation and communication abilities**',
        'preferred_qualifications': '- **MBA from top-tier program**\n- Management consulting experience (McKinsey, BCG, Bain)\n- Experience in technology industry or digital transformation\n- Knowledge of business model innovation and platform strategies\n- Understanding of international markets and expansion strategies',
        'responsibilities': '- Lead strategic planning processes and long-term roadmap development\n- Conduct market analysis and competitive intelligence research\n- Evaluate new business opportunities and partnership strategies\n- Support M&A due diligence and integration activities\n- Present strategic recommendations to senior leadership\n- Monitor industry trends and emerging technology opportunities'
    }
]

def generate_tech_company_roles():
    """Generate all tech company role variations"""
    files_created = 0
    
    companies = ['amazon', 'google', 'microsoft', 'meta', 'apple']
    locations = {
        'amazon': 'Seattle, WA, USA',
        'google': 'Mountain View, CA, USA',
        'microsoft': 'Redmond, WA, USA', 
        'meta': 'Menlo Park, CA, USA',
        'apple': 'Cupertino, CA, USA'
    }
    
    for company in companies:
        for role_template in tech_roles:
            for specialization in role_template['specializations']:
                title = role_template['title_template'].format(specialization)
                team_overview = role_template['team_overview_template'].format(specialization)
                
                job_data = {
                    'title': title,
                    'company': company.title(),
                    'location': locations[company],
                    'experience_level': role_template['experience_level'],
                    'salary_range': role_template['salary_range'],
                    'source': company_templates[company]['source'],
                    'company_overview': company_templates[company]['company_overview'],
                    'team_overview': team_overview,
                    'min_qualifications': role_template['min_qualifications'],
                    'preferred_qualifications': role_template['preferred_qualifications'],
                    'responsibilities': role_template['responsibilities'],
                    'compensation_details': f'- Base salary range: {role_template["salary_range"].split(" +")[0]}\n- Additional compensation includes annual bonus, equity compensation, and comprehensive benefits\n- Salary determination based on experience, qualifications, and location',
                    'location_info': f'This position is based in {locations[company]} with hybrid work options available.',
                    'eeo_statement': company_templates[company]['eeo_statement']
                }
                
                # Create filename
                filename = f"{title.lower().replace(' ', '_').replace('-', '_')}_{company}_{locations[company].split(',')[0].lower().replace(' ', '_')}_20240918.md"
                filepath = f'/Users/adi/code/socratify/socratify-yolo/jd/bulk-generated/tech-companies/{company}/{filename}'
                
                # Generate and save
                content = create_job_description(job_data)
                save_job_description(content, filepath)
                files_created += 1
                
    return files_created

def generate_consulting_roles():
    """Generate consulting firm variations across multiple offices"""
    files_created = 0
    
    consulting_firms = {
        'mckinsey': {
            'full_name': 'McKinsey & Company',
            'overview': 'McKinsey & Company is a global management consulting firm that helps leading organizations across private, public, and social sectors solve their most important challenges.',
            'source': 'McKinsey Careers'
        },
        'bcg': {
            'full_name': 'Boston Consulting Group',
            'overview': 'Boston Consulting Group is a global consulting firm that partners with leaders in business and society to tackle their most challenging opportunities and drive transformation.',
            'source': 'BCG Careers'
        },
        'bain': {
            'full_name': 'Bain & Company',
            'overview': 'Bain & Company is a global consultancy that helps ambitious leaders navigate the future. We accelerate results by challenging conventional thinking and empowering bold leadership.',
            'source': 'Bain Careers'
        },
        'deloitte': {
            'full_name': 'Deloitte Consulting',
            'overview': 'Deloitte provides industry-leading audit, consulting, tax, and advisory services to many of the world\'s most admired brands, including nearly 90% of the Fortune 500.',
            'source': 'Deloitte Careers'
        }
    }
    
    offices = [
        ('New York, NY, USA', '$180,000-$250,000'),
        ('London, UK', '$120,000-$180,000'),
        ('Singapore', '$90,000-$140,000'),
        ('Tokyo, Japan', '$100,000-$150,000'),
        ('Sydney, Australia', '$110,000-$160,000'),
        ('Toronto, Canada', '$130,000-$190,000'),
        ('Paris, France', '$110,000-$160,000'),
        ('Munich, Germany', '$105,000-$155,000'),
        ('Hong Kong', '$115,000-$170,000'),
        ('São Paulo, Brazil', '$70,000-$120,000')
    ]
    
    consulting_roles = [
        {
            'title': 'Business Analyst',
            'experience_level': 'Entry Level',
            'team_overview': 'Our Business Analyst program provides recent graduates with intensive training and hands-on experience solving complex business problems for Fortune 500 clients.',
            'min_qualifications': '- **Bachelor\'s degree with exceptional academic record** (typically top 10% of class)\n- **Strong analytical and quantitative skills**\n- **Excellent communication and presentation abilities**\n- **Demonstrated leadership** through internships or extracurricular activities\n- **Ability to work effectively** in team environments',
            'preferred_qualifications': '- **Advanced degree or MBA preferred**\n- Previous consulting or analytical work experience\n- International experience or language skills\n- Strong technical skills including Excel and PowerPoint\n- Industry-specific knowledge or expertise',
            'responsibilities': '- Conduct comprehensive analysis of client business challenges\n- Develop data-driven recommendations and strategic solutions\n- Create compelling presentations for C-suite executives\n- Collaborate with cross-functional teams on client engagements\n- Support business development and proposal preparation\n- Participate in knowledge sharing and best practice development'
        },
        {
            'title': 'Associate Consultant',
            'experience_level': 'Mid-Level',
            'team_overview': 'Associate Consultants lead client workstreams and mentor junior team members while developing deep expertise in specific industries and functional areas.',
            'min_qualifications': '- **MBA from top-tier program** or equivalent experience\n- **2+ years of consulting or relevant industry experience**\n- **Proven track record** of client relationship management\n- **Strong project management** and leadership skills\n- **Expertise in specific industry** or functional area',
            'preferred_qualifications': '- **Advanced degree in relevant field**\n- Previous management consulting experience\n- Industry expertise in target sectors\n- International business experience\n- Fluency in multiple languages',
            'responsibilities': '- Lead client workstreams and manage project deliverables\n- Develop strategic recommendations and implementation plans\n- Mentor and develop junior team members\n- Build and maintain strong client relationships\n- Support business development and thought leadership\n- Drive knowledge sharing across the firm'
        },
        {
            'title': 'Senior Associate',
            'experience_level': 'Senior Level',
            'team_overview': 'Senior Associates serve as trusted advisors to client leadership teams and drive the development of innovative solutions to complex business challenges.',
            'min_qualifications': '- **MBA or advanced degree** with outstanding academic credentials\n- **4+ years of consulting experience** or equivalent\n- **Deep expertise** in specific industry or functional area\n- **Proven ability** to manage complex client relationships\n- **Strong business development** and thought leadership skills',
            'preferred_qualifications': '- **Top-tier MBA or PhD**\n- Previous consulting experience at tier-1 firm\n- Published thought leadership or industry recognition\n- International consulting experience\n- Specialization in emerging technology or digital transformation',
            'responsibilities': '- Serve as trusted advisor to C-suite executives\n- Design and lead complex transformation initiatives\n- Develop innovative frameworks and methodologies\n- Lead business development efforts and proposal preparation\n- Mentor and develop consulting talent\n- Drive thought leadership and knowledge creation'
        }
    ]
    
    for firm, firm_data in consulting_firms.items():
        for role in consulting_roles:
            for location, salary_range in offices:
                job_data = {
                    'title': role['title'],
                    'company': firm_data['full_name'],
                    'location': location,
                    'experience_level': role['experience_level'],
                    'salary_range': f'{salary_range} + bonus + benefits',
                    'source': firm_data['source'],
                    'company_overview': firm_data['overview'],
                    'team_overview': role['team_overview'],
                    'min_qualifications': role['min_qualifications'],
                    'preferred_qualifications': role['preferred_qualifications'],
                    'responsibilities': role['responsibilities'],
                    'compensation_details': f'- Base salary range: {salary_range}\n- Additional compensation includes performance bonus and comprehensive benefits\n- Salary determination based on experience, qualifications, and location',
                    'location_info': f'This position is based in {location} with travel requirements for client engagements.',
                    'eeo_statement': f'{firm_data["full_name"]} is an equal opportunity employer committed to diversity and inclusion.'
                }
                
                # Create filename
                location_code = location.split(',')[0].lower().replace(' ', '_')
                filename = f"{role['title'].lower().replace(' ', '_')}_{firm}_{location_code}_20240918.md"
                filepath = f'/Users/adi/code/socratify/socratify-yolo/jd/bulk-generated/consulting-firms/{firm}/{filename}'
                
                # Generate and save
                content = create_job_description(job_data)
                save_job_description(content, filepath)
                files_created += 1
                
    return files_created

def generate_investment_banking_roles():
    """Generate investment banking division-specific roles"""
    files_created = 0
    
    ib_firms = {
        'goldman_sachs': {
            'full_name': 'Goldman Sachs',
            'overview': 'Goldman Sachs is a leading global investment banking, securities and investment management firm that provides a wide range of financial services to a substantial and diversified client base.',
            'source': 'Goldman Sachs Careers'
        },
        'jpmorgan': {
            'full_name': 'JPMorgan Chase',
            'overview': 'JPMorgan Chase & Co. is a leading global financial services firm with assets of $3.7 trillion and operations worldwide.',
            'source': 'JPMorgan Careers'
        },
        'morgan_stanley': {
            'full_name': 'Morgan Stanley',
            'overview': 'Morgan Stanley is a leading global financial services firm providing a wide range of investment banking, securities, wealth management and investment management services.',
            'source': 'Morgan Stanley Careers'
        }
    }
    
    divisions = [
        ('Mergers & Acquisitions', 'M&A Advisory', '$175,000-$200,000'),
        ('Equity Capital Markets', 'ECM', '$170,000-$195,000'),
        ('Debt Capital Markets', 'DCM', '$170,000-$195,000'),
        ('Leveraged Finance', 'LevFin', '$175,000-$200,000'),
        ('Financial Institutions Group', 'FIG', '$175,000-$200,000')
    ]
    
    ib_roles = [
        {
            'title_template': 'Investment Banking Analyst - {}',
            'experience_level': 'Entry Level',
            'team_overview_template': 'The {} team provides strategic advisory services to corporations, financial institutions, and governments. As an Analyst, you\'ll work on high-profile transactions and gain exposure to senior executives.',
            'min_qualifications': '- **Bachelor\'s degree with outstanding academic record** (typically top 10% of class, 3.7+ GPA)\n- **Strong quantitative and analytical skills**\n- **Advanced proficiency in Microsoft Excel and PowerPoint**\n- **Exceptional attention to detail** and ability to work under pressure\n- **Excellent communication skills** and professional maturity',
            'preferred_qualifications': '- **Relevant internship experience** in investment banking or finance\n- **CFA Level I candidate** or planning to pursue designation\n- **Technical skills** including Bloomberg, Capital IQ, or FactSet\n- **International experience** and foreign language capabilities\n- **Leadership experience** through extracurricular activities',
            'responsibilities': '- Build comprehensive financial models for M&A transactions and capital markets deals\n- Perform valuation analyses using DCF, comparable companies, and precedent transactions\n- Prepare pitch books, offering memoranda, and other client materials\n- Conduct industry research and competitive analysis\n- Support senior bankers in client meetings and transaction execution\n- Coordinate due diligence processes and manage data rooms'
        },
        {
            'title_template': 'Investment Banking Associate - {}',
            'experience_level': 'Mid-Level',
            'team_overview_template': 'The {} team delivers sophisticated financial solutions to our most important clients. As an Associate, you\'ll lead transaction workstreams and mentor junior team members.',
            'min_qualifications': '- **MBA from top-tier program** with concentration in finance\n- **2+ years of investment banking** or relevant finance experience\n- **Strong leadership and project management skills**\n- **Deep understanding** of financial markets and valuation methodologies\n- **Proven ability** to manage multiple priorities and work effectively under pressure',
            'preferred_qualifications': '- **Previous investment banking analyst experience**\n- **CFA or MBA with finance concentration**\n- **Industry expertise** in specific sectors\n- **Client relationship management** experience\n- **Advanced technical skills** and knowledge of financial systems',
            'responsibilities': '- Lead transaction execution and manage client relationships\n- Oversee financial modeling and valuation analysis\n- Mentor and develop analyst team members\n- Prepare materials for client presentations and board meetings\n- Support business development and pitch preparation\n- Drive deal process management and coordinate with legal and other advisors'
        }
    ]
    
    locations = ['New York, NY, USA', 'London, UK', 'Hong Kong', 'Tokyo, Japan']
    
    for firm, firm_data in ib_firms.items():
        for division_name, division_code, salary_range in divisions:
            for role in ib_roles:
                for location in locations:
                    title = role['title_template'].format(division_code)
                    team_overview = role['team_overview_template'].format(division_name)
                    
                    job_data = {
                        'title': title,
                        'company': firm_data['full_name'],
                        'location': location,
                        'experience_level': role['experience_level'],
                        'salary_range': f'{salary_range} + bonus + benefits',
                        'source': firm_data['source'],
                        'company_overview': firm_data['overview'],
                        'team_overview': team_overview,
                        'min_qualifications': role['min_qualifications'],
                        'preferred_qualifications': role['preferred_qualifications'],
                        'responsibilities': role['responsibilities'],
                        'compensation_details': f'- Base salary range: {salary_range}\n- Additional compensation includes performance bonus (typically 50-100% of base)\n- Comprehensive benefits including health insurance and retirement plans',
                        'location_info': f'This position is based in {location} with opportunities for international assignments.',
                        'eeo_statement': f'{firm_data["full_name"]} is an equal opportunity employer committed to diversity and inclusion in the workplace.'
                    }
                    
                    # Create filename
                    location_code = location.split(',')[0].lower().replace(' ', '_')
                    filename = f"{title.lower().replace(' ', '_').replace('-', '_')}_{firm}_{location_code}_20240918.md"
                    filepath = f'/Users/adi/code/socratify/socratify-yolo/jd/bulk-generated/investment-banking/{firm}/{filename}'
                    
                    # Generate and save
                    content = create_job_description(job_data)
                    save_job_description(content, filepath)
                    files_created += 1
                    
    return files_created

def generate_geographic_variations():
    """Generate geographic variations for common MBA roles"""
    files_created = 0
    
    # Common MBA roles with geographic variations
    geographic_roles = [
        {
            'title': 'Product Manager',
            'experience_level': 'Mid-Level',
            'team_overview': 'Our Product Management team drives innovation and customer-centric product development across global markets.',
            'min_qualifications': '- **Bachelor\'s degree in Engineering, Business, or related field**\n- **3+ years of product management experience**\n- **Strong analytical and technical skills**\n- **Experience with agile development methodologies**\n- **Excellent communication and leadership abilities**',
            'preferred_qualifications': '- **MBA or Master\'s degree**\n- Experience in technology product development\n- Knowledge of user experience design principles\n- Understanding of data analytics and A/B testing\n- Previous startup or high-growth company experience',
            'responsibilities': '- Define product strategy and roadmap based on market research and customer insights\n- Collaborate with engineering teams to deliver high-quality products\n- Analyze product performance metrics and user feedback\n- Work with design teams to create intuitive user experiences\n- Coordinate with marketing and sales teams on product launches\n- Manage product lifecycle from conception to retirement'
        },
        {
            'title': 'Management Consultant',
            'experience_level': 'Mid-Level',
            'team_overview': 'Our Consulting team helps organizations solve complex business challenges and drive transformation across industries.',
            'min_qualifications': '- **Bachelor\'s degree with strong academic record**\n- **2+ years of consulting or analytical experience**\n- **Strong problem-solving and analytical skills**\n- **Excellent presentation and communication abilities**\n- **Ability to work effectively with senior executives**',
            'preferred_qualifications': '- **MBA from top-tier program**\n- Previous management consulting experience\n- Industry expertise in specific sectors\n- International business experience\n- Advanced skills in data analysis and modeling',
            'responsibilities': '- Lead client engagements and develop strategic recommendations\n- Conduct market research and competitive analysis\n- Build financial models and business cases\n- Present findings and recommendations to client leadership\n- Manage project timelines and deliverables\n- Mentor junior team members and support business development'
        },
        {
            'title': 'Business Development Manager',
            'experience_level': 'Mid-Level',
            'team_overview': 'Our Business Development team identifies and pursues strategic partnerships and growth opportunities in local and international markets.',
            'min_qualifications': '- **Bachelor\'s degree in Business or related field**\n- **3+ years of business development or sales experience**\n- **Strong relationship building and negotiation skills**\n- **Experience with partnership development**\n- **Excellent communication and presentation abilities**',
            'preferred_qualifications': '- **MBA or Master\'s degree**\n- Experience in technology or consulting industry\n- Knowledge of local market dynamics and regulations\n- Previous startup or entrepreneurial experience\n- Fluency in local language and cultural understanding',
            'responsibilities': '- Identify and evaluate new business opportunities and partnerships\n- Develop and execute business development strategies\n- Build relationships with key industry partners and stakeholders\n- Negotiate contracts and partnership agreements\n- Collaborate with product and marketing teams on go-to-market strategies\n- Monitor market trends and competitive landscape'
        }
    ]
    
    # Geographic locations with local market characteristics
    locations = [
        ('San Francisco, CA, USA', '$140,000-$190,000', 'Technology Hub'),
        ('New York, NY, USA', '$130,000-$180,000', 'Financial Center'),
        ('Seattle, WA, USA', '$125,000-$175,000', 'Innovation Center'),
        ('Austin, TX, USA', '$110,000-$160,000', 'Emerging Tech Hub'),
        ('London, UK', '$90,000-$140,000', 'European Headquarters'),
        ('Toronto, Canada', '$95,000-$145,000', 'North American Hub'),
        ('Singapore', '$80,000-$130,000', 'Asia-Pacific Center'),
        ('Hong Kong', '$95,000-$145,000', 'Asian Financial Hub'),
        ('Mumbai, India', '$40,000-$80,000', 'Innovation Center'),
        ('Dubai, UAE', '$85,000-$135,000', 'Middle East Hub'),
        ('Tokyo, Japan', '$90,000-$140,000', 'Japanese Headquarters'),
        ('Sydney, Australia', '$85,000-$135,000', 'Pacific Region Hub')
    ]
    
    companies = ['TechGlobal Corp', 'InnovateGlobal', 'GlobalConsulting Partners', 'NextGen Solutions', 'FutureScale International']
    
    for role in geographic_roles:
        for location, salary_range, market_desc in locations:
            for company in companies:
                job_data = {
                    'title': role['title'],
                    'company': company,
                    'location': location,
                    'experience_level': role['experience_level'],
                    'salary_range': f'{salary_range} + bonus + benefits',
                    'source': f'{company} Careers',
                    'company_overview': f'{company} is a leading global technology company that delivers innovative solutions to enterprises worldwide. We operate in {market_desc.lower()} with a focus on driving digital transformation.',
                    'team_overview': role['team_overview'],
                    'min_qualifications': role['min_qualifications'],
                    'preferred_qualifications': role['preferred_qualifications'],
                    'responsibilities': role['responsibilities'],
                    'compensation_details': f'- Base salary range: {salary_range}\n- Additional compensation includes performance bonus and comprehensive benefits\n- Salary adjusted for local market conditions and cost of living',
                    'location_info': f'This position is based in {location}, a key {market_desc.lower()} for our global operations.',
                    'eeo_statement': f'{company} is an equal opportunity employer committed to building a diverse and inclusive workforce.'
                }
                
                # Create filename
                location_code = location.split(',')[0].lower().replace(' ', '_')
                company_code = company.lower().replace(' ', '_').replace('.', '')
                filename = f"{role['title'].lower().replace(' ', '_')}_{company_code}_{location_code}_20240918.md"
                filepath = f'/Users/adi/code/socratify/socratify-yolo/jd/bulk-generated/geographic-variations/{filename}'
                
                # Generate and save
                content = create_job_description(job_data)
                save_job_description(content, filepath)
                files_created += 1
                
    return files_created

def main():
    """Generate all job descriptions"""
    total_files = 0
    
    print("Starting bulk job description generation...")
    print("=" * 50)
    
    # Phase 1: Tech companies
    print("PHASE 1: Generating tech company MBA role variations...")
    tech_files = generate_tech_company_roles()
    total_files += tech_files
    print(f"Generated {tech_files} tech company job descriptions")
    
    # Phase 2: Consulting firms  
    print("\nPHASE 2: Generating consulting firm office variations...")
    consulting_files = generate_consulting_roles()
    total_files += consulting_files
    print(f"Generated {consulting_files} consulting firm job descriptions")
    
    # Phase 3: Investment banking
    print("\nPHASE 3: Generating investment banking division roles...")
    ib_files = generate_investment_banking_roles()
    total_files += ib_files
    print(f"Generated {ib_files} investment banking job descriptions")
    
    # Phase 4: Geographic variations
    print("\nPHASE 4: Generating geographic role variations...")
    geo_files = generate_geographic_variations()
    total_files += geo_files
    print(f"Generated {geo_files} geographic variation job descriptions")
    
    print("=" * 50)
    print(f"TOTAL FILES GENERATED: {total_files}")
    print("Bulk generation complete!")
    
    return total_files

if __name__ == "__main__":
    main()