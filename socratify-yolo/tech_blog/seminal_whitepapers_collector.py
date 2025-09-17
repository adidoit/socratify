#!/usr/bin/env python3
"""
Seminal Whitepapers Collector

Collects foundational computer science and system architecture whitepapers
that provide the theoretical foundations for modern distributed systems.
"""

import requests
import time
from pathlib import Path
import hashlib
import re
from bs4 import BeautifulSoup
import html2text
from urllib.parse import urlparse

class SeminalWhitepapersCollector:
    """Collector for seminal system architecture whitepapers."""
    
    # Seminal papers that are freely available online
    SEMINAL_PAPERS = {
        # 🌐 Distributed Systems Foundations
        'distributed_systems': [
            {
                'title': 'Time, Clocks, and the Ordering of Events in a Distributed System',
                'author': 'Leslie Lamport',
                'url': 'https://lamport.azurewebsites.net/pubs/time-clocks.pdf',
                'year': 1978,
                'significance': 'Foundational paper on logical clocks and causal ordering'
            },
            {
                'title': 'The Part-Time Parliament (Paxos)',
                'author': 'Leslie Lamport', 
                'url': 'https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf',
                'year': 1998,
                'significance': 'The original Paxos consensus algorithm paper'
            },
            {
                'title': 'Paxos Made Simple',
                'author': 'Leslie Lamport',
                'url': 'https://lamport.azurewebsites.net/pubs/paxos-simple.pdf', 
                'year': 2001,
                'significance': 'Simplified explanation of Paxos consensus'
            },
            {
                'title': 'In Search of an Understandable Consensus Algorithm (Raft)',
                'author': 'Diego Ongaro, John Ousterhout',
                'url': 'https://raft.github.io/raft.pdf',
                'year': 2014,
                'significance': 'Raft consensus algorithm, designed for understandability'
            },
            {
                'title': 'Impossibility of Distributed Consensus with One Faulty Process (FLP)',
                'author': 'Fischer, Lynch, Paterson',
                'url': 'https://groups.csail.mit.edu/tds/papers/Lynch/jacm85.pdf',
                'year': 1985,
                'significance': 'Fundamental impossibility result in distributed computing'
            },
        ],
        
        # 💾 Database Systems Foundations  
        'database_systems': [
            {
                'title': 'ACID Properties of Transactions',
                'author': 'Jim Gray, Andreas Reuter',
                'url': 'https://web.stanford.edu/class/cs340v/papers/recovery.pdf',
                'year': 1983,
                'significance': 'Foundational paper defining ACID properties'
            },
            {
                'title': 'Brewer\'s Conjecture and the Feasibility of Consistent Available Partition-tolerant Web Services',
                'author': 'Seth Gilbert, Nancy Lynch',
                'url': 'https://users.ece.cmu.edu/~adrian/731-sp04/readings/GL-cap.pdf',
                'year': 2002,
                'significance': 'Formal proof of the CAP theorem'
            },
            {
                'title': 'Multiversion Concurrency Control - Theory and Algorithms', 
                'author': 'Bernstein, Goodman',
                'url': 'https://courses.cs.washington.edu/courses/cse544/11wi/papers/bernstein-1983.pdf',
                'year': 1983,
                'significance': 'Foundational MVCC paper for database concurrency'
            },
        ],
        
        # 🏗️ Google Systems Papers (Publicly Available)
        'google_systems': [
            {
                'title': 'The Google File System',
                'author': 'Sanjay Ghemawat, Howard Gobioff, Shun-Tak Leung',
                'url': 'https://static.googleusercontent.com/media/research.google.com/en//archive/gfs-sosp2003.pdf',
                'year': 2003,
                'significance': 'Foundational distributed file system that influenced Hadoop HDFS'
            },
            {
                'title': 'MapReduce: Simplified Data Processing on Large Clusters',
                'author': 'Jeffrey Dean, Sanjay Ghemawat',
                'url': 'https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf',
                'year': 2004,
                'significance': 'Paradigm that revolutionized big data processing'
            },
            {
                'title': 'Bigtable: A Distributed Storage System for Structured Data',
                'author': 'Fay Chang, Jeffrey Dean, et al.',
                'url': 'https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf',
                'year': 2006,
                'significance': 'Wide-column database that influenced HBase and Cassandra'
            },
            {
                'title': 'Spanner: Google\'s Globally-Distributed Database',
                'author': 'James C. Corbett, Jeffrey Dean, et al.',
                'url': 'https://static.googleusercontent.com/media/research.google.com/en//archive/spanner-osdi2012.pdf',
                'year': 2012,
                'significance': 'Global-scale consistent database with external consistency'
            },
            {
                'title': 'Dremel: Interactive Analysis of Web-Scale Datasets',
                'author': 'Sergey Melnik, Andrey Gubarev, et al.',
                'url': 'https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36632.pdf',
                'year': 2010,
                'significance': 'Columnar storage and query system that inspired BigQuery'
            },
        ],
        
        # 🏪 Amazon & Industry Systems
        'industry_systems': [
            {
                'title': 'Dynamo: Amazon\'s Highly Available Key-value Store',
                'author': 'DeCandia, Hastorun, Jampani, et al.',
                'url': 'https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf',
                'year': 2007,
                'significance': 'Eventually consistent distributed hash table'
            },
            {
                'title': 'Finding a Needle in Haystack: Facebook\'s Photo Storage',
                'author': 'Doug Beaver, Sanjeev Kumar, et al.',
                'url': 'https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Beaver.pdf',
                'year': 2010,
                'significance': 'Efficient storage system for billions of photos'
            },
        ],
        
        # 🔄 Streaming & Real-time Systems
        'streaming_systems': [
            {
                'title': 'The Log: What every software engineer should know about real-time data\'s unifying abstraction',
                'author': 'Jay Kreps',
                'url': 'https://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying',
                'year': 2013,
                'significance': 'Foundational concepts behind Kafka and stream processing'
            },
        ],
        
        # 🔐 Security & Cryptography Foundations
        'security_foundations': [
            {
                'title': 'New Directions in Cryptography',
                'author': 'Diffie, Hellman',
                'url': 'https://ee.stanford.edu/~hellman/publications/24.pdf',
                'year': 1976,
                'significance': 'Introduced public-key cryptography concept'
            },
        ],
        
        # 📊 Analytics & Data Processing
        'data_processing': [
            {
                'title': 'Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing',
                'author': 'Matei Zaharia, et al.',
                'url': 'https://www.usenix.org/system/files/conference/nsdi12/nsdi12-final138.pdf',
                'year': 2012,
                'significance': 'Foundation of Apache Spark'
            },
        ]
    }
    
    def __init__(self, base_dir="whitepapers"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(exist_ok=True)
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        })
        
        self.stats = {'attempted': 0, 'downloaded': 0, 'errors': 0, 'already_exists': 0}
    
    def download_pdf(self, category, paper_info):
        """Download a PDF whitepaper."""
        try:
            self.stats['attempted'] += 1
            title = paper_info['title']
            url = paper_info['url']
            author = paper_info['author']
            year = paper_info['year']
            significance = paper_info['significance']
            
            print(f"   📄 Downloading: {title[:60]}...")
            print(f"      Author: {author} ({year})")
            
            # Create category directory
            category_dir = self.base_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Create safe filename
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'[-\s]+', '_', safe_title)
            
            # Check if it's a PDF URL or needs processing
            if url.endswith('.pdf'):
                # Direct PDF download
                pdf_filename = f"{safe_title[:60]}_{year}.pdf"
                pdf_path = category_dir / pdf_filename
                
                if pdf_path.exists():
                    print(f"      ⚠️  Already exists: {pdf_filename}")
                    self.stats['already_exists'] += 1
                    return True
                
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                
                # Save PDF
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)
                
                # Create markdown metadata file
                md_filename = f"{safe_title[:60]}_{year}.md"
                md_path = category_dir / md_filename
                
                metadata = f"""# {title}

**Author**: {author}  
**Year**: {year}  
**Category**: {category.replace('_', ' ').title()}  
**PDF**: {pdf_filename}  

## Significance
{significance}

## Download Information
- **Original URL**: {url}
- **Downloaded**: {time.strftime('%Y-%m-%d %H:%M:%S')}
- **File Size**: {len(response.content)} bytes

## Abstract/Summary
This seminal paper represents foundational knowledge in {category.replace('_', ' ')} and is essential reading for understanding modern distributed systems architecture.

---
*This whitepaper is part of a curated collection of seminal system architecture papers.*
"""
                
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(metadata)
                
            else:
                # HTML page - extract content
                response = self.session.get(url, timeout=15)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try to find PDF link or extract content
                pdf_links = soup.find_all('a', href=re.compile(r'\.pdf$', re.IGNORECASE))
                
                if pdf_links:
                    # Found PDF link, download it
                    pdf_url = pdf_links[0]['href']
                    if not pdf_url.startswith('http'):
                        from urllib.parse import urljoin
                        pdf_url = urljoin(url, pdf_url)
                    
                    # Recursive call with PDF URL
                    paper_info_pdf = paper_info.copy()
                    paper_info_pdf['url'] = pdf_url
                    return self.download_pdf(category, paper_info_pdf)
                
                else:
                    # Extract HTML content and convert to markdown
                    content_elem = self.extract_paper_content(soup)
                    
                    if content_elem:
                        h = html2text.HTML2Text()
                        h.ignore_links = False
                        h.body_width = 0
                        
                        markdown_content = h.handle(str(content_elem))
                        
                        md_filename = f"{safe_title[:60]}_{year}.md"
                        md_path = category_dir / md_filename
                        
                        if md_path.exists():
                            print(f"      ⚠️  Already exists: {md_filename}")
                            self.stats['already_exists'] += 1
                            return True
                        
                        full_content = f"""# {title}

**Author**: {author}  
**Year**: {year}  
**Category**: {category.replace('_', ' ').title()}  
**Source**: {url}  

## Significance
{significance}

---

{markdown_content}

---
*Downloaded from: {url}*  
*Part of seminal system architecture papers collection*
"""
                        
                        with open(md_path, 'w', encoding='utf-8') as f:
                            f.write(full_content)
                    else:
                        print(f"      ❌ Could not extract content from HTML")
                        self.stats['errors'] += 1
                        return False
            
            self.stats['downloaded'] += 1
            print(f"      ✅ Successfully downloaded")
            return True
            
        except Exception as e:
            print(f"      ❌ Error: {str(e)[:80]}")
            self.stats['errors'] += 1
            return False
    
    def extract_paper_content(self, soup):
        """Extract paper content from HTML."""
        # Try various selectors for academic paper content
        selectors = [
            'article', '.paper-content', '.content', '.post-content',
            '.entry-content', 'main', '#content', '.paper', '.document'
        ]
        
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem and len(elem.get_text(strip=True)) > 1000:
                return elem
        
        # Fallback: look for largest content block
        for div in soup.find_all(['div', 'section']):
            if len(div.get_text(strip=True)) > 2000:
                return div
        
        return None
    
    def collect_seminal_papers(self):
        """Collect all seminal whitepapers."""
        print("📚 SEMINAL SYSTEM ARCHITECTURE WHITEPAPERS COLLECTION")
        print("=" * 70)
        print("🎯 Focus: Foundational papers that shaped distributed systems")
        print("📁 Output: whitepapers/ directory with PDFs and metadata")
        print(f"📊 Total papers: {sum(len(papers) for papers in self.SEMINAL_PAPERS.values())}")
        print()
        print("Categories: 🌐 Distributed Systems, 💾 Database Systems,")
        print("           🏗️ Google Systems, 🏪 Industry Systems,")
        print("           🔄 Streaming Systems, 🔐 Security, 📊 Data Processing")
        print()
        
        total_papers = 0
        
        for category, papers in self.SEMINAL_PAPERS.items():
            print(f"\n📚 {category.upper().replace('_', ' ')}")
            print("-" * 60)
            
            for paper in papers:
                self.download_pdf(category, paper)
                total_papers += 1
                time.sleep(2)  # Respectful downloading
            
            print(f"   📊 Processed {len(papers)} papers in {category}")
            time.sleep(3)  # Pause between categories
        
        # Final summary
        print(f"\n📚 SEMINAL PAPERS COLLECTION COMPLETE")
        print("=" * 60)
        for key, value in self.stats.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        total_files = len(list(self.base_dir.rglob('*.*')))
        print(f"\n📁 Total files in whitepapers/: {total_files}")
        
        if self.stats['downloaded'] > 0:
            print(f"📚 Successfully collected {self.stats['downloaded']} seminal papers!")
            print("🎓 These represent the foundational knowledge of distributed systems")
            print("🔗 Perfect complement to the practical blog articles collection")

def main():
    collector = SeminalWhitepapersCollector()
    collector.collect_seminal_papers()

if __name__ == "__main__":
    main()