# Convergent Evaluation and Direction Selection Ontology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended when independently available) or superpowers:executing-plans. Work task-by-task; record steps with `- [ ]` checkboxes. This is an implementation plan, not evidence that its steps have been performed.

**Goal:** Make a convergent assessment's transition into a **justified, scoped direction selection—or an explicit non-selection** source-reconstructible across agents and sessions, without promoting comparative preferences into authority or implementation.

**Architecture:** Reuse the existing Possibility Assessment ontology, Warrant / Choice policy, Prospective Reasoning decision semantics, and existing historical records. Add a focused conceptual ontology, portable selection guide and optional documentary record, pinned cases, and a small selective existing-schema source projection. Expose the guide conditionally through existing Skills. Do not introduce a selection engine, new public Skill, required stage sequence, ranking algorithm, or schema changes without a demonstrated consumer.

**Tech Stack:** Markdown conceptual ontology; installed Skills and Markdown references; existing JSON reviewed-knowledge contract (`schema_version: 1`) and current `sensemaking-skills` semantic CLI; GitHub PRs, source-linked history, built wheel and isolated `entrypoint` installation. No new runtime dependency in v1.

**Spec:** [Convergent Evaluation and Direction Selection Ontology v1 — Design Basis](../specs/2026-11-04-convergent-evaluation-direction-selection-ontology-design.md).

**Planning baseline:** `ThorStarlord/sensemaking-skills@4ef254cd6251e515910e2187de22195d0e49401d` (2026-11-04). Refresh HEAD, governing docs, local instructions and source identities at execution.

**Status:** **IMPLEMENTED (core v1) — 2026-11-04.** Seven bounded tasks / fifty checkable steps were completed under the explicit owner implementation request, with substantive implementation merged in PRs #742, #743 and #745. The final administrative closeout records the validated receipt. No future product direction was selected or authorized by this ontology implementation.

## Global constraints

- **G1 — Source and authority first:** Read the current `CLAUDE.md`, accepted ADRs 0029/0031/0034, existing [Possibility Assessment ontology](../../semantic-architecture/possibility-assessment-ontology.md), [Prospective ontology](../../semantic-architecture/prospective-reasoning-ontology.md), [Product Possibility ontology](../../semantic-architecture/product-possibility-ontology.md), [Warrant / Choice policy](../../../skills/using-sensemaking/references/warrant-choice-policy-v0.md) and relevant case sources before editing. Preserve current product identity and single `using-sensemaking` entrypoint.
- **G2 — Selection is not comparison:** A `PortfolioSnapshot`, top-ranked inquiry, `AssessmentJudgment` and `ProvisionalPreference` do not create `Decision` or action authorization. Selection requires a real actor, scope and applicable authority.
- **G3 — Warrant and comparative advantage are distinct:** A preferred alternative can still be unwarranted. Candidate-specific premises/evidence and comparison under a common purpose must both be reconstructible.
- **G4 — No manufactured winner:** `NO_SELECTION`, owner decision required, more evidence, incomplete options, conditional preference and non-adoption are valid outcomes. Do not invent an option to make a minimum count.
- **G5 — Typed target identity:** Preserve source qualified `InquiryQuestion + ProposedInquiryApproach`, `ProductPossibility`, `ArchitectureOption`, `ConstructionPath` and authorized work units. `SelectedDirection` is a **role** in a decision, not a universal new target entity.
- **G6 — Selection scope matters:** Record what a choice actually settles, the accepted tradeoffs, what remains open, and what a returning agent may inherit. A selected inquiry does not select a product thesis, a strategic path or implementation.
- **G7 — Credible alternatives survive:** Source-local IDs, grouping grounds, nonselected/disputed/outside-frame dispositions and historical assessments remain accessible. Do not equate nonselection with rejection or duplicate grouping with identity.
- **G8 — Reconsideration is bounded:** Preserve historical decision identity. A changed premise, owner goal or source may justify a currentness/target-warrant check, not automatic reopening or a different downstream Skill.
- **G9 — No unsupported composite selection:** A new synthesis needs explicit combined meaning, assessed assumptions/consequences and proper authority; collecting positive labels is not a warranted future.
- **G10 — Portable and light:** The guide must work from installed reference text and target-repository evidence without a framework checkout, SQLite or a new mandatory artifact. Existing ADR/PR/strategic report/receipt/handoff surfaces carry real decisions.
- **G11 — Schema growth is conditional:** Do not widen current `ComparativeJudgment evaluates`, `ProvisionalPreference prefers` or `Decision selects` architecture/path endpoints by analogy. No new machine predicate, `artifact_id`, universal state enum, planner or ranking engine absent a real lost answer/parsed consumer and separate schema authorization.
- **G12 — Local verification policy:** Recheck repository instructions at implementation. At planning time, they explicitly disallow creating or manually running local unit or synthetic-evidence tests in this repository's construction phase. Use source/diff review, actual artifact/contract checks, real exact-commit retrieval, wheel parity and hosted CI where warranted. Mark `NOT_RUN` truthfully; never remove hosted protections.
- **G13 — Evidence ceiling:** Structural validity, source fidelity, retrieval, installed files and an author reader exercise do not demonstrate independent creative improvement, superior owner choice, automatic host loading or executed work.
- **G14 — User scope:** Implement the bounded ontology and integration only once separately authorized; do not take a plan request as a request to select a product direction or perform that choice's downstream work.

