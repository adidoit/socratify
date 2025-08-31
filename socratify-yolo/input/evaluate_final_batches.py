#!/usr/bin/env python3

import json
import os
from collections import defaultdict

# Batch 9 stories (166-190)
BATCH_9_STORIES = [
    "shein-real-time", "singapore-budget-airline", "snap-ar-glasses", "solana-treasury", 
    "southwest-fees", "southwest-hedging", "spotify-creator-platform", "spotify-podcasting", 
    "stablecoin-disruption", "stablecoin-walmart", "starbucks-store-experience", "stripe-publishing", 
    "stripe-staying-private", "substack-ads", "substack-podcast", "swiggy-quick-commerce", 
    "tata-conglomerate", "temu-global", "tesla-insurance-data", "tesla-underwriting", 
    "threads-user", "tiffany-streetwear", "trader-joes-retail-media", "uber-baidu-autonomous", 
    "uber-partner-autonomy"
]

# Batch 10 stories (191-215)
BATCH_10_STORIES = [
    "vc-secondaries-as-ipo", "verizon-postpaid", "vinted-fees", "visa-apple-card", 
    "visa-mobile-first", "volkswagen-self-driving", "walmart-dark-stores", "walmart-freight-broker", 
    "walmart-vizio", "whatsapp-ads", "whoop-monetize-data", "youtube-won", "zara-sustainability", 
    "zomato-beyond-food", "zoom-hardware"
]

QUESTION_TYPES = ["contrarian", "trade_off", "assumption", "define_success", "options"]
THRESHOLD = 7.5

def load_exercise_scores(story_name, question_type):
    """Load scores for a specific story and question type."""
    filename = f"{story_name}-{question_type}.json"
    
    # Check main directory first
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                return data.get('exercises', [])
        except json.JSONDecodeError:
            pass
    
    # Check pass directory
    pass_file = f"pass/{filename}"
    if os.path.exists(pass_file):
        try:
            with open(pass_file, 'r') as f:
                data = json.load(f)
                return data.get('exercises', [])
        except json.JSONDecodeError:
            pass
    
    return []

def evaluate_story(story_name):
    """Evaluate a single story and return top exercises."""
    story_results = []
    max_scores = []
    
    for question_type in QUESTION_TYPES:
        exercises = load_exercise_scores(story_name, question_type)
        
        if exercises:
            # Get highest score for debugging
            max_score = max(ex.get('overall_score', 0) for ex in exercises)
            max_scores.append(max_score)
            
            # Filter exercises above threshold and sort by score
            high_quality = [ex for ex in exercises if ex.get('overall_score', 0) >= THRESHOLD]
            high_quality.sort(key=lambda x: x.get('overall_score', 0), reverse=True)
            
            # Take top exercise for this question type
            if high_quality:
                best_exercise = high_quality[0]
                story_results.append({
                    'story': story_name,
                    'question_type': question_type,
                    'score': best_exercise.get('overall_score', 0),
                    'exercise_text': best_exercise.get('exercise', '')[:200] + '...'
                })
    
    # Debug info
    if max_scores and max(max_scores) < THRESHOLD:
        print(f"    Max score for {story_name}: {max(max_scores):.1f}")
    
    # Sort by score and take top 3
    story_results.sort(key=lambda x: x['score'], reverse=True)
    return story_results[:3]

def evaluate_batch(batch_name, stories):
    """Evaluate a batch of stories."""
    print(f"\n=== EVALUATING {batch_name} ===")
    batch_results = []
    
    for story in stories:
        print(f"Processing {story}...")
        top_exercises = evaluate_story(story)
        batch_results.extend(top_exercises)
        
        if top_exercises:
            print(f"  Found {len(top_exercises)} high-quality exercises")
            for ex in top_exercises:
                print(f"    {ex['question_type']}: {ex['score']:.1f}")
        else:
            print(f"  No exercises above {THRESHOLD} threshold")
    
    return batch_results

def main():
    """Main evaluation function."""
    print("Starting final batch evaluation...")
    
    # Evaluate both batches
    batch_9_results = evaluate_batch("BATCH 9", BATCH_9_STORIES)
    batch_10_results = evaluate_batch("BATCH 10", BATCH_10_STORIES)
    
    # Combine results
    all_results = batch_9_results + batch_10_results
    
    # Summary statistics
    print(f"\n=== FINAL SUMMARY ===")
    print(f"Batch 9: {len(batch_9_results)} high-quality exercises from {len(BATCH_9_STORIES)} stories")
    print(f"Batch 10: {len(batch_10_results)} high-quality exercises from {len(BATCH_10_STORIES)} stories")
    print(f"Total: {len(all_results)} high-quality exercises from {len(BATCH_9_STORIES + BATCH_10_STORIES)} stories")
    
    # Question type breakdown
    type_counts = defaultdict(int)
    for result in all_results:
        type_counts[result['question_type']] += 1
    
    print(f"\nQuestion type distribution:")
    for qtype, count in sorted(type_counts.items()):
        print(f"  {qtype}: {count}")
    
    # Top scoring exercises
    all_results.sort(key=lambda x: x['score'], reverse=True)
    print(f"\nTop 10 exercises:")
    for i, result in enumerate(all_results[:10], 1):
        print(f"  {i}. {result['story']} ({result['question_type']}): {result['score']:.1f}")
    
    # Save results
    results_data = {
        'batch_9_results': batch_9_results,
        'batch_10_results': batch_10_results,
        'summary': {
            'total_exercises': len(all_results),
            'total_stories': len(BATCH_9_STORIES + BATCH_10_STORIES),
            'type_counts': dict(type_counts),
            'average_score': sum(r['score'] for r in all_results) / len(all_results) if all_results else 0
        }
    }
    
    with open('final_batches_results.json', 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"\nResults saved to final_batches_results.json")

if __name__ == "__main__":
    main()