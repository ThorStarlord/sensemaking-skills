# Autonomous Task v2 — Pilot Dispatch Block Record

Status: OPERATIONAL RECORD. Produced by the **E3 Autonomous Task v2
pilot-execution** responsibility. Records the outcome of attempting to
dispatch the nine frozen pilot cells `(T1/T2/T3) × (R0/R1/R2)` in the frozen
order on this execution harness, and the reason the pilot was not
evidentiarily run.

This record corrects and supersedes the prior draft
(`AUTONOMOUS-TASK-V2-PILOT-DISPATCH-RESULT.md`) and is durably published. All
frozen experimental artifacts are preserved unchanged.

## Operational accounting

```
pilot_dispatch_attempts    = 1
attempted cell             = T3 × R2
valid evidentiary cells    = 0
completed / scored cells   = 0
cells 2-9 dispatched       = NO
manual repair count        = 0
PILOT_HARNESS_READY        = NO
PILOT_EVIDENTIARY_VERDICT  = NOT_REACHED
session disposition        = PILOT_NEEDS_REPAIR
```

`PILOT_NEEDS_REPAIR` here is a **pre-evidentiary harness disposition**, NOT
an evidentiary pilot verdict and NOT a product (`a7b957d`) outcome. Because
zero valid evidentiary cells ran, no pilot verdict under the experiment's
evidence standard was reached. The disposition records that the execution
harness must be repaired/qualified before any cell can yield evidentiary
output.

## 1. Immutable identities (all confirmed unchanged)

