# Strategic Evolution & Learning Ontology v1 — Design Basis

**Date:** 2026-11-05  
**Status:** owner-agreed **planning design**, not an implemented ontology, public Skill, strategic analysis, strategy change or executable schema.  
**Assessed repository:** `ThorStarlord/sensemaking-skills@32562d3364fe90c8f53317ea75eb96db3ba7d635`. Reconfirm source HEAD, governance, contracts and source cases before implementation.  
**Companion implementation plan:** [2026-11-05 detailed plan](../plans/2026-11-05-strategic-evolution-learning-ontology.md).  
**Authority:** current product strategy, ADR 0029 / 0031 / 0034, accepted Level-3 Strategic Repository Sensemaking / Strategic Continuity contracts, existing Learning / Reconciliation Policy and actual owner/delegated authority.

## 1. Owner intent and design decision

The owner wants to explore ontological structure for two connected inquiry responsibilities:

| Profile | Question | Intended meaning |
| --- | --- | --- |
| **Strategic Evolution Analysis** | **Where should this system evolve, and why?** | Evolution opportunities, differentiated plausible futures, strategic rationale, justified direction or deliberate nonselection. |
| **Learning & Reassessment** | **What did we learn, and what changes?** | Source-attributed change or reaffirmation of understanding, uncertainty, lessons and consequences for judgments, responsibilities and strategy *where warranted*. |

**Selected approach:** **one shared Level-2 conceptual extension with two independently optional, differentiated profiles**. Reuse existing `Strategic Frontier`, `ProductPossibility`, `ConstructionPath`, `Decision`, `ConsequenceHypothesis`, `AssessmentRevisionAccount`, `strategic_repository_analysis`, `strategic_reconciliation`, `Strategic Continuity` and Learning / Reconciliation. Add only documentary roles and conditional crosswalks where existing concepts do not make the perspective clear.

**Working documentary roles (not new parsed types):**

- `StrategicEvolutionRationale`: a purpose-relative, source-grounded explanation linking governing intent, present capabilities/limits, plausible future outcomes, evolution opportunities, construction-path alternatives, tradeoffs, warranted strategic disposition and reconsideration conditions.
- `LearningAccount`: an attributed explanation linking *prior explicit understanding* to new observations, analysis, owner intent or cross-episode material; stating what actually changed, its epistemic ceiling/applicability, what remains unchanged, and any distinct Level-2, Level-3, Level-4 or doctrine implications.

The profiles complement the [Connected Prospective Inquiry Ontology](../../semantic-architecture/connected-prospective-inquiry-ontology.md), not append two mandatory stages to it. A strategy analysis can invoke consequences, review or synthesis as needed; a learning account may cause no priority change, localized reassessment, a new possibility hypothesis, a changed bounded responsibility, or (with authority) strategic/owner review.

## 2. Approaches considered

| Approach | Benefit | Failure/limit | Disposition |
| --- | --- | --- | --- |
| **A. Only cross-reference existing strategy and policy docs** | Minimal footprint; no duplication | Does not directly surface how a novel user end, strategic direction and evidence-driven conceptual learning fit together; cross-session reconstruction may remain scattered | Viable minimal fallback if the reference cases reveal no missing distinction |
| **B. One shared conceptual extension + two focused profiles** | Integrates strategy and learning across already supported entities, preserves source identity and optionality, and supplies portable decision-facing guidance | Risk of redundant prose; must substantiate its purpose via explicit source cases and competency questions | **Recommended and selected planning basis** |
| **C. Executable strategic-learning graph, scores, routing or self-modifying policy runtime** | Potentially machine-queryable trajectories | No demonstrated missing parsed consumer; risks duplicated control, false causal inference, strategic-authority confusion and knowledge inflation | **Not warranted in v1** |

An ontology should improve *meaning and recoverability* first. No new universal `StrategyState`, `BeliefState`, `LearningEngine`, mandatory lesson artifact, workflow stage, automatic frontier ranking, doctrine mutator, causal predictor or public Skill is authorized by this design.

## 3. Current foundations and non-identities

