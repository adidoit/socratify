#!/usr/bin/env python3
"""
Check completion status for Batch 8 stories
"""

import os
import subprocess
from pathlib import Path

# Batch 8 stories
BATCH_8_STORIES = [
    "nintendo-brand-extension",
    "nissan-tarriffs", 
    "ola-krutrim",
    "openai-ads",
    "openai-mattel",
    "oura-vs-tech",
    "patagonia-purpose",
    "paytm-super-app",
    "peloton-retail",
    "pepsico-snack",
    "porsche-crossroads",
    "replit-monetization",
    "robinhood-prediction",
    "roblox-education",
]

# Priority exercise types (based on optimized methodology)
PRIORITY_TYPES = [
    "contrarian",
    "trade_off", 
    "assumption",
    "define_success",
    "options"
]

# Base path
BASE_PATH = Path("/Users/adi/code/socratify/socratify-agent/exercises/v2/data/exercises")

def check_exercise_status(story, exercise_type):
    """Check if an exercise needs processing"""
    exercise_file = BASE_PATH / story / "0-checklist" / f"{story}-{exercise_type}.md"
    
    if not exercise_file.exists():
        return "NOT_FOUND"
    
    # Check if PASS-rated
    try:
        content = exercise_file.read_text()
        if "<recommendation>PASS</recommendation>" not in content:
            return "NOT_PASS"
    except:
        return "READ_ERROR"
    
    # Check if already completed
    try:
        result = subprocess.run([
            "python", 
            "/Users/adi/code/socratify/socratify-agent/exercises/v2/agentic_workflow/exercise_pipeline.py",
            str(exercise_file),
            "--dry-run"
        ], capture_output=True, text=True, timeout=30)
        
        if "Exercise already completed!" in result.stdout:
            return "COMPLETED"
        elif "ERROR: Exercise is not PASS-rated!" in result.stdout:
            return "NOT_PASS"
        else:
            return "NEEDS_PROCESSING"
            
    except subprocess.TimeoutExpired:
        return "TIMEOUT"
    except:
        return "ERROR"

def main():
    print("=== BATCH 8 COMPLETION STATUS ===\n")
    
    needs_processing = []
    
    for story in BATCH_8_STORIES:
        print(f"Story: {story}")
        story_needs_processing = False
        
        for exercise_type in PRIORITY_TYPES:
            status = check_exercise_status(story, exercise_type)
            
            if status == "NEEDS_PROCESSING":
                needs_processing.append((story, exercise_type))
                story_needs_processing = True
                print(f"  ✅ {exercise_type}: NEEDS PROCESSING")
            elif status == "COMPLETED":
                print(f"  ✓ {exercise_type}: COMPLETED")
            elif status == "NOT_PASS":
                print(f"  ❌ {exercise_type}: NOT PASS-RATED")
            elif status == "NOT_FOUND":
                print(f"  ? {exercise_type}: NOT FOUND")
            else:
                print(f"  ⚠ {exercise_type}: {status}")
        
        if not story_needs_processing:
            print(f"  → All priority exercises completed for {story}")
        print()
    
    print("\n=== SUMMARY ===")
    print(f"Stories checked: {len(BATCH_8_STORIES)}")
    print(f"Exercises needing processing: {len(needs_processing)}")
    
    if needs_processing:
        print("\nExercises to process:")
        for story, exercise_type in needs_processing:
            print(f"  - {story}-{exercise_type}")
    else:
        print("\n🎉 All priority exercises in Batch 8 are already completed!")

if __name__ == "__main__":
    main()