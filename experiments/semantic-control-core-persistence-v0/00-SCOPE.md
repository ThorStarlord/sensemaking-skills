# 00 — SCOPE: SEMANTIC CONTROL CORE — PERSISTENCE / MAINTENANCE PROTOTYPE v0

**Prototype id:** `SEMANTIC_CONTROL_CORE_PERSISTENCE_V0`
Terminology: still `THIN_SEMANTIC_CORE_CANDIDATE`. **Not** ratified persistence,
**not** product architecture, **not** a canonical doc, **not** an ADR, **not**
infrastructure.

## Why this exists

Owner review of V1 (draft PR #245) accepted
`THIN_CORE_PLUS_PROJECTIONS_PRESERVES_VALUE` as the leading architecture design
and set the next responsibility:

1. append the V1 accounting erratum without changing frozen artifacts — **done**
   (`experiments/semantic-control-core-v1/{COMPRESSION-EVALUATION,SYNTHESIS}.md`);
2. one independent reconstruction from `ba8968c` with no V0/V1 exposure — **done**;
3. compare semantic-boundary convergence — **done**
   (`experiments/semantic-control-core-v1/INDEPENDENT-RECONSTRUCTION-COMPARISON.md`):
   `INDEPENDENT_SEMANTIC_RECONSTRUCTABILITY = SUBSTANTIALLY_CONVERGENT`;
4. **if substantially convergent, proceed directly to a bounded persistence /
   maintenance architecture prototype** — **this package**.

The distinctive remaining uncertainty is no longer "is this information useful?"
or "is it one agent's invention?" (both answered). It is:

> **How do we maintain this tiny semantic core cheaply and safely?**

## Starting-state guard

| Fact | Value |
|---|---|
| Canonical `main` | `ba8968ca1a12caa90ce7beb0ee5fd2dfac055f37` (unchanged since V0/V1 construction) |
| This branch | `research/semantic-control-core-persistence-v0`, branched from canonical `main` (not from PR #244 or #245) |
| V1 reference | branch `research/semantic-control-core-v1`, draft PR #245 |
| Independent reconstruction reference | `H:/GithubRepositories/smk-indep-recon-out/independent-semantic-control-representation.md` (agent B, 32 rows, zero V0/V1 exposure) |

## What this prototype does

- Merges V1's 22 rows + agent B's non-duplicate additions into one
  `SEMANTIC-CONTROL-MAP.md` (still one authoritative row per concern).
- Adds a **Derivation** classification to every row:
  `DERIVED-MECHANICAL` (a script could refresh it) · `JUDGMENT` (irreducible
  human/model call) · `MIXED`.
- Specifies a **cheap maintenance procedure**: how the `DERIVED-MECHANICAL`
  rows would be refreshed from existing repo machinery (no new infrastructure),
  and how the `JUDGMENT` rows are reviewed and on what trigger.
- Estimates the maintenance cost and names what would make persistence
  unsafe.

## Hard boundaries

- **No new infrastructure.** No database, graph store, daemon, watcher,
  invalidation system, query engine, Skill, or workflow. The "mechanical
  derivation" is a *sketch that reuses existing scripts*
  (`scripts/probe_relationships.py`, `diff`, CI-workflow inspection), not new code.
- **Nothing lands in `docs/` or canonical product docs.** The map lives under
  `experiments/`. `docs/semantic-control-map.md` is a *possible future
  location*, not created here.
- No product / runtime / validator / probe / contract / PHB / ADR / test change.
- `GOAL_A_MODIFIED=false`, `ISSUE_218_MODIFIED=false`, `ISSUE_226_EXECUTED=false`.
- No merge. Draft PR only. PR #244 and PR #245 untouched.
- Frozen V0 (`experiments/detailed-repository-architecture-v0/`) and frozen V1
  core (`experiments/semantic-control-core-v1/00-SCOPE.md`,
  `SEMANTIC-CONTROL-CORE.md`, `ON-DEMAND-PROJECTION-RECIPE.md`) are not edited.

## Files

| File | Role |
|---|---|
| `00-SCOPE.md` | this file |
| `SEMANTIC-CONTROL-MAP.md` | merged candidate map, one row per concern, with Derivation + Grade + Rate columns |
| `MAINTENANCE.md` | derived-vs-judgment split; cheap refresh procedure; review cadence; staleness triggers; safety conditions |
| `PERSISTENCE-EVALUATION.md` | does it reconcile · maintenance-cost estimate · what makes persistence unsafe · disposition |
| `FREEZE-MANIFEST.md` | represented SHA + SHA-256 of the frozen prototype files |

## Epistemic grades

`DEMONSTRATED` / `DERIVED` / `INTERPRETIVE` / `HYPOTHESIS` — unchanged from V0/V1.
Every load-bearing row carries one, plus a change-rate (`SLOW`/`MEDIUM`/`FAST`)
and now a `Derivation` class.
