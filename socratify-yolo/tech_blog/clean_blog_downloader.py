#!/usr/bin/env python3
"""
Clean Engineering Blog Downloader

Simple, clean structure: blogs/company/article.md
Downloads from top 25-50 engineering blogs with quality filtering.
"""

import os
import re
import sys
import time
import argparse
import requests
from datetime import datetime
from urllib.parse import urljoin, urlparse
from pathlib import Path
import json

try:
    import feedparser
    import html2text
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with:")
    print("pip install feedparser html2text beautifulsoup4 requests")
    sys.exit(1)

# Top Engineering Blogs (Combined list of 50 highest quality)
TOP_ENGINEERING_BLOGS = {
    # Tier 1: Premier Tech Companies
    "airbnb": {
        "name": "Airbnb Engineering",
        "url": "https://medium.com/airbnb-engineering", 
        "rss": "https://medium.com/feed/airbnb-engineering"
    },
    "netflix": {
        "name": "Netflix Technology Blog",
        "url": "https://netflixtechblog.com/",
        "rss": "https://netflixtechblog.com/feed"
    },
    "spotify": {
        "name": "Spotify Engineering",
        "url": "https://engineering.atspotify.com/",
        "rss": "https://engineering.atspotify.com/feed/"
    },
    "uber": {
        "name": "Uber Engineering",
        "url": "https://www.uber.com/blog/engineering/",
        "rss": "https://www.uber.com/blog/engineering/rss/"
    },
    "linkedin": {
        "name": "LinkedIn Engineering",
        "url": "https://engineering.linkedin.com/",
        "rss": "https://engineering.linkedin.com/blog.rss"
    },
    "pinterest": {
        "name": "Pinterest Engineering",
        "url": "https://medium.com/pinterest-engineering",
        "rss": "https://medium.com/feed/pinterest-engineering"
    },
    "dropbox": {
        "name": "Dropbox Tech Blog",
        "url": "https://dropbox.tech/",
        "rss": "https://dropbox.tech/feed"
    },
    
    # Tier 2: Major Tech Platforms
    "github": {
        "name": "GitHub Engineering",
        "url": "https://github.blog/category/engineering/",
        "rss": "https://github.blog/category/engineering/feed/"
    },
    "slack": {
        "name": "Slack Engineering",
        "url": "https://slack.engineering/",
        "rss": "https://slack.engineering/feed/"
    },
    "shopify": {
        "name": "Shopify Engineering",
        "url": "https://shopify.engineering/",
        "rss": "https://shopify.engineering/blog.atom"
    },
    "stripe": {
        "name": "Stripe Engineering",
        "url": "https://stripe.com/blog/engineering",
        "rss": "https://stripe.com/blog/feed.rss"
    },
    "cloudflare": {
        "name": "Cloudflare Engineering",
        "url": "https://blog.cloudflare.com/tag/engineering",
        "rss": "https://blog.cloudflare.com/tag/engineering/rss/"
    },
    "twilio": {
        "name": "Twilio Engineering",
        "url": "https://www.twilio.com/blog/tag/engineering",
        "rss": "https://www.twilio.com/blog/tag/engineering/feed"
    },
    "square": {
        "name": "Square Engineering",
        "url": "https://developer.squareup.com/blog/",
        "rss": "https://developer.squareup.com/blog/rss.xml"
    },
    
    # Big Tech Engineering
    "meta": {
        "name": "Meta Engineering",
        "url": "https://engineering.fb.com/",
        "rss": "https://engineering.fb.com/feed/"
    },
    "google": {
        "name": "Google AI Blog", 
        "url": "https://ai.googleblog.com/",
        "rss": "https://ai.googleblog.com/feeds/posts/default"
    },
    "microsoft": {
        "name": "Microsoft Engineering",
        "url": "https://devblogs.microsoft.com/engineering-at-microsoft/",
        "rss": "https://devblogs.microsoft.com/engineering-at-microsoft/feed/"
    },
    "aws": {
        "name": "AWS Architecture Blog",
        "url": "https://aws.amazon.com/blogs/architecture/",
        "rss": "https://aws.amazon.com/blogs/architecture/feed/"
    },
    
    # Data & Analytics
    "databricks": {
        "name": "Databricks Engineering",
        "url": "https://www.databricks.com/blog/category/engineering", 
        "rss": "https://www.databricks.com/blog/rss.xml"
    },
    "elastic": {
        "name": "Elastic Engineering",
        "url": "https://www.elastic.co/blog/category/engineering",
        "rss": "https://www.elastic.co/blog/feed"
    },
    "mongodb": {
        "name": "MongoDB Engineering",
        "url": "https://www.mongodb.com/blog/channel/engineering-blog",
        "rss": None
    },
    
    # Infrastructure & Cloud
    "hashicorp": {
        "name": "HashiCorp Engineering",
        "url": "https://www.hashicorp.com/blog/products/terraform",
        "rss": "https://www.hashicorp.com/blog/feed.xml"
    },
    "docker": {
        "name": "Docker Engineering",
        "url": "https://www.docker.com/blog/category/engineering/",
        "rss": "https://www.docker.com/blog/feed/"
    },
    "redis": {
        "name": "Redis Engineering",
        "url": "https://redis.com/blog/",
        "rss": "https://redis.com/blog/feed/"
    },
    
    # Specialized High-Quality Blogs
    "segment": {
        "name": "Segment Engineering",
        "url": "https://segment.com/blog/engineering/",
        "rss": "https://segment.com/blog/engineering/atom.xml"
    },
    "cockroachdb": {
        "name": "CockroachDB Engineering",
        "url": "https://www.cockroachlabs.com/blog/engineering/",
        "rss": None
    },
    "fly": {
        "name": "Fly.io Engineering",
        "url": "https://fly.io/blog/",
        "rss": "https://fly.io/blog/feed.xml"
    },
    "tailscale": {
        "name": "Tailscale Engineering",
        "url": "https://tailscale.com/blog/",
        "rss": "https://tailscale.com/blog/index.xml"
    },
    "teleport": {
        "name": "Teleport Engineering",
        "url": "https://goteleport.com/blog/",
        "rss": "https://goteleport.com/blog/feed/"
    },
    "honeycomb": {
        "name": "Honeycomb Engineering",
        "url": "https://www.honeycomb.io/blog/",
        "rss": "https://www.honeycomb.io/blog/rss.xml"
    },
    "timescale": {
        "name": "TimescaleDB Engineering",
        "url": "https://blog.timescale.com/blog/category/engineering/",
        "rss": "https://blog.timescale.com/rss/"
    },
    "planetscale": {
        "name": "PlanetScale Engineering",
        "url": "https://planetscale.com/blog",
        "rss": None
    },
    "buildkite": {
        "name": "Buildkite Engineering",
        "url": "https://buildkite.com/blog",
        "rss": "https://buildkite.com/blog.atom"
    },
    "railway": {
        "name": "Railway Engineering",
        "url": "https://blog.railway.app/",
        "rss": "https://blog.railway.app/rss.xml"
    },
    "deno": {
        "name": "Deno Engineering",
        "url": "https://deno.com/blog",
        "rss": "https://deno.com/feed"
    },
    "meilisearch": {
        "name": "Meilisearch Engineering",
        "url": "https://blog.meilisearch.com/",
        "rss": "https://blog.meilisearch.com/rss/"
    },
    "vector": {
        "name": "Vector Engineering",
        "url": "https://vector.dev/blog/",
        "rss": "https://vector.dev/blog/rss.xml"
    },
    
    # Additional Quality Blogs
    "grafana": {
        "name": "Grafana Engineering",
        "url": "https://grafana.com/blog/engineering/",
        "rss": None
    },
    "neon": {
        "name": "Neon Engineering",
        "url": "https://neon.tech/blog",
        "rss": None
    },
    "temporal": {
        "name": "Temporal Engineering",
        "url": "https://temporal.io/blog",
        "rss": None
    },
    "pulsar": {
        "name": "Apache Pulsar",
        "url": "https://pulsar.apache.org/blog/",
        "rss": "https://pulsar.apache.org/blog/feed.xml"
    },
    "discord": {
        "name": "Discord Engineering",
        "url": "https://discord.com/category/engineering",
        "rss": None
    },
    "figma": {
        "name": "Figma Engineering",
        "url": "https://www.figma.com/blog/section/engineering/",
        "rss": None
    },
    "zed": {
        "name": "Zed Engineering",
        "url": "https://zed.dev/blog",
        "rss": None
    },
    "oxide": {
        "name": "Oxide Computer",
        "url": "https://oxide.computer/blog",
        "rss": "https://oxide.computer/blog/rss.xml"
    },
    "tigerbeetle": {
        "name": "TigerBeetle Engineering",
        "url": "https://tigerbeetle.com/blog/",
        "rss": None
    },
    "algolia": {
        "name": "Algolia Engineering",
        "url": "https://blog.algolia.com/engineering/",
        "rss": None
    },
    "typesense": {
        "name": "Typesense Engineering",
        "url": "https://typesense.org/blog/",
        "rss": None
    },
    "lightstep": {
        "name": "Lightstep Engineering",
        "url": "https://lightstep.com/blog/",
        "rss": None
    },
    "snowflake": {
        "name": "Snowflake Engineering",
        "url": "https://www.snowflake.com/blog/?category=engineering",
        "rss": None
    },
    "replit": {
        "name": "Replit Engineering",
        "url": "https://blog.replit.com/engineering",
        "rss": None
    }
}


