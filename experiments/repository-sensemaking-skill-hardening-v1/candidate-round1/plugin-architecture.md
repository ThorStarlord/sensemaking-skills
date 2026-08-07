# Repository Sensemaking Brief

## 1. Repository goal

The repository is a minimal Python "plugin host" demo: a tiny application (`plugins-app`) whose entire purpose is to load and execute Python files found in a `plugins/` directory (README.md:3 "Loads plugins from plugins/."). The implied goal is a simple extension mechanism — drop a `.py` file into `plugins/` and have it run when the app starts. This is a no-user-intent fixture run (GAP-8), so no problem statement exists; the goal is reconstructed from the code alone and `user_implied_fog_type` is `unknown`.

## 2. Current shape

Inventory (OBSERVED via full recursive listing and reading every file): `README.md` (3 lines), `core/main.py` (7 lines), `core/registry.py` (6 lines), `plugins/alpha.py` (1 line), `plugins/beta.py` (1 line). There is no manifest (no `pyproject.toml`, `setup.py`, or `requirements.txt`), no build configuration, no CI configuration, no tests, and no docs directory.

Runtime flow (each hop with file:line citations, per the Architecture Reconstruction protocol):

- **Startup path**: `core/main.py:6-7` — `if __name__ == '__main__': main()` is the only entry point; the app is launched by running this module as a script.
- **Orchestration**: `core/main.py:3-4` — `main()` calls `load_plugins('plugins')`, delegating all application behavior to the registry module.
- **Domain/core logic**: `core/registry.py:3-6` — `load_plugins(directory)` lists the directory (`os.listdir`, registry.py:4), filters names by `.endswith('.py')` (registry.py:5), and `exec()`s each file's raw text (registry.py:6). There is no other logic in the system.
- **Persistence/state**: none — no files written, no database, no caches, no queues, no environment variables; the only state is the side effects the exec'd plugin code performs (the two sample plugins print to stdout, plugins/alpha.py:1 and plugins/beta.py:1).
- **External integration**: the `plugins/` directory (filesystem) is the sole external input; it crosses the filesystem → process boundary via `exec` at registry.py:6.
- **Background work**: none.
- **Output boundary**: plugin code's stdout prints; nothing else leaves the system.
- **Where responsibility becomes unclear**: the plugin contract. What a "plugin" must be (a module with a register function? a callable? side-effect-only code?) is **UNKNOWN** — no interface file exists, no documentation beyond README.md:3, and the sample plugins (plugins/alpha.py:1, plugins/beta.py:1) only print. The host→plugin boundary assumes "any `.py` file in the directory is a plugin" but nothing defines or enforces that.

Dependency semantics: `os` is imported at core/registry.py:1 and actually used at registry.py:4 (`used`); there is no manifest, so no `declared` dependencies exist to verify. The exec'd plugins (plugins/alpha.py, plugins/beta.py) are `runtime` on the proven execution path but are not imports — they are executed by name, not imported, per registry.py:6.

## 3. Strong signals

- Minimal, readable structure: 5 files, each with a single responsibility (main.py = entry, registry.py = loading, plugins/ = payloads). OBSERVED via directory listing and file contents.
- The loader is deterministic and trivially auditable: `core/registry.py:4-6` is a loop, a filter, and an exec — 3 lines of behavior with no hidden paths.
- README accurately describes the high-level behavior ("Loads plugins from plugins/.", README.md:3) — Pass E (contradiction search) found no docs-vs-code disagreement.
- Plugin payloads are trivially simple (single print statements, plugins/alpha.py:1, plugins/beta.py:1), making the fixture easy to reason about end to end.

## 4. Missing pieces

- **No plugin contract**: nothing defines what a plugin must provide (registration function, metadata, error semantics). The "plugin" concept exists only in README.md:3 and the directory name; the expected plugin shape is UNKNOWN.
- **No validation at the load boundary**: core/registry.py:5-6 accepts any `.py` file with no contract check, no import safety, and no error containment.
- **No tests**: the repository contains zero test files; the loading logic (core/registry.py:3-6) and entry point (core/main.py:6-7) are entirely unverified (OBSERVED absence in the recursive inventory).
- **No error handling**: `os.listdir` (registry.py:4) raises if the directory is missing; `open()` and `exec()` (registry.py:6) raise on failure — all uncaught, terminating the process via main.py:3-4.
- **Fragile path assumption**: `load_plugins('plugins')` (core/main.py:4) passes a CWD-relative path, so launching from any other working directory breaks startup (DERIVED from registry.py:4 consuming the literal argument).
- **No run/install documentation**: README.md (lines 1-3) describes only the loading behavior, not how to run the app or author a plugin.

