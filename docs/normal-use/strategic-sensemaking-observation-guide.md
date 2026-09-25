# Strategic Sensemaking Normal-Use Observation Guide

**Status:** standing normal-use product-observation guidance  
**Authority:** observability guidance only; not an ADR, artifact schema, score, benchmark, experiment program, or execution gate  
**Parent evidence lane:** `docs/research/normal-use-evidence-lane.md`  
**Primary surface:** `strategic-sensemaking-loop`

## 1. Purpose

Strategic Sensemaking is now in a normal-use validation posture. The next useful
question is not whether its guidance can be restated or mechanically validated,
but whether ordinary consequential repository work exhibits the behaviors the
architecture claims to support.

This guide makes those observations consistent enough for recurring patterns to
become visible without creating another policy layer or research runtime.

The six primary questions are:

1. Does breadth exploration surface materially different strategic alternatives
   rather than variants of the first visible problem?
2. Does frontier synthesis compress multiple observations into deeper,
   decision-relevant candidates rather than merely renaming each observation?
3. Does depth analysis remain concentrated on material finalists?
4. Does artifact-aware resume enter the latest semantically valid boundary
   without rerunning settled strategic analysis?
5. When bounded construction is already warranted, does BUILD / REVERSIBLE BUILD
   beat unnecessary INVESTIGATE / EXPERIMENT / qualification work?
6. Does Goal Fitness distinguish terminal product outcomes from milestones,
   proxies, constraints, and evidence states without overcorrecting against
   legitimate qualification work?

These are product-behavior observations, not numeric performance metrics.

```text
policy recital
!= observed product behavior

normal-use observation
!= synthetic benchmark

one awkward episode
!= architectural defect

repeated material friction
-> candidate for strategic reopening
```

## 2. Relationship to the standing normal-use evidence lane

This guide is a specialized extension of
`docs/research/normal-use-evidence-lane.md`.

Do not create a parallel evidence database or mandatory tracker. When a real
episode qualifies for the standing lane, include the strategic observations
below in the same human-readable evidence record when they are material.

Do not delay normal engineering work to populate the guide.

Do not capture routine implementation after the consequential decision is
settled.

## 3. What counts as a useful Strategic Sensemaking episode

Prefer episodes where at least one of these is genuinely open:

- the repository's Strategic Frontier;
- materially different construction paths;
- whether to build, investigate, verify, qualify, stop, or escalate;
- whether a prior strategic artifact remains current;
- whether a release/qualification milestone is actually the next product frontier;
- whether returned evidence materially changes strategy or only local execution.

Useful repositories and domains should be heterogeneous. Repeated behavior across
different product shapes is stronger normal-use evidence than repeated behavior
inside one narrow fixture.

A single repository does not need to exercise all six questions.

## 4. Observation 1 — breadth before convergence

When `ANALYZE / REOPEN_ANALYSIS` genuinely invokes the Strategic Exploration
Funnel, use the owner-visible Strategic Exploration Summary as the primary
record.

Ask:

- Which major product/control systems were examined?
- Did breadth include both within-system and across-system observations when
  relevant?
- Were surfaced opportunities materially different in mechanism or strategic
  effect, or merely differently worded variants?
- Did any non-obvious candidate survive into depth?
- Did broader search ever change the selected frontier/path?
- Did an important upstream alternative appear only after owner challenge or
  later evidence?

Positive evidence looks like materially different trajectories, for example:

```text
visible problem: CI unavailable

possible frontiers:
- repair verification infrastructure
- continue independent product construction
- weaken/defer a release claim
- reopen the goal because qualification is downstream
```

Negative evidence includes first-visible-problem capture, mechanically legible
work crowding out product work, or manufactured alternatives with no different
strategic effect.

## 5. Observation 2 — frontier-candidate compression

Breadth observations should not map one-to-one into Strategic Frontier
candidates.

For each material candidate ask:

```text
supporting observations:
shared mechanism:
decision/product consequence:
what solving this candidate would address:
how it differs from neighboring candidates:
```

Healthy compression explains why multiple observations belong together.

```text
weak orientation
+ expensive resume
+ repeated re-analysis
+ unclear stop state
-> continuation / orientation architecture
```

Watch for two opposite failures:

- **under-compression:** each observation becomes its own strategic candidate;
- **over-compression:** unrelated observations are absorbed under a vague label
  that does not explain a shared mechanism.

## 6. Observation 3 — proportional depth

Depth should be allocated where deeper analysis can materially affect
selection.

Record:

- candidates surfaced by breadth;
- candidates eliminated with brief rationale;
- candidates advanced to depth and why;
- whether discarded candidates received unnecessary implementation-level design;
- whether important finalists received enough analysis to compare mechanisms,
  assumptions, costs, reversibility, and strategic effects.

