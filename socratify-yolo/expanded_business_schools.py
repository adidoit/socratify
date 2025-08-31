#!/usr/bin/env python3
"""
Expanded list of top business schools with their domains
Top 100 US, Top 50 Europe, Top 50 India, Top 50 Canada
"""

# Top 100 US Business Schools with domains
US_BUSINESS_SCHOOLS = {
    # Top 20
    "Harvard Business School": "hbs.edu",
    "Stanford Graduate School of Business": "gsb.stanford.edu",
    "Wharton School": "wharton.upenn.edu",
    "MIT Sloan School of Management": "mitsloan.mit.edu",
    "Chicago Booth School of Business": "chicagobooth.edu",
    "Northwestern Kellogg School of Management": "kellogg.northwestern.edu",
    "Columbia Business School": "gsb.columbia.edu",
    "UC Berkeley Haas School of Business": "haas.berkeley.edu",
    "Yale School of Management": "som.yale.edu",
    "Dartmouth Tuck School of Business": "tuck.dartmouth.edu",
    "Michigan Ross School of Business": "michiganross.umich.edu",
    "Duke Fuqua School of Business": "fuqua.duke.edu",
    "NYU Stern School of Business": "stern.nyu.edu",
    "Cornell Johnson School of Management": "johnson.cornell.edu",
    "UCLA Anderson School of Management": "anderson.ucla.edu",
    "USC Marshall School of Business": "marshall.usc.edu",
    "Georgetown McDonough School of Business": "msb.georgetown.edu",
    "UNC Kenan-Flagler Business School": "kenan-flagler.unc.edu",
    "Carnegie Mellon Tepper School of Business": "tepper.cmu.edu",
    "Emory Goizueta Business School": "goizueta.emory.edu",
    
    # 21-40
    "Indiana Kelley School of Business": "kelley.iu.edu",
    "Washington University Olin Business School": "olin.wustl.edu",
    "Rice Jones Graduate School of Business": "business.rice.edu",
    "Vanderbilt Owen Graduate School of Management": "owen.vanderbilt.edu",
    "Notre Dame Mendoza College of Business": "mendoza.nd.edu",
    "Georgia Tech Scheller College of Business": "scheller.gatech.edu",
    "Boston College Carroll School of Management": "bc.edu/bc-web/schools/carroll-school.html",
    "Michigan State Broad College of Business": "broad.msu.edu",
    "Penn State Smeal College of Business": "smeal.psu.edu",
    "Maryland Smith School of Business": "smith.umd.edu",
    "Rochester Simon Business School": "simon.rochester.edu",
    "Purdue Krannert School of Management": "krannert.purdue.edu",
    "Minnesota Carlson School of Management": "carlsonschool.umn.edu",
    "Ohio State Fisher College of Business": "fisher.osu.edu",
    "Wisconsin School of Business": "bus.wisc.edu",
    "Georgia Terry College of Business": "terry.uga.edu",
    "Arizona State WP Carey School of Business": "wpcarey.asu.edu",
    "Texas McCombs School of Business": "mccombs.utexas.edu",
    "Washington Foster School of Business": "foster.uw.edu",
    "Florida Warrington College of Business": "warrington.ufl.edu",
    
    # 41-60
    "UC Davis Graduate School of Management": "gsm.ucdavis.edu",
    "UC Irvine Merage School of Business": "merage.uci.edu",
    "Boston University Questrom School of Business": "bu.edu/questrom",
    "Tulane Freeman School of Business": "freeman.tulane.edu",
    "University of Miami Business School": "bus.miami.edu",
    "Babson Olin Graduate School of Business": "babson.edu",
    "SMU Cox School of Business": "cox.smu.edu",
    "Pittsburgh Katz Graduate School of Business": "business.pitt.edu",
    "Iowa Tippie College of Business": "tippie.uiowa.edu",
    "Syracuse Whitman School of Management": "whitman.syr.edu",
    "Connecticut School of Business": "business.uconn.edu",
    "Fordham Gabelli School of Business": "gabelli.fordham.edu",
    "George Washington School of Business": "business.gwu.edu",
    "Temple Fox School of Business": "fox.temple.edu",
    "Rutgers Business School": "business.rutgers.edu",
    "Missouri Trulaske College of Business": "business.missouri.edu",
    "Colorado Leeds School of Business": "leeds.colorado.edu",
    "Alabama Manderson Graduate School of Business": "manderson.culverhouse.ua.edu",
    "Tennessee Haslam College of Business": "haslam.utk.edu",
    "South Carolina Darla Moore School of Business": "moore.sc.edu",
    
    # 61-80
    "SUNY Buffalo School of Management": "mgt.buffalo.edu",
    "Northeastern D'Amore-McKim School of Business": "damore-mckim.northeastern.edu",
    "Pepperdine Graziadio Business School": "bschool.pepperdine.edu",
    "William & Mary Mason School of Business": "mason.wm.edu",
    "Texas A&M Mays Business School": "mays.tamu.edu",
    "Oklahoma Price College of Business": "price.ou.edu",
    "Auburn Harbert College of Business": "harbert.auburn.edu",
    "Utah Eccles School of Business": "eccles.utah.edu",
    "Kentucky Gatton College of Business": "gatton.uky.edu",
    "Kansas School of Business": "business.ku.edu",
    "Arkansas Walton College of Business": "walton.uark.edu",
    "Oregon Lundquist College of Business": "lcb.uoregon.edu",
    "NC State Jenkins Graduate School of Management": "mgt.ncsu.edu",
    "Virginia Tech Pamplin College of Business": "pamplin.vt.edu",
    "UC San Diego Rady School of Management": "rady.ucsd.edu",
    "Lehigh College of Business": "business.lehigh.edu",
    "Delaware Lerner College of Business": "lerner.udel.edu",
    "Houston Bauer College of Business": "bauer.uh.edu",
    "DePaul Driehaus College of Business": "business.depaul.edu",
    "Bentley Graduate School of Business": "bentley.edu",
    
    # 81-100
    "Villanova School of Business": "villanovaschoolofbusiness.com",
    "Wake Forest School of Business": "business.wfu.edu",
    "George Mason School of Business": "business.gmu.edu",
    "Baylor Hankamer School of Business": "baylor.edu/business",
    "Loyola Chicago Quinlan School of Business": "luc.edu/quinlan",
    "Stevens School of Business": "stevens.edu/school-business",
    "Claremont Graduate University Drucker School": "cgu.edu/drucker",
    "Case Western Weatherhead School of Management": "weatherhead.case.edu",
    "Cincinnati Lindner College of Business": "business.uc.edu",
    "Tulsa Collins College of Business": "business.utulsa.edu",
    "Denver Daniels College of Business": "daniels.du.edu",
    "San Diego State Fowler College of Business": "business.sdsu.edu",
    "Drexel LeBow College of Business": "lebow.drexel.edu",
    "Clemson College of Business": "business.clemson.edu",
    "LSU Ourso College of Business": "business.lsu.edu",
    "Baruch Zicklin School of Business": "zicklin.baruch.cuny.edu",
    "Illinois Gies College of Business": "giesbusiness.illinois.edu",
    "Texas Tech Rawls College of Business": "rawlsbusiness.ttu.edu",
    "Oklahoma State Spears School of Business": "spears.okstate.edu",
    "TCU Neeley School of Business": "neeley.tcu.edu",
}

