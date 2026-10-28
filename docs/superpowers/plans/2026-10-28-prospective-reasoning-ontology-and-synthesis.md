> **Repository record (2026-10-28).** Owner-supplied program plan, preserved verbatim below from the owner's message in the session that built its first increment.
> **Status:** proposed program plan. Its own section 14 describes the governance it requests; each increment is still selected against current source and authority.
> **Inspected base:** `ThorStarlord/sensemaking-skills` `main@b6cf50998467a42fa999b2cf3a52b7271d14ec6a`.
> **Canonical concepts:** [`../../semantic-architecture/prospective-reasoning-ontology.md`](../../semantic-architecture/prospective-reasoning-ontology.md). This file describes construction; the ontology document is authoritative for meanings.
>
> **Reconciliation with the repository at that base.** The plan text below is unchanged; these notes record how it was applied.
>
> - Conceptual relation names keep the camelCase convention of `relations-and-epistemics.md`; snake_case stays reserved for predicates `knowledge.py` accepts.
> - CQ-089 to CQ-102 are used as proposed: the sequence ended at CQ-088.
> - The six-dimension Product Possibility model (alignment, ambition, horizon, realization, epistemic status, disposition) is unchanged; prospective entities reuse its identity and governing-authority rules.
> - Strategic construction paths already carry `future_state`, `unlocks`, `risks`, `assumptions` and `reassessment_triggers` as prose (`scripts/validate-strategic-repository-analysis.py`); the ontology maps FutureCapabilityState and path consequences onto those fields rather than adding parallel ones.

# Prospective Reasoning Ontology & Pre-Implementation Synthesis v1

**Repository:** `ThorStarlord/sensemaking-skills`  
**Planning baseline:** `main@b6cf50998467a42fa999b2cf3a52b7271d14ec6a`  
**Status:** Proposed development plan — not yet implemented  
**Parent product direction:** Persistent Semantic Stewardship, ADR 0031  
**Implementation philosophy:** Continuous construction, source-grounded semantic reasoning, proportional verification and agent-owned decisions

---

## 1. Executive Summary

### 1.1 Objective

Extend Sensemaking Skills from remembering product possibilities into preserving and using the reasoning that connects those possibilities to architecture, strategy, consequences and implementation decisions.

The system should help an agent reconstruct:

1. What product futures were considered.
2. What architectural structures could realize them.
3. What coherent construction trajectories could lead to them.
4. How alternatives were compared.
5. What consequences might follow from each alternative.
6. Why one direction was preferred, selected, deferred or rejected.
7. Which consequences generated further product possibilities.
8. How later implementation evidence changes those conclusions.

The desired result is **cumulative prospective product knowledge**: understanding not only what the product is, but what it could become and how the available futures change over time.

### 1.2 Primary product outcome

A coding agent working in a later session should be able to recover a consequential earlier ProductPossibility, reconstruct at least two materially distinct ways to realize it, inspect their architectural and strategic implications, recover the previous comparison and its assumptions, and continue the analysis without regenerating everything from conversation history.

If a new consequence creates a distinct product possibility, the agent should be able to retain that possibility and link it to the reasoning that produced it.

If the analysis supports construction, the agent should identify one warranted bounded responsibility without confusing its recommendation with execution authorization.

### 1.3 Non-goals

The program will not introduce:

- A deterministic strategic planner or numerical path-ranking engine.
- A mandatory reasoning pipeline for every coding task.
- A parallel graph database or competing repository source of truth.
- A new Skill for every reasoning operator.
- An automatic mechanism that promotes possibilities into the Strategic Frontier.
- A requirement to explore every consequence before implementation.
- Automatic inference of causal truth from graph connectivity.
- A requirement that a synthesis produce a novel idea every time.
- Automatic Level-4 product-thesis changes or protected external operations.

The existing six-layer Semantic Architecture, ADR 0029, ADR 0031, Level-3 analysis and agent-control boundaries remain governing.

---

## 2. Current Repository Baseline

The development program must reuse the existing infrastructure rather than reconstruct it.

| Existing system | Current capability | Planned extension |
|---|---|---|
| Product Possibility Ontology | Retains possible futures, realization and dispositions | Connect possibilities to prospective architectures, paths and consequences |
| Reviewed semantic knowledge | Git-authored, indexed claims and relations | Encode consequential prospective reasoning using existing types first |
| Strategic Repository Analysis v2 | Capability map, frontier, construction paths, comparisons and disposition | Connect strategic trajectories to architecture alternatives and conditional consequences |
| Strategic Exploration Funnel | Breadth, frontier candidates, candidate depth and comparison | Add explicit post-convergence consequence feedback |
| Architectural Review | Evaluates a supplied architectural proposal | Preserve synthesis of multiple alternatives before or alongside review |
| Consequence Depth v0 | Six-order systems-reasoning guidance | Retain material prospective consequence chains |
| Strategic Continuity | Assumptions, reassessment triggers, history and currentness | Reconsider decisions when relevant assumptions or expected consequences change |
| Repository Semantic Steward | Recall, reconcile and source-grounded knowledge | Retain the useful products of synthesis and evaluation |

### Canonical sources to inspect during implementation

- `docs/semantic-architecture/ontology.md`
- `docs/semantic-architecture/constitution.md`
- `docs/semantic-architecture/competency-questions.md`
- `docs/semantic-architecture/relations-and-epistemics.md`
- `docs/semantic-architecture/product-possibility-ontology.md`
- `docs/idea-library.md`
- `docs/strategic-repository-sensemaking-v1.md`
- `docs/research/consequence-depth-and-systems-reasoning-v0.md`
- `skills/strategic-repository-analysis/`
- `skills/repository-semantic-steward/`
- `skills/architectural-review/`
- `skills/workflow-planner/references/artifact-contracts.yaml`
- `src/sensemaking_skills/semantic_architecture/knowledge.py`
- `src/sensemaking_skills/semantic_architecture/knowledge_store.py`
- `src/sensemaking_skills/strategy_cli.py`

