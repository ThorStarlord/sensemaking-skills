---
validator_case: negative
expected_error_contains: "EXECUTION_MODE_DENIED"
---
# Fail: disallowed mode

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-contract-reconciliation
execution_mode: yolo_execution
status: READY
initial_inputs:
  - id: repository_state
    type: external_context
    source: repository
```

