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
5. **Boundary Stress Test**: Find the "Weakest Boundary" (e.g., mismatch between README and code, unsafe workflows, missing validation) and **classify it with one of the recognized [Weakness Types](references/weakness-types.md)** — `Vocabulary Drift`, `Contract Mismatch`, `Ghost Features`, `Safety Gaps`, `Implicit Dependencies`, `Zero Validation`, or `Orphaned Examples` — stated explicitly as `**Weakness type:** <type>` in Section 6's prose, AND recorded in the structured `weakness_type` field in Section 13's machine-readable YAML (the two must agree). If none of the 7 types fit, use `Other` and give a non-empty `weakness_type_explanation` in Section 13 — an unrecognized value or a missing explanation for `Other` is a non-blocking validator warning, not a rejection, but it must be resolved before a human grants final approval.
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

## Repository Exploration Protocol (deterministic)

Investigate in passes. Do not rely on repository size, first impressions, or random sampling: the protocol below is the ordering, and every claim must trace to a file actually opened.

**Pass A — Repository orientation**: root inventory; README; manifests (package manager, project files); language markers; build configuration; CI configuration; container/deployment configuration; top-level documentation; repository-level configuration. Record what exists and what is absent.

**Pass B — Execution discovery**: executable declarations; package scripts; `main`/entry-point modules; CLI commands; server bootstrap; route registration; framework entry points; workers/jobs; plugin registration; helper scripts. Every entry point found must be named with its file and line.

**Pass C — System structure**: map each entry point through the flow: entry point → orchestration → domain/core logic → state/persistence → external integrations → outputs. Identify where each transition happens (file:line). If a hop cannot be traced, record it as UNKNOWN — do not invent the missing hop.

**Pass D — Validation structure**: tests; schemas; assertions; input validation; authorization; error boundaries; type boundaries. Record what is validated and where, and what is not.

**Pass E — Contradiction search**: actively look for README vs implementation disagreement; docs vs current code disagreement; manifest vs actual imports; declared feature vs missing implementation; test claims vs uncovered behavior; generated code mistaken for authored source. Surface every conflict found — do not silently pick a side.

**Low-value content**: deprioritize generated bundles, dependency/vendor trees, caches, compiled artifacts, lockfiles (unless relevant to the question), large test snapshots, and duplicated generated sources. Never let repository size force random sampling; the passes above define the sample.

## Evidence Authority

Every substantive claim carries an internal evidence class:

- **OBSERVED** — directly visible in a file you actually inspected (cite file + lines).
- **DERIVED** — follows logically from multiple observed facts (the `Logic trace:` makes the derivation explicit).
- **INFERRED** — plausible but not directly established (must be labeled as inference, never stated as fact).
- **UNKNOWN** — evidence is insufficient (state it as unknown; do not convert into a confident conclusion).

Rules:
1. Never state an INFERRED claim as an observed fact.
2. Never convert UNKNOWN into a conclusion; record what would resolve it.
3. Conflicting evidence must be surfaced, not arbitrarily resolved.
4. Source code/config outranks descriptive documentation for current runtime behavior.
5. Configuration outranks prose for configured behavior.
6. Tests prove intended/covered behavior, not necessarily production execution.
7. Historical docs must be identified as historical.
8. A file not opened must never be cited.

Supported citation formats: any of `md, py, yaml, yml, toml, txt, js, jsx, ts, tsx, json, html, css, go, rs, java, rb, sh` as `path/to/file.ext:line` (or `:line-line`). Do not cite other extensions as evidence, and never invent a path.

## Output Format
Every response must follow the [Repository Sensemaking Brief](references/repo-analysis-template.md) structure.

## Boundary Rules
1. **No Implementation**: Do not execute workflows or implement changes. The output of this skill is a diagnostic artifact.
2. **Registry Grounding**: Every `recommended_workflow_id` MUST be verified against `skills/workflow-planner/references/workflow-registry.yaml`. Do not invent or "hallucinate" workflow IDs from semantic context. If no matching workflow exists, recommend a `plan_only` mode with the closest structural match or leave it blank with a note.

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

## Runtime-owned artifact skeleton (issue #55)

When this skill is invoked through the runtime (`ClaudeAgentSdkSkillExecutor`),
`expected_output_path` already contains a **runtime-generated skeleton** by
the time you read it — see `scripts/brief_skeleton.py`. This exists because
prompt guidance alone was proven insufficient to guarantee the artifact's
deterministic grammar (PR #54: the model omitted the YAML fence entirely).

**Do not recreate the envelope.** These are already filled in by the runtime
and must not be re-authored or reordered:
- `artifact_id`, `schema_version`, `source_intent_ref`, `created_at`, `immutable`
- The heading structure and the single `## 13. Machine-readable handoff` YAML fence
- `<!-- MODEL_SECTION:<name>:BEGIN/END -->` marker comments — do not delete them

**Your job is only to fill in:**
- The prose between each `MODEL_SECTION` marker pair (repository goal, current
  shape, strong signals, missing pieces, improvement opportunities, weakest
  boundary prose, evidence prose, why-it-matters, candidate next steps,
  recommended next step, ready-to-copy prompt).
- The `evidence_excerpts` YAML block under Section 8.
- The placeholder YAML fields in Section 13: `user_implied_fog_type`,
  `primary_fog_type`, `diagnosis_conflict`, `escalation_recommended`,
  `evidence`, `recommended_workflow_id`, `recommended_execution_mode`,
  `weakest_boundary`.

**Workflow IDs vs. skill IDs**: `recommended_workflow_id` must be an id from
`workflow-registry.yaml` (e.g. `architecture-implementation-workflow`), never
a skill id (e.g. `docs-aligner`). If uncertain which workflow applies, prefer
escalation (`escalation_recommended: true`) over guessing — the runtime will
preserve your value verbatim, valid or not, and the validator (not the
runtime) is what rejects an invalid one.

**Evidence-authority hierarchy and grammar** (unchanged from prior guidance,
still your responsibility): cite specific files and line ranges you actually
read (`Lx`/`Lx-Ly` or bare numbers both work, e.g. `L18` or `18`); never cite
a file you have not opened; prefer direct code/config over comments over
external docs when they conflict; include a **Logic trace** paragraph
(beginning literally with "Logic trace:") connecting evidence to your
weakest-boundary conclusion.

## Invocation modes (quote handling)

There are two distinct invocation modes. Know which one you are in before
deciding how to write evidence quotes.

**Runtime invocation** (through `ClaudeAgentSdkSkillExecutor` or the
orchestration runtime): the runtime skeleton exists, and the runtime
overwrites placeholder `quote` values with the exact verbatim text it reads
from the cited file/lines before validation runs (issue #89). In this mode
you MAY write a short placeholder (`"see file/lines"`) — but only because the
runtime guarantees the overwrite happens before validation. Never assume this
guarantee outside the runtime.

**Standalone invocation** (skill executed directly, no runtime — e.g. a
baseline, fixture, or manual run): there is no skeleton and no overwrite. You
author the complete artifact yourself (including the envelope fields), and
`quote` values MUST be verbatim text from the cited file/lines, or validation
fails with blocking `EVIDENCE_QUOTE_NOT_FOUND`. Validate standalone output
with `python scripts/validate-brief.py <artifact> --target-repo <repo> --repo-root <root>`.

When in doubt, write verbatim quotes: verbatim quotes are valid in both
modes, placeholders are valid only in the runtime mode.

The runtime writes a **tool-call trace** (`tool-call-trace.jsonl` in the
session artifact directory) recording every tool call you make during this
invocation — this is for debugging failed runs, not something you need to
produce yourself.

