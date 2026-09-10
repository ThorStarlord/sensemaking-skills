# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** finalized post-milestone handoff; repository implementation complete, empirical external qualification pending  
**Primary program:** Sensemaking Campaign productization  
**Current `main` at handoff finalization:** `de1013fc675f8981b24749ff068427f0140e08ba`  
**Current frontier:** no pending repository work package; next decision depends on real-harness evidence

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, target identity, narrative/evidence binding, and reconstructible qualification evidence.

## Handoff finalization

This handoff was revalidated on 2026-09-10 against `main@de1013fc675f8981b24749ff068427f0140e08ba`, the merge of PR #305. This documentation refresh does not change product code and does not cause later commits to inherit earlier exact-head qualification claims.

The milestone remains complete. The next repository change must be justified by genuine external dogfood evidence (or another separately authorized objective), not by inventing a fourth implementation package.

## Release architecture continuity

This handoff preserves the validated v0.3 release architecture rather than replacing it:

- **Campaign schema v2** remains the current durable representation baseline. Historical v1 artifacts migrate deterministically without inventing semantics or rewriting append-only history.
- The shipped **product/lab split** remains intact: Product Validation owns shipped/installed-product claims, while retained Lab Validation owns source-only research/lab claims.
- The release includes the **real-harness qualification verifier**. Verifier and receipt success are mechanical evidence about exact frozen bytes; they are not semantic truth and do not by themselves prove that a live harness created the attempt.

## Current milestone handoff

The most recent three-package milestone is complete:

| Package | PR | Exact candidate head | Merge commit | Delivered |
|---|---:|---|---|---|
| Package 1 — Post-Milestone Release Contract Reconciliation | #302 | `2cb50eae32516f716d9c62846876e67b1f5741ec` | `7e539dd88742fc7fca27e7a1368682047719bcda` | Reconciled stale v0.3/P11 release documentation, restored product/lab and real-harness contract wording, and preserved exact-head qualification boundaries. |
| Package 2 — Narrative Verification Receipts | #303 | `a3cede49449ad2857bc348c7ba06877acc113ac0` | `732ea14752510dc05352ddcc004010a3e2d9284c` | Added append-only receipts that bind exact current Campaign narrative claims to exact durable evidence bytes without claiming semantic truth or authorizing transitions. |
| Package 3 — Durable Qualification Evidence Receipts | #304 | `86f9a2ec96ed58ce096c71184f03a6ff839f3473` | `cd183827b438107dafd65f48fa23145b2e21fbdd` | Added content-bound receipts for structurally valid frozen external attempts plus CI verification for future checked-in qualification evidence. |

All three packages are merged. There is no fourth implementation package implied by this handoff.

## Evidence verified for this milestone

### Package 1

Exact head `2cb50eae32516f716d9c62846876e67b1f5741ec` completed successfully in:

- Product Validation;
- Release Candidate Distribution.

The package was documentation-only and preserved the rule that later heads cannot borrow an earlier candidate's qualification.

### Package 2

Exact head `a3cede49449ad2857bc348c7ba06877acc113ac0` completed successfully in:

- Product Validation;
- Lab Validation;
- Release Candidate Distribution.

The dedicated `tests/campaign_validation/test_campaign_narrative_verification.py` suite includes positive and rejection coverage for exact narrative membership, unknown fields/scopes, missing evidence, orphan artifacts, unsafe or duplicate receipt IDs, evidence deletion/mutation, receipt tampering, historical-state behavior, and non-mutation of Campaign lifecycle state.

### Package 3

Exact head `86f9a2ec96ed58ce096c71184f03a6ff839f3473` completed successfully in:

- Product Validation;
- External Golden Path Qualification;
- Release Candidate Distribution.

The qualification-evidence contract rejects structurally invalid attempts, append-only overwrite attempts, receipt tampering, and mutated attempt/evidence bytes. Structurally valid recorded failures remain `qualified: false` evidence rather than being rewritten into PASS.

