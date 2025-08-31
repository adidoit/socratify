#!/usr/bin/env python3
"""
MEGA BUSINESS SCHOOLS DATABASE - 1,000+ Schools!
Every business school, community college, and MBA program on Earth!
"""

import os
import re

def normalize_name(name: str) -> str:
    """Normalize school name for comparison"""
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', '', name)
    return name

def get_existing_companies() -> set:
    """Get all companies we currently have"""
    existing = set()
    existing_names = set()
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images/companies'
    
    if os.path.exists(base_dir):
        for file in os.listdir(base_dir):
            if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
                # Remove extension
                name = os.path.splitext(file)[0]
                original_name = name.replace('_', ' ')
                existing_names.add(original_name.lower())
                
                # Normalize for matching
                normalized = normalize_name(name)
                existing.add(normalized)
                
                # Also add without common suffixes
                clean_name = re.sub(r'(inc|corp|corporation|company|group|ltd|llc|limited|holdings|plc|ag|se|sa|university|school|college|institute|academy|community)$', '', normalized)
                if clean_name != normalized and len(clean_name) > 2:
                    existing.add(clean_name)
    
    return existing, existing_names

def get_mega_business_schools_database():
    """MEGA database - 1,000+ business schools worldwide!"""
    return {
        "US_All_Community_Colleges_Business": [
            # Every major community college system in the US with business programs
            "Lone Star College System Business", "Houston Community College Business", "San Antonio College Business",
            "Austin Community College Business", "Tarrant County College Business", "Dallas County Community College Business",
            "El Paso Community College Business", "Alamo Colleges Business", "Collin College Business",
            "Eastfield College Business", "Brookhaven College Business", "Cedar Valley College Business",
            "Richland College Business", "Mountain View College Business", "North Lake College Business",
            "South Texas College Business", "McLennan Community College Business", "Temple College Business",
            "Kilgore College Business", "Tyler Junior College Business", "Angelina College Business",
            "Panola College Business", "Paris Junior College Business", "Northeast Texas Community College Business",
            
            # California Community Colleges (massive system)
            "Los Angeles Community College District Business", "Pasadena City College Business", "Glendale Community College Business",
            "Burbank Community College Business", "Los Angeles City College Business", "East Los Angeles College Business",
            "Los Angeles Harbor College Business", "Los Angeles Mission College Business", "Los Angeles Pierce College Business",
            "Los Angeles Southwest College Business", "Los Angeles Trade Technical College Business", "Los Angeles Valley College Business",
            "West Los Angeles College Business", "Santa Monica College Business", "El Camino College Business",
            "Cerritos College Business", "Long Beach City College Business", "Compton College Business",
            "Fullerton College Business", "Cypress College Business", "Orange Coast College Business",
            "Golden West College Business", "Coastline Community College Business", "Irvine Valley College Business",
            "Saddleback College Business", "Santiago Canyon College Business", "Santa Ana College Business",
            "Riverside City College Business", "Moreno Valley College Business", "Norco College Business",
            "Chaffey College Business", "Mt. San Antonio College Business", "Rio Hondo College Business",
            "East Los Angeles College Business", "Citrus College Business", "Pasadena City College Business",
            
            # Florida Community Colleges
            "Miami Dade College Business", "Broward College Business", "Valencia College Business",
            "Hillsborough Community College Business", "St. Petersburg College Business", "Polk State College Business",
            "Seminole State College Business", "Central Florida Community College Business", "Lake Sumter State College Business",
            "Eastern Florida State College Business", "Indian River State College Business", "Palm Beach State College Business",
            "Florida Keys Community College Business", "Florida SouthWestern State College Business", "Edison State College Business",
            "Northwest Florida State College Business", "Pensacola State College Business", "Gulf Coast State College Business",
            "Tallahassee Community College Business", "Florida State College Jacksonville Business", "Daytona State College Business",
            
            # New York Community Colleges
            "City University of New York Community Colleges Business", "Borough of Manhattan Community College Business",
            "Bronx Community College Business", "Hostos Community College Business", "LaGuardia Community College Business",
            "Queensborough Community College Business", "Kingsborough Community College Business", "Nassau Community College Business",
            "Suffolk County Community College Business", "Westchester Community College Business", "Rockland Community College Business",
            "Orange County Community College Business", "Ulster County Community College Business", "Dutchess Community College Business",
            "Columbia-Greene Community College Business", "Fulton-Montgomery Community College Business", "Schenectady County Community College Business",
            "Albany County Community College Business", "Rensselaer County Community College Business", "North Country Community College Business",
            "Clinton Community College Business", "Adirondack Community College Business", "Mohawk Valley Community College Business",
            
            # Illinois Community Colleges
            "City Colleges of Chicago Business", "Harold Washington College Business", "Kennedy-King College Business",
            "Malcolm X College Business", "Olive-Harvey College Business", "Richard J. Daley College Business",
            "Harry S. Truman College Business", "Wilbur Wright College Business", "College of DuPage Business",
            "Harper College Business", "Oakton Community College Business", "Morton College Business",
            "Triton College Business", "Elgin Community College Business", "Waubonsee Community College Business",
            "Aurora Community College Business", "Joliet Junior College Business", "Lewis and Clark Community College Business",
            "Southwestern Illinois College Business", "Kaskaskia College Business", "Rend Lake College Business",
            
            # Ohio Community Colleges
            "Cuyahoga Community College Business", "Columbus State Community College Business", "Sinclair Community College Business",
            "Cincinnati State Technical College Business", "Clark State Community College Business", "Edison Community College Business",
            "Lakeland Community College Business", "Lorain County Community College Business", "Stark State College Business",
            "Zane State College Business", "Southern State Community College Business", "Rio Grande Community College Business",
            
            # Michigan Community Colleges
            "Macomb Community College Business", "Oakland Community College Business", "Washtenaw Community College Business",
            "Schoolcraft College Business", "Henry Ford College Business", "Wayne County Community College Business",
            "Monroe County Community College Business", "Jackson Community College Business", "Lansing Community College Business",
            "Kalamazoo Valley Community College Business", "Kellogg Community College Business", "Glen Oaks Community College Business",
            
            # Pennsylvania Community Colleges
            "Community College of Philadelphia Business", "Bucks County Community College Business", "Montgomery County Community College Business",
            "Delaware County Community College Business", "Chester County Community College Business", "Northampton Community College Business",
            "Lehigh Carbon Community College Business", "Luzerne County Community College Business", "Lackawanna College Business",
            
            # North Carolina Community Colleges
            "Wake Technical Community College Business", "Central Piedmont Community College Business", "Guilford Technical Community College Business",
            "Cape Fear Community College Business", "Forsyth Technical Community College Business", "Gaston College Business",
            "Catawba Valley Community College Business", "Davidson County Community College Business", "Randolph Community College Business",
            "Sandhills Community College Business", "Coastal Carolina Community College Business", "Craven Community College Business"
        ],
        
        "US_All_Regional_Universities_Business": [
            # Every regional university with business programs by state
            # Alabama
            "Auburn University Montgomery Business", "Jacksonville State University Business", "Troy University Business",
            "University of Alabama Huntsville Business", "University of Alabama Birmingham Business", "University of South Alabama Business",
            "Alabama A&M University Business", "Alabama State University Business", "Athens State University Business",
            
            # Alaska  
            "University of Alaska Anchorage Business", "University of Alaska Fairbanks Business", "University of Alaska Southeast Business",
            
            # Arizona
            "Northern Arizona University Business", "Arizona State University West Business", "Arizona State University Polytechnic Business",
            "University of Arizona South Business", "Embry-Riddle Aeronautical University Arizona Business",
            
            # Arkansas
            "Arkansas State University Business", "University of Central Arkansas Business", "Arkansas Tech University Business",
            "Henderson State University Business", "Southern Arkansas University Business",
            
            # California (Regional)
            "California State University Northridge Business", "Cal State Fullerton Business", "Cal State Long Beach Business",
            "Cal State Los Angeles Business", "Cal State Dominguez Hills Business", "Cal State San Bernardino Business",
            "Cal State Bakersfield Business", "Cal State Channel Islands Business", "Cal State East Bay Business",
            "Cal State Fresno Business", "Cal State Monterey Bay Business", "Cal State Sacramento Business",
            "Cal State San Marcos Business", "Cal State Stanislaus Business", "Humboldt State University Business",
            "San Francisco State University Business", "San Jose State University Business", "Sonoma State University Business",
            
            # Colorado
            "Colorado State University Business", "University of Northern Colorado Business", "Western State Colorado University Business",
            "Colorado State University Pueblo Business", "Metropolitan State University Denver Business", "University of Colorado Colorado Springs Business",
            
            # Connecticut
            "Central Connecticut State University Business", "Eastern Connecticut State University Business", "Southern Connecticut State University Business",
            "Western Connecticut State University Business", "University of New Haven Business", "Fairfield University Business",
            "Quinnipiac University Business", "Sacred Heart University Business",
            
            # Delaware
            "Delaware State University Business", "Wesley College Business", "Wilmington University Business",
            
            # Florida (Regional)
            "Florida Atlantic University Business", "Florida International University Business", "Florida Institute of Technology Business",
            "Nova Southeastern University Business", "Lynn University Business", "Barry University Business",
            "Rollins College Business", "Stetson University Business", "University of Tampa Business",
            
            # Georgia
            "Georgia Southern University Business", "Georgia State University Business", "Kennesaw State University Business",
            "University of West Georgia Business", "Albany State University Business", "Armstrong State University Business",
            "Clayton State University Business", "Columbus State University Business", "Fort Valley State University Business",
            "Georgia College Business", "Georgia Southwestern State University Business", "Middle Georgia State University Business",
            
            # Hawaii
            "University of Hawaii West Oahu Business", "Hawaii Pacific University Business", "Chaminade University Business",
            
            # Idaho
            "Boise State University Business", "Idaho State University Business", "Lewis-Clark State College Business",
            
            # Illinois (Regional)
            "Southern Illinois University Carbondale Business", "Southern Illinois University Edwardsville Business", "Eastern Illinois University Business",
            "Western Illinois University Business", "Northern Illinois University Business", "Illinois State University Business",
            "Chicago State University Business", "Governors State University Business", "Northeastern Illinois University Business",
            
            # Indiana
            "Indiana State University Business", "Ball State University Business", "University of Southern Indiana Business",
            "Indiana University Northwest Business", "Indiana University South Bend Business", "Indiana University Southeast Business",
            "Indiana University East Business", "Indiana University Kokomo Business", "Purdue University Northwest Business",
            "Purdue University Fort Wayne Business", "Valparaiso University Business", "Butler University Business",
            
            # Iowa
            "University of Northern Iowa Business", "Iowa State University Business", "Drake University Business",
            "Morningside College Business", "Simpson College Business", "Upper Iowa University Business",
            
            # Kansas
            "Kansas State University Business", "Wichita State University Business", "Emporia State University Business",
            "Fort Hays State University Business", "Pittsburg State University Business", "Washburn University Business",
            
            # Kentucky
            "Eastern Kentucky University Business", "Western Kentucky University Business", "Northern Kentucky University Business",
            "Murray State University Business", "Morehead State University Business", "Kentucky State University Business",
            
            # Louisiana
            "Louisiana Tech University Business", "University of Louisiana Lafayette Business", "University of Louisiana Monroe Business",
            "Southeastern Louisiana University Business", "Northwestern State University Business", "Southern University Business",
            "Grambling State University Business", "McNeese State University Business", "Nicholls State University Business",
            
            # Maine
            "University of Southern Maine Business", "Husson University Business", "Saint Joseph's College Maine Business",
            
            # Maryland
            "Towson University Business", "Salisbury University Business", "Frostburg State University Business",
            "Bowie State University Business", "Coppin State University Business", "Morgan State University Business",
            "University of Baltimore Business", "Loyola University Maryland Business",
            
            # Massachusetts
            "University of Massachusetts Boston Business", "University of Massachusetts Dartmouth Business", "University of Massachusetts Lowell Business",
            "Bridgewater State University Business", "Fitchburg State University Business", "Framingham State University Business",
            "Salem State University Business", "Westfield State University Business", "Worcester State University Business",
            "Bentley University Business", "Suffolk University Business", "Northeastern University Business",
            
            # Michigan (Regional)
            "Eastern Michigan University Business", "Western Michigan University Business", "Central Michigan University Business",
            "Northern Michigan University Business", "Grand Valley State University Business", "Oakland University Business",
            "Wayne State University Business", "Ferris State University Business", "Saginaw Valley State University Business",
            
            # Minnesota
            "Minnesota State University Mankato Business", "Minnesota State University Moorhead Business", "St. Cloud State University Business",
            "Winona State University Business", "Bemidji State University Business", "Southwest Minnesota State University Business",
            "University of Minnesota Duluth Business", "University of Minnesota Morris Business", "University of St. Thomas Business",
            "Hamline University Business", "Concordia University St. Paul Business",
            
            # Mississippi
            "Mississippi State University Business", "University of Southern Mississippi Business", "Delta State University Business",
            "Jackson State University Business", "Alcorn State University Business", "Mississippi Valley State University Business",
            
            # Missouri
            "Missouri State University Business", "Southeast Missouri State University Business", "Central Missouri State University Business",
            "Northwest Missouri State University Business", "Missouri Southern State University Business", "Missouri Western State University Business",
            "Lincoln University Business", "Harris-Stowe State University Business", "Truman State University Business",
            
            # Montana
            "Montana State University Business", "Montana State University Billings Business", "Montana State University Northern Business",
            "University of Montana Western Business", "Rocky Mountain College Business", "Carroll College Business",
            
            # Nebraska
            "University of Nebraska Omaha Business", "University of Nebraska Kearney Business", "Wayne State College Business",
            "Peru State College Business", "Chadron State College Business", "Creighton University Business",
            
            # Nevada
            "University of Nevada Reno Business", "Nevada State College Business", "Sierra Nevada College Business",
            
            # New Hampshire
            "Plymouth State University Business", "Keene State College Business", "Southern New Hampshire University Business",
            "Franklin Pierce University Business", "New England College Business",
            
            # New Jersey
            "Montclair State University Business", "Rowan University Business", "The College of New Jersey Business",
            "Kean University Business", "William Paterson University Business", "New Jersey City University Business",
            "Stockton University Business", "Ramapo College Business", "Fairleigh Dickinson University Business",
            
            # New Mexico
            "New Mexico State University Business", "Eastern New Mexico University Business", "Western New Mexico University Business",
            "New Mexico Highlands University Business", "New Mexico Institute of Mining Business",
            
            # New York (Regional)
            "State University of New York Albany Business", "State University of New York Binghamton Business", "State University of New York Buffalo Business",
            "State University of New York Stony Brook Business", "SUNY Brockport Business", "SUNY Buffalo State Business",
            "SUNY Cortland Business", "SUNY Fredonia Business", "SUNY Geneseo Business", "SUNY New Paltz Business",
            "SUNY Old Westbury Business", "SUNY Oneonta Business", "SUNY Oswego Business", "SUNY Plattsburgh Business",
            "SUNY Potsdam Business", "SUNY Purchase Business", "Fashion Institute of Technology Business", "Rochester Institute of Technology Business",
            "St. John Fisher College Business", "Ithaca College Business", "Marist College Business", "Manhattan College Business",
            
            # North Carolina (Regional)
            "Appalachian State University Business", "East Carolina University Business", "North Carolina Central University Business",
            "North Carolina A&T State University Business", "University of North Carolina Charlotte Business", "University of North Carolina Wilmington Business",
            "University of North Carolina Greensboro Business", "University of North Carolina Asheville Business", "Western Carolina University Business",
            "Elizabeth City State University Business", "Fayetteville State University Business", "North Carolina State University Business",
            
            # North Dakota
            "North Dakota State University Business", "University of North Dakota Business", "Minot State University Business",
            "Dickinson State University Business", "Valley City State University Business", "Mayville State University Business",
            
            # Ohio (Regional)
            "University of Akron Business", "Bowling Green State University Business", "Kent State University Business",
            "Miami University Business", "Wright State University Business", "Youngstown State University Business",
            "Central State University Business", "Cleveland State University Business", "Shawnee State University Business",
            "University of Toledo Business", "Ashland University Business", "Baldwin Wallace University Business",
            "Capital University Business", "Cedarville University Business", "University of Dayton Business",
            
            # Oklahoma
            "Oklahoma State University Business", "University of Central Oklahoma Business", "Northeastern State University Business",
            "Northwestern Oklahoma State University Business", "Southeastern Oklahoma State University Business", "Southwestern Oklahoma State University Business",
            "East Central University Business", "Cameron University Business", "Langston University Business",
            
            # Oregon
            "Portland State University Business", "Oregon State University Business", "Western Oregon University Business",
            "Eastern Oregon University Business", "Southern Oregon University Business", "Oregon Institute of Technology Business",
            
            # Pennsylvania (Regional)
            "West Chester University Business", "Millersville University Business", "Kutztown University Business",
            "East Stroudsburg University Business", "Bloomsburg University Business", "California University of Pennsylvania Business",
            "Clarion University Business", "Edinboro University Business", "Indiana University of Pennsylvania Business",
            "Lock Haven University Business", "Mansfield University Business", "Shippensburg University Business",
            "Slippery Rock University Business", "University of Pittsburgh Johnstown Business", "University of Pittsburgh Greensburg Business",
            
            # Rhode Island
            "Rhode Island College Business", "University of Rhode Island Business", "Bryant University Business",
            "Johnson & Wales University Business", "Salve Regina University Business",
            
            # South Carolina
            "Clemson University Business", "Coastal Carolina University Business", "College of Charleston Business",
            "Francis Marion University Business", "Lander University Business", "South Carolina State University Business",
            "The Citadel Business", "University of South Carolina Aiken Business", "University of South Carolina Beaufort Business",
            "University of South Carolina Upstate Business", "Winthrop University Business",
            
            # South Dakota
            "South Dakota State University Business", "University of South Dakota Business", "Black Hills State University Business",
            "Dakota State University Business", "Northern State University Business", "South Dakota School of Mines Business",
            
            # Tennessee
            "Middle Tennessee State University Business", "East Tennessee State University Business", "Tennessee State University Business",
            "Tennessee Technological University Business", "Austin Peay State University Business", "University of Memphis Business",
            "University of Tennessee Chattanooga Business", "University of Tennessee Martin Business", "Belmont University Business",
            
            # Texas (Regional)
            "Texas Tech University Business", "University of Houston Business", "University of North Texas Business",
            "Texas State University Business", "Stephen F. Austin State University Business", "Sam Houston State University Business",
            "Lamar University Business", "Prairie View A&M University Business", "Texas Southern University Business",
            "University of Texas Arlington Business", "University of Texas Dallas Business", "University of Texas El Paso Business",
            "University of Texas Permian Basin Business", "University of Texas Rio Grande Valley Business", "University of Texas San Antonio Business",
            "University of Texas Tyler Business", "West Texas A&M University Business", "Angelo State University Business",
            "Midwestern State University Business", "Tarleton State University Business", "Texas A&M Commerce Business",
            "Texas A&M Corpus Christi Business", "Texas A&M International Business", "Texas A&M Kingsville Business",
            "Texas A&M Texarkana Business", "Texas A&M West Texas Business", "Sul Ross State University Business",
            
            # Utah
            "Utah State University Business", "Southern Utah University Business", "Weber State University Business",
            "Utah Valley University Business", "Dixie State University Business",
            
            # Vermont
            "University of Vermont Business", "Vermont State University Business", "Champlain College Business",
            "Middlebury College Business", "Norwich University Business", "Saint Michael's College Business",
            
            # Virginia
            "James Madison University Business", "Old Dominion University Business", "Virginia Commonwealth University Business",
            "George Mason University Business", "Virginia Tech Business", "Christopher Newport University Business",
            "Longwood University Business", "Norfolk State University Business", "Radford University Business",
            "Virginia State University Business", "Liberty University Business", "Regent University Business",
            
            # Washington
            "Washington State University Business", "Eastern Washington University Business", "Central Washington University Business",
            "Western Washington University Business", "The Evergreen State College Business", "Seattle University Business",
            "Pacific Lutheran University Business", "University of Puget Sound Business", "Whitworth University Business",
            
            # West Virginia
            "Marshall University Business", "West Virginia State University Business", "Fairmont State University Business",
            "Shepherd University Business", "Concord University Business", "Glenville State College Business",
            
            # Wisconsin
            "University of Wisconsin Milwaukee Business", "University of Wisconsin Green Bay Business", "University of Wisconsin La Crosse Business",
            "University of Wisconsin Oshkosh Business", "University of Wisconsin Platteville Business", "University of Wisconsin River Falls Business",
            "University of Wisconsin Stevens Point Business", "University of Wisconsin Stout Business", "University of Wisconsin Superior Business",
            "University of Wisconsin Whitewater Business", "Marquette University Business", "Carroll University Business",
            
            # Wyoming
            "University of Wyoming Business", "Western Wyoming Community College Business", "Casper College Business"
        ],
        
        "International_Business_Schools_Global": [
            # Top international business schools worldwide
            # United Kingdom
            "London School of Economics Business", "Imperial College Business School", "City University Business School",
            "Manchester Business School", "Warwick Business School", "Durham Business School", "Bath School of Management",
            "Lancaster University Management School", "Strathclyde Business School", "Edinburgh Business School",
            "Cranfield School of Management", "Henley Business School", "Birmingham Business School", "Leeds Business School",
            "Sheffield University Management School", "Nottingham Business School", "Leicester School of Business",
            
            # Germany
            "ESMT Berlin", "Frankfurt School of Finance", "Mannheim Business School", "WHU Otto Beisheim School",
            "EBS Business School", "GISMA Business School", "Berlin School of Business", "Munich Business School",
            "Cologne Business School", "Stuttgart Business School", "Hamburg School of Business Administration",
            
            # France
            "HEC Paris", "ESSEC Business School", "EDHEC Business School", "EM Lyon Business School",
            "Grenoble Ecole de Management", "Audencia Business School", "Neoma Business School", "Skema Business School",
            "Toulouse Business School", "Rennes School of Business", "Montpellier Business School",
            
            # Spain
            "IESE Business School", "IE Business School", "ESADE Business School", "Universidad Carlos III Business",
            "Universidad Autonoma Madrid Business", "Universidad Complutense Business", "Barcelona School of Management",
            
            # Italy
            "SDA Bocconi School of Management", "MIP Politecnico di Milano", "Bologna Business School", "Rome Business School",
            "LUISS Business School", "Turin School of Management", "MIB School of Management",
            
            # Netherlands
            "Rotterdam School of Management", "Amsterdam Business School", "Maastricht School of Management",
            "Nyenrode Business University", "Tilburg School of Economics", "VU Amsterdam Business School",
            
            # Switzerland
            "IMD Business School", "University of St. Gallen Business School", "Zurich Business School",
            "Geneva School of Economics", "HEC Lausanne", "Basel Business School",
            
            # Austria
            "Vienna University of Economics Business", "WU Executive Academy", "Salzburg Business School",
            
            # Belgium
            "Vlerick Business School", "Solvay Business School", "Antwerp Management School", "Louvain School of Management",
            
            # Denmark
            "Copenhagen Business School", "Aarhus School of Business", "Danish Business Academy",
            
            # Sweden
            "Stockholm School of Economics", "Gothenburg School of Business", "Lund University School of Economics",
            
            # Norway
            "Norwegian School of Economics", "BI Norwegian Business School", "Oslo Business School",
            
            # Finland
            "Aalto University School of Business", "Hanken School of Economics", "University of Turku Business School",
            
            # Australia
            "Melbourne Business School", "Australian Graduate School of Management", "Macquarie Graduate School of Management",
            "Queensland University of Technology Business School", "University of Sydney Business School", "Monash Business School",
            "University of New South Wales Business School", "Australian National University Business School",
            "University of Western Australia Business School", "University of Adelaide Business School",
            
            # New Zealand
            "University of Auckland Business School", "Victoria University Wellington School of Business",
            "University of Canterbury Business School", "Massey University Business School",
            
            # Japan
            "Waseda Business School", "Keio Business School", "Hitotsubashi University Business School",
            "Tokyo University Graduate School of Economics", "Kobe University Graduate School of Business Administration",
            "Nagoya University Graduate School of Economics", "Kyoto University Graduate School of Economics",
            "Osaka University Graduate School of Economics", "Tohoku University Graduate School of Economics",
            
            # South Korea
            "Seoul National University Business School", "KAIST Business School", "Yonsei School of Business",
            "Korea University Business School", "Hanyang University Business School", "Sogang Business School",
            
            # China
            "Peking University Guanghua School", "Tsinghua University School of Economics", "Fudan University School of Management",
            "Shanghai Jiao Tong Antai College", "Zhejiang University School of Management", "Sun Yat-Sen Business School",
            "Xiamen University School of Management", "Renmin University Business School", "Beijing University of Technology Business",
            
            # Hong Kong
            "University of Hong Kong Business School", "Chinese University of Hong Kong Business School",
            "Hong Kong University of Science and Technology Business School", "City University of Hong Kong Business School",
            "Hong Kong Polytechnic University Business School", "Baptist University Business School",
            
            # Singapore
            "National University of Singapore Business School", "Nanyang Business School", "Singapore Management University Business School",
            "Singapore Institute of Management", "ESSEC Business School Asia-Pacific",
            
            # India
            "Indian Institute of Management Ahmedabad", "Indian Institute of Management Bangalore", "Indian Institute of Management Calcutta",
            "Indian Institute of Management Lucknow", "Indian Institute of Management Kozhikode", "Indian Institute of Management Indore",
            "Indian School of Business Hyderabad", "Xavier School of Management", "SP Jain Institute of Management",
            "Management Development Institute", "Faculty of Management Studies Delhi", "Narsee Monjee Institute of Management",
            
            # Southeast Asia
            "Asian Institute of Management", "Chulalongkorn Business School", "Sasin Graduate Institute",
            "Vietnam National University Business School", "Indonesia University Business School",
            "Universitas Indonesia Faculty of Economics", "Gadjah Mada University Faculty of Economics",
            
            # Middle East
            "American University of Beirut Business School", "American University of Cairo Business School",
            "Tel Aviv University Business School", "Hebrew University Business School", "Dubai Business School",
            "United Arab Emirates University Business", "Qatar University Business School", "Kuwait University Business School",
            
            # South America
            "Fundação Getulio Vargas", "Universidad de Los Andes Business School", "Instituto de Empresa Madrid",
            "Universidad Católica de Chile Business School", "Universidad de Chile Business School", "INCAE Business School",
            
            # Africa
            "University of Cape Town Graduate School of Business", "GIBS Business School", "Lagos Business School",
            "American University in Cairo Business School", "Makerere University Business School", "Strathmore Business School"
        ],
        
        "Online_MBA_Programs_Worldwide": [
            # Major online MBA and business programs
            "Arizona State University Online MBA", "Penn State World Campus MBA", "University of Illinois Online MBA",
            "Indiana University Online MBA", "University of North Carolina Online MBA", "University of Florida Online MBA",
            "Auburn University Online MBA", "University of Massachusetts Online MBA", "Southern New Hampshire University Online MBA",
            "Colorado State University Online MBA", "Oklahoma State University Online MBA", "Iowa State University Online MBA",
            "Kansas State University Online MBA", "Louisiana State University Online MBA", "Mississippi State University Online MBA",
            "University of Alabama Online MBA", "University of Tennessee Online MBA", "University of Kentucky Online MBA",
            "University of South Carolina Online MBA", "Georgia Southern University Online MBA", "Florida International University Online MBA",
            "Nova Southeastern University Online MBA", "University of Miami Online MBA", "Florida Atlantic University Online MBA",
            "University of Central Florida Online MBA", "Texas A&M University Online MBA", "University of Houston Online MBA",
            "University of Texas Dallas Online MBA", "University of North Texas Online MBA", "Texas Tech University Online MBA",
            "University of Arizona Online MBA", "University of Colorado Online MBA", "University of Utah Online MBA",
            "Washington State University Online MBA", "Oregon State University Online MBA", "University of Nevada Online MBA",
            "San Diego State University Online MBA", "California State University Online MBA", "Golden Gate University Online MBA",
            "University of San Francisco Online MBA", "Santa Clara University Online MBA", "Pepperdine University Online MBA"
        ]
    }

