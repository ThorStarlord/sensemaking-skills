# Repository Sensemaking Brief: Canonical Template Fixture

This fixture mirrors the "Complete Example" yaml block from
`skills/repo-sensemaker/references/repo-analysis-template.md` exactly, so a
producer following the template documentation as-written is proven to pass
`validate-brief.py`.

## 1. Repository goal
Example repository goal text.

## 6. Weakest boundary
**Weakness type:** Contract Mismatch

## 7. Evidence
- README.md (lines 5-12): feature requirements are vague, no user context
- docs/ARCHITECTURE.md: does not exist

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: README.md
    lines: L5-L12
    quote: "An agent-native framework for repository diagnosis and workflow orchestration."
    supports_claim: "Feature requirements are vague"
```

## 12. Recommended workflow
Logic trace: the evidence shows feature requirements are vague and no
architecture documentation exists, so the fog is centered on undefined
product scope rather than UI, docs, or architecture concerns; this points
to product_fog and the product-implementation-workflow.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: product_fog
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (lines 5-12): feature requirements are vague, no user context"
  - "docs/ARCHITECTURE.md: does not exist"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: analytics_feedback_gap
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-05-19T16:00:00Z"
immutable: true
```
