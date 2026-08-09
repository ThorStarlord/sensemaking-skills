---
validator_case: positive
---
# Example: Repository Sensemaking Brief (integration_fog case)

## 1. Repository goal
Diagnose whether the third-party payments webhook integration is safe to extend.

## 2. Current shape
- `integrations/payments/`: webhook receiver and signature verification.
- `skills/`: sensemaking pipeline, unrelated to this example's subject repo.

## 3. Strong signals
Signature verification is present and covered by one test.

## 4. Missing pieces
No documented contract for the third-party webhook payload shape.

## 5. Improvement opportunities
Document the external API contract explicitly instead of inferring it from code.

## 6. Weakest boundary
Contract Mismatch: the webhook handler assumes a payload shape the third-party API's own docs do not guarantee.

## 7. Evidence
- [webhook_handler.py](../../skills/repo-sensemaker/references/weakness-types.md): Handler reads fields with no schema validation.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: skills/repo-sensemaker/references/weakness-types.md
    lines: L6
    quote: "2. **Contract Mismatch**: Files claim to be one format (e.g., `.yaml`) but are actually another (e.g., Markdown)."
    supports_claim: "Confirms Contract Mismatch is a registered weakness type, used here by analogy for the external contract."
```

## 9. Why this boundary matters
If the third-party API changes its payload shape without notice, the integration fails silently. Logic trace: the handler has no schema check, so the only test that would catch drift is absent.

## 10. Candidate next steps
1. Add schema validation for the inbound webhook payload.
2. Document the external contract explicitly.

## 11. Recommended next step
Add schema validation for the inbound webhook payload.

## 12. Recommended workflow
full-local-sensemaking

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
primary_fog_type: integration_fog
evidence:
  - "skills/repo-sensemaker/references/weakness-types.md: used by analogy for the external contract shape."
recommended_workflow_id: full-local-sensemaking
recommended_execution_mode: guided_execution
weakest_boundary: webhook-payload-contract
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - repository_sensemaking_brief
created_at: "2026-08-09T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```markdown
/workflow-planner

Brief: [Link to this brief]
Target: Add schema validation to the payments webhook handler.
Workflow: full-local-sensemaking
Mode: guided_execution
```
