#!/usr/bin/env python3
import json
import os
import time
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

def clean_filename(name):
    """Clean company name for filename"""
    clean = name.replace('&amp;', 'and').replace('&', 'and')
    clean = re.sub(r'[^\w\s-]', '', clean)
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean.strip('_')

def get_company_domain_variations(company_name):
    """Generate possible domain variations for a company"""
    # Clean the company name
    clean = company_name.lower()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    clean = ' '.join(clean.split())
    
    # Common company name to domain mappings
    domain_mappings = {
        'dhl group deutsche post': ['dhl.com', 'deutschepost.de'],
        'jingdong mall': ['jd.com', 'jingdong.com'],
        'jd logistics': ['jdl.com', 'jd.com'],
        'home depot': ['homedepot.com'],
        'china mobile': ['chinamobileltd.com', 'chinamobile.com'],
        'ahold delhaize': ['aholddelhaize.com'],
        'tjx companies': ['tjx.com'],
        'ntt nippon telegraph': ['ntt.com', 'ntt.co.jp'],
        'x5 retail group': ['x5.ru'],
        'lowes companies': ['lowes.com'],
        'ck hutchison': ['ckh.com.hk'],
        'luxshare precision': ['luxshare-ict.com'],
        'ping an insurance': ['pingan.com'],
        'iss a s': ['issworld.com', 'iss.com'],
        'china unicom': ['chinaunicom.com.cn'],
        'jardine cycle carriage': ['jcclgroup.com'],
        'hca healthcare': ['hcahealthcare.com'],
        'hcl technologies': ['hcltech.com'],
        'japan post': ['japanpost.jp'],
        'loblaw companies': ['loblaw.ca'],
        'george weston': ['weston.ca'],
        'dfi retail group': ['dfiretailgroup.com'],
        'jardine matheson': ['jardines.com'],
        'deutsche telekom': ['telekom.com', 'deutschetelekom.com'],
        'ntt data': ['nttdata.com'],
        'darden restaurants': ['darden.com'],
        'bnp paribas': ['bnpparibas.com'],
        'america movil': ['americamovil.com'],
        'yamato holdings': ['yamato-hd.co.jp'],
        'power construction corporation china': ['powerchina.cn'],
        'picc property casualty': ['epicc.com.cn'],
        'grupo acs': ['grupoacs.com'],
        'schneider electric': ['se.com', 'schneider-electric.com'],
        'forvia': ['forvia.com'],
        'gxo logistics': ['gxo.com'],
        'j t global express': ['jet.co.id'],
        's f express': ['sf-express.com'],
        'genpact': ['genpact.com'],
        'anheuser busch inbev': ['ab-inbev.com'],
        'sainsburys': ['sainsburys.co.uk'],
        'yum china': ['yumchina.com'],
        'h m': ['hm.com', 'hennes-mauritz.com'],
        'johnson johnson': ['jnj.com'],
        'tyson foods': ['tysonfoods.com'],
        'associated british foods': ['abf.co.uk'],
        'china communications construction': ['ccccltd.cn'],
        'hai di lao': ['haidilao.com'],
        'lens technology': ['lenstech.com'],
        'ke holdings': ['ke.com'],
        'muyuan foods': ['muyuanfoods.com'],
        'elior group': ['eliorgroup.com'],
        'koc holding': ['koc.com.tr'],
        'thermo fisher': ['thermofisher.com'],
        'ubm development': ['ubm.at'],
        'dxc technology': ['dxc.com'],
        'jeronimo martins': ['jeronimomartins.com'],
        'abm industries': ['abm.com'],
        'poste italiane': ['poste.it'],
        'itochu': ['itochu.co.jp'],
        'nippon steel': ['nipponsteel.com'],
        'dongfeng motor': ['dfmc.com.cn'],
        'jones lang lasalle': ['jll.com'],
        'societe generale': ['societegenerale.com'],
        'united airlines': ['united.com'],
        'ross stores': ['rossstores.com'],
        'tdk': ['tdk.com'],
        'air china': ['airchina.com.cn'],
        'elevance health': ['elevancehealth.com'],
        'traton': ['traton.com'],
        'life insurance corporation india': ['licindia.in'],
        'first pacific': ['firstpacific.com'],
        'wh group': ['wh-group.com'],
        'boe technology': ['boe.com'],
        'china life insurance': ['chinalife.com.cn'],
        'china southern airlines': ['csair.com'],
        'weichai power': ['weichai.com'],
        'wendel': ['wendelgroup.com'],
        'ase group': ['aseglobal.com'],
        'china pacific insurance': ['cpic.com.cn'],
        'charter communications': ['charter.com'],
        'loreal': ['loreal.com'],
        'macys': ['macys.com'],
        'intesa sanpaolo': ['intesasanpaolo.com'],
        'oreilly automotive': ['oreillyauto.com'],
        'ramsay health care': ['ramsayhealth.com'],
        'pick n pay': ['pnp.co.za'],
        'bim': ['bim.com.tr'],
        'grupo carso': ['carso.com.mx'],
        'kohls': ['kohls.com'],
        'swire pacific': ['swirepacific.com'],
        'sendas distribuidora': ['assai.com.br'],
        'gac guangzhou automobile': ['gacgroup.com.cn'],
        'banco do brasil': ['bb.com.br'],
        'lingyi itech': ['luxshare-ict.com'],
        'china eastern airlines': ['ceair.com'],
        'best buy': ['bestbuy.com'],
        'te connectivity': ['te.com'],
        'great wall motors': ['gwm.com.cn'],
        'minebea mitsumi': ['minebeamitsumi.com']
    }
    
    # Generate variations
    variations = []
    
    # Direct lookup
    for key, domains in domain_mappings.items():
        if key in clean:
            return domains
    
    # Try simple domain construction
    words = clean.split()
    if words:
        # First word
        variations.append(f"{words[0]}.com")
        # All words together
        joined = ''.join(words)
        if len(joined) < 20:
            variations.append(f"{joined}.com")
        # First two words
        if len(words) > 1:
            variations.append(f"{words[0]}{words[1]}.com")
    
    return variations

