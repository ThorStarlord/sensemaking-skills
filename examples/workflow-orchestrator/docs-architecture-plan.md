# Example: Workflow Orchestration Plan (Docs Architecture)

## 1. Brief consumed
Diagnosis: Vocabulary drift between `README.md` and `skills/`.
Weakest Boundary: System documentation hierarchy.
Recommended Workflow: `docs-architecture`

## 2. Chosen workflow
`docs-architecture`

## 3. Why this workflow
It specifically addresses documentation misalignment by aligning docs with domain language and producing copy-paste prompts for implementation.

## 4. Skills in sequence
1. `grill-with-docs`
2. `handoff`

## 5. Inputs and outputs
- `grill-with-docs`: Receives Brief + Context. Produces Alignment Report.
- `handoff`: Receives Alignment Report. Produces copy-paste Handoff Prompt.

## 6. Approval gates
- **Gate 1**: Review Alignment Report (after `grill-with-docs`).
- **Gate 2**: Review Handoff Prompt (after `handoff`).

## 7. Stop conditions
- If `grill-with-docs` identifies a major architectural contradiction that requires a human decision.

## 8. Execution mode
`guided_execution` (Defaulting from brief recommendation).

## 9. Prompt chain
1. `/grill-with-docs: Align the system vocab in README with the new skill structure.`
2. `/handoff: Summarize the alignment findings and generate implementation prompts.`

## 10. Run log template
Initialized at `docs/runs/2026-05-13-docs-alignment.md`.

## 11. Machine-readable plan

```yaml
artifact_id: workflow_orchestration_plan
chosen_workflow_id: docs-architecture
execution_mode: guided_execution
status: PENDING
subset_run: false

initial_inputs:
  - id: repository_state
    type: repository_snapshot
    required: true

steps:
  - id: 1
    skill: grill-with-docs
    step_type: local_execution
    gate: review_alignment_report
    input_source: repository_state
    output_artifact: domain_alignment_report
    status: PENDING
  - id: 2
    skill: handoff
    step_type: local_execution
    gate: review_handoff_prompt
    input_artifact: domain_alignment_report
    output_artifact: prompt_handoff
    status: PENDING

approval_gates:
  - review_alignment_report
  - review_handoff_prompt

gate_behavior:
  review_alignment_report: human_approval
  review_handoff_prompt: human_approval

stop_conditions:
  - architectural_contradiction
```

## Expected Behavior Checklist
- [x] Selects `docs-architecture` workflow (redesigned 2-step version).
- [x] Correctly identifies skill sequence from registry: grill-with-docs → handoff.
- [x] Explicitly defines `guided_execution` mode.
- [x] Lists 2 mandatory approval gates (review_alignment_report, review_handoff_prompt).
- [x] Refuses to start execution until "Go" signal.
