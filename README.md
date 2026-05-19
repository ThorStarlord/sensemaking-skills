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

- **Problem Frame** (Full Fog Path only): Structured framing of the "problem under the problem" and the object under pressure.
- **Unknowns Map** (Full Fog Path only): Separation of Knowns, Unknowns, Assumptions, and Risks with research paths.
- **Repository Sensemaking Brief**: A 14-section diagnostic report naming the fog type, weakest boundary, and candidate workflows with evidence.
- **Workflow Orchestration Plan**: A 10-section procedural plan naming the selected workflow, skill sequence, approval gates, and execution mode.
- **Workflow Run Log**: Records all skill executions, gate decisions, artifact validations, and error handling for the workflow run.

## Repository Structure

- `skills/`:
  - `repo-sensemaker/`: Diagnostic skill and templates.
  - `workflow-orchestrator/`: Execution/Orchestration skill and registries.
- `workflows/`: Composite skill chains (e.g., [Experimental Autonomous Sprint](workflows/experimental-autonomous-sprint.md)).
- `examples/`: Validation fixtures for both skills.
- `docs/`: Repository-level documentation (PRDs, Issues, ADRs).

## Usage

The sensemaking system provides two automated diagnostic workflows that analyze your project and produce recommendations. You then choose which implementation workflow to run next.

### Quick Start: Choose Your Diagnostic Workflow

**Fast Path** — When you have a clear repo goal:
```bash
python scripts/orchestration-runner.py fast-path-workflow --mode guided_execution
```
**Chains**: `repo-sensemaker`  
**Output**: Repository Sensemaking Brief (identifies weakest boundary + recommended workflows)  
**Time**: ~5 minutes

**Full Fog Path** — When the problem is ambiguous:
```bash
python scripts/orchestration-runner.py full-fog-workflow --mode guided_execution
```
**Chains**: `problem-framer` → `unknowns-mapper` → `repo-sensemaker` → `prompt-handoff`  
**Output**: Problem Frame + Unknowns Map + Repository Brief + Ready-to-copy Prompts  
**Time**: ~20 minutes

### Execution Flow (Default: guided_execution mode)

1. **Invoke diagnostic workflow** — `orchestration-runner.py <workflow-name>`
2. **Provide initial inputs** — vague problem (Full Fog Path) or repository context (Fast Path)
3. **Skills chain automatically** with approval gates at each step:
   - Step 1 completes → Orchestrator pauses
   - You review the artifact → Approve/Deny
   - If approved → continues to Step 2
   - If denied → workflow halts
4. **Final artifact** is a brief with recommendations:
   - Section 12: Recommended workflow (e.g., `docs-architecture`)
   - Section 13: Machine-readable handoff (workflow ID, execution mode, inputs)
   - Section 14: Ready-to-copy prompts for next skill

### Next Steps: Run Implementation Workflow

After the diagnostic workflow completes, run the recommended workflow:

```bash
# Example: if brief recommends docs-architecture
python scripts/orchestration-runner.py docs-architecture --mode guided_execution
```

Or copy the ready-to-copy prompt from the brief and paste it directly into the next skill.

### Advanced: Other Execution Modes

- **`plan_only`**: See what WOULD happen without executing (safe for testing)
- **`prompt_chain`**: Generate all prompts; user runs them manually
- **`autonomous_execution`**: Automatic skill chaining with gates (but fewer pauses)
- **`yolo_execution`**: Full automation, no gates (for trusted workflows only)

See [Execution Modes Reference](docs/orchestration-patterns.md#execution-modes) for details.

## Skill Invocation & Downstream Workflows

### Automatic Skill Chaining (Phase 5 Complete)

In `guided_execution`, `autonomous_execution`, and `yolo_execution` modes, `orchestration-runner.py` automatically chains skills within a workflow. No external agent invocation is required.

### Downstream Implementation Workflows

When a sensemaking workflow routes to an implementation workflow (e.g., `product-implementation-workflow`, `ui-implementation-workflow`, `implementation-workflow`, `docs-implementation-workflow`), the orchestrator automatically invokes those workflows in the same execution mode.

### Optional Downstream Skill Packs

For product, UI, and implementation workflows, this repository assumes the following skill packs are optionally installed:

- [Product Manager Skills](https://github.com/ThorStarlord/pm-skills)
- [Matt Pocock Skills](https://github.com/mattpocock/skills)
- [Interface Skills](https://github.com/ThorStarlord/interface-skills)

If these are not installed:
- **In `plan_only` mode**: The orchestrator produces copy-paste prompts for manual invocation
- **In execution modes**: The orchestrator fails with a clear error indicating which skill pack is required

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
