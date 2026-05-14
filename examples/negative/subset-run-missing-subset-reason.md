# Workflow Orchestration Plan (FAIL: Missing subset reason)

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-local-sensemaking
execution_mode: guided_execution
status: IN_PROGRESS
subset_run: true
# MISSING subset_reason

included_steps: [1]
excluded_steps:
  - id: 2
    skill: unknowns-mapper
    reason: test
  - id: 3
    skill: repo-sensemaker
    reason: test
  - id: 4
    skill: handoff
    reason: test

steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    input_source: raw_fog
    output_artifact: problem_frame
    status: COMPLETED

approval_gates: []
gate_behavior: {}
stop_conditions:
  - type: step_limit
    value: 1
```