## Pending human / empirical gates

Repository-side qualification machinery is complete, but empirical qualification is **not** complete.

Current repository-owned evidence status remains:

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
Human/external action required for empirical PASS: YES
```

A synthetic fixture, green contract test, generated receipt, or repository-local transformation is **not** evidence that a real coding-agent harness performed the run.

A real empirical PASS requires an actual external coding-agent harness attempt frozen under:

```text
v0.3-external-golden-path-dogfood-v1
```

and then verified against the exact frozen attempt bytes.

Other owner-controlled gates remain separate:

- tagging/publication of v0.3.0 is an explicit owner decision;
- any milestone/release claim that requires retained Lab Validation must use the intended exact head;
- a real-harness failure or INVALID result must be preserved honestly rather than repaired into a PASS artifact.

## Recommended next priorities

These are recommendations for the next milestone session, not pre-authorized implementation packages.

1. **Run one genuine external golden-path dogfood attempt.** Use a real supported coding-agent harness against an external repository, complete the canonical Campaign lifecycle without prior-chat/manual-repair shortcuts, freeze the evidence package, generate the qualification receipt, and preserve the recorded outcome.
2. **Turn the empirical result into the next milestone decision.** If the attempt passes, check in the frozen evidence and requalify the exact evidence PR head. If it fails or is invalid, preserve that result and derive the smallest repository improvement from the observed failure rather than broadening scope speculatively.
3. **Evaluate operator ergonomics only after dogfood.** Narrative verification currently ships as a Python service/API (`CampaignNarrativeVerificationService`), not a new `sensemaking-skills campaign ...` CLI subcommand. Add a first-class CLI only if real usage demonstrates that it is the next warranted boundary.

## Product and semantic boundaries

Keep these distinctions explicit:

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
narrative claim bound to evidence != evidence proves claim
narrative verification receipt != warranted transition
qualification receipt != real-harness origin proof
synthetic fixture PASS != empirical real-harness PASS
lineage != semantic warrant
handoff != semantic recommendation
```

The Campaign Controller is not a semantic router.

## Current product baseline

The earlier v0.3 product-code baseline remains the completed Feature-3 merge from the preceding milestone:

```text
24a88bf6311122dae1257999f5a7379cb0b095d5
```

That preceding milestone delivered CI Authority Reconciliation (#298), v0.3 Release Baseline Rebuild (#299), and Durable Target Snapshot Binding (#300). The current #302–#304 milestone builds on that baseline with release-document reconciliation, narrative verification receipts, and qualification evidence receipts.

## Operator handoff / commands

Use `docs/post-milestone-handoff-runbook.md` for the newly added Package 2/3 service usage, qualification-evidence commands, focused positive/rejection test suites, checked-in evidence protocol, and the empirical handoff procedure. Its quick-command index is the shortest path for future engineers to reproduce the milestone-specific checks.

Use `docs/milestone-runbook.md` for the earlier v0.3 Product Validation, Lab Validation, Release Candidate Distribution, target-bound Campaign, harness setup, filesystem-security, and worktree procedures.

When prose and a checked-in workflow disagree about exact CI commands, the workflow is executable authority and the documentation should be reconciled.

## Canonical sources

- `STATUS.md` — current milestone state and next-session handoff.
- `docs/post-milestone-handoff-runbook.md` — Packages #302–#304 operational commands and evidence protocol.
- `qualification-evidence/STATUS.md` — empirical external-qualification status.
- `docs/campaign-narrative-verification.md` — narrative verification receipt contract.
- `docs/qualification-evidence.md` — qualification evidence receipt contract.
- `docs/external-golden-path-verifier.md` — external attempt package/verifier protocol.
- `docs/milestone-runbook.md` — v0.3 baseline operations and qualification runbook.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — retained Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.
- `.github/workflows/external-golden-path.yml` — external qualification/evidence authority.