## Review focus: five high-risk failure cases

| Failure to prevent | Expected correct behavior | Owning task |
| --- | --- | --- |
| The November 4 portfolio's recommended owner-agency inquiry is treated as an owner-adopted direction | Preserve **recommendation only** unless a separate actual selection source is found | 1, 2, 3, 6 |
| ADR 0034's owner-ratified product identity becomes equivalent to an inquiry priority | Keep **Level-4 adopted product thesis** separate from a bounded next-question choice | 1, 2, 6 |
| A preferred but unwarranted direction is forced into a decision | Record comparative advantage separately from candidate-specific warrant; valid `NO_SELECTION` | 1, 2, 3, 6 |
| Nonselected alternatives or new composite lose their lineage | Preserve every original alternative; synthetic combined option needs independent grounds and conditional consequences | 1, 2, 6 |
| A selected direction automatically launches coding or reverses history | Selection scope / authorization boundaries are explicit; returning agent checks only decision-critical prerequisites; old decision stays historical | 1, 3, 4, 6 |

---

## 1. File map and responsibility boundaries

### New files

| File | Responsibility |
| --- | --- |
| `docs/semantic-architecture/convergent-direction-selection-ontology.md` | Canonical conceptual roles, target/decision/authority relationship meanings and reconsideration invariants |
| `docs/semantic-architecture/convergent-direction-selection-competency-v1.md` | Local competency questions, existing concept mapping, documentary fit and actual verification account |
| `docs/semantic-architecture/convergent-direction-selection-reference-cases-v1.md` | Source-pinned historical cases and clearly labeled hypothetical negative cases |
| `skills/strategic-repository-analysis/references/convergent-direction-selection-v1.md` | Portable agent guidance for deciding whether selection is warranted, making/recommending scoped choices, and handing off |
| `skills/strategic-repository-analysis/references/convergent-direction-selection-record-template.md` | Optional Markdown form, sparse by default, for a consequential retained convergence/selection |
| `.sensemaking/knowledge/convergent-direction-selection.json` | **Conditional in content, planned file**: bounded definitions and one source-case claim using supported v1 claim kinds/predicates; omit the file if no independently useful retained knowledge can be justified |

### Existing files: minimal targeted edits only

| File | Scope |
| --- | --- |
| `docs/semantic-architecture/ontology.md` | Brief extension/navigation link, no changed meaning of `Decision` |
| `docs/semantic-architecture/prospective-reasoning-ontology.md` | Short cross-reference to scoped selection role; keep architecture/path endpoint constraints |
| `docs/semantic-architecture/possibility-assessment-ontology.md` | Clarify downstream selection boundary, not a new assessment method |
| `docs/semantic-architecture/relations-and-epistemics.md` | Crosswalk of documentary relationships only, no executable predicate |
| `docs/semantic-architecture/competency-questions.md` | Link new *local* questions without inventing global CQ numbers |
| `docs/semantic-architecture/README.md` | Discovery links to ontology, cases and fit account |
| `skills/using-sensemaking/SKILL.md` | One conditional cue **only if** it changes the first-load decision |
| `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md` | Distinguish Level-3 comparative selection from exploration-only and owner-reserved choices |
| `skills/using-sensemaking/references/warrant-choice-policy-v0.md` | Optional pointer **only if** needed; do not change policy's disposition meanings |
| `skills/using-sensemaking/references/adaptive-skill-composition-v1.md` | Optional pointer **only if** an existing wording confuses specialist recommendation with controller adoption |
| `skills/repository-semantic-steward/references/knowledge-contract.md` | Optional selective-retention boundary only if existing guidance is unclear |
| `docs/explorations/README.md` | Show how nonselected and selected historical outcomes differ, without changing the archive |
| `STATUS.md` | Update only for a material, *verified* capability change |
| `docs/superpowers/plans/2026-11-04-convergent-evaluation-direction-selection-ontology.md` | Checklist, real observations, PR references and closeout after execution |
| `.sensemaking/receipts/YYYY-MM-DD-convergent-direction-selection-ontology-implementation.session.yaml` | Existing receipt when implementation is actually performed and its authority/persistence warrants a receipt |

Do **not** rewrite historical convergence reports, existing ADR decisions, curated possibilities, old portfolio rankings, code packages, installer profiles, graph parser/schema, planning runtime, or external product strategies to satisfy this plan.

