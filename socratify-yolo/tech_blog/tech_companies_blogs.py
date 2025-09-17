#!/usr/bin/env python3
"""
Tech Company Engineering Blogs Directory

High-quality engineering blogs from top tech companies.
Focuses on technical content, not sales/marketing material.
"""

TECH_COMPANY_BLOGS = {
    # Tier 1: Premier Tech Companies
    "netflix": {
        "name": "Netflix Technology Blog", 
        "url": "https://netflixtechblog.com/",
        "rss": "https://netflixtechblog.com/feed",
        "categories": ["engineering", "data", "machine-learning", "infrastructure"],
        "quality_indicators": ["architecture", "scale", "performance", "ml", "data", "microservices"],
        "avoid_keywords": ["hiring", "culture", "announcement", "event"]
    },
    
    "airbnb": {
        "name": "Airbnb Engineering & Data Science",
        "url": "https://medium.com/airbnb-engineering", 
        "rss": "https://medium.com/feed/airbnb-engineering",
        "categories": ["engineering", "data-science", "machine-learning"],
        "quality_indicators": ["algorithm", "architecture", "data", "ml", "infrastructure", "optimization"],
        "avoid_keywords": ["hiring", "culture", "diversity", "announcement"]
    },
    
    "uber": {
        "name": "Uber Engineering",
        "url": "https://www.uber.com/blog/engineering/",
        "rss": "https://www.uber.com/blog/engineering/rss/",
        "categories": ["ai", "backend", "data", "mobile"],
        "quality_indicators": ["algorithm", "ml", "distributed", "architecture", "optimization"],
        "avoid_keywords": ["announcement", "hiring", "culture"]
    },
    
    "spotify": {
        "name": "Spotify Engineering",
        "url": "https://engineering.atspotify.com/",
        "rss": "https://engineering.atspotify.com/feed/",
        "categories": ["engineering", "data", "machine-learning", "backend"],
        "quality_indicators": ["algorithm", "ml", "data", "architecture", "performance"],
        "avoid_keywords": ["culture", "hiring", "announcement"]
    },
    
    "dropbox": {
        "name": "Dropbox Tech Blog",
        "url": "https://dropbox.tech/",
        "rss": "https://dropbox.tech/feed",
        "categories": ["infrastructure", "machine-learning", "frontend", "mobile"],
        "quality_indicators": ["infrastructure", "storage", "sync", "performance", "ml"],
        "avoid_keywords": ["announcement", "hiring", "culture"]
    },
    
    # Tier 2: Major Tech Platforms
    "github": {
        "name": "The GitHub Blog - Engineering",
        "url": "https://github.blog/category/engineering/",
        "rss": "https://github.blog/category/engineering/feed/",
        "categories": ["engineering", "infrastructure", "security"],
        "quality_indicators": ["git", "version-control", "ci/cd", "infrastructure", "security"],
        "avoid_keywords": ["announcement", "product-launch", "acquisition"]
    },
    
    "slack": {
        "name": "Slack Engineering",
        "url": "https://slack.engineering/",
        "rss": "https://slack.engineering/feed/",
        "categories": ["engineering", "infrastructure", "mobile"],
        "quality_indicators": ["real-time", "messaging", "infrastructure", "mobile", "performance"],
        "avoid_keywords": ["announcement", "hiring", "culture"]
    },
    
    "linkedin": {
        "name": "LinkedIn Engineering",
        "url": "https://engineering.linkedin.com/",
        "rss": "https://engineering.linkedin.com/blog.rss",
        "categories": ["engineering", "data", "machine-learning"],
        "quality_indicators": ["distributed", "data", "ml", "recommendation", "search"],
        "avoid_keywords": ["announcement", "hiring", "culture", "product-launch"]
    },
    
    "pinterest": {
        "name": "Pinterest Engineering",
        "url": "https://medium.com/pinterest-engineering",
        "rss": "https://medium.com/feed/pinterest-engineering",
        "categories": ["engineering", "data", "machine-learning"],
        "quality_indicators": ["recommendation", "ml", "computer-vision", "search", "data"],
        "avoid_keywords": ["announcement", "hiring", "culture"]
    },
    
    "shopify": {
        "name": "Shopify Engineering",
        "url": "https://shopify.engineering/",
        "rss": "https://shopify.engineering/blog.atom",
        "categories": ["engineering", "infrastructure", "performance"],
        "quality_indicators": ["e-commerce", "performance", "ruby", "infrastructure", "database"],
        "avoid_keywords": ["announcement", "hiring", "culture"]
    },
    
    # Tier 3: Cloud & Infrastructure 
    "cloudflare": {
        "name": "Cloudflare Blog - Engineering",
        "url": "https://blog.cloudflare.com/tag/engineering",
        "rss": "https://blog.cloudflare.com/tag/engineering/rss/",
        "categories": ["engineering", "security", "networking", "performance"],
        "quality_indicators": ["cdn", "dns", "security", "ddos", "performance", "edge"],
        "avoid_keywords": ["announcement", "product-launch", "acquisition"]
    },
    
    "stripe": {
        "name": "Stripe Engineering",
        "url": "https://stripe.com/blog/engineering",
        "rss": "https://stripe.com/blog/feed.rss",
        "categories": ["engineering", "infrastructure", "security"],
        "quality_indicators": ["payments", "api", "reliability", "security", "infrastructure"],
        "avoid_keywords": ["announcement", "product-launch", "partnership"]
    },
    
    "twilio": {
        "name": "Twilio Engineering",
        "url": "https://www.twilio.com/blog/tag/engineering",
        "rss": "https://www.twilio.com/blog/tag/engineering/feed",
        "categories": ["engineering", "communications", "apis"],
        "quality_indicators": ["telecom", "api", "messaging", "voice", "infrastructure"],
        "avoid_keywords": ["announcement", "product-launch", "partnership"]
    },
    
    # Tier 4: Specialized Tech Companies
    "square": {
        "name": "Square Corner Blog",
        "url": "https://developer.squareup.com/blog/",
        "rss": "https://developer.squareup.com/blog/rss.xml",
        "categories": ["engineering", "mobile", "payments"],
        "quality_indicators": ["payments", "mobile", "pos", "api", "security"],
        "avoid_keywords": ["announcement", "product-launch", "partnership"]
    },
    
    "discord": {
        "name": "Discord Engineering & Design",
        "url": "https://discord.com/category/engineering",
        "rss": None,  # May need web scraping
        "categories": ["engineering", "infrastructure", "real-time"],
        "quality_indicators": ["real-time", "voice", "chat", "infrastructure", "gaming"],
        "avoid_keywords": ["announcement", "hiring", "culture"]
    },
    
    "figma": {
        "name": "Figma Engineering",
        "url": "https://www.figma.com/blog/section/engineering/",
        "rss": None,  # May need web scraping
        "categories": ["engineering", "frontend", "graphics"],
        "quality_indicators": ["graphics", "canvas", "collaboration", "performance", "rendering"],
        "avoid_keywords": ["announcement", "product-launch", "design-thinking"]
    },
    
    # Big Tech Engineering (when they focus on tech)
    "aws": {
        "name": "AWS Architecture Blog",
        "url": "https://aws.amazon.com/blogs/architecture/",
        "rss": "https://aws.amazon.com/blogs/architecture/feed/",
        "categories": ["architecture", "cloud", "infrastructure"],
        "quality_indicators": ["architecture", "serverless", "microservices", "cloud", "scalability"],
        "avoid_keywords": ["announcement", "product-launch", "case-study"]
    },
    
    "google_ai": {
        "name": "Google AI Blog", 
        "url": "https://ai.googleblog.com/",
        "rss": "https://ai.googleblog.com/feeds/posts/default",
        "categories": ["machine-learning", "ai", "research"],
        "quality_indicators": ["machine-learning", "deep-learning", "tensorflow", "research", "nlp"],
        "avoid_keywords": ["announcement", "product-launch", "acquisition"]
    },
    
    "microsoft": {
        "name": "Microsoft Engineering Blog",
        "url": "https://devblogs.microsoft.com/engineering-at-microsoft/",
        "rss": "https://devblogs.microsoft.com/engineering-at-microsoft/feed/",
        "categories": ["engineering", "azure", "infrastructure"],
        "quality_indicators": ["azure", "kubernetes", "microservices", "infrastructure", ".net"],
        "avoid_keywords": ["announcement", "product-launch", "acquisition"]
    },
    
    "meta": {
        "name": "Engineering at Meta",
        "url": "https://engineering.fb.com/",
        "rss": "https://engineering.fb.com/feed/",
        "categories": ["engineering", "machine-learning", "infrastructure"],
        "quality_indicators": ["machine-learning", "infrastructure", "react", "graphql", "scaling"],
        "avoid_keywords": ["announcement", "hiring", "culture", "metaverse"]
    },
    
    # Data & Analytics Focused
    "databricks": {
        "name": "Databricks Engineering",
        "url": "https://www.databricks.com/blog/category/engineering", 
        "rss": "https://www.databricks.com/blog/rss.xml",
        "categories": ["engineering", "data", "spark", "ml"],
        "quality_indicators": ["spark", "data-engineering", "ml", "analytics", "lakehouse"],
        "avoid_keywords": ["announcement", "product-launch", "partnership"]
    },
    
    "snowflake": {
        "name": "Snowflake Engineering",
        "url": "https://www.snowflake.com/blog/?category=engineering",
        "rss": None,  # May need web scraping
        "categories": ["engineering", "data", "cloud"],
        "quality_indicators": ["data-warehouse", "sql", "performance", "architecture", "cloud"],
        "avoid_keywords": ["announcement", "product-launch", "customer-story"]
    },
    
    # Additional High-Quality Blogs
    "hashicorp": {
        "name": "HashiCorp Engineering",
        "url": "https://www.hashicorp.com/blog/products/terraform",
        "rss": "https://www.hashicorp.com/blog/feed.xml",
        "categories": ["infrastructure", "devops", "cloud"],
        "quality_indicators": ["terraform", "vault", "consul", "infrastructure", "devops"],
        "avoid_keywords": ["announcement", "product-launch", "partnership"]
    },
    
    "mongodb": {
        "name": "MongoDB Engineering Blog",
        "url": "https://www.mongodb.com/blog/channel/engineering-blog",
        "rss": None,
        "categories": ["database", "engineering", "performance"],
        "quality_indicators": ["database", "nosql", "performance", "sharding", "replication"],
        "avoid_keywords": ["announcement", "product-launch", "customer-story"]
    },
    
    "elastic": {
        "name": "Elastic Engineering",
        "url": "https://www.elastic.co/blog/category/engineering",
        "rss": "https://www.elastic.co/blog/feed",
        "categories": ["search", "engineering", "elasticsearch"],
        "quality_indicators": ["elasticsearch", "search", "logging", "performance", "distributed"],
        "avoid_keywords": ["announcement", "product-launch", "customer-story"]
    },
    
    "cockroachdb": {
        "name": "CockroachDB Engineering",
        "url": "https://www.cockroachlabs.com/blog/engineering/",
        "rss": None,
        "categories": ["database", "distributed-systems"],
        "quality_indicators": ["distributed", "sql", "consistency", "performance", "database"],
        "avoid_keywords": ["announcement", "product-launch", "funding"]
    }
}


