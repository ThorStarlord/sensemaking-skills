# Repository Sensemaking Brief: tasks-cli (cli-app fixture)

## 1. Repository goal
A minimal terminal-based task manager ("tasks-cli"): a Python `argparse` CLI that stores tasks in a local JSON file and exposes `add`, `list`, `done`, and `delete` commands. The intended product surface is defined in `README.md:1-5` ("Manage tasks from the terminal. Commands: `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>`.").

## 2. Current shape
The repository is two files, no subdirectories:
- `README.md` (5 lines): project title (`README.md:1`), one-line purpose (`README.md:3`), and the documented command list (`README.md:5`).
- `main.py` (33 lines): the entire implementation.
  - `STORE = Path("tasks.json")` — storage location (`main.py:5`).
  - `load()` — reads `tasks.json`, returns `[]` if the file does not exist (`main.py:7-10`).
  - `add(title)` — appends `{"id": len(tasks) + 1, "title": title, "done": False}` and writes the file (`main.py:12-15`).
  - `main()` — argparse setup with `add`, `list`, `done` subparsers (`main.py:17-23`) and a dispatch chain for `add`/`list`/`done` (`main.py:24-30`).
  - `if __name__ == "__main__":` entry guard (`main.py:32-33`).

There are no test files, no packaging metadata, no docs directory, and no other source modules.

## 3. Strong signals
- Storage is cleanly isolated behind two small functions (`load()`/`add()`, `main.py:7-15`), so the data layer is easy to extend and test once test scaffolding exists.
- The CLI uses the standard `argparse` subcommand pattern (`main.py:18-23`), which is conventional and self-documenting via `--help`.
- `load()` gracefully handles a missing store file (`main.py:8-9`), so first-run behavior does not crash.
- The README crisply defines the intended command surface (`README.md:5`), which makes the gap between documentation and implementation measurable.

## 4. Missing pieces
- **`delete` command: absent from code entirely.** `README.md:5` documents `tasks delete <id>`, but `main.py:19-22` registers only `add`, `list`, and `done` subparsers, and the dispatch chain (`main.py:24-30`) has no `delete` branch. Running `tasks delete 1` produces an argparse "invalid choice" error.
- **`done` command: a non-functional stub.** The subparser exists (`main.py:22`), but its handler is `print("not implemented")` (`main.py:30`); no task is ever marked done and nothing is persisted.
- **No tests.** The repo has no test files at all (only `README.md` and `main.py` exist); the command behaviors and JSON persistence have zero automated checks (Zero Validation).
- **No user feedback on `add`.** `add()` silently writes the store (`main.py:15`) without printing confirmation.
- **No error handling for corrupt data.** `json.loads(STORE.read_text())` (`main.py:10`) will raise an uncaught exception if `tasks.json` is malformed.

## 5. Improvement opportunities
- Add a pytest suite covering `add`/`list`/`done`/`delete` and store persistence once the missing commands exist — this directly addresses the Zero Validation gap.
- Rework ID assignment: `len(tasks) + 1` (`main.py:14`) reuses IDs after any deletion, which would corrupt the `done <id>`/`delete <id>` contract the moment `delete` is implemented; a monotonic `max(id) + 1` (or a counter) avoids duplicate IDs.
- Format `list` output (`main.py:27-28`) as a readable table/rows instead of raw Python dict repr.
- Give every mutating command consistent feedback (e.g. "Added task 3", "Task 2 marked done") so the CLI behaves like a finished product.
- Add a small `--help`-consistent usage note in the README about the store file location (`main.py:5`).

## 6. Weakest boundary
The boundary between the **documented product surface** and the **implemented CLI** is broken. `README.md:5` promises four commands; `main.py:19-22` implements three subparsers, of which one (`done`) is a placeholder (`main.py:30`) and one documented command (`delete`) has no code path at all. A user who follows the README gets an argparse error for `tasks delete 1` and a silent no-op for `tasks done 1` — the documentation and the code disagree about what this product does.

**Weakness type:** Ghost Features

Logic trace: `README.md:5` documents `tasks done <id>` and `tasks delete <id>` as supported commands. `main.py:19-22` registers only `add`, `list`, and `done` subparsers, and `main.py:30` implements `done` as `print("not implemented")` — while no `delete` subparser or dispatch branch exists anywhere in the file. Therefore two of the four documented commands have no working implementation: `done` is a placeholder and `delete` is entirely absent. That is exactly "functionality mentioned in documentation that has no corresponding implementation" — the defining case of Ghost Features. Every other part of the repo (CLI wiring, storage, entry point) is coherent, so this doc-vs-implementation mismatch is the weakest, most user-visible boundary.

## 6.5. Problem classification (fog type)
`primary_fog_type: product_fog`.

- **Not `ui_fog`**: the UI Fog Signals Registry decision tree's first gate is "does the codebase have frontend/UI code (React/Vue/Angular/HTML/CSS)?" — this repo has none; it is a terminal CLI with no screens, flows, routing, or design system.
- **Not `architecture_fog`**: the code is a single 33-line module with clear function boundaries; there is no structural confusion, coupling, or unclear module layout.
- **Not `docs_fog` as the primary problem**: the README is short, unambiguous, and current in its own terms; the source of the mismatch is that the *code* fails to realize the documented feature set — `main.py:30` literally acknowledges a feature that is "not implemented", i.e. the product is unfinished rather than mis-documented. Generating more documentation would not restore `delete`.
- **`product_fog`**: the documented requirements (the four-command feature set in `README.md:5`) are not realized in the implementation; the central uncertainty a consumer faces is "which of these features actually exist". The blocker is incomplete feature delivery, which needs feature implementation rather than research, docs work, or refactoring.

