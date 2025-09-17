#!/usr/bin/env python3
"""
Premium Engineering Blogs Expansion

Focus: Novel applications, beyond-textbook insights, practitioner perspectives
Categories: International, smaller high-quality, open source, vendor engineering
Quality bar: Must explain something genuinely novel or interesting applications
"""

PREMIUM_ENGINEERING_BLOGS_EXPANSION = {
    # International Tech Powerhouses (Non-US)
    "atlassian": {
        "name": "Atlassian Engineering",
        "url": "https://blog.developer.atlassian.com/",
        "rss": "https://blog.developer.atlassian.com/feed/",
        "description": "Distributed team coordination, JIRA/Confluence scaling, Australian engineering excellence",
        "specialization": ["distributed-collaboration", "enterprise-scale", "workflow-engineering"]
    },
    
    "booking": {
        "name": "Booking.com Engineering", 
        "url": "https://blog.booking.com/",
        "rss": "https://blog.booking.com/rss.xml",
        "description": "Travel platform scaling, A/B testing at massive scale, European engineering",
        "specialization": ["experimentation", "personalization", "global-scale"]
    },
    
    "deliveroo": {
        "name": "Deliveroo Engineering",
        "url": "https://deliveroo.engineering/",
        "rss": "https://deliveroo.engineering/feed.xml", 
        "description": "On-demand logistics, real-time routing, UK food delivery engineering",
        "specialization": ["logistics", "real-time-optimization", "marketplace"]
    },
    
    "spotify_rnd": {
        "name": "Spotify R&D",
        "url": "https://research.spotify.com/",
        "rss": None,
        "description": "Music recommendation research, audio ML, Swedish engineering excellence",
        "specialization": ["audio-ml", "recommendation-systems", "music-technology"]
    },
    
    "klarna": {
        "name": "Klarna Engineering",
        "url": "https://engineering.klarna.com/",
        "rss": "https://engineering.klarna.com/rss/",
        "description": "Fintech innovation, buy-now-pay-later engineering, European payments",
        "specialization": ["fintech", "payments", "risk-modeling"]
    },
    
    "canva": {
        "name": "Canva Engineering",
        "url": "https://canva.dev/blog/engineering/",
        "rss": None,
        "description": "Creative platform scaling, collaborative design, Australian design-tech",
        "specialization": ["creative-tools", "collaboration", "design-systems"]
    },
    
    # Novel Applications & Smaller High-Quality Companies
    "retool": {
        "name": "Retool Engineering",
        "url": "https://retool.com/blog/",
        "rss": "https://retool.com/blog/rss.xml",
        "description": "Internal tool building, low-code platform engineering, developer productivity",
        "specialization": ["low-code", "developer-tools", "productivity"]
    },
    
    "notion": {
        "name": "Notion Engineering",
        "url": "https://www.notion.so/blog/topic/eng",
        "rss": None,
        "description": "Block-based editing, collaborative documents, workspace engineering",
        "specialization": ["collaborative-editing", "document-systems", "workspace"]
    },
    
    "linear": {
        "name": "Linear Engineering",
        "url": "https://linear.app/blog",
        "rss": None,
        "description": "Project management engineering, fast UI, developer workflow optimization",
        "specialization": ["project-management", "ui-performance", "developer-workflow"]
    },
    
    "vercel": {
        "name": "Vercel Engineering",
        "url": "https://vercel.com/blog",
        "rss": "https://vercel.com/atom",
        "description": "Edge computing, serverless deployment, frontend infrastructure",
        "specialization": ["edge-computing", "serverless", "frontend-infra"]
    },
    
    "supabase": {
        "name": "Supabase Engineering",
        "url": "https://supabase.com/blog",
        "rss": "https://supabase.com/rss.xml",
        "description": "Open source Firebase alternative, Postgres extensions, developer experience",
        "specialization": ["postgres", "developer-experience", "open-source"]
    },
    
    "planetscale_tech": {
        "name": "PlanetScale Technical Blog",
        "url": "https://planetscale.com/blog",
        "rss": None,
        "description": "MySQL branching, database-as-code, Vitess scaling innovations",
        "specialization": ["mysql-scaling", "database-branching", "vitess"]
    },
    
    # Specialized Technical Domains
    "render": {
        "name": "Render Engineering",
        "url": "https://blog.render.com/",
        "rss": "https://blog.render.com/rss/",
        "description": "Cloud platform engineering, auto-scaling, developer platform",
        "specialization": ["cloud-platform", "auto-scaling", "developer-platform"]
    },
    
    "netlify": {
        "name": "Netlify Engineering", 
        "url": "https://www.netlify.com/blog/",
        "rss": "https://www.netlify.com/blog/index.xml",
        "description": "JAMstack architecture, edge functions, static site optimization",
        "specialization": ["jamstack", "edge-functions", "static-sites"]
    },
    
    "hasura": {
        "name": "Hasura Engineering",
        "url": "https://hasura.io/blog/",
        "rss": "https://hasura.io/blog/rss.xml",
        "description": "GraphQL engine, real-time subscriptions, API layer innovations",
        "specialization": ["graphql", "real-time", "api-layer"]
    },
    
    "postman": {
        "name": "Postman Engineering",
        "url": "https://blog.postman.com/engineering/",
        "rss": "https://blog.postman.com/feed/",
        "description": "API development platform, collaboration tools, testing infrastructure",
        "specialization": ["api-development", "testing", "collaboration"]
    },
    
    # High-Quality Vendor Engineering (Not Sales)
    "confluent": {
        "name": "Confluent Engineering",
        "url": "https://www.confluent.io/blog/",
        "rss": "https://www.confluent.io/blog/feed/",
        "description": "Kafka ecosystem, event streaming patterns, distributed systems",
        "specialization": ["kafka", "event-streaming", "distributed-systems"]
    },
    
    "cockroachdb_tech": {
        "name": "CockroachDB Technical Blog",
        "url": "https://www.cockroachlabs.com/blog/",
        "rss": "https://www.cockroachlabs.com/blog/rss.xml",
        "description": "Distributed SQL, consistency models, database engineering",
        "specialization": ["distributed-sql", "consistency", "database-internals"]
    },
    
    "timescaledb_tech": {
        "name": "TimescaleDB Engineering",
        "url": "https://blog.timescale.com/",
        "rss": "https://blog.timescale.com/rss/",
        "description": "Time-series database optimization, PostgreSQL extensions, analytics",
        "specialization": ["time-series", "postgresql", "analytics"]
    },
    
    "pinecone": {
        "name": "Pinecone Engineering",
        "url": "https://www.pinecone.io/blog/",
        "rss": None,
        "description": "Vector databases, similarity search, ML infrastructure",
        "specialization": ["vector-database", "similarity-search", "ml-infrastructure"]
    },
    
    "weaviate": {
        "name": "Weaviate Engineering",
        "url": "https://weaviate.io/blog",
        "rss": "https://weaviate.io/blog/rss.xml",
        "description": "Vector search engine, knowledge graphs, semantic search",
        "specialization": ["vector-search", "knowledge-graphs", "semantic-search"]
    },
    
    # Open Source Engineering Excellence
    "kubernetes": {
        "name": "Kubernetes Blog",
        "url": "https://kubernetes.io/blog/",
        "rss": "https://kubernetes.io/blog/feed.xml",
        "description": "Container orchestration, cluster management, cloud-native patterns",
        "specialization": ["container-orchestration", "cloud-native", "cluster-management"]
    },
    
    "istio": {
        "name": "Istio Engineering",
        "url": "https://istio.io/latest/blog/",
        "rss": "https://istio.io/blog/feed.xml",
        "description": "Service mesh architecture, microservices networking, security",
        "specialization": ["service-mesh", "microservices", "networking"]
    },
    
    "prometheus": {
        "name": "Prometheus Engineering",
        "url": "https://prometheus.io/blog/",
        "rss": "https://prometheus.io/blog/feed.xml",
        "description": "Monitoring systems, time-series metrics, alerting patterns",
        "specialization": ["monitoring", "time-series", "alerting"]
    },
    
    "vitess": {
        "name": "Vitess Engineering",
        "url": "https://vitess.io/blog/",
        "rss": "https://vitess.io/blog/index.xml",
        "description": "MySQL sharding, database scaling, YouTube's database architecture",
        "specialization": ["mysql-sharding", "database-scaling", "horizontal-partitioning"]
    },
    
    "cncf": {
        "name": "CNCF Engineering",
        "url": "https://www.cncf.io/blog/",
        "rss": "https://www.cncf.io/feed/",
        "description": "Cloud native technologies, ecosystem engineering, open source governance",
        "specialization": ["cloud-native", "open-source", "ecosystem"]
    },
    
    # Specialized Domains - High Innovation
    "plaid": {
        "name": "Plaid Engineering",
        "url": "https://blog.plaid.com/",
        "rss": None,
        "description": "Financial data connectivity, API security, fintech infrastructure",
        "specialization": ["fintech", "financial-data", "api-security"]
    },
    
    "datadog": {
        "name": "Datadog Engineering",
        "url": "https://www.datadoghq.com/blog/engineering/",
        "rss": "https://www.datadoghq.com/blog/rss.xml",
        "description": "Monitoring at scale, distributed tracing, observability engineering",
        "specialization": ["monitoring", "observability", "distributed-tracing"]
    },
    
    "newrelic": {
        "name": "New Relic Engineering",
        "url": "https://blog.newrelic.com/engineering/",
        "rss": "https://blog.newrelic.com/feed/",
        "description": "Application performance monitoring, telemetry data processing",
        "specialization": ["apm", "telemetry", "performance-monitoring"]
    },
    
    "auth0": {
        "name": "Auth0 Engineering",
        "url": "https://auth0.com/blog/developers/",
        "rss": "https://auth0.com/blog/rss.xml", 
        "description": "Identity and authentication systems, security protocols, OAuth/OIDC",
        "specialization": ["identity", "authentication", "security"]
    },
    
    "okta": {
        "name": "Okta Engineering",
        "url": "https://developer.okta.com/blog/",
        "rss": "https://developer.okta.com/feed.xml",
        "description": "Identity management, zero-trust architecture, enterprise security",
        "specialization": ["identity-management", "zero-trust", "enterprise-security"]
    },
    
    # Gaming/Entertainment Engineering
    "roblox": {
        "name": "Roblox Engineering",
        "url": "https://blog.roblox.com/",
        "rss": None,
        "description": "Metaverse infrastructure, user-generated content platforms, gaming scale",
        "specialization": ["metaverse", "user-generated-content", "gaming-infrastructure"]
    },
    
    "unity": {
        "name": "Unity Engineering",
        "url": "https://blog.unity.com/engine-platform",
        "rss": None,
        "description": "Game engine architecture, real-time rendering, cross-platform development",
        "specialization": ["game-engine", "rendering", "cross-platform"]
    },
    
    # Financial/Crypto Innovation
    "chain": {
        "name": "Chain Engineering",
        "url": "https://chain.com/blog/",
        "rss": None,
        "description": "Blockchain infrastructure, institutional crypto, distributed ledger technology",
        "specialization": ["blockchain", "distributed-ledger", "crypto-infrastructure"]
    },
    
    "circle": {
        "name": "Circle Engineering", 
        "url": "https://www.circle.com/blog",
        "rss": None,
        "description": "Stablecoin infrastructure, cryptocurrency payments, regulatory compliance",
        "specialization": ["stablecoin", "crypto-payments", "compliance"]
    },
    
    # Transportation/Logistics Innovation
    "lyft": {
        "name": "Lyft Engineering",
        "url": "https://eng.lyft.com/",
        "rss": "https://eng.lyft.com/feed",
        "description": "Rideshare optimization, real-time dispatch, transportation algorithms",
        "specialization": ["rideshare", "dispatch-algorithms", "transportation"]
    },
    
    "doordash": {
        "name": "DoorDash Engineering",
        "url": "https://doordash.engineering/",
        "rss": "https://doordash.engineering/feed/",
        "description": "Food delivery logistics, demand prediction, marketplace optimization",
        "specialization": ["delivery-logistics", "demand-prediction", "marketplace"]
    }
}


