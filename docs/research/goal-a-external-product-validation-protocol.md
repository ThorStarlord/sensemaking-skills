# Goal A — External Product Validation Protocol (Canonical)

**Protocol status:** APPROVED (v1.0 FINAL) — owner-approved protocol-design review
**OSA (product-validation) status:**
```
PROTOCOL_STATUS          = APPROVED  (Goal A — External Product Validation Protocol v1.0 FINAL)
Goal A                   = ACTIVE
A1                       = ACTIVE
A2                       = DEFERRED / UNAUTHORIZED
Goal B / E3              = FROZEN / DEFERRED
Goal A episodes authorized = NO
repository mutation authorized = NO
```
**Document status:** CANONICAL — this file is the single source of truth for the
approved Goal A protocol. Do not redesign or re-litigate the protocol; make
bounded revisions only through a fresh owner-approved review.

This file lives under `docs/research/` by design: it is the current
product-validation strategy for the research/campaigning work of this
repository, **separate** from the frozen E3 experiment tree
(`experiments/evaluation-design-e3-autonomous-task-v2/`).

---

## 1. Purpose

Goal A is the current product-validation responsibility for Sensemaking
Skills. It replaces the historical E3 research-grade experiment as the active
external product-validation strategy. It validates the ratified current
product scope — a human-reviewed, evidence-grounded
`repository_sensemaking_brief` — against structurally different external
repositories, through constructed external product-validation episodes.

Goal A is **not** an experiment-regime campaign (it does not inherit E3
telemetry, cost, randomization, or harness requirements). Nor is it a
continuation of E4 (E4 / Issue #83 is historical and grants no Goal A
authorization).

## 2. Scope and boundaries

### Ratified current product scope

The product scope that Goal A validates is exactly the accepted, narrowed
boundary recorded in ADR 0014:

- a pre-implementation intelligence / workflow-orchestration assistant;
- produces a validated, **human-reviewed** `repository_sensemaking_brief`;
- the settled core is brief production;
- routing / downstream orchestration remains **not yet ratified as in-scope**.

Keep distinct:

- **ratified current product scope** = validated, human-reviewed
  `repository_sensemaking_brief`;
- **broader orchestration/control architecture** = informs research and
  architecture, but is **≠ silently ratified external product scope**.

### Out of scope for Goal A

Goal A does not authorize: repository or task selection, a real Goal A task
episode, a fresh producer spawn, an evidence audit, usage-rubric scoring, a
human usefulness review, or any A1 episode. Those belong to later, separate
responsibilities.

### Goal B / E3 boundary

Goal B / research-grade E3 is **FROZEN / DEFERRED** and is **not** a gate on
Goal A. E3 remains frozen; no E3 task/oracle/regime/manifest/seed/order/lock
artifacts may be modified, no harness qualification resumed, no E3 pilot cell
dispatched, no E3 product-under-test SHA changed, no E3 telemetry contract
weakened, and no E3 harness implemented. Do not mix the historical
`HARNESS_INCONCLUSIVE` session with Goal A work. The historical E3
qualification-result finalization is off the Goal A critical path.

### D8 historical evidence

D8 (`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`) is **historical / inherited
evidence guidance**, not current binding readiness authority. Goal A's own
evaluation axes govern episode admissibility and verdicts. Goal A does not
inherit D7/D8 readiness bars as binding gates; it does inherit the product
boundary from ADR 0014.

## 3. Overall status

```
Goal A = ACTIVE
A1     = ACTIVE            (absolute product utility)
A2     = DEFERRED/UNAUTHORIZED  (incremental value)
Goal B / E3 = FROZEN / DEFERRED
```

- **Goal A** — the current outcome goal for external product validation.
- **A1** — the primary active axis: absolute product utility (is the brief
  useful as a standalone human-reviewed product artifact).
- **A2** — incremental value (usefulness relative to some baseline) is
  **DEFERRED / UNAUTHORIZED**: not active, not measured this protocol.
- **Goal B / E3** — frozen experimental research-grade regime; not a gate.

## 4. Episode construction

Goal A episodes are **constructed external product-validation episodes**, not
normal-use episodes. They satisfy the following construction rules:

- **2 structurally different repositories** × **2 fresh runs** each.
- **independent evidence audit** is performed after runs.
- **actual human decision owner** may perform the usefulness review.
- **no target mutation** — elements in the target repository may not be
  modified by Goal A.
- **no manual artifact repair** — once a run's artifact is produced and
  mechanically adjudicated, it may not be manually repaired to pass.
- **four independent evaluation axes** drive episode admissibility and the
  verdict (see §5).

## 5. Evaluation axes and the usage rubric

Goal A evaluates each episode along **four independent axes**:

1. **episode admissibility** — is the episode even eligible as evidence
   (constructed external episode, fresh runs, no mutation, no manual repair).
