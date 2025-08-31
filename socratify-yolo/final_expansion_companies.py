#!/usr/bin/env python3
"""
Final comprehensive expansion - covering ALL remaining gaps
Goal: The most complete employer logo collection possible
"""

# Eastern Europe & Russia
EASTERN_EUROPE_COMPANIES = {
    # Poland
    "PKN Orlen": "orlen.pl",
    "PZU": "pzu.pl",
    "Allegro": "allegro.pl",
    "CD Projekt": "cdprojekt.com",
    "Asseco": "asseco.com",
    "mBank": "mbank.pl",
    "Play": "play.pl",
    "InPost": "inpost.pl",
    "Dino Polska": "grupadino.pl",
    "LPP": "lppsa.com",
    "CCC": "ccc.eu",
    "Cyfrowy Polsat": "grupapolsat.pl",
    
    # Czech Republic
    "Škoda Auto": "skoda-auto.com",
    "ČEZ": "cez.cz",
    "Avast": "avast.com",
    "Komerční banka": "kb.cz",
    "O2 Czech Republic": "o2.cz",
    "Agrofert": "agrofert.cz",
    "PPF Group": "ppf.eu",
    "JetBrains": "jetbrains.com",
    
    # Romania
    "Dacia": "dacia.com",
    "Bitdefender": "bitdefender.com",
    "OMV Petrom": "omvpetrom.com",
    "Banca Transilvania": "bancatransilvania.ro",
    "eMAG": "emag.ro",
    "UiPath": "uipath.com",
    
    # Hungary
    "MOL Group": "molgroup.info",
    "OTP Bank": "otpbank.hu",
    "Richter Gedeon": "richter.hu",
    "Wizz Air": "wizzair.com",
    
    # Russia (Western operations)
    "Yandex": "yandex.com",
    "Kaspersky": "kaspersky.com",
    "Mail.ru Group": "vk.company",
    "Tinkoff": "tinkoff.ru",
    "JetBrains": "jetbrains.com",
    
    # Ukraine
    "EPAM": "epam.com",
    "SoftServe": "softserveinc.com",
    "Luxoft": "luxoft.com",
    "MacPaw": "macpaw.com",
    "Grammarly": "grammarly.com",
    "GitLab": "gitlab.com",
    "Preply": "preply.com",
    
    # Other Eastern Europe
    "Avito": "avito.ru",
    "Revolut": "revolut.com",
    "Wise": "wise.com",
    "Bolt": "bolt.eu",
    "Vinted": "vinted.com"
}

# Nordic Companies
NORDIC_COMPANIES = {
    # Sweden
    "Ericsson": "ericsson.com",
    "Volvo Group": "volvogroup.com",
    "Volvo Cars": "volvocars.com",
    "H&M": "hm.com",
    "IKEA": "ikea.com",
    "Spotify": "spotify.com",
    "Klarna": "klarna.com",
    "Northvolt": "northvolt.com",
    "Sandvik": "sandvik.com",
    "Atlas Copco": "atlascopco.com",
    "ABB": "abb.com",
    "Electrolux": "electrolux.com",
    "SEB": "seb.se",
    "Swedbank": "swedbank.com",
    "Handelsbanken": "handelsbanken.com",
    "Telia": "teliacompany.com",
    "Evolution": "evolution.com",
    "King": "king.com",
    "Mojang": "mojang.com",
    "Paradox Interactive": "paradoxinteractive.com",
    
    # Norway
    "Equinor": "equinor.com",
    "DNB": "dnb.no",
    "Telenor": "telenor.com",
    "Norsk Hydro": "hydro.com",
    "Yara": "yara.com",
    "Orkla": "orkla.com",
    "Aker": "akerasa.com",
    "Schibsted": "schibsted.com",
    "Opera": "opera.com",
    "Kahoot!": "kahoot.com",
    
    # Denmark
    "Maersk": "maersk.com",
    "Novo Nordisk": "novonordisk.com",
    "Carlsberg": "carlsberggroup.com",
    "LEGO": "lego.com",
    "Ørsted": "orsted.com",
    "DSV": "dsv.com",
    "Danske Bank": "danskebank.com",
    "Vestas": "vestas.com",
    "Pandora": "pandoragroup.com",
    "Danfoss": "danfoss.com",
    "ISS": "issworld.com",
    "Coloplast": "coloplast.com",
    "Demant": "demant.com",
    "Unity": "unity.com",
    
    # Finland
    "Nokia": "nokia.com",
    "Kone": "kone.com",
    "Wärtsilä": "wartsila.com",
    "Fortum": "fortum.com",
    "Neste": "neste.com",
    "Stora Enso": "storaenso.com",
    "UPM": "upm.com",
    "Nordea": "nordea.com",
    "Rovio": "rovio.com",
    "Supercell": "supercell.com",
    "Reaktor": "reaktor.com",
    
    # Iceland
    "Össur": "ossur.com",
    "CCP Games": "ccpgames.com",
    "Marel": "marel.com",
    "Arion Bank": "arionbanki.is"
}

