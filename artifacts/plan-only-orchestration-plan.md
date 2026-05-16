# Workflow Orchestration Plan

## 1. Brief consumed
Repository sensemaking brief for `sensemaking-skills` (artifacts/repository_sensemaking_brief.md).
Identifies "Contract Mismatch" as the weakest boundary: the run-log-template.md structure does not fully align with the validator ecosystem's expectations. Recommends `docs-contract-reconciliation` in `guided_execution` mode.

## 2. Chosen workflow
`fast-local-diagnostic` — 2-step workflow (repo-sensemaker → handoff). Supports all 5 execution modes including `plan_only`.

## 3. Why this workflow
The PRD-mode-proving-automation requires `plan_only` to be proven on a workflow where the input brief already exists. `fast-local-diagnostic` meets this with zero additional cost: the repository_sensemaking_brief exists, the workflow is the simplest in the registry (2 steps, local-only), and proving `plan_only` here exercises the Section 11 production path for the first time.

## 4. Skills in sequence
| Step | Skill | Step Type | Output Artifact |
|:----:|-------|:---------:|:---------------:|
| 1 | repo-sensemaker | local_execution | repository_sensemaking_brief |
| 2 | handoff | local_execution | prompt_handoff |

## 5. Inputs and outputs
- **Initial input**: `repository_state` (current repository files, registries, templates, validator scripts, and git state)
- **Step 1**: Input = `repository_state`, Output = `repository_sensemaking_brief`
- **Step 2**: Input = `repository_sensemaking_brief`, Output = `prompt_handoff`

## 6. Approval gates
| Step | Gate | Behavior |
|:----:|------|:--------:|
| 1 | `review_sensemaking_brief` | N/A (plan_only — no gates exercised) |
| 2 | `review_handoff_prompt` | N/A (plan_only — no gates exercised) |

## 7. Stop conditions
- Plan artifact fails Section 11 validation
- validate-plan.py returns non-zero
- Run log cannot be written

## 8. Execution mode
`plan_only`

## 9. Prompt chain
N/A — mode is plan_only. No prompt chain generated.

## 10. Run log template
Run log recorded at `artifacts/plan_only_run_log.md` per run-log-template.md.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: fast-local-diagnostic
execution_mode: plan_only
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
  review_sensemaking_brief: not_applicable_plan_only
  review_handoff_prompt: not_applicable_plan_only
stop_conditions:
  - Plan artifact fails Section 11 validation
  - validate-plan.py returns non-zero
  - Run log cannot be written
subset_run: false
subset_reason: null
included_steps: []
excluded_steps: []
```
