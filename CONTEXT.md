# Context: Sensemaking Skills

## Goal
To provide a meta-routing layer for AI agents that turns project uncertainty ("fog") into actionable problem frames, research paths, and specific skill recommendations.

## Engineering Philosophy
This repository is built on **Artifact-Driven Agentic Engineering**. We treat artifacts as the API between skills to ensure reliability, auditability, and safety. 
> See [docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md](docs/philosophy/ARTIFACT_DRIVEN_AGENTIC_ENGINEERING.md) for the deep theory.

## Core Principles
1. **Fog First**: Always classify the type of uncertainty before proposing a solution.
2. **Artifacts as API**: Skills communicate via durable artifacts, not conversation memory.
3. **Boundary Rule**: Do not perform downstream work (building) by default.
4. **Anti-Causal Confusion**: Classify defect source (Skill vs. Fixture) before any repair.
5. **Human in the Loop**: Skills provide judgment, but humans approve usefulness.

## Orchestration Principles

The workflow orchestration system follows four key design patterns, each proven through implementation and testing:

1. **Strict vs. Lenient Validation** (ADR 0001)
   - **Planning modes** (`plan_only`, `prompt_chain`) use lenient validation — artifacts don't exist yet, so only structure is checked
   - **Execution modes** (`guided_execution`, `autonomous_execution`, `yolo_execution`) use strict validation — artifacts MUST be produced or the step fails
   - **Why**: Lenient validation allows planning ahead; strict validation prevents silent failures in production
   - See: [docs/adr/0001-strict-validation-in-execution-modes.md](docs/adr/0001-strict-validation-in-execution-modes.md)

2. **Workflow Separation of Concerns** (ADR 0002)
   - Each workflow has **one clear purpose** — every step must advance that purpose
   - If a step has a different purpose, move it to a separate workflow
   - **Why**: Clear workflows are easier to understand, maintain, and compose
   - See: [docs/adr/0002-workflow-separation-of-concerns.md](docs/adr/0002-workflow-separation-of-concerns.md)

3. **Artifact Composition & Chaining** (ADR 0003)
   - Each step must **meaningfully transform** its input artifact
   - No pass-through steps, formatting steps, or renaming — each step adds semantic value
   - **Why**: Clear transformations make workflows debuggable and reusable
   - See: [docs/adr/0003-artifact-composition-pattern.md](docs/adr/0003-artifact-composition-pattern.md)

4. **Evidence Tracking for Trust** (ADR 0004)
   - Record which validators exercised which artifacts and which gates approved steps
   - Create an audit trail in `mode-coverage.yaml` proving the system works
   - **Why**: Trust comes from verifiable proof, not faith
   - See: [docs/adr/0004-evidence-tracking-for-trust.md](docs/adr/0004-evidence-tracking-for-trust.md)

5. **Three-Stage Automation** (ADR 0005)
   - **Stage 1 — Diagnostic Workflow**: User provides initial input (vague problem or repository state)
   - **Stage 2 — Orchestration (workflow-orchestrator skill)**: Analyzes diagnostic output and produces orchestration-plan with fog_type classification and recommended_workflow_id
   - **Stage 3 — Implementation Workflow (auto-invoked)**: orchestration-runner automatically reads recommended_workflow_id from orchestration-plan and invokes the implementation workflow
   - **Result**: Single entry point (fast-path-workflow or full-fog-workflow) automatically chains to the right implementation path without manual intervention
   - **Why**: Automates the human decision point between "what's the problem?" (diagnosis) and "what do we do?" (implementation)
   - **Auto-invocation mechanism**: Workflows declare `auto_invoke_next_workflow: true` and `auto_invoke_source: <artifact_id>` in workflow-registry.yaml; orchestration-runner.py detects this after workflow completion and invokes the next workflow in the same execution mode
   - **See**: [docs/adr/0005-skill-invocation-via-workflows.md](docs/adr/0005-skill-invocation-via-workflows.md)

