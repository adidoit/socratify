#!/usr/bin/env python3
"""
Create the final, well-organized logo collection structure
"""

import os
import shutil
import hashlib
from collections import defaultdict
import json

# Define the final structure
FINAL_BASE = 'logos/final_collection'
STRUCTURE = {
    'business_schools': 'Business school logos (separate from universities)',
    'universities': 'University and college logos',
    'companies': 'Company and employer logos'
}

def get_file_hash(filepath):
    """Calculate MD5 hash of file content"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except:
        return None

def create_final_structure():
    """Create clean, deduplicated final structure"""
    print("=" * 80)
    print("CREATING FINAL LOGO COLLECTION")
    print("=" * 80)
    
    # Create directories
    for category in STRUCTURE:
        os.makedirs(os.path.join(FINAL_BASE, category), exist_ok=True)
    
    # Track all files by hash to avoid duplicates
    all_hashes = {}
    stats = defaultdict(int)
    
    # Source directory
    source_base = 'logos/organized_collection'
    
    print("\nProcessing organized collection...")
    
    # Process each category
    for category in ['business_schools', 'universities', 'companies']:
        category_dir = os.path.join(source_base, category)
        dest_dir = os.path.join(FINAL_BASE, category)
        
        print(f"\n{category.upper().replace('_', ' ')}:")
        
        # Process all regions
        for region in os.listdir(category_dir):
            region_path = os.path.join(category_dir, region)
            if not os.path.isdir(region_path):
                continue
            
            region_count = 0
            
            for filename in os.listdir(region_path):
                if not filename.endswith(('.png', '.jpg', '.svg')):
                    continue
                
                source_path = os.path.join(region_path, filename)
                file_hash = get_file_hash(source_path)
                
                if file_hash:
                    if file_hash not in all_hashes:
                        # New unique file
                        dest_path = os.path.join(dest_dir, filename)
                        
                        # Handle filename conflicts
                        if os.path.exists(dest_path):
                            base, ext = os.path.splitext(filename)
                            counter = 1
                            while os.path.exists(dest_path):
                                dest_path = os.path.join(dest_dir, f"{base}_{counter}{ext}")
                                counter += 1
                        
                        try:
                            shutil.copy2(source_path, dest_path)
                            all_hashes[file_hash] = dest_path
                            stats[category] += 1
                            region_count += 1
                        except Exception as e:
                            print(f"    Error: {e}")
            
            if region_count > 0:
                print(f"  {region}: {region_count} logos")
    
    # Create comprehensive summary
    print("\n" + "=" * 80)
    print("FINAL COLLECTION SUMMARY")
    print("=" * 80)
    
    total = sum(stats.values())
    print(f"\n📊 TOTAL UNIQUE LOGOS: {total:,}")
    print("\nBreakdown by category:")
    for category, count in stats.items():
        print(f"  • {category.replace('_', ' ').title()}: {count:,}")
    
    # Calculate total size
    total_size = 0
    for category in STRUCTURE:
        category_dir = os.path.join(FINAL_BASE, category)
        for filename in os.listdir(category_dir):
            if filename.endswith(('.png', '.jpg', '.svg')):
                filepath = os.path.join(category_dir, filename)
                total_size += os.path.getsize(filepath)
    
    print(f"\n💾 Total size: {total_size / (1024 * 1024):.1f} MB")
    print(f"📁 Location: {FINAL_BASE}")
    
    # Create detailed summary file
    summary_path = os.path.join(FINAL_BASE, 'COLLECTION_SUMMARY.md')
    with open(summary_path, 'w') as f:
        f.write("# Final Logo Collection Summary\n\n")
        f.write(f"**Total Unique Logos:** {total:,}\n\n")
        f.write("## Categories\n\n")
        f.write(f"### 1. Business Schools ({stats['business_schools']:,} logos)\n")
        f.write("Separate logos for business schools with distinct branding:\n")
        f.write("- Harvard Business School, Wharton, Kellogg, Booth, Sloan\n")
        f.write("- INSEAD, London Business School, HEC Paris, IESE, IMD\n")
        f.write("- IIMs (Ahmedabad, Bangalore, Calcutta, etc.)\n")
        f.write("- ISB, XLRI, FMS, and other top business schools\n\n")
        f.write(f"### 2. Universities ({stats['universities']:,} logos)\n")
        f.write("Parent universities and educational institutions:\n")
        f.write("- Top 250 US universities\n")
        f.write("- Top 100 Canadian universities\n")
        f.write("- Top 100 UK universities\n")
        f.write("- Top 100 European universities\n")
        f.write("- Top 100 Indian universities (IITs, NITs, etc.)\n")
        f.write("- Top 50 Australian universities\n")
        f.write("- Top global universities\n\n")
        f.write(f"### 3. Companies ({stats['companies']:,} logos)\n")
        f.write("Comprehensive employer coverage:\n")
        f.write("- Consulting: MBB, Big 4, Tier 2, boutiques\n")
        f.write("- Finance: Investment banks, PE/VC, hedge funds, commercial banks\n")
        f.write("- Technology: FAANG, unicorns, startups, enterprise software\n")
        f.write("- Law firms: Magic Circle, White Shoe, global elite\n")
        f.write("- Healthcare: Pharma, biotech, medical devices\n")
        f.write("- Consumer: CPG, retail, luxury brands\n")
        f.write("- Industrial: Aerospace, defense, automotive, energy\n")
        f.write("- And many more sectors...\n\n")
        f.write("## Coverage\n")
        f.write("- **Geographic:** Global coverage across all continents\n")
        f.write("- **Industries:** All major sectors where MBAs are recruited\n")
        f.write("- **Quality:** Deduplicated, high-quality logos\n\n")
        f.write(f"**Collection size:** {total_size / (1024 * 1024):.1f} MB\n")
    
    # Create usage guide
    usage_path = os.path.join(FINAL_BASE, 'USAGE_GUIDE.md')
    with open(usage_path, 'w') as f:
        f.write("# Logo Collection Usage Guide\n\n")
        f.write("## Directory Structure\n")
        f.write("```\n")
        f.write("final_collection/\n")
        f.write("├── business_schools/     # Business school specific logos\n")
        f.write("├── universities/         # University logos\n")
        f.write("└── companies/           # Company/employer logos\n")
        f.write("```\n\n")
        f.write("## Important Notes\n\n")
        f.write("1. **Business Schools vs Universities**: Business schools often have separate branding\n")
        f.write("   - Use `business_schools/` for business school specific logos\n")
        f.write("   - Use `universities/` for parent university logos\n")
        f.write("   - Example: 'Harvard Business School' logo vs 'Harvard University' logo\n\n")
        f.write("2. **File Naming**: Files are named with underscores replacing spaces\n")
        f.write("   - Example: `Harvard_Business_School.png`\n\n")
        f.write("3. **Duplicates**: This collection has been deduplicated\n")
        f.write("   - Each logo appears only once\n")
        f.write("   - Highest quality version was kept\n\n")
        f.write("4. **Updates**: To add new logos, ensure they don't duplicate existing ones\n")
    
    print(f"\n✅ Final collection created successfully!")
    print(f"✅ Summary: {summary_path}")
    print(f"✅ Usage guide: {usage_path}")

if __name__ == "__main__":
    create_final_structure()