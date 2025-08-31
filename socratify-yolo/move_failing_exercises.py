#!/usr/bin/env python3
"""
Move failing exercises from pass to fail folder based on evaluation results
"""

import json
import shutil
from pathlib import Path

def move_failing_exercises():
    """Move exercises that scored below 65 to fail folder"""
    
    # Load evaluation results
    results_file = Path("/Users/adi/code/socratify/socratify-yolo/comprehensive_evaluation_results.json")
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    pass_folder = Path("/Users/adi/code/socratify/socratify-yolo/pass")
    fail_folder = Path("/Users/adi/code/socratify/socratify-yolo/fail")
    
    exercises_to_move = results['recommendations']['MOVE_TO_FAIL']
    
    print(f"Moving {len(exercises_to_move)} exercises from pass to fail folder...")
    
    moved_count = 0
    for exercise_name in exercises_to_move:
        source_file = pass_folder / f"{exercise_name}.json"
        target_file = fail_folder / f"{exercise_name}.json"
        
        if source_file.exists():
            try:
                shutil.move(str(source_file), str(target_file))
                moved_count += 1
                print(f"Moved: {exercise_name}")
            except Exception as e:
                print(f"Error moving {exercise_name}: {e}")
        else:
            print(f"File not found: {exercise_name}")
    
    print(f"\nSuccessfully moved {moved_count} exercises to fail folder")
    
    # Update counts
    remaining_pass = len(list(pass_folder.glob("*.json")))
    total_fail = len(list(fail_folder.glob("*.json")))
    
    print(f"Remaining in pass folder: {remaining_pass}")
    print(f"Total in fail folder: {total_fail}")


def analyze_top_performers():
    """Analyze the top performing exercises in detail"""
    
    results_file = Path("/Users/adi/code/socratify/socratify-yolo/comprehensive_evaluation_results.json")
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    # Get exercises with scores 80+ (excellent and very good)
    excellent_exercises = []
    for exercise_name, eval_data in results['detailed_results'].items():
        if eval_data['total_score'] >= 80:
            excellent_exercises.append((exercise_name, eval_data))
    
    # Sort by score
    excellent_exercises.sort(key=lambda x: x[1]['total_score'], reverse=True)
    
    print(f"\n=== TOP PERFORMING EXERCISES (Score ≥ 80) ===")
    print(f"Found {len(excellent_exercises)} excellent exercises:")
    
    for exercise_name, eval_data in excellent_exercises:
        score = eval_data['total_score']
        print(f"\n{exercise_name}: {score:.1f}/100")
        
        # Show category breakdown
        categories = eval_data['category_scores']
        print(f"  - Accessibility: {categories['accessibility']:.1f}/100")
        print(f"  - Goldilocks Zone: {categories['goldilocks_zone']:.1f}/100") 
        print(f"  - Mobile Discussion: {categories['mobile_discussion']:.1f}/100")
        print(f"  - Learning Value: {categories['learning_value']:.1f}/100")
        print(f"  - Quality Execution: {categories['quality_execution']:.1f}/100")
    
    # Analyze by exercise type for top performers
    print(f"\n=== EXCELLENCE BY EXERCISE TYPE ===")
    type_analysis = {}
    for exercise_name, eval_data in excellent_exercises:
        exercise_type = exercise_name.split('-')[-1] if '-' in exercise_name else 'unknown'
        if exercise_type not in type_analysis:
            type_analysis[exercise_type] = []
        type_analysis[exercise_type].append((exercise_name, eval_data['total_score']))
    
    for exercise_type, exercises in type_analysis.items():
        avg_score = sum(score for _, score in exercises) / len(exercises)
        print(f"{exercise_type.title()}: {len(exercises)} exercises, avg {avg_score:.1f}")
        for name, score in exercises:
            print(f"  - {name}: {score:.1f}")


def analyze_improvement_needs():
    """Analyze exercises that need improvement"""
    
    results_file = Path("/Users/adi/code/socratify/socratify-yolo/comprehensive_evaluation_results.json")
    with open(results_file, 'r') as f:
        results = json.load(f)
    
    improvement_exercises = results['recommendations']['IMPROVE']
    
    # Analyze most common improvement areas
    improvement_areas = {}
    
    for exercise_name in improvement_exercises:
        eval_data = results['detailed_results'][exercise_name]
        actions = eval_data['action_needed']
        
        for action in actions:
            if action not in improvement_areas:
                improvement_areas[action] = []
            improvement_areas[action].append(exercise_name)
    
    print(f"\n=== IMPROVEMENT ANALYSIS ===")
    print(f"Total exercises needing improvement: {len(improvement_exercises)}")
    print(f"\nMost common improvement areas:")
    
    sorted_areas = sorted(improvement_areas.items(), key=lambda x: len(x[1]), reverse=True)
    
    for area, exercises in sorted_areas:
        print(f"{area}: {len(exercises)} exercises ({len(exercises)/len(improvement_exercises)*100:.1f}%)")
    
    # Show specific examples for top areas
    print(f"\n=== IMPROVEMENT EXAMPLES ===")
    for area, exercises in sorted_areas[:3]:  # Top 3 areas
        print(f"\n{area} - Examples:")
        for exercise in exercises[:5]:  # Show 5 examples
            score = results['detailed_results'][exercise]['total_score']
            print(f"  - {exercise}: {score:.1f}/100")


if __name__ == "__main__":
    move_failing_exercises()
    analyze_top_performers()
    analyze_improvement_needs()