#!/usr/bin/env python3
"""
Final Story Processor - Handle all story name patterns correctly
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple
import re
from collections import defaultdict

# Import the evaluation framework
import sys
sys.path.append('/Users/adi/code/socratify/socratify-yolo')
from comprehensive_evaluator import ComprehensiveEvaluator

class FinalStoryProcessor:
    """Final processor with sophisticated story name extraction"""
    
    def __init__(self, pass_dir: str, fail_dir: str, logs_dir: str):
        self.pass_dir = Path(pass_dir)
        self.fail_dir = Path(fail_dir)
        self.logs_dir = Path(logs_dir)
        
        # Initialize evaluator
        temp_input = "/tmp/temp_eval"
        Path(temp_input).mkdir(exist_ok=True)
        self.evaluator = ComprehensiveEvaluator(temp_input, "/tmp", "/tmp")
        
        # Exercise types that appear at the end of filenames
        self.exercise_types = {
            'assumption', 'contrarian', 'implications', 'question', 'questions',
            'define_success', 'elevator_pitch', 'hypothesis', 'options', 
            'response', 'trade_off', 'data'
        }
        
        # Priority types for ranking
        self.priority_types = ['assumption', 'contrarian', 'implications']
    
    def extract_story_name(self, filename: str) -> str:
        """Extract story name by removing exercise type suffix"""
        base = filename.replace('.json', '')
        parts = base.split('-')
        
        # Work backwards to find exercise type
        for i in range(len(parts) - 1, 0, -1):
            potential_type = '-'.join(parts[i:])
            if potential_type in self.exercise_types:
                return '-'.join(parts[:i])
        
        # If no exercise type found, remove last part as fallback
        if len(parts) > 1:
            return '-'.join(parts[:-1])
        
        return base
    
    def analyze_stories(self) -> Dict[str, List[Path]]:
        """Analyze all stories and their exercises"""
        stories = defaultdict(list)
        
        for exercise_file in self.pass_dir.glob("*.json"):
            story_name = self.extract_story_name(exercise_file.name)
            stories[story_name].append(exercise_file)
        
        return dict(stories)
    
    def rank_exercises(self, exercises: List[Path]) -> List[Tuple[Path, int, str]]:
        """Rank exercises by quality score"""
        ranked = []
        
        for exercise_path in exercises:
            result = self.evaluator.evaluate_exercise(exercise_path)
            
            # Type priority bonus
            type_bonus = 5 if result.exercise_type in self.priority_types else 0
            final_score = result.overall_score + type_bonus
            
            ranked.append((exercise_path, final_score, result.exercise_type))
        
        return sorted(ranked, key=lambda x: x[1], reverse=True)
    
    def process_oversized_story(self, story_name: str, exercises: List[Path]) -> Tuple[int, int]:
        """Process a story with >3 exercises"""
        print(f"\nProcessing {story_name}: {len(exercises)} exercises")
        
        # Show all exercises for this story
        for ex in exercises:
            print(f"  - {ex.name}")
        
        # Rank exercises
        ranked = self.rank_exercises(exercises)
        
        moved_count = 0
        kept_count = 0
        
        print(f"\nRanking for {story_name}:")
        for i, (path, score, ex_type) in enumerate(ranked):
            if i < 3:
                print(f"  KEEP #{i+1}: {path.name} (score: {score}, type: {ex_type})")
                kept_count += 1
            else:
                # Move to fail folder
                target_path = self.fail_dir / path.name
                try:
                    shutil.move(str(path), str(target_path))
                    print(f"  MOVE: {path.name} (score: {score}, type: {ex_type}) -> fail/")
                    moved_count += 1
                except Exception as e:
                    print(f"  ERROR: Could not move {path.name}: {e}")
        
        return moved_count, kept_count
    
    def run_final_processing(self) -> Dict:
        """Run the final processing to ensure all stories have ≤3 exercises"""
        print("=== FINAL STORY PROCESSING ===")
        
        stories = self.analyze_stories()
        
        # Find stories with >3 exercises
        oversized_stories = {name: exercises for name, exercises in stories.items() 
                           if len(exercises) > 3}
        
        print(f"Total stories found: {len(stories)}")
        print(f"Stories with >3 exercises: {len(oversized_stories)}")
        
        if not oversized_stories:
            print("SUCCESS: All stories already have ≤3 exercises!")
            return {"processed": 0, "moved": 0, "final_over_3": 0}
        
        # Show oversized stories
        print("\nOversized stories:")
        for name, exercises in sorted(oversized_stories.items(), 
                                    key=lambda x: len(x[1]), reverse=True):
            print(f"  {name}: {len(exercises)} exercises")
        
        # Process each oversized story
        total_moved = 0
        total_processed = 0
        
        for story_name, exercises in sorted(oversized_stories.items(), 
                                          key=lambda x: len(x[1]), reverse=True):
            moved, kept = self.process_oversized_story(story_name, exercises)
            total_moved += moved
            total_processed += 1
            
            print(f"  Result: Kept {kept}, Moved {moved}")
        
        # Final validation
        final_stories = self.analyze_stories()
        final_oversized = {name: exercises for name, exercises in final_stories.items() 
                          if len(exercises) > 3}
        
        print(f"\n=== FINAL VALIDATION ===")
        print(f"Stories processed: {total_processed}")
        print(f"Exercises moved to fail: {total_moved}")
        print(f"Stories still >3: {len(final_oversized)}")
        
        if final_oversized:
            print("WARNING: These stories still have >3 exercises:")
            for name, exercises in final_oversized.items():
                print(f"  {name}: {len(exercises)} exercises")
        else:
            print("SUCCESS: All stories now have ≤3 exercises!")
        
        return {
            "processed": total_processed,
            "moved": total_moved,
            "final_over_3": len(final_oversized),
            "total_stories": len(final_stories)
        }

def main():
    pass_dir = "/Users/adi/code/socratify/socratify-yolo/pass"
    fail_dir = "/Users/adi/code/socratify/socratify-yolo/fail"
    logs_dir = "/Users/adi/code/socratify/socratify-yolo/logs"
    
    processor = FinalStoryProcessor(pass_dir, fail_dir, logs_dir)
    results = processor.run_final_processing()
    
    print(f"\n=== PROCESSING COMPLETE ===")
    if results["final_over_3"] == 0:
        print("✅ SUCCESS: All stories now have exactly 3 exercises or fewer!")
    else:
        print(f"⚠️  {results['final_over_3']} stories still need manual review")
    
    print(f"Total exercises moved: {results['moved']}")
    print(f"Total stories: {results['total_stories']}")

if __name__ == "__main__":
    main()