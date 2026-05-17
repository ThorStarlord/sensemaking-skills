# Workflow Orchestration Plan

## 1. Brief consumed
The repository `sensemaking-skills` is a modular agentic framework for reducing information entropy. The core objective is to bridge the gap between "messy ideas" and "useful workflows." The diagnosis identifies the `full-local-sensemaking` workflow as the primary path for cold-start scenarios.

## 2. Chosen workflow
Full Local Sensemaking

## 3. Why this workflow
This workflow directly addresses the weakest boundary (semantic-handoff-continuity) by providing a complete, auditable chain from raw fog to prompt handoff, ensuring that each step validates the prior artifact's contract.

## 4. Skills in sequence
1. `problem-framer`
2. `unknowns-mapper`
3. (Conditional) `discovery` - if `unknowns_map.research_needed == true`; otherwise skip
4. `repo-sensemaker`
5. `handoff`

## 5. Inputs and outputs
- **Step 1**: `raw_fog` -> `problem_frame`
- **Step 2**: `problem_frame` -> `unknowns_map`
- **Step 3 (Conditional)**:
  - If true: `unknowns_map` -> `discovery_findings`
  - If false: Pass through `unknowns_map`
- **Step 4**: (from step 3 pass-through) + `repository_state` -> `repository_sensemaking_brief`
- **Step 5**: `repository_sensemaking_brief` -> `prompt_handoff`

## 6. Approval gates
- `review_problem_frame`
- `review_unknowns_map`
- `review_sensemaking_brief`
- `review_final_prompt`

## 7. Stop conditions
- Missing input artifact.
- Failed Level 2 or Level 3 validation.
- Dirty git state (for execution modes > guided).

## 8. Execution mode
`plan_only`

## 9. Prompt chain
N/A - mode is plan_only. No prompt chain generated.

## 10. Run log template
Refer to `skills/workflow-orchestrator/references/run-log-template.md`.

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
    description: High-level project description, ambiguous ideas, or strategic goals.
    value: "I want this repo to help me turn messy ideas into useful AI workflows."
  - id: repository_state
    type: external_context
    required: true
    description: Current repository files, registries, templates, validator scripts, and git state.
    value: "current"
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
    skill: handoff
    step_type: local_execution
    gate: review_final_prompt
    input_artifact: repository_sensemaking_brief
    output_artifact: prompt_handoff
    status: pending
approval_gates:
  - review_problem_frame
  - review_unknowns_map
  - review_sensemaking_brief
  - review_final_prompt
gate_behavior:
  review_problem_frame: manual_approval
  review_unknowns_map: manual_approval
  review_sensemaking_brief: manual_approval
  review_final_prompt: manual_approval
stop_conditions:
  - id: validation_failure
    description: "Stop if any artifact fails Level 2 or Level 3 validation."
  - id: contract_drift
    description: "Stop if artifact handoff contract is violated."
subset_run: false
subset_reason: n/a
included_steps: []
excluded_steps: []
```
