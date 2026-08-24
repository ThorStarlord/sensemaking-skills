# Autonomous Task v2 — Design Options

Status: DRAFT — design-only, not locked. No pilot or main-study tasks have been
constructed from this document.

Frozen repository under study: `ThorStarlord/sensemaking-skills` at
`0ffb564b67eb7fcac3c1a2c8a1365ed6b2a0e6c5`. Prior Autonomous Task experiment
history (v0.1 feasibility, v1 admissibility closure, v2.1 judgment lessons
M1-M4) is external research provenance supplied to this design task, not an
artifact expected to exist inside this repository — see
`AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §0 for how that provenance is used.

This document compares options in five areas and records the selected option
with its rationale. Rejected options are kept because the rejection reasoning
is itself a design constraint for later phases.

---

## 1. Experimental-regime design

### Option A — Three discrete regimes (R0 Robust / R1 Lean / R2 Escalation), same task/oracle, differing only in execution-discipline instructions

Each regime is a fixed prompt overlay applied to an identical task-visible
contract. Differences are procedural (how much investigation, how many
validation passes, whether one bounded escalation is permitted) — never
differences in the goal, the oracle, or the information available about the
repository.

**Pros**: clean paired comparison; isolates protocol effect from task effect;
matches the requested primary matrix (6 tasks x 3 regimes = 18 runs).
**Cons**: three regimes x six tasks is already 18 runs before any pilot;
regime "leanness" is itself hard to keep genuinely equivalent in information
content (see §2).

### Option B — Continuous dial (single regime, agent self-reports a chosen effort level 1-5)

Instead of fixed regimes, the agent is told its efficiency budget is its own
judgment call, and the analysis regresses cost against self-reported effort.

**Pros**: fewer frozen artifacts; potentially captures a natural frontier
rather than three arbitrary points.
**Cons**: self-reported effort is not an experimental treatment — it's a
confound with whatever produced the agent's behavior that run (model
variance, task-order effects, mood of the sampling). It would not let H2
("LEAN reduces cost without reducing efficacy") be tested as a controlled
comparison, only observed as a correlation. This directly reintroduces the
M1-style route/mechanism ambiguity lesson: an uncontrolled variable posing as
a measured one.

**Selected: Option A.** A discrete, frozen, paired-per-task regime design is
the only one of the two that supports the confirmatory hypotheses (H1, H2) as
stated. Option B is noted as a plausible *exploratory* follow-up once R0/R1
telemetry exists, not a substitute for the controlled comparison.

---

## 2. Cost-accounting design

### Option A — Charge every run for its full input context, including task bundle and regime prompt, with regime-prompt tokens tracked as a separate line item

All tokens the agent actually consumes (system context, task bundle, regime
instructions, tool results) count toward "agent resource cost." Regime-prompt
length is logged separately so a reviewer can check whether LEAN looking
cheaper is *merely* an artifact of a shorter prompt.

**Pros**: honest — the deployed cost of running an agent includes its
instructions; hiding regime-prompt tokens would make LEAN look artificially
cheap by fiat rather than by behavior.
**Cons**: requires care in the telemetry schema to keep "prompt-only" cost
separable from "investigation-driven" cost, otherwise H2 could be confirmed
for the wrong reason (design question 2 in the protocol draft names this
directly).

### Option B — Charge only cost incurred *after* the regime prompt is delivered (treat regime instructions as free, amortized infrastructure)

Only tool calls, model turns spent reasoning/acting, and output tokens count.
The regime prompt itself is treated like a system prompt that "doesn't count"
because it's fixed infrastructure, not task work.

**Pros**: simpler; avoids double-counting a fixed constant across every run
of a regime.
**Cons**: silently exempts the exact quantity (prompt length/complexity)
whose confound the protocol is required to rule out. This is a direct route
to `EFFICIENCY_BY_UNDERVERIFICATION`-adjacent gaming: a LEAN regime could win
purely by having a terser prompt while producing equivalent or worse
verification behavior once running, and Option B would never surface it.

**Selected: Option A.** Full-context accounting with a separate regime-prompt
line item. This directly answers design question 2/3 in the protocol draft:
task-bundle tokens are counted in every run (constant across regimes, so they
cancel in the paired comparison); regime-prompt tokens are counted and
reported separately so a reviewer can verify H2 survives with that line item
excluded, as a robustness check.

---

## 3. Human-baseline design

### Option A — Single blinded human completes all six held-out tasks, sequentially, with no visibility into agent trajectories, oracle, or evaluator routes

One consistent human, timed per task, gives a within-subject baseline that
minimizes between-human variance (the protocol draft explicitly favors this
per the original design brief).

**Pros**: matches the requested design; reduces a major variance source
(different humans have wildly different task-specific tacit knowledge of this
repository).
**Cons**: n=1 human is a severe external-validity limitation; ordering
effects (task 6 benefits from having done tasks 1-5 in the *same* repository,
which the agent runs do not get — each agent run is a fresh session per
`AUTONOMOUS-TASK-V2-PROTOCOL-DRAFT.md` §Main Matrix). This is exactly the
`HUMAN_BASELINE_INFORMATION_ADVANTAGE` failure mode.

### Option B — No human baseline collected; only cross-regime autonomous comparison performed

Skip human timing entirely for v2's first tranche; treat cost-benefit
(`r*` break-even) as a deferred, optional follow-up.

**Pros**: removes a real recruitment/scheduling dependency and the n=1
validity problem entirely; keeps the study's confirmatory claims narrow and
achievable with resources actually available to this design task.
**Cons**: forfeits H3/H4's strongest form ("autonomy becomes preferable to
human execution above rate `r*`") — the study can only report
`AUTONOMOUS-PROTOCOL-EFFICIENCY-IMPROVED`-class conclusions, never
`POSITIVE_ECONOMIC_SIGNAL`.

**Selected: Option B, with Option A specified as an optional add-on module.**
No credible single blinded human operator is available to this design task
(no scheduling access, no ability to guarantee blinding under the
same-repository within-subject conditions Option A needs). Per the protocol
brief's own instruction ("if a credible human baseline is unavailable, that's
okay — but the conclusion must stop at autonomous-protocol efficiency
improved"), Tranche 1 is designed to run *without* a human baseline. The
break-even formula (`r* = A / (Sh - Sa)`) and Option A's design are fully
specified in the protocol draft as a ready-to-activate module for whoever
does have a credible operator, but Tranche 1's own hypotheses (H1, H2, H3,
H5) do not depend on it.

---

## 4. Complexity rubric

### Option A — Structural point-count rubric (sum of five weighted factors: repository surfaces, plausible routes, invariants, execution stages, validation conditions), MEDIUM = 5-8 points, HIGH = 9+

A task instance is scored before construction by counting, e.g., how many
files it plausibly touches, how many mechanisms could be mistaken for the
correct one, how many hard invariants must hold, how many stages of
work/validation are required. MEDIUM/HIGH is a threshold on the sum.

**Pros**: auditable, constructed *before* any agent runs it (satisfies "do
not define complexity by expected runtime"); directly reusable across T1/T2/T3
since the five factors are family-agnostic; supports H4 (complexity-dependent
break-even) because the score is an independent variable set at design time.
**Cons**: factor weights are somewhat arbitrary; two designers could score
the same task differently by +/-1 point near a threshold boundary.

### Option B — Ordinal family-specific rubric (each task family defines its own MEDIUM/HIGH criteria in family-native terms, e.g. T1: "1 wrong route" vs "2+ wrong routes"; T3: "no reconciliation needed" vs "reconciliation across 2+ artifacts needed")

Each family gets a bespoke two-level ladder tuned to what actually varies in
that family's construct, without forcing a shared numeric scale.

**Pros**: avoids false precision from a shared point count that doesn't mean
the same thing across three very different constructs; easier for a designer
to apply consistently within one family.
**Cons**: MEDIUM(T1) and MEDIUM(T2) are not comparable in any strict sense,
which weakens any pooled complexity-level analysis (H4 would only be
testable within-family, not pooled).

**Selected: Option A, with Option B's per-family concreteness folded in as
the *definition* of each factor.** `AUTONOMOUS-TASK-V2-TASK-CONSTRUCTION.md`
uses the five-factor structural rubric as the scoring mechanism, but each
factor is given family-specific worked examples (grounded in this repo's
actual surfaces — see that document) so scoring is not abstract. H4 is then
tested primarily *within* family (3 families x MEDIUM-vs-HIGH pairs) with a
pooled analysis reported only as exploratory, which resolves design question
13/14 without pretending six tasks support a strong pooled claim.

---

## 5. Tranche-2 activation

### Option A — Statistical-ambiguity trigger: activate Tranche 2 only if Tranche 1's paired H2 comparison is not clearly resolved in either direction (effect size within a preregistered indifference band, e.g. |median reduction| < 10%) AND no instrument-validity failure explains the ambiguity

Tranche 2 exists to add precision to a genuinely unresolved signal, not to
rescue a disliked result.

**Pros**: matches the brief's explicit instruction ("must not be activated
merely because Tranche 1 produced an undesirable answer"); ties activation to
a frozen, falsifiable numeric band decided before Tranche 1 runs.
**Cons**: with n=6 paired tasks, confidence intervals are wide enough that
"ambiguous" could describe a large fraction of plausible outcomes, making the
trigger fire often — this needs to be stated honestly rather than treated as
a rare escape valve.

### Option B — Fixed two-tranche design (both tranches are pre-committed regardless of Tranche 1 outcome; 36 runs planned from the start)

Skip the conditional activation logic; run Tranche 2 unconditionally to reach
n=12 pairs, which meaningfully improves statistical power over n=6.

**Pros**: better-powered from the outset; avoids the appearance of
outcome-contingent data collection entirely (no possible accusation of
"we kept sampling until it looked significant").
**Cons**: doubles the resource commitment (36 vs. potentially 18 runs) before
any evidence that the instrument itself works; contradicts the brief's
explicit request for a *sequential* design that can stop early when the
answer is already clear.

**Selected: Option A**, with the indifference band and its width treated as
the single most important number to get right in preregistration — flagged
as an open item in `AUTONOMOUS-TASK-V2-DESIGN-REVIEW.md` (design question 13)
rather than picked arbitrarily here. A secondary activation path is also
specified: instrument-validity failure in >=2 of the 18 Tranche-1 runs
(oracle invalid, isolation breach, harness unstable) triggers a *repair-then-
repeat* path distinct from Tranche 2 — repairing the instrument is not the
same event as adding statistical power, and the protocol keeps them visibly
separate so a reviewer can't mistake one for the other.
