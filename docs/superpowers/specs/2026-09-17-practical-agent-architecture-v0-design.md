# Practical Agent Architecture v0 — Warrant-Centered Hybrid Design

**Status:** proposed architectural design  
**Date:** 2026-09-17  
**Target repository:** `ThorStarlord/sensemaking-skills`  
**Branch:** `research/practical-agent-architecture-v0`  
**Authority:** design only; not an ADR, product-strategy revision, runtime specification, schema change, Skill contract, routing rule, or implementation authorization  
**Parent research:** [General Agency Model v0](../../research/general-agency-model-v0.md) and [General Agency Model ↔ Sensemaking Crosswalk v0](../../research/general-agency-sensemaking-crosswalk-v0.md)  
**Current product boundary:** unchanged; [ADR 0029](../../adr/0029-current-product-boundary.md) remains authoritative

## 1. Purpose

This design answers the next question opened by the General Agency Model v0 research package:

> **What is the smallest practical architecture that can operationalize value-directed adaptive agency for AI agents without converting cognition into a rigid runtime state machine, collapsing decision into orchestration, or expanding Sensemaking into a generic autonomous-agent platform?**

The recommended answer is a **warrant-centered hybrid architecture**:

```text
semantic model judgment
        +
target-specific warrant
        +
minimal durable decision state
        +
deterministic assurance
        +
external execution/orchestration
        +
explicit authority boundaries
```

The architecture is intentionally asymmetric.

The model owns semantic judgment. Deterministic machinery owns mechanically decidable facts. Durable state preserves only what must survive context boundaries. Orchestration coordinates work that has already been selected. Authority constrains all layers.

## 2. Why this design exists

The General Agency Model identified a broad lifecycle:

```text
value
-> context
-> strategy
-> decision frame
-> epistemic state
-> sufficiency
-> inquiry / option generation
-> forecast / evaluation
-> decision
-> action
-> reality
-> observation
-> verification
-> impact assessment
-> sensemaking
-> belief update
-> selective reassessment
```

The Sensemaking crosswalk found that many of these roles already exist in domain-specific form, but several are distributed across:

- the Semantic Architecture Reasoning Model;
- the Four-Level Control Model;
- Campaign durability;
- Level-3 strategic state;
- Level-4 product-thesis review;
- authority contracts;
- validators and probes;
- research on warrant, uncertainty selection, and decision versus orchestration.

The practical architecture should therefore **compose existing ideas before inventing new machinery**.

## 3. Design classification

This is an **architectural design package**.

It does not authorize implementation.

Its job is to establish:

1. which General Agency concepts belong to semantic model reasoning;
2. which decision state should survive context boundaries;
3. which facts deterministic machinery may validate;
4. which work belongs to execution/orchestration;
5. which decisions remain owner/human-reserved;
6. how evidence flows back upward after action;
7. when adversarial challenge or exploration should be invoked;
8. what minimum interfaces would let these layers cooperate without centralizing semantic control.

## 4. Prior research this design inherits

This design builds on four existing results.

### 4.1 General Agency Model v0

The parent model provides the value-to-action-to-learning grammar.

This design does **not** turn its lifecycle nodes into mandatory runtime services.

### 4.2 Warrant as a Control Primitive

The existing warrant research defines warrant as:

> a target-specific, defeasible relation between the current situation and a proposed claim or transition.

The practical architecture adopts that relation.

It also inherits the constraints that warrant is **not**:

- a scalar confidence score;
- a universal lifecycle state;
- a synonym for authorization;
- a permission token;
- proof that downstream transitions are justified.

### 4.3 Selecting Decision-Changing Uncertainty

The uncertainty research establishes:

> investigation is valuable through its effect on a consequential decision, not because more information is inherently better.

The practical architecture therefore uses **decision-relevant warrant gaps**, not generic uncertainty reduction, as the primary trigger for inquiry.

### 4.4 Decision Versus Orchestration

The existing boundary remains:

> **Decision selects the work. Orchestration coordinates the work. Evidence determines what becomes warranted next.**

The practical architecture treats this sentence as a hard ownership constraint.

## 5. Architectural principles

### 5.1 Semantic judgment remains model-owned

The model or active agent owns judgments such as:

- what matters;
- what the current situation means;
- which decision is consequential;
- which uncertainty is decision-changing;
- what alternatives should be considered;
- what evidence implies;
- whether action, inquiry, stopping, or escalation is warranted;
- whether new evidence should change strategy.

No deterministic component may silently make these semantic selections.

