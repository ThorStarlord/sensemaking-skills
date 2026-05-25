# Diagnostic Report: Fast Local Diagnostic

- **Generated**: 2026-05-23 18:15:06
- **Workflow**: fast-local-diagnostic
- **Mode**: yolo_execution
- **Session**: orchestration-20260523-181501-af0261dc

## What Will Happen

This report documents the execution plan for this workflow.

## Steps in Sequence

### Step 1: repo-sensemaker
- **Output**: repository_sensemaking_brief
- **Gate**: review_sensemaking_brief

### Step 2: handoff
- **Output**: session_summary
- **Gate**: review_handoff_prompt

## Validators Expected to Run

- **repository_sensemaking_brief**: 2 validators
- **session_summary**: 1 validators

**Total validators to run**: 3

## Success Criteria

- All 2 steps complete successfully
- All artifacts produced
- All validators pass
