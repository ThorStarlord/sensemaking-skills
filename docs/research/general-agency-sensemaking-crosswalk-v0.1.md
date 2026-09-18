# General Agency Model ↔ Sensemaking Crosswalk v0.1

**Status:** research reconciliation / non-authoritative  
**Date:** 2026-09-18  
**Supersedes for research/reference use:** General Agency Model ↔ Sensemaking Crosswalk v0  
**Historical baseline preserved:** `general-agency-sensemaking-crosswalk-v0.md`  
**Authority:** research only; does not change ADR 0029, product strategy, the Four-Level Control Model, the Semantic Reasoning Model, Campaign semantics, or runtime authority  
**Parent model:** `general-agency-model-v0.1.md`  
**Design:** `../superpowers/specs/2026-09-18-general-agency-model-v0.1-design.md`

## 1. Research question

> Does General Agency Model v0.1 clarify persistence, knowledge externalization, iterative-search control, and adaptive capability activation without forcing Sensemaking to add unwarranted state or runtime machinery?

This is a reconciliation exercise, not a product revision.

No canonical Sensemaking authority document is modified by this artifact.

## 2. Mapping vocabulary

Mappings use four categories.

### `EXACT`

The General Agency concept and an existing Sensemaking concept perform materially the same reasoning role at the relevant scope.

### `PARTIAL`

Sensemaking contains part of the concept or performs the role implicitly, but the General Agency concept is broader or more explicit.

### `DOMAIN_SPECIALIZATION`

Sensemaking contains a software/repository-specific realization of the broader concept.

### `NON_EQUIVALENT`

The concepts may look similar but should not be treated as interchangeable.

A tidy mapping is not preferred over an honest one.

## 3. Model-role separation

The strongest result of this reconciliation is that the models answer different questions.

```text
General Agency Model
= value-to-inquiry-to-action-to-learning grammar

Semantic Architecture Reasoning Model
= evidence-to-decision grammar

Four-Level Control Model
= decision scope + authority ownership

Sensemaking product model
= software-engineering-domain decision-support specialization

Software-factory runtime
= execution/orchestration environment
```

These are complementary.

The General Agency Model is broader in semantic scope, but it does not supersede the more precise Sensemaking models inside their current domain.

## 4. Concept crosswalk

