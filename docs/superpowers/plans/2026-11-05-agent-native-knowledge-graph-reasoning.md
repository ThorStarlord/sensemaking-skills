# Agent-Native Knowledge Graph Reasoning and Secondary Interactive View — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. **This plan is not implementation authorization.** Refresh the repository, real source and owner's current operating rules before execution.

**Goal:** Make the coding agent use source-grounded graph relationships to identify which prior judgments or opportunities deserve reconsideration after a premise changes, while providing an optional local interactive graph for transparent inspection, scenario exploration and agent-directed follow-up.

**Architecture:** Begin with a real historical premise-sensitive inquiry and the existing `knowledge-query` graph and original files. Add only the minimal bounded read-only graph projection and optional typed record role that a concrete consumer question demonstrates is missing. Reuse this source-pinned projection in a secondary, self-contained HTML view; the coding agent remains the sole semantic controller and primary conversation UI.

**Tech Stack:** Python >=3.11, `sensemaking_skills.semantic_architecture`, Git-reviewed `.sensemaking/knowledge/*.json` (authored schema 1/2), existing SQLite index, Click CLI, PyYAML/packaging as currently installed; optional bundled vanilla HTML/CSS/JS/SVG with no remote dependency or additional database.

**Spec:** [Agent-Native Knowledge Graph Reasoning — Design v1](../specs/2026-11-05-agent-native-knowledge-graph-reasoning-design.md).

**Design/plan baseline:** `ThorStarlord/sensemaking-skills@1f7d4edc432dae5b7526675217cc798adf4e425e`, 2026-11-05. The owner previously agreed **A (expressiveness) + B (agent reasoning) + C (secondary interactive graph)** with **coding-agent UI primary**. This PR is **planning only**; no new executable capability, test/qualification, schema authority, application or new owner/product thesis is implied.

## Global Constraints

- The [product/ADR 0034](../../adr/0034-ontology-first-adaptive-sensemaking.md) is ontology-grounded repository understanding and prospective reasoning. `using-sensemaking` remains the one public entrypoint and active agent the semantic controller.
- ADR 0029 protects the no automatic planner/router/ranking/Skill-selection/merge/release/publish boundary. A `BUILD` recommendation, inferred comparison, browser selection or graph relation does **not** authorize execution.
- ADR 0031 governs persistent reviewed knowledge; original Git/ADR/user sources remain authority; indexed graph and derived HTML are reproducible read-only projections.
- Preserve canonical `strategic_repository_analysis` v2, `strategic_reconciliation`, Strategic Continuity, `AssessmentRevisionAccount` and `ProductPossibility`/`arch:`/`conseq:` identity and actual source/assessed revisions.
- Mechanically checked representation != true source interpretation; source-ref validity != evidence supports claim; adjacency != necessity; graph path != causal entailment; omitted results != absence.
- New graph kind/predicate/schema extension requires the existing [schema-evolution procedure](../../../skills/repository-semantic-steward/references/schema-evolution.md): actual failed question, representation alternatives, typed endpoints, old-schema compatibility, migrations and owner/schema authority.
- No remote dependencies or new backend/UI framework in the initial viewer; no automatic write from HTML to JSON/SQLite/Git; scenarios and unpublished inferences live only in view/agent message.
- Safe presentation: UTF-8 file export with escaped untrusted content; **CLI stdout ASCII-only** (current Windows/cp1252 source policy); no external fetch, HTML injection or credential export. `--target-ref` is a 40-character indexed commit SHA.
- Target system's current source and owner intent remain source-checked. A current-view query must not silently merge incompatible versions; direct file reading is a valid `NOT_ASSESSED` fallback.
- **Current local construction exception:** [`CLAUDE.md`](../../../CLAUDE.md) ``Local verification scope`` directs **do not add or manually run local unit or synthetic evidence tests** for this repository's current construction PRs. Source/diff review and honest `NOT_RUN` apply; hosted CI/protection stays. This plan supplies exact **deferred test recipes** for execution only if that owner exception is lifted. Do not incorrectly mark deferred tests PASS. Real-source inspection, existing hosted validation and narrow manual end-to-end use are allowed under current policy.
- One bounded `claude/<topic>` branch/PR per meaningful increment, source-grounded PR decision note, prompt authorized merges after clean review as current policy permits; never knowingly bypass a material failure or protected permission. This planned sequence is a proposal, not an automatic backlog.

## Review Focus

The following five input classes and expected behaviors require explicit review in the owning tasks; use deferred test recipes only when the owner changes the local-test rule.

1. **Missing/stale/unindexed premise:** no source-backed dependency is invented; `NOT_ASSESSED`, original source reentry and explicit index/current SHA are visible. *Owner: Tasks 1, 4, 6; test `test_premise_context_missing_or_stale_ref`.*
2. **Merely adjacent premise / many unrelated neighbors:** never label it necessary or invalidate unrelated decisions; distinguish navigation, supporting, defeater and unknown. *Owner: Tasks 3–5; test `test_premise_context_does_not_infer_necessity_from_references`.*
3. **Contrary scenario or owner-reserved intent:** visually isolated `HYPOTHETICAL` branch, real authority untouched, copy prompt indicates no authorization. *Owner: Tasks 7–9; test `test_scenario_overlay_never_rewrites_baseline`.*
4. **Large or malicious authored statements:** bounded/truncated output; HTML payload inert (e.g., literal `<script>`), safe relative evidence pointers, keyboard alternative. *Owner: Tasks 6–8; tests `test_view_export_escapes_untrusted_labels` and `test_view_bounded_omissions`.*
5. **Cross-revision/namespace collision:** no mixing of repository identity, indexed source, historical assessed SHA, same-name record from another repository or false Git ancestry claim. *Owner: Tasks 4, 6, 7; test `test_view_does_not_mix_revisions_or_repositories`.*

