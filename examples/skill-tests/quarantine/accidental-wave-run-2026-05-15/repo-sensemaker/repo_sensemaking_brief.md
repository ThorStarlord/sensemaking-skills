# Repository Sensemaking Brief

## 1. Repository goal
Establish a high-fidelity meta-engineering pipeline that converts unstructured user intent ("Fog") into verified, executable agentic workflows. The system prioritizes "Discipline over Magic" through strict artifact contracts and auditable execution logs.

## 2. Current shape
- `skills/`: Atomic sensemaking units (`problem-framer`, `unknowns-mapper`, `repo-sensemaker`).
- `scripts/`: Python-based validators (`validate-artifact.py`, `validate-repo.py`).
- `examples/skill-tests/`: (NEW) Verification suite for parallel task execution.
- `workflow-registry.yaml` / `skill-registry.yaml`: Machine-readable orchestration source of truth.

## 3. Strong signals
- **Artifact Contracts**: Defined in `skills/workflow-orchestrator/references/artifact-contracts.yaml` with required sections and machine fields.
- **Boundary Logic**: Skills include specific rules like "Orchestration Shield" to prevent hallucination.
- **Safety Hardening**: Recent addition of `TEST-RUN-LOG.md` and forbidden path lists for parallel runs.

## 4. Missing pieces
- **Stable Input Fixtures**: Some test plan tasks refer to missing files in `examples/pipeline/`.
- **Cross-Artifact Semantic Validation**: Validators check structure but not yet semantic alignment between e.g., Problem Frame and Unknowns Map.

## 5. Improvement opportunities
- Unify validation command signatures across all documentation and test plans.
- Implement a "Compliance Auditor" skill to automate the review of `TEST-RUN-LOG.md` files.

## 6. Weakest boundary
**Test Plan Reliability**: The verification layer (the "tester") has drift between its documentation (`ALL-SKILLS-TEST-PLAN.md`) and the actual repository state (missing fixtures and mismatched script signatures).

## 7. Evidence
- Missing fixture: `examples/pipeline/problem_frame.md` cited in `ALL-SKILLS-TEST-PLAN.md:L141`.
- Command signature mismatch: `ALL-SKILLS-TEST-PLAN.md:L93` vs `scripts/validate-artifact.py`.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: examples/skill-tests/ALL-SKILLS-TEST-PLAN.md
    lines: 141
    quote: "Task: Run unknowns-mapper on examples/pipeline/problem_frame.md."
    supports_claim: "The test plan refers to a non-existent input fixture."
  - file: scripts/validate-artifact.py
    lines: 104-107
    quote: "parser.add_argument(\"artifact_id\", ...)\nparser.add_argument(\"artifact_path\", ...)"
    supports_claim: "The script requires artifact_id, but the test plan command omits it."
```

## 9. Why this boundary matters
If the testing environment is unreliable, we cannot trust the "green" status of skills. Parallel tasks might report success while failing to validate correctly due to script errors or missing data.

## 10. Candidate next steps
- Patch `ALL-SKILLS-TEST-PLAN.md` with correct command signatures.
- Seed `examples/pipeline/` with stable output artifacts from Wave 1.
- Implement the "Compliance Audit" meta-task.

## 11. Recommended next step
Execute the "Compliance Audit" (Meta-Task) on Wave 1 outputs to finalize the parallel execution contract.

## 12. Recommended workflow
`skill_maintenance_workflow`

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: skill_maintenance_workflow
recommended_execution_mode: plan_only
weakest_boundary: test_plan_fixture_drift
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
Run the skill-maintainer to patch `examples/skill-tests/ALL-SKILLS-TEST-PLAN.md` using the evidence provided in this brief. Fix command signatures and update input paths to point to stable fixtures in `examples/skill-tests/`.
