#!/usr/bin/env python3
"""
Legendary Systems Architecture Collector

Targets specific legendary/famous system architecture articles that we know exist
and are considered must-reads in the systems engineering community.
"""

import requests
import time
from pathlib import Path
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class LegendarySystemsCollector:
    """Collector for legendary/famous system architecture articles."""
    
    # Legendary system architecture articles (known URLs)
    LEGENDARY_ARTICLES = {
        # 🔥 Slack Engineering (Legendary scaling series)
        'slack': [
            'https://slack.engineering/scaling-slacks-job-queue/',
            'https://slack.engineering/flannel-an-application-level-edge-cache/',
            'https://slack.engineering/service-encryption/',
            'https://slack.engineering/migrating-millions-of-concurrent-websockets/',
            'https://slack.engineering/real-time-messaging/',
        ],
        
        # 🎨 Figma Engineering (Real-time collaboration)
        'figma': [
            'https://www.figma.com/blog/how-figmas-multiplayer-technology-works/',
            'https://www.figma.com/blog/figmas-journey-to-typescript-compiling-away-our-custom-programming-language/',
            'https://www.figma.com/blog/realtime-editing-of-ordered-sequences/',
            'https://www.figma.com/blog/rust-in-production-at-figma/',
        ],
        
        # 💰 High-Frequency Trading & Financial Systems
        'janestreet': [
            'https://blog.janestreet.com/what-the-interns-have-wrought-2016/',
            'https://blog.janestreet.com/what-the-interns-have-wrought-2017/',
            'https://blog.janestreet.com/what-the-interns-have-wrought-2018/',
            'https://blog.janestreet.com/seven-implementations-of-incremental/',
            'https://blog.janestreet.com/announcing-incremental/',
        ],
        
        # 🏗️ Infrastructure & Deployment
        'vercel': [
            'https://vercel.com/blog/how-we-optimized-package-imports-in-next-js',
            'https://vercel.com/blog/understanding-next-js-data-fetching',
            'https://vercel.com/blog/introducing-the-edge-runtime',
            'https://vercel.com/blog/edge-functions-generally-available',
        ],
        
        'fly': [
            'https://fly.io/blog/docker-without-docker/',
            'https://fly.io/blog/sqlite-internals/',
            'https://fly.io/blog/all-in-on-sqlite-litestream/',
            'https://fly.io/blog/globally-distributed-postgres/',
        ],
        
        # 📊 Data Infrastructure Legends
        'snowflake': [
            'https://www.snowflake.com/blog/how-foundational-technologies-create-cloud-data-platforms/',
            'https://www.snowflake.com/en/blog/2016/05/23/scaling-snowflake-to-thousands-of-queries-per-second/',
        ],
        
        'databricks': [
            'https://www.databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html',
            'https://www.databricks.com/blog/2018/10/29/open-sourcing-delta-lake.html',
            'https://www.databricks.com/blog/2017/05/08/introducing-vectorized-query-execution-in-apache-spark.html',
        ],
        
        # 🎮 Gaming Systems
        'roblox': [
            'https://blog.roblox.com/2020/05/scaling-backend-infrastructure/',
            'https://blog.roblox.com/2019/10/roblox-return-to-service-10-28-2019/',
            'https://blog.roblox.com/2018/11/roblox-adventures-in-microservices/',
        ],
        
        'riot': [
            'https://technology.riotgames.com/news/running-online-services-riot-part-i',
            'https://technology.riotgames.com/news/running-online-services-riot-part-ii',
            'https://technology.riotgames.com/news/deep-dive-riot-messaging-service',
        ],
        
        # 🔍 Search & Discovery
        'algolia': [
            'https://blog.algolia.com/inside-the-algolia-engine-part-1-nifi/',
            'https://blog.algolia.com/inside-the-algolia-engine-part-2-the-indexing-challenge/',
            'https://blog.algolia.com/inside-the-algolia-engine-part-3-query-processing/',
            'https://blog.algolia.com/when-solid-state-drives-are-not-that-solid/',
        ],
        
        # 🛡️ Security & Authentication  
        'auth0': [
            'https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/',
            'https://auth0.com/blog/critical-vulnerabilities-in-json-web-token-libraries/',
            'https://auth0.com/blog/rs256-vs-hs256-whats-the-difference/',
        ],
        
        '1password': [
            'https://blog.1password.com/1password-x-december-2019-security-audit/',
            'https://blog.1password.com/secure-remote-password/',
            'https://blog.1password.com/introducing-secrets-automation/',
        ],
        
        # 📈 Observability & Monitoring
        'grafana': [
            'https://grafana.com/blog/2019/05/09/grafana-6.2-released/',
            'https://grafana.com/blog/2020/03/18/how-to-successfully-run-grafana-at-scale/',
            'https://grafana.com/blog/2019/11/21/how-to-configure-grafana-as-code/',
        ],
        
        # 🔄 Workflow & Data Integration
        'temporal': [
            'https://docs.temporal.io/blog/workflow-engine-principles',
            'https://docs.temporal.io/blog/temporal-transparency-update-1',
            'https://temporal.io/blog/durable-execution',
        ],
        
        'airbyte': [
            'https://airbyte.com/blog/data-engineering-thoughts',
            'https://airbyte.com/blog/change-data-capture-definition',
            'https://airbyte.com/blog/airflow-vs-prefect',
        ],
        
        # 🚀 Modern Infrastructure
        'retool': [
            'https://retool.com/blog/how-we-built-retool/',
            'https://retool.com/blog/eraser-map-making-retool-fast/',
            'https://retool.com/blog/text-editor/',
        ],
        
        'supabase': [
            'https://supabase.com/blog/supabase-beta-may-2021',
            'https://supabase.com/blog/how-we-launch',
            'https://supabase.com/blog/postgrest',
        ],
        
        'render': [
            'https://render.com/blog/how-render-autoscaling-works',
            'https://render.com/blog/zero-downtime-deploys',
        ],
        
        # 💾 Database Systems
        'planetscale': [
            'https://planetscale.com/blog/how-planetscale-boost-serves-your-sql-queries-instantly',
            'https://planetscale.com/blog/operating-mysql-at-planetscale',
            'https://planetscale.com/blog/announcing-planetscale-boost',
        ],
        
        'neon': [
            'https://neon.tech/blog/architecture-decisions-in-neon',
            'https://neon.tech/blog/getting-started-with-neon-branching',
            'https://neon.tech/blog/neon-serverless-driver',
        ],
        
        # 🎥 Video & Communication
        'zoom': [
            'https://blog.zoom.us/how-zoom-works/',
            'https://medium.com/zoom-developer-blog/zoom-chat-message-architecture-4a6b9ca0ef85',
        ],
        
        # 📱 Instagram & Social Media (Historical but legendary)
        'instagram': [
            'https://instagram-engineering.com/what-powers-instagram-hundreds-of-instances-dozens-of-technologies-adf2e22da2ad',
            'https://instagram-engineering.com/making-instagram-com-faster-part-1-62cc0c327538',
            'https://instagram-engineering.com/making-instagram-com-faster-part-2-f350c8fba0d4',
        ],
    }
    
    def __init__(self, blogs_dir="blogs"):
        self.blogs_dir = Path(blogs_dir)
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
        
        self.stats = {'attempted': 0, 'downloaded': 0, 'duplicates_skipped': 0, 'errors': 0, 'companies_processed': 0}
    
    def extract_content_robust_universal(self, soup):
        """Universal content extraction for any blog platform."""
        extraction_strategies = [
            # Slack Engineering
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('article .content'),
            
            # Figma Blog
            lambda s: s.select_one('article'),
            lambda s: s.select_one('[data-testid="blog-post-content"]'),
            
            # Jane Street
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('.entry-content'),
            
            # Medium-based blogs
            lambda s: s.select_one('article[data-testid="storyContent"]'),
            lambda s: s.select_one('.story-content'),
            lambda s: s.select_one('.postArticle-content'),
            
            # Modern framework patterns
            lambda s: s.select_one('main'),
            lambda s: s.select_one('[role="main"]'),
            lambda s: s.select_one('.blog-post-content'),
            
            # Generic patterns
            lambda s: s.select_one('.content'),
            lambda s: s.select_one('#content'),
            lambda s: s.select_one('.post'),
            lambda s: s.select_one('.entry'),
            
            # Fallback: largest content div
            lambda s: max(
                (div for div in s.find_all(['div', 'section', 'article']) 
                 if len(div.get_text(strip=True)) > 2000), 
                key=lambda x: len(x.get_text(strip=True)), 
                default=None
            )
        ]
        
        for strategy in extraction_strategies:
            try:
                content_elem = strategy(soup)
                if content_elem and len(content_elem.get_text(strip=True)) > 2000:
                    return content_elem
            except:
                continue
        
        return None
    
    def extract_title_universal(self, soup, url):
        """Universal title extraction."""
        title_strategies = [
            lambda s: s.select_one('h1'),
            lambda s: s.select_one('.post-title'),
            lambda s: s.select_one('.entry-title'),
            lambda s: s.select_one('title'),
            lambda s: s.select_one('[data-testid="post-title"]'),
            lambda s: s.select_one('.blog-post-title'),
            lambda s: s.select_one('h2'),  # Fallback
        ]
        
        for strategy in title_strategies:
            try:
                title_elem = strategy(soup)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if 10 < len(title) < 300:
                        return title
            except:
                continue
        
        # Fallback: derive from URL
        url_part = url.split('/')[-1].replace('-', ' ').replace('_', ' ')
        return url_part.title() or "Legendary System Architecture Article"
    
    def download_legendary_article(self, company, url):
        """Download a legendary article."""
        try:
            self.stats['attempted'] += 1
            print(f"   📥 Downloading: {url}")
            
            response = self.session.get(url, timeout=20)
            if response.status_code != 200:
                print(f"   ❌ HTTP {response.status_code}")
                self.stats['errors'] += 1
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self.extract_title_universal(soup, url)
            
            # Extract content
            content_elem = self.extract_content_robust_universal(soup)
            
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
            h.single_line_break = False
            
            markdown_content = h.handle(str(content_elem))
            
            # Quality validation
            content_length = len(markdown_content.strip())
            if content_length < 2000:
                print(f"   ❌ Content too short ({content_length} chars)")
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
            filename = f"{safe_title[:75]}.md"
            filepath = company_dir / filename
            
            # Handle conflicts
            counter = 1
            while filepath.exists():
                base_name = safe_title[:70]
                filepath = company_dir / f"{base_name}_{counter}.md"
                counter += 1
            
            # Enhanced frontmatter for legendary articles
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
content_length: {content_length}
type: "legendary_systems_architecture"
legendary: true
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            # Update tracking
            self.existing_hashes.add(content_hash)
            self.stats['downloaded'] += 1
            
            print(f"   ✅ Saved: {title[:70]}... ({content_length} chars)")
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:120]}")
            self.stats['errors'] += 1
            return False
    
    def collect_legendary_articles(self):
        """Collect all legendary system architecture articles."""
        print("⭐ LEGENDARY SYSTEMS ARCHITECTURE COLLECTOR")
        print("=" * 70)
        print("🎯 Target: Famous/legendary system architecture articles")
        print("🏆 These are the must-read articles in systems engineering")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing")
        print()
        print("Categories: 🔥 Slack Scaling, 🎨 Figma Real-time, 💰 HFT, 🏗️ Infrastructure,")
        print("           📊 Data Systems, 🎮 Gaming, 🔍 Search, 🛡️ Security, 📈 Observability")
        print()
        
        for company, urls in self.LEGENDARY_ARTICLES.items():
            print(f"\n🏢 {company.upper()}")
            print("-" * 50)
            
            downloaded = 0
            for url in urls:
                if self.download_legendary_article(company, url):
                    downloaded += 1
                    time.sleep(3)  # Respectful pause
                else:
                    time.sleep(1.5)
            
            print(f"   📊 Downloaded {downloaded}/{len(urls)} legendary articles")
            self.stats['companies_processed'] += 1
            
            # Pause between companies
            time.sleep(5)
        
        # Final stats
        print(f"\n⭐ LEGENDARY COLLECTION COMPLETE")
        print("=" * 50)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        total_files = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total articles in collection: {total_files}")
        
        if self.stats['downloaded'] > 0:
            print(f"🏆 Successfully added {self.stats['downloaded']} legendary system architecture articles!")
            print("⭐ These are considered must-reads in the systems engineering community")

def main():
    collector = LegendarySystemsCollector()
    collector.collect_legendary_articles()

if __name__ == "__main__":
    main()