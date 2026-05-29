# Execution Modes for Workflow Orchestrator

**Important:** This document describes modes *within* the orchestrator. For decisions about *whether* to use the orchestrator, see [Agent Decision Tree](../../docs/AGENTS.md).

---

## Overview

When invoking `workflow-orchestrator`, choose an execution mode that fits your approval/audit needs:

| Mode | Approval Gates | Run Logs | Use Case |
|------|---|---|---|
| `plan_only` | Yes (for each step) | Yes | Exploration, preview what would happen |
| `prompt_chain` | Minimal | Yes | Light guidance, mostly autonomous |
| `guided_execution` | Yes (at key checkpoints) | Yes | Production changes, need human sign-off |
| `autonomous_execution` | Yes (at each step) | Yes | Autonomous with safety gates |
| `yolo_execution` | None | Yes | Trusted context, full speed ahead |

---

## Mode Descriptions

### Mode 1: `plan_only`

**Stops after producing a plan. Does not execute.**

Use when you want to:
- Preview what the workflow will do
- Get approval on the approach before execution
- Refine the plan based on feedback

Produces:
- Orchestration plan artifact
- No execution, no run logs yet

---

### Mode 2: `prompt_chain`

**Executes with minimal approval gates.**

Use when you:
- Trust the automated decisions
- Want fast feedback loops
- Don't need human approval at every step

Gates:
- Large artifact creation (PRD, issue list)
- Critical changes (schema modifications, breaking changes)

---

### Mode 3: `guided_execution`

**Executes with checkpoints at key decision points.**

Use when you:
- Want human approval on major milestones
- Need to review progress before continuing
- Are making production changes

Gates:
- After discovery phase (before PRD)
- After PRD approval (before issues)
- After issues (before triage/implementation)

---

### Mode 4: `autonomous_execution`

**Executes fully with approval gates at each step.**

Use when you:
- Want safety gates on every skill execution
- Are operating in a regulated environment
- Don't want any skipped validations

Gates:
- After each skill produces an artifact
- Before that artifact is consumed by the next skill

---

### Mode 5: `yolo_execution`

**Full speed, no gates. Requires explicit opt-in incantation.**

Use when you:
- Trust the workflow completely
- Are in a fully isolated sandbox (worktree, feature branch)
- Want maximum speed

Requirements:
- Must be running on a feature branch (not main)
- Must run with `--yolo` flag (explicit opt-in)
- Must have no uncommitted changes
- Must have run logs enabled

---

## When to Choose Each Mode

### Choosing by Risk Level

**Low Risk** (you understand the code, you've done this before)
→ Use `yolo_execution` (with feature branch)

**Medium Risk** (new codebase, complex changes)
→ Use `guided_execution` (approve at checkpoints)

**High Risk** (production, regulated, multi-stakeholder)
→ Use `autonomous_execution` (validate at every step)

**Exploration / Prototyping**
→ Use `plan_only` (see the plan, then decide)

---

## How to Invoke

```
# Plan only (preview)
invoke orchestrator --mode plan_only --workflow <id>

# Guided (approve at checkpoints)
invoke orchestrator --mode guided_execution --workflow <id>

# Autonomous (gates at each step)
invoke orchestrator --mode autonomous_execution --workflow <id>

# Yolo (full speed, feature branch required)
invoke orchestrator --mode yolo_execution --workflow <id> --yolo
```

---

## Related

- [Agent Decision Tree](../../docs/AGENTS.md) -- When to use orchestrator vs. direct skill invocation
- [Skill Registry](skill-registry.yaml) -- Available skills
- [Workflow Registry](workflow-registry.yaml) -- Pre-built workflows
- [Artifact Contracts](artifact-contracts.yaml) -- Skill input/output contracts
