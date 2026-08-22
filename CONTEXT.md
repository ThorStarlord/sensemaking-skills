# Context: Sensemaking Skills

## Current product definition

Sensemaking Skills is an **agent-native engineering sensemaking and control layer for software-engineering agents**. It helps an active coding agent move from repository uncertainty to **evidence-grounded, warranted next action**.

The product-level question is not "which predefined workflow node runs next?" It is:

> **Given the current goal, evidence, uncertainty, and authority, what responsibility is warranted next?**

A responsibility is **warranted** when it is supported by the current evidence, appropriate to the unresolved uncertainty, and permitted by the current authority/scope.

The active coding agent owns the recursive control loop (ADR 0013). Sensemaking constrains that loop with repository evidence, bounded responsibilities, durable artifacts, validators, reconciliation, repair verification, and authority boundaries.

See:
- [docs/agent-native-operating-workflow.md](docs/agent-native-operating-workflow.md) — current end-to-end operating map
- [docs/decision-orchestration-boundary.md](docs/decision-orchestration-boundary.md) — decision vs. orchestration ownership
- [docs/research/control-model-research-agenda.md](docs/research/control-model-research-agenda.md) — explicitly non-ratified research directions

## Top operating rule

> **Resolve the nearest unresolved decision-changing uncertainty before committing to the eventual solution.**

The practical loop is:

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
10. **Harden only where pressured** — formalize new machinery when repeated real use exposes a stable, mechanically expressible failure boundary.

## Architecture and ownership

### Active coding agent

The active software-engineering/coding agent owns the top-level loop. It:
- maintains the current goal and authorized scope;
- interprets repository state and artifacts;
- identifies decision-changing uncertainty;
- selects the next responsibility;
- chooses an appropriate bounded capability;
- interprets resulting evidence;
- decides whether continuation, stopping, escalation, or an owner decision is warranted.

### Sensemaking decision layer

The Sensemaking decision layer answers **what responsibility should happen next**. It does not require a complete predetermined path to the final solution.

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

### Execution and orchestration

Execution/orchestration answers **how an already-selected responsibility is coordinated and performed**. It may invoke a Skill, sequence deterministic substeps, resolve artifact paths, collect outputs, retry established execution steps, and return results to the active agent.

Registered workflows are bounded subgraphs inside the larger agent-owned loop. They are not the product-level controller.

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

Validation is deterministic/mechanical. It can establish that required fields exist, controlled vocabulary is valid, references resolve, paths satisfy contracts, and artifact structure is correct.

It cannot prove that the right evidence was selected, that a conclusion follows, that a recommendation is useful, or that the original engineering problem is solved.

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
- **Can DECIDE?** Reversible implementation details may be agent-decidable within scope; owner preference, policy, and canonical authority remain owner/ADR decisions.
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
```

A correct terminal state can be: **the remaining uncertainty is no longer technical; it is an owner or publication decision.**

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

Not every cycle ends in code. Valid outcomes include discovery, recommendation, reconciliation, retirement, escalation, owner handoff, or a decision not to change anything.

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
- ADR 0014 settles the current product boundary around evidence-grounded, human-reviewed repository sensemaking and defers automatic downstream routing.
- Registered workflows can remain useful bounded subgraphs or compatibility paths.
- Runtime support for a route does not give that route product-level authority.

The legacy CLI path may still expose planning/execution modes and registered workflow sequencing. Treat those as compatibility/execution features, not as a replacement for agent-reasoned responsibility selection.

## Source-of-truth map

| Resource | Purpose |
| --- | --- |
| `docs/agent-native-operating-workflow.md` | current top-level operating map |
| `docs/decision-orchestration-boundary.md` | current decision/orchestration ownership boundary |
| `docs/canonical-vocabulary.yaml` | canonical enumerated vocabulary |
| `skills/workflow-planner/references/artifact-contracts.yaml` | artifact and machine-field contracts |
| `skills/workflow-planner/references/workflow-registry.yaml` | registered workflow/subgraph definitions |
| `skill-registry.yaml` | registered Skill/capability catalog |
| `skills/repo-sensemaker/references/evidence-rules.md` | repository-sensemaking evidence discipline |
| `docs/adr/` | ratified/proposed architecture decisions and historical rationale |
| `docs/research/control-model-research-agenda.md` | non-ratified research hypotheses |

## Domain language

- **Sensemaking**: the broader decision/evidence/authority layer that moves engineering uncertainty toward warranted action.
- **Sensemaking Skills**: this repository/distribution and its bounded responsibility implementations/support machinery.
- **Responsibility**: the class of work warranted by the current uncertainty/evidence state.
- **Skill**: a bounded implementation of a responsibility with declared inputs/outputs.
- **Workflow**: a registered, mechanically expressible sequence/subgraph; not automatically the top-level control loop.
- **Warrant**: the current justification for a responsibility, claim, or action from evidence + unresolved uncertainty + authority.
- **Repository Sensemaking Brief**: evidence-grounded diagnostic artifact from `repo-sensemaker`.
- **Orchestration Plan**: optional procedural planning artifact; recommendation, not authority.
- **Weakest Boundary**: the most consequential fragile/unenforced repository boundary identified by evidence.
- **Probe**: bounded empirical observation used when repository text alone cannot establish reality.
- **Validation**: mechanical contract checking.
- **Reconciliation**: comparison of claims against durable evidence.
- **Repair verification**: finding-specific post-change verification.
- **Authority boundary**: point where knowing/understanding is possible but deciding, acting, publishing, or merging is not authorized.
- **Harden Only Where Pressured**: formalize machinery after repeated real-use pressure exposes a stable failure boundary.

## Current product boundaries and open edges

Current, ratified/operationally grounded:
- agent-native top-level loop;
- repository sensemaking + Brief;
- bounded Skills and artifact contracts;
- deterministic validation;
- output reconciliation;
- repair verification;
- authority-aware stopping/escalation discipline.

Not automatically ratified merely because related machinery exists:
- deterministic fog-type routing as product control policy;
- a universal centralized orchestrator;
- one registered workflow that encodes the whole Sensemaking loop;
- automatic external mutation/publication authority;
- domain-general research-agent control semantics;
- new decision-theory/control-model machinery from the research agenda.

The product should deepen through normal engineering use: preserve observations, identify repeated failure boundaries, and formalize only when the evidence warrants it.
