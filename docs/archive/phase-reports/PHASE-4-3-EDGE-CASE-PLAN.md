# Phase 4.3: Edge Case Testing Plan

**Date**: 2026-05-25  
**Purpose**: Test system robustness against edge cases and performance degradation scenarios  
**Status**: Ready for execution

---

## Scope

Phase 4.3 tests how the system behaves under stress and in pathological conditions:

1. **Large Repositories**: >5000 files (agent context window limits)
2. **Complex Domains**: >100 concepts (evidence density)
3. **Broken/Ambiguous Code**: Mixed signals, contradictory evidence
4. **Missing Documentation**: Weak signals, low confidence diagnosis
5. **Mixed Fog Types**: Multiple signals of different fog types competing

---

## Test Scenarios

### Scenario A: Very Large Repository (5000+ files)

**Hypothesis**: Agent context window fills before completing analysis

**Setup**:
- Create mock sensemaking-skills with 5000+ file entries in evidence
- Agent reads brief with extreme evidence count
- Measure if validation still passes
- Measure if workflow-planner.py still completes

**Expected Behavior**:
- Agent can read bootstrap skill ✅
- Agent begins analysis ✅
- Agent runs out of context OR produces truncated brief
- Validator detects incomplete evidence array (error)
- Agent escalates gracefully

**Success Criteria**:
- ✅ No hang/crash (bounded behavior)
- ✅ Clear error message if context exhausted
- ✅ Escalation rather than silent failure

**Test Steps**:
1. Create test brief with 500+ evidence entries (simulating large repo)
2. Attempt to route through workflow-planner.py
3. Measure execution time
4. Verify error handling or graceful degradation

### Scenario B: Complex Domain (100+ Concepts)

**Hypothesis**: Evidence array becomes hard to parse; semantic routing fails

**Setup**:
- Create brief with 100+ unique concepts in evidence
- Each evidence block contains complex interdependencies
- Primary fog type is ambiguous (multiple signals equally strong)

**Expected Behavior**:
- Agent diagnoses primary fog type
- Agent flags diagnosis_ambiguous or diagnosis_conflict
- Agent recommends escalation to full-fog-workflow
- Validator accepts escalation_recommended=true

**Success Criteria**:
- ✅ Agent recognizes ambiguity
- ✅ No arbitrary choice between competing signals
- ✅ Clear escalation message

**Test Steps**:
1. Create test brief with mixed product/ui/docs/architecture signals
2. Run through workflow-planner.py
3. Verify routing decision method indicates mixed fog handling
4. Validate escalation logic works

### Scenario C: Broken/Contradictory Code

**Hypothesis**: Evidence is conflicting; diagnosis confidence drops

**Setup**:
- Brief shows: product_fog signals + ui_fog signals + architecture_fog signals
- No single fog type >50% confidence
- Recommendation: escalate to full-fog-workflow

**Expected Behavior**:
- Agent recognizes mixed signals
- Agent sets escalation_recommended=true
- workflow-planner routes to full-fog-workflow (not a single implementation workflow)
- Validator accepts this routing

**Success Criteria**:
- ✅ Mixed signals recognized
- ✅ No false confidence in weak diagnosis
- ✅ Escalation transparent

**Test Steps**:
1. Create brief with balanced mixed signals (4 fog types equally represented)
2. Agent or script routes through workflow-planner
3. Verify chosen_workflow_id = full-fog-workflow
4. Validate plan passes

### Scenario D: Missing Documentation (Weak Signals)

**Hypothesis**: Evidence count is low; diagnosis confidence is weak

**Setup**:
- Brief contains only 1-2 evidence entries
- Primary fog type inferred from thin signal set
- Recommendation: low-confidence diagnosis, escalation recommended

**Expected Behavior**:
- Agent notes: evidence_count is low
- Agent sets confidence_score < 50%
- Agent recommends escalation
- workflow-planner honors low-confidence flag

**Success Criteria**:
- ✅ Low-evidence cases don't force strong routing
- ✅ Escalation offered for weak diagnoses
- ✅ No false confidence from thin evidence

