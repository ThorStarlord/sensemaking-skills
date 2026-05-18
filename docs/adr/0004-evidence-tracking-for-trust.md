# ADR 0004: Evidence Tracking for Trust

**Status**: Accepted  
**Date**: 2026-05-18  
**Context**: Phase 4 Implementation  
**Decision**: Record which validators exercised which artifacts and which gates approved steps to create an audit trail proving the system works

---

## Context

The orchestration system executes workflows, validates artifacts, and enforces approval gates. But without evidence, there's no way to know:
- Which validators actually ran?
- Which gates were checked?
- Did the system catch problems or just get lucky?
- Can we trust this output?

**Example of Missing Evidence:**
1. Workflow runs to completion (success!)
2. But did artifacts actually get validated?
3. Or did validation skip silently?
4. Did gates actually approve, or were they auto-approved?
5. How do we know the system worked as designed?

**The Trust Problem:**
- Users can't verify the system is trustworthy
- New operators don't know what's been validated
- If a problem surfaces later, no audit trail to show what was checked

---

## Decision

### Core Rule
**Record machine-produced evidence proving the system worked as designed.**

### What to Track

For every workflow execution, record:

1. **Workflow & Execution Mode**
   - workflow_id: product-to-issues
   - mode: guided_execution
   - last_run: 2026-05-17

2. **Steps Executed**
   - steps_completed: 3
   - steps_total: 3

3. **Validators Exercised**
   - level_1: validate-repo.py (repository-wide checks)
   - dispatcher: validate-output.py (artifact-specific validation)
     - For prd: validate-artifact.py (generic) + validate-prd.py (specific)
     - For issue_list: validate-artifact.py (generic) + validate-issues.py (specific)
     - For agent_brief: validate-artifact.py (generic) + validate-brief.py (specific)

4. **Gates Exercised**
   - gates_exercised: true
   - gates_note: 3 approved, 0 denied
   - For each gate: decision (approved/denied), who approved, when

5. **Hardening Triggered**
   - hardening_triggered: none
   - Indicates if validators discovered issues requiring infrastructure changes

### Implementation

**File: docs/mode-coverage.yaml**

```yaml
# Evidence tracker for orchestration system
# Machine-produced proof that workflows execute correctly

- mode: guided_execution
  workflow_id: product-to-issues
  last_run: '2026-05-17'
  run_log_path: artifacts/run_log_product-to-issues_guided_execution.md
  
  steps_completed: 3
  steps_total: 3
  
  validators_exercised:
    - level_1: validate-repo.py
    - dispatcher: validate-output.py (prd)
    - dispatcher: validate-output.py (issue_list)
    - dispatcher: validate-output.py (agent_brief)
  
  gates_exercised: true
  gates_note: 3 approved, 0 denied
  
  hardening_triggered: none
  
  notes: |
    Full pipeline proven end-to-end.
    All 3 artifacts validated through dispatcher.
    All 3 gates approved by human reviewers.
    Zero validators suggested hardening.
    System is working as designed.
```

### Where Evidence Comes From

Evidence should be **machine-produced** by orchestration-runner.py:

1. **Step Execution**: Runner records which steps executed (automatically)
2. **Validator Invocation**: Runner logs which validators ran for which artifacts (automatically)
3. **Gate Decisions**: Run log records which gates were presented and how users responded (during execution)
4. **Hardening Suggestions**: Validators can suggest hardening (through error codes)

Evidence should NOT be hand-written (except for historical entries).

---

## Consequences

### Positive
1. **Verifiable Trust**: Point to evidence proving validators ran and gates approved
2. **New Operator Confidence**: "What's been validated?" → Look at mode-coverage.yaml
3. **Problem Investigation**: "Did this artifact get validated?" → Check run log
4. **System Improvement**: "Are validators actually catching issues?" → Analyze hardening_triggered trends
5. **Compliance**: Audit trail showing what was checked and who approved

### Negative
1. **Extra Recording**: Orchestrator must track more data (small performance cost)
2. **Evidence Stale**: If you re-run a workflow with same code, do you update evidence?
3. **Privacy Concerns**: Recorded gates show who approved/denied (may be sensitive)

### Trade-offs
- We chose **recorded evidence over no evidence** because:
  - Trust only comes from verifiable proof
  - The cost of recording (small performance hit) is worth the benefit (verified trustworthiness)

---

## Alternatives Considered

### Alternative 1: No Evidence Tracking
- Don't record which validators ran or gates approved
- **Rejected because**: No way to verify system works; users can't trust it
- **Consequence**: System seen as a black box; users skeptical

### Alternative 2: Evidence Only on Failure
- Record evidence only when something breaks
- **Rejected because**: No baseline of normal operation; hard to prove system works in steady state
- **Consequence**: Users don't know if success was due to validation or luck

