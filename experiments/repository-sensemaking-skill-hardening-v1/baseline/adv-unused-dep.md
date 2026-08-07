# Repository Sensemaking Brief — adv-unused-dep

## 1. Repository goal
The repository (`light-app`) appears to be a minimal HTTP status-check utility: a
single function `fetch(url)` that performs a `requests.get(url)` and returns the
HTTP status code. The README (`README.md:1`) names the project "light-app" and
describes it as "A light application" (`README.md:3`), and the code
(`app.py:3-4`) is exactly that — one four-line module with no other behavior.
The declared intent in `requirements.txt` is larger than the implementation:
besides `requests==2.31.0` (`requirements.txt:1`), the manifest pins
`tensorflow==2.16.0` (`requirements.txt:2`), a multi-gigabyte machine-learning
framework that no code in the repository imports or uses.

## 2. Current shape
Three files, no subdirectories:

```
adv-unused-dep/
├── README.md           (3 lines: "# light-app" + "A light application.")
├── app.py              (4 lines: import requests; def fetch(url); return requests.get(url).status_code)
└── requirements.txt    (2 lines: requests==2.31.0, tensorflow==2.16.0)
```

- `app.py:1` imports only `requests`; `app.py:3-4` is the entire implementation
  (one function, one return statement).
- `requirements.txt:1-2` declares two pinned dependencies.
- `README.md:1-3` is the title and a one-line description; there is no usage,
  install, or architecture documentation.

Absent (structural proof from `ls`): no tests, no test framework, no CI
configuration, no package metadata (`setup.py`/`pyproject.toml`), no docs
directory, and no other Python modules — `app.py` is the only source file, so
there is nowhere else `tensorflow` could be consumed.

## 3. Strong signals
- **The used dependency is declared and pinned**: `requirements.txt:1`
  (`requests==2.31.0`) exactly matches the only import in the codebase
  (`app.py:1`), so the environment contract is accurate for the code that
  actually runs.
- **Implementation is minimal and coherent**: `app.py:3-4` is a single
  side-effect-light function with no hidden state; the README's "light" claim
  (`README.md:3`) is true of the code itself.
- **Deterministic dependency pinning**: both entries in `requirements.txt:1-2`
  use exact `==` versions, so the declared environment is reproducible in
  principle.
- **Single, discoverable entry point**: `app.py:3` (`def fetch(url):`) is the
  only function, so the repository's behavior surface is fully enumerable by
  reading three files.

## 4. Missing pieces
- **A declared dependency with no implementation**: `requirements.txt:2` pins
  `tensorflow==2.16.0`, but no file imports it — `app.py:1` imports only
  `requests`, and there are no other source files. The manifest promises an
  ML-capable environment that the code never exercises.
- **No tests**: no test files or test configuration exist anywhere, so nothing
  verifies `fetch()`'s behavior or the dependency contract.
- **No usage documentation**: `README.md:1-3` never says what `fetch()` does,
  how to install, or how to run the app; the README's only statement
  (`README.md:3`) is a self-description, not a spec.
- **No automation**: no CI, no linting, no dependency-audit step — nothing
  checks that `requirements.txt` matches what the code actually imports.
- **No package metadata**: no `pyproject.toml`/`setup.py`, so installability is
  implicit.

## 5. Improvement opportunities
- Document `fetch()` usage (a single usage line would cover the whole app) in
  `README.md`.
- Add a minimal smoke test (e.g., `tests/test_app.py` asserting `fetch` returns
  an int/status code) and wire it into CI.
- Replace or supplement `requirements.txt` with `pyproject.toml` dependency
  metadata.
- Add a cheap CI check that scans imports vs. declared dependencies to prevent
  future ghost dependencies.
- Reconcile the README self-description (`README.md:3`) with the actual
  dependency footprint after cleanup.

## 6. Weakest boundary
The weakest boundary is the **declared dependency contract**:
`requirements.txt:2` declares `tensorflow==2.16.0` even though the repository's
only module (`app.py:1`) imports nothing but `requests`, and no other file
exists that could use it. The manifest is the machine-readable promise of what
the environment must contain; that promise is disconnected from the
implementation. The same boundary surfaces in prose: the README self-description
("A light application", `README.md:3`) is contradicted by the heavyweight
declared footprint, so both the docs and the manifest over-state the
repository's surface.

Logic trace: `app.py:1` shows the sole import is `requests`; `app.py:3-4` shows
the entire implementation calls only `requests.get`; the directory listing shows
`app.py` is the only Python source file, so no code path can reference
`tensorflow`; yet `requirements.txt:2` pins `tensorflow==2.16.0`. Every declared
dependency is either exercised by implementation or it is a declaration without
an implementation — and here `tensorflow` is exactly that: functionality
declared in the manifest (an ML-capable environment) with no corresponding
implementation anywhere in the codebase.

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)
**architecture_fog** — the primary uncertainty is structural: the
environment/dependency contract (`requirements.txt`) is disconnected from the
implementation, and nothing validates that declared dependencies match used
ones.

- Not `ui_fog`: the repository contains no frontend code (no React/Vue/HTML/CSS),
  so per the UI Fog Signals Registry decision tree the answer is "NO → Not
  ui_fog; evaluate other fog types".
- Not `product_fog`: there is no vague user need — the code's purpose
  (`app.py:3-4`) is unambiguous; the issue is not "what to build".
- Not `docs_fog`: the README (`README.md:1-3`) is thin, but the weakest boundary
  is the dependency manifest, not documentation; routing to a docs workflow
  would not fix a wrong `requirements.txt`.

