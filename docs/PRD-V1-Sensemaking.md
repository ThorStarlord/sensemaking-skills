# PRD: Sensemaking Skills V1 (Flagship Release)

## Status: Draft
## Date: 2026-05-13

## 1. Executive Summary
Sensemaking Skills V1 establishes a robust "meta-routing" layer for AI agents. It standardizes the transition from project uncertainty to actionable implementation by producing a "Sensemaking Brief" and routing to specialized ecosystems (Interface, Matt, PM).

## 2. Problem Statement
Agents often jump into implementation ("building") before they understand the "fog" (uncertainty). This leads to misaligned PRDs, incorrect architectural choices, and technical debt.

## 3. Goals
- Provide a package-valid `project-sensemaker` skill.
- Enforce structural integrity via a 12-section output template.
- Enable precise routing via a structured skill registry.
- Maintain human-in-the-loop control for high-velocity workflows.

## 4. Key Features
- **Project Sensemaker Skill**: YAML frontmatter, Boundary Rules, Core Philosophy, and portable Skill UI metadata.
- **Sensemaking Brief**: Canonical 12-section structure (Fog Type, Object Under Pressure, etc.).
- **Structured Skill Registry**: Valid YAML routing table with tie-breakers and confidence rules.
- **Validation Fixtures**: 3 positive examples and 1 negative fixture, all aligned with the 12-section template and behavior checklists.
- **Experimental Workflows**: Hardened "Autonomous Sprint" with "review and stop" gates.
- **Governance**: MIT License, CONTRIBUTING.md, and `validate-repo.py` script.

## 5. Functional Requirements
- Must produce a 12-section Markdown report by default.
- Must recommend at least one downstream skill or concrete artifact.
- Must use valid YAML for the skill registry to enable future automation.
- Must refuse to route downstream if unknowns are too fundamental (Confidence Rule).
- Must include a negative fixture demonstrating "refusal to route."

## 6. Non-Functional Requirements
- **Portability**: Must be installable as a ChatGPT skill.
- **Safety**: Must not commit to `main` or approve designs without user permission.
- **Clarity**: Must identify "Fog Type" before any implementation.

## 7. Success Metrics
- 100% compliance with the 12-section template in dogfooding tests.
- 0 instances of "downstream building" by `project-sensemaker` unless requested.
- Successful routing to at least 3 different ecosystems.

## 8. Open Questions
- Should we add a `ui-spec-linter` equivalent for Sensemaking Briefs?
- How do we handle external skill updates in the registry?
