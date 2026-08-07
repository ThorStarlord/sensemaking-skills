# Repository Sensemaking Brief

## 1. Repository goal
A minimal Python project (`partial-impl`) whose stated purpose is to implement report generation: `README.md:3` declares "Implements report generation." The repo is meant to expose a single core function, `generate_report(path)` (`core.py:1`), and a runnable entry point (`main.py:1-5`) that invokes it on a CSV path. The goal inferred from the codebase alone is: turn an input data file into a generated report via a small, testable Python module.

## 2. Current shape
- `README.md` (3 lines): title plus a one-line claim that the repo implements report generation.
- `core.py` (2 lines): single function `generate_report(path)` whose entire body raises `NotImplementedError`.
- `main.py` (5 lines): imports `generate_report` from core and calls it with `'data.csv'` under an `if __name__ == '__main__'` guard.
- `tests/test_core.py` (6 lines): one pytest that asserts `generate_report('x')` raises `NotImplementedError`.
- Absent: package metadata (no `pyproject.toml` / `setup.py`), no `docs/` directory, no data fixtures, no other modules.

## 3. Strong signals
- Clear, single public API surface: `generate_report(path)` (`core.py:1`) makes the intended contract legible in one function signature.
- Entry point wired end-to-end: `main.py:1` imports from `core` and `main.py:4` invokes the function; the module boundary between `core` and `main` is clean.
- A test file exists and follows standard pytest conventions (`tests/test_core.py:1` imports pytest; `tests/test_core.py:5` uses `pytest.raises`).
- README states the purpose concisely (`README.md:1-3`), and naming is consistent across files (`partial-impl` / `core` / `generate_report`).

## 4. Missing pieces
- The implementation itself: `core.py:2` raises `NotImplementedError('report generation not implemented yet')` — no code reads the input or produces a report.
- A definition of the input contract: `main.py:4` implies a CSV (`'data.csv'`), but no schema, columns, or parsing rules are documented anywhere.
- A definition of the output/report format: nothing specifies what "a report" is (file? stdout? rows? summary?).
- Package metadata: `from core import generate_report` (`main.py:1`) only resolves when running from the repo root; the project is not installable or runnable from elsewhere.
- Error handling for missing or invalid input files: `main.py:4` passes `'data.csv'` unconditionally and `core.py` has no handling for it.
- Behavior-level tests: `tests/test_core.py:5-6` only assert the exception, so nothing proves a report is ever generated.
- No user-intent artifact: this standalone run has no `00-user-intent.md`, so user intent is not directly available and is inferred from the repository alone.

## 5. Improvement opportunities
- Document the expected CSV schema and the report output format in `README.md` so the README's claim becomes a checkable contract instead of a slogan.
- Add a `pyproject.toml` so the package can be installed and invoked from any directory.
- Add a small sample data fixture so behavior tests are concrete rather than hypothetical.
- Once real behavior exists, remove the `NotImplementedError` assertion (`tests/test_core.py:5-6`) so the suite stops enshrining the stub.

## 6. Weakest boundary
The weakest boundary is between **documented behavior** and **actual behavior**. `README.md:3` asserts the repo "Implements report generation.", but `core.py:2` is a stub whose only statement is `raise NotImplementedError(...)`. What makes this the weakest boundary — rather than merely "unfinished work" — is that the repository is internally consistent around the absence: `main.py:4` puts the stub on the real execution path (any run terminates with the exception), and `tests/test_core.py:5-6` codify the exception as the expected outcome, so the test suite passes green while the advertised feature does not exist. Nothing in the repo signals the discrepancy; only a human reading the code can see it.

**Weakness type:** Ghost Features

Logic trace: `README.md:3` promises "Implements report generation." — a documented feature claim. `core.py:2` (`raise NotImplementedError('report generation not implemented yet')`) shows that claim has no corresponding implementation. `main.py:4` executes `generate_report('data.csv')`, proving the missing implementation is on the runtime path rather than dead code. `tests/test_core.py:5-6` asserts the exception is the expected behavior, meaning validation exists but enforces the absence, so the gap is invisible to automated checks. Documentation-promised functionality with no implementation is precisely the Ghost Features weakness type (`weakness-types.md`, type 3: "Functionality mentioned in documentation that has no corresponding implementation").

## 6.5. Problem classification (fog type)
`architecture_fog`. Rationale: the repository contains no frontend code (no React/Vue/Angular/HTML/CSS), so per the UI Fog Signals Registry decision tree (`ui-fog-signals.md`, "Does the codebase have frontend/UI code? NO → Not ui_fog") `ui_fog` is excluded. The requirement itself is explicit — `README.md:3` states the feature — so the fog is not about unclear user needs (`product_fog`) and not about missing documentation (`docs_fog`; the README exists and states the goal). The gap lives in the code: the core deliverable is an unimplemented stub (`core.py:2`). That is a code-side problem, classified as `architecture_fog` (the default when the codebase signals the problem and no other fog type fits). No user-intent artifact exists for this run, so `user_implied_fog_type` is `unknown` and no intent-vs-codebase conflict can be detected (`diagnosis_conflict: false`); the diagnosis itself is high-confidence and unambiguous, so no escalation is recommended.

