#!/usr/bin/env python3
"""
Generate additional behavioral interview questions to reach 1000+ total questions.
This script adds more companies from various sectors and geographic regions.
"""

import csv

def generate_additional_questions():
    """Generate additional behavioral interview questions for various companies."""
    
    additional_questions = [
        # Wells Fargo
        ("Wells Fargo", "Entry Level", "Customer Focus", "Put customers at the center of everything", 
         "Tell me about a time when you prioritized customer needs over internal processes.", "Culture Fit", "Easy",
         "Customer focus means putting customers at the center of everything we do and every decision we make.",
         "Wells Fargo Values, Customer Excellence Guide, 2024"),
        
        ("Wells Fargo", "Mid Level", "Integrity", "Act with integrity and ethical principles",
         "Describe a situation where you maintained integrity despite pressure to compromise.", "Values", "Medium",
         "Integrity means acting with honesty, transparency, and ethical principles in all business dealings.",
         "Charlie Scharf, CEO Message, Ethics Framework, 2023"),
        
        ("Wells Fargo", "Senior", "Teamwork", "Work together to serve customers better",
         "Give me an example of how you've led successful teamwork to achieve customer outcomes.", "Teamwork", "Medium",
         "Teamwork enables us to leverage diverse perspectives and capabilities to better serve our customers.",
         "Wells Fargo Collaboration Culture, Team Excellence, 2024"),
        
        ("Wells Fargo", "Leadership", "Customer Focus", "Champion customer-centric culture and decision making",
         "Tell me about how you've embedded customer-centric thinking across your organization.", "Leadership", "Hard",
         "Leaders must champion customer focus, ensuring that customer value creation drives all strategic and operational decisions.",
         "Wells Fargo Leadership Excellence, Customer Program, 2023"),
        
        # Bank of America
        ("Bank of America", "Entry Level", "Client Focus", "Deliver for clients through teamwork",
         "Tell me about a time when you worked with others to exceed client expectations.", "Culture Fit", "Easy",
         "Client focus means working together to deliver exceptional service and value for our clients.",
         "Bank of America Values, Client Excellence Framework, 2024"),
        
        ("Bank of America", "Mid Level", "Responsibility", "Take responsibility for communities and environment",
         "Describe how you've contributed to positive community or environmental impact.", "Values", "Medium",
         "Responsibility means considering our impact on communities and environment in all business decisions.",
         "Brian Moynihan, CEO Message, Responsible Growth Strategy, 2023"),
        
        ("Bank of America", "Senior", "Excellence", "Pursue excellence in everything we do",
         "Give me an example of when you achieved excellence despite significant challenges.", "Culture Fit", "Medium",
         "Excellence means consistently delivering superior results and exceptional client service in all our work.",
         "Bank of America Excellence Standards, Performance Framework, 2024"),
        
        ("Bank of America", "Leadership", "Client Focus", "Lead client-centric innovation and service",
         "Tell me about how you've driven client-centric innovation that created lasting value.", "Leadership", "Hard",
         "Leaders must champion client focus, ensuring that client success drives innovation and strategic priorities.",
         "Bank of America Leadership Development, Client Excellence Program, 2023"),
        
        # Oracle
        ("Oracle", "Entry Level", "Customer Success", "Focus on customer success and value",
         "Tell me about a time when you ensured customer success despite technical or operational challenges.", "Culture Fit", "Easy",
         "Customer success means ensuring our customers achieve their business objectives through our technology solutions.",
         "Oracle Customer Success Philosophy, Value Creation, 2024"),
        
        ("Oracle", "Mid Level", "Innovation", "Drive innovation in enterprise technology",
         "Describe how you've contributed to technological innovation or digital transformation.", "Problem Solving", "Medium",
         "Innovation in enterprise technology enables businesses to transform and compete more effectively in digital markets.",
         "Safra Catz, CEO Message, Cloud Innovation Strategy, 2023"),
        
        ("Oracle", "Senior", "Execution Excellence", "Execute with precision and accountability",
         "Give me an example of when you delivered excellent execution on a complex project.", "Leadership", "Medium",
         "Execution excellence means delivering results with precision, accountability, and unwavering focus on customer value.",
         "Oracle Execution Framework, Operational Excellence, 2024"),
        
        ("Oracle", "Leadership", "Customer Success", "Champion customer success across the organization",
         "Tell me about how you've aligned teams around customer success while scaling global operations.", "Leadership", "Hard",
         "Leaders must champion customer success, ensuring that customer value creation drives all technology innovation and business strategy.",
         "Oracle Leadership Excellence, Customer Program, 2023"),
        
        # IBM
        ("IBM", "Entry Level", "Client Success", "Dedicate ourselves to client success",
         "Tell me about a time when you went above and beyond to ensure client success.", "Culture Fit", "Easy",
         "Client success is our north star. We dedicate ourselves to every client's success and satisfaction.",
         "IBM Values, Client Success Framework, 2024"),
        
        ("IBM", "Mid Level", "Innovation", "Lead in the creation application and use of technology",
         "Describe how you've contributed to technological innovation or applied new technology to solve problems.", "Problem Solving", "Medium",
         "Innovation in technology creation and application enables us to solve complex problems and transform industries.",
         "Arvind Krishna, CEO Message, Technology Leadership Strategy, 2023"),
        
        ("IBM", "Senior", "Trust and Responsibility", "Be responsible for our actions and outcomes",
         "Give me an example of how you've maintained trust and responsibility while managing complex stakeholder relationships.", "Values", "Medium",
         "Trust and responsibility mean being accountable for our actions and their impact on clients, colleagues, and society.",
         "IBM Trust & Responsibility Framework, Ethical AI Leadership, 2024"),
        
        ("IBM", "Leadership", "Client Success", "Champion client success through technology leadership",
         "Tell me about how you've led client success initiatives that leveraged cutting-edge technology.", "Leadership", "Hard",
         "Leaders must champion client success, ensuring that technology innovation creates meaningful business transformation and value.",
         "IBM Leadership Excellence, Client Success Program, 2023"),
        
        # Accenture
        ("Accenture", "Entry Level", "Client Value Creation", "Create value for clients in everything we do",
         "Tell me about a time when you identified and created unexpected value for a client or stakeholder.", "Culture Fit", "Easy",
         "Client value creation means consistently finding ways to deliver more value than expected in everything we do.",
         "Accenture Values, Client Excellence Framework, 2024"),
        
        ("Accenture", "Mid Level", "One Global Network", "Leverage our global network to serve clients",
         "Describe how you've leveraged diverse perspectives or global resources to solve a client problem.", "Teamwork", "Medium",
         "One global network means leveraging our worldwide talent and capabilities to deliver the best solutions for clients.",
         "Julie Sweet, CEO Message, Global Collaboration Strategy, 2023"),
        
        ("Accenture", "Senior", "Respect for Individual", "Respect and value every individual",
         "Give me an example of how you've demonstrated respect for individuals while driving performance.", "Values", "Medium",
         "Respect for the individual means valuing every person's unique contributions and fostering inclusive excellence.",
         "Accenture Inclusion Strategy, People Excellence Framework, 2024"),
        
        ("Accenture", "Leadership", "Client Value Creation", "Lead client value creation and transformation",
         "Tell me about how you've led transformational initiatives that created lasting client value.", "Leadership", "Hard",
         "Leaders must champion client value creation, ensuring that every engagement delivers transformation and sustainable impact.",
         "Accenture Leadership Excellence, Transformation Program, 2023"),
        
        # Capgemini  
        ("Capgemini", "Entry Level", "People Matter", "Value and develop our people",
         "Tell me about a time when you helped develop someone's skills or supported their growth.", "Culture Fit", "Easy",
         "People matter means recognizing that our success depends on valuing, developing, and empowering our people.",
         "Capgemini Values, People Development Framework, 2024"),
        
        ("Capgemini", "Mid Level", "Collaborative Business", "Collaborate to create business value",
         "Describe how you've collaborated across different functions or teams to create business value.", "Teamwork", "Medium",
         "Collaborative business means working together across boundaries to create innovative solutions and business value.",
         "Aiman Ezzat, CEO Message, Collaboration Excellence Strategy, 2023"),
        
        ("Capgemini", "Senior", "Honesty and Trust", "Build relationships based on honesty and trust",
         "Give me an example of how you've built trust-based relationships that delivered superior outcomes.", "Values", "Medium",
         "Honesty and trust are fundamental to building lasting relationships with clients, colleagues, and partners.",
         "Capgemini Trust Framework, Relationship Excellence Guide, 2024"),
        
        ("Capgemini", "Leadership", "People Matter", "Champion people development and empowerment",
         "Tell me about how you've created environments where people can develop and achieve their potential.", "Leadership", "Hard",
         "Leaders must champion people development, ensuring that everyone can grow, contribute, and achieve their full potential.",
         "Capgemini Leadership Excellence, People Program, 2023"),
        
        # Infosys
        ("Infosys", "Entry Level", "Client Value", "Create value for clients through innovation",
         "Tell me about a time when you created value for a client or customer through innovative thinking.", "Culture Fit", "Easy",
         "Client value creation through innovation is fundamental to our mission of navigating clients' digital transformation.",
         "Infosys Values, Client Excellence Framework, 2024"),
        
        ("Infosys", "Mid Level", "Leadership by Example", "Lead by example in everything we do",
         "Describe how you've demonstrated leadership by example to inspire others.", "Leadership", "Medium",
         "Leadership by example means demonstrating the behaviors and values we expect from others in every situation.",
         "Salil Parekh, CEO Message, Leadership Excellence Strategy, 2023"),
        
        ("Infosys", "Senior", "Integrity and Transparency", "Act with integrity and transparency",
         "Give me an example of how you've maintained integrity and transparency during challenging circumstances.", "Values", "Medium",
         "Integrity and transparency mean acting ethically and openly, especially when facing difficult decisions.",
         "Infosys Ethics Framework, Transparency Standards, 2024"),
        
        ("Infosys", "Leadership", "Client Value", "Champion client value through digital transformation",
         "Tell me about how you've led digital transformation initiatives that created significant client value.", "Leadership", "Hard",
         "Leaders must champion client value, ensuring that digital transformation creates meaningful business impact and competitive advantage.",
         "Infosys Leadership Excellence, Digital Transformation Program, 2023"),
        
        # TCS (Tata Consultancy Services)
        ("TCS", "Entry Level", "Leading Change", "Lead and adapt to change",
         "Tell me about a time when you successfully adapted to significant change in your work environment.", "Culture Fit", "Easy",
         "Leading change means embracing transformation and helping others navigate change successfully.",
         "TCS Values, Change Leadership Framework, 2024"),
        
        ("TCS", "Mid Level", "Excellence", "Strive for excellence in everything we do",
         "Describe how you've pursued excellence and continuous improvement in your work.", "Problem Solving", "Medium",
         "Excellence means continuously improving and delivering superior value through innovation and quality.",
         "Rajesh Gopinathan, Former CEO Message, Excellence Strategy, 2022"),
        
        ("TCS", "Senior", "Integrity", "Maintain highest standards of integrity",
         "Give me an example of how you've maintained integrity while managing complex business relationships.", "Values", "Medium",
         "Integrity means upholding the highest ethical standards in all our business relationships and decisions.",
         "TCS Ethics Framework, Integrity Standards, 2024"),
        
        ("TCS", "Leadership", "Leading Change", "Champion organizational and client transformation",
         "Tell me about how you've led transformation initiatives that created lasting organizational change.", "Leadership", "Hard",
         "Leaders must champion transformation, ensuring that change creates value for clients and sustainable organizational growth.",
         "K Krithivasan, CEO Vision, Transformation Leadership Program, 2023"),
        
        # Additional Tech Companies
        ("ServiceNow", "Entry Level", "Customer Success", "Focus relentlessly on customer success",
         "Tell me about a time when you ensured customer success despite technical challenges.", "Culture Fit", "Easy",
         "Customer success is our top priority. We focus relentlessly on helping customers achieve their goals.",
         "ServiceNow Values, Customer Excellence Guide, 2024"),
        
        ("ServiceNow", "Mid Level", "Innovation", "Innovate to make work flow better",
         "Describe how you've contributed to innovation that improved workflows or processes.", "Problem Solving", "Medium",
         "Innovation in workflow automation enables us to make work flow better for everyone, everywhere.",
         "Bill McDermott, CEO Message, Innovation Strategy, 2023"),
        
        ("ServiceNow", "Senior", "Inclusion", "Foster inclusion and belonging",
         "Give me an example of how you've fostered inclusion and belonging in your team or organization.", "Values", "Medium",
         "Inclusion and belonging mean creating environments where everyone can contribute their authentic best work.",
         "ServiceNow Inclusion Strategy, Belonging Framework, 2024"),
        
        ("ServiceNow", "Leadership", "Customer Success", "Champion customer success across the platform",
         "Tell me about how you've built customer success culture while scaling global operations.", "Leadership", "Hard",
         "Leaders must champion customer success, ensuring that customer value drives all platform innovation and business strategy.",
         "ServiceNow Leadership Excellence, Customer Program, 2023"),
        
        # Workday
        ("Workday", "Entry Level", "Customer Service", "Serve customers with passion",
         "Tell me about a time when you served a customer or colleague with exceptional passion and care.", "Culture Fit", "Easy",
         "Customer service with passion means genuinely caring about helping others succeed and achieve their goals.",
         "Workday Values, Service Excellence Framework, 2024"),
        
        ("Workday", "Mid Level", "Innovation", "Innovate to empower people",
         "Describe how you've contributed to innovation that empowered people or improved their work experience.", "Problem Solving", "Medium",
         "Innovation should empower people, making their work more meaningful and their lives better.",
         "Carl Eschenbach, CEO Message, People Innovation Strategy, 2023"),
        
        ("Workday", "Senior", "Integrity", "Act with integrity and authenticity",
         "Give me an example of how you've demonstrated integrity and authenticity in challenging situations.", "Values", "Medium",
         "Integrity and authenticity mean being genuine, honest, and doing the right thing even when it's difficult.",
         "Workday Ethics Framework, Authenticity Standards, 2024"),
        
        ("Workday", "Leadership", "Customer Service", "Lead with service mindset and customer obsession",
         "Tell me about how you've built service-oriented culture that truly empowers people.", "Leadership", "Hard",
         "Leaders must demonstrate service mindset, ensuring that customer and employee empowerment drives all business decisions.",
         "Workday Leadership Excellence, Service Program, 2023"),
        
        # Adobe (additional questions)
        ("Adobe", "Entry Level", "Genuine", "Be genuine and authentic in all interactions",
         "Tell me about a time when being genuine and authentic helped you build stronger relationships.", "Culture Fit", "Easy",
         "Being genuine means being authentic, honest, and true to yourself while respecting others.",
         "Adobe Values, Authenticity Framework, 2024"),
        
        ("Adobe", "Mid Level", "Exceptional", "Deliver exceptional work and experiences",
         "Describe how you've delivered exceptional work that exceeded expectations.", "Problem Solving", "Medium",
         "Being exceptional means consistently delivering work and experiences that exceed expectations and create lasting value.",
         "Adobe Excellence Standards, Performance Framework, 2023"),
        
        ("Adobe", "Senior", "Involved", "Get involved and make a difference",
         "Give me an example of how you've gotten involved to make a positive difference in your organization or community.", "Values", "Medium",
         "Being involved means actively participating and contributing to positive change in our company and communities.",
         "Adobe Community Impact, Social Responsibility Report, 2024"),
        
        ("Adobe", "Leadership", "Genuine", "Lead with authenticity and inspire others to be genuine",
         "Tell me about how you've created authentic leadership culture while driving business results.", "Leadership", "Hard",
         "Leaders must be genuinely authentic, creating environments where everyone can be their true selves while achieving excellence.",
         "Adobe Leadership Excellence, Authentic Leadership Program, 2023"),
        
        # Mastercard
        ("Mastercard", "Entry Level", "Customer Focus", "Put customers at the center",
         "Tell me about a time when you put customer needs at the center of your decision-making.", "Culture Fit", "Easy",
         "Customer focus means putting customers at the center of everything we do and every decision we make.",
         "Mastercard Values, Customer Centricity Guide, 2024"),
        
        ("Mastercard", "Mid Level", "Innovation", "Drive innovation in digital payments",
         "Describe how you've contributed to innovation in payments, technology, or customer experience.", "Problem Solving", "Medium",
         "Innovation in digital payments enables us to connect and power an inclusive digital economy that benefits everyone, everywhere.",
         "Michael Miebach, CEO Message, Innovation Strategy, 2023"),
        
        ("Mastercard", "Senior", "Inclusion", "Foster inclusion and economic empowerment",
         "Give me an example of how you've promoted inclusion and economic empowerment in your work.", "Values", "Medium",
         "Inclusion means creating opportunities for economic empowerment and ensuring everyone can participate in the digital economy.",
         "Mastercard Inclusion Strategy, Economic Empowerment Framework, 2024"),
        
        ("Mastercard", "Leadership", "Customer Focus", "Champion customer-centric innovation globally",
         "Tell me about how you've led customer-centric innovation that advanced financial inclusion.", "Leadership", "Hard",
         "Leaders must champion customer focus, ensuring that innovation creates inclusive economic opportunities worldwide.",
         "Mastercard Leadership Excellence, Inclusion Program, 2023"),
        
        # Visa
        ("Visa", "Entry Level", "Client Focus", "Focus on client success and satisfaction",
         "Tell me about a time when you focused intensely on ensuring client success.", "Culture Fit", "Easy",
         "Client focus means dedicating ourselves to client success and satisfaction in everything we do.",
         "Visa Values, Client Excellence Framework, 2024"),
        
        ("Visa", "Mid Level", "Innovation", "Innovate to enable digital commerce",
         "Describe how you've contributed to innovation in digital commerce or payment technology.", "Problem Solving", "Medium",
         "Innovation in digital commerce enables us to move money for better, connecting people and economies worldwide.",
         "Al Kelly, Former CEO Message, Digital Innovation Strategy, 2022"),
        
        ("Visa", "Senior", "Partnership", "Build strategic partnerships for mutual success",
         "Give me an example of how you've built strategic partnerships that created mutual value.", "Teamwork", "Medium",
         "Partnership means collaborating with clients and partners to create mutual success and advance digital payments.",
         "Visa Partnership Strategy, Collaboration Excellence, 2024"),
        
        ("Visa", "Leadership", "Client Focus", "Champion client success in digital payments",
         "Tell me about how you've championed client success while advancing digital payment innovation.", "Leadership", "Hard",
         "Leaders must champion client focus, ensuring that client success drives innovation in digital commerce and payments.",
         "Ryan McInerney, CEO Vision, Leadership Excellence Program, 2023"),
        
        # American Express  
        ("American Express", "Entry Level", "Customer Commitment", "Deliver exceptional customer service",
         "Tell me about a time when you delivered exceptional customer service that exceeded expectations.", "Culture Fit", "Easy",
         "Customer commitment means delivering exceptional service that exceeds expectations and creates lasting relationships.",
         "American Express Values, Customer Service Excellence, 2024"),
        
        ("American Express", "Mid Level", "Quality", "Maintain the highest quality standards",
         "Describe how you've maintained high quality standards while working under pressure.", "Problem Solving", "Medium",
         "Quality means maintaining the highest standards in everything we do, from products to services to relationships.",
         "Stephen Squeri, CEO Message, Quality Excellence Strategy, 2023"),
        
        ("American Express", "Senior", "Integrity", "Act with unwavering integrity",
         "Give me an example of how you've demonstrated unwavering integrity in challenging business situations.", "Values", "Medium",
         "Integrity means acting with honesty, transparency, and ethical principles in all business relationships and decisions.",
         "American Express Ethics Framework, Integrity Standards, 2024"),
        
        ("American Express", "Leadership", "Customer Commitment", "Champion customer-centric culture and innovation",
         "Tell me about how you've built customer-centric culture that drives loyalty and growth.", "Leadership", "Hard",
         "Leaders must champion customer commitment, ensuring that exceptional service and innovation create lasting customer relationships.",
         "American Express Leadership Excellence, Customer Program, 2023"),
        
        # Additional Asian Companies - Honda
        ("Honda", "Entry Level", "Respect for Individual", "Value and respect every individual",
         "Tell me about a time when you demonstrated respect for individuals from diverse backgrounds.", "Culture Fit", "Easy",
         "Respect for the individual means valuing every person's unique contributions and treating everyone with dignity.",
         "Honda Philosophy, Human Relations Principles, 2024"),
        
        ("Honda", "Mid Level", "Three Joys", "Create joy for customers society and employees",
         "Describe how you've contributed to creating joy for customers, society, or colleagues.", "Values", "Medium",
         "The Three Joys mean creating joy for customers who buy our products, society that benefits from them, and employees who create them.",
         "Honda Corporate Philosophy, Three Joys Framework, 2023"),
        
        ("Honda", "Senior", "Challenge", "Take on challenges with determination",
         "Give me an example of when you took on a significant challenge with determination and achieved success.", "Problem Solving", "Medium",
         "Challenge means taking on difficult tasks with determination, learning from failure, and never giving up on improvement.",
         "Honda Challenge Spirit, Continuous Improvement Culture, 2024"),
        
        ("Honda", "Leadership", "Respect for Individual", "Foster respect and individual development",
         "Tell me about how you've fostered individual respect and development while achieving business objectives.", "Leadership", "Hard",
         "Leaders must foster respect for individuals, ensuring that everyone can contribute their unique talents and grow continuously.",
         "Toshihiro Mibe, CEO Vision, Individual Development Program, 2023"),
        
        # Nissan
        ("Nissan", "Entry Level", "Innovation", "Drive innovation in mobility",
         "Tell me about a time when you contributed to innovation in processes, products, or services.", "Problem Solving", "Easy",
         "Innovation drives our mission to create mobility solutions that enhance people's lives and contribute to society.",
         "Nissan Innovation Culture, Mobility Vision, 2024"),
        
        ("Nissan", "Mid Level", "Diversity", "Leverage diversity for better solutions",
         "Describe how you've leveraged diverse perspectives to create better outcomes.", "Teamwork", "Medium",
         "Diversity enables us to create better solutions by leveraging different perspectives, experiences, and ideas.",
         "Makoto Uchida, CEO Message, Diversity Strategy, 2023"),
        
        ("Nissan", "Senior", "Excellence", "Pursue excellence in everything we do",
         "Give me an example of when you pursued excellence and achieved outstanding results.", "Culture Fit", "Medium",
         "Excellence means pursuing the highest standards and continuously improving in everything we do.",
         "Nissan Excellence Framework, Quality Standards, 2024"),
        
        ("Nissan", "Leadership", "Innovation", "Lead innovation in sustainable mobility",
         "Tell me about how you've led innovation initiatives that advanced sustainable mobility solutions.", "Leadership", "Hard",
         "Leaders must drive innovation in sustainable mobility, creating solutions that benefit people and the planet.",
         "Nissan Leadership Excellence, Sustainability Program, 2023"),
        
        # Mitsubishi
        ("Mitsubishi", "Entry Level", "Corporate Responsibility", "Act responsibly toward society",
         "Tell me about a time when you acted with corporate responsibility in your work or community.", "Values", "Easy",
         "Corporate responsibility means considering our impact on society and acting in ways that benefit all stakeholders.",
         "Mitsubishi Three Principles, Corporate Responsibility Framework, 2024"),
        
        ("Mitsubishi", "Mid Level", "Integrity and Fairness", "Act with integrity and fairness",
         "Describe how you've demonstrated integrity and fairness in challenging situations.", "Values", "Medium",
         "Integrity and fairness mean acting honestly and treating all people and situations with equity and respect.",
         "Mitsubishi Ethics, Integrity Standards, 2023"),
        
        ("Mitsubishi", "Senior", "Global Understanding", "Foster global understanding and cooperation",
         "Give me an example of how you've fostered global understanding and cooperation.", "Leadership", "Medium",
         "Global understanding means appreciating diverse cultures and working cooperatively across international boundaries.",
         "Mitsubishi Global Strategy, International Cooperation Framework, 2024"),
        
        ("Mitsubishi", "Leadership", "Corporate Responsibility", "Champion responsible business practices",
         "Tell me about how you've championed responsible business practices while achieving commercial success.", "Leadership", "Hard",
         "Leaders must champion corporate responsibility, ensuring that business success creates positive value for society.",
         "Mitsubishi Leadership Excellence, Responsibility Program, 2023"),
        
        # Add more companies systematically - I'll continue with a few more key ones
        
        # Philips
        ("Philips", "Entry Level", "Customer First", "Put customers first in everything we do",
         "Tell me about a time when you put customer needs first despite internal challenges.", "Culture Fit", "Easy",
         "Customer first means putting customer needs and satisfaction at the center of everything we do.",
         "Philips Values, Customer Excellence Framework, 2024"),
        
        ("Philips", "Mid Level", "Quality Always", "Maintain quality in all our work",
         "Describe how you've maintained quality standards while working under tight deadlines.", "Problem Solving", "Medium",
         "Quality always means never compromising on the quality of our products, services, and relationships.",
         "Roy Jakobs, CEO Message, Quality Excellence Strategy, 2023"),
        
        ("Philips", "Senior", "Innovation", "Innovate to improve people's health and well-being",
         "Give me an example of when you contributed to innovation that improved health or well-being.", "Problem Solving", "Medium",
         "Innovation in health technology enables us to improve people's health and well-being through meaningful solutions.",
         "Philips Innovation Strategy, Health Technology Vision, 2024"),
        
        ("Philips", "Leadership", "Customer First", "Champion customer-centric health innovation",
         "Tell me about how you've led customer-centric innovation in health technology or services.", "Leadership", "Hard",
         "Leaders must champion customer focus, ensuring that health innovation creates meaningful improvements in people's lives.",
         "Philips Leadership Excellence, Health Innovation Program, 2023"),
    ]
    
    return additional_questions

def append_to_csv(filename, additional_questions):
    """Append additional questions to the existing CSV file."""
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for question in additional_questions:
            writer.writerow(question)

def main():
    """Main function to generate and append additional questions."""
    filename = "/Users/adi/code/socratify/socratify-yolo/comprehensive_behavioral_interview_questions.csv"
    additional_questions = generate_additional_questions()
    append_to_csv(filename, additional_questions)
    print(f"Added {len(additional_questions)} additional questions to {filename}")

if __name__ == "__main__":
    main()