At the value layer, adversarial reasoning may expose competing stakeholder interests, consequences, assumptions, or rights, but empirical evidence does not automatically settle a genuinely normative conflict. Where legitimacy or governance requires an owner/human decision, the system should surface the contest rather than manufacture a mechanical answer.

### 5.2 Mechanically decidable facts should be deterministic

Where a fact has a stable mechanical contract, infrastructure should own it.

Examples:

- identity;
- currentness;
- digest equality;
- file/reference existence;
- declared schema validity;
- transition integrity;
- configured policy constraints;
- exact-head CI status;
- authority metadata presence;
- deterministic tool output capture.

### 5.3 Persist decisions, not hidden thought

Long-running agents need memory, but the system should persist **reconstructible decision state**, not private chain-of-thought.

Persist:

- explicit commitments;
- current decision frame;
- evidence references;
- material claims;
- unresolved decision-relevant uncertainty;
- selected responsibility/action;
- authority boundary;
- concise rationale;
- stop/reopen conditions;
- provenance/currentness.

Do not persist a hidden scratchpad merely because it existed during reasoning.

### 5.4 Orchestration cannot acquire semantic authority by convenience

Queues, retries, workflows, schedulers, subagents, and fallback paths may coordinate selected work.

They may not silently change:

- the responsibility;
- the decision frame;
- the strategic objective;
- the authority path;
- the closure claim.

### 5.5 Authority is orthogonal to intelligence

```text
capable of deciding
!=
warranted to decide
!=
authorized to decide
!=
authorized to act
```

A strong model may identify a warranted action while still being required to escalate.

### 5.6 Ceremony should scale with consequence

The architecture must collapse gracefully for trivial, reversible work.

It should become explicit only as consequence, uncertainty, continuation complexity, irreversibility, novelty, or authority sensitivity increases.

## 6. Recommended architecture

The architecture has five ownership zones plus a cross-cutting authority envelope.

These zones are **ownership boundaries**, not required processes, deployable services, classes, databases, or runtime engines. A lightweight agent may realize several zones inside one model context; a larger system may distribute them across tools and processes while preserving the same ownership law.

```text
┌──────────────────────────────────────────────────────┐
│ 1. SEMANTIC AGENCY PLANE                             │
│                                                      │
│ model-owned judgment                                 │
│                                                      │
│ value / purpose interpretation                       │
│ context / situation modeling                         │
│ strategy                                             │
│ decision framing                                     │
│ epistemic interpretation                             │
│ uncertainty selection                                │
│ metareasoning                                        │
│ option generation                                    │
│ forecast / evaluation                                │
│ adversarial challenge / exploration                  │
│ impact interpretation                                │
│ sensemaking / belief revision                        │
└──────────────────────────┬───────────────────────────┘
                           │
                           │ externalizes target-specific warrant
                           v
┌──────────────────────────────────────────────────────┐
│ 2. WARRANT / DECISION CONTROL                        │
│                                                      │
│ What is justified now, for which target?             │
│                                                      │
│ possible target classes:                             │
│ claim                                                │
│ inquiry                                              │
│ responsibility                                       │
│ action                                               │
│ continue / stop / escalate                           │
│ closure                                              │
│ merge / publish / other protected transition         │
└──────────────────────────┬───────────────────────────┘
                           │
                           │ preserve only if continuation warrants
                           v
┌──────────────────────────────────────────────────────┐
│ 3. DURABLE DECISION SUBSTRATE                        │
│                                                      │
│ explicit commitments                                 │
│ decision frame                                       │
│ material evidence / claims                           │
│ decision-changing uncertainty                        │
│ selected responsibility                              │
│ authority                                            │
│ concise rationale                                    │
│ decision / transition                                │
│ reopen / stop conditions                             │
│ provenance / currentness                             │
└──────────────────────────┬───────────────────────────┘
                           │
                           v
┌──────────────────────────────────────────────────────┐
│ 4. DETERMINISTIC ASSURANCE                           │
│                                                      │
│ identity / currentness                               │
│ representation validity                              │
│ evidence existence / integrity                       │
│ provenance                                           │
│ authority metadata                                   │
│ transition integrity                                 │
│ mechanical qualification / verification              │
│                                                      │
│ NEVER selects semantic responsibility                │
└──────────────────────────┬───────────────────────────┘
                           │
                           │ selected work + bounded envelope
                           v
┌──────────────────────────────────────────────────────┐
│ 5. EXECUTION / ORCHESTRATION                         │
│                                                      │
│ tools / Skills / subagents                           │
│ workflows / workers                                  │
│ schedulers / queues                                   │
│ retries / timeout / wait                             │
│ CI / external actions                                │
│                                                      │
│ coordinates already-selected work                    │
│ returns evidence upward                              │
└──────────────────────────────────────────────────────┘

AUTHORITY / GOVERNANCE constrains every zone.
```

