# Agent-Native Knowledge Graph Reasoning with Secondary Interactive Exploration — Design v1

**Status:** Owner-agreed design direction, **planning/specification only**, not built/qualified. Approved in conversation 2026-11-05: prioritize the coding agent as the primary interface; a selective interactive graph is the *secondary* interface.  
**Inspected implementation baseline:** `ThorStarlord/sensemaking-skills@1f7d4edc432dae5b7526675217cc798adf4e425e`. Refresh before execution; source changes are not automatic semantic/strategy change.  
**Governing product:** [ADR 0034](../../adr/0034-ontology-first-adaptive-sensemaking.md) (ontology-grounded understanding and prospective reasoning, one `using-sensemaking` entrypoint, agent owns control), [ADR 0031](../../adr/0031-persistent-semantic-stewardship.md) (typed versioned knowledge), [ADR 0029](../../adr/0029-current-product-boundary.md) (no deterministic planner/authority expansion), [strategy](../../product-strategy.md) and [current status](../../../STATUS.md).  
**Related conceptual foundations:** [layered ontology](../../semantic-architecture/ontology.md), [source epistemics](../../semantic-architecture/relations-and-epistemics.md), [product possibilities](../../semantic-architecture/product-possibility-ontology.md), [prospective reasoning](../../semantic-architecture/prospective-reasoning-ontology.md), [possibility assessment](../../semantic-architecture/possibility-assessment-ontology.md), [connected inquiry](../../semantic-architecture/connected-prospective-inquiry-ontology.md), [strategic evolution and learning](../../semantic-architecture/strategic-evolution-learning-ontology.md), [graph CLI](../../semantic-architecture/persistent-knowledge-cli.md), and [schema-extension gate](../../../skills/repository-semantic-steward/references/schema-evolution.md).  
**Implementation plan:** [Agent-Native Knowledge Graph Reasoning — Implementation Plan](../plans/2026-11-05-agent-native-knowledge-graph-reasoning.md).

## 1. Why this exists

The repository has a real source-pinned graph of reviewed semantic claims, explicit relations, and deterministic probes, but graph lookup alone is not prospective reasoning. The authored packs present in the inspected baseline contain 186 claims / 217 relations across 10 JSON files (authored records **only**, not the generated whole index). The current executable knowledge graph supports reviewed schema-v1/v2 documents and exact-commit SQLite lookup, including `search`, `explain`, `why`, `impact`, `contradictions`, `history`, `changes`, `context-for`, `rules-for` and related operations.

The current distinction is:

1. **A — Knowledge expressiveness.** Precisely preserve necessary/supporting/contradicting assumptions; decision-scoped comparative grounds; conditional consequences; past lessons and their applicability; what changed, where, and under which original purpose.
2. **B — Agent-native reasoning.** Starting from a *user's consequential question*, recover relevant recorded relationships, check originals, challenge omitted premises and conflicting interpretations, and generate genuinely differentiated possibilities or justified no-change results.
3. **C — Secondary interactive graph.** Only for an inquiry worth visual inspection, show its selected source-qualified neighborhood; let a human inspect evidence, compare states, introduce counterfactual scenario overlays and send a selected question back to the coding agent. The UI **is not a graph authoring authority**, master interface, evidence oracle or replacement for conversation.

**Primary output:** a source-qualified, understandable agent answer and optional reusable inquiry explanation. The agent can complete the work with **no browser**, no existing index and no graph rendering. The UI is a secondary path, not a prerequisite to intelligence.

## 2. Product boundaries, goals and anti-goals

### Goals

1. An agent can ask "which earlier judgments warrant reconsideration if premise P changes?" and receive explicit scoped candidates, reasons, counterexamples, source links and omissions, not blanket invalidations.
2. An agent can identify **multi-premise dependencies, apparent-but-scoped contradictions, rejected-mechanism/retained-benefit separation, and conditional opportunity combinations** without representing speculative paths as causal truth.
3. An agent can distinguish **recovered source**, **previously retained interpretation**, **new same-session inference**, and **new hypothetical product end**; novelty relative to an inspected set is not absolute novelty.
4. An agent can still reach useful answers from primary sources alone if the graph is sparse, stale, absent or fails to cover a particular judgment.
5. A read-only, local, inspectable graph view can open a selected inquiry's nodes/edges/sources, compare original versus current interpretations and return copy-ready selection/scenario context to the agent.
6. A minimal concrete *vertical slice* works on real historical Sensemaking materials before expanding types, UI, or query modes.

