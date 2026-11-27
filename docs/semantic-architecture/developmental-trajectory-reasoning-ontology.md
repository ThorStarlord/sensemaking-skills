# Developmental Trajectory Reasoning Ontology v1

**Scope:** explicit conceptual specialization of the existing layered ontology, governed by ADRs 0034 and 0038. This is a normative semantic reference for agent reasoning, not a new ontology service, graph schema, controller, roadmap or authority grant. The [portable reasoning method](../../skills/using-sensemaking/references/developmental-trajectory-reasoning-v1.md) remains executable by the active agent even without the CLI.

## 1. Competency questions

A useful ontology should let the agent answer, with source and uncertainty:

- What capability state is actual, intended, hypothesized or merely imagined? What transition could change it, under which conditions?
- Which alternatives reach the same outcome differently, or different valuable outcomes from the same present? Which capabilities or constraints are shared?
- Which requirements are necessary, supporting, substitutable or unassessed? What options would a transition open, foreclose, delay or preserve, and for whom?
- Which paths could recombine and by what mechanism? What cost, incompatibility or counterevidence weakens the hypothesis?
- What earlier path, premise or choice has been affected by new evidence? What remains viable, and what must be reconsidered? How does the next context distinguish two paths with the same local ID?
- Can construction develop both the beneficiary and the agent's reasoning methods, without conflating a domain outcome with cognitive improvement?

These questions motivate a developmental landscape, not complete enumeration or a forecast. For decisions with a short, stable horizon, no separate landscape is needed.

## 2. Entities and documentary roles

| Concept | Meaning | Existing owner / representation |
| --- | --- | --- |
| DevelopmentalState | A capability/outcome condition at an assessed or hypothesized context, not a time point or task status | Observed ProductCapability/SoftwareCapability, TargetSnapshot and evidence; proposed FutureCapabilityState or ProductPossibility. Never overwrite observed identity with a proposed one. |
| DevelopmentalTransition | A proposed mechanism changing capability conditions; distinguish expected and observed effects | ConstructionPath path_transitions, ArchitecturalTransition when structural, actual Change/Outcome and evidence on realization. Not a roadmap task. |
| DevelopmentalTrajectory | A coherent possible sequence of capability development relative to a beneficiary/outcome | Existing ConstructionPath within its original strategic_repository_analysis. Not all possible futures, nor a commitment. |
| TrajectoryLandscape | Decision-relative documentary view of actual states, competing and complementary paths, conditions, consequences and open/deferred opportunities | Existing strategic analysis plus referenced possibility/architecture/consequence knowledge and dated reconciliation. No independent entity ID or master artifact. |
| EnablingCondition | A condition claimed to support or be required for a transition; strength and applicability must be stated | Existing capability references, Assumption, Hypothesis, Requirement, dependency/evidence fields or source-qualified prose. |
| SharedEnabler | An EnablingCondition hypothesized to support more than one route | Role of an existing capability/condition in a scoped comparison; shared authored reference alone establishes overlap, not enabling efficacy or complementarity. |
| DevelopmentalConstraint | A contextual limit on a transition or valuable outcome | Constraint, risk, dependency, counterevidence or ConsequenceHypothesis; actual restrictions and predicted effects separate. |
| StrategicOptionality | Qualitative capacity to pursue valuable alternatives under a stated frame after a commitment | ComparativeJudgment with conditional ConsequenceHypotheses and retained opportunities; include carrying cost and lost alternatives. No scalar or universal score. |
| EmergentOpportunity | A newly discovered valuable potential future made salient or plausibly feasible by changed capability/understanding | Existing ProductPossibility when enduring; temporary candidate otherwise. Novel discovery and actual realization are different. |
| PathDependence | Conditional effect of prior commitments on availability, cost or suitability of later choices | ConsequenceHypothesis plus prior Decision, transition and source evidence. Not determinism from temporal ordering. |
| TrajectoryConvergence | Hypothesis that two distinct routes become complementary or share a later outcome/mechanism | Comparison and ConsequenceHypothesis; existing architecture/possibility relations when endpoints fit. No automatic merge of identities. |
| TrajectoryReassessment | Attributed reconsideration of old state, path, premise or comparison using new evidence | Existing AssessmentRevisionAccount, LearningAccount or strategic_reconciliation; preserve original source and scoped decision. |

The capitalized role labels here are explanatory specializations, not new
persistent kinds. Future states, options, reviewed possibilities and
consequence hypotheses retain the established identity and retention rules.
A relationship with decision value that cannot be expressed precisely using
existing kinds is documented at its original decision site first. Consider
a formal predicate or kind only after a real producer and consumer demonstrate
an unmet semantic need; do not downgrade this conceptual model to a list of
unstructured features.

## 3. Relationship meanings and epistemic obligations

