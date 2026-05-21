# Sensemaking Skills

A collection of skills designed to turn vague project uncertainty into clear problem frames, research paths, decisions, and next-step prompts.

The repository is organized around a clean split: **Diagnosis** (`repo-sensemaker`) and **Orchestration** (`workflow-planner`).

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
- A split between **Diagnosis** (`repo-sensemaker`) and **Orchestration** (`workflow-planner`).
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
- **`workflow-planner`** — Consumes a Brief and produces a Workflow Orchestration Plan. Selects execution mode and defines approval gates.
- **`sensemaking-docs-reconciler`** — Aligns repository docs, registries, and artifact contracts to resolve drift.
- **`prompt-handoff`** — Packages sensemaking context into a ready-to-copy Prompt for downstream skills.

### Drafting & Implementation (6 skills)

Transform diagnostic outputs into specifications and implementation plans.

- **`docs-aligner`** — Stress-test a plan against existing domain documentation. Sharpens terminology and updates docs inline.
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
  ↓ (workflow-planner)
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

## Skill Workflows

The repository registers 17 skill workflows in `workflow-planner/references/workflow-registry.yaml`. Each chains skills into an ordered sequence that processes fog into actionable artifacts.

### Diagnostic Skill Workflows

| Workflow ID | Skill Sequence | Default |
|---|---|---|
| `full-local-sensemaking` | problem-framer → unknowns-mapper → (discovery?) → repo-sensemaker → handoff | **DEFAULT** |
| `full-fog-workflow` | problem-framer → unknowns-mapper → repo-sensemaker → workflow-planner | |
| `fast-path-workflow` | repo-sensemaker → workflow-planner | |
| `fast-local-diagnostic` | repo-sensemaker → handoff | |
| `setup-sensemaking-repo` | setup-sensemaking-skills → repo-sensemaker → prompt-handoff | |
| `docs-contract-reconciliation` | repo-sensemaker → sensemaking-docs-reconciler → prompt-handoff | |
| `autonomous-sprint-preflight` | repo-sensemaker → prompt-handoff | |

### Implementation Skill Workflows

| Workflow ID | Skill Sequence | |
|---|---|---|
| `implementation-workflow` | docs-aligner → to-prd → to-issues → triage → tdd → handoff | (auto-invoked from default) |
| `product-implementation-workflow` | docs-aligner → discovery → opportunity-tree → to-prd → to-issues → triage → tdd → handoff | |
| `ui-implementation-workflow` | docs-aligner → ui-flow → ui-screen-spec → to-issues → triage → tdd → handoff | |
| `docs-implementation-workflow` | docs-aligner → to-prd → handoff | |

### Product Strategy Skill Workflows

| Workflow ID | Skill Sequence | |
|---|---|---|
| `product-discovery-sprint` | persona → discovery → interview-synthesis → opportunity-tree → hypothesis | |
| `product-strategy-sprint` | lean-canvas → north-star → okr → roadmap → stakeholder-update | |
| `product-autonomous-sprint` | persona → discovery → opportunity-tree → hypothesis → prd → user-stories → acceptance-criteria → handoff | |
| `product-to-issues` | to-prd → to-issues → triage | |

### Specialized Skill Workflows

| Workflow ID | Skill Sequence | |
|---|---|---|
| `experimental-autonomous-sprint` | docs-aligner → to-prd → to-issues → triage → tdd → handoff | |
| `docs-architecture` | docs-aligner → handoff | |
| `skill-maintenance-loop` | skill-maintainer → handoff | |

---

## Repository Structure

- `skills/`:
  - `repo-sensemaker/`: Diagnostic skill and templates.
  - `workflow-planner/`: Planning skill and registries.
- `workflows/`: Composite skill chains (e.g., [Experimental Autonomous Sprint](workflows/experimental-autonomous-sprint.md)).
- `examples/`: Validation fixtures for both skills.
- `docs/`: Repository-level documentation (PRDs, Issues, ADRs).

## Usage

### Default Workflow Chain

The system uses a **two-stage default workflow chain** for production use:

```
full-local-sensemaking (DEFAULT)
  ↓ (auto-invokes on completion)
implementation-workflow (AUTOMATIC)
```

Simply run:
```bash
python scripts/workflow-runtime.py
```

