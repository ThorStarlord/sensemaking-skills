# Workflow Orchestration Plan: YOLO Dry-Run Test (FAILURE CASE)

## 1. Brief consumed
[repository_sensemaking_brief](examples/negative/yolo-hallucination-failure.md)

## 2. Chosen workflow
`fast-local-diagnostic`

## 3. Why this workflow
To verify fail-fast behavior in YOLO mode starting from the diagnostic brief.

## 4. Skills in sequence
1. `repo-sensemaker` (Produces `repository_sensemaking_brief`)
2. `handoff` (Produces `prompt_handoff`)

## 5. Inputs and outputs
- Step 1:
  - Input Source: `repository_state`
  - Output Artifact: `repository_sensemaking_brief`
- Step 2:
  - Input Artifact: `repository_sensemaking_brief`
  - Output Artifact: `prompt_handoff`

## 6. Approval gates
- `review_sensemaking_brief` (Bypassed by YOLO)
- `review_handoff_prompt` (Bypassed by YOLO)

## 7. Stop conditions
- `validator_failure`: Halt on any validator failure.
- `missing_artifact`: Halt if a skill fails to produce its declared output.

## 8. Execution mode
`yolo_execution`

## 9. Prompt chain
N/A - mode is yolo_execution. No static prompt chain generated.

## 10. Run log template
`examples/workflow-orchestrator/yolo-dry-run-failure-log.md`

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: fast-local-diagnostic
execution_mode: yolo_execution
status: FAILED
subset_run: false
dry_run: true
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
    status: FAILED
  - id: 2
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    input_artifact: repository_sensemaking_brief
    output_artifact: prompt_handoff
    status: CANCELLED
approval_gates:
  - review_sensemaking_brief
  - review_handoff_prompt
gate_behavior:
  review_sensemaking_brief: bypassed_by_yolo
  review_handoff_prompt: bypassed_by_yolo
stop_conditions:
  - id: validator_failure
    description: Halt on any validator failure.
```
