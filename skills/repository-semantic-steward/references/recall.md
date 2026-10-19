# RECALL — Source-verified use during engineering

RECALL is lightweight by default. It does not decide whether a task is warranted.

1. Identify current repository SHA, task and expected decision. Ask which remembered constraints or rationale could materially change implementation.
2. Inspect available reviewed knowledge records and current indexed versions. Prefer existing Git-authored sources when an index is missing.
3. Query `knowledge-query search|explain|why|history` for the named capability, invariant, component, decision or incident. Use `impact` only as an explicitly declared-edge **candidate** view.
4. Open the cited original source and verify applicability at current SHA. Run `knowledge-audit` against historical index when drift may matter. History order is indexing order, not automatically Git ancestry.
5. Distinguish validated contemporaneous evidence, historically correct but now superseded rationale, contested interpretation and unknown coverage.
6. Give the active engineering agent the smallest useful evidence packet: decision, applicable claims, original source paths/revisions, supporting tests and explicit uncertainties.
7. If retrieval contradicts current code or current owner intent, preserve the disagreement and initiate RECONCILE only when it would change a consequential future action.

**Do not:** blindly trust retrieved text; load the whole graph into context; promote source documentation or generated observations into owner authority; block a local useful fix merely because indexing is absent.

**Exit:** A source-checked architectural context that helps the active responsibility, with honest NOT ASSESSED entries instead of false negative results.
