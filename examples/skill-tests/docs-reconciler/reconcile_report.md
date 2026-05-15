# Documentation Reconciliation Report

## 1. Drift Diagnosis
A comparison between `CONTEXT.md`, `skill-registry.yaml`, and the `skills/` directory reveals slight vocabulary drift. Specifically, the "Flagship Skills" list in `CONTEXT.md` (Line 27) identifies only five skills, omitting the recently institutionalized maintenance loop skills (`usage-researcher`, `skill-maintainer`) and configuration skills (`setup-sensemaking-skills`, `sensemaking-docs-reconciler`).

## 2. Weakest Boundary
**Glossary Alignment**: The central glossary in `CONTEXT.md` is the "Source of Truth" for agentic routing, but it is currently trailing the actual file system state. If an agent relies solely on the glossary for discovery, it will miss 40% of the repository's capabilities.

## 3. Missing Instructions
There is no "Maintenance Protocol" section in `CONTEXT.md` describing how the `usage-researcher -> skill-maintainer` loop should be triggered by an agent during a normal workflow.

## 4. Missing Examples
The repository lacks a "Gold Standard" example for:
- `docs_contract_reconciliation_report`
- `setup_plan`

## 5. Validator Blind Spots
The `validate-artifact.py` script performs structural header checks but does not verify if the "Next Artifact" section of a `problem_frame.md` matches the actual workflow chosen by the `workflow-orchestrator`.

## 6. Ambiguous Artifact Names
The term "Sensemaking Brief" is used in `CONTEXT.md`, but the machine ID in `artifact-contracts.yaml` is `repository_sensemaking_brief`. While semantically close, this could lead to ID mismatch in autonomous execution.

## 7. Drift Risks
Medium. While the core five-skill pipeline is stable, the maintenance loop is currently "invisible" to agents starting from the root glossary, which may lead to manual, non-auditable patches instead of formal `skill_improvement_plan` artifacts.

## 8. Recommended Patches
1. Update `CONTEXT.md` flagship list to include all 9 skills.
2. Align "Sensemaking Brief" terminology with `repository_sensemaking_brief` ID.
3. Add a "Maintenance Loop" section to the Routing Source of Truth table in `CONTEXT.md`.

## 9. Mismatches Found
- **Skill Count**: `CONTEXT.md` (5) vs `skills/` directory (9).
- **Artifact ID**: "Sensemaking Brief" vs `repository_sensemaking_brief`.
- **Validation List**: `CONTEXT.md` lists 4 validators, but `scripts/` contains 5 core validation scripts (including `validate-usage-research-report.py`).

## 10. Changes Required
- [ ] Patch `CONTEXT.md` lines 27-32.
- [ ] Patch `CONTEXT.md` lines 52-58.
- [ ] Synchronize terminology in `README.md` to match `artifact-contracts.yaml` IDs.

## 11. Patches Proposed
```diff
- - **Flagship Skills**: The repo contains a five-skill sensemaking pipeline: `problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-orchestrator`, and `prompt-handoff`.
+ - **Flagship Skills**: The repo contains a nine-skill sensemaking pipeline: `problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-orchestrator`, `prompt-handoff`, `setup-sensemaking-skills`, `sensemaking-docs-reconciler`, `usage-researcher`, and `skill-maintainer`.
```

## 12. Validation Result
PASS (Dry Run Audit Complete).

## 13. Next Handoff
Recommended Next Move: Execute the proposed patches to `CONTEXT.md` after Wave 1 completion.
