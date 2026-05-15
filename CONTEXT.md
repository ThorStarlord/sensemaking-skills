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

## Domain Language
- **Fog**: The state of project uncertainty (Product, Architecture, Strategy, or Routing).
- **Flagship Skills**: The repo contains a five-skill sensemaking pipeline: `problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-orchestrator`, and `prompt-handoff`.
- **Sensemaking Brief**: The primary diagnostic artifact (14 sections). It must identify the "weakest boundary" and provide file-level evidence and excerpts.
- **Orchestration Plan**: The procedural artifact (11 sections). It defines the workflow, execution mode, and approval gates.
- **Execution Modes**: The system supports `plan_only`, `prompt_chain`, `guided_execution`, `autonomous_execution`, and `yolo_execution`.
- **YOLO Execution**: High-velocity automation that bypasses approval gates for local skills. Requires explicit opt-in and feature branches.
- **Skill Split**: Diagnosis (`repo-sensemaker`) is separated from Action (`workflow-orchestrator`) to ensure human-in-the-loop validation.
- **Object Under Pressure**: The specific artifact or system boundary that is most ambiguous.
- **Weakest Boundary**: The most fragile or unenforced point in a repository.
- **Approval Gates**: Mandatory review points in an orchestration workflow.
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
The repository uses a Python-based validation stack to enforce artifact integrity and safety:
- **`validate-artifact.py`**: Enforces structural contracts for Sensemaking Briefs and Orchestration Plans.
- **`validate-repo.py`**: Performs global consistency checks across registries and examples.
- **`validate-skill-improvement-plan.py`**: Hardened gate for the maintenance loop; enforces formal failure mode classification and prevents logic overfitting.
- **`validate-usage-research-report.py`**: Ensures research evidence is grounded and machine-readable.
