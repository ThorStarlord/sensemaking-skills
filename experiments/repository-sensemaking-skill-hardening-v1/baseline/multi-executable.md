# Repository Sensemaking Brief: multi-exec (multi-executable fixture)

## 1. Repository goal
A small Python project containing several executables: a server, a CLI, a worker, and a maintenance script. The entry-point surface is defined in `README.md:3` ("Server: `python main.py`; CLI: `python cli.py`; worker: `python worker.py`."), and the codebase also ships a fourth executable, `scripts/backfill.py`, that the README does not mention. All executables are wired to a single shared data-access module, `db.py`.

## 2. Current shape
Six files, one subdirectory:
- `README.md` (3 lines): project title (`README.md:1`) and the one-line entry-point list for server/CLI/worker (`README.md:3`).
- `main.py` (8 lines): the server executable. Imports `get_conn` from `db` (`main.py:1`) and `serve()` prints the connection object (`main.py:3-5`); guarded entry point (`main.py:7-8`).
- `worker.py` (8 lines): the worker executable. Imports `get_conn` from `db` (`worker.py:1`) and `poll()` obtains a connection it never uses, printing only `'polling'` (`worker.py:3-5`); guarded entry point (`worker.py:7-8`).
- `cli.py` (3 lines): the CLI executable. Creates an `argparse` parser and calls `parse_args()` (`cli.py:2-3`) but never inspects or acts on the parsed arguments.
- `db.py` (2 lines): the shared data layer. `get_conn()` returns a hardcoded string `'fake-conn'` (`db.py:1-2`).
- `scripts/backfill.py` (1 line): prints `'backfill'` (`scripts/backfill.py:1`).

There are no test files, no packaging metadata, no docs directory, and no configuration of any kind.

## 3. Strong signals
- The multi-executable intent is explicit and readable: `README.md:3` names server, CLI, and worker, and each has its own file with a guarded entry point (`main.py:7-8`, `worker.py:7-8`), so the "several executables" shape is easy to discover.
- Data access is intentionally funneled through one module: both `main.py:1` and `worker.py:1` import `get_conn` from `db` rather than duplicating connection logic — a single shared data boundary exists in principle.
- The server path is coherent end-to-end in miniature: `main.py:3-5` obtains a connection and uses it in its output, so the server's shape is a plausible skeleton for a real service.
- The CLI uses the conventional `argparse` pattern (`cli.py:2-3`), so the entry point is idiomatic and cheap to extend.

## 4. Missing pieces
- **No explicit contract for the shared `db` module.** `db.py:1-2` returns a hardcoded `'fake-conn'` string — no connection parameters, no lifecycle, no error handling, no validation. The dependency that both server (`main.py:1`) and worker (`worker.py:1`) rely on is a stub with an undefined contract.
- **The shared dependency is undocumented.** `README.md:3` lists entry points but never mentions `db.py` or how the executables relate to it; the dependency graph of the system is implicit.
- **No coordination between executables.** `main.py:4` and `worker.py:4` each obtain the shared connection independently; nothing states who owns it, whether access is exclusive, or how server and worker interact with the same underlying state.
- **The CLI is a no-op.** `cli.py:2-3` parses arguments and exits without any behavior — no commands, no output.
- **The worker ignores its connection.** `worker.py:4` assigns `conn = get_conn()` and `worker.py:5` never uses `conn` — dead code that masks the worker's actual role.
- **`scripts/backfill.py` is an orphaned entry point.** It exists (`scripts/backfill.py:1`) and is executable, but `README.md:3` does not list it, so the README's executable inventory is incomplete.
- **Zero tests.** No test directory or test files exist for any of the four executables or the `db` layer.

## 5. Improvement opportunities
- Add a short "Architecture / data layer" section to the README naming `db.py` as the single shared boundary (fixes the documentation gap cheaply).
- Decide the worker's real behavior: either use `conn` in `poll()` (`worker.py:4-5`) or drop the dead assignment.
- Give the CLI at least one real command (or explicitly document it as a placeholder) so the entry point isn't a silent no-op.
- Add a pytest suite covering each executable's entry behavior and the `db` layer once the contract exists.
- Note `scripts/backfill.py` in the README, or move it under a documented `scripts/` convention.

## 6. Weakest boundary
The boundary between the **multi-executable system** and its **shared data layer** is implicit and unenforced. Both the server (`main.py:1`) and the worker (`worker.py:1`) reach into `db` via bare module-level imports, yet the module they share has no contract (`db.py:2` returns a hardcoded `'fake-conn'`), is not mentioned in the README (`README.md:3` lists only entry points), and nothing coordinates their concurrent access to the same connection. The repo's central structural fact — that several executables depend on one data module — is stated nowhere and validated by nothing.

