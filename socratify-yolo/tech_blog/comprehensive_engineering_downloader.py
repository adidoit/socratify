#!/usr/bin/env python3
"""
Comprehensive Engineering Blog Downloader

Downloads from both mainstream (25) and specialized (25) high-quality engineering blogs.
Total: 50 premium engineering content sources with intelligent quality filtering.
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
    from specialized_engineering_blogs import SPECIALIZED_ENGINEERING_BLOGS, get_specialized_engineering_blogs
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with:")
    print("pip install feedparser html2text beautifulsoup4 requests")
    sys.exit(1)


class AdvancedEngineeringFilter:
    """Enhanced filter for identifying premium engineering content."""
    
    def __init__(self):
        # Ultra-strong technical indicators (highest weight)
        self.ultra_tech_keywords = [
            'distributed consensus', 'raft algorithm', 'byzantine fault tolerance',
            'consistency models', 'cap theorem', 'acid properties', 'eventual consistency',
            'vector clocks', 'merkle trees', 'bloom filters', 'consistent hashing',
            'gossip protocol', 'crdt', 'conflict-free replicated data types',
            'state machine replication', 'leader election', 'split-brain'
        ]
        
        # Strong technical indicators (high weight)
        self.strong_tech_keywords = [
            'algorithm', 'architecture', 'distributed', 'microservices', 'performance',
            'scalability', 'database', 'infrastructure', 'machine learning', 'deep learning',
            'consensus', 'replication', 'sharding', 'partitioning', 'load balancing',
            'caching', 'indexing', 'query optimization', 'storage engine', 'b-tree',
            'lsm-tree', 'write-ahead log', 'mvcc', 'serialization', 'protocol buffers',
            'grpc', 'kubernetes', 'docker', 'containers', 'orchestration',
            'service mesh', 'circuit breaker', 'bulkhead pattern', 'saga pattern',
            'event sourcing', 'cqrs', 'stream processing', 'batch processing',
            'real-time', 'low latency', 'high throughput', 'zero downtime',
            'fault tolerance', 'reliability', 'monitoring', 'observability',
            'tracing', 'metrics', 'logging', 'alerting', 'sre', 'devops'
        ]
        
        # Systems programming and language-specific
        self.systems_keywords = [
            'rust', 'go', 'c++', 'zig', 'systems programming', 'memory management',
            'garbage collection', 'jvm', 'v8', 'llvm', 'compilation', 'optimization',
            'profiling', 'benchmarking', 'concurrency', 'parallelism', 'async',
            'coroutines', 'green threads', 'event loop', 'reactor pattern'
        ]
        
        # Specialized domains (bonus for deep expertise)
        self.domain_keywords = [
            'computer vision', 'nlp', 'natural language processing', 'information retrieval',
            'search algorithms', 'recommendation systems', 'reinforcement learning',
            'neural networks', 'transformers', 'attention mechanism',
            'cryptography', 'zero-knowledge proofs', 'blockchain', 'smart contracts',
            'networking', 'tcp/ip', 'http/2', 'quic', 'websockets', 'webrtc',
            'cdn', 'edge computing', 'dns', 'load balancers', 'reverse proxy'
        ]
        
        # Academic/research quality indicators
        self.research_keywords = [
            'paper', 'research', 'whitepaper', 'algorithm analysis', 'complexity analysis',
            'big o', 'time complexity', 'space complexity', 'benchmarks', 'evaluation',
            'empirical study', 'performance analysis', 'trade-offs', 'comparison'
        ]
        
        # Anti-patterns (stronger negative weight)
        self.anti_patterns = [
            'we are excited to announce', 'proud to announce', 'thrilled to share',
            'join our team', 'we are hiring', 'careers at', 'job opening',
            'funding round', 'series a', 'series b', 'acquisition', 'merger',
            'partnership with', 'collaboration with', 'customer success',
            'case study', 'user story', 'testimonial', 'event recap',
            'conference talk', 'webinar', 'demo', 'product launch',
            'new feature', 'introducing', 'unveiling', 'roadmap update'
        ]
    
    def calculate_advanced_technical_score(self, title, content, url="", blog_metadata=None):
        """Calculate advanced technical score with domain expertise weighting."""
        
        full_text = f"{title} {content} {url}".lower()
        score = 0
        
        # Ultra-strong technical patterns (+5 each)
        for keyword in self.ultra_tech_keywords:
            if keyword in full_text:
                score += 5
                
        # Strong technical indicators (+3 each)
        for keyword in self.strong_tech_keywords:
            if keyword in full_text:
                score += 3
                
        # Systems programming (+2 each)
        for keyword in self.systems_keywords:
            if keyword in full_text:
                score += 2
                
        # Domain expertise (+2 each)
        for keyword in self.domain_keywords:
            if keyword in full_text:
                score += 2
                
        # Research quality (+2 each)
        for keyword in self.research_keywords:
            if keyword in full_text:
                score += 2
        
        # Blog-specific bonuses
        if blog_metadata:
            # Bonus for specialized blog quality indicators
            blog_indicators = blog_metadata.get('quality_indicators', [])
            for indicator in blog_indicators:
                if indicator.replace('-', ' ') in full_text:
                    score += 2
        
        # Technical content patterns
        if re.search(r'```.*```', content, re.DOTALL):  # Code blocks
            score += 3
        if 'github.com' in content or 'gitlab.com' in content:  # Code references
            score += 2
        if re.search(r'\b\d+ms\b|\b\d+%\b|\d+x faster', full_text):  # Performance metrics
            score += 2
        if re.search(r'benchmark|profiling|optimization', full_text):
            score += 2
        
        # Anti-pattern penalties (stronger)
        for anti_pattern in self.anti_patterns:
            if anti_pattern in full_text:
                score -= 4
        
        # URL quality indicators
        technical_paths = ['/engineering/', '/tech/', '/blog/engineering/', '/architecture/']
        if any(path in url.lower() for path in technical_paths):
            score += 2
            
        # Marketing URL penalties
        marketing_paths = ['/press/', '/news/', '/careers/', '/events/', '/resources/']
        if any(path in url.lower() for path in marketing_paths):
            score -= 5
        
        return score
    
    def is_premium_engineering_content(self, title, content, url="", blog_metadata=None, threshold=8):
        """Higher threshold for premium engineering content."""
        score = self.calculate_advanced_technical_score(title, content, url, blog_metadata)
        return score >= threshold


class ComprehensiveEngineeringDownloader:
    """Download from both mainstream and specialized engineering blogs."""
    
    def __init__(self, output_dir="comprehensive_engineering_blogs", delay=2.0, max_workers=2):
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.max_workers = max_workers
        self.content_filter = AdvancedEngineeringFilter()
        
        # HTTP session with realistic headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # Enhanced markdown converter
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0
        self.html_converter.single_line_break = True
        self.html_converter.mark_code = True
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Enhanced statistics
        self.stats = {
            'mainstream_blogs': 0,
            'specialized_blogs': 0,
            'total_attempted': 0,
            'premium_downloaded': 0,
            'filtered_out': 0,
            'errors': 0,
            'score_distribution': {'ultra_high': 0, 'high': 0, 'medium': 0}
        }
    
    def sanitize_filename(self, title):
        """Enhanced filename sanitization."""
        # Remove common prefixes
        title = re.sub(r'^(how|why|what|when|building|creating|implementing|deep dive into)\s+', '', title, flags=re.I)
        
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        filename = re.sub(r'_+', '_', filename)  # Remove multiple underscores
        filename = filename[:80].rstrip('._')  # Shorter for better readability
        return filename or "untitled"
    
    def extract_enhanced_content(self, url, blog_metadata=None):
        """Enhanced content extraction with better parsing."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove noise more aggressively
            unwanted_tags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'form']
            for tag in unwanted_tags:
                for element in soup.find_all(tag):
                    element.decompose()
            
            # Remove social/marketing elements
            unwanted_patterns = [
                '[class*="social"]', '[class*="share"]', '[class*="follow"]',
                '[class*="subscribe"]', '[class*="newsletter"]', '[class*="cta"]',
                '[class*="sidebar"]', '[class*="related"]', '[class*="comment"]',
                '[class*="author-bio"]', '[class*="navigation"]', '[id*="disqus"]'
            ]
            
            for pattern in unwanted_patterns:
                for element in soup.select(pattern):
                    element.decompose()
            
            # Smart content detection
            content_strategies = [
                # Strategy 1: Look for article/main content
                lambda: soup.select_one('article') or soup.select_one('[role="main"]') or soup.select_one('main'),
                
                # Strategy 2: Look for content classes
                lambda: soup.select_one('.post-content') or soup.select_one('.entry-content') or soup.select_one('.article-content'),
                
                # Strategy 3: Look for content by ID  
                lambda: soup.select_one('#content') or soup.select_one('#post-content') or soup.select_one('#article'),
                
                # Strategy 4: Specialized blog patterns
                lambda: soup.select_one('.blog-post') or soup.select_one('.story-body') or soup.select_one('.markdown-body'),
            ]
            
            content_element = None
            for strategy in content_strategies:
                try:
                    content_element = strategy()
                    if content_element and len(content_element.get_text().strip()) > 800:
                        break
                except:
                    continue
            
            # Fallback: largest content container
            if not content_element:
                candidates = soup.find_all(['div', 'section'])
                if candidates:
                    content_element = max(candidates, key=lambda x: len(x.get_text()), default=None)
            
            if not content_element:
                return None
            
            # Extract title with multiple strategies
            title_strategies = [
                lambda: soup.select_one('h1'),
                lambda: soup.select_one('.post-title') or soup.select_one('.entry-title'),
                lambda: soup.select_one('title'),
                lambda: soup.select_one('[property="og:title"]'),
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
                        
                        # Clean title
                        title_text = re.sub(r'\s*[\|\-—–]\s*[^|]*$', '', title_text)
                        if len(title_text.split()) >= 3:
                            break
                except:
                    continue
            
            # Extract author with enhanced detection
            author_patterns = [
                '.author', '.byline', '.post-author', '[rel="author"]',
                '.writer', '.contributor', '[data-author]', '.author-name',
                '[property="article:author"]', '.post-meta .author'
            ]
            
            author = "Unknown"
            for pattern in author_patterns:
                try:
                    author_elem = soup.select_one(pattern)
                    if author_elem:
                        author_text = author_elem.get_text().strip() if author_elem.get_text() else author_elem.get('content', '')
                        author_text = re.sub(r'^(by|written by|author:)\s*', '', author_text, flags=re.I)
                        if author_text and len(author_text) < 100:  # Reasonable author name length
                            author = author_text
                            break
                except:
                    continue
            
            # Extract date with enhanced patterns
            date_patterns = [
                'time[datetime]', '[datetime]', '.date', '.published',
                '.post-date', '.publish-date', '[data-date]',
                '[property="article:published_time"]', '.timestamp'
            ]
            
            pub_date = "Unknown"
            for pattern in date_patterns:
                try:
                    date_elem = soup.select_one(pattern)
                    if date_elem:
                        pub_date = date_elem.get('datetime') or date_elem.get('content') or date_elem.get_text().strip()
                        if pub_date and pub_date != "Unknown":
                            break
                except:
                    continue
            
            # Convert to enhanced markdown
            html_content = str(content_element)
            markdown_content = self.html_converter.handle(html_content)
            
            # Clean up markdown
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
    
    def process_blog_entry(self, entry_data, blog_key, blog_metadata, is_specialized=False):
        """Process a single blog entry with enhanced filtering."""
        if isinstance(entry_data, dict) and 'link' in entry_data:
            # RSS entry
            title = entry_data.get('title', 'Untitled')
            url = entry_data.get('link', '')
        else:
            # Direct URL
            url = entry_data
            title = "Article"
        
        if not url:
            return None
            
        # Extract full content
        content_data = self.extract_enhanced_content(url, blog_metadata)
        if not content_data:
            return None
            
        # Apply advanced quality filter
        tech_score = self.content_filter.calculate_advanced_technical_score(
            content_data['title'], content_data['content'], url, blog_metadata)
        
        # Different thresholds for different blog types
        threshold = 10 if is_specialized else 8
        
        if tech_score < threshold:
            print(f"   🚫 Filtered (score: {tech_score}): {content_data['title'][:50]}...")
            self.stats['filtered_out'] += 1
            return None
        
        # Categorize by score
        if tech_score >= 20:
            self.stats['score_distribution']['ultra_high'] += 1
            score_label = "⭐⭐⭐"
        elif tech_score >= 15:
            self.stats['score_distribution']['high'] += 1
            score_label = "⭐⭐"
        else:
            self.stats['score_distribution']['medium'] += 1
            score_label = "⭐"
        
        # Save premium article
        saved = self.save_enhanced_article(content_data, blog_key, is_specialized, tech_score)
        if saved:
            print(f"   ✅ {score_label} Downloaded (score: {tech_score}): {content_data['title'][:50]}...")
            self.stats['premium_downloaded'] += 1
            return content_data
        else:
            self.stats['errors'] += 1
            return None
    
    def save_enhanced_article(self, article_data, blog_key, is_specialized, tech_score):
        """Save article with enhanced metadata."""
        if not article_data or not article_data['content']:
            return False
        
        # Create blog directory with type prefix
        blog_prefix = "specialized_" if is_specialized else "mainstream_"
        blog_dir = self.output_dir / f"{blog_prefix}{blog_key}"
        blog_dir.mkdir(exist_ok=True)
        
        # Enhanced filename with score prefix for sorting
        score_prefix = f"score_{tech_score:02d}_"
        safe_title = self.sanitize_filename(article_data['title'])
        filename = f"{score_prefix}{safe_title}.md"
        filepath = blog_dir / filename
        
        # Handle duplicates
        counter = 1
        while filepath.exists():
            filename = f"{score_prefix}{safe_title}_{counter}.md"
            filepath = blog_dir / filename
            counter += 1
        
        # Enhanced frontmatter
        frontmatter = f"""---
title: "{article_data['title'].replace('"', '\\"')}"
author: "{article_data['author']}"
url: "{article_data['url']}"
published_date: "{article_data['published_date']}"
downloaded_date: "{datetime.now().isoformat()}"
company: "{blog_key}"
blog_type: "{'specialized' if is_specialized else 'mainstream'}"
technical_score: {tech_score}
quality_rating: "{'⭐⭐⭐' if tech_score >= 20 else '⭐⭐' if tech_score >= 15 else '⭐'}"
---

"""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + article_data['content'])
            return True
        except Exception as e:
            print(f"   ❌ Save error: {e}")
            return False
    
    def download_comprehensive_collection(self, mainstream_limit=25, specialized_limit=25, 
                                        articles_per_blog=15, quality_threshold=8):
        """Download comprehensive collection from both mainstream and specialized blogs."""
        
        print("🚀 COMPREHENSIVE ENGINEERING BLOG DOWNLOADER")
        print("=" * 65)
        print(f"📊 Target: {mainstream_limit} mainstream + {specialized_limit} specialized blogs")
        print(f"📄 Articles per blog: {articles_per_blog}")
        print(f"🎯 Quality threshold: {quality_threshold}+ points")
        print(f"📈 Total potential articles: {(mainstream_limit + specialized_limit) * articles_per_blog}")
        print()
        
        # Get blog lists
        mainstream_blogs = get_top_engineering_blogs(mainstream_limit)
        specialized_blogs = get_specialized_engineering_blogs(specialized_limit)
        
        self.stats['mainstream_blogs'] = len(mainstream_blogs)
        self.stats['specialized_blogs'] = len(specialized_blogs)
        
        print(f"🏢 Mainstream Engineering Blogs: {len(mainstream_blogs)}")
        for i, (key, blog, score) in enumerate(mainstream_blogs[:5], 1):
            print(f"   {i}. {blog['name']}")
        if len(mainstream_blogs) > 5:
            print(f"   ... and {len(mainstream_blogs) - 5} more")
        
        print(f"\n🔬 Specialized Engineering Blogs: {len(specialized_blogs)}")
        for i, (key, blog, score) in enumerate(specialized_blogs[:5], 1):
            print(f"   {i}. {blog['name']}")
        if len(specialized_blogs) > 5:
            print(f"   ... and {len(specialized_blogs) - 5} more")
        
        print(f"\n🔄 Starting download process...")
        
        # Download mainstream blogs
        print(f"\n{'='*20} MAINSTREAM BLOGS {'='*20}")
        for i, (blog_key, blog_config, score) in enumerate(mainstream_blogs, 1):
            print(f"\n[{i}/{len(mainstream_blogs)}] {blog_config['name']}")
            try:
                self.download_from_blog(blog_key, blog_config, articles_per_blog, is_specialized=False)
                time.sleep(self.delay)
            except Exception as e:
                print(f"   ❌ Blog error: {e}")
                self.stats['errors'] += 1
        
        # Download specialized blogs
        print(f"\n{'='*20} SPECIALIZED BLOGS {'='*20}")
        for i, (blog_key, blog_config, score) in enumerate(specialized_blogs, 1):
            print(f"\n[{i}/{len(specialized_blogs)}] {blog_config['name']}")
            try:
                self.download_from_blog(blog_key, blog_config, articles_per_blog, is_specialized=True)
                time.sleep(self.delay)
            except Exception as e:
                print(f"   ❌ Blog error: {e}")
                self.stats['errors'] += 1
        
        self.print_comprehensive_stats()
    
    def download_from_blog(self, blog_key, blog_config, max_articles, is_specialized=False):
        """Download from a single blog with RSS support."""
        rss_url = blog_config.get('rss')
        
        if rss_url:
            try:
                response = self.session.get(rss_url, timeout=30)
                if response.status_code == 200:
                    feed = feedparser.parse(response.content)
                else:
                    feed = feedparser.parse(rss_url)
                
                if feed.entries:
                    print(f"   📰 Found {len(feed.entries)} articles in RSS feed")
                    entries_to_process = feed.entries[:max_articles]
                    
                    for entry in entries_to_process:
                        self.process_blog_entry(entry, blog_key, blog_config, is_specialized)
                        time.sleep(self.delay / 2)
                    return
                    
            except Exception as e:
                print(f"   ⚠️ RSS failed: {e}")
        
        print(f"   🕷️ RSS not available - would need custom scraper for {blog_config['url']}")
    
    def print_comprehensive_stats(self):
        """Print comprehensive statistics."""
        total_blogs = self.stats['mainstream_blogs'] + self.stats['specialized_blogs']
        
        print(f"\n🎯 COMPREHENSIVE DOWNLOAD COMPLETE")
        print("=" * 50)
        print(f"📊 Blog Coverage:")
        print(f"   🏢 Mainstream engineering blogs: {self.stats['mainstream_blogs']}")
        print(f"   🔬 Specialized engineering blogs: {self.stats['specialized_blogs']}")
        print(f"   📈 Total blogs processed: {total_blogs}")
        
        print(f"\n📄 Content Quality Results:")
        print(f"   ✅ Premium articles downloaded: {self.stats['premium_downloaded']}")
        print(f"   🚫 Low-quality filtered out: {self.stats['filtered_out']}")
        print(f"   ❌ Errors encountered: {self.stats['errors']}")
        
        total_processed = self.stats['premium_downloaded'] + self.stats['filtered_out']
        if total_processed > 0:
            success_rate = (self.stats['premium_downloaded'] / total_processed) * 100
            print(f"   📈 Premium content rate: {success_rate:.1f}%")
        
        print(f"\n⭐ Quality Distribution:")
        print(f"   ⭐⭐⭐ Ultra-high (20+ points): {self.stats['score_distribution']['ultra_high']}")
        print(f"   ⭐⭐ High (15-19 points): {self.stats['score_distribution']['high']}")
        print(f"   ⭐ Medium (8-14 points): {self.stats['score_distribution']['medium']}")
        
        print(f"\n📁 Articles organized in: {self.output_dir}/")
        print(f"   📂 mainstream_* folders: Mainstream tech company blogs")
        print(f"   📂 specialized_* folders: Specialized engineering blogs")
        print(f"   📝 Files prefixed with score for easy quality sorting")


