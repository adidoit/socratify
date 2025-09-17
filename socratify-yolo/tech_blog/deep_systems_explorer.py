#!/usr/bin/env python3
"""
Deep Systems Architecture Blog Explorer

Specifically targets high-quality engineering system architecture articles 
that discuss specific systems, design decisions, and technical implementations.
Goes beyond RSS feeds to find comprehensive system design content.
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

class SystemArchitectureFilter:
    """Enhanced filter specifically for system architecture content."""
    
    SYSTEM_KEYWORDS = {
        # Core system design concepts
        'architecture': 15, 'system': 12, 'infrastructure': 12, 'platform': 10,
        'scalability': 12, 'performance': 10, 'distributed': 15, 'microservices': 15,
        'database': 12, 'storage': 10, 'caching': 12, 'load balancing': 12,
        
        # Specific technical implementations
        'design decisions': 20, 'technical decisions': 18, 'implementation': 15,
        'engineering': 12, 'built': 15, 'designed': 12, 'developed': 10,
        'migration': 15, 'scaling': 15, 'optimization': 12,
        
        # System components
        'api': 10, 'service': 12, 'pipeline': 15, 'framework': 12,
        'real-time': 15, 'streaming': 15, 'messaging': 12, 'queue': 10,
        'search': 10, 'recommendation': 12, 'ml infrastructure': 20,
        
        # Specific technologies that indicate deep systems content
        'kubernetes': 12, 'docker': 10, 'kafka': 15, 'redis': 12,
        'postgresql': 12, 'mongodb': 10, 'elasticsearch': 12,
        'graphql': 10, 'grpc': 12, 'protobuf': 10,
        
        # High-value system design terms
        'at scale': 20, 'high availability': 18, 'fault tolerance': 18,
        'consistency': 15, 'eventual consistency': 18, 'cap theorem': 20,
        'sharding': 15, 'partitioning': 15, 'replication': 12,
        
        # Problem-solving and decision-making
        'challenges': 15, 'lessons learned': 20, 'tradeoffs': 18,
        'why we': 15, 'how we': 15, 'our approach': 15,
        'deep dive': 20, 'case study': 18, 'postmortem': 20,
    }
    
    EXCLUDE_KEYWORDS = {
        'marketing': -20, 'sales': -15, 'hiring': -10, 'culture': -8,
        'announcement': -15, 'press release': -20, 'event': -8,
        'conference': -5, 'meetup': -5, 'webinar': -10,
        'partnership': -12, 'acquisition': -15, 'funding': -20,
        'product launch': -15, 'feature announcement': -12,
        'newsletter': -10, 'recap': -5, 'trends': -8,
        'predictions': -10, 'opinion': -8, 'thought leadership': -15,
    }
    
    def calculate_system_score(self, title, content_preview):
        """Calculate score specifically for system architecture content."""
        text = f"{title} {content_preview}".lower()
        score = 0
        
        # Positive system keywords
        for keyword, points in self.SYSTEM_KEYWORDS.items():
            if keyword in text:
                # Bonus for multiple mentions
                count = text.count(keyword)
                score += points * min(count, 3)  # Cap at 3x multiplier
        
        # Negative keywords
        for keyword, penalty in self.EXCLUDE_KEYWORDS.items():
            if keyword in text:
                score += penalty
        
        # Bonus for specific system-building phrases
        system_phrases = [
            'how we built', 'building our', 'designing our', 'our system',
            'technical deep dive', 'architecture overview', 'system design',
            'lessons from building', 'scaling our', 'migrating our'
        ]
        
        for phrase in system_phrases:
            if phrase in text:
                score += 25  # High bonus for system-specific phrases
        
        # Bonus for technical metrics and specifics
        if re.search(r'\d+[kmg]?\s*(qps|rps|ops|requests|queries)', text):
            score += 15  # Technical performance metrics
        
        if re.search(r'\d+[kmgtpz]b\s*(storage|data|memory)', text):
            score += 12  # Data scale indicators
        
        return max(0, score)

class DeepSystemsExplorer:
    """Deep exploration of system architecture articles."""
    
    # Target companies with known excellent system blogs
    COMPANIES_WITH_DEEP_SYSTEMS = {
        'uber': {
            'base_url': 'https://www.uber.com/en-US/blog/engineering/',
            'patterns': [
                '/engineering/page/{}',  # Pagination
                '/engineering/category/architecture/',
                '/engineering/category/infrastructure/',
                '/engineering/category/data/',
                '/engineering/category/backend/',
            ]
        },
        'netflix': {
            'base_url': 'https://netflixtechblog.com/',
            'patterns': [
                '?p={}',  # WordPress pagination
                '/tagged/infrastructure',
                '/tagged/architecture', 
                '/tagged/scalability',
                '/tagged/data-engineering',
            ]
        },
        'airbnb': {
            'base_url': 'https://medium.com/airbnb-engineering/',
            'patterns': [
                '?p={}',
                '/tagged/data-science',
                '/tagged/infrastructure',
                '/tagged/architecture',
            ]
        },
        'dropbox': {
            'base_url': 'https://dropbox.tech/',
            'patterns': [
                '/page/{}',
                '/infrastructure/',
                '/data/',
                '/backend/',
            ]
        },
        'pinterest': {
            'base_url': 'https://medium.com/pinterest-engineering/',
            'patterns': [
                '?p={}',
                '/tagged/infrastructure',
                '/tagged/data-engineering',
                '/tagged/architecture',
            ]
        },
        'linkedin': {
            'base_url': 'https://engineering.linkedin.com/blog/',
            'patterns': [
                '/page/{}',
                '/distributed-systems',
                '/data',
                '/infrastructure',
            ]
        },
        'facebook': {
            'base_url': 'https://engineering.fb.com/',
            'patterns': [
                '/page/{}',
                '/core-infra/',
                '/data-infrastructure/',
                '/backend/',
            ]
        },
        'spotify': {
            'base_url': 'https://engineering.atspotify.com/',
            'patterns': [
                '/page/{}',
                '/tag/infrastructure/',
                '/tag/data/',
                '/tag/backend/',
            ]
        },
        'shopify': {
            'base_url': 'https://shopify.engineering/',
            'patterns': [
                '/page/{}',
                '/topics/infrastructure',
                '/topics/data',
                '/topics/backend',
            ]
        },
        'stripe': {
            'base_url': 'https://stripe.com/blog/engineering/',
            'patterns': [
                '/page/{}',
                '/infrastructure',
                '/data',
                '/scaling',
            ]
        }
    }
    
    def __init__(self, blogs_dir="blogs", max_articles_per_company=15):
        self.blogs_dir = Path(blogs_dir)
        self.max_articles_per_company = max_articles_per_company
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        self.filter = SystemArchitectureFilter()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.stats = {
            'companies_explored': 0,
            'pages_crawled': 0,
            'articles_found': 0,
            'high_quality_downloaded': 0,
            'duplicates_skipped': 0,
        }
    
    def discover_system_articles(self, company, config):
        """Discover system architecture articles for a company."""
        print(f"🔍 Deep exploring {company} for system articles...")
        
        articles_found = []
        base_url = config['base_url']
        
        # Explore main pages and category pages
        urls_to_explore = [base_url]
        
        # Add pagination URLs
        for pattern in config['patterns']:
            if '{}' in pattern:
                # Pagination pattern
                for page in range(1, 6):  # Explore first 5 pages
                    if pattern.startswith('/'):
                        url = base_url.rstrip('/') + pattern.format(page)
                    else:
                        url = base_url + pattern.format(page)
                    urls_to_explore.append(url)
            else:
                # Category/tag pattern
                if pattern.startswith('/'):
                    url = base_url.rstrip('/') + pattern
                else:
                    url = base_url + pattern
                urls_to_explore.append(url)
        
        # Explore each URL
        for url in urls_to_explore[:10]:  # Limit to prevent excessive crawling
            try:
                print(f"   📄 Exploring: {url}")
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                self.stats['pages_crawled'] += 1
                
                # Find article links
                article_links = self.extract_article_links(soup, base_url)
                
                for article_url, article_title, preview in article_links:
                    # Score the article
                    score = self.filter.calculate_system_score(article_title, preview)
                    
                    if score >= 30:  # High threshold for system articles
                        articles_found.append({
                            'url': article_url,
                            'title': article_title,
                            'preview': preview,
                            'score': score
                        })
                        self.stats['articles_found'] += 1
                        
                        if len(articles_found) >= self.max_articles_per_company:
                            break
                
                # Respectful crawling
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                print(f"   ❌ Error exploring {url}: {e}")
                continue
            
            if len(articles_found) >= self.max_articles_per_company:
                break
        
        # Sort by score and return top articles
        articles_found.sort(key=lambda x: x['score'], reverse=True)
        return articles_found[:self.max_articles_per_company]
    
    def extract_article_links(self, soup, base_url):
        """Extract article links from a page."""
        links = []
        
        # Common selectors for article links
        selectors = [
            'article h2 a', 'article h3 a', '.post-title a',
            '.entry-title a', 'h1 a', 'h2 a', 'h3 a',
            'a[href*="/blog/"]', 'a[href*="/post/"]',
            'a[href*="/article/"]', '.blog-post-title a',
        ]
        
        for selector in selectors:
            for link in soup.select(selector):
                href = link.get('href')
                if not href:
                    continue
                
                # Convert relative URLs to absolute
                if href.startswith('/'):
                    article_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    article_url = href
                else:
                    continue
                
                title = link.get_text(strip=True)
                if not title or len(title) < 10:
                    continue
                
                # Get preview text from parent elements
                preview = self.extract_preview_text(link.find_parent())
                
                # Filter out obvious non-system articles
                if self.is_likely_system_article(title, preview):
                    links.append((article_url, title, preview))
        
        return list(set(links))  # Remove duplicates
    
    def extract_preview_text(self, element):
        """Extract preview text from article element."""
        if not element:
            return ""
        
        # Look for description/preview in nearby elements
        preview_selectors = ['.excerpt', '.summary', '.description', 'p']
        
        for selector in preview_selectors:
            preview_elem = element.select_one(selector)
            if preview_elem:
                preview = preview_elem.get_text(strip=True)
                if len(preview) > 50:
                    return preview[:500]  # Limit preview length
        
        # Fallback to element text
        text = element.get_text(strip=True)
        return text[:500] if len(text) > 50 else ""
    
    def is_likely_system_article(self, title, preview):
        """Quick filter for likely system articles."""
        text = f"{title} {preview}".lower()
        
        # Must contain at least one strong system indicator
        strong_indicators = [
            'system', 'architecture', 'infrastructure', 'scalability',
            'distributed', 'microservices', 'database', 'pipeline',
            'how we built', 'design decisions', 'at scale', 'deep dive'
        ]
        
        has_indicator = any(indicator in text for indicator in strong_indicators)
        
        # Must not be obviously non-technical
        excludes = ['hiring', 'culture', 'announcement', 'event', 'conference']
        has_exclude = any(exclude in text for exclude in excludes)
        
        return has_indicator and not has_exclude
    
    def download_system_article(self, company, article_info):
        """Download and process a system article."""
        try:
            url = article_info['url']
            title = article_info['title']
            score = article_info['score']
            
            print(f"   📥 Downloading (score: {score}): {title[:60]}...")
            
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content
            content_selectors = [
                'article', '.post-content', '.entry-content',
                '.content', 'main', '.blog-post-content',
                '[role="main"]', '.post-body'
            ]
            
            content_elem = None
            for selector in content_selectors:
                content_elem = soup.select_one(selector)
                if content_elem:
                    break
            
            if not content_elem:
                content_elem = soup
            
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
            
            # Create company directory
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            # Create filename
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:80]}.md"
            filepath = company_dir / filename
            
            # Create frontmatter
            frontmatter = f"""---