---

## 0. Baseline, immutable decisions and smallest meaningful vertical slice

Before any code edit, the implementing agent must read `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `docs/product-strategy.md`, accepted ADRs 0029/0031/0034, `STATUS.md` and this spec. Do **not** reopen Level 3 merely because ontology work was discussed. Recheck current `main` and prior PR #754–757 source/doc output; ignore a changed SHA unless its content matters.

**Existing implementation owners to reuse:**

| Responsibility | Existing source |
| --- | --- |
| Reviewed kinds/relations, source/authority/epistemic validation | `src/sensemaking_skills/semantic_architecture/knowledge.py` |
| Git-authored source ingestion and exact HEAD source checks | `src/sensemaking_skills/semantic_architecture/knowledge_sources.py` |
| SQLite snapshots / declared link traversal / change and context queries | `src/sensemaking_skills/semantic_architecture/knowledge_store.py` |
| Filter/coverage/truncation and current-record helpers | `src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py` |
| File context, scoped rules, term and orientation | `src/sensemaking_skills/semantic_architecture/knowledge_architecture.py` |
| Existing Click command surfaces | `src/sensemaking_skills/semantic_cli.py` |
| Agent creative question/lens/novelty method | `skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md` |
| Conditional strategic/learning responsibility | `skills/strategic-repository-analysis/references/strategic-evolution-learning-v1.md` and `skills/using-sensemaking/references/learning-reconciliation-policy-v0.md` |
| Existing stored cases | `docs/semantic-architecture/strategic-evolution-learning-reference-cases-v1.md`, historical 2026-10-23/24 analysis/reconciliation, `docs/normal-use/2026-11-02-creative-prospective-discovery.md` |
| Deferred test owners if construction exception lifts | `tests/test_semantic_knowledge.py`, `tests/test_semantic_cli.py`, `tests/test_architecture_queries.py` and narrowly scoped new test modules |

**Bounded product demonstration:** The agent receives "Source reachability assumptions changed; what does that mean for PATH-1 and alternatives?" The right answer rechecks ``ASSUMPTION-1``, preserves ``ASSUMPTION-2`` and original strategic choice, distinguishes changed source/interpretation from changed governing purpose and may identify further *inquiry* without promoting a new selected strategy. The viewer shows the *small* source-qualified network behind that answer.

### Task 1: Source-pinned user question, negative cases and reference output

**Files:**
- Create: `docs/semantic-architecture/premise-sensitive-reconsideration-cases-v1.md`
- Reference only: `artifacts/history/2026-10-23-strategic-repository-analysis.md`, `artifacts/history/2026-10-24-strategic-reconciliation.md`, `docs/semantic-architecture/strategic-evolution-learning-reference-cases-v1.md`, `docs/normal-use/2026-11-02-creative-prospective-discovery.md`
- Deferred Test: `tests/test_semantic_premise_context.py`

**Interfaces:**
- Consumes: source artifacts with original IDs, actual analyzed revisions and original actor/conclusion.
- Produces: `CASE-P1` (positive revised assumption without strategy reversal), `CASE-N1` (adjacent but nondecisive), `CASE-N2` (unknown graph), `CASE-N3` (unchanged intent and real authority), `CASE-O1` (new *hypothetical* beneficiary outcome vs mechanism). Source pointers and exact expected distinctions, no fabricated event.

- [ ] Step 1: Read original A/B strategic sources and verify which ``ASSUMPTION-1``, ``ASSUMPTION-2``, ``PATH-1`` and ``PATH-2`` conclusions were actually authored at which inspected revisions; note anything not reconstructible from original source.
- [ ] Step 2: Write the five source-qualified cases with a minimal exemplar *agent answer*: affected premise, exact affected judgment, unaffected choice, competing interpretation, no-change/unknown and optional new question. Label any normative comparator **NOT HISTORICAL**.
- [ ] Step 3: Specify deferred tests: `test_premise_context_missing_or_stale_ref` and `test_premise_context_does_not_infer_necessity_from_references` against exact known inputs; tests must reject "graph miss => absence" and "changed premise => PATH-1 invalid".
- [ ] Step 4: Review all source links, revision identities and original choice scope. **STOP** rather than invent a historical owner ratification or new `poss:`. Source/diff inspection is current verification; local tests `NOT_RUN` under current exception.
- [ ] Step 5: Commit a small docs-only change and open an attributable PR; a reviewer can reject this case/expected answer without any schema or viewer change.

**Acceptance:** A new agent reading the cases can correctly distinguish a revised interpretation of a premise from reversal of a choice and can state what is **NOT_ASSESSED**.

### Task 2: Agent-native premise-sensitive inquiry guide with source-only fallback

**Files:**
- Create: `skills/strategic-repository-analysis/references/premise-sensitive-reconsideration-v1.md`
- Modify: `skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md` (single conditional pointer only)
- Modify: `skills/strategic-repository-analysis/references/strategic-evolution-learning-v1.md` (single conditional pointer only)
- Deferred Test: existing source-focused Skill reference/distribution checks; no new public Skill

**Interfaces:**
- Consumes: Task 1 source cases and existing `knowledge-query` `search/explain/why/history/changes/context-for` and source-only reading.
- Produces: optional guide for **question -> selective source neighborhood -> decisive premise/contrary source -> conditional reconsideration -> meaningful alternative/no change -> answer/re-entry**; no registered artifact and no invocation by a new runtime controller.

- [ ] Step 1: Document the activation trigger as a genuinely consequential assumption, comparison or strategic-learning question; skip routine coding and no-material-change work.
- [ ] Step 2: Describe the exact source-only route (original prior analysis/assumptions and newer source) and optional graph route (candidate links, omission/currentness check). Both reach equivalent evidence/authority ceilings; graph gaps are not negative existential evidence.
- [ ] Step 3: Add the "decisive, supporting, context-only, defeater, unknown" interpretation check with negative case from Task 1. For new possibilities, explicitly compare the closest `poss:`/`arch:` and distinguish new desired end vs mechanism.
- [ ] Step 4: Provide a compact answer format: question, prior source identity and assessed SHA, actual current source, supported delta, affected/unaffected judgments, counterevidence, hypothetical opportunity, authority/stop, optional graph.
- [ ] Step 5: Add only conditional links in the two existing reference files, not `using-sensemaking/SKILL.md` or a new public Skill. Verify relative paths remain within packaged `strategic-repository-analysis` Skill tree. Source/diff review; tests `NOT_RUN` per current policy.
- [ ] Step 6: Commit/PR and merge only within the owner's actual document-update authority.

**Acceptance:** The coding agent can perform the complete inquiry even without any index, browser, graph export, host API or new typed predicate.

### Task 3: Document the minimal representation/view contract and schema gate

**Files:**
- Create: `docs/semantic-architecture/premise-sensitive-reconsideration-contract-v1.md`
- Modify only if needed: `docs/semantic-architecture/relations-and-epistemics.md` (non-executable relation-role meanings, not a new predicate dictionary without gate)
- Reference: `skills/repository-semantic-steward/references/schema-evolution.md`, `src/sensemaking_skills/semantic_architecture/knowledge.py`

**Interfaces:**
- Consumes: Task 1 cases and Task 2 agent answer requirements.
- Produces: `PremiseInquiryView v1` and ``GraphExplorationView v1`` *presentation* contracts, explicit role/epistemic/provenance semantics and a written **GO / NO_GO** decision on whether current kinds/predicates/attributes can preserve the specific missing distinction. These are not registered artifact IDs and do not revise existing indexed snapshot schema.

- [ ] Step 1: Inventory existing `hypothesis`, `decision`, `alternative`, `references`, `requires_capability`, `contradicts` and `derived_from` support for the Task 1 case; inspect original IDs. Evaluate the exact question that fails without richer semantics.
- [ ] Step 2: Specify if/when an association is **NECESSARY**, **SUPPORTING**, **DEFEATER**, **CONTEXT_ONLY**, **UNKNOWN**, or **SCENARIO_ONLY**, and its actual source/actor/assessed revision/target. Do not make a generic `references` edge necessary by label.
- [ ] Step 3: Specify `PremiseInquiryView v1` fields: `repository`, `target_ref`, `premise_id`, `focus_question`, `candidates[]` (original target ID, declaration role, evidence, original/currents, reason, status, no automatic change), `gaps[]`, `omissions`, ``semantic_truth_established:false``, ``action_authorized:false``.
- [ ] Step 4: Specify `GraphExplorationView v1` fields: `view_version:1`, `repository`, `target_ref`, optional `indexed_ref`/`assessed_ref`, `question`, `focus_ref`, `nodes[]` (original IDs, kind, label, source refs, epistemic/authority/establishment), `edges[]` (original endpoints, explicit role/basis, source refs, scenario flag), `coverage`, `comparisons[]`/`scenarios[]` optional, false truth/authority flags. Make output stable/deterministic and bounded.
- [ ] Step 5: Write the **schema-extension decision** with 3 options: source-only documentary; existing kinds + validated optional metadata; new validated kind/predicate only with qualified failing consumer and owner authority. Keep decision `NO_NEW_SCHEMA` until real failure shows the second/third option is needed; do not create graph types for ease of diagramming.
- [ ] Step 6: Specify downstream consumer that motivates each new field and actual test/review criteria, including migration/backward-compatible old indexed records and absence handling. Commit as a documentation-only contract decision.

**Acceptance:** Another implementer can distinguish durable reviewed meaning, agent interpretation and scenario-only modifications, and can implement without inventing schema authority. A documentary-only `NO_GO` is a correct completion if no consumer gap exists.

### Task 4: Bounded read-only premise-neighborhood projection (conditional on real consumer gap)

**Files:**
- Create, **only if GO from Task 3**: `src/sensemaking_skills/semantic_architecture/premise_context.py`
- Modify: `src/sensemaking_skills/semantic_architecture/knowledge_store.py` (only one new `query_knowledge` operation)
- Modify: `src/sensemaking_skills/semantic_cli.py` (only `knowledge-query` Choice and strict input validation)
- Deferred Test: `tests/test_semantic_premise_context.py`; relevant existing `tests/test_semantic_knowledge.py`

**Interfaces:**
- Consumes: `premise_context(claims, relations, *, premise_id, limit)` as a pure function over indexed `dict` records from existing SQLite store; `premise_id` must exist in **exact** selected snapshot; never consult mutable working tree during query.
- Produces: `query_knowledge(db_path, *, repository, target_ref, operation="premise-context", subject=premise_id, limit=50) -> dict` with the established top-level query envelope + `premise_context` defined in Task 3. Original query shape/operations remain backward-compatible.

- [ ] Step 1: If Task 3 can answer the actual user question just as faithfully through existing queries/source read, record `NO_NEW_QUERY` and **skip this Task's code/files**. Do not create a "generic graph query" merely because available.
- [ ] Step 2 (if GO): Specify deferred `test_premise_context_does_not_infer_necessity_from_references`: a `references` edge may locate a judgment but `relation_role` must remain `CONTEXT_ONLY`/`UNKNOWN` absent source-qualified explicit role. Specify `test_premise_context_missing_or_stale_ref`: unknown indexed `premise_id` cannot silently fall back to current unindexed files.
- [ ] Step 3 (if GO): Implement `premise_context(claims: Mapping[str, dict], relations: Iterable[dict], *, premise_id: str, limit: int) -> dict` with exact endpoints, stable order, bounded truncation and explicit uncertainty. It must not infer transitive proof/automatic selection. Pure function remains importable without SQLite.
- [ ] Step 4 (if GO): Add the narrow `premise-context` branch to `query_knowledge` and CLI `knowledge-query --operation`; reuse existing subject/limit validation and return fixed `semantic_truth_established:false` and `action_authorized:false`.
- [ ] Step 5 (if GO): Specify deferred `test_view_does_not_mix_revisions_or_repositories` plus existing-query shape regressions. Only after exception lifted: run `pytest tests/test_semantic_premise_context.py tests/test_semantic_knowledge.py -q` and require PASS. Under current policy: do not add/run tests locally; source/diff check + existing hosted CI + honest `NOT_RUN`.
- [ ] Step 6 (if GO): Demonstrate a real exact-SHA source case that is improved *in retrieval precision* over `explain`, without claiming automatically correct semantic assessment; PR/merge through active owner process.

**Acceptance:** Returned candidates have explainable, source-bound reasons and gaps, not just breadth-first adjacency; unchanged existing commands work. **NO_GO** if existing operations already suffice.

### Task 5: Optional reviewed representation for genuinely decisive premise role

**Files:** **Create/change only if justified and authorized at Task 3.**
- Modify: `src/sensemaking_skills/semantic_architecture/knowledge.py` (existing authored schema-v2 attribute validation)
- Modify: `src/sensemaking_skills/semantic_architecture/knowledge_sources.py` *only if* current source parser cannot retain the validated attribute
- Create: `.sensemaking/knowledge/premise-sensitive-reconsideration.json` *only if* actual consumer needs reviewed durable source links not already recorded
- Deferred Tests: `tests/test_semantic_premise_context.py`; `tests/test_architecture_vocabulary_v2.py`

**Interfaces:**
- Consumes: existing `KnowledgeClaim`/`KnowledgeRelation`, original source IDs and `schema_version:2` parser. Proposed *optional*, opt-in existing-kind metadata only: `attributes["reasoning_premises"]` on a reviewed `decision`/`alternative`/`hypothesis` claim, list entries `{premise_id, role, evidence_ref, assessed_ref}`, where `role` is `necessary|supporting|defeater|context_only`. This is a **candidate shape subject to Task 3**, not automatically authorized new schema.
- Produces: source-supported explicit role only for the specific reviewed claim; no automatic truth, no legacy migration, no new graph predicate by default.

- [ ] Step 1: Prove a source/consumer case where plain `references` + original source/agent source-check cannot preserve a necessary/supporting distinction for later independent retrieval. If absent or owner/contract authority inadequate, record `NO_NEW_REVIEWED_PACK / NO_SCHEMA_CHANGE` and skip this entire task.
- [ ] Step 2 (if GO): Document why the optional `reasoning_premises` shape wins over prose/source-only or new predicate, strict relationship endpoint kinds, source attribution and original assessed revision. Explicit `UNSUPPORTED` when source claims necessity without evidence.
- [ ] Step 3 (if GO): Before code, specify deferred `test_schema_v1_snapshots_still_build` and `test_reasoning_premises_requires_source_and_known_endpoint` with exact invalid/valid shapes; ensure existing versionless/v1 authored records and SQLite store version remain unchanged.
- [ ] Step 4 (if GO): Update `validate_v2_attributes` and `validate_snapshot` with strict metadata validation/known IDs only for opted-in records; avoid checking unmodified legacy records as though new required fields exist.
- [ ] Step 5 (if GO): Add the minimal Git-authored source record with original A/B historical citations and no duplicated new owner decision, proposal check/reindex at exact commit and correct `NOT_ASSESSED` for unsourced roles.
- [ ] Step 6 (if GO): Check full old/new contract compatibility and hosted source reentry, PR separately. No new `claim kind`, `predicate`, `schema_version:3` or general graph inference unless the gate explicitly supports a different, separately authorized design.

**Acceptance:** Either a correctly source-qualified opt-in premise role is queryable without changing historical schemas, or a source-grounded `NO_GO` explains why the representation was intentionally not expanded. Metadata must never silently transform a navigation link into a causal assertion.

### Task 6: Source-qualified investigation response and feedback case

**Files:**
- Create: `docs/normal-use/2026-11-05-premise-sensitive-reconsideration-first-use.md` (actual results and error/qualification boundaries, date/suffix adjusted to real run)
- Modify only if material: `skills/strategic-repository-analysis/references/premise-sensitive-reconsideration-v1.md` (evidenced gaps)
- Deferred Test: `tests/test_semantic_premise_context.py`

**Interfaces:**
- Consumes: Task 1 source reference case, Task 2 agent guide, existing graph or Task 4 query if GO.
- Produces: one *genuine source-read* agent answer with exact cited predecessor/changed premise, unchanged decision, missed relationships, role of graph (retrieved vs agent-added), feasible follow-up and honest stopping conditions. Not a fresh independent agent or compared outcome.

- [ ] Step 1: Reconstruct the actual historical ``ASSUMPTION-1`` revision through the agent's source-first flow, using installed graph if available, otherwise original reviewed JSON and sources. Track where material source-only reading was still needed.
- [ ] Step 2: Attempt one **separate meaningful** new outcome/reframing question using existing product possibilities and show the closest existing `poss:`, why proposal is `RESTATED`/`REVISED`/`NEW`/`NOT_ASSESSED`; do not fabricate new historical `poss:`.
- [ ] Step 3: Review two negative controls: a relation merely navigational, and a real source change that does not change owner strategy. Record whether the agent correctly refused premature reversal or product promotion.
- [ ] Step 4: Compare the observed reading burden/coverage to direct original-source reading **qualitatively**; attribute graph vs retained knowledge vs prompt guidance. Do not claim comparative creative superiority without an actually comparable independent agent.
- [ ] Step 5: Record what the graph was missing/where the guide was misleading, whether it warrants Task 4/5 GO or NO_GO, and what can remain source-only. Publish normal-use note within authorized PR review.
- [ ] Step 6: Check the agent answer contains exact assessed SHA, current source SHA, status, counterevidence, no-change outcome and optional new hypothesis. This is a **meaningful product behavior review**, not a synthetic benchmark or independent-agent trial.

**Acceptance:** A convincing agent-facing result is available now, including justified **NO_CHANGE** and evidence of what was and was not materially retrieved by the graph.

### Task 7: Stable read-only view export shared by CLI and browser

**Files:**
- Create: `src/sensemaking_skills/semantic_architecture/knowledge_view.py`
- Modify: `src/sensemaking_skills/semantic_cli.py` (one optional explicit export command; do not modify existing registered artifact producer)
- Deferred Test: `tests/test_semantic_graph_view.py` and `tests/test_semantic_cli.py`

**Interfaces:**
- Consumes: `build_graph_exploration_view(query: dict, *, question: str, focus_ref: str, max_nodes: int=80, max_edges: int=160) -> dict`, where `query` is an existing source-bound `query_knowledge` result or Task 4 result if GO. Use only original IDs and explicit existing records.
- Produces: `GraphExplorationView v1` with `view_version`, `repository`, `target_ref`, `indexed_ref`/`assessed_ref` when known, `nodes[]`, `edges[]`, source scope, `coverage: {omitted_nodes, omitted_edges, truncated, unassessed}` and `semantic_truth_established:false/action_authorized:false`.
- CLI (proposed): `sensemaking-skills semantic knowledge-view-export --db DB --repository ID --target-ref SHA --focus-ref ID --output PATH --format json --json`; source-only inquiry may also export a separately checked source-bound view input. Do not invent a new auto-discovering repo identifier.

- [ ] Step 1: Specify deferred `test_view_bounded_omissions` (e.g. >80 node or >160 edge candidates -> exact omitted counts and `truncated:true`) and `test_view_does_not_mix_revisions_or_repositories` (exact repository/SHA preserved and mixed input rejected).
- [ ] Step 2: Implement pure `build_graph_exploration_view`, stable sorting/deduplication, known source/epistemic and plain recorded-edge role; missing links omitted with visible `NOT_ASSESSED`. No causal/semantic closure or inference from an ordinary `references` edge.
- [ ] Step 3: Add narrow `knowledge-view-export` Click command initially supporting ``--format json``. Output path is outside canonical reviewed knowledge and never treated as new source authority. Explicit guard against accidental same-root overwrite of tracked reviewed JSON/SQLite.
- [ ] Step 4: Distinguish **declared edge**, **agent interpretation** (only when explicitly provided and labeled with its source), **scenario-only** (unpersisted), **unknown**, and **mechanical observation**. Never set `RATIFIED` solely because a source file exists.
- [ ] Step 5: Ensure output includes original source refs and actual source/assessed revision not just current HEAD; don't present index insertion order as Git ancestry. Deferred regression command: `pytest tests/test_semantic_graph_view.py tests/test_semantic_cli.py -q` **only if** local-test policy later allows.
- [ ] Step 6: Source-review export from real Task 1 case with bounded source display. If viewer requires metadata not in the source, show unassessed instead of silently extending machine schema.
- [ ] Step 7: Open/merge separate PR with exact data example, acceptance bounds and package/source verification. **Do not** claim HTML UI already exists.

**Acceptance:** A deterministic compact JSON projection can support both coding-agent citation text and any later UI. It is read-only and source-pinned even without new graph predicates.

### Task 8: Local static interactive viewer, source inspector and accessibility

**Files:**
- Create: `src/sensemaking_skills/semantic_architecture/view_assets/graph_view.html` (self-contained HTML/CSS/JS; no external CDN)
- Create or extend: `src/sensemaking_skills/semantic_architecture/knowledge_view.py` with `render_graph_view_html(view: dict) -> str`
- Modify: `pyproject.toml` (packaging for `semantic_architecture/view_assets/graph_view.html` only if not already included)
- Modify: `src/sensemaking_skills/semantic_cli.py` (allow ``--format html`` in `knowledge-view-export`)
- Deferred Tests: `tests/test_semantic_graph_view.py` and distribution/package tests

**Interfaces:**
- Consumes: Task 7 `GraphExplorationView v1`; no live backend/index/credential access inside browser.
- Produces: offline single-file HTML view with source-specific labels, node-kind/epistemic status/edge role, keyboard navigable companion list, a provenance inspector, focus filtering and visibly omitted/unassessed items. The original source metadata is unchanged.

- [ ] Step 1: Specify deferred `test_view_export_escapes_untrusted_labels`: content including `<script>`, quotation marks, Unicode separators and malicious URI-like evidence remains inert text; no executable injection, no remote fetch, no untrusted `innerHTML`.
- [ ] Step 2: Create a bounded deterministic left-to-right SVG relationship layout by role (premise/judgment/alternatives/evidence) or use compact list when graph density exceeds bound; preserve all surviving source IDs. Avoid an unneeded force simulation/library.
- [ ] Step 3: Add keyboard-focusable node/list selection and clear textual legend for `SOURCE_DECLARED`, `AGENT_INFERRED`, `SCENARIO`, `UNKNOWN`; do not rely on colors alone. Each selected item shows exact source/revision, kind, status, authority and role.
- [ ] Step 4: Implement `render_graph_view_html(view: dict) -> str` with safely embedded JSON; avoid HTML/script-end injection via escaped `<`, `>`, `&`. Only explicitly selected/reviewed source references are exposed. For large data show truncation, not silent disappearance.
- [ ] Step 5: Add explicit HTML export; verify output can be opened from `file://` without a development server or network. Check HTML asset inclusion in actual wheel source path, not just checkout-local success.
- [ ] Step 6: Manually inspect the real Task 1 case in browser if available (mouse, keyboard, narrower viewport, no JS fallback). If browser unavailable, report `NOT_RUN` rather than claim visual/keyboard qualification.
- [ ] Step 7: Specify deferred no-injection, packaging and deterministic-serialization tests; local tests remain `NOT_RUN` in current construction exception. PR/diff review with exact host/browser evidence ceiling.

