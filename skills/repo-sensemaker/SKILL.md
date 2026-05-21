---
name: repo-sensemaker
description: analyze a repository to produce a repository sensemaking brief. use when the user asks what a repo is for, what is missing, what can be improved, what the weakest boundary is, or what the next steps should be.
---

# repo-sensemaker

Analyzes a repository and produces a **Repository Sensemaking Brief**. This skill is diagnostic, focusing on understanding the user intent, codebase structure, and fragility to find the "weakest boundary."

## Stage 1: Intent-Aware Analysis (New)

When analyzing a repository, **always compare** what the user intends with what the codebase signals:

1. **Extract User Intent**: From the user's problem statement or prior context, identify what fog type they *implied*:
   - Implied product_fog? ("We need better user onboarding")
   - Implied ui_fog? ("Dashboard UX redesign")
   - Implied docs_fog? ("API docs are confusing")
   - Implied architecture_fog? ("System is slow")

2. **Diagnose Codebase**: Analyze the code structure to determine what fog type the *actual problems* require:
   - **product_fog signals**: Feature flags, user data, analytics tracking, roadmap docs, unclear user needs
   - **ui_fog signals**: See [UI Fog Signals Registry](references/ui-fog-signals.yaml) for checkable indicators:
     - Missing user flow documentation or interaction specs
     - Frontend components scattered without clear boundaries
     - Routing logic complex and undocumented
     - Design system fragmented or absent
     - Low test coverage for UI interactions
   - **docs_fog signals**: README, ADR files, architecture docs, runbooks missing or outdated
   - **architecture_fog signals**: Module boundaries unclear, circular dependencies, performance issues, coupling, state management scattered

3. **Detect Conflicts**: If user intent (implied fog) ≠ codebase diagnosis (actual fog), flag it:
   - Example: User wants "UI redesign" but code shows "state management is broken" → conflict
   - This is when escalation to full-fog is recommended

4. **Emit Stage 1 Fields** (required for downstream routing):
   - `source_intent_ref`: Reference to 00-user-intent.md
   - `user_implied_fog_type`: What the user's problem statement suggests
   - `primary_fog_type`: What the codebase actually signals
   - `diagnosis_conflict`: Boolean (user_implied != primary?)
   - `escalation_recommended`: Boolean (true if high uncertainty or conflict)

## UI Fog Classification Guide (NEW)

When evaluating whether a repository has **UI Fog**, follow the [UI Fog Signals Registry](references/ui-fog-signals.yaml):

1. **Check for frontend code**: Does the codebase contain React/Vue/Angular/HTML/CSS?
   - If no → Not ui_fog; evaluate other fog types
   - If yes → Continue to step 2

2. **Evaluate Tier 1 signals** (high-confidence UI fog indicators):
   - Missing UI flow documentation?
   - Frontend components scattered without clear boundaries?
   - Routing logic complex and undocumented?
   - Design system fragmented or absent?
   - Count how many Tier 1 signals are present (0-4)

3. **Evaluate Tier 2 signals** (moderate confidence):
   - Low test coverage for UI interactions?
   - Accessibility not addressed?
   - Responsive design undocumented?
   - Screen count vs. documentation mismatch?

4. **Make the call**:
   - 2+ Tier 1 signals → STRONG CONFIDENCE: Classify as `ui_fog`
   - 1 Tier 1 + 2+ Tier 2 signals → MEDIUM CONFIDENCE: Classify as `ui_fog`
   - Only Tier 3 signals or missing frontend → NOT ui_fog; evaluate architecture_fog or product_fog

5. **Break ties with user intent**: If diagnosis is uncertain and user's problem statement mentions screens, flows, navigation, or design → use intent as tiebreaker to classify as `ui_fog`.

**Important**: Avoid vibe-based diagnosis. Every ui_fog classification must cite specific signals from the UI Fog Signals Registry.

---

## Standard Workflow
1. **Analyze**: Inspect README, core files, folder structure, and existing documentation.
2. **Signal Detection**: Identify what is working well (Strong Signals).
3. **Gap Analysis**: Identify what is absent or incomplete (Missing Pieces).
4. **Evidence Gathering**: Cite specific file paths and code snippets to back up signals and gaps.
5. **Boundary Stress Test**: Find the "Weakest Boundary" (e.g., mismatch between README and code, unsafe workflows, missing validation).
6. **Intent Comparison** (Stage 1): Compare user intent with diagnosis. Detect conflicts. Recommend escalation if needed.
7. **Problem Classification**: Classify the primary fog type based on the weakest boundary.
   Use [UI Fog Signals Registry](references/ui-fog-signals.yaml) to evaluate `ui_fog` signals systematically:
   - **product_fog**: Unclear user needs, missing feature specs, undocumented workflows → needs discovery/research
   - **ui_fog**: Screen/flow design problems (use UI Fog Signals Registry for checkable indicators):
     - Missing or unclear user flows/screen specs
     - Components scattered without reusability boundaries
     - Routing logic complex and undocumented
     - Design system inconsistent or absent
     - → needs UI diagnostic workflow: ui-brief → ui-flow → ui-screen-spec
   - **docs_fog**: Missing documentation, unclear specifications, knowledge silos → needs documentation architecture
   - **architecture_fog**: Code structure problems, unclear boundaries, module coupling, state management scattered → needs spec-driven refactoring (default)
8. **Synthesis**: Produce a Repository Sensemaking Brief with fog type classification, intent alignment, candidate next steps, and recommended workflows.

## Output Format
Every response must follow the [Repository Sensemaking Brief](references/repo-analysis-template.md) structure.

## Boundary Rules
1. **No Implementation**: Do not execute workflows or implement changes. The output of this skill is a diagnostic artifact.
2. **Registry Grounding**: Every `recommended_workflow_id` MUST be verified against `skills/workflow-planner/references/workflow-registry.yaml`. Do not invent or "hallucinate" workflow IDs from semantic context. If no matching workflow exists, recommend a `plan_only` mode with the closest structural match or leave it blank with a note.

## References
- [Repo Analysis Template](references/repo-analysis-template.md)
- [Weakness Types](references/weakness-types.md)
- [Evidence Rules](references/evidence-rules.md)