## 7. Zone 1 — Semantic Agency Plane

The Semantic Agency Plane is the model-owned cognition layer.

It is a **role**, not a mandatory standalone service.

### 7.1 Responsibilities

It may:

- interpret goals and value commitments;
- construct a bounded situation model;
- identify the consequential decision;
- assess current epistemic state;
- identify warrant dependencies;
- select decision-relevant uncertainty;
- decide whether more reasoning is worth its cost;
- generate alternatives;
- challenge assumptions;
- forecast outcomes;
- compare alternatives qualitatively;
- interpret verification results;
- assess impact;
- revise explicit beliefs;
- decide whether evidence requires upward strategic/value reassessment.

### 7.2 What it must not silently do

It must not treat:

- a capability listing as a recommendation;
- a validator PASS as semantic truth;
- an available tool as authorization;
- a stored prior decision as permanently current;
- a high-confidence answer as owner authority;
- an orchestration fallback as a new responsibility.

### 7.3 Implementation posture

For v0, these functions should primarily remain:

- model instructions;
- reasoning policy;
- explicit prompt/context structure;
- bounded tool use.

Do **not** create one runtime component per cognitive function.

## 8. Zone 2 — Warrant / Decision Control

### 8.1 Warrant is the bridge

The practical architecture uses warrant to connect evidence, uncertainty, action, authority, and stopping.

Informally:

```text
W(
  target
  |
  goal,
  current_state,
  evidence,
  constraints,
  authority
)
```

This notation is explanatory.

**Warrant is not a score, ranking, authorization token, or deterministic decision function.** It is an explicit semantic justification relation that may be supported or defeated by evidence, constraints, and authority.

### 8.2 Warrant target classes

Candidate target classes include:

- **claim** — may this proposition be asserted?
- **inquiry** — is further investigation worth doing?
- **responsibility** — is this class of work justified?
- **action** — should this intervention be performed?
- **continue** — should the current process continue?
- **stop** — is additional work no longer justified?
- **escalate** — is higher authority or broader scope required?
- **closure** — is the original decision/finding resolved?
- **protected transition** — is merge/publish/deploy/release appropriate and authorized?

These are conceptual classes, not a required enum.

### 8.3 Warrant dependencies

For a contemplated target, the agent should ask:

> **What must be true for this target to be justified now?**

A warrant dependency can involve:

- factual claims;
- evidence sufficiency;
- scope;
- currentness;
- constraints;
- authority;
- reversibility;
- resource cost;
- dependencies;
- expected impact.

### 8.4 Warrant gap

A warrant gap is a missing premise or authority condition that blocks a contemplated target.

The architecture does not require a persistent `warrant_gap` schema.

It requires the agent to be able to externalize the blocking uncertainty when continuation depends on it.

### 8.5 Target-locality

```text
warrant for investigation
!=
warrant for repair

warrant for candidate correctness
!=
warrant for merge

warrant for configured-test PASS claim
!=
warrant for user-value claim

warrant for responsibility selection
!=
authority to execute
```

This locality is essential.

## 9. Zone 3 — Durable Decision Substrate

The Durable Decision Substrate exists so a fresh context can reconstruct **what decision is live and why**, without replaying hidden internal reasoning.

### 9.1 Minimum persistence rule

Persist only information whose loss could materially change:

- the reconstructed decision;
- the authority path;
- the evidence boundary;
- the stop/continue decision;
- the ability to verify or hand off work.

### 9.2 Candidate durable concepts

A consequential long-running decision may need:

```text
Commitments
DecisionFrame
TargetIdentity / Currentness
MaterialClaims
EvidenceRefs
DecisionRelevantUncertainty
SelectedResponsibility
AuthorityBoundary
Decision
ConciseRationale
Dependencies
StopConditions
ReopenConditions
Provenance
TransitionHistory
```

### 9.3 Concise rationale versus chain-of-thought

The durable rationale should answer:

- what decision was made;
- what evidence materially supported it;
- what alternatives were material;
- what uncertainty remains;
- what would reopen the decision.

It should not attempt to persist private internal chain-of-thought.

### 9.4 Existing substrate first

For Sensemaking, existing structures should be reused before designing a new generic state store:

- Campaign state;
- Campaign evidence and transitions;
- semantic-state records;
- STATUS / Strategic Frontier;
- ADRs;
- handoff/resume state;
- target identity/currentness;
- existing authority metadata.

A generic cognitive-state database is out of scope for v0.

### 9.5 Persistence should be optional

```text
agency used
!=
durable state required
```