Source-of-truth hierarchy and exact meaning must be inspected again at implementation:

- `CONTEXT.md`, `docs/product-strategy.md`, ADR 0029 / 0031 / 0034: product identity, authority and value boundaries; Level-4 outcomes require their actual owner ratification.
- `docs/strategic-repository-sensemaking-v1.md` and `skills/strategic-repository-analysis/SKILL.md`: Level-3 strategic model, opportunity landscape, system and goal fitness, capability/limitation map, Strategic Frontier, alternative construction paths, qualitative comparison, future hypothesis admission, current evidence/uncertainty, substantive disposition and candidate responsibility. Current canonical `strategic_repository_analysis` uses `schema_version: 2`.
- `docs/strategic-state-contract.md` and `STATUS.md`: authoritative meaning and current Level-3 projection; keep Strategic Decision to Support, active/deferred boundaries, thesis tensions and owner scope.
- `docs/strategic-continuity-v1.md`: immutable prior/new `strategic_repository_analysis` lineage, assessed source revision, decision assumptions/reassessment triggers and declared path transition results; mechanical `strategy compare/drift/history/graph` does not infer semantic judgment.
- `skills/using-sensemaking/references/learning-reconciliation-policy-v0.md`: canonical current-model interpretation of evidence; permits `NO_MODEL_CHANGE`, `CONFIRM`, `REVISE_CLAIM`, `RESOLVE_UNCERTAINTY`, `OPEN_NEW_UNCERTAINTY`, `CHANGE_RESPONSIBILITY`, `CONTINUE`, `STOP`, `REOPEN_STRATEGY` and `THESIS_REVIEW_REQUIRED` without automatic mutation.
- `skills/strategic-repository-reconciliation/SKILL.md` and `artifact-contracts.yaml`: current canonical durable `strategic_reconciliation` producer/consumer/fields; preserve source attribution, prior claim/assumption, selected path and strategic effect. Do not add an alternative producer or loosen validators.
- `docs/research/capability-learning-loop-v0.md`: existing three loops (responsibility, repository and higher-order capability learning) with generalization and qualification thresholds; conceptual cross-episode doctrine promotion is **not** a deployed learning engine.
- `docs/semantic-architecture/ontology.md`, `possibility-assessment-ontology.md`, `connected-prospective-inquiry-ontology.md`: source-grounded typed entities; distinct inquiry, strategic and implementation priorities; documentary `ConsequenceStructure`, `AssessmentRevisionAccount`, `ChallengeResponseAccount`, `DesignRationaleView`.
- `docs/semantic-architecture/competency-questions.md`: existing **CQ-115–130** for longitudinal learning, including retrieval versus beneficial use; new local competencies must not duplicate these global IDs or imply they are passed.

**Non-identities to preserve:**

```text
evolution opportunity != missing feature != issue != strategic frontier automatically
product end != capability mechanism != architecture option != construction path
plausible future != observed product outcome
qualitative strategic preference != decision != implementation authority
LearningAccount != strategic_reconciliation artifact != generic belief state
repository changed != our interpretation changed != owner intent changed
currentness drift != strategy invalidated
retrieved historical lesson != applied lesson != beneficial later-agent outcome
one local lesson != cross-repository doctrine
learning occurred != changed strategic priority
Level-2 semantic formalization != Level-2 bounded-control responsibility
```

The *same* original typed target, historical decision or possibility can appear in successive documentary views while keeping its canonical type, source revision, actor and original ID. Narrative `supports`, `motivates`, `reconsiders` or `exposes` relations remain *explanatory* unless a separately justified, existing-compatible parsed relation consumer is established.

## 4. Strategic Evolution Analysis profile

**Unit:** one source-bounded repository/system and its governing intent, a strategically material question, credible alternative ways of changing future outcomes, and the current portfolio of capability/evidence constraints.

**Core account `StrategicEvolutionRationale`**, proportionate to the decision:

