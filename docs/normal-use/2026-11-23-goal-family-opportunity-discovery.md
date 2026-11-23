# Goal-family opportunity discovery (2026-11-23)

**Status:** normal-use discovery and construction record. **Source baseline:** `ccebb54d87215c7a45b40d683b767779b2f017d8`. **Construction:** one-hop goal-family candidate projection in `product-outline` and `possibility-ecology`, plus a reviewed realization update for `poss:assumption-aware-opportunity-ecology`. This is not independent later-agent use, comparative benefit or a claim that the possibility's value hypothesis is proven.

## 1. Starting observation

At `ccebb54d`, the top-level ratified goal exposed no direct candidate opportunities:

| Goal | Direct candidates | Subgoal candidates |
| --- | ---: | ---: |
| `goal:domain-general-cognitive-development` | 0 | — |
| `goal:compounding-product-knowledge` | 4 | — |
| `goal:longterm-stewardship` | 4 | — |

`product-outline --include-candidates` showed the top goal's six implementation routes, including two one-hop indirect routes, but `candidate_total: 0`. `possibility-ecology` for the same goal returned zero direct candidates. The two specialized subgoals each returned four candidates.

This was not evidence that the repository had no relevant possibilities. The records existed under the subgoals. The existing orientation consumer followed one explicit `serves_goal` hop for implementation routes but not for candidate opportunities, so an agent reading the ratified top-level goal could see an apparently empty opportunity landscape.

## 2. Local Warrant Dominance hypothesis

The recent sequence (#953–#956) produced useful local integrity and provenance repairs. Each was locally warranted. The pattern is consistent with **Local Warrant Dominance**: a readily demonstrable source-level defect can win selection because it is easier to justify and verify than a larger capability-development opportunity.

This episode does not establish that hypothesis as an AMS defect. It establishes a concrete discovery limitation and deliberately compares a local-repair continuation against a capability-building alternative. No current source defect was left unfixed at the starting revision.

## 3. Opportunity comparison

| Option | Value if successful | Why not selected |
| --- | --- | --- |
| Another local integrity repair | Bounded correctness | No current consequential defect was confirmed; lower product value than the visible discovery gap |
| Campaign schema extension for opportunity binding | Stronger structured continuity | Existing Campaign/strategy handoff already preserves mission and responsibility; a schema change was not demonstrated as necessary |
| Method-recognition/applicability mechanism | Better conditional method use | The 2026-11-22 review found no current source-level defect; the remaining limitation is recognition/adoption and needs authentic later-agent evidence |
| External application work | Application value | Outside this repository's construction scope |
| Goal-family opportunity discovery | Makes the ratified goal's candidate landscape visible and supports comparison across subgoals | Selected: concrete consumer gap, existing data/consumer, reversible, no ranking or selection engine |

The selected candidate was `poss:assumption-aware-opportunity-ecology`, a hypothetical product possibility already linked to `goal:compounding-product-knowledge`. It describes coherent families of interacting possible capabilities, shared premises and assumption-dependent futures. The top-level goal made that family invisible.

## 4. Construction

### Product outline

`product-outline --include-candidates` now adds `indirect_candidate_opportunities` to each goal. It follows exactly one explicit `serves_goal` link from a specialized goal to the broader goal, matching the existing one-hop indirect implementation-route rule. Direct candidate links are not repeated. Each indirect entry carries:

- the candidate's existing statement, authority, evidence, source and relation provenance;
- `via_goal_claim_id`, `via_goal_statement`, `via_goal_epistemic_status`, `via_goal_source_ref` and `via_goal_evidence_refs`;
- `via_goal_serves_goal_relation_id` and relation evidence;
- `via_goal_claim_ids` and `via_goal_relations` for multiple authored paths;
- `intermediate_goal_hops: 1`.

The goal also carries `indirect_candidate_total`, `indirect_candidate_omitted`, `indirect_candidate_link_not_assessed`, `family_candidate_total` and `family_candidate_link_not_assessed`. Direct candidate fields are unchanged.

### Possibility ecology

`possibility-ecology` for a goal now adds `descendant_goal_candidates` under the same one-hop rule. Direct candidates remain in `candidates`. Descendant entries carry `candidate_scope: descendant_goal`, `via_goals` with goal and relation provenance, and `intermediate_goal_hops: 1`. `descendant_candidate_total`, `descendant_candidate_omitted`, `family_candidate_total` and family omission flags disclose the bound.

`shared_links` now considers both direct and descendant visible candidates, and each link identifies the candidate's `candidate_scope`. This surfaces authored relationships across specialized-goal candidates. It remains an authored co-reference, not proof of a shared premise, complement, conflict, feasibility, priority or value.

Neither consumer ranks, selects or infers a goal hierarchy. Longer paths are `NOT_ASSESSED`. The existing flat direct view is preserved.

### Outcome reconciliation

`poss:assumption-aware-opportunity-ecology` was updated from `NOT_ASSESSED` to `PARTIALLY_IMPLEMENTED`. Its realization history preserves the previous assessment. It records that the one-hop family projection exists, while generation of new assumptions, comparison of conflicting alternatives and demonstrated value remain unimplemented. No new product-thesis or authority claim was made.

## 5. Before and after

| Observation | Before | After |
| --- | --- | --- |
| Top goal direct candidates | 0 | 0 (unchanged) |
| Top goal one-hop family candidates | not projected | 8 |
| Top goal implementation routes | 6, including 2 indirect | 6 (unchanged) |
| `goal:compounding-product-knowledge` candidates | 4 direct | 4 direct (unchanged) |
| `poss:assumption-aware-opportunity-ecology` realization | `NOT_ASSESSED` | `PARTIALLY_IMPLEMENTED` |
| Top-goal shared links | 0 | 10 authored links across descendant candidates |

The new view makes the top-level goal's candidate family visible without changing direct candidate semantics or the subgoal ecology. It exposes existing authored material; it does not generate new possibilities.

## 6. Remaining capability and next evidence

The selected possibility is only partially realized. The projection shows authored candidates, dimensions, realization states and shared links, but it does not:

- generate new candidate combinations or assumption-dependent futures;
- compare candidates by beneficiary outcome or construct a coherent path;
- replace the agent's applicability, value or selection judgment;
- establish independent agent use or comparative benefit.

The next warranted evidence is an authentic later agent using the goal-family view in a real consequential selection, recording which candidates it inspected, which relationships or realization states mattered, whether it selected or rejected a path, and what outcome followed. No automatic selector or ranking engine is warranted by this episode.

## 7. Evidence ceiling

| Level | Status |
| --- | --- |
| Source-grounded discovery gap | Observed at `ccebb54d` |
| Functional goal-family projection | Observed through the real CLI |
| Direct-candidate and subgoal behavior preserved | Observed |
| Possibility realization update | Authored review, not value proof |
| Agent use of the new view | Not observed |
| Decision influence, independent reuse, comparative benefit or longitudinal development | Not established |

Local unit/synthetic tests were `NOT_RUN` under the construction policy; hosted CI remains the comprehensive safety net.
