# Repository Sensemaking Brief — tiny-lib

## 1. Repository goal
`tiny-lib` is a minimal Python library whose sole purpose is to greet a user by
name: one pure function, `greet(name)`, returning `"Hello, {name}!"`, exposed as
`from greeter import greet` and covered by a single unit test. The README
(`README.md:3`) states the intent ("A tiny library that greets users.") and the
only usage example (`README.md:5`) is `from greeter import greet; greet("Ada")`.

## 2. Current shape
The repository contains exactly five files:

```
tiny-lib/
├── README.md              (5 lines: title, one-line description, usage example)
├── pyproject.toml         (3 lines: [project] name = "tiny-lib", version = "0.1.0")
├── greeter/
│   ├── __init__.py        (1 line: `from .greet import greet`)
│   └── greet.py           (2 lines: the greet() implementation)
└── tests/
    └── test_greet.py      (4 lines: one test asserting greet("Ada") == "Hello, Ada!")
```

Notably absent (structural proof from `ls`): no `[build-system]` in
`pyproject.toml`, no `setup.py`/`setup.cfg`, no `tests/__init__.py`, no
`conftest.py`, no `pytest.ini`/`[tool.pytest.ini_options]`, no CI configuration,
no LICENSE, and no docs beyond the README.

## 3. Strong signals
- **Coherent contract**: the README usage example (`README.md:5`) and the test
  assertion (`tests/test_greet.py:4`) agree exactly on behavior — the
  documentation and the code describe the same thing.
- **Conventional package layout**: `greeter/__init__.py:1` re-exports the
  public symbol, and `greeter/greet.py:1-2` is a single, pure, side-effect-free
  function.
- **A test for the core logic exists**: `tests/test_greet.py:3-4` asserts the
  exact documented output.
- **Metadata is present in the right format**: `pyproject.toml:1-3` is valid
  TOML and names the project and version.

## 4. Missing pieces
- **No build backend declaration**: `pyproject.toml:1-3` contains no
  `[build-system]` table, so how the library is built/installed is left to
  implicit tool defaults.
- **No declared test dependency**: `pyproject.toml:1-3` has no
  `[project.optional-dependencies]`, so `pytest` (required to run the only
  test) is never declared.
- **No test-runner configuration**: there is no `[tool.pytest.ini_options]`
  block and no `tests/__init__.py`, so nothing defines how `greeter` becomes
  importable when tests run.
- **No automation**: no CI config or script anywhere — nothing runs the
  existing test outside a human's ad-hoc invocation.
- **No install/test instructions**: `README.md:5` is the only usage line; the
  README never says how to install or test the library.

## 5. Improvement opportunities
- Add a `[build-system]` table (e.g. setuptools backend) to `pyproject.toml`.
- Add `[project.optional-dependencies] dev = ["pytest"]` and
  `[tool.pytest.ini_options] pythonpath = ["."]` to `pyproject.toml`.
- Add a minimal CI workflow that runs `pip install -e .` and `pytest` on a
  clean checkout.
- Expand the README with install and test sections after the usage example.
- Optionally add `tests/__init__.py` or switch the test to an installed-package
  import so the test does not depend on the working directory.

## 6. Weakest boundary
The weakest boundary is the **execution contract between the documented
library and the environment needed to build, install, and test it**. The README
promises `from greeter import greet; greet("Ada")` (`README.md:5`) and a test
asserts that exact behavior (`tests/test_greet.py:4`), but nothing in the
repository declares how that contract is made runnable: the test imports the
package with a top-level import (`tests/test_greet.py:1`) that only resolves if
the repo root happens to be on `sys.path` (i.e. the runner's working directory
or an installed package), `pytest` itself is never declared as a dependency
(`pyproject.toml:1-3`), and the build backend is never declared either. The
boundary between "documented contract" and "verifiable artifact" is enforced
only by convention and by whatever happens to be installed in the ambient
environment.

Logic trace: the import at `tests/test_greet.py:1` is a bare
`from greeter import greet` with no relative path, no `tests/__init__.py`, and
no `[tool.pytest.ini_options]` pythonpath setting in `pyproject.toml:1-3` — so
its resolution depends on an implicit path that no file defines or validates;
the tool required to run that test is not declared anywhere in
`pyproject.toml:1-3`; and the build backend is likewise implicit. All three
observations are the same defect class: the repository's behavior depends on
files, paths, and tools that are neither explicitly defined nor validated.

**Weakness type:** Implicit Dependencies

## 6.5. Problem classification (fog type)
**architecture_fog** — the primary uncertainty is structural: how the package
is built, installed, and tested (module/package boundary and its enforcement),
not what the product should do, not screen/flow design, and not missing
documentation per se.

- Not `ui_fog`: the repository contains no frontend code at all (no
  React/Vue/HTML/CSS), so per the UI Fog Signals Registry decision tree the
  answer is "Not ui_fog; evaluate other fog types".
- Not `product_fog`: the user need is unambiguous and fully specified by
  `README.md:3` and `README.md:5`.
- Not `docs_fog`: the README is thin but accurate — it matches the code
  (`greeter/greet.py:1-2`) and the test; documentation is not the weakest
  boundary. The gap is the unenforced build/test structure.

## 7. Evidence
The diagnosis rests on four cited observations:

1. `tests/test_greet.py:1` (`from greeter import greet`) — a top-level import
   with no `tests/__init__.py` and no pythonpath configuration anywhere in the
   repo, so it resolves only if the working directory happens to be on
   `sys.path` or the package is pre-installed. The path dependency is implicit.
2. `pyproject.toml:1-3` is the entirety of the packaging metadata — three
   lines, `[project]` with only `name` and `version`. There is no
   `[build-system]`, no `[project.optional-dependencies]` (so `pytest` is
   undeclared), and no `[tool.pytest.ini_options]`.
