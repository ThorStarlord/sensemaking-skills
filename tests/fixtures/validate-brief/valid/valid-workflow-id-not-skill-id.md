---
validator_case: positive
---
# Example: Valid Workflow ID (Positive Fixture)

Companion to `repo-sensemaker-real-skill-id-in-workflow-field.md`: proves a
genuine top-level workflow ID (`docs-implementation-workflow`, taken from
`workflow-registry.yaml`) passes validation, so the regression test isn't
rejecting all IDs that look similar to a skill name.

## 1. Repository goal
Test that a real workflow ID (as opposed to a skill ID) passes validation.

## 2. Current shape
Standard repo structure.

## 3. Strong signals
- Workflow IDs are enumerated in workflow-registry.yaml.

## 4. Missing pieces
None relevant to this fixture.

## 6. Weakest boundary
Contract Mismatch: nothing in this fixture; used only to prove valid IDs pass.

## 7. Evidence
`skills/workflow-planner/references/workflow-registry.yaml` (L812): declares `docs-implementation-workflow` as a top-level workflow id.

Logic trace: the validator loads workflow-registry.yaml and checks recommended_workflow_id against the set of top-level `id` values; docs-implementation-workflow is one of those values, so it must pass.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/workflow-planner/references/workflow-registry.yaml
    lines: L812
    quote: "- id: docs-implementation-workflow"
    supports_claim: "docs-implementation-workflow is a real top-level workflow id."
```

## 9. Why this boundary matters
Confirms valid IDs are not falsely rejected.

## 10. Candidate next steps
None.

## 11. Recommended next step
None.

## 12. Recommended workflow
docs-implementation-workflow

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
primary_fog_type: docs_fog
evidence:
  - "skills/workflow-planner/references/workflow-registry.yaml (lines L812): docs-implementation-workflow is a valid workflow id"
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: none
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-07-25T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```markdown
/workflow-planner
Brief: [Link to this brief]
Workflow: docs-implementation-workflow
Mode: guided_execution
```
