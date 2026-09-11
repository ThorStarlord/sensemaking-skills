# Agent Workflow / Golden Path v1

**Status:** repository-qualified canonical workflow-composition reference  
**Authority:** static composition guidance only; the active agent owns semantic and authority gates  
**Execution:** none; this surface never invokes Campaign commands on the caller's behalf  
**Human entry point:** `../GETTING_STARTED.md`  
**Agent instruction surface:** `../skills/using-sensemaking/SKILL.md`

## Purpose

Sensemaking has many mechanically useful Campaign surfaces. Golden Path v1 is the canonical reference for how those surfaces compose into normal usage flows without creating a router, planner, or workflow engine.

Use `GETTING_STARTED.md` for the human first-use walkthrough. Use this document when the question is specifically **which existing Sensemaking surfaces compose into a lifecycle**. For the deeper Level-2 responsibility/authority model, see `agent-native-operating-workflow.md`; for maintainer qualification procedures, see `operations-runbook.md`.

```text
GETTING_STARTED.md
  = canonical human how-to entry point

agent-workflow-golden-path-v1.md
  = canonical workflow-composition reference

agent-native-operating-workflow.md
  = deeper Level-2 reasoning / authority map

operations-runbook.md
  = maintainer/operator mechanics
```

The CLI projects the same static flow definitions:

```bash
sensemaking-skills campaign workflow list
sensemaking-skills campaign workflow show single-repository
sensemaking-skills campaign workflow show fresh-context
sensemaking-skills campaign workflow show transferred-campaign
sensemaking-skills campaign workflow show multi-repository
```

The same flows are shipped with the `using-sensemaking` Skill at `skills/using-sensemaking/references/golden-paths-v1.md`.

## Contract

Each projected step has:

- a stable flow-local `id`;
- a human-readable existing `surface`;
- `decision_gate: true|false`.

A decision gate means the active agent/human must make the semantic or authority decision represented there. The static projection never supplies the answer.

Every payload reports:

```text
flow_selected_by_tool = false
steps_executed = false
responsibility_selected = false
capability_selected = false
authority_granted = false
semantic_truth_established = false
```

## Canonical flows

### Single repository

Strategy inspection -> agent responsibility selection -> explicit strategy handoff -> preflight -> capability context -> agent-controlled implementation -> native validation/evidence -> explicit Campaign decision -> closeout -> optional archive.

### Fresh context

Resume Profile -> preflight -> Doctor if a mechanical failure exists -> agent re-evaluates current responsibility -> bounded continuation or explicit Campaign decision.

### Transferred Campaign

Bundle inspection -> ephemeral Resume projection -> explicit import decision -> durable import -> explicit primary/additional target rebinding -> preflight -> agent-controlled continuation.

### Multi repository

Agent responsibility selection -> strategy handoff -> explicit target additions -> explicit relation declarations -> target verification -> dependency check -> preflight -> agent-controlled work -> explicit target refresh -> explicit Campaign decision -> closeout.

## Non-goals

```text
golden path != workflow engine
flow shown != flow recommended
step listed != step authorized
static navigation != semantic routing
canonical workflow reference != automatic workflow selection
```

The existing responsibility-before-Skill model remains authoritative. If a task is already narrow and locally evidenced, the agent can still act directly rather than forcing a Campaign ceremony.
