# Connected Prospective Inquiry Ontologies v1 — Detailed Implementation Plan

> **Implementation record:** The owner subsequently authorized implementation. The implementation source, reviewer limitations and remaining unqualified claims are recorded below. Future changes must still refresh HEAD, governing instructions, evidence and authority; this plan does not grant reusable authorization.

**Goal:** Build a coherent, reusable **Level-2 conceptual ontology with four conditional inquiry profiles**—Focused Depth Exploration, Convergent Reassessment, Adversarial Review and Architecture Synthesis—so future agents can reconstruct how conditional consequences affect judgments, how substantive challenges affect proposals, and why design elements serve an intended product outcome.

**Selected design:** One shared conceptual spine; four semantically distinct profiles; bounded source-pinned cases and competency questions; a single optional, self-contained portable guidance/reference and lightweight record template; minimal conditional Skill/navigation integration. Existing prospects, claims, assessments, decisions, architecture synthesis, PRD and authority surfaces keep their meanings. No executable model or new Skill in v1.

**Spec:** [Connected Prospective Inquiry Ontologies v1 — Design Basis](../specs/2026-11-05-connected-prospective-inquiry-ontologies-design.md).  
**Planning baseline:** `ThorStarlord/sensemaking-skills@6fa8d05f3845ac7c06cf4ef7127ef0d9f164d405` on 2026-11-05. The previous Convergent Direction Selection ontology and PRs #742/#743/#745/#747 are already merged.  
**Plan status:** **IMPLEMENTED (documentary v1) — 2026-11-05**, in PRs **#749 (ontology), #750 (cases and competencies), #751 (portable guide and conditional integration)**; final validation/receipt in closeout PR. The checklist below records work actually performed; optional knowledge/schema work legitimately ended **NO_GO**, while local unit/synthetic tests and a separate local isolated wheel install remained **NOT_RUN**. Hosted Product Validation, Release Candidate Distribution and Semantic Context Re-entry for PR #751 passed.  
**Technology:** Markdown, existing installed Skill/reference paths, existing `schema_version: 1` reviewed-knowledge JSON only if necessary, current local semantic knowledge CLI, GitHub PR and existing hosted validation. No added runtime dependency.

## A. Owner decisions incorporated

1. **Conceptual scope:** design all four profiles together and preserve shared identities. Do not create independent ontology vocabularies that duplicate `ConsequenceHypothesis`, `AssessmentRevisionAccount`, `Decision`, or `ArchitectureOption`.
2. **Depth question:** a consequence structure captures causal/enabling conditional links and their limits, not an asserted predictive engine or a required depth count.
3. **Reassessment:** reuse `AssessmentRevisionAccount` and priority/selection semantics. Permit reasoned `NO_CHANGE`, a changed rationale or narrowed conditions without a new rank. Do not rewrite historical snapshots.
4. **Adversarial challenge:** preserve each target/challenge/response/residual question; objections are not automatic vetoes or demonstrated defects.
5. **Synthesis scope:** one coherent **product-and-technical design proposal**, with PRD and architecture-specification views where warranted. Preserve existing `architectural_synthesis` as multi-option **provisional comparison** and `to-prd` as the current canonical PRD capability.
6. **Formalization:** conceptual/documentary first. Machine schema, predicates, stage routing, scoring and new executable artifact IDs require an evidenced producer/consumer and separate authorization. No graph-causal inference.
7. **Adaptive operation:** these are conditional responsibilities, never a fixed pipeline, automatic handoff, public Skill expansion or implementation authorization.
8. **Plan-only boundary:** this plan commits no ontology changes, product choice, roadmap change, PRD adoption or implementation. The implementation may proceed later under explicit delegation.

## B. Governing constraints