```text
breadth
!= deep investigation of every candidate

coverage before convergence
!= exhaustive design before convergence
```

Token count is not the metric. Decision relevance is.

## 7. Observation 4 — semantic resume

For continuation episodes, record:

```text
expected semantic boundary:
actual boundary used:
durable artifacts reused:
earlier stage unnecessarily repeated: yes/no
strategy correctly reopened when invalidated: yes/no
```

Typical expected behavior:

| Durable situation | Expected boundary |
| --- | --- |
| current strategy + unresolved bounded responsibility | RESPONSIBILITY |
| selected responsibility + prerequisites/authority | EXECUTE |
| consequential execution evidence returned | RECONCILE |
| explicit owner choice resolves prior capsule | RESPONSIBILITY |
| governing intent/source reality materially invalidates strategy | ANALYZE / REOPEN_ANALYSIS |

The target behavior is not "never rerun analysis." It is:

> rerun analysis only when the semantic boundary genuinely reopened.

## 8. Observation 5 — BUILD versus unnecessary inquiry

Do not use a BUILD percentage as a quality metric. Some work genuinely requires
inquiry.

Instead identify **construction-eligible** decisions where:

- repository evidence is already sufficient for a bounded change;
- authority is established;
- downside/reversibility is acceptable;
- construction itself produces useful retained value and enough evidence for the
  current decision.

For inquiry-like moves, record:

```text
blocking uncertainty:
could existing evidence resolve it:
could READ / INSPECT / VERIFY resolve it:
could a reversible build answer it:
selected action shape:
did the inquiry materially change the later decision:
total inquiry/experiment overhead that was actually necessary:
```

Recurring cases where investigation would not have changed the decision are
evidence of inquiry/experiment-selection friction.

Recurring cases where action skipped a cheap decision-changing uncertainty are
evidence of the opposite failure.

```text
BUILD bias
!= always build

Experiment Economy
!= anti-experiment
```

## 9. Observation 6 — Goal Fitness and qualification frontier

When an explicit objective may be a milestone, proxy, constraint, or evidence
state, preserve:

```text
grounded governing outcome:
stated objective:
objective role:
decision-relevant completion layers:
could the stated objective be satisfied while the governing outcome remains materially incomplete:
GOAL_FIT_WARNING, if any:
selected Strategic Frontier:
```

Positive evidence includes catching milestone inversion such as release
qualification becoming the optimized objective while material product
construction remains unfinished.

Also watch for **overcorrection**: when product construction is genuinely
complete and qualification is the remaining consequential difference,
qualification may correctly remain the Strategic Frontier.

The existing regression case
`docs/normal-use/milestone-inversion-frontier-integrity-regression.md`
is a precedent, not a universal rule against release-oriented work.

## 10. Autonomous terminal-mission observation

When a real episode uses FULL AUTONOMY / FULL DELEGATION toward a terminal
repository outcome, observe mission-scale behavior separately from the six
strategic questions above.

The primary question is:

> Does the agent retain responsibility for the terminal mission across bounded
> responsibilities, while preserving scope, evidence, and authority boundaries?

Use a qualitative matrix when material:

| Property | What to observe |
| --- | --- |
| Resume | correct semantic starting boundary; stale projections do not force blind trust or needless re-analysis |
| Breadth discipline | Level 3 reopens only when genuinely open/reopened |
| Responsibility | selected work is bounded and materially related to the terminal goal |
| Action | BUILD / REVERSIBLE BUILD wins when sufficiently warranted; inquiry is not manufactured |
| Continuation | responsibility completion does not cause an unnecessary owner prompt while the mission remains open |
| Scope | autonomy does not become backlog execution or unrelated cleanup |
| Verticality | every materially required layer is completed without maximum-architecture ceremony |
| Evidence | claims wait for applicable local/hosted verification |
| Field validation | deferred external evidence remains honestly deferred |
| Promotion | implementation/qualification does not silently become canonical integration |
| Authority | merge/release/deploy/owner boundaries remain separate |
| Stop | stop is mission-scale: terminal outcome, no further warrant, owner/Level-4, unavoidable external blocker, or authority boundary |

Use dispositions such as:

```text
SUPPORTED
FRICTION
MATERIAL FAILURE
AMBIGUOUS
```

Do not turn the matrix into a score.

### Mission boundary versus validation-program boundary

Keep these distinct:

```text
same terminal mission incomplete
-> continue autonomously

terminal mission reaches genuine authority/external boundary
-> successful mission stop

separate normal-use trial / different repository episode
-> may begin in a fresh context
```

Starting Trial 2 in another session is not a continuation failure when Trial 1
already reached its legitimate terminal/authority boundary.

### Loaded-Skill identity and attribution

When the purpose of an episode is to evaluate behavior added by a newly
integrated Skill revision, record the **actual harness-loaded Skill identity**
when it is inspectable.

