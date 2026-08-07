# Repository Sensemaking Brief

## 1. Repository goal

`plugins-app` is a minimal Python host application whose entire stated purpose is to load and execute plugins from a `plugins/` directory at runtime (README.md:3, "Loads plugins from plugins/."). The intent is a dynamic plugin architecture: drop a `.py` file into `plugins/`, run the host, and the plugin's code executes without being imported or registered by name. There is no broader product promise in the repository — no feature list, no roadmap, no user-facing behavior beyond this loading mechanism. The repository goal as evidenced is therefore: *a runnable host that discovers and executes Python plugin files from a directory*.

## 2. Current shape

The repository is a flat fixture with five files and no package metadata:

- `README.md` (3 lines) — states the single purpose: "Loads plugins from plugins/." (README.md:3). No run instructions, no plugin-authoring contract, no architecture notes.
- `core/main.py` (7 lines) — entry point. `if __name__ == '__main__': main()` at core/main.py:6-7; `main()` calls `load_plugins('plugins')` at core/main.py:4. The import at core/main.py:1 (`from .registry import load_plugins`) is a relative import, so the module must be invoked as a package module (e.g. `python -m core.main`) from a working directory where `core/` resolves and where the relative path `'plugins'` (core/main.py:4) exists.
- `core/registry.py` (6 lines) — the entire orchestration/domain layer. `load_plugins(directory)` at core/registry.py:3 iterates `os.listdir(directory)` (core/registry.py:4), filters names ending in `.py` (core/registry.py:5), and executes each file's raw source with `exec(open(os.path.join(directory, name)).read())` (core/registry.py:6).
- `plugins/alpha.py` (1 line) — `print('alpha plugin loaded')` (plugins/alpha.py:1).
- `plugins/beta.py` (1 line) — `print('beta plugin loaded')` (plugins/beta.py:1).

**Runtime flow (architecture reconstruction):**

- **Startup path**: `python -m core.main` from the repository root (core/main.py:6-7). OBSERVED constraint: the relative import at core/main.py:1 makes direct script execution (`python core/main.py`) fail; the relative path `'plugins'` at core/main.py:4 binds startup to the current working directory. Neither constraint is documented in README.md.
- **Orchestration**: `main()` → `load_plugins('plugins')` (core/main.py:3-4) → the loop in core/registry.py:4-6. There is no other logic in the system; the loader is both orchestrator and domain core.
- **Domain/core logic**: none beyond directory scanning and `exec()` (core/registry.py:4-6). There is no plugin model, no interface, no result handling.
- **Persistence/state**: none. No files are written, no database, no cache, no module-level state. The only state boundary is the filesystem read of the `plugins/` directory (core/registry.py:4) and the process working directory on which core/main.py:4 depends.
- **External integration points**: the `plugins/` directory on disk is the single external input (core/registry.py:4). Plugins enter the system as raw text executed by `exec()` (core/registry.py:6) — there is no import boundary, no function-call boundary, and no validation boundary between plugin code and host.
- **Background work**: none. No workers, jobs, or scheduled tasks.
- **Output boundary**: whatever plugin code prints (e.g. plugins/alpha.py:1, plugins/beta.py:1). The host itself produces no output and returns no status.
- **Validation**: none anywhere. No tests exist (no test directory or test files in the repository), no input validation in `load_plugins` (core/registry.py:3-6 has no existence check on `directory`, no `try/except` around `exec`), no packaging metadata (no `pyproject.toml`, `setup.py`, or manifest), and no CI configuration. `os.listdir` (core/registry.py:4) raises `FileNotFoundError` if `plugins` is absent; a syntax error inside any plugin file propagates out of `exec` (core/registry.py:6) and crashes the host.
- **Responsibility becomes unclear at**: the host↔plugin boundary. The host promises to "load plugins" but defines no contract for what a plugin is (a script? a module exposing a function? a registration call?), validates nothing about the loaded file, and provides no isolation between plugin failures and host execution (core/registry.py:6).

**Dependency semantics**: `os` is imported at core/registry.py:1 and used at core/registry.py:4 — declared (stdlib import), used, and runtime-exercised on the sole execution path. There are zero third-party or manifest-declared dependencies (no manifest exists). The `plugins/` directory is an implicit external dependency of the runtime path (core/main.py:4 → core/registry.py:4): nothing declares or validates that it exists.

## 3. Strong signals

