# Example: Local Command Failure Handling

## 1. Brief consumed
Diagnosis: Missing test coverage in `core/` module.
Weakest Boundary: Implementation gap.
Recommended Workflow: `fast-local-diagnostic`

## 2. Chosen workflow
`fast-local-diagnostic`

## 3. Why this workflow
Quickly produce a handoff prompt for the implementer.

## 4. Skills in sequence
1. `repo-sensemaker`
2. `handoff`

## 5. Inputs and outputs
- `repo-sensemaker`: Consumes repository state. Produces brief.
- `handoff`: Consumes brief. Produces handoff.

## 6. Approval gates
- **Gate 1**: Review brief.
- **Gate 2**: Review handoff.

## 7. Stop conditions
- Command failure.
- Malformed artifact.

## 8. Execution mode
`guided_execution`

## 9. Prompt chain
1. `/repo-sensemaker: Audit core/ for coverage gaps.`
2. `/handoff: Prepare test implementation prompt.`

## 10. Run log template
`docs/runs/tdd-failure-test.md`.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: fast-local-diagnostic
execution_mode: guided_execution
status: FAILED
subset_run: false

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
  review_sensemaking_brief: human_approval
  review_handoff_prompt: human_approval

stop_conditions:
  - command_failure
  - malformed_artifact
```

### Observed Failure (Simulation)
> **Orchestrator**: Attempting to execute `repo-sensemaker` command...
> **Error**: `local_command` failure.
> **Skill**: `repo-sensemaker`
> **Command**: `/repo-sensemaker`
> **Exit Code**: 1
> **Reason**: `claude_code` runtime not found in environment.
> **Action**: Stopping execution. Please ensure the `claude_code` runtime is installed and accessible.
