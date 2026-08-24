# Autonomous Task v2 — Re-Freeze Provenance (old -> new instrument)

## Purpose

This document is the audit trail for re-freezing the E3 Autonomous Task v2
instrument from the original construction freeze to current product main.
It records, explicitly and transparently:

- the old freeze and the new freeze;
- why the change is required;
- what comparability is lost;
- what validity is gained;
- the re-validation classification of every pilot task/oracle against the new
  freeze;
- every derived value (hash, seed, ranking, bundle, lock record) that the
  re-freeze changed, and the old->new mapping.

It is written during the **E3 pilot preparation** responsibility (Phases 1-4)
which produces `PILOT_READY`. It does **not** dispatch a pilot, does **not**
execute a main-study cell, and does **not** authorize main-study execution.

## 1. Re-freeze decision

| Field | Old freeze | New freeze |
|---|---|---|
| Revision | `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5` | `a7b957d738f5e1c42b6dd06824c3e6029d816bcd` |
| Product state | Pre-#229/#232/#230 campaign | Post-#229/#232/#230 (current `main`) |
| Campaign status | ADR 0025/0026 pending | ADR 0025 ACCEPTED, ADR 0026 ACCEPTED, PR #236 merged |

**Why the change is required.** The original E3 instrument was frozen against
`0ffb564b`, which predates the #229 -> #232 -> #230 internal-repair campaign
(workflow-planner four-fog SKILL semantics; two-stage plan lifecycle per ADR
0025; auto-invoke execution-authority fail-closed per ADR 0026). The purpose of
the E3 external/generalization pilot is to test the **current product**. Testing
an instrument frozen on a superseded product revision would not be a
generalization test of the current product; it would re-test the internal
repair era. Per the owner's prescribed default (current `main` as candidate new
freeze unless concrete experimental-validity evidence argues otherwise), and
because no such counter-evidence surfaced, the new freeze is `a7b957d`.

**What compatibility/comparability is lost.** T1's substrate (`workflow-registry.yaml`
duplication) and T3's runtime (`validate-artifact.py` missing `--json`, resume
mechanics) are version-sensitive. T1's observable divergence is now **larger**
at the new freeze (defaults=20 vs skills=23, versus defaults=20 vs skills=22 at
old freeze) — the task is no longer byte-identical to its old-freeze instance.
T3's runtime was rewritten ~570 lines by #232/#230, so the old-freeze empirical
proof no longer directly carries; the seven-link chain had to be re-run at the
new freeze. Any historical run on the old freeze would not be directly comparable
to a new-freeze run in terms of the exact intermediate repository state.

**What validity is gained.** The re-frozen instrument tests the product as it
exists at `a7b957d`, which is the artifact a fresh external agent would actually
encounter upon cloning the current repository. This restores the pilot's stated
purpose: a warranted next action on a fresh, ambiguous engineering task against
the current product, without manual repair.

## 2. Task/oracle re-validation against the new freeze

For every pilot task, each Phase-2 gate was checked against `a7b957d`:

1. substrate still exists;
2. task remains ambiguous in the intended way;
3. hidden oracle remains factually valid;
4. expected answer is not trivial or impossible;
5. regime distinction still measures the intended independent variable;
6. no #229/#232/#230 repair leaked the oracle into task-visible material.

