import os
import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Mapping of schools to their actual domains
school_domains = {
    # US Schools
    "Boston College Carroll School of Management": "bc.edu",
    "Michigan State Broad College of Business": "broad.msu.edu",
    "Georgia Terry College of Business": "terry.uga.edu",
    "Maryland Smith School of Business": "smith.umd.edu",
    "Rochester Simon Business School": "simon.rochester.edu",
    "Boston University Questrom School of Business": "questrom.bu.edu",
    "SMU Cox School of Business": "cox.smu.edu",
    "UC Davis Graduate School of Management": "gsm.ucdavis.edu",
    "Colorado Leeds School of Business": "leeds.colorado.edu",
    "Connecticut School of Business": "business.uconn.edu",
    "Fordham Gabelli School of Business": "gabelli.fordham.edu",
    "George Washington School of Business": "business.gwu.edu",
    "Miami Business School": "bus.miami.edu",
    "Missouri Trulaske College of Business": "business.missouri.edu",
    "Northeastern D'Amore-McKim School of Business": "damore-mckim.northeastern.edu",
    "Rutgers Business School": "business.rutgers.edu",
    "Temple Fox School of Business": "fox.temple.edu",
    "Tennessee Haslam College of Business": "haslam.utk.edu",
    "Texas A&M Mays Business School": "mays.tamu.edu",
    "Tulane Freeman School of Business": "freeman.tulane.edu",
    "Arkansas Walton College of Business": "walton.uark.edu",
    "Auburn Harbert College of Business": "harbert.auburn.edu",
    "Baylor Hankamer School of Business": "baylor.edu/business",
    "Case Western Weatherhead School of Management": "weatherhead.case.edu",
    "Cincinnati Lindner College of Business": "business.uc.edu",
    "Clemson College of Business": "business.clemson.edu",
    "Delaware Lerner College of Business": "lerner.udel.edu",
    "DePaul Driehaus College of Business": "driehaus.depaul.edu",
    "Drexel LeBow College of Business": "lebow.drexel.edu",
    "George Mason School of Business": "business.gmu.edu",
    "Houston Bauer College of Business": "bauer.uh.edu",
    "Howard School of Business": "business.howard.edu",
    "Kansas School of Business": "business.ku.edu",
    "Kentucky Gatton College of Business": "gatton.uky.edu",
    "LSU Ourso College of Business": "lsu.edu/business",
    "Louisville College of Business": "business.louisville.edu",
    "Loyola Chicago Quinlan School of Business": "luc.edu/quinlan",
    "NC State Jenkins Graduate School of Management": "mgt.ncsu.edu",
    "Oklahoma Price College of Business": "price.ou.edu",
    "Oregon Lundquist College of Business": "business.uoregon.edu",
    "Pepperdine Graziadio Business School": "bschool.pepperdine.edu",
    "San Diego State Fowler College of Business": "business.sdsu.edu",
    "South Carolina Darla Moore School of Business": "sc.edu/moore",
    "Syracuse Whitman School of Management": "whitman.syr.edu",
    "TCU Neeley School of Business": "neeley.tcu.edu",
    "Texas Tech Rawls College of Business": "rawlsbusiness.ttu.edu",
    "Thunderbird School of Global Management": "thunderbird.asu.edu",
    "Tulsa Collins College of Business": "business.utulsa.edu",
    "Utah Eccles School of Business": "eccles.utah.edu",
    "Villanova School of Business": "villanova.edu/business",
    "Virginia Tech Pamplin College of Business": "pamplin.vt.edu",
    "Wake Forest School of Business": "business.wfu.edu",
    "William & Mary Mason School of Business": "mason.wm.edu",
    "American Kogod School of Business": "kogod.american.edu",
    "Baruch Zicklin School of Business": "zicklin.baruch.cuny.edu",
    "Clark University Graduate School of Management": "clarku.edu/gsom",
    "Stevens School of Business": "stevens.edu/school-business",
    
    # Canadian Schools
    "Rotman School of Management - University of Toronto": "rotman.utoronto.ca",
    "Ivey Business School - Western University": "ivey.uwo.ca",
    "Desautels Faculty of Management - McGill University": "mcgill.ca/desautels",
    "Sauder School of Business - University of British Columbia": "sauder.ubc.ca",
    "Smith School of Business - Queen's University": "smith.queensu.ca",
    "Schulich School of Business - York University": "schulich.yorku.ca",
    "DeGroote School of Business - McMaster University": "degroote.mcmaster.ca",
    "Alberta School of Business - University of Alberta": "business.ualberta.ca",
    "HEC Montreal": "hec.ca",
    "Haskayne School of Business - University of Calgary": "haskayne.ucalgary.ca",
    
    # Indian Schools
    "IIM Ahmedabad": "iima.ac.in",
    "IIM Bangalore": "iimb.ac.in",
    "IIM Calcutta": "iimcal.ac.in",
    "IIM Lucknow": "iiml.ac.in",
    "IIM Kozhikode": "iimk.ac.in",
    "IIM Indore": "iimidr.ac.in",
    "ISB Hyderabad": "isb.edu",
    "IIM Shillong": "iimshillong.ac.in",
    "IIM Udaipur": "iimu.ac.in",
    "IIM Trichy": "iimtrichy.ac.in",
    "IIM Raipur": "iimraipur.ac.in",
    "IIM Ranchi": "iimranchi.ac.in",
    "IIM Kashipur": "iimkashipur.ac.in",
    "IIM Rohtak": "iimrohtak.ac.in",
    "IIM Visakhapatnam": "iimv.ac.in",
    "IIM Amritsar": "iima.ac.in",
    "IIM Bodh Gaya": "iimbg.ac.in",
    "IIM Sambalpur": "iimsambalpur.ac.in",
    "IIM Sirmaur": "iimsirmaur.ac.in",
    "IIM Nagpur": "iimnagpur.ac.in",
    "IIM Jammu": "iimj.ac.in",
    "FMS Delhi": "fms.edu",
    "XLRI Jamshedpur": "xlri.ac.in",
    "MDI Gurgaon": "mdi.ac.in",
    "SPJIMR Mumbai": "spjimr.org",
    "JBIMS Mumbai": "jbims.edu",
    "IIFT Delhi": "iift.edu",
    "NMIMS Mumbai": "nmims.edu",
    "SIBM Pune": "sibm.edu.in",
    "SCMHRD Pune": "scmhrd.edu",
    
    # European Schools
    "INSEAD": "insead.edu",
    "London Business School": "london.edu",
    "HEC Paris": "hec.edu",
    "IESE Business School": "iese.edu",
    "IMD Business School": "imd.org",
    "IE Business School": "ie.edu",
    "SDA Bocconi School of Management": "unibocconi.it",
    "ESADE Business School": "esade.edu",
    "Cambridge Judge Business School": "jbs.cam.ac.uk",
    "Oxford Said Business School": "sbs.ox.ac.uk",
    "Imperial College Business School": "imperial.ac.uk/business-school",
    "Warwick Business School": "wbs.ac.uk",
    "Manchester Alliance Business School": "mbs.ac.uk",
    "ESSEC Business School": "essec.edu",
    "ESCP Business School": "escp.eu",
    "Rotterdam School of Management": "rsm.nl",
    "St. Gallen Business School": "unisg.ch",
    "WHU Otto Beisheim School of Management": "whu.edu",
    "Mannheim Business School": "mannheim-business-school.com",
    "EDHEC Business School": "edhec.edu",
    "emlyon business school": "em-lyon.com",
    "Grenoble Ecole de Management": "grenoble-em.com",
    "Copenhagen Business School": "cbs.dk",
    "Stockholm School of Economics": "hhs.se",
    "NHH Norwegian School of Economics": "nhh.no"
}

