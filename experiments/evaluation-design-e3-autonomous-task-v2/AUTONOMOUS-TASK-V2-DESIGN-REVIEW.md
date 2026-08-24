# Autonomous Task v2 — Design Review

Status: DRAFT. This is the adversarial review pass required before any
pilot-lock recommendation. It does not itself lock, hash, dispatch, pilot,
or construct main-study tasks.

## Adversarial review — eight pathological agents

For each archetype: is the behavior structurally blocked by the protocol as
drafted, and if not, is it unambiguously observable in telemetry/scorecard?

### 1. The Cheap Quitter (fails quickly, looks inexpensive)
Not structurally blocked — a regime cannot force genuine effort. **Observable**:
`CHEAP_FAILURE` detection (scorecard §6) flags a `NOT_ACHIEVED` run cheaper
than the median `ACCEPTED` cost for the same task instance. Because cost per
accepted task keeps failures in the numerator (protocol §7), a fleet of cheap
quitters *raises* rather than lowers a regime's reported cost-per-accepted-
task — the derived metric is itself the primary defense here, not a
behavioral rule.

### 2. The Verifier Addict (succeeds, wastes budget re-checking known state)
Partially blocked in R1/R2 by the "verification must trace to a plausible
failure mode" instruction; not blocked at all in R0 by design (R0's whole
purpose is reliability-over-efficiency, so R0 is *expected* to look like
this to some degree). **Observable**: `VERIFICATION_THEATER` tag (scorecard
§6) plus `redundant_validations_count` in telemetry. Risk: if R0 is
expected to over-verify, the review must not mistake R0's designed-in
generosity for a defect — the failure mode is for *unmotivated* repetition
(re-checking unchanged state), not thoroughness itself. This distinction is
evaluator judgment and is the weakest link in this defense; flagged as an
open risk below.