### Non-goals

- A full graph DB replacement, RDF reasoner, inference engine, LLM orchestration runtime, hidden cognitive trace store, automatic backlog optimizer, scheduler, global strategy scorer or self-muting doctrine.
- Universal completion of repository architecture knowledge or multi-repository semantic fusion.
- Automatically promoting ideas into ratified `ProductPossibility`, selecting PATHs, changing Level 3/4, authorizing a PR/merge/release, or altering owner intent through scenario clicks.
- A graph-first app, server-side graphical service, new public Skill, mandatory graph query for narrow coding edits, uncontrolled ontology class/predicate expansion, or committing generated SQLite and HTML export files to the reviewed graph.
- Claiming independent agent improvement, cross-repository transfer, or novel user value from a successful export, visual presentation, documentation or CI alone.

## 3. Approaches compared and selected

| Approach | Merit | Failure / tradeoff | Disposition |
| --- | --- | --- | --- |
| **1. Add many schema classes + graph-first explorer** | Richly queryable when fully populated | Breaks compatibility/maintainability, encourages empty ontology rows, displaces agent, interface precedes real consumer | **Decline** |
| **2. Documentation-only agent prompts over existing graph** | Minimal cost and portable | Conditional judgments remain in prose and disconnected views; can fail to recover cross-episode premise/dependent decisions | **Fallback / first probe, not complete aspiration** |
| **3. Agent-native, consumer-driven typed view + optional local visual companion** | Directly serves real reasoning question; schema only when demonstrated missing; UI displays same read-only explanation; reversible | Needs disciplined source/projection contract and semantic validation; browser UX needs separate scope | **Select** |

The accepted orientation is an **agent-led reasoning capability** whose secondary view shares original source identities and explicit epistemic/authority limits. Build the minimal read-only reasoning projection/agent guidance first, then add **only** the documented schema expression missing from an actual consumer, then build the secondary viewer over the same projection. Source data and conceptual records remain owners, not the browser.

## 4. First concrete use case: premise-sensitive reconsideration

**Question:** "A premise has changed. Which existing architectural, strategic or possibility judgments should be reconsidered, with which reasoning, and what remains valid?"

A real source case is the original [2026-10-23 strategic analysis](../../../artifacts/history/2026-10-23-strategic-repository-analysis.md) (`PATH-1` vs `PATH-2` and `ASSUMPTION-1`/`ASSUMPTION-2`) and [2026-10-24 reconciliation](../../../artifacts/history/2026-10-24-strategic-reconciliation.md): source reachability qualified the first assumption but `PATH-1` was reaffirmed. The [2026-11-05 reference cases](../../semantic-architecture/strategic-evolution-learning-reference-cases-v1.md) already preserve these revisions and explicit no-reopening conclusions. Use original files to derive actual targets and source identities; do **not** invent a newly ratified strategic choice.

**Expected inquiry outcome:** "ASSUMPTION-1 was narrower than the original expectation. This may cause the agent to inspect retrieval prerequisites of certain judgments; it did not by itself establish PATH-1 invalid. ASSUMPTION-2 and governing purpose remained unchanged." This is more valuable than a generic PATH-1 --references--> ASSUMPTION-1 edge.

**Important negative cases:**
- Premise appears as nearby context but did **not** supply decisive support: do not mark dependent decision invalid.
- Premise is still supported, or evidence is missing: report `NO_MODEL_CHANGE`/`NOT_ASSESSED` rather than forcing changed direction.
- Source revision changed but governing meaning did not: explain file difference without fake strategy reopening.
- A hypothetical scenario contradicts real authority: keep scenario separate; return owner boundary.
- Query returns no authored links: do not claim no architectural dependence; reconstruct from original sources and disclose the graph gap.

The vertical slice is **source-grounded read-only**. At first, run existing `search`/`explain`/`history` and direct source reading. Only when a specific required comparison/conditional relation cannot be recovered as typed, source-qualified, bounded data from existing kinds/predicates/attributes should an executable extension be proposed.

## 5. Representation: explicit assertion roles, no invented causation

### 5.1 Original objects retain identity

