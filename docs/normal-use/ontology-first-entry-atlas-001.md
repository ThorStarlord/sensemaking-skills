# Ontology-First Entry — Authentic-Use Assessment (Atlas Midgard 001)

**Status:** normal-use evidence record for ADR 0034 plan PR 8. Single session, by the same agent that wrote the guidance and, earlier, the Atlas records it reuses. Not an independent trial.
**Date:** 2026-10-28
**Guidance under test:** `using-sensemaking` controller and references after #641–#646 (`main@ef88bdb`)
**Target:** `ThorStarlord/atlas-midgard` at `main@d3cd47d`, **read-only**. This plan grants no write authority in Atlas, so nothing below was persisted there.

## 1. What ran

Request, as the controller would receive it: *apply Sensemaking to Atlas Midgard; understanding and exploration only, no product changes* (plan Scenario 5 on a repository in the Scenario 2 state).

1. **Goal and authority.** Repository-level reasoning, read-only. A target receipt could not be written. That limitation is reported here, as `using-sensemaking` section 7 requires.
2. **Orient.** Retrieved the two Atlas knowledge files (21 claims, 24 relations from the 2026-10-28 application), its synthesis and strategic analysis, its receipts and `STATUS.md`. Currentness: the records describe `7589b45`; `main` adds only the merge, so they are current.
3. **Assess adequacy** (`ontology-first-entry-v1.md` section 2). Atlas has about 13 product systems. The reviewed records cover one, world continuity and consequence presentation, so they are **inadequate for a repository-level goal**. Bootstrap or deepening is warranted. This is not a restart, and the existing records were reused unchanged.
4. **Provisional bootstrap** (Steward BOOTSTRAP steps 1–9, read-only). Section 2 below holds the model; section 3 holds the coverage report.
5. **Breadth** (funnel section 4). Recalled the two retained `poss:` records and the three paths of the earlier analysis, then scanned within and across systems. Section 4 has the landscape.
6. **Possibility coverage assessment** (funnel section 4). Section 5.
7. **Stop.** Disposition and its reasons are in section 6. No product code, records or receipts in Atlas were changed.

## 2. Provisional semantic model (not persisted)

**Governing intent.** Atlas is a tactical isometric action RPG: "hardcore depth without the hardcore stress" (README, `docs/vision/`). Construction selection follows the canonical scale model (`docs/decisions/construction-scale-and-roadmap-model.md`):

- Four qualitative scales: A breadth, B depth, C continuity, D integration.
- Scales A and B are on HOLD; Scale D (Epoch V, integrated co-op) is the active frontier; Scale C is next.
- The owner's First Journey release cut is a bounded solo-first track.
- Construction precedes field testing.

**Systems and source owners** (system level only):

| System | Owner in source | Governing decisions |
| --- | --- | --- |
| Combat and encounters | `runtime/combatant.gd`, `ability_executor.gd`, `encounter_director.gd`, three Saga bosses | `docs/systems/core-systems.md` (Tactical Trinity) |
| Jobs and builds | `progression/job_*_catalog.gd`, `legacy_technique_catalog.gd`, `runtime/job_runtime.gd` | build-system identity, hero-job models |
| Itemization, crafting, economy | `progression/itemization_catalog.gd`, `persistent_item.gd` | itemization/economy, forging, loot cadence |
| Persistent progression | `progression/progression_service.gd`, `profile_store.gd`, `profile_migrator.gd`, `player_profile.gd` | STATUS "Persistence authority" |
| Companions | `progression/companion_*`, `world/companion_*_area.gd`, `runtime/companion_controller.gd` | companion identity, relationship, continuity models |
| Living Continuity, Hearth and regional network | `progression/regional_*`, `hearth_*`, `world/regional_*_area.gd`, restoration presenters | living-continuity-network, hearth models |
| World consequences (remembered places) | `progression/world_consequence_catalog.gd`, `world/world_consequence_site.gd` | **the only system with reviewed records** |
| Chronos (historical reactivation) | `runtime/chronos_session.gd`, `chronos_portal_area.gd` | context-reactivation authority |
| Ordinary life | `world/*_circuit.gd`, `ordinary_life_*` | Larkspur/Mossbell packages 16, 19 |
| Host-authoritative co-op | `runtime/coop_*`, `party_seat.gd` | production-platform-and-networking; packages 26–35 |
| Endgame Atlas | `runtime/endgame_atlas_session.gd`, `content/endgame_atlas_catalog.gd` | endgame-atlas-* decisions; Epoch VIII |
| First Journey shell | `world/first_journey_title.gd`, `prototype_journey_*` | first-finishable-prototype-cut |
| Telemetry and qualification | `runtime/telemetry_*`, `qualification_bootstrap.gd` | Package 8 (deferred field qualification) |

**Distinctions that must not be conflated** (declared in the cited decisions; key ones verified in source):

- Durable profile History versus derived presentation. World consequences are derived, as in the existing records.
- Chronos historical context versus Endgame Atlas corruption versus ordinary travel. These are mutually isolated (`endgame-atlas-presentation-grammar.md`, "Context integrity"; `endgame_atlas_session.gd` refuses to begin during Chronos).
- Host simulation authority versus client presentation (Epoch V exit condition).
- A shared companion chronicle unlocked by accumulated biography versus a relationship score (`companion_reflection_area.gd`).

## 3. Coverage report

