# Connected Prospective Inquiry Ontology v1

**Status:** Level-2 conceptual / documentary extension, implemented in source guidance on 2026-11-05. This is not an executable schema, artifact contract, graph-reasoning engine, phase controller, or new decision authority.  
**Assessed source baseline:** `ThorStarlord/sensemaking-skills@d8c0f4de30e989a5e99501942bf9167148bd16a3` (planning PR #748 merged); confirm current source and original case revisions whenever applying it elsewhere.  
**Governing authority:** [ADR 0029](../adr/0029-current-product-boundary.md), [ADR 0031](../adr/0031-persistent-semantic-stewardship.md), [ADR 0034](../adr/0034-ontology-first-adaptive-sensemaking.md), current owner intent, and the active agent's actually delegated authority.  
**Foundation:** [Layered ontology](ontology.md), [Prospective Reasoning](prospective-reasoning-ontology.md), [Possibility Assessment](possibility-assessment-ontology.md), [Convergent Direction Selection](convergent-direction-selection-ontology.md), [Divergent Exploration](divergent-exploration-ontology.md), [relations and epistemics](relations-and-epistemics.md).  
**Evidence:** [source cases](connected-prospective-inquiry-reference-cases-v1.md), [local competencies and source review](connected-prospective-inquiry-competency-v1.md), [portable agent guide](../../skills/strategic-repository-analysis/references/connected-prospective-inquiry-v1.md).  
**Design basis:** [2026-11-05 specification](../superpowers/specs/2026-11-05-connected-prospective-inquiry-ontologies-design.md).

## 1. Purpose: four questions, one source-preserving reasoning system

A prospective inquiry often carries the *same* source-grounded possibility, premise, assessment or architecture through several differently motivated reasoning activities. Each changes **what the agent knows or judges**, not necessarily what the product is or who has authority.

| Conditional reasoning profile | Key question | Documentary result | What it does not do |
| --- | --- | --- | --- |
| **Focused Depth Exploration** | If this premise or possibility held, what effects, interactions and new options might follow? | A bounded **ConsequenceStructure**: mechanisms, conditional chains, alternatives, beneficiaries, limits, stop | Establish causality from prose, mint a selected ProductPossibility or mandate next-stage inquiry |
| **Convergent Reassessment** | Do those consequences or other new grounds change an identifiable earlier evaluation? | Dated **AssessmentRevisionAccount**: previous frame, new grounds, changed/unchanged judgments, limits | Rewrite a historical portfolio, rerank unrelated members, or ratify strategy |
| **Adversarial Review** | What specific premise, inference, comparison or proposed design could fail, and how is the challenge addressed? | **ChallengeResponseAccount**: precise target, grounded challenge, response, unresolved issue | Treat every fear as observed defect, confer veto power or verify a proposed repair |
| **Architecture Synthesis** | Which coherent proposed product-and-technical design would serve the authorized goal under the available consequences and challenges? | **DesignRationaleView**: outcome/requirements -> proposed design elements/contracts, tradeoffs, open decisions | Replace the `architectural_synthesis` contract, create a second PRD producer, authorize implementation |

**These are reasoning responsibilities, not four obligatory lifecycle stages.** An inquiry may move from a challenge to depth, from synthesis to reassessment, from consequences to more divergence, or stop after one warranted question. A legitimate answer can be no meaningful further consequence, unchanged judgment, unsustained objection or no coherent design.

This vocabulary is a *semantic formalization Level 2*. The product's **control Level 2** (bounded responsibility/Campaign) is a different taxonomy. Do not identify them by their number.

## 2. Shared frame, identities and epistemic boundaries

### 2.1 A shared assessment envelope, only where consequential

Use the containing report/PR/ADR/receipt instead of requiring a new universal artifact. State once per record, where material:

- **Question and activity:** why this inquiry is being done now, which profile(s) are actually used, and where it stops.
- **Actor and date:** actual author, attributable judgment/decision, current scope of delegation; *not* inferred owner approval.
- **Original typed target:** original `InquiryQuestion` plus proposed method, `CandidateExpression`, `poss:`, `arch:`, `conseq:`, ConstructionPath, `AssessmentJudgment`, observed RepositoryElement, design, requirement or concrete work claim.
- **Source identities and currentness:** full source paths, original IDs, assessed code/target revision, governing revision, relevant prior dated judgment and later findings. Do not replace an older report's assessed source with the revision of the current report.
- **Relevant purpose:** beneficiary, intended improvement, comparison frame, time/context horizon, applicable requirements, constraints and non-goals.
- **Grounds:** observed evidence, owner intent, explicit assumptions, hypothetical mechanisms, counterevidence and unknowns, separately labeled.
- **Effect and limit:** what judgment, choice, design or next question could change, what remains unassessed or out of frame, and when more reasoning would no longer change the decision.

A short paragraph is sufficient for low-stakes work; unknown is better than an invented field value.

### 2.2 Persistent entities versus transient activities and views

**Activity labels** follow [Prospective Reasoning section 2](prospective-reasoning-ontology.md#2-what-the-agent-does-three-independent-descriptors-of-a-reasoning-activity): `EXPLORE`, `SYNTHESIZE`, `EVALUATE`, `SELECT`, `RECONCILE`, crossed with domain and divergent/convergent breadth/depth. A profile can exercise more than one operation.

**Entities** retain their original identities across those activities:

- `ProductPossibility` is a potential desirable future, not an analysis heading, a proposed architecture, an action or an adopted goal.
- `ArchitectureOption` and `ConstructionPath` are proposed realizations/trajectories with their existing endpoints; they do not become observed components.
- `ConsequenceHypothesis` is an attributed conditional predicted effect, usually from an architecture option or path; source-local `conseq:` identities keep their existing meaning and contract.
- `ComparativeJudgment`, `ProvisionalPreference`, `AssessmentJudgment`, `PortfolioSnapshot` and `AssessmentRevisionAccount` are different judgments/views; a later preference does not erase the earlier one.
- `Decision` is a sourced actor's choice within actual authority. A recommended, evaluated or preferred direction is not automatically selected, executed or verified.
- `ConsequenceStructure`, `ChallengeResponseAccount` and `DesignRationaleView` below are **documentary roles** of a report/section, not new graph kinds, mandatory artifact identifiers or universal objects.

A local `D1` or `C1` inside a report is identified by its containing artifact, revision and source-local ID. A navigational group is not `sameAs`. If a prose depth exploration concerns a *general premise* rather than an option/path, it may use a source-local conditional-effect label; **do not assign `conseq:` or an `ArchitectureOption mayProduce` edge unless their existing ontology endpoints actually apply**.

### 2.3 Epistemic classification is more precise than confidence wording

| Status of statement | Appropriate claim | Inappropriate promotion |
| --- | --- | --- |
| **OBSERVED** source fact or behavior | A cited document, code boundary or executed result states/shows X at revision R. | X will occur in all products or later runs. |
| **DERIVED** conditional logic | If stated assumptions hold, conclusion follows by an explained inference. | The assumptions are observed true. |
| **INFERRED** interpretive relationship | On these cited grounds, this alternative likely constrains that ability. | The repository implements a formal dependency. |
| **HYPOTHESIZED** causal or future effect | If mechanism and context hold, X *may* cause/enable/constrain Y. | X causes Y, or Y is an observed user outcome. |
| **PROPOSED** creative opportunity/design | This could become a new product end or design component. | It is curated, approved, implemented, demanded or verified. |
| **EVALUATED** preference/judgment | Under frame F, A is comparatively stronger, possibly conditionally. | Owner/Level-3/Level-4 selection, implementation authorization. |
| **RATIFIED / ACTUALLY DECIDED** | An identifiable actor/source adopted this defined scope. | Unrelated side effect or future construction is authorized. |

Use the existing [canonical epistemic statuses](relations-and-epistemics.md#epistemic-statuses) when authoring actual claims. Terms like "proposed" and "evaluated" in this table qualify *activity/outcome*, and **do not add machine-readable epistemic enum values**.

**Conditional relation chains do not prove distant conclusions:** `A mayProduce B` + `B mayEnable C` does not entail `A will cause C`. Temporal sequence is not causation; common premises are not causal links. Observing a requirement or design proposal is not observing its product benefit. A valid graph link means that a proposition was retained with some attribution, not that it is true or currently applicable.

## 3. Conceptual relationship crosswalk (documentary only)

These verbs help humans follow the four kinds of accounts. They are **not executable predicates**, do not widen the existing `arch:`/path relation endpoints, and do not introduce inferential closure:

| Source role | Documentary relation | Target role | Required meaning and limit |
| --- | --- | --- | --- |
| ConsequenceStructure | `examines` | One typed target/premise | State source, context, beneficiary and actual question; no generic identity conversion. |
| ConsequenceStructure | `describesEffect` | Conditional statement or existing ConsequenceHypothesis | Separate direct vs systemic, assumptions, possible mechanism and contrary branch. |
| Conditional statement | `dependsOnPremise` | Source/assumption | State what fails if the premise is absent; not an executable dependency. |
| Conditional statement | `couldChange` | Named judgment, constraint, question or opportunity | Explain decision relevance, not selection. |
| AssessmentRevisionAccount | `reconsiders` | Dated predecessor judgment/snapshot | Preserve earlier meaning/IDs and declared purpose. |
| AssessmentRevisionAccount | `becauseOf` | New evidence/consequence/changed criterion | Say why the new information changes the old frame, or why it does not. |
| ChallengeResponseAccount | `targets` | Exact claim/inference/design element | Exact quoted or source-local target, overlap in scope/currentness and actual failure mechanism. |
| ChallengeResponseAccount | `answersWith` | Source-grounded rebuttal, revision, inquiry or unresolved risk | State whether response truly addresses the original challenge; no automated veto. |
| DesignRationaleView | `isMotivatedBy` | Intended outcome, requirement or consequential constraint | A proposed design element has a stated goal and supporting rationale, not proved efficacy. |
| DesignRationaleView | `addressesOrDiscloses` | Previous challenge/tradeoff | Distinguish resolved in proposed design, accepted risk and unassessed uncertainty. |

**Existing conceptual prospective relations are not replaced.** `ArchitectureOption | ConstructionPath mayProduce ConsequenceHypothesis`; `ConsequenceHypothesis mayEnable ProductPossibility`, `mayConstrain`, and `challenges Assumption | Hypothesis`; `ComparativeJudgment evaluates ArchitectureOption | ConstructionPath`; `ProvisionalPreference prefers ArchitectureOption | ConstructionPath`; `Decision selects` retain the endpoint constraints in [Layered Ontology](ontology.md#product-relations) and [Prospective Reasoning](prospective-reasoning-ontology.md#6-relationships). Broader literary examples do not extend those endpoints.

## 4. Focused Depth Exploration: consequence structure

**Unit of analysis:** one sourced premise/possibility/capability/option/relation, its beneficiary and context, plus the nearest prior interpretation. **Question:** What materially changes if this premise holds, and what fails if it does not?

A **ConsequenceStructure** contains only decision-relevant branches. A useful record separates:

1. **Baseline and direct effect.** What would change first, for whom, by what mechanism, compared with which current state?
2. **Propagation.** Each second-order link names its *own* enabling assumptions and mechanism. Distinguish necessary condition, plausible enabling circumstance and claimed causal effect.
3. **Systemic interaction.** When relevant, trace feedback, substitution, lock-in, maintenance burden, changes to future option space, side effects across affected actors or knowledge environments.
4. **Counterfactual forks.** Compare at least the forks that could reverse the decision: missing authority, unavailable evidence, absent consumer, differing beneficiaries or owner constraints. Do not force a branch count.
5. **Distribution and asymmetry.** A benefit for an agent/owner may create costs for another user, maintainer or downstream actor. Do not collapse distinct beneficiaries into one "value".
6. **Opportunity and non-effect.** Say whether a new end was imagined, a known end gained a new mechanism, or the chain supplied no distinct opportunity. A new question is not an owner-approved goal.
7. **Depth and stopping.** Stop where another link would not change purpose-relative evaluation, responsibility, constraints or strategy; stop earlier if an untestable premise makes deeper confidence unwarranted.

**Anchored example.** [Discovery Memory, 2026-10-28](../../artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md#7-consequence-exploration-post-convergence-of-the-provisional-preference) records `conseq:persistence-requires-write-authority`. The observed default read-only discovery mode means a repository-local retention proposal cannot fulfill its durable-value mechanism *in that mode*. The result is a **narrowed context of use**, not proof that the alternative is universally bad.

**Negative chain.** "A graph entry may surface X; X may inspire Y; therefore the graph causes a valuable new product goal Y" fails without agent-use evidence, independent source-only contrast, value grounds and both causal bridges. Record a plausible question and stopping condition, not a newly proved benefit.

## 5. Convergent Reassessment: change or reaffirm attributable judgment

**Unit:** a specific prior `AssessmentJudgment`/`PortfolioSnapshot`/`ProvisionalPreference`, sometimes an actual sourced `Decision`, under its original purpose and revision. This is not a command to run Convergent Evaluation again.

Use the existing **AssessmentRevisionAccount** to record:

- Previous author/date/target(s)/frame, criteria, ranking or nonranking, disputed/outside-frame members and exact source identity.
- New evidence, consequence, changed premise or owner intent **and the causal/evaluative connection to the old criterion**.
- New judgment **for the same question**, or explicit explanation that the question or beneficiary changed and therefore comparisons are not commensurate.
- Delta: `NO_CHANGE` with grounds, same preference with revised conditions, same order for new reasons, local pairwise change, incomparability, insufficient evidence, missing option set or appropriately sourced change in decision.
- Preserved history: untouched members, original report and alternatives; the later record links instead of overwriting.
- Re-entry trigger and permitted next inquiry or decision actor.

**Three priorities are non-interchangeable:** intellectual **exploration priority**, strategic **attractiveness of a future product**, and independently authorized **implementation priority**. Even a justified local change to the first does not establish the other two. A preference only becomes an actual scoped decision when the source names a selecting actor and valid authority, per [Convergent Selection](convergent-direction-selection-ontology.md).

**Anchored examples.**
- [Discovery Memory, section 8](../../artifacts/history/2026-10-28-discovery-memory-prospective-synthesis.md#8-provisional-preference-and-feedback-revise_preference-narrowed) retains the preferred architecture while narrowing it to sessions with knowledge-edit/commit authority.
- [Architectural Generativity, 2026-11-03](../explorations/2026-11-03-portfolio-reassessment-architectural-generativity.md) changes a bounded **pairwise inquiry priority**, not the historical global portfolio or product thesis.

**Negative outcome.** Reading another report on a familiar subject, without a new decision-relevant premise or effect, warrants `NO_CHANGE` or no additional account. An unaffected portfolio member is not demoted simply because two other questions were compared in depth.

## 6. Adversarial Review: an objection with a genuine target and response

**Unit:** a named proposition or intended consequence—an assumption, source claim, mechanism/inference, comparison criterion, requirement, architecture element, contract, authority assertion or closure statement.

A **ChallengeResponseAccount** is an attributable documentary group with five distinguishable parts:

1. **Target:** source-local proposition/identity, original context, revision, epistemic class and the scope the review actually covers.
2. **Challenge:** how the target could fail, with source counterevidence or an explicitly hypothetical failure case. Name the broken inference or conflicting requirement, not just a generic "risk".
3. **Impact:** which conclusion, beneficiary, architecture contract, previous preference or authorization would change **if** the objection holds.
4. **Response:** concession and narrow correction; evidence-grounded rebuttal; prospective repair/alternative; bounded inquiry; knowingly retained risk; or unresolved issue. The response's grounds must answer the original challenge.
5. **Residual and return:** what remains uncertain, what new consequence the proposed response itself introduces, what requires real verification, what would reopen the underlying judgment.

A proposed design repair is *not* observed closure. A credible hypothetical threat is *not* an established defect. A critic's objection is evidence for active-agent interpretation, never an automatic veto, new priority, or authorization to change another actor's decision.

When the work is a review of an already proposed architecture, the existing [`architectural-review` Skill](../../skills/architectural-review/SKILL.md) retains its input of a current `repository_sensemaking_brief` and an explicit `proposed_direction`. This documentary profile does not relax it or create a competing review Skill.

**Anchored example.** [Graph Activation, 2026-11-01](../../artifacts/history/2026-11-01-graph-activation-architectural-synthesis.md#4-architecture-options-same-comparison-level-graph-activation-mechanisms) retains a runtime-forced graph-context option as a *declined counterfactual* under authority and maintenance concerns. This is a reasoned comparative challenge, not observed runtime failure. The same source says `installed != loaded != invoked != applied`.

**Negative outcomes.** An imaginary downstream outage cannot be recorded as an actual observed defect. A code patch offered to answer "does this knowledge source improve independent creative judgments?" is a possible intervention, not evidence proving the claim.

## 7. Architecture Synthesis: proposed coherence with product-and-technical traceability

**Unit:** a proposed solution to an authorized **product/problem goal**, informed by compared options, conditional consequences and substantive challenges.

A **DesignRationaleView** is a traceable account, not a selected `ArchitectureOption` class or executable schema. Minimum connections where relevant:

| View | Question | Distinct proper home |
| --- | --- | --- |
| Beneficiary / desired outcome | Whose better experience, product result or capability is intended? | User intent, product evidence, opportunity/hypothesis, current governing strategy |
| Requirements and acceptance | What behaviors, scope, constraints, non-goals and proposed success criteria follow? | **`to-prd`** produces canonical `prd` when product specification is warranted |
| Compared architectural realizations | Which genuine option-level alternatives and conditional consequences were considered? | Existing **`architectural_synthesis`** and its multi-option comparison; preference remains provisional |
| Proposed technical design | Which responsibilities, components, interfaces, contract changes, information paths, dependencies and reversibility form one coherent proposal? | Repository-native technical spec/design explanation, not a new registered `architecture_spec` |
| Challenge reconciliation | Which risks, contrary sources, unmodeled consumers and review objections were addressed, accepted or remain open? | Source-linked review and rationale; a revision may return to Depth Exploration |
| Downstream authorization | What actor, decision and separate responsibility would allow construction? | Accepted owner/agent delegation, governing decisions, a later bounded plan |

For each consequential proposed design element, state **goal/requirement -> structural responsibility -> interface/interaction -> expected consequence -> evidence/assumption -> challenge/risk**. Check coherent ownership, contract boundaries, incompatible dependencies, option tradeoffs and explicit non-goals. A component name is not a demonstrated capability. Competing objectives do not become consistent because they appear in one drawing.

**Avoid competing producers.** The existing `architectural_synthesis` artifact continues to require genuine alternative options and may express a `PROVISIONAL` preference or none; it does not designate an adopted architecture. The `to-prd` Skill remains the single PRD capability and its `source_intent_ref` and scope-expansion approval fields are unchanged. The design proposal can link these **existing** artifacts or be one appropriately bounded prose document; it does not require fabricating an artifact because another phase is notionally "complete".

**Negative design case.** A technically detailed graph-injection runtime spec with no product beneficiary, contractual consumer or authority to impose it is not an authorized coherent solution. If an option is merely preferred in an `architectural_synthesis`, presenting it as "approved final architecture" is a factual authority error. Even a well-grounded, internally consistent PRD/design is **not** implemented code.

## 8. Feedback, stop and source preservation

A possible substantive feedback pattern—not a workflow:

```text
sourced premise / proposed direction
  -> conditional consequence
  -> targeted prior-judgment reconsideration (or reasoned NO_CHANGE)
  -> targeted challenge + response (or unresolved concern)
  -> coherent proposed design (if warranted)
  -> newly exposed consequence or evidence need
  -> active agent decides whether another bounded responsibility is justified
```

Individual profiles may run independently or in any order. If a new alternative changes the question, return to divergence; if a supposed cause lacks an observable mechanism, stop deeper inference; if a relevant owner's selection is absent, retain a proposal or stop at the actual boundary. No artifact here launches a Skill, changes a portfolio rank, repairs a defect, opens an issue or grants merge/release authority.

**Historical preservation:** retain original candidate IDs, attributed perspectives, prior judged conditions, rejected or deferred options, source/assessed revision, unaffected members and scope-limited corrections. A newer record is not a replacement for the truth of an earlier historical judgment.

**Retention:** use ordinary dated reports, ADRs, existing `architectural_synthesis`, PRDs, strategic artifacts and case-linked source documents first. Selective `schema_version: 1` reviewed knowledge under `.sensemaking/knowledge/` is optional *only if* a real retrieval/re-entry question is not well served by current material and the existing supported kinds/predicates can express it without false authority. The existing knowledge schema cannot be extended by a diagram or vocabulary request.

## 9. Competency, negative-case and claim ceiling

The [sixteen local CPI-CQ questions](connected-prospective-inquiry-competency-v1.md) have source-specific answers and negative controls: broken transitive chain; source-preserving local reassessment; hypothetical challenge versus observed defect; proposed design/PRD versus adopted architecture; authority-sensitive no-selection; warranted no further depth.

**What this implementation can establish:** descriptive source/contract fit; coherent Level-2 terms; reproducible documentary reconstruction from specific cases; repository reference reachability; installation/package presence when separately checked; source-grounded agent-facing guidance.

**What it cannot establish:** independent later-agent creativity, causal superiority over a source-only agent, improved ranking quality, downstream host loading/invocation/application, accepted new product goals, implemented design, or automatic graph-based semantic inference. Those require separate warranted evidence and the correct authority. In particular, `installed != loaded != invoked != applied`.

**Stopping condition for this ontology increment:** the shared model, four distinct profiles, local competency answers, optional installed reference and preservation of current contracts/authority are reconstructible without creating new executable semantics.
