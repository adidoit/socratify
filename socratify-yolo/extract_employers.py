import csv
import re

# Read the CSV file manually to handle parsing issues
all_employers = set()

with open('logos/business_school_employers_65.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header
    
    for row in reader:
        if len(row) < 24:  # Skip incomplete rows
            continue
            
        # Extract employers from positions 3, 5, 7, 9, 11, 13, 15, 17, 19, 21
        # These are Employer1, Employer2, ..., Employer10 columns
        employer_positions = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
        
        for pos in employer_positions:
            if pos < len(row) and row[pos]:
                employer = row[pos].strip()
                # Skip empty values and numeric values (which are counts)
                if employer and not employer.replace('.', '').replace(',', '').isdigit() and employer != '≥2':
                    all_employers.add(employer)

# Convert to sorted list
unique_employers = sorted(list(all_employers))

print(f"Found {len(unique_employers)} unique employers")
print("\nUnique employers:")
for emp in unique_employers:
    print(f"- {emp}")

# Save to file for reference
with open('logos/unique_employers.txt', 'w') as f:
    for emp in unique_employers:
        f.write(f"{emp}\n")