# Strategic Evolution & Learning Ontology v1 — Detailed Implementation Plan

> **For a subsequent implementing agent:** Load the current installed `using-sensemaking` Skill, refresh the repository/authority baseline and perform only work authorized at that time. **Implementation record:** The owner separately authorized execution of all tasks on 2026-11-05. The checklist and closeout section below distinguish completed documentary implementation from optional NO_GO actions, actual validation, and outcomes requiring independent later-agent evidence. This record does not grant reusable thesis, merge, publication or deployment authority.

**Goal:** Connect two distinctive responsibilities through one source-preserving, portable Level-2 conceptual ontology: **Strategic Evolution Analysis** ("Where should this system evolve, and why?") and **Learning & Reassessment** ("What did we learn, and what changes—if anything?"). Preserve past judgments and accepted authority while making future opportunity, source-grounded reasoning, knowledge delta and decision consequences reconstructible.

**Selected approach:** single conceptual module, shared semantic spine, two focused profiles, no fixed pipeline; real source-pinned examples, local competency questions, one optional installed guide/record and minimal conditional integration. Repository-local learning is the default; cross-repository method/doctrine learning is a higher-threshold *candidate* using current Capability Learning Loop guidance, never automatic.

**Design:** [Strategic Evolution & Learning Ontology — Design Basis](../specs/2026-11-05-strategic-evolution-learning-ontology-design.md).  
**Planning baseline:** `ThorStarlord/sensemaking-skills@32562d3364fe90c8f53317ea75eb96db3ba7d635` (2026-11-05, after integrated Connected Prospective Inquiry v1).  
**Plan status:** **IMPLEMENTED (documentary conceptual v1) — 2026-11-05**, via PRs **#754 (shared ontology), #755 (historical cases and SEL competencies), #756 (portable guidance and conditional integration)**; closeout recorded here. Task 9 ended **NO_NEW_KNOWLEDGE_PACK**, not a partial attempt to create JSON. The 20 questions have documentary source-fit judgments, not independent agent qualification. Current hosted checks and intentionally unrun local validation are recorded in Section I.  
**Technology and representations:** repository Markdown/Skill references, existing strategy/learning/ontology contracts and `schema_version: 1` reviewed knowledge **only if a real retrieval need warrants it**. No runtime dependency, new public Skill, new strategic artifact ID, stage controller, graph predicate or automatic ranking engine.

## A. Decisions taken for the plan

1. **One connected design:** `StrategicEvolutionRationale` and `LearningAccount` are **documentary account roles**, not two competing ontology families or executable entities. They share original target identities, source/assessed revision, author, beneficiary, governing intent, epistemic basis, causal/interpretive limits and authority.
2. **Evolution means change in desirable future capacity:** include distinct new product ends, known ends through different capabilities, architectural leverage, simplification/retirement, and legitimate no-change. Do not equate "has a missing feature" with "should evolve here."
3. **Learning means an explicit understanding delta:** distinguish changed system/world, changed interpretation, and changed governing intent; allow `NO_MODEL_CHANGE` and `CONFIRM` as substantive outcomes; learning is not synonymous with reordered priorities.
4. **Scope across three learning loops:** episode/responsibility, longitudinal repository strategy, and cross-repository reusable capability doctrine. The third is conditional and evidence-gated; no automatic self-improvement or Skill editing.
5. **Reuse existing producers:** canonical `strategic_repository_analysis` (v2), `strategic_reconciliation`, Strategic Continuity, Learning/Reconciliation Policy and ADR/product-thesis authority keep their current meaning, machine field contracts and validators.
6. **Keep purpose-relative comparisons:** intellectual inquiry priority, strategic attractiveness and authorized implementation priority are distinct; a new possibility is not a selected ProductPossibility, and strategic recommendation is not implementation permission.
7. **Adaptive integration:** possible feedback across Depth Exploration, Convergent Reassessment, Adversarial Review, Architecture Synthesis, strategic analysis, implementation and Learning/Reconciliation; no mandatory chronological stages.
8. **No executable v1:** new `StrategicEvolutionRationale`/`LearningAccount` semantics and documentary verbs are prose-only until an actual source/re-entry/parsed consumer limitation warrants an independent, compatible schema proposal.
9. **Default no redundant knowledge pack:** retain source-linked guides and existing historical records first. Add an existing-schema reviewed pack only after a concrete user/agent retrieval question remains inadequately served.
10. **No separate fresh-agent qualification requirement:** documentary fit is checked with source cases; independent agent improvement is explicitly `NOT_ASSESSED` unless a separately warranted real task provides that observation.
11. **Review and closure:** source/diff inspection and existing applicable hosted checks, current local test exception, separate PR boundaries, ordinary authorized merge, qualified final receipt and strategic-state preservation.

## B. Governing constraints and stop rules

