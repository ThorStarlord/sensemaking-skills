# Status

**Version:** 0.2.2  
**Last updated:** 2026-09-08  
**Current phase:** Productization / implementation  
**Primary program:** Sensemaking Skills v0.3 campaign-based productization

This is the repository's living status summary. It points at authoritative design sources and current implementation direction; it is not itself an ADR or an execution authorization.

## What the product is

Sensemaking Skills is an **agent-native engineering sensemaking and control layer for software-engineering agents**.

The active coding agent owns the semantic control loop. Sensemaking constrains that loop with repository evidence, bounded responsibilities, durable artifacts, deterministic validators, reconciliation, repair verification, authority boundaries, and now typed campaign state.

It is not a centralized semantic router, autonomous project manager, or universal multi-agent orchestrator.

Current architectural authority remains grounded in the accepted ADRs and current operating docs, especially:

- ADR 0013 — the active coding agent owns the top-level control loop;
- ADR 0014 — the evidence-grounded repository-sensemaking brief is the ratified core product boundary and automatic downstream routing is deferred;
- ADR 0015 addendum — representation sufficiency / MODEL_WARRANT;
- ADR 0023 — experiment authorization separation;
- ADR 0026 / 0027 — execution authority is distinct from recommendation/selection, and workflow catalog identity is distinct from liveness;
- `docs/agent-native-operating-workflow.md` — current operating map;
- `docs/decision-orchestration-boundary.md` — semantic decision vs deterministic orchestration boundary.

## Owner productization decision — 2026-09-08

The repository is moving from **research/experiment-first development** to **implementation/productization-first development**.

The default development loop is now:

```text
identify a user-visible capability
→ implement the smallest complete vertical slice
→ validate deterministically
→ dogfood in ordinary engineering use
→ repair observed friction
→ ship the slice
```

Formal experiments are no longer the normal next step. They are reserved for consequential product uncertainties that ordinary implementation and dogfood evidence cannot resolve.

The detailed active plan is:

[`docs/productization-v0.3.md`](docs/productization-v0.3.md)

## Current implementation baseline

`main` at the productization pivot is:

`5c2c807542f7e150d4a031430f59e297ed816b24`

That merge integrated PR #277, adding the typed campaign-semantic contract and strict I/O boundary:

- `CampaignState`;
- `Responsibility`;
- `Uncertainty`;
- `Authority`;
- typed dependencies;
- `TransitionRecord`;
- `CampaignPolicy`;
- `CampaignHandoff`;
- `CampaignTrace`;
- `CapabilityRegistry` / availability semantics;
- strict campaign YAML load/dump boundaries;
- semantic round-trip qualification.

Those types are deliberately structural. They do not judge semantic sufficiency and do not take control away from the coding agent.

## Current productization objective

The v0.3 north-star outcome is:

> A coding agent can start a durable Sensemaking Campaign on a real repository, consume validated agent-native diagnostic artifacts, record the warranted responsibility and authority, perform bounded work, validate/reconcile the result, hand the campaign to a fresh agent, and continue or terminate without relying on prior conversation memory.

The intended lifecycle is:

```text
user goal
→ campaign init
→ repository sensemaking
→ validated artifact
→ agent chooses responsibility
→ campaign records decision + authority
→ bounded capability / ordinary coding
→ validation / reconciliation
→ durable transition
→ handoff / continue / stop
```

## Current implementation boundary

The immediate build sequence is deliberately vertical and bounded:

1. **P0 — Productization pivot**: make the new development regime durable and stop treating formal experiment execution as the active program.
2. **P1 — Durable campaign workspace**: file-backed, isolated campaign persistence around the already-merged `campaign_semantics` types.
3. **P2 — Campaign service**: deterministic lifecycle operations, including atomic state+transition commits.
4. **P3 — Campaign CLI foundation**: real `campaign init/status/validate/history` commands.
5. **P4/P5 — Artifact ingestion + agent-authored transition decisions**.
6. **P6 — Real capability registry**, without automatic routing.
7. **P7 — Durable handoff/resume**.
8. **P8/P9 — Artifact lineage + reconciliation lifecycle**.
9. **P10/P11 — harness adapters + v0.3 release qualification**.

## Semantic-control invariant

The implementation must preserve this separation:

```text
Agent:
  What does the evidence mean?
  Which responsibility is warranted?
  Which available capability should be selected?

Deterministic machinery:
  Is the representation valid?
  Is state persisted safely?
  Does authority metadata permit the claimed action?
  Is the transition structurally reconstructible?
  What durable evidence and history exist?
```

Therefore:

```text
validator passed != conclusion is true
capability exists != capability should be selected
capability available != execution authorized
recommendation != execution authority
```

## Research and experiment disposition

Prior research remains useful evidence and is preserved. It is no longer the default active product program.

### EXP-0006 / Empirical Skill Qualification v1

The experiment may stop at the actual completed boundary under the owner's productization pivot.

Preserve:

- the three D attempts and their exact outcomes;
- the frozen Q/T holdout identity and integrity record;
- the candidate-context contamination audit;
- the fact that no candidate was authored before the contamination event;
- all existing exploratory/non-canonical claim ceilings.

Do not manufacture a Skill candidate or continue Q/T execution merely to complete the experimental mechanism. Do not relabel incomplete work as a completed scientific conclusion.

### Goal A and other research lanes

Goal A, the standing normal-use evidence lane, control-model studies, and other research artifacts remain available as evidence/research surfaces. They are not the primary development queue unless a later owner decision explicitly reactivates them.

## Explicit non-goals for v0.3

Do not build by default:

- centralized semantic routing;
- HTN/generic planning;
- Skill ranking;
- critic/voting swarms;
- self-modifying Skills;
- autonomous SkillOpt optimization;
- campaign server/database/cloud backend;
- universal semantic truth validation;
- automatic external mutation authority;
- full multi-repository campaign control.

## Definition of v0.3 success

The first campaign-based release is successful when a real agent can:

```text
start
→ consume diagnosis
→ record responsibility
→ bind authority
→ inspect available capability
→ record work evidence
→ transition
→ handoff
→ resume in a fresh context
→ stop honestly
```

with deterministic state reconstruction and without requiring the prior conversation as hidden input.

## Where to look

| Topic | Source |
|---|---|
| Product definition, principles, authority model | `CONTEXT.md` |
| Active v0.3 productization plan | `docs/productization-v0.3.md` |
| Agent-native operating model | `docs/agent-native-operating-workflow.md` |
| Decision vs orchestration boundary | `docs/decision-orchestration-boundary.md` |
| Campaign semantic contract | `docs/campaign-semantics.md`, `src/sensemaking_skills/campaign_semantics/` |
| Workflow catalog/liveness | `docs/workflow-system-disposition.md`, ADR 0027 |
| Design decisions | `docs/adr/` — always read each ADR's status |
| Historical research/evidence | `experiments/`, `docs/research/`, `docs/campaigns/` |
| Installation and usage | `README.md`, `GETTING_STARTED.md`, `INSTALLATION.md` |
