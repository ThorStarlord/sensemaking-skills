# Cognitive construction — source-linked goal-to-capability implementation routes (2026-11-17)

**Status:** Bounded construction and responsibility-selection record, not a new Level-3 strategy, Level-4 thesis, generic planner, accepted cognitive-performance claim, or independent evaluation. The decision note is authored **after** the initial code commit and is not a contemporaneous trace of private reasoning.

**Repository baseline:** [main@2e44d84ef9145ac593a405fd9991ea32c9dcd63c](https://github.com/ThorStarlord/sensemaking-skills/tree/2e44d84ef9145ac593a405fd9991ea32c9dcd63c), after merged divergent exploration [PR #894](https://github.com/ThorStarlord/sensemaking-skills/pull/894). **Delegation:** owner requested focused convergence, source inspection, bounded implementation, reconciliation and autonomous continuation. Ordinary repository construction authorized; Level-4, shared policy promotion and releases remain protected.

## 1. Focused convergence at the bounded responsibility boundary

The [divergent opportunity landscape](../explorations/2026-11-17-cognitive-construction-opportunity-landscape.md) already supplied meaningful breadth. No further breadth study or new product thesis is needed for selecting a first construction responsibility.

| Coherent direction | Product value if successful | Existing evidence/consumer | Why not the first whole program |
| --- | --- | --- | --- |
| **A2 + A4 + B1:** discover capability gaps from actual goal-to-consumer evidence; compare product consequences; continue across bounded increments | Later agents can distinguish intended goal service from source-linked implementation, select a valuable capability outcome and preserve it across work | `product-outline` already returns direct `serves_goal` declarations and optional goal-linked futures; existing `implemented_by` relationships and component-owned paths are retained but **not projected together at this consumer**. Warrant/Choice and construction continuity already describe comparison and longitudinal intent. | **Selected direction**, subject to grounded, reversible increments; no new automatic gap or value-ranking oracle. |
| **B2 + B3:** experience-informed method choice and downstream value learning | Actual SCL lessons change later methods and inform expected value | [Issue #860](https://github.com/ThorStarlord/sensemaking-skills/issues/860) construction-first amendment, [Issue #859](https://github.com/ThorStarlord/sensemaking-skills/issues/859), existing lesson search and AMS/RECALL interfaces | Existing functional construction already addresses much of this; qualification remains separate, and a duplicate learning engine would be redundant. Revisit at an authentic consequential method choice or consumer defect. |
| **C4:** simplify to capable host + useful source context and minimal learning | Lower ceremony and potentially better decision quality | The host remains semantic controller; direct `product-outline` and normal source inspection are available | A pure no-code/simplification path would leave the source-observed joined context gap in the existing consumer. Simplification remains a live design constraint on new work. |

**Selected near-term engineering responsibility:** Extend the existing read-only `product-outline` consumer to expose a bounded, directly authored **goal <- serves_goal - capability - implemented_by -> component** evidence route, with separate source references, identity, omission disclosure and explicit `NOT_ASSESSED` boundaries. Do not claim that the query diagnoses missing product functionality or selects the highest-value task.

**Why this is more valuable than a smaller graph-only edit:** It changes an actual retrieval contract that later coding agents can use to connect goals to owning implementation. The graph can already contain an `implemented_by` relation; without exposing its connection to goal service, a product-outline consumer must perform manual multi-query joins. [PR #892](https://github.com/ThorStarlord/sensemaking-skills/pull/892) remains a separate, unmerged goal-data change. This consumer enhancement works whether or not that graph proposal is accepted.

**Why this is less costly than a larger architecture:** No new Skill, controller, planner, query command, ontology, persistence store or learned reward model. Existing exact-SHA caching, indexed explicit relations, default workspace entrypoint and original-source verification remain controlling.

## 2. First bounded vertical and concrete consumer

**Pre-change observed seam (baseline source):**
- [knowledge_architecture.py](../../src/sensemaking_skills/semantic_architecture/knowledge_architecture.py) `product_outline` groups goals with direct `serves_goal` records, `constrained_by` relations and optional `candidate_opportunity_for` futures.
- The same snapshot may contain `capability - implemented_by -> component` and source-cited component `owned_paths`. [stewardship.json](../../.sensemaking/knowledge/stewardship.json) demonstrates the route from `goal:longterm-stewardship` through `cap:semantic-queries` to `component:knowledge-store`.
- The public [CLI](../../src/sensemaking_skills/semantic_cli.py) and [workspace query](../../src/sensemaking_skills/workspace_knowledge.py) already expose `product-outline` at an exact commit with no prepared database.

**Implemented consumer contract (source review at branch head):**
- Each visible goal exposes `implementation_routes`, `implementation_route_total`, `implementation_route_omitted` and `implementation_link_not_assessed`.
- Each route preserves both direct relation identities, separate relation/source citations, capability and component descriptions, component authority and authored owned paths.
- Global `total_counts` and `omitted_counts` disclose routes excluded by the independent bound; selected top-level envelopes carry visible route IDs but can truncate independently.
- `implementation_verified` is **false** for every route. No route or missing route proves implementation, current semantic applicability, goal completion, priority, or absence of hidden capability.
- The default query gains additive fields without changing the command surface; the optional `--include-candidates` path remains separate.

**Intended normal-use outcome:** When selecting a repository-wide cognitive-development responsibility, an agent can inspect a goal, its declared serving capabilities, source-linked implementing components and alternative futures in one existing consumer, then inspect real code/consumers and compare consequential value **under the existing Warrant/Choice method**. The response is evidence for active-agent judgment, not an automatic choice.

## 3. What this does not yet accomplish

This first increment is **a source-grounded integration layer**, not completion of A2 + A4 + B1. No automatic discovery of absent capabilities, no observed superior strategic choice, no autonomous opportunity evaluator, no cross-PR outcome preservation beyond existing continuity, and no cognitive adaptation demonstrated. In particular, more query data can still go unused.

The next construction responsibility is *conditional*, not automatic: inspect an authentic open-ended selection consuming these routes. If it exposes a specific missing behavioral capability, choose the strongest warranted improvement (possibly active-agent integration, capability gap recognition, value comparison or outcome-continuity repair). If source retrieval is sufficient and the remaining issue is agent judgment, do not build another query.

## 4. Implementation and evidence limits

- Implementation branch: `claude/goal-capability-routes-20261117`; changes are an additive implementation projection, CLI contract documentation and this bounded decision record.
- Original-source and code inspection plus precise GitHub diff inspection are the intended construction-phase verification. No local unit or synthetic evidence tests added or run under the current repository construction policy.
- Any hosted validation checks, merged state, and actual independent agent use must be reported from observed results, never inferred from the presence of fields.
- `STATUS.md`, ADRs, the original exploration, PRs #892/#893, and reviewed knowledge packs are unchanged. No new candidate knowledge claim is promoted by this document.

**Consequence and continuation:** A coherent goal-to-implementation source route is available in the existing consumer if the patch is integrated. Product value requires later genuine decisions to use it appropriately. Reassess the next bounded action from returned evidence and the revised product thesis rather than simply implement every item from the divergent landscape.
