# Repository Sensemaking Brief

## 1. Repository goal
`tiny-lib` is a minimal Python library whose only purpose is to greet a user by name: "A tiny library that greets users." (README.md:3) with the documented usage `from greeter import greet; greet("Ada")` (README.md:5). This is a fixture/standalone run with no user problem statement (GAP-8 no-user-intent run), so `user_implied_fog_type` is `unknown` and there is no stated intent to conflict with (`diagnosis_conflict: false`).

## 2. Current shape
Root inventory (all files actually opened, 5 total): `README.md` (5 lines), `pyproject.toml` (3 lines), `greeter/__init__.py` (1 line), `greeter/greet.py` (2 lines), `tests/test_greet.py` (4 lines). Absent from the inventory: setup.py, setup.cfg, CI configuration, container/deployment configuration, any documentation beyond the README, LICENSE.

Runtime flow (architecture reconstruction, not just inventory):
- **Startup**: there is nothing to start — this is a library, not an application. The only entry point is the documented import `from greeter import greet` (README.md:5), which is also the import exercised by the sole test (tests/test_greet.py:1).
- **Orchestration**: none. No CLI, no server bootstrap, no route registration, no workers; pyproject.toml declares no `[project.scripts]` or entry points.
- **Domain/core logic**: `greet(name: str) -> str` returns `f"Hello, {name}!"` (greeter/greet.py:1-2); the package re-exports it at greeter/__init__.py:1.
- **Persistence/state**: none — the function is pure; no files, databases, caches, queues, or environment variables are read or written.
- **External integration points**: none.
- **Output boundary**: a string returned to the caller.
- **Validation**: exactly one automated check — tests/test_greet.py:3-4 asserts `greet("Ada") == "Hello, Ada!"` — covering only the happy path.
- **Where responsibility becomes unclear**: the packaging/deliverable boundary. pyproject.toml:1-3 declares a project (`name = "tiny-lib"`, `version = "0.1.0"`) but the entire file contains no `[build-system]` table, and no setup.py/setup.cfg exists anywhere. Dependency semantics: `pyproject.toml` is `declared` project metadata but is not `used` by any build tooling that could produce a distribution — there is no declared build backend at all.

## 3. Strong signals
- Core function is implemented, type-annotated, and trivially correct (greeter/greet.py:1-2).
- Package entry point is a clean one-line re-export (greeter/__init__.py:1).
- README usage example matches the actual API exactly — Pass E contrastive check found **no** README-vs-code disagreement (README.md:5 vs greeter/greet.py:1-2 + greeter/__init__.py:1).
- A test exists for the core behavior (tests/test_greet.py:3-4) and, with the repo root importable, asserts the documented output.

## 4. Missing pieces
- `[build-system]` and any packaging configuration in pyproject.toml — the file is only the `[project]` name/version block (pyproject.toml:1-3).
- setup.py / setup.cfg — absent from the root inventory.
- Any mechanism that makes `greeter` importable outside the repo checkout (installed package, repo-root conftest.py, or a documented `python -m pytest` invocation) — tests/test_greet.py:1 imports by top-level name.
- CI, linting, type-checking configuration, LICENSE, and any documentation beyond the 5-line README.

## 5. Improvement opportunities
- Add a `[build-system]` table plus `[tool.setuptools] packages = ["greeter"]` (or adopt a src/ layout) so the library is pip-installable.
- Add a repo-root conftest.py or README test instructions so test invocation is deterministic regardless of how pytest is launched.
- Expand tests beyond the single happy path (empty name, Unicode names, non-str input).
- Add minimal CI that runs pytest plus a build/install smoke check so the packaging boundary is continuously validated.
- Add install/usage instructions to README once packaging is complete.

## 6. Weakest boundary

Candidate generation and scoring (4 candidates, per SKILL.md "Weakest Boundary Reasoning"):

| # | Boundary (file:line) | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|---|
| C1 | Packaging/deliverable: pyproject.toml:1-3 declares a project but no `[build-system]`/setup.py exists | strong | high | medium | high | high | low–medium |
| C2 | Test import contract: tests/test_greet.py:1 `from greeter import greet` requires repo root on sys.path | strong | medium | medium | medium | medium | medium |
| C3 | README usage example correctness (README.md:5) | strong (shows NO violation) | — | — | high | — | low |
| C4 | No automated checks for the documented contract (no CI/lint/type checks) | strong (absence) | low–medium | medium | medium | low | low |

Selection: **C1**.