# Top 50 European Business Schools
EUROPEAN_BUSINESS_SCHOOLS = {
    # UK Schools
    "London Business School": "london.edu",
    "Cambridge Judge Business School": "jbs.cam.ac.uk",
    "Oxford Said Business School": "sbs.ox.ac.uk",
    "Imperial College Business School": "imperial.ac.uk/business-school",
    "Warwick Business School": "wbs.ac.uk",
    "Manchester Alliance Business School": "alliancembs.manchester.ac.uk",
    "Cass Business School": "cass.city.ac.uk",
    "Edinburgh Business School": "business-school.ed.ac.uk",
    "Durham Business School": "dur.ac.uk/business",
    "Lancaster Management School": "lancaster.ac.uk/lums",
    "Cranfield School of Management": "cranfield.ac.uk/som",
    "Strathclyde Business School": "strath.ac.uk/business",
    "Birmingham Business School": "birmingham.ac.uk/business",
    "Leeds University Business School": "business.leeds.ac.uk",
    "Nottingham Business School": "ntu.ac.uk/nbs",
    
    # France
    "INSEAD": "insead.edu",
    "HEC Paris": "hec.edu",
    "ESSEC Business School": "essec.edu",
    "ESCP Business School": "escp.eu",
    "EDHEC Business School": "edhec.edu",
    "emlyon business school": "em-lyon.com",
    "Grenoble Ecole de Management": "grenoble-em.com",
    "NEOMA Business School": "neoma-bs.com",
    "KEDGE Business School": "kedge.edu",
    "Audencia Business School": "audencia.com",
    
    # Spain
    "IESE Business School": "iese.edu",
    "ESADE Business School": "esade.edu",
    "IE Business School": "ie.edu",
    "EADA Business School": "eada.edu",
    "EAE Business School": "eae.es",
    
    # Italy
    "SDA Bocconi School of Management": "sdabocconi.it",
    "MIP Politecnico di Milano": "mip.polimi.it",
    "LUISS Business School": "businessschool.luiss.it",
    "Bologna Business School": "bbs.unibo.it",
    
    # Netherlands
    "Rotterdam School of Management": "rsm.nl",
    "Amsterdam Business School": "abs.uva.nl",
    "Nyenrode Business University": "nyenrode.nl",
    "Maastricht School of Management": "msm.nl",
    
    # Switzerland
    "IMD Business School": "imd.org",
    "St. Gallen Business School": "unisg.ch",
    
    # Germany
    "ESMT Berlin": "esmt.org",
    "Mannheim Business School": "mannheim-business-school.com",
    "WHU Otto Beisheim School of Management": "whu.edu",
    "Frankfurt School": "frankfurt-school.de",
    "HHL Leipzig": "hhl.de",
    
    # Scandinavia
    "Copenhagen Business School": "cbs.dk",
    "Stockholm School of Economics": "hhs.se",
    "BI Norwegian Business School": "bi.edu",
    "NHH Norwegian School of Economics": "nhh.no",
    
    # Other
    "INSEAD": "insead.edu",
    "Vienna University of Economics and Business": "wu.ac.at",
    "Trinity College Dublin Business School": "tcd.ie/business",
}

