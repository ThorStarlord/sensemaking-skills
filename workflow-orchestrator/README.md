# workflow-orchestrator/ (legacy, deprecated)

This directory holds only a legacy copy of the artifact contracts
(`references/artifact-contracts.yaml`). It was deprecated 2026-08-09.

- **Canonical file:** `skills/workflow-planner/references/artifact-contracts.yaml`.
  All live consumers read that path.
- **Do not** read or edit the legacy copy. Field names are part of the
  artifact contract, so change the canonical file.
- The standalone `workflow-orchestrator` Skill no longer exists; workflow
  planning is `skills/workflow-planner/` and control is agent-native (ADR 0013).
  Regression tests (`tests/test_path_drift.py`,
  `tests/test_skill_hygiene_canonical_wiring.py`) guard against stale
  references to this location.
