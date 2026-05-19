# Repository Sensemaking Brief

## 1. Repository goal
The `sensemaking-skills` repository is an agentic framework designed to transform ambiguous project "fog" into structured, executable workflows. It provides a modular pipeline of skills (Framing, Mapping, Diagnosis, Orchestration) to reduce information entropy in complex engineering tasks.

## 2. Current shape
- **Skills**: Modular components in `skills/` (problem-framer, unknowns-mapper, repo-sensemaker, workflow-orchestrator, etc.).
- **Registry**: Centralized `workflow-registry.yaml` and `skill-registry.yaml` in `skills/workflow-orchestrator/references/`.
- **Validation**: Strict artifact contract enforcement via `scripts/validate-artifact.py`.
- **Tests**: Scenario-based verification in `examples/skill-tests/`.

## 3. Strong signals
- **Artifact Hardening**: Every stage of the pipeline produces a machine-verifiable artifact.
- **Boundary Control**: Skills have explicit "Forbidden Edits" and "Boundary Rules" defined in their `SKILL.md`.
- **Taxonomy**: A formal `AGENTIC_FAILURE_MODES.md` exists to classify defects systematically.

## 4. Missing pieces
- **Workflow Maturity**: Some workflows (e.g., `autonomous-sprint`) are marked experimental or drafting.
- **Integration Tests**: The "Full-Chain" verification is currently being executed (Section 9.5) to prove end-to-end continuity.

## 5. Improvement opportunities
- **Handoff Automation**: Reducing the friction in "Ready-to-copy prompt" generation by leveraging the orchestrator's `autonomous_execution` mode.
- **Semantic Monitoring**: Enhancing Level 3 validators to check for semantic drift across the entire chain.

## 6. Weakest boundary
The semantic handoff between `repo-sensemaker` and `workflow-planner`. If the brief recommends a workflow ID that is stale or missing from the registry, the orchestrator must fail fast. This is currently enforced by `validate-plan.py`.

## 7. Evidence
- **Workflow Registry**: `skills/workflow-orchestrator/references/workflow-registry.yaml` (Lines 277-326) defines the `full-local-sensemaking` workflow.
- **Artifact Contracts**: `skills/workflow-orchestrator/references/artifact-contracts.yaml` defines the mandatory fields for the brief.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/workflow-orchestrator/references/workflow-registry.yaml
    lines: 277-280
    quote: "full-local-sensemaking: display_name: Full Local Sensemaking purpose: Convert raw fog into a repository diagnosis..."
    supports_claim: "The repository provides a formal workflow for the current cold-start task."
  - file: skills/workflow-orchestrator/SKILL.md
    lines: 32-34
    quote: "The orchestrator MUST refuse the request or downgrade to plan_only if a brief does not contain a valid machine-readable handoff."
    supports_claim: "The boundary between sensemaking and orchestration is strictly guarded."
```

## 9. Why this boundary matters
If the handoff fails, the agent will hallucinate a workflow path or attempt to execute skills out of order, violating the repository's safety policies and potentially corrupting the state.

## 10. Candidate next steps
1. Execute Step 4 of the `full-chain-cold-start` using `workflow-planner`.
2. Run `scripts/validate-plan.py` on the resulting orchestration plan.
3. Verify repository integrity with `scripts/validate-repo.py`.

## 11. Recommended next step
Execute `workflow-planner` on this brief to generate a formal `workflow_orchestration_plan.md`.

## 12. Recommended workflow
`full-local-sensemaking`

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: plan_only
weakest_boundary: semantic-handoff-continuity
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
```text
Task: Run workflow-orchestrator on examples/skill-tests/full-chain/001-cold-start/repo_sensemaking_brief.md.
Execution Mode: plan_only
Target Path: examples/skill-tests/full-chain/001-cold-start/workflow_orchestration_plan.md
```
