# Language & Style Evaluator

This evaluator assesses the language quality, formatting, and accessibility of Socratify exercises to ensure clear, accessible communication for first-year business students.

## Core Purpose

Socratify exercises must use language that:
- Is accessible to first-year business students with no specialized knowledge
- Works effectively in 2-minute verbal mobile conversations
- Follows clear writing principles that eliminate confusion and cognitive burden
- Uses proper formatting and structure for mobile learning

This evaluator checks language quality, sentence structure, accessibility, and formatting compliance.

## Evaluation Principles

### **Language Accessibility**
- Write for first-year business students with no specialized knowledge
- Use simple, universal vocabulary that translates across cultures
- Replace jargon with clear, concrete language
- Define any technical terms immediately when first used

### **Sentence Clarity** 
- Use active voice and clear subject-verb-object structure
- Keep sentences focused on one main idea
- Make connections between ideas explicit
- Avoid complex grammatical constructions

### **Content Efficiency**
- Every word must serve a clear purpose
- Cut filler phrases, redundancies, and unnecessary qualifiers
- Front-load important information
- Use specific examples instead of abstract concepts

### **Mobile Optimization**
- Language must work in 2-minute verbal conversations
- Avoid tongue twisters and awkward word combinations
- Use natural speech rhythms and conversational flow
- Test readability when spoken aloud

## Language Quality Standards

### **Jargon Elimination**
Replace business jargon with clear, accessible language:
- "leverage" → "use"
- "optimize" → "improve" 
- "strategic" → delete or replace with specific action
- "ecosystem" → "network" or specific description
- "infrastructure" → specific systems/tools mentioned

### **Concrete Language**
Use specific examples instead of abstract concepts:
- Bad: "market disruption occurred"
- Good: "Netflix killed Blockbuster"
- Bad: "significant growth"
- Good: "revenue jumped 40% to $2B"

### **Clear Pronouns**
Avoid vague pronouns without clear antecedents:
- Bad: "Tesla launched insurance. This could change everything."
- Good: "Tesla launched insurance. This move into financial services could change everything."

### **Active Voice**
Use clear subject-verb-object structure:
- Bad: "A decision was made by Amazon to acquire Whole Foods"
- Good: "Amazon decided to acquire Whole Foods"

### **Filler Phrase Elimination**
Cut meaningless phrases that add no information:
- "it's worth noting that" → delete
- "at the end of the day" → delete
- "the key insight is" → delete
- "it goes without saying" → delete
- "for all intents and purposes" → delete

### **Strong Verbs**
Use energetic, specific verbs:
- "increased rapidly" → "soared" or "jumped"
- "decreased significantly" → "plummeted" or "crashed"
- "moved quickly" → "raced" or "sprinted"  
- "went up" → "climbed" or "surged"

### **Zombie Noun Elimination**
Avoid turning verbs into nouns - use active language instead:
- "make a decision" → "decide"
- "conduct an analysis" → "analyze"
- "perform an evaluation" → "evaluate"
- "give consideration to" → "consider"
- "make an acquisition" → "acquire"
- "provide assistance" → "assist"
- "reach a conclusion" → "conclude"

### **Predictable Combination Avoidance**
Never use clichéd business phrases - use specifics instead:
- "significant growth" → use actual numbers ("grew from $10M to $50M")
- "operational efficiency" → describe improvements ("delivers in 1 day instead of 3")
- "strategic initiative" → name specific action ("launched insurance division")
- "enhanced experience" → show changes ("checkout takes 2 clicks instead of 10")
- "positive outcomes" → state actual results ("cut costs by 30%")

### **Right-Branching Structure**
Put main clause first, then add details:
- Good: "Tesla launched insurance to capture customer revenue throughout ownership"
- Bad: "To capture customer revenue that traditionally went to third parties, Tesla launched insurance"