## 2. Dependencies and increments

Suggested sequence (bounded PRs, not a mandatory pipeline): **A. conceptual foundation (Task 1)** → **B. cases and portable profile (Tasks 2–3)** → **C. minimal integration and selective knowledge (Tasks 4–5)** → **D. verification and source reconciliation (Tasks 6–7)**. Tasks 4 and 5 can be prepared in parallel after Task 3, but both must be reconciled with the final case source and target revision. Each PR needs a source-grounded decision note, actual source/diff verification and an accurate CI status. Follow current branch/merge protections.

### Task 1: Define convergence-specific semantics and competency questions

**Files:**
- Create: `docs/semantic-architecture/convergent-direction-selection-ontology.md`
- Create: `docs/semantic-architecture/convergent-direction-selection-competency-v1.md`
- Modify (minimal): `docs/semantic-architecture/ontology.md`, `docs/semantic-architecture/possibility-assessment-ontology.md`, `docs/semantic-architecture/prospective-reasoning-ontology.md`, `docs/semantic-architecture/relations-and-epistemics.md`, `docs/semantic-architecture/competency-questions.md`

**Consumes:** accepted design spec and current Layered/Divergent/Assessment/Prospective models plus Warrant / Choice policy.
**Produces:** stable documentary roles/relationship meanings for cases and the portable profile.

- [x] **1.1 Pin source and authority:** record exact HEAD, current local instructions, accepted ADRs and existing `Decision`/`ComparativeJudgment` endpoints. Explain which roles can reuse existing concepts and which are new descriptive specializations.
- [x] **1.2 Define choice objects:** ChoiceQuestion, ConsideredChoiceSet and typed target references including `InquiryQuestion+ProposedInquiryApproach`, product future, architecture/path, and separately authorized work; preserve original identities.
- [x] **1.3 Define justification and rationale:** distinguish CandidateWarrant from ConvergenceRationale; include evidence, defeaters, currentness, rejected/conditional premises and meaningful alternative comparators.
- [x] **1.4 Define ScopedDirectionSelection:** require an actual attributable selecting actor/authority, selected target, choice question, scope, what is settled/open, date and reconsideration; explicitly distinguish recommendation, preference, adoption and implementation permission.
- [x] **1.5 Define nonselection and history:** AlternativeDispositionAccount, SelectionReconsiderationBoundary, SelectionHandoff; allow no-selection, underdeveloped options, owner-reserved and revised choices without forced ranking or silent historical overwrite.
- [x] **1.6 Write local semantic relationship/endpoints crosswalk:** explain all relationships as documentary, reuse existing Decision/Claim meanings, preserve architecture/path `evaluates`/`prefers`/`selects` restrictions and do not create executable predicates.
- [x] **1.7 Draft local competency matrix:** map each question in §3 below to existing global CQ/PAO-CQ sources; record baseline faithful/awkward/lost/not established from actual sources without presenting examples as independent trials.
- [x] **1.8 Review and commit the semantic increment:** inspect source/diff, local links, contradictions and the five Review Focus failures; stop at a genuine product-thesis/ontology-authority conflict rather than silently extending authority.

**Acceptance:** a reader can describe what a choice settles, why selection is more than comparison, what `NO_SELECTION` means and why "selected inquiry" cannot mutate accepted strategy. No new runtime/typed graph endpoint.

### Task 2: Create source-pinned reference cases and negative examples

**Files:**
- Create: `docs/semantic-architecture/convergent-direction-selection-reference-cases-v1.md`
- Modify: `docs/semantic-architecture/convergent-direction-selection-competency-v1.md`

**Consumes:** Task 1 roles; ADR 0034; November 3/4 convergence/portfolio reports; prospective and Warrant policy sources.
**Produces:** trustworthy annotated cases, including a genuinely ratified decision and genuine nonselection.

- [x] **2.1 Pin all containing file revisions:** identify source files, actual revisions containing judgments, earlier source baselines they inspected, author vs owner attribution, and quotation/interpretation boundaries.
- [x] **2.2 Case S1 — no selected direction:** reconstruct November 3 nonbinding convergence and its qualified directions for separate depth; explain why it is not a `ScopedDirectionSelection`.
- [x] **2.3 Case S2 — recommendation versus adoption:** reconstruct November 4 owner-agency **recommended inquiry**, its reasons/reversal conditions and distinct strategic Futures+Continuity synthesis without inventing owner selection.
- [x] **2.4 Case S3 — actual adopted selection:** reconstruct ADR 0034's owner-ratified Level-4 product direction, authority, adopted scope, boundaries and continuing prior ADRs; never label it fresh empirical validation.
- [x] **2.5 Case S4 — architectural preference and feedback:** use prospective ontology's architecture option/conditional feedback source to explain `ProvisionalPreference`, reopened consequences and need for separate `Decision`/action authority.
- [x] **2.6 Case S5 — no-selection / option-set incomplete:** use Warrant / Choice and owner-decision-capsule policy as **normative/illustrative** cases; do not present them as a historical observation that an agent actually made this choice.
- [x] **2.7 Case S6 — synthesis versus adoption:** document why a composite future needs separately assessed benefits/costs/assumptions and cannot be called selected merely because November 4 found the synthesis attractive.
- [x] **2.8 Source and counterexample review:** preserve original candidate IDs, missing authority, decline/defer/retained-alternative meanings, case labels and links; correct a source conflict rather than fabricate a more dramatic selection.

