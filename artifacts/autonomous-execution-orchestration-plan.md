# Workflow Orchestration Plan

## 1. Brief consumed
Repository sensemaking brief for `sensemaking-skills` (artifacts/repository_sensemaking_brief.md).
Identifies "Contract Mismatch" as the weakest boundary.

## 2. Chosen workflow
`fast-local-diagnostic` — 2-step workflow (repo-sensemaker → handoff). Supports `autonomous_execution`.

## 3. Why this workflow
Mode proving requires autonomous_execution to be proven on a workflow that supports it.
`fast-local-diagnostic` is the simplest autonomous-eligible workflow (2 steps, local-only).
The brief already exists, making this a low-risk proving target.

## 4. Skills in sequence
| Step | Skill | Step Type | Output Artifact |
|:----:|-------|:---------:|:---------------:|
| 1 | repo-sensemaker | local_execution | repository_sensemaking_brief |
| 2 | handoff | local_execution | prompt_handoff |

## 5. Inputs and outputs
- **Initial input**: `repository_state`
- **Step 1**: Input = `repository_state`, Output = `repository_sensemaking_brief`
- **Step 2**: Input = `repository_sensemaking_brief`, Output = `prompt_handoff`

## 6. Approval gates
| Step | Gate | Behavior |
|:----:|------|:--------:|
| 1 | `review_sensemaking_brief` | automated_approval (autonomous mode — user opted in) |
| 2 | `review_handoff_prompt` | automated_approval (autonomous mode — user opted in) |

## 7. Stop conditions
- Validator failure at any step (zero tolerance)
- Opt-in string not provided
- Dirty worktree before execution
- Current branch is main or master

## 8. Execution mode
`autonomous_execution`

## 9. Prompt chain
N/A — autonomous_execution executes steps directly. Use run log for step details.

## 10. Run log template
Run log recorded at `artifacts/autonomous_execution_run_log.md` per run-log-template.md.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: fast-local-diagnostic
execution_mode: autonomous_execution
status: proposed
initial_inputs:
  - id: repository_state
    type: external_context
    required: true
steps:
  - id: "1"
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_sensemaking_brief
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
    status: planned
  - id: "2"
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    input_artifact: repository_sensemaking_brief
    output_artifact: prompt_handoff
    status: planned
approval_gates:
  - review_sensemaking_brief
  - review_handoff_prompt
gate_behavior:
  review_sensemaking_brief: automated_approval
  review_handoff_prompt: automated_approval
stop_conditions:
  - Validator failure at any step
  - Opt-in string not provided
  - Dirty worktree before execution
  - Branch is main or master
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
```
