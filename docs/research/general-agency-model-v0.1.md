# General Agency Model v0.1

**Status:** research/reference model; non-authoritative  
**Date:** 2026-09-18  
**Supersedes for research/reference use:** General Agency Model v0  
**Historical baseline preserved:** `general-agency-model-v0.md`  
**Authority:** research only; not an ADR, product-strategy revision, runtime specification, schema, Skill contract, routing rule, or implementation authorization  
**Current product boundary:** unchanged; ADR 0029 remains authoritative  
**Design:** `../superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md`

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

The candidate lifecycle remains a reasoning relation, but v0.1 makes three relationships more explicit:

1. **Memory / Provenance is a persistent substrate**, not a terminal phase.
2. **Knowledge Externalization / Communication is cross-cutting**, not a mandatory documentation phase.
3. **Exploration Policy appears only when inquiry becomes iterative search.**

```text
╔══════════════════════════════════════════════════════════╗
║ GOVERNANCE / AUTHORITY                                  ║
║ RISK / CONSEQUENCE / RESOURCES / TIME / REVERSIBILITY   ║
║                                                          ║
║   VALUE / PURPOSE                                        ║
║          ↓                                               ║
║   CONTEXT / SITUATION                                    ║
║          ↓                                               ║
║   STRATEGIC MODEL                                        ║
║          ↓                                               ║
║   DECISION FRAME                                         ║
║          ↓                                               ║
║   EPISTEMIC STATE                                        ║
║          ↓                                               ║
║   SUFFICIENCY GATE                                       ║
║       ↙           ↘                                      ║
║   INQUIRY          CHOICE                                ║
║      ↓                                                    ║
║   INQUIRY OBJECTIVE                                      ║
║      ↓                                                    ║
║   METAREASONING                                          ║
║      ↓                                                    ║
║   EXPLORATION POLICY  [only when iterative search exists]║
║      ↓                                                    ║
║   INVESTIGATION / SEARCH                                 ║
║      ↓                                                    ║
║   SEARCH EVALUATION                                      ║
║      └──────────────↺                                     ║
║                                                          ║
║               DECISION                                   ║
║                  ↓                                       ║
║               ACTION                                     ║
║                  ↓                                       ║
║               REALITY                                    ║
║                  ↓                                       ║
║            OBSERVATION                                   ║
║                  ↓                                       ║
║            VERIFICATION                                  ║
║                  ↓                                       ║
║         IMPACT / SENSEMAKING                             ║
║                  ↓                                       ║
║            BELIEF UPDATE ─────↺                          ║
║                                                          ║
║ ← CHALLENGE / EXPLORATION / COUNTERFACTUAL →             ║
║ ← KNOWLEDGE EXTERNALIZATION / COMMUNICATION →            ║
╠══════════════════════════════════════════════════════════╣
║ MEMORY / PROVENANCE SUBSTRATE                            ║
║ commitments • beliefs • evidence • uncertainty           ║
║ decisions • rationale • search history • results         ║
║ provenance • currentness • interventions                 ║
╚══════════════════════════════════════════════════════════╝
```

This diagram is a **reasoning relation**, not a mandatory runtime state machine.

Not every case requires every stage. A trivial reversible task may pass through most of the structure implicitly. A high-consequence or poorly understood decision may require explicit treatment of nearly every stage. Likewise, the presence of a capability in the architecture does not imply that the capability should become visible in every task.

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
- whether iterative search is warranted;
- when to stop.

#### 5.9.1 Exploration Policy

**Exploration Policy** is a specialized metareasoning controller that becomes explicit only when inquiry has become iterative search.

It asks:

> **Given the current search state, evidence, uncertainty, resources, and history, where should search effort go next?**

Possible search modes include:

- **EXPLOIT** — refine the current best;
- **EXPLORE** — try a materially different direction;
- **ADVERSARIAL** — search for falsification or counterexample;
- **DIAGNOSTIC** — investigate why an attempt failed;
- **COMBINATORIAL** — recombine useful components;
- **RESTART** — abandon the current local search region;
- **VERIFY** — spend effort confirming that a promising result is real.