def download_logo_by_domain(school_name, domain, index, total):
    safe_filename = "".join(c for c in school_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_filename = safe_filename.replace(' ', '_')[:100]
    
    # Check if already exists
    for ext in ['.png', '.jpg', '.svg']:
        filepath = f"logos/business_school_logos/{safe_filename}{ext}"
        if os.path.exists(filepath):
            return {'school': school_name, 'status': 'skipped', 'filepath': filepath}
    
    print(f"[{index}/{total}] Downloading: {school_name} ({domain})")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    # Try different variations of the domain
    domain_variations = [
        domain,
        domain.split('.')[0],  # Just the subdomain
        domain.replace('/', '.')  # Replace slashes with dots
    ]
    
    for domain_var in domain_variations:
        methods = [
            {
                'name': 'Clearbit',
                'url': f"https://logo.clearbit.com/{domain_var}",
                'params': {'size': '512', 'format': 'png'}
            },
            {
                'name': 'Logo.dev',
                'url': f"https://img.logo.dev/{domain_var}",
                'params': {'token': 'pk_X8wlC2LJQkCG3ibQQDeQ_g', 'size': '512'}
            }
        ]
        
        for method in methods:
            try:
                response = requests.get(method['url'], headers=headers, params=method['params'], timeout=10)
                
                if response.status_code == 200 and response.headers.get('content-type', '').startswith('image'):
                    content_type = response.headers.get('content-type', '')
                    if 'png' in content_type:
                        ext = 'png'
                    elif 'jpeg' in content_type or 'jpg' in content_type:
                        ext = 'jpg'
                    elif 'svg' in content_type:
                        ext = 'svg'
                    else:
                        ext = 'png'
                    
                    filepath = f"logos/business_school_logos/{safe_filename}.{ext}"
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    print(f"  ✓ Success using {method['name']}!")
                    return {'school': school_name, 'status': 'success', 'method': method['name'], 'filepath': filepath}
                    
            except Exception as e:
                continue
    
    print(f"  ✗ Failed")
    return {'school': school_name, 'status': 'failed'}

# Download logos
print(f"Downloading logos for {len(school_domains)} schools using their domains...")

all_results = []
batch_size = 25

schools_list = list(school_domains.items())

for i in range(0, len(schools_list), batch_size):
    batch = schools_list[i:i+batch_size]
    print(f"\nBatch {i//batch_size + 1}/{(len(schools_list) + batch_size - 1)//batch_size}")
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        for j, (school, domain) in enumerate(batch):
            future = executor.submit(download_logo_by_domain, school, domain, i+j+1, len(schools_list))
            futures[future] = school
            time.sleep(0.1)
        
        for future in as_completed(futures):
            result = future.result()
            all_results.append(result)
    
    if i + batch_size < len(schools_list):
        time.sleep(1)

# Save results
with open('logos/domain_download_results.json', 'w') as f:
    json.dump(all_results, f, indent=2)

# Summary
successful = sum(1 for r in all_results if r['status'] == 'success')
failed = sum(1 for r in all_results if r['status'] == 'failed')
skipped = sum(1 for r in all_results if r['status'] == 'skipped')

print(f"\n=== FINAL RESULTS ===")
print(f"Successfully downloaded: {successful}")
print(f"Failed: {failed}")
print(f"Skipped (already exist): {skipped}")
print(f"Total processed: {len(all_results)}")
if successful + failed > 0:
    print(f"Success rate: {successful/(successful+failed)*100:.1f}%")