**Acceptance:** the source record distinguishes **recommended**, **owner-ratified**, **provisional**, **no selection**, **option-set incomplete**, and **hypothetical synthesis**; all original reports remain unchanged.

### Task 3: Build a portable convergence/selection profile and optional record

**Files:**
- Create: `skills/strategic-repository-analysis/references/convergent-direction-selection-v1.md`
- Create: `skills/strategic-repository-analysis/references/convergent-direction-selection-record-template.md`

**Consumes:** Task 1 definitions and Task 2 historical cases.
**Produces:** self-contained guidance for the active agent and durable records for a future reader.

- [x] **3.1 Write standalone scope/warrant guidance:** use a current goal, current sources, existing assessment and governing authority; select a bounded convergent responsibility only when the decision is actually open.
- [x] **3.2 Explain adequacy of considered set and target-specific warrant:** check missing options and decisive prerequisites before picking, with clear `NO_SELECTION`, `MORE_EVIDENCE_REQUIRED`, `OWNER_DECISION_REQUIRED` and `OPTION_SET_INCOMPLETE` interpretation anchored to existing policies.
- [x] **3.3 Explain comparative preference versus choice:** present why a target warrants pursuit at all **and** why it better addresses the choice question than alternatives. Allow uncertainty, conditional preferences, ties, credible complements and different beneficiary frames.
- [x] **3.4 Define choice-scope guidance:** what is settled, left open, decision actor and delegated authority, accepted costs, consequences, and an explicit "what later agents may inherit" boundary; no automatic Skill transition or execution.
- [x] **3.5 Write optional sparse Markdown record:** date, source/revisions, typed targets, purpose/authority, available alternatives, warrant/defeaters, rationale, *actual status* (recommendation / selection / nonselection), alternatives' dispositions, handoff/reopen triggers and stop.
- [x] **3.6 Add compact worked distinctions:** no-selection despite preference, inquiry selection versus product thesis, declined alternative versus out-of-frame, conditional synthesis and owner-reserved escalation; explicitly mark illustrations.
- [x] **3.7 Portability review and commit:** the installed reference must be usable without the framework checkout or target `CLAUDE.md`. Require neither a new mandatory form nor full Level-3 Strategic Analysis for a bounded choice.

**Acceptance:** a fresh agent can read the installed guide and produce a meaningful selected-or-not-selected outcome without false authority; a short low-stakes decision need not become an eight-section artifact.

### Task 4: Integrate the selection profile at warranted existing entrypoints

**Files:**
- Modify minimally: `skills/using-sensemaking/SKILL.md` (conditional)
- Modify: `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`
- Modify only if necessary: `skills/using-sensemaking/references/warrant-choice-policy-v0.md`, `skills/using-sensemaking/references/adaptive-skill-composition-v1.md`, `skills/repository-semantic-steward/references/knowledge-contract.md`

**Consumes:** stable portable path from Task 3.
**Produces:** discoverable guidance without changing controller ownership.

- [x] **4.1 Inspect actual entrypoint trigger semantics:** determine whether current first-load references already cover a standalone "which direction should guide further work?" request; record justification for each edit.
- [x] **4.2 Add the smallest conditional cue:** point to `convergent-direction-selection-v1.md` only when a warranted selection/nonselection question is material; avoid loading for every divergent or comparative assessment.
- [x] **4.3 Clarify existing strategic funnel:** a Level-3 selection may consume assessed directions and Warrant/Choice, while a standalone Convergent Evaluation may stop without Level-3 frontier/path or implementation.
- [x] **4.4 Preserve ownership of choice and evidence return:** specialist recommendation goes back to active agent; an owner-reserved selection goes to the existing decision-capsule path; no specialist-to-specialist automatic execution.
- [x] **4.5 Check reference/package reachability:** the current `entrypoint` profile must contain all needed Skill paths; no new public Skill, install profile, parser or workflow change.
- [x] **4.6 Review minimal integration diff:** check negative cases (portfolio recommendation not accepted decision; selected direction not execution; no policy-disposition changes); commit with an exact source-grounded PR note.

**Acceptance:** a first-load agent can find the profile for an explicit selection responsibility, but ordinary bounded comparisons and already-authorized repairs remain light.

### Task 5: Retain selective reviewed semantic knowledge only where justified