**Important distinction:** The existing `strategic_repository_analysis` artifact already has schema version 2. The persistent knowledge substrate separately accepts authored knowledge versions 1 and 2, while its SQLite store has its own version. These versions must not be conflated.

---

## 3. Architectural Decision: One Shared Ontology, Domain-Specific Extensions

### 3.1 Separate three semantic dimensions

The shared model must distinguish three independent questions.

**A. Reasoning operation — What is the agent doing?**

- `EXPLORE`: Investigate possibilities, interpretations and consequences.
- `SYNTHESIZE`: Combine elements into a coherent proposed structure, state or path.
- `EVALUATE`: Examine and compare alternatives against evidence and governing criteria.
- `SELECT`: Record a preference or decision appropriate to available authority.
- `RECONCILE`: Update prior claims and reasoning using consequential new evidence.

These are conceptual descriptions of reasoning activities. Their existence does not require a new execution engine, Skill router or runtime state machine.

**B. Reasoning domain — What is the subject?**

- `PRODUCT`: User value, intended capabilities and product futures.
- `ARCHITECTURE`: Components, contracts, boundaries and structural alternatives.
- `STRATEGY`: Future capability states, construction paths and product evolution.
- `CONSEQUENCES`: Conditional effects, downstream changes, enabling relationships and risks.

An analysis may span several domains.

**C. Reasoning orientation — How is inquiry directed?**

Maintain two independent axes:

| Axis | Values | Interpretation |
|---|---|---|
| Search direction | `DIVERGENT`, `CONVERGENT` | Expand alternatives or narrow/compare them |
| Exploration scope | `BREADTH`, `DEPTH` | Search across alternatives or investigate selected subjects in detail |

Consequently, divergent depth exploration and convergent depth evaluation are legitimate combinations.

Neither `DEPTH` nor `DIVERGENT` is inherently a subtype of the other.

### 3.2 Preserve independence of activities and knowledge entities

Do not make `ArchitecturalSynthesis` a subclass of `StrategicEvolutionAnalysis`, or vice versa.

Treat both as domain-specific applications of shared reasoning operations.

Likewise, do not turn `DepthExploration` into a permanent subclass of `DivergentExploration`.

The same ArchitectureOption can be explored, synthesized, evaluated, challenged, selected and later revised.

The ArchitectureOption remains one entity through those operations.

### 3.3 Do not create executable types merely for taxonomy

The conceptual model may describe a reasoning operation without storing every thought as a separate claim.

A durable reasoning record should be created when its conclusions, alternatives, relationships or assumptions would materially improve a later decision.

Routine local engineering can continue without creating a reasoning episode.

---

## 4. Proposed Knowledge Ontology

### 4.1 Shared foundation

Reuse existing `Claim`, `Hypothesis`, `Assumption`, `Decision`, `Evidence`, `ProductPossibility`, `ProductCapability`, `Component`, `Contract`, `Boundary`, `Responsibility` and `TargetSnapshot` concepts.

Add conceptual specializations only where they express a materially different meaning.

**Proposed new conceptual entities:**

| Entity | Definition | Persistence policy |
|---|---|---|
| `ArchitectureOption` | A proposed coherent structural realization of a desired outcome | Retain material alternatives |
| `TargetArchitectureState` | A proposed system structure associated with an architecture option | May be embedded in an option initially |
| `ArchitecturalTransition` | A proposed change from the current architecture toward a target structure | Retain when it affects sequencing or feasibility |
| `FutureCapabilityState` | A hypothesized product/repository capability state | Reuse existing strategic artifact representation where possible |
| `ConsequenceHypothesis` | A conditional predicted effect of an option, path or change | Retain when decision-relevant |
| `ComparativeJudgment` | An attributed qualitative assessment between alternatives | Reuse existing comparison artifacts first |
| `ProvisionalPreference` | A preferred option awaiting confirmation after further reasoning or authority checks | Represent separately from a ratified decision |

**Existing entities to retain:**

- `ProductPossibility`: a potential product future.
- `ConstructionPath`: a coherent trajectory toward a future capability state.
- `StrategicDecision`: an authoritative or appropriately attributed strategic disposition.
- `Observation`: source-grounded evidence about what currently exists or happened.

Do not introduce a parallel `StrategicIdea` class that duplicates ProductPossibility.

### 4.2 Architectural specialization

Architectural synthesis should answer:

- Which existing components and capabilities can be reused?
- What architectural alternatives could realize the desired outcome?
- What contracts and boundaries would each alternative modify?
- What would each alternative require?
- Which invariants must remain valid?
- How would the current system transition toward each target architecture?
- What new possibilities would the architecture enable or constrain?

An ArchitectureOption should include its proposed structure, rationale, key structural differences, constraints, assumptions, implementation dependencies and known or hypothesized consequences.

Its target structure must remain explicitly prospective.

A proposed component is not an observed component. A proposed dependency is not a current dependency.

### 4.3 Strategic specialization

Strategic evolution analysis should answer:

- Which future product capability states are strategically meaningful?
- What existing capabilities create leverage toward them?
- What plausible construction paths connect the present to those futures?
- Which paths are materially different?
- What would each path enable, constrain or postpone?
- Which strategic assumptions differentiate the paths?
- What is the cost of choosing incorrectly or not pursuing an opportunity?
- Which direction is most warranted under current intent and authority?

Reuse `strategic_repository_analysis` for the governing Level-3 decision.

The new ontology should enrich its semantic references, not replace its Strategic Frontier or decision contract.

