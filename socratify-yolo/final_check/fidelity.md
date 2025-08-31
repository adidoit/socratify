# Business Situation Fidelity Evaluator

This evaluator assesses whether business situations in Socratify exercises are realistic, accurate, and grounded in actual business dynamics - not fictional or fantastical scenarios.

## Core Purpose

Socratify exercises must present business situations that:
- Could realistically happen in the actual business world
- Reflect accurate company data and market dynamics
- Present genuine business challenges students might encounter
- Avoid unrealistic scenarios that undermine credible learning

## Evaluation Principles

### **Business Realism**
- Company actions reflect realistic strategic thinking and capabilities
- Market dynamics follow actual business world patterns
- Competitive responses align with real industry behavior
- Scenarios could plausibly happen in the real business environment

### **Data Accuracy**
- Financial figures are proportionate and credible for company size/industry
- Market data aligns with actual market conditions and trends
- Company information is consistent with known facts about the organization
- Industry dynamics accurately reflect real competitive landscapes

### **Strategic Plausibility**
- Business decisions make strategic sense given stated context
- Resource allocations are appropriate for company stage and capabilities
- Timeline expectations match realistic business implementation cycles
- Risk/reward ratios reflect sound business judgment

## Validation Framework

### 1. BUSINESS REALISM
**Question**: Could this business situation realistically happen?

**Company Behavior:**
- Actions align with company's known strategy and capabilities
- Resource allocation decisions are realistic for company size/stage
- Strategic moves reflect genuine business logic and constraints
- Timeline expectations are believable for actual implementation

**Market Context:**
- Competitive responses are realistic for the industry
- Economic factors and market conditions are accurately represented
- Industry trends align with actual business environment
- Consumer/customer behavior assumptions are grounded in reality

### 2. DATA ACCURACY
**Question**: Are all facts and figures credible and accurate?

**Financial Data:**
- Revenue, cost, and investment figures are proportionate for company/industry
- Market size estimates align with actual market data
- Growth rates and projections are credible
- Financial implications match realistic business scales

**Company Information:**
- Company details consistent with known public information
- Strategic positioning aligns with actual company capabilities
- Historical context accurate when referencing real events
- Competitive landscape reflects actual market players

### 3. STRATEGIC PLAUSIBILITY
**Question**: Do the business moves make strategic sense?

**Strategic Logic:**
- Decisions follow logical reasoning given stated context
- Risk/reward ratios reflect sound business judgment
- Competitive positioning makes sense for company stage/resources
- Resource utilization is strategically appropriate

**Implementation Realism:**
- Technology and operational constraints are realistic
- Regulatory environment accurately reflected when relevant
- Market timing and conditions support the strategic moves
- Capability requirements match what company could reasonably develop

## Critical Failure Conditions

**Automatic FAIL if any of these are present:**

**Unrealistic Scenarios:**
- Business situations that couldn't realistically occur in practice
- Company actions that defy basic business logic or capabilities
- Market dynamics that contradict known business realities
- Strategic moves that no competent business would consider

**Data Inaccuracies:**
- Financial figures wildly disproportionate for company/industry size
- Company information that contradicts known public facts
- Market data that conflicts with actual business conditions
- Industry dynamics that are factually incorrect or outdated

**Strategic Impossibilities:**
- Resource allocations that make no business sense
- Timeline expectations impossible to achieve in practice
- Competitive assumptions that ignore market realities
- Implementation requirements beyond company capabilities

## Output Format