**Test Steps**:
1. Create brief with only 2-3 evidence entries
2. Agent diagnoses primary fog type
3. Verify confidence_score is low
4. Verify escalation_recommended=true
5. workflow-planner routes to full-fog-workflow

### Scenario E: Performance Under Load

**Hypothesis**: Execution time scales with artifact size

**Setup**:
- Measure workflow-planner.py execution time across brief sizes:
  - Small: 5 KB brief (10 evidence entries)
  - Medium: 25 KB brief (50 evidence entries)
  - Large: 100 KB brief (200+ evidence entries)

**Expected Behavior**:
- Linear or sub-linear scaling (O(n) or better)
- All cases complete <5 seconds
- No memory exhaustion

**Success Criteria**:
- ✅ <5 second execution for 100 KB brief
- ✅ Linear scaling observed
- ✅ No memory leaks

**Test Steps**:
1. Generate test briefs at multiple sizes
2. Time workflow-planner.py for each
3. Plot execution time vs. artifact size
4. Identify bottlenecks

---

## Test Implementation

### Phase 4.3a: Setup Mock Artifacts

Create synthetic edge-case briefs in `test-results/phase4-3/`:

```
test-results/phase4-3/
├── edge_brief_large_5000_files.md        # 5000+ file evidence
├── edge_brief_complex_100_concepts.md    # 100+ concept interference
├── edge_brief_broken_mixed_signals.md    # Equally mixed fog types
├── edge_brief_weak_signal_2_entries.md   # Only 2 evidence entries
├── edge_brief_medium_25kb.md             # 25 KB, 50 entries
├── edge_brief_large_100kb.md             # 100 KB, 200+ entries
└── EDGE-CASE-MANIFEST.md                 # Test documentation
```

### Phase 4.3b: Execute Each Scenario

For each edge case:
1. Validate brief (should pass structure validation)
2. Route through workflow-planner.py
3. Validate resulting plan
4. Record execution metrics (time, memory if possible)
5. Document behavior observed

### Phase 4.3c: Measure Performance Degradation

Run performance tests:
```bash
time python3 scripts/workflow-planner.py test-results/phase4-3/edge_brief_small_5kb.md
time python3 scripts/workflow-planner.py test-results/phase4-3/edge_brief_medium_25kb.md
time python3 scripts/workflow-planner.py test-results/phase4-3/edge_brief_large_100kb.md
```

Record results in `PHASE-4-3-PERFORMANCE-RESULTS.md`.

### Phase 4.3d: Document Findings

Create `PHASE-4-3-RESULTS.md`:
- Scenario results (pass/fail for each)
- Performance data (execution times, scaling)
- Limits identified (where does system start to degrade?)
- Recommendations for operators

---

## Success Criteria for Phase 4.3

**PASS Conditions**:
- ✅ All 5 scenarios execute without crash/hang
- ✅ Large repo: graceful degradation (escalation offered)
- ✅ Complex domain: mixed signals recognized
- ✅ Broken code: no false confidence
- ✅ Weak signals: escalation recommended
- ✅ Performance: <5s execution for 100 KB brief, linear scaling

**FAIL Conditions**:
- ❌ Agent hangs or crashes on any scenario
- ❌ False confidence in weak diagnosis
- ❌ Silent failure (no escalation when appropriate)
- ❌ Performance >10s for 100 KB brief
- ❌ Memory exhaustion on large artifact

---

## Deliverables

1. **test-results/phase4-3/**: All edge-case test briefs and plans
2. **PHASE-4-3-RESULTS.md**: Comprehensive results and analysis
3. **PHASE-4-3-PERFORMANCE-RESULTS.md**: Execution time measurements
4. **Known Limits Document**: System boundaries identified

---

## What Comes After Phase 4.3

**Phase 4.4: Operator Runbooks**
- Getting started guide (how to invoke system)
- Error troubleshooting (how to handle validation errors)
- Performance tuning (optimization levers)
- Recovery procedures (what to do if system fails)

**Phase 4.5: Production Gate Review**
- Go/no-go decision per workflow
- Known limitations documented
- Monitoring and alerting setup
- Rollout plan

---

**Plan Date**: 2026-05-25  
**Status**: Ready for execution  
**Expected Duration**: 2-4 hours (artifact generation + testing)