# Top 50 Indian Business Schools
INDIAN_BUSINESS_SCHOOLS = {
    # IIMs
    "IIM Ahmedabad": "iima.ac.in",
    "IIM Bangalore": "iimb.ac.in",
    "IIM Calcutta": "iimcal.ac.in",
    "IIM Lucknow": "iiml.ac.in",
    "IIM Kozhikode": "iimk.ac.in",
    "IIM Indore": "iimidr.ac.in",
    "IIM Shillong": "iimshillong.ac.in",
    "IIM Udaipur": "iimu.ac.in",
    "IIM Trichy": "iimtrichy.ac.in",
    "IIM Raipur": "iimraipur.ac.in",
    "IIM Ranchi": "iimranchi.ac.in",
    "IIM Kashipur": "iimkashipur.ac.in",
    "IIM Rohtak": "iimrohtak.ac.in",
    "IIM Visakhapatnam": "iimv.ac.in",
    "IIM Amritsar": "iimamritsar.ac.in",
    "IIM Bodh Gaya": "iimbg.ac.in",
    "IIM Sambalpur": "iimsambalpur.ac.in",
    "IIM Sirmaur": "iimsirmaur.ac.in",
    "IIM Nagpur": "iimnagpur.ac.in",
    "IIM Jammu": "iimj.ac.in",
    
    # Other Top Schools
    "ISB Hyderabad": "isb.edu",
    "FMS Delhi": "fms.edu",
    "XLRI Jamshedpur": "xlri.ac.in",
    "MDI Gurgaon": "mdi.ac.in",
    "SPJIMR Mumbai": "spjimr.org",
    "JBIMS Mumbai": "jbims.edu",
    "IIFT Delhi": "iift.edu",
    "NMIMS Mumbai": "nmims.edu",
    "SIBM Pune": "sibm.edu.in",
    "SCMHRD Pune": "scmhrd.edu",
    "XIM Bhubaneswar": "ximb.ac.in",
    "IMT Ghaziabad": "imt.edu",
    "IMI New Delhi": "imi.edu",
    "TAPMI Manipal": "tapmi.edu.in",
    "Great Lakes Chennai": "greatlakes.edu.in",
    "MICA Ahmedabad": "mica.ac.in",
    "FORE School of Management": "fsm.ac.in",
    "LBSIM Delhi": "lbsim.ac.in",
    "BIMTECH Noida": "bimtech.ac.in",
    "Welingkar Mumbai": "welingkar.org",
    "KJ Somaiya Mumbai": "somaiya.edu/kjsim",
    "IBS Hyderabad": "ibsindia.org",
    "Alliance Bangalore": "alliance.edu.in",
    "Amity Business School": "amity.edu",
    "Symbiosis Pune": "siu.edu.in",
    "Christ University": "christuniversity.in",
    "VIT Business School": "vit.ac.in",
    "Manipal Business School": "manipal.edu/mu/mbs",
    "Nirma University": "nirmauni.ac.in",
    "BIT Mesra": "bitmesra.ac.in",
}

