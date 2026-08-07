# Repository Sensemaking Brief

## 1. Repository goal
As documented, the repository presents itself as an ingest → transform → export pipeline: docs/spec.md:3 declares the features "ingest, transform, export", docs/architecture.md:3 states the system is composed of modules ingestor.py, transformer.py, and exporter.py, and docs/roadmap.md:3 plans a real-time mode for Q3. As implemented, the repository contains a single script, src/main.py:1, that prints "hello". The repository's goal is therefore ambiguous: the documented goal (a data pipeline) has no corresponding implementation, and the implemented goal (a hello-world script) is undocumented. Resolving what this repository is actually for — pipeline-to-be-built vs. stub whose docs overstate it — is the first question any consumer must answer, and the docs currently answer it falsely.

## 2. Current shape
Inventory (Pass A): the repository root contains README.md (3 lines), docs/ (architecture.md, roadmap.md, spec.md, 3 lines each), and src/main.py (1 line). Absent: any package manifest (no pyproject.toml, setup.py, or equivalent), CI configuration, container/deployment configuration, tests, or repository-level configuration. The docs are the bulk of the repository (10 of 11 total lines).

Runtime model (Passes B-C): the only executable statement in the repository is src/main.py:1 (`print('hello')`). There is no declared entry point (no manifest), no orchestration, no domain/core logic, no persistence/state (no files, database, cache, queue, or environment configuration anywhere), no external integration points, no background work, and no output boundary beyond stdout. The documented pipeline flow (ingest → transform → export, per docs/spec.md:3 and docs/architecture.md:3) cannot be traced to any code: Pass C found no modules named ingestor.py, transformer.py, or exporter.py in the repository tree — that hop is recorded as UNKNOWN/absent rather than invented. There is no way to "start the system" other than running src/main.py directly.

Dependency semantics: no dependencies are declared (no manifest exists), none are used, and none are exercised at runtime. The module-level structure claimed by docs/architecture.md:3 is a prose-declared surface with zero implementation.

State model: no state boundaries exist — nothing writes or reads files, databases, caches, queues, or environment variables.

Boundary model (Pass D): validation structure is entirely absent — no tests, schemas, assertions, input validation, authorization, or error boundaries. The only responsibility transition in the repository is documentation → code, and that boundary is where the repository's single serious defect lives (Section 6).

## 3. Strong signals
- The documentation skeleton is small, consistent, and conventionally named: architecture, spec, and roadmap are separated into three files (docs/architecture.md, docs/spec.md, docs/roadmap.md), which is a reasonable doc structure for a small project (OBSERVED).
- docs/architecture.md:3 names concrete module boundaries (ingestor.py, transformer.py, exporter.py); if the pipeline is the intended product, this is a sensible decomposition to build toward (DERIVED — the decomposition is documented; its intent is not).
- README.md:3 defers to docs/ instead of duplicating content, keeping the README a single-purpose pointer (OBSERVED).

These are thin positives; the repository's substance is its documentation, and the documentation's substance is unverified.

## 4. Missing pieces
- Implementation of every documented module: ingestor.py, transformer.py, exporter.py do not exist anywhere in the tree (contradicts docs/architecture.md:3).
- Implementation of every documented feature: ingest, transform, export have no code (contradicts docs/spec.md:3).
- A project manifest declaring the package, entry point, and dependencies (absent — no pyproject.toml/setup.py/package.json).
- Tests or any validation structure (Pass D: none).
- A README that describes the repository beyond a pointer (README.md:3).
- Any statement of whether the docs are a plan (spec for future work) or a record of current state — the status ambiguity is what makes the mismatch unresolvable by readers.

## 5. Improvement opportunities
- Decide and record the repository's actual scope: stub vs. pipeline (one short decision note unblocks everything).
- If the pipeline is intended: add a manifest, an entry point, and implement the three documented modules in dependency order (ingestor → transformer → exporter).
- If the stub is intended: rewrite docs/architecture.md:3 and docs/spec.md:3 to describe the actual repository, and expand README.md beyond the pointer.
- Add a minimal smoke test or lint/validation script so the docs↔code contract becomes mechanically checkable (addresses the secondary Zero Validation candidate).
- Mark each docs/ file with its status (plan vs. state) so future readers can distinguish promises from facts.

## 6. Weakest boundary
Candidate generation (2-5 candidates, scored per SKILL.md):

