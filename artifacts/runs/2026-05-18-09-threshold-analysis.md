# Threshold Analysis & Tuning Opportunities
## Based on May 18 Full Fog Path Execution

**Date**: 2026-05-18  
**Data Point**: 1 (Metamorfose Finance)  
**Status**: Provisional - needs 3-5 more runs for statistical confidence  

---

## Current Provisional Heuristic

```
research_needed = (unknowns_count >= 5) OR (clarity_assessment == "low")
```

**Validation Status**: ✅ PASS on one data point (Metamorfose Finance)
- unknowns_count: 9 (>= 5) ✓
- clarity_assessment: "medium" (NOT "low")
- Result: research_needed = true ✓ (correctly routed to discovery)

---

## Open Questions About Thresholds

### Question 1: Is unknowns_count >= 5 the right threshold?

**Current Data**:
- Metamorfose Finance: unknowns_count = 9 → correctly routed to research ✓

**Scenarios to Validate**:

| unknowns_count | clarity | Expected Outcome | Validated |
|---|---|---|---|
| 1-2 | high | Skip research (implementation ready) | No |
| 3-4 | high | Skip research | No |
| 5-6 | high | Include research (threshold borderline) | No |
| 7-8 | high | Include research | No |
| 9+ | any | Include research | Yes (1 data point) |

**Why Threshold Might Be Wrong**:
1. **Too Low**: Maybe 5 is too conservative. Could we handle 4-5 unknowns without research?
2. **Too High**: Maybe 5 is too high. Should we research anything >= 3 unknowns?
3. **Context-Dependent**: Maybe the threshold should vary by domain (finance, auth, UI, etc.)

**Recommendation for Validation**: 
Test on projects with unknowns_count = 3, 4, 5, 6, 7 to find the actual inflection point.

### Question 2: When should clarity_assessment = "medium" trigger research_needed independently?

**Current Logic**:
```
research_needed = (unknowns_count >= 5) OR (clarity == "low")
```

In Metamorfose Finance:
- clarity = "medium" (didn't trigger research alone)
- BUT unknowns_count = 9 (did trigger research)
- Net result: research_needed = true ✓

**Edge Case**: What if we have:
- clarity = "medium"
- unknowns_count = 3

**Current logic**: research_needed = false (neither condition met)
**Question**: Is that correct? Should "medium" clarity ever trigger research independently?

**Scenarios to Validate**:

| unknowns_count | clarity | Current Logic | Is This Right? |
|---|---|---|---|
| 1-2 | high | false | ✓ Implementation ready |
| 1-2 | medium | false | ? Maybe true? |
| 1-2 | low | true | ✓ Research needed |
| 3-4 | high | false | ? Maybe true? |
| 3-4 | medium | false | ? Borderline |
| 3-4 | low | true | ✓ Research needed |
| 5+ | any | true | ✓ Research needed |

**Recommendation for Validation**:
Test on projects with medium clarity + low unknowns. Does analysis still provide value? Do teams need discovery/research even with few unknowns but medium clarity?

### Question 3: Should Dual-Path Divergence Automatically Trigger Consolidation Over Discovery?

**New Finding from May 18**:
When the sensemaking brief identifies "incomplete refactoring with dual-path divergence", should the orchestrator recommend:
- A) consolidation-before-discovery (wait for architecture stability)
- B) discovery-and-consolidation-in-parallel (extract specs while fixing architecture)
- C) consolidation-only (skip discovery, architecture is the priority)

**Current Routing Rule**:
```
IF research_needed = true THEN insert_discovery_workflow
```

**Proposed New Rule**:
```
IF (incomplete_refactoring == true) AND (dal_coverage < 0.80) THEN
  recommend consolidation-before-discovery
ELSE IF research_needed == true THEN
  recommend discovery-first
END
```

**May 18 Evidence Supports**: Option A (consolidation-before-discovery)
- Reason: Dual-path divergence is worse than single implicit pattern
- Fixing divergence unblocks better discovery work later

**Needs Validation**: Test on other repos with coexisting patterns.

---

## Proposed Threshold Refinements

### Refinement 1: Clarity Assessment Levels
**Current**:
```
clarity_assessment ∈ {"critical", "high", "medium", "low"}
```

**Observation**: 
- May 18 has clarity = "medium" and unknowns = 9
- Yet unknowns triggered research (not clarity)
- This suggests "medium" clarity alone might not be sufficient

**Proposal**:
```
research_needed = (unknowns_count >= 5) 
                  OR (clarity_assessment == "low")
                  OR (clarity_assessment == "medium" AND unknowns_count >= 3)
```

**Rationale**: 
- Low clarity always needs research
- Medium clarity needs research only if complexity is high (unknowns >= 3)

### Refinement 2: Boundary-Specific Thresholds
**Observation**: Different weakest boundaries might need different thresholds.

**Examples**:
- **"Implicit Contract"** (Metamorfose case) → unknowns = 9 → research needed
- **"Ghost Features"** (unused code paths) → unknowns = 2 → might not need research
- **"Safety Gaps"** (security boundary) → unknowns = 1 → ALWAYS needs research