def get_premium_expansion_blogs(limit=40):
    """Get premium expansion blogs ranked by innovation and quality."""
    
    ranked_blogs = []
    
    # Weight scoring for different types of innovation
    category_weights = {
        "novel-applications": 5,      # Completely new problem domains
        "international": 3,           # Geographic diversity brings different perspectives  
        "open-source": 4,            # Usually highest technical quality
        "vendor-engineering": 2,     # Good but need to filter sales content
        "specialized-domains": 4     # Deep expertise in specific areas
    }
    
    for key, blog in PREMIUM_ENGINEERING_BLOGS_EXPANSION.items():
        score = 0
        
        # Base quality score from specializations
        score += len(blog['specialization']) * 2
        
        # Innovation indicators in specialization
        innovation_keywords = [
            'real-time', 'distributed', 'scaling', 'novel', 'optimization',
            'ml', 'ai', 'blockchain', 'edge', 'serverless', 'collaboration'
        ]
        
        specialization_text = ' '.join(blog['specialization']).lower()
        score += sum(3 for keyword in innovation_keywords if keyword in specialization_text)
        
        # Novel application bonus (look for unique problem domains)
        novel_domains = [
            'metaverse', 'user-generated-content', 'creative-tools', 'collaborative-editing',
            'vector-database', 'time-series', 'identity', 'fintech', 'logistics',
            'game-engine', 'audio-ml', 'food-delivery', 'rideshare'
        ]
        score += sum(4 for domain in novel_domains if domain in specialization_text)
        
        # International diversity bonus
        international_companies = ['atlassian', 'booking', 'deliveroo', 'klarna', 'canva']
        if key in international_companies:
            score += 3
            
        # Open source excellence bonus  
        open_source = ['kubernetes', 'istio', 'prometheus', 'vitess', 'cncf', 'supabase']
        if key in open_source:
            score += 4
        
        # RSS availability bonus (easier to process)
        if blog.get('rss'):
            score += 2
            
        ranked_blogs.append((key, blog, score))
    
    # Sort by innovation/quality score
    ranked_blogs.sort(key=lambda x: x[2], reverse=True)
    return ranked_blogs[:limit]


