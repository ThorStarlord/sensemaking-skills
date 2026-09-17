# General Agency Model v0

**Status:** research/reference model; non-authoritative  
**Date:** 2026-09-17  
**Authority:** research only; not an ADR, product-strategy revision, runtime specification, schema, Skill contract, routing rule, or implementation authorization  
**Current product boundary:** unchanged; ADR 0029 remains authoritative  
**Design:** `../superpowers/specs/2026-09-17-general-agency-model-design.md`

## 1. Purpose

This document defines a candidate domain-independent model of **value-directed adaptive agency**.

The model asks:

> How does an intelligent agent relate what matters, what it believes, what it needs to learn, what it can do, what it chooses, what reality returns, and what should change afterward?

The model is intentionally broader than the current Sensemaking product. It is a research/reference abstraction that may help explain why several existing Sensemaking concepts fit together, but it does not redefine those concepts or expand the product boundary.

The working relationship is:

```text
GENERAL THEORY OF INTELLIGENT AGENCY
        |
        | may inform
        v
PRACTICAL AGENT ARCHITECTURE
        |
        | may specialize as
        v
SENSEMAKING FOR SOFTWARE ENGINEERING
        |
        | may operate within
        v
SOFTWARE-FACTORY EXECUTION / ORCHESTRATION
```

These are distinct layers.

```text
theory != runtime
runtime != product
product != orchestration environment
semantic judgment != mechanical validation
capability != authority
```

## 2. Evidence ceiling and prior research

Sensemaking has already completed a bounded domain-transfer study in `path-4-domain-transfer-results.md`.

Across eight frozen synthetic AI-research cases, the following control concepts remained coherent after software-engineering-specific semantics were replaced:

- decision-changing uncertainty;
- evidence-bounded claims;
- separation between evidence sufficiency and authority;
- continuation, stopping, and escalation;
- outcome-specific verification;
- decision versus orchestration separation.

The proposed Path 4 disposition was `TRANSFER_COHERENT`.

That is **limited transfer evidence**, not proof of a general theory of agency.

Path 4 did not establish:

- a universal value model;
- a complete value-to-action-to-learning lifecycle;
- a general option-generation architecture;
- generic forecast/simulation semantics;
- lateral adversarial/exploratory cognition as a general operator class;
- a generic memory architecture;
- a practical general-agent runtime;
- domain-general product value.

This document therefore treats Path 4 as evidence that some control relations may transfer beyond software engineering, while keeping the broader General Agency Model as a candidate theory under study.

## 3. Core distinction: reasoning versus agency

A reasoner can answer a problem presented to it.

An agent must also determine, within some authority boundary:

- what matters;
- what situation it is in;
- which decision is currently consequential;
- whether additional information is worth obtaining;
- which questions, methods, experiments, tools, or collaborators are useful;
- which actions are available;
- what consequences those actions may have;
- what to do;
- what happened;
- what the outcome means;
- whether beliefs, strategy, or purpose should change.

The model therefore treats **reasoning as one component of agency**, not as the whole of agency.

A useful shorthand is:

```text
Object-level reasoning:
What follows from this problem and evidence?

Metareasoning:
What reasoning, information gathering, or computation is worth doing?

Strategic reasoning:
What problem or decision is worth addressing?

Value reasoning:
What outcome is being treated as desirable, for whom, and under what constraints?

Reflective reasoning:
Does new evidence require revising the strategy, framing, or value commitment itself?
```

## 4. Core lifecycle

The candidate lifecycle is:

```text
VALUE / PURPOSE
        |
        v
CONTEXT / SITUATION MODEL
        |
        v
STRATEGIC MODEL
        |
        v
DECISION FRAME
        |
        v
EPISTEMIC STATE
        |
        v
SUFFICIENCY GATE
      /             \
     /               \
INQUIRE              CHOOSE
   |                    |
QUESTION /          OPTION SPACE
UNCERTAINTY              |
   |                 FORECAST /
METAREASONING        EVALUATION
   |                    |
INVESTIGATION           |
     \                 /
      \               /
          DECISION
             |
             v
           ACTION
             |
             v
           REALITY
             |
             v
        OBSERVATION
             |
             v
        VERIFICATION
             |
             v
      IMPACT ASSESSMENT
             |
             v
        SENSEMAKING
             |
             v
        BELIEF UPDATE
             |
             +-----------------> REASSESS AS WARRANTED
```

