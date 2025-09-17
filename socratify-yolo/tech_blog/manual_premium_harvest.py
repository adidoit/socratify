#!/usr/bin/env python3
"""
Manual Premium Harvest

Targets specific URLs of known premium system architecture articles
that are publicly accessible and represent the highest quality content.
"""

import requests
import time
from pathlib import Path
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class ManualPremiumHarvest:
    """Manual harvest of specific premium system architecture articles."""
    
    # Manually curated list of specific premium articles (verified URLs)
    PREMIUM_ARTICLES = {
        # 🏗️ More from companies we already have (highest quality picks)
        'google': [
            'https://research.google/blog/spanner-googles-globally-distributed-database/',
            'https://research.google/blog/mapreduce-simplified-data-processing-on-large-clusters/',
            'https://research.google/blog/the-google-file-system/',
            'https://research.google/blog/bigtable-a-distributed-storage-system-for-structured-data/',
        ],
        
        'aws': [
            'https://aws.amazon.com/blogs/architecture/amazon-aurora-under-the-hood-quorum-and-correlated-failure/',
            'https://aws.amazon.com/blogs/architecture/optimizing-amazon-s3-for-high-concurrency-in-distributed-workloads/',
            'https://aws.amazon.com/blogs/architecture/how-amazon-prime-video-uses-amazon-kinesis/',
        ],
        
        # 🌍 International Companies (specific working URLs)
        'atlassian': [
            'https://blog.developer.atlassian.com/how-we-built-bitbucket-pipelines/',
            'https://blog.developer.atlassian.com/scaling-confluence-for-performance/',
            'https://blog.developer.atlassian.com/jira-software-data-center-performance-improvements/',
        ],
        
        'booking': [
            'https://medium.com/booking-com-development/150k-requests-second-peeking-under-the-hood-of-booking-coms-distributed-systems-a6e1e2ccef4b',
            'https://medium.com/booking-com-development/better-data-and-ml-systems-through-a-better-ml-lifecycle-2de6bc3b95ce',
        ],
        
        'klarna': [
            'https://medium.com/klarna-engineering/klarna-checkout-in-50-milliseconds-d4b680b8a7b0',
            'https://medium.com/klarna-engineering/real-time-data-infrastructure-at-klarna-40f4e06d02e2',
        ],
        
        # 🔬 High-Quality Open Source Articles
        'apache': [
            'https://kafka.apache.org/documentation/#design',
            'https://cassandra.apache.org/doc/4.1/cassandra/architecture/',
        ],
        
        # 🏦 Financial Services (verified URLs) 
        'square': [
            'https://developer.squareup.com/blog/gos-extended-concurrency-comparing-the-sync-package-and-channels/',
            'https://developer.squareup.com/blog/streaming-mysql-results-in-python/',
        ],
        
        # 🎨 Individual Engineering Excellence (known good URLs)
        'engineering_blogs': [
            'https://www.allthingsdistributed.com/2006/03/a_word_on_scalability.html',  # Werner Vogels (AWS CTO)
            'https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html',  # DynamoDB paper
            'https://blog.acolyer.org/2016/04/26/the-log-what-every-software-engineer-should-know-about-real-time-datas-unifying/',
            'https://queue.acm.org/detail.cfm?id=1394128',  # Eventually Consistent - Werner Vogels
        ],
        
        # 🎮 Gaming (verified URLs)
        'roblox': [
            'https://blog.roblox.com/2021/01/scaling-backend-infrastructure-multi-dc/',
            'https://blog.roblox.com/2020/05/scaling-backend-infrastructure/',
        ],
        
        'epicgames': [
            'https://www.unrealengine.com/en-US/blog/the-technology-behind-fortnites-cross-platform-play',
        ],
        
        # 📊 Data Infrastructure (verified working URLs)
        'databricks': [
            'https://databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html',
            'https://databricks.com/blog/2018/10/29/open-sourcing-delta-lake.html',
        ],
        
        'snowflake': [
            'https://www.snowflake.com/blog/how-foundational-technologies-create-cloud-data-platforms/',
        ],
        
        # 🔄 Infrastructure Tools (verified)
        'hashicorp': [
            'https://www.hashicorp.com/blog/raft-consensus-algorithm',
            'https://www.hashicorp.com/blog/consul-gossip-protocol',
        ],
        
        'docker': [
            'https://docs.docker.com/engine/architecture/',
            'https://www.docker.com/blog/how-docker-desktop-networking-works-under-the-hood/',
        ],
        
        # 🌐 CDN and Performance (verified)
        'fastly': [
            'https://www.fastly.com/blog/building-and-scaling-fastly-network-part-1-fighting-fib',
            'https://www.fastly.com/blog/building-and-scaling-fastly-network-part-2-balancing-requests',
        ],
        
        'cloudflare': [
            'https://blog.cloudflare.com/cloudflare-architecture-and-how-bpf-eats-the-world/',
            'https://blog.cloudflare.com/how-we-built-spectrum/',
        ],
        
        # 💾 Database Systems (specific technical articles)
        'mongodb': [
            'https://www.mongodb.com/blog/post/building-with-patterns-a-summary',
            'https://www.mongodb.com/blog/post/building-with-patterns-the-bucket-pattern',
        ],
        
        'redis': [
            'https://redis.io/docs/manual/replication/',
            'https://redis.io/docs/manual/sentinel/',
        ],
        
        # 🚀 Startups with Excellent Technical Content
        'segment': [
            'https://segment.com/blog/a-brief-history-of-the-uuid/',
            'https://segment.com/blog/exactly-once-delivery/',
        ],
        
        'intercom': [
            'https://www.intercom.com/blog/scaling-side-projects/',
            'https://www.intercom.com/blog/how-we-build-software/',
        ],
        
        # 🔍 Search and Discovery
        'algolia': [
            'https://blog.algolia.com/inside-the-algolia-engine-part-1-nifi/',
            'https://blog.algolia.com/when-solid-state-drives-are-not-that-solid/',
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
        
        self.stats = {'attempted': 0, 'downloaded': 0, 'duplicates_skipped': 0, 'errors': 0}
    
    def extract_content_universal(self, soup):
        """Universal content extraction for any site type."""
        strategies = [
            # Research papers and technical docs
            lambda s: s.select_one('.paper-content'),
            lambda s: s.select_one('.research-content'),
            lambda s: s.select_one('.technical-content'),
            
            # Standard blog patterns
            lambda s: s.select_one('article'),
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('.entry-content'),
            lambda s: s.select_one('.content'),
            lambda s: s.select_one('main'),
            
            # Documentation patterns
            lambda s: s.select_one('.doc-content'),
            lambda s: s.select_one('.documentation'),
            lambda s: s.select_one('#content'),
            
            # Medium and modern platforms
            lambda s: s.select_one('.story-content'),
            lambda s: s.select_one('[data-testid="storyContent"]'),
            
            # AWS and cloud provider patterns
            lambda s: s.select_one('.blog-post-content'),
            lambda s: s.select_one('.blog-content'),
            
            # Fallback: largest meaningful content
            lambda s: max(
                (elem for elem in s.find_all(['div', 'section', 'article']) 
                 if len(elem.get_text(strip=True)) > 1500), 
                key=lambda x: len(x.get_text(strip=True)), 
                default=None
            )
        ]
        
        for strategy in strategies:
            try:
                content_elem = strategy(soup)
                if content_elem and len(content_elem.get_text(strip=True)) > 1500:
                    return content_elem
            except:
                continue
        
        return None
    
    def extract_title_universal(self, soup, url):
        """Universal title extraction."""
        strategies = [
            lambda s: s.select_one('h1'),
            lambda s: s.select_one('.post-title'),
            lambda s: s.select_one('.entry-title'),
            lambda s: s.select_one('.paper-title'),
            lambda s: s.select_one('title'),
            lambda s: s.select_one('.blog-post-title'),
            lambda s: s.select_one('h2'),
        ]
        
        for strategy in strategies:
            try:
                title_elem = strategy(soup)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if 8 < len(title) < 300:
                        # Clean up title
                        title = re.sub(r'\s+', ' ', title)
                        return title
            except:
                continue
        
        # Fallback from URL
        url_part = url.split('/')[-1].replace('-', ' ').replace('_', ' ')
        return url_part.title() or "Premium System Architecture Article"
    
    def download_manual_premium(self, company, url):
        """Download manually curated premium article."""
        try:
            self.stats['attempted'] += 1
            print(f"   📥 {url}")
            
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                print(f"   ❌ HTTP {response.status_code}")
                self.stats['errors'] += 1
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title and content
            title = self.extract_title_universal(soup, url)
            content_elem = self.extract_content_universal(soup)
            
            if not content_elem:
                print(f"   ❌ No content extracted")
                self.stats['errors'] += 1
                return False
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            h.single_line_break = False
            
            markdown_content = h.handle(str(content_elem))
            
            # Quality validation
            content_length = len(markdown_content.strip())
            if content_length < 1500:
                print(f"   ❌ Content too short ({content_length} chars)")
                self.stats['errors'] += 1
                return False
            
            # Check for duplicate
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate, skipping")
                self.stats['duplicates_skipped'] += 1
                return False
            
            # Create directory and save
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:75]}.md"
            filepath = company_dir / filename
            
            # Handle conflicts
            counter = 1
            while filepath.exists():
                filepath = company_dir / f"{safe_title[:70]}_{counter}.md"
                counter += 1
            
            # Premium frontmatter
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
content_length: {content_length}
type: "manual_premium_harvest"
premium: true
curated: true
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            self.existing_hashes.add(content_hash)
            self.stats['downloaded'] += 1
            
            print(f"   ✅ {title[:65]}... ({content_length} chars)")
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:80]}")
            self.stats['errors'] += 1
            return False
    
    def run_manual_harvest(self):
        """Run the manual premium harvest."""
        print("🎯 MANUAL PREMIUM SYSTEMS ARCHITECTURE HARVEST")
        print("=" * 70)
        print("📋 Manually curated premium articles from verified URLs")
        print("🏆 Focus: Highest quality technical content available")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing")
        print()
        print("Categories: 🏗️ Tech Giants, 🌍 International, 🔬 Open Source,")
        print("           🏦 Financial, 🎮 Gaming, 📊 Data, 🔄 Infrastructure")
        print()
        
        total_attempted = 0
        total_downloaded = 0
        
        for company, urls in self.PREMIUM_ARTICLES.items():
            print(f"\n🏢 {company.upper()}")
            print("-" * 50)
            
            downloaded = 0
            for url in urls:
                if self.download_manual_premium(company, url):
                    downloaded += 1
                    time.sleep(2)  # Respectful pause
                else:
                    time.sleep(1)
            
            print(f"   📊 Downloaded: {downloaded}/{len(urls)}")
            total_attempted += len(urls)
            total_downloaded += downloaded
            
            time.sleep(3)  # Brief company pause
        
        # Final summary
        print(f"\n🎯 MANUAL HARVEST COMPLETE")
        print("=" * 50)
        print(f"Attempted: {total_attempted}")
        print(f"Downloaded: {total_downloaded}")
        print(f"Duplicates Skipped: {self.stats['duplicates_skipped']}")
        print(f"Errors: {self.stats['errors']}")
        
        total_files = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total collection: {total_files} articles")
        
        if total_downloaded > 0:
            print(f"🏆 Added {total_downloaded} manually curated premium articles!")
            print("⭐ These represent the absolute best system architecture content")

def main():
    harvester = ManualPremiumHarvest()
    harvester.run_manual_harvest()

if __name__ == "__main__":
    main()