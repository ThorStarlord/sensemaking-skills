# ALL-SKILLS-TEST-PLAN (Production Ready)

This plan defines a non-interfering verification suite for the Sensemaking Skills ecosystem. It is designed for parallel execution with strict boundary enforcement and machine-auditable run logs.

## 1. Test Strategy

| Strategy | Scope | Goal | Verification Method |
| :--- | :--- | :--- | :--- |
| **Isolated Skill Tests** | Single Skill | Verify logic compliance with `SKILL.md` boundary rules. | Fixed Input fixture -> Isolated Output artifact. |
| **Handoff Tests** | Two Skills | Verify that generated artifact $A$ satisfies consumer $C$. | Generated Output $A$ -> Consumer Input $C$. |
| **End-to-End Chain Tests** | Full Pipeline | Verify semantic thread from raw fog to final prompt. | Chain execution (Fog -> Handoff). |
| **Maintenance Safety Tests** | Meta-Skills | Verify defect classification without blind patching. | Adversarial fixture testing (Scenario 005). |

## 2. File Ownership Matrix

| Task Category | Allowed Write Paths | Forbidden Write Paths |
| :--- | :--- | :--- |
| **Isolated Tests** | `examples/skill-tests/[skill-name]/**` | See Section 3 (Danger List) |
| **Handoff Tests** | `examples/skill-tests/handoff/**` | See Section 3 (Danger List) |
| **Full Chain** | `examples/skill-tests/full-chain/001-cold-start/**`| See Section 3 (Danger List) |
| **Maintenance** | `examples/skill-tests/maintenance/**` | See Section 3 (Danger List) |

## 3. Shared-File Danger List (DO NOT EDIT)

The following paths are strictly **READ-ONLY** for all verification tasks. No task may modify these files:

- `skills/**/SKILL.md` (Core instructions)
- `scripts/**` (Validation logic)
- `docs/**` (Architecture and PRDs)
- `examples/usage-research/**` (Scenario fixtures)
- `workflow-registry.yaml` / `skill-registry.yaml` (Registries)
- `walkthrough/**` / `status/**` (Maintenance/audit docs)
- `README.md` / `CONTEXT.md`
- `examples/pipeline/**` (Fixed input fixtures)

## 4. Execution & Merge Order

1.  **Phase 1: Read-only Audits** (Observation only).
2.  **Phase 2: Isolated Output Artifacts** (Independent skill verification).
3.  **Phase 3: Handoff & Full-chain Tests** (Inter-skill consistency).
4.  **Phase 4: Maintenance Safety Tests** (Defect classification loop).
5.  **Phase 5: Status Update** (Only after all validation gates pass).

## 5. Anti-Causal Confusion Rule (Taxonomy Integration)

Before recommending any edit, classify the failure using the formal taxonomy:

### behavioral_failure_class (Docs: docs/philosophy/AGENTIC_FAILURE_MODES.md)
- **Class 1: Input Ambiguity**: User was too vague.
- **Class 2: Wrong Routing**: Chose the wrong skill/workflow.
- **Class 3: Artifact Weakness**: Generated thin or low-quality artifact.
- **Class 4: Handoff Failure**: Next agent can't use the output.
- **Class 5: Boundary Violation**: Agent ignored `Forbidden Edits`.
- **Class 6: Hallucinated Evidence**: Fact-check failed.
- **Class 7: Path Hygiene Error**: Absolute paths or `file:///` links used.
- **Class 8: Over-Maintenance**: Blindly patching correct logic for flawed tests.
- **Class 9: Validator Mismatch**: Script or Registry is stale/broken.
- **Class 10: Status Overclaiming**: Claimed "Done" but task incomplete.

### defect_source (Structural Root Cause)
- `fixture_defect`: Test fog or expected-behavior fixture is broken.
- `validator_defect`: Validation script has a bug.
- `registry_defect`: Metadata in skill/workflow registry is incorrect.
- `consumer_skill_defect`: The skill logic itself failed.
- `producer_artifact_defect`: The upstream artifact was low quality.


