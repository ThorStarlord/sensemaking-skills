---
validator_case: negative
expected_error_contains: "Hallucination detected!"
---
# Example: Repo-Sensemaker ID Hallucination (Negative Fixture)

This example demonstrates a `repository_sensemaking_brief` that contains a hallucinated `recommended_workflow_id`.

## 1. Repository goal
Test grounding validation.

## 2. Current shape
Standard repo structure.

## 3. Strong signals
- Grounding is required.

## 4. Missing pieces
- Registry enforcement.

## 5. Improvement opportunities
- None.

## 6. Weakest boundary
Workflow ID selection.

## 7. Evidence
The skill currently recommends `wave-1-execution` which does not exist in `workflow-registry.yaml`.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: scripts/validate-brief.py
    lines: L1-L10
    quote: "import os"
    supports_claim: "Validators are present."
```

## 9. Why this boundary matters
Prevents orchestrator failure.

## 10. Candidate next steps
- Fix grounding.

## 11. Recommended next step
Fix grounding.

## 12. Recommended workflow
wave-1-execution

## 13. Machine-readable handoff
```yaml
recommended_workflow_id: wave-1-execution
recommended_execution_mode: plan_only
weakest_boundary: workflow_grounding
required_inputs:
  - repository_sensemaking_brief
```

## 14. Ready-to-copy prompt
N/A