2. **mechanical validation** — deterministic validator PASS of the produced
   artifact (structural/contract validity).
3. **grounding** — is the artifact's evidence grounding `STRONG` or `MIXED`.
4. **repeatability** — do the two fresh runs agree (`CONSISTENT` or
   `COMPATIBLE_VARIANCE`).
5. **human usefulness** — the semantic usefulness review performed by the
   actual human decision owner (`USEFUL` or `PARTIALLY_USEFUL`).

The existing 0–21 usage-research rubric
(`docs/research/usage-research-rubric.md`) is **diagnostic only** for Goal A.
It may inform the human usefulness review but is not a binding scoring
mechanism and does not make an episode admissible or produce a verdict by
itself.

**`MISLEADING` is confined to human usefulness.** A `MISLEADING` verdict means
the human usefulness review judged the artifact positively misleading to the
human owner; it does **not** extend to mechanical/structural or grounding
outcomes, which have their own axis outcomes as described above.

## 6. A1_POSITIVE conditions

An episode earns `A1_POSITIVE` only when **all** of the following hold:

```
episode_admissibility      = EVIDENTIARY_VALID
mechanical_validation      = VALID
target_mutated             = false
manual_artifact_repair     = false
grounding                  = STRONG or MIXED
repeatability              = CONSISTENT or COMPATIBLE_VARIANCE
at least one run           = USEFUL
other run                  = USEFUL or PARTIALLY_USEFUL
```

Notes:

- `target_mutated = false` and `manual_artifact_repair = false` are **negative
  evidence** gates: they are confirmed by the absence of target mutation and
  absence of manual artifact repair over the episode lifecycle, not by a
  positive measurement. `target_mutated = true` or
  `manual_artifact_repair = true` is **negative evidence** against the episode
  as an A1_POSITIVE indicator.
- `grounding` must be `STRONG or MIXED`. `WEAK` does not satisfy A1_POSITIVE.
- No automatic repair-and-rerun is permitted: a run is not automatically
  repaired and re-executed to chase a positive outcome. A verdict may require
  a fresh run only under a separately authorized new episode; it is never an
  automatic recovery.
- The **usage rubric is diagnostic only** and cannot, by itself, flip an
  outcome to A1_POSITIVE.

## 7. What A1_POSITIVE means (interpretation discipline)

`A1_POSITIVE` for an episode means the constructed external product-validation
episode demonstrated that the produced brief was **absolutely useful** to a
human decision owner, as a standalone human-reviewed product artifact, on a
structurally different external repository, repeatably, without target
mutation or manual artifact repair.

It is **not** a claim about:
- incremental value (A2, deferred/unauthorized);
- broad orchestration/control architecture (separate research domain);
- automatic routing or downstream workflow readiness (not ratified, ADR 0014);
- generalization beyond the two validated repositories.

## 8. Protocol approval does not authorize execution

This protocol being APPROVED does **not** authorize any Goal A episode. All
episode execution requires a separately authorized responsibility (Goal A —
Repository/Task Selection, then a fresh responsibility for each run), each
with its own authority, in a fresh session. No repository or task has been
selected under this protocol, and no episode has been run.

## 9. Relationship to other repository evidence lanes

- **Issue #218** / `docs/research/normal-use-evidence-lane.md` — the
  **separate normal-use evidence lane**, distinct from Goal A. Normal-use
  episodes inform research; Goal A episodes are constructed product-validation
  episodes. They do not merge.
- **E4 / Issue #83** — historical; grants **no** Goal A authorization. Issue
  #83 is closed. E4 is not "resumed" by Goal A; Goal A is a **successor
  strategy**.
- **`docs/research/control-model-research-agenda.md`** — explicitly
  non-ratified research directions; informs research but is not ratified as
  product behavior and is not a Goal A gate.
- **`docs/experimental-phase-gates.md`** — reusable methodology for
  regime-comparison experiments (E3 lineage). Goal A is not an E3-style
  regime-comparison; these phase gates are non-normative for Goal A.

## 10. Ownership and review

- The **owner** approved this protocol v1.0 FINAL in the preceding review
  session (Decisions 0 and A–E).
- Future bounded revisions require a fresh owner-approved review in a fresh
  session; they are not silently editable from this file.
- Do not weaken, extend, or reinterpret the owner-approved rules above.

## 11. Next responsibility (not begun)

The next responsibility, in a **fresh session**, is:

```
Goal A — Repository/Task Selection
```

That session will select structurally different repositories and formulate a
real Goal A task, and then in turn hand off to fresh per-run episode
responsibilities. None of that is begun in this document.

## Status disposition (canonical close)

```
GOAL_A_PROTOCOL = CANONICAL
Goal A          = ACTIVE
A1              = ACTIVE
A2              = DEFERRED / UNAUTHORIZED
Goal B / E3     = FROZEN / DEFERRED
Goal A episodes executed = 0
```