## 5. Improvement opportunities

- Document the plugin contract (what a plugin must export, how load failures are handled) in README.md.
- Add a minimal test that loads the two sample plugins and asserts their behavior, covering core/registry.py:3-6.
- Wrap `exec` in per-plugin error containment so one bad plugin cannot kill the host.
- Resolve the `plugins` path relative to the package (e.g. `Path(__file__).parent / 'plugins'`) instead of the process CWD.
- Replace raw `exec` with `importlib` + explicit registration once the contract is defined — noted as a refinement, not required for the diagnosis.

## 6. Weakest boundary

Candidate generation (2-5 candidates, scored per SKILL.md "Weakest Boundary Reasoning"):

1. **Plugin-load boundary via raw `exec` with zero validation** — `core/registry.py:4-6`, invoked from `core/main.py:3-4`.
   - evidence_strength: **strong** (direct code observation); severity: **high**; blast_radius: **high**; goal_relevance: **high**; downstream_blocking_effect: **high**; uncertainty: **low**.
2. **Implicit plugin contract** — a "plugin" is defined only by directory membership + `.py` extension (README.md:3 vs core/registry.py:5-6); the sample plugins define no interface (plugins/alpha.py:1, plugins/beta.py:1).
   - evidence_strength: **strong**; severity: **medium**; blast_radius: **medium**; goal_relevance: **high**; downstream_blocking_effect: **medium**; uncertainty: **medium**.
3. **Zero automated verification of the core loading logic** — no test files exist anywhere in the repository.
   - evidence_strength: **strong** (directory inventory); severity: **medium**; blast_radius: **medium**; goal_relevance: **high**; downstream_blocking_effect: **medium**; uncertainty: **low**.
4. **CWD-relative `plugins` path with no error handling** — `core/main.py:4` + `core/registry.py:4`.
   - evidence_strength: **strong**; severity: **medium**; blast_radius: **medium**; goal_relevance: **medium**; downstream_blocking_effect: **low**; uncertainty: **low**.
5. **Vocabulary drift on "plugins"** — README.md:3 uses the term "plugins" while the code has no plugin concept (no interface/registration), so the word implies a contract the code never defines.
   - evidence_strength: **medium**; severity: **low**; blast_radius: **low**; goal_relevance: **low**; downstream_blocking_effect: **low**; uncertainty: **medium**.

Selection: candidate 1 wins on the strongest combination of high consequence (any `.py` file executes with full host privileges, unchecked), strong direct evidence, centrality to the goal (loading IS the entire application), and downstream blocking (no real plugin can be built or verified until the load contract is defined and validated). Candidates 2-4 are consequences or sub-cases of the same boundary and lose on severity/blast radius; candidate 5 is low-severity.

```text
Boundary: host → plugin loading transition (filesystem → process) at core/registry.py:4-6, reached from core/main.py:3-4.
Observed contract: any file in the plugins/ directory whose name ends with '.py' is executed as a plugin at startup (core/registry.py:5-6); README.md:3 describes this as "Loads plugins from plugins/."
Observed violation or uncertainty: nothing validates the loading contract. There is no check that a file is actually a plugin (interface, registration, metadata), no error containment around exec, and no test anywhere in the repository. A malformed or hostile .py file is executed with full host-process privileges; a plugin that raises propagates uncaught through core/main.py:3-4 and terminates the entry point (core/main.py:6-7). The sample plugins (plugins/alpha.py:1, plugins/beta.py:1) define no interface at all, so the expected plugin shape is UNKNOWN.
Evidence: core/registry.py:6 (exec(open(os.path.join(directory, name)).read())); core/registry.py:5 (the only gate is a filename-extension check); core/main.py:4 (unconditional call, no error handling); plugins/alpha.py:1 and plugins/beta.py:1 (bare print statements, no registration); README.md:3 (only documentation of the mechanism).
Weakness type: Zero Validation
Logic trace: core/registry.py:6 executes the raw text of every .py file in the directory and core/registry.py:5 shows the only gate before execution is a filename-extension check — there is no automated check of the loading contract (no interface validation, no registration check, no error containment), and the repository inventory shows zero test files exercising core/registry.py:3-6 or core/main.py:6-7. Because the entire application's behavior is this load (core/main.py:3-4 delegates everything to it), the unvalidated exec is the core logic of the repository. Per the taxonomy mapping for exec()/dynamic loading without validation (SKILL.md, GAP-6), this classifies as Zero Validation — not Safety Gaps, which is reserved for autonomous workflows lacking human approval gates, and not Ghost Features, because the feature (loading) demonstrably runs. The consequence chain: any .py file dropped into plugins/ runs with full privileges; any exception inside exec propagates uncaught and terminates the process.
Failure consequence: arbitrary code execution at startup with no checks; a single broken plugin crashes the entire application; plugin authors receive no feedback on contract violations because no contract is checked; every future plugin change (the repo's stated purpose) is unsafe until the load contract is defined and validated.
Confidence: high — the entire logic is 6 lines of fully inspected code with no competing interpretation. What would raise it further: executing the app with a deliberately malformed plugin to observe the crash (runtime evidence); currently the crash behavior is DERIVED from the OBSERVED absence of error handling.
Alternatives considered: (2) implicit plugin contract — real, but a consequence of the same boundary (the contract is implicit precisely because nothing validates it); loses on severity and blast radius. (3) no tests — supporting evidence for (1), not a separate boundary: the missing safety net is the absence of checks, which is candidate 1's defect. (4) CWD-relative path — a sub-case of unvalidated assumptions at the same boundary; lower goal relevance. (5) vocabulary drift — low severity; README and code are behaviorally consistent, the term "plugin" is aspirational rather than contradictory.
```

