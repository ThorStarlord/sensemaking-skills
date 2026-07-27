# Validation Run Log

This log records all validation attempts for artifacts in this repository.
Each entry preserves the complete validation result for auditing.

## Validation Attempt — 2026-07-27T19:52:15.956349Z

- Artifact: `repository_sensemaking_brief`
- Path: `C:\scratch\stage1-auteur-attempt-20260727-164125\framework\artifacts\05-orchestration-run\repository_sensemaking_brief.md`
- Validator: `validate-brief.py`
- Result: **INVALID**
- Error count: 5

| error_id | type | field | message | suggested_fix |
|---|---|---|---|---|
| `` | logic_error | weakness_type | HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT: weakness_type is 'Ghost Features', a high-risk claim catego |  |
| `` | logic_error | None | EVIDENCE_QUOTE_NOT_FOUND: Excerpt[0] quote not found in docs/adr/ADR-013-Universe-to-Series-Propagat |  |
| `` | logic_error | None | EVIDENCE_QUOTE_NOT_FOUND: Excerpt[1] quote not found in src/auteur/universe/models.py (searched line |  |
| `` | logic_error | None | EVIDENCE_QUOTE_NOT_FOUND: Excerpt[2] quote not found in src/auteur/universe/compiler.py (searched li |  |
| `` | logic_error | None | EVIDENCE_QUOTE_NOT_FOUND: Excerpt[4] quote not found in src/auteur/series/universe_integration.py (s |  |

References:
- `skills/workflow-planner/references/artifact-contracts.yaml`

---