- A source `Assumption` is a Layer-4 conceptual claim. The existing executable vocabulary supports `hypothesis` or another appropriate existing kind, with source-qualified statement/attributes. Do not fabricate an unsupported canonical `assumption` kind during initial projection.
- A `Comparison` is usually a *reified, attributed decision/judgment record*, not a context-free edge between alternatives. It cites source ID, actor, assessed target SHA, comparison frame, operands, criteria, supporting/defeating premises, original outcome and later reconsideration.
- An `ArchitectureOption` and `ProductPossibility` retain their original `arch:` / `poss:` identities and source; a strategy `PATH-n` remains in the owning strategic artifact, not a graph-created alternative kind.
- A `ConsequenceHypothesis` is a conditional effect, **not** a verified causal outcome. Its dependencies may contain AND/OR grouping and explicitly unknown sufficiency, which must not be flattened into implied transitively true edges.
- `LearningAccount` / `StrategicEvolutionRationale` remain conceptual documentary views, not automatic executable entity classes. Reuse `strategic_reconciliation` or `AssessmentRevisionAccount` when those specific source-owned roles apply.

### 5.2 Three distinct relationships

Each inquiry-relevant association is classified as:

- **Source-declared / reviewed** — original record/source supports the stated relation and its role, scope, authority, revision and limits.
- **Agent-interpreted** — a new **inference candidate** with cited grounds and counterexamples; it is not silently written into reviewed knowledge.
- **Scenario-only** — hypothetical premise inversion/branch, never an actual world/source edit or owner instruction.

Structural adjacency can suggest a relationship for checking, never establish necessity or causality.

### 5.3 Reconsideration reasons and expected semantics

The projected result distinguishes:

- **Necessary premise** for a *particular judgment under a particular frame*; no automatic invalidation of the outcome when unsupported.
- **Supporting but non-necessary premise**, where the assessment may remain justified.
- **Defeater/counterevidence**, with source and status.
- **Context/navigation only**, which does not trigger a reconsideration claim.
- **Unknown applicability / missing link**, which requires source reading or honest nonassessment.

A multi-premise group should say **ALL**, **ANY**, or **UNKNOWN** only where the source actually establishes that structure. Compare original source/assessed revision to current observed revision separately; a hash difference is not a logical premise change.

### 5.4 Extension gate

The initial implementation may build a **read-only, explicitly scoped projection** using existing reviewed sources, existing `schema_version: 1/2` records, and source-attributed documentary content. If exactly specified inquiry and reference cases demonstrate missing expressive power that cannot be represented faithfully by existing records/metadata, conduct the existing [schema-evolution gate](../../../skills/repository-semantic-steward/references/schema-evolution.md). Choose the smallest change:

1. Existing source-owned prose + read-only projection;
2. Existing `attributes`/supported typed records and explicit `references`, with source-checked relationship role in a view;
3. New validated optional typed relation/claim kind **only** after evidence of failed consumer question, endpoint definition, compatibility/migration and owner/schema authority.

If the gate fails, preserve a **source-only agent outcome** and leave the machine extension `NO_GO`. No package migration or universal graph truth authority by default.

## 6. Primary agent interaction

**Activation:** a user explicitly asks to reconsider a direction, compare architecture/strategy, explore consequences, find new product ends, or source-check why a previous decision might change. The agent decides relevance and scope under `using-sensemaking`; routine edits do not require graph access.

**Conversation-first sequence (not a fixed controller):**

1. **Frame question:** target, beneficiary/outcome, original decision versus exploratory question, permissible action, current source revision and relevant assessed historical revision.
2. **Retrieve bounded context:** existing `knowledge-query` operations and selective source/doc reading. Candidate relation discovery is not mandatory success; if indexed view missing, sources are fallback.
3. **Check exact source:** original evidence, actual authority, relation role, scope, currentness, omitted records and any counterexamples.
4. **Challenge critical bridge:** what makes the premise decisive, what remains true if it changes, whether A and B are being compared under same frame, what contrary sources say.
5. **Explore meaningful alternative:** when material, apply assumption inversion, temporal revival, negative-space search, recombination or consequence analysis. Preserve distinction between known capability, new mechanism, revised possibility and genuinely new desired end.
6. **Answer with a bounded inquiry explanation** and a clear stop. It includes source-backed/interpretive/hypothetical distinctions and changed-versus-unchanged conclusions; it does not auto-authorize work.
7. **Optional second interface:** if relationships, counterfactuals or temporal deltas are difficult to inspect in prose, export/open focused graph. Selection/scenario yields a copy-ready *new agent turn*, not an automatic tool invocation.
8. **Selective learning:** only reconcile material source-backed new knowledge when another context would benefit and authorized. `NO_MODEL_CHANGE` is valid.

### Expected primary answer contract (documentary, not a new registered artifact)

