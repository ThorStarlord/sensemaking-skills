# Possibility Assessment and Prioritization Ontology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended when independent workers are available) or superpowers:executing-plans. Track each checkable step with its checkbox. This is a plan, not implementation authorization.

**Goal:** Make coverage, diminishing-return, consolidation, comparative evaluation, and ranked-portfolio reasoning source-reconstructible and purpose-relative, without changing decision authority or erasing historical possibilities.

**Architecture:** Extend the existing divergent-exploration and prospective semantic foundation with one conceptual assessment module, a portable assessment guide and optional Markdown record, source-pinned reference cases, and a small reviewed-knowledge projection using the already supported contract. Focused activity profiles reuse one assessment pattern. Existing active-agent control, strategy ownership, and construction authority remain unchanged.

**Tech Stack:** Markdown semantic architecture and installed Skill references; Git source history; existing JSON reviewed-knowledge contract (schema_version 1) and semantic Python CLI/SQLite index for bounded verification; existing setup-skills/wheel distribution. No new runtime dependency, parser, scoring engine, graph kind, or workflow is authorized by this plan.

**Spec:** [Possibility Assessment and Prioritization Ontology v1 — Design Basis](../specs/2026-11-04-possibility-assessment-prioritization-ontology-design.md). Read the spec and this plan together.

