#!/usr/bin/env python3
"""
Top employers for business graduates in 2025
Including hot startups, mid-sized companies, and Australian organizations
"""

# Top 50 Australian Business Schools
AUSTRALIAN_BUSINESS_SCHOOLS = {
    "Melbourne Business School": "mbs.edu",
    "Australian Graduate School of Management (AGSM)": "agsm.edu.au",
    "UQ Business School": "business.uq.edu.au",
    "Monash Business School": "monash.edu/business",
    "Sydney Business School": "sydney.edu.au/business",
    "Macquarie Business School": "mq.edu.au/macquarie-business-school",
    "RMIT Business School": "rmit.edu.au/business",
    "UTS Business School": "uts.edu.au/about/uts-business-school",
    "Deakin Business School": "deakin.edu.au/business",
    "Griffith Business School": "griffith.edu.au/business-government",
    "QUT Business School": "qut.edu.au/business",
    "La Trobe Business School": "latrobe.edu.au/business",
    "Curtin Business School": "business.curtin.edu.au",
    "UniSA Business School": "unisa.edu.au/business",
    "Newcastle Business School": "newcastle.edu.au/faculty/business-law",
    "Wollongong Business School": "uow.edu.au/business",
    "Bond Business School": "bond.edu.au/faculty/bond-business-school",
    "Swinburne Business School": "swinburne.edu.au/business-law",
    "ECU Business School": "ecu.edu.au/schools/business-and-law",
    "Victoria University Business School": "vu.edu.au/business",
    "Charles Sturt Business School": "csu.edu.au/faculty/business-justice-behavioural-sciences",
    "Murdoch Business School": "murdoch.edu.au/study/colleges-schools/business-governance",
    "Western Sydney Business School": "westernsydney.edu.au/business",
    "ACU Business School": "acu.edu.au/faculties/thomas-more-law-school",
    "CQU Business School": "cqu.edu.au/about-us/structure/schools/business-and-law",
    "USQ Business School": "usq.edu.au/business-law",
    "SCU Business School": "scu.edu.au/business-school",
    "Charles Darwin Business School": "cdu.edu.au/business",
    "Tasmania Business School": "utas.edu.au/business-and-economics",
    "Flinders Business School": "flinders.edu.au/college-business-government-law",
    "James Cook Business School": "jcu.edu.au/college-of-business-law-governance",
    "Federation Business School": "federation.edu.au/schools/school-of-business",
    "Notre Dame Business School": "notredame.edu.au/about/schools/business",
    "Canberra Business School": "canberra.edu.au/faculties/busgovlaw",
    "Avondale Business School": "avondale.edu.au/courses/business",
    "Alphacrucis Business School": "ac.edu.au/business",
    "Torrens Business School": "torrens.edu.au/schools/business",
    "ICMS Business School": "icms.edu.au",
    "Kaplan Business School": "kaplan.edu.au",
    "AIM Business School": "aim.com.au/business-school",
    "Melbourne Institute of Technology": "mit.edu.au",
    "Sydney Institute of Business and Technology": "sibt.nsw.edu.au",
    "Perth Institute of Business and Technology": "pibt.wa.edu.au",
    "Brisbane School of Business": "bsb.edu.au",
    "Adelaide Business School": "adelaide.edu.au/business",
    "UNE Business School": "une.edu.au/about-une/faculty-of-science-agriculture-business-and-law",
    "Holmes Institute": "holmes.edu.au",
    "TOP Education Institute": "top.edu.au",
    "King's Own Institute": "koi.edu.au",
    "Australian Institute of Business": "aib.edu.au"
}

