# Normal use: graph re-entry and prospective-guidance source context (2026-11-01)

**Scope:** Sensemaking-Skills only; current source baseline `main@e0be46c614f36bcae23c15f5bff7484d1455904d`.
**Program:** October 30 graph-mediated reasoning plan, R1-R5 / WP-1 through WP-5.
**Claim ceiling:** Source-grounded engineering/knowledge work, not an independent agent trial, graph-completeness assessment or causal product-benefit result.

## R1: executed exact-commit graph consumer

PR [#696](https://github.com/ThorStarlord/sensemaking-skills/pull/696) merged an optional, narrowly path-triggered real Semantic CLI consumer. Its [GitHub Actions run 41323492572](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41323492572) passed on exact PR head `842511e932acfbb9c3344fc17f253b38b3790092`. It installed that checkout, ran `knowledge-proposal-check` across seven authored packs, built a source-pinned index outside the checkout and invoked `knowledge-query --operation context-for --subject PATH --repo .`.

The three strategic-analysis file paths returned `component:strategic-repository-analysis-skill`, `decision:comparison-level-guidance`, `decision:ontology-first-adaptive-sensemaking`, `alternative:comparison-level-required-schema` and `observation:comparison-level-guidance-in-source`. Their `contracts` category remained `NOT_ASSESSED` for those source paths. `src/sensemaking_skills/workflow_availability.py` returned `component:workflow-installation-availability` and `observation:installation-availability-not-graph-use`, while contracts, decisions and alternatives remained `NOT_ASSESSED` for that path. Each result was not truncated and reported `semantic_truth_established: false`, `action_authorized: false` and `agent_decision_benefit_established: false` in the job's authored log summary.

This verifies only the named consumers at the exact PR SHA, not every dependency or a host's application of the returned information.

## R2: genuine re-entry question

**Question:** An agent editing the existing optional prospective architecture-guidance reference or its synthesis template should be able to recover the owning Steward capability, governing ontology-first decision and architectural-synthesis contract from the source-file path, without knowing a previous PR or graph ID. Can the currently reviewed graph support that re-entry?

The original references [architecture exploration](../../skills/repository-semantic-steward/references/architecture-exploration.md) and [architectural synthesis template](../../skills/repository-semantic-steward/references/architectural-synthesis-template.md) already describe this capability. They explicitly make architecture exploration optional for a warranted choice, keep the active agent as controller, and keep an `architectural_synthesis` preference distinct from an authorized decision. [ADR 0034](../adr/0034-ontology-first-adaptive-sensemaking.md) governs this agent-native role.

The authored graph at the stated baseline contains `component:repository-semantic-steward-skill` with `decided_by -> decision:ontology-first-adaptive-sensemaking` and `exposes -> contract:architectural-synthesis`. However its `owned_paths` lists only the Steward's `SKILL.md` and `references/recall.md`, not either prospective source file. Inspection of `knowledge_architecture.context_for` shows that file ownership is selected from exact `owned_paths`, and linked decision and contract categories require an owning component or applicable rule. Hence the authored component-to-path route is absent for these two files at the baseline. **This is a source/graph inspection, not an executed baseline `context-for` miss**; a broad applicable rule or other context may still be returned.

## R3: relational assessment

**Claim:** The reviewed graph already makes the Steward's relevant owner, governing decision and synthesis contract reachable from each prospective reference by file-first query. Positive direction, scoped to reviewed authored knowledge at the baseline.

- **Declared:** The Steward source and ADR 0034 establish optional prospective synthesis and agent-owned control.
- **Implemented:** The two reference files and the synthesis artifact contract implement this guidance; the existing query selects exact file ownership and explicit edges.
- **Exercised:** PR #696 exercises the same query mechanism on four other files. There is no executed baseline or post-repair query for the two prospective files yet.
- **Graph:** Existing Steward decision/contract links are recorded, but the exact ownership anchors for the two source paths are missing from the authored pack.

**Verdict:** `OVERSTATED` for the full file-first reachability claim. This is not a missing product capability or an absence of the governing decision. No runtime or ontology change is warranted.

## R4: prospective alternatives and conditional consequences

The governing product outcome is improved future-agent understanding of real architectural choices. Three **mechanisms at the same comparison level** were considered:

1. **Leave only the source text and search fallback.** Lowest maintenance. A later editor could find the rationale manually but `context-for` cannot reach the existing owner/contract route from these paths.
2. **Add the two exact reference paths to the existing Steward component** (selected). This reuses an existing source owner, `decided_by` and `exposes`, adds no duplicated control layer and makes a later exact-revision retrieval possible.
3. **Create a new prospective Steward component or mandatory graph-context operation.** Would add duplicate ownership/consumer complexity without a demonstrated separate capability or retrieval implementation gap.

**Provisional preference:** option 2, contingent on the exact-commit query recognizing one owning Steward component and returning the existing ADR decision and synthesis contract. It is a bounded delegated engineering choice, not a Level-4 product decision or strategy reopening.

**Conditional consequences:** Narrow source anchoring may reduce a returning editor's search cost; it does not ensure host loading or application. Reusing a component means the query can return its other component-level context, so the agent must still inspect original sources and `NOT_ASSESSED` categories. More aggressive component splitting could make categories superficially precise while inventing unverified architecture. No causal reduction in agent effort is established by this session.

## R5: knowledge correction, consumer and stopping boundary

This change updates only the existing component's statement, evidence and exact `owned_paths` in `.sensemaking/knowledge/architecture.json`. The source-backed governing decision and contract already exist, so no new claim kind, relation predicate, second controller, standalone synthesis artifact or duplicate normative decision is added.

The same optional GitHub Actions consumer should be extended to the two prospective paths on this change, reusing its actual exact-SHA index and `context-for` path. Success establishes the file-to-component/decision/contract route at that head, **not** semantic completeness, independent use, or longitudinal agent benefit.

R6 fresh-host knowledge consumption and R7 independent comparison remain distinct evidence responsibilities. The cloud Chess-Mentor-Engine pair showed a narrow, unreplicated reuse signal, not general superiority. This connector/CI-based episode does not create a fresh autonomous agent, isolate participant credentials or observe its decision-making. Further independent qualification must use the existing safety and authorization boundaries.

**Decision for continuation:** Continue agent-native selective RECALL and source-driven knowledge enrichment (PATH-1). No new runtime graph injection or ontology schema is warranted by these findings. If the new exact-revision consumer passes, prioritize a later real coding-agent decision where the additional context could change an option, assumption or consequence, and reconcile only its demonstrated learning.