**Proposal**: 
```
IF weakness_type == "safety_gap" THEN research_needed = true
ELSE IF weakness_type IN ["ghost_features", "vocabulary_drift"] THEN research_needed = (unknowns_count >= 7)
ELSE research_needed = (unknowns_count >= 5) OR (clarity == "low")
```

**Needs Validation**: Collect weakness_type data across multiple runs.

### Refinement 3: Coverage-Based Thresholds
**New finding**: DAL coverage % might be a signal for research_needed.

**Proposal**:
```
IF dal_coverage < 0.30 THEN research_needed = true  // New pattern barely started
ELSE IF dal_coverage < 0.80 THEN research_needed = (unknowns_count >= 4)  // Incomplete, but progressing
ELSE research_needed = (unknowns_count >= 5)  // Well-formed, normal threshold
```

**Rationale**: When refactoring is far along (80%+ coverage), fewer unknowns trigger research.

**Needs Validation**: Collect coverage metrics across runs.

---

## Evidence Quality Check

### What We Know (High Confidence)
1. ✅ unknowns_count >= 5 correctly triggers research (1 data point)
2. ✅ clarity = "medium" alone doesn't override unknowns (1 data point)
3. ✅ Dual-path divergence is a real risk worth prioritizing (1 data point)

### What We Don't Know (Needs Validation)
1. ❓ Is 5 the optimal threshold, or is it too conservative/aggressive?
2. ❓ Do projects with unknowns_count = 3-4 benefit from research?
3. ❓ Does "medium" clarity + low unknowns ever need research?
4. ❓ Is dual-path divergence common enough to warrant routing rules?
5. ❓ Do different weakness types need different thresholds?
6. ❓ Should DAL coverage % inform research decisions?

### Confidence Levels

| Claim | Evidence | Confidence |
|---|---|---|
| `unknowns_count >= 5` triggers research | 1 success case | 30% (low) |
| Dual-path divergence is a risk | 1 case, but clear | 50% (medium) |
| clarity="medium" alone insufficient | 1 case shows it doesn't solo trigger | 20% (low) |
| Current heuristic is "good enough" | Works on 1 repo | 30% (low) |

---

## Validation Plan

To increase confidence from 30% to >80%, run Full Fog Path on:

### Set A: Similar Projects (Finance/Backend Domain)
- Repo with incomplete refactoring (like Metamorfose)
- Repo with completed refactoring (good example)
- Repo with no refactoring (monolithic)

### Set B: Different Domains
- UI/Frontend heavy repo (different unknowns profile)
- Auth/Security system (safety-critical)
- Data pipeline (ETL/transformation)

### Set C: Edge Cases
- Very small repo (few unknowns by definition)
- Greenfield project (all known, can be implemented)
- Mature legacy system (many knowns, few unknowns)

### Measurement Points
For each run, collect:
- unknowns_count
- clarity_assessment
- research_needed (output)
- dal_coverage (if refactoring)
- weakness_type (output)
- Domain (backend, frontend, auth, etc.)
- Recommendations accuracy (did discovered weaknesses matter?)

---

## Hypothesis for Next Validation

**H1**: `unknowns_count >= 5` is the correct threshold
- If <30% of projects with unknowns_count=4 skip research and fail: threshold is too high
- If >30% of projects with unknowns_count=4 do research and succeed: threshold is too low

**H2**: `clarity="medium"` never triggers research alone
- Run on a project with clarity="medium" and unknowns_count=2
- If recommendation is useful: threshold is too high
- If recommendation is not useful: threshold is correct

**H3**: Dual-path divergence should trigger consolidation-before-discovery
- Find a repo with coexisting patterns but no explicit divergence risk
- Run existing skills (no dual-path detection)
- Run improved skills (with dual-path detection)
- Measure: which recommendation led to better outcomes?

---

## Timeline & Budget

**Current Status**:
- Evidence gathered: 1 data point (Metamorfose Finance)
- Confidence: 30% (provisional heuristic OK)
- Budget remaining: 4-5 runs before thresholds "lock in"

**Recommended Spending**:
- Week 1 (May 19-23): Run Set A (3 runs) - Finance/Backend domain
- Week 2 (May 26-30): Run Set B (2 runs) - Different domains
- Week 3+ (June onwards): Run Set C + continuous validation

**Stop Criteria**: 
- Once 5+ runs confirm `unknowns_count >= 5` is correct
- Or once we find a better threshold with statistical confidence
- Or once thresholds are domain-specific and documented

---

## Conclusion

**Current heuristic is working** based on 1 data point. But **confidence is low** (30%).

**To increase confidence**, we need 4-5 more full runs across different project types.

**In the meantime**: 
- Use current threshold (unknowns_count >= 5)
- Document it as provisional
- Collect metrics for tuning
- Plan validation runs

**Don't change thresholds yet** - the 1 data point validates them adequately for deployment, but not for optimization.