### 4.4 Consequence specialization

A ConsequenceHypothesis describes an effect that **might occur under stated conditions**.

Minimum semantic content:

- Stable identity.
- Source option, construction path or contemplated change.
- Predicted effect.
- Conditional assumptions.
- Proposed causal or enabling mechanism.
- Affected capability, contract, architecture or decision.
- Consequence category: benefit, risk, constraint, opportunity or mixed effect.
- Relevant future horizon or sequence position, when meaningful.
- Evidence supporting the inference.
- Counterevidence or uncertainty.
- What would change the current decision.
- Currentness and historical reassessment.

Do not require numeric probability, impact scores or confidence percentages.

Do not infer that because A may cause B and B may enable C, A is proven to enable C.

A multi-hop prospective chain remains conditional and potentially contestable.

---

## 5. Relationship Ontology

Establish endpoint types and semantic meaning before adding executable predicates.

### 5.1 Proposed conceptual relations

| Subject | Relationship | Object |
|---|---|---|
| `ArchitectureOption` | `proposesToRealize` | `ProductPossibility` |
| `ArchitectureOption` | `proposesChangeTo` | `Component`, `Boundary` or `Contract` |
| `ArchitectureOption` | `alternativeTo` | `ArchitectureOption` |
| `ArchitectureOption` | `mayProduce` | `ConsequenceHypothesis` |
| `ConstructionPath` | `targets` | `FutureCapabilityState` |
| `ConstructionPath` | `advances` | `ProductPossibility` |
| `ConstructionPath` | `proposesUseOf` | `ArchitectureOption` |
| `ConstructionPath` | `mayProduce` | `ConsequenceHypothesis` |
| `ConsequenceHypothesis` | `mayEnable` | `ProductPossibility` |
| `ConsequenceHypothesis` | `mayConstrain` | `FutureCapabilityState` or `ProductCapability` |
| `ConsequenceHypothesis` | `challenges` | `Assumption` or `Hypothesis` |
| `ProductPossibility` | `derivedFrom` | `ProductPossibility`, `ConsequenceHypothesis` or source evidence |
| `ComparativeJudgment` | `evaluates` | `ArchitectureOption` or `ConstructionPath` |
| `ProvisionalPreference` | `prefers` | `ArchitectureOption` or `ConstructionPath` |
| `Decision` | `selects` | `ArchitectureOption` or `ConstructionPath` |

These are proposed semantic relations, not an assertion that the current `knowledge.py` accepts their names.

### 5.2 Required relationship distinctions

Preserve these non-identities:

- `proposesToRealize` is not `realizedBy`.
- `mayProduce` is not an observed causal relationship.
- `mayEnable` is not an established dependency.
- `preferred` is not `selected`.
- `selected` is not `authorizedToExecute`.
- `derivedFrom` is not necessarily `dependsOn`.
- `sharesAssumptionWith` is not automatically `complements`.
- `contradicts` is not automatically an architecture violation.

### 5.3 Relationship provenance

Every consequential relationship should preserve:

1. Source and target identities.
2. Relationship meaning.
3. Epistemic status.
4. Establishment basis: observed, inferred, hypothesized or appropriately ratified.
5. Source/evidence references.
6. Target repository and assessment revision.
7. Material assumptions.
8. Invalidation or reconsideration conditions where applicable.

Historical conclusions must remain reconstructible when newer evidence changes the interpretation.

### 5.4 Identity and naming conventions

Illustrative identities:

- `poss:target-repository-discovery-memory`
- `arch:git-reviewed-local-memory`
- `arch:receipt-based-memory`
- `conseq:portable-possibility-recall`
- `hyp:later-agent-reuses-options`

For construction paths, preserve the existing analysis-local `PATH-1`, `PATH-2` conventions.

When referenced across analyses, qualify a path using its parent analysis identity rather than assuming `PATH-1` is globally unique.

Do not rename historical records simply to conform to a new naming scheme.

---

## 6. Competency Questions and Formalization Requirements

Add a new section after the existing Product Possibility questions in `docs/semantic-architecture/competency-questions.md`.

The current sequence ends at CQ-088, so use **CQ-089 onward**, reconciling numbering against `main` at implementation time.

Proposed questions:

| ID | Competency question |
|---|---|
| CQ-089 | Can the system distinguish an exploration/synthesis/evaluation activity from the entity it produced? |
| CQ-090 | Which ProductPossibility motivated a particular ArchitectureOption? |
| CQ-091 | Which proposed architectural components, contracts and boundaries would an option change? |
| CQ-092 | How do two architecture options differ structurally, and what existing capabilities do they reuse? |
| CQ-093 | Which future capability state does a construction path target, and what transitions does it propose? |
| CQ-094 | Which consequences are predicted to follow from a provisionally preferred option? |
| CQ-095 | Which predicted consequences depend on unresolved assumptions rather than observed effects? |
| CQ-096 | Which consequence generated a genuinely distinct new ProductPossibility? |
| CQ-097 | Which discovered consequence could change the comparison or provisional preference? |
| CQ-098 | Why was a direction preferred, selected, deferred or rejected, and under which authority? |
| CQ-099 | Can a later agent reconstruct the architectural and strategic reasoning without the original conversation? |
| CQ-100 | Can the system distinguish a restated idea, revised idea, new synthesis and already rejected alternative? |
| CQ-101 | Can the agent stop deeper exploration when further consequences would not change the decision? |
| CQ-102 | Can ordinary bounded work proceed without a mandatory full pre-implementation analysis? |

For every question, document:

- The decision the answer would support.
- The required semantic entities and relationships.
- The current repository's closest representation.
- Whether the question is expressible, awkward or not expressible.
- What information is lost, if anything.
- Which schema or Skill capability would resolve the loss.