**Acceptance:** The secondary UI gives a useful inspectable picture of **one** real inquiry, with no source mutation and no external frontend dependency. This is not a new primary app.

### Task 9: Hypothetical scenario overlay and "Ask coding agent" handoff

**Files:**
- Modify: `src/sensemaking_skills/semantic_architecture/view_assets/graph_view.html`
- Extend if needed: `src/sensemaking_skills/semantic_architecture/knowledge_view.py` (deterministic copy-context payload; no server)
- Deferred Test: `tests/test_semantic_graph_view.py`

**Interfaces:**
- Consumes: selected baseline node/edge, viewer original source identity, explicit user scenario changes and optional question text.
- Produces: read-only `ScenarioOverlay` **client state**, plus copy-ready Markdown instruction: question, selected original IDs, indexed/assessed refs, temporary counterfactual, known gaps and "do not treat scenario as owner ratification". Copy is user-triggered; no automatic agent API execution.

- [ ] Step 1: Define one scenario operation: mark one sourced **premise** as counterfactually absent or alternate, without editing baseline truth/authority/edges. Visible banner `HYPOTHETICAL — NOT COMMITTED` persists while the scenario view is active.
- [ ] Step 2: Show scenario-associated "candidate impacted" nodes only when the source explicitly qualifies relevance; otherwise show a *question to investigate*, not a simulated proved strategy reversal.
- [ ] Step 3: Add "Ask agent" user-action copy containing original view/ref, selected IDs, scenario text and `NOT_ASSESSED`/truncation flags. If the browser clipboard API is unavailable, provide selectable text for manual copy.
- [ ] Step 4: Add "Reset scenario" that restores **exact baseline view** and removes any scenario-only styling/annotations. Do not modify index files, graph source JSON, private filesystem, external apps or owner policy.
- [ ] Step 5: Specify deferred `test_scenario_overlay_never_rewrites_baseline` and `test_selection_handoff_includes_source_identity_and_limits`. Source/JS review for no hidden navigation, fetch, publication or automatic action.
- [ ] Step 6: Real manual inspect/copy one source-grounded Task 1 scenario and demonstrate the agent can continue from copied context **only if the current coding harness supports an honest foreground agent turn**; otherwise preserve manual copy-only fallback and report no host integration.
- [ ] Step 7: PR independently of backend scope expansion; do not invent direct Codex/Archon API integration.

