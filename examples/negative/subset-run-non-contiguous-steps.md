# Workflow Orchestration Plan (FAIL: Non-contiguous subset)

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-local-sensemaking
execution_mode: guided_execution
status: IN_PROGRESS
subset_run: true
subset_reason: testing_non_contiguous_failure

included_steps:
  - 1
  - 3  # Skips step 2!

excluded_steps:
  - id: 2
    skill: unknowns-mapper
    reason: testing_non_contiguous_failure
  - id: 4
    skill: handoff
    reason: testing_non_contiguous_failure

steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    input_source: raw_fog
    output_artifact: problem_frame
    status: COMPLETED
  - id: 3
    skill: repo-sensemaker
    step_type: local_execution
    input_artifact: unknowns_map
    output_artifact: sensemaking_report
    status: PENDING

approval_gates: []
gate_behavior: {}
stop_conditions:
  - type: step_limit
    value: 2
```
