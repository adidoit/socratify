#!/usr/bin/env python3
"""
Multi-Blog Engineering Content Downloader

Downloads high-quality engineering articles from top tech company blogs.
Filters out sales/marketing content to focus on technical depth.
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
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import feedparser
    import html2text
    from bs4 import BeautifulSoup
    from tech_companies_blogs import TECH_COMPANY_BLOGS, get_top_engineering_blogs
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with:")
    print("pip install feedparser html2text beautifulsoup4 requests")
    sys.exit(1)


class EngineeringContentFilter:
    """Filter to identify high-quality engineering content vs marketing/sales."""
    
    def __init__(self):
        # Strong technical indicators (high weight)
        self.strong_tech_keywords = [
            'algorithm', 'architecture', 'distributed', 'microservices', 'performance',
            'scalability', 'database', 'infrastructure', 'machine learning', 'deep learning',
            'tensorflow', 'kubernetes', 'docker', 'api design', 'system design',
            'optimization', 'caching', 'load balancing', 'sharding', 'replication',
            'consensus', 'raft', 'paxos', 'eventual consistency', 'cap theorem',
            'data pipeline', 'etl', 'stream processing', 'batch processing',
            'monitoring', 'observability', 'tracing', 'metrics', 'logging',
            'security', 'cryptography', 'authentication', 'authorization',
            'testing', 'ci/cd', 'deployment', 'devops', 'sre', 'reliability'
        ]
        
        # Medium technical indicators  
        self.medium_tech_keywords = [
            'code', 'programming', 'software', 'development', 'engineering',
            'backend', 'frontend', 'mobile', 'web', 'framework', 'library',
            'open source', 'git', 'version control', 'debugging', 'profiling',
            'aws', 'gcp', 'azure', 'cloud', 'serverless', 'lambda'
        ]
        
        # Marketing/sales indicators (negative weight)
        self.marketing_keywords = [
            'announce', 'launch', 'introduce', 'unveil', 'release',
            'partnership', 'acquisition', 'funding', 'investment',
            'hiring', 'recruiting', 'culture', 'diversity', 'inclusion',
            'event', 'conference', 'webinar', 'summit', 'meetup',
            'customer story', 'case study', 'success story', 'testimonial',
            'product update', 'feature announcement', 'roadmap',
            'business', 'growth', 'revenue', 'market', 'sales'
        ]
        
        # Strong marketing indicators (very negative)
        self.strong_marketing_keywords = [
            'press release', 'acquisition', 'ipo', 'funding round',
            'series a', 'series b', 'venture capital', 'valuation',
            'hire', 'job opening', 'career', 'interview process'
        ]
    
    def calculate_technical_score(self, title, content, url=""):
        """Calculate how technical/engineering-focused an article is."""
        
        # Combine all text for analysis
        full_text = f"{title} {content} {url}".lower()
        
        score = 0
        
        # Strong technical indicators (+3 each)
        for keyword in self.strong_tech_keywords:
            if keyword in full_text:
                score += 3
                
        # Medium technical indicators (+1 each)  
        for keyword in self.medium_tech_keywords:
            if keyword in full_text:
                score += 1
                
        # Marketing penalties (-2 each)
        for keyword in self.marketing_keywords:
            if keyword in full_text:
                score -= 2
                
        # Strong marketing penalties (-5 each)
        for keyword in self.strong_marketing_keywords:
            if keyword in full_text:
                score -= 5
        
        # Additional heuristics
        
        # Bonus for code blocks or technical formatting
        if '<code>' in content or '```' in content or 'github.com' in content:
            score += 2
            
        # Bonus for technical URLs
        technical_url_indicators = ['/engineering/', '/tech/', '/developers/', '/architecture/']
        if any(indicator in url.lower() for indicator in technical_url_indicators):
            score += 2
            
        # Penalty for obviously non-technical URLs
        marketing_url_indicators = ['/press/', '/news/', '/careers/', '/hiring/']
        if any(indicator in url.lower() for indicator in marketing_url_indicators):
            score -= 3
        
        return score
    
    def is_high_quality_engineering(self, title, content, url="", threshold=5):
        """Determine if article meets high-quality engineering standards."""
        score = self.calculate_technical_score(title, content, url)
        return score >= threshold


class MultiBlogDownloader:
    """Download engineering content from multiple tech company blogs."""
    
    def __init__(self, output_dir="tech_blogs", delay=2.0, max_workers=3):
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.max_workers = max_workers
        self.content_filter = EngineeringContentFilter()
        
        # HTTP session with good headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
        })
        
        # HTML to markdown converter
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False  
        self.html_converter.body_width = 0
        self.html_converter.single_line_break = True
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics tracking
        self.stats = {
            'total_attempted': 0,
            'high_quality_downloaded': 0,
            'filtered_out': 0,
            'errors': 0
        }
    
    def sanitize_filename(self, title):
        """Convert title to safe filename."""
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        filename = filename[:100].rstrip('._')
        return filename or "untitled"
    
    def download_from_rss(self, blog_key, blog_config, max_articles=20):
        """Download articles from RSS feed."""
        rss_url = blog_config['rss']
        if not rss_url:
            return []
            
        print(f"📰 Processing RSS: {blog_config['name']}")
        
        try:
            # Try custom headers first
            response = self.session.get(rss_url, timeout=30)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
            else:
                # Fallback to feedparser direct
                feed = feedparser.parse(rss_url)
                
            if not feed.entries:
                print(f"   ⚠️  No entries found in RSS feed")
                return []
                
            print(f"   🔍 Found {len(feed.entries)} articles in feed")
            
            downloaded = []
            for entry in feed.entries[:max_articles]:
                article_data = self.process_rss_entry(entry, blog_key, blog_config)
                if article_data:
                    downloaded.append(article_data)
                    
                time.sleep(self.delay / 2)  # Lighter delay for RSS
                
            return downloaded
            
        except Exception as e:
            print(f"   ❌ RSS Error: {e}")
            return []
    
    def process_rss_entry(self, entry, blog_key, blog_config):
        """Process a single RSS entry."""
        title = entry.get('title', 'Untitled')
        url = entry.get('link', '')
        
        if not url:
            return None
            
        # Get full article content
        content_data = self.extract_article_content(url)
        if not content_data:
            return None
            
        # Apply quality filter
        tech_score = self.content_filter.calculate_technical_score(
            title, content_data['content'], url)
        
        if tech_score < 5:  # Configurable threshold
            print(f"   🚫 Filtered out (score: {tech_score}): {title[:60]}...")
            self.stats['filtered_out'] += 1
            return None
            
        # Save high-quality article
        saved = self.save_article(content_data, blog_key)
        if saved:
            print(f"   ✅ Downloaded (score: {tech_score}): {title[:60]}...")
            self.stats['high_quality_downloaded'] += 1
            return content_data
        else:
            self.stats['errors'] += 1
            return None
    
    def extract_article_content(self, url):
        """Extract clean article content from URL."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
                element.decompose()
                
            # Remove social/sharing elements
            unwanted_selectors = [
                '[class*="social"]', '[class*="share"]', '[class*="follow"]',
                '[class*="sidebar"]', '[class*="related"]', '[class*="comment"]',
                '[class*="navigation"]', '[class*="breadcrumb"]'
            ]
            
            for selector in unwanted_selectors:
                for element in soup.select(selector):
                    element.decompose()
            
            # Find main content using multiple strategies
            content_selectors = [
                'article', '[role="main"]', 'main',
                '.post-content', '.entry-content', '.article-content',
                '.content', '.post-body', '.story-body'
            ]
            
            content_element = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element and len(content_element.get_text().strip()) > 500:
                    break
            
            # Fallback to largest text container
            if not content_element:
                text_containers = soup.find_all(['div', 'section'])
                if text_containers:
                    content_element = max(text_containers, 
                                        key=lambda x: len(x.get_text()), 
                                        default=None)
            
            if not content_element:
                return None
            
            # Extract metadata
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Untitled"
            
            # Clean title (remove site branding)
            title_text = re.sub(r'\s*[\|\-—–]\s*[^|]*$', '', title_text)
            
            # Try h1 as backup title
            if not title_text or len(title_text.split()) < 3:
                h1 = soup.find('h1')
                if h1:
                    title_text = h1.get_text().strip()
            
            # Extract author
            author_selectors = [
                '.author', '.byline', '.post-author', '[rel="author"]',
                '.writer', '.contributor', '[class*="author"]'
            ]
            author = "Unknown"
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    author = author_elem.get_text().strip()
                    # Clean author text
                    author = re.sub(r'^(by|written by|author:)\s*', '', author, flags=re.I)
                    break
            
            # Extract publish date
            date_selectors = [
                'time[datetime]', '[datetime]', '.date', '.published',
                '.post-date', '.publish-date', '[class*="date"]'
            ]
            pub_date = "Unknown"
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    pub_date = date_elem.get('datetime', date_elem.get_text().strip())
                    break
            
            # Convert to clean markdown
            html_content = str(content_element)
            markdown_content = self.html_converter.handle(html_content)
            
            # Clean up markdown formatting
            markdown_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown_content)
            markdown_content = re.sub(r'^\s+', '', markdown_content, flags=re.M)
            
            return {
                'title': title_text,
                'author': author,
                'url': url,
                'published_date': pub_date,
                'content': markdown_content.strip()
            }
            
        except Exception as e:
            print(f"   ❌ Content extraction error for {url}: {e}")
            return None
    
    def save_article(self, article_data, blog_key):
        """Save article to blog-specific directory."""
        if not article_data or not article_data['content']:
            return False
        
        # Create blog directory
        blog_dir = self.output_dir / blog_key
        blog_dir.mkdir(exist_ok=True)
        
        # Create safe filename
        safe_title = self.sanitize_filename(article_data['title'])
        filename = f"{safe_title}.md"
        filepath = blog_dir / filename
        
        # Handle duplicates
        counter = 1
        while filepath.exists():
            filename = f"{safe_title}_{counter}.md"
            filepath = blog_dir / filename
            counter += 1
        
        # Create frontmatter
        frontmatter = f"""---
title: "{article_data['title'].replace('"', '\\"')}"
author: "{article_data['author']}"
url: "{article_data['url']}"
published_date: "{article_data['published_date']}"
downloaded_date: "{datetime.now().isoformat()}"
company: "{blog_key}"
---

"""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + article_data['content'])
            return True
        except Exception as e:
            print(f"   ❌ Save error: {e}")
            return False
    
    def download_blog(self, blog_key, blog_config, max_articles=15):
        """Download articles from a single blog."""
        self.stats['total_attempted'] += max_articles
        
        print(f"\n🏢 {blog_config['name']}")
        print(f"   📍 {blog_config['url']}")
        
        if blog_config['rss']:
            return self.download_from_rss(blog_key, blog_config, max_articles)
        else:
            print(f"   ⚠️  No RSS feed - would need custom scraper")
            return []
    
    def download_all_blogs(self, blog_limit=25, articles_per_blog=15, parallel=False):
        """Download from all top engineering blogs."""
        
        print("🚀 MULTI-BLOG ENGINEERING CONTENT DOWNLOADER")
        print("=" * 60)
        print(f"Target: Top {blog_limit} engineering blogs")
        print(f"Articles per blog: {articles_per_blog}")
        print(f"Quality filter: Technical score ≥ 5")
        print()
        
        # Get top blogs
        top_blogs = get_top_engineering_blogs(blog_limit)
        
        if parallel and self.max_workers > 1:
            print(f"🔄 Using parallel processing ({self.max_workers} workers)")
            self.download_parallel(top_blogs, articles_per_blog)
        else:
            print(f"🔄 Using sequential processing")
            self.download_sequential(top_blogs, articles_per_blog)
        
        self.print_final_stats()
    
    def download_sequential(self, blogs, articles_per_blog):
        """Download blogs sequentially."""
        for i, (blog_key, blog_config, score) in enumerate(blogs, 1):
            print(f"\n[{i}/{len(blogs)}] Processing {blog_key}...")
            
            try:
                self.download_blog(blog_key, blog_config, articles_per_blog)
                time.sleep(self.delay)  # Be respectful between different sites
            except Exception as e:
                print(f"   ❌ Blog error: {e}")
                self.stats['errors'] += 1
    
    def download_parallel(self, blogs, articles_per_blog):
        """Download blogs in parallel (use cautiously)."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {}
            
            for blog_key, blog_config, score in blogs:
                future = executor.submit(self.download_blog, blog_key, blog_config, articles_per_blog)
                futures[future] = blog_key
            
            for future in as_completed(futures):
                blog_key = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"   ❌ {blog_key} error: {e}")
                    self.stats['errors'] += 1
    
    def print_final_stats(self):
        """Print download statistics."""
        print(f"\n📊 FINAL STATISTICS")
        print("=" * 40)
        print(f"High-quality articles downloaded: {self.stats['high_quality_downloaded']}")
        print(f"Low-quality articles filtered out: {self.stats['filtered_out']}")
        print(f"Errors encountered: {self.stats['errors']}")
        print(f"Success rate: {self.stats['high_quality_downloaded']/(self.stats['high_quality_downloaded']+self.stats['filtered_out']+self.stats['errors']):.1%}")
        print(f"\n📁 Articles saved in: {self.output_dir}/")
        print(f"   Each company has its own subdirectory")


def main():
    parser = argparse.ArgumentParser(description="Download high-quality engineering content from top tech blogs")
    parser.add_argument('-o', '--output', default='tech_engineering_blogs',
                       help='Output directory (default: tech_engineering_blogs)')
    parser.add_argument('-b', '--blogs', type=int, default=10,
                       help='Number of top blogs to process (default: 10)')
    parser.add_argument('-a', '--articles', type=int, default=15,
                       help='Articles per blog (default: 15)')
    parser.add_argument('-d', '--delay', type=float, default=2.0,
                       help='Delay between requests (default: 2.0)')
    parser.add_argument('-w', '--workers', type=int, default=1,
                       help='Parallel workers (default: 1, be careful with >1)')
    parser.add_argument('--parallel', action='store_true',
                       help='Use parallel processing (use cautiously)')
    
    args = parser.parse_args()
    
    # Create downloader and start
    downloader = MultiBlogDownloader(
        output_dir=args.output,
        delay=args.delay,
        max_workers=args.workers
    )
    
    downloader.download_all_blogs(
        blog_limit=args.blogs,
        articles_per_blog=args.articles,
        parallel=args.parallel
    )


if __name__ == "__main__":
    main()