**Weakness type:** Zero Validation

## 6.5. Problem classification (fog type)

primary_fog_type: **architecture_fog**. Evidence: the responsibility boundary between host and plugin is undefined and unenforced — core/registry.py:5-6 loads plugins by convention (directory + extension) with no contract, and core/registry.py:6 executes code with no lifecycle or state model, so the module structure prevents confident implementation of the repo's stated purpose. `ui_fog` is excluded by the UI Fog decision tree (no frontend code exists — the repository contains only Python). `product_fog` is excluded because README.md:3 makes no feature promise the code fails to deliver. `docs_fog` is excluded as primary because the documentation (README.md:1-3) is thin but accurate — the defect is in the unvalidated loading structure, not in stale or missing specs. A secondary docs_fog thread exists (no plugin contract documented), but it does not drive routing.

## 7. Evidence

All five repository files were opened and read in full (core/main.py, core/registry.py, plugins/alpha.py, plugins/beta.py, README.md), and the repository tree was listed recursively.

- `core/registry.py:6` — `exec(open(os.path.join(directory, name)).read())`: the loading mechanism is raw exec with no contract check; the only filter is the filename-extension test at `core/registry.py:5`. OBSERVED.
- `core/main.py:3-4` — `main()` calls `load_plugins('plugins')` unconditionally with no try/except; the entry point `core/main.py:6-7` delegates the entire application to this single call. OBSERVED.
- `plugins/alpha.py:1` and `plugins/beta.py:1` — both plugins are bare `print()` statements; neither defines an interface, registration, or metadata, so the expected plugin shape is UNKNOWN rather than documented. OBSERVED.
- `README.md:1-3` — the only documentation; states "Loads plugins from plugins/." and gives no plugin contract, run instructions, or test guidance. OBSERVED.
- Repository inventory — there is no test file, manifest, CI configuration, or docs directory anywhere in the tree (recursive listing of the repository root). OBSERVED (absence).

Logic trace: the exec at `core/registry.py:6` runs with no validation between the filesystem and the process — `core/registry.py:5` shows the only gate is a filename extension, `core/main.py:3-4` shows no error containment around the call, and the repository inventory shows no automated check (test) of this behavior exists. The absence of any contract check on the loading boundary, combined with the app having no other logic (everything routes through `load_plugins`), means the weakest boundary is the unvalidated host→plugin transition, which classifies as Zero Validation and drives the architecture_fog classification: the structure (convention-based exec loading) is what prevents confident plugin implementation.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: core/registry.py
    lines: 4-6
    quote: "    for name in os.listdir(directory):\n        if name.endswith('.py'):\n            exec(open(os.path.join(directory, name)).read())"
    supports_claim: "The only gate before executing a file is a .py filename-extension check; the file content is exec'd with no contract validation, error containment, or authorization - the unvalidated plugin-load boundary (Zero Validation)."
  - file: core/main.py
    lines: 3-7
    quote: "def main():\n    load_plugins('plugins')\n\nif __name__ == '__main__':\n    main()"
    supports_claim: "The entry point delegates the entire application to load_plugins('plugins') with no error handling; startup depends on a CWD-relative path."
  - file: plugins/alpha.py
    lines: 1
    quote: "print('alpha plugin loaded')"
    supports_claim: "The sample plugin defines no interface or registration, so the expected plugin contract is UNKNOWN."
  - file: plugins/beta.py
    lines: 1
    quote: "print('beta plugin loaded')"
    supports_claim: "Second sample plugin also defines no interface - nothing in the repo establishes what a plugin must provide."
  - file: README.md
    lines: 1-3
    quote: "# plugins-app\n\nLoads plugins from plugins/."
    supports_claim: "The only documentation describes the loading mechanism but defines no plugin contract, run instructions, or test expectations."