- **G1 — Authority/currentness.** Re-read `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `docs/product-strategy.md`, `STATUS.md` and relevant accepted ADR 0029/0031/0034 at implementation HEAD; pin the actually **assessed** repository revision separately from each report/file revision.
- **G2 — Canonical strategy.** `docs/strategic-repository-sensemaking-v1.md`, `docs/strategic-state-contract.md` and `docs/strategic-continuity-v1.md` own Level-3 strategic semantics, source-currentness and path lineage. `STATUS.md` is current projection, historical source reports stay immutable.
- **G3 — Machine contract safety.** `strategic_repository_analysis` canonical `schema_version: 2`, `strategic_reconciliation` and their current producers/consumers/validators remain unchanged; no `StrategyState` replacement, new `LearningAccount` artifact ID, invented `strategy_version`, numeric priority field, inferred currentness/authority, or automatic disposition.
- **G4 — No false decision.** Distinguish evidence, interpretation, provisional preference, scoped decision, authority to execute, merged work and verified user outcome. Level-4 thesis challenge requires the actual ratifying actor.
- **G5 — No false causality.** Inferred evolution mechanism and proposed future consequences are hypotheses. `A may enable B` plus `B may enable C` is not proven causal or economically valuable C. Present-state fact and future speculation must have different claims.
- **G6 — Keep original identity.** Preserve source-local `poss:`, `arch:`, `conseq:`, `PATH-1`/`PATH-2`, `ASSUMPTION-1` and other IDs with originating artifact and assessed revision. A prose view or thematic grouping is not a `sameAs` claim.
- **G7 — Substantive strategicity.** Level-3 opportunity needs a material change in future outcome/capability/architecture/authority or genuinely valuable options; routine fix, UI polish, backlog or source drift alone need not reopen strategic analysis.
- **G8 — Priority frames.** Inquiry-learning preference, relative product/strategic attractiveness, and authorized implementation priority must never substitute for each other. Local pairwise changes leave unaffected previous judgments historical.
- **G9 — Learning category.** `WORLD_CHANGED`, `UNDERSTANDING_CHANGED`, `GOVERNING_INTENT_CHANGED` are descriptive distinctions only; no new machine enum. Owner selection cannot be reclassified as an agent's empirical learning.
- **G10 — Learning evidence ceiling.** Repository source reads and hosted validation may support the fact an artifact exists/works mechanically; they do not prove a later agent retrieved/applied it or that creative/strategic decisions improved.
- **G11 — Selective transfer.** One episode can create a local lesson candidate. Cross-episode generalization needs comparable independent/heterogeneous sources, context limits and counterevidence; doctrine promotion requires separately warranted ordinary changes/qualification/authority.
- **G12 — No mandatory forms.** Optional sparse account only when another actor/context needs it; trivial local work can end with no new learning file, strategic analysis or review.
- **G13 — Source-specific examples.** Historical records A–E are evidence of *what their authors recorded*, not re-enacted performance. The owner-intent/world/interpretation triad's case F is explicitly **NORMATIVE**, not a fabricated historical implementation.
- **G14 — Current installed path.** Reuse `using-sensemaking` and `strategic-repository-analysis`/existing learning-policy references. The real minimal installer profile matters; do not introduce a sixth public stage or a required new Skill.
- **G15 — Current local construction policy.** `CLAUDE.md` (2026-10-25/26 instructions) directs **no added or manually run local unit or synthetic-evidence tests** for present construction PRs, source/diff inspection, and prompt merge after authorized clean review without waiting for hosted CI. Preserve hosted CI and protections; record `NOT_RUN`, `PENDING` or `PASS` accurately.
- **G16 — Product thesis remains stable.** Do not change ADRs, product strategy, governing PATH-1 or normal-use research agenda merely because a conceptual module exists. A source-grounded implementation note is not an owner-facing decision to redirect strategy.
- **G17 — Evidence economy.** Do not run an independent experiment, new causal/learning benchmark, install-time engine or cross-repository field campaign just to populate this plan. Source fit and real consumers first.
- **G18 — Stop boundary.** Finish when the two profiles, source cases, competency meaning, optional portable guidance, source/authority preservation and no-go retention decision are reconstructible. If no consumer demonstrates missing semantics, stop without extra infrastructure.

## C. Target files and artifact ownership

### New core deliverables

| Planned path | Contents / consumer |
| --- | --- |
| `docs/semantic-architecture/strategic-evolution-learning-ontology.md` | Shared Level-2 conceptual spine, two distinct profiles, scope and evidence axes, non-identities, documentary relations, feedback and authority/stop boundaries. |
| `docs/semantic-architecture/strategic-evolution-learning-reference-cases-v1.md` | Five historical pinned cases A–E plus one **normative** F counterexample, provenance, negative outcomes and cross-case limitations. |
| `docs/semantic-architecture/strategic-evolution-learning-competency-v1.md` | `SEL-CQ-01..20` local questions, expected source-specific answers, `ANSWERABLE`/`PARTIAL`/`NOT_ASSESSED` and claim ceilings; crosswalk to global CQ-115..130. |
| `skills/strategic-repository-analysis/references/strategic-evolution-learning-v1.md` | Portable self-contained conditional agent-facing instructions, each profile has trigger/input/source rules/output/anti-patterns/stop; no target-specific document dependency. |
| `skills/strategic-repository-analysis/references/strategic-evolution-learning-record-template.md` | **Optional**, sparse single Markdown record for cross-session reasoning, not a parsed artifact, mandatory form, PRD, new `strategic_reconciliation` producer or receipt. |

The shared conceptual module is one file with two distinct internally labeled profiles. If a source case reveals a distinct meaning already perfectly captured by current contracts, use an explicit crosswalk rather than adding a duplicative new named role.

### Existing files — touch only with justified, minimal edits

| Existing path | Acceptable change |
| --- | --- |
| `docs/semantic-architecture/README.md` | Index ontology, source cases, competencies and portable guidance. |
| `docs/semantic-architecture/ontology.md` | Link the conceptual account roles; no executable relation endpoint or new knowledge kind. |
| `docs/semantic-architecture/competency-questions.md` | Point to local `SEL-CQ` questions without allocating conflicting global CQ numbers. |
| `docs/semantic-architecture/connected-prospective-inquiry-ontology.md` | One bounded cross-reference distinguishing its **Convergent Reassessment** from broad Learning & Reassessment. |
| `docs/strategic-repository-sensemaking-v1.md` | Small ontology pointer only if it adds a concrete interpretive aid not already given by canonical strategy semantics. |
| `docs/strategic-continuity-v1.md` | Only a short source/learning cross-reference if needed; do not alter machine comparison/currentness or path lineage. |
| `docs/research/capability-learning-loop-v0.md` | At most a pointer to the conceptual account; no promotion of evidence-gated candidate into automatic runtime. |
| `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md` | Conditional link when an evolution judgment or changed learning frame requires specific guidance. |
| `skills/using-sensemaking/references/learning-reconciliation-policy-v0.md` | Conditional pointer for learning account when a material change must be explained across contexts; no second policy. |
| `skills/strategic-repository-analysis/SKILL.md` | At most a one-line first-load cue **only if** source review demonstrates a decision it changes. Otherwise unchanged. |
| `skills/using-sensemaking/SKILL.md` | **Prefer unchanged** unless a genuinely different responsibility decision requires an entrypoint cue; ensure no duplication with the already integrated Connected Prospective Inquiry first-load row. |
| `skills/strategic-repository-reconciliation/SKILL.md` | **Prefer unchanged**; it already owns the canonical Level-3 reconciliation producer and machine contract. |
| `STATUS.md` | Only if the implemented documentary capability changes a material current-state statement; preserve Level-3 PATH-1 and owner authority. |
| `docs/semantic-architecture/relations-and-epistemics.md` | Optional compact documentary verb crosswalk if semantically necessary; never add parsed relation IDs. |
| `.sensemaking/receipts/<dated-session>.session.yaml` | A real existing-schema implementation receipt if work has actually completed and a future context needs it. |

### Strictly conditional file

`.sensemaking/knowledge/strategic-evolution-learning.json` — **default NO_GO**. Only add reviewed source-grounded existing-schema assertions if a documented retrieval/re-entry question cannot be answered adequately through the existing guide/records and a real `context-for` / `search/explain` consumer benefits. Omit the file otherwise. No new enum, `KnowledgeGraph` causal rule, graph-score or Level-3 state mirror.

### Preserve unchanged unless a separate warranted responsibility is found

`docs/product-strategy.md`, ADRs, `CONTEXT.md`, source historical artifacts, existing `strategic_repository_analysis`/`strategic_reconciliation` templates, `artifact-contracts.yaml`, validators, Skill registry, installer profiles, application code, runtime, and product-thesis/scope machinery.

## D. Detailed task sequence and acceptance gates

### Task 0 — Currentness, responsibilities, source and contract audit

**Input:** implementing HEAD, planning design, actual owner delegation. **Output:** short evidence/consumer inventory in implementation PR note or ontology provenance; no redundant permanent audit document by default.

- [x] Read current `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, product strategy, `STATUS.md` and ADRs 0029/0031/0034; record execution and original assessed revisions separately.
- [x] Confirm current Level-3 strategic authority, active PATH-1 and exact owner-reserved Level-4 commitments.
- [x] Inspect strategic analysis v1 semantics, canonical current v2 `strategic_repository_analysis`, Strategic State Contract, Strategic Continuity, and `strategy compare/drift/history/graph` claim ceiling.
- [x] Inspect Learning / Reconciliation Policy, existing strategic-reconciliation Skill and exact current `strategic_reconciliation` producer/consumer and field contract.
- [x] Inspect current layered ontology, product-possibility ontology, assessment, connected-inquiry profiles, CQ-115..130 and capability-learning research model; identify genuinely distinct versus overlapping meanings.
- [x] Confirm source availability and old analyzed revisions for cases A–E (H-A/B/C nomenclature from older ontology is not reused as new canonical identity).
- [x] Check whether planned files/reference links already exist or have been moved; adapt to actual current source.
- [x] Record precise source-grounded choice: conceptual crosswalk warranted; no new parsed ontology, self-modifying learning engine, universal learning artifact or extra public Skill.