| General Agency concept | Current Sensemaking analogue | Mapping | Reconciliation |
| --- | --- | --- | --- |
| **Value / Purpose** | Level-4 product purpose, problem, JTBD, value proposition, strategic principles | `DOMAIN_SPECIALIZATION` | Sensemaking has explicit value-bearing commitments, but they are commitments about the Sensemaking product, not a universal value model. |
| **Context / Situation Model** | bounded current state, target identity/currentness, semantic map, repository/product capability state | `DOMAIN_SPECIALIZATION` | Sensemaking constructs decision-bounded repository/product context rather than a general world model. |
| **Strategic Model** | Level-3 Strategic Repository Evolution | `DOMAIN_SPECIALIZATION` | Level 3 asks where repository/product intervention is warranted under current product strategy. General strategy can concern any domain. |
| **Decision Frame** | Decision Being Supported; Strategic Decision to Support; affected Level-4 commitment | `EXACT` at reasoning-role level | Sensemaking explicitly requires the consequential decision to be stated before uncertainty/responsibility selection. Scope and authority vary by level. |
| **Epistemic State** | Observation → Evidence → Claim → EpistemicStatus → Contradiction/Uncertainty | `EXACT` as a bounded grammar | Sensemaking already distinguishes observation, evidence, claims, status, contradiction, and uncertainty. Its representations are repository/product oriented. |
| **Decision-relevant uncertainty** | consequential uncertainty / decision-changing uncertainty | `EXACT` | Both define uncertainty by whether a credible answer could change a decision, action, scope, authority path, or stop/continue result. |
| **Sufficiency Gate** | Semantic Reasoning Model stopping rule | `EXACT` as a control principle | Sensemaking already stops when evidence is sufficient for the decision, remaining uncertainty would not change action, or more evidence is unavailable/outside authority/not worth cost. |
| **Inquiry / Question Selection** | select consequential uncertainty; identify cheapest sufficient evidence; select evidence-producing responsibility | `PARTIAL` | Sensemaking expresses inquiry through uncertainty/evidence/responsibility reasoning rather than a general question-selection abstraction. |
| **Metareasoning** | agent selects uncertainty, responsibility, capability, evidence path, stopping behavior | `PARTIAL` | Sensemaking contains substantial metareasoning but does not name a generic cognitive-resource controller. |
| **Option Space** | Strategic Frontier candidates; bounded Level-4 alternatives; competing responsibilities | `PARTIAL` | Sensemaking represents alternatives where needed, but does not define general option generation as a first-class cross-domain concept. |
| **Forecast / Evaluation** | qualitative frontier lenses, expected decision effect, consequence of error, deferral, reversibility, dependency | `PARTIAL` | Sensemaking compares consequences qualitatively but does not define a generic forecast/simulation stage. |
| **Decision** | Level-2/3/4 scope-appropriate decision vocabularies | `EXACT` as a role, `NON_EQUIVALENT` as one universal type | Sensemaking deliberately preserves scope-specific decision semantics rather than one enum or authority class. |
| **Action** | bounded Skill/tool/engineering work; Level-2/Level-1 execution | `DOMAIN_SPECIALIZATION` | Sensemaking action is primarily software/repository work. General Agency action is any authorized intervention. |
| **Reality** | repository/product/external evidence-producing environment | `PARTIAL` | Sensemaking treats repositories, tools, tests, users, and external systems as evidence sources but does not model a generic environment object. |
| **Observation** | source-grounded Observation | `EXACT` | The distinction between observation and semantic conclusion is already explicit. |
| **Verification** | validators, qualification, claim-specific verification, evidence admission | `PARTIAL` | Sensemaking explicitly limits mechanical validation to mechanical facts, while broader verification can be semantic, empirical, stochastic, or human-reviewed. |
| **Impact Assessment** | semantic result evaluation; goal/responsibility/strategic-decision closure checks | `PARTIAL` | Sensemaking asks whether results actually satisfied the responsibility/goal/strategic rationale, but does not expose “impact assessment” as one general primitive. |
| **Sensemaking** | agent semantic result judgment and reconciliation | `DOMAIN_SPECIALIZATION` | This is central to the product, but its current domain is repository/product decision support. |
| **Belief Update** | claim revision, uncertainty update, strategic adjudication, STATUS/Campaign reconciliation | `PARTIAL` | Sensemaking updates durable decision state and claims, not a generic agent-wide belief store. |
| **Memory / Provenance substrate** | Campaign state, evidence, handoff/resume, STATUS, target identity, provenance/currentness, transition history, ADRs | `DOMAIN_SPECIALIZATION` | Sensemaking already has mature durable decision memory. v0.1 clarifies that persistence is a substrate read/written across cycles rather than a universal late phase. |
| **Knowledge Externalization / Communication** | ADRs, handoffs, repository artifacts, Campaign projections, reports, Skills/reference docs, STATUS/reconciliation records | `DOMAIN_SPECIALIZATION` | Sensemaking externalizes selected decision-relevant knowledge in domain-specific artifacts. Durable state exists != knowledge is sufficiently transferable. |
| **Search State** | Campaign evidence/history, uncertainty history, strategic alternatives, handoff records, repository history | `PARTIAL` | Current surfaces can reconstruct material search history when preserved, but Sensemaking does not define a generic search-state object or search-tree database. |
| **Adaptive Capability Activation** | adaptive guidance, lightest-process rule, Campaign conditionality, challenge/exploration triggers, minimum necessary ascent, smallest warranted intervention | `EXACT` as a control principle | Sensemaking already treats available capabilities as conditional rather than mandatory process. The general concept is broader, but the control law closely matches. |
| **Authority / Governance** | Authority semantics; lower-level delegation law; owner-reserved Level-4 decisions | `EXACT` as a control principle | Sensemaking strongly separates semantic judgment, capability, authorization, and ratification. |
| **Risk / Consequence** | consequence-of-error, reversibility, deferral cost, blocking power, evidence ceilings | `PARTIAL` | These lenses exist, but there is no universal risk envelope or deterministic risk score. |
| **Resources / Attention** | cheapest sufficient evidence; smallest warranted intervention; compute/resource authority in transfer research | `PARTIAL` | Sensemaking reasons about bounded cost and intervention size but not generic cognitive-budget allocation. |
| **Constraints** | authority boundary, product boundary, dependency, external blockers, compatibility/evidence constraints | `PARTIAL` | Constraints are present in several domain-specific forms rather than one general constraint model. |
| **Time Horizon** | deferral cost, continuation state, product-thesis slower cadence | `PARTIAL` | Temporal reasoning is present but not a general explicit horizon layer. |
| **Reversibility / Commitment** | reversibility lens; owner ratification; dependency-sensitive holds | `PARTIAL` | Sensemaking uses reversibility in strategic comparison but does not generalize commitment dynamics across domains. |
| **Adversarial Challenge** | contradiction detection, counter-evidence, invalidation evidence, falsification studies, review | `PARTIAL` | The ingredients exist, but a generic `Challenge(X)` operator across value/strategy/frame/belief/option/interpretation is not canonical. |
| **Exploration / Alternative Generation** | Strategic Frontier, candidate directions, bounded alternatives, competing uncertainties/responsibilities | `PARTIAL` | Sensemaking can preserve and compare alternatives, but does not define exploration as a general lateral operator. |
| **Exploration Policy** | PAA exploration triggers/stopping, using-sensemaking challenge/exploration guidance, Strategic Frontier alternatives, repeated-failure reassessment, resource-aware stopping | `PARTIAL` | Existing guidance helps decide when to broaden search and when to stop, but it does not clearly distinguish iterative search-allocation choices such as exploit, explore, diagnose, recombine, restart, or verify. |
| **Value Revision** | Level-4 Product Thesis / Strategy Revision | `DOMAIN_SPECIALIZATION` | Level 4 revises the product thesis, not arbitrary normative value systems. |

