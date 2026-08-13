# Evidence 0020 — Read-the-output pattern (artifact-gated reconciliation)

## Purpose

Formalizes the recurring process observed across the auteur analysis, the
per-issue implementations, and the self-dogfood reconciliation in this
session: treat every stage's output as a durable, contract-shaped artifact
that the next stage READS instead of trusting the producer's prose. This is
the operating pattern of the `artifact-reconciliation` workflow
(`skills/workflow-planner/references/workflow-registry.yaml`) and the
`output-reconciler` skill (`skills/output-reconciler/SKILL.md`).

## The pattern

Produce -> Read the artifact, not the prose -> Verify like-for-like ->
Dispose (fix | defer | file) -> Record.

The invariant: a handoff's claims are not facts. They are re-derived from
artifacts (probe reports, evidence records, validator output, diffs, merged
HEAD) before being trusted or acted on.

## Session evidence per move

| Move | Evidence from this session |
|---|---|
| Read the artifact, not the prose | The pasted auteur task summary was treated as claims, then re-derived from experiments/evidence/0016/0017, integration-report.md, and auteur's merged HEAD 8b8b7fd. This exposed two facts the summary flattened: the merged ADR direction contradicts evidence-rules Rule 7, and the executing repo used a stale vendored skill snapshot (no Rules 6-8, no test_case_count). |
| Verify like-for-like | The 2 test_generate_plan_conformance failures were confirmed pre-existing by stashing the registry change and re-running the baseline before attributing anything to the change. |
| Validator output is a first-class artifact | The validator harness (74/74) caught the validate-plan.py INPUT_MISMATCH coupling introduced by the prior_evidence workflow input -- a contract break no prose review surfaced. The harness output, not the agent's confidence, was the acceptance artifact. |
| Diff is an artifact with failure modes | CRLF whole-file churn was caught twice by comparing raw vs --ignore-cr-at-eol diff stats and repaired via amend (86148f9). |
| Disposition is recorded, never silent | Evidence 0019's "deliberately deferred" section records reasons for Vg=0.67, the ADR status findings, and the baseline test breakage. |
| The loop terminates in a durable artifact | Evidence 0018 + issues #170-175; evidence 0019; each commit message; each artifact feeds the next loop (0016 -> 0018 -> 0019). |

## Workflow encoding

`artifact-reconciliation` (Handoff Audit), plan_only/guided_execution:

1. repo-sensemaker -> repository_sensemaking_brief (probe-grounded state)
2. output-reconciler -> reconciliation_report (claims classified
   verified/disputed/omitted, dispositions fixed/deferred/filed)
3. to-issues -> issue_list (actionable findings filed)
4. handoff -> session_summary (next prompt)

Inputs: work_claim (the audited handoff/summary), repository_state,
prior_evidence (previous reconciliation reports -- the loop is closed:
each run's output is the next run's prior evidence).

## Prototype artifacts

- reconciliation_report prototype: experiments/evidence/0018-auteur-docs-contract-reconciliation-analysis/
- work_claim prototype: the pasted auteur task summary audited in that run
- deferred-disposition prototype: experiments/evidence/0019-sensemaking-self-dogfood-reconciliation/EVIDENCE.md

## Notes

- This record is authored documentation of an observed process; the
  workflow/skill/contracts it describes are the executable encoding.
- Not adjudicated here: whether the pattern should also be wired into
  execution-mode workflows (implementation-workflow) as an explicit gate
  artifact (validator-output-as-acceptance); proposal, not yet decided.