**Done when:** existing owners/types, source-of-truth boundaries and actual deliverable gaps are distinguishable from mere terminology gaps.

### Task 1 — Shared semantic spine

**Prerequisite:** Task 0. **Deliverable:** `strategic-evolution-learning-ontology.md` sections for purpose, identity, evidence and authority.

- [x] Define the same source-preserving frame for both profiles: actor, date, purpose, beneficiary, original target/reference, governing revision, assessed target revision, constraints, evidence class, alternatives, decision affected, consequence and stop/re-entry.
- [x] Distinguish reasoning activities from original entities and durable current/history projections; no `sameAs` across a proposal, present capability, path, historical decision or lesson interpretation.
- [x] Define `StrategicEvolutionRationale` and `LearningAccount` as optional *documentary roles*; reuse the named existing canonical strategy/reconciliation artifacts and `AssessmentRevisionAccount`.
- [x] Define the three orthogonal axes: **learning scope** (episode/repository/doctrine), **change object** (world/model/governing intent), **evidence class** (observed/derived/inferred/hypothesized/evaluated/ratified).
- [x] Define documentary associations (`groundedIn`, `supportsFuture`, `motivatesReconsideration`, `updatesUnderstandingOf`, `mayOpenPossibility`) with source/target meaning and non-executable warning.
- [x] Record why source-change detection and valid graph references do **not** imply semantic invalidation, causal inference, strategic selection or lesson correctness.
- [x] Include small proportional record policy: prose/section when cheap; existing canonical artifact when needed; avoid duplicate universal record and multi-phase ceremony.
- [x] Record accepted owner/product scope and Level-3/Level-4 boundary without treating this planning authority as owner revision.

**Done when:** a future agent can answer which original object, sourced assertion, comparison and actual authority a learning or evolution claim concerns without inventing new data kinds.

### Task 2 — Strategic Evolution Analysis profile

**Prerequisite:** Task 1. **Deliverable:** its bounded conceptual ontology section.

- [x] Specify trigger: an open material system/product future-direction question rather than a localized known edit, ordinary implementation or generic possibility-only inquiry.
- [x] Define capability-state/limitation baseline, governing outcome and original owner intent with assessed revision/claim ceiling.
- [x] Distinguish *new desirable end*, *new ability serving existing end*, *new architecture mechanism*, *simplification/retirement*, *maintenance repair* and *strategy-thesis review*; prevent conflating an end and one possible means.
- [x] Reuse `Strategic Frontier`, `ProductPossibility`, `ConstructionPath`, `FutureCapabilityState`, `ArchitectureOption` and current path/strategic hypotheses with unchanged identity and producer.
- [x] Explain opportunity plausibility through current capabilities/relationships/constraints, mechanisms, prerequisites and conditional consequences; avoid undocumented success/feasibility claims.
- [x] Require purpose-relative qualitative comparison including commission risk, **omission/deferral cost**, reversibility, uncertainties and alternatives not selected; no numeric score, candidate quota or universal ranking.
- [x] Allow no path, one path, multiple paths or `NO_CHANGE` after grounded inquiry; retain a meaningful absence/authority/stop conclusion.
- [x] Preserve recommendation vs source-attributed selected path vs action authorization; Level-4 tension must go through actual owner review.
- [x] Record specific decision-changing assumptions and the evidence/owner-change conditions that would justify future reassessment.

**Done when:** the profile can articulate a credible strategic future, a better simplification alternative, an unfounded/mechanism-only option and a warranted no-selection outcome without creating new canonical artifacts.

