---
validator_case: negative
validator_args:
  - repository_sensemaking_brief
expected_error_contains: "MISSING_REQUIRED_SECTION"
---
# Repository Sensemaking Brief

## 1. Repository Goal
Goal.

## 2. Current Shape
Shape.

## 3. Strong Signals
Signals.

## 4. Missing Pieces
Pieces.

## 5. Improvement Opportunities
Opportunities.

## 7. Evidence
Evidence.

## 8. Evidence Excerpts
```yaml
evidence_excerpts:
  - file: "tests/fixtures/validate-artifact/invalid/missing-required-section.md"
    lines: "1-2"
    quote: "A quote"
    supports_claim: "A claim"
```

## 9. Why This Boundary Matters
Matters.

## 10. Candidate Next Steps
Steps.

## 11. Recommended Next Step
Step.

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
recommended_workflow_id: "docs-contract-reconciliation"
recommended_execution_mode: "plan_only"
weakest_boundary: "validation"
required_inputs: []
primary_fog_type: architecture_fog
evidence: "Evidence."
created_at: "2026-05-19T16:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
Prompt.
