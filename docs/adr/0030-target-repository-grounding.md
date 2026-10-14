# ADR 0030: Target-Repository Grounding Pack

**Status**: ACCEPTED — owner-delegated 2026-10-12 (owner asked the agent to choose owner decisions and proceed)  
**Date**: 2026-10-12  
**Supersedes**: none. Does not change ADR 0029.  
**Level**: Level 4 — Product Thesis / Strategy Revision (applied through `docs/product-strategy.md`, section 1 revision note)

## Context

Sensemaking's existing ontology (`CONTEXT.md`) and its main repository artifact (`repository_sensemaking_brief`) describe Sensemaking's own decision process. Nothing records a target repository's intent, non-goals, invariants, traps, or past decisions for the next agent session. Analysis in [`docs/research/repository-grounding-direction-2026-10.md`](../research/repository-grounding-direction-2026-10.md) argues that for a capable coding agent, repository-specific context is the main limit on delegated work, but that a spec detailed enough to determine implementation is the implementation, and that owner intent cannot be recovered from code.

## Decision

1. A target repository may carry a **Grounding Pack** at `.sensemaking/` (or reuse an existing `CONTEXT.md`, `docs/adr/`, and `CLAUDE.md`): `intent.md`, `context.md`, `invariants.md`, and `decisions/`. Template: `templates/grounding-pack/`.
2. Each factual line carries one provenance tag: `[code: path]`, `[test: path]`, `[owner: date or link]`, or `[hypothesis]`. A `[hypothesis]` line does not justify an action by itself.
3. Lines are included only if the code cannot supply them cheaply. Checkable rules belong in tests, types, or lints, cited from the pack.
4. Each file has a hard word budget (see the template). Over-budget files are cut or merged; new files are not added.
5. The **question ratchet**: before asking the owner, an agent checks `intent.md` and `decisions/`; each owner answer is recorded with an `[owner: date]` tag in the same change.
6. The Repository Sensemaking Brief and its contract fields stay for compatibility. Nothing that a test or validator reads is removed by this ADR.

## Owner delegation

The owner asked the agent to choose owner decisions and proceed. Choices recorded under that delegation:

- Phase 0 approval of the direction: accepted.
- First target repository: `ThorStarlord/React_incremental_game_prototype` (real ongoing work and Build Validation CI). Access to it was denied in the session that made this choice, so Phase 2 is pending.

Major reversals of this ADR remain Level-4 decisions.

## Consequences

- Positive: a fresh agent gets target-specific intent and traps without reading the whole codebase; owner answers stop repeating.
- Negative: the pack can go stale; mitigated by same-change updates and the budgets.
- Not claimed: that the pack improves outcomes. That is the hypothesis in `docs/product-strategy.md` section 9, to be tested in Phase 3.

## Amendment 2026-10-12 (status amendment; original decisions above are preserved)

- **Provenance (replaces decision 2 above).** Each factual line carries exactly one primary tag: `[policy: path]` (authority document), `[code: path]` (source file), `[test: path]`, `[owner: date]` (owner intent), `[delegated: date]` (agent choice under owner delegation), or `[hypothesis]` (agent inference). Supporting sources use an ordinary Markdown link, not a second tag.
- **Question ratchet (replaces decision 5).** Reuse a recorded answer while it still applies to the current scope. Ask again only if the scope changed, the decision was superseded, or new evidence materially challenges it.
- **Status correction (2026-10-14; supersedes the earlier Phase 2 snapshot).** The first target Grounding Pack was merged via `ThorStarlord/React_incremental_game_prototype` PR #166 on 2026-10-12. The owner approved `intent.md` and accepted the corrected citations with a **spot-check waiver**, not a passing quality sample: 20% of the fresh 10-line check needed correction against the planned 10% ceiling. Phase 2 is complete by owner directive; comparative Phase 3 remains unexecuted. See `docs/normal-use/grounding-pack-build-001.md`. The earlier "blocked by access" note is historical.
