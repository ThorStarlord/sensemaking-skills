# Quarantine: retired-runner integration tests

Moved here 2026-09-29 (from `tests/integration/`) with history preserved
(`git mv`). These tests are NOT skipped — they are retired with reason, and
`pytest.ini:norecursedirs` excludes this directory from collection.

## Why

The tests assert the pre-liveness workflow registry and the retired runner path:

- `test_end_to_end_workflows.py` — expects `experimental-autonomous-sprint`,
  `product-to-issues`, `product-autonomous-sprint` in the registry
  (`test_twelve_workflows_exist_in_registry` plus 15 subtests over those IDs).
- `test_yolo_execution_with_skills.py` — executes retired workflow IDs and the
  removed `skills/workflow-presenter/` skill (0/2 steps complete).
- `test_autonomous_execution_integration.py` — same retired execution path.

The live registry follows the ADR 0027 liveness model (`active` vs
`compatibility_only`; e.g. `fast-local-diagnostic`, `full-fog-workflow`,
`docs-implementation-workflow`) and the runner retirement plan is CLOSED.
Updating these tests to the new registry would assert a migration that never
happened; the honest disposition is quarantine, not silent skip and not
rewrite.

## Baseline effect

On the post-PR-#484 main baseline (2026-09-29, 74 failed), these three files
contribute 5 FAILED + 15 SUBFAIL = 20 of the failures. After this change those 20 leave the collected set; the remaining failures are unchanged
(like-for-like command minus the quarantined paths).

## Revival condition

If the retired workflows are ever restored to the registry as `active`, move
the corresponding file(s) back to `tests/integration/` and remove this
directory's `norecursedirs` entry when empty.


## Post-RC4 additions (2026-10-07)

- `test_architectural_review_recommendation_runtime.py`
- `test_architectural_review_acceptance.py`

These prove the historical `architectural-review-planning-workflow` wrapper and
`--from-session` execution route. The current path invokes the
`architectural-review` Skill directly, so keeping these tests in the live suite
would require preserving a workflow runtime solely to satisfy its own tests.
