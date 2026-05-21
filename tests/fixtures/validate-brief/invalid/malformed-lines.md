---
validator_case: negative
expected_error_contains: "INVALID_LINE_FORMAT"
---
# Repository Sensemaking Brief (Malformed Evidence Lines)

Otherwise valid, but an evidence excerpt's `lines` field is free-text rather than
a line number or range. The validator must still reject this even though it now
accepts bare numbers like `18` and `25-30`.

## 1. Repository goal
Test that a non-numeric line reference is rejected.

## 2. Current shape
- `skills/`: sensemaking pipeline.
- `scripts/`: governance.

## 3. Strong signals
The pipeline separates diagnosis from action.

## 4. Missing pieces
- Automated parity tests.

## 5. Improvement opportunities
Consolidate shared references.

## 6. Weakest boundary
Contract Mismatch: the repo-sensemaker to workflow-planner handoff is not contract-enforced.

## 7. Evidence
- [SKILL.md](../../skills/repo-sensemaker/SKILL.md): lacks a hard schema check.

Logic trace: the handoff shape is defined but unenforced, so it is the weakest link.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/SKILL.md
    lines: "see the handoff section"
    quote: "The output of this skill is a diagnostic artifact"
    supports_claim: "Diagnosis/Action boundary exists."
```

## 9. Why this boundary matters
A wrong workflow ID could trigger unsafe execution.

## 10. Candidate next steps
1. Add a brief-to-plan contract check.

## 11. Recommended next step
Implement the `full-local-sensemaking` workflow.

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: guided_execution
weakest_boundary: manual-handoff
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
```markdown
/workflow-planner
Brief: [Link to this brief]
Workflow: full-local-sensemaking
Mode: guided_execution
```