- **Represented in reviewed records:** world consequence presentation only (component, decision, rule, verification, options, consequences).
- **Provisionally modelled here, system level only:** the 13 systems above, their owners and governing decisions.
- **Not assessed:**
  - combat balance and encounter design;
  - itemization and economy depth;
  - the co-op wire and transport internals;
  - telemetry semantics;
  - scene and asset inventory;
  - the full Endgame Atlas decision series (posts 28–32);
  - roadmap packages beyond their STATUS summaries.
- **Not persisted:** no write authority in Atlas, so a later session will not inherit this model unless it is recorded through Atlas's own review.

## 4. Possibility landscape

| Item | Kind | Status |
| --- | --- | --- |
| Remembered route places | possibility (`poss:remembered-route-places`) | restated; realized as derived presentation |
| Companions remark on remembered places | possibility (`poss:companions-remark-on-remembered-places`) | **revised**: the existing Shared Chronicle (`CompanionRelationshipCatalog`, reflections unlocked by shared History) is the natural composition point, not a new remarks system |
| Visible co-op (Epoch V exit) | construction path (earlier PATH-1) | restated |
| First Journey release gates | construction path (earlier PATH-3), external | restated |
| History-sourced Endgame contexts (corruptions that reflect what the player restored) | possibility, counterfactual, long horizon (Epoch VIII) | new, hypothetical |
| Ordinary-life routines changed by restoration | possibility (Scale C × ordinary life) | new, hypothetical |
| Second region (Scale A) | possibility | on HOLD by the scale model |
| Orphaned `larkspur_morning` / `larkspur_hunger` scenes | engineering cleanup | not a possibility (classified, not retained) |

**Cross-system consequence surfaced by breadth.** Endgame Atlas corruptions reload the Ruined Causeway and Silent Archive scenes (`endgame_atlas_catalog.gd`, `default_corruption_for_scene`). Since #84 those scenes carry `WorldConsequenceSite`s, and the sites hide only during Chronos (`world_consequence_site.gd`). So restoration markers are presented inside corruptions.

The Endgame grammar describes corruptions as "transformed versions of familiar places". Showing the markers is therefore defensible, but no analysis decided it: the earlier synthesis's consequence exploration never mapped Endgame Atlas. This is a design question for the next Atlas session or the owner, not a defect claim.

## 5. Possibility coverage assessment

- **Systems and user outcomes:** all 13 mapped at the system level. Depth was reached only where a candidate touched world continuity, companions, Chronos or Endgame.
- **Compositions:** examined for companions × world consequences, Endgame × world consequences, and ordinary life × restoration.
- **Recall:** both retained possibilities and all three earlier paths were recalled.
- **Counterfactuals:** History-sourced Endgame contexts, and the declined durable world-state authority (its reopening trigger is not met).
- **Ease-driven convergence:** not the cause here. The repository-wide direction turns on the owner's open scale reconciliation, not on any visible defect.
- **Unexamined:** listed in section 3. Could an excluded direction overturn the result? Not plausibly within Scales A and B, which the governing model holds. A combat or feel problem found by the pending human playthrough could.

## 6. Disposition

**OWNER_DECISION for the repository-wide direction.** It turns on the reconciliation Atlas already records as open (its session receipt Q-1): after the First Journey release, resume Epoch V (visible co-op) or reconcile toward Scale C. Breadth found no candidate that dissolves that choice. It did add two inputs to it:

1. The Scale C continuation is cheaper than recorded, because the companion step can compose the existing Shared Chronicle.
2. The Endgame consequence in section 4 should be decided before more remembered-place sites land in corruption-capable scenes.

No implementation was selected or warranted under this authority.

## 7. Evaluation against the plan's evidence kinds

| Evidence kind | Status | Basis |
| --- | --- | --- |
| Instruction contract implemented | **Yes** | #640–#646; hygiene, repo, docs-currentness and probe gates pass |
| Skill discoverability established | **No** | No installed host Skill was invoked; the guidance was read from the repository |
| Specialist composition observed | **Partly** | The Steward's bootstrap steps and the funnel's breadth and coverage steps were applied in one session through the in-session fallback, not native nested invocation |
| Ontology-first behavior observed | **Yes, same agent** | The adequacy judgment and provisional model came before any direction; no local repair was selected first |
| Decision usefulness observed | **Limited** | Two findings the earlier focused session missed (Shared Chronicle composition; the Endgame consequence). The direction itself did not change |
| Independent-session reuse observed | **No** | Same agent, with summarized memory of the earlier Atlas work |

**By scenario:**

- **Scenario 2 (incomplete ontology):** existing records reused, gaps identified, missing space explored; extension provisional only.
- **Scenario 5 (exploration-only):** observed; completed with no product change.
- **Scenario 4 (returning agent):** not separable from the agent's memory.
- **Scenarios 1, 3 and 6:** not run under the new guidance. Scenarios 3 and 6 had pre-ADR analogs in Atlas 001.

## 8. Limits and what would test it

- The agent that wrote the guidance applied it. That is the strongest bias here, and validation does not remove it.
- Read-only access meant the model and landscape live only in this record.
- **Next useful evidence:** a fresh session, with `using-sensemaking` installed and no prior context, applied to a repository with no `.sensemaking/` records (Scenario 1), and a later fresh session on Atlas that must use whatever earlier sessions retained (Scenario 4).
