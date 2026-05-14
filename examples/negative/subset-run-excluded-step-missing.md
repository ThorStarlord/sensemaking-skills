# Workflow Orchestration Plan (FAIL: Missing excluded step)

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-local-sensemaking
execution_mode: guided_execution
status: IN_PROGRESS
subset_run: true
subset_reason: testing_missing_step_accounting

included_steps: [1, 2]
excluded_steps:
  - id: 3
    skill: repo-sensemaker
    reason: test
  # STEP 4 IS MISSING!

steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    input_source: raw_fog
    output_artifact: problem_frame
    status: COMPLETED
  - id: 2
    skill: unknowns-mapper
    step_type: local_execution
    input_artifact: problem_frame
    output_artifact: unknowns_map
    status: PENDING

approval_gates: []
gate_behavior: {}
stop_conditions:
  - type: step_limit
    value: 2
```
