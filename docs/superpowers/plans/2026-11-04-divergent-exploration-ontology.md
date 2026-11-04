# Divergent Exploration Ontology Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give coding agents a usable ontology and source-bound record profile for exploring materially different questions, frames and candidate meanings, preserving those distinctions for later inquiry.

**Architecture:** Add a conceptual module to the existing semantic architecture, a readable exploration-record profile and template in installed Skill references, and a bounded worked-case set. Connect the model to the existing active-agent entrypoint and selectively represent definitions and record provenance in the current reviewed-knowledge format. A dedicated executable artifact contract, new knowledge kinds or specialized queries are conditional follow-ups, not prerequisites for v1.

**Tech Stack:** Markdown semantic definitions and portable Skill references; existing JSON reviewed-knowledge schema version 1; existing Python semantic CLI and SQLite projection where available; Git history and existing session receipts. No new runtime dependency is planned.

**Spec:** [Divergent Exploration Ontology v1 — Design Basis](../specs/2026-11-04-divergent-exploration-ontology-design.md). Read both documents.

**Date and baseline:** 2026-11-04; `ThorStarlord/sensemaking-skills@8bd41bdf324e00aa75c1b849e333e076d85648ef`, after PR #724. Refresh applicable sources before implementation.

**Status and scope:** implementation plan requested after the owner accepted the preceding recommendations. The plan and its design basis are documentation deliverables; all implementation checkboxes below are initially unchecked. A later implementation instruction authorizes execution within its scope. Historical exploration, owner agreement with recommendations, and this plan do not establish creative benefit or qualify an inquiry operation.

## Global Constraints

- G1. The active agent remains the semantic controller; no new Skill, workflow engine, automatic next-stage transition, candidate ranking or implementation authorization is introduced by v1.
- G2. Preserve existing candidate identifiers, original records and historical judgments. A new expression, a revised interpretation and a new enduring possibility are different events.
- G3. Permit incomplete and unclassified candidate expressions. Do not require a product goal, value mechanism, architecture or canonical graph identity before an idea can be recorded.
- G4. Keep source facts, assumptions, interpretations, hypothetical outcomes, preferences and governing authority distinguishable. Every material judgment identifies its basis and scope.
- G5. Treat novelty, overlap and coverage as attributed, bounded judgments. No global originality claim, exhaustive possibility universe, numerical creativity score or fixed candidate/lens quota follows from the model.
- G6. Retain consequential meaning and provenance; do not persist private scratch reasoning or claim that a transformation account proves the model's internal cognitive cause.
- G7. Standalone Divergent Exploration ends with its landscape and a warranted stop or recommendation. Coverage Assessment, convergence, depth, strategic adoption and construction remain separately warranted responsibilities.
- G8. Use existing reviewed-knowledge kinds and predicates for v1. Do not bulk-promote the 59 archive candidates, change their dispositions, invent unsupported kind names or increment the universal knowledge schema.
- G9. Portable guidance must work from installed Skill references without a checkout of the Sensemaking framework, a SQLite index, a new CLI command or access to another repository's private sources.
- G10. Follow this repository's current CLAUDE.md policy: do not add or manually run local unit or synthetic evidence tests; use source/diff review and proportionate real-artifact checks, preserve hosted CI and release gates, and report NOT_RUN and evidence limits accurately.

