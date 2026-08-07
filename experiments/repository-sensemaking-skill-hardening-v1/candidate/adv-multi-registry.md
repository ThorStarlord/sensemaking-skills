# Repository Sensemaking Brief

## 1. Repository goal

The repository's goal is **UNKNOWN** from the inspected evidence. `README.md:1` contains only the title `# multi-registry` — no goal statement, no feature list, no usage or architecture explanation (OBSERVED). The only executable, `main.py:1`, is a single `print('app')` statement (OBSERVED). The remaining content is two workflow-registry data files (`.workflows/registry.yaml`, `docs/workflow-registry.yaml`) whose relationship to the code is not documented anywhere. Based on the inventory, the repo appears to be a minimal Python scaffold that also ships workflow-registry metadata, but that purpose is INFERRED — nothing in the repository states it.

## 2. Current shape

**Inventory (OBSERVED, Pass A — root inventory and manifests):**
- `README.md` — 1 line, a bare title (`# multi-registry`).
- `main.py` — 1 line, `print('app')`.
- `.workflows/registry.yaml` — 3 lines (a workflow ID list).
- `docs/workflow-registry.yaml` — 3 lines (a workflow ID list).

Absent (OBSERVED absence in the recursive inventory): package manifest (`pyproject.toml`, `requirements.txt`), build configuration, CI configuration, container/deployment configuration, any other top-level documentation, any repository-level configuration, any tests.

**Runtime flow (Pass B — execution discovery, Pass C — system structure):**
- Startup path: `python main.py` → `print('app')` at `main.py:1` (OBSERVED). This is the only entry point; there are no package scripts, CLI commands, server bootstrap, route registrations, workers, or helper scripts.
- Orchestration: none — the program is a single statement.
- Domain/core logic: none.
- Persistence/state: none — no files, databases, caches, global/module state, queues, environment-variable reads, or remote systems.
- External integration points: none.
- Background work: none.
- Output boundary: stdout, via `print` at `main.py:1`.
- Validation: none anywhere (Pass D) — no tests, schemas, assertions, input validation, authorization, or error boundaries.

**Registry files:** Both are static data files. Nothing in the repository imports, reads, or validates them (OBSERVED — `main.py:1` is the only module in the tree; no consumer exists). How they are supposed to be consumed is **UNKNOWN** — no consumer could be found, so their intended use cannot be established from inspected files.

