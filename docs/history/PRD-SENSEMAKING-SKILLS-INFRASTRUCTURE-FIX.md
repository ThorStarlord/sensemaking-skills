# Product Requirements Document: Sensemaking Skills Infrastructure Stabilization

**Date:** 2026-05-29  
**Status:** Pending Approval  
**Author:** Autonomous Workflow  

---

## 1. Executive Summary

This PRD addresses four structural gaps in the sensemaking skills framework identified during Phase 4 testing. These gaps cause ad-hoc format drift, manual coordination overhead, and lack of automated validation. Fixing them removes blockers to production rollout without changing skill behavior — only adding contracts, validators, and documentation.

**Deliverables:**
- Evidence rules dual-mode rendering (investigative + durable)
- Documented decision criteria for direct skill execution vs. orchestration
- Automated skill-hygiene validator (npm, registry, artifact contracts)
- Four artifact-contract schemas (PRD, issue_list, agent_brief, code_patch)

**Timeline:** 2 days  
**Effort Estimate:** 2.75 person-days (breakdown per feature)

---

## 2. User Goal

From `00-user-intent.md`: Fix four structural gaps in the sensemaking skills system to stabilize the framework for production deployment.

---

## 3. Goal Preservation & Expansion

**Goal Preservation:** `exact_match`  
**Scope Expansion Proposed:** `false`

This PRD addresses exactly the four gaps the user identified. No scope expansion beyond user's stated goal.

---

## 4. Features

### Core Feature 1: Evidence Rules Dual-Mode Rendering

**What it solves:** Downstream skills (to-prd, workflow-orchestrator, prompt-handoff) currently strip line numbers manually. With 4+ consumers, this leads to duplicate transform logic and format drift.

**What changes:**

| File | Change | Reason |
|------|--------|--------|
| `repo-sensemaker/references/evidence-rules.md` | Add section documenting two output modes: `investigative` (file + line numbers) and `durable` (file paths only, grep-verifiable) | Consumers need to know which mode they're getting |
| `repo-analysis-template.md` Section 7 | Add YAML frontmatter: `<!-- mode: investigative \| durable -->` | Allow template to signal which mode is expected |
| `prompt-handoff/` consumer docs | Document that durable mode outputs can be safely cited in PRDs without staleness risk | Explain why mode matters downstream |

**Acceptance Criteria:**
- [ ] Evidence rules doc lists both modes with examples
- [ ] Template can toggle between modes via frontmatter
- [ ] Downstream consumer docs explain mode implications
- [ ] Test: repo-sensemaker produces both modes on demand

**Effort Estimate:** 0.5 days

---

### Core Feature 2: Execution Mode Decision Criteria

**What it solves:** User instruction "don't wait for my approval" doesn't fit existing execution modes (autonomous_execution requires gates; yolo_execution requires ceremony). Need documented criteria for when to skip orchestration entirely.

**What changes:**

| File | Change | Reason |
|------|--------|--------|
| `docs/AGENTS.md` new section | Add "Agent Decision Tree: When to invoke orchestrator vs. direct skill execution" with three heuristics | Document when orchestration is optional/required |
| `workflow-orchestrator/references/execution-modes.md` | Add context note: "For decisions to *skip* orchestration, see AGENTS.md decision tree" | Keep orchestrator modes clean; execution-modes only covers within-orchestration modes |

**Decision Criteria:**
- 1-3 skills in sequence → direct execution optional (lower overhead)
- 4+ skills → orchestrator recommended (context carriage, gates, logs)
- User says "don't wait" → direct execution allowed even at 4+ (override)

**Acceptance Criteria:**
- [ ] Decision tree is documented in AGENTS.md with clear criteria
- [ ] Context note in execution-modes.md points to decision tree
- [ ] Example: "TDD on single issue" uses direct execution; "orchestrate 6 downstream skills" uses orchestrator

**Effort Estimate:** 0.25 days

---

### Core Feature 3: Skill-Hygiene Validator (v1)

**What it solves:** Skills reference npm scripts, skill IDs, and artifact contracts that may not exist. Manual review catches these late; automation catches them before commit.