| Input | Value |
|---|---|
| product-under-test SHA | `a7b957d738f5e1c42b6dd06824c3e6029d816bcd` (PR #236 merge; not current main) |
| reviewed experiment SHA | `27cee78f2a5e1cb4f01db0b490e64832cbaaa58d` (reachable) |
| experiment merge SHA | `3169730d8e9b3f390fb57d73e5542a359c71c5d8` (PR #237, canonical history) |
| pilot manifest hash | `e640de278b1218ad20df7a5a0e20e5a63f5d63aeccdc2ccedc703f566597a8b6` |
| pilot seed | `0ab5cab61c1703f51f583d2ca527c9c3` |
| frozen 9-cell order | T3×R2, T3×R1, T1×R2, T3×R0, T1×R0, T2×R2, T2×R0, T2×R1, T1×R1 |

All of the above were verified against live repository state (Phase 0) and
matched exactly. No frozen byte or value differs.

## 2. Canonical preflight HARD GATE (PASS)

`experiments/evaluation-design-e3-autonomous-task-v2/AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`
was invoked byte-for-byte on a bash-capable harness (WSL Ubuntu) against a
fresh standalone clone at `a7b957d` with a network-style
(`https://github.com/...`) origin, in full DISPATCH mode (run-state-dir,
task-bundle, oracle-self-test supplied):

```
PASS=17  FAIL=0  UNVERIFIABLE=0   (exit 0)
```

The single `ENV_LIMIT` disclosure line (`ambient-scope-runtime-enforcement`)
is designed to be permanently non-counting (it discloses that runtime
filesystem sandboxing cannot be enforced/verified by the gate; it is not a
failure). Full raw output is preserved under `evidence/` (see section 5).

**Important scope note:** the preflight gate certifies the frozen
*instrument* state. It does not certify that the *execution harness* can
instantiate the instrument (that is the separate `HARNESS_READY` gate, which
is NOT met; see section 3).

## 3. Harness disposition (PILOT_NEEDS_REPAIR) — evidence

The `HARNESS_READY` gate (`docs/experimental-phase-gates.md`; Process-Learnings
§1, §7; `AUTONOMOUS-TASK-V2-PILOT-HARNESS-READINESS.md`) is separate from the
instrument preflight and is NOT met. This was established by non-evidentiary
calibration (never a real cell):

1. **Scoped writer sub-agent (`tool:task` with `write_paths`)** — the only
   configuration that can scoped-write an isolated clone:
   - file reads/writes within `write_paths`: **WORK** (verified).
   - **cannot execute bash/python/git**: `bash` is denied for every target.
     Exact error: `use_capability target "bash" is not proven read-only;
     explicit write_paths sub-agents cannot execute unscoped MCP writers`.
     Root cause (host `docs/SPEC.md` §3.12): on Windows there is no OS Bash
     sandbox to rebind write roots, so `bash` is removed from writer
     sub-agents; the proxy refuses every not-proven-read-only target before
     any command runs. Every T1/T2/T3 task requires running commands both to
     complete and to verify, so a writer sub-agent cannot execute any cell.

2. **Whole-workspace sub-agent (no `write_paths`)** — can execute (bash:
   python/git confirmed) and write files, but it claims/writes the whole
   workspace and retains **read access to the entire workspace**, which on
   this host is the live `main` checkout containing the hidden oracles and
   evaluator bundles under
   `experiments/evaluation-design-e3-autonomous-task-v2/construction/pilot/`.
   A tested agent with oracle read access **cannot enforce oracle isolation**,
   which destroys the measurement the pilot exists to make.

3. **Controller execution** is contaminated: the only other execution-capable
   agent is this controller, which has evaluator/oracle context (it read the
   frozen oracles/regimes to build the preflight self-test and to adjudicate).
   Running the cells as the controller would give "the tested agent" prior
   knowledge of all oracles and other cells — a cross-cell and oracle-isolation
   violation.

**Conclusion:** no execution-harness configuration on this host yields a
fresh, oracle-blind tested agent that can both run commands and edit an
isolated clone at `a7b957d`. This reproduces the repo's prior recorded
determination (`PILOT-HARNESS-READINESS = NO`) on the current harness. Per the
frozen execution responsibility's STOP-and-preserve rule, no frozen cell was
dispatched beyond the single attempted cell below; nothing was repaired
mid-matrix.

## 4. Dispatch attempt (the single tried cell)

The only dispatch attempt was **T3 × R2** (cell 1 of the frozen order). A
fresh isolated clone was created at exact `a7b957d`, and a scoped writer
sub-agent was given the T3 task contract and the R2 (escalation) regime.
That attempt **failed as a harness implementation defect**, before any
evidentiary work:

- The scoped writer sub-agent could not execute `bash`/python/git at all
  (section 3.1), so it could not run the orchestrator, make the fix, or
  verify — it returned a blocked status with a complete static diagnosis of
  the underlying `--json` bug but no executed run and no repo edit.
- Separately, the dispatch clone used was a **raw `a7b957d` checkout**. The
  frozen `T3-PILOT-TASK.md` specifies a **three-part pre-dispatch initial-state
  patch** ("Initial-state setup", applied before dispatch, not part of the
  agent's work) that the dispatch harness is required to apply and commit
  before the agent starts:
  1. register `t3-pilot-recovery-workflow` in
     `skills/workflow-planner/references/workflow-registry.yaml`;
  2. repair `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`
     to be a valid brief artifact;
  3. repair `examples/unknowns-mapper/unknowns_map-fixture.md` to match
     current machine-readable conventions.
  That frozen harness setup was **omitted** in the attempted dispatch, so the
  clone did not have the workflow registered or the fixtures repaired before
  the agent started.

This is a **harness implementation defect**, not a T3 instrument-design
defect: the frozen T3 task (and its `T3-PILOT-ORACLE.md`) already specify the
initial-state substrate; the execution setup failed to apply it. Correcting
this is part of the smallest repair in section 6.

## 5. Durable evidence

Raw receipts for the preflight result and the calibration/probe findings are
copied under:

```
experiments/evaluation-design-e3-autonomous-task-v2/construction/evidence/pilot-dispatch-block/
```

so this record does not depend on the ephemeral `~/e3-pilot-dispatch/...`
paths used during the session. Files:
- `preflight-raw-output.txt` — full raw `PASS=17 FAIL=0 UNVERIFIABLE=0` gate report.
- `calibration-writer-subagent-bash-denied.txt` — scoped writer sub-agent:
  writes OK, bash denied (exact error).
- `calibration-whole-workspace-subagent-exec-write.txt` — whole-workspace
  sub-agent: bash/python/git execute + write OK, oracle isolation not enforceable.
- `dispatch-attempt-T3xR2-subagent-blocked.txt` — single T3×R2 attempt: blocked
  (no command executed, no edit).

Manual-repair count: **0**.

## 6. Smallest repair (do NOT perform in this session)

1. Provide a bash-capable, oracle-isolated execution harness for tested-agent
   cells: a fresh agent that can both run commands and edit an isolated clone
   at `a7b957d` with no read access to `construction/pilot/*` (oracle
   isolation enforceable).
2. Apply the frozen T3 `Initial-state setup` patch (three parts, specified in
   `T3-PILOT-TASK.md`) to each T3 dispatch clone and commit it before the
   agent starts.
3. Re-run the non-evidentiary calibration to green `HARNESS_READY`, then
   re-dispatch the nine cells in the frozen order.

No effort was spent this session attempting to repair the harness or to
manufacture an evidentiary outcome.
