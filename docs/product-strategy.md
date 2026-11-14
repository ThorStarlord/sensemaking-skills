# Sensemaking Skills Product Strategy

**Status:** owner-ratified intended product thesis and strategic authority; empirical claims retain source evidence ceilings  
**Updated:** 2026-11-13  
**Control level:** Level 4 — Product Thesis / Strategy Revision  
**Scope:** public repository strategy; empirical claims retain the ceilings of their source evidence

This document answers what Sensemaking Skills is trying to make valuable. It is
the current Level-4 product-thesis authority surface. It does not replace ADRs,
artifact contracts, validators, dated research, or the Level-3 operational state
in `STATUS.md`.

Major strategy changes follow
[`product-thesis-revision.md`](product-thesis-revision.md). Repository-level
execution of this strategy is governed by the Strategic Repository Evolution
Loop in [`strategic-outer-loop.md`](strategic-outer-loop.md).

The 2026-09-11 Persona & Adaptive Guidance Model v0 clarification is an
owner-ratified Level-4 `REINTERPRET`, not a product-category pivot. Its design
preflight is [`persona-adaptive-guidance-design-preflight.md`](persona-adaptive-guidance-design-preflight.md).

The 2026-09-11 Product Boundary Reconciliation v1 is an owner-ratified Level-4
`SUPERSEDE`: ADR 0029 is now the current product-boundary authority, while ADR
0014 remains historical evidence for the narrower July 2026 boundary.

## 1. Product purpose

Sensemaking's **owner-ratified fundamental purpose** is to serve as a **domain-general cognitive substrate for the continuous development of intelligent agents**. Its primary users are intelligent agents across software engineering, scientific research, creative practice, education and other domains, with equal conceptual standing even when current implementations differ.

Sensemaking intends to enable **persistent, reflective, increasingly capable and independent cognitive agency** through the functional integration of knowledge, prospective discovery, reflective value formation, adaptive metareasoning, learning and cognitive continuity. An active host agent, not a separate Sensemaking agent or automatic planner, owns semantic judgment. Independently forming a value judgment does not grant authority over external resources or protected commitments.

**The intended differentiator is integrated cognitive development:** retained experience should improve later judgment and intellectual method selection. Co-located knowledge records or separate Skills alone do not establish this outcome. The selected destination does not protect any particular schema or runtime from revision.

**Current implementation:** ontology-grounded software-repository understanding and prospective reasoning through the single public using-sensemaking Skill, with persistent semantic stewardship and optional separately authorized engineering construction. These are valuable specialized foundations, not a finished or qualified domain-general system.

[ADR 0037](adr/0037-domain-general-cognitive-development.md) records the explicit 2026-11-13 Level-4 REVISE. General cognitive improvement, functional integration advantage and cross-domain transfer remain NOT QUALIFIED.

### Level-4 extension 2026-11-12: Adaptive Metareasoning System (ADR 0036)

The owner selected **Adaptive Metareasoning System (AMS)** as an explicit,
first-class **cognitive regulation capability** within the existing
ontology-grounded, agent-native reasoning system. AMS evaluates purpose,
question and method fitness; distinguishes productive inquiry from misleading
but technically correct progress; and allocates the next unit of cognitive or
engineering effort proportionately, including justified direct action or
stopping. It is exercised through the single **using-sensemaking** controller
and existing Inquiry, Metareasoning, Exploration and Warrant/Choice policies.

AMS does not replace **Sensemaking Continuous Learning (SCL)**. AMS owns
current reasoning and method selection; SCL supports selective retention,
source-checked reuse and feedback on earlier product or methodological
experience. Neither historical lessons nor AMS inferences transfer authority
from another repository. [ADR 0036](adr/0036-adaptive-metareasoning-system.md)
records the selected product outcome; the [AMS design](superpowers/specs/2026-11-12-adaptive-metareasoning-system-design.md)
and [development program](superpowers/plans/2026-11-12-adaptive-metareasoning-system.md)
separate the existing policy/knowledge infrastructure from unqualified
authentic adaptive-behavior and comparative-benefit claims. No second
controller, numeric method ranker or self-modifying runtime is authorized.

