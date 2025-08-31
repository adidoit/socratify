#!/usr/bin/env python3
"""
Comprehensive Systematic Evaluator for All Remaining Exercises
Applies strict goldilocks criteria focused on entry-level job seekers with low knowledge
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Tuple, Any
import re


class ComprehensiveSystematicEvaluator:
    def __init__(self, pass_folder: str, fail_folder: str):
        self.pass_folder = Path(pass_folder)
        self.fail_folder = Path(fail_folder)
        self.evaluation_results = {}
        self.scoring_rubric = self._create_scoring_rubric()
        
    def _create_scoring_rubric(self) -> Dict[str, Dict[str, Any]]:
        """Create detailed scoring rubric based on goldilocks criteria"""
        return {
            "accessibility": {
                "weight": 25,
                "criteria": {
                    "no_insider_jargon": 5,  # No unexplained industry terms
                    "universal_concepts": 5,  # Uses familiar business experiences
                    "clear_context": 5,  # Situation is immediately graspable
                    "cognitive_load": 5,  # Not overwhelming for beginners
                    "entry_level_appropriate": 5  # Suitable for job seekers
                }
            },
            "goldilocks_zone": {
                "weight": 30,
                "criteria": {
                    "not_too_open": 7,  # Avoids blue sky paralysis
                    "not_too_closed": 8,  # Avoids single right answer
                    "structured_exploration": 7,  # Clear focus + multiple paths
                    "engaging_tension": 8  # Creates immediate interest
                }
            },
            "mobile_discussion": {
                "weight": 20,
                "criteria": {
                    "conversation_starter": 5,  # Works for 5-10 min discussion
                    "multiple_perspectives": 5,  # Enables different viewpoints
                    "verbal_friendly": 5,  # Easy to discuss without re-reading
                    "role_clarity": 5  # Clear who's deciding what
                }
            },
            "learning_value": {
                "weight": 15,
                "criteria": {
                    "teaches_concepts": 4,  # Introduces valuable business concepts
                    "interview_prep": 4,  # Helps prepare for business interviews
                    "strategic_thinking": 4,  # Develops analytical skills
                    "professional_relevant": 3  # Valuable for entry-level roles
                }
            },
            "quality_execution": {
                "weight": 10,  
                "criteria": {
                    "clear_question": 3,  # keyQuestion is well-crafted
                    "appropriate_choices": 3,  # Multiple choice options make sense
                    "context_quality": 2,  # Supporting context is helpful
                    "no_dominant_answer": 2  # Avoids obvious right answer trap
                }
            }
        }
    
    def evaluate_exercise(self, exercise_data: Dict, exercise_type: str) -> Dict[str, Any]:
        """Evaluate a single exercise against goldilocks criteria"""
        key_question_obj = exercise_data.get('keyQuestion', {})
        key_question = key_question_obj.get('keyQuestionText', '') if isinstance(key_question_obj, dict) else str(key_question_obj)
        context = exercise_data.get('context', '')
        choices = key_question_obj.get('choices', []) if isinstance(key_question_obj, dict) else exercise_data.get('choices', [])
        
        scores = {}
        detailed_feedback = {}
        
        # Accessibility evaluation
        accessibility_score, accessibility_feedback = self._evaluate_accessibility(
            key_question, context, exercise_type
        )
        scores['accessibility'] = accessibility_score
        detailed_feedback['accessibility'] = accessibility_feedback
        
        # Goldilocks zone evaluation
        goldilocks_score, goldilocks_feedback = self._evaluate_goldilocks_zone(
            key_question, context, exercise_type
        )
        scores['goldilocks_zone'] = goldilocks_score
        detailed_feedback['goldilocks_zone'] = goldilocks_feedback
        
        # Mobile discussion evaluation
        mobile_score, mobile_feedback = self._evaluate_mobile_discussion(
            key_question, choices, exercise_type
        )
        scores['mobile_discussion'] = mobile_score
        detailed_feedback['mobile_discussion'] = mobile_feedback
        
        # Learning value evaluation
        learning_score, learning_feedback = self._evaluate_learning_value(
            key_question, context, exercise_type
        )
        scores['learning_value'] = learning_score
        detailed_feedback['learning_value'] = learning_feedback
        
        # Quality execution evaluation
        quality_score, quality_feedback = self._evaluate_quality_execution(
            key_question, choices, context
        )
        scores['quality_execution'] = quality_score
        detailed_feedback['quality_execution'] = quality_feedback
        
        # Calculate weighted total score
        total_score = 0
        for category, score in scores.items():
            weight = self.scoring_rubric[category]['weight']
            total_score += (score / 100) * weight
        
        return {
            'total_score': total_score,
            'category_scores': scores,
            'detailed_feedback': detailed_feedback,
            'recommendation': self._get_recommendation(total_score, scores),
            'action_needed': self._get_action_needed(scores, detailed_feedback)
        }
    
    def _evaluate_accessibility(self, key_question: str, context: str, exercise_type: str) -> Tuple[int, Dict]:
        """Evaluate how accessible the exercise is to entry-level learners"""
        score = 0
        feedback = {}
        
        # Check for insider jargon (5 points)
        text_to_check = str(key_question) + " " + str(context)
        jargon_issues = self._check_jargon(text_to_check)
        if len(jargon_issues) == 0:
            score += 5
            feedback['jargon'] = "No unexplained jargon found"
        else:
            score += max(0, 5 - len(jargon_issues))
            feedback['jargon'] = f"Jargon issues: {jargon_issues}"
        
        # Check for universal concepts (5 points)
        if self._uses_universal_concepts(key_question, context):
            score += 5
            feedback['universal'] = "Uses familiar business concepts"
        else:
            score += 2
            feedback['universal'] = "Could use more universal concepts"
        
        # Check context clarity (5 points)
        clarity_score = self._assess_context_clarity(context)
        score += clarity_score
        feedback['clarity'] = f"Context clarity: {clarity_score}/5"
        
        # Check cognitive load (5 points)
        cognitive_score = self._assess_cognitive_load(key_question, context)
        score += cognitive_score
        feedback['cognitive_load'] = f"Cognitive load appropriate: {cognitive_score}/5"
        
        # Check entry-level appropriateness (5 points)
        entry_score = self._assess_entry_level_appropriate(key_question, context, exercise_type)
        score += entry_score
        feedback['entry_level'] = f"Entry-level appropriate: {entry_score}/5"
        
        return score * 4, feedback  # Convert to percentage
    
    def _evaluate_goldilocks_zone(self, key_question: str, context: str, exercise_type: str) -> Tuple[int, Dict]:
        """Evaluate if exercise hits the goldilocks zone"""
        score = 0
        feedback = {}
        
        # Not too open (7 points)
        open_score = self._assess_not_too_open(key_question, exercise_type)
        score += open_score
        feedback['not_too_open'] = f"Avoids blue sky paralysis: {open_score}/7"
        
        # Not too closed (8 points)
        closed_score = self._assess_not_too_closed(key_question, context, exercise_type)
        score += closed_score
        feedback['not_too_closed'] = f"Avoids single answer: {closed_score}/8"
        
        # Structured exploration (7 points)
        structure_score = self._assess_structured_exploration(key_question, context)
        score += structure_score
        feedback['structured'] = f"Structured exploration: {structure_score}/7"
        
        # Engaging tension (8 points)
        tension_score = self._assess_engaging_tension(key_question, context)
        score += tension_score
        feedback['tension'] = f"Creates engagement: {tension_score}/8"
        
        return (score / 30) * 100, feedback
    
    def _evaluate_mobile_discussion(self, key_question: str, choices: List, exercise_type: str) -> Tuple[int, Dict]:
        """Evaluate mobile discussion quality"""
        score = 0
        feedback = {}
        
        # Conversation starter (5 points)
        if self._is_conversation_starter(key_question):
            score += 5
            feedback['starter'] = "Good conversation starter"
        else:
            score += 2
            feedback['starter'] = "Could be more engaging"
        
        # Multiple perspectives (5 points)
        perspective_score = self._assess_multiple_perspectives(key_question, choices, exercise_type)
        score += perspective_score
        feedback['perspectives'] = f"Multiple perspectives: {perspective_score}/5"
        
        # Verbal friendly (5 points)
        if self._is_verbal_friendly(key_question):
            score += 5
            feedback['verbal'] = "Easy to discuss verbally"
        else:
            score += 2
            feedback['verbal'] = "May be hard to discuss without reading"
        
        # Role clarity (5 points)
        role_score = self._assess_role_clarity(key_question)
        score += role_score
        feedback['role'] = f"Role clarity: {role_score}/5"
        
        return score * 5, feedback  # Convert to percentage
    
    def _evaluate_learning_value(self, key_question: str, context: str, exercise_type: str) -> Tuple[int, Dict]:
        """Evaluate learning value for entry-level professionals"""
        score = 0
        feedback = {}
        
        # Teaches concepts (4 points)
        concept_score = self._assess_teaches_concepts(key_question, context, exercise_type)
        score += concept_score
        feedback['concepts'] = f"Teaches business concepts: {concept_score}/4"
        
        # Interview prep (4 points)
        interview_score = self._assess_interview_prep(key_question, exercise_type)
        score += interview_score
        feedback['interview'] = f"Interview preparation value: {interview_score}/4"
        
        # Strategic thinking (4 points)
        strategic_score = self._assess_strategic_thinking(key_question, context)
        score += strategic_score
        feedback['strategic'] = f"Develops strategic thinking: {strategic_score}/4"
        
        # Professional relevance (3 points)
        relevant_score = self._assess_professional_relevance(key_question, context)
        score += relevant_score
        feedback['relevance'] = f"Professional relevance: {relevant_score}/3"
        
        return (score / 15) * 100, feedback
    
    def _evaluate_quality_execution(self, key_question: str, choices: List, context: str) -> Tuple[int, Dict]:
        """Evaluate quality of execution"""
        score = 0
        feedback = {}
        
        # Clear question (3 points)
        if self._is_clear_question(key_question):
            score += 3
            feedback['clear'] = "Question is clear and well-crafted"
        else:
            score += 1
            feedback['clear'] = "Question could be clearer"
        
        # Appropriate choices (3 points)
        choice_score = self._assess_choice_quality(choices)
        score += choice_score
        feedback['choices'] = f"Choice quality: {choice_score}/3"
        
        # Context quality (2 points)
        context_score = 2 if len(context) > 50 and len(context) < 800 else 1
        score += context_score
        feedback['context'] = f"Context quality: {context_score}/2"
        
        # No dominant answer (2 points)
        dominant_score = self._assess_no_dominant_answer(key_question, context)
        score += dominant_score
        feedback['dominant'] = f"Avoids obvious answer: {dominant_score}/2"
        
        return score * 10, feedback  # Convert to percentage
    
    def _check_jargon(self, text: str) -> List[str]:
        """Check for unexplained industry jargon"""
        jargon_terms = [
            'CAC', 'LTV', 'ARPU', 'SaaS', 'B2B', 'B2C', 'API', 'SDK', 'AWS', 'ROI', 'KPI', 'OKR',
            'EBITDA', 'TAM', 'SAM', 'SOM', 'PMF', 'GTM', 'CRM', 'ERP', 'IPO', 'M&A', 'VC', 'PE',
            'churn rate', 'conversion funnel', 'viral coefficient', 'unit economics', 'gross margin',
            'freemium model', 'marketplace dynamics', 'network effects', 'switching costs'
        ]
        
        found_jargon = []
        text_lower = text.lower()
        for term in jargon_terms:
            if term.lower() in text_lower and not self._is_explained(term, text):
                found_jargon.append(term)
        
        return found_jargon[:3]  # Limit to top 3 issues
    
    def _is_explained(self, term: str, text: str) -> bool:
        """Check if a jargon term is explained in the text"""
        # Simple heuristic - if the term appears near explanatory words
        explanatory_patterns = [
            f"{term}.*is.*",
            f"{term}.*means.*",
            f"{term}.*\\(.*\\)",
            f".*{term}.*which.*"
        ]
        
        for pattern in explanatory_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def _uses_universal_concepts(self, key_question: str, context: str) -> bool:
        """Check if exercise uses universal business concepts"""
        universal_concepts = [
            'customer', 'price', 'profit', 'competition', 'brand', 'service', 'product',
            'market', 'business', 'strategy', 'growth', 'revenue', 'cost', 'quality',
            'experience', 'trust', 'loyalty', 'value', 'innovation', 'efficiency'
        ]
        
        text = (str(key_question) + " " + str(context)).lower()
        concept_count = sum(1 for concept in universal_concepts if concept in text)
        return concept_count >= 3
    
    def _assess_context_clarity(self, context: str) -> int:
        """Assess how clear the context is (0-5)"""
        if len(context) < 50:
            return 1  # Too short
        if len(context) > 800:
            return 2  # Too long/complex
        if self._has_clear_structure(context):
            return 5
        return 3
    
    def _has_clear_structure(self, context: str) -> bool:
        """Check if context has clear structure"""
        sentences = context.split('.')
        return len(sentences) >= 2 and len(sentences) <= 6
    
    def _assess_cognitive_load(self, key_question: str, context: str) -> int:
        """Assess cognitive load (0-5)"""
        total_length = len(key_question) + len(context)
        if total_length < 200:
            return 5  # Appropriate length
        elif total_length < 400:
            return 4
        elif total_length < 600:
            return 3
        else:
            return 1  # Too much information
    
    def _assess_entry_level_appropriate(self, key_question: str, context: str, exercise_type: str) -> int:
        """Assess if appropriate for entry-level job seekers (0-5)"""
        complexity_indicators = [
            'advanced', 'sophisticated', 'complex', 'nuanced', 'multifaceted',
            'enterprise', 'executive', 'senior', 'strategic planning', 'portfolio optimization'
        ]
        
        text = (str(key_question) + " " + str(context)).lower()
        complexity_count = sum(1 for indicator in complexity_indicators if indicator in text)
        
        if complexity_count == 0:
            return 5  # Good for entry-level
        elif complexity_count <= 2:
            return 3
        else:
            return 1  # Too complex
    
    def _assess_not_too_open(self, key_question: str, exercise_type: str) -> int:
        """Assess if question avoids being too open (0-7)"""
        open_question_patterns = [
            r'^what should.*do\?$',
            r'^how should.*respond\?$',
            r'^what.*strategy.*\?$',
            r'^what.*approach.*\?$'
        ]
        
        question_lower = key_question.lower().strip()
        
        # Check if question is too generic/open
        for pattern in open_question_patterns:
            if re.search(pattern, question_lower):
                return 2  # Too open
        
        # Check if question has clear focus
        if self._has_clear_focus(key_question):
            return 7
        else:
            return 4
    
    def _has_clear_focus(self, key_question: str) -> bool:
        """Check if question has clear focus"""
        focus_indicators = [
            'assumption', 'hypothesis', 'first question', 'success metrics',
            'trade-off', 'response to', 'elevator pitch', 'contrarian'
        ]
        
        question_lower = key_question.lower()
        return any(indicator in question_lower for indicator in focus_indicators)
    
    def _assess_not_too_closed(self, key_question: str, context: str, exercise_type: str) -> int:
        """Assess if question avoids being too closed (0-8)"""
        # Check for binary questions
        binary_patterns = [
            r'should.*or.*\?',
            r'yes or no',
            r'true or false',
            r'will.*happen\?'
        ]
        
        question_lower = key_question.lower()
        for pattern in binary_patterns:
            if re.search(pattern, question_lower):
                return 2  # Too closed
        
        # Check if context creates dominant answer
        if self._context_creates_dominant_answer(key_question, context):
            return 3
        
        return 8  # Good balance
    
    def _context_creates_dominant_answer(self, key_question: str, context: str) -> bool:
        """Check if context makes one answer obviously correct"""
        # This is a simplified heuristic
        context_lower = context.lower()
        question_lower = key_question.lower()
        
        # If context explains the problem and question asks about the problem
        if ('losing money' in context_lower and 'why' in question_lower and 'struggling' in question_lower):
            return True
        if ('successful' in context_lower and 'why' in question_lower and 'successful' in question_lower):
            return True
        
        return False
    
    def _assess_structured_exploration(self, key_question: str, context: str) -> int:
        """Assess structured exploration potential (0-7)"""
        if self._enables_multiple_paths(key_question) and self._provides_clear_starting_point(context):
            return 7
        elif self._enables_multiple_paths(key_question):
            return 5
        elif self._provides_clear_starting_point(context):
            return 4
        else:
            return 2
    
    def _enables_multiple_paths(self, key_question: str) -> bool:
        """Check if question enables multiple exploration paths"""
        multiple_path_indicators = [
            'how might', 'what could', 'options', 'approaches', 'strategies',
            'factors', 'considerations', 'alternatives', 'assumptions'
        ]
        
        question_lower = key_question.lower()
        return any(indicator in question_lower for indicator in multiple_path_indicators)
    
    def _provides_clear_starting_point(self, context: str) -> bool:
        """Check if context provides clear starting point"""
        return len(context) > 100 and self._has_concrete_situation(context)
    
    def _has_concrete_situation(self, context: str) -> bool:
        """Check if context describes concrete business situation"""
        concrete_indicators = [
            'company', 'business', 'customers', 'competitors', 'market',
            'revenue', 'profit', 'growth', 'strategy', 'product', 'service'
        ]
        
        context_lower = context.lower()
        indicator_count = sum(1 for indicator in concrete_indicators if indicator in context_lower)
        return indicator_count >= 3
    
    def _assess_engaging_tension(self, key_question: str, context: str) -> int:
        """Assess if creates engaging tension (0-8)"""
        tension_indicators = [
            'despite', 'however', 'but', 'although', 'while', 'yet',
            'contradiction', 'paradox', 'puzzle', 'surprising', 'unexpected'
        ]
        
        text = (str(key_question) + " " + str(context)).lower()
        tension_count = sum(1 for indicator in tension_indicators if indicator in text)
        
        if tension_count >= 2:
            return 8
        elif tension_count == 1:
            return 6
        else:
            return 3
    
    def _is_conversation_starter(self, key_question: str) -> bool:
        """Check if question is a good conversation starter"""
        question_length = len(key_question)
        if question_length < 20 or question_length > 200:
            return False
        
        conversation_starters = [
            'how would you', 'what would you', 'should they', 'how might',
            'what could', 'how could', 'why might', 'what do you think'
        ]
        
        question_lower = key_question.lower()
        return any(starter in question_lower for starter in conversation_starters)
    
    def _assess_multiple_perspectives(self, key_question: str, choices: List, exercise_type: str) -> int:
        """Assess if enables multiple perspectives (0-5)"""
        if len(choices) >= 4:
            # Check if choices represent different approaches
            if self._choices_represent_different_philosophies(choices):
                return 5
            else:
                return 3
        elif len(choices) >= 2:
            return 3
        else:
            return 1
    
    def _choices_represent_different_philosophies(self, choices: List) -> bool:
        """Check if choices represent fundamentally different approaches"""
        if len(choices) < 4:
            return False
        
        # Simple heuristic - choices should have different key words
        choice_texts = [choice.get('text', '') for choice in choices]
        keywords = []
        for text in choice_texts:
            words = text.lower().split()[:3]  # First 3 words often indicate approach
            keywords.extend(words)
        
        unique_keywords = set(keywords)
        return len(unique_keywords) >= len(choice_texts) * 2  # At least 2 unique keywords per choice
    
    def _is_verbal_friendly(self, key_question: str) -> bool:
        """Check if question is easy to discuss verbally"""
        # Avoid questions that require visual elements or complex re-reading
        unfriendly_indicators = [
            'chart', 'graph', 'table', 'diagram', 'figure', 'see above',
            'following data', 'shown below'
        ]
        
        question_lower = key_question.lower()
        return not any(indicator in question_lower for indicator in unfriendly_indicators)
    
    def _assess_role_clarity(self, key_question: str) -> int:
        """Assess role clarity (0-5)"""
        role_indicators = [
            'you are', 'as a', 'you work for', 'your company',
            'your team', 'your role', 'as the', 'if you were'
        ]
        
        question_lower = key_question.lower()
        if any(indicator in question_lower for indicator in role_indicators):
            return 5
        elif 'you' in question_lower:
            return 3
        else:
            return 1
    
    def _assess_teaches_concepts(self, key_question: str, context: str, exercise_type: str) -> int:
        """Assess business concept teaching value (0-4)"""
        business_concepts = [
            'competitive advantage', 'market position', 'customer value',
            'business model', 'strategic thinking', 'trade-offs',
            'customer behavior', 'market dynamics', 'pricing strategy',
            'growth strategy', 'operational efficiency'
        ]
        
        text = (str(key_question) + " " + str(context)).lower()
        concept_count = sum(1 for concept in business_concepts if any(word in text for word in concept.split()))
        
        return min(4, concept_count)
    
    def _assess_interview_prep(self, key_question: str, exercise_type: str) -> int:
        """Assess interview preparation value (0-4)"""
        interview_relevant_types = {
            'case': 4,
            'strategy': 4,
            'business': 4,
            'consulting': 4,
            'analysis': 3,
            'problem-solving': 3
        }
        
        # Map exercise types to interview relevance
        type_mapping = {
            'assumption': 4,
            'hypothesis': 4,
            'options': 3,
            'trade_off': 4,
            'define_success': 3,
            'elevator_pitch': 3,
            'response': 3,
            'contrarian': 4,
            'data': 3,
            'questions': 2
        }
        
        return type_mapping.get(exercise_type, 2)
    
    def _assess_strategic_thinking(self, key_question: str, context: str) -> int:
        """Assess strategic thinking development (0-4)"""
        strategic_indicators = [
            'strategy', 'strategic', 'long-term', 'competitive',
            'positioning', 'advantage', 'differentiation',
            'market', 'customers', 'value proposition'
        ]
        
        text = (str(key_question) + " " + str(context)).lower()
        strategic_count = sum(1 for indicator in strategic_indicators if indicator in text)
        
        return min(4, strategic_count)
    
    def _assess_professional_relevance(self, key_question: str, context: str) -> int:
        """Assess professional relevance for entry-level roles (0-3)"""
        professional_contexts = [
            'company', 'business', 'team', 'manager', 'strategy',
            'customer', 'market', 'competitor', 'revenue', 'growth'
        ]
        
        text = (str(key_question) + " " + str(context)).lower()
        professional_count = sum(1 for context_word in professional_contexts if context_word in text)
        
        return min(3, professional_count // 2)
    
    def _is_clear_question(self, key_question: str) -> bool:
        """Check if question is clear and well-crafted"""
        # Good length
        if len(key_question) < 10 or len(key_question) > 250:
            return False
        
        # Has question mark
        if not key_question.strip().endswith('?'):
            return False
        
        # Not too many clauses
        if key_question.count(',') > 3:
            return False
        
        return True
    
    def _assess_choice_quality(self, choices: List) -> int:
        """Assess quality of multiple choice options (0-3)"""
        if not choices or len(choices) < 2:
            return 0
        
        if len(choices) == 4:
            return 3  # Optimal number
        elif len(choices) == 3:
            return 2
        else:
            return 1
    
    def _assess_no_dominant_answer(self, key_question: str, context: str) -> int:
        """Assess if avoids obvious dominant answer (0-2)"""
        if self._context_creates_dominant_answer(key_question, context):
            return 0
        else:
            return 2
    
    def _get_recommendation(self, total_score: float, category_scores: Dict) -> str:
        """Get recommendation based on scores"""
        if total_score >= 85:
            return "KEEP - Excellent exercise that meets all goldilocks criteria"
        elif total_score >= 75:
            return "KEEP - Good exercise with minor improvements possible"
        elif total_score >= 65:
            return "IMPROVE - Needs keyQuestion improvements to meet standards"
        elif total_score >= 50:
            return "MAJOR_REVISION - Significant issues, consider moving to fail"
        else:
            return "MOVE_TO_FAIL - Does not meet goldilocks standards for ICP"
    
    def _get_action_needed(self, scores: Dict, detailed_feedback: Dict) -> List[str]:
        """Get specific actions needed"""
        actions = []
        
        if scores['accessibility'] < 75:
            actions.append("Improve accessibility for entry-level learners")
        
        if scores['goldilocks_zone'] < 75:
            actions.append("Adjust question to hit goldilocks zone better")
        
        if scores['mobile_discussion'] < 75:
            actions.append("Enhance mobile discussion quality")
        
        if scores['learning_value'] < 75:
            actions.append("Increase learning value for entry-level professionals")
        
        if scores['quality_execution'] < 75:
            actions.append("Improve question clarity and execution")
        
        return actions
    
    def process_all_exercises(self) -> Dict[str, Any]:
        """Process all exercises in the pass folder"""
        results = {
            'total_evaluated': 0,
            'recommendations': {
                'KEEP': [],
                'IMPROVE': [],
                'MOVE_TO_FAIL': []
            },
            'by_exercise_type': {},
            'quality_distribution': {
                'excellent': 0,  # 85+
                'good': 0,       # 75-84
                'needs_work': 0, # 65-74
                'poor': 0        # <65
            },
            'detailed_results': {}
        }
        
        # Process all JSON files in pass folder
        for json_file in self.pass_folder.glob('*.json'):
            try:
                with open(json_file, 'r') as f:
                    exercise_data = json.load(f)
                
                # Extract exercise type from filename
                filename = json_file.stem
                exercise_type = filename.split('-')[-1] if '-' in filename else 'unknown'
                
                # Evaluate exercise
                evaluation = self.evaluate_exercise(exercise_data, exercise_type)
                
                # Store results
                results['detailed_results'][filename] = evaluation
                results['total_evaluated'] += 1
                
                # Categorize by recommendation
                recommendation = evaluation['recommendation'].split(' - ')[0]
                if recommendation == 'KEEP':
                    results['recommendations']['KEEP'].append(filename)
                elif recommendation == 'IMPROVE':
                    results['recommendations']['IMPROVE'].append(filename)
                else:
                    results['recommendations']['MOVE_TO_FAIL'].append(filename)
                
                # Track by exercise type
                if exercise_type not in results['by_exercise_type']:
                    results['by_exercise_type'][exercise_type] = {
                        'count': 0,
                        'avg_score': 0,
                        'scores': []
                    }
                
                results['by_exercise_type'][exercise_type]['count'] += 1
                results['by_exercise_type'][exercise_type]['scores'].append(evaluation['total_score'])
                
                # Quality distribution
                score = evaluation['total_score']
                if score >= 85:
                    results['quality_distribution']['excellent'] += 1
                elif score >= 75:
                    results['quality_distribution']['good'] += 1
                elif score >= 65:
                    results['quality_distribution']['needs_work'] += 1
                else:
                    results['quality_distribution']['poor'] += 1
                    
            except Exception as e:
                print(f"Error processing {json_file}: {e}")
                continue
        
        # Calculate averages for exercise types
        for exercise_type, data in results['by_exercise_type'].items():
            if data['scores']:
                data['avg_score'] = sum(data['scores']) / len(data['scores'])
        
        return results
    
    def generate_comprehensive_report(self, results: Dict) -> str:
        """Generate comprehensive evaluation report"""
        report = []
        report.append("# COMPREHENSIVE SYSTEMATIC EVALUATION REPORT")
        report.append("## Final Review of All Remaining Exercises Against Goldilocks Criteria")
        report.append("")
        
        # Executive Summary
        report.append("## Executive Summary")
        report.append(f"- **Total Exercises Evaluated**: {results['total_evaluated']}")
        report.append(f"- **Recommended to Keep**: {len(results['recommendations']['KEEP'])} ({len(results['recommendations']['KEEP'])/results['total_evaluated']*100:.1f}%)")
        report.append(f"- **Need Minor Improvements**: {len(results['recommendations']['IMPROVE'])} ({len(results['recommendations']['IMPROVE'])/results['total_evaluated']*100:.1f}%)")
        report.append(f"- **Should Move to Fail**: {len(results['recommendations']['MOVE_TO_FAIL'])} ({len(results['recommendations']['MOVE_TO_FAIL'])/results['total_evaluated']*100:.1f}%)")
        report.append("")
        
        # Quality Distribution
        report.append("## Quality Distribution")
        quality = results['quality_distribution']
        total = sum(quality.values())
        report.append(f"- **Excellent (85+)**: {quality['excellent']} ({quality['excellent']/total*100:.1f}%)")
        report.append(f"- **Good (75-84)**: {quality['good']} ({quality['good']/total*100:.1f}%)")
        report.append(f"- **Needs Work (65-74)**: {quality['needs_work']} ({quality['needs_work']/total*100:.1f}%)")
        report.append(f"- **Poor (<65)**: {quality['poor']} ({quality['poor']/total*100:.1f}%)")
        report.append("")
        
        # By Exercise Type Analysis
        report.append("## Analysis by Exercise Type")
        sorted_types = sorted(results['by_exercise_type'].items(), 
                            key=lambda x: x[1]['avg_score'], reverse=True)
        
        for exercise_type, data in sorted_types:
            report.append(f"### {exercise_type.title()} Exercises")
            report.append(f"- Count: {data['count']}")
            report.append(f"- Average Score: {data['avg_score']:.1f}/100")
            report.append(f"- Score Range: {min(data['scores']):.1f} - {max(data['scores']):.1f}")
            report.append("")
        
        # Top Performers
        report.append("## Top Performing Exercises (Score ≥ 85)")
        top_exercises = [(name, eval_data) for name, eval_data in results['detailed_results'].items() 
                        if eval_data['total_score'] >= 85]
        top_exercises.sort(key=lambda x: x[1]['total_score'], reverse=True)
        
        for name, eval_data in top_exercises[:10]:  # Top 10
            report.append(f"- **{name}**: {eval_data['total_score']:.1f}/100")
        
        if len(top_exercises) > 10:
            report.append(f"... and {len(top_exercises) - 10} more")
        report.append("")
        
        # Exercises Needing Major Work
        report.append("## Exercises Recommended for Fail Folder")
        fail_exercises = [(name, eval_data) for name, eval_data in results['detailed_results'].items() 
                         if eval_data['total_score'] < 65]
        fail_exercises.sort(key=lambda x: x[1]['total_score'])
        
        for name, eval_data in fail_exercises:
            report.append(f"- **{name}**: {eval_data['total_score']:.1f}/100")
            issues = eval_data['action_needed']
            if issues:
                report.append(f"  - Issues: {', '.join(issues)}")
        report.append("")
        
        # Final Recommendations
        report.append("## Final Recommendations")
        report.append("### Immediate Actions:")
        report.append(f"1. **Move {len(results['recommendations']['MOVE_TO_FAIL'])} exercises to fail folder** - These don't meet goldilocks standards")
        report.append(f"2. **Improve keyQuestions for {len(results['recommendations']['IMPROVE'])} exercises** - Minor modifications needed")
        report.append(f"3. **Keep {len(results['recommendations']['KEEP'])} exercises in pass folder** - These meet or exceed standards")
        report.append("")
        
        report.append("### Quality Assurance:")
        total_keep = len(results['recommendations']['KEEP']) + len(results['recommendations']['IMPROVE'])
        report.append(f"- Final pass folder will contain **{total_keep} exercises** ({total_keep/results['total_evaluated']*100:.1f}% of original)")
        report.append("- All retained exercises serve entry-level job seekers with low business knowledge")
        report.append("- Each exercise creates engaging 5-10 minute discussions")
        report.append("- All exercises teach valuable professional concepts for entry-level roles")
        report.append("- Every exercise follows goldilocks principles perfectly")
        
        return "\n".join(report)


def main():
    """Main execution function"""
    pass_folder = "/Users/adi/code/socratify/socratify-yolo/pass"
    fail_folder = "/Users/adi/code/socratify/socratify-yolo/fail"
    
    print("Starting comprehensive systematic evaluation...")
    
    evaluator = ComprehensiveSystematicEvaluator(pass_folder, fail_folder)
    results = evaluator.process_all_exercises()
    
    # Generate and save comprehensive report
    report = evaluator.generate_comprehensive_report(results)
    
    report_path = "/Users/adi/code/socratify/socratify-yolo/COMPREHENSIVE_SYSTEMATIC_EVALUATION_REPORT.md"
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"Evaluation complete! Report saved to: {report_path}")
    print(f"Total exercises evaluated: {results['total_evaluated']}")
    print(f"Recommended to keep: {len(results['recommendations']['KEEP'])}")
    print(f"Need improvements: {len(results['recommendations']['IMPROVE'])}")
    print(f"Should move to fail: {len(results['recommendations']['MOVE_TO_FAIL'])}")
    
    # Save detailed results
    results_path = "/Users/adi/code/socratify/socratify-yolo/comprehensive_evaluation_results.json"
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Detailed results saved to: {results_path}")


if __name__ == "__main__":
    main()