# Top 50 Canadian Business Schools
CANADIAN_BUSINESS_SCHOOLS = {
    # Top Schools
    "Rotman School of Management - University of Toronto": "rotman.utoronto.ca",
    "Ivey Business School - Western University": "ivey.uwo.ca",
    "Desautels Faculty of Management - McGill University": "mcgill.ca/desautels",
    "Smith School of Business - Queen's University": "smith.queensu.ca",
    "Schulich School of Business - York University": "schulich.yorku.ca",
    "Sauder School of Business - UBC": "sauder.ubc.ca",
    "DeGroote School of Business - McMaster University": "degroote.mcmaster.ca",
    "HEC Montreal": "hec.ca",
    "Alberta School of Business - University of Alberta": "ualberta.ca/business",
    "Haskayne School of Business - University of Calgary": "haskayne.ucalgary.ca",
    "Beedie School of Business - Simon Fraser University": "beedie.sfu.ca",
    "Telfer School of Management - University of Ottawa": "telfer.uottawa.ca",
    "John Molson School of Business - Concordia University": "concordia.ca/jmsb",
    "Lazaridis School of Business - Wilfrid Laurier University": "laurier.ca/lazaridis",
    "Edwards School of Business - University of Saskatchewan": "edwards.usask.ca",
    "Gustavson School of Business - University of Victoria": "uvic.ca/gustavson",
    "Sobey School of Business - Saint Mary's University": "smu.ca/sobey",
    "Rowe School of Business - Dalhousie University": "dal.ca/faculty/rowe",
    "Asper School of Business - University of Manitoba": "umanitoba.ca/asper",
    "Sprott School of Business - Carleton University": "sprott.carleton.ca",
    "Goodman School of Business - Brock University": "brocku.ca/goodman",
    "Memorial University Faculty of Business Administration": "mun.ca/business",
    "Ted Rogers School of Management - Ryerson University": "ryerson.ca/trsm",
    "DeGroote School of Business - McMaster University": "degroote.mcmaster.ca",
    "Lang School of Business - University of Guelph": "uoguelph.ca/lang",
    "Odette School of Business - University of Windsor": "uwindsor.ca/odette",
    "Thompson Rivers University School of Business": "tru.ca/business",
    "Shannon School of Business - Cape Breton University": "cbu.ca/academics/shannon-school-of-business",
    "UQAM School of Management": "esg.uqam.ca",
    "Université Laval Faculty of Business": "fsa.ulaval.ca",
    "HEC Montreal": "hec.ca",
    "Université de Sherbrooke Business School": "usherbrooke.ca/ecole-gestion",
    "UOIT Faculty of Business": "ontariotechu.ca/fbit",
    "Nipissing University School of Business": "nipissingu.ca/academics/faculties/business",
    "Laurentian University Faculty of Management": "laurentian.ca/faculty/management",
    "Royal Roads University School of Business": "royalroads.ca/prospective-students/faculties-schools/faculty-management/school-business",
    "Mount Royal University Bissett School of Business": "mtroyal.ca/business",
    "MacEwan University School of Business": "macewan.ca/business",
    "Athabasca University Faculty of Business": "athabascau.ca/business",
    "University of Northern British Columbia School of Business": "unbc.ca/business",
    "Vancouver Island University Faculty of Management": "viu.ca/management",
    "Trinity Western University School of Business": "twu.ca/academics/school-business",
    "University of Lethbridge Dhillon School of Business": "uleth.ca/dhillon",
    "University of Regina Hill School of Business": "uregina.ca/business",
    "University of Winnipeg Faculty of Business": "uwinnipeg.ca/business-and-economics",
    "Brandon University School of Business": "brandonu.ca",
    "Saint Francis Xavier University Schwartz School of Business": "stfx.ca/academics/schwartz-school-business",
    "Acadia University Manning School of Business": "business.acadiau.ca",
    "Mount Saint Vincent University Faculty of Business": "msvu.ca",
    "University of New Brunswick Faculty of Business": "unb.ca",
}

def get_all_schools_with_domains():
    """Return all schools combined with their domains"""
    all_schools = {}
    all_schools.update(US_BUSINESS_SCHOOLS)
    all_schools.update(EUROPEAN_BUSINESS_SCHOOLS)
    all_schools.update(INDIAN_BUSINESS_SCHOOLS)
    all_schools.update(CANADIAN_BUSINESS_SCHOOLS)
    return all_schools

if __name__ == "__main__":
    print(f"Total US schools: {len(US_BUSINESS_SCHOOLS)}")
    print(f"Total European schools: {len(EUROPEAN_BUSINESS_SCHOOLS)}")
    print(f"Total Indian schools: {len(INDIAN_BUSINESS_SCHOOLS)}")
    print(f"Total Canadian schools: {len(CANADIAN_BUSINESS_SCHOOLS)}")
    print(f"Grand total: {len(get_all_schools_with_domains())}")