title: "{title}"
author: "{company}"
url: "{url}"
system_score: {score}
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            # Add to existing hashes
            self.existing_hashes.add(content_hash)
            self.stats['high_quality_downloaded'] += 1
            
            print(f"   ✅ Saved: {filepath}")
            return True
            
        except Exception as e:
            print(f"   ❌ Error downloading {article_info.get('title', 'unknown')}: {e}")
            return False
    
    def explore_all_companies(self):
        """Explore all companies for system articles."""
        print("🏗️  DEEP SYSTEMS ARCHITECTURE EXPLORATION")
        print("=" * 60)
        print(f"🎯 Target: System architecture articles from {len(self.COMPANIES_WITH_DEEP_SYSTEMS)} companies")
        print(f"📊 Quality threshold: 30+ system architecture score")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing articles")
        print()
        
        for company, config in self.COMPANIES_WITH_DEEP_SYSTEMS.items():
            print(f"\n🏢 {company.upper()}")
            print("-" * 40)
            
            # Discover articles
            articles = self.discover_system_articles(company, config)
            
            if not articles:
                print("   📭 No high-quality system articles found")
                continue
            
            print(f"   🎯 Found {len(articles)} system architecture articles")
            
            # Download articles
            downloaded = 0
            for article in articles:
                if self.download_system_article(company, article):
                    downloaded += 1
                
                # Respectful downloading
                time.sleep(random.uniform(1, 3))
            
            print(f"   ✅ Downloaded {downloaded} articles")
            self.stats['companies_explored'] += 1
            
            # Longer pause between companies
            time.sleep(random.uniform(3, 6))
        
        # Print final statistics
        print("\n" + "=" * 60)
        print("📊 EXPLORATION COMPLETE")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Final article count
        total_files = len(list(self.blogs_dir.rglob('*.md')))
        print(f"Total articles in collection: {total_files}")

def main():
    explorer = DeepSystemsExplorer(max_articles_per_company=15)
    explorer.explore_all_companies()

if __name__ == "__main__":
    main()