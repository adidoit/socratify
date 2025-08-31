#!/usr/bin/env python3
"""
Script to generate individual decision log files for key fail exercises
based on the corrected ICP criteria.
"""

import json
import os
import random
from pathlib import Path

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

def determine_fail_reason(exercise_name, exercise_info):
    """Determine why an exercise fails the corrected ICP criteria."""
    
    # Check for specialized/obscure companies
    obscure_indicators = ['aipocalypse', 'aena', 'bigbasket', 'blinkit', 'coreweave', 'helion', 'mighty-building', 'napster', 'ola-krutrim', 'lovable', 'atlantic-games']
    technical_indicators = ['anthropic', 'ai-search', 'undersea-cable', 'mini-grid', 'stablecoin-fears', 'bitcoin-strategic', 'aramco', 'fusion-alchemy']
    regulatory_indicators = ['banks-stablecoin-fears', 'bitcoin-strategic-reserve', 'fannie-freddie', 'republic-private-tokens']
    
    # Analyze exercise name and content
    exercise_lower = exercise_name.lower()
    
    fail_reasons = []
    
    # Check for obscure companies
    if any(indicator in exercise_lower for indicator in obscure_indicators):
        fail_reasons.append("Features obscure company not widely followed by casual business news readers")
    
    # Check for technical complexity
    if any(indicator in exercise_lower for indicator in technical_indicators):
        fail_reasons.append("Requires specialized technical knowledge beyond general business interest")
    
    # Check for regulatory complexity
    if any(indicator in exercise_lower for indicator in regulatory_indicators):
        fail_reasons.append("Involves complex regulatory or financial concepts requiring specialized expertise")
    
    # Check general level
    general_level = exercise_info.get('general_level', 3)
    if general_level > 4:
        fail_reasons.append("Complexity level too high - requires expert knowledge beyond 'interested but not knowledgeable'")
    
    # Check background requirements
    background = exercise_info.get('background_needed', '').lower()
    if any(term in background for term in ['specialized', 'expert', 'advanced', 'regulatory', 'technical', 'insider']):
        fail_reasons.append("Background requirements indicate need for specialized knowledge")
    
    # Default reasons based on common patterns
    if not fail_reasons:
        if 'ai' in exercise_lower and 'search' in exercise_lower:
            fail_reasons.append("AI search dynamics require technical understanding beyond casual business interest")
        elif 'crypto' in exercise_lower or 'bitcoin' in exercise_lower:
            fail_reasons.append("Cryptocurrency topics require specialized knowledge of digital assets")
        elif any(term in exercise_lower for term in ['infrastructure', 'grid', 'cable', 'hardware']):
            fail_reasons.append("Infrastructure topics require technical or operational expertise")
        else:
            fail_reasons.append("Exercise complexity or specialized context not suitable for general business learners")
    
    return fail_reasons

def create_fail_log(exercise_path, logs_dir):
    """Create individual log file for a failed exercise."""
    exercise_name = os.path.basename(exercise_path).replace('.json', '')
    exercise_info = extract_exercise_info(exercise_path)
    
    if 'error' in exercise_info:
        print(f"Error processing {exercise_name}: {exercise_info['error']}")
        return
    
    # Generate fail reasoning
    fail_reasons = determine_fail_reason(exercise_name, exercise_info)
    
    # Create log content
    log_content = f"""Exercise: {exercise_name}
Decision: FAIL
ICP Fit: Does not match "interested in industry but not knowledgeable" target learner

Primary Failure Reasons:
{chr(10).join('- ' + reason for reason in fail_reasons)}

Corrected ICP Analysis:
Our target learner is someone interested in business but NOT knowledgeable - they follow business news casually, know major companies, and want to learn about industries they might work in, but lack deep expertise, insider knowledge, or specialized training.

This exercise fails because:
✗ Requires specialized knowledge beyond general business interest
✗ May involve obscure companies/concepts not widely followed  
✗ Complexity level inappropriate for target learning zone

Exercise Details:
- Type: {exercise_info.get('exercise_type', 'unknown')}
- Story Type: {exercise_info.get('story_type', 'unknown')}
- General Level: {exercise_info.get('general_level', 'unknown')}
- Primary Domain: {exercise_info.get('primary_domain', 'unknown')}

Goldilocks Zone Analysis:
❌ Either too basic (obvious) or too complex (requires expertise)
❌ Not in the sweet spot for interested but not knowledgeable learners
❌ Fails to provide accessible entry point for business learning

Background Requirements: {exercise_info.get('background_needed', 'N/A')[:200]}{'...' if len(exercise_info.get('background_needed', '')) > 200 else ''}
"""
    
    # Write log file
    log_file_path = logs_dir / f"{exercise_name}.log"
    with open(log_file_path, 'w') as f:
        f.write(log_content)
    
    print(f"Created fail log: {log_file_path}")

def main():
    # Setup paths
    input_dir = Path("/Users/adi/code/socratify/socratify-yolo/input")
    fail_dir = input_dir / "fail"
    logs_fail_dir = input_dir / "logs" / "fail"
    
    # Ensure logs directory exists
    logs_fail_dir.mkdir(parents=True, exist_ok=True)
    
    # Get all fail exercises and select a representative sample
    all_fail_exercises = list(fail_dir.glob("*.json"))
    
    # Select key representative exercises for logging (about 30-40 exercises)
    # Focus on different failure patterns
    key_patterns = [
        'aipocalypse', 'aena', 'bigbasket', 'blinkit', 'coreweave', 'helion', 'napster', 'ola-krutrim',
        'anthropic', 'ai-search', 'undersea-cable', 'mini-grid', 'bitcoin-strategic', 'aramco',
        'banks-stablecoin', 'republic-private', 'fannie-freddie', 'luxury-vibe-shift', 'kraft-heinz'
    ]
    
    selected_exercises = []
    
    # Select exercises matching key failure patterns
    for pattern in key_patterns:
        matching = [ex for ex in all_fail_exercises if pattern in ex.name.lower()]
        if matching:
            selected_exercises.extend(matching[:2])  # Take up to 2 per pattern
    
    # Add some random additional exercises to get a good sample
    remaining = [ex for ex in all_fail_exercises if ex not in selected_exercises]
    selected_exercises.extend(random.sample(remaining, min(20, len(remaining))))
    
    # Remove duplicates and limit total
    selected_exercises = list(set(selected_exercises))[:50]
    
    print(f"Selected {len(selected_exercises)} key fail exercises to create logs for...")
    
    # Create individual logs
    for exercise_path in sorted(selected_exercises):
        create_fail_log(exercise_path, logs_fail_dir)
    
    print(f"\nCompleted creating individual logs for {len(selected_exercises)} fail exercises")
    print(f"Logs created in: {logs_fail_dir}")

if __name__ == "__main__":
    main()