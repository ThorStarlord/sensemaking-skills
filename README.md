# Sensemaking Skills

A collection of skills designed to turn vague project uncertainty into clear problem frames, research paths, decisions, and next-step prompts.

The repository is organized around a clean split: **Diagnosis** (`repo-sensemaker`) and **Orchestration** (`workflow-orchestrator`).

## Engineering Philosophy: Artifact-Driven Agentic Engineering

This repository is not just a collection of prompts; it is a **systems engineering** project built on the principle that **Artifacts are the API between skills**.

By forcing agents to communicate via durable, validated artifacts instead of ephemeral conversation memory, we ensure:
- **Auditability**: Every step of the reasoning is recorded in a structured document.
- **Reliability**: Skills are grounded in evidence, not hallucinations.
- **Safety**: Handoffs occur at explicit, human-approvable boundaries.

For a deep dive into our methodology, failure taxonomy, and the "Anti-Causal Confusion Rule," see [docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md](docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md).

## What this is / is not

### What this is
- A meta-routing layer to convert repository uncertainty ("fog") into actionable next steps.
- A split between **Diagnosis** (`repo-sensemaker`) and **Orchestration** (`workflow-orchestrator`).
- A structural enforcement tool for mental model alignment.

### What this is not
- A replacement for specialized tools (PM skills, Matt Pocock skills, Interface Skills).
- A blind automation engine. It uses explicit approval gates.

## Skill Ecosystem

The repository provides a complete skill ecosystem for converting project uncertainty into action. Skills are organized by purpose and can be composed into workflows.

### Core Sensemaking (5 skills)

The foundation layer: diagnostic and orchestration skills that identify problems and route work.

- **`problem-framer`** — Converts vague ideas into structured Problem Frames. Identifies the "problem under the problem" and "object under pressure."
- **`unknowns-mapper`** — Separates Knowns, Unknowns, Assumptions, and Risks. Defines research paths and stopping rules. Can dynamically trigger research skills based on fog clarity.
- **`repo-sensemaker`** — Produces a 14-section Repository Sensemaking Brief. Audits repository health, identifies the "weakest boundary," cites file-level evidence.
- **`workflow-orchestrator`** — Consumes a Brief and produces a Workflow Orchestration Plan. Selects execution mode and defines approval gates.
- **`sensemaking-docs-reconciler`** — Aligns repository docs, registries, and artifact contracts to resolve drift.
- **`prompt-handoff`** — Packages sensemaking context into a ready-to-copy Prompt for downstream skills.

### Drafting & Implementation (6 skills)

Transform diagnostic outputs into specifications and implementation plans.

- **`grill-with-docs`** — Stress-test a plan against existing domain documentation. Sharpens terminology and updates docs inline.
- **`to-prd`** — Transform a domain alignment report into a PRD.
- **`to-issues`** — Transform a PRD into specific, independently-grabbable implementation issues (tracer bullets).
- **`triage`** — Assign issues to agent briefs and prepare work for implementation.
- **`tdd`** — Execute implementation using test-driven development (red-green-refactor loop).
- **`ui-brief`** — Create high-fidelity UI specifications from product requirements.

### Product Management (20+ skills)

Comprehensive product and strategy toolkit for discovery, planning, and validation.

**Discovery & Insights:**
- `persona` — Define target user and player fantasy.
- `discovery` — Investigate problem space and user needs.
- `interview-synthesis` — Extract patterns from customer interviews.
- `competitive-analysis` — Audit market alternatives and positioning.

**Planning & Strategy:**
- `opportunity-tree` — Map problems to desired outcomes.
- `hypothesis` — Define testable product bets.
- `customer-journey` — Map user flow and friction points.
- `user-stories` — Define feature slices from user perspective.
- `acceptance-criteria` — Define done states for features.

**Prioritization & Execution:**
- `prioritize` — Rank work by impact and feasibility.
- `roadmap` — Sequence work across time.
- `launch-checklist` — Verify operational readiness for release.
- `pre-mortem` — Identify failure modes before launch.

**Goals & Metrics:**
- `okr` — Define goals and key results.
- `north-star` — Identify core leading metric.
- `lean-canvas` — Summarize business model on one page.
- `measure-pmf` — Audit product-market fit signals.

**Monetization & Growth:**
- `pricing` — Design monetization and packaging.
- `gtm` — Define go-to-market execution plan.
- `battlecard` — Summarize competitive talk tracks.

**Experimentation & Release:**
- `experiment-design` — Plan validation tests for hypotheses.
- `ab-test-analysis` — Evaluate results of split tests.
- `release-notes` — Communicate value to users and stakeholders.
- `stakeholder-update` — Communicate progress and blockers.

### Research & Maintenance (2 skills)

Support ongoing learning and skill improvement.

- **`usage-researcher`** — Evaluate skill performance in realistic scenarios.
- **`skill-maintainer`** — Translate usage research into auditable skill improvements.

---

## The Sensemaking Pipeline

```text
Raw Fog
  ↓ (problem-framer)
Problem Frame
  ↓ (unknowns-mapper)
Unknowns Map
  ↓ (repo-sensemaker)
Repository Sensemaking Brief (14 sections)
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

### Fast Path (Direct Repo Analysis)
Use this when the goal is clear and you just need a repository-level diagnosis.
1. Run `repo-sensemaker` to identify the **Weakest Boundary**.
2. Review the **Repository Sensemaking Brief**.
3. Pass the brief to `workflow-orchestrator` to select and run a corrective workflow.

### Full Fog Path (Comprehensive Sensemaking)
Use this when the project is highly ambiguous or lacks a clear problem frame.
1. `problem-framer`: Define the "problem under the problem."
2. `unknowns-mapper`: Map the research paths and assumptions.
3. `repo-sensemaker`: Conduct the deep repository audit.
4. `workflow-orchestrator`: Select the workflow and execution mode.
5. `prompt-handoff`: Generate the bridge prompt for specialized tools.

## Downstream Skill Assumption

This repository assumes the following downstream skill packs are installed in the local working environment when using product or implementation workflows:

- [Product Manager Skills](https://github.com/ThorStarlord/pm-skills)
- [Matt Pocock Skills](https://github.com/mattpocock/skills)
- [Interface Skills](https://github.com/ThorStarlord/interface-skills)

If these skills are not installed, `workflow-orchestrator` can still produce `prompt_chain` outputs, but it cannot execute those workflow steps directly.

## License
MIT

## Contributing
- New diagnosis rules go in `repo-sensemaker/references/`.
- New skill entries go in `workflow-orchestrator/references/skill-registry.yaml`.
- New workflows go in `workflow-orchestrator/references/workflow-registry.yaml`.
- New examples must include an expected behavior checklist.

## V1 Definition of Done (New Architecture)
- All five core skills are package-valid with separate `agents/openai.yaml`.
- `repo-sensemaker` produces a 14-section diagnostic brief with evidence.
- `workflow-orchestrator` produces a 10-section orchestration plan.
- Registry-based routing is fully machine-readable.
- Negative fixtures exist to test refusal-to-act.
