# Context: Sensemaking Skills

## Current product definition

Sensemaking Skills is an **agent-native engineering sensemaking and control layer for software-engineering agents**. It helps an active coding agent move from repository uncertainty to **evidence-grounded, warranted next action** while preserving durable state across different scopes of repository development.

The repository now distinguishes four control scopes:

```text
LEVEL 4 — PRODUCT THESIS / STRATEGY REVISION
What product should this be, for whom, and why?
                    |
                    v
LEVEL 3 — STRATEGIC REPOSITORY EVOLUTION
What should change in the product/repository next?
                    |
                    v
LEVEL 2 — RESPONSIBILITY / CAMPAIGN
What bounded responsibility resolves the selected decision?
                    |
                    v
LEVEL 1 — EXECUTION
What concrete steps correctly perform the bounded work?
```

These are reasoning/control scopes, **not four runtime engines**. The active coding agent owns semantic judgment across the scopes permitted by current authority. Deterministic machinery supports mechanically decidable representation, validation, provenance, persistence, integrity, target identity, conformance, reference resolution under existing authoritative namespaces, and reconstruction.

The core control law is:

> **Lower levels may execute decisions delegated from higher levels, but they may not silently redefine commitments owned by the higher level.**

At Level 2, the product-level question remains:

> **Given the current goal, evidence, uncertainty, and authority, what responsibility is warranted next?**

A responsibility is **warranted** when it is supported by the current evidence, appropriate to the unresolved uncertainty, and permitted by the current authority/scope.

The active coding agent owns the recursive semantic control loop (ADR 0013). Sensemaking constrains that loop with repository evidence, bounded responsibilities, durable artifacts, validators, reconciliation, repair verification, authority boundaries, and higher-scope strategic state.

### Lifecycle positioning

Sensemaking is **cross-cutting, not an SDLC stage**. Software-engineering work contains nested feedback loops (discovery/definition/design/build/verify, and smaller loops inside each). The Sensemaking decision layer can operate across transitions where current evidence could change the warranted responsibility.

New evidence may warrant a responsibility conventionally considered earlier, later, or sideways in a lifecycle. These are evidence-grounded responsibility transitions, not backward/forward commands. Local mechanical iteration stays inside the selected responsibility until evidence puts that responsibility itself in question.

The Strategic Repository Evolution loop operates above bounded Campaign work. It evaluates product/repository capability state against current strategy, maintains the Strategic Frontier, selects or declines a repository-level responsibility, delegates bounded work downward, and reassesses after qualified results. It is not a roadmap processor and does not automatically rank work.

This clarification does not silently broaden external product scope. The current product definition remains an engineering sensemaking/control layer for software-engineering agents, and the ratified external product scope remains the validated, human-reviewed `repository_sensemaking_brief` defined by ADR 0014 unless Level-4 authority explicitly revises it.

See:
- [docs/product-strategy.md](docs/product-strategy.md) — Level-4 product thesis and strategic authority
- [docs/strategic-outer-loop.md](docs/strategic-outer-loop.md) — canonical four-level control model
- [docs/strategic-state-contract.md](docs/strategic-state-contract.md) — Level-3 durable strategic-state contract
- [docs/product-thesis-revision.md](docs/product-thesis-revision.md) — Level-4 revision and owner-ratification contract
- [docs/product-operating-model.md](docs/product-operating-model.md) — value stream, ownership, delegation, and escalation
- [docs/agent-native-operating-workflow.md](docs/agent-native-operating-workflow.md) — Level-2 agent-native responsibility/Campaign operating map
- [docs/operations-runbook.md](docs/operations-runbook.md) — current operator-facing validation, qualification, Campaign, and release runbook; checked-in workflows remain executable authority
- [docs/decision-orchestration-boundary.md](docs/decision-orchestration-boundary.md) — decision vs. orchestration ownership
- [docs/semantic-architecture/b7-semantic-reference-audit-design-preflight.md](docs/semantic-architecture/b7-semantic-reference-audit-design-preflight.md) — B7 reference-resolution boundaries and construction authority
- [docs/research/control-model-research-agenda.md](docs/research/control-model-research-agenda.md) — explicitly non-ratified research directions

