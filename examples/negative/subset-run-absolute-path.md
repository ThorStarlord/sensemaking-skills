# Workflow Orchestration Plan (FAIL: Absolute path)

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-local-sensemaking
execution_mode: guided_execution
status: COMPLETED
subset_run: false

initial_inputs:
  - id: raw_fog
    type: external_context
    required: true
  - id: repository_state
    type: repository_snapshot
    required: true

steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    input_source: raw_fog
    output_artifact: problem_frame
    status: COMPLETED
    # ABSOLUTE PATH BELOW
    artifact_path: C:\Users\Admin\Desktop\problem_frame.md 

approval_gates: []
gate_behavior: {}
stop_conditions:
  - type: step_limit
    value: 1
```