```

## 9. Why this boundary matters

If the load boundary stays unvalidated: (1) any `.py` file placed in `plugins/` executes arbitrary code at startup with no checks — a real reliability and security risk the moment the directory is shared or writable; (2) a single plugin that raises (SyntaxError, missing import, runtime exception) terminates the whole app because nothing catches it (core/registry.py:6 → core/main.py:3-4); (3) the repo's stated purpose — "Loads plugins from plugins/" (README.md:3) — cannot be built upon: every future plugin author must guess the contract, and every change to the loader is unverifiable because no test exists; (4) the fixture cannot serve as a trustworthy reference for plugin-architecture patterns until the boundary is defined and enforced.

## 10. Candidate next steps

1. Define and document the plugin contract (what a plugin must export, how discovery/registration works, error semantics) in README.md.
2. Add validation at the load boundary in core/registry.py (contract check before/after exec, per-plugin error isolation).
3. Add a minimal test suite covering core/registry.py:3-6 (valid plugin loads, malformed plugin is contained, missing directory handled).
4. Make plugin path resolution robust (package-relative) and handle missing-directory errors at core/main.py:4 / core/registry.py:4.
5. Replace raw `exec` with a safer mechanism (importlib + explicit registration) once the contract is defined.

## 11. Recommended next step

Define the plugin contract first (candidate 1 of Section 10): until the expected plugin shape is specified, steps 2-5 have no target to validate against. This is the smallest concrete action with the highest leverage — it converts the UNKNOWN plugin shape into a checkable specification and unblocks every other candidate. Concretely: extend README.md with a short "Plugin contract" section stating what a plugin file must provide (e.g., a `register()` callable) and how load failures are handled.

## 12. Recommended workflow

`architecture-implementation-workflow` from the canonical `skills/workflow-planner/references/workflow-registry.yaml` (registry lines 848-904) — the workflow for architecture/refactoring problems: aligns the domain (docs-aligner), creates a refactoring/architecture spec (to-prd), decomposes into issues (to-issues), prepares agent briefs (triage), and implements via TDD. Rationale: the weakest boundary is structural (unvalidated convention-based plugin loading), which matches the workflow's stated purpose (registry lines 849-851). Closest alternatives rejected: `implementation-workflow` (registry lines 587-643) is the generic default for the same problem class and loses to the more specific architecture workflow; `ui-implementation-workflow` and `ui-diagnostic-workflow` are excluded because the repository has no frontend code; `docs-implementation-workflow` is excluded because the documentation is thin but accurate — the defect is structural; `product-implementation-workflow` is excluded because no product contract is broken. Precondition before the workflow can run: none blocking — the brief, repository_state, and (fixture) user_intent are the workflow's initial inputs; the execution-mode contract is satisfied by `guided_execution`, which is one of the workflow's allowed_execution_modes (registry lines 858-861). `plan_only` is NOT in that list (GAP-7), so it must not be used. Recommending this workflow is a routing decision only — this brief performs no implementation.

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
  - "core/registry.py (lines 4-6): load_plugins exec()s every .py file in the plugins directory with no contract check, error containment, or tests"
  - "core/main.py (lines 3-7): entry point delegates the whole app to load_plugins('plugins') with no error handling"
  - "plugins/alpha.py (line 1): plugin body is a bare print statement - no interface or registration, so the plugin contract is UNKNOWN"
  - "plugins/beta.py (line 1): plugin body is a bare print statement - no interface or registration"
  - "README.md (lines 1-3): only documentation; describes loading but no plugin contract, run instructions, or tests"
  - "repository inventory (recursive listing): no test files, manifest, CI configuration, or docs directory exist"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Zero Validation
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-06-18T23:20:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

Prompt for `workflow-planner` (or another downstream skill):

> Repository sensemaking brief for `experiments/repository-sensemaking-skill-hardening-v1/corpus/plugin-architecture`. primary_fog_type: `architecture_fog`; weakest boundary: `Zero Validation` at the plugin-load boundary (`core/registry.py:4-6` — raw `exec` of every `.py` file with no contract check, no error containment, no tests). Recommended workflow: `architecture-implementation-workflow` in `guided_execution` mode. Produce a workflow orchestration plan that (1) aligns the domain around a defined plugin contract, (2) specs the refactor of `core/registry.py` from convention-based raw exec to a validated plugin-loading contract with per-plugin error isolation, (3) decomposes into issues including a test suite for the loader, and (4) preserves the existing entry-point behavior at `core/main.py:3-7`. Do not begin implementation — planning only.