6. **Dynamic Workflow Routing**    - **Fog Type Classification**: Sensemaking produces a classification of the primary problem type
   - **Four fog types**: product_fog (user needs), ui_fog (design), docs_fog (knowledge), architecture_fog (code structure)
   - **Automatic routing**: orchestration-runner reads fog_type from orchestration-plan and invokes the appropriate implementation workflow via auto-invocation
   - **Specialized workflows**: Four implementation workflows, each optimized for its fog type
   - **High-velocity execution**: Implementation workflows use `gate: none` between steps for automatic progression
   - **Why**: Allows single entry point (sensemaking) that automatically routes to the right implementation path
   - **Details**: See [docs/adr/0005-skill-invocation-via-workflows.md](docs/adr/0005-skill-invocation-via-workflows.md)

6. **User Intent as Durable Artifact** (ADR 0006)
   - **Immutable raw intent**: Every run creates `00-user-intent.md` that preserves exactly what the user asked for
   - **Append-only amendments**: User clarifications create separate `00b-user-clarification.md`, never edit the original
   - **Intent propagation**: Downstream artifacts (brief, plan, prd, issues) reference intent and record how it's addressed
   - **Why**: Audit trail remains unbroken; system can surface diagnosis that differs from user intent without losing user's original goal
   - See: [docs/adr/0006-intent-as-durable-artifact.md](docs/adr/0006-intent-as-durable-artifact.md)

7. **Soft Context Routing** (ADR 0007)
   - **User intent shapes the question; repo diagnosis answers it**: System recommends workflows based on code analysis, not user assumption
   - **Routing authority ladder**: Explicit override > approved gate > high-confidence diagnosis > low-confidence + intent tie-breaker > default
   - **Low-confidence diagnosis can use intent as tie-breaker**: When multiple fog types are plausible, user intent can guide selection
   - **Why**: Preserves diagnostic integrity while respecting user agency; explicit override is always available for experts
   - See: [docs/adr/0007-soft-context-routing.md](docs/adr/0007-soft-context-routing.md)

8. **Routing Divergence and Action Audit Trail** (ADR 0008)
   - **Separate system recommendation from selected action**: Every decision records what was recommended vs. what was actually chosen
   - **Explicit escalation control**: Fast-path recommends escalation to full-fog but does NOT auto-chain by default; user or execution mode must approve
   - **Scope expansion is intentional**: Implementation workflows can propose additional work, but selection stays within approved scope unless a gate approves expansion
   - **Intent changes invalidate approval**: If user re-scopes mid-workflow, prior approval becomes invalid; system pauses and requires re-approval
   - **Why**: Audit trail is complete; divergences never silent; scope creep requires intentional approval; intent changes are safely detected
   - See: [docs/adr/0008-routing-divergence-audit.md](docs/adr/0008-routing-divergence-audit.md)

**For designers**: See [docs/orchestration-patterns.md](docs/orchestration-patterns.md) for detailed patterns and [docs/workflow-design-guide.md](docs/workflow-design-guide.md) for step-by-step workflow design instructions.

## Routing Source of Truth
| Resource | Purpose |
|----------|---------|
| `skill-registry.yaml` | Find specific tools for a task |
| `workflow-registry.yaml` | Find the sequence of skills for a project mode |
| `examples/skill-tests/` | Behavioral evidence and test fixtures |
| `docs/philosophy/` | Engineering rationale and FMEA taxonomies |
| `docs/mode-coverage.yaml` | Execution mode proving status and run log references |

## Domain Language
- **Fog**: The state of project uncertainty. Four primary types:
  - **product_fog**: Unclear user needs, vague feature requirements, undocumented workflows
  - **ui_fog**: Navigation complexity, screen design issues, interaction patterns unclear
  - **docs_fog**: Missing documentation, unclear specifications, knowledge silos
  - **architecture_fog**: Code structure problems, design boundaries unclear, implicit contracts
