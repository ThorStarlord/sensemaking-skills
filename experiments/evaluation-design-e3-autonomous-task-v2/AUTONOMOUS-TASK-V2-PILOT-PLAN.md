# Autonomous Task v2 — Instrument Pilot Plan

Status: DRAFT. Describes a 9-run instrument pilot (3 disposable tasks x 3
regimes). This plan does NOT run the pilot — it defines what the pilot must
prove and how its outcome is adjudicated, so it can be executed later as a
separate, explicit step after human sign-off.

## Purpose

The pilot answers instrument questions ONLY:

- Are the three disposable task instances independently solvable at all
  (not too hard, not degenerate)?
- Is each hidden oracle valid (positive and negative calibration cases both
  behave correctly against the oracle logic itself)?
- Does telemetry capture actually populate the fields in
  `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md`?
- **Was the R0/R1/R2 treatment actually delivered** — prompts reach the
  agent correctly, hashes verified (`TREATMENT_DELIVERY_VALID`)? This is
  the pilot's actual pass bar for the regime manipulation, corrected in
  `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §"Pilot-design point":
  the pilot does **not** require R0 and R1 to show an *observed* behavioral
  difference to pass — requiring that would create pressure to edit LEAN
  until it produces a desired separation, contaminating the very question
  the main study exists to ask. If treatment delivery is confirmed valid
  but R0 and R1 behave identically anyway, that is recorded as
  `NO_BEHAVIORAL_UPTAKE` — a valid, reportable, negative finding ("protocol
  engineering didn't measurably change behavior at this task's scale"), not
  an instrument defect requiring repair.
- Are the R2 escalation mechanics operable (can an agent actually produce a
  well-formed escalation request; can the evaluator produce a narrow,
  non-leaking response)? **Corrected in Lock-Readiness Response 2 §9**: this
  is validated conditionally, not by requiring escalation to occur — see
  "Execution notes" below.
- Does filesystem-scope isolation and clean-state restoration actually work
  across repeated runs from a standalone clone?
- Does cost accounting produce internally consistent numbers across regimes
  (no `COST_ACCOUNTING_DRIFT`)?

Pilot performance (which regime "won") must NEVER be used to tune the six
main-study task instances. Only instrument DEFECTS discovered during the
pilot may change anything, and only through explicit supersession/addendum
to this or the protocol draft — never a silent edit.

## Disposable pilot task shapes (UNFROZEN DESIGN CANDIDATES)

These are illustrative shapes only, sized to MEDIUM-equivalent complexity so
the pilot doesn't accidentally validate only the easy end of the range.
None of these is a locked task instance.

### T1 pilot candidate — UNFROZEN DESIGN CANDIDATE (corrected in Hardening
Pass 1, relabeled "Semantic Mechanism Routing" in the Lock-Readiness
Response; see `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §1 and
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md` §Issue 2)
Ask for a semantic outcome achievable via editing `workflow-registry.yaml`
for one explicitly named consumer — either the local dogfood CLI path
(`skills/workflow-planner/references/workflow-registry.yaml`, read by
`scripts/workflow-planner.py` / `_validator_utils.py`) or the installed-
package-defaults path (`src/sensemaking_skills/defaults/workflow-registry.yaml`,
read by `WorkflowRegistry` for an external target repo) — with the intended
consumer stated as an explicit process-contract requirement (per Task
Construction §T1 rule: never left implicit). Hidden oracle exercises the
named consumer directly (e.g., instantiates `WorkflowRegistry` against a
throwaway target repo, or runs `scripts/workflow-planner.py` locally) and
checks its resulting workflow list. This construct was frozen-SHA-verified
in Hardening Pass 1 (both files confirmed to exist and to already differ in
content at `0ffb564b`); the pilot's remaining purpose is to confirm an agent
can actually be tasked with this distinction and produce a checkable result,
not to re-establish the substrate's existence.

### T2 pilot candidate — UNFROZEN DESIGN CANDIDATE
Add one new declared field to one existing artifact-contract block in
`skills/workflow-planner/references/artifact-contracts.yaml`, preserving all
other blocks byte-for-byte. Oracle: structural YAML diff over preserved
regions + a rerun of the field-contract-agreement check equivalent. Primary
pilot purpose: confirm the "multiple valid implementations, single checkable
shape" property actually holds (i.e., two structurally different but both
locally-valid insertions both pass the oracle).

### T3 pilot candidate — UNFROZEN DESIGN CANDIDATE (interrupt mechanism
corrected twice; see `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §3,
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-2.md` §"T3 interrupt mechanism,
corrected", and `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §1)

