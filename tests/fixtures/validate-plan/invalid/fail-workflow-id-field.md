---
validator_case: negative
expected_error_contains: "WORKFLOW_NOT_FOUND"
---
# Fail: workflow_id field

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
workflow_id: docs-contract-reconciliation
execution_mode: plan_only
status: READY
```

