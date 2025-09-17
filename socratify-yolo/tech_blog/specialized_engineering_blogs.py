#!/usr/bin/env python3
"""
Specialized High-Quality Engineering Blogs

Focus on deep technical content, architecture discussions, and real engineering insights
from teams that may not be household names but produce exceptional technical content.
"""

SPECIALIZED_ENGINEERING_BLOGS = {
    # Infrastructure & Platform Engineering
    "discord_engineering": {
        "name": "Discord Engineering",
        "url": "https://discord.com/category/engineering",
        "rss": None,  # Need scraping
        "categories": ["real-time", "infrastructure", "gaming", "voice"],
        "quality_indicators": ["websockets", "voice-processing", "real-time", "latency", "gaming-infrastructure", "erlang", "elixir"],
        "avoid_keywords": ["announcement", "hiring", "culture"],
        "description": "Deep dives into real-time voice/chat infrastructure at massive scale"
    },
    
    "segment_engineering": {
        "name": "Segment Engineering",
        "url": "https://segment.com/blog/engineering/",
        "rss": "https://segment.com/blog/engineering/atom.xml",
        "categories": ["data-infrastructure", "streaming", "analytics"],
        "quality_indicators": ["data-pipeline", "streaming", "kafka", "analytics", "etl", "customer-data"],
        "avoid_keywords": ["product-launch", "announcement", "partnership"],
        "description": "Customer data infrastructure and streaming analytics at scale"
    },
    
    "cockroachdb_engineering": {
        "name": "CockroachDB Engineering",
        "url": "https://www.cockroachlabs.com/blog/engineering/",
        "rss": None,
        "categories": ["distributed-database", "consensus", "sql"],
        "quality_indicators": ["distributed", "consensus", "raft", "sql", "acid", "consistency", "byzantine"],
        "avoid_keywords": ["funding", "partnership", "announcement"],
        "description": "Distributed database internals, consensus algorithms, SQL at scale"
    },
    
    "fly_io": {
        "name": "Fly.io Engineering",
        "url": "https://fly.io/blog/",
        "rss": "https://fly.io/blog/feed.xml",
        "categories": ["edge-computing", "infrastructure", "containers"],
        "quality_indicators": ["edge-computing", "containers", "networking", "firecracker", "virtualization"],
        "avoid_keywords": ["announcement", "funding", "partnership"],
        "description": "Edge computing, container orchestration, and infrastructure"
    },
    
    "buildkite": {
        "name": "Buildkite Engineering", 
        "url": "https://buildkite.com/blog",
        "rss": "https://buildkite.com/blog.atom",
        "categories": ["ci-cd", "infrastructure", "devops"],
        "quality_indicators": ["ci-cd", "pipeline", "infrastructure", "devops", "testing", "deployment"],
        "avoid_keywords": ["announcement", "funding", "hiring"],
        "description": "CI/CD infrastructure, pipeline engineering, and devops practices"
    },

    # Database & Storage Systems
    "planetscale": {
        "name": "PlanetScale Engineering",
        "url": "https://planetscale.com/blog",
        "rss": None,
        "categories": ["database", "mysql", "scaling"],
        "quality_indicators": ["mysql", "database", "scaling", "vitess", "sharding", "branching"],
        "avoid_keywords": ["announcement", "funding", "partnership"],
        "description": "MySQL scaling, database branching, and Vitess architecture"
    },
    
    "tigerbeetle": {
        "name": "TigerBeetle Engineering",
        "url": "https://tigerbeetle.com/blog/",
        "rss": None,
        "categories": ["database", "financial", "performance"],
        "quality_indicators": ["database", "financial", "accounting", "performance", "zig", "kernel"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "High-performance financial database engineering in Zig"
    },
    
    "neon_tech": {
        "name": "Neon Engineering",
        "url": "https://neon.tech/blog",
        "rss": None,
        "categories": ["postgresql", "serverless", "storage"],
        "quality_indicators": ["postgresql", "serverless", "storage", "separation", "branching"],
        "avoid_keywords": ["announcement", "funding", "partnership"],
        "description": "Serverless Postgres, storage separation, database branching"
    },
    
    "timescaledb": {
        "name": "TimescaleDB Engineering",
        "url": "https://blog.timescale.com/blog/category/engineering/",
        "rss": "https://blog.timescale.com/rss/",
        "categories": ["time-series", "postgresql", "analytics"],
        "quality_indicators": ["time-series", "postgresql", "analytics", "compression", "aggregation"],
        "avoid_keywords": ["announcement", "funding", "partnership"],
        "description": "Time-series database engineering and PostgreSQL extensions"
    },

    # Search & Analytics
    "algolia_engineering": {
        "name": "Algolia Engineering",
        "url": "https://blog.algolia.com/engineering/",
        "rss": None,
        "categories": ["search", "algorithms", "performance"],
        "quality_indicators": ["search", "indexing", "algorithms", "performance", "relevance", "nlp"],
        "avoid_keywords": ["announcement", "partnership", "funding"],
        "description": "Search algorithms, indexing strategies, and relevance engineering"
    },
    
    "meilisearch": {
        "name": "Meilisearch Engineering", 
        "url": "https://blog.meilisearch.com/",
        "rss": "https://blog.meilisearch.com/rss/",
        "categories": ["search", "rust", "algorithms"],
        "quality_indicators": ["search", "rust", "indexing", "algorithms", "performance"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "Search engine architecture and algorithms in Rust"
    },
    
    "typesense": {
        "name": "Typesense Engineering",
        "url": "https://typesense.org/blog/",
        "rss": None,
        "categories": ["search", "cpp", "performance"],
        "quality_indicators": ["search", "cpp", "performance", "indexing", "typo-tolerance"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "High-performance search engine implementation in C++"
    },

    # Messaging & Communication
    "temporal_io": {
        "name": "Temporal Engineering",
        "url": "https://temporal.io/blog",
        "rss": None,
        "categories": ["workflow", "orchestration", "distributed"],
        "quality_indicators": ["workflow", "orchestration", "saga", "distributed", "state-machine"],
        "avoid_keywords": ["announcement", "funding", "partnership"],
        "description": "Workflow orchestration, saga patterns, and distributed state machines"
    },
    
    "apache_pulsar": {
        "name": "Apache Pulsar Blog",
        "url": "https://pulsar.apache.org/blog/",
        "rss": "https://pulsar.apache.org/blog/feed.xml",
        "categories": ["messaging", "streaming", "distributed"],
        "quality_indicators": ["messaging", "streaming", "kafka", "pulsar", "event-streaming"],
        "avoid_keywords": ["announcement", "conference"],
        "description": "Distributed messaging, event streaming, and Pulsar architecture"
    },
    
    "railway_engineering": {
        "name": "Railway Engineering",
        "url": "https://blog.railway.app/",
        "rss": "https://blog.railway.app/rss.xml",
        "categories": ["infrastructure", "deployment", "platforms"],
        "quality_indicators": ["infrastructure", "deployment", "containers", "kubernetes", "platform"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "Platform engineering, deployment infrastructure, and container orchestration"
    },

    # Security & Systems
    "teleport_engineering": {
        "name": "Teleport Engineering",
        "url": "https://goteleport.com/blog/",
        "rss": "https://goteleport.com/blog/feed/",
        "categories": ["security", "access", "infrastructure"],
        "quality_indicators": ["security", "access-control", "certificates", "ssh", "kubernetes"],
        "avoid_keywords": ["announcement", "funding", "partnership"],
        "description": "Security infrastructure, access control, and certificate management"
    },
    
    "tailscale": {
        "name": "Tailscale Engineering",
        "url": "https://tailscale.com/blog/",
        "rss": "https://tailscale.com/blog/index.xml",
        "categories": ["networking", "vpn", "go"],
        "quality_indicators": ["networking", "vpn", "wireguard", "nat", "peer-to-peer", "go"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "Network engineering, VPN implementation, and Go system programming"
    },
    
    "boundary": {
        "name": "Boundary by HashiCorp",
        "url": "https://www.boundaryproject.io/blog",
        "rss": None,
        "categories": ["security", "access", "identity"],
        "quality_indicators": ["security", "identity", "access", "zero-trust", "authentication"],
        "avoid_keywords": ["announcement", "partnership"],
        "description": "Identity-based access management and zero-trust architecture"
    },

    # Developer Tools & Languages
    "oxide_computer": {
        "name": "Oxide Computer Engineering",
        "url": "https://oxide.computer/blog",
        "rss": "https://oxide.computer/blog/rss.xml",
        "categories": ["hardware", "rust", "systems"],
        "quality_indicators": ["hardware", "rust", "firmware", "bmc", "illumos", "systems"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "Hardware engineering, Rust systems programming, and rack-scale computing"
    },
    
    "replit_engineering": {
        "name": "Replit Engineering",
        "url": "https://blog.replit.com/engineering",
        "rss": None,
        "categories": ["ide", "containers", "collaboration"],
        "quality_indicators": ["ide", "containers", "collaboration", "real-time", "multiplayer"],
        "avoid_keywords": ["announcement", "funding", "education"],
        "description": "Collaborative IDE engineering and real-time multiplayer systems"
    },
    
    "zed_industries": {
        "name": "Zed Engineering",
        "url": "https://zed.dev/blog",
        "rss": None,
        "categories": ["editor", "rust", "collaboration"],
        "quality_indicators": ["editor", "rust", "collaboration", "crdt", "real-time"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "Text editor engineering, CRDTs, and collaborative editing"
    },
    
    "deno_engineering": {
        "name": "Deno Engineering",
        "url": "https://deno.com/blog",
        "rss": "https://deno.com/feed",
        "categories": ["javascript", "typescript", "runtime"],
        "quality_indicators": ["v8", "rust", "typescript", "runtime", "security", "permissions"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "JavaScript runtime engineering, V8 integration, and security model"
    },

    # Observability & Monitoring
    "grafana_engineering": {
        "name": "Grafana Engineering",
        "url": "https://grafana.com/blog/engineering/",
        "rss": None,
        "categories": ["observability", "monitoring", "visualization"],
        "quality_indicators": ["observability", "monitoring", "metrics", "visualization", "prometheus"],
        "avoid_keywords": ["announcement", "partnership", "conference"],
        "description": "Observability engineering, metrics visualization, and monitoring systems"
    },
    
    "honeycomb_engineering": {
        "name": "Honeycomb Engineering",
        "url": "https://www.honeycomb.io/blog/",
        "rss": "https://www.honeycomb.io/blog/rss.xml",
        "categories": ["observability", "tracing", "debugging"],
        "quality_indicators": ["observability", "tracing", "debugging", "high-cardinality", "sampling"],
        "avoid_keywords": ["announcement", "funding", "partnership"],
        "description": "Observability engineering, distributed tracing, and debugging at scale"
    },
    
    "lightstep": {
        "name": "Lightstep Engineering", 
        "url": "https://lightstep.com/blog/",
        "rss": None,
        "categories": ["observability", "tracing", "microservices"],
        "quality_indicators": ["observability", "tracing", "microservices", "sampling", "latency"],
        "avoid_keywords": ["announcement", "acquisition"],
        "description": "Distributed tracing, microservices observability, and performance analysis"
    },
    
    "vector_dev": {
        "name": "Vector Engineering",
        "url": "https://vector.dev/blog/",
        "rss": "https://vector.dev/blog/rss.xml",
        "categories": ["logging", "observability", "rust"],
        "quality_indicators": ["logging", "observability", "rust", "performance", "data-pipeline"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "High-performance log processing and observability data pipelines"
    },

    # Additional Quality Picks
    "read_the_docs": {
        "name": "Read the Docs Engineering",
        "url": "https://blog.readthedocs.com/",
        "rss": "https://blog.readthedocs.com/rss/",
        "categories": ["documentation", "infrastructure", "django"],
        "quality_indicators": ["documentation", "sphinx", "django", "infrastructure", "hosting"],
        "avoid_keywords": ["announcement", "funding"],
        "description": "Documentation hosting infrastructure and Django at scale"
    }
}


def get_specialized_engineering_blogs(limit=25):
    """Get specialized engineering blogs ranked by technical depth."""
    
    ranked_blogs = []
    
    for key, blog in SPECIALIZED_ENGINEERING_BLOGS.items():
        # Calculate quality score based on technical specialization
        tech_score = len(blog['quality_indicators']) * 2
        
        # Bonus for RSS feed
        if blog['rss']:
            tech_score += 3
            
        # Bonus for specialized technical categories
        specialized_categories = ['distributed-database', 'real-time', 'consensus', 
                                'search', 'messaging', 'security', 'hardware', 'systems']
        category_bonus = sum(2 for cat in blog['categories'] 
                           if any(spec in cat for spec in specialized_categories))
        tech_score += category_bonus
        
        # Bonus for deep technical focus (fewer avoid keywords = more focused)
        focus_bonus = max(0, 5 - len(blog['avoid_keywords']))
        tech_score += focus_bonus
        
        ranked_blogs.append((key, blog, tech_score))
    
    # Sort by score and return top N
    ranked_blogs.sort(key=lambda x: x[2], reverse=True)
    return ranked_blogs[:limit]


def print_specialized_blog_list():
    """Print the curated list of specialized engineering blogs."""
    top_blogs = get_specialized_engineering_blogs(25)
    
    print("🔬 SPECIALIZED HIGH-QUALITY ENGINEERING BLOGS")
    print("=" * 65)
    print("Deep technical content from specialized teams & smaller companies")
    print("Focus: Architecture, algorithms, systems internals, real engineering\n")
    
    categories = {}
    
    for i, (key, blog, score) in enumerate(top_blogs, 1):
        rss_status = "✅ RSS" if blog['rss'] else "🕷️  Scrape"
        
        # Group by primary category for better organization
        primary_category = blog['categories'][0] if blog['categories'] else 'other'
        if primary_category not in categories:
            categories[primary_category] = []
        categories[primary_category].append((i, key, blog, score, rss_status))
    
    # Print by category groups
    for category, blogs in categories.items():
        category_title = category.replace('-', ' ').title()
        print(f"\n📂 {category_title}")
        print("-" * 40)
        
        for i, key, blog, score, rss_status in blogs:
            quality_indicators_str = ", ".join(blog['quality_indicators'][:4])
            
            print(f"{i:2d}. {blog['name']}")
            print(f"    📍 {blog['url']}")
            print(f"    🎯 Specialization: {quality_indicators_str}")
            print(f"    📊 Quality Score: {score}/15 | {rss_status}")
            print(f"    💡 {blog['description']}")
            print()


if __name__ == "__main__":
    print_specialized_blog_list()