```text
Boundary:
  The packaging/deliverable boundary — what the repository claims to be (a
  library: README.md:3) and declares as a project (pyproject.toml:1-3) versus
  what standard tooling can actually build or install.
Observed contract:
  README.md:3 documents the deliverable as "A tiny library"; pyproject.toml:1-3
  declares the project metadata (name = "tiny-lib", version = "0.1.0").
Observed violation or uncertainty:
  The declared project has no reachable build/install path. pyproject.toml
  (all 3 lines) contains only the [project] name/version block — no
  [build-system] table — and the root inventory contains no setup.py or
  setup.cfg. PEP 517/518 build frontends require a declared build backend;
  with neither [build-system] nor legacy setup.py present, `pip install .` /
  `python -m build` cannot produce an installable artifact (DERIVED from the
  observed file contents and PEP 517 semantics; direct execution was blocked
  in this read-only environment, so this remains DERIVED, not OBSERVED).
Evidence:
  pyproject.toml:1-3 (full file: no [build-system]); README.md:3; root
  inventory of exactly 5 files with no setup.py/setup.cfg/CI config.
Weakness type:
  Ghost Features
Logic trace:
  README.md:3 documents the deliverable as "A tiny library" and README.md:5
  shows it consumed via `from greeter import greet` → a library is a
  deliverable that must be importable/installable outside its checkout → the
  distribution contract is declared by pyproject.toml:1-3 → pyproject.toml is
  only 3 lines long and contains no [build-system] table, and the root
  inventory shows no setup.py or setup.cfg → no build backend is declared or
  present anywhere → standard tooling cannot build or install the project →
  the documented "library" deliverable has no reachable implementation. Per
  the SKILL.md GAP-6 taxonomy mapping, a documented/declared surface with no
  reachable implementation is `Ghost Features` (the packaging structure
  cannot support the documented deliverable).
Failure consequence:
  Consumers cannot install the library; the sole test can only run from the
  repo checkout with the root directory importable; any CI or publishing
  attempt fails at build time; the "library" behaves as documentation-only.
Confidence:
  medium-high. What would raise it: executing `pip install --dry-run .` /
  `python -m build` in a sandboxed copy to observe the build failure directly
  (not possible in this environment — every execution command was blocked);
  the claim rests on OBSERVED file contents plus DERIVED PEP 517 behavior.
Alternatives considered:
  C2 (test import contract, tests/test_greet.py:1) lost because it is
  downstream of C1 — the import depends on repo-root-on-sys.path precisely
  because nothing is installable — and its failure mode is invocation-
  dependent (bare `pytest` vs `python -m pytest` import-path behavior is
  INFERRED and could not be executed here). C3 lost on evidence: the README
  example matches the implementation exactly (greeter/greet.py:1-2,
  greeter/__init__.py:1), so no violation exists. C4 lost because it is a
  contributor/symptom rather than a sharp boundary; for a 5-file repo the
  concrete blocker is the packaging gap.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)
`primary_fog_type`: **architecture_fog**.

- **ui_fog ruled out**: no frontend code exists — the inventory contains no HTML/CSS/JS/TS files — so the UI Fog Signals Registry decision tree exits at step 1 (NO frontend → not ui_fog). No Tier 1/2 UI signals can be cited.
- **product_fog ruled out**: the goal is crisply stated (README.md:3-5) and the one promised feature is fully implemented and working; no roadmap/feature promises are absent.
- **docs_fog ruled out**: the README accurately describes the code (Pass E found no README-vs-code disagreement); the defect is not in the documentation.
- **architecture_fog selected**: the defects are structural — an incomplete packaging surface (pyproject.toml:1-3 without `[build-system]`) and an implicit import contract (tests/test_greet.py:1). Per the skill's ghost-feature reasoning, the "library" deliverable exists only partially because the *packaging structure* cannot support it → architecture_fog candidate. No user intent exists to tie-break with (GAP-8); no escalation needed (`escalation_recommended: false`).

## 7. Evidence
All evidence is OBSERVED from files opened in full: `pyproject.toml:1` (the entire 3-line file: `[project]` name/version only, no `[build-system]`), `README.md:3` (deliverable claim), `greeter/greet.py:1` (core implementation), `greeter/__init__.py:1` (re-export), `tests/test_greet.py:1` and `tests/test_greet.py:3` (sole test, top-level import, happy-path assertion). The root inventory of exactly 5 files establishes the absence of setup.py, setup.cfg, CI, and any other configuration.

**Logic trace:** pyproject.toml:1-3 declares `name = "tiny-lib"` and `version = "0.1.0"` with no `[build-system]` table (the whole file is those 3 lines, so the absence is exhaustive), and the root inventory shows no setup.py or setup.cfg → no build backend exists → standard PEP 517 tooling cannot build or install the project → the "A tiny library" deliverable (README.md:3) has no reachable implementation → the weakest boundary is the packaging/deliverable contract, classified `Ghost Features` (declared/documented surface with no reachable implementation). Because the boundary is structural — packaging/module structure, not documentation, not product promises, not UI — the primary fog is `architecture_fog`. The one piece of INFERRED (not OBSERVED) reasoning in this brief is that a bare `pytest` invocation from the repo root fails to import `greeter` (tests/test_greet.py:1) due to pytest's default import mode; it could not be executed in this read-only environment and is labeled as inference accordingly.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: pyproject.toml
    lines: L1-L3
    quote: "[project]\nname = \"tiny-lib\"\nversion = \"0.1.0\""
    supports_claim: "Project declared with name/version only; the 3-line file contains no [build-system] table."
  - file: README.md
    lines: L3
    quote: "A tiny library that greets users."
    supports_claim: "Documented deliverable is a library (an installable/importable unit)."
  - file: README.md
    lines: L5
    quote: "Usage: `from greeter import greet; greet(\"Ada\")`"
    supports_claim: "Documented consumption contract imports by top-level package name."
  - file: greeter/greet.py
    lines: L1-L2
    quote: "def greet(name: str) -> str:\n    return f\"Hello, {name}!\""
    supports_claim: "Core implementation exists and returns the documented greeting."
  - file: greeter/__init__.py
    lines: L1
    quote: "from .greet import greet"
    supports_claim: "Package re-exports greet, making the README import resolvable only when the repo root is importable."
  - file: tests/test_greet.py
    lines: L1
    quote: "from greeter import greet"
    supports_claim: "The sole test relies on the repo root being on sys.path (no installed package, no conftest.py)."
  - file: tests/test_greet.py
    lines: L3-L4
    quote: "def test_greet():\n    assert greet(\"Ada\") == \"Hello, Ada!\""
    supports_claim: "The only automated check covers the single happy path."
```

## 9. Why this boundary matters
If the packaging boundary stays broken: consumers cannot `pip install` the library, so the documented deliverable (README.md:3) is unreachable; the only test (tests/test_greet.py:1) keeps depending on the checkout directory being importable, so standard test setups (installed-package mode, CI containers, bare `pytest` from the root — INFERRED for the last) can fail with `ModuleNotFoundError` while the repo "looks" green; and every future change (a second module, a dependency, publishing) fails at build time. Any downstream implementation work routed from this brief would start from a false baseline: the code works, but the thing the repo claims to be does not exist as a shippable artifact.

## 10. Candidate next steps
1. **Complete the packaging contract**: add `[build-system]` (setuptools backend) and package discovery (`packages = ["greeter"]`) to pyproject.toml; verify `pip install -e .` and `python -m build` succeed.
2. **Make test invocation deterministic**: add a repo-root conftest.py (or document `python -m pytest` in the README) and verify the suite runs in both bare and installed modes.
3. **Add minimal CI** (e.g., GitHub Actions) running pytest plus a build/install smoke check so the packaging boundary is continuously validated.
4. **Expand tests** beyond the happy path (empty name, Unicode names, non-str input).
5. **Update README** with install and test instructions once packaging works.

## 11. Recommended next step
Step 1 — add `[build-system]` and packaging configuration to pyproject.toml and verify the project builds and installs. It is the smallest concrete action at the weakest boundary (it makes the documented "library" real), and it unblocks step 2 (deterministic test invocation via an installed package).

## 12. Recommended workflow
`architecture-implementation-workflow` (ID verified against `skills/workflow-planner/references/workflow-registry.yaml`), with `recommended_execution_mode: guided_execution` — one of that workflow's `allowed_execution_modes` (guided_execution, autonomous_execution); `plan_only` is NOT offered for this workflow and is therefore not used. Rationale: `primary_fog_type` is `architecture_fog` and the weakest boundary is structural (packaging/module structure), which routes to spec-driven refactoring per SKILL.md Section 7. Closest alternatives rejected: `fast-path-workflow` (a chaining wrapper that would re-run sensemaking + planning this brief already completes), `docs-contract-reconciliation` (targets docs-vs-code drift; the defect is structural, not documentary), `implementation-workflow` (generic default; the architecture-specific workflow fits the structural boundary better). Preconditions: none missing — the brief supplies the goal and boundary; the workflow's docs-aligner step consumes this brief as its context artifact.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/tiny-lib
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (L3): deliverable documented as 'A tiny library'"
  - "README.md (L5): usage example imports by top-level package name"
  - "pyproject.toml (L1-L3): project declares only name/version; no [build-system]"
  - "greeter/greet.py (L1-L2): core greet() implemented"
  - "greeter/__init__.py (L1): re-exports greet"
  - "tests/test_greet.py (L1, L3-L4): sole test imports greeter by top-level name; happy-path assertion only"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:06:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
"Run `architecture-implementation-workflow` (mode: guided_execution) against the tiny-lib repository (`experiments/repository-sensemaking-skill-hardening-v1/corpus/tiny-lib`) using the `repository_sensemaking_brief` (primary_fog_type: architecture_fog; weakest boundary: Ghost Features at the packaging/deliverable boundary). Scope: make the declared 'tiny library' actually buildable and installable — add a `[build-system]` table and packaging configuration to pyproject.toml (currently only `[project]` name/version at pyproject.toml:1-3), verify `pip install -e .` and `python -m build` succeed, and make the test import at tests/test_greet.py:1 deterministic (install the package or add a repo-root conftest.py) so the suite runs regardless of invocation. Do not change the `greet()` API (greeter/greet.py:1-2); the README usage at README.md:5 must keep working. Add regression coverage for the build/install step (e.g., a CI smoke check)."
