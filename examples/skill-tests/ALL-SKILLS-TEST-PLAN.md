# ALL-SKILLS-TEST-PLAN (Hardened)

This plan defines a non-interfering verification suite for the Sensemaking Skills ecosystem. It is designed for parallel execution by multiple agents with zero interference and strict boundary enforcement.

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
| **Isolated Tests** | `examples/skill-tests/[skill-name]/**` | `skills/**`, `scripts/**`, `docs/**`, registries, examples/pipeline/** |
| **Handoff Tests** | `examples/skill-tests/handoff/**` | `skills/**`, `scripts/**`, `docs/**`, registries, examples/pipeline/** |
| **Full Chain** | `examples/skill-tests/full-chain/001-cold-start/**`| `skills/**`, `scripts/**`, `docs/**`, registries, examples/pipeline/** |
| **Maintenance** | `examples/skill-tests/maintenance/**` | `skills/**`, `scripts/**`, `docs/**`, registries, examples/pipeline/** |

## 3. Shared-File Danger List (DO NOT EDIT)

The following files are strictly **Read-Only** during this verification phase. No task may modify them:

- `skills/**/SKILL.md` (Core instructions)
- `scripts/**` (Validation logic)
- `docs/**` (Architecture and PRDs)
- `examples/usage-research/**` (Scenario fixtures)
- `workflow-registry.yaml` / `skill-registry.yaml` (Registries)
- `walkthrough/*.md` / `status/*.md` (Maintenance docs)
- `README.md` / `CONTEXT.md`

## 4. Execution & Merge Order

To ensure safety and logical flow, tasks must be merged in this order:

1.  **Phase 1: Read-only Audits** (No files written, observation only).
2.  **Phase 2: Isolated Output Artifacts** (Independent skill verification).
3.  **Phase 3: Handoff & Full-chain Tests** (Inter-skill consistency).
4.  **Phase 4: Maintenance Safety Tests** (Defect classification loop).
5.  **Phase 5: Status Update** (Only after all validation gates pass).

## 5. Anti-Causal Confusion Rule

If a validation failure or behavioral defect is detected, the task must classify the defect BEFORE recommending an edit. Choose one:

- `producer_artifact_defect`: The input artifact was malformed or semantically thin.
- `consumer_skill_defect`: The skill ignored instructions or boundary rules.
- `fixture_defect`: The test fixture (fog or repository state) is unrealistic or broken.
- `evaluator_defect`: The human or LLM evaluator used a flawed rubric.
- `validator_defect`: The script flagged a false positive or missed a contract breach.
- `registry_defect`: The workflow or skill registry entry contains incorrect metadata.

## 6. Isolated Skill Task Prompts

### Isolated: Problem Framer
```text
Task: Run problem-framer on examples/pipeline/raw_fog.md.
Allowed Edits: examples/skill-tests/problem-framer/problem_frame.md
Forbidden Edits: skills/**, scripts/**, docs/**, registries, status docs.
Expected Output: examples/skill-tests/problem-framer/problem_frame.md
Validation Command: python scripts/validate-artifact.py examples/skill-tests/problem-framer/problem_frame.md
Safety: Do not edit SKILL.md. If logic errors are found, document follow-up instead of patching.
```

### Isolated: Unknowns Mapper
```text
Task: Run unknowns-mapper on examples/pipeline/problem_frame.md (fixture).
Allowed Edits: examples/skill-tests/unknowns-mapper/unknowns_map.md
Forbidden Edits: skills/**, scripts/**, docs/**, registries, status docs.
Expected Output: examples/skill-tests/unknowns-mapper/unknowns_map.md
Validation Command: python scripts/validate-artifact.py examples/skill-tests/unknowns-mapper/unknowns_map.md
Safety: Do not edit SKILL.md. Document logic gaps in your response.
```

### Isolated: Repo Sensemaker
```text
Task: Run repo-sensemaker on the current repository state.
Allowed Edits: examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md
Forbidden Edits: skills/**, scripts/**, docs/**, registries, status docs.
Expected Output: examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md
Validation Command: python scripts/validate-repo.py
Safety: Do not edit SKILL.md. Focus on evidence-backed diagnostic brief quality.
```

### Isolated: Workflow Orchestrator
```text
Task: Run workflow-orchestrator on examples/pipeline/repo_sensemaking_brief.md (fixture).
Allowed Edits: examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md
Forbidden Edits: skills/**, scripts/**, docs/**, registries, status docs.
Expected Output: examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md
Validation Command: python scripts/validate-plan.py examples/skill-tests/workflow-orchestrator/workflow_orchestration_plan.md
Safety: Do not edit SKILL.md. Ensure Section 11 is valid YAML.
```

## 7. Handoff & Full-Chain Task Prompts

### Handoff: Framer -> Mapper
```text
Task: Consume the GENERATED problem_frame.md from Phase 2 and run unknowns-mapper.
Allowed Edits: examples/skill-tests/handoff/framer-to-mapper/unknowns_map.md
Forbidden Edits: All shared-danger files.
Expected Output: A map that satisfies the specific Search Seed requirements for the next step.
Validation Command: python scripts/validate-artifact.py examples/skill-tests/handoff/framer-to-mapper/unknowns_map.md
Classification: If the map is weak, classify if it is due to a producer defect (Framer) or consumer defect (Mapper).
```

### Full-Chain: Cold Start
```text
Task: Execute full pipeline from raw fog to prompt handoff.
Target Path: examples/skill-tests/full-chain/001-cold-start/
Steps:
1. problem-framer -> problem_frame.md
2. unknowns-mapper -> unknowns_map.md
3. repo-sensemaker -> repo_sensemaking_brief.md
4. workflow-orchestrator -> workflow_orchestration_plan.md
5. prompt-handoff -> prompt_handoff.md
Allowed Edits: Only files within the Target Path.
Forbidden Edits: All shared-danger files.
Validation: Run validate-repo.py and validate-plan.py on the final artifacts.
```

## 8. Maintenance Safety Test Prompt

### Maintenance Loop Audit
```text
Task: Run usage-researcher -> skill-maintainer loop using Scenario 005 (Flawed Evaluation).
Input: examples/usage-research/scenarios/005-conflicting-fixes/
Allowed Edits: examples/skill-tests/maintenance/output/**
Forbidden Edits: All SKILL.md files, all scripts.
Goal: Verify that skill-maintainer classifies the failure as a `fixture_defect` and recommends a fixture edit instead of a logic patch.
Validation: python scripts/validate-skill-improvement-plan.py examples/skill-tests/maintenance/output/skill_improvement_plan.md
```

## 9. Final Validation Gates

These commands must pass before any status or walkthrough documentation is updated:

1.  **Repository Structure**: `python scripts/validate-repo.py`
2.  **Artifact Contracts**: `python scripts/validate-artifact.py [all-generated-artifacts]`
3.  **Plan Integrity**: `python scripts/validate-plan.py [all-generated-plans]`
4.  **Maintenance Logic**: `python scripts/validate-skill-improvement-plan.py [generated-plan]`

**Note**: If any validation gate fails, document the defect classification (Section 5) and stop. Do not update production status.