| Pilot | Classification | Evidence at `a7b957d` |
|---|---|---|
| T1 | `VALID_UNCHANGED` (substrate drift still holds; no byte change to task) | `defaults/workflow-registry.yaml` = 20 workflows, strict subset of `skills/` copy's 23 (3 extra). `registry.py` `WorkflowRegistry` still loads `defaults/` for bare targets; `workflow-planner.py` still hardcodes `skills/` and never reads `defaults/`. Oracle is base-independent; defaults-count invariant `21` still correct. #229/#230/#232 did not leak task payload. |
| T2 | `VALID_WITH_METADATA_UPDATE` (oracle `git diff` base SHA re-pointed; content otherwise valid) | `_WORKFLOW_ID_FIELDS` tuple byte-identical old->new. `FROZEN_REQUIRED`/`FROZEN_RECOMMENDED` field sets of `workflow_orchestration_plan` unchanged at `a7b957d` (#232 added only an ADR-0025 note line; block shifted ~452->~459, no block-header change). `target_workflow_id` absent from contracts at new freeze (clean input state). Check 4 base updated `0ffb564b`->`a7b957d`. |
| T3 | `VALID` (re-frozen after empirical seven-link re-run at `a7b957d`) | Real bug intact: `validate-artifact.py` still has no `--json`; `validate-and-report.py` still invokes generic fallback with `--json`, producing `execution_error`/invalid-JSON. Fixture files still stale (brief uses invalid `specification_fog`, missing `artifact_id`/`evidence`/`immutable`/`weakness_type`). Resume machinery (`_find_resume_state`, `resume_skip`, `completed_steps`, `_resumable_terminal_statuses`) present. Seven-link chain re-proven end-to-end (see §4). |

Every gateway was checked mechanically. Gateway 6 (no oracle leakage) was checked
by searching all repaired components (`workflow-runtime.py`, `workflow-planner.py`,
`validate-{,and-report,artifact,brief,plan}.py`, `registry.py`, `runner.py`,
`SKILL.md`) for the pilot's task payload strings (`duplicate-detection-workflow`,
`target_workflow_id`, `t3-pilot-recovery-workflow`): none present.

## 3. What previously untracked -> what became durable

The E3 design package (17 files under `experiments/evaluation-design-e3-autonomous-task-v2/`)
was **untracked** in the working tree. The full constructed instrument (pilot
tasks/oracles, 36 main-study candidates across two tranches, rankings, dispatch
seeds, bundle separation, preflight result, lock record, construction scripts)
lived on the local, un-pushed, un-merged historical branch
`experiment/autonomous-task-v2-pilot`, constructed against the **old** freeze and
never merged to `main`.

This preparation responsibility promotes both to a **fresh branch off
`a7b957d`**: `experiment/e3-autonomous-task-v2-pilot-prep`. The historical
construction branch is preserved unchanged as provenance (it is *not* the
authoritative re-frozen instrument; see §6).

## 4. T3 empirical re-run at the new freeze (evidence summary)

A disposable scratch clone was created at exact `a7b957d`. The T3 initial-state
patch was applied and committed (brief + unknowns fixtures repaired to be valid
`repository_sensemaking_brief`/`unknowns_map`; `t3-pilot-recovery-workflow`
registered). Then the disposable seven-link recovery chain was run:

1. First `workflow-runtime.py ... --workflow t3-pilot-recovery-workflow --resume-absent`
   invocation: **step 1 passed**, **step 2 failed** with
   `unknowns_map.validator.execution_error: Validator returned invalid JSON` —
   the real missing-`--json` bug. Ledger (`05-orchestration-run`) recorded
   step 1 `validated`, step 2 `failed` exit 1, `run_completed failed` exit 2.
2. `--json` support added to `validate-artifact.py` (real validator; a
   deliberately invalid artifact still reports `valid:false` exit 1). Committed.
3. `--resume --log-dir artifacts/01-orchestration-run`: `Resuming: skipping steps
   [1], starting from step 2`. New ledger (`06`) recorded **zero step-1 events**,
   step 2 `validation_completed passed`, `run_completed completed` exit 0. Step-1
   artifact hash in ledger `05` == current brief fixture hash (no reset laundering).
4. Idempotent replay: a second `--resume` from a clean committed tree found `2
   completed`, skipped steps [1,2], and produced a new ledger (`07`) with only
   `run_started`/`run_completed` bookkeeping — **zero step/artifact/validation
   events** (link 7).