**Weakness type:** Implicit Dependencies

Logic trace: `README.md:3` defines the product as three executables plus (in the tree) a fourth script, but never names `db.py` or any relationship between executables — the dependency graph is implied, not documented. The code shows the dependency is real and shared: `main.py:1` and `worker.py:1` both execute `from db import get_conn`, and both call sites (`main.py:4`, `worker.py:4`) obtain the same connection object with no ownership, locking, or coordination between them. The module they depend on is a stub — `db.py:1-2` is `def get_conn(): return 'fake-conn'` — so the shared contract is not just undocumented, it is undefined: no parameters, no lifecycle, no error behavior, and no validation anywhere. That is exactly weakness type 5 in `weakness-types.md`: "Skills or scripts that depend on files or paths not explicitly defined or validated." Every other defect (no-op CLI at `cli.py:2-3`, unused `conn` at `worker.py:4`, orphaned `scripts/backfill.py:1`) is a stub or documentation gap that becomes addressable only once the executables' relationship to the data layer is explicit. Hence the weakest boundary is the implicit, unvalidated `db` dependency shared by the executables.

## 6.5. Problem classification (fog type)
`primary_fog_type: architecture_fog`.

- **Not `ui_fog`**: the UI Fog Signals Registry decision tree's first gate is "does the codebase have frontend/UI code (React/Vue/Angular/HTML/CSS)?" — this repo is pure Python executables with no screens, flows, routing, or design system, and zero Tier 1 signals apply.
- **Not `product_fog`**: user needs are not the uncertainty. `README.md:3` states the product's shape plainly (server/CLI/worker); the ambiguity is about how the executables relate structurally, not what users need.
- **Not `docs_fog` as the primary problem**: the README is thin but accurate about its three named entry points; the blocker is not missing prose but the undefined `db` contract — documenting the dependency would help, but the contract itself (`db.py:1-2`) must be defined and validated in code.
- **`architecture_fog`**: multiple executables couple to a single shared module through implicit imports (`main.py:1`, `worker.py:1`) with no stated boundaries, no contract (`db.py:2`), no coordination, and no validation — a module-boundary and coupling problem, exactly the "spec-driven refactoring (default)" case. This matches the ground-truth expectation (`expected_fog_candidates: [architecture_fog]` in `corpus/ground-truth.yaml`).

## 7. Evidence
The strongest evidence is contrastive, comparing the README's executable inventory with the code's actual dependency structure:
- `README.md:3` names server, CLI, and worker — and nothing else; `db.py` and `scripts/backfill.py` never appear.
- `main.py:1` and `worker.py:1` both contain the bare import `from db import get_conn` — two independent executables coupled to one module.
- `db.py:1-2` shows the shared module's entire contract: `return 'fake-conn'` — no parameters, no lifecycle, no errors, no validation.
- `worker.py:4-5` obtains the connection (`conn = get_conn()`) and never uses it — evidence that even the worker's own relationship to the data layer is unresolved.
- `cli.py:2-3` parses arguments and exits without acting, and `scripts/backfill.py:1` prints a string and exits — additional executables whose behavior is stubbed or undocumented.

Logic trace: The README (`README.md:3`) presents the repo as a set of independent executables, but the code shows they are not independent: `main.py:1` and `worker.py:1` both import the same `db` module, making the data layer a hidden shared dependency. That dependency is simultaneously the system's only real coupling and its least defined part — `db.py:1-2` is a two-line stub returning a hardcoded string, with no contract, no documentation in the README, and no coordination between the server and worker that both consume it (`main.py:4`, `worker.py:4`). Per `weakness-types.md` type 5, a dependency that is not explicitly defined or validated is an Implicit Dependency; because it is the single structural fact that ties the multi-executable system together, it is the weakest boundary. The undefined shared boundary drives the architecture-fog classification: the repo's structural problem is module-boundary/coupling, not missing features, missing docs, or UI design.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Server: `python main.py`; CLI: `python cli.py`; worker: `python worker.py`."
    supports_claim: "README defines the product as three executables and never mentions the shared db module or scripts/backfill.py"
  - file: main.py
    lines: L1
    quote: "from db import get_conn"
    supports_claim: "The server executable couples to the shared db module via a bare module-level import"
  - file: worker.py
    lines: L1
    quote: "from db import get_conn"
    supports_claim: "The worker executable imports the same shared db module independently, with no coordination with the server"
  - file: db.py
    lines: L1-L2
    quote: "def get_conn():\n    return 'fake-conn'"
    supports_claim: "The shared data-layer contract is a hardcoded stub: no parameters, no lifecycle, no error handling, no validation"
  - file: worker.py
    lines: L3-L5
    quote: "def poll():\n    conn = get_conn()\n    print('polling')"
    supports_claim: "The worker obtains a connection it never uses, showing its relationship to the data layer is unresolved"
  - file: cli.py
    lines: L2-L3
    quote: "p = argparse.ArgumentParser()\np.parse_args()"
    supports_claim: "The CLI executable parses arguments and exits without any behavior"
  - file: scripts/backfill.py
    lines: L1
    quote: "print('backfill')"
    supports_claim: "A fourth executable exists that the README entry-point list omits"