## 5. Explicit non-equivalences

The crosswalk is only useful if it preserves boundaries.

### 5.1 General value != Level-4 product strategy

Level 4 contains value-bearing product commitments, but General Agency “value” may concern any domain, stakeholder set, right, mission, or normative commitment.

### 5.2 General action != repository mutation

Action may be investigation, communication, resource allocation, publication, waiting, escalation, or physical intervention.

### 5.3 General memory != Campaign State

Campaign State is one domain-specific durable control structure. A general agent may require other memory forms.

### 5.4 Knowledge externalization != documentation phase

A documentation workflow may use observation, verification, sensemaking, externalization, provenance, governance, and sufficiency. The general model does not require a universal vertical documentation phase.

### 5.5 Knowledge externalization != store every thought

```text
reasoning result
!= durable artifact required
```

Externalize only when continuation, transfer, governance, rediscovery cost, operations, or future search quality makes persistence valuable.

### 5.6 Exploration operator != Exploration Policy

```text
exploration operator
-> generates or discovers alternatives

Exploration Policy
-> allocates effort across search modes once iterative search is warranted
```

### 5.7 Exploration Policy != Strategic Frontier ranking

Exploration Policy is a semantic search-allocation concept, not deterministic ranking, scoring, or backlog priority.

### 5.8 Search State != Campaign schema

Search State is a decision-relevant projection of memory/provenance for a current investigation. Campaign is one repository-domain durable control structure; neither implies a universal search schema.

### 5.9 Search State != hidden chain-of-thought

Persist reconstructible explicit decision/search state when warranted, never private reasoning traces.

### 5.10 Adaptive Capability Activation != deterministic routing

The active semantic controller decides which capability is warranted. The principle does not authorize automatic Skill/workflow selection.

```text
Available capability != selected capability
```

