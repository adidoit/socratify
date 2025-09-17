#!/usr/bin/env python3
"""
Comprehensive Systems Architecture Collector

Targets ALL remaining high-value system architecture sources:
- Real-time collaboration (Slack, Figma, Notion, Linear)
- Financial/Trading systems (Jane Street, etc.)
- Data infrastructure (Snowflake, Databricks, etc.)
- Video streaming (Zoom, YouTube)
- Modern startups with excellent technical blogs
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

class ComprehensiveSystemsCollector:
    """Comprehensive collector for all high-value system architecture content."""
    
    # ALL high-value system architecture sources
    COMPREHENSIVE_TARGETS = {
        # 🔥 Real-time Collaboration Systems
        'slack': {
            'urls': [
                'https://slack.engineering/',
                'https://slack.engineering/category/backend/',
                'https://slack.engineering/category/infrastructure/',
            ],
            'focus': 'chat systems, real-time messaging, scaling slack'
        },
        'figma': {
            'urls': [
                'https://www.figma.com/blog/engineering/',
                'https://www.figma.com/blog/tag/engineering/',
            ],
            'focus': 'real-time collaboration, multiplayer systems, operational transform'
        },
        'notion': {
            'urls': [
                'https://www.notion.so/blog/topic/engineering',
                'https://www.notion.so/blog/engineering',
            ],
            'focus': 'block-based systems, database architecture, real-time sync'
        },
        'linear': {
            'urls': [
                'https://linear.app/blog/category/engineering',
                'https://linear.app/blog',
            ],
            'focus': 'performance optimization, real-time updates, frontend/backend sync'
        },
        
        # 🎥 Video & Communication Infrastructure
        'zoom': {
            'urls': [
                'https://blog.zoom.us/category/engineering/',
                'https://medium.com/zoom-developer-blog',
            ],
            'focus': 'video infrastructure, WebRTC, real-time communication'
        },
        'youtube': {
            'urls': [
                'https://blog.youtube/inside-youtube/engineering/',
                'https://developers.googleblog.com/search/label/YouTube',
            ],
            'focus': 'video serving, content delivery, massive scale streaming'
        },
        
        # 💰 Financial & Trading Systems
        'janestreet': {
            'urls': [
                'https://blog.janestreet.com/',
                'https://blog.janestreet.com/category/ocaml/',
                'https://blog.janestreet.com/category/systems/',
            ],
            'focus': 'trading systems, OCaml, low-latency, financial infrastructure'
        },
        'twosigma': {
            'urls': [
                'https://www.twosigma.com/articles/',
                'https://medium.com/@twosigma',
            ],
            'focus': 'quantitative trading, data infrastructure, ML systems'
        },
        
        # 📊 Modern Data Infrastructure
        'snowflake': {
            'urls': [
                'https://www.snowflake.com/blog/engineering/',
                'https://medium.com/snowflake',
            ],
            'focus': 'data warehouse architecture, cloud data platform'
        },
        'databricks': {
            'urls': [
                'https://databricks.com/blog/category/engineering',
                'https://databricks.com/blog/category/platform',
            ],
            'focus': 'data lakehouse, Spark optimization, ML infrastructure'
        },
        'dbt': {
            'urls': [
                'https://blog.getdbt.com/category/engineering/',
                'https://docs.getdbt.com/blog',
            ],
            'focus': 'data transformation pipelines, analytics engineering'
        },
        'segment': {
            'urls': [
                'https://segment.com/blog/engineering/',
                'https://segment.com/blog/category/engineering/',
            ],
            'focus': 'customer data platform, event streaming, data pipelines'
        },
        'posthog': {
            'urls': [
                'https://posthog.com/blog/engineering',
                'https://posthog.com/blog/categories/engineering',
            ],
            'focus': 'product analytics, real-time events, open source analytics'
        },
        
        # 🚀 Infrastructure & Developer Tools
        'vercel': {
            'urls': [
                'https://vercel.com/blog/category/engineering',
                'https://vercel.com/blog',
            ],
            'focus': 'edge computing, deployment systems, frontend infrastructure'
        },
        'fly': {
            'urls': [
                'https://fly.io/blog/',
                'https://fly.io/blog/tags/engineering/',
            ],
            'focus': 'edge computing, global deployment, container orchestration'
        },
        'render': {
            'urls': [
                'https://render.com/blog',
                'https://render.com/blog/engineering',
            ],
            'focus': 'deployment infrastructure, cloud platforms'
        },
        'supabase': {
            'urls': [
                'https://supabase.com/blog',
                'https://supabase.com/blog/tags/engineering',
            ],
            'focus': 'real-time database, PostgreSQL scaling, backend-as-a-service'
        },
        'neon': {
            'urls': [
                'https://neon.tech/blog',
                'https://neon.tech/blog/tag/engineering',
            ],
            'focus': 'serverless PostgreSQL, database branching, storage separation'
        },
        
        # 🎮 Gaming Infrastructure (More Companies)
        'roblox': {
            'urls': [
                'https://blog.roblox.com/category/engineering/',
                'https://blog.roblox.com/tag/engineering/',
            ],
            'focus': 'multiplayer game systems, user-generated content, massive scale gaming'
        },
        'unity': {
            'urls': [
                'https://blog.unity.com/technology',
                'https://blog.unity.com/engine-platform',
            ],
            'focus': 'game engine architecture, real-time 3D, cross-platform systems'
        },
        
        # 🛡️ Security & Identity Systems
        'okta': {
            'urls': [
                'https://developer.okta.com/blog/',
                'https://www.okta.com/blog/category/engineering/',
            ],
            'focus': 'identity systems, authentication, security architecture'
        },
        '1password': {
            'urls': [
                'https://blog.1password.com/category/engineering/',
                '1password.com/blog/tag/development/',
            ],
            'focus': 'security architecture, cryptography, password management'
        },
        
        # 🔍 Search & Discovery
        'algolia': {
            'urls': [
                'https://www.algolia.com/blog/engineering/',
                'https://www.algolia.com/blog/category/engineering/',
            ],
            'focus': 'search systems, real-time indexing, search-as-a-service'
        },
        'elasticsearch': {
            'urls': [
                'https://www.elastic.co/blog/category/engineering',
                'https://www.elastic.co/blog/elasticsearch',
            ],
            'focus': 'distributed search, log analytics, observability'
        },
        
        # 📈 Observability & Monitoring
        'grafana': {
            'urls': [
                'https://grafana.com/blog/category/engineering/',
                'https://grafana.com/blog/tags/technical/',
            ],
            'focus': 'monitoring systems, observability, time-series data'
        },
        'datadog': {
            'urls': [
                'https://www.datadoghq.com/blog/engineering/',
                'https://www.datadoghq.com/blog/category/engineering/',
            ],
            'focus': 'monitoring infrastructure, observability at scale'
        },
        
        # 🔄 Workflow & Orchestration
        'temporal': {
            'urls': [
                'https://temporal.io/blog',
                'https://docs.temporal.io/blog',
            ],
            'focus': 'workflow orchestration, distributed systems, fault tolerance'
        },
        'airbyte': {
            'urls': [
                'https://airbyte.com/blog/category/engineering',
                'https://airbyte.com/blog',
            ],
            'focus': 'data integration pipelines, ETL systems, connector architecture'
        },
        
        # 💎 Modern Infrastructure Companies
        'retool': {
            'urls': [
                'https://retool.com/blog/category/engineering/',
                'https://retool.com/blog/engineering',
            ],
            'focus': 'internal tool architecture, low-code platforms, developer productivity'
        },
        'planetscale': {
            'urls': [
                'https://planetscale.com/blog',
                'https://planetscale.com/blog/tag/engineering',
            ],
            'focus': 'database branching, MySQL scaling, schema migrations'
        }
    }
    
    # Enhanced system keywords for comprehensive scoring
    SYSTEM_KEYWORDS = {
        # Core system architecture
        'architecture': 25, 'system design': 30, 'infrastructure': 22, 
        'distributed system': 30, 'microservices': 25, 'scalability': 25,
        'performance': 20, 'real-time': 25, 'streaming': 22,
        
        # Implementation & engineering
        'how we built': 35, 'building our': 30, 'designing our': 28,
        'technical deep dive': 35, 'lessons learned': 30, 'at scale': 30,
        'engineering challenges': 28, 'migration': 22, 'optimization': 20,
        
        # System components & patterns
        'database': 20, 'api': 15, 'service': 15, 'pipeline': 22,
        'load balancing': 22, 'caching': 20, 'messaging': 20,
        'storage': 20, 'networking': 20, 'security': 18,
        
        # Specific system types
        'multiplayer': 30, 'collaboration': 25, 'real-time sync': 28,
        'video streaming': 25, 'chat system': 25, 'game server': 28,
        'trading system': 30, 'fraud detection': 25, 'payment': 22,
        'authentication': 22, 'identity': 20, 'search': 20,
        
        # Advanced technical concepts
        'operational transform': 35, 'consensus': 30, 'replication': 25,
        'sharding': 25, 'partitioning': 25, 'eventual consistency': 28,
        'low latency': 28, 'high throughput': 25, 'fault tolerance': 25,
        
        # Quality indicators
        'deep dive': 30, 'case study': 25, 'postmortem': 30,
        'technical decision': 28, 'design pattern': 22, 'tradeoff': 25,
        'lessons from': 28, 'why we': 25, 'our approach': 22,
    }
    
    EXCLUDE_KEYWORDS = {
        'announcement': -25, 'press release': -30, 'marketing': -30,
        'product launch': -22, 'feature update': -18, 'news': -15,
        'event': -12, 'conference': -10, 'webinar': -15, 'hiring': -18,
        'culture': -12, 'opinion': -10, 'trends': -12, 'predictions': -15,
        'partnership': -18, 'acquisition': -22, 'funding': -25,
    }
    
    def __init__(self, blogs_dir="blogs", max_per_company=25):
        self.blogs_dir = Path(blogs_dir)
        self.max_per_company = max_per_company
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        # Robust session setup
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.stats = {
            'companies_processed': 0,
            'pages_crawled': 0,
            'articles_discovered': 0,
            'premium_downloaded': 0,
            'duplicates_skipped': 0,
            'errors': 0,
        }
    
    def calculate_comprehensive_score(self, title, description="", content_preview=""):
        """Calculate comprehensive system architecture score."""
        text = f"{title} {description} {content_preview}".lower()
        score = 0
        
        # Positive system keywords with enhanced weighting
        for keyword, points in self.SYSTEM_KEYWORDS.items():
            if keyword in text:
                count = text.count(keyword)
                score += points * min(count, 2)  # Cap multiplier at 2x
        
        # Negative keywords
        for keyword, penalty in self.EXCLUDE_KEYWORDS.items():
            if keyword in text:
                score += penalty
        
        # Special bonuses for exceptional content indicators
        exceptional_phrases = [
            'how we built', 'building our', 'technical deep dive', 'lessons learned',
            'scaling to', 'million users', 'billion requests', 'at scale',
            'operational transform', 'consensus algorithm', 'distributed consensus',
            'real-time collaboration', 'multiplayer systems', 'low latency',
            'high throughput', 'fault tolerance', 'system design'
        ]
        
        for phrase in exceptional_phrases:
            if phrase in text:
                score += 25
        
        # Performance/scale indicators
        if re.search(r'\d+[kmgtpz]?\s*(qps|rps|ops|requests|queries|users|connections|messages)', text):
            score += 20
            
        # Scale descriptors
        if re.search(r'(billion|million|thousand).*?(users|requests|messages|transactions|operations)', text):
            score += 18
        
        return max(0, score)
    
    def fetch_with_retries(self, url, max_retries=2):
        """Fetch URL with retries and comprehensive error handling."""
        for attempt in range(max_retries + 1):
            try:
                print(f"   🌐 Fetching: {url} (attempt {attempt + 1})")
                
                response = self.session.get(
                    url, 
                    timeout=15,
                    allow_redirects=True,
                    verify=False
                )
                
                if response.status_code == 200:
                    return BeautifulSoup(response.content, 'html.parser')
                elif response.status_code in [403, 406]:
                    print(f"   ⚠️  Access denied ({response.status_code}): {url}")
                    return None
                elif response.status_code == 404:
                    print(f"   ⚠️  Not found: {url}")
                    return None
                else:
                    print(f"   ⚠️  HTTP {response.status_code}: {url}")
                    if attempt == max_retries:
                        return None
                    
            except requests.exceptions.Timeout:
                print(f"   ⏱️  Timeout on attempt {attempt + 1}: {url}")
                if attempt == max_retries:
                    return None
            except Exception as e:
                print(f"   ❌ Error on attempt {attempt + 1}: {str(e)[:80]}")
                if attempt == max_retries:
                    self.stats['errors'] += 1
                    return None
            
            # Brief pause before retry
            time.sleep(2)
        
        return None
    
    def extract_articles_comprehensive(self, soup, base_url, company_focus):
        """Comprehensive article extraction with multiple strategies."""
        if not soup:
            return []
        
        articles = []
        found_urls = set()
        
        # Strategy 1: Standard blog selectors
        selectors_standard = [
            'article h1 a', 'article h2 a', 'article h3 a',
            '.post-title a', '.entry-title a', '.blog-post-title a',
            '.post h2 a', '.entry h2 a', '.blog-item h2 a',
        ]
        
        # Strategy 2: Modern framework selectors
        selectors_modern = [
            '[data-testid="post-preview-title"] a',  # Medium
            '.notion-page-block a',  # Notion
            '[class*="BlogPost"] h2 a',  # Various React blogs
            '[class*="Post"] h2 a', '[class*="Article"] h2 a',
        ]
        
        # Strategy 3: Generic content selectors
        selectors_generic = [
            '.content h2 a', '.article-title a', 'h1 a[href*="blog"]',
            'h2 a[href*="blog"]', 'h3 a[href*="blog"]',
            'a[href*="/post/"]', 'a[href*="/article/"]'
        ]
        
        all_selectors = selectors_standard + selectors_modern + selectors_generic
        
        for selector in all_selectors:
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
                
                # Skip if already found
                if article_url in found_urls:
                    continue
                found_urls.add(article_url)
                
                # Extract description
                description = self.extract_comprehensive_description(link)
                
                # Score the article
                score = self.calculate_comprehensive_score(title, description, company_focus)
                
                # High threshold for comprehensive collection
                if score >= 35:  # Raised threshold for quality
                    articles.append({
                        'url': article_url,
                        'title': title,
                        'description': description,
                        'score': score,
                        'focus_area': company_focus
                    })
        
        # Strategy 4: Text-based search for system articles
        system_terms = ['architecture', 'infrastructure', 'scaling', 'system', 'engineering', 'technical']
        
        for term in system_terms:
            links = soup.find_all('a', href=True, string=re.compile(term, re.IGNORECASE))
            for link in links:
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
                    score = self.calculate_comprehensive_score(title, "", company_focus)
                    
                    if score >= 30:
                        articles.append({
                            'url': article_url,
                            'title': title,
                            'description': "",
                            'score': score,
                            'focus_area': company_focus
                        })
        
        return articles
    
    def extract_comprehensive_description(self, link_element):
        """Extract description using comprehensive strategies."""
        descriptions = []
        
        # Look in multiple parent levels
        current = link_element
        for _ in range(3):  # Check up to 3 parent levels
            if current:
                desc_selectors = [
                    '.excerpt', '.summary', '.description', '.subtitle',
                    '.post-excerpt', '.entry-summary', '.post-content p',
                    'p', '.content p', '[class*="description"]'
                ]
                
                for selector in desc_selectors:
                    desc_elem = current.select_one(selector)
                    if desc_elem:
                        desc_text = desc_elem.get_text(strip=True)
                        if 30 < len(desc_text) < 600:
                            descriptions.append(desc_text)
                            break
                
                if descriptions:
                    break
                    
                current = current.find_parent()
        
        return ' '.join(descriptions[:1])
    
    def extract_content_comprehensive(self, soup):
        """Extract content using comprehensive strategies for all sites."""
        strategies = [
            # Notion-specific
            lambda s: s.select_one('.notion-page-content'),
            lambda s: s.select_one('[data-block-id]'),
            
            # Modern blog frameworks
            lambda s: s.select_one('main article'),
            lambda s: s.select_one('[role="main"]'),
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('.entry-content'),
            
            # Standard patterns
            lambda s: s.select_one('article'),
            lambda s: s.select_one('.content'),
            lambda s: s.select_one('main'),
            
            # Medium-specific
            lambda s: s.select_one('article[data-testid="storyContent"]'),
            lambda s: s.select_one('.story-content'),
            
            # React/Next.js patterns
            lambda s: s.select_one('[class*="BlogPost"]'),
            lambda s: s.select_one('[class*="Post"]'),
            lambda s: s.select_one('[class*="Article"]'),
            
            # Fallback: largest content block
            lambda s: max(
                (elem for elem in s.find_all(['div', 'section', 'article', 'main']) 
                 if len(elem.get_text(strip=True)) > 1500), 
                key=lambda x: len(x.get_text(strip=True)), 
                default=None
            )
        ]
        
        for strategy in strategies:
            try:
                content_elem = strategy(soup)
                if content_elem and len(content_elem.get_text(strip=True)) > 1500:
                    return content_elem
            except:
                continue
        
        return None
    
    def download_comprehensive_article(self, company, article_info):
        """Download and save article with comprehensive processing."""
        try:
            url = article_info['url']
            title = article_info['title']
            score = article_info['score']
            focus_area = article_info['focus_area']
            
            print(f"   📥 Downloading (score: {score}): {title[:70]}...")
            
            soup = self.fetch_with_retries(url)
            if not soup:
                return False
            
            # Extract content
            content_elem = self.extract_content_comprehensive(soup)
            
            if not content_elem:
                print(f"   ❌ Could not extract content")
                return False
            
            # Convert to markdown with optimal settings
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            h.ignore_emphasis = False
            h.single_line_break = False
            
            markdown_content = h.handle(str(content_elem))
            
            # Enhanced quality validation
            content_length = len(markdown_content.strip())
            if content_length < 1500:
                print(f"   ❌ Content too short ({content_length} chars)")
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
            filename = f"{safe_title[:75]}.md"
            filepath = company_dir / filename
            
            # Handle filename conflicts
            counter = 1
            while filepath.exists():
                base_name = safe_title[:70]
                filepath = company_dir / f"{base_name}_{counter}.md"
                counter += 1
            
            # Enhanced frontmatter
            frontmatter = f"""---
