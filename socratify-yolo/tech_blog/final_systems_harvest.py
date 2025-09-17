#!/usr/bin/env python3
"""
Final Systems Architecture Harvest

Targets the most accessible and legendary system architecture articles
with optimized extraction and error handling.
"""

import requests
import time
from pathlib import Path
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class FinalSystemsHarvest:
    """Final harvest of accessible legendary system architecture articles."""
    
    # Most accessible legendary articles (verified working URLs)
    ACCESSIBLE_LEGENDARY = {
        # High Success Rate Sources
        'engineering': [
            # High Scalability (aggregator of system design articles)
            'http://highscalability.com/blog/2016/1/25/design-of-a-modern-cache.html',
            'http://highscalability.com/blog/2012/5/16/27-things-i-learned-about-databases-last-year.html',
            
            # Individual legendary posts that usually work
            'https://martinfowler.com/articles/microservices.html',
            'https://martinfowler.com/bliki/EventSourcing.html',
            'https://martinfowler.com/articles/patterns-of-distributed-systems/',
        ],
        
        'whatsapp': [
            # WhatsApp's famous scaling posts
            'https://www.wired.com/2015/09/whatsapp-serves-900-million-users-50-engineers/',
        ],
        
        'instagram': [
            # Instagram's classic scaling posts
            'https://instagram-engineering.com/what-powers-instagram-hundreds-of-instances-dozens-of-technologies-adf2e22da2ad',
        ],
        
        'basecamp': [
            # DHH and Basecamp's architecture posts
            'https://signalvnoise.com/posts/3113-how-key-based-cache-expiration-works',
            'https://world.hey.com/dhh/the-one-person-framework-711e6318',
        ],
        
        'shopify': [
            # Additional Shopify engineering posts
            'https://shopify.engineering/defining-component-apis-in-ruby-and-typescript',
            'https://shopify.engineering/faster-shopify-cli-plugin-development-with-better-tooling',
        ],
        
        'heroku': [
            # Heroku's classic architecture posts
            'https://blog.heroku.com/archives/2013/7/10/cedar-14-public-beta',
            'https://devcenter.heroku.com/articles/http-routing',
        ],
        
        'github': [
            # Additional GitHub engineering posts that might work
            'https://github.blog/2022-08-15-the-complete-guide-to-full-stack-web3-development/',
            'https://github.blog/2022-06-15-how-we-think-about-browsers/',
        ],
    }
    
    def __init__(self, blogs_dir="blogs"):
        self.blogs_dir = Path(blogs_dir)
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        })
        
        self.stats = {'attempted': 0, 'downloaded': 0, 'duplicates_skipped': 0, 'errors': 0}
    
    def extract_content_flexible(self, soup):
        """Flexible content extraction for various blog types."""
        strategies = [
            # Standard blog patterns
            lambda s: s.select_one('article'),
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('.entry-content'),
            lambda s: s.select_one('.content'),
            lambda s: s.select_one('main'),
            lambda s: s.select_one('#main'),
            
            # Medium and modern blogs
            lambda s: s.select_one('.story-content'),
            lambda s: s.select_one('[data-testid="storyContent"]'),
            
            # Older blog patterns
            lambda s: s.select_one('.post'),
            lambda s: s.select_one('.entry'),
            lambda s: s.select_one('#post'),
            
            # Fallback: find largest text block
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
    
    def extract_title_flexible(self, soup, url):
        """Flexible title extraction."""
        strategies = [
            lambda s: s.select_one('h1'),
            lambda s: s.select_one('.post-title'),
            lambda s: s.select_one('.entry-title'),
            lambda s: s.select_one('title'),
            lambda s: s.select_one('h2'),
        ]
        
        for strategy in strategies:
            try:
                title_elem = strategy(soup)
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if 8 < len(title) < 200:
                        return title
            except:
                continue
        
        # Fallback from URL
        url_part = url.split('/')[-1].replace('-', ' ').replace('_', ' ')
        return url_part.title() or "System Architecture Article"
    
    def download_final_article(self, company, url):
        """Download with optimized error handling."""
        try:
            self.stats['attempted'] += 1
            print(f"   📥 {url}")
            
            # Quick timeout to avoid hanging
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                print(f"   ❌ HTTP {response.status_code}")
                self.stats['errors'] += 1
                return False
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract content and title
            title = self.extract_title_flexible(soup, url)
            content_elem = self.extract_content_flexible(soup)
            
            if not content_elem:
                print(f"   ❌ No content extracted")
                self.stats['errors'] += 1
                return False
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.body_width = 0
            markdown_content = h.handle(str(content_elem))
            
            # Quick validation
            if len(markdown_content.strip()) < 1000:
                print(f"   ❌ Content too short")
                self.stats['errors'] += 1
                return False
            
            # Check duplicate
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate, skipping")
                self.stats['duplicates_skipped'] += 1
                return False
            
            # Save file
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:70]}.md"
            filepath = company_dir / filename
            
            # Handle conflicts
            counter = 1
            while filepath.exists():
                filepath = company_dir / f"{safe_title[:65]}_{counter}.md"
                counter += 1
            
            # Write with frontmatter
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
type: "final_harvest"
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            self.existing_hashes.add(content_hash)
            self.stats['downloaded'] += 1
            
            print(f"   ✅ {title[:60]}...")
            return True
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:60]}")
            self.stats['errors'] += 1
            return False
    
    def run_final_harvest(self):
        """Run the final harvest of system architecture articles."""
        print("🌾 FINAL SYSTEMS ARCHITECTURE HARVEST")
        print("=" * 60)
        print("🎯 Target: Most accessible legendary articles")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing")
        print("⚡ Quick extraction, optimized for success")
        print()
        
        for company, urls in self.ACCESSIBLE_LEGENDARY.items():
            print(f"\n🏢 {company.upper()}")
            print("-" * 40)
            
            downloaded = 0
            for url in urls:
                if self.download_final_article(company, url):
                    downloaded += 1
                    time.sleep(1.5)  # Quick pause
                else:
                    time.sleep(0.5)
            
            print(f"   📊 Success: {downloaded}/{len(urls)}")
            time.sleep(2)  # Brief company pause
        
        # Final stats
        print(f"\n🌾 FINAL HARVEST COMPLETE")
        print("=" * 40)
        for key, value in self.stats.items():
            print(f"{key.title()}: {value}")
        
        total_files = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total collection: {total_files} articles")
        
        if self.stats['downloaded'] > 0:
            print(f"🎉 Added {self.stats['downloaded']} more legendary articles!")

def main():
    harvester = FinalSystemsHarvest()
    harvester.run_final_harvest()

if __name__ == "__main__":
    main()