### 5.11 General decision != authorization

Sensemaking already provides the stronger law:

```text
recommendation != selection
selection != authorization
authorization != ratification
```

The General Agency Model must preserve this separation.

### 5.12 General strategy != `StrategicPlanner`

A semantic strategy concept does not justify a deterministic planning engine.

### 5.13 General agency != autonomous authority

Capability to reason about a decision does not grant legitimate authority to make or execute it.

### 5.14 General verification != validator PASS

Mechanical validation establishes declared invariants. It does not automatically establish semantic truth, causal attribution, strategic correctness, or value creation.

### 5.15 General option generation != Strategic Frontier ranking

The Strategic Frontier is decision-relevant possibility state, not a backlog or automatically ranked option set.

### 5.16 General learning != model weight update

Learning in this model includes belief, state, policy, strategy, or commitment revision. It does not imply online parameter training.

### 5.17 General context != exhaustive ontology

Both the Semantic Reasoning Model and the General Agency Model favor decision-bounded representation over exhaustive world modeling.

## 6. Prior domain-transfer evidence

Path 4 already tested whether selected Sensemaking control concepts survive a domain substitution from software engineering to AI research.

Its proposed `TRANSFER_COHERENT` result found bounded support for:

- decision-changing uncertainty outside repository vocabulary;
- evidence-bounded claims under stochastic evidence;
- evidence/authority separation;
- decision/orchestration separation.

This crosswalk therefore does **not** repeat the claim “some Sensemaking control principles may transfer.”

The new question is broader:

> Do the transferred principles fit coherently inside a larger value-to-action-to-learning architecture without forcing Sensemaking to become that architecture as a product?

The stress tests below target that question.

## 7. Stress test A — trivial reversible task

### Situation

A developer asks:

> Rename a clearly identified local symbol and update its direct references.

The correct solution path is already known. The change is cheap, reversible, low consequence, and mechanically verifiable.

### General Agency reading

```text
Value/Purpose:
preserve intended code behavior while completing the requested rename

Context:
scope is already bounded

Decision Frame:
perform the rename or not

Epistemic State:
sufficient

Sufficiency Gate:
YES

Option Space:
rename as requested / decline only if a discovered contradiction blocks it

Action:
edit references

Observation/Verification:
tests/static checks/review as appropriate

Belief Update:
normally none beyond completion evidence
```

### Sensemaking reading

Current product strategy explicitly identifies obvious small deterministic tasks as an anti-persona for added Sensemaking ceremony.

### Result

**PASS — the parent model compresses rather than expands the workflow.**

The General Agency Model does not require every conceptual node to become visible process.

This is important evidence against interpreting the model as a mandatory runtime state machine.

## 8. Stress test B — ambiguous repository goal

### Situation

A repository owner says:

> Improve this repository's architecture.

No specific responsibility or failure boundary is identified.

### General Agency reading

The agent must establish:

1. value/purpose: what architectural improvement should accomplish;
2. context: current repository/product structure and constraints;
3. decision frame: which consequential architecture decision is actually blocked;
4. epistemic state: what evidence exists;
5. decision-relevant uncertainty: what could change the responsibility;
6. metareasoning: what bounded investigation is worth performing;
7. option space: repair, simplify, retire, reconcile, preserve, or no change;
8. action only after a warranted responsibility is selected;
9. verification and impact assessment after intervention;
10. belief/strategic reconciliation.

### Sensemaking reading

This maps strongly to:

- repository sensemaking;
- evidence catalog and claims;
- decision being supported;
- consequential uncertainty;
- warranted responsibility;
- authority inspection;
- bounded work;
- semantic result evaluation;
- durable reconciliation where warranted.

### Result

**PASS — strong domain-specialized correspondence.**

The General Agency Model explains the wider logic, while the Semantic Reasoning Model provides the more precise repository evidence-to-decision grammar.

No new runtime concept is required by this case.

## 9. Stress test C — strategic repository evolution

### Situation

After completing a milestone, the owner asks:

