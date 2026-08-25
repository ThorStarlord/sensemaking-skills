# Autonomous Task v2 — Lock-Readiness Response 2

Status: DRAFT. Response to the human reviewer's line-by-line pass against
the uploaded bundle (`CHANGES REQUIRED BEFORE PILOT LOCK`, 11 numbered
issues). No pilot run, no lock, no hash, no dispatch, no main-study task
instantiated. This is a targeted correction pass over the nine checks the
reviewer specified as the lock bar, not a broad redesign.

---

## 1. Post-pilot selection — the two remaining gaps, closed

### 1A. Selection independence from the task author

**The gap**: `seed = sha256(frozen_sha || salt_string)` is computable by
the constructor before authoring any candidate, so while the pool is being
written the constructor could in principle already know which
`candidate_id` will rank first and shape authorship around that knowledge.
This isn't post-pilot bias (no regime has run yet), but it isn't
author-independent either.

**Fix — commit-then-salt, adopted exactly as proposed**:
1. The constructor authors all candidate texts with fixed, arbitrary
   `candidate_id`s (e.g., `T1-MEDIUM-A`, `T1-MEDIUM-B`, ...), assigned
   without reference to any ranking.
2. The complete candidate manifest (all `(candidate_id, family, level,
   sha256(task_text))` rows) is frozen and hashed as a whole:
   `manifest_hash = sha256(manifest)`. This commitment is recorded before
   the next step.
3. **Only after `manifest_hash` is frozen** is an independent random salt
   generated — by a process the constructor does not control at authoring
   time (e.g., OS-level CSPRNG bytes captured and logged at the moment of
   freeze, by a party other than the constructor, or from an external
   unpredictable source). The salt is recorded alongside `manifest_hash`.
4. Ranking: `rank_key(candidate_id) = sha256(manifest_hash || salt ||
   candidate_id)`, ascending.

Because the salt cannot exist until after the manifest (and every
`candidate_id` in it) is already fixed, the constructor cannot have shaped
any candidate's content around knowledge of its eventual rank — the
salt genuinely introduces information the constructor did not have while
writing.

### 1B. Tranche 2 has no preregistered source — closed

**The gap**: Tranche 2 (6 new tasks) had no frozen source, recreating the
exact selection-bias problem one stage later — author six new tasks only
after seeing Tranche-1 results.

**Fix**: a **second, symmetric candidate pool is frozen at the same
pre-pilot moment as the Tranche-1 pool** — 18 more candidates (3 per
family x level cell), manifest-hashed, and ranked via its own independently
generated salt (`salt_2`, generated after `manifest_hash_2` is frozen, by
the same commit-then-salt procedure as 1A, and distinct from `salt` used
for Tranche 1). If Tranche 2 activates, its 6 instances are the Rank-1
draws from this second pool — already fixed before Tranche-1 results, let
alone Tranche-2 activation, exist. Authoring cost is real (36 candidates
total instead of 18) but this is the only way to close the loophole
completely rather than partially, and it costs nothing at pilot time (only
the Tranche-1 pool's 3 disposable-adjacent instances are touched before
Tranche-2 activation is even decided).

### 1C. Fallback rank mapping — made explicit

**The gap**: "Rank 2 is used for the fallback 3rd instance" didn't say Rank
2 of which cell (MEDIUM or HIGH).

**Fix, stated explicitly**: the family-fallback 3rd instance (triggered
only if T3 fails its pilot gate — Hardening Pass 1 §4) is **HIGH-cell Rank
2** — i.e., the *second*-ranked HIGH-shaped candidate from that family's
pool. This reproduces exactly the "MEDIUM, HIGH, HIGH-variant" shape
Hardening Pass 1 described in prose, now unambiguous: the fallback triple
for a family is {MEDIUM Rank 1, HIGH Rank 1, HIGH Rank 2} — never a second
MEDIUM instance, because complexity differentiation (H4) is where the
extra depth matters most.

### Reserve semantics corrected (smaller item, same section)

