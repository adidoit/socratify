# Software Engineering Interview Questions Database Schema

## CSV Structure
- `company`: Company name (e.g., "Google", "Meta", "Amazon")
- `question`: The actual interview question text
- `difficulty`: Junior | Mid | Senior | Staff | Principal
- `question_type`: Category of question (see below)
- `skills_assessed`: Comma-separated list of skills (see below)
- `swe_level`: Target SWE level (see below)
- `source`: Source of the question for credibility

## Focus: Verbal/Discussion-Based Questions
These are questions that can be answered with:
- Whiteboard discussions
- Verbal explanations
- Architecture diagrams
- Trade-off conversations
- 2-minute explanations with follow-ups

**NOT included:**
- Coding problems requiring implementation
- Algorithm puzzles requiring code
- Data structure coding exercises

## Question Categories

### System Design
**Large-scale system architecture questions**
- Design Twitter/Facebook feed
- Design URL shortener like bit.ly
- Design chat application like WhatsApp
- Design video streaming like YouTube
- Design ride-sharing like Uber

### Architecture & Trade-offs
**Technical decision and trade-off discussions**
- Microservices vs Monolith trade-offs
- SQL vs NoSQL database choices
- Caching strategies and trade-offs
- Load balancing approaches
- Consistency vs Availability trade-offs

### Technical Concepts
**Explain fundamental CS/engineering concepts**
- How does HTTPS work?
- Explain REST vs GraphQL
- What is eventual consistency?
- How do distributed locks work?
- Explain MapReduce paradigm

### Scaling & Performance
**Discussions about scale and optimization**
- How to scale a database?
- Handling millions of concurrent users
- Performance bottleneck identification
- Caching strategies at scale
- Database sharding approaches

### Infrastructure & DevOps
**Deployment and infrastructure discussions**
- CI/CD pipeline design
- Container orchestration strategies
- Monitoring and alerting approaches
- Blue-green vs Rolling deployments
- Infrastructure as Code principles

### API Design
**RESTful and API architecture discussions**
- Design REST API for e-commerce
- API versioning strategies
- Rate limiting implementation
- Authentication and authorization
- API gateway patterns

### Database Design
**Data modeling and storage discussions**
- Database schema design
- Indexing strategies
- Replication vs Sharding
- ACID properties explanation
- CAP theorem applications

### Security & Privacy
**Security architecture discussions**
- Authentication vs Authorization
- OAuth flow explanation
- Data encryption strategies
- Security best practices
- Privacy compliance approaches

## Difficulty Levels
- **Junior**: 0-2 years experience, New Grad, SWE I
- **Mid**: 2-5 years experience, SWE II-III level
- **Senior**: 5-8 years experience, Senior SWE level
- **Staff**: 8-12 years experience, Staff Engineer level
- **Principal**: 12+ years experience, Principal/Distinguished Engineer

## Skills Assessed (Standardized List)
- System Design & Architecture
- Scalability & Performance
- Database Design & Modeling
- API Design & Integration
- Distributed Systems Knowledge
- Security & Privacy
- Infrastructure & DevOps
- Technical Communication
- Trade-off Analysis
- Problem Decomposition
- Technology Selection
- Performance Optimization
- Microservices Architecture
- Cloud Computing
- Software Engineering Principles

## Target Companies (Top Tech Companies)

### Tier 1 (FAANG+)
Google, Meta, Amazon, Apple, Netflix, Microsoft

### Tier 2 (Major Tech)
Tesla, Uber, Airbnb, Salesforce, Adobe, PayPal, Nvidia, LinkedIn, Spotify

### Tier 3 (High-Growth/Unicorns)
Stripe, Shopify, Zoom, Slack, Dropbox, Pinterest, Snap, Square, Discord, etc.

### Specialized Tech
Palantir, Databricks, Snowflake, MongoDB, Elastic, CrowdStrike, Okta, etc.

## SWE Levels
- **New Grad**: New Graduate Software Engineer
- **SWE I**: Software Engineer I
- **SWE II**: Software Engineer II  
- **SWE III**: Software Engineer III
- **Senior SWE**: Senior Software Engineer
- **Staff**: Staff Engineer
- **Principal**: Principal Engineer
- **Distinguished**: Distinguished Engineer