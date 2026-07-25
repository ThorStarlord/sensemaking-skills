# ADR 0017: Readiness Criteria for Adding New Features

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #32

---

## Context

Standing principle: "fix the spine before adding breadth. One canonical
path must prove end-to-end." The golden path (#28) is now proven via #38/#39.
This ADR defines the measurable bar for what "proven" means so future
feature work has a consistent gate.

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
   self-repository bias. (Raising this bar to N>1 is a Phase 2 decision,
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
