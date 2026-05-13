# Context: Sensemaking Skills

## Goal
To provide a meta-routing layer for AI agents that turns project uncertainty ("fog") into actionable problem frames, research paths, and specific skill recommendations.

## Core Principles
1. **Fog First**: Always classify the type of uncertainty before proposing a solution.
2. **Boundary Rule**: Do not perform downstream work (building) by default. Focus on making the work answerable.
3. **Pragmatic Routing**: Use the `skill-registry.yaml` to find the most specific tool for the job.
4. **Human in the Loop**: Skills provide judgment, but humans approve usefulness.

## Domain Language
- **Fog**: The state of project uncertainty (Product, Architecture, Strategy, or Routing).
- **Repository Sensemaking Brief**: The canonical 11-section output of `repo-sensemaker`.
- **Workflow Orchestration Plan**: The canonical 10-section output of `workflow-orchestrator`.
- **Object Under Pressure**: The specific artifact or system boundary that is most ambiguous.
- **Weakest Boundary**: The most fragile or unenforced point in a repository.
- **Approval Gates**: Mandatory review points in an orchestration workflow.
- **Tracer Bullets**: AFK-compatible vertical slices of implementation.

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
