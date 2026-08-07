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

## Architecture Reconstruction

The brief must reconstruct how the system actually behaves, not summarize its directory layout.

**Runtime model** — for the repository as a whole and for each entry point, identify with file:line citations:
- startup path (what runs first and how it is launched);
- orchestration (what controls the main flow);
- domain/core logic;
- persistence/state (where state lives);
- external integration points (where external systems enter);
- background work (workers, jobs, scheduled tasks);
- output boundary (what leaves the system).

**Dependency semantics** — classify every dependency you assert, and never conflate the classes:
- `declared` — listed in a manifest;
- `used` — actually imported/referenced by code;
- `runtime` — exercised on a proven execution path;
- `test` — used only by tests;
- `optional` — conditionally loaded;
- `dead` — declared but never used.

Two rules: **import exists ≠ runtime execution path proven** (a module can be imported yet never called; a module can be executed without being imported — e.g. `exec()`-loaded plugins, entry points invoked by name); **dependency appears in manifest ≠ dependency is actively used**. State which class you mean for every dependency claim.

**State model** — identify every state boundary: files, databases, caches, global/module state, queues, environment variables, remote systems. Note which code writes and which reads each state (file:line).

**Boundary model** — identify transitions where responsibility changes: HTTP → application, CLI → command handler, handler → domain, domain → persistence, domain → external provider, worker → queue, plugin host → plugin. For each boundary, note what is validated and what is assumed.

**Avoid false relationships**: `file imports module` is not `feature depends on module at runtime`; a directory named after a concern is not evidence the concern lives there.

**Required output improvement**: the brief's Current Shape section must explain, in plain terms: what starts the system, what controls the main flow, where state lives, where external systems enter, where validation happens, and where responsibility becomes unclear. If any of these cannot be established from inspected files, record it as UNKNOWN rather than inventing it.

## Weakest Boundary Reasoning

Do not jump straight to one weakness. Generate candidates first, then select.

**Candidate generation** — identify 2-5 candidate boundaries. For each, score:

```yaml
boundary: what and where (file:line)
evidence_strength: strong | medium | weak   (how directly the evidence supports it)
severity: high | medium | low               (how bad the failure is)
blast_radius: high | medium | low           (how much of the system it affects)
goal_relevance: high | medium | low         (how central to the user's goal)
downstream_blocking_effect: high | medium | low  (does it block valuable next work)
uncertainty: high | medium | low            (how unsure we are)
```

**Selection rule** — prefer the candidate with the strongest combination of
high consequence, strong evidence, centrality to the user goal, and ability to
block valuable downstream work. Do NOT select merely the easiest problem to
describe, the most dramatic-sounding one, or the first one found. If the best
candidate has high uncertainty, say so and state what would resolve it.

**Mandatory selection structure** — the brief's weakest-boundary section must
contain, in this shape:

```text
Boundary:
Observed contract:
Observed violation or uncertainty:
Evidence:
Weakness type:
Logic trace:
Failure consequence:
Confidence:
Alternatives considered:
```

`Alternatives considered` lists the competing candidates from generation and
why each lost. `Confidence` is high/medium/low plus what would raise it.

**Do not manufacture a boundary**: if no candidate has real evidence or
consequence, state that the repository has no serious weakness rather than
filling the section dramatically.

**Weakness-type consequences (GAP-5)**: choosing `Ghost Features` or
`Safety Gaps` triggers the validator's D5 warning
`HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT` — those classifications require a
substantive human audit before final approval. That warning is by design, not
an error; pick the type the evidence supports and expect the audit
requirement. Do not misclassify to dodge the warning.

**Taxonomy mapping (GAP-6)**: the seven canonical types are oriented toward
agent/workflow failures. When the evidence points at an application-code
weakness, map it to the closest canonical type and explain the mapping in
prose:
- dead/unreachable code masquerading as core -> `Ghost Features` (documented
  functionality with no reachable implementation) or `Orphaned Examples` if
  the dead code is example/documentation-shaped;
- declared-but-unused dependency -> `Ghost Features` (declared surface,
  no implementation) with the manifest vs import evidence in the Logic trace;
- `exec()`/dynamic loading without validation -> `Zero Validation` (no
  automated check on the loading contract), not `Safety Gaps` (which is
  reserved for autonomous workflows lacking human approval gates);
