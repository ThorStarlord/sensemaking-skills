# Value-Directed Continuous Construction (Architect + Builder)

**Status:** Owner-endorsed operating guidance for the current `sensemaking-skills` CONSTRUCTION phase (2026-10-26).  
**Scope:** How an active coding agent or delegated builder chooses, constructs, integrates, learns from, and continues ordinary repository responsibilities.  
**Authority:** [product strategy](product-strategy.md) and [ADR 0031](adr/0031-persistent-semantic-stewardship.md) govern the product destination; [ADR 0029](adr/0029-current-product-boundary.md) governs the external boundary; [STATUS.md](../STATUS.md) and current reconciled Level-3 artifacts govern repository direction; [CLAUDE.md](../CLAUDE.md) governs the current local verification/merge discipline. This guide creates no additional authority.

**Working label:** *Value-Directed Continuous Construction* is a descriptive name for the owner's working preference, not a standardized methodology, another strategic level, a registered Skill, or an executable planner.

**Document roles:** This page states the construction philosophy and product-value policy. The [agent build loop](agents/build-loop.md) applies it to one PR: a proportional Architect/Builder/Close cycle with a brief decision note. `CLAUDE.md` provides the short entry trigger and the current integration/verification rules. These pages complement one another; they are not competing control layers.

## 1. Build toward product value, not activity volume

The selected Level-4 destination is **Persistent Semantic Stewardship**: source-grounded, typed, queryable knowledge of product intent, domain, capabilities, architecture, evidence, decisions, and history that later coding agents can reuse and challenge. ADR 0031 selects that destination; continuous product-grounded development is its operating/learning loop, while lean decision assistance remains appropriate for simple tasks.

The intended product outcome is twofold:

1. **Better software:** an intrinsically useful, retained capability or reduction of real product/engineering friction.
2. **Better later decisions:** consequential, source-linked understanding that another engineering episode can correctly retrieve, challenge, and use.

Neither the number of commits, pull requests, Skills, ontology entries, tests, nor documents is itself a product-value metric. A small fix can be more valuable than a large abstraction; a warranted new capability can be more valuable than the most convenient local repair. No product benefit or longitudinal improvement is established merely by building or indexing it.

## 2. Reconstruct the governing context before selecting work

Read **selectively**, with current source identity and explicit authority:

| Need | Start here | Governing role |
| --- | --- | --- |
| Product definition and non-goals | [CONTEXT.md](../CONTEXT.md), [product-strategy.md](product-strategy.md), ADRs [0031](adr/0031-persistent-semantic-stewardship.md) and [0029](adr/0029-current-product-boundary.md) | Level 4 purpose and external boundary |
| Current development direction | [STATUS.md](../STATUS.md), [persistent stewardship plan](persistent-semantic-stewardship-plan.md), the current [strategic analysis](../artifacts/history/2026-10-23-strategic-repository-analysis.md) and [reconciliation](../artifacts/history/2026-10-24-strategic-reconciliation.md) | Level 3 compass and historical decision lineage; check for later reconciliations |
| Working authority and verification | [AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md), applicable ADRs, actual GitHub protections/CI | What the agent may change, merge, or claim |
| Semantic and architecture context | [Semantic Architecture](semantic-architecture/README.md), [ontology](semantic-architecture/ontology.md), [relations and epistemics](semantic-architecture/relations-and-epistemics.md), and reviewed `.sensemaking/knowledge/*.json` | Meanings, constraints, owners, relationships, and source-linked rationale; not action authority |
| Implementation reality | Current code, consumers, contracts, Git history, observed runs and CI | What exists and what a change could affect |

The root `roadmap.md` and `goal.md` explicitly mark themselves **historical/superseded**. Do not promote either to the current construction backlog. A plan is a **compass**, not a proof of correctness or an instruction to implement every listed item. Favor current, semantically applicable decisions over file recency or a familiar filename.

The current Level-3 PATH-1 direction is to **accrete useful product knowledge through genuine engineering responsibilities**. A new prompt, a completed earlier task, ordinary code drift, or a visible issue does not automatically reopen the Level-3 strategic analysis.

## 3. Architect and Builder are complementary responsibilities

**Architect:** understand the product goal, affected capabilities and boundaries; consider distinct options and their downstream consequences; decide what would make the system better.

**Builder:** implement a bounded valuable change; inspect the real consumers and contracts; integrate it within authority; observe its consequences.

