# Validation Cache

This directory stores baseline validation artifacts for comparison across validation runs.

## Structure

```
.validation-cache/
├─ latest/                    (Symlink to most recent successful run)
│  ├─ sensemaking_brief.md
│  ├─ error_analysis.md
│  └─ changes_identified.md
├─ run-2026-05-15-143022/     (Individual run directories)
├─ run-2026-05-18-091433/
└─ manifest.json              (Metadata: dates, statuses, triggers)
```

## How It Works

1. After each successful validation run, artifacts are copied to `.validation-cache/run-{timestamp}/`
2. Symlink `latest` always points to the most recent successful run
3. `repo_sensemaker` uses `baseline_dir: ".validation-cache/latest"` for comparison
4. Manifest tracks run history for troubleshooting and metrics

## Run Structure

Each `run-{timestamp}/` directory contains validation artifacts:

- **sensemaking_brief.md** — Repository analysis from repo-sensemaker
- **error_analysis.md** — Errors found during validation
- **changes_identified.md** — What changed since last run
- **comparison_report.md** — Side-by-side comparison with previous run
- **problem_frame.md** — Re-framed problem statement
- **unknowns_map.md** — Map of unknowns in the system

## Retention Policy

- **Keep:** 90 days of validation runs
- **Archive:** Runs older than 90 days are archived (not deleted)
- **Cleanup Frequency:** Weekly

## Manifest

The `manifest.json` file tracks:

- Version of cache schema
- Cache location path
- Latest run pointer
- All runs metadata (timestamps, statuses)
- Retention policy settings

## Usage

Validation workflows read from `.validation-cache/latest` to establish baseline for comparison. This enables identifying:

- New errors introduced since the last iteration
- Fixed issues from previous runs
- Regression detection

## Notes

- This directory is generated and updated by the validation workflow
- Do not manually edit run directories
- Manifest.json may be updated programmatically but structure should remain stable

## See Also

For more information on using the validation workflow, see:
- The validation workflow documentation (describes how to use validation)
- The workflow configuration guide (defines how validation runs)
- Orchestration patterns and architecture decisions
