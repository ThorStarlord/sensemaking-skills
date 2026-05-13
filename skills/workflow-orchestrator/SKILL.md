---
name: workflow-orchestrator
description: select and stage a workflow from a repository sensemaking brief. use when the user has a diagnostic brief and wants a workflow plan, prompt chain, guided execution plan, or guarded orchestration with approval gates.
---

# workflow-orchestrator

## Workflow
1. **Consume Brief**: Review the diagnostic brief from `repo-sensemaker`.
2. **Select Workflow**: Match the recommended path to an available workflow in the `workflow-registry.yaml`.
3. **Plan**: Produce a Workflow Orchestration Plan with ordered steps and approval gates.
4. **Mode Selection**: Determine the execution mode (Default: `plan_only`).
5. **Execute/Generate**:
   - `plan_only`: produce the plan and stop.
   - `prompt_chain`: produce copy/paste prompts and stop.
   - `guided_execution`: execute one eligible local step, validate its output artifact, write/update the run log, then stop for approval.
   - `autonomous_execution`: execute eligible local steps until the next approval gate, failed validation, non-local skill, or stop condition.
   - `yolo_execution`: execute only eligible local steps with no intermediate approval, but stop immediately on missing artifact, invalid handoff, failed validation, non-local skill, dirty git state, or run-log failure.

## Output Format
Every response must follow the [Workflow Orchestration Plan](references/workflow-orchestration-template.md) structure.
Use [Run Log Template](references/run-log-template.md) only when recording an actual guided or autonomous run.

## Execution Modes
| Mode | Behavior |
| :--- | :--- |
| `plan_only` | Choose workflow and explain sequence. No execution. |
| `prompt_chain` | Generate copy/paste prompts only. |
| `guided_execution` | Run one step at a time and ask for approval between steps. |
| `autonomous_execution` | Execute full chain with approval gates (Requires opt-in). |
| `yolo_execution` | Full automation of local steps without intermediate gates (Requires YOLO opt-in). |

## Boundary Rules
- **Safety First**: Default to `plan_only` mode. 
- **Contract Enforcement**: If a brief does not contain a valid machine-readable handoff, or the requested execution mode is not allowed by [Execution Modes](references/execution-modes.md), the orchestrator MUST refuse the request or downgrade to `plan_only` or `guided_execution`.
- **Handoff Compliance**: Transitions between skills in a workflow MUST comply with the [Artifact Contracts](references/artifact-contracts.yaml).
- **Execution Authority**: The orchestrator is ONLY authorized to execute `local` skills. `external` or `prompt_only` skills must be treated as routing targets.
- **YOLO Mode Restrictions**: 
    - Requires exact opt-in: `"I choose yolo_execution and accept automated repository changes, feature-branch commits, bypassed gates, and recovery risk."`
    - Requires a feature branch (No direct commits to `main`).
    - Requires a [Run Log](references/run-log-template.md).
- **Approval Gates**: Do not bypass approval gates in `guided_execution` or `autonomous_execution` mode. Only `yolo_execution` bypasses gates for local skills.

## Hard Stop Conditions
The orchestrator MUST stop and report instead of continuing when any of these occur:
- The workflow step is `external` or `prompt_only`.
- The next step is `workflow-orchestrator` itself, unless the mode is `plan_only`.
- The expected output artifact is missing, malformed, or does not satisfy `artifact-contracts.yaml`.
- The selected workflow does not explicitly allow the requested execution mode.
- The run log cannot be created or updated.
- The working tree is dirty before `autonomous_execution` or `yolo_execution`.
- The current branch is `main` or `master` during a mode that can mutate files.
- More than one retry would be required for the same step.
- The current context contains more than one full artifact from prior steps; summarize earlier artifacts before continuing.

## References
- [Workflow Orchestration Template](references/workflow-orchestration-template.md)
- [Skill Registry](references/skill-registry.yaml)
- [Workflow Registry](references/workflow-registry.yaml)
- [Artifact Contracts](references/artifact-contracts.yaml)
- [Execution Modes](references/execution-modes.md)
- [Git Safety Policy](references/git-safety-policy.md)
- [Recovery Policy](references/recovery-policy.md)
- [Approval Gates](references/approval-gates.md)
- [Run Log Template](references/run-log-template.md)
