---
validator_case: positive
---
# Example: Repository Sensemaking Brief — toolchain workflow not available in target (escalated)

## 1. Repository goal
A standalone application repository the analyst was asked to diagnose. It is not
a Sensemaking-configured repository and does not vendor the Sensemaking skill set.

## 2. Current shape
- `src/`: application code.
- `docs/`: a short README and one architecture note.
- No `skills/` directory, no `skills/workflow-planner/`, no `skills/VENDORED.yaml`,
  no `sensemaking-config.yaml`.

## 3. Strong signals
The core module boundaries are clear and the build is green. The architecture
note describes the intended layering and mostly matches the code.

## 4. Missing pieces
- No decision record for the proposed move to an event-driven core.
- The proposed direction is discussed in an issue but never evaluated against the
  repository's own constraints.

## 5. Improvement opportunities
Capture the layering rules from the architecture note as an enforced check.

## 6. Weakest boundary
Contract Mismatch: the proposed architectural direction (event-driven core) is
described as decided in one issue but is not reconciled with the still-current
layered architecture note, and nothing evaluates the proposal against the repo's
constraints.

## 7. Evidence
- `skills/repo-sensemaker/references/weakness-types.md:6` registers Contract
  Mismatch as a weakness type, which is the shape of the disagreement here
  between the issue and the architecture note.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L6
    quote: "2. **Contract Mismatch**: Files claim to be one format (e.g., `.yaml`) but are actually another (e.g., Markdown)."
    supports_claim: "Confirms Contract Mismatch is a registered weakness type."
```

## 9. Why this boundary matters
Downstream architecture and schema work is blocked until the proposed direction
is either ratified or rejected against the repository's own constraints.

Logic trace: the evidence establishes an unreconciled architectural proposal, and
the conceptually fitting Sensemaking workflow for that situation
(`architectural-review-planning-workflow`) is part of the Sensemaking toolchain
but is **not vendored or available in this target repository**, so no runnable
workflow can be recommended from the target's context.

## 10. Candidate next steps
1. Escalate the proposed direction to the owner for an explicit ruling.
2. Separately, add a lightweight architecture-decision record so the outcome is
   captured.

## 11. Recommended next step
Escalate: the target repository does not vendor `workflow-planner`, so no
Sensemaking workflow is available as an execution vehicle here. The conceptually
appropriate toolchain workflow, `architectural-review-planning-workflow`, is
named only as a pointer for a maintainer who runs it inside the Sensemaking
toolchain against this repository — it is not available in the analysed target.

## 12. Recommended workflow
null — `architectural-review-planning-workflow` would fit the situation
conceptually, but it exists only in the Sensemaking toolchain registry and is
**not available in the target repository** (no `skills/workflow-planner/`, no
`skills/VENDORED.yaml`, no `sensemaking-config.yaml`). Recommending it as a
runnable next step would imply target-local availability that does not exist.

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "skills/repo-sensemaker/references/weakness-types.md:6: Contract Mismatch is a registered weakness type."
recommended_workflow_id: null
recommended_execution_mode: plan_only
escalation_recommended: true
weakest_boundary: unreconciled-architectural-proposal
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-09-03T16:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```markdown
Escalate: no downstream workflow is recommended by this brief. The analysed
target does not vendor `workflow-planner`, so `architectural-review-planning-workflow`
(named as a conceptual pointer only) is not available here (ADR 0014 no-match state).
```