> What repository-level change is warranted next, if any?

Several plausible directions exist.

### General Agency reading

Relevant concepts are:

- value/purpose;
- current context;
- strategic model;
- decision frame;
- option space;
- forecast/evaluation;
- decision-relevant uncertainty;
- sufficiency;
- authority;
- smallest sufficient action;
- evidence-driven reassessment.

### Sensemaking reading

Level 3 already defines:

- Strategic Frontier;
- Strategic Decision to Support;
- qualitative candidate-boundary comparison;
- decision-changing uncertainty;
- smallest warranted intervention;
- bounded Level-2/1 execution;
- strategic adjudication;
- explicit no-change/stop outcomes.

### What the General Agency Model adds conceptually

Two concepts become more explicit:

1. **Option generation** — the frontier is not only a set to compare; the quality and diversity of candidate boundaries can itself matter.
2. **Forecast/evaluation** — current qualitative lenses can be understood as domain-specific outcome/reversibility/decision-value reasoning.

### Boundary

That clarification does **not** justify:

- automatic Strategic Frontier generation;
- numeric priority scoring;
- deterministic ranking;
- `StrategicPlanner`;
- automatic Campaign creation.

### Result

**PASS — General Agency provides explanatory parent concepts for behavior Level 3 already largely performs.**

The additions are conceptual clarifications, not current implementation requirements.

## 10. Stress test D — product-thesis contradiction

### Situation

Repeated repository/product evidence begins to indicate that a ratified product commitment may no longer match the actual user/problem or product behavior.

### General Agency reading

Bottom-up evidence propagates through:

```text
OBSERVATION
-> VERIFICATION
-> SENSEMAKING
-> BELIEF UPDATE
-> STRATEGIC CONTRADICTION
-> selective ascent
-> VALUE / PURPOSE REVIEW
```

The minimum-necessary-ascent rule says not to revise purpose until lower-level explanations are insufficient.

### Sensemaking reading

This maps directly to:

- Thesis Tension for repeated but not-yet-decision-changing signals;
- `THESIS_REVIEW_REQUIRED` when a Level-4 commitment becomes decision-changing;
- affected commitment + evidence + alternatives;
- owner ratification where reserved;
- `REAFFIRM / REINTERPRET / REVISE / RETIRE / SUPERSEDE`;
- mandatory Level-3 reconciliation afterward.

### Result

**PASS — the General Agency upward-learning model explains why Level-4 revision exists, while Sensemaking provides stronger domain governance and authority semantics.**

The parent model must inherit, not weaken, the rule that evidence sufficiency does not automatically grant authority to revise values or product commitments.

### v0.1 additional stress case E — repeated iterative search

#### Situation

Several implementation approaches have been tried. Some improved the result, one failed for unclear reasons, and the current best may be a local optimum.

#### General Agency v0.1 reading

```text
Memory / Provenance
-> reconstruct attempts and outcomes
-> Search State projection
-> Exploration Policy
-> exploit / explore / diagnose / challenge / recombine / restart / verify
-> next bounded investigation
-> evaluation
-> search-state update
```

#### Sensemaking reading

Current PAA/using-sensemaking guidance already supports repeated-failure reassessment, exploration triggers, challenge, and resource-aware stopping. It does not yet clearly name search-allocation modes.

#### Result

**PASS — v0.1 explains iterative-search control without requiring a search runtime or persistent search tree.**

### v0.1 additional stress case F — fresh-agent continuation of prior search

#### Situation

A new agent must continue consequential work after several prior attempts.

#### General Agency v0.1 reading

```text
Memory / Provenance
-> externalize selected decision/search knowledge
-> future actor reconstructs current state
-> Exploration Policy allocates next search effort
```

#### Sensemaking reading

Campaign/handoff/STATUS/artifact surfaces already provide domain-specific continuity when continuation complexity warrants it.

#### Result

**PASS — existing durable surfaces are plausible domain specializations; no generic memory engine follows.**

### v0.1 additional stress case G — documentation-heavy release workflow

