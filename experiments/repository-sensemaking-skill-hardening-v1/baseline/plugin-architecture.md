# Repository Sensemaking Brief — plugin-architecture

## 1. Repository goal
`plugin-architecture` is a minimal Python demonstration of a plugin-loading
architecture: an entry point (`core/main.py`) delegates to a registry
(`core/registry.py`) that discovers and executes every `.py` file found under
`plugins/`. The entire intent is stated by `README.md:1-3` — a title
(`# plugins-app`) and one description line ("Loads plugins from plugins/.").
Two example plugins (`plugins/alpha.py`, `plugins/beta.py`) exist solely to
print a line when loaded, proving the mechanism runs.

## 2. Current shape
The repository contains exactly five files:

```
plugin-architecture/
├── README.md           (3 lines: title + one-line description)
├── core/
│   ├── main.py         (7 lines: entry point; calls load_plugins('plugins'))
│   └── registry.py     (6 lines: load_plugins() — os.listdir + exec)
└── plugins/
    ├── alpha.py        (1 line: print('alpha plugin loaded'))
    └── beta.py         (1 line: print('beta plugin loaded'))
```

Notably absent (structural proof from `ls`): no `__init__.py` anywhere (both
`core/` and `plugins/` rely on namespace-package semantics), no `tests/`
directory, no `pyproject.toml`/`setup.py`/`requirements.txt`, no plugin
manifest or interface file, and no documentation beyond the three-line README.

## 3. Strong signals
- **Clear core/plugins separation in the layout**: plugins live in their own
  `plugins/` directory apart from `core/` — the directory structure itself
  expresses the intended architecture.
- **Conventional Python entry point**: `core/main.py:6-7` guards execution
  with the standard `if __name__ == '__main__':` idiom.
- **Package-relative import**: `core/main.py:1` (`from .registry import
  load_plugins`) indicates package-aware structuring rather than
  `sys.path` manipulation.
- **Working examples**: `plugins/alpha.py:1` and `plugins/beta.py:1` each
  print when loaded — the discovery/execution mechanism demonstrably works
  for the two shipped plugins.
- **Honest README**: `README.md:1-3` describes exactly what the code does;
  there are no overstated claims or ghost features.

## 4. Missing pieces
- **No plugin contract or interface**: nothing defines what a plugin is — no
  base class, no registration function, no manifest, no expected exports.
  `core/registry.py:5-6` treats any `.py` file as a plugin and executes it.
- **No validation of loaded content**: `core/registry.py:6` runs arbitrary
  code with zero checks on what the file defines or does.
- **No error handling**: `core/registry.py:4` calls `os.listdir(directory)`
  with no existence check (an unhandled `FileNotFoundError` if `plugins/` is
  missing), and read/`exec` failures inside the loop are likewise unhandled.
- **No tests**: there is no `tests/` directory or test file anywhere, so the
  loader's behavior is entirely unverified.
- **Hardcoded relative path**: `core/main.py:4` passes `'plugins'`, resolved
  against the process working directory — an implicit dependency on where the
  app is invoked from.
- **No packaging metadata and no run instructions**: no
  `pyproject.toml`/`setup.py`, and `README.md:1-3` never says how to run the
  app (e.g. `python -m core.main` from the repo root).
- **No plugin authoring guidance**: the README's single description line is
  the only documentation a plugin author would find.

## 5. Improvement opportunities
- Document a minimal plugin contract (e.g. each plugin must expose a
  `register(registry)` callable) in the README and in a docstring at
  `core/registry.py:3`.
- Add explicit `__init__.py` files so `core/` and `plugins/` stop relying on
  namespace-package behavior.
- Add a `tests/` directory with a loader test suite (valid plugin loads,
  non-conforming file rejected, missing directory handled).
- Add a `pyproject.toml` declaring a `console_scripts` entry point so the app
  is runnable without ambient working-directory assumptions.
- Isolate per-plugin failures (try/except around `exec`) so one bad plugin
  cannot crash the whole process.

## 6. Weakest boundary
The weakest boundary is the **core↔plugin loading contract implemented in
`core/registry.py:3-6`**. `load_plugins(directory)` accepts any directory,
selects files solely by the `.py` suffix (`core/registry.py:5`), and executes
the raw contents of each match with `exec(open(os.path.join(directory,
name)).read())` (`core/registry.py:6`). Nothing verifies that a loaded file is
a plugin in any meaningful sense — no expected exports, no registration step,
no per-file error containment, no tests. The only "contract" is the file
extension, and the only documentation of the mechanism is the one-line
description in `README.md:3`. The path itself is hardcoded relative to the
invocation site (`core/main.py:4`), so the boundary is simultaneously
implicitly dependent on the working directory.