- **Single clear purpose, honestly documented**: the README claims exactly one behavior — loading plugins from `plugins/` (README.md:3) — and the code does implement that behavior (core/registry.py:3-6). There is no README-vs-code contradiction; the documented surface is real (OBSERVED, README.md:1-3 vs core/registry.py:3-6).
- **Minimal, readable core**: the loader is six lines (core/registry.py:1-6); the entry point is seven (core/main.py:1-7). No dead code, no vendored or generated content, no framework indirection to fight.
- **Small, legible fixture**: two plugins, one line each (plugins/alpha.py:1, plugins/beta.py:1), making the loading behavior trivially traceable end to end (startup core/main.py:6-7 → loader core/registry.py:4-6 → plugin output plugins/alpha.py:1).
- **Deterministic discovery convention**: filtering by the `.py` suffix (core/registry.py:5) is a simple, predictable loading rule that a future contract could be built on.

## 4. Missing pieces

- **Any validation of the loading contract**: no test files exist anywhere in the repository; nothing checks that the directory exists, that a loaded file parses, or that the host survives a bad plugin (core/registry.py:4-6).
- **A plugin contract**: plugins are bare scripts (plugins/alpha.py:1, plugins/beta.py:1) with no registration API, no expected interface, and no documentation of what a valid plugin must provide. The word "plugin" implies a defined extension point that does not exist in code or docs.
- **Run/usage documentation**: README.md:1-3 says only "Loads plugins from plugins/." — no invocation command, no working-directory requirement (core/main.py:4), no module-invocation requirement (core/main.py:1), no packaging metadata that would let a tool discover how to run it.
- **Packaging metadata**: no `pyproject.toml`/`setup.py`/manifest, so the entry point is neither declared nor installable, and there is no declared test/build contract to validate.
- **Error handling and isolation**: no `try/except` anywhere (core/registry.py:1-6), so one malformed plugin terminates the entire host.

## 5. Improvement opportunities

- Document the invocation contract in README.md (module path, working directory, plugin file format) — cheap and removes the implicit startup assumptions (core/main.py:1,4).
- Add a minimal plugin contract (e.g. an optional `register()` hook or a documented "any code that runs" convention) so plugin authors and the loader agree on the boundary (plugins/alpha.py:1, core/registry.py:6).
- Wrap each plugin execution in error isolation so one failing plugin does not kill the host (core/registry.py:6).
- Add a smoke test (e.g. run the loader against a `plugins/` dir and assert both plugins load) — the first automated check the repository would have.
- Add packaging metadata declaring the module entry point, which would also fix the implicit CWD dependency (core/main.py:4).

## 6. Weakest boundary

Candidate boundaries generated and scored before selection:

1. **Plugin-loading boundary — `exec()` of raw plugin source with zero validation** (core/registry.py:6). Evidence strength: strong (direct code). Severity: high (a plugin with a syntax error crashes the host; any plugin executes arbitrary code with host privileges). Blast radius: high (every plugin passes through this line; it is the whole system). Goal relevance: high (it IS the repository's stated purpose, README.md:3). Downstream blocking effect: high (any hardening, contract, or testing work must start here). Uncertainty: low.
2. **Startup/entry contract — relative import + relative path with no packaging or docs** (core/main.py:1,4; README.md:1-3). Evidence strength: medium (code plus absence of manifest/docs). Severity: medium (fails fast and loudly at boot if invoked wrongly). Blast radius: high (nothing runs). Goal relevance: medium-high. Downstream blocking effect: medium. Uncertainty: medium (namespace-package semantics make `python -m core.main` from the root likely to work, but nothing documents or verifies it; I did not execute the repo).
3. **Plugin contract mismatch — "plugins" have no defined interface** (plugins/alpha.py:1, plugins/beta.py:1 vs core/registry.py:6). Evidence strength: medium. Severity: medium. Blast radius: medium. Goal relevance: high. Downstream blocking: medium. Uncertainty: low. Loses because it is a symptom of candidate 1: the missing contract IS the missing validation, not a separate boundary.
4. **README documentation gap** (README.md:1-3). Evidence strength: medium (absence). Severity: low. Blast radius: low. Goal relevance: medium. Downstream blocking: low. Uncertainty: low. Loses on all consequence axes; the README does not misdescribe existing code (no Vocabulary Drift), it is merely thin.

Selection: candidate 1 dominates on evidence strength, severity, blast radius, goal centrality, and downstream blocking, with the lowest uncertainty.

```text
Boundary: host ↔ plugin loading boundary — every .py file in plugins/ is executed
          as raw source with no validation, isolation, or contract check
          (core/registry.py:6).
Observed contract: README.md:3 promises "Loads plugins from plugins/." — the
          documented contract is that files in plugins/ are loaded.
Observed violation or uncertainty: the loading mechanism (exec of raw source,
          core/registry.py:6) validates nothing: no existence check on the
          directory (core/registry.py:4), no syntax/parse guard, no exception
          isolation, no check of what a plugin exposes, no tests anywhere. A
          single malformed plugin terminates the whole host; a plugin can do
          anything the host process can do.
Evidence: core/registry.py:4-6 (os.listdir → .py filter → exec(open(...).read()));
          core/main.py:4 (the only call site); plugins/alpha.py:1 and
          plugins/beta.py:1 (plugins are bare scripts, no interface);
          README.md:3 (the documented surface, which IS implemented — so this
          is not a Ghost Feature; the defect is the unvalidated load).
Weakness type: Zero Validation
Logic trace: README.md:3 documents "Loads plugins from plugins/." and
          core/registry.py:3-6 does implement directory discovery and
          execution, so the documented surface has a reachable implementation
          (not Ghost Features). The defect is that the loading contract is
          enforced by nothing: core/registry.py:6 runs exec() over each .py
          file's contents with no automated check of the loading contract —
          no tests, no try/except, no directory guard (core/registry.py:4-6),
          no declared packaging/test metadata. Under the GAP-6 taxonomy
          mapping, dynamic loading via exec() without validation classifies
          as Zero Validation (no automated check on the loading contract), not
          Safety Gaps (reserved for autonomous workflows lacking human
          approval gates) and not Ghost Features (the feature exists). The
          boundary is the weakest because every plugin, including a future
          third-party one, crosses it unexamined, and the whole host depends
          on it (core/main.py:4 → core/registry.py:6).
Failure consequence: any plugin with a syntax error, an exception, or hostile
          code crashes or compromises the entire host; there is no way to know
          whether the advertised plugin loading works except by manual
          execution, since nothing verifies the loading contract.
Confidence: high. Evidence is direct code (core/registry.py:4-6) plus total
          absence of tests/metadata (verified by full-tree inspection — the
          repository contains exactly five files). What would raise it
          further: executing the host to demonstrate the crash on a malformed
          plugin (not done — read-only analysis).
Alternatives considered: (a) startup/entry contract (core/main.py:1,4) — real
          but medium evidence and it fails loudly at boot rather than
          corrupting behavior, so it lost on severity and evidence strength;
          (b) plugin contract mismatch (plugins/alpha.py:1 vs core/registry.py:6)
          — subsumed by the Zero Validation finding, the missing interface is
          the missing validation; (c) README documentation gap (README.md:1-3)
          — the README does not misdescribe code, it is merely thin, so it has
          no violation and lost on every consequence axis.
```

**Weakness type:** Zero Validation

## 6.5. Problem classification (fog type)

**architecture_fog.** The repository has no frontend surface (no React/Vue/Angular/HTML/CSS anywhere — the tree is two Python modules and two one-line plugin scripts), so the UI Fog Signals Registry decision tree resolves to "Not ui_fog" immediately. The README does not misdescribe existing code: its one claim (README.md:3) is implemented (core/registry.py:3-6), so there is no docs_fog defect and no product_fog promise violation — nothing is advertised that does not exist. The actual defect is structural: the responsibility boundary between host and plugin is unenforced (core/registry.py:6 executes arbitrary file contents), the module structure leaves the loading contract unvalidated and the startup contract implicit (core/main.py:1,4), and the system's shape prevents confident implementation of any plugin feature — exactly the architecture_fog signals (implicit dependency chains, unwired contracts, structural mismatch between entry point and flow). Per the entry-point rule: the entry point (core/main.py:6-7) runs but forms an incomplete, unvalidated system — a structural defect, not a missing deliverable. Secondary fog: none material; the thin README (README.md:1-3) is a contributing minor docs gap, not a separate fog type.

## 7. Evidence

The core evidence for the weakest boundary is the loader itself: core/registry.py:4-6 shows `os.listdir(directory)` (no existence guard), a `.py` suffix filter (core/registry.py:5), and `exec(open(os.path.join(directory, name)).read())` (core/registry.py:6) — raw source execution with no validation, no exception handling, and no contract check. The single call site is core/main.py:4 (`load_plugins('plugins')`), reached from the entry point at core/main.py:6-7 via a relative import (core/main.py:1) and a relative path, neither documented. The plugins themselves are one-line scripts (plugins/alpha.py:1, plugins/beta.py:1) with no interface, confirming the loader is the entire contract. README.md:3 documents the surface that the code does implement, which is why this is Zero Validation on an existing feature rather than Ghost Features. Structural absence evidence: the full repository inventory (five files total, no test files, no manifest, no CI config) was verified by directory listing; no test or packaging file exists to cite because none exists.

**Logic trace:** README.md:3 states the repository's only promise — "Loads plugins from plugins/." — and core/registry.py:3-6 does implement directory discovery plus execution, so the documented feature is real and reachable (excluding Ghost Features). The failure is that nothing checks the loading contract: the only loading path (core/main.py:4 → core/registry.py:4-6) performs an unguarded `os.listdir` and an unguarded `exec()` of arbitrary file contents, and the repository contains no tests or packaging metadata to catch a broken plugin or a broken invocation. Because dynamic loading via `exec()` without validation is mapped by the taxonomy to Zero Validation (not Safety Gaps), and because the defect sits in the structure of the system (unenforced host↔plugin boundary, implicit startup contract at core/main.py:1,4) rather than in its documentation or product promises, the weakest boundary is Zero Validation at core/registry.py:6 and the primary fog type is architecture_fog.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: core/registry.py
    lines: L3-L6
    quote: "def load_plugins(directory):\n    for name in os.listdir(directory):\n        if name.endswith('.py'):\n            exec(open(os.path.join(directory, name)).read())"
    supports_claim: "The loader executes every .py file in the directory via exec() with no validation, no directory guard, and no exception isolation — the Zero Validation boundary."
  - file: core/main.py
    lines: L1-L7
    quote: "from .registry import load_plugins\n\ndef main():\n    load_plugins('plugins')\n\nif __name__ == '__main__':\n    main()"
    supports_claim: "The entry point invokes the loader with a relative path via a relative import; startup depends on module invocation and on the working directory."
  - file: README.md
    lines: L1-L3
    quote: "# plugins-app\n\nLoads plugins from plugins/."
    supports_claim: "The documented surface is implemented (so not Ghost Features) but contains no run instructions, no plugin contract, and no validation claims."
  - file: plugins/alpha.py
    lines: L1
    quote: "print('alpha plugin loaded')"
    supports_claim: "Plugins are bare scripts with no registration API or interface — the plugin contract is entirely implicit."
  - file: plugins/beta.py
    lines: L1
    quote: "print('beta plugin loaded')"
    supports_claim: "Second plugin confirms the pattern: plugin code is free-form script text executed by the host."
```

## 9. Why this boundary matters

If the host↔plugin boundary stays unvalidated, the advertised capability — "Loads plugins from plugins/." (README.md:3) — is only one malformed plugin away from failing entirely: a syntax error in any plugin crashes the host at core/registry.py:6, and there is no test to catch it. Because the repository's entire value is this loading mechanism, the boundary is not a corner of the system but the system itself. Any downstream work — adding a real plugin API, packaging the app, letting third parties contribute plugins — is blocked by it, because no one can state what a valid plugin is or prove the host survives one. The boundary also silently grants every plugin full code-execution privilege in the host process, with no contract and no verification, which compounds the risk of every future plugin.

## 10. Candidate next steps

1. Add a smoke test that runs `load_plugins` against a fixture `plugins/` directory (valid + deliberately broken plugin) and asserts the valid plugin loads and the host survives the broken one — the first automated check on the loading contract (core/registry.py:6).
2. Define and document the plugin contract (what a plugin is allowed to be, e.g. plain script vs. `register()` hook) in README.md and enforce it in the loader (plugins/alpha.py:1, core/registry.py:6).
3. Wrap each plugin's execution in error isolation (`try/except` per file, continue on failure) so one bad plugin cannot terminate the host (core/registry.py:6).
4. Document and validate the startup contract: module invocation (core/main.py:1), working-directory requirement (core/main.py:4), and add packaging metadata declaring the entry point.
5. Expand README.md beyond the one-liner (README.md:3) into run instructions and a plugin-authoring section.

## 11. Recommended next step

Add the smoke test (candidate 1) and make it the repository's first automated check of the loading contract. It is the smallest action with the highest leverage: it converts the currently unproven claim "Loads plugins from plugins/." (README.md:3) into a verified behavior, it exercises the exact boundary where the weakness lives (core/registry.py:6), and it gives every later step (contract, isolation, packaging) a regression net. Concretely: a `tests/` directory with a test invoking `load_plugins` on a temporary directory containing one valid and one malformed `.py` file, asserting the valid plugin executed and the malformed one was reported rather than crashing the host.

## 12. Recommended workflow

**architecture-implementation-workflow** (from `skills/workflow-planner/references/workflow-registry.yaml`) with execution mode **guided_execution** (one of that workflow's `allowed_execution_modes`: `guided_execution`, `autonomous_execution` — `plan_only` is not offered for this workflow). This workflow fits because the diagnosed problem is architectural: the repository's plugin-host boundary is structurally unenforced and needs a refactoring spec (module boundaries, plugin contract, validation) before implementation, and architecture-implementation-workflow's chain — docs-aligner → to-prd → to-issues → triage → tdd (registry steps 1-5) — is exactly the spec-driven refactoring path the fog classification calls for. Alternatives considered and rejected: `ui-implementation-workflow` (no frontend surface exists), `product-implementation-workflow` (no broken product promise — the README's one feature is implemented), `docs-implementation-workflow` (the README does not misdescribe code; fixing docs alone leaves the core defect untouched), and `implementation-workflow` (the generic default; the architecture-specific workflow is the closer match). Precondition before the workflow can run: a user intent / scope statement is required (`context_artifacts` is a required initial input), which this standalone fixture run does not provide — the recommended next step (Section 11) can proceed regardless, and the workflow should be started once intent exists.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/plugin-architecture
source_intent_ref: standalone fixture run (no user-intent artifact exists in this corpus; GAP-8 no-intent defaults applied)
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "core/registry.py (lines L3-L6): load_plugins executes every .py file via exec() with no validation, isolation, or directory guard"
  - "core/main.py (lines L1-L7): entry point calls load_plugins('plugins') via relative import; startup contract (module invocation, CWD) is implicit and undocumented"
  - "README.md (lines L1-L3): only document claims 'Loads plugins from plugins/.' — implemented, so not Ghost Features; no run instructions or plugin contract"
  - "plugins/alpha.py (line L1): plugin is a bare one-line script with no interface"
  - "plugins/beta.py (line L1): second plugin confirms free-form script pattern"
  - "repository inventory (5 files, no tests, no manifest, no CI): no automated check of the loading contract exists anywhere"
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: "Zero Validation — host↔plugin loading boundary (core/registry.py:6): exec() of arbitrary .py contents with no automated check of the loading contract"
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:06:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

```text
Goal: Harden the plugin-loading boundary of plugins-app
(experiments/repository-sensemaking-skill-hardening-v1/corpus/plugin-architecture).

Diagnosis (repository_sensemaking_brief, plugin-architecture.md):
- Weakest boundary: Zero Validation at core/registry.py:6 — load_plugins()
  exec()s every .py file under plugins/ with no directory guard, no syntax
  check, no exception isolation, and no plugin contract. One malformed plugin
  crashes the host; the loading contract has zero automated checks (no tests,
  no packaging metadata anywhere in the repo).
- Primary fog type: architecture_fog.
- Recommended workflow: architecture-implementation-workflow (guided_execution).

First step to implement (smallest, highest leverage):
- Add a smoke test (tests/ directory): invoke load_plugins() on a temporary
  directory containing one valid .py plugin and one malformed .py plugin;
  assert the valid plugin's code executed and that the malformed plugin is
  handled without terminating the host. This is the first automated check of
  the loading contract and the regression net for everything after.

Then, in order:
1. Define and document the plugin contract (what a valid plugin is) in README.md.
2. Add per-plugin error isolation in core/registry.py:6 (try/except, continue
   on failure, report the failing file).
3. Document and validate the startup contract: module invocation
   (core/main.py:1 relative import), working-directory requirement
   (core/main.py:4 relative path 'plugins'), and packaging metadata declaring
   the entry point.

Constraints: do not change the documented surface (README.md:3 "Loads plugins
from plugins/." must stay true); keep the fixture's minimal shape; run the new
tests and the existing behavior check before completing.
```