**Acceptance:** Graph interaction is meaningful and reversible, while all actual reasoning/commit authority remains with the primary agent and user.

### Task 10: Conditional discoverability, documentation and distribution integration

**Files:**
- Modify: `docs/semantic-architecture/README.md` (what actually exists, no premature UI claim)
- Modify: `docs/semantic-architecture/persistent-knowledge-cli.md` (new `premise-context`/`knowledge-view-export` only if shipped)
- Modify: `skills/repository-semantic-steward/references/recall.md` or `skills/strategic-repository-analysis/references/premise-sensitive-reconsideration-v1.md` only where actual consumer needs a discoverable reference
- Modify only if warranted: `src/sensemaking_skills/semantic_architecture/__init__.py` for public exports
- Deferred Test: distribution/source-reference checks

**Interfaces:**
- Consumes: actual shipped Task 2, and conditional Tasks 4/5/7/8/9 output.
- Produces: documented entry examples showing agent-primary path, optional `knowledge-view-export`, source-only and no-index fallback, exact original and current SHA, and realistic claim ceiling.

- [ ] Step 1: Inspect actual primary entrypoint and reference-loading paths. Add a short optional trigger only where discoverability changes decision; avoid `using-sensemaking/SKILL.md` text churn if existing references suffice.
- [ ] Step 2: Document two user journeys: agent-only source-grounded reconsideration; same inquiry with explicit secondary viewer and copied scenario back to agent.
- [ ] Step 3: Verify source links resolve and packaged reference assets match the selected `entrypoint` profile. Use existing `setup.py` and `setup_skills.py`, avoid installer redesign or unrelated skill installs.
- [ ] Step 4: For any new CLI command verify documented exact flags match `--help` through real package source; record Windows ASCII stdout invariant. If not runnable in current host, state source-level verification only.
- [ ] Step 5: Check the view and guide can be omitted in a normal narrow code edit. This remains an optional capability, not a universal mandatory graph-phase.
- [ ] Step 6: Record legacy status/version implications and untouched strategic/thesis source; PR with bounded files and source-grounded note.

