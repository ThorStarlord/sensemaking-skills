# Sensemaking Skills

A collection of skills designed to turn vague project uncertainty into clear problem frames, research paths, decisions, and next-step prompts.

The flagship skill is `project-sensemaker`, which routes unclear work to the right downstream method, skill, or artifact.

## Core Philosophy

"I do not know what I need because I do not yet understand what I am building."

Sensemaking skills sit **before** specialized tools. They handle the moment of "fog" where the type of problem is not yet known.

## What this is / is not

### What this is
- A meta-routing layer to convert project uncertainty ("fog") into actionable next steps.
- A way to choose the right specialized workflow (PM, Engineering, UI) before building.
- A structural enforcement tool for mental model alignment.

### What this is not
- A replacement for specialized tools (PM skills, Matt Pocock skills, Interface Skills).
- An implementation or coding agent (by default).
- A PRD or Issue generator (it routes to these, it doesn't replace them).

## Core Artifact: Sensemaking Brief

A **Sensemaking Brief** is the primary output of `project-sensemaker`. It does not solve the downstream work; it makes the work answerable by naming:
- The fog type and object under pressure.
- Knowns, unknowns, and assumptions.
- Candidate paths and the weakest boundary.
- The smallest useful next step and a ready-to-copy prompt for the next skill.

## Flagship Skill: `project-sensemaker`

Turns vague project ideas, uncertainty, or early product fog into researched, concrete next-step options.

### Ecosystems We Route To

This toolkit acts as a meta-layer, helping you choose between:
- **Interface Skills**: For Spec Packages, UI specs, and contract validation.
- **Matt Pocock Skills**: For engineering discipline, grilling, TDD, and diagnosis.
- **Product Manager Skills**: For discovery, hypotheses, PRDs, and GTM strategy.

## V1 Definition of Done

- `project-sensemaker` is a package-valid ChatGPT skill (includes YAML frontmatter and `agents/openai.yaml`).
- It produces a **Sensemaking Brief** (12-section standard).
- It routes using a curated registry with explicit skill entries.
- It includes validation fixtures for representative fog types.
- It adheres to the **Boundary Rule**: no downstream work by default.
- It can recommend a next skill or concrete artifact.

## Repository Structure

- `skills/`: Packaged instructions for AI agents.
  - `project-sensemaker/references/`: Registry, fog types, routing rules, and templates used by the flagship skill.
- `workflows/`: Composite skill chains (e.g., [Experimental Autonomous Sprint](workflows/experimental-autonomous-sprint.md)).
- `examples/`: Real-world "fog-to-clarity" validation fixtures (including negative fixtures).
- `docs/`: Repository-level documentation (PRDs, Issues, ADRs).

## Usage

Paste a vague project idea into an agent with `project-sensemaker` installed.

**Example:**

> /project-sensemaker
>
> I want to build an AI assistant for my school, maybe with WhatsApp, maybe a web app, maybe something with games.

## Fixture Pass Criteria

A fixture passes when the skill:
- Identifies the correct fog type.
- Names the object under pressure.
- Separates knowns, unknowns, and assumptions.
- Recommends a bounded research path.
- Identifies the weakest boundary.
- Recommends a downstream skill or artifact.
- Does not perform downstream work by default.
- Produces a ready-to-copy prompt.

## License

MIT

## Contributing

- New skills must have a `SKILL.md`.
- New routing entries must include `use_when`, `do_not_use_when`, `expected_input`, `expected_output`, and `example_prompt`.
- New examples must include an expected behavior checklist.
- Do not add downstream execution skills until `project-sensemaker` V1 is validated.
