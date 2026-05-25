# Orchestration Plan: Fast Local Diagnostic

- **Session ID**: orchestration-20260523-181501-af0261dc
- **Date**: 2026-05-23
- **Workflow**: fast-local-diagnostic
- **Execution Mode**: yolo_execution

## 1. Brief consumed

Runtime-authored execution plan for `fast-local-diagnostic`. Consumes the run's initial inputs (repository_state); the upstream diagnostic brief, when produced by an earlier step, informs the routing recommendation recorded in the machine-readable plan.

## 2. Chosen workflow

`fast-local-diagnostic` — Fast Local Diagnostic

## 3. Why this workflow

Quickly identify the weakest boundary and produce a handoff prompt.

## 4. Skills in sequence

### Step 1: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_sensemaking_brief
- **Output**: repository_sensemaking_brief

### Step 2: handoff
- **Type**: local_execution
- **Gate**: review_handoff_prompt
- **Output**: session_summary

## 5. Inputs and outputs

- **repository_state** (external_context): Current repository files, registries, templates, validator scripts, and git state.

## 6. Approval gates

- **Mode**: yolo_execution
- **Gate behavior**: bypassed

- `review_sensemaking_brief`: bypassed
- `review_handoff_prompt`: bypassed

## 7. Stop conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

## 8. Execution mode

`yolo_execution` (gate behavior: bypassed, mutates repo: True).

## 9. Prompt chain

N/A - mode is `yolo_execution`; the runtime executes steps directly.

## 10. Run log template

```markdown
# Run Log: fast-local-diagnostic

| Step | Skill | Status | Artifact | Validation |
| :--- | :--- | :--- | :--- | :--- |
| 1 | repo-sensemaker | [ ] | [ ] | [ ] |
| 2 | handoff | [ ] | [ ] | [ ] |
```

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
source_intent_ref: 00-user-intent.md
chosen_workflow_id: fast-local-diagnostic
execution_mode: yolo_execution
system_recommended_workflow: fast-local-diagnostic
selected_workflow: fast-local-diagnostic
routing_divergence: false
routing_decision_method: diagnosis_primary_soft_context
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
status: created
session_id: orchestration-20260523-181501-af0261dc
initial_inputs:
- id: repository_state
  type: external_context
  required: true
  description: Current repository files, registries, templates, validator scripts,
    and git state.
steps:
- id: 1
  skill: repo-sensemaker
  step_type: local_execution
  gate: review_sensemaking_brief
  input_source: repository_state
  output_artifact: repository_sensemaking_brief
  status: pending
- id: 2
  skill: handoff
  step_type: local_execution
  gate: review_handoff_prompt
  input_artifact: repository_sensemaking_brief
  output_artifact: session_summary
  status: pending
approval_gates:
- review_sensemaking_brief
- review_handoff_prompt
gate_behavior:
  review_sensemaking_brief: bypassed
  review_handoff_prompt: bypassed
stop_conditions:
- id: validation_failure
- id: gate_denial
- id: step_failure
subset_run: false
subset_reason: null
included_steps:
- 1
- 2
excluded_steps: []
```