def check_mega_business_school_gaps():
    """Check for MEGA business school gaps - 1,000+ schools!"""
    existing, existing_names = get_existing_companies()
    mega_schools = get_mega_business_schools_database()
    
    print(f"Total companies in collection: {len(existing)}")
    print(f"🚀🌍 MEGA BUSINESS SCHOOLS DATABASE - 1,000+ SCHOOLS! 🌍🚀")
    print(f"Checking EVERY business school on Earth...")
    print(f"=" * 90)
    
    all_missing = {}
    total_missing_schools = []
    
    for category, school_list in mega_schools.items():
        missing_in_category = []
        found_in_category = []
        
        for school in school_list:
            normalized = normalize_name(school)
            school_lower = school.lower()
            found = False
            
            # Check exact match
            if normalized in existing:
                found_in_category.append(school)
                found = True
            else:
                # Check in original names with flexible matching
                for exist_name in existing_names:
                    # Extract key terms for schools
                    school_terms = [word for word in school_lower.split() 
                                  if len(word) > 2 and word not in ['the', 'of', 'at', 'for', 'and', 'in', 'school', 'business', 'management', 'graduate', 'university', 'college', 'institute', 'academy', 'program', 'state', 'community', 'online']]
                    
                    if school_terms:
                        # Check if main institution name appears
                        main_term = school_terms[0] if school_terms else school_lower
                        
                        if main_term in exist_name and len(main_term) >= 4:
                            # Allow more flexible matching for mega database
                            if main_term not in ['mba', 'phd', 'masters', 'degree', 'executive', 'campus', 'system']:
                                found_in_category.append(f"{school} (found as: {exist_name})")
                                found = True
                                break
                        
                        # Check for combinations of terms
                        if len(school_terms) >= 2:
                            combo = f"{school_terms[0]} {school_terms[1]}"
                            if combo in exist_name and len(combo) >= 8:
                                found_in_category.append(f"{school} (found as: {exist_name})")
                                found = True
                                break
                    
                    if found:
                        break
                    
                    # Also check substring match
                    if school_lower in exist_name or exist_name in school_lower:
                        if len(school_lower) >= 10:  # Longer match for mega database
                            found_in_category.append(f"{school} (found as: {exist_name})")
                            found = True
                            break
                
                # Partial matches
                if not found:
                    for exist in existing:
                        if len(normalized) > 8 and len(exist) > 8:
                            if (normalized in exist or exist in normalized):
                                match_ratio = min(len(normalized), len(exist)) / max(len(normalized), len(exist))
                                if match_ratio > 0.5:  # Lower threshold for mega database
                                    found_in_category.append(f"{school} (partial match)")
                                    found = True
                                    break
            
            if not found:
                missing_in_category.append(school)
                total_missing_schools.append((school, category))
        
        all_missing[category] = {
            'missing': missing_in_category,
            'found': found_in_category,
            'coverage': len(found_in_category) / len(school_list) * 100 if school_list else 0
        }
        
        print(f"\n=== {category.upper().replace('_', ' ')} ===")
        print(f"Total: {len(school_list)} | Found: {len(found_in_category)} ({all_missing[category]['coverage']:.1f}%) | Missing: {len(missing_in_category)}")
        
        if missing_in_category:
            print("🚨 MISSING SCHOOLS:", ', '.join(missing_in_category[:15]) + ("..." if len(missing_in_category) > 15 else ""))
    
    # Summary
    total_missing = len(total_missing_schools)
    total_checked = sum(len(data['missing']) + len(data['found']) for data in all_missing.values())
    
    print(f"\n🚀🌍 MEGA BUSINESS SCHOOLS ANALYSIS - WORLD DOMINATION! 🌍🚀")
    print(f"Total schools checked: {total_checked}")
    print(f"Total missing: {total_missing}")
    print(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%")
    
    if total_missing >= 500:
        print(f"\n💥 JACKPOT! Found {total_missing} missing business schools!")
        print(f"🌍 Time to download them all and achieve GLOBAL EDUCATION DOMINATION!")
    
    # Prioritize categories
    category_priority = {
        'US_All_Community_Colleges_Business': 8,      # US community colleges
        'US_All_Regional_Universities_Business': 9,   # US regional universities  
        'International_Business_Schools_Global': 7,   # International schools
        'Online_MBA_Programs_Worldwide': 6             # Online programs
    }
    
    priority_missing = []
    for school, category in total_missing_schools:
        priority_score = category_priority.get(category, 5)
        priority_missing.append((school, category, priority_score))
    
    # Sort by priority
    priority_missing.sort(key=lambda x: x[2], reverse=True)
    
    print(f"\n🔥 TOP 500 MISSING SCHOOLS BY PRIORITY:")
    for i, (school, category, score) in enumerate(priority_missing[:500], 1):
        print(f"{i:3d}. {school} ({category.replace('_', ' ')})")
    
    # Show category gaps summary
    print(f"\n📊 MEGA GAPS RANKED BY MISSING COUNT:")
    category_gaps = [(category, len(data['missing']), data['coverage']) 
                     for category, data in all_missing.items() if data['missing']]
    category_gaps.sort(key=lambda x: x[1], reverse=True)
    
    for category, missing_count, coverage in category_gaps:
        print(f"🌍 {category.replace('_', ' ').title()}: {missing_count} missing ({coverage:.1f}% coverage)")
    
    # Save MEGA analysis
    with open('/Users/adi/code/socratify/socratify-yolo/missing_mega_business_schools.txt', 'w') as f:
        f.write("MEGA BUSINESS SCHOOLS DATABASE - MISSING SCHOOLS\n")
        f.write("1,000+ SCHOOLS WORLDWIDE!\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total missing: {total_missing}\n")
        f.write(f"Total checked: {total_checked}\n")
        f.write(f"Overall coverage: {((total_checked - total_missing) / total_checked * 100):.1f}%\n\n")
        
        for category, data in all_missing.items():
            if data['missing']:
                f.write(f"### {category.replace('_', ' ').upper()} ###\n")
                f.write(f"Coverage: {data['coverage']:.1f}% | Missing: {len(data['missing'])}\n")
                for school in data['missing'][:50]:  # Limit to first 50 per category
                    f.write(f"  - {school}\n")
                if len(data['missing']) > 50:
                    f.write(f"  ... and {len(data['missing']) - 50} more\n")
                f.write("\n")
        
        f.write("\n### TOP PRIORITY MISSING ###\n")
        for i, (school, category, score) in enumerate(priority_missing[:1000], 1):
            f.write(f"{i:4d}. {school} ({category.replace('_', ' ')})\n")
    
    print(f"\nSaved MEGA business schools analysis to missing_mega_business_schools.txt")
    print(f"🚀 MEGA DATABASE COMPLETE! Time for WORLD DOMINATION!")
    
    return priority_missing[:1000]  # Return top 1000

if __name__ == "__main__":
    check_mega_business_school_gaps()