**Two superseded interrupt methods** (kept here only for the record — do
not use either): (1) killing the runner process once `run-ledger.jsonl`
showed N entries — the real resume capability parses a *different* file
(the markdown run log, written once after the step loop ends), so a kill
leaves nothing for it to read; (2) an unapproved `gate: review` step —
**frozen-SHA-verified directly**: `if paused: resume_skip.add(paused)`, a
`PAUSED` step (from either a genuinely unapproved gate or an explicit
denial — both set that status) is unconditionally folded into
`resume_skip` and silently skipped as already-complete, bypassing the
approval boundary rather than testing recovery from it.

**Verified-working method**: cause a step's own validator to fail on first
attempt, for a realistic, constructible reason within that validator's
actual purpose. Frozen-SHA-verified: `_resumable_terminal_statuses()`
returns only `{MODE_CEILINGS[mode], "COMPLETED"}` — `FAILED` is not a
member and is never treated as `paused_step` either, so a `FAILED` step is
absent from `resume_skip` entirely and `--resume` calls `execute_step()` on
it again fresh — a genuine, code-verified legitimate retry. Task the agent
with fixing the underlying condition and resuming to completion via a
second `workflow-runtime.py` invocation with `resume=True` against the same
session directory; earlier successfully-validated steps are correctly
preserved via `completed_steps`. Oracle: reuse `workflow-runtime.py`'s
existing `handle_audit_run` ledger-audit subcommand as a secondary check on
top of the resume outcome, plus hash-preservation of pre-existing
artifacts and a hidden replay check (re-invoke `resume=True` once more,
require zero new *step/artifact/validation* ledger events —
`run_started`/`run_completed`-class bookkeeping events are explicitly
exempted, since every invocation logs these regardless of step execution).
Primary pilot purpose: the mechanism-level evidence (a real, code-verified
legitimate-retry path, plus the append-only ledger as an independent audit
layer) is now strong and traced against actually-working code, but no live
validator-failure-and-resume cycle has actually been executed — the
pilot's central job is to perform that one execution and confirm the
resulting state is agent-solvable and oracle-checkable end to end.

**T3 pilot pass bar — the full seven-link causal chain, made explicit**
(Lock-Readiness Response §T3 final attack; verification substrate — the
ledger and audit command — is not the same thing as recovery substrate, and
the pilot must not conflate the two):

```
real repository operation begins
-> deterministic interruption leaves meaningful partial state
-> some work is already correct
-> recovery can preserve that work
-> restart/delete/recreate is detectably different from genuine recovery
-> agent can reach a valid final state
-> replay remains idempotent
```

All seven links must be demonstrated, not merely the substrate's structural
compatibility with them. If producing this chain requires inventing a
partial state no real repository operation could actually produce, **T3
fails construct admissibility and must not be rescued** — this is a valid,
complete, reportable pilot finding (see Outcomes below), not a pilot failure
to be forced past — and per the frozen family-fallback rule (Hardening Pass
1 §4), T1 and T2 each expand to 3 instances, drawn from their pre-frozen
candidate pools (§3b of the protocol draft — never freshly authored
post-hoc), to preserve 6 paired main-study tasks if T3 is dropped.

## Execution notes (for whoever runs the pilot later)

- 9 runs: 3 tasks x 3 regimes, fresh standalone clone per run, fresh agent
  session per run, randomized order, no shared conversational memory,
  identical task-visible contract across regimes for a given task.
- All telemetry and scorecard fields from the other draft documents apply
  in full — the pilot is not exempt from any capture requirement, since
  under-testing the instrument here would defeat the pilot's purpose.