# Defense & Aerospace
DEFENSE_AEROSPACE_COMPANIES = {
    # US Defense
    "Lockheed Martin": "lockheedmartin.com",
    "Raytheon Technologies": "rtx.com",
    "Northrop Grumman": "northropgrumman.com",
    "General Dynamics": "gd.com",
    "L3Harris": "l3harris.com",
    "Huntington Ingalls": "huntingtoningalls.com",
    "SAIC": "saic.com",
    "Leidos": "leidos.com",
    "CACI": "caci.com",
    "Booz Allen Hamilton": "boozallen.com",
    "General Atomics": "ga.com",
    "Textron": "textron.com",
    "Oshkosh": "oshkoshdefense.com",
    
    # European Defense
    "BAE Systems": "baesystems.com",
    "Airbus Defence": "airbus.com",
    "Thales": "thalesgroup.com",
    "Leonardo": "leonardo.com",
    "Safran": "safran-group.com",
    "Dassault Aviation": "dassault-aviation.com",
    "Rheinmetall": "rheinmetall.com",
    "Saab": "saab.com",
    "Naval Group": "naval-group.com",
    "MBDA": "mbda-systems.com",
    "Rolls-Royce": "rolls-royce.com",
    "QinetiQ": "qinetiq.com",
    "Babcock": "babcockinternational.com",
    "Ultra Electronics": "ultra.group",
    
    # Aerospace & Space
    "Boeing": "boeing.com",
    "Airbus": "airbus.com",
    "Bombardier": "bombardier.com",
    "Embraer": "embraer.com",
    "Gulfstream": "gulfstream.com",
    "Spirit AeroSystems": "spiritaero.com",
    "Collins Aerospace": "collinsaerospace.com",
    "Honeywell Aerospace": "aerospace.honeywell.com",
    "GE Aviation": "geaviation.com",
    "Pratt & Whitney": "prattwhitney.com",
    "Safran": "safran-group.com",
    "MTU Aero": "mtu.de",
    
    # Space
    "Virgin Galactic": "virgingalactic.com",
    "Axiom Space": "axiomspace.com",
    "Firefly Aerospace": "fireflyspace.com",
    "Rocket Lab": "rocketlabusa.com",
    "Maxar": "maxar.com",
    "Iridium": "iridium.com",
    "SES": "ses.com",
    "Intelsat": "intelsat.com",
    "Astroscale": "astroscale.com",
    "OneWeb": "oneweb.net",
    "Planet Labs": "planet.com",
    "Spire": "spire.com"
}

