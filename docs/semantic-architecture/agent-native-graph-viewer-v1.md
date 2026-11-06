# Agent-Native Graph Exploration and Secondary Local Viewer v1

**Status:** Initial executable read-only JSON/HTML graph projection and offline viewer merged via PR #761; agent-first premise-reconsideration guidance and source-only historical example via PRs #759–760. The actual coding-agent interaction is primary; this viewer is an **optional secondary local interface**. Section 6 records what has been exercised in a browser. This status does not imply general UI validation, independent later-agent creative benefit, or graph-based semantic inference.

**Owners of meaning:** [Semantic model](ontology.md), [source/epistemic contract](relations-and-epistemics.md), [Git-authored source and CLI](persistent-knowledge-cli.md), [premise interpretation contract](premise-sensitive-reconsideration-contract-v1.md), [reference cases](premise-sensitive-reconsideration-cases-v1.md), and the [agreed design](../superpowers/specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md).

## 1. What this adds—and what it cannot establish

The existing `sensemaking-skills semantic knowledge-query` returns explicit source-pinned graph relationships. `knowledge-view-export` turns **one** exact-revision `explain` or bounded `impact` neighborhood into an inspectable, bounded presentation view. `knowledge-view-render` turns a **source-attributed, separately reviewed view JSON** into the same offline HTML presentation without writing it into the semantic graph.

The HTML inspector supports:
- Selection of a source node **or explicit edge** with kind, claim/relationship role, epistemic class, source and evidence text;
- Bounded SVG relationship overview and a keyboard-operable full exported-node list; kind/establishment filters and omissions;
- Historical original-versus-current reference labels and attributed pairwise comparison text **only when supplied**;
- A temporary `HYPOTHETICAL / NOT COMMITTED` scenario for a selected record of kind `hypothesis` or `constraint`, or `assumption` or `premise` in a curated view (see section 5);
- User-triggered **copy-ready agent question** with source identities, selected evidence and scenario limits. If clipboard permission fails (common for `file://` URLs), select and copy manually.

The browser does **not** fetch remote content, authenticate, update the Git-reviewed graph, edit strategy, run agents, change source evidence, or transmit a message. A changed assumption is **not** a proven change in any linked judgment. A plain `references` relationship is navigation, not a `NECESSARY` premise.

## 2. Direct indexed view (ordinary graph entries)

From a clean checkout with a known SHA, build the existing index **outside** the checkout:

```bash
REF="$(git rev-parse HEAD)"
sensemaking-skills semantic knowledge-build --repo . \
  --repository "ThorStarlord/sensemaking-skills" \
  --target-ref "$REF" --db /tmp/sensemaking-graph.sqlite --json
```

First discover a real target ID through the normal source-aware query, not by guessing:

```bash
sensemaking-skills semantic knowledge-query \
  --db /tmp/sensemaking-graph.sqlite \
  --repository "ThorStarlord/sensemaking-skills" \
  --target-ref "$REF" --operation search \
  --term "ontology-first" --json
```

Then export one source-pinned, read-only neighborhood for a **found** ID:

```bash
sensemaking-skills semantic knowledge-view-export \
  --db /tmp/sensemaking-graph.sqlite \
  --repository "ThorStarlord/sensemaking-skills" \
  --target-ref "$REF" \
  --focus-ref "decision:ontology-first-adaptive-sensemaking" \
  --question "What did the source actually establish?" \
  --depth 1 --max-nodes 80 --max-edges 160 \
  --format html --output /tmp/sensemaking-view.html --json
```

Open the resulting local HTML file in a browser. To get JSON instead, set `--format json` and a fresh `.json` output path. Use `--depth 2..4` only if a wider explicit-edge context materially answers the question. Results are bounded by the original query limit and local view caps. A `truncated` envelope may have **unknown** further omissions. Output files are create-only; use a new path rather than overwriting previous exports.

`knowledge-view-export` invokes the existing source-bound `query_knowledge` with `explain` at depth 1 or `impact` beyond depth 1. The projection does not re-read working-tree edits, fabricate transitive dependencies, or attach new authority. If `focus_ref` is absent because a larger query was truncated, reduce depth or inspect the source by ID; do not claim it is absent from the repository.

## 3. Historical source-only example (not a machine-indexed claim)

The dated `PATH-1` / `ASSUMPTION-1` example is a **source-interpreted view**. Those IDs are scoped to the original historical strategic artifact and are not automatically global graph claim IDs. Its view is kept as an explicitly attributed illustration, not in `.sensemaking/knowledge`.

To render that example from the repository:

```bash
sensemaking-skills semantic knowledge-view-render \
  --input docs/semantic-architecture/premise-sensitive-reconsideration-example-view-v1.json \
  --output /tmp/premise-reconsideration.html --json
```