These documentary relationships refine the existing ontology. Reuse the named
existing predicates only at their declared endpoints. No new executable
predicate or transitive rule is implied.

| Source role -> relationship -> target role | Meaning / existing surface | Invalid inference |
| --- | --- | --- |
| Trajectory -> targets -> FutureCapabilityState | Existing targets; authored future_state | Forecast or adoption |
| Transition -> changesConditionOf -> State | Expected condition delta; actual Change and Outcome after evidence | A proposed transition already occurred |
| Condition -> supportsTransition -> Transition | State the mechanism, necessary/supporting/substitutable status and applicability; path builds_on, requirements and assumptions | A declared reference proves necessity |
| Condition -> sharedAcross -> Trajectories | Same condition explicitly referenced in multiple source-local paths, with separate semantic warrants | Overlap proves complementarity or common causal mechanism |
| Trajectory -> mayProduce -> ConsequenceHypothesis | Existing mayProduce | Observed causation |
| ConsequenceHypothesis -> mayEnable/mayConstrain -> existing permissible endpoint | Conditional downstream future or capability effect | Transitive reachability, guaranteed feasibility |
| Prior commitment -> mayAlterAvailabilityOf -> opportunity or trajectory | Explain path dependence, costs, counterfactual and conditions | Earlier choice is irreversible or exclusive by default |
| Trajectories -> mayRecombineToward -> state or opportunity | Specify shared interface/condition, compatible responsibilities and contrary case | Paths automatically merged or both authorized |
| Observation -> bearsOn -> original premise/transition | Attributed returned evidence; identify what is supported, weakened, contradicted or unassessed | An observed file edit proves benefit |
| Reassessment -> revisits -> prior scoped judgment | Preserve earlier frame, changed material and chosen/deferred consequence | Automatic strategy mutation or revised governing intent |

Each consequential relationship names source and target, assessed repository
revision(s), context/horizon, attribution, evidence or assumptions, status
(OBSERVED, DERIVED, INFERRED, HYPOTHESIZED, PROPOSED, EVALUATED or RATIFIED as
appropriate to the owning contract), counterevidence/limits and a reconsideration
condition if worth retaining. Use the existing epistemic rules rather than
inventing another enum. A possible multi-step chain remains conditional at
each link. Compare alternatives under the same frame or disclose the mismatch.

## 4. Identity, history and representational coverage

The local identity of a path, assumption or transition is scoped to its original
analysis. A reference such as `<analysis_ref>#PATH-1` is documentary shorthand;
retain both original values. Exact source-local references can be projected
mechanically. Cross-analysis correspondence is a separate attributed judgment
with evidence, not string similarity, chronology or matching IDs. Legacy
path-based analysis references may be associated only by exact supplied file
identity, not filename guesses. Unresolved/ambiguous references remain visibly
unresolved; a reconciliation's new current path has no implied analysis
identity if that identity is absent.

| Needed distinction | Representational status |
| --- | --- |
| Present/possible states, scoped paths, transitions, hypotheses | Existing typed/artifact surfaces adequate at initial scale |
| Common declared capability/assumption references within one analysis | Mechanically projectable from v2 fields and declared IDs; legacy prose is unassessed, not absent |
| Necessary versus supporting versus replaceable, option loss, recombination, conditional transition effects | Explicit conceptual relationships; source-qualified narrative and existing consequence/possibility records carry current need; not machine-inferred |
| Cross-analysis semantic identity, changed causal warrant | Explicit attributed reconciliation; no executable semantic matching |
| Durable reviewed knowledge projection of DTR itself | Existing knowledge kinds/relations can be assessed, but proposal preflight and exact-commit build required before claiming reviewed/indexable coverage |

The existing `strategy paths --json --include-trajectory-context` consumer
projects declared shared capability and assumption references in one analysis.
`strategy graph` keeps analysis-local identifiers distinct. Neither establishes
semantic truth, strategy, evidence completeness or implementation permission.
The source-only fallback is always the original analysis and reconciliation.

## 5. Use, feedback and proportionate persistence

Use forward and backward reasoning, compare alternatives and shared enablers,
challenge necessary-condition claims, then select the warranted responsibility
using existing controller and authority. After real work distinguish actual
domain changes, changed understanding and changed governing intent. Revisit
affected selected and unselected routes, preserve unaffected judgments, retain
enduring possibilities with the existing knowledge contract, and only reopen
Level 3 when warranted. AMS regulates reasoning effort; SCL retains attributable
method experience, not imagined causal improvement. Do not require a
TrajectoryLandscape file or new record for each task.

The [self-development episode](../../artifacts/history/2026-11-27-dtr-ontology-self-development.md)
contains a real source-grounded application and bounded construction, including
a historical local-ID collision and a shared-reference example. It is not
independent cognitive qualification.