3. `README.md:5` documents usage but never installation or test invocation —
   the environment needed to honor the documented contract is never stated.
4. `greeter/greet.py:1-2` and `greeter/__init__.py:1` show the implementation
   and re-export are coherent — the source itself is not the problem; the
   boundary around it is unenforced.

Logic trace: `tests/test_greet.py:1` requires `greeter` to be importable, which
in a fresh clone depends on either CWD being the repo root (an implicit path)
or the package being installed; installing requires a build backend, which
`pyproject.toml:1-3` never declares; running the test requires `pytest`, which
`pyproject.toml:1-3` never declares. Each step of the chain "clone → install →
test" depends on an undeclared tool or path, so the repository's runnable
behavior is not reproducible from its own files. Because the README
(`README.md:5`) and test (`tests/test_greet.py:4`) are consistent with the
implementation (`greeter/greet.py:1-2`), the defect is not in the code's
content but in the implicit, unvalidated environment it depends on — which is
exactly the Implicit Dependencies weakness type.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: tests/test_greet.py
    lines: L1
    quote: 'from greeter import greet'
    supports_claim: "The only test uses a top-level import that resolves only if the repo root is on sys.path (CWD) or the package is installed — a path dependency defined nowhere in the repo."
  - file: tests/test_greet.py
    lines: L4
    quote: 'assert greet("Ada") == "Hello, Ada!"'
    supports_claim: "The test asserts the exact README-documented contract, so core logic is covered — but nothing automates running it."
  - file: pyproject.toml
    lines: L1-L3
    quote: "[project]\nname = \"tiny-lib\"\nversion = \"0.1.0\""
    supports_claim: "The entire packaging metadata is three lines: no [build-system], no [project.optional-dependencies] (pytest undeclared), no [tool.pytest.ini_options]."
  - file: greeter/greet.py
    lines: L1-L2
    quote: "def greet(name: str) -> str:\n    return f\"Hello, {name}!\""
    supports_claim: "The implementation is a single pure function matching README and test — source content is coherent; the boundary around it is not."
  - file: greeter/__init__.py
    lines: L1
    quote: 'from .greet import greet'
    supports_claim: "The package re-exports greet, so `from greeter import greet` works once the package is importable — which is exactly what is never made explicit."
  - file: README.md
    lines: L5
    quote: 'Usage: `from greeter import greet; greet("Ada")`'
    supports_claim: "README documents usage but never installation or test invocation — the environment needed to honor the contract is implicit."
```

## 9. Why this boundary matters
A fresh clone of `tiny-lib` cannot be built, installed, or tested
reproducibly: `pytest` fails with `ModuleNotFoundError: No module named
'greeter'` unless the working directory or an ad-hoc `pythonpath` setting
happens to rescue the import, and `pip install .` depends on an undeclared
build backend. The one test that protects the documented contract
(`tests/test_greet.py:4` vs `README.md:5`) is therefore not a reliable
safety net — regressions can ship unobserved, and every contributor
re-discovers the environment by trial and error. For a library whose entire
value proposition is "import and call it", an unverifiable import/test
boundary is the whole product at risk.

## 10. Candidate next steps
1. Declare the packaging and test contract in `pyproject.toml`: add
   `[build-system]`, `[project.optional-dependencies] dev = ["pytest"]`, and
   `[tool.pytest.ini_options] pythonpath = ["."]`.
2. Wire the existing test into automation: add a minimal CI workflow that runs
   `pip install -e .` and `pytest` on a clean checkout.
3. Document install/test usage in the README after the existing usage line
   (`README.md:5`).
4. Remove the CWD dependence structurally (e.g. `tests/__init__.py` plus
   installed-package import) so the test passes regardless of invocation site.
5. Run the change through `architecture-implementation-workflow` so the
   refactor is specified and reviewed rather than applied ad hoc.

## 11. Recommended next step
Extend `pyproject.toml` (currently only `pyproject.toml:1-3`) with
`[build-system]`, `[project.optional-dependencies] dev = ["pytest"]`, and
`[tool.pytest.ini_options] pythonpath = ["."]`, then verify `python -m pytest`
passes from a clean clone. This is the smallest change that converts the
implicit build/test dependencies into declared, validated ones without
touching `greet()`'s behavior — and it unblocks every other step (CI, README
instructions) on top of it.

## 12. Recommended workflow
`architecture-implementation-workflow` — defined in
`skills/workflow-planner/references/workflow-registry.yaml:848` as "For
architecture/refactoring problems. Aligns domain, creates refactoring spec,
decomposes into issues, and implements via TDD." It matches this diagnosis:
the weakest boundary is structural (package/build/test boundary), not
product, UI, or docs. (`implementation-workflow` at
`workflow-registry.yaml:587` is the generic fallback but is less specific to
the packaging-refactor shape of this fix.)

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "tests/test_greet.py:1: top-level `from greeter import greet` import relies on CWD being on sys.path; no tests/__init__.py, no pythonpath config"
  - "pyproject.toml:1-3: only [project] name/version; no [build-system], no [project.optional-dependencies] (pytest undeclared), no [tool.pytest.ini_options]"
  - "README.md:5: documents usage but not installation or test invocation"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Implicit Dependencies
weakness_type: Implicit Dependencies
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
> `tiny-lib`. Scope: make the build/test boundary explicit without changing
> `greet()` behavior — declare the build backend and dev dependencies
> (`pytest`) in `pyproject.toml`, add `[tool.pytest.ini_options]`
> `pythonpath = ["."]`, and wire a minimal CI check that installs and runs
> `pytest` from a clean clone. Produce the refactoring spec and issue
> decomposition; do not alter the public API (`greeter.greet`).