**The gap** (reviewer's smaller-issues list): Rank-3 "reserve" replacement
was described loosely enough to be confused with ordinary run-level retry.

**Fix**: Rank 3 is invoked **only** when a *selected candidate itself* is
found task/oracle-level invalid (`ORACLE_INVALID`, or a task-construction
defect discovered during main-study execution) — never for a run-level
`HARNESS_UNSTABLE` interruption, which triggers a same-task technical
re-run under the existing `INSTRUMENT_VALIDITY` rule instead. A harness
hiccup never causes a different task to be selected.

---

## 2. T3 pre-pilot freeze vs. "prove recovery before building" — reconciled

**The contradiction, confirmed real**: §3b (all families get fully-drafted,
admissibility-checked candidates before pilot) directly conflicts with the
T3 pilot's own stated purpose (prove the recovery construct before either
T3 held-out task is built) — you cannot have fully-drafted, ready-to-run T3
task instances before you've proven T3's construct produces solvable,
checkable instances at all.

**Fix — parameterized specs for T3, full texts for T1/T2**: the pool-freeze
procedure now has two modes, stated explicitly rather than applied
uniformly:

- **T1 and T2** (admissibility already proven at the frozen SHA in
  Hardening Pass 1): pool candidates are fully-drafted, ready-to-run task
  texts, hashed as before.
- **T3** (admissibility itself is what the pilot tests): pool candidates
  are **frozen parameterized specifications**, not finished task text —
  each spec fixes, before the pilot: the visible task-contract template,
  the source repository operation, the interrupt boundary (see §"T3
  interrupt mechanism, corrected" below), the complexity classification,
  the state-construction parameters, the oracle requirements, and a
  selection identity/hash over all of the above. Selection (§1A/1C) is
  applied to these frozen specs exactly as to T1/T2's frozen texts — no
  human or agent picks a spec after seeing pilot results. Only **if** the
  T3 pilot's seven-link chain (Pilot Plan §T3) passes does the selected
  spec get **mechanically materialized** into an actual task instance —
  a deterministic instantiation step, not a fresh authoring decision.

This preserves "no post-pilot selection" for T3 without falsely claiming a
proven-admissible recovery task already exists before the recovery
construct itself is proven.

---

## 3. R2 = exact R1 + escalation — fixed

`AUTONOMOUS-TASK-V2-REGIME-R2-ESCALATION.txt` was rewritten so its
execution-discipline body (items 1-10, the priority-order paragraph) is
byte-for-byte identical to `AUTONOMOUS-TASK-V2-REGIME-R1-LEAN.txt`,
confirmed by direct diff — the only difference in that shared body is one
explicitly-flagged, necessary addition to item 10 (an instruction to
include the escalation copy in the final report, which cannot exist in R1
since R1 has no escalation to report). The ESCALATION section is appended
after item 10, unchanged from the prior draft. The closing "you will not
receive human assistance" paragraph, which was already regime-specific
content (R1 asserts no assistance at all; R2 must state the one-escalation
exception), remains correctly different — that was never claimed to be
identical, only the execution-discipline body was. H3 now compares LEAN
against LEAN-plus-escalation with no other confound.

---

## 4. Execution-phase cost formula — replaced with per-call accounting

**The flaw, confirmed real**: in a multi-turn agent conversation, static
context (task bundle + regime prompt) is typically present in every
subsequent model call, not billed once. Subtracting it once from a
combined total (the original `execution_phase_cost` formula) does not
isolate autonomous reasoning efficiency — a longer regime prompt inflates
cost on every turn, not on turn one only, and the old formula only ever
removed turn one's worth.

**Fix — per-model-call telemetry, two honestly-named views**:

- New telemetry: `model_calls[]`, one entry per model call —
  `{call_index, input_tokens, cached_input_tokens (if the provider reports
  it), output_tokens, model_id}`.
- **Operational actual cost**: sum of what was genuinely billed across all
  calls (using cached-token pricing where the provider reports and prices
  it distinctly). This is a real, auditable dollar figure — "what would
  deploying this regime actually cost."
- **Dynamic-execution resource cost**: for each call, subtract the fixed
  static-prefix token count (`input_tokens_task_bundle +
  input_tokens_regime_prompt`, or the reported cached-prefix count if the
  provider distinguishes it) from that call's input tokens, floored at
  zero, then cost the remainder at the same rate card. Summed across all
  calls. This is a **normalized analysis metric**, not an invoice figure —
  it exists specifically to isolate whether LEAN's autonomous behavior
  itself became cheaper, independent of how many turns repeated the prompt
  or how long the prompt was.

The old `execution_phase_cost_usd` (single-subtraction) field is retired
and replaced by `dynamic_execution_resource_cost_usd`, computed from
`model_calls[]` rather than from the two aggregate token counts alone.
Tool-call counts, subprocess runtime, and wall-clock remain independent,
directly-observed behavioral-cost measures, unaffected by this fix and
already immune to the flaw (they were never derived from token
subtraction).

---

## 5. Human minutes / USD mixing — separated, sensitivity analysis added

**The conflict, confirmed real**: `operational_total_cost_usd` folded human
supervision minutes into a dollar figure using a "frozen rate card,"
directly contradicting the design's own earlier commitments (human minutes
stay separate; no single assumed hourly rate; break-even analysis derives
the rate rather than assuming it).

