# Strategic Evolution & Learning Ontology v1

**Status:** Level-2 *conceptual/documentary* extension; source-grounded semantics, **not** a graph/schema/runtime implementation, new strategy artifact or owner-ratified direction.  
**Assessed source:** `ThorStarlord/sensemaking-skills@095ae3fdaec229bb5d2d49e7fe5a95969f8ab22e` (merged design/plan PR #753), 2026-11-05. Historical cases have their own older inspected revisions; this ontology does not retroactively change them.  
**Governing:** [product strategy](../product-strategy.md), ADR [0029](../adr/0029-current-product-boundary.md), [0031](../adr/0031-persistent-semantic-stewardship.md), [0034](../adr/0034-ontology-first-adaptive-sensemaking.md), current owner delegation and [Level-3 strategic state contract](../strategic-state-contract.md).  
**Existing semantics reused:** [Strategic Repository Sensemaking](../strategic-repository-sensemaking-v1.md), [Strategic Continuity](../strategic-continuity-v1.md), [Learning/Reconciliation Policy](../../skills/using-sensemaking/references/learning-reconciliation-policy-v0.md), [Capability Learning Loop](../research/capability-learning-loop-v0.md), [Layered Ontology](ontology.md), [Possibility Assessment](possibility-assessment-ontology.md) and [Connected Prospective Inquiry](connected-prospective-inquiry-ontology.md).  
**Design basis:** [2026-11-05 design specification](../superpowers/specs/2026-11-05-strategic-evolution-learning-ontology-design.md).

## 1. Question, value, responsibility and limits

The two questions share *meaningful historical source identity*, not one mandatory process.

| Conditional profile | Decision-quality question | Optional documentary view | Explicitly not implied |
| --- | --- | --- | --- |
| **Strategic Evolution Analysis** | Given current purpose, capabilities and evidence, which credible future directions might create valuable outcomes, and why pursue, defer, reject or not select them? | `StrategicEvolutionRationale`, preferably within an existing `strategic_repository_analysis` or source-grounded strategic report | A new ProductPossibility ratified, a strategy automatically selected, a numeric frontier, authorized construction or Level-4 change |
| **Learning & Reassessment** | Given prior attributable understanding and new material, what was learned, what remains true, and what claim, responsibility, priority or strategy (if any) should change? | `LearningAccount`, within an existing learning/reconciliation, PR, decision or episode source; `strategic_reconciliation` when its canonical Level-3 contract is warranted | An automatic new priority, universal lesson, separate generic learning artifact, model-weight update, owner authority or strategy mutation |

Both **account names are documentary roles of existing authored surfaces**. They are not graph kinds, registered artifact IDs, machine enums, Skill names or new first-load phases. A simple answer can be sufficient where no future actor needs a separate durable account. An explicit `NO_CHANGE`, `NO_MODEL_CHANGE`, `NO_SELECTION`, `DEFER` or `NOT_ASSESSED` can complete the relevant responsibility.

This is **Level-2 conceptual formalization**, not the repository's control-level 2, which governs bounded responsibility/Campaign semantics.

## 2. Shared source-qualified semantic spine

When decision-relevant, each account identifies:

1. **Actual question, actor, purpose and beneficiary:** user-supplied end/intent versus agent interpretation versus hypothetical new goal; who evaluated/selected what, when, and under which delegation.
2. **Original typed target:** `Goal`, `RatifiedIntent`, `ProductPossibility`/`poss:`, `ProductCapability`, `RepositoryElement`, `ArchitectureOption`/`arch:`, `ConsequenceHypothesis`/`conseq:`, `ConstructionPath`/`PATH-n`, `AssessmentJudgment`, `Decision`, `Claim`, `Assumption`, `lesson`/`incident` or explicit prior `strategic_repository_analysis`—without retyping it for the new activity.
3. **Source/provenance and currentness:** original artifact path, historical author/date/ID and **assessed target Git revision**; governing strategy revision; newer report/source revision; competing/counterevidence. A historical record observed in a newer checkout does not mean it assessed that checkout.
4. **Baseline versus delta:** what the original claim, capability, alternative, constraint, uncertainty and priority frame meant; what new material changes, confirms or fails to establish.
5. **Mechanism and decision relevance:** conditional connection between present state and possible future outcome, or between new evidence and a particular earlier judgment; what would materially change the decision, what does not change.
6. **Epistemic and authority ceiling:** directly observed/quoted source fact, derived logical result, inferred interpretation, prospective hypothesis, purpose-relative evaluation, actually ratified decision and verified result are distinct. A recommendation cannot grant release, merge, scope expansion or owner thesis revision.
7. **Limits and stop/re-entry:** unsupported value/causal claims, unassessed affected actors, unchanged alternatives, counterfactuals, new evidence/actor that would warrant a return.

A view may use one paragraph when that fully preserves the decision. The ontology does **not** require reconstructing hidden reasoning, retaining every observation, persisting a universal report or creating a new ontology entry for every source link.

### 2.1 Keep original identities and endpoints

A proposed `ProductPossibility` expresses a potentially desirable end; it is not a confirmed user requirement, actual `ProductCapability`, current code component, architecture mechanism or planned task. `ArchitectureOption` proposes a realization. A `ConstructionPath` describes a contingent transition to a future capability; neither is an executed product outcome. `Strategic Frontier` is a decision-relevant Level-3 unresolved boundary, not an inventory of every issue or imaginative candidate.

The existing `ProductPossibility`, architecture, consequence, assessment, `Decision` and strategic-path IDs retain their source names and typed relation endpoints. An opportunity grouping, changed interpretation or new report label does not prove `sameAs`. Existing architecture/path-specific `mayProduce`, `mayEnable`, `evaluates`, `prefers` and `selects` relations are **not widened to arbitrary prose claims**.

The canonical machine artifacts remain `strategic_repository_analysis` (current `schema_version: 2`) and `strategic_reconciliation` with their original producers, field names, validators and historical v1 compatibility. `Strategic Continuity` authors lineage across immutable earlier analyses. Mechanical `strategy compare/drift/history/graph` projections can show declared differences or source currentness; they **cannot determine** which strategy is correct.

### 2.2 Documentary associations, not executable relations

| Explanation in a report | Source role -> target role | Meaning and disallowed leap |
| --- | --- | --- |
| `groundedIn` | Evolution rationale -> current capability, owner intent and evidence | Source support for **present** state; not evidence future benefit was achieved |
| `mayAdvanceOutcome` | Opportunity or path -> desired outcome and beneficiaries | Hypothetical future value and assumptions; not automatic `ProductPossibility servesGoal` mutation or causality |
| `motivatesComparison` | Changed capability/constraint -> original option set or purpose-relative frame | Which comparison is materially affected; does not rank all members |
| `reconsideredBecauseOf` | Learning account -> exact prior sourced claim/assumption/judgment plus new material | What supports a particular interpretation revision; not full strategy reopening |
| `updatesUnderstandingOf` | Learning account -> interpretation/uncertainty/capability claim | State whether source/world, understanding or owner intent changed; not a new technical component |
| `mayOpenFutureQuestion` | Changed interpretation -> inquiry or hypothesized possibility | Creative reframe; not validated demand, curated goal or owner's product selection |
| `boundedByAuthority` | Recommendation/learning consequence -> actual selecting actor and scope | What remains owner/Level-4 or external; cannot self-authorize |
| `reconsiderIf` | Rationale or retained lesson -> premise, counterevidence or new context | Reassessment condition, **not** an automatic workflow trigger |

These are documentary verbs only: **no new v1 JSON predicate, inferred edge closure, machine-triggered plan, strategic score or self-modifying policy**. A sequence `A may support B` then `B may enable C` never proves that A produces a desirable C. Distinguish observed world change from an agent's changed belief about unchanged reality.

## 3. Strategic Evolution Analysis — future direction, outcome and warrant

**Use when:** the important unanswered question genuinely concerns *where a repository/system should evolve*, or what radically different valuable outcomes existing source-grounded relationships might make conceivable. Do not activate a full Level-3 restart simply because another possibility can be imagined, a code defect exists or a different question is interesting. The [Strategic Exploration Funnel](../../skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md) remains the conditional breadth/depth source.

**Primary unit:** current system and governing intent at an actual assessed revision, one meaningful Strategic Decision to Support, material alternatives, and the beneficiaries/futures the alternatives might serve.

A `StrategicEvolutionRationale` should make these connected interpretations reconstructible where material:

### 3.1 What future is at stake?

- **Desired end:** a genuinely different future user/owner experience or outcome—source-authorized if adopted, expressly hypothetical if discovered through the analysis.
- **Enabling capability:** a new or stronger ability realizing a previously known end.
- **Architectural/technical mechanism:** one or several implementations of a given capability, not automatically new ends or independent strategic paths.
- **Simplification/consolidation/retirement:** reducing burden, removing unsafe autonomy, or freeing capacity can increase outcome value; "evolution" does not mean expansion.
- **Routine repair/maintenance:** useful bounded work may not alter the strategically material future or warrant a Strategic Frontier entry.
- **Thesis challenge:** a proposed different primary beneficiary/problem/JTBD or material product boundary is Level-4 *review material*, not a Level-3 decision just because it is imaginable.

**Goal-fitness test:** would satisfying the stated proxy, milestone or construction gate leave a material accepted outcome unmet? Preserve the explicit owner goal and flag the mismatch rather than silently substituting a new goal.

### 3.2 Why is that future plausible from current reality?

Ground present `ProductCapability` and limits in source; identify which existing architecture/knowledge relationships support a conditional path, what new dependencies/constraints/authority it requires, what capability transition it might unlock and which evidence could defeat it. A future-state strategic hypothesis may be useful without empirical proof of its outcome—but must be described as hypothetical, with source-grounded leverage and a reconsideration trigger.

Preserve the difference between **no capability**, **capability already implemented but unused**, **capability present but source/agent cannot find it**, **capability unverified** and **wrong desired product end**. They imply different responsibilities.

### 3.3 Why prefer this direction *now*, or choose none?

Compare coherent, actually distinct alternatives with a stated beneficiary/purpose using qualitative mission fit, decision value, gain/loss of future options, dependencies, authority, reversibility, risk of commission **and omission/deferral**, evidence sufficiency and maintenance burden. **Do not require** a candidate count, score or total order. An existing `AssessmentFrame` and `AssessmentJudgment` can express comparison rationale without changing original portfolio history.

Separate:
- **Inquiry/exploration priority**: which question to investigate for prospective learning;
- **Strategic attractiveness**: which possible end/direction is compelling for the beneficiary under a frame;
- **Implementation priority**: which specific authorized product change or bounded responsibility can be built now.

A source-attributed `BUILD` strategic disposition nominates a bounded responsibility **only if** a real path is selected and warranted. It is not implementation authorization; cite selecting actor and available authority. `INVESTIGATE`, `DEFER`, `NO_CHANGE`, `OWNER_DECISION`, `THESIS_REVIEW`, and zero coherent paths all remain legitimate existing outcomes.

### 3.4 Reconsideration conditions and stopping

Name the exact source/currentness change, beneficiary/owner intent revision, broken premise, repeated failure, new capability, counterexample, cost/omission change or alternative that would materially alter the choice. A changed file hash alone is **not** evidence of strategy invalidity. Stop once source-grounded options and uncertainty suffice for the present decision, or a protected owner decision is needed.

**Historical anchor:** the [2026-10-23 Strategic Repository Analysis](../../artifacts/history/2026-10-23-strategic-repository-analysis.md) compared source-grounded `PATH-1` accretion through genuine engineering responsibilities against `PATH-2` bootstrap, selected `PATH-1` as a strategy proposal under current intent and identified two assumptions. The record expressly limits work authority. The [2026-10-24 reconciliation](../../artifacts/history/2026-10-24-strategic-reconciliation.md) later narrowed one assumption without reranking/invalidating the entire strategy.

**Negative case:** "A graph file lacks a link, so build a new knowledge engine and replace the product thesis" contains two unsupported jumps: absence in reviewed graph != missing system ability; local source reachability != warranted Level-4 revision.

## 4. Learning & Reassessment — attributable knowledge delta, not automatic priority change

**Use when:** returned evidence, a later source reading, an explicit user choice or an interpretive insight can change a **previous explicit** consequential claim, uncertainty, decision assumption, prior lesson, responsibility or strategic rationale. Trivial success can be closed directly: `LearningAccount` is optional, not a universal learning log.

**Primary unit:** sourced predecessor meaning + new material + exact interpretation and affected decision, with attributable author/date and original/current repository revision. It is **not** a generic permanent BeliefState.

### 4.1 What actually changed?

| Documentary change lens | Question and legitimate example | What cannot be inferred |
| --- | --- | --- |
| **WORLD_CHANGED** | Was an actual repository capability/code/behavior added, removed or modified, and which source/verification supports that? | A new code artifact necessarily changes user value or Level-3 direction. |
| **UNDERSTANDING_CHANGED** | Was a prior analysis mistaken, stale, incomplete, reframed, or missing already-existing source/capability? | The repository changed merely because the agent discovered what was already there. |
| **GOVERNING_INTENT_CHANGED** | Did the owner or authoritative document actually select a different intended beneficiary, product goal, criterion or constraint? | An analyst's interpretation or a new opportunity hypothesis counts as owner ratification. |

These labels are **conceptual descriptors**, not additions to canonical epistemic enums. One episode may contain several, but explain each separately. A changed *world* can affect an earlier *understanding* without evidence of changed *intent*. Do not invent an owner decision where no such source exists.

### 4.2 Evidence -> interpreted delta -> consequence

A useful `LearningAccount` names:

1. **Previous state:** source and revision of the earlier claim, cited premise, assumption, `lesson` or attributed judgment, and the decision it informed.
2. **New material:** what was observed vs source-read vs derived/inferred vs hypothetical vs newly owner-ratified; preserved counterevidence, method/currentness and what remains unobserved.
3. **Revised/unchanged interpretation:** `NO_MODEL_CHANGE`, `CONFIRM`, `REVISE_CLAIM`, `RESOLVE_UNCERTAINTY`, `OPEN_NEW_UNCERTAINTY`, `CHANGE_RESPONSIBILITY`, `CONTINUE`, `STOP`, `ESCALATE`, `REOPEN_STRATEGY` and `THESIS_REVIEW_REQUIRED` keep their existing Learning/Reconciliation Policy meaning. They are **not** new machine fields on the account.
4. **Different decision consequences:** change one bounded responsibility, narrow a specific purpose-relative preference, update `strategic_reconciliation` when prior Level-3 analysis materially changes, or keep strategy untouched. New information does not require a changed rank.
5. **Applicability and limits:** what old fact remains historically true, which context supports the new interpretation, what would reverse it, and which actors/option set were *not* assessed.

**Historical anchor:** in the [2026-10-24 Strategic Reconciliation](../../artifacts/history/2026-10-24-strategic-reconciliation.md), `ASSUMPTION-1` ("later separate sessions query relevant reviewed knowledge") was **REVISE**d to recognize the *reachability prerequisite*, not invalidated as wholly false; `ASSUMPTION-2` was **CONFIRM**ed. `PATH-1` remained selected, with `CONTINUE` and a `PARTIAL` transition and `REAFFIRM` strategic implication. Source identity/history survived. Here learning changed **the interpreted applicability of a strategic assumption**, not evidence of a completed product outcome or a new owner goal.

### 4.3 Retained lesson versus applied value

For material later use, keep distinct:

- **Retained:** a source-attributed historical incident/lesson exists.
- **Retrieved:** an agent/reader actually obtained it.
- **Source-checked:** original incident and current source were inspected for context/currentness.
- **Decision-informing:** the later actor demonstrably *applied, narrowed or rejected* the lesson in a consequential reasoning step.
- **Outcome-supported:** subsequent evidence bears on that step.
- **Independent reuse:** another genuine session applied it without simply repeating the earlier prompt.
- **Comparatively beneficial:** credible source-only or other alternative shows a materially different/better outcome.

Each is a stronger **evidence question**, not an obligatory telemetry stage or runtime enum. Retention and mechanical `context-for` lookup are **not** proof of later agent use or improved strategic/creative reasoning.

A lesson can remain historically accurate while no longer applicable under changed dependencies, authority, source revision or product end. Prefer source-grounded **rejection/narrowing** to forced use. If changed, revise the **current interpretation** through the original owning source, never erase historical event evidence.

### 4.4 Three scales and generalization threshold

| Scope | Existing owning surface | Valid learning decision |
| --- | --- | --- |
| **Episode / responsibility** | Active agent with Learning/Reconciliation; relevant PR/receipt/Campaign when meaningful | Clarify one claim/assumption, close or change a responsibility, stop with `NO_MODEL_CHANGE` without new artifact. |
| **Repository / longitudinal** | Existing strategic analysis, `strategic_reconciliation`, Strategic Continuity, `STATUS.md` and source-backed history | Reaffirm, revise, close or reopen one source-governed path/assumption; protect prior immutable analyses and current Level-3 projection. |
| **Cross-repository capability / doctrine** | [Capability Learning Loop v0](../research/capability-learning-loop-v0.md) and authorized ordinary Skill/reference/ADR changes | Compare materially similar independent episodes, distinct mechanisms, contrary cases and transfer conditions; propose bounded change only if sufficiently warranted. |

**One source episode != universal doctrine.** Four repairs in the *same repository* may illuminate repeated source-to-context reachability failures, but common symptoms do not establish a universal cause across architectures or agent hosts. Transfer requires contextual fit, alternative explanations, independent/heterogeneous corroboration when aiming broad, qualified evidence and actual change authority. No automatic `learning-engine`, auto-edited Skill, training run or doctrine approval is introduced.

**Historical anchor:** [Cross-episode source re-entry synthesis, 2026-11-02](../normal-use/2026-11-02-cross-episode-source-reentry-learning.md) relates PRs #691/#697/#701/#704, notes different mechanisms and a successful counterexample #696, and retains only a local, source-relevant lesson. Mechanically reachable context does not establish agent decision benefit.

### 4.5 Creative return is a question, not a promotion

An interpretive correction can expose a genuinely new desired future or make a rejected mechanism relevant under different conditions. Record it as a **hypothetical ProductPossibility/inquiry** with source lineage and beneficiary/authority limits; compare it separately before nomination into any Strategic Frontier. A newly imagined future is not validated demand, a modified Level-4 thesis or an automatically selected implementation priority.

**Negative case:** in the [2026-11-03 pairwise portfolio reconsideration](../explorations/2026-11-03-portfolio-reassessment-architectural-generativity.md), one *next intellectual inquiry* preference shifts while historical global ranks 3/5 and Level-3 construction remain unchanged. Treating that as a new product strategy is a target/frame substitution.

## 5. How the two profiles connect without a phase controller

```text
source-grounded present capabilities + governing end
 -> (when the future decision is open) StrategicEvolutionRationale:
    credible desired future, mechanism, alternative, conditions, stop
 -> source/agent inquiry, ordinary engineering, adversarial challenge or use
 -> result, revised source, owner intent, or new interpretation
 -> (when decision-relevant) LearningAccount:
    exactly what changed and what did not
 -> a local claim/responsibility update, or
    a specific Convergent Reassessment of one earlier judgment, or
    canonical strategic_reconciliation and Level-3 reopening if warranted, or
    Level-4 thesis-review/owner boundary if truly implicated, or
    a new hypothetical opportunity / no further work
```

This is a **possible evidence loop**, not an obligatory order. A relevant lesson may precede strategic analysis; a source-only strategy answer may not require a retained `LearningAccount`; a read-only possibility exploration may not open Level 3.

- [Connected Prospective Inquiry](connected-prospective-inquiry-ontology.md) **Convergent Reassessment** addresses a *particular dated purpose-relative judgment*. **Learning & Reassessment** also covers changed interpretation, evidence, claims, uncertainty, lesson applicability, responsibility and strategic state, with or without a preference update. Reuse `AssessmentRevisionAccount` when that precise judgment-revision role applies.
- [Strategic Repository Sensemaking](../strategic-repository-sensemaking-v1.md) and the `strategic-repository-analysis` Skill own **future-direction exploration/synthesis** and the canonical `strategic_repository_analysis`; this document provides no rival producer.
- [Strategic Reconciliation](../../skills/strategic-repository-reconciliation/SKILL.md) owns a source-linked Level-3 **returned-evidence versus prior strategic artifact** account, using the current registered `strategic_reconciliation` contract. The conceptual `LearningAccount` is not an alternative producer.
- [Strategic Continuity](../strategic-continuity-v1.md) preserves immutable historical analysis lineage. Machine `strategy drift` reports currentness facts, **not semantic invalidity or new work warrants**.
- [Capability Learning Loop](../research/capability-learning-loop-v0.md) remains an **evidence-gated candidate** for changing reusable guidance, not a second control level or self-modification scheduler.

The active agent owns interpretation, chooses the smallest warranted next responsibility and stops at real authority boundaries.

## 6. Negative outcomes, example boundaries and evidence ceilings

A competent reading may conclude any of:

- **No credible future direction:** zero source-grounded construction paths, real missing owner end or `NO_SELECTION`. Do not invent options to make a portfolio look balanced.
- **Simplify rather than add:** retirement or boundary removal better serves owner outcomes while a proposed new engine offers no distinct consumer value.
- **Local fix, no strategy:** actual implementation changes code or source reachability but does not alter PATH-1, Level-3 frontier or Level-4 product purpose.
- **Interpretation changed, system unchanged:** discovering a previously existing component corrects an inventory claim but not the codebase or owner intent.
- **Lesson inapplicable:** historical context differs and a later agent justifiably declines to follow that precedent.
- **New hypothetical user end:** intellectually valuable next question but not demonstrated demand, selected `poss:`, implementation or thesis revision.
- **Owner intent materially changed:** new source-attributed governing decision requires proper Level-4 author/ratification; never treat inference as authorization.
- **No useful learning account:** returned evidence is not consequential for future decisions and no new durable object is justified.

**Documentary success:** the profiles, historical source identities, conceptual crosswalk, negative cases, conditional portable guidance and limits can be reconstructed by a source-literate agent. **Not established:** superior actual strategic selections, independent creative novelty, beneficial cross-session or cross-repository lesson use, a query engine that proves causal implications, self-modifying AI behavior, automatic strategy approval or new product-market value.

**Retention rule:** prefer existing PR/Strategic Analysis/Strategic Reconciliation/STATUS/ADR/history/Skill references. A new `.sensemaking/knowledge` file is considered only after a real parser/retrieval consumer demonstrates material missing information not recoverable through the cited sources, and current `schema_version: 1` allows truthful representation. Do not duplicate every conceptual relation as an unsupported graph predicate.
