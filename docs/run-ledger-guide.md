# Run Ledger Architecture Guide

## Overview

The run ledger is an append-only JSONL file that records every step of a workflow execution. It provides machine-checkable provenance: proof of what happened, in what order, with what inputs and outputs, and whether each step validated.

## Architecture

```
orchestrator-skill (AI-native control loop)
  ↓
scripts/run-ledger.py (event recording)
  ↓
worker skills (problem-framer, unknowns-mapper, repo-sensemaker, etc.)
  ↓
scripts/validate-and-record.py (validation wrapper)
  ↓
artifacts/ (session-scoped directory with validated output)
  ↓
workflow-runtime.py audit-run (post-run verification)
```

## The Ledger Format

Each line in `artifacts/<run-id>/run-ledger.jsonl` is a JSON event:

```jsonl
{"event":"run_started","run_id":"orchestrator-run-01","workflow_id":"fast-path-workflow","mode":"guided_execution","git_commit":"abc123...","timestamp":"2026-05-22T18:00:00Z"}
{"event":"step_started","step_id":"1","skill_id":"problem-framer","input_artifacts":[],"timestamp":"2026-05-22T18:00:01Z"}
{"event":"artifact_created","step_id":"1","artifact_id":"problem_frame","path":"artifacts/01-orchestration-run/problem_frame.md","hash":"sha256abc...","timestamp":"2026-05-22T18:00:02Z"}
{"event":"validation_completed","step_id":"1","artifact_id":"problem_frame","validator_command":"validate-output.py","exit_code":0,"status":"passed","timestamp":"2026-05-22T18:00:03Z"}
{"event":"step_completed","step_id":"1","status":"completed","gate_status":"approved","timestamp":"2026-05-22T18:00:04Z"}
```

## Event Types

### run_started
Records the beginning of a workflow run.
```json
{
  "event": "run_started",
  "run_id": "orchestrator-run-01",
  "workflow_id": "fast-path-workflow",
  "mode": "guided_execution",
  "git_commit": "abc123def456...",
  "timestamp": "2026-05-22T18:00:00Z"
}
```

### step_started
Records the beginning of a workflow step.
```json
{
  "event": "step_started",
  "step_id": "1",
  "skill_id": "problem-framer",
  "input_artifacts": ["user_intent"],
  "timestamp": "2026-05-22T18:00:01Z"
}
```

### artifact_created
Records that a worker skill produced an artifact.
```json
{
  "event": "artifact_created",
  "step_id": "1",
  "artifact_id": "problem_frame",
  "path": "artifacts/01-orchestration-run/problem_frame.md",
  "hash": "sha256:abc123def456...",
  "timestamp": "2026-05-22T18:00:02Z"
}
```

### validation_completed
Records that an artifact was validated.
```json
{
  "event": "validation_completed",
  "step_id": "1",
  "artifact_id": "problem_frame",
  "validator_command": "validate-output.py problem_frame ...",
  "exit_code": 0,
  "status": "passed",
  "timestamp": "2026-05-22T18:00:03Z"
}
```

### step_completed
Records the completion of a step, including gate decision.
```json
{
  "event": "step_completed",
  "step_id": "1",
  "status": "completed",
  "gate_status": "approved",
  "timestamp": "2026-05-22T18:00:04Z"
}
```

## Using the Run Ledger System

### 1. Orchestrator Initializes

The orchestrator skill starts a run:

```bash
python scripts/run-ledger.py \
  --repo-root /path/to/repo \
  --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl \
  start-run \
  --run-id orchestrator-run-01 \
  --workflow fast-path-workflow \
  --mode guided_execution
```

### 2. For Each Step

#### 2a. Start the step

```bash
python scripts/run-ledger.py \
  --repo-root /path/to/repo \
  --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl \
  start-step \
  --step-id 1 \
  --skill problem-framer
```

#### 2b. Worker skill executes

