# Validation Fixture: Metamorfose Finance Improvement Expected Results

**Test Repository**: Metamorfose Edutech Finance System  
**Test Objective**: Prove that improved skills detect dual-path divergence earlier than May 17 baseline  
**Fixture Type**: Expected outputs for validation test suite  

---

## Test Scenario: Full Fog Path on Metamorfose Finance (Improved Skills)

### Input
**Repository**: Metamorfose Edutech finance system (same state as May 18 analysis)  
**User Question**: "How can we simplify the finance system and make it spec-driven?"  

### Expected Outputs by Step

#### Step 1: Problem-Framer (Baseline - No Changes)
**Expected Artifact**: Problem frame  
**No changes expected** — problem framing remains the same

**Expected Traits**:
- Challenge: Finance UI complexity (40+ state variables)
- Context: Phase 4 implementation just completed
- Goal: Simplify and spec-drive the system

---

#### Step 2: Unknowns-Mapper (IMPROVED)

**Artifact**: Unknowns Map  
**Expected Changes from May 17**:

**NEW Questions Asked** (Detection improvement):
- ✅ "Are there coexisting patterns for accessing the same data?"
- ✅ "Which modules use the old pattern vs. new pattern?"
- ✅ "Are there tests comparing old and new implementations?"
- ✅ "Is there a documented deprecation roadmap?"

**Expected Answers for Metamorfose**:
```yaml
coexisting_patterns: true
  old_pattern: "Direct Supabase queries (financial_transactions, month_closures, etc.)"
  new_pattern: "DAL wrapper functions (getTransactionMetrics, getMonthClosures, etc.)"
  both_active: true

dal_coverage: 0.40  # Only 40% of tables have DAL wrappers
  tables_with_queries: [financial_transactions, financial_month_closures, financial_categories, financial_insights, ...]
  tables_with_dal_wrappers: [financial_transactions, financial_month_closures]
  coverage_percentage: 40%

consistency_tests: false
  test_files: []
  comparison_tests: 0

deprecation_roadmap: null
  document: null
  timeline: "undefined"
```

**Metrics Changed**:
- May 17: `unknowns_count=9, clarity="medium"` → research_needed=true
- May 18 (improved): `unknowns_count=8, clarity="medium-high"` → research_needed=true **PLUS** `escalate_priority=true`

**Detection Success**: ✅ Dual-path divergence detected in Step 2 (improvement over Step 4)

---

#### Step 3: Repo-Sensemaker (IMPROVED)

**Artifact**: Repository Sensemaking Brief  
**Expected Changes from May 17**:

**Weakest Boundary Identified** (More specific):
- **May 17**: "Implicit dashboard ↔ aggregation contracts"
  - Risk: "Missing specs create maintenance burden"
  - Action: "product-discovery-sprint"
  
- **May 18 (Improved)**: "Incomplete Refactoring with Divergence Risk"
  - **New Weakness Type**: "Incomplete Refactoring with Divergence Risk" ✅
  - Risk: "Coexisting patterns can diverge silently; dual-path increases complexity"
  - Action: "finance-architecture-consolidation"
  - Metrics: "DAL coverage 40%, no consistency tests, no deprecation plan"

**Evidence in Brief** (More specific):
```yaml
weakest_boundary: "incomplete_refactoring"
weakness_type: "Incomplete Refactoring with Divergence Risk"

detected_patterns:
  coexisting: 
    old: "Direct Supabase queries in finance-overview-aggregator.ts:175-182"
    new: "DAL functions in lib/data-access/months.ts"
    both_in_use: true
  
  dal_coverage:
    percentage: 0.40
    implemented: 2  # getTransactionMetrics, getMonthClosures
    total_needed: 5  # financial_transactions, month_closures, categories, insights, inbox_items
  
  consistency_testing:
    tests_found: 0
    risk_level: "HIGH"
  
  deprecation_planning:
    roadmap_exists: false
    risk_level: "HIGH"

priority_assessment: "URGENT - consolidation blocks discovery"
```

**Detection Success**: ✅ Specific weakness type identified with metrics

---

#### Step 4: Workflow-Orchestrator (IMPROVED)

**Artifact**: Workflow Orchestration Plan  
**Expected Changes from May 17**:

**Routing Logic** (NEW conditional):
- **May 17**: `research_needed=true` → route to `product-discovery-sprint`
  - Problem: Recommends discovery on unstable foundation
  
- **May 18 (Improved)**: `incomplete_refactoring=true AND dal_coverage < 0.80` → route to `consolidation`
  - Recommendation: `finance-architecture-consolidation` (or explicit consolidation steps)
  - Sequencing: "Complete refactoring FIRST, then discover specs on stable architecture"
  - **Detection Success**: ✅ Correct routing logic applied

**Recommendation Quality** (Measurable):
```yaml
may_17_recommendation:
  workflow: "product-discovery-sprint"
  reasoning: "Extract specs through research"
  reusability: 0.60  # 60% of findings were useful
  problem: "Recommends discovery on unstable foundation"

may_18_recommendation:
  workflow: "consolidation"
  primary_action: "Complete DAL wiring (40% → 100% coverage)"
  secondary_action: "Add consistency tests between old/new paths"
  tertiary_action: "Document deprecation roadmap"
  quaternary_action: "Then extract specs on stable architecture"
  reusability: 0.95  # 95% of findings were useful and correct
  advantage: "Recommends consolidation BEFORE discovery (correct sequencing)"
```