This will:
1. Execute `full-local-sensemaking` (diagnoses your repository)
2. Automatically chain to `implementation-workflow` (transforms diagnosis into implementation)
3. Return exit code 0 on success, 2 on failure, 3 if paused

To use a different execution mode (default is `yolo_execution`):
```bash
python scripts/workflow-runtime.py --mode guided_execution
```

To use a different workflow explicitly:
```bash
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution
```

---

### Alternative: Choose Your Own Diagnostic Workflow

For special cases, you can manually select a different diagnostic workflow. These do NOT auto-chain to implementation-workflow:

**Fast Path** — When you have a clear repo goal:
```bash
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution
```
**Chains**: `repo-sensemaker`  
**Output**: Repository Sensemaking Brief (identifies weakest boundary + recommended workflows)  
**Time**: ~5 minutes  
**Next**: You choose the implementation workflow manually

**Full Fog Path** — When the problem is ambiguous:
```bash
python scripts/workflow-runtime.py --workflow full-fog-workflow --mode guided_execution
```
**Chains**: `problem-framer` → `unknowns-mapper` → `repo-sensemaker` → `prompt-handoff`  
**Output**: Problem Frame + Unknowns Map + Repository Brief + Ready-to-copy Prompts  
**Time**: ~20 minutes  
**Next**: You choose the implementation workflow manually

### Execution Flow (Default: yolo_execution mode)

The default execution mode is `yolo_execution` — full automation that bypasses approval gates for local skills. To use guided execution with approval pauses, add `--mode guided_execution` to the command.

**With default mode (yolo_execution):**
```bash
python scripts/workflow-runtime.py full-local-sensemaking
# Runs with full automation, no approval gates
```

**With guided mode (manual approvals):**
```bash
python scripts/workflow-runtime.py full-local-sensemaking --mode guided_execution
```

**Execution flow with guided mode:**

1. **Invoke diagnostic workflow** — `workflow-runtime.py <workflow-name> --mode guided_execution`
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

### Next Steps: Implementation Workflow

**If using default workflow chain** (`full-local-sensemaking`):
- The `implementation-workflow` is **automatically invoked** after diagnosis completes
- No manual intervention needed
- Both workflows run in the same execution mode

**If using alternative diagnostic workflows** (fast-path-workflow, full-fog-workflow, etc.):
- After the diagnostic workflow completes, manually run the recommended workflow:

```bash
# Example: if brief recommends docs-architecture
python scripts/workflow-runtime.py --workflow docs-architecture --mode guided_execution
```

- Or copy the ready-to-copy prompt from the brief and paste it directly into the next skill

### Execution Modes

The system supports five execution modes ranging from fully automatic to read-only:

| Mode | Execution | Approval Gates | Best For | Command |
|------|-----------|---------------|----------|---------|
| **`yolo_execution`** (DEFAULT) | **Automatic** | Bypassed (validators enforce safety) | Production, trusted repos | `python scripts/workflow-runtime.py` |
| **`autonomous_execution`** | **Automatic** | Auto-approved | CI/CD, unattended runs | `--mode autonomous_execution` |
| **`guided_execution`** | **Manual** | Required at each step | Learning the system, high-value decisions | `--mode guided_execution` |
| **`prompt_chain`** | **Manual** | None (user runs prompts) | Air-gapped environments | `--mode prompt_chain` |
| **`plan_only`** | Read-only | None (no execution) | Dry-run, what-if analysis | `--mode plan_only` |

See [Execution Modes Reference](docs/orchestration-patterns.md#execution-modes) for details.

## Skill Invocation & Downstream Workflows

### Automatic Skill Chaining (Phase 5 Complete)

In `guided_execution`, `autonomous_execution`, and `yolo_execution` modes, `workflow-runtime.py` automatically chains skills within a workflow. No external agent invocation is required.

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
- New skill entries go in `workflow-planner/references/skill-registry.yaml`.
- New workflows go in `workflow-planner/references/workflow-registry.yaml`.
- New examples must include an expected behavior checklist.

## V1 Definition of Done (New Architecture)
- All five core skills are package-valid with separate `agents/openai.yaml`.
- `repo-sensemaker` produces a 14-section diagnostic brief with evidence.
- `workflow-planner` produces a 10-section orchestration plan.
- Registry-based routing is fully machine-readable.
- Negative fixtures exist to test refusal-to-act.
