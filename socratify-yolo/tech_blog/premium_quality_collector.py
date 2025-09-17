#!/usr/bin/env python3
"""
Premium Quality Systems Architecture Collector

Targets only the highest-quality, most prestigious sources for system architecture articles.
Focus: Quality over quantity - the absolute best remaining sources.
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

class PremiumQualityCollector:
    """Collector focusing on the highest quality system architecture sources."""
    
    # PREMIUM TIER: Highest quality sources known for exceptional system architecture content
    PREMIUM_TIER_SOURCES = {
        # 🌍 International Powerhouses (Guaranteed High Quality)
        'zalando': {
            'urls': [
                'https://engineering.zalando.com/',
                'https://engineering.zalando.com/tags/architecture/',
                'https://engineering.zalando.com/tags/microservices/',
            ],
            'focus': 'microservices architecture, e-commerce scaling, European tech leadership',
            'known_for': 'Microservices pioneers, detailed technical posts'
        },
        'booking': {
            'urls': [
                'https://blog.booking.com/',
                'https://medium.com/booking-com-development',
                'https://blog.booking.com/tagged/architecture',
            ],
            'focus': 'A/B testing at scale, travel systems, distributed architecture',
            'known_for': 'Scaling to handle millions of bookings, A/B testing expertise'
        },
        'deliveroo': {
            'urls': [
                'https://deliveroo.engineering/',
                'https://deliveroo.engineering/categories/architecture/',
                'https://medium.com/deliveroo-engineering',
            ],
            'focus': 'logistics systems, real-time delivery, microservices',
            'known_for': 'Real-time logistics, food delivery scaling challenges'
        },
        
        # 🏦 Premium Financial Services (Ultra High Quality)
        'wise': {
            'urls': [
                'https://medium.com/wise-engineering',
                'https://wise.com/us/blog/category/engineering',
            ],
            'focus': 'international payments, financial infrastructure, regulatory compliance',
            'known_for': 'International money transfers, financial system architecture'
        },
        'monzo': {
            'urls': [
                'https://monzo.com/blog/technology',
                'https://medium.com/monzo-bank',
            ],
            'focus': 'banking infrastructure, real-time payments, financial systems',
            'known_for': 'Modern banking architecture, real-time financial processing'
        },
        
        # 🎮 Premium Gaming (Known for Excellent Technical Posts)  
        'mojang': {
            'urls': [
                'https://www.minecraft.net/en-us/article/category/insider',
                'https://help.minecraft.net/hc/en-us/sections/12618486543501',
            ],
            'focus': 'game server architecture, massive multiplayer systems, Minecraft scaling',
            'known_for': 'Minecraft server architecture, handling millions of concurrent players'
        },
        'ea': {
            'urls': [
                'https://www.ea.com/news/category/technology',
                'https://technology.ea.com/',
            ],
            'focus': 'game infrastructure, multiplayer systems, sports game architecture',
            'known_for': 'FIFA/sports game infrastructure, massive multiplayer systems'
        },
        
        # 🔬 Premium Open Source (High-Quality Technical Content)
        'postgresql': {
            'urls': [
                'https://www.postgresql.org/about/news/',
                'https://wiki.postgresql.org/wiki/Development_information',
                'https://www.postgresql.org/docs/devel/',
            ],
            'focus': 'database internals, storage engines, query optimization',
            'known_for': 'Deep technical database architecture, storage systems'
        },
        'mysql': {
            'urls': [
                'https://dev.mysql.com/blog-archive/',
                'https://blogs.oracle.com/mysql/',
                'https://mysqlhighavailability.com/',
            ],
            'focus': 'storage engines, replication, high availability',
            'known_for': 'Database replication, storage architecture, HA systems'
        },
        
        # 🏗️ Premium Infrastructure (Top-Tier Technical Content)
        'cloudformation': {
            'urls': [
                'https://aws.amazon.com/blogs/devops/',
                'https://aws.amazon.com/architecture/',
                'https://aws.amazon.com/blogs/architecture/',
            ],
            'focus': 'cloud architecture patterns, infrastructure as code, AWS systems',
            'known_for': 'Cloud architecture patterns, real customer use cases'
        },
        'kubernetes': {
            'urls': [
                'https://kubernetes.io/blog/',
                'https://kubernetes.io/case-studies/',
                'https://github.com/kubernetes/enhancements',
            ],
            'focus': 'container orchestration, distributed systems, cloud native',
            'known_for': 'Container orchestration architecture, cloud-native systems'
        },
        
        # 📊 Premium Data Infrastructure (Exceptional Technical Quality)
        'clickhouse': {
            'urls': [
                'https://clickhouse.com/blog',
                'https://clickhouse.com/blog/category/technical',
                'https://clickhouse.com/docs/en/development/',
            ],
            'focus': 'columnar database architecture, analytics systems, performance optimization',
            'known_for': 'High-performance analytics, columnar storage architecture'
        },
        'scylladb': {
            'urls': [
                'https://www.scylladb.com/blog/',
                'https://www.scylladb.com/blog/category/engineering/',
                'https://www.scylladb.com/users/',
            ],
            'focus': 'high-performance NoSQL, C++ optimization, low-latency systems',
            'known_for': 'Ultra-high performance NoSQL, low-latency architecture'
        },
        
        # 🎯 Premium Specialized (Known for Deep Technical Content)
        'hashicorp': {
            'urls': [
                'https://www.hashicorp.com/blog',
                'https://www.hashicorp.com/blog/category/engineering',
                'https://learn.hashicorp.com/',
            ],
            'focus': 'infrastructure tooling, service discovery, secrets management',
            'known_for': 'Infrastructure automation, service mesh, secrets management'
        },
        'elastic': {
            'urls': [
                'https://www.elastic.co/blog/',
                'https://www.elastic.co/blog/category/engineering',
                'https://www.elastic.co/guide/en/elasticsearch/guide/current/',
            ],
            'focus': 'distributed search, log analytics, observability systems',
            'known_for': 'Distributed search architecture, real-time analytics'
        },
    }
    
    # Ultra-high quality keywords for premium filtering
    PREMIUM_KEYWORDS = {
        # Core system design (highest value)
        'system architecture': 50, 'distributed systems': 50, 'microservices architecture': 45,
        'scalability patterns': 45, 'performance optimization': 40, 'high availability': 40,
        
        # Implementation excellence
        'how we built': 45, 'technical deep dive': 45, 'lessons learned': 40,
        'engineering at scale': 40, 'architecture decisions': 40, 'design patterns': 35,
        
        # Specific technical domains
        'database internals': 40, 'storage systems': 35, 'query optimization': 35,
        'real-time systems': 40, 'event-driven architecture': 35, 'stream processing': 35,
        
        # Advanced concepts
        'consensus algorithms': 45, 'distributed consensus': 45, 'replication': 35,
        'sharding strategies': 35, 'load balancing': 30, 'caching strategies': 30,
        
        # Scale indicators
        'million users': 35, 'billion requests': 40, 'petabyte scale': 40,
        'high throughput': 35, 'low latency': 35, 'fault tolerance': 35,
        
        # Quality content indicators
        'case study': 35, 'postmortem': 40, 'technical analysis': 35,
        'performance benchmarks': 35, 'optimization techniques': 35,
    }
    
    EXCLUDE_KEYWORDS = {
        'announcement': -30, 'press release': -35, 'marketing': -35,
        'product launch': -25, 'feature update': -20, 'news': -20,
        'hiring': -25, 'culture': -20, 'opinion': -15, 'trends': -15,
        'beginner': -25, 'tutorial': -20, 'getting started': -20,
    }
    
    def __init__(self, blogs_dir="blogs", max_per_source=12):
        self.blogs_dir = Path(blogs_dir)
        self.max_per_source = max_per_source
        self.deduplicator = BlogDeduplicator(blogs_dir)
        self.existing_hashes = self.deduplicator.get_existing_article_hashes()
        
        # Premium session configuration
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
        self.stats = {
            'sources_processed': 0,
            'pages_crawled': 0,
            'articles_discovered': 0,
            'premium_downloaded': 0,
            'duplicates_skipped': 0,
            'low_quality_filtered': 0,
            'errors': 0,
        }
    
    def calculate_premium_score(self, title, description="", preview=""):
        """Calculate premium quality score with high standards."""
        text = f"{title} {description} {preview}".lower()
        score = 0
        
        # Premium keyword scoring with higher weights
        for keyword, points in self.PREMIUM_KEYWORDS.items():
            if keyword in text:
                count = text.count(keyword)
                score += points * min(count, 2)  # Cap at 2x multiplier
        
        # Exclusion penalties
        for keyword, penalty in self.EXCLUDE_KEYWORDS.items():
            if keyword in text:
                score += penalty
        
        # Premium content indicators (bonus scoring)
        premium_indicators = [
            'technical deep dive', 'architecture decisions', 'lessons learned',
            'how we built', 'engineering at scale', 'system design',
            'performance optimization', 'scalability patterns', 'case study',
            'distributed systems', 'microservices', 'real-time systems'
        ]
        
        for indicator in premium_indicators:
            if indicator in text:
                score += 30  # High bonus for premium indicators
        
        # Scale and performance indicators
        if re.search(r'\d+[kmgtpz]?\s*(million|billion)\s*(users|requests|operations|queries)', text):
            score += 35  # Major scale indicators
            
        if re.search(r'\d+[kmgt]?\s*(qps|rps|tps|ops|requests/sec)', text):
            score += 30  # Performance metrics
        
        return max(0, score)
    
    def safe_premium_fetch(self, url, max_retries=2):
        """Premium fetch with robust error handling."""
        for attempt in range(max_retries + 1):
            try:
                print(f"   🌐 Fetching: {url.split('//')[-1].split('/')[0]} (attempt {attempt + 1})")
                
                response = self.session.get(
                    url, 
                    timeout=12,
                    allow_redirects=True,
                    verify=False  # Some sites have SSL issues
                )
                
                if response.status_code == 200:
                    return BeautifulSoup(response.content, 'html.parser')
                elif response.status_code in [403, 406, 429]:
                    print(f"   ⚠️  Access restricted ({response.status_code})")
                    return None
                elif response.status_code == 404:
                    print(f"   ⚠️  Not found")
                    return None
                else:
                    print(f"   ⚠️  HTTP {response.status_code}")
                    if attempt == max_retries:
                        return None
                    
            except requests.exceptions.Timeout:
                print(f"   ⏱️  Timeout on attempt {attempt + 1}")
                if attempt < max_retries:
                    time.sleep(3)  # Longer pause on timeout
            except Exception as e:
                print(f"   ❌ Error on attempt {attempt + 1}: {str(e)[:60]}")
                if attempt == max_retries:
                    self.stats['errors'] += 1
                    return None
            
            if attempt < max_retries:
                time.sleep(2)  # Brief pause between retries
        
        return None
    
    def extract_premium_articles(self, soup, base_url, source_focus):
        """Extract articles using premium quality filtering."""
        if not soup:
            return []
        
        articles = []
        found_urls = set()
        
        # Premium article selectors (comprehensive)
        premium_selectors = [
            # Standard blog patterns
            'article h1 a', 'article h2 a', 'article h3 a',
            '.post-title a', '.entry-title a', '.blog-post-title a',
            
            # Engineering blog patterns
            '.engineering-post a', '.tech-post a', '.technical-article a',
            
            # Medium and modern platforms
            '[data-testid="post-preview-title"] a',
            '.story-title a', '.post-preview-title a',
            
            # Generic content patterns
            '.content h2 a', '.article-title a', '.post h2 a',
            'h1 a[href*="blog"]', 'h2 a[href*="blog"]',
            
            # Specialized patterns for technical sites
            '.doc-title a', '.guide-title a', '.tutorial-title a'
        ]
        
        for selector in premium_selectors:
            for link in soup.select(selector):
                href = link.get('href')
                title = link.get_text(strip=True)
                
                if not href or not title or len(title) < 10:
                    continue
                
                # Create absolute URL
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
                
                # Extract rich description
                description = self.extract_premium_description(link)
                
                # Calculate premium score
                score = self.calculate_premium_score(title, description, source_focus)
                
                # Ultra-high quality threshold
                if score >= 50:  # Very high bar for premium content
                    articles.append({
                        'url': article_url,
                        'title': title,
                        'description': description,
                        'score': score,
                        'source_focus': source_focus
                    })
                elif score >= 30:  # Medium quality still tracked
                    self.stats['low_quality_filtered'] += 1
        
        return articles
    
    def extract_premium_description(self, link_element):
        """Extract rich description for premium scoring."""
        descriptions = []
        
        # Look through multiple parent levels for description
        current = link_element
        for level in range(4):  # Check up to 4 parent levels
            if current:
                desc_selectors = [
                    '.excerpt', '.summary', '.description', '.subtitle',
                    '.post-excerpt', '.entry-summary', '.lead',
                    '.abstract', '.intro', 'p', '.content p'
                ]
                
                for selector in desc_selectors:
                    desc_elem = current.select_one(selector)
                    if desc_elem:
                        desc_text = desc_elem.get_text(strip=True)
                        if 40 < len(desc_text) < 800:  # Good description length
                            descriptions.append(desc_text)
                            break
                
                if descriptions:
                    break
                    
                current = current.find_parent()
        
        return ' '.join(descriptions[:2])  # Combine up to 2 descriptions
    
    def extract_premium_content(self, soup):
        """Extract content using premium strategies."""
        strategies = [
            # Engineering blog patterns
            lambda s: s.select_one('article .content'),
            lambda s: s.select_one('.post-content'),
            lambda s: s.select_one('.entry-content'),
            
            # Modern framework patterns
            lambda s: s.select_one('main article'),
            lambda s: s.select_one('[role="main"]'),
            lambda s: s.select_one('article'),
            lambda s: s.select_one('main'),
            
            # Medium and blog platforms
            lambda s: s.select_one('.story-content'),
            lambda s: s.select_one('[data-testid="storyContent"]'),
            
            # Documentation patterns
            lambda s: s.select_one('.doc-content'),
            lambda s: s.select_one('.guide-content'),
            
            # Generic patterns
            lambda s: s.select_one('.content'),
            lambda s: s.select_one('#content'),
            
            # Fallback: largest high-quality content block
            lambda s: max(
                (elem for elem in s.find_all(['div', 'section', 'article']) 
                 if len(elem.get_text(strip=True)) > 2000), 
                key=lambda x: len(x.get_text(strip=True)), 
                default=None
            )
        ]
        
        for strategy in strategies:
            try:
                content_elem = strategy(soup)
                if content_elem and len(content_elem.get_text(strip=True)) > 2000:
                    return content_elem
            except:
                continue
        
        return None
    
    def download_premium_article(self, source, article_info):
        """Download premium article with high quality standards."""
        try:
            url = article_info['url']
            title = article_info['title']
            score = article_info['score']
            source_focus = article_info['source_focus']
            
            print(f"   📥 Premium (score: {score}): {title[:75]}...")
            
            soup = self.safe_premium_fetch(url)
            if not soup:
                return False
            
            # Extract high-quality content
            content_elem = self.extract_premium_content(soup)
            
            if not content_elem:
                print(f"   ❌ Could not extract premium content")
                return False
            
            # Convert to markdown with premium settings
            h = html2text.HTML2Text()
            h.ignore_links = False
            h.ignore_images = False
            h.body_width = 0
            h.ignore_emphasis = False
            h.single_line_break = False
            h.wrap_links = False
            
            markdown_content = h.handle(str(content_elem))
            
            # Premium quality validation
            content_length = len(markdown_content.strip())
            if content_length < 2000:  # High minimum for premium content
                print(f"   ❌ Content too short for premium ({content_length} chars)")
                return False
            
            # Check for duplicate
            content_hash = self.deduplicator.get_content_hash(markdown_content)
            if content_hash in self.existing_hashes:
                print(f"   ⚠️  Duplicate detected, skipping")
                self.stats['duplicates_skipped'] += 1
                return False
            
            # Create source directory
            source_dir = self.blogs_dir / source
            source_dir.mkdir(parents=True, exist_ok=True)
            
            # Create premium filename
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            filename = f"{safe_title[:75]}.md"
            filepath = source_dir / filename
            
            # Handle filename conflicts
            counter = 1
            while filepath.exists():
                base_name = safe_title[:70]
                filepath = source_dir / f"{base_name}_{counter}.md"
                counter += 1
            
            # Premium frontmatter
            frontmatter = f"""---