**Fix**: `operational_total_cost_usd` (and its renamed sibling from §4,
`operational_actual_cost_usd`) now include **only** model/API dollar cost —
human supervision minutes are removed from it entirely. Primary economics
is reported as the three-dimensional vector already specified elsewhere in
the protocol and now enforced consistently: model/API dollars, wall-clock
seconds, active human minutes, never combined by default. A new, explicitly
labeled **sensitivity-analysis** derived metric,
`total_cost_at_rate[]` = `{rate_usd_per_human_hour, total_cost_usd}` for a
small preregistered set of rate points (e.g., $0, $50, $150, $400/hour), is
computed post-hoc for illustration only — never a primary metric, never
feeding H1-H5 or the Tranche-2 decision rule.

---

## 6. H1 deterministic decidability — fixed, and the HARNESS_UNSTABLE
conflation resolved

**The conflict, confirmed real**: the severity rubric called a
`HARNESS_UNSTABLE`-classified failure a "MINOR efficacy regression," but
`HARNESS_UNSTABLE` means `INSTRUMENT_VALIDITY != VALID`, which the protocol
elsewhere says must be excluded/replaced, never scored as an efficacy
outcome at all. A run cannot simultaneously be instrument-invalid (no
efficacy judgment possible) and a valid (if minor) efficacy data point.

**Fix — complete separation, then a deterministic H1 rule**:
- `INSTRUMENT_VALIDITY != VALID` (including `HARNESS_UNSTABLE`) → **no
  efficacy judgment of any kind**; the run is excluded and replaced via
  technical rerun (already-existing rule), full stop. The word "MINOR" is
  removed from this case entirely — it is not a minor efficacy regression,
  it is not an efficacy data point.
- Severity classification (`SEVERE` / — no `MINOR` tier remains, since the
  only case that previously used `MINOR` was actually instrument-invalid)
  now applies only to genuine, `INSTRUMENT_VALIDITY = VALID` pairs where
  ROBUST is `ACCEPTED` and LEAN is `NOT_ACHIEVED` or
  `PROCESS_CONTRACT = VIOLATED` for a real (non-harness) reason.
- **H1 exact, deterministic rule**: H1 HOLDS unless at least one valid
  (`INSTRUMENT_VALIDITY = VALID`) task instance shows this exact pattern —
  ROBUST `ACCEPTED`, LEAN not accepted, where LEAN's failure traces to a
  hidden-invariant or oracle violation (not an instrument-invalidity
  exclusion, which is a separate, prior gate). Any single such occurrence
  means H1 FAILS. This is deliberately conservative, matching the
  reviewer's own suggested default, and is now fully mechanical — the
  Tranche-2 state machine's "H1 holds" branch reads this rule directly, not
  an evaluator's qualitative sense of "approximately equal."

---

## 7. Preflight — dispatch mode added, hidden-sibling fix applied

**The gap, confirmed real**: `run-state-dir-is-fresh`, `oracle-self-test`,
and `task-bundle-excludes-evaluator-artifacts` were unconditionally
`UNVERIFIABLE`, and `UNVERIFIABLE` results block a zero exit — meaning the
script as written could never return 0 for a real dispatch invocation, no
matter what was supplied to it. That contradicts its own stated purpose as
"the gate before any pilot or main-study run."

