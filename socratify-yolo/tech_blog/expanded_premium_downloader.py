#!/usr/bin/env python3
"""
Expanded Premium Engineering Blog Downloader

Combines original 47 + expansion 37 = 84 premium engineering blogs
Focus: Novel applications, beyond-textbook insights, practitioner perspectives
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

try:
    import feedparser
    import html2text
    from bs4 import BeautifulSoup
    from clean_blog_downloader import TOP_ENGINEERING_BLOGS, QualityFilter
    from premium_engineering_blogs_expansion import PREMIUM_ENGINEERING_BLOGS_EXPANSION
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with:")
    print("pip install feedparser html2text beautifulsoup4 requests")
    sys.exit(1)

# Combine original and expansion blogs
ALL_PREMIUM_ENGINEERING_BLOGS = {**TOP_ENGINEERING_BLOGS, **PREMIUM_ENGINEERING_BLOGS_EXPANSION}

# Convert expansion format to match original format
for key, blog in PREMIUM_ENGINEERING_BLOGS_EXPANSION.items():
    if key not in ALL_PREMIUM_ENGINEERING_BLOGS:
        ALL_PREMIUM_ENGINEERING_BLOGS[key] = {
            "name": blog["name"],
            "url": blog["url"], 
            "rss": blog.get("rss")
        }


class EnhancedQualityFilter:
    """Enhanced quality filter for premium engineering content."""
    
    def __init__(self):
        # Ultra-premium technical indicators (novel applications focus)
        self.novel_tech_keywords = [
            'novel approach', 'innovative solution', 'unique challenge', 'first-of-its-kind',
            'breakthrough', 'pioneering', 'cutting-edge', 'state-of-the-art', 'novel algorithm',
            'innovative architecture', 'unique implementation', 'creative solution'
        ]
        
        # Practitioner-focused keywords (beyond textbook)
        self.practitioner_keywords = [
            'lessons learned', 'in production', 'at scale', 'real-world', 'production experience',
            'battle-tested', 'production-ready', 'operational insights', 'engineering challenges',
            'practical experience', 'war stories', 'post-mortem', 'incident report',
            'case study', 'deep dive', 'behind the scenes', 'engineering journey'
        ]
        
        # High-quality technical indicators  
        self.premium_tech_keywords = [
            'distributed systems', 'system design', 'architecture', 'scalability', 'performance',
            'microservices', 'event-driven', 'real-time', 'machine learning', 'data engineering',
            'infrastructure', 'observability', 'reliability', 'security', 'optimization',
            'consensus', 'consistency', 'availability', 'partition tolerance', 'cap theorem',
            'eventual consistency', 'strong consistency', 'distributed consensus', 'raft',
            'paxos', 'blockchain', 'cryptography', 'zero-knowledge', 'vector database'
        ]
        
        # Novel application domains
        self.novel_domains = [
            'metaverse', 'collaborative editing', 'creative tools', 'low-code platform',
            'vector search', 'semantic search', 'knowledge graph', 'time-series database',
            'edge computing', 'serverless', 'jamstack', 'identity management',
            'zero-trust', 'food delivery', 'ride sharing', 'fintech', 'blockchain infrastructure'
        ]
        
        # Sales/marketing content (stronger penalties)
        self.sales_keywords = [
            'announcing', 'introducing', 'launch', 'unveiling', 'proud to announce',
            'excited to share', 'thrilled to introduce', 'partnership', 'acquisition',
            'funding', 'investment', 'series a', 'series b', 'ipo', 'valuation',
            'customer success', 'testimonial', 'case study success', 'roi', 'cost savings',
            'webinar', 'demo', 'free trial', 'get started', 'contact sales'
        ]
    
    def calculate_premium_score(self, title, content, url=""):
        """Calculate premium engineering content score."""
        text = f"{title} {content} {url}".lower()
        score = 0
        
        # Novel/innovative content (highest weight)
        for keyword in self.novel_tech_keywords:
            if keyword in text:
                score += 5
                
        # Practitioner insights (high weight)
        for keyword in self.practitioner_keywords:
            if keyword in text:
                score += 4
                
        # Premium technical content (medium-high weight)
        for keyword in self.premium_tech_keywords:
            if keyword in text:
                score += 3
                
        # Novel application domains (medium weight)
        for keyword in self.novel_domains:
            if keyword in text:
                score += 2
        
        # Technical depth indicators
        if 'algorithm' in text and ('implementation' in text or 'optimization' in text):
            score += 3
        if 'architecture' in text and ('design' in text or 'pattern' in text):
            score += 3
        if 'performance' in text and ('optimization' in text or 'scaling' in text):
            score += 3
        if 'production' in text and ('lessons' in text or 'experience' in text):
            score += 4
            
        # Code/technical content indicators
        if '```' in content or 'github.com' in content:
            score += 2
        if re.search(r'benchmark|profiling|measurement|metrics', text):
            score += 2
            
        # Sales content penalties (strong negative)
        for keyword in self.sales_keywords:
            if keyword in text:
                score -= 5
                
        # Additional quality indicators
        if len(content) > 5000:  # Substantial content
            score += 1
        if re.search(r'\b\d+%|\d+x faster|\d+ms\b', text):  # Quantitative results
            score += 2
            
        return score
    
    def is_premium_engineering_content(self, title, content, url="", threshold=8):
        """Determine if content meets premium engineering standards."""
        score = self.calculate_premium_score(title, content, url)
        return score >= threshold


class ExpandedPremiumDownloader:
    """Downloader for expanded premium engineering blogs."""
    
    def __init__(self, output_dir="blogs", delay=2.0):
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.filter = EnhancedQualityFilter()
        
        # Ensure clean structure
        self.output_dir.mkdir(exist_ok=True)
        
        # HTTP session with better headers for international sites
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive'
        })
        
        # Enhanced markdown converter
        self.converter = html2text.HTML2Text()
        self.converter.ignore_links = False
        self.converter.ignore_images = False
        self.converter.body_width = 0
        self.converter.single_line_break = True
        
        # Enhanced statistics
        self.stats = {
            'total_blogs': 0,
            'international_blogs': 0,
            'novel_application_blogs': 0,
            'open_source_blogs': 0,
            'vendor_blogs': 0,
            'premium_downloaded': 0,
            'filtered_out': 0,
            'errors': 0,
            'score_distribution': {'ultra_premium': 0, 'premium': 0, 'good': 0}
        }
    
    def sanitize_filename(self, title):
        """Create clean filename."""
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        return filename[:70] or "untitled"
    
    def extract_enhanced_content(self, url):
        """Enhanced content extraction for international and specialized blogs."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements more aggressively
            unwanted_tags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']
            for tag in unwanted_tags:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Remove marketing/social elements
            unwanted_selectors = [
                '[class*="social"]', '[class*="share"]', '[class*="subscribe"]',
                '[class*="newsletter"]', '[class*="cta"]', '[class*="promo"]',
                '[class*="related"]', '[class*="sidebar"]', '[class*="comment"]'
            ]
            
            for selector in unwanted_selectors:
                for element in soup.select(selector):
                    element.decompose()
            
            # Enhanced content detection strategies
            content_strategies = [
                # Strategy 1: Semantic HTML5 elements
                lambda: soup.select_one('article') or soup.select_one('[role="main"]') or soup.select_one('main'),
                
                # Strategy 2: Common CMS content classes
                lambda: soup.select_one('.post-content') or soup.select_one('.entry-content') or soup.select_one('.article-content'),
                
                # Strategy 3: Blog platform specific
                lambda: soup.select_one('.blog-post') or soup.select_one('.story-body') or soup.select_one('.markdown-body'),
                
                # Strategy 4: Content by ID
                lambda: soup.select_one('#content') or soup.select_one('#post-content') or soup.select_one('#main-content'),
                
                # Strategy 5: Specialized blog platforms
                lambda: soup.select_one('.notion-page-content') or soup.select_one('.medium-content') or soup.select_one('.ghost-content')
            ]
            
            content_element = None
            for strategy in content_strategies:
                try:
                    content_element = strategy()
                    if content_element and len(content_element.get_text().strip()) > 1000:
                        break
                except:
                    continue
            
            # Fallback to largest text container
            if not content_element:
                text_containers = soup.find_all(['div', 'section', 'article'])
                if text_containers:
                    content_element = max(text_containers, key=lambda x: len(x.get_text()), default=None)
            
            if not content_element:
                return None
            
            # Enhanced title extraction
            title_strategies = [
                lambda: soup.select_one('h1'),
                lambda: soup.select_one('.post-title') or soup.select_one('.entry-title') or soup.select_one('.article-title'),
                lambda: soup.select_one('[property="og:title"]'),
                lambda: soup.select_one('title')
            ]
            
            title_text = "Untitled"
            for strategy in title_strategies:
                try:
                    title_elem = strategy()
                    if title_elem:
                        if title_elem.name == 'title':
                            title_text = title_elem.get_text().strip()
                        elif title_elem.get('content'):
                            title_text = title_elem.get('content').strip()
                        else:
                            title_text = title_elem.get_text().strip()
                        
                        # Clean title of site branding
                        title_text = re.sub(r'\s*[\|\-—–]\s*[^|]*$', '', title_text)
                        title_text = re.sub(r'\s*\|\s*(Blog|Engineering|Tech).*$', '', title_text, flags=re.I)
                        
                        if len(title_text.split()) >= 3:
                            break
                except:
                    continue
            
            # Enhanced author extraction
            author_patterns = [
                '.author', '.byline', '.post-author', '[rel="author"]', '.writer',
                '[data-author]', '.author-name', '[property="article:author"]',
                '.post-meta .author', '.byline-author', '.entry-author'
            ]
            
            author = "Unknown"
            for pattern in author_patterns:
                try:
                    author_elem = soup.select_one(pattern)
                    if author_elem:
                        author_text = author_elem.get_text().strip() if author_elem.get_text() else author_elem.get('content', '')
                        author_text = re.sub(r'^(by|written by|author:)\s*', '', author_text, flags=re.I)
                        author_text = re.sub(r'\s*\|.*$', '', author_text)  # Remove extra info after |
                        if author_text and len(author_text) < 100 and not any(x in author_text.lower() for x in ['published', 'updated', 'read']):
                            author = author_text
                            break
                except:
                    continue
            
            # Convert to enhanced markdown
            html_content = str(content_element)
            markdown_content = self.converter.handle(html_content)
            
            # Clean up markdown formatting
            markdown_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown_content)
            markdown_content = re.sub(r'^\s+', '', markdown_content, flags=re.M)
            markdown_content = markdown_content.strip()
            
            return {
                'title': title_text,
                'author': author, 
                'url': url,
                'content': markdown_content
            }
            
        except Exception as e:
            print(f"   ❌ Content extraction error for {url}: {str(e)[:100]}...")
            return None
    
    def process_premium_entry(self, entry_data, company, is_rss=True):
        """Process entry with premium quality filtering."""
        if is_rss and isinstance(entry_data, dict):
            title = entry_data.get('title', 'Untitled')
            url = entry_data.get('link', '')
        else:
            url = entry_data
            title = "Article"
        
        if not url:
            return None
            
        # Extract full content
        article = self.extract_enhanced_content(url)
        if not article:
            return None
            
        # Apply premium quality filter
        score = self.filter.calculate_premium_score(article['title'], article['content'], url)
        
        # Premium threshold (higher than basic)
        threshold = 10
        
        if score < threshold:
            print(f"   🚫 Filtered (score: {score}): {article['title'][:45]}...")
            self.stats['filtered_out'] += 1
            return None
        
        # Categorize by score for statistics
        if score >= 20:
            self.stats['score_distribution']['ultra_premium'] += 1
            score_label = "⭐⭐⭐"
        elif score >= 15:
            self.stats['score_distribution']['premium'] += 1 
            score_label = "⭐⭐"
        else:
            self.stats['score_distribution']['good'] += 1
            score_label = "⭐"
        
        # Save premium article
        if self.save_premium_article(article, company):
            print(f"   ✅ {score_label} Downloaded (score: {score}): {article['title'][:45]}...")
            self.stats['premium_downloaded'] += 1
            return article
        else:
            self.stats['errors'] += 1
            return None
    
    def save_premium_article(self, article, company):
        """Save article with clean structure."""
        if not article or not article['content']:
            return False
        
        # Create company directory
        company_dir = self.output_dir / company
        company_dir.mkdir(exist_ok=True)
        
        # Clean filename
        safe_title = self.sanitize_filename(article['title'])
        filepath = company_dir / f"{safe_title}.md"
        
        # Handle duplicates
        counter = 1
        while filepath.exists():
            filepath = company_dir / f"{safe_title}_{counter}.md"
            counter += 1
        
        # Create clean markdown with metadata
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
            print(f"   ❌ Save error: {str(e)[:50]}...")
            return False
    
    def download_premium_blog(self, company, config, max_articles=8):
        """Download from a premium engineering blog."""
        print(f"\n📝 {config['name']}")
        self.stats['total_blogs'] += 1
        
        # Track blog categories for stats
        if company in ['atlassian', 'booking', 'deliveroo', 'klarna', 'canva']:
            self.stats['international_blogs'] += 1
        elif company in ['retool', 'notion', 'linear', 'roblox', 'unity']:
            self.stats['novel_application_blogs'] += 1 
        elif company in ['kubernetes', 'istio', 'prometheus', 'vitess', 'cncf']:
            self.stats['open_source_blogs'] += 1
        elif company in ['confluent', 'cockroachdb_tech', 'datadog', 'pinecone']:
            self.stats['vendor_blogs'] += 1
        
        if not config['rss']:
            print(f"   ⚠️  No RSS feed available")
            return
        
        try:
            # Enhanced RSS processing with better error handling
            response = self.session.get(config['rss'], timeout=30)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
            else:
                feed = feedparser.parse(config['rss'])
            
            if not feed.entries:
                print(f"   ⚠️  No articles found")
                return
            
            print(f"   🔍 Found {len(feed.entries)} articles")
            
            # Process articles with premium filtering
            downloaded = 0
            for entry in feed.entries[:max_articles * 2]:  # Try more to account for filtering
                if downloaded >= max_articles:
                    break
                    
                if self.process_premium_entry(entry, company, is_rss=True):
                    downloaded += 1
                
                time.sleep(self.delay / 3)  # Lighter delay for RSS
                
        except Exception as e:
            print(f"   ❌ RSS error: {str(e)[:60]}...")
            self.stats['errors'] += 1
    
    def download_all_premium(self, limit=50, articles_per_blog=8):
        """Download from all premium engineering blogs."""
        print("🚀 EXPANDED PREMIUM ENGINEERING BLOG DOWNLOADER")
        print("=" * 65)
        print(f"📊 Target: Top {limit} premium engineering blogs")
        print(f"📄 Articles per blog: {articles_per_blog}")
        print(f"🎯 Quality threshold: 10+ points (premium level)")
        print(f"📁 Output: {self.output_dir}/")
        
        # Get blogs with RSS feeds
        blogs_with_rss = [(k, v) for k, v in ALL_PREMIUM_ENGINEERING_BLOGS.items() if v.get('rss')]
        selected_blogs = blogs_with_rss[:limit]
        
        print(f"\n🌟 Processing {len(selected_blogs)} premium blogs:")
        
        # Download from each blog
        for i, (company, config) in enumerate(selected_blogs, 1):
            print(f"\n[{i}/{len(selected_blogs)}]", end=" ")
            self.download_premium_blog(company, config, articles_per_blog)
            time.sleep(self.delay)
        
        self.print_premium_stats()
    
    def print_premium_stats(self):
        """Print premium download statistics."""
        print(f"\n🎯 PREMIUM DOWNLOAD COMPLETE")
        print("=" * 50)
        
        print(f"📊 Blog Categories:")
        print(f"   🌍 International: {self.stats['international_blogs']}")
        print(f"   💡 Novel Applications: {self.stats['novel_application_blogs']}")
        print(f"   🔧 Open Source: {self.stats['open_source_blogs']}")
        print(f"   🏢 Vendor Engineering: {self.stats['vendor_blogs']}")
        print(f"   📈 Total blogs: {self.stats['total_blogs']}")
        
        print(f"\n📄 Content Quality Results:")
        print(f"   ✅ Premium articles: {self.stats['premium_downloaded']}")
        print(f"   🚫 Filtered out: {self.stats['filtered_out']}")
        print(f"   ❌ Errors: {self.stats['errors']}")
        
        total_processed = self.stats['premium_downloaded'] + self.stats['filtered_out']
        if total_processed > 0:
            premium_rate = (self.stats['premium_downloaded'] / total_processed) * 100
            print(f"   📈 Premium content rate: {premium_rate:.1f}%")
        
        print(f"\n⭐ Quality Distribution:")
        print(f"   ⭐⭐⭐ Ultra-premium (20+ pts): {self.stats['score_distribution']['ultra_premium']}")
        print(f"   ⭐⭐ Premium (15-19 pts): {self.stats['score_distribution']['premium']}")
        print(f"   ⭐ Good (10-14 pts): {self.stats['score_distribution']['good']}")
        
        print(f"\n📁 Articles saved in: {self.output_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Download expanded premium engineering blog collection")
    parser.add_argument('-n', '--num-blogs', type=int, default=40,
                       help='Number of blogs to process (default: 40)')
    parser.add_argument('-a', '--articles', type=int, default=8,
                       help='Articles per blog (default: 8)')
    parser.add_argument('-d', '--delay', type=float, default=2.0,
                       help='Delay between requests (default: 2.0)')
    
    args = parser.parse_args()
    
    downloader = ExpandedPremiumDownloader(delay=args.delay)
    downloader.download_all_premium(limit=args.num_blogs, articles_per_blog=args.articles)


if __name__ == "__main__":
    main()