**Acceptance:** A coding agent can discover the appropriate guide and optional viewer without requiring a second public entrypoint, new service or manual schema configuration.

### Task 11: End-to-end reality check, authority and qualified closeout

**Files:**
- Modify if material capability changed: `STATUS.md` (one concise evidence-qualified capability note, PATH-1 unchanged unless separately justified)
- Modify: `docs/superpowers/plans/2026-11-05-agent-native-knowledge-graph-reasoning.md` (actual completion, NO_GO decisions, tests/CI truth)
- Create when actual work exists: `.sensemaking/receipts/<actual-session-ref>.session.yaml` (existing `sensemaking_session_receipt` schema, not new artifact)
- Reference: actual PRs, exact commits, CI runs and source case/explanation

**Interfaces:**
- Consumes: Task 1–10 specific PR heads and source/host observation; not planned tests treated as run.
- Produces: source-linked factual closure ``IMPLEMENTED``/`DOCUMENTARY_ONLY`/`PARTIAL`/`NO_GO`, preserved original history, action/authority boundary and independently unqualified agent benefit.

- [ ] Step 1: List every PR's exact files and source revision; compare diff against intended ownership. Confirm no secret source exports, no index/checkpoint commits or out-of-scope mutations.
- [ ] Step 2: Verify original A/B source and all negative-case interpretations; a reconsideration candidate must not be called a confirmed strategy reversal.
- [ ] Step 3: Check CLI query & view output on one real exact-commit source where runnable, look for limits, malformed/missing IDs and output encoding. File-level/source checks cannot be called a successful native-harness user workflow.
- [ ] Step 4: Inspect hosted CI results at the exact PR heads. Preserve `PASS`, `PENDING`, `FAILED`, `NOT_RUN` separately; repair material failures as bounded responsibilities rather than calling them acceptable.
- [ ] Step 5: Apply the current owner local verification exception exactly: do not add/run local unit/synthetic tests during construction; when exception changes, use each task's named deferred tests (and the real e2e path) to guard behavior before asserting test PASS.
- [ ] Step 6: Confirm the primary agent can answer a source-only version, the projection is optional and the graph UI can only propose a hypothetical branch/copy follow-up.
- [ ] Step 7: Reconcile `STATUS.md`, canonical strategy, authored knowledge and historical source only where actual meaningful facts changed. Preserve valid `NO_MODEL_CHANGE` and no new knowledge pack if unneeded.
- [ ] Step 8: Write one receipt with source identity, actual skill/host availability, responsibility, actual testing/CI, claim ceiling and stop/next warranted responsibility. Stop at owner/Level-4/external boundaries and report uncertainties.
- [ ] Step 9: Mark **GOAL_SATISFIED** only if the agreed agent-primary vertical slice and genuinely secondary inspectable view exist and are source/contract-verified at their claimed scope; otherwise report precisely partial and what is missing.