- **Fog Type Classification**: Sensemaking stage (via `repo-sensemaker`) classifies the primary fog type to enable routing
- **Flagship Skills**: The repo contains a five-skill sensemaking pipeline: `problem-framer`, `unknowns-mapper`, `repo-sensemaker`, `workflow-orchestrator`, and `prompt-handoff`.
- **Workflow**: An ordered sequence of Skill Steps that processes fog into actionable artifacts.
- **Skill Step**: One skill invocation within a Workflow. Each Skill Step has inputs (artifacts or external context), a skill to execute, an output artifact, and an approval gate.
- **Core Skills**: Skills that always execute in a Workflow (e.g., problem-framer, unknowns-mapper, repo-sensemaker). Define the backbone of the pipeline.
- **Conditional Skills**: Skills inserted into a Workflow based on characteristics of the input or intermediate artifacts (e.g., discovery skill if raw_fog clarity is low).
- **Dynamic Chaining**: The system of routing decisions that selects the next Skill Step based on analyzed input quality or artifact content. Primary decision point: raw_fog input clarity and specificity. Secondary decision points defer until recurrence validates their necessity (Harden Only Where Pressured).
- **Sensemaking Brief**: The primary diagnostic artifact (14 sections). It must identify the "weakest boundary" and provide file-level evidence and excerpts.
- **Orchestration Plan**: The procedural artifact that includes fog type classification, recommended implementation workflow, and execution strategy
- **Implementation Workflows**: Four specialized workflows that execute based on fog type classification:
  - **product-implementation-workflow**: discovery → opportunity-tree → to-prd → to-issues → triage → tdd (for product_fog)
  - **ui-implementation-workflow**: ui-flow → ui-screen-spec → to-issues → triage → tdd (for ui_fog)
  - **docs-implementation-workflow**: to-prd → handoff (for docs_fog)
  - **implementation-workflow**: to-prd → to-issues → triage → tdd (default for architecture_fog)
- **High-Velocity Gate Pattern** (`gate: none`): Steps execute immediately without approval pauses. Used in implementation workflows for automatic progression between steps
- **Execution Modes**: The system supports `plan_only`, `prompt_chain`, `guided_execution`, `autonomous_execution`, and `yolo_execution`.
- **YOLO Execution**: High-velocity automation that bypasses approval gates for local skills. Requires explicit opt-in and feature branches.
- **Skill Split**: Diagnosis (`repo-sensemaker`) is separated from Action (`workflow-orchestrator`) to ensure human-in-the-loop validation.
- **Object Under Pressure**: The specific artifact or system boundary that is most ambiguous.
- **Weakest Boundary**: The most fragile or unenforced point in a repository. Diagnosed by repo-sensemaker via evidence-backed analysis of signal-gap boundaries.
- **Approval Gates**: Mandatory review points in an orchestration workflow. In `yolo_execution` mode, validators replace gates as the safety mechanism — gates are bypassed, but post-step validation is zero-tolerance.
- **Canonical Evidence Layer**: The validator + run-log + mode-coverage infrastructure (`scripts/validate-*.py` scripts, `docs/mode-coverage.yaml`, run logs in `runs/` and `artifacts/`) that provides machine-verifiable proof of system claims. Every workflow execution records which validators ran, which gates fired, and which artifacts were produced. This layer makes the system auditable: you can verify claims about mode coverage, gate behavior, and artifact integrity without trusting the agent that produced them. It proves the system works correctly but does not, by itself, produce value for anyone outside the system.