# Semiconductors & Hardware
SEMICONDUCTOR_HARDWARE_COMPANIES = {
    # Chip Manufacturers
    "TSMC": "tsmc.com",
    "Intel": "intel.com",
    "Samsung Electronics": "samsung.com",
    "Broadcom": "broadcom.com",
    "Qualcomm": "qualcomm.com",
    "NVIDIA": "nvidia.com",
    "AMD": "amd.com",
    "Texas Instruments": "ti.com",
    "Analog Devices": "analog.com",
    "Micron": "micron.com",
    "Marvell": "marvell.com",
    "MediaTek": "mediatek.com",
    "SK Hynix": "skhynix.com",
    "Infineon": "infineon.com",
    "STMicroelectronics": "st.com",
    "NXP": "nxp.com",
    "ON Semiconductor": "onsemi.com",
    "Microchip": "microchip.com",
    "Xilinx": "xilinx.com",
    "Lattice": "latticesemi.com",
    
    # Equipment & Materials
    "ASML": "asml.com",
    "Applied Materials": "appliedmaterials.com",
    "Lam Research": "lamresearch.com",
    "KLA": "kla.com",
    "Tokyo Electron": "tel.com",
    "SCREEN": "screen.co.jp",
    "Advantest": "advantest.com",
    "Teradyne": "teradyne.com",
    "FormFactor": "formfactor.com",
    
    # Hardware & Components
    "Foxconn": "foxconn.com",
    "Flex": "flex.com",
    "Jabil": "jabil.com",
    "Celestica": "celestica.com",
    "Sanmina": "sanmina.com",
    "Benchmark Electronics": "bench.com",
    "TE Connectivity": "te.com",
    "Amphenol": "amphenol.com",
    "Molex": "molex.com",
    "Corning": "corning.com",
    "3M Electronics": "3m.com",
    
    # Storage & Memory
    "Western Digital": "westerndigital.com",
    "Seagate": "seagate.com",
    "NetApp": "netapp.com",
    "Pure Storage": "purestorage.com",
    "Kingston": "kingston.com",
    "Corsair": "corsair.com",
    
    # Networking
    "Cisco": "cisco.com",
    "Arista Networks": "arista.com",
    "Juniper Networks": "juniper.net",
    "Ciena": "ciena.com",
    "F5": "f5.com",
    "Palo Alto Networks": "paloaltonetworks.com",
    "Fortinet": "fortinet.com"
}

# Logistics & Supply Chain
LOGISTICS_SUPPLY_CHAIN_COMPANIES = {
    # Global Logistics
    "DHL": "dhl.com",
    "FedEx": "fedex.com",
    "UPS": "ups.com",
    "DSV": "dsv.com",
    "Kuehne + Nagel": "kuehne-nagel.com",
    "DB Schenker": "dbschenker.com",
    "C.H. Robinson": "chrobinson.com",
    "XPO Logistics": "xpo.com",
    "Expeditors": "expeditors.com",
    "GEODIS": "geodis.com",
    "Nippon Express": "nipponexpress.com",
    "DACHSER": "dachser.com",
    "CEVA Logistics": "cevalogistics.com",
    "Panalpina": "panalpina.com",
    "Agility": "agility.com",
    
    # Shipping & Freight
    "Maersk": "maersk.com",
    "MSC": "msc.com",
    "CMA CGM": "cma-cgm.com",
    "Hapag-Lloyd": "hapag-lloyd.com",
    "ONE": "one-line.com",
    "Evergreen": "evergreen-line.com",
    "COSCO": "cosco-shipping.com",
    "Yang Ming": "yangming.com",
    "ZIM": "zim.com",
    
    # Last Mile & E-commerce
    "Amazon Logistics": "logistics.amazon.com",
    "Deliverr": "deliverr.com",
    "ShipBob": "shipbob.com",
    "Flexport": "flexport.com",
    "Freightos": "freightos.com",
    "project44": "project44.com",
    "FourKites": "fourkites.com",
    "Convoy": "convoy.com",
    "Uber Freight": "uberfreight.com",
    "Sennder": "sennder.com",
    
    # Warehousing
    "Prologis": "prologis.com",
    "GLP": "glp.com",
    "Americold": "americold.com",
    "Lineage Logistics": "lineagelogistics.com",
    "NFI": "nfiindustries.com"
}

# Insurance Companies
INSURANCE_COMPANIES = {
    # Global Insurance
    "Allianz": "allianz.com",
    "AXA": "axa.com",
    "Ping An": "pingan.com",
    "China Life": "chinalife.com.cn",
    "Zurich": "zurich.com",
    "Munich Re": "munichre.com",
    "Swiss Re": "swissre.com",
    "Generali": "generali.com",
    "Prudential": "prudential.com",
    "MetLife": "metlife.com",
    "AIG": "aig.com",
    "Chubb": "chubb.com",
    "Travelers": "travelers.com",
    "Hartford": "thehartford.com",
    "Liberty Mutual": "libertymutual.com",
    "Allstate": "allstate.com",
    "Progressive": "progressive.com",
    "State Farm": "statefarm.com",
    "GEICO": "geico.com",
    "USAA": "usaa.com",
    
    # Reinsurance
    "Lloyd's of London": "lloyds.com",
    "Berkshire Hathaway Re": "bhre.com",
    "Hannover Re": "hannover-re.com",
    "SCOR": "scor.com",
    "PartnerRe": "partnerre.com",
    "Everest Re": "everestre.com",
    "RenaissanceRe": "renre.com",
    
    # Life & Health
    "Aflac": "aflac.com",
    "Principal": "principal.com",
    "Guardian Life": "guardianlife.com",
    "MassMutual": "massmutual.com",
    "New York Life": "newyorklife.com",
    "Northwestern Mutual": "northwesternmutual.com",
    "John Hancock": "johnhancock.com",
    "Lincoln Financial": "lfg.com",
    "Voya": "voya.com",
    
    # InsurTech
    "Lemonade": "lemonade.com",
    "Root": "root.com",
    "Hippo": "hippo.com",
    "Next Insurance": "nextinsurance.com",
    "Clearcover": "clearcover.com",
    "Metromile": "metromile.com",
    "Haven Life": "havenlife.com",
    "Ethos": "ethoslife.com"
}

