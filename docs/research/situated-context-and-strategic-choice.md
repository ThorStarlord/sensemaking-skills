# Situated Context, Opportunity Coverage, and Adaptive Strategic Selection

**Status:** Working research hypothesis — NOT EMPIRICALLY QUALIFIED  
**Date:** 2026-11-16  
**Scope:** Agent-native strategic responsibility selection during genuine repository work  
**Authority:** Non-authoritative research note; not an ADR, product-thesis revision, Skill/policy change, implementation specification, experiment mandate, or strategic reopening  
**Origin:** Owner-reported concerns and conceptual discussion, reconciled against the existing Sensemaking documentation. The discussion is not an independently observed agent episode.

## 1. Concern: local success may not advance the governing outcome

A highly capable coding agent can complete locally correct tasks while allocating effort poorly toward the product's longer-term purpose. Illustrative cases include repeated hardening of a low-impact edge case, further qualification of an already adequate support surface, or refinement of an existing subsystem while a more valuable capability remains unbuilt.

This is a **possible strategic-selection failure**, not evidence that small repairs, verification, or locally bounded tasks are intrinsically low value. A tiny fix can prevent a consequential failure; a large feature can be speculative or unauthorized. The question is whether the selected responsibility is justified against the *current* product purpose, available alternatives, consequences, authority, and opportunity cost.

The repository already describes related but distinct failure families: **F1 premature convergence**, **F2 exhaustive-search ceremony**, **F4 false option diversity**, **F5 proxy capture**, **F6 construction starvation**, **F8 qualification/hardening preemption**, and **F13 reconciliation omission** in the [Strategic Normal-Use Failure Taxonomy](../strategic-normal-use-failure-taxonomy-v1.md). This note does not assert a new observed failure class.

## 2. Competing causal explanations

Poor strategic choices can have materially different causes. Do not diagnose an adaptive-metareasoning defect solely from a disappointing result.

| Hypothesis | What might be inadequate | Evidence that would help discriminate it |
| --- | --- | --- |
| **H1 — Situated-context acquisition/delivery** | The agent does not obtain or use current product intent, capabilities, decisions, consumers, constraints, or actual repository evidence at the consequential choice. | Compare available sources with sources actually encountered **before** selection; assess whether grounded context changes the chosen responsibility. |
| **H2 — Opportunity coverage** | The agent understands the system but never represents materially different high-value paths. | Inspect the contemporaneous option set; compare it with grounded alternatives under the same source revision, without inventing a globally complete option inventory. |
| **H3 — Value and warrant judgment** | The agent recognizes alternatives but gives inadequate weight to mission relevance, user value, deferral/omission cost, risk, or authorization. | Review the stated decision effects and consequences of credible alternatives; distinguish weak comparison from missing facts or options. |
| **H4 — Adaptive cognitive control/reassessment** | The agent chooses an unsuitable intellectual move, converges too early, or fails to reconsider an increasingly low-value responsibility despite relevant returned evidence. | Trace observed decision-time method choices, reconsideration triggers, and whether later evidence changed the warrant; do not infer hidden model reasoning. |
| **H5 — Execution and delivery** | The selected responsibility was defensible, but the agent did not create, integrate, or verify the intended useful capability. | Inspect the actual code, consumers, integration, outcome, and remaining product-completion layers separately from the quality of selection. |

