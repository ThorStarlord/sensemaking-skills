# Extracted Heuristics from May 18 Analysis
## New Patterns for Detecting Dual-Path Divergence & Incomplete Refactoring

**Date**: 2026-05-18  
**Source**: Full Fog Path execution on Metamorfose Edutech finance system  
**Purpose**: Inform skill improvements to detect this class of problem earlier  

---

## Executive Summary

Three new heuristics were extracted from the May 18 escalation analysis. These patterns detect **dual-path divergence** (incomplete refactoring with coexisting patterns) before it becomes a critical risk.

**Goal**: Detect these patterns in Step 2 (unknowns-mapper) or Step 3 (repo-sensemaker), not Step 4 (orchestrator).

---

## Heuristic 1: Coexisting Data Access Patterns
### Description
A codebase has two different ways to access the same data (old pattern + new pattern), and both are actively used.

### Detection Signal
```
EXISTS(direct_supabase_query("table_X")) AND EXISTS(dal_wrapper("table_X"))
AND both_are_used_in_production
```

### Example
```
// Old way (direct Supabase):
supabase.from("financial_transactions").select("amount,transaction_type")

// New way (DAL wrapper):
getTransactionMetrics(supabase, { startDate, endDate })

// Both exist; aggregator still uses old way
```

### Why It Matters
When coexisting patterns both work, developers face ambiguity:
- Which pattern should I use for new code?
- Are both patterns equally correct?
- If I change one, should I change the other?

**Result**: Code diverges organically. No single "wrong" decision, but collectively they lead to inconsistency.

### How to Detect
1. **Code audit**: Search for direct table queries vs. DAL wrappers
2. **Usage analysis**: Map which modules use which pattern
3. **Configuration check**: Look for feature flags, version indicators
4. **Test coverage**: Are there tests comparing both patterns?

### Questions to Add to Unknowns-Mapper
**Primary**: "Are there coexisting patterns for accessing the same data (e.g., old abstraction layer + new abstraction layer)?"

**Follow-up**: 
- "Which modules use the old pattern?"
- "Which modules use the new pattern?"
- "Is there documentation about which pattern to use for new features?"
- "Are there tests comparing output from both patterns?"

### Risk Assessment Matrix
| Test Coverage | DAL Completion | Risk Level |
|---|---|---|
| Yes | >80% | Low (well-tested migration) |
| Yes | <80% | Medium (good tests, incomplete implementation) |
| No | >80% | Medium (complete but untested) |
| No | <80% | High (incomplete + untested) |

---

## Heuristic 2: Incomplete Refactoring (Low DAL Coverage)
### Description
A refactoring was started (new DAL layer, new abstractions) but not completed. The new pattern covers <80% of the data access points; the old pattern still handles the rest.

### Detection Signal
```
dal_coverage = (# of DAL functions with implementations) / (# of table access points)
dal_coverage < 0.80 → incomplete_refactoring = true
```

### Example
```
Table: financial_transactions
- Direct queries: 7 (in aggregator.ts)
- DAL wrappers: 0 (none yet)
- Coverage: 0%

Table: financial_month_closures  
- Direct queries: 2 (in aggregator.ts)
- DAL wrappers: 1 (getMonthClosures)
- Coverage: 50%

Total coverage: (1 DAL function) / (5 tables) = 20% INCOMPLETE
```

### Why It Matters
Incomplete refactoring creates **transition risk**:
- "New system is almost done, let's just use the old system for now"
- "Old system works fine, why change anything?"
- "New system is tested, but old system has edge cases we don't know about"

The code enters a **zombie state**: both systems coexist, but neither is fully maintained.