## 6. Per-Task Run Log Requirement

Every execution task must create a `TEST-RUN-LOG.md` in its assigned output directory. This log is the source of truth for the verification step.

| Field | Description | Required |
| :--- | :--- | :--- |
| **Task ID** | Unique ID (e.g., `iso-framer-001`) | Yes |
| **Skill Tested** | Name of the skill under test | Yes |
| **Input Path** | Repository-relative path to input fixture | Yes |
| **Output Path** | Repository-relative path to generated artifact | Yes |
| **Files Edited** | List of all files modified/created | Yes |
| **Files Skipped** | Files not edited due to scope/boundary rules | Yes |
| **Validation Result** | Output from validation command (Pass/Fail) | Yes |
| **Defect Class** | Classification if failure observed (Section 5) | If Fail |
| **Follow-up** | Recommended changes (Logic/Fixtures) | If needed |

> [!IMPORTANT]
> Do not update global status, walkthrough, README, CONTEXT, registries, scripts, or SKILL.md files from execution tasks. Document these needs as "Follow-up" in the log.

## 7. Path Hygiene & Response Rules

- **NO `file:///` LINKS**: Do not use `file:///` syntax in artifacts, logs, reports, or final responses.
- **RELATIVE PATHS**: Use repository-relative paths only (e.g., `examples/skill-tests/...`).
- **NO IMPROVISATION**: Stay within the `Allowed Edits` paths. Document out-of-scope needs in the `TEST-RUN-LOG.md`.

## 8. Hardened Task Prompts

## 8. Wave 1 Task Prompts (Phase 2)

### 8.1. Isolated: Problem Framer
```text
Task: Run problem-framer on examples/usage-research/scenarios/001-cold-start-messy-ai-workflows/raw_fog.md.
Allowed Edits:
- examples/skill-tests/problem-framer/problem_frame.md
- examples/skill-tests/problem-framer/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Expected Output: examples/skill-tests/problem-framer/problem_frame.md
Validation Command: python scripts/validate-artifact.py problem_frame examples/skill-tests/problem-framer/problem_frame.md
Safety: Do not edit SKILL.md. Document follow-up in TEST-RUN-LOG.md. No file:/// links. Use repo-relative paths.
```

### 8.2. Isolated: Repo Sensemaker
```text
Task: Run repo-sensemaker on the current repository.
Allowed Edits:
- examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md
- examples/skill-tests/repo-sensemaker/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Expected Output: examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md
Validation Command: python scripts/validate-repo.py ; python scripts/validate-artifact.py repository_sensemaking_brief examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md
Follow-up: Run "python scripts/validate-brief.py examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md" for deeper audit.
Safety: Do not edit SKILL.md. No file:/// links. Use repo-relative paths.
```

### 8.3. Isolated: Setup Sensemaking Skills (Dry Run)
```text
Task: Run setup-sensemaking-skills to audit repository configuration.
Test Design: examples/skill-tests/setup-sensemaking-skills/SETUP-TEST-DESIGN.md
Allowed Edits:
- examples/skill-tests/setup-sensemaking-skills/setup_plan.md
- examples/skill-tests/setup-sensemaking-skills/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Expected Output: examples/skill-tests/setup-sensemaking-skills/setup_plan.md
Validation: Manual / Checklist-based (See SETUP-TEST-DESIGN.md).
Safety: Do not modify core config files (AGENTS.md, etc.). Write audit findings only to setup_plan.md. No file:/// links.
```

