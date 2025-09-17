#!/usr/bin/env python3
"""
Extract and Download Individual Articles

Extracts article URLs from the downloaded listing page and downloads individual articles.
"""

import re
import time
from pathlib import Path
from web_scraper import WebScraper

def extract_urls_from_markdown(file_path):
    """Extract blog article URLs from the downloaded markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all URLs in markdown links that point to blog articles
    # Pattern matches [text](/blog/article-name/)
    url_pattern = r'\]\(/blog/[^)]+/\)'
    matches = re.findall(url_pattern, content)
    
    urls = []
    for match in matches:
        # Extract just the URL part (remove '](' and ')')
        url = match[2:-1]  # Remove '](' from start and ')' from end
        
        # Skip certain URLs
        skip_patterns = [
            '/blog/engineering/ai/page/',
            '/blog/engineering/ai/',
            '/blog/engineering/',
            '/blog/earn/',
            '/blog/ride/',
            '/blog/eat/',
            '/blog/merchants/',
            '/blog/business/',
            '/blog/freight/',
            '/blog/health/',
            '/blog/higher-education/',
            '/blog/transit/'
        ]
        
        should_skip = any(pattern in url for pattern in skip_patterns)
        if not should_skip and url not in urls:
            urls.append(url)
    
    return urls

def main():
    # Extract URLs from the downloaded listing
    markdown_file = Path("uber_articles/uber_engineering/Uber_AI.md")
    
    if not markdown_file.exists():
        print(f"Markdown file not found: {markdown_file}")
        return
    
    print(f"Extracting URLs from {markdown_file}")
    article_urls = extract_urls_from_markdown(markdown_file)
    
    print(f"Found {len(article_urls)} article URLs:")
    for i, url in enumerate(article_urls[:10], 1):  # Show first 10
        print(f"{i:2d}. {url}")
    if len(article_urls) > 10:
        print(f"    ... and {len(article_urls) - 10} more")
    
    # Initialize scraper
    scraper = WebScraper(output_dir="uber_articles", delay=2.0)
    
    # Download individual articles
    downloaded = 0
    failed = 0
    
    for i, relative_url in enumerate(article_urls[:15]):  # Limit to first 15 articles
        full_url = f"https://www.uber.com{relative_url}"
        print(f"\n[{i+1}/{min(15, len(article_urls))}] Processing: {full_url}")
        
        # Extract and save article
        article_data = scraper.extract_article_content(full_url)
        if article_data and scraper.save_article(article_data, "uber_engineering"):
            downloaded += 1
        else:
            failed += 1
        
        # Rate limiting
        time.sleep(scraper.delay)
    
    print(f"\n📊 Summary:")
    print(f"Downloaded: {downloaded}")
    print(f"Failed: {failed}")
    print(f"Total processed: {downloaded + failed}")

if __name__ == "__main__":
    main()