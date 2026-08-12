# Sensemaking-skills dogfood evidence index

This index records the provenance of the dogfood artifacts and separates
historical observations from current-state evidence. It contains no production
code or owner decisions.

## Repository states

| Evidence group | Repository state | Meaning |
| --- | --- | --- |
| Baseline diagnosis | `63350d4` | Pre-fix observation of the interpreter handoff and related contract gaps. |
| Implementation worktree | `63350d4` plus uncommitted implementation changes | Post-fix local evidence captured before the implementation commit was merged. |
| Current state | `main` at `5c82e6b` | Post-merge evidence after PRs 166 and 167. |

## Artifacts

- `repo-sensemaker-dogfood-probe-report.yaml`: baseline probe report.
- `repository_sensemaking_brief_dogfood.md`: baseline sensemaking brief. Its
  `python3` citation is intentionally historical and should be validated
  against the baseline checkout, not against current `main`.
- `repo-sensemaker-implementation-probe-report.yaml`: implementation-worktree
  probe report captured before the fixes were merged.
- `docs_contract_reconciliation_report_dogfood.md`: reconciliation findings
  and proposed resolutions.
- `workflow_orchestration_plan_dogfood.md`: bounded plan derived from the
  baseline findings.
- `session_summary_dogfood.md`: handoff preserving the owner-gated follow-up
  decisions.
- `repo-sensemaker-current-dogfood-probe-report.yaml`: fresh probe of current
  `main` at `5c82e6b`.
- `repository_sensemaking_brief_dogfood_current.md`: current-state brief
  whose weakest boundary is the remaining authority/enforcement contract.

## Validation record

The current-state brief, current probe, baseline probe, implementation-worktree
probe, workflow plan, reconciliation report, and session summary pass their
applicable validators on the current checkout. The baseline brief is retained
as historical evidence; its old `python3` excerpt no longer matches the fixed
implementation on current `main`, which is why the current-state brief is
provided separately.

## Follow-up boundary

The version conflict, five missing fixture families, and ADR 0018-0020 status
findings are evidence candidates requiring owner decisions. This evidence
commit does not select an authority, add fixtures, or change ADR status.