### 8.4. Isolated: Docs Reconciler (Dry Run)
```text
Task: Run sensemaking-docs-reconciler to identify vocabulary or contract drift.
Allowed Edits:
- examples/skill-tests/docs-reconciler/reconcile_report.md
- examples/skill-tests/docs-reconciler/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Expected Output: examples/skill-tests/docs-reconciler/reconcile_report.md
Validation Command: python scripts/validate-artifact.py docs_contract_reconciliation_report examples/skill-tests/docs-reconciler/reconcile_report.md
Safety: Do not mutate CONTEXT.md or registries. Write discrepancies to reconcile_report.md. No file:/// links.
```

## 9. Future Phase Task Prompts

### 9.1. Isolated: Unknowns Mapper
```text
Task: Run unknowns-mapper on examples/skill-tests/problem-framer/problem_frame.md.
Allowed Edits:
- examples/skill-tests/unknowns-mapper/unknowns_map.md
- examples/skill-tests/unknowns-mapper/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Expected Output: examples/skill-tests/unknowns-mapper/unknowns_map.md
Validation Command: python scripts/validate-artifact.py unknowns_map examples/skill-tests/unknowns-mapper/unknowns_map.md
Safety: Do not edit SKILL.md. No file:/// links.
```

### 9.2. Isolated: Workflow Orchestrator
```text
Task: Run workflow-orchestrator on examples/pipeline/repo_sensemaking_brief.md.
Allowed Edits:
- examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md
- examples/skill-tests/workflow-orchestrator/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Expected Output: examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md
Validation Command: python scripts/validate-artifact.py workflow_orchestration_plan examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md ; python scripts/validate-plan.py examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md
Safety: Ensure Section 11 is valid. Do not edit SKILL.md. No file:/// links.
```

### 9.3. Handoff: Framer -> Mapper
```text
Task: Consume GENERATED problem_frame.md from Phase 2 and run unknowns-mapper.
Allowed Edits:
- examples/skill-tests/handoff/framer-to-mapper/unknowns_map.md
- examples/skill-tests/handoff/framer-to-mapper/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Validation Command: python scripts/validate-artifact.py unknowns_map examples/skill-tests/handoff/framer-to-mapper/unknowns_map.md
Safety: Classify defects as producer vs consumer in TEST-RUN-LOG.md. No file:/// links.
```

### 9.4. Maintenance Loop Audit
```text
Task: Run usage-researcher -> skill-maintainer loop using Scenario 005.
Input: examples/usage-research/scenarios/005-conflicting-fixes/
Allowed Edits:
- examples/skill-tests/maintenance/output/**
- examples/skill-tests/maintenance/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/scenarios/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Expected Output: examples/skill-tests/maintenance/output/skill_improvement_plan.md
Validation Command: python scripts/validate-skill-improvement-plan.py examples/skill-tests/maintenance/output/skill_improvement_plan.md
Goal: Confirm it identifies "fixture_defect" and "Class 8: Over-Maintenance" metadata. No file:/// links.

```

### 9.5. Full-Chain: Cold Start
```text
Task: Execute full pipeline from raw fog to prompt handoff.
Target Path: examples/skill-tests/full-chain/001-cold-start/
Allowed Edits:
- examples/skill-tests/full-chain/001-cold-start/**
- examples/skill-tests/full-chain/001-cold-start/TEST-RUN-LOG.md
Forbidden Edits:
- skills/**/SKILL.md, scripts/**, docs/**, examples/usage-research/**, workflow-registry.yaml, skill-registry.yaml, walkthrough/**, status/**, README.md, CONTEXT.md
Validation: Run scripts/validate-repo.py and scripts/validate-plan.py on final artifacts.
Safety: Document the thread of Search Seeds in the log. No file:/// links.
```

## 10. Final Validation Gates

1.  `python scripts/validate-repo.py`
2.  `python scripts/validate-brief.py [generated-brief]`
3.  `python scripts/validate-plan.py [generated-plan]`
4.  `python scripts/validate-usage-research-report.py [generated-report]`
5.  `python scripts/validate-skill-improvement-plan.py [generated-improvement-plan]`
