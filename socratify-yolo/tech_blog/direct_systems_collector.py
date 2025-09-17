#!/usr/bin/env python3
"""
Direct Systems Architecture Collector

Uses specific URLs of known excellent system architecture articles
from gaming, financial, security, and infrastructure companies.
"""

import requests
import time
from pathlib import Path
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class DirectSystemsCollector:
    """Collect specific high-quality system architecture articles."""
    
    # Direct URLs to excellent system architecture articles
    DIRECT_SYSTEM_ARTICLES = {
        'discord': [
            'https://discord.com/blog/how-discord-stores-billions-of-messages',
            'https://discord.com/blog/how-discord-stores-trillions-of-messages',
            'https://discord.com/blog/using-rust-to-scale-elixir-for-11-million-concurrent-users',
            'https://discord.com/blog/why-discord-is-switching-from-go-to-rust',
            'https://discord.com/blog/how-discord-scaled-elixir-to-5-000-000-concurrent-users',
        ],
        'github': [
            'https://github.blog/2018-10-30-oct21-post-incident-analysis/',
            'https://github.blog/2020-09-02-how-we-upgraded-github-com-to-mysql-8-0/',
            'https://github.blog/2021-09-27-partitioning-githubs-relational-databases-scale/',
            'https://github.blog/2022-02-02-how-we-scaled-github-api-with-a-sharded-replicated-rate-limiter/',
            'https://github.blog/2020-12-21-how-we-built-the-github-globe/',
        ],
        'uber': [
            'https://www.uber.com/blog/michelangelo-machine-learning-platform/',
            'https://www.uber.com/blog/engineering/schemaless/',  
            'https://www.uber.com/blog/engineering/ringpop-open-source-nodejs-library/',
            'https://www.uber.com/blog/engineering/express-js-python-golang/',
            'https://www.uber.com/blog/engineering/cherami/',
        ],
        'medium': [
            'https://medium.engineering/how-medium-detects-hotspots-in-dynamodb-using-machine-learning-fd679b9c5cf5',
            'https://medium.engineering/how-medium-goes-social-b7dbefa6d413',
            'https://medium.engineering/2016-in-review-medium-engineering-8b5b8b77ad36',
        ],
        'netflix': [
            'https://netflixtechblog.medium.com/netflix-conductor-a-microservices-orchestrator-2e8d4771bf40',
            'https://netflixtechblog.medium.com/netflix-at-velocity-2015-linux-performance-tools-51964ddb81cf',
            'https://netflixtechblog.medium.com/netflix-recommendations-beyond-the-5-stars-part-1-55838468f429',
        ],
        'twitch': [
            'https://blog.twitch.tv/en/2016/10/11/how-twitch-uses-postgresql-c34aa9e56f58/',
            'https://blog.twitch.tv/en/2019/04/10/live-video-transmuxing-transcoding-f6ac6914ce82/',
            'https://blog.twitch.tv/en/2017/02/13/how-we-built-twitchs-auto-hosting-system-52198dc2b9dc/',
        ],
        'mongodb': [
            'https://www.mongodb.com/blog/post/building-with-patterns-a-summary',
            'https://www.mongodb.com/blog/post/building-with-patterns-the-bucket-pattern',
            'https://www.mongodb.com/blog/post/building-with-patterns-the-subset-pattern',
        ],
        'coinbase': [
            'https://blog.coinbase.com/scaling-coinbase-9592d6a2d4e6',
            'https://blog.coinbase.com/how-coinbase-builds-secure-infrastructure-93b5930e3208',
            'https://blog.coinbase.com/container-technologies-at-coinbase-d4ae118dcb6c',
        ],
        'capitalone': [
            'https://www.capitalone.com/tech/cloud/container-runtime-security/',
            'https://www.capitalone.com/tech/machine-learning/fraud-detection-with-ml-at-capital-one/',
        ],
        'robinhood': [
            'https://robinhood.engineering/taming-the-python-gil-156548ef1a3e',
            'https://robinhood.engineering/debugging-memory-leaks-in-python-3b2b1466d9bd',
            'https://robinhood.engineering/the-architecture-of-robinhoods-brokerage-platform-f6d3b31aa2eb',
        ],
        'riot': [
            'https://technology.riotgames.com/news/running-online-services-riot-part-i',
            'https://technology.riotgames.com/news/running-online-services-riot-part-ii',
            'https://technology.riotgames.com/news/riots-approach-research-and-development',
        ]
    }
    
    def __init__(self, blogs_dir="blogs"):
        self.blogs_dir = Path(blogs_dir)
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
        
        self.stats = {'attempted': 0, 'downloaded': 0, 'duplicates_skipped': 0, 'errors': 0}
    
    def extract_content_robust(self, soup):
        """Extract content using multiple robust strategies."""
        strategies = [
            # Medium-specific
            lambda s: s.select_one('article[data-testid="storyContent"]'),
            lambda s: s.select_one('.story-content'),
            lambda s: s.select_one('.postArticle-content'),
            
            # GitHub blog
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('article'),
            
            # Discord blog  
            lambda s: s.select_one('main'),
            lambda s: s.select_one('.content'),
            
            # General patterns
            lambda s: s.select_one('[role="main"]'),
            lambda s: s.select_one('.entry-content'),
            
            # Fallback: find largest content block
            lambda s: max(
                (div for div in s.find_all(['div', 'section', 'article']) 
                 if len(div.get_text(strip=True)) > 1200), 
                key=lambda x: len(x.get_text(strip=True)), 
                default=None
            )
        ]
        
        for strategy in strategies:
            try:
                content_elem = strategy(soup)
                if content_elem and len(content_elem.get_text(strip=True)) > 1200:
                    return content_elem
            except:
                continue
        
        return None
    
    def extract_title_robust(self, soup, url):
        """Extract title using multiple strategies."""
        strategies = [
            lambda s: s.select_one('h1'),
            lambda s: s.select_one('.post-title'),
            lambda s: s.select_one('title'),
            lambda s: s.select_one('h2'),
            lambda s: s.select_one('[data-testid="storyTitle"]'),  # Medium
        ]
        
        for strategy in strategies:
            try:
                title_elem = strategy(soup)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if 10 < len(title) < 200:
                        return title
            except:
                continue
        
        # Fallback: derive from URL
        url_part = url.split('/')[-1].replace('-', ' ').replace('_', ' ')
        return url_part.title() or "System Architecture Article"
    
    def download_direct_article(self, company, url):
        """Download and save a direct article URL."""
        try:
            self.stats['attempted'] += 1
            print(f"   📥 Downloading: {url}")
            
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                print(f"   ❌ HTTP {response.status_code}")
                self.stats['errors'] += 1
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self.extract_title_robust(soup, url)
            
            # Extract content
            content_elem = self.extract_content_robust(soup)
            
            if not content_elem:
                print(f"   ❌ Could not extract content")
                self.stats['errors'] += 1
                return False
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            h.ignore_emphasis = False
            
            markdown_content = h.handle(str(content_elem))
            
            # Quality validation
            if len(markdown_content.strip()) < 1200:
                print(f"   ❌ Content too short ({len(markdown_content)} chars)")
                self.stats['errors'] += 1
                return False
            
            # Check for duplicate
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate detected, skipping")
                self.stats['duplicates_skipped'] += 1
                return False
            
            # Create directory
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            # Create filename
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:70]}.md"
            filepath = company_dir / filename
            
            # Handle conflicts
            counter = 1
            while filepath.exists():
                base_name = safe_title[:65]
                filepath = company_dir / f"{base_name}_{counter}.md"
                counter += 1
            
            # Create frontmatter
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
type: "direct_systems_collection"
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            # Update tracking
            self.existing_hashes.add(content_hash)
            self.stats['downloaded'] += 1
            
            print(f"   ✅ Saved: {title[:60]}...")
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            self.stats['errors'] += 1
            return False
    
    def collect_direct_articles(self):
        """Collect all direct system architecture articles."""
        print("🎯 DIRECT SYSTEMS ARCHITECTURE COLLECTOR")
        print("=" * 60)
        print(f"🎮 Gaming: Discord, Riot, Twitch")
        print(f"💰 Financial: Coinbase, Capital One, Robinhood") 
        print(f"🏗️ Infrastructure: GitHub, MongoDB, Uber")
        print(f"📺 Media: Medium, Netflix")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing")
        print()
        
        for company, urls in self.DIRECT_SYSTEM_ARTICLES.items():
            print(f"\n🏢 {company.upper()}")
            print("-" * 40)
            
            downloaded = 0
            for url in urls:
                if self.download_direct_article(company, url):
                    downloaded += 1
                    time.sleep(2)  # Respectful pause
                else:
                    time.sleep(1)
            
            print(f"   📊 Downloaded {downloaded}/{len(urls)} articles")
            
            # Pause between companies
            time.sleep(3)
        
        # Final stats
        print(f"\n✅ DIRECT COLLECTION COMPLETE")
        print("=" * 40)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        total_files = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total articles in collection: {total_files}")
        
        if self.stats['downloaded'] > 0:
            print(f"🚀 Successfully added {self.stats['downloaded']} premium system architecture articles!")

def main():
    collector = DirectSystemsCollector()
    collector.collect_direct_articles()

if __name__ == "__main__":
    main()