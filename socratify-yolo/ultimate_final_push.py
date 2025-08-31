#!/usr/bin/env python3
"""
Ultimate final push - Getting EVERYTHING we missed
Making this the most complete collection possible
"""

# Major Global Law Firms
LAW_FIRMS = {
    # US Elite
    "Cravath Swaine & Moore": "cravath.com",
    "Wachtell Lipton": "wlrk.com",
    "Sullivan & Cromwell": "sullcrom.com",
    "Davis Polk": "davispolk.com",
    "Simpson Thacher": "stblaw.com",
    "Skadden": "skadden.com",
    "Latham & Watkins": "lw.com",
    "Kirkland & Ellis": "kirkland.com",
    "Gibson Dunn": "gibsondunn.com",
    "Sidley Austin": "sidley.com",
    "White & Case": "whitecase.com",
    "Cleary Gottlieb": "clearygottlieb.com",
    "Paul Weiss": "paulweiss.com",
    "Debevoise & Plimpton": "debevoise.com",
    "Shearman & Sterling": "shearman.com",
    "Milbank": "milbank.com",
    "Willkie Farr": "willkie.com",
    "Fried Frank": "friedfrank.com",
    "Proskauer Rose": "proskauer.com",
    "Cooley": "cooley.com",
    "Wilson Sonsini": "wsgr.com",
    "Fenwick & West": "fenwick.com",
    "Morrison & Foerster": "mofo.com",
    "O'Melveny": "omm.com",
    "Paul Hastings": "paulhastings.com",
    "Ropes & Gray": "ropesgray.com",
    "Goodwin Procter": "goodwinlaw.com",
    "WilmerHale": "wilmerhale.com",
    "Weil Gotshal": "weil.com",
    "Jones Day": "jonesday.com",
    "Baker McKenzie": "bakermckenzie.com",
    "DLA Piper": "dlapiper.com",
    "Dentons": "dentons.com",
    "Norton Rose Fulbright": "nortonrosefulbright.com",
    "Hogan Lovells": "hoganlovells.com",
    "Reed Smith": "reedsmith.com",
    "Mayer Brown": "mayerbrown.com",
    "McDermott Will & Emery": "mwe.com",
    "Winston & Strawn": "winston.com",
    "Perkins Coie": "perkinscoie.com",
    "Quinn Emanuel": "quinnemanuel.com",
    
    # UK Magic Circle
    "Allen & Overy": "allenovery.com",
    "Clifford Chance": "cliffordchance.com",
    "Freshfields": "freshfields.com",
    "Linklaters": "linklaters.com",
    "Slaughter and May": "slaughterandmay.com",
    
    # Other UK/Europe
    "Herbert Smith Freehills": "herbertsmithfreehills.com",
    "Ashurst": "ashurst.com",
    "CMS": "cms.law",
    "Eversheds Sutherland": "eversheds-sutherland.com",
    "Pinsent Masons": "pinsentmasons.com",
    "Bird & Bird": "twobirds.com",
    "Simmons & Simmons": "simmons-simmons.com"
}

# Food & Agriculture
FOOD_AGRICULTURE = {
    # ABCD Traders
    "Cargill": "cargill.com",
    "ADM": "adm.com",
    "Bunge": "bunge.com",
    "Louis Dreyfus": "ldc.com",
    "COFCO": "cofco.com",
    "Glencore Agriculture": "glencore.com",
    "Olam": "olamgroup.com",
    "Wilmar": "wilmar-international.com",
    
    # Meat & Protein
    "Tyson Foods": "tysonfoods.com",
    "JBS USA": "jbssa.com",
    "Smithfield Foods": "smithfieldfoods.com",
    "Hormel": "hormel.com",
    "Perdue": "perdue.com",
    "Sanderson Farms": "sandersonfarms.com",
    "Pilgrim's Pride": "pilgrims.com",
    "Maple Leaf Foods": "mapleleaffoods.com",
    "BRF": "brf-global.com",
    "WH Group": "wh-group.com",
    
    # Seeds & Crop Science
    "Bayer Crop Science": "cropscience.bayer.com",
    "Corteva": "corteva.com",
    "Syngenta": "syngenta.com",
    "BASF Agricultural": "agriculture.basf.com",
    "FMC": "fmc.com",
    "Nutrien": "nutrien.com",
    "Mosaic": "mosaicco.com",
    "CF Industries": "cfindustries.com",
    "Yara": "yara.com",
    
    # Food Distribution
    "Sysco": "sysco.com",
    "US Foods": "usfoods.com",
    "Performance Food Group": "pfgc.com",
    "Gordon Food Service": "gfs.com",
    "McLane": "mclaneco.com",
    "Core-Mark": "core-mark.com",
    
    # Dairy & Beverages
    "Fonterra": "fonterra.com",
    "Arla Foods": "arla.com",
    "FrieslandCampina": "frieslandcampina.com",
    "Dean Foods": "deanfoods.com",
    "Lactalis": "lactalis.com",
    "Dairy Farmers of America": "dfamilk.com"
}

