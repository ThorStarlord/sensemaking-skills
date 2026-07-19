# Repository Sensemaking Brief

## Summary
This repository implements an agent-native framework for repository diagnosis
and workflow orchestration. It turns repository uncertainty into clear problem
frames, research paths, and actionable next-step prompts.

## Weakest Boundary
The current weakest boundary is in workflow routing: the gap between initial
problem-domain identification and domain-specific implementation workflows.

## Evidence
- File: CONTEXT.md (missing — recommend creating)
- File: skills/workflow-planner/references/workflow-registry.yaml (complete)
- File: scripts/validate-plan.py (alignment enforcement works)

## Recommended Next Step
Implement the architectural-review skill to handle routing decisions when
proposed architectural changes need validation against principal-engineer judgment.

## Machine-readable metadata

```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: architecture_fog
evidence:
  - "Workflow registry defined with 30+ workflows"
  - "Validation framework in place"
  - "routing decision fields present in artifact-contracts.yaml"
  - "Gap: architectural-review skill not yet implemented"
recommended_workflow_id: architectural-review-planning-workflow
created_at: "2026-07-19T12:00:00Z"
created_by: "deterministic-test-executor"
immutable: false
```