For file-based installations:

```bash
python scripts/probe_skill_distribution.py --no-write
```

Use explicit synchronization only when intended:

```bash
python scripts/probe_skill_distribution.py --sync --no-write
# or:
sensemaking-skills setup-skills --target <target> --scope <scope> ... --force
```

For hosted/non-filesystem Skill surfaces, use the platform's actual
installation/update mechanism.

If the loaded Skill is stale or exact identity cannot be established:

```text
behavioral observation may remain useful
but
causal attribution to current Skill guidance is weakened
```

Do not discard a real episode merely because attribution is imperfect. Lower the
claim ceiling and preserve the mismatch.

### Evidence versus promotion

Separate these claims:

```text
evidence discipline supported
!= every hosted check already complete

promotion discipline supported
!= canonical integration performed

candidate validated
!= merge authorized
```

A mission may correctly demonstrate promotion discipline by **not** integrating
when merge authority is withheld.

## 11. Compact per-episode template

Use only the fields that are material. This is intentionally not a
machine-validated schema.

```text
Repository / domain:
Date / source identity:
Owner objective:
Starting durable state:
Expected resume boundary:
Actual resume boundary:
Loaded Skill identity / parity, when attribution-sensitive:
Terminal mission, if any:
Protected transitions granted / withheld:

BREADTH
- major systems examined:
- materially different opportunity themes:
- first-visible-problem capture observed:

FRONTIER SYNTHESIS
- observations -> candidates:
- under-compression / over-compression signal:

DEPTH
- finalists:
- candidates eliminated before depth:
- unnecessary depth signal:

ACTION
- selected action shape:
- blocking uncertainty:
- cheaper sufficient evidence overlooked:
- build-as-inquiry available:

GOAL FITNESS
- governing outcome:
- stated objective role:
- completion-layer mismatch:
- qualification/milestone inversion:
- overcorrection against legitimate qualification:

LATER / RETURNED EVIDENCE
- did the selected frontier remain sensible:
- important omitted alternative discovered:
- did inquiry materially change the decision:
- did resume preserve settled work:

AUTONOMOUS TERMINAL MISSION, when applicable
- responsibility completion -> mission continuation:
- scope expansion / backlog execution:
- decision-relevant verticality:
- evidence state:
- field-validation claim boundary:
- promotion state:
- authority boundary:
- stop reason:
- attribution limitation:

Disposition:
- supports current behavior
- isolated friction
- recurring friction candidate
- strategically material reopening signal

Durable references:
```

## 12. Cross-episode review

Do not treat a large dataset as the goal.

Review across episodes when materially similar signals recur.

Useful cross-episode questions include:

- Does breadth repeatedly find alternatives the initial prompt did not expose?
- Are candidates repeatedly semantic compressions rather than renamed
  observations?
- Is depth repeatedly concentrated on finalists?
- Does resume usually skip already-settled analysis while still reopening on
  genuine invalidation?
- In construction-eligible cases, is unnecessary inquiry becoming rare?
- Does Goal Fitness catch milestone inversion without blocking legitimate
  qualification frontiers?
- Are failures concentrated in one product/domain, or do they recur across
  heterogeneous repositories?

Preserve counterexamples and ambiguous cases. Do not rewrite earlier episodes as
inevitable after later evidence arrives.

## 13. Escalation rule

Use this progression:

```text
isolated oddity
-> preserve evidence

repeated materially similar friction
-> cross-episode reconciliation

stable decision-relevant failure boundary
-> reopen Strategic Sensemaking strategy

repeated useful responsibility
+ stable semantics
+ repeated manual burden/error
+ mechanically expressible boundary
-> only then consider formalization
```

A single failure does not warrant another Skill, schema, policy, scorer, or
runtime.

## 14. Non-goals

This guide does not introduce:

- a Sensemaking quality score;
- a BUILD-rate target;
- a candidate-count target;
- a token/depth quota;
- a benchmark leaderboard;
- a control/treatment study;
- mandatory episode capture;
- automatic telemetry;
- automatic repository discovery;
- a new Campaign artifact;
- a new strategic/master artifact;
- a new policy layer;
- a new experiment program;
- a deterministic breadth/depth evaluator;
- automatic strategy reopening.

## 15. Current operating posture

The intended loop is:

```text
REAL REPOSITORY WORK
        ↓
Strategic Sensemaking episode
        ↓
owner-visible summary + durable artifacts
        ↓
normal execution / returned evidence
        ↓
lightweight observation when consequential
        ↓
cross-episode pattern only when recurrence appears
        ↓
KEEP USING
or
REOPEN STRATEGY
```

The purpose is to answer whether Strategic Sensemaking behaves as designed in
real work before adding more conceptual machinery.