**Files:**
- Create conditionally: `.sensemaking/knowledge/convergent-direction-selection.json`
- Modify: `docs/semantic-architecture/convergent-direction-selection-competency-v1.md`

**Consumes:** Task 1 concept definitions, Task 2 source-case document, existing knowledge contract and CLI.
**Produces:** source-linked discoverability using accepted v1 shapes, or an evidenced decision that no pack is needed.

- [x] **5.1 Inspect current `knowledge-contract.md` and parser:** record allowed kinds/statuses/predicates and source-reference rules, including whether `domain_concept`, `source`, and `references` suffice. Do not infer attributes from prior reports.
- [x] **5.2 Decide selective knowledge scope:** add only durable shared concept definitions and a dated case-source reference if they materially assist recall; **do not** ingest all ranked directions or claim an enacted Decision from policy/examples.
- [x] **5.3 If warranted, author existing-schema JSON:** choose distinct IDs from the current knowledge pack, correct tracked source paths and epistemic statuses; relations use only supported predicates, with no new endpoint semantics.
- [x] **5.4 Validate the authored proposal:** run `python -m sensemaking_skills.cli semantic knowledge-proposal-check --repo . --proposal .sensemaking/knowledge/convergent-direction-selection.json --json` from a checkout with the CLI; expected accepted records without source/schema errors. If no pack was warranted, mark this check `NOT_APPLICABLE` in prose, **not** PASS.
- [x] **5.5 Reconcile any checker failures from source and contract:** correct actual errors without weakening validation; a failed/unrun pack remains draft and is not described as reviewed.
- [x] **5.6 Commit the selective pack or recorded no-change decision:** no archive rewrites, no pseudo-canonical selected-direction graph nodes, no invented endorsement.

**Acceptance:** retained knowledge is structurally checked, traceable and clearly distinct from decisions; or its omission is justified because existing source records already provide sufficient recovery.

### Task 6: Perform source/currentness, retrieval, installation and reader checks

**Files:**
- Modify: `docs/semantic-architecture/convergent-direction-selection-competency-v1.md`
- Modify cases/guide only to repair grounded defects.

**Consumes:** committed Tasks 1–5 at an identified revision.
**Produces:** specific evidence for delivered meanings, without claiming independent performance.

- [x] **6.1 Inspect source integrity:** verify changed Markdown links, source-file revisions, case labels and original intended decision status (provisional/recommendation/owner decision); preserve original archive documents.
- [x] **6.2 Check actual retained-knowledge/index when applicable:** build an exact-commit index using current `sensemaking-skills semantic knowledge-build --repo . --repository ThorStarlord/sensemaking-skills --target-ref <HEAD_SHA> --db <TEMP_SQLITE> --json`; record actual result and source revision. If no pack, use source-only evidence without misreporting retrieval.
- [x] **6.3 Search and explain source-scoped concepts when applicable:** use `sensemaking-skills semantic knowledge-query --db <TEMP_SQLITE> --repository ThorStarlord/sensemaking-skills --target-ref <HEAD_SHA> --operation search --term "ScopedDirectionSelection" --json` plus `--operation explain --subject <ACTUAL_ID> --json`; inspect paths, actual claim status, exact source hashes and absence of asserted authority.
- [x] **6.4 Build an actual wheel and install entrypoint:** use current documented wheel mechanism in an isolated environment, run `sensemaking-skills setup-skills --target claude --scope project --project-root <TEMP_PROJECT> --profile entrypoint`, and compare installed and source reference trees, including the new guide/template.
- [x] **6.5 Perform a source-only cold-reader reconstruction:** a genuinely fresh reader if available, otherwise an explicitly labeled author cold-read, answers the local competency questions without using unseen conversation memory.
- [x] **6.6 Challenge the five Review Focus failures:** verify the reader rejects owner adoption from portfolio recommendation, refuses a forced winner/forced merge, preserves original alternatives, distinguishes strategy choice from selected inquiry, and cannot turn a scope-limited choice into build authority.
- [x] **6.7 Log evidence ceilings and actual status:** record source SHA, command/results or absence, qualitative fit per question, CI jobs, `NOT_RUN` local tests and lack of independent creative-benefit observation. Repair a concrete documented failure before final closure.

**Acceptance:** all decision-critical meanings are recoverable with inspected sources and valid installed guidance, or an honest unresolved defect with a justified stop; delivery does not falsely imply semantic truth or authorization.

### Task 7: Reconcile navigation, actual completion, and continuation

**Files:**
- Modify: `docs/semantic-architecture/README.md`, `docs/explorations/README.md`
- Modify only if warranted: `STATUS.md`
- Modify after actual work: this plan and `docs/semantic-architecture/convergent-direction-selection-competency-v1.md`
- Create after actual work when warranted: `.sensemaking/receipts/YYYY-MM-DD-convergent-direction-selection-ontology-implementation.session.yaml`