**Verification adaptation:** the local owner policy in [CLAUDE.md](../../../CLAUDE.md#local-verification-scope) overrides the writing-plans Skill's generic test-first task examples. The steps below use source review, actual artifact checks, retrieval and installed-reference inspection. Worked examples are semantic representation cases, not synthetic pass/fail experiments. No task adds a local unit-test or synthetic-evidence suite.

## Review Focus

1. **Incomplete candidate:** a useful question, tension or fragment survives without invented product value or architecture. Owned by Tasks 1–2; inspect the explicitly labeled fragment case and its optional fields.
2. **Similar wording or common mechanism:** expressions with different beneficiaries, goals or truth conditions stay distinguishable; a near-duplicate judgment preserves both origins. Owned by Tasks 1–2 and re-read in Task 5.
3. **Source-to-hypothesis transition:** a real constraint or capability does not make an imagined experience observed, and an attributed transformation does not become a cognitive-causation claim. Owned by Tasks 2 and 4.
4. **Changed question, frame or authority:** a later interpretation preserves the earlier scope; an observed implementation choice does not silently become a permanent constraint or permission to act. Owned by Tasks 1, 3 and 5.
5. **Installed use without framework checkout:** a user invoking standalone divergence can reach the relevant reference and create a useful result without a full Level-3 analysis or framework-only links. Owned by Task 3 and checked in Task 5.

---

## 1. What v1 will deliver

V1 has six concrete deliverables:

1. A canonical conceptual module defining inquiry, question, frame, lens, candidate expression, transformation account, bounded landscape and exploratory judgment, with explicit mapping to existing concepts.
2. A readable record profile and optional template that preserve meaningful distinctions while allowing sparse or incomplete ideas.
3. A small set of annotated, source-pinned historical cases and one clearly illustrative fragment, with a vocabulary-fit matrix.
4. Portable guidance reachable from the current `using-sensemaking` entrypoint and existing creative-discovery references.
5. A small reviewed-knowledge pack that makes the semantic definitions and reference record discoverable through existing mechanisms.
6. A documented producer/reader reconstruction showing what the representation preserves, what remains manual or awkward, and what the evidence does not establish.

**V1 completion does not require** a new schema parser, a new graph kind, automatic novelty detection, a coverage score, bulk historical migration, a fresh-agent qualification campaign, or a release of a new orchestration runtime. Those are separate questions with their own warrant.

The substantive implementation must still be completed if no executable extension is warranted. Do not close after writing a glossary while the template, agent-use guidance, retention mapping or installed delivery is missing.

## 2. Source decisions that constrain the implementation

| Inspected source | Decision carried into the plan |
| --- | --- |
| [Semantic Architecture README](../../semantic-architecture/README.md#three-levels-of-formalization) | Vocabulary, conceptual ontology and executable contract are different levels of formalization |
| [Layered ontology](../../semantic-architecture/ontology.md) | Reuse existing evidence, knowledge, work and product concepts; not every relation must be a graph edge |
| [Prospective ontology](../../semantic-architecture/prospective-reasoning-ontology.md) | Separate activity, expression/analysis and enduring prospective identity; existing comparison endpoints must not be silently widened |
| [Creative discovery guidance](../../../skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md) | Preserve optional creative operations, anti-anchoring, bounded novelty and meaningful stopping |
| [Competency questions](../../semantic-architecture/competency-questions.md) | Reuse CQ-099/100 and CQ-103..114; add local refinements instead of a duplicate global catalogue |
| [Inquiry reconciliation](../../explorations/2026-11-03-inquiry-process-reconciliation.md) | Keep inquiry responsibilities separate; a new report alone does not warrant schema or runtime growth |
| [Knowledge contract](../../../skills/repository-semantic-steward/references/knowledge-contract.md) | Existing kinds, source references, epistemic states, selective curation and proposal checking remain authoritative |
| [Schema evolution](../../../skills/repository-semantic-steward/references/schema-evolution.md) | Shared types require a concrete unanswered question and comparison with simpler representations |
| [Session receipt](../../../skills/using-sensemaking/references/session-receipt-v1.md) | Existing facts/pointers record execution; substantive analysis remains in referenced artifacts |
| [Current strategic Skill](../../../skills/strategic-repository-analysis/SKILL.md) | Its contracted responsibility remains Level-3 strategic analysis; standalone divergence must not silently acquire that scope |
| [Build hook](../../../setup.py), [installer](../../../src/sensemaking_skills/setup_skills.py) and [profiles](../../../src/sensemaking_skills/defaults/install-profiles.yaml) | Whole Skill trees are copied; both profiles include the relevant Skills. Verify new references in the resulting output without changing profile membership |
| [Qualification readiness](../../normal-use/2026-11-04-independent-inquiry-operation-readiness.md) | Historical reconstruction and a local reader exercise do not count as new independent qualification trials |

## 3. File and ownership map

### New v1 files

| Planned file | Owns |
| --- | --- |
| `docs/semantic-architecture/divergent-exploration-ontology.md` | Concept definitions, role/layer mapping, relationship meanings, identity and epistemic invariants |
| `docs/semantic-architecture/divergent-exploration-competency-v1.md` | Local competency refinements, baseline/implemented fit, source cases and unresolved limitations |
| `docs/semantic-architecture/divergent-exploration-reference-cases-v1.md` | Bounded annotated representations of historical expressions and the labeled fragment illustration |
| `skills/strategic-repository-analysis/references/divergent-exploration-v1.md` | Self-contained portable operating profile: when to use the model, how to express it, and how to stop |
| `skills/strategic-repository-analysis/references/divergent-exploration-record-template.md` | Optional human/agent-readable shape for a substantial retained inquiry |
| `.sensemaking/knowledge/divergent-exploration.json` | Source-bound definition and record-reference claims using supported schema/version/kinds |

### Existing files with bounded changes

| File | Permitted change |
| --- | --- |
| `docs/semantic-architecture/ontology.md` | Short cross-layer extension pointer; reuse existing Artifact/Claim/product concepts |
| `docs/semantic-architecture/relations-and-epistemics.md` | Document conceptual relation meanings, endpoints and establishment requirements without adding executable predicates |
| `docs/semantic-architecture/competency-questions.md` | Link the local fit matrix from relevant existing CQ sections; retain global IDs and historical baseline statements |
| `docs/semantic-architecture/README.md` | Add module, competency and case navigation; describe actual formalization level |
| `skills/using-sensemaking/SKILL.md` | One conditional reference cue for a standalone divergent inquiry where question/frame/candidate distinctions matter |
| `skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md` | Link the new profile; distinguish emerging expressions from material candidates and selective curation |
| `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md` | Reuse the profile when breadth is actually part of an authorized strategic analysis |
| `skills/repository-semantic-steward/references/knowledge-contract.md` | Small retention mapping: complete prospective entities versus fragments and record references |
| `docs/explorations/README.md` | Navigation to the implemented model/cases; preserve all old dated records and rankings |
| `STATUS.md` | After implementation, record the actual capability and limitations if they change the next-agent context; do not claim qualification |

Inspect but do not change by default: `src/sensemaking_skills/semantic_architecture/knowledge.py`, `knowledge_sources.py`, `knowledge_store.py`, `src/sensemaking_skills/semantic_cli.py`, `setup_skills.py`, `defaults/install-profiles.yaml`, both artifact-contract registries, Skill manifests and CI. A concrete defect may warrant a bounded change; their mere involvement does not.

No new generic Python module or function signature is planned. The implementation interfaces are the semantic definitions, readable profile, source references and supported JSON/CLI contracts below.

## 4. Dependency and PR sequence

| Increment | Tasks | Result available after merge |
| --- | --- | --- |
| PR A — semantic foundation | Task 1 | Definitions, relation meanings and a concrete competency map |
| PR B — usable records and cases | Task 2 | A portable record profile/template with faithful worked representations |
| PR C — agent use and delivery | Task 3 | The current entrypoint can discover and use the model in installed form |
| PR D — reviewed memory | Task 4 | Selected definitions and record provenance can be retrieved with existing knowledge queries |
| PR E — reconstruction and reconciliation | Tasks 5–6 | Reader findings, any bounded corrections, accurate navigation/status and completion account |

Tasks 3 and 4 can be prepared in parallel after Task 2 because their main files differ. Integrate both before the final consumer review. One agent keeps semantic ownership of names, identity and status meanings. Combine PRs only when separating them would leave a broken reference or unusable increment; do not generate empty administrative PRs.

Use a separate `claude/<topic>` branch for each PR, a short source-grounded decision note, clean source/diff review and the current authorized merge policy. Once execution is authorized, continue through warranted core increments rather than asking for permission after each one. Recheck current source reality after a merge; later evidence can change the implementation detail without changing the goal.

## 5. Implementation tasks

### Task 1: Define the conceptual ontology and its competency boundary

**Files**

- Create: `docs/semantic-architecture/divergent-exploration-ontology.md`.
- Create: `docs/semantic-architecture/divergent-exploration-competency-v1.md`.
- Modify: `docs/semantic-architecture/ontology.md`, `relations-and-epistemics.md`, `competency-questions.md`, `README.md`.

**Interfaces**

- Consumes: design sections 4–5; existing Artifact, Claim, EvidenceSource, Provenance, TargetSnapshot, Hypothesis, Assumption, Goal, Constraint and prospective entities.
- Produces: definitions of the eight proposed concepts/roles; the conceptual relationship rows from the design, including inquiry-to-expression and expression-to-question provenance; identity/revision rules; DEO-CQ-01..10 and their mapping to existing global questions.
- Downstream readers use these meanings, not a new claim-kind enum. The operational profile in Task 2 may summarize them for portability but may not redefine them.

- [ ] **Step 1: Refresh governing sources and record the implementation baseline.** Read current AGENTS/CLAUDE, product strategy, relevant accepted ADRs, semantic model, creative guidance and current work. Confirm the requested scope and local verification policy. Preserve a receipt when using the entrypoint, under its existing authority and persistence rules.
- [ ] **Step 2: Write the ontology module.** Define the eight roles, map them across evidence/knowledge/work/product layers, and distinguish the activity, its record, a candidate expression and an enduring candidate. Make partial frames and incomplete expressions valid. Do not create a new universal Candidate replacement for ProductPossibility/ArchitectureOption.
- [ ] **Step 3: Define relation and identity semantics.** For each design relation, specify endpoints, direction, source or attribution requirement and one applicable example. Keep a plain artifact reference distinct from a claim that two expressions mean the same thing. Document how a question/frame revision differs from wording edits and new candidate identity.
- [ ] **Step 4: Author the local competency matrix.** Use the ten questions in section 6 below. For each, name the source case, current representation and missing or awkward distinction. A baseline answer may be faithful; do not invent a failed question to justify a new schema.
- [ ] **Step 5: Connect the canonical documentation.** Add concise ontology/relation/README pointers and links from existing CQ-099/100/103..114. Preserve prior baseline assessments as dated history. Introduce no link to an uncreated future file; add those links when its task lands.
- [ ] **Step 6: Review meanings against the spec and original sources.** Resolve inconsistent use of question, frame, expression, referent and judgment. Check that existing ComparativeJudgment/ProvisionalPreference endpoints are not silently broadened from architecture/path to arbitrary inquiry targets. Use ExploratoryJudgment as a documented Claim role unless a deliberate conceptual extension is separately explained.
- [ ] **Step 7: Commit and integrate the semantic increment.** Suggested commit: `docs(ontology): define divergent inquiry semantics and competencies`. Report source/diff review and local tests NOT_RUN.

**Acceptance:** a reader can explain each role, distinguish its neighbors, identify its source/evidence meaning, and tell which questions the model is intended to make reconstructible. No executable support or creative improvement is claimed from definitions alone.

### Task 2: Build the readable record profile and faithful reference cases

**Files**

- Create: `skills/strategic-repository-analysis/references/divergent-exploration-v1.md`.
- Create: `skills/strategic-repository-analysis/references/divergent-exploration-record-template.md`.
- Create: `docs/semantic-architecture/divergent-exploration-reference-cases-v1.md`.
- Modify: `docs/semantic-architecture/divergent-exploration-competency-v1.md` and the new ontology module's example links.

**Interfaces**

- Consumes: Task 1 definitions/identity rules and the historical records listed in section 7.
- Produces: the seven optional template headings named in design section 6; stable local reference conventions; a self-contained portable explanation; bounded case annotations and a fit result per applicable DEO-CQ.
- Mandatory information is semantic: question/target, source scope, substantive result, material uncertainty/authority and completion. Optional fields must not become empty-form obligations.

- [ ] **Step 1: Write the portable profile.** Explain the user-visible purpose, the minimal meanings needed without framework docs, valid sparse expressions, frame changes, attributed differences and how a later reader resolves sources. Keep the deeper canonical documents as optional provenance.
- [ ] **Step 2: Write the record template.** Include the headings from the design and mark conditional sections as optional. Offer a compact prose example and an expanded candidate/relationship example. Do not add `artifact_id`, automatic lifecycle statuses, a mandatory JSON sidecar or a new registered schema.
- [ ] **Step 3: Define concrete local references.** In newly authored records, an explicitly referenced candidate may use a stable heading `### C1` with a separate label; questions/frames/accounts/judgments may use Q/F/T/J prefixes similarly. An old table label is referenced by original file plus label, not a fabricated URL fragment. Record known `poss:`/`arch:` referents separately from expression IDs.
- [ ] **Step 4: Annotate the bounded authentic cases.** Preserve their original wording or a clearly marked faithful paraphrase, source revision, candidate labels, epistemic limits and original disposition. Add only the interpretation needed to demonstrate the ontology. Every annotation is this implementation's representation assessment, not a retroactive correction of the original inquiry.
- [ ] **Step 5: Add one incomplete-question illustration.** Mark it explicitly as illustrative, without a historical-session or empirical claim. Demonstrate a partial frame, unknown beneficiary/outcome if appropriate, a stable local expression and a useful open question; do not fill the unknowns merely for completeness.
- [ ] **Step 6: Fill the vocabulary-fit matrix.** Mark each local question faithful, awkward, lost or not established, with evidence. Distinguish a documentary answer from a machine-queryable relation. Record which proposed distinctions improve explicitness even where the old prose could already carry them.
- [ ] **Step 7: Inspect the retained record as a reader.** Verify original identities survive, a relationship judgment identifies both operands and its comparison basis, and a fragment is not coerced into a ProductPossibility. Confirm that known gaps do not become a claim of global exhaustion.
- [ ] **Step 8: Commit and integrate.** Suggested commit: `docs(exploration): add portable record profile and source-bound cases`.

**Acceptance:** both a sparse fragment and a mature candidate can be expressed; the source-to-hypothesis transition, original IDs and changed frames remain recoverable; the profile can be read on its own by an installed agent. Case reconstruction is not counted as a fresh creative trial.

### Task 3: Connect agent behavior and verify installed delivery

**Files**

- Modify: `skills/using-sensemaking/SKILL.md`, limited to a conditional reference cue.
- Modify: `skills/strategic-repository-analysis/references/creative-prospective-discovery-v1.md`.
- Modify: `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`.
- Inspect: `setup.py`, `src/sensemaking_skills/setup_skills.py`, `src/sensemaking_skills/defaults/install-profiles.yaml`, packaged Skill-resource paths and existing distribution guidance.

**Interfaces**

- Consumes: Task 2 portable reference and template.
- Produces: a discoverable agent-native path from an explicit divergent request to the relevant guidance, plus evidence that its relative reference targets survive installation.
- The current strategic Skill's output contract remains `strategic_repository_analysis`. Loading its reference does not invoke that whole responsibility.

- [ ] **Step 1: Add one entrypoint cue.** In the reference-loading table, link `../strategic-repository-analysis/references/divergent-exploration-v1.md`. Load it for a bounded divergent inquiry where question/frame/candidate distinctions or durable continuation matter; skip it for a narrow edit or a trivial brainstorm. Explain the decision this cue changes so it earns space in the core.
- [ ] **Step 2: Amend creative discovery at the expression/material-candidate boundary.** Permit fragments and new questions before mature candidate discrimination. Once a material candidate exists, retain existing source/novelty/authority discipline. Do not turn the model's concepts or the existing creative operators into compulsory passes.
- [ ] **Step 3: Link the strategic funnel at its existing breadth seam.** When a real strategic analysis uses divergence, it may consume the same profile. Keep its subsequent coverage/frontier responsibilities scoped to that analysis and preserve standalone divergence's stopping boundary.
- [ ] **Step 4: Inspect discovery and dependency closure.** At the inspected baseline, `entrypoint` includes the referenced strategic and steward Skills, `full` includes every packaged Skill, and both the build hook and installer copy complete Skill trees. Confirm those facts still hold and that both new reference files reach the resulting package. No profile membership change is presently warranted.
- [ ] **Step 5: Inspect an actual isolated installation or package output when the current setup path is available.** Use an explicitly chosen temporary/project destination and the existing installer; do not overwrite the owner's user-wide installation. Check the entrypoint link and the reference-to-template link in that output. If the installer cannot run in the host, report installed delivery NOT_RUN and preserve the source-inspection result; do not claim distribution verification.
- [ ] **Step 6: Repair only a concrete delivery defect.** Prefer existing copy/packaging patterns. Do not add a new profile, duplicate the semantic framework inside each Skill, change default installation scope or rewrite the public entrypoint. If no defect exists, leave installer/manifests/registries unchanged.
- [ ] **Step 7: Commit and integrate.** Suggested commit: `feat(guidance): apply divergent inquiry ontology through the existing entrypoint`. Report exactly whether source inspection, installed-file inspection or an actual invocation was observed.

**Acceptance:** the new model is reachable through the existing public entrypoint and its required portable meanings are delivered with the relevant Skills. No new mandatory orchestrator, runtime mode or framework checkout dependency appears. If actual package/installation inspection could not run, report the guidance as implemented with installed delivery unverified; do not mark that verification step complete.

### Task 4: Add selective reviewed-knowledge representation and retrieval

**Files**

- Create: `.sensemaking/knowledge/divergent-exploration.json`.
- Modify: `skills/repository-semantic-steward/references/knowledge-contract.md`, with a small record/fragment retention section.
- Modify: `docs/semantic-architecture/divergent-exploration-competency-v1.md`, with actual vocabulary/retrieval fit.
- Inspect: `src/sensemaking_skills/semantic_architecture/knowledge.py`, `knowledge_sources.py`, `knowledge_store.py`, `src/sensemaking_skills/semantic_cli.py`.

**Interfaces**

- Consumes: committed ontology definitions and the reference-case artifact from Tasks 1–2.
- Produces: an existing-schema JSON pack, definition identities and a source identity as specified in design section 7; existing `search`/`explain` retrieval can reach the model and its source.
- File envelope is exactly `schema_version`, `claims`, `relations`. Claim fields remain `id`, `kind`, `statement`, `authority_kind`, `authority_ref`, `evidence_refs`, plus supported optional fields. Relationship fields remain `id`, `subject`, `predicate`, `object`, `evidence_refs`, plus supported optional fields.

- [ ] **Step 1: Check existing identities and choose only useful definition/source records.** Use the proposed domain_concept IDs from the design unless an existing claim already expresses that meaning. Record a real equivalence instead of duplicating a definition under a different ID.
- [ ] **Step 2: Author the version-1 pack.** Definitions use `domain_concept`, document authority and `declared` status. The source claim describes the worked document and its limited purpose. Cite tracked source files. Do not add unsupported `artifact`, `question`, `frame` or `assessment` claim kinds.
- [ ] **Step 3: Add only source-grounded relationships.** Reuse `references` and, when its actual meaning fits, `derived_from`. Put a more specific documentary meaning in `attributes.conceptual_relation` and explicitly acknowledge its unchecked semantics. Do not use `relates_to` as a generic relation or force questions/fragments into `opportunity`.
- [ ] **Step 4: Document selective target retention.** Explain how an actual target can preserve a record reference, selected hypotheses or coherent prospective entities under existing authority. Keep its local expressions and full source record. Never copy the framework's knowledge pack or Atlas claims into another target as that target's own knowledge.
- [ ] **Step 5: Run the existing real-artifact proposal check when available.** Use the command in section 8 against the authored pack and inspect schema, endpoints and cited tracked files. Resolve any concrete defect; do not weaken the checker to accommodate a mistaken representation. Under the existing knowledge contract, an unchecked pack remains a draft. If this operation is unavailable, complete the possible documentation work and leave this acceptance item open rather than claiming reviewed-knowledge delivery.
- [ ] **Step 6: Commit the reviewed sources, build a source-pinned index and retrieve the actual records when available.** Search for `candidate-expression`, explain `domain_concept:candidate-expression`, and explain `source:divergent-exploration-reference-cases`. Follow the returned source references and assess whether the useful meaning can be recovered. Raw presence in JSON or a nonempty query alone is insufficient.
- [ ] **Step 7: Record limits and integrate.** State which questions are answered by indexed identity, which require reading source attributes/prose, and which remain unresolved. Suggested commit: `feat(knowledge): retain divergent inquiry definitions and provenance`.

**Acceptance:** the retained records have passed the existing proposal checker under the unchanged supported schema and actual retrieval leads a reader to the correct source meanings. Historical speculative candidates remain unpromoted. Unavailable proposal/retrieval checks remain explicit outstanding acceptance items; they cannot be waived by a source-only review. Retrieval evidence does not claim that future agents used the model or became more creative.

### Task 5: Review the actual producer-to-reader boundary

**Files**

- Modify: `docs/semantic-architecture/divergent-exploration-reference-cases-v1.md`, with a short reconstruction/review section.
- Modify: `docs/semantic-architecture/divergent-exploration-competency-v1.md`.
- Correct the owning ontology/profile/retention file only if a material source-backed defect is found.

**Interfaces**

- Consumes: final profile, actual case artifact, original source references and selected retrieved records.
- Produces: a bounded source-grounded reconstruction, documented remaining limits, and any necessary in-scope correction.
- The reader's role is to recover meanings and sources, not to score creativity, rank the portfolio or begin a new inquiry stage.

- [ ] **Step 1: Read the completed artifact through the consumer's entry path.** Start from its published navigation or returned source record, then inspect the profile and decisive original sources. A separate reviewer can do this when useful; do not describe collaboration within the implementation as the independent qualification program.
- [ ] **Step 2: Answer the local competency questions from the retained material.** Recover question, frame, expression, original label, asserted difference, supporting source and uncertainty. Note when source prose is required. Admit an unknown rather than manufacture missing provenance.
- [ ] **Step 3: Inspect the five Review Focus conditions.** Confirm the fragment survives, near-duplicate IDs remain distinct, different truth conditions stay distinguishable, hypothetical player value stays hypothetical, and a changed frame does not rewrite owner intent.
- [ ] **Step 4: Check the Coverage Assessment handoff without running a new assessment.** The record should identify its inspected scope, candidate references and known omissions so a later separately requested assessment can use them. It must not represent unexamined dimensions as absent or silently supply rankings.
- [ ] **Step 5: Fix only the nearest concrete representational or guidance defect.** Distinguish a lost meaning from a slow retrieval, unclear wording, missing reference or lack of empirical evidence. Existing attributes/prose may remain adequate. Record a conditional follow-up when a real machine consumer is needed; do not build it automatically.
- [ ] **Step 6: Record the actual evidence ceiling.** Separate source fidelity, representation completeness, structural validity, retrieval, installed delivery, observed agent use, independent repeatability and causal benefit. Mark unperformed activities NOT_RUN or NOT_ASSESSED.
- [ ] **Step 7: Commit the review and corrections.** Suggested commit: `docs(exploration): reconcile divergent ontology reconstruction and limits`.

**Acceptance:** a reader can reconstruct the intended distinctions from durable material, or the exact remaining limitation is explicit and honestly scoped. No historical example or well-formed artifact is counted as a fresh independent operation trial.

### Task 6: Reconcile navigation, capability state and completion

**Files**

- Modify: `docs/semantic-architecture/README.md`, `docs/explorations/README.md`.
- Modify `STATUS.md` only for the actual new capability/limitation/next-responsibility delta.
- Update this implementation plan's checkboxes and a small completion note only when the work has actually occurred.
- Maintain the current session receipt under its existing contract when applicable; do not add a new receipt field.

**Interfaces**

- Consumes: completed core tasks, source/diff review and actual verification receipts.
- Produces: discoverable documentation, accurate current capability statements and a reconstructible stop.

- [ ] **Step 1: Link the implemented model and examples from existing indexes.** Preserve all dated archive records, 59 local identities, seven GD families, curated possibility counts and prior rankings. An ontology reference is not another exploration pass or a new portfolio decision.
- [ ] **Step 2: Describe the real capability.** State that the model/profile/guidance and selected representation exist, naming any unverified installed or consumer path. Keep improved creativity and independent repeatability unproven unless independently established.
- [ ] **Step 3: Review the complete diff and references.** Check that source-specific examples stay in the framework's case record, portable guidance contains no mandatory framework-only file dependency, no unsupported schema fields/kinds were introduced, and no required CI or authority behavior changed.
- [ ] **Step 4: Integrate the final bounded changes under current repository policy.** Use the existing source-grounded PR note and merge instructions. Preserve actual GitHub protections. Assess any known consequential failure; do not disable checks or claim pending CI passed.
- [ ] **Step 5: Verify the merged files and report completion.** Link the model/profile, cases, knowledge representation and actual review results. Clearly identify any optional future work. Finalize applicable receipt state and state persistence truthfully.

**Acceptance:** the v1 implementation is usable and discoverable through its intended agent-facing surfaces, its retained records are source-bound, and the report describes actual support and limitations. No optional schema or qualification initiative is silently added to the completion definition.

## 6. Local competency matrix

These refine existing competencies; the labels are local to this implementation.

| Local question | What a faithful answer preserves | Existing competency connection |
| --- | --- | --- |
| DEO-CQ-01 | The question behind an expression and what remains unresolved | CQ-099, CQ-103 |
| DEO-CQ-02 | Relevant beneficiary, purpose, situation, horizon and assumptions, including unknowns | CQ-103, CQ-105 |
| DEO-CQ-03 | A useful incomplete expression without invented outcome/mechanism or premature type | CQ-110, CQ-112; new explicit refinement |
| DEO-CQ-04 | Producing/revising activity, recording artifact and any enduring referent remain distinct | CQ-099 and prospective activity/entity distinction |
| DEO-CQ-05 | Whether a claimed difference concerns end, beneficiary, mechanism, premise, scope or truth conditions | CQ-100, CQ-106 |
| DEO-CQ-06 | Restatement, variant, complement, incompatible alternative and unassessed relation remain distinguishable | CQ-100, CQ-107 |
| DEO-CQ-07 | Assessor, comparison corpus, source revision, basis and uncertainty for a novelty/overlap judgment | CQ-107, CQ-111 |
| DEO-CQ-08 | Evidence for identity across expressions without destructive merging | CQ-099, CQ-100 |
| DEO-CQ-09 | A changed question/frame/premise and the historical assessment it qualifies | CQ-105, CQ-108 |
| DEO-CQ-10 | Expression, retained possibility, observed capability, preference, decision and action authority remain distinct | CQ-106, CQ-109 and existing authority concepts |

For each row record: source case; baseline fit; implemented fit; exact source/record references; answer or missing distinction; whether reading prose/attributes is required; and the smallest warranted follow-up. Use **faithful / awkward / lost / not established** as local review labels, not global canonical enums or a score.

CQ-114 and the independent-use parts of CQ-111 are not settled by this implementation exercise. Leave their empirical status explicit.

## 7. Concrete source cases

| Case | Original source | Distinction to preserve |
| --- | --- | --- |
| Atlas belonging hypothesis | `docs/explorations/2026-11-03-cross-repository-creative-discovery-atlas-midgard.md` | Source-backed architecture versus attributed reframing and hypothetical player value |
| Question collision and role migration | `docs/explorations/2026-11-02-divergent-repository-knowledge.md`, DE-A2 and DE-B1 | New questions before coherent futures; changed beneficiary or desired end |
| Near-duplicate expression pair | `docs/explorations/2026-11-02-generative-depth-repository-knowledge.md`, GD-D; first divergent record, DE-F2; comparison in the convergent record | Near duplication is a judgment; both source identities survive |
| Different causes of apparent plurality | `docs/explorations/2026-11-03-convergent-accumulated-creative-possibilities.md`, DE-G1 / NX-N2 / NX-K3 and their origins | Rival interpretation, conditional validity and different observation conditions |
| Hiding, successful exit and non-capture | Same convergent record, NX-M1 / RP-Q1 / RP-Q2 and their origins | A changed desired end or retention premise, not cosmetic variation |
| Labeled fragment illustration | Newly authored example in the reference-case document | An incomplete question can remain meaningful without invented history, value or realization |

Pin the original source revision used by each annotation. The number of cases is selected to cover these specific distinctions; it is not a general exploration quota. Do not rerun all three divergent passes or migrate the full archive.

## 8. Proportionate verification and evidence

### Source and semantic review

For every increment, inspect the changed files and the decisive original sources. Check identity, source scope, conceptual relation endpoints and the distinction between inferred meaning and observed facts. Use the five Review Focus conditions and the local competency matrix; do not add a new numerical rubric.

For documentation, inspect actual relative paths, stable headings and packaged reference targets. JSON parsing or a valid link is evidence about structure only.

### Existing knowledge commands

Run these only when executing Task 4 against the real authored artifacts and an available existing CLI. They are normal artifact/retrieval operations, not a new unit or synthetic-evidence test suite.

```bash
sensemaking-skills semantic knowledge-proposal-check --repo . \
  --proposal .sensemaking/knowledge/divergent-exploration.json --json
```

Expected: successful exit and no schema, endpoint or cited-file defect. Inspect the actual output contract; success does not establish the semantic truth or utility of the content.

After the source and knowledge files are committed, use the exact commit. The following is Bash syntax; use equivalent variable syntax in the host shell while preserving the CLI arguments.

```bash
DEO_REF="$(git rev-parse HEAD)"
DEO_DB="$(python -c 'import tempfile; from pathlib import Path; print(Path(tempfile.mkdtemp(prefix="sensemaking-deo-")) / "knowledge.sqlite")')"
sensemaking-skills semantic knowledge-build --repo . \
  --repository ThorStarlord/sensemaking-skills --target-ref "$DEO_REF" \
  --temporary-checkout --db "$DEO_DB" --json
sensemaking-skills semantic knowledge-query --db "$DEO_DB" \
  --repository ThorStarlord/sensemaking-skills --target-ref "$DEO_REF" \
  --operation search --term candidate-expression --json
sensemaking-skills semantic knowledge-query --db "$DEO_DB" \
  --repository ThorStarlord/sensemaking-skills --target-ref "$DEO_REF" \
  --operation explain --subject domain_concept:candidate-expression --json
sensemaking-skills semantic knowledge-query --db "$DEO_DB" \
  --repository ThorStarlord/sensemaking-skills --target-ref "$DEO_REF" \
  --operation explain --subject source:divergent-exploration-reference-cases --json
```

Expected: returned definitions/source records match the committed source, references resolve, provenance and hypothetical/declared statuses remain accurate, and the agent can follow the actual source to answer the bounded question. Uncommitted edits are not part of the index. Do not relax that boundary or require the active checkout to be pristine when the existing temporary-checkout option suffices.

### Evidence categories reported separately

| Category | What can establish it | What it does not establish |
| --- | --- | --- |
| Semantic specification | Source-grounded definition and relation review | Runtime support or usefulness |
| Documentary representation | Faithful case mapping and recoverable references | New creative discovery |
| Structural validity | Existing parser/proposal check on actual artifacts | Truth, value or authorization |
| Retrieval | Actual queries plus inspection of returned sources | Later independent use |
| Installed delivery | Inspection of actual isolated installation/package output | That every host loaded the guidance |
| Observed agent use | A genuine bounded invocation with its record and limits | Repeatability or comparative creative benefit |
| Independent qualification | The separately warranted program's actual fresh cases and reviews | Universal generality or causal graph advantage |

Do not add local unit/synthetic tests in the current construction phase. Hosted CI and release gates remain intact. If a tool or independent host is unavailable, report the specific activity NOT_RUN; do not manufacture a transcript, synthetic pass or new infrastructure project.

## 9. Conditional follow-ups, outside the core completion path

### C1. Machine-readable inquiry artifact

Trigger: an identified producer/consumer actually needs stable parsed fields or an inter-process handoff and the documentary profile cannot preserve it reliably.

Before implementation, record the consumer, exact lost distinction, failed input/output example, alternatives and minimum required fields. Then write a small reviewed design for a registered artifact contract and focused validator/reader. Inspect both current artifact registries and their synchronization/ownership rules; preserve old documents. Every validator constraint must trace to a real consumer. Do not automatically introduce a graph type or a workflow transition with the artifact.

If no such need is observed, record **DEFERRED — no executable consumer requirement**. V1 remains complete.

### C2. Shared graph vocabulary or retrieval specialization

Trigger: a real later inquiry cannot faithfully represent or recover a necessary meaning using supported claims, attributes, references and source reading. Distinguish a retrieval/filtering limitation from a semantic-model limitation.

Follow the existing schema-evolution process: authentic example, competency loss, alternatives, identities/endpoints/epistemics, compatibility, migrations and required authority. An unchecked attribute or an unfamiliar domain term alone is not proof of a lost answer. Avoid a parallel store, unbounded ontology import or broad migration.

If existing representations suffice, record **NO CHANGE WARRANTED** for executable vocabulary. Do not leave the usable semantic implementation unfinished while waiting for an unnecessary schema change.

### C3. Independent creative-use qualification

Use the existing qualification program only when its authentic cases, fresh session access, relevant reviewer and source/version controls are available and separately warranted. Preserve raw outputs and inspectable records. The reference cases in this plan count as zero fresh qualification trials.

## 10. Risks, rollback and completion

| Risk | Design response | Review owner |
| --- | --- | --- |
| Ontology narrows imagination | Partial frames, unclassified expressions, open lenses and revisable questions | Tasks 1–3 |
| More documentation without better reasoning | Cases ask what changed in meaning; guidance must influence an actual agent decision to inspect or distinguish | Tasks 2, 3, 5 |
| Duplicate parallel vocabulary | Map to existing concepts and CQs; keep new role names explicit and bounded | Tasks 1, 4 |
| False canonicalization of historical ideas | Preserve original labels, hypotheses, disagreements and selective curation | Tasks 2, 4, 6 |
| False cognitive or causal provenance | Attribute transformation accounts and preserve observed-versus-inferred distinctions | Tasks 1, 2, 5 |
| Metadata burden | Optional detail and compact prose; no lens/candidate quotas | Tasks 2–3 |
| Framework-only installation dependency | Self-contained portable profile and actual installed-reference inspection | Tasks 3, 5 |
| Verification inflates claims | Separate structural, representational, use and independent-benefit evidence | Tasks 4–6 |

All core changes are additive documentation, reference integration and a separate reviewed pack. If a use cue proves misleading, narrow or remove that cue while preserving the historical record. If a reviewed interpretation is wrong, correct or supersede it with its source history; do not rewrite the original exploration. No v1 migration changes old schema versions or candidate namespaces.

**Completion report must include:** delivered files and user-visible behavior; the conceptual-to-executable mapping; actual source/diff, artifact, retrieval and installation observations; local tests NOT_RUN; hosted CI status as observed; unresolved limitations; disposition of each conditional follow-up; and exact merged PRs/commits.

The intended result is a usable ontology for divergent inquiry, expressed through the existing agent-native product. It should preserve what changed in the question, frame or candidate and let later inquiry recover that meaning without treating a tidy representation as proof of creativity.