### Alternative 3: Optional Evidence
- Let each workflow choose whether to record evidence
- **Rejected because**: Inconsistent; some workflows trusted, others not; hard to reason about
- **Consequence**: Confusing mixed evidence

### Alternative 4: Detailed Post-Execution Analysis
- Run full analysis after workflow completes (verbose, detailed)
- **Rejected because**: Expensive; slow workflow completion; delayed feedback
- **Consequence**: Workflows take longer; analysis results not immediately available

---

## Evidence

This decision was validated during Phase 4:

### Before Evidence Tracking
- Workflows ran to completion
- But: No record of which validators checked which artifacts
- But: No clear record of which gates approved/denied
- Result: Users had no proof the system worked as designed

### After Evidence Tracking
- mode-coverage.yaml records all workflow executions
- Each entry shows: validators_exercised, gates_exercised, hardening_triggered
- Run logs link to detailed step-by-step execution records
- **Result**: Users can point to evidence proving the system works

### Real-World Validation
- product-to-issues workflow: 3 steps completed, 3 validators exercised, 3 gates approved
- docs-architecture workflow: 2 steps completed, 2 validators exercised, 2 gates approved
- Zero hardening triggered across all runs
- Proof: System is working as designed (not by luck)

---

## Implications for Future Decisions

1. **Orchestrator Design**: Runner must log validators and gates (non-negotiable)
2. **Evidence Requirements**: Every production workflow run must produce evidence entry
3. **Hardening Philosophy**: Only add infrastructure when evidence shows it's needed (not theoretical)

---

## Related

- **Pattern**: See `orchestration-patterns.md` → Pattern 4: Evidence Tracking for Trust
- **Guide**: `workflow-design-guide.md` → Step 20: Document Your Workflow
- **Evidence**: `mode-coverage.yaml` — Actual evidence entries for all workflows
- **Prior Gap**: No clear record of what was validated in previous runs

---

## For Workflow Operators

**After running a workflow:**

1. Check the run log (`artifacts/run_log_*.md`)
2. Verify: Which steps ran?
3. Verify: Which validators were exercised?
4. Verify: How did gates respond?
5. Update mode-coverage.yaml with the evidence:
   - workflow_id, mode, last_run
   - steps_completed, steps_total
   - validators_exercised (list each validator)
   - gates_exercised, gates_note
   - hardening_triggered
   - notes summarizing what was proven

**Example entry:**
```yaml
- mode: guided_execution
  workflow_id: product-to-issues
  last_run: '2026-05-18'
  steps_completed: 3
  steps_total: 3
  validators_exercised:
    - level_1: validate-repo.py
    - dispatcher: validate-output.py (prd)
    - dispatcher: validate-output.py (issue_list)
    - dispatcher: validate-output.py (agent_brief)
  gates_exercised: true
  gates_note: 3 approved, 0 denied
  hardening_triggered: none
  notes: "Full pipeline proven. All artifacts validated. All gates approved."
```

---

## Machine-Produced vs. Hand-Written Evidence

**Machine-Produced** (Good):
- Automatically logged by orchestration-runner.py
- Trustworthy (not subject to human error)
- Consistent format
- Complete (doesn't miss anything)

**Hand-Written** (Avoid):
- Typed manually into mode-coverage.yaml
- Subject to human error (typos, incorrect counts)
- Inconsistent format
- Incomplete (author might forget to record something)

**Exception**: Historical entries from before this ADR was written can be hand-authored (grandfathered in). Going forward, all new entries must be machine-produced.

---

## Acceptance Criteria

This decision is accepted when:
- ✓ mode-coverage.yaml records validators_exercised for all workflows
- ✓ mode-coverage.yaml records gates_exercised for all workflows
- ✓ mode-coverage.yaml records hardening_triggered for all workflows
- ✓ All entries in mode-coverage.yaml have associated run_log files
- ✓ Run logs are machine-produced by orchestration-runner.py
- ✓ Evidence clearly shows validators and gates were exercised
- ✓ Zero repeatable failures detected (correct state)

---

## Questions & Answers

**Q: How do I update evidence if I re-run the same workflow?**  
A: Update the last_run date and counts. If you discover a validator found a new issue, update gates_note. If hardening is needed, update hardening_triggered.

**Q: What if a validator fails—should I still record it?**  
A: Yes. Record it as a "validator failure" in the run log and gates_note (gate denied by validator). The evidence shows the system caught the problem.

**Q: How long do I keep evidence?**  
A: Keep all evidence in version control. It's part of the audit trail and helps identify trends (e.g., "this workflow always hits validator X").

**Q: What if evidence shows a validator never runs?**  
A: That's a discovery! It means either:
- The validator isn't configured for that artifact type
- The validator was supposed to run but didn't
- You found a hardening need: add the validator

**Q: Can evidence be private or anonymized?**  
A: Run logs are part of the repository (public), so assume they'll be readable. If gate decisions include sensitive info (who approved), consider redacting names but keeping counts (3 approved, 0 denied).
