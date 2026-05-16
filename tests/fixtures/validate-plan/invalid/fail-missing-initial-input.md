---
validator_case: negative
expected_error_contains: "INPUT_MISMATCH"
---
# Fail: missing initial input

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-contract-reconciliation
execution_mode: plan_only
status: READY
initial_inputs: []
steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_drift_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
```

