# Data Engineering Interview Questions Database Schema

## CSV Structure
- `company`: Company name (e.g., "Google", "Meta", "Amazon")
- `question`: The actual interview question text
- `difficulty`: Junior | Mid | Senior | Staff | Principal
- `question_type`: Category of question (see below)
- `skills_assessed`: Comma-separated list of skills (see below)
- `de_level`: Target Data Engineering level (see below)
- `source`: Source of the question for credibility

## Focus: Verbal/Discussion-Based Questions
These are questions that can be answered with:
- Architecture diagrams and data flow designs
- Verbal explanations of trade-offs
- Whiteboard pipeline designs
- Technology selection discussions
- 2-minute explanations with follow-ups

**NOT included:**
- SQL coding problems
- Python/Scala implementation tasks
- Complex mathematical derivations

## Question Categories

### Data Pipeline Architecture
**ETL/ELT design and workflow discussions**
- Design batch processing pipeline
- Real-time vs batch processing trade-offs
- Stream processing architecture
- Data ingestion strategies
- Pipeline orchestration approaches

### Data Warehouse Design
**Data modeling and warehouse architecture**
- Star schema vs snowflake schema
- Dimensional modeling approaches
- Data lakehouse architecture
- OLAP vs OLTP design decisions
- Data mart strategies

### Big Data Technologies
**Technology selection and architecture trade-offs**
- Spark vs Hadoop comparisons
- Kafka vs other message brokers
- Airflow vs other orchestrators
- NoSQL database selection
- Distributed computing patterns

### Streaming & Real-time Processing
**Real-time data processing discussions**
- Event streaming architectures
- Change data capture (CDC) strategies
- Lambda vs Kappa architecture
- Stream processing frameworks
- Real-time analytics approaches

### Cloud Data Platforms
**Cloud-native data architecture**
- Snowflake vs BigQuery vs Redshift
- Data lake vs data warehouse
- Cloud migration strategies
- Multi-cloud data architecture
- Serverless data processing

### Data Quality & Governance
**Data reliability and governance frameworks**
- Data lineage implementation
- Data validation strategies
- Data cataloging approaches
- Privacy and compliance frameworks
- Data monitoring and alerting

### Performance Optimization
**Scaling and optimization discussions**
- Query optimization strategies
- Partitioning and indexing
- Caching strategies for data
- Resource allocation and tuning
- Cost optimization approaches

### Data Security & Privacy
**Security architecture for data systems**
- Data encryption strategies
- Access control mechanisms
- Compliance frameworks (GDPR, SOX)
- Data masking and anonymization
- Audit and monitoring approaches

## Difficulty Levels
- **Junior**: 0-2 years experience, Entry-level DE
- **Mid**: 2-5 years experience, Mid-level DE
- **Senior**: 5-8 years experience, Senior DE
- **Staff**: 8-12 years experience, Staff/Lead DE
- **Principal**: 12+ years experience, Principal DE

## Skills Assessed (Standardized List)
- Data Pipeline Design & Architecture
- ETL/ELT Development & Optimization
- Data Warehouse & Lake Architecture
- Big Data Technologies & Frameworks
- Streaming & Real-time Processing
- Cloud Data Platform Architecture
- Data Quality & Governance
- Performance Optimization & Tuning
- Data Security & Privacy
- Data Modeling & Design
- Technology Selection & Trade-offs
- Data Infrastructure & DevOps
- Business Requirements Analysis
- Technical Communication
- Problem Decomposition

## Target Companies

### Tier 1 (FAANG+)
Google, Meta, Amazon, Apple, Netflix, Microsoft

### Tier 2 (Major Tech & Data-Heavy)
Tesla, Uber, Airbnb, Salesforce, Adobe, LinkedIn, Spotify, Twitter/X

### Tier 3 (Data-Focused Companies)
Snowflake, Databricks, MongoDB, Elastic, Confluent, Palantir, Splunk

### Tier 4 (High-Growth with Heavy Data Needs)
Stripe, Shopify, DoorDash, Instacart, Robinhood, Coinbase, Discord

## DE Levels
- **Junior DE**: Junior Data Engineer
- **DE**: Data Engineer
- **Senior DE**: Senior Data Engineer
- **Staff DE**: Staff Data Engineer
- **Principal DE**: Principal Data Engineer / Data Architect