1. **Purpose and currentness:** named intended beneficiary, accepted product outcome, source-authoritative strategy revision, current capability and limits; distinguish owner request from inferred or proposed new value.
2. **Value opportunity and abstraction:** distinguish (a) a distinct future user end, (b) ability to realize a known end, (c) a different design mechanism, (d) architecture/authority change, (e) simplification or retirement, (f) maintenance repair. A useful local fix need not be a Level-3 evolution.
3. **Future hypothesis and option set:** identify coherent futures grounded in existing capabilities, relationships, prior alternatives, relevant constraints or accepted intent; distinguish proposed opportunities from presently observed capability and from newly ratified strategy. One, multiple, or zero real paths are valid.
4. **Present-to-future mechanism:** state what capability would have to change, which causal/enabling hypotheses support that possibility, its assumptions, required dependencies and risk of no effect. Include omission risk and strategic optionality where material.
5. **Qualitative relative judgment:** say why one direction better serves *this purpose now* than nearby viable alternatives, or why no choice is justified. Preserve strategic attractiveness versus inquiry priority versus implementation priority. Do not compute scalar ranks or manufacture symmetrical paths.
6. **Scope and authority:** current Level-3 remit, potential Level-4 thesis tension and source-grounded owner review boundary; recommendation is not ratification.
7. **Reconsideration:** what relevant observation, new lesson, changed owner intent, context shift, unsatisfied beneficiary or path consequence would change this judgment; state stopping/no-selection when appropriate.

**Distinct strategic questions to support:** Does solving a visible proxy/milestone leave the intended end unmet? Is the system failing because an ability is missing, an existing ability is not used, or the wrong outcome is being pursued? Could an architectural relation create a *new category* of desirable future rather than merely another implementation of a known end? Would simplifying or retiring machinery improve the goal more than adding it? When is omission/delay more consequential than a reversible construction risk?

**Output boundary:** reuse actual `strategic_repository_analysis` and `Strategic Continuity` when a substantive Level-3 strategic analysis is performed. `StrategicEvolutionRationale` can be a section, crosswalk or guidance view of that same artifact; it is not a competing strategy file or automatic next-backlog item. A possibility-only inquiry may be completed without reopening Level 3.

## 5. Learning & Reassessment profile

**Unit:** an explicit prior belief/claim/hypothesis/decision assumption/question, the source-bounded new material and their assessed applicability to a current decision. May be triggered by construction, reading, inquiry, owner clarification or later normal use.

**Core `LearningAccount`**:

1. **Original understanding:** original attributable proposition, source and *assessed revision*, confidence/epistemic ceiling, purpose, context and implied decision; preserve historical evidence unchanged.
2. **New material and what kind of change:** separate **WORLD_CHANGED** (repository or observed behavior truly changed), **UNDERSTANDING_CHANGED** (new explanation or recognition of something already there), and **GOVERNING_INTENT_CHANGED** (attributed owner/rule revision). These are conceptual descriptors, not new machine enums; multiple may coexist with explicit grounding.
3. **Evidence type and mechanism:** observation versus read-source interpretation, logically derived conditional, speculative prospect, participant report or cross-episode analogy; ask what the evidence establishes, what it merely suggests and what it does not speak to.
4. **Meaningful delta:** exact revised, affirmed, resolved, contradicted, stale, superseded or still-unassessed *explicit* claim, assumption, uncertainty, lesson, capability attribution or rationale. Include `NO_MODEL_CHANGE` where new data changes nothing decision-relevant.
5. **Applicability and transfer:** what original conditions made a lesson relevant, contrary episodes, contextual dependencies, and whether a later agent retrieved, source-checked, actually applied, used in a consequential decision, or merely observed it. Rejecting an inapplicable lesson is an admissible success.
6. **Decision/priority implications:** distinguish local responsibility change, a named purpose-relative comparison, true Level-3 reopening, Level-4 thesis-review requirement, or no preference change. Do not imply a universal rank update or silent owner authority.
7. **Creative return:** a new possible desired end or strategically valuable question may arise from the changed framing, but remains a hypothetical `ProductPossibility` or inquiry until independently curated/assessed.
8. **Durability and stop:** persist only consequential meaning in already-owned Campaign/PR/reconciliation/ADR/STATUS/lesson/knowledge surfaces; name what a later actor must reconstruct, what evidence would reopen it, and why stopping is warranted.