The two responsibilities can operate in the same agent and working context, and may interleave as implementation reveals new facts. Do not create a separate architect/worker pipeline or approval ceremony for an otherwise clear, authorized fix. Every PR retains a brief decision note; clear local repairs can document the chosen responsibility in two sentences. A material in-scope design revision updates that note, while a changed outcome or authority returns to selection.

Use **divergent then convergent exploration** in proportion to the decision:

- At a genuine Level-3 `ANALYZE` / `REOPEN_ANALYSIS` boundary, follow the existing [Strategic Exploration Funnel](../skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md): system map -> breadth of grounded opportunities and counterfactual alternatives -> frontier candidates -> depth on plausible finalists -> comparison -> selected path and bounded responsibility. Explore both missing capabilities and novel combinations/simplifications; do not treat the issue queue as the full product frontier.
- At a settled `RESPONSIBILITY` / `EXECUTE` boundary, explore only the materially different **local design alternatives**. Do not rerun a repository-wide funnel simply because a feature is being built.
- At either scope, distinguish **governing commitments**, **observed implementation**, **revisable design choices**, and **hypotheses**. An imagined solution is not evidence that it works, and an existing implementation is not proof that its design must be preserved.

**Converge on the highest-value sufficiently warranted and authorized responsibility**, not the highest PR count or lowest-risk action by default.

## 4. Choose construction using product value and opportunity cost

For material alternatives, compare qualitatively:

- **Product outcome:** which user/agent task becomes easier, safer, possible, or less costly?
- **Retained leverage:** what capability is reusable, and what future meaningful decisions can it inform?
- **Architecture and fit:** does it strengthen the accepted product definition and respect boundaries?
- **Evidence and uncertainty:** what actual sources support the need, and what would change the choice?
- **Total costs:** implementation, maintenance, ambiguity, complexity, future rework, and delayed opportunity.
- **Downside, reversibility, authority:** what happens if the design is wrong, and what is safe to change now?

A **reversible build** is often preferable to an isolated experiment followed by reimplementing the same useful feature, provided the build is already warranted, the downside is acceptable, and normal use can supply enough evidence for the current decision. This is a conditional preference, not permission to turn every idea into code.

Do not always choose the smallest patch, the largest feature, or the next old roadmap item. Do not manufacture work to keep a Campaign alive. Correct deferment, stopping, and removing an unhelpful abstraction can also be valuable decisions.

## 5. "Continuous Construction IS the Probe" has a bounded meaning

This phrase expresses an **architect-and-builder construction posture**: retain useful changes, learn from real implementation and subsequent use, and avoid turning synthetic experiments or perfect documentation into prerequisites for every worthwhile increment.

It is **not** a formal claim that every construction increment is an experimental probe, that merged code is correct, or that a new interface improves downstream agent performance.

Keep three evidence questions separate:

| Question | Appropriate evidence |
| --- | --- |
| Did we create the intended retained capability? | Source/diff review, integrated artifact, relevant mechanical observations |
| Does its declared behavior work correctly within scope? | Proportionate verification, contract checks, existing CI, runtime/behavioral evidence as required |
| Does the capability improve agent outcomes over time? | Genuine later-episode use, correct knowledge reuse/correction, and comparative evidence when a comparative claim is made |

**Current local construction exception:** For the owner's current `sensemaking-skills` construction PRs, [CLAUDE.md](../CLAUDE.md) directs agents **not to add or manually run local unit or synthetic evidence tests**. Do source inspection, review the diff, run relevant non-test static/mechanical checks where appropriate, and state `NOT_RUN` accurately. The owner separately chose **prompt merge after clean review without waiting for hosted CI**; CI still runs, and any post-merge substantive failure warrants a bounded repair. Existing branch protections and release-qualification contracts remain intact. This phase- and repository-scoped exception does not erase the ordinary verification policy or justify knowingly integrating a consequential defect.

The earlier [build-first Semantic Architecture policy](semantic-architecture/build-first-policy.md) distinguishes mechanical verification from further empirical validation and remains relevant in its original scope. Apply the newer explicit construction exception to local test execution without rewriting previous qualifications.

When the decisive uncertainty is user/agent benefit, repeated stale knowledge, maintenance cost, or competing architectures that construction cannot discriminate, reassess the value of further implementation. Do not invent S5/S6, release-readiness, or causal claims.

## 6. Make semantic context useful, not mandatory ceremony

