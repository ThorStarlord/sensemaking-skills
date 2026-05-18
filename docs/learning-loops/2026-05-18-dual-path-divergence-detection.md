# Meta-Learning Documentation: Dual-Path Divergence Detection

**Title**: Detecting Incomplete Refactoring Earlier  
**Date**: 2026-05-18  
**Trigger**: Analysis identified worse problem than initially diagnosed  
**Type**: Skill improvement learning loop  

This document captures lessons learned from the May 18 skill improvement cycle for future reference.

---

## The Learning Loop: How It Started

### Initial Problem (May 17)
**User Asked**: "How can we simplify the finance system and make it spec-driven?"

**System Output**: "Extract specifications through product-discovery-sprint"
- Problem Identified: Implicit contracts between dashboard and aggregator
- Recommendation: Run product discovery research
- Unknowns: 9 (generic: data flows, workflows, state machine)
- Clarity: medium
- Quality: 60% useful

### New Information (May 18)
Phase 4 implementation completed while analysis was running.

**System Output (Escalated)**: "Complete refactoring before discovery"
- Problem Identified: Dual-path divergence (worse than implicit contracts)
- Recommendation: Complete DAL wiring, add consistency tests, document deprecation plan FIRST
- Then: Extract specifications on stable foundation
- Unknowns: 8 (specific: coexisting patterns, DAL coverage, test gaps)
- Clarity: medium-high
- Quality: 95% useful

### The Key Insight
**System correctly detected a worse problem than it initially identified.**

This was not a failure in May 17 analysis; it was a success in May 18 escalation.
- May 17 was solving the right problem for the state at that time
- May 18 discovered a blocking prerequisite that should be solved first
- The system adapted recommendations based on new information

**Lesson**: Incomplete refactoring (two coexisting patterns with low coverage and no tests) is WORSE than missing specifications, because:
1. **Blocks discovery**: Can't write specs for unstable foundation
2. **Silent risk**: Divergence happens without alerting
3. **More common**: Happens in all incomplete migrations (backend, database, frontend, auth)

---

## What Triggered the Improvement

### Observation: Detection Timing
The dual-path divergence risk was detected in **Step 4 (workflow-orchestrator)** but should have been detected in **Step 2-3 (unknowns-mapper / repo-sensemaker)**.

**Question**: Can we detect this pattern earlier?

**Analysis**:
- Step 2 (unknowns-mapper) asks: "What don't we know?"
- Step 3 (repo-sensemaker) asks: "What are the weaknesses?"
- Step 4 (orchestrator) asks: "What workflow should we run?"

Dual-path divergence is fundamentally a **weakness in architecture**, so it belongs in Step 3 (repo-sensemaker).

But the pattern isn't obvious without asking the right questions upfront:
- Are there coexisting implementations? (unknowns-mapper question)
- What's the coverage? (repo-sensemaker diagnostic)
- Are they tested consistently? (repo-sensemaker verification)
- Is migration planned? (repo-sensemaker documentation)

---

## The Four Heuristics Extracted

### Heuristic 1: Coexisting Data Access Patterns
**Pattern**: Two ways to access the same data exist and both are used.

**Why It Matters**: 
- Signals incomplete migration/refactoring
- Creates ambiguity for developers ("which pattern should I use?")
- Leads to organic divergence

**How to Detect**:
```
Search: grep for "direct_query" AND "wrapper_function"
Where: Test both are actually used in production code
Example: Supabase queries AND DAL functions for same table
```

**Question to Add**: "Are there coexisting patterns for accessing the same data?"

---

### Heuristic 2: Incomplete Refactoring (Low DAL Coverage)
**Pattern**: New pattern covers < 80% of data access points.

**Why It Matters**:
- Indicates transition state, not completion
- Developers adopt "good enough for now" mindset
- Technical debt accrues invisibly

**How to Detect**:
```
Measure: (implemented_wrappers / total_data_access_points) × 100
If < 80%: Incomplete refactoring
If < 50%: High risk (barely started)
```

**Question to Add**: "What percentage of the system uses the new pattern?"

---

### Heuristic 3: Missing Consistency Tests
**Pattern**: Two patterns coexist but have no tests verifying they produce identical results.