### Level-4 extension 2026-11-12: Sensemaking Continuous Learning (ADR 0035)

The owner selected **Sensemaking Continuous Learning (SCL)** as an explicit,
first-class intended product capability **within** Persistent Semantic
Stewardship. Ordinary real engineering episodes should be eligible for
proportionate learning consideration: improve source-grounded product/domain
understanding and, where experience supports it, the context-sensitive
effectiveness of the agent's reasoning methods. **Every observable episode is
eligible; every episode does not require a persistent lesson.** Selectively
retain evidence that future actors need, permit justified rejection of past
methods and retain `NO_MODEL_CHANGE` for routine outcomes.

SCL reuses the existing `using-sensemaking` controller, Learning/Reconciliation
policy, Git-reviewed knowledge records, original source evidence and bounded
Steward recall. A later agent must check source, context, applicability and
authority before using a precedent. Lessons do not grant permission across
repositories. Higher-order methodological guidance changes require
independent corroboration, counterevidence and ordinary protected review.

The owner's [ADR 0035](adr/0035-sensemaking-continuous-learning.md) records the
scope and evidence ceiling; the [SCL development program](superpowers/plans/2026-11-12-sensemaking-continuous-learning.md)
separates current retrieval/guidance capabilities from still-unqualified
independent use, feedback, comparative benefit and possible later automation.
This **does not** declare an automatic learning runtime, new semantic controller,
model training or self-modification. ADRs 0029, 0031 and 0034 remain operative.

### Level-4 revision 2026-10-28: ontology-first adaptive Sensemaking (ADR 0034)

The owner selected seven governing decisions, recorded in
[ADR 0034](adr/0034-ontology-first-adaptive-sensemaking.md):

1. Sensemaking is an ontology-grounded repository understanding and prospective
   reasoning system, not primarily an implementation agent or task picker.
2. `using-sensemaking` is the single public entrypoint and adaptive controller.
3. First repository-level engagement establishes source-grounded domain and
   architecture knowledge before any repository-wide strategic selection.
4. Possibility-space coverage precedes strategic convergence.
5. The active agent composes specialized reasoning adaptively and may revisit it.
6. Implementation is optional and separately authorized.
7. There is one semantic controller; strategic continuation supports it.

ADR 0031's destination and ADR 0029's boundary are unchanged. The benefits of
ontology-first entry and single-entrypoint composition are **unproven**.

### Level-4 revision 2026-10-15: persistent semantic stewardship (ADR 0031)

The owner explicitly selected **Path 3 — Persistent Semantic Stewardship
Platform** as Sensemaking's long-term architectural destination. Continuous
product-grounded development (Path 2) is the operational loop that uses and
enriches this knowledge. Lean decision assistance (Path 1) remains a
low-ceremony mode for tasks that do not need deeper context.

The intended product has two cooperating planes:

- **Persistent semantic knowledge:** goals, capabilities, constraints,
  dependencies, architectural rationale, source/verification relationships,
  decisions, contradictions, uncertainties and historical lessons.
- **Skill-mediated reasoning and construction:** divergent exploration,
  convergent evaluation, adversarial review, bounded implementation,
  verification, reconciliation and revision of retained knowledge.

Important semantic relationships may merit typed representation even when
parts of their underlying code topology can be derived automatically. Build
the model progressively, distinguish prescriptive/descriptive/epistemic
knowledge, and preserve exact source/authority/temporal identity. Code review,
tests and CI remain essential evidence sources, but the overarching product
outcome is **knowledge that compounds to improve future engineering
decisions** rather than test or documentation volume.

The accepted decision is [ADR 0031](adr/0031-persistent-semantic-stewardship.md);
the detailed construction trajectory is
[persistent semantic stewardship plan](persistent-semantic-stewardship-plan.md).
ADR 0029's external execution/authority boundary remains controlling.
The comparative and long-horizon benefits remain **unproven**.

### Historical Level-4 revision 2026-10-12: target-repository grounding (ADR 0030)