### Task 3 — Learning & Reassessment profile

**Prerequisite:** Task 1. **Deliverable:** its bounded conceptual ontology section.

- [x] State the minimum unit: previous explicit attributed claim/assumption/judgment/lesson, exact new source/revision, assessed applicability and decision-relevance question.
- [x] Distinguish **repository changed**, **understanding changed**, and **governing intent changed** with at least one case of different implications and multiple simultaneous deltas allowed.
- [x] Reuse current Learning/Reconciliation dispositions without inventing machine enums or a second policy; `NO_MODEL_CHANGE` is a valid end.
- [x] Separate observed evidence, interpretive inference, conditional effect, speculative opportunity, comparison, owner instruction and verified product outcome.
- [x] State which previous facts remain historically correct, what interpretation was revised, which uncertainty resolved/opened, and how another context can verify source relevance.
- [x] Distinguish retained, retrieved, source-checked, decision-informing, outcome-supported, independently reused and comparatively beneficial lesson evidence **without** making new parsed stage fields.
- [x] Describe positive, negative and inapplicable precedent: a later reader can challenge or reject a retained lesson when current conditions differ.
- [x] Describe new possible futures exposed by a corrected frame without automatically promoting/choosing a ProductPossibility or reopening Level 3.
- [x] Define local `CHANGE_RESPONSIBILITY` versus proper `strategic_reconciliation`/`REOPEN_STRATEGY`/Level-4 review; owner change remains owner authority.
- [x] Describe cross-episode capability doctrine candidate: specific multi-episode evidence, contextual commonality/differences, counterexample, proposed smallest reusable target, qualification need, retained vs applied value and no automatic Skill edit.

**Done when:** a learning account can explain an altered claim with unchanged strategy, an applicable vs inapplicable lesson, an actually changed source, a conceptual reframe and a separately authorized product-purpose change.

### Task 4 — Cross-profile interfaces and existing ownership

**Prerequisites:** Tasks 2–3. **Deliverable:** explicit crosswalk/feedback section and identified no-duplicate producer boundary.

- [x] Distinguish **Strategic Evolution Analysis** (Level-3 direction synthesis) from **Strategic Reconciliation** (returned Level-3 evidence versus an earlier strategic artifact).
- [x] Distinguish **Learning & Reassessment** (meaning/interpretation delta for any qualified scope) from **Convergent Reassessment** (particular dated judgment under a purpose-relative frame).
- [x] Crosswalk to connected Depth/Adversarial/Architecture Synthesis profiles as optional input/output evidence, never as required stage order.
- [x] Crosswalk `strategic_repository_analysis` v2 grounding (frontier refs, capability refs, `why_plausible`, assumptions and path IDs) and `strategic_reconciliation` without redefining their machine fields or validators.
- [x] Explain distinct roles of `Strategic Continuity` authored lineage versus `strategy compare/drift` mechanical observation versus Learning/Reconciliation semantic judgment.
- [x] Define safe re-entry patterns: explanation changes with same direction; choice narrows; source invalidates current path; owner changes purpose; retained lesson is rejected; new creative question opens while strategy remains stable.
- [x] Explicitly support `NO_MODEL_CHANGE`, `NO_SELECTION`, `NOT_ASSESSED`, `REOPEN_STRATEGY` and `THESIS_REVIEW_REQUIRED` at existing owning boundaries; do not invent a new mandatory control enum.

**Done when:** no profile competes with an existing producer and a reader cannot mistake changed source, comparison, instruction or artifact validity for adopted strategy.

### Task 5 — Source-pinned reference cases and adversarial counterexamples

**Prerequisite:** Tasks 2–4. **Deliverable:** `strategic-evolution-learning-reference-cases-v1.md`.

- [x] Pin this report's repository source snapshot and each original historical artifact's *own* analyzed revision, actor/status/authority.
- [x] **A: 2026-10-23 Strategic Repository Analysis** — reconstruct PATH-1 vs PATH-2 opportunity, actual decision frame, assumptions, costs, alternatives and legitimate Build/selection boundary.
- [x] **B: 2026-10-24 Strategic Reconciliation** — reconstruct `ASSUMPTION-1` revised for source reachability, `ASSUMPTION-2` confirmed, `PATH-1` reaffirmed and transition partially achieved, without rewriting original strategy.
- [x] **C: 2026-11-02 cross-episode source re-entry** — explain exact missing-anchor mechanisms across PRs #691/#697/#701/#704 and counterexample #696; show why plausible generalization is currently repository-local.
- [x] **D: 2026-11-03 pairwise portfolio update** — distinguish next *inquiry* preference from strategic attractiveness and work authorization, preserving original full portfolio.
- [x] **E: 2026-11-05 Connected Prospective Inquiry implementation** — contrast documentary capability/source distribution PASS with independent agent-value NOT_ASSESSED and Level-3 `NO_MODEL_CHANGE`.
- [x] **F: normative comparator** — distinguish observed code change, new interpretation of unchanged code, and actual owner-adopted governing intent; label every constructed input/outcome **illustrative, not historical**.
- [x] Include negative cases: repository diff as proof of strategy invalidity, feature absence as strategic priority, speculative goal as validated demand, lesson storage as applied benefit, pairwise inquiry reorder as global product preference, one anecdote as universal Skill law, expected future effect as observed, and planning PR as implementation.
- [x] Preserve exact original IDs, unaffected past judgments, source attribution, counterevidence, alternative mechanisms and stopping conditions.

**Done when:** each profile has at least two source-grounded positive examples and each high-risk semantic error has a source-based or clearly labeled normative counterexample.

### Task 6 — Twenty local competency questions and source-fit review

**Prerequisite:** Task 5. **Deliverable:** `strategic-evolution-learning-competency-v1.md`.