# Accounting Beyond Big 4
ACCOUNTING_FIRMS = {
    "Grant Thornton": "grantthornton.com",
    "BDO": "bdo.com",
    "RSM": "rsm.global",
    "Mazars": "mazars.com",
    "Crowe": "crowe.com",
    "Baker Tilly": "bakertilly.com",
    "PKF": "pkf.com",
    "Smith & Williamson": "smithandwilliamson.com",
    "UHY": "uhy.com",
    "HLB": "hlb.global",
    "Nexia": "nexia.com",
    "Moore Global": "moore.global",
    "Kreston": "kreston.com",
    "AGN International": "agn.org",
    "PrimeGlobal": "primeglobal.net",
    "KPMG": "kpmg.com",
    "Moss Adams": "mossadams.com",
    "CohnReznick": "cohnreznick.com",
    "Marcum": "marcumllp.com",
    "Plante Moran": "plantemoran.com",
    "CliftonLarsonAllen": "claconnect.com",
    "CBIZ": "cbiz.com",
    "Wipfli": "wipfli.com",
    "Dixon Hughes Goodman": "dhg.com",
    "Cherry Bekaert": "cbh.com",
    "Frank Rimerman": "frankrimerman.com",
    "Eide Bailly": "eidebailly.com",
    "BKD": "bkd.com",
    "McGladrey": "rsm.us"
}

# Regional Banks
REGIONAL_BANKS = {
    # US Regional
    "PNC Bank": "pnc.com",
    "US Bank": "usbank.com",
    "Truist": "truist.com",
    "Fifth Third": "53.com",
    "KeyBank": "key.com",
    "Regions Bank": "regions.com",
    "M&T Bank": "mtb.com",
    "Huntington Bank": "huntington.com",
    "Citizens Bank": "citizensbank.com",
    "Santander US": "santanderbank.com",
    "BMO Harris": "bmoharris.com",
    "MUFG Union Bank": "unionbank.com",
    "Comerica": "comerica.com",
    "Zions Bank": "zionsbank.com",
    "First Republic": "firstrepublic.com",
    "SVB": "svb.com",
    "Signature Bank": "signatureny.com",
    "First Citizens": "firstcitizens.com",
    "Synovus": "synovus.com",
    "BOK Financial": "bokf.com",
    
    # European Banks
    "BNP Paribas": "bnpparibas.com",
    "Société Générale": "societegenerale.com",
    "Crédit Agricole": "credit-agricole.com",
    "UniCredit": "unicredit.it",
    "Intesa Sanpaolo": "intesasanpaolo.com",
    "Santander": "santander.com",
    "BBVA": "bbva.com",
    "ING": "ing.com",
    "Rabobank": "rabobank.com",
    "KBC": "kbc.com",
    "Nordea": "nordea.com",
    "SEB": "seb.se",
    "Danske Bank": "danskebank.com",
    "DNB": "dnb.no",
    "Commerzbank": "commerzbank.com",
    "Landesbank": "lbbw.de",
    
    # Asian Banks
    "Mitsubishi UFJ": "mufg.jp",
    "Sumitomo Mitsui": "smbc.co.jp",
    "Mizuho": "mizuho-fg.com",
    "Bank of Communications": "bankcomm.com",
    "China Merchants Bank": "cmbchina.com",
    "Industrial Bank": "cib.com.cn",
    "Shanghai Pudong": "spdb.com.cn",
    "Minsheng Bank": "cmbc.com.cn",
    
    # Other Regional
    "National Bank of Canada": "nbc.ca",
    "Scotiabank": "scotiabank.com",
    "CIBC": "cibc.com",
    "Westpac": "westpac.com.au",
    "NAB": "nab.com.au"
}

