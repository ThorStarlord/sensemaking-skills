# Autonomous Task v2 — Lock-Readiness Response 3

Status: DRAFT. Response to the reviewer's second line-by-line pass against
the corrected bundle (`CHANGES REQUIRED BEFORE PILOT LOCK`, 10 numbered
findings + 1 pilot-design point). No pilot run, no lock, no hash, no
dispatch, no main-study task instantiated.

---

## 1. T3's gate-based mechanism — independently re-verified as broken,
replaced with a mechanism verified to actually work

**Re-checked directly against the frozen SHA** (not taken on the
reviewer's word): `scripts/workflow-runtime.py`, the resume-skip
construction —

```python
resume_skip = set(resume_state.get("completed_steps", []))
paused = resume_state.get("paused_step")
if paused:
    resume_skip.add(paused)
```

— confirms the finding exactly: a `PAUSED` step (whether from a genuinely
unapproved gate, or from `_manage_gate` returning `denied_by_user`, both of
which set `status = "PAUSED"` — checked directly) is unconditionally added
to `resume_skip`, and the execution loop then treats any index in
`resume_skip` as already-completed and skips it, writing a synthetic
`"status": "COMPLETED"` result. **The prior "corrected" mechanism was wrong
— it bypasses the approval boundary rather than honoring it.** This is
withdrawn.

**Also re-checked and confirmed: the "zero new ledger entries" replay
oracle is impossible as literally stated.** Every invocation logs
`run_started` (and, on completion, `run_completed`)-class events regardless
of whether any step executes — a second `resume=True` invocation against an
already-complete run will always add at least these run-level bookkeeping
events to the ledger, even with zero step/artifact/validator work performed.

**Replacement mechanism, traced through the same code and confirmed to
work as intended**: a step's validator failure (not a gate denial) sets
`status = "FAILED"` (`scripts/workflow-runtime.py`, the `v_failures`
branch, and separately the `gate_result in ("failed",)` branch — both
distinct from the `denied_by_user` branch that sets `PAUSED`).
`_resumable_terminal_statuses()` returns only `{MODE_CEILINGS[mode],
"COMPLETED"}` — `FAILED` is not a member, and `_find_resume_state()` only
special-cases `PAUSED` separately from the resumable set. **A `FAILED` step
therefore lands in neither `completed_steps` nor `paused_step`, so it is
absent from `resume_skip` entirely, and the execution loop calls
`execute_step()` on it again fresh on `--resume`.** This is a genuine,
legitimate retry — not a skip, not a bypass — while every earlier step
whose status is in `resumable_terminal_statuses()` (e.g., `VALIDATED` for
`autonomous_execution`) is correctly preserved and skipped via
`completed_steps`.

**Corrected T3 construct**: interrupt = a step's own validator fails on
first attempt for a realistic, constructible reason (e.g., a precondition
the task's construction deliberately leaves unmet for that run, of the kind
this validator is designed to actually catch — not an artificial crash).
Recovery = fix the underlying condition, then re-invoke
`workflow-runtime.py --resume` against the same session directory; prior
successfully-validated steps are preserved and skipped, the failed step is
legitimately retried and this time succeeds. Idempotency oracle, corrected
to match the confirmed run-level-bookkeeping fact above: **zero new
step/artifact/validation ledger events on a second post-completion
`--resume` invocation; `run_started`/`run_completed`-class events are
exempted from the "zero new mutation" requirement, not silently ignored** —
this exemption is stated explicitly in the oracle spec, not glossed over.

This mechanism was found and traced through the same source reading that
found the reviewer's original bug, not asserted on authority — it genuinely
exists in the code and is genuinely different from the broken gate path,
so **T3 is not dropped**; it is corrected a second time, this time against
a directly-confirmed working code path rather than a plausible-looking one.
`AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §3 and §3b, `AUTONOMOUS-TASK-V2-
TASK-CONSTRUCTION.md` §T3, and `AUTONOMOUS-TASK-V2-PILOT-PLAN.md` §T3 are
all updated accordingly; every stale gate-pause or hard-kill description
identified in finding 5 (below) is corrected in the same pass, not left as
surviving prose.

---

## 2. H1 — simplified to the reviewer's exact rule

**The gap, confirmed real**: gating H1 on the failure being classified as
"traces to a hidden-invariant/oracle violation" left `LEAN NOT_ACHIEVED`
and `LEAN PROCESS_CONTRACT=VIOLATED` cases technically outside H1's failure
condition if an evaluator didn't (or couldn't cleanly) classify them that
way — contradicting the `ACCEPTED` definition's own inclusiveness (§6 of
the protocol: goal achieved AND process contract satisfied AND oracle
passes AND no forbidden mutation AND instrument valid).

**Fix, adopted exactly as proposed**: after instrument-invalid runs are
excluded and replaced (unchanged, still the prior gate), **H1 FAILS on any
single valid pair where ROBUST = ACCEPTED and LEAN != ACCEPTED, full stop
— no sub-classification of LEAN's failure reason gates this determination
any longer.** Severity/cause classification (hidden-invariant violation vs.
other) is retained as a *separate*, purely descriptive field attached to
the failing pair for the tranche report's narrative — it explains the
failure, it no longer decides whether H1 failed.

---

## 3. Tranche-2 decision rule — made a strict, non-overlapping priority
order; dollar view named

**The contradiction, confirmed real**: the outcome table's `<10%`/`>25%`
stop rows were not conditioned on cross-dimension consistency, so a result
like -30% dollars / +20% wall-clock / +15% human-minutes could satisfy both
"clearly meaningful, stop" and "inconsistent across dimensions, Tranche-2
eligible" simultaneously. Separately, "paired median model/API cost
reduction" never said which of the two dollar views (operational-actual vs.
dynamic-execution-resource) drives the percentage.

**Fix — strict priority order, evaluated top to bottom, first match wins**:
```
1. H1 FAILS (any valid pair, ROBUST accepted / LEAN not accepted)
   -> STOP; report the efficacy failure. Highest priority, overrides
      everything below.

2. (H1 holds) Are wall-clock and human-minutes paired deltas consistent in
   direction with the operational_actual_cost_usd paired delta?
   NO  -> MATERIALLY AMBIGUOUS; Tranche 2 eligible, regardless of the
          dollar percentage magnitude.
   YES -> continue to 3.

3. (H1 holds, dimensions consistent) operational_actual_cost_usd paired
   median reduction -- THIS is the named decision variable; dynamic_
   execution_resource_cost_usd remains required, co-equal REPORTING (per
   §4/§7) but does not drive this specific decision:
   <10%    -> STOP; negligible
   10-25%  -> Tranche 2 eligible
   >25%    -> STOP; EFFICIENCY_IMPROVED
```
Because step 2 is evaluated before step 3's magnitude bands, the exact
contradiction the reviewer found is now structurally impossible — a result
can never simultaneously qualify for a magnitude-based stop and a
consistency-based Tranche-2 eligibility.

---

## 4. Oracle-spec pool commitments — added for T1/T2

**The gap, confirmed real**: T3's frozen pre-pilot spec already included
oracle requirements, but T1/T2's manifest entry was `(candidate_id, family,
level, sha256(task_text))` — the *visible* task only. This left a real
path: freeze the visible task, run the pilot, then design the hidden oracle
for the main task afterward, informed by what was observed — without
anyone needing to act in bad faith.

**Fix**: every T1/T2 candidate commitment now includes, frozen at the same
pre-pilot moment as the task text:
```
candidate_id
family
level
task_text_sha256
oracle_spec_sha256                    the hidden oracle's semantic
                                       requirements (what it checks and why)
complexity_breakdown_sha256           the rubric scoring that assigned
                                       MEDIUM/HIGH
initial_state_or_fixture_spec_sha256  any fixture/starting-state
                                       requirements
```
The *executable* oracle implementation may still be mechanically
materialized later from this frozen spec (paralleling T3's spec-to-instance
materialization) — what changes is that its semantic requirements, not just
its existence, are committed before the pilot runs. Commit-then-salt now
genuinely freezes the whole task, not only what the agent sees.

---

## 5. T3 stale pre-correction descriptions — removed

`AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §3 (T3 admissibility paragraph, the
"process killed after step 3 of 5" framing and literal
zero-new-ledger-entry replay language) and `AUTONOMOUS-TASK-V2-TASK-
CONSTRUCTION.md` §T3 (the HIGH-complexity truncated-artifact worked
example) are rewritten to describe the validator-failure/legitimate-retry
mechanism from §1 above, not the withdrawn gate-pause mechanism or the
original hard-kill mechanism before that. No description of an interrupt
method this repository's code does not actually support survives anywhere
in the bundle after this pass.

---

## 6. R2 — restructured for genuine, mechanically-verifiable byte identity

**The gap, confirmed real**: the previous R2 kept items 1-9 identical to R1
but inserted escalation-report language into item 10 itself and a
lead-in sentence before item 1, so the "byte-for-byte identical" claim was
false for the actual shared block, even though the *content* difference was
minor and disclosed.

**Fix, structured exactly per the reviewer's template**: R2 is rebuilt as
four literal sections: (1) an R2-only header line, (2) the *exact* R1
body — from "You are executing..." through item 10, **unmodified,
including item 10 exactly as R1 has it**, with no lead-in sentence and no
escalation-report clause inserted anywhere inside it, (3) the escalation
extension (four-element request format, response constraints, one-per-run
limit, AND the "if you escalated, include a copy in your report"
instruction — moved here from item 10), (4) an R2-specific closing
paragraph replacing R1's "you will not receive human assistance" paragraph
(which is factually inapplicable to R2 and was never claimed to be shared).
Verified directly: a diff of R1's full body (line 3 through the end of item
10) against R2's corresponding block now shows zero differences — the
shared block can be hashed and compared mechanically, exactly as requested,
not merely asserted as "effectively" the same.

