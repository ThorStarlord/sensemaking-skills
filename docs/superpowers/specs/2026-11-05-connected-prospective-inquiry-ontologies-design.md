# Connected Prospective Inquiry Ontologies v1 — Design Basis

**Date:** 2026-11-05  
**Status:** owner-approved direction for **planning**; implementation not yet performed.  
**Planning source:** `ThorStarlord/sensemaking-skills`, `main@6fa8d05f3845ac7c06cf4ef7127ef0d9f164d405`. Refresh source and instructions before implementation.  
**Companion:** [detailed implementation plan](../plans/2026-11-05-connected-prospective-inquiry-ontologies.md).  
**Authority:** current product thesis and ADRs 0029, 0031, 0034, existing Level-3/Level-4 processes, the active agent within delegated scope, and owner-reserved decisions.

## 1. Decision and desired capability

Develop **one connected semantic extension with four focused, conditional reasoning profiles**:

| Profile | Question | Primary documentary product |
| --- | --- | --- |
| Focused Depth Exploration | If this possibility/premise holds, what follows, under which conditions? | Bounded `ConsequenceStructure` with effects, branches, mechanisms, limits and newly exposed opportunities. |
| Convergent Reassessment | Do new consequences or findings change earlier judgments? | Dated `AssessmentRevisionAccount` or explicit reasoned reaffirmation, affecting only justified comparisons/portfolio members. |
| Adversarial Review | Where could this claim, comparison or proposed design fail; what follows from the objection? | `ChallengeResponseAccount` with exact target, grounds, response, scope and residual issue. |
| Architecture Synthesis | What coherent product-and-technical proposal follows from the chosen goals, constraints and judgments? | `DesignRationaleView` linking intended outcomes and requirements to architectural responsibilities/structures, with PRD and technical spec when warranted. |

These four profiles are **responsibilities that can interleave**, not mandatory phases, Skills, runtime states, or a control-level hierarchy. Each can finish at a reasoned no-change/no-consequence/uncertainty result. Consequence analysis may return to divergence; challenge can occur before or after a proposal; reassessment need not reorder a portfolio. A PRD/spec is not an implementation authorization.

### Scope choice for the final profile

Use **a unified product-and-technical proposal** as the conceptual goal. The PRD addresses intended beneficiary, outcomes, user-visible behavior, scope and success criteria; the technical specification addresses proposed responsibilities, boundaries, contracts, interactions, constraints and risks. They may be one proportionate document or linked documents. The existing `architectural_synthesis` remains a **multi-option comparison with optional provisional preference**, not a newly selected final design. The existing `to-prd` Skill remains the PRD authority. This extension must not add a competing PRD producer or imply an unratified design has been adopted.

## 2. Existing foundations to preserve

- `docs/semantic-architecture/prospective-reasoning-ontology.md`: activities versus entities; `ConsequenceHypothesis`, `ArchitectureOption`, `ConstructionPath`, `ComparativeJudgment`, `ProvisionalPreference`; chain rule and feedback outcomes.
- `docs/semantic-architecture/possibility-assessment-ontology.md`: `AssessmentFrame`, `AssessmentJudgment`, `PortfolioSnapshot`, `AssessmentRevisionAccount`; distinction among inquiry, strategic and implementation priority.
- `docs/semantic-architecture/convergent-direction-selection-ontology.md`: candidate warrant, preference versus actual selection, explicit actor/scope/authority, nonselection, preserved alternatives and reconsideration.
- `docs/explorations/2026-11-03-inquiry-process-reconciliation.md`: consequence-driven Depth Exploration, pairwise portfolio reassessment and bounded inquiry contracts.
- `docs/research/consequence-depth-and-systems-reasoning-v0.md`: justified depth and stopping condition.
- `skills/repository-semantic-steward/references/architecture-exploration.md` and `architectural-synthesis-template.md`: option comparison, consequences, challenge and feedback; `architectural_synthesis` contract.
- `skills/architectural-review/SKILL.md`: review of a concrete `proposed_direction` against a current `repository_sensemaking_brief`; do not weaken its inputs.
- `skills/to-prd/SKILL.md`, PRD contract: goal, scope, evidence, acceptance, owner-approval boundaries.
- `skills/using-sensemaking/references/learning-reconciliation-policy-v0.md`: returned evidence changes explicit claims and responsibilities only when warranted.
- `skills/using-sensemaking/SKILL.md`: single public entry and agent-owned adaptive composition.
- `skills/workflow-planner/references/artifact-contracts.yaml`: current producers/consumers and required fields. No schema inferred from prose.

