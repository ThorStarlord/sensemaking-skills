# Diagnostic Report: Architectural Review Planning

- **Generated**: 2026-07-25 10:19:26
- **Workflow**: architectural-review-planning-workflow
- **Mode**: guided_execution
- **Session**: orchestration-20260725-101913-76791b95

## What Will Happen

This report documents the execution plan for this workflow.

## Steps in Sequence

### Step 1: repo-sensemaker
- **Output**: repository_sensemaking_brief
- **Gate**: review_diagnosis

### Step 2: architectural-review
- **Output**: architectural_review_recommendation
- **Gate**: review_recommendation

## Validators Expected to Run

- **repository_sensemaking_brief**: 2 validators
- **architectural_review_recommendation**: 2 validators

**Total validators to run**: 4

## Success Criteria

- All 2 steps complete successfully
- All artifacts produced
- All validators pass