This analysis should follow the pattern of `docs/semantic-architecture/architecture-ontology-competency-v1.md`.

It must not be used as an excuse to delay all construction until an exhaustive ontology assessment is complete.

---

## 7. Artifact and Executable Schema Design

The plan distinguishes **analysis artifact contracts** from **persistent semantic knowledge schemas**.

Artifact contracts preserve the bounded reasoning result of an analysis.

Knowledge schemas preserve source-grounded claims and relationships for later reuse.

They should connect through stable references, without making both sources authoritative copies of the same facts.

### 7.1 Architectural Synthesis artifact

**Proposed artifact identity:** `architectural_synthesis`

This is the strongest candidate for a new standalone artifact contract.

The current `architectural_review_recommendation` contract evaluates a concrete proposed direction. It does not serve as a durable multi-option structural synthesis contract.

Proposed content:

| Field family | Meaning |
|---|---|
| `target_repository`, `target_source_identity` | Exact repository/currentness context |
| `governing_intent_refs` | Accepted strategy, constraints and authority |
| `target_possibility_refs` | Product possibilities being addressed |
| `current_architecture_refs` | Existing components, contracts, boundaries and evidence |
| `architecture_options` | Proposed alternative structures |
| `proposed_transitions` | Structural changes required by each option |
| `assumption_refs` | Material dependencies and uncertain premises |
| `conditional_consequence_refs` | Predicted effects |
| `option_comparison` | Qualitative architectural comparison |
| `provisional_preference` | Preferred option and rationale, if warranted |
| `unresolved_questions` | Decision-changing uncertainty |
| `authority_and_claim_boundaries` | Explicit limits of recommendation and authorization |

An illustrative machine-readable summary:

```yaml
artifact_id: architectural_synthesis
schema_version: 1

target_repository: owner/repository
target_source_identity: "<exact revision>"

target_possibility_refs:
  - poss:target-repository-discovery-memory

architecture_options:
  - option_id: arch:git-reviewed-local-memory
    proposed_structure: >
      Store source-grounded possibility records
      in the target repository.
    proposed_contract_changes:
      - "Repository-local authored knowledge contract"
    assumption_refs:
      - hyp:later-agent-reuses-options
    conditional_consequence_refs:
      - conseq:portable-possibility-recall

  - option_id: arch:receipt-based-memory
    proposed_structure: >
      Extend existing session records to retain
      the compared candidate set.
    assumption_refs:
      - hyp:receipt-retrieval-is-sufficient

provisional_preference:
  option_id: arch:git-reviewed-local-memory
  rationale: >
    Candidate preference for consideration;
    comparison remains subject to assumptions.
  status: PROVISIONAL

semantic_truth_established: false
implementation_authority_established_by_artifact: false
```

This is a design example, not a schema already registered in the repository.

Implementation tasks:

1. Define its contract in `artifact-contracts.yaml`.
2. Provide an authoring template.
3. Add a focused validator for IDs, links, required fields, status separation and authorization invariants.
4. Preserve an explicitly valid outcome with no preferred option.
5. Establish which existing Skill authors the artifact.
6. Avoid introducing a separate Architectural Synthesis Skill merely to generate the artifact unless normal use demonstrates a stable, independently warranted responsibility.

**Acceptance:** An agent can compare materially different architectural structures, retain their rationale and retrieve the result later without representing proposed structures as implemented facts.

### 7.2 Strategic Evolution artifact integration

**Reuse:** `strategic_repository_analysis`, schema version 2.

Do not create `strategic_evolution_analysis` as a competing canonical artifact.

Evaluate additive, optional references such as:

- `relevant_possibility_refs`
- `architecture_synthesis_refs`
- `conditional_consequence_refs`
- `future_capability_state_refs`
- `comparison_assumption_refs`

These names are proposals; their final placement and types must be reconciled with the existing validator and source contract.

In particular:

- Reuse `construction_paths`, `path_comparison`, `decision_assumptions` and `reassessment_triggers`.
- Preserve the existing nine qualitative comparison lenses.
- Keep the distinction between Strategic Frontier candidates and construction paths.
- Do not place a merely provisional architecture preference into a field that signifies a selected strategic path.
- Preserve zero-path and no-selection outcomes.
- Preserve historical v1 and v2 artifact readability.
- Keep the artifact's authorization and semantic-truth flags false.

**Acceptance:** A strategic analysis can cite its architectural alternatives and material consequence hypotheses while remaining the authoritative Level-3 analysis surface.

### 7.3 Depth / Consequence Exploration schema

Initially define the smallest structured representation that the reference case needs.

Proposed identity if a standalone artifact is warranted:

`prospective_consequence_assessment`

Minimum fields:

- Source option/path and exact analysis identity.
- Assumptions and conditional predicates.
- Consequence hypotheses.
- Affected product, architecture and decision references.
- Material dependency or enabling chains.
- Distinct new possibilities produced through exploration.
- Counterevidence and invalidation conditions.
- Comparison implications.
- Resulting recommendation: reaffirm, revise comparison, reopen alternatives, defer or escalate.

**Important:** Before registering a separate artifact, assess whether the required structure can be represented faithfully as an optional section or companion of `architectural_synthesis` and `strategic_repository_analysis`.

A separate artifact is warranted when consequence analysis has independent authorship, reuse, currentness, validation or consumer needs.

It should not exist merely to mirror a conceptual reasoning stage.

### 7.4 Persistent knowledge encoding

Before extending `knowledge.py`, attempt to express the reference case using existing reviewed claim kinds and predicates.

Candidate encodings:

