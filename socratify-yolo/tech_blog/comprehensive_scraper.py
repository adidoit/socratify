#!/usr/bin/env python3
"""
Comprehensive Tech Blog Scraper

Enhanced version that discovers and downloads many more articles
by exploring multiple pages, categories, and time periods.
"""

import os
import re
import sys
import time
import argparse
import requests
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse, parse_qs
from pathlib import Path
import json

try:
    import html2text
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with:")
    print("pip install html2text beautifulsoup4 requests")
    sys.exit(1)


class ComprehensiveScraper:
    def __init__(self, output_dir="articles", delay=2.0):
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0
        self.html_converter.single_line_break = True
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.discovered_urls = set()
        
    def sanitize_filename(self, title):
        """Convert article title to safe filename."""
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        filename = filename[:100]
        filename = filename.rstrip('._')
        return filename or "untitled"
    
    def discover_uber_articles(self, max_pages=20, explore_categories=True):
        """
        Comprehensively discover Uber engineering articles.
        
        Args:
            max_pages (int): Maximum number of pages to explore
            explore_categories (bool): Whether to explore different categories
        
        Returns:
            set: All discovered article URLs
        """
        print(f"🔍 Discovering Uber engineering articles...")
        
        base_urls_to_explore = [
            "https://www.uber.com/blog/engineering/",
            "https://www.uber.com/blog/engineering/ai/",
            "https://www.uber.com/blog/engineering/backend/",
            "https://www.uber.com/blog/engineering/data/",
        ]
        
        if explore_categories:
            # Try to discover more categories
            base_urls_to_explore.extend(self.discover_categories())
        
        all_discovered = set()
        
        for base_url in base_urls_to_explore:
            print(f"\n📂 Exploring: {base_url}")
            urls_from_base = self.explore_paginated_listing(base_url, max_pages)
            all_discovered.update(urls_from_base)
            print(f"   Found {len(urls_from_base)} articles from this section")
            time.sleep(self.delay)
        
        print(f"\n🎯 Total unique articles discovered: {len(all_discovered)}")
        return all_discovered
    
    def discover_categories(self):
        """Discover different blog categories/sections."""
        categories = []
        try:
            response = self.session.get("https://www.uber.com/blog/engineering/", timeout=30)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for category links
            category_patterns = [
                r'/blog/engineering/[^/]+/?$',
                r'/blog/[^/]+/?$'
            ]
            
            for pattern in category_patterns:
                category_links = soup.find_all('a', href=re.compile(pattern))
                for link in category_links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin("https://www.uber.com", href)
                        if full_url not in categories and '/page/' not in full_url:
                            categories.append(full_url)
            
            print(f"📂 Discovered {len(categories)} category sections")
            return categories[:10]  # Limit to avoid too many
            
        except Exception as e:
            print(f"Warning: Could not discover categories: {e}")
            return []
    
    def explore_paginated_listing(self, base_url, max_pages=20):
        """Explore all pages of a blog listing."""
        discovered = set()
        
        for page in range(1, max_pages + 1):
            # Try different pagination patterns
            page_urls = [
                f"{base_url}?page={page}" if page > 1 else base_url,
                f"{base_url}page/{page}/" if page > 1 else base_url,
                f"{base_url}?p={page}" if page > 1 else base_url,
            ]
            
            page_found = False
            for page_url in page_urls:
                if page_found:
                    break
                    
                try:
                    response = self.session.get(page_url, timeout=30)
                    if response.status_code != 200:
                        continue
                        
                    soup = BeautifulSoup(response.content, 'html.parser')
                    page_articles = self.extract_article_urls_from_page(soup, base_url)
                    
                    if page_articles:
                        discovered.update(page_articles)
                        print(f"   Page {page}: {len(page_articles)} articles")
                        page_found = True
                        time.sleep(self.delay / 2)  # Shorter delay for pagination
                    elif page > 1:
                        print(f"   Page {page}: No articles found, stopping pagination")
                        return discovered
                        
                except Exception as e:
                    print(f"   Error on page {page}: {e}")
                    continue
            
            if not page_found and page > 1:
                break
                
        return discovered
    
    def extract_article_urls_from_page(self, soup, base_url):
        """Extract article URLs from a single page."""
        article_urls = set()
        
        # Multiple strategies to find article links
        strategies = [
            # Strategy 1: Look for links containing /blog/ 
            lambda: soup.find_all('a', href=re.compile(r'/blog/[^/]+/[^/]+/?$')),
            
            # Strategy 2: Look in common article containers
            lambda: [link for container in soup.find_all(['article', '.post', '.entry']) 
                    for link in container.find_all('a', href=True)],
            
            # Strategy 3: Look for title links
            lambda: [link for heading in soup.find_all(['h1', 'h2', 'h3']) 
                    for link in heading.find_all('a', href=True)],
            
            # Strategy 4: Any link with blog in the URL
            lambda: soup.find_all('a', href=re.compile(r'/blog/')),
        ]
        
        for strategy in strategies:
            try:
                links = strategy()
                for link in links:
                    href = link.get('href')
                    if href and self.is_valid_article_url(href):
                        full_url = urljoin(base_url, href)
                        article_urls.add(full_url)
            except:
                continue
        
        return article_urls
    
    def is_valid_article_url(self, url):
        """Check if URL looks like a valid article."""
        # Skip pagination, categories, and other non-article URLs
        skip_patterns = [
            r'/page/\d+',
            r'/(ai|backend|data|engineering)/?$',
            r'/blog/?$',
            r'/blog/engineering/?$',
            r'/tag/',
            r'/category/',
            r'/author/',
            r'\?page=',
            r'#',
        ]
        
        for pattern in skip_patterns:
            if re.search(pattern, url):
                return False
        
        # Must be a blog URL with some depth
        if '/blog/' in url and url.count('/') >= 4:
            return True
            
        return False
    
    def extract_article_content(self, url):
        """Extract article content from URL."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
                element.decompose()
            
            # Remove ads, sidebars, etc.
            unwanted_classes = ['sidebar', 'related-posts', 'comments', 'navigation', 'breadcrumb', 'social-share']
            for class_name in unwanted_classes:
                for element in soup.find_all(class_=re.compile(class_name, re.I)):
                    element.decompose()
            
            # Find main content
            content_selectors = [
                'article',
                '[role="main"]',
                'main',
                '.post-content',
                '.entry-content',
                '.article-content',
                '.content',
                '.post-body'
            ]
            
            content_element = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element and len(content_element.get_text().strip()) > 500:
                    break
            
            if not content_element:
                # Fallback: find largest content div
                divs = soup.find_all('div')
                content_element = max(divs, key=lambda x: len(x.get_text()), default=None)
            
            if not content_element:
                return None
            
            # Extract metadata
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Untitled"
            title_text = re.sub(r'\s*[\|\-]\s*Uber.*$', '', title_text)
            
            # Try h1 as backup
            if not title_text or title_text == "Untitled":
                h1 = soup.find('h1')
                if h1:
                    title_text = h1.get_text().strip()
            
            # Extract author
            author_selectors = ['.author', '.byline', '.post-author', '[rel="author"]']
            author = "Unknown"
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    author = author_elem.get_text().strip()
                    break
            
            # Extract date
            date_selectors = ['time[datetime]', '.date', '.published', '.post-date']
            pub_date = None
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    pub_date = date_elem.get('datetime', date_elem.get_text().strip())
                    break
            
            # Convert to markdown
            html_content = str(content_element)
            markdown_content = self.html_converter.handle(html_content)
            markdown_content = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_content)
            
            return {
                'title': title_text,
                'author': author,
                'url': url,
                'published_date': pub_date,
                'content': markdown_content
            }
            
        except Exception as e:
            print(f"❌ Error extracting {url}: {e}")
            return None
    
    def save_article(self, article_data, blog_name):
        """Save article as markdown file."""
        if not article_data:
            return False
        
        blog_dir = self.output_dir / blog_name
        blog_dir.mkdir(exist_ok=True)
        
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
published_date: "{article_data.get('published_date', 'Unknown')}"
downloaded_date: "{datetime.now().isoformat()}"
---

"""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + article_data['content'])
            print(f"✅ Saved: {safe_title}")
            return True
        except Exception as e:
            print(f"❌ Error saving {safe_title}: {e}")
            return False
    
    def comprehensive_download(self, max_articles=100, max_pages=20):
        """Perform comprehensive download of Uber engineering articles."""
        print("🚗 Comprehensive Uber Engineering Blog Download")
        print("=" * 50)
        
        # Step 1: Discover all articles
        all_urls = self.discover_uber_articles(max_pages=max_pages, explore_categories=True)
        
        # Step 2: Limit if requested
        urls_to_download = list(all_urls)[:max_articles] if max_articles else list(all_urls)
        
        print(f"\n📥 Downloading {len(urls_to_download)} articles...")
        
        # Step 3: Download articles
        downloaded = 0
        failed = 0
        
        for i, url in enumerate(urls_to_download, 1):
            print(f"\n[{i}/{len(urls_to_download)}] {url}")
            
            article_data = self.extract_article_content(url)
            if article_data and self.save_article(article_data, "uber_engineering"):
                downloaded += 1
            else:
                failed += 1
            
            time.sleep(self.delay)
        
        print(f"\n📊 Final Summary:")
        print(f"✅ Downloaded: {downloaded}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Articles saved in: {self.output_dir}/uber_engineering/")
        
        return downloaded, failed


def main():
    parser = argparse.ArgumentParser(description="Comprehensive Uber blog scraper")
    parser.add_argument('-o', '--output', default='comprehensive_articles',
                       help='Output directory (default: comprehensive_articles)')
    parser.add_argument('-m', '--max', type=int, default=100,
                       help='Maximum articles to download (default: 100)')
    parser.add_argument('-p', '--pages', type=int, default=20,
                       help='Maximum pages to explore (default: 20)')
    parser.add_argument('-d', '--delay', type=float, default=2.0,
                       help='Delay between requests (default: 2.0)')
    
    args = parser.parse_args()
    
    scraper = ComprehensiveScraper(output_dir=args.output, delay=args.delay)
    scraper.comprehensive_download(
        max_articles=args.max,
        max_pages=args.pages
    )


if __name__ == "__main__":
    main()