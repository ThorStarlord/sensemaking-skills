> **CURRENT (2026-08, ADR 0013)**: where this guide describes the programmatic
> second-model runner, it is superseded: execution is agent-native (the active
> coding agent reads the Skill and performs it; validators check the artifact),
> and the CLI/runtime is deterministic support (planning, paths, gates,
> sessions/ledger, validation) - not a model launcher. The claude-code/api
> executors were retired.

# Workflow Output System: Two-Layer Architecture

**Date**: 2026-05-20  
**Status**: Production Ready  
**Implemented**: Phase 5b

---

## Overview

The workflow output system uses a **two-layer architecture** to provide both machine-readable audit trails and beautiful human-readable summaries.

```
Layer 1 (Machine): workflow-runtime.py
  ├─ Executes workflow steps
  ├─ Records execution data
  └─ Outputs: workflow_summary.json
                (structured execution data)
       ↓
Layer 2 (Human): workflow-presenter skill
  ├─ Reads workflow_summary.json
  ├─ Reads artifact files
  └─ Outputs: EXECUTION_SUMMARY.md
              (beautiful formatted report)
       ↓
End-User sees beautiful summary with artifact links
```

---

## Layer 1: Machine-Readable Output

**File**: `scripts/workflow-runtime.py`  
**Method**: `generate_workflow_summary_json()`  
**Output**: `artifacts/workflow_summary.json`

### What It Contains

```json
{
  "workflow_id": "fast-path-workflow",
  "workflow_name": "Fast-Path Diagnostic",
  "session_id": "orchestration-20260520-abc123",
  "mode": "guided_execution",
  "status": "completed",
  "final_note": "All 3 steps completed successfully...",
  "branch": "main",
  "executed_at": "2026-05-20T14:30:45.123456",
  "steps_completed": 3,
  "steps_total": 3,
  "steps_failed": 0,
  "steps": [
    {
      "step_id": "1",
      "skill": "repo-sensemaker",
      "status": "EXECUTED",
      "output_artifact": "diagnostic_report",
      "artifact_path": "artifacts/01-orchestration-run/diagnostic_report.md",
      "duration_seconds": 75.5,
      "validators": [
        {
          "level": "level_2: validate-artifact.py",
          "result": "PASSED"
        }
      ]
    }
  ],
  "errors": []
}
```

### Purpose

- **Audit Trail**: Complete record of what was executed
- **Machine Parsing**: Easy to parse for downstream tools
- **Debugging**: Detailed information for troubleshooting
- **Metrics**: Duration, step counts, validator results
- **Versioning**: Preserves execution data for future reference

---

## Layer 2: Human-Readable Output

**File**: `skills/workflow-presenter/workflow-presenter.py`  
**Input**: `workflow_summary.json`  
**Output**: `EXECUTION_SUMMARY.md`

### What It Generates

Beautiful markdown report with:
- Workflow metadata (name, mode, session, branch)
- Execution summary table (steps completed, failed, status)
- Step-by-step details with artifact links
- Artifacts manifest
- Status conclusion with next steps
- Emoji-based status indicators (✓ ✗ ⚠)

### Example Output

```markdown
# Workflow Execution Summary

**Workflow**: Fast-Path Diagnostic (`fast-path-workflow`)  
**Mode**: guided_execution  
**Status**: ✓ **COMPLETED**  
**Session**: `orchestration-20260520-abc123`  
**Branch**: `main`  

## Execution Summary

| Metric | Value |
|--------|-------|
| Steps Executed | 3/3 ✓ |
| Steps Failed | 0 |
| Final Status | COMPLETED |

## Steps Executed

### Step 1: repo-sensemaker
- **Status**: ✓ `EXECUTED`
- **Output**: [diagnostic_report.md](artifacts/diagnostic_report.md)
- **Duration**: 75.5s

## Artifacts Created
- [diagnostic_report.md](artifacts/diagnostic_report.md)
- [workflow_orchestration_plan.md](artifacts/workflow_orchestration_plan.md)
- [implementation_guide.md](artifacts/implementation_guide.md)

## Status
✓ **Success**: All workflow steps executed and validated successfully.
```

---

## Auto-Invocation Flow