All seven links of the T3 pilot chain were re-confirmed at `a7b957d`.

## 5. Regenerated derived values for the new freeze

The following pilot-bound values changed because task/oracle bytes changed under
re-freeze. (T1 task/oracle content is unchanged; only its provenance note was
added. T2 and T3 oracle/task text changed, so their hashes and the manifest
hash change.)

- **T2 oracle**: `git diff` base SHA `0ffb564b...` -> `a7b957d...`; re-freeze
  provenance note added. `oracle_sha256` regenerated.
- **T2 task**: `frozen SHA` reference updated to `a7b957d`. `task_sha256`
  regenerated.
- **T3 task**: `frozen SHA` reference updated to `a7b957d`. `task_sha256`
  regenerated.
- **T1 task**: `frozen SHA` reference updated to `a7b957d`. `task_sha256`
  regenerated. **T3 oracle**: re-freeze provenance note added; `oracle_sha256`
  regenerated. **T1 oracle**: re-freeze provenance note added; `oracle_sha256`
  regenerated.
- **Pilot manifest**: re-hashed because T1/T2/T3 task+oracle hashes changed.
  `pilot_manifest_sha256` regenerated (see lock record).
- **Tranche-1 / Tranche-2 candidate pools, salts, rankings, samples, seeds,
  bundles**: carried over **unchanged** as historical construction frozen at the
  old freeze. Their re-validation/re-ranking against `a7b957d` is a
  **prerequisite for the separate main-study responsibility** and is explicitly
  out of scope for the pilot-only `PILOT_READY` gate. They are NOT asserted
  valid at the new freeze here.

Precisely what changed and what was retained unchanged (matching the lock record):

- **Task/oracle SHA-256**: regenerated (T1/T2/T3 task + oracle hashes all changed
  because freeze-base references / provenance notes changed).
- **Pilot manifest hash**: regenerated (`pilot_manifest_sha256` recomputed).
- **Evaluator-only bundles**: regenerated to match the updated oracle files.
  **Agent-visible bundles**: byte-identical to the old freeze (the visible task
  contract / non-goal sections carried no SHA reference and did not change).
- **Regime hashes**: **unchanged** (regimes are substrate-independent prompts;
  hashes verified identical to the old freeze).
- **`seed_pilot_dispatch`**: **RETAINED unchanged.** Task/regime identities
  (T1/T2/T3 × R0/R1/R2) were unchanged by the re-freeze, and the seed is
  content-independent cryptographic random bytes (it only orders the 9
  (task, regime) pairs), so it was not regenerated.
- **Deterministic pilot order**: therefore **unchanged** (the 9-cell order
  derived from the retained seed is identical to the old freeze).
- **Tranche-1/Tranche-2 candidate pools, salts, rankings, samples**: carried
  over **unchanged** as historical construction frozen at the old freeze; NOT
  re-ranked or asserted valid at the new freeze here. Their re-validation is a
  separate main-study responsibility.

The main-study pools are intentionally left at their old-freeze frozen state
(historical) until the main-study responsibility re-freezes them.

## 6. Historical vs new instrument provenance

- `experiment/autonomous-task-v2-pilot` (local, historical): the original E3
  construction, frozen at `0ffb564b`. Preserved unchanged as evidence of the
  prior construction state. Not the authoritative re-frozen instrument.
- `experiment/e3-autonomous-task-v2-pilot-prep` (this branch, off `a7b957d`):
  the re-frozen preparation package. Contains the full design package + carried
  construction + this re-freeze provenance + regenerated pilot values +
  preflight + lock record = the authoritative `PILOT_READY` handoff.

## 7. Status

Phase 1 (re-freeze decision): complete. Phase 2 (task/oracle revalidation):
complete. Phase 3 (durability): complete on this branch. Phase 4 (lock
reconstruction): see lock record. Phase 5 (preflight + `PILOT_READY`): lock
record.
