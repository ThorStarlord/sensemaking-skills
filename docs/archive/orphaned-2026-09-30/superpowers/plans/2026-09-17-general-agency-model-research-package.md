# General Agency Model v0 Research Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Produce the two approved research artifacts that define the General Agency Model v0 and reconcile it against current Sensemaking semantics without changing product authority or runtime behavior.

**Architecture:** Keep the General Agency Model as a non-authoritative parent/reference model. Package 1 defines the domain-independent value-to-action-to-learning grammar; Package 2 maps that grammar against the current Four-Level Control Model, Semantic Reasoning Model, Campaign/Responsibility/Authority semantics, prior Path 4 transfer evidence, and ADR 0029, then records bounded stress-test and Level-4 implications.

**Tech Stack:** Markdown documentation, existing Sensemaking canonical/research artifacts, Git/GitHub review.

**Spec:** `docs/superpowers/specs/2026-09-17-general-agency-model-design.md`

## Global Constraints

- ADR 0029 remains the current product-boundary authority.
- The General Agency Model remains research/reference material unless separately ratified.
- Do not introduce a generic agent runtime, planner, scheduler, orchestration engine, universal state database, schema, Skill, or automatic semantic controller.
- Reuse existing Sensemaking vocabulary where meanings already match.
- Record non-equivalence instead of forcing analogies.
- Treat Path 4 `TRANSFER_COHERENT` as prior bounded evidence, not proof of domain-general agency and not a study to repeat.
- Preserve `theory != runtime != product != orchestration environment`.
- Preserve `semantic judgment != mechanical validation` and `capability != authority`.
- Candidate gaps are research findings, not implementation requirements.
- No empirical experiment or release qualification is required for this package.
- Do not edit `docs/product-strategy.md`, `docs/strategic-outer-loop.md`, `docs/semantic-architecture/reasoning-model.md`, `docs/adr/0029-current-product-boundary.md`, or `STATUS.md` as part of Packages 1-2.

---

## File Structure

### Create: `docs/research/general-agency-model-v0.md`

Responsibility: define the domain-independent General Agency Model v0, its scope, terminology, core cycle, directional flows, cognitive operators, control envelopes, persistent state, stopping semantics, adversarial/value-contestation semantics, and evidence ceiling.

### Create: `docs/research/general-agency-sensemaking-crosswalk-v0.md`

Responsibility: reconcile General Agency concepts with current Sensemaking concepts, document exact/partial/non-equivalent mappings, run four bounded conceptual stress tests, identify candidate explanatory gaps, and record a bounded Level-4 implication without changing product authority.

### Modify: draft PR #374 body only if needed after artifacts exist

Responsibility: summarize completed research artifacts and their bounded disposition. Do not mark runtime/product expansion as authorized.

---

### Task 1: Author General Agency Model v0

**Files:**
- Create: `docs/research/general-agency-model-v0.md`
- Read/reference: `docs/superpowers/specs/2026-09-17-general-agency-model-design.md`
- Read/reference: `docs/strategic-outer-loop.md`
- Read/reference: `docs/semantic-architecture/reasoning-model.md`
- Read/reference: `docs/research/domain-general-control-transfer.md`
- Read/reference: `docs/research/path-4-domain-transfer-results.md`
- Read/reference: `docs/research/decision-versus-orchestration.md`
- Read/reference: `docs/adr/0029-current-product-boundary.md`

**Interfaces:**
- Consumes: the approved architectural spec and current Sensemaking terminology.
- Produces: a stable research vocabulary and lifecycle that Task 2 can map against exactly.

- [x] **Step 1: Establish authority and evidence ceiling**

Start the file with:
- status = research/reference only;
- current product boundary unchanged;
- strongest permitted claim = coherent candidate parent model informed by Sensemaking and bounded transfer evidence;
- explicit statement that Path 4 supports transfer of some control concepts but does not establish the full model;
- explicit non-goals against runtime/product expansion.

- [x] **Step 2: Define terminology**

Define, at minimum:
- value / purpose;
- context / situation model;
- strategic model;
- decision frame;
- epistemic state;
- decision-relevant uncertainty;
- sufficiency gate;
- question/inquiry;
- metareasoning;
- option space;
- forecast/evaluation;
- action;
- observation;
- verification;
- impact assessment;
- sensemaking;
- belief update;
- cognitive operator;
- control envelope;
- persistent state.

