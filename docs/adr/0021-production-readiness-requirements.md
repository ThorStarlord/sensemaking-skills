# ADR 0021: Production-Readiness Requirements

**Status**: PROPOSED — draft for owner review, not yet accepted
**Date**: 2026-07-25
**Resolves**: Issue #36 (was blocked by #28 [closed], #32, #30 — both drafted in ADR 0017, ADR 0015)

---

## Context

This ADR answers what must be true for a *general availability* claim,
building on the proven golden path (#28) and the readiness criteria for
individual features (ADR 0017). Several of the sub-questions in #36
genuinely require owner/business input (cost budgets, supported-agent
commitments) rather than evidence already in the repo — those are called
out explicitly rather than guessed.

## Decision

**Settled by existing repo evidence:**
- **End-to-end test coverage**: the golden path must pass on this repo
  plus ≥1 real external repository (ADR 0017 criterion 3), with
  `scripts/test-validators.py` at 66/66 and `scripts/validate-repo.py`
  clean as the baseline gate (already true today).
- **Schema/artifact versioning**: additive-only changes to deterministic
  fields (ADR 0015) without a version bump; breaking changes require a
  contract update landing in the same PR as every consumer (already
  enforced by `tests/test_field_contract_agreement.py`).
- **Failure recovery**: rollback is proven via
  `git reset --hard HEAD && git clean -fd` (see
  `scripts/test-controlled-failures.py` Test 8/9) and `--resume` for
  paused gates (already implemented, `workflow-runtime.py --resume`).
- **Observability**: run logs (`run_log_*.md`) plus
  `docs/mode-coverage.yaml` are the audit trail (ADR 0004); this bar is
  already met.
- **Retry policy**: bounded retry, max 3 attempts, documented in this
  repo's `using-sensemaking` skill and referenced throughout memory —
  already the standing policy.
- **Secret handling**: no secrets are stored in artifacts or run logs by
  design (artifacts are plain Markdown/YAML in git); this is a structural
  property, not something requiring new work.

**Requires explicit owner decision (not resolvable from repo evidence):**
- Supported coding agents beyond Claude Code (commitment, not a technical
  fact) — the runtime is agent-agnostic (invoked via Skill tool + CLI), so
  this is a support/marketing scope decision, not an engineering blocker.
- Model-cost budgets and concurrency/rate-limiting policy — no existing
  cost-tracking mechanism in the repo to build this from; needs a fresh
  proposal once the owner sets a budget target.
- Supported platforms/environments beyond what's been exercised
  (Windows + the CI Ubuntu runner, per `.github/workflows/validation.yml`).

## Consequences
- General-availability sign-off can proceed once the "settled" items above
  are verified true on `main` and the "requires owner decision" items are
  explicitly answered (even if the answer is "defer to Phase 2").
- This ADR does not itself constitute a GA sign-off — it's the checklist.

## Owner sign-off required
Product-direction decision, and three items above require your explicit
input (cost/concurrency policy, supported-agent commitments, platform
support scope) that cannot be derived from the repository alone.