The worker skill (problem-framer) is invoked by the orchestrator.

#### 2c. Record artifact creation

```bash
python scripts/run-ledger.py \
  --repo-root /path/to/repo \
  --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl \
  record-artifact \
  --step-id 1 \
  --artifact-id problem_frame \
  --path artifacts/01-orchestration-run/problem_frame.md
```

#### 2d. Record validation

```bash
python scripts/validate-and-record.py \
  --repo-root /path/to/repo \
  --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl \
  --step-id 1 \
  --artifact-id problem_frame \
  --path artifacts/01-orchestration-run/problem_frame.md
```

#### 2e. Complete the step

```bash
python scripts/run-ledger.py \
  --repo-root /path/to/repo \
  --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl \
  complete-step \
  --step-id 1 \
  --status completed \
  --gate-status approved
```

### 3. Audit the Run

After all steps, verify the entire causal chain:

```bash
python scripts/workflow-runtime.py audit-run \
  --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl \
  --repo-root /path/to/repo
```

This will:
- Verify every event is in chronological order
- Check that all artifact hashes match what's on disk
- Confirm all validation exits were 0 (passed)
- Verify input dependencies match output hashes from prior steps
- Report any inconsistencies

## Worker Skill Protocol

Every worker skill must follow this pattern when invoked as part of a workflow:

```markdown
## Execution Protocol

When executing as part of a workflow run:

1. Read the provided run_id, step_id, input artifacts, and expected artifact_id.
2. Call `scripts/run-ledger.py start-step`.
3. Call `scripts/create-artifact.py` to resolve the output path.
4. Produce the artifact at that exact path.
5. Call `scripts/validate-and-record.py`.
6. Only report completion if validation passes.
7. Never mark the next step complete yourself.
```

Each skill's SKILL.md should include this documentation.

## Design Principles

### 1. Orchestrator Owns Flow Control
The orchestrator skill (Claude) decides what to do next. It observes the ledger and adapts.

### 2. Scripts Record Facts
Helper scripts (`run-ledger.py`, `validate-and-record.py`, `create-artifact.py`) are deterministic utilities that can never fail to record what happened. They are never called directly by Claude code — only by worker skills and orchestrators.

### 3. Ledger Is the Source of Truth
The run ledger is append-only and immutable. It proves causality, dependencies, and validation outcomes. The audit tool reconstructs what happened from the ledger alone.

### 4. Worker Skills Stay in Control
Worker skills are not "driven" by a runner. They invoke helper scripts, produce artifacts, and report success/failure. The orchestrator observes results via the ledger.

### 5. Validation Is Decoupled
Validation happens through a wrapper script (`validate-and-record.py`), not via orchestrator logic. This keeps the validation contract separate from skill execution and auditing logic.

## Example: Fast-Path Workflow

The `fast-path-workflow` is a good starting point:

1. **problem-framer** (step 1) — produces `problem_frame.md`
2. **unknowns-mapper** (step 2) — produces `unknowns_map.md`
3. **repo-sensemaker** (step 3) — produces `repository_sensemaking_brief.md`
4. **handoff** (step 4) — produces decision summary

Each step follows the worker skill protocol, and the ledger records the complete chain.

## Advantages

- **Auditable**: `workflow-runtime.py audit-run` can verify the entire execution deterministically
- **Resumable**: If a step fails, the ledger shows exactly where and why; re-runs can pick up from that point
- **Decoupled**: Skills don't need to know about the runtime; they follow a simple protocol
- **Verifiable**: Hashes prove that inputs and outputs haven't changed
- **AI-Native**: The orchestrator skill sees the same facts the ledger records; no hidden state

## Next Steps

- Use the orchestrator-skill to run a workflow
- Observer the ledger events in `artifacts/NN-orchestration-run/run-ledger.jsonl`
- Run `workflow-runtime.py audit-run` to verify the causal chain
- Extend worker skills to fully implement the execution protocol
