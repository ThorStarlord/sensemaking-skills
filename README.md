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

The repository is built around a five-skill **Sensemaking Pipeline** that converts raw project "fog" into a safe, evidence-backed workflow plan.

### 1. `problem-framer`
Converts vague ideas into a structured **Problem Frame**. It identifies the "problem under the problem" and the "object under pressure" before any technical mapping occurs.

### 2. `unknowns-mapper`
Separates **Knowns, Unknowns, Assumptions, and Risks**. It defines clear research paths and stopping rules to prevent premature implementation.

### 3. `repo-sensemaker`
Produces a **13-section Repository Sensemaking Brief**. It audits the repository's health, identifies the "weakest boundary," and cites specific file-level evidence.

### 4. `workflow-orchestrator`
Consumes a Brief and produces a **Workflow Orchestration Plan**. It selects the correct execution mode (plan, chain, guided, or autonomous) and defines approval gates.

### 5. `prompt-handoff`
Packages the sensemaking context into a **Ready-to-copy Prompt** for specialized downstream skills (e.g., `to-prd`, `tdd`), ensuring context is preserved across transitions.

---

## The Sensemaking Pipeline

```text
Raw Fog
  ↓ (problem-framer)
Problem Frame
  ↓ (unknowns-mapper)
Unknowns Map
  ↓ (repo-sensemaker)
Repository Sensemaking Brief (13 sections)
  ↓ (workflow-orchestrator)
Workflow Orchestration Plan (10 sections)
  ↓ (prompt-handoff)
Guided Execution / Prompt Chain
```

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
- All five core skills are package-valid with separate `agents/openai.yaml`.
- `repo-sensemaker` produces a 13-section diagnostic brief with evidence.
- `workflow-orchestrator` produces a 10-section orchestration plan.
- Registry-based routing is fully machine-readable.
- Negative fixtures exist to test refusal-to-act.
