# Adaptive Metareasoning System (AMS) — Product Design v0

**Date:** 2026-11-12
**Status:** Owner-selected first-class intended product capability through [ADR 0036](../../adr/0036-adaptive-metareasoning-system.md). Design is not evidence of behavioral improvement.
**Planning baseline:** ThorStarlord/sensemaking-skills at main c644323abab5f9ca7808f1f2369b2ccb22286828. Refresh source and authority before execution.
**Implementation companion:** [AMS development plan](../plans/2026-11-12-adaptive-metareasoning-system.md).

## 1. Product outcome and beneficiaries

**AMS** is Sensemaking's agent-native cognitive regulation capability. Its purpose is to make current decisions more appropriate to the governing goal, rather than merely make reasoning more elaborate. It recognizes the intellectual problem, detects a consequential mismatch between purpose, question, method and progress, and selects proportionate subsequent action or inquiry.

The active coding agent benefits from choosing the right intellectual work. The owner benefits from better-grounded decisions with less ceremony and agenda drift. A future agent benefits from reconcilable material question/method changes; the maintainer can assess and refine AMS using authentic episodes.

**Success:** Better warranted allocation of reasoning and engineering effort, including justified continued use of a method, direct ACT or STOP. More mode switching, alternatives, records or PRs are not measures of success.

## 2. Prior capability and actual gap

Already available:
- The one public agent-owned controller [using-sensemaking](../../../skills/using-sensemaking/SKILL.md), governed by ADR 0034.
- [Metareasoning Policy v0](../../../skills/using-sensemaking/references/metareasoning-policy-v0.md): ACT, INQUIRE, CHALLENGE, EXPLORE, VERIFY, ESCALATE, STOP.
- [Adaptive Policy Coordinator](../../../skills/using-sensemaking/references/adaptive-policy-coordinator-v0.md), Inquiry, Exploration, Warrant/Choice and [Learning/Reconciliation](../../../skills/using-sensemaking/references/learning-reconciliation-policy-v0.md).
- [Cognitive Orientation Crosswalk](../../semantic-architecture/cognitive-orientation-crosswalk-v1.md), Prospective Reasoning and the source-grounded divergent/abductive conceptual vocabularies.
- Existing semantic knowledge records, exact-revision retrieval, source context, session receipts and bounded observability.
- [SCL ADR 0035](../../adr/0035-sensemaking-continuous-learning.md), with lesson discovery, retrieval, and episode learning guidance.

The unresolved product gap is *demonstrated, appropriately reliable application* of these capabilities in authentic consequential reasoning. A prior diagnostic established insufficient evidence, not a demonstrated need for a new schema/controller. The Level-4 owner decision now supplies a separate warrant to improve the intended capability, not a presumption that any chosen implementation is effective.

## 3. Architectural choice and responsibilities

**Single semantic controller:** using-sensemaking is the sole decision maker. AMS is the cognitive-regulation capability of that controller, not a second actor or new mandatory policy layer.

**Existing policies:** produce qualitative candidate questions and control moves. They can remain implicit for easy tasks.

**Existing specialist Skills:** perform bounded inquiries, challenges, exploration, construction and verification as selected and authorized. No Skill automatically routes or selects another.

**Knowledge subsystem:** supplies explicit source-linked claims and applicability candidates. Retrieval and validation do not establish semantic truth or choice.

**SCL:** selectively retains and offers experience from other episodes; AMS checks the precedent and may use, adapt or reject it. AMS does not automatically promote episodes to doctrine.

**Execution and authority:** current target repo and human owner remain controlling. No lesson imports permission.

Illustrative flow, not a runtime pipeline:

~~~
CURRENT GOAL / SCOPE / EVIDENCE
  -> cognitive orientation: what question and why?
  -> question + method fitness when consequential
  -> smallest useful control move
  -> bounded task / inquiry / justified stop
  -> actual evidence
  -> current decision reconciliation
  -> SCL learning consideration if material
  -> future AMS decision, if one exists
~~~

## 4. Competency contract

