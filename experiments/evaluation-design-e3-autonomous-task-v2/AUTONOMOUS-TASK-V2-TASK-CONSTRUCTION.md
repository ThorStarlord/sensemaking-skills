# Autonomous Task v2 — Task Construction Rules

Status: DRAFT. Normative rules only. The six main-study task instances are
NOT constructed by this document — only the disposable pilot task *shapes*
(labeled UNFROZEN DESIGN CANDIDATES) are sketched, per
`AUTONOMOUS-TASK-V2-PILOT-PLAN.md`.

## General rules (all families)

1. **Route independence.** A task's success criteria must be checkable from
   end state alone. If a specific mechanism is genuinely required (e.g. "you
   must use the canonical source file, not a build artifact"), that
   requirement must be stated as part of the visible process contract, never
   left implicit for the hidden oracle to enforce as a surprise.
2. **No reference-solution leakage.** The task bundle must never contain the
   evaluator's intended solution path, the exact file the evaluator expects
   to be touched (beyond what the task naturally implies), or wording
   borrowed from the hidden oracle's implementation.
3. **Fresh instances only.** No task instance may reuse content, artifacts,
   or scenarios from prior Autonomous Task work (banked Semantic Tool
   Routing candidates, D/D' family, lifecycle candidates) per the standing
   instruction. This applies even though those artifacts are external to
   this repository — the rule is about instance novelty, not about where the
   prior work lives.
4. **No live external dependency.** No task may require network access,
   credentials, or a live external service. This repository's own
   "Dependency Philosophy: Local-First Design" (`CONTEXT.md`) makes this a
   natural fit, not an artificial constraint.
5. **Multiple valid implementations where the family calls for it (T2, T3).**
   A task must not be gameable by literal reference-diff matching; the oracle
   checks properties of the end state, not textual identity with one
   solution.
6. **Constructed, not discovered, complexity level.** A task's MEDIUM/HIGH
   label is assigned by the rubric below *before* any agent attempts it.
   Runtime is never used to justify or revise the label after the fact.

## Complexity rubric

Five structural factors, each scored 0-3 for a given task instance. MEDIUM =
5-8 total points; HIGH = 9+. (Scores below 5 are not admissible as either
main-study level — they indicate the task is under-specified as a
complexity-differentiated instance.)

| Factor | 0 | 1 | 2 | 3 |
|---|---|---|---|---|
| Repository surfaces touched or inspected | 1 | 2 | 3 | 4+ |
| Plausible-but-wrong routes/mechanisms present | 0 | 1 | 2 | 3+ |
| Hard invariants that must hold at completion | 0-1 | 2 | 3 | 4+ |
| Required execution stages (sequential dependencies) | 1 | 2 | 3 | 4+ |
| Independent validation conditions in the hidden oracle | 1 | 2 | 3 | 4+ |

Worked examples, grounded in this repository's actual surfaces (see
`AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §3 for the underlying facts):

- **T1 MEDIUM/HIGH-shaped examples (corrected in Hardening Pass 1 — the
  original Skill-tool-vs-CLI example below was dropped; see
  `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §1)**: the verified substrate is
  the dual-consumer `workflow-registry.yaml` divergence (`skills/
  workflow-planner/references/` read by local dogfood CLI scripts vs.
  `src/sensemaking_skills/defaults/` read by `WorkflowRegistry` as package
  defaults for an external target repo). A MEDIUM-shaped instance names one
  consumer explicitly and asks for a single workflow addition/edit visible
  to that consumer only (2 surfaces — the two registry copies — 1 wrong
  route, 2-3 invariants, 2 stages, 2 validation conditions: mid-range
  MEDIUM). A HIGH-shaped instance requires the edit to be visible to *one*
  named consumer while explicitly NOT changing the other consumer's
  behavior (adds an invariant — the other copy must remain semantically
  unaffected for its own consumer — and a validation condition, pushing
  toward HIGH). Both examples are grounded in content confirmed to exist,
  and to already differ, at the frozen SHA.
- **T2 MEDIUM-shaped example**: add one declared field to one existing
  artifact-contract block in `artifact-contracts.yaml`, preserving all other
  blocks, passing the contract-agreement check — 1 surface, 0 wrong routes,
  2-3 invariants (parseability, preservation, field-shape correctness), 2
  stages, 2 validation conditions: mid-range MEDIUM.
- **T2 HIGH-shaped example**: same but spanning two related declarations
  that must stay mutually consistent (e.g. a producer's declared output
  field and a consumer's declared required field), raising invariants and
  validation conditions into HIGH range.
- **T3 MEDIUM/HIGH-shaped examples (interrupt mechanism corrected in Lock-
  Readiness Response 3 — the gate-pause example below is withdrawn; see
  `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §1)**: the verified
  mechanism is a step's own validator failing on first attempt for a
  realistic, constructible reason, which `workflow-runtime.py`'s
  `--resume` genuinely retries (confirmed: `FAILED` status is excluded from
  both `completed_steps` and the paused-step handling, so it is absent from
  `resume_skip` and gets re-executed) — never a `gate: review` pause
  (confirmed broken: a `PAUSED` step is unconditionally folded into
  `resume_skip` and silently skipped, bypassing the approval boundary
  rather than testing recovery from it) and never a hard process kill
  (confirmed the run log needed for resume is written once, after the step
  loop ends, so a kill leaves nothing for `--resume` to read). A
  MEDIUM-shaped instance: 2 of 4 steps already validated and preserved, the
  3rd fails its validator for one realistic reason, agent fixes the
  condition and resumes successfully — invariants center on no-duplication
  of the preserved steps and correct legitimate-retry of the failed one;
  MEDIUM range once the replay check is counted as a validation condition.
  A HIGH-shaped instance: the failing step's validator failure could
  plausibly be misdiagnosed as a different, superficially similar problem
  (a second surface — distinguishing the real cause from a plausible wrong
  one — and an added invariant: the agent must not "fix" the wrong thing
  and must not touch already-validated steps' artifacts while
  investigating), pushing to HIGH.

These are shapes for calibration, not the frozen instances.

## Family-specific construction rules

### T1 — Semantic Mechanism Routing (relabeled; see
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md` §Issue 2 — the surviving
substrate is resource/consumer-routing, not tool-invocation routing, so the
family name now reflects the broader "which mechanism governs this
outcome" construct rather than implying command/tool choice specifically)
- The task must state the desired *semantic outcome*, never the mechanism.
- At least one wrong-but-plausible route must fail on a genuine semantic
  difference (e.g., a build artifact not being picked up by the running
  package), not a cosmetic difference (e.g., a different log message for the
  same effect).
- If the frozen SHA's repository state does not reproduce a given ambiguity
  (e.g., `build/` is regenerated/absent in a clean checkout), the task must
  be re-grounded against what the clean, frozen checkout actually contains —
  never patched into existence by the evaluator setup step, which would
  itself violate M3 (evaluator-induced dirty baseline).

### T2 — Constrained State Transformation
- The permitted edit region and the preserved region must both be
  mechanically checkable (e.g., via structural YAML diff, not prose
  description).
- At least one existing automated check in the repository (e.g., the
  contract-agreement test) should be reusable as part of the hidden oracle,
  reducing the chance the oracle silently diverges from what the repository
  itself considers "correct."

### T3 — Operational Recovery / Idempotency
- **Interrupt mechanism, corrected twice** — see
  `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-2.md` §"T3 interrupt
  mechanism, corrected" for the first correction (hard process kill,
  withdrawn: the run log `_find_resume_state()` needs is written once,
  after the step loop ends, so a kill leaves nothing to parse) and
  `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §1 for the second
  (`gate: review` pause, also withdrawn: frozen-SHA-verified directly —
  `if paused: resume_skip.add(paused)` — a `PAUSED` step, whether from an
  unapproved gate or an explicit denial, is unconditionally folded into
  `resume_skip` and silently skipped as if complete, bypassing the approval
  boundary rather than testing recovery from it).

  **Verified-working mechanism**: a step's validator failure sets
  `status = "FAILED"` (distinct code path from gate denial/pause).
  `_resumable_terminal_statuses()` returns only `{MODE_CEILINGS[mode],
  "COMPLETED"}` — `FAILED` is not a member, and `_find_resume_state()`
  never treats it as `paused_step` either (that branch only fires on the
  literal string `"PAUSED"`). A `FAILED` step is therefore absent from
  `resume_skip` entirely, so `--resume` calls `execute_step()` on it again
  fresh — a genuine, code-verified legitimate retry, not a skip. Construct
  the interrupt as a task-constructed step whose validator fails on first
  attempt for a realistic, constructible reason within that validator's
  actual purpose (never an artificial crash); earlier steps whose status is
  a resumable terminal status are correctly preserved via `completed_steps`.
- **Recovery** = fix the underlying condition, then a second invocation of
  `workflow-runtime.py` with `resume=True` against the same session
  directory — the previously-failed step is retried and this time
  succeeds. **Replay/idempotency** = invoking `resume=True` a second time
  after the agent claims completion, expecting zero *new step/artifact/
  validation* ledger events — checked against `run-ledger.jsonl` via the
  existing `handle_audit_run` subcommand. `run_started`/`run_completed`-
  class bookkeeping events are explicitly exempted from this requirement
  (confirmed: every invocation logs these regardless of whether any step
  executes, so a literal zero-new-ledger-entry requirement is impossible to
  satisfy and is not what is checked). The ledger and its audit command
  remain useful as an independent verification layer on top of the actual
  resume mechanism — they establish *that* nothing was duplicated or
  corrupted, while the `resume=True` path is what establishes recovery
  *actually happened*; the two are complementary, not substitutes for each
  other.
- Partial state must arise from this real, reproducible mechanical
  procedure, never hand-edited into a shape that looks plausible but
  couldn't arise from real execution — hand-edited partial state risks
  testing "can the agent recognize our fabricated pattern" rather than "can
  the agent recover from real interruption," a construct-validity failure
  distinct from, but related to, `RECOVERY_RESET_LAUNDERING`. A
  byte-identical copy of the pre-recovery state, or a hash manifest taken at
  construction time, must be retained by the evaluator (never trusted to
  the agent) so the "unrelated state must remain untouched" invariant is
  checkable independent of the agent's own claims.
- The idempotency/replay check (§12 of the protocol draft) is mandatory for
  every T3 instance, not optional.

## Pilot vs. main-study instance rules

- Pilot instances (3, one per family) are disposable: they exist only to
  validate the instrument (oracle correctness, telemetry capture, regime
  differentiation, escalation mechanics, isolation, cost accounting). They
  must never be reused as, or lightly modified into, a held-out main-study
  instance — that would leak pilot-adjudication learning into a supposedly
  fresh evidence unit.
- Main-study instances (6, two per family) must be **selected and
  materialized** only after pilot adjudication is complete and the
  instrument is judged `PILOT INSTRUMENT VALID` (or
  `PILOT_INSTRUMENT_VALID_WITH_FAMILY_DROPPED`) per
  `AUTONOMOUS-TASK-V2-PILOT-PLAN.md` — corrected wording, since *authoring*
  and *freezing* the T1/T2 candidate texts (and T3's parameterized specs)
  happens pre-pilot (see the pool-freeze rule immediately below); what
  actually happens post-pilot is selection (the deterministic ranking) and
  materialization (a no-op for T1/T2's already-finished text; a real
  deterministic instantiation step for T3's spec). Pilot *performance*
  (which regime looked better) must never influence which candidates were
  authored or how they were shaped — only pilot *instrument defects* may,
  and only via explicit addendum to the frozen pool, never a fresh
  post-hoc candidate.
- **Candidate-pool freeze, before the pilot, T1/T2 vs. T3 split, oracle
  specs included** (closes post-pilot task-selection bias — see
  `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md` §Issue 1,
  `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-2.md` §1-§2, and
  `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §4 and §10 items 1-2 for
  the successive fixes, and `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §3b for
  the full mechanism). **Pre-pilot (authored/frozen)**: for T1 and T2
  (admissibility already proven at the frozen SHA), each of the 4 cells
  gets **exactly 3** fully-drafted, admissible candidate *texts*, each
  committed together with its oracle spec, complexity-breakdown, and any
  fixture-spec hashes (not the visible task alone — freezing only the task
  text left the hidden oracle's semantic requirements free to be shaped
  after seeing pilot behavior, even without bad faith). For T3
  (admissibility not yet proven — that is what the pilot tests), each of
  the 2 cells gets **exactly 3** frozen candidate *specifications*
  (parameterized, not finished task text — see the T3 rules above). This
  authoring/freezing step happens identically for BOTH the Tranche-1 pool
  and a second, symmetric Tranche-2 pool (36 candidates total), closing the
  identical selection-bias problem one stage later. **Post-pilot (selected/
  materialized)**: which candidate becomes the actual main-study instance
  is decided by a deterministic seeded ranking with the salt generated only
  after the manifest is frozen (commit-then-salt — §3b of the protocol
  draft), never by a human or agent choosing after seeing pilot behavior;
  materialization is a no-op for T1/T2 (already-finished text) and a real
  deterministic instantiation step for T3 (spec-to-instance, only performed
  if the T3 pilot's seven-link chain passes). The pool's extra candidates
  (rank 2 within the HIGH cell specifically, and rank 3) exist so the
  family-fallback expansion (a 3rd instance per family if T3 fails its
  pilot gate) and any later task/oracle-level invalidity replacement draw
  from the same pre-frozen pool rather than requiring fresh, post-hoc
  authoring. A run-level `HARNESS_UNSTABLE` interruption never triggers a
  different-task selection — only a same-task technical rerun. **If T3 was
  dropped in Tranche 1, Tranche 2 (if activated) draws only from its second
  pool's T1/T2 cells** using the same fallback shape — it never
  reintroduces T3 via the second pool's T3 Rank-1 draws.