- **G1 — Product identity:** Follow `CONTEXT.md`, `docs/product-strategy.md`, accepted ADRs 0029/0031/0034 and current `STATUS.md` without reopening Level 4 or silently replacing Level 3.
- **G2 — Current sources first:** Read `AGENTS.md`, `CLAUDE.md`, the previous ontology plan, current Skill references, artifact contracts, actual source examples and current branch at execution. Pin the assessed source revision separately from the report revision.
- **G3 — Shared target identity:** Keep existing `poss:`, `arch:`, `conseq:`, source-local IDs, path identities, and `Decision` authority. Document grouping or documentary crosswalks without inventing `sameAs` equivalence.
- **G4 — Epistemic care:** Keep observed premises, logical conditional consequences, causal hypotheses, creative opportunities, assessments, sourced decisions and verified post-change outcomes distinct. `A may produce B` plus `B may enable C` is not `A produces C`.
- **G5 — No false authority:** A suggestion, rank, selected direction, PRD/spec, validation PASS or reference pointer never grants execution, merge, Level-4 ratification or other protected action.
- **G6 — Existing endpoint restrictions:** Do not widen executable `ComparativeJudgment evaluates`, `ProvisionalPreference prefers` or `Decision selects` beyond their current architecture/path definitions by analogy.
- **G7 — No new obligatory ceremony:** A short source-grounded report is sufficient when cross-session durable extra structure would be wasteful; no mandatory records, forms, transitions or standalone consequence artifact.
- **G8 — Lossless negative outcomes:** Preserve meaningful `NO_CHANGE`, `NO_SELECTION`, incomparable, unresolved, invalid consequence chain, objection not sustained, no design, no new possibility and `NOT_ASSESSED` outcomes.
- **G9 — PRD/design separation:** Do not equate product requirements with architectural choices, or an architecture specification with an implementation plan. A coherent proposal may still be unratified.
- **G10 — Source-specific review:** Independent documentary reconstruction is useful only at its appropriate claim ceiling; structural validity and historical examples do not demonstrate benefit for independent new agents.
- **G11 — Change boundaries:** Do not modify historical portfolio rankings, original Depth reports, old ADRs, Idea Library dispositions, contract/schema/runtime, existing PRD and architectural-synthesis validators, or accepted product strategy just to satisfy a conceptual ontology.
- **G12 — Local build policy:** At planning baseline, `CLAUDE.md` says no locally added/run unit or synthetic evidence tests for current construction PRs. Perform source/diff inspection, justified mechanical/source checks and existing hosted verification where warranted; state `NOT_RUN` accurately. Merge authorized PRs promptly after clean review without bypassing required protection or knowingly dangerous failures.
- **G13 — Retention:** Selective existing-schema reviewed knowledge only when useful to a real reader/query, grounded in source; no bulk candidate promotion or invented demonstrated benefit.
- **G14 — Stop:** When the documentary semantics, reference cases, conditional agent guidance and evidence ceilings are reconstructible, stop; do not continue building a graph compiler because the conceptual drawing has arrows.

## C. Deliverables and precise file map

### New deliverables, core scope

| Path | Content and consumer |
| --- | --- |
| `docs/semantic-architecture/connected-prospective-inquiry-ontology.md` | Shared identity/envelope/relations, plus four separate profile chapters with limits and feedback; central Level-2 conceptual module for source-reading agents. |
| `docs/semantic-architecture/connected-prospective-inquiry-competency-v1.md` | Sixteen local competency questions, answer sources, fit review, negative cases and explicit evidence ceiling. |
| `docs/semantic-architecture/connected-prospective-inquiry-reference-cases-v1.md` | Historical source-pinned cases and clearly marked normative counterexamples spanning all four profiles. |
| `skills/strategic-repository-analysis/references/connected-prospective-inquiry-v1.md` | Installed standalone, conditional four-profile guidance; does not depend on reading this repo's `docs/` in target installs. |
| `skills/strategic-repository-analysis/references/connected-prospective-inquiry-record-template.md` | Optional sparse Markdown evidence/reasoning record, **not** a new registered artifact; sections omitted when immaterial. |

This is **one ontology file with four internally distinct profiles**, avoiding five nearly duplicate documents. Split a profile into a separate document only if real navigation or maintenance evidence warrants it, and preserve links/identity.

### Conditional new deliverable

| Path | Only if warranted |
| --- | --- |
| `.sensemaking/knowledge/connected-prospective-inquiry.json` | Existing `schema_version: 1` declared concepts + accurately sourced historical case(s) + supported `references`; omit entirely if current index/search and source pointers suffice. No new executable predicates. |

### Existing files: only minimal justified edits

| Path | Allowed change |
| --- | --- |
| `docs/semantic-architecture/README.md` | Index ontology, cases, competencies and portable reference. |
| `docs/semantic-architecture/ontology.md` | Link a single cross-layer specialization; preserve `Decision` and existing target types. |
| `docs/semantic-architecture/competency-questions.md` | Link the new *local* CPI-CQ set without allocating global CQ numbers. |
| `docs/semantic-architecture/relations-and-epistemics.md` | Crosswalk documentary relations, explicitly not new machine predicates. |
| `docs/semantic-architecture/prospective-reasoning-ontology.md` | Short cross-reference at activity/consequence/feedback boundary only; no endpoint change. |
| `docs/semantic-architecture/possibility-assessment-ontology.md` | Link to consequence-informed bounded reassessment, retaining existing assessment meaning. |
| `docs/semantic-architecture/convergent-direction-selection-ontology.md` | Bounded reconsideration pointer; no selection/authorization change. |
| `skills/using-sensemaking/SKILL.md` | At most one first-load conditional pointer **if** it changes responsibility choice. Otherwise keep unchanged. |
| `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md` | Conditional guide pointer without creating an expected next stage. |
| `skills/repository-semantic-steward/references/architecture-exploration.md` | Link to cross-profile traceability where the option decision genuinely needs it. |
| `skills/to-prd/SKILL.md` | Usually unchanged; only a bounded cross-reference if producer/consumer ambiguity is observed. |
| `docs/explorations/README.md` | Optional link to cases; leave dated original exploration reports unchanged. |
| `STATUS.md` | Only a materially implemented and source-reviewed capability note; never replace current Level-3 next responsibility because of a documentation module. |
| Existing receipts | New receipt only for actual implementation under existing contract, never as a replacement for substantive reports. |

