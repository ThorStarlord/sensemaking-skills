# Example: Workflow Orchestration Plan (Docs Architecture)

## 1. Brief consumed
Diagnosis: Vocabulary drift between `README.md` and `skills/`. 
Weakest Boundary: System documentation hierarchy.

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

## 7. Stop conditions
- If `grill-with-docs` identifies a major architectural contradiction that requires a human decision.

## 8. Execution mode
`guided_execution`

## 9. Prompt chain
1. `/grill-with-docs: Align the system vocab in README with the new skill structure.`
2. `/to-prd: Update the V1 PRD based on the alignment report.`
3. `/handoff: Summarize the doc hardening.`

## 10. Run log template
Initialized at `docs/runs/2026-05-13-docs-alignment.md`.

## Expected Behavior Checklist
- [ ] Selects `docs-architecture` workflow.
- [ ] Explicitly defines `guided_execution` mode.
- [ ] Lists approval gates for doc review.
- [ ] Does not execute until "Go" signal.