- **User Intent**: What the user actually cares about solving. Can come from explicit problem statement (`--problem "..."`), imported ticket, or system inference from repo state. Recorded immutably in `00-user-intent.md` and propagated through artifacts with references.
- **Intent Source**: How user intent was obtained. Values: `user_problem_statement` (explicit CLI), `repo_inferred` (system guessed from code), `imported_ticket` (loaded from issue tracker).
- **Scope Mode**: How strictly intent constrains the system's analysis. Values: `soft` (intent is context; system can surface broader concerns), `hard` (intent defines boundary; out-of-scope findings are appendix-only), `advisory` (intent is primary; system can propose conflicts but execution stays bounded).
- **Intent Amendment**: A user clarification or re-scoping created mid-workflow. Stored as separate artifact (`00b-user-clarification.md`, etc.), never edits to original intent. Invalidates prior approval if it changes routing/scope.
- **Routing Divergence**: Occurs when `system_recommended_workflow` differs from `selected_workflow`. May be due to explicit user override, low-confidence diagnosis + intent tie-break, or approved gate decision. Always recorded with rationale in orchestration plan.
- **Routing Decision Method**: How the system chose which workflow to run. Values: `diagnosis_primary_soft_context` (repo diagnosis won), `intent_tiebreaker` (user intent broke a low-confidence tie), `user_explicit_override` (user --workflow flag), `approved_gate` (human approval changed the decision), `escalation_approved` (escalation to deeper analysis was approved).
- **Escalation**: Fast-path workflow recommends deeper analysis (full-fog) when uncertainty is high or diagnosis conflicts with intent. Escalation is recommended but NOT automatic by default; user or execution mode must approve. Recorded as `escalation_recommended: true` with `auto_escalation_allowed: false`.
- **Scope Expansion**: Implementation workflows (to-prd, to-issues) can propose work beyond the user's stated intent. Proposed expansions are explicit and require approval before being included in selected scope. Recorded as `scope_expansion_proposed: [list]` and `scope_expansion_requires_approval: true`.

- **Harden Only Where Pressured**: A principle for post-run system improvement — restrict changes to boundaries where live execution exposes a **repeatable failure boundary** (same failure class across independent runs). Isolated one-off data issues are fixed in the artifact but do not trigger system hardening. Prevents preemptive over-engineering based on theory alone.
  **Enforcement rule**: System-level hardening (new validators, runner features, or evidence tools) is only permitted when at least one condition is met: (1) a real (non-test) run fails with a specific error, (2) the same failure class recurs across independent runs, or (3) CI or static analysis detects a real inconsistency that a live run would miss. Exempted: artifact data fixes, bug fixes in existing validators, test fixtures, documentation, and contract/registry registration.
  Validated by the first fast-local-diagnostic run: the brief theorized "Contract Mismatch" but the run stressed only weakness-type and logic-trace authoring, and those were single-occurrence data issues — no structural hardening was warranted. All subsequent runs record `hardening_triggered: none` in mode-coverage.yaml, confirming no structural hardening has been triggered to date.

- **Repeatable Failure Boundary**: A failure class that recurs across independent live runs, signaling a systemic gap rather than an isolated data-quality issue. Determines whether a friction point triggers system hardening (repeatable) or artifact-level correction (single occurrence). Example: if UNKNOWN_WEAKNESS_TYPE occurs in two different workflow runs with different authors, that's a repeatable pattern warranting tooling improvement; a one-time authoring mistake is not.

- **System-Proving Run vs. Value-Production Run**: A distinction in run purpose. A **system-proving run** exists to demonstrate that the orchestrator, validators, gates, and run-log infrastructure work correctly — the run log notes say "Proves X works." A **value-production run** uses the proven system to produce artifacts someone outside the system wants — the purpose is the outcome, not the proof. The 5 PRD mode-proving runs plus all subsequent guided_execution runs (full-local-sensemaking, product-discovery-sprint, skill-maintenance-loop, validator-live-coverage) are system-proving. No value-production run exists yet. The canonical evidence layer is necessary before value-production is safe, but it is not sufficient — the system must also be *used*.
- **Evidence Source Rule**: Going forward, mode-coverage entries and run logs MUST be produced by `orchestration-runner.py`, not hand-authored. Existing hand-authored entries (e.g., early yolo and guided_execution runs from 2026-05-14 through 2026-05-16 morning) are grandfathered. This ensures all evidence is machine-verifiable and follows the canonical execution path.
- **TDD Validator Cycle**: The red-green-refactor loop triggered when a Level 3 validator fails during a workflow run. Failure = RED, artifact data fix = GREEN, re-validation pass = REFACTOR. Demonstrated in the first YOLO run when validate-brief.py caught UNKNOWN_WEAKNESS_TYPE and NO_LOGIC_TRACE.
- **Tracer Bullets**: AFK-compatible vertical slices of implementation.
- **Validator Verification Suite**: A repeatable verification mechanism that checks validator behavior against positive and negative fixtures. It confirms that valid artifacts pass, invalid artifacts fail, and expected failures fail for the intended reason. Now enforces mandatory fixture coverage for all validator scripts.