**Acceptance:** Accurate product status, no fantasy qualification and no unearned new authority. A design/plan/PR merge alone never satisfies this implementation task.

## 12. Independent later-agent usefulness — separate evidence question, not build gate

**Do not manufacture an empirical experiment solely because the new view and reasoning guide exist.** Independent benefit is not demonstrated by a same-agent sourced case, docs or hosted CI. When a genuine new agent with target-repo sources and comparable access is available, consider one ordinary source-grounded question whose consequences matter.

- [ ] **Conditional future assessment:** observe whether a fresh agent independently discovers a decisive prior premise and correctly differentiates prior rejection from changed applicability, with or without the graph. Preserve exact context, source access, host Skill loading and prompt differences.
- [ ] **Conditional comparison:** if an actual source-only alternative is available, assess separately the benefit of *retained original judgments*, *graph representation and access*, and *agent guide*. Novel-product-outcome claims must compare against closest prior `poss:` and named beneficiary/end.
- [ ] **Conditional result:** record faithful retrieval, useful application/rejection, actionable novelty, or no discernible advantage; keep scope and sample limitations explicit. Do not require universal transfer/cross-repo doctrine proof to close the bounded construction.

These are **future qualification possibilities**, not currently scheduled tests or implicit permission for an external agent runtime. Mark `NOT_ASSESSED` if no actual case occurs.

