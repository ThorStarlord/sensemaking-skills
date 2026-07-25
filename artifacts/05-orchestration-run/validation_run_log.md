# Validation Run Log

This log records all validation attempts for artifacts in this repository.
Each entry preserves the complete validation result for auditing.

## Validation Attempt — 2026-07-25T13:22:49.340075Z

- Artifact: `repository_sensemaking_brief`
- Path: `H:\GithubRepositories\sensemaking-skills\.claude\worktrees\agent-a71d0c50e38cec9fe\artifacts\05-orchestration-run\repository_sensemaking_brief.md`
- Validator: `validate-brief.py`
- Result: **INVALID**
- Error count: 7

| error_id | type | field | message | suggested_fix |
|---|---|---|---|---|
| `repository_sensemaking_brief.recommended_workflow_id.unknown_value` | unknown_value | recommended_workflow_id | HALLUCINATED_WORKFLOW_ID: Recommended workflow ID 'docs-aligner' not found in registry. | Check available workflows in workflow-registry.yaml |
| `` | logic_error | None | INVALID_LINE_FORMAT: Excerpt[0] has invalid lines format: See `escalation_recommended` field definit |  |
| `` | logic_error | None | INVALID_LINE_FORMAT: Excerpt[1] has invalid lines format: Entire skill file (expected a line number  |  |
| `` | logic_error | None | INVALID_LINE_FORMAT: Excerpt[3] has invalid lines format: Routing accuracy section (expected a line  |  |
| `` | logic_error | None | INVALID_LINE_FORMAT: Excerpt[4] has invalid lines format: Runbook table of contents (expected a line |  |
| `` | logic_error | None | INVALID_LINE_FORMAT: Excerpt[5] has invalid lines format: Entire document (expected a line number or |  |
| `` | logic_error | None | INVALID_LINE_FORMAT: Excerpt[6] has invalid lines format: Routing divergence section (expected a lin |  |

References:
- `skills/workflow-planner/references/artifact-contracts.yaml`

---

