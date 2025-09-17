#!/usr/bin/env python3
"""
Web-based Tech Blog Scraper

Alternative approach for blogs without accessible RSS feeds.
Scrapes blog listing pages and downloads individual articles.
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
    import html2text
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"Missing required dependency: {e}")
    print("Please install dependencies with:")
    print("pip install html2text beautifulsoup4 requests")
    sys.exit(1)


class WebScraper:
    def __init__(self, output_dir="articles", delay=2.0):
        """
        Initialize the web scraper.
        
        Args:
            output_dir (str): Directory to save markdown files
            delay (float): Delay between requests in seconds
        """
        self.output_dir = Path(output_dir)
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache'
        })
        
        # Configure html2text for better markdown conversion
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.body_width = 0
        self.html_converter.single_line_break = True
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def sanitize_filename(self, title):
        """Convert article title to safe filename."""
        filename = re.sub(r'[<>:"/\\|?*]', '', title)
        filename = re.sub(r'\s+', '_', filename.strip())
        filename = filename[:100]
        filename = filename.rstrip('._')
        return filename or "untitled"
    
    def extract_uber_article_links(self, base_url="https://www.uber.com/blog/engineering/", max_pages=3):
        """
        Extract article links from Uber's engineering blog listing pages.
        
        Args:
            base_url (str): Base URL of the blog
            max_pages (int): Maximum number of listing pages to scrape
            
        Returns:
            list: List of article URLs
        """
        article_urls = []
        
        for page in range(1, max_pages + 1):
            if page == 1:
                url = base_url
            else:
                url = f"{base_url}?page={page}"
                
            print(f"Scraping page {page}: {url}")
            
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Look for article links (Uber-specific selectors)
                # The listing page contains markdown-style links like [text](/blog/article/)
                found_links = []
                
                # Find all links that go to individual blog posts
                all_links = soup.find_all('a', href=True)
                for link in all_links:
                    href = link.get('href')
                    if href and '/blog/' in href and href != '/blog/engineering/ai/' and href != '/blog/engineering/':
                        # Skip pagination and category links
                        if 'page/' not in href and '/ai/' != href.rstrip('/'):
                            found_links.append(link)
                
                page_urls = []
                for link in found_links:
                    href = link.get('href')
                    if href:
                        full_url = urljoin(base_url, href)
                        if full_url not in article_urls and '/engineering/' in full_url:
                            article_urls.append(full_url)
                            page_urls.append(full_url)
                
                print(f"Found {len(page_urls)} article links on page {page}")
                
                if not page_urls:
                    print(f"No more articles found, stopping at page {page}")
                    break
                    
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"Error scraping page {page}: {e}")
                break
        
        return article_urls
    
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
            for element in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
                element.decompose()
            
            # Remove common unwanted classes
            unwanted_classes = ['sidebar', 'related-posts', 'comments', 'navigation', 'breadcrumb']
            for class_name in unwanted_classes:
                for element in soup.find_all(class_=re.compile(class_name)):
                    element.decompose()
            
            # Try different selectors for article content
            content_selectors = [
                'article',
                '.post-content',
                '.entry-content', 
                '.content',
                '.post-body',
                '.article-content',
                '.blog-post-content',
                'main',
                '.blog-post'
            ]
            
            content_element = None
            for selector in content_selectors:
                content_element = soup.select_one(selector)
                if content_element and len(content_element.get_text().strip()) > 200:
                    break
                    
            if not content_element:
                # Fallback to largest text container
                containers = soup.find_all(['div', 'section'], string=False)
                content_element = max(containers, key=lambda x: len(x.get_text()), default=None)
                
            if not content_element:
                return None
                
            # Extract metadata
            title = soup.find('title')
            title_text = title.get_text().strip() if title else "Untitled"
            
            # Clean up title (remove site name)
            title_text = re.sub(r'\s*\|\s*Uber.*$', '', title_text)
            title_text = re.sub(r'\s*-\s*Uber.*$', '', title_text)
            
            # Look for h1 as backup title
            if not title_text or title_text == "Untitled":
                h1 = soup.find('h1')
                if h1:
                    title_text = h1.get_text().strip()
            
            # Look for author info
            author_selectors = [
                '.author',
                '.byline',
                '.post-author',
                '[rel="author"]',
                '.entry-author',
                '.author-name'
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
                '.post-date',
                '.publish-date'
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
            
            # Clean up markdown
            markdown_content = re.sub(r'\n\s*\n\s*\n', '\n\n', markdown_content)
            
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
    
    def scrape_uber_blog(self, max_articles=10, max_pages=3):
        """
        Scrape Uber's engineering blog.
        
        Args:
            max_articles (int): Maximum number of articles to download
            max_pages (int): Maximum number of listing pages to scrape
        """
        print("🚗 Scraping Uber Engineering Blog")
        
        # Extract article URLs
        article_urls = self.extract_uber_article_links(max_pages=max_pages)
        
        if not article_urls:
            print("No article URLs found")
            return
        
        print(f"Found {len(article_urls)} article URLs")
        
        # Limit to max_articles
        if max_articles:
            article_urls = article_urls[:max_articles]
            print(f"Limiting to {len(article_urls)} articles")
        
        downloaded = 0
        failed = 0
        
        for i, url in enumerate(article_urls):
            print(f"\n[{i+1}/{len(article_urls)}] Processing: {url}")
            
            # Extract and save article
            article_data = self.extract_article_content(url)
            if article_data and self.save_article(article_data, "uber_engineering"):
                downloaded += 1
            else:
                failed += 1
            
            # Rate limiting
            if self.delay > 0:
                time.sleep(self.delay)
        
        print(f"\n📊 Summary:")
        print(f"Downloaded: {downloaded}")
        print(f"Failed: {failed}")
        print(f"Total processed: {downloaded + failed}")


def main():
    parser = argparse.ArgumentParser(description="Scrape Uber's engineering blog articles")
    parser.add_argument('-o', '--output', default='articles', 
                       help='Output directory for markdown files (default: articles)')
    parser.add_argument('-m', '--max', type=int, default=10,
                       help='Maximum number of articles to download (default: 10)')
    parser.add_argument('-p', '--pages', type=int, default=3,
                       help='Maximum number of listing pages to scrape (default: 3)')
    parser.add_argument('-d', '--delay', type=float, default=2.0,
                       help='Delay between requests in seconds (default: 2.0)')
    
    args = parser.parse_args()
    
    # Create scraper and start scraping
    scraper = WebScraper(output_dir=args.output, delay=args.delay)
    scraper.scrape_uber_blog(
        max_articles=args.max,
        max_pages=args.pages
    )


if __name__ == "__main__":
    main()