---

## 7. Dynamic-cost / cache semantics — demoted to diagnostic, not
confirmatory

**The gap, confirmed real**: a provider's `cached_input_tokens` figure can
include cached *conversation history*, not only the original static
task/regime prefix — substituting the provider's whole cached-token count
for "static prefix" could subtract genuine execution history, silently
deflating the dynamic-execution cost figure by an amount that has nothing
to do with prompt length.

**Fix, adopted as proposed**: `operational_actual_cost_usd` remains the
sole **primary, confirmatory economic dollar measure**. The per-call
subtraction figure is demoted: `dynamic_execution_input_tokens` and
`dynamic_execution_output_tokens` (token counts, not dollars) plus tool-call
counts and wall-clock are reported as **normalized behavioral/resource
diagnostics**, used to interpret *why* a cost difference occurred, never to
assert a confirmatory dollar-efficiency claim on their own. A derived
`dynamic_execution_resource_cost_usd` MAY additionally be computed **only**
when the provider exposes exact cache-segment attribution (i.e., can
distinguish "static prefix" from "prior turns" within its cached-token
report) — and even then it is labeled best-effort/conditional, never
promoted to confirmatory status alongside `operational_actual_cost_usd`.
H2's dual-view requirement is updated: the two required, co-equal views are
now `operational_actual_cost_usd` (dollars, confirmatory) and
`dynamic_execution_input_tokens + dynamic_execution_output_tokens` (tokens,
diagnostic) — not two dollar figures.