## Artifact Run Organization

Artifacts from pipeline runs follow a flat numbered sequence at `artifacts/` root:

```
artifacts/
├── 01-metamorfose-finance/       ← NN-project-name/
│   ├── 01-problem-frame.md       ← NN-file-name.md
│   ├── 02-unknowns-map.md
│   ├── 03-sensemaking-brief.md
│   ├── 04-orchestration-plan.md
│   ├── 05-run-analysis.md
│   └── README.md
├── 02-metamorfose-classes/
│   ├── 01-problem-frame.md
│   └── ...
├── 03-[next-run]/
├── meta-analyses/                ← cross-run analyses
├── ORGANIZATION-GUIDE.md
└── README.md
```

**Rules:**
- **Numbered run folders**: `NN-project-name` at `artifacts/` root — no `runs/` subfolder nesting
- **Numbered files inside**: `NN-file-name.md` showing pipeline sequence
- **Historical root-level files**: Left in place as pre-organization archive — not migrated
- **Path convention**: The workflow-orchestrator outputs future runs to `artifacts/NN-project-name/NN-file-name.md`
- **Run folder numbering**: Monotonic across time — each new run gets the next integer in the sequence, regardless of date. Date metadata lives in the run's `README.md` or content, not the folder name.

## Known Gaps

These are acknowledged gaps that the project is aware of but has not yet addressed. The gaps are ordered by practical impact.

- **Rollback-after-mutation proven** (closed): Test 8 proves the runner recommends ROLLBACK_RECOMMENDED with correct recovery commands (`git reset --hard HEAD`, `git clean -fd`). Test 9 proves those commands actually restore mutated state in an isolated temp repo — committed files revert to original content, untracked files are removed, git tree returns to clean. The full mutation → failure → rollback → recovery cycle is verified.
- **Controlled failure tests can silently skip under dirty local state** : Integration tests
    (gate denial, resume) include a guard that skips when the git tree is not clean.
    In CI this guard is never triggered. Locally, the test suite now reports skipped
    tests as `[SKIP]` (distinct from passed) and exits with code 2 when any tests are
    skipped. The skip is visible and actionable rather than silent. Run with a clean
    git tree to prove the full integration path.
- **Failure-ledger has not detected organic repeated failures** (no action needed): `analyze-run-failures.py` detects repeatable failure boundaries, and the controlled test proves the mechanism. But no organic runs have produced repeated failures yet. The learning loop is too young to have generated enough failure data. This resolves with time as more value-production runs accumulate.
- **No value-production runs exist** (blocked — see preconditions): All runs to date are system-proving. A value-production run requires: (a) a clean git worktree (guided_execution and higher modes enforce this), (b) external raw_fog input from a real stakeholder with an actual problem, and (c) human gate approval for each step (or --gate-decision auto-approve for non-interactive proving). Until a real external need triggers such a run, the operating habit of using the system for productive work remains unproven. See **System-Proving Run vs. Value-Production Run** above.

## Tech Stack
- Markdown-based skill definitions (`SKILL.md`).
- YAML-based registries and agent definitions.
- Relative linking for package portability.

