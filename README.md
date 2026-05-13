# Sensemaking Skills

A collection of skills designed to turn vague project uncertainty into clear problem frames, research paths, decisions, and next-step prompts.

The flagship skill is `project-sensemaker`, which routes unclear work to the right downstream method, skill, or artifact.

## Core Philosophy

"I do not know what I need because I do not yet understand what I am building."

Sensemaking skills sit **before** specialized tools. They handle the moment of "fog" where the type of problem is not yet known.

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
- `workflows/`: Composite skill chains (e.g., [Experimental Autonomous Sprint](workflows/experimental-autonomous-sprint.md)).
- `references/`: Knowledge maps, registries, and templates.
- `examples/`: Real-world "fog-to-clarity" validation fixtures.