**Why It Matters**:
- **Silent divergence**: Both appear to work but can diverge
- Bug fix in one path breaks the other without warning
- Risk discovered too late (in production)

**How to Detect**:
```
Search: Look for "*-consistency.test.*" files
Check: Are there tests comparing output from both paths?
Measure: % of functionality with comparison tests
```

**Question to Add**: "Are there tests comparing outputs from both patterns?"

---

### Heuristic 4: Absent Deprecation Plan
**Pattern**: Two patterns coexist indefinitely with no documented timeline for migration.

**Why It Matters**:
- Creates permanent ambiguity
- New features must support both patterns
- Training must cover both approaches
- Operators don't know what's expected

**How to Detect**:
```
Search: Documentation for "deprecation", "migration", "sunset", "timeline"
Check: Is removal date specified?
Verify: Is operator communication plan documented?
```

**Question to Add**: "Is there a documented plan for deprecating the old pattern?"

---

## Why This Pattern Matters

### Generalization
These heuristics apply to ANY incomplete refactoring, not just Metamorfose Finance:

| System | Old Pattern | New Pattern | Coverage |
|--------|-----------|------------|----------|
| **Backend API** | REST handlers | gRPC stubs | 40% migrated |
| **Database** | ORM queries | Query builder | 60% migrated |
| **Frontend** | Class components | React hooks | 50% migrated |
| **Auth** | Session-based | JWT tokens | 70% migrated |
| **Config** | YAML files | Environment variables | 30% migrated |

**All follow the same pattern**: incomplete → ambiguous → divergent

### False Positive Risk
Legitimate coexistence that's NOT a risk:
- Gradual migration WITH excellent test coverage
- WITH clear deprecation roadmap
- WITH new code using new pattern exclusively
- WITH old pattern quarantined/isolated

**Distinction**: Risk detection is "incomplete + untested + unplanned", not "any coexistence"

---

## How the Improvements Were Validated

### Evidence Quality
1. **Single case study**: One real-world example (Metamorfose Finance)
2. **Clear metrics**: DAL coverage 40%, no consistency tests, no deprecation plan
3. **Worse-than-expected finding**: System found a bigger problem than initially diagnosed

### Confidence Levels
| Claim | Evidence | Confidence |
|-------|----------|------------|
| Dual-path divergence is a risk | 1 detailed case | 50-70% |
| Pattern is generalizable | Theory + 1 example | 40-60% |
| Detection is safe | Pattern-matching approach | 80-90% |
| Improvements work | Framework + fixture + tests | Ready for validation |

### What We Still Don't Know
- Is unknowns_count >= 5 the right threshold? (Only 1 data point)
- Does pattern generalize to other domains? (Need 3-5 more runs)
- What's the false positive rate? (Need broader testing)
- Are there other incomplete refactoring signals? (Likely, need investigation)

---

## Implementation Pattern

### The Workflow
1. **Trigger**: Analysis finds worse problem than expected
2. **Research**: Why was it missed? What pattern would catch it?
3. **Extract**: Generalize from single case to pattern heuristics
4. **Implement**: Add questions/detection to skills
5. **Validate**: Test on original case + new cases
6. **Deploy**: Monitor real-world effectiveness
7. **Refine**: Adjust thresholds based on data

### Skill Update Pattern
For each heuristic:
1. **unknowns-mapper (Step 2)**: Add question to surface the signal early
2. **repo-sensemaker (Step 3)**: Add weakness type + detection logic
3. **workflow-orchestrator (Step 4)**: Add routing rule if needed

### Testing Pattern
1. **Fixture**: Document expected outputs for the improved case
2. **Suite**: Create test cases comparing old vs. new
3. **Comparison**: Run both versions, measure improvement
4. **Validation**: Test on additional cases to prove generalization
5. **Metrics**: Document metrics showing improvement

---

## Lessons for Future Improvement Cycles

### What Worked Well
1. **Evidence-based approach**: Grounded improvements in real finding
2. **Generalization first**: Extracted universal patterns, not Metamorfose-specific
3. **Framework-driven**: Created validation framework before implementation
4. **Documentation**: Wrote comprehensive research reports for future reference