```

## 9. Why this boundary matters
If the implicit `db` dependency stays unenforced, every executable built on it inherits an undefined contract: the server and worker both consume the same connection with no ownership or coordination (`main.py:4`, `worker.py:4`), so the moment real state replaces `'fake-conn'` (`db.py:2`), concurrent access bugs become unavoidable and untestable — there is no validation anywhere to catch them. Downstream work compounds the damage: tests cannot be written against a contract that returns a hardcoded string; a real worker cannot be implemented while its connection variable is dead (`worker.py:4`); and the README's executable inventory (`README.md:3`) misleads anyone who assumes `scripts/backfill.py` does not exist. The boundary is the contract between the multi-executable system and its shared data layer — the single highest-leverage defect in the repo, because fixing it (defining and validating the `db` contract) unblocks coordination, testing, and honest documentation in one move.

## 10. Candidate next steps
1. **Define the `db` module contract explicitly**: replace the `'fake-conn'` stub (`db.py:2`) with a real connection factory (config source, lifecycle, error handling) and document it as the single shared data boundary in `README.md` — this directly removes the Implicit Dependency.
2. **Establish ownership/coordination for the shared connection**: decide whether server (`main.py:4`) and worker (`worker.py:4`) may both hold the connection, and add an explicit mechanism (exclusive access, queue ownership, or a documented read-only contract) — or split `db.py` into per-executable access modules.
3. **Resolve the worker's dead code**: either make `poll()` use `conn` (`worker.py:4-5`) or drop the assignment, so the worker's actual data-layer role is visible.
4. **Give the CLI a real command or an explicit placeholder note** (`cli.py:2-3`) so the entry point is not a silent no-op.
5. **Add a pytest suite** covering each executable's entry behavior and the `db` contract once it exists, closing the Zero Validation gap.

## 11. Recommended next step
Make the shared `db` dependency explicit: replace the `'fake-conn'` stub in `db.py:2` with a documented connection contract (parameters, lifecycle, error handling) and name `db.py` as the shared boundary in `README.md:3`. This is the smallest concrete action with the highest leverage — it converts the repo's central implicit dependency into a defined, testable surface, and every other fix (worker coordination, tests, CLI behavior, README completeness) hangs off that contract.

## 12. Recommended workflow
`architecture-implementation-workflow` (id present in `skills/workflow-planner/references/workflow-registry.yaml`, line 848) — the spec-driven refactoring path for architecture/refactoring problems: align domain, create a refactoring spec defining module boundaries, decompose into issues, and implement via TDD. It matches the `architecture_fog` routing (the default for code-structure/boundary problems) and the diagnosis that the executables' boundary with the shared `db` module must be specified and implemented in code.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-executable
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "README.md (line L3): defines the product as server/CLI/worker executables and never mentions the shared db module or scripts/backfill.py"
  - "main.py (line L1): the server imports db.get_conn via a bare module-level import; serve() prints the connection with no contract"
  - "worker.py (lines L1, L3-L5): the worker imports the same db.get_conn and obtains a connection it never uses; no coordination with the server"
  - "db.py (lines L1-L2): get_conn() returns a hardcoded 'fake-conn' stub — the shared data-layer contract is undefined and unvalidated"
  - "cli.py (lines L2-L3): the CLI entry point parses arguments and exits without any behavior"
  - "scripts/backfill.py (line L1): a fourth executable exists that the README's entry-point list omits"
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
For `workflow-planner`:

> Plan an `architecture-implementation-workflow` run for the `multi-exec` repository (fixture `multi-executable`). Diagnosis: `primary_fog_type: architecture_fog`; weakest boundary is **Implicit Dependencies** — `README.md:3` presents the repo as independent executables, but `main.py:1` and `worker.py:1` both import `db.get_conn` from a module whose entire contract is `return 'fake-conn'` (`db.py:1-2`), with no documentation, no coordination between server (`main.py:4`) and worker (`worker.py:4`), and no validation anywhere. Objective: make the shared data boundary explicit and validated — define a real `db` connection contract (config source, lifecycle, error handling) replacing the `'fake-conn'` stub, document `db.py` as the shared boundary in the README, resolve the worker's unused `conn` (`worker.py:4`), and add a pytest suite covering each executable and the `db` layer. Keep `recommended_execution_mode: guided_execution` with review gates; do not implement anything outside this scope.