# Airlines & Transport
AIRLINES_TRANSPORT = {
    # US Airlines
    "American Airlines": "aa.com",
    "Delta Air Lines": "delta.com",
    "United Airlines": "united.com",
    "Southwest Airlines": "southwest.com",
    "JetBlue": "jetblue.com",
    "Alaska Airlines": "alaskaair.com",
    "Spirit Airlines": "spirit.com",
    "Frontier Airlines": "flyfrontier.com",
    "Hawaiian Airlines": "hawaiianairlines.com",
    "Allegiant": "allegiant.com",
    
    # European Airlines
    "Lufthansa": "lufthansa.com",
    "Air France": "airfrance.com",
    "KLM": "klm.com",
    "British Airways": "britishairways.com",
    "Iberia": "iberia.com",
    "Ryanair": "ryanair.com",
    "easyJet": "easyjet.com",
    "Wizz Air": "wizzair.com",
    "TAP Air Portugal": "flytap.com",
    "SAS": "sas.com",
    "Finnair": "finnair.com",
    "Aegean": "aegeanair.com",
    "Turkish Airlines": "turkishairlines.com",
    "LOT Polish": "lot.com",
    "Czech Airlines": "csa.cz",
    "Austrian Airlines": "austrian.com",
    "Brussels Airlines": "brusselsairlines.com",
    "Vueling": "vueling.com",
    "Eurowings": "eurowings.com",
    "Condor": "condor.com",
    
    # Asian Airlines
    "Air China": "airchina.com",
    "China Eastern": "ceair.com",
    "China Southern": "csair.com",
    "Hainan Airlines": "hainanairlines.com",
    "Japan Airlines": "jal.com",
    "ANA": "ana.co.jp",
    "Korean Air": "koreanair.com",
    "Asiana": "flyasiana.com",
    "Thai Airways": "thaiairways.com",
    "Malaysia Airlines": "malaysiaairlines.com",
    "Garuda Indonesia": "garuda-indonesia.com",
    "Philippine Airlines": "philippineairlines.com",
    "Vietnam Airlines": "vietnamairlines.com",
    "Air India": "airindia.in",
    "IndiGo": "goindigo.in",
    "SpiceJet": "spicejet.com",
    
    # Other Airlines
    "Air Canada": "aircanada.com",
    "WestJet": "westjet.com",
    "Aeromexico": "aeromexico.com",
    "Copa Airlines": "copaair.com",
    "Avianca": "avianca.com",
    "LATAM": "latam.com",
    "Azul": "voeazul.com.br",
    "GOL": "voegol.com.br",
    "Ethiopian Airlines": "ethiopianairlines.com",
    "Kenya Airways": "kenya-airways.com",
    "South African Airways": "flysaa.com",
    "Air New Zealand": "airnewzealand.com",
    
    # Rail & Ground
    "Union Pacific": "up.com",
    "BNSF": "bnsf.com",
    "CSX": "csx.com",
    "Norfolk Southern": "nscorp.com",
    "Canadian National": "cn.ca",
    "Canadian Pacific": "cpr.ca",
    "Amtrak": "amtrak.com",
    "SNCF": "sncf.com",
    "Deutsche Bahn": "deutschebahn.com",
    "Trenitalia": "trenitalia.com",
    "Renfe": "renfe.com",
    "JR Group": "jreast.co.jp",
    "China Railway": "china-railway.com.cn"
}

# Utilities
UTILITIES = {
    # US Utilities
    "NextEra Energy": "nexteraenergy.com",
    "Duke Energy": "duke-energy.com",
    "Southern Company": "southerncompany.com",
    "Dominion Energy": "dominionenergy.com",
    "Exelon": "exeloncorp.com",
    "American Electric Power": "aep.com",
    "Sempra Energy": "sempra.com",
    "PG&E": "pge.com",
    "Edison International": "edison.com",
    "Entergy": "entergy.com",
    "FirstEnergy": "firstenergycorp.com",
    "Xcel Energy": "xcelenergy.com",
    "WEC Energy": "wecenergygroup.com",
    "Eversource": "eversource.com",
    "DTE Energy": "dteenergy.com",
    "Consolidated Edison": "coned.com",
    "Public Service Enterprise": "pseg.com",
    "CenterPoint Energy": "centerpointenergy.com",
    "NiSource": "nisource.com",
    "Alliant Energy": "alliantenergy.com",
    
    # European Utilities
    "EDF": "edf.fr",
    "Engie": "engie.com",
    "Enel": "enel.com",
    "Iberdrola": "iberdrola.com",
    "E.ON": "eon.com",
    "RWE": "rwe.com",
    "National Grid": "nationalgrid.com",
    "SSE": "sse.com",
    "Centrica": "centrica.com",
    "Vattenfall": "vattenfall.com",
    "Fortum": "fortum.com",
    "Orsted": "orsted.com",
    "Naturgy": "naturgy.com",
    "EDP": "edp.com",
    "A2A": "a2a.eu",
    
    # Asian Utilities
    "Tokyo Electric": "tepco.co.jp",
    "Kansai Electric": "kepco.co.jp",
    "State Grid China": "sgcc.com.cn",
    "China Southern Power": "csg.cn",
    "NTPC": "ntpc.co.in",
    "Power Grid India": "powergridindia.com",
    "Tata Power": "tatapower.com",
    "Korea Electric": "kepco.co.kr",
    "Taiwan Power": "taipower.com.tw",
    
    # Water & Waste
    "Veolia": "veolia.com",
    "Suez": "suez.com",
    "American Water": "amwater.com",
    "Waste Management": "wm.com",
    "Republic Services": "republicservices.com",
    "Waste Connections": "wasteconnections.com",
    "Clean Harbors": "cleanharbors.com",
    "Stericycle": "stericycle.com"
}