A trivial task may need no durable substrate at all.

## 10. Zone 4 — Deterministic Assurance

Deterministic Assurance owns facts for which a stable mechanical predicate exists.

### 10.1 Appropriate deterministic responsibilities

Examples:

- schema validity;
- target identity;
- currentness checks;
- artifact digests;
- evidence-reference resolution;
- provenance integrity;
- transition-chain integrity;
- declared authority metadata presence;
- capability declaration lookup;
- exact-head checkout identity;
- configured test/validator result;
- static conformance;
- reproducible mechanical probes.

### 10.2 Forbidden semantic promotions

```text
evidence exists
!= evidence is decision-sufficient

schema valid
!= decision is good

authority field present
!= actor is morally or organizationally entitled

capability compatible
!= capability selected

test passed
!= user value created

reference resolved
!= referenced claim is true
```

### 10.3 Deterministic gates may fail closed

Infrastructure may block a transition when a declared mechanical precondition is false.

Examples:

- stale target binding;
- missing required evidence reference;
- invalid digest;
- malformed transition;
- absent required approval reference.

Failing closed on a mechanical contract is not semantic selection.

## 11. Zone 5 — Execution / Orchestration

Execution/orchestration performs already-selected work.

### 11.1 Legitimate responsibilities

It may:

- invoke a selected tool or Skill;
- delegate a bounded task to a subagent;
- sequence deterministic steps;
- run CI/tests;
- wait/retry under declared policy;
- capture outputs;
- move artifacts;
- execute a selected workflow;
- return observations/evidence.

### 11.2 Forbidden responsibility expansion

Execution may not decide:

- that repair should replace investigation;
- that a different strategic objective is now preferable;
- that an owner-reserved action is implicitly approved;
- that a failed tool call justifies crossing a product boundary;
- that a new repository should become in scope;
- that a validator result establishes semantic closure.

### 11.3 Failure returns evidence upward

A failed execution does not automatically select fallback responsibility.

```text
selected responsibility
        |
orchestration attempt
        |
failure evidence
        |
semantic reassessment
        |
same responsibility
OR revised responsibility
OR stop
OR escalate
```

The semantic layer owns that reassessment.

## 12. Cross-cutting Authority / Governance Envelope

Authority applies across the architecture.

### 12.1 Authority questions

Every consequential transition may need to distinguish:

- Who may propose?
- Who may recommend?
- Who may select?
- Who may authorize?
- Who may execute?
- Who may ratify?
- Who may publish/merge/deploy?
- Who may revise the governing objective?

### 12.2 Owner-reserved decisions

Within the current Sensemaking product boundary, examples may include:

- Level-4 thesis ratification;
- protected merge/release/publication where owner policy reserves it;
- expansion of product scope;
- changing governing authority contracts;
- irreversible external actions not already delegated.

### 12.3 Authority is explicit state where consequential

The model may reason about authority semantically.

Deterministic infrastructure may validate declared authority metadata or approval references.

Neither grants itself additional authority.

## 13. General Agency concept placement matrix

This matrix is the main classification output of Practical Agent Architecture v0.