**Dependency semantics:** No declared dependencies exist (no manifest of any kind). The registry files reference workflow IDs whose authoritative definitions live in the external canonical registry (`skills/workflow-planner/references/workflow-registry.yaml`) — an implicit, undeclared dependency on that vocabulary (INFERRED from the ID spellings matching the canonical registry's vocabulary).

**Where responsibility becomes unclear:** at the two registry files — they both claim to enumerate the repository's workflows but disagree with each other about which workflows exist (see Section 6).

## 3. Strong signals

- The entry point is real and runnable: `main.py:1` executes a complete (if trivial) program — this is not a broken or stubbed entry point (OBSERVED).
- `.workflows/registry.yaml:2-3` uses workflow IDs that exactly match canonical IDs — `architecture-implementation-workflow` (canonical at `skills/workflow-planner/references/workflow-registry.yaml:848`) and `fast-path-workflow` (canonical at `skills/workflow-planner/references/workflow-registry.yaml:2`) — so at least one in-repo artifact is vocabulary-aligned with the authoritative registry (OBSERVED, contrastive).
- Minimalism: no dependency graph, no build complexity, no vendored or generated content — there is almost nothing to maintain yet (OBSERVED via inventory absence).

## 4. Missing pieces

- README content: no goal, no usage, no explanation of the registry files (OBSERVED — `README.md:1` is the only line).
- Any consumer or documentation of the two workflow registries (OBSERVED — no reader of either file exists in the tree).
- Tests or validation of any kind (OBSERVED — no test files, no assertions, no schemas).
- Package metadata (`pyproject.toml` / `requirements.txt`) (OBSERVED absence).
- Reconciliation between the two in-repo registries (DERIVED from the contradiction documented in Section 6).

## 5. Improvement opportunities

- Expand the README to state the repo's purpose and how the registry files are consumed.
- Consolidate the two in-repo registries into a single source of truth (or explicitly document which is authoritative).
- Add a trivial smoke test (e.g., assert `main.py` runs) and — if the registries matter — a check that every in-repo workflow ID exists in the canonical `skills/workflow-planner/references/workflow-registry.yaml`.
- Add packaging metadata if the scaffold is intended to grow.

## 6. Weakest boundary

**Candidate generation (from Pass E — contradiction search):**

Candidate 1 — In-repo registry vocabulary vs. the authoritative vocabulary.
- boundary: `docs/workflow-registry.yaml:2-3` vs. canonical `skills/workflow-planner/references/workflow-registry.yaml:2`, `:848`
- evidence_strength: strong (verbatim ID text on both sides)
- severity: high (invalid workflow IDs break downstream routing/validation)
- blast_radius: medium (only tooling that consumes the repo's registry; the one-line app itself is unaffected)
- goal_relevance: high (the registries are the repo's only substantive content)
- downstream_blocking_effect: high (any routing grounded on the repo's own docs fails)
- uncertainty: low

Candidate 2 — Zero Validation (whole repo: no tests/schemas/assertions).
- evidence_strength: medium (absence is observable but proves little)
- severity: low (one-line program; nothing complex to validate)
- blast_radius: low
- goal_relevance: low
- downstream_blocking_effect: low
- uncertainty: medium

Candidate 3 — Ghost Features (`docs/workflow-registry.yaml:2-3` promises `arch-implementation-workflow` / `fastpath-workflow`, which exist nowhere).
- evidence_strength: strong
- severity: medium
- blast_radius: medium
- goal_relevance: medium
- downstream_blocking_effect: medium
- uncertainty: medium — rejected on taxonomy grounds: the canonical workflows these IDs approximate DO exist; the docs misname existing entries, which the GAP-6 mapping assigns to Vocabulary Drift, never Ghost Features.

Candidate 4 — Implicit Dependencies (registries depend on the canonical registry without declaring or validating it). Real but secondary: the observable defect is a naming mismatch with direct text evidence, not an undeclared path.

**Selection — Candidate 1:**

```text
Boundary: the repository's workflow-registry documentation (docs/workflow-registry.yaml:2-3)
          vs. the authoritative workflow vocabulary
          (skills/workflow-planner/references/workflow-registry.yaml:2, :848).
Observed contract: docs/workflow-registry.yaml presents itself as a workflow registry
          enumerating valid workflow IDs.
Observed violation or uncertainty: the two in-repo registries contradict each other
          (.workflows/registry.yaml:2-3 lists architecture-implementation-workflow and
          fast-path-workflow; docs/workflow-registry.yaml:2-3 lists arch-implementation-workflow
          and fastpath-workflow), and the docs copy's two IDs do not exist in the canonical
          registry. Nothing in the repository validates either file against the canonical one.
Evidence: docs/workflow-registry.yaml:2-3; .workflows/registry.yaml:2-3;
          skills/workflow-planner/references/workflow-registry.yaml:2 and :848.
Weakness type: **Weakness type:** Vocabulary Drift
Logic trace: docs/workflow-registry.yaml:2-3 (OBSERVED) enumerates the IDs
          arch-implementation-workflow and fastpath-workflow. The canonical registry
          defines the authoritative spellings architecture-implementation-workflow
          (skills/workflow-planner/references/workflow-registry.yaml:848) and
          fast-path-workflow (skills/workflow-planner/references/workflow-registry.yaml:2)
          (OBSERVED, contrastive). .workflows/registry.yaml:2-3 (OBSERVED) uses those
          canonical spellings, so the repository's own two registry documents disagree
          with each other, and the docs copy drifts from the authoritative vocabulary.
          No file in the repository reads or validates either registry (OBSERVED — the
          only module is main.py:1), so nothing catches the drift. Terms used in the
          repository's documentation therefore do not match the authoritative vocabulary:
          Vocabulary Drift.
Failure consequence: any consumer that trusts the repo's own docs registry emits workflow
          IDs the runtime rejects (invalid-ID validation failure) or silently targets
          nonexistent workflows; the two registries give contradictory answers to "which
          workflows exist," so even a human reader cannot tell the intended vocabulary.
Confidence: high. What would raise it: finding a consumer of these registries (none exists
          in the repo — how they are used is UNKNOWN) or a commit/issue stating which
          registry is authoritative.
Alternatives considered: Zero Validation (rejected as primary — the absence of tests is
          real but low-consequence for a one-line program, and validation is a remedy for
          the drift, not the defect itself); Ghost Features (rejected per the GAP-6 mapping —
          the canonical workflows exist and docs/workflow-registry.yaml misnames existing
          entries, so Vocabulary Drift applies, never Ghost Features); Implicit Dependencies
          (secondary contributor — the registries implicitly depend on the canonical
          registry — but the observed failure is a naming mismatch, not an undeclared path).
```

If this candidate's evidence were absent, the honest answer would be "no serious weakness"; here the evidence is direct and the consequence concrete, so the boundary is real.

## 6.5. Problem classification (fog type)

Primary fog: **docs_fog**. The conflict lives in the documentation layer: two in-repo registry documents contradict each other (`docs/workflow-registry.yaml:2-3` vs. `.workflows/registry.yaml:2-3`, OBSERVED) and one diverges from the authoritative vocabulary (contrastive OBSERVED vs. `skills/workflow-planner/references/workflow-registry.yaml:2`, `:848`). The implementation (`main.py:1`) is coherent and runs; the defect is not in code structure.

- `ui_fog`: does not apply — no frontend code exists at all (`main.py` is the only source file; no React/Vue/Angular/HTML/CSS), so the UI Fog decision tree's first branch is NO.
- `product_fog`: does not apply — `README.md:1` advertises no product features or deliverables, so no product contract is violated.
- `architecture_fog`: does not apply — the sole entry point exists and runs (`main.py:1`), so this is not a structural entry-point defect, and there is no module structure whose boundaries could be unclear.

Secondary fog: none strong. A minor documentation gap (README is a bare title) reinforces `docs_fog` but does not change routing. No user intent was provided for this run (fixture/standalone), so per GAP-8 `user_implied_fog_type` is `unknown` and there is no intent conflict.

## 7. Evidence

The diagnosis rests on four target-repository files, all opened and read in full:

- `README.md:1` — the entire README is the title `# multi-registry`; no goal, features, or registry documentation (OBSERVED).
- `main.py:1` — the entire program is `print('app')` (OBSERVED).
- `.workflows/registry.yaml:2-3` — lists `architecture-implementation-workflow` and `fast-path-workflow`, both of which ARE canonical IDs (OBSERVED).
- `docs/workflow-registry.yaml:2-3` — lists `arch-implementation-workflow` and `fastpath-workflow`, which are NOT canonical IDs (OBSERVED; contrastive against `skills/workflow-planner/references/workflow-registry.yaml:2` and `:848`).

No test files, manifests, build/CI configuration, or additional documentation exist in the repository (OBSERVED via the full recursive inventory).

Logic trace: The canonical registry `skills/workflow-planner/references/workflow-registry.yaml` defines `fast-path-workflow` (line 2) and `architecture-implementation-workflow` (line 848). `.workflows/registry.yaml:2-3` copies those exact spellings (vocabulary-aligned). `docs/workflow-registry.yaml:2-3` instead contains `arch-implementation-workflow` and `fastpath-workflow` — near-miss spellings that exist nowhere in the canonical registry and directly contradict the repo's other registry. Since both in-repo files claim to be workflow registries and no code consumes either (`main.py:1` is the only module), the disagreement is a documentation-layer vocabulary conflict: the repo's documentation drifts from the authoritative vocabulary. That is Vocabulary Drift, and because the failing surface is documentation — not code structure, not product promises, not UI — the fog type is `docs_fog`.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L1
    quote: "# multi-registry"
    supports_claim: "README contains only a bare title; no goal, feature list, or documentation of the registry files."
  - file: main.py
    lines: L1
    quote: "print('app')"
    supports_claim: "The entire runtime is a single print statement: no logic, orchestration, persistence, or validation."
  - file: .workflows/registry.yaml
    lines: L1-L3
    quote: "workflows:\n  - id: architecture-implementation-workflow\n  - id: fast-path-workflow"
    supports_claim: "One in-repo registry uses workflow IDs that exist in the canonical registry (vocabulary-aligned)."
  - file: docs/workflow-registry.yaml
    lines: L1-L3
    quote: "workflows:\n  - id: arch-implementation-workflow\n  - id: fastpath-workflow"
    supports_claim: "The other in-repo registry uses workflow IDs that do not exist in the canonical registry and contradict .workflows/registry.yaml — Vocabulary Drift."
```

## 9. Why this boundary matters

If this boundary remains weak, any consumer that trusts the repository's documentation — a workflow-planner run, an agent grounding routing on the in-repo registry, or a human reading the docs — will emit or act on workflow IDs that do not exist. The runtime's validator rejects such IDs (HALLUCINATED_WORKFLOW_ID), so routing fails or silently targets nothing. The repository currently gives two contradictory answers to "which workflows exist," and nothing catches the contradiction, so the drift persists until a human notices it. Because the registries are the only substantive content this repository contains, the drift undermines the repository's sole asset — its documentation — and erodes trust in any future tooling that reads it.

## 10. Candidate next steps

1. Reconcile `docs/workflow-registry.yaml:2-3` with the canonical vocabulary: `arch-implementation-workflow` → `architecture-implementation-workflow`, `fastpath-workflow` → `fast-path-workflow`.
2. Consolidate the two in-repo registries into one (or delete the redundant one), explicitly stating which is authoritative.
3. Add a validation check (test/CI) that every in-repo workflow ID exists in the canonical `skills/workflow-planner/references/workflow-registry.yaml`.
4. Expand the README to state the repository's goal and how the registry files are consumed.
5. Add minimal packaging metadata and a smoke test for `main.py`.

## 11. Recommended next step

Step 1 — correct the two IDs in `docs/workflow-registry.yaml:2-3` (or delete that file if `.workflows/registry.yaml` is the intended source of truth). It is the smallest concrete change with the highest leverage: it removes the invalid-ID hazard that breaks any downstream routing, and it forces the decision of which registry is authoritative.

## 12. Recommended workflow

`docs-contract-reconciliation` — from the canonical `skills/workflow-planner/references/workflow-registry.yaml:127` — whose purpose is to "Resolve drift between documentation, registries, artifact contracts, templates, and validator rules." This is the purpose-built workflow for the diagnosed defect: drift between the repository's documentation/registries and the authoritative vocabulary. Execution mode: `plan_only` (one of `docs-contract-reconciliation`'s `allowed_execution_modes`, registry line 138) — the brief is a diagnostic artifact and the skill's No Implementation boundary holds; `plan_only` produces the reconciliation plan for human review without executing changes.

Why not the closest alternatives:
- `docs-implementation-workflow` (registry line 812): built for generating documentation/knowledge artifacts, not for reconciling conflicting vocabulary; its allowed modes (`guided_execution`, `autonomous_execution`) also skip `plan_only`, which is the right mode for this diagnostic handoff.
- `docs-architecture` (registry line 187): aligns documentation with domain language via `docs-aligner`; it addresses domain terminology, not registry/vocabulary drift.
- `architecture-implementation-workflow` (registry line 848): for code-structure defects; none exists here (`main.py:1` runs).
- `fast-local-diagnostic` (registry line 477): a diagnostic loop that ends in a handoff prompt; it has no reconciliation step for the drift, which is the actual defect.

Preconditions before it can run: none blocking — the repository state (two conflicting registries) is exactly the input this workflow consumes. Routing is grounded exclusively on the canonical registry; the in-repo registries (`.workflows/registry.yaml`, `docs/workflow-registry.yaml`) were used as evidence of the defect only, never as routing authority.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-multi-registry
workflow_registry_source: "skills/workflow-planner/references/workflow-registry.yaml (canonical)"
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md:1 - bare title; no goal or feature documentation"
  - "main.py:1 - single print statement; no logic or validation"
  - ".workflows/registry.yaml:2-3 - IDs match canonical registry (architecture-implementation-workflow, fast-path-workflow)"
  - "docs/workflow-registry.yaml:2-3 - IDs do not exist in canonical registry (arch-implementation-workflow, fastpath-workflow); contradicts .workflows/registry.yaml"
recommended_workflow_id: docs-contract-reconciliation
recommended_execution_mode: plan_only
weakest_boundary: Vocabulary Drift
weakness_type: Vocabulary Drift
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

"Run workflow `docs-contract-reconciliation` in `plan_only` mode against the adv-multi-registry repository. Input: this repository sensemaking brief (primary fog: docs_fog; weakest boundary: Vocabulary Drift between `docs/workflow-registry.yaml:2-3` and the canonical `skills/workflow-planner/references/workflow-registry.yaml`). Produce a reconciliation plan that (1) resolves the two conflicting in-repo registries — `docs/workflow-registry.yaml` lists `arch-implementation-workflow` and `fastpath-workflow`, which are not canonical IDs, while `.workflows/registry.yaml` uses the canonical spellings — (2) states which registry is authoritative, and (3) proposes a validation check that every in-repo workflow ID exists in the canonical registry. Do not modify the repository; deliver the plan for approval."
