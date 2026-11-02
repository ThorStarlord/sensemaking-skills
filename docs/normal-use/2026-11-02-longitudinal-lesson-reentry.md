# Normal use: source-file re-entry to historical engineering lessons

**Date:** 2026-11-02. **Target:** `ThorStarlord/sensemaking-skills`. **Source baseline:** `main@d0dfb21556bb306c84303bfd8d36843dabcdc182` before the graph change. **Evidence level:** source-inspected, same-agent, PR construction plus an exact-commit hosted CLI consumer proposed below. Not a second coding agent or a demonstration of learned performance.

## Real engineering question

While changing `src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py` or `knowledge_store.py`, which relevant lessons about result completeness, unreferenced changes and record/source drift should an engineer consider? Can an agent starting with the **source path** rather than a historical lesson ID recover them through the normal `context-for` consumer?

Existing reviewed `component:knowledge-store` owns those two exact tracked source paths. Inspection of `src/sensemaking_skills/semantic_architecture/knowledge_architecture.py` shows `context_for` returns historical lessons only through an explicit `references`, `learned_from` or `contradicts` relation involving an owning component or applicable rule. The baseline steward pack has no `component:knowledge-store -> lesson` edges, although its authored lessons and historical incidents exist. **This was a source-inspected missing-link finding, not a recorded before-change CLI failure.** Absence of a link is neither evidence that a precedent never occurred nor evidence that every query behavior is defective.

## Source-verified historical scope

| Lesson | Existing historical source | Applicability and limit |
| --- | --- | --- |
| `lesson:query-completeness-is-evidence` | `docs/normal-use/semantic-stewardship-episode-a-2026-10-15.md` | Earlier bounded `history`/`changes` results failed to disclose omissions; current code must be inspected and an earlier repaired defect must not be assumed to recur |
| `lesson:uncited-change-is-coverage-gap` | `docs/normal-use/semantic-steward-workspace-impact-2026-10-21.md` | Changed files without reviewed citations require examination; the query does not mechanically establish the existence or absence of a semantic effect |
| `lesson:distinguish-provenance-content-and-meaning` | Same 2026-10-21 report and cited retrieval/store modules | Whole-pack fingerprint changes, individual authored fields and actual semantic revisions must be interpreted separately; the code cannot automatically judge meaning |

## Bounded construction

Added three declared `component:knowledge-store references lesson:*` relationships in existing `.sensemaking/knowledge/stewardship.json`, preserving the lesson claims and their historical `learned_from` edges. They connect source-owner relevance, not a normative obligation or universal causal principle. No new ontology, query implementation or capability-learning Skill is warranted.

Extended the existing `.github/workflows/semantic-context-reentry.yml` exact-head consumer, which already installs the commit, validates seven authored packs, builds an exact-commit SQLite index outside the checkout and executes real `knowledge-query --operation context-for` commands. For each named source file, the consumer now checks ownership by `component:knowledge-store` and that `context.history` returns the three lessons with no truncation, while source identity matches the queried commit and `semantic_truth_established` / `action_authorized` remain false.

**Evidence ceiling:** the workflow text asserts intended checks. Only an actually completed run on the PR SHA supports a `MECHANICAL_REENTRY_PASS` claim. A passing mechanical result would not show whether a later coding agent discovered a lesson without prompting, whether it applied or correctly rejected the lesson, or whether the change improved its engineering outcome.

## Applicability challenge

An engineer touching an exhaustive, unbounded query may reasonably reject the bounded-query-completeness lesson as inapplicable. An engineer observing a source file absent from reviewed citations may use the uncited-change lesson to reopen evidence inspection, but must not invent a dependency. A lesson's previous authority and source revision must be checked against the current code and applicable accepted decisions. This episode demonstrates a warranted **source-to-graph coverage repair**, not a general proof of the lesson's transfer across contexts.

## Next genuinely independent responsibility

A separate coding-agent session with the correct loaded Skill and current source should encounter a real query-/architecture-related question without receiving these lesson IDs as the answer, retrieve the relevant historical sources where useful, decide whether they apply, and produce a decision/outcome report with truthful authority and claim ceilings. If no separate executor exists, this remains `NOT_EXECUTED — INDEPENDENT EXECUTOR UNAVAILABLE`; no synthetic replay or same-conversation source review counts as longitudinal qualification.
