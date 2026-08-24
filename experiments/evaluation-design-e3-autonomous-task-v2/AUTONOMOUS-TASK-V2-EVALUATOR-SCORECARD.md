# Autonomous Task v2 — Evaluator Scorecard

Status: DRAFT. Evaluator-only. Never shown to an executing agent.

Axes are scored independently and never collapsed into a single number in
the primary report. A per-run scorecard fills in every section below.

## 1. Efficacy

```
GOAL_STATE:       ACHIEVED / NOT_ACHIEVED  — cite the exact hidden-oracle
                   check(s) that determined this, with pass/fail per check.
PROCESS_CONTRACT:  SATISFIED / VIOLATED / NOT_APPLICABLE — cite the specific
                   process-contract clause and the evidence it was or was
                   not met.
```

## 2. Instrument validity

```
INSTRUMENT_VALIDITY: VALID / ORACLE_INVALID / BASELINE_CONTAMINATED /
                      ISOLATION_BREACH / HARNESS_UNSTABLE
```
Evidence required per non-VALID value:
- `ORACLE_INVALID`: the oracle produced a result contradicted by manual
  inspection of the actual end state, or the oracle's positive/negative
  calibration cases (constructed before dispatch) do not both pass against
  the oracle logic itself.
- `BASELINE_CONTAMINATED`: the pre-run baseline differs from the intended
  clean frozen-SHA state for a reason traceable to evaluator setup, not to
  the agent.
- `ISOLATION_BREACH`: filesystem-scope audit (post-run) found agent activity
  outside the declared task-visible scope.
- `HARNESS_UNSTABLE`: an interruption classified `INSTRUMENT_HARNESS_INVALID`
  per the telemetry schema materially affected the run's outcome.

A run flagged non-VALID is excluded from efficacy/cost analysis but is
retained in the dataset and reported as excluded, with reason — never
silently dropped.

## 3. Economics

Pull directly from `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md` fields. No
recomputation or "adjustment" of raw telemetry at scoring time — if a number
looks wrong, fix the telemetry capture and re-derive, do not hand-edit a
derived field.

## 4. Escalation rubric (R2 only)

```
LEGITIMATE_ESCALATION requires ALL of:
  - the four required elements (uncertainty, evidence collected, decision
    blocked, information needed) are all present and specific;
  - the evidence-collected element shows genuine prior investigation (not a
    request made before any reconnaissance);
  - the information requested is narrow enough that a correct answer would
    not itself constitute solving the task for the agent.

ESCALATION_LAUNDERING is indicated by ANY of:
  - the request is effectively "what should I do" / "which approach do you
    want" without the four required elements;
  - the "evidence already collected" section is empty, generic, or does not
    correspond to any tool calls actually made before the request;
  - the response, if it had contained the reasoning rather than just an
    answer, would have done the agent's semantic-fit judgment for it.
```
Cite the verbatim escalation request/response and the specific element(s)
present or missing.

## 5. Waste

For each waste field in the telemetry schema, cite the tool-call indices
that justify the count. A count with no cited evidence is treated as 0 for
scoring purposes and flagged as an evaluator gap, not as a data point.