class QualityFilter:
    """Simple quality filter for engineering content."""
    
    def __init__(self):
        self.tech_keywords = [
            'architecture', 'algorithm', 'distributed', 'performance', 'scalability',
            'database', 'infrastructure', 'microservices', 'kubernetes', 'docker',
            'machine learning', 'data pipeline', 'real-time', 'optimization',
            'monitoring', 'observability', 'security', 'engineering', 'system design'
        ]
        
        self.avoid_keywords = [
            'announce', 'hiring', 'culture', 'partnership', 'funding', 
            'acquisition', 'event', 'webinar', 'conference'
        ]
    
    def is_engineering_content(self, title, content, threshold=3):
        """Check if content is engineering-focused."""
        text = f"{title} {content}".lower()
        
        tech_score = sum(1 for keyword in self.tech_keywords if keyword in text)
        avoid_score = sum(1 for keyword in self.avoid_keywords if keyword in text)
        
        return (tech_score - avoid_score) >= threshold


class CleanBlogDownloader:
    """Clean, simple blog downloader with organized structure."""
    
    def __init__(self, output_dir="blogs", delay=2.0):
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.filter = QualityFilter()
        
        # Clean up any existing messy structure
        self.output_dir.mkdir(exist_ok=True)
        
        # HTTP session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Markdown converter
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.ignore_images = False
        self.converter.body_width = 0
        
        # Statistics
        self.stats = {'downloaded': 0, 'filtered': 0, 'errors': 0}
    
    def sanitize_filename(self, title):
        """Create clean filename."""
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        return filename[:60] or "untitled"
    
    def extract_content(self, url):
        """Extract clean article content."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer']):
                element.decompose()
            
            # Find content
            content_element = (
                soup.select_one('article') or 
                soup.select_one('.post-content') or 
                soup.select_one('.entry-content') or
                soup.select_one('main')
            )
            
            if not content_element:
                divs = soup.find_all('div')
                content_element = max(divs, key=lambda x: len(x.get_text()), default=None)
            
            if not content_element:
                return None
            
            # Extract metadata
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Untitled"
            title_text = re.sub(r'\s*[\|\-]\s*[^|]*$', '', title_text)
            
            # Get author
            author_elem = soup.select_one('.author') or soup.select_one('.byline')
            author = author_elem.get_text().strip() if author_elem else "Unknown"
            
            # Convert to markdown
            markdown = self.converter.handle(str(content_element))
            
            return {
                'title': title_text,
                'author': author,
                'url': url,
                'content': markdown.strip()
            }
            
        except Exception as e:
            print(f"   ❌ Error extracting {url}: {e}")
            return None
    
    def save_article(self, article, company):
        """Save article in clean structure: blogs/company/article.md"""
        if not article or not article['content']:
            return False
        
        # Create company directory
        company_dir = self.output_dir / company
        company_dir.mkdir(exist_ok=True)
        
        # Create clean filename
        safe_title = self.sanitize_filename(article['title'])
        filepath = company_dir / f"{safe_title}.md"
        
        # Handle duplicates
        counter = 1
        while filepath.exists():
            filepath = company_dir / f"{safe_title}_{counter}.md"
            counter += 1
        
        # Create clean markdown with simple frontmatter
        content = f"""---
