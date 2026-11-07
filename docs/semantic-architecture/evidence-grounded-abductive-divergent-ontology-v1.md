# Evidence-Grounded Abductive and Divergent Reasoning Ontology v1

**Status:** implemented **Level-2 conceptual/documentary composition**, 2026-11-06. No new executable kind, graph predicate, artifact schema, default stage, agent controller or empirical claim of improved reasoning.  
**Source baseline:** `ThorStarlord/sensemaking-skills@c6a9562b07b948aa07b7bb68e8bdeb1f37cb8f52`.  
**Purpose:** let agents distinguish competing source-grounded *explanations of what is observed* from divergent *possibilities about what could become desirable*, then carry forward only justified conceptual transformations.  
**Fit:** [competency assessment](evidence-grounded-abductive-divergent-competency-v1.md); [source-pinned cases](evidence-grounded-abductive-divergent-reference-cases-v1.md); [portable conditional method](../../skills/strategic-repository-analysis/references/evidence-grounded-abductive-inquiry-v1.md).

## 1. Exact intellectual distinction

**Abductive inquiry:** given an observation, contradiction, incomplete explanation or surprising result, ask *which explanations might account for it, what each would predict, and what would discriminate among them?* An explanation is a source-qualified **Hypothesis**, not an OBSERVED fact, proven cause or ratified purpose. "Best available" is a bounded comparative judgment under an explicit criterion and inspected corpus, not deductive truth.

**Divergent inquiry:** given an open question, source-grounded tensions and revisable premises, ask *which materially different ends, beneficiaries, experiences, mechanisms or questions could follow?* A CandidateExpression can remain an incomplete fragment and does not become a ProductPossibility simply by being articulated.

**Their relation:** explaining what happened may reveal a new question or future; a proposed future may generate an explanatory question. Neither operation is automatically the next stage of the other. They can legitimately coexist, diverge, stop separately, or never intersect. They do not authorize strategy selection, construction, publication or owner-intent modification.

**Assessment compatibility:** an explanatory `Hypothesis` is an unestablished `Claim` and may be evaluated under a diagnostic, purpose-relative `AssessmentFrame` without becoming a product alternative. Evidence supporting the explanation does not establish the desirability or novelty of an expression it inspires. The [abductive-to-assessment bridge](abductive-assessment-integration-v1.md), [competencies](abductive-assessment-integration-competency-v1.md) and [source cases](abductive-assessment-integration-cases-v1.md) clarify how explanation, divergence and later assessment retain distinct identity, coverage and revision histories. No mandatory transition follows.

This is a profile **composing existing semantic concepts**, not a rival to:
- [Layered Ontology](ontology.md): Observation, EvidenceSource, CounterEvidence, Hypothesis, Claim, Assumption, Provenance and authority;
- [Relations and Epistemics](relations-and-epistemics.md): OBSERVED / INFERRED / HYPOTHESIZED / CONTRADICTED / UNRESOLVED / RATIFIED and their establishment rules;
- [Reasoning Model](reasoning-model.md): evidence and claim boundaries;
- [Prospective Reasoning Ontology](prospective-reasoning-ontology.md): possible products, structural alternatives, effects and judgments;
- [Divergent Exploration Ontology](divergent-exploration-ontology.md): ExplorationInquiry, InquiryQuestion, ExplorationFrame, CandidateExpression, TransformationAccount, PossibilityLandscape and ExploratoryJudgment;
- [Cognitive Orientation Crosswalk](cognitive-orientation-crosswalk-v1.md): method-versus-target orientation, global-local coherence and reflective regulation;
- [Connected Prospective Inquiry](connected-prospective-inquiry-ontology.md): conditional consequence reasoning and specifically targeted adversarial review.

## 2. Ontology roles (existing meanings; no new machine entities)