### How to Detect
1. **DAL audit**: Count implemented DAL functions vs. data access points
2. **Table mapping**: For each table, identify all access points (direct queries)
3. **Coverage calculation**: (# DAL functions) / (# tables) = coverage %
4. **Threshold check**: Coverage < 80% = incomplete

### Questions to Add to Repo-Sensemaker
**Primary**: "Does the codebase show signs of incomplete refactoring (new pattern started but not finished)?"

**Evidence to gather**:
- Which tables have DAL wrappers? Which don't?
- For tables with DAL wrappers, are they actually used or just implemented?
- Are there comments like "TODO: migrate to DAL" or "FIXME: use new pattern"?
- Is there a deprecation roadmap or migration plan?

### Coverage Assessment
```
Ideal:        >=80%  (nearly complete, finishing touches)
Concerning:   50-80% (halfway, needs focus)
High Risk:    <50%   (barely started, long way to go)
```

---

## Heuristic 3: Missing Consistency Tests
### Description
The codebase has both old and new patterns, but no tests verify that both produce identical results.

### Detection Signal
```
coexisting_patterns = true
consistency_tests = false
→ divergence_risk = true
```

### Example
```
// Old path in aggregator.ts:
const { data: transactions } = await supabase
  .from("financial_transactions")
  .select("amount,transaction_type");

// New path in Month Overview page:
const metrics = await getTransactionMetrics(supabase, {...});

// No test file: finance-consistency.test.ts
// No comparison: old_path_output vs. new_path_output
```

### Why It Matters
**Silent divergence**: Both systems appear to work, but data could diverge without warning.

Example drift scenario:
```
// Scenario: Bug fix in aggregator logic
const income = rows.filter(r => r.type === "income");  // OLD CODE

// Gets fixed to:
const income = rows.filter(r => r.type === "INCOME"); // Fixed (uppercase)

// New path already had uppercase in database query:
select ...where type = "INCOME" ...

// Result: OLD path broken, NEW path still works
// Bug detected late: in production, when users see inconsistency
```

### How to Detect
1. **Test file search**: Look for files named `*-consistency.test.*`
2. **Snapshot tests**: Are there snapshots comparing old vs. new paths?
3. **Data comparison**: Do tests run both paths on same data and assert equality?
4. **Coverage tracking**: What % of shared functionality has comparison tests?

### Questions to Add to Repo-Sensemaker
**Primary**: "Are there tests comparing the old and new implementations to verify they produce identical results?"

**Evidence to gather**:
- Do consistency test files exist?
- Do they test all major user journeys (happy path + error cases)?
- Do they verify data shape, not just presence?
- What's the test coverage for comparison scenarios?

### Test Checklist
```
□ Consistency test file exists
□ Tests both old and new paths on same input data
□ Compares output shapes (not just counts)
□ Tests error scenarios (invalid input, null data, etc.)
□ Snapshots are version-controlled
□ Tests run in CI/CD pipeline
□ Coverage >90% of shared functionality
```

---

## Heuristic 4: Absent Deprecation Plan
### Description
The codebase is in transition (old + new patterns coexist), but there's no documented plan for deprecating the old pattern.

### Detection Signal
```
coexisting_patterns = true
deprecation_plan = null
→ migration_risk = "indefinite"
```

### Example
```
Missing from docs:
- When will old pattern be removed?
- What's the migration path?
- Are there breaking changes?
- How will operators be notified?
- What's the rollback strategy?

Code status: "Both systems live simultaneously"
Expected end state: Undefined
Timeline: None
```

### Why It Matters
**Indefinite coexistence** means:
- Technical debt accrues forever
- Context switches for developers ("which pattern do I use?")
- New features fight two systems simultaneously
- Operator training covers both paths

Without a plan, the transition becomes **implicit and emergent** rather than **planned and deliberate**.

### How to Detect
1. **Documentation search**: Look for "deprecation", "migration", "sunset" in docs
2. **Roadmap check**: Is there a timeline document?
3. **Comments audit**: Are there TODOs with dates or milestones?
4. **Issue tracking**: Are there tickets for completing the refactoring?

### Questions to Add to Repo-Sensemaker
**Primary**: "Is there a documented plan for deprecating the old pattern and completing the migration?"

**Evidence to gather**:
- Deprecation roadmap document exists?
- Timeline is concrete (not "eventually")?
- Operator communication plan exists?
- Migration steps are documented?
- Rollback strategy is defined?

### Plan Checklist
```
□ Deprecation roadmap document exists
□ Timeline: When will old pattern be removed? (date TBD is not acceptable)
□ Operator communication: How will they learn?
□ Migration steps: What do developers do?
□ Rollback plan: What if we need to revert?
□ Test coverage: Is full migration tested before production?
□ Data migration: Any data needs to be migrated?
```

---

## Integration into Skills: Where Each Heuristic Fits

### Unknowns-Mapper (Step 2)
**Questions to add**:
```
Domain Understanding:
- "Are there coexisting patterns for accessing the same data?"
- "Which modules use the old pattern vs. new pattern?"

Research Paths:
- "Code audit: identify all data access patterns in codebase"
- "Determine: DAL coverage percentage"
- "Check: do consistency tests exist between patterns?"

Stopping Rule:
- "Stop when you've mapped coexisting patterns and identified risk"
```

### Repo-Sensemaker (Step 3)
**Weakness type to add**:
```
Weakness: "Incomplete Refactoring with Divergence Risk"

Detection Pattern:
1. Identify coexisting data access patterns (old + new)
2. Measure DAL coverage percentage
3. Check for consistency tests (present/absent)
4. Check for deprecation plan (documented/absent)

Risk Factors:
- DAL coverage <50% = HIGH risk
- No consistency tests = HIGH risk
- No deprecation plan = HIGH risk

Recommended Action:
- Complete refactoring and consolidate patterns
- Add consistency tests
- Document deprecation plan
```

### Workflow-Orchestrator (Step 4)
**Decision rule to add**:
```
IF (sensemaking_brief.weakest_boundary == "incomplete_refactoring") THEN
  IF (dal_coverage < 0.80) THEN
    recommend_workflow = "consolidation"  // Complete the refactoring first
    recommended_execution_mode = "guided"  // Human gates for architecture decisions
  ELSE
    recommend_workflow = "discovery"  // Complete refactoring already done
  END
ELSE
  // Apply existing routing logic
END
```

---

## Validation Criteria

These heuristics should:

1. **Detect earlier**: Find the pattern in Step 2-3 (unknowns/repo), not Step 4 (orchestrator)
2. **Be specific**: Name the exact weakness (incomplete refactoring, not just "complex code")
3. **Enable action**: Provide clear next steps (complete DAL, add tests, document plan)
4. **Generalize**: Work across repos, not just Metamorfose Finance
5. **Avoid false positives**: Don't flag legitimate transitional states

---

## Test Scenarios for Validation

### Scenario 1: Metamorfose Finance (Dual-Path Divergence)
**Expected detection**: Step 3 (repo-sensemaker) identifies "incomplete refactoring"
**Test**: Run updated skills on Metamorfose Finance
**Result**: Recommends consolidation-before-discovery

### Scenario 2: Clean Refactoring (Good Example)
**Setup**: New DAL layer, all queries migrated, old code removed, tests comprehensive
**Expected detection**: Step 2 reports "no coexisting patterns", research_needed = false
**Test**: Run on well-completed refactoring
**Result**: No high-risk signals, allows discovery workflow

### Scenario 3: Early-Stage Refactoring (Acceptable Risk)
**Setup**: New DAL layer, 30% coverage, but excellent test coverage and documented deprecation plan
**Expected detection**: Step 3 identifies incomplete refactoring, but with low risk due to tests/plan
**Test**: Run on intentional WIP refactoring
**Result**: Identifies risk correctly, but severity is "medium" not "critical"

---

## Next Steps

1. **Skills Implementation** (Workflow 2.2a-2.2d)
   - Add questions to unknowns-mapper SKILL.md
   - Add weakness type to repo-sensemaker SKILL.md
   - Add decision rule to workflow-orchestrator SKILL.md

2. **Validation** (Workflow 3)
   - Test heuristics on Metamorfose Finance (should detect earlier)
   - Test on 2-3 other projects to validate generalization
   - Measure false positive rate

3. **Threshold Tuning** (Future runs)
   - Is 80% DAL coverage the right threshold?
   - Should absence of deprecation plan always be flagged?
   - Do the heuristics work on different architecture styles (monolithic, microservices, etc.)?

---

## Summary Table

| Heuristic | Detection Method | Risk Signal | Added To Skill |
|-----------|---|---|---|
| **Coexisting Patterns** | Code audit + usage analysis | Two ways to access same data | unknowns-mapper + repo-sensemaker |
| **Incomplete Refactoring** | DAL coverage < 80% | New pattern barely started | unknowns-mapper + repo-sensemaker |
| **Missing Tests** | Test file search + coverage analysis | No consistency validation | repo-sensemaker |
| **No Deprecation Plan** | Documentation search | Indefinite coexistence | repo-sensemaker |

