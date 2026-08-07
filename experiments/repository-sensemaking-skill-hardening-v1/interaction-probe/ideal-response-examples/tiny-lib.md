# Ideal response prototype — tiny-lib

**What this is:** a 5-file Python library with one function: `greet(name)`
returns `"Hello, {name}!"` (greeter/greet.py:1-2), re-exported from the package
(greeter/__init__.py:1), with one passing-style test (tests/test_greet.py:1-4).

**How it works:** import the package, call `greet("Ada")`, get a greeting.
There is no state, no I/O, no CLI — just the one pure function.

**The one important weakness:** the repository cannot be built or tested
reproducibly. `pyproject.toml:1-3` declares only name/version — no build
backend, no pytest dependency, no test path config — so `pip install .` and
`pytest` both depend on unstated environment luck. Evidence: the full
pyproject.toml is three lines and omits `[build-system]` and
`[tool.pytest.ini_options]`; the test's top-level import
(tests/test_greet.py:1) resolves only if the CWD happens to be on sys.path.

**Alternatives considered:** (1) missing input validation on `greet()`
(rejected — the function is a pure example, not a security surface);
(2) no CI (rejected — CI absence is a symptom of the undeclared build/test
boundary, not the boundary itself).

**Confidence: high** — the entire repo is 5 files; all facts are directly
observed. Would be raised further by actually running `pip install .` and
`pytest` in a clean clone.

**Recommended next step:** one small packaging commit: declare the build
backend, declare pytest as a dev dependency, add `pythonpath = ["."]` under
`[tool.pytest.ini_options]`. No API change.

**Ask before:** publishing the package or renaming the public API.
