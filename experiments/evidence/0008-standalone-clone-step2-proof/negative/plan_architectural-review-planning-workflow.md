# Orchestration Plan: Architectural Review Planning

- **Session ID**: step2-negative-session
- **Date**: 2026-07-25
- **Workflow**: architectural-review-planning-workflow
- **Execution Mode**: guided_execution

## 1. Brief consumed

Runtime-authored execution plan for `architectural-review-planning-workflow`. Consumes the run's initial inputs (repository_state, proposed_direction); the upstream diagnostic brief, when produced by an earlier step, informs the routing recommendation recorded in the machine-readable plan.

## 2. Chosen workflow

`architectural-review-planning-workflow` — Architectural Review Planning

## 3. Why this workflow

Evaluate a proposed architectural response against repository diagnostics and risks.

## 4. Skills in sequence

### Step 1: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_diagnosis
- **Output**: repository_sensemaking_brief

### Step 2: architectural-review
- **Type**: local_execution
- **Gate**: review_recommendation
- **Output**: architectural_review_recommendation

## 5. Inputs and outputs

- **repository_state** (external_context): Current repository files, folder structure, README, documentation, and git state.
- **proposed_direction** (external_context): The proposed architectural response, feature, or capability to evaluate.

## 6. Approval gates

- **Mode**: guided_execution
- **Gate behavior**: mandatory

- `review_diagnosis`: mandatory
- `review_recommendation`: mandatory

## 7. Stop conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

## 8. Execution mode

`guided_execution` (gate behavior: mandatory, mutates repo: True).

## 9. Prompt chain

N/A - mode is `guided_execution`; the runtime executes steps directly.

## 10. Run log template

```markdown
# Run Log: architectural-review-planning-workflow

| Step | Skill | Status | Artifact | Validation |
| :--- | :--- | :--- | :--- | :--- |
| 1 | repo-sensemaker | [ ] | [ ] | [ ] |
| 2 | architectural-review | [ ] | [ ] | [ ] |
```

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
source_intent_ref: 00-user-intent.md
chosen_workflow_id: architectural-review-planning-workflow
execution_mode: guided_execution
system_recommended_workflow: architectural-review-planning-workflow
selected_workflow: architectural-review-planning-workflow
routing_divergence: false
routing_decision_method: diagnosis_primary_soft_context
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
status: created
session_id: step2-negative-session
initial_inputs:
- id: repository_state
  type: external_context
  required: true
  description: Current repository files, folder structure, README, documentation,
    and git state.
- id: proposed_direction
  type: external_context
  required: true
  description: The proposed architectural response, feature, or capability to evaluate.
steps:
- id: 1
  skill: repo-sensemaker
  step_type: local_execution
  gate: review_diagnosis
  input_source: repository_state
  output_artifact: repository_sensemaking_brief
  description: Diagnose repository state and identify the weakest boundary
  status: pending
- id: 2
  skill: architectural-review
  step_type: local_execution
  gate: review_recommendation
  input_artifact: repository_sensemaking_brief
  input_source: proposed_direction
  output_artifact: architectural_review_recommendation
  description: Evaluate proposed response against diagnosed fog and identify risks
  status: pending
approval_gates:
- review_diagnosis
- review_recommendation
gate_behavior:
  review_diagnosis: mandatory
  review_recommendation: mandatory
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
