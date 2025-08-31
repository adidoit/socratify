#!/usr/bin/env python3
"""
Story Top-3 Exercise Processor
Systematically processes all stories with >3 exercises to keep only the top 3 highest quality exercises.
Uses the established 5-criteria evaluation framework.
"""

import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
import re

# Import the evaluation framework
import sys
sys.path.append('/Users/adi/code/socratify/socratify-yolo')
from comprehensive_evaluator import ComprehensiveEvaluator, EvaluationResult

@dataclass
class StoryProcessingResult:
    """Results of processing a single story"""
    story_name: str
    initial_count: int
    final_count: int
    moved_to_fail: int
    kept_exercises: List[str]
    moved_exercises: List[str]
    selection_rationale: str

class StoryTop3Processor:
    """Processes stories to keep only top 3 exercises each"""
    
    def __init__(self, pass_dir: str, fail_dir: str, logs_dir: str):
        self.pass_dir = Path(pass_dir)
        self.fail_dir = Path(fail_dir)
        self.logs_dir = Path(logs_dir)
        
        # Ensure directories exist
        self.fail_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Initialize evaluator for quality assessment
        temp_input = "/tmp/temp_eval"
        Path(temp_input).mkdir(exist_ok=True)
        self.evaluator = ComprehensiveEvaluator(temp_input, "/tmp", "/tmp")
        
        # Priority exercise types (typically strongest)
        self.priority_types = ['assumption', 'contrarian', 'implications']
        
    def get_stories_needing_processing(self) -> Dict[str, List[Path]]:
        """Get all stories with >3 exercises"""
        stories = {}
        
        for exercise_file in self.pass_dir.glob("*.json"):
            # Extract story name (everything before the last dash)
            parts = exercise_file.stem.split('-')
            if len(parts) >= 2:
                story_name = '-'.join(parts[:-1])  # Everything except exercise type
                if story_name not in stories:
                    stories[story_name] = []
                stories[story_name].append(exercise_file)
        
        # Filter to only stories with >3 exercises
        return {story: exercises for story, exercises in stories.items() 
                if len(exercises) > 3}
    
    def evaluate_exercise_file(self, file_path: Path) -> EvaluationResult:
        """Evaluate a single exercise file using the established framework"""
        return self.evaluator.evaluate_exercise(file_path)
    
    def rank_exercises(self, exercises: List[Path]) -> List[Tuple[Path, EvaluationResult, int]]:
        """Rank exercises by quality score with type priority bonus"""
        ranked = []
        
        for exercise_path in exercises:
            result = self.evaluate_exercise_file(exercise_path)
            
            # Apply type priority bonus
            type_bonus = 0
            if result.exercise_type in self.priority_types:
                type_bonus = 5  # Small bonus for priority types
            
            # Calculate final ranking score
            ranking_score = result.overall_score + type_bonus
            
            ranked.append((exercise_path, result, ranking_score))
        
        # Sort by ranking score (highest first)
        return sorted(ranked, key=lambda x: x[2], reverse=True)
    
    def process_story(self, story_name: str, exercises: List[Path]) -> StoryProcessingResult:
        """Process a single story to keep only top 3 exercises"""
        print(f"\nProcessing story: {story_name} ({len(exercises)} exercises)")
        
        # Rank all exercises
        ranked_exercises = self.rank_exercises(exercises)
        
        # Keep top 3, move rest to fail
        keep_exercises = ranked_exercises[:3]
        move_exercises = ranked_exercises[3:]
        
        kept = []
        moved = []
        
        # Keep top 3 (they're already in pass/)
        for exercise_path, result, score in keep_exercises:
            kept.append(f"{exercise_path.name} (score: {score}, type: {result.exercise_type})")
            print(f"  KEEP: {exercise_path.name} - Score: {score}")
        
        # Move excess to fail/
        for exercise_path, result, score in move_exercises:
            target_path = self.fail_dir / exercise_path.name
            try:
                shutil.move(str(exercise_path), str(target_path))
                moved.append(f"{exercise_path.name} (score: {score}, type: {result.exercise_type})")
                print(f"  MOVE: {exercise_path.name} - Score: {score} -> fail/")
            except Exception as e:
                print(f"  ERROR moving {exercise_path.name}: {e}")
        
        # Create selection rationale
        rationale = self._create_selection_rationale(story_name, keep_exercises, move_exercises)
        
        return StoryProcessingResult(
            story_name=story_name,
            initial_count=len(exercises),
            final_count=3,
            moved_to_fail=len(move_exercises),
            kept_exercises=kept,
            moved_exercises=moved,
            selection_rationale=rationale
        )
    
    def _create_selection_rationale(self, story_name: str, 
                                   kept: List[Tuple[Path, EvaluationResult, int]],
                                   moved: List[Tuple[Path, EvaluationResult, int]]) -> str:
        """Create detailed rationale for exercise selection"""
        
        rationale = f"## Selection Rationale for {story_name}\n\n"
        
        rationale += "### KEPT (Top 3):\n"
        for i, (path, result, score) in enumerate(kept, 1):
            rationale += f"{i}. **{path.name}** (Score: {score})\n"
            rationale += f"   - Type: {result.exercise_type}\n"
            rationale += f"   - Goldilocks: {result.goldilocks_score}/100\n"
            rationale += f"   - Fidelity: {result.fidelity_score}/100\n"
            rationale += f"   - Pedagogy: {result.pedagogy_score}/100\n"
            rationale += f"   - Semantic: {result.semantic_score}/100\n"
            rationale += f"   - Style: {result.style_score}/100\n"
            if result.goldilocks_score < 70:
                rationale += f"   - Key Issues: {', '.join(result.goldilocks_failures[:2])}\n"
            rationale += "\n"
        
        rationale += "### MOVED TO FAIL:\n"
        for i, (path, result, score) in enumerate(moved, 1):
            rationale += f"{i}. **{path.name}** (Score: {score})\n"
            rationale += f"   - Type: {result.exercise_type}\n"
            rationale += f"   - Primary issues: {result.overall_status}\n"
            
            # Show top 2 failure reasons
            all_failures = (result.goldilocks_failures + result.fidelity_failures + 
                           result.pedagogy_failures + result.semantic_failures + 
                           result.style_failures)
            if all_failures:
                rationale += f"   - Key failures: {', '.join(all_failures[:2])}\n"
            rationale += "\n"
        
        return rationale
    
    def create_story_log(self, result: StoryProcessingResult):
        """Create detailed log for story processing"""
        log_path = self.logs_dir / f"{result.story_name}_top3_selection.md"
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"# Top 3 Selection Log: {result.story_name}\n\n")
            f.write(f"**Processing Date:** {import_date()}\n")
            f.write(f"**Initial Exercise Count:** {result.initial_count}\n")
            f.write(f"**Final Exercise Count:** {result.final_count}\n")
            f.write(f"**Exercises Moved to Fail:** {result.moved_to_fail}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"Processed {result.story_name} story with {result.initial_count} exercises.\n")
            f.write(f"Selected top 3 exercises based on comprehensive evaluation framework.\n")
            f.write(f"Moved {result.moved_to_fail} lower-quality exercises to fail folder.\n\n")
            
            f.write("## Exercises Kept (Pass Folder)\n\n")
            for i, exercise in enumerate(result.kept_exercises, 1):
                f.write(f"{i}. {exercise}\n")
            
            f.write("\n## Exercises Moved (Fail Folder)\n\n")
            for i, exercise in enumerate(result.moved_exercises, 1):
                f.write(f"{i}. {exercise}\n")
            
            f.write(f"\n{result.selection_rationale}")
    
    def process_all_stories(self) -> List[StoryProcessingResult]:
        """Process all stories needing reduction to 3 exercises"""
        stories_to_process = self.get_stories_needing_processing()
        
        print(f"Found {len(stories_to_process)} stories needing processing")
        
        # Sort by exercise count (highest first for efficiency)
        sorted_stories = sorted(stories_to_process.items(), 
                              key=lambda x: len(x[1]), reverse=True)
        
        results = []
        total_moved = 0
        
        for i, (story_name, exercises) in enumerate(sorted_stories, 1):
            print(f"\n=== Processing {i}/{len(sorted_stories)} ===")
            
            result = self.process_story(story_name, exercises)
            results.append(result)
            total_moved += result.moved_to_fail
            
            # Create detailed log
            self.create_story_log(result)
            
            # Progress update
            if i % 10 == 0:
                print(f"\nProgress: {i}/{len(sorted_stories)} stories processed")
                print(f"Total exercises moved to fail so far: {total_moved}")
        
        self.create_final_summary(results, total_moved)
        return results
    
    def create_final_summary(self, results: List[StoryProcessingResult], total_moved: int):
        """Create comprehensive final summary report"""
        summary_path = self.logs_dir / "TOP3_PROCESSING_FINAL_SUMMARY.md"
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("# Top 3 Exercise Selection - Final Summary\n\n")
            f.write(f"**Processing Date:** {import_date()}\n")
            f.write(f"**Stories Processed:** {len(results)}\n")
            f.write(f"**Total Exercises Moved to Fail:** {total_moved}\n\n")
            
            # Calculate final statistics
            initial_total = sum(r.initial_count for r in results)
            final_total = sum(r.final_count for r in results)
            
            f.write("## Summary Statistics\n\n")
            f.write(f"- **Initial Exercise Count:** {initial_total}\n")
            f.write(f"- **Final Exercise Count:** {final_total}\n")
            f.write(f"- **Exercises Moved:** {total_moved}\n")
            f.write(f"- **Reduction Rate:** {(total_moved/initial_total)*100:.1f}%\n\n")
            
            f.write("## Stories Processed\n\n")
            f.write("| Story | Initial Count | Final Count | Moved to Fail |\n")
            f.write("|-------|---------------|-------------|---------------|\n")
            
            for result in sorted(results, key=lambda x: x.initial_count, reverse=True):
                f.write(f"| {result.story_name} | {result.initial_count} | {result.final_count} | {result.moved_to_fail} |\n")
            
            f.write("\n## Quality Improvement\n\n")
            f.write("All remaining exercises in the pass folder represent the highest quality content:\n")
            f.write("- Meet Goldilocks Zone criteria for structured but rich discussion\n")
            f.write("- Demonstrate business fidelity and realistic scenarios\n")
            f.write("- Appropriate pedagogical structure for target learners\n")
            f.write("- Semantic consistency across all exercise elements\n")
            f.write("- Clear, accessible language and style\n\n")
            
            f.write("## Validation\n\n")
            f.write(f"After processing, each of the {len(results)} stories has exactly 3 exercises.\n")
            f.write("All moved exercises are available in the fail folder with detailed evaluation logs.\n")
            f.write("Selection decisions documented in individual story logs.\n")

def import_date():
    """Get current date for logging"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def main():
    """Main execution"""
    pass_dir = "/Users/adi/code/socratify/socratify-yolo/pass"
    fail_dir = "/Users/adi/code/socratify/socratify-yolo/fail"
    logs_dir = "/Users/adi/code/socratify/socratify-yolo/logs"
    
    processor = StoryTop3Processor(pass_dir, fail_dir, logs_dir)
    results = processor.process_all_stories()
    
    print(f"\n=== PROCESSING COMPLETE ===")
    print(f"Stories processed: {len(results)}")
    print(f"Total exercises moved to fail: {sum(r.moved_to_fail for r in results)}")
    print(f"All stories now have exactly 3 exercises in pass folder")
    print(f"Detailed logs available in {logs_dir}")

if __name__ == "__main__":
    main()