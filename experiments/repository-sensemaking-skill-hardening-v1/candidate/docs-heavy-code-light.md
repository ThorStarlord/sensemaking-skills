# Repository Sensemaking Brief

## 1. Repository goal

The repository presents itself as "docs-heavy" (README.md:1 `# docs-heavy`), a documentation-first repository whose stated purpose — carried entirely by its docs — is a data-processing pipeline: docs/architecture.md:3 declares three modules (`ingestor.py`, `transformer.py`, `exporter.py`) and docs/spec.md:3 declares three features (`ingest`, `transform`, `export`). docs/roadmap.md:3 plans a "real-time mode" for Q3. The apparent intent is a small ingest → transform → export pipeline product; whether the docs describe a current deliverable or a design intent is left ambiguous — and no code implements any of it (src/main.py:1).

## 2. Current shape

Runtime flow (architecture reconstruction, per SKILL.md):

- **Startup**: the only executable file is `src/main.py` (src/main.py:1), a one-line `print('hello')` stub. Nothing else can start the system; no manifest, entry-point declaration, launcher, or script exists in the tree. The recursive repository listing contains exactly five files: `README.md`, `docs/architecture.md`, `docs/roadmap.md`, `docs/spec.md`, `src/main.py`.
- **Orchestration**: none. No code exists that sequences ingest → transform → export or any other flow.
- **Domain/core logic**: none. The modules declared at docs/architecture.md:3 (`ingestor.py`, `transformer.py`, `exporter.py`) do not exist as files — OBSERVED absence in the listing; nothing under `src/` or anywhere else.
- **Persistence/state**: none. No state boundary of any kind (no files written, no database, no cache, no environment-variable reads).
- **External integration**: none.
- **Background work**: none.
- **Output boundary**: `print('hello')` at src/main.py:1 — a hello-world to stdout, unrelated to the documented pipeline.
- **Validation**: none. No tests, no schemas, no assertions, no CI configuration exist in the repository (Pass D).

Dependency semantics: there is no manifest of any kind, so the `declared` / `used` / `runtime` / `test` / `optional` / `dead` classes are all empty. The only `runtime`-class behavior proven by inspection is the `print('hello')` statement in src/main.py:1 — and even that is not proven to be launched by anything (how the repository is invoked is UNKNOWN).

Responsibility becomes unclear immediately: the docs describe modules and features, but there is no code for them and no documented way to run the repository. Every hop of the documented pipeline (entry point → orchestration → domain → persistence → output) is recorded as UNKNOWN because the hops do not exist; per the exploration protocol they are not invented.

## 3. Strong signals

- **Internally consistent documentation vocabulary**: docs/architecture.md:3, docs/spec.md:3, and docs/roadmap.md:3 use one coherent vocabulary (ingest/transform/export), so the intended product shape is legible.
- **Documentation-first orientation**: README.md:3 ("See docs/.") deliberately delegates description to docs/, a workable convention if the docs track reality.
- **Tiny surface**: five files total — the cost of bringing the documented surface and the implementation into agreement is low.
- **Roadmap awareness**: docs/roadmap.md:3 shows forward thinking (real-time mode), i.e., the author has a direction.

## 4. Missing pieces

- All three documented modules — `ingestor.py`, `transformer.py`, `exporter.py` (docs/architecture.md:3) — are absent from the repository (OBSERVED in the listing).
- All three documented features — ingest, transform, export (docs/spec.md:3) — have no implementation anywhere.
- A real entry point: src/main.py:1 is a hello-world stub; nothing invokes or wires any pipeline stage.
- Packaging/build metadata: no manifest (no pyproject.toml, setup.py, requirements.txt, package.json, etc. — OBSERVED absent).
- Validation structure: no tests, no CI, no schemas (Pass D: nothing checks the build/test contract).
- Run instructions: no document explains how the system is launched (UNKNOWN).
- Docs-vs-intent statement: nothing states whether docs/spec.md describes a current deliverable or a target design (UNKNOWN).

## 5. Improvement opportunities