## Empirical qualification context

The repository still retains the Goal A external-product-validation protocol and related evidence ceilings, but **new empirical experiments are currently deferred by owner direction**. Repository construction and mechanical qualification may continue when a concrete product/integrity/reconstruction capability has a mechanically bounded contract.

The canonical Goal A protocol remains [docs/research/goal-a-external-product-validation-protocol.md](docs/research/goal-a-external-product-validation-protocol.md). Its admissibility and claim ceilings remain valid; deferral does not convert missing empirical evidence into a PASS.

```text
Goal A protocol = CANONICAL
new Goal A execution = DEFERRED BY OWNER DIRECTION
A2 comparative work = DEFERRED / UNAUTHORIZED
native-harness / portability evidence = STILL OPEN
```

Keep distinct:

- **ratified current external product scope** = validated, human-reviewed `repository_sensemaking_brief` (ADR 0014);
- **broader orchestration/control architecture** = informs repository development and architecture, but is not silently promoted into external product scope;
- **repository qualification** = proves repository/mechanical contracts at an exact candidate state;
- **native-harness/product-value evidence** = remains unestablished where the relevant protocol requires it.

The owner-directed build-first rule does not delete empirical questions. It says those questions need not control the current construction phase while existing contracts can still resolve a concrete mechanical/reconstruction boundary.

## Top operating rule — Level 2

> **Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.**

The practical Level-2 loop is:

```text
GOAL / AUTHORIZED SCOPE
  -> identify nearest decision-changing uncertainty
  -> select the responsibility most likely to resolve it
  -> perform bounded work
  -> produce durable evidence/artifact
  -> validate mechanics
  -> interpret what the evidence warrants now
  -> continue / stop / escalate / ask owner / verify repair
```

This loop is recursive. New evidence may change the responsibility, the expected solution, or whether action is warranted at all.

Level 3 sits above this loop:

```text
CURRENT PRODUCT STRATEGY
  -> CURRENT CAPABILITY / REPOSITORY STATE
  -> STRATEGIC FRONTIER
  -> select or decline a strategic boundary
  -> warranted repository-level responsibility
  -> bounded Campaign / task
  -> qualified result + evidence
  -> update Level-3 state
  -> reassess
```

Level 4 activates only when evidence challenges a product-thesis commitment or the owner changes strategic intent.

## Core principles

1. **Responsibility before Skill** — decide what class of engineering work is warranted before choosing a Skill, tool, workflow, or patch.
2. **Evidence before commitment** — resolve the closest uncertainty that could change the next action instead of jumping to the desired final implementation.
3. **Artifacts are the API** — consequential information crosses responsibility boundaries through durable artifacts and declared inputs, not conversation memory.
4. **Finding is not authorization** — diagnosis, recommendation, implementation, validation, owner decision, publication, and closure are distinct lifecycle states.
5. **Validation is not closure** — deterministic PASS proves contract/mechanical properties, not analytical correctness, goal satisfaction, or repair of the original finding.
6. **Claims must reconcile to evidence** — material claims such as "implemented," "fixed," or "ready" should be checked against durable repository evidence when consequential.
7. **Repair requires finding-specific verification** — generic green CI is not proof that the diagnosed finding was closed.
8. **Authority is explicit** — distinguish what the agent may know, decide, act on, and publish/merge.
9. **Stop when the next action is stable** — do not investigate every possible uncertainty once remaining uncertainty cannot change the warranted next action.
10. **Harden only where pressured** — formalize new machinery when a stable, mechanically expressible boundary is actually justified.
11. **Strategic Frontier is not backlog** — a Level-3 possibility is not automatic work or authorization.
12. **Higher-level commitments are not silently rewritten** — Level 1 cannot redefine Level 2, Level 2 cannot redefine Level 3, and Level 3 cannot silently redefine Level 4.
13. **Reference resolution is not semantic warrant** — B7 may establish addressability/integrity under existing authorities; it does not establish currentness, relevance, support, or truth.

