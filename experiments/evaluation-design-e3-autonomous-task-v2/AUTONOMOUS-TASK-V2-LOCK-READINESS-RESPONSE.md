# Autonomous Task v2 — Lock-Readiness Response

Status: DRAFT. Narrow response to the human reviewer's provisional verdict
("close to READY FOR PILOT LOCK, but not until the post-pilot task-selection
issue is explicitly closed") and its four numbered issues plus five
non-blocker items. No pilot run, no lock, no hash, no dispatch, no main-study
task instantiated. This pass changed protocol text and preflight tooling
only, per the reviewer's own instruction not to reopen broad design.

---

## Issue 1 (blocker): post-pilot task-selection bias — CLOSED

**The gap, restated precisely**: as drafted, the six main-study task
instances would have been authored *after* the 9-run pilot, by whoever
constructs them, who would by then have seen how ROBUST/LEAN/ESCALATION
behaved on the pilot's three disposable tasks. Even with good faith, that
creates an unconscious selection channel — "this admissible candidate feels
less representative" is exactly the kind of judgment call that can silently
tilt the main study toward a flattering result.

**Resolution: frozen candidate pool + deterministic selection**, adopted as
the "preferred" option the reviewer named. Mechanism:

1. **Before pilot dispatch**, the task constructor enumerates, for each
   (family, complexity level) cell — 6 cells total (T1/T2/T3 x MEDIUM/HIGH)
   — a pool of at least **3 admissible candidate task instances**, not just
   one. Each candidate is fully drafted (its complete task-visible contract
   text) and admissibility-checked against the Task Construction rubric
   only — never against any regime's behavior, since no regime will have
   been run against any of these candidates yet at this point in the
   sequence. Pool size of 3 per cell (18 candidates total) is chosen
   specifically to cover the normal 2-per-family draw *and* the family-
   fallback 3rd-instance draw (Hardening Pass 1 §4) without ever requiring
   fresh, post-hoc authoring of a "just in time" instance.
2. Each candidate is recorded in a manifest as `(candidate_id, family,
   level, sha256(full task-visible contract text))`. The manifest itself is
   then hashed as a whole. This manifest and its hash are frozen **before**
   the pilot's 9 runs execute — they become part of the pilot-lock record,
   not the post-pilot construction step.
3. A **deterministic selection function** picks which candidates actually
   become the held-out main-study instances: `seed =
   sha256(frozen_sha || "autonomous-task-v2-main-selection")`. Within each
   (family, level) cell, candidates are ranked by `sha256(seed ||
   candidate_id)` ascending. Rank 1 is the primary main-study instance for
   that cell. Rank 2 is used only if the family-fallback rule (Hardening
   Pass 1 §4) requires a 3rd instance for that family (T3 pilot-gate
   failure). Rank 3 is a reserve, invoked only if a selected candidate is
   later found `INSTRUMENT_VALIDITY != VALID` during actual main-study
   execution — a narrow, evidence-triggered contingency, never a
   "we didn't like this outcome" redo.
4. Because the seed is a deterministic function of the frozen SHA and a
   fixed salt string (not of anything pilot-related), the selection ranking
   for a given pool is fully determined the moment the pool is frozen —
   before pilot results exist to bias it, and reproducible by anyone who
   has the pool manifest and the seed formula.
5. Pool candidates remain fully distinct from the 3 disposable pilot tasks
   (Task Construction's existing rule against promoting pilot instances to
   main-study status is unaffected and still applies).

This closes the gap the reviewer identified precisely: by the time pilot
results are known, the exact text of the main-study tasks is already fixed
and hashed. No human or agent choice happens after seeing treatment
behavior. Applied to `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` (new §"Candidate
pool and selection procedure," inserted before the pilot in the sequential
design) and `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md` (pool-freeze
procedure added under "Pilot vs. main-study instance rules").

---

## Issue 2: T1 construct label — resolved, relabeled honestly

Attacked with the reviewer's own four questions, against the actual verified
substrate (dual-consumer `workflow-registry.yaml` divergence):

- **What are the two executable/operational routes?** Not two executables —
  two identically-named *data files*, each read by a different consumer
  (`scripts/_validator_utils.py`/`scripts/workflow-planner.py` vs.
  `src/sensemaking_skills/registry.py:WorkflowRegistry`).
- **What semantic outcome differs?** Which consumer's runtime behavior
  reflects the edit.
- **Could an agent succeed merely by choosing the right file?** Yes —
  literally the entire task, once the intended consumer is stated, reduces
  to "edit the file that consumer actually reads." There is no tool/command
  invocation ambiguity left in the surviving construct at all (the one
  candidate that WAS about invocation mechanism — Skill-tool vs. CLI — was
  already dropped in Hardening Pass 1 for not being a genuine ambiguity).
- **Tool routing or resource-location reasoning?** Resource-location
  reasoning, honestly. The construct measures whether an agent can
  determine, from reading consumer-side code, which of several duplicated
  resources backs a given consumer's behavior — not whether it can choose
  among different executable mechanisms to accomplish a goal.

**Resolution**: the T1 family is relabeled from "Semantic Tool Routing" to
**"Semantic Mechanism Routing,"** per the reviewer's proposed broader
category, with an explicit operational note that the specific verified
substrate is a *resource/consumer-routing* case within that broader
construct (choosing among duplicated config resources based on which
consumer reads which) rather than a *command/API-routing* case. The T1
identifier, matrix slot, and all admissibility findings are unchanged — this
is a label-and-definition correction, not a substrate change, applied
consistently across `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md`,
`AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md`, and
`AUTONOMOUS-TASK-V2-PILOT-PLAN.md`.

---

## Issue 3: isolation-breach normative rule + Git metadata — resolved

**Normative rule added** (not just preflight) to
`AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §14 (Stop/invalidity rules), using
language very close to the reviewer's own: any agent tool access that
reaches outside the approved task root / approved runtime-tool locations /
an explicit allowlist, into another repository or experiment location, is an
`ISOLATION_BREACH`. Such a run is retained for harness telemetry but
excluded from efficacy and economic inference — consistent with, and now
explicit about, how `INSTRUMENT_VALIDITY != VALID` runs are already handled
elsewhere in the protocol.

**Multi-channel coverage requirement added**: the rule explicitly states the
evidence trail must cover every tool-access channel the harness exposes to
the agent (shell/Bash, file-read tools, search tools, language-specific
filesystem APIs), not shell commands alone. Where a specific channel cannot
be observed or logged, that is recorded as a **named, additional technical
limitation** (distinct from, and stacked on top of, the existing
`AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED` disclosure) rather than silently
assumed covered.

**Git-metadata preflight checks added**, both name-agnostic and both
smoke-tested:
- `clone-no-alternate-object-store`: fails if
  `$CLONE_DIR/.git/objects/info/alternates` (or the equivalent path for a
  non-standard `.git` layout) exists at all — a clone made with
  `--shared`/`--reference` depends on and can leak the path to its source
  repository's object store, and was not previously checked.
- `clone-common-dir-is-self`: fails unless `git -C $CLONE_DIR rev-parse
  --git-common-dir` resolves to the clone's own `.git` directory. This is a
  strictly more general replacement for the earlier
  `clone-is-standalone-not-worktree` heuristic (which only checked whether
  `.git` was a file vs. a directory) — it catches linked worktrees, external
  `commondir` files, and any other mechanism that would point the clone's
  git metadata back at a shared location, by construction rather than by
  enumerating known cases.

Both were added to `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` and smoke-tested
against a clean standalone clone (passes both) and a linked worktree (fails
`clone-common-dir-is-self`, as the original Hardening-Pass-1 calibration
worktree would have).

---

## Issue 4: dual cost views — resolved, made co-equal top-line metrics

Previously, regime-prompt-token separation existed only as a robustness
*check* on H2, secondary to a single combined cost figure. The reviewer is
right that this understates the risk: LEAN's prompt is genuinely shorter
than ROBUST's (confirmed in the regime-separation diff, Hardening Pass 1
§7), so a naive combined number could show "LEAN cheaper" for a reason that
has nothing to do with autonomous reasoning efficiency.

**Resolution**: two cost views are now both **required, co-equal, always-
reported** top-line metrics for every run and every derived comparison —
neither is primary, neither is a secondary robustness check:

- **Operational total cost**: everything (`task_bundle` tokens + `regime_
  prompt` tokens + all subsequent model/tool/subprocess cost + logged human
  supervision minutes converted at the frozen rate card). Answers "what
  would this regime actually cost to deploy."
- **Execution-phase cost**: operational total cost minus the fixed,
  regime-determined initialization cost (`task_bundle` tokens + `regime_
  prompt` tokens), i.e., only the cost incurred *after* the agent has
  received its full instructions and begun acting. Answers "did LEAN's
  autonomous behavior actually become more efficient," independent of
  prompt length.

H2 is now stated as requiring **both** views to be reported for every
paired comparison; a result where only the operational-total view drops is
explicitly labeled a real but different finding ("operational saving,
prompt-driven") from a result where the execution-phase view also drops
("reasoning-efficiency improvement"). Neither is silently treated as
sufficient on its own to claim `EFFICIENCY_IMPROVED` in the reasoning-
efficiency sense; the protocol draft, telemetry schema, and evaluator
scorecard were all updated to carry both fields through consistently.

---

## Non-blocker items — all five addressed

1. **Paired-failure interpretation, preregistered exactly** (not "approximately
   equal success"): a `ROBUST accepted / LEAN not accepted` pair is defined
   as a **paired efficacy regression**, and regressions are weighted by
   violation severity — a hidden-invariant/oracle violation counts as a
   `SEVERE` regression that blocks an uncomplicated `EFFICIENCY_IMPROVED`
   conclusion pending explicit examination in the report; a recoverable
   `HARNESS_UNSTABLE`-classified timeout counts as `MINOR` and does not by
   itself block that conclusion. Added to protocol draft §8 (H1) and the
   scorecard.
2. **Aggregate and paired cost metrics kept co-equal, neither replacing the
   other**: `cost_per_accepted_task` (aggregate, failures in the numerator)
   and a new `paired_cost_delta_matched_outcomes` (task-by-task ROBUST-vs-
   LEAN cost comparison restricted to pairs where both were `ACCEPTED`) are
   both required outputs. The reviewer's own example (LEAN 4/6 accepted with
   a deceptively low median on its easy successes) is recorded verbatim as
   the reason neither metric may substitute for the other.
3. **Waste labeling made regime-blind where feasible**: the scorecard's
   waste-tagging step now instructs the evaluator to review the evidence
   object (tool-call trace + the existing "why info was already established
   / whether a later action depended on it" justification format) with the
   regime label withheld during the judgment call itself, re-attached only
   after the tag is recorded. Where blinding isn't practical (e.g., regime
   text is visible in the transcript itself), that limitation is logged
   explicitly rather than assumed away — matching how the reviewer's own
   `route_evidence_trace` idea was applied.
4. **R2 responder blindness, made a first-class requirement**: the
   escalation responder must receive only the visible task contract,
   permitted environment facts, and the agent's request — never the hidden
   oracle or intended solution route. If full blindness isn't achievable in
   a given run (e.g., one person plays both roles for logistical reasons),
   that is logged as an explicit, named limitation on that run, and the full
   verbatim exchange is preserved regardless (already required).
5. **Stochasticity, preregistered explicitly** rather than left implicit:
   task is the paired block; model/settings identical across regimes within
   a task; a valid-but-surprising run is never rerun; only
   instrument-invalid runs receive technical replacement (per the existing
   `INSTRUMENT_VALIDITY` rule); conclusions remain descriptive/paired, never
   inferential-statistical, at n=6. Tranche 2 improves precision across new
   tasks but is explicitly noted as NOT estimating within-cell stochastic
   variance — that limitation is named, not solved.

---

## T3 — final attack, causal chain made explicit

The pilot's T3 requirement is tightened from "prove a partial-run state
exists and is checkable" to requiring the full **seven-link causal chain**
the reviewer specified, verbatim, as the pilot's pass condition:

```
real repository operation begins
-> deterministic interruption leaves meaningful partial state
-> some work is already correct
-> recovery can preserve that work
-> restart/delete/recreate is detectably different from genuine recovery
-> agent can reach a valid final state
-> replay remains idempotent
```

`AUTONOMOUS-TASK-V2-PILOT-PLAN.md` §T3 now states this chain explicitly as
the pass bar, and repeats the reviewer's own instruction verbatim: if
producing this chain requires inventing a partial state no real operation
could produce, **T3 fails construct admissibility and must not be rescued**
— the frozen family-fallback rule (Hardening Pass 1 §4) exists precisely so
this can happen without forcing the construct.

---

## Tranche 2 — stop-outcomes frozen alongside continuation outcomes

The activation rule (Hardening Pass 1 §5) is extended with an explicit,
mutually exclusive outcome table, so "stop" is as fully specified as
"continue":

```
CLEARLY NEGLIGIBLE (paired median cost reduction < 10%, H1 holding)
  -> stop; report negative/negligible

CLEARLY MEANINGFUL + efficacy preserved (> 25%, H1 holding)
  -> stop; report EFFICIENCY_IMPROVED

CLEAR EFFICACY REGRESSION (H1 failing, any cost effect size)
  -> stop; report the efficacy failure

INSTRUMENT INVALID (>=2 of 18 runs non-VALID)
  -> repair/re-pilot the affected cell(s), NOT Tranche 2

MATERIALLY AMBIGUOUS VALID RESULT (10-25% band, or inconsistent sign across
cost dimensions, WITH H1 holding and no gaming tag)
  -> Tranche 2 eligible
```

This is the same rule already frozen in Hardening Pass 1 §5, now stated as a
complete partition (every possible Tranche-1 outcome maps to exactly one
row) rather than only specifying the activation condition and leaving stop
conditions implicit.

---

## Artifacts touched in this pass

- `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md`: candidate-pool/selection
  procedure (new section, sequential design updated), T1 relabel,
  `ISOLATION_BREACH` normative rule, dual cost views, paired-failure
  severity weighting, stochasticity clause, Tranche-2 outcome table.
- `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md`: pool-freeze procedure, T1
  relabel.
- `AUTONOMOUS-TASK-V2-PILOT-PLAN.md`: T3 seven-link causal-chain pass bar,
  T1 relabel.
- `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md`: dual cost view fields,
  `paired_cost_delta_matched_outcomes` field.
- `AUTONOMOUS-TASK-V2-EVALUATOR-SCORECARD.md`: paired-failure severity
  rubric, regime-blind waste-tagging instruction, R2 responder-blindness
  requirement.
- `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`: two new git-metadata checks
  (`clone-no-alternate-object-store`, `clone-common-dir-is-self`, the
  latter superseding the older, narrower worktree-pointer-file heuristic).
- `AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md`: status pointer updated.

No task family, hypothesis identity, or sample size changed. No document was
silently overwritten — this file exists precisely so the resolution of each
issue is traceable to the reviewer's own numbering.

## Status

All four blocker-level issues and all five non-blocker items from the
review are addressed as narrow, mechanical changes — no broad redesign was
performed, consistent with the reviewer's own instruction. Design status
remains **READY FOR PILOT LOCK-CANDIDATE REVIEW** — this pass does not
elevate its own status to "locked": that determination is explicitly
reserved for the human reviewer's line-by-line pass against the uploaded
artifact bundle, per their own stated process.
