#!/usr/bin/env python3
"""
Quick Systems Architecture Article Finder

Fast, targeted approach to find specific system architecture articles
from companies we already have content from.
"""

import requests
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class QuickSystemsFinder:
    """Quick finder for additional system architecture articles."""
    
    # Specific high-value URLs we know have system articles
    DIRECT_SYSTEM_URLS = {
        'dropbox': [
            'https://dropbox.tech/infrastructure/rewriting-the-heart-of-our-sync-engine',
            'https://dropbox.tech/infrastructure/atlas--our-journey-from-a-python-monolith-to-a-managed-platform',
            'https://dropbox.tech/infrastructure/how-we-migrated-dropbox-from-nginx-to-envoy',
            'https://dropbox.tech/backend/creating-a-modern-ocr-pipeline-using-computer-vision-and-deep-learning',
        ],
        'pinterest': [
            'https://medium.com/pinterest-engineering/how-pinterest-powers-a-healthy-comment-ecosystem-with-machine-learning-f9d06e2b83c1',
            'https://medium.com/pinterest-engineering/building-pinterests-a-b-testing-platform-ab4934ace9f4',
            'https://medium.com/pinterest-engineering/scaling-kubernetes-to-7500-nodes-2a1ab30767fb',
            'https://medium.com/pinterest-engineering/how-we-built-a-general-purpose-key-value-store-for-facebook-with-zippydb-9a5837adf57',
        ],
        'stripe': [
            'https://stripe.com/blog/online-migrations',
            'https://stripe.com/blog/rate-limiters',
            'https://stripe.com/blog/canonical-log-lines',
            'https://stripe.com/blog/idempotency',
        ],
        'shopify': [
            'https://shopify.engineering/how-shopify-reduced-storefront-response-times-rewrite',
            'https://shopify.engineering/building-data-pipeline-with-kafka-connect-and-debezium',
            'https://shopify.engineering/building-resilient-graphql-apis',
        ],
        'cloudflare': [
            'https://blog.cloudflare.com/how-cloudflare-auto-mitigated-world-record-312-million-rps-ddos-attack/',
            'https://blog.cloudflare.com/inside-the-infamous-mirai-iot-botnet-a-retrospective-analysis/',
            'https://blog.cloudflare.com/architecture-of-cloudflares-new-sql-based-analytics-api/',
            'https://blog.cloudflare.com/building-fast-interpreters-in-rust/',
        ],
        'linkedin': [
            'https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying',
            'https://engineering.linkedin.com/kafka/running-kafka-scale',
            'https://engineering.linkedin.com/architecture/brief-history-scaling-linkedin',
        ],
        'facebook': [
            'https://engineering.fb.com/2021/03/22/production-engineering/how-facebook-encodes-your-videos/',
            'https://engineering.fb.com/2021/06/21/data-infrastructure/mysql/',
            'https://engineering.fb.com/2020/12/09/data-infrastructure/messenger/',
        ],
        'spotify': [
            'https://engineering.atspotify.com/2022/03/how-we-improved-data-discovery-for-data-scientists-at-spotify/',
            'https://engineering.atspotify.com/2021/11/spotifys-journey-to-event-driven-architecture/',
        ],
        'datadog': [
            'https://www.datadoghq.com/blog/engineering/how-we-collect-and-standardize-kubernetes-resource-metrics/',
            'https://www.datadoghq.com/blog/engineering/introducing-glommio/',
        ]
    }
    
    def __init__(self, blogs_dir="blogs"):
        self.blogs_dir = Path(blogs_dir)
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        self.stats = {'downloaded': 0, 'duplicates_skipped': 0, 'errors': 0}
    
    def download_specific_article(self, company, url):
        """Download a specific article URL."""
        try:
            print(f"   📥 Downloading: {url}")
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_selectors = ['h1', 'title', '.post-title', '.entry-title']
            title = "System Architecture Article"
            
            for selector in title_selectors:
                title_elem = soup.select_one(selector)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if len(title) > 10:
                        break
            
            # Extract main content
            content_selectors = [
                'article', '.post-content', '.entry-content', '.content',
                'main', '.story-content', '.postArticle-content'
            ]
            
            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem and len(content_elem.get_text(strip=True)) > 500:
                    break
            
            if not content_elem:
                print(f"   ❌ Could not extract content")
                return False
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            
            markdown_content = h.handle(str(content_elem))
            
            # Check for duplicate
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate detected, skipping")
                self.stats['duplicates_skipped'] += 1
                return False
            
            # Validate content
            if len(markdown_content.strip()) < 800:
                print(f"   ❌ Content too short")
                return False
            
            # Create directory and file
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:60]}.md"
            filepath = company_dir / filename
            
            # Write with frontmatter
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
type: "system_architecture"
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            self.existing_hashes.add(content_hash)
            self.stats['downloaded'] += 1
            
            print(f"   ✅ Saved: {title[:50]}...")
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:80]}")
            self.stats['errors'] += 1
            return False
    
    def run_quick_download(self):
        """Download specific high-value system articles."""
        print("⚡ QUICK SYSTEMS ARCHITECTURE FINDER")
        print("=" * 50)
        print(f"🎯 Target: Specific high-value system articles")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing")
        print()
        
        for company, urls in self.DIRECT_SYSTEM_URLS.items():
            print(f"\n🏢 {company.upper()}")
            print("-" * 30)
            
            for url in urls:
                success = self.download_specific_article(company, url)
                if success:
                    time.sleep(2)  # Brief pause between downloads
                else:
                    time.sleep(1)
        
        # Final stats
        print(f"\n✅ DOWNLOAD COMPLETE")
        print("=" * 30)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        total_files = len(list(self.blogs_dir.rglob('*.md')))
        print(f"📚 Total articles: {total_files}")

def main():
    finder = QuickSystemsFinder()
    finder.run_quick_download()

if __name__ == "__main__":
    main()