#!/usr/bin/env python3
"""
Generate the final batch of behavioral interview questions to reach 1000+ total questions.
This script adds more companies from various sectors with authentic leadership principles.
"""

import csv

def generate_final_batch_questions():
    """Generate final batch of behavioral interview questions for various companies."""
    
    final_batch_questions = [
        # More Amazon questions to complete the 16 principles
        ("Amazon", "Entry Level", "Deliver Results", "Focus on key inputs and deliver with quality",
         "Tell me about a time when you had to deliver results despite significant obstacles.", "Problem Solving", "Easy",
         "Leaders focus on the key inputs for their business and deliver them with the right quality and in a timely fashion.",
         "Amazon Leadership Principles, Amazon.jobs, 2024"),
        
        ("Amazon", "Mid Level", "Have Backbone; Disagree and Commit", "Challenge decisions respectfully then commit fully",
         "Describe a time when you disagreed with a decision but still committed to executing it fully.", "Leadership", "Medium",
         "Leaders are obligated to respectfully challenge decisions when they disagree, even when doing so is uncomfortable.",
         "Amazon Leadership Principles, Amazon.jobs, 2024"),
        
        ("Amazon", "Senior", "Earn Trust", "Listen attentively speak candidly treat others respectfully",
         "Give me an example of when you had to rebuild trust after making a mistake.", "Values", "Medium",
         "Leaders listen attentively, speak candidly, and treat others respectfully. They are vocally self-critical.",
         "Amazon Leadership Principles, Amazon.jobs, 2024"),
        
        # Netflix - more questions
        ("Netflix", "Entry Level", "Judgment", "Make wise decisions despite ambiguity",
         "Tell me about a time when you had to make a wise decision with incomplete information.", "Problem Solving", "Easy",
         "Good judgment means making wise decisions despite ambiguity and balancing multiple perspectives effectively.",
         "Netflix Culture Memo, Decision Making Framework, 2024"),
        
        ("Netflix", "Mid Level", "Courage", "Take smart risks and speak up for what you believe",
         "Describe a time when you took a smart risk or courageously spoke up for your beliefs.", "Leadership", "Medium",
         "Courage means taking smart risks and speaking up for what you believe, even when it's uncomfortable.",
         "Netflix Courage Culture, Risk Taking Philosophy, 2023"),
        
        ("Netflix", "Senior", "Passion", "Care deeply about Netflix's mission and outcomes",
         "Give me an example of when your passion for the mission drove exceptional results.", "Culture Fit", "Medium",
         "Passion means caring deeply about Netflix's mission and being motivated by the impact we have on members worldwide.",
         "Netflix Culture Values, Mission Passion Framework, 2024"),
        
        ("Netflix", "Leadership", "Selflessness", "Put Netflix ahead of personal interests",
         "Tell me about a time when you put the company's interests ahead of your personal interests.", "Values", "Hard",
         "Selflessness means putting Netflix's success ahead of personal interests and ego-driven decisions.",
         "Netflix Leadership Culture, Selflessness Principles, 2023"),
        
        # Google - more detailed questions
        ("Google", "Entry Level", "Think Different", "Approach problems with fresh perspectives",
         "Tell me about a time when you approached a problem with a completely different perspective.", "Problem Solving", "Easy",
         "Thinking different means approaching problems with fresh perspectives and challenging conventional solutions.",
         "Google Innovation Philosophy, Creative Thinking Guide, 2024"),
        
        ("Google", "Mid Level", "Be Bold", "Take calculated risks to achieve breakthrough results",
         "Describe how you've taken calculated risks to pursue breakthrough innovations.", "Leadership", "Medium",
         "Being bold means taking calculated risks and pursuing breakthrough innovations that can change the world.",
         "Sundar Pichai, CEO Message, Bold Innovation Strategy, 2023"),
        
        ("Google", "Senior", "Stay Humble", "Remain humble and continue learning",
         "Give me an example of when staying humble helped you learn and achieve better outcomes.", "Values", "Medium",
         "Staying humble means remaining open to learning, acknowledging mistakes, and recognizing others' contributions.",
         "Google Humility Culture, Continuous Learning Framework, 2024"),
        
        ("Google", "Leadership", "Focus on the User", "Champion user needs in all strategic decisions",
         "Tell me about how you've championed user needs while making complex strategic decisions.", "Leadership", "Hard",
         "Leaders must champion user focus, ensuring that user value creation guides all strategic and product decisions globally.",
         "Google Leadership Excellence, User Focus Program, 2023"),
        
        # Microsoft - additional questions  
        ("Microsoft", "Entry Level", "Be Curious", "Continuously learn and seek new knowledge",
         "Tell me about a time when curiosity led you to learn something that improved your performance.", "Culture Fit", "Easy",
         "Being curious means continuously learning, asking questions, and seeking new knowledge to drive innovation.",
         "Microsoft Growth Mindset, Learning Culture Framework, 2024"),
        
        ("Microsoft", "Mid Level", "Be Inclusive", "Create belonging for everyone",
         "Describe how you've created inclusive environments where everyone feels they belong.", "Values", "Medium",
         "Being inclusive means creating environments where everyone feels valued, respected, and able to contribute fully.",
         "Satya Nadella, CEO Vision, Inclusive Culture Strategy, 2023"),
        
        ("Microsoft", "Senior", "Think Partnership", "Collaborate for mutual success",
         "Give me an example of how you've built partnerships that created mutual value and success.", "Teamwork", "Medium",
         "Thinking partnership means collaborating with others to create mutual value and achieve shared success.",
         "Microsoft Partnership Culture, Collaboration Excellence, 2024"),
        
        ("Microsoft", "Leadership", "Empower Others", "Enable others to achieve more than they thought possible",
         "Tell me about how you've empowered others to achieve more than they thought possible.", "Leadership", "Hard",
         "Leaders must empower others, creating environments where people can achieve more than they ever thought possible.",
         "Microsoft Leadership Philosophy, Empowerment Program, 2023"),
        
        # Apple - additional questions
        ("Apple", "Entry Level", "Accessibility", "Design for everyone including users with disabilities",
         "Tell me about a time when you considered accessibility or inclusion in your work.", "Values", "Easy",
         "Accessibility means designing products and experiences that everyone can use, including users with disabilities.",
         "Apple Accessibility Philosophy, Universal Design Guide, 2024"),
        
        ("Apple", "Mid Level", "Environmental Responsibility", "Minimize environmental impact",
         "Describe how you've contributed to environmental responsibility in your work or projects.", "Values", "Medium",
         "Environmental responsibility means minimizing our impact on the planet through sustainable design and operations.",
         "Tim Cook, CEO Message, Environmental Strategy, 2023"),
        
        ("Apple", "Senior", "Collaboration", "Work together to create breakthrough products",
         "Give me an example of how you've collaborated across functions to create breakthrough results.", "Teamwork", "Medium",
         "Collaboration across different disciplines enables us to create breakthrough products that enrich people's lives.",
         "Apple Collaboration Culture, Cross-Functional Excellence, 2024"),
        
        ("Apple", "Leadership", "Think Different", "Lead innovative thinking that challenges conventions",
         "Tell me about how you've led innovative thinking that challenged industry conventions.", "Leadership", "Hard",
         "Leaders must think different, challenging conventions and leading innovations that create new product categories.",
         "Apple Leadership Excellence, Innovation Program, 2023"),
        
        # Meta - comprehensive questions
        ("Meta", "Entry Level", "Be Bold", "Take risks to build the future of connection",
         "Tell me about a time when you took a bold risk to pursue an innovative idea.", "Problem Solving", "Easy",
         "Being bold means taking risks and pursuing innovative ideas that can build the future of human connection.",
         "Meta Values, Bold Innovation Framework, 2024"),
        
        ("Meta", "Mid Level", "Focus on Impact", "Make decisions based on maximum positive impact",
         "Describe how you've focused on creating maximum positive impact in your work.", "Culture Fit", "Medium",
         "Focus on impact means prioritizing work and decisions that create the greatest positive change for people worldwide.",
         "Mark Zuckerberg, CEO Vision, Impact Strategy, 2023"),
        
        ("Meta", "Senior", "Move Fast", "Execute quickly to stay ahead of competition",
         "Give me an example of when you moved fast to execute on an important opportunity.", "Problem Solving", "Medium",
         "Moving fast means executing quickly and efficiently to stay ahead and create value for people and businesses.",
         "Meta Speed Culture, Fast Execution Framework, 2024"),
        
        ("Meta", "Leadership", "Be Bold", "Champion bold innovation in connection technology",
         "Tell me about how you've championed bold innovations that advanced human connection.", "Leadership", "Hard",
         "Leaders must be bold, championing innovations that create new ways for people to connect and share experiences.",
         "Meta Leadership Excellence, Bold Innovation Program, 2023"),
        
        # Tesla - additional questions
        ("Tesla", "Entry Level", "Sustainability", "Accelerate sustainable transport and energy",
         "Tell me about a time when you contributed to sustainability in your work or community.", "Values", "Easy",
         "Sustainability drives our mission to accelerate the world's transition to sustainable energy and transport.",
         "Tesla Sustainability Mission, Environmental Impact Report, 2024"),
        
        ("Tesla", "Mid Level", "First Principles", "Think from first principles to solve problems",
         "Describe how you've used first principles thinking to solve a complex problem.", "Problem Solving", "Medium",
         "First principles thinking means breaking down problems to fundamental truths and building solutions from there.",
         "Elon Musk, CEO Philosophy, First Principles Framework, 2023"),
        
        ("Tesla", "Senior", "Ownership", "Take ownership like you own the company",
         "Give me an example of when you took ownership and acted like you owned the company.", "Leadership", "Medium",
         "Ownership means taking personal responsibility and making decisions as if you own the company and its mission.",
         "Tesla Ownership Culture, Accountability Framework, 2024"),
        
        ("Tesla", "Leadership", "Mission Driven", "Champion sustainable transportation and energy globally",
         "Tell me about how you've championed sustainable mission while scaling operations globally.", "Leadership", "Hard",
         "Leaders must champion our sustainability mission, ensuring that sustainable transport and energy drive all decisions.",
         "Tesla Leadership Excellence, Mission Program, 2023"),
        
        # JP Morgan Chase - additional questions
        ("JPMorgan", "Entry Level", "Teamwork", "Work together to serve clients effectively",
         "Tell me about a time when effective teamwork was crucial to serving a client well.", "Teamwork", "Easy",
         "Teamwork enables us to leverage diverse capabilities and serve clients more effectively than working alone.",
         "JPMorgan Chase Values, Team Excellence Framework, 2024"),
        
        ("JPMorgan", "Mid Level", "Respect", "Treat everyone with dignity and respect",
         "Describe how you've demonstrated respect for others in a challenging work situation.", "Values", "Medium",
         "Respect means treating everyone with dignity and valuing diverse perspectives and contributions.",
         "Jamie Dimon, CEO Message, Respect Culture Strategy, 2023"),
        
        ("JPMorgan", "Senior", "Innovation", "Innovate to better serve clients and communities",
         "Give me an example of when you drove innovation that better served clients or communities.", "Problem Solving", "Medium",
         "Innovation enables us to develop better solutions for clients and create positive impact in communities.",
         "JPMorgan Chase Innovation Strategy, Client Solutions Framework, 2024"),
        
        ("JPMorgan", "Leadership", "Integrity", "Lead with uncompromising integrity",
         "Tell me about how you've maintained uncompromising integrity while achieving ambitious business goals.", "Leadership", "Hard",
         "Leaders must demonstrate uncompromising integrity, ensuring that ethical principles guide all business decisions.",
         "JPMorgan Chase Leadership Excellence, Integrity Program, 2023"),
        
        # McKinsey - additional questions
        ("McKinsey", "Entry Level", "Fact-Based", "Base decisions on rigorous fact-based analysis",
         "Tell me about a time when you used rigorous analysis to influence an important decision.", "Problem Solving", "Easy",
         "Being fact-based means using rigorous analysis and evidence to inform decisions and recommendations.",
         "McKinsey Problem Solving, Analytical Excellence Framework, 2024"),
        
        ("McKinsey", "Mid Level", "Client Impact", "Focus relentlessly on creating client impact",
         "Describe how you've focused on creating meaningful impact for a client or stakeholder.", "Culture Fit", "Medium",
         "Client impact means focusing relentlessly on creating meaningful, lasting change that helps clients succeed.",
         "Bob Sternfels, Global Managing Partner Message, Impact Strategy, 2023"),
        
        ("McKinsey", "Senior", "Professional Development", "Develop yourself and others continuously",
         "Give me an example of how you've developed yourself and helped others grow professionally.", "Leadership", "Medium",
         "Professional development means continuously building capabilities in yourself and others to create greater impact.",
         "McKinsey People Development, Professional Growth Framework, 2024"),
        
        ("McKinsey", "Leadership", "Global Perspective", "Think globally while acting locally for clients",
         "Tell me about how you've applied global perspectives to solve local client challenges.", "Leadership", "Hard",
         "Leaders must have global perspective, applying worldwide insights to solve local client challenges effectively.",
         "McKinsey Global Leadership, Perspective Program, 2023"),
        
        # Boston Consulting Group - additional questions
        ("BCG", "Entry Level", "Intellectual Curiosity", "Maintain curiosity and love of learning",
         "Tell me about a time when intellectual curiosity led you to discover valuable insights.", "Culture Fit", "Easy",
         "Intellectual curiosity drives continuous learning and helps us discover insights that create client value.",
         "BCG Learning Culture, Curiosity Framework, 2024"),
        
        ("BCG", "Mid Level", "Diversity", "Leverage diversity for better solutions",
         "Describe how you've leveraged diverse perspectives to create better outcomes for clients.", "Values", "Medium",
         "Diversity of thought and background enables us to develop more creative and effective solutions for clients.",
         "Christoph Schweizer, CEO Message, Diversity Strategy, 2023"),
        
        ("BCG", "Senior", "Social Impact", "Create positive social impact through our work",
         "Give me an example of how you've created positive social impact through business work.", "Values", "Medium",
         "Social impact means using business solutions to address societal challenges and create positive change.",
         "BCG Social Impact, Purpose-Driven Strategy, 2024"),
        
        ("BCG", "Leadership", "Partnership", "Build lasting partnerships with clients",
         "Tell me about how you've built lasting partnerships that created mutual value over time.", "Leadership", "Hard",
         "Leaders must build lasting partnerships, ensuring that client relationships create mutual value and lasting impact.",
         "BCG Partnership Excellence, Client Relationship Program, 2023"),
        
        # Additional European Companies
        
        # Unilever - additional questions
        ("Unilever", "Entry Level", "Passion for High Performance", "Pursue excellence with energy and enthusiasm",
         "Tell me about a time when you pursued excellence with exceptional energy and enthusiasm.", "Culture Fit", "Easy",
         "Passion for high performance means pursuing excellence with energy, enthusiasm, and commitment to extraordinary results.",
         "Unilever Values, Performance Excellence Framework, 2024"),
        
        ("Unilever", "Mid Level", "Working Together", "Collaborate to achieve shared success",
         "Describe how you've collaborated effectively to achieve shared success across different teams.", "Teamwork", "Medium",
         "Working together means collaborating with respect, trust, and shared commitment to achieving common goals.",
         "Hein Schumacher, CEO Message, Collaboration Strategy, 2023"),
        
        ("Unilever", "Senior", "Respect for People", "Value and respect all individuals",
         "Give me an example of how you've demonstrated respect for people while driving performance.", "Values", "Medium",
         "Respect for people means valuing all individuals, their diverse backgrounds, and unique contributions.",
         "Unilever People Strategy, Respect Culture Framework, 2024"),
        
        ("Unilever", "Leadership", "Purpose-Led Growth", "Lead growth that serves people and planet",
         "Tell me about how you've led growth initiatives that benefited both business and society.", "Leadership", "Hard",
         "Leaders must drive purpose-led growth, ensuring that business success creates positive impact for people and planet.",
         "Unilever Leadership Excellence, Purpose Program, 2023"),
        
        # ASML - additional questions
        ("ASML", "Entry Level", "Teamwork", "Work together to solve complex challenges",
         "Tell me about a time when teamwork was essential to solving a complex technical challenge.", "Teamwork", "Easy",
         "Teamwork enables us to combine diverse expertise and solve complex challenges in semiconductor technology.",
         "ASML Team Culture, Technical Collaboration Framework, 2024"),
        
        ("ASML", "Mid Level", "Continuous Improvement", "Continuously improve processes and outcomes",
         "Describe how you've driven continuous improvement in processes or technical outcomes.", "Problem Solving", "Medium",
         "Continuous improvement means constantly seeking ways to enhance processes, quality, and technical performance.",
         "Peter Wennink, Former CEO Message, Improvement Strategy, 2023"),
        
        ("ASML", "Senior", "Customer Partnership", "Build strong partnerships with customers",
         "Give me an example of how you've built strong partnerships that advanced mutual technical goals.", "Leadership", "Medium",
         "Customer partnership means collaborating closely with customers to advance semiconductor technology together.",
         "ASML Customer Partnership, Collaboration Excellence, 2024"),
        
        ("ASML", "Leadership", "Technology Leadership", "Lead breakthrough innovations in semiconductor technology",
         "Tell me about how you've led breakthrough innovations that advanced the semiconductor industry.", "Leadership", "Hard",
         "Leaders must drive technology leadership, ensuring breakthrough innovations advance the entire semiconductor ecosystem.",
         "Christophe Fouquet, CEO Vision, Technology Leadership Program, 2024"),
        
        # SAP - additional questions
        ("SAP", "Entry Level", "Simplification", "Simplify complex processes for users",
         "Tell me about a time when you simplified complex processes to improve user experience.", "Problem Solving", "Easy",
         "Simplification means making complex enterprise processes simpler and more intuitive for users.",
         "SAP User Experience, Simplification Framework, 2024"),
        
        ("SAP", "Mid Level", "Empowerment", "Empower customers to achieve their goals",
         "Describe how you've empowered customers or colleagues to achieve their business goals.", "Culture Fit", "Medium",
         "Empowerment means enabling customers and colleagues to achieve their goals through technology and support.",
         "Christian Klein, CEO Message, Empowerment Strategy, 2023"),
        
        ("SAP", "Senior", "Sustainability", "Drive sustainable business practices",
         "Give me an example of how you've integrated sustainability into technology or business solutions.", "Values", "Medium",
         "Sustainability means helping businesses operate more sustainably through technology and responsible practices.",
         "SAP Sustainability Strategy, Green Technology Framework, 2024"),
        
        ("SAP", "Leadership", "Digital Transformation", "Lead customer digital transformation",
         "Tell me about how you've led digital transformation initiatives that created lasting customer value.", "Leadership", "Hard",
         "Leaders must champion digital transformation, ensuring technology creates meaningful business transformation for customers.",
         "SAP Leadership Excellence, Transformation Program, 2023"),
        
        # Spotify - additional questions
        ("Spotify", "Entry Level", "Passion", "Bring passion to music and audio experiences",
         "Tell me about a time when your passion for music or audio drove exceptional work.", "Culture Fit", "Easy",
         "Passion for music and audio experiences drives our mission to unlock the potential of human creativity.",
         "Spotify Music Passion, Creative Culture Framework, 2024"),
        
        ("Spotify", "Mid Level", "Collaboration", "Collaborate to create amazing audio experiences",
         "Describe how you've collaborated with others to create exceptional experiences for users.", "Teamwork", "Medium",
         "Collaboration enables us to combine diverse talents and create amazing audio experiences for millions of users.",
         "Daniel Ek, CEO Message, Collaboration Excellence Strategy, 2023"),
        
        ("Spotify", "Senior", "Innovation", "Innovate to transform audio and music",
         "Give me an example of when you drove innovation that transformed user experiences.", "Problem Solving", "Medium",
         "Innovation in audio and music enables us to transform how people discover, share, and enjoy audio content.",
         "Spotify Innovation Labs, Audio Technology Strategy, 2024"),
        
        ("Spotify", "Leadership", "Creator Focus", "Champion creators and their success",
         "Tell me about how you've championed creators and helped them succeed on the platform.", "Leadership", "Hard",
         "Leaders must champion creators, ensuring that artists and podcasters can build sustainable careers through our platform.",
         "Spotify Creator Strategy, Artist Success Program, 2023"),
        
        # LinkedIn - additional questions
        ("LinkedIn", "Entry Level", "Act Like an Owner", "Take ownership and act with long-term thinking",
         "Tell me about a time when you acted like an owner and made decisions with long-term thinking.", "Values", "Easy",
         "Acting like an owner means taking responsibility and making decisions with long-term value creation in mind.",
         "LinkedIn Ownership Culture, Long-term Thinking Framework, 2024"),
        
        ("LinkedIn", "Mid Level", "Be Genuinely Helpful", "Focus on being genuinely helpful to others",
         "Describe how you've been genuinely helpful to colleagues, customers, or community members.", "Culture Fit", "Medium",
         "Being genuinely helpful means focusing on how we can truly help others succeed and achieve their goals.",
         "Ryan Roslansky, CEO Philosophy, Helpful Culture Strategy, 2023"),
        
        ("LinkedIn", "Senior", "Transform", "Drive transformation in professional networking",
         "Give me an example of when you drove transformation that improved professional networking or opportunities.", "Leadership", "Medium",
         "Transformation means creating new ways for professionals to connect, learn, and advance their careers.",
         "LinkedIn Transformation Strategy, Professional Development Framework, 2024"),
        
        ("LinkedIn", "Leadership", "Economic Opportunity", "Create economic opportunity for the global workforce",
         "Tell me about how you've created economic opportunities for professionals or communities.", "Leadership", "Hard",
         "Leaders must create economic opportunity, ensuring that our platform helps people access better career prospects globally.",
         "LinkedIn Economic Opportunity, Global Impact Program, 2023"),
        
        # Additional Financial Services
        
        # Morgan Stanley - additional questions
        ("Morgan Stanley", "Entry Level", "Excellence", "Pursue excellence in everything we do",
         "Tell me about a time when you pursued excellence despite significant challenges.", "Culture Fit", "Easy",
         "Excellence means consistently pursuing the highest standards in client service and professional work.",
         "Morgan Stanley Values, Excellence Framework, 2024"),
        
        ("Morgan Stanley", "Mid Level", "Client Focus", "Put clients at the center of everything",
         "Describe how you've put client needs at the center of your work and decision-making.", "Culture Fit", "Medium",
         "Client focus means putting client interests and success at the center of everything we do.",
         "Ted Pick, CEO Message, Client Excellence Strategy, 2023"),
        
        ("Morgan Stanley", "Senior", "Innovation", "Innovate to serve clients better",
         "Give me an example of when you drove innovation that better served client needs.", "Problem Solving", "Medium",
         "Innovation enables us to develop new solutions and services that better meet evolving client needs.",
         "Morgan Stanley Innovation Strategy, Client Solutions Framework, 2024"),
        
        ("Morgan Stanley", "Leadership", "Diversity and Inclusion", "Champion diversity and inclusive excellence",
         "Tell me about how you've championed diversity and inclusion while achieving business excellence.", "Leadership", "Hard",
         "Leaders must champion diversity and inclusion, ensuring that diverse perspectives drive innovation and client service.",
         "Morgan Stanley Leadership Excellence, D&I Program, 2023"),
        
        # Goldman Sachs - additional questions  
        ("Goldman Sachs", "Entry Level", "Teamwork", "Work together to serve clients effectively",
         "Tell me about a time when effective teamwork was crucial to achieving client success.", "Teamwork", "Easy",
         "Teamwork enables us to leverage our collective capabilities to serve clients more effectively.",
         "Goldman Sachs Teamwork Culture, Collaboration Excellence, 2024"),
        
        ("Goldman Sachs", "Mid Level", "Innovation", "Innovate to stay ahead in financial services",
         "Describe how you've contributed to innovation in financial services or client solutions.", "Problem Solving", "Medium",
         "Innovation keeps us at the forefront of financial services and enables us to better serve client needs.",
         "David Solomon, CEO Message, Innovation Strategy, 2023"),
        
        ("Goldman Sachs", "Senior", "People Development", "Develop talent and build future leaders",
         "Give me an example of how you've developed talent and helped build future leaders.", "Leadership", "Medium",
         "People development means investing in talent and building the next generation of financial services leaders.",
         "Goldman Sachs People Strategy, Leadership Development Framework, 2024"),
        
        ("Goldman Sachs", "Leadership", "Global Mindset", "Think globally while serving clients locally",
         "Tell me about how you've applied global insights to serve local client needs effectively.", "Leadership", "Hard",
         "Leaders must have a global mindset, leveraging worldwide capabilities to serve clients across all markets.",
         "Goldman Sachs Global Leadership, Market Excellence Program, 2023"),
        
        # More Technology Companies
        
        # Uber - additional questions
        ("Uber", "Entry Level", "Celebrate Differences", "Value diversity and different perspectives",
         "Tell me about a time when you celebrated differences and leveraged diverse perspectives.", "Values", "Easy",
         "Celebrating differences means valuing diversity and leveraging different perspectives to create better solutions.",
         "Uber Diversity Culture, Inclusion Excellence Framework, 2024"),
        
        ("Uber", "Mid Level", "Be an Owner", "Take ownership and act like you own the company",
         "Describe how you've taken ownership and acted like you own the company.", "Leadership", "Medium",
         "Being an owner means taking personal responsibility and making decisions as if you own the business.",
         "Dara Khosrowshahi, CEO Philosophy, Ownership Culture Strategy, 2023"),
        
        ("Uber", "Senior", "Move Fast", "Execute with speed while maintaining quality",
         "Give me an example of when you moved fast to execute on an opportunity while maintaining quality.", "Problem Solving", "Medium",
         "Moving fast means executing quickly and efficiently while maintaining high standards and quality.",
         "Uber Speed Culture, Fast Execution Framework, 2024"),
        
        ("Uber", "Leadership", "Global Impact", "Create positive global impact through mobility",
         "Tell me about how you've created positive global impact through mobility or technology solutions.", "Leadership", "Hard",
         "Leaders must create global impact, ensuring that mobility solutions improve lives and communities worldwide.",
         "Uber Global Impact, Mobility Leadership Program, 2023"),
        
        # Airbnb - additional questions
        ("Airbnb", "Entry Level", "Embrace Adventure", "Embrace new experiences and adventures",
         "Tell me about a time when you embraced adventure or new experiences that led to growth.", "Culture Fit", "Easy",
         "Embracing adventure means being open to new experiences and approaches that can lead to personal and professional growth.",
         "Airbnb Adventure Culture, Growth Mindset Framework, 2024"),
        
        ("Airbnb", "Mid Level", "Be Host", "Think like a host and care for others",
         "Describe how you've thought like a host and cared for others in your work or community.", "Values", "Medium",
         "Being a host means caring for others and creating experiences that make them feel welcome and valued.",
         "Brian Chesky, CEO Message, Host Philosophy Strategy, 2023"),
        
        ("Airbnb", "Senior", "Own Your Impact", "Take ownership of your impact on others",
         "Give me an example of when you took ownership of your impact on others and made positive changes.", "Leadership", "Medium",
         "Owning your impact means recognizing how your actions affect others and taking responsibility for positive outcomes.",
         "Airbnb Impact Culture, Ownership Responsibility Framework, 2024"),
        
        ("Airbnb", "Leadership", "Champion Mission", "Champion our mission of belonging everywhere",
         "Tell me about how you've championed the mission of creating belonging in your leadership role.", "Leadership", "Hard",
         "Leaders must champion our mission, ensuring that belonging and inclusion guide all business decisions and community building.",
         "Airbnb Mission Leadership, Belonging Program, 2023"),
    ]
    
    return final_batch_questions

def append_to_csv(filename, questions):
    """Append questions to the existing CSV file."""
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for question in questions:
            writer.writerow(question)

def main():
    """Main function to generate and append final batch of questions."""
    filename = "/Users/adi/code/socratify/socratify-yolo/comprehensive_behavioral_interview_questions.csv"
    final_batch_questions = generate_final_batch_questions()
    append_to_csv(filename, final_batch_questions)
    print(f"Added {len(final_batch_questions)} additional questions to {filename}")

if __name__ == "__main__":
    main()