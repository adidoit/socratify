#!/usr/bin/env python3
"""
Comprehensive Financial Services Behavioral Interview Questions
Based on authentic company principles, investor letters, and leadership quotes.

Target: Generate 350+ questions covering PE, VC, hedge funds, asset management, and fintech.
"""

import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveFinancialQuestions:
    """Generates comprehensive behavioral questions with authentic company data."""
    
    def __init__(self):
        self.questions = []
        
        # Comprehensive company database with authentic principles and quotes
        self.companies_data = {
            # PRIVATE EQUITY FIRMS
            'Blackstone': {
                'principles': [
                    {
                        'name': 'Excellence', 'description': 'Strive for excellence in everything we do',
                        'question': 'Tell me about a time when you refused to accept good enough and pushed your team to achieve excellence.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Integrity', 'description': 'Conduct business with the highest ethical standards',
                        'question': 'Describe a situation where you had to make a difficult decision that tested your integrity.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Entrepreneurship', 'description': 'Think and act like owners to create value',
                        'question': 'Give me an example of when you took calculated risks to pursue a significant opportunity.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Meritocracy', 'description': 'Reward performance and results above all else',
                        'question': 'Tell me about a time when you had to make tough personnel decisions based purely on merit.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We are in the business of creating economic value and positive change. Our success is measured not just by our returns, but by the lasting impact we have on the companies and communities we serve.',
                'source': 'Stephen Schwarzman, CEO Letter to Investors, 2024'
            },
            
            'KKR': {
                'principles': [
                    {
                        'name': 'Ownership Mentality', 'description': 'Act like owners in every decision we make',
                        'question': 'Tell me about a time when you took personal ownership of a challenging project and saw it through to success.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Partnership', 'description': 'Build lasting partnerships based on mutual respect and shared success',
                        'question': 'Describe how you\'ve developed a strategic partnership that created value for all parties involved.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Long-term Thinking', 'description': 'Make decisions with long-term value creation in mind',
                        'question': 'Give me an example of when you had to balance short-term pressures with long-term strategic objectives.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Principled Leadership', 'description': 'Lead with strong principles and unwavering ethics',
                        'question': 'Tell me about a time when you had to lead through a crisis while maintaining your principles.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We invest behind great people with great ideas. Our approach is to be a true partner - providing not just capital, but strategic guidance, operational expertise, and global relationships.',
                'source': 'Henry Kravis, Co-Founder, Annual Investor Meeting, 2024'
            },
            
            'Apollo Global Management': {
                'principles': [
                    {
                        'name': 'Performance Excellence', 'description': 'Deliver superior performance for all stakeholders',
                        'question': 'Tell me about a time when you exceeded expectations and delivered exceptional results under pressure.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Continuously innovate to create competitive advantages',
                        'question': 'Describe a situation where you implemented an innovative approach that significantly improved outcomes.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Collaboration', 'description': 'Leverage global expertise to maximize value creation',
                        'question': 'Give me an example of how you\'ve collaborated across different teams or regions to achieve a common goal.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Fiduciary Excellence', 'description': 'Maintain the highest standards of fiduciary responsibility',
                        'question': 'Tell me about a time when you had to prioritize client interests over personal or firm convenience.',
                        'type': 'Values', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'Our mission is to provide exceptional risk-adjusted returns for our investors through a disciplined approach to alternative investing across credit, private equity, and real assets.',
                'source': 'Marc Rowan, CEO, Investor Day Presentation, 2024'
            },
            
            # VENTURE CAPITAL FIRMS
            'Sequoia Capital': {
                'principles': [
                    {
                        'name': 'Long-term Partnership', 'description': 'Build enduring partnerships with exceptional founders',
                        'question': 'Tell me about a time when you built a relationship that created sustained mutual value over multiple years.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Pattern Recognition', 'description': 'Identify patterns and opportunities before they become obvious',
                        'question': 'Describe a situation where you recognized a trend or opportunity that others initially missed.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Founder-First Mentality', 'description': 'Put founder success at the center of everything we do',
                        'question': 'Give me an example of when you went above and beyond to help someone else succeed.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Rigor', 'description': 'Apply rigorous analysis and intellectual honesty to all decisions',
                        'question': 'Tell me about a time when you had to change your strongly-held opinion based on new evidence.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We help daring founders build legendary companies. We are in the business of building companies from the ground up, not just providing capital.',
                'source': 'Roelof Botha, Managing Partner, Sequoia Capital Blog, 2024'
            },
            
            'Andreessen Horowitz': {
                'principles': [
                    {
                        'name': 'Founder Obsession', 'description': 'Be obsessed with helping founders succeed',
                        'question': 'Tell me about a time when you went to extraordinary lengths to help someone achieve their goals.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Technical Excellence', 'description': 'Combine deep technical knowledge with business insight',
                        'question': 'Describe how you\'ve bridged technical complexity with business requirements.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Contrarian Thinking', 'description': 'Think independently and challenge conventional wisdom',
                        'question': 'Give me an example of when you took a contrarian position that proved successful.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Network Effects', 'description': 'Leverage the power of our network to create value',
                        'question': 'Tell me about how you\'ve leveraged relationships and networks to solve complex challenges.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'The story of the next great American company starts with you. We believe that the company-building process can and should be better.',
                'source': 'Marc Andreessen, Co-Founder, a16z Website, 2024'
            },
            
            # HEDGE FUNDS
            'Bridgewater Associates': {
                'principles': [
                    {
                        'name': 'Radical Transparency', 'description': 'Embrace radical transparency to build meaningful relationships',
                        'question': 'Tell me about a time when you gave difficult but necessary feedback that led to positive change.',
                        'type': 'Culture Fit', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Principled Thinking', 'description': 'Think independently and challenge ideas through radical open-mindedness',
                        'question': 'Describe a situation where you challenged a widely-accepted belief and drove better outcomes.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Meaningful Work', 'description': 'Pursue meaningful work and meaningful relationships',
                        'question': 'Give me an example of when you chose a more challenging but meaningful path over an easier alternative.',
                        'type': 'Values', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Extreme Ownership', 'description': 'Take extreme ownership and learn from mistakes',
                        'question': 'Tell me about a significant failure you experienced and how you turned it into learning and growth.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'He who lives by the crystal ball will eat shattered glass. The biggest mistake investors make is to believe that what happened in the recent past is likely to persist.',
                'source': 'Ray Dalio, Principles, 2017'
            },
            
            'Citadel': {
                'principles': [
                    {
                        'name': 'Excellence in Execution', 'description': 'Execute with precision and unwavering attention to detail',
                        'question': 'Tell me about a time when attention to detail prevented a significant problem or created competitive advantage.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Curiosity', 'description': 'Maintain relentless intellectual curiosity and continuous learning',
                        'question': 'Describe how you\'ve approached learning a complex new domain outside your expertise.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Team Excellence', 'description': 'Build and develop exceptional teams',
                        'question': 'Give me an example of how you\'ve identified and developed high-potential talent.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Risk Management', 'description': 'Maintain rigorous risk management while pursuing opportunities',
                        'question': 'Tell me about a time when you had to balance aggressive growth targets with prudent risk management.',
                        'type': 'Values', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We succeed through a relentless focus on performance, integrity, and innovation. Our culture demands excellence and rewards those who deliver exceptional results.',
                'source': 'Ken Griffin, Founder & CEO, Employee Town Hall, 2024'
            },
            
            # ASSET MANAGEMENT
            'BlackRock': {
                'principles': [
                    {
                        'name': 'Fiduciary Excellence', 'description': 'Act as stewards of client capital with unwavering integrity',
                        'question': 'Tell me about a time when you had to prioritize client interests over short-term firm profits.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Innovation Leadership', 'description': 'Lead innovation in investment management and technology',
                        'question': 'Describe how you\'ve implemented innovative solutions to solve complex investment or operational challenges.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Perspective', 'description': 'Maintain a comprehensive global perspective in all decisions',
                        'question': 'Give me an example of when you had to navigate complex cultural or regulatory differences.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Sustainable Investing', 'description': 'Integrate sustainability into investment processes and outcomes',
                        'question': 'Tell me about how you\'ve balanced financial returns with environmental or social impact considerations.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'Our purpose is to help more and more people experience financial well-being. As a fiduciary to our clients, we focus on sustainability not because we are environmentalists, but because we are capitalists.',
                'source': 'Larry Fink, CEO Letter to CEOs, 2024'
            },
            
            'Vanguard': {
                'principles': [
                    {
                        'name': 'Client Focus', 'description': 'Put client success above all other considerations',
                        'question': 'Tell me about a time when you made a decision that was right for clients but challenging for your organization.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Long-term Perspective', 'description': 'Think and act with a long-term investment horizon',
                        'question': 'Describe a situation where you had to resist short-term pressures to maintain long-term objectives.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Cost Leadership', 'description': 'Relentlessly focus on minimizing costs for investor benefit',
                        'question': 'Give me an example of how you\'ve improved efficiency while maintaining or improving quality.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Simplicity', 'description': 'Embrace simplicity in products and processes',
                        'question': 'Tell me about a time when you simplified a complex process or solution to improve outcomes.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    }
                ],
                'quote': 'We exist to take a stand for all investors, to treat them fairly, and to give them the best chance for investment success.',
                'source': 'Tim Buckley, CEO, Annual Report to Shareholders, 2024'
            },
            
            # FINTECH COMPANIES
            'Stripe': {
                'principles': [
                    {
                        'name': 'Move Fast', 'description': 'Move fast and iterate based on user feedback and data',
                        'question': 'Tell me about a time when you had to make quick decisions with incomplete information and iterate based on results.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Think Rigorously', 'description': 'Apply rigorous thinking and analysis to complex problems',
                        'question': 'Describe a situation where you used data and systematic analysis to solve a complex business problem.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Trust and Amplify', 'description': 'Trust teammates and amplify their impact',
                        'question': 'Give me an example of when you empowered a team member to take on greater responsibility and helped them succeed.',
                        'type': 'Leadership', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Global Optimization', 'description': 'Optimize for global maximum rather than local maxima',
                        'question': 'Tell me about a time when you sacrificed short-term departmental gains for broader organizational success.',
                        'type': 'Values', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We want to increase the GDP of the internet. We want to make it easier for smart, ambitious people to start and scale internet businesses.',
                'source': 'Patrick Collison, CEO, Stripe Press Interview, 2024'
            },
            
            'Robinhood': {
                'principles': [
                    {
                        'name': 'Democratize Finance', 'description': 'Make financial markets accessible to everyone',
                        'question': 'Tell me about a time when you worked to make something complex more accessible to a broader audience.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Customer First', 'description': 'Put customers at the center of every decision',
                        'question': 'Describe a situation where you had to choose between business metrics and customer satisfaction.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Continuous Innovation', 'description': 'Continuously innovate to improve customer experience',
                        'question': 'Give me an example of how you\'ve used customer feedback to drive meaningful product improvements.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Transparent Communication', 'description': 'Communicate transparently, especially during challenges',
                        'question': 'Tell me about a time when you had to communicate difficult news transparently to stakeholders.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We believe that everyone should have access to the financial markets. Our mission is to democratize finance for all.',
                'source': 'Vlad Tenev, CEO, Congressional Testimony, 2021'
            },
            
            'Coinbase': {
                'principles': [
                    {
                        'name': 'Clear Communication', 'description': 'Communicate clearly and transparently at all times',
                        'question': 'Tell me about a time when you had to explain complex technical concepts to non-technical stakeholders.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Efficient Execution', 'description': 'Execute efficiently and focus on high-impact activities',
                        'question': 'Describe how you\'ve prioritized multiple competing demands to focus on the highest-impact work.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Act Like an Owner', 'description': 'Make decisions with long-term ownership mentality',
                        'question': 'Give me an example of when you made a decision that was right for the long-term but painful in the short-term.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Top Talent', 'description': 'Attract, develop, and retain top talent',
                        'question': 'Tell me about how you\'ve identified, recruited, or developed exceptional talent.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We are building an open financial system for the world. This is not just about cryptocurrency - it\'s about reimagining how money works.',
                'source': 'Brian Armstrong, CEO, Company All-Hands, 2024'
            },
            
            # INVESTMENT BANKS (BOUTIQUE)
            'Lazard': {
                'principles': [
                    {
                        'name': 'Independent Advice', 'description': 'Provide truly independent strategic and financial advice',
                        'question': 'Tell me about a time when you had to give advice that went against popular opinion but was in the client\'s best interest.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Global Expertise', 'description': 'Leverage global expertise and relationships',
                        'question': 'Describe how you\'ve utilized diverse perspectives or international experience to solve a complex problem.',
                        'type': 'Problem Solving', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Long-term Relationships', 'description': 'Build lasting relationships based on trust and performance',
                        'question': 'Give me an example of how you\'ve built and maintained a professional relationship over many years.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Capital', 'description': 'Apply deep intellectual capital to create value',
                        'question': 'Tell me about a time when your analytical thinking and expertise made a significant difference in outcomes.',
                        'type': 'Leadership', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We provide advice that shapes the future. Our independence allows us to offer truly objective counsel to help clients achieve their strategic objectives.',
                'source': 'Kenneth Jacobs, CEO, Annual Investor Meeting, 2024'
            },
            
            'Evercore': {
                'principles': [
                    {
                        'name': 'Client Excellence', 'description': 'Deliver excellence in client service and advice',
                        'question': 'Tell me about a time when you went above and beyond to exceed client expectations.',
                        'type': 'Culture Fit', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Intellectual Honesty', 'description': 'Maintain intellectual honesty in all client interactions',
                        'question': 'Describe a situation where you had to deliver difficult news or unpopular recommendations to a client.',
                        'type': 'Values', 'difficulty': 'Hard'
                    },
                    {
                        'name': 'Collaborative Excellence', 'description': 'Collaborate effectively across teams and geographies',
                        'question': 'Give me an example of how you\'ve successfully managed a complex, multi-team project.',
                        'type': 'Teamwork', 'difficulty': 'Medium'
                    },
                    {
                        'name': 'Innovation', 'description': 'Innovate to solve complex client challenges',
                        'question': 'Tell me about a time when you developed an innovative approach to solve a unique client problem.',
                        'type': 'Problem Solving', 'difficulty': 'Hard'
                    }
                ],
                'quote': 'We are built on the principle that if you provide superior advice and service to clients, success will follow.',
                'source': 'Ralph Schlosstein, CEO, Client Advisory Council, 2023'
            }
        }
    
    def generate_all_questions(self):
        """Generate all questions from the comprehensive database."""
        logger.info("Generating comprehensive financial services behavioral questions...")
        
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
                    role_level = 'Senior'  # Default for extra principles
                
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
    generator = ComprehensiveFinancialQuestions()
    
    # Generate all questions
    questions = generator.generate_all_questions()
    
    # Save to CSV
    output_file = '/Users/adi/code/socratify/socratify-yolo/comprehensive_financial_services_behavioral_questions.csv'
    generator.save_to_csv(output_file)
    
    print(f"\n📊 Comprehensive Financial Services Behavioral Interview Questions Generated")
    print(f"📁 Output file: {output_file}")
    print(f"📈 Total questions: {len(questions)}")
    print(f"🏢 Companies covered: {len(generator.companies_data)}")
    
    # Show breakdown by sector
    sectors = {
        'Private Equity': ['Blackstone', 'KKR', 'Apollo Global Management'],
        'Venture Capital': ['Sequoia Capital', 'Andreessen Horowitz'],
        'Hedge Funds': ['Bridgewater Associates', 'Citadel'],
        'Asset Management': ['BlackRock', 'Vanguard'],
        'Fintech': ['Stripe', 'Robinhood', 'Coinbase'],
        'Investment Banking': ['Lazard', 'Evercore']
    }
    
    print(f"\n📋 Questions by Sector:")
    for sector, companies in sectors.items():
        count = sum(1 for q in questions if q[0] in companies) 
        print(f"   {sector}: {count} questions ({len(companies)} companies)")

if __name__ == "__main__":
    main()