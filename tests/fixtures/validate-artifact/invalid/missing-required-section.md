---
validator_case: negative
validator_args:
  - repository_sensemaking_brief
expected_error_contains: "Missing required section: weakest_boundary"
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

## 12. Recommended Workflow
Workflow.

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: "test-workflow"
recommended_execution_mode: "plan_only"
weakest_boundary: "validation"
required_inputs: []
```

## 14. Ready-to-copy prompt
Prompt.
