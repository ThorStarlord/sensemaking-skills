---
name: repo-sensemaker
description: Analyze a repository to produce a Repository Sensemaking Brief. Identifies the repository goal, current structure, missing pieces, improvement opportunities, and the weakest boundary. Recommended next steps and workflows are provided.
---

# repo-sensemaker

Analyzes a repository and produces a **Repository Sensemaking Brief**. This skill is diagnostic, focusing on understanding the intent, structure, and fragility of a codebase to find the "weakest boundary."

## Description
Use when you need a deep audit of a repository's health, alignment with its stated goals, or a clear path forward when the repository feels stagnant, messy, or lacks direction.

## Core Philosophy
`repo-sensemaker` finds the weak point. It does not act; it diagnoses.

## Workflow
1. **Analyze**: Inspect README, core files, folder structure, and existing documentation.
2. **Signal Detection**: Identify what is working well (Strong Signals).
3. **Gap Analysis**: Identify what is absent or incomplete (Missing Pieces).
4. **Boundary Stress Test**: Find the "Weakest Boundary" (e.g., mismatch between README and code, unsafe workflows, missing validation).
5. **Synthesis**: Produce a Repository Sensemaking Brief with candidate next steps and recommended workflows.

## Output Format
Every response must follow the [Repository Sensemaking Brief](references/repo-analysis-template.md) structure.

## Boundary Rule
Do not execute workflows or implement changes. The output of this skill is a diagnostic artifact intended for consumption by `workflow-orchestrator` or a human.

## References
- [Repo Analysis Template](references/repo-analysis-template.md)
- [Weakness Types](references/weakness-types.md)
- [Evidence Rules](references/evidence-rules.md)