- **R2 escalation is not forced** (corrected in Lock-Readiness Response 2
  §9 — requiring the pilot's R2 run to produce an escalation would reward
  escalating absent genuine uncertainty, exactly the behavior H3 exists to
  measure honestly). If spontaneous escalation occurs during the pilot's R2
  run, the request/response mechanism must work correctly (four-element
  format, narrow non-leaking response, verbatim logging). If no escalation
  occurs, the escalation channel is validated separately via a
  non-evidentiary handshake/calibration exercise — a synthetic
  request-response round trip exercised outside the scored pilot task —
  rather than treating the absence of escalation as an instrument failure.

## Outcomes

**Renamed and corrected in Lock-Readiness Response 2 §8** — the prior
version of this section described a stale "2 families x 2 levels x 3
regimes = 12 runs" narrowing that predates Hardening Pass 1's actual frozen
fallback (T1+T2 x 3 instances x 3 regimes = 18 runs), and used
`EXPERIMENT_NOT_ADMISSIBLE` for a family-level failure the fallback already
covers, which is confusing given the same name is reserved for a genuinely
inadmissible whole experiment:

```
PILOT_INSTRUMENT_VALID
  All oracles behave correctly under calibration (including T3's, if its
  seven-link chain passes); telemetry fields populate as designed;
  TREATMENT_DELIVERY_VALID confirmed for R0/R1/R2 (prompts delivered
  correctly, hashes verified) -- an observed R0-vs-R1 behavioral difference
  is NOT required for this outcome (corrected in Lock-Readiness Response 3
  -- see "Pilot-design point" above; its absence is recorded separately as
  NO_BEHAVIORAL_UPTAKE, a valid descriptive finding, not an instrument
  defect); the R2 escalation mechanism is validated per the conditional
  rule above; isolation and clean-state restoration held across all 9 runs
  with zero unreplaced ISOLATION_BREACH
  runs (a breached run must be excluded and replaced via technical rerun
  before its cell counts -- "individually explained and not systemic" is no
  longer an accepted substitute for replacement).
  -> Proceed to selection-driven materialization (T1/T2 mechanical
     instantiation from frozen texts; T3 mechanical instantiation from its
     frozen spec) and lock.

PILOT_INSTRUMENT_VALID_WITH_FAMILY_DROPPED
  family = T3
  Same bar as PILOT_INSTRUMENT_VALID for T1 and T2, but T3's seven-link
  chain (above) did not pass -- a valid, complete finding for that family
  specifically, not an instrument defect.
  -> Proceed with T1 + T2 only, each expanded to 3 instances via the frozen
     fallback rank mapping (MEDIUM Rank 1, HIGH Rank 1, HIGH Rank 2 --
     AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md §3b), preserving 6 paired
     main-study tasks and the 18-run total. Never narrowed to 12 runs.

CHANGES_REQUIRED_BEFORE_MAIN_LOCK
  One or more instrument defects found (e.g., an oracle's negative
  calibration case did not fail as expected; a telemetry field was
  consistently null; TREATMENT_DELIVERY_VALID could not be confirmed for
  one or more regimes -- prompts/hashes did not actually reach the agent as
  intended) that are plausibly fixable without redesigning the task family
  itself. NOTE, corrected for internal consistency: R0-vs-R1 behaving
  identically despite valid treatment delivery is NOT an instrument defect
  -- that is NO_BEHAVIORAL_UPTAKE (see "Purpose" above and the
  PILOT_INSTRUMENT_VALID condition below), a valid descriptive finding.
  -> Fix via explicit addendum, re-run only the affected pilot cell(s), then
     re-adjudicate.

EXPERIMENT_NOT_ADMISSIBLE
  Reserved for the case where the REMAINING design -- after any single-
  family drop -- cannot support the research question at all (e.g., two of
  the three families fail their pilot cells). Never used for a single
  family's pilot failure when the fallback covers it -- that case is
  PILOT_INSTRUMENT_VALID_WITH_FAMILY_DROPPED above.
```

Pilot success is explicitly NOT defined as "a particular regime wins" —
success is defined purely in terms of whether the instrument measures what
it claims to measure.
