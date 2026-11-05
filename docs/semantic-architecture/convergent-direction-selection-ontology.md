# Convergent Evaluation and Direction Selection Ontology v1

**Status:** conceptual Level-2 extension and documentary selection profile; introduced 2026-11-04. No new executable schema, control phase, machine predicate or authority.
**Planning baseline:** `ThorStarlord/sensemaking-skills@ad223927e533268b2867d07851f1993860ace647`.
**Governing authority:** accepted [ADR 0029](../adr/0029-current-product-boundary.md), [ADR 0031](../adr/0031-persistent-semantic-stewardship.md), [ADR 0034](../adr/0034-ontology-first-adaptive-sensemaking.md), and the active agent's bounded delegated decision authority. The ontology itself authorizes nothing.
**Builds on:** [Possibility Assessment](possibility-assessment-ontology.md), [Divergent Exploration](divergent-exploration-ontology.md), [Product Possibility](product-possibility-ontology.md), [Prospective Reasoning](prospective-reasoning-ontology.md), and the [Warrant / Choice Policy](../../skills/using-sensemaking/references/warrant-choice-policy-v0.md).
**Cases and competency questions:** [source-pinned cases](convergent-direction-selection-reference-cases-v1.md) and [local fit account](convergent-direction-selection-competency-v1.md).

## 1. Purpose and distinguishing gap

**Convergent Evaluation** asks which direction is justified *for a particular question and scope*, **if any**. It goes beyond explaining the differences among alternatives by interpreting what their comparison actually warrants, and beyond ranking by distinguishing a preferred suggestion from an enacted decision.

Three separate questions must survive:

1. **Candidate warrant:** Is pursuing this particular target justified at all under its actual prerequisites and available evidence?
2. **Comparative rationale:** Why does this warranted target serve the declared purpose better than credible alternatives, with what accepted consequences and unresolved premises?
3. **Scoped adoption:** Has an actual selecting actor adopted this target under authority that covers this specific choice, what does that adoption settle, and what remains open?

A candidate can be preferred to every visible alternative yet lack a decisive prerequisite. A source report can recommend the next inquiry without the owner adopting it. An owner-ratified product thesis differs from the same author's provisional next-question preference. A selected direction does not, by itself, authorize construction, publication, external side effects or protected operations.

