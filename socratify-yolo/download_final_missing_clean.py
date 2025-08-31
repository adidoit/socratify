#!/usr/bin/env python3
"""
Download final 234 missing companies with clean filenames
Filenames will be exactly the company name, no extra noise
"""

import os
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configuration
MAX_WORKERS = 15
RATE_LIMIT = threading.Semaphore(10)  # Max 10 concurrent requests
RATE_LIMIT_DELAY = 0.1  # 100ms delay between requests

def clean_filename(company_name):
    """Convert company name to clean filename"""
    # Simple clean conversion: replace special chars with underscores, remove multiple underscores
    filename = company_name.replace('&', 'and')
    filename = re.sub(r'[^\w\s-]', '', filename)  # Keep only alphanumeric, spaces, hyphens
    filename = re.sub(r'\s+', '_', filename)  # Replace spaces with single underscore
    filename = re.sub(r'_+', '_', filename)  # Replace multiple underscores with single
    filename = filename.strip('_')  # Remove leading/trailing underscores
    return filename

def generate_domains(company_name):
    """Generate possible domain variations"""
    base = company_name.lower()
    
    # Clean the name
    base = base.replace('&', 'and')
    base = base.replace('.', '')
    base = base.replace(',', '')
    base = base.replace("'", '')
    base = base.replace('"', '')
    base = base.replace('(', '').replace(')', '')
    base = base.replace('[', '').replace(']', '')
    base = base.replace('{', '').replace('}', '')
    
    # Split into words
    words = base.split()
    
    domains = []
    
    if len(words) == 1:
        domains.extend([
            f"{words[0]}.com",
            f"{words[0]}.io", 
            f"{words[0]}.co",
            f"{words[0]}.net",
            f"{words[0]}corp.com",
            f"{words[0]}inc.com"
        ])
    elif len(words) == 2:
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com",
            f"{words[1]}.com",
            f"{words[0]}{words[1]}.io",
            f"{words[0]}-{words[1]}.io"
        ])
    elif len(words) >= 3:
        # First two words
        domains.extend([
            f"{words[0]}{words[1]}.com",
            f"{words[0]}-{words[1]}.com",
            f"{words[0]}.com"
        ])
        
        # Try acronym (first letters)
        acronym = ''.join(word[0] for word in words if word)
        if len(acronym) >= 2:
            domains.extend([
                f"{acronym}.com",
                f"{acronym}.io"
            ])
    
    # Special domain mappings
    special_cases = {
        '10x genomics': ['10xgenomics.com'],
        'a24': ['a24films.com'],
        'ab inbev': ['ab-inbev.com', 'anheuser-busch.com'],
        'abn amro': ['abnamro.com', 'abnamro.nl'],
        'agco corporation': ['agcocorp.com'],
        'abbott laboratories': ['abbott.com'],
        'accenture strategy': ['accenture.com'],
        'air products & chemicals': ['airproducts.com'],
        'alaska airlines': ['alaskaair.com'],
        'alexion pharmaceuticals': ['alexion.com'],
        'altice usa': ['alticeusa.com'],
        'alvarez & marsal': ['alvarezandmarsal.com'],
        'american airlines': ['aa.com'],
        'american electric power': ['aep.com'],
        'apollo global management': ['apollo.com'],
        'asus': ['asus.com'],
        'audemars piguet': ['audemarspiguet.com'],
        'avalonbay communities': ['avalonbay.com'],
        'bae systems': ['baesystems.com'],
        'bnp paribas': ['bnpparibas.com'],
        'bed bath & beyond': ['bedbathandbeyond.com'],
        'betterment': ['betterment.com'],
        'biogen': ['biogen.com'],
        'biomedical': ['biomedical.com'],
        'biomarin': ['biomarin.com'],
        'blumhouse': ['blumhouse.com'],
        'bombardier': ['bombardier.com'],
        'boston scientific': ['bostonscientific.com'],
        'burberry': ['burberry.com'],
        'canadian national railway': ['cn.ca'],
        'canadian pacific railway': ['cpr.ca'],
        'cardinal health': ['cardinalhealth.com'],
        'carlyle group': ['carlyle.com'],
        'catl': ['catl.com'],
        'cb2': ['cb2.com'],
        'celanese': ['celanese.com'],
        'centene corporation': ['centene.com'],
        'centurylink': ['lumen.com'],
        'charles river associates': ['crai.com'],
        'charles schwab corporation': ['schwab.com'],
        'charter communications': ['spectrum.com'],
        'check point': ['checkpoint.com'],
        'choice hotels': ['choicehotels.com'],
        'cnh industrial': ['cnhindustrial.com'],
        'coca-cola': ['coca-cola.com'],
        'colliers international': ['colliers.com'],
        'community health systems': ['chs.net'],
        'conagra brands': ['conagrabrands.com'],
        'consolidated edison': ['conEd.com'],
        'constellation brands': ['cbrands.com'],
        'cox communications': ['cox.com'],
        'crate & barrel': ['crateandbarrel.com'],
        'credit karma': ['creditkarma.com'],
        'credit suisse': ['credit-suisse.com'],
        'csx transportation': ['csx.com'],
        'cushman & wakefield': ['cushmanwakefield.com'],
        'cyberark': ['cyberark.com'],
        'danaher corporation': ['danaher.com'],
        'dassault aviation': ['dassault-aviation.com'],
        'davita': ['davita.com'],
        'deere & company': ['deere.com'],
        'delivery hero': ['deliveryhero.com'],
        'dell technologies': ['dell.com'],
        'delta air lines': ['delta.com'],
        'deutsche bank': ['db.com'],
        'deutsche post dhl': ['dhl.com'],
        'discover financial services': ['discover.com'],
        'dollar general': ['dollargeneral.com'],
        'dollar tree': ['dollartree.com'],
        'dover corporation': ['dovercorporation.com'],
        'dow inc': ['dow.com'],
        'duke energy': ['duke-energy.com'],
        'dupont': ['dupont.com'],
        'e*trade': ['etrade.com'],
        'eastman chemical': ['eastman.com'],
        'eaton corporation': ['eaton.com'],
        'ecolab': ['ecolab.com'],
        'edwards lifesciences': ['edwards.com'],
        'eli lilly': ['lilly.com'],
        'embraer': ['embraer.com'],
        'emerson electric': ['emerson.com'],
        'encompass health': ['encompasshealth.com'],
        'energy transfer': ['energytransfer.com'],
        'enterprise products partners': ['enterpriseproducts.com'],
        'eqt partners': ['eqtpartners.com'],
        'equity residential': ['equityresidential.com'],
        'evercore': ['evercore.com'],
        'exact sciences': ['exactsciences.com'],
        'exelon': ['exeloncorp.com'],
        'expedia group': ['expediagroup.com'],
        'exxonmobil': ['exxonmobil.com'],
        'farmers insurance': ['farmers.com'],
        'fidelity investments': ['fidelity.com'],
        'fitbit': ['fitbit.com'],
        'flipkart': ['flipkart.com'],
        'ford': ['ford.com'],
        'fortinet': ['fortinet.com'],
        'fox corporation': ['fox.com'],
        'francisco partners': ['franciscopartners.com'],
        'franklin templeton': ['franklintempleton.com'],
        'fresenius medical care': ['freseniusmedicalcare.com'],
        'frontier airlines': ['flyfrontier.com'],
        'frontier communications': ['frontier.com'],
        'fujitsu': ['fujitsu.com'],
        'garmin': ['garmin.com'],
        'general dynamics': ['generaldynamics.com'],
        'general electric': ['ge.com'],
        'general mills': ['generalmills.com'],
        'general motors': ['gm.com'],
        'genmab': ['genmab.com'],
        'gilead sciences': ['gilead.com'],
        'glaxosmithkline': ['gsk.com'],
        'goto group': ['goto.com'],
        'grab': ['grab.com'],
        'grubhub': ['grubhub.com'],
        'h&m': ['hm.com'],
        'harris williams': ['harriswilliams.com'],
        'hawaiian airlines': ['hawaiianairlines.com'],
        'hca healthcare': ['hcahealthcare.com'],
        'hcl technologies': ['hcltech.com'],
        'hdfc bank': ['hdfcbank.com'],
        'heineken': ['heineken.com'],
        'hellman & friedman': ['hf.com'],
        'hilton': ['hilton.com'],
        'home depot': ['homedepot.com'],
        'honeywell': ['honeywell.com'],
        'hormel foods': ['hormel.com'],
        'hp inc': ['hp.com'],
        'hsbc': ['hsbc.com'],
        'humana': ['humana.com'],
        'huntsman corporation': ['huntsman.com'],
        'huron consulting': ['huronconsultinggroup.com'],
        'hyatt': ['hyatt.com'],
        'hyundai': ['hyundai.com'],
        'icici bank': ['icicibank.com'],
        'illumina': ['illumina.com'],
        'illinois tool works': ['itw.com'],
        'incyte': ['incyte.com'],
        'infosys': ['infosys.com'],
        'infosys consulting': ['infosys.com'],
        'ing group': ['ing.com'],
        'ingersoll rand': ['ingersollrand.com'],
        'instacart': ['instacart.com'],
        'interactive brokers': ['interactivebrokers.com'],
        'intercontinental hotels group': ['ihg.com'],
        'intuitive surgical': ['intuitive.com'],
        'invesco': ['invesco.com'],
        'j.b. hunt': ['jbhunt.com'],
        'jbs': ['jbs.com.br'],
        'jd.com': ['jd.com'],
        'jefferies': ['jefferies.com'],
        'jetblue airways': ['jetblue.com'],
        'jm smucker': ['jmsmucker.com'],
        'jnj': ['jnj.com'],
        'jones lang lasalle': ['jll.com'],
        'just eat takeaway': ['justeattakeaway.com'],
        'kansas city southern': ['kcsouthern.com'],
        'kddi': ['kddi.com'],
        'kellogg company': ['kellogg.com'],
        'kia': ['kia.com'],
        'kinder morgan': ['kindermorgan.com'],
        'kkr': ['kkr.com'],
        'kohls': ['kohls.com'],
        'kraft heinz': ['kraftheinzcompany.com'],
        'kroger': ['kroger.com'],
        'l3harris': ['l3harris.com'],
        'labcorp': ['labcorp.com'],
        'lazard': ['lazard.com'],
        'lek consulting': ['lek.com'],
        'lending club': ['lendingclub.com'],
        'lendingtree': ['lendingtree.com'],
        'leonard green & partners': ['leonardgreen.com'],
        'leonardo': ['leonardo.com'],
        'levi strauss': ['levistrauss.com'],
        'lg electronics': ['lg.com'],
        'liberty mutual': ['libertymutual.com'],
        'lincoln financial': ['lincolnfinancial.com'],
        'lincoln international': ['lincolninternational.com'],
        'linde': ['linde.com'],
        'lionsgate': ['lionsgate.com'],
        'lockheed martin': ['lockheedmartin.com'],
        'lowes': ['lowes.com'],
        'lululemon': ['lululemon.com'],
        'lyondellbasell': ['lyondellbasell.com'],
        'macys': ['macys.com'],
        'marathon petroleum': ['marathonpetroleum.com'],
        'marcus & millichap': ['marcusmillichap.com'],
        'marriott international': ['marriott.com'],
        'mars': ['mars.com'],
        'marvel entertainment': ['marvel.com'],
        'mckesson corporation': ['mckesson.com'],
        'meituan': ['meituan.com'],
        'mercado libre': ['mercadolibre.com'],
        'merck & co': ['merck.com'],
        'metlife': ['metlife.com'],
        'mgm': ['mgm.com'],
        'mint': ['mint.com'],
        'mitsubishi': ['mitsubishi.com'],
        'mitsui': ['mitsui.com'],
        'moelis & company': ['moelis.com'],
        'molina healthcare': ['molinahealthcare.com'],
        'monday.com': ['monday.com'],
        'mondelez international': ['mondelezinternational.com'],
        'moneygram': ['moneygram.com'],
        'monitor deloitte': ['deloitte.com'],
        'nbc universal': ['nbcuniversal.com'],
        'nec': ['nec.com'],
        'nera economic consulting': ['nera.com'],
        'netease': ['netease.com'],
        'newmark': ['newmark.com'],
        'nextera energy': ['nexteraenergy.com'],
        'nike': ['nike.com'],
        'nintendo': ['nintendo.com'],
        'nissan': ['nissan.com'],
        'norfolk southern': ['nscorp.com'],
        'nordstrom': ['nordstrom.com'],
        'northrop grumman': ['northropgrumman.com'],
        'northern trust': ['northerntrust.com'],
        'ntt docomo': ['nttdocomo.com'],
        'nvidia': ['nvidia.com'],
        'okta': ['okta.com'],
        'oliver wyman': ['oliverwyman.com'],
        'onplus': ['oneplus.com'],
        'overstock.com': ['overstock.com'],
        'pacific gas & electric': ['pge.com'],
        'palo alto networks': ['paloaltonetworks.com'],
        'panasonic': ['panasonic.com'],
        'paramount global': ['paramount.com'],
        'parker-hannifin': ['parker.com'],
        'parthenon-ey': ['ey.com'],
        'patagonia': ['patagonia.com'],
        'patek philippe': ['patek.com'],
        'personal capital': ['personalcapital.com'],
        'pfizer': ['pfizer.com'],
        'phillips 66': ['phillips66.com'],
        'ping identity': ['pingidentity.com'],
        'pinduoduo': ['pdd.com'],
        'piper sandler': ['pipersandler.com'],
        'plains gp holdings': ['plainsallamerican.com'],
        'pnc financial': ['pnc.com'],
        'pottery barn': ['potterybarn.com'],
        'ppg industries': ['ppg.com'],
        'prada': ['prada.com'],
        'progressive corporation': ['progressive.com'],
        'prologis': ['prologis.com'],
        'prudential financial': ['prudential.com'],
        'public service enterprise group': ['pseg.com'],
        'public storage': ['publicstorage.com'],
        'puma': ['puma.com'],
        'pwc strategy&': ['strategyand.pwc.com'],
        'quest diagnostics': ['questdiagnostics.com'],
        'rakuten': ['rakuten.com'],
        'raymond james': ['raymondjames.com'],
        'raytheon technologies': ['rtx.com'],
        'regeneron pharmaceuticals': ['regeneron.com'],
        'reliance industries': ['ril.com'],
        'remit2india': ['remit2india.com'],
        'remitly': ['remitly.com'],
        'restoration hardware': ['rh.com'],
        'richemont': ['richemont.com'],
        'roland berger': ['rolandberger.com'],
        'rolex': ['rolex.com'],
        'room & board': ['roomandboard.com'],
        'ross stores': ['rossstores.com'],
        'royal mail': ['royalmailgroup.com'],
        'saab': ['saab.com'],
        'samsung': ['samsung.com'],
        'sanofi': ['sanofi.com'],
        'sap': ['sap.com'],
        'sea limited': ['sea.com'],
        'seagen': ['seagen.com'],
        'sempra energy': ['sempra.com'],
        'sennheiser': ['sennheiser.com'],
        'sharp': ['sharp.com'],
        'sherwin-williams': ['sherwin-williams.com'],
        'societe generale': ['societegenerale.com'],
        'softbank': ['softbank.com'],
        'sony': ['sony.com'],
        'sony pictures': ['sonypictures.com'],
        'sonos': ['sonos.com'],
        'southern company': ['southerncompany.com'],
        'southwest airlines': ['southwest.com'],
        'spirit airlines': ['spirit.com'],
        'stanley black & decker': ['stanleyblackanddecker.com'],
        'state bank of india': ['sbi.co.in'],
        'state farm': ['statefarm.com'],
        'stephens inc': ['stephens.com'],
        'stryker': ['stryker.com'],
        'sumitomo': ['sumitomocorp.com'],
        't-mobile': ['t-mobile.com'],
        'take-two': ['take2games.com'],
        'target': ['target.com'],
        'tata consultancy services': ['tcs.com'],
        'tcs': ['tcs.com'],
        'td ameritrade': ['tdameritrade.com'],
        'tech mahindra': ['techmahindra.com'],
        'tenet healthcare': ['tenethealth.com'],
        'textron': ['textron.com'],
        'thales': ['thalesgroup.com'],
        'the north face': ['thenorthface.com'],
        'timberland': ['timberland.com'],
        'tjx companies': ['tjx.com'],
        'tomtom': ['tomtom.com'],
        'toshiba': ['toshiba.com'],
        'toyota': ['toyota.com'],
        'tpg': ['tpg.com'],
        'travelers companies': ['travelers.com'],
        'tripadvisor': ['tripadvisor.com'],
        'truist financial': ['truist.com'],
        'tsmc': ['tsmc.com'],
        'tyson foods': ['tysonfoods.com'],
        'ubs': ['ubs.com'],
        'under armour': ['underarmour.com'],
        'unilever': ['unilever.com'],
        'union pacific': ['up.com'],
        'uniqlo': ['uniqlo.com'],
        'united airlines': ['united.com'],
        'unitedhealth group': ['unitedhealthgroup.com'],
        'universal health services': ['uhsinc.com'],
        'us bancorp': ['usbank.com'],
        'usaa': ['usaa.com'],
        'valero energy': ['valero.com'],
        'vans': ['vans.com'],
        'verizon': ['verizon.com'],
        'vertex pharmaceuticals': ['vrtx.com'],
        'viacom': ['viacom.com'],
        'visa': ['visa.com'],
        'vista equity partners': ['vistaequitypartners.com'],
        'vivo': ['vivo.com'],
        'volkswagen': ['volkswagen.com'],
        'vornado realty trust': ['vno.com'],
        'wayfair': ['wayfair.com'],
        'wealthfront': ['wealthfront.com'],
        'wellcare health plans': ['wellcare.com'],
        'welltower': ['welltower.com'],
        'west elm': ['westelm.com'],
        'western union': ['westernunion.com'],
        'williams-sonoma': ['williams-sonoma.com'],
        'william blair': ['williamblair.com'],
        'windstream': ['windstream.com'],
        'wipro': ['wipro.com'],
        'wise': ['wise.com'],
        'wyndham hotels': ['wyndhamhotels.com'],
        'xcel energy': ['xcelenergy.com'],
        'xiaomi': ['mi.com'],
        'zara': ['zara.com'],
        'zimmer biomet': ['zimmerbiomet.com'],
        'zte': ['zte.com']
    }
    
    if base in special_cases:
        domains = special_cases[base] + domains
    
    return list(dict.fromkeys(domains))  # Remove duplicates while preserving order

