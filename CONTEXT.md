# Context: Sensemaking Skills

## Goal
To provide a meta-routing layer for AI agents that turns project uncertainty ("fog") into actionable problem frames, research paths, and specific skill recommendations.

## Engineering Philosophy
This repository is built on **Artifact-Driven Agentic Engineering**. We treat artifacts as the API between skills to ensure reliability, auditability, and safety. 
> See [docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md](docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md) for the deep theory.

## Core Principles
1. **Fog First**: Always classify the type of uncertainty before proposing a solution.
2. **Artifacts as API**: Skills communicate via durable artifacts, not conversation memory.
3. **Boundary Rule**: Do not perform downstream work (building) by default.
4. **Anti-Causal Confusion**: Classify defect source (Skill vs. Fixture) before any repair.
5. **Human in the Loop**: Skills provide judgment, but humans approve usefulness.

## Routing Source of Truth
| Resource | Purpose |
|----------|---------|
| `skill-registry.yaml` | Find specific tools for a task |
| `workflow-registry.yaml` | Find the sequence of skills for a project mode |
| `examples/skill-tests/` | Behavioral evidence and test fixtures |
| `docs/philosophy/` | Engineering rationale and FMEA taxonomies |
| `docs/mode-coverage.yaml` | Execution mode proving status and run log references |

## Domain Language
- **Fog**: The state of project uncertainty (Product, Architecture, Strategy, or Routing).
- **Flagship Skills**: The repo contains a five-skill sensemaking pipeline: `problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-orchestrator`, and `prompt-handoff`.
- **Sensemaking Brief**: The primary diagnostic artifact (14 sections). It must identify the "weakest boundary" and provide file-level evidence and excerpts.
- **Orchestration Plan**: The procedural artifact (11 sections). It defines the workflow, execution mode, and approval gates.
- **Execution Modes**: The system supports `plan_only`, `prompt_chain`, `guided_execution`, `autonomous_execution`, and `yolo_execution`.
- **YOLO Execution**: High-velocity automation that bypasses approval gates for local skills. Requires explicit opt-in and feature branches.
- **Skill Split**: Diagnosis (`repo-sensemaker`) is separated from Action (`workflow-orchestrator`) to ensure human-in-the-loop validation.
- **Object Under Pressure**: The specific artifact or system boundary that is most ambiguous.
- **Weakest Boundary**: The most fragile or unenforced point in a repository. Diagnosed by repo-sensemaker via evidence-backed analysis of signal-gap boundaries.
- **Approval Gates**: Mandatory review points in an orchestration workflow. In `yolo_execution` mode, validators replace gates as the safety mechanism — gates are bypassed, but post-step validation is zero-tolerance.
- **Harden Only Where Pressured**: A principle for post-run system improvement — restrict changes to boundaries where live execution exposes a **repeatable failure boundary** (same failure class across independent runs). Isolated one-off data issues are fixed in the artifact but do not trigger system hardening. Prevents preemptive over-engineering based on theory alone. Validated by the first fast-local-diagnostic run: the brief theorized "Contract Mismatch" but the run stressed only weakness-type and logic-trace authoring, and those were single-occurrence data issues — no structural hardening was warranted.

- **Repeatable Failure Boundary**: A failure class that recurs across independent live runs, signaling a systemic gap rather than an isolated data-quality issue. Determines whether a friction point triggers system hardening (repeatable) or artifact-level correction (single occurrence). Example: if UNKNOWN_WEAKNESS_TYPE occurs in two different workflow runs with different authors, that's a repeatable pattern warranting tooling improvement; a one-time authoring mistake is not.
- **TDD Validator Cycle**: The red-green-refactor loop triggered when a Level 3 validator fails during a workflow run. Failure = RED, artifact data fix = GREEN, re-validation pass = REFACTOR. Demonstrated in the first YOLO run when validate-brief.py caught UNKNOWN_WEAKNESS_TYPE and NO_LOGIC_TRACE.
- **Tracer Bullets**: AFK-compatible vertical slices of implementation.
- **Validator Verification Suite**: A repeatable verification mechanism that checks validator behavior against positive and negative fixtures. It confirms that valid artifacts pass, invalid artifacts fail, and expected failures fail for the intended reason. Now enforces mandatory fixture coverage for all validator scripts.

## Tech Stack
- Markdown-based skill definitions (`SKILL.md`).
- YAML-based registries and agent definitions.
- Relative linking for package portability.

## Skills Split
1. **repo-sensemaker**: Diagnostic. Finds the weakest boundary.
2. **workflow-orchestrator**: Procedural. Acts on the weak point via gated sequences.

## Ecosystems
- **Interface Skills**: Spec Packages and UI validation.
- **Matt Pocock Skills**: Engineering rigor, TDD, and grilling.
- **Product Manager Skills**: Discovery, PRDs, and Strategy.

## Automation & Validation (scripts/)
The repository uses a Python-based three-level validator hierarchy to enforce artifact integrity and safety:

- **Level 1 — Structural** (`validate-repo.py`): Repository-wide consistency checks across registries and examples. Runs pre-flight before any workflow that mutates the repo.
- **Level 2 — Generic** (`validate-artifact.py`): Universal contract checks (sections, machine fields, no absolute paths). Runs after every artifact-producing step.
- **Level 3 — Specialized** (one per artifact type): Semantic checks requiring registry cross-references. Currently:
  - `validate-brief.py` — enforces evidence grounding, weakness-type recognition, workflow-ID validation
  - `validate-plan.py` — verifies workflow steps, execution modes, approval gates, stop conditions
  - `validate-skill-improvement-plan.py` — enforces formal failure mode classification and anti-overfitting
  - `validate-usage-research-report.py` — checks semantic scores, role boundaries, evidence grounding
  - `validate-prompt-handoff.py` — checks target skill exists in registry, artifact refs are real, stop conditions have content
- **`validate-output.py`**: Dispatcher that delegates to per-artifact validators via `artifact-contracts.yaml`. This is the normal validation path — all runs should use it instead of calling validators directly.
- **`validate-run-log.py`**: Validates run log structure against the template specification. Checks header fields, step structure, gate recording consistency (gate_result, approved_at, approved_by), pre-flight documentation, and path hygiene.
- **`analyze-run-failures.py`**: Builds a failure ledger from all run logs in a directory. Detects repeatable failure boundaries (same error code across 2+ independent runs) per the Repeatable Failure Boundary principle.
- **`_validator_utils.py`**: Shared utility module for registry loading, path resolution, and error formatting.

In YOLO and autonomous execution modes, validators function as **zero-tolerance safety gates**: any failure triggers an immediate hard stop and rollback recommendation. See [validator-stack-policy.md](skills/workflow-orchestrator/references/validator-stack-policy.md) for execution order.