# Australian Major Employers
AUSTRALIAN_COMPANIES = {
    # Mining & Resources
    "BHP": "bhp.com",
    "Rio Tinto": "riotinto.com",
    "Fortescue Metals": "fmgl.com.au",
    "Woodside Energy": "woodside.com",
    "Santos": "santos.com",
    "Origin Energy": "originenergy.com.au",
    "Newcrest Mining": "newcrest.com.au",
    "South32": "south32.net",
    
    # Banks & Financial
    "Commonwealth Bank": "commbank.com.au",
    "ANZ Bank": "anz.com.au",
    "Westpac": "westpac.com.au",
    "National Australia Bank": "nab.com.au",
    "Macquarie Group": "macquarie.com",
    "AMP": "amp.com.au",
    "Suncorp": "suncorp.com.au",
    "QBE Insurance": "qbe.com",
    
    # Retail & Consumer
    "Woolworths": "woolworths.com.au",
    "Coles": "coles.com.au",
    "Wesfarmers": "wesfarmers.com.au",
    "JB Hi-Fi": "jbhifi.com.au",
    "Harvey Norman": "harveynorman.com.au",
    
    # Telecom & Tech
    "Telstra": "telstra.com.au",
    "Optus": "optus.com.au",
    "TPG Telecom": "tpg.com.au",
    "Atlassian": "atlassian.com",
    "Canva": "canva.com",
    "Afterpay": "afterpay.com",
    "WiseTech Global": "wisetechglobal.com",
    "Xero": "xero.com",
    "SEEK": "seek.com.au",
    "REA Group": "realestate.com.au",
    "Carsales.com": "carsales.com.au",
    
    # Airlines & Transport
    "Qantas": "qantas.com",
    "Virgin Australia": "virginaustralia.com",
    "Transurban": "transurban.com",
    "Aurizon": "aurizon.com.au",
    
    # Healthcare
    "CSL": "csl.com",
    "Cochlear": "cochlear.com",
    "Ramsay Health Care": "ramsayhealth.com",
    "Sonic Healthcare": "sonichealthcare.com",
    
    # Construction & Property
    "Lendlease": "lendlease.com",
    "Stockland": "stockland.com.au",
    "Mirvac": "mirvac.com",
    "Dexus": "dexus.com",
    "Goodman Group": "goodman.com"
}