# Emerging Tech Companies
EMERGING_TECH_COMPANIES = {
    # Quantum Computing
    "IBM Quantum": "quantum-computing.ibm.com",
    "Rigetti": "rigetti.com",
    "IonQ": "ionq.com",
    "D-Wave": "dwavesys.com",
    "PsiQuantum": "psiquantum.com",
    "Xanadu": "xanadu.ai",
    "Quantum Computing Inc": "quantumcomputinginc.com",
    "Oxford Quantum": "oxfordquantumcircuits.com",
    "Atom Computing": "atom-computing.com",
    
    # Robotics & Automation
    "Boston Dynamics": "bostondynamics.com",
    "Fanuc": "fanuc.com",
    "ABB Robotics": "new.abb.com/products/robotics",
    "KUKA": "kuka.com",
    "Universal Robots": "universal-robots.com",
    "Intuitive Surgical": "intuitive.com",
    "iRobot": "irobot.com",
    "Zebra Technologies": "zebra.com",
    "Cognex": "cognex.com",
    "Teradyne": "teradyne.com",
    "Brooks Automation": "brooks.com",
    "Omron": "omron.com",
    "Yaskawa": "yaskawa.com",
    "Kawasaki Robotics": "kawasakirobotics.com",
    
    # Drones & Autonomous
    "DJI": "dji.com",
    "Zipline": "flyzipline.com",
    "Wing": "wing.com",
    "Skydio": "skydio.com",
    "Volocopter": "volocopter.com",
    "Joby Aviation": "joby.aero",
    "Lilium": "lilium.com",
    "Archer": "archer.com",
    "Beta Technologies": "beta.team",
    "Wisk": "wisk.aero",
    
    # AR/VR/Metaverse
    "Magic Leap": "magicleap.com",
    "Varjo": "varjo.com",
    "Pico Interactive": "pico-interactive.com",
    "Nreal": "nreal.ai",
    "Vuzix": "vuzix.com",
    "RealWear": "realwear.com",
    "Matterport": "matterport.com",
    "Spatial": "spatial.io",
    "Rec Room": "recroom.com",
    "VRChat": "vrchat.com",
    
    # Biotech & Synthetic Biology
    "Ginkgo Bioworks": "ginkgobioworks.com",
    "Zymergen": "zymergen.com",
    "Synthetic Genomics": "syntheticgenomics.com",
    "Twist Bioscience": "twistbioscience.com",
    "Inscripta": "inscripta.com",
    "Mammoth Biosciences": "mammothbiosciences.com",
    "Synthego": "synthego.com",
    "Culture Biosciences": "culturebiosciences.com",
    
    # Clean Tech & Energy Storage
    "QuantumScape": "quantumscape.com",
    "SolidPower": "solidpowerbattery.com",
    "Sila Nanotechnologies": "silanano.com",
    "Northvolt": "northvolt.com",
    "CATL": "catl.com",
    "BYD Battery": "byd.com",
    "LG Energy Solution": "lgensol.com",
    "SK Innovation": "skinnovation.com",
    "Fluence": "fluenceenergy.com",
    "ESS Inc": "essinc.com"
}