## Skills Split
1. **repo-sensemaker**: Diagnostic. Finds the weakest boundary.
2. **workflow-orchestrator**: Procedural. Acts on the weak point via gated sequences.
3. **docs-aligner**: Domain alignment. Resolves contradictions between code and documentation, sharpens terminology, and updates CONTEXT.md inline. Automates grilling for autonomous workflows.

## Ecosystems
- **Interface Skills**: Spec Packages and UI validation.
- **Matt Pocock Skills**: Engineering rigor, TDD, and docs-aligner (domain alignment).
- **Product Manager Skills**: Discovery, PRDs, and Strategy.

## Automation & Validation (scripts/)
The repository uses a Python-based three-level validator hierarchy to enforce artifact integrity and safety:

- **Level 1 — Structural** (`validate-repo.py`): Repository-wide consistency checks across registries and examples. Runs pre-flight before any workflow that mutates the repo.
- **Level 2 — Generic** (`validate-artifact.py`): Universal contract checks (sections, machine fields, no absolute paths). Runs after every artifact-producing step.
- **Level 3 — Specialized** (one per artifact type): Semantic checks requiring registry cross-references. Currently:
  - `validate-brief.py` — enforces evidence grounding, weakness-type recognition, workflow-ID validation
  - `validate-plan.py` — verifies workflow steps, execution modes, approval gates, stop conditions
  - `validate-skill-improvement-plan.py` — enforces formal failure mode classification and anti-overfitting
  - `validate-usage-research-report.py` — checks semantic scores, role boundaries, evidence grounding
  - `validate-prompt-handoff.py` — checks target skill exists in registry, artifact refs are real, stop conditions have content
- **`validate-output.py`**: Dispatcher that delegates to per-artifact validators via `artifact-contracts.yaml`. This is the normal validation path — all runs should use it instead of calling validators directly.
- **`validate-run-log.py`**: Validates run log structure against the template specification. Checks header fields, step structure, gate recording consistency (gate_result, approved_at, approved_by), pre-flight documentation, and path hygiene.
- **`analyze-run-failures.py`**: Builds a failure ledger from all run logs in a directory. Detects repeatable failure boundaries (same error code across 2+ independent runs) per the Repeatable Failure Boundary principle.
- **`_validator_utils.py`**: Shared utility module for registry loading, path resolution, and error formatting.

In YOLO and autonomous execution modes, validators function as **zero-tolerance safety gates**: any failure triggers an immediate hard stop and rollback recommendation. See [validator-stack-policy.md](skills/workflow-orchestrator/references/validator-stack-policy.md) for execution order.

## Dynamic Chaining Implementation

**Overview:** Workflows support conditional routing of Skill Steps based on artifact signals. The primary decision point is the clarity of the initial raw_fog input, detected by unknowns-mapper and encoded in the unknowns_map routing fields.

**Routing Signal:** unknowns_map.research_needed (boolean)
- Determined by: `(unknowns_count >= 5) OR (clarity_assessment == "low")`
- If true: A discovery or research skill is inserted into the workflow
- If false: The workflow skips to repo-sensemaker

**Provisional Heuristic:** The thresholds (5 unknowns, "low" clarity) are initial estimates. They are validated empirically in early value-production runs, then refined using repeatable failure analysis.

**Conditional Step Schema:** Workflows can define conditional steps with if_true/if_false branches:
```yaml
- id: 3-conditional
  conditional: true
  decision_field: unknowns_map.research_needed
  if_true:
    skill: discovery
    gate: review_discovery
    input_artifact: unknowns_map
    output_artifact: discovery_findings
    next_step: 4
  if_false:
    next_step: 4
```

**Machine Fields on unknowns_map:**
- clarity_assessment: "high" | "medium" | "low"
- unknowns_count: integer (count of unknowns)
- assumptions_count: integer (count of unvalidated assumptions)
- research_needed: boolean (routing decision)

**Validators:**
- `validate-unknowns-map.py` — Validates unknowns_map routing fields are present and well-typed
- `validate-plan.py` — Validates conditional step logic references real skills