**Consumes:** source-reviewed merged increments and verification evidence from Task 6.
**Produces:** an accurate durable record of what was implemented and what remains outside this scope.

- [x] **7.1 Add semantic architecture navigation:** link ontology, cases, competencies and installed profile; distinguish conceptual Level-2 semantics from any selective Level-3 checked knowledge.
- [x] **7.2 Add historical exploration navigation:** show that the archive contains unselected evaluations, recommendations, provisional preferences and an actual owner-ratified ADR in different authority contexts; do not reinterpret the reports.
- [x] **7.3 Review cross-layer authority and history:** verify no changed ADR, historical candidate disposition, accepted strategic commitment, execution contract or new router; no future direction automatically becomes selected because the ontology exists.
- [x] **7.4 Reconcile actual construction evidence:** update status only for material capability; record merged PRs, exact heads, source-vs-installed parity, uncertainties, test `NOT_RUN` and conditional schema/empirical follow-ups.
- [x] **7.5 Complete this checklist honestly:** mark only performed steps after relevant merges; record separate disposition for any conditional unexecuted action. Do not write a success claim for an unchecked knowledge pack or absent reader observation.
- [x] **7.6 Persist and validate the existing receipt when warranted:** use the actual `sensemaking_session_receipt` contract, source/skill/goal/authority, completed responsibilities, real validation and stop; a receipt never confers authority. Validate through `scripts/validate-receipt.py` when runtime is available.
- [x] **7.7 Final source/diff review and merge within current policy:** include source-grounded decision notes, preserve protected branch rules and hosted CI; inspect canonical `main` file identity and report pending runs accurately.
- [x] **7.8 Stop at the bounded v1 goal:** do not automatically implement a direction selected by a *future* Convergent Evaluation or launch independent creative qualification. Record genuine follow-ups separately.

**Acceptance:** canonical repo has the reviewed ontology, portable guide, source cases and checkable completion evidence; historical choice and authority meanings are preserved. No unfinished core task is hidden by a generic "done" claim.

## 3. Local competency questions and source targets

New local identifiers are **CDS-CQ-01..14**; they should cross-link existing global CQs and PAO-CQ without inventing conflicting canonical IDs.

| Question | Critical evidence / case | Owning tasks |
| --- | --- | --- |
| **01** What decision question, target kind, actor and authority are actually in scope? | ADR 0034 versus portfolio inquiry | 1, 2, 6 |
| **02** Which credible alternatives were considered, and were material alternatives omitted? | November 3 non-ranked map; owner capsule option-set adequacy | 1, 2, 6 |
| **03** Is each candidate warranted *at all* independently of its relative appeal? | Warrant/Choice prerequisites and genuine no-selection | 1, 3, 6 |
| **04** Why is the preferred candidate better for this purpose, including accepted tradeoffs? | November 4 qualitative comparison | 1, 2, 3 |
| **05** Is this a comparison, recommendation, provisional preference, actual decision or authorization? | Portfolio vs ADR 0034 | 1, 2, 6 |
| **06** Does the selected target remain the same source-qualified inquiry/product/architecture/path? | Named target IDs across source cases | 1, 2 |
| **07** What exactly does a selection settle and leave open? | ADR 0034 and bounded inquiry example | 1, 2, 3 |
| **08** What happens to declined, deferred, retained/complementary and outside-frame alternatives? | November 3 and November 4 portfolios | 1, 2, 6 |
| **09** What evidence or premise could reverse a selection, and who may reconsider it? | Warrant/Choice currency; strategic feedback | 1, 2, 6 |
| **10** How is a composite direction distinguished from a list of attractive ingredients? | Futures+Continuity synthesis **not** new ratification | 1, 2, 6 |
| **11** What is the valid result when no candidate warrants selection or options are inadequate? | Warrant `NO_SELECTION`; owner capsule incomplete set | 1, 2, 3 |
| **12** Can a later agent inherit the selected direction without automatic execution or full strategic reopening? | Selected work vs controller/authority boundary | 1, 3, 4, 6 |
| **13** Does source-file revision differ from inspected-target revision and decision date? | Actual historical report/ADR dates | 2, 6 |
| **14** Does a graph/receipt/contract PASS establish truth, owner preference or action permission? | Knowledge + installed/receipt checks | 5, 6, 7 |

Assess as `faithful`, `awkward`, `lost` or `not established` **at documentary representation level**. A source-pinned example or author cold-read is not an independent creative-use trial.

## 4. Conditional follow-ups outside this implementation

