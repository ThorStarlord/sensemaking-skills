# ALL-SKILLS-TEST-PLAN

This plan defines a non-interfering verification suite for the Sensemaking Skills ecosystem. It focuses on artifact quality, handoff integrity, and behavioral correctness without patching the underlying skills.

## 1. Test Strategy

| Strategy | Scope | Goal | Verification Method |
| :--- | :--- | :--- | :--- |
| **Isolated Skill Tests** | Single Skill | Verify logic compliance with `SKILL.md` boundary rules. | Input fixture -> Output artifact validation. |
| **Handoff Tests** | Two Skills | Verify that artifact $A$ from Producer $P$ satisfies the requirements for Consumer $C$. | Cross-artifact validation (scripts/validate-artifact.py). |
| **End-to-End Chain Tests** | Full Pipeline | Verify the semantic thread from raw fog to final executable prompt. | Sequential execution with frozen state. |
| **Maintenance Safety Tests** | Meta-Skills | Verify that research/maintenance skills classify defects without blind patching. | Adversarial fixture testing (Scenario 005). |

## 2. File Isolation Strategy

All test outputs must be written to isolated folders to prevent state contamination.

- **Problem Framer**: examples/skill-tests/problem-framer/
- **Unknowns Mapper**: examples/skill-tests/unknowns-mapper/
- **Repo Sensemaker**: examples/skill-tests/repo-sensemaker/
- **Workflow Orchestrator**: examples/skill-tests/workflow-orchestrator/
- **Prompt Handoff**: examples/skill-tests/prompt-handoff/
- **Usage Researcher**: examples/skill-tests/usage-researcher/
- **Skill Maintainer**: examples/skill-tests/skill-maintainer/
- **Docs Reconciler**: examples/skill-tests/docs-reconciler/
- **Setup Skill**: examples/skill-tests/setup-skill/
- **Full Chain**: examples/skill-tests/full-chain/001-cold-start/

## 3. Skill Test Matrix

| Skill | Test purpose | Input fixture | Expected output artifact | Failure modes to detect | Allowed edits |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **problem-framer** | Fog deconstruction | examples/pipeline/raw_fog.md | problem_frame.md | Non-implementation violation, vague OUP. | Test outputs only |
| **unknowns-mapper** | Gap classification | examples/pipeline/problem_frame.md | unknowns_map.md | Premature research, tautological stopping rules. | Test outputs only |
| **repo-sensemaker** | Diagnostic brief | Root directory | repo_sensemaking_brief.md | Lack of evidence, missing "Weakest Boundary". | Test outputs only |
| **workflow-orchestrator**| Plan generation | examples/pipeline/repo_sensemaking_brief.md | workflow_orchestration_plan.md | Missing Section 11, registry mismatch. | Test outputs only |
| **prompt-handoff** | Packaging | examples/pipeline/workflow_orchestration_plan.md | prompt_handoff.md | Lost constraints, non-actionable task. | Test outputs only |
| **usage-researcher** | Behavioral audit | examples/usage-research/scenarios/004-broken-registry/maintenance_run_log.md | usage_research_report.md | Speculative reporting, missing failure category. | Test outputs only |
| **skill-maintainer** | Maintenance plan | examples/usage-research/scenarios/005-conflicting-fixes/output/usage_research_report.md | skill_improvement_plan.md | Overfitting, missing risk classification. | Test outputs only |
| **docs-reconciler** | Vocabulary sync | CONTEXT.md / workflow-registry.yaml | Resolution Proposal | Unapproved mutation, logic drift. | Test outputs only |
| **setup-skill** | Config bootstrap | README.md | AGENTS.md (Sensemaking Block) | Premature file write, non-interactive bulk questions. | Test outputs only |

## 4. Handoff Matrix

| Producer skill | Artifact | Consumer skill | Contract risk | Validation idea |
| :--- | :--- | :--- | :--- | :--- |
| problem-framer | problem_frame.md | unknowns-mapper | OUP too vague for mapper | Verify OUP provides an "inspectable proxy". |
| unknowns-mapper | unknowns_map.md | repo-sensemaker | Missing Search Seed | Verify research paths map to concrete files. |
| repo-sensemaker | repo_sensemaking_brief.md | workflow-orchestrator | Unmapped workflow ID | Match against workflow-registry.yaml IDs. |
| workflow-orchestrator| workflow_orchestration_plan.md | prompt-handoff | Lost constraints | Verify critical "must-haves" persist. |

## 5. Parallel execution plan

1. **Phase 1 (Parallel)**:
   - `problem-framer` test.
   - `repo-sensemaker` test.
   - `setup-skill` test.
   - `docs-reconciler` test.

