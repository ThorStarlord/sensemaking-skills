# Workflow Orchestration Plan (Subset Run Example)

## 1. Brief consumed
The user wants to evaluate the end-to-end usefulness of the `sensemaking-skills` pipeline, specifically moving from a vague idea ("I want this repo to help me turn messy ideas into useful AI workflows") to structured artifacts. The objective is to evaluate recent improvements to `problem-framer` and `unknowns-mapper` regarding handoff friction and routing clarity.

## 2. Chosen workflow
- **Workflow ID**: `full-local-sensemaking`
- **Display Name**: Full Local Sensemaking

## 3. Why this workflow
This workflow is the canonical path for transforming "raw fog" into a structured repository diagnosis. It includes the `problem-framer` and `unknowns-mapper` skills requested by the user.

## 4. Skills in sequence
1. **problem-framer**: Deconstructs the raw fog into a structured problem frame.
2. **unknowns-mapper**: Maps informational gaps and risks based on the problem frame.

*Note: Steps 3 (repo-sensemaker) and 4 (handoff) are excluded per user request.*

## 5. Inputs and outputs
- **Step 1**:
    - Input: `raw_fog` (User's vague idea)
    - Output: `problem_frame` (artifact)
- **Step 2**:
    - Input: `problem_frame` (artifact)
    - Output: `unknowns_map` (artifact)

## 6. Approval gates
- **Gate 1**: Review the `problem_frame` artifact.
- **Gate 2**: Review the `unknowns_map` artifact.

## 7. Stop conditions
- Validation failure at any step.
- Handoff contract violation.
- User rejection at an approval gate.
- Completion of Step 2.

## 8. Execution mode
- **Mode**: `guided_execution`
- **Behavior**: Execute one step, validate, update log, and stop for approval.

## 9. Prompt chain
- N/A - mode is `guided_execution`. No prompt chain generated.

## 10. Run log template
- [Run Log Template](../../skills/workflow-orchestrator/references/run-log-template.md)

## 10.5. Routing Decision Rationale

This fixture demonstrates a **diagnostic-stage scenario** where the problem domain is architectural (vague ideas about AI workflow orchestration patterns) but the workflow chosen is `full-local-sensemaking` (a diagnostic workflow, not an implementation workflow).

**Why this routing**: The repository is at a cold-start stage with messy, unstructured ideas about workflow architecture. The recommended approach is to apply structured sensemaking (problem-framing + unknowns-mapping) before attempting architectural implementation. This requires an intentional override from the canonical architecture-fog → architecture-implementation-workflow mapping to allow a diagnostic-phase workflow to execute first.

**Routing Decision Method**: `manual_override` — explicitly allows this workflow to execute despite the fog-to-workflow mismatch.

**Audit Trail**: The `routing_divergence: true` field records that this plan deviates from the system's default recommendation based on fog type alone.

## 11. Machine-readable plan
```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: full-local-sensemaking
execution_mode: guided_execution
status: COMPLETED
subset_run: true
subset_reason: user_requested_first_two_steps_only
primary_fog_type: architecture_fog
routing_decision_method: manual_override
routing_divergence: true
created_at: "2026-05-14T16:20:15Z"

initial_inputs:
  - id: raw_fog
    type: external_context
    required: true
  - id: repository_state
    type: repository_snapshot
    required: true

included_steps:
  - 1
  - 2

excluded_steps:
  - id: 3-conditional
    skill: ~
    reason: user_requested_stop_after_step_2
  - id: 4
    skill: repo-sensemaker
    reason: user_requested_stop_after_step_2
  - id: 5
    skill: workflow-planner
    reason: user_requested_stop_after_step_2
  - id: 6
    skill: handoff
    reason: user_requested_stop_after_step_2

workflow_steps:
  - id: 1
    skill: problem-framer
    step_type: local_execution
    input_source: raw_fog
    output_artifact: problem_frame
    gate: review_problem_frame
    status: COMPLETED

  - id: 2
    skill: unknowns-mapper
    step_type: local_execution
    input_artifact: problem_frame
    output_artifact: unknowns_map
    gate: review_unknowns_map
    status: COMPLETED

approval_gates:
  - review_problem_frame
  - review_unknowns_map

gate_behavior:
  review_problem_frame: simulated_for_research
  review_unknowns_map: simulated_for_research

stop_conditions:
  - type: step_limit
    value: 2
    reason: user_requested_first_two_steps_only
  - type: validation_failure
```