def get_top_engineering_blogs(limit=25):
    """Get the top engineering blogs, ranked by quality and technical depth."""
    
    # Rank blogs by technical quality indicators
    ranked_blogs = []
    
    for key, blog in TECH_COMPANY_BLOGS.items():
        # Calculate quality score based on technical indicators
        tech_score = len(blog['quality_indicators']) * 2
        
        # Bonus points for having RSS feed (easier to process)
        if blog['rss']:
            tech_score += 3
            
        # Bonus for specialized engineering URL
        if 'engineering' in blog['url'].lower():
            tech_score += 2
            
        # Bonus for technical categories
        tech_categories = ['engineering', 'machine-learning', 'infrastructure', 'data']
        category_score = sum(1 for cat in blog['categories'] if any(tech in cat for tech in tech_categories))
        tech_score += category_score
        
        ranked_blogs.append((key, blog, tech_score))
    
    # Sort by score and return top N
    ranked_blogs.sort(key=lambda x: x[2], reverse=True)
    return ranked_blogs[:limit]


def print_blog_list():
    """Print the curated list of top engineering blogs."""
    top_blogs = get_top_engineering_blogs(25)
    
    print("🏗️  TOP 25 TECH COMPANY ENGINEERING BLOGS")
    print("=" * 60)
    print("Ranked by technical depth, engineering focus, and content quality\n")
    
    for i, (key, blog, score) in enumerate(top_blogs, 1):
        rss_status = "✅ RSS" if blog['rss'] else "🕷️  Scrape"
        categories_str = ", ".join(blog['categories'][:3])  # Show first 3 categories
        
        print(f"{i:2d}. {blog['name']}")
        print(f"    📍 {blog['url']}")
        print(f"    🎯 Focus: {categories_str}")
        print(f"    📊 Quality Score: {score}/10 | {rss_status}")
        print()


if __name__ == "__main__":
    print_blog_list()