Logic trace: `core/registry.py:5` shows the loader's only selection criterion
is `name.endswith('.py')`, and `core/registry.py:6` shows its only action is
`exec()` of the file's raw text — no interface check, no registration, no
error handling; `core/main.py:4` shows the target directory is a hardcoded
relative string; and the repository contains no `tests/` directory (structural
proof from `ls`) and no plugin interface file, so nothing anywhere in the repo
automatically checks any part of this loading behavior. A mechanism whose
every step — what a plugin is, that the directory exists, that the file is
safe to run, that it behaves correctly — is unverified by construction is a
Zero Validation boundary: core logic with no automated check.

**Weakness type:** Zero Validation

## 6.5. Problem classification (fog type)
**architecture_fog** — the primary uncertainty is structural: the module
boundary between `core/` and `plugins/` exists only as a directory convention
and is unenforced, and the coupling mechanism is raw code execution
(`core/registry.py:6`) rather than any declared interface.

- Not `ui_fog`: the repository contains no frontend code at all (no
  HTML/CSS/JS/React/Vue), so per the UI Fog Signals Registry decision tree the
  answer is "Not ui_fog; evaluate other fog types". Zero Tier 1 signals apply.
- Not `product_fog`: there is no user-need ambiguity; the repo's purpose is
  fully stated by `README.md:1-3`, and there are no feature flags, analytics,
  or roadmap artifacts.
- Not `docs_fog`: the README is minimal but accurate — it matches the code
  (`core/registry.py:3-6`, `core/main.py:4`) — so documentation is thin, not
  the weakest boundary. The unvalidated loading contract is.

## 7. Evidence
The diagnosis rests on five cited observations:

1. `core/registry.py:3-6` is the entire loader: `def load_plugins(directory)`
   followed by a `for` loop that filters on `name.endswith('.py')` and
   `exec`s each file's contents. There is no interface check, no directory-
   existence check, no error handling.
2. `core/main.py:4` calls `load_plugins('plugins')` with a hardcoded relative
   path — the plugins directory is resolved against whatever directory the
   process happens to be invoked from, and nothing validates it.
3. `plugins/alpha.py:1` and `plugins/beta.py:1` are bare side-effect scripts
   (`print(...)` statements): they define and return nothing, so "plugin"
   cannot mean anything more specific than "any `.py` file in the directory".
4. `README.md:1-3` is the only documentation; it describes the loading
   behavior but defines no plugin contract, no run instructions, and no
   authoring guide.
5. Structural proof from `ls`: the repository has no `tests/` directory, no
   packaging metadata, and no plugin interface file — nothing automates a
   check of the loader's behavior.

Logic trace: `core/registry.py:4-6` shows the loader's only selection
criterion is the `.py` suffix and its only action is `exec()` of raw file
content — no verification that a file is a plugin, that the directory exists,
or that execution succeeded; `core/main.py:4` shows the directory argument is
a hardcoded relative path no file defines or validates; and the absence of any
`tests/` directory or validator script (structural proof from `ls`) means no
automated check of this logic exists anywhere in the repository. The `.py`
suffix is the sole standing between "repository file" and "executed code",
and nothing enforces even that boundary — which is precisely the Zero
Validation weakness type: core logic with no automated check.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: core/registry.py
    lines: L3-L6
    quote: "def load_plugins(directory):\n    for name in os.listdir(directory):\n        if name.endswith('.py'):\n            exec(open(os.path.join(directory, name)).read())"
    supports_claim: "The entire loader: selects files only by .py suffix and execs raw contents with no interface check, no directory-existence check, and no error handling."
  - file: core/registry.py
    lines: L5
    quote: "if name.endswith('.py'):"
    supports_claim: "The only selection criterion is the file extension — nothing verifies a file is actually a plugin."
  - file: core/main.py
    lines: L4
    quote: "load_plugins('plugins')"
    supports_claim: "The plugins directory is a hardcoded relative path resolved against the invocation working directory — an implicit dependency defined nowhere."
  - file: core/main.py
    lines: L1
    quote: "from .registry import load_plugins"
    supports_claim: "Package-relative import shows package-aware structuring (strong signal) — the coupling problem is in the loader, not the entry point style."
  - file: plugins/alpha.py
    lines: L1
    quote: "print('alpha plugin loaded')"
    supports_claim: "A shipped 'plugin' is a bare side-effect script with no registration or interface conformance — plugins are defined by nothing but location and extension."
  - file: plugins/beta.py
    lines: L1
    quote: "print('beta plugin loaded')"
    supports_claim: "Same as alpha.py: the second example plugin also exports nothing, confirming no plugin contract exists."
  - file: README.md
    lines: L1-L3
    quote: "# plugins-app\n\nLoads plugins from plugins/."
    supports_claim: "The only documentation states the loading behavior but defines no plugin contract, run instructions, or authoring guide."
