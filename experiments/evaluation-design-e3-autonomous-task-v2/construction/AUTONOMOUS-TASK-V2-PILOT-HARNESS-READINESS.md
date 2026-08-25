# Autonomous Task v2 — Pilot Harness Readiness Report

Status of this document: OPERATIONAL FINDING, not an adjudication of any pilot
run. Produced at the boundary between `PILOT LOCKED` (construction completed,
lock verified) and the 9-cell disposable pilot execution. This report does not
execute, adjudicate, or substitute for any pilot run. It identifies a
harness-readiness blocker and records the operational status honestly.

Related frozen artifacts (do not alter any of these):
`construction/AUTONOMOUS-TASK-V2-LOCK-RECORD.md`,
`construction/AUTONOMOUS-TASK-V2-PILOT-ADJUDICATION.md` (does not exist yet —
intentionally not produced), the three `construction/pilot/*-PILOT-TASK.md` /
`*-PILOT-ORACLE.md` pairs, `construction/pilot/PILOT-TASK-MANIFEST.md`,
`construction/tranche{1,2}/` content, `construction/AUTONOMOUS-TASK-V2-*.md`,
and the frozen design package in the sibling source repo.

## Operational status

```
INPUT_LOCK_STATUS    = PILOT_LOCKED
PILOT_DISPATCHED     = NO
PILOT_HARNESS_READY  = NO
```

- The experimental design is LOCKED and the lock verifies cleanly (Section 1).
- Nothing has been dispatched: zero of the nine frozen pilot cells
  (`T1/T2/T3 × R0/R1/R2`) have been run, exposed to an agent, or observed.
- The current execution harness cannot yet instantiate the frozen instrument
  faithfully, so `PILOT_INSTRUMENT_VALID` cannot honestly be established and
  no frozen pilot cell should be dispatched until the harness qualifies.

## 1. What verified from the lock / PILOT LOCKED

All mechanically checkable lock-record items were re-verified against
`construction/AUTONOMOUS-TASK-V2-LOCK-RECORD.md` during this session. Every
one matched. None was altered.

| Lock item | Status |
|---|---|
| Frozen repository SHA `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5` exists as a commit | PASS |
| 17 normative design-package artifact hashes (sibling source repo, raw UTF-8 bytes, sha256) | PASS (17/17) |
| R0/R1/R2 regime-file hashes | PASS |
| R1/R2 shared execution-discipline block hash `a19c6c2c…0cde4c` | PASS (`a19c6c2cdc5dbff9664031c68c1b3084baa6e057adbf53eb080c0231c10cde4c`) |
| Pilot manifest hash `d6988ce3…` (recomputed via `sha256_manifest`) | PASS |
| Tranche-1 manifest hash `bed02782…` and salt `d7b1cc…` | PASS |
| Tranche-2 manifest hash `f6a08e99…` and salt `01a9c4…` | PASS |
| Ranking derivation (`rank_key = sha256(manifest_hash‖salt‖candidate_id)`, ascending per cell) | PASS |
| Dispatch seeds `0ab5cab6…`, `c20edf22…`, `a4c5145d…` | PASS |
| Agent/evaluator bundle separation + leakage audit (0 findings) | PASS |
| Preflight result at Task 22: `PASS=17 FAIL=0 UNVERIFIABLE=0`, exit 0, `PREFLIGHT: CLEAN` | PASS |

Recorded: `INPUT_LOCK_STATUS = PILOT_LOCKED`.

This finding is a **harness-readiness failure**, not a failure of the locked
Autonomous Task v2 experimental design and not a failure of any task family
(T1/T2/T3). It mirrors the isolation audit's standing disclosure
(`MITIGATED, AUDITABLE, NOT TECHNICALLY CLOSED`) in the sense that what can be
mechanically checked is checked and clean; what this report adds is the
specific execution-path gap.

## 2. Telemetry fields unavailable through the current execution path

The current execution path for a cell would be an isolated sub-agent spawned
via the `task` capability over a fresh standalone clone. That boundary returns
only a final textual answer; it does not expose an instrumented model-API
layer, so the following frozen `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md` fields
**cannot be produced** as specified:

Per-model-call / session LLM telemetry:
```
model_calls[]                       (call_index, input_tokens,
                                     cached_input_tokens, output_tokens,
                                     model_id)
input_tokens_total                  input_tokens_task_bundle
input_tokens_regime_prompt          output_tokens_total
model_turns_count                   tool_calls_count
tool_calls_by_type                  (map: tool_name -> count)
operational_actual_cost_usd         monetary_cost_usd (alias)
dynamic_execution_input_tokens      dynamic_execution_output_tokens
dynamic_execution_resource_cost_usd (conditional)
```

Some operational counters that a shell-level wrapper could observe for the
agent's *subprocesses* (e.g. `subprocess_executions_count`,
`subprocess_runtime_seconds_total`, `failed_commands_count`, `retries_count`,
`wall_clock_seconds_total`) are partly capturable, but the LLM-call and
token/cost fields above are not, and several of the subprocess counters at the
agent's own tool-turn level (not the sub-process level) are also not exposed
by the sub-agent boundary.

## 3. Fields required for `PILOT_INSTRUMENT_VALID`