- [x] Author `SEL-CQ-01..10` for strategic evolution: intent/identity, outcome/mechanism distinction, grounded hypothetical future, alternative distinctness, value/beneficiary, omission/simplification, qualitative purpose-relative comparison, authority/Level3–4, reconsideration hinge, warranted no-selection.
- [x] Author `SEL-CQ-11..20` for learning/reassessment: predecessor and new source, world/model/owner delta, evidence category and claim ceiling, changed/unchanged state, lesson applicability and rejection, retained-vs-applied-vs-beneficial, discovery/reframing of new questions, local vs strategic reconciliation, cross-repo doctrine threshold, stop/reopen/authority.
- [x] Cross-reference existing global CQ-115..130 and local CPI-CQ in current connected ontology; do not duplicate numbers or claim their empirical answers have changed.
- [x] Map every local question to exact A–F source location, source-qualified expected answer, contrary/negative interpretation and a fit result (`ANSWERABLE`, `PARTIAL`, `NOT_ASSESSED`).
- [x] Explicitly mark independent agent-use/better strategy quality, cross-repository generalization and automated re-entry as **not assessed**, not PASS merely because the conceptual account is valid.
- [x] Correct any role that cannot be distinguished from existing canonical concepts; remove redundant roles or scope claims rather than adding arbitrary fields.

**Done when:** another source-literate reviewer can reconstruct and challenge the authors' claims without conversation context, and unproven hypotheses remain visibly unproven.

### Task 7 — Portable guidance and optional documentary record

**Prerequisite:** Tasks 1–6. **Deliverables:** one installed source reference and one optional sparse template.

- [x] Create a self-contained conditional `strategic-evolution-learning-v1.md` usable in target repositories without this source repo's `CONTEXT.md`, ADRs, history, graph, or its CLI.
- [x] Explain each profile's trigger, bounded question, evidence/source inspection, minimal meaningful output, legitimate negative result, common drift and stopping condition.
- [x] Include explicit decision of **when** a pure creative inquiry is not a Level-3 restart, when a local lesson does not need a strategic reconciliation artifact, and when an actual owner-intent change requires true authority.
- [x] Include conceptual difference from Connected Prospective Inquiry and existing `Strategic Exploration Funnel` guidance; do not reprint their whole procedures.
- [x] Include cross-repository doctrine promotion only as *conditional reasoning* subject to evidence/authority; warn that `installed != loaded != invoked != applied`.
- [x] Create one optional `strategic-evolution-learning-record-template.md` with shared envelope plus either/both profile sections; omit empty boilerplate and keep existing canonical artifacts authoritative.
- [x] Include one small worked counterexample of `NO_MODEL_CHANGE` and one of rejecting an inapplicable past lesson; no claim that a new agent actually performed them.
- [x] Keep file references packaged within the same installed Skill tree and free of source-repo-relative dependencies that fail in target installations.

**Done when:** a fresh target agent reading the installed guide can recognize the relevant question without knowing this chat, and the template is clearly not a new schema or mandatory output.

### Task 8 — Conditional integration and navigation, minimal touch

**Prerequisite:** Task 7. **Deliverables:** only source refs shown necessary by actual reading path.

- [x] Link ontology, local competencies, source cases and installed guide from `docs/semantic-architecture/README.md`, with no duplicate conceptual index.
- [x] Add one bounded conceptual link to `docs/semantic-architecture/ontology.md` and local `competency-questions.md`; no typed graph predicate or global CQ allocation.
- [x] Clarify in `connected-prospective-inquiry-ontology.md` that Convergent Reassessment is *judgment-specific* while Learning & Reassessment may change understanding at other scopes; avoid two competing `AssessmentRevisionAccount` producers.
- [x] Provide conditional guide link in `strategic-exploration-funnel-v1.md` at strategic future-direction reasoning, without creating a mandatory restart or next stage.
- [x] Provide conditional guide link in the **existing** Learning/Reconciliation Policy at material durable delta/cross-episode scope, without replacing its dispositions or generating a universal learning artifact.
- [x] Add first-load pointer to `strategic-repository-analysis/SKILL.md` / `using-sensemaking/SKILL.md` **only if** a concrete responsibility-selection decision cannot be made from existing first-load policy/pointers. Otherwise avoid core Skill churn.
- [x] Review `docs/strategic-repository-sensemaking-v1.md`, `strategic-continuity-v1.md`, `capability-learning-loop-v0.md` for minimal source-reference need; leave unchanged where no reader need is demonstrated.
- [x] Confirm via installed-profile and packaging source that the guide lives in the selected entrypoint Skill directory; check exact-commit wheel profile path where feasible, distinguish packaging from actual host invocation.
- [x] Leave `strategic-repository-reconciliation/SKILL.md`, canonical contracts, runtime and default public Skill names unchanged absent a demonstrated consumer ambiguity.

**Done when:** existing Skills can find the relevant guide *selectively* and no expanded stage, required form, duplicated authority or broken installed link is introduced.

### Task 9 — Explicit GO/NO-GO for reviewed machine knowledge

**Prerequisite:** Tasks 5–8. **Output:** justified `NO_NEW_KNOWLEDGE_PACK` in closeout *or* minimally justified, valid existing-schema pack (and separately bounded PR).

- [x] Identify one precise future agent query/re-entry need not adequately answerable by current strategic files, retained history, source links, optional guide and already-indexed knowledge.
- [x] If no gap is material, record **`NO_NEW_KNOWLEDGE_PACK`** and leave `.sensemaking/knowledge/` untouched. **This completes Task 9.**
- [ ] **Only if GO:** inspect supported `schema_version: 1` kinds, allowable relations, provenance and current archived records; choose an existing legal kind rather than inventing `LearningAccount` or `StrategicEvolutionRationale` as parsed kinds.
- [ ] **Only if GO:** add the smallest source-grounded reviewed definition or cross-reference needed for an actual `search/explain/context-for` consumer, preserving each historical report revision and identity.
- [ ] **Only if GO:** inspect index and actual retrieval behavior at the candidate commit; check missing-source and omission semantics; do not treat successful graph navigation as causal truth or agent benefit.
- [ ] **Only if GO:** if required meaning cannot be expressed by current schema safely, stop and prepare **separately justified compatibility/schema discussion**, not silent evolution of v1.
- [x] Keep all generic experiment infrastructure, automatic doctrine promotion, semantic scores, history rewriting and universal memory files out of scope.

**Done when:** a justified source-only/guide-only NO-GO exists, or a minimal useful existing-schema consumer projection is actually checked; no optional pack is necessary to claim documentary ontology completion.