This diagram is a **reasoning relation**, not a mandatory runtime state machine.

Not every case requires every stage. A trivial reversible task may pass through most of the structure implicitly. A high-consequence or poorly understood decision may require explicit treatment of nearly every stage.

## 5. Core concepts

### 5.1 Value / Purpose

**Value / Purpose** answers:

> What outcomes matter, to whom, and why?

Value may include:

- owner/user preferences;
- mission or organizational commitments;
- safety or ethical commitments;
- legal obligations;
- scientific goals;
- economic outcomes;
- quality criteria;
- rights or non-negotiable constraints.

Value is not assumed to be a single scalar utility function.

Some values may be:

- incomparable;
- conditionally prioritized;
- stakeholder-specific;
- constrained by rights or authority;
- contested rather than empirically falsifiable.

### 5.2 Context / Situation Model

**Context / Situation Model** answers:

> What world, state, actors, constraints, resources, history, and causal relationships are relevant to the current problem?

It represents the situation in which value and action acquire meaning.

A context model may be incomplete and should preserve uncertainty rather than pretending exhaustiveness.

### 5.3 Strategic Model

**Strategic Model** answers:

> Given what matters and the current situation, where could intervention create meaningful value?

Strategy selects or narrows consequential problem space.

It is not yet the action itself.

### 5.4 Decision Frame

**Decision Frame** answers:

> What decision is actually before the agent now?

A good frame identifies:

- the choice or commitment at stake;
- relevant alternatives;
- what changes if the decision goes one way or another;
- the decision owner or authority boundary;
- the time horizon;
- the consequence of delay or error.

A malformed decision frame can make later reasoning locally correct but globally useless.

### 5.5 Epistemic State

**Epistemic State** represents what is currently believed and how strongly the evidence supports it.

It may include:

- observations;
- claims;
- hypotheses;
- evidence and counter-evidence;
- uncertainty;
- confidence or epistemic status;
- source provenance;
- currentness;
- known contradictions;
- known unknowns.

The epistemic state is not identical to memory. Memory preserves information; epistemic state expresses the currently decision-relevant belief condition.

### 5.6 Decision-Relevant Uncertainty

**Decision-relevant uncertainty** is an unresolved question whose credible alternative answers could change:

- the preferred action;
- the scope of a claim;
- whether to continue or stop;
- whether to spend resources;
- whether to escalate;
- which authority path is required;
- whether the decision is ready at all.

```text
unknown != decision-relevant uncertainty
interesting question != decision-relevant uncertainty
high uncertainty != high decision value
```

### 5.7 Sufficiency Gate

The **Sufficiency Gate** asks:

> Do we know enough to choose responsibly at this consequence, reversibility, authority, and cost level?

The gate is contextual.

The same uncertainty may be acceptable for a cheap reversible experiment and unacceptable for an irreversible high-consequence commitment.

### 5.8 Inquiry / Question Selection

When evidence is insufficient, the agent asks:

> What should be learned next?

The target is not maximum information. It is **decision-changing information**.

A useful question is one whose answer has a credible path to changing a decision.

### 5.9 Metareasoning

**Metareasoning** answers:

> How should the agent reason, investigate, search, experiment, delegate, simulate, verify, or stop?

It allocates cognitive and information-gathering effort.

Metareasoning includes deciding:

- whether to think further;
- whether to search externally;
- whether to run an experiment;
- whether to ask another agent or human;
- whether to decompose;
- whether to simulate;
- whether to challenge the current frame;
- when to stop.

### 5.10 Option Space

**Option Space** is the set of materially plausible actions, strategies, or dispositions under consideration.

Decision quality is bounded by option quality.

```text
perfect evaluation of bad options != good decision
```

Option generation therefore matters separately from option evaluation.

### 5.11 Forecast / Evaluation

**Forecast / Evaluation** asks:

> What is expected to happen under each material option, and how do those possible outcomes relate to value, risk, constraints, and uncertainty?

Evaluation may use:

- prediction;
- simulation;
- causal reasoning;
- scenario analysis;
- counterfactual analysis;
- precedent;
- expert judgment;
- bounded qualitative comparison.

The model does not require a numeric score.

### 5.12 Decision

**Decision** selects a current disposition or commitment within authority.

A decision is not automatically authorization.

```text
recommended != selected
selected != authorized
authorized != executed
executed != successful
```

### 5.13 Action

**Action** is an intervention in the world.

Action may include:

- changing software;
- running an experiment;
- sending a message;
- allocating resources;
- publishing;
- waiting;
- gathering data;
- asking a human;
- deciding to stop.

Action is broader than mutation.

### 5.14 Reality

**Reality** is the external or internal environment that responds to action and evolves independently of the agent's model.

Reality is not assumed to conform to the agent's ontology, prediction, or intended causal model.

### 5.15 Observation

**Observation** records what was measured, detected, reported, or otherwise encountered.

Observation should preserve the distinction between:

```text
what happened / was measured
!=
what it means
```

### 5.16 Verification

**Verification** asks:

> Can the observation, result, artifact, or claimed condition be trusted for the decision being made?

Verification may be:

- deterministic;
- statistical;
- replication-based;
- source/provenance-based;
- human-reviewed;
- adversarial;
- claim-specific.

Mechanical validation is one form of verification, not semantic truth.

### 5.17 Impact Assessment

**Impact Assessment** asks:

> Did the intervention change the outcomes that mattered?

This separates a successful action or proxy metric from actual value creation.

```text
action completed
!= result valid
!= intended effect occurred
!= value created
```

### 5.18 Sensemaking

**Sensemaking** integrates evidence into an interpretation relevant to the current decision and larger model.

It asks:

- what did the result establish?
- what remains uncertain?
- what causal explanation is plausible?
- what alternatives remain?
- what prior belief or assumption should change?
- what should be reconsidered next?

### 5.19 Belief Update

**Belief Update** changes the current epistemic state in response to verified evidence and interpretation.

A belief update may:

- strengthen a claim;
- weaken a claim;
- narrow a claim;
- reject a hypothesis;
- create a new uncertainty;
- change a causal model;
- expose a strategic contradiction.

Belief revision does not automatically change strategy or value. Upward revision should occur only when the evidence warrants it.

## 6. Three natural directional movements

### 6.1 Top-down control flow

```text
VALUE
  ->
STRATEGY
  ->
DECISION FRAME
  ->
INQUIRY / CHOICE
  ->
ACTION
```

Question:

> Given what matters, what should be done?

This is the natural order when the agent begins from a goal, mission, or desired outcome.

### 6.2 Bottom-up epistemic flow

```text
REALITY
  ->
OBSERVATION
  ->
VERIFICATION
  ->
SENSEMAKING
  ->
BELIEF UPDATE
  ->
selective higher-level revision
```

Question:

> Given what happened, what should now be believed?

This is the natural order when reality supplies new evidence.

### 6.3 Lateral cognitive flow

```text
current model
   <-> challenge
   <-> alternatives
   <-> countermodels
```

Question:

> What else could be true, valuable, or possible?

This flow prevents the vertical loop from becoming a confirmation machine.

## 7. Minimum necessary ascent

New evidence should not automatically reopen the highest-level commitments.

A useful control principle is:

> Revise the lowest-level assumption capable of explaining the discrepancy; ascend only when lower-level revision is insufficient.

Conceptually:

```text
execution problem?
    -> revise execution

method problem?
    -> revise reasoning method

question/frame problem?
    -> revise inquiry or decision frame

strategy problem?
    -> revise strategy

value/purpose problem?
    -> contest or revise value commitment
```

This provides stability while preserving reflectiveness.

## 8. Cognitive operators

Operators may act at multiple lifecycle stages.

They are not mandatory sequential nodes and do not imply independent runtime services.

### 8.1 Adversarial Challenge

```text
PROPOSAL
   ->
CHALLENGE
   ->
ADJUDICATION
   ->
RETAIN / REVISE / REJECT
```

It asks:

- What evidence would falsify this?
- What assumption carries the most risk?
- What alternative explanation fits the same evidence?
- What stakeholder or value has been omitted?
- What failure mode has not been considered?
- Is the question itself malformed?
- Is confidence greater than justification?

### 8.2 Exploration / Alternative Generation

Exploration asks:

- What frame has not been considered?
- What option lies outside the current search space?
- What analogy from another domain is useful?
- What opportunity is being ignored?
- What would become possible if one assumed constraint changed?

Adversarial challenge attacks or stress-tests the current model.

Exploration searches for models or options not currently represented.

### 8.3 Causal Reasoning

Causal reasoning distinguishes:

```text
X happened after Y
!=
Y caused X
```

It supports intervention design, explanation, and impact attribution.

### 8.4 Counterfactual Reasoning