| General Agency concept | Primary owner | Persist when? | Deterministic support | Orchestration role |
| --- | --- | --- | --- | --- |
| **Value / Purpose** | Semantic Agency | When a long-running decision depends on explicit commitments | identity/reference integrity only | none |
| **Context / Situation** | Semantic Agency | When continuity requires reconstruction of bounded context | target identity, currentness, probes | collect requested data |
| **Strategic Model** | Semantic Agency | When strategic continuation crosses contexts | structural state validation only | execute selected strategic responsibility |
| **Decision Frame** | Semantic Agency | Usually for consequential durable work | representation/currentness checks | none |
| **Epistemic State** | Semantic Agency | Material claims/evidence/uncertainty only | provenance, reference integrity | collect evidence |
| **Decision-Relevant Uncertainty** | Semantic Agency | When unresolved uncertainty controls continuation | structural validation only | execute selected inquiry |
| **Sufficiency Gate** | Semantic Agency | Persist resulting decision/stop reason when material | verify declared prerequisites | none |
| **Question Selection** | Semantic Agency | Only selected inquiry / warrant dependency if durable | none beyond representation | run selected search/experiment |
| **Metareasoning** | Semantic Agency | Normally not persisted beyond explicit selected method/rationale | resource/limit telemetry may be mechanical | coordinate selected computation |
| **Option Generation** | Semantic Agency | Material alternatives for consequential decisions | dedupe/identity if useful | gather requested option evidence |
| **Forecast / Evaluation** | Semantic Agency, tool-assisted | Material forecast claims/evidence | deterministic simulation when contract exists | run selected simulation/tool |
| **Decision** | Semantic Agency within authority | Yes when consequential/durable | transition integrity | execute only if authorized |
| **Action** | Execution / Orchestration after semantic selection | outcome/evidence, not hidden execution thought | mechanical precondition checks | primary owner |
| **Reality / Environment** | external | no direct persistence requirement | sensors/probes/tool output | interaction surface |
| **Observation** | capture may be mechanical; meaning semantic | when material evidence | provenance/currentness | capture |
| **Verification** | Hybrid | verification result if material | deterministic where decidable | run verification |
| **Impact Assessment** | Semantic Agency | when it affects continuation/closure/strategy | metric calculation may be deterministic | collect outcome data |
| **Sensemaking** | Semantic Agency | conclusions, not hidden reasoning | none beyond integrity | none |
| **Belief Update** | Semantic Agency | material revised claims/uncertainty | state integrity | none |
| **Adversarial Challenge** | Semantic operator | only challenge/result if materially decision-changing | none by default | may delegate critic work |
| **Exploration** | Semantic operator | material alternatives only | none by default | may delegate discovery |
| **Authority / Governance** | Human/owner + explicit policy | when consequential | metadata/approval validation | enforce execution boundary |
| **Risk / Consequence** | Semantic control envelope | explicit constraints when material | metric calculation if defined | none |
| **Resources / Attention** | Semantic metareasoning + system limits | explicit budget only when needed | usage accounting | enforce selected budgets |
| **Constraints** | Hybrid | material constraints | deterministic validation where possible | obey constraints |
| **Time Horizon** | Semantic control envelope | when decision depends on it | deadlines/timestamps | scheduling only after decision |
| **Reversibility / Commitment** | Semantic control envelope | when material | mechanical rollback availability may be inspectable | execute authorized reversible steps |

## 14. Natural operational loop

The practical control loop is:

```text
TRIGGER
(goal / event / anomaly / inherited decision)
        |
        v
BIND PURPOSE + AUTHORITY + TARGET
        |
        v
RECONSTRUCT / BUILD DECISION FRAME
        |
        v
RECONSTRUCT / BUILD EPISTEMIC STATE
        |
        v
NAME CONTEMPLATED WARRANT TARGET
        |
        v
IDENTIFY WARRANT DEPENDENCIES
        |
        v
IS TARGET SUFFICIENTLY WARRANTED?
        |
     +--+--+
     |     |
    YES    NO
     |     |
     |     v
     |   SELECT DECISION-RELEVANT WARRANT GAP
     |     |
     |   CHOOSE REASONING / INQUIRY METHOD
     |     |
     |   ORCHESTRATE INVESTIGATION
     |     |
     |   CAPTURE OBSERVATION
     |     |
     |   VERIFY
     |     |
     |   SENSEMAKE / UPDATE EXPLICIT BELIEF STATE
     |     |
     +-----+
        |
        v
SELECT:
INQUIRE / ACT / STOP / ESCALATE / VERIFY / CLOSE
        |
        v
CHECK AUTHORITY + MECHANICAL PRECONDITIONS
        |
        v
ORCHESTRATE SELECTED WORK
        |
        v
REALITY / RESULT
        |
        v
OBSERVATION + VERIFICATION
        |
        v
IMPACT / SENSEMAKING
        |
        v
UPDATE WARRANT
        |
        +---------------------> repeat only as warranted
```

## 15. Warrant update is not automatic planning

The phrase **update warrant** means:

> reconsider whether a specific contemplated target remains justified given new evidence and authority.

It does not mean:

- automatically compute the next objective;
- automatically rank all possible actions;
- automatically choose a Skill;
- automatically create a Campaign;
- automatically launch the next workflow.

## 16. Adversarial challenge policy

Adversarial review is a lateral semantic operator.

It should not be mandatory on every decision.

### 16.1 Strong challenge triggers

Challenge becomes more valuable when one or more of these are materially present:

- high consequence of error;
- low reversibility;
- conflicting evidence;
- unusually high confidence from weak evidence;
- novel or poorly understood domain;
- narrow option set on a consequential decision;
- repeated failure;
- strong stakeholder/value conflict;
- decision frame instability;
- external publication/commitment;
- closure claim with weak falsification evidence.

### 16.2 Challenge targets

A critic may challenge:

- value interpretation;
- decision frame;
- causal assumption;
- claim;
- evidence sufficiency;
- selected uncertainty;
- option set;
- forecast;
- selected action;
- impact interpretation;
- closure claim.

### 16.3 Critic output

A critic/subagent returns:

- counter-evidence;
- alternative hypotheses;
- omitted stakeholders/constraints;
- failure modes;
- falsification tests;
- candidate reframes.

It does **not** automatically overrule the primary agent.

The primary semantic controller adjudicates the challenge under authority.

## 17. Exploration policy

Exploration is distinct from adversarial criticism.

Exploration asks:

> **What plausible frame, option, explanation, or intervention is not yet represented?**

### 17.1 Useful exploration triggers

Explore when:

- all current options are weak;
- a consequential decision has only one generated option;
- repeated attempts fail;
- the current frame creates circular investigation;
- evidence suggests the problem category may be wrong;
- local optimization may be hiding a better boundary;
- a high-value opportunity is plausible but not represented.

### 17.2 Stopping exploration

Stop when:

- additional alternatives are unlikely to change the decision;
- the selected option is sufficiently warranted and reversible;
- search cost exceeds likely decision improvement;
- authority/time constraints dominate;
- remaining alternatives are materially dominated under the current evidence.

No numeric score is required.

## 18. Resource-aware metareasoning

The architecture treats reasoning as resource-consuming work.

A qualitative control law is:

```text
continue reasoning when

expected decision improvement
>
reasoning cost
+ information cost
+ delay cost
+ opportunity cost
```

The system need not calculate this numerically.

### 18.1 Cheap reversible action

When action is cheap, reversible, low consequence, and information-producing:

> act may be better than think more.

### 18.2 Expensive irreversible action

When action is consequential, propagating, externally visible, or hard to reverse:

> stronger evidence, challenge, verification, and authority may be warranted.

## 19. Multi-agent delegation

Multi-agent systems fit inside this architecture without changing control ownership.

### 19.1 Parent agent

The parent/active semantic controller owns:

- current decision frame;
- warrant target;
- delegation purpose;
- integration of returned evidence;
- final semantic reassessment.

### 19.2 Worker/subagent

A worker may be delegated:

- bounded investigation;
- code change;
- proof attempt;
- adversarial review;
- alternative generation;
- verification;
- domain-specific analysis.

The delegation should specify:

- responsibility;
- scope;
- authority;
- expected artifact/evidence;
- success/stop conditions.

### 19.3 Returned result

A subagent result is evidence.

```text
subagent recommendation
!= parent decision

subagent success
!= global closure

subagent capability
!= delegated authority expansion
```

### 19.4 Multiple critics

The architecture does not recommend automatic majority voting.

Disagreement should be preserved as evidence for semantic adjudication.

## 20. Interaction with existing Sensemaking structures

The Practical Agent Architecture should first be realized by **composition**, not replacement.

### 20.1 Campaign

Campaign already provides a durable Level-2 substrate for:

- goal;
- uncertainty;
- responsibility;
- evidence;
- authority;
- transition history;
- continuation.

Practical Agent Architecture should not create a parallel universal agent state if Campaign can carry the required decision state for repository work.

### 20.2 Semantic Architecture

The Semantic Reasoning Model already supplies the evidence-to-decision grammar.

The Practical Agent Architecture should use it inside the wider warrant loop.

### 20.3 Strategic state

Level 3 already externalizes:

- current strategic decision;
- frontier/candidates;
- evidence;
- authority;
- stop/no-change conditions.

### 20.4 Level 4

Product-thesis revision already demonstrates minimum-necessary ascent and owner-ratified value/strategy revision.

### 20.5 Software-factory integration

A software factory may supply:

- issue/event intake;
- workers;
- scheduling;
- repo checkout;
- CI;
- retry;
- artifact transport;
- merge mechanics.

Sensemaking-informed agency supplies:

- what decision is live;
- what responsibility is warranted;
- what evidence matters;
- whether results justify continuation or escalation.

## 21. Failure handling

### 21.1 Stale context

If target identity/currentness is stale:

```text
do not continue from remembered semantic state
-> rebind/reconstruct
-> identify what remains valid
-> reassess warrant
```

### 21.2 Missing evidence

If a material claim cannot be reconstructed from evidence:

- downgrade the claim;
- reopen uncertainty;
- reacquire evidence;
- or stop/escalate.

Do not silently preserve confidence.

### 21.3 Contradictory evidence

Contradiction should trigger:

- semantic adjudication;
- targeted investigation;
- narrowed claim;
- or upward reassessment when material.

Do not average incompatible claims mechanically.

### 21.4 Execution failure

Execution failure returns evidence to the semantic controller.

Retries may be automatic only inside an already-selected responsibility and declared retry policy.

### 21.5 Authority failure

If an action is warranted but not authorized:

```text
WARRANTED_ACTION
+
AUTHORITY_MISSING
=
ESCALATE / HOLD
```

Do not reinterpret missing authority as a technical failure.

### 21.6 No-result

A no-result may still reduce uncertainty.

The architecture should preserve:

- what was attempted;
- what scope was inspected;
- what the negative result does and does not establish.

## 22. Security and governance implications

This architecture reduces several failure modes:

### 22.1 Hidden autonomy creep

Explicit warrant and authority boundaries make it harder for orchestration to silently expand scope.

### 22.2 Stale-memory action

Currentness and target binding prevent old decisions from masquerading as current authorization.

### 22.3 Validator overreach

Deterministic assurance is explicitly evidence, not semantic truth.

### 22.4 Critic overreach

Adversarial subagents generate challenge evidence; they do not become automatic veto/approval authorities.

### 22.5 Goal drift

Durable commitments and decision frames provide a reconstructible reference for detecting whether execution has drifted from the selected responsibility.

## 23. Approaches considered

### Approach A — Protocol-only reasoning guidance

Keep the General Agency Model as prompt-level reasoning guidance and add no explicit architecture beyond current Sensemaking.

**Advantages:**

- minimal product complexity;
- no new conceptual runtime boundaries;
- easiest to preserve ADR 0029.

**Limitations:**

- weaker account of how long-running general agent work should externalize decision state;
- less explicit decision/orchestration interface;
- does not clearly classify when challenge/exploration/persistence should become visible.

### Approach B — Warrant-centered hybrid architecture

**Selected.**

Combine:

- semantic model reasoning;
- target-specific warrant;
- minimal durable decision state;
- deterministic assurance;
- external orchestration;
- explicit authority.

**Advantages:**

- operationalizes the General Agency Model without a generic cognition engine;
- reuses current Sensemaking mechanisms;
- provides clear multi-agent and orchestration boundaries;
- preserves gradual visibility/ceremony;
- gives persistence a principled minimum scope.

**Risks:**

- “warrant” could become vague if target/dependencies are not explicit;
- teams may be tempted to turn qualitative warrant into a score;
- durable state may expand into a generic ontology if not constrained.

### Approach C — Explicit cognitive runtime/state machine

Implement lifecycle nodes as runtime services/states.

**Advantages:**

- high observability;
- easy workflow visualization;
- deterministic transition tracking.

**Rejected for v0 because:**

- semantic cognition is not mechanically stable enough for those boundaries;
- risks encoding premature ontology;
- invites `OuterLoopEngine` behavior;
- centralizes semantic control;
- conflicts with the current product boundary and research evidence ceiling.

## 24. Design invariants

Any later implementation should preserve these invariants.

### Invariant 1

```text
semantic judgment remains agent-owned
```

### Invariant 2

```text
deterministic machinery may validate representation
but may not convert representation into semantic selection
```

### Invariant 3

```text
warrant is target-specific and defeasible
```

### Invariant 4

```text
warrant != authorization
```

### Invariant 5

```text
persist explicit decision state
!= persist hidden chain-of-thought
```

### Invariant 6

```text
decision selects work
orchestration coordinates selected work
evidence returns upward
```

### Invariant 7

```text
challenge / exploration produce evidence
not automatic authority
```

### Invariant 8

```text
higher-level revision occurs only as far upward as evidence requires
```

### Invariant 9

```text
trivial reversible work must remain trivial
```

### Invariant 10

```text
a practical architecture concept does not automatically justify a product feature
```

## 25. Candidate implementation surfaces — not yet authorized

If a later implementation plan is warranted, likely surfaces should be considered in this order.

### 25.1 Agent-facing reasoning guidance

Potentially clarify:

- contemplated warrant target;
- warrant dependencies;
- decision-relevant warrant gaps;
- challenge/exploration triggers;
- resource-aware stopping;
- evidence return from subagents/orchestration.

This may require documentation/Skill guidance before code.

### 25.2 Reuse of existing durable state

Determine whether Campaign / strategic-state / semantic-state surfaces already carry enough explicit decision state.

Add no schema unless a demonstrated reconstruction failure requires it.

### 25.3 Deterministic assurance gaps

Only add machinery for mechanically decidable needs exposed by concrete use.

### 25.4 Orchestration interface guidance

Document the handoff:

```text
selected responsibility
+ authority envelope
+ expected evidence
-> orchestration
-> evidence/result
-> semantic reassessment
```

Do not build generic orchestration inside Sensemaking.

### 25.5 Challenge/exploration operator guidance

Prefer prompting/delegation conventions first.

Build dedicated components only after repeated evidence shows the convention is insufficient.

## 26. Implementation decision matrix