**Fix — concrete dispatch-mode arguments added**: `--run-state-dir <path>`,
`--task-bundle <path>`, `--task-bundle-sha256 <hash>`,
`--oracle-self-test-command <cmd>`, `--expected-oracle-self-test-sha
<hash>`. When supplied, each check now performs a real, gradeable test
(directory freshness = empty or absent; task bundle hash match; oracle
self-test command executed and its output hash compared) and can return
PASS or FAIL. When omitted — i.e., a design-time invocation with nothing
yet to check — the script still reports `UNVERIFIABLE` for whichever checks
lack their argument, preserving the fail-closed default for exactly the
case (no oracle exists yet) where that default is honest. A real dispatch
invocation that supplies all five new arguments can now mechanically reach
exit 0.

**Hidden-sibling fix**: `clone-parent-directory-is-uncrowded` used `ls -1`,
which does not list dotfile entries, so a hidden sibling directory could
sit next to the clone undetected. Changed to enumerate all entries
including dotfiles (excluding the synthetic `.` and `..` self-references),
closing that evasion.

---

## 8. Pilot outcome state machine — reconciled with the frozen fallback,
renamed for clarity

**The inconsistency, confirmed real**: `AUTONOMOUS-TASK-V2-PILOT-PLAN.md`'s
`EXPERIMENT_NOT_ADMISSIBLE` outcome still described a stale "2 families x 2
levels x 3 regimes = 12 runs" narrowing, written before Hardening Pass 1
froze the actual fallback (T1+T2 x 3 instances x 3 regimes = 18 runs). The
outcome name `EXPERIMENT_NOT_ADMISSIBLE` was also being used for a
family-level (not whole-experiment-level) failure, which is confusing
given the same name is reserved elsewhere for a genuinely inadmissible
whole experiment.

**Fix — outcome states renamed and corrected**, adopted per the reviewer's
own proposal:
```
PILOT_INSTRUMENT_VALID
  -- all families' pilot cells pass; proceed to selection-driven
     materialization (T1/T2 mechanical instantiation from frozen texts;
     T3 mechanical instantiation from its frozen spec, since its pilot
     passed) and lock.

PILOT_INSTRUMENT_VALID_WITH_FAMILY_DROPPED
  family = T3
  fallback matrix = frozen T1/T2 expansion (18 runs total, per §1C above)
  -- corrected from the stale 12-run figure.

CHANGES_REQUIRED_BEFORE_MAIN_LOCK
  -- a plausibly-fixable instrument defect found; repair via addendum,
     re-run only the affected cell(s).

EXPERIMENT_NOT_ADMISSIBLE
  -- reserved for the case where the REMAINING design (after any family
     drop) cannot support the research question at all -- never used for
     a single family's pilot failure when the fallback covers it.
```

---

## 9. Pilot no longer forces an R2 escalation

**The gap, confirmed real**: requiring the T1 pilot cell's R2 run to
produce "at least one well-formed escalation request/response" would
reward an agent for escalating even absent genuine uncertainty — exactly
the behavior H3 exists to measure honestly, contaminated at the instrument
level.

**Fix**: the pilot's R2 requirement is now conditional: *if* spontaneous
escalation occurs during the pilot's R2 run, the request/response mechanism
must work correctly (four-element format, narrow non-leaking response,
verbatim logging). *If no escalation occurs*, the escalation channel itself
is validated separately via a non-evidentiary handshake/calibration
exercise (a synthetic request-response round trip exercised outside the
scored pilot task, confirming the mechanism functions) rather than treating
the pilot's absence of escalation as an instrument failure. The behavioral
pilot is never required to manufacture escalation to pass.

---

## T3 interrupt mechanism — corrected (this pass found a real, additional
gap beyond what the reviewer flagged)

Re-inspecting `scripts/workflow-runtime.py` at the frozen SHA to answer the
reviewer's item 10 turned up something the prior passes had missed: the
actual **resume** capability (`resume: bool` constructor flag,
`_find_resume_state()`) parses the **markdown run log**
(`run_log_<workflow_id>_<mode>.md`, looking for `### Step N ... **status**:
X` blocks and a `PAUSED` marker) — a **different file** from the
`run-ledger.jsonl` the earlier passes verified as append-only and
audit-checkable. Confirmed by reading `write_run_log()`'s call site: it is
invoked once, after the step-execution loop breaks or ends — meaning a hard
process kill mid-step (the interrupt method assumed since the first
Hardening Pass) would leave **no run-log file at all** for
`_find_resume_state()` to parse, so "resume" as actually implemented would
not engage for that interrupt method. This is exactly the "ledger audit
substrate vs. recovery substrate are not the same thing" distinction the
reviewer named in item 10, now traced to its root cause.