def download_logo(company_name, output_dir):
    """Download logo for a company with clean filename"""
    
    with RATE_LIMIT:
        time.sleep(RATE_LIMIT_DELAY)
        
        domains = generate_domains(company_name)
        
        for domain in domains:
            try:
                # Try Clearbit first
                logo_url = f"https://logo.clearbit.com/{domain}"
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                }
                
                response = requests.get(logo_url, headers=headers, timeout=15, stream=True)
                
                if response.status_code == 200:
                    content_type = response.headers.get('Content-Type', '')
                    
                    # Skip if not an image
                    if 'image' not in content_type and 'octet-stream' not in content_type:
                        continue
                    
                    # Get file extension
                    if 'png' in content_type:
                        ext = 'png'
                    elif 'jpeg' in content_type or 'jpg' in content_type:
                        ext = 'jpg'
                    elif 'svg' in content_type:
                        ext = 'svg'
                    elif 'webp' in content_type:
                        ext = 'webp'
                    else:
                        ext = 'png'  # Default
                    
                    # Clean filename - just the company name
                    filename = f"{clean_filename(company_name)}.{ext}"
                    filepath = os.path.join(output_dir, filename)
                    
                    # Download and save
                    with open(filepath, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Check if file is valid (non-empty)
                    if os.path.getsize(filepath) > 500:  # At least 500 bytes
                        return f"✅ {company_name} -> {filename}"
                    else:
                        os.remove(filepath)
                
                # Also try Google Favicons as backup
                favicon_url = f"https://www.google.com/s2/favicons?domain={domain}&sz=256"
                response = requests.get(favicon_url, headers=headers, timeout=10)
                
                if response.status_code == 200 and len(response.content) > 500:
                    filename = f"{clean_filename(company_name)}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    return f"🔍 {company_name} -> {filename}"
                
            except Exception as e:
                continue
        
        return f"❌ {company_name} - No logo found"

def main():
    # Get the 234 verified missing companies
    with open('/Users/adi/code/socratify/socratify-yolo/final_verified_missing.txt', 'r') as f:
        lines = f.readlines()
    
    # Extract company names (skip header lines)
    missing_companies = []
    for line in lines:
        if line.strip() and line[0].isdigit():
            # Extract company name after the number
            parts = line.strip().split('.', 1)
            if len(parts) > 1:
                company_name = parts[1].strip()
                missing_companies.append(company_name)
    
    output_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Starting download of {len(missing_companies)} verified missing companies...")
    print(f"Output directory: {output_dir}")
    print(f"Using {MAX_WORKERS} parallel workers")
    print("Filenames will be clean company names (no extra noise)\n")
    
    downloaded_count = 0
    failed_count = 0
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # Submit all download tasks
        future_to_company = {
            executor.submit(download_logo, company, output_dir): company 
            for company in missing_companies
        }
        
        # Process completed tasks
        for future in as_completed(future_to_company):
            result = future.result()
            print(result)
            
            if result.startswith("✅") or result.startswith("🔍"):
                downloaded_count += 1
            else:
                failed_count += 1
    
    print(f"\n=== DOWNLOAD COMPLETE ===")
    print(f"Total companies: {len(missing_companies)}")
    print(f"Downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    print(f"Success rate: {(downloaded_count/len(missing_companies)*100):.1f}%")
    
    # Update collection count
    new_total = 8262 + downloaded_count
    print(f"Collection now has approximately: {new_total} logos")

if __name__ == "__main__":
    main()