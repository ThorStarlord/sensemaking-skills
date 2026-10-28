# Prospective Reasoning Ontology v1

**Status:** Conceptual Level-2 extension of the Product (Layer 6), Software-system (Layer 2) and Knowledge (Layer 4) ontology, v1. Descriptive only; no executable schema change.  
**Introduced:** 2026-10-28 at `main@b6cf509`, as the first increment of the owner-supplied [Prospective Reasoning Ontology & Pre-Implementation Synthesis v1 plan](../superpowers/plans/2026-10-28-prospective-reasoning-ontology-and-synthesis.md).  
**Authority:** semantic vocabulary only. A proposed architecture, path, consequence or preference described with these terms is not an implemented structure, a strategic selection, an owner decision or an authorization. [ADR 0031](../adr/0031-persistent-semantic-stewardship.md) governs the destination, [ADR 0029](../adr/0029-current-product-boundary.md) the boundary, and [`STATUS.md`](../../STATUS.md) the current Level-3 state.  
**Builds on:** [`product-possibility-ontology.md`](product-possibility-ontology.md) (what could exist) and [`../research/consequence-depth-and-systems-reasoning-v0.md`](../research/consequence-depth-and-systems-reasoning-v0.md) (how far to reason).  
**Reference case and vocabulary fit:** [`prospective-reasoning-competency-v1.md`](prospective-reasoning-competency-v1.md); the case itself is [`../../artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md`](../../artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md).  
**Competency questions:** CQ-089 to CQ-102 in [`competency-questions.md`](competency-questions.md), section N.

## 1. Why the concept exists

Product possibilities record what the product could become. The reasoning that connects a possibility to a structure that could realize it, a path that could reach it, and the consequences of choosing it is mostly not retained. At `b6cf509`:

- Strategic construction paths carry `future_state`, `unlocks`, `risks`, `assumptions` and `reassessment_triggers` (`scripts/validate-strategic-repository-analysis.py`). Consequences exist there only as unidentified prose: none has an identity, its own assumptions, or a link to a possibility it would enable.
- `architectural_review_recommendation` evaluates one supplied `proposed_direction` (`skills/architectural-review/SKILL.md`). No contract retains several architecture options side by side.
- The steward's architecture exploration returns its options in task output (`skills/repository-semantic-steward/references/architecture-exploration.md`, section 6). Rejected alternatives are retained only when a source-reviewed decision exists.
- Consequence Depth v0 is guidance with a stop rule, and its section 6 warns against "a second systems-reasoning artifact merely to record consequence depth". Any consequence representation must therefore earn its place through reuse, not mirror a reasoning stage.

**Decision this changes:** a later agent can recover which structures and paths were considered for a possibility, why one was preferred, and which consequences supported or challenged that preference (CQ-090 to CQ-099). It can also tell a preference from a selection, and a selection from an authorization (CQ-098).

## 2. What the agent does: three independent descriptors of a reasoning activity

These describe **activities**. They are labels an analysis may use for its own provenance, not entity types, Skill routes, workflow stages or runtime states.

| Descriptor | Values | Question it answers |
| --- | --- | --- |
| Operation | `EXPLORE`, `SYNTHESIZE`, `EVALUATE`, `SELECT`, `RECONCILE` | What is the agent doing? |
| Domain | `PRODUCT`, `ARCHITECTURE`, `STRATEGY`, `CONSEQUENCES` (one or several) | What is it reasoning about? |
| Orientation | direction `DIVERGENT` or `CONVERGENT`; scope `BREADTH` or `DEPTH` | How is inquiry directed? |

Direction and scope are independent axes: divergent depth (opening alternatives inside one subject) and convergent depth (comparing finalists in detail) are both legitimate. Neither axis is a subtype of the other.

Existing guidance already instantiates several combinations:

| Existing guidance | Operation, domain, orientation |
| --- | --- |
| Strategic Exploration Funnel, sections 3-5 | `EXPLORE`, `STRATEGY` and `PRODUCT`, divergent breadth, then convergent depth on finalists |
| Consequence Depth v0 (pre-convergence) | `EXPLORE`, `CONSEQUENCES`, depth, before a responsibility is chosen |
| Steward architecture exploration | `SYNTHESIZE` and `EVALUATE`, `ARCHITECTURE`, divergent then convergent |
| `architectural-review` | `EVALUATE`, `ARCHITECTURE`, convergent depth on one proposal |
| Post-convergence consequence exploration (section 7) | `EXPLORE`, `CONSEQUENCES`, depth, after a provisional preference; feeds back into `EVALUATE` |

**Activity is not entity (CQ-089).** An activity produces or changes entities and is recorded, when worth recording, by an analysis artifact. The entities persist independently: the same architecture option can be explored in one session, evaluated in another and reconciled after construction, keeping one identity throughout (section 5).

## 3. What the agent produces: entities

Reuse existing concepts: Claim, Hypothesis, Assumption, Decision, Evidence, Observation (Layers 3 and 4); Component, Contract, Boundary (Layer 2); ProductPossibility, ProductCapability (Layer 6); Responsibility (Layer 5); TargetSnapshot. Add a specialization only where its meaning differs materially.

| Entity | Definition | Closest existing representation | Persistence policy |
| --- | --- | --- | --- |
| `ArchitectureOption` (`arch:`) | A proposed, coherent structural realization of a desired outcome | `alternative` claims (decision-scoped); options in task output | Retain material alternatives, including declined ones |
| `TargetArchitectureState` | The proposed system structure an option would produce | None; prose | Embedded in its option |
| `ArchitecturalTransition` | A proposed change from the current architecture toward a target state | Strategic `path_transitions` (strategy level only) | Embedded in its option; separate only when it affects sequencing across options |
| `FutureCapabilityState` | A hypothesized future product or repository capability state | Strategic path `future_state` and `capability_states` | Reuse the strategic artifact; give it a separate identity only when several analyses reuse it |
| `ConsequenceHypothesis` (`conseq:`) | A conditional predicted effect of an option, path or contemplated change | Strategic path `unlocks` and `risks` (unidentified prose) | Retain when decision-relevant |
| `ComparativeJudgment` | An attributed qualitative assessment between alternatives | Strategic `path_comparison` (nine lenses); `architectural_review_recommendation` | Reuse existing comparison surfaces first |
| `ProvisionalPreference` | A preferred option or path awaiting further reasoning or an authority check | None that is not a Decision | Record separately from any Decision |

Retained without change: `ProductPossibility`, `ConstructionPath` (a coherent trajectory toward a future capability state, defined in `strategic_repository_analysis`), Decision (including strategic dispositions), Observation. Do not introduce a "strategic idea" concept that duplicates ProductPossibility.

### 3.1 Prospective versus observed identity

- A proposed component, contract or dependency is never given an identifier in the namespace of observed things (`component:`, `contract:`). It lives inside its option until it exists.
- When construction makes it real, the new observed entity gets its own identity, and the option or possibility links to it with `realizedBy`. The option's original proposal stays recorded.
- An option that reuses existing structure cites the existing identifiers (for example `component:knowledge-store`); those citations are observations about the present, not about the proposal.
- A path is identified within the analysis that defines it (`PATH-1`). Across analyses, qualify it with its parent: `<analysis_ref>#PATH-1`. Historical records are not renamed.

## 4. Domain specializations

**Architecture.** An option states its target structure, the existing components and capabilities it reuses, the contracts and boundaries it would change, what it requires (authority, dependencies), the invariants it must preserve, its transition from the present, and the consequences it may produce. The target structure is explicitly prospective.

**Strategy.** `strategic_repository_analysis` stays the authoritative Level-3 surface. A construction path's `future_state` is the FutureCapabilityState it targets. Its `unlocks` and `risks` become ConsequenceHypotheses only when a consequence is decision-relevant enough to need identity, assumptions or a link to a new possibility. A path may cite the architecture options it would use. No second strategic-analysis artifact is introduced.