Reuse these identities and consumers before proposing new graph kinds or artifact fields. Existing `conseq:` records in `architectural_synthesis` are option-linked; general Depth Exploration must be representable in dated narrative without pretending an architectural option exists.

## 3. Shared conceptual spine

**Common envelope when material:** actual actor/date, bounded question and assessed target, owner/repository/target revision, accepted intent and authority, original entity IDs and source references, assumptions, observed premises, epistemic class, comparison frame, affected beneficiary, contradiction/counterevidence, revisions and stop/re-entry condition. Share the envelope once in a report; do not require empty fields or a new universal artifact.

**Identity:** An original `poss:`, `arch:`, `conseq:`, decision, source-local candidate, `AssessmentJudgment`, PRD or observed component keeps its original type. Each documentary view uses its containing artifact plus revision and a local scoped ID. New proposed components stay inside a proposed architecture until implemented. Consolidation is not equality; a design view is not a new canonical architecture identity.

**Epistemics:** Separate (a) source observation, (b) conditional logical implication under stated assumptions, (c) plausible causal/enabling hypothesis, (d) creative possibility, (e) assessment/preference, (f) sourced adoption/authority and (g) verified observed result. Causal edge composition is **not transitive proof**: if A may yield B and B may enable C, A is not proven to yield C. Graph navigation and reference integrity are not truth/warrant.

**Authority:** Evaluation, recommendation, selected direction, implementation authorization, completed work and verified outcome remain distinct. The agent can choose a bounded responsibility under existing delegation; a prospective artifact cannot ratify Level 4, create work permission, or mutate strategy automatically.

### Candidate documentary relations (not executable predicates)

- `ConsequenceStructure` **examines** a typed premise/possibility and **contains** related `ConsequenceHypothesis` references, branches, interactions, counterexamples and scope limits.
- A conditional consequence **dependsOnPremise**, **couldAffectJudgment** and **exposesQuestionOrOpportunity** with source and uncertainty; existing `mayProduce`, `mayEnable`, `mayConstrain` and `challenges` keep their declared endpoint meanings.
- An `AssessmentRevisionAccount` **reconsiders** an attributable historical judgment/snapshot **becauseOf** a source-qualified new finding; it states the target, purpose/frame, delta and unchanged parts.
- A `ChallengeResponseAccount` **challenges** one exact claim, premise, inference, comparison, requirement or design element; **respondsWith** a rebuttal, revision, deferral, investigation or acknowledged open issue, and **leavesOpen** residual uncertainty when material.
- A `DesignRationaleView` **connects** target outcomes and constraints to requirements, responsibilities, design elements, interface contracts and alternatives; **addressesOrDiscloses** challenges without claiming implementation or owner acceptance.

These names are explanatory prose, not changes to the v1 knowledge predicate set, graph endpoints, Campaign schema or a machine-enforced causal model.

## 4. Depth Exploration profile

**Unit:** a specific premise/possible capability/relation with beneficiary, context, source revision and nearest predecessor.

**Minimum intellectually meaningful record:** baseline and boundary; direct effects; downstream propagation with *per-link mechanism and assumptions*; relevant second-order/systemic interactions; benefits/harms for affected parties; conditional forks and non-effects; evidence and counterevidence; opportunity versus mechanism classification; consequence depth already covered; gaps and reason for stopping.

**Key distinctions:** temporal order is not causality; several effects can share a premise without causing one another; a proposed consequence is not an observed effect; opportunity generation is not a new selected ProductPossibility. No artificial consequence-chain length or branch quota.

**Negative case:** the only plausible later effect lacks a causal bridge or depends on a forbidden authority transfer. Correct output is a bounded gap or failed chain, not a fabricated positive cascade.

## 5. Convergent Reassessment profile

**Unit:** dated reconsideration of one or more explicitly identified, previous, purpose-relative comparisons or a genuine adopted decision, with original frame and source/revision preserved. Inquiry priority, strategic attractiveness, implementation priority and adopted authority must not merge into a universal rank.

**Possible outcomes:** unchanged same grounds; unchanged preference with narrowed conditions/changed grounds; conditional/incomparable/unresolved; localized reordered preference; option-set inadequate/reopen alternatives; evidence/owner authority needed; actual decision reconsideration **only under appropriate authority**. Reassessment never erases the predecessor.

**Negative case:** a new document about an already explored topic with no new decision-relevant consequence does not compel a portfolio rerank. A pairwise change does not become an eight-item ordinal order.

