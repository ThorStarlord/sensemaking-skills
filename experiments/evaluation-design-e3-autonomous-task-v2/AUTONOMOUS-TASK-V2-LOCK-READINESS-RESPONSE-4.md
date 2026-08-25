# Autonomous Task v2 — Lock-Readiness Response 4

Status: DRAFT. Small, final correction pass per the reviewer's third
line-by-line review (`CHANGES REQUIRED BEFORE PILOT LOCK`, 5 findings + 2
tiny schema cleanups). No pilot run, no lock, no hash, no dispatch.

## 1. R2 prompt — actually fixed this time, verified mechanically

`AUTONOMOUS-TASK-V2-REGIME-R2-ESCALATION.txt` rebuilt: the "this regime
also permits..." framing and the escalation-report instruction are both
moved out of the shared block (the framing now opens the ESCALATION
section; the report instruction now sits in the escalation section,
referencing item 10 rather than being appended to it). Verified, not just
asserted: `diff` between R1 lines 3-60 and R2's corresponding block returns
no differences; `sha256sum` of both blocks matches exactly
(`a19c6c2c...0cde4c` for both). The claim in Response 3 was true in intent
and false in the actual file; it is now true in the actual file, checked.

## 2. Three stale contradictions — fixed

- `PILOT-PLAN.md` `CHANGES_REQUIRED_BEFORE_MAIN_LOCK`: "R1 was not
  behaviorally distinguishable from R0" removed as an instrument-defect
  example; replaced with a `TREATMENT_DELIVERY_VALID`-framed example and an
  explicit note that behavioral non-distinguishability is
  `NO_BEHAVIORAL_UPTAKE`, not a defect — cross-referencing the rule earlier
  in the same file rather than contradicting it.
- `TASK-CONSTRUCTION.md`: "constructed only after pilot adjudication"
  corrected to "selected and materialized" after pilot, with the
  pre-pilot-authoring / post-pilot-selection distinction restated inline
  so the two rules in the same document no longer disagree.
- `PROTOCOL-DRAFT.md` §12 (T3 held-out verification): "requires zero
  additional mutation" replaced with "zero new step/artifact/validation
  ledger events," with the `run_started`/`run_completed` bookkeeping
  exemption stated explicitly at the point of the claim, not only in the
  T3 admissibility section elsewhere in the document.

## 3. `seed_tranche2_dispatch` — now genuinely frozen pre-pilot

Corrected: all three dispatch-order seeds (`seed_pilot`, `seed_3`,
`seed_tranche2_dispatch`) are generated at the same pre-pilot moment as
both candidate-pool manifests. Tranche-2 *activation* still depends on
Tranche-1 results, as it must — but the *seed* does not; it sits already
fixed whether or not Tranche 2 ever actually runs. Activation determines
use, not generation.

## 4. Absolute ROBUST-efficacy floor — added, closing the "cheap but
ineffective" false-positive path

Confirmed the failure mode precisely: with the rules as previously stated,
ROBUST 0/6 and LEAN 0/6 ACCEPTED, LEAN costing 40% less, aligned other
dimensions, would pass through H1 undetected (H1 only checks
ROBUST-accepted/LEAN-failed *pairs*, and finds none when ROBUST itself
never succeeds) straight into the `>25%` row, declaring
`EFFICIENCY_IMPROVED` for two regimes that accomplished nothing. **Fixed
with a new, highest-priority gate**: `ROBUST ACCEPTED rate < 5/6` (the
frozen threshold, adopted as proposed — ROBUST is explicitly the
high-reliability baseline, so a rate below this means the baseline itself
isn't established) stops the tranche and reports `EFFICACY_NOT_ESTABLISHED`
— no positive efficiency conclusion may be issued regardless of any cost
figure. This gate is checked *before* H1, since H1 alone structurally
cannot detect "both regimes failed."

## 5. H2 / Tranche-2 pair set — made one explicit, shared definition

`operational_actual_cost_usd`'s paired median (H2, §8) and the Tranche-2
decision rule's steps 2/3 (§10) now explicitly reference the *same* pair
set as §7's `paired_cost_delta_matched_outcomes` — both-ACCEPTED matched
pairs only — stated once and cross-referenced, not restated three
different ways that could quietly drift apart. A zero human-minutes delta
on those matched pairs is now explicitly defined as neutral/consistent,
not a contradiction requiring a nonzero match. Aggregate
`cost_per_accepted_task_usd` remains the separate cheap-failure guard
alongside the matched-pair view, per §7's existing "neither metric replaces
the other" language — unchanged, now correctly the thing step 3 points to
rather than an independently-worded parallel concept.

## Two tiny schema cleanups

- `monetary_cost_usd` retired as an independently-computed field and
  aliased exactly to `operational_actual_cost_usd` — it can no longer drift
  from the primary confirmatory dollar measure via a separately-maintained
  formula.
- `human_active_seconds_total` is now explicitly *defined* (not merely
  named) as the sum of `human_active_seconds` (escalation) +
  `operational_recovery_seconds` + `approval_review_seconds`;
  `manual_repair_seconds` and `research_evaluator_labor_seconds` are
  explicitly excluded, consistent with their own existing field
  descriptions (post-acceptance salvage cost and research labor,
  respectively) rather than left to be inferred.

## T3 — reviewer's own re-assessment recorded, no change needed

The reviewer independently re-traced the `PAUSED`-vs-`FAILED` distinction
and confirmed `T3_CONDITIONALLY_ADMISSIBLE` remains justified, with the
live pilot still required to prove the seven-link chain and the frozen
T1/T2 fallback available if it doesn't. No action needed here beyond what
Response 3 already did.

## Mechanical consistency pass performed

- `bash -n AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` — passes.
- R1/R2 shared-block diff and sha256 comparison — identical (§1 above).
- Grepped the bundle for the specific stale phrases named in the review
  ("R1 was not behaviorally distinguishable," "constructed only after
  pilot adjudication," "zero additional mutation," `seed_tranche2_dispatch`
  generated only if/when Tranche 2 activates) — no remaining live
  instances found outside corrected/historical context.
- Both candidate-pool manifests and all three dispatch seeds confirmed
  specified as pre-pilot-frozen throughout (§3b of the protocol draft, the
  Task Construction pool-freeze rule, and this document's §3).
- No task instance, pilot run, or main-study run has been dispatched,
  constructed, or hashed anywhere in the bundle.

## Status

All 5 numbered findings and both tiny schema cleanups addressed. Final
lock authorization remains with the reviewer's own re-inspection of the
corrected bundle.
