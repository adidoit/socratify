#!/usr/bin/env python3
"""
Fix quote formatting issues in the CSV database.
Issues: 
1. Triple quotes should be single quotes
2. Missing line breaks between records
3. Improperly escaped quotes
"""

import csv
import re

def fix_csv_quotes(input_file, output_file):
    """Fix quote formatting issues in CSV file"""
    
    # Read the entire file as text first
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the main structural issues
    # 1. Fix line breaks that got merged (pattern: quote"Company -> quote"\nCompany)
    content = re.sub(r'\"([^"]+)\",\"([^"]+)\",\"([^"]+)\"([A-Z][^,]+),', r'"\1","\2","\3"\n\4,', content)
    
    # 2. Replace triple quotes with single quotes
    content = re.sub(r'"""([^"]+?)"""', r'"\1"', content)
    
    # 3. Fix specific cases where records are merged
    content = re.sub(r'(\d{4}")(General Atlantic)', r'\1\n\2', content)
    content = re.sub(r'(\d{4}")(Vista Equity)', r'\1\n\2', content)
    content = re.sub(r'(\d{4}")(Silver Lake)', r'\1\n\2', content)
    content = re.sub(r'(\d{4}")(Thoma Bravo)', r'\1\n\2', content)
    content = re.sub(r'(\d{4}")(Insight Partners)', r'\1\n\2', content)
    content = re.sub(r'(\d{4}")(TA Associates)', r'\1\n\2', content)
    content = re.sub(r'(\d{4}")(Boeing)', r'\1\n\2', content)
    
    # Write the corrected content back
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed quote formatting issues and saved to {output_file}")
    
    # Verify by counting lines
    lines = content.strip().split('\n')
    print(f"Total lines in corrected file: {len(lines)}")
    print(f"Expected: Header + 1265 questions = 1266 lines")

if __name__ == "__main__":
    input_file = "CLEAN_BUSINESS_BEHAVIORAL_DATABASE.csv"
    output_file = "CLEAN_BUSINESS_BEHAVIORAL_DATABASE_FIXED.csv"
    fix_csv_quotes(input_file, output_file)