- **C-A — Parsed selection artifact:** Only after a named producer/consumer needs specific reliable machine fields and existing Markdown/ADR/PR/receipt/strategic contract cannot provide them. Document compatibility and authority before changing `artifact-contracts.yaml`.
- **C-B — Graph vocabulary or retrieval extension:** Only after a real comparison/selection-revision question loses a necessary identity, dependency or scope relation under existing claims/references/attributes; demonstrate the loss and alternatives. No generic `selectsProductPossibility` predicate by analogy.
- **C-C — Independent quality/creative benefit:** Separate normal-use qualification with genuine open decisions, reviewers and consent/access; differentiate source-only context from typed-memory and prompt effects. No automatic experiment.
- **C-D — Actual strategic adoption or implementation:** Owner- or delegation-authorized choices go through the appropriate ADR/Level-3/engineering authority; merely creating an ontology does not select a direction in this repository.

## 5. Risk controls and explicit stop

| Risk | Mitigation |
| --- | --- |
| Convergence model merely duplicates assessments | Focus on **choice transition**, actor/authority, scope, nonselected alternatives and justified continuation |
| Generic "SelectedDirection" becomes a new entity for everything | Reuse typed referents; decision refers to them in one scope |
| No-selection forced to look like failure | Model it as legitimate result; keep option-set-incomplete distinct |
| Owner-reserved decision is inferred from recommendation | Require actual ratification source; ADR 0034 positive control |
| Synthesis appears to inherit benefits without costs | Explicit new meaning, conditional consequence assumptions and re-evaluation |
| Later agents ignore selected choice or follow it blindly | Preserve scope/prerequisite and reconsideration; neither reopen by default nor auto-execute |
| Portable Skill guidance needs framework checkout | Self-contained reference with target-repository authority and source requirements |
| Knowledge schema accidentally gains normative selection truth | Selective source/definition projection only; no new predicate or status |
| Validators/CI overstated as product benefit | Separate source/document fidelity, graph structure, installed parity, independent behavior and owner value |

**Definition of complete:** Tasks 1–7 are performed within current authority; all source-grounded semantics, guide/templates, case meanings and links are discoverable; any checked knowledge and installed package are verified on actual sources; the final record distinguishes actual outcomes and `NOT_RUN`. No conditional follow-up is a v1 prerequisite without a separately justified reason.

**Handoff:** Future executor reads the spec and plan, checks HEAD/current authority, performs the bounded tasks, uses fresh reviewers if genuinely available, and stops at the selection-ontology boundary. Plan creation alone does not implement or ratify its contents.

**Current disposition:** **CORE IMPLEMENTATION COMPLETE.** This remains a documentary/conceptual capability. Conditional parsed artifacts, graph schema extensions and independent quality qualification are separate, presently unwarranted responsibilities.


## 6. Implementation completion account — 2026-11-04

**Owner authorization:** The owner explicitly requested that the agent implement all tasks without intermediate approval, make bounded implementation decisions, and continue until the plan's completion boundary. The owner did **not** separately ratify the example product directions discussed in the historical reference cases.

**Implemented architecture:** focused conceptual `Convergent Evaluation and Direction Selection` ontology built on existing Possibility Assessment, Prospective Reasoning and Warrant / Choice meanings. One optional portable guide/record, source-pinned documentary examples, a selective v1 knowledge pack, and conditional entrypoint navigation. It changes neither the active-agent controller, strategic authority, nor any executable ranking/selection contract.