Counterfactual reasoning asks:

> What would likely have happened under a different action, assumption, or condition?

It supports option evaluation and post-action learning.

### 8.5 Decomposition

Decomposition breaks a problem into bounded subproblems where doing so improves reasoning, verification, delegation, or tractability without destroying the important interaction effects.

### 8.6 Comparison

Comparison evaluates alternatives using decision-relevant dimensions.

The dimensions may be qualitative and context-dependent rather than universal scores.

### 8.7 Simulation / Forecasting

Simulation estimates possible future states under candidate interventions.

Simulation output remains evidence for judgment, not automatic authority.

## 9. Adversarial review and value contestation

Adversarial reasoning can operate on values as well as factual beliefs, but two cases must be distinguished.

### 9.1 Empirical challenge to an instrumental value claim

Example:

> Higher engagement creates more user value.

This includes empirical assumptions that can be tested.

### 9.2 Normative contestation

Example:

> User autonomy should take priority over engagement-maximizing revenue in this case.

Evidence can clarify consequences and trade-offs, but evidence alone may not settle the normative priority.

At the value layer, the appropriate operation is therefore often **contestation**, not ordinary verification.

A value review may ask:

- Value to whom?
- Who benefits?
- Who bears the cost?
- Which stakeholder is omitted?
- Which rights or commitments constrain optimization?
- What happens if this value is maximized aggressively?
- What competing value becomes material?
- Which decision owner has authority to resolve the trade-off?

## 10. Control envelopes

Control envelopes affect multiple nodes without becoming ordinary lifecycle stages.

### 10.1 Authority / Governance

Asks:

- Who may recommend?
- Who may select?
- Who may authorize?
- Who may ratify?
- What requires escalation?
- What action is prohibited even if technically possible?

Intelligence does not imply legitimate authority.

### 10.2 Risk / Consequence

Asks:

> How costly would it be to be wrong?

Higher consequence can justify:

- stronger evidence;
- deeper adversarial review;
- slower commitment;
- more independent verification;
- higher authority;
- narrower action.

### 10.3 Resources / Attention / Cost of Delay

Reasoning has cost.

Relevant resources include:

- time;
- compute;
- money;
- experiments;
- human attention;
- API/tool usage;
- scarce physical resources;
- opportunity cost.

A rational metareasoner should not gather information whose expected decision benefit is lower than its acquisition and delay cost.

### 10.4 Constraints

Constraints define the feasible or permissible action space.

They may include:

- legal restrictions;
- safety limits;
- budget;
- compatibility requirements;
- deadlines;
- contractual obligations;
- technical limits;
- governance rules.

Constraints are not always values.

### 10.5 Time Horizon

An option can be attractive short-term and destructive long-term.

Time horizon affects:

- evaluation;
- strategy;
- risk;
- reversibility;
- learning cadence;
- commitment.

### 10.6 Reversibility / Commitment

Reversible actions normally tolerate greater uncertainty than irreversible commitments.

As reversibility decreases, the architecture should generally demand more warrant before action.

## 11. Persistent state

A long-running agent requires persistence across cycles.

Candidate persistent state includes:

### 11.1 Goals and commitments

What the agent is currently pursuing and which higher-level commitments constrain it.

### 11.2 Beliefs and epistemic status

What the agent currently treats as established, inferred, uncertain, contradicted, or superseded.

### 11.3 Evidence and counter-evidence

Why those beliefs exist.

### 11.4 Unresolved uncertainty

Which open questions remain decision-relevant.

### 11.5 Decisions and rationale

What was selected, under what evidence, with what alternatives and authority.

### 11.6 Provenance and currentness

Where information came from and whether it still applies.

### 11.7 Intervention history

What was tried, why, and what happened.

### 11.8 Calibration

Where useful, whether the system's confidence has historically matched reality.

This is a **conceptual state model**.

It does not authorize:

- a universal schema;
- a central cognitive-state database;
- automatic cross-domain ontology construction.

## 12. Resource-aware metareasoning and stopping

Reasoning itself is an action with opportunity cost.

A useful abstraction is:

```text
continue reasoning when:

expected improvement in decision quality
>
cost of reasoning
+ cost of information
+ cost of delay
+ opportunity cost
```

This is not required to be numerically calculated.

It is a qualitative control principle.

### 12.1 High uncertainty does not automatically require more reasoning

If the action is:

- cheap;
- reversible;
- low consequence;
- highly informative;

