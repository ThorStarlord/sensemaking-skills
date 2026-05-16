# Implementation Issues: Complete Execution Mode Coverage

Generated from PRD via to-issues skill  
Date: 2026-05-16

---

## Issue 1: Prepare Orchestration Infrastructure for Live Mode Proving

### What to build

Fix orchestration-runner.py to support non-interactive gate handling, ensuring all validators are available, and documenting artifact contract locations for the mode-proving workflow sequence.

**Key tasks**:
1. Modify `_manage_gate()` to handle missing TTY gracefully when `--gate-decision` flag is set
2. Verify all 5 Level-3 validators are present and callable
3. Create artifact contract reference for each workflow
4. Document expected artifacts and validator stacks for each mode

### Acceptance criteria

- [ ] orchestration-runner.py accepts `--gate-decision auto-approve` and runs without hang in non-TTY environment
- [ ] All 5 Level-3 validators (validate-plan.py, validate-prompt-handoff.py, validate-skill-improvement-plan.py, validate-usage-research-report.py, validate-brief.py) are confirmed working
- [ ] Artifact paths for all workflows resolve correctly per ARTIFACT_CONTRACTS.md
- [ ] Pre-flight checks pass for `fast-local-diagnostic` and `docs-contract-reconciliation` workflows

### Blocked by

None - can start immediately

---

## Issue 2: Prove `plan_only` Execution Mode with Live Plan Validator

### What to build

Execute the `fast-local-diagnostic` workflow in `plan_only` mode, exercising `validate-plan.py` on a real artifact for the first time. Verify plan generation works and validator catches errors (or confirms plan is valid).

**Expected outcome**: Run log showing plan_only execution with validate-plan.py invoked and passed.

### Acceptance criteria

- [ ] `orchestration-runner.py fast-local-diagnostic --mode plan_only` completes without error
- [ ] Artifact `plan_fast-local-diagnostic.md` is produced with Section 11 (machine-readable plan) populated
- [ ] Run log shows `validate-plan.py` invoked and result (PASSED or FAILED with reason)
- [ ] Run log recorded in mode-coverage.yaml with validator invocation details

### Blocked by

- Issue 1: Prepare Orchestration Infrastructure

---

## Issue 3: Prove `prompt_chain` Execution Mode with Live Handoff Validator

### What to build

Execute the `fast-local-diagnostic` workflow in `prompt_chain` mode, exercising `validate-prompt-handoff.py` on real artifact (copy-paste prompts). Verify prompt generation works and prompts are properly validated.

**Expected outcome**: Run log showing prompt_chain execution with validate-prompt-handoff.py invoked and passed.

### Acceptance criteria

- [ ] `orchestration-runner.py fast-local-diagnostic --mode prompt_chain` completes without error
- [ ] Artifact `prompt_handoff` is produced with all required sections (copy-paste blocks)
- [ ] Run log shows `validate-prompt-handoff.py` invoked and result (PASSED or FAILED with reason)
- [ ] Run log recorded in mode-coverage.yaml with validator invocation details

### Blocked by

- Issue 1: Prepare Orchestration Infrastructure

---

## Issue 4: Complete `guided_execution` Full Cycle Step 2 with Gate Approvals

### What to build

Complete Step 2 of `docs-contract-reconciliation` workflow in `guided_execution` mode with explicit human gate approval. This produces the `docs_contract_reconciliation_report` artifact and exercises gate approval infrastructure for the first time in a real run.

**Expected outcome**: Step 2 completes with gate approval recorded in run log.

### Acceptance criteria

- [ ] `orchestration-runner.py docs-contract-reconciliation --mode guided_execution` continues from Step 1 (pre-existing)
- [ ] Step 2 completes and produces `docs_contract_reconciliation_report` artifact
- [ ] Run log shows gate `review_reconciliation_patch` with `gate_result: approved_by_user` and timestamp
- [ ] Gate approver name captured in run log
- [ ] All validators invoked on produced artifact

### Blocked by

- Issue 1: Prepare Orchestration Infrastructure

---

## Issue 5: Complete `guided_execution` Full Cycle Step 3 & Final Handoff

### What to build

Complete Step 3 of `docs-contract-reconciliation` workflow in `guided_execution` mode, producing final `prompt_handoff` artifact with gate approval. This completes the first full guided_execution workflow cycle with all gate infrastructure exercised.

**Expected outcome**: Full workflow completes with all gates approved and final handoff prompt validated.

### Acceptance criteria

