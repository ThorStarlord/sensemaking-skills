# Strategic Exploration Funnel v1 — Handoff

**Status:** COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF  
**Issue:** #468 — Strategic Exploration Funnel v1 — explicit breadth-to-depth repository analysis  
**Feature PR:** #469 — feat: add Strategic Exploration Funnel v1  
**Feature head:** `7d1535db56d3afb2d8a104fb8e7a522671783e78`  
**Integrated merge:** `b91c8f3a4c19dee259d2dcbcb60ff2d0eed82029`  
**Date:** 2026-09-24

## 1. Why this package existed

Normal-use Strategic Sensemaking showed that the repository already had the
ingredients for broad strategic search — current-system modeling, capability
maps, Strategic Frontier formation, Strategic Hypothesis Admission,
orthogonality challenge, path synthesis, and qualitative comparison — but the
breadth→depth funnel remained too implicit.

That created two product risks:

1. the agent could converge on the first visible or mechanically legible problem
   before deliberately scanning the wider repository opportunity landscape;
2. the owner could be told that alternatives were considered without seeing a
   compact representation of the breadth→candidate→depth funnel.

The package makes coverage-before-convergence explicit while preserving
artifact-aware resume and avoiding repeated whole-repository analysis during
settled execution/verification.

## 2. Integrated behavior

### Strategic Exploration Funnel

At a genuine Level-3 `ANALYZE` or `REOPEN_ANALYSIS` boundary,
`strategic-repository-analysis` now follows:

```text
FULL REPOSITORY / GOVERNING INTENT
        ↓
SYSTEM MAP
        ↓
BREADTH EXPLORATION
        ↓
FRONTIER CANDIDATE SYNTHESIS
        ↓
DEPTH DRILL
        ↓
CONSTRUCTION PATH SYNTHESIS
        ↓
COMPARATIVE SELECTION
        ↓
BOUNDED RESPONSIBILITY / DISPOSITION
```

The system map is a product/control-system decomposition, not a file inventory.

Breadth exploration deliberately searches:

- within major systems for missing capability, incomplete product promises,
  simplification, autonomy, underused leverage, and adjacent value;
- across system boundaries for semantic/information loss, authority loss,
  duplicated responsibility/state, isolated capabilities, compositional
  opportunities, and avoidable handoff cost.

### Frontier candidates vs construction paths

The package makes the distinction explicit:

```text
frontier candidate
!= construction path

FRONTIER CANDIDATE
= where strategic value/tension may be concentrated

CONSTRUCTION PATH
= coherent future trajectory for changing that frontier
```

Breadth observations are compressed into grounded frontier candidates. Only
material finalists receive proportional depth analysis. Construction paths are
synthesized after frontier depth rather than for every surfaced observation.

### Coverage without exhaustive analysis

The funnel preserves:

```text
repository-wide
!= inspect every file

breadth exploration
!= manufacture an opportunity for every system

depth drill
!= deeply analyze every candidate

coverage before convergence
!= exhaustive inventory
```

No opportunity score, search tree, strategic planner, or deterministic router was
added.

### Resume discipline

The funnel belongs only to a genuinely open/reopened Level-3 boundary.

```text
ANALYZE / REOPEN_ANALYSIS
-> funnel eligible

RESPONSIBILITY / EXECUTE / VERIFY / RECONCILE
-> preserve current Level 3 unless evidence genuinely reopens it
```

This prevents the new search discipline from recreating the analysis ceremony
that `strategic-sensemaking-loop` was designed to remove.

### Owner-visible Strategic Exploration Summary

When the front-door loop actually invokes strategic analysis, its final report
now exposes a compact Strategic Exploration Summary showing:

- major systems examined;
- breadth opportunity themes/observations;
- frontier candidates;
- candidates advanced to depth and why;
- selected Strategic Frontier;
- selected construction path, if one exists.

That summary precedes the existing Decision Trace. It is owner-facing
observability, not private scratch reasoning and not a new canonical artifact.

## 3. Canonical documentation

The behavior is documented in:

