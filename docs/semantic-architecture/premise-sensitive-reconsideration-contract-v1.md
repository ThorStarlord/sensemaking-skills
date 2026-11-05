# Premise-Sensitive Reconsideration — Read-Only Inquiry and Graph View Contract v1

**Status:** Conceptual/presentation contract for an *optional* consumer, not a new registered artifact, schema migration, graph truth engine, general-purpose planner, owner permission or mandatory inquiry stage. [Governing design](../superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md). Source-checked originals and current owner/ADR authority remain authoritative. No new claim kind or predicate is ratified by this file.

## Consumer problem and minimality decision

The current reviewed graph contains useful `decision`, `alternative`, `hypothesis`, `observation`, `opportunity`, `references`, `contradicts`, `derived_from` and similar records. Existing `explain`, `why`, `history`, `changes` and `context-for` can recover selected neighbors and source pointers. They do **not** establish that a relationship was *logically necessary* for a historic comparison, or that changing a source automatically overturns a strategic selection.

The first historical case (2026-10-23/24 `ASSUMPTION-1`, `PATH-1`) is already reconstructible from original source text. There is **no material, observed consumer failure** requiring an additional universal graph predicate or a permanent reviewed pack that copies the strategic artifact. Thus:
- **NO_NEW_SCHEMA / NO_NEW_REVIEWED_PACK** for this first slice.
- **NO_NEW_PREMISE_QUERY**, unless a later exact case demonstrates that existing operations plus source access fail at a recurrent *bounded retrieval* question; a projection built over existing `explain`/`impact` is sufficient for the visual consumer.
- **GO** for an explicitly scoped, read-only `GraphExplorationView v1` because the secondary viewer needs a bounded stable display envelope, source IDs and truncation indicators not provided by raw query output. It is a *presentation projection*, not reviewed semantic records or a new knowledge store.

Future opt-in `reasoning_premises` on a reviewed decision/alternative/hypothesis is only a **proposal**, with candidate fields `premise_id`, `role`, `evidence_ref`, `assessed_ref`. It cannot be accepted before an actual consumer question fails, an authored source supports the role, endpoints are validated and the existing schema-evolution authority/migration gate passes.

## Role distinctions for one *attributed, scoped assertion*

| Role | Meaning | May be inferred from generic `references`? |
| --- | --- | --- |
| `NECESSARY` | Specific earlier judgment's reason requires this premise within the stated frame; loss warrants reconsidering that **reason**, not automatic rejection of the chosen outcome. | **No** |
| `SUPPORTING` | Premise was used in the stated justification but other grounds could sustain the conclusion. | **No** |
| `DEFEATER` | Credible evidence or competing premise challenges that exact interpretation. | **No** |
| `CONTEXT_ONLY` | Navigation, provenance or background reference, no established argumentative dependence. | **Yes**, as conservative display role for plain link, or `UNKNOWN` when insufficient scope. |
| `UNKNOWN` | Source/author or applicability has not established a defensible classification. | Default when needed. |
| `SCENARIO_ONLY` | User-proposed counterfactual and not a historic/reviewed world relationship. | Never; browser-only overlay. |

An `ALL` or `ANY` premise dependency group is legal only when a source expressly establishes joint/alternative sufficiency. Otherwise `UNKNOWN`. There is no inferred transitive causal closure. A preference under criterion F does not become a global score.

### Three establishment classes

- `SOURCE_DECLARED`: a source or reviewed authored record establishes this **limited role** and the agent inspected the original; reviewed content still does not prove source truth.
- `AGENT_INFERRED`: attributable new interpretation of source content with cited grounds, counterevidence and explicit uncertainty; not silently persisted.
- `SCENARIO`: hypothetical user-edited overlay, never a current claim/ratification.

Machine-generated path containment and import syntax may be shown as `MECHANICAL` **only** for their stated syntax observation, not as a reviewed semantic dependency.

## `PremiseInquiryView v1` (documentary)

A concise agent answer may express:

- `repository`, `target_ref`, `assessed_ref`, `premise_id`, `focus_question`;
- `candidates[]` of `{target_id, original_source_ref, assessed_ref, relation_role, why_decision_relevant, supporting_evidence[], defeating_evidence[], still_valid, reconsideration}`;
- `gaps[]`, `omissions`, `truncated`, `semantic_truth_established:false`, `action_authorized:false`.

This is not a required JSON serialization or new registered artifact. If a fact is unavailable, say `NOT_ASSESSED`; never fill it to satisfy a form.

## `GraphExplorationView v1` (mechanical presentation only)

