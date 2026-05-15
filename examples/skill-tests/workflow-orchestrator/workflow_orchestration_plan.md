# Workflow Orchestration Plan

## 1. Brief Consumed
`examples/skill-tests/repo-sensemaker/repo_sensemaking_brief.md`

## 2. Chosen Workflow
`setup-sensemaking-repo`

## 3. Why this workflow
The repository is in a "hardening" phase. This workflow ensures that agent documentation, artifact contracts, and validator scripts are correctly configured and reconciled.

## 4. Skills in Sequence
1. `setup-sensemaking-skills`
2. `repo-sensemaker`
3. `prompt-handoff`

## 5. Inputs and Outputs
- **Initial Input**: `repository_state`
- **Step 1 Output**: N/A (local_execution with gate)
- **Step 2 Output**: `repository_sensemaking_brief`
- **Step 3 Output**: `prompt_handoff`

## 6. Approval Gates
- **Gate 1**: `review_setup_plan`
- **Gate 2**: `review_repo_brief`
- **Gate 3**: `review_handoff_prompt`

## 7. Stop Conditions
- Fail if `repo-sensemaker` produces an invalid brief.
- Fail if `setup-sensemaking-skills` detects a structural mismatch in the environment.

## 8. Execution Mode
`plan_only`

## 9. Prompt Chain
N/A - mode is plan_only. No prompt chain generated.

## 10. Run Log Template
- **Run ID**: `iso-orch-001-run`
- **Log Path**: `examples/skill-tests/workflow-orchestrator/run_log.md`

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: setup-sensemaking-repo
execution_mode: plan_only
status: staged
initial_inputs:
  - id: repository_state
    type: external_context
    required: true
steps:
  - id: 1
    skill: setup-sensemaking-skills
    step_type: local_execution
    status: pending
    gate: review_setup_plan
    input_source: repository_state
  - id: 2
    skill: repo-sensemaker
    step_type: local_execution
    status: pending
    gate: review_repo_brief
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 3
    skill: prompt-handoff
    step_type: local_execution
    status: pending
    gate: review_handoff_prompt
    input_artifact: repository_sensemaking_brief
    output_artifact: prompt_handoff
approval_gates:
  - review_setup_plan
  - review_repo_brief
  - review_handoff_prompt
gate_behavior:
  review_setup_plan: stop_for_approval
  review_repo_brief: stop_for_approval
  review_handoff_prompt: stop_for_approval
stop_conditions:
  - artifact_validation_failure
  - env_mismatch
subset_run: false
subset_reason: N/A
included_steps: []
excluded_steps: []
```