### Task 10 — Integrated source/contract review, validation, merge and closeout

**Prerequisite:** Tasks 0–9, where Task 9 NO-GO is a legitimate result.

- [x] Review implementation PR diffs and ensure edits are confined to intended ontology, portable guide, optional case/knowledge and minimal navigation paths; no unexpected product/ADR, schema, runtime or status authority change.
- [x] Review historical A–E against original source artifacts, recorded analyzed revisions and negative-case interpretations; F remains labeled normative.
- [x] Verify local `SEL-CQ` expected answers against source; record `ANSWERABLE`/`PARTIAL`/`NOT_ASSESSED` without conflating documentary fitness with autonomous agent qualification.
- [x] Check actual relevant file links, source IDs, original typed entities and assessed vs report revisions; if linked files are missing, repair the documentation without inventing identities.
- [x] Verify no altered semantics/validators of `strategic_repository_analysis`, `strategic_reconciliation`, Strategic Continuity, Knowledge Schema v1, Connected Prospective Inquiry or core Warrant/Choice/Policy Hierarchy.
- [x] Inspect actual installed guide packaging path and existing hosted checks. Use source/diff and relevant non-test mechanical checks per current `CLAUDE.md`; record any local unit/synthetic test as `NOT_RUN` unless policy changes.
- [x] Make short source-grounded decision note and exact file list for each PR; follow current owner-directed branch/merge policy after clean review, preserving protections and actual pending/failed CI states.
- [ ] If post-merge hosted CI identifies a material failure, assess/repair that original failure as a bounded follow-up before claiming completion.
- [x] Update `STATUS.md` only if a material implemented capability changed; do not replace current PATH-1 strategic responsibility merely because the ontology exists.
- [x] Produce a final existing `sensemaking_session_receipt` only for actual implementation, exact source/authority/review evidence, NO_GO decisions, current status and unqualified later-agent value.
- [x] Conclude `GOAL_SATISFIED` (documentary implementation), a real source/authority blocker, or a specific unresolved gap. Do not proceed into empirical trials, machine causal models or self-updating strategy absent an independently warranted responsibility.

**Done when:** the shared conceptual model, two profiles, cases, competencies, portable conditional guidance, evidence/authority ceilings and implementation history are reconstructible; appropriate source/packaging checks are honestly qualified.

## E. Proposed implementation PR boundaries (only after separate implementation authorization)

| Increment | Tasks | Change scope and merge condition |
| --- | --- | --- |
| **PR A — Semantic core** | 0–4 | Shared ontology and differentiated profiles, source identifiers, exact existing producer/consumer/Level-3/4 constraints. Accept after source/contract review; no new parsed schema/Skill. |
| **PR B — Cases + competencies** | 5–6 | Historically pinned cases, clearly normative comparison, twenty local questions and negative controls. Accept when original source and uncertainty can be independently reconstructed at documentary level. |
| **PR C — Portable guidance and integration** | 7–8 | Self-contained Skill reference, optional template and minimal conditional pointers. Accept after installed source-path check and no mandatory workflow/producer duplication. |
| **PR D — Reviewed knowledge, conditional** | 9 | **Default NO_GO, omit PR.** Proceed only for an identified actual retrieval question and a legal existing-schema representation. |
| **PR E — Evidence and closeout, only if needed** | 10 | Real-path check/qualification note, factual status update and actual implementation receipt. Accept without overstating independent value or ratifying strategy. |

Merge low-risk adjacent increments if this produces a clearer smaller diff and preserves reviewability. Never treat PR letter/order as an automatic procedure for an ordinary later Sensemaking user task.

## F. Twenty local competency questions to implement

| Local ID | A competent agent should be able to answer |
| --- | --- |
| `SEL-CQ-01` | Which governing purpose, beneficiary, original typed target, actor and **assessed repository revision** frame this evolution question? |
| `SEL-CQ-02` | Is a proposed improvement a genuinely different desirable user end, an enabling capability, a technical mechanism, simplification/retirement or routine repair? |
| `SEL-CQ-03` | What present-source capability/relationship/constraint and conditional mechanism make this future plausible rather than manufactured? |
| `SEL-CQ-04` | Are proposed construction alternatives materially different futures, interchangeable variants, or one path with optional components? |
| `SEL-CQ-05` | What outcome makes the opportunity valuable for a named beneficiary, and which benefit remains hypothesized? |
| `SEL-CQ-06` | How do commission risk, **omission/deferral cost**, reversibility and alternative simplification affect strategic direction? |
| `SEL-CQ-07` | Which comparison is about exploration priority, strategic attractiveness or actual implementation order—and which other comparisons remain untouched? |
| `SEL-CQ-08` | What is the Level-3 strategic analysis conclusion, if any, and what owner/Level-4 decision or separate action authority remains reserved? |
| `SEL-CQ-09` | Which assumption/evidence change would make the chosen or recommended evolution rationale wrong, conditional or no longer relevant? |
| `SEL-CQ-10` | When is `NO_CHANGE`, zero construction paths, a deferred option or an owner decision more warranted than inventing more strategy? |
| `SEL-CQ-11` | What **previous explicit understanding**, dated source and assessed revision is the new result being compared against? |
| `SEL-CQ-12` | Did the **repository/world change**, did only **our interpretation change**, or did **governing owner intent change**? Which source supports the distinction? |
| `SEL-CQ-13` | Is the learning grounded in observation, analyzed source, conditional derivation, creative hypothesis, reported experience or owner decision, and what claims remain unsupported? |
| `SEL-CQ-14` | Which prior claim/assumption/uncertainty/responsibility was confirmed, revised, invalidated, left unchanged or made irrelevant—and why? |
| `SEL-CQ-15` | Which historical lesson remains applicable, which counterexample changes its scope, and when should a later agent source-check, narrow or reject it? |
| `SEL-CQ-16` | Was a lesson merely retained or retrieved, actually source-checked, used in a decision, followed by observed outcome, independently reused or comparatively beneficial? |
| `SEL-CQ-17` | Does changed interpretation reopen a *new future question* while leaving product demand, strategic preference and authority unestablished? |
| `SEL-CQ-18` | Is an update local `Learning/Reconciliation`, purpose-relative Convergent Reassessment, a warranted canonical `strategic_reconciliation`, or a genuinely reopened Level-3/Level-4 question? |
| `SEL-CQ-19` | Does a repeated cross-episode pattern generalize across contexts, survive counterevidence and justify *a candidate* doctrine change rather than automatic Skill modification? |
| `SEL-CQ-20` | What can a source-literate reader truthfully conclude, what is still `NOT_ASSESSED`, what warrants stopping or reopening, and who can authorize the next action? |

