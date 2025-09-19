#!/usr/bin/env python3
"""
Batch generator for comprehensive data scientist job descriptions
Covers all major company categories and specializations
"""

import os
from datetime import datetime

def create_job_description(company, role, location, salary_range, department, description_content):
    """Create a comprehensive job description file"""
    
    filename = f"{company.lower().replace(' ', '-').replace('.', '').replace('&', 'and')}-{role.lower().replace(' ', '-').replace('/', '-')}-{location.lower().replace(' ', '-').replace(',', '')}-2024.md"
    
    content = f"""# {role} - {company}
## {location} | Full-time | 2024

**Company:** {company}  
**Department:** {department}  
**Location:** {location}  
**Salary Range:** {salary_range}  
**Posted:** September 2024

{description_content}

---
*{company} is an equal opportunity employer committed to diversity and inclusion.*"""

    filepath = f"/Users/adi/code/socratify/socratify-yolo/jd/data-scientist/{filename}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

# Define job descriptions data
job_descriptions = [
    # Big Tech Additional Roles
    {
        "company": "Apple",
        "role": "Senior Machine Learning Engineer, Siri",
        "location": "Cupertino, CA",
        "salary_range": "$320,000 - $550,000 (ICT4-ICT5)",
        "department": "Machine Learning and AI",
        "content": """### About Apple ML & AI
Apple's Machine Learning and AI team creates intelligent experiences that delight millions of users worldwide. From Siri to computational photography, we're advancing the state-of-the-art in on-device AI and privacy-preserving machine learning.

### Role Overview
Join Apple's Siri team to build the next generation of conversational AI experiences. You'll develop ML models that understand user intent, generate natural responses, and provide personalized assistance while maintaining Apple's commitment to privacy and on-device processing.

### Key Responsibilities
- **Conversational AI**: Develop advanced NLU and dialogue management systems
- **On-Device ML**: Optimize models for iOS devices with strict latency and power constraints
- **Privacy-First**: Implement differential privacy and federated learning techniques
- **Multimodal Integration**: Combine voice, text, and visual understanding
- **Performance Optimization**: Achieve real-time inference on mobile hardware
- **Cross-functional Collaboration**: Work with design, product, and engineering teams

### Technical Focus Areas
- **Natural Language Understanding**: Intent classification, entity extraction, context tracking
- **Speech Processing**: ASR improvements, voice activity detection, speaker recognition
- **Personal Intelligence**: User behavior modeling with privacy preservation
- **Knowledge Integration**: Structured knowledge graphs and reasoning
- **Edge AI**: Model quantization, pruning, and hardware acceleration
- **Evaluation**: Comprehensive testing frameworks for conversational AI

### Required Qualifications
- **Education**: MS/PhD in Computer Science, Machine Learning, or related field
- **Experience**: 5+ years in ML with focus on NLP or speech processing
- **Mobile Optimization**: Experience with on-device ML and resource constraints
- **Programming**: Expert Python, Swift/Objective-C, C++, and ML frameworks
- **Privacy Awareness**: Understanding of privacy-preserving ML techniques
- **Product Impact**: Track record of shipping ML features to millions of users

### What We Offer
- **Total Compensation**: $320K-$550K including base, equity, and bonuses
- **Apple Stock**: RSUs with strong historical performance and growth potential
- **Innovation Environment**: Work on products used by over 1 billion people
- **Privacy Leadership**: Pioneer privacy-preserving AI techniques
- **Hardware Integration**: Close collaboration with world-class hardware teams
- **Global Impact**: Shape the future of human-computer interaction"""
    },
    
    # Netflix
    {
        "company": "Netflix",
        "role": "Senior Data Scientist, Algorithms",
        "location": "Los Gatos, CA",
        "salary_range": "$300,000 - $500,000 (L5-L6)",
        "department": "Algorithms Engineering",
        "content": """### About Netflix Algorithms
Netflix's Algorithms team is responsible for the recommendation systems that help 250+ million members discover content they love. We develop ML systems that personalize the Netflix experience, optimize content creation decisions, and drive member engagement.

### Role Overview
As a Senior Data Scientist on the Algorithms team, you'll develop recommendation systems and personalization algorithms that directly impact member satisfaction and retention. You'll work with massive datasets to understand viewing behavior and create ML models that improve content discovery.

### Key Responsibilities
- **Recommendation Systems**: Develop and improve Netflix's core recommendation algorithms
- **A/B Testing**: Design experiments to measure algorithm impact on member behavior
- **Personalization**: Create personalized experiences across different contexts and devices
- **Content Analytics**: Analyze viewing patterns to inform content strategy
- **Ranking Optimization**: Optimize ranking algorithms for different surfaces (homepage, search)
- **Causal Inference**: Apply causal methods to understand member behavior drivers

### Technical Specializations
- **Collaborative Filtering**: Advanced matrix factorization and deep learning approaches
- **Content Understanding**: Computer vision and NLP for content analysis
- **Multi-Armed Bandits**: Online learning for personalization and optimization
- **Deep Learning**: Neural networks for recommendation and ranking
- **Real-time Systems**: Low-latency inference for 250M+ members
- **Evaluation**: Offline and online evaluation frameworks for recommendations

### Required Qualifications
- **Education**: PhD in Computer Science, Statistics, or related quantitative field
- **Experience**: 5+ years in ML/data science with recommender systems experience
- **Large Scale**: Experience with ML systems serving millions of users
- **Statistics**: Strong background in experimental design and causal inference
- **Programming**: Expert Python, Scala, and distributed computing (Spark)
- **Business Impact**: Track record of algorithm improvements driving user engagement

### What We Offer
- **Total Compensation**: $300K-$500K including base salary, bonuses, and stock options
- **Creative Environment**: Influence content creation and member experience
- **Global Scale**: Impact entertainment for 250+ million members worldwide
- **Data Resources**: Access to unique, large-scale viewing behavior datasets
- **Innovation**: Freedom to explore novel approaches to recommendation problems
- **Flexible Culture**: Netflix's culture of freedom and responsibility"""
    },

    # Traditional Companies
    {
        "company": "Walmart",
        "role": "Principal Data Scientist, Supply Chain ML",
        "location": "Bentonville, AR",
        "salary_range": "$250,000 - $400,000 (Principal level)",
        "department": "Global Tech - Supply Chain",
        "content": """### About Walmart Global Tech
Walmart Global Tech is reimagining retail through technology innovation. Our supply chain ML team develops AI solutions that optimize the world's largest retail supply chain, serving 240 million customers weekly across 10,000+ stores globally.

### Role Overview
Lead the development of ML solutions that optimize Walmart's massive supply chain operations. You'll work on forecasting, inventory optimization, logistics planning, and automated decision-making systems that impact billions in revenue and ensure product availability for customers.

### Key Responsibilities
- **Demand Forecasting**: Develop ML models predicting customer demand across millions of SKUs
- **Inventory Optimization**: Create algorithms for optimal inventory levels and replenishment
- **Logistics Planning**: Optimize transportation routes, warehouse operations, and delivery
- **Supplier Analytics**: ML solutions for supplier performance and risk assessment
- **Real-time Operations**: Build systems for real-time supply chain decision making
- **Cross-functional Leadership**: Partner with operations, merchandising, and technology teams

### Technical Focus Areas
- **Time Series Forecasting**: Advanced forecasting models for demand planning
- **Optimization**: Linear programming, mixed-integer optimization for logistics
- **Causal Inference**: Understanding the impact of promotions, seasonality, and external factors
- **Computer Vision**: Image recognition for warehouse automation and quality control
- **IoT Analytics**: Sensor data analysis for fleet management and asset tracking
- **Graph Neural Networks**: Modeling complex supplier and transportation networks

### Required Qualifications
- **Education**: PhD in Operations Research, Statistics, Computer Science, or related field
- **Experience**: 8+ years in data science with supply chain or operations focus
- **Optimization**: Strong background in mathematical optimization and operations research
- **Scale**: Experience with enterprise-scale systems and billions of data points
- **Business Acumen**: Deep understanding of retail operations and supply chain management
- **Leadership**: Experience leading technical teams and cross-functional initiatives

### What We Offer
- **Total Compensation**: $250K-$400K including base, bonuses, and stock awards
- **Massive Impact**: Optimize operations serving 240M+ customers weekly
- **Innovation Budget**: Resources for cutting-edge ML research and development
- **Global Reach**: Work on supply chain challenges across international markets
- **Sustainability**: Contribute to Walmart's environmental and social impact goals
- **Career Growth**: Clear advancement paths within Walmart's technology organization"""
    },

    # Canadian Companies
    {
        "company": "Shopify",
        "role": "Staff Data Scientist, Merchant Intelligence",
        "location": "Ottawa, ON",
        "salary_range": "CAD $280,000 - $450,000 (Staff level)",
        "department": "Data Science & Engineering",
        "content": """### About Shopify Data Science
Shopify powers over 2 million merchants worldwide, from small businesses to Fortune 500 companies. Our Data Science team builds ML systems that help merchants succeed through intelligent insights, automated decisions, and personalized experiences.

### Role Overview
As a Staff Data Scientist focusing on Merchant Intelligence, you'll develop ML systems that help merchants grow their businesses. You'll work on product recommendations, demand forecasting, fraud detection, and business intelligence tools that directly impact merchant success and revenue.

### Key Responsibilities
- **Merchant Analytics**: Build ML models to provide actionable business insights to merchants
- **Demand Forecasting**: Develop forecasting systems for inventory and capacity planning
- **Fraud Detection**: Create real-time fraud detection systems protecting merchants and customers
- **Product Intelligence**: ML-powered product recommendations and catalog optimization
- **Growth Analytics**: Identify opportunities for merchant growth and expansion
- **Platform Innovation**: Contribute to Shopify's ML platform and infrastructure

### Technical Specializations
- **E-commerce Analytics**: Deep understanding of online retail metrics and behavior
- **Time Series**: Advanced forecasting for seasonal and trend-based patterns
- **Recommendation Systems**: Product and customer matching algorithms
- **Anomaly Detection**: Identifying unusual patterns in merchant and customer behavior
- **Natural Language Processing**: Product description optimization and search
- **A/B Testing**: Experimental design for product and algorithm validation

### Required Qualifications
- **Education**: PhD in Computer Science, Statistics, Economics, or related field
- **Experience**: 7+ years in data science with e-commerce or marketplace experience
- **Product Sense**: Strong understanding of product development and user experience
- **Technical Leadership**: Experience leading technical initiatives and mentoring teams
- **Business Impact**: Track record of ML solutions driving measurable business outcomes
- **Communication**: Excellent presentation skills for executive and merchant audiences

### What We Offer
- **Total Compensation**: CAD $280K-$450K including base, equity, and performance bonuses
- **Remote-First**: Distributed team culture with flexible work arrangements
- **Impact**: Directly influence the success of 2M+ merchants globally
- **Growth Stage**: Join a rapidly growing company with international expansion
- **Innovation**: Access to cutting-edge ML infrastructure and datasets
- **Canadian Benefits**: Comprehensive health benefits and RRSP matching"""
    },

    # European Companies
    {
        "company": "Spotify",
        "role": "Senior ML Engineer, Music Understanding",
        "location": "Stockholm, Sweden",
        "salary_range": "€180,000 - €300,000 (Senior level)",
        "department": "ML Platform - Music Understanding",
        "content": """### About Spotify ML
Spotify uses machine learning to create the world's most personalized audio experience for 500+ million users. Our Music Understanding team develops ML systems that analyze audio content, understand user preferences, and power recommendation systems.

### Role Overview
Join Spotify's Music Understanding team to build ML systems that comprehend music at scale. You'll work on audio analysis, content tagging, similarity modeling, and recommendation systems that help users discover their next favorite song from 100+ million tracks.

### Key Responsibilities
- **Audio ML**: Develop deep learning models for music analysis and understanding
- **Content Intelligence**: Build systems for automatic music tagging and classification
- **Recommendation Systems**: Create algorithms that match users with relevant music content
- **Real-time Processing**: Deploy models processing millions of audio streams daily
- **Research Innovation**: Advance the state-of-the-art in music information retrieval
- **Global Scale**: Build systems serving 500M+ users across 180+ markets

### Technical Focus Areas
- **Audio Signal Processing**: Spectral analysis, feature extraction, and audio preprocessing
- **Deep Learning**: CNNs and transformers for audio understanding and generation
- **Music Information Retrieval**: Similarity, genre classification, and mood detection
- **Embedding Learning**: Learning representations for tracks, artists, and user preferences
- **Multi-modal Learning**: Combining audio, text, and behavioral signals
- **Scalable Inference**: Real-time audio analysis and recommendation serving

### Required Qualifications
- **Education**: MS/PhD in Computer Science, Electrical Engineering, or related field
- **Experience**: 5+ years in ML with focus on audio, music, or signal processing
- **Audio Expertise**: Deep understanding of digital signal processing and audio analysis
- **Deep Learning**: Extensive experience with neural networks for audio applications
- **Production Systems**: Experience deploying ML models at consumer internet scale
- **Research**: Publications in audio ML, MIR, or related conferences preferred

### What We Offer
- **Total Compensation**: €180K-€300K including base, equity, and comprehensive benefits
- **Creative Impact**: Shape how millions discover and experience music
- **Research Freedom**: 10% time for personal research and experimentation
- **Global Platform**: Work with diverse, international team across multiple time zones
- **Innovation**: Access to unique audio datasets and cutting-edge ML infrastructure
- **Swedish Benefits**: Excellent work-life balance and comprehensive social benefits"""
    },

    # Indian Companies
    {
        "company": "Flipkart",
        "role": "Principal Data Scientist, Recommendations",
        "location": "Bangalore, India",
        "salary_range": "₹80,00,000 - ₹1,50,00,000 (Principal level)",
        "department": "Machine Learning Platform",
        "content": """### About Flipkart ML
Flipkart is India's leading e-commerce platform, serving 450+ million customers with AI-powered experiences. Our ML team builds recommendation systems, search algorithms, and personalization engines that drive discovery and engagement across India's diverse market.

### Role Overview
Lead the development of next-generation recommendation systems for Flipkart's e-commerce platform. You'll work on large-scale ML systems that understand customer preferences, predict demand, and optimize the shopping experience for India's rapidly growing digital commerce market.

### Key Responsibilities
- **Recommendation Systems**: Design and scale ML algorithms for product recommendations
- **Search & Discovery**: Improve search relevance and product discovery algorithms
- **Personalization**: Create personalized shopping experiences across mobile and web
- **Regional Adaptation**: Develop ML solutions for India's diverse languages and cultures
- **Business Intelligence**: Build analytics systems for category managers and business teams
- **Platform Development**: Contribute to Flipkart's ML infrastructure and tools

### Technical Specializations
- **Deep Learning**: Neural collaborative filtering and deep recommendation models
- **Natural Language Processing**: Multi-lingual search and content understanding
- **Computer Vision**: Visual search and image-based product matching
- **Real-time Systems**: Low-latency inference for personalized recommendations
- **Causal Inference**: Understanding the impact of recommendations on purchase behavior
- **Fraud Detection**: ML systems for payment security and seller verification

### Required Qualifications
- **Education**: MTech/PhD in Computer Science, Statistics, or related field
- **Experience**: 8+ years in data science with e-commerce or marketplace experience
- **Large Scale**: Experience with ML systems serving millions of users daily
- **Indian Market**: Understanding of Indian consumer behavior and market dynamics
- **Technical Leadership**: Experience leading data science teams and initiatives
- **Business Impact**: Track record of ML solutions driving revenue and engagement

### What We Offer
- **Total Compensation**: ₹80L-₹1.5Cr including base, bonuses, and equity
- **Market Leadership**: Work for India's leading e-commerce platform
- **Scale Impact**: Influence shopping experience for 450M+ customers
- **Innovation**: Access to cutting-edge ML infrastructure and diverse datasets
- **Career Growth**: Clear advancement paths within Flipkart and Walmart Global Tech
- **India Focus**: Build solutions specifically for Indian market needs and preferences"""
    },

    # Fintech Startups
    {
        "company": "Robinhood",
        "role": "Senior Quantitative Researcher",
        "location": "Menlo Park, CA",
        "salary_range": "$300,000 - $500,000 (L5-L6)",
        "department": "Quantitative Research",
        "content": """### About Robinhood Quant
Robinhood is democratizing finance for all through commission-free investing and accessible financial products. Our Quantitative Research team develops ML models for risk management, algorithmic trading, portfolio optimization, and market microstructure analysis.

### Role Overview
Join Robinhood's Quantitative Research team to build ML systems that power our trading platform and investment products. You'll work on market prediction models, risk management systems, and algorithmic trading strategies that serve millions of retail investors.

### Key Responsibilities
- **Quantitative Modeling**: Develop statistical models for market prediction and risk assessment
- **Algorithmic Trading**: Build execution algorithms and market making strategies
- **Risk Management**: Create real-time risk monitoring and position management systems
- **Market Research**: Analyze market microstructure and retail investor behavior
- **Product Analytics**: Support product development with quantitative insights
- **Regulatory Compliance**: Ensure models meet financial regulatory requirements

### Technical Focus Areas
- **Time Series Analysis**: Market prediction and volatility modeling
- **Portfolio Optimization**: Risk-adjusted return optimization for customer portfolios
- **Market Microstructure**: Order flow analysis and execution optimization
- **Behavioral Finance**: Understanding and modeling retail investor behavior
- **Real-time Risk**: Low-latency risk monitoring and automated controls
- **Alternative Data**: Integration of non-traditional data sources for alpha generation

### Required Qualifications
- **Education**: PhD in Finance, Economics, Statistics, Physics, or related quantitative field
- **Experience**: 5+ years in quantitative finance with focus on equity markets
- **Programming**: Expert Python, R, SQL, and statistical computing
- **Financial Markets**: Deep understanding of equity markets, options, and derivatives
- **Statistics**: Advanced knowledge of time series analysis and statistical modeling
- **Regulatory**: Understanding of SEC, FINRA, and other financial regulations

### What We Offer
- **Total Compensation**: $300K-$500K including base, equity, and performance bonuses
- **Democratizing Finance**: Mission to make investing accessible to everyone
- **Growth Stage**: Join a rapidly scaling fintech with strong market position
- **Innovation**: Build cutting-edge financial products and trading systems
- **Data Access**: Work with unique retail investor behavior datasets
- **Impact**: Directly influence investing experience for millions of customers"""
    },

    # Healthcare/Pharma
    {
        "company": "Pfizer",
        "role": "Principal Data Scientist, Drug Discovery AI",
        "location": "Cambridge, MA",
        "salary_range": "$280,000 - $450,000 (Principal level)",
        "department": "Digital Medicine & Translational Imaging",
        "content": """### About Pfizer Digital Medicine
Pfizer's Digital Medicine team leverages AI and ML to accelerate drug discovery, optimize clinical trials, and improve patient outcomes. We're applying cutting-edge AI to solve some of healthcare's most challenging problems and bring life-changing medicines to patients faster.

### Role Overview
Lead AI initiatives in drug discovery as a Principal Data Scientist at Pfizer. You'll develop ML models for target identification, molecule design, clinical trial optimization, and real-world evidence generation that accelerate the development of breakthrough therapies.

### Key Responsibilities
- **Drug Discovery AI**: Build ML models for target identification and validation
- **Molecular Design**: Develop generative models for novel drug molecule creation
- **Clinical Analytics**: Optimize clinical trial design and patient stratification
- **Real-World Evidence**: Analyze healthcare data to support regulatory submissions
- **Biomarker Discovery**: Identify predictive biomarkers using multi-omics data
- **Cross-functional Leadership**: Collaborate with scientists, clinicians, and regulatory teams

### Technical Specializations
- **Computational Biology**: Genomics, proteomics, and multi-omics data analysis
- **Molecular ML**: Graph neural networks for chemical property prediction
- **Clinical AI**: Electronic health records analysis and patient outcome prediction
- **Computer Vision**: Medical imaging analysis for biomarker discovery
- **Natural Language Processing**: Scientific literature mining and clinical note analysis
- **Causal Inference**: Understanding treatment effects and clinical outcomes

### Required Qualifications
- **Education**: PhD in Computer Science, Computational Biology, Bioinformatics, or related field
- **Experience**: 8+ years in data science with healthcare or pharmaceutical focus
- **Domain Knowledge**: Deep understanding of drug discovery and development processes
- **Regulatory**: Experience with FDA submissions and clinical trial regulations
- **Biological Data**: Expertise with genomics, clinical, and real-world evidence data
- **Leadership**: Experience leading cross-functional teams and strategic initiatives

### What We Offer
- **Total Compensation**: $280K-$450K including base, bonuses, and comprehensive benefits
- **Medical Impact**: Contribute to life-saving drug discovery and development
- **Research Resources**: Access to world-class datasets and computational infrastructure
- **Global Reach**: Collaborate with international teams and research institutions
- **Career Development**: Leadership opportunities in pharmaceutical AI and digital health
- **Mission Alignment**: Work toward improving patient outcomes and global health"""
    }
]

# Generate all job descriptions
print("Generating comprehensive data scientist job descriptions...")
created_files = []

for job in job_descriptions:
    filename = create_job_description(
        job["company"],
        job["role"], 
        job["location"],
        job["salary_range"],
        job["department"],
        job["content"]
    )
    created_files.append(filename)
    print(f"Created: {filename}")

print(f"\nGenerated {len(created_files)} additional job descriptions")
print("All files created successfully!")