A later implementation proposal must classify every proposed addition into exactly one primary category.

| Category | Test |
| --- | --- |
| **Reasoning guidance** | Does this help the model make a semantic judgment? |
| **Durable representation** | Must this explicit state survive context/process boundaries to reconstruct the decision? |
| **Deterministic assurance** | Is there a mechanically decidable invariant with a stable contract? |
| **Orchestration interface** | Does this coordinate work that has already been semantically selected? |
| **Owner/human authority** | Is the decision reserved because legitimacy/governance, not capability, requires a human/owner? |

If a proposed feature cannot be cleanly classified, it should not be implemented until the ambiguity is resolved.

## 27. Validation strategy for the design

This design should be reviewed against scenario classes rather than runtime benchmarks.

### Scenario A — trivial reversible engineering task

Expected:

- semantic processing remains mostly implicit;
- no Campaign/general state object required;
- bounded work proceeds with normal verification.

### Scenario B — ambiguous repository responsibility

Expected:

- decision frame and warrant dependencies become explicit;
- inquiry resolves the nearest decision-changing warrant gap;
- existing Sensemaking structures suffice.

### Scenario C — long-running multi-agent repository change

Expected:

- parent agent owns decision;
- workers receive bounded responsibilities;
- durable state preserves explicit continuation;
- orchestration coordinates execution;
- results return as evidence.

### Scenario D — strategic repository choice

Expected:

- Level 3 remains the strategic specialization;
- options/forecast/challenge support judgment;
- no deterministic ranking.

### Scenario E — product-thesis contradiction

Expected:

- evidence ascends only as far as needed;
- Level-4 owner authority remains intact.

### Scenario F — external protected action

Expected:

- technical warrant can exist without execution authority;
- system holds/escalates instead of inferring permission.

### Scenario G — failed worker/tool

Expected:

- orchestration returns failure evidence;
- semantic controller decides retry/change responsibility/stop;
- fallback mechanics do not silently change responsibility.

### Scenario H — adversarial review

Expected:

- critic returns counter-evidence/alternatives;
- primary agent adjudicates;
- disagreement may remain unresolved.

## 28. Success criteria

The design succeeds if a fresh reader can answer:

1. What makes this architecture “practical” rather than only theoretical?
2. Which cognition remains model-owned?
3. What exactly is warrant?
4. Why is warrant not a score or authorization token?
5. What state should persist?
6. What state should not persist?
7. What may deterministic machinery decide?
8. What may orchestration decide?
9. How do subagents fit?
10. When should adversarial challenge/exploration occur?
11. How does evidence re-enter the decision loop?
12. Which decisions remain owner/human-reserved?
13. Why does this architecture not require an `OuterLoopEngine`?
14. How can current Sensemaking structures implement much of it without new machinery?

## 29. Explicit non-goals

This design does not authorize:

- a general autonomous-agent runtime;
- a cognitive workflow engine;
- `StrategicPlanner`;
- `OuterLoopEngine`;
- deterministic objective selection;
- deterministic uncertainty ranking;
- deterministic option ranking;
- numeric warrant scoring;
- automatic normative adjudication;
- universal memory/database schema;
- hidden chain-of-thought persistence;
- automatic critic voting;
- automatic Campaign creation;
- automatic Skill selection;
- generic worker scheduling inside Sensemaking;
- autonomous merge/release/deployment/publication;
- expansion beyond ADR 0029;
- immediate implementation of any candidate surface.

## 30. Design conclusion

The practical architecture should not be:

```text
General Agency lifecycle
-> one runtime component per node
```

It should be:

```text
General Agency lifecycle
        |
        v
semantic model judgment
        |
        v
target-specific warrant
        |
        v
minimal explicit decision state
        |
        v
deterministic assurance where facts are mechanical
        |
        v
external orchestration of selected work
        |
        v
evidence returns upward
        |
        v
semantic reassessment
```

The core operational law is:

> **The active agent reasons about what is warranted. Durable state preserves the explicit decision boundary. Deterministic machinery verifies only mechanically decidable facts. Orchestration performs selected work. Authority constrains every transition.**

## 31. Next gate

If this design is approved, the next task is to write an implementation/reconciliation plan that answers:

1. Which parts are already satisfied by current Sensemaking?
2. Which parts require only documentation/Skill guidance?
3. Which parts reveal a genuine durable-state gap?
4. Which parts reveal a genuine deterministic-assurance gap?
5. Which parts belong entirely outside the Sensemaking repository?
6. What is the smallest bounded implementation package, if any?

The implementation plan must begin from **gap analysis**, not from the assumption that every architecture concept should produce code.