#### Situation

A release requires accurate runbooks, user guidance, decision provenance, and verified operational instructions.

#### General Agency v0.1 reading

Documentation is a specialized subcycle using observation, verification, sensemaking, Knowledge Externalization / Communication, provenance, governance, and sufficiency.

#### Sensemaking reading

ADRs, handoffs, release artifacts, documentation-currentness checks, and repository qualification already distribute these functions across current surfaces.

#### Result

**PASS — Knowledge Externalization clarifies the function without adding a universal `DOCUMENTATION` lifecycle node.**

## 11. Candidate explanatory gaps

The stress tests and crosswalk expose several places where the General Agency Model is more explicit than current Sensemaking.

These are **research gaps**, not product backlog items.

### 11.1 Explicit option generation

**Current Sensemaking support:** Strategic Frontier candidates, bounded Level-4 alternatives, competing uncertainties/responsibilities.

**General-model addition:** option-set quality itself can bound decision quality.

**Why this may matter:** a system can compare available options correctly while missing the best option entirely.

**Implementation warrant would require:** repeated normal-use evidence that agents prematurely converge because existing guidance fails to surface materially better alternatives.

**Current disposition:** conceptual only.

### 11.2 Explicit forecast / simulation semantics

**Current Sensemaking support:** qualitative comparison lenses, expected decision effect, consequence of error, deferral, reversibility.

**General-model addition:** candidate actions may need explicit predicted consequence models before selection.

**Implementation warrant would require:** recurring decisions where current qualitative comparison cannot reconstruct why an option was expected to create value or avoid harm.

**Current disposition:** conceptual only.

### 11.3 Generic adversarial operator

**Current Sensemaking support:** contradiction, counter-evidence, invalidation evidence, falsification studies, review.

**General-model addition:** structured challenge can target values, frames, beliefs, questions, methods, options, forecasts, and interpretations.

**Implementation warrant would require:** repeated high-consequence errors traceable to unchallenged assumptions that existing evidence/uncertainty discipline does not catch.

**Current disposition:** conceptual/operator guidance candidate only.

### 11.4 Generic exploration operator

**Current Sensemaking support:** candidate directions, Strategic Frontier, bounded alternatives.

**General-model addition:** exploration is distinct from criticism; it searches for unrepresented frames/options.

**Implementation warrant would require:** evidence of premature local convergence across consequential repository decisions.

**Current disposition:** conceptual only.

### 11.5 Exploration Policy / search allocation

**Current Sensemaking support:** exploration triggers/stopping, repeated-failure reassessment, Strategic Frontier alternatives, resource-aware stopping, challenge/exploration guidance.

**General-model addition:** distinguish alternative generation from the policy that allocates iterative search among exploit, explore, diagnose, adversarial challenge, recombination, restart, and verify.

**Implementation warrant would require:** repeated consequential search failures traceable to poor search allocation that current guidance cannot absorb.

**Current disposition:** research/guidance candidate only; no runtime, scoring model, or search-tree persistence warranted.

### 11.6 Knowledge Externalization / Communication

**Current Sensemaking support:** ADRs, handoffs, artifacts, reports, Campaign projections, STATUS, Skills/reference docs.

**General-model addition:** make transferability distinct from mere storage and state explicitly when durable externalization is worth its cost.

**Implementation warrant would require:** repeated rediscovery, continuation, audit, or operational-transfer failures that current artifacts/guidance do not prevent.

**Current disposition:** domain-specialized support is strong; possible bounded guidance clarification only.

### 11.7 Search State projection

**Current Sensemaking support:** evidence/transition history, uncertainty history, strategic alternatives, handoffs, repository history.

**General-model addition:** a current-investigation view over attempts, outcomes, promising/abandoned branches, failure attribution, and remaining budget.

**Implementation warrant would require:** repeated inability to reconstruct decision-relevant search history using existing surfaces.

**Current disposition:** no generic schema/database warranted.

### 11.8 Adaptive Capability Activation

