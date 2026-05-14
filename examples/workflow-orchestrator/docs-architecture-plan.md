# Example: Workflow Orchestration Plan (Docs Architecture)

## 1. Brief consumed
Diagnosis: Vocabulary drift between `README.md` and `skills/`.
Weakest Boundary: System documentation hierarchy.
Recommended Workflow: `docs-architecture`

## 2. Chosen workflow
`docs-architecture`

## 3. Why this workflow
It specifically addresses documentation misalignment by using `grill-with-docs` and `to-prd`.

## 4. Skills in sequence
1. `grill-with-docs`
2. `to-prd`
3. `handoff`

## 5. Inputs and outputs
- `grill-with-docs`: Receives Brief + Context. Produces Alignment Report.
- `to-prd`: Receives Alignment Report. Produces updated PRD.
- `handoff`: Receives final PRD. Produces Session Summary.

## 6. Approval gates
- **Gate 1**: Review Alignment Report (after `grill-with-docs`).
- **Gate 2**: Review updated PRD (after `to-prd`).
- **Gate 3**: Review Handoff Prompt.

## 7. Stop conditions
- If `grill-with-docs` identifies a major architectural contradiction that requires a human decision.

## 8. Execution mode
`guided_execution` (Defaulting from brief recommendation).

## 9. Prompt chain
1. `/grill-with-docs: Align the system vocab in README with the new skill structure.`
2. `/to-prd: Update the V1 PRD based on the alignment report.`
3. `/handoff: Summarize the doc hardening.`

## 10. Run log template
Initialized at `docs/runs/2026-05-13-docs-alignment.md`.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-architecture
execution_mode: guided_execution
initial_inputs:
  - id: repository_state
    type: external_context
steps:
  - id: 1
    skill: grill-with-docs
    step_type: local_execution
    gate: review_alignment_report
    input_source: repository_state
    output_artifact: domain_alignment_report
  - id: 2
    skill: to-prd
    step_type: local_execution
    gate: review_prd
    input_artifact: domain_alignment_report
    output_artifact: prd
  - id: 3
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    input_artifact: prd
    output_artifact: prompt_handoff
approval_gates:
  - review_alignment_report
  - review_prd
  - review_handoff_prompt
stop_conditions:
  - architectural_contradiction
```

## Expected Behavior Checklist
- [x] Selects `docs-architecture` workflow.
- [x] Correctly identifies skill sequence from registry.
- [x] Explicitly defines `guided_execution` mode.
- [x] Lists mandatory approval gates.
- [x] Refuses to start execution until "Go" signal.
