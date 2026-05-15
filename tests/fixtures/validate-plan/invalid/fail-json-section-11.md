---
validator_case: negative
expected_error_contains: "Section 11 YAML block"
---
# Fail: JSON Section 11

## 11. Machine-readable plan
```json
{
  "artifact_id": "workflow_orchestration_plan",
  "chosen_workflow_id": "docs-contract-reconciliation",
  "execution_mode": "plan_only",
  "status": "READY"
}
```

