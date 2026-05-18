---
validator_case: positive
improvement_type: detection_pattern_expansion
evidence_source: usage_research_report_2026-05-18-10
---

# Skill Improvement Plan: Dual-Path Divergence Detection

**Date**: 2026-05-18  
**Validator Case**: Positive (improvements prevent a known failure mode)  
**Scope**: 4 skill updates + 1 registry addition  
**Implementation Status**: Ready for deployment and validation  

---

## 1. Diagnosis

### Failure Mode Identified
**Class**: Incomplete Refactoring with Divergence Risk (NEW weakness type)

**Description**: A codebase has two coexisting data access patterns (old + new) where:
- New pattern is only partially implemented (<80% coverage)
- No consistency tests verify both patterns produce identical results
- No documented deprecation plan for the old pattern
- Developers lack guidance on which pattern to use for new features
- **Result**: Silent divergence risk—both systems appear to work but can drift without detection

**Real-World Impact**: Metamorfose Edutech finance system had direct Supabase queries (old) + DAL wrapper functions (new) with only 40% DAL coverage, no consistency tests, and no migration roadmap. This was a worse problem than the initial "missing specifications" diagnosis because incomplete refactoring blocks reliable discovery work.

### Root Cause Analysis
**Why was this pattern missed initially?**
- May 17 analysis focused on implicit domain contracts → recommended product-discovery-sprint
- May 18 implementation revealed Phase 4 refactoring created coexisting patterns
- System correctly escalated the problem; skills need heuristics to detect this earlier