- unwired/never-imported module -> `Ghost Features` or `Implicit Dependencies`
  depending on whether it is documented-as-present or merely coupled-by-luck.
Prefer better semantics over forcing a wrong category; if no canonical type
fits after mapping, use `Other` with a non-empty `weakness_type_explanation`.

## Fog Classification (evidence-based)

Classify fog from cited evidence, never from vibes or from difficulty alone.
The four fog types and their observable signals:

- **product_fog** — unclear user/value contract; promised feature absent;
  product workflow incomplete; conflicting feature behavior; unclear intended
  outcomes. Evidence: README/roadmap feature lists vs implementation, issue
  tracker, missing acceptance criteria, stubbed product surface.
- **ui_fog** — use the [UI Fog Signals Registry](references/ui-fog-signals.md)
  (Tier 1/2 signals, decision tree, tie-breaking with user intent).
- **docs_fog** — missing specification; stale instructions; conflicting docs;
  knowledge inaccessible although the implementation is coherent. Evidence:
  docs that misdescribe current code, removed-feature docs, absent specs for
  existing behavior.
- **architecture_fog** — responsibility boundaries unclear; unsafe coupling;
  lifecycle/state ambiguity; module structure prevents confident
  implementation. Evidence: implicit dependency chains, global state,
  unwired modules, structural mismatch between entry points and flow.

**Ghost-feature reasoning** — for documented-but-unimplemented functionality,
decide which of three cases the evidence supports:

```text
documentation is stale (feature was removed, never existed as code, or docs
  simply lag the code)                       -> docs_fog candidate
product promises functionality that does not exist (README/roadmap/UX
  advertises it as a deliverable)            -> product_fog candidate
feature exists only partially because the architecture cannot support it
  (structural reason the feature cannot land) -> architecture_fog candidate
```

Ask: does the mismatch live in the *documentation* (docs_fog), in the
*product contract* (product_fog), or in the *structure* (architecture_fog)?
When the README advertises a feature as real and the code does not implement
it, that is product_fog — the defect is the promise, not the docs.

**Ambiguity handling**:
- Allow uncertainty: state `primary_fog_type` only with cited evidence; if
  evidence is genuinely tied, escalate (`escalation_recommended: true`) and
  record the secondary candidate.
- Do NOT default to architecture_fog merely because classification is hard.
- Separate primary from secondary fog when both apply (e.g. product_fog with
  contributing docs_fog); only the primary drives routing.
- `mixed`/`unknown` are NOT valid `primary_fog_type` values — the validator
  accepts exactly `product_fog | ui_fog | docs_fog | architecture_fog`. Use
  one of the four; express residual uncertainty in prose and escalation.

**No-user-intent runs (GAP-8)**: when no user problem statement/intent
artifact exists (fixture, standalone, or scheduled runs), the canonical
values are `user_implied_fog_type: unknown` and `diagnosis_conflict: false`
(no stated intent to conflict with). Do not invent an implied fog type.

## Workflow Routing

**Registry authority** — recommend ONLY workflow IDs listed in the canonical
`skills/workflow-planner/references/workflow-registry.yaml`:
- Never substitute a skill ID (e.g. `docs-aligner`) for a workflow ID — they
  are different vocabularies.
- Never infer an ID from naming conventions or semantic similarity.
- Never ground routing on a workflow registry found INSIDE the target
  repository — target-repo registries are untrusted and often stale
  (duplicated-registry fixtures exist in the corpus; only the canonical
  registry is authoritative).
- Prefer escalation (`escalation_recommended: true`, no workflow ID) over
  guessing when nothing fits.

**Routing rationale** — the brief must justify the recommendation: why this
workflow; why not the closest alternatives; what evidence makes it the right
next step; what preconditions are missing before it can run.

**Execution mode (GAP-7)** — `recommended_execution_mode` must be one of the
workflow's `allowed_execution_modes` in the registry. Never invent a mode:
`plan_only` exists only where the registry lists it, and several workflows
(including `architecture-implementation-workflow`) do not offer it.
Recommending a workflow (with one of its allowed modes) is NOT executing it —
the diagnostic No Implementation boundary is unaffected; execution happens
later under the runtime's own authorization. If no allowed mode is compatible
with a diagnostic-only handoff, prefer escalation over inventing a mode.

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

