# Path 3 — Frozen Episode Set

**Status:** frozen episode-selection artifact / no disposition  
**Authority:** research only; not an ADR, product contract, runtime specification, Skill, schema, routing rule, or machinery proposal  
**Tracker:** Issue #210  
**Protocol:** `docs/research/decision-versus-orchestration.md`  
**Freeze baseline:** `main@be2c836105eb5167ee6b58983e96a534958a667a`  
**Episode count:** 8

## 1. Purpose of this artifact

This file freezes the repository-grounded episode set for the Path 3 decision-versus-orchestration study **before episode analysis or synthesis**.

Selection here means only that durable repository evidence is sufficient to make the episode useful for later boundary analysis. It does **not** pre-judge whether an episode ultimately supports `BOUNDARY_COHERENT`, `BOUNDARY_LIMITED`, or `BOUNDARY_INCOHERENT`.

The frozen set intentionally covers:

- a historical unsafe routing shape;
- responsibility redirection after new evidence;
- legitimate deterministic execution coordination;
- fail-closed execution at an authority boundary;
- exact-head validation followed by separate research/integration judgment;
- a stop-investigating / `act_now` decision control;
- a current registered bounded workflow/subflow;
- a concrete generic-execution-continuity pressure involving scheduler/host-local state.

Two episodes (P3-E03 and P3-E05) use different transitions from the same EXP-0005 campaign. They are retained because they test different ownership boundaries, but they must **not** be treated as independent empirical replications in the synthesis.

## 2. Freeze rule

Later analysis must use these eight episode identities as frozen here. Do not substitute a more favorable episode after seeing the emerging result.

If an exact source turns out to be factually unusable, record that as an episode limitation. Replacing an episode requires a separately reviewed amendment to this freeze before synthesis continues.

No episode record, failure-mode verdict, cross-episode conclusion, or bounded disposition is written in this artifact.

## 3. Frozen episodes

### P3-E01 — superseded ADR 0018 deterministic fog routing

**Coverage role:** historical unsafe-routing / F1-oriented control candidate.  
**Primary durable source:** `docs/adr/0018-workflow-routing-policy.md` on freeze baseline.  
**Blob:** `a6ff0bb294875c38778a8114bb0dcd166bd2aca5`.

**Eligibility rationale:** the preserved historical proposal explicitly made routing a deterministic function of `primary_fog_type`, while the superseding disposition states that later agent-native architecture moved responsibility selection to the active coding agent and retained deterministic subflows only after responsibility selection. This gives a concrete before/after design surface for asking whether orchestration was selecting engineering work too early.

**Later analysis must inspect:** what responsibility the routing table selected, what evidence/uncertainty should have governed that selection, and the counterfactual difference between diagnostic metadata informing a decision versus granting routing authority.

### P3-E02 — PR #164 stale-vs-live responsibility redirection

**Coverage role:** responsibility-redirection case.  
**Primary durable sources:**

- PR #164, `PROTOTYPE (not for merge): repo-sensemaker vNext exploratory spike`;
- `docs/research/uncertainty-selection-pr164-falsification.md` on freeze baseline.

**PR #164 head:** `b51822e7da941cf5a5d42d31017d6c9e186c36e4`; closed, unmerged.  
**Research-note blob:** `102e03a74a98c9cc84f8418aa700fc4f81ab35b2`.

**Eligibility rationale:** the provisional path was to refresh/rebase the old prototype and run another experiment, but a liveness check established that later canonical evidence had already adjudicated the material product questions. The selected responsibility changed from further prototype execution to inspecting current canonical decision state and then stopping work on the stale surface.

**Later analysis must inspect:** whether a predetermined execution path would have continued stale work, and which semantic transition belongs to evidence-grounded decision rather than orchestration.

### P3-E03 — EXP-0005 durable attempt lifecycle

**Coverage role:** positive deterministic-orchestration control.  
**Primary durable source:** `experiments/results/EXP-0005-stage1-auteur-github-connector-pilot/report.md` on freeze baseline.  
**Blob:** `93bb74fa17d46a2566932342b3645b5663ba2620`.

**Frozen campaign identity:** `EXP-0005-stage1-auteur-github-connector-pilot`.

**Relevant preserved transition shape:**

`RESERVED -> INVOKED -> OUTPUT_CAPTURED -> exact-head validation -> terminal state`