- Replace src/main.py:1 with a real CLI/library entry point that at least loads the pipeline stages.
- Add a minimal manifest (e.g. pyproject.toml) declaring the entry point and test configuration — closes the Zero Validation gap once there is code to validate.
- Add a smoke test asserting the ingest → transform → export contract.
- Mark docs/architecture.md and docs/spec.md as design intent (or remove them until implemented) so readers stop inferring existing functionality.
- Add a run/usage section to README.md so the repository's execution model is no longer UNKNOWN.

## 6. Weakest boundary

Candidates generated and scored (evidence_strength / severity / blast_radius / goal_relevance / downstream_blocking_effect / uncertainty):

| # | Boundary | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|---|
| 1 | Documented product surface vs. implementation (docs/architecture.md:3, docs/spec.md:3 promise modules + features; only code is src/main.py:1 hello-world) | strong | high | high | high | high | low |
| 2 | Entry-point contract: src/main.py:1 stub is the sole runnable surface, with no wiring to documented stages | strong | medium | high | high | medium | medium (is main.py even the intended entry point? docs never say) |
| 3 | Packaging/build contract: no manifest, no test runner, no CI — nothing validates the build/test contract | strong (absence) | medium | medium | medium | medium | low |
| 4 | Doc completeness: docs are three lines each; no run instructions, no design-vs-current distinction | medium | low | low | medium | low | low |

Selection: candidate 1 wins on every dimension that matters — it is the only candidate with high consequence (the entire documented product is absent), strong direct evidence (all files inspected; the modules simply do not exist), highest goal relevance (it is the repository's stated purpose), and it blocks all valuable downstream work (nothing can be implemented, documented, or validated until the docs↔code relationship is resolved).

Boundary:
The documented product surface (modules `ingestor.py`/`transformer.py`/`exporter.py` at docs/architecture.md:3; features ingest/transform/export at docs/spec.md:3) versus the actual implementation surface (src/main.py:1, `print('hello')`).

Observed contract:
docs/architecture.md:3 and docs/spec.md:3 present a working pipeline: three modules implementing three features. README.md:3 directs readers to those docs as the repository's description.

Observed violation or uncertainty:
None of the documented modules or features has any implementation, import, or reachable execution path anywhere in the repository. The only executable statement is src/main.py:1 (`print('hello')`), which is unrelated to the documented pipeline. No file named `ingestor.py`, `transformer.py`, or `exporter.py` exists (OBSERVED in the recursive listing of the five repository files).

Evidence:
- docs/architecture.md:3 — "Modules: ingestor.py, transformer.py, exporter.py."
- docs/spec.md:3 — "Features: ingest, transform, export."
- src/main.py:1 — "print('hello')"
- Repository listing — only README.md, docs/architecture.md, docs/roadmap.md, docs/spec.md, src/main.py exist.

Weakness type:
Ghost Features

Logic trace:
The docs declare a module and feature surface (docs/architecture.md:3, docs/spec.md:3) as if it were the repository's current shape, and the README (README.md:1, README.md:3) presents the repository as documentation of that surface. Pass B of the exploration protocol found exactly one executable: src/main.py:1, a hello-world print. Pass C could not trace a single hop of the documented pipeline because none of its components exist; Pass E found the contradiction directly: documented modules (docs/architecture.md:3) and documented features (docs/spec.md:3) have no corresponding files or code. Because the docs describe a surface with NO reachable implementation anywhere, the GAP-6 taxonomy maps this to Ghost Features (documented surface with no reachable implementation) — not Vocabulary Drift (the docs do not misdescribe existing code; the only code that exists, src/main.py:1, is described by no doc) and not Implicit Dependencies (there is no wiring to be undocumented — the components do not exist).

Failure consequence:
Every reader — human or agent — infers a working ingest/transform/export pipeline from docs/architecture.md:3 and docs/spec.md:3. Any attempt to use, extend, test, or document the repository hits an empty implementation: nothing imports, runs, or validates. The repository cannot serve its stated purpose, and downstream work (implementation, docs alignment, validation) is blocked until the docs↔code relationship is decided.

Confidence:
High — all five repository files were inspected, and the absence of the three declared modules is directly observed in the file listing. What would raise it further: git history showing whether the modules ever existed (would sharpen "stale docs" vs. "never implemented", though both land in the same boundary), and any user statement of intent (none exists in this fixture run).

Alternatives considered:
- Candidate 2 (entry-point contract, src/main.py:1): strong evidence, but it is a symptom of candidate 1 — the stub exists because the pipeline it should launch does not. Per the entry-point-stub rule, the documented features have NO implementation anywhere (not merely a skeletal runtime), so this folds into the product-contract defect rather than standing alone as architecture_fog.
- Candidate 3 (packaging/build contract, Zero Validation): real and observed (no manifest), but severity is capped — there is nothing to build or validate yet, so it is downstream of candidate 1.
- Candidate 4 (doc completeness): the docs are internally consistent; the defect is not inside the docs but between the docs and a missing implementation, so this loses as a primary boundary (it survives only as a secondary docs_fog contributor).

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)