**Date / planning baseline:** 2026-11-04, ThorStarlord/sensemaking-skills@b327ed2e82e125644a1f88b7feba478f1cd583b1 (after merged divergent-exploration ontology PR #732). Refresh source identities at implementation time.

**Status:** IMPLEMENTED — the seven authorized core tasks and 52 checkable steps were carried through on 2026-11-04. Substantive documentation and knowledge were merged via PRs #734, #735 and #738. The closeout records the canonical receipt validator, actual retrieval and installed-delivery checks; none establishes independent creative benefit, strategic adoption or construction authority.

## Global Constraints

- **G1:** Use the existing ExplorationInquiry, InquiryQuestion, ExplorationFrame, CandidateExpression, PossibilityLandscape, ExploratoryJudgment, ProductPossibility, ArchitectureOption, ConstructionPath, Claim, Assumption and authority vocabulary. Add conceptual roles only where they preserve real differences.
- **G2:** The active agent chooses warranted responsibilities. Coverage, consolidation, evaluation, depth, portfolio review and implementation are distinct responsibilities, not mandatory pipeline stages; no automatic next-stage routing.
- **G3:** A judgment is attributed and bounded by target, purpose, source/revision scope, criteria, evidence/counterevidence, uncertainty and revision conditions. Unknowns remain unknown.
- **G4:** Coverage of a declared corpus, conceptual breadth, consequence depth, empirical support and independent perspective coverage are separate judgments. Sufficiency for one next purpose is not global saturation.
- **G5:** Retrospective repetition, prospective marginal learning under a proposed inquiry **method**, and attention allocation relative to alternatives are separate judgments; no candidate-count novelty-rate inference.
- **G6:** Consolidation is purpose-relative, non-transitive across criteria, and source preserving. Keep old expressions, source labels, historical dispositions, contested identities and legitimately overlapping groupings.
- **G7:** Qualitative comparison may yield preference, tie, partial order, conditional comparison, incomparability, unresolved comparison or NOT_ASSESSED. No forced total ordinal order, numerical score, weight or rank confidence percentage.
- **G8:** Exploration priority concerns a specific question AND proposed investigation; strategic attractiveness concerns desired futures and their consequences; implementation priority concerns concrete work with independently established authorization. Never turn rankings into tasks or permissions.
- **G9:** Preserve dated snapshots and explain changes in source evidence, frame, target, method, criteria, or authority. An updated portfolio does not silently rewrite older documents.
- **G10:** Make portable references usable without the Sensemaking framework checkout, SQLite, a CLI, or external target-repository data. Retention is selective and does not bulk-promote historical speculative candidates.
- **G11:** No new executable predicate, universal schema, artifact contract, mandatory sidecar or specialized query without a named consumer and demonstrated loss under existing representation; follow the existing schema-evolution procedure if triggered.
- **G12:** Follow current repository-local CLAUDE.md at implementation time. As of this plan, the owner construction exception forbids adding/manually running local unit and synthetic evidence tests. Use source/diff review, link/source checks, real artifact and installed-delivery checks; record NOT_RUN accurately. Preserve hosted CI and protections.
- **G13:** Definitions, structural validation, retrieval, installed files, reader reconstruction, normal-use behavior and creative-benefit claims occupy distinct evidence levels. Do not claim one from another.

The G12 local-policy exception governs work on this repository, not portable instructions for other repositories. Do not borrow generic test-first examples against the explicit local policy.

## Review Focus — five highest-risk misunderstandings

1. **A different priority object is ranked as if it were the same:** a question+method, a product future and authorized work must remain distinct; test through the source-based Futures example (Tasks 1, 2, 3, 6).
2. **Grouping silently destroys provenance or becomes sameAs:** GD-D/DE-F2 must keep both source identities and the precise, non-transitive criterion (Tasks 1, 2, 6).
3. **Missing assessment is reported as low rank or a tie:** Exit/Public must remain retained but outside the common ranking; NOT_ASSESSED, unknown, conditional and incomparable must not be collapsed (Tasks 1, 2, 3, 6).
4. **Coverage or diminishing return is overstated:** a locally repetitive lens is not a saturated universe; historical repetition is not prospective return or resource allocation (Tasks 1, 2, 6).
5. **Documentary/graph/index validity is sold as creativity or authority:** checked definitions and a wheel install prove only their bounded claims; no new action consent, independent creative benefit or automatic host discovery (Tasks 4–7).

---

## 1. Scope, deliverables and verification boundary

**Expected end state:**

1. Canonical conceptual ontology for assessment framing, target roles, attributed judgments, consolidation views, portfolios and revisions, with explicit ties to existing concepts and endpoint non-widening.
2. A local competency/fit account answering the twelve questions in the design basis.
3. Source-pinned historical examples covering coverage, duplication, method-dependent inquiry priority, outside-frame members and ranking revision.
4. A self-contained portable assessment guide and optional record shape for agents performing the separately warranted activities.
5. Conditional entrypoint/reference cues that do not auto-activate a sequence or alter the existing Skill's public responsibility.
6. Selectively reviewed knowledge definitions and source-document links, using current supported JSON kinds and predicates.
7. Actual source-link, proposed-knowledge, retrieval, installed-package and later-reader reconstruction evidence, followed by navigation and plan/receipt reconciliation.

**Out of scope for v1:** a new execution Skill, dedicated parser/schema, automatic scoring/ordering, forced stage choreography, universal assessment completeness checker, bulk archive rewrite, backfilled ranked graph instances, new product thesis, independent creative qualification, external release or deployment.

### 1.1 Existing authoritative sources to inspect

- [Divergent exploration ontology](../../semantic-architecture/divergent-exploration-ontology.md) and its [competencies](../../semantic-architecture/divergent-exploration-competency-v1.md).
- [Layered ontology](../../semantic-architecture/ontology.md), [prospective ontology](../../semantic-architecture/prospective-reasoning-ontology.md), [product possibility ontology](../../semantic-architecture/product-possibility-ontology.md) and [relations/epistemics](../../semantic-architecture/relations-and-epistemics.md).
- [Current accumulated portfolio](../../explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md), [convergent source crosswalk](../../explorations/2026-11-03-convergent-accumulated-creative-possibilities.md), [coverage assessment](../../explorations/2026-11-02-divergent-coverage-assessment.md), [initial ranking](../../explorations/2026-11-03-depth-exploration-prioritization.md), [later reassessment](../../explorations/2026-11-03-portfolio-reassessment-architectural-generativity.md), and [inquiry process reconciliation](../../explorations/2026-11-03-inquiry-process-reconciliation.md).
- [Existing portable divergent profile](../../../skills/strategic-repository-analysis/references/divergent-exploration-v1.md), [strategic exploration funnel](../../../skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md), [using-sensemaking entrypoint](../../../skills/using-sensemaking/SKILL.md), [knowledge contract](../../../skills/repository-semantic-steward/references/knowledge-contract.md), and [schema evolution](../../../skills/repository-semantic-steward/references/schema-evolution.md).
- Repository-local CLAUDE.md and the current product strategy/accepted ADR 0029, 0031 and 0034. Recheck these when execution begins.

### 1.2 File and ownership map — new files

| File | Single responsibility |
| --- | --- |
| docs/semantic-architecture/possibility-assessment-ontology.md | Canonical proposed conceptual roles, relationship endpoints, comparison meanings, provenance and authority invariants |
| docs/semantic-architecture/possibility-assessment-competency-v1.md | Local twelve-question fit matrix, case-based documentary reconstruction and evidence ceilings |
| docs/semantic-architecture/possibility-assessment-reference-cases-v1.md | Source-pinned annotated cases; full original expression and judgment identities preserved |
| skills/strategic-repository-analysis/references/possibility-assessment-v1.md | Self-contained portable guide for bounded coverage, consolidation, evaluation and portfolio reasoning |
| skills/strategic-repository-analysis/references/possibility-assessment-record-template.md | Optional common assessment envelope and task-specific record sections |
| .sensemaking/knowledge/possibility-assessment.json | Selective declared concept definitions plus the case-source record and existing supported reference links |

### 1.3 Existing files with bounded edits

| File | Permitted change |
| --- | --- |
| docs/semantic-architecture/ontology.md | One conceptual-extension pointer; no new control stage |
| docs/semantic-architecture/divergent-exploration-ontology.md | One cross-reference to downstream assessment meanings; do not alter historic divergence semantics |
| docs/semantic-architecture/relations-and-epistemics.md | Short documentary relation/endpoint crosswalk without adding predicates |
| docs/semantic-architecture/competency-questions.md | Point from relevant existing CQ sections to local assessment fit; avoid duplicate global IDs |
| docs/semantic-architecture/README.md | Module, competency, case and formalization-level navigation |
| skills/using-sensemaking/SKILL.md | Conditional one-line assessment reference cue only if it changes first-load decisions |
| skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md | Reference optional assessment profile when that responsibility is warranted within Level 3 |
| skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md | One handoff clarification if existing language implies that divergence itself ranks futures |
| skills/repository-semantic-steward/references/knowledge-contract.md | Minimal selective-retention crosswalk if the current guidance otherwise leaves meaning ambiguous |
| docs/explorations/README.md | Discoverability and responsibility boundary, not history rewrite |
| STATUS.md | Change only if the capability state materially changes the next-agent decision |
| docs/superpowers/plans/2026-11-04-possibility-assessment-prioritization-ontology.md | Completion checkboxes and evidence after actual implementation |
| .sensemaking/receipts/YYYY-MM-DD-possibility-assessment-ontology-implementation.session.yaml | Existing session receipt only when the responsible session has real execution facts to record |

Do not modify the 59-candidate reports, the curated Idea Library's dispositions, the accepted ADRs, existing prospective comparison endpoints, packaging profiles or executable schema merely to satisfy the file map.

## 2. Implementation dependency and PR plan

Suggested increments (each independently reviewable):

- **PR A — semantic foundation:** Task 1, then locally coherent competency definitions. Creates the shared contract for later cases.
- **PR B — cases and portable profile:** Tasks 2–3. Provides substantive usable records instead of a glossary alone.
- **PR C — integration and selective knowledge:** Tasks 4–5. May prepare in parallel after Task 3, but must reconcile common source identities before merging.
- **PR D — reconstruction and closeout:** Tasks 6–7, including source identity, links, installed evidence, final account and receipt.

Split if review reveals independently rejectable work; combine small related edits to avoid knowingly broken references. Each PR carries a source-grounded decision note, exact verification scope, and actual CI state. Follow the repository's current merge policy; do not circumvent protections. No PR is authorized to silently turn a recommendation into a product or implementation decision.

### Task 1: Define shared assessment semantics and local competency contract

**Files:**
- Create: docs/semantic-architecture/possibility-assessment-ontology.md
- Create: docs/semantic-architecture/possibility-assessment-competency-v1.md
- Modify: docs/semantic-architecture/ontology.md
- Modify: docs/semantic-architecture/divergent-exploration-ontology.md
- Modify: docs/semantic-architecture/relations-and-epistemics.md
- Modify: docs/semantic-architecture/competency-questions.md

**Consumes:** approved design basis; latest layered/divergent/product/prospective meanings.
**Produces:** stable conceptual definitions and comparison endpoints for Tasks 2–5.

- [x] **1.1 Source-lock:** record current HEAD, source-file revisions and the specific existing terms reused; inspect CLAUDE.md, governing ADRs and the latest divergent-ontology merge before editing.
- [x] **1.2 Draft the conceptual ontology:** define AssessmentActivity, AssessmentFrame, AssessmentTarget reference role, AssessmentJudgment, ConsolidatedView, PortfolioSnapshot, ProposedInquiryApproach and AssessmentRevisionAccount; explain layer/role mappings and what is not a new persistent entity.
- [x] **1.3 Define the five substantive judgment refinements:** coverage; three meanings of diminishing returns; consolidation relation; purpose-relative qualitative comparison; exploration/strategic/implementation priority. Include NOT_ASSESSED, unresolved, tie and incomparable as distinct cases.
- [x] **1.4 Specify relationship endpoints and establishment:** link assessment to target, frame, criteria, evidence, source/revision, results and later revision; explicitly preserve narrow ComparativeJudgment/ProvisionalPreference architecture/path endpoints and existing decision authority.
- [x] **1.5 Specify identity and history:** local IDs qualified by source artifact, original candidate labels, report-file vs inspected-target revisions, append-only dated reassessment, non-transitivity, overlapping groupings, and no hidden rank promotions.
- [x] **1.6 Write the local competency matrix:** include each of the design's twelve questions, the closest existing CQ/ontology concept, baseline fit (faithful/awkward/lost/not established) and required implemented answer. State what sources actually justify each baseline claim.
- [x] **1.7 Update only relevant ontology/competency pointers:** cross-link definitions; leave executable enum/contract untouched. Inspect the diff for contradictory definitions and unintended changes to historic roles.
- [x] **1.8 Commit a source-reviewed semantic increment:** check paths and links; record review findings and precise evidence limits in the PR. Stop if a proposed concept actually requires a new owner-level decision.

**Task 1 acceptance:** a reader can identify each activity/role and its existing ancestor; every relationship has named operand roles; a portfolio never ranks construction from a divergent judgment; no schema/ADR/control contract is silently widened.

### Task 2: Annotate the source-grounded edge cases

**Files:**
- Create: docs/semantic-architecture/possibility-assessment-reference-cases-v1.md
- Modify: docs/semantic-architecture/possibility-assessment-competency-v1.md

**Consumes:** Task 1 roles and five documented sources in spec section 7.
**Produces:** concrete case IDs/source anchors that Tasks 3–6 can reconstruct.

- [x] **2.1 Inspect original source locations and revisions:** extract only source-established labels, questions, premises, groupings and assessment wording; distinguish the revision containing a report from the older target revision it inspected.
- [x] **2.2 Case C1 — coverage not saturation:** describe the inspected scope, conceptual breadth, missing perspectives, qualitative sufficiency for provisional convergence, and why candidate counts do not produce an overall novelty-rate claim.
- [x] **2.3 Case C2 — near duplicate without identity merge:** retain GD-D and DE-F2 with their original documentary identities; state the criterion of overlap and why original expressions and alternative groupings survive.
- [x] **2.4 Case C3 — proposed investigation changes priority:** use the retained goal-discovery causal-benefit question to distinguish another conceptual essay from a viable independent observation, while keeping the broader strategic direction separate.
- [x] **2.5 Case C4 — portfolio member outside order:** represent Exit and Public as retained directions with different evaluative frames, not rankings seven and eight.
- [x] **2.6 Case C5 — changed question and relative order:** compare historical depth ranking, architectural reappraisal and updated portfolio using actual source revisions/remaining questions rather than overwriting historical priority.
- [x] **2.7 Record any unestablished parts honestly:** do not invent numerical weights, a human reviewer's identity, detailed owner utility, or an independent empirical result; mark genuinely illustrative material explicitly.
- [x] **2.8 Update qualitative fit:** judge the twelve questions from real examples; include one counterexample where similar wording has different criteria or a missing comparison is not a tie. Inspect source links, exact labels, and revised claims before merging.

**Task 2 acceptance:** a later reader can find every source, explain how each grouping/ranking was scoped, and recover at least one honest absence or incomparable case without fabricated meaning.

### Task 3: Write portable agent guidance and an optional retained-record template

**Files:**
- Create: skills/strategic-repository-analysis/references/possibility-assessment-v1.md
- Create: skills/strategic-repository-analysis/references/possibility-assessment-record-template.md

**Consumes:** Task 1 meanings and Task 2 source cases.
**Produces:** target-independent agent guidance consumed by Task 4 and installed delivery.

- [x] **3.1 Write a standalone portable guide:** state when assessment is useful, its bounded entry, source/currentness and owner-authority requirements, the shared envelope, how to use qualitative judgments, and when to stop rather than rank.
- [x] **3.2 Add separate responsibility profiles:** coverage/returns, consolidation, comparative evaluation and portfolio snapshot; make explicit that none automatically triggers the next profile.
- [x] **3.3 Add priority framing instructions:** explicitly distinguish question+proposed method, product future and authorized work; explain evidence/decision thresholds without fixed stage gates or scoring.
- [x] **3.4 Draft an optional Markdown record:** common header (question, scope, targets, source revisions, frame, criteria, grounds, uncertainty, reconsideration); sections for each profile; local IDs and source pointers; sparse records permitted.
- [x] **3.5 Include compact illustrative distinctions:** distinguish NOT_ASSESSED, incomparable, tied, conditional and low-ranked; specify that grouping does not erase original IDs; include a worked priority change without auto-building.
- [x] **3.6 Audit portability:** remove reliance on the framework checkout, SQLite, hidden prior chat or source-specific private target paths; explain how a target repository supplies its own sources and authorized retention surface.
- [x] **3.7 Review and commit the usable profile:** ensure the guide is not an automatic planning or strategy mandate; check source names and relative links, and mark illustrative content as illustrative.

**Task 3 acceptance:** an agent can use installed reference text alone to produce a bounded, meaningful assessment and stop with valid uncertainty; a short honest prose result does not fail for omitting irrelevant template sections.

### Task 4: Integrate guidance at the smallest real entrypoints

**Files:**
- Modify: skills/using-sensemaking/SKILL.md (only if required)
- Modify: skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md
- Modify: skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md (only if required)
- Modify: skills/repository-semantic-steward/references/knowledge-contract.md (only if required)

**Consumes:** the final Task 3 reference paths and established responsibility boundaries.
**Produces:** a discoverable optional route for separately warranted assessment.

- [x] **4.1 Inspect the current entrypoint/reference triggers:** identify whether a standalone assessment request already reaches a suitable reference; decide whether a one-line cue changes a first-load decision.
- [x] **4.2 Add the minimum cue where justified:** point to the portable guide only when assessing coverage, consolidation, qualitative comparison or a bounded opportunity portfolio; explicitly reject automatic passage to strategy or implementation.
- [x] **4.3 Clarify the Level-3 funnel handoff:** a full strategic analysis may use these semantics but a standalone assessment need not become Level 3; existing strategic artifacts retain authority.
- [x] **4.4 Clarify divergence boundary if needed:** divergence produces expressions and scoped judgments; independent coverage, consolidation or ranking remains separately warranted. Avoid expanding the core reference if it already says this.
- [x] **4.5 Clarify selective knowledge retention only if needed:** source reports and receipts vs reviewed claims; never automatically promote every group, rank or fragment to a ProductPossibility.
- [x] **4.6 Inspect installed Skill tree composition and links:** verify proposed cues resolve within current distribution profiles, without changing profile membership or inventing a new entrypoint.
- [x] **4.7 Commit a minimal diff with decision note:** include the concrete reason for each core Skill text change and the cost of not making it.

**Task 4 acceptance:** a fresh agent can locate the profile for an explicit assessment request; existing clear bounded work and divergent-only requests do not acquire unwanted assessment ceremony.

### Task 5: Add a bounded reviewed-knowledge projection

**Files:**
- Create: .sensemaking/knowledge/possibility-assessment.json
- Modify: docs/semantic-architecture/possibility-assessment-competency-v1.md (record observed check results)

**Consumes:** Task 1 canonical definitions, Task 2 case document, and current knowledge-contract schema.
**Produces:** source-linked definitions/source record findable through the existing semantic CLI.

- [x] **5.1 Reinspect the actual accepted schema:** use skills/repository-semantic-steward/references/knowledge-contract.md and the parser, not inferred field names; keep exact top-level schema_version, claims and relations.
- [x] **5.2 Author only needed claims:** use supported domain_concept declarations for selected semantic roles and one source claim for the case record, with actual tracked evidence paths and declared/hypothetical status appropriate to the claim.
- [x] **5.3 Author only supported relationships:** references or other existing valid predicates backed by source evidence; conceptual_relation attributes may document meanings but are not machine-verified predicates.
- [x] **5.4 Check structure on the authored proposal:** run python -m sensemaking_skills.cli semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/possibility-assessment.json --json. Expected: accepted claims/relations with no contract or source errors. A file not checked successfully remains a draft.
- [x] **5.5 Inspect the checker output and source identities:** reconcile a failure from actual evidence/schema rules, not by weakening the parser; ensure no hypothesis was marked as observed product value.
- [x] **5.6 Commit the validated pack without historical bulk migration:** source/diff review and PR note explain what it represents and what it does not.

**Task 5 acceptance:** the existing checker accepts every retained record; definitions and source pointers are identifiable without inventing new predicate/kind names or elevating portfolio preferences into decisions.

### Task 6: Verify real retrieval, installed delivery, and fresh-reader reconstruction

**Files:**
- Modify: docs/semantic-architecture/possibility-assessment-competency-v1.md
- Modify: docs/semantic-architecture/possibility-assessment-reference-cases-v1.md only to fix sourced defects

**Consumes:** committed Tasks 1–5, an exact source revision, and current installer.
**Produces:** an accurate evidence account for the actual documented consumer.

- [x] **6.1 Source and link inspection:** at an exact committed head, check all new/changed paths and relative links; inspect the source-cited original paragraphs/tables for case identity drift.
- [x] **6.2 Real index build:** at the clean committed HEAD, build outside the checkout using sensemaking-skills semantic knowledge-build --repo . --repository ThorStarlord/sensemaking-skills --target-ref <HEAD_SHA> --db <TEMP_SQLITE> --json. If working tree is dirty, use the documented --temporary-checkout option.
- [x] **6.3 Actual search and explanation:** query selected role definitions and the source-document claim using knowledge-query --operation search / explain with the same repository and target-ref. Inspect returned source paths, kind, authority, source hash and bounded relation coverage. Retrieval is not proof of normative correctness.
- [x] **6.4 Real package and installed profile:** build a wheel using the repository's current documented mechanism, install in an isolated environment, run setup-skills --target claude --scope project --profile entrypoint into a fresh project, and compare relevant Skill/reference trees source -> wheel -> installed files.
- [x] **6.5 Consumer reconstruction:** have a fresh reader if available (otherwise a separately conducted cold-read) follow the installed entrypoint and profile, consult the source-pinned cases, and answer all twelve local competency questions without assuming previous-chat memory.
- [x] **6.6 Challenge edge cases:** verify specifically that Futures' evidence-only inquiry is not equated with Futures' product attractiveness, that GD-D/DE-F2 remain separately sourced, Exit/Public are not last-ranked, and NOT_ASSESSED is not tied or incomparable by default.
- [x] **6.7 Record real outcomes, limits and unresolved defects:** use faithful/awkward/lost/not established; do not count the cold-read or reference examples as an independent creative-benefit or normal-use qualification study. Fix concrete semantic loss, then rerun the affected source/retrieval/reader checks.
- [x] **6.8 Record test discipline:** local unit/synthetic tests NOT_RUN under the still-current repository policy, hosted CI state exact to head SHA, and real artifact/retrieval/installed-delivery checks actually performed.

**Task 6 acceptance:** all critical documentary distinctions are source-reconstructible by the tested reader, or any unresolved loss is explicitly documented with a justified stop; real retrieval and installed files are verified from identified revisions.

### Task 7: Reconcile navigation, boundaries, and durable completion

**Files:**
- Modify: docs/semantic-architecture/README.md
- Modify: docs/explorations/README.md
- Modify: STATUS.md only if warranted by a changed capability statement
- Modify: docs/superpowers/plans/2026-11-04-possibility-assessment-prioritization-ontology.md
- Create: .sensemaking/receipts/YYYY-MM-DD-possibility-assessment-ontology-implementation.session.yaml when a real completed session warrants the existing receipt

**Consumes:** accepted source documents, the actual Task 6 evidence, and current repository authority.
**Produces:** discoverable, honestly closed implementation with preserved historical records.

- [x] **7.1 Update semantic navigation:** link ontology, profile, cases and fit account; describe Level-2 semantic meanings separately from any existing Level-3 knowledge projection.
- [x] **7.2 Update exploration archive navigation:** distinguish divergence from assessed coverage, consolidation, evaluation and portfolio; link to historical source assessments without modifying them.
- [x] **7.3 Update capability status only when material:** identify actual shipped documentary guidance and indexing evidence, not creative improvement or independent qualification.
- [x] **7.4 Review the entire diff and source boundaries:** no modified historic candidate descriptions or statuses; no widened prospective endpoints; no accidental new Skill/contract; no misleading claim that "top priority" authorizes a build.
- [x] **7.5 Close checked steps against observed work:** record PRs, commits, evidence, genuine NOT_RUN checks, active conditional follow-ups and uncertainties; do not check an unperformed step.
- [x] **7.6 Create/validate the ordinary session receipt when warranted:** include target/source and Skill identity, existing authority, actual work/validation, open empirical question and stopping reason; receipt must not become a semantic-index claim or source of new authority.
- [x] **7.7 Integrate and confirm canonical source:** follow the repository's current branch/review/merge policy; verify the final files on main and report CI checks pending/success/failure at the exact observed revision.
- [x] **7.8 Stop at the justified boundary:** no schema/query expansion or independent creative qualification unless a separate concrete need, target and authority exist.

**Task 7 acceptance:** all planned v1 files and integration points are present at an identified merged revision, the completion account is evidence-bounded, and historical exploration, possibility and strategy decisions remain intact.

---

## 3. Local competency and acceptance matrix

| Question | Owning task(s) | Required observable answer |
| --- | --- | --- |
| C1: What exactly was assessed, by whom, against which revisions? | 1, 2, 6 | Source, target, assessor/unknown and distinct source-file / inspected baselines |
| C2: Coverage of what: corpus, breadth, depth, empirical support, perspective? | 1, 2 | Multiple meanings stated; no conflation |
| C3: Sufficient for what, and what was not assessed? | 1, 2, 6 | Bounded purpose and omissions, without global saturation |
| C4: Repetition vs forecast marginal learning vs attention allocation? | 1, 2, 6 | Three separate attributed claims with method/context |
| C5: Which expressions grouped and which distinctions omitted? | 1, 2 | Source-qualified original expressions and purpose |
| C6: Can purported duplicates remain disputed and separately identifiable? | 1, 2, 6 | Non-transitive, provenance-preserving relation |
| C7: Is priority about question+method, product future or authorized change? | 1, 3, 6 | Exact target and correct evaluation frame |
| C8: How is preferred/tied/conditional/incomparable/unresolved/NOT_ASSESSED represented? | 1, 3, 6 | Distinct outcomes; missing data does not imply tie |
| C9: Does portfolio membership differ from ordinal ranking? | 1, 2, 6 | Exit/Public remain visible without rank seven/eight |
| C10: Which new information or question changes a ranking? | 2, 6 | Historical snapshot and explicit changed premise/criterion |
| C11: How are shared uncertainties and complements shown without causal overclaim? | 1, 2, 3 | Conditional relation with evidence/unknown stated |
| C12: Does any assessment create product truth, decision or action permission? | 1, 4, 5, 6 | No; existing authority separately sourced |

Use this matrix as a documentary fit review. The exact global CQ numbers, when cross-referenced, must be inspected from the current repository rather than assigned by analogy.

## 4. Explicit conditional follow-ups outside the core completion path

**C-A: Registered parsed assessment artifact.** Trigger only when a named producer and consumer require specific stable fields not reliably recoverable from the Markdown profile. Record the exact question, input/output field expectations, compatibility, and why the existing session receipt and artifact are inadequate. Then use normal schema design/review separately.

**C-B: New knowledge predicate, type or specialized query.** Trigger only when an authentic retrieval question cannot preserve a necessary comparison/priority distinction using source records, supported references, attributes, existing knowledge kinds and explanation. Demonstrate the lost answer, endpoint rule, backwards compatibility, existing alternatives and authorization before changing schema.

**C-C: Independent normal-use/creative qualification.** Trigger when real independent coding-agent tasks, appropriate reviewers and separately authorized evidence production are available. Compare effective outcomes with source-only reasoning where feasible; do not reuse these reference cases or a fresh-reader documentary check as independent qualification.

**C-D: Strategic adoption or construction priority.** Trigger only through the applicable owner/strategic decision and implementation planning, respectively. A portfolio's first position never grants permission to build it.

## 5. Common risks and mitigation

| Risk | Preventive design and verification |
| --- | --- |
| Overly broad AssessmentJudgment erases existing semantics | Explicit specializations and narrow endpoints, annotated by real cases |
| New ontology becomes a stage engine | Optional profiles; explicit standalone stopping, no automatic routing |
| New labels invent ontology where prose already suffices | Concept-first mapping, competency fit and conditional schema gate |
| Historical ranking treated as universal best idea | Keep question+method+frame+timestamp, revisions and reversal conditions |
| Consolidation destroys minority or competing interpretations | Preserve source expressions, overlapping views, disagreement and non-transitive criteria |
| Strong-looking structured record masks weak evidence | Source/counterevidence, NOT_ASSESSED and qualitative uncertainty; no scores |
| Framework-only links prevent installed use | Self-contained Skill references, isolated wheel and target repository check |
| Source reference and graph claim mismatch | Real knowledge proposal check, exact-head index, search/explain and file hash review |
| Hosted CI green overstated as user outcome | Separate evidence ceilings, exact SHA and status; independent benefit remains unqualified |

## 6. Definition of complete

The **core implementation** is complete when Tasks 1–7 have been performed within actual authority, the ontology and profile are understandable and discoverable, the source cases preserve their original meaning, the knowledge projection passes the existing contract and retrieves correctly, the installed reference reaches the reader, and the final account records limitations and merge state.

It is **not** complete merely because the ontology glossary or optional record template exists. Conversely, it does **not** require the conditional C-A through C-D work without a new warrant.

After implementation, a follow-on independent inquiry could ask whether assessment reuse improves actual agent reasoning. That future question is valuable, but does not retroactively become an acceptance test for this documentary v1.

## 7. Handoff

The future coding agent should read the spec and this plan, verify the target repository's current source and local instructions, implement bounded tasks with source review and real artifact checks, preserve their exact evidence and authority, and stop at the documented completion boundary.

**Recommended execution approach:** subagent-driven implementation if independent worker/reviewer tools are genuinely available; otherwise native execution with a separate critical final review. This choice affects review organization only, not the ontology semantics or the user's implementation authorization.

**Current disposition:** CORE IMPLEMENTATION COMPLETE; conditional schema, query and independent qualification inquiries are not automatic implementation responsibilities.

## 8. Implementation completion account — 2026-11-04

**Authorization and disposition.** The owner explicitly authorized completing every task, making bounded owner decisions and continuing without intermediate approval. This record documents the implemented **conceptual ontology, portable documentary assessment profile, selective existing-schema knowledge projection and bounded verification**, not a new product-thesis decision, strategy-selection runtime, numerical ranking procedure or parser contract. The original planning baseline remains historical. The canonical implementation is linked in the [Assessment Ontology](../../semantic-architecture/possibility-assessment-ontology.md), the [twelve-question fit account](../../semantic-architecture/possibility-assessment-competency-v1.md), the [reference cases](../../semantic-architecture/possibility-assessment-reference-cases-v1.md) and the [session receipt](../../../.sensemaking/receipts/2026-11-04-possibility-assessment-ontology-implementation.session.yaml).

| Task | Delivered result | Observed integration/evidence |
| --- | --- | --- |
| **1 — Semantics and competencies** | AssessmentActivity, AssessmentFrame, typed AssessmentTarget, AssessmentJudgment, ConsolidatedView, PortfolioSnapshot, ProposedInquiryApproach and AssessmentRevisionAccount, including narrow inherited comparison endpoints and twelve local competency questions | [PR #734](https://github.com/ThorStarlord/sensemaking-skills/pull/734) merged as `7773aa04e686ac06eb4ad9d2f8d92bad89d046cc`; relevant layered/semantic/epistemic cross-references were reviewed. |
| **2 — Source-bound cases** | Five annotated historical cases: bounded coverage, GD-D/DE-F2 grouping, the method-dependent Futures inquiry, Exit/Public outside the common order and three differently scoped historical rankings | [Case record](../../semantic-architecture/possibility-assessment-reference-cases-v1.md) pins the **containing file revision** `4f732aaf293b5efb52f1a4428da2c65c48b3c72e` separately from the report's earlier inspected target revision. Original candidate identity and dispositions remain unchanged. |
| **3 — Portable record guide** | Self-contained guide and optional Markdown template; sparse, qualitative, partial or non-comparable findings remain legitimate | [Profile](../../../skills/strategic-repository-analysis/references/possibility-assessment-v1.md) and [template](../../../skills/strategic-repository-analysis/references/possibility-assessment-record-template.md) in PR #734; corrected Markdown escapes in PR #738 and verified installed-byte parity. |
| **4 — Agent and strategy integration** | Conditional first-load entrypoint cue, existing Level-3 funnel cross-reference and Steward retention boundary | [PR #735](https://github.com/ThorStarlord/sensemaking-skills/pull/735) merged as `12c5b314b5a2a065c8cf9ffdbe959eab7bf05566`; no new Skill, default routing, workflow engine or mandatory stage. |
| **5 — Reviewed knowledge** | `schema_version:1` authored pack with **eight declared concept definitions, one observed case-document source claim and four supported references relations** | The [Source-pinned context consumer](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41930560601/job/126926073771) on PR #735 head `136fb26c99169596fa5a7a6eca112ef1184686f0` ran proposal checks over all packs and exact-commit graph build: **PASS**. All nine hosted PR #735 jobs eventually succeeded. |
| **6 — Real-path and reconstruction review** | Exact-commit knowledge search and explanation; real wheel; isolated fresh project `entrypoint` installation; source/install byte comparisons; author reconstruction against twelve local questions | The [corrected-source real-path job](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41931267934/job/126928462432) on `37a6ad7aa539349a4e1d280d67d259934cb69765` logged `ASSESSMENT_PROPOSAL_INDEX_SEARCH_EXPLAIN_PASS` and `ASSESSMENT_INSTALLED_REFERENCE_PARITY_PASS`. The compared substantive file blobs matched the merged source branch. This was **author self-review**, not a fresh independent-agent qualification. |
| **7 — Reconciliation and closeout** | Semantic and Exploration Atlas navigation, STATUS capability statement, source formatting fixes, dated evidence ceilings, completed plan and immutable session receipt | [PR #738](https://github.com/ThorStarlord/sensemaking-skills/pull/738) merged as `1d73a8b49dee2251f581f03cf253e7fe553cd73b`. Canonical receipt validator on the real receipt returned **`RECEIPT_VALID`** in [hosted job](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41931723068/job/126930015455). The final administrative PR commits this plan and receipt. |

### Review and construction decisions made under delegation

- Reuse the existing conceptual ontology and checked knowledge `domain_concept`/`source`/`references` format. **No parsed assessment artifact, new schema kind, predicate, query, automatic ranking engine or scoring procedure** was justified by the examined reader use case. A future schema extension requires a concrete producer/consumer or lost answer.
- Preserve the distinction between coverage, local repetition, conditional expected learning and attention allocation. Keep `NOT_ASSESSED`, unresolved comparison, assessed tie and incomparability distinct; do not interpret an unranked portfolio member as inferior.
- Preserve original candidate/source identities and the historical H/B/N rankings as dated judgments. Do not promote a navigational group to a `poss:` record, retroactively change accepted owner strategy, or widen the ArchitectureOption/ConstructionPath endpoints of `ComparativeJudgment`/`ProvisionalPreference`.
- Deliver guidance through existing installed Skill trees. Do **not** require a Sensemaking framework checkout, index or CLI in the target repository.
- Use hosted real-artifact checks because local container execution did not provide a connected repository checkout. The temporary verification PRs [#736](https://github.com/ThorStarlord/sensemaking-skills/pull/736), [#737](https://github.com/ThorStarlord/sensemaking-skills/pull/737) and [#739](https://github.com/ThorStarlord/sensemaking-skills/pull/739) were **closed without merging**, leaving the permanent CI workflow set unchanged. The corrected-source verification after Markdown fixes was used for final installed-delivery evidence.
- No independent subagent reviewer was available. The twelve-question case reconstruction and diff/source review were conducted by the implementing author. That is weaker evidence than a fresh independent normal-use session. It is stated explicitly rather than portrayed as independent qualification.

### Verification scope, nonclaims and stop

**PASS:** source and diff inspection, source-qualified case identity, internal link paths, no literal escaped Markdown ticks after repair, hosted authored-knowledge proposal and committed index, explicit search/explain results, real wheel and fresh project installed reference parity, and canonical receipt validation. **NOT_RUN:** local unit and synthetic evidence tests, under the then-current repository-local construction policy. Hosted CI is revision-specific; report final administrative PR/main reruns by their observed status, not by assumption.

**NOT ESTABLISHED:** general creative improvement, independent agent repeatability, relative owner benefit, semantic truth of every historical judgment, causal graph advantage, automatic host loading, strategic product attractiveness or any authorization to implement the ranked inquiries. This implementation explicitly creates no ranked backlog.

**Conditional continuation only:** C-A parsed artifact requires a real machine consumer; C-B schema/query extension requires an authentic lost distinction under existing mechanisms; C-C independent benefit requires genuinely open tasks and suitable independent observations; C-D strategic adoption and implementation priority require their respective authority. None is a core implementation completion prerequisite.

**Stop disposition:** all seven core responsibilities are implemented, source-reconciled and durably retained. The implementation receipt records `GOAL_SATISFIED` for the authorized ontology v1, with empirically unqualified benefits preserved as a nonblocking question.
