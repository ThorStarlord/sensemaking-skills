# Autonomous Task v2 — Protocol Draft (Operational Value)

Status: DRAFT — normative draft, NOT locked. No hash has been taken. No pilot
or main-study task instance has been dispatched, run, or constructed from
this document beyond the disposable-pilot *shapes* in
`AUTONOMOUS-TASK-V2-PILOT-PLAN.md`.

## 0. Provenance and scope note

The frozen repository under study is `ThorStarlord/sensemaking-skills` at
`0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`. That commit exists in this
repository's history (verified: it is an ancestor of the current `main` tip,
`1458f92`). It is **not** the current tip — `main` has moved ~85 commits past
it toward `origin/main` as of this design pass. Any executable run against
the frozen SHA must therefore use a standalone clone/worktree checked out
exactly at that commit, not the working tree this design task ran in (see
`AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` §clean-clone check).

**Hardening Pass 1 note**: §3 below was re-verified against a detached git
worktree checked out at exactly this SHA (not the 85-commits-ahead working
tree used in the initial design pass). Findings that changed as a result are
marked "frozen-SHA-verified" and are detailed in full in
`AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md`; this section reflects the
corrected conclusions, not the initial pass's.

**Ambient-isolation audit note**: `AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md`
subsequently performed a metadata-only inventory of this repository's
pre-existing sibling git worktrees (several already based on this same
frozen SHA under other experiment names) and found two concrete ambient-
exposure vectors, now caught by `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`. This
did not change any task family, hypothesis, or sample-size decision in this
document — it hardened the preflight tooling that gates dispatch, which is
a distinct concern from the admissibility questions this section answers.

The Autonomous Task v0.1/v1/v2.1 experiment history, the M1-M4 lessons, and
the banked-but-unexecuted Semantic Tool Routing construct are supplied to
this design task as **external research provenance** — prior benchmark
records that live outside this repository. This repository was independently
searched for matching artifacts (no `AUTONOMOUS-TASK*`, no matching failure-
mode identifiers, no matching construct names were found anywhere in tracked
or untracked files as of this pass) and that absence is treated as expected,
not as evidence against the supplied provenance, per instruction. The M1-M4
lessons are used below as binding design constraints regardless.

This repository's actual documented purpose — a fog-classification and
workflow-routing meta-layer for AI agents, per `CONTEXT.md` — is used
throughout as the **experimental substrate**: task families are grounded in
real mechanisms this repository already has (see §3), not invented to
resemble a benchmark harness.

## 1. Research question

> Can autonomous execution reduce human-attention cost while maintaining
> externally verified task quality, and can its efficiency be systematically
> improved without sacrificing efficacy?

Three separable claims, each gets its own evidence, none is assumed by
answering another:

| Claim | Question |
|---|---|
| Efficacy | Can the agent reliably produce accepted task outcomes? |
| Improvability | Can a leaner autonomy protocol lower cost without lowering reliability? |
| Cost-benefit | Does autonomy become preferable to competent human execution for some task classes? |

A negative or null result on any claim is a valid, complete scientific
outcome. This protocol does not treat "autonomy loses" as a failure of the
experiment.

## 2. Scope boundary (frozen for this design pass)

This design task does **not**:
- dispatch a benchmark agent, run a pilot, or run a main-study task;
- lock or hash a final protocol;
- select a repository other than `sensemaking-skills`;
- modify production source code;
- construct the six final held-out main-study task instances;
- claim autonomy is or is not cost-effective;
- claim protocol optimization will necessarily improve economics.

It produces draft artifacts and one design-readiness recommendation
(§ "Final status" in `AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md`).

## 3. Task families

Grounding was done by inspecting the actual repository at the current tip
(a superset of the frozen SHA's surfaces, since `main` has only added
material since `0ffb564b`) rather than assuming a construct in the abstract.
**Frozen-SHA re-verification is complete, not pending**: Hardening Pass 1
re-checked every finding below against a detached, clean worktree at exactly
`0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5` (confirmed HEAD match, confirmed
zero dirty entries) — see `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §1-§3 for
the verification evidence. What remains open, per Lock-Readiness Response 2,
is not re-verification but full task-instance materialization, which is
gated on the pilot for T3 specifically (§3b below).

### T1 — Semantic Mechanism Routing (relabeled in the Lock-Readiness
Response — see `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md` §Issue 2)

Originally named "Semantic Tool Routing." A human reviewer correctly pointed
out that the surviving substrate below is not tool-invocation ambiguity (no
candidate involving a choice between executable mechanisms survived
Hardening Pass 1) but resource/consumer-routing: choosing which of two
identically-named, duplicated config *files* backs a given consumer's
behavior. This is a real case of the broader construct — an agent must
determine, from semantic understanding of consumer-side code, which
*mechanism* (here: which duplicated resource) governs a stated outcome — so
the family is relabeled "Semantic Mechanism Routing" rather than dropped or
renamed to something narrower. The T1 identifier and all admissibility
findings below are unchanged.

**Frozen-SHA-verified substrate (Hardening Pass 1 corrected this section —
see `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §1 for the full evidence
trail):**