**Consequences.** A ConsequenceHypothesis has a stable identity; a source (option, path or contemplated change); the predicted effect; conditional assumptions; the proposed causal or enabling mechanism; what it affects; a category (`benefit`, `risk`, `constraint`, `opportunity`, `mixed`); a horizon or sequence position when meaningful; supporting evidence; counterevidence or uncertainty; what would change the current decision; and currentness. No numeric probability, impact score or confidence percentage.

**Chain rule.** If A may produce B and B may enable C, A is not thereby shown to enable C. A multi-hop prospective chain stays conditional, and each link keeps its own status.

## 5. One entity through many operations (example)

From the reference case, `arch:receipt-based-memory` (extend the session receipt to retain compared candidates):

```text
EXPLORE     divergent breadth   proposed as one of four options             identity created
SYNTHESIZE  divergent depth     target structure, reused receipt reader     same identity
EVALUATE    convergent breadth  compared with three other options            judgment attributed to the agent
EXPLORE     consequences, depth receipts persist only with commit authority  consequence linked, not merged into option
EVALUATE    convergent depth    not preferred; reconsideration condition set disposition appended
RECONCILE   (later session)     revisited if ADR 0032 is accepted            new assessment appended, history kept
```

The activity changes; the entity, its identity and its history persist.

## 6. Relationships

Meanings are canonical in [`relations-and-epistemics.md`](relations-and-epistemics.md), "Prospective reasoning relations (proposed, conceptual)". Endpoints:

| Subject | Relation | Object |
| --- | --- | --- |
| ArchitectureOption | `proposesToRealize` | ProductPossibility |
| ArchitectureOption | `proposesChangeTo` | Component, Boundary or Contract (existing) |
| ArchitectureOption | `alternativeTo` | ArchitectureOption |
| ArchitectureOption, ConstructionPath | `mayProduce` | ConsequenceHypothesis |
| ConstructionPath | `targets` | FutureCapabilityState |
| ConstructionPath | `advances` | ProductPossibility |
| ConstructionPath | `proposesUseOf` | ArchitectureOption |
| ConsequenceHypothesis | `mayEnable` | ProductPossibility |
| ConsequenceHypothesis | `mayConstrain` | FutureCapabilityState or ProductCapability |
| ConsequenceHypothesis | `challenges` | Assumption or Hypothesis |
| ProductPossibility | `derivedFrom` | ProductPossibility, ConsequenceHypothesis or source evidence |
| ComparativeJudgment | `evaluates` | ArchitectureOption or ConstructionPath |
| ProvisionalPreference | `prefers` | ArchitectureOption or ConstructionPath |
| Decision | `selects` | ArchitectureOption or ConstructionPath |

**Non-identities to preserve:**

```text
proposesToRealize   != realizedBy
proposesChangeTo    != affected_by_change (an observed change)
mayProduce          != observed causation
mayEnable           != established dependency
prefers             != selects
selects             != authorized to execute
derivedFrom         != dependsOn
sharesAssumptionWith != complements
contradicts         != architecture violation
```

Each consequential relationship keeps the provenance required by [`product-possibility-ontology.md`](product-possibility-ontology.md) section 6.1, plus its assessed revision and the conditions under which it would be reconsidered.

## 7. The pre-implementation loop and its feedback outcomes

The loop is conditional and agent-controlled; no phase is mandatory for every task.

```text
recall prior possibilities, options and decisions (when they could change the analysis)
-> explore and synthesize materially distinct options and paths
-> preliminary evaluation: several viable, one credible, none grounded, a provisional preference, or an open uncertainty
-> post-convergence consequence exploration of the provisional preference (only if it could change the decision)
-> feedback into evaluation
-> decision handoff through existing Level-3 / responsibility processes
-> after construction: reconcile observed outcomes with the earlier predictions
```