- **Question/outcome/actor and original target identities**.
- **Source identity:** repository, indexed SHA, inspected current revision and historical assessed SHA(s).
- **Findings:** directly supported, inferred with grounds, hypothetical scenario branches, and unassessed gaps.
- **Premise-sensitive candidates:** each exact target, relation role, why it matters, affected comparisons, unchanged alternatives and counterexamples.
- **New possibilities:** differentiated against closest reviewed `poss:`; no invented owner demand.
- **Authority/stop:** whether no change, limited reconsideration, bounded further inquiry, reserved owner decision or optional downstream construction is warranted.
- **Optional graph link/export and minimal scenario context** for continued agent chat.

The output is a source-qualified *reasoning result*, not a hidden chain-of-thought transcript.

## 7. Secondary interactive graph

### 7.1 Intent and boundaries

A **local, read-only, question-scoped visual companion**, launched from a coding-agent answer or an explicit CLI export. Default: no server, no login, no external network, no JavaScript framework/Cytoscape dependency, no graph database replacement and no graph file checked into `.sensemaking/knowledge/`. Use the existing Python >=3.11 package and a packaged static HTML/CSS/JS asset under `src/sensemaking_skills/semantic_architecture/view_assets/` or a deterministic self-contained HTML export. Validate package resource inclusion.

The browser receives an **explicitly bounded, source-pinned view**, not the full repository, hidden prompts, secrets, tool credentials, unrelated files or user conversation history. Avoid accidental sensitive data exposure by requiring explicit local export and applying bounded content/source paths. Treat source text as untrusted; render using text nodes / escaping, never arbitrary HTML.

### 7.2 Planned useful views

- **Premise and consequences:** a judgment, original premises, supporting/defeating relationships, consequence hypotheses and material unknowns.
- **Alternatives under a comparison frame:** A/B/unchanged preference, source scope, actual deciding actor versus proposed recommendation.
- **Before / after:** original assessed source and current evidence/change, with preserved historical decision and new interpretation instead of claiming original source was false.
- **Opportunity neighborhood:** current outcome, recorded possibilities, enabling capabilities, common assumptions, conflict/complement candidates. New combination is visibly marked *hypothetical*.

Initial viewer may ship one focus (`premise-sensitive reconsideration`) with controls reusable for the other three. Do not fabricate missing graph edges just to complete a pleasant diagram.

### 7.3 Core controls

- **Focus and depth:** open a named source-qualified node, select a finite neighborhood, expand within explicit bound, display omitted/`NOT_ASSESSED` neighbors.
- **Kinds/evidence:** filter entities/relations by role or establishment class; a citation/source inspector shows source ID, Git revision and status. Visual shape/color alone must not be sole carrier of epistemic meaning.
- **History/compare:** show two real indexed/source-attributed states separately (or a sourced pairwise reconciliation), identify revised versus unchanged judgments without assuming Git indexing order is ancestry.
- **Scenario:** temporary premise inversion or changed criterion, clearly bannered `HYPOTHETICAL / NOT COMMITTED`, affecting only the view/agent follow-up text. No browser mutation writes to repo, SQLite or owner policy.
- **"Ask coding agent" selection handoff:** copy a deterministic, bounded Markdown instruction containing original IDs, selected node/edge, source refs, scenario assumptions, limits and user-entered question. Host-specific API integration is optional later, never a prerequisite or silent background execution.
- **Accessibility/degradation:** keyboard-accessible list/inspector and static tables when SVG arrangement is hard to read, screen-reader labels, source links, clear truncation; mobile/low-vision readable. A graph is an optional aid, never the only way to inspect findings.

### 7.4 Projection/view contract

Design a stable **read-only view envelope** independent of HTML renderer (not the canonical knowledge artifact schema):

- `view_version: 1`, `repository`, `target_ref`, optional `indexed_ref`/`assessed_ref`, `question`, `focus_ref`, `source_scope`, `omissions`/`truncated` and `action_authorized:false` / `semantic_truth_established:false`.
- `nodes[]`: stable original ID and existing kind, concise label, source refs, epistemic class, authority/display notes, role and interpretation provenance. Never return inferred source status as observed.
- `edges[]`: stable local view edge ID, original subject/object IDs, meaningful relation role, establishment class, evidence/source, scope, necessary/supporting/contrary/context distinctions when actually sourced, scenario-only marker and no automatic transitive entailment.
- `comparisons[]` / `scenarios[]` only when warranted; a scenario records its assumptions and **does not rewrite baseline nodes**.
- `selection_context` generated from the view by an explicit user action; it is an input draft for the coding agent, not a canonical command or source revision.