acting may be more valuable than prolonged investigation.

### 12.2 Low uncertainty does not automatically justify action

If:

- authority is missing;
- consequence is extreme;
- the option set is incomplete;
- a relevant constraint is unresolved;

action may still be unwarranted.

### 12.3 Zero uncertainty is not the goal

The goal is **sufficient warrant for the current decision**.

## 13. Natural entry modes

There is no universal runtime start node.

### 13.1 Goal-driven entry

```text
purpose -> strategy -> decision -> inquiry/choice -> action
```

Used when a mission or desired outcome initiates reasoning.

### 13.2 Event-driven entry

```text
observation -> verification -> sensemaking -> significance -> decision -> action
```

Used when reality changes first.

### 13.3 Anomaly / surprise-driven entry

A prediction error, contradiction, failure, or unexpected opportunity can reopen a bounded part of the model.

Surprise is a trigger for reassessment, not proof that the highest-level theory is wrong.

### 13.4 Pre-existing decision entry

An agent may inherit an already-framed decision and begin at the epistemic/sufficiency boundary.

## 14. Nested loops and cadence

The full architecture is better understood as nested loops than as one monolithic pipeline.

```text
VALUE LOOP
Are these still the outcomes/commitments that matter?

  STRATEGY LOOP
  Are we solving the right problem?

    EPISTEMIC LOOP
    Do we understand enough to choose?

      EXECUTION LOOP
      Did the selected action work?
```

These loops need not run at the same frequency.

Higher-level commitments normally require stronger evidence and should change less frequently than execution tactics.

## 15. Generality and domain knowledge

The model distinguishes transferable control relations from domain semantics.

Potentially transferable reasoning includes:

- decomposition;
- causal reasoning;
- hypothesis generation;
- uncertainty selection;
- value-of-information reasoning;
- option generation;
- comparison;
- verification;
- stopping;
- escalation.

Domain knowledge determines:

- which variables matter;
- which measurements are trustworthy;
- what interventions are feasible;
- what consequences are likely;
- what constitutes appropriate evidence;
- which authorities and constraints apply.

The strongest general capability may therefore be not possession of every domain fact but the ability to **construct and revise a useful domain model while preserving decision and evidence discipline**.

This remains a hypothesis.

## 16. Relationship to existing Sensemaking models

This model is deliberately orthogonal to, not a replacement for, current Sensemaking models.

```text
General Agency Model
= value-to-inquiry-to-action-to-learning grammar

Semantic Architecture Reasoning Model
= evidence-to-decision grammar

Four-Level Control Model
= decision scope + authority ownership

Sensemaking product model
= repository/software-engineering decision-support specialization

Software-factory runtime
= execution/orchestration environment
```

The crosswalk and non-equivalence analysis are recorded separately in `general-agency-sensemaking-crosswalk-v0.md`.

## 17. Strongest permitted claims

This document supports only the following bounded research claims:

1. A coherent candidate General Agency Model can be expressed using value, context, strategy, decision, epistemic state, inquiry, options, action, observation, verification, impact, sensemaking, and belief revision.
2. The model can distinguish top-down control, bottom-up learning, and lateral cognition.
3. Authority, risk, resources, constraints, time horizon, reversibility, and persistent state are plausibly cross-cutting rather than ordinary sequential nodes.
4. Prior Sensemaking transfer evidence provides limited support that some control relations can survive beyond software engineering.
5. The relationship between the General Agency Model and current Sensemaking requires explicit crosswalk and non-equivalence analysis before any product conclusion.

## 18. Explicit non-goals

This model does not establish:

- a complete or universal theory of intelligence;
- an optimal decision procedure;
- a universal utility function;
- a universal ontology;
- a generic agent runtime;
- a new Sensemaking product category;
- a new planner, scheduler, or workflow engine;
- automatic objective selection;
- automatic normative adjudication;
- automatic authority expansion;
- automatic product-thesis revision;
- a universal cognitive-state database;
- automatic multi-agent critic voting;
- implementation priority for any candidate concept.

## 19. Research continuation rule

The next research question is not:

> How do we implement every box?

It is:

> Does this parent model clarify current Sensemaking without collapsing distinct control, semantic, authority, product, and orchestration concepts?

That question is addressed in `general-agency-sensemaking-crosswalk-v0.md`.

Only after that reconciliation should a separate decision ask whether a **Practical Agent Architecture v0** design is warranted.
