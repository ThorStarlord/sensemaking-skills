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

### E-1 — Authority seam table was used in every prospective view
`05-AUTHORITY-MAP.md`'s DEFINES / ENFORCES / RUNTIME-OWNS / WINS-ON-CONFLICT /
POLICY-vs-IMPL row shape was consulted for `09` Q1, Q2, Q3, Q5, Q6, Q7 and
`11` RC#1, RC#2, RC#4, RC#5, RC#6. Code C/D. Highest-use element in V0.

### E-2 — POLICY-vs-IMPL column produced the sharpest single finding
Ranking automatic fog-type routing as the #1 impl-ahead-of-policy divergence
(`09` Q5, `11` RC#5) is not stated as a ranking anywhere in the repo; it is
assembled from ADR 0014 + 0018(SUPERSEDED) + 0026 + CONTEXT.md:127/335 +
registry flags + runtime chain. Code C/G, grade DERIVED.

### E-3 — Cross-cutting impact analysis (09 Q6) is the one hard-to-recover capability
Enumerating the ~9-node blast radius of a `representation_sufficiency` semantics
change spans 4 relationship families (authority, artifact, research, structural).
A human doing this from raw sources would plausibly miss the
`infra.reasoning-slice DERIVES_FROM research-agenda` edge or the
`validate-brief.py` parse. Code C. But this is question-specific — an on-demand
projection, not a standing document (feeds `12` Q8/Q9).

### E-4 — RC#6 (deprecated-file-is-canonical) is the clearest "V0 earned its keep"
The contradiction spans two files and is only visible when you ask "who enforces
the `prd` contract?" — V0 pre-assembled that question + answer in `06` §2. Code A,
grade DEMONSTRATED.

### E-5 — RC#3 exposed V0's floor: it does not enumerate validator rules
The `Lx`-format-with-no-consumer episode is NOT_REPRESENTED at rule level; V0
only carries the governing *principle*. Confirms V0 is a map to the right file +
question, not a substitute for the file. Code H at rule granularity.

### E-6 — RC#7 exposed a staleness/over-read risk
Showing the reconciliation fan-in as "resolved" without foregrounding that
cross-run prior-report identity is still `CONVENTION` risks code I (mislead by
omission). Mitigated only if the reader reaches the `04` session_summary row.

### E-7 — Most of V0 decays fast
`02` (ADR statuses, counts), `07` (evidence-class rungs, issue numbers), and the
SHAs throughout are time-stamped to `ba8968c`. The 6 commits since the
authorization SHA already moved the research surface. A persisted rich V0 would
need continuous refresh; the thin core (authority seams, lifecycle, enforcement
gaps) changes far more slowly. Feeds `12` finding #4 and the disposition.

### E-8 — No infrastructure was needed to USE V0 either
Every prospective view and challenge was answered by reading the frozen Markdown/
YAML directly. No index, query engine, or graph store was reached for. (The
cross-cutting Q6 trace was done by hand across 4 files — tedious but not
blocked.)

### E-9 — ERRATUM: EVIDENCE-INDEX.yaml does not parse as strict YAML (frozen; NOT corrected)
Post-freeze `yaml.safe_load` found 5 lines in `EVIDENCE-INDEX.yaml` of the form
`E-CONTRACT-brief-notes:{kind: ...}` — a missing space after the key colon, so
the file is not strict-YAML-parseable (lines 91, 93, and 3 others; `02` and `03`
parse cleanly). Per freeze rule (authorization Section 14) the frozen bytes are
**left unchanged** — this is a mechanical typo, not an architecture change, and
V0 is historical evidence "as built." The file remains fully human-readable and
every evidence id resolves by eye.
**This is itself a finding:** hand-authoring flow-mapping YAML for a rich
representation is error-prone (construction friction, feeds `12` finding #6 and
the disposition toward *generated projections* over hand-maintained rich files).
A V1 core should be tables or machine-generated, not hand-written nested YAML.

## FREEZE-INTEGRITY NOTE
Frozen artifacts (00-08, 10, EVIDENCE-INDEX) were not edited after
`V0-FREEZE-MANIFEST.md`. `09`, `11`, `12` are post-freeze evaluation outputs.
This file's construction-phase section (above the FREEZE LINE) is unchanged;
only the EVALUATION PHASE section was appended to.
