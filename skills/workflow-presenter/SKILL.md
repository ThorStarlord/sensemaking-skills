---
name: workflow-presenter
description: Generates beautiful markdown execution summaries from workflow JSON output. Auto-invoked by orchestration-runner to present results to end-users.
---

# workflow-presenter

Presentation layer for orchestration system. Reads machine-readable workflow execution JSON and generates a beautiful, human-friendly markdown summary.

## Purpose

Transform raw workflow execution data into a readable, navigable report that:
- Shows what was executed and what the status is
- Lists artifacts created with clickable links
- Documents validation results
- Provides clear next steps

## Input

**workflow_summary.json** — Structured JSON produced by orchestration-runner.py after workflow completion.

```json
{
  "workflow_id": "fast-path-workflow",
  "workflow_name": "Fast-Path Diagnostic",
  "session_id": "orchestration-20260520-abc123",
  "mode": "guided_execution",
  "status": "completed",
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
      "validators": []
    }
  ]
}
```

## Output

**EXECUTION_SUMMARY.md** — Beautiful markdown report with:
- Workflow identification (name, mode, session ID, branch)
- Execution summary table (steps completed, failures, status)
- Step-by-step details with artifact links
- Artifact manifest
- Status conclusion with next steps

## Usage

### Direct Invocation
```bash
python skills/workflow-presenter/workflow-presenter.py artifacts/workflow_summary.json --output-dir artifacts
```

### Auto-Invocation
Automatically called by orchestration-runner after workflow completion:
```python
self.invoke_presentation_skill(summary_json_path)
```

## Features

- ✓ Emoji-based status indicators (✓ ✗ ⚠)
- ✓ Clickable artifact links
- ✓ Validation result details
- ✓ Step duration tracking
- ✓ Error summary on failure
- ✓ Guided next steps based on status

## Design Principles

1. **Separation of Concerns**: Orchestrator generates data, presenter generates presentation
2. **Idempotent**: Same JSON input always produces same markdown output
3. **Automation-Friendly**: No user interaction required; safe to auto-invoke
4. **Human-Centered**: Format prioritizes readability and actionability
5. **Audit Trail**: Links back to structured JSON and detailed logs for drilling down

## Related

- **Input Source**: scripts/workflow-runtime.py (generates workflow_summary.json)
- **Use Case**: ADR 0005 — Skill Invocation Via Workflows (auto-invocation pattern)
