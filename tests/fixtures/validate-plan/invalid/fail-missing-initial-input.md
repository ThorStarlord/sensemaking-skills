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
primary_fog_type: architecture_fog
routing_decision_method: manual_override
created_at: \"2026-05-19T16:00:00Z\"
initial_inputs: []
workflow_steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_drift_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
```