# Enterprise Software & Tech
ENTERPRISE_TECH = {
    # ERP & Business Software
    "SAP": "sap.com",
    "Oracle": "oracle.com",
    "Microsoft Dynamics": "dynamics.microsoft.com",
    "Infor": "infor.com",
    "Epicor": "epicor.com",
    "NetSuite": "netsuite.com",
    "Sage": "sage.com",
    "IFS": "ifs.com",
    "QAD": "qad.com",
    "Unit4": "unit4.com",
    
    # Data & Analytics
    "Alteryx": "alteryx.com",
    "Domo": "domo.com",
    "Sisense": "sisense.com",
    "Looker": "looker.com",
    "Qlik": "qlik.com",
    "MicroStrategy": "microstrategy.com",
    "SAS": "sas.com",
    "TIBCO": "tibco.com",
    "Informatica": "informatica.com",
    "Talend": "talend.com",
    
    # Cybersecurity
    "Zscaler": "zscaler.com",
    "Cloudflare": "cloudflare.com",
    "Rapid7": "rapid7.com",
    "Tenable": "tenable.com",
    "Qualys": "qualys.com",
    "Proofpoint": "proofpoint.com",
    "Mimecast": "mimecast.com",
    "Sophos": "sophos.com",
    "Trend Micro": "trendmicro.com",
    "Check Point": "checkpoint.com",
    "McAfee": "mcafee.com",
    "Norton": "norton.com",
    "Symantec": "symantec.com",
    "Kaspersky": "kaspersky.com",
    "Bitdefender": "bitdefender.com",
    "ESET": "eset.com",
    "Malwarebytes": "malwarebytes.com",
    "CyberArk": "cyberark.com",
    "Varonis": "varonis.com"
}

# Specialty Sectors
SPECIALTY_SECTORS = {
    # Staffing & HR Services
    "Adecco": "adecco.com",
    "Randstad": "randstad.com",
    "ManpowerGroup": "manpowergroup.com",
    "Robert Half": "roberthalf.com",
    "Kelly Services": "kellyservices.com",
    "Allegis Group": "allegisgroup.com",
    "Hays": "hays.com",
    "Michael Page": "michaelpage.com",
    "Korn Ferry": "kornferry.com",
    "Russell Reynolds": "russellreynolds.com",
    "Spencer Stuart": "spencerstuart.com",
    "Egon Zehnder": "egonzehnder.com",
    "Heidrick & Struggles": "heidrick.com",
    
    # Facilities & Services
    "Aramark": "aramark.com",
    "Sodexo": "sodexo.com",
    "Compass Group": "compass-group.com",
    "ISS": "issworld.com",
    "ABM": "abm.com",
    "Cintas": "cintas.com",
    "Ecolab": "ecolab.com",
    "Rollins": "rollins.com",
    "ServiceMaster": "servicemaster.com",
    "Terminix": "terminix.com",
    
    # Testing & Inspection
    "SGS": "sgs.com",
    "Bureau Veritas": "bureauveritas.com",
    "Intertek": "intertek.com",
    "TÜV SÜD": "tuvsud.com",
    "TÜV Rheinland": "tuv.com",
    "DNV": "dnv.com",
    "Lloyd's Register": "lr.org",
    "UL": "ul.com",
    "NSF": "nsf.org",
    "Eurofins": "eurofins.com",
    
    # Auction Houses & Luxury
    "Christie's": "christies.com",
    "Sotheby's": "sothebys.com",
    "Phillips": "phillips.com",
    "Bonhams": "bonhams.com",
    "Heritage Auctions": "ha.com",
    
    # Sports & Entertainment Venues
    "Madison Square Garden": "msg.com",
    "AEG": "aegworldwide.com",
    "Live Nation": "livenation.com",
    "Oak View Group": "oakviewgroup.com",
    "ASM Global": "asmglobal.com",
    "Manchester United": "manutd.com",
    "Real Madrid": "realmadrid.com",
    "FC Barcelona": "fcbarcelona.com",
    "Yankees": "mlb.com/yankees",
    "Lakers": "nba.com/lakers",
    "Cowboys": "dallascowboys.com",
    
    # Government Contractors
    "Parsons": "parsons.com",
    "KBR": "kbr.com",
    "Battelle": "battelle.org",
    "MITRE": "mitre.org",
    "Aerospace Corporation": "aerospace.org",
    "RAND": "rand.org",
    "IDA": "ida.org",
    "STX": "stx.com",
    "DynCorp": "dyn-intl.com",
    "PAE": "pae.com",
    "Vectrus": "vectrus.com",
    
    # Specialty Retail
    "Whole Foods": "wholefoodsmarket.com",
    "Trader Joe's": "traderjoes.com",
    "Wegmans": "wegmans.com",
    "Publix": "publix.com",
    "HEB": "heb.com",
    "Meijer": "meijer.com",
    "Dick's Sporting Goods": "dickssportinggoods.com",
    "Academy Sports": "academy.com",
    "REI": "rei.com",
    "Bass Pro Shops": "basspro.com",
    "Cabela's": "cabelas.com",
    "Office Depot": "officedepot.com",
    "Staples": "staples.com",
    "Michaels": "michaels.com",
    "Hobby Lobby": "hobbylobby.com",
    "Jo-Ann": "joann.com",
    "Barnes & Noble": "barnesandnoble.com",
    "Books-A-Million": "booksamillion.com"
}

