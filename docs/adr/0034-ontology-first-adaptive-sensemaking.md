# ADR 0034: Ontology-First Adaptive Sensemaking — Product Identity and Single Entrypoint

**Status**: ACCEPTED — owner-selected 2026-10-28 in the owner-supplied plan "Ontology-First Adaptive Sensemaking: Product Architecture and Implementation Plan" (baseline `main@f805124`). This ADR records the selection, not an implemented capability or demonstrated benefit.
**Date**: 2026-10-28
**Level**: Level 4 — Product Thesis / Strategy Revision
**Disposition**: REVISE the product's primary outcome and public entrypoint; preserve ADR 0029's external execution and authority boundary and ADR 0031's destination
**Related authority**: ADR 0013 (agent-native orchestration), ADR 0029 (product boundary), ADR 0030 (Grounding Pack), ADR 0031 (persistent semantic stewardship), `docs/product-strategy.md`, `docs/product-thesis-revision.md`

## Context

ADR 0031 made persistent semantic stewardship the long-term destination and called selecting the next engineering responsibility "an instrumental capability". The operating guidance did not follow it all the way:

- `using-sensemaking` described its default as discovering "the next warranted engineering responsibility", guided by an Architect -> Builder -> Reconcile construction loop.
- `GETTING_STARTED.md` told users the repository-only entry discovers "what to build next".
- `strategic-sensemaking-loop` presented itself as a second "single front door" for strategic work.
- `CLAUDE.md` described the general capability as Architect -> Builder -> Reconcile construction under Value-Directed Continuous Construction.

The first target-repository application (`docs/normal-use/prospective-reasoning-atlas-001.md`) showed the cost of that framing. Consequence exploration was the most valuable activity, and the useful outcome was understanding: what was considered, why, and what it was expected to cause. Implementation was the smaller part. It also showed that reasoning and knowledge can pass every check and still be unreachable to the next agent.

## Decision

The owner selected the following governing decisions.

**A. Product identity.** Sensemaking is an ontology-grounded repository understanding and prospective reasoning system. It is not primarily an implementation agent, code factory, backlog executor or automated task picker.

**B. Single public entrypoint.** `using-sensemaking` owns public invocation and adaptive control. Other Skills keep their specialized responsibilities and stay directly invokable by maintainers, but ordinary users need to know only `using-sensemaking`.

**C. Ontology-first initial engagement.** When Sensemaking is applied to a repository without an adequate semantic model, it first establishes source-grounded domain and architecture knowledge before making repository-wide strategic selections.

**D. Breadth before strategic convergence.** A preferred product-evolution direction is not selected solely from the first visible weakness or the most recent backlog item. Sufficient coverage of the relevant possibility landscape comes first.

**E. Adaptive composition.** The active agent decides which specialized reasoning procedures are warranted and in what order, and may revisit earlier reasoning when new evidence changes the decision.

**F. Implementation is optional.** Understanding, exploration, architecture synthesis, evaluation and durable knowledge are complete, legitimate outputs. Implementation is a separate downstream decision that needs its own authority.

**G. One semantic controller.** The active agent applying `using-sensemaking` keeps responsibility-selection judgment. Strategic continuation procedures support that controller; they are not a competing public orchestrator.

The primary outcome for a repository is **durable, source-grounded understanding and an informed prospective selection** (or a justified decision not to select), preserved so the next session starts from it.

## Relationship to earlier decisions

- **ADR 0031** is extended, not replaced. Its destination (persistent, typed, queryable semantic knowledge operated through Skills) is unchanged. This ADR makes understanding and prospective reasoning the default outcome of using the product, and makes construction ("Path 2") an optional downstream use of that knowledge rather than the default identity.
- **ADR 0013** is consistent: the active agent remains the controller and Skills remain platform-agnostic. This ADR names which Skill carries that control publicly.
- **ADR 0029** is unchanged. A single entrypoint is not a deterministic router. Automatic responsibility, Skill or workflow selection by machinery, autonomous merge, release, deployment and publication all stay outside product scope.
- **ADR 0030**'s Grounding Pack remains a valid compact entry representation.
- **ADR 0033** stays PROPOSED; this ADR neither depends on nor ratifies it.

