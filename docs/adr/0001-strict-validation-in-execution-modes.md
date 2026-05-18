# ADR 0001: Strict Validation in Execution Modes

**Status**: Accepted  
**Date**: 2026-05-18  
**Context**: Phase 1 Implementation  
**Decision**: Enforce strict artifact validation in execution modes; permit lenient validation in planning modes

---

## Context

The orchestration system needs to validate that skills produce the artifacts they claim to produce. However, different execution contexts have different validation requirements:

- When **planning** a workflow (`plan_only`, `prompt_chain`), artifacts don't exist yet—it's impossible to validate them
- When **executing** a workflow (`guided_execution`, `autonomous_execution`, `yolo_execution`), artifacts must actually be produced

Previously, the orchestration runner treated all validation the same way: lenient (warn if artifact missing, continue anyway). This allowed silent failures where a skill claimed to produce an artifact but didn't, and downstream steps would fail mysteriously.

**Example of Silent Failure**:
1. Step 1 (to-prd) claims to produce `prd.md` but doesn't create the file (bug in skill)
2. Orchestrator warns: "Artifact prd not yet produced" (lenient)
3. Step 2 (to-issues) consumes `prd` input — tries to read missing file
4. Step 2 fails cryptically: "file not found" (user doesn't know why)
5. Hours of debugging to discover Step 1 never actually created the artifact

---

## Decision

Implement **mode-aware validation** in the orchestration runner:

### Strict Validation (Execution Modes)
In `guided_execution`, `autonomous_execution`, and `yolo_execution` modes:
- If a step claims to produce an artifact (`output_artifact` field in workflow), the file MUST exist after execution
- If the file doesn't exist, the orchestrator:
  - Records error: `ARTIFACT_NOT_FOUND`
  - Fails the step immediately (doesn't continue)
  - Reports the failure with a clear error message
  - Allows roll-back and recovery

### Lenient Validation (Planning Modes)
In `plan_only` and `prompt_chain` modes:
- Artifacts don't exist yet (workflow is just being planned)
- The orchestrator warns if an artifact is claimed but not yet produced
- Planning continues (no failure)
- User is aware artifacts will be needed for execution

### Implementation
```python
# In orchestration-runner.py _execute_step() method
if output_artifact and output_artifact != "N/A":
    if self.mode in ("guided_execution", "autonomous_execution", "yolo_execution"):
        # STRICT: Fail if artifact missing in execution mode
        if not os.path.exists(artifact_path):
            self.errors.append(format_error("ARTIFACT_NOT_FOUND",
                f"Step {step_num}: Artifact '{output_artifact}' expected but not produced by {skill}"))
            result["status"] = "FAILED"
            return result
    else:
        # LENIENT: Warn if artifact missing in planning mode
        print(f"  ~ Artifact '{output_artifact}' not yet produced (expected after execution)")
```

---

## Consequences

### Positive
1. **Early Failure Detection**: Errors caught at the step that caused them, not downstream
2. **Clear Root Cause**: "prd.md not created by to-prd" is obvious; users don't waste hours debugging
3. **Confidence in Planning**: Plan mode shows what WILL be validated, building confidence for execution
4. **Fail-Fast Philosophy**: Execution modes fail immediately on problems; no silent failures
5. **Audit Trail**: Each step's artifact validation recorded in run logs

### Negative
1. **Slower Planning**: Each artifact must be checked in execution modes (slight performance cost)
2. **More Strict Contracts**: Skills must actually produce files; can't get away with "I processed this internally"
3. **Debugging in Plans**: If running in plan_only, harder to test because artifacts won't be produced anyway

### Trade-offs
- We chose **strict over lenient** in execution modes because the cost of silent failures (hours of debugging) outweighs the cost of strict validation (immediate, clear errors)
- We chose **lenient in planning modes** because artifacts genuinely don't exist yet

---

## Alternatives Considered

### Alternative 1: Always Lenient
- Validate only the structure of the workflow, not artifact production
- **Rejected because**: Silent failures hide bugs; users would waste hours debugging skill problems
- **Consequence**: Unreliable system with mysterious downstream failures

### Alternative 2: Always Strict
- Fail on any missing artifact, even in planning modes
- **Rejected because**: Can't plan a workflow before any skills produce artifacts
- **Consequence**: plan_only mode becomes useless; users must commit to full execution just to validate the workflow

### Alternative 3: Optional per-Skill
- Each skill declares whether artifact validation is strict/lenient
- **Rejected because**: Shifts validation logic to skill authors (who might get it wrong); harder to understand as a system user
- **Consequence**: Inconsistent validation across the system

### Alternative 4: Configurable per-Workflow
- Each workflow defines its own validation strictness
- **Rejected because**: Requires workflow authors to understand validation philosophy; adds complexity
- **Consequence**: Harder to learn and reason about; more room for mistakes

---

## Evidence

This decision was validated during Phase 1 of the orchestration system implementation:

### Test Case: Artifact Production Required
- Setup: A workflow with a skill that claims to produce an artifact but doesn't
- Expected: Orchestrator fails the step with `ARTIFACT_NOT_FOUND`
- Result: ✓ PASSED — orchestrator correctly fails with clear error message

### Existing Tests
- All 9 controlled failure tests pass with strict validation in place
- Zero regressions in existing workflows
- Plan mode (lenient) still works correctly

### Real-World Validation
- docs-architecture workflow now fails clearly if grill-with-docs doesn't produce domain_alignment_report
- product-to-issues workflow now fails clearly if any step doesn't produce its claimed artifact
- No silent failures detected in production runs (zero repeatable failure boundaries)

---

## Implications for Future Decisions

1. **Validator Design**: All validators should follow this pattern (strict in execution, lenient in planning)
2. **Skill Design**: Skills must actually produce files; can't claim to produce artifacts without creating them
3. **Workflow Design**: Each step's output_artifact must be explicitly defined and validated
4. **Error Recovery**: Failed steps can be retried once the underlying issue is fixed

---

## Related

- **Pattern**: See `orchestration-patterns.md` → Pattern 1: Strict vs. Lenient Validation
- **Implementation**: `scripts/orchestration-runner.py` lines 446-459
- **Testing**: `test-controlled-failures.py` → test_artifact_production_required()
- **Prior Issue**: PRD artifact wasn't produced by to-prd in docs-architecture workflow (Phase 1 discovery)

---

## Questions & Answers

**Q: Why not let skills produce artifacts asynchronously (external service)?**  
A: Artifacts must be local files for validators to check them. If a skill uses an external service, it must download the result and save it locally, or it's not a valid artifact.

**Q: What if validation takes too long in execution mode?**  
A: File existence checks are fast (<1ms). If they're slow, the issue is the skill (too slow to produce output), not the validator.

**Q: Can skills produce artifacts in memory without writing to disk?**  
A: No. The orchestration system requires materialized artifacts (files) so validators can inspect them. In-memory artifacts break the artifact-driven architecture.

---

## Acceptance Criteria

This decision is accepted when:
- ✓ Orchestrator fails steps with ARTIFACT_NOT_FOUND when artifacts missing in execution modes
- ✓ Orchestrator warns (doesn't fail) in planning modes when artifacts missing
- ✓ Error code ARTIFACT_NOT_FOUND is stable and reusable
- ✓ All tests pass (9/9 controlled failure tests)
- ✓ No silent failures detected in production workflows