## 6. Adversarial Review profile

**Unit:** a reviewable exact target and an objection with attribution, source/epistemic class and falsification or impact pathway. Cover counterevidence, failure scenario, inference gap, missing alternative/consumer, changed assumption, beneficiary harm, violated contract or owner intent, and false closure.

**Response:** accepted defect, supported rebuttal, narrowed claim, modified design, bounded inquiry, explicitly tolerated risk or unresolved concern. Record why the response answers the original challenge; changed proposal may create new consequences and return to depth/reassessment. No automatic veto or forced repair for hypothetical concerns.

**Negative case:** an imagined failure treated as current observed defect, or a code patch offered as the answer to an unsupported empirical benefit claim. Both fail epistemic alignment.

## 7. Architecture Synthesis profile

**Unit:** a proposed coherent design for a specific intended user/product outcome, informed by compared options, consequences and substantive objections. Check internal compatibility, ownership, boundaries, interactions, source-to-requirement rationale, risks, reversibility, acceptance questions and open decisions.

**Views and existing artifacts:**
- Requirement/PRD view: reuse `to-prd` and existing `prd` contract only when requirements work is warranted.
- Multi-option analysis: reuse existing `architectural_synthesis` without altering its meaning or validator.
- Technical design view: use repository-native prose/spec or existing selected design/handoff; do not add a new canonical `architecture_spec` artifact without a producer/consumer.
- Construction plan: separate downstream responsibility, never inferred from the existence of a spec.

**Negative case:** a design has excellent structural detail but no traceable beneficiary/requirement, or claims final approval from a provisional preference. It is incomplete or unapproved, not a coherent authorized design.

## 8. Real reference cases and independent questions

Start from real source-pinned history rather than invented demonstrations:
1. `artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md`: write authority narrows a provisional preference; a derived possibility remains hypothetical.
2. `docs/explorations/2026-11-03-depth-situated-knowledge-and-possible-futures.md`: consequences of global versus invented contextual applicability.
3. `docs/explorations/2026-11-03-portfolio-reassessment-architectural-generativity.md`: bounded pairwise inquiry-priority revision without rewriting the historical portfolio.
4. `artifacts/history/2026-11-01-graph-activation-architectural-synthesis.md`: comparison, potential failures, complementary mechanism and refusal to equate availability with application.
5. Existing `architectural_synthesis` and `prd` contracts as a **normative cross-artifact handoff case**, not a historically verified combined design.

Author local competency questions sufficient to recover: original identity and revision; causal chain limits; alternative forks; beneficiary distribution; consequence-to-preference delta; no-change; inquiry-versus-product-versus-implementation priority; challenge grounds; response-versus-resolution; residual risk; PRD-versus-architecture handoff; scope/authority; no automatic stage; source-to-design traceability; epistemic claim ceiling; subsequent stopping. Questions should be operationally answerable by a future reader, not vague aspirations.

## 9. Portable consumption and retention

Represent in **dated Markdown profiles and historical cases first**. Expose guidance conditionally via the existing `using-sensemaking` / strategic-analysis / semantic-steward reference chain only where a decision genuinely changes. One existing optional record profile may serve all four; avoid four compulsory forms. Historical records remain immutable.

Selectively add definitions or cited source-case claims to existing schema-v1 `.sensemaking/knowledge/` only if actual query/re-entry needs are demonstrated. No bulk source promotion, new relation predicate, parser, graph scoring, causality engine, runtime router, registered workflow, mandatory phase, PRD authority or extra public Skill. If a later verified consumer cannot recover decisive distinctions, use the existing schema-evolution procedure **as a separately justified change**, with compatibility and authority review.

## 10. Evidence and acceptance ceiling

**Documentary success** means a source-literate reader can reconstruct all four questions, their distinct outputs, the source-grounded cases, the feedback between operations, protected owner decisions, and a coherent proposal's rationale without confusing hypotheses with observed outcomes.

**Package/retrieval success** means any actually changed Skill references ship and load through supported installation paths and any selective knowledge pack can be built, retrieved and traced to exact source revisions.

**Not established by this work:** improved independent-agent creativity, better choice quality, real user value, host invocation of the guide, automatic causal inference, accepted PRDs, implemented architecture or ratified strategy. These require separate warranted observation and authority.

**Stop** once the documentary roles, cases, conditional guidance and evidence ceilings are reconstructible. Do not extend to executable semantics just to reproduce the conceptual diagram.
