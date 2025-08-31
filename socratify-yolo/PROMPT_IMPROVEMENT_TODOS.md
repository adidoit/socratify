# Prompt Improvement TODOs Based on Goldilocks Analysis

## High Priority Fixes Needed

### 1. Universal Binary Checks Integration
**Problem**: Prompts lack systematic goldilocks binary check integration
**Fix**: Add goldilocks binary check validation steps to all exercise type prompts
**Files**: All `generate/*.md` files
**Impact**: High - ensures systematic goldilocks compliance

### 2. Exercise-Specific Goldilocks Patterns
**Problem**: Each exercise type has unique goldilocks risks not fully addressed
**Fix**: Add exercise-specific goldilocks guidance to each prompt
**Files**: All `generate/*.md` files
**Details**:
- **Assumption**: Add guidance on avoiding binary vs overly complex scenarios
- **Data**: Strengthen decision context requirements
- **Options**: Improve failure establishment requirements
- **Response**: Strengthen specific entity naming requirements
- **Trade_off**: Improve explicit trade-off statement requirements

### 3. ICP Accessibility Systematic Checks
**Problem**: Prompts mention ICP but lack systematic accessibility validation
**Fix**: Add ICP accessibility checklist to all prompts
**Requirements**:
- Entry-level job seeker perspective check
- Business knowledge assumption audit
- Interview preparation value verification
- Universal business concept usage validation

### 4. Curse of Knowledge Prevention
**Problem**: Prompts have banned word lists but need proactive curse of knowledge checks
**Fix**: Add systematic curse of knowledge prevention steps
**Requirements**:
- Undefined acronym detection (beyond current banned lists)
- Industry context bridging requirements
- Technical concept explanation mandates
- Universal experience grounding checks

## Medium Priority Improvements

### 5. Dominant Answer Trap Prevention
**Problem**: Some exercise types risk obvious answer scenarios
**Fix**: Add specific dominant answer trap checks per exercise type
**Focus Areas**:
- **Response**: Prevent telegraphed competitive responses
- **Assumption**: Avoid obvious assumption scenarios
- **Trade_off**: Prevent obvious trade-off evaluations

### 6. Blue Sky Paralysis Prevention
**Problem**: Some prompts could generate overly broad questions
**Fix**: Strengthen constraint requirements
**Focus Areas**:
- **Data**: Ensure decision context specification
- **Questions**: Ensure specific decision scenario requirements
- **Options**: Ensure clear failure context establishment

### 7. Mobile Discussion Quality Checks
**Problem**: Prompts mention mobile optimization but need specific validation
**Fix**: Add mobile discussion quality checklist
**Requirements**:
- 30-second grasp test
- 5-10 minute discussion sustainability check
- Verbal flow validation
- Re-reading elimination verification

## Low Priority Enhancements

### 8. Exercise Type Cross-Validation
**Problem**: Similar scenarios might work better as different exercise types
**Fix**: Add cross-exercise type validation guidance
**Benefit**: Ensures optimal exercise type selection for each scenario

### 9. Progressive Difficulty Calibration
**Problem**: Prompts don't systematically calibrate for entry-level difficulty
**Fix**: Add difficulty calibration guidelines
**Benefit**: Ensures consistent difficulty across exercise types

### 10. Regional Context Preservation
**Problem**: Geographic context handling could be more systematic
**Fix**: Strengthen geographic context preservation requirements
**Benefit**: Better local market relevance

## Specific File Updates Needed

### All Generate Files Need:
1. **Goldilocks Binary Checks Section**: Add 6-check validation framework
2. **ICP Accessibility Checklist**: Systematic entry-level verification
3. **Exercise-Specific Goldilocks Guidance**: Type-specific risk mitigation
4. **Curse of Knowledge Prevention**: Proactive accessibility checks
5. **Mobile Discussion Quality**: Systematic verbal discussion validation

### Priority Order for Implementation:
1. **data.md** - Most at risk for blue sky paralysis
2. **options.md** - Needs better failure context establishment
3. **response.md** - Needs stronger entity naming requirements
4. **trade_off.md** - Needs explicit trade-off statement strengthening
5. **questions.md** - Needs decision context specification
6. **elevator_pitch.md** - Needs pitch context establishment
7. **assumption.md** - Generally strong, minor refinements
8. **contrarian.md** - Generally strong, minor refinements
9. **define_success.md** - Generally strong, minor refinements
10. **hypothesis.md** - Not reviewed in detail, needs assessment

## Expected Impact

### High Priority Fixes:
- **Systematic goldilocks compliance**: 85%+ pass rate on binary checks
- **Consistent ICP accessibility**: All exercises serve entry-level learners
- **Eliminated curse of knowledge**: No undefined jargon or assumptions

### Medium Priority Improvements:
- **Reduced dominant answer traps**: Better discussion engagement
- **Eliminated blue sky paralysis**: Clearer question constraints
- **Improved mobile quality**: Better verbal discussion flow

### Low Priority Enhancements:
- **Optimized exercise type selection**: Better scenario-type matching
- **Consistent difficulty**: Appropriate challenge level
- **Enhanced regional relevance**: Better local context preservation

## Implementation Notes

1. **Binary Integration**: Each prompt should include the 6 goldilocks binary checks as validation steps
2. **Exercise-Specific Guidance**: Add type-specific goldilocks risk sections to each prompt
3. **Systematic Validation**: Include step-by-step goldilocks compliance verification
4. **ICP Focus**: Strengthen entry-level job seeker perspective throughout
5. **Accessibility First**: Lead with accessibility requirements rather than trailing additions

This comprehensive prompt improvement plan addresses all goldilocks compliance issues identified in the analysis while maintaining the existing prompt structure and effectiveness.