## Architecture and ownership

### Human owner

The human owner retains authority for mission, strategic intent, major product-thesis changes, authority grants, claim-ceiling expansion, and reserved merge/release/publication decisions.

### Active coding agent

The active software-engineering/coding agent owns semantic judgment within authorized scope. It:
- maintains the current goal and authorized scope;
- interprets repository state and artifacts;
- at Level 3, reconstructs current strategic state and selects or declines a strategic boundary;
- identifies decision-changing uncertainty;
- selects the next warranted responsibility;
- chooses an appropriate bounded capability;
- interprets resulting evidence;
- decides whether continuation, stopping, escalation, or an owner decision is warranted;
- escalates thesis-level contradictions rather than silently rewriting Level-4 commitments.

### Level 4 — Product Thesis / Strategy Revision

Level 4 owns the slower-changing product commitments: purpose, primary user, problem, JTBD, value proposition, product boundary, strategic principles, major non-goals, success measures, strategic bets, and evidence ceilings.

The authority surface is `docs/product-strategy.md`; revision semantics are defined in `docs/product-thesis-revision.md`. Major strategy changes require the authority specified there, including explicit owner ratification for owner-reserved commitments.

### Level 3 — Strategic Repository Evolution

Level 3 answers **what should change in the product/repository next, if anything**. It works from current strategy, capability/repository state, material gaps/contradictions/opportunities, and the Strategic Frontier.

`STATUS.md` is the current operational projection of Level-3 state. The conceptual contract is `docs/strategic-state-contract.md`.

Level 3 may select product-definition, product-design, architecture, domain-model, capability-development, implementation, integrity/hardening, simplification/removal, qualification, documentation-reconciliation, migration, or no-change responsibilities. These are responsibility classes, not fixed lifecycle stages.

### Level 2 — Sensemaking decision / Campaign layer

The Level-2 Sensemaking decision layer answers **what bounded responsibility should happen next** for the selected decision. It does not require a complete predetermined path to the final solution.

A Sensemaking Campaign is the durable Level-2 representation for bounded responsibility state, transitions, evidence, authority, artifacts, handoff, and continuation. Campaign machinery does not become a Level-3 strategic planner merely because strategic state exists above it.

### Skills

A Skill performs a **bounded responsibility** and produces a contracted artifact or evidence result. A Skill is not the whole product and should not absorb the full engineering lifecycle.

Representative responsibilities include:
- repository diagnosis: `repo-sensemaker`
- problem framing: `problem-framer`
- unknown mapping: `unknowns-mapper`
- planning: `workflow-planner`
- documentation/contract reconciliation: `sensemaking-docs-reconciler`
- completed-work claim audit: `output-reconciler`
- finding-specific repair verification: `repair-verifier`
- durable handoff: `handoff`

Ordinary coding work is also a valid bounded responsibility when the task is already mechanically narrow and sufficiently evidenced.

### Execution and orchestration — Level 1 support

Execution/orchestration answers **how an already-selected responsibility is coordinated and performed**. It may invoke a Skill, sequence deterministic substeps, resolve artifact paths, collect outputs, retry established execution steps, and return results to the active agent.

Registered workflows are bounded subgraphs inside the larger agent-owned loop. They are not the product-level controller and they are not the Strategic Outer Loop.

> **Decision selects the work. Orchestration coordinates the work. Evidence determines what becomes warranted next.**

Automatic fog-type-to-implementation routing is **not ratified product behavior**. Existing runtime routing paths are compatibility machinery unless separately ratified. Do not restore automatic downstream routing merely because a runtime path or registry field exists.

## Repository sensemaking and fog classification

`repo-sensemaker` turns user intent plus repository evidence into an evidence-grounded `repository_sensemaking_brief`. It identifies consequential boundaries, weakness patterns, relevant evidence, and remaining uncertainty.

The four canonical fog types remain useful **diagnostic metadata**:

| Fog type | Primary uncertainty |
| --- | --- |
| `product_fog` | user needs, feature scope, product workflow |
| `ui_fog` | interaction, navigation, design-system behavior |
| `docs_fog` | specifications, knowledge, documentation contracts |
| `architecture_fog` | code structure, boundaries, coupling, implicit contracts |

Fog classification can help describe the repository and inform planning. It does **not** by itself authorize a downstream implementation workflow. A `recommended_workflow_id` is a recommendation/planning field, not execution authority.

The brief is decision support, not repair authorization.

### MODEL_WARRANT authority (canonical; see ADR 0015 addendum)

Whether the brief's existing evidence environment is **sufficient for the current consequential reasoning problem** is a task-relative judgment. `representation_sufficiency` is that authoritative judgment supplied by the producer and mapped deterministically to `MODEL_WARRANT` (sufficient -> NO; contract-valid insufficient_bounded -> PARTIAL; inconclusive/missing/malformed -> INCONCLUSIVE; FULL deferred). Mechanical signals (behavioral flow, provenance spread, self-derived) are diagnostic evidence to that judgment, not independent vetoes. `MODEL_WARRANT` and the repository-action outcome are orthogonal; `NO_CHANGE` is affirmative-only; INCONCLUSIVE gates before representation materialization, action routing, and NO_CHANGE terminalization. Absence of evidence is never treated as insufficiency. The agent-mediated external product path is demonstrated on one fresh repository; product-wide GA and standard-CLI real-executor E2E are NOT claimed.

## Evidence model

Keep these categories distinct:

- **direct evidence** — observed directly in repository/tool state;
- **derived evidence** — mechanically calculated from direct evidence;
- **interpretation** — reasoned explanation of evidence;
- **hypothesis** — unresolved proposition requiring more evidence or a decision.

Do not flatten them into equivalent confidence.

Useful hierarchy:

```text
schema validity
!= evidence sufficiency
!= analytical correctness
!= usefulness
!= authorization
!= closure
```

The Probe Engine (`scripts/probe-repo.py`) provides measured repository state for `repo-sensemaker`. When a probe cannot evaluate a fact, that is not evidence of absence.

## Artifact and claim flow

Important durable artifacts include:

| Artifact | Role |
| --- | --- |
| `user_intent` | preserves the user's goal/scope context |
| `problem_frame` | frames the problem and constraints |
| `unknowns_map` | records unresolved unknowns/research needs |
| `repository_sensemaking_brief` | evidence-grounded repository diagnosis |
| `workflow_orchestration_plan` | optional procedural/planning artifact; not execution authority |
| `work_claim` | falsifiable statement of allegedly completed work |
| `reconciliation_report` | classifies work claims against durable evidence |
| `docs_contract_reconciliation_report` | records documentation/contract reconciliation |
| `repair_verification_report` | checks original findings against fresh evidence |
| `session_summary` / `prompt_handoff` | durable continuation/handoff state |

The canonical artifact contracts live in `skills/workflow-planner/references/artifact-contracts.yaml`.

## Validation, reconciliation, and verification

### Validation

Validation is deterministic/mechanical. It can establish that required fields exist, controlled vocabulary is valid, references resolve under declared contracts, paths satisfy contracts, and artifact structure is correct.

It cannot prove that the right evidence was selected, that a conclusion follows, that a recommendation is useful, that the Strategic Frontier is correctly prioritized, or that the original engineering problem is solved.

B7 reference audit is one bounded instance of mechanical validation: it can establish addressability/integrity only where current authoritative resolver context exists.

### Reconciliation

Reconciliation compares material work claims with durable repository evidence. The `artifact-reconciliation` registered workflow and `output-reconciler` Skill operationalize this responsibility.

Representative claim states include `verified`, `disputed`, and `omitted`.

### Repair verification

Repair verification asks whether a change actually closed the original finding. `repair-verifier` re-observes the repository and emits a `repair_verification_report`.

```text
implemented != validated != reconciled != repair-verified != authorized != integrated != closed
```

## Authority model

Treat authority as a parallel control track:

- **Can KNOW?** Inspect repository facts; use bounded probes for empirical facts; do not infer external reality without evidence.
- **Can DECIDE?** Reversible implementation details may be agent-decidable within scope; owner preference, policy, and owner-reserved product-thesis commitments remain owner decisions.
- **Can ACT?** Local reversible work depends on scope; external mutations require explicit authority.
- **Can PUBLISH / MERGE / DEPLOY?** Requires explicit authorization where the environment or project policy requires it.

Non-identities:

```text
finding        != authorization to fix
recommendation != owner decision
implemented    != verified
validated      != owner-ratified
promoted       != merged
merged         != original-finding closure
reference occurrence != reference resolution
reference resolution != semantic support
resolved       != current
not_addressable != invalid
product thesis != strategic state
Strategic Frontier != backlog
strategic boundary selected != implementation authorized
Level-3 state != Level-4 strategy authority
```

A correct terminal state can be: **the remaining uncertainty is no longer technical; it is an owner, strategic, or publication decision.**

## Stop and continuation conditions

Continue while:
- the goal is not yet satisfied;
- another responsibility is knowable and warranted;
- the agent has authority to perform it;
- repository safety permits continuation.

Stop when:
- the goal is genuinely satisfied;
- evidence shows further work is unwarranted;
- the next consequential action is stable and remaining uncertainty cannot change it;
- a genuine authority boundary is reached;
- repository safety requires stopping;
- authorized scope is exhausted.

Not every cycle ends in code. Valid outcomes include discovery, recommendation, reconciliation, retirement, escalation, owner handoff, strategy review, or a decision not to change anything.

Durable continuation should prefer:

```text
next agent/run -> reads durable artifacts -> reconstructs state
```

over dependence on transient conversation memory.

## Local-first and dependency boundary

The **core CLI/package is local-first**: repository inspection, artifact validation, registry/contract use, and most support utilities do not require an external model API or hosted Sensemaking service. Agent reasoning is supplied by the user's coding-agent harness.

The optional `exploratory_execution` subsystem may call the GitHub REST API for its approved experimental/campaign responsibilities. Do not generalize that optional integration into a requirement for the core product.

## Registered workflows and compatibility mechanics

The repository contains historical and current workflow/runtime machinery. Preserve the distinction between **mechanics that exist** and **product behavior that is ratified**.

- ADRs 0001-0012 document important validation, artifact, routing, invocation, and runtime mechanics and their history.
- ADR 0013 establishes the active agent as the primary control-loop owner.
- ADR 0014 settles the current external product boundary around evidence-grounded, human-reviewed repository sensemaking and defers automatic downstream routing.
- Registered workflows can remain useful bounded subgraphs or compatibility paths.
- Runtime support for a route does not give that route product-level authority.

The legacy CLI path may still expose planning/execution modes and registered workflow sequencing. Treat those as compatibility/execution features, not as a replacement for agent-reasoned responsibility selection.

## Source-of-truth map