The view builder never decides semantic truth, reopens Level 3/4, or produces a new product requirement. It checks IDs, paths, limits, metadata and escaped presentation. The UI can only derive local display/layout or user-selected hypothetical scenarios.

## 8. Three separable, independently valuable vertical increments

**Increment I — source-qualified premise reconsideration:** A short authoring/reconstruction example and self-contained optional agent guidance over current graph + originals. A useful answer can be delivered without any new executable schema or browser.

**Increment II — bounded structural retrieval/view contract:** If I reveals a material repeated query/representation gap, add one minimal read-only bounded projection. For actual role distinction that fails under current schema, run extension gate first. Implement negative-case and source-currency checks, and document exact existing consumer. Do not implement general causal inferencing or generic graph rankings.

**Increment III — local secondary viewer:** Build one self-contained source-pinned, read-only visual over the same bounded projection, including source inspector, selected scenario and "Ask agent" copy handoff. It must be useful without agent-specific browser integration and absent from the primary workflow unless requested/valuable.

Each increment has its own outcome/review gate and can stop without pretending the remaining increments were implemented. The whole feature needs source/contract/packaging evidence, not automatic broad empirical qualification.

## 9. Acceptance and evidence ceilings

### Documentary/semantic correctness

- Agent can reconstruct the historic `ASSUMPTION-1` qualification and the reason `PATH-1` remained selected, from sources rather than guessed adjacency.
- Three different relations—necessary, merely supporting, and context-only—are represented or explicitly marked unassessed; one changed assumption never automatically invalidates every linked judgment.
- Positive, negative, no-change, unknown/missing link, contested/contrary and old-revision cases are covered at the correct epistemic/source ceiling.
- A new outcome idea remains hypothetical and is contrasted with a closest known `poss:` and with mechanism-only novelty.
- A sparse/absent graph produces a useful source-only or honest `NOT_ASSESSED` answer.

### Mechanical/projection/view correctness

- Explicit repository and SHA identity, bounded result count, unchanged source ID, truncation, no cross-repo leakage and no fabricated predicate/endpoint. A missing target SHA fails closed.
- Scenario and interactive selection do not modify reviewed JSON, SQLite, owner/authority source, or historical reports.
- Exported HTML reads no remote scripts; untrusted labels and evidence render inert, keyboard-only navigation is usable and copy handoff works or has a documented manual fallback.
- Original and current source statements are visually distinct; observed versus inferred versus hypothetical status remains visible even without color.

### Product/reasoning claim ceiling

- **Source projection/hosted CI** may establish correct serialization, distribution and deterministic UI behavior, not improved agent reasoning.
- **Agent application** requires a real agent to independently frame, retrieve, source-check and materially apply relevant knowledge; pasted scripted answers do not count.
- **Comparative benefit** requires a credible source-only alternative with comparable access/quality and attribution of retained interpretation versus graph structure versus guidance.
- **Novel goal** requires a genuinely different beneficiary outcome, not an architecture variation or prior-idea restatement; owner ratification is separate.
- **Cross-repo doctrine** requires heterogeneous evidence/valid transfer conditions; this bounded first slice does not claim it.

## 10. Failure modes and stop conditions

1. **Promising but unsupported chain:** a path in the graph is mistaken for a cause; respond with explicit hypothetical bridge and required evidence.
2. **Stale source/assumption:** a current implementation exists but old decision was judged at an older SHA; preserve both and recheck actual applicability, no automatic veto.
3. **Too little graph coverage:** source-only reconstruction before schema expansion, `NOT_ASSESSED` where sources cannot resolve.
4. **False novelty:** output appears new only because agent did not inspect closest recorded possibilities; reclassify as restated/revised/unknown.
5. **False universal learning:** one reviewed lesson is copied into another repository without matching conditions; reject or narrow.
6. **Graph UI becomes product controller:** browser click triggers job or writes historical truth; prohibit and keep human selection as provisional message.
7. **Large visual without useful question:** reject broad canvas until one actual agent result benefits from inspection.
8. **Evaluation inflation:** docs/CI or same-agent construction reported as independent superiority; record narrower achieved status.

**Definition of design success:** the agent can answer a real premise-sensitive reconsideration better *in kind* than a raw adjacency dump, using original sources and explicit uncertainty. The visual companion helps inspect/challenge the same account without stealing the primary UI role. Additional ontology types, automated generator and generalized cross-repository agent benefit are **not** assumed outcomes.
