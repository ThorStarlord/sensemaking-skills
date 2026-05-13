---
name: workflow-orchestrator
description: Take a Repository Sensemaking Brief, select an appropriate workflow, and execute it with explicit gates and approval modes. Supports plan only, prompt chain, guided, and autonomous execution.
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
Every response must follow the [Workflow Orchestration Plan](references/run-log-template.md) structure (Wait, the user called it Workflow Orchestration Plan but referenced run-log-template in the structure... I'll create a specific template).

## Execution Modes
| Mode | Behavior |
| :--- | :--- |
| `plan_only` | Choose workflow and explain sequence. No execution. |
| `prompt_chain` | Generate copy/paste prompts only. |
| `guided_execution` | Run one step at a time and ask for approval between steps. |
| `autonomous_execution` | Execute full chain (Only when user explicitly opts in). |

## Boundary Rule
`workflow-orchestrator` must not execute an irreversible action unless the user explicitly chooses an execution mode that allows it. Irreversible actions include:
- Committing to `main`
- Creating issues / opening PRs
- Rewriting architecture docs / deleting files

## References
- [Workflow Orchestration Template](references/workflow-orchestration-template.md)
- [Skill Registry](references/skill-registry.yaml)
- [Workflow Registry](references/workflow-registry.yaml)
- [Approval Gates](references/approval-gates.md)
- [Run Log Template](references/run-log-template.md)
