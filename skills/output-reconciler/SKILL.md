---
name: output-reconciler
description: verify claims about completed work against durable repository artifacts, classify each claim verified/disputed/omitted, and produce a reconciliation report with findings and actionable recommendations. use when a work_claim artifact (a handoff, task summary, or status report) asserts work was done and the claim must be grounded before it is trusted or acted on.
---

# output-reconciler

Reads the output of a stage as an artifact, never as trusted prose. Every
claim in the audited `work_claim` is re-derived from the repository tree,
probe reports, evidence records, and validator outputs before it is
accepted. This is the "read-the-output" pattern (evidence 0020): produce ->
read the artifact, not the prose -> verify like-for-like -> dispose
(fix | defer | file) -> record.

## Inputs

- `work_claim` (required): the handoff/task summary whose claims are audited.
- `repository_sensemaking_brief` (required): the repo-sensemaker diagnosis of
  the target repository (verified current state from the probe report).
- `prior_evidence` (recommended): earlier briefs, postmortems, and evidence
  records about the target (e.g. `experiments/evidence/NNNN-*`,
  `docs/reviews/*`). Framework learnings captured after the target vendored
  its skills must still reach this reconciliation (evidence 0018).

## Workflow

1. **Extract claims**: split the `work_claim` into falsifiable statements.
   A claim is falsifiable if it names an artifact, a metric, a commit, or a
   state that exists (or does not) in the tree.
2. **Ground each claim**: for every claim, find the durable artifact that
   proves or disproves it (probe-report.yaml fields, evidence records,
   validator output, `git log`/`git mv` state, merged HEAD). Cite the
   artifact with its location.
3. **Classify**: mark each claim `verified`, `disputed`, or `omitted`.
   - `verified`: the artifact supports the claim (like-for-like, same
     baseline and same change).
   - `disputed`: the artifact contradicts the claim, or the claim's own
     evidence is absent from the tree.
   - `omitted`: the claim is silent about something the artifacts show --
     a handoff that flattens a controversy (evidence 0018: the auteur
     summary omitted the Rule 7 direction conflict and the stale vendored
     skills).
4. **Compare like-for-like**: before attributing a failure to the claimed
   change, run the same check on the baseline. A failure present on both is
   a pre-existing condition, not a claim to dispute.
5. **Dispose**: for each disputed/omitted claim, one of:
   - fix (repair the producer or consumer), or
   - defer with a written reason (never silently), or
   - file (turn the finding into an issue for the tracker).
6. **Emit**: write the `reconciliation_report` artifact (Section 13
   machine-readable handoff, see below) with the classified claims,
   findings, lessons, and recommendations.

## Output

`reconciliation_report` artifact with required sections `claims`,
`findings`, `recommendations`, and this Section 13 machine handoff:

```yaml
artifact_id: reconciliation_report
schema_version: 1
source_claim_ref: <path of the audited work_claim>
claims:
  - claim: <falsifiable statement from the work_claim>
    classification: verified | disputed | omitted
    artifact: <the artifact that grounds the verdict, with location>
    disposition: none | fixed | deferred | filed
findings:
  - concept: <domain concept>
    finding_type: <e.g. claim_contradicted | claim_omitted | pre_existing>
    observations:
      - source: <path>
        location: <path:line>
        value: <observed value>
        evidence: <short quote or metric>
    confidence: high | medium
    requires_semantic_review: true | false
    notes: <why this matters>
recommendations:
  - issue: <one actionable item>
    target: <repo surface that owns the fix>
created_at: <ISO 8601 UTC>
immutable: true
```

## Mutate Rules

- **Read-only until disposition**: the skill verifies and classifies before
  any write. Repairing a producer/consumer is a separate authorized step.
- **No silent dispositions**: every disputed/omitted claim ends in
  `fixed`, `deferred` (with a reason), or `filed` (with an issue ref).
- **No new field names**: field names above are the contract; add none.
- **Do not touch unrelated code**: repairs are scoped to the claim being
  reconciled.

## References

- [Evidence 0020: read-the-output pattern](../../experiments/evidence/0020-read-the-output-pattern/EVIDENCE.md)
- [Evidence 0018: auteur docs-contract-reconciliation analysis](../../experiments/evidence/0018-auteur-docs-contract-reconciliation-analysis/EVIDENCE.md)
- [Evidence Rules: repo-sensemaker](../../skills/repo-sensemaker/references/evidence-rules.md)
- [Artifact Contracts: reconciliation_report](../../skills/workflow-planner/references/artifact-contracts.yaml)