# Regional Champions & Specialized
REGIONAL_CHAMPIONS = {
    # Southeast Asia
    "GoTo": "gotocompany.com",
    "Bukalapak": "bukalapak.com",
    "Traveloka": "traveloka.com",
    "Tiket.com": "tiket.com",
    "Blibli": "blibli.com",
    "Bank Mandiri": "bankmandiri.co.id",
    "Bank Central Asia": "bca.co.id",
    "Telkom Indonesia": "telkom.co.id",
    "Pertamina": "pertamina.com",
    "Garuda Indonesia": "garuda-indonesia.com",
    "Siam Cement": "scg.com",
    "Bangkok Bank": "bangkokbank.com",
    "Kasikornbank": "kasikornbank.com",
    "VinGroup": "vingroup.net",
    "Viettel": "viettel.com.vn",
    "FPT": "fpt.com.vn",
    "VietJet": "vietjetair.com",
    "Petronas": "petronas.com",
    "Maybank": "maybank.com",
    "CIMB": "cimb.com",
    "Public Bank": "publicbank.com.my",
    
    # India Additional
    "Vedanta": "vedanta.com",
    "Sun Pharma": "sunpharma.com",
    "Godrej": "godrej.com",
    "Aditya Birla": "adityabirla.com",
    "Zee Entertainment": "zee.com",
    "Jubilant": "jubilantindustries.com",
    "Pidilite": "pidilite.com",
    "Marico": "marico.com",
    "Dabur": "dabur.com",
    "Britannia": "britannia.co.in",
    "Dream11": "dream11.com",
    "Razorpay": "razorpay.com",
    "Zerodha": "zerodha.com",
    "Pine Labs": "pinelabs.com",
    "Billdesk": "billdesk.com",
    "PolicyBazaar": "policybazaar.com",
    "Nykaa": "nykaa.com",
    "Udaan": "udaan.com",
    "Delhivery": "delhivery.com",
    "Rivigo": "rivigo.com",
    
    # China Additional
    "DJI": "dji.com",
    "Anker": "anker.com",
    "OnePlus": "oneplus.com",
    "Hisense": "hisense.com",
    "TCL": "tcl.com",
    "Midea": "midea.com",
    "Gree": "gree.com",
    "Haier": "haier.com",
    "Geely": "geely.com",
    "Great Wall Motors": "gwm.com.cn",
    "SAIC Motor": "saicmotor.com",
    "GAC Group": "gac.com.cn",
    "Fosun": "fosun.com",
    "Wanda": "wanda.com",
    "Dalian Wanda": "wandagroup.com",
    "Country Garden": "countrygarden.com.cn",
    "Vanke": "vanke.com",
    "Poly Group": "poly.com.cn",
    
    # Middle East Additional
    "Careem": "careem.com",
    "Noon": "noon.com",
    "Talabat": "talabat.com",
    "Aramex": "aramex.com",
    "Emirates NBD": "emiratesnbd.com",
    "Souq": "souq.com",
    "Fetchr": "fetchr.us",
    "Namshi": "namshi.com",
    "Wadi": "wadi.com",
    "Awok": "awok.com",
    "Dubizzle": "dubizzle.com",
    "Bayut": "bayut.com",
    "Property Finder": "propertyfinder.ae",
    "Kitopi": "kitopi.com",
    "Anghami": "anghami.com",
    "Shahid": "shahid.net",
    
    # Africa Additional
    "Sasol": "sasol.com",
    "Shoprite": "shoprite.co.za",
    "Pick n Pay": "pnp.co.za",
    "Woolworths SA": "woolworths.co.za",
    "Bidvest": "bidvest.com",
    "Remgro": "remgro.com",
    "Steinhoff": "steinhoff.com",
    "Telkom SA": "telkom.co.za",
    "Cell C": "cellc.co.za",
    "Rain": "rain.co.za",
    "Safaricom": "safaricom.co.ke",
    "Liquid Telecom": "liquid.tech",
    "IHS Towers": "ihstowers.com",
    "Kobo360": "kobo360.com",
    "54gene": "54gene.com",
    "mPharma": "mpharma.com",
    "Zipline": "flyzipline.com",
    "Twiga Foods": "twiga.com",
    "MarketForce": "marketforce.com"
}

