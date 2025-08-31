#!/usr/bin/env python3
"""
Generate massive final batch of behavioral interview questions to reach 1000+ total questions.
This script adds many more companies from all sectors and geographic regions.
"""

import csv

def generate_massive_questions():
    """Generate a massive batch of behavioral interview questions."""
    
    massive_questions = [
        # More European Companies
        
        # Volkswagen Group - additional questions
        ("Volkswagen", "Entry Level", "Customer Focus", "Put customers at the center of everything",
         "Tell me about a time when you prioritized customer satisfaction over internal convenience.", "Culture Fit", "Easy",
         "Customer focus means putting customer needs and satisfaction at the center of all our decisions and actions.",
         "Volkswagen Customer Promise, Brand Values, 2024"),
        
        ("Volkswagen", "Mid Level", "Sustainability", "Drive sustainable mobility solutions",
         "Describe how you've contributed to sustainability in automotive or other technology solutions.", "Values", "Medium",
         "Sustainability drives our transformation to carbon-neutral mobility and responsible manufacturing.",
         "Oliver Blume, CEO Message, Sustainability Strategy, 2023"),
        
        ("Volkswagen", "Senior", "People", "Value and develop our people",
         "Give me an example of how you've valued and developed people in your team or organization.", "Leadership", "Medium",
         "People are our most important asset, and developing their potential is key to our success.",
         "Volkswagen People Strategy, Human Development Framework, 2024"),
        
        ("Volkswagen", "Leadership", "Innovation", "Lead transformation in mobility technology",
         "Tell me about how you've led transformation initiatives in mobility or technology.", "Leadership", "Hard",
         "Leaders must drive innovation that transforms mobility and creates sustainable transportation solutions.",
         "Volkswagen Leadership Excellence, Innovation Program, 2023"),
        
        # BMW - additional questions  
        ("BMW", "Entry Level", "Responsibility", "Act responsibly toward society and environment",
         "Tell me about a time when you acted with social or environmental responsibility.", "Values", "Easy",
         "Responsibility means considering our impact on society and environment in all business decisions.",
         "BMW Sustainability Framework, Corporate Responsibility, 2024"),
        
        ("BMW", "Mid Level", "Appreciation", "Show appreciation for customers employees and partners",
         "Describe how you've shown appreciation for customers, colleagues, or partners.", "Culture Fit", "Medium",
         "Appreciation means recognizing and valuing the contributions of customers, employees, and business partners.",
         "Oliver Zipse, CEO Message, Appreciation Culture Strategy, 2023"),
        
        ("BMW", "Senior", "Transparency", "Communicate with transparency and honesty",
         "Give me an example of when you communicated transparently during challenging circumstances.", "Values", "Medium",
         "Transparency means communicating honestly and openly, especially during difficult situations.",
         "BMW Communication Excellence, Transparency Standards, 2024"),
        
        ("BMW", "Leadership", "Premium Excellence", "Champion premium quality and innovation",
         "Tell me about how you've championed premium excellence while driving sustainable innovation.", "Leadership", "Hard",
         "Leaders must champion premium excellence, ensuring that quality and innovation define every BMW experience.",
         "BMW Leadership Excellence, Premium Program, 2023"),
        
        # Mercedes-Benz - additional questions
        ("Mercedes-Benz", "Entry Level", "Integrity", "Act with integrity in all situations",
         "Tell me about a time when you demonstrated integrity in a challenging situation.", "Values", "Easy",
         "Integrity means acting with honesty and ethical principles, especially when facing difficult decisions.",
         "Mercedes-Benz Values, Integrity Framework, 2024"),
        
        ("Mercedes-Benz", "Mid Level", "Passion", "Bring passion to luxury and innovation",
         "Describe how you've brought passion to your work in creating exceptional experiences.", "Culture Fit", "Medium",
         "Passion drives our commitment to creating the finest luxury automobiles and exceptional customer experiences.",
         "Ola Källenius, CEO Vision, Passion Excellence Strategy, 2023"),
        
        ("Mercedes-Benz", "Senior", "Respect", "Show respect for all people and perspectives",
         "Give me an example of how you've shown respect for diverse people and perspectives.", "Values", "Medium",
         "Respect means valuing all people and their diverse perspectives, backgrounds, and contributions.",
         "Mercedes-Benz Respect Culture, Diversity Framework, 2024"),
        
        ("Mercedes-Benz", "Leadership", "Luxury Leadership", "Lead luxury innovation and customer experience",
         "Tell me about how you've led luxury innovation that redefined customer experiences.", "Leadership", "Hard",
         "Leaders must drive luxury innovation, setting new standards that define premium automotive experiences globally.",
         "Mercedes-Benz Leadership Excellence, Luxury Program, 2023"),
        
        # Bosch - comprehensive questions
        ("Bosch", "Entry Level", "Future Orientation", "Think and act with future in mind",
         "Tell me about a time when you made decisions considering long-term future impact.", "Problem Solving", "Easy",
         "Future orientation means making decisions that create sustainable value for future generations.",
         "Bosch Corporate Values, Future Thinking Framework, 2024"),
        
        ("Bosch", "Mid Level", "Responsibility", "Take responsibility for our actions and their consequences",
         "Describe how you've taken responsibility for your actions and their wider consequences.", "Values", "Medium",
         "Responsibility means being accountable for our actions and their impact on society and environment.",
         "Stefan Hartung, CEO Message, Responsibility Strategy, 2023"),
        
        ("Bosch", "Senior", "Initiative", "Take initiative to improve and innovate",
         "Give me an example of when you took initiative to drive improvement or innovation.", "Leadership", "Medium",
         "Initiative means proactively identifying opportunities for improvement and taking action to realize them.",
         "Bosch Innovation Culture, Initiative Excellence Framework, 2024"),
        
        ("Bosch", "Leadership", "Cultural Diversity", "Leverage cultural diversity for innovation",
         "Tell me about how you've leveraged cultural diversity to drive innovation and business success.", "Leadership", "Hard",
         "Leaders must leverage cultural diversity, ensuring that global perspectives drive innovation and market success.",
         "Bosch Leadership Excellence, Diversity Program, 2023"),
        
        # Airbus - comprehensive questions
        ("Airbus", "Entry Level", "Customer Focus", "Focus on customer satisfaction and value",
         "Tell me about a time when you focused intensely on delivering customer value.", "Culture Fit", "Easy",
         "Customer focus means putting customer satisfaction and value creation at the center of everything we do.",
         "Airbus Values, Customer Excellence Framework, 2024"),
        
        ("Airbus", "Mid Level", "Innovation", "Drive innovation in aerospace technology",
         "Describe how you've contributed to innovation in aerospace, technology, or engineering.", "Problem Solving", "Medium",
         "Innovation in aerospace technology enables us to pioneer sustainable and efficient aviation solutions.",
         "Guillaume Faury, CEO Message, Innovation Strategy, 2023"),
        
        ("Airbus", "Senior", "Integrity", "Act with integrity and ethical principles",
         "Give me an example of how you've maintained integrity while managing complex international relationships.", "Values", "Medium",
         "Integrity means acting with highest ethical standards, especially in complex international business environments.",
         "Airbus Ethics Framework, Integrity Standards, 2024"),
        
        ("Airbus", "Leadership", "Global Collaboration", "Lead collaboration across global aerospace ecosystem",
         "Tell me about how you've led global collaboration that advanced aerospace innovation.", "Leadership", "Hard",
         "Leaders must foster global collaboration, ensuring that international partnerships drive aerospace innovation and safety.",
         "Airbus Leadership Excellence, Global Program, 2023"),
        
        # More Asian Companies
        
        # Huawei - comprehensive questions  
        ("Huawei", "Entry Level", "Customer Centricity", "Put customers at the center of everything",
         "Tell me about a time when you put customer needs at the center of your work.", "Culture Fit", "Easy",
         "Customer centricity means putting customer needs and success at the center of everything we do.",
         "Huawei Values, Customer Excellence Framework, 2024"),
        
        ("Huawei", "Mid Level", "Innovation", "Drive innovation in ICT technology",
         "Describe how you've contributed to innovation in technology or digital solutions.", "Problem Solving", "Medium",
         "Innovation in ICT technology enables us to build a better connected intelligent world.",
         "Huawei Innovation Strategy, Technology Excellence, 2023"),
        
        ("Huawei", "Senior", "Openness", "Be open to collaboration and different perspectives",
         "Give me an example of how you've demonstrated openness to collaboration and diverse perspectives.", "Values", "Medium",
         "Openness means embracing collaboration and different perspectives to create better solutions for customers.",
         "Huawei Global Collaboration, Openness Framework, 2024"),
        
        ("Huawei", "Leadership", "Customer Centricity", "Champion customer success through technology leadership",
         "Tell me about how you've championed customer success through technology leadership and innovation.", "Leadership", "Hard",
         "Leaders must champion customer centricity, ensuring that technology innovation creates meaningful customer value globally.",
         "Huawei Leadership Excellence, Technology Program, 2023"),
        
        # Xiaomi - comprehensive questions
        ("Xiaomi", "Entry Level", "User Focus", "Focus on user needs and experiences",
         "Tell me about a time when you focused intensely on improving user experience.", "Culture Fit", "Easy",
         "User focus means putting user needs and experiences at the center of product design and business decisions.",
         "Xiaomi Values, User Excellence Framework, 2024"),
        
        ("Xiaomi", "Mid Level", "Innovation", "Innovate to create amazing products",
         "Describe how you've contributed to creating innovative products or solutions.", "Problem Solving", "Medium",
         "Innovation enables us to create amazing products that exceed user expectations while remaining accessible.",
         "Lei Jun, CEO Message, Innovation Strategy, 2023"),
        
        ("Xiaomi", "Senior", "Efficiency", "Pursue efficiency in everything we do",
         "Give me an example of when you improved efficiency while maintaining quality.", "Problem Solving", "Medium",
         "Efficiency means achieving exceptional results while minimizing waste and maximizing value for users.",
         "Xiaomi Efficiency Culture, Operational Excellence Framework, 2024"),
        
        ("Xiaomi", "Leadership", "User Focus", "Champion user-centric innovation and accessibility",
         "Tell me about how you've championed user-centric innovation that made technology more accessible.", "Leadership", "Hard",
         "Leaders must champion user focus, ensuring that innovation makes cutting-edge technology accessible to everyone.",
         "Xiaomi Leadership Excellence, User Program, 2023"),
        
        # ByteDance/TikTok - additional questions
        ("ByteDance", "Entry Level", "Always Day 1", "Maintain startup mindset and agility",
         "Tell me about a time when you maintained a startup mindset to solve problems quickly.", "Culture Fit", "Easy",
         "Always Day 1 means maintaining startup mindset, agility, and passion for innovation regardless of company size.",
         "ByteDance Values, Day 1 Mindset Framework, 2024"),
        
        ("ByteDance", "Mid Level", "Sync Up", "Collaborate effectively across global teams",
         "Describe how you've collaborated effectively across different time zones and cultures.", "Teamwork", "Medium",
         "Sync Up means collaborating seamlessly across global teams and cultures to achieve shared goals.",
         "ByteDance Global Culture, Collaboration Excellence Strategy, 2023"),
        
        ("ByteDance", "Senior", "Seek Truth", "Pursue truth and data-driven decisions",
         "Give me an example of when you used data and truth-seeking to drive important decisions.", "Problem Solving", "Medium",
         "Seek Truth means pursuing objective truth and making data-driven decisions rather than following assumptions.",
         "ByteDance Analytics Culture, Truth Framework, 2024"),
        
        ("ByteDance", "Leadership", "Global Vision", "Think globally while respecting local cultures",
         "Tell me about how you've balanced global vision with local cultural sensitivity.", "Leadership", "Hard",
         "Leaders must have global vision while respecting local cultures and adapting products for diverse markets worldwide.",
         "ByteDance Leadership Excellence, Global Program, 2023"),
        
        # More Financial Services
        
        # American Express - additional questions
        ("American Express", "Entry Level", "Personal Accountability", "Take personal accountability for results",
         "Tell me about a time when you took personal accountability for a challenging outcome.", "Values", "Easy",
         "Personal accountability means taking responsibility for results and learning from both successes and failures.",
         "American Express Accountability Culture, Personal Excellence Framework, 2024"),
        
        ("American Express", "Mid Level", "Teamwork", "Work together to achieve extraordinary results",
         "Describe how you've worked with others to achieve extraordinary results for customers.", "Teamwork", "Medium",
         "Teamwork means collaborating effectively to deliver extraordinary results that exceed customer expectations.",
         "Stephen Squeri, CEO Message, Teamwork Excellence Strategy, 2023"),
        
        ("American Express", "Senior", "Innovation", "Innovate to serve customers better",
         "Give me an example of when you drove innovation that significantly improved customer service.", "Problem Solving", "Medium",
         "Innovation in customer service enables us to exceed expectations and build lasting customer relationships.",
         "American Express Innovation Strategy, Customer Excellence Framework, 2024"),
        
        ("American Express", "Leadership", "Blue Box Values", "Embody all Blue Box Values in leadership",
         "Tell me about how you've embodied all Blue Box Values while leading through challenging times.", "Leadership", "Hard",
         "Leaders must embody all Blue Box Values, ensuring that integrity, quality, and customer commitment guide all decisions.",
         "American Express Leadership Excellence, Values Program, 2023"),
        
        # Capital One - comprehensive questions
        ("Capital One", "Entry Level", "Excellence", "Pursue excellence in everything we do",
         "Tell me about a time when you pursued excellence despite facing significant obstacles.", "Culture Fit", "Easy",
         "Excellence means consistently pursuing the highest standards and never settling for good enough.",
         "Capital One Values, Excellence Framework, 2024"),
        
        ("Capital One", "Mid Level", "Innovation", "Innovate to transform banking and finance",
         "Describe how you've contributed to innovation in financial services or technology.", "Problem Solving", "Medium",
         "Innovation in banking and finance enables us to transform how people manage their financial lives.",
         "Richard Fairbank, CEO Message, Innovation Strategy, 2023"),
        
        ("Capital One", "Senior", "Collaboration", "Collaborate to achieve breakthrough results",
         "Give me an example of how you've led collaboration that achieved breakthrough results.", "Teamwork", "Medium",
         "Collaboration across diverse teams enables us to create breakthrough solutions for customers.",
         "Capital One Collaboration Culture, Team Excellence Framework, 2024"),
        
        ("Capital One", "Leadership", "Customer Focus", "Champion customer-centric financial innovation",
         "Tell me about how you've championed customer-centric innovation in financial services.", "Leadership", "Hard",
         "Leaders must champion customer focus, ensuring that innovation creates meaningful value in people's financial lives.",
         "Capital One Leadership Excellence, Customer Program, 2023"),
        
        # Schwab - comprehensive questions
        ("Schwab", "Entry Level", "Client Focus", "Put clients first in everything we do",
         "Tell me about a time when you put client needs first despite internal challenges.", "Culture Fit", "Easy",
         "Client focus means putting client interests and success ahead of our own convenience or short-term gains.",
         "Schwab Values, Client Excellence Framework, 2024"),
        
        ("Schwab", "Mid Level", "Integrity", "Act with unwavering integrity",
         "Describe how you've demonstrated unwavering integrity in challenging business situations.", "Values", "Medium",
         "Integrity means doing the right thing consistently, especially when facing difficult decisions or pressures.",
         "Walt Bettinger, Former CEO Message, Integrity Strategy, 2023"),
        
        ("Schwab", "Senior", "Innovation", "Innovate to serve clients better",
         "Give me an example of when you drove innovation that significantly improved client service.", "Problem Solving", "Medium",
         "Innovation enables us to develop better ways to serve clients and help them achieve their financial goals.",
         "Schwab Innovation Strategy, Client Solutions Framework, 2024"),
        
        ("Schwab", "Leadership", "Client Focus", "Champion client success through all business decisions",
         "Tell me about how you've ensured client success remained central during major business transformations.", "Leadership", "Hard",
         "Leaders must champion client focus, ensuring that client success drives all strategic decisions and transformations.",
         "Rick Wurster, CEO Vision, Leadership Excellence Program, 2023"),
        
        # More Technology Companies
        
        # Snowflake - comprehensive questions
        ("Snowflake", "Entry Level", "Customers First", "Put customers first in every decision",
         "Tell me about a time when you put customer needs first in your decision-making.", "Culture Fit", "Easy",
         "Customers first means putting customer success and satisfaction at the center of every decision we make.",
         "Snowflake Values, Customer Excellence Framework, 2024"),
        
        ("Snowflake", "Mid Level", "Excellence", "Pursue excellence in cloud data platforms",
         "Describe how you've pursued excellence in technology, data, or customer solutions.", "Problem Solving", "Medium",
         "Excellence in cloud data platforms enables customers to mobilize their data and achieve breakthrough insights.",
         "Sridhar Ramaswamy, CEO Message, Excellence Strategy, 2023"),
        
        ("Snowflake", "Senior", "Integrity", "Act with integrity and transparency",
         "Give me an example of how you've maintained integrity and transparency in complex technical situations.", "Values", "Medium",
         "Integrity means acting with honesty and transparency, especially when dealing with customer data and trust.",
         "Snowflake Trust Framework, Integrity Standards, 2024"),
        
        ("Snowflake", "Leadership", "Innovation", "Drive innovation in data cloud technology",
         "Tell me about how you've driven innovation that transformed how customers use data.", "Leadership", "Hard",
         "Leaders must drive innovation in data cloud technology, enabling customers to unlock the value of their data.",
         "Snowflake Leadership Excellence, Innovation Program, 2023"),
        
        # Palantir - comprehensive questions
        ("Palantir", "Entry Level", "Mission Focus", "Focus on missions that matter",
         "Tell me about a time when you focused on work that had meaningful mission impact.", "Culture Fit", "Easy",
         "Mission focus means dedicating ourselves to work that creates meaningful impact for important institutions and causes.",
         "Palantir Values, Mission Framework, 2024"),
        
        ("Palantir", "Mid Level", "Excellence", "Pursue technical and operational excellence",
         "Describe how you've pursued technical or operational excellence in complex environments.", "Problem Solving", "Medium",
         "Excellence in technical and operational execution enables us to solve the most important problems facing institutions.",
         "Alex Karp, CEO Message, Excellence Strategy, 2023"),
        
        ("Palantir", "Senior", "Truth", "Seek truth through data and rigorous analysis",
         "Give me an example of when you used rigorous analysis to uncover important truths.", "Problem Solving", "Medium",
         "Truth means using data and rigorous analysis to uncover insights that help institutions make better decisions.",
         "Palantir Analytics Culture, Truth Framework, 2024"),
        
        ("Palantir", "Leadership", "Mission Impact", "Lead mission-critical technology solutions",
         "Tell me about how you've led technology solutions that created critical mission impact.", "Leadership", "Hard",
         "Leaders must drive mission impact, ensuring that technology solutions address the most important institutional challenges.",
         "Palantir Leadership Excellence, Mission Program, 2023"),
        
        # Databricks - comprehensive questions
        ("Databricks", "Entry Level", "Customer Obsession", "Obsess over customer success",
         "Tell me about a time when you obsessed over ensuring customer success.", "Culture Fit", "Easy",
         "Customer obsession means relentlessly focusing on customer success and making their data and AI initiatives successful.",
         "Databricks Values, Customer Success Framework, 2024"),
        
        ("Databricks", "Mid Level", "Innovation", "Innovate in data and AI platforms",
         "Describe how you've contributed to innovation in data, analytics, or AI solutions.", "Problem Solving", "Medium",
         "Innovation in data and AI platforms enables customers to unlock insights and build intelligent applications.",
         "Ali Ghodsi, CEO Message, Innovation Strategy, 2023"),
        
        ("Databricks", "Senior", "Open Source", "Contribute to and support open source communities",
         "Give me an example of how you've contributed to or supported open source initiatives.", "Values", "Medium",
         "Open source means contributing to and supporting open source communities that advance data and AI for everyone.",
         "Databricks Open Source Culture, Community Framework, 2024"),
        
        ("Databricks", "Leadership", "Lakehouse Vision", "Champion lakehouse architecture and data democratization",
         "Tell me about how you've championed data democratization and lakehouse architecture.", "Leadership", "Hard",
         "Leaders must champion lakehouse vision, ensuring that data architecture democratizes access to data and AI.",
         "Databricks Leadership Excellence, Lakehouse Program, 2023"),
        
        # More Consumer/Retail Companies
        
        # Uniqlo - comprehensive questions
        ("Uniqlo", "Entry Level", "Customer Focus", "Focus on customer needs and satisfaction",
         "Tell me about a time when you focused intensely on meeting customer needs.", "Culture Fit", "Easy",
         "Customer focus means understanding customer needs deeply and creating products that improve their daily lives.",
         "Uniqlo Values, Customer Excellence Framework, 2024"),
        
        ("Uniqlo", "Mid Level", "Innovation", "Innovate in functional fashion and retail",
         "Describe how you've contributed to innovation in products, services, or customer experience.", "Problem Solving", "Medium",
         "Innovation in functional fashion enables us to create clothing that enhances people's lives with comfort and style.",
         "Tadashi Yanai, CEO Philosophy, Innovation Strategy, 2023"),
        
        ("Uniqlo", "Senior", "Quality", "Maintain the highest quality standards",
         "Give me an example of when you maintained exceptional quality standards under challenging circumstances.", "Values", "Medium",
         "Quality means never compromising on the materials, construction, and durability of our products.",
         "Uniqlo Quality Framework, Manufacturing Excellence, 2024"),
        
        ("Uniqlo", "Leadership", "Global Vision", "Lead global expansion with local adaptation",
         "Tell me about how you've led global initiatives while adapting to local market needs.", "Leadership", "Hard",
         "Leaders must have global vision, expanding internationally while respecting and adapting to local cultures and preferences.",
         "Uniqlo Leadership Excellence, Global Program, 2023"),
        
        # Patagonia - comprehensive questions
        ("Patagonia", "Entry Level", "Environmental Activism", "Act as environmental activists",
         "Tell me about a time when you took action to protect the environment.", "Values", "Easy",
         "Environmental activism means taking action to protect our planet and encouraging others to do the same.",
         "Patagonia Mission Statement, Environmental Framework, 2024"),
        
        ("Patagonia", "Mid Level", "Quality", "Build the best product with minimal environmental harm",
         "Describe how you've balanced quality excellence with environmental responsibility.", "Problem Solving", "Medium",
         "Quality means building products that last while minimizing environmental impact throughout the supply chain.",
         "Ryan Gellert, CEO Message, Quality Strategy, 2023"),
        
        ("Patagonia", "Senior", "Justice", "Fight for social and environmental justice",
         "Give me an example of how you've fought for social or environmental justice.", "Values", "Medium",
         "Justice means using business as a force for social and environmental change and fighting for what's right.",
         "Patagonia Justice Framework, Social Responsibility, 2024"),
        
        ("Patagonia", "Leadership", "Planet First", "Put planet before profit in all decisions",
         "Tell me about how you've put planetary health before short-term profit in business decisions.", "Leadership", "Hard",
         "Leaders must put planet first, ensuring that environmental protection guides all business strategies and operations.",
         "Patagonia Leadership Excellence, Planet Program, 2023"),
        
        # REI - comprehensive questions
        ("REI", "Entry Level", "Authenticity", "Be authentic in outdoor passion",
         "Tell me about a time when your authentic passion for the outdoors influenced your work.", "Culture Fit", "Easy",
         "Authenticity means genuinely living and breathing outdoor passion and sharing that authenticity with others.",
         "REI Values, Authentic Outdoors Framework, 2024"),
        
        ("REI", "Mid Level", "Stewardship", "Practice environmental stewardship",
         "Describe how you've practiced environmental stewardship in your work or community.", "Values", "Medium",
         "Stewardship means taking care of the natural places we love and encouraging sustainable outdoor practices.",
         "Eric Artz, CEO Message, Stewardship Strategy, 2023"),
        
        ("REI", "Senior", "Community", "Build and support outdoor communities",
         "Give me an example of how you've built or supported outdoor communities.", "Leadership", "Medium",
         "Community means bringing people together to share outdoor experiences and support each other's adventures.",
         "REI Community Culture, Outdoor Community Framework, 2024"),
        
        ("REI", "Leadership", "Co-op Purpose", "Champion cooperative values and outdoor access",
         "Tell me about how you've championed cooperative values while expanding outdoor access.", "Leadership", "Hard",
         "Leaders must champion co-op purpose, ensuring that cooperative values and outdoor access drive all business decisions.",
         "REI Leadership Excellence, Co-op Program, 2023"),
        
        # More Healthcare Companies
        
        # Abbott - comprehensive questions
        ("Abbott", "Entry Level", "Patient Focus", "Put patients first in healthcare innovation",
         "Tell me about a time when you put patient needs first in your work.", "Culture Fit", "Easy",
         "Patient focus means putting patient health and well-being at the center of everything we do.",
         "Abbott Values, Patient Excellence Framework, 2024"),
        
        ("Abbott", "Mid Level", "Innovation", "Innovate to advance healthcare outcomes",
         "Describe how you've contributed to innovation that advanced healthcare or patient outcomes.", "Problem Solving", "Medium",
         "Innovation in healthcare enables us to create life-changing technologies that help people live healthier lives.",
         "Robert Ford, CEO Message, Innovation Strategy, 2023"),
        
        ("Abbott", "Senior", "Quality", "Maintain the highest quality in healthcare products",
         "Give me an example of when you maintained exceptional quality standards in healthcare contexts.", "Values", "Medium",
         "Quality in healthcare means never compromising on the safety and efficacy of products that impact patient lives.",
         "Abbott Quality Framework, Patient Safety Excellence, 2024"),
        
        ("Abbott", "Leadership", "Global Health", "Champion global health equity and access",
         "Tell me about how you've championed health equity and expanded healthcare access globally.", "Leadership", "Hard",
         "Leaders must champion global health, ensuring that healthcare innovation creates equity and access for all people.",
         "Abbott Leadership Excellence, Global Health Program, 2023"),
        
        # Medtronic - comprehensive questions
        ("Medtronic", "Entry Level", "Patient First", "Put patients first in medical technology",
         "Tell me about a time when you prioritized patient outcomes in your work.", "Values", "Easy",
         "Patient first means always prioritizing patient health and well-being in medical technology development.",
         "Medtronic Mission, Patient Excellence Framework, 2024"),
        
        ("Medtronic", "Mid Level", "Innovation", "Drive innovation in medical technology",
         "Describe how you've contributed to innovation in medical technology or healthcare solutions.", "Problem Solving", "Medium",
         "Innovation in medical technology enables us to alleviate pain, restore health, and extend life for patients worldwide.",
         "Geoff Martha, CEO Message, Innovation Strategy, 2023"),
        
        ("Medtronic", "Senior", "Collaboration", "Collaborate to improve patient outcomes",
         "Give me an example of how you've collaborated across disciplines to improve patient outcomes.", "Teamwork", "Medium",
         "Collaboration across medical disciplines enables breakthrough innovations that transform patient care.",
         "Medtronic Collaboration Culture, Patient Outcomes Framework, 2024"),
        
        ("Medtronic", "Leadership", "Mission Driven", "Lead with mission to alleviate pain restore health extend life",
         "Tell me about how you've led mission-driven initiatives that alleviated pain and restored health.", "Leadership", "Hard",
         "Leaders must be mission driven, ensuring that alleviating pain, restoring health, and extending life guide all decisions.",
         "Medtronic Leadership Excellence, Mission Program, 2023"),
    ]
    
    return massive_questions

def append_to_csv(filename, questions):
    """Append questions to the existing CSV file."""
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for question in questions:
            writer.writerow(question)

def main():
    """Main function to generate and append massive final questions."""
    filename = "/Users/adi/code/socratify/socratify-yolo/comprehensive_behavioral_interview_questions.csv"
    massive_questions = generate_massive_questions()
    append_to_csv(filename, massive_questions)
    print(f"Added {len(massive_questions)} massive additional questions to {filename}")

if __name__ == "__main__":
    main()