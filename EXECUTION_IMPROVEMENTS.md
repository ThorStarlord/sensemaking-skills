# Workflow-Runtime Execution Improvements

## Summary

The workflow-runtime.py script was executed with default settings (full-local-sensemaking → implementation-workflow auto-chain, yolo_execution mode). The execution revealed design issues and opportunities for improvement.

**Outcome**: Execution halted on Step 2 (unknowns-mapper validator failure), but the orchestration system and error messaging were significantly improved.

---

## What Worked ✅

1. **Pre-flight checks**: Git state validation, repository structure validation
2. **Plan generation**: Workflow orchestration plan generated correctly
3. **Step execution**: Problem-framer step passed validation
4. **Error handling**: Validators caught malformed artifacts with zero-tolerance (safety feature)
5. **Rollback recommendation**: System correctly recommended rollback on failure
6. **Run log generation**: All execution details recorded for audit trail

---

## Issues Found ❌

### 1. Missing Artifact Sections in unknowns-mapper Output
**Status**: Blocker for workflow completion

The unknowns_map artifact is missing required sections per the artifact contract:
- Missing: `knowns`, `risks`, `research_paths`, `stopping_rule`
- Missing machine fields: `clarity_assessment`, `unknowns_count`, `assumptions_count`, `research_needed`

**Root Cause**: The unknowns-mapper skill is not being invoked/executed. Skills need an execution mechanism to actually run and produce artifacts.

**Impact**: Cannot progress beyond Step 2

---

## Improvements Made ✅

### 1. Error Messages (Priority 1 - DONE)
Enhanced validate-artifact.py to provide actionable error messages:

**Before**:
```
ERROR MISSING_REQUIRED_SECTION: Missing required section: knowns
ERROR MISSING_MACHINE_FIELDS: Could not find a single YAML block containing all required machine fields: ['clarity_assessment', ...]
```

**After**:
```
ERROR MISSING_REQUIRED_SECTION: Missing 4 required section(s): knowns, risks, research_paths, stopping_rule
Expected template: skills/unknowns-mapper/references/unknowns_map-template.md
Artifact contract: skills/workflow-planner/references/artifact-contracts.yaml (id: unknowns_map)

ERROR MISSING_MACHINE_FIELDS: Missing required machine-readable fields: clarity_assessment, unknowns_count, assumptions_count, research_needed
Add YAML block at end of artifact:
```yaml
clarity_assessment: <value>
unknowns_count: <value>
assumptions_count: <value>
research_needed: <value>
```
See template: skills/unknowns-mapper/references/unknowns_map-template.md
```

**Benefits**:
- Users know exactly which sections are missing
- Template locations provided for reference
- YAML structure shown as an example
- Links to artifact contracts

### 2. Error Output Formatting (Priority 1 - DONE)
Enhanced workflow-runtime.py to print full validator output instead of truncating:
- Full error details now visible (not just first 150 chars)
- Better diagnostics for troubleshooting

### 3. Fixed Workflow Registry (Priority 1 - DONE)
Added missing `branch_policy` to product-to-issues workflow to support yolo_execution mode

---

## Next Steps 🚀

### Priority 2: Create Fixture Artifacts (Easy)
Create valid artifacts for testing orchestration without skill execution:
- `examples/unknowns-mapper/unknowns_map-valid.md` (complete, valid template)
- `examples/problem-framer/problem_frame-valid.md`
- `examples/repo-sensemaker/repository_sensemaking_brief-valid.md`

Use with flag: `python scripts/workflow-runtime.py --use-fixtures`

### Priority 3: Skill Execution Infrastructure (Hard)
**Current gap**: Skills exist as SKILL.md prompts but aren't executable

Options:
1. **Mock execution**: Use fixture artifacts instead of actually running skills
2. **Claude API integration**: Connect to Claude API via skill_executor.py
3. **Manual mode**: Allow users to manually run skills and save artifacts

### Priority 4: Testing & Validation (Medium)
- Add end-to-end integration tests for all 5 execution modes
- Create parametrized tests for each mode ceiling (plan_only, prompt_chain, etc.)
- Coverage report for workflow-runtime.py

---

## Files Modified

- `scripts/validate-artifact.py` — Enhanced error messages with template references
- `scripts/workflow-runtime.py` — Full error output, improved error display
- `CONTEXT.md` — Documented default workflows and yolo_execution mode
- `README.md` — Added default workflow chain documentation
- `skills/workflow-planner/references/workflow-registry.yaml` — Added branch_policy to product-to-issues

---

## Test Results

**Workflow**: `full-local-sensemaking` (DEFAULT)  
**Mode**: `yolo_execution` (DEFAULT)  
**Session**: orchestration-20260520-205341-d4b06f14  

| Phase | Status |
|-------|--------|
| Pre-flight checks | ✅ PASSED |
| Plan generation | ✅ PASSED |
| Step 1: problem-framer | ✅ PASSED |
| Step 2: unknowns-mapper | ❌ FAILED (missing artifact sections) |
| Error handling | ✅ PASSED |
| Rollback recommendation | ✅ PASSED |
| Run log generation | ✅ PASSED |

**Conclusion**: Orchestration system is **production-ready for planning**. Skill execution infrastructure needed for full workflow completion.
