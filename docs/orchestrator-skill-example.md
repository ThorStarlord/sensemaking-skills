# Orchestrator-Skill Example Implementation

This document shows how the orchestrator-skill would execute a workflow using the run-ledger system.

## Example: Fast-Path Workflow

The orchestrator runs the `fast-path-workflow`, which has 4 steps:

```
1. problem-framer     → problem_frame.md
2. unknowns-mapper    → unknowns_map.md
3. repo-sensemaker    → repository_sensemaking_brief.md
4. handoff            → final_summary.md
```

## Execution Flow

### Phase 1: Initialization

```python
# orchestrator-skill receives user intent
user_intent = "I'm confused about where to start with this repo"
workflow_id = "fast-path-workflow"
mode = "guided_execution"

# Initialize run
orchestrator.run(workflow_id, mode, user_intent)
```

### Phase 2: Step-by-Step Execution

#### Step 1: problem-framer

```bash
# 1. Orchestrator calls run-ledger to start step 1
$ python scripts/run-ledger.py start-step \
    --step-id 1 --skill problem-framer

# 2. Orchestrator invokes problem-framer skill (via Claude)
# "Please analyze the user intent and produce a problem frame"

# 3. problem-framer produces artifacts
# The skill is told:
#   - run_id: orchestrator-run-01
#   - step_id: 1
#   - expected_artifact: problem_frame
#   - session_dir: artifacts/01-orchestration-run/

# 4. problem-framer calls create-artifact to get the output path
$ python scripts/create-artifact.py \
    --run-id orchestrator-run-01 \
    --artifact-id problem_frame \
    --step-id 1
# Returns: artifacts/01-orchestration-run/problem_frame.md

# 5. problem-framer writes to that exact path
$ cat > artifacts/01-orchestration-run/problem_frame.md << EOF
# Problem Frame

## Problem Under the Problem
The user is uncertain about repository structure and entry points.

## Object Under Pressure
The repository's routing and configuration system.

...
EOF

# 6. problem-framer calls validate-and-record to validate the artifact
$ python scripts/validate-and-record.py \
    --run-id orchestrator-run-01 \
    --step-id 1 \
    --artifact-id problem_frame \
    --path artifacts/01-orchestration-run/problem_frame.md

# This wrapper:
#   - Runs the problem_frame validator
#   - Records the validation event in the ledger
#   - Returns exit code 0 (success) or 1 (failure)

# 7. Orchestrator observes the result in the ledger
$ python scripts/workflow-runtime.py audit-run \
    --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl

# Ledger now contains:
#   run_started
#   step_started (step 1)
#   artifact_created (problem_frame)
#   validation_completed (problem_frame, exit_code=0, status=passed)

# 8. Orchestrator decides to proceed (in guided_execution, user approves)
# Orchestrator calls run-ledger to complete the step
$ python scripts/run-ledger.py complete-step \
    --step-id 1 \
    --status completed \
    --gate-status approved
```

#### Step 2: unknowns-mapper

```bash
# Same flow as Step 1:
# 1. start-step
$ python scripts/run-ledger.py start-step \
    --step-id 2 --skill unknowns-mapper

# 2. Orchestrator invokes unknowns-mapper skill
# "Use the problem frame to identify unknowns"

# 3. unknowns-mapper receives:
#   - session_dir: artifacts/01-orchestration-run/
#   - input_artifacts: [problem_frame.md]
#   - expected_artifact: unknowns_map

# 4. unknowns-mapper calls create-artifact
$ python scripts/create-artifact.py \
    --run-id orchestrator-run-01 \
    --artifact-id unknowns_map \
    --step-id 2

# 5. unknowns-mapper writes to artifacts/01-orchestration-run/unknowns_map.md

# 6. unknowns-mapper validates
$ python scripts/validate-and-record.py \
    --run-id orchestrator-run-01 \
    --step-id 2 \
    --artifact-id unknowns_map \
    --path artifacts/01-orchestration-run/unknowns_map.md

# 7. Orchestrator completes the step
$ python scripts/run-ledger.py complete-step \
    --step-id 2 \
    --status completed \
    --gate-status approved
```

#### Steps 3-4: Similar Pattern

repo-sensemaker and handoff follow the same pattern.

### Phase 3: Finalization & Audit