The owner-delegated Phase 0 of
[`repository-grounding-plan.md`](repository-grounding-plan.md) revises the
main lever of the product. The product's output for a target repository is a
small, provenance-tagged Grounding Pack (intent and non-goals, domain terms,
invariants and traps, decision records) that a fresh coding agent reads before
work, and an owner-question ratchet that records each owner answer so it is not
asked again. The hypothesis is that this improves delegation quality (fewer
owner questions and less rework) more than additional procedural machinery.
At its adoption this added a grounding hypothesis and measures without
changing the then-current product purpose, strategic non-goals or ADR 0029.
ADR 0031 now broadens the **product destination**: the compact Grounding Pack
is a useful entry point, not a global ontology format or size ceiling.
The 2026-10-12 intended capability was **continuous, autonomous domain grounding**:
the agent retrieves only decision-relevant intent and system relationships,
finds a valuable difference between desired and actual user experience,
selects and implements a bounded improvement, observes its consequences, and
updates only durable non-derivable knowledge before continuing. Perfect
upfront understanding and documentation volume are not product outcomes.
This is the intended behavior, **not** established comparative effectiveness.

## 2. Problem

Capable agents often execute local tasks without reliably retaining their cognitive development, noticing unasked questions, revising questionable purposes, selecting suitable reasoning methods or improving subsequent judgment from experience. External memory and separate Skills may help without demonstrating generalizable learning. Domain evidence, values and authority also differ; indiscriminate transfer can be harmful. Repository-specific missing-question, stale-evidence and continuity failures remain important applications of this broader problem.

## 3. Primary users and anti-persona

**Primary operational users:** intelligent agents across all domains, with equal standing in the shared cognitive capabilities. Coding agents are the best-developed current specialization, not a privileged universal user. **Secondary users:** the people and organizations deploying, authorizing and evaluating these agents. Owner intent is context and legitimate authority, not a prohibition on critically examining objectives.

**Anti-persona:** a narrow, mechanically obvious task whose correct execution needs no consequential uncertainty assessment, cognitive adaptation or continuity. Do not force expensive process or generic-agent machinery onto such tasks.

## 4. Job to be done

> When an intelligent agent encounters a consequential question, help it recover relevant evidence and its own cognitive history, discover and evaluate alternative purposes, determine suitable intellectual methods, reach a defensible provisional judgment, and learn from consequences so its future reasoning becomes more capable.

Sufficient understanding and relevant possibility coverage are required **before consequential strategic commitments**, but are not mandatory fixed procedures for every local task. Explicit and agent-adaptive intellectual approaches coexist. A persistent agent may work across domains, while distinct agents may selectively exchange qualified methods without assuming identical identity or transferred permissions.

## 5. Value proposition

Sensemaking combines **portable cognitive continuity**, source- and authority-aware knowledge, possibility discovery, reflective value formation, metareasoning, and experience-grounded method adaptation. The same agent may combine Architect, Free-Thinker, Critic, Tutor and other cognitive modes without spawning competing controllers.

**Agent-level cognitive state** (attributed learned methods, history and evaluative commitments) remains distinct from **domain knowledge** (local facts, evidence, assumptions, preferences and authority). Persistent state may migrate across compatible hosts without assuming identical models or proving agent identity. Agent-owned, reversible method adaptations require independent evaluation; changes to shared guidance require separate qualification, review and authority.

A minimal shared cognitive ontology admits domain-specific extensions. Cognitive packages may add knowledge and methods, while executable software packages, including possible game-genre components, are separate interoperable tools rather than required cognitive-core implementations.

**Evidence ceiling:** no independent proof currently establishes a domain-general improvement, longitudinal transfer, causal benefit of integration, cross-host identity continuity, automatic self-improvement or superiority to capable direct agents using ordinary memory and specialist Skills.

## 6. Positioning and boundary

**Long-term identity:** domain-general cognitive substrate, not a separate agent, foundation model, universal runtime or execution platform. **Present implemented scope:** source-grounded repository knowledge, prospective reasoning, specialized Skills and bounded engineering/Campaign support. ADR 0029 remains the controlling **current external product boundary**, while ADR 0037 governs intended purpose.

Functional integration must change the agent's future behavior through interactions among continuity, cognitive regulation and learning, not merely share a data store. The developmental objective persists, but particular mechanisms are revisable under contrary evidence.

