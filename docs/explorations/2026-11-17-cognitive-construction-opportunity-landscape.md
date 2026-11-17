# Cognitive Construction Opportunities — Divergent Exploration (2026-11-17)

**Status:** DIVERGENT EXPLORATION ONLY. This is a source-grounded, non-authoritative opportunity landscape, not a Level-3 selection, accepted architecture, revised Level-4 thesis, adopted implementation plan, ticket queue, requirement, new Skill, research protocol, or permission to modify existing mechanisms.

**Target:** ThorStarlord/sensemaking-skills. **Inspected canonical source:** [main at f20547fa7888b96ec45f06945c9103854bb8faf1](https://github.com/ThorStarlord/sensemaking-skills/tree/f20547fa7888b96ec45f06945c9103854bb8faf1), 2026-11-16. **Exploration date:** 2026-11-17. Later unmerged PRs are identified separately.

**Seed:** The owner wants Sensemaking to improve autonomous opportunity discovery, strategic value judgment, long-horizon construction and experience-grounded cognitive development. The owner prefers *bounded, value-directed construction* over repeating separate Skill exercises or synthetic qualification merely to produce more evidence. The user requested divergent exploration of what could be built, then requested this exploration be retained in repository documentation.

**Method:** Problem-led and repository-led broad divergence, using the [Divergent Exploration Skill](../../skills/strategic-repository-analysis/references/divergent-exploration-v1.md) as related repository precedent and the active-agent responsibility boundary of [using-sensemaking](../../skills/using-sensemaking/SKILL.md). No separate strategic analysis was invoked and no alternative was selected. This record is not a fresh empirical comparison of agents.

## 1. Governing intent and evidence boundary

The ratified purpose is **domain-general cognitive development**, not simply an increasingly detailed repository knowledge base. The intended differentiator is the *functional integration* of persistent knowledge, prospective discovery, reflective value formation, adaptive metareasoning, learning and continuity. The active host agent retains semantic control; no automatic planner or separate Sensemaking controller gains authority. See [product strategy](../product-strategy.md) and [ADR 0037](../adr/0037-domain-general-cognitive-development.md).

The current mature specialization is ontology-grounded software-repository understanding. Existing, actual interfaces include:

- **Source-grounded product orientation:** the reviewed knowledge graph and the **product-outline** operation, optionally projecting explicitly linked future possibilities with **--include-candidates**. This is an explicit-edge, bounded documentary view; a goal/edge being present is not evidence of product benefit. See [knowledge_architecture.py](../../src/sensemaking_skills/semantic_architecture/knowledge_architecture.py), [workspace_knowledge.py](../../src/sensemaking_skills/workspace_knowledge.py), and [semantic_cli.py](../../src/sensemaking_skills/semantic_cli.py).
- **Task/context/lesson lookup:** **context-for**, **search** with optional question-friendly lexical matching, and retained original-source references. Retrieval is not semantic applicability or decision-time use. See [knowledge_retrieval.py](../../src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py) and [Steward recall](../../skills/repository-semantic-steward/references/recall.md).
- **Existing cognitive guidance:** [AMS design](../superpowers/specs/2026-11-12-adaptive-metareasoning-system-design.md), [SCL](../adr/0035-sensemaking-continuous-learning.md), [Warrant/Choice](../../skills/using-sensemaking/references/warrant-choice-policy-v0.md), and [Experiment Economy](../../skills/using-sensemaking/references/experiment-economy-v1.md). Their availability does not prove a particular agent applied them correctly.
- **Construction-first philosophy:** [Value-Directed Continuous Construction](../value-directed-continuous-construction.md) treats useful reversible construction as a possible evidence source, not a replacement for all outcome verification. A bounded increment need not be a small local patch.
- **Long-standing diagnostic work:** [PR #825 responsibility-selection case](../normal-use/2026-11-12-pr825-responsibility-selection-case.md), [construction versus outcomes retrospective](./2026-11-13-construction-vs-product-outcomes-retrospective.md), [situated-context/strategic-choice hypotheses](../research/situated-context-and-strategic-choice.md), [decision-time selection depth study](./2026-11-11-decision-time-responsibility-selection-depth.md), and the [strategic normal-use failure taxonomy](../strategic-normal-use-failure-taxonomy-v1.md).

These sources document **repeated concern and multiple real engineering episodes**: locally valid improvements can have uncertain relative strategic value, and retrospective records incompletely reveal original selection. They do **not** establish a single recurring causal mechanism or prove that one proposed fix will improve independent agent outcomes. [PR #892](https://github.com/ThorStarlord/sensemaking-skills/pull/892) and its pending [audit PR #893](https://github.com/ThorStarlord/sensemaking-skills/pull/893) are recent cases, not accepted proof of an AMS defect.

The current [STATUS.md](../../STATUS.md) Q-2 disposition separates useful construction from formal independent comparative qualification. The [Issue #860](https://github.com/ThorStarlord/sensemaking-skills/issues/860) amendment preserves this two-track boundary. Missing causal proof should not automatically block an otherwise warranted, reversible and useful build, nor should a build be advertised as cognitive improvement without the relevant evidence.

## 2. Five rival problem framings

| Framing | Potential limiting behavior | Intervention family | Crucial distinction |
| --- | --- | --- | --- |
| Situated context | Relevant product intent, real consumers, current capability or precedent fails to reach a consequential choice | Decision-time context delivery/interpretation | Stored != retrieved != applied |
| Opportunity discovery | Agent never represents a materially different high-value responsibility | Capability-gap discovery and possibility recombination | Recorded possibilities != adequate choice set |
| Comparative valuation | Alternatives are seen but selected using cost, verification convenience or weak value assumptions | Consequence-based comparative judgment | Local correctness != highest-value selection |
| Strategic continuity | Each PR is bounded, but the intended end-to-end capability is never completed | Outcome-centered construction trajectories | PR completion != capability completion |
| Cognitive learning | Experience is retained but does not improve later method or value decisions | Decision-time re-entry and outcome-grounded adaptation | A lesson exists != later reasoning improves |

These framings can coexist. Do not solve all five by declaring a mandatory pipeline or assuming the problem is merely missing instructions.

## 3. Possibility landscape — current-decision capabilities

The candidates below are **conceptual construction directions**, not a prioritized feature list. For each, the smallest plausible product-valuable slice is illustrative, not yet source-validated or approved.

### A1. Decision-time cognitive context bridge

- **Mechanism:** Combine the relevant governing goal, source-grounded capabilities, constraints, competing possibilities and applicable methodological experience *at the moment of strategic responsibility choice* through an existing agent-visible consumer.
- **Possible bounded slice:** Extend an existing orientation/selection consumer to expose one compact, revision-pinned product-decision context for a genuine repository mission, rather than adding another independent context database.
- **Value:** Reduces strategic selection from whichever issue/file is most visible. Preserves the distinction between source presence, agent exposure and actual interpretation.
- **Dependency / failure mode:** Need to identify the real selection consumer. Another excellent but unconsulted output would be wasted work; overbroad context could crowd out high-value evidence.
- **Status:** Grounded compositional opportunity; whether current host guidance already suffices is an open consumer-level question.

### A2. Goal-to-capability gap discovery

- **Mechanism:** Start from a consequential agent/user outcome and inspect whether current implemented capabilities and consumers actually support it, rather than searching only for locally broken code.
- **Possible bounded slice:** A read-only outcome-to-capability/consumer assessment for one actual product objective, explicitly distinguishing observed absence, unassessed coverage and merely hypothetical benefits.
- **Value:** Shifts discovery from cheap implementation discrepancies to missing beneficiary behavior and potentially unasked questions.
- **Dependency / failure mode:** Incomplete graph coverage is not proof a capability is absent; the feature might merely reformat issue titles. A valuable slice must inspect code and consumers, not just authored records.
- **Status:** Inferred opportunity consistent with the accepted product purpose, not a demonstrated missing API.

### A3. Opportunity ecology and cross-episode synthesis

- **Mechanism:** Represent meaningful relationships among possible futures: shared premises, complements, dependencies, conflicts, enablement and novel combinations. Discover opportunities beyond the current issue queue.
- **Possible bounded slice:** For a selected product outcome, compose source-grounded existing opportunities into alternative coherent paths and permit new, clearly hypothetical combinations.
- **Value:** Potentially expands the candidate space beyond familiar infrastructure and exposes higher-leverage combinations.
- **Dependency / failure mode:** Can become idea theater, generate false diversity, or imply that an authored link proves strategic warrant.
- **Status:** Prefigured by hypothetical reviewed possibilities **poss:assumption-aware-opportunity-ecology** and **poss:cross-episode-possibility-synthesis** in [possibilities.json](../../.sensemaking/knowledge/possibilities.json); not adopted functionality.

### A4. Consequence-first comparative valuation

- **Mechanism:** Compare materially different responsibilities by beneficiary outcome, retained leverage, omitted value, authority, implementation/maintenance cost and reversibility, rather than by patch size or ease of CI verification.
- **Possible bounded slice:** An optional comparative consumer for one genuine consequential selection that makes the expected effect of each alternative inspectable without automatic scalar ranking.
- **Value:** Helps distinguish a real repair from the most valuable currently warranted responsibility.
- **Dependency / failure mode:** Better argument formatting cannot fix an impoverished opportunity set; retrospective justifications can be polished without changing the original decision.
- **Status:** Existing Warrant/Choice guidance covers the principle; incremental *operational* value is unqualified.

### A5. Adaptive question-fitness challenge during execution

- **Mechanism:** At a consequential decision boundary, notice that technically correct progress is failing to answer the governing question and choose to continue, reframe, challenge or stop.
- **Possible bounded slice:** Improve the connection between returned implementation evidence and the current responsibility's end-to-end purpose in an existing reconciliation/continuation consumer.
- **Value:** Corrects course *during* construction, not only when choosing the first task.
- **Dependency / failure mode:** Excessive reconsideration can prevent finishing useful work; a shallow warning may merely restate goals.
- **Status:** Accepted AMS competency direction; specific consumer gap remains to be selected from actual use.

## 4. Possibility landscape — construction and cumulative experience

### B1. Outcome-centered construction trajectories

- **Mechanism:** Preserve an intended user/agent capability across multiple bounded PRs so that each increment is evaluated for its contribution to a coherent end-to-end outcome.
- **Possible bounded slice:** Reuse existing Campaign/strategic continuity or handoff consumers to retain the target behavior, remaining product layers, and change-triggered reconsideration without an automatic backlog executor.
- **Value:** Addresses the possibility that locally correct PRs accumulate without completing a consequential cognitive capability.
- **Dependency / failure mode:** A trajectory can become a rigid plan and suppress discovery; actual next responsibilities must remain independently warranted.
- **Status:** Grounded recombination of existing construction and strategic-continuity semantics.

### B2. Methodological learning at the decision point

- **Mechanism:** A later agent encounters a relevant historical *conditional method lesson* before selecting a method, checks its original source and contrary evidence, then applies, adapts or rejects it.
- **Possible bounded slice:** Repair a demonstrated seam in the existing AMS/SCL/Steward entrypoint during a genuinely useful agent task; do not construct a second learning engine without a consumer need.
- **Value:** Moves beyond lesson availability toward experience-informed intellectual choice.
- **Dependency / failure mode:** Historical anchoring and irrelevant retrieval; later presence alone does not prove decision influence.
- **Status:** Strongly grounded in [Issue #859](https://github.com/ThorStarlord/sensemaking-skills/issues/859) and [Issue #860](https://github.com/ThorStarlord/sensemaking-skills/issues/860); existing construction/qualification scope must be respected rather than duplicated.

### B3. Outcome-linked strategic learning

- **Mechanism:** Compare a responsibility's original expected beneficiary/product value with its actual later use, limits and downstream effects; retain a defeasible insight about future value judgment when warranted.
- **Possible bounded slice:** Link one existing source-attributed choice to a later authentic outcome in current receipt/decision/learning surfaces, without inventing numeric reward scores or retroactively revising the original observation.
- **Value:** Lets future agents improve their judgment of *what is worth building*, not only *how to build it*.
- **Dependency / failure mode:** Outcome attribution can be confounded by context, tool availability, later product changes or execution quality.
- **Status:** Inferred integration opportunity; real source and consumer boundary must be inspected before implementation.

## 5. Possibility landscape — architectural counterfactuals

### C1. Search across competing intellectual approaches

- **Mechanism:** When stakes justify it, use the available active agent and optional delegated agents to explore rival frames (Architect, Free-Thinker, Critic, etc.), then synthesize the results under **one** accountable host decision.
- **Possible bounded slice:** Selective, cost-bounded multiple-approach exploration in a real open strategic decision using ordinary host delegation, without a second semantic controller or agent voting.
- **Value:** Might expose neglected futures or assumptions when one intellectual approach repeatedly converges locally.
- **Dependency / failure mode:** Shared context and correlated assumptions can produce false independence and more output without better decisions.
- **Status:** Speculative mechanism extension, not an authorization to add subagent orchestration.

### C2. Experience-driven adaptation of intellectual methods

- **Mechanism:** Revisit the agent's conditional strategy for choosing intellectual methods based on actual task outcomes; adaptation is attributable, revisable and scoped to the current agent unless separately reviewed for shared use.
- **Possible bounded slice:** One authentic method adaptation retained through existing learning surfaces and later examined when relevant; no automatic shared Skill rewriting.
- **Value:** May develop the ability to *learn when to explore, challenge, act or stop* rather than accumulate fixed reasoning rules.
- **Dependency / failure mode:** Noise, proxy rewards, source mismatch, overgeneralization and identity/authority confusion.
- **Status:** Longer-horizon product hypothesis consistent with ADR 0037; autonomous runtime self-modification and shared policy promotion remain protected decisions.

### C3. Domain-general cognitive capability beyond Git

- **Mechanism:** Make a genuinely useful cognitive competence (for example opportunity judgment or source-grounded method adaptation) portable to an authentic scientific, creative or educational consumer without forcing repository-specific contracts.
- **Possible bounded slice:** Adapt one existing cognitive contract to a second real domain through the active host, preserving domain-specific evidence and authority.
- **Value:** Tests whether the product is becoming a cognitive substrate rather than only a larger software-repository toolkit.
- **Dependency / failure mode:** Premature abstraction could weaken the mature coding-agent specialization; a cross-domain example alone is not demonstrated transfer.
- **Status:** Ratified *goal*, but concrete construction mechanism and value remain open.

### C4. Simplification / less machinery

- **Mechanism:** Prefer an existing capable host with appropriate source context, ordinary memory and a compact lesson mechanism where an additional coordination or policy layer has no observable incremental value.
- **Possible bounded slice:** Simplify or bypass one demonstrably redundant integration in normal use, without discarding still-useful provenance, authority or portable contracts.
- **Value:** Lower friction, fewer handoff failures, less procedural distraction and potentially better actual decisions.
- **Dependency / failure mode:** Can remove valuable long-horizon continuity or obscure ownership of consequential decisions.
- **Status:** Serious counterinterpretation; no current claim that a particular subsystem is redundant.

## 6. Compact comparison — different kinds of leverage

| Candidate | Main lever | Distinctive first outcome | Principal risk |
| --- | --- | --- | --- |
| A1 Context bridge | Decision-time exposure | Relevant product context appears at a real decision | New unused interface |
| A2 Capability-gap discovery | Product-outcome recognition | Identified missing agent behavior beyond one defect | Backlog repackaging |
| A3 Opportunity ecology | Candidate diversity/combination | Coherent new alternatives from known and new futures | Search ceremony |
| A4 Consequence-first valuation | Comparative judgment | Explicit effect and opportunity-cost rationale | Post-hoc eloquence |
| A5 Question-fitness challenge | Corrective control | Agent revises a materially unproductive direction | Constant interruption |
| B1 Outcome trajectories | Multi-PR continuity | Bounded increments complete an intended capability | Rigid project inertia |
| B2 Method-learning re-entry | Historical method influence | Source-checked precedent affects a later method choice | Anchoring and noise |
| B3 Outcome-linked learning | Value-model revision | Expected product value is revised from authentic outcomes | False causal attribution |
| C1 Competing methods | Intellectual search | Missing frame appears through another approach | Correlated redundancy |
| C2 Method adaptation | Cognitive learning | Reversible conditional method improvement | Proxy overfitting |
| C3 Cross-domain capability | Portability | Useful cognitive behavior in another domain | Premature generality |
| C4 Simplification | Cognitive economy | Less machinery for equivalent or better use | Removed useful memory |

No rank or numeric score is claimed. These directions have different expected consumers and evidentiary requirements, and several are complementary.

## 7. Recombination hypotheses (not selected paths)

1. **Situated strategic agent (A1 + A2 + A4):** Reach governing context at selection, detect concrete missing capability, compare consequential value. Potential benefit: better initial responsibility choice. Vulnerability: does not guarantee long-horizon completion.
2. **Long-horizon cognitive builder (A2 + B1 + B3):** Discover an outcome gap, pursue it through independently warranted bounded increments, revise expectations from authentic use. Potential benefit: product completion over PR throughput. Vulnerability: trajectory inertia and attribution.
3. **Experience-informed strategic agent (A5 + B2 + B3 + C2):** Current method choice incorporates source-checked experience; subsequent outcomes correct conditional assumptions. Potential benefit: integrated AMS/SCL development. Vulnerability: still weak if available opportunities are impoverished.
4. **Discovery-oriented evolving agent (A3 + C1 + C2 + C3):** Search varied futures/methods and learn which approaches transfer. Potential benefit: open-ended intellectual capability beyond repository constraints. Vulnerability: high ambiguity and an unclear smallest useful consumer.
5. **Counterfactual simplification (A1 or B2 + C4):** Deliver one well-grounded capability directly through the host, removing redundant intermediate ceremony. Potential benefit: lower total cognitive cost. Vulnerability: lost continuity if simpler methods are insufficient.

These bundles are intellectual compositions, not required packages or a predetermined sequence of tickets. A smaller vertical may deliver more value than a larger bundle.

## 8. Three cross-cutting tensions

**Where does improvement reside?** In reusable Skills, a better existing consumer, source-grounded shared knowledge, an agent-specific acquired method or the host's ordinary capabilities? Shared guidance and agent-local adaptation have different evidence and authority boundaries.

**What is the durable unit of progress?** A PR, a responsibility, a completed agent/user capability, or an adaptable long-horizon trajectory? Optimizing PR count can obscure product benefit; overly rigid trajectories can suppress legitimate strategic revision.

**What should accumulate?** More facts, better opportunity discovery, improved value judgment, greater method competence, stronger construction capability or transferable cognitive continuity? Treat these as distinct outcomes until their interaction is observed, rather than inferring one from another.

## 9. Decision-changing unknowns and possible next inquiries

| Uncertainty | Why it changes the later construction choice | Cheapest appropriate source/observation |
| --- | --- | --- |
| Is the important gap exposure, applicability, or discovery? | Separates A1 from A2/A3/B2 | Inspect actual current consumer and an authentic selection; use prior traces if available |
| Are good alternatives being missed or just undervalued? | Separates A2/A3 from A4 | Compare source-grounded contemporary opportunities and original reasoned selection, without inventing hidden thoughts |
| Is single-PR optimization responsible for incomplete capabilities? | Makes B1 attractive or unnecessary | Inspect multi-increment product outcomes and actual remaining consumers |
| Do later agents retrieve and apply conditional lessons predecision? | Changes warrant for B2/C2 | Genuine later episodes, not merely presence of a lesson record |
| Do anticipated benefits survive downstream use? | Changes value of B3 | Source-pinned original expectation plus authentic returned results |
| Do added cognitive layers outperform simpler direct-agent use? | Puts C4 and C1 in competition with more integration | Ordinary use and proportionate comparison if a causal claim becomes decision-critical |
| Can one cognitive capability retain value outside software repositories? | Changes C3's scope and design | A genuine non-software beneficiary task with current tools |

The owner's open question is conceptually important: **Is the highest-priority missing capability discovering what deserves construction, or becoming better at that discovery through repeated experience?** These are complementary but lead to different first verticals.

Possible next *intellectual* responsibilities: targeted depth on current decision-time consumer seams, scope-matched convergent evaluation of opportunity discovery vs long-horizon construction vs method learning vs simplification, or directly selecting an independently warranted bounded build. These are alternatives, not automatic stages.

## 10. Boundaries and handoff

- **No winner selected.** This document provides breadth and challenge, not a strategic disposition, implementation authorization, score, backlog or commitment to build all ideas.
- **No hidden causal claim.** A retrospective PR rationale, stored possibility, successful test or retrieved lesson does not establish original cognition, comparative superiority or transfer.
- **No compulsory evidence program.** Follow Q-2: construction can deliver value and learn through use; formal comparative qualification remains separate and should be undertaken only when its decision impact warrants the cost.
- **No authority laundering.** The active host retains semantic judgment; existing repository owner/ADR boundaries govern Skill, shared-method, protected-action and external-asset changes.
- **No unneeded architecture multiplication.** Before adding a controller, schema, policy or query, inspect the *existing* real consumer and ask what distinct agent behavior would change.
- **No forced opportunity quota.** Material diversity matters; a fixed number of candidates, modes, subagents or reflections is not a success metric.
- **No narrow-patch bias.** Bounded construction limits cost, risk and responsibility, not ambition. A meaningful end-to-end cognitive capability can be advanced incrementally without redefining the goal after each PR.
- **No automatic promotion to reviewed knowledge.** This exploration alone does not warrant new **poss:** records, new authored goals, new lessons or revision of existing hypothetical possibility statuses.

**Handoff question:** Which materially different construction direction creates the greatest credible value for a real agent while remaining compatible with existing consumer boundaries, construction-first policy and legitimate authority? Answer that separately from this divergent map; the strongest direction may be a reuse, integration, new consumer, sustained trajectory or simplification.