# Top 250 Hot Startups & Mid-sized Companies for 2025
HOT_COMPANIES_2025 = {
    # AI & ML Companies
    "OpenAI": "openai.com",
    "Anthropic": "anthropic.com",
    "Cohere": "cohere.com",
    "Hugging Face": "huggingface.co",
    "Scale AI": "scale.com",
    "Databricks": "databricks.com",
    "DataRobot": "datarobot.com",
    "Weights & Biases": "wandb.ai",
    "Replica": "replica.com",
    "Jasper AI": "jasper.ai",
    "Midjourney": "midjourney.com",
    "Stability AI": "stability.ai",
    "Runway": "runwayml.com",
    "Character AI": "character.ai",
    "Perplexity AI": "perplexity.ai",
    "Pika Labs": "pika.art",
    "Mistral AI": "mistral.ai",
    "Inflection AI": "inflection.ai",
    "Adept": "adept.ai",
    "Replit": "replit.com",
    
    # Fintech
    "Stripe": "stripe.com",
    "Plaid": "plaid.com",
    "Chime": "chime.com",
    "Brex": "brex.com",
    "Ramp": "ramp.com",
    "Mercury": "mercury.com",
    "Wise": "wise.com",
    "Revolut": "revolut.com",
    "N26": "n26.com",
    "Monzo": "monzo.com",
    "Nubank": "nubank.com.br",
    "Affirm": "affirm.com",
    "Klarna": "klarna.com",
    "Checkout.com": "checkout.com",
    "Marqeta": "marqeta.com",
    "Bill.com": "bill.com",
    "Gusto": "gusto.com",
    "Rippling": "rippling.com",
    "Carta": "carta.com",
    "Pipe": "pipe.com",
    
    # Climate Tech & Clean Energy
    "Rivian": "rivian.com",
    "Lucid Motors": "lucidmotors.com",
    "Northvolt": "northvolt.com",
    "Commonwealth Fusion Systems": "cfs.energy",
    "Helion Energy": "helionenergy.com",
    "Form Energy": "formenergy.com",
    "Redwood Materials": "redwoodmaterials.com",
    "Sila Nanotechnologies": "silanano.com",
    "Impossible Foods": "impossiblefoods.com",
    "Beyond Meat": "beyondmeat.com",
    "Perfect Day": "perfectday.com",
    "Bolt Threads": "boltthreads.com",
    "Carbon Engineering": "carbonengineering.com",
    "Climeworks": "climeworks.com",
    "Pachama": "pachama.com",
    
    # Health Tech
    "Oscar Health": "hioscar.com",
    "Ro": "ro.co",
    "Hims & Hers": "forhims.com",
    "Carbon Health": "carbonhealth.com",
    "Oak Street Health": "oakstreethealth.com",
    "Devoted Health": "devoted.com",
    "Butterfly Network": "butterflynetwork.com",
    "Tempus": "tempus.com",
    "Freenome": "freenome.com",
    "Color Health": "color.com",
    "Forward": "goforward.com",
    "One Medical": "onemedical.com",
    "Babylon Health": "babylonhealth.com",
    "K Health": "khealth.com",
    "Headspace Health": "headspacehealth.com",
    
    # SaaS & Productivity
    "Notion": "notion.so",
    "Figma": "figma.com",
    "Miro": "miro.com",
    "Airtable": "airtable.com",
    "Monday.com": "monday.com",
    "ClickUp": "clickup.com",
    "Linear": "linear.app",
    "Coda": "coda.io",
    "Loom": "loom.com",
    "Calendly": "calendly.com",
    "Zapier": "zapier.com",
    "Webflow": "webflow.com",
    "Bubble": "bubble.io",
    "Retool": "retool.com",
    "Vercel": "vercel.com",
    "Netlify": "netlify.com",
    "HashiCorp": "hashicorp.com",
    "GitLab": "gitlab.com",
    "JetBrains": "jetbrains.com",
    "Postman": "postman.com",
    
    # E-commerce & Marketplaces
    "Instacart": "instacart.com",
    "DoorDash": "doordash.com",
    "Gopuff": "gopuff.com",
    "Gorillas": "gorillas.io",
    "Getir": "getir.com",
    "StockX": "stockx.com",
    "GOAT": "goat.com",
    "Vinted": "vinted.com",
    "Depop": "depop.com",
    "Mercari": "mercari.com",
    "OfferUp": "offerup.com",
    "Faire": "faire.com",
    "Whatnot": "whatnot.com",
    "Fanatics": "fanatics.com",
    "ThredUp": "thredup.com",
    
    # Space & Deep Tech
    "SpaceX": "spacex.com",
    "Blue Origin": "blueorigin.com",
    "Rocket Lab": "rocketlabusa.com",
    "Relativity Space": "relativityspace.com",
    "Astra": "astra.com",
    "Planet Labs": "planet.com",
    "Spire Global": "spire.com",
    "Anduril": "anduril.com",
    "Shield AI": "shield.ai",
    "Palantir": "palantir.com",
    
    # Gaming & Entertainment
    "Epic Games": "epicgames.com",
    "Roblox": "roblox.com",
    "Discord": "discord.com",
    "Unity": "unity.com",
    "Niantic": "nianticlabs.com",
    "Scopely": "scopely.com",
    "AppLovin": "applovin.com",
    "Activision Blizzard": "activisionblizzard.com",
    "Zynga": "zynga.com",
    "Supercell": "supercell.com",
    
    # Crypto & Web3
    "Coinbase": "coinbase.com",
    "Kraken": "kraken.com",
    "Binance US": "binance.us",
    "Gemini": "gemini.com",
    "FTX US": "ftx.us",
    "BlockFi": "blockfi.com",
    "Chainalysis": "chainalysis.com",
    "OpenSea": "opensea.io",
    "Dapper Labs": "dapperlabs.com",
    "Alchemy": "alchemy.com",
    
    # B2B Software
    "Snowflake": "snowflake.com",
    "UiPath": "uipath.com",
    "Automation Anywhere": "automationanywhere.com",
    "Celonis": "celonis.com",
    "Workato": "workato.com",
    "Segment": "segment.com",
    "Amplitude": "amplitude.com",
    "Mixpanel": "mixpanel.com",
    "Heap": "heap.io",
    "FullStory": "fullstory.com",
    "LaunchDarkly": "launchdarkly.com",
    "PagerDuty": "pagerduty.com",
    "Datadog": "datadoghq.com",
    "New Relic": "newrelic.com",
    "Sumo Logic": "sumologic.com",
    
    # EdTech
    "Coursera": "coursera.org",
    "Udacity": "udacity.com",
    "MasterClass": "masterclass.com",
    "Duolingo": "duolingo.com",
    "Outschool": "outschool.com",
    "Guild Education": "guild.com",
    "BetterUp": "betterup.com",
    "Handshake": "joinhandshake.com",
    "Course Hero": "coursehero.com",
    "Quizlet": "quizlet.com",
    
    # PropTech
    "Opendoor": "opendoor.com",
    "Compass": "compass.com",
    "Redfin": "redfin.com",
    "Zillow": "zillow.com",
    "Divvy Homes": "divvyhomes.com",
    "Flyhomes": "flyhomes.com",
    "Better.com": "better.com",
    "Roofstock": "roofstock.com",
    "Pacaso": "pacaso.com",
    "Sonder": "sonder.com",
    
    # Mobility & Logistics
    "Waymo": "waymo.com",
    "Cruise": "getcruise.com",
    "Aurora": "aurora.tech",
    "Argo AI": "argo.ai",
    "Nuro": "nuro.ai",
    "TuSimple": "tusimple.com",
    "Flexport": "flexport.com",
    "Convoy": "convoy.com",
    "Shippo": "goshippo.com",
    "Samsara": "samsara.com",
    
    # Security & Privacy
    "CrowdStrike": "crowdstrike.com",
    "SentinelOne": "sentinelone.com",
    "Okta": "okta.com",
    "Auth0": "auth0.com",
    "1Password": "1password.com",
    "Bitwarden": "bitwarden.com",
    "NordVPN": "nordvpn.com",
    "ExpressVPN": "expressvpn.com",
    "Proton": "proton.me",
    "Signal": "signal.org",
    
    # HR Tech
    "Workday": "workday.com",
    "Greenhouse": "greenhouse.io",
    "Lever": "lever.co",
    "SmartRecruiters": "smartrecruiters.com",
    "Lattice": "lattice.com",
    "Culture Amp": "cultureamp.com",
    "15Five": "15five.com",
    "Namely": "namely.com",
    "BambooHR": "bamboohr.com",
    "Justworks": "justworks.com",
    
    # Marketing Tech
    "Canva": "canva.com",
    "Klaviyo": "klaviyo.com",
    "Iterable": "iterable.com",
    "Braze": "braze.com",
    "Segment": "segment.com",
    "Customer.io": "customer.io",
    "ActiveCampaign": "activecampaign.com",
    "ConvertKit": "convertkit.com",
    "Mailchimp": "mailchimp.com",
    "Constant Contact": "constantcontact.com"
}