---

## Comparison: May 17 vs. May 18 (Improved)

| Dimension | May 17 (Baseline) | May 18 (Improved) | Change |
|-----------|------|------|--------|
| **Detection Step** | Step 4 (orchestrator) | Step 2-3 (unknowns/diagnosis) | ⬆️ Earlier |
| **Problem Specificity** | "Implicit contracts" | "40% DAL coverage + no tests + no plan" | ⬆️ More specific |
| **Clarity** | medium | medium-high | ⬆️ Improved |
| **Recommendation Quality** | 60% reusable | 95% reusable | ⬆️ Better |
| **Root Cause** | Missing specs | Incomplete refactoring | ⬆️ Correct |
| **Action Sequencing** | Discovery-first | Consolidation-first | ⬆️ Correct order |
| **Unknowns Count** | 9 | 8 | ⬇️ Reduced |
| **Evidence Grounding** | Generic | Specific metrics | ⬆️ More concrete |

---

## Failure Modes Prevented

### Failure Mode 1: Wrong Priority (May 17 Problem)
**What Would Have Happened**: 
- Team extracts specifications while architecture is unstable
- Phase 4 refactoring incomplete; spec targets a moving foundation
- Specs become outdated as refactoring completes
- Rework required

**How Improvement Prevents It**: ✅
- Detects incomplete refactoring in Step 2 (unknowns-mapper)
- Asks about DAL coverage explicitly
- Routes to consolidation BEFORE discovery
- Result: Specs written on stable foundation

### Failure Mode 2: Silent Divergence (Worse Than Detected)
**What Could Have Happened**:
- Two data access patterns coexist indefinitely
- Without consistency tests, divergence goes unnoticed
- Bug fix in old pattern breaks new pattern (or vice versa)
- Users see inconsistent data without clear cause

**How Improvement Prevents It**: ✅
- Detects missing consistency tests in Step 3 (repo-sensemaker)
- Flags as high-risk weakness
- Recommends adding tests BEFORE discovery
- Result: Coexistence is safe because both paths are tested

### Failure Mode 3: Indefinite Transition (Unclear State)
**What Could Have Happened**:
- New DAL pattern kept at 40% coverage indefinitely
- "Good enough for now" prevents completion
- Developers confused about which pattern to use
- Technical debt accrues invisibly

**How Improvement Prevents It**: ✅
- Detects absent deprecation plan in Step 3
- Routes to consolidation workflow with explicit timeline
- Makes migration roadmap visible and actionable
- Result: Clear path to completion with communication plan

---

## Validation Test Cases

### Test Case 1: Unknowns-Mapper Detects Coexisting Patterns
**Input**: Metamorfose Finance repository  
**Expected**: New dual-path questions are asked and answered  
**Pass Criteria**: 
- Unknowns map includes coexisting_patterns = true
- DAL coverage is measured as 40%
- Consistency tests are noted as absent
- Escalate_priority = true is set

### Test Case 2: Repo-Sensemaker Identifies Weakness Type
**Input**: Unknowns map from Step 2  
**Expected**: Repo-sensemaker identifies "Incomplete Refactoring with Divergence Risk"  
**Pass Criteria**:
- Brief includes weakest_boundary = "incomplete_refactoring"
- Weakness type matches new definition
- Metrics include DAL coverage percentage
- Risk assessment is HIGH

### Test Case 3: Orchestrator Routes to Consolidation
**Input**: Brief from repo-sensemaker  
**Expected**: Orchestrator recommends consolidation workflow  
**Pass Criteria**:
- Routing logic detects dal_coverage < 0.80
- Recommends consolidation-before-discovery
- Provides specific action steps (wire DAL, add tests, deprecation plan)

### Test Case 4: Detection Earlier Than May 17
**Aggregate Test**: Run full pipeline and compare  
**Expected**: All three improvements work together  
**Pass Criteria**:
- Step 2 detects dual-path risk (was Step 4 in May 17)
- Problem specificity improves (measurable in brief)
- Recommendation improves (consolidation-first is correct)
- Reusability increases (95% vs. 60%)

---

## Regression Test Cases

### Must Pass: Existing Test Runs
**Regression Suite**: All 21 existing test cases must still pass  
**What Should NOT Change**:
- Artifact contracts remain valid
- Validator stack still enforces
- Skill outputs still valid
- Existing workflows still execute

**What MAY Change**:
- Clarity assessment (may improve)
- Unknowns count (may decrease)
- Problem specificity (should improve)
- Recommendation quality (should improve)

---

## Success Criteria for Validation

✅ **Improvement Plan Is Validated** when:
1. Test Case 1 passes (unknowns-mapper detects patterns)
2. Test Case 2 passes (repo-sensemaker identifies weakness)
3. Test Case 3 passes (orchestrator routes to consolidation)
4. Test Case 4 passes (detection earlier than May 17)
5. All 21 regression tests pass (no breaking changes)

**If all 5 criteria pass**: Improvements are ready for deployment ✅

**If any criterion fails**: Improvements need refinement before deployment ❌

---

## Artifacts Generated by This Fixture

- `tests/integration/test_skill_improvements_metamorfose.py` ← Will use this fixture
- `artifacts/runs/2026-05-18-12-improvement-metrics.md` ← Will record metrics from this fixture
- `.validation-cache/run-2026-05-18-validated/` ← Will archive results
