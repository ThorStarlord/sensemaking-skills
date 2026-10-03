# Sensemaking / Dark Factory Autonomy Boundary

**Status:** current architecture clarification / owner decision  
**Date:** 2026-10-02  
**Scope:** relationship between `sensemaking-skills` and `ThorStarlord/dark-factory` for full-autonomy / full-delegation software-production work  
**Authority:** clarifies ownership and product boundaries; creates no runtime authority, release authority, or new Skill

## 1. Decision

`sensemaking-skills` and Dark Factory have different responsibilities.

```text
sensemaking-skills
= semantic R&D + reusable repository decision-support Skills
+ evidence / warrant / authority doctrine
+ interactive terminal-mission front door

Dark Factory
= canonical durable software-factory runtime
+ Goal / Frontier / Delegation / Campaign state
+ evidence admission / assurance / integration / continuation / stopping

Archon / bounded executors
= model and SDLC execution beneath already-warranted Dark Factory work
```

Mature semantic-control ideas may be incubated, clarified, or qualified in
`sensemaking-skills`, then deliberately reconciled into Dark Factory when the
runtime product needs them. Once Dark Factory owns a mature runtime behavior,
Sensemaking must not create a competing runtime controller merely to mirror it.

```text
upstream semantic provenance
!= downstream runtime ownership

reusable Skill guidance
!= canonical factory state

full autonomy
!= duplicate control loops
```

Dark Factory's own architecture and qualification records are authoritative for
what the factory runtime currently implements and has qualified.

## 2. Full autonomy / full delegation

Within `sensemaking-skills`, the existing
`strategic-sensemaking-loop` + Autonomous Terminal Mission profile remains the
single reusable front door for an active agent asked to pursue a repository
terminal outcome with FULL AUTONOMY / FULL DELEGATION.

Do **not** add a second generic `full-autonomy` or
`full-autonomy-and-full-delegation` Skill.

The reason is structural, not naming preference:

```text
new generic Full Autonomy Skill
-> duplicates terminal-mission orchestration
-> creates competing ownership
-> risks diverging authority / stopping semantics

existing strategic-sensemaking-loop
-> already owns reusable semantic continuation

Dark Factory
-> owns durable factory-runtime continuation
```

A Skill may orchestrate or operate an existing runtime; it must not become a
second source of Goal, Frontier, Campaign, evidence, or transition truth.

## 3. Dark Factory relationship

Dark Factory is the canonical successor runtime for the closed-loop
software-production objective that combines:

- bounded authorized product intent;
- repository-grounded strategic assessment;
- warranted responsibility selection;
- standing delegation for ordinary repository-answerable work;
- Campaign execution;
- admitted evidence and assurance;
- protected transition authority;
- post-integration observation;
- exact-revision reassessment;
- continued work only when a material difference remains; and
- correct stopping or escalation.

Dark Factory E2E-6 records a bounded qualification of serial delegated strategic
continuation through two integrated Campaigns followed by a correct final stop.
That is downstream runtime evidence. It does **not** promote the
`sensemaking-skills` normal-use claim ceiling into a general proof that the
interactive Skill path is universally reliable.

```text
Dark Factory serial-continuation qualification
!= general Skill reliability proof

Dark Factory runtime ownership
!= Sensemaking semantic R&D is obsolete
```

## 4. Operator-front-door candidate

A future `dark-factory-mission` Skill is a legitimate candidate only as an
**operator/front-door adapter to Dark Factory**, not as another autonomy brain.

Its expected contract would be:

### Input

- target repository or already-existing Dark Factory mission identity;
- terminal Goal / desired repository outcome;
- authority envelope;
- protected-transition grants or reservations;
- validation / qualification policy;
- optional execution-provider constraints.

### Responsibility

- initialize or resume the correct Dark Factory mission;
- inspect durable Goal / Frontier / Delegation / Campaign state;
- translate explicit owner intent into existing Dark Factory interfaces without
  inventing new semantic state;
- operate or dispatch already-authorized runtime actions;
- surface evidence, blockers, protected boundaries, and terminal state;
- resume through Dark Factory rather than manually bypassing it.

### Output

- concise current mission state;
- Dark Factory actions actually performed;
- returned evidence and qualification state;
- exact protected boundary or terminal stop when reached.

### Non-goals

The candidate must not:

- independently select a second Strategic Frontier when Dark Factory already owns
  the current Frontier;
- maintain a parallel Goal / Campaign database;
- reinterpret worker success as factory closure;
- infer merge/release/deploy/credential/billing authority;
- bypass Dark Factory and perform the delegated implementation manually merely
  because the active ChatGPT agent can do so;
- duplicate the generic `strategic-sensemaking-loop` terminal-mission semantics.

```text
Dark Factory operator Skill
= interface to the autonomy runtime

Dark Factory operator Skill
!= autonomy runtime
!= second strategic controller
```

## 5. Current implementation disposition

The operator Skill is **candidate-only** for the frozen `1.0.0rc3` line.

Do not add it to the current shipped Skill catalogue merely from architectural
attractiveness. A new shipped Skill is warranted when a concrete Dark Factory
operator consumer exists and the available tool/connector/CLI surface is stable
enough that the Skill can actually initialize, resume, inspect, and operate the
runtime reliably.

Until then:

```text
CURRENT SENSEMAKING CONSTRUCTION RESPONSIBILITY = NONE
GENERIC FULL AUTONOMY SKILL = REJECTED AS DUPLICATE
DARK FACTORY OPERATOR SKILL = CANDIDATE_EXTENSION
DARK FACTORY RUNTIME OWNERSHIP = EXTERNAL / CANONICAL FOR FACTORY EXECUTION
SENSEMAKING OPERATING MODE = NORMAL_USE_VALIDATION
```

This clarification does not reopen Level 3, alter the frozen RC3 release scope,
or grant any protected transition.

## 6. Reopen trigger

Reassess the operator-front-door candidate when at least one of these becomes
true:

1. the owner explicitly asks ChatGPT to operate Dark Factory repeatedly through
   a stable exposed interface;
2. normal use shows repeated operator mistakes that a compact Skill contract
   would prevent;
3. Dark Factory exposes a stable connector/CLI contract whose correct use is
   non-obvious enough to warrant reusable instructions.

At that point, use the ordinary Skill-creation discipline and preserve the
boundary in this document.

## 7. Related sources

Sensemaking:

- `skills/strategic-sensemaking-loop/SKILL.md`
- `skills/strategic-sensemaking-loop/references/autonomous-terminal-mission-v1.md`
- `docs/autonomous-terminal-mission-continuation-v1-handoff.md`
- `docs/strategic-candidate-directions.md`
- `docs/product-strategy.md`

Dark Factory:

- `docs/adr/0001-canonical-successor-product.md`
- `docs/strategy/2026-09-22-semantic-control-layer-integration-program.md`
- `docs/audits/2026-09-22-sensemaking-runtime-ownership-closeout.md`
- `docs/architecture/delegated-autonomy-operating-model.md`
- `docs/qualification/2026-09-26-outer-loop-e2e-006.md`
