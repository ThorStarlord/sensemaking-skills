# Orchestration Plan: Full Local Sensemaking

- **Session ID**: orchestration-20260516-203735-cf32c251
- **Date**: 2026-05-16
- **Workflow**: full-local-sensemaking
- **Execution Mode**: yolo_execution
- **Purpose**: Convert raw fog into a repository diagnosis and downstream handoff using only local executable skills.

## Skills in Sequence

### Step 1: problem-framer
- **Type**: local_execution
- **Gate**: review_problem_frame
- **Output**: problem_frame

### Step 2: unknowns-mapper
- **Type**: local_execution
- **Gate**: review_unknowns_map
- **Output**: unknowns_map

### Step 3: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_sensemaking_brief
- **Output**: repository_sensemaking_brief

### Step 4: handoff
- **Type**: local_execution
- **Gate**: review_final_prompt
- **Output**: prompt_handoff

## Inputs and Outputs

- **raw_fog** (external_context): High-level project description, ambiguous ideas, or strategic goals.
- **repository_state** (external_context): Current repository files, registries, templates, validator scripts, and git state.

## Approval Gates

- **Mode**: yolo_execution
- **Gate Behavior**: bypassed

- review_problem_frame: BYPASSED
- review_unknowns_map: BYPASSED
- review_sensemaking_brief: BYPASSED
- review_final_prompt: BYPASSED

## Stop Conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

---

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-local-sensemaking
execution_mode: yolo_execution
status: created
session_id: orchestration-20260516-203735-cf32c251
initial_inputs:
  raw_fog: external_context
  repository_state: external_context
steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    gate: review_problem_frame
    output_artifact: problem_frame
  - id: 2
    skill: unknowns-mapper
    step_type: local_execution
    gate: review_unknowns_map
    output_artifact: unknowns_map
  - id: 3
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_sensemaking_brief
    output_artifact: repository_sensemaking_brief
  - id: 4
    skill: handoff
    step_type: local_execution
    gate: review_final_prompt
    output_artifact: prompt_handoff
approval_gates:
  behavior: bypassed
stop_conditions:
  - validator_failure
  - gate_denial
  - step_failure
```