These are descriptive modes, not a required enum or scoring system.

```text
metareasoning
= whether / how to conduct cognition or search

exploration policy
= where iterative search effort goes next once such search is warranted
```

For one-shot, obvious, reversible tasks, Exploration Policy may collapse to an implicit direct inquiry.

#### 5.9.2 Search State

**Search State** is a decision-relevant projection of Memory / Provenance for the current investigation.

It may include:

- attempts already made;
- observed outcomes;
- promising branches;
- abandoned branches and reasons;
- failures or crashes;
- failure-attribution hypotheses;
- unresolved search uncertainty;
- remaining budget;
- verified results;
- relevant provenance/currentness.

Search State may remain entirely transient for small inquiries.

```text
Search State
!= mandatory persistent object
!= SearchState.json
!= generic search-tree database
```

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

In v0.1, distinguish this **exploration operator** from **Exploration Policy**:

```text
exploration operator
-> generates/discovers alternatives

Exploration Policy
-> allocates iterative search effort among possible search modes
```

The policy may choose to invoke exploration, but it may also choose exploitation, diagnosis, adversarial challenge, recombination, restart, or verification.

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

## 11. Memory / Provenance as persistent substrate

A long-running agent may require persistence across cycles, but v0.1 treats Memory / Provenance as a substrate that can be read and written throughout the cognitive cycle rather than as a late sequential phase.

```text
Memory / Provenance
!= final lifecycle phase

Memory / Provenance
= persistent substrate read and written across cycles
```

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

### 11.7 Intervention and search history

What was tried, why, what happened, and—when iterative search is decision-relevant—which branches were explored, abandoned, verified, or left unresolved.

Search history should be preserved only when continuation, delegation, reconstruction, or search cost makes persistence useful.

### 11.8 Calibration

Where useful, whether the system's confidence has historically matched reality.

This is a **conceptual state model**.

Every major part of the cognitive cycle may read from or write to it. For example:

```text
decision frame
-> reads prior commitments/decisions

investigation
-> reads prior attempts
-> writes observations/results

verification
-> writes verified evidence/provenance

sensemaking
-> updates decision-relevant interpretation

belief update
-> updates epistemic state

externalization
-> converts selected state into durable transferable artifacts
```

Important non-identities:

```text
memory != epistemic state
memory != documentation
memory != hidden chain-of-thought
memory != universal database
provenance != truth
stored != decision-relevant
```

It does not authorize:

- a universal schema;
- a central cognitive-state database;
- automatic cross-domain ontology construction;
- a generic search-tree persistence layer.

## 12. Knowledge Externalization / Communication

**Knowledge Externalization / Communication** asks:

> **What selected knowledge should be made explicit, durable, intelligible, and transferable to another actor, in what representation, and with what provenance?**

A recipient may be:

- a future instance of the same agent;
- another agent or worker;
- a developer;
- an operator;
- a user;
- an auditor;
- a decision owner;
- the future self of the current actor.

Externalization is not identical to storage.

```text
externalization
=
selection
+ compression
+ structuring
+ explanation
+ audience adaptation
+ provenance attachment
```

Raw logs can be valuable Memory / Provenance while remaining poor externalized knowledge.

Examples of externalized knowledge include:

- ADRs and RFCs;
- specifications;
- runbooks;
- tutorials;
- handoffs;
- evidence summaries;
- release notes;
- architecture maps;
- research notes;
- machine-readable contracts;
- operationalized knowledge such as executable examples or verified API specifications.

Externalization should become explicit when one or more of the following are material:

- knowledge must survive context/session loss;
- another actor must continue the work;
- rediscovery cost is meaningful;
- the rationale behind a consequential decision must remain reconstructible;
- governance or audit requires durable evidence;
- operations or users need actionable knowledge;
- future search quality depends on preserving what was tried and learned.

Otherwise, reasoning may remain ephemeral.

```text
reasoning result
!= durable artifact required
```

Knowledge Externalization / Communication is cross-cutting. A domain may implement a dedicated documentation workflow, but the general model does not add a universal vertical `DOCUMENTATION` node.

