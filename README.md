# Sensemaking Skills

A collection of skills designed to turn vague project uncertainty into clear problem frames, research paths, decisions, and next-step prompts.

The repository is organized around a clean split: **Diagnosis** (`repo-sensemaker`) and **Orchestration** (`workflow-planner`).

---

## Quick Start

### Install

```bash
pip install sensemaking-skills
```

### Analyze Your Repository

```bash
# Initialize (one-time setup)
sensemaking-skills init --repo /path/to/your/repo

# Run analysis
sensemaking-skills analyze --repo /path/to/your/repo
```

### Check Results

Your analysis artifacts are in `.sensemaking/artifacts/`:

```bash
# View the diagnostic brief
cat /path/to/your/repo/.sensemaking/artifacts/repository_sensemaking_brief.md

# View recommended workflows
cat /path/to/your/repo/.sensemaking/artifacts/workflow_orchestration_plan.md
```

### Next Steps

- **Manual Path** (inspect between steps): See [INSTALLATION.md](INSTALLATION.md#manual-path-full-control)
- **Automation Path** (single command, full pipeline): See [INSTALLATION.md](INSTALLATION.md#automation-path-full-speed)
- **Extend the System**: See [EXTENDING.md](EXTENDING.md) to add custom skills
- **Python API**: See [API.md](API.md) to integrate into your code

### Full Documentation

- [INSTALLATION.md](INSTALLATION.md) — Complete setup and usage guide
- [EXTENDING.md](EXTENDING.md) — Create custom skills and workflows
- [API.md](API.md) — Python API reference and examples
- [GETTING_STARTED.md](GETTING_STARTED.md) — Detailed walkthroughs and workflows

---

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

### Core Sensemaking (6 skills)

The foundation layer: diagnostic and orchestration skills that identify problems and route work.

- **`problem-framer`** — Converts vague ideas into structured Problem Frames. Identifies the "problem under the problem" and "object under pressure."
- **`unknowns-mapper`** — Separates Knowns, Unknowns, Assumptions, and Risks. Defines research paths and stopping rules. Can dynamically trigger research skills based on fog clarity.
- **`repo-sensemaker`** — Produces a 14-section Repository Sensemaking Brief. Audits repository health, identifies the "weakest boundary," cites file-level evidence.
- **`workflow-planner`** — Consumes a Brief and produces a Workflow Orchestration Plan. Selects execution mode and defines approval gates.
- **`sensemaking-docs-reconciler`** — Aligns repository docs, registries, and artifact contracts to resolve drift.
- **`handoff`** — Packages sensemaking context into a session summary with machine-readable fields for downstream skills.

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
  ↓ (handoff)
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

| Workflow ID | Skill Sequence |
|---|---|
| `implementation-workflow` | docs-aligner → to-prd → to-issues → triage → tdd → handoff |
| `product-implementation-workflow` | docs-aligner → discovery → opportunity-tree → to-prd → to-issues → triage → tdd → handoff |
| `ui-implementation-workflow` | docs-aligner → ui-flow → ui-screen-spec → to-issues → triage → tdd → handoff |
| `docs-implementation-workflow` | docs-aligner → to-prd → handoff |

*Note: `implementation-workflow` is auto-invoked from the default diagnostic workflow.*

### Product Strategy Skill Workflows

| Workflow ID | Skill Sequence |
|---|---|
| `product-discovery-sprint` | persona → discovery → interview-synthesis → opportunity-tree → hypothesis |
| `product-strategy-sprint` | lean-canvas → north-star → okr → roadmap → stakeholder-update |
| `product-autonomous-sprint` | persona → discovery → opportunity-tree → hypothesis → prd → user-stories → acceptance-criteria → handoff |
| `product-to-issues` | to-prd → to-issues → triage |

### Specialized Skill Workflows

| Workflow ID | Skill Sequence |
|---|---|
| `experimental-autonomous-sprint` | docs-aligner → to-prd → to-issues → triage → tdd → handoff |
| `docs-architecture` | docs-aligner → handoff |
| `skill-maintenance-loop` | skill-maintainer → handoff |

---

## Repository Structure

- `skills/`:
  - `repo-sensemaker/`: Diagnostic skill and templates.
  - `workflow-planner/`: Planning skill and registries.
- `workflows/`: Composite skill chains (e.g., [Experimental Autonomous Sprint](workflows/experimental-autonomous-sprint.md)).
- `examples/`: Validation fixtures for both skills.
- `docs/`: Repository-level documentation (PRDs, Issues, ADRs).

## Quick Start

**👉 See [GETTING_STARTED.md](GETTING_STARTED.md) for detailed usage instructions**

Choose your path:

### Manual Path (Full Control)
```bash
# Run diagnostic workflow
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution

# Read output, then manually invoke implementation workflow
python scripts/workflow-runtime.py --workflow product-implementation-workflow --mode guided_execution
```

### Automation Path (Full Speed)
```bash
# Single command: entire pipeline auto-chains based on fog_type
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode autonomous_execution
```

---

## Usage

The system supports two invocation paths with flexible execution modes:

### Default Workflow Chain

The system uses a **multi-stage default workflow chain with fog-type-aware routing** for production use:

```
fast-path-workflow (DEFAULT) → Diagnose fog type
  ↓ (auto-invokes in autonomous_execution mode)
  ├→ product-implementation-workflow (if product_fog detected)
  ├→ ui-implementation-workflow (if ui_fog detected)
  ├→ docs-implementation-workflow (if docs_fog detected)
  └→ implementation-workflow (if architecture_fog detected)
```

### Two Invocation Paths

1. **Manual Path**: Full control, inspect artifacts between stages
   - User explicitly runs each workflow
   - User reviews output and decides next step
   - Best for debugging, exploration, complex decisions

2. **Automation Path**: Full speed, deterministic routing
   - Single invocation runs entire pipeline
   - System auto-detects recommended workflow
   - System auto-chains based on fog_type (in autonomous mode)
   - Best for production, fast iteration, known workflows

### Execution Modes

| Mode | Gates | Speed | Use Case |
|------|-------|-------|----------|
| `guided_execution` | Pause at every gate (user approves) | Slowest | Development, exploration |
| `autonomous_execution` | Auto-approve valid gates | Fast | Production, automation |
| `prompt_chain` | Generate prompts for manual execution | Fast | Multi-step planning |
| `plan_only` | No execution, show plan only | Instant | Validation, planning |
| `yolo_execution` | Bypass gates; validators still enforce | Fastest | Experimental only |

### Examples

```bash
# Manual path with control
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode guided_execution

# Automation path with auto-chaining
python scripts/workflow-runtime.py --workflow fast-path-workflow --mode autonomous_execution

# List all workflows
python scripts/workflow-runtime.py --list-workflows
```

**👉 See [GETTING_STARTED.md](GETTING_STARTED.md) for complete documentation, real-world examples, and troubleshooting**

This will:
1. Execute `full-local-sensemaking` (diagnoses your repository and classifies fog type)
2. Automatically routes to the appropriate implementation workflow based on fog type
3. Chains to the implementation workflow with automatic progression
4. Return exit code 0 on success, 2 on failure, 3 if paused

**What's new**: The system now intelligently detects whether your problem is UI-specific, product-focused, documentation-related, or architecture-focused, and routes to the specialized workflow accordingly.

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

### Execution Modes

The system supports five execution modes ranging from fully automatic to read-only:

| Mode | Execution | Approval Gates | Best For | Command |
|------|-----------|---------------|----------|---------|
| **`yolo_execution`** (DEFAULT) | **Automatic** | Bypassed (validators enforce safety) | Production, trusted repos | `python scripts/workflow-runtime.py` |
| **`autonomous_execution`** | **Automatic** | Auto-approved | CI/CD, unattended runs | `--mode autonomous_execution` |
| **`guided_execution`** | **Manual** | Required at each step (pause + approve/deny) | Learning the system, high-value decisions | `--mode guided_execution` |
| **`prompt_chain`** | **Manual** | None (user runs generated prompts) | Air-gapped environments | `--mode prompt_chain` |
| **`plan_only`** | Read-only | None (no execution) | Dry-run, what-if analysis | `--mode plan_only` |

**How automation works:** The script reads the workflow from the registry, executes each skill step in sequence, validates artifacts, and chains to the next step automatically — no manual prompt invocation needed.

**How manual execution works:** Run with `--mode prompt_chain` — the script generates ready-to-copy prompts for each skill step. You paste each prompt into the target agent and invoke the next step yourself.

**Guided flow step by step:**

1. `python scripts/workflow-runtime.py --workflow <workflow-name> --mode guided_execution`
2. Provide initial inputs (vague problem or repository context)
3. Skills chain automatically with approval gates:
   - Step completes → orchestrator pauses
   - Review the artifact → Approve/Deny
   - If approved → continues to next step
   - If denied → workflow halts
4. Final artifact includes ready-to-copy prompts for the next skill

### UI-Specific Workflows

For UI/frontend redesign projects, the system provides specialized workflows.

> **Prerequisite for direct UI workflows**: `ui-diagnostic-workflow` and
> `ui-implementation-workflow` consume a `context_artifacts` bundle produced by a prior
> sensemaking run (problem frame, unknowns map, sensemaking brief, orchestration plan).
> Run them either **after** a diagnostic workflow in the same session, or let the
> diagnostic workflow **auto-invoke** them. A direct cold-start with no context now
> **fails fast at pre-flight** with guidance, rather than producing an empty run.

**Automatic UI Routing (recommended)** — Diagnose first, then route automatically. Pass a
problem statement so intent reinforces the codebase diagnosis:
```bash
python scripts/workflow-runtime.py \
  "Our frontend components are inconsistent and we need a coherent design system" \
  --workflow full-local-sensemaking \
  --mode guided_execution \
  --executor claude-code
# Diagnoses fog type, then auto-invokes ui-implementation-workflow if ui_fog is detected
```

**UI Diagnostic Workflow** — Analyze UI scope before committing to implementation
*(requires context_artifacts — see prerequisite above)*:
```bash
python scripts/workflow-runtime.py --workflow ui-diagnostic-workflow --mode guided_execution
```
**Output**: `ui_specification` artifact with screen inventory, design system assessment, and interaction patterns  
**Chains to**: `ui-implementation-workflow` (if you approve the scope)

**UI Implementation Workflow** — Full redesign workflow with TDD
*(requires context_artifacts — see prerequisite above)*:
```bash
python scripts/workflow-runtime.py --workflow ui-implementation-workflow --mode guided_execution
```
**Steps**: Domain alignment → UI flows → Screen specs → Decompose into issues → Triage → TDD implementation

See [docs/examples/ui-routing-example.md](docs/examples/ui-routing-example.md) for a complete example of UI fog detection and implementation.

### Fog Type Classification

The system automatically classifies repository problems using **Fog Type Classification**:

| Fog Type | Signals | Recommended Workflow | When to Use |
|----------|---------|---------------------|-----------|
| **`ui_fog`** | Missing flow docs, scattered components, routing complexity, design gaps | `ui-implementation-workflow` | Dashboard redesigns, UI consistency projects |
| **`product_fog`** | Vague features, missing specs, unclear requirements | `product-implementation-workflow` | New feature development, unclear user needs |
| **`docs_fog`** | Missing documentation, unclear specs, knowledge silos | `docs-implementation-workflow` | Architecture documentation, API docs |
| **`architecture_fog`** | Code structure issues, high coupling, unclear boundaries | `implementation-workflow` | Refactoring, performance improvements |

See [docs/CONTEXT.md](docs/CONTEXT.md) for detailed classification rules and [skills/repo-sensemaker/references/ui-fog-signals.md](skills/repo-sensemaker/references/ui-fog-signals.md) for UI-specific signal detection.

### Next Steps: Implementation Workflow

**If using default workflow chain** (`full-local-sensemaking`):
- The appropriate implementation workflow is **automatically invoked** after diagnosis completes
- No manual intervention needed
- Both workflows run in the same execution mode

**If using alternative diagnostic workflows** (fast-path-workflow, full-fog-workflow, ui-diagnostic-workflow, etc.):
- After the diagnostic workflow completes, manually run the recommended workflow:

```bash
# Example: if brief recommends ui-diagnostic-workflow
python scripts/workflow-runtime.py --workflow ui-diagnostic-workflow --mode guided_execution
```

- Or copy the ready-to-copy prompt from the brief and paste it directly into the next skill

### CLI Reference

```
usage: workflow-runtime.py [--workflow WORKFLOW] [--mode MODE]
                           [--scope {soft,hard,advisory}]
                           [--repo-root REPO_ROOT] [--plan-out PLAN_OUT]
                           [--log-dir LOG_DIR] [--list-workflows]
                           [--resume] [--executor EXECUTOR]
                           [--gate-decision {auto-approve,auto-deny}]
                           [--use-fixtures] [--chained]
                           [problem]
```

| Argument | Description | Default |
|---|---|---|
| `problem` | Optional user problem statement or goal | — |
| `--workflow` | Explicit workflow ID (overrides default chain) | `full-local-sensemaking` |
| `--mode` | Execution mode | `yolo_execution` |
| `--scope` | How strictly the problem constrains analysis: `soft`, `hard`, `advisory` | `soft` |
| `--repo-root` | Repository root directory | `.` |
| `--plan-out` | Output path for the orchestration plan | auto |
| `--log-dir` | Directory for run log output | auto |
| `--list-workflows` | List all registered workflow IDs | off |
| `--resume` | Resume a paused execution | off |
| `--executor` | Skill executor: `dry-run`, `prompt-chain`, `claude-code`, `api` | `claude-code` |
| `--gate-decision` | Non-interactive gate decision for testing: `auto-approve`, `auto-deny` | — |
| `--use-fixtures` | Use fixture artifacts instead of executing real skills | off |
| `--chained` | (Internal) Invoked as a chained workflow from another run | off |
| `--from-session` | Reuse parent session artifacts (manual invocation path) | — |

## Execution Model

This repository supports a hybrid execution model:

- **Runner-led orchestration**: `workflow-runtime.py` owns the control loop, calling worker skills, validating artifacts, managing gates, and recording run evidence. Use this for repeatable, production-like workflows where the full sequence must be machine-auditable.
- **Skill-led orchestration**: An orchestrator skill owns the semantic control loop. Worker skills create artifacts. Deterministic helper scripts (`validate-*.py`, `record-step.py`) create, validate, and record artifacts. Use this for exploratory or AI-native workflows where the next step depends on judgment.
- In both models, proof comes from durable artifacts, validator results, and an append-only run ledger — not from agent memory.

See [CONTEXT.md](CONTEXT.md) for the full principle under **Orchestration Principles → Orchestration Ownership: Skills Act, Scripts Record**.

## Skill Invocation & Downstream Workflows

### Automatic Skill Chaining (Phase 5 Complete)

In `guided_execution`, `autonomous_execution`, and `yolo_execution` modes, `workflow-runtime.py` automatically chains skills within a workflow. No external agent invocation is required.

### Downstream Implementation Workflows

When a sensemaking workflow routes to an implementation workflow (e.g., `product-implementation-workflow`, `ui-implementation-workflow`, `implementation-workflow`, `docs-implementation-workflow`), the orchestrator automatically invokes those workflows in the same execution mode.

### Optional Downstream Skill Packs

For product, UI, and implementation workflows, this repository assumes the following skill packs are optionally installed:

- [Product Manager Skills](https://github.com/ThorStarlord/pm-skills) — For discovery, PRDs, strategy, and Go-To-Market
- [Matt Pocock Skills](https://github.com/mattpocock/skills) — For engineering rigor, TDD, and docs alignment
- [Interface Skills](https://github.com/ThorStarlord/interface-skills) — For UI flows, screen specs, and design systems

**Graceful Degradation Strategy**:

| Scenario | In `plan_only` Mode | In Execution Modes | Behavior |
|----------|-------|----------|----------|
| **All packs installed** | ✓ Full pipeline executes normally | ✓ Workflows run end-to-end | Recommended setup |
| **One pack missing** | ✓ Generates copy-paste prompts for missing steps | ✗ Fails with clear error message and recovery instructions | Use `plan_only` to generate prompts you run manually |
| **Multiple packs missing** | ✓ Generates prompts for all missing skills | ✗ Fails at first missing skill; tells you which pack to install | Install missing packs or use `plan_only` to continue |

**Example: Missing Matt Pocock Skills**

```bash
# In plan_only mode: you get ready-to-copy prompts
python scripts/workflow-runtime.py --workflow product-implementation-workflow --mode plan_only
# → Generates prompts for: docs-aligner, discovery, opportunity-tree, to-prd, to-issues, triage, tdd
# You can copy each prompt and run manually

# In autonomous_execution mode: you get a clear error
python scripts/workflow-runtime.py --workflow product-implementation-workflow --mode autonomous_execution
# → ERROR: Missing skill pack 'matt-pocock-skills' required for 'tdd' step
# → Install with: git clone https://github.com/mattpocock/skills
```

**Recommended Setup**:

For full automation (no manual steps), install all three optional packs:

```bash
git clone https://github.com/ThorStarlord/pm-skills your-claude-code-dir/skills/
git clone https://github.com/mattpocock/skills your-claude-code-dir/skills/
git clone https://github.com/ThorStarlord/interface-skills your-claude-code-dir/skills/
```

For learning/exploration, use `plan_only` mode and manually run generated prompts—no additional skill packs required.

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
