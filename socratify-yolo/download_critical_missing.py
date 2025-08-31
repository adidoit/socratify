#!/usr/bin/env python3
import os
import requests
import time

# Critical missing companies from top 100 with their likely domains
critical_companies = [
    ("DHL_Group", ["dhl.com", "deutschepost.de", "dpdhl.com"]),
    ("Jingdong_Mall", ["jd.com", "jingdong.com", "jdcloud.com"]),
    ("JD_Logistics", ["jdl.com", "jd.com"]),
    ("United_Parcel_Service", ["ups.com", "upsc.com"]),
    ("Home_Depot", ["homedepot.com", "thd.com"]),
    ("China_Mobile", ["chinamobile.com", "chinamobileltd.com", "10086.cn"]),
    ("Agricultural_Bank_of_China", ["abchina.com", "abcchina.com", "agbank.com"]),
    ("FEMSA", ["femsa.com", "femsa.com.mx", "oxxo.com"]),
    ("Berkshire_Hathaway", ["berkshirehathaway.com", "brk.com", "brkdirect.com"]),
    ("Ahold_Delhaize", ["aholddelhaize.com", "ahold.com", "delhaize.com"]),
    ("China_Construction_Bank", ["ccb.com", "ccb.com.cn", "ccb-intl.com"]),
    ("TJX_Companies", ["tjx.com", "tjmaxx.com", "marshalls.com"]),
    ("China_State_Construction", ["cscec.com", "cscec.com.cn"]),
    ("NTT", ["ntt.com", "ntt.co.jp", "nttdocomo.co.jp"]),
    ("Securitas", ["securitas.com", "securitasusa.com"]),
    ("X5_Retail_Group", ["x5.ru", "pyaterochka.ru", "perekrestok.ru"]),
    ("Lowes", ["lowes.com", "lowescompanies.com"]),
    ("CK_Hutchison", ["ckh.com.hk", "ckhutchison.com"]),
    ("Luxshare_Precision", ["luxshare-ict.com", "luxshare.com.cn"]),
    ("Ping_An", ["pingan.com", "pingan.com.cn", "pingan.cn"]),
    ("ISS", ["issworld.com", "iss.com", "us.issworld.com"]),
    ("Brookfield", ["brookfield.com", "brookfieldproperties.com"]),
    ("China_Unicom", ["chinaunicom.com", "chinaunicom.com.cn", "10010.com"]),
    ("Jardine_Cycle_Carriage", ["jcclgroup.com", "cyclecarriage.com"]),
    ("Walmex", ["walmex.mx", "walmart.com.mx"]),
    ("HCA_Healthcare", ["hcahealthcare.com", "hca.com"]),
    ("HCL_Technologies", ["hcltech.com", "hcl.com"]),
    ("Japan_Post", ["japanpost.jp", "post.japanpost.jp"]),
    ("Loblaw", ["loblaw.ca", "loblaws.ca"]),
    ("George_Weston", ["weston.ca", "georgeweston.com"]),
    ("DFI_Retail", ["dfiretailgroup.com", "dairyfarminternational.com"]),
    ("Jardine_Matheson", ["jardines.com", "jardinematheson.com"]),
    ("Deutsche_Telekom", ["telekom.com", "telekom.de", "t-mobile.com"])
]

def download_logo(name, domains):
    """Try to download logo from multiple domain options"""
    for domain in domains:
        url = f"https://logo.clearbit.com/{domain}"
        try:
            print(f"  Trying {domain}...", end='')
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            })
            if response.status_code == 200 and len(response.content) > 100:
                print(" ✓ Success!")
                return response.content
            else:
                print(" ✗ Not found")
        except Exception as e:
            print(f" ✗ Error: {e}")
    return None

def main():
    print("="*70)
    print("DOWNLOADING CRITICAL MISSING LOGOS (TOP 100)")
    print("="*70)
    
    output_dir = "critical_logos"
    os.makedirs(output_dir, exist_ok=True)
    
    downloaded = []
    failed = []
    
    for name, domains in critical_companies:
        print(f"\n{name}:")
        logo_data = download_logo(name, domains)
        
        if logo_data:
            filepath = os.path.join(output_dir, f"{name}.png")
            with open(filepath, 'wb') as f:
                f.write(logo_data)
            downloaded.append(name)
        else:
            failed.append(name)
        
        time.sleep(0.5)  # Rate limiting
    
    print(f"\n{'='*70}")
    print("RESULTS:")
    print(f"  ✓ Downloaded: {len(downloaded)}/{len(critical_companies)}")
    print(f"  ✗ Failed: {len(failed)}/{len(critical_companies)}")
    
    if downloaded:
        print(f"\nSuccessfully downloaded:")
        for name in downloaded:
            print(f"  • {name}")
        print(f"\nTo move to main folder:")
        print(f"  cp {output_dir}/*.png ../socratify-images/logos/images/companies/")
    
    if failed:
        print(f"\nFailed to download (need manual download):")
        for name in failed:
            print(f"  • {name}")

if __name__ == "__main__":
    main()