#!/usr/bin/env python3
"""
Generate a unique list of entities from the logo collection
"""

import os
import re
from collections import defaultdict

def normalize_name(filename):
    """Extract and normalize entity name from filename"""
    # Remove extension
    name = os.path.splitext(filename)[0]
    
    # Remove common variations
    # Remove things like _Electronics, _Corporation, _Inc, etc.
    name = re.sub(r'_(Corporation|Corp|Company|Co|Inc|LLC|Ltd|Group|Holdings|International|Global|Electronics|Systems|Technologies|Tech|Software|Solutions|Services|Digital|Media|Financial|Bank|Insurance|Healthcare|Medical|Pharma|Pharmaceutical|Retail|Manufacturing|Industries|Industrial|Automotive|Motors|Airways|Airlines|Air|Rail|Transport|Logistics|Energy|Power|Utilities|Telecom|Communications|Network|Wireless|Mobile|Broadband|Cable|Satellite|Broadcasting|Entertainment|Studios|Productions|Pictures|Films|Music|Records|Publishing|News|Magazine|Journal|Press|Daily|Times|Post|Tribune|Herald|Chronicle|Gazette|Review|Standard|National|Federal|State|Regional|Local|Municipal|County|City|Town|Village|District|Authority|Commission|Agency|Department|Bureau|Office|Center|Institute|Foundation|Trust|Fund|Association|Society|Organization|Union|Alliance|Coalition|Partnership|Consortium|Council|Board|Committee|Task_Force|Working_Group|Advisory|Panel|Forum|Summit|Conference|Convention|Expo|Fair|Festival|Show|Event|Program|Project|Initiative|Campaign|Movement|Action|Advocacy|Outreach|Support|Relief|Aid|Assistance|Help|Care|Service|Resource|Information|Education|Training|Development|Research|Study|Analysis|Assessment|Evaluation|Review|Report|Survey|Poll|Data|Statistics|Analytics|Intelligence|Insight|Strategy|Planning|Management|Operations|Administration|Governance|Leadership|Executive|Director|Manager|Supervisor|Coordinator|Specialist|Analyst|Consultant|Advisor|Expert|Professional|Technician|Engineer|Developer|Designer|Architect|Builder|Contractor|Vendor|Supplier|Provider|Partner|Client|Customer|User|Member|Participant|Stakeholder|Investor|Shareholder|Owner|Founder|CEO|President|Chairman|Board|Officer|Staff|Employee|Worker|Team|Crew|Squad|Unit|Division|Department|Branch|Section|Segment|Sector|Region|Area|Zone|Territory|Market|Industry|Field|Domain|Space|Arena|Sphere|Realm|World|Universe|Galaxy|Planet|Earth|Moon|Sun|Star|Sky|Cloud|Storm|Thunder|Lightning|Rain|Snow|Ice|Fire|Flame|Spark|Light|Dark|Shadow|Night|Day|Dawn|Dusk|Morning|Evening|Noon|Midnight|Hour|Minute|Second|Time|Clock|Calendar|Date|Year|Month|Week|Day|Today|Tomorrow|Yesterday|Now|Then|Soon|Later|Before|After|During|While|Until|Since|From|To|Through|Throughout|Within|Without|Beyond|Above|Below|Behind|Ahead|Beside|Between|Among|Across|Along|Around|Against|Toward|Away|Into|Out|Up|Down|Left|Right|Forward|Backward|North|South|East|West|Northeast|Northwest|Southeast|Southwest|Central|Middle|Inner|Outer|Upper|Lower|Top|Bottom|Front|Back|Side|Edge|Corner|Point|Line|Circle|Square|Triangle|Rectangle|Pentagon|Hexagon|Octagon|Polygon|Shape|Form|Figure|Image|Picture|Photo|Video|Audio|Text|Document|File|Folder|Directory|Path|Link|URL|Web|Site|Page|App|Application|Software|Program|System|Platform|Framework|Tool|Utility|Widget|Plugin|Extension|Module|Component|Element|Feature|Function|Method|Process|Procedure|Protocol|Standard|Specification|Requirement|Condition|Criteria|Parameter|Variable|Constant|Value|Number|String|Boolean|Array|List|Set|Map|Dictionary|Object|Class|Interface|Enum|Struct|Type|Model|View|Controller|Service|Repository|Factory|Builder|Observer|Strategy|Command|State|Template|Adapter|Bridge|Composite|Decorator|Facade|Proxy|Chain|Iterator|Mediator|Memento|Visitor|Interpreter|Flyweight)$', '', name, flags=re.IGNORECASE)
    
    return name

def main():
    base_dir = '/Users/adi/code/socratify/socratify-images/logos/images'
    
    # Collect all unique entities
    universities = set()
    business_schools = set()
    companies = set()
    
    # Process universities
    uni_dir = os.path.join(base_dir, 'universities')
    for file in os.listdir(uni_dir):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
            name = normalize_name(file)
            universities.add(name)
    
    # Process business schools
    bs_dir = os.path.join(base_dir, 'business_schools')
    for file in os.listdir(bs_dir):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
            name = normalize_name(file)
            business_schools.add(name)
    
    # Process companies
    comp_dir = os.path.join(base_dir, 'companies')
    for file in os.listdir(comp_dir):
        if file.endswith(('.png', '.jpg', '.jpeg', '.svg', '.ico', '.webp')):
            name = normalize_name(file)
            companies.add(name)
    
    print(f"UNIQUE ENTITY COUNT")
    print(f"===================")
    print(f"Universities: {len(universities)}")
    print(f"Business Schools: {len(business_schools)}")
    print(f"Companies: {len(companies)}")
    print(f"TOTAL UNIQUE ENTITIES: {len(universities) + len(business_schools) + len(companies)}")
    
    # Write to file
    with open(os.path.join(base_dir, 'UNIQUE_ENTITIES.md'), 'w') as f:
        f.write("# Unique Entity List\n\n")
        f.write(f"## Summary\n")
        f.write(f"- **Total Unique Entities**: {len(universities) + len(business_schools) + len(companies)}\n")
        f.write(f"- **Universities**: {len(universities)}\n")
        f.write(f"- **Business Schools**: {len(business_schools)}\n")
        f.write(f"- **Companies**: {len(companies)}\n\n")
        
        f.write("---\n\n")
        
        f.write(f"## UNIVERSITIES ({len(universities)})\n\n")
        for name in sorted(universities):
            f.write(f"- {name}\n")
        
        f.write("\n---\n\n")
        
        f.write(f"## BUSINESS SCHOOLS ({len(business_schools)})\n\n")
        for name in sorted(business_schools):
            f.write(f"- {name}\n")
        
        f.write("\n---\n\n")
        
        f.write(f"## COMPANIES ({len(companies)})\n\n")
        for name in sorted(companies):
            f.write(f"- {name}\n")
    
    print(f"\nCreated UNIQUE_ENTITIES.md")

if __name__ == "__main__":
    main()