```bash
# After all steps complete, orchestrator runs final audit
$ python scripts/workflow-runtime.py audit-run \
    --ledger-path artifacts/01-orchestration-run/run-ledger.jsonl \
    --repo-root /path/to/repo

# Audit checks:
# 1. All events in chronological order
# 2. All artifact hashes match files on disk
# 3. All validation exits were 0 (passed)
# 4. Input dependencies:
#    - Step 2's unknowns_map input references Step 1's problem_frame output hash
#    - Step 3's brief input references Step 2's unknowns_map output hash
#    - etc.
# 5. No steps marked completed without validation

# If audit passes, orchestrator reports success:
print("[ORCHESTRATOR] ✓ Run completed successfully")
print("[ORCHESTRATOR] Artifacts in: artifacts/01-orchestration-run/")
```

## The Ledger After Execution

```jsonl
{"event":"run_started","run_id":"orchestrator-run-01","workflow_id":"fast-path-workflow","mode":"guided_execution","git_commit":"def789abc123...","timestamp":"2026-05-22T18:00:00Z"}
{"event":"step_started","step_id":"1","skill_id":"problem-framer","input_artifacts":[],"timestamp":"2026-05-22T18:00:01Z"}
{"event":"artifact_created","step_id":"1","artifact_id":"problem_frame","path":"artifacts/01-orchestration-run/problem_frame.md","hash":"sha256:abc123...","timestamp":"2026-05-22T18:00:02Z"}
{"event":"validation_completed","step_id":"1","artifact_id":"problem_frame","validator_command":"validate-output.py problem_frame ...","exit_code":0,"status":"passed","timestamp":"2026-05-22T18:00:03Z"}
{"event":"step_completed","step_id":"1","status":"completed","gate_status":"approved","timestamp":"2026-05-22T18:00:04Z"}
{"event":"step_started","step_id":"2","skill_id":"unknowns-mapper","input_artifacts":["problem_frame"],"timestamp":"2026-05-22T18:00:05Z"}
{"event":"artifact_created","step_id":"2","artifact_id":"unknowns_map","path":"artifacts/01-orchestration-run/unknowns_map.md","hash":"sha256:def456...","timestamp":"2026-05-22T18:00:06Z"}
{"event":"validation_completed","step_id":"2","artifact_id":"unknowns_map","validator_command":"validate-output.py unknowns_map ...","exit_code":0,"status":"passed","timestamp":"2026-05-22T18:00:07Z"}
{"event":"step_completed","step_id":"2","status":"completed","gate_status":"approved","timestamp":"2026-05-22T18:00:08Z"}
...
```

## Key Design Principles in Action

### 1. Orchestrator Owns Flow
- Orchestrator decides to invoke problem-framer, unknowns-mapper, etc.
- Orchestrator reads ledger to check validation results
- Orchestrator decides when to proceed, retry, or halt

### 2. Scripts Record Facts
- `run-ledger.py` records every event deterministically
- `validate-and-record.py` runs validators and records results
- `create-artifact.py` resolves the exact output path
- These scripts never have business logic

### 3. Ledger Is Truth
- The ledger proves what happened
- `audit-run` verifies the ledger against filesystem reality
- No hidden state in the orchestrator or runtime

### 4. Worker Skills Stay Simple
- problem-framer doesn't call start-step itself
- unknowns-mapper doesn't decide step order
- Both follow a simple protocol: receive inputs, produce outputs, validate

### 5. Validation Is Decoupled
- Each skill's validator is independent
- `validate-and-record.py` wraps all validators uniformly
- Validators never affect orchestrator logic

## How to Run This

1. Create a simple test input:
```bash
mkdir -p /tmp/test-repo
echo "I'm confused about this repo" > /tmp/test-repo/user_intent.txt
```

2. Run the orchestrator:
```bash
python skills/orchestrator-skill/orchestrator.py \
    --repo-root /tmp/test-repo \
    --workflow fast-path-workflow \
    --mode guided_execution
```

3. Watch the ledger being created:
```bash
tail -f /tmp/test-repo/artifacts/01-orchestration-run/run-ledger.jsonl
```

4. Audit the result:
```bash
python scripts/workflow-runtime.py audit-run \
    --ledger-path /tmp/test-repo/artifacts/01-orchestration-run/run-ledger.jsonl \
    --repo-root /tmp/test-repo
```

## Next Steps

- Integrate this with actual Claude API calls so orchestrator-skill can really invoke worker skills
- Implement resumability: if a step fails, re-run from that point using the ledger
- Add more sophisticated gate handling: user prompts, automated decisions, etc.
- Migrate all worker skills to fully implement the execution protocol