2. **Phase 2 (Sequential)**:
   - `unknowns-mapper` (depends on Framer output).
   - `usage-researcher` (depends on existing run logs).

3. **Phase 3 (Sequential)**:
   - `workflow-orchestrator` (depends on Mapper/Sensemaker output).
   - `skill-maintainer` (depends on Researcher output).

4. **Phase 4 (Final)**:
   - `prompt-handoff` (depends on Orchestrator output).
   - `Full-chain integration test`.

## 6. Copy/paste Jules task prompts

### Problem Framer Test
```text
Task: Run problem-framer on examples/pipeline/raw_fog.md.
Expected Output: examples/skill-tests/problem-framer/problem_frame.md.
Rules: Do not propose technical solutions. Identify the Object Under Pressure (OUP).
Validation: python scripts/validate-artifact.py examples/skill-tests/problem-framer/problem_frame.md
```

### Unknowns Mapper Test
```text
Task: Run unknowns-mapper on examples/pipeline/problem_frame.md.
Expected Output: examples/skill-tests/unknowns-mapper/unknowns_map.md.
Rules: Do not perform research. Define concrete Stopping Rules.
Validation: python scripts/validate-artifact.py examples/skill-tests/unknowns-mapper/unknowns_map.md
```

### Repo Sensemaker Test
```text
Task: Run repo-sensemaker on the current repository.
Expected Output: examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md.
Rules: Cite file paths for all evidence. Identify the "Weakest Boundary".
Validation: python scripts/validate-repo.py
```

### Workflow Orchestrator Test
```text
Task: Run workflow-orchestrator on examples/pipeline/repo_sensemaking_brief.md.
Expected Output: examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md.
Rules: Must include Section 11 (Machine-readable plan). Default to plan_only mode.
Validation: python scripts/validate-plan.py examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md
```

### Prompt Handoff Test
```text
Task: Run prompt-handoff on examples/pipeline/workflow_orchestration_plan.md.
Expected Output: examples/skill-tests/prompt-handoff/prompt_handoff.md.
Rules: Preserve all critical constraints and evidence.
Validation: python scripts/validate-artifact.py examples/skill-tests/prompt-handoff/prompt_handoff.md
```

### Usage Researcher Test
```text
Task: Run usage-researcher on examples/usage-research/scenarios/004-broken-registry/maintenance_run_log.md.
Expected Output: examples/skill-tests/usage-researcher/usage_research_report.md.
Rules: Classify failures as Structural, Semantic, or Boundary. Link evidence to snippets.
Validation: python scripts/validate-usage-research-report.py examples/skill-tests/usage-researcher/usage_research_report.md
```

### Skill Maintainer Test
```text
Task: Run skill-maintainer on examples/usage-research/scenarios/005-conflicting-fixes/output/usage_research_report.md.
Expected Output: examples/skill-tests/skill-maintainer/skill_improvement_plan.md.
Rules: Do not patch SKILL.md. Classify edits by type and risk. Provide before/after behavior.
Validation: python scripts/validate-skill-improvement-plan.py examples/skill-tests/skill-maintainer/skill_improvement_plan.md
```

## 7. Full-chain integration test

**Target**: examples/skill-tests/full-chain/001-cold-start/

**Workflow**:
1. raw_fog.md (Input)
2. problem-framer -> problem_frame.md
3. unknowns-mapper -> unknowns_map.md
4. repo-sensemaker -> repo_sensemaking_brief.md
5. workflow-orchestrator -> workflow_orchestration_plan.md
6. prompt-handoff -> prompt_handoff.md

**Success Criteria**: The final prompt_handoff.md must contain the specific "Search Seed" and "Stopping Rules" defined in the earlier steps.

## 8. Maintenance safety test

**Scenario**: Verify `usage-researcher` -> `skill-maintainer` loop against Scenario 005 (Flawed Evaluation).

**Test**:
1. Run `usage-researcher` on Scenario 005 fixtures.
2. Verify the report correctly identifies that the *fixture* is flawed, not the skill logic.
3. Pass the report to `skill-maintainer`.
4. **Pass Condition**: `skill-maintainer` must propose a `fixture_edit` instead of an `instruction_edit`.

## 9. Final validation gate

After execution, run these commands to ensure repository integrity:

1. `python scripts/validate-repo.py`
2. `python scripts/validate-brief.py examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md`
3. `python scripts/validate-plan.py examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md`
4. `python scripts/validate-skill-improvement-plan.py examples/skill-tests/skill-maintainer/skill_improvement_plan.md`

**Note**: Do not update walkthrough or status docs unless all validation gates pass.
