#!/usr/bin/env python3
"""
Expansion Systems Architecture Crawler

Targets high-value companies known for excellent system architecture content:
gaming, financial services, security, and underexplored tech giants.
"""

import requests
import time
import random
from pathlib import Path
from urllib.parse import urljoin
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from deduplication_tool import BlogDeduplicator

class ExpansionSystemsCrawler:
    """Crawler for high-value system architecture articles from new companies."""
    
    # High-value companies with excellent system architecture content
    EXPANSION_TARGETS = {
        # Gaming & Real-time Systems
        'discord': {
            'urls': [
                'https://discord.com/blog/engineering',
                'https://blog.discord.com/',
                'https://discord.com/blog/category/engineering',
            ],
            'focus': 'chat scaling, voice infrastructure, real-time systems'
        },
        'riot': {
            'urls': [
                'https://technology.riotgames.com/',
                'https://www.riotgames.com/en/news/tags/dev',
            ],
            'focus': 'game servers, global infrastructure, real-time gaming'
        },
        'github': {
            'urls': [
                'https://github.blog/category/engineering/',
                'https://githubengineering.com/',
                'https://github.blog/engineering/',
            ],
            'focus': 'git hosting, CI/CD systems, developer tools'
        },
        'twitch': {
            'urls': [
                'https://blog.twitch.tv/en/tags/engineering/',
                'https://blog.twitch.tv/en/',
            ],
            'focus': 'live streaming, video infrastructure, real-time chat'
        },
        
        # Financial Services & Security
        'capitalone': {
            'urls': [
                'https://www.capitalone.com/tech/blog/',
                'https://medium.com/capital-one-tech',
                'https://www.capitalone.com/tech/solutions/',
            ],
            'focus': 'fraud detection, ML infrastructure, financial systems'
        },
        'robinhood': {
            'urls': [
                'https://robinhood.engineering/',
                'https://blog.robinhood.com/category/engineering/',
            ],
            'focus': 'trading systems, financial infrastructure, mobile backends'
        },
        'coinbase': {
            'urls': [
                'https://blog.coinbase.com/tagged/engineering',
                'https://www.coinbase.com/blog/tags/engineering',
            ],
            'focus': 'cryptocurrency systems, security, trading infrastructure'
        },
        'auth0': {
            'urls': [
                'https://auth0.com/blog/dev/',
                'https://auth0.com/blog/engineering/',
            ],
            'focus': 'identity systems, authentication, security architecture'
        },
        
        # Database & Infrastructure Companies
        'mongodb': {
            'urls': [
                'https://www.mongodb.com/blog/channel/engineering-blog',
                'https://www.mongodb.com/developer/languages/',
            ],
            'focus': 'database internals, sharding, storage systems'
        },
        'planetscale': {
            'urls': [
                'https://planetscale.com/blog',
                'https://planetscale.com/blog/category/engineering',
            ],
            'focus': 'database systems, MySQL scaling, branching'
        },
        'fastly': {
            'urls': [
                'https://www.fastly.com/blog/engineering',
                'https://developer.fastly.com/learning/',
            ],
            'focus': 'CDN engineering, edge computing, performance'
        },
        
        # Underexplored Giants
        'google': {
            'urls': [
                'https://developers.googleblog.com/',
                'https://cloud.google.com/blog/products/engineering-productivity',
                'https://ai.googleblog.com/',
            ],
            'focus': 'distributed systems, search, ML infrastructure'
        },
        'microsoft': {
            'urls': [
                'https://devblogs.microsoft.com/',
                'https://azure.microsoft.com/en-us/blog/topics/architecture/',
                'https://techcommunity.microsoft.com/t5/azure-architecture-blog/bg-p/AzureArchitectureBlog',
            ],
            'focus': 'cloud infrastructure, distributed systems, Azure architecture'
        },
        'apple': {
            'urls': [
                'https://developer.apple.com/news/',
                'https://machinelearning.apple.com/',
            ],
            'focus': 'mobile systems, ML infrastructure, privacy-preserving systems'
        }
    }
    
    SYSTEM_KEYWORDS = {
        # Core system architecture
        'architecture': 20, 'system design': 25, 'infrastructure': 18, 
        'distributed system': 25, 'microservices': 20, 'scalability': 20,
        'performance': 15, 'real-time': 20, 'streaming': 18,
        
        # Implementation focus
        'how we built': 30, 'building our': 25, 'designing our': 22,
        'technical deep dive': 30, 'lessons learned': 25, 'at scale': 25,
        'engineering challenges': 22, 'migration': 18, 'optimization': 15,
        
        # System components
        'database': 15, 'api': 12, 'service': 12, 'pipeline': 18,
        'load balancing': 18, 'caching': 15, 'messaging': 15,
        'storage': 15, 'networking': 15, 'security': 12,
        
        # Domain-specific systems
        'game server': 25, 'chat system': 20, 'video streaming': 22,
        'fraud detection': 22, 'trading system': 25, 'payment': 18,
        'authentication': 18, 'identity': 15, 'cdn': 18,
        
        # Technical depth indicators
        'deep dive': 25, 'case study': 20, 'postmortem': 25,
        'technical decision': 22, 'design pattern': 18, 'tradeoff': 20,
    }
    
    EXCLUDE_KEYWORDS = {
        'announcement': -20, 'press release': -25, 'marketing': -25,
        'product launch': -18, 'feature update': -15, 'news': -12,
        'event': -10, 'conference': -8, 'webinar': -12, 'hiring': -15,
        'culture': -10, 'opinion': -8, 'trends': -10, 'predictions': -12,
    }
    
    def __init__(self, blogs_dir="blogs", max_per_company=20):
        self.blogs_dir = Path(blogs_dir)
        self.max_per_company = max_per_company
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        # Setup robust session
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        
        self.stats = {
            'companies_crawled': 0,
            'pages_explored': 0,
            'articles_found': 0,
            'high_quality_downloaded': 0,
            'duplicates_skipped': 0,
            'errors': 0,
        }
    
    def calculate_system_score(self, title, description="", content_preview=""):
        """Calculate comprehensive system architecture score."""
        text = f"{title} {description} {content_preview}".lower()
        score = 0
        
        # Positive keywords with multipliers
        for keyword, points in self.SYSTEM_KEYWORDS.items():
            if keyword in text:
                count = text.count(keyword)
                score += points * min(count, 2)
        
        # Negative keywords
        for keyword, penalty in self.EXCLUDE_KEYWORDS.items():
            if keyword in text:
                score += penalty
        
        # Bonus for specific system-building phrases
        system_phrases = [
            'how we built', 'building our', 'designing our', 'lessons from building',
            'technical deep dive', 'architecture overview', 'system design',
            'scaling our', 'migrating our', 'engineering at', 'infrastructure at'
        ]
        
        for phrase in system_phrases:
            if phrase in text:
                score += 20
        
        # Performance metrics bonus
        if re.search(r'\d+[kmgtpz]?\s*(qps|rps|ops|requests|queries|users|connections)', text):
            score += 15
            
        # Scale indicators
        if re.search(r'(billion|million|thousand).*?(users|requests|messages|transactions)', text):
            score += 12
        
        return max(0, score)
    
    def safe_request(self, url, timeout=12):
        """Make request with comprehensive error handling."""
        try:
            print(f"   🌐 Fetching: {url}")
            
            response = self.session.get(
                url, 
                timeout=timeout,
                allow_redirects=True,
                verify=False  # Some sites have SSL issues
            )
            
            if response.status_code == 200:
                return BeautifulSoup(response.content, 'html.parser')
            else:
                print(f"   ⚠️  HTTP {response.status_code}: {url}")
                return None
                
        except requests.exceptions.Timeout:
            print(f"   ⏱️  Timeout: {url}")
            return None
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:80]}")
            self.stats['errors'] += 1
            return None
    
    def extract_articles_smart(self, soup, base_url, company_focus):
        """Smart article extraction with multiple strategies."""
        if not soup:
            return []
        
        articles = []
        found_urls = set()
        
        # Strategy 1: Look for blog post patterns
        article_selectors = [
            # Standard blog selectors
            'article h1 a', 'article h2 a', 'article h3 a',
            '.post-title a', '.entry-title a', '.blog-post-title a',
            
            # Platform-specific
            '.post h2 a', '.entry h2 a', '.blog-item h2 a',
            '[data-testid="post-preview-title"] a',  # Medium
            
            # Generic content selectors
            '.content h2 a', '.article-title a', 'h1 a[href*="blog"]',
            'h2 a[href*="blog"]', 'h3 a[href*="blog"]',
            
            # Company-specific patterns
            '.news-item a', '.tech-post a', '.dev-blog a'
        ]
        
        for selector in article_selectors:
            for link in soup.select(selector):
                href = link.get('href')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 8:
                    continue
                
                # Make absolute URL
                if href.startswith('/'):
                    article_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    article_url = href
                else:
                    continue
                
                # Avoid duplicates
                if article_url in found_urls:
                    continue
                found_urls.add(article_url)
                
                # Extract description
                description = self.extract_article_description(link)
                
                # Score the article
                score = self.calculate_system_score(title, description)
                
                # High threshold for expansion companies
                if score >= 30:
                    articles.append({
                        'url': article_url,
                        'title': title,
                        'description': description,
                        'score': score,
                        'focus_area': company_focus
                    })
        
        # Strategy 2: Look for direct links with system keywords
        system_links = soup.find_all('a', href=True, string=re.compile(
            r'(architecture|infrastructure|system|scaling|engineering|technical)', 
            re.IGNORECASE
        ))
        
        for link in system_links:
            href = link.get('href')
            title = link.get_text(strip=True)
            
            if href and href not in found_urls and len(title) > 8:
                if href.startswith('/'):
                    article_url = urljoin(base_url, href)
                elif href.startswith('http'):
                    article_url = href
                else:
                    continue
                
                found_urls.add(article_url)
                score = self.calculate_system_score(title, "")
                
                if score >= 25:  # Slightly lower threshold for direct system links
                    articles.append({
                        'url': article_url,
                        'title': title,
                        'description': "",
                        'score': score,
                        'focus_area': company_focus
                    })
        
        return articles
    
    def extract_article_description(self, link_element):
        """Extract description from article element context."""
        descriptions = []
        
        # Look for description in parent elements
        parent = link_element.find_parent()
        if parent:
            desc_selectors = [
                '.excerpt', '.summary', '.description', '.subtitle',
                '.post-excerpt', '.entry-summary', 'p'
            ]
            
            for selector in desc_selectors:
                desc_elem = parent.select_one(selector)
                if desc_elem:
                    desc_text = desc_elem.get_text(strip=True)
                    if 20 < len(desc_text) < 500:
                        descriptions.append(desc_text)
                        break
        
        return ' '.join(descriptions[:1])  # Take first good description
    
    def download_expansion_article(self, company, article_info):
        """Download and save an expansion article."""
        try:
            url = article_info['url']
            title = article_info['title']
            score = article_info['score']
            focus_area = article_info['focus_area']
            
            print(f"   📥 Downloading (score: {score}): {title[:65]}...")
            
            soup = self.safe_request(url)
            if not soup:
                return False
            
            # Extract main content with multiple strategies
            content_elem = self.extract_main_content(soup)
            
            if not content_elem:
                print(f"   ❌ Could not extract content")
                return False
            
            # Convert to markdown
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            h.ignore_emphasis = False
            
            markdown_content = h.handle(str(content_elem))
            
            # Quality validation
            if len(markdown_content.strip()) < 1000:
                print(f"   ❌ Content too short ({len(markdown_content)} chars)")
                return False
            
            # Check for duplicate
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate detected, skipping")
                self.stats['duplicates_skipped'] += 1
                return False
            
            # Create company directory
            company_dir = self.blogs_dir / company
            company_dir.mkdir(parents=True, exist_ok=True)
            
            # Create safe filename
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:70]}.md"
            filepath = company_dir / filename
            
            # Handle filename conflicts
            counter = 1
            while filepath.exists():
                base_name = safe_title[:65]
                filepath = company_dir / f"{base_name}_{counter}.md"
                counter += 1
            
            # Create enhanced frontmatter
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
focus_area: "{focus_area}"
system_score: {score}
type: "expansion_systems"
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            # Update tracking
            self.existing_hashes.add(content_hash)
            self.stats['high_quality_downloaded'] += 1
            
            print(f"   ✅ Saved: {title[:50]}...")
            return True
            
        except Exception as e:
            print(f"   ❌ Error downloading {article_info.get('title', 'unknown')}: {e}")
            return False
    
    def extract_main_content(self, soup):
        """Extract main content using multiple strategies."""
        content_strategies = [
            # Standard content selectors
            lambda s: s.select_one('article'),
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('.entry-content'),
            lambda s: s.select_one('.content'),
            lambda s: s.select_one('main'),
            
            # Platform-specific
            lambda s: s.select_one('.story-content'),  # Medium
            lambda s: s.select_one('.postArticle-content'),  # Medium
            lambda s: s.select_one('[role="main"]'),
            lambda s: s.select_one('.blog-post-content'),
            
            # Fallback: largest text block
            lambda s: max(
                (div for div in s.find_all(['div', 'section']) 
                 if len(div.get_text(strip=True)) > 800), 
                key=lambda x: len(x.get_text(strip=True)), 
                default=None
            )
        ]
        
        for strategy in content_strategies:
            try:
                content_elem = strategy(soup)
                if content_elem and len(content_elem.get_text(strip=True)) > 800:
                    return content_elem
            except:
                continue
        
        return None
    
    def crawl_expansion_company(self, company, config):
        """Crawl a company for expansion system articles."""
        print(f"\n🏢 {company.upper()}")
        print("-" * 50)
        print(f"🎯 Focus: {config['focus']}")
        
        all_articles = []
        
        for url in config['urls'][:3]:  # Limit URLs per company
            soup = self.safe_request(url)
            self.stats['pages_explored'] += 1
            
            if soup:
                articles = self.extract_articles_smart(soup, url, config['focus'])
                all_articles.extend(articles)
                print(f"   📄 Found {len(articles)} system articles")
            
            # Respectful crawling
            time.sleep(random.uniform(3, 5))
        
        if not all_articles:
            print("   📭 No high-quality system articles found")
            return
        
        # Sort by score and take top articles
        all_articles.sort(key=lambda x: x['score'], reverse=True)
        top_articles = all_articles[:self.max_per_company]
        
        self.stats['articles_found'] += len(top_articles)
        print(f"   🎯 Selected {len(top_articles)} top articles")
        print(f"   📊 Score range: {top_articles[0]['score']}-{top_articles[-1]['score']}")
        
        # Download articles
        downloaded = 0
        for article in top_articles:
            if self.download_expansion_article(company, article):
                downloaded += 1
            
            # Respectful downloading
            time.sleep(random.uniform(2, 4))
        
        print(f"   ✅ Successfully downloaded {downloaded}/{len(top_articles)} articles")
        self.stats['companies_crawled'] += 1
    
    def run_expansion_crawl(self):
        """Run the complete expansion crawl."""
        print("🚀 EXPANSION SYSTEMS ARCHITECTURE CRAWL")
        print("=" * 60)
        print(f"🎯 Target: High-value system architecture from {len(self.EXPANSION_TARGETS)} companies")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing articles")
        print(f"📊 Quality threshold: 30+ system score")
        print(f"📝 Max per company: {self.max_per_company}")
        print("\n🎮 Gaming, 💰 Financial, 🛡️ Security, 🏗️ Infrastructure Companies")
        print()
        
        for company, config in self.EXPANSION_TARGETS.items():
            try:
                self.crawl_expansion_company(company, config)
                
                # Longer pause between companies for respectful crawling
                time.sleep(random.uniform(5, 8))
            except KeyboardInterrupt:
                print(f"\n⚠️  Interrupted during {company}")
                break
            except Exception as e:
                print(f"   ❌ Error processing {company}: {e}")
                continue
        
        # Final comprehensive statistics
        print("\n" + "=" * 60)
        print("🎉 EXPANSION CRAWL COMPLETE")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        final_count = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total articles in collection: {final_count}")
        
        if self.stats['high_quality_downloaded'] > 0:
            print(f"🚀 Successfully expanded with {self.stats['high_quality_downloaded']} new system architecture articles!")

def main():
    crawler = ExpansionSystemsCrawler(max_per_company=15)
    crawler.run_expansion_crawl()

if __name__ == "__main__":
    main()