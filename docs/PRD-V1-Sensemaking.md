# PRD: Sensemaking Skills V1 (Refactored Release)

## Status: Refactored
## Date: 2026-05-13

## 1. Executive Summary
Sensemaking Skills V1 establishes a robust "meta-routing" layer for AI agents. It standardizes the transition from repository uncertainty to actionable implementation by splitting the job into two specialized skills: `repo-sensemaker` (Diagnosis) and `workflow-orchestrator` (Orchestration).

## 2. Problem Statement
Agents often jump into implementation ("building") before they understand the repository-level "fog" (uncertainty). This leads to misaligned PRDs, incorrect architectural choices, and technical debt.

## 3. Goals
- Provide package-valid `repo-sensemaker` and `workflow-orchestrator` skills.
- Enforce structural integrity via canonical output templates (11-section Brief / 10-section Plan).
- Enable precise, gated orchestration of skill sequences.
- Maintain safety-first human-in-the-loop control for all execution workflows.

## 4. Key Features
- **Repo Sensemaker Skill**: Diagnostic focus on finding the "Weakest Boundary".
- **Workflow Orchestrator Skill**: Procedural focus on selecting and running gated workflows.
- **Structured Registries**: Valid YAML for both skills and workflows.
- **Validation Fixtures**: Diagnostic and Orchestration examples with behavior checklists.
- **Safety Gates**: Explicit "Guided" and "Plan Only" execution modes.
- **Governance**: MIT License, CONTRIBUTING.md, and `validate-repo.py` script.

## 5. Functional Requirements
- `repo-sensemaker` must produce an 11-section diagnostic brief by default.
- `workflow-orchestrator` must produce a 10-section orchestration plan.
- Must refuse to act if a diagnostic brief is missing or unknowns are too fundamental.
- Must include negative fixtures demonstrating safe refusal-to-route.

## 6. Non-Functional Requirements
- **Decoupling**: Diagnosis must be separate from Action.
- **Safety**: No irreversible actions (commits, deletions) without explicit "Autonomous" opt-in.
- **Clarity**: Must identify "Weakest Boundary" before orchestration.

## 7. Success Metrics
- 100% compliance with canonical templates.
- 0 instances of unapproved execution in guided mode.
- Successful orchestration of at least 3 distinct workflow types.

## 8. Open Questions
- Should we add a automated contract validator between the Brief and the Plan?
- How do we handle dynamic skill discovery in the registry?