| Capability | Consequential question | Desired observable behavior | Negative boundary |
| --- | --- | --- | --- |
| AMS-C1 Orientation | What problem and operation are we addressing? | Ground task, goal, target and authority; choose appropriate intellectual operation | Do not replace repository-wide intent with a favorite local code task |
| AMS-C2 Purpose/question fitness | Does our question still serve the governing purpose? | Retain a valid question, correct an invalid frame, or distinguish a newly opened question | A new curiosity does not automatically become the goal |
| AMS-C3 Reflective monitoring | Is apparent progress decision-relevant? | Detect a real purpose/progress mismatch when it matters | No mandatory reflective loop or progress score |
| AMS-C4 Diagnostic discrimination | What best explains observed inadequacy? | Separate source, inference, method, question, composition, host, tool and authority causes | Poor result does not itself prove bad method |
| AMS-C5 Adaptive control | What next move adds sufficient value at acceptable cost? | ACT/INQUIRE/CHALLENGE/EXPLORE/VERIFY/ESCALATE/STOP or minimal correction | No automatic method switching |
| AMS-C6 Economy and stability | Is further thought worth its opportunity cost? | Direct action/stop for obvious work; proportionate deeper reasoning for consequential ambiguity | No fixed quota, scheduler, mandatory critic or Campaign |
| AMS-C7 Learning-informed adaptation | Does historical method experience actually apply? | Source-check, consider exclusions, use/adapt/reject a lesson in current context | No authority transfer or automatic method rule |

When the question is clear and evidence sufficient, only AMS-C5's implicit ACT may be visible. Coverage does not require showing all seven capabilities in every run.

## 5. Critical distinctions and causal limits

### A. Misleading progress vs valid narrow work

A technically correct solution can miss a higher governing purpose. Inspect the original target, user benefit, source evidence and relevance before classifying the work. A deliberately bounded local task may be exactly right; technical detail is not itself drift.

### B. Bad method vs bad evidence, question or environment

One unsuccessful outcome does not identify a cognitive cause. Consider only plausible rival explanations whose resolution could change the response. Host failure or unavailable permissions must not be diagnosed as a methodology defect.

### C. Corrective reframing vs productive question evolution

- **Correction:** the previous frame/premise was inadequate; preserve what remains valid and correct the question.
- **Evolution:** the previous question and its answer remain valid; a separate consequential question emerges and is independently warranted.
- **Tangent:** a new but currently non-consequential idea does not justify scope expansion.

Use existing InquiryQuestion, ExplorationFrame, source-grounded hypotheses and attributed transformation accounts; no new record type is warranted.

### D. Historical learning vs current decision authority

A past episode may help AMS but never binds its current decision. Retained, retrieved, source-checked, decision-informing, outcome-supported and comparatively beneficial are separate evidence classes. An appropriate rejection may be successful use.

## 6. User-facing initial vertical

Through the existing using-sensemaking entrypoint, an owner may ask the agent to orient to purpose, check whether question/method fit remains adequate, choose the next action under evidence/cost/authority and continue with useful work. A narrow task can simply proceed without extra diagnostic narration. Use the [human first-use guide](../../../GETTING_STARTED.md) for a real prompt.

This *available interaction*, once documented, proves a discoverable invocation path. It does **not** prove an independent later agent will load, use or benefit from the guidance. Host loading and effect require their own evidence.

## 7. Maturity / acceptance

**A — Represented:** the repository's existing concepts express the responsibility without conflating method, question, knowledge and authority.

**B — Accessible:** an agent or user can find the applicable policy/reference and execute existing code/tools when relevant.

**C — Authentic behavior observed:** a real agent's available primary evidence shows an appropriate cognitive decision, correction, restraint or stop, with actual task outcome. A retrospective account alone is insufficient.

**D — Benefit qualified:** appropriately independent or comparative evidence supports a material decision improvement at acceptable cost; this is not implied by A-C.

Review genuine cases covering: an obvious local task, fluent but irrelevant progress, ambiguous failure cause, a correct answer opening a new question, an attractive tangent, a relevant SCL lesson and an authority boundary. Do not fabricate trials to fill a checklist. Preserve genuine negative and ambiguous cases.

## 8. Safeguards and explicit non-goals

No duplicate controller, generic MetareasoningEngine, numerical cognitive ranker, state database, automatic Skill activation, mandatory checkpoints, private chain-of-thought capture, blanket logging, automatic policy/Skill modification, model training, unrelated repository mutation, autonomous product-thesis or release action.

Any later deterministic assistance requires a concrete named consumer, stable mechanically decidable operation, existing contract check, safe fallback, proportional verification and independent authority.

## 9. Revision triggers

Revisit the design if authentic repeated work shows relevant guidance is not delivered at a consequential decision, a specific question/method confusion changes an outcome, actual consumers cannot reconstruct necessary evidence, or qualified AMS behavior creates disproportionate overhead or authority failures.

An absence of traces remains NOT_ASSESSED, not proof that cognition failed or that a new runtime is needed.