- `skills/strategic-repository-analysis/SKILL.md`;
- `skills/strategic-repository-analysis/references/strategic-exploration-funnel-v1.md`;
- `skills/strategic-sensemaking-loop/SKILL.md`;
- `docs/strategic-repository-sensemaking-v1.md`;
- `docs/strategic-sensemaking-loop-v1.md`.

No artifact schema change was required.

## 4. Regression coverage

New regression coverage establishes that:

- the Strategic Exploration Funnel contains system map, breadth exploration,
  frontier-candidate synthesis, depth drill, and path synthesis;
- the funnel distinguishes frontier candidates from construction paths;
- breadth search is neither exhaustive nor numeric;
- the loop runs the funnel only at `ANALYZE / REOPEN_ANALYSIS`;
- mid-episode continuation does not repeat repository-wide breadth analysis;
- owner-facing output exposes the Strategic Exploration Summary.

## 5. Qualification evidence

Initial feature head:

`309a809b8adbf5aac0933468ec7db88469204ea4`

Release Candidate Distribution run `35940174410` / #346 found one concrete
regression assertion mismatch:

```text
expected compact law:
frontier candidate
!= construction path
```

The reference already expressed the distinction semantically, but not using the
canonical compact law required by the new regression test.

The repair made that boundary explicit rather than weakening the test.

Final exact feature head:

`7d1535db56d3afb2d8a104fb8e7a522671783e78`

GitHub Actions:

- Product Validation run `35940239815` / #1215 — **PASS**
  - Repository and Skill contracts — PASS
  - Campaign product Python 3.11 — PASS
  - Campaign product Python 3.12 — PASS
  - Filesystem security Linux — PASS
  - Filesystem security Windows — PASS
  - Installed core wheel regressions — PASS
- Release Candidate Distribution run `35940239691` / #347 — **PASS**
  - release baseline contracts — PASS
  - distribution build/metadata — PASS
  - fresh wheel install proof — PASS
  - fresh sdist install proof — PASS

Feature PR #469 merged as:

`b91c8f3a4c19dee259d2dcbcb60ff2d0eed82029`

Issue #468 closed as completed.

## 6. Claim ceiling

The integrated evidence supports:

- explicit breadth→depth Level-3 strategic-analysis guidance;
- system-map and within/across-system opportunity-search semantics;
- explicit frontier-candidate vs construction-path separation;
- owner-visible Strategic Exploration Summary guidance;
- explicit no-rerun behavior during settled mid-episode continuation;
- repository/release/install contract coherence.

It does **not** establish:

- that the breadth pass finds every valuable opportunity;
- that the selected frontier is objectively optimal;
- that more candidate generation is always better;
- that every system deserves an opportunity candidate;
- that the owner-visible summary proves hidden reasoning completeness;
- that numeric scoring or a deterministic search/runtime layer is warranted.

## 7. Remaining normal-use questions

Use ordinary repository work to observe:

1. Does system mapping cover enough of the product to avoid first-visible-problem
   capture without becoming exhaustive?
2. Does breadth exploration surface materially different opportunities rather
   than verbose variants of the same problem?
3. Does candidate compression find deeper shared frontiers across multiple
   system-level observations?
4. Does the depth drill spend effort only on real finalists?
5. Does the Strategic Exploration Summary give the owner enough evidence that
   broad search occurred without becoming an idea dump?
6. Does the loop continue to skip the funnel correctly during normal
   execution/verification resume?

No synthetic search-quality benchmark or numeric frontier scorer is warranted
from this package alone.

## 8. Current operating posture

```text
ISSUE_468_STRATEGIC_EXPLORATION_FUNNEL_V1
= COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF

CURRENT CONSTRUCTION RESPONSIBILITY = NONE
PRIMARY CONSTRUCTION PROGRAM = NONE
OPERATING MODE = NORMAL_USE_VALIDATION
```

## 9. Non-goals preserved

This package introduced no:

- new strategic artifact schema;
- deterministic breadth/depth search engine;
- numeric opportunity/frontier score;
- persistent search tree;
- mandatory opportunity per system;
- exhaustive file/system inventory;
- automatic Skill/action routing;
- repeated full-repository analysis during settled continuation.

The next mode is ordinary use.