### **Agency Clarity**
Make WHO does WHAT crystal clear - put real decision-maker as subject:
- Good: "Trader Joe's bans screens from all 540 stores"
- Bad: "48 states refuse all screens in stores" (states don't make retail decisions)

### **Number Contextualization**  
Raw numbers mean nothing without comparison:
- Bad: "The company spent $50 million on R&D"
- Good: "The company spent 10% of revenue on R&D"

## Validation Framework

### 1. LANGUAGE ACCESSIBILITY
**Question**: Is the language accessible to first-year business students?

**Jargon Elimination:**
- [ ] **No Business Jargon**: "leverage" → "use", "optimize" → "improve", "strategic" → deleted
- [ ] **Simple Word Choices**: "buy" not "purchase", "about" not "approximately"  
- [ ] **No Complex Vocabulary**: Uses words accessible to non-native English speakers
- [ ] **Technical Terms Defined**: Any necessary technical terms explained immediately

**Accessibility for Global Audience:**
- [ ] **Universal Vocabulary**: Words that translate easily across cultures
- [ ] **No Cultural Idioms**: Avoids expressions that don't translate
- [ ] **Simple Grammar**: Sentence structures accessible to non-native speakers

### 2. SENTENCE STRUCTURE & CLARITY
**Question**: Are sentences clear and well-structured?

**Active Voice & Structure:**
- [ ] **Active Voice Used**: "Tesla launched insurance" not "Insurance was launched"
- [ ] **Clear Subject-Verb-Object**: WHO does WHAT is immediately obvious
- [ ] **One Idea Per Sentence**: No cramming multiple concepts together
- [ ] **Complete Sentences**: No fragments without subject and verb

**Sentence Flow:**
- [ ] **Right-Branching**: Main clause first, details second
- [ ] **Clear Transitions**: Logical connections between adjacent sentences
- [ ] **Explicit Connections**: No forcing readers to infer relationships
- [ ] **Given-New Contract**: Start with familiar info, end with new info
- [ ] **Topic Chains**: Same subject across related sentences when discussing one topic

### 3. CONTENT EFFICIENCY
**Question**: Does every word serve a clear purpose?

**Filler Elimination:**
- [ ] **No Filler Phrases**: Cut "it's worth noting", "at the end of the day"
- [ ] **No Weak Intensifiers**: Remove "very", "really", "extremely"
- [ ] **No Redundant Words**: "future plans" → "plans"
- [ ] **No Unnecessary Qualifiers**: "vital importance" → "importance"

**Content Focus:**
- [ ] **Front-Loaded Information**: Most important details first  
- [ ] **Specific Examples**: Concrete details over abstract concepts
- [ ] **Meaningful Numbers**: Context provided for all figures
- [ ] **Essential Content Only**: Everything directly serves the purpose
- [ ] **No Zombie Nouns**: Active verbs instead of nominalizations
- [ ] **No Predictable Combinations**: Specific language over clichéd business phrases
- [ ] **Agency Clarity**: Real decision-maker clearly identified as subject

### 4. MOBILE & SPEECH OPTIMIZATION
**Question**: Does the language work in 2-minute mobile conversations?

**Speech Flow:**
- [ ] **Natural Rhythm**: Sentences flow when read aloud
- [ ] **No Tongue Twisters**: Avoids awkward word combinations
- [ ] **Conversational Tone**: Sounds like explaining to a friend
- [ ] **Clear Pronunciation**: Easy to speak and understand verbally

**Mobile Format:**
- [ ] **Scannable Structure**: Information easy to process quickly
- [ ] **Short Paragraphs**: Digestible chunks for mobile screens  
- [ ] **Clear Visual Hierarchy**: Important information stands out

## Critical Failure Conditions

**Automatic FAIL if any of these are present:**

**Language Accessibility Issues:**
- Business jargon without definition ("leverage", "optimize", "strategic", "ecosystem")
- Complex vocabulary inaccessible to non-native English speakers
- Cultural idioms or expressions that don't translate globally
- Technical terms used without immediate explanation

**Sentence Structure Problems:**
- Vague pronouns without clear antecedents ("this", "it", "they")
- Sentence fragments missing subject or verb
- Passive voice that obscures WHO does WHAT
- Complex grammatical constructions that impede understanding
- Left-branching sentences that delay main clause
- Unclear agency - not obvious who does what

**Content Inefficiency:**
- Filler phrases that add no information ("it's worth noting", "at the end of the day")
- Weak intensifiers that dilute meaning ("very", "really", "extremely")
- Redundant words and unnecessary qualifiers
- Abstract language when concrete examples would clarify
- Zombie nouns instead of active verbs ("make a decision" vs "decide")
- Predictable business clichés ("significant growth", "operational efficiency")
- Numbers without context or comparison
- Wrong currency for local context (using $ for Indian companies instead of rupees)
- Exaggerated business dynamics not grounded in reality
- Redundant conclusion explanations that don't trust user intelligence

**Mobile & Speech Issues:**
- Awkward word combinations that create tongue twisters
- Unnatural rhythm that doesn't flow when spoken aloud
- Complex sentence structures that don't work in conversation
- Information density too high for quick mobile consumption

## Output Format

```xml
<language-style-evaluation>
    <exercise-info>
        <name>[Exercise Name and Type]</name>
        <language-assessment>[Overall language quality assessment]</language-assessment>
    </exercise-info>
    
    <binary-checks>
        <!-- language-accessibility Section Checks -->
        <accessibility-no-business-jargon>PASS/FAIL</accessibility-no-business-jargon>
        <accessibility-simple-word-choices>PASS/FAIL</accessibility-simple-word-choices>
        <accessibility-no-complex-vocabulary>PASS/FAIL</accessibility-no-complex-vocabulary>
        <accessibility-technical-terms-defined>PASS/FAIL</accessibility-technical-terms-defined>
        <accessibility-universal-vocabulary>PASS/FAIL</accessibility-universal-vocabulary>
        <accessibility-no-cultural-idioms>PASS/FAIL</accessibility-no-cultural-idioms>
        <accessibility-simple-grammar>PASS/FAIL</accessibility-simple-grammar>
        
        <!-- sentence-structure Section Checks -->
        <structure-active-voice-used>PASS/FAIL</structure-active-voice-used>
        <structure-clear-subject-verb-object>PASS/FAIL</structure-clear-subject-verb-object>
        <structure-one-idea-per-sentence>PASS/FAIL</structure-one-idea-per-sentence>
        <structure-complete-sentences>PASS/FAIL</structure-complete-sentences>
        <structure-right-branching>PASS/FAIL</structure-right-branching>
        <structure-clear-transitions>PASS/FAIL</structure-clear-transitions>
        <structure-explicit-connections>PASS/FAIL</structure-explicit-connections>
        <structure-given-new-contract>PASS/FAIL</structure-given-new-contract>
        <structure-topic-chains>PASS/FAIL</structure-topic-chains>
        
        <!-- content-efficiency Section Checks -->
        <efficiency-no-filler-phrases>PASS/FAIL</efficiency-no-filler-phrases>
        <efficiency-no-weak-intensifiers>PASS/FAIL</efficiency-no-weak-intensifiers>
        <efficiency-no-redundant-words>PASS/FAIL</efficiency-no-redundant-words>
        <efficiency-no-unnecessary-qualifiers>PASS/FAIL</efficiency-no-unnecessary-qualifiers>
        <efficiency-front-loaded-information>PASS/FAIL</efficiency-front-loaded-information>
        <efficiency-specific-examples>PASS/FAIL</efficiency-specific-examples>
        <efficiency-meaningful-numbers>PASS/FAIL</efficiency-meaningful-numbers>
        <efficiency-essential-content-only>PASS/FAIL</efficiency-essential-content-only>
        <efficiency-no-zombie-nouns>PASS/FAIL</efficiency-no-zombie-nouns>
        <efficiency-no-predictable-combinations>PASS/FAIL</efficiency-no-predictable-combinations>
        <efficiency-agency-clarity>PASS/FAIL</efficiency-agency-clarity>
        
        <!-- mobile-speech-optimization Section Checks -->
        <mobile-natural-rhythm>PASS/FAIL</mobile-natural-rhythm>
        <mobile-no-tongue-twisters>PASS/FAIL</mobile-no-tongue-twisters>
        <mobile-conversational-tone>PASS/FAIL</mobile-conversational-tone>
        <mobile-clear-pronunciation>PASS/FAIL</mobile-clear-pronunciation>
        <mobile-scannable-structure>PASS/FAIL</mobile-scannable-structure>
        <mobile-short-paragraphs>PASS/FAIL</mobile-short-paragraphs>
        <mobile-clear-visual-hierarchy>PASS/FAIL</mobile-clear-visual-hierarchy>
    </binary-checks>
    
    <!-- Overall Assessment -->
    <overall-status>PASS/FAIL</overall-status>
    <summary>[2-3 sentences summarizing language quality and accessibility for target audience]</summary>
    <style-violations>[List specific violations or "None"]</style-violations>
</language-style-evaluation>
```

## Evaluation Process

1. **Assess language accessibility** - appropriate for first-year business students?
2. **Check sentence structure** - clear, active voice, well-organized?
3. **Evaluate content efficiency** - every word serves a purpose?
4. **Test mobile optimization** - works in 2-minute verbal conversations?
5. **Identify critical failures** - any automatic failure conditions present?
6. **Output XML results** using the format above

## Quality Benchmarks

**PASS Criteria:**
- Language accessible to first-year business students globally
- Clear sentence structure with active voice and explicit connections
- Every word serves a purpose with no filler or redundancy
- Content flows naturally when spoken aloud in mobile conversations
- Technical terms defined immediately when used

**FAIL Criteria:**
- Business jargon without definition or complex vocabulary
- Vague pronouns, sentence fragments, or passive voice obscuring meaning
- Filler phrases, weak intensifiers, or redundant content
- Awkward phrasing that doesn't work in verbal conversation
- Language inaccessible to global, non-native English speakers

## Evaluation Philosophy

**Accessibility First**: Language must work for global audience of first-year business students.

**Clarity Over Sophistication**: Simple, clear communication beats impressive vocabulary.

**Mobile-First Communication**: All content must work effectively in 2-minute verbal conversations.

Remember: This evaluator ensures Socratify exercises use language that is accessible, efficient, and optimized for mobile learning conversations with a global audience.