Each definition must distinguish the concept from adjacent Sensemaking-specific terms where ambiguity is likely.

- [x] **Step 3: Define the core lifecycle**

Include this semantic order:

```text
VALUE / PURPOSE
-> CONTEXT / SITUATION
-> STRATEGIC MODEL
-> DECISION FRAME
-> EPISTEMIC STATE
-> SUFFICIENCY GATE
   -> INQUIRE when evidence is insufficient
   -> CHOOSE when evidence is sufficient
-> OPTION SPACE
-> FORECAST / EVALUATE
-> DECISION
-> ACTION
-> REALITY
-> OBSERVATION
-> VERIFICATION
-> IMPACT ASSESSMENT
-> SENSEMAKING
-> BELIEF UPDATE
-> REASSESS AS WARRANTED
```

State that this is a reasoning relation, not a mandatory runtime state machine or phase-gated workflow.

- [x] **Step 4: Define the three directional movements**

Document:
- top-down control: purpose -> strategy -> decision -> inquiry/choice -> action;
- bottom-up learning: reality -> observation -> verification -> sensemaking -> belief revision;
- lateral cognition: challenge/exploration across current beliefs, frames, options, and interpretations.

State the minimum-necessary-ascent rule for bottom-up evidence.

- [x] **Step 5: Define cognitive operators**

Specify at least:
- adversarial challenge;
- exploration / alternative generation;
- causal reasoning;
- counterfactual reasoning;
- decomposition;
- comparison;
- simulation / forecasting.

Clarify that operators can be invoked at multiple nodes and do not imply separate runtime services.

- [x] **Step 6: Define adversarial review and value contestation**

Include:
- proposal -> challenge -> adjudication -> retain/revise/reject;
- empirical challenge versus normative value contestation;
- challenge intensity should scale with consequence, uncertainty, irreversibility, novelty, and cost.

- [x] **Step 7: Define control envelopes**

Document:
- authority/governance;
- risk/consequence;
- resources/attention/cost of delay;
- constraints;
- time horizon;
- reversibility/commitment.

Explain how envelopes alter sufficiency thresholds, review intensity, action permission, and escalation.

- [x] **Step 8: Define persistent state**

Document:
- goals/commitments;
- beliefs and epistemic status;
- evidence/counter-evidence;
- unresolved uncertainty;
- decisions/rationale;
- provenance/currentness;
- intervention history;
- calibration where appropriate.

Clarify that this is conceptual state, not authorization for a universal state schema/database.

- [x] **Step 9: Define stopping and resource-aware metareasoning**

State:
- zero uncertainty is unnecessary;
- continue reasoning only when expected decision improvement exceeds reasoning cost plus delay/opportunity cost;
- cheap/reversible actions may justify acting under larger uncertainty;
- expensive/irreversible actions should normally require stronger evidence and review.

- [x] **Step 10: Define natural entry modes**

Cover:
- goal-driven entry;
- event-driven entry;
- anomaly/surprise-driven entry;
- pre-existing-decision entry.

State that no single node is the universal runtime start state.

- [x] **Step 11: Record explicit non-goals and strongest permitted claims**

End with:
- no claim of universal intelligence theory;
- no claim of optimality;
- no product-boundary change;
- no automatic value selection;
- no authority transfer;
- no implementation requirement;
- no generic runtime warrant.

- [x] **Step 12: Self-review Task 1**

Verify:
- no unresolved placeholders;
- no use of Sensemaking-specific words as if domain-general unless defined;
- Path 4 is cited as bounded prior evidence, not universal proof;
- lifecycle distinguishes observation, verification, impact, and sensemaking;
- theory/runtime/product/orchestration separation is explicit;
- file does not modify current product authority.

- [x] **Step 13: Commit Task 1**

Commit message:

```text
docs: add General Agency Model v0 research reference
```

---

### Task 2: Author General Agency ↔ Sensemaking Crosswalk v0