The current Engineering and Product Management Domain Packs describe implemented Skill contracts, not a cognitive package marketplace. Future game-genre cognitive and executable packages remain separate conceptual types with no automatic build commitment. The expanded purpose does **not** authorize new runtimes, model training, shared-policy self-modification, semantic truth or authority engines, third-party mutation, release or deployment.

## 7. Strategic principles

1. Evidence precedes a consequential transition.
2. Resolve the nearest decision-changing uncertainty appropriate to the current
   control level.
3. A responsibility exists because its result changes a decision.
4. Recommendation, selection, authorization, and ratification are different
   states.
5. Capability availability does not imply capability appropriateness.
6. Agents own semantic judgment; deterministic mechanisms own mechanical facts
   and invariants.
7. Solved questions stop generating work.
8. Deferred work does not become a TODO merely because it exists.
9. Correct stopping is successful behavior.
10. External boundaries are recorded rather than fabricated around.
11. Productize demonstrated needs, not speculative machinery.
12. Preserve evidence ceilings and do not manufacture work to keep a campaign
    or strategic loop active.
13. Lower control levels may execute higher-level commitments but may not
    silently redefine them.
14. Product-thesis revision is slower and more authority-sensitive than ordinary
    repository evolution.
15. **Opinionated about engineering invariants, adaptive about process,
    progressive in disclosure.** Stable principles should proactively protect
    evidence, responsibility, authority, and closure boundaries, while visible
    ceremony and durable machinery should scale only when the situation warrants
    them.
16. **Higher desired delegation increases the amount of judgment the user wants
    the agent to exercise; it does not increase the agent's granted authority.**
17. Beginner-first guidance should surface missing considerations without
    requiring the user to understand Sensemaking's internal machinery. Experts
    should be able to consume concise evidence/control surfaces without losing
    the same invariants.
18. **Preserve knowledge that compounds:** authoritative rationale, capability
    relationships, architectural assumptions and consequential lessons should
    survive changing code and agent contexts; derived topology should be
    refreshable rather than copied into a second manual truth.
19. **Separate intent, observations and inference:** no model, graph edge,
    test result or extracted symbol silently becomes owner authority.
20. **Learn by correction as well as retention:** make contradiction,
    supersession and historical scope queryable; more records are not
    automatically more knowledge.

21. Cognitive development is assessed through better later judgment, not more recorded knowledge or reasoning procedures.
22. Domain-general user standing does not imply current equal implementation or evidence.
23. Personal learning does not silently promote shared policy or third-party permissions.
24. Preserve the developmental objective while allowing evidence to replace its technical realization.

## 8. Strategic non-goals

The following are not current build commitments: a custom coding-agent runtime,
central deterministic semantic router, HTN planner, generic autonomous-agent
platform, mandatory multi-agent swarm, automatic critic voting, semantic truth
oracle, `OuterLoopEngine`, automatic Strategic Frontier ranking, automatic
product-thesis revision, autonomous Campaign generation, autonomous merge or
release authority, cross-repository transaction/deployment coordinator,
user-expertise scoring, deterministic task-complexity or consequentiality
scoring, automatic persona inference, beginner/expert runtime modes, automatic
Campaign thresholds, or campaign/strategy infrastructure larger than
demonstrated need.

Reconsider a non-goal only when repository/product evidence shows that its
absence is decision-changing and a smaller intervention cannot address the
problem. Major reversal of a strategic non-goal is a Level-4 decision.

The prohibition on a central deterministic semantic router or semantic truth
oracle does **not** prohibit a substantial, persistent semantic knowledge
store. Grounding Pack word budgets are local presentation constraints,
not limits on the selected future typed ontology (ADR 0031).

These remain **current implementation non-goals**, not prohibitions against the new long-term cognitive-development purpose. Any generic runtime or package machinery still needs a demonstrated consumer and separately authorized design.

## 9. Hypotheses and bets