## 20. Resource-aware metareasoning and stopping

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

### 13.1 High uncertainty does not automatically require more reasoning

If the action is:

- cheap;
- reversible;
- low consequence;
- highly informative;

acting may be more valuable than prolonged investigation.

### 13.2 Low uncertainty does not automatically justify action

If:

- authority is missing;
- consequence is extreme;
- the option set is incomplete;
- a relevant constraint is unresolved;

action may still be unwarranted.

### 13.3 Zero uncertainty is not the goal

The goal is **sufficient warrant for the current decision**.

### 13.4 Adaptive Capability Activation

v0.1 names an existing control principle:

> **A cognitive capability being available does not imply that invoking it is warranted.**

Activation is governed by:

- metareasoning;
- the sufficiency gate;
- expected decision improvement;
- reasoning, information, delay, and opportunity cost;
- consequence;
- reversibility;
- authority;
- continuation complexity.

Conceptually:

```text
available capability
        ↓
metareasoning + control envelopes
        ↓
expected decision value worth cost?
     ↙                     ↘
   yes                      no
activate                   remain implicit / skip
```

This applies to:

- challenge;
- exploration;
- Exploration Policy;
- forecasting;
- delegation;
- persistence;
- Knowledge Externalization / Communication;
- verification depth;
- strategic ascent.

```text
capability available
!= capability selected
!= capability warranted
```

## 20. Natural entry modes

There is no universal runtime start node.

### 14.1 Goal-driven entry

```text
purpose -> strategy -> decision -> inquiry/choice -> action
```

Used when a mission or desired outcome initiates reasoning.

### 14.2 Event-driven entry

```text
observation -> verification -> sensemaking -> significance -> decision -> action
```

Used when reality changes first.

### 14.3 Anomaly / surprise-driven entry

A prediction error, contradiction, failure, or unexpected opportunity can reopen a bounded part of the model.

Surprise is a trigger for reassessment, not proof that the highest-level theory is wrong.

### 14.4 Pre-existing decision entry

An agent may inherit an already-framed decision and begin at the epistemic/sufficiency boundary.

## 20. Nested loops and cadence

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

## 20. Generality and domain knowledge

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

## 20. Relationship to existing Sensemaking models

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

## 20. Strongest permitted claims

This document supports only the following bounded research claims:

1. A coherent candidate General Agency Model can be expressed using value, context, strategy, decision, epistemic state, inquiry, options, action, observation, verification, impact, sensemaking, and belief revision.
2. The model can distinguish top-down control, bottom-up learning, and lateral cognition.
3. Authority, risk, resources, constraints, time horizon, reversibility, and persistent state are plausibly cross-cutting rather than ordinary sequential nodes.
4. Prior Sensemaking transfer evidence provides limited support that some control relations can survive beyond software engineering.
5. The relationship between the General Agency Model and current Sensemaking requires explicit crosswalk and non-equivalence analysis before any product conclusion.

## 20. Explicit non-goals

This model does not establish:

- a complete or universal theory of intelligence;
- that a generic memory architecture improves outcomes;
- that an explicit Exploration Policy improves Sensemaking repository work;
- that Search State should always be persisted;
- that Knowledge Externalization should always occur;
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
- a generic memory engine or vector-memory layer;
- a generic search-state schema or search-tree database;
- an ExplorationPolicy runtime class;
- numeric exploration/exploitation scoring;
- deterministic capability activation;
- automatic documentation/externalization;
- model-weight learning or recursive self-improvement claims;
- automatic multi-agent critic voting;
- implementation priority for any candidate concept.

## 20. Research continuation rule

The next research question is not:

> How do we implement every box?

It is:

> Does this parent model clarify current Sensemaking without collapsing distinct control, semantic, authority, product, and orchestration concepts?

That question is addressed for v0.1 in `general-agency-sensemaking-crosswalk-v0.1.md`.

The v0.1 refinement should then be reconciled against the existing Practical Agent Architecture v0 and current Sensemaking surfaces before any product/runtime conclusion. Conceptual additions do not by themselves justify Practical Agent Architecture v1, a new schema, or new execution machinery.