The presentation skill is **automatically invoked** after every workflow completes.

### Execution Timeline

```
1. workflow-runtime.py finishes execution
         ↓
2. Phase 4: WRITE RUN LOG
   - Generates run_log_*.md
         ↓
3. Phase 4b: IMPLEMENTATION REPORT
   - Generates implementation_*.md
         ↓
4. Phase 4c: WORKFLOW SUMMARY (MACHINE-READABLE)
   - Calls generate_workflow_summary_json()
   - Outputs workflow_summary.json
         ↓
5. Phase 4d: WORKFLOW PRESENTATION (HUMAN-READABLE)
   - Calls invoke_presentation_skill()
   - Auto-invokes skills/workflow-presenter/workflow-presenter.py
   - Outputs EXECUTION_SUMMARY.md
         ↓
6. User sees in console:
   [OK] Execution summary generated: artifacts/EXECUTION_SUMMARY.md
```

### Modes Supported

| Mode | Behavior |
|------|----------|
| `plan_only` | Stops after Phase 2 (no execution, no summary) |
| `prompt_chain` | Generates prompts, produces summary with PROMPT_GENERATED status |
| `guided_execution` | Executes with user gates, produces summary with EXECUTED/VALIDATED status |
| `autonomous_execution` | Auto-executes all steps, produces summary with EXECUTED/VALIDATED status |
| `yolo_execution` | Auto-executes, bypasses gates, produces summary with EXECUTED/VALIDATED status |

---

## Design Principles

1. **Separation of Concerns**
   - Orchestrator generates data
   - Presenter formats for humans
   - Each tool has one responsibility

2. **Idempotent**
   - Same JSON input → same markdown output
   - Safe to re-run without side effects

3. **Automation-Friendly**
   - No user interaction required
   - Safe to auto-invoke
   - No error handling needed in user workflows

4. **Human-Centered**
   - Format prioritizes readability
   - Clickable artifact links
   - Clear next steps based on status

5. **Audit Trail**
   - JSON preserved for debugging
   - Both files stored in artifacts/ folder
   - Complete execution record

---

## Files Created/Modified

### New Files
- `skills/workflow-presenter/workflow-presenter.py` — Presentation skill
- `skills/workflow-presenter/SKILL.md` — Skill documentation

### Modified Files
- `scripts/workflow-runtime.py`
  - Added `generate_workflow_summary_json()` method
  - Added `invoke_presentation_skill()` method
  - Updated `run()` to call new methods in Phase 4c & 4d

### Outputs (Generated per Run)
- `artifacts/workflow_summary.json` — Machine-readable summary
- `artifacts/EXECUTION_SUMMARY.md` — Human-readable summary
- `artifacts/run_log_*.md` — Detailed execution log (existing)
- `artifacts/implementation_*.md` — Implementation report (existing)

---

## Usage

### For End-Users
After running a workflow:
```bash
python scripts/workflow-runtime.py <workflow-id> --mode <mode>
```

Outputs:
- Console shows workflow progress
- `artifacts/EXECUTION_SUMMARY.md` contains beautiful summary
- `artifacts/workflow_summary.json` contains detailed data

### For Developers
To manually invoke the presenter:
```bash
python skills/workflow-presenter/workflow-presenter.py \
  artifacts/workflow_summary.json \
  --output-dir artifacts/
```

---

## Status Indicators

| Symbol | Meaning |
|--------|---------|
| ✓ | Success (COMPLETED, EXECUTED, VALIDATED, PROMPT_GENERATED) |
| ✗ | Failed |
| ⚠ | Incomplete/Partial (PAUSED, PROMPT_CHAIN_GENERATED) |

---

## Future Enhancements

Potential improvements (out of scope for Phase 5b):
- HTML export of summary (for email/web viewing)
- Summary comparison between runs
- Integration with CI/CD pipeline reporting
- Custom summary templates per workflow
- Metrics dashboard generation

---

## Related Documentation

- [ADR 0005: Skill Invocation Via Workflows](docs/adr/0005-skill-invocation-via-workflows.md) — Auto-invocation pattern
- [CONTEXT.md](CONTEXT.md) — Domain language and principles
- [Workflow Runtime](docs/workflow-runtime.md) — Orchestration engine