The secondary viewer consumes *one exact revision* of a known repository's indexed graph or an explicitly source-attributed, independently checked inquiry projection:

```json
{
  "view_version": 1,
  "repository": "owner/repository",
  "target_ref": "40-character-commit-SHA",
  "indexed_ref": "40-character-commit-SHA",
  "assessed_ref": null,
  "question": "Which assumptions merit reconsideration?",
  "focus_ref": "decision:example",
  "nodes": [
    {
      "id": "decision:example",
      "kind": "decision",
      "label": "Source-attributed statement",
      "epistemic_status": "declared",
      "authority_kind": "document",
      "establishment": "SOURCE_DECLARED",
      "source_ref": ".sensemaking/knowledge/example.json",
      "evidence_refs": ["file:docs/example.md"]
    }
  ],
  "edges": [],
  "coverage": {
    "omitted_nodes": 0,
    "omitted_edges": 0,
    "truncated": false,
    "unassessed": []
  },
  "semantic_truth_established": false,
  "action_authorized": false
}
```

**Fields and rules:** Stable original node IDs and relation IDs. An edge contains `id`, `subject`, `object`, original `predicate`, conservative `role`, `establishment`, `epistemic_status`, `source_ref`, `evidence_refs` and `scenario_only:false`. `SOURCE_DECLARED` here means **source-declared relationship**, not substantive dependency/necessity or source correctness. `indexed_ref` is not silently rewritten to today's HEAD; `assessed_ref` is present only when original analysis supplies it. If the source/query does not establish premise role, the view says `CONTEXT_ONLY` or `UNKNOWN`, never makes it up. Export never merges records from different repositories or indexed source revisions. A `truncated` source query remains truncated in view even if local caps have room.

The renderer is read-only. `scenarios[]` if present represent transient, explicitly hypothetical overlays; baseline `nodes[]` and `edges[]` never change in response. The copy-back text is a **new proposed agent question**, not a command or API action. A graph list/table alternative and an evidence inspector must provide complete content without relying on SVG/color.

## Projection inputs, limits and safe output

- Existing `knowledge-query --operation explain --subject ID --json` (one-hop neighborhood), `impact` (bounded explicit links) or other documented source query. A local CLI can call `query_knowledge` against the exact indexed revision and pass its result to a pure projection; original top-level `claims[]` and `relations[]` are unchanged.
- Proposed `build_graph_exploration_view(query: dict, *, question: str, focus_ref: str, max_nodes: int=80, max_edges: int=160) -> dict` validates repository/ref/IDs and selects bounded original claims/relations. No inferred neighbors, no programmatic semantic meaning, no guessed source path and no untrusted HTML.
- `target_ref` must be the exact indexed SHA. Any `assessed_ref` is a *historical assessed source* and must be separately identified; don't infer Git ancestry from index insertion order.
- If a query's claims or relations are truncated, propagate `truncated:true` and note unknown omitted counts. Only count omissions exactly from data actually available; never report fabricated total counts.
- Fail closed on malformed record identity, wrong repo/ref, unsafe output destination or invalid source handles. Preserve `semantic_truth_established:false` and `action_authorized:false`.
- The browser loads an embedded copy of this *explicitly exported* local view, no network, no auth, no file writes, no source reconciliation or host tool execution; scenario reset restores original baseline.
- All rendered source text is untrusted; safely encode JSON and escape HTML/script terminators; display via text-safe operations. A source pointer might be non-navigable; show it as text rather than crafting guessed URL.

## Concrete competence checks and gate decisions

1. Reconstruct `ASSUMPTION-1 REVISE`, `ASSUMPTION-2 CONFIRM` and `PATH-1 CONTINUE/REAFFIRM` from the dated source. No new graph edge required.
2. A plain `references` or `derived_from` relation never becomes `NECESSARY`; it remains a literal source link.
3. Source-only answer is still useful if there is no graph/CLI, and a graph miss is `NOT_ASSESSED`.
4. The exported view is a bounded mechanical projection with source IDs and omissions; *the source-only historical answer need not correspond to a current global graph node*.
5. A scenario cannot change owner authority or retroactively alter the original dated strategic report.
6. A newly proposed product goal is checked against the actual reviewed `poss:` corpus and explicitly assigned a novelty ceiling.

**Rationale:** This first consumer needs a *truthful view of existing relationships*, not a new inference engine or semantic ontology migration. Keep adding richness where it preserves an otherwise-lost source-based distinction and passes the normal gate; don't add concepts merely because the UI would draw a more impressive graph.