When domain meaning, component ownership, rules, past decisions, or architectural tradeoffs could change an implementation, follow the existing [Repository Semantic Steward](../skills/repository-semantic-steward/SKILL.md) **RECALL -> BUILD -> RECONCILE** practice:

1. **RECALL:** identify current Git revision and precise engineering question. Retrieve bounded, relevant source-pinned context using the existing semantic query/index if available. Inspect original cited documents and code. A missing index or `NOT_ASSESSED` result is not a stop sign or proof of absence.
2. **BUILD:** act on the warranted responsibility in the active context; preserve component contracts, scope and the distinction between real source facts and inference.
3. **RECONCILE:** record only consequential, non-obvious knowledge that can improve a later decision; preserve provenance, alternatives, contradiction, supersession and uncertainty. Do not create graph records to fill quotas or a second manual truth.

Keep these concepts distinct:

- **Ontology:** concepts and relationship meanings (not a mandate to model everything).
- **Architecture:** responsibilities, components, interfaces, boundaries and dependencies.
- **Design:** choices, alternatives and rationales for realizing capabilities.
- **Schema/executable contracts:** representations and mechanical validation; see `src/sensemaking_skills/semantic_architecture/knowledge.py`.
- **Reviewed knowledge/index:** bounded source-linked projections, not semantic truth, code reality, owner intent, or permission to act.

Read `semantic-architecture/ontology.md` and related references as needed; do not load the entire graph or rebuild an index merely to perform a clear bounded edit. Unratified proposals (including the current proposed status of ADR 0033) are not automatically binding Level-4 product decisions.

## 7. Integrate promptly within real authority

For each independent construction increment:

1. Establish the bounded responsibility, relevant contract and current source identity. Put a **brief decision note in every PR**, proportional to the choice.
2. Implement and review the change against actual consumers, applicable product intent, and the authorization boundary. If an in-scope design improves, update the note; return to selection for changed outcome/scope/authority.
3. Preserve consequential documentation/semantic knowledge without creating an entry in `STATUS.md` for routine work. PR description and Git history retain ordinary increment evidence.
4. Use one `claude/<topic>` branch per PR; inspect the proposed diff, base/head, reviewability and mergeability.
5. **Merge authorized construction PRs promptly after clean source/diff review, without waiting for hosted CI or local unit/evidence tests** (owner choice 2026-10-26). Existing GitHub CI continues to run; do not bypass required checks, disregard an already-known material failure, force-push around protections or knowingly integrate a consequential defect.
6. Verify GitHub reports a merge and the resulting commit is on `main`. State CI as pending, passing or failing only from observed results, and investigate a meaningful post-merge failure as the next warranted repair responsibility.
7. Read the merged result before selecting the next independent worthwhile responsibility. Stopping remains valid when no further warranted action exists.

Owner delegation covers ordinary repository-answerable engineering and authorized construction merges; it does **not** unilaterally grant release/deployment, secrets/billing changes, destructive unrelated mutations, Level-4 thesis revision or a new external product scope. Respect enforced policy and repository rules regardless of their current configuration.

## 8. Keep the next agent's context small and durable

At the beginning of a new development episode, the agent should establish:

```text
PRODUCT: current accepted purpose, users, non-goals and evidence ceiling
STRATEGY: current PATH/frontier, later reconciliations and real next decision
SOURCE: repository identity and checked-out HEAD; relevant code/consumers
ARCHITECTURE: targeted constraints, domain meaning, component ownership and decisions
AUTHORITY: current construction/verification policy and protected transitions
RESPONSIBILITY: one warranted product outcome and its likely consequences
```

After the episode, report a compact decision trace:

```text
PRODUCT VALUE: meaningful capability created, simplified or repaired
ALTERNATIVES: materially different options considered and why one was chosen
INTEGRATION: changed sources, PR, actual merge/main commit (or blocker)
KNOWLEDGE: what RECALL changed and what was corrected or retained
EVIDENCE LIMITS: source review, mechanical checks, observed CI, NOT_RUN claims
CONTINUATION: next independently warranted responsibility or justified stop
```

Retain a brief decision note in each PR, then adapt the detail of its final readout to the consequence of the work; it is not a requirement to write every field for trivial fixes. The retained sources are the authority. This report is an orientation/handoff aid, **not** a new master strategy file, a planner result or a reason to reopen settled analysis.

**Compact principle:** Build when product value, evidence and authority support a useful bounded increment; explore when alternatives could change that decision; verify to the level required by the claim; reconcile learning so the next agent can reason from better sources.
