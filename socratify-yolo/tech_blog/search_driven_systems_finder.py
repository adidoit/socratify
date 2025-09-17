#!/usr/bin/env python3
"""
Search-Driven Systems Architecture Finder

Uses targeted web searches to find specific system architecture articles
from companies we know produce high-quality content.
"""

import requests
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class SearchDrivenSystemsFinder:
    """Find system articles using targeted searches and direct URLs."""
    
    # Working system architecture URLs we've identified
    VERIFIED_SYSTEM_ARTICLES = {
        'dropbox': [
            'https://dropbox.tech/machine-learning/creating-a-modern-ocr-pipeline-using-computer-vision-and-deep-learning',
            'https://dropbox.tech/infrastructure/how-we-rolled-out-one-of-the-largest-python-3-migrations-ever',
            'https://dropbox.tech/infrastructure/streaming-file-synchronization',
        ],
        'pinterest': [
            'https://medium.com/pinterest-engineering/sharding-pinterest-how-we-scaled-our-mysql-fleet-3f341e96ca6f',
            'https://medium.com/pinterest-engineering/building-a-real-time-user-action-counting-system-for-ads-b2a3cd8c2d8e',
            'https://medium.com/pinterest-engineering/how-pinterest-runs-kafka-at-scale-ff9c6f735be',
        ],
        'shopify': [
            'https://shopify.engineering/how-shopify-reduced-storefront-response-times-rewrite',
            'https://shopify.engineering/kafka-connect-debezium',
            'https://shopify.engineering/building-resilient-payment-systems',
        ],
        'stripe': [
            'https://stripe.com/blog/online-migrations',  
            'https://stripe.com/blog/rate-limiters',
            'https://stripe.com/blog/canonical-log-lines',
            'https://stripe.com/blog/designing-robust-and-predictable-apis-with-idempotency',
        ],
        'cloudflare': [
            'https://blog.cloudflare.com/the-relative-performance-of-c-and-rust/',
            'https://blog.cloudflare.com/how-we-built-spectrum/',
            'https://blog.cloudflare.com/dns-resolver-1-1-1-1/',
        ],
        'linkedin': [
            'https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying',
            'https://engineering.linkedin.com/kafka/running-kafka-scale', 
            'https://engineering.linkedin.com/architecture/brief-history-scaling-linkedin',
        ],
        'spotify': [
            'https://engineering.atspotify.com/2021/11/spotifys-journey-to-event-driven-architecture/',
            'https://engineering.atspotify.com/2020/01/how-we-improved-our-performance-culture/',
        ],
        'airbnb': [
            'https://medium.com/airbnb-engineering/dynein-building-a-distributed-delayed-job-queueing-system-93ab10f05f99',
            'https://medium.com/airbnb-engineering/airpal-a-web-based-query-execution-tool-for-facebook-presto-82b3ea6e3b7b',
        ],
        'datadog': [
            'https://www.datadoghq.com/blog/engineering/introducing-glommio/',
            'https://www.datadoghq.com/blog/engineering/benefits-of-rust-for-infrastructure/',
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
    
    def extract_content_with_multiple_strategies(self, soup, url):
        """Try multiple content extraction strategies."""
        strategies = [
            # Strategy 1: Standard article selectors
            lambda s: s.select_one('article'),
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('.entry-content'),
            
            # Strategy 2: Medium-specific
            lambda s: s.select_one('article div[data-testid="storyContent"]'),
            lambda s: s.select_one('.story-content'),
            lambda s: s.select_one('.postArticle-content'),
            
            # Strategy 3: Blog-specific patterns
            lambda s: s.select_one('main'),
            lambda s: s.select_one('.content'),
            lambda s: s.select_one('[role="main"]'),
            
            # Strategy 4: By text length (fallback)
            lambda s: max((div for div in s.find_all('div') 
                          if len(div.get_text(strip=True)) > 1000), 
                         key=lambda x: len(x.get_text(strip=True)), default=None)
        ]
        
        for strategy in strategies:
            try:
                content_elem = strategy(soup)
                if content_elem and len(content_elem.get_text(strip=True)) > 1000:
                    return content_elem
            except:
                continue
        
        return None
    
    def extract_title_with_strategies(self, soup):
        """Extract title using multiple strategies."""
        strategies = [
            lambda s: s.select_one('h1'),
            lambda s: s.select_one('.post-title'),
            lambda s: s.select_one('.entry-title'), 
            lambda s: s.select_one('title'),
            lambda s: s.select_one('h2'),  # Fallback
        ]
        
        for strategy in strategies:
            try:
                title_elem = strategy(soup)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if len(title) > 5 and len(title) < 200:
                        return title
            except:
                continue
        
        return "System Architecture Article"
    
    def download_verified_article(self, company, url):
        """Download and save a verified article URL."""
        try:
            self.stats['attempted'] += 1
            print(f"   📥 Downloading: {url}")
            
            response = self.session.get(url, timeout=15, verify=False)
            if response.status_code != 200:
                print(f"   ❌ Status {response.status_code}")
                self.stats['errors'] += 1
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self.extract_title_with_strategies(soup)
            
            # Extract content with multiple strategies
            content_elem = self.extract_content_with_multiple_strategies(soup, url)
            
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
            
            # Quality check
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
            
            # Create directory and filename
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:70]}.md"
            filepath = company_dir / filename
            
            # Avoid filename conflicts
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
type: "system_architecture"
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            self.existing_hashes.add(content_hash)
            self.stats['downloaded'] += 1
            
            print(f"   ✅ Saved: {title[:60]}...")
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            self.stats['errors'] += 1
            return False
    
    def run_search_driven_download(self):
        """Run the search-driven download process."""
        print("🔍 SEARCH-DRIVEN SYSTEMS ARCHITECTURE FINDER")
        print("=" * 55)
        print(f"🎯 Target: Verified system architecture articles")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing")
        print(f"🏢 Companies: {len(self.VERIFIED_SYSTEM_ARTICLES)}")
        print()
        
        for company, urls in self.VERIFIED_SYSTEM_ARTICLES.items():
            print(f"\n🏢 {company.upper()}")
            print("-" * 35)
            
            downloaded_count = 0
            
            for url in urls:
                success = self.download_verified_article(company, url)
                if success:
                    downloaded_count += 1
                    time.sleep(2)  # Respectful pause
                else:
                    time.sleep(1)  # Brief pause on failure
            
            print(f"   📊 Downloaded {downloaded_count}/{len(urls)} articles")
            
            # Longer pause between companies
            time.sleep(3)
        
        # Final statistics
        print(f"\n✅ SEARCH-DRIVEN DOWNLOAD COMPLETE")
        print("=" * 40)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        total_files = len(list(self.blogs_dir.rglob('*.md')))
        print(f"📚 Total articles in collection: {total_files}")
        
        if self.stats['downloaded'] > 0:
            print(f"\n🎉 Successfully added {self.stats['downloaded']} new system architecture articles!")

def main():
    finder = SearchDrivenSystemsFinder()
    finder.run_search_driven_download()

if __name__ == "__main__":
    main()