## 7. Evidence
`README.md:3` declares the repo "Implements report generation." — the only statement of intent. `core.py:2` shows the corresponding implementation is a stub that raises `NotImplementedError` instead of producing anything. `main.py:4` calls `generate_report('data.csv')` on the import path, so any real execution terminates with the exception. `tests/test_core.py:5-6` asserts that exception as the expected behavior, so the suite passes without the feature existing. The directory listing (4 files, no package metadata) confirms there is no other implementation hiding elsewhere.

Logic trace: The README's feature claim (`README.md:3`) is the contract; the function's body (`core.py:2`) is the implementation of that contract; `main.py:4` is the execution path proving the contract is actually exercised; `tests/test_core.py:5-6` is the validation layer proving automated checks bless the absence. Every layer of the repo is consistent — with a feature that does not exist. Because the documented contract and the delivered behavior disagree while every automated signal says "fine", the boundary is Ghost Features, and the primary fog is architectural (the code does not deliver what the repo claims).

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Implements report generation."
    supports_claim: "README claims the repo implements report generation -- the documented feature contract."
  - file: core.py
    lines: L1-L2
    quote: "def generate_report(path):\n    raise NotImplementedError('report generation not implemented yet')"
    supports_claim: "The core function is a stub: it raises NotImplementedError and generates no report."
  - file: main.py
    lines: L1-L4
    quote: "from core import generate_report\n\nif __name__ == '__main__':\n    generate_report('data.csv')"
    supports_claim: "The entry point imports and calls generate_report on a CSV path, so any real run terminates with NotImplementedError."
  - file: tests/test_core.py
    lines: L5-L6
    quote: "with pytest.raises(NotImplementedError):\n        generate_report('x')"
    supports_claim: "The test suite codifies the stub as expected behavior, so tests pass while the advertised feature is absent."
```

## 9. Why this boundary matters
- Any user or automation that trusts `README.md:3` and runs `main.py` gets a runtime `NotImplementedError`; the trust boundary between documentation and code is broken at the very first execution.
- The green test suite manufactures false confidence: CI passes and the feature can be reported "done" without ever existing, which is how Ghost Features silently propagate into dependent code.
- Downstream sensemaking and workflow routing can misread this repo as functional; a workflow auto-invoked on this brief would otherwise plan around a feature that is not there.
- The only automated check (`tests/test_core.py:5-6`) actively enforces non-implementation, so the discrepancy is invisible to every guardrail the repo has.

## 10. Candidate next steps
1. Implement `generate_report(path)` in `core.py:2` — replace the `NotImplementedError` with minimal real logic that reads the input (CSV per `main.py:4`) and produces a report.
2. Replace the stub-codifying test at `tests/test_core.py:5-6` with behavior tests: valid input produces a report; missing input raises a clear, documented error.
3. Document the input schema and report output format in `README.md` so the README claim becomes a testable contract.
4. Add package metadata (`pyproject.toml`) and a small sample data fixture so the project is installable and tests are concrete.
5. Re-run the suite and confirm it is green on real behavior, then re-run this sensemaking skill to confirm the Ghost Feature is closed.

## 11. Recommended next step
Replace the `NotImplementedError` stub in `core.py:2` with a minimal real implementation of report generation, and add one behavior test in `tests/test_core.py` that asserts a report is produced for a valid input (replacing the exception assertion at `tests/test_core.py:5-6`). This is the smallest change that closes the README-vs-code boundary: it makes the documented contract (`README.md:3`) true and makes the test suite enforce the feature instead of its absence.

## 12. Recommended workflow
`implementation-workflow` — "Implementation Workflow (Default)" in `skills/workflow-planner/references/workflow-registry.yaml` (registry entry id `implementation-workflow`): a generic implementation workflow for architecture/code design problems that aligns domain, creates a spec, decomposes into issues, and implements via TDD. This fits a repo whose documented feature is missing from the code. (`architecture-implementation-workflow` is the closest alternative if the work is treated as a refactor, but this repo needs net-new feature code, so the generic implementation workflow is the closer match. Both IDs exist in the registry; no ID was invented.)

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-partial-impl
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
evidence:
  - "README.md (lines L3): claims the repo 'Implements report generation.'"
  - "core.py (lines L1-L2): generate_report raises NotImplementedError instead of generating a report"
  - "main.py (lines L1-L4): entry point imports and calls generate_report('data.csv'), so runs terminate with NotImplementedError"
  - "tests/test_core.py (lines L5-L6): test asserts NotImplementedError is the expected behavior"
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-06-18T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
Run the `implementation-workflow` from the workflow registry (`skills/workflow-planner/references/workflow-registry.yaml`) against the repository at `experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-partial-impl`: align domain (report generation from a CSV path), produce a spec defining the input CSV schema and the report output format, decompose into issues, and implement `core.py`'s `generate_report` via TDD — replacing the `NotImplementedError` stub (`core.py:2`) and the stub-codifying assertion (`tests/test_core.py:5-6`) with behavior tests. Execution mode: `guided_execution` with human review gates between steps.