This model complements the [AssessmentJudgment](possibility-assessment-ontology.md#2-shared-concepts-and-reference-roles) and [PortfolioSnapshot](possibility-assessment-ontology.md#2-shared-concepts-and-reference-roles) roles. It does **not** create another overall assessment process or a fourth authority level. `EVALUATE` and `SELECT` remain different operations under the [prospective ontology](prospective-reasoning-ontology.md#2-what-the-agent-does-three-independent-descriptors-of-a-reasoning-activity), not automatic consecutive stages.

## 2. Source-preserving concept roles

These are **documentary roles, not eight executable entity classes**. Existing `Claim`, `Assumption`, `Decision`, `AssessmentFrame`, `AssessmentTarget`, `ProvisionalPreference`, `ProductPossibility`, `ArchitectureOption` and `ConstructionPath` preserve their meanings and identifiers.

| Role | Documentary definition | Inheritance / hard non-identity |
| --- | --- | --- |
| **ChoiceQuestion** | What consequential choice must be resolved *now*, under which beneficiary, decision level, purpose, time horizon and possible commitment? | Reuses `InquiryQuestion` and `AssessmentFrame`; "what next?" alone is not a typed target. |
| **ConsideredChoiceSet** | The source-qualified, credible alternatives actually considered, with coverage sufficiency and known omissions. Include status quo/no change if materially plausible; overlap and incomparability survive. | A purpose-relative view of `PossibilityLandscape` or `PortfolioSnapshot`, **not** a forced shortlist, fixed option count or canonical merged identity. |
| **CandidateWarrant** | Attributed defeasible judgment about whether *one named target* is sufficiently supported to be contemplated: prerequisites, evidence, defeaters, constraints, currentness, consequences and needed authority. | Specializes an `AssessmentJudgment` using existing Warrant / Choice meanings. **Warranted != authorized or executed**. |
| **ConvergenceRationale** | Attributed reason that one *warranted* alternative better serves this particular choice than other credible candidates, with accepted tradeoffs, lost alternatives, contrary perspectives and conditional comparisons. | Reuses `AssessmentJudgment` and qualitative comparison, **not** numerical preference or a new `ProvisionalPreference` predicate. |
| **ScopedDirectionSelection** | The *role of an actual `Decision`* selecting an existing typed target, attributable to an actor with decision authority for a defined scope and date. It states what is settled, what is not, and what subsequent work may inherit. | Not a new target identity or selected `poss:`; a recommendation, portfolio rank, preference and pending owner decision do **not** instantiate it. |
| **AlternativeDispositionAccount** | Source-attributed interpretation of each material nonselected candidate: deferred, declined under this frame, complementary/retained, out-of-frame, superseded, defeated, or not assessed. | A decision-relative explanation, not global rejection, graph deletion or automated opportunity status. |
| **SelectionReconsiderationBoundary** | Conditions under which changes in evidence, critical prerequisites, owner intention, source revision or consequences could warrant reexamining this selection. | Reuses `AssessmentRevisionAccount` / reconciliation; change in a file is not automatic reversal or Level-3/4 reopening. |
| **SelectionHandoff** | Portable explanation for the next reader: actual choice and authority, accepted constraints, unresolved premises, excluded work, permissible subsequent reasoning and stopping boundary. | Uses existing PR, ADR, strategic-artifact, receipt or handoff surfaces. Not an implementation ticket, workflow dispatch or new mandatory artifact. |

A **DirectionSelectionRecord** is the optional readable representation of these roles; it is not a registered `artifact_id` or executable schema. A small, low-stakes choice can be expressed directly in prose if its consequential meanings survive.

## 3. Typed targets and decision scope

| Choice being considered | What can be selected | What does **not** follow |
| --- | --- | --- |
| **Further intellectual inquiry** | An `InquiryQuestion` **together with a `ProposedInquiryApproach`** (evidence source, method and availability) | Product-future adoption or permission to run an inaccessible experiment. |
| **Future product direction / Level-4 thesis** | A `ProductPossibility` or coherent strategic direction under adequate depth and the applicable strategic/owner ratification | Automatically ratified product identity, new ADR or implementation priority. |
| **Level-3 realization choice** | A source-backed `ArchitectureOption` or `ConstructionPath` inside the existing strategic processes | An authorized work order, deployment, autonomous merge or retrospective product-thesis change. |
| **Construction responsibility** | A bounded, independently **authorized** change, current repository responsibility or intervention | Permission inferred solely from a higher-scored possibility or graph retrieval. |

Target **type** and decision **scope** are not the same: choosing an inquiry for a bounded session is not a Level-4 selection even when the inquiry concerns future product identity. A direction may be comparatively attractive yet inappropriate for present construction.

### Core decision distinctions

- **Compared:** alternatives were considered; no direction need have been preferred.
- **Preferred/recommended:** an attributed judgment indicates a leading alternative; adoption, actor and authorization may be absent.
- **Actually selected:** an actor exercised their available authority and declared a scoped choice with a source. For owner-reserved product decisions, this requires a genuine owner ratification or governing decision—not an inferred preference.
- **Authorized to execute:** a separate decision/permission applies to that action, repository and side effect. It may follow an adopted direction but is not created by its existence.
- **Completed/verified:** actual work and evidence are separate facts.

Use the existing [Warrant / Choice dispositions](../../skills/using-sensemaking/references/warrant-choice-policy-v0.md#5-warrant-dispositions) and relevant strategic/owner procedures. In particular, `NO_SELECTION` is a legitimate *result*, not a "selected none" product entity. `OWNER_DECISION_REQUIRED`, `MORE_EVIDENCE_REQUIRED`, `EXPLORATION_REQUIRED`, `AUTHORITY_REQUIRED`, `CHALLENGE_REQUIRED` and `VERIFICATION_REQUIRED` describe different blockers; do not force a winner to populate a record. `OPTION_SET_INCOMPLETE` is an owner-capsule return condition, not a newly inferred universal runtime enum.

## 4. Relationship semantics without predicate expansion

These descriptions make prose readable; they are **not** new machine predicates or revisions of current relation endpoints.

| Subject | Conceptual relationship | Object | Grounding requirement |
| --- | --- | --- | --- |
| ChoiceQuestion | `frames` | ConsideredChoiceSet, target type and decision authority | State purpose, beneficiary, horizon and actor; know if an owner decision is reserved. |
| ConsideredChoiceSet | `retainsAlternative` | Existing source-qualified target | Document what was considered, excluded and why; no automatic merging. |
| CandidateWarrant | `checksPrerequisitesOf` | One typed target | Cite support, defeating evidence, uncertainties and authority; no inferred success. |
| ConvergenceRationale | `prefersWithinFrame` | Existing warranted targets | Explain consequences and relative tradeoffs; a preference is not yet `Decision`. |
| ScopedDirectionSelection | `selectsWithinScope` | Existing typed target | Actual deciding actor/source/date/authority and explicit scope; not a newly generated target identity. |
| ScopedDirectionSelection | `adoptsGrounds` | Warrant and rationale sources | Attribute acceptance; an actor may decide despite uncertain premises, but should make the uncertainty visible. |
| AlternativeDispositionAccount | `characterizesNonselected` | Original nonselected target(s) | Distinguish rejected-under-purpose, deferred, complementary, outside-frame and not assessed. |
| SelectionHandoff | `inheritsBoundedDecision` | A sourced decision with prerequisites | Carry the settled/remaining distinction forward, not an executable work permission. |
| SelectionReconsiderationBoundary | `qualifiesReassessmentOf` | Historical decision | Trigger new judgment if critical conditions change; preserve historical decision as original. |

Existing prospective `ComparativeJudgment evaluates` / `ProvisionalPreference prefers` / `Decision selects` retain their documented **ArchitectureOption/ConstructionPath endpoints**. The relationships above do not widen them to `InquiryQuestion`, `ProductPossibility`, or an arbitrary human goal. Similarly, a `source` or `references` reviewed-knowledge link is a navigation aid, not an executable `selects` or proof of governing authority.

## 5. Credible choice sets, synthesis and nonselected alternatives

The active agent must examine **option-set adequacy** when a potentially decisive missing alternative would change the selection. This is not a demand for exhaustive creative exploration: inspect the consequential omission, status quo, meaningful upstream possibilities, and source coverage to the level warranted by the actual choice.

An apparently strong candidate can be less valuable than retaining the current approach; a single credible construction path may be enough if other choices have no grounded identity. Conversely, a false binary may be **OPTION_SET_INCOMPLETE** and requires returning to appropriate source-level synthesis rather than inventing a third option.

A newly synthesized target differs from a list of positive labels. A coherence claim must describe the **new combined meaning**, what each source alternative contributes, the consequential interactions/tradeoffs and uncertain hypotheses. The synthesis can be *proposed* without being *adopted*. Selection must use the target's proper original/proposed identity and sufficient support.

Nonselected alternatives remain source-identifiable and can be explicitly `DEFERRED`, `DECLINED_FOR_THIS_PURPOSE`, `RETAINED_COMPLEMENT`, `OUTSIDE_FRAME`, `UNRESOLVED` or `NOT_ASSESSED` as **descriptive labels**, not mandatory machine statuses. Nonselected in the current comparison does not imply universally rejected or inferior.

## 6. Inheritance, reconsideration and authority

A later agent should answer **what the choice settles** and **what remains uncertain** before continuing. It should not replay the entire option analysis when a valid current choice already answers the relevant question. Nor should it treat inherited selection as immune from changed prerequisites.

```text
sourced selection + current decision-critical prerequisites
    -> subsequent reasoning may use the chosen target within stated scope
source revision or observed contradiction
    -> decide whether the changed premise is decision-critical
changed decisive premise
    -> bounded reconsideration and new attributed decision if warranted
no change to decisive premises
    -> do not reopen strategy by default
```

A reconsideration creates a **new dated interpretation** that refers to its predecessor; it does not rewrite the earlier decision, adopted product thesis or historical portfolio.

**Authority orthogonality:**
- The current `using-sensemaking` agent selects a warranted *responsibility* within actual delegation.
- A specialist returns evidence and perhaps a recommendation; it does not transfer control or owner authorization.
- A reserved Level-4 choice belongs to the appropriate owner/ADR process. The [owner-decision-capsule](../../skills/owner-decision-capsule/SKILL.md) can prepare a packet but cannot decide for the owner.
- A selected direction alone does not authorize code changes, artifact publication, protected merge, release, external integrations or any protected action. The original task and applicable governance still govern.

## 7. Representation, reuse and evidence ceiling

| Surface | What it preserves | Claim limit |
| --- | --- | --- |
| Dated source report, ADR or strategic artifact | Actual recommendation or selecting decision with source, scope, actor and authority | Authored statement, not necessarily valid real-world consequence. |
| [Optional selection record](../../skills/strategic-repository-analysis/references/convergent-direction-selection-record-template.md) | Choice set, warrant, rationale, alternative dispositions, selection scope and handoff | Documentary format, not a new executable `artifact_id`. |
| [Portable agent guidance](../../skills/strategic-repository-analysis/references/convergent-direction-selection-v1.md) | How to distinguish choice, no-selection, handoff and reopening in installed Skills | Not automatic host invocation or new routing. |
| Source-bound [reference cases](convergent-direction-selection-reference-cases-v1.md) | Real historical distinctions and clearly marked normative examples | Not a fresh independent choice-quality study. |
| Selected existing-schema `domain_concept` and `source` claims | Searchable definitions and source locations | Checked source pointers do not create decisions or authorization. |
| Existing session receipt / PR history | Activity performed and verified, or why work stopped | Receipt does not replace an actual `Decision` or independent benefit evidence. |

This module is a **conceptual/Level-2 ontology**. A small reviewed-knowledge projection under the existing Level-3 semantic system is not a new fully executable selection ontology. Before introducing a parsed decision artifact or machine relationship, demonstrate a real producer/consumer requirement and a necessary distinction lost under existing docs, `Decision`/Claim, `source`, `references` and artifact contracts; use the established [schema-evolution procedure](../../skills/repository-semantic-steward/references/schema-evolution.md).

## 8. Competencies, cases and success boundary

The [CDS-CQ-01..14 questions](convergent-direction-selection-competency-v1.md) and [source-pinned cases](convergent-direction-selection-reference-cases-v1.md) test whether a reader can recover **actual selection versus mere recommendation**, the question and typed target, target-specific warrant versus preference, actor/scope, alternatives, no-selection, synthesis limitations and meaningful reconsideration conditions.

Historical examples distinguish the **November 3 unselected convergent report**, **November 4 recommended owner-agency inquiry**, **owner-ratified ADR 0034**, **provisional architecture feedback**, and **normative NO_SELECTION/OPTION_SET_INCOMPLETE** without inventing independent trials.

**The acceptance ceiling is documentary reconstruction and usable installed guidance.** Better independent agent choice quality, user satisfaction, causal graph advantage, automatic continuation/host loading, and empirical creative benefit remain unqualified. The ontology does not itself choose a direction.
