#!/usr/bin/env python3
"""
Complete Story Processor - Final cleanup to ensure ALL stories have exactly 3 exercises
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import re

# Import the evaluation framework
import sys
sys.path.append('/Users/adi/code/socratify/socratify-yolo')
from comprehensive_evaluator import ComprehensiveEvaluator

class CompleteStoryProcessor:
    """Final processor to ensure all stories have exactly 3 exercises"""
    
    def __init__(self, pass_dir: str, fail_dir: str, logs_dir: str):
        self.pass_dir = Path(pass_dir)
        self.fail_dir = Path(fail_dir)
        self.logs_dir = Path(logs_dir)
        
        # Initialize evaluator
        temp_input = "/tmp/temp_eval"
        Path(temp_input).mkdir(exist_ok=True)
        self.evaluator = ComprehensiveEvaluator(temp_input, "/tmp", "/tmp")
        
        # Priority exercise types
        self.priority_types = ['assumption', 'contrarian', 'implications']
    
    def extract_story_name(self, filename: str) -> str:
        """Extract story name from filename more accurately"""
        # Remove .json extension
        base = filename.replace('.json', '')
        
        # Exercise types that can appear at the end
        exercise_types = [
            'assumption', 'contrarian', 'implications', 'question', 'questions',
            'define_success', 'elevator_pitch', 'hypothesis', 'options', 
            'response', 'trade_off', 'data'
        ]
        
        # Try to find the exercise type and remove it
        for ex_type in exercise_types:
            if base.endswith('-' + ex_type):
                return base[:-len('-' + ex_type)]
        
        # If no exercise type found, take everything except last part
        parts = base.split('-')
        if len(parts) > 1:
            return '-'.join(parts[:-1])
        
        return base
    
    def get_all_stories(self) -> Dict[str, List[Path]]:
        """Get all stories with their exercises"""
        stories = {}
        
        for exercise_file in self.pass_dir.glob("*.json"):
            story_name = self.extract_story_name(exercise_file.name) 
            if story_name not in stories:
                stories[story_name] = []
            stories[story_name].append(exercise_file)
        
        return stories
    
    def evaluate_and_rank(self, exercises: List[Path]) -> List[Tuple[Path, int]]:
        """Evaluate and rank exercises by quality"""
        ranked = []
        
        for exercise_path in exercises:
            result = self.evaluator.evaluate_exercise(exercise_path)
            
            # Apply type priority bonus
            type_bonus = 0
            if result.exercise_type in self.priority_types:
                type_bonus = 5
            
            ranking_score = result.overall_score + type_bonus
            ranked.append((exercise_path, ranking_score))
        
        return sorted(ranked, key=lambda x: x[1], reverse=True)
    
    def process_story(self, story_name: str, exercises: List[Path]) -> Tuple[int, int]:
        """Process one story to have exactly 3 exercises"""
        if len(exercises) <= 3:
            return 0, len(exercises)  # No changes needed
        
        print(f"Processing {story_name}: {len(exercises)} -> 3 exercises")
        
        # Rank exercises
        ranked = self.evaluate_and_rank(exercises)
        
        # Keep top 3, move rest to fail
        keep_count = 0
        move_count = 0
        
        for i, (exercise_path, score) in enumerate(ranked):
            if i < 3:
                # Keep (already in pass folder)
                keep_count += 1
                print(f"  KEEP: {exercise_path.name} (score: {score})")
            else:
                # Move to fail
                target_path = self.fail_dir / exercise_path.name
                try:
                    shutil.move(str(exercise_path), str(target_path))
                    move_count += 1
                    print(f"  MOVE: {exercise_path.name} (score: {score}) -> fail/")
                except Exception as e:
                    print(f"  ERROR moving {exercise_path.name}: {e}")
        
        return move_count, keep_count
    
    def run_complete_processing(self) -> Dict:
        """Process all stories to have exactly 3 exercises"""
        all_stories = self.get_all_stories()
        
        stories_over_3 = {name: exercises for name, exercises in all_stories.items() 
                         if len(exercises) > 3}
        
        print(f"Found {len(stories_over_3)} stories needing processing")
        print(f"Total stories: {len(all_stories)}")
        
        total_moved = 0
        processed_count = 0
        
        # Sort by number of exercises (highest first)
        sorted_stories = sorted(stories_over_3.items(), 
                              key=lambda x: len(x[1]), reverse=True)
        
        for story_name, exercises in sorted_stories:
            moved, kept = self.process_story(story_name, exercises)
            total_moved += moved
            processed_count += 1
            
            if processed_count % 10 == 0:
                print(f"Progress: {processed_count}/{len(stories_over_3)} stories processed")
        
        # Final validation
        final_stories = self.get_all_stories()
        stories_still_over_3 = {name: exercises for name, exercises in final_stories.items() 
                               if len(exercises) > 3}
        
        print(f"\n=== FINAL RESULTS ===")
        print(f"Stories processed: {processed_count}")
        print(f"Exercises moved to fail: {total_moved}")
        print(f"Stories still over 3: {len(stories_still_over_3)}")
        
        if stories_still_over_3:
            print("Stories still needing processing:")
            for name, exercises in stories_still_over_3.items():
                print(f"  {name}: {len(exercises)} exercises")
        else:
            print("SUCCESS: All stories now have ≤3 exercises!")
        
        return {
            "processed": processed_count,
            "moved": total_moved,
            "remaining_over_3": len(stories_still_over_3),
            "total_stories": len(final_stories)
        }

def main():
    pass_dir = "/Users/adi/code/socratify/socratify-yolo/pass"
    fail_dir = "/Users/adi/code/socratify/socratify-yolo/fail"
    logs_dir = "/Users/adi/code/socratify/socratify-yolo/logs"
    
    processor = CompleteStoryProcessor(pass_dir, fail_dir, logs_dir)
    results = processor.run_complete_processing()
    
    print(f"\n=== PROCESSING COMPLETE ===")
    print(f"All stories should now have exactly 3 exercises each")

if __name__ == "__main__":
    main()