| Documentary role | Existing representation | Essential distinction |
| --- | --- | --- |
| **Abductive inquiry** | `ExplorationInquiry` / `InquiryQuestion` plus source-scoped reasoning activity | A question about explanation or mechanism; may be bounded and need not trigger repository-wide strategy. |
| **Explandum** (thing to explain) | `Observation`, `Claim`, contradiction or explicitly absent-from-inspected-sources datum | What was actually observed, by whom, from which source/revision; no interpretation smuggled in as observation. |
| **Candidate explanation** | `Hypothesis` with source, conditions, and explanatory reach | A possible account of the explandum, not a selected root cause or prescribed correction. Distinguish from prospective `ProductPossibility`. |
| **Rival-explanation view** | Attributed, revision-scoped comparison of two or more Hypotheses in a report | Multiple explanations may coexist, overlap, or be partial; their rivalry depends on a named question and relevant discrimination basis. No "rival set" graph kind. |
| **Evidence relation assessment** | `Claim` / `ExploratoryJudgment` plus evidence/counterevidence and provenance | Whether a specific source supports, undermines, is neutral to, or has not assessed an explanation. Source admission is not causal proof. |
| **Discriminating condition or question** | `InquiryQuestion` with proposed observation, threshold in ordinary language, source/consumer, possible outcomes | A proposed observation whose alternative results would affect a named explanation contrast. Not every unanswered question is discriminating. |
| **Explanation revision account** | `TransformationAccount`, predecessor identity, revised `Hypothesis`/`InquiryQuestion` | Why an explanation was narrowed, preserved, rejected as unsupported or replaced after evidence/premise changes; historical version survives. |
| **Creative transformation from explanation** | `TransformationAccount` -> `CandidateExpression`, and optionally reviewed `poss:`/`arch:`/`conseq:` | A new end/question may be suggested by an explanation. Its novelty and value are distinct claims requiring separate grounds. |

These labels are **semantic roles inside an authored report**. Do not register them as new universal schema kinds, `artifact_id` values, `workflow` stages, graph predicates or mandatory receipt fields.

## 3. Documentary relations and establishment

| Relation (prose semantics) | Endpoints and warranted establishment | Forbidden inference |
| --- | --- | --- |
| **seeksToExplain** | InquiryQuestion -> source-identified Observation/Claim; author names scope and observed predicate | A question's wording proves the event happened |
| **offersExplanation** | Abductive inquiry -> Hypothesis, with author/date/source | Existence of H proves it is true |
| **accountsFor / wouldPredict** | Hypothesis -> observed or hypothetical consequence, with mechanism, assumptions and attribution | A fit to one datum proves causal explanation |
| **isSupportedBy / isChallengedBy** | Hypothesis -> EvidenceSource / CounterEvidence, with how and within which inspected revision | Source citation alone demonstrates support; absence from graph demonstrates negation |
| **contrastsWith** | Hypothesis -> Hypothesis under a specific Explandum, criterion and evidence boundary | Two descriptions are logically incompatible or equally plausible by default |
| **wouldDiscriminate** | InquiryQuestion (proposed observation/condition) -> identified explanation contrast, with predicted outcomes under each candidate | Merely proposing a probe shows it was run, or promises decisive falsification |
| **revisesExplanation** | later Hypothesis/TransformationAccount -> earlier one with delta and evidence | Newer text silently replaces or invalidates all historical judgments |
| **opensQuestion / yieldsExpression** | Explanation/inquiry/TransformationAccount -> new InquiryQuestion/CandidateExpression, with conceptual change recorded | An explanation licenses an adopted product end, new source fact or action |

These are **documentary relation meanings only**. A real knowledge record should use an existing supported relation/predicate, references and source-backed attributed prose, or leave the relation in its readable source. Do not silently write new relation strings into the validated store.

## 4. Five competency targets and how to avoid conflating them

1. **Rival explanations of identical observations:** preserve a shared explandum and at least two *actually distinguishable* explanatory mechanisms or preconditions. If only one is warranted or all are effectively equivalent, say so rather than padding.
2. **Evidence for and against each explanation:** name actual source identity/revision and relevance to *that explanation*. Evidence may support more than one rival; a neutral or uninspected source is not counterevidence.
3. **Assumption sensitivity:** specify what would change if a revisable premise held, failed or stayed unknown. Distinguish source-observed premises from the owner's fixed constraints; a changed assumption is not newly observed fact.
4. **Revision and discrimination:** record a question whose distinct possible results affect the explanation contrast; after evidence arrives, retain the predecessor and explain changed/narrowed/unchanged/unresolved status. Do not force a winning theory from inconclusive observations.
5. **Explanatory-to-creative transformation:** preserve source-backed inputs, asserted conceptual change and a provisional question/end/outcome. Compare to nearby prior candidates before labeling novel; do not equate explanation novelty, new wording and valuable new product goals.

