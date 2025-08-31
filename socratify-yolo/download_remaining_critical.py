#!/usr/bin/env python3
import csv
import os
import requests
import time
import re

# Read the complete unmatched list and focus on top 1000
def clean_filename(name):
    """Clean company name for filename"""
    clean = name.replace('&amp;', 'and').replace('&', 'and')
    clean = re.sub(r'[^\w\s-]', '', clean)
    clean = re.sub(r'[-\s]+', '_', clean)
    return clean.strip('_')

def get_domain_variations(company_name):
    """Get possible domains for a company"""
    # Special mappings for known companies
    mappings = {
        'JD Logistics': ['jdl.com', 'jd.com', 'jdwl.com'],
        'X5 Retail Group': ['x5.ru', 'x5group.ru'],
        'CK Hutchison Holdings': ['ckh.com.hk', 'ckhutchison.com'],
        'HCA Healthcare': ['hcahealthcare.com', 'hca.com'],
        'DFI Retail Group': ['dfiretailgroup.com', 'dairyfarminternational.com'],
        'BNP Paribas': ['bnpparibas.com', 'bnpparibas.fr'],
        'PICC Property and Casualty': ['epicc.com.cn', 'picc.com.cn'],
        'GXO Logistics': ['gxo.com', 'gxologistics.com'],
        'J&T Global Express': ['jet.co.id', 'jtexpress.com'],
        'S.F. Express': ['sf-express.com', 'sf-international.com'],
        'Rio Tinto': ['riotinto.com'],
        'Dai-ichi Life': ['dai-ichi-life.co.jp', 'dai-ichi.co.jp'],
        'RaiaDrogasil': ['rd.com.br', 'raiadrogasil.com.br'],
        'Huaneng Power': ['hpi.com.cn', 'huaneng.com'],
        'Zijin Mining': ['zijinmining.com', 'zjky.cn'],
        # Add more top companies
        'Groupe ACS': ['grupoacs.com', 'acs.es'],
        'Forvia SE': ['forvia.com', 'faurecia.com'],
        'Elior Group': ['eliorgroup.com', 'elior.com'],
        'Jones Lang LaSalle': ['jll.com', 'joneslanglasalle.com'],
        'Société Générale': ['societegenerale.com', 'socgen.com'],
        'BOE Technology': ['boe.com', 'boe.com.cn'],
        'Weichai Power': ['weichai.com', 'weichaipower.com'],
        'Wendel': ['wendelgroup.com', 'wendel.fr'],
        'ASE Group': ['aseglobal.com', 'asekh.com.tw'],
        "L'Oréal": ['loreal.com', 'loreal-paris.com'],
        'Intesa Sanpaolo': ['intesasanpaolo.com', 'intesasanpaolo.it'],
        "O'Reilly Automotive": ['oreillyauto.com', 'oreilly.com'],
        'Ramsay Health Care': ['ramsayhealth.com', 'ramsayhealth.com.au'],
        'Pick n Pay': ['pnp.co.za', 'picknpay.com'],
        'BİM Birleşik Mağazalar': ['bim.com.tr', 'bimmarket.com'],
        'Grupo Carso': ['carso.com.mx', 'gcarso.com.mx'],
        'Swire Pacific': ['swirepacific.com', 'swire.com'],
        'Sendas Distribuidora': ['assai.com.br', 'gpabr.com'],
        'GAC': ['gacgroup.com.cn', 'gac.com.cn'],
        'Banco do Brasil': ['bb.com.br', 'bancodobrasil.com.br'],
        'Lingyi iTECH': ['luxshare-ict.com', 'lingyiitech.com'],
        'China Eastern Airlines': ['ceair.com', 'ce-air.com'],
        'TE Connectivity': ['te.com', 'teconnectivity.com'],
        'Great Wall Motors': ['gwm.com.cn', 'gwm-global.com'],
        'MinebeaMitsumi': ['minebeamitsumi.com', 'minebea.co.jp'],
        'Itōchū Shōji': ['itochu.co.jp', 'itochu.com'],
        'Nippon Steel': ['nipponsteel.com', 'nssmc.com'],
        'Dongfeng Motor': ['dfmc.com.cn', 'dongfeng-motor.com'],
        'TDK': ['tdk.com', 'tdk.co.jp'],
        'Air China': ['airchina.com.cn', 'airchina.com'],
        'Elevance Health': ['elevancehealth.com', 'anthem.com'],
        'Traton': ['traton.com'],
        'Life Insurance Corporation': ['licindia.in', 'lic.in'],
        'First Pacific': ['firstpacific.com', 'firstpacific.com.hk'],
        'WH Group': ['wh-group.com', 'smithfieldfoods.com'],
        'China Life Insurance': ['chinalife.com.cn', 'e-chinalife.com'],
        'China Southern Airlines': ['csair.com', 'cs-air.com'],
        'China Pacific Insurance': ['cpic.com.cn', 'cpicglobal.com'],
        'Charter Communications': ['charter.com', 'spectrum.com'],
        "Macy's": ['macys.com', 'macysinc.com'],
        "Kohl's": ['kohls.com', 'kohlscorporation.com']
    }
    
    # Check if we have a specific mapping
    for key, domains in mappings.items():
        if key in company_name or company_name in key:
            return domains
    
    # Generic domain generation
    clean = company_name.lower()
    clean = re.sub(r'[^\w\s]', ' ', clean)
    words = clean.split()
    
    domains = []
    if words:
        # Try first word
        domains.append(f"{words[0]}.com")
        # Try all words combined
        combined = ''.join(words)
        if len(combined) < 30:
            domains.append(f"{combined}.com")
    
    return domains

