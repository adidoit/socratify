#!/usr/bin/env python3
"""
Blog Deduplication Tool

Removes duplicate articles and improves markdown quality.
Prevents future duplicates by checking existing content before download.
"""

import os
import re
import hashlib
from pathlib import Path
from collections import defaultdict


class BlogDeduplicator:
    """Remove duplicates and improve markdown quality."""
    
    def __init__(self, blogs_dir="blogs"):
        self.blogs_dir = Path(blogs_dir)
        self.stats = {
            'total_files': 0,
            'duplicates_removed': 0,
            'encoding_fixed': 0,
            'files_cleaned': 0
        }
    
    def get_content_hash(self, content):
        """Generate hash of article content for duplicate detection."""
        # Remove frontmatter and whitespace variations for comparison
        content_lines = content.split('\n')
        main_content = []
        in_frontmatter = False
        
        for line in content_lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter:
                # Normalize whitespace for comparison
                normalized_line = ' '.join(line.split())
                if normalized_line:
                    main_content.append(normalized_line)
        
        # Create hash of main content
        content_text = '\n'.join(main_content)
        return hashlib.md5(content_text.encode('utf-8')).hexdigest()
    
    def extract_title_from_content(self, content):
        """Extract clean title from article content."""
        lines = content.split('\n')
        
        # Try to get title from frontmatter
        in_frontmatter = False
        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if in_frontmatter and line.startswith('title:'):
                title = line.replace('title:', '').strip().strip('"')
                return title
        
        # Fallback: look for first H1
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        
        return "Unknown Title"
    
    def fix_encoding_issues(self, content):
        """Fix character encoding issues in content."""
        # Fix common encoding issues
        fixes = [
            ('â\x80\x99', "'"),  # Right single quotation mark
            ('â\x80\x9c', '"'),  # Left double quotation mark  
            ('â\x80\x9d', '"'),  # Right double quotation mark
            ('â\x80\x94', '—'),  # Em dash
            ('â\x80\x93', '–'),  # En dash
            ('â\x80¦', '...'),  # Horizontal ellipsis
            ('Ã¡', 'á'), ('Ã©', 'é'), ('Ã­', 'í'), ('Ã³', 'ó'), ('Ãº', 'ú'),  # Accented chars
            ('\ufffd', ''),  # Replace replacement characters
        ]
        
        fixed_content = content
        changes_made = 0
        
        for old, new in fixes:
            if old in fixed_content:
                fixed_content = fixed_content.replace(old, new)
                changes_made += 1
        
        # Fix multiple newlines
        fixed_content = re.sub(r'\n\s*\n\s*\n+', '\n\n', fixed_content)
        
        return fixed_content, changes_made > 0
    
    def clean_markdown_content(self, content):
        """Clean and improve markdown content quality."""
        lines = content.split('\n')
        cleaned_lines = []
        in_frontmatter = False
        
        for line in lines:
            # Handle frontmatter
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                cleaned_lines.append(line)
                continue
                
            if in_frontmatter:
                cleaned_lines.append(line)
                continue
            
            # Clean main content
            cleaned_line = line
            
            # Remove excessive whitespace but preserve code blocks
            if not line.startswith('    ') and not line.startswith('\t'):
                cleaned_line = ' '.join(line.split())
            
            # Fix markdown formatting issues
            cleaned_line = re.sub(r'\*\*\s+', '**', cleaned_line)  # Fix bold formatting
            cleaned_line = re.sub(r'\s+\*\*', '**', cleaned_line)
            cleaned_line = re.sub(r'`\s+', '`', cleaned_line)      # Fix code formatting
            cleaned_line = re.sub(r'\s+`', '`', cleaned_line)
            
            cleaned_lines.append(cleaned_line)
        
        return '\n'.join(cleaned_lines)
    
    def find_duplicates(self):
        """Find duplicate articles by content hash."""
        print("🔍 Scanning for duplicate articles...")
        
        content_hashes = defaultdict(list)
        title_hashes = defaultdict(list)
        
        for company_dir in self.blogs_dir.iterdir():
            if not company_dir.is_dir():
                continue
                
            for md_file in company_dir.glob('*.md'):
                self.stats['total_files'] += 1
                
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    content_hash = self.get_content_hash(content)
                    content_hashes[content_hash].append(md_file)
                    
                    # Also check for title similarity
                    title = self.extract_title_from_content(content)
                    title_key = re.sub(r'[^\w\s]', '', title.lower())
                    title_key = ' '.join(title_key.split())
                    title_hashes[title_key].append(md_file)
                    
                except Exception as e:
                    print(f"   ❌ Error reading {md_file}: {e}")
        
        # Find duplicates
        duplicates = []
        
        # Content-based duplicates
        for content_hash, files in content_hashes.items():
            if len(files) > 1:
                duplicates.extend(files[1:])  # Keep first, remove rest
        
        # Title-based duplicates (for similar articles)
        for title_key, files in title_hashes.items():
            if len(files) > 1:
                # Only add if not already in content duplicates
                for file in files[1:]:
                    if file not in duplicates:
                        duplicates.append(file)
        
        return duplicates
    
    def remove_duplicates(self):
        """Remove duplicate articles."""
        duplicates = self.find_duplicates()
        
        if not duplicates:
            print("✅ No duplicates found!")
            return
        
        print(f"🗑️  Found {len(duplicates)} duplicate articles:")
        
        for duplicate_file in duplicates:
            try:
                print(f"   🗑️  Removing: {duplicate_file}")
                duplicate_file.unlink()
                self.stats['duplicates_removed'] += 1
            except Exception as e:
                print(f"   ❌ Error removing {duplicate_file}: {e}")
    
    def fix_all_encoding_issues(self):
        """Fix encoding issues in all markdown files."""
        print("🔧 Fixing character encoding issues...")
        
        for company_dir in self.blogs_dir.iterdir():
            if not company_dir.is_dir():
                continue
                
            for md_file in company_dir.glob('*.md'):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Fix encoding issues
                    fixed_content, had_issues = self.fix_encoding_issues(content)
                    
                    # Clean markdown
                    cleaned_content = self.clean_markdown_content(fixed_content)
                    
                    # Write back if changes were made
                    if had_issues or cleaned_content != content:
                        with open(md_file, 'w', encoding='utf-8') as f:
                            f.write(cleaned_content)
                        
                        if had_issues:
                            self.stats['encoding_fixed'] += 1
                            print(f"   🔧 Fixed encoding: {md_file.name}")
                        
                        self.stats['files_cleaned'] += 1
                        
                except Exception as e:
                    print(f"   ❌ Error processing {md_file}: {e}")
    
    def get_existing_article_hashes(self):
        """Get hashes of all existing articles for duplicate prevention."""
        hashes = set()
        
        for company_dir in self.blogs_dir.iterdir():
            if not company_dir.is_dir():
                continue
                
            for md_file in company_dir.glob('*.md'):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    hashes.add(self.get_content_hash(content))
                except:
                    continue
        
        return hashes
    
    def run_full_cleanup(self):
        """Run complete cleanup process."""
        print("🧹 BLOG DEDUPLICATION & CLEANUP")
        print("=" * 50)
        
        print(f"📁 Processing directory: {self.blogs_dir}")
        print(f"📊 Total files found: {len(list(self.blogs_dir.rglob('*.md')))}")
        
        # Remove duplicates
        self.remove_duplicates()
        
        # Fix encoding issues
        self.fix_all_encoding_issues()
        
        # Print final stats
        print(f"\n✅ CLEANUP COMPLETE")
        print("=" * 30)
        print(f"📁 Total files processed: {self.stats['total_files']}")
        print(f"🗑️  Duplicates removed: {self.stats['duplicates_removed']}")
        print(f"🔧 Encoding issues fixed: {self.stats['encoding_fixed']}")
        print(f"🧹 Files cleaned: {self.stats['files_cleaned']}")
        
        # Final count
        final_count = len(list(self.blogs_dir.rglob('*.md')))
        print(f"📊 Final article count: {final_count}")


def main():
    deduplicator = BlogDeduplicator()
    deduplicator.run_full_cleanup()


if __name__ == "__main__":
    main()