## D. Workstreams, checks and dependency gates

### Task 0 — Refresh currentness, ground authority and finalize exact file ownership

**Deliverable:** one source/consumer inventory in the ontology draft or implementation PR decision note; no separate permanent inventory required.

- [x] Read current `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `docs/product-strategy.md` and `STATUS.md` and record actual execution HEAD.
- [x] Confirm accepted ADR 0029/0031/0034 and latest changes to the convergent selection ontology.
- [x] Inspect the prospective, possibility-assessment, convergent-selection, product-possibility and layered ontologies for concept collisions.
- [x] Check exact `architectural_synthesis`, `prd`, `architectural_review_recommendation` and `strategic_reconciliation` producer/consumer fields in current `artifact-contracts.yaml`.
- [x] Check whether relevant conditional guide/template paths or proposed ontology files already exist on execution HEAD; adapt rather than duplicate.
- [x] Verify historical cases at their original assessed revisions; do not represent source-provided interpretations as freshly observed effects.
- [x] Record high-level decision: connected documentary profiles warranted; executable schema/Skill/runtime not warranted by these sources alone.

**Done when:** source-of-truth, currentness, producers, existing identifiers and non-goals are explicit.

### Task 1 — Shared semantic spine and four-profile boundaries

**Prerequisite:** Task 0.

- [x] Create `connected-prospective-inquiry-ontology.md` with status, authority, scope and compact map of the four decision questions.
- [x] Define a shared assessment envelope using existing `ExplorationFrame`/`AssessmentFrame`, original target identity, author/date, source ref, assessed revision, constraints, epistemic status and stop/re-entry.
- [x] Define the **activity versus entity** distinction and the reason one option can survive exploration, reassessment, review and synthesis unchanged.
- [x] Define only necessary new *documentary roles*: `ConsequenceStructure`, `ChallengeResponseAccount`, `DesignRationaleView`; reuse `AssessmentRevisionAccount`.
- [x] Explain that a role may be represented by a section of an existing report, not a graph class or executable artifact.
- [x] Define proposed relations in prose with subject/object meaning, grounding requirement and non-inference warning.
- [x] Record explicit boundaries among evidence, plausible mechanism, conditional logical entailment, creative possibility, preference, authority and actual outcome.
- [x] Record existing relation endpoint restrictions, non-transitive causal chain rule and no `sameAs`/identity-collapse rule.
- [x] Define adaptive composition: any profile can run or be skipped; challenge/reassessment/depth may revisit earlier reasoning without automatic transitions.
- [x] Add a short glossary for `portfolio reassessment` versus `strategic reconciliation` versus `Decision` reconsideration.

**Done when:** a reader can distinguish the four activities from the entities they examine, without believing a new engine or authority was created.

### Task 2 — Focused Depth Exploration / conditional consequence structure

**Prerequisite:** Task 1.

- [x] State the minimal inquiry target: one concrete premise/capability/relation, beneficiary, horizon, target revision and closest predecessor.
- [x] Reuse `ConsequenceHypothesis` where its identity/role is appropriate; support non-architecture premises as documentary source-linked explorations.
- [x] Describe first-order effect, multi-step propagation, interactions, systemic feedback, counterfactual forks, non-effects and unknowns **without depth quotas**.
- [x] Require an intelligible proposed mechanism and assumptions **for each consequential link**; distinguish enabling, constraining, causal and merely chronological descriptions.
- [x] Trace affected beneficiaries, benefits/harms and incompatible goals where material.
- [x] Provide a negative case of unsupported transitive inference: `A may B` and `B may C` do not establish `A causes C`.
- [x] Explain consequence-to-opportunity return: new question or hypothetical `poss:` candidate is not automatically curated, preferred or authorized.
- [x] State stopping criteria: decision-relevant branches sufficiently understood, empirical ceiling reached, no meaningful cascade, or more speculation would not help.

**Done when:** the profile can represent a convincing consequence, a broken link, a counterfactual fork and a useful `NO_FURTHER_DEPTH` outcome.

### Task 3 — Convergent Reassessment / attributed judgment revision

**Prerequisite:** Tasks 1–2.

- [x] Define reassessment target: original comparison/judgment/portfolio or genuine sourced decision, with its frame and assessed revision.
- [x] Reuse `AssessmentRevisionAccount`, `PortfolioSnapshot`, `AssessmentJudgment`, `SelectionReconsiderationBoundary` and Learning/Reconciliation.
- [x] Preserve difference among inquiry learning priority, strategic attractiveness, implementation priority and owner-adopted strategy.
- [x] Explain how a newly considered consequence affects a criterion, assumption, prerequisite, beneficiary or choice frame.
- [x] Distinguish same rationale/no change, narrowed conditional preference, new grounds same preference, pairwise reorder, unresolved/incomparable, incomplete options and appropriately authorized decision reconsideration.
- [x] Preserve the predecessor and unaffected portfolio members; no retrospective rewriting or global ranking from a local pairwise change.
- [x] Include nonselection/authority-needed and no-new-decision outcomes.
- [x] Show one reassessment that changes **conditions**, not ordinal rank.

**Done when:** a reader can reconstruct exactly what changed and why, without believing the portfolio was automatically reselected.

### Task 4 — Adversarial Review / target–challenge–response

**Prerequisite:** Task 1; integrate with Tasks 2–3.

- [x] Define the reviewable target types: claim, assumption, consequence link, comparison, proposed architecture, requirement, contract, scope or closure claim.
- [x] Define `ChallengeResponseAccount` as an attributed documentary role with source/counterevidence and the actual failure or inference pathway.
- [x] Distinguish current contradiction, source gap, hypothetical failure scenario, misunderstood authority, missing consumer and valid alternative value frame.
- [x] Record challenge strength as qualitative **grounds and epistemic class**, never automatic score/probability.
- [x] Define response: concede, refute with source, narrow claim, revise design, request bounded evidence, defer knowingly, or retain unresolved risk.
- [x] Explain how to judge whether the response actually addresses its original target; proposed repair is not finding-specific verification.
- [x] Account for new consequences introduced by a response, with conditional links back to Depth Exploration and Reassessment.
- [x] Respect current `architectural-review` input contract; do not turn the profile into another review Skill/validator.
- [x] Include negative cases: unsupported fear called observed defect; change to software offered as proof of creative user value; critic recommendation treated as veto.

**Done when:** a returning agent can distinguish objection, evidence, response and remaining risk for the exact target.

### Task 5 — Architecture Synthesis / traceable product-and-technical proposal

**Prerequisite:** Tasks 1–4.

- [x] Define `DesignRationaleView`: a purpose-relative trace from intended beneficiary/outcome to requirement, design responsibility, component/boundary/contract proposal and unresolved challenge.
- [x] Specify coherence checks: consistent assumptions, interactions, ownership, interface contracts, non-goals, conflicting dependencies, reversibility, operational consequences and review status.
- [x] Distinguish **coherent design proposal** from `architectural_synthesis` multi-option comparison and from an adopted decision.
- [x] Distinguish PRD view, architecture/technical-spec view and separately authorized implementation plan.
- [x] Reuse `to-prd` for canonical `prd`; preserve `source_intent_ref`, scope-expansion approval and current acceptance-contract meanings.
- [x] Reuse `architectural_synthesis` where actual multi-option comparison must persist; do not change its mandatory options or validator.
- [x] Represent source-to-requirement, consequence-to-constraint and challenge-to-design revision **as explanatory links**, not machine-observed dependencies.
- [x] Include design alternatives, rationale, unresolved decisions, acceptance conditions and conditions for reopening.
- [x] Include a negative example: detailed architecture without product value or a claimed final approval from a provisional preference.

**Done when:** requirements and technical design can be traced to the underlying reasoning without implying they are implemented or owner-ratified.

### Task 6 — Historical source cases, negative examples and competencies

**Prerequisite:** Tasks 2–5.

- [x] Create the source-pinned reference-cases document, stating source/assessed revisions and historical versus normative status.
- [x] Case A: Discovery Memory synthesis; write/commit authority narrows A's preference without reversing its local order, and an opportunity remains hypothetical.
- [x] Case B: Situated knowledge consequences; false global contradiction versus invented contextual qualifier produce opposite risks.
- [x] Case C: Architectural-generativity portfolio; pairwise inquiry preference changes without rewriting the original overall ranking.
- [x] Case D: Graph activation synthesis; compare A/B/C, distinguish availability from application, challenge runtime-forced context without implying proven behavioral gains.
- [x] Case E (normative): coherent combined PRD/technical spec with distinct approval and implementation boundaries; do not falsely claim it occurred historically.
- [x] Cross-check at least one broken consequence chain, unaffected comparison, unsupported objection and rejected authority transfer.
- [x] Create `connected-prospective-inquiry-competency-v1.md` with CPI-CQ-01..16 and source-specific expected answers.
- [x] Include assessed-vs-report revision and disputed interpretations; do not fabricate independent trials or new ProductPossibility identity.
- [x] Record fit verdicts per question: `ANSWERABLE`, `PARTIAL`, `NOT_ASSESSED` with why; never invent PASS of agent benefit.

**Done when:** all profiles have at least one source-grounded case or honestly labeled normative boundary, and each competency has an inspectable answer source.

### Task 7 — Portable guide, optional record and adaptive consumption

**Prerequisite:** Tasks 1–6.

- [x] Write one self-contained installed guide `connected-prospective-inquiry-v1.md` with four separately titled conditionally invoked procedures and no dependency on this repo's source documentation in a target install.
- [x] For each profile specify the trigger, bounded target, source discipline, useful output, common drift, stop and return to agent-owned controller.
- [x] Write one optional sparse `connected-prospective-inquiry-record-template.md`; omit unneeded sections; it is Markdown, not a registered `artifact_id`.
- [x] Make appropriate distinctions among source observations, inferred effects, comparison, objections, proposed design and owner authority visible in both guide and template.
- [x] Add minimal cross-references in semantic README, ontology, competencies and relations; keep existing type definitions authoritative.
- [x] Add conditional pointer(s) in strategic funnel and Steward architecture exploration where they change a real handoff.
- [x] Touch `using-sensemaking/SKILL.md` only if naming the guide when first loaded materially improves responsibility selection; otherwise do not lengthen it.
- [x] Do not change `to-prd`, `architectural-review` inputs or required fields without a demonstrated producer/consumer need.
- [x] Inspect all linked references and ensure existing entrypoint or entrypoint+PM installer profiles package the files if they are intended to ship.

**Done when:** a fresh installed Skill reader can select the correct profile based on the question without the project docs, CLI, new runtime stage or forced four-step ceremony.

### Task 8 — Selective reviewed knowledge: explicit GO/NO-GO

**Prerequisite:** Tasks 1–7. **This step may end NO-GO with no file.**

- [ ] State one real retrieval/re-entry question that ordinary linked Markdown and already retained knowledge cannot answer conveniently.
- [x] If **no material retrieval gap**, document `NO_NEW_KNOWLEDGE_PACK` and leave `.sensemaking/knowledge/` unchanged.
- [ ] If warranted, inspect current source schema-v1 kinds/predicates and historical reviewed-knowledge shape before authoring.
- [ ] Select only stable definitions and accurately sourced case claims; no invented observed benefits or normalized causal graph edge.
- [ ] Retain document/revision/authority references, reviewed epistemic status and original example IDs.
- [ ] Use supported `references` links and clearly qualified conceptual attributes rather than introducing a causal/reconsideration predicate.
- [ ] Exercise existing proposal check, exact-source index build and `search/explain` consumer on the candidate commit where feasible; check failure and missing-source behavior honestly.
- [x] Keep knowledge pack optional: no bulk promotion, new kind, migration, CI workflow, library rewrite or semantic truth engine.
- [ ] If a real parsed consumer loses a decisive distinction, **stop** and write a separate compatibility/schema proposal instead of silently widening this v1 task.

**Done when:** there is either a justified omission or a minimal, source-grounded and actually consumable v1 knowledge projection.

### Task 9 — Real-path review, source reconciliation, delivery and closeout

**Prerequisite:** Tasks 0–8; Task 8's NO-GO is an acceptable completion.

- [x] Inspect every changed file/diff and confirm changes are confined to approved ontology, case, guide, optional knowledge and navigation surfaces.
- [x] Review every local CPI competency answer against the actual historic/normative source and document the reviewer's limitations.
- [x] Verify internal file links and exact source identifiers; material paths must resolve; historical source baselines stay distinguished from implementation HEAD.
- [x] Verify no previously accepted `ConsequenceHypothesis`, `Decision`, `architectural_synthesis` or PRD contract has been silently redefined.
- [x] Check the guide's packaging/installed-reference parity where installed references changed, ideally by exact-commit wheel + isolated entrypoint install, without asserting host application.
- [x] Run existing relevant non-unit mechanical checks / hosted validation under then-current repository instructions; record `PASS`, `FAIL`, `PENDING` or `NOT_RUN` distinctly.
- [x] Make a source-grounded decision note for each bounded PR, state scope/authority, and merge under current owner/project policy after clean review.
- [x] Update documentation navigation and `STATUS.md` **only** if a material capability/decision context changed; do not replace Level-3 responsibility by ontology completion.
- [x] Where actual implementation warrants, produce and validate the existing final `sensemaking_session_receipt` with source authority, actual work, pointers, stop and claim ceiling; never pretend planning work has completed implementation.
- [x] Record what remains unqualified: independent reader benefit, agent creativity, causal graph value, host invocation, product choice and end-to-end implemented design.
- [x] Conclude with source-grounded `GOAL_SATISFIED`, bounded open question or actual authority/external stopping condition. Do not launch an empirical trial solely to fill a checklist.

**Done when:** the reviewed installed documentary capability can be reconstructed; evidence and non-claims are honest; all implementation actions are reconciled.

## E. Suggested implementation PR boundaries (after separate authorization)

| Increment | Contains | Merge/acceptance boundary |
| --- | --- | --- |
| **PR A — Conceptual semantics** | Tasks 0–5: one shared ontology with four distinct profiles and explicit non-identities. | Source-reviewed definitions, no schema/authority drift. |
| **PR B — Competency and source cases** | Task 6: cases, 16 local questions and negative examples. | Each question source-answerable or honestly `PARTIAL/NOT_ASSESSED`. |
| **PR C — Portable consumption** | Task 7: installed guide/template and bounded pointers. | Installed guide self-contained; correct conditional trigger; no new public Skill. |
| **PR D — Selective knowledge, if warranted** | Task 8: optional pack or recorded NO-GO. | Actual consumer question and checked existing-schema source/retrieval; skip PR if NO-GO. |
| **PR E — Evidence and closeout, if distinct** | Task 9: links, real-path qualification records, minimal state note and receipt. | Authored work represented accurately; no unsupported agent-value claim. |

PR boundaries may be combined for a small low-risk change, but keep source evidence and authority explicit. This is not a prescribed sequence for every later Sensemaking user task.

## F. Sixteen documentary competency questions to implement

| ID | A successful reader can answer |
| --- | --- |
| CPI-CQ-01 | What is the inquiry activity, original typed target and exact assessed source/revision? |
| CPI-CQ-02 | Which observed premise and conditional assumption underlie the explored consequence? |
| CPI-CQ-03 | Which link in a multi-hop consequence is substantiated, hypothetical, broken or only enabling? |
| CPI-CQ-04 | Which affected beneficiaries gain, lose or remain unassessed, and on what time/context horizon? |
| CPI-CQ-05 | Which counterfactual branch changes the conclusion without inventing new facts? |
| CPI-CQ-06 | Is an apparent new opportunity a genuine new user end, an architecture mechanism, a restatement, or not assessed? |
| CPI-CQ-07 | Which **existing** assessment, portfolio snapshot and declared purpose are being reconsidered? |
| CPI-CQ-08 | Exactly which new consequence or evidence changed which criterion, prerequisite or judgment? |
| CPI-CQ-09 | Did comparison stay unchanged, narrow, reverse, become incomparable, or require more evidence; what was left untouched? |
| CPI-CQ-10 | Does a revised preference remain merely provisional, or is there a genuine selecting actor, scope and authority? |
| CPI-CQ-11 | Which exact target and inference/failure mechanism does an adversarial challenge address? |
| CPI-CQ-12 | What source evidence supports or weakens the objection, and what is still speculative? |
| CPI-CQ-13 | Did the response address the original weakness, introduce a new consequence, or leave a residual problem? |
| CPI-CQ-14 | For a design element, what user outcome, requirement, consequence, constraint or accepted challenge motivates it? |
| CPI-CQ-15 | Which part is PRD, proposed architectural specification, existing `architectural_synthesis`, or separately authorized implementation? |
| CPI-CQ-16 | What reason justifies stopping or revisiting this inquiry without treating a valid document as demonstrated product value? |

## G. High-risk acceptance scenarios

| Scenario | Correct outcome | Must not occur |
| --- | --- | --- |
| A speculative effect is followed by a speculative opportunity | Each link keeps its premise and status; the opportunity remains hypothetical. | Transitive causal proof, automatic new curated `poss:` or plan. |
| A consequence changes the **scope** of a favored option | Keep original comparison, new date, narrowed applicability and reason. | Claim an ordinal reversal or owner adoption without evidence. |
| One inquiry overtakes another after new depth | Reassess only the affected pair under the *same inquiry-purpose* frame. | Rewrite historical global ranks or turn inquiry priority into product superiority. |
| A critic suggests a plausible but unobserved failure | Review as contingent scenario with affected target and response options. | Claim an actual defect, block by runtime rule or fabricate verification. |
| A critique is answered with a design revision | Show why the revision answers the challenge and any newly introduced consequence. | Treat proposed repair as verified closure. |
| A PRD and architecture spec cite the same user goal | Each preserves its own requirements vs structure scope and source rationale. | Competing PRD authority, spec as ratification, design as implementation. |
| A selected direction depends on owner-reserved intent | Preserve pending decision and stop/handoff condition. | Infer owner approval from ranking or ontology record. |
| No further material consequence or challenge exists | Reasoned stopping/NO_CHANGE is valid. | Force a next stage or fabricate a non-empty graph. |

## H. Completion definition and conditional follow-on

The program is **complete as a documentary/installed v1 ontology** when:
1. All four questions have distinct source-preserving profile semantics with an explicit shared spine.
2. Current concepts and contract boundaries remain unchanged.
3. The 16 competencies and pinned cases are reviewable with correct outcomes for negative scenarios.
4. A portable agent can find the relevant conditional guidance without mandatory new machinery.
5. Any selective knowledge addition addresses a concrete retrieval question, uses the existing schema and is source-checkable—or is legitimately omitted.
6. The implementation history, actual checks, non-claims and continuation boundary are reconstructible.

**Not part of v1:** an automatic causal/consequence inference system; preference-ranking engine; challenge-verdict authority; new architecture/PRD schema; implementation pipeline; installed Skill host-use study; comparative creativity experiment; automatic Level-3/4 state update; external mutating actions or construction of a newly proposed product.

**Subsequent optional research:** If authentic independent agents repeatedly fail a specific competency despite access to the correct guide, first isolate whether the failure is source reachability, ambiguous concept, host installation/application or missing consumer fields. Only then consider a targeted executable-contract extension or qualification study; success of the documentation phase alone does not warrant either.


## I. Implementation, validation and decision reconciliation (2026-11-05)

**Owner implementation authorization:** explicit 2026-11-05 request to implement all tasks and proceed autonomously. The authorization covers this repository's bounded semantic/Skill documentation work and ordinary merge under the project's current PR convention. It does not ratify any of the example ProductPossibilities, Level-4 strategy, production release, external deployment or protected changes.

### Actual integrated increments

| PR / exact merged result | Source-backed delivered work and limitation |
| --- | --- |
| [#749](https://github.com/ThorStarlord/sensemaking-skills/pull/749), merged as `609c60e2507eb6c26fd82020fa43cf9afd30b7fb` | One shared [connected Level-2 ontology](../../semantic-architecture/connected-prospective-inquiry-ontology.md); four differentiated profiles, source identity, non-transitive conditional chains, decision/authority and PRD/spec separation. No new executable graph schema. |
| [#750](https://github.com/ThorStarlord/sensemaking-skills/pull/750), merged as `fd185d4563356684305ddf6a109e26e3f12a2a96` | Four historical source-pinned cases and one labeled normative PRD+technical proposal crosswalk in [reference cases](../../semantic-architecture/connected-prospective-inquiry-reference-cases-v1.md); [CPI-CQ-01..16](../../semantic-architecture/connected-prospective-inquiry-competency-v1.md) documentary fit and negative controls. No independent agent trial or invented product selection. |
| [#751](https://github.com/ThorStarlord/sensemaking-skills/pull/751), merged as `032694ead51a08564a770c5e7fbd5e2fe01607a7` | [Portable conditional guide](../../../skills/strategic-repository-analysis/references/connected-prospective-inquiry-v1.md), [optional record](../../../skills/strategic-repository-analysis/references/connected-prospective-inquiry-record-template.md), existing `using-sensemaking` first-load cue, strategic/Steward pointers and relevant semantic navigation. No second public Skill, altered PRD producer, mandatory stage or runtime hook. |

### Task 8 — explicit GO/NO-GO for machine-readable knowledge

**Decision: `NO_NEW_KNOWLEDGE_PACK` — GO for source-linked Markdown/installed guide, NO_GO for additional `.sensemaking/knowledge/*.json` records.**

The concrete consumer questions are the sixteen CPI-CQ documentary reconstruction questions, which already have source-pinned answers in the newly linked source files and existing `AssessmentRevisionAccount` / `Decision` / `ConsequenceHypothesis`/PRD architecture contracts. Inspecting these sources revealed **no demonstrably lost answer or parsed consumer need** that requires retaining the same role definitions or historical interpretations as new machine claims. The actual useful recall entry is a source path through the installed guide; duplicating it would add maintenance and uncertain provenance benefit. No authority-sensitive decision is recoverable merely by adding a new source reference. Conditional steps 8.1, 8.3–8.7 and 8.9 remain unchecked/not applicable because **the pack was deliberately omitted**, not because an attempted index build passed. Future source-consumer evidence could reopen that distinct responsibility under the existing schema-evolution process.

**Do not create** new `domain_concept` copies, speculative `ConsequenceStructure` graph predicates, source-case claims, a retrieval benchmark, parser, migration, causal inference or automatic ranking engine to make a conditional branch appear implemented. The `schema_version: 1` knowledge files remain untouched.

### Task 9 — actual review and qualification evidence

| Review / gate | Result and precise claim ceiling |
| --- | --- |
| Current governing instructions/strategy/ADRs and original source reports | **PASS (source review)** for current ontology/plan scope, prior selection ontology, dated H-A/H-B/H-C/H-D cases, authority/nonidentity constraints and existing contract producers/consumers. Original analyzed Git baselines are not rewritten. |
| `architectural_synthesis` / `prd` / `architectural_review_recommendation` / `strategic_reconciliation` contract crosswalk | **PASS (source review)**: existing artifact IDs, producers, consumers and required fields were inspected, no schema/validator modified; `to-prd` is an optional product-management Skill outside the minimal entrypoint set. |
| Changed files, source links, negative cases and competency attribution | **PASS (documentary review)** for agreed meaning and source identity. Four historical cases plus the normative E example are classified correctly, including nonselection, unchanged/conditional judgments and the `installed != loaded != invoked != applied` ceiling. It does **not** demonstrate independent readers solving a new task. |
| Hosted PR #749 source head `24b39bc2f308d1d47e731d4f110b9566a438d4be` | **PASS** Product Validation and Release Candidate Distribution; PR source/diff review and merge confirmed. |
| Hosted PR #750 source head `ea62c5acf808dba7a20209966ef22fb3255cee17` | **PASS** Product Validation and Release Candidate Distribution; PR source/diff review and merge confirmed. |
| Hosted PR #751 source head `e55938e612e985285c16d8f9b44a8284a36baa4b` | **PASS** Product Validation, Release Candidate Distribution and Semantic Context Re-entry. Hosted distribution workflow reported wheel and sdist builds and fresh wheel/sdist install proof, with job success. This is package/release-boundary validation, **not** a manually repeated byte-for-byte new-guide parity check or proof of agent host loading. |
| Source installation contract | **PASS (source inspection)**: `setup.py` packages the canonical `skills/` tree into `skill_trees`; `setup_skills.py` selects whole Skill directories, and the `entrypoint` profile includes `strategic-repository-analysis` and `repository-semantic-steward`. The new reference is in a packaged tree and is linked conditionally from `using-sensemaking`. |
| Separate local exact-commit isolated wheel/entrypoint install | **NOT_RUN**: the execution environment could not resolve the GitHub host for checkout; do not report local parity or later host application as observed. Hosted distribution validation remains the relevant available real-path evidence. |
| Local unit and synthetic evidence tests | **NOT_RUN (repository construction policy)**; no tests created or manually run. Existing hosted CI protections were left intact and hosted checks above passed. |
| Knowledge proposal, index build and search/explain for a **new** `.sensemaking/knowledge` candidate | **NOT_RUN / NOT_APPLICABLE** because the no-pack decision does not introduce a candidate, and running one to satisfy a checklist would contradict the evidence economy. |
| New independent agent creativity, actual PRD+technical-spec creation, user/beneficiary impact, automatic graph causality | **NOT_ASSESSED**. The Level-2 ontology is a source/agent-documentary capability, not a qualification result about improved reasoning. |

### Concluding reconciliation

**Responsibility state: `GOAL_SATISFIED` for the bounded documentary Level-2 ontology, source cases, competency review, installed-source references and conditional integration.** No additional machine-readable knowledge projection was warranted. A final existing-schema `sensemaking_session_receipt` records what actually occurred with stable source paths and this plan, without granting any downstream authority.

**Strategic state: `NO_MODEL_CHANGE`.** ADRs 0029/0031/0034, the existing strategic PATH-1 responsibility, current PRD/architecture consumers, historical reports, owner decisions and installer defaults were not revised. `STATUS.md` may record only this qualified new documentary capability, not redirect current construction priority.

**Unqualified next question (not a required stage):** Would an independent later agent actually retrieve and correctly apply this guide in an authentic repository inquiry, and would it make a meaningful decision or product-possibility improvement relative to source-only reasoning? A new agent trial would need a separately warranted task and instrumentation; this work does not manufacture one.

**Stop:** the relevant source/Skill capability is delivered and integrated; no further authorized vertical ontology layer or code consumer is evidenced. Preserving the ability to choose `NO_CHANGE` and `NO_SELECTION` is intentional. A future genuine failure in retrieval, source interpretation, contract or agent invocation can warrant targeted repair, not automatic executable ontology expansion.
