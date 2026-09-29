# monitoring/

`config.yaml` is an illustrative monitoring configuration from the
deployment-hardening phase: metric names (`execution_time_seconds`,
`workflows_completed`, `validation_failures`, `gate_decisions_by_result`),
example alert rules, and JSON logging settings.

**Status:** reference configuration. No code in `src/` reads it, so it does
not enforce or emit anything by itself. For current operations see
`docs/operations-runbook.md`; for run history see `docs/run-ledger-guide.md`.