title: "{title}"
company: "{company}"
url: "{url}"
focus_area: "{focus_area}"
system_score: {score}
content_length: {content_length}
type: "comprehensive_systems_collection"
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            # Update tracking
            self.existing_hashes.add(content_hash)
            self.stats['premium_downloaded'] += 1
            
            print(f"   ✅ Saved: {title[:60]}... ({content_length} chars)")
            return True
            
        except Exception as e:
            print(f"   ❌ Error downloading {article_info.get('title', 'unknown')}: {str(e)[:100]}")
            return False
    
    def process_comprehensive_company(self, company, config):
        """Process a company comprehensively."""
        print(f"\n🏢 {company.upper()}")
        print("-" * 60)
        print(f"🎯 Focus: {config['focus']}")
        print(f"📊 Target: {self.max_per_company} premium articles")
        
        all_articles = []
        
        for url in config['urls']:
            soup = self.fetch_with_retries(url)
            self.stats['pages_crawled'] += 1
            
            if soup:
                articles = self.extract_articles_comprehensive(soup, url, config['focus'])
                all_articles.extend(articles)
                print(f"   📄 Discovered {len(articles)} system articles from {url.split('//')[-1].split('/')[0]}")
            
            # Respectful crawling pause
            time.sleep(random.uniform(3, 6))
        
        if not all_articles:
            print("   📭 No premium system articles discovered")
            return
        
        # Sort by score and take top articles
        all_articles.sort(key=lambda x: x['score'], reverse=True)
        top_articles = all_articles[:self.max_per_company]
        
        self.stats['articles_discovered'] += len(all_articles)
        print(f"   🎯 Selected {len(top_articles)} premium articles")
        if top_articles:
            print(f"   📊 Score range: {top_articles[0]['score']}-{top_articles[-1]['score']}")
        
        # Download articles
        downloaded = 0
        for article in top_articles:
            if self.download_comprehensive_article(company, article):
                downloaded += 1
                time.sleep(random.uniform(2, 4))  # Respectful downloading
            else:
                time.sleep(random.uniform(1, 2))
        
        print(f"   ✅ Successfully downloaded {downloaded}/{len(top_articles)} articles")
        self.stats['companies_processed'] += 1
        
        # Pause between companies
        time.sleep(random.uniform(5, 10))
    
    def run_comprehensive_collection(self):
        """Run the complete comprehensive collection."""
        print("🚀 COMPREHENSIVE SYSTEMS ARCHITECTURE COLLECTION")
        print("=" * 70)
        print(f"🎯 Target: ALL remaining high-value system architecture sources")
        print(f"🏢 Companies: {len(self.COMPREHENSIVE_TARGETS)}")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing articles")
        print(f"📊 Quality threshold: 35+ comprehensive score")
        print(f"📝 Max per company: {self.max_per_company}")
        print()
        print("Categories: 🔥 Real-time, 🎥 Video, 💰 Financial, 📊 Data, 🚀 Infrastructure,")
        print("           🎮 Gaming, 🛡️ Security, 🔍 Search, 📈 Observability, 🔄 Workflow")
        print()
        
        # Process all companies
        for company, config in self.COMPREHENSIVE_TARGETS.items():
            try:
                self.process_comprehensive_company(company, config)
            except KeyboardInterrupt:
                print(f"\n⚠️  Collection interrupted during {company}")
                break
            except Exception as e:
                print(f"   ❌ Error processing {company}: {str(e)[:100]}")
                continue
        
        # Final comprehensive statistics
        print("\n" + "=" * 70)
        print("🎉 COMPREHENSIVE COLLECTION COMPLETE")
        print("=" * 70)
        
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        final_count = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total articles in collection: {final_count}")
        
        if self.stats['premium_downloaded'] > 0:
            print(f"🚀 Successfully added {self.stats['premium_downloaded']} premium system architecture articles!")
            print(f"📈 Collection growth: +{self.stats['premium_downloaded']} articles")

def main():
    collector = ComprehensiveSystemsCollector(max_per_company=20)
    collector.run_comprehensive_collection()

if __name__ == "__main__":
    main()