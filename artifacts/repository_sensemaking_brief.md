# Repository Sensemaking Brief: sensemaking-skills

## 1. Repository goal
The `sensemaking-skills` repository aims to provide a set of agentic skills for "sensemaking" — turning ambiguous project ideas (fog) into structured, machine-verifiable plans and execution paths. It formalizes the orchestration of these skills via a `workflow-orchestrator`.

## 2. Current shape
- **skills/**: Logic and documentation for each skill (e.g., `workflow-orchestrator`, `repo-sensemaker`).
- **scripts/**: Python validators (`validate-artifact.py`, `validate-brief.py`, `validate-repo.py`).
- **references/**: (Inside skills) Templates and registries.
- **examples/**: Positive and negative fixtures for testing.
- **artifacts/**: (Generated) Output of skill executions.

## 3. Strong signals
- **Contract Enforcement**: High usage of `artifact-contracts.yaml` and Python validators.
- **Auditability**: Mandatory `run_log` for autonomous/guided runs.
- **YOLO Mode Hardening**: Built-in safety heuristics and post-step verification.

## 4. Missing pieces
- **Validator Unified Interface**: Inconsistency in how validators are invoked in contracts.
- **Template Centralization**: Core templates like `repo-analysis-template.md` are scattered across skill-specific references.

## 5. Improvement opportunities
- Consolidate all artifact templates into a central `references/` directory.
- Standardize all `verification.script` entries to use `validate-artifact.py`.

## 6. Weakest boundary
The **Contract Mismatch**. Specifically, the drift between the intended general validator (`validate-artifact.py`) and specialized ones, along with the lack of run-log schema validation against the workflow registry.

## 7. Evidence
- `skills/workflow-orchestrator/references/artifact-contracts.yaml`: Shows `validate-brief.py` for the brief while others use `validate-artifact.py`.
- `skills/workflow-orchestrator/references/run-log-template.md`: Requires a `gate` field, but no script verifies this field against `workflow-registry.yaml`.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/workflow-orchestrator/references/artifact-contracts.yaml
    lines: L63-L65
    quote: "verification:\n      script: \"python scripts/validate-brief.py {artifact_path}\""
    supports_claim: "Inconsistency in validator invocation compared to other artifacts using validate-artifact.py."
  - file: skills/workflow-orchestrator/references/run-log-template.md
    lines: L20-L21
    quote: "- **gate**: [Gate Name]\n- **status**: [COMPLETED | PAUSED | FAILED]"
    supports_claim: "Run log tracks gates, but no automated script verifies gate names against workflow-registry.yaml."
```

## 9. Why this boundary matters
If the run log records incorrect gate names or skips validation steps due to contract drift, the machine-auditable nature of the pipeline is compromised. The logic trace for this diagnosis runs from observed invocation inconsistencies to contract drift as the root cause.

## 10. Candidate next steps
- Update `artifact-contracts.yaml` to use `validate-artifact.py` for all artifacts.
- Create `scripts/validate-run-log.py`.
- Move templates to a central location.

## 11. Recommended next step
Standardize `artifact-contracts.yaml` to use `validate-artifact.py repository_sensemaking_brief {artifact_path}`.

## 12. Recommended workflow
`docs-contract-reconciliation`

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: guided_execution
weakest_boundary: Validator/Contract Synchronization
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
```text
Use workflow-orchestrator in guided_execution mode.
Input: artifacts/repository_sensemaking_brief.md
Workflow: docs-contract-reconciliation
Step 2: sensemaking-docs-reconciler
```