def main():
    parser = argparse.ArgumentParser(description="Download from comprehensive collection of 50 engineering blogs")
    parser.add_argument('-o', '--output', default='comprehensive_engineering_blogs',
                       help='Output directory (default: comprehensive_engineering_blogs)')
    parser.add_argument('-m', '--mainstream', type=int, default=15,
                       help='Number of mainstream blogs (default: 15)')
    parser.add_argument('-s', '--specialized', type=int, default=15,
                       help='Number of specialized blogs (default: 15)')
    parser.add_argument('-a', '--articles', type=int, default=12,
                       help='Articles per blog (default: 12)')
    parser.add_argument('-t', '--threshold', type=int, default=8,
                       help='Quality threshold (default: 8)')
    parser.add_argument('-d', '--delay', type=float, default=2.0,
                       help='Delay between requests (default: 2.0)')
    
    args = parser.parse_args()
    
    # Create comprehensive downloader
    downloader = ComprehensiveEngineeringDownloader(
        output_dir=args.output,
        delay=args.delay
    )
    
    downloader.download_comprehensive_collection(
        mainstream_limit=args.mainstream,
        specialized_limit=args.specialized,
        articles_per_blog=args.articles,
        quality_threshold=args.threshold
    )


if __name__ == "__main__":
    main()