**Files:**
- Create: `docs/research/general-agency-sensemaking-crosswalk-v0.md`
- Read/reference: `docs/research/general-agency-model-v0.md`
- Read/reference: `docs/strategic-outer-loop.md`
- Read/reference: `docs/semantic-architecture/reasoning-model.md`
- Read/reference: `docs/product-strategy.md`
- Read/reference: `docs/adr/0029-current-product-boundary.md`
- Read/reference: `STATUS.md`
- Read/reference: `docs/research/path-4-domain-transfer-results.md`

**Interfaces:**
- Consumes: the terminology and lifecycle defined in Task 1.
- Produces: bounded evidence about whether the parent model clarifies current Sensemaking and whether any Level-4 product change is warranted.

- [x] **Step 1: State reconciliation purpose and authority**

Open with:
- research-only status;
- no canonical Sensemaking documents are modified;
- the task is reconciliation, not product revision;
- mapping categories are `EXACT`, `PARTIAL`, `DOMAIN_SPECIALIZATION`, and `NON_EQUIVALENT`.

- [x] **Step 2: Build the concept crosswalk**

Map at least:

| General Agency concept | Sensemaking analogue |
| --- | --- |
| Value / Purpose | Level-4 product purpose / strategy commitments |
| Context / Situation | bounded target/current state / semantic map |
| Strategic Model | Level-3 Strategic Repository Evolution |
| Decision Frame | Strategic Decision to Support / decision being supported |
| Epistemic State | Observation -> Evidence -> Claim -> EpistemicStatus |
| Decision-relevant uncertainty | consequential / decision-changing uncertainty |
| Sufficiency Gate | existing stopping rule |
| Inquiry | evidence-producing responsibility / uncertainty resolution |
| Metareasoning | agent selection of uncertainty, responsibility, capability, evidence path |
| Option Space | candidate boundaries / bounded alternatives, only partially generalized |
| Forecast / Evaluation | qualitative comparison lenses / expected decision effect, partial |
| Action | Level-2/Level-1 bounded work |
| Observation | source-grounded observation |
| Verification | mechanical validation plus claim-specific verification |
| Impact Assessment | partially explicit in semantic result evaluation; not a single current primitive |
| Sensemaking | semantic judgment / decision reconciliation |
| Belief Update | claim/state reconciliation |
| Memory / Provenance | Campaign/STATUS/handoff/provenance |
| Governance / Authority | Authority model + owner-reserved decisions |
| Risk / Reversibility | consequence-of-error / reversibility / deferral lenses |
| Value revision | Level-4 thesis review |

For each row, classify the mapping and explain any scope mismatch.

- [x] **Step 3: Record explicit non-equivalences**

Include at minimum:
- General value != current Level-4 product strategy in every domain.
- General action != repository modification.
- General memory != Campaign State.
- General decision != authorization.
- General strategy != StrategicPlanner.
- General agency != autonomous authority.
- General verification != mechanical validator pass.
- General option generation != Strategic Frontier ranking.
- General learning != automatic model weight update.

- [x] **Step 4: Compare model roles**

State explicitly:

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

Explain why these are complementary rather than replacements.

- [x] **Step 5: Run stress test A — trivial reversible task**

Use a simple change such as renaming a local symbol where the solution path is already known.

Expected finding:
- most outer-loop machinery is bypassed;
- low consequence + low uncertainty + high reversibility makes immediate bounded action warranted;
- theory must not force ceremony.

- [x] **Step 6: Run stress test B — ambiguous repository goal**

Use a goal such as "improve this repository's architecture."

Expected finding:
- context, decision framing, epistemic state, consequential uncertainty, investigation, warranted responsibility, authority, and verification become relevant;
- maps strongly to current Sensemaking.

- [x] **Step 7: Run stress test C — strategic repository evolution**

Use a decision such as "what repository-level change is warranted next?"

Expected finding:
- maps to Level 3;
- option generation/forecasting clarify existing qualitative candidate-boundary comparison but do not justify deterministic ranking.

- [x] **Step 8: Run stress test D — product-thesis contradiction**

Use accumulated evidence suggesting that a current product commitment may be wrong.

Expected finding:
- evidence propagates upward;
- Level 3 cannot silently rewrite Level 4;
- product-thesis review and owner authority remain distinct from evidence sufficiency.

- [x] **Step 9: Identify candidate explanatory gaps**