## 13. Proposed PR increments and dependencies

| Increment | Tasks and deliverable | Depends on | Gate/stop |
| --- | --- | --- | --- |
| **PR-A: agent answer and source meaning** | Tasks 1–3: historical source cases + portable premise inquiry guidance + view/typed schema gate. **Useful without any code.** | Refresh Task 0 sources | `NO_NEW_SCHEMA` and possible `NO_NEW_QUERY` are legitimate |
| **PR-B: minimal graph assistance** | Tasks 4–6: one bounded read-only premise context only if real consumer gap; optional validated reviewed metadata/record; authentic same-agent source-use note | PR-A | Do not add new kinds/predicates/pack if source-first route already adequate |
| **PR-C: graph view export** | Task 7: stable minimal source-pinned JSON view/CLI export, even if it consumes existing `explain` (no new query) | PR-A; PR-B only if new query exists | Viewer requires useful bounded actual-case data; don't export a fake semantic truth |
| **PR-D: secondary local viewer** | Tasks 8–9: HTML local offline view, source inspector, ephemeral scenario and copy-back to agent | PR-C | UI not a second controller or editor; no remote service |
| **PR-E: integration and qualified closure** | Tasks 10–11: docs/packaging/skill discoverability/status/receipt | Actual merged implementation | Report actual results and independent-value `NOT_ASSESSED` |

