# Cross-episode learning synthesis: explicit source anchors for useful historical context

**Date:** 2026-11-02. **Repository baseline:** `main@b497ad7e0195cfb7d68dd551ec58ec43b5ea538f`. **Scope:** Sensemaking-skills historical `context-for` reachability only. **Evidence:** source-reviewed PR histories, current query implementation, current authored graph, exact-head CI where available; not a fresh independent coding-agent learning episode.

## Why compare these cases?

The current owner-directed longitudinal learning objective asks whether an agent encountering an important engineering file can recover earlier lessons or rationale without knowing the original PR, conversation or claim ID. Several earlier bounded repairs touched the same underlying *source-to-context reachability* question, although their exact missing links differed.

| Historical engineering episode | What source inspection found | What was changed | Actual result / limit |
| --- | --- | --- | --- |
| [PR #691](https://github.com/ThorStarlord/sensemaking-skills/pull/691), 2026-11-01 | Strategic-comparison Skill/reference files had no relevant owner/decision anchors in reviewed graph (`docs/normal-use/graph-decision-context-strategic-comparison-2026-11-01.md`) | Reviewed component, decision, alternative and evidence links | PR #696 later established source-pinned mechanical `context-for` retrieval, not fresh-agent use |
| [PR #697](https://github.com/ThorStarlord/sensemaking-skills/pull/697), 2026-11-01 | Steward prospective references lacked exact `owned_paths` although component decision and synthesis contract already existed (`docs/normal-use/graph-reentry-prospective-guidance-2026-11-01.md`) | Added two source ownership anchors | [Run 41323680926](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41323680926) passed; agent benefit unassessed |
| [PR #701](https://github.com/ThorStarlord/sensemaking-skills/pull/701), 2026-11-02 | New creative-discovery reference was not declared among its Skill component's exact owned paths; source guidance existed | Added the path, observed guidance and context consumer | [Run 41471339686](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41471339686) passed; independent creative effect unassessed |
| [PR #704](https://github.com/ThorStarlord/sensemaking-skills/pull/704), 2026-11-02 | Query-store source owner was known, but there was no explicit owner-to-lesson link to three existing historical lessons (`docs/normal-use/2026-11-02-longitudinal-lesson-reentry.md`) | Added three bounded `references` edges, extended real source-pinned query checks | [Run 41480135285](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41480135285) passed on exact PR head `c74c3e68c49b64d374600775688ba60bb4ac583f`; not a fresh agent's lesson use |

## Material commonality and distinct mechanisms

**Common semantic situation:** original source-backed engineering guidance or historical events existed while a relevant file-first `context-for` route was absent in the reviewed graph. `src/sensemaking_skills/semantic_architecture/knowledge_architecture.py` explicitly selects file ownership from `component.owned_paths` and follows only recorded `references`, `learned_from`, `contradicts`, `decided_by`, and specific other links; no lexical/source-neighbor inference supplies the missing relation.

**Different defects:** PR #691 required an actual component plus decisions/alternatives; #697/#701 needed exact path ownership; #704 needed a history relation to an existing owner. These are not interchangeable. Missing historical `lesson` entries in a bounded context do not imply absence of a historical incident, incorrect CLI implementation, or an obligation to add an unbounded amount of graph material.

**Historical counterexample:** PR #696's original exact-head context consumer successfully found already reviewed owner and governing links on its tested paths. The issue is **selective authored-graph coverage**, not that file-first retrieval is generally broken. Source-only reconstruction also remains legitimate and may be cheaper for some tasks.

## Reusable, deliberately local interpretation

Candidate lesson `lesson:source-anchored-context-reentry` states: when a consequential file-first historical/decision query appears to miss a source-backed relevant record, first inspect the actual owning component's exact paths and established relationships, then the original source. Prefer a bounded source/graph correction to a new query or ontology *only if* that is the demonstrated cause. The lesson is grounded in the present Sensemaking `context-for` semantics, not in all repositories or query engines.

Retain one local historical `incident` and one `lesson` in the existing stewardship pack, linked by `learned_from`. Make that lesson reachable from the source-level knowledge architecture and the Steward's RECALL guidance through explicit reviewed `references` where those exact files are already owned. Do not synthesize an automatic validator, mandatory graph stage, generic MemoryEngine, new cross-episode Skill, or strategic authorization.

## Counterevidence, unknowns, and applicability

- These episodes overlap in repository, contributors, engine, ontology, and source-owner workflow. They are **not** several independent cross-repository demonstrations of one causal learning mechanism.
- The repair of a missing source anchor can improve *mechanical* context retrieval, but may yield too much, stale, or irrelevant information. A later agent must source-check the history and can reject it.
- The existing graph may intentionally leave some categories `NOT_ASSESSED` because no relevant evidence was reviewed; adding links simply to remove a gap would be knowledge pollution.
- No observed host outcome shows that the agent took a different engineering action because these source links were present.
- Other query consumers, other host adapters and other software domains may have different retrieval semantics; generalization and cross-repository transfer remain unqualified.

## Qualification and later feedback

The existing Semantic Context Re-entry CI can check that a file-first query of `knowledge_architecture.py` and of Steward `recall.md` returns the new, appropriately scoped lesson and correct owning component. It proves representation and reachability only. A future genuinely independent coding agent should encounter an ordinary relevant engineering question, determine whether the local precedent applies, inspect counterevidence and sources, and record whether it changed its reasoning. If another context contradicts the lesson, preserve this case's historical observations and **revise the lesson rather than overwrite history**.

**Disposition:** bounded repository-local lesson candidate retained; no universal reusable doctrine promotion, no new learning infrastructure, independent applicability/effectiveness NOT_ASSESSED.
