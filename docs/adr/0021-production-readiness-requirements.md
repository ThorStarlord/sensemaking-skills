# ADR 0021: Production-Readiness Requirements

**Status**: PROPOSED — draft for owner review, not yet accepted. Owner has
explicitly deferred D7/D8; **no implementation or GA claim authorized**.
**Date**: 2026-07-25 (updated 2026-07-26)
**Proposes resolution for**: Issue #36 (was blocked by #28 [closed], #32,
#30 — proposed in ADR 0017, provisionally addressed in ADR 0015)

**2026-07-26 update**: following the 2026-07-26 product-contract review and
owner decision round (`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`), the
owner explicitly left this ADR's two readiness sub-items open rather than
deciding them now:
- **D7 (readiness target)**: **UNDECIDED by explicit owner instruction** —
  the review's recommendation was "externally validated," but the owner
  chose to leave this open pending the contract-redesign phase (D10)
  landing first, rather than pre-committing to a target now.
- **D8 (external-validation bar)**: **UNDECIDED by explicit owner
  instruction** — same reasoning; the review's recommendation was "at least
  two structurally different external repositories," not yet ratified.

This ADR's status does not change — it remains **Proposed**. Even once
D7/D8 are ratified, this ADR's three other named "requires explicit owner
decision" items (model-cost budgets and concurrency/rate-limiting policy;
supported-coding-agents commitment beyond Claude Code; supported
platforms/environments beyond Windows + CI Ubuntu) remain outstanding
regardless — per this ADR's own "Consequences" section, GA sign-off requires
*all* owner-decision items answered, not a subset.

---

## Context

This ADR answers what must be true for a *general availability* claim,
building on the golden path and the readiness criteria for individual
features (ADR 0017). Several of the sub-questions in #36 genuinely require
owner/business input (cost budgets, supported-agent commitments) rather
than evidence already in the repo — those are called out explicitly rather
than guessed.

**Evidence note (corrects the original draft's framing):** the golden path
referenced throughout this ADR is proven for exactly one workflow,
`architectural-review-planning-workflow`, via PR #57 (issue #55), PR #59
(issue #58), PR #60 (issue #56), PR #62 (issue #61), PR #64 (issue #63),
and PR #65 (issue #51) — Step 1 and Step 2, both positive and the
missing-`proposed_direction` negative path, all live and committed. It is
**not** proven against any external repository, and the other three
implementation workflows remain unproven with real agents. This ADR must
not be read as "product-wide production readiness is settled" — see the
per-item narrowing below.

## Decision

**Settled by existing repo evidence — narrowed to what is actually true:**
- **End-to-end test coverage**: the golden path passes on *this repository*
  for `architectural-review-planning-workflow`, live, both Step 1 and Step
  2, both the positive and missing-input negative path (PR #57, #59, #60,
  #62, #64, #65), with `scripts/test-validators.py` and
  `scripts/validate-repo.py` clean as the baseline gate. **The ≥1 real
  external repository leg of ADR 0017 criterion 3 is NOT met** — every
  merged proof ran against this repository (including via a standalone
  clone and disposable worktrees of it, per PR #65's evidence), never an
  independent codebase. The original draft of this ADR claimed this
  criterion was "already true today"; that was incorrect and is corrected
  here. Until an external-repo run exists, this item is **internally
  proven, externally unvalidated** — not a settled GA criterion.
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
  are verified true on `main`, the external-repository leg of end-to-end
  test coverage is actually run (not merely assumed), and the "requires
  owner decision" items are explicitly answered (even if the answer is
  "defer to Phase 2").
- This ADR does not itself constitute a GA sign-off — it's the checklist.
- **This ADR does not establish product-wide production readiness.** It
  establishes that one workflow's golden path is proven internally on this
  repository. Treating that as "production ready" for the whole product
  would be the same overbroad-claim error this revision corrects elsewhere
  in ADRs 0014/0017/0018.

## Owner sign-off required
Product-direction decision, and three items above require your explicit
input (cost/concurrency policy, supported-agent commitments, platform
support scope) that cannot be derived from the repository alone.

**Status as of 2026-07-26**: D7/D8 explicitly left UNDECIDED by owner
instruction (see the update note at the top of this ADR), not merely
unaddressed. The three items listed above (cost/concurrency, supported
agents, platform scope) remain outstanding regardless. This ADR stays
Proposed until the owner ratifies D7/D8 and answers the three items above.

---

## Hypothesis

A defined checklist of technical + policy criteria (test coverage,
versioning, failure recovery, observability, retry policy, secret handling,
plus three owner-decision items) determines whether the product is ready
for general availability.

## Supporting evidence

- Six of the seven "settled" bullets are backed by existing, running
  mechanisms independently verified in this campaign or prior ones:
  `tests/test_field_contract_agreement.py` (contract stability),
  `scripts/test-controlled-failures.py` (rollback), `--resume` (exercised
  directly in PR #65's positive and negative runs via the
  `_find_resume_state()` check), `docs/mode-coverage.yaml` +
  `run_log_*.md` (observability, and specifically repaired by PR #48/#60),
  and the bounded-retry policy documented in `using-sensemaking`.
- The one bullet that was NOT settled (end-to-end coverage including an
  external repository) has been corrected in this revision rather than
  left as an unverified claim.

## Missing evidence

- The external-repository leg of end-to-end coverage, as detailed above —
  the single largest gap in this ADR's evidence base.
- No evidence in this campaign addresses cost/concurrency, supported-agent
  commitments, or platform support beyond Windows + the CI Ubuntu runner —
  these remain genuinely open owner decisions, not evidence gaps that more
  testing would close.
- No evidence that the "settled" items hold under production-scale load
  (concurrent sessions, large repositories) — the campaign's runs were
  single-session, single-repository proofs.

## Experiment or review trigger

The recommended next evidence campaign is running the proven Step-1 +
Step-2 procedure against one real external repository. A successful run
would close the largest gap in this ADR; a failure would falsify the
implicit assumption that this repo's proof generalizes and should block any
GA claim until addressed.

## Status rationale

Remains **Proposed**, revised down from the original draft's implicit
"settled" framing. This ADR mixes real, verifiable technical facts (mostly
supported) with an explicit false claim (external-repo coverage) that has
now been corrected, plus three items that are owner decisions, not evidence
questions. None of that adds up to Provisional or Accepted status for a
product-wide readiness claim — at most it is Proposed with one clearly
identified blocking gap and three clearly identified owner decisions.
