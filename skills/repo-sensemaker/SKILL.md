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
   - **ui_fog signals**: See [UI Fog Signals Registry](references/ui-fog-signals.md) for checkable indicators:
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

When evaluating whether a repository has **UI Fog**, follow the [UI Fog Signals Registry](references/ui-fog-signals.md):

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
4. **Evidence Gathering**: Cite specific file paths and code snippets to back up signals and gaps. Each evidence excerpt's `lines` field is a single line or range — `Lx`/`Lx-Ly` or bare numbers both work (e.g. `L18` or `18`). Include a **Logic trace** (begin the paragraph with the literal words "Logic trace:") that walks from the cited evidence to the weakest-boundary conclusion.
5. **Boundary Stress Test**: Find the "Weakest Boundary" (e.g., mismatch between README and code, unsafe workflows, missing validation) and **classify it with one of the recognized [Weakness Types](references/weakness-types.md)** — `Vocabulary Drift`, `Contract Mismatch`, `Ghost Features`, `Safety Gaps`, `Implicit Dependencies`, `Zero Validation`, or `Orphaned Examples` — stated explicitly as `**Weakness type:** <type>`.
6. **Intent Comparison** (Stage 1): Compare user intent with diagnosis. Detect conflicts. Recommend escalation if needed.
7. **Problem Classification**: Classify the primary fog type based on the weakest boundary.
   Use [UI Fog Signals Registry](references/ui-fog-signals.md) to evaluate `ui_fog` signals systematically:
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

## Identifier Rules (read before filling in Section 12/13)

There are two distinct kinds of identifier in this repository. Confusing them
produces a `HALLUCINATED_WORKFLOW_ID` validation failure:

- **Workflow IDs**: the only values that may ever be written into
  `recommended_workflow_id`. The complete and current set of valid values is
  the top-level `workflows: - id: <value>` entries in
  `skills/workflow-planner/references/workflow-registry.yaml` — **read that
  file and use only an `id` you found there.** Do not guess, abbreviate, or
  reconstruct a workflow ID from memory or from a skill's name.
- **Skill IDs**: names of individual skills under `skills/<skill-id>/`
  (for example `docs-aligner`, `architectural-review`, `workflow-planner`,
  `sensemaking-docs-reconciler`). A skill ID is a real, valid identifier —
  but only when it appears describing a **workflow step** (e.g. "step 2 runs
  the `docs-aligner` skill") or a skill-level capability in prose. **A skill ID
  must never be written into `recommended_workflow_id`.** A workflow is a
  named sequence of steps, each of which may invoke a skill; the workflow's
  own `id` field (from workflow-registry.yaml) is a different string than any
  of its steps' skill names, and `docs-aligner` in particular is a skill that
  appears as a *step* inside larger workflows — it is never itself a
  top-level workflow ID.
- **Uncertain routing**: if, after reading workflow-registry.yaml, no
  workflow ID is confidently supported by the evidence, do **not** invent one
  and do **not** substitute a skill ID as a stand-in. Instead set
  `escalation_recommended: true`, leave `recommended_workflow_id` blank (with
  a note in prose explaining the uncertainty), and describe the ambiguity in
  Section 6/9. Escalating honestly is always preferred over a confident
  guess.

## Evidence Authority Hierarchy

When multiple sources make claims about the repository's current state, they
do not carry equal weight. Apply this precedence, highest first, and never let
a lower-authority source override a higher one:

1. Current executable code and current tests (the ground truth of what the
   system actually does today).
2. Current contracts and registries (e.g. `artifact-contracts.yaml`,
   `workflow-registry.yaml`, validator source).
3. Accepted ADRs (`docs/adr/`, status: Accepted).
4. Current canonical documentation (e.g. `CONTEXT.md`, current README).
5. Open issues and PROPOSED ADRs (signal intent, not settled fact).
6. Historical milestone/status/rollout documents (e.g. `PHASE-*`,
   `PRODUCTION-DEPLOYMENT-READY-*`, `GA-LAUNCH-ANNOUNCEMENT.md`, and similar
   dated self-reported status files).
7. Untracked drafts and archival material.

Required behavior:
- A lower-authority source must never override or be presented as equal to a
  higher-authority source it contradicts.
- Any claim sourced from tier 6 or 7 (historical status/milestone documents,
  drafts) MUST be explicitly labeled **historical** in the brief — never
  restated as a current fact.
- A "production ready" / "complete" / "shipped" style claim requires current
  corroboration (tier 1-4). Without it, do not assert it as true; state that
  it is an unverified historical claim.
- If sources genuinely contradict each other, surface the contradiction as an
  explicit uncertainty in the brief rather than silently picking one.
- Absence of current corroboration is not evidence of current fact either
  way — do not convert "nothing current confirms this" into "so it's true"
  or "so it's false." State the absence.
- When historical documents would be the only support for a load-bearing
  claim (e.g. a routing decision or a "done" status), prefer escalation
  (`escalation_recommended: true`) over confidently synthesizing from stale
  sources.

## References
- [Canonical Vocabulary Registry](../../docs/canonical-vocabulary.yaml) — Authoritative fog type definitions and routing field enums
- [Repo Analysis Template](references/repo-analysis-template.md)
- [Weakness Types](references/weakness-types.md)
- [Evidence Rules](references/evidence-rules.md)
- [UI Fog Signals Registry](references/ui-fog-signals.md)

## Execution Protocol

When executing as part of a workflow run:

1. Read the provided run_id, step_id, input artifacts, and expected artifact_id.
2. Call `scripts/run-ledger.py start-step`.
3. The runtime already resolved the output path and passed it as `expected_output_path` in context — use that path verbatim. Never call `scripts/create-artifact.py` (or otherwise recompute a path) during a runtime-invoked run; that path-recomputation is what caused a prior run to overwrite a tracked framework artifact (see ADR 0010, issue #40).
4. Produce the artifact at that exact path.
5. Call `scripts/validate-and-record.py`.
6. Only report completion if validation passes.
7. Never mark the next step complete yourself.

