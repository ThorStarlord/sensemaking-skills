# Graph-mediated decision-context re-entry: strategic comparison rule

**Status:** source-reviewed normal-use engineering assessment; not an independent host trial
**Date:** 2026-11-01
**Target:** `ThorStarlord/sensemaking-skills`, baseline `main@2ea8d357af3c52b627f9344aff4e40275439b9af`
**Plan:** `docs/superpowers/plans/2026-10-30-graph-mediated-reasoning-evolution.md`, WP-1/WP-2/WP-3/WP-5
**Source access:** authenticated GitHub connector; no local checkout, installed host Skill, or executed semantic SQLite index was available for this assessment

## Decision and why this question matters

Can an agent opening the strategic-analysis Skill reconstruct *why strategic candidates must be compared at a consistent decision level* without knowing the original PR number?

The current guidance in `skills/strategic-repository-analysis/SKILL.md` (comparison procedure) says to name the product outcome and compare enabling capabilities, mechanisms, interventions and evidence activities **against** it rather than as rival futures. `references/strategic-exploration-funnel-v1.md` section 8 gives the five-level table; `references/goal-fitness-and-completion-v1.md` explains how candidate comparison levels differ from objective roles. [PR #680](https://github.com/ThorStarlord/sensemaking-skills/pull/680) chose this guidance rather than a required schema field, a second taxonomy or mandatory artifact labels. This is a delegated engineering choice, not a new owner-ratified product thesis. ADR 0034's breadth and adaptive-control decisions remain governing authority for their respective scope.

A returning editor starting from any one of these three source files should be able to discover its owning Skill and relevant governing and implementation rationale from reviewed knowledge, then inspect the original sources.

## Source-level retrieval assessment

The seven tracked `.sensemaking/knowledge/*.json` authored packs were inspected at the baseline revision. This is a bounded authored-record assessment, **not** a `knowledge-query` CLI run or a claim about all generated index records.

- No `component` claim's `owned_paths` selected any of the three strategic-analysis files.
- The broad `rule:runtime-owns-artifact-paths` convention matched `skills/**`, but it concerns output location, not comparison levels.
- No authored claim contained the specific comparison-level guidance, its rationale or the PR #680 alternative set.
- The existing `context_for` implementation starts from owning components and path-scoped rules, and expands relevant decisions via `decided_by` and alternatives via a linked decision's `references` relations. For these three source paths, the reviewed decision/alternative graph anchors were therefore missing.

**Scope of this negative finding:** the reviewed authored graph and the inspected source-path selection mechanism at the baseline revision. The guidance itself exists in the live Skill; a graph miss does **not** establish product absence. Original sources and PR #680 supplied the missing decision context.

## RELATIONAL_VERDICT — pre-correction

**Claim:** The reviewed graph already connects the strategic-analysis comparison-level decision and its rationale to the source files a returning editor would open. **Direction:** positive, scoped to reviewed records at the stated revision.

| Cell | Source-grounded assessment |
| --- | --- |
| Declared | The Skill and funnel declare the comparison-level guidance; ADR 0034 governs the broader product identity, not the specific PR #680 engineering choice |
| Implemented | The current Skill and references contain the rule and the five-level distinction; this is guidance, not an automatic runtime validator |
| Exercised | This session inspected source text and PR #680; fresh-agent Skill invocation and adherence are NOT_ASSESSED |
| Graph | The authored records lacked an owning component anchor and the specific decision/alternative relationships for these paths |

**Verdict: OVERSTATED** for the graph-reachability claim. It would also be overstated to say the product lacks the comparison-level rule. The correct response is a source-grounded knowledge repair, not a new ontology construct, query operation, automatic controller, or obligatory graph-lookup stage.

## Selected repair and rejected moves

1. Add a `component` with exact `owned_paths` for the strategic-analysis Skill and two relevant references.
2. Record PR #680's implemented comparison-level rule as an **observed** guidance fact, separately from its delegated design decision.
3. Link the owning component separately to its delegated PR #680 design decision and the governing ADR 0034 product decision without promoting PR #680 to Level-4 owner authority; retain the rejected schema alternative as a historical alternative.
4. Anchor source references so file-oriented context can expose the governing decision, design decision, alternative and implementation observation.

The more conservative choice (keep only PR text and use literal search) preserves the information but makes the file-first re-entry depend on knowing the earlier identifier. The more aggressive choice (introduce `decision-context` API or mandatory schema) adds runtime/contract complexity without a demonstrated consumer limitation. The authored-knowledge repair creates useful retained value at lower cost.

## Expected post-repair consumer behavior and limits

At a future exact committed revision with a rebuilt knowledge index:

- `context-for` on each of the three paths should select `component:strategic-repository-analysis-skill` via its exact `owned_paths`.
- `decided_by` relationships should make `decision:ontology-first-adaptive-sensemaking` and `decision:comparison-level-guidance` available in the decisions category.
- The delegated decision's `references` edge should expose `alternative:comparison-level-required-schema` through the existing bounded second hop.
- The component's `references` edge should expose `observation:comparison-level-guidance-in-source` as history.

This is a **source-derived expected retrieval path**, not an executed post-merge query. The current environment could not build an exact-revision index or invoke a fresh native coding-agent host. The next capable local/host session should run the actual `context-for` query on those source paths and report `NOT_ASSESSED` categories rather than implying complete context. Proposal-check, index-build, retrieval, unit tests and independent comparison remain `NOT_RUN` in this connector-only episode.

## Strategic consequence

The current PATH-1 direction and October 30 reasoning program remain valid. This case reveals a missing decision-to-source anchor rather than a fundamental retrieval-algorithm defect. WP-3 can continue through real questions; WP-4 prospective reasoning should reuse the recorded alternative and current strategy. No Level-3 reopening or Level-4 thesis change is warranted by this bounded observation.