```

## 9. Why this boundary matters
The architecture's entire value proposition is "drop a file into `plugins/`
and it loads" — and with `core/registry.py:5-6` as written, that promise is
enforced by nothing but the `.py` suffix. Any `.py` file dropped into the
directory is executed with full interpreter privileges: a typo'd or malicious
file runs arbitrary code with no check, a file that fails at `exec` time
crashes the whole process (no per-plugin isolation), a missing `plugins/`
directory raises an unhandled `FileNotFoundError` (`core/registry.py:4`), and
because there are no tests, a change to the loader can silently alter which
files load without any signal. For a plugin architecture, an unvalidated
load boundary is the whole product at risk: the mechanism that is supposed to
be the safe extension point is the least verified part of the system.

## 10. Candidate next steps
1. Define a minimal plugin contract (e.g. each plugin must expose a
   `register(registry)` callable) and enforce it in `core/registry.py:3-6`
   before executing — reject non-conforming files with a clear error.
2. Add validation and error containment to the loader: check the directory
   exists before `os.listdir` (`core/registry.py:4`), and wrap each file's
   read/`exec` in try/except so one bad plugin cannot kill the process.
3. Add a test suite (`tests/test_registry.py`) covering: valid plugin loads,
   non-conforming `.py` file rejected, missing directory handled gracefully.
4. Replace the hardcoded `'plugins'` path (`core/main.py:4`) with a path
   resolved relative to the package (e.g. `os.path.join(os.path.dirname(
   __file__), '..', 'plugins')`) and document invocation via
   `python -m core.main`.
5. Expand `README.md:1-3` with a plugin authoring contract section and a run
   example.

## 11. Recommended next step
Define and enforce the plugin contract at the loading boundary: specify the
one thing a plugin must export (e.g. a `register()` callable), add the
conformance check in `core/registry.py:3-6` before `exec`, and add a single
test proving a non-conforming `.py` file is rejected while
`plugins/alpha.py`/`plugins/beta.py` still load. This is the smallest change
that converts the weakest boundary from "any file is executed" into "a plugin
is validated before it runs" — and it is the prerequisite that makes every
other step (path fix, error isolation, README contract docs, wider test
suite) meaningful.

## 12. Recommended workflow
`architecture-implementation-workflow` — defined in
`skills/workflow-planner/references/workflow-registry.yaml:848` as "For
architecture/refactoring problems. Aligns domain, creates refactoring spec,
decomposes into issues, and implements via TDD." It matches this diagnosis:
the weakest boundary is structural (the core↔plugin loading contract), not
product, UI, or docs. (`implementation-workflow` at
`workflow-registry.yaml:587` is the generic fallback but is less specific to
the plugin-contract refactor shape of this fix.)

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/plugin-architecture
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "core/registry.py:3-6: load_plugins() selects files solely by .py suffix and execs raw contents — no interface check, no directory-existence check, no error handling"
  - "core/registry.py:5: the only selection criterion is name.endswith('.py')"
  - "core/main.py:4: load_plugins('plugins') hardcodes a relative path resolved against the invocation working directory"
  - "plugins/alpha.py:1 and plugins/beta.py:1: plugins are bare side-effect print scripts with no registration or interface conformance"
  - "README.md:1-3: only documentation; states the loading behavior but defines no plugin contract, run instructions, or authoring guide"
  - "repo tree (structural): no tests/ directory, no packaging metadata, no plugin interface file — nothing validates the loader"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Zero Validation
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:38:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
> Run workflow `architecture-implementation-workflow` with
> `context_artifacts = [this repository_sensemaking_brief]` for repository
> `plugin-architecture`. Scope: define and enforce a minimal plugin contract —
> require each plugin to expose a `register()` callable, validate conformance
> in `core/registry.py` (currently `core/registry.py:3-6`) before executing,
> add a test proving a non-conforming `.py` file is rejected while
> `plugins/alpha.py` and `plugins/beta.py` still load, and add error
> containment so one failing plugin cannot crash the process. Produce the
> refactoring spec and issue decomposition; do not change the public entry
> point `core.main` or the two shipped plugins' visible behavior.