# Alternative Investments & Specialized Finance
ALTERNATIVE_INVESTMENTS = {
    # Alternative Asset Managers
    "Oaktree Capital": "oaktreecapital.com",
    "Ares Management": "aresmgmt.com",
    "Brookfield Asset Management": "brookfield.com",
    "Fortress Investment": "fortress.com",
    "Blue Owl Capital": "blueowl.com",
    "StepStone Group": "stepstonegroup.com",
    "Hamilton Lane": "hamiltonlane.com",
    "Partners Group": "partnersgroup.com",
    "Investcorp": "investcorp.com",
    "Tikehau Capital": "tikehaucapital.com",
    
    # Credit Funds
    "Cerberus": "cerberus.com",
    "Angelo Gordon": "angelogordon.com",
    "PIMCO": "pimco.com",
    "DoubleLine": "doubleline.com",
    "TCW": "tcw.com",
    "Western Asset": "westernasset.com",
    "Oaktree": "oaktreecapital.com",
    "GSO Capital": "gsocap.com",
    "Benefit Street Partners": "benefitstreetpartners.com",
    
    # Real Estate Investment
    "Starwood Capital": "starwoodcapital.com",
    "Colony Capital": "clnc.com",
    "Tishman Speyer": "tishmanspeyer.com",
    "Related Companies": "related.com",
    "Hines": "hines.com",
    "JBG Smith": "jbgsmith.com",
    "AvalonBay": "avalonbay.com",
    "Equity Residential": "equityresidential.com",
    "Prologis": "prologis.com",
    
    # Infrastructure Funds
    "Global Infrastructure Partners": "global-infra.com",
    "IFM Investors": "ifminvestors.com",
    "Stonepeak": "stonepeakpartners.com",
    "DigitalBridge": "digitalbridge.com",
    "Antin": "antin-ip.com",
    "EQT Infrastructure": "eqtgroup.com",
    "First Sentier": "firstsentierinvestors.com",
    
    # Sovereign Wealth Funds
    "Norway GPFG": "nbim.no",
    "China Investment Corporation": "china-inv.cn",
    "ADIA": "adia.ae",
    "Kuwait Investment Authority": "kia.gov.kw",
    "GIC Singapore": "gic.com.sg",
    "Qatar Investment Authority": "qia.qa",
    "Public Investment Fund": "pif.gov.sa",
    "Mubadala": "mubadala.com",
    "Khazanah": "khazanah.com.my",
    "Future Fund": "futurefund.gov.au"
}

# Creator Economy & B2B SaaS
CREATOR_ECONOMY_B2B = {
    # Creator Platforms
    "Substack": "substack.com",
    "Patreon": "patreon.com",
    "OnlyFans": "onlyfans.com",
    "Cameo": "cameo.com",
    "Teachable": "teachable.com",
    "Thinkific": "thinkific.com",
    "Podia": "podia.com",
    "Gumroad": "gumroad.com",
    "Ko-fi": "ko-fi.com",
    "Buy Me a Coffee": "buymeacoffee.com",
    "ConvertKit": "convertkit.com",
    "Ghost": "ghost.org",
    "Circle": "circle.so",
    "Mighty Networks": "mightynetworks.com",
    "Kajabi": "kajabi.com",
    "Memberful": "memberful.com",
    "Discord": "discord.com",
    "Geneva": "geneva.com",
    
    # B2B SaaS
    "Salesforce": "salesforce.com",
    "ServiceNow": "servicenow.com",
    "Workday": "workday.com",
    "Snowflake": "snowflake.com",
    "Databricks": "databricks.com",
    "Palantir": "palantir.com",
    "Splunk": "splunk.com",
    "Elastic": "elastic.co",
    "Confluent": "confluent.io",
    "MongoDB": "mongodb.com",
    "Cockroach Labs": "cockroachlabs.com",
    "Hashicorp": "hashicorp.com",
    "GitLab": "gitlab.com",
    "JFrog": "jfrog.com",
    "CircleCI": "circleci.com",
    "Travis CI": "travis-ci.com",
    "Buildkite": "buildkite.com",
    
    # Collaboration Tools
    "Slack": "slack.com",
    "Zoom": "zoom.us",
    "Teams": "teams.microsoft.com",
    "Asana": "asana.com",
    "Trello": "trello.com",
    "Jira": "atlassian.com",
    "Confluence": "atlassian.com",
    "Basecamp": "basecamp.com",
    "Smartsheet": "smartsheet.com",
    "Wrike": "wrike.com",
    "ClickUp": "clickup.com",
    "Todoist": "todoist.com",
    "Any.do": "any.do",
    
    # Marketing & Sales Tech
    "HubSpot": "hubspot.com",
    "Marketo": "marketo.com",
    "Pardot": "pardot.com",
    "Eloqua": "eloqua.com",
    "Drift": "drift.com",
    "Intercom": "intercom.com",
    "Zendesk": "zendesk.com",
    "Freshworks": "freshworks.com",
    "Pipedrive": "pipedrive.com",
    "Close": "close.com",
    "Copper": "copper.com",
    "Outreach": "outreach.io",
    "SalesLoft": "salesloft.com",
    "Gong": "gong.io",
    "Chorus": "chorus.ai",
    "Clari": "clari.com"
}