The frozen `AUTONOMOUS-TASK-V2-PILOT-PLAN.md` (in the sibling source repo)
defines `PILOT_INSTRUMENT_VALID` to require, among other conditions, that **"telemetry
fields populate as designed."** The frozen protocol (§7 and the telemetry
schema) additionally makes the following **required, non-optional** for every
run:

```
operational_actual_cost_usd          THE primary confirmatory dollar measure
dynamic_execution_input_tokens       required token diagnostics (co-equal,
dynamic_execution_output_tokens      never optional)
```

plus the per-call `model_calls[]` capture from the first model call on which
those aggregates depend. Because these fields cannot be populated through the
current sub-agent execution path, `PILOT_INSTRUMENT_VALID` **cannot be
honestly established** in this environment. This is the blocking condition.
Consistent with the frozen protocol's anti-theater stance (`VERIFICATION_THEATER`,
`SEARCH_THEATER`), the correct response is to qualify the harness rather than
to fabricate or weaken these measurements.

## 4. The exact capability an execution harness must expose

For each of the nine cells the harness must provide, from the very first model
call:

```
per model call:
  timestamp
  model identity
  input tokens
  cached-input tokens if exposed
  output tokens
  actual/billable cost if exposed
session:
  model-turn count
  tool-call trace / count by type
  failed calls
  retries
  subprocess/runtime information (count, seconds)
  wall clock
evaluator-readable pointer to the final isolated repository state
```

plus per-cell instantiation guarantees:
```
fresh agent session
fresh standalone repo clone at the frozen SHA
exact regime prompt (hash-verified)
exact agent-visible task bundle (hash-verified)
exact model/configuration
```

If the provider/API cannot expose one of the frozen required measurements,
that must become a **harness admissibility finding**, never a fabricated
estimate.

## 5. R2 human-responder requirements

R2 escalation, if a P2 agent spontaneously escalates, requires a responder
who is **oracle-blind**: given only the visible task contract, permitted
environment facts, and the agent's escalation request — never the hidden
oracle, the intended solution route, alternate candidates, or prior regime
outcomes. Required telemetry:

```
escalation_count
escalation_request_emitted_at        responder_started_at
responder_submitted_at               human_active_seconds
                                       (= responder_submitted_at
                                          - responder_started_at;
                                        latency form documented separately)
escalation_request_text (verbatim)   escalation_response_text (verbatim)
responder_blinded                    operational_recovery_seconds
approval_review_seconds              manual_repair_seconds
salvaged_after_manual_repair         research_evaluator_labor_seconds
```

The "no-human-responder" issue is solvable: a designated blinded responder can
fill this role as long as the harness enforces the oracle-blind information
boundary and timestamps presentation/start/submission. No escalation is to be
forced; if none occurs spontaneously in the R2 pilot cell, the channel is
validated separately via the non-evidentiary handshake/calibration exercise
(Section 6) — absence of escalation is a legitimate instrument result, not an
instrument defect.

## 6. What can be tested with a NON-EVIDENTIARY calibration run

A **non-evidentiary harness-calibration task** — deliberately **not** any of
the nine frozen T1/T2/T3 × R0/R1/R2 cells, and never eligible to enter the
evidence set — can exercise the full machinery end-to-end and prove readiness
without contaminating the pilot:

```
fresh clone -> fresh agent -> regime-like test prompt
  -> telemetry from first model call -> tools -> final repo state
  -> evaluator -> telemetry record -> teardown
```

Proving (and checking) the following constitutes `PILOT_HARNESS_READY`:
```
required telemetry populated
agent/evaluator separation holds
fresh state holds (no cross-run leakage)
no ambient leakage occurred
R2 transport calibration works (synthetic request/response round-trip,
                               outside the scored pilot task)
```

Only after that should the harness be declared `PILOT_HARNESS_READY` and the
nine frozen cells be unlocked.

## 7. Confirmation: zero frozen pilot cells dispatched

During this session only the following were performed, all read-only with
respect to the frozen instrument:

- verified the lock record and all Section-1 items (hashes recomputed, not
  relied on from memory);
- read the frozen pilot manifest, task/oracle bundles, dispatch seeds,
  telemetry schema, and preflight result;
- located the 17-file design package (regimes, protocol draft, telemetry
  schema, preflight gate) in the sibling source repo and verified each hash;
- produced this readiness report.

No frozen pilot cell (`T1/T2/T3 × R0/R1/R2`), no probe disguised as a pilot
cell, and no agent session was dispatched against any pilot task. Nothing in
the frozen set — task texts, oracle specifications, regime prompts, candidate
manifests, salts, rankings, dispatch seeds, or the lock record — was modified.
The telemetry requirements were not weakened to fit the current harness.

## Explicit non-goals of this report

- This is not `AUTONOMOUS-TASK-V2-PILOT-ADJUDICATION.md`; no pilot run occurred,
  so no adjudication exists yet.
- This introduces no new milestone authority; it records that the missing
  phase between `PILOT LOCKED` and the 9-cell pilot is **harness
  qualification** leading to a `PILOT_HARNESS_READY` gate.

## Terminal status

No pilot result is claimed. The next warranted step is to build and qualify an
instrumented execution harness (Section 4), demonstrate readiness with a
non-evidentiary calibration run (Section 6), and only then gate
`PILOT_HARNESS_READY` before dispatching the nine frozen cells.