`workflow-registry.yaml` exists in exactly two locations at the frozen SHA —
`skills/workflow-planner/references/workflow-registry.yaml` and
`src/sensemaking_skills/defaults/workflow-registry.yaml` — and the two
copies have **already diverged**: the `skills/` copy contains a workflow
(`architecture-implementation-workflow`) the `src/defaults/` copy lacks.
Tracing the actual loading code (not just file location) shows the two
copies serve two different, real consumers: `scripts/_validator_utils.py`
and `scripts/workflow-planner.py` hardcode the `skills/` path (the local
"dogfood" CLI path, operating on this repository directly), while
`src/sensemaking_skills/registry.py`'s `WorkflowRegistry` class loads the
`src/defaults/` copy as package defaults, merged with a target repository's
own overrides, when `sensemaking_skills` is used as an installed library
against an *external* repository. Both files share the identical name
`workflow-registry.yaml`, so naming gives no signal about which is
authoritative for a given task's stated intent; a task naming its intended
consumer explicitly (local-dogfood vs. installed-package-default) has a
genuine right answer the oracle can check by exercising that consumer, and a
wrong-route edit fails semantically (the stated consumer's behavior doesn't
change) rather than cosmetically. This mechanism is discoverable only by
reading the two Python modules that load each file — it is undocumented in
`API.md`/`CONTEXT.md`/`docs/` — which is a real but modest caveat, not a
blocker.

Two candidates considered in the initial design pass were dropped after
re-verification:
- `skill-registry.yaml` has exactly **one** copy at the frozen SHA (not
  duplicated) — not a viable trap.
- The proposed "Skill-tool vs. `workflow-runtime.py` CLI" dual-invocation
  ambiguity does not qualify: `CONTEXT.md` (ADR 0013 section) states these
  two invocation surfaces are explicitly *designed* to be equivalent
  ("Skills are platform-agnostic... Same skill works whether called by agent
  (Skill tool) or CLI"), so there is no genuine wrong answer for an oracle to
  detect. A task built on this distinction would violate the "wrong route
  must be genuinely plausible" requirement, not merely be redundant.
- The `build/lib/...` third/fourth copy cited in the initial pass does not
  exist at the frozen SHA at all — it is a later, untracked build artifact
  only present in the current (85-commits-ahead) working tree.

**Admissibility: `T1_ADMISSIBLE`**, confirmed against a clean, detached
worktree checked out exactly at `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`
(not inferred from the newer working tree).

### T2 — Constrained State Transformation

**Grounded substrate:** `skills/workflow-planner/references/artifact-contracts.yaml`
declares, per artifact, `required_sections`, `required_machine_fields`, and a
`verification` block (generic + specialized validators). `CLAUDE.md`'s own
"Verification discipline" section states this file is binding contract text,
not documentation, and that `tests/test_field_contract_agreement.py`
mechanically enforces producer/consumer field-name agreement. This gives a
real, pre-existing hard-invariant surface: add or amend a declared field/
artifact block while (a) preserving every other declaration byte-for-byte,
(b) keeping the file parseable, (c) passing the contract-agreement test,
(d) not touching unrelated skills' consumed_by lists. Multiple valid
implementations exist because YAML insertion point, comment style, and key
ordering within a block are not themselves constrained — only the declared
shape is.

**Admissibility: ADMISSIBLE.** This is a real, currently-enforced contract
surface, not a synthetic one built for the benchmark.

### T3 — Operational Recovery / Idempotency

**Grounded substrate, mechanism corrected twice — see
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §1 for the full evidence
trail; the interrupt/recovery mechanism described here is the version
directly verified to work against the frozen SHA's actual code, not either
of the two earlier candidates (hard process kill; unapproved `gate: review`
pause), both of which are withdrawn.**

`artifacts/<NN>-orchestration-run/` directories hold a per-run artifact set
plus an append-only JSONL run ledger (`run-ledger.jsonl`). Separately,
`scripts/workflow-runtime.py` has a genuine, code-verified resume capability
(`resume=True`, `_find_resume_state()`) that parses the markdown run log
(`run_log_<workflow_id>_<mode>.md`) for per-step status. Tracing this code
directly: a step whose status is `PAUSED` (which covers both a gate left
unapproved AND an explicit gate denial — both set `status = "PAUSED"`) is
unconditionally folded into `resume_skip` and silently treated as
already-completed on resume — **a `gate: review` interrupt mechanism
bypasses the approval boundary rather than testing recovery from it, and is
not used.** A step whose status is `FAILED` (set on a genuine validator
failure, or a distinct `gate_result == "failed"` auto-fail — neither is
folded into `resume_skip`) is, by contrast, absent from both
`completed_steps` and the paused-step handling, so `--resume` calls
`execute_step()` on it again fresh: a real, legitimate retry, not a skip.

**Interrupt mechanism**: a task-constructed step's validator fails on first
attempt for a realistic, constructible reason within that validator's own
actual purpose (never an artificial crash). **Recovery**: fix the
underlying condition, re-invoke `workflow-runtime.py --resume` against the
same session directory — prior successfully-validated steps are preserved
and skipped (`completed_steps`), the failed step is legitimately retried
and this time succeeds. **Idempotency oracle**: zero new step/artifact/
validation ledger events on a second post-completion `--resume` invocation;
`run_started`/`run_completed`-class bookkeeping events are explicitly
exempted from this requirement (confirmed: every invocation logs these
regardless of whether any step executes, so literal zero-new-ledger-entry
replay is impossible and is not what is required).

**Admissibility: `T3_CONDITIONALLY_ADMISSIBLE` — medium-high confidence,
still the highest construction risk of the three families**, but now
resting on a mechanism directly confirmed to execute the intended
legitimate-retry code path, not merely one that looked structurally
plausible. What remains unproven: no live validator-failure-and-resume
cycle has actually been executed end to end. The disposable T3 pilot task's
primary purpose remains to prove this construction is reproducible before
either T3 held-out instance is built — see
`AUTONOMOUS-TASK-V2-PILOT-PLAN.md` §T3. See
`AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §4 for the frozen family-fallback
rule if this pilot gate fails.

## 3b. Candidate pool and deterministic selection (closes post-pilot
task-selection bias — see `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md`
§Issue 1 and `AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-2.md` §1, §2 for
the two gaps a human reviewer found in the first version of this section and
their fixes)

**T1/T2 pool (admissibility already proven): fully-drafted texts plus
frozen oracle specs** (oracle-spec commitment added per
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §4 — the visible task
text alone left a path open where the hidden oracle could still be shaped
after seeing pilot behavior, even in good faith). For each of the 4 (family
x level) cells in {T1, T2} x {MEDIUM, HIGH}, the task constructor freezes
a pool of **exactly 3** fully-drafted, admissible candidate task instances,
admissibility-checked against the Task Construction rubric only, never
against any regime's behavior. Each candidate is recorded as:
```
candidate_id
family
level
task_text_sha256
oracle_spec_sha256                    the hidden oracle's semantic
                                       requirements (what it checks, why)
complexity_breakdown_sha256           the rubric scoring behind MEDIUM/HIGH
initial_state_or_fixture_spec_sha256  any fixture/starting-state requirement
```
The executable oracle implementation may still be built later from the
frozen `oracle_spec`; what is committed pre-pilot is the spec's semantic
content, not only its existence.

**T3 pool (admissibility not yet proven): frozen parameterized specs, not
finished text.** For each of the 2 T3 cells (MEDIUM, HIGH), the constructor
freezes **exactly 3** candidate *specifications* — visible task-contract
template, source repository operation, interrupt boundary (a step
constructed to fail its own validator on first attempt for a realistic,
constructible reason — see §3 above and
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md` §1 for why this replaced
the earlier, withdrawn gate-pause candidate), complexity classification,
state-construction parameters, oracle requirements — each recorded as
`(candidate_id, family, level, sha256(spec))`. A selected T3 spec is only
*mechanically materialized* into an actual task instance after the T3
pilot's seven-link chain (`AUTONOMOUS-TASK-V2-PILOT-PLAN.md` §T3) passes;
no human or agent judgment is exercised at materialization time beyond
deterministic instantiation from the already-frozen spec.