# Impact & ESG Companies
IMPACT_ESG_COMPANIES = {
    # Certified B Corps
    "Patagonia": "patagonia.com",
    "Ben & Jerry's": "benjerry.com",
    "Warby Parker": "warbyparker.com",
    "Allbirds": "allbirds.com",
    "Bombas": "bombas.com",
    "Seventh Generation": "seventhgeneration.com",
    "Method": "methodproducts.com",
    "Eileen Fisher": "eileenfisher.com",
    "Natura": "natura.com.br",
    "The Body Shop": "thebodyshop.com",
    "Kickstarter": "kickstarter.com",
    "Etsy": "etsy.com",
    "King Arthur Baking": "kingarthurbaking.com",
    "New Belgium Brewing": "newbelgium.com",
    "Danone North America": "danonenorthamerica.com",
    
    # Impact Investing
    "Generation Investment": "generationim.com",
    "LeapFrog Investments": "leapfroginvest.com",
    "Acumen": "acumen.org",
    "Root Capital": "rootcapital.org",
    "BlueOrchard": "blueorchard.com",
    "Triodos Bank": "triodos.com",
    "DOEN Foundation": "doen.nl",
    "Omidyar Network": "omidyar.com",
    "Bridges Fund Management": "bridgesfundmanagement.com",
    "Social Finance": "socialfinance.org.uk",
    
    # Clean Energy Leaders
    "Ørsted": "orsted.com",
    "NextEra Energy": "nexteraenergy.com",
    "Enel Green Power": "enelgreenpower.com",
    "EDP Renewables": "edpr.com",
    "Acciona": "acciona.com",
    "Brookfield Renewable": "brookfieldrenewable.com",
    "Pattern Energy": "patternenergy.com",
    "Innergex": "innergex.com",
    "Boralex": "boralex.com",
    "Voltalia": "voltalia.com",
    
    # Sustainable Brands
    "Tesla": "tesla.com",
    "Beyond Meat": "beyondmeat.com",
    "Impossible Foods": "impossiblefoods.com",
    "Oatly": "oatly.com",
    "Too Good To Go": "toogoodtogo.com",
    "Ecosia": "ecosia.org",
    "Fairphone": "fairphone.com",
    "Framework": "frame.work",
    "Grove Collaborative": "grove.co",
    "Who Gives A Crap": "whogivesacrap.org"
}

