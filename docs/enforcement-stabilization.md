# Enforcement-gate stabilization: failure classification and repairs

- **Date**: 2026-08-12
- **Branch**: `feat/enforcement-stabilization` (based on `feat/enforcement-gate`
  @ `e1db7dc`; gate semantics preserved unmodified)
- **Owner decision**: HOLD the enforcement-gate merge; classify and resolve
  the six core-assertions failures by authority before merge.

## Classification of the six failures

Each failure was reproduced independently, its exact disagreement captured,
and traced to authority (accepted ADRs, canonical contracts, the canonical
registry, status docs, tests). Classification legend: A = evidence-resolved
implementation/test defect; B = stale verification assertion; C = normative
ambiguity needing owner decision; D = environmental/non-product.

| # | Failure | Exact disagreement | Authority | Class |
|---|---|---|---|---|
| 1 | `test_cli.py::test_cli_version` | asserts CLI version is the old value; CLI reports the canonical one (declared by pyproject.toml, setup.py, `src/sensemaking_skills/__init__.py`) | declaration family is the version authority; docs/tests claims of the old value are stale | **B** (owner pre-authorized) |
| 2 | `test_path_drift.py::test_canonical_paths_used_in_docs` | "0 references to canonical paths found" - the test's own exclude list contains "worktrees" and the gate runs inside `.claude/worktrees/`, so the entire walk is skipped | n/a - passes on a clean checkout (verified: clone without "worktrees" in path, old code, PASSES) | **D** |
| 3 | `test_path_drift.py::test_fog_type_consistency_in_docs` | `UnicodeDecodeError` reading a SKILL.md with default cp1252 on Windows | n/a - passes on Linux/UTF-8 (verified: UTF-8 mode, old code, PASSES) | **D** |
| 4 | `test_path_drift.py::test_gate_names_are_canonical` | registry steps use gates `review_findings`, `review_recommendation` not defined in `docs/canonical-vocabulary.yaml` | canonical registry (runtime-loaded) uses them for skill-evaluation-workflow and architectural-review-planning-workflow; vocabulary gates section is the catalog that must cover them (ADR 0011 enforcement direction) | **A** (vocabulary incomplete) |
| 5 | `test_path_drift.py::test_vocabulary_covers_all_artifacts` | `architectural_review_recommendation`, `proposed_direction` declared in artifact-contracts.yaml (canonical contract) but absent from vocabulary `artifact_ids` | artifact-contracts.yaml is the canonical contract; vocabulary must cover contract artifacts (ADR 0011) | **A** (vocabulary incomplete) |
| 6 | `test_path_drift.py::test_vocabulary_covers_all_workflows` | 3 registered workflows (`architecture-implementation-workflow`, `skill-evaluation-workflow`, `architectural-review-planning-workflow`) absent from vocabulary `workflow_ids` | canonical registry registers them; tests/briefs already recommend them; docs/HARDENING_STATUS documents the intent that the vocabulary covers all registry workflow ids; the alternative (unregister the workflows) contradicts runtime, tests, and product machinery | **A** (vocabulary incomplete) |

Items 4-6 form one coherent cluster: the architectural-review /
skill-evaluation workflow family was added to the canonical registry and
contract but never added to the canonical vocabulary. The repair direction
(vocabulary catches up) is the only one consistent with all accepted
authority; the reverse (remove from registry) would break tested product
machinery.

## Repairs made and authorization

1. `tests/test_cli.py:20` - assertion updated to the canonical CLI version.
   Classification B; explicitly authorized by the owner.
2. `docs/canonical-vocabulary.yaml` - vocabulary completed to cover the
   accepted canonical sets (classification A, evidence-resolved):
   - `workflow_ids`: +3 (architecture-implementation-workflow,
     skill-evaluation-workflow, architectural-review-planning-workflow)
   - `routing_fields.recommended_workflow_id.values`: +3 (required by
     `test_recommended_workflow_id_matches_workflow_ids`, which enforces
     enum == workflow_ids)
   - `artifact_ids`: +2 (architectural_review_recommendation,
     proposed_direction; produced_by/consumed_by from the contract and
     registry)
   - `gates`: +2 (review_findings, review_recommendation; semantics from
     their use in the registry, format identical to the 41 existing gates)
   All added values use the existing vocabulary taxonomy (no new
   categories/types invented; `artifact_type: plan` is the closest
   existing value for the two review artifacts - flagged as a judgment
   call).

## Not repaired (out of scope / not authorized)

- The 4 evidence-only relationship findings (version conflict, 3 ADR
  status mismatches) - probe-gate must still show 0 blockers / 4 evidence.
- The packaged defaults mirror (`src/sensemaking_skills/defaults/
  workflow-registry.yaml`, 20 ids vs canonical 22) - a separate evidence
  finding, not one of the six gate failures; left as evidence.
- No gate weakening: no tests removed, no xfail/skip added, no policy
  changes, no semantic findings promoted to blockers.

## Verification (CI-equivalent conditions)

Full core-assertions subset run on a clean clone of this branch at a
worktrees-free path with UTF-8 mode (== CI Linux behavior for the two
environmental tests):
- before repairs (clone of the gate branch, old code): 83 passed /
  4 failed (the 4 real-drift items) - the two environmental tests green
- after repairs: see final probe-gate and core-assertions results in the
  cycle report; target is a fully green core-assertions.