# Failed Downloads to Retry
FAILED_RETRIES = {
    # From previous attempts
    "Cyfrowy Polsat": "grupapolsat.pl",
    "Yang Ming": "yangming.com",
    "Fanuc": "fanuc.co.jp",
    "Jubilant": "jubilantindustries.com",
    "Geely": "geely.com",
    "Wanda Group": "wanda-group.com",
    "Dalian Wanda": "wanda.cn",
    "Steinhoff": "steinhoffinternational.com",
    "Fujitsu": "fujitsu.com",
    "OCBC Bank": "ocbc.com",
    "Stone": "stone.com.br",
    "Credicorp": "credicorp.com",
    "M-Pesa": "safaricom.co.ke",
    "ViacomCBS": "viacomcbs.com",
    
    # Other notable misses
    "Grab": "grab.com",
    "Gojek": "gojek.com",
    "Sea Limited": "sea.com",
    "Shopee": "shopee.com",
    "Lazada": "lazada.com",
    "Tokopedia": "tokopedia.com",
    "Bukalapak": "bukalapak.com",
    "Traveloka": "traveloka.com",
    "Careem": "careem.com",
    "Talabat": "talabat.com",
    "Deliveroo": "deliveroo.com",
    "Glovo": "glovoapp.com",
    "Rappi": "rappi.com",
    "iFood": "ifood.com.br",
    "Zomato": "zomato.com",
    "Swiggy": "swiggy.com"
}

def get_all_ultimate_final_companies():
    """Return all companies for ultimate final push"""
    all_companies = {}
    all_companies.update(LAW_FIRMS)
    all_companies.update(FOOD_AGRICULTURE)
    all_companies.update(ACCOUNTING_FIRMS)
    all_companies.update(REGIONAL_BANKS)
    all_companies.update(AIRLINES_TRANSPORT)
    all_companies.update(UTILITIES)
    all_companies.update(ENTERPRISE_TECH)
    all_companies.update(SPECIALTY_SECTORS)
    all_companies.update(FAILED_RETRIES)
    return all_companies

if __name__ == "__main__":
    all_companies = get_all_ultimate_final_companies()
    print(f"Law Firms: {len(LAW_FIRMS)}")
    print(f"Food & Agriculture: {len(FOOD_AGRICULTURE)}")
    print(f"Accounting Firms: {len(ACCOUNTING_FIRMS)}")
    print(f"Regional Banks: {len(REGIONAL_BANKS)}")
    print(f"Airlines & Transport: {len(AIRLINES_TRANSPORT)}")
    print(f"Utilities: {len(UTILITIES)}")
    print(f"Enterprise Tech: {len(ENTERPRISE_TECH)}")
    print(f"Specialty Sectors: {len(SPECIALTY_SECTORS)}")
    print(f"Failed Retries: {len(FAILED_RETRIES)}")
    print(f"\nTOTAL ULTIMATE FINAL: {len(all_companies)}")