---

## 8. Human-attention timing — exact timestamps specified

**The gap, confirmed real**: `human_active_seconds_total` had no specified
measurement boundary, risking silent substitution of request-to-response
*latency* (which includes idle time before a responder even looks at the
request) for genuine active attention — directly relevant since H3 depends
on escalation attention specifically, and the Design Review already
disclosed this as an unbuilt instrumentation dependency.

**Fix**: three explicit timestamps are now required —
`escalation_request_emitted_at`, `responder_started_at` (when the responder
actually begins working the request), `responder_submitted_at` (when the
response is sent). `human_active_seconds = responder_submitted_at -
responder_started_at` — **never** `responder_submitted_at -
escalation_request_emitted_at` (that would be latency, not attention). If
`responder_started_at` cannot be captured in a given execution environment,
the field is renamed `response_latency_seconds` for that run and no
human-attention-savings claim may be drawn from it — logged as a per-run
limitation rather than silently reported under the attention field's name.

---

## 9. Manual repair no longer able to retroactively create ACCEPTED

**The gap, confirmed real and correctly flagged as dangerous**:
`manual_repair_seconds`'s prior description ("time spent by a human to
reach ACCEPTED after agent completion") implied the acceptance
determination could happen *after*, and be conditioned on, human repair —
entangling efficacy and cost-benefit exactly as the reviewer said.