1. Documented surface vs. actual code (docs/architecture.md:3, docs/spec.md:3 vs. src/main.py:1 and the tree inventory). evidence_strength: strong (both sides directly observed); severity: high (readers are misled about what exists); blast_radius: high (the entire documented surface — 100% of it — is affected); goal_relevance: high (the repo's purpose is unknowable from its docs); downstream_blocking_effect: high (any downstream workflow starts from a false model); uncertainty: low. → SELECTED.
2. Zero validation: no tests, schemas, or checks anywhere (Pass D). evidence_strength: strong (absence observed); severity: medium; blast_radius: medium; goal_relevance: medium; downstream_blocking_effect: low (validation only matters once logic exists); uncertainty: low. → loses: it is a downstream consequence of the code being absent, not the root defect.
3. README as information dead-end (README.md:3). evidence_strength: strong; severity: low; blast_radius: low; goal_relevance: medium; downstream_blocking_effect: low. → loses: a symptom of the docs↔code mismatch, not an independent defect.
4. Roadmap promise without a path (docs/roadmap.md:3 "Q3: real-time mode"). evidence_strength: medium (roadmaps are inherently future promises); severity: low; blast_radius: low; goal_relevance: medium; downstream_blocking_effect: low. → loses: normal roadmap behavior, not a violation.

Boundary:
Observed contract: README.md:3 directs readers to docs/ as the authoritative description; docs/architecture.md:3 states the repository is composed of modules "ingestor.py, transformer.py, exporter.py"; docs/spec.md:3 states the features are "ingest, transform, export".
Observed violation or uncertainty: the repository contains exactly one source file, src/main.py, whose entire content is `print('hello')` (src/main.py:1). None of the three documented modules exists anywhere in the tree, and none of the three documented features has any implementation. No manifest exists to declare the project at all.
Evidence: docs/architecture.md:3; docs/spec.md:3; README.md:3; src/main.py:1; full repository inventory (README.md, docs/architecture.md, docs/roadmap.md, docs/spec.md, src/main.py — nothing else).
Weakness type: **Weakness type:** Ghost Features
Logic trace: README.md:3 makes docs/ the authoritative knowledge surface for this repository → docs/architecture.md:3 states the architecture is three modules, ingestor.py, transformer.py, exporter.py → the repository inventory (Pass A) shows src/ contains exactly one file, src/main.py → src/main.py:1 is a single print statement, not an ingest/transform/export pipeline → every module and feature named in the documentation therefore has no corresponding implementation → per weakness-types.md ("Functionality mentioned in documentation that has no corresponding implementation"), this is Ghost Features. The Ghost Features classification is deliberate: the mismatch is about existence (documented surface, no implementation), not about terminology (Vocabulary Drift), format claims (Contract Mismatch), or missing checks (Zero Validation).
Failure consequence: any human or agent that reads the docs and acts on them — extending the repo, planning work, or routing to an implementation workflow — starts from a false model of what exists. Effort is mis-scoped (searching for modules that do not exist), and every doc-driven decision inherits the error. The cost grows with each downstream consumer because the docs are the only knowledge surface (README.md:3).
Confidence: high — the contradiction is directly observed on both sides (docs/architecture.md:3 claims modules; tree inventory shows they are absent) with no inference required. What would raise it further: git history or an issue tracker showing whether the modules ever existed or were planned — both are UNKNOWN in this fixture (no git metadata, no issue tracker).
Alternatives considered: (1) Zero Validation — real (no tests/schemas anywhere, Pass D) but secondary: there is no core logic to validate, so it is a consequence of the missing implementation, not the central defect; (2) README information dead-end (README.md:3) — real but low-severity and a symptom of the same mismatch; (3) Roadmap promise (docs/roadmap.md:3) — not a defect, roadmaps are future promises by nature; (4) Vocabulary Drift framing — the docs' module names have no referents, but the defect is existence, not terminology, so Ghost Features is the precise category.

## 6.5. Problem classification (fog type)
Primary fog type: docs_fog. The dominant, directly observed problem is that the documentation misdescribes the current code: docs/architecture.md:3 asserts modules that do not exist, and docs/spec.md:3 asserts features with no implementation. Applying the SKILL.md ghost-feature reasoning: the documentation is stale/aspirational in the sense that the described modules "never existed as code" → docs_fog candidate. The defect lives in the documentation's claims about the repository's current state, not in a product promise: README.md:3 does not advertise the pipeline (it merely points at docs/), and docs/roadmap.md:3 is a conventional future promise.

Secondary candidate: product_fog — if docs/spec.md:3 is read as a product contract (features the product must deliver) rather than a description, then the "promised feature absent" signal applies. This reading is noted but not primary: a spec file listing intended features is documentation about intent, and the clearest single contradiction (architecture.md:3's present-tense module list) is a documentation misdescription of the codebase, which is the definitional docs_fog signal ("docs that misdescribe current code").

Not ui_fog: the UI Fog Signals Registry gate (SKILL.md) fails at step 1 — there is no frontend code (no React/Vue/HTML/CSS/JS in the tree), so ui_fog is not evaluated further. Not architecture_fog: there is no module structure or coupling to be unclear about — the structure is absent, and the absence is a documentation claim, not a code-structure defect. Do NOT default to architecture_fog merely because classification is hard (SKILL.md ambiguity handling).

Because the docs-vs-product interpretation (docs_fog vs. product_fog) carries residual ambiguity, escalation_recommended is false only because the evidence for docs_fog is direct and observed; the residual ambiguity is recorded here in prose and flagged for the human gate at routing time (the recommended workflow's first step forces the docs↔code question).

## 7. Evidence
All claims in this brief trace to files actually opened in the target repository.

- docs/architecture.md:3 — "Modules: ingestor.py, transformer.py, exporter.py." The architecture document asserts the repository's composition; the repository inventory contradicts it (src/ contains only main.py). This is the sharpest contradiction in the repository: OBSERVED.
- docs/spec.md:3 — "Features: ingest, transform, export." The spec asserts a three-feature product surface with no implementation anywhere: OBSERVED.
- README.md:3 — "See docs/." The README makes docs/ the authoritative knowledge surface, which is why the docs' misdescription propagates to every reader: OBSERVED.
- src/main.py:1 — `print('hello')` is the entire implementation: OBSERVED.
- docs/roadmap.md:3 — "Q3: real-time mode." A future promise with no implementation path: OBSERVED (and read as a roadmap, not as a current-state claim).

Logic trace: The evidence chain is: README.md:3 establishes docs/ as the knowledge surface → docs/architecture.md:3 and docs/spec.md:3 assert modules and features that the repository inventory (and src/main.py:1) show do not exist → the documentation therefore describes functionality with no corresponding implementation → that is the Ghost Features weakness (weakness-types.md), and because the defect is the documentation's misdescription of the codebase's state (not a README product promise), the primary fog is docs_fog. The absence of any manifest, tests, or validation structure (Pass D) is corroborating context but not the selected boundary.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: docs/architecture.md
    lines: L3
    quote: "Modules: ingestor.py, transformer.py, exporter.py."
    supports_claim: "Architecture doc asserts the repository is composed of three modules; none exist in src/."
  - file: docs/spec.md
    lines: L3
    quote: "Features: ingest, transform, export."
    supports_claim: "Spec asserts three features with no corresponding implementation."
  - file: README.md
    lines: L3
    quote: "See docs/."
    supports_claim: "README defers all description to docs/, making the docs the authoritative knowledge surface."
  - file: src/main.py
    lines: L1
    quote: "print('hello')"
    supports_claim: "The only source file is a hello-world print; no pipeline logic exists."
  - file: docs/roadmap.md
    lines: L3
    quote: "Q3: real-time mode."
    supports_claim: "Roadmap promises real-time mode with no implementation path; a future promise, not a current-state claim."
```

## 9. Why this boundary matters
The docs↔code existence boundary is the only contract this repository has, and it is broken. Every downstream consumer — a human onboarding, an agent planning work, a workflow router selecting an implementation workflow — reads the docs first (README.md:3) and will act on a false model: modules that do not exist, features that do not exist. The consequence is not a subtle degradation; it is systematic mis-scoping of any work done on this repository, and it blocks the very first decision (build the documented pipeline or correct the docs) from being made correctly. Until this boundary is repaired, no other improvement (tests, manifest, implementation) can be grounded in a true understanding of the repository.

## 10. Candidate next steps
1. Human decision on intent: is the documented ingest/transform/export pipeline the intended product, or was this repository always a stub? Record the answer in a short decision note. (Precondition for everything else.)
2. If the pipeline is intended: add a manifest (e.g., pyproject.toml), declare an entry point, and implement the three documented modules in dependency order (ingestor.py → transformer.py → exporter.py) per docs/spec.md:3.
3. If the stub is intended: rewrite docs/architecture.md:3 and docs/spec.md:3 to describe the actual repository (a single script), and expand README.md:3 beyond a pointer.
4. Add a minimal smoke test / validation script so the docs↔code contract becomes mechanically checkable (addresses the secondary Zero Validation candidate).
5. Mark each docs/ file with its status (plan vs. state) so future readers can distinguish promises from facts without re-deriving them.

## 11. Recommended next step
Write the intent decision note first: a 5-line note answering "does this repository intend to implement ingest/transform/export?" with a date and owner. This is the smallest action with the highest leverage because every other candidate step branches on it: implementing the pipeline (step 2) and correcting the docs (step 3) are mutually exclusive directions, and the docs cannot be repaired truthfully (steps 3/5) until the intended scope is decided. It is also cheap: no code, no doc rewrite, one paragraph.

## 12. Recommended workflow
docs-implementation-workflow — "For documentation/knowledge problems. Aligns domain understanding, creates documentation architecture, and generates docs" (workflow-registry.yaml:812-813). Execution mode: guided_execution (an allowed mode of docs-implementation-workflow per workflow-registry.yaml:822-824; plan_only is NOT in this workflow's allowed modes, so it must not be used).

Why this workflow: primary_fog_type is docs_fog, and docs-implementation-workflow is the registry's documentation-problem workflow. Its step 1 (docs-aligner, workflow-registry.yaml:827-832) creates CONTEXT.md, which forces the docs↔code question ("what is actually in this repository") to be answered before any generation; its step 2 (to-prd, workflow-registry.yaml:834-841) produces a documentation specification defining structure and coverage — exactly the artifact that reconciles the inflated docs (docs/architecture.md:3, docs/spec.md:3) with the actual repository.

Why not the closest alternatives: implementation-workflow (workflow-registry.yaml:587-589, "architecture/code design problems") and architecture-implementation-workflow (workflow-registry.yaml:848-851) both assume the documented architecture is a valid specification to implement — but the docs' validity is precisely the open question, so running them first would build a phantom system on an unverified contract. docs-contract-reconciliation (workflow-registry.yaml:127-130) is scoped to the framework's own documentation/registries/validators, not to application repositories, and its reconciler skill does not apply here. product-implementation-workflow (workflow-registry.yaml:644-647) would only apply if the spec is reclassified as a product promise (the secondary fog candidate), which the routing should not assume.

Preconditions before this workflow can run: (1) the intent decision from Section 11 (build vs. trim), and (2) a human gate on the docs-aligner CONTEXT.md output — guided_execution provides that gate by design. If the intent decision cannot be made, escalate rather than run the workflow on an unverified contract.

## 13. Machine-readable handoff
```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/docs-heavy-code-light
source_intent_ref: "n/a - no-user-intent standalone run (fixture)"
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "docs/architecture.md (line 3): declares modules ingestor.py, transformer.py, exporter.py that do not exist in src/"
  - "docs/spec.md (line 3): declares features ingest, transform, export with no implementation"
  - "README.md (line 3): defers all repository description to docs/ (authoritative knowledge surface)"
  - "src/main.py (line 1): only source file is a single print('hello') statement"
  - "docs/roadmap.md (line 3): promises Q3 real-time mode with no implementation path (future promise)"
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-06-18T12:00:00Z"
analyzed_at: "2026-06-18T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
"Produce a workflow orchestration plan for docs-implementation-workflow in guided_execution mode, targeting repository <target_repo> (fixture docs-heavy-code-light). Precondition already diagnosed: primary_fog_type docs_fog; weakest boundary is Ghost Features — docs/architecture.md:3 and docs/spec.md:3 describe modules (ingestor.py, transformer.py, exporter.py) and features (ingest, transform, export) that do not exist; src/main.py:1 is the only code and prints 'hello'. Before routing, confirm with the human which intent applies: (a) build the documented pipeline, or (b) correct the documentation to describe the actual stub. Incorporate that decision into the plan's first gate; if the decision cannot be made, recommend escalation instead of execution. Do not implement anything."