Record as hypotheses, not roadmap items:
- explicit option generation;
- explicit forecast/simulation semantics;
- generic adversarial operator;
- generic exploration operator;
- resource-aware metareasoning;
- impact assessment;
- general persistent-state abstraction.

For each, state whether Sensemaking already has partial semantics and what concrete future pressure would be needed before implementation is warranted.

- [x] **Step 10: Make bounded Level-4 assessment**

Choose one research disposition from:
- `NO_PRODUCT_CHANGE_INDICATED`
- `REINTERPRET_CANDIDATE`
- `LEVEL_4_REVIEW_WARRANTED`

The expected disposition should be based on evidence from the crosswalk/stress tests rather than assumed in advance.

If `REINTERPRET_CANDIDATE`, state only the research candidate wording:

> Sensemaking remains repository decision support but may be understood as a software-engineering-domain realization of a broader value-directed agency model.

Do not edit canonical Level-4 authority.

- [x] **Step 11: Self-review Task 2**

Verify:
- every mapping points to an existing current concept;
- non-equivalences prevent vocabulary collapse;
- stress tests do not assume their expected finding if the actual mapping contradicts it;
- gaps remain hypotheses;
- Level-4 disposition remains research-only;
- no claim exceeds Path 4 or current product evidence ceilings.

- [x] **Step 12: Commit Task 2**

Commit message:

```text
docs: reconcile General Agency Model with Sensemaking
```

---

### Task 3: Review Package 1 + Package 2 as one bounded research result

**Files:**
- Review: `docs/research/general-agency-model-v0.md`
- Review: `docs/research/general-agency-sensemaking-crosswalk-v0.md`
- Review: `docs/superpowers/specs/2026-09-17-general-agency-model-design.md`
- Review: `docs/superpowers/plans/2026-09-17-general-agency-model-research-package.md`
- Update: draft PR #374 body if final artifact/disposition summary changed materially

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: a reviewable research package and an explicit stop/next-gate decision.

- [x] **Step 1: Spec coverage review**

Check every design section against Packages 1-2:
- terminology;
- core lifecycle;
- directional flows;
- operators;
- control envelopes;
- persistence;
- sufficiency/stopping;
- adversarial reasoning;
- crosswalk;
- non-equivalence;
- stress tests;
- gap analysis;
- Level-4 implications.

- [x] **Step 2: Placeholder and authority scan**

Search for unresolved placeholders and for language that accidentally implies:
- product authority;
- runtime authorization;
- automatic planning/routing;
- universal proof;
- implementation roadmap status.

Correct any violations before completion.

- [x] **Step 3: Cross-document consistency review**

Verify:
- terms in the crosswalk match Task 1 definitions;
- mapping categories are used consistently;
- the Level-4 disposition does not contradict ADR 0029;
- Path 4 evidence ceiling is preserved;
- the General Agency Model does not replace the Four-Level or Semantic Reasoning models.

- [x] **Step 4: Update PR #374 summary**

Add:
- links/paths for both research artifacts;
- bounded disposition;
- candidate gaps;
- explicit statement that no runtime/product-authority change was made;
- next gate: decide whether a separate Practical Agent Architecture v0 design is warranted.

- [x] **Step 5: Stop at the next architectural gate**

Do not create Package 3 implementation/runtime artifacts in this task.

Record the next decision as:

> Does the completed research package warrant designing Practical Agent Architecture v0, and if so, which theoretical concepts need first-class implementation versus remaining reasoning guidance/operators?

- [x] **Step 6: Final commit if review changes were required**

Use a bounded message such as:

```text
docs: close General Agency Model v0 research package
```


---

## Execution Outcome

**Status:** COMPLETE for Packages 1-2.

Created:

- `docs/research/general-agency-model-v0.md`
- `docs/research/general-agency-sensemaking-crosswalk-v0.md`

Research disposition:

- General Agency parent model: coherent candidate research/reference abstraction.
- Sensemaking relationship: `REINTERPRET_CANDIDATE` only; no canonical Level-4 change made.
- ADR 0029/product boundary: unchanged.
- Runtime/product implementation: not authorized.
- Next gate: separate Practical Agent Architecture v0 design, if approved.

Package-wide review found no unresolved placeholders and no product-authority/runtime-boundary contradiction.