| Resource | Purpose |
| --- | --- |
| `docs/product-strategy.md` | Level-4 product thesis: purpose, user, problem/JTBD, value, boundary, principles, non-goals, strategic bets, success measures, and evidence ceilings |
| `STATUS.md` | current Level-3 Strategic Repository Evolution state: capability state, Strategic Frontier, active boundary/responsibility, deferrals, evidence ceilings, and reassessment status |
| `docs/strategic-outer-loop.md` | canonical four-level control model and Level-3/Level-4 relationship |
| `docs/strategic-state-contract.md` | Level-3 durable state semantics and required projection contents |
| `docs/product-thesis-revision.md` | Level-4 strategy revision, escalation, disposition, and owner-ratification contract |
| `docs/product-operating-model.md` | current value stream, responsibility ownership, governance loop, delegation, escalation, and runtime boundary |
| `docs/agent-native-operating-workflow.md` | current Level-2 agent-native responsibility/Campaign operating map |
| `docs/operations-runbook.md` | current operator-facing local validation/qualification/Campaign/release runbook; checked-in workflows remain executable authority |
| `docs/decision-orchestration-boundary.md` | current decision/orchestration ownership boundary |
| `docs/canonical-vocabulary.yaml` | canonical enumerated vocabulary |
| `skills/workflow-planner/references/artifact-contracts.yaml` | artifact and machine-field contracts |
| `skills/workflow-planner/references/workflow-registry.yaml` | registered workflow/subgraph definitions |
| `skills/workflow-planner/references/skill-registry.yaml` | registered Skill/capability catalog |
| `skills/repo-sensemaker/references/evidence-rules.md` | repository-sensemaking evidence discipline |
| `docs/semantic-architecture/README.md` | semantic-model/reasoning/capability/substrate architecture; orthogonal to the four control scopes |
| `docs/semantic-architecture/b7-semantic-reference-audit-design-preflight.md` | B7 reference-resolution scope, authoritative resolver matrix, negative cases, and abort boundary |
| `docs/semantic-architecture/build-first-handoff.md` | B1–B7 repository qualification and continuation handoff |
| `docs/campaign-observability-and-portability.md` | Campaign observability, semantic companion, B7 reference audit rendering, Resume Capsule, replay/graph, and bundles |
| `docs/research/control-model-research-agenda.md` | non-ratified research hypotheses |
| `docs/research/goal-a-external-product-validation-protocol.md` | canonical external product-validation protocol; new execution currently deferred by owner direction |
| `docs/adr/` | ratified/proposed architecture decisions and historical rationale |

## Domain language

- **Sensemaking**: the broader decision/evidence/authority layer that moves engineering uncertainty toward warranted action.
- **Sensemaking Skills**: this repository/distribution and its bounded responsibility implementations/support machinery.
- **Product Thesis**: the Level-4 slower-changing commitments about product purpose, user, problem/JTBD, value, product boundary, strategic principles, major non-goals, success measures, strategic bets, and evidence ceilings.
- **Strategic Repository Evolution**: Level-3 reasoning over current product/repository capability state to determine what repository-level responsibility, if any, is warranted next under the current product thesis.
- **Strategic Frontier**: the currently material set of decision-relevant product/repository gaps, contradictions, opportunities, and unresolved boundaries. It is not a backlog and does not authorize work by itself.
- **Thesis Review**: Level-3 escalation when evidence challenges a Level-4 commitment or when the owner changes strategic intent; the outcome may reaffirm, reinterpret, revise, retire, or supersede strategy under the applicable authority.
- **Responsibility**: the class of work warranted by the current uncertainty/evidence state.
- **Skill**: a bounded implementation of a responsibility with declared inputs/outputs.
- **Workflow** (use qualified forms): `workflow-definition` (registry entry in `workflow-registry.yaml`), `workflow-recommendation` (`recommended_workflow_id` in brief), `workflow-selection` (`chosen_workflow_id` in plan), `workflow-execution` (runtime invocation). Bare `workflow` is ambiguous — always qualify.
- **Warrant**: the current justification for a responsibility, claim, or action from evidence + unresolved uncertainty + authority. Distinct from `MODEL_WARRANT` (system-computed gate) and `gate-approval` (human approval event).
- **MODEL_WARRANT**: deterministic task-relative gate (`NO | PARTIAL | INCONCLUSIVE`; `FULL` deferred) computed from authoritative `representation_sufficiency` judgment; diagnostic probes are telemetry only, never the warrant basis.
- **Representation Sufficiency** (`representation_sufficiency`): producer-authored judgment `{status: sufficient | insufficient_bounded | inconclusive, rationale, needed_representation}` that is the sole authority for `MODEL_WARRANT`.
- **NO_REPOSITORY_CHANGE_WARRANTED**: affirmative terminal outcome meaning no repository change is warranted on current evidence; mutually exclusive with `recommended_workflow_id` and orthogonal to `MODEL_WARRANT`.
- **Repository Sensemaking Brief**: evidence-grounded diagnostic artifact from `repo-sensemaker`.
- **Orchestration Plan** (`workflow_orchestration_plan`): optional procedural planning artifact; recommendation, not authority. `provisional` (pre-brief skeleton, may omit `primary_fog_type`) vs `canonical` (post-brief finalized, contract-valid).
- **Weakest Boundary**: the most consequential fragile/unenforced repository boundary identified by evidence.
- **Weakness Type**: closed taxonomy for the shape of the weakest boundary (`Vocabulary Drift`, `Contract Mismatch`, `Ghost Features`, `Safety Gaps`, `Implicit Dependencies`, `Zero Validation`, `Orphaned Examples`, or `Other` with explanation).
- **Extended Analysis** (`extended_analysis.domain` etc.): optional Section 15 multi-fog disclosure (`domain`, `consequential_boundary`, `uncertainty`, `owner_intent_state`); routing-inert, non-blocking, model-constrained.
- **Probe** (qualified): `state-currency probe` (`probe-report.yaml` measured fact) → `probe-evidence`; distinct from `repository-evidence` (inspectable file/git state) and `derived-evidence`. Never infer `FALSE` from absent probe.
- **Gate** (`gate_id`): human approval checkpoint (`review_repository_brief`, `review_workflow_plan`, etc.) with outcomes `approved | denied | needs_revision | none`; sentinel `none` means no gate required.
- **Execution Mode**: `plan_only | prompt_chain | guided_execution (default) | autonomous_execution | yolo_execution (compatibility-only)`; determines `gates_honored` and auto-approval criteria.
- **Validation** (`mechanical-validation`): deterministic contract checking. `Validation != evidence sufficiency != usefulness`.
- **Semantic reference audit**: B7 mechanical resolution/integrity check over existing authoritative reference families. It distinguishes `resolved`, `dangling`, `ambiguous`, and `not_addressable` without inferring currentness, support, relevance, or truth.
- **Reconciliation** (`claim-reconciliation`): comparison of `work_claim` against durable evidence → `reconciliation_report` (`verified | disputed | omitted`).
- **Repair verification** (`finding-repair-verification`): finding-specific post-change check via fresh probe → `repair_verification_report` (`closed | remaining`).
- **Authority boundary**: point where knowing/understanding is possible but deciding, acting, publishing, or merging is not authorized.
- **Harden Only Where Pressured**: formalize machinery after a stable, mechanically expressible failure/reconstruction/integrity boundary is justified; do not create runtime machinery merely to mirror a conceptual diagram.

