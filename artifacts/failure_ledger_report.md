# Failure Ledger & Repeatable Failure Boundary Report

Generated: 2026-05-16 16:18:25

## Summary
- Run logs scanned: 11
- Runs with failures: 1
- Total failure entries: 1
- Repeatable failure boundaries: 0

## Repeatable Failure Boundaries

No repeatable failure boundaries detected. All failure occurrences are single-occurrence data issues and do not warrant systemic hardening.

## Error Code Registry

| Code | Occurrences | Independent Runs | Repeatable? |
| :--- | :---: | :---: | :--- |
| `NO_LOGIC_TRACE` | 1 | 1 | No |
| `UNKNOWN_WEAKNESS_TYPE` | 1 | 1 | No |

## Failure Detail

- **Session**: yolo/fast-local-diagnostic/2026-05-16
  - **Type**: tdd_cycle
  **Mode**: yolo_execution
  - **RED**: Level 3 validator failed with NO_LOGIC_TRACE + UNKNOWN_WEAKNESS_TYPE
  - **GREEN**: Fixed weakness type to "Contract Mismatch" + added logic trace sentence
  - **REFACTOR**: Both validators pass after fix. Run log written.
  - **Codes**: NO_LOGIC_TRACE, UNKNOWN_WEAKNESS_TYPE