## 7. Evidence
The strongest evidence is contrastive, comparing the README's claim with the code's actual surface:
- `README.md:5` lists all four commands, including `tasks done <id>` and `tasks delete <id>`.
- `main.py:19-22` registers only the `add`, `list`, and `done` subparsers — there is no `delete` subparser, so the documented `delete` command has no implementation to reach.
- `main.py:30` shows the `done` handler is `print("not implemented")` — a stub, not a feature.
- `main.py:14` shows IDs are assigned as `len(tasks) + 1`, which will collide once deletion exists.
- `main.py:7-10` shows the persistence layer (`load`) with no validation of file contents.

Logic trace: The README is the only specification in this repo and it defines four commands (`README.md:5`). The argparse wiring (`main.py:19-22`) and dispatch (`main.py:24-30`) implement only three commands, with `done` stubbed out (`main.py:30`) and `delete` missing entirely. A feature that is documented but has no corresponding implementation is, by definition, a Ghost Feature (weakness-types.md, type 3). Because the repo is otherwise small and internally consistent, this doc-vs-implementation mismatch is the most consequential boundary: it determines what the product actually delivers, and it is the boundary that would corrupt any downstream work (tests, packaging, feature planning) built on the README's command inventory. Hence the weakest boundary is Ghost Features and the primary fog is product_fog — the documented product surface is not delivered by the code.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: README.md
    lines: L5
    quote: 'Commands: `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>`.'
    supports_claim: "README documents four commands, including done and delete, as the product surface"
  - file: main.py
    lines: L19-L22
    quote: 'done_p = sub.add_parser("done"); done_p.add_argument("id", type=int)'
    supports_claim: "Only add, list, and done subparsers are registered; there is no delete subparser"
  - file: main.py
    lines: L29-L30
    quote: 'print("not implemented")'
    supports_claim: "The done command is a stub that never marks a task done or persists anything"
  - file: main.py
    lines: L12-L15
    quote: 'tasks.append({"id": len(tasks) + 1, "title": title, "done": False})'
    supports_claim: "IDs are assigned as len(tasks)+1, which will reuse IDs after deletion; add() writes with no user feedback"
  - file: main.py
    lines: L5
    quote: 'STORE = Path("tasks.json")'
    supports_claim: "Storage is a single local JSON file; the whole implementation is one module with no tests"
```

## 9. Why this boundary matters
If the documented-vs-implemented command surface stays broken, every user following the README hits an argparse error (`tasks delete <id>`) or a silent no-op (`tasks done <id>`), eroding trust in the documentation and the tool. Downstream work compounds the damage: a test suite written against the README would fail before it can validate anything; feature planning cannot reference `delete` because the code has no hook for it; and the ID scheme (`main.py:14`) is already incompatible with deletion, so whoever finally implements `delete` will silently introduce duplicate-ID bugs unless the ID assignment is fixed in the same change. The boundary is the contract between what the product promises and what it delivers — the single most user-visible and highest-leverage defect in the repo.

## 10. Candidate next steps
1. **Implement the `delete` subcommand and handler** in `main.py` (subparser + dispatch branch + store rewrite), restoring the README contract for `tasks delete <id>`.
2. **Implement the `done` handler** (`main.py:30`): look up the task by id, set `done: true`, persist, and print feedback — replacing the `"not implemented"` stub.
3. **Fix ID assignment** (`main.py:14`) to `max(existing ids) + 1` so deletion cannot cause ID reuse.
4. **Add a pytest suite** covering `add`/`list`/`done`/`delete` and persistence, closing the Zero Validation gap.
5. **Reconcile the contract**: if the feature set is intentionally smaller, trim `README.md:5` to the implemented commands (docs-side fallback) — but the stub text at `main.py:30` indicates implementation is the intended direction.

## 11. Recommended next step
Implement the missing `delete` subcommand and handler in `main.py` (smallest concrete action that restores the documented product surface and unblocks the `done` and ID fixes). Pair it with the `len(tasks)+1` ID fix in the same change, since `delete` cannot exist safely under the current ID scheme (`main.py:14`).

## 12. Recommended workflow
`product-implementation-workflow` (id present in `skills/workflow-planner/references/workflow-registry.yaml`, line 644) — the feature-implementation path for product/feature problems: align domain, specify the feature set, decompose into issues, and implement via TDD. It matches the canonical-vocabulary routing (`typical_fog_types: [product_fog]`) and the diagnosis that the documented feature surface must be delivered in code.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/cli-app
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "README.md (line L5): documents tasks done <id> and tasks delete <id> as supported commands"
  - "main.py (lines L19-L22): only add, list, and done subparsers are registered; no delete subparser exists"
  - "main.py (line L30): done handler is a stub that prints 'not implemented'"
  - "main.py (line L14): IDs are assigned as len(tasks)+1, unsafe once delete exists; no test files exist in the repo"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
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
For `workflow-planner`:

> Plan a `product-implementation-workflow` run for the `tasks-cli` repository (fixture `cli-app`). Diagnosis: `primary_fog_type: product_fog`; weakest boundary is **Ghost Features** — `README.md:5` documents four commands but `main.py:19-22` registers only `add`/`list`/`done`, `main.py:30` stubs `done` as `print("not implemented")`, and `delete` has no implementation at all. Objective: deliver the documented feature surface in code — implement the `delete` subcommand + handler, replace the `done` stub with real mark-and-persist logic, fix the `len(tasks)+1` ID assignment (`main.py:14`) so deletion cannot reuse IDs, and add a pytest suite covering all four commands and JSON persistence. Keep `recommended_execution_mode: guided_execution` with review gates; do not implement anything outside this scope.
