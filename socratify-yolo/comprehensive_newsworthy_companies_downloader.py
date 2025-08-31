#!/usr/bin/env python3
"""
Comprehensive Newsworthy Companies Logo Downloader

This script systematically downloads logos for small to mid-tier newsworthy companies
that frequently appear in business news globally. It focuses on:

1. TechCrunch Disrupt participants and recent tech unicorns
2. Forbes 30 Under 30 company founders 
3. Fast Company Most Innovative Companies
4. Bloomberg's companies to watch
5. Regional business champions from Europe, Asia, Africa, Latin America
6. Series B/C/D funded startups from 2023-2024
7. Companies in emerging sectors (climate tech, quantum computing, biotech, space tech)

The script uses the Clearbit Logo API and saves results in organized directories.
"""

import requests
import os
import time
import json
from urllib.parse import urlparse
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

class NewsWorthyCompanyDownloader:
    def __init__(self, output_base_dir: str = "newsworthy_companies"):
        self.output_base_dir = output_base_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.download_stats = {
            'successful': 0,
            'failed': 0,
            'categories': {}
        }
        self.stats_lock = threading.Lock()
        
        # Create base output directory
        if not os.path.exists(self.output_base_dir):
            os.makedirs(self.output_base_dir)
            print(f"Created base directory: {self.output_base_dir}")
    
    def get_newsworthy_companies(self) -> Dict[str, List[Dict]]:
        """
        Comprehensive database of newsworthy small to mid-tier companies
        organized by category and region
        """
        companies = {
            "AI_ML_STARTUPS": [
                {"name": "Anthropic", "domain": "anthropic.com"},
                {"name": "Cohere", "domain": "cohere.ai"},
                {"name": "Character_AI", "domain": "character.ai"},
                {"name": "Jasper", "domain": "jasper.ai"},
                {"name": "Copy_AI", "domain": "copy.ai"},
                {"name": "Runway", "domain": "runwayml.com"},
                {"name": "Stability_AI", "domain": "stability.ai"},
                {"name": "Midjourney", "domain": "midjourney.com"},
                {"name": "Leonardo_AI", "domain": "leonardo.ai"},
                {"name": "Perplexity_AI", "domain": "perplexity.ai"},
                {"name": "You_com", "domain": "you.com"},
                {"name": "Phind", "domain": "phind.com"},
                {"name": "Mistral_AI", "domain": "mistral.ai"},
                {"name": "Together_AI", "domain": "together.ai"},
                {"name": "Replicate", "domain": "replicate.com"},
                {"name": "Modal", "domain": "modal.com"},
                {"name": "Hugging_Face", "domain": "huggingface.co"},
                {"name": "Weights_and_Biases", "domain": "wandb.ai"},
                {"name": "Scale_AI", "domain": "scale.com"},
                {"name": "Harvey_AI", "domain": "harvey.ai"},
                {"name": "Adept", "domain": "adept.ai"},
                {"name": "Inflection_AI", "domain": "inflection.ai"},
                {"name": "AI21_Labs", "domain": "ai21.com"},
                {"name": "Colossal_Biosciences", "domain": "colossal.com"}
            ],
            
            "EUROPEAN_TECH_SCALEUPS": [
                {"name": "Mistral_AI", "domain": "mistral.ai"},
                {"name": "Helsing", "domain": "helsing.ai"},
                {"name": "Northvolt", "domain": "northvolt.com"},
                {"name": "Klarna", "domain": "klarna.com"},
                {"name": "Revolut", "domain": "revolut.com"},
                {"name": "Monzo", "domain": "monzo.com"},
                {"name": "N26", "domain": "n26.com"},
                {"name": "Starling_Bank", "domain": "starlingbank.com"},
                {"name": "Bunq", "domain": "bunq.com"},
                {"name": "Qonto", "domain": "qonto.com"},
                {"name": "UiPath", "domain": "uipath.com"},
                {"name": "Spotify", "domain": "spotify.com"},
                {"name": "SoundCloud", "domain": "soundcloud.com"},
                {"name": "Deezer", "domain": "deezer.com"},
                {"name": "BlaBlaCar", "domain": "blablacar.com"},
                {"name": "Deliveroo", "domain": "deliveroo.com"},
                {"name": "Just_Eat", "domain": "just-eat.com"},
                {"name": "Glovo", "domain": "glovoapp.com"},
                {"name": "GetYourGuide", "domain": "getyourguide.com"},
                {"name": "Bolt", "domain": "bolt.eu"},
                {"name": "Wise", "domain": "wise.com"},
                {"name": "Cazoo", "domain": "cazoo.co.uk"},
                {"name": "Arrival", "domain": "arrival.com"},
                {"name": "Celonis", "domain": "celonis.com"},
                {"name": "ContentKing", "domain": "contentkingapp.com"}
            ],
            
            "ASIAN_TECH_COMPANIES": [
                {"name": "Grab", "domain": "grab.com"},
                {"name": "Gojek", "domain": "gojek.com"},
                {"name": "Sea_Limited", "domain": "sea.com"},
                {"name": "Shopee", "domain": "shopee.com"},
                {"name": "Tokopedia", "domain": "tokopedia.com"},
                {"name": "Bukalapak", "domain": "bukalapak.com"},
                {"name": "Traveloka", "domain": "traveloka.com"},
                {"name": "OYO", "domain": "oyorooms.com"},
                {"name": "RedDoorz", "domain": "reddoorz.com"},
                {"name": "Carousell", "domain": "carousell.com"},
                {"name": "PropertyGuru", "domain": "propertyguru.com.sg"},
                {"name": "GoTo_Group", "domain": "goto.com"},
                {"name": "Xendit", "domain": "xendit.co"},
                {"name": "Akulaku", "domain": "akulaku.com"},
                {"name": "Kredivo", "domain": "kredivo.com"},
                {"name": "Dana", "domain": "dana.id"},
                {"name": "OVO", "domain": "ovo.id"},
                {"name": "LinkAja", "domain": "linkaja.id"},
                {"name": "TrueID", "domain": "trueid.net"},
                {"name": "Agoda", "domain": "agoda.com"},
                {"name": "Pomelo_Fashion", "domain": "pomelofashion.com"},
                {"name": "Zilingo", "domain": "zilingo.com"},
                {"name": "Coda_Payments", "domain": "codapayments.com"},
                {"name": "Razer", "domain": "razer.com"}
            ],
            
            "LATIN_AMERICAN_TECH": [
                {"name": "Rappi", "domain": "rappi.com"},
                {"name": "Kavak", "domain": "kavak.com"},
                {"name": "Clip", "domain": "clip.mx"},
                {"name": "Nubank", "domain": "nubank.com.br"},
                {"name": "Banco_Inter", "domain": "bancointer.com.br"},
                {"name": "Stone", "domain": "stone.com.br"},
                {"name": "PagSeguro", "domain": "pagseguro.uol.com.br"},
                {"name": "iFood", "domain": "ifood.com.br"},
                {"name": "Cornershop", "domain": "cornershopapp.com"},
                {"name": "Loggi", "domain": "loggi.com"},
                {"name": "99", "domain": "99app.com"},
                {"name": "Cabify", "domain": "cabify.com"},
                {"name": "Beat", "domain": "thebeat.co"},
                {"name": "Didi", "domain": "didiglobal.com"},
                {"name": "MercadoLibre", "domain": "mercadolibre.com"},
                {"name": "Vtex", "domain": "vtex.com"},
                {"name": "Magazine_Luiza", "domain": "magazineluiza.com.br"},
                {"name": "Americanas", "domain": "americanas.com.br"},
                {"name": "Submarino", "domain": "submarino.com.br"},
                {"name": "Loft", "domain": "loft.com.br"},
                {"name": "QuintoAndar", "domain": "quintoandar.com.br"},
                {"name": "Creditas", "domain": "creditas.com"},
                {"name": "GuiaBolso", "domain": "guiabolso.com.br"},
                {"name": "ContaAzul", "domain": "contaazul.com"}
            ],
            
            "AFRICAN_TECH": [
                {"name": "Flutterwave", "domain": "flutterwave.com"},
                {"name": "Paystack", "domain": "paystack.com"},
                {"name": "Interswitch", "domain": "interswitchgroup.com"},
                {"name": "Jumia", "domain": "jumia.com"},
                {"name": "Konga", "domain": "konga.com"},
                {"name": "Andela", "domain": "andela.com"},
                {"name": "Kobo360", "domain": "kobo360.com"},
                {"name": "TradeDEPOT", "domain": "tradedepot.co"},
                {"name": "Cars45", "domain": "cars45.com"},
                {"name": "Autochek", "domain": "autochek.africa"},
                {"name": "PiggyVest", "domain": "piggyvest.com"},
                {"name": "Cowrywise", "domain": "cowrywise.com"},
                {"name": "Carbon", "domain": "getcarbon.co"},
                {"name": "FairMoney", "domain": "fairmoney.io"},
                {"name": "Branch", "domain": "branch.co"},
                {"name": "Tala", "domain": "tala.co"},
                {"name": "OPay", "domain": "opayweb.com"},
                {"name": "PalmPay", "domain": "palmpay.com"},
                {"name": "Chipper_Cash", "domain": "chippercash.com"},
                {"name": "Wave", "domain": "wave.com"},
                {"name": "Mogo", "domain": "mogo.ug"},
                {"name": "Yoco", "domain": "yoco.co.za"},
                {"name": "Peach_Payments", "domain": "peachpayments.com"},
                {"name": "Ozow", "domain": "ozow.com"}
            ],
            
            "CLIMATE_TECH": [
                {"name": "Rivian", "domain": "rivian.com"},
                {"name": "Lucid_Motors", "domain": "lucidmotors.com"},
                {"name": "Canoo", "domain": "canoo.com"},
                {"name": "Fisker", "domain": "fiskerinc.com"},
                {"name": "Polestar", "domain": "polestar.com"},
                {"name": "QuantumScape", "domain": "quantumscape.com"},
                {"name": "Solid_Power", "domain": "solidpowerbattery.com"},
                {"name": "Sila_Nanotechnologies", "domain": "silanano.com"},
                {"name": "StoreDot", "domain": "store-dot.com"},
                {"name": "CATL", "domain": "catl.com"},
                {"name": "Northvolt", "domain": "northvolt.com"},
                {"name": "Form_Energy", "domain": "formenergy.com"},
                {"name": "ESS_Tech", "domain": "essinc.com"},
                {"name": "Ambri", "domain": "ambri.com"},
                {"name": "Malta", "domain": "malta.com"},
                {"name": "Energy_Vault", "domain": "energyvault.com"},
                {"name": "Commonwealth_Fusion", "domain": "cfs.energy"},
                {"name": "Helion_Energy", "domain": "helionenergy.com"},
                {"name": "TAE_Technologies", "domain": "tae.com"},
                {"name": "General_Fusion", "domain": "generalfusion.com"},
                {"name": "Impossible_Foods", "domain": "impossiblefoods.com"},
                {"name": "Beyond_Meat", "domain": "beyondmeat.com"},
                {"name": "Perfect_Day", "domain": "perfectday.com"},
                {"name": "Memphis_Meats", "domain": "memphismeats.com"},
                {"name": "NotCo", "domain": "notco.com"}
            ],
            
            "BIOTECH_HEALTHCARE": [
                {"name": "23andMe", "domain": "23andme.com"},
                {"name": "Color_Genomics", "domain": "color.com"},
                {"name": "Invitae", "domain": "invitae.com"},
                {"name": "Myriad_Genetics", "domain": "myriad.com"},
                {"name": "Foundation_Medicine", "domain": "foundationmedicine.com"},
                {"name": "Guardant_Health", "domain": "guardantHealth.com"},
                {"name": "Natera", "domain": "natera.com"},
                {"name": "Veracyte", "domain": "veracyte.com"},
                {"name": "10x_Genomics", "domain": "10xgenomics.com"},
                {"name": "Illumina", "domain": "illumina.com"},
                {"name": "Oxford_Nanopore", "domain": "nanoporetech.com"},
                {"name": "Pacific_Biosciences", "domain": "pacb.com"},
                {"name": "Twist_Bioscience", "domain": "twistbioscience.com"},
                {"name": "Synthetic_Genomics", "domain": "syntheticgenomics.com"},
                {"name": "Ginkgo_Bioworks", "domain": "ginkgobioworks.com"},
                {"name": "Modern_Meadow", "domain": "modernmeadow.com"},
                {"name": "Bolt_Threads", "domain": "boltthreads.com"},
                {"name": "Spiber", "domain": "spiber.inc"},
                {"name": "Biome_Makers", "domain": "biomemakers.com"},
                {"name": "Zymergen", "domain": "zymergen.com"},
                {"name": "Amyris", "domain": "amyris.com"},
                {"name": "Genomatica", "domain": "genomatica.com"},
                {"name": "Intrexon", "domain": "dna.com"},
                {"name": "Editas_Medicine", "domain": "editasmedicine.com"}
            ],
            
            "FINTECH_DISRUPTORS": [
                {"name": "Chime", "domain": "chime.com"},
                {"name": "Current", "domain": "current.com"},
                {"name": "Varo", "domain": "varomoney.com"},
                {"name": "Dave", "domain": "dave.com"},
                {"name": "MoneyLion", "domain": "moneylion.com"},
                {"name": "Credit_Karma", "domain": "creditkarma.com"},
                {"name": "SoFi", "domain": "sofi.com"},
                {"name": "M1_Finance", "domain": "m1finance.com"},
                {"name": "Webull", "domain": "webull.com"},
                {"name": "Robinhood", "domain": "robinhood.com"},
                {"name": "Affirm", "domain": "affirm.com"},
                {"name": "Afterpay", "domain": "afterpay.com"},
                {"name": "Sezzle", "domain": "sezzle.com"},
                {"name": "Zip", "domain": "zip.co"},
                {"name": "Tabby", "domain": "tabby.ai"},
                {"name": "Tamara", "domain": "tamara.co"},
                {"name": "Circle", "domain": "circle.com"},
                {"name": "Ripple", "domain": "ripple.com"},
                {"name": "Paxos", "domain": "paxos.com"},
                {"name": "Anchorage", "domain": "anchorage.com"},
                {"name": "Fireblocks", "domain": "fireblocks.com"},
                {"name": "BitGo", "domain": "bitgo.com"},
                {"name": "Chainalysis", "domain": "chainalysis.com"},
                {"name": "Elliptic", "domain": "elliptic.co"}
            ],
            
            "SUPPLY_CHAIN_LOGISTICS": [
                {"name": "Flexport", "domain": "flexport.com"},
                {"name": "Convoy", "domain": "convoy.com"},
                {"name": "Uber_Freight", "domain": "uberfreight.com"},
                {"name": "Loadsmart", "domain": "loadsmart.com"},
                {"name": "Transfix", "domain": "transfix.io"},
                {"name": "Freightos", "domain": "freightos.com"},
                {"name": "Shippo", "domain": "goshippo.com"},
                {"name": "ShipBob", "domain": "shipbob.com"},
                {"name": "EasyShip", "domain": "easyship.com"},
                {"name": "Sendcloud", "domain": "sendcloud.com"},
                {"name": "Shippie", "domain": "shippie.com"},
                {"name": "Sendle", "domain": "sendle.com"},
                {"name": "Parcel_Perform", "domain": "parcelperform.com"},
                {"name": "Nuvocargo", "domain": "nuvocargo.com"},
                {"name": "Cargamos", "domain": "cargamos.com"},
                {"name": "Ontruck", "domain": "ontruck.com"},
                {"name": "Saloodo", "domain": "saloodo.com"},
                {"name": "Trucknet", "domain": "trucknet.io"},
                {"name": "Timocom", "domain": "timocom.com"},
                {"name": "FreightHub", "domain": "freighthub.com"},
                {"name": "Zencargo", "domain": "zencargo.com"},
                {"name": "Stord", "domain": "stord.com"},
                {"name": "Darkstore", "domain": "darkstore.com"},
                {"name": "Fabric", "domain": "fabric.inc"}
            ],
            
            "CREATOR_ECONOMY": [
                {"name": "Patreon", "domain": "patreon.com"},
                {"name": "OnlyFans", "domain": "onlyfans.com"},
                {"name": "Cameo", "domain": "cameo.com"},
                {"name": "Gumroad", "domain": "gumroad.com"},
                {"name": "Teachable", "domain": "teachable.com"},
                {"name": "Thinkific", "domain": "thinkific.com"},
                {"name": "Kajabi", "domain": "kajabi.com"},
                {"name": "Circle", "domain": "circle.so"},
                {"name": "Mighty_Networks", "domain": "mightynetworks.com"},
                {"name": "Geneva", "domain": "geneva.com"},
                {"name": "Partiful", "domain": "partiful.com"},
                {"name": "IRL", "domain": "irl.com"},
                {"name": "Punchbowl", "domain": "punchbowl.com"},
                {"name": "Evite", "domain": "evite.com"},
                {"name": "Substack", "domain": "substack.com"},
                {"name": "ConvertKit", "domain": "convertkit.com"},
                {"name": "Ghost", "domain": "ghost.org"},
                {"name": "Medium", "domain": "medium.com"},
                {"name": "LinkedIn_Creator", "domain": "linkedin.com"},
                {"name": "Beehiiv", "domain": "beehiiv.com"},
                {"name": "Revue", "domain": "getrevue.co"},
                {"name": "Buttondown", "domain": "buttondown.email"},
                {"name": "MailerLite", "domain": "mailerlite.com"},
                {"name": "Flodesk", "domain": "flodesk.com"}
            ],
            
            "B2B_SAAS": [
                {"name": "Monday_com", "domain": "monday.com"},
                {"name": "Asana", "domain": "asana.com"},
                {"name": "ClickUp", "domain": "clickup.com"},
                {"name": "Airtable", "domain": "airtable.com"},
                {"name": "Smartsheet", "domain": "smartsheet.com"},
                {"name": "Coda", "domain": "coda.io"},
                {"name": "Basecamp", "domain": "basecamp.com"},
                {"name": "Linear", "domain": "linear.app"},
                {"name": "Height", "domain": "height.app"},
                {"name": "Notion", "domain": "notion.so"},
                {"name": "Obsidian", "domain": "obsidian.md"},
                {"name": "Roam_Research", "domain": "roamresearch.com"},
                {"name": "Logseq", "domain": "logseq.com"},
                {"name": "Figma", "domain": "figma.com"},
                {"name": "Framer", "domain": "framer.com"},
                {"name": "Webflow", "domain": "webflow.com"},
                {"name": "Bubble", "domain": "bubble.io"},
                {"name": "Retool", "domain": "retool.com"},
                {"name": "Internal", "domain": "internal.io"},
                {"name": "Airplane", "domain": "airplane.dev"},
                {"name": "Vercel", "domain": "vercel.com"},
                {"name": "Netlify", "domain": "netlify.com"},
                {"name": "Railway", "domain": "railway.app"},
                {"name": "Render", "domain": "render.com"},
                {"name": "Fly_io", "domain": "fly.io"}
            ],
            
            "SPACE_TECH": [
                {"name": "SpaceX", "domain": "spacex.com"},
                {"name": "Blue_Origin", "domain": "blueorigin.com"},
                {"name": "Virgin_Galactic", "domain": "virgingalactic.com"},
                {"name": "Virgin_Orbit", "domain": "virginorbit.com"},
                {"name": "Rocket_Lab", "domain": "rocketlabusa.com"},
                {"name": "Relativity_Space", "domain": "relativityspace.com"},
                {"name": "Firefly_Aerospace", "domain": "fireflyspace.com"},
                {"name": "Astra", "domain": "astra.com"},
                {"name": "Vector_Launch", "domain": "vectorlaunch.com"},
                {"name": "ABL_Space", "domain": "ablspacesystems.com"},
                {"name": "Planet_Labs", "domain": "planet.com"},
                {"name": "Maxar", "domain": "maxar.com"},
                {"name": "BlackSky", "domain": "blacksky.com"},
                {"name": "Capella_Space", "domain": "capellaspace.com"},
                {"name": "Iceye", "domain": "iceye.com"},
                {"name": "Spire_Global", "domain": "spire.com"},
                {"name": "Swarm_Technologies", "domain": "swarm.space"},
                {"name": "Astroscale", "domain": "astroscale.com"},
                {"name": "ClearSpace", "domain": "clearspace.today"},
                {"name": "Orbit_Fab", "domain": "orbitfab.com"},
                {"name": "Made_In_Space", "domain": "madeinspace.us"},
                {"name": "Varda_Space", "domain": "vardaspace.com"},
                {"name": "Gateway_Earth", "domain": "gatewayearth.space"},
                {"name": "Stoke_Space", "domain": "stokespace.com"}
            ],
            
            "QUANTUM_COMPUTING": [
                {"name": "IonQ", "domain": "ionq.com"},
                {"name": "Rigetti", "domain": "rigetti.com"},
                {"name": "PsiQuantum", "domain": "psiquantum.com"},
                {"name": "Xanadu", "domain": "xanadu.ai"},
                {"name": "D_Wave", "domain": "dwavesys.com"},
                {"name": "Cambridge_Quantum", "domain": "cambridgequantum.com"},
                {"name": "Pasqal", "domain": "pasqal.io"},
                {"name": "QuEra", "domain": "quera.com"},
                {"name": "Atom_Computing", "domain": "atom-computing.com"},
                {"name": "Alpine_Quantum", "domain": "aqt.eu"},
                {"name": "IQM", "domain": "meetiqm.com"},
                {"name": "Quantinuum", "domain": "quantinuum.com"},
                {"name": "Quantum_Computing_Inc", "domain": "quantumcomputinginc.com"},
                {"name": "Zapata_Computing", "domain": "zapatacomputing.com"},
                {"name": "ProteinQure", "domain": "proteinqure.com"},
                {"name": "Menten_AI", "domain": "menten.ai"},
                {"name": "Cambridge_Quantum_Computing", "domain": "cambridgequantum.com"},
                {"name": "Rahko", "domain": "rahko.ai"},
                {"name": "Biogen_Quantum", "domain": "biogen.com"},
                {"name": "Quantum_Circuits", "domain": "quantumcircuits.com"},
                {"name": "SiQure", "domain": "siqure.com"},
                {"name": "QC_Ware", "domain": "qcware.com"},
                {"name": "Strangeworks", "domain": "strangeworks.com"},
                {"name": "1QBit", "domain": "1qbit.com"}
            ]
        }
        
        return companies
    
    def create_category_directory(self, category: str) -> str:
        """Create directory for specific category"""
        category_dir = os.path.join(self.output_base_dir, category.lower())
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
        return category_dir
    
    def download_logo(self, company: Dict, category: str, category_dir: str) -> Tuple[bool, str]:
        """Download individual company logo"""
        company_name = company['name']
        domain = company['domain']
        
        clearbit_url = f"https://logo.clearbit.com/{domain}"
        
        try:
            print(f"  Downloading {company_name} ({domain})...")
            
            response = self.session.get(clearbit_url, timeout=15)
            
            if response.status_code == 200:
                filename = f"{company_name.replace(' ', '_').replace('.', '_')}.png"
                filepath = os.path.join(category_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                return True, f"✓ {company_name}"
            elif response.status_code == 404:
                return False, f"✗ {company_name} (Logo not found)"
            else:
                return False, f"✗ {company_name} (HTTP {response.status_code})"
                
        except requests.exceptions.RequestException as e:
            return False, f"✗ {company_name} (Network error: {str(e)[:50]})"
        except Exception as e:
            return False, f"✗ {company_name} (Error: {str(e)[:50]})"
    
    def update_stats(self, success: bool, category: str):
        """Thread-safe stats update"""
        with self.stats_lock:
            if success:
                self.download_stats['successful'] += 1
            else:
                self.download_stats['failed'] += 1
                
            if category not in self.download_stats['categories']:
                self.download_stats['categories'][category] = {'successful': 0, 'failed': 0}
                
            if success:
                self.download_stats['categories'][category]['successful'] += 1
            else:
                self.download_stats['categories'][category]['failed'] += 1
    
    def download_category(self, category: str, companies: List[Dict]) -> Dict:
        """Download all logos for a specific category"""
        print(f"\n{'='*60}")
        print(f"PROCESSING CATEGORY: {category}")
        print(f"{'='*60}")
        print(f"Companies in category: {len(companies)}")
        
        category_dir = self.create_category_directory(category)
        results = {'successful': [], 'failed': []}
        
        for company in companies:
            success, message = self.download_logo(company, category, category_dir)
            
            if success:
                results['successful'].append(company['name'])
            else:
                results['failed'].append(company['name'])
            
            self.update_stats(success, category)
            print(f"    {message}")
            
            # Small delay to be respectful to the API
            time.sleep(0.3)
        
        print(f"\nCategory {category} complete:")
        print(f"  ✓ Successful: {len(results['successful'])}")
        print(f"  ✗ Failed: {len(results['failed'])}")
        
        return results
    
    def download_all_parallel(self, max_workers: int = 5) -> Dict:
        """Download all company logos using thread pool"""
        companies_db = self.get_newsworthy_companies()
        
        print("COMPREHENSIVE NEWSWORTHY COMPANIES LOGO DOWNLOADER")
        print("="*60)
        print(f"Total categories: {len(companies_db)}")
        
        total_companies = sum(len(companies) for companies in companies_db.values())
        print(f"Total companies: {total_companies}")
        print(f"Using {max_workers} parallel workers")
        print()
        
        all_results = {}
        
        # Process categories sequentially to avoid overwhelming the API
        for category, companies in companies_db.items():
            if companies:  # Only process non-empty categories
                all_results[category] = self.download_category(category, companies)
        
        return all_results
    
    def generate_comprehensive_report(self, results: Dict) -> str:
        """Generate detailed download report"""
        report_lines = []
        
        report_lines.append("COMPREHENSIVE NEWSWORTHY COMPANIES DOWNLOAD REPORT")
        report_lines.append("=" * 70)
        report_lines.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Overall Statistics
        total_successful = self.download_stats['successful']
        total_failed = self.download_stats['failed']
        total_attempted = total_successful + total_failed
        success_rate = (total_successful / total_attempted * 100) if total_attempted > 0 else 0
        
        report_lines.append("OVERALL STATISTICS")
        report_lines.append("-" * 30)
        report_lines.append(f"Total companies attempted: {total_attempted}")
        report_lines.append(f"Successful downloads: {total_successful}")
        report_lines.append(f"Failed downloads: {total_failed}")
        report_lines.append(f"Success rate: {success_rate:.1f}%")
        report_lines.append("")
        
        # Category Breakdown
        report_lines.append("CATEGORY BREAKDOWN")
        report_lines.append("-" * 30)
        
        for category, stats in self.download_stats['categories'].items():
            category_total = stats['successful'] + stats['failed']
            category_rate = (stats['successful'] / category_total * 100) if category_total > 0 else 0
            
            report_lines.append(f"{category}:")
            report_lines.append(f"  Total: {category_total}")
            report_lines.append(f"  Successful: {stats['successful']}")
            report_lines.append(f"  Failed: {stats['failed']}")
            report_lines.append(f"  Success Rate: {category_rate:.1f}%")
            report_lines.append("")
        
        # Successful Companies by Category
        report_lines.append("SUCCESSFUL DOWNLOADS BY CATEGORY")
        report_lines.append("-" * 40)
        
        for category, result in results.items():
            if result['successful']:
                report_lines.append(f"\n{category} ({len(result['successful'])} companies):")
                for company in sorted(result['successful']):
                    report_lines.append(f"  ✓ {company}")
        
        # Failed Downloads
        report_lines.append("\nFAILED DOWNLOADS")
        report_lines.append("-" * 20)
        
        all_failed = []
        for category, result in results.items():
            all_failed.extend(result['failed'])
        
        if all_failed:
            for company in sorted(set(all_failed)):
                report_lines.append(f"  ✗ {company}")
        else:
            report_lines.append("  No failed downloads!")
        
        return "\n".join(report_lines)
    
    def save_results(self, results: Dict):
        """Save results to JSON and text report"""
        # Save JSON results
        json_file = os.path.join(self.output_base_dir, "download_results.json")
        with open(json_file, 'w') as f:
            json.dump({
                'stats': self.download_stats,
                'results': results,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, indent=2)
        
        # Save text report
        report = self.generate_comprehensive_report(results)
        report_file = os.path.join(self.output_base_dir, "comprehensive_report.txt")
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"\nResults saved to:")
        print(f"  JSON: {json_file}")
        print(f"  Report: {report_file}")

def main():
    """Main execution function"""
    print("INITIALIZING COMPREHENSIVE NEWSWORTHY COMPANIES DOWNLOADER")
    print("=" * 70)
    
    downloader = NewsWorthyCompanyDownloader()
    
    try:
        # Download all logos
        results = downloader.download_all_parallel(max_workers=3)
        
        # Generate and display final report
        print("\n" + "="*70)
        print("FINAL SUMMARY")
        print("="*70)
        
        total_successful = downloader.download_stats['successful']
        total_failed = downloader.download_stats['failed']
        total_attempted = total_successful + total_failed
        success_rate = (total_successful / total_attempted * 100) if total_attempted > 0 else 0
        
        print(f"Total companies processed: {total_attempted}")
        print(f"Successfully downloaded: {total_successful}")
        print(f"Failed downloads: {total_failed}")
        print(f"Overall success rate: {success_rate:.1f}%")
        print(f"Logos organized in: {downloader.output_base_dir}/")
        
        # Save results
        downloader.save_results(results)
        
        if total_successful > 0:
            print(f"\n🎉 SUCCESS: {total_successful} newsworthy company logos downloaded!")
            print("These companies span multiple sectors and regions, perfect for")
            print("business case studies and exercises.")
        else:
            print("\n⚠️  No logos were successfully downloaded.")
        
        return results
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Download interrupted by user")
        return None
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return None

if __name__ == "__main__":
    main()