| Hypothesis | Current status |
| --- | --- |
| Repository sensemaking improves ambiguous repository decisions | Supported, bounded |
| Durable artifacts support fresh-context continuation | Supported |
| Responsibility-first thinking is better than workflow-first thinking | Emerging hypothesis |
| Opinionated guidance can add value by surfacing considerations a high-delegation user did not know or want to specify | Product hypothesis; not comparatively established |
| Adaptive process rigor can reduce unnecessary ceremony while preserving stable engineering invariants | Product hypothesis; no formal routing/tiers authorized |
| Durable Level-3 strategic state can reduce development-direction reconstruction ambiguity | Supported in bounded self-development campaigns; broader value not established |
| Adaptive campaign execution reduces owner routing | Not yet demonstrated |
| Campaign State materially improves continuation | Hypothesis |
| Claim Evidence Register generalizes beyond Clause B | Hypothesis |
| Sensemaking consistently beats a capable direct-agent baseline | Not established |
| A target-repository Grounding Pack reduces owner questions and rework versus a direct agent on the same tasks | Not established; Phase 3 of the grounding plan will test it on one repository |
| A typed semantic model preserves architectural rationale and constraint relationships more reliably across changing implementations and fresh contexts | Selected long-term product hypothesis; not implemented or validated at the intended horizon |
| Longitudinal semantic knowledge accumulation improves later architectural decisions beyond direct code/history inspection | Not established; requires later-episode evidence, not row counts |
| A custom execution runtime is required | No evidence |
| A deterministic strategic planner is required | No evidence |
| Functional integration of continuity, metareasoning and learning improves later judgment beyond simpler compositions | New product-level hypothesis; NOT QUALIFIED |
| Experience-based method adaptation improves decisions in independent later episodes | Intended benefit; NOT QUALIFIED |
| Cognitive principles transfer across domains without erasing domain distinctions | Limited synthetic conceptual evidence only; practical transfer NOT QUALIFIED |
| Portability of cognitive state preserves appropriate continuity across hosts | Intended capability; NOT QUALIFIED |

## 10. Success measures

The ultimate success measure is **independently established longitudinal, transferable improvement in an agent's consequential reasoning and intellectual methods**, including any incremental benefit of functional integration over strong simpler-tool baselines.

Use graduated qualification with distinct ceilings:

1. **Conceptual coherence:** well-defined cognitive relationships without collapsing domain meanings.
2. **Operational availability:** real host agents can access and apply the capabilities.
3. **Authentic use:** consequential experience, method choice or prior evidence affects a later agent decision, including justified rejection.
4. **Matched comparative benefit:** comparable baselines control model, tools, task and cost; isolate retrieval, metareasoning and learning effects.
5. **Longitudinal transfer:** learning persists across independent episodes and unfamiliar situations or domains with independent evaluation.

For the **current engineering specialization**, retain narrower measures: grounded diagnosis, appropriate engineering responsibility and stopping, verified reuse of architectural decisions, source currentness, reduced rediscovery, and cost. They are not interchangeable with general intelligence improvement.

The first practical *research direction*, not an automatic experiment order, is a bounded matched multi-episode comparison of experience-informed method selection/adaptation versus fixed methods. Wider component ablations and cross-domain assessment follow only when warranted.

## 11. Product-level strategic frontier

> Can functional integration of persistent cognitive continuity, reflective value formation, adaptive metareasoning and experience-grounded learning yield **demonstrably better later judgment across episodes and domains**, beyond capable direct agents and conventional memory-plus-Skills approaches?

Key open hypotheses concern methodological improvement beyond retrieval, independent agent identity continuity, justified cross-domain transfer and the incremental cost-adjusted benefit of integration. No empirical benefit is currently established by the decision to adopt the thesis.

The old **PATH-1** direction—growing reviewed repository knowledge through genuine engineering responsibilities—remains a valuable **domain-specific construction path**, not Sensemaking's ultimate purpose. See the [mandatory Level-3 reconciliation](../artifacts/history/2026-11-13-domain-general-cognitive-thesis-reconciliation.md). No new runtime, universal ontology, benchmark, or game package becomes an automatic task.

## 12. Level-4 revision semantics

This document is the Level-4 authority surface, but editing it is not equivalent
to ordinary documentation cleanup.

Consequential product-thesis review should end in one explicit disposition:

```text
REAFFIRM
REINTERPRET
REVISE
RETIRE
SUPERSEDE
```

The detailed contract is
[`product-thesis-revision.md`](product-thesis-revision.md).

The Persona & Adaptive Guidance Model v0 change uses `REINTERPRET`: the existing
primary-user commitment remains materially the same, while its high-delegation,
beginner-first/expert-capable meaning is made explicit.

Product Boundary Reconciliation v1 uses `SUPERSEDE`: ADR 0014 remains historical
and ADR 0029 becomes the current boundary authority. Product purpose, agent-owned
semantic judgment, major strategic non-goals, Campaign schema, and empirical
claim ceilings are not expanded by the act of supersession itself.

The active agent may identify thesis-level tension, gather evidence, formulate
alternatives, and draft a recommendation. Major changes to product mission,
primary user, external product boundary, strategic non-goals, or public claim
ceilings remain owner-reserved unless authority is explicitly delegated.

The 2026-10-15 owner selection uses **REVISE**: the product purpose becomes
long-term semantic stewardship rather than only immediate repository
responsibility selection. ADR 0031 preserves ADR 0029's external boundary
and applies ADR 0030 only to the compact Grounding Pack presentation.

After a ratified Level-4 change, Level 3 must reassess the Strategic Frontier
rather than blindly continue the previous repository responsibility.

**2026-11-13 — ADR 0037:** owner-selected REVISE of product purpose, primary users and ultimate evidence criteria; existing ADRs 0029/0031/0034/0035/0036 remain authoritative within their qualified current-scope meanings. The broader intended purpose and its evidence ceilings are separated from present operational/release permissions. Level 3 is separately reconciled before dependent work.

## 13. Public/private boundary

Public strategy may include the product problem, persona, JTBD, positioning,
principles, non-goals, public hypotheses, and sanitized experimental or
repository conclusions. Keep private target identities, private repository
findings, security details, raw unpublished experiments, and sensitive
commercial reasoning local. Public claims must not imply evidence beyond the
underlying record.

## 14. Authority and related documents

- Current owner-ratified intended product purpose: [ADR 0037](adr/0037-domain-general-cognitive-development.md)
- Mandatory post-revision Level-3 reconciliation: [2026-11-13 cognitive thesis reconciliation](../artifacts/history/2026-11-13-domain-general-cognitive-thesis-reconciliation.md)
- Current product-boundary authority: [ADR 0029](adr/0029-current-product-boundary.md)
- Owner-selected persistent semantic stewardship: [ADR 0031](adr/0031-persistent-semantic-stewardship.md)
- Detailed development trajectory: [persistent-semantic-stewardship-plan.md](persistent-semantic-stewardship-plan.md)
- Compact target-repository Grounding Pack: [ADR 0030](adr/0030-target-repository-grounding.md)
- Product-boundary reconciliation record: [product-boundary-reconciliation-v1.md](product-boundary-reconciliation-v1.md)
- Historical July 2026 product boundary: [ADR 0014](adr/0014-product-boundary.md)
- Persona/adaptive-guidance reinterpretation preflight: [persona-adaptive-guidance-design-preflight.md](persona-adaptive-guidance-design-preflight.md)
- Four-level control model: [strategic-outer-loop.md](strategic-outer-loop.md)
- Level-3 state contract: [strategic-state-contract.md](strategic-state-contract.md)
- Level-4 revision contract: [product-thesis-revision.md](product-thesis-revision.md)
- Non-authoritative future possibilities: [strategic-candidate-directions.md](strategic-candidate-directions.md) — idea memory only; not Strategic Frontier membership or implementation authorization
- Current operating model: [product-operating-model.md](product-operating-model.md)
- Current Level-3 status and development direction: [STATUS.md](../STATUS.md)
- Architecture authority: [ADR index](adr/README.md), especially ADRs 0013 and 0029
- Operating workflow: [agent-native-operating-workflow.md](agent-native-operating-workflow.md)
- Research hypotheses: [control-model research agenda](research/control-model-research-agenda.md)
- Goal A protocol: [external product-validation protocol](research/goal-a-external-product-validation-protocol.md)