| Task | Result | Actual integration / evidence |
| --- | --- | --- |
| **1 — Ontology and competencies** | Choice question/set, CandidateWarrant, ConvergenceRationale, ScopedDirectionSelection, AlternativeDispositionAccount, reconsideration/handoff, and 14 local competency questions, with narrow predicate endpoints retained | [PR #742](https://github.com/ThorStarlord/sensemaking-skills/pull/742) merged at `d1d77a29034cede7ec2d1676c061ab1fbcd09217`; [ontology](../../semantic-architecture/convergent-direction-selection-ontology.md) and [competencies](../../semantic-architecture/convergent-direction-selection-competency-v1.md) reviewed. |
| **2 — Source-bound cases** | Six sections preserving Nov 3 unselected convergence, Nov 4 recommendation, owner-selected ADR 0034, provisional architecture preference, policy NO_SELECTION/incomplete options, and hypothetical synthesis | [Source-pinned cases](../../semantic-architecture/convergent-direction-selection-reference-cases-v1.md) inspect the **containing source snapshot** `ad223927e533268b2867d07851f1993860ace647` separately from historical inspected baselines. Cases S5 and parts of S6 are explicitly normative/illustrative. |
| **3 — Portable profile** | Self-contained [guide](../../../skills/strategic-repository-analysis/references/convergent-direction-selection-v1.md) and [optional Markdown record](../../../skills/strategic-repository-analysis/references/convergent-direction-selection-record-template.md) | Merged in #742; the actual installed copies were compared byte-for-byte to source in the hosted wheel check. |
| **4 — Conditional integration** | One conditional first-load `using-sensemaking` entry, Level-3 funnel clarification, and selective-retention crosswalk in Steward reference | [PR #743](https://github.com/ThorStarlord/sensemaking-skills/pull/743) merged at `a3914b736cc82314833b27d30be8481b9f0a3c6a`. The other controller/policy references already preserved specialist-return and owner boundaries and required no additional edit. |
| **5 — Reviewed knowledge** | `schema_version:1` source-authored pack containing **8 declared concept definitions, 1 observed case-document claim and 5 supported `references`** | Existing [Source-pinned context consumer](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41945851917/job/126977729220) on #743 head `b10cb3f348084707470935dc786aecadc9a82db4` ran proposal checks and exact-commit graph build: **PASS**. No proposed Decision instances or new predicates. |
| **6 — Real retrieval, installed delivery and source reconstruction** | Actual `ScopedDirectionSelection` search/explain and case-source explain; built wheel, isolated `entrypoint` install, comparison with source, fourteen-question author reconstruction | Hosted [real-path job](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41945927998/job/126977985070) at `262bdb1975bf8fd2dcfe886bc1509ccecde4f8b5` logged **`CONVERGENCE_PROPOSAL_INDEX_SEARCH_EXPLAIN_PASS`** and **`CONVERGENCE_INSTALLED_REFERENCE_PARITY_PASS`**; all job steps passed. The six tested substantive file blobs matched published `main@a3914b7`. |
| **7 — Reconciliation** | Semantic navigation, Exploration Atlas, status, actual evidence ceilings, completed checklist and immutable session receipt | [PR #745](https://github.com/ThorStarlord/sensemaking-skills/pull/745) merged at `b82f9ffecd363867f23044ad047d459b211e35a0`. Canonical receipt [validator job](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41946305671/job/126979250896) returned **`RECEIPT_VALID`**. This final administrative increment publishes the plan/receipt together. |

### Review and consequential rulings

- The meaningful increment is **choice transition semantics**, not a second assessment framework: a target may be comparatively first yet **not warranted** at all; a recommendation is not a ratified Decision.
- `ScopedDirectionSelection` is a **role of a sourced existing Decision**, not a new global selected-target identity or machine kind. The same `poss:`, `arch:`, inquiry+approach and path referents persist.
- Actual owner decision is sourced by ADR 0034. The November 3 convergence and November 4 inquiry portfolio contain **no equivalent owner adoption**. No historical source, ADR, candidate disposition or portfolio rank was rewritten.
- The current `Warrant / Choice Policy`, `owner-decision-capsule` and active-agent controller already cover legitimate no-selection, option-set incompleteness, reserved decisions and premise checks. No alternative selection engine, fixed stage machine, numeric score, public Skill or workflow profile was added.
- The current v1 graph record needs only checked `domain_concept`/`source`/`references`. No identified consumer or unrecoverable decision-scope distinction justified adding a new parsed artifact, predicate, `Decision selects` target kind, mandatory handoff or bulk knowledge migration.
- A successful ontology record does not provide owner ratification or permission to build, merge, deploy or conduct an external empirical investigation.

### Verification performed and boundaries

**PASS:** source/diff and historical identity review; six pinned case interpretations; new code-span/source link inspections; checked v1 knowledge proposal and exact committed index; query/search and explain for a defined selection concept and case-source claim; actual wheel built and installed into a fresh project; byte-for-byte parity of source and four installed references; canonical receipt validation.

**NOT_RUN:** local unit tests and synthetic evidence tests under this repository's then-current owner construction policy. Existing hosted CI/protections were preserved.

**NOT_ASSESSED:** genuinely independent fresh-reader reasoning, independent choice-quality improvement, owner satisfaction, incremental effect of typed graph relationships, automatic host loading, or causal source-only versus memory benefit. The fourteen-question source reconstruction was conducted by the **author**, not a separately commissioned agent. Source fidelity is not an empirical user outcome.

**Temporary verification CI:** [PR #744](https://github.com/ThorStarlord/sensemaking-skills/pull/744) (real graph/wheel) and [PR #746](https://github.com/ThorStarlord/sensemaking-skills/pull/746) (receipt validator) were **closed without merge**. No temporary GitHub Actions workflow was added to main.

### Conditional research, not leftover core tasks

- **C-A parsed artifact:** only after a named producer/consumer demonstrates a stable field handoff missing from readable source decisions.
- **C-B graph/query evolution:** only after an authentic retrieval question loses a necessary scoped-selection relationship under existing claims, source links and accepted artifact contracts.
- **C-C independent benefit:** only through separately warranted authentic inquiries and review; historical examples and author reconstruction count as zero independent qualification trials.
- **C-D product adoption or construction:** must follow the existing owner/strategic/implementation authority. No ontology implementation automatically selects an actual product future.

**Stop:** the seven authorized tasks have bounded deliverables, verified retrieval/installed distribution, source-reconstructible semantics and a completed receipt. The final [receipt](../../../.sensemaking/receipts/2026-11-04-convergent-direction-selection-ontology-implementation.session.yaml) records `GOAL_SATISFIED` without inflating the claim ceiling.