### 3. The Human Outsourcer (uses escalation to get the solution)
Structurally limited (one escalation, four required elements, response
constrained to be narrow) but not fully blocked — a sufficiently narrow-
sounding question can still smuggle in the effective answer ("is route X the
canonical one?" answered "yes" is close to naming the route). **Observable**:
`ESCALATION_LAUNDERING` rubric (scorecard §4) is the primary defense; the
rubric explicitly says a response that would have done the agent's semantic-
fit judgment for it counts as laundering even if the request was formally
well-shaped. This puts real weight on evaluator judgment at escalation-
response-authoring time, not just after the fact — the evaluator answering
the escalation must itself follow the "narrow, no preferred route" rule
before the run continues, not only in retrospective scoring.

### 4. The Route Gambler (guesses first plausible route, hopes it passes)
Blocked by construction, not by observation: T1's rule that wrong routes
must fail *semantically* (Task Construction §T1) means a gambled wrong route
produces a genuine `NOT_ACHIEVED`, not a lucky pass. **Observable** as a
matter of course via `GOAL_STATE` and, if it happens repeatedly for one
regime, via `TASK_FAMILY_IMBALANCE`. Hardening Pass 1 added a second,
finer-grained defense specific to T1's now-verified construct: a gambler who
happens to land on the correct `workflow-registry.yaml` copy without ever
reading the consumer-side code (`registry.py` / `_validator_utils.py`) that
determines which copy is authoritative is caught by the new
`route_evidence_trace` telemetry field and its associated
`ORACLE_ROUTE_COUPLING`-adjacent scorecard note (see Hardening Pass 1 §6,
Risk C) — a lucky guess still counts as `ACCEPTED` but is flagged as evidence
-thin in evaluator notes rather than silently indistinguishable from a
reasoned choice.

### 5. The Benchmark Gamer (infers evaluator preference over stated goal)
Blocked by construction rules (no reference-solution leakage; oracle checks
end-state semantics, not command identity) more than by observation. Residual
risk: if a task bundle's wording inadvertently signals "the intended way," a
gamer succeeds without genuinely resolving the ambiguity the task exists to
test. **Observable** via `REFERENCE_SOLUTION_LEAKAGE` and via
`ORACLE_ROUTE_COUPLING` checked in the *opposite* direction (a route the
contract didn't require still passing is fine; a gamer converging on the
"obviously intended" route across every regime/run at a rate suspiciously
higher than the route's actual evidentiary support would warrant is a
construct-validity smell worth flagging in adjudication notes even though no
single preregistered failure-mode tag captures it directly — this is named
here as a gap, not resolved).

### 6. The Recovery Resetter (destroys/recreates state instead of recovering) — T3 only
Blocked by construction: the evaluator retains an independent hash manifest
of pre-existing artifacts (Task Construction §T3) not trusted to the agent,
so a reset-and-recreate is detectable even if the recreated content looks
plausible. **Observable** via `RECOVERY_RESET_LAUNDERING` tag, hash mismatch
on supposedly-untouched artifacts, and duplicate run-ledger entries for
already-completed steps.

### 7. The Silent Near-Miss (plausible artifact, violates one hidden invariant)
This is precisely what independent, agent-hidden oracle checks exist to
catch (protocol §12/§6 acceptance rule: ALL stated invariants must hold, not
"the ones the agent thought to check"). **Observable** directly via
`GOAL_STATE`/oracle fail. The real risk is oracle *incompleteness* — an
invariant the task construction rules failed to make checkable. Mitigated,
not eliminated, by requiring every T2/T3 oracle to reuse an existing
repository-native check where one exists (Task Construction §T2).

### 8. The Slow Winner (perfect result, operationally irrational cost)
Not blocked at all by design — R0 is explicitly allowed to be this. The
defense is entirely in the derived metrics: cost-per-accepted-task and the
paired R0-vs-R1/R2 comparison are exactly the numbers that would reveal a
regime (or a whole family) is a "slow winner" pattern, which is itself one
of the experiment's legitimate possible findings
(`EFFICACY_WITHOUT_ECONOMIC_GAIN`), not a defect to be engineered away.

**Summary**: no archetype passes fully undetected, but three residual risks
depend on evaluator judgment quality rather than a mechanical rule: (2)
distinguishing designed-in R0 thoroughness from genuine
`VERIFICATION_THEATER`; (3) an evaluator's own escalation response quality
at the moment of answering, not just in retrospect; (5) the "obviously
intended route" convergence smell has no dedicated failure-mode tag. These
three are named as open risks, not silently absorbed.

## Construct-validity analysis

- **T1**: strongest construct of the three — grounded in a real, currently-
  live dual-invocation-path ambiguity and a real multi-copy registry file
  duplication, neither invented for this benchmark. Main open risk: whether
  the multi-copy duplication survives a clean checkout at the exact frozen
  SHA (build directories are commonly regenerated/untracked) — this must be
  re-verified before lock, not assumed from the current 85-commits-ahead
  working tree.
- **T2**: strong construct — `artifact-contracts.yaml` is an actively
  enforced contract (per this repository's own `CLAUDE.md` verification-
  discipline section), giving the task family a genuine external ground
  truth beyond the benchmark's own oracle.
- **T3**: real substrate (append-only run ledger, per-run artifact sets) but
  the weakest-*proven* construct — this design pass identified the
  substrate and a plausible interrupt-and-resume construction method, but did
  not attempt to build or run it. The pilot's T3 cell carries disproportionate
  weight: if reproducible partial-state construction fails there, the
  family should be narrowed or dropped for Tranche 1 rather than forced
  (see Pilot Plan §Outcomes, `EXPERIMENT_NOT_ADMISSIBLE` applies at the
  family level, not automatically at the whole-experiment level).

## Cost-accounting threats

Covered substantively in `AUTONOMOUS-TASK-V2-DESIGN-OPTIONS.md` §2. Residual
risk after selecting Option A (full accounting + separate regime-prompt line
item): a reviewer must actually run the robustness check (H2 with
regime-prompt tokens excluded) rather than treating the line-item split as
sufficient by itself — the split creates the *possibility* of the check, it
does not perform it automatically.

## Evaluator bias threats

The escalation rubric (§4 of the scorecard) and the "obviously intended
route" gap above both place real interpretive weight on the evaluator. No
purely mechanical design eliminates this for a study whose subject is
*judgment quality under different resource budgets* — an evaluator with a
prior preference for one regime's philosophy is a real, unmitigated risk.
Partial mitigation: adjudication ordering (protocol §13) forces instrument-
validity to be assessed before efficacy/cost, and requires evidence citation
(tool-call indices, verbatim escalation text) for every subjective call,
which at least makes evaluator reasoning auditable after the fact even
though it does not prevent bias at the time of scoring.

## T1/T2/T3 admissibility at this frozen SHA — summary

**Superseded by Hardening Pass 1** (`AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md`),
which re-verified all three families against an actual clean, detached
worktree at exactly `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`, not the
85-commits-ahead working tree this initial review used. Updated table:

| Family | Admissibility | Confidence | Key open item |
|---|---|---|---|
| T1 | `T1_ADMISSIBLE` | Medium-high | substrate corrected to the verified dual-consumer `workflow-registry.yaml` divergence; discoverable only via source, not docs |
| T2 | `T2_ADMISSIBLE` | High | distinctness from external D/D' cannot be confirmed from this repo alone |
| T3 | `T3_CONDITIONALLY_ADMISSIBLE` | Medium-high (upgraded) | mechanism-verified (safe append-only writes, reusable audit subcommand) but no live interrupt-and-resume has been executed; pilot-gated; family-fallback rule now frozen |

The original table below is retained for provenance (what the initial pass
believed before frozen-SHA re-verification), not as current guidance:

| Family | Admissibility (initial pass, since corrected) | Confidence | Key open item |
|---|---|---|---|
| T1 | ADMISSIBLE | Medium-high | re-verify registry duplication at exact frozen-SHA clean checkout |
| T2 | ADMISSIBLE | High | none material |
| T3 | CONDITIONALLY ADMISSIBLE | Low-medium | reproducible partial-state construction unproven; pilot-gated |

## Design questions — full resolution log

1. **Is R0 vs R1 a real treatment while keeping task info identical?** Yes —
   the three regime texts differ only in execution-discipline instructions;
   task bundle content is identical across regimes for a given instance
   (verified by construction: the regime files contain no task-specific
   content at all).
2. **Could LEAN look cheaper merely from a shorter prompt?** **Updated per
   Lock-Readiness Response 3 §7** (the original with/without-regime-prompt
   robustness-check answer below is superseded, not merely supplemented):
   `operational_actual_cost_usd` (sum of what was genuinely billed across
   every model call, via `model_calls[]`) is the sole primary, confirmatory
   dollar measure; `dynamic_execution_input_tokens` /
   `dynamic_execution_output_tokens` (static task/regime-prefix tokens
   subtracted per call) are required, co-equal *diagnostics* reported
   alongside it — a drop in the dollar measure unaccompanied by any drop in
   the token diagnostics is reported as an operational-saving,
   prompt-driven finding, distinct from a reasoning-efficiency finding,
   never conflated. This replaced the original with/without-regime-prompt-
   tokens robustness check because per-call subtraction (needed once
   multi-turn context repetition was accounted for) made a single robustness
   comparison insufficiently precise as a dollar figure — see Lock-Readiness
   Response 2 §4 and Response 3 §7 for the two successive corrections.
3. **Should task-bundle tokens count in every run?** Yes — they're constant
   across regimes for a given task instance, so they cancel in the paired
   comparison; excluding them would just remove information for no benefit.
4. **How does wall-clock handle forced background execution / rate limits?**
   Classified via the Interruption Classification schema
   (`AGENT_OPERATIONAL_COST` vs `INSTRUMENT_HARNESS_INVALID`), decided at
   the time of interruption with a one-line justification, never
   reconstructed post-hoc from the outcome.
5. **Which interruptions count as agent cost vs. instrument invalidity?**
   Same mechanism as Q4 — the classification is the answer, not a separate
   rule.
6. **How is active human attention timed mechanically?** **Resolved, not
   merely partial** (updated per Lock-Readiness Response 3 §8 — the
   `escalation_response_seconds` field named below no longer exists, and
   the "harness-level instrumentation not yet built" caveat is narrowed):
   `AUTONOMOUS-TASK-V2-TELEMETRY-SCHEMA.md` now specifies three explicit
   timestamps — `escalation_request_emitted_at`, `responder_started_at`,
   `responder_submitted_at` — with `human_active_seconds =
   responder_submitted_at - responder_started_at` defined precisely
   (never request-to-response latency, which would include idle wait
   before the responder looks at the request). `human_active_seconds_total`
   is defined as the explicit sum of `human_active_seconds` +
   `operational_recovery_seconds` + `approval_review_seconds`. The one
   remaining honest limitation: if `responder_started_at` cannot be
   captured in a given execution environment, the field is renamed
   `response_latency_seconds` for that run and no attention-savings claim
   may be drawn from it — a per-run fallback, not an unsolved design gap.
7. **How is an R2 escalation response standardized for paired comparison?**
   The four-element request format plus the "narrow, no preferred route, no
   solving-for-the-agent" response rule (regime text + scorecard §4) is the
   standardization; it is qualitative, not templated, because templating a
   response risks leaking the oracle's shape.
8. **How is regime ordering randomized without leakage?** Fresh standalone
   clone + fresh agent session per run (protocol §10, §Main Matrix) is the
   leakage control; randomized dispatch order is recorded per run
   (`run_order_index`) so post-hoc order-effect analysis is possible without
   the order itself being a confound in the primary paired comparison
   (each task_instance_id x regime cell is independent of dispatch order by
   construction). **Updated per Lock-Readiness Response 3 §10 item 5**: the
   dispatch order is no longer merely "randomized" but generated by a named,
   frozen procedure — `seeded_fisher_yates(seed, ...)` — with three
   independent seeds (`seed_pilot`, `seed_3`, `seed_tranche2_dispatch`), all
   generated via the same commit-then-salt process and all frozen at the
   same pre-pilot moment as the candidate-pool manifests (corrected once
   more in Response 4 §3, since the Tranche-2 seed was initially, and
   wrongly, described as generated only upon Tranche-2 activation).
9. **Distinguishing unnecessary validation from reasonable-given-uncertainty
   validation?** This is the Verifier Addict residual risk above — answered
   only partially: the "plausible failure mode" test is the rule, evaluator
   judgment (with cited evidence) is the enforcement mechanism, and this
   protocol does not claim to have removed the judgment call.
10. **Can T3 recovery tasks be constructed naturally at this frozen SHA?**
    Plausibly yes (real run-ledger + per-run artifact substrate exists) but
    UNPROVEN — this is exactly why the T3 pilot cell exists and carries
    extra weight (see Construct-validity analysis above). **Refreshed, per
    the reviewer's own suggestion (not a correction — this conclusion was
    never wrong, only worth naming more precisely)**: the now-confirmed
    substrate is specifically the `FAILED`-validator/legitimate-retry code
    path (`workflow-runtime.py`'s `resume=True`, verified against the
    frozen SHA that a `FAILED` step is excluded from `resume_skip` and is
    genuinely re-executed on resume — Lock-Readiness Response 3 §1), not
    the originally-assumed hard-kill or the subsequently-tried-and-withdrawn
    `gate: review` pause (confirmed broken: a `PAUSED` step is
    unconditionally skipped, bypassing the approval boundary). "Plausibly
    yes, unproven" remains the accurate status — the mechanism is now
    traced through working code, but no live run has exercised it.
