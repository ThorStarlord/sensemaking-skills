# Phase 4.3 Edge Case Testing: Critical Finding

**Date**: 2026-05-25  
**Status**: Edge case testing revealed system limitation  
**Severity**: HIGH — affects escalation path behavior

---

## Summary

During Phase 4.3 edge case testing, a critical routing bug was discovered:

**The workflow-planner does not honor escalation recommendations.**

When a brief sets `escalation_recommended=true` and recommends `full-fog-workflow`, the workflow-planner ignores this and routes to the fog-type-based workflow instead.

---

## What Was Expected

**Test Scenarios A, C, D** (large codebase, mixed signals, weak signals) should route to `full-fog-workflow`:

- **Scenario A (Large 500 files)**: escalation_recommended=true → should route to full-fog-workflow
- **Scenario C (Mixed signals)**: escalation_recommended=true → should route to full-fog-workflow  
- **Scenario D (Weak signals)**: escalation_recommended=true → should route to full-fog-workflow

**Test Scenarios E** (performance tests) should route to fog-type-based workflows:

- **Small**: ui_fog → ui-implementation-workflow ✓
- **Medium**: product_fog → product-implementation-workflow ✓
- **Large**: architecture_fog → architecture-implementation-workflow ✓

---

## What Actually Happened

| Scenario | Expected | Actual | Result |
|----------|----------|--------|--------|
| Large (500 files) | full-fog-workflow | product-implementation-workflow | ✗ FAIL |
| Mixed signals | full-fog-workflow | product-implementation-workflow | ✗ FAIL |
| Weak signals | full-fog-workflow | product-implementation-workflow | ✗ FAIL |
| Perf Small | ui-implementation-workflow | ui-implementation-workflow | ✓ PASS |
| Perf Medium | product-implementation-workflow | product-implementation-workflow | ✓ PASS |
| Perf Large | architecture-implementation-workflow | architecture-implementation-workflow | ✓ PASS |

**Success Rate**: 50% (3/6 scenarios correct)

---

## Root Cause Analysis

**File**: `scripts/workflow-planner.py`  
**Lines**: 88-107

```python
# Line 89: Always use fog-type mapping, regardless of escalation
chosen_workflow_id = FOG_TYPE_TO_WORKFLOW[primary_fog_type]

# Lines 101-107: Recognize the mismatch but don't act on it
system_recommended = brief_data.get("recommended_workflow_id", chosen_workflow_id)
if chosen_workflow_id == system_recommended:
    routing_decision_method = "diagnosis_primary_soft_context"
    routing_divergence = False
else:
    routing_decision_method = "manual_override"  # <-- Records divergence but ignores recommendation
    routing_divergence = True
```

**The Bug**: 
- Line 89 hardcodes `chosen_workflow_id` to the fog-type-based workflow
- Lines 101-107 check if the brief's `recommended_workflow_id` differs from this hardcoded choice
- When they differ, it marks as "manual_override" but never actually uses the recommended workflow

**Fix**: Check `escalation_recommended` flag and honor the `recommended_workflow_id`:

```python
chosen_workflow_id = FOG_TYPE_TO_WORKFLOW[primary_fog_type]

# NEW: Honor escalation recommendations
if brief_data.get("escalation_recommended", False):
    recommended = brief_data.get("recommended_workflow_id")
    if recommended and recommended in valid_workflow_ids:
        chosen_workflow_id = recommended
        routing_decision_method = "escalation_recommended_accepted"
    else:
        # Fallback: use fog-type mapping
        routing_decision_method = "escalation_recommended_invalid"
else:
    routing_decision_method = "diagnosis_primary_soft_context"
```

---

## Performance Test Results (All Passed)

Despite the routing bug, the system passed all performance tests:

```
Scenario              Time (s)   Size (KB)   Success
-------------------------------------------------
performance_small     0.274      0.9         PASS
performance_medium    0.267      1.9         PASS
performance_large     0.266      2.0         PASS
large_500_files       0.475      6.8         PASS
mixed_signals         0.290      5.5         PASS
weak_signals          0.286      3.3         PASS
-------------------------------------------------
Total: 1.858 seconds (average 0.310s per brief)
```

**Scaling Analysis**: Linear-to-sub-linear (1.1x-1.6x slower for 12x larger artifact)

**Conclusion**: Performance is acceptable. Routing logic bug is separate from performance characteristics.

---

## Impact Assessment

### Affected Scenarios
- Scenario A: Large repository (context window constraints) — marked for escalation but not honored
- Scenario C: Mixed fog types (no clear primary) — marked for escalation but not honored
- Scenario D: Weak signals (insufficient evidence) — marked for escalation but not honored

### Correct Behavior (NOT Affected)
- Scenario E: Performance tests — routing works correctly (no escalation needed)
- Normal path: Single fog type without escalation — routes correctly

### Operational Impact
- **Users who receive escalation**: Will get a plan for a single-fog implementation instead of comprehensive full-fog-workflow
- **Risk**: Incomplete solutions for ambiguous or complex repositories
- **Likelihood**: Low (only when escalation is recommended)
- **Severity**: HIGH (delivers wrong solution for most complex cases)

---

## Recommended Fix

**Priority**: HIGH — Fix before Phase 4.4 (operator runbooks)

**Fix Location**: `scripts/workflow-planner.py`, lines 88-107

**Fix Type**: Add escalation logic to honor `escalation_recommended` flag

**Testing**: 
- ✓ Unit test: escalation_recommended=true routes to full-fog-workflow
- ✓ Integration test: re-run Scenarios A, C, D and verify correct routing
- ✓ Regression test: verify Scenarios E still work

**Effort**: ~30 minutes (write fix + test)

---

## What This Reveals About the System

### Positive
- ✓ Performance is excellent (0.3s average, sub-1s for all cases)
- ✓ Artifact validation catches structure errors
- ✓ Scaling is linear (no context explosions)
- ✓ System recognizes when escalation is needed (via flag)

### Gap
- ✗ Escalation logic not enforced in routing
- ✗ Brief's `recommended_workflow_id` is ignored if it differs from fog-type mapping
- ✗ No error when routing divergence is detected

### Lesson
The system correctly identifies escalation scenarios but doesn't act on them. This is a coordination issue: brief correctly says "escalate", but planner doesn't honor it.

---

## Next Steps

**Immediate (Today)**:
1. Fix workflow-planner.py to honor escalation_recommended
2. Re-run Scenarios A, C, D
3. Verify plans now route to full-fog-workflow

**Phase 4.3 Completion**:
4. Document the fix in validation log
5. Update PHASE-4-3-RESULTS.md

**Phase 4.4**:
6. Add escalation logic to operator runbooks
7. Document when users should expect full-fog-workflow

**Phase 4.5**:
8. Include this finding in production gate review
9. Set SLO for escalation handling

---

## Severity Assessment

| Factor | Assessment |
|--------|------------|
| Frequency | Rare (only when escalation recommended) |
| Impact | High (delivers wrong solution type) |
| Detectability | Detected by edge case testing ✓ |
| Fixability | Easy (add one conditional) |
| Risk | Can be fixed before Phase 4.4 |

**Overall**: HIGH priority, LOW risk (caught before production)

---

**Finding Date**: 2026-05-25T05:40:00Z  
**Test Type**: Phase 4.3 Edge Case Testing  
**Detection Method**: Routing validation in performance tests