The primary fog type is **product_fog**: the feature list at docs/spec.md:3 and the module list at docs/architecture.md:3 advertise deliverables (ingest, transform, export) that have no implementation anywhere — the defect is the promise, not the documentation. Applying the ghost-feature reasoning: the mismatch lives in the *product contract* (a documented deliverable with no code exists for it), not in the *documentation* (the docs are not stale descriptions of coherent existing code — no coherent code exists) and not in the *structure* (there is no architecture that cannot support the features; there is no architecture at all). `ui_fog` is excluded by the UI Fog Signals Registry decision tree: the repository contains no frontend code (no React/Vue/Angular/HTML/CSS — the tree holds one Python file), so no Tier 1/2 signals apply. A secondary, contributing fog is `docs_fog`: docs/architecture.md:3 and docs/spec.md:3 do not distinguish design intent from current state, so readers cannot tell what exists. The user-intent tie-break does not apply: this is a no-user-intent fixture run (GAP-8), so `user_implied_fog_type: unknown`.

## 7. Evidence

The diagnosis rests on five files, all inspected in full:

- `README.md:1-3` — repository title "# docs-heavy" and the instruction "See docs/."; the README offers no description of its own and no run instructions.
- `docs/architecture.md:3` — "Modules: ingestor.py, transformer.py, exporter.py." — declares three modules that do not exist as files.
- `docs/spec.md:3` — "Features: ingest, transform, export." — declares three features with no implementation.
- `docs/roadmap.md:3` — "Q3: real-time mode." — plans future capability on top of a nonexistent base.
- `src/main.py:1` — "print('hello')" — the only executable statement in the repository; unrelated to the documented pipeline.

Contrastive evidence (evidence-rules.md:3): the recursive repository listing contains exactly five files (README.md, docs/architecture.md, docs/roadmap.md, docs/spec.md, src/main.py); there is no `ingestor.py`, `transformer.py`, or `exporter.py` anywhere, and no manifest, tests, or CI configuration.

Logic trace: docs/architecture.md:3 and docs/spec.md:3 assert a module and feature surface; src/main.py:1 shows what the repository actually executes — a hello-world stub; the file listing (structural proof, evidence-rules.md:2) shows the asserted modules do not exist. A documented surface with no reachable implementation is Ghost Features, and the promise lives in the product contract, so the primary fog is product_fog. Each link in this chain is OBSERVED or directly DERIVED; nothing is inferred, and nothing is claimed about files that were not opened.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L1
    quote: "# docs-heavy"
    supports_claim: "Repository presents itself as a docs-heavy repo; the title implies a data-processing product."
  - file: README.md
    lines: L3
    quote: "See docs/."
    supports_claim: "README delegates all description to docs/, so the docs are the repository's only product contract."
  - file: docs/architecture.md
    lines: L3
    quote: "Modules: ingestor.py, transformer.py, exporter.py."
    supports_claim: "Architecture doc declares three modules as the system's shape; none of these files exists."
  - file: docs/spec.md
    lines: L3
    quote: "Features: ingest, transform, export."
    supports_claim: "Spec doc declares three features with no implementation anywhere."
  - file: docs/roadmap.md
    lines: L3
    quote: "Q3: real-time mode."
    supports_claim: "Roadmap plans future capability on top of a base that does not exist."
  - file: src/main.py
    lines: L1
    quote: "print('hello')"
    supports_claim: "The only executable code is a hello-world stub unrelated to the documented pipeline."
