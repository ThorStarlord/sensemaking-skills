# Validation Cache

This directory stores baseline artifacts from validation runs for comparison purposes.

## Structure

- `latest/` — Symlink to the most recent successful validation run
- `run-{timestamp}/` — Individual run artifacts
- `manifest.json` — Metadata about all runs

## How It Works

After each successful validation:
1. Artifacts are copied to `run-{timestamp}/`
2. Symlink `latest` points to the newest run
3. Scripts use `latest` baseline for comparing current analysis

## Cleanup

Runs older than 90 days are archived (not deleted) for audit trails.

## See Also

- `docs/validation-workflow.md` — How to use validation
- `docs/workflows/validation-finance-system.yaml` — Workflow configuration