## G. High-risk scenarios and negative controls

| Scenario | Correct behavior | Prohibited inference |
| --- | --- | --- |
| A missing code capability has no material beneficiary/outcome impact | Record local repair/maintenance or defer; assess strategicity separately | "Missing" becomes "strategically highest priority" |
| A technically distinct implementation changes no user end or capability | Identify it as mechanism/option within a purpose-relative future | Manufacture a separate future product goal |
| New user experience is imaginable but not yet built | Preserve as grounded hypothesis with assumptions, value/authority gaps | Call it implemented, validated user demand or owner-selected thesis |
| A new code patch closes a bounded source finding | Source-reconcile world changed and verified claim only; strategy may stay intact | Automatically reopen strategic frontier or change Level-4 purpose |
| A discovery reveals capability already implemented | Correct interpretation and past assumption without claiming a new code capability | Fabricate new implementation progress |
| The owner changes the primary intended beneficiary | Attribute a governing-intent change to actual owner/ADR | Classify it as agent-inferred empirical truth |
| Returned evidence weakens one PATH-1 assumption | Revise exact assumption, possibly retain PATH-1 and untouched alternatives | Rewrite history or automatically select PATH-2 |
| A pairwise inquiry preference changes | Keep original global portfolio and separate purpose/authority | Rename it strategic/product/implementation priority #1 |
| A past lesson is retrieved in different architecture | Check current mechanism/conditions; narrow or reject if inapplicable | Historical precedent becomes mandatory rule |
| Several same-repository incidents share a symptom | Evaluate distinct root causes and contrary cases; local candidate lesson | Assume an independent cross-repository causal law |
| Guide and ontology are merged and hosted checks pass | Report source/installation qualification at correct level | Claim independent agent creativity or beneficial host application |
| No consequential new evidence arrived | `NO_MODEL_CHANGE` or no extra learning account is valid | Force a revised strategy, new question, new ledger file or implementation |

## H. Completion contract and optional future inquiry

**Documentary implementation goal satisfied when:**