title: "{title}"
source: "{source}"
url: "{url}"
focus_area: "{source_focus}"
premium_score: {score}
content_length: {content_length}
type: "premium_systems_architecture"
premium: true
date: "{time.strftime('%Y-%m-%d')}"
---

"""
            
            # Write premium content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter + markdown_content)
            
            # Update tracking
            self.existing_hashes.add(content_hash)
            self.stats['premium_downloaded'] += 1
            
            print(f"   ✅ Saved premium: {title[:60]}... ({content_length} chars)")
            return True
            
        except Exception as e:
            print(f"   ❌ Error downloading premium article: {str(e)[:100]}")
            return False
    
    def process_premium_source(self, source, config):
        """Process a premium source with high quality standards."""
        print(f"\n🏆 {source.upper()}")
        print("-" * 70)
        print(f"🎯 Focus: {config['focus']}")
        print(f"⭐ Known for: {config['known_for']}")
        print(f"📊 Target: {self.max_per_source} premium articles (score ≥50)")
        
        all_articles = []
        
        for url in config['urls'][:3]:  # Limit URLs per source for quality
            soup = self.safe_premium_fetch(url)
            self.stats['pages_crawled'] += 1
            
            if soup:
                articles = self.extract_premium_articles(soup, url, config['focus'])
                all_articles.extend(articles)
                print(f"   📄 Discovered {len(articles)} premium articles")
            
            # Respectful crawling for premium sources
            time.sleep(random.uniform(4, 7))
        
        if not all_articles:
            print("   📭 No premium articles met quality threshold")
            return
        
        # Sort by premium score and take top articles
        all_articles.sort(key=lambda x: x['score'], reverse=True)
        top_articles = all_articles[:self.max_per_source]
        
        self.stats['articles_discovered'] += len(all_articles)
        print(f"   🎯 Selected {len(top_articles)} highest-scoring articles")
        if top_articles:
            scores = [a['score'] for a in top_articles]
            print(f"   📊 Premium scores: {max(scores)}-{min(scores)}")
        
        # Download premium articles
        downloaded = 0
        for article in top_articles:
            if self.download_premium_article(source, article):
                downloaded += 1
                time.sleep(random.uniform(3, 5))  # Respectful premium downloading
            else:
                time.sleep(random.uniform(1, 2))
        
        print(f"   ✅ Successfully downloaded {downloaded}/{len(top_articles)} premium articles")
        self.stats['sources_processed'] += 1
        
        # Extended pause between premium sources
        time.sleep(random.uniform(7, 12))
    
    def run_premium_collection(self):
        """Run the premium quality collection."""
        print("🏆 PREMIUM QUALITY SYSTEMS ARCHITECTURE COLLECTION")
        print("=" * 80)
        print("🎯 Focus: QUALITY OVER QUANTITY - Only the absolute best")
        print(f"⭐ Premium sources: {len(self.PREMIUM_TIER_SOURCES)}")
        print(f"🔄 Duplicate prevention: {len(self.existing_hashes)} existing articles")
        print(f"📊 Quality threshold: 50+ premium score (ultra-high bar)")
        print(f"📝 Max per source: {self.max_per_source}")
        print()
        print("Categories: 🌍 International Powerhouses, 🏦 Premium Financial,")
        print("           🎮 Gaming Excellence, 🔬 Premium Open Source,")
        print("           🏗️ Infrastructure Leaders, 📊 Data Systems Experts")
        print()
        
        # Process premium sources
        for source, config in self.PREMIUM_TIER_SOURCES.items():
            try:
                self.process_premium_source(source, config)
            except KeyboardInterrupt:
                print(f"\n⚠️  Premium collection interrupted during {source}")
                break
            except Exception as e:
                print(f"   ❌ Error processing premium source {source}: {str(e)[:100]}")
                continue
        
        # Premium collection summary
        print("\n" + "=" * 80)
        print("🏆 PREMIUM QUALITY COLLECTION COMPLETE")
        print("=" * 80)
        
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        final_count = len(list(self.blogs_dir.rglob('*.md')))
        print(f"\n📚 Total articles in collection: {final_count}")
        
        if self.stats['premium_downloaded'] > 0:
            print(f"🏆 Successfully added {self.stats['premium_downloaded']} PREMIUM system architecture articles!")
            print(f"⭐ These represent the highest quality technical content available")
            print(f"📈 Quality-focused growth: +{self.stats['premium_downloaded']} ultra-premium articles")

def main():
    collector = PremiumQualityCollector(max_per_source=10)
    collector.run_premium_collection()

if __name__ == "__main__":
    main()