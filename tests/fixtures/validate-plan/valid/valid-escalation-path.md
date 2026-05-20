---
validator_case: positive
---
# Valid: escalation recommended, system correctly recommends full-fog-workflow

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-fog-workflow
execution_mode: guided_execution
status: READY
system_recommended_workflow: full-fog-workflow
selected_workflow: full-fog-workflow
routing_divergence: false
routing_decision_method: escalation_recommended_accepted
escalation_recommended: true
auto_escalation_allowed: false
scope_expansion_requires_approval: true
initial_inputs:
  - id: user_intent
    type: artifact
    required: true
    source: user
  - id: raw_fog
    type: external_context
    required: true
    source: user
  - id: repository_state
    type: external_context
    required: true
    source: repository
steps:
  - id: 1
    skill: problem-framer
    status: PENDING
    step_type: local_execution
    gate: review_problem_frame
    input_source: raw_fog
    output_artifact: problem_frame
  - id: 2
    skill: unknowns-mapper
    status: PENDING
    step_type: local_execution
    gate: review_unknowns_map
    input_artifact: problem_frame
    output_artifact: unknowns_map
  - id: 3
    skill: repo-sensemaker
    status: PENDING
    step_type: local_execution
    gate: review_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 4
    skill: workflow-planner
    status: PENDING
    step_type: local_execution
    gate: review_orchestration_plan
    input_artifact: repository_sensemaking_brief
    output_artifact: workflow_orchestration_plan
approval_gates:
  - review_problem_frame
  - review_unknowns_map
  - review_diagnosis
  - review_orchestration_plan
gate_behavior:
  review_problem_frame: manual_review
  review_unknowns_map: manual_review
  review_diagnosis: manual_review
  review_orchestration_plan: manual_review
stop_conditions:
  - validator_failure
  - user_interrupt
```
