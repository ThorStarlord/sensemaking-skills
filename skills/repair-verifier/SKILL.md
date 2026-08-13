---
name: repair-verifier
description: re-run the probe after a docs-contract-reconciliation patch and verify that the original brief's findings no longer reproduce, marking each finding closed or remaining. use as the final gate of docs-contract-reconciliation before handoff.
---

# repair-verifier

The diagnostic brief is consumed by its own verification: after the
reconciler applies fixes, this skill re-measures the repository and checks
each original finding against the fresh state. Structural closure (the
re-probe) plus direction-evidence closure (validate-brief's
`collision_dedup_direction` rule) together prove the reconciliation worked.

## Inputs

- `docs_contract_reconciliation_report` (required): the reconciler's output;
  it names the fixes and cites the original brief.
- `prior_evidence` (recommended): the original `repository_sensemaking_brief`
  and its probe report — the acceptance criteria.
- `repository_state`: the repository to re-probe.

## Workflow

1. **Locate the original findings**: from the reconciliation report and
   prior evidence, list the original brief's findings (duplicate ids, stale
   docs claims, artifact sprawl, fixture gaps, etc.).
2. **Re-probe**: run `python scripts/probe-repo.py --repo-root <target>` and
   validate the report (`scripts/validate-probe-report.py`). Use the probe
   report, never the reconciler's prose, as the measured state.
3. **Check each finding**: for every original finding, decide from the fresh
   probe report whether it is `closed` (no longer reproduces: e.g.
   `relationships.adr.findings` has no `duplicate_id`, `fixtures_coverage`
   has no unexplained `missing_fixtures`, `context_entropy.ce` is measured)
   or `remaining` (still reproduces, with the fresh evidence).
4. **Emit**: write the `repair_verification_report` artifact. If any
   finding remains, the gate `review_reconciliation_verified` must not be
   approved silently — the remaining findings are either fixed in a follow-up
   or recorded as deferred with a reason (evidence 0019 doctrine).

## Output

`repair_verification_report` artifact with required sections
`findings_closed`, `findings_remaining`, `probe_summary`, and this
Section 13 machine handoff:

```yaml
artifact_id: repair_verification_report
schema_version: 1
verified_brief_ref: <path of the original repository_sensemaking_brief>
findings_closed:
  - finding: <original finding, cited from the brief>
    evidence: <fresh probe field proving closure>
findings_remaining:
  - finding: <original finding still reproducing>
    evidence: <fresh probe field>
    disposition: fixed_in_follow_up | deferred
    reason: <why it remains>
created_at: <ISO 8601 UTC>
immutable: true
```

## Mutate Rules

- **Read-only**: this skill never modifies the repository; it only measures.
- **No silent remaining findings**: every `remaining` entry carries a
  disposition and a reason.
- **Cite the probe**: every verdict is grounded in a fresh
  `probe-report.yaml` field, not in the reconciler's summary.

## References

- [Probe Engine: CONTEXT.md](../../CONTEXT.md)
- [Artifact Contracts: repair_verification_report](../../skills/workflow-planner/references/artifact-contracts.yaml)
- [Evidence 0019: self-dogfood reconciliation (deferred-items doctrine)](../../experiments/evidence/0019-sensemaking-self-dogfood-reconciliation/EVIDENCE.md)
