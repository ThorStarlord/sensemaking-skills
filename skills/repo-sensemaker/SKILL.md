---
name: repo-sensemaker
description: analyze a repository to produce a repository sensemaking brief. use when the user asks what a repo is for, what is missing, what can be improved, what the weakest boundary is, or what the next steps should be. When invoked conversationally (not via automated workflow execution), also applies an investigate-first interaction procedure to decide whether one neutral clarifying question is needed before recommending.
---

# repo-sensemaker

Analyzes a repository and produces a **Repository Sensemaking Brief**. This skill is diagnostic, focusing on understanding the user intent, codebase structure, and fragility to find the "weakest boundary."

## Two responsibilities, one skill

This skill has two responsibilities. They stay conceptually separate (see [docs/candidate/architecture-decision.md](../../docs/candidate/architecture-decision.md), Decision 1) but live in one file, not two, because one of them is structurally incapable of running outside conversation:

- **Diagnose** (below, through "Runtime-owned artifact skeleton") — produces the brief. Runs identically whether invoked by a human or by `workflow-runtime.py`'s automated per-step execution. This is the whole of what this skill did before this section existed.
- **Interact** (final section of this file) — reads the brief and decides whether to ask one clarifying question before recommending. **Only runs in direct conversational invocation.** The automated runtime path has no chat channel mid-run — its deliverable is the artifact, full stop — so this responsibility cannot execute there even in principle. Giving it a separate, independently-routable Skill file would misrepresent when it can run at all; keeping it as a clearly-labeled section of the same file keeps that constraint visible where an implementer will actually see it.