## What this supersedes

| Earlier instruction | Status after this ADR |
| --- | --- |
| `using-sensemaking` default: "discover the next warranted engineering responsibility" | SUPERSEDED as the default outcome; a warranted next responsibility remains a valid result when the reasoning supports one |
| Architect -> Builder -> Reconcile as the general Sensemaking capability (`using-sensemaking`, `CLAUDE.md`, `README.md`) | REVISED: the portable construction loop remains, activated as optional downstream realization |
| `strategic-sensemaking-loop` as a public "single front door" | REVISED: it becomes an internal continuation capability that `using-sensemaking` composes |
| `GETTING_STARTED.md`: repository-only entry discovers "what to build next" | SUPERSEDED: the entry establishes understanding and explores what the repository could become |
| `setup-sensemaking-skills` described as configuration before first use | REVISED: setup is optional and never a prerequisite for the entrypoint |
| Owner construction-phase rules for **this** repository's own development (`CLAUDE.md` local verification scope and PR rules) | UNCHANGED: they govern how this repository is built, not what the product does for users |

Earlier evidence, accepted decisions and receipts remain historically accurate. Superseded text is revised in place only where it states current behavior. Historical records are not rewritten.

## What does not change

- Deterministic machinery never selects responsibilities, Skills or strategy (ADR 0029 boundary law).
- Nothing fabricates authority. Findings, preferences, selections and implementation authorization stay distinct.
- Knowledge schemas, artifact contracts, receipts and their validators stay compatible. Repository-specific domain concepts use the existing vocabulary unless a demonstrated gap passes the schema-evolution procedure.
- Narrow requests keep their scope. An explicit implementation request with an adequate governing decision does not need a new repository-wide exploration.

## Evidence ceiling

This is a product-identity selection. Nothing yet establishes that ontology-first entry improves decisions, that a single entrypoint composes specialists reliably across hosts, or that knowledge from one session is reused by another. The Atlas Midgard application reached representation, same-session retrieval and local decision usefulness only.

## Downstream reconciliation required

Per `docs/product-thesis-revision.md` section 12, Level 3 reassesses before thesis-dependent work resumes.

| Affected surface | Classification | Disposition |
| --- | --- | --- |
| `using-sensemaking` entry contract | CONTRADICTORY | REVISE (plan PR 2) |
| `repository-semantic-steward` BOOTSTRAP as an occasional mode | STALE | REVISE: first-engagement entry responsibility (plan PR 3) |
| Strategic Exploration Funnel convergence | STILL_RELEVANT | EXTEND with a possibility coverage assessment (plan PR 4) |
| Prospective reasoning procedures | STILL_RELEVANT | COMPOSE through the entrypoint (plan PR 5) |
| `strategic-sensemaking-loop` public role | CONTRADICTORY | REVISE to internal continuation (plan PR 6) |
| Implementation-first onboarding and descriptions | CONTRADICTORY | REVISE (plan PR 7) |
| `STATUS.md` current next step (PATH-1 accretion through genuine responsibilities) | SUSPECT | REASSESS: PATH-1 continues only as it serves this identity; this program comes first |
| `CLAUDE.md` description of the general capability | STALE | REVISE wording; keep local construction rules |

## Implementation (2026-10-28)

Implemented in guidance through #640 (identity), #641 (controller), #643 (bootstrap), #644 (coverage and composition), #645 (continuation) and #646 (onboarding), with #642 repairing fixtures. The first assessment is `docs/normal-use/ontology-first-entry-atlas-001.md`. The evidence ceiling above still holds: no independent or cross-session use has been observed.

## Owner ratification

The owner supplied the governing decisions A–G on 2026-10-28 and asked for them to be recorded as "the owner's newly selected product identity". Implementation proceeds through ordinary reviewed PRs under the repository's construction policy.