**Current Sensemaking support:** lightest-process guidance, Campaign conditionality, challenge/exploration triggers, smallest warranted intervention, minimum necessary ascent, resource-aware stopping.

**General-model addition:** name the common control principle that available capability != warranted activation.

**Implementation warrant would require:** repeated over-activation or under-activation that current guidance cannot absorb.

**Current disposition:** strong existing control-law correspondence; implementation need not assumed.

### 11.9 Resource-aware metareasoning

**Current Sensemaking support:** cheapest sufficient evidence, smallest warranted intervention, decision cost, deferral cost, resource authority in transfer cases.

**General-model addition:** reasoning itself consumes scarce resources and should be governed by expected decision improvement versus reasoning/information/delay cost.

**Implementation warrant would require:** recurring over-investigation or under-investigation that materially harms delegation quality.

**Current disposition:** principle-level clarification only; no scoring model warranted.

### 11.10 Explicit impact assessment

**Current Sensemaking support:** semantic result evaluation distinguishes capability completion, responsibility satisfaction, goal achievement, strategic decision resolution, and thesis validation.

**General-model addition:** make the distinction between proxy success and actual value creation explicit.

**Implementation warrant would require:** repeated cases where repository qualification is mistaken for user/product impact despite existing evidence ceilings.

**Current disposition:** conceptual clarification; current evidence-ceiling language already mitigates much of the risk.

### 11.11 General persistent-state abstraction

**Current Sensemaking support:** Campaign state, STATUS, handoff/resume, provenance/currentness, strategic projection.

**General-model addition:** a domain-independent account of commitments, beliefs, evidence, decisions, unresolved uncertainty, and intervention history.

**Implementation warrant would require:** a concrete non-repository consumer or a proven cross-domain product boundary.

**Current disposition:** no generic schema/database warranted.

## 12. What the parent model explains that Sensemaking leaves distributed

Current Sensemaking already contains most of the underlying control principles, but they are intentionally distributed across models with different responsibilities.

The General Agency Model adds value primarily by explaining their **relationship**:

```text
VALUE determines what outcomes matter.
        |
CONTEXT determines what situation those values apply to.
        |
STRATEGY identifies where intervention may matter.
        |
DECISION FRAME identifies the commitment actually at stake.
        |
EPISTEMIC STATE determines what is known.
        |
SUFFICIENCY determines whether inquiry is worth more than action.
        |
METAREASONING chooses how to reduce relevant uncertainty.
        |
OPTIONS + FORECASTS make action selection explicit.
        |
ACTION changes reality.
        |
OBSERVATION + VERIFICATION constrain what can be claimed.
        |
IMPACT + SENSEMAKING determine what the outcome means.
        |
BELIEF UPDATE may propagate upward only as far as warranted.
```

Sensemaking already implements or documents many domain-specific pieces of this relation.

The parent model's main contribution is **integration and abstraction**, not proof that missing runtime components should be built.

## 13. Relationship to the Four-Level Control Model

The General Agency lifecycle can operate at different control scopes.

For example, a Level-3 repository strategy decision and a Level-4 product-thesis decision can both involve:

- context;
- epistemic state;
- uncertainty;
- alternatives;
- evaluation;
- evidence;
- belief revision.

But:

```text
same agency grammar
!= same control scope
!= same authority
```

The Four-Level Control Model therefore remains necessary.

The General Agency Model cannot replace it without losing explicit decision-scope and authority ownership.

## 14. Relationship to the Semantic Reasoning Model

The Semantic Reasoning Model is more precise about how repository/product evidence becomes bounded semantic judgment:

```text
Observation
-> Evidence
-> Claim
-> EpistemicStatus
-> Contradiction / Uncertainty
-> DecisionBeingSupported
-> Responsibility
-> Capability
-> Artifact / Change / Evidence
-> Validation
-> Decision
-> Durable reconciliation
```

The General Agency Model is broader because it starts earlier and ends later:

- before evidence: value, context, strategy, option generation;
- around reasoning: metareasoning, exploration, challenge, forecast;
- after result: impact assessment and possible higher-level belief/strategy/value revision.