**What changes:**

| File | Change | Reason |
|------|--------|--------|
| `scripts/validate-skill-hygiene.mts` (new) | Implement three checks: npm scripts exist, skill IDs cross-ref, artifact refs resolve | Deterministic, high-signal checks |
| `package.json` | Add `"validate:skills": "tsx scripts/validate-skill-hygiene.mts"` | Enable `npm run validate:skills` |
| CI/pre-commit | Hook validates before merge | Prevent drift in main |

**Three checks (v1):**

1. **npm script validation:** Every citation of `npm run X` in AGENTS.md must exist in package.json
2. **Skill-registry cross-ref:** Every step in workflow-registry.yaml that references a skill ID must exist in skill-registry.yaml
3. **Artifact-contract validation:** Every input/output_artifact ref in skill registry must exist in artifact-contracts.yaml

**Deferred (Phase 5):** File-path globs, slash-commands, env vars (too fragile or low-signal)

**Acceptance Criteria:**
- [ ] Script runs without error on current codebase
- [ ] Detects missing npm script (test: add ref to nonexistent script, run validator, confirm failure)
- [ ] Detects missing skill ID (test: add workflow step with fake skill, confirm failure)
- [ ] Detects missing artifact contract (test: add artifact ref not in contracts.yaml, confirm failure)
- [ ] Can be run via `npm run validate:skills`

**Effort Estimate:** 0.5 days

---

### Core Feature 4: Artifact-Contract Schemas (PM/Engineering Pipeline)

**What it solves:** UI pipeline has complete contracts; PM/engineering pipeline (PRD → issues → brief → code) is ad-hoc. Downstream validators (to-issues, triage, tdd) have no formal contracts to validate against.

**What changes:**

| File | Change | Reason |
|------|--------|--------|
| `workflow-orchestrator/references/artifact-contracts.yaml` | Add four new artifact entries: `prd`, `issue_list`, `agent_brief`, `code_patch` | Document required structure for each artifact |

**Schema for each artifact:**

```yaml
- id: prd
  produced_by: to-prd
  consumed_by: [to-issues, workflow-orchestrator, docs-sync]
  required_sections:
    - executive_summary
    - user_goal
    - features (with acceptance_criteria per feature)
    - out_of_scope
    - acceptance_criteria
  required_machine_fields:
    - prd_id
    - date
    - status
    - source_intent_ref
    - user_goal_preserved_as

- id: issue_list
  produced_by: to-issues
  consumed_by: [triage, tdd, workflow-orchestrator]
  required_sections:
    - issues (ordered list with dependencies)
  per_issue:
    - issue_id
    - title
    - effort_estimate (P0/P1/P2 or days)
    - acceptance_criteria (list)
    - parallelizable (boolean)
  required_machine_fields:
    - parent_prd_id
    - total_effort_estimate
    - created_date

- id: agent_brief
  produced_by: triage
  consumed_by: [tdd, workflow-orchestrator, prompt-handoff]
  required_sections:
    - agent_brief_id
    - task (concise statement)
    - context (background needed)
    - instructions (ordered steps)
    - acceptance_criteria (testable)
    - expected_output (artifact type)
  required_machine_fields:
    - parent_issue_id
    - effort_estimate
    - required_skills (list)
    - created_date

- id: code_patch
  produced_by: tdd
  consumed_by: [verification-loop, workflow-orchestrator]
  required_sections:
    - files_created (list)
    - files_modified (list with test results)
    - test_summary (pass/fail counts)
  required_machine_fields:
    - parent_brief_id
    - test_count
    - test_pass_count
    - test_fail_count
    - created_date
```

**Schema derivation:** From intersection of actual Phase 4 artifacts (PRD-2026-05-27-PHASE-4-OPERATIONAL-RESILIENCE.md + PRD-docs-implementation-drift-repair.md). Legacy artifacts marked "pre-schema."