## 7. Evidence
The diagnosis rests on four cited observations:

1. `requirements.txt:2` — `tensorflow==2.16.0` is pinned, yet no source file
   imports `tensorflow`; `app.py:1` imports only `requests`, and the repository
   contains no other `.py` files.
2. `app.py:1` and `app.py:3-4` — the import line and the entire function body
   show the implementation's complete dependency surface is `requests`.
3. `requirements.txt:1` — `requests==2.31.0` is declared and matches usage
   exactly; contrastive evidence that the manifest is accurate for the used
   dependency and only over-declares `tensorflow`.
4. `README.md:3` — "A light application." is the README's only substantive
   claim; it conflicts with the declared heavyweight footprint in
   `requirements.txt:2`.

Logic trace: the citation chain above shows the manifest is the only place
`tensorflow` appears in the repository — it is in `requirements.txt:2` and
nowhere else; because `app.py:1` plus `app.py:3-4` enumerate the entire
implementation's dependencies and the directory listing confirms there are no
other modules, the `tensorflow` declaration cannot correspond to any
implementation. A dependency that is declared but has no corresponding
implementation is a ghost in the environment contract, which is the definition
of the Ghost Features weakness type; the README contradiction (`README.md:3`
"light" vs `requirements.txt:2` tensorflow) is the same boundary surfacing in
prose.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: requirements.txt
    lines: L2
    quote: "tensorflow==2.16.0"
    supports_claim: "tensorflow is pinned in the dependency manifest but no file in the repository imports or uses it — a declared dependency with no corresponding implementation."
  - file: app.py
    lines: L1
    quote: "import requests"
    supports_claim: "The repository's only module imports only requests; the full dependency surface of the implementation is a single package."
  - file: app.py
    lines: L3-L4
    quote: "def fetch(url):\n    return requests.get(url).status_code"
    supports_claim: "The entire implementation is one function that calls only requests.get — there is no code path that could consume tensorflow."
  - file: requirements.txt
    lines: L1
    quote: "requests==2.31.0"
    supports_claim: "Contrastive evidence: the used dependency is declared and pinned accurately; only the tensorflow entry is ghost."
  - file: README.md
    lines: L3
    quote: "A light application."
    supports_claim: "The README's only substantive claim contradicts the heavyweight tensorflow declaration in requirements.txt:2 — the same over-declared surface in prose."
```

## 9. Why this boundary matters
Every environment built from `requirements.txt:1-2` installs
`tensorflow==2.16.0` — a multi-gigabyte framework — to run a four-line
`requests` wrapper. Fresh installs pay substantial time and disk for capability
nothing uses; tensorflow's platform-specific wheels are a classic source of
install failures that can block a repository whose real code needs only
`requests`; and CI minutes and image sizes inflate for every pipeline that
installs the manifest. Because nothing validates declared-vs-used dependencies,
the drift is silent and self-reinforcing: future contributors trust
`requirements.txt:2` as an accurate statement of what the app does, and the
"light application" description (`README.md:3`) becomes harder to trust as
well. For a repo whose whole value is a trivial HTTP helper, an inaccurate
environment contract is the entire surface at risk.

## 10. Candidate next steps
1. Remove `tensorflow==2.16.0` from `requirements.txt` (line 2), leaving the
   accurate `requests==2.31.0` entry.
2. Add a smoke test (e.g., `tests/test_app.py`) and a CI step that installs
   from `requirements.txt` and runs it, so the manifest is validated against
   usage.
3. Add a dependency-vs-import check to CI (e.g., a tiny script or an audit
   scan) so future ghost dependencies are caught.
4. Document `fetch()` usage and the real dependency footprint in `README.md`
   (replacing the bare `README.md:3` description).
5. Run the change through `architecture-implementation-workflow` so the
   refactoring spec and review gates apply.

## 11. Recommended next step
Delete the `tensorflow==2.16.0` line from `requirements.txt` (line 2), then
verify with `pip install -r requirements.txt` and
`python -c "import app; print(app.fetch)"` that the remaining manifest is
sufficient. This is the smallest change that makes the declared environment
contract match the implementation, and it immediately unblocks the follow-ups
(tests, CI import-scan, README) on top of it.

## 12. Recommended workflow
`architecture-implementation-workflow` — defined in
`skills/workflow-planner/references/workflow-registry.yaml:848` as "For
architecture/refactoring problems. Aligns domain, creates refactoring spec,
decomposes into issues, and implements via TDD." It matches this diagnosis: the
weakest boundary is structural (the dependency/environment contract), not
product, UI, or docs. (`implementation-workflow` at
`workflow-registry.yaml:587` is the generic fallback but is less specific to
the refactoring shape of this fix.)

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-unused-dep
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "requirements.txt:2: tensorflow==2.16.0 is pinned but never imported — declared dependency with no corresponding implementation"
  - "app.py:1: only import in the repository is requests; app.py:3-4 is the entire implementation"
  - "README.md:3: 'A light application.' contradicts the heavyweight declared footprint in requirements.txt:2"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
> Run workflow `architecture-implementation-workflow` with
> `context_artifacts = [this repository_sensemaking_brief]` for repository
> `light-app` (adv-unused-dep). Scope: make the declared dependency contract
> match the implementation without changing `fetch()` behavior — remove
> `tensorflow==2.16.0` from `requirements.txt`, keep `requests==2.31.0`, add a
> minimal smoke test that imports `app` and calls `fetch`, and add a CI step
> that installs from `requirements.txt` and runs the test. Produce the
> refactoring spec and issue decomposition; do not alter the public API
> (`app.fetch`).