The report records all three serialized attempts, their state commits, exact output heads, exact validator runs, terminal states, concurrency one, no hidden retry/repair, and no automatic merge.

**Eligibility rationale:** once the campaign responsibility, target, authorization envelope, and attempt budget were already selected, several mechanics became deterministic and durably ordered. This provides a concrete test of execution-control transitions that may legitimately belong to orchestration without acquiring authority to choose a different engineering responsibility.

**Later analysis must inspect:** which transitions are purely execution control, where evidence returns to the active agent, and whether any deterministic failure/retry rule could silently cross into responsibility selection.

### P3-E04 — EXP-0004 approval-audit fail-closed boundary

**Coverage role:** authority-boundary / stop-execution case.  
**Primary durable sources:** Issue #197 and its final checkpoint comment.  
**Issue:** `https://github.com/ThorStarlord/sensemaking-skills/issues/197`.  
**Disposition comment:** `https://github.com/ThorStarlord/sensemaking-skills/issues/197#issuecomment-5331288456`.

**Relevant durable facts:** standalone human approval was received, but the frozen approval receipt required a concrete `session-id#message-id` reference unavailable on the active execution surface. Fabricating one would violate the fail-closed contract. No operative approval receipt, results branch, reservation, invocation, target read, retry, repair, or target mutation followed.

**Eligibility rationale:** this is a concrete case where execution machinery had technical paths available but did not gain authority to reinterpret authorization or select a replacement responsibility. It exposes the boundary among human authority, execution capability, and the decision to stop.

**Later analysis must inspect:** whether stopping is a decision-layer judgment, an orchestration policy outcome, or a sequential interaction between both; preserve ambiguity if the ownership cannot be reduced cleanly.

### P3-E05 — EXP-0005 exact-head validation, disposition, and integration separation

**Coverage role:** execution-evidence-to-decision handoff / publication-authority case.  
**Primary durable sources:**

- PR #203, `experiment: EXP-0005 supported results — do not merge`;
- `experiments/results/EXP-0005-stage1-auteur-github-connector-pilot/report.md`.

**Results head:** `c206f212011924deae045f03303fec40eb344ef6`.  
**Aggregate exact-head validator:** Validator #503 (`32177211469`).  
**Later owner-authorized merge:** `65c2be1b430e7bc8d1400ca99d80c6ff6256a051`.  
**Report blob:** `93bb74fa17d46a2566932342b3645b5663ba2620`.

**Eligibility rationale:** deterministic validation established facts about an exact results head, while the research disposition and later integration remained separate judgment/authority steps. The PR explicitly prohibited automatic merge and classified the evidence as exploratory.

**Later analysis must inspect:** where deterministic evidence production ends, where research interpretation begins, and why technical success does not itself grant publication/integration authority.

**Dependence note:** P3-E05 and P3-E03 share the EXP-0005 campaign and are separate transition episodes, not independent replications.

### P3-E06 — Path 01b `act_now` / stop-investigating control

**Coverage role:** decision-layer stopping control.  
**Primary durable source:** `docs/research/path-01b-synthetic-coherence-results.md`.  
**Blob:** `02db3672294fe09774f8e917b482bed9231105ec`.

**Frozen scenario:** `SCLU-006`.

**Relevant recorded decision:** `act now / investigate neither` because two genuine unresolved questions were non-gating for a cheap, reversible, behavior-preserving refactor.

**Eligibility rationale:** this synthetic control makes the decision layer's stopping function explicit: the agent may decide that no further evidence responsibility is warranted, after which execution may perform the already-selected bounded action. It is useful for checking that orchestration is not asked to choose among unresolved uncertainties.

**Later analysis must preserve limitation:** this is evaluator-aware synthetic research evidence, not a normal-use empirical engineering episode.

### P3-E07 — registered `docs-contract-reconciliation` subflow

**Coverage role:** current positive bounded-orchestration control.  
**Primary durable source:** `skills/workflow-planner/references/workflow-registry.yaml` on freeze baseline.  
**Blob:** `31aa4550bed57e13a4fbae66b6528c512ca056a5`.  
**Workflow id:** `docs-contract-reconciliation`.

**Frozen mechanically declared sequence:**