**Fix — ordering made explicit and enforced**: `accepted` /
`accepted_with_escalation` are frozen at the moment the hidden oracle and
process-contract evaluation run against the agent's own completion state —
**before** any human repair is considered, full stop. A new boolean field,
`salvaged_after_manual_repair`, plus the existing `manual_repair_seconds`,
record post-hoc human salvage as a separate, clearly-labeled fact; neither
field, nor any amount of manual repair, can change an already-frozen
`accepted` value. A NOT_ACCEPTED run that a human later salvages remains
NOT_ACCEPTED for efficacy/economics purposes, with the salvage cost
recorded separately (useful for deployment-realism discussion, never for
inflating an accepted-outcome count).

---

## 10. Mechanical consistency fixes — all seven addressed

1. §3b's "at least 3" is tightened to **exactly 3** per cell (3 x 6 cells =
   18 per pool).
2. The sequential-design diagram is corrected to show **two** 18-entry
   pools (36 total pre-pilot commitments), not one, matching §2 of Lock-
   Readiness Response 2.
3. **Tranche-2/T3-drop interaction, closed**: if T3 was dropped in Tranche
   1 (family-fallback triggered), Tranche 2 — if it activates — draws only
   from its own second pool's T1/T2 cells, using the same 3-instances-per-
   family fallback shape; it never reintroduces T3 via the second pool's
   T3 Rank-1 draws. Stated explicitly rather than left to be inferred.
4. `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md`'s pool-freeze section now
   distinguishes, in so many words: **pre-pilot** = authored and frozen
   (T1/T2 full texts + oracle specs; T3 parameterized specs); **post-pilot**
   = selected (by the deterministic ranking) and materialized (mechanical
   instantiation, needed only for T3's spec-to-instance step — T1/T2's
   selected candidates are already finished text, materialization is a
   no-op for them beyond "this is now the locked instance").
5. Pilot dispatch order and Tranche-2 dispatch order each get their own
   frozen seed (`seed_pilot`, `seed_tranche2_dispatch`), generated by the
   same commit-then-independent-salt procedure as the main-study dispatch
   order (`seed_3`) — not left to ad hoc ordering at run time.
6. Preflight check renamed `task-bundle-matches-frozen-hash` (from
   `task-bundle-excludes-evaluator-artifacts`, which overclaimed — a
   contaminated bundle can have a perfectly matching hash if it was
   contaminated before the hash was taken). A separate, explicitly named
   pre-lock requirement is added: a human/process bundle-separation audit
   (confirming the agent-visible bundle actually excludes evaluator-only
   content) must occur once, before the hash is taken, as a prerequisite to
   the hash meaning what the check now honestly claims it means.
7. The preflight footer's "explicitly waived by a human" escape hatch is
   removed. A fail-closed dispatch gate does not need, and should not
   offer, a waiver path; the one honest, permanent limitation is already
   correctly carried by the always-reported `ENV_LIMIT` line, which is not
   a waiver — it is a disclosure that cannot be dismissed by anyone
   checking a box.

---

## Pilot-design point: TREATMENT_DELIVERY_VALID vs. NO_BEHAVIORAL_UPTAKE

**Adopted exactly as proposed.** The pilot's pass condition no longer
requires R0 and R1 to show an *observed* behavioral difference — that would
create pressure to edit LEAN until it produces a desired separation, which
would contaminate the very question the main study exists to ask. Instead:
`TREATMENT_DELIVERY_VALID` (prompts delivered correctly, hashes verified,
both regimes' text confirmed to reach the agent as intended) is the actual
pilot pass bar for this item. If R0 and R1 turn out to behave identically
despite genuinely different instructions, that is recorded as
`NO_BEHAVIORAL_UPTAKE` — a valid, reportable, negative finding ("protocol
engineering didn't measurably change behavior at this task's scale") rather
than an instrument defect requiring repair. `AUTONOMOUS-TASK-V2-PILOT-
PLAN.md`'s Purpose section and `PILOT_INSTRUMENT_VALID` condition are
updated accordingly.

---

## Status

All 10 numbered findings and the pilot-design point are addressed. Item 1
(T3) required and received independent re-verification against the actual
frozen-SHA source — not just applying the reviewer's fix, but re-tracing
the code myself, which confirmed the bug exactly as described and located a
different, genuinely-working code path (`FAILED` status via validator
failure) rather than either forcing the broken gate mechanism through or
dropping T3 by default. No task family was abandoned; T3 survives on
stronger, now twice-corrected evidence. Final lock authorization remains
with the reviewer's own re-inspection of the corrected bundle.
