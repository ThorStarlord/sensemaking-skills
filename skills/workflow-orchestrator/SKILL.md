---
name: workflow-orchestrator
description: select and stage a workflow from a repository sensemaking brief. use when the user has a diagnostic brief and wants a workflow plan, prompt chain, guided execution plan, or guarded orchestration with approval gates.
---

# workflow-orchestrator

Takes a **Repository Sensemaking Brief** as input, selects the best workflow to address the identified weak point, and coordinates the execution of that workflow.

## Description
Use when you have a diagnostic brief and are ready to act. This skill manages the sequence of other skills, ensuring that execution is safe and bounded.

## Core Philosophy
`workflow-orchestrator` acts on the weak point. It manages the "how" of execution.

## Workflow
1. **Consume Brief**: Review the diagnostic brief from `repo-sensemaker`.
2. **Select Workflow**: Match the recommended path to an available workflow in the `workflow-registry.yaml`.
3. **Plan**: Produce a Workflow Orchestration Plan with ordered steps and approval gates.
4. **Mode Selection**: Determine the execution mode (Default: `plan_only`).
5. **Execute/Generate**: Depending on the mode, generate a prompt chain or coordinate step-by-step execution.

## Output Format
Every response must follow the [Workflow Orchestration Plan](references/workflow-orchestration-template.md) structure.
Use [Run Log Template](references/run-log-template.md) only when recording an actual guided or autonomous run.

## Execution Modes
| Mode | Behavior |
| :--- | :--- |
| `plan_only` | Choose workflow and explain sequence. No execution. |
| `prompt_chain` | Generate copy/paste prompts only. |
| `guided_execution` | Run one step at a time and ask for approval between steps. |
| `autonomous_execution` | Execute full chain (Only when user explicitly opts in). |

## Boundary Rules
- **Safety First**: Default to `plan_only` mode. 
- **Contract Enforcement**: If a brief does not contain a valid machine-readable handoff, or the requested execution mode is not allowed by [Execution Modes](references/execution-modes.md), the orchestrator MUST refuse the request or downgrade to `plan_only` or `guided_execution`.
- **Approval Gates**: Do not bypass approval gates in `guided_execution` mode.
- **Irreversible Actions**: `workflow-orchestrator` must not execute an irreversible action unless the user explicitly chooses an execution mode that allows it. Irreversible actions include:
- Committing to `main`
- Creating issues / opening PRs
- Rewriting architecture docs / deleting files

## References
- [Workflow Orchestration Template](references/workflow-orchestration-template.md)
- [Skill Registry](references/skill-registry.yaml)
- [Workflow Registry](references/workflow-registry.yaml)
- [Execution Modes](references/execution-modes.md)
- [Approval Gates](references/approval-gates.md)
- [Run Log Template](references/run-log-template.md)
