#!/usr/bin/env python3
"""
Download logos for top business schools we're actually missing
"""

import os
import requests
import json
import urllib.parse

# These are the ACTUAL domains for top business schools
TOP_SCHOOL_DOMAINS = {
    # Schools we're definitely missing
    "Michigan Ross School of Business": "michiganross.umich.edu",
    "Harvard Business School": "hbs.edu",
    "Stanford Graduate School of Business": "gsb.stanford.edu",
    "Duke Fuqua School of Business": "fuqua.duke.edu",
    "NYU Stern School of Business": "stern.nyu.edu",
    "Cornell Johnson School of Management": "johnson.cornell.edu",
    "Northwestern Kellogg School of Management": "kellogg.northwestern.edu",
    "UC Berkeley Haas School of Business": "haas.berkeley.edu",
    "Carnegie Mellon Tepper School of Business": "tepper.cmu.edu",
    "UNC Kenan-Flagler Business School": "kenan-flagler.unc.edu",
    "Virginia Darden School of Business": "darden.virginia.edu",
    "Indiana Kelley School of Business": "kelley.iu.edu",
    "Georgetown McDonough School of Business": "msb.georgetown.edu",
    "Vanderbilt Owen Graduate School of Management": "owen.vanderbilt.edu",
    "Washington Olin Business School": "olin.wustl.edu",
    "Rice Jones Graduate School of Business": "business.rice.edu",
    "Notre Dame Mendoza College of Business": "mendoza.nd.edu",
    "Boston College Carroll School of Management": "bc.edu/bc-web/schools/carroll-school.html",
    "Rochester Simon Business School": "simon.rochester.edu",
    "Michigan State Broad College of Business": "broad.msu.edu",
}

# Check what we already have
existing = set()
if os.path.exists('logos/business_school_logos'):
    existing = {f.lower() for f in os.listdir('logos/business_school_logos')}

os.makedirs('logos/business_school_logos', exist_ok=True)

results = []
downloaded = 0

print("=" * 70)
print("DOWNLOADING MISSING TOP BUSINESS SCHOOL LOGOS")
print("=" * 70)

for school, domain in TOP_SCHOOL_DOMAINS.items():
    # Check if we already have it
    school_clean = school.replace(' ', '_')
    if any(school_clean.lower() in ex for ex in existing):
        print(f"✓ {school:<50} (already exists)")
        continue
    
    # Try multiple strategies
    success = False
    
    # Strategy 1: Direct domain
    try:
        url = f"https://logo.clearbit.com/{domain}"
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
            filename = f"{school_clean}.png"
            filepath = os.path.join('logos/business_school_logos', filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✓ {school:<50} → {domain}")
            results.append({
                'school': school,
                'status': 'success',
                'method': f'clearbit_{domain}',
                'filepath': filepath
            })
            downloaded += 1
            success = True
    except:
        pass
    
    # Strategy 2: Try parent domain
    if not success and '.' in domain:
        parent_domain = '.'.join(domain.split('.')[-2:])
        try:
            url = f"https://logo.clearbit.com/{parent_domain}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                filename = f"{school_clean}.png"
                filepath = os.path.join('logos/business_school_logos', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ {school:<50} → {parent_domain}")
                results.append({
                    'school': school,
                    'status': 'success',
                    'method': f'clearbit_{parent_domain}',
                    'filepath': filepath
                })
                downloaded += 1
                success = True
        except:
            pass
    
    # Strategy 3: Try alternative APIs
    if not success:
        # Try logo.dev
        try:
            url = f"https://img.logo.dev/{domain}?token=pk_X-1ZO13GSgeOoUrIuCGGfw"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                filename = f"{school_clean}.png"
                filepath = os.path.join('logos/business_school_logos', filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                print(f"✓ {school:<50} → logo.dev/{domain}")
                results.append({
                    'school': school,
                    'status': 'success',
                    'method': f'logodev_{domain}',
                    'filepath': filepath
                })
                downloaded += 1
                success = True
        except:
            pass
    
    if not success:
        print(f"✗ {school:<50} → FAILED")
        results.append({
            'school': school,
            'status': 'failed',
            'domain': domain
        })

# Save results
with open('logos/top_schools_download_results.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\n" + "=" * 70)
print(f"DOWNLOAD COMPLETE: {downloaded} new logos")
print("=" * 70)

# List what we now have for top schools
print("\nCurrent business school logos:")
if os.path.exists('logos/business_school_logos'):
    files = sorted([f for f in os.listdir('logos/business_school_logos') if f.endswith(('.png', '.jpg', '.svg'))])
    for f in files[:20]:
        print(f"  • {f}")
    if len(files) > 20:
        print(f"  ... and {len(files) - 20} more")