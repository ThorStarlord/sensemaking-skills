# ADR 0017: Readiness Criteria for Adding New Features

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #32

---

## Context

Standing principle: "fix the spine before adding breadth. One canonical
path must prove end-to-end." The golden path (#28, narrow-scope decision)
is now proven for `architectural-review-planning-workflow` only, via merged,
committed, reviewable evidence: PR #57 (issue #55, runtime-owned Step-1
structure), PR #59 (issue #58, live Step-1 semantic validity), PR #60
(issue #56, mode-coverage preservation), PR #62 (issue #61, resume state),
PR #64 (issue #63, YAML fence contract), and PR #65 (issue #51, live Step-2
positive and negative proof). Issue #39's original claim was a free-text
issue comment with no linked commit, PR, or preserved artifacts; it was
never independently verifiable and issue #51 was opened specifically to
replace it with durable evidence. This ADR treats #39 as historical and
not authoritative — the citations above are the actual evidence base. This
ADR defines the measurable bar for what "proven" means so future feature
work has a consistent gate.

## Decision

A feature (new skill, workflow, or artifact type) may be added once:

1. **Golden-path parity**: it follows the same producer/consumer artifact
   pattern as the proven path — session-scoped output via
   `expected_output_path` (ADR 0010), declared in
   `artifact-contracts.yaml`, with both a generic (`validate-artifact.py`)
   and (if needed) specialized validator.
2. **Test coverage**: a fixture pair (valid + invalid) in
   `tests/fixtures/`, wired into `scripts/test-validators.py`, and at
   least one end-to-end test exercising the real runtime path (not just
   the validator in isolation) — per CLAUDE.md's "Done requires running
   the real path."
3. **Real-repo proof**: the golden path succeeds on **at least 1 real
   external repository** in addition to this repo, to catch
   self-repository bias. **This criterion is not yet met for the currently
   proven golden path**: every merged proof (PR #57, #59, #60, #62, #64,
   #65) ran against this repository itself (or a standalone clone / disposable
   worktree of it) — never against an independent external repository. The
   N=1 threshold's rationale is "catch self-repository bias" (a repo whose
   own structure and conventions may make its own diagnostic tooling look
   more reliable than it is on unfamiliar code); N=1 is chosen as the
   minimum bar that exercises this risk at all, not as a statistically
   validated sample size. (Raising this bar to N>1 is a Phase 2 decision,
   not a blocker for the first feature additions.)
4. **Contract stability**: no existing artifact contract's *deterministic*
   fields (ADR 0015) change shape — only additive changes are allowed
   without a version bump; breaking changes require updating
   `artifact-contracts.yaml` and every consumer in the same PR (this
   repo's own field-contract-agreement rule already enforces this for
   routing fields via `tests/test_field_contract_agreement.py`).
5. **No orphaned coverage claims**: any new workflow/mode combination
   claiming to be "proven" must have a real, committed run log backing its
   `docs/mode-coverage.yaml` entry (ADR 0004, enforced by
   `validate-mode-coverage.py` — see #47/#48).

## Consequences
- This becomes the checklist for accepting future feature PRs.
- Directly informs ADR 0021 (production-readiness requirements), which
  asks the same question at the whole-product level rather than the
  per-feature level.

## Owner sign-off required
Product-direction decision; confirm or amend before treating as Accepted.

---

## Hypothesis

A feature (new skill/workflow/artifact type) is ready to add once it meets
five criteria: golden-path parity, test coverage, external-repo proof,
contract stability, and non-orphaned coverage claims.

## Supporting evidence

- Criteria 1, 2, 4, and 5 are directly modeled on mechanisms the merged
  campaign exercised repeatedly: session-scoped `expected_output_path`
  (ADR 0010, exercised by every run in PR #65's evidence),
  `tests/test_field_contract_agreement.py` (existing, running),
  `scripts/test-validators.py` fixture pairs (existing, running), and
  `validate-mode-coverage.py` closing the exact orphaned-coverage gap found
  and fixed in PR #48 (issue #47) and PR #60 (issue #56).
- The golden path itself (PR #57, #59, #60, #62, #64, #65) is a worked
  example that satisfies criteria 1, 2, 4, and 5 for
  `architectural-review-planning-workflow` — proof the checklist is
  achievable, not just aspirational.

## Missing evidence

- Criterion 3 (external-repo proof) is **unmet by the very path this ADR
  uses as its own supporting example** — see the inline note above. No
  merged evidence runs the golden path outside this repository.
- No feature has yet been proposed and run through this checklist
  end-to-end as an acceptance gate; the checklist is inferred from what
  proof techniques worked, not validated as a gate by rejecting or
  accepting a real feature proposal.

## Experiment or review trigger

The recommended next evidence campaign (see final report) is running the
proven Step-1 + Step-2 procedure against one real external repository —
this would be the first evidence for criterion 3. Revisit this ADR's N=1
threshold if that run surfaces a self-repository-bias failure mode N=1
wouldn't catch.

## Status rationale

Remains **Proposed**. This is an operational-policy ADR whose mechanics are
well-supported by evidence, but its own criterion 3 is explicitly unmet —
an ADR cannot honestly claim Provisional or Accepted status for a readiness
bar that the evidence base itself has not cleared.
