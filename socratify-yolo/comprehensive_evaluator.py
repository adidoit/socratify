#!/usr/bin/env python3
"""
Comprehensive Exercise Evaluator for Socratify
Evaluates all exercises against 5 criteria: Goldilocks, Fidelity, Pedagogy, Semantic, Style
"""

import json
import os
import re
from typing import Dict, List, Any, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path

@dataclass
class EvaluationResult:
    """Results of evaluating an exercise against all criteria"""
    exercise_name: str
    exercise_type: str
    goldilocks_score: int  # 0-100
    fidelity_score: int    # 0-100
    pedagogy_score: int    # 0-100
    semantic_score: int    # 0-100
    style_score: int       # 0-100
    overall_score: int     # 0-100
    overall_status: str    # PASS/FAIL
    category: str          # pass/fail/rewrite
    
    # Detailed failures by criteria
    goldilocks_failures: List[str]
    fidelity_failures: List[str]
    pedagogy_failures: List[str]
    semantic_failures: List[str]
    style_failures: List[str]
    
    # Summary assessments
    goldilocks_summary: str
    fidelity_summary: str
    pedagogy_summary: str
    semantic_summary: str
    style_summary: str

class ComprehensiveEvaluator:
    """Evaluates exercises against all 5 Socratify criteria"""
    
    def __init__(self, input_dir: str, output_dir: str, logs_dir: str):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.logs_dir = Path(logs_dir)
        
        # Create output directories
        (self.output_dir / "pass").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "fail").mkdir(parents=True, exist_ok=True)
        (self.output_dir / "rewrite").mkdir(parents=True, exist_ok=True)
        
        # Create log directories
        (self.logs_dir / "pass").mkdir(parents=True, exist_ok=True)
        (self.logs_dir / "fail").mkdir(parents=True, exist_ok=True)
        (self.logs_dir / "rewrite").mkdir(parents=True, exist_ok=True)
        
        # Business jargon to flag
        self.business_jargon = {
            'leverage', 'utilize', 'optimize', 'strategic', 'ecosystem', 
            'synergy', 'best practices', 'stakeholders', 'touch base',
            'deep dive', 'low-hanging fruit', 'facilitate', 'commence',
            'terminate', 'subsequent', 'prior to', 'in order to',
            'due to the fact that', 'at this point in time'
        }
        
        # Filler phrases to flag
        self.filler_phrases = {
            "it's worth noting", "when done correctly", "at the end of the day",
            "the bottom line is", "here's the kicker", "but wait, there's more",
            "the key insight is", "moving forward", "in today's landscape",
            "this comprehensive approach", "it should be noted that",
            "what's interesting is", "the fact of the matter is",
            "when you really think about it", "to be perfectly honest"
        }
    
    def load_exercise(self, file_path: Path) -> Dict[str, Any]:
        """Load exercise JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return {}
    
    def evaluate_goldilocks(self, exercise: Dict[str, Any]) -> Tuple[int, List[str], str]:
        """Evaluate Goldilocks Zone criteria - structured but rich questions"""
        failures = []
        score = 100
        
        key_question = exercise.get('keyQuestion', {})
        question_text = key_question.get('keyQuestionText', '')
        choices = key_question.get('choices', [])
        exercise_type = exercise.get('exerciseType', '')
        
        # Check for overly open questions (blue sky paralysis)
        if any(phrase in question_text.lower() for phrase in ['what should', 'how should', 'what do you think about']):
            if not any(constraint in question_text.lower() for constraint in ['specific', 'most', 'first', 'which']):
                failures.append("Overly open question - blue sky paralysis risk")
                score -= 30
        
        # Check for overly closed questions (simplistic single-track)
        binary_indicators = ['should', 'will', 'do', 'is', 'can', 'would']
        if any(question_text.lower().startswith(word) for word in binary_indicators):
            if len(choices) < 3:
                failures.append("Overly closed question - binary choice limits discussion")
                score -= 30
        
        # Check choice quality - must represent different philosophies
        if len(choices) < 4:
            failures.append("Insufficient choices - need 4 distinct strategic philosophies")
            score -= 20
        
        # Check for curse of knowledge indicators
        if any(jargon in question_text.lower() for jargon in self.business_jargon):
            failures.append("Business jargon in key question - curse of knowledge")
            score -= 15
        
        # Check for dominant answer trap
        entity_text = exercise.get('introElements', {}).get('entityExplainer', {}).get('text', '')
        situation_text = exercise.get('introElements', {}).get('situationExplainer', {}).get('text', '')
        
        if "obviously" in (entity_text + situation_text).lower() or "clearly" in (entity_text + situation_text).lower():
            failures.append("Context points to obvious answer - dominant answer trap")
            score -= 25
        
        # Exercise type specific checks
        if exercise_type == 'assumption' and 'assuming' not in question_text.lower():
            failures.append("Assumption exercise missing assumption framing")
            score -= 20
        
        if exercise_type == 'hypothesis' and 'hypothesis' not in question_text.lower() and 'explain' not in question_text.lower():
            failures.append("Hypothesis exercise missing hypothesis framing")
            score -= 20
        
        # Mobile discussion quality - accessibility check
        if len(question_text) > 200:
            failures.append("Key question too long for mobile conversation")
            score -= 15
        
        summary = f"{'PASS' if score >= 70 else 'FAIL'} - Goldilocks evaluation for {exercise_type} exercise"
        return max(0, score), failures, summary
    
    def evaluate_fidelity(self, exercise: Dict[str, Any]) -> Tuple[int, List[str], str]:
        """Evaluate Business Fidelity - realistic, accurate business scenarios"""
        failures = []
        score = 100
        
        entity_text = exercise.get('introElements', {}).get('entityExplainer', {}).get('text', '')
        situation_text = exercise.get('introElements', {}).get('situationExplainer', {}).get('text', '')
        
        # Check for unrealistic financial figures
        import re
        numbers = re.findall(r'\$?(\d+(?:\.\d+)?)\s*(?:billion|million|%)', entity_text + situation_text, re.IGNORECASE)
        for number in numbers:
            if float(number) > 1000:  # Unrealistically large numbers
                failures.append(f"Unrealistic financial figure: {number}")
                score -= 15
        
        # Check for plausible company behavior
        if 'announced' in situation_text.lower() and 'surprising' in situation_text.lower():
            # Good - realistic business announcement
            pass
        elif 'plans to' in situation_text.lower() and any(word in situation_text.lower() for word in ['impossible', 'never', 'unheard of']):
            failures.append("Implausible company plans described")
            score -= 20
        
        # Check for market realism
        if 'market' in (entity_text + situation_text).lower():
            if any(word in (entity_text + situation_text).lower() for word in ['monopoly', 'dominates everything', 'controls all']):
                failures.append("Unrealistic market dynamics described")
                score -= 25
        
        # Check for strategic plausibility
        if 'strategy' in (entity_text + situation_text).lower():
            if any(phrase in (entity_text + situation_text).lower() for phrase in ['radical shift', 'complete pivot', 'abandon everything']):
                failures.append("Implausible strategic moves described")
                score -= 20
        
        # Check for timeline realism
        timeline_words = ['immediate', 'instantly', 'overnight', 'next week']
        if any(word in (entity_text + situation_text).lower() for word in timeline_words):
            if any(scale in (entity_text + situation_text).lower() for scale in ['major', 'massive', 'complete']):
                failures.append("Unrealistic implementation timeline")
                score -= 15
        
        summary = f"{'PASS' if score >= 70 else 'FAIL'} - Business situation appears {'realistic' if score >= 70 else 'unrealistic'}"
        return max(0, score), failures, summary
    
    def evaluate_pedagogy(self, exercise: Dict[str, Any]) -> Tuple[int, List[str], str]:
        """Evaluate Pedagogical Quality - zone of proximal development, scaffolding"""
        failures = []
        score = 100
        
        # Check zone of proximal development
        key_question = exercise.get('keyQuestion', {}).get('keyQuestionText', '')
        entity_text = exercise.get('introElements', {}).get('entityExplainer', {}).get('text', '')
        
        # Too easy check - binary questions
        if any(key_question.lower().startswith(word) for word in ['should', 'will', 'is', 'can']):
            failures.append("Question too easy - binary choice below ZPD")
            score -= 25
        
        # Too hard check - multiple complex steps
        complexity_indicators = ['design', 'create', 'develop', 'build', 'implement']
        if any(word in key_question.lower() for word in complexity_indicators):
            if 'strategy' in key_question.lower() or 'plan' in key_question.lower():
                failures.append("Question too complex - above ZPD requiring multiple steps")
                score -= 25
        
        # Check scaffolding quality
        if not entity_text:
            failures.append("Missing entity scaffolding - insufficient context")
            score -= 20
        
        # Check for established language only
        if any(jargon in (entity_text + key_question).lower() for jargon in self.business_jargon):
            failures.append("Uses business jargon - violates established language principle")
            score -= 15
        
        # Check cognitive load for mobile
        total_text = entity_text + exercise.get('introElements', {}).get('situationExplainer', {}).get('text', '')
        if len(total_text) > 1000:
            failures.append("High cognitive load - too much text for mobile")
            score -= 15
        
        # Check for first-principles reasoning
        if 'because' not in key_question.lower() and 'why' not in key_question.lower() and 'how' not in key_question.lower():
            if exercise.get('exerciseType') in ['hypothesis', 'assumption', 'contrarian']:
                failures.append("Missing first-principles reasoning prompts")
                score -= 20
        
        # Check for appropriate knowledge assumption
        technical_terms = ['API', 'SaaS', 'B2B', 'CAC', 'LTV']
        undefined_technical = [term for term in technical_terms if term in total_text and term not in entity_text]
        if undefined_technical:
            failures.append(f"Technical terms used without definition: {undefined_technical}")
            score -= 15
        
        summary = f"{'PASS' if score >= 70 else 'FAIL'} - Pedagogical structure {'appropriate' if score >= 70 else 'inappropriate'} for target learners"
        return max(0, score), failures, summary
    
    def evaluate_semantic(self, exercise: Dict[str, Any]) -> Tuple[int, List[str], str]:
        """Evaluate Semantic Consistency - all elements serve same key question"""
        failures = []
        score = 100
        
        key_question = exercise.get('keyQuestion', {}).get('keyQuestionText', '')
        entity_text = exercise.get('introElements', {}).get('entityExplainer', {}).get('text', '')
        situation_text = exercise.get('introElements', {}).get('situationExplainer', {}).get('text', '')
        cover_text = exercise.get('coverElements', {}).get('coverParagraph', '')
        mental_model = exercise.get('mentalModel', {}).get('mentalModelLinkText', '')
        
        # Extract key business challenge from key question
        challenge_keywords = []
        if 'growth' in key_question.lower():
            challenge_keywords.append('growth')
        if 'competition' in key_question.lower() or 'competitor' in key_question.lower():
            challenge_keywords.append('competition')
        if 'cost' in key_question.lower() or 'price' in key_question.lower():
            challenge_keywords.append('cost')
        if 'customer' in key_question.lower():
            challenge_keywords.append('customer')
        
        # Check element alignment with key question
        if challenge_keywords:
            if not any(keyword in entity_text.lower() for keyword in challenge_keywords):
                failures.append("Entity explainer doesn't align with key question focus")
                score -= 25
            
            if not any(keyword in situation_text.lower() for keyword in challenge_keywords):
                failures.append("Situation explainer doesn't align with key question focus")
                score -= 25
        
        # Check for semantic drift - different challenges
        entity_topics = set()
        if 'revenue' in entity_text.lower() or 'sales' in entity_text.lower():
            entity_topics.add('revenue')
        if 'market share' in entity_text.lower() or 'competition' in entity_text.lower():
            entity_topics.add('competition')
        if 'cost' in entity_text.lower() or 'efficiency' in entity_text.lower():
            entity_topics.add('operations')
        
        question_topics = set()
        if 'revenue' in key_question.lower() or 'profit' in key_question.lower():
            question_topics.add('revenue')
        if 'competitor' in key_question.lower() or 'market' in key_question.lower():
            question_topics.add('competition')
        if 'cost' in key_question.lower() or 'operations' in key_question.lower():
            question_topics.add('operations')
        
        if entity_topics and question_topics and not entity_topics.intersection(question_topics):
            failures.append("Semantic drift - entity and question focus on different topics")
            score -= 30
        
        # Check narrative coherence - same company/context
        company_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', entity_text)
        key_company_names = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', key_question)
        
        if company_names and key_company_names:
            if not any(name in key_company_names for name in company_names[:2]):  # Check first 2 company names
                failures.append("Different companies referenced in entity vs key question")
                score -= 20
        
        # Check scaffolding effectiveness
        if len(entity_text) < 50:
            failures.append("Insufficient scaffolding - entity explainer too brief")
            score -= 15
        
        if mental_model and exercise.get('exerciseType'):
            exercise_type = exercise.get('exerciseType')
            if exercise_type == 'assumption' and 'assumption' not in mental_model.lower():
                failures.append("Mental model doesn't match exercise type")
                score -= 15
        
        summary = f"{'PASS' if score >= 70 else 'FAIL'} - Elements {'aligned' if score >= 70 else 'misaligned'} with key question"
        return max(0, score), failures, summary
    
    def evaluate_style(self, exercise: Dict[str, Any]) -> Tuple[int, List[str], str]:
        """Evaluate Language & Style Quality - clear, accessible communication"""
        failures = []
        score = 100
        
        all_text = ""
        for element in ['coverElements', 'introElements']:
            if element in exercise:
                for key, value in exercise[element].items():
                    if isinstance(value, str):
                        all_text += value + " "
                    elif isinstance(value, dict) and 'text' in value:
                        all_text += value['text'] + " "
        
        key_question_text = exercise.get('keyQuestion', {}).get('keyQuestionText', '')
        all_text += key_question_text
        
        # Check for business jargon
        jargon_found = [word for word in self.business_jargon if word in all_text.lower()]
        if jargon_found:
            failures.append(f"Business jargon found: {jargon_found[:3]}")  # Show first 3
            score -= len(jargon_found) * 5
        
        # Check for filler phrases
        filler_found = [phrase for phrase in self.filler_phrases if phrase in all_text.lower()]
        if filler_found:
            failures.append(f"Filler phrases found: {filler_found[:2]}")  # Show first 2
            score -= len(filler_found) * 10
        
        # Check for passive voice indicators
        passive_indicators = ['was', 'were', 'been', 'being']
        passive_count = sum(1 for word in passive_indicators if word in all_text.lower().split())
        if passive_count > 3:
            failures.append("Excessive passive voice usage")
            score -= 15
        
        # Check for vague pronouns
        sentences = all_text.split('.')
        for sentence in sentences:
            if sentence.strip().lower().startswith(('this', 'that', 'it', 'they')):
                if len(sentence.split()) < 8:  # Short sentences with vague pronouns
                    failures.append("Vague pronouns without clear antecedents")
                    score -= 10
                    break
        
        # Check for zombie nouns (nominalizations)
        zombie_patterns = [
            'implementation of', 'make a decision', 'conduct an analysis',
            'perform an evaluation', 'give consideration to', 'make an acquisition'
        ]
        zombie_found = [pattern for pattern in zombie_patterns if pattern in all_text.lower()]
        if zombie_found:
            failures.append(f"Zombie nouns found: {zombie_found[:2]}")
            score -= len(zombie_found) * 8
        
        # Check sentence complexity
        avg_sentence_length = len(all_text.split()) / max(1, len(sentences))
        if avg_sentence_length > 25:
            failures.append("Sentences too complex for mobile conversation")
            score -= 15
        
        # Check for concrete vs abstract language
        abstract_words = ['concept', 'approach', 'methodology', 'framework', 'paradigm']
        abstract_count = sum(1 for word in abstract_words if word in all_text.lower())
        if abstract_count > 2:
            failures.append("Too much abstract language - needs concrete examples")
            score -= 10
        
        # Check for predictable combinations
        predictable_phrases = [
            'significant growth', 'operational efficiency', 'strategic initiative',
            'positive outcomes', 'enhanced experience', 'transformative technology'
        ]
        predictable_found = [phrase for phrase in predictable_phrases if phrase in all_text.lower()]
        if predictable_found:
            failures.append(f"Predictable business clichés: {predictable_found[:2]}")
            score -= len(predictable_found) * 8
        
        summary = f"{'PASS' if score >= 70 else 'FAIL'} - Language {'accessible' if score >= 70 else 'problematic'} for target audience"
        return max(0, score), failures, summary
    
    def determine_category(self, goldilocks_score: int, fidelity_score: int, 
                          pedagogy_score: int, semantic_score: int, style_score: int,
                          exercise_type: str) -> str:
        """Determine if exercise should go to pass/, fail/, or rewrite/"""
        
        # Must pass all criteria for PASS
        all_scores = [goldilocks_score, fidelity_score, pedagogy_score, semantic_score, style_score]
        
        if all(score >= 70 for score in all_scores):
            return "pass"
        
        # Strong candidates with good foundations but poor keyQuestion framing
        if (fidelity_score >= 70 and semantic_score >= 70 and 
            pedagogy_score >= 60 and style_score >= 60 and goldilocks_score < 70):
            return "rewrite"
        
        # Everything else fails
        return "fail"
    
    def evaluate_exercise(self, file_path: Path) -> EvaluationResult:
        """Evaluate a single exercise against all criteria"""
        exercise = self.load_exercise(file_path)
        
        if not exercise:
            return EvaluationResult(
                exercise_name=file_path.stem,
                exercise_type="unknown",
                goldilocks_score=0, fidelity_score=0, pedagogy_score=0,
                semantic_score=0, style_score=0, overall_score=0,
                overall_status="FAIL", category="fail",
                goldilocks_failures=["Failed to load exercise"],
                fidelity_failures=[], pedagogy_failures=[],
                semantic_failures=[], style_failures=[],
                goldilocks_summary="Failed to load", fidelity_summary="Failed to load",
                pedagogy_summary="Failed to load", semantic_summary="Failed to load",
                style_summary="Failed to load"
            )
        
        exercise_type = exercise.get('exerciseType', 'unknown')
        
        # Evaluate against all criteria
        goldilocks_score, goldilocks_failures, goldilocks_summary = self.evaluate_goldilocks(exercise)
        fidelity_score, fidelity_failures, fidelity_summary = self.evaluate_fidelity(exercise)
        pedagogy_score, pedagogy_failures, pedagogy_summary = self.evaluate_pedagogy(exercise)
        semantic_score, semantic_failures, semantic_summary = self.evaluate_semantic(exercise)
        style_score, style_failures, style_summary = self.evaluate_style(exercise)
        
        # Calculate overall score (weighted average - Goldilocks is most critical)
        overall_score = int(
            goldilocks_score * 0.3 +  # Most critical
            fidelity_score * 0.2 +
            pedagogy_score * 0.2 +
            semantic_score * 0.15 +
            style_score * 0.15
        )
        
        overall_status = "PASS" if overall_score >= 70 else "FAIL"
        category = self.determine_category(goldilocks_score, fidelity_score, pedagogy_score, 
                                         semantic_score, style_score, exercise_type)
        
        return EvaluationResult(
            exercise_name=file_path.stem,
            exercise_type=exercise_type,
            goldilocks_score=goldilocks_score,
            fidelity_score=fidelity_score,
            pedagogy_score=pedagogy_score,
            semantic_score=semantic_score,
            style_score=style_score,
            overall_score=overall_score,
            overall_status=overall_status,
            category=category,
            goldilocks_failures=goldilocks_failures,
            fidelity_failures=fidelity_failures,
            pedagogy_failures=pedagogy_failures,
            semantic_failures=semantic_failures,
            style_failures=style_failures,
            goldilocks_summary=goldilocks_summary,
            fidelity_summary=fidelity_summary,
            pedagogy_summary=pedagogy_summary,
            semantic_summary=semantic_summary,
            style_summary=style_summary
        )
    
    def save_exercise_and_log(self, exercise_path: Path, result: EvaluationResult):
        """Save exercise to appropriate category folder and create detailed log"""
        
        # Copy exercise to appropriate category
        category_dir = self.output_dir / result.category
        target_path = category_dir / exercise_path.name
        
        try:
            import shutil
            shutil.copy2(exercise_path, target_path)
        except Exception as e:
            print(f"Error copying {exercise_path} to {target_path}: {e}")
        
        # Create detailed log
        log_dir = self.logs_dir / result.category
        log_path = log_dir / f"{result.exercise_name}_evaluation.md"
        
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(f"# Evaluation Log: {result.exercise_name}\n\n")
            f.write(f"**Exercise Type:** {result.exercise_type}\n")
            f.write(f"**Overall Status:** {result.overall_status}\n")
            f.write(f"**Category:** {result.category}\n")
            f.write(f"**Overall Score:** {result.overall_score}/100\n\n")
            
            f.write("## Criteria Scores\n\n")
            f.write(f"- **Goldilocks Zone:** {result.goldilocks_score}/100\n")
            f.write(f"- **Business Fidelity:** {result.fidelity_score}/100\n")
            f.write(f"- **Pedagogical Quality:** {result.pedagogy_score}/100\n")
            f.write(f"- **Semantic Consistency:** {result.semantic_score}/100\n")
            f.write(f"- **Style Quality:** {result.style_score}/100\n\n")
            
            f.write("## Detailed Analysis\n\n")
            
            criteria = [
                ("Goldilocks Zone", result.goldilocks_failures, result.goldilocks_summary),
                ("Business Fidelity", result.fidelity_failures, result.fidelity_summary),
                ("Pedagogical Quality", result.pedagogy_failures, result.pedagogy_summary),
                ("Semantic Consistency", result.semantic_failures, result.semantic_summary),
                ("Style Quality", result.style_failures, result.style_summary)
            ]
            
            for criteria_name, failures, summary in criteria:
                f.write(f"### {criteria_name}\n")
                f.write(f"**Summary:** {summary}\n\n")
                if failures:
                    f.write("**Specific Issues:**\n")
                    for failure in failures:
                        f.write(f"- {failure}\n")
                else:
                    f.write("**Specific Issues:** None identified\n")
                f.write("\n")
    
    def run_comprehensive_evaluation(self) -> Dict[str, Any]:
        """Run evaluation on all exercises in input directory"""
        json_files = list(self.input_dir.glob("*.json"))
        total_files = len(json_files)
        
        print(f"Starting comprehensive evaluation of {total_files} exercises...")
        
        results = []
        stats = {"pass": 0, "fail": 0, "rewrite": 0}
        
        for i, file_path in enumerate(json_files, 1):
            print(f"Processing {i}/{total_files}: {file_path.name}")
            
            result = self.evaluate_exercise(file_path)
            results.append(result)
            stats[result.category] += 1
            
            # Save exercise and create log
            self.save_exercise_and_log(file_path, result)
            
            # Progress update every 50 exercises
            if i % 50 == 0:
                print(f"Progress: {i}/{total_files} ({i/total_files*100:.1f}%) - "
                      f"Pass: {stats['pass']}, Fail: {stats['fail']}, Rewrite: {stats['rewrite']}")
        
        # Generate summary report
        self.generate_summary_report(results, stats, total_files)
        
        return {
            "total_processed": total_files,
            "results": results,
            "statistics": stats
        }
    
    def generate_summary_report(self, results: List[EvaluationResult], 
                               stats: Dict[str, int], total: int):
        """Generate comprehensive evaluation summary"""
        
        report_path = self.logs_dir / "COMPREHENSIVE_EVALUATION_SUMMARY.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Comprehensive Evaluation Summary\n\n")
            f.write(f"**Total Exercises Evaluated:** {total}\n\n")
            
            f.write("## Results Distribution\n\n")
            f.write(f"- **PASS:** {stats['pass']} ({stats['pass']/total*100:.1f}%)\n")
            f.write(f"- **FAIL:** {stats['fail']} ({stats['fail']/total*100:.1f}%)\n")
            f.write(f"- **REWRITE:** {stats['rewrite']} ({stats['rewrite']/total*100:.1f}%)\n\n")
            
            # Score statistics
            all_scores = {
                'goldilocks': [r.goldilocks_score for r in results],
                'fidelity': [r.fidelity_score for r in results],
                'pedagogy': [r.pedagogy_score for r in results],
                'semantic': [r.semantic_score for r in results],
                'style': [r.style_score for r in results],
                'overall': [r.overall_score for r in results]
            }
            
            f.write("## Score Statistics\n\n")
            for criteria, scores in all_scores.items():
                avg_score = sum(scores) / len(scores)
                f.write(f"- **{criteria.title()} Average:** {avg_score:.1f}/100\n")
            
            f.write("\n## Most Common Failures\n\n")
            
            # Collect failure patterns
            all_failures = {}
            for result in results:
                for failure_list in [result.goldilocks_failures, result.fidelity_failures,
                                   result.pedagogy_failures, result.semantic_failures,
                                   result.style_failures]:
                    for failure in failure_list:
                        all_failures[failure] = all_failures.get(failure, 0) + 1
            
            # Sort by frequency
            sorted_failures = sorted(all_failures.items(), key=lambda x: x[1], reverse=True)[:10]
            
            for failure, count in sorted_failures:
                f.write(f"- **{failure}:** {count} exercises ({count/total*100:.1f}%)\n")
            
            f.write("\n## Exercise Type Analysis\n\n")
            type_stats = {}
            for result in results:
                ex_type = result.exercise_type
                if ex_type not in type_stats:
                    type_stats[ex_type] = {"pass": 0, "fail": 0, "rewrite": 0, "total": 0}
                type_stats[ex_type][result.category] += 1
                type_stats[ex_type]["total"] += 1
            
            for ex_type, stats in type_stats.items():
                if stats["total"] > 5:  # Only show types with significant counts
                    pass_rate = stats["pass"] / stats["total"] * 100
                    f.write(f"- **{ex_type}:** {pass_rate:.1f}% pass rate ({stats['pass']}/{stats['total']})\n")
            
            f.write(f"\n## Evaluation Completed\n\n")
            f.write(f"All {total} exercises have been evaluated and categorized.\n")
            f.write(f"Detailed logs available in logs/ directory organized by category.\n")
            f.write(f"Exercise files moved to appropriate pass/, fail/, or rewrite/ directories.\n")

def main():
    """Main execution function"""
    input_dir = "/Users/adi/code/socratify/socratify-yolo/input"
    output_dir = "/Users/adi/code/socratify/socratify-yolo"
    logs_dir = "/Users/adi/code/socratify/socratify-yolo/logs"
    
    evaluator = ComprehensiveEvaluator(input_dir, output_dir, logs_dir)
    results = evaluator.run_comprehensive_evaluation()
    
    print(f"\n=== EVALUATION COMPLETE ===")
    print(f"Total processed: {results['total_processed']}")
    print(f"Pass: {results['statistics']['pass']}")
    print(f"Fail: {results['statistics']['fail']}")
    print(f"Rewrite: {results['statistics']['rewrite']}")
    print(f"\nDetailed logs and categorized exercises available in respective directories.")

if __name__ == "__main__":
    main()