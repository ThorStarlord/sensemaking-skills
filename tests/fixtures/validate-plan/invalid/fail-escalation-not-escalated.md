---
validator_case: negative
expected_error_contains: "CONFLICT_NOT_ESCALATED"
---
# Fail: escalation recommended but system does not recommend full-fog-workflow

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: fast-path-workflow
execution_mode: guided_execution
status: READY
system_recommended_workflow: fast-path-workflow
selected_workflow: fast-path-workflow
routing_divergence: false
routing_decision_method: diagnosis_primary_soft_context
escalation_recommended: true
auto_escalation_allowed: false
scope_expansion_requires_approval: true
initial_inputs:
  - id: user_intent
    type: artifact
    required: true
    source: user
steps:
  - id: 1
    skill: repo-sensemaker
    status: PENDING
    step_type: local_execution
    gate: review_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 2
    skill: workflow-planner
    status: PENDING
    step_type: local_execution
    gate: review_orchestration_plan
    input_artifact: repository_sensemaking_brief
    output_artifact: workflow_orchestration_plan
approval_gates:
  - review_diagnosis
  - review_orchestration_plan
gate_behavior:
  review_diagnosis: manual_review
  review_orchestration_plan: manual_review
stop_conditions:
  - validator_failure
  - user_interrupt
```