- ProductPossibility → existing `opportunity` convention.
- ArchitectureOption → evaluate `alternative` or a hypothesis claim with a clearly identified conceptual type.
- ConsequenceHypothesis → existing `hypothesis` kind, if its source and effect relationships can be recovered faithfully.
- FutureCapabilityState → prospective claim or artifact reference, not an incorrectly observed `capability`.
- StrategicDecision → existing decision and strategy artifact references.
- Provenance/derivation → `derived_from` where its semantics match.
- Shared assumptions → explicit hypothesis nodes and `references`.

Do not use `depends_on`, `implemented_by` or `contradicts` as substitutes for different concepts merely because those predicates exist.

Where an existing predicate approximates a new semantic relation through unchecked attributes, record the approximation and test whether it loses a decision-relevant distinction.

### 7.5 Executable schema specialization

Specialize only the meanings justified by the reference case.

Candidates worth examining first:

- Prospective architectural realization versus observed realization.
- Conditional consequences versus observed impacts.
- Relationships connecting a consequence to a newly enabled ProductPossibility.
- First-class identity for architectural alternatives.
- Provenance of qualitative comparison judgments.

For each proposed new kind or predicate, answer:

1. Which competency question fails with the existing vocabulary?
2. What answer becomes ambiguous or unavailable?
3. Why is a generic `references` edge insufficient?
4. Which consumer needs the distinction?
5. Can the new semantics be checked mechanically without claiming semantic truth?
6. How are existing authored records and indexes preserved?

Prefer additive authored-schema compatibility and a rebuildable index over unnecessary SQLite migrations.

ADR 0033's proposed status remains separate from authorization to introduce new shared semantics.

---

## 8. Pre-Implementation Reasoning Loop

The intended loop is conditional, iterative and agent-controlled.

### 8.1 Exploration and synthesis

Start with governing intent, current capabilities, relevant knowledge and a meaningful opportunity.

Recover prior ProductPossibilities and historical alternatives when they could change the analysis.

Explore materially distinct futures and architecture options.

Synthesize coherent proposals rather than producing an unstructured list of features.

### 8.2 Preliminary evaluation

Compare options at the level necessary to determine which deserve further attention.

The result may be:

- Several viable alternatives.
- One credible alternative.
- No sufficiently grounded option.
- A provisional preference.
- An unresolved decision-changing uncertainty.

A preference is not automatically an authorized final selection.

### 8.3 Post-convergence consequence exploration

When deeper implications could change the preferred direction, examine what follows conditionally.

The existing pre-convergence depth drill remains valid. This is a second use of depth, focused on the downstream effects of a provisional choice.

Explore:

- Direct architectural changes.
- Effects on dependent components and users.
- Changes to later product capabilities.
- New constraints and invariants.
- Further architectural dependencies.
- New opportunities enabled by the choice.
- Futures made harder or less attractive.
- Decision-relevant reversibility and opportunity costs.

Stop when further depth cannot materially change the current decision, responsibility, architecture, verification or strategic commitment.

### 8.4 Feedback into comparison

If consequence analysis changes the judgment, return to comparative evaluation.

Possible results:

- `REAFFIRM`
- `REVISE_PREFERENCE`
- `REOPEN_ALTERNATIVES`
- `INVESTIGATE`
- `DEFER`
- `NO_CHANGE`
- `OWNER_DECISION_REQUIRED`
- `THESIS_REVIEW_REQUIRED`

These are proposed conceptual consequences of the analysis, not a new universal runtime enum.

Only existing governing decision processes may establish the corresponding authoritative strategic disposition.

### 8.5 Decision and implementation handoff

When a real strategic decision is warranted, use the current Level-3 process.

Preserve:

- The preferred or selected path.
- Why it was selected.
- Which alternatives were declined and why.
- Governing commitments.
- Material assumptions.
- The smallest warranted repository responsibility.
- Implementation authority.
- What evidence should cause reconsideration.

A strategically sound direction may still end in `NO_CHANGE`, `INVESTIGATE` or `OWNER_DECISION`.

### 8.6 Implementation feedback

After material construction work:

1. Inspect which capabilities or architectural relationships actually changed.
2. Compare observed outcomes with prospective claims.
3. Confirm, revise, contest or supersede consequential hypotheses.
4. Reassess affected ProductPossibilities and future capability states.
5. Preserve the original prediction and its historical context.
6. Update strategic continuity only when the new evidence warrants it.
7. Retain genuinely new possibilities when useful.

This completes the connection between prospective reasoning and persistent semantic stewardship.

---

## 9. End-to-End Reference Case

Use an existing repository possibility rather than an invented generic example.

**Candidate:** `poss:target-repository-discovery-memory`

This possibility is already recorded in the Idea Library, but its realization has not been established.

### 9.1 Problem

A coding agent explores a target repository, compares several candidate engineering responsibilities, selects one and executes it.

A later agent may lose the meaningful unselected alternatives and the assumptions that distinguished them.

### 9.2 Strategic question

Should Sensemaking preserve the compared candidate set across sessions in addition to the selected next responsibility?

What future capabilities would doing so unlock?

### 9.3 Architectural synthesis

Generate materially different options.

**Architecture A: Repository-local reviewed knowledge**

- Retain consequential candidate possibilities in source-controlled records.
- Preserve stable identity, rationale, relationships and epistemic status.
- Reuse the existing knowledge index when available.
- Avoid importing another repository's records without authority.

**Architecture B: Extended session receipt**

- Preserve considered alternatives and reasons inside a session receipt.
- Minimize additional storage concepts.
- Investigate whether later sessions can retrieve and reconcile the information without excessive reconstruction.

**Architecture C: Read-only projection from existing strategic artifacts**

- Reuse already-recorded analysis and path history.
- Avoid additional authored records.
- Investigate which alternatives would be lost because they never entered a formal strategic analysis.

C is a legitimate counterfactual architecture option for comparison, even if earlier Idea Library work found a related approach insufficient.

