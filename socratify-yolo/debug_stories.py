#!/usr/bin/env python3
"""Debug story extraction"""

from pathlib import Path
from collections import defaultdict

def extract_story_name(filename: str) -> str:
    """Extract story name by removing exercise type suffix"""
    base = filename.replace('.json', '')
    
    exercise_types = {
        'assumption', 'contrarian', 'implications', 'question', 'questions',
        'define_success', 'elevator_pitch', 'hypothesis', 'options', 
        'response', 'trade_off', 'data'
    }
    
    parts = base.split('-')
    
    # Work backwards to find exercise type
    for i in range(len(parts) - 1, 0, -1):
        potential_type = '-'.join(parts[i:])
        if potential_type in exercise_types:
            return '-'.join(parts[:i])
    
    # If no exercise type found, remove last part as fallback
    if len(parts) > 1:
        return '-'.join(parts[:-1])
    
    return base

def main():
    pass_dir = Path("/Users/adi/code/socratify/socratify-yolo/pass")
    stories = defaultdict(list)
    
    for exercise_file in pass_dir.glob("*.json"):
        story_name = extract_story_name(exercise_file.name)
        stories[story_name].append(exercise_file.name)
    
    # Show stories with >3 exercises
    oversized = {name: exercises for name, exercises in stories.items() if len(exercises) > 3}
    
    print(f"Total stories: {len(stories)}")
    print(f"Oversized stories: {len(oversized)}")
    
    if oversized:
        print("\nStories with >3 exercises:")
        for name, exercises in sorted(oversized.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"\n{name} ({len(exercises)} exercises):")
            for ex in exercises:
                print(f"  - {ex}")
    else:
        print("No stories found with >3 exercises")
        
        # Show some examples
        print("\nFirst 10 stories:")
        for name, exercises in list(stories.items())[:10]:
            print(f"{name}: {len(exercises)} exercises")

if __name__ == "__main__":
    main()