Both manifests (T1/T2 texts+specs, T3 specs — exactly 18 entries total: 3
candidates x 6 cells) are frozen and hashed as a whole (`manifest_hash`)
strictly before the pilot's 9 runs are dispatched, as part of the
pilot-lock record. Pre-pilot vs. post-pilot terminology, disambiguated:
**authored/frozen** happens pre-pilot for every family (full text for
T1/T2, parameterized spec for T3); **selected** (by the deterministic
ranking) and **materialized** (mechanical instantiation — a no-op for
T1/T2's already-finished text, a real deterministic build step for T3's
spec) both happen post-pilot, and neither involves human or agent judgment
beyond the frozen procedure itself.

**Selection independence (commit-then-salt)**: to prevent the constructor
from shaping candidate content around foreknowledge of its own rank, salt
generation is deliberately sequenced *after* the manifest is frozen. (1)
Candidates are authored with arbitrary, rank-uninformed `candidate_id`s. (2)
`manifest_hash = sha256(manifest)` is computed and recorded — this
commitment fixes the candidate set. (3) *Only then* is an independent
random salt generated (e.g., OS-CSPRNG bytes captured at freeze time by a
party other than the constructor) and recorded. (4) Ranking:
`rank_key(candidate_id) = sha256(manifest_hash || salt || candidate_id)`,
ascending, within each cell.

Rank 1 is the primary main-study instance for that cell. **Fallback rank
mapping, made explicit**: if the T3 pilot fails (Hardening Pass 1 §4), T1
and T2 each gain a third instance — specifically **HIGH-cell Rank 2** (the
second-ranked HIGH candidate), never a second MEDIUM instance, giving the
triple {MEDIUM Rank 1, HIGH Rank 1, HIGH Rank 2} per family. **Reserve
(Rank 3)** is invoked only when a *selected candidate itself* is later found
task/oracle-level invalid (`ORACLE_INVALID` or an analogous task-construction
defect) — never for a run-level `HARNESS_UNSTABLE` interruption, which
triggers a same-task technical re-run under the existing
`INSTRUMENT_VALIDITY` rule instead. A harness hiccup never causes a
different task to be selected.