# Major global employers we might be missing
MISSING_GLOBAL_EMPLOYERS = {
    # Private Equity
    "KKR": "kkr.com",
    "Blackstone": "blackstone.com",
    "Apollo Global Management": "apollo.com",
    "Silver Lake": "silverlake.com",
    "Vista Equity Partners": "vistaequitypartners.com",
    "Thoma Bravo": "thomabravo.com",
    "Warburg Pincus": "warburgpincus.com",
    "General Atlantic": "generalatlantic.com",
    "Advent International": "adventinternational.com",
    
    # Hedge Funds
    "Bridgewater Associates": "bridgewater.com",
    "Renaissance Technologies": "rentec.com",
    "Two Sigma": "twosigma.com",
    "Citadel": "citadel.com",
    "D.E. Shaw": "deshaw.com",
    "Millennium Management": "mlp.com",
    "Point72": "point72.com",
    
    # Venture Capital
    "Sequoia Capital": "sequoiacap.com",
    "Andreessen Horowitz": "a16z.com",
    "Kleiner Perkins": "kleinerperkins.com",
    "Benchmark": "benchmark.com",
    "Greylock Partners": "greylock.com",
    "Accel": "accel.com",
    "Bessemer Venture Partners": "bvp.com",
    "GV (Google Ventures)": "gv.com",
    "Founders Fund": "foundersfund.com",
    "Index Ventures": "indexventures.com",
    "Lightspeed Venture Partners": "lsvp.com",
    "Battery Ventures": "battery.com"
}

def get_all_new_companies():
    """Return all new companies to download"""
    all_companies = {}
    all_companies.update(AUSTRALIAN_BUSINESS_SCHOOLS)
    all_companies.update(AUSTRALIAN_COMPANIES)
    all_companies.update(HOT_COMPANIES_2025)
    all_companies.update(MISSING_GLOBAL_EMPLOYERS)
    return all_companies

if __name__ == "__main__":
    all_new = get_all_new_companies()
    print(f"Australian Business Schools: {len(AUSTRALIAN_BUSINESS_SCHOOLS)}")
    print(f"Australian Companies: {len(AUSTRALIAN_COMPANIES)}")
    print(f"Hot Companies 2025: {len(HOT_COMPANIES_2025)}")
    print(f"Missing Global Employers: {len(MISSING_GLOBAL_EMPLOYERS)}")
    print(f"Total new organizations: {len(all_new)}")