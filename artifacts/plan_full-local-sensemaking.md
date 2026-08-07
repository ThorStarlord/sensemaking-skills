# Orchestration Plan: Full Local Sensemaking

- **Session ID**: orchestration-20260803-211126-2a68f975
- **Date**: 2026-08-03
- **Workflow**: full-local-sensemaking
- **Execution Mode**: plan_only

## 1. Brief consumed

Runtime-authored execution plan for `full-local-sensemaking`. Consumes the run's initial inputs (raw_fog, repository_state); the upstream diagnostic brief, when produced by an earlier step, informs the routing recommendation recorded in the machine-readable plan.

## 2. Chosen workflow

`full-local-sensemaking` — Full Local Sensemaking

## 3. Why this workflow

Convert raw fog into a repository diagnosis and downstream handoff using only local executable skills.

## 4. Skills in sequence

### Step 1: problem-framer
- **Type**: local_execution
- **Gate**: review_problem_frame
- **Output**: problem_frame

### Step 2: unknowns-mapper
- **Type**: local_execution
- **Gate**: review_unknowns_map
- **Output**: unknowns_map

### Step 3-conditional: discovery (conditional)
- **Type**: local_execution
- **Gate**: review_discovery
- **Output**: discovery_findings or unknowns_map

### Step 4: repo-sensemaker
- **Type**: local_execution
- **Gate**: review_sensemaking_brief
- **Output**: repository_sensemaking_brief

### Step 5: workflow-planner
- **Type**: local_execution
- **Gate**: none
- **Output**: workflow_orchestration_plan

### Step 6: handoff
- **Type**: local_execution
- **Gate**: review_final_prompt
- **Output**: session_summary

## 5. Inputs and outputs

- **raw_fog** (external_context): High-level project description, ambiguous ideas, or strategic goals.
- **repository_state** (external_context): Current repository files, registries, templates, validator scripts, and git state.

## 6. Approval gates

- **Mode**: plan_only
- **Gate behavior**: none

- `review_problem_frame`: none
- `review_unknowns_map`: none
- `review_sensemaking_brief`: none
- `none`: automatic
- `review_final_prompt`: none

## 7. Stop conditions

- Validator failure at any level -> HALT
- Gate denial -> HALT (rollback recommended for mutating modes)
- Step execution failure -> HALT
- Final step completed -> SUCCESS

## 8. Execution mode

`plan_only` (gate behavior: none, mutates repo: False).

## 9. Prompt chain

N/A - mode is `plan_only`; the runtime executes steps directly.

## 10. Run log template

```markdown
# Run Log: full-local-sensemaking

| Step | Skill | Status | Artifact | Validation |
| :--- | :--- | :--- | :--- | :--- |
| 1 | problem-framer | [ ] | [ ] | [ ] |
| 2 | unknowns-mapper | [ ] | [ ] | [ ] |
| 3-conditional | discovery (conditional) | [ ] | [ ] | [ ] |
| 4 | repo-sensemaker | [ ] | [ ] | [ ] |
| 5 | workflow-planner | [ ] | [ ] | [ ] |
| 6 | handoff | [ ] | [ ] | [ ] |
```

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
source_intent_ref: 00-user-intent.md
chosen_workflow_id: full-local-sensemaking
execution_mode: plan_only
system_recommended_workflow: full-local-sensemaking
selected_workflow: full-local-sensemaking
routing_divergence: false
routing_decision_method: diagnosis_primary_soft_context
escalation_recommended: false
auto_escalation_allowed: false
scope_expansion_requires_approval: true
status: created
session_id: orchestration-20260803-211126-2a68f975
initial_inputs:
- id: raw_fog
  type: external_context
  required: true
  description: High-level project description, ambiguous ideas, or strategic goals.
- id: repository_state
  type: external_context
  required: true
  description: Current repository files, registries, templates, validator scripts,
    and git state.
steps:
- id: 1
  skill: problem-framer
  step_type: local_execution
  gate: review_problem_frame
  input_source: raw_fog
  output_artifact: problem_frame
  status: pending
- id: 2
  skill: unknowns-mapper
  step_type: local_execution
  gate: review_unknowns_map
  input_artifact: problem_frame
  output_artifact: unknowns_map
  status: pending
- id: 3-conditional
  skill: null
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
  condition_rule: If unknowns_map.research_needed == true, insert discovery (producing
    discovery_findings); else skip and pass through unknowns_map to repo-sensemaker
  status: pending
- id: 4
  skill: repo-sensemaker
  step_type: local_execution
  gate: review_sensemaking_brief
  input_artifact: unknowns_map
  input_source: repository_state
  output_artifact: repository_sensemaking_brief
  status: pending
- id: 5
  skill: workflow-planner
  step_type: local_execution
  gate: none
  input_artifact: repository_sensemaking_brief
  output_artifact: workflow_orchestration_plan
  description: Orchestration planning - select implementation workflow based on fog
    type
  status: pending
- id: 6
  skill: handoff
  step_type: local_execution
  gate: review_final_prompt
  input_artifact: workflow_orchestration_plan
  output_artifact: session_summary
  status: pending
approval_gates:
- review_problem_frame
- review_unknowns_map
- review_sensemaking_brief
- none
- review_final_prompt
gate_behavior:
  review_problem_frame: none
  review_unknowns_map: none
  review_sensemaking_brief: none
  none: automatic
  review_final_prompt: none
stop_conditions:
- id: validation_failure
- id: gate_denial
- id: step_failure
subset_run: false
subset_reason: null
included_steps:
- 1
- 2
- 3-conditional
- 4
- 5
- 6
excluded_steps: []
```