def download_logo(company_name):
    """Try to download a logo"""
    domains = get_domain_variations(company_name)
    
    for domain in domains:
        url = f"https://logo.clearbit.com/{domain}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200 and len(response.content) > 100:
                return response.content
        except:
            pass
    
    return None

def main():
    print("="*80)
    print("DOWNLOADING REMAINING CRITICAL LOGOS")
    print("="*80)
    
    # Read the unmatched companies
    critical_companies = []
    
    # Manually add the top 100 that are still missing
    top_missing = [
        (11, "JD Logistics", "China"),
        (43, "X5 Retail Group", "Netherlands"),
        (53, "CK Hutchison Holdings", "Hong Kong"),
        (80, "HCA Healthcare", "United States"),
        (89, "DFI Retail Group", "Hong Kong"),
        (115, "BNP Paribas", "France"),
        (129, "PICC Property and Casualty Company Limited", "China"),
        (145, "GXO Logistics", "United States"),
        (147, "J&T Global Express", "China"),
        (151, "S.F. Express", "China"),
        # Add more from top 500
        (165, "China Communications Construction", "China"),
        (167, "Lens Technology", "China"),
        (176, "Koç Holding", "Turkey"),
        (198, "Jerónimo Martins", "Portugal"),
        (211, "Itōchū Shōji", "Japan"),
        (220, "Société Générale", "France"),
        (244, "Air China", "China"),
        (271, "BOE Technology", "China"),
        (277, "Weichai Power", "China"),
        (281, "Wendel", "France"),
        (283, "ASE Group", "Taiwan"),
        (297, "L'Oréal", "France"),
        (300, "Macy's", "United States"),
        (303, "Intesa Sanpaolo", "Italy"),
        (304, "O'Reilly Automotive", "United States"),
        (315, "Ramsay Health Care", "Australia"),
        (317, "Pick n Pay Stores", "South Africa"),
        (322, "BİM Birleşik Mağazalar", "Turkey"),
        (323, "Grupo Carso", "Mexico"),
        (324, "Kohl's", "United States"),
        (325, "Swire Pacific", "Hong Kong"),
        (326, "Sendas Distribuidora (Assaí Atacadista)", "Brazil"),
        (330, "GAC (Guangzhou Automobile Group)", "China"),
        (332, "Banco do Brasil", "Brazil"),
        (333, "Lingyi iTECH", "China"),
        (334, "China Eastern Airlines", "China"),
        (336, "TE Connectivity", "Switzerland"),
        (337, "Great Wall Motors", "China"),
        (341, "MinebeaMitsumi", "Japan"),
        (361, "Bolloré", "France"),
        (365, "Crédit Agricole", "France"),
        (378, "Kühne + Nagel", "Switzerland"),
        (391, "Seiko Epson Corporation", "Japan"),
        (419, "Becton Dickinson", "United States"),
        (440, "New Oriental", "China"),
        (441, "PKN Orlen", "Poland"),
        (445, "Tingyi (master kang)", "China"),
        (450, "Hapvida", "Brazil"),
        (508, "Rio Tinto", "United Kingdom"),
        (514, "Dai-ichi Life Holdings", "Japan"),
        (524, "RaiaDrogasil", "Brazil"),
        (525, "Huaneng Power International", "China"),
        (532, "Zijin Mining", "China")
    ]
    
    output_dir = "final_missing_logos"
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"\nWill attempt to download {len(top_missing)} critical missing logos\n")
    
    downloaded = []
    failed = []
    
    for rank, name, country in top_missing:
        print(f"[Rank {rank}] {name}...", end=' ')
        
        logo_data = download_logo(name)
        
        if logo_data:
            filename = f"{clean_filename(name)}.png"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(logo_data)
            print("✓")
            downloaded.append((rank, name))
        else:
            print("✗")
            failed.append((rank, name, country))
        
        time.sleep(0.5)
    
    print(f"\n{'='*80}")
    print("RESULTS:")
    print(f"Downloaded: {len(downloaded)}/{len(top_missing)}")
    print(f"Failed: {len(failed)}/{len(top_missing)}")
    
    if downloaded:
        print(f"\n✓ Successfully downloaded {len(downloaded)} logos:")
        for rank, name in downloaded:
            print(f"   {rank:3d}. {name}")
        print(f"\nTo move to main folder:")
        print(f"  cp {output_dir}/*.png ../socratify-images/logos/images/companies/")
    
    if failed:
        print(f"\n✗ Failed to download {len(failed)} logos:")
        for rank, name, country in failed[:20]:
            print(f"   {rank:3d}. {name} ({country})")

if __name__ == "__main__":
    main()