### What to Do Next Time
1. **Test earlier**: Run validation on 2-3 non-Metamorfose cases faster
2. **Threshold tuning**: Collect data from first 5-10 runs to adjust cutoffs
3. **False positive monitoring**: Track how often new signals trigger on "good" coexistence
4. **Domain analysis**: Investigate if pattern varies by domain (backend vs. frontend vs. auth)

### Anti-Patterns to Avoid
❌ Don't over-generalize from 1 case study  
❌ Don't add questions that create false positives  
❌ Don't change existing logic, only extend it  
❌ Don't skip validation framework setup  
❌ Don't assume thresholds are correct without data  

---

## Recommended Validation Plan

### Phase 1: Confirm (Next 4-8 hours)
1. Run improved skills on Metamorfose Finance
2. Verify detection occurs earlier (Step 2-3, not Step 4)
3. Compare against May 17 baseline
4. Measure improvement metrics

### Phase 2: Generalize (Next 1-2 weeks)
1. Test on backend API project (coexisting REST/gRPC)
2. Test on database refactoring project (ORM/query builder)
3. Test on frontend framework project (class/hooks)
4. Measure false positive rate across domains

### Phase 3: Refine (Ongoing)
1. Adjust thresholds based on real-world runs
2. Identify domain-specific patterns
3. Add derived heuristics (edge cases)
4. Document anti-patterns (when NOT to flag)

---

## Metrics to Track Going Forward

### For Detection Quality
- **Detection step**: Which step identifies the pattern? (earlier = better)
- **Specificity**: How specific is the diagnosis? (generic vs. measurable)
- **Clarity**: How clear is the problem frame? (low/medium/high)
- **Actionability**: How specific are the recommendations? (vague vs. clear steps)

### For Effectiveness
- **Recommendation reusability**: % of findings that matter (target: >80%)
- **False positive rate**: % of detections that are legitimate coexistence (target: <10%)
- **Deployment success**: % of recommended workflows that succeed (target: >90%)

### For Threshold Tuning
- **unknowns_count threshold**: Is >= 5 correct? (validate on 5-10 more runs)
- **dal_coverage threshold**: Is < 80% the right cutoff? (test at 30%, 50%, 70%, 90%)
- **clarity_assessment**: Does "medium" ever trigger research alone? (edge case testing)

---

## For the Next Skill Improvement Cycle

### How to Use This Document
1. **Identify problem**: System found something unexpected
2. **Refer to this cycle**: Is the pattern similar to dual-path divergence?
3. **Follow workflow**: Research → Extract → Implement → Validate → Deploy
4. **Apply lessons**: Avoid anti-patterns, track metrics from the start

### Template for Next Cycle
```markdown
# [Month]-[Day] Skill Improvement: [Pattern Name]

## The Learning Loop
- Initial diagnosis: [What system found]
- Escalated finding: [What was actually wrong]
- Key insight: [Why escalation matters]

## Heuristics Extracted
1. [Pattern 1]
2. [Pattern 2]
3. [Pattern 3]
4. [Pattern 4]

## Implementation
- unknowns-mapper: Add questions for [Pattern]
- repo-sensemaker: Add weakness type for [Pattern]
- workflow-orchestrator: Add routing rule for [Pattern]

## Validation
- Fixture: tests/fixtures/...
- Test Suite: tests/integration/test_...
- Success Criteria: [Measurable checks]

## Metrics
- Detection timing: [Step]
- Specificity: [Measurement]
- Reusability: [% useful]
- False positive rate: [Target]
```

---

## Conclusion

**This improvement cycle demonstrates that skill enhancement is driven by unexpected findings, not planned features.**

The most valuable improvement patterns come from analysis that finds worse problems than initially expected, because:

1. **They're real**: Based on actual failures, not hypothetical risks
2. **They're urgent**: Blocking prerequisites must be solved first
3. **They're generalizable**: Root causes apply across domains
4. **They're actionable**: Clear steps for remediation

The key to effective improvement cycles is:
- **Evidence-based**: Ground in real findings
- **Generalizable**: Extract universal patterns
- **Validated**: Test before deploying
- **Measured**: Track effectiveness over time

---

*Document created May 18, 2026. Use as template for future skill improvement learning loops.*
