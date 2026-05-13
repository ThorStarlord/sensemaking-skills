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
- **Project Sensemaker Skill**: YAML frontmatter, Boundary Rules, Core Philosophy.
- **Sensemaking Brief**: 12 sections covering Fog Type, Object Under Pressure, Weakest Boundary, etc.
- **Skill Registry**: Explicit routing table for Engineering, UI, and PM skills.
- **Experimental Workflows**: Quarantined "Autonomous Sprint" with safety gates.

## 5. Functional Requirements
- Must produce a 12-section Markdown report by default.
- Must recommend at least one downstream skill or concrete artifact.
- Must use relative links for all internal references.
- Must include validation fixtures (examples) with expected behavior checklists.

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