**Scope remains orthogonal to evidence:**

| Learning scale | Existing owner | Value and threshold |
| --- | --- | --- |
| **Responsibility/episode** | Active agent / Learning & Reconciliation | Improve a live action, claim, uncertainty or verification decision; no separate artifact for trivial work. |
| **Repository/longitudinal** | Strategic Reconciliation + Strategic Continuity, repo-owned history, retained evidence | Preserve why current repository strategy/path should continue, narrow, change or stop. Historical state remains immutable. |
| **Cross-repository capability/doctrine** | Evidence-gated Capability Learning Loop and ordinary authorized Skill/reference/ADR changes | Multiple comparable independent episodes, counterevidence, transfer limits, smallest improvement target, exact-candidate qualification; no automatic Skill editing or generalization from one example. |

**Output boundary:** a `LearningAccount` is not the source of a second `strategic_reconciliation` contract. The latter remains the canonical durable Level-3 producer where warranted. A claim correction can be local; cross-episode inference may remain a candidate; an authentic agent-use claim requires actual use evidence and does not follow from a successful stored record or hosted source-check.

## 6. Relationship to previous assessment, exploration and choice

A single repository future can be reasoned about through previous profiles without mechanical routing:

```text
present evidence + accepted purpose
  -> (where warranted) divergent opportunity / construction paths
  -> conditional consequence structure and exact-target challenge
  -> attributed, purpose-relative comparison / selection or no selection
  -> bounded authorized engineering, user encounter or further inquiry
  -> actual observed result, new source or conceptual insight
  -> LearningAccount: precise changed/unchanged understanding
  -> unchanged direction OR local reassessment OR Level-3 reconciliation
     OR Level-4 thesis review when actual owner authority is implicated
  -> optional new question/possibility, not automatic work
```

- **Convergent Reassessment** from the connected inquiry ontology reconsiders a particular `AssessmentJudgment` / `PortfolioSnapshot` / `ProvisionalPreference` under its declared purpose. It is not the general Learning & Reassessment profile.
- **Strategic Reconciliation** interprets returned evidence against a prior `strategic_repository_analysis` and its concrete path/assumptions, emitting the existing `strategic_reconciliation` machine artifact when necessary. It is not a generic learning diary.
- **Strategic Evolution Analysis** opens or revisits the Level-3 *future-direction question* only where warranted; no change in local evidence mandates strategic reopening.
- **Capability Learning** compares several source-attributed episodes when the question is whether reusable Sensemaking doctrine merits revision; it neither discovers all repositories nor mutates guidance automatically.

An explicit `NO_CHANGE`, `NO_MODEL_CHANGE`, `NO_SELECTION`, `NOT_ASSESSED`, `DEFER`, `STOP` or authority-required outcome can be analytically complete.

## 7. Source-pinned historical and normative cases for implementation

Inspect the actual source files and their own assessed revisions; do not simply restate conclusions:

| Case | Source at planning snapshot | Conceptual question and correct limit |
| --- | --- | --- |
| **A — Strategic evolution choice** | `artifacts/history/2026-10-23-strategic-repository-analysis.md` (inspected source `main@aa13f40115b52f9e7687d742cbc8430d5a9a4a25`) | Why `PATH-1` accretion through genuine responsibilities was preferred to `PATH-2` bootstrap, including value creation, assumptions, construction paths and no automatic implementation authority. |
| **B — Learning changes assumption, not strategy** | `artifacts/history/2026-10-24-strategic-reconciliation.md` (current source `main@b5fc38960491655ffa5d01547c281485a4d59c00`) | Revises `ASSUMPTION-1` about later-session knowledge reachability, confirms `ASSUMPTION-2`, reaffirms PATH-1 and records partial transition—no wholesale strategic reopening. |
| **C — Conditional, local cross-episode lesson** | `docs/normal-use/2026-11-02-cross-episode-source-reentry-learning.md` | Compares PR #691/#697/#701/#704 missing context link mechanisms and counterexample #696; source-pinned reachability improvement is not an independent coding-agent benefit or universally generalizable rule. |
| **D — Inquiry preference is not strategy or build priority** | `docs/explorations/2026-11-03-portfolio-reassessment-architectural-generativity.md` | One provisional pairwise *learning/inquiry* preference changes; historical global priorities, product choice and implementation authority do not. |
| **E — New capability without strategy revision** | `docs/superpowers/plans/2026-11-05-connected-prospective-inquiry-ontologies.md` and its receipt / STATUS | Implementation/source checks establish a documentary capability; `NO_MODEL_CHANGE` regarding Level-3 PATH-1/Level-4 thesis, independent agent value not assessed. |
| **F — Owner intent, world change and interpretation** | **Normative counterexample only** built from accepted ADR and authority contracts | An owner selecting a new product end changes governing intent; a code patch changes repository reality; discovering an already present feature changes knowledge. Do not pretend these occurred as one historical episode. |