### 9.4 Strategic evolution analysis

Compare coherent trajectories such as:

- Incrementally extend repository-local possibility records and relevant Skill guidance.
- Extend existing receipt/continuity contracts first, then decide if persistent semantic records are needed.
- Retain current behavior until a concrete discovery responsibility demonstrates material loss.

These are construction trajectories, not automatic implementation tasks.

### 9.5 Post-convergence depth exploration

Suppose Architecture A is provisionally preferred.

Explore conditional consequences:

- Later agents might recover previously considered opportunities.
- Persistent records might reduce repeated exploration.
- Better historical recall might reveal new combinations of capabilities.
- Repository-local state might increase maintenance burden.
- Poorly scoped evidence references might cause excessive reconciliation.
- Portable behavior might require clear target-repository authority and currentness semantics.
- The persistence model might become useful for architectural alternatives and strategic decisions beyond the original discovery use case.

The last point may generate a **new ProductPossibility**: repository-local prospective decision memory, broader than storing only discovery candidates.

That new idea should be linked to the consequence that motivated it.

It is not automatically selected.

### 9.6 Evaluation feedback

Recompare A, B and C using the consequences.

If A remains preferred, preserve why. If a new constraint changes the answer, revise the preference.

If the correct decision remains uncertain, preserve the uncertainty rather than invent a commitment.

### 9.7 Demonstration deliverable

Produce a source-grounded reference set containing:

- One original ProductPossibility.
- At least two real architectural alternatives.
- Material target-structure differences.
- Coherent strategic paths where warranted.
- A qualitative comparison.
- A provisional preference or justified non-selection.
- Conditional consequence hypotheses.
- At least one new or revised possibility if genuine synthesis warrants it.
- Reconsideration conditions.
- A reconstructible history of the reasoning.

This case is the bridge between conceptual ontology and executable schemas.

---

## 10. Incremental Implementation Roadmap

### PR A — Shared Prospective Reasoning Ontology

**Purpose:** Establish the conceptual model and its relationship to the existing six layers.

**Work:**

1. Create `docs/semantic-architecture/prospective-reasoning-ontology.md`.
2. Define operation, domain, direction and scope as independent dimensions.
3. Add bounded architectural, strategic and consequence specializations.
4. Define identity and provenance for proposed versus observed entities.
5. Add the proposed relationship dictionary and endpoint rules.
6. Extend `ontology.md`, `relations-and-epistemics.md` and competency questions.
7. Document authority and currentness boundaries.
8. Cross-link the Product Possibility Ontology.
9. Include examples showing that one ArchitectureOption survives multiple reasoning operations.

**Acceptance:** The model distinguishes what the agent does from what it produces, without creating a new runtime or overriding existing architectural semantics.

### PR B — Source-Grounded Reference Case and Vocabulary Fit

**Purpose:** Demonstrate where the ontology helps a real reasoning responsibility.

**Work:**

1. Use `poss:target-repository-discovery-memory` as the initial case.
2. Inspect existing source, contracts and recorded decisions.
3. Generate architectural alternatives and strategic paths.
4. Trace material conditional consequences.
5. Record an attributed qualitative comparison.
6. Attempt to represent all important relationships with existing types.
7. Mark each competency question expressible, awkward or not expressible.
8. Identify exactly which distinctions require executable formalization.

**Acceptance:** The reference case is coherent, source-grounded and reconstructible. Any proposed schema expansion identifies a specific semantic loss.

### PR C — Persistent Prospective Knowledge Slice

**Purpose:** Preserve consequential synthesis results using the existing knowledge substrate.

**Work:**

1. Create a reviewed `.sensemaking/knowledge/` record set for the reference case.
2. Reuse existing kinds and relations where semantically appropriate.
3. Record provisional architecture options and consequence hypotheses without claiming implementation.
4. Preserve source references, assumptions and decision provenance.
5. Link new possibilities to their synthesis origins.
6. Run existing `search`, `explain`, `why`, `history`, `changes` and applicable impact queries.
7. Record what later retrieval can and cannot reconstruct.

**Acceptance:** Existing queries recover the core prospective relationships. Any information lost through generic attributes is explicitly documented, not concealed.

### PR D — Architectural Synthesis Executable Contract

**Purpose:** Make multi-option architectural synthesis a durable, inspectable artifact.

**Work:**

1. Add the bounded `architectural_synthesis` artifact contract.
2. Create its authoring template.
3. Implement focused structural validation.
4. Define references to current architecture, ProductPossibilities, options, proposed transitions and assumptions.
5. Support qualitative comparison and a genuinely provisional preference.
6. Support no-selection outcomes.
7. Preserve compatibility with the existing `architectural-review` input/output contract.
8. Exercise the contract through the reference case.

**Acceptance:** The artifact can faithfully preserve materially different architectural alternatives and their provenance without creating implementation authority.

### PR E — Strategic Evolution Schema Integration

**Purpose:** Link architectural synthesis to the existing Level-3 strategic decision surface.

**Work:**

1. Extend the existing strategic-analysis contract only with justified optional references.
2. Reuse v2 construction paths and comparison fields.
3. Link a strategic path to relevant product possibilities and architecture options.
4. Preserve the distinction between a candidate future, a proposed architecture and an authorized strategic disposition.
5. Keep optional analysis links valid when no architectural synthesis is warranted.
6. Update the strategy artifact template, validator and read-only projections only where a concrete consumer needs the new references.
7. Preserve historical artifact validity and `BUILD`/`NO_CHANGE`/`INVESTIGATE` semantics.

**Acceptance:** A Level-3 analysis can reconstruct the architectural basis of its compared construction paths without requiring a new strategic planner or a second canonical strategic-analysis artifact.

