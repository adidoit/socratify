import json
import os
from collections import defaultdict

# Load all result files
result_files = [
    'logos/download_results.json',  # Original CSV employers
    'logos/global_download_results.json',  # Global MBA employers
    'logos/institution_download_results.json',  # Institutions from list.txt
    'logos/business_school_download_results.json',  # Business schools
    'logos/final_business_school_results.json',  # Additional business schools
    'logos/domain_download_results.json'  # Domain-based downloads
]

all_failures = []
all_successes = []
failure_patterns = defaultdict(list)

for file_path in result_files:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            results = json.load(f)
            
        for result in results:
            if 'status' in result:
                if result['status'] == 'failed':
                    name = result.get('employer') or result.get('institution') or result.get('school', '')
                    all_failures.append(name)
                    
                    # Categorize failures
                    name_lower = name.lower()
                    if 'cdn' in name_lower or 'static' in name_lower or 'assets' in name_lower:
                        failure_patterns['cdn/static'].append(name)
                    elif any(x in name_lower for x in ['.com', '.org', '.edu', '.net']):
                        failure_patterns['domain_in_name'].append(name)
                    elif len(name) < 5:
                        failure_patterns['too_short'].append(name)
                    elif '&' in name or '-' in name_lower:
                        failure_patterns['special_chars'].append(name)
                    elif any(x in name_lower for x in ['university', 'college', 'school', 'business']):
                        failure_patterns['educational'].append(name)
                    else:
                        failure_patterns['other'].append(name)
                        
                elif result['status'] == 'success':
                    name = result.get('employer') or result.get('institution') or result.get('school', '')
                    all_successes.append(name)

# Remove duplicates
unique_failures = list(set(all_failures))
unique_successes = list(set(all_successes))

print("=== DOWNLOAD FAILURE ANALYSIS ===")
print(f"Total unique failures: {len(unique_failures)}")
print(f"Total unique successes: {len(unique_successes)}")
print(f"Overall success rate: {len(unique_successes)/(len(unique_successes)+len(unique_failures))*100:.1f}%")

print("\n=== FAILURE PATTERNS ===")
for pattern, companies in sorted(failure_patterns.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"\n{pattern.upper()} ({len(companies)} failures):")
    # Show first 10 examples
    for company in sorted(set(companies))[:10]:
        print(f"  • {company}")
    if len(set(companies)) > 10:
        print(f"  ... and {len(set(companies)) - 10} more")

# Identify potentially fixable failures
print("\n=== POTENTIALLY FIXABLE FAILURES ===")

# Companies that might work with better search terms
fixable = []
for failure in unique_failures:
    failure_lower = failure.lower()
    # Skip CDN/static assets
    if any(x in failure_lower for x in ['cdn', 'static', 'assets', 'favicon']):
        continue
    # Skip placeholder names
    if failure in ['ama', 'api', 'aga', 'bis', 'cdp', 'cps', 'fx']:
        continue
    # Educational institutions often need special handling
    if any(x in failure_lower for x in ['university', 'college', 'school']) and failure not in unique_successes:
        fixable.append(failure)
    # Companies with special characters
    elif ('&' in failure or '-' in failure) and failure not in unique_successes:
        fixable.append(failure)

print(f"\nFound {len(fixable)} potentially fixable failures")

# Save lists for further processing
with open('logos/all_failed_downloads.txt', 'w') as f:
    for failure in sorted(unique_failures):
        f.write(f"{failure}\n")

with open('logos/fixable_failures.txt', 'w') as f:
    for failure in sorted(fixable):
        f.write(f"{failure}\n")

print(f"\nSaved failed downloads to: logos/all_failed_downloads.txt")
print(f"Saved fixable failures to: logos/fixable_failures.txt")

# Analyze which download methods worked best
method_stats = defaultdict(int)
for file_path in result_files:
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            results = json.load(f)
        
        for result in results:
            if result.get('status') == 'success' and 'method' in result:
                method_stats[result['method']] += 1

print("\n=== SUCCESSFUL DOWNLOAD METHODS ===")
for method, count in sorted(method_stats.items(), key=lambda x: x[1], reverse=True):
    print(f"{method}: {count} successes")