1. One shared conceptual spine identifies the two roles, correct original entities, decision/evidence/authority boundaries and three learning scales.
2. Strategic Evolution Analysis makes future user ends, capability mechanisms, alternative paths, simplification, omission risk, no-selection and Level-3/4 scope legible without a numeric strategy engine.
3. Learning & Reassessment makes world change, interpretation change, governing-intent change, unchanged beliefs, source applicability, creative reframing and doctrine-generalization thresholds legible without a new policy.
4. Both roles use current `strategic_repository_analysis`, `strategic_reconciliation`, Strategic Continuity and existing connected-inquiry/knowledge identities rather than competing with them.
5. All twenty local competencies have source-specific answers or honest ``PARTIAL` / `NOT_ASSESSED`, historical cases A–E retain original source identity, and normative F cannot be mistaken for an observed event.
6. Portable guidance can be found conditionally through existing entrypoint/SRA/learning references; relevant source paths and package evidence are checked without implying host application.
7. Reviewed knowledge additions are minimal and **consumer-justified—or absent after explicit NO_GO**.
8. Actual work and verification claims are reconciled, status/strategy are not silently changed, and a legitimate stop is recorded.

**Specifically not proved:** higher-quality real strategic choices, greater independent creative novelty, causal direction from a graph, real user desire for a new future, cross-repository transfer success, host invocation, a self-updating learning system, a valid owner thesis change, changed product-market value, new automatic work authorization or improved AI weights.

**Possible later independent question:** When a capable coding agent faces a genuinely new repository evolution or learning/reassessment decision, does this new guidance actually change the sourced rationale, application of historical evidence or selection compared with a source-only agent, while preserving owner authority? Only a separate authentic task and observation can support an answer. Do not manufacture that study as a dependency for the documentary v1 ontology.


## I. Implementation, knowledge-retention decision and review reconciliation — 2026-11-05

**Owner authorization:** explicit request after merged planning PR #753: implement all tasks, proceed without further input, choose repository-answerable intermediate decisions. Authority covers the bounded conceptual/Skill-reference changes and ordinary repository PR merges under current `CLAUDE.md`; it does not ratify new product theses, owner preferences, external publication or release/deployment.

### Merged increments and actual artifacts

| PR | Merged change and evidence scope |
| --- | --- |
| [#754](https://github.com/ThorStarlord/sensemaking-skills/pull/754), merge `6f97cdeb79e9777967c9f3029dd1f13768367b17` | [Conceptual Strategic Evolution & Learning ontology](../../semantic-architecture/strategic-evolution-learning-ontology.md), two shared documentary roles and source/evidence/authority spine, with distinct future end versus mechanism and world/interpretation/owner delta. Six conceptual sections, source references reviewed; no schema, strategic authority or new artifact producer. Hosted Product Validation **PASS** and Release Candidate Distribution **PASS** (PR head `0be1b1745133ad242ce5fd640444b0b44b30ad57`). |
| [#755](https://github.com/ThorStarlord/sensemaking-skills/pull/755), merge `f4750260ebc14a34f3c6bf14b1fdddab0516f5d4` | [Reference cases](../../semantic-architecture/strategic-evolution-learning-reference-cases-v1.md) A–E (original dated reports) plus F (**NORMATIVE**), source-qualifying [SEL-CQ-01–20](../../semantic-architecture/strategic-evolution-learning-competency-v1.md) and 12 negative controls. Original source revision and current report snapshot differentiated; no historical rank/product claim changed. Hosted Product Validation **PASS** and Release Candidate Distribution **PASS** (PR head `954b1f8797e674ae00e8ae9934c77596fbbdb107`). |
| [#756](https://github.com/ThorStarlord/sensemaking-skills/pull/756), merge `c356afaff29a3363ac5a5ffb9356e0e98df5eee1` | [Portable conditional guide](../../../skills/strategic-repository-analysis/references/strategic-evolution-learning-v1.md), [optional sparse record](../../../skills/strategic-repository-analysis/references/strategic-evolution-learning-record-template.md) and six minimal source index/Skill-reference crosslinks. Existing `using-sensemaking` core/strategic reconciliation producer left unchanged. Hosted Semantic Context Re-entry **PASS** at PR head `ab241bf22cf8733fce9f53b4a02d5d3772fbc195`; Product Validation / Release Candidate Distribution **IN_PROGRESS at last check**, not claimed passing before completion. |

### Task 9 — explicit retained knowledge NO-GO

**Decision: `NO_NEW_KNOWLEDGE_PACK`.**

**Consumer question assessed:** Can an agent recover a strategy's accepted end, source-current capability basis, conditional PATH-1/PATH-2 preference, subsequent source-qualified `ASSUMPTION-1` learning delta, distinct cross-episode lesson mechanisms, and the scope/authority of a newly delivered documentary capability using the existing strategic sources plus an installed guide? **Yes at the source-documentary level.** The six source-annotated cases, 20 local competency answers, current `strategic_repository_analysis` and `strategic_reconciliation` contracts, and the installed reference provide those meanings without inventing graph type IDs.

No observed `search/explain/context-for` consumer failure or material re-entry gap specifically requires mirroring the new conceptual role labels and historical interpretations as `.sensemaking/knowledge/strategic-evolution-learning.json`. Duplicating the same source claims would increase maintenance/currentness burden without established semantic or retrieval benefit. Retaining documentary account names as JSON predicates would falsely enlarge schema-v1 authority. Thus **no knowledge pack, index build, new queries, parser, validator, migration or knowledge promotion** was introduced. The four "Only if GO" actions stay unchecked **intentionally and legitimately not applicable**, not failed attempts.

A future real source/agent retrieval miss with source-cited consumer need may warrant a separate existing-schema patch under current source/authority rules, but this implementation does not manufacture one.

### Task 10 — review evidence and claim ceilings

| Check | Actual result |
| --- | --- |
| Governing and source baseline | **SOURCE_REVIEW_COMPLETE:** `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `docs/product-strategy.md`, `STATUS.md`, ADR/product intent context and planned source/strategic/learning ontology contracts were reviewed at `main@095ae3fdaec229bb5d2d49e7fe5a95969f8ab22e` before the first construction PR. Original historical reports carry separate analyzed target revisions. |
| Canonical machine producers and authority | **SOURCE_REVIEW_COMPLETE:** current `strategic_repository_analysis` v2, `strategic_reconciliation`, Strategic Continuity, existing Learning/Reconciliation and connected-inquiry semantics retained. No production code, validator, schema, Knowledge v1, Level-3 PATH-1, ADR or Level-4 product strategy changed by the three implementation PRs. |
| Historical source cases/competency author review | **DOCUMENTARY_FIT:** A–E source-bound, F labeled normative, SEL-CQ-01..20 with explicit `ANSWERABLE`, `PARTIAL` and `NOT_ASSESSED` claims. No independent model/agent experiment conducted; no novel user demand or cross-repository doctrine benefit established. |
| Changed-file/diff review | **PASS (source inspection):** PR #754 one new ontology file; #755 two new semantic-architecture files; #756 two portable reference files plus six existing documentation/reference pointers, exactly the bounded planned paths. All source-link target paths explicitly checked where material; unbounded link crawl and independent host loading were not demonstrated. |
| Source packaging/profile path | **PASS (source inspection):** `src/sensemaking_skills/defaults/install-profiles.yaml` entrypoint includes `using-sensemaking` and `strategic-repository-analysis`. `setup.py` copies canonical `skills/` to packaged `skill_trees`; `setup_skills.py` installs selected Skill directories whole. New guide and optional record live in that tree. |
| Separate isolated exact-commit local wheel install | **NOT_RUN**. Source packaging and hosted distribution are distinct; neither proves the active host loaded or used the reference. |
| Local unit/synthetic evidence tests | **NOT_RUN** under current repository owner-directed `CLAUDE.md` construction exception. No local tests created or added, and existing hosted CI/protections were preserved. |
| Hosted PR #754 | **PASS** Product Validation and Release Candidate Distribution at exact PR head; PR merged after source/diff review. |
| Hosted PR #755 | **PASS** Product Validation and Release Candidate Distribution at exact PR head; PR merged after source/diff review. |
| Hosted PR #756 | Semantic Context Re-entry **PASS**; Product Validation and Release Candidate Distribution **PENDING at closeout authorship**, pending results should be checked later and any material failure handled as a separate warranted repair. Do not report PASS before observed. |
| Independent later-agent reasoning, capability learning or user/product value | **NOT_ASSESSED**. Historical source reconstruction, source-profile reachability and CI do not prove agent-guidance invocation/application, better strategic choices, owner-valued product ends, causal semantic graphs or transferable doctrine. |

**Result:** ``SOURCE_DOCUMENTARY_GOAL_SATISFIED`: the conceptual two-profile ontology, full source cases and 20 competencies, portable conditional guide, optional template and no-duplicate producer/authority boundaries exist on `main`. No Level-3/Level-4 strategy reopening or doctrine mutation is warranted solely because the ontology was added. ``NO_MODEL_CHANGE` to accepted strategic PATH-1. This closeout is not a new product-thesis decision, an empirical qualification certificate, or automatic authorization to run future inquiries.

**Explicit stop / re-entry:** stop now after documenting the actual receipts and qualification ceiling. If a later genuinely independent agent fails to recover/apply the guide, source context changes materially, or repeated counterexamples defeat the semantics, return through normal Sensemaking responsibility selection and source-grounded learning; do not blindly rerun the whole ontology program.

**Post-merge CI conditional:** the "If post-merge hosted CI identifies a material failure" item remains open while checks on #756 are pending; it is not a blocker to merging this documentation under the active source-review-first repo policy. A later material failure warrants finding-specific repair; no hypothetical successful check is invented.