The source-only input cites [2026-10-23 analysis](../../artifacts/history/2026-10-23-strategic-repository-analysis.md), assessed at `aa13f40`, and [2026-10-24 reconciliation](../../artifacts/history/2026-10-24-strategic-reconciliation.md), assessed at `b5fc389`. It illustrates `ASSUMPTION-1 REVISE`, `ASSUMPTION-2 CONFIRM` and `PATH-1 CONTINUE` / `REAFFIRM`. These attributed interpretation edges are **view-only associations**, not automatically generated executable predicates or a new owner decision. `ASSUMPTION-1` and `ASSUMPTION-2` are `hypothesis` records, so they can activate a scenario. The dated revision and confirmation records are `observation` records, so they cannot, although their IDs mention an assumption.

A future coding agent may construct a similarly attributed, source-bound `GraphExplorationView v1`, inspect original sources, and render it locally. The JSON structure is mechanically checked for identity, bounded arrays, source/evidence fields and permission/semantic-truth flags; it **does not** prove that the cited source entails the interpretation. Never label a fresh inference `SOURCE_DECLARED` if the original does not support it.

## 4. Primary agent experience and visual handoff

The intended workflow remains conversational:

1. Ask the coding agent to reconsider a particular source-backed premise, comparison or opportunity.
2. The agent checks the original source, associated revision, counterevidence and affected/unaffected judgments. It can answer without an index or viewer.
3. If visual inspection helps, export or curate a **source-qualified, bounded** view. The browser can inspect a relation and select a hypothetical premise inversion.
4. Click **Prepare follow-up** or **Copy for coding agent**. Paste the generated question into the original coding agent conversation; the copied message names original IDs and revisions, and asks the agent to verify—not automatically accept—the apparent connection.
5. The coding agent may source-check the selection, compare options or explain a no-change result. Durable knowledge updates require the normal reviewed process and applicable authority.

This intentionally omits a host-specific Codex/Archon browser API, direct workspace writes, a graph database migration and any requirement that the agent launch a browser for ordinary repository edits.

## 5. Original source and epistemic safety rules

- `source_ref` / `evidence_refs` are presented as **text**, not constructed remote URLs. Inspect original source at the relevant exact revision. A valid link is not proof of its content's correctness.
- On the indexed path, edge role is **CONTEXT_ONLY** for `references`/path containment and **UNKNOWN** for other predicate categories. No generic predicate is automatically converted into `NECESSARY`, `DEFEATER` or causal proof. A curated view may declare any supported role, and the renderer checks only that the role is supported, not that its source establishes it.
- Scenario eligibility comes only from the record's `kind`: `hypothesis` or `constraint`, plus `assumption` or `premise`, which only a curated view can use because they are not indexed kinds. ID wording and graph adjacency do not make a record eligible. Eligible means the record may be explored as absent, not that it is a premise of any linked judgment.
- Graph query records marked `SOURCE_DECLARED` are still attributable records, not automatically verified intent. Mechanically observed syntax is distinguishable from authored semantic relationships.
- `semantic_truth_established:false` and `action_authorized:false` are fixed in the exported envelope; renderer refuses input asserting either flag as true.
- A `HYPOTHETICAL` scenario never edits baseline nodes, source, comparisons or owner permissions. A suggestion returned to the agent is an invitation to investigate.
- Malicious source content is escaped in HTML's embedded JSON and placed into DOM through text-safe operations, never `innerHTML` or dynamic script loading.
- A missing graph edge, nonindexed original historical ID, stale source, unverified comparison, and truncated selection are reasons to inspect or report `NOT_ASSESSED`, not to manufacture a relationship.

## 6. Verification and evidence ceiling

The first PR's corrected commit passed Hosted Release Candidate Distribution and Semantic Context Re-entry. Under the repository's current `CLAUDE.md` owner construction rule, **no local unit/synthetic tests were added or run**. Independent later-agent consumption, comparative creative superiority and universal cross-repository benefit are **NOT_RUN / NOT_ASSESSED** unless separately verified and recorded with exact evidence. Hosted CI passing at one revision is evidence for its checked scope, not a global product-quality proof.

The premise-eligibility repair was exercised once, with the viewer asset from commit `9d2b37d` installed in an isolated environment. Five views were exported or rendered from it: four indexed at `96f7794`, and the curated example.

- **Observed in a Chromium-based browser pane, served from loopback:** the control activated, showed its banner and reset for an indexed `hypothesis`, an indexed `constraint` and the curated `ASSUMPTION-1`. The prepared follow-up named the selected premise and its hypothetical status. Records whose IDs merely mention an assumption stayed ineligible, and a selected `references` edge showed `CONTEXT_ONLY`. The server logged only page and favicon requests, and the index file hash was unchanged.
- **Not run:** `file://` pages, an actual clipboard write, keyboard-only operation, SVG node and edge clicks, other browsers, and a curated record of kind `assumption` or `premise` (no such view exists in this repository; that branch was checked by source reading only).

Selecting another record leaves the follow-up text unchanged until **Prepare follow-up** or **Copy for coding agent** regenerates it.

Source and packaging owners: `src/sensemaking_skills/semantic_architecture/knowledge_view.py`, `view_assets/graph_view.html`, `semantic_cli.py`, `pyproject.toml`, `MANIFEST.in`; see [implementation plan](../superpowers/plans/2026-11-05-agent-native-knowledge-graph-reasoning.md).