title: "{article['title'].replace('"', '\\"')}"
author: "{article['author']}"
url: "{article['url']}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
---

{article['content']}
"""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"   ❌ Save error: {e}")
            return False
    
    def download_blog(self, company, config, max_articles=10):
        """Download articles from a single blog."""
        print(f"\n📝 {config['name']}")
        
        if not config['rss']:
            print(f"   ⚠️  No RSS feed available")
            return
        
        try:
            # Get RSS feed
            response = self.session.get(config['rss'], timeout=30)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
            else:
                feed = feedparser.parse(config['rss'])
            
            if not feed.entries:
                print(f"   ⚠️  No articles found")
                return
            
            print(f"   🔍 Found {len(feed.entries)} articles")
            
            # Process articles
            downloaded = 0
            for entry in feed.entries[:max_articles]:
                if downloaded >= max_articles:
                    break
                    
                title = entry.get('title', 'Untitled')
                url = entry.get('link', '')
                
                if not url:
                    continue
                
                # Extract content
                article = self.extract_content(url)
                if not article:
                    self.stats['errors'] += 1
                    continue
                
                # Quality filter
                if not self.filter.is_engineering_content(article['title'], article['content']):
                    print(f"   🚫 Filtered: {title[:40]}...")
                    self.stats['filtered'] += 1
                    continue
                
                # Save article
                if self.save_article(article, company):
                    print(f"   ✅ Downloaded: {title[:40]}...")
                    self.stats['downloaded'] += 1
                    downloaded += 1
                else:
                    self.stats['errors'] += 1
                
                time.sleep(self.delay / 2)
                
        except Exception as e:
            print(f"   ❌ RSS error: {e}")
            self.stats['errors'] += 1
    
    def download_all(self, limit=25, articles_per_blog=10):
        """Download from top engineering blogs."""
        print("🚀 ENGINEERING BLOG DOWNLOADER")
        print("=" * 50)
        print(f"📊 Target: Top {limit} engineering blogs")
        print(f"📄 Articles per blog: {articles_per_blog}")
        print(f"📁 Output: {self.output_dir}/")
        
        # Get top blogs (only those with RSS)
        blogs_with_rss = [(k, v) for k, v in TOP_ENGINEERING_BLOGS.items() if v['rss']]
        selected_blogs = blogs_with_rss[:limit]
        
        print(f"\n🎯 Processing {len(selected_blogs)} blogs with RSS feeds:")
        
        # Download from each blog
        for i, (company, config) in enumerate(selected_blogs, 1):
            print(f"\n[{i}/{len(selected_blogs)}]", end=" ")
            self.download_blog(company, config, articles_per_blog)
            time.sleep(self.delay)
        
        # Print final stats
        print(f"\n📊 FINAL RESULTS")
        print("=" * 30)
        print(f"✅ Downloaded: {self.stats['downloaded']} articles")
        print(f"🚫 Filtered: {self.stats['filtered']} articles")
        print(f"❌ Errors: {self.stats['errors']}")
        print(f"📁 Saved to: {self.output_dir}/")
        
        return self.stats['downloaded']


def main():
    parser = argparse.ArgumentParser(description="Download engineering blog articles")
    parser.add_argument('-n', '--num-blogs', type=int, default=25,
                       help='Number of blogs to process (default: 25)')
    parser.add_argument('-a', '--articles', type=int, default=10,
                       help='Articles per blog (default: 10)')
    parser.add_argument('-d', '--delay', type=float, default=2.0,
                       help='Delay between requests (default: 2.0)')
    
    args = parser.parse_args()
    
    downloader = CleanBlogDownloader(delay=args.delay)
    downloader.download_all(limit=args.num_blogs, articles_per_blog=args.articles)


if __name__ == "__main__":
    main()