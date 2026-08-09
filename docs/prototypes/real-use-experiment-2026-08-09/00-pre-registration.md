# Real-use experiment — pre-registration

Written before spawning the diagnostic subagent, so this cannot be
retroactively cleaned up to make the experiment look tidier. This is a
genuine owner-originated decision, not a synthetic test question.

## Exact owner-originated question (verbatim)

> "Given the current state of Sensemaking Skills, what should I focus on
> next to create the most product value, and what should I deliberately
> stop investing in?"

## Repository revision / pins

- Repository: `H:\GithubRepositories\sensemaking-skills`
- Branch under evaluation: `prototype/repo-sensemaker-vnext`
- HEAD at experiment start: `abab6c497cdd056dd6f50862c8fc448868ef63a9`
- `main` at experiment start: `e790f30` (unchanged since branch point;
  PR #162 merged, PR #163 open/mergeable, PR #164 open/mergeable/draft —
  all confirmed immediately before this record was written)
- No rebase performed — #163 still open, no material overlap requiring one.

## Known owner intent, before investigation

Recovered from this conversation's own history — not re-derived from the
repository, since that's repository-diagnostician's job, not this step's.

- Sustained emphasis, repeated across many turns, on returning to "the
  product sequence" / "real product use" rather than continuing
  infrastructure/cleanup work indefinitely — explicit statements against
  chasing every newly-discovered drift item into "another infrastructure
  campaign."
- Explicit epistemic discipline: `implemented ≠ validated ≠ owner-ratified
  ≠ production-ready` — repeatedly insisted on, most recently as a formal
  standing instruction for `prototype/*` work.
- A long-running, multi-experiment research line already exists and
  predates this conversation: P1-P4 and S1-S2 (solution-interaction)
  experiments, all about *interaction design* as a value driver for
  `repo-sensemaker` — S2 was merged into `main` before this conversation
  began. This looks like a sustained, deliberate owner research interest,
  not incidental.
- Explicitly deferred, not yet acted on: the `fog_type` runtime alias fix
  (waiting on #163), three further canonical-vocabulary.yaml drift items
  (recorded, not fixed), the INFRA-004 PM-engineering contract gap
  (recorded, xfail-marked), external validation (ADR 0021-gated, not
  self-authorizable).
- Heavy, real investment already made in exploring the repo-sensemaker /
  repository-diagnostician architecture split, brief vNext fields, evidence
  tooling, and one downstream consumer (PR #164) — explicitly still
  PROTOTYPE ONLY, explicitly said to require real use (not more
  construction) as the next evidence.
- **What I do NOT already know**: the actual current state of the several
  other major subsystems visible in `.github/workflows/validation.yml`
  (Gate A security suites, "Phase 2" campaign validation, "Phase 3"
  exploratory authorization, "Phase 4" campaign ledger, "Phase 5"
  EXP-0001 preparation, "Phase 6" execution boundary) — these were only
  ever seen as CI job names in this conversation, never actually
  investigated. My intent knowledge here is thin to none. This is exactly
  the kind of thing repository-diagnostician's investigation, not my prior
  memory, needs to establish.

## Status before investigation

This is genuinely **thin-to-moderate**, not sufficient: real context exists
for the repo-sensemaker/vNext track specifically, but the question asks
about the *whole repository's* next-highest-value investment, and several
large subsystems are essentially unknown to me going in. Recording this
honestly, before investigation, is the point of this file.