```xml
<business-fidelity-evaluation>
    <exercise-info>
        <name>[Exercise Name and Type]</name>
        <business-situation>[Core business situation being evaluated]</business-situation>
    </exercise-info>
    
    <binary-checks>
        <!-- business-realism Section Checks -->
        <realism-company-actions-realistic>PASS/FAIL</realism-company-actions-realistic>
        <realism-resource-allocation-realistic>PASS/FAIL</realism-resource-allocation-realistic>
        <realism-strategic-moves-logical>PASS/FAIL</realism-strategic-moves-logical>
        <realism-timeline-believable>PASS/FAIL</realism-timeline-believable>
        <realism-competitive-responses-realistic>PASS/FAIL</realism-competitive-responses-realistic>
        <realism-market-conditions-accurate>PASS/FAIL</realism-market-conditions-accurate>
        <realism-industry-trends-accurate>PASS/FAIL</realism-industry-trends-accurate>
        <realism-customer-behavior-grounded>PASS/FAIL</realism-customer-behavior-grounded>
        
        <!-- data-accuracy Section Checks -->
        <data-financial-figures-proportionate>PASS/FAIL</data-financial-figures-proportionate>
        <data-market-size-accurate>PASS/FAIL</data-market-size-accurate>
        <data-growth-rates-credible>PASS/FAIL</data-growth-rates-credible>
        <data-company-info-consistent>PASS/FAIL</data-company-info-consistent>
        <data-strategic-positioning-accurate>PASS/FAIL</data-strategic-positioning-accurate>
        <data-historical-context-accurate>PASS/FAIL</data-historical-context-accurate>
        <data-competitive-landscape-realistic>PASS/FAIL</data-competitive-landscape-realistic>
        
        <!-- strategic-plausibility Section Checks -->
        <strategy-decisions-logical>PASS/FAIL</strategy-decisions-logical>
        <strategy-risk-reward-sound>PASS/FAIL</strategy-risk-reward-sound>
        <strategy-competitive-positioning-sensible>PASS/FAIL</strategy-competitive-positioning-sensible>
        <strategy-resource-utilization-appropriate>PASS/FAIL</strategy-resource-utilization-appropriate>
        <strategy-technology-constraints-realistic>PASS/FAIL</strategy-technology-constraints-realistic>
        <strategy-regulatory-environment-accurate>PASS/FAIL</strategy-regulatory-environment-accurate>
        <strategy-market-timing-appropriate>PASS/FAIL</strategy-market-timing-appropriate>
        <strategy-capability-requirements-realistic>PASS/FAIL</strategy-capability-requirements-realistic>
    </binary-checks>
    
    <!-- Overall Assessment -->
    <overall-status>PASS/FAIL</overall-status>
    <summary>[2-3 sentences summarizing whether business situation is realistic and grounded in actual business dynamics]</summary>
    <unrealistic-elements>[List specific unrealistic elements or "None"]</unrealistic-elements>
</business-fidelity-evaluation>
```

## Evaluation Process

1. **Assess business realism** - could this situation actually occur in practice?
2. **Verify data accuracy** - are all facts, figures, and company details credible?
3. **Evaluate strategic plausibility** - do the business moves make logical sense?
4. **Identify critical failures** - any unrealistic scenarios, data inaccuracies, or strategic impossibilities?
5. **Output XML results** using the format above

## Quality Benchmarks

**PASS Criteria:**
- Business situation could realistically occur in actual business world
- All financial figures and data are credible and proportionate
- Company actions reflect realistic strategic capabilities and logic
- Market dynamics and competitive responses are grounded in reality
- Strategic decisions follow sound business reasoning

**FAIL Criteria:**
- Unrealistic scenarios that couldn't happen in practice
- Data inaccuracies or figures wildly disproportionate to reality
- Strategic moves that defy basic business logic
- Company actions beyond realistic capabilities
- Market assumptions that contradict known business realities

## Evaluation Philosophy

**Realism Over Drama**: Credible business scenarios are more valuable than exciting but implausible ones.

**Accuracy Over Approximation**: Data and company information must be factually grounded.

**Strategic Soundness**: All business moves must reflect competent strategic thinking within realistic constraints.

Remember: This evaluator ensures Socratify exercises present realistic business challenges grounded in actual business dynamics, not fictional scenarios that undermine credible learning.