- [ ] Step 3 completes after Step 2 approval (see Issue 4)
- [ ] Step 3 produces `prompt_handoff` artifact with all sections populated
- [ ] Run log shows gate `review_next_prompt` with `gate_result: approved_by_user` and timestamp
- [ ] Final run log shows all 3 steps PASSED with gate decisions recorded
- [ ] Mode coverage records first complete `guided_execution` workflow cycle

### Blocked by

- Issue 4: Complete `guided_execution` Full Cycle Step 2

---

## Issue 6: Prove `autonomous_execution` Mode with Automated Gates

### What to build

Execute the `fast-local-diagnostic` workflow in `autonomous_execution` mode with automated gate approvals (no human intervention). Verify gates work with automated approval policy and all artifacts produced.

**Expected outcome**: Full workflow completes with all gates auto-approved.

### Acceptance criteria

- [ ] `orchestration-runner.py fast-local-diagnostic --mode autonomous_execution` completes without human intervention
- [ ] All steps produce expected artifacts
- [ ] Run log shows all gates with `gate_result: automated_approval` (not manual approval)
- [ ] Run log recorded in mode-coverage.yaml with automated gate decision details
- [ ] All validators invoked and passed

### Blocked by

- Issue 1: Prepare Orchestration Infrastructure

---

## Issue 7: Prove `yolo_execution` on New Workflow (Full Pipeline)

### What to build

Execute the `full-local-sensemaking` workflow (4 steps) in `yolo_execution` mode, which bypasses all gates and runs at full speed. This proves the full automation pipeline end-to-end on a diverse workflow with complete mutation.

**Expected outcome**: All 4 steps complete with final `prompt_handoff` produced.

### Acceptance criteria

- [ ] `orchestration-runner.py full-local-sensemaking --mode yolo_execution` completes all 4 steps
- [ ] Final artifact `prompt_handoff` produced with all sensemaking outputs
- [ ] Run log shows all gates with `gate_result: bypassed` (YOLO mode)
- [ ] All validators invoked on all artifacts
- [ ] Run log recorded in mode-coverage.yaml with YOLO-specific behavior noted

### Blocked by

- Issue 1: Prepare Orchestration Infrastructure

---

## Issue 8: Implement Repeatable Failure Boundary Analysis

### What to build

Enhance `analyze-run-failures.py` to track failure patterns across independent runs. Identify which failures recur (repeatable boundaries = candidates for systemic hardening) vs. isolated incidents (artifact-level fixes). Create a failure pattern report.

**Expected outcome**: Analysis showing which failure classes are repeatable and which are single-occurrence.

### Acceptance criteria

- [ ] `analyze-run-failures.py` scans all run logs from Issues 2-7 
- [ ] For each error/validator failure, tracks: error_class, count, runs_affected, recurrence_pattern
- [ ] Generates failure_pattern_report.md showing repeatable vs. isolated failures
- [ ] Flags failures occurring in 2+ independent runs as "repeatable boundary candidates"
- [ ] Report recommends no hardening if zero repeatable failures found (per hardening policy)

### Blocked by

- Issue 2: Prove `plan_only` Execution Mode
- Issue 3: Prove `prompt_chain` Execution Mode
- Issue 4: Complete `guided_execution` Step 2
- Issue 5: Complete `guided_execution` Step 3
- Issue 6: Prove `autonomous_execution` Mode
- Issue 7: Prove `yolo_execution` on New Workflow

---

## Issue 9: Create Mode/Validator/Gate Coverage Dashboard

### What to build

Aggregate all mode-proving run logs into a coverage dashboard showing which modes are proven, which validators have been invoked live, which gate types have been exercised, and what repeatable failures exist. Single source of truth for "production readiness."

**Expected outcome**: coverage_dashboard.md showing all coverage metrics and production readiness status.

### Acceptance criteria

- [ ] Dashboard shows mode coverage: % of 5 modes with 1+ live run (target: 100%)
- [ ] Dashboard shows validator coverage: % of validators invoked on real artifacts (target: 100% of Level-3 validators)
- [ ] Dashboard shows gate coverage: all gate types (approval, denial, bypass, automated) with run counts
- [ ] Dashboard shows repeatable failure count and status (target: 0 blocking failures)
- [ ] Dashboard includes summary statement: "PRODUCTION READY" or blockers requiring fixes
- [ ] Linked from README.md

### Blocked by

- Issue 8: Implement Repeatable Failure Boundary Analysis

---

