# Suite stabilization: 74 baseline failures to green (2026-09-29)

Closed record of the Step 1-3 stabilization program. Every cluster below was
worked one PR at a time, each verified like-for-like (same command, same
environment) before and after. This is a record, not a new authority.

## Baseline

- Command: `python -m pytest --ignore=tests/test_validate_brief_json.py -q --tb=no -rf -n 6`
- Commit: `2543ff6` (main after merging PR #484), clean detached worktree.
- Result: **74 failed, 3454 passed, 22 skipped, 5 xfailed**.
- The author's reference count was 73; the +1 was
  `tests/test_strategic_continuity_refinement_v1.py::test_typed_currentness_reports_mechanical_observation_kinds`,
  which fails only where Git's system default `core.autocrlf=true` corrupts
  blob hashes in the test's scratch repo (Windows), and passes with it off.

## Root-cause clusters and dispositions

| Cluster | Count | Cause | Disposition | PR |
| --- | --- | --- | --- | --- |
| F: missing importable validator shim | 1 + 1 knock-on | `scripts/validate_brief.py` (underscore) never tracked; whole suite errored at collection | Restore the shim over the canonical hyphenated validator | #486 |
| B: retired runner/workflows | 5 + 15 subfails | Tests pinned the pre-ADR-0027 registry and the retired runner path (`workflow-presenter`) | Quarantine with reason (`tests/quarantine-retired-runner/` + README + `norecursedirs`); retarget the ui-diagnostic gate test | #487 |
| A: governed-docs drift | 7 + 12 subfails | Programmatic-runner retirement (ADR 0013) left the Evidence-0016 docs, contract block, and pins describing a live enforcing consumer | Reframe docs to retired truth; reconcile pins; regenerate authorization-record digests | #488 |
| C: skill/contract drift | 8 + 3 subfails | Liveness split (ADR 0027) never reached the fog->workflow fallback maps; two skill-text test anchors were stale | Fallback maps now name liveness-active workflows only; tests re-anchored to current SKILL.md phrasing | #489 |
| D: fixture rot | 15 | Fixtures pinned retired `*-implementation-workflow` IDs, a rewritten README sentence, and missing weakness_type metadata | Modernize fixtures to active IDs + current README + Section 6/13 weakness pair | #490 |
| E: env/white-box assumptions | 13 | Tests pinned the pre-retirement runtime shape, pre-rewrite docs, or a POSIX/lab Git config | Fix tests to the current contract; `git -c core.autocrlf=false` for the hash-sensitive test | #491 |

## CI blind spot (Step 2)

CI on `main` was green while the full suite failed because `validation.yml`
runs a curated subset. A new `full-suite` job now runs
`python -m pytest -q -n auto` with `rfc8785` + `jsonschema` installed, and
asserts the suite does not dirty tracked state. PR #492; the job passed in
1m49s.

## Docs cleanup decision (Step 3)

Historical `docs/PHASE-*`, `STAGE-*`, `IMPLEMENTATION-*` and the root records
stay in place, marked historical. Moving them would invalidate evidence
citations (probe reports, campaign records) for no benefit.
`release-v1.0.yaml` stays as the load-bearing machine contract. Recorded in
`docs/README.md`; PR #493.

## Verification

- CI full-suite gate (Linux): **PASS** (PR #492) — the authoritative "suite is
  green" evidence.
- Local Windows `-n 6` on merged main: 4 failures remain
  (`tests/performance/test_performance_benchmarks.py::test_orchestration_runner_startup_time`
  and three architectural-review tests that spawn `workflow-runtime.py` with a
  hard 30s subprocess timeout). Each passes in isolation; they are
  parallel-load wall-clock artifacts on this machine, not regressions, and
  none were in the baseline failure list.
- Baseline failure count resolved: 74 / 74.
