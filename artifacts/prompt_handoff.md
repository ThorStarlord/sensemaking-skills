# Prompt Handoff

## 1. Target Skill

`sensemaking-docs-reconciler`

## 2. Context to Preserve

The repository_sensemaking_brief at `artifacts/repository_sensemaking_brief.md` identifies a Contract Mismatch as the weakest boundary. The key finding: `artifact-contracts.yaml` has inconsistent validator invocations across artifact types, and no automated check verifies run-log gate names against `workflow-registry.yaml`. The brief contains two evidence excerpts with file-level citations supporting this diagnosis.

## 3. Task

Reconcile the validator invocations in `artifact-contracts.yaml` so that all artifact types use a consistent pattern, and verify that run-log gate names match the workflow registry. Produce a reconciliation report documenting all drifts found and patches applied.

## 4. Constraints

- Do not modify validator scripts — only update contract registries and documentation
- All artifact paths in the reconciliation report must be repository-relative
- Do not change the `required_sections` or `required_machine_fields` of any artifact contract
- The run-log template's gate field must be checked against `workflow-registry.yaml` step gates

## 5. Inputs

- `artifacts/repository_sensemaking_brief.md`
- `skills/workflow-orchestrator/references/artifact-contracts.yaml`
- `skills/workflow-orchestrator/references/workflow-registry.yaml`
- `skills/workflow-orchestrator/references/run-log-template.md`

## 6. Expected Output

A `docs_contract_reconciliation_report` artifact at `artifacts/docs_contract_reconciliation_report.md` documenting all found drifts, the patches applied, and the validation result of the reconciled state.

## 7. Stop Condition

The reconciliation report has been produced and `python scripts/validate-repo.py` passes on the updated contracts.

## 8. Ready-to-Copy Prompt

```text
You are the sensemaking-docs-reconciler skill. Your task is to reconcile validator invocations in artifact-contracts.yaml.

Read artifacts/repository_sensemaking_brief.md for the diagnosis.
Read skills/workflow-orchestrator/references/artifact-contracts.yaml for current contract state.
Read skills/workflow-orchestrator/references/workflow-registry.yaml for workflow definitions.
Read skills/workflow-orchestrator/references/run-log-template.md for gate field expectations.

Produce a docs_contract_reconciliation_report at artifacts/docs_contract_reconciliation_report.md with:
- A drift_diagnosis section listing each inconsistency found
- A patches_proposed section with specific changes
- A validation_result section confirming validate-repo.py passes

Use repository-relative paths throughout. Do not modify validator scripts.
```