**Acceptance Criteria:**
- [ ] All four schemas added to artifact-contracts.yaml
- [ ] Schema is valid YAML and parseable
- [ ] `to-issues` can consume `prd` artifact without errors
- [ ] `tdd` can consume `agent_brief` without errors
- [ ] Validator (Feature 3) can cross-ref these schemas

**Effort Estimate:** 0.75 days

---

## 5. Out of Scope

- **Skill behavior changes:** This PRD adds contracts and documentation, not new skill functionality
- **Orchestrator code refactoring:** Execution-mode decision lives in docs, not code
- **Retroactive schema validation:** Legacy artifacts (pre-schema) are not retrofitted; forward validation starts with next runs
- **Glob-matching file-path validation:** Deferred to Phase 5 after npm/registry/contract checks prove stable
- **Slash-command validation:** Requires runtime context; deferred indefinitely

---

## 6. Acceptance Criteria (Test Plan)

**Feature 1: Evidence Modes**
- [ ] Evidence rules doc can be read without errors
- [ ] Template render works with both `investigative` and `durable` mode flags
- [ ] Downstream consumer (e.g., to-prd) successfully strips line numbers in durable mode

**Feature 2: Execution Criteria**
- [ ] AGENTS.md has documented decision tree
- [ ] Decision tree includes examples for 1-3 skills, 4+ skills, and "don't wait" override
- [ ] Context note in execution-modes.md is clear and not duplicative

**Feature 3: Skill-Hygiene Validator**
- [ ] `npm run validate:skills` completes without error on current codebase
- [ ] Deliberate errors (bad npm script, bad skill ID, bad artifact ref) are caught
- [ ] Error messages are actionable (point to file + line where ref appears)

**Feature 4: Artifact Contracts**
- [ ] All four schemas in artifact-contracts.yaml are valid YAML
- [ ] `to-issues` reads PRD schema without validation errors
- [ ] `tdd` reads agent_brief schema without validation errors
- [ ] Validator (Feature 3) detects missing artifact contracts

---

## 7. Non-Functional Requirements

| Requirement | Details |
|---|---|
| **Windows Compatibility** | All scripts (validator, docs) must run on Windows 10+ (cp1252 encoding, PowerShell + Bash compatible) |
| **Documentation Clarity** | All new sections in docs must have examples (not just prose) |
| **Validation Performance** | `validate:skills` must complete in < 2 seconds on full codebase |
| **Backward Compatibility** | Existing skills continue to work; new contracts are validated on *new* artifacts only |

---

## 8. Approval Gate

**Scope Expansion Status:** `exact_match`  
**User Approval Required:** No

This PRD addresses exactly the four gaps proposed. No approval needed to proceed.

---

## 9. Machine-Readable Handoff

```yaml
# Artifact Contract: PRD
artifact_id: PRD-SENSEMAKING-SKILLS-INFRASTRUCTURE-FIX
artifact_type: prd
source_intent_ref: ../../00-user-intent.md
user_goal_preserved_as: exact_match
scope_expansion_proposed: false
scope_expansion_status: exact_match
parent_workflow: autonomous_execution
created_date: 2026-05-29
status: pending_implementation
features:
  - id: evidence_dual_mode
    effort_days: 0.5
    files_to_change:
      - path: repo-sensemaker/references/evidence-rules.md
        change_type: document
      - path: repo-analysis-template.md
        change_type: document
  - id: execution_decision_criteria
    effort_days: 0.25
    files_to_change:
      - path: docs/AGENTS.md
        change_type: document
      - path: workflow-orchestrator/references/execution-modes.md
        change_type: document
  - id: skill_hygiene_validator
    effort_days: 0.5
    files_to_change:
      - path: scripts/validate-skill-hygiene.mts
        change_type: create
      - path: package.json
        change_type: modify
  - id: artifact_contracts_pm_engineering
    effort_days: 0.75
    files_to_change:
      - path: workflow-orchestrator/references/artifact-contracts.yaml
        change_type: modify
total_effort_estimate_days: 2.0
downstream_consumer: to-issues
```

---

**Next Steps:** to-issues skill will consume this PRD to create an issue list with dependencies and parallelization plan.