**Corrected interrupt mechanism**: use a `gate: review` step (a real,
already-used repository feature — e.g., visible in
`architecture-implementation-workflow`'s own step definitions) in
`guided_execution` mode, and do not approve the gate. This is a genuinely
realistic operation (a workflow legitimately pausing for pending human
review), not a synthetic kill signal, and it produces exactly the
resumable state `_find_resume_state()` is built to read: prior steps'
status entries plus a `PAUSED` marker at the gate. **Recovery** = a second
invocation of `workflow-runtime.py` with `resume=True` (confirmed:
`resume_skip = set(resume_state.get("completed_steps", []))` is computed
and used to skip already-completed steps, not merely reported) against the
same session directory — a real, working, code-verified skip mechanism, not
an assumption. **Replay/idempotency** = invoking that same resume procedure
a second time after the agent claims completion, expecting zero additional
mutation, checked against `run-ledger.jsonl` via the existing
`handle_audit_run` command (the ledger and its audit command remain useful
as the independent verification layer — they were never wrong, just
insufficient on their own to establish recovery, exactly as the reviewer
said).

`AUTONOMOUS-TASK-V2-PILOT-PLAN.md` §T3 and
`AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md` §T3 are updated to specify this
mechanism precisely rather than the earlier "kill after N ledger entries"
sketch, which is now known, with evidence, not to engage the real resume
path.

---

## 10. T2 vs. D/D' distinctness — closed using reviewer-supplied provenance

The reviewer supplied the missing external fact directly: D/D' transformed
a `repository_sensemaking_brief` artifact while preserving an exact
Evidence region and obtaining validator acceptance; this T2 construct works
on the artifact-*contract declaration* surface
(`artifact-contracts.yaml`) and producer/consumer field agreement. Recorded
as external-provenance verification, not left open: the two are related by
the broad "constrained transformation" idea but are materially different
task instances and semantic substrates. `AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md`
and `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md`'s open-items lists are updated
to mark this closed rather than unresolved.

---

## 11. Smaller consistency issues — all six addressed

1. `responder_blinded` field added to `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md`
   (was required by the scorecard but absent from the schema).
2. `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §0's stale "pending re-verification"
   wording corrected to reflect that Hardening Pass 1 already completed it.
3. Hardening Pass 1's "3 points of complexity" phrasing corrected: the
   fallback triple is two complexity *levels* (MEDIUM, HIGH) with one
   additional HIGH-shaped replication (HIGH Rank 2), not three distinct
   complexity points — matches the explicit rank mapping in §1C above.
4. Reserve-vs-rerun distinction — see §1C above.
5. Randomized dispatch ordering: a frozen procedure is now specified —
   `dispatch_order = seeded_fisher_yates(seed_3, the 18 (task, regime)
   pairs)`, where `seed_3` is generated by the same commit-then-independent-
   salt pattern as §1A/1B (frozen and logged before dispatch, not chosen ad
   hoc).
6. Pilot isolation-breach softness: the "or breaches were individually
   explained and are not systemic" escape clause is removed from
   `PILOT_INSTRUMENT_VALID`'s pass condition. A pilot cell with an
   `ISOLATION_BREACH`-flagged run is excluded and must be replaced via
   technical rerun (same rule as any other `INSTRUMENT_VALIDITY != VALID`
   run) before that cell counts toward a clean pilot — no case-by-case
   explaining-away.

---

## Status

All nine of the reviewer's specified lock-bar checks, all four blocker
issues, both non-blocker follow-ups actually required by them (T2/D-D'
closed, T3 interrupt mechanism corrected with new evidence), and all six
smaller consistency items are addressed as targeted, mechanical changes —
no task family, hypothesis, or sample-size decision was reopened beyond
what these fixes required (the Tranche-2 pool doubling from 18 to 36 total
candidates is the one place scope grew, and it grew only to close a named
loophole, not to expand the study). Final lock authorization remains
reserved for the reviewer's own re-inspection of the corrected bundle.
