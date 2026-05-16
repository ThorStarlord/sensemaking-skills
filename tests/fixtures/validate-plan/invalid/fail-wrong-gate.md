---
validator_case: negative
expected_error_contains: "GATE_MISMATCH"
---
# Fail: wrong gate

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-contract-reconciliation
execution_mode: plan_only
status: READY
initial_inputs:
  - id: repository_state
    type: external_context
    source: repository
steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_drift_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 2
    skill: sensemaking-docs-reconciler
    step_type: local_execution
    gate: wrong_gate
    input_artifact: repository_sensemaking_brief
    output_artifact: docs_contract_reconciliation_report
  - id: 3
    skill: prompt-handoff
    step_type: local_execution
    gate: review_next_prompt
    input_artifact: docs_contract_reconciliation_report
    output_artifact: prompt_handoff
approval_gates:
  - review_drift_diagnosis
  - wrong_gate
  - review_next_prompt
stop_conditions:
  - user_rejection
```

