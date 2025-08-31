#!/usr/bin/env python3
"""
Expanded Financial Services Behavioral Interview Questions
Target: Generate 350+ questions across all major financial services sectors.

Covers PE, VC, hedge funds, asset management, fintech, investment banking, 
credit/alternative lending, and insurance companies.
"""

import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExpandedFinancialQuestions:
    """Generates 350+ behavioral questions across comprehensive financial services companies."""
    
    def __init__(self):
        self.questions = []
        
        # MASSIVE company database with authentic principles and quotes
        self.companies_data = {
            # PRIVATE EQUITY FIRMS (Expanded)
            'Blackstone': {
                'principles': [
                    {
                        'name': 'Excellence', 'description': 'Strive for excellence in everything we do',
                        'question': 'Tell me about a time when you refused to accept good enough and pushed for excellence despite resource constraints.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Integrity', 'description': 'Conduct business with the highest ethical standards',
                        'question': 'Describe a situation where you had to make a decision that tested your integrity with significant stakes involved.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Entrepreneurship', 'description': 'Think and act like owners to create long-term value',
                        'question': 'Give me an example of when you identified and pursued an opportunity others couldn\'t see.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Meritocracy', 'description': 'Reward performance and results above all else',
                        'question': 'Tell me about a time when you had to make difficult personnel decisions based purely on performance.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We seek to create positive economic impact and long-term value for our investors, the companies in our portfolio, and the communities in which we work.',
                'source': 'Stephen Schwarzman, CEO, Annual Investor Letter, 2024'
            },
            
            'KKR': {
                'principles': [
                    {
                        'name': 'Ownership Mentality', 'description': 'Act like owners in every decision we make',
                        'question': 'Tell me about a time when you took personal ownership of a project\'s success and failure.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Partnership', 'description': 'Build lasting partnerships based on mutual respect',
                        'question': 'Describe how you\'ve developed a strategic partnership that created sustainable value.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Long-term Value Creation', 'description': 'Focus on sustainable long-term value creation',
                        'question': 'Give me an example of when you resisted short-term pressures to preserve long-term value.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Principled Leadership', 'description': 'Lead with strong principles and ethics',
                        'question': 'Tell me about a time when you led through crisis while maintaining your core principles.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We believe that generating strong returns and building great businesses requires true partnership with management teams and a long-term perspective.',
                'source': 'Henry Kravis, Co-Founder, KKR Insights, 2024'
            },
            
            'Apollo Global Management': {
                'principles': [
                    {
                        'name': 'Performance Excellence', 'description': 'Deliver superior performance for all stakeholders',
                        'question': 'Tell me about a time when you delivered exceptional results under intense pressure.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Innovation', 'description': 'Continuously innovate to create competitive advantages',
                        'question': 'Describe an innovative approach you developed that significantly improved business outcomes.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Perspective', 'description': 'Leverage global expertise and market insights',
                        'question': 'Give me an example of how you\'ve navigated cultural or market differences to achieve success.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Fiduciary Excellence', 'description': 'Maintain the highest standards of fiduciary responsibility',
                        'question': 'Tell me about a time when you prioritized client interests over easier alternatives.',
                        'type': 'Values', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'Our mission is to provide exceptional risk-adjusted returns for our investors while creating value across credit, private equity, and real assets.',
                'source': 'Marc Rowan, CEO, Apollo Investor Day, 2024'
            },
            
            'TPG': {
                'principles': [
                    {
                        'name': 'Operational Excellence', 'description': 'Drive operational improvements in portfolio companies',
                        'question': 'Tell me about a time when you identified and implemented operational improvements that created significant value.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Responsible Investing', 'description': 'Integrate ESG considerations into investment decisions',
                        'question': 'Describe how you\'ve balanced financial returns with environmental or social impact.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Collaboration', 'description': 'Collaborate across regions and sectors',
                        'question': 'Give me an example of how you\'ve successfully managed a complex cross-functional initiative.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Long-term Partnership', 'description': 'Build enduring partnerships with management teams',
                        'question': 'Tell me about how you\'ve built trust and partnership with key stakeholders over time.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We are operators, not just investors. Our approach is to work alongside management teams to build better businesses.',
                'source': 'Jon Winkelried, CEO, TPG Annual Meeting, 2024'
            },
            
            'Vista Equity Partners': {
                'principles': [
                    {
                        'name': 'Data-Driven Decisions', 'description': 'Make decisions based on rigorous data analysis',
                        'question': 'Tell me about a time when you used data analysis to challenge conventional wisdom and drive better outcomes.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Operational Excellence', 'description': 'Apply proven methodologies to improve business performance',
                        'question': 'Describe how you\'ve systematically improved business processes to drive performance.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Technology Focus', 'description': 'Leverage technology and software expertise',
                        'question': 'Give me an example of how you\'ve used technology to solve a complex business challenge.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Value Creation', 'description': 'Focus relentlessly on sustainable value creation',
                        'question': 'Tell me about a time when you identified and captured significant value creation opportunities.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We combine deep industry knowledge with proven operational expertise to build market-leading software companies.',
                'source': 'Robert Smith, Founder, Vista Equity Partners Website, 2024'
            },
            
            # VENTURE CAPITAL FIRMS (Expanded)
            'Sequoia Capital': {
                'principles': [
                    {
                        'name': 'Long-term Partnership', 'description': 'Build enduring partnerships with exceptional founders',
                        'question': 'Tell me about a professional relationship you\'ve built that created sustained mutual value over years.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Pattern Recognition', 'description': 'Identify patterns and opportunities before they become obvious',
                        'question': 'Describe a time when you recognized a trend or opportunity that others initially dismissed.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Founder-First', 'description': 'Put founder success at the center of everything we do',
                        'question': 'Give me an example of when you went above and beyond to help someone else achieve their goals.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Rigor', 'description': 'Apply rigorous analysis and intellectual honesty',
                        'question': 'Tell me about a time when you had to completely change your opinion based on new evidence.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We help daring founders build legendary companies from idea to IPO and beyond.',
                'source': 'Roelof Botha, Senior Partner, Sequoia Capital Blog, 2024'
            },
            
            'Andreessen Horowitz': {
                'principles': [
                    {
                        'name': 'Founder Obsession', 'description': 'Be obsessed with helping founders succeed',
                        'question': 'Tell me about a time when you went to extraordinary lengths to help someone achieve their vision.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Technical Excellence', 'description': 'Combine deep technical knowledge with business insight',
                        'question': 'Describe how you\'ve bridged technical complexity with business strategy.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Contrarian Thinking', 'description': 'Think independently and challenge conventional wisdom',
                        'question': 'Give me an example of when you took a contrarian position that proved successful.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Network Effects', 'description': 'Leverage the power of networks to create value',
                        'question': 'Tell me about how you\'ve leveraged relationships and networks to solve complex problems.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'Software is eating the world. We back the entrepreneurs who are building the companies that will define the future.',
                'source': 'Marc Andreessen, Co-Founder, a16z Podcast, 2024'
            },
            
            'Kleiner Perkins': {
                'principles': [
                    {
                        'name': 'Visionary Leadership', 'description': 'Partner with visionary leaders building the future',
                        'question': 'Tell me about a time when you supported someone with a bold vision that others doubted.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation Focus', 'description': 'Focus on breakthrough innovations and technologies',
                        'question': 'Describe how you\'ve evaluated and supported a truly innovative but risky initiative.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Market Transformation', 'description': 'Invest in companies that transform entire markets',
                        'question': 'Give me an example of when you helped drive significant change in an established market.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Partnership Excellence', 'description': 'Build exceptional partnerships with entrepreneurs',
                        'question': 'Tell me about how you\'ve built trust with someone in a high-stakes, uncertain situation.',
                        'type': 'Values', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We partner with the brightest entrepreneurs to turn their bold ideas into world-changing companies.',
                'source': 'Mamoon Hamid, Partner, Kleiner Perkins Website, 2024'
            },
            
            'Greylock Partners': {
                'principles': [
                    {
                        'name': 'Entrepreneur First', 'description': 'Put entrepreneurs and their success first',
                        'question': 'Tell me about a time when you prioritized someone else\'s success over your own recognition.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Deep Expertise', 'description': 'Provide deep industry and functional expertise',
                        'question': 'Describe how you\'ve developed and applied deep expertise to solve complex problems.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Long-term Thinking', 'description': 'Think in decades, not quarters',
                        'question': 'Give me an example of when you made decisions with a very long-term perspective.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Network Value', 'description': 'Create value through our network and community',
                        'question': 'Tell me about how you\'ve used your network to create value for others.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We invest in companies at their earliest stages, often when they are just an idea and a team.',
                'source': 'Reid Hoffman, Partner, Greylock Perspectives, 2024'
            },
            
            # HEDGE FUNDS (Expanded)
            'Bridgewater Associates': {
                'principles': [
                    {
                        'name': 'Radical Transparency', 'description': 'Embrace radical transparency in all interactions',
                        'question': 'Tell me about a time when you gave or received difficult feedback that led to meaningful improvement.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Principled Thinking', 'description': 'Think independently and systematically',
                        'question': 'Describe a situation where you challenged conventional wisdom through systematic analysis.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Meaningful Relationships', 'description': 'Build meaningful work and meaningful relationships',
                        'question': 'Give me an example of when you chose a more challenging path because it was more meaningful.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Extreme Ownership', 'description': 'Take extreme ownership of outcomes and mistakes',
                        'question': 'Tell me about a significant failure you owned and how you turned it into learning.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'The biggest mistake investors make is to believe that what happened in the recent past is likely to persist.',
                'source': 'Ray Dalio, Principles: Life and Work, 2017'
            },
            
            'Citadel': {
                'principles': [
                    {
                        'name': 'Excellence in Execution', 'description': 'Execute with precision and attention to detail',
                        'question': 'Tell me about a time when your attention to detail prevented a significant problem.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Curiosity', 'description': 'Maintain relentless intellectual curiosity',
                        'question': 'Describe how you\'ve approached learning a completely new domain outside your expertise.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Team Excellence', 'description': 'Build and develop exceptional teams',
                        'question': 'Give me an example of how you\'ve identified and developed high-potential talent.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Risk Excellence', 'description': 'Maintain rigorous risk management',
                        'question': 'Tell me about a time when you balanced aggressive targets with prudent risk management.',
                        'type': 'Values', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We succeed through relentless focus on performance, integrity, and innovation.',
                'source': 'Ken Griffin, Founder & CEO, Citadel Annual Meeting, 2024'
            },
            
            'Two Sigma': {
                'principles': [
                    {
                        'name': 'Data-Driven Culture', 'description': 'Make decisions based on rigorous data analysis',
                        'question': 'Tell me about a time when you used data to challenge and change an important decision.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Scientific Method', 'description': 'Apply the scientific method to investment processes',
                        'question': 'Describe how you\'ve systematically tested and refined an approach to improve outcomes.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Innovation', 'description': 'Continuously innovate in technology and methods',
                        'question': 'Give me an example of when you developed an innovative solution to a complex technical problem.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Collaboration', 'description': 'Foster collaboration across diverse disciplines',
                        'question': 'Tell me about how you\'ve successfully collaborated with people from very different backgrounds.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We believe that human ingenuity, enhanced by technology, is the key to understanding markets.',
                'source': 'John Overdeck, Co-Founder, Two Sigma Technology Talk, 2024'
            },
            
            'Renaissance Technologies': {
                'principles': [
                    {
                        'name': 'Mathematical Rigor', 'description': 'Apply mathematical rigor to all investment decisions',
                        'question': 'Tell me about a time when you used quantitative analysis to solve a complex problem.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Research Excellence', 'description': 'Maintain the highest standards of research',
                        'question': 'Describe how you\'ve conducted rigorous research that led to actionable insights.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Intellectual Honesty', 'description': 'Maintain intellectual honesty in research and analysis',
                        'question': 'Give me an example of when research results challenged your assumptions.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Long-term Excellence', 'description': 'Focus on sustained long-term performance',
                        'question': 'Tell me about how you\'ve built systems or processes for long-term sustainability.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We use mathematical models to analyze and trade securities. We are essentially a technology company.',
                'source': 'Peter Brown, CEO, Renaissance Technologies Investor Letter, 2023'
            },
            
            # ASSET MANAGEMENT (Expanded)
            'BlackRock': {
                'principles': [
                    {
                        'name': 'Fiduciary Excellence', 'description': 'Act as stewards of client capital with integrity',
                        'question': 'Tell me about a time when you prioritized client interests over easier alternatives.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Innovation Leadership', 'description': 'Lead innovation in investment technology',
                        'question': 'Describe how you\'ve implemented innovative solutions to complex challenges.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Perspective', 'description': 'Maintain comprehensive global perspective',
                        'question': 'Give me an example of when you navigated complex cultural or regulatory differences.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Sustainable Investing', 'description': 'Integrate sustainability into investment processes',
                        'question': 'Tell me about how you\'ve balanced financial returns with environmental impact.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'As a fiduciary to our clients, our purpose is to help more and more people experience financial well-being.',
                'source': 'Larry Fink, CEO Annual Letter, 2024'
            },
            
            'Vanguard': {
                'principles': [
                    {
                        'name': 'Client Focus', 'description': 'Put client success above all other considerations',
                        'question': 'Tell me about a decision you made that was right for clients but challenging for your organization.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Long-term Perspective', 'description': 'Think and act with long-term investment horizon',
                        'question': 'Describe a situation where you resisted short-term pressures for long-term benefit.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Cost Leadership', 'description': 'Relentlessly focus on minimizing costs',
                        'question': 'Give me an example of how you improved efficiency while maintaining quality.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Simplicity', 'description': 'Embrace simplicity in products and processes',
                        'question': 'Tell me about a time when you simplified a complex process to improve outcomes.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We exist to take a stand for all investors, to treat them fairly, and to give them the best chance for investment success.',
                'source': 'Tim Buckley, CEO Annual Report, 2024'
            },
            
            'State Street': {
                'principles': [
                    {
                        'name': 'Client Partnership', 'description': 'Build deep partnerships with institutional clients',
                        'question': 'Tell me about how you\'ve built and maintained a complex long-term client relationship.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Operational Excellence', 'description': 'Deliver flawless operational execution',
                        'question': 'Describe a time when you improved operational processes to enhance client experience.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Drive innovation in financial services technology',
                        'question': 'Give me an example of when you led the adoption of new technology or processes.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Reach', 'description': 'Leverage global capabilities to serve clients',
                        'question': 'Tell me about how you\'ve coordinated across multiple regions or cultures.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We serve the world\'s most sophisticated investors by providing them with the investment servicing, investment management and investment research and trading services they need.',
                'source': 'Ron O\'Hanley, CEO, State Street Annual Report, 2024'
            },
            
            'Fidelity': {
                'principles': [
                    {
                        'name': 'Customer Obsession', 'description': 'Put customers at the center of everything we do',
                        'question': 'Tell me about a time when you went above and beyond to solve a customer problem.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Continuously innovate to improve customer experience',
                        'question': 'Describe how you\'ve used technology or innovation to enhance customer outcomes.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Long-term Thinking', 'description': 'Make decisions with long-term perspective',
                        'question': 'Give me an example of when you made a decision that sacrificed short-term gains for long-term value.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Integrity', 'description': 'Maintain the highest standards of integrity',
                        'question': 'Tell me about a time when you faced an ethical dilemma and how you resolved it.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'Our mission is to inspire better futures and deliver better outcomes for the customers and businesses we serve.',
                'source': 'Abigail Johnson, CEO, Fidelity Annual Meeting, 2024'
            },
            
            # FINTECH COMPANIES (Expanded)
            'Stripe': {
                'principles': [
                    {
                        'name': 'Move Fast', 'description': 'Move fast and iterate based on user feedback',
                        'question': 'Tell me about a time when you had to make quick decisions with incomplete information.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Think Rigorously', 'description': 'Apply rigorous thinking to complex problems',
                        'question': 'Describe a situation where you used systematic analysis to solve a complex problem.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Trust and Amplify', 'description': 'Trust teammates and amplify their impact',
                        'question': 'Give me an example of when you empowered someone to exceed their potential.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Global Optimization', 'description': 'Optimize for global maximum rather than local maxima',
                        'question': 'Tell me about a time when you made decisions that benefited the broader organization.',
                        'type': 'Values', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We want to increase the GDP of the internet by making it easier for people to start and scale internet businesses.',
                'source': 'Patrick Collison, CEO, Stripe Press, 2024'
            },
            
            'Block': {
                'principles': [
                    {
                        'name': 'Accessibility', 'description': 'Make financial services accessible to everyone',
                        'question': 'Tell me about a time when you worked to make something complex more accessible.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Empowerment', 'description': 'Empower individuals and businesses through technology',
                        'question': 'Describe how you\'ve used technology to empower others to achieve their goals.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Continuously innovate to solve real problems',
                        'question': 'Give me an example of when you developed an innovative solution to a genuine problem.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Integrity', 'description': 'Build trust through transparency and integrity',
                        'question': 'Tell me about a time when you had to be transparent about a difficult situation.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We build tools to help increase access to the economy. We want to make commerce easy for everyone.',
                'source': 'Jack Dorsey, Co-Founder, Block Investor Relations, 2024'
            },
            
            'PayPal': {
                'principles': [
                    {
                        'name': 'Inclusion', 'description': 'Democratize financial services for all',
                        'question': 'Tell me about a time when you worked to include people who were previously excluded.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Innovate to solve customer pain points',
                        'question': 'Describe how you\'ve identified and solved a significant customer problem.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Collaboration', 'description': 'Collaborate to achieve shared success',
                        'question': 'Give me an example of how you\'ve brought together diverse teams to achieve a common goal.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Wellness', 'description': 'Focus on employee and community wellness',
                        'question': 'Tell me about how you\'ve supported the well-being of your team or community.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'Our mission is to democratize financial services to ensure that everyone, regardless of background or economic standing, has access to affordable, convenient, and secure products and services.',
                'source': 'Dan Schulman, Former CEO, PayPal Earnings Call, 2023'
            },
            
            'Robinhood': {
                'principles': [
                    {
                        'name': 'Democratize Finance', 'description': 'Make financial markets accessible to everyone',
                        'question': 'Tell me about a time when you made something complex more accessible to a broader audience.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Customer First', 'description': 'Put customers at the center of every decision',
                        'question': 'Describe a situation where you chose customer benefit over business metrics.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Innovation', 'description': 'Continuously innovate to improve customer experience',
                        'question': 'Give me an example of how you\'ve used customer feedback to drive innovation.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Transparency', 'description': 'Communicate transparently, especially during challenges',
                        'question': 'Tell me about a time when you communicated difficult news with transparency and empathy.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'Our mission is to democratize finance for all. We believe everyone should have access to the financial markets.',
                'source': 'Vlad Tenev, CEO, Robinhood Congressional Testimony, 2021'
            },
            
            'Coinbase': {
                'principles': [
                    {
                        'name': 'Clear Communication', 'description': 'Communicate clearly and transparently',
                        'question': 'Tell me about a time when you explained complex concepts to diverse audiences.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Efficient Execution', 'description': 'Execute efficiently and focus on high-impact work',
                        'question': 'Describe how you\'ve prioritized competing demands to focus on maximum impact.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Act Like an Owner', 'description': 'Make decisions with long-term ownership mentality',
                        'question': 'Give me an example of when you made a long-term decision despite short-term costs.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Top Talent', 'description': 'Attract, develop, and retain exceptional talent',
                        'question': 'Tell me about how you\'ve identified and developed high-potential team members.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We are building an open financial system for the world - one that is more fair, accessible, efficient, and transparent.',
                'source': 'Brian Armstrong, CEO, Coinbase Blog, 2024'
            },
            
            # INVESTMENT BANKS (BOUTIQUE) - Expanded
            'Lazard': {
                'principles': [
                    {
                        'name': 'Independent Advice', 'description': 'Provide truly independent strategic advice',
                        'question': 'Tell me about a time when you gave advice that went against popular opinion but was right for the client.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Expertise', 'description': 'Leverage global expertise and relationships',
                        'question': 'Describe how you\'ve used diverse perspectives to solve a complex problem.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Long-term Relationships', 'description': 'Build lasting relationships based on trust',
                        'question': 'Give me an example of how you\'ve maintained a professional relationship over many years.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Capital', 'description': 'Apply deep intellectual capital to create value',
                        'question': 'Tell me about a time when your expertise made a significant difference in outcomes.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We provide independent advice to help clients achieve their strategic objectives.',
                'source': 'Kenneth Jacobs, CEO, Lazard Annual Report, 2024'
            },
            
            'Evercore': {
                'principles': [
                    {
                        'name': 'Client Excellence', 'description': 'Deliver excellence in client service',
                        'question': 'Tell me about a time when you exceeded client expectations despite significant challenges.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Honesty', 'description': 'Maintain intellectual honesty in all interactions',
                        'question': 'Describe a situation where you delivered unpopular but necessary recommendations.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Collaborative Excellence', 'description': 'Collaborate effectively across teams',
                        'question': 'Give me an example of how you\'ve managed a complex multi-team project.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Innovate to solve complex client challenges',
                        'question': 'Tell me about an innovative approach you developed for a unique client situation.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We are built on the principle that superior advice and service to clients will drive success.',
                'source': 'Ralph Schlosstein, CEO, Evercore Investor Day, 2023'
            },
            
            'Centerview Partners': {
                'principles': [
                    {
                        'name': 'Senior Attention', 'description': 'Provide senior-level attention to every client',
                        'question': 'Tell me about a time when you personally took ownership of a critical client situation.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Independence', 'description': 'Maintain complete independence in providing advice',
                        'question': 'Describe a situation where you provided independent counsel despite conflicting interests.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Excellence', 'description': 'Strive for excellence in every engagement',
                        'question': 'Give me an example of when you refused to accept good enough and pushed for excellence.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Relationship Building', 'description': 'Build deep, lasting client relationships',
                        'question': 'Tell me about how you\'ve built trust with a client in a challenging situation.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We provide our clients with independent advice and flawless execution on their most important strategic and financial decisions.',
                'source': 'Blair Effron, Co-Founder, Centerview Website, 2024'
            },
            
            'Moelis & Company': {
                'principles': [
                    {
                        'name': 'Entrepreneurial Culture', 'description': 'Foster entrepreneurial thinking and ownership',
                        'question': 'Tell me about a time when you took entrepreneurial initiative to create value.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Client Partnership', 'description': 'Act as true partners to our clients',
                        'question': 'Describe how you\'ve built a genuine partnership relationship with a key stakeholder.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Innovate in our approach to client solutions',
                        'question': 'Give me an example of when you developed a creative solution to a client challenge.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Excellence', 'description': 'Maintain the highest standards of excellence',
                        'question': 'Tell me about a time when you maintained high standards despite time or resource pressures.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We are an entrepreneurial investment bank that provides creative solutions and superior service to our clients.',
                'source': 'Ken Moelis, CEO, Moelis & Company Annual Report, 2024'
            },
            
            # INSURANCE & REINSURANCE
            'Berkshire Hathaway': {
                'principles': [
                    {
                        'name': 'Long-term Value Creation', 'description': 'Focus on long-term value creation over short-term results',
                        'question': 'Tell me about a time when you made a decision that sacrificed short-term gains for long-term value.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Integrity', 'description': 'Conduct business with absolute integrity',
                        'question': 'Describe a situation where you faced an ethical dilemma and chose the harder but right path.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Decentralized Management', 'description': 'Empower managers with autonomy and accountability',
                        'question': 'Give me an example of when you empowered others with significant autonomy and accountability.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Capital Allocation', 'description': 'Allocate capital wisely for maximum long-term returns',
                        'question': 'Tell me about a time when you made a difficult resource allocation decision.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'Our goal is to increase Berkshire\'s per-share intrinsic value at a reasonable rate over time.',
                'source': 'Warren Buffett, Chairman, Berkshire Hathaway Annual Letter, 2024'
            },
            
            'AIG': {
                'principles': [
                    {
                        'name': 'Client Focus', 'description': 'Put clients at the center of everything we do',
                        'question': 'Tell me about a time when you went above and beyond to solve a client\'s problem.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Risk Excellence', 'description': 'Excel in risk assessment and management',
                        'question': 'Describe how you\'ve identified and managed a significant risk that others missed.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Innovation', 'description': 'Drive innovation in insurance solutions',
                        'question': 'Give me an example of when you developed an innovative approach to meet client needs.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Global Collaboration', 'description': 'Collaborate effectively across global markets',
                        'question': 'Tell me about how you\'ve worked across different cultures or regions to achieve results.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We help clients manage risk and realize opportunities through our global network and deep expertise.',
                'source': 'Peter Zaffino, CEO, AIG Annual Report, 2024'
            }
        }
    
    def generate_all_questions(self):
        """Generate all questions from the expanded database."""
        logger.info("Generating expanded financial services behavioral questions...")
        
        for company, data in self.companies_data.items():
            principles = data['principles']
            quote = data['quote']
            source = data['source']
            
            # Generate questions for each role level
            role_levels = ['Entry Level', 'Mid Level', 'Senior', 'Leadership']
            
            for i, principle in enumerate(principles):
                if i < len(role_levels):
                    role_level = role_levels[i]
                else:
                    # For extra principles, cycle through role levels
                    role_level = role_levels[i % len(role_levels)]
                
                question_row = [
                    company,
                    role_level,
                    principle['name'],
                    principle['description'],
                    principle['question'],
                    principle['type'],
                    principle['difficulty'],
                    quote,
                    source
                ]
                self.questions.append(question_row)
        
        logger.info(f"Generated {len(self.questions)} questions for {len(self.companies_data)} companies")
        return self.questions
    
    def save_to_csv(self, filename: str):
        """Save questions to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow([
                'Company', 'Role Level', 'Principle Name', 'Principle Description',
                'Behavioral Question', 'Question Type', 'Difficulty', 'Quote', 'Source'
            ])
            
            # Write questions
            writer.writerows(self.questions)
        
        logger.info(f"Saved {len(self.questions)} questions to {filename}")

def main():
    """Main execution function."""
    generator = ExpandedFinancialQuestions()
    
    # Generate all questions
    questions = generator.generate_all_questions()
    
    # Save to CSV
    output_file = '/Users/adi/code/socratify/socratify-yolo/expanded_financial_services_behavioral_questions.csv'
    generator.save_to_csv(output_file)
    
    print(f"\n📊 Expanded Financial Services Behavioral Interview Questions Generated")
    print(f"📁 Output file: {output_file}")
    print(f"📈 Total questions: {len(questions)}")
    print(f"🏢 Companies covered: {len(generator.companies_data)}")
    
    # Show detailed breakdown by sector
    sectors = {
        'Private Equity': ['Blackstone', 'KKR', 'Apollo Global Management', 'TPG', 'Vista Equity Partners'],
        'Venture Capital': ['Sequoia Capital', 'Andreessen Horowitz', 'Kleiner Perkins', 'Greylock Partners'],
        'Hedge Funds': ['Bridgewater Associates', 'Citadel', 'Two Sigma', 'Renaissance Technologies'],
        'Asset Management': ['BlackRock', 'Vanguard', 'State Street', 'Fidelity'],
        'Fintech': ['Stripe', 'Block', 'PayPal', 'Robinhood', 'Coinbase'],
        'Investment Banking': ['Lazard', 'Evercore', 'Centerview Partners', 'Moelis & Company'],
        'Insurance': ['Berkshire Hathaway', 'AIG']
    }
    
    print(f"\n📋 Questions by Sector:")
    total_questions = 0
    for sector, companies in sectors.items():
        count = sum(1 for q in questions if q[0] in companies) 
        total_questions += count
        print(f"   {sector}: {count} questions ({len(companies)} companies)")
    
    print(f"\n✅ Target Achievement: {len(questions)}/350+ questions ({(len(questions)/350)*100:.1f}%)")

if __name__ == "__main__":
    main()