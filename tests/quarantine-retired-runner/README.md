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


## Auto-invocation consumer removal (2026-10-07)

The following tests were moved here when executable auto-invocation consumers
were removed after all remaining metadata carriers became `compatibility_only`:

- `test_auto_invoke_authority_gating.py`
- `test_auto_invocation_target_repo.py`
- `test_invocation_paths.py`

The historical metadata remains in catalog records for provenance. Current
execution no longer parses it, surfaces hypothetical child workflows, or keeps a
no-op router alive merely to prove that it will not route.


- `test_field_contract_agreement.py` was also retired with the executable
  auto-routing consumer. Its sole contract was that the removed runtime routing
  alias lists matched artifact schemas; with those readers gone, preserving the
  alias lists only to satisfy this test would recreate dead product machinery.
