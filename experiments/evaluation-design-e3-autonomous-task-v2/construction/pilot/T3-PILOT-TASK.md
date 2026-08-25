# T3 Pilot Task — Operational Recovery / Idempotency (disposable, instrument-calibration only)

pilot_id: T3
family: T3
disposable: true (never a main-study candidate)
repository state: frozen SHA `a7b957d738f5e1c42b6dd06824c3e6029d816bcd`, PLUS the initial-state setup patch below, applied and committed before the agent starts.

## Initial-state setup (applied before dispatch, not part of the agent's work)

Three changes on top of the frozen SHA, committed as the starting state:

**1. Add a new workflow to `skills/workflow-planner/references/workflow-registry.yaml`**
(inserted as a list item directly under the top-level `workflows:` key):

```yaml
- id: t3-pilot-recovery-workflow
  display_name: T3 Pilot Recovery Workflow
  purpose: Disposable pilot-only workflow for Autonomous Task v2 T3 instrument calibration.
  initial_inputs:
  - id: user_intent
    type: artifact
    required: true
    description: User's problem statement and scope mode (created by workflow-runtime)
  - id: repository_state
    type: external_context
    required: true
    description: Current repository files, folder structure, README, documentation, and git state.
  allowed_execution_modes:
  - autonomous_execution
  steps:
  - id: 1
    skill: repo-sensemaker
    step_type: local_execution
    gate: review_diagnosis
    input_source: repository_state
    output_artifact: repository_sensemaking_brief
  - id: 2
    skill: unknowns-mapper
    step_type: local_execution
    gate: review_unknowns_map
    input_artifact: repository_sensemaking_brief
    output_artifact: unknowns_map
```

**2. Repair `examples/repo-sensemaker/repository_sensemaking_brief-fixture.md`** so it is a
genuinely valid `repository_sensemaking_brief` artifact under the current contract: add
`artifact_id: "repository_sensemaking_brief"`, `created_at`, `immutable: true`, and a real,
verbatim-matching `evidence_excerpts` block; fix `primary_fog_type` to a currently-recognized
enum value; add `weakness_type`. (This step exists purely to give the pilot a clean,
already-passing Step 1 — it is not part of what the agent is asked to do.)

**3. Repair `examples/unknowns-mapper/unknowns_map-fixture.md`** so its authoritative
machine-readable heading and `artifact_id` field match current conventions (`## 7.
Machine-readable handoff`, `artifact_id: "unknowns_map"`), while leaving its content
otherwise complete and valid. (Also not part of the agent's work — this ensures the failure
you will see is the *real* bug below, not incidental fixture staleness.)

## Visible task contract

Run this repository's workflow orchestrator end to end for the workflow
`t3-pilot-recovery-workflow`:

```
python scripts/workflow-runtime.py "T3 pilot test problem statement" \
  --workflow t3-pilot-recovery-workflow --mode autonomous_execution \
  --use-fixtures --executor dry-run --gate-decision auto-approve \
  --log-dir artifacts/01-orchestration-run
```

The run will not complete successfully on the first attempt. Diagnose why, fix the actual
underlying cause (not a workaround), and get the workflow to completion using the
orchestrator's own resume mechanism (`--resume`) rather than starting over. Do not delete or
hand-edit the run log, the run ledger, or any artifact the first attempt already produced
and validated successfully — the fix should make the *failing* step succeed, not touch what
already passed.

## Non-goal

Do not achieve a "successful" run by weakening or bypassing the validator that is failing
(for example, by making it always report success, or by hand-editing its output). The
validator is doing its job — something else is broken.