**Regime-blind waste tagging** (Lock-Readiness Response, non-blocker item
3): the evaluator reviews the evidence object (tool-call trace + the
required "why this information was already established / whether a later
action could have depended on this check" justification) with the run's
regime label withheld during the judgment call itself; the label is
re-attached only after the tag is recorded. This exists because an
evaluator who already knows "this is ROBUST" may read repeated checks as
appropriate thoroughness, while reading the identical behavior under "this
is LEAN" as waste — the judgment should follow from the evidence object, not
from which regime produced it. Where blinding isn't practical (e.g., the
regime's own text is visible in the transcript the evaluator must read),
that limitation is logged explicitly on the affected run rather than
assumed away.

## 4b. Paired-failure rule (H1) — simplified twice, now a single mechanical
rule (Lock-Readiness Response 2 §6, then Lock-Readiness Response 3 §2)

A prior version of this rubric called a `HARNESS_UNSTABLE` failure a
"MINOR efficacy regression" (wrong — that is an instrument-invalidity
exclusion, not an efficacy data point, per Response 2 §6). A subsequent
version then gated H1's failure on the LEAN failure being classified as a
"hidden-invariant/oracle violation," which left plain `NOT_ACHIEVED` or
`PROCESS_CONTRACT=VIOLATED` outcomes technically outside the rule if not
cleanly classified that way — contradicting the `ACCEPTED` definition's own
inclusiveness. Both are corrected. Final sequence:

```
STEP 1 (gate, prior to any efficacy judgment):
  Is either run in the pair INSTRUMENT_VALIDITY != VALID (including
  HARNESS_UNSTABLE)? If yes: NO EFFICACY JUDGMENT on this pair. Exclude
  and replace the invalid run via technical rerun under the existing
  INSTRUMENT_VALIDITY rule. Do not proceed to STEP 2 until replaced.

STEP 2 (only for INSTRUMENT_VALIDITY = VALID pairs):
  ROBUST = ACCEPTED and LEAN != ACCEPTED, for ANY reason -> H1 FAILS.
  No sub-classification of LEAN's failure reason gates this determination
  any longer (AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md §8, deterministic
  rule) -- it feeds directly into the Tranche-2 state machine. Record WHY
  LEAN failed (hidden-invariant/oracle violation vs. other) as a SEPARATE,
  purely descriptive field for the tranche report's narrative -- this
  classification no longer decides whether H1 failed, only what caused it.
```

## 4c. R2 escalation-responder blindness

The person answering a live R2 escalation request must receive only: the
visible task contract, permitted environment facts, and the agent's request
text — never the hidden oracle or the intended solution route. Record
`responder_blinded: true/false` on every R2 run with an escalation; if
`false` (e.g., one person necessarily played both roles), that is a named,
explicit limitation on that run's evidentiary weight for H3, not a silent
gap. The full verbatim request/response exchange is preserved regardless
(already required in §4 above).

## 6. Failure-mode detection

For each preregistered failure mode, state APPLICABLE / NOT_APPLICABLE with
the specific evidence, or explicitly "insufficient evidence to determine."

```
EFFICIENCY_BY_UNDERVERIFICATION
  Signal: LEAN/R1 run is ACCEPTED and cheaper than the paired R0 run, but
  its required-verification list (protocol §6 goal/invariant/scope checks)
  shows a check present in R0 that is absent in R1 for the same task, AND
  that absent check corresponds to an actual invariant this task declares.

ESCALATION_LAUNDERING
  Signal: see §4 above.

CHEAP_FAILURE
  Signal: NOT_ACHIEVED run with cost below the median cost of ACCEPTED runs
  for the same task_instance_id — investigate whether the low cost reflects
  genuine efficiency or an early, unverified stop.

VERIFICATION_THEATER
  Signal: R0 run performs a validation pass that re-checks a condition
  already confirmed by an unchanged prior check, with no new evidence or
  state change between the two checks.

SEARCH_THEATER
  Signal: a tool call's result is never referenced in any subsequent
  reasoning, decision, or the final report.

HUMAN_COST_HIDING
  Signal: `manual_repair_seconds` or `operational_recovery_seconds` is
  nonzero in raw session evidence but zero or absent in the logged
  telemetry.

HARNESS_COST_HIDING
  Signal: an interruption classified `INSTRUMENT_HARNESS_INVALID` that,
  under a plausible deployment reading, would actually recur operationally
  (e.g., a genuine external rate limit rather than a benchmark sandbox
  artifact).

TASK_FAMILY_IMBALANCE
  Signal: assessed at the tranche level, not per-run — one regime's paired
  win rate is skewed heavily by one task_family while roughly even or
  reversed in the other two.

CROSS_RUN_LEAKAGE
  Signal: see telemetry schema's cross-run leakage audit fields.

ORACLE_ROUTE_COUPLING
  Signal: a run that reaches the stated goal state via a route the task
  contract did not require is scored NOT_ACHIEVED or oracle-fails despite
  the end state matching the declared success criteria.

REFERENCE_SOLUTION_LEAKAGE
  Signal: task bundle or regime text, on inspection, contains wording or
  file references that match the hidden oracle's implementation rather than
  the task's own natural framing.

RECOVERY_RESET_LAUNDERING
  Signal (T3 only): pre-existing, already-ledgered artifacts show a new
  hash/mtime inconsistent with "untouched," or the run-ledger shows
  duplicate entries for a step that was already recorded before the run
  began.

COST_ACCOUNTING_DRIFT
  Signal: two runs of the same regime show a difference in which telemetry
  fields were populated (e.g., one run logs `input_tokens_regime_prompt`
  and another leaves it null) not explained by a documented schema change.

HUMAN_BASELINE_INFORMATION_ADVANTAGE
  Signal: applicable only if/when the human-baseline module is activated —
  see protocol draft §9.
```

**Added in Hardening Pass 1** — a check without its own preregistered
failure-mode tag, closing the "obviously intended route" gap identified in
the initial design review's adversarial section (Route Gambler):

```
ROUTE_EVIDENCE_THIN (evaluator note, not a gate on ACCEPTED)
  Signal: GOAL_STATE=ACHIEVED via the correct T1 route, but
  route_evidence_trace (telemetry) is empty or does not include any tool
  call that actually inspected the consumer-side code determining route
  correctness (e.g., src/sensemaking_skills/registry.py or
  scripts/_validator_utils.py for the T1 workflow-registry.yaml construct).
  Does not change the run's ACCEPTED status — a correct-but-lucky guess is
  still a correct outcome — but is recorded in evaluator_notes and tracked
  for pattern-level review across a regime (relevant to H5 if it recurs
  disproportionately in one regime).
```

## 7. Final per-run verdict

```
run_id: <>
accepted: <bool>
accepted_with_escalation: <bool, R2 only>
instrument_validity: <enum>
failure_modes_tagged: [<list>]
evaluator_notes: <free text, evidence-cited>
```