If you are invoked through `workflow-runtime.py` (see "Execution Protocol" below), stop after producing and recording the artifact — the Interact section does not apply to you this run.

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
4. **Evidence Gathering**: Cite specific file paths and code snippets to back up signals and gaps. Each evidence excerpt's `lines` field is a single line or range — `Lx`/`Lx-Ly` or bare numbers both work (e.g. `L18` or `18`). Include a **Logic trace** (begin the paragraph with the literal words "Logic trace:") that walks from the cited evidence to the weakest-boundary conclusion. **State-currency verification:** documented state is not automatically verified current state — before treating any tracker, roadmap, TODO, review, milestone, or branch-status claim as current, verify it with the cheapest repository probe (current branches, commits, working-tree state, tests, runtime artifacts, recent reviews), or clearly identify the claim as documented but not independently verified. Never convert "documented X" into "X is currently true" without verification, and do not treat unfinished documentation as proof that work remains unfinished.
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
8. **Synthesis**: Produce a Repository Sensemaking Brief with fog type classification, intent alignment, candidate next steps, and recommended workflows. Keep observed evidence, documented claims, inference, and owner-supplied judgment/context distinguishable in the synthesis. Decision-changing current-state claims must explicitly distinguish verified current state from merely documented state: cite the probe used when verified, and clearly identify unverified documented claims as documented but not independently verified. If you have grounds for it, optionally fill in Section 15 (Extended analysis) — see [Repo Analysis Template](references/repo-analysis-template.md#15-extended-analysis). It is optional and non-blocking (ADR 0024); leave it out entirely if you have nothing to add.

## Probe Engine (verified current state, mandatory before synthesis)

Deterministic probes replace *derived* evidence (text inspection) with *measured*
current-state evidence. Before writing Sections 3–9, run the probe engine against
the target repository:

```powershell
python scripts/probe-repo.py --repo-root <target-repo> [--output <path>/probe-report.yaml]
```

Then:

1. **Read `probe-report.yaml`.** Its values are verified current state, measured
   on the checked-out tree — prefer them over any documented claim (state-currency
   verification, per Standard Workflow item 4).
2. **Surface the numbers in your prose.** The report's `verification_gap.vg`,
   `context_entropy.ce`, `fixtures_coverage.coverage`, and `churn` fields feed
   directly into the missing-pieces, weakest-boundary, and evidence sections.
   A `vg > 0` with declared-but-unenforced checks is a `Contract Mismatch` signal;
   `vg == 1.0` means every declared check is unenforced (or CI is absent).
   `ce >= 5` triggers a hygiene warning about untracked/ignored artifact sprawl.
   A non-empty `missing_fixtures` list signals validator orphans (Zero Validation
   or Orphaned Examples candidates).
3. **Cite the probe in Section 8.** Every excerpt that rests on a measured value
   must reference the probe that produced it (e.g.
   `probe-report.yaml:verification_gap.vg`), plus the usual `file:lines`.
4. **Probe failure fallback.** If the probe exits nonzero or the target is not a
   git repository (`is_git_repo: false`), the probe still reports directory-level
   facts; any claim you cannot measure must be labeled
   "documented but not independently verified" (per Standard Workflow item 4 and
   Section 8). Never skip the probe because a repo "looks simple" — a
   non-git repo is itself a finding.
5. **Relationship findings are evidence candidates, not diagnoses.** The report's
   `relationships` section (version drift + ADR integrity, plus the discovered
   doc surface) lists mechanically-established disagreements with file:line
   provenance. Treat each finding as a candidate requiring semantic review:
   the probe cannot decide which source has authority, which claim is
   historical, or whether a disagreement matters — you can. A repository with
   zero relationship findings is a valid correct-negative result. Where a
   relationship finding sharpens a boundary (e.g. a version conflict, a stale
   ADR-status claim, a doc that references a missing ADR), cite it in Section 8
   like any measured value (`probe-report.yaml:relationships.version.findings`).

## Output Format
Every response must follow the [Repository Sensemaking Brief](references/repo-analysis-template.md) structure.

## Boundary Rules
1. **No Implementation**: Do not execute workflows or implement changes. The output of this skill is a diagnostic artifact.
2. **Registry Grounding**: Every `recommended_workflow_id` MUST be verified against `skills/workflow-planner/references/workflow-registry.yaml`. Do not invent or "hallucinate" workflow IDs from semantic context. If no matching workflow exists, recommend a `plan_only` mode with the closest structural match or leave it blank with a note.
3. **Clarification policy**: Ask no questions when repository evidence is sufficient. When unresolved owner intent would materially change the recommendation, ask a neutral, high-information clarification that gathers intent rather than advocating one option. Resolve empirical uncertainty through probes rather than asking the owner to guess. This policy applies regardless of execution mode, but *how* it's carried out differs: in conversational invocation, apply it directly — see "Interact" below, which is this policy's full worked-out procedure (uncertainty classification, the neutral-clarification discipline, the one-question default). In automated runtime execution there is no owner to ask (see Execution Protocol step 8) — the equivalent signal is `escalation_recommended: true`, optionally sharpened by Section 15's `uncertainty`/`owner_intent_state` fields, which is what a later conversational consumer (a human, or this skill re-invoked conversationally) uses to actually ask.

## References
- [Canonical Vocabulary Registry](../../docs/canonical-vocabulary.yaml) — Authoritative fog type definitions and routing field enums
- [Repo Analysis Template](references/repo-analysis-template.md)
- [Weakness Types](references/weakness-types.md)
- [Evidence Rules](references/evidence-rules.md)
- [UI Fog Signals Registry](references/ui-fog-signals.md)
- [Architecture decision record](../../docs/candidate/architecture-decision.md) — why Diagnose/Interact are one skill, not two

## Execution Protocol

When executing as part of a workflow run:

1. Read the provided run_id, step_id, input artifacts, and expected artifact_id.
2. Call `scripts/run-ledger.py start-step`.
3. The runtime already resolved the output path and passed it as `expected_output_path` in context — use that path verbatim. Never call `scripts/create-artifact.py` (or otherwise recompute a path) during a runtime-invoked run; that path-recomputation is what caused a prior run to overwrite a tracked framework artifact (see ADR 0010, issue #40).
4. Produce the artifact at that exact path.
5. Call `scripts/validate-and-record.py`.
6. Only report completion if validation passes.
7. Never mark the next step complete yourself.
8. Stop here. Do not proceed to the Interact section below — there is no owner to ask in this execution path.

## Runtime-owned artifact skeleton (issue #55)

When this skill is invoked through the runtime's model executor,
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
- Optionally, Section 15's `extended_analysis:` block (see `references/repo-analysis-template.md`'s Section 15; ratified per ADR 0024). Leave it out
  entirely if you have nothing grounded to add; it is never required.

**Workflow IDs vs. skill IDs**: `recommended_workflow_id` must be an id from
`workflow-registry.yaml` (e.g. `architecture-implementation-workflow`), never
a skill id (e.g. `docs-aligner`). If uncertain which workflow applies, prefer
escalation (`escalation_recommended: true`) over guessing — the runtime will
preserve your value verbatim, valid or not, and the validator (not the
runtime) is what rejects an invalid one.

**Evidence-authority hierarchy and grammar** (unchanged from prior guidance,
still your responsibility): cite specific files and line ranges you actually
read (`Lx`/`Lx-Ly` or bare numbers both work, e.g. `L18` or `18`); never cite
a file you have not opened; probe-report.yaml (measured current state) sits
above direct code/config; prefer probes over code/config over comments over
external docs when they conflict; include a **Logic trace** paragraph
(beginning literally with "Logic trace:") connecting evidence to your
weakest-boundary conclusion.

The runtime writes a **tool-call trace** (`tool-call-trace.jsonl` in the
session artifact directory) recording every tool call you make during this
invocation — this is for debugging failed runs, not something you need to
produce yourself.

---

## Interact: conversational-invocation-only interaction procedure

**Applies only when you are talking directly with a user (or another agent) in conversation, not when invoked as an automated workflow step (see "Execution Protocol" above, step 8).** If you're not sure which mode you're in: if you were given a `run_id`/`step_id`/`expected_output_path`, you're in the automated path — stop after producing the artifact. Otherwise, continue below.

This section is the conversational-mode procedure for **Boundary Rule 3's clarification policy** — the policy itself is stated once, above, and applies in both execution modes; what follows is how to actually carry it out when a chat channel exists. Don't let this section's wording drift from Boundary Rule 3's — if you're revising one, revise both.

This skill's job, in this mode: given real (or agent-selected) owner uncertainty, produce a useful recommendation with the least owner burden possible, while never inventing an owner preference it doesn't have. This procedure is evidenced by a real-use validation experiment (see `docs/prototypes/real-use-experiment-2026-08-09/` on `prototype/repo-sensemaker-vnext`, PR #164) that ran it twice under genuine context isolation and found it independently avoided a real design failure mode (bundling an evidence-resolved fact with an evidence-supported-but-unauthorized recommendation) both times — see [docs/candidate/architecture-decision.md](../../docs/candidate/architecture-decision.md) for why the underlying *behavior* is treated as evidenced even though the packaging it originally shipped in (a separate Skill) was not. Independently, canonical `main`'s Boundary Rule 3 (PR #165, merged without knowledge of this branch) codifies the same "ask only if evidence-insufficient and decision-changing, resolve empirical uncertainty via probes" policy at the Diagnose level — real, if indirect, corroboration that this behavior is worth having, from a source that never saw #164's evidence.

### Interaction workflow

```text
recover known owner intent (conversation/prior context)
        |
        v
run Diagnose (above) -- produce the Repository Sensemaking Brief,
        |               optionally with Section 15 filled in
        v
read the brief you just produced
        |
        v
does Section 15's extended_analysis block exist and have an
owner_intent_state?
        |
   +----+----+
   no        yes
   |          |
   |          v
   |    inspect owner_intent_state.status
   |          |
   |   +------+-------------------+
   |   |                          |
   | sufficient / thin      blocking_unknown
   |   |                          |
   |   |                          v
   |   |                    ask the owner what's needed
   |   |                    to proceed at all (a hard
   |   |                    stop, not the "one neutral
   |   |                    question" refinement below)
   |   v
   |  inspect uncertainty.source
   |          |
   |   repository_evidence -> re-run Diagnose with a narrower
   |                          investigation focus (not a new
   |                          owner question)
   |   empirical            -> formulate a bounded probe and recommend
   |                          it. Do not run it here -- Boundary Rule
   |                          #1 (No implementation) still applies in
   |                          this mode. If the probe would itself need
   |                          separate authorization (e.g. it's
   |                          ADR-0017/0021-gated, not ordinary
   |                          read-only investigation), say so; do not
   |                          assume "bounded" means "pre-authorized."
   |   owner_intent         -> would a different answer materially
   |                          change the recommendation?
   |                             no  -> proceed, note the residual
   |                                    uncertainty as non-decision-
   |                                    changing
   |                             yes -> ask ONE neutral, high-
   |                                    information question (see
   |                                    below), then proceed
   |   external_environment -> note what would need inspecting
   |                          outside this repository; do not guess
   v
synthesize and recommend, keeping these separate (do not bundle them
into one "ready to act on" recommendation, even when both are true):
  - a repository-evidence-resolved fact/fix (ready regardless of any
    open owner question)
  - an evidence-supported-but-not-owner-authorized recommendation
    (present it as a recommendation for the owner to ratify, not as
    already decided)
```

**"One question" is a working constraint, not a hard-coded rule.** If investigation genuinely produces two independent decision-changing owner-intent uncertainties, that is itself a finding worth reporting plainly rather than silently forcing both into one question or silently dropping the second — but the default is one question.

### `repository_evidence` vs. `empirical`

The discriminant is not the question's subject matter or tense ("is X true," "has X happened") — it's whether the answer already exists somewhere inspectable, or has to be newly generated:

- **`repository_evidence`**: the answer exists already, in something you can look up or search — files, git history, run logs, session artifact directories, `tool-call-trace.jsonl` records, CI history. You haven't looked yet, but looking is enough.
- **`empirical`**: nothing that already exists can answer it. Answering requires making something happen that hasn't happened yet — running a script, executing a probe, triggering an experiment.

"Has this ever caused a real failure in production" is `repository_evidence` if run logs/traces already exist to search. It's `empirical` if nothing has ever been run and the only way to find out is to run it. Get this wrong in either direction and the downstream behavior is still safe (neither branch asks the owner to guess), but get it right and the *type* of next step you recommend — search vs. probe — is the correct one, not just a defensible one.

### Neutral clarification

A clarification question that labels one option as "what the repository evidence supports" is leading, even when unintentional. Concretely, when constructing the question:

- Do not name a preferred option in the option labels.
- Do not use language that implies one answer is more evidenced than another when the uncertainty is genuinely about *owner preference*, not evidence — if it were an evidence question, it wouldn't have reached this step (`uncertainty.source` would have been `repository_evidence` or `empirical`, handled above without asking).
- State the decision each option leads to, not just the option's label — the owner is choosing a consequence, not a taxonomy term.

### Recover known intent

Before producing the brief, extract whatever the owner has already established from the conversation or prior context (this is the same extraction Stage 1 already does for `user_implied_fog_type` — apply it here as the interaction procedure's first step too, not a separate mechanism). **Do not pad thin intent to look more complete than it is** — a Section 15 `owner_intent_state.known` that overstates what's actually established defeats the field's own purpose.

### What this procedure does not do

- Does not treat this procedure as running during automated workflow execution — see the mode check above.
- Does not ask more than one clarifying question without explicitly noting why the default was insufficient.
- Does not present Section 15's fields or this interaction procedure as experimental in the final output to the user — they are ratified (ADR 0024); represent them as such, without hedging.