1. `repo-sensemaker` -> `repository_sensemaking_brief`;
2. `sensemaking-docs-reconciler` -> `docs_contract_reconciliation_report`;
3. `repair-verifier` -> `repair_verification_report`;
4. `handoff` -> `session_summary`.

The workflow purpose is specifically to resolve drift between documentation, registries, artifact contracts, templates, and validator rules; each step has declared artifacts and review gates.

**Eligibility rationale:** this is a concrete registered sequence that can be analyzed as a bounded subgraph once the docs/contract-reconciliation responsibility has been selected. It provides a present-day positive control for distinguishing stable sequencing from product-level responsibility selection.

**Later analysis must inspect:** whether any step inside the subflow actually changes the engineering responsibility rather than coordinating/validating the selected one; if so, preserve that as a limitation instead of assuming the registry label proves correct ownership.

### P3-E08 — EXP-0002 executor-host recovery / generic execution-continuity pressure

**Coverage role:** F2-oriented generic-runtime/control-plane pressure.  
**Primary durable sources:** Issue #187 and its reclassification comment.  
**Issue:** `https://github.com/ThorStarlord/sensemaking-skills/issues/187`.  
**Reclassification comment:** `https://github.com/ThorStarlord/sensemaking-skills/issues/187#issuecomment-5327362061`.

**Concrete execution-continuity mechanisms named by the issue:** Windows Task Scheduler `LastRunTime` / `LastTaskResult`, frozen execution logs, machine-local campaign root, `ledger.jsonl`, attempt directories, reservation/output/result files, and campaign summary state.

**Eligibility rationale:** the episode makes generic scheduling, persistence, host-local process history, and recovery semantics concrete rather than hypothetical. GitHub could not distinguish whether the scheduled executor never launched or launched and failed before publishing machine-local state; the workspace therefore preserved the ambiguity as an external-evidence limitation rather than fabricating a conclusion or blindly rerunning.

**Later analysis must inspect:** whether correctness of the Sensemaking decision layer actually requires owning this scheduler/worker/persistence machinery, or whether these are execution-infrastructure concerns whose evidence merely constrains later decisions. This episode is selected specifically to stress F2 without presupposing the answer.

## 4. Coverage matrix

| Episode | Intended coverage role before analysis |
|---|---|
| P3-E01 | historical unsafe routing / F1-oriented control |
| P3-E02 | responsibility redirection after new evidence |
| P3-E03 | legitimate deterministic campaign coordination |
| P3-E04 | authority-boundary fail-closed execution |
| P3-E05 | exact-head validation -> interpretation/integration separation |
| P3-E06 | decision-layer stopping / `act_now` |
| P3-E07 | current registered bounded subflow |
| P3-E08 | generic scheduler/persistence pressure / F2-oriented control |

These roles are sampling/coverage labels only. They are **not** episode verdicts.

## 5. Explicit exclusions and non-goals

This freeze does not:

- conclude that ADR 0018 was the only or dominant F1 failure;
- claim PR #164 proves all stale-work redirection belongs to decision;
- treat EXP-0005's two included transition episodes as independent replications;
- upgrade Path 01b synthetic evidence into real-world evidence;
- claim the current workflow registry is architecturally correct merely because it is canonical;
- claim Issue #187 proves Sensemaking should or should not own scheduler/persistence infrastructure;
- authorize automatic responsibility routing;
- revive ADR 0018;
- create a decision/orchestration schema or state machine;
- change Workflow-v0, workflow registry behavior, retry/fallback semantics, or runtime code;
- create a scheduler, queue, worker manager, persistence service, or DAG runtime;
- add a new Skill;
- claim any Path 3 bounded disposition.

## 6. Next step after integration

After this freeze is integrated on canonical `main`, record one episode analysis for each P3-E01 through P3-E08 using the canonical Path 3 template:

```text
Episode:
Repository evidence:
Contemplated decision:
Responsibility selected / under consideration:
Decision-changing evidence or uncertainty:
Authority boundary:
Orchestration mechanism:
Decision owner:
Orchestration owner:
Why the behavior belongs on that side:
Counterfactual if orchestration owned the decision:
Counterfactual if decision owned the orchestration:
Ambiguity / caveat:
Failure-mode signal: none | F1 | F2 | mixed
```

Only after all eight records exist should cross-episode comparison and the bounded synthesis begin.
