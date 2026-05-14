# Workflow Run Log: fast-local-diagnostic (YOLO DRY-RUN FAILURE)

- **Date**: 2026-05-14
- **Session ID**: yolo-dry-run-failure-001
- **Orchestrator Mode**: yolo_execution

## Preflight
- **validator_stack**:
    - level: Structural (Level 1)
      command: `python scripts/validate-repo.py`
      result: PASSED
- **branch**:
    - name: `yolo/fast-local-diagnostic/20260514`
    - main_or_master: false
- **dry_run**: true
- **repository_mutation_allowed**: false

## Sequence Log

### Step 1
- **step_id**: 1
- **skill**: repo-sensemaker
- **runtime**: local
- **invocation**: LLM Generation (Simulated output)
- **input_artifact**: N/A
- **input_source**: repository_state
- **output_artifact**: repository_sensemaking_brief
- **artifact_path**: examples/negative/yolo-hallucination-failure.md
- **validator_stack**:
    - level: Generic (Level 2)
      command: `python scripts/validate-artifact.py repository_sensemaking_brief examples/negative/yolo-hallucination-failure.md`
      result: PASSED
    - level: Specialized (Level 3)
      command: `python scripts/validate-brief.py examples/negative/yolo-hallucination-failure.md`
      result: FAILED
- **gate**: review_sensemaking_brief
- **gate_behavior**: bypassed_by_yolo
- **failure reason**: Brief verification failed: Excerpt[1] references non-existent file: scripts/hallucinated-file.py (Hallucination detected!)
- **status**: FAILED

## Decisions & Overrides
- **Dry-run simulation**: Treated `examples/negative/yolo-hallucination-failure.md` as the actual output of Step 1 to test fail-fast logic.

## Final State
- **Status**: FAILED
- **Result**: YOLO execution halted immediately after Step 1 validator failure. Step 2 (`prompt_handoff`) was not reached.
- **Rollback Required**: false
- **Rollback Recommendation**: No mutation occurred; no reset required.
