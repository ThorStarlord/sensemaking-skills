---
name: orchestrator-skill
description: AI-native orchestrator that controls the workflow run loop, invokes worker skills, and verifies the run ledger.
---

# orchestrator-skill

This skill acts as the decentralized, AI-native control loop for workflow execution. Instead of a central Python runner driving skill execution, the `orchestrator-skill` reads the intent, determines the steps, invokes worker skills, manages step gates, and verifies machine-readable facts using run ledger utilities.

## Workflow

1. **Initialization**:
   - Call `scripts/run-ledger.py start-run` to log the `run_started` event.
   - Resolve the execution mode and workflow ID (e.g. `fast-local-diagnostic`).

2. **Step Loop**:
   - For each step in the workflow sequence:
     1. Formulate the inputs and output artifact ID.
     2. Invoke the worker skill corresponding to the step.
     3. Ensure the worker skill follows the **Execution Protocol**:
        - Start step via `run-ledger.py start-step`.
        - Resolve path via `create-artifact.py`.
        - Generate artifact content.
        - Validate via `validate-and-record.py`.
     4. Inspect the ledger to confirm validation was completed successfully and check the exit code.
     5. Handle approval gates (auto-approve in autonomous mode, prompt user in guided mode).
     6. Call `scripts/run-ledger.py complete-step` with the gate status.

3. **Finalization**:
   - Call `scripts/run-ledger.py finalize-run` with `--update-mode-coverage` to finalize the run status and update metrics.
   - Run `python scripts/workflow-runtime.py audit-run --ledger-path <path>` to deterministically verify the entire causal chain, artifact hashes, and validation outcomes.
   - Provide a final human-readable summary of the run to the user.

## References
- [Artifact Contracts](../workflow-planner/references/artifact-contracts.yaml)
- [Workflow Registry](../workflow-planner/references/workflow-registry.yaml)