# Crypto & Web3 Infrastructure
CRYPTO_WEB3_COMPANIES = {
    # Exchanges & Trading
    "Binance": "binance.com",
    "Coinbase": "coinbase.com",
    "Kraken": "kraken.com",
    "Gemini": "gemini.com",
    "Bitstamp": "bitstamp.net",
    "Bitfinex": "bitfinex.com",
    "OKX": "okx.com",
    "Bybit": "bybit.com",
    "Gate.io": "gate.io",
    "KuCoin": "kucoin.com",
    "Crypto.com": "crypto.com",
    "eToro": "etoro.com",
    "Robinhood Crypto": "robinhood.com",
    
    # Infrastructure
    "ConsenSys": "consensys.net",
    "Alchemy": "alchemy.com",
    "Infura": "infura.io",
    "QuickNode": "quicknode.com",
    "Moralis": "moralis.io",
    "Chainlink": "chain.link",
    "The Graph": "thegraph.com",
    "Filecoin": "filecoin.io",
    "Arweave": "arweave.org",
    
    # DeFi
    "Uniswap": "uniswap.org",
    "Aave": "aave.com",
    "Compound": "compound.finance",
    "MakerDAO": "makerdao.com",
    "Curve": "curve.fi",
    "Yearn": "yearn.finance",
    "Synthetix": "synthetix.io",
    "dYdX": "dydx.exchange",
    "1inch": "1inch.io",
    
    # Custody & Security
    "Fireblocks": "fireblocks.com",
    "Anchorage Digital": "anchorage.com",
    "BitGo": "bitgo.com",
    "Ledger": "ledger.com",
    "Trezor": "trezor.io",
    "Casa": "casa.io",
    "Copper": "copper.co",
    "Hex Trust": "hextrust.com",
    
    # Enterprise Blockchain
    "Ripple": "ripple.com",
    "Stellar": "stellar.org",
    "R3": "r3.com",
    "Digital Asset": "digitalasset.com",
    "Hyperledger": "hyperledger.org",
    "Hedera": "hedera.com",
    "Avalanche": "avax.network",
    "Polygon": "polygon.technology",
    "Arbitrum": "arbitrum.io",
    "Optimism": "optimism.io",
    
    # NFT & Gaming
    "OpenSea": "opensea.io",
    "Rarible": "rarible.com",
    "SuperRare": "superrare.com",
    "Nifty Gateway": "niftygateway.com",
    "Axie Infinity": "axieinfinity.com",
    "The Sandbox": "sandbox.game",
    "Decentraland": "decentraland.org",
    "Immutable": "immutable.com",
    "Dapper Labs": "dapperlabs.com",
    "Sorare": "sorare.com",
    
    # Funds & Investment
    "Digital Currency Group": "dcg.co",
    "Galaxy Digital": "galaxydigital.io",
    "Pantera Capital": "panteracapital.com",
    "Polychain Capital": "polychain.capital",
    "Paradigm": "paradigm.xyz",
    "a16z crypto": "a16zcrypto.com",
    "Framework Ventures": "framework.ventures",
    "Multicoin Capital": "multicoin.capital",
    "Three Arrows Capital": "threearrowscap.com",
    "Jump Crypto": "jumpcrypto.com"
}

def get_all_final_expansion_companies():
    """Return all companies from final expansion"""
    all_companies = {}
    all_companies.update(EASTERN_EUROPE_COMPANIES)
    all_companies.update(NORDIC_COMPANIES)
    all_companies.update(DEFENSE_AEROSPACE_COMPANIES)
    all_companies.update(SEMICONDUCTOR_HARDWARE_COMPANIES)
    all_companies.update(LOGISTICS_SUPPLY_CHAIN_COMPANIES)
    all_companies.update(INSURANCE_COMPANIES)
    all_companies.update(EMERGING_TECH_COMPANIES)
    all_companies.update(REGIONAL_CHAMPIONS)
    all_companies.update(ALTERNATIVE_INVESTMENTS)
    all_companies.update(CREATOR_ECONOMY_B2B)
    all_companies.update(IMPACT_ESG_COMPANIES)
    all_companies.update(CRYPTO_WEB3_COMPANIES)
    return all_companies

if __name__ == "__main__":
    all_companies = get_all_final_expansion_companies()
    print(f"Eastern Europe: {len(EASTERN_EUROPE_COMPANIES)}")
    print(f"Nordic: {len(NORDIC_COMPANIES)}")
    print(f"Defense & Aerospace: {len(DEFENSE_AEROSPACE_COMPANIES)}")
    print(f"Semiconductors & Hardware: {len(SEMICONDUCTOR_HARDWARE_COMPANIES)}")
    print(f"Logistics & Supply Chain: {len(LOGISTICS_SUPPLY_CHAIN_COMPANIES)}")
    print(f"Insurance: {len(INSURANCE_COMPANIES)}")
    print(f"Emerging Tech: {len(EMERGING_TECH_COMPANIES)}")
    print(f"Regional Champions: {len(REGIONAL_CHAMPIONS)}")
    print(f"Alternative Investments: {len(ALTERNATIVE_INVESTMENTS)}")
    print(f"Creator Economy & B2B: {len(CREATOR_ECONOMY_B2B)}")
    print(f"Impact & ESG: {len(IMPACT_ESG_COMPANIES)}")
    print(f"Crypto & Web3: {len(CRYPTO_WEB3_COMPANIES)}")
    print(f"\nTOTAL FINAL EXPANSION: {len(all_companies)}")