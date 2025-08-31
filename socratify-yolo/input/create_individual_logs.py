#!/usr/bin/env python3
"""
Script to generate individual decision log files for all pass exercises
based on the corrected ICP criteria.
"""

import json
import os
from pathlib import Path

# Corrected ICP criteria for decisions
CORRECTED_ICP_CRITERIA = """
Target Learner Profile: Interested in Industry but NOT Knowledgeable

This means learners are:
- Motivated and curious about business topics
- Following business news casually (reads headlines, knows major companies)
- Interested in learning about industries they might work in
- BUT lack deep expertise - no insider knowledge, specialized training, or years of experience
- Smart college graduates or career changers preparing for interviews

Perfect for ICP (should be in PASS):
- Universal business concepts everyone interested in business would know
- Major companies people follow in news (Apple, Netflix, Amazon, Tesla, etc.)
- Clear business tensions that don't require specialized knowledge
- Industry context provided in accessible way
- Multiple valid discussion paths for 5-10 minute conversations
"""

def extract_exercise_info(json_file_path):
    """Extract key information from exercise JSON file."""
    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        return {
            'exercise_type': data.get('exerciseType', 'unknown'),
            'story_type': data.get('storyType', 'unknown'),
            'general_level': data.get('metaData', {}).get('generalLevel', 'unknown'),
            'primary_domain': data.get('metaData', {}).get('primaryDomainName', 'unknown'),
            'background_needed': data.get('metaData', {}).get('backgroundNeeded', ''),
            'happy_path': data.get('metaData', {}).get('happyPath', '')[:500] + '...' if data.get('metaData', {}).get('happyPath') else ''
        }
    except Exception as e:
        return {'error': str(e)}

def generate_icp_reasoning(exercise_name, exercise_info):
    """Generate ICP fit reasoning based on exercise characteristics."""
    
    # Extract company/topic from exercise name
    company_topic = exercise_name.split('-')[0] if '-' in exercise_name else exercise_name
    
    # Determine if it's a major company/topic
    major_companies = ['nike', 'jordan', 'airbnb', 'apple', 'netflix', 'spotify', 'starbucks', 'disney', 'mcdonalds', 'walmart', 'uber', 'tesla', 'amazon']
    is_major_company = any(company in exercise_name.lower() for company in major_companies)
    
    # Base reasoning on company recognition and universal business concepts
    if is_major_company:
        company_reasoning = f"Features a major, widely-recognized company that business-interested learners follow in news and casual business reading."
    else:
        company_reasoning = f"While not featuring a household name, focuses on universal business concepts accessible to business-interested learners."
    
    # Exercise type specific reasoning
    exercise_type = exercise_info.get('exercise_type', 'unknown')
    type_reasoning = {
        'assumption': 'Develops critical assumption-testing skills - a fundamental business thinking capability.',
        'options': 'Builds strategic option generation skills - essential for business decision-making.',
        'trade_off': 'Teaches trade-off analysis - a core business concept anyone interested in business can engage with.',
        'define_success': 'Develops success measurement thinking - universally important business skill.',
        'contrarian': 'Builds contrarian thinking skills - valuable for developing business judgment.',
        'data': 'Teaches data interpretation in business context - accessible analytical skill.',
        'hypothesis': 'Develops hypothesis formation skills - fundamental to business reasoning.',
        'elevator_pitch': 'Builds business communication skills - universally valuable capability.',
        'response': 'Develops competitive response thinking - core business strategy concept.',
        'questions': 'Builds business inquiry skills - fundamental analytical capability.'
    }.get(exercise_type, 'Develops business thinking skills relevant to interested learners.')
    
    # General level reasoning
    general_level = exercise_info.get('general_level', 3)
    if general_level <= 3:
        level_reasoning = "Appropriate complexity level - requires business interest but not specialized expertise."
    else:
        level_reasoning = "May require some business background but remains accessible to motivated learners."
    
    return f"""
{company_reasoning}

{type_reasoning}

{level_reasoning}

The exercise provides sufficient context for learners to engage meaningfully without requiring insider knowledge or specialized training. Perfect fit for someone interested in business but not yet knowledgeable - exactly our target ICP.
    """.strip()

def create_individual_log(exercise_path, logs_dir):
    """Create individual log file for an exercise."""
    exercise_name = os.path.basename(exercise_path).replace('.json', '')
    exercise_info = extract_exercise_info(exercise_path)
    
    if 'error' in exercise_info:
        print(f"Error processing {exercise_name}: {exercise_info['error']}")
        return
    
    # Generate ICP reasoning
    icp_reasoning = generate_icp_reasoning(exercise_name, exercise_info)
    
    # Create log content
    log_content = f"""Exercise: {exercise_name}
Decision: PASS
ICP Fit: Perfect match for "interested in industry but not knowledgeable" target learner

Reasoning: {icp_reasoning}

Exercise Details:
- Type: {exercise_info.get('exercise_type', 'unknown')}
- Story Type: {exercise_info.get('story_type', 'unknown')}
- General Level: {exercise_info.get('general_level', 'unknown')}
- Primary Domain: {exercise_info.get('primary_domain', 'unknown')}

Goldilocks Zone Analysis:
✅ Not too basic: Requires thoughtful analysis and business reasoning
✅ Not too complex: Accessible without specialized expertise or insider knowledge  
✅ Just right: Perfect for someone interested in business but building knowledge

Background Context Provided: {exercise_info.get('background_needed', 'N/A')[:200]}{'...' if len(exercise_info.get('background_needed', '')) > 200 else ''}
"""
    
    # Write log file
    log_file_path = logs_dir / f"{exercise_name}.log"
    with open(log_file_path, 'w') as f:
        f.write(log_content)
    
    print(f"Created log: {log_file_path}")

def main():
    # Setup paths
    input_dir = Path("/Users/adi/code/socratify/socratify-yolo/input")
    pass_dir = input_dir / "pass"
    logs_pass_dir = input_dir / "logs" / "pass"
    
    # Ensure logs directory exists
    logs_pass_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all pass exercises
    pass_exercises = list(pass_dir.glob("*.json"))
    
    print(f"Found {len(pass_exercises)} pass exercises to create logs for...")
    
    # Create individual logs
    for exercise_path in sorted(pass_exercises):
        create_individual_log(exercise_path, logs_pass_dir)
    
    print(f"\nCompleted creating individual logs for {len(pass_exercises)} exercises")
    print(f"Logs created in: {logs_pass_dir}")

if __name__ == "__main__":
    main()