**Post-convergence depth** is a second use of depth, distinct from the funnel's pre-convergence finalist depth: it follows the downstream effects of a provisional choice (direct changes, dependent users and components, later capabilities, new constraints and invariants, new opportunities, futures made harder, reversibility and opportunity cost). The [Consequence Depth v0 stop rule](../research/consequence-depth-and-systems-reasoning-v0.md) applies: stop when the next layer cannot change the interpretation, responsibility, architecture, verification or a strategic commitment.

**Feedback outcomes** are results of the analysis, not dispositions (the `architectural_synthesis` contract checks them as `preference_feedback` outcomes): `REAFFIRM`, `REVISE_PREFERENCE`, `REOPEN_ALTERNATIVES`, `INVESTIGATE`, `DEFER`, `NO_CHANGE`, `OWNER_DECISION_REQUIRED`, `THESIS_REVIEW_REQUIRED`. Only the existing governing processes turn them into authoritative dispositions: a strategic analysis's `BUILD`, `INVESTIGATE`, `DEFER`, `NO_CHANGE`, `OWNER_DECISION` or `THESIS_REVIEW`, an owner decision, or the Level-4 process. A sound analysis may legitimately end without selection.

## 8. Authority and currentness

- Every prospective record names its target repository and assessed revision. Currentness is checked with existing surfaces (`strategy drift`, knowledge `changes` and `workspace-impact`).
- `ProvisionalPreference` is attributed (who, when, on what basis) and carries no authority. A Decision `selects` only under the authority that decision process holds; selection is still not authorization to execute, merge or release.
- Exploring a counterfactual or thesis-conflicting option needs no review. Level 4 applies only when a product-thesis commitment becomes decision-changing ([`product-thesis-revision.md`](../product-thesis-revision.md), section 4).
- In a target repository, prospective records are authored only under that repository's knowledge-edit authority, cite that repository's sources, and never import another repository's records or authority.
- No artifact or record grants authority by existing; contract flags such as `implementation_authority_established_by_artifact` stay `false`.

## 9. Representation now and next

**Now:** this conceptual model, competency questions CQ-089 to CQ-102, a source-grounded reference case with a vocabulary-fit assessment, reviewed records for that case using existing kinds and predicates (`.sensemaking/knowledge/prospective-reasoning.json`; plan PR C), and the `architectural_synthesis` artifact contract with its template and focused validator, to which the reference case conforms (plan PR D). No claim kind, predicate, knowledge schema version, Skill or runtime is added.

**Where each concept is expected to live** (predictions tested in [`prospective-reasoning-competency-v1.md`](prospective-reasoning-competency-v1.md)):

| Concept | Analysis artifact | Reviewed knowledge (existing vocabulary first) |
| --- | --- | --- |
| ArchitectureOption | `architectural_synthesis` `architecture_options`, with `proposed_transitions` | `alternative` claim with `arch:` id and `attributes.concept` |
| FutureCapabilityState | strategic path `future_state` | artifact reference, not an observed `capability` |
| ConsequenceHypothesis | the synthesis's consequence section, cited by `conditional_consequence_refs` (plan PR F decides any further structure) | `hypothesis` claim with `conseq:` id |
| ComparativeJudgment, ProvisionalPreference | synthesis `option_comparison`, `provisional_preference` | attributes on the analysis reference; never a `decision` claim |
| derived new possibility | synthesis `derived_possibility_refs` | `opportunity` claim `derived_from` the consequence |

## 10. Competency questions served

| Element | Competency questions |
| --- | --- |
| Activity descriptors and the activity/entity distinction (section 2) | CQ-089 |
| Entities and prospective identity (section 3) | CQ-090, CQ-091, CQ-092, CQ-093 |
| Consequence specialization and chain rule (section 4) | CQ-094, CQ-095, CQ-096 |
| Feedback outcomes and stop rule (section 7) | CQ-097, CQ-101 |
| Preference, selection and authority (sections 6 and 8) | CQ-098 |
| Persistence policy and identity across operations (sections 3 and 5) | CQ-099, CQ-100 |
| Conditional loop, no mandatory phase (section 7) | CQ-102 |