def print_premium_expansion_list():
    """Print the premium expansion blog list."""
    blogs = get_premium_expansion_blogs(40)
    
    print("🚀 PREMIUM ENGINEERING BLOGS EXPANSION")
    print("=" * 70)
    print("Focus: Novel applications, beyond-textbook insights, practitioner perspectives")
    print("Quality bar: Must explain something genuinely interesting/innovative\n")
    
    # Group by category
    categories = {
        "🌍 International Powerhouses": [],
        "💡 Novel Applications": [], 
        "🔧 Open Source Excellence": [],
        "🏢 Vendor Engineering (High Quality)": [],
        "🎯 Specialized Domains": []
    }
    
    # Categorize blogs
    international = ['atlassian', 'booking', 'deliveroo', 'klarna', 'canva', 'spotify_rnd']
    open_source = ['kubernetes', 'istio', 'prometheus', 'vitess', 'cncf', 'supabase']
    novel_apps = ['retool', 'notion', 'linear', 'vercel', 'roblox', 'unity', 'plaid']
    vendors = ['confluent', 'cockroachdb_tech', 'timescaledb_tech', 'pinecone', 'datadog']
    
    for i, (key, blog, score) in enumerate(blogs, 1):
        rss_status = "✅ RSS" if blog.get('rss') else "🕷️ Scrape"
        specializations = ', '.join(blog['specialization'][:3])
        
        entry = f"{i:2d}. {blog['name']}\n"
        entry += f"    🎯 {specializations}\n"
        entry += f"    💡 {blog['description']}\n" 
        entry += f"    📊 Score: {score} | {rss_status}\n\n"
        
        if key in international:
            categories["🌍 International Powerhouses"].append(entry)
        elif key in open_source:
            categories["🔧 Open Source Excellence"].append(entry)
        elif key in novel_apps:
            categories["💡 Novel Applications"].append(entry)
        elif key in vendors:
            categories["🏢 Vendor Engineering (High Quality)"].append(entry)
        else:
            categories["🎯 Specialized Domains"].append(entry)
    
    # Print by categories
    for category, entries in categories.items():
        if entries:
            print(category)
            print("-" * 50)
            for entry in entries:
                print(entry)


if __name__ == "__main__":
    print_premium_expansion_list()