```

## 9. Why this boundary matters

If the documented surface keeps claiming a pipeline that does not exist (docs/architecture.md:3, docs/spec.md:3) while the only code is src/main.py:1, every downstream consumer is misled: implementers will build against a phantom contract, docs work will polish a description of nothing, and validation work has no subject. Because the boundary sits at the product contract, it silently converts every future task into guesswork about whether the docs are a spec or a lie — the single most expensive ambiguity a repository can carry, and the cheapest to resolve while the repository is still five files.

## 10. Candidate next steps

1. Decide the docs↔code relationship: confirm whether ingest/transform/export is a committed product surface or aspirational design (resolve the UNKNOWN in Section 4). If committed, treat the docs as the product contract and build to it; if aspirational, mark docs/architecture.md and docs/spec.md as design intent immediately.
2. Implement the minimal pipeline (ingestor/transformer/exporter) behind a real entry point, replacing the src/main.py:1 stub.
3. Add a manifest (pyproject.toml) plus a smoke test that exercises the pipeline contract — closes the Zero Validation gap.
4. Add a run/usage section to README.md (README.md:3 currently points at docs that do not explain execution).
5. Run a product-discovery pass to validate that ingest/transform/export matches a real user need before building.

## 11. Recommended next step

Resolve the docs↔code relationship first (candidate step 1): a one-line decision — "docs are the product contract" vs. "docs are design intent" — determines whether the next action is implementation, discovery, or doc correction. It is the smallest action with the highest leverage because it unblocks every other candidate step and eliminates the Ghost Features ambiguity at its source.

## 12. Recommended workflow

`product-implementation-workflow` (registry: skills/workflow-planner/references/workflow-registry.yaml; id `product-implementation-workflow`; allowed_execution_modes: `guided_execution`, `autonomous_execution`) with `recommended_execution_mode: guided_execution`.

Rationale: the primary fog is product_fog — a documented deliverable with no implementation — and product-implementation-workflow is the registry's workflow for product/feature problems; its discovery → opportunity-tree → to-prd chain (registry steps 2-4) first validates what to build, which is exactly the open question here (docs-as-contract vs. docs-as-intent). Closest alternatives rejected: `implementation-workflow` (generic; skips the discovery step this repository's unresolved product contract needs), `docs-implementation-workflow` (wrong direction — the code does not exist to be documented; the problem is the missing product, not missing docs), `architecture-implementation-workflow` (no architecture exists to refactor), `ui-diagnostic-workflow` (no frontend surface). Precondition gap: the workflow consumes context artifacts including user intent; this fixture run has no user-intent artifact (GAP-8), so a human must supply the docs↔code decision (Section 11) before or during step 1. `plan_only` is not offered by this workflow (registry), so `guided_execution` is the recommended mode; recommending it here does not execute it — the diagnostic No Implementation boundary is preserved.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/docs-heavy-code-light
source_intent_ref: null  # no user-intent artifact exists for this fixture run (GAP-8)
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (lines 1-3): repo title 'docs-heavy' and 'See docs/.' delegate the product contract to docs/"
  - "docs/architecture.md (line 3): declares modules ingestor.py, transformer.py, exporter.py that do not exist as files"
  - "docs/spec.md (line 3): declares features ingest, transform, export with no implementation"
  - "docs/roadmap.md (line 3): plans Q3 real-time mode on a nonexistent base"
  - "src/main.py (line 1): only executable code is print('hello'), unrelated to the documented pipeline"
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:10:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

Copy for workflow-planner (or a human owner):

"The repository at experiments/repository-sensemaking-skill-hardening-v1/corpus/docs-heavy-code-light is a five-file, docs-heavy repo whose documentation (docs/architecture.md:3, docs/spec.md:3) declares an ingest/transform/export pipeline whose modules and features have no implementation anywhere; the only executable code is src/main.py:1 (print('hello')). The sensemaking brief classifies this as product_fog with a Ghost Features weakest boundary and recommends product-implementation-workflow (guided_execution). First action: decide whether the docs are the product contract (then implement the pipeline) or design intent (then mark the docs as such). Validate the decision with a human before any implementation begins."
