# Workflow Run Log: [Workflow Name]

- **Date**: [YYYY-MM-DD]
- **Session ID**: [ID]
- **Orchestrator Mode**: [Mode]

## Sequence Log

### Step [ID]
- **step_id**: [ID]
- **skill**: [Skill Name]
- **runtime**: [local | local_command | external]
- **invocation**: [exact command or local function]
- **input_artifact**: [Artifact ID or N/A]
- **input_source**: [Source ID or N/A]
- **output_artifact**: [Artifact ID]
- **artifact_path**: [Relative path, e.g., artifacts/name.md]
- **validation_command**: [Exact command used to validate]
- **validation_result**: [PASSED | FAILED]
- **gate**: [Gate Name]
- **status**: [COMPLETED | PAUSED | FAILED]

## Decisions & Overrides
- [List any manual interventions or logic changes made during the run]

## Final State
- [Summary of what was achieved]