def try_download_logo(company_name, company_rank):
    """Try to download a logo for a company"""
    domains = get_company_domain_variations(company_name)
    
    for domain in domains:
        url = f"https://logo.clearbit.com/{domain}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and len(response.content) > 100:
                return response.content
        except:
            pass
    
    return None

def download_batch(companies_batch, output_dir):
    """Download a batch of company logos"""
    results = []
    
    for company in companies_batch:
        name = company['original_name']
        rank = company['rank']
        
        logo_data = try_download_logo(name, rank)
        
        if logo_data:
            filename = f"{clean_filename(name)}.png"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(logo_data)
            
            results.append({
                'name': name,
                'rank': rank,
                'status': 'success',
                'filename': filename
            })
        else:
            results.append({
                'name': name,
                'rank': rank,
                'status': 'failed'
            })
    
    return results

def main():
    print("="*70)
    print("DOWNLOADING ALL MISSING LOGOS")
    print("="*70)
    
    # Load missing companies
    with open('missing_logos_fast.json', 'r') as f:
        missing_companies = json.load(f)
    
    # Filter to top 1000 by rank
    top_missing = [c for c in missing_companies if c['rank'] <= 1000]
    top_missing.sort(key=lambda x: x['rank'])
    
    print(f"\nWill attempt to download logos for {len(top_missing)} companies (rank <= 1000)")
    
    # Create output directory
    output_dir = 'downloaded_logos_batch'
    os.makedirs(output_dir, exist_ok=True)
    
    # Download in batches
    batch_size = 10
    all_results = []
    
    print("\nDownloading logos...")
    for i in range(0, len(top_missing), batch_size):
        batch = top_missing[i:i+batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(top_missing) + batch_size - 1) // batch_size
        
        print(f"  Batch {batch_num}/{total_batches}...", end='', flush=True)
        
        results = download_batch(batch, output_dir)
        all_results.extend(results)
        
        success_count = sum(1 for r in results if r['status'] == 'success')
        print(f" {success_count}/{len(batch)} downloaded")
        
        time.sleep(1)  # Rate limiting
    
    # Summary
    successful = [r for r in all_results if r['status'] == 'success']
    failed = [r for r in all_results if r['status'] == 'failed']
    
    print(f"\n{'='*70}")
    print("DOWNLOAD COMPLETE")
    print(f"{'='*70}")
    print(f"Successfully downloaded: {len(successful)} logos")
    print(f"Failed to download: {len(failed)} logos")
    
    # Save results
    with open('download_results.json', 'w') as f:
        json.dump(all_results, f, indent=2)
    
    if successful:
        print(f"\nLogos saved to: {output_dir}/")
        print("\nTo move to main folder, run:")
        print(f"  cp {output_dir}/*.png ../socratify-images/logos/images/companies/")
    
    # Show some failed companies for manual download
    if failed:
        print(f"\nTop 20 companies that need manual download:")
        for company in failed[:20]:
            print(f"  Rank {company['rank']:4d}: {company['name']}")

if __name__ == "__main__":
    main()