Therefore:

> **General Agency Model contains a broader agency grammar; the Semantic Reasoning Model remains the stronger evidence-to-decision grammar inside Sensemaking.**

## 15. Relationship to software-factory orchestration

The existing Path 3 principle remains intact:

> **Decision selects the work. Orchestration coordinates the work. Evidence determines what becomes warranted next.**

A software factory can coordinate:

- workers;
- queues;
- repositories;
- retries;
- tool calls;
- CI;
- artifact movement;
- scheduled execution.

The General Agency Model does not imply that Sensemaking should own those mechanics.

A factory may host or call a Sensemaking-informed agent, but:

```text
agency semantics != worker scheduling
decision control != orchestration control
semantic state != job queue state
```

## 16. Bounded Level-4 assessment

### Research disposition: `REINTERPRET_CANDIDATE` remains coherent

General Agency Model v0.1 strengthens the research interpretation that Sensemaking can be understood as a software-engineering-domain realization of a broader value-directed agency model.

The refinement does **not** require a canonical Level-4 revision:

- product purpose remains unchanged;
- primary user and JTBD remain unchanged;
- ADR 0029 remains coherent and authoritative;
- strategic non-goals against generic agent runtime and automatic semantic planning remain valid;
- no new product/value contradiction is introduced.

### Is immediate Level-4 canonical revision required?

**No.**

v0.1 is a research/reference refinement. Product strategy and ADR 0029 remain unchanged unless later normal-use evidence creates a decision-changing thesis tension.

## 17. Relationship to existing Practical Agent Architecture v0

Practical Agent Architecture v0 already exists and is guidance-first.

v0.1 should therefore be reconciled against it rather than used to justify a new architecture package automatically.

Current likely relationships are:

```text
Memory / Provenance substrate
-> existing durable decision substrate

Knowledge Externalization
-> existing ADR/artifact/handoff/report surfaces + possible guidance clarification

Exploration Policy
-> extends current exploration-trigger/stopping guidance conceptually

Search State
-> projection over existing evidence/history unless repeated reconstruction failure proves otherwise

Adaptive Capability Activation
-> existing ceremony-scaling / progressive-disclosure control law
```

This crosswalk does **not** establish a Practical Agent Architecture v1 need.

## 18. Reconciliation questions for the implementation gate

The next repository-specific reconciliation should decide:

1. Does current Sensemaking already provide a domain specialization for each v0.1 concept?
2. Is any remaining gap explanatory/guidance-only?
3. Does repeated normal-use evidence establish a durable-state gap?
4. Is any missing requirement mechanically decidable?
5. Would implementation violate ADR 0029 or evidence ceilings?
6. Does the smallest intervention preserve progressive disclosure and low ceremony?
7. Does Exploration Policy require anything beyond model-owned guidance?
8. Does Search State require persistence beyond existing evidence/history surfaces?
9. When should Knowledge Externalization become explicit rather than remain ephemeral?
10. Does Adaptive Capability Activation need new wording or is it already operationally clear?

## 19. Final bounded conclusion

### 19.1 Conceptual evolution remains natural

The v0.1 additions sharpen rather than redirect the existing trajectory:

```text
repository observation
-> evidence
-> uncertainty
-> warranted responsibility
-> Campaign continuation
-> Strategic Repository Evolution
-> Product Thesis revision
-> broader value-directed agency
```

### 19.2 Product expansion remains unwarranted

A clearer memory/search/externalization model does not imply a general agent product, generic memory system, or search runtime.

ADR 0029 remains authoritative.

### 19.3 The next useful step is reconciliation, not machinery

```text
v0.1 research model clarified
        |
v0.1 crosswalk coherent
        |
existing PAA/Sensemaking surfaces inspected
        |
per-concept implementation dispositions assigned
        |
guidance changes only if a concrete gap is established
        |
runtime/schema/product changes NOT AUTOMATIC
```

The proper next artifact is `general-agency-model-v0.1-reconciliation.md`.