## Current product boundaries and open edges

Current, ratified/operationally grounded:
- agent-native semantic control by the active coding agent;
- canonical four-level control architecture as repository documentation/authority model;
- Level-4 product strategy authority and Level-3 strategic-state projection;
- repository sensemaking + Brief;
- bounded Skills and artifact contracts;
- deterministic validation;
- output reconciliation;
- repair verification;
- authority-aware stopping/escalation discipline;
- Campaign persistence, provenance, observability, handoff, and bounded portability;
- B7 semantic-reference resolution/audit under existing Campaign/semantic-state authorities;
- repository-qualified Semantic Architecture B1–B7 substrate and PM source-capability migration within their stated evidence ceilings.

Not automatically ratified merely because related machinery or concepts exist:
- an `OuterLoopEngine` or deterministic `StrategicPlanner`;
- automatic Strategic Frontier ranking;
- automatic product-thesis revision;
- automatic Campaign generation from Level-3 state;
- deterministic fog-type routing as product control policy;
- a universal centralized orchestrator;
- one registered workflow that encodes the whole Sensemaking loop;
- a universal semantic-reference registry or universal Claim/Evidence identity layer;
- automatic external mutation/publication authority;
- domain-general research-agent control semantics;
- new decision-theory/control-model machinery from the research agenda.

The product should deepen through repository-grounded construction while architecture remains informative. Preserve observations, identify concrete failure/reconstruction/integrity boundaries, and formalize only mechanically bounded support. The Strategic Outer Loop v0 control model is now a frozen operational baseline: use it during normal repository evolution, and reopen outer-loop construction only from new concrete pressure or explicit owner direction. When the decisive question becomes behavioral product value rather than repository/mechanical correctness, stop construction at that boundary unless the owner explicitly reauthorizes empirical work.