**Tranche 2 has its own, symmetric, pre-pilot-frozen pool** — a second set
of 18 candidates (T1/T2 texts+specs + T3 specs, same structure as above),
hashed as `manifest_hash_2`, ranked via an independently generated `salt_2`
(generated after `manifest_hash_2` is frozen, distinct from `salt`, same
commit-then-salt procedure). If Tranche 2 activates, its 6 instances are the
Rank-1 draws from this second pool — fixed before Tranche-1 results, let
alone the Tranche-2 activation decision, exist. This closes the identical
selection-bias problem one stage later, which the first version of this
section left open. **T3-drop interaction, made explicit**: if the family-
fallback rule dropped T3 in Tranche 1, Tranche 2 (if it activates) draws
**only from its second pool's T1/T2 cells**, using the same 3-instances-
per-family fallback shape — it never reintroduces T3 via the second pool's
T3 Rank-1 draws just because a second pool happens to contain them.

Pool candidates (both pools) remain fully distinct from the pilot's 3
disposable tasks (Task Construction's rule against promoting pilot
instances to main-study status is unaffected).

**Three independent dispatch-order seeds, each via the same commit-then-
salt procedure, ALL frozen pre-pilot — none chosen ad hoc, and none
generated contingent on a later decision** (corrected — a reviewer found
the original wording made `seed_tranche2_dispatch` dependent on the
Tranche-2 activation decision itself, leaving dispatch order for a
not-yet-triggered tranche open until after Tranche-1 results existed,
which is exactly the kind of post-hoc freedom this design otherwise closes
everywhere else): `seed_pilot` (orders the 9 pilot runs), `seed_3` (orders
the 18 main-study Tranche-1 runs), and `seed_tranche2_dispatch` (orders
Tranche 2's 18 runs). All three are generated from `manifest_hash_2`'s own
commit-then-salt procedure and frozen **at the same pre-pilot moment as
both candidate-pool manifests** — `seed_tranche2_dispatch` sits ready and
already fixed whether or not Tranche 2 ever actually activates; activation
only determines whether it is ever *used*, never when it was *generated*.

**Dispatch-order randomization, also frozen pre-pilot**: `dispatch_order =
seeded_fisher_yates(seed_3, the 18 (task, regime) pairs)`, where `seed_3` is
generated by the same commit-then-independent-salt pattern above and logged
before dispatch, not chosen ad hoc at run time.

## 4. Complexity rubric

Selected design: `AUTONOMOUS-TASK-V2-DESIGN-OPTIONS.md` §4, Option A
(structural point count) with family-grounded worked factor definitions —
see `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md` §Complexity Rubric for the full
scoring table and worked MEDIUM/HIGH examples per family.

## 5. Execution regimes

Full agent-facing text lives in the three `AUTONOMOUS-TASK-V2-REGIME-*.txt`
files; this section is the normative summary an evaluator uses to check
regime-fidelity.

- **R0 Robust**: reliability-prioritized baseline. Generous but still bounded
  investigation, explicit final validation, full hard-invariant checks,
  permission to inspect multiple plausible routes, no human help.
- **R1 Lean**: identical task/oracle/model, efficiency-disciplined execution
  — one reconnaissance pass, strongest-route-first, at most one fallback
  route, authoritative single final validation, stop once success conditions
  are sufficiently established, verification effort must trace to a
  plausible failure mode (not ritual). R1 must not be instructable as "be
  less careful" — the regime text is written entirely in terms of *where*
  effort goes, never *whether* effort goes.
- **R2 Escalation-aware**: R1 discipline plus exactly one bounded human
  escalation, gated on the agent being able to state uncertainty, evidence
  already collected, the blocked decision, and the specific information
  needed. Evaluator response is narrow, logged, and must not supply a
  solution or name a preferred route. See
  `AUTONOMOUS-TASK-V2-EVALUATOR-SCORECARD.md` §Escalation Rubric for the
  `LEGITIMATE_ESCALATION` vs `ESCALATION_LAUNDERING` line.

## 6. Acceptance model

Every run is scored on four independent axes (never collapsed into one
number for the primary analysis):

```
GOAL_STATE:          ACHIEVED | NOT_ACHIEVED
PROCESS_CONTRACT:    SATISFIED | VIOLATED | NOT_APPLICABLE
INSTRUMENT_VALIDITY: VALID | ORACLE_INVALID | BASELINE_CONTAMINATED
                      | ISOLATION_BREACH | HARNESS_UNSTABLE
ESCALATION (R2 only): NONE | LEGITIMATE_ESCALATION | ESCALATION_LAUNDERING
```

`ACCEPTED` iff: `GOAL_STATE=ACHIEVED AND PROCESS_CONTRACT in {SATISFIED,
NOT_APPLICABLE} AND hidden oracle passes AND no forbidden mutation AND
INSTRUMENT_VALIDITY=VALID`. R2 additionally records `ACCEPTED_WITH_ESCALATION`
as a distinguishable but still-accepted subtype. Agent self-report never
determines any axis; every axis is set by the evaluator scorecard against
mechanically captured evidence (see
`AUTONOMOUS-TASK-V2-EVALUATOR-SCORECARD.md`).

**Acceptance is frozen before any human repair — ordering enforced, not
just stated** (Lock-Readiness Response 3 §9, closing a real risk: a prior
telemetry field description implied `accepted` could be conditioned on
post-completion human repair, entangling efficacy and cost-benefit). The
four axes above, and the `accepted`/`accepted_with_escalation` booleans
derived from them, are evaluated against the agent's own completion state
**only** — before any human repair is considered. If a human later
salvages a `NOT_ACCEPTED` run, that is recorded as a separate fact
(`salvaged_after_manual_repair`, `manual_repair_seconds` —
`AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md`) and never retroactively changes
the frozen `accepted` value.

## 7. Telemetry and cost model

Full schema: `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md`. Cost-accounting design
selected in `AUTONOMOUS-TASK-V2-DESIGN-OPTIONS.md` §2 (Option A: full-context
accounting, regime-prompt tokens tracked as a separate reportable line item).

**One primary confirmatory dollar measure plus required diagnostics,
corrected twice** (Lock-Readiness Response 2 §4 first replaced a flawed
single-subtraction formula with per-call accounting; Lock-Readiness
Response 3 §7 then found that even per-call subtraction is unsafe as a
*dollar* figure, since a provider's `cached_input_tokens` reporting can
conflate genuine conversation history with the static task/regime prefix —
demoted accordingly):

- **Operational actual cost** (`operational_actual_cost_usd`): sum of what
  was genuinely billed across every model call in the run (using
  cached-token pricing where the provider reports and prices it
  distinctly). The **sole primary, confirmatory dollar measure** — "what
  would deploying this regime actually cost." Computed from
  `model_calls[]` per-call telemetry (schema: §below), not from two
  aggregate token counts.
- **Dynamic-execution resource diagnostics** (`dynamic_execution_input_tokens`,
  `dynamic_execution_output_tokens` — token counts, not dollars): for each
  model call, the fixed static-prefix token count (task-bundle +
  regime-prompt tokens) is subtracted from that call's input tokens,
  floored at zero, summed across all calls. Required, co-equal reporting
  used to interpret *why* a cost difference occurred — never itself a
  confirmatory dollar claim. A `dynamic_execution_resource_cost_usd` dollar
  figure MAY additionally be derived, but only when the provider exposes
  exact cache-segment attribution, and even then is labeled best-effort/
  conditional, never promoted alongside `operational_actual_cost_usd`. A
  result where only `operational_actual_cost_usd` drops, unaccompanied by
  any drop in the token/tool/wall-clock diagnostics, is reported as an
  operational-saving finding ("prompt-driven") distinct from one where the
  diagnostics also drop ("reasoning-efficiency improvement") — neither
  substitutes for the other in any report.

**Human minutes are never folded into a dollar cost view** (corrected — the
original draft's `operational_total_cost_usd` had folded in human
supervision minutes at a frozen rate card, contradicting this same
document's later commitment to deriving, not assuming, a labor rate).
Primary economics is always reported as the three-dimensional vector: model/
API dollars, wall-clock seconds, active human minutes — never combined by
default. A separate, explicitly-labeled **sensitivity-analysis** metric,
`total_cost_at_rate[]` over a small preregistered set of hourly rates (e.g.
$0/$50/$150/$400), exists purely for illustration and never feeds H1-H5 or
the Tranche-2 decision rule.

Central derived metrics, computed separately for dollars (operational
actual cost only) / wall-clock / active human minutes (never combined into
one weighted score in the primary analysis):

```
Cost per Accepted Task (aggregate) = total cost of ALL attempts (including
                                      failures) / number of accepted outcomes

Paired Cost Delta (matched outcomes) = task-by-task ROBUST-vs-LEAN cost
                                        comparison, restricted to pairs
                                        where BOTH runs were ACCEPTED
```

Neither metric replaces the other: the aggregate metric protects against
`CHEAP_FAILURE` inflating an apparent efficiency win; the paired-matched
metric shows whether an efficiency difference holds on genuinely comparable
outcomes (a regime with a much lower accepted rate can still show a
misleadingly low aggregate cost on its easier successes).

Human break-even rate (only meaningful if a human baseline exists — see §9):

```
r* = A / (Sh - Sa),   valid only when Sh > Sa
```

## 8. Hypotheses

- **H1 (Efficacy preservation), simplified to a single mechanical rule**
  (corrected twice: Lock-Readiness Response 2 §6 first separated
  instrument-invalidity from efficacy judgment; Lock-Readiness Response 3
  §2 then found the remaining rule still too narrow — gating H1's failure
  on the LEAN failure being classified as a "hidden-invariant/oracle
  violation" left plain `NOT_ACHIEVED` or `PROCESS_CONTRACT=VIOLATED`
  outcomes technically outside the rule if not cleanly classified that way,
  contradicting the `ACCEPTED` definition's own inclusiveness in §6 above).
  Sequence: first, `INSTRUMENT_VALIDITY != VALID` runs (including
  `HARNESS_UNSTABLE`) are excluded and replaced via technical rerun — **no
  efficacy judgment of any kind** is made on them, full stop; this gate
  remains entirely prior to and separate from H1. Then, among the surviving
  `INSTRUMENT_VALIDITY = VALID` runs: **H1 HOLDS unless at least one valid
  task instance shows ROBUST = `ACCEPTED` and LEAN != `ACCEPTED` — no
  further sub-classification of LEAN's failure reason gates this
  determination.** Any single such occurrence means **H1 FAILS**,
  deterministically, feeding directly into the Tranche-2 state machine
  (§10). A separate, purely descriptive field records *why* LEAN failed
  (for the tranche report's narrative) but no longer decides whether H1
  failed. At n=6, one such regression is a 16.7-point swing and must never
  be waved off as "approximately equal success."
- **H2 (Efficiency improvement)**: LEAN's paired median cost, **computed
  over the matched pairs where both ROBUST and LEAN are ACCEPTED on that
  task instance** (the same pair set as §7's
  `paired_cost_delta_matched_outcomes` and the Tranche-2 decision rule's
  step 2/3, §10 — one explicit, shared pair set, not restated three
  different ways), is lower than ROBUST's on `operational_actual_cost_usd`
  — **the sole primary, confirmatory dollar measure** (Lock-Readiness Response 3 §7 demoted the
  per-call-subtracted "dynamic execution" figure from a second confirmatory
  dollar view to a diagnostic one, after a reviewer found that a provider's
  cached-token reporting can conflate genuine conversation history with the
  static task/regime prefix, making a naive subtraction unreliable as a
  dollar figure). `dynamic_execution_input_tokens` /
  `dynamic_execution_output_tokens` (token counts, not dollars) plus tool-
  call counts and wall-clock are reported as required, co-equal
  **behavioral/resource diagnostics** used to interpret *why* a cost
  difference occurred — a drop in `operational_actual_cost_usd` unaccompanied
  by any drop in the diagnostic token/tool/wall-clock measures is reported
  as an operational-saving finding ("prompt-driven") distinct from one where
  the diagnostics also drop ("reasoning-efficiency improvement"), never
  conflated. A `dynamic_execution_resource_cost_usd` dollar figure MAY
  additionally be derived only when the provider exposes exact cache-
  segment attribution, and is labeled best-effort/conditional even then —
  never promoted to confirmatory status alongside `operational_actual_cost_usd`.
  A 20% paired-median reduction on `operational_actual_cost_usd` is retained
  as an *effect-size reference*, not a pass/fail gate (see design question
  13 resolution in `AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md`) — with n=6 pairs,
  a single frozen threshold would create false precision.
- **H3 (Escalation efficiency)**: bounded escalation (R2) yields a lower or
  equal cost-per-accepted-task than LEAN alone, accounting for logged human
  escalation minutes.
- **H4 (Complexity-dependent break-even)**: within each family, autonomy's
  relative cost position (vs. ROBUST, and vs. a human baseline if collected)
  improves from MEDIUM to HIGH complexity. Tested within-family; pooled
  across families only as exploratory (per
  `AUTONOMOUS-TASK-V2-DESIGN-OPTIONS.md` §4).
- **H5 (No concealed quality loss)**: LEAN's efficiency gain, if any, is not
  explained by INSTRUMENT_VALIDITY failures, PROCESS_CONTRACT violations, or
  hidden-oracle failures being more frequent than in ROBUST.

H1/H2/H5 are confirmatory. H3/H4 are exploratory given n=6 (stated plainly,
not hedged).

**Stochasticity, preregistered explicitly** (Lock-Readiness Response,
non-blocker item 5): each (task, regime) cell is one run. Task is the
paired block; model/settings are identical across regimes within a task; a
run that is valid but surprising is never rerun; only runs flagged
`INSTRUMENT_VALIDITY != VALID` receive technical replacement (per §14).
Conclusions remain descriptive/paired, never inferential-statistical, at
n=6. Tranche 2 (§10) improves precision across additional tasks but does
NOT estimate within-cell stochastic variance (ordinary agent-run-to-run
variation vs. a true regime effect are not separable with one run per
cell) — this is a named, accepted limitation, not something this design
claims to solve.

## 9. Human baseline

Selected design: `AUTONOMOUS-TASK-V2-DESIGN-OPTIONS.md` §3, Option B — no
human baseline collected in Tranche 1; the single-blinded-operator module
(Option A) is fully specified below as ready-to-activate but not scheduled.

If activated later: one operator, blinded to agent trajectories/oracle/
evaluator routes, completes all six held-out task contracts (task-visible
text only, identical to what the agent regimes receive), timed for active
completion minutes, failed attempts, and external help used. Order is fixed
(not randomized) to avoid mid-sequence context bleed changing task
information content; this within-subject-only design accepts
`HUMAN_BASELINE_INFORMATION_ADVANTAGE` risk (later tasks benefit from earlier
ones in a way agent runs, which are fresh per run, do not) and that risk must
be reported alongside any r* number, not silently absorbed into it.

**Without a human baseline, Tranche 1's allowed conclusion ceiling is
`AUTONOMOUS PROTOCOL EFFICIENCY IMPROVED` (or its negative). It may not claim
`AUTONOMY IS COST-EFFECTIVE RELATIVE TO HUMAN EXECUTION`.**

## 10. Sequential design

```
CANDIDATE POOL  TWO 18-candidate pools (Tranche 1 + Tranche 2, 3 per family
FREEZE          x level cell each, 36 total), each fully drafted/specced,
                oracle-spec-committed, and hashed; deterministic selection
                ranking computed for both via commit-then-salt — all before
                any pilot run (see §3b) — closes post-pilot task-selection
                bias for BOTH tranches, not just the first
                                |
PILOT           3 disposable tasks (1/family) x 3 regimes = 9 runs
                purpose: instrument validation only, never task tuning
                                |
                         freeze + adjudicate
                                |
                repair instrument only if defects found
                (explicit supersession/addendum, never silent edit)
                                |
                    lock MAIN STUDY (this design's exit point)
                                |
MAIN TRANCHE 1  6 held-out tasks (2/family) x 3 regimes = 18 runs
                (instances are Rank-1 draws from the frozen pool per §3b,
                not freshly authored after the pilot)
                                |
                    freeze all 18 runs, adjudicate
                                |
              Tranche-2 activation check (see below)
                     /                        \
              not activated                 activated
                    |                            |
          report Tranche-1-only        MAIN TRANCHE 2 (preregistered
          conclusion                    6 new tasks x 3 regimes = 18 runs)
```

**Tranche-2 decision rule — rebuilt as a strict priority order, evaluated
top to bottom, first match wins, now with an absolute ROBUST-efficacy floor
gate** (Lock-Readiness Response 3 §3 first removed the row-overlap
contradiction; a subsequent review then found a remaining false-positive
path: with the rules as stated, ROBUST 0/6 ACCEPTED and LEAN 0/6 ACCEPTED,
with LEAN costing 40% less and the other dimensions happening to align,
would pass straight through H1 — which only fires on a ROBUST-accepted/
LEAN-failed *pair*, and finds none here — into the `>25%` row, declaring
`EFFICIENCY_IMPROVED` for two regimes that accomplished nothing. Closed
with an efficacy floor gate that runs before H1 is even consulted):

```
INSTRUMENT INVALID (>=2 of 18 runs non-VALID)
  -> repair/re-pilot the affected cell(s), NOT Tranche 2 -- a separate,
     non-equivalent trigger, checked before any of the rows below and never
     conflated with them

0. ROBUST ACCEPTED rate < 5/6 (the frozen efficacy floor -- ROBUST is
   explicitly the high-reliability baseline; a rate below this means the
   baseline itself is not established, so no comparison against it is
   meaningful)
   -> STOP; report EFFICACY_NOT_ESTABLISHED. No positive efficiency
      conclusion (EFFICIENCY_IMPROVED or otherwise) may be issued from
      this tranche regardless of any cost figure. Checked BEFORE H1 --
      H1 alone (a paired ROBUST-accepted/LEAN-failed check) cannot detect
      "both regimes failed," which is exactly the gap this row closes.

1. (ROBUST efficacy floor met) H1 FAILS (any valid pair, ROBUST=ACCEPTED,
   LEAN!=ACCEPTED)
   -> STOP; report the efficacy failure. Overrides every row below
      regardless of cost effect size.

2. (H1 holds) Using ONLY the matched pairs where BOTH ROBUST and LEAN are
   ACCEPTED on that task instance (the same "matched outcomes" set §7's
   paired_cost_delta_matched_outcomes is defined over -- H2/this rule and
   §7's metric now share one explicit pair set, not two independently
   worded ones): are wall-clock and human-minutes paired deltas consistent
   in direction with the operational_actual_cost_usd paired delta? A ZERO
   human-minute delta on the matched pairs counts as NEUTRAL/CONSISTENT,
   not as a contradiction requiring a nonzero match.
   NO  -> MATERIALLY AMBIGUOUS; Tranche 2 eligible, regardless of the
          dollar percentage magnitude in step 3.
   YES -> continue to step 3.

3. (H1 holds, dimensions consistent) operational_actual_cost_usd paired
   median reduction, computed over the SAME both-ACCEPTED matched pairs as
   step 2 -- the ONE named decision variable (dynamic-execution
   diagnostics remain required reporting, never the Tranche-2 trigger;
   aggregate cost_per_accepted_task_usd, §7, remains the separate
   cheap-failure guard alongside this matched-pair view, not a substitute
   for it):
   <10%    -> STOP; report negative/negligible
   10-25%  -> Tranche 2 eligible
   >25%    -> STOP; report EFFICIENCY_IMPROVED
```

Because step 0 precedes step 1, step 1 precedes step 2, and step 2 precedes
step 3's magnitude bands, no Tranche-1 outcome can ever satisfy two rows at
once, and "cheap because ineffective" can no longer produce a positive
conclusion — the efficacy floor forecloses that path before H1 or any cost
comparison is even reached.

## 11. Failure modes (preregistered)

`EFFICIENCY_BY_UNDERVERIFICATION`, `ESCALATION_LAUNDERING`, `CHEAP_FAILURE`,
`VERIFICATION_THEATER`, `SEARCH_THEATER`, `HUMAN_COST_HIDING`,
`HARNESS_COST_HIDING`, `TASK_FAMILY_IMBALANCE`, `CROSS_RUN_LEAKAGE`,
`ORACLE_ROUTE_COUPLING`, `REFERENCE_SOLUTION_LEAKAGE`,
`RECOVERY_RESET_LAUNDERING`, `COST_ACCOUNTING_DRIFT`,
`HUMAN_BASELINE_INFORMATION_ADVANTAGE`. Full definitions and the detection
signal for each: `AUTONOMOUS-TASK-V2-EVALUATOR-SCORECARD.md` §Failure Mode
Detection. Adversarial simulation against eight pathological agent archetypes:
`AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md` §Adversarial Review.

## 12. Held-out verification

Route-independent, agent-hidden, capable of contradicting the agent. Per
family (full detail in `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md`):

- **T1**: independent semantic oracle checks the *end state* the mechanism
  was supposed to produce (e.g., does the installed/importable package now
  route correctly?), never which command/tool was invoked.
- **T2**: exact-diff oracle over the preserved regions (byte-identical
  outside the permitted edit) plus a re-run of
  `tests/test_field_contract_agreement.py`-equivalent validation.
- **T3**: ledger-diff oracle (no duplicate/re-executed steps for already-
  ledgered work) plus a hidden **replay check** — the evaluator re-invokes
  the same `resume=True` recovery procedure once more after the agent
  claims completion and requires **zero new step/artifact/validation
  ledger events** (idempotency). Corrected for internal consistency (Lock-
  Readiness Response 3 §1): `run_started`/`run_completed`-class bookkeeping
  events are explicitly exempted from this requirement — every invocation
  logs these regardless of whether any step executes, so a literal
  "zero additional mutation" requirement is impossible to satisfy and is
  not what is checked.

## 13. Adjudication ordering

1. Instrument validity axis first (a run with `ORACLE_INVALID`,
   `ISOLATION_BREACH`, or `HARNESS_UNSTABLE` is excluded from efficacy/cost
   analysis and reported separately — never silently dropped).
2. Goal state and process contract next (both required for ACCEPTED).
3. Escalation classification (R2 only).
4. Cost/telemetry rollup, computed only over the surviving, valid runs, with
   failures still counted in the "cost per accepted task" denominator's
   numerator per §7.
5. Failure-mode tagging (§11) applied to every run, accepted or not.

## 14. Stop / invalidity rules

- **`ISOLATION_BREACH`, defined normatively** (Lock-Readiness Response
  §Issue 3, not merely a preflight concern): any agent tool access that
  reaches outside the approved task root, the approved runtime/tool
  locations, or an explicit allowlist, into another repository or
  experiment location, is an `ISOLATION_BREACH`. That run is retained for
  harness telemetry but cannot support efficacy or economic inference. The
  evidence trail required to detect a breach must cover every tool-access
  channel the harness exposes to the agent (shell/Bash, file-read tools,
  search tools, language-specific filesystem APIs) — not shell commands
  alone. Where a specific channel cannot be observed or logged, that is
  recorded as a named, additional technical limitation (distinct from, and
  stacked on top of, the `AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED` disclosure
  already carried by `AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh`) rather than
  silently assumed covered.
- Any run flagged `ISOLATION_BREACH` invalidates that run only; it does not
  invalidate the tranche unless >=2 such breaches occur, at which point the
  filesystem-scope isolation approach itself must be re-audited before
  continuing (`AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` is the mitigation, not a
  guarantee — see that script's header for the same MITIGATED / AUDITABLE /
  NOT TECHNICALLY CLOSED framing used in prior Autonomous Task work, and see
  `AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md` for the two concrete
  exposure vectors it was hardened against).
- Any run flagged `ORACLE_INVALID` blocks that task instance across *all
  three regimes* for the current tranche (the oracle is task-level, not
  run-level) and routes to instrument repair, not silent exclusion.
- `CROSS_RUN_LEAKAGE` detected on any run invalidates that run and triggers a
  fresh re-run from a clean clone before that task/regime cell counts.

## 15. Design questions — resolutions

See `AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md` §Design Questions for the full
15-question resolution log (referenced inline above at each relevant
section). Two are called out here because they gate whether this protocol is
locked as-is or needs a human decision first:

- **Q13 (20% threshold)**: resolved in Hardening Pass 1 — replaced by a
  10%/25% band (§10 above), frozen and justified by n=6's actual statistical
  power rather than picked as a default. See
  `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §5.
- **Q11 (T1 admissibility)**: resolved `T1_ADMISSIBLE` in Hardening Pass 1
  against an actual clean checkout at the frozen SHA (not the newer working
  tree) — see §3 above and
  `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §1. The substrate changed from
  the initial pass's (partly incorrect) description to the verified
  dual-consumer `workflow-registry.yaml` divergence.
- **Q10/Q11 fallback (T3 fails)**: resolved in Hardening Pass 1 — frozen
  family-fallback rule (T1+T2 expand to 3 instances each, preserving 6
  paired tasks) — see `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §4.
