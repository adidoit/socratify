#!/usr/bin/env python3
"""
Elite Systems Architecture Articles Harvest

Targets the absolute elite, must-read system architecture articles
that are easily accessible and represent legendary technical content.
"""

import requests
import time
from pathlib import Path
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class EliteArticlesHarvest:
    """Harvest of elite system architecture articles."""
    
    # The absolute elite articles - legendary technical content
    ELITE_ARTICLES = {
        # 🏆 Legendary Technical Papers & Posts (Known Working URLs)
        'legendary': [
            'https://www.allthingsdistributed.com/2006/03/a_word_on_scalability.html',
            'https://www.allthingsdistributed.com/2007/10/amazons_dynamo.html', 
            'https://martinfowler.com/articles/microservices.html',
        ],
        
        # 🏗️ More from Top Companies (Specific URLs)
        'google_research': [
            'https://research.google/blog/spanner-googles-globally-distributed-database/',
            'https://research.google/blog/mapreduce-simplified-data-processing-on-large-clusters/',
        ],
        
        'aws_architecture': [
            'https://aws.amazon.com/blogs/architecture/amazon-aurora-under-the-hood-quorum-and-correlated-failure/',
        ],
        
        # 🌍 International Excellence (Working URLs)
        'international': [
            'https://medium.com/booking-com-development/150k-requests-second-peeking-under-the-hood-of-booking-coms-distributed-systems-a6e1e2ccef4b',
            'https://medium.com/klarna-engineering/real-time-data-infrastructure-at-klarna-40f4e06d02e2',
        ],
        
        # 🔬 High-Quality Open Source
        'open_source': [
            'https://kafka.apache.org/documentation/#design',
        ],
        
        # 🚀 Excellent Startup Engineering
        'startups': [
            'https://segment.com/blog/exactly-once-delivery/',
            'https://blog.algolia.com/inside-the-algolia-engine-part-1-nifi/',
        ],
        
        # 📊 Data Systems Excellence
        'data_systems': [
            'https://databricks.com/blog/2016/07/28/structured-streaming-in-apache-spark.html',
        ],
    }
    
    def __init__(self, blogs_dir="blogs"):
        self.blogs_dir = Path(blogs_dir)
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        self.stats = {'attempted': 0, 'downloaded': 0, 'duplicates': 0, 'errors': 0}
    
    def extract_content_fast(self, soup):
        """Fast content extraction."""
        selectors = [
            'article', '.post-content', '.entry-content', '.content', 
            'main', '.story-content', '#content'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem and len(elem.get_text(strip=True)) > 1000:
                return elem
        
        # Fallback
        for div in soup.find_all(['div', 'section']):
            if len(div.get_text(strip=True)) > 2000:
                return div
        
        return None
    
    def extract_title_fast(self, soup, url):
        """Fast title extraction."""
        for selector in ['h1', '.post-title', '.entry-title', 'title']:
            elem = soup.select_one(selector)
            if elem:
                title = elem.get_text(strip=True)
                if 5 < len(title) < 200:
                    return title
        
        # URL fallback
        return url.split('/')[-1].replace('-', ' ').title()
    
    def download_elite_article(self, category, url):
        """Download elite article with fast processing."""
        try:
            self.stats['attempted'] += 1
            print(f"   📥 {url.split('//')[-1].split('/')[0]}")
            
            response = self.session.get(url, timeout=8)
            if response.status_code != 200:
                print(f"   ❌ {response.status_code}")
                self.stats['errors'] += 1
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            title = self.extract_title_fast(soup, url)
            content_elem = self.extract_content_fast(soup)
            
            if not content_elem:
                print(f"   ❌ No content")
                self.stats['errors'] += 1
                return False
            
            # Quick markdown conversion
            h = html2text.HTML2Text()
            h.body_width = 0
            markdown_content = h.handle(str(content_elem))
            
            if len(markdown_content.strip()) < 800:
                print(f"   ❌ Too short")
                self.stats['errors'] += 1
                return False
            
            # Duplicate check
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate")
                self.stats['duplicates'] += 1
                return False
            
            # Save
            category_dir = self.blogs_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)
            
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filepath = category_dir / f"{safe_title[:70]}.md"
            
            counter = 1
            while filepath.exists():
                filepath = category_dir / f"{safe_title[:65]}_{counter}.md"
                counter += 1
            
            frontmatter = f"""---
title: "{title}"
category: "{category}"
url: "{url}"
type: "elite_systems_architecture"
elite: true
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            self.existing_hashes.add(content_hash)
            self.stats['downloaded'] += 1
            
            print(f"   ✅ {title[:50]}...")
            return True
            
        except Exception as e:
            print(f"   ❌ {str(e)[:40]}")
            self.stats['errors'] += 1
            return False
    
    def run_elite_harvest(self):
        """Run elite articles harvest."""
        print("🏆 ELITE SYSTEMS ARCHITECTURE HARVEST")
        print("=" * 60)
        print("🎯 Only the absolute best, legendary articles")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing")
        print()
        
        for category, urls in self.ELITE_ARTICLES.items():
            print(f"\n📚 {category.upper()}")
            print("-" * 30)
            
            for url in urls:
                self.download_elite_article(category, url)
                time.sleep(1)
            
            time.sleep(2)
        
        # Summary
        print(f"\n🏆 ELITE HARVEST COMPLETE")
        print("=" * 30)
        for k, v in self.stats.items():
            print(f"{k.title()}: {v}")
        
        total = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total: {total} articles")
        
        if self.stats['downloaded'] > 0:
            print(f"⭐ Added {self.stats['downloaded']} elite articles!")

def main():
    harvester = EliteArticlesHarvest()
    harvester.run_elite_harvest()

if __name__ == "__main__":
    main()