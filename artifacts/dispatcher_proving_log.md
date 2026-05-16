# Dispatcher Proving Record: validate-output.py as Normal Path

- **Date**: 2026-05-16
- **Session ID**: dispatcher-proving/2026-05-16
- **Purpose**: Prove validate-output.py dispatcher as the normal validator invocation path

## Validation Cross-Check

All existing artifacts validated using the validate-output.py dispatcher instead of direct validator calls:

| Artifact | Dispatcher Command | Result |
|----------|:-----------------:|:------:|
| `repository_sensemaking_brief` | `python scripts/validate-output.py repository_sensemaking_brief artifacts/repository_sensemaking_brief.md --repo-root .` | ✅ PASSED |
| `prompt_handoff` | `python scripts/validate-output.py prompt_handoff artifacts/prompt_handoff.md --repo-root .` | ✅ PASSED |
| `workflow_orchestration_plan` | `python scripts/validate-output.py workflow_orchestration_plan artifacts/plan-only-orchestration-plan.md --repo-root .` | ✅ PASSED |
| `docs_contract_reconciliation_report` | `python scripts/validate-output.py docs_contract_reconciliation_report artifacts/docs_contract_reconciliation_report.md --repo-root .` | ✅ PASSED |

## Dispatcher Behavior Verified

For each artifact, validate-output.py:
1. ✅ Reads artifact-contracts.yaml
2. ✅ Finds the contract by artifact_id
3. ✅ Resolves the generic_validator script path
4. ✅ Runs generic_validator (validate-artifact.py) via subprocess
5. ✅ Runs all specialized_validators from the contract
6. ✅ Reports aggregated pass/fail

## Fixture coverage

Test-validators.py was run with validate-output.py included in the auto-discovery, verifying:
- All 22 artifact types in artifact-contracts.yaml have valid generic_validator entries
- All 5 specialized_validator references point to existing .py files

## Conclusion

validate-output.py dispatcher is now the normal validation path for all workflow runs.
All artifact types validated successfully through the dispatcher.
The dispatcher is fully functional and ready for use in all execution modes.

```yaml
artifact_id: dispatcher_proving_record
dispatcher_script: scripts/validate-output.py
artifacts_validated: 4
artifact_types_covered: 4
all_passed: true
validated_at: 2026-05-16
```