### PR F — Consequence Depth and Feedback Schema

**Purpose:** Preserve conditional future implications and connect them back to comparison.

**Work:**

1. Define the minimum typed consequence representation required by the reference case.
2. Separate prospective consequences from observed change impacts.
3. Represent material direct and downstream effects with explicit assumptions.
4. Support enabling and constraining consequences.
5. Represent connections to newly generated ProductPossibilities.
6. Add an optional post-convergence consequence assessment.
7. Determine whether an existing artifact section is sufficient or a standalone `prospective_consequence_assessment` is warranted.
8. Define a feedback outcome that can reaffirm or reopen a provisional preference.
9. Preserve non-automatic Level-3 and Level-4 boundaries.

**Acceptance:** An agent can explain why a predicted consequence matters to a strategic comparison, challenge its assumptions and preserve the result without claiming causal certainty.

### PR G — Reasoning Integration and Knowledge Reconciliation

**Purpose:** Connect the new representation to the existing Skills.

**Work:**

1. Update relevant architecture-exploration guidance to retrieve existing possibilities and produce coherent architectural alternatives.
2. Update `strategic-repository-analysis` to consult architecture synthesis only when decision-relevant.
3. Preserve its existing Strategicity Gate, breadth/depth discipline and path-selection semantics.
4. Add optional post-convergence consequence reasoning, with an explicit stop rule.
5. Update `architectural-review` guidance only where the new artifact improves its bounded proposal evaluation.
6. Extend Repository Semantic Steward reconciliation guidance for prospective hypotheses, changed architectural options and newly generated possibilities.
7. Preserve normal lightweight operation for clear local coding tasks.
8. Avoid adding new Skills or mandatory modes without an independent consumer need.

**Acceptance:** Relevant existing agent workflows can use the new semantic records naturally, while unrelated implementation work remains unaffected.

### PR H — Construction-First End-to-End Use

**Purpose:** Exercise the full pre-implementation loop in a genuine engineering responsibility.

**Work:**

1. Select a real source-grounded product or architectural decision within the approved repository scope.
2. Recover relevant historical ProductPossibilities and architecture knowledge.
3. Produce distinct architectural alternatives.
4. Build coherent strategic paths if the decision is Level-3 material.
5. Compare alternatives and record the initial rationale.
6. Perform consequence depth where it could change that rationale.
7. Reconsider or reaffirm the preferred direction.
8. Implement one bounded responsibility if warranted and authorized.
9. Reconcile actual construction evidence with previous prospective claims.
10. Preserve useful new possibilities, revised assumptions and rejected alternatives.

**Acceptance:** The loop changes or meaningfully informs a real engineering decision and produces retained product value, not merely a collection of mechanically valid artifacts.

### PR I — Conditional Semantic Schema and Query Specialization

**Purpose:** Resolve meaningful representational limitations exposed by actual use.

This PR is conditional and may be skipped or divided into smaller increments.

Potential work:

- Add a dedicated ArchitectureOption claim type.
- Add prospective realization or consequence predicates.
- Add query support for relevant options, their conditional effects and derived possibilities.
- Add source-aware consequence retrieval.
- Add authored schema versioning only when necessary.
- Add compatibility and migration handling.
- Preserve the existing SQLite rebuildability and historical knowledge format.

**Acceptance:** Every new executable type or query resolves a specific unanswered competency question. The change does not become a generic causal reasoning engine.

### PR J — Portable Target-Repository Application

**Purpose:** Extend the completed capability beyond Sensemaking Skills itself.

Once the local loop is coherent:

1. Select one explicitly authorized target repository.
2. Use the portable Skill to inspect its actual product ontology.
3. Recover or author a small relevant possibility landscape.
4. Perform a real architectural or strategic synthesis.
5. Retain consequential options, reasoning and conditional consequences in that repository's authorized knowledge surface.
6. Revisit them in a later independent session when practical.
7. Reconcile only the evidence actually observed.

**Acceptance:** The portable workflow can improve continuity in a different product domain without importing another repository's authority, requiring a shared external database or declaring S6 fully proven.

---

## 11. Program Dependencies

Recommended order:

1. **PR A + PR B:** Conceptual model and first real reference case.
2. **PR C:** Reviewed prospective knowledge using existing vocabulary.
3. **PR D:** Architectural synthesis artifact and validator.
4. **PR E:** Strategic-analysis integration.
5. **PR F:** Conditional consequences and feedback.
6. **PR G:** Integration into existing reasoning guidance.
7. **PR H:** Real construction and knowledge reconciliation.
8. **PR I:** Specialized predicates or queries, only where their need is demonstrated.
9. **PR J:** Portable target-repository use.

PR H should not be blocked solely because PR I has not happened. A coherent source-grounded reversible implementation can provide more value than another round of abstract schema design.

Likewise, not every activity requires a separate PR if tightly related changes form one reviewable and useful increment.

The program should stop or redirect if a proposed increment adds documentation or graph complexity without improving an actual reasoning capability.

---

## 12. Verification and Acceptance Strategy

### 12.1 Representation acceptance

Verify that:

- Entity identities are stable.
- Relationship endpoints match their conceptual contracts.
- Current, proposed and observed architecture are distinguishable.
- Conditional consequences cannot masquerade as established impacts.
- Provisional preferences cannot masquerade as ratified decisions.
- Historical reasons remain accessible.
- Source identity and currentness are preserved.
- No new artifact grants authority by existing.

### 12.2 Retrieval acceptance

A fresh query should be able to recover:

- The ProductPossibility motivating an architecture option.
- The architectures that were considered.
- The meaningful structural differences between them.
- The strategic construction paths connected to those options.
- The predicted consequences and their assumptions.
- The reasons for a provisional or selected preference.
- New possibilities derived from consequence exploration.
- The evidence that could reopen a previous comparison.

