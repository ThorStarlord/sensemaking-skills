# RECALL — Source-verified use during engineering

RECALL is lightweight by default. It does not decide whether a task is warranted.

1. Identify current repository SHA, task and expected decision. Ask which remembered constraints or rationale could materially change implementation.
2. Inspect available reviewed knowledge records and current indexed versions. Prefer existing Git-authored sources when an index is missing.
3. Retrieve narrowly. When a relevant claim ID is already known, use `explain` (or `why` for a decision) with that exact ID. Otherwise search with one short phrase likely to appear verbatim in a claim statement or ID, inspect returned IDs, then `explain` the relevant claims.

   `search` is case-insensitive **literal substring matching within one claim statement or ID**. It does not tokenize, rank, or interpret natural language. A long question or bag of terms can return no matches even when useful claims exist. If a short literal search misses, inspect the reviewed JSON records and their IDs rather than treating the miss as evidence that knowledge is absent. Use `impact` only as an explicitly declared-edge **candidate** view.
4. Open the cited original source and verify applicability at current SHA. Run `knowledge-audit` against historical index when drift may matter. History order is indexing order, not automatically Git ancestry.
5. Distinguish validated contemporaneous evidence, historically correct but now superseded rationale, contested interpretation and unknown coverage. Ask whether the retrieved sources cover the **specific engineering decision**, not merely whether their claims are correct within the modeled area. Name the smallest decision-relevant **NOT ASSESSED** area (for example, an alternative backend, an acceptance owner, or a dependency) and inspect its actual sources only when it could change the handoff.
6. When evidence appears to establish **BLOCKED**, **NO EXECUTION PATH**, or **NO DEFECT**, distinguish a missing particular dependency from absence of *all* authorized alternatives. Check the smallest relevant original architectural decision and owning implementation before passing on such a conclusion. Example from Auteur: missing direct-provider credentials do not alone rule out its documented host-agent-first handoff; the handoff's source existence does not prove the active host runtime can execute it. The active agent or `using-sensemaking` decides whether to inquire, act, or stop; Steward does not select a provider, authorize a model call, or become a second planner.
7. Give the active engineering agent the smallest useful evidence packet: decision, applicable claims, original source paths/revisions, supporting tests, alternative paths actually inspected and explicit uncertainties.
8. If retrieval contradicts current code or current owner intent, preserve the disagreement and initiate RECONCILE only when it would change a consequential future action.

**Do not:** blindly trust retrieved text; load the whole graph into context; promote source documentation or generated observations into owner authority; block a local useful fix merely because indexing is absent.

**Exit:** A source-checked architectural context that helps the active responsibility, with honest NOT ASSESSED entries instead of false negative results.
