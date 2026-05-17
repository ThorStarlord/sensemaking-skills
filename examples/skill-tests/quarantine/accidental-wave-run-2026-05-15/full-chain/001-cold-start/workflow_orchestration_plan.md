# Workflow Orchestration Plan

## 1. Brief Consumed
`examples/skill-tests/full-chain/001-cold-start/repo_sensemaking_brief.md`

## 2. Chosen Workflow
`full-local-sensemaking`

## 3. Why this workflow
This is the standard pipeline for converting raw fog into a repository diagnosis and downstream handoff. We are currently at the final stage (Handoff) following the successful production of the Repository Sensemaking Brief.

## 4. Skills in Sequence
1. `problem-framer` (Completed)
2. `unknowns-mapper` (Completed)
3. (Conditional) `discovery` (Skipped - no research needed)
4. `repo-sensemaker` (Completed)
5. `handoff` (Pending)

## 5. Inputs and Outputs
- **Initial Input**: `raw_fog`, `repository_state`
- **Step 5 Output**: `prompt_handoff`

## 6. Approval Gates
- **Gate 1**: `review_problem_frame` (Bypassed)
- **Gate 2**: `review_unknowns_map` (Bypassed)
- **Gate 3**: `review_sensemaking_brief` (Bypassed)
- **Gate 4**: `review_final_prompt` (Pending)

## 7. Stop Conditions
- Fail if `handoff` output does not satisfy the `prompt_handoff` contract.
- Fail if `validate-repo.py` detects a registry breach.

## 8. Execution Mode
`plan_only`

## 9. Prompt Chain
N/A - mode is plan_only. No prompt chain generated.

## 10. Run Log Template
- **Run ID**: `chain-001-run`
- **Log Path**: `examples/skill-tests/full-chain/001-cold-start/run_log.md`

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-local-sensemaking
execution_mode: plan_only
status: staged
initial_inputs:
  - id: raw_fog
    type: external_context
    required: true
  - id: repository_state
    type: external_context
    required: true
steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    status: completed
    gate: review_problem_frame
    input_source: raw_fog
    output_artifact: problem_frame
  - id: 2
    skill: unknowns-mapper
    step_type: local_execution
    status: completed
    gate: review_unknowns_map
    input_artifact: problem_frame
    output_artifact: unknowns_map
  - id: 3-conditional
    skill: ~
    conditional: true
    decision_field: unknowns_map.research_needed
    if_true:
      skill: discovery
      step_type: external_routing
      gate: review_discovery
      input_artifact: unknowns_map
      output_artifact: discovery_findings
      next_step: 4
    if_false:
      output_artifact: unknowns_map
      next_step: 4
    status: completed
  - id: 4
    skill: repo-sensemaker
    step_type: local_execution
    status: completed
    gate: review_sensemaking_brief
    input_artifact: unknowns_map
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 5
    skill: handoff
    step_type: local_execution
    status: pending
    gate: review_final_prompt
    input_artifact: repository_sensemaking_brief
    output_artifact: prompt_handoff
approval_gates:
  - review_problem_frame
  - review_unknowns_map
  - review_sensemaking_brief
  - review_final_prompt
gate_behavior:
  review_problem_frame: stop_for_approval
  review_unknowns_map: stop_for_approval
  review_sensemaking_brief: stop_for_approval
  review_final_prompt: stop_for_approval
stop_conditions:
  - artifact_validation_failure
  - registry_breach
subset_run: false
subset_reason: N/A
included_steps: []
excluded_steps: []
```