A syntactically valid response that omits the distinction between predicted and observed consequences does not satisfy semantic acceptance.

### 12.3 Reasoning-use acceptance

In one real decision, the agent should be able to demonstrate at least one of the following:

- A retrieved historical alternative prevents redundant discovery.
- An architectural synthesis exposes a previously hidden tradeoff.
- A future capability dependency changes a strategic path comparison.
- Post-convergence consequence reasoning changes a provisional preference.
- A conditional consequence produces a useful new ProductPossibility.
- Recovered rationale supports a well-grounded `NO_CHANGE`.
- A retained assumption helps the agent select a better-scoped implementation responsibility.

It need not achieve all of these in one session.

### 12.4 Longitudinal acceptance

In a later genuinely separate session, observe whether an agent can correctly recover and apply consequential prior reasoning.

Keep the claim levels separate:

1. **Representation established:** records and contracts exist.
2. **Retrieval demonstrated:** queries recover the intended records.
3. **Local reasoning value observed:** a genuine decision uses the recovered knowledge.
4. **Cross-session value observed:** a separate session reuses or revises the knowledge correctly.
5. **Longitudinal benefit supported:** repeated normal use justifies broader product-value claims.

Do not claim levels 4 or 5 solely from passing CI or a same-session walkthrough.

### 12.5 Verification economy

Follow the repository's construction-first policy:

- Run the relevant artifact and knowledge validators.
- Inspect consequential diffs and generated records.
- Use source-grounded, finding-specific checks.
- Let existing hosted CI run.
- Do not create broad synthetic research gates or wait for unrelated unit-test cycles before authorized construction.
- Do not ignore known material defects or enforced branch protections.
- Report checks not run.
- Reconcile after a genuine implementation or reasoning consequence, not after every trivial edit.

---

## 13. Risks and Design Responses

| Risk | Response |
|---|---|
| Overly abstract reasoning ontology | Start from a real ProductPossibility and practical competency questions |
| Duplicated concept hierarchies | Reuse existing six-layer ontology and ProductPossibility |
| Every reasoning act becomes a graph node | Retain only consequential, reusable conclusions |
| False causal certainty | Represent conditional effects as hypotheses with assumptions |
| Overloaded `references` predicates | Test fidelity and specialize only where important meaning is lost |
| Two authoritative strategic-analysis artifacts | Extend `strategic_repository_analysis` instead of replacing it |
| Architectural Review accidentally becomes strategy selection | Preserve its proposal-evaluation responsibility |
| Provisional preferences treated as final choices | Separate preference, selection and action authority |
| Depth exploration never terminates | Stop when further consequences cannot change the relevant decision |
| Depth exploration only considers risks | Model enabling consequences, new possibilities and opportunity costs too |
| Graph topology used to rank ideas automatically | Preserve qualitative agent comparison and ADR 0029 boundaries |
| History rewritten after implementation | Append assessments and retain earlier assumptions |
| Source-reference changes cause excessive reconciliation | Cite true origins and material evidence, not every related document |
| Self-referential ontology construction dominates the roadmap | Move to real architectural/product decisions once the minimum coherent model exists |
| Cross-repository knowledge leaks authority | Keep target-repository identities, permissions and provenance explicit |

---

## 14. Program Decision and Governance

### Recommended owner-level direction

Within the existing Persistent Semantic Stewardship thesis, select:

**Prospective Reasoning Ontology & Pre-Implementation Synthesis v1**

as a bounded product-development program.

The program expands persistent semantic knowledge into architecture alternatives, strategic trajectories, comparative judgments and conditional consequences.

It does not replace ADR 0031, ratify proposed ADR 0033, or change ADR 0029's prohibition on automatic semantic control and protected operations.

### Repository integration

Use the repository's established construction policy for ordinary implementation decisions and PR merges.

Each PR should have a source-grounded decision note describing its intended product value, actual change, relevant alternatives, evidence ceiling and known uncertainty.

Do not wait for routine owner approval between already-authorized, bounded implementation increments, but preserve all applicable external, schema-governance, Level-4 and branch-protection boundaries.

### Documentation placement

Store the program plan under:

`docs/superpowers/plans/2026-10-28-prospective-reasoning-ontology-and-synthesis.md`

Link it from the relevant semantic-architecture index and product-development context.

Keep the new ontology canonical in `docs/semantic-architecture/`, not in the plan file itself.

The plan describes construction; the ontology describes concepts; the artifact contracts describe executable structure; the Skill guidance describes agent reasoning responsibilities; reviewed knowledge preserves consequential source-bound instances.

---

## 15. Final Completion Criteria

The initial program is construction-complete when the repository can support this behavior:

**Given a real ProductPossibility, an agent can retrieve historical context, synthesize materially distinct architectural options, connect them to coherent strategic paths, compare them, investigate conditional consequences of a provisional preference, reconsider the preference if warranted, and preserve the resulting reasoning for future use—all before any implementation is required.**

When implementation does occur, the agent can reconcile what actually happened with its earlier predictions.

The loop does not require every phase on every task, does not require a new idea at every stage, and does not automatically convert reasoning into authority.

### Selected first increment

**Begin with PR A and the smallest useful part of PR B.**

Define the common ontology and competency questions, then immediately apply them to `poss:target-repository-discovery-memory` to find the meaningful schema gaps.

Continue into actual artifact and knowledge construction rather than repeatedly refining the taxonomy without consumers.

### Guiding architectural principle

**A durable product-reasoning system should preserve not only possible futures, but the structures that might realize them, the consequences that could follow, the reasons for preferring one direction, and the new futures that become imaginable because of those choices.**

That is the intended bridge from the Idea Library to genuinely cumulative architectural and strategic intelligence.
