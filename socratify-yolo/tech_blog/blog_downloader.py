#!/usr/bin/env python3
"""
Tech Blog Article Downloader

Downloads articles from tech blog RSS feeds and converts them to markdown files.
Handles HTML parsing, content extraction, and markdown conversion.
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
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with:")
    print("pip install feedparser html2text beautifulsoup4 requests")
    sys.exit(1)


class BlogDownloader:
    def __init__(self, output_dir="articles", delay=1.0):
        """
        Initialize the blog downloader.
        
        Args:
            output_dir (str): Directory to save markdown files
            delay (float): Delay between requests in seconds
        """
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/rss+xml, application/xml, text/xml, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        })
        
        # Configure html2text for better markdown conversion
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0  # Don't wrap lines
        self.html_converter.single_line_break = True
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def sanitize_filename(self, title):
        """Convert article title to safe filename."""
        # Remove/replace problematic characters
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        # Limit length
        filename = filename[:100]
        # Remove trailing periods and spaces
        filename = filename.rstrip('._')
        return filename or "untitled"
    
    def extract_article_content(self, url):
        """
        Extract main article content from webpage.
        
        Args:
            url (str): Article URL
            
        Returns:
            dict: Article metadata and content
        """
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside']):
                element.decompose()
            
            # Try different selectors for article content
            content_selectors = [
                'article',
                '.post-content',
                '.entry-content', 
                '.content',
                '.post-body',
                '.article-content',
                'main',
                '.blog-post'
            ]
            
            content_element = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element:
                    break
                    
            if not content_element:
                # Fallback to body if no specific content area found
                content_element = soup.find('body')
                
            if not content_element:
                return None
                
            # Extract metadata
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Untitled"
            
            # Look for author info
            author_selectors = [
                '.author',
                '.byline',
                '.post-author',
                '[rel="author"]',
                '.entry-author'
            ]
            
            author = "Unknown"
            for selector in author_selectors:
                author_elem = soup.select_one(selector)
                if author_elem:
                    author = author_elem.get_text().strip()
                    break
            
            # Look for publish date
            date_selectors = [
                'time[datetime]',
                '.date',
                '.published',
                '.post-date'
            ]
            
            pub_date = None
            for selector in date_selectors:
                date_elem = soup.select_one(selector)
                if date_elem:
                    if date_elem.get('datetime'):
                        pub_date = date_elem['datetime']
                    else:
                        pub_date = date_elem.get_text().strip()
                    break
            
            # Convert content to markdown
            html_content = str(content_element)
            markdown_content = self.html_converter.handle(html_content)
            
            return {
                'title': title_text,
                'author': author,
                'url': url,
                'published_date': pub_date,
                'content': markdown_content
            }
            
        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None
    
    def save_article(self, article_data, blog_name):
        """
        Save article as markdown file.
        
        Args:
            article_data (dict): Article content and metadata
            blog_name (str): Name of the blog for subdirectory
        """
        if not article_data:
            return False
            
        # Create blog-specific subdirectory
        blog_dir = self.output_dir / blog_name
        blog_dir.mkdir(exist_ok=True)
        
        # Create filename
        safe_title = self.sanitize_filename(article_data['title'])
        filename = f"{safe_title}.md"
        filepath = blog_dir / filename
        
        # Handle duplicate filenames
        counter = 1
        while filepath.exists():
            filename = f"{safe_title}_{counter}.md"
            filepath = blog_dir / filename
            counter += 1
        
        # Create markdown content with frontmatter
        frontmatter = f"""---
title: "{article_data['title'].replace('"', '\\"')}"
author: "{article_data['author']}"
url: "{article_data['url']}"
published_date: "{article_data.get('published_date', 'Unknown')}"
downloaded_date: "{datetime.now().isoformat()}"
---

"""
        
        full_content = frontmatter + article_data['content']
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(full_content)
            print(f"✓ Saved: {filepath}")
            return True
        except Exception as e:
            print(f"✗ Error saving {filepath}: {e}")
            return False
    
    def download_from_rss(self, rss_url, max_articles=None, skip_existing=True):
        """
        Download articles from RSS feed.
        
        Args:
            rss_url (str): RSS feed URL
            max_articles (int): Maximum number of articles to download
            skip_existing (bool): Skip articles that already exist as files
        """
        print(f"Fetching RSS feed: {rss_url}")
        
        try:
            # Try to fetch RSS feed with custom headers first
            response = self.session.get(rss_url, timeout=30)
            print(f"RSS fetch status: {response.status_code}")
            
            if response.status_code == 200:
                # Parse RSS feed from response content
                feed = feedparser.parse(response.content)
            else:
                # Fallback to direct feedparser parsing
                print(f"Direct fetch failed ({response.status_code}), trying feedparser...")
                feed = feedparser.parse(rss_url)
            
            if not feed.entries:
                print("No articles found in RSS feed")
                return
                
            # Extract blog name from feed or URL
            blog_name = "unknown_blog"
            if hasattr(feed, 'feed') and hasattr(feed.feed, 'title'):
                blog_name = self.sanitize_filename(feed.feed.title)
            else:
                parsed_url = urlparse(rss_url)
                blog_name = parsed_url.netloc.replace('www.', '').replace('.', '_')
            
            print(f"Found {len(feed.entries)} articles in feed")
            print(f"Blog: {blog_name}")
            
            downloaded = 0
            skipped = 0
            failed = 0
            
            for i, entry in enumerate(feed.entries):
                if max_articles and downloaded >= max_articles:
                    break
                    
                title = entry.get('title', 'Untitled')
                url = entry.get('link', '')
                
                if not url:
                    print(f"✗ Skipping article without URL: {title}")
                    failed += 1
                    continue
                
                # Check if file already exists
                if skip_existing:
                    safe_title = self.sanitize_filename(title)
                    blog_dir = self.output_dir / blog_name
                    potential_files = list(blog_dir.glob(f"{safe_title}*.md"))
                    if potential_files:
                        print(f"⏭ Skipping existing: {title}")
                        skipped += 1
                        continue
                
                print(f"\n[{i+1}/{len(feed.entries)}] Processing: {title}")
                print(f"URL: {url}")
                
                # Extract and save article
                article_data = self.extract_article_content(url)
                if article_data and self.save_article(article_data, blog_name):
                    downloaded += 1
                else:
                    failed += 1
                
                # Rate limiting
                if self.delay > 0:
                    time.sleep(self.delay)
            
            print(f"\n📊 Summary:")
            print(f"Downloaded: {downloaded}")
            print(f"Skipped: {skipped}")
            print(f"Failed: {failed}")
            print(f"Total processed: {downloaded + skipped + failed}")
            
        except Exception as e:
            print(f"Error processing RSS feed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Download tech blog articles from RSS feeds")
    parser.add_argument('rss_url', help='RSS feed URL to download from')
    parser.add_argument('-o', '--output', default='articles', 
                       help='Output directory for markdown files (default: articles)')
    parser.add_argument('-m', '--max', type=int,
                       help='Maximum number of articles to download')
    parser.add_argument('-d', '--delay', type=float, default=1.0,
                       help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--overwrite', action='store_true',
                       help='Overwrite existing files')
    
    args = parser.parse_args()
    
    # Create downloader and start downloading
    downloader = BlogDownloader(output_dir=args.output, delay=args.delay)
    downloader.download_from_rss(
        rss_url=args.rss_url,
        max_articles=args.max,
        skip_existing=not args.overwrite
    )


if __name__ == "__main__":
    main()