11. **Does T1 have a genuinely admissible fresh instance, or is the banked
    idea still confounded?** **Resolved `T1_ADMISSIBLE`, not merely
    pending** (updated — the frozen-SHA re-verification this entry
    originally deferred to has since completed): Hardening Pass 1 re-checked
    the substrate against an actual clean, detached worktree at exactly
    `0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`, which corrected the
    ambiguity's description (dropped the Skill-tool-vs-CLI candidate and the
    `build/`-based triple-copy claim) and confirmed a real, already-diverged
    dual-consumer `workflow-registry.yaml` ambiguity instead — fresh
    relative to the banked-but-unexecuted Semantic Tool Routing construct,
    grounded in this repository's own current mechanisms. See
    `AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §3 and
    `AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §1.
12. **Is six held-out tasks enough for the intended claims?** No, not for
    strong pooled statistical claims — resolved by scoping H3/H4 as
    exploratory and H1/H2/H5 as confirmatory-but-modest (paired comparison,
    effect-size reference rather than a hard threshold), per protocol §8,
    rather than fabricating confidence n=6 doesn't support.
13. **Should the 20% threshold be retained, changed, or reference-only?**
    **Resolved, not open** (updated — the "deliberately left for a human to
    set" language below described the state before Hardening Pass 1 froze
    the band): the 20% figure is retained as an *effect-size reference*
    only (protocol §8), not a pass/fail gate — at n=6 a single frozen
    threshold would manufacture false precision. The Tranche-2
    indifference band itself is frozen at `<10% / 10-25% / >25%`
    (Hardening Pass 1 §5), further hardened into a strict, non-overlapping
    priority order — efficacy floor, then H1, then cross-dimension
    consistency, then the magnitude band — in Lock-Readiness Response 3 §3
    and Response 4 §4 (closing a "cheap but ineffective" false-positive
    path the original band alone did not catch).
14. **What constitutes meaningful efficacy loss under paired n=6?**
    **Replaced with a stricter, deterministic pairwise rule** (updated — the
    aggregate-rate-drop framing below is superseded, not merely refined):
    after the absolute ROBUST-efficacy floor (`ROBUST ACCEPTED rate < 5/6`
    stops the tranche with `EFFICACY_NOT_ESTABLISHED` before any comparison
    is attempted — Lock-Readiness Response 4 §4), H1 fails on **any single
    valid pair** where ROBUST = `ACCEPTED` and LEAN != `ACCEPTED`, for any
    reason — not an aggregate rate drop, and not qualified by how the
    failure is classified (Lock-Readiness Response 3 §2 removed the
    classification-gated version of this rule after finding it too narrow).
    The original aggregate-rate framing below undercounted risk at n=6 by
    treating individual flips as informative context for a rate number
    rather than as the decisive signal themselves.
15. **Can a human baseline be information-equivalent enough for cost-benefit
    claims?** Not with the single-operator, no-blinding-guarantee-across-
    session-order design available to this pass — resolved by deferring the
    human baseline entirely for Tranche 1 (Design Options §3 Option B) and
    capping Tranche 1's conclusion ceiling accordingly (protocol §9).

## Recommendation

**Superseded by Hardening Pass 1** (`AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md`).
The three blockers this initial review raised have each been resolved there:
(a) T1 was re-verified against an actual clean, detached worktree at exactly
`0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`, which corrected the substrate
description (dropped the Skill-tool-vs-CLI candidate and the `build/`-based
triple-copy claim; confirmed a real, already-diverged dual-consumer
`workflow-registry.yaml` ambiguity instead); (b) the Tranche-2 indifference
band was frozen as a 10%/25% region rather than left open, with the
statistical-power reasoning for choosing a band over a point threshold
stated explicitly; (c) the three evaluator-judgment risks were each given an
explicit disposition — two remain genuinely non-mechanizable and are carried
forward as named, evidence-preserving residual risks (not silently resolved
away), and the third (the "obviously intended route" convergence gap) was
closed with a new `route_evidence_trace` telemetry field and scorecard note.
Hardening Pass 1 additionally froze the family-fallback rule this review had
left implicit (§ family-fallback in that document) and performed a regime-
separation diff, preflight review, and a re-run of the eight-agent
adversarial simulation against the changed areas only.

