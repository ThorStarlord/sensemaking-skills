# Semantic Architecture Phase 10 — Real Repository Episodes

**Status:** ACTIVE EXPERIMENT  
**Parent contract:** `../common-semantic-contract.md`  
**Profile:** `semantic_reasoning_profile` v1  
**Campaign admission:** unchanged / not registered

## Purpose

Phase 10 tests whether the common semantic envelope earns its coordination cost in real repository reasoning. It does not attempt to prove semantic truth or justify a universal schema.

The experiment uses three contrasting episodes:

1. `repo-sensemaker` — direct diagnosis of `ThorStarlord/Chess-Mentor-Engine`.
2. `output-reconciler` — currentness-aware reconciliation of `ThorStarlord/React_incremental_game_prototype` handoff claims against live PR state.
3. `pre-mortem` — cross-domain Product Management risk reasoning for `ThorStarlord/ViralFactory` production activation.

Each episode preserves one companion `semantic_reasoning_profile` plus a human-readable episode note. No target repository is modified.

## Questions

For each episode record:

- Did the profile expose a material currentness, evidence, inference, uncertainty, or limit that could change a decision?
- Which fields merely duplicate the domain artifact or source material?
- Would embedding the shared fields into the canonical domain artifact improve the workflow, or create schema/boilerplate cost?
- Is the companion profile useful to a fresh context without becoming a second semantic authority?
- Did any validator boundary encourage or require a false semantic claim?

## Decision outcomes

After all three episodes choose one bounded outcome:

- **A — keep companion:** the profile is useful primarily as a cross-artifact audit/reconstruction instrument.
- **B — selectively embed:** a smaller demonstrated subset belongs in multiple canonical analytical artifacts.
- **C — narrow/retire:** duplication and ceremony exceed the coordination value.

Do not assume B is maturity. A or C are valid outcomes.

## Decision rule

Prefer **B** only if at least two contrasting Phase 10 episodes show the same missing semantic field materially affects a decision *and* that field is not already adequately represented in each domain artifact.

Prefer **A** when the profile materially improves cross-artifact currentness/reconstruction while domain artifacts already carry adequate local semantics.

Prefer **C** when at least two episodes show mostly duplicate fields/boilerplate without a material omission caught.

Any outcome remains bounded to the observed episodes. None authorizes Campaign schema promotion, a Repository Semantic Map, or a central reasoning engine.

## Evidence surface

All repository-content reads are pinned to exact Git SHAs. Live PR metadata is recorded separately where an episode explicitly tests currentness beyond the pinned repository snapshot. Local-only Probe Engine metrics are unmeasured because these episodes use the authorized read-only GitHub connector surface.
