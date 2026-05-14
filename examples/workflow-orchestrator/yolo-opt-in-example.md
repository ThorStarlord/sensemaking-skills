# Example: YOLO Execution Plan

## 1. Brief consumed
Diagnosis: High-velocity implementation of internal utility scripts.
Weakest Boundary: Manual script updates.
Recommended Workflow: `fast-local-diagnostic`

## 2. Chosen workflow
`fast-local-diagnostic`

## 3. Why this workflow
The user explicitly requested YOLO mode for rapid internal tooling updates.

## 4. Skills in sequence
1. `repo-sensemaker`
2. `handoff`

## 5. Inputs and outputs
- `repo-sensemaker`: Consumes repository state. Produces sensemaking brief.
- `handoff`: Consumes brief. Produces implementation prompt.

## 6. Approval gates
- **Gate 1**: Bypassed (YOLO mode).
- **Gate 2**: Bypassed (YOLO mode).

## 7. Stop conditions
- Missing artifact.
- Failed validation.
- Non-executable skill.
- Dirty git state.

## 8. Execution mode
`yolo_execution`

## 9. Prompt chain
1. `/repo-sensemaker: Audit the scripts/ directory.`
2. `/handoff: Prepare the upgrade prompt.`

## 10. Run log template
Initialized at `docs/runs/yolo-2026-05-14.md`.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: fast-local-diagnostic
execution_mode: yolo_execution
status: PENDING
subset_run: false
yolo_opt_in: "I choose yolo_execution and accept automated repository changes, feature-branch commits, bypassed gates, and recovery risk."
initial_inputs:
  - id: repository_state
    type: repository_snapshot
    required: true
steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_sensemaking_brief
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
    status: PENDING
  - id: 2
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    input_artifact: repository_sensemaking_brief
    output_artifact: prompt_handoff
    status: PENDING
approval_gates:
  - review_sensemaking_brief
  - review_handoff_prompt
gate_behavior:
  review_sensemaking_brief: bypassed_by_yolo
  review_handoff_prompt: bypassed_by_yolo
stop_conditions:
  - missing_artifact
  - failed_validation
  - non_executable_skill
  - dirty_git_state
```