**Why is earlier detection important?**
1. **Blocking**: Incomplete refactoring blocks reliable specification discovery (you can't extract spec on unstable foundation)
2. **Common**: This pattern appears in all incomplete refactoring scenarios (backend APIs, databases, frontend frameworks, auth systems)
3. **Actionable**: Clear remediation path (complete refactoring, add tests, document deprecation plan)

---

## 2. Evidence

### Source Research Reports
- **Usage Research Report** (`artifacts/runs/2026-05-18-10-usage-research-report.md`)
  - 200+ line comprehensive validation of skill improvements
  - Effectiveness measurements: May 18 recommendation reusability 95% vs. May 17 60%
  - Conclusion: System is production-ready; improvements are safe to deploy
  
- **Extracted Heuristics** (`artifacts/runs/2026-05-18-08-extracted-heuristics.md`)
  - 4 new detection heuristics for dual-path divergence
  - Questions to add to unknowns-mapper (Step 2)
  - Weakness type definition for repo-sensemaker (Step 3)
  - Routing logic for workflow-orchestrator (Step 4)

- **Skill Improvement Analysis** (`artifacts/runs/2026-05-18-07-skill-improvement-analysis.md`)
  - Detailed comparison of May 17 vs. May 18 findings
  - Demonstrates improved clarity and specificity after escalation
  - Documents that system correctly adapted recommendations

### Evidence Snippet: Why May 18 Was Better
| Aspect | May 17 | May 18 | Impact |
|--------|--------|--------|--------|
| **Specificity** | General ("implicit contracts") | Specific ("40% DAL coverage, no tests") | Actionable |
| **Priority** | Long-term (missing specs) | Urgent (current divergence risk) | Clarifies sequencing |
| **Blockers** | Unknown unknowns | Known knowns (concrete metrics) | Enables faster action |
| **Guidance** | "Discover workflows" | "Complete DAL + add tests + deprecate" | Clear steps |

---

## 3. Proposed Skill Improvements

### Improvement 1: Unknowns-Mapper (Step 2)
**File**: `skills/unknowns-mapper/SKILL.md`  
**Change Type**: Add new detection questions to Pathfinding section  

**Additions**:
```markdown
## Dual-Path Detection (NEW)

When mapping unknowns, explicitly ask about coexisting patterns:
- "Are there multiple ways to access the same data (e.g., old direct queries + new DAL wrapper functions)?"
- "If refactoring is in progress, what percentage of the system uses the new pattern? (DAL coverage %)"
- "Are there tests comparing the old and new implementations to verify they produce identical results?"
- "Is there a documented deprecation roadmap for the old pattern?"

**Purpose**: Detect **Incomplete Refactoring with Divergence Risk** in Step 2, not Step 4.

**Routing Signal**: If coexisting patterns are confirmed AND coverage < 80% AND no tests, escalate `escalate_priority = true` to signal that consolidation should precede discovery.
```

**Impact**: Enables detection of dual-path divergence risk early, before full diagnostic analysis.

---

### Improvement 2: Repo-Sensemaker (Step 3)
**File**: `skills/repo-sensemaker/references/weakness-types.md`  
**Change Type**: Add new weakness type (already completed)  

**Status**: ✅ Complete—"Incomplete Refactoring with Divergence Risk" documented as weakness type #8.

**Definition**:
```markdown
8. **Incomplete Refactoring with Divergence Risk**: Two coexisting data access patterns (old + new) 
   that can diverge because:
   - New pattern has low coverage (<80%) and is partially implemented
   - No consistency tests verify both patterns produce identical results
   - No deprecation plan documents migration timeline
   - Developers don't know which pattern to use for new code
   
   Example: Finance system with both direct Supabase queries and DAL wrapper functions, 
   but only 40% migrated to DAL and no tests comparing both paths.
   
   Risk: Silent divergence - both systems appear to work, but data could diverge without warning.
   
   Detection: Search for coexisting patterns, measure DAL coverage, check for consistency tests, 
   look for deprecation roadmap.
```

**Impact**: Formalizes the weakness type so repo-sensemaker can identify and diagnose it.

---

### Improvement 3: Workflow-Orchestrator (Step 4)
**File**: `skills/workflow-orchestrator/SKILL.md`  
**Change Type**: Add consolidation-before-discovery conditional routing  

**Addition**:
```markdown
## Consolidation-Before-Discovery Routing

If the brief indicates `weakest_boundary == "incomplete_refactoring"` with `dal_coverage < 0.80`, 
recommend the `consolidation` workflow instead of `discovery`. This is because incomplete refactoring 
with coexisting patterns (old + new) blocks reliable discovery work.

The recommendation sequence is:
1. Complete refactoring + add consistency tests
2. Then extract specifications on stable architecture

This reverses the normal order (discovery → consolidation) because unstable architecture makes discovery unreliable.
```

**Impact**: Changes routing logic to recommend consolidation BEFORE discovery when incomplete refactoring is detected.

---

### Improvement 4: Workflow Registry (Step 4)
**File**: `skills/workflow-orchestrator/references/workflow-registry.yaml`  
**Change Type**: Add conditional step or reference to consolidation workflow (optional)

**Status**: Conditional routing is documented in orchestrator SKILL.md. A full consolidation workflow can be added later once consolidation skills are defined.

---

## 4. Impact Assessment

### Scope of Changes
- **Minimal**: 4 skill/documentation updates
- **Boundary Compliance**: All changes extend existing detection; no logic replacements
- **Risk**: Low (new questions + new weakness type + new routing condition)
- **Reversibility**: All changes can be removed without breaking existing workflows

### Benefits
1. **Detects dual-path divergence risk in Step 2-3** instead of Step 4 (earlier)
2. **More specific diagnoses** (40% DAL coverage, no tests) vs. generic (implicit contracts)
3. **Better recommendations** (complete refactoring FIRST) vs. wrong sequencing
4. **Actionable next steps** (consolidate, test, document) vs. vague research
5. **Prevents worse problems** (silent divergence) by detecting incomplete refactoring early

### Antifragility: Not Overfitting to Metamorfose
These improvements are NOT tuned to Metamorfose Edutech specifically:
- **Coexisting patterns** are a general architecture principle applicable to any incomplete refactoring
- **DAL coverage measurement** is a standard pattern independent of domain
- **Consistency testing** is a generic quality practice applicable everywhere
- **Deprecation planning** is universal best practice for migrations

**Validation Plan**: Run improved skills on non-Metamorfose repositories to prove generalization.

---

## 5. Verification Plan

### Rerun Scenario: Metamorfose Finance (Same Repo)
**Repository**: Metamorfose Edutech finance system  
**Objective**: Prove that improved skills detect dual-path divergence EARLIER

**Expected Results**:
1. ✅ **Step 2 (unknowns-mapper)**: New questions about coexisting patterns are asked and answered
2. ✅ **Step 3 (repo-sensemaker)**: "Incomplete Refactoring with Divergence Risk" identified as weakest boundary
3. ✅ **Step 4 (orchestrator)**: Recommends `consolidation-before-discovery` routing instead of generic discovery

**Success Criteria**:
- Detection step moves from Step 4 (orchestrator) → Step 2-3 (unknowns/diagnosis)
- Problem description becomes specific (40% DAL coverage, coexisting patterns, no tests)
- Recommendation remains the same (consolidation-before-discovery) but with better justification

### Cross-Repo Validation: Non-Metamorfose Projects
**Objective**: Prove skills generalize beyond single case

**Test Repos** (TBD, selected by user):
- Backend API with coexisting REST + gRPC handlers
- Database with old ORM + new query builder (partial migration)
- Frontend with class components + hooks (mixed)
- Auth system with session-based + JWT tokens (hybrid)

**Expected Results**:
- ✅ New dual-path questions apply to non-finance systems
- ✅ DAL coverage metric generalizes to different migration patterns
- ✅ Consistency testing signal applies across domains
- ✅ Zero false positives for legitimate transitions (high test coverage + deprecation plan)

### Regression Prevention
**Regression Test Suite**: Run skill-maintenance-loop validator against 21 existing test cases
- Must pass: All existing test cases still work with improved skills
- May change: Detection steps and specificity (should improve)
- Must not change: Artifact contracts and validator stack

---

## 6. Anti-Overfitting Guard

### What We're NOT Doing
❌ Tuning skills to detect only Metamorfose-specific problems  
❌ Adding finance-domain-specific heuristics  
❌ Creating domain-specific weakness types  
❌ Hardcoding table names or company-specific patterns  

### What We ARE Doing
✅ Extracting general architectural patterns (coexisting implementations)  
✅ Using universal metrics (coverage %, test coverage, documentation)  
✅ Creating generalizable questions (any refactoring scenario)  
✅ Improving routing logic (applicable to all incomplete refactoring)  

**Proof**: Same heuristics apply to:
- Backend API migration (REST → gRPC)
- Database refactoring (ORM → query builder)
- Frontend modernization (class components → hooks)
- Auth systems (sessions → JWT)
- Configuration management (files → environment)
- Data pipeline stages (batch → streaming)

---

## 7. Dependency Analysis

### Input Dependencies
- **Sources**: May 17 + May 18 Full Fog Path analysis on Metamorfose Finance
- **Artifacts Required**:
  - `artifacts/runs/2026-05-18-08-extracted-heuristics.md` (defines what to implement) ✅
  - `artifacts/runs/2026-05-18-10-usage-research-report.md` (validates improvements) ✅

### Output Dependencies
- **Generated Artifacts**: This improvement plan document (you are here)
- **Enables**: Skill-Improvement-Validation workflow (Workflow 3, tasks 3.2+)
- **Requires**: Validation test suite (`tests/integration/test_skill_improvements_metamorfose.py`)

### Approval Gates
✅ All source materials completed and reviewed  
⏳ Awaiting user approval to proceed with implementation/validation  

---

## 8. Implementation Checklist

### Phase 1: Skill Updates (HIGH PRIORITY)
- [x] Update unknowns-mapper SKILL.md with dual-path detection questions
- [x] Add "Incomplete Refactoring with Divergence Risk" weakness type to repo-sensemaker references
- [x] Update workflow-orchestrator SKILL.md with consolidation-before-discovery routing rule
- [ ] (Optional) Add consolidation workflow to workflow-registry.yaml (can be added later)

**Status**: 3 of 4 tasks complete. Workflow registry update is optional for now.

### Phase 2: Validation Tests
- [ ] Create `tests/integration/test_skill_improvements_metamorfose.py` validation suite
- [ ] Create `tests/fixtures/validate-skill-improvement-plan/metamorfose-finance-improvement.md`
- [ ] Run baseline comparison against May 18 baseline
- [ ] Measure improvement metrics (detection step, specificity, actionability)

### Phase 3: Documentation & Archive
- [ ] Create improvement summary report (`artifacts/runs/2026-05-18-13-improvement-validation-summary.md`)
- [ ] Update baseline cache with validated checkpoint
- [ ] Create meta-learning documentation (`docs/learning-loops/2026-05-18-dual-path-divergence-detection.md`)

---

## 9. Risk Mitigation

### Risk: New Questions Cause False Positives
**Mitigation**: Questions are designed to be specific (coexisting patterns, DAL coverage, consistency tests). False positives only occur if codebase genuinely has these characteristics. Additionally, absence of deprecation plan is not alone sufficient—it must be combined with incomplete coverage and missing tests.

### Risk: Improvements Don't Generalize Beyond Metamorfose
**Mitigation**: Validation plan includes running on 3-5 non-Metamorfose repos. Pattern selection was based on universal architectural principles, not domain-specific details.

### Risk: Regression in Existing Analyses
**Mitigation**: All 21 existing test cases must pass. New questions are additions, not replacements. Existing detection logic unchanged.

### Risk: Orchestrator Routing Breaks Existing Workflows
**Mitigation**: Consolidation-before-discovery is only triggered when BOTH conditions are true:
1. `weakest_boundary == "incomplete_refactoring"`
2. `dal_coverage < 0.80`

Existing workflows unaffected if these conditions don't apply.

---

## 10. Success Criteria (Deployment-Ready)

✅ **Passes Validation**:
- Improved skills detect dual-path divergence on Metamorfose Finance
- Detection occurs in Step 2-3 (unknowns/diagnosis), not Step 4
- Problem description is specific and actionable
- Recommendation is consolidation-before-discovery with clear justification

✅ **Zero Regressions**:
- All 21 existing test cases pass without modification
- No changes to artifact contracts or validator stack
- No breaking changes to existing skill outputs

✅ **Generalizable**:
- Same questions apply to 3-5 different repo types
- No false positives for legitimate migrations (high test coverage + deprecation plan)
- Heuristics prove applicable across domains

✅ **Documented**:
- Usage research report explains findings
- Improvement plan documents what was changed and why
- Meta-learning documentation enables future iterations

---

## 11. Timeline & Next Steps

### Immediate (Today - May 18)
- [x] Complete skill improvements (Tasks 2.2a-2.2d of Workflow 2)
- [x] Create this improvement plan document (Task 3.1a of Workflow 3)
- [ ] Create validation test suite (Task 3.2a of Workflow 3) ← **NEXT**

### Short Term (May 19-20)
- [ ] Run baseline comparison against May 18 analysis
- [ ] Measure improvement metrics
- [ ] Validate on non-Metamorfose repos

### Before Deployment
- [ ] Complete all 3 validation workflows
- [ ] Create improvement summary report
- [ ] Archive results in .validation-cache/

### Post-Deployment
- [ ] Monitor effectiveness in real-world skill runs
- [ ] Tune thresholds based on additional data points
- [ ] Refine pattern detection based on false positives/negatives

---

## Conclusion

**This skill improvement plan is ready for implementation and validation.**

The improvements are:
- ✅ Based on real evidence (May 17 vs. May 18 analysis)
- ✅ Generalizable across domains (not Metamorfose-specific)
- ✅ Low-risk (additive, no logic replacement)
- ✅ Reversible (can be removed if issues arise)
- ✅ Valuable (detect worse problems earlier, enable better recommendations)

**Next action**: Create validation test suite and run baseline comparison to prove improvements work as expected.
