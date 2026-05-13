# Sensemaking Skills

A collection of skills designed to turn vague project uncertainty into clear problem frames, research paths, decisions, and next-step prompts.

The repository is organized around a clean split: **Diagnosis** (`repo-sensemaker`) and **Orchestration** (`workflow-orchestrator`).

## Core Philosophy

"I do not know what I need because I do not yet understand what I am building."

Sensemaking skills sit **before** specialized tools. They handle the moment of "fog" where the type of problem is not yet known.

## What this is / is not

### What this is
- A meta-routing layer to convert repository uncertainty ("fog") into actionable next steps.
- A split between **Diagnosis** (`repo-sensemaker`) and **Orchestration** (`workflow-orchestrator`).
- A structural enforcement tool for mental model alignment.

### What this is not
- A replacement for specialized tools (PM skills, Matt Pocock skills, Interface Skills).
- A blind automation engine. It uses explicit approval gates.

## Core Skills

### 1. `repo-sensemaker`
**Purpose**: finds the weak point.
Analyzes a repository to produce a **Repository Sensemaking Brief**. It identifies the weakest boundary, missing pieces, and recommended next moves.

### 2. `workflow-orchestrator`
**Purpose**: acts on the weak point.
Takes a Sensemaking Brief, selects an appropriate workflow, and coordinates the execution (or prompt generation) with explicit safety gates.

## Core Artifacts

- **Repository Sensemaking Brief**: A diagnostic report naming the fog type, object under pressure, and the weakest boundary.
- **Workflow Orchestration Plan**: A procedural plan naming the chosen workflow, skill sequence, and mandatory approval gates.

## Repository Structure

- `skills/`:
  - `repo-sensemaker/`: Diagnostic skill and templates.
  - `workflow-orchestrator/`: Execution/Orchestration skill and registries.
- `workflows/`: Composite skill chains (e.g., [Experimental Autonomous Sprint](workflows/experimental-autonomous-sprint.md)).
- `examples/`: Validation fixtures for both skills.
- `docs/`: Repository-level documentation (PRDs, Issues, ADRs).

## Usage

1. Run `repo-sensemaker` on a codebase to find the weakest boundary.
2. Review the **Repository Sensemaking Brief**.
3. Pass the brief to `workflow-orchestrator` to select and run a corrective workflow.

## License
MIT

## Contributing
- New diagnosis rules go in `repo-sensemaker/references/`.
- New skill entries go in `workflow-orchestrator/references/skill-registry.yaml`.
- New workflows go in `workflow-orchestrator/references/workflow-registry.yaml`.
- New examples must include an expected behavior checklist.

## V1 Definition of Done (New Architecture)
- Both skills are package-valid with separate `agents/openai.yaml`.
- `repo-sensemaker` produces an 11-section diagnostic brief.
- `workflow-orchestrator` produces a 10-section orchestration plan.
- Registry-based routing is fully machine-readable.
- Negative fixtures exist to test refusal-to-act.