Tasks 1–3 and 7–9 each deliver reviewable value; Stage B may be `NO_GO`. The plan is not permission to continue into an unratified schema migration or deployment; an authorized implementing agent should stop and reconcile if a genuine owner/schema/host boundary appears.

## 14. Initial acceptance matrix (check against actual delivered behavior)

| Required user-observable capability | Source of expected meaning | Owning task(s) | Pass / acceptable alternative |
| --- | --- | --- | --- |
| Coding-agent-first answer to changed-premise strategic question | Historical A/B case and accepted design | 1–2, 6 | Source-grounded, revised/unchanged/unknown and counterevidence visible; source-only PASS if no index |
| Necessary vs merely supporting vs navigation distinction | Semantic A design, epistemic model | 3–5 | Source-qualified typed link or explicit `NOT_ASSESSED`, never fabricated necessary edge |
| Temporal/historical identity and original judgment retained | Strategic Continuity, LearningAccount | 1, 3–7 | Exact original and newer revision distinct; `NO_MODEL_CHANGE` is valid |
| Conditional prospective discovery | Creative discovery and possibility ontology | 2, 6 | New end vs revised future vs mechanism-only, closest `poss:` checked; no automatic owner ratification |
| Bounded graph projection and omissions | Existing SQLite/source query and view contract | 4, 7 | Same namespace/ref, bounded IDs/edges, metadata, no causal inference |
| Secondary UI inspect/copy instead of replacing agent | User-agreed primary/secondary design | 8–9 | Source inspector, keyboard alternative, scenario reset, copy-ready agent question |
| Untrusted text and read-only data | Current source/authority and security boundary | 7–9 | Escaped text, no external fetch or source write, clipboard fallback |
| Existing entrypoint/distribution preserved | ADR 0034 and setup.py packaging | 2, 10 | Optional reference; no new public Skill/backend |
| Honest verification and authority | CLAUDE.md/AGENTS.md, current CI | 4–11 | Mark hosted / local / independent evidence separately; no forced Level-3/4 change |

### Exact deferred test inventory

The following **names are design-time expected behaviors, not existing passing tests**. Under the current repository owner exception they are **NOT_RUN** and need not be written during construction. If test permissions change, implement each in its named file and perform the standard failure-first cycle before coding that behavior:

| Test | File | Main assertion |
| --- | --- | --- |
| `test_premise_context_missing_or_stale_ref` | `tests/test_semantic_premise_context.py` | Unknown/old premise -> explicit error/`NOT_ASSESSED` with source/ref, no silent current checkout fallback. |
| `test_premise_context_does_not_infer_necessity_from_references` | same | A plain `references` relation never returns `NECESSARY`. |
| `test_schema_v1_snapshots_still_build` | same or `tests/test_architecture_vocabulary_v2.py` | Existing authored schema1/2 snapshots preserve old validator/queried meaning. |
| `test_reasoning_premises_requires_source_and_known_endpoint` | `tests/test_architecture_vocabulary_v2.py` | If metadata extension GO: unknown premise/source or invalid role rejected. |
| `test_view_does_not_mix_revisions_or_repositories` | `tests/test_semantic_graph_view.py` | View and links bound to one explicit repo/indexed SHA; cross-revision mix rejected. |
| `test_view_bounded_omissions` | same | Cap overflow advertises exact counts and `truncated:true`. |
| `test_view_export_escapes_untrusted_labels` | same | Literal HTML/script-like text in graph labels does not become executable. |
| `test_scenario_overlay_never_rewrites_baseline` | same (or manual browser if purely client-side) | Reset restores source baseline; scenario not a persisted fact. |
| `test_selection_handoff_includes_source_identity_and_limits` | same | Copy text carries IDs, SHA, hypothetical state and gaps; never claims permission. |

## 15. Owner/implementation decisions chosen for planning

| Decision | Proposed default and reason | Revisit when |
| --- | --- | --- |
| **Primary interface** | Coding agent chat/CLI `using-sensemaking`; it is already canonical and benefits no new UI dependency | Actual owner changes product identity |
| **Secondary interface** | Optional local HTML/SVG single-file inspection/export; no web server/framework or external provider | Real graph UI interactions require authenticated shared sessions |
| **First feature** | Premise-sensitive reconsideration with historical source A/B and negative controls; connects expressiveness, creative reasoning and UI | A different owner-selected first question is materially more decision-relevant |
| **Schema policy** | No new graph kind/predicate by default; use existing source and attributes, seek consumer evidence before new typed roles | Source-verified question cannot be represented faithfully |
| **Query policy** | Existing queries first; bounded premise-context op only if material repeated question gap | Source-only answer or `explain` is adequate |
| **UI writing** | No write API, direct graph source changes, auto job dispatch or owner policy mutation; copy selected scenario into agent conversation | An explicit different editing/authority design is ratified |
| **Record retention** | Retain material source-grounded learnings; no generalized knowledge-file dump | Real later-agent retrieval needs an additional compact record |
| **Verification** | Current repo-specific no local unit/synthetic tests exception; source/diff and hosted CI, real use where possible; no fake PASS | Owner changes CLAUDE.md; then named TDD recipes apply |
| **Independent benefit** | Strictly `NOT_ASSESSED` until actually observed; no mandatory fabricated benchmark gate | Genuine separate agent opportunity exists |

**Anti-goal check:** A beautifully rendered canvas, 30 new predicates, or an extra public Skill with no material effect on agent decisions does not satisfy the product goal.

**End state:** a source-bound, optional, inspectable reasoning experience where the coding agent can explain *what changed, what did not, which alternative may now be plausible and what remains hypothetical*. The next agent can reuse that explanation without confusing source history, graphical presentation or speculation with truth and authority.
