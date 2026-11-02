# Normal use: creative prospective discovery from retained Sensemaking knowledge

**Date:** 2026-11-02. **Baseline:** `ThorStarlord/sensemaking-skills` at `main@bb77dac13fa4212d11f414176c9a37071dcc0a7f` (merged PR #699).
**Task:** User-delegated development of a knowledge graph that enables creative prospective reasoning and new product possibilities.
**Evidence:** This is a genuine source-reviewed same-agent design/construction episode through the authenticated GitHub connector. The bundled `using-sensemaking` and `strategic-sensemaking-loop` instructions were read. No independent fresh coding-agent host, native host Skill invocation, local CLI index, comparison, or autonomous generation engine was executed. Existing reviewed authored records were inspected directly rather than querying a new exact-commit SQLite index.

## Product outcome and source seeds

The desired user outcome is to discover coherent product futures that cannot be obtained simply by reading the most recent backlog item or by listing existing graph nodes. ADR 0034 (`docs/adr/0034-ontology-first-adaptive-sensemaking.md`) establishes understanding and prospective reasoning as the product outcome, with one agent-native semantic controller; ADR 0029 protects the automatic-planning boundary.

At this baseline the source-reviewed `.sensemaking/knowledge/possibilities.json` contains 18 product possibilities, plus capability, observation and hypothesis records. The directly inspected seeds were:

- `poss:cross-episode-possibility-synthesis`: recombine retained futures and strategic history into new, distinct product directions; guidance partly implemented, independent creative use unqualified.
- `poss:possibility-reconsideration-from-change`: reconsider an idea after a source/claim change; its claim-ID-addressable `revisit_when` mechanism remains unimplemented per its recorded assessment.
- `poss:repository-local-prospective-decision-memory`: retain architecture options, consequences and preferences for later sessions in a target repository; some same-session use, independent reuse not shown.
- `cap:breadth-exploration-guidance` and the existing Strategic Exploration Funnel: source-grounded, counterfactual breadth and prior possibility recall.

These seeds were compared with `docs/idea-library.md`, `docs/semantic-architecture/product-possibility-ontology.md`, `docs/semantic-architecture/prospective-reasoning-ontology.md`, `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`, `skills/repository-semantic-steward/references/architecture-exploration.md`, and the new optional creative-discovery reference. Source review establishes the documents and authored claims, **not** that a hosted agent has applied their guidance.

## Generative transformation and novelty check

| Candidate | Generative move | Closest existing record | Assessment |
| --- | --- | --- | --- |
| Source-grounded creative possibility discovery | Recombination and breadth | `poss:cross-episode-possibility-synthesis` and `poss:strategic-exploration-funnel` | **REVISED/EXTENDED GUIDANCE**, not a new `poss:`; PR #699 makes a missing capability-vs-architecture novelty distinction explicit |
| Assumption-aware opportunity ecology | Recombine cross-episode synthesis, changed-premise reconsideration and prospective memory | The three source seeds above | **NEW hypothetical product outcome**: agent helps people understand *families of interacting future capabilities and their assumption-dependent alternatives* for one user outcome, not merely synthesize an isolated new idea, reopen one deferred idea, or preserve one architecture decision |
| Automatic graph-ranked possibility backlog | Deterministic candidate selection | `poss:ranked-possibility-backlog`, `poss:automatic-strategic-planner` | **RESTATED / DECLINED**: existing rejected approach; no new ID or changed owner decision |
| Counterfactual architecture studio as a separate product capability | Assumption inversion | Existing architecture-exploration and `arch:` synthesis | **NOT_ASSESSED as independently novel** at this scope; keep as an optional exploration mode, not a new authored possibility |

**Novelty boundary of the new candidate:** an *opportunity ecology* answers how several product futures complement, conflict or depend on shared premises, and what emergent families of user outcomes might result. It is not a static concept map, graph ranking, or temporal change notification. The envisioned experience is relational and outcome-oriented; whether that outcome adds enough value beyond existing agent-native synthesis remains a hypothesis. The representation is deliberately a `poss:` opportunity claim, not a new graph engine, a new schema or a selected feature.

## Prospective architectural options for the new candidate

**Option A (provisionally preferred): Agent-native relational discovery.** The active agent selectively recalls relevant `poss:`/`arch:`/`conseq:` records, inspects source references and shared assumptions, explores grounded and counterfactual combinations, and reports linked families of possible futures using the existing synthesis/report and optional reviewed knowledge records. No new runtime; low reversibility cost and consistent with ADR 0034.

**Option B (retained alternative): Read-only graph-assistance for opportunity neighborhoods.** Only if actual cases demonstrate that existing `search`/`explain`/`context-for` cannot retrieve needed shared-premise or multi-option neighborhoods, consider a bounded deterministic candidate-view operation. It would return explicit source-pinned links, limits and unknowns, never candidate rankings or semantic decisions. No present consumer defect justifies building it now.

**Option C (declined): Automatically rank connected ideas and dispatch the top result.** This is the earlier rejected ranked-backlog/automatic-planner thesis; graph degree and adjacency do not establish product value or grant authority. Would require a real Level-4 review if pursued.

No new `arch:` records are authored for these implementation mechanisms because this case does not select a structural realization or establish a consumer need beyond current documented architecture; their comparison is retained here, and the provisional preference is not authority.

## Conditional consequences and challenge

| If... | Then possibly... | Constraint / rebuttal |
| --- | --- | --- |
| A later agent applies the new discovery lens to reviewed records | It could reveal useful clusters of future capabilities instead of reproducing a list of ideas | No independent hosted application or comparative novelty evidence yet |
| The agent identifies a genuinely shared premise | It might discover two futures that should be explored together | Shared citations or graph adjacency alone do not establish a logical or architectural dependency |
| An earlier rejection premise changes | A cluster of related possibilities might become worth reconsidering | `revisit_when` is not yet a claim-ID matched automatic trigger; reconsideration remains agent judgment |
| Every possible edge is treated as an idea | A flood of shallow candidates could obscure meaningful product outcomes | Start with a desired user outcome, use optional transformations, stop when alternatives are cosmetic |

Compared with a documentation-only, no-idea-retention approach, keeping this one hypothetical possibility and its clear differentiator gives a future agent a useful challenge to accept, modify or reject. Compared with a new executable generator, the agent-native approach retains useful construction value and lower implementation burden without claiming unobserved benefits.

## Authored-memory reconciliation

Retain `poss:assumption-aware-opportunity-ecology` as an exploratory, hypothetical `opportunity` with this report as origin. Link it through hypothetical `derived_from` relations to cross-episode synthesis and change reconsideration, a conceptual `references` relation to prospective decision memory, and existing `cap:possibility-records` as a genuine prerequisite. This is **knowledge about a possible future**, not a runtime implementation or an owner-selected Strategic Frontier.

No other generated possibility is promoted to a separate `poss:`. No new ontology kind/predicate/query, automatic planner, synthetic test, or target-repository work is warranted by the examined evidence.

## What is and is not established

**Established:** source-grounded possibility retrieval by direct authored-file inspection; meaningful distinction among restated, new and unassessed creative ideas; an attributable prospective comparison; an authorized Git knowledge/documentation change. **Not established:** mechanical exact-revision retrieval of the new record (until hosted validation/reindex), independent host consumption, effectiveness of opportunity-ecology guidance, comparative creative superiority, graph completeness or realization of the hypothetical future. Local unit/synthetic tests are `NOT_RUN` under the current `CLAUDE.md` construction exception.

**Continuation:** The current existing R6/R7/S5 fresh-agent and comparison responsibilities remain separate. A future genuine agent should address a naturally open product question, recover the stored premise/alternative lineage without being given its specific IDs, verify sources, and report whether it made a materially different creative proposal. If no isolated executor is available, continue independent warranted repository construction rather than relabeling this source review as a hosted experiment.