These explanations may coexist. In particular, context can be *present in the repository* without being *retrieved*, and retrieved information can be *read* without being *applied* to a consequential choice. A retrospective rationale cannot establish what the agent considered before acting. See the bounded [PR #825 responsibility-selection case](../normal-use/2026-11-12-pr825-responsibility-selection-case.md) for an example of this attribution limit.

## 3. Context, exploration, metareasoning, and construction

**General model knowledge is not situated product knowledge.** Good task-specific judgment may require the governing goal, exact-revision capability state, strategic history, authentic unmet user outcomes, relevant competing opportunities, and authority. No single document or knowledge query guarantees this understanding.

**Broad exploration can improve both opportunity coverage and situational understanding.** It may expose neglected systems, new combinations, or an inappropriate local frame. But more branches generated from the same weak assumptions can produce false diversity and search ceremony, not better decisions.

**Adaptive metareasoning allocates intellectual effort; it does not manufacture missing evidence or alternatives.** An agent may choose ACT, INQUIRE, CHALLENGE, EXPLORE, VERIFY, ESCALATE, or STOP coherently *within an impoverished context* and still pursue a poor overall responsibility. Conversely, fixed breadth is not automatically better: once the strategic choice is grounded and settled, reopening repository-wide exploration can obstruct valuable construction.

The working synthesis is **context-grounded, opportunity-aware adaptive selection**: proportionately reconstruct the decision-relevant system and meaningful alternatives when the strategic direction is open; choose the smallest useful intellectual move; prefer warranted value-producing work; reconcile consequential returned evidence; and reconsider the responsibility only when the warrant changes. This describes a possible relationship among **existing responsibilities**, not a new mandatory pipeline, controller, scoring formula, or requirement to explore before every repair.

See [Cognitive Orientation Crosswalk](../semantic-architecture/cognitive-orientation-crosswalk-v1.md), [AMS design](../superpowers/specs/2026-11-12-adaptive-metareasoning-system-design.md), [Strategic Repository Sensemaking](../strategic-repository-sensemaking-v1.md), [Metareasoning Policy](../../skills/using-sensemaking/references/metareasoning-policy-v0.md), and [Value-Directed Continuous Construction](../value-directed-continuous-construction.md).

## 4. Possible discriminating observations (not an experiment commitment)

When an authentic, authorized repository responsibility makes this distinction consequential, preserve enough **decision-time** evidence to ask:

1. **Context:** What product/strategic sources were available, retrieved, and demonstrably used before selecting work? Which consequential source or currentness condition was absent?
2. **Opportunity set:** What genuinely different responsibilities were represented, and which material alternative was omitted? Was the omission evident at the time or only in hindsight?
3. **Selection:** Why was the chosen responsibility warranted relative to credible alternatives, including commission risk, deferral cost, and value that construction could retain?
4. **Control and adaptation:** Which intellectual move was observable, what evidence returned, and did it justify continuation, a new inquiry, bounded building, a strategic reassessment, or stopping?
5. **Outcome:** Did the work deliver the intended capability or decision benefit? Keep local completion, product relevance, and independent comparative benefit separate.

One possible comparison varies **context grounding** (limited versus sufficient decision-relevant repository context) and **search breadth** (adaptive versus deliberately broad), while holding the goal, source revision, authority, and comparable effort as stable as practical. This is an *optional causal-discrimination idea*, not a required synthetic benchmark, fixed 2×2 protocol, or new qualification gate. Real construction that provides adequate evidence may be preferable to a separate experiment. Positive, negative, neutral, and inconclusive outcomes are all informative within their actual claim ceilings.

## 5. Interpretation limits and reopening conditions

- **Not established:** that context inadequacy is the primary cause of poor coding-agent choices; that brute-force breadth outperforms adaptive metareasoning; that an agent can identify the globally optimal responsibility; or that any current Sensemaking mechanism reliably improves independent long-term outcomes.
- **Not authorized:** an additional Skill, ontology, policy, runtime, mandatory strategic funnel, numerical opportunity score, test program, or rewrite of accepted product commitments. [ADR 0037](../adr/0037-domain-general-cognitive-development.md) remains product-purpose authority and [ADR 0036](../adr/0036-adaptive-metareasoning-system.md) remains the accepted AMS direction.
- **Revisit if:** source-grounded normal-use episodes repeatedly reveal context unavailability, impoverished alternatives, poor comparative warrant, incorrect method selection, or unproductive continuation that materially changes what should be built; or credible comparative observations favor a different contextual/search composition.
- **Otherwise:** continue already-warranted construction. Keep this hypothesis available for interpreting future evidence; do not promote an interesting explanation into an implementation responsibility merely because it is documented.

**Research question preserved:** *When a capable agent repeatedly produces locally successful but strategically low-value work, which missing or misused input—situated context, meaningful options, value comparison, cognitive-control choice, or execution feedback—actually explains the divergence from the product goal?*