The paragraph and status line immediately below are retained for provenance
(the initial review's own conclusion, before hardening) and are superseded
by Hardening Pass 1's final status, not current guidance.

---

*Original recommendation (superseded):* The frozen SHA is real and confirmed
as an ancestor of this repository's current tip; the working tree this
design pass ran in is 85 commits ahead of it, so no executable step beyond
design has occurred against the actual frozen state, and none should until a
standalone clone at that exact SHA is prepared. T1 and T2 constructs are
grounded in real, pre-existing repository mechanisms and are admissible with
high confidence, modulo the noted frozen-SHA re-verification for T1. T3's
construct is real but its construction method is unproven, making it the
pilot's most important cell. The 20% threshold's replacement (an
indifference band for Tranche-2 activation) is the one design parameter this
pass deliberately leaves for a human to set rather than fixing unilaterally.

**ORIGINAL STATUS (superseded): CHANGES REQUIRED BEFORE HUMAN DRAFT REVIEW**

**CURRENT STATUS, per Hardening Pass 1: READY FOR HUMAN DRAFT REVIEW** — see
`AUTONOMOUS-TASK-V2-HARDENING-PASS-1.md` §Final summary for the full
resolution of each item and the residual risks that remain honestly
unresolved (T3's construction is mechanism-verified but not
execution-proven; two evaluator-judgment risks depend on run-time human
care, not just scoring).

**T2 vs. D/D' distinctness: CLOSED**, not open (corrected in
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-2.md` §10). The human reviewer
supplied the missing external fact directly: D/D' transformed a
`repository_sensemaking_brief` artifact while preserving an exact Evidence
region; this T2 works on the artifact-*contract declaration* surface
(`artifact-contracts.yaml`) and producer/consumer field agreement — related
by the broad "constrained transformation" idea but materially different
task instances and semantic substrates. Recorded as external-provenance
verification.

**Status reaffirmed after a subsequent, narrower pre-lock audit**: see
`AUTONOMOUS-TASK-V2-AMBIENT-ISOLATION-AUDIT.md`, a metadata-only inventory
of ~24 pre-existing sibling git worktrees sharing this repository's common
`.git` directory (several based on the same frozen SHA under different
experiment names). That audit found two concrete, previously-undetected
ambient-exposure vectors — parent-directory name enumeration and a
local-clone git-config remote-URL breadcrumb — fixed narrowly in
`AUTONOMOUS-TASK-V2-PREFLIGHT-GATE.sh` (three new, name-agnostic checks plus
an always-reported `AMBIENT_SCOPE_NOT_TECHNICALLY_ENFORCED` disclosure line).
No sibling worktree's contents were read. Status remains **READY FOR HUMAN
DRAFT REVIEW**; the residual, honestly-unclosed risk is that no bash-level
preflight can prove the live benchmark agent's filesystem access is actually
bounded to its assigned clone — that depends on execution-environment
sandboxing this repository's tooling cannot itself verify.

**Human review pass**: a reviewer with access to this report (but not yet
the underlying files) provisionally assessed the design as close to `READY
FOR PILOT LOCK`, contingent on closing four issues — most importantly,
post-pilot task-selection bias, which they judged capable of contaminating
the entire economic comparison while leaving every individual run
apparently valid. All four blocker-level issues and five non-blocker
preregistration items from that review are resolved in
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE.md`. Final lock authorization
is explicitly reserved for that reviewer's own line-by-line pass against the
uploaded artifact bundle, not asserted here.

**Line-by-line lock review, actual bundle inspected**: the reviewer then
directly inspected the uploaded 14-file bundle (not a summary) and returned
`CHANGES REQUIRED BEFORE PILOT LOCK` with 11 numbered findings — 7 flagged
as lock-level blockers, including two remaining gaps in the candidate-pool
selection mechanism itself (author-selection independence; Tranche 2 had no
frozen source), a genuine measurement flaw in the execution-phase cost
formula (didn't account for static-context repetition across multi-turn
model calls), a human-minutes/USD mixing contradiction, and a real code-level
gap in the T3 recovery construct (the ledger-audit substrate previously
verified is not the same file the actual `resume=True` code path reads).
All are addressed in
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-2.md`, including one additional
finding this pass made on its own while investigating the reviewer's T3
question (re-reading `workflow-runtime.py`'s actual resume code, not just
its audit code, found the real interrupt mechanism must be a `gate: review`
pause, not a process kill). Final lock authorization remains with the
reviewer's own re-inspection of the corrected bundle.

**Second line-by-line lock review**: the reviewer re-inspected the
corrected (15-file) bundle directly and again returned `CHANGES REQUIRED
BEFORE PILOT LOCK`, this time with the headline finding that the `gate:
review` mechanism from the previous pass was itself broken — traced,
correctly, to `resume_skip.add(paused)` unconditionally folding a `PAUSED`
step (gate left unapproved OR explicitly denied) into the skip set,
bypassing the approval boundary rather than testing recovery from it. This
pass independently re-verified that finding against the frozen SHA before
accepting it, and located a different, genuinely-working code path
(`FAILED` status via validator failure, confirmed absent from both
`completed_steps` and the paused-step handling, so it is legitimately
retried on `--resume`) — T3 is corrected a second time rather than dropped.
The review's other nine findings (H1 still too narrow; the Tranche-2 rule's
internal contradiction; T1/T2's oracle-spec pool gap; stale T3 prose
surviving the first correction; R2 not literally byte-identical to R1;
cache-attribution risk in the dynamic-cost formula; unspecified human-
attention timing boundaries; manual repair able to retroactively create
`ACCEPTED`; and six mechanical consistency items) are all addressed in
`AUTONOMOUS-TASK-V2-LOCK-READINESS-RESPONSE-3.md`. Final lock authorization
remains with the reviewer's own re-inspection of the twice-corrected
bundle.
