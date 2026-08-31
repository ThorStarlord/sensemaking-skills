# OBSERVATIONS (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Running log. **Construction-phase entries are frozen with V0.** Entries after
the freeze line are evaluation observations and are appended, not edited.

Value-observation codes (authorization Section 19):
A previously-obscure relationship becomes immediately visible ·
B historically expensive discovery becomes a cheap query ·
C impact analysis more complete ·
D semantic-authority conflict becomes explicit ·
E stale/superseded state easier to identify ·
F repeated rediscovery avoided ·
G a consequential interpretation changes ·
H no advantage — raw inspection equally necessary ·
I V0 actively misleads.

Grade codes as in `00-PROTOTYPE-SCOPE.md`.

---

## CONSTRUCTION PHASE

### C-1 — Most consequential relationships already exist in prose, scattered
`CONTEXT.md` + `docs/agent-native-operating-workflow.md` between them already
carry ~70% of what `02`/`04`/`05` represent — but as three prose views
(`AGW:33` explicitly says modeling one hides the architecture). Turning them
into typed, cross-linked, individually-evidence-graded edges took real work but
discovered little *new* at the top level. The friction was **assembly**, not
**discovery**. (Bears on primary question C: much of the persistent-doc content
would be *re-indexed*, not *revealed*.)

### C-2 — The authority + validation views are where construction found new things
Building `05-AUTHORITY-MAP.md` and `06-VALIDATION-MAP.md` surfaced items that
are *not* stated together anywhere:
- a **DEPRECATED** contract file (`workflow-orchestrator/references/artifact-contracts.yaml`)
  is the *sole* home of 4 live contracts (`E-CONTRACT-dupe-header`). "No code
  should read this file" + "these 4 contracts live only here" are 13 lines
  apart but their *contradiction* is only visible when you ask "who enforces
  the `prd` contract?" — code A, grade DEMONSTRATED.
- two `workflow-registry.yaml` copies with **real content drift** and no parity
  check among 21 validators (`E-WFREG-dupe`) — code A, grade DEMONSTRATED.
- the `repository_sensemaking_brief` contract has **5 defining sources and 2
  enforcers** with a deliberate generic/conditional split; no single file says
  this — code C, grade DEMONSTRATED.

### C-3 — "Impl ahead of policy / policy ahead of impl" is a productive column
Adding a POLICY-vs-IMPL column to `05` forced a judgment on every seam and
produced the clearest single finding: **automatic fog-type routing** is the
largest impl-ahead-of-policy gap (runtime + registry can do it; ADR 0014/0018/0026
+ CONTEXT.md refuse to ratify it). This is stated in ~4 places individually;
the *ranking* of it as #1 divergence is new — code C/G, grade DERIVED.

### C-4 — Epistemic grading was cheap and disciplining
Marking every edge DEMONSTRATED / DERIVED / INTERPRETIVE / HYPOTHESIS cost
almost nothing and repeatedly caught me about to assert an INTERPRETIVE claim
(e.g. "SKILL.md defines producer behavior") as DEMONSTRATED. Low cost, real
value. Candidate for "always" representation.

### C-5 — Research-claim map mostly re-indexes existing discipline
`07` was fast to build because **every live claim already has a written
ceiling** ("what this does NOT claim" sections everywhere). The structured map
makes ceilings *queryable* and makes the single load-bearing edge (RC-1 -> the
opt-in warrant seam) obvious, but it *discovered* nothing — the repo's research
hygiene is already high. Code F (future rediscovery avoided) but not B. Bears
on question C.

### C-6 — Component granularity was the hardest modeling call
Deciding what is "a component" (a skill? a script? a package subdir? a doc?) has
no repository-given answer. I used *semantic responsibility* as the unit, which
put `CONTEXT.md` and `probe_relationships.py` at the same level. This is
`INTERPRETIVE` and a reviewer could reasonably redraw it. Friction: high.
Redundancy risk: enumerating all 21 validators individually adds size without
insight, so `02` collapses them to `validator.other-specialized`.

### C-7 — What was unexpectedly difficult
- **Path resolution semantics** (`_resolve_artifact_path` / `expected_output_path`)
  are load-bearing (ADR 0010) but only legible by reading ~40 lines of runtime
  across 3 call sites. Representing the *relation* ("runtime OWNS path,
  executor RECEIVES it") is easy; verifying it required real code reading.
- **The MODEL_WARRANT seam being opt-in.** The authorization's flow treats it as
  a pipeline stage. Establishing "it's `warrant_enabled`, off by default, after
  validator PASS" needed `grep` + reading `L1438-1473` + `L1831-1857` of the
  runtime. A rich representation that just said "brief -> MODEL_WARRANT -> route"
  would have been code I (misleading).

### C-8 — No infrastructure was built or needed
Plain Markdown + YAML instantiated the whole representation. At no point did a
graph DB / query engine / index feel necessary to *construct* V0. Whether one
is needed to *use* it repeatedly is a separate question for evaluation.

### C-9 — Approximate construction cost
~18 targeted repository reads/greps (git state, CONTEXT.md, AGW,
artifact-contracts.yaml, ADR statuses + 0014/0026, both registry pairs, runtime
head + routing internals, probe engine, warrant gate, gate_a, research agenda,
PHB artifacts, skill/src trees). ~11 authored artifacts. No dead ends that
required rework. The dominant cost was *reading enough to grade an edge
DEMONSTRATED rather than INTERPRETIVE*.

---

## FREEZE LINE — DETAILED_ARCHITECTURE_V0_FROZEN = true as of V0-FREEZE-MANIFEST.md

## EVALUATION PHASE
(entries appended during retrospective challenges `11` and decision views `09`)
