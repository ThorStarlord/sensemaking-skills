# Prompt Chain Output: fast-local-diagnostic

## Workflow Context
- **Workflow**: `fast-local-diagnostic`
- **Mode**: `prompt_chain`
- **Input Brief**: `artifacts/repository_sensemaking_brief.md`
- **Session**: prompt-chain/fast-local-diagnostic/2026-05-16

---

## Prompt 1: repo-sensemaker

**Target**: Run repo-sensemaker diagnosis to identify the weakest boundary.

**Input**: Repository state (files, registries, templates, scripts).

```markdown
/repo-sensemaker
Analyze the repository at `.` and produce a repository_sensemaking_brief.
Focus on identifying the weakest boundary between the artifact contracts,
validator scripts, and run-log templates. Use the existing brief at
artifacts/repository_sensemaking_brief.md as a reference for format.
Output to artifacts/repository_sensemaking_brief.md.
```

---

## Prompt 2: handoff

**Target**: Produce a prompt_handoff for the downstream skill (`sensemaking-docs-reconciler`).

**Input**: `artifacts/repository_sensemaking_brief.md` (the brief produced by Step 1).

**Constraints**: Must reference real artifact IDs from artifact-contracts.yaml. Stop condition must be non-empty.

```markdown
/prompt-handoff
Read the repository_sensemaking_brief at artifacts/repository_sensemaking_brief.md.
Produce a prompt_handoff artifact targeting the `sensemaking-docs-reconciler` skill.
Context: The brief identifies Contract Mismatch as the weakest boundary.
The reconciler should resolve drift between run-log-template.md structure
and what the validator ecosystem expects.
Include: target_skill, context_to_preserve, task, constraints, inputs,
expected_output, stop_condition, and a ready-to-copy prompt in a code block.
Output to artifacts/prompt_handoff.md.
```

---

## Validation Results

| Prompt | Target | Artifact | Validator | Result |
|:------:|--------|:--------:|:---------:|:------:|
| 1 | repo-sensemaker | repository_sensemaking_brief | validate-artifact.py (Level 2) + validate-brief.py (Level 3) | PASSED (existing brief revalidated) |
| 2 | handoff | prompt_handoff | validate-artifact.py (Level 2) + validate-prompt-handoff.py (Level 3) | PASSED (existing handoff revalidated) |

## Machine-readable record

```yaml
artifact_id: prompt_chain_output
session_id: prompt-chain/fast-local-diagnostic/2026-05-16
workflow_id: fast-local-diagnostic
execution_mode: prompt_chain
prompts:
  - step: 1
    skill: repo-sensemaker
    target_artifact: repository_sensemaking_brief
    validated: true
  - step: 2
    skill: handoff
    target_artifact: prompt_handoff
    validated: true
validators_exercised:
  - validate-artifact.py (Level 2, generic)
  - validate-brief.py (Level 3, specialized)
  - validate-prompt-handoff.py (Level 3, specialized)
all_passed: true
```