**Source and report revisions remain distinct.** No retrospective edit of A–E; no new permanent `poss:`, `Decision` or formal knowledge predicate merely to demonstrate vocabulary.

## 8. Competency design and empirical claim ceiling

Construct a local, source-specific competency set (tentatively `SEL-CQ-01..20`, unique only within this module), with expected answers grounded in cases A–F. It must cover:

1. source/actor/governing-intent and target currentness;
2. outcome versus capability versus mechanism versus local repair;
3. future plausibility from existing evidence and explicit assumed bridges;
4. option diversity without manufacturing paths;
5. omission risk, deferral, simplification and no-change;
6. source-attributed rationale for one current direction and alternatives;
7. strategic attractiveness versus inquiry priority versus implementation authority;
8. Level-3 strategy versus Level-4 thesis tension;
9. exact reconsideration conditions;
10. original claim/assumption and new finding;
11. WORLD versus UNDERSTANDING versus GOVERNING_INTENT change;
12. observed result versus source review versus creative interpretation;
13. changed/unchanged explicit state and rationale;
14. applicability/rejection of past lessons and counterevidence;
15. knowledge retained versus retrieved versus actually applied;
16. consequences that open new future questions without proving demand;
17. local responsibility versus strategic reconciliation;
18. cross-repository lesson/generalization and contrary cases;
19. no unauthorized doctrine or source mutation;
20. stop/reopen and claim ceilings.

Each question may be marked `ANSWERABLE`, `PARTIAL` or `NOT_ASSESSED`, with historical or normative grounding and counterexamples; do not report “agent benefited” from an author-reviewed table or a mechanically valid record. Existing global CQ-115–130 remain authoritative learning coverage.

**Success ceiling:** coherent documentary semantics; source- and actor-reconstructible historical rationales; accurate crosswalk to current contracts; suitable portable reference and packaging path if integrated; actual negative cases. Not independently established: strategically better choice, improved autonomous creativity, transfer/generalization benefit, an executed/new PRD, modified agent weights, causal prediction or owner strategy revision.

## 9. Implementation and evidence economy

The [detailed plan](../plans/2026-11-05-strategic-evolution-learning-ontology.md) governs future execution. Recommended initial implementation creates:

- one conceptual `docs/semantic-architecture/strategic-evolution-learning-ontology.md`;
- one source-pinned case account and one local competency review;
- one portable conditional guide and one **optional sparse** record template;
- minimal navigation/conditional references from existing entrypoint/strategic-analysis/learning-policy surfaces **only when they change real responsibility selection**;
- optional existing `schema_version: 1` reviewed knowledge **only if** a concrete retrieval or consumer gap is first demonstrated.

No automatic graph predicates, new universal learning artifact, schema version, scoring, extra public Skill, mandatory session receipt, fixed workflow, tests manufactured for demonstration, or Level-3/4 strategy mutation. Historical artifact producers/validators and source records remain intact.

**Stop:** when a source-literate later agent can reconstruct both profiles, their shared identities, distinct outcomes, decision/authority/epistemic boundaries and conditional interactions from the existing installed guidance, without a second strategic-state or learning-state system.
