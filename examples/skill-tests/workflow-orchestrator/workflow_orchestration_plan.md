# Workflow Orchestration Plan

## 1. Brief consumed
The `repo_sensemaking_brief.md` identifies a semantic translation gap between "messy ideas" and executable AI workflows. It highlights `workflow-registry.yaml` as the Object Under Pressure and recommends stabilizing the repository baseline through Wave 1 completion. The brief notes Path Hygiene as the weakest boundary.

## 2. Chosen workflow
Full Local Sensemaking

## 3. Why this workflow
This workflow provides the end-to-end bridge (Framer -> Mapper -> Sensemaker -> Handoff) required to transform the "messy ideas" identified in the brief into a validated repository diagnosis and executable handoff prompt. It directly addresses the "hallucinated workflow" failure mode by introducing structured sensemaking.

## 4. Skills in sequence
1. `problem-framer`
2. `unknowns-mapper`
3. (Conditional) `discovery` - if `unknowns_map.research_needed == true`; otherwise skip
4. `repo-sensemaker`
5. `workflow-planner`
6. `handoff`

## 5. Inputs and outputs
- **Step 1**: Input `raw_fog`, Output `problem_frame`.
- **Step 2**: Input `problem_frame`, Output `unknowns_map`.
- **Step 3 (Conditional)**:
  - If true: Input `unknowns_map`, Output `discovery_findings`.
  - If false: Pass through `unknowns_map`.
- **Step 4**: Input (from step 3 pass-through), Output `repository_sensemaking_brief`.
- **Step 5**: Input `repository_sensemaking_brief`, Output `workflow_orchestration_plan`.
- **Step 6**: Input `workflow_orchestration_plan`, Output `session_summary`.

## 6. Approval gates
- **Gate 1**: `review_problem_frame` (Manual verification of framing accuracy).
- **Gate 2**: `review_unknowns_map` (Verification of research path completeness).
- **Gate 3**: `review_discovery` (Audit of discovery findings if needed).
- **Gate 4**: `review_sensemaking_brief` (Audit of weakest boundary identification).
- **Gate 5**: `none` (Automatic workflow planning).
- **Gate 6**: `review_final_prompt` (Confirmation of handoff readiness).

## 7. Stop conditions
- **Structural Failure**: Stop if any generated artifact fails Level 2 (Generic) validation.
- **Ambiguity**: Stop if `problem-framer` fails to identify a clear Object Under Pressure.
- **Contract Drift**: Stop if `unknowns-mapper` identifies information gaps that cannot be resolved within the current repository scope.

## 8. Execution mode
`plan_only`

## 9. Prompt chain
N/A - mode is plan_only. No prompt chain generated.

## 10. Run log template
```markdown
# Run Log: full-local-sensemaking

| Step | Skill | Status | Artifact | Validation |
| :--- | :--- | :--- | :--- | :--- |
| 1 | problem-framer | [ ] | [ ] | [ ] |
| 2 | unknowns-mapper | [ ] | [ ] | [ ] |
| 3 | (conditional) discovery | [ ] | [ ] | [ ] |
| 4 | repo-sensemaker | [ ] | [ ] | [ ] |
| 5 | workflow-planner | [ ] | [ ] | [ ] |
| 6 | handoff | [ ] | [ ] | [ ] |
```

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
    skill: workflow-planner
    step_type: local_execution
    gate: none
    input_artifact: repository_sensemaking_brief
    output_artifact: workflow_orchestration_plan
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
  review_problem_frame: mandatory
  review_unknowns_map: mandatory
  review_sensemaking_brief: mandatory
  none: automatic
  review_final_prompt: mandatory
stop_conditions:
  - id: validation_failure
  - id: ambiguous_oup
subset_run: false
subset_reason: null
included_steps: [1, 2, '3-conditional', 4, 5, 6]
excluded_steps: []
```
