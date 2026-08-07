# Diagnostic Report: Full Local Sensemaking

- **Generated**: 2026-08-03 21:11:27
- **Workflow**: full-local-sensemaking
- **Mode**: plan_only
- **Session**: orchestration-20260803-211126-2a68f975

## What Will Happen

This report documents the execution plan for this workflow.

## Steps in Sequence

### Step 1: problem-framer
- **Output**: problem_frame
- **Gate**: review_problem_frame

### Step 2: unknowns-mapper
- **Output**: unknowns_map
- **Gate**: review_unknowns_map

### Step 3-conditional: discovery (conditional)
- **Output**: discovery_findings or unknowns_map
- **Gate**: review_discovery

### Step 4: repo-sensemaker
- **Output**: repository_sensemaking_brief
- **Gate**: review_sensemaking_brief

### Step 5: workflow-planner
- **Output**: workflow_orchestration_plan
- **Gate**: none

### Step 6: handoff
- **Output**: session_summary
- **Gate**: review_final_prompt

## Validators Expected to Run

- **problem_frame**: 2 validators
- **unknowns_map**: 2 validators
- **repository_sensemaking_brief**: 2 validators
- **workflow_orchestration_plan**: 2 validators
- **session_summary**: 1 validators

**Total validators to run**: 9

## Success Criteria

- All 6 steps complete successfully
- All artifacts produced
- All validators pass