[Competency assessment](evidence-grounded-abductive-divergent-competency-v1.md) demonstrates that the existing ontology can *represent* these distinctions in authored prose. Its identified gap is **explicit agent-facing abductive composition**, not an observed failure of the parsed ontology or a requirement for a new universal machine class.

## 5. Example of conditional contrast (not a diagnosis)

**Explandum:** an October 27 owner-supplied transcript reports the agent narrowed the owner's repository-wide task to examining the invoked Skill component, and then stopped early. See [local Build Loop](../agents/build-loop.md#observed-repository-only-discovery-miss-2026-10-27).

- **H1 (hypothesized):** the agent's first task frame confused the method with the target; relevant evidence is that its own declared responsibility concerned the component. This is a *leading explanation*, not a proven internal cause.
- **H2 (hypothesized):** an incomplete context read hid later repository-wide status and increased the chance of premature closure; the reported partial STATUS read is compatible with this hypothesis but does not establish the causal chain.
- **H3 (unresolved):** another instruction-application factor may matter; no discriminating host trace is available in the cited source.
- **Discriminating question:** in a new *real* invocation with known original target, actual loaded guidance and complete governing source access, does the agent preserve target scope and correct a component-only proposed stop? Even success would narrow rather than conclusively explain the original event.

A creative follow-on could ask which **different repository-wide product outcomes** become visible after the target is restored. That is a *new divergent question*, not a finding that the explanation proves such an outcome exists.

## 6. Lightweight operating profile

**Orient:** name the actual question, target and source boundary; decide whether the responsibility is explanatory, divergent, both, or direct engineering.  
**Explain if warranted:** preserve an observed explandum; construct only materially plausible rival mechanisms; check each against source and counter-source; identify discriminating, decision-relevant observation.  
**Transform if warranted:** explore new questions/ends when the explanation or a revised premise genuinely changes the potential product landscape. Use the existing Divergent Exploration vocabulary.  
**Regulate:** distinguish confirmation from fit-to-known-data; detect duplicate explanations, one-mechanism local fixation and premature creative or root-cause convergence; choose another lens, source probe or bounded stop only when it could change the answer.  
**Reconcile:** preserve original versions, uncertainty, authoring/provenance and the actual stop reason. Explanation, candidate possibility, ranking, decision and authorized action remain different things.

The [portable method](../../skills/strategic-repository-analysis/references/evidence-grounded-abductive-inquiry-v1.md) contains self-sufficient directions for installed use. No framework checkout, graph, CLI, separate Skill or new execution process is necessary.

## 7. Representation, authority and evidence ceiling

- Use existing `Hypothesis`, `Claim`, `CounterEvidence`, `Observation`, `Provenance`, `ExplorationInquiry`, `InquiryQuestion`, `CandidateExpression` and `TransformationAccount`; detailed candidate comparisons live in source-addressable reports.
- Preserve exact original/source revision separately from the publication date of a later report. Each hypothesis may have a different assessed source horizon.
- A graph miss is absence in that graph, not proof of missing implementation, false claim or original new idea.
- Contradictions are evidence to examine, not an instruction to choose a winner. An explanation can be locally credible without being exclusive, causal or globally complete.
- An authored contrast can establish **documentary reconstructibility**; it does not verify independent agent use, better reasoning quality, empirical cause, owner demand or execution.
- No new shared knowledge pack, universal schema, parsing/migration, stored explanation graph or synthetic agent evaluation follows without an actual producer/consumer competency gap and the [schema evolution gate](../../skills/repository-semantic-steward/references/schema-evolution.md).
- Owner/product commitments continue to come from accepted authoritative sources. The agent may propose hypotheses and future ends but may not ratify them, auto-select strategy, mutate target state or merge/release on that basis.

**Scope limit:** This profile is complete as a documentary semantic composition. Its independent application and creative benefit are **not qualified** by the act of writing or source-reviewing it.
