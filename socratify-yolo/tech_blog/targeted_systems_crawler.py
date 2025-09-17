#!/usr/bin/env python3
"""
Targeted Systems Architecture Crawler

Focuses on companies and URLs that we know have excellent system architecture content.
Uses more targeted approach with better error handling.
"""

import requests
import time
import random
from pathlib import Path
from urllib.parse import urljoin, urlparse
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator
import ssl
import urllib3

# Disable SSL warnings for problematic sites
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TargetedSystemsCrawler:
    """Targeted crawler for system architecture articles."""
    
    # High-value system architecture URLs we know work
    TARGET_URLS = {
        'dropbox': [
            'https://dropbox.tech/',
            'https://dropbox.tech/infrastructure',  
            'https://dropbox.tech/backend',
            'https://dropbox.tech/data',
        ],
        'pinterest': [
            'https://medium.com/pinterest-engineering',
            'https://medium.com/pinterest-engineering/tagged/infrastructure',
            'https://medium.com/pinterest-engineering/tagged/data-engineering',
            'https://medium.com/pinterest-engineering/tagged/architecture',
        ],
        'shopify': [
            'https://shopify.engineering/',
            'https://shopify.engineering/topics/infrastructure',
            'https://shopify.engineering/topics/data',  
            'https://shopify.engineering/topics/backend',
        ],
        'stripe': [
            'https://stripe.com/blog/engineering',
            'https://stripe.com/blog/engineering?tags=infrastructure',
            'https://stripe.com/blog/engineering?tags=scaling',
        ],
        'linkedin': [
            'https://engineering.linkedin.com/blog',
            'https://engineering.linkedin.com/distributed-systems',
            'https://engineering.linkedin.com/data',
            'https://engineering.linkedin.com/infrastructure',
        ],
        'spotify': [
            'https://engineering.atspotify.com/',
            'https://engineering.atspotify.com/category/data/',
            'https://engineering.atspotify.com/category/backend/',
        ],
        'facebook': [
            'https://engineering.fb.com/',
            'https://engineering.fb.com/category/core-infra/',
            'https://engineering.fb.com/category/data-infrastructure/',
        ],
        'cloudflare': [
            'https://blog.cloudflare.com/',
            'https://blog.cloudflare.com/tag/deep-dive/',
            'https://blog.cloudflare.com/tag/architecture/',
            'https://blog.cloudflare.com/tag/performance/',
        ],
        'datadog': [
            'https://www.datadoghq.com/blog/engineering/',
            'https://www.datadoghq.com/blog/category/engineering/',
        ],
        'hashicorp': [
            'https://www.hashicorp.com/blog/engineering',
            'https://www.hashicorp.com/blog/category/engineering',
        ]
    }
    
    SYSTEM_KEYWORDS = {
        # Core system indicators
        'architecture': 15, 'system': 12, 'infrastructure': 15, 'scalability': 15,
        'distributed': 20, 'microservices': 18, 'database': 12, 'pipeline': 15,
        'how we built': 25, 'building our': 22, 'designing our': 20,
        'technical deep dive': 25, 'system design': 20, 'at scale': 22,
        'performance': 12, 'optimization': 15, 'migration': 18,
        'real-time': 15, 'streaming': 15, 'api': 10, 'service': 10,
        'lessons learned': 20, 'case study': 18, 'deep dive': 20,
        'engineering challenges': 18, 'scaling': 15, 'load balancing': 15,
        'fault tolerance': 18, 'consistency': 15, 'sharding': 15,
        'caching': 12, 'storage': 12, 'messaging': 12, 'queue': 12,
    }
    
    def __init__(self, blogs_dir="blogs", max_per_company=10):
        self.blogs_dir = Path(blogs_dir)
        self.max_per_company = max_per_company
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        # Setup session with better error handling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
        
        # Stats
        self.stats = {
            'companies_crawled': 0,
            'urls_explored': 0, 
            'articles_found': 0,
            'high_quality_downloaded': 0,
            'duplicates_skipped': 0,
            'errors': 0,
        }
    
    def calculate_system_score(self, title, description=""):
        """Calculate system architecture score."""
        text = f"{title} {description}".lower()
        score = 0
        
        for keyword, points in self.SYSTEM_KEYWORDS.items():
            if keyword in text:
                count = text.count(keyword)
                score += points * min(count, 2)  # Cap multiplier
        
        # Bonus for specific system phrases
        if any(phrase in text for phrase in [
            'how we built', 'building our', 'designing our', 'technical deep dive',
            'lessons from building', 'scaling our', 'migrating our', 'at scale'
        ]):
            score += 20
        
        # Performance metrics bonus
        if re.search(r'\d+[kmg]?\s*(qps|rps|ops|requests)', text):
            score += 15
            
        return score
    
    def fetch_url_safely(self, url):
        """Fetch URL with comprehensive error handling."""
        try:
            print(f"   🌐 Fetching: {url}")
            
            response = self.session.get(
                url, 
                timeout=10,
                verify=False,  # Skip SSL verification for problematic sites
                allow_redirects=True
            )
            
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            else:
                print(f"   ⚠️  Status {response.status_code}: {url}")
                return None
                
        except Exception as e:
            print(f"   ❌ Error fetching {url}: {str(e)[:100]}")
            self.stats['errors'] += 1
            return None
    
    def extract_articles_from_page(self, soup, base_url):
        """Extract article information from a page."""
        articles = []
        
        if not soup:
            return articles
        
        # Multiple selectors for different site structures
        article_selectors = [
            # Generic article selectors
            'article h1 a', 'article h2 a', 'article h3 a',
            '.post-title a', '.entry-title a', '.blog-post-title a',
            
            # Medium-specific
            'h2[data-testid="post-preview-title"] a',
            'article [data-testid="post-preview-title"]',
            
            # Site-specific patterns
            '.post h2 a', '.entry h2 a', '.blog-item h2 a',
            '.content h2 a', '.article-title a',
            
            # Fallback broad selectors
            'h1 a[href*="/"]', 'h2 a[href*="/"]', 'h3 a[href*="/"]'
        ]
        
        found_links = set()
        
        for selector in article_selectors:
            for link in soup.select(selector):
                href = link.get('href')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                # Make absolute URL
                if href.startswith('/'):
                    article_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    article_url = href
                else:
                    continue
                
                # Avoid duplicates
                if article_url in found_links:
                    continue
                found_links.add(article_url)
                
                # Get description from nearby elements
                description = self.extract_description(link)
                
                # Score the article
                score = self.calculate_system_score(title, description)
                
                if score >= 25:  # High threshold for system content
                    articles.append({
                        'url': article_url,
                        'title': title,
                        'description': description,
                        'score': score
                    })
        
        return articles
    
    def extract_description(self, link_element):
        """Extract article description from nearby elements."""
        descriptions = []
        
        # Look in parent elements for description
        parent = link_element.find_parent()
        if parent:
            # Common description selectors
            desc_selectors = ['.excerpt', '.summary', '.description', '.subtitle', 'p']
            
            for selector in desc_selectors:
                desc_elem = parent.select_one(selector)
                if desc_elem:
                    desc_text = desc_elem.get_text(strip=True)
                    if len(desc_text) > 30:
                        descriptions.append(desc_text[:300])
        
        return ' '.join(descriptions)
    
    def download_article(self, company, article):
        """Download and save an article."""
        try:
            url = article['url']
            title = article['title']
            score = article['score']
            
            print(f"   📥 Downloading (score: {score}): {title[:60]}...")
            
            soup = self.fetch_url_safely(url)
            if not soup:
                return False
            
            # Extract main content
            content_selectors = [
                'article', '.post-content', '.entry-content', '.content',
                'main', '.blog-post-content', '[role="main"]', '.post-body',
                '.story-content', '.postArticle-content'  # Medium-specific
            ]
            
            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem and len(content_elem.get_text(strip=True)) > 500:
                    break
            
            if not content_elem:
                print(f"   ❌ Could not extract content from {url}")
                return False
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            h.ignore_emphasis = False
            
            markdown_content = h.handle(str(content_elem))
            
            # Check for duplicate
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate detected, skipping")
                self.stats['duplicates_skipped'] += 1
                return False
            
            # Validate content quality
            if len(markdown_content.strip()) < 1000:
                print(f"   ❌ Content too short, skipping")
                return False
            
            # Create company directory
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            # Create safe filename
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:70]}.md"
            filepath = company_dir / filename
            
            # Create frontmatter
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
system_score: {score}
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            # Update tracking
            self.existing_hashes.add(content_hash)
            self.stats['high_quality_downloaded'] += 1
            
            print(f"   ✅ Saved: {filepath}")
            return True
            
        except Exception as e:
            print(f"   ❌ Error downloading {article.get('title', 'unknown')}: {e}")
            return False
    
    def crawl_company(self, company, urls):
        """Crawl all URLs for a company."""
        print(f"\n🏢 {company.upper()}")
        print("-" * 50)
        
        all_articles = []
        
        for url in urls[:4]:  # Limit URLs per company
            soup = self.fetch_url_safely(url)
            self.stats['urls_explored'] += 1
            
            if soup:
                articles = self.extract_articles_from_page(soup, url)
                all_articles.extend(articles)
                print(f"   📄 Found {len(articles)} system articles from {url}")
            
            # Respectful crawling
            time.sleep(random.uniform(2, 4))
        
        if not all_articles:
            print("   📭 No high-quality system articles found")
            return
        
        # Sort by score and take top articles
        all_articles.sort(key=lambda x: x['score'], reverse=True)
        top_articles = all_articles[:self.max_per_company]
        
        self.stats['articles_found'] += len(top_articles)
        print(f"   🎯 Selected {len(top_articles)} top articles (scores: {[a['score'] for a in top_articles[:3]]}...)")
        
        # Download articles
        downloaded = 0
        for article in top_articles:
            if self.download_article(company, article):
                downloaded += 1
            
            time.sleep(random.uniform(1, 3))
        
        print(f"   ✅ Successfully downloaded {downloaded}/{len(top_articles)} articles")
        self.stats['companies_crawled'] += 1
    
    def run_targeted_crawl(self):
        """Run the complete targeted crawl."""
        print("🎯 TARGETED SYSTEMS ARCHITECTURE CRAWL")
        print("=" * 60)
        print(f"🏢 Target companies: {len(self.TARGET_URLS)}")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing articles")
        print(f"📊 Quality threshold: 25+ system score")
        print(f"📝 Max per company: {self.max_per_company}")
        print()
        
        for company, urls in self.TARGET_URLS.items():
            self.crawl_company(company, urls)
            
            # Longer pause between companies
            time.sleep(random.uniform(4, 7))
        
        # Final statistics
        print("\n" + "=" * 60)
        print("📊 CRAWL COMPLETE")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        final_count = len(list(self.blogs_dir.rglob('*.md')))
        print(f"📚 Total articles in collection: {final_count}")

def main():
    crawler = TargetedSystemsCrawler(max_per_company=12)
    crawler.run_targeted_crawl()

if __name__ == "__main__":
    main()