# Repository Sensemaking Brief — tasks-cli

## 1. Repository goal

`tasks-cli` is a minimal terminal task manager: it manages a to-do list from the command line and persists tasks to a local JSON file. The README states the intent tersely — "Manage tasks from the terminal." (README.md:3) — and the implementation is a single 33-line Python module (`main.py`) using only the standard library. The README's command list (README.md:5) is the repository's de-facto product contract: `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>`.

## 2. Current shape

The repository inventory is exactly two files (OBSERVED via root listing): `README.md` (5 lines) and `main.py` (33 lines). There is no manifest, no test directory, no CI configuration, and no documentation beyond the README.

**Runtime flow (architecture reconstruction):**

- **Startup path**: `main.py:32-33` — `if __name__ == "__main__": main()` is the sole runtime entry point. It is launched as `python main.py` (no console-script packaging exists; no `pyproject.toml`/`requirements.txt` in the inventory — OBSERVED absence).
- **Orchestration**: `main.py:17-23` — `argparse` builds a subparser-based CLI (`prog="tasks"`, `main.py:18`); subcommands `add`, `list`, `done` are registered at `main.py:19-22`. `main.py:23` parses arguments; unknown commands are rejected by argparse at parse time.
- **Dispatch**: `main.py:24-30` — an `if/elif` chain on `args.cmd` routes to `add()` (`main.py:25`), inline listing (`main.py:27-28`), or the `done` branch (`main.py:29-30`). There is no branch for `delete` and no `else` for a missing subcommand (`args.cmd is None` silently does nothing).
- **Domain/core logic**: `add()` at `main.py:12-15` (appends `{"id": len(tasks) + 1, "title": title, "done": False}` and writes back) and `load()` at `main.py:7-10` (reads the file, parses JSON).
- **Persistence/state**: a single state boundary — the JSON file `tasks.json` at `main.py:5` (`STORE = Path("tasks.json")`), a relative path resolved against the process's current working directory. Read at `main.py:10`, written at `main.py:15`. No locking, no atomic write, no schema, and no error handling for corrupt JSON (`main.py:10` would raise).
- **External integration points**: none. The only imports are `argparse`, `json`, `pathlib` (`main.py:1-3`) — all standard library, all **declared = used = runtime** (exercised on the `add`/`list` execution paths). There are no third-party dependencies and no manifest to declare them.
- **Background work**: none (no workers, jobs, or scheduled tasks — OBSERVED absence).
- **Output boundary**: stdout. `list` prints raw Python dict representations (`main.py:28`); `done` prints the literal text `not implemented` (`main.py:30`); `add` prints nothing (`main.py:24-25`), so success is silent.
- **Where responsibility becomes unclear**: the boundary between the documented CLI contract (`README.md:5`) and the wired dispatch table (`main.py:19-30`). `delete` is documented but has no subparser or handler anywhere in the file (OBSERVED: the complete 33-line file contains no `delete` token); `done` is wired but its handler is a stub.

## 3. Strong signals

- **Single-file, stdlib-only implementation** (`main.py:1-3`): zero dependency friction; install/run story is `python main.py`.
- **Declarative command registration in one place** (`main.py:19-22`): argparse subparsers make the command surface visible and easy to extend.
- **State access isolated behind `load()`/`add()`** (`main.py:7-15`): the persistence boundary is concentrated in one file and two functions, which is a clean seam for tests and refactoring.
- **The data model already anticipates `done`** (`main.py:14`): the `done: False` flag exists in stored records even though no command sets it yet.
- **A documented contract exists** (`README.md:5`): the README states the full command surface in one line, which gives any future test or implementation work an explicit specification to satisfy.

## 4. Missing pieces

- **`delete` command**: documented at `README.md:5` ("`tasks delete <id>`") but entirely absent from `main.py` — no subparser at `main.py:19-22`, no handler in the dispatch chain at `main.py:24-30`. OBSERVED over the complete 33-line file.
- **`done` behavior**: the subparser exists (`main.py:22`) but the handler is a stub that prints `not implemented` (`main.py:30`) and never mutates task state.
- **Any automated validation**: no tests, no CI configuration, no package manifest exist anywhere in the repository (OBSERVED absence — the root inventory contains only `README.md` and `main.py`). Nothing checks the build/test contract or the CLI surface.
- **Input/state validation**: no error handling for corrupt or non-JSON `tasks.json` (`main.py:10`); no existence check for the id passed to `done` (`main.py:22` parses an int but nothing verifies the task exists); no unique-id guarantee — `add()` computes `id = len(tasks) + 1` (`main.py:14`), which can repeat an existing id once deletion exists (DERIVED).
- **CWD-independent state location**: `STORE = Path("tasks.json")` (`main.py:5`) silently depends on the working directory the process is launched from (INFERRED consequence of an OBSERVED relative path; UNKNOWN whether the fixture intends this).
- **User feedback**: `add` is silent on success (`main.py:24-25`); bare `python main.py` (no subcommand) exits doing nothing (`main.py:24` has no `None` branch).

## 5. Improvement opportunities

- Make `STORE` configurable (environment variable or `--store` flag) and resolve it against a stable base directory instead of the process CWD (`main.py:5`).
- Wrap `json.loads` at `main.py:10` in error handling with recovery guidance for a corrupt store.
- Print human-readable list output instead of raw dict reprs (`main.py:28`) and confirm success for `add` (`main.py:24-25`).
- Add packaging metadata (`pyproject.toml` with a `tasks` console-script entry point) so the documented `tasks` command is actually on PATH.
- Replace the `len(tasks) + 1` id scheme (`main.py:14`) with `max(existing ids) + 1` before any deletion feature lands (currently latent, DERIVED).
- Add `pytest` tests with `tmp_path`-isolated stores covering all four commands.

## 6. Weakest boundary

**Candidate generation and scoring:**

1. **Documented CLI surface vs wired subcommands** — `README.md:5` promises four commands; `main.py:19-23` wires three, one of which is a stub. `evidence_strength: strong` (both sides directly observed); `severity: high` (a documented command fails outright); `blast_radius: medium` (1 of 4 commands, but the entire product IS the CLI surface); `goal_relevance: high` (the repo's whole purpose is these commands); `downstream_blocking_effect: high` (any next step — tests, packaging, new commands — must first settle the contract); `uncertainty: low`. → **SELECTED**.
2. **`done` stub** — `main.py:22` registers the command; `main.py:30` prints `not implemented`. `evidence_strength: strong`; `severity: medium` (command runs and exits 0 while changing nothing — a misleading no-op rather than a hard failure); `blast_radius: low-medium`; `goal_relevance: high`; `downstream_blocking_effect: medium`; `uncertainty: low`. Lost to #1: the entry point is reachable and acknowledged, so the failure is a silent lie instead of a broken promise.
3. **`add()` id-collision logic** — `main.py:14` (`"id": len(tasks) + 1`). `evidence_strength: medium` (DERIVED — only manifests once deletion exists); `severity: medium`; `blast_radius: low`; `goal_relevance: medium`; `downstream_blocking_effect: low`; `uncertainty: medium`. Lost: currently unreachable defect — no deletion path exists to trigger it.
4. **Zero validation of the whole repo** — no tests, no CI, no manifest (OBSERVED absence). `evidence_strength: strong`; `severity: medium`; `blast_radius: high` (whole repo); `goal_relevance: medium`; `downstream_blocking_effect: medium`; `uncertainty: low`. Lost: real but generic — the specific contract hole in #1 is sharper, more central, and blocks the same downstream work.

**Selection (mandatory structure):**

```text
Boundary: the documented CLI command surface — README.md:5 promises four
commands; main.py:19-23 wires only add/list/done; of the wired commands,
done is a stub (main.py:30).
Observed contract: README.md:5 — "Commands: `tasks add <title>`, `tasks
list`, `tasks done <id>`, `tasks delete <id>`."
Observed violation or uncertainty: `tasks delete <id>` has no subparser
(main.py:19-22 registers add, list, done only) and no handler anywhere in
the 33-line file; invoking it fails at argparse parse time (main.py:23).
`tasks done <id>` parses (main.py:22) but its handler prints "not
implemented" (main.py:30) without touching state.
Evidence: README.md:5; main.py:19-22; main.py:29-30; main.py:14.
Weakness type: Ghost Features
Logic trace: README.md:5 documents `tasks delete <id>` as a live command.
main.py:19-22 registers subparsers only for add, list, and done, and the
complete file (33 lines, fully inspected) contains no `delete` token. A
documented product surface with no reachable implementation is exactly the
GAP-6 Ghost Features case ("Ghost Features ONLY for documented surface with
no reachable implementation") — `delete` is documented (README.md:5) and has
no reachable implementation. The `done` stub (main.py:29-30) is reachable
but skeletal — an entry-point stub that reinforces the same contract
failure rather than a separate defect. Because the promise lives in the
README's product surface and the code is absent (not merely misdescribed),
the mismatch is a product-contract defect: primary_fog_type product_fog,
with the `done` stub noted as a secondary architecture_fog signal.
Failure consequence: a user following the README gets argparse's "invalid
choice: 'delete'" error (exit code 2) on the documented delete workflow;
`tasks done 1` exits 0 while changing nothing, teaching users that
commands succeeded when they did not. Once delete is implemented, the
len(tasks)+1 id scheme (main.py:14) will emit duplicate ids. Any downstream
work — tests, packaging, new commands — builds on a contract that is
already false.
Confidence: high — both sides of the mismatch are directly observed in the
two files that constitute the entire repository. What would raise it
further: a task-owner statement of the intended command set (UNKNOWN — no
issue tracker, roadmap, or tests exist in the repo to disambiguate).
Alternatives considered: (2) the `done` stub (main.py:22, 30) — real
evidence, but reachable and acknowledged, so a misleading no-op rather than
a broken promise; lost on severity. (3) the latent id-collision logic
(main.py:14) — DERIVED and currently unreachable; lost on consequence and
evidence. (4) zero automated validation (no tests/CI/manifest) — real but
generic; lost on centrality to the repo's goal.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)

**Primary fog type: `product_fog`.**

Reasoning (evidence-based, per the skill's classification rules):

- **Not `ui_fog`**: the UI Fog Signals Registry decision tree's first check is whether frontend code exists (React/Vue/Angular/HTML/CSS). This repository has no frontend surface at all (OBSERVED: inventory is `README.md` + `main.py`, stdlib-only) → not ui_fog; no Tier 1/2 signals are checkable because the checkable surface is absent.
- **`product_fog` (primary)**: the README advertises `tasks delete <id>` as a real deliverable (`README.md:5`) and no code exists for it anywhere (`main.py:19-23`, complete file inspection). Per the skill's ghost-feature reasoning, a README that advertises a feature as real while the code does not implement it is a defect in the *product promise*, i.e. `product_fog` — the defect is the promise, not the docs.
- **Contributing `architecture_fog` (secondary, recorded in prose only)**: the `done` command (`main.py:22`, `main.py:30`) is a stubbed RUNTIME ENTRY POINT within an otherwise-running system — a structural defect by the skill's entry-point-stub rule (entry points that run but form an incomplete system are architecture; features with no implementation at all are product). This is secondary because the sharper, more central failure is the absent `delete` deliverable.
- **Not `docs_fog`**: the README is not stale prose misdescribing existing code (which would be Vocabulary Drift); it is a product contract listing a command that does not exist in any form.

`user_implied_fog_type` is `unknown` and `diagnosis_conflict` is `false` per GAP-8: this is a no-user-intent fixture run with no problem statement to conflict with.

## 7. Evidence

All substantive claims trace to the two files that constitute the repository, both fully inspected.

- `README.md:5` documents the four-command surface, including `tasks delete <id>` — the OBSERVED product contract that the code does not fulfill.
- `main.py:19-22` registers argparse subparsers for `add`, `list`, and `done` only — OBSERVED absence of any `delete` subparser.
- `main.py:29-30` is the entire `done` branch: it prints `not implemented` — OBSERVED stub; no task state is ever mutated by it.
- `main.py:14` computes `id` as `len(tasks) + 1` — DERIVED: this scheme collides once deletion is implemented (deleting an id below the max, then adding, reuses an id).
- `main.py:5` and `main.py:7-10` define the state boundary: a CWD-relative `tasks.json` read via `json.loads` with no corruption handling — OBSERVED implicit dependency on the working directory and zero validation of stored data.
- No test files, no CI configuration, and no package manifest exist in the root inventory (OBSERVED absence — only `README.md` and `main.py` are present).

**Logic trace:** `README.md:5` is the repository's only specification and it lists four commands. `main.py:19-22` — the only command-registration point in the codebase — registers three, and the complete file read of `main.py` (33 lines) finds no `delete` handler in the dispatch chain at `main.py:24-30`. A documented surface with no reachable implementation is Ghost Features under the GAP-6 taxonomy, and because the absent surface is a README-advertised deliverable rather than misdescribed existing code, the mismatch is a product promise defect → `product_fog`. The `done` stub (`main.py:22`, `main.py:30`) is a reachable-but-skeletal entry point, which the skill classifies as a structural (architecture) signal; it is recorded as secondary fog because the primary contract failure — the missing `delete` command — is the defect a user hits first and the one with no implementation of any kind. This chain is what makes the CLI command surface the weakest boundary: every other candidate (id collision, zero validation) is either latent, generic, or downstream of this contract.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L5
    quote: |-
      Commands: `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>`.
    supports_claim: The README documents four commands, including `tasks delete <id>` — the documented surface with no implementation.
  - file: main.py
    lines: L19-L22
    quote: |-
      sub = p.add_subparsers(dest="cmd")
      add_p = sub.add_parser("add"); add_p.add_argument("title")
      sub.add_parser("list")
      done_p = sub.add_parser("done"); done_p.add_argument("id", type=int)
    supports_claim: argparse registers only add/list/done subparsers; no delete subparser exists anywhere.
  - file: main.py
    lines: L29-L30
    quote: |-
      elif args.cmd == "done":
          print("not implemented")
    supports_claim: The done command is a reachable but skeletal stub that never mutates task state.
  - file: main.py
    lines: L12-L15
    quote: |-
      def add(title: str):
          tasks = load()
          tasks.append({"id": len(tasks) + 1, "title": title, "done": False})
          STORE.write_text(json.dumps(tasks))
    supports_claim: add() assigns id = len(tasks)+1 (latent collision once delete exists) and models a done flag nothing ever sets.
  - file: main.py
    lines: L5
    quote: |-
      STORE = Path("tasks.json")
    supports_claim: Task state is a relative path resolved against the current working directory (implicit environment dependency).
  - file: main.py
    lines: L7-L10
    quote: |-
      def load():
          if not STORE.exists():
              return []
          return json.loads(STORE.read_text())
    supports_claim: load() has no error handling for corrupt JSON and no schema validation of stored tasks.
  - file: main.py
    lines: L32-L33
    quote: |-
      if __name__ == "__main__":
          main()
    supports_claim: main.py is the sole runtime entry point, launched as `python main.py`.
```

## 9. Why this boundary matters

The README is the only contract this repository has, and it is false in the way a product promise is false: one of the four documented commands does not exist and a second does nothing. A user following the README hits a hard argparse failure on `tasks delete` and a silent, exit-0 no-op on `tasks done` — the two failure modes (loud absence, quiet lie) that most erode trust in a CLI. If the boundary stays weak, every subsequent improvement builds on a false contract: tests would encode the wrong surface, packaging would ship a `tasks` binary with a documented command that cannot run, and the latent id-collision bug in `main.py:14` becomes live the moment anyone "helpfully" implements delete. The boundary is also the natural first decision point: it cannot be fixed by documentation alone (docs_fog would be wrong — the docs are the source of truth here) and it cannot be fixed by refactoring alone (the missing deliverable is a product decision, not a structural one).

## 10. Candidate next steps

1. **Lock the command contract (product decision first)**: fixture/task owner decides whether `delete` and `done` are in scope; if not, trim `README.md:5` to match the implemented surface. This is the cheapest way to make the contract true and is the prerequisite for everything else.
2. **Implement `tasks delete <id>`**: add a `delete` subparser alongside `main.py:19-22`, an id-validated handler in the dispatch chain at `main.py:24-30`, and remove the task from `tasks.json`. Also fix the id scheme at `main.py:14` (max+1) so deletion cannot cause duplicate ids.
3. **Implement `tasks done <id>`**: replace the stub at `main.py:30` with real state mutation (set `done: True` for the matching id and persist via the `main.py:15` write path), with existence validation.
4. **Add a test suite**: `pytest` coverage of all four commands with `tmp_path`-isolated stores (patching `STORE` from `main.py:5`), asserting exit codes and persisted JSON — the first automated check this repository has ever had.
5. **Package the CLI**: add `pyproject.toml` with a `tasks` console-script entry point so the documented command name is actually invocable.

## 11. Recommended next step

**Decide and lock the command contract, then implement `tasks delete <id>`.** The smallest highest-leverage action is: (a) get the fixture/task owner's explicit call on whether `delete`/`done` are in scope, and (b) implement `delete` so `README.md:5` becomes accurate — a ~15-line change (subparser at `main.py:19-22` block, handler in the `main.py:24-30` dispatch chain, id fix at `main.py:14`). This single step converts the repository's only specification from fiction to fact and unblocks every other candidate step; steps 4 and 5 (tests, packaging) only make sense against a settled contract.

## 12. Recommended workflow

**`product-implementation-workflow`** (execution mode: `guided_execution`), from the canonical `skills/workflow-planner/references/workflow-registry.yaml` (verified: id present at registry lines 644-714; `allowed_execution_modes` = `guided_execution`, `autonomous_execution`, registry lines 654-657 — `plan_only` is NOT offered, and no invented mode is used).

**Routing rationale**: the primary fog type is `product_fog` — the README promises a deliverable (`tasks delete`) that has no implementation. `product-implementation-workflow` is the registry's designated path for product/feature problems: it aligns the domain, researches user needs, synthesizes opportunities, then produces a PRD and issues (registry lines 644-714). That chain fits this fixture's defect exactly: the first step must establish *what the command surface should be* (the product promise) before implementation.

**Why not the closest alternatives**: `implementation-workflow` (registry lines 587-643) is the generic default for architecture/code-design problems but omits the discovery/opportunity steps that a promise-level product defect needs; `architecture-implementation-workflow` (registry lines 848-904) would only fit if the `done` stub were the primary defect — the missing `delete` deliverable is product-level, not structural; `ui-diagnostic-workflow` (registry lines 715-747) is excluded because the repository has no frontend surface (UI Fog registry decision-tree step 1).

**Preconditions before it can run**: a `user_intent` artifact stating who owns the command-contract decision and which commands are in scope (currently UNKNOWN — no intent artifact exists in this fixture); `repository_state` is fully captured by this brief. If no intent is ever supplied, escalation (rather than guessing a workflow) is the correct fallback.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: 'H:\GithubRepositories\sensemaking-skills\experiments\repository-sensemaking-skill-hardening-v1\corpus\cli-app'
source_intent_ref: 'none (no-user-intent fixture run; GAP-8)'
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "README.md (L5): documents the full command surface including `tasks delete <id>`"
  - "main.py (L19-L22): argparse subparsers register only add/list/done; no delete subparser exists"
  - "main.py (L29-L30): done handler is a stub printing 'not implemented'"
  - "main.py (L12-L15): add() assigns id = len(tasks)+1 and models a done flag nothing sets"
  - "main.py (L5, L7-L10): state is a CWD-relative tasks.json read with no corruption handling"
  - "No test files, CI config, or package manifest exist in the root inventory (OBSERVED absence)"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary:
  type: Ghost Features
  evidence:
    - "README.md (L5): `tasks delete <id>` documented as a live command"
    - "main.py (L19-L22): only add/list/done are wired; no delete implementation anywhere"
    - "main.py (L29-L30): done is a reachable but skeletal stub"
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
timestamps:
  created_at: "2026-08-07T04:10:00Z"
created_at: "2026-08-07T04:10:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

> You are planning the next step for `tasks-cli` (experiments/repository-sensemaking-skill-hardening-v1/corpus/cli-app), a two-file terminal task manager whose README (README.md:5) documents four commands but whose implementation (main.py:19-30) wires only three, with `done` stubbed and `delete` absent (Ghost Features; primary fog type: product_fog; secondary architecture_fog from the done stub). The sensemaking brief recommends the `product-implementation-workflow` in `guided_execution` mode. Before any implementation: (1) obtain an explicit owner decision on the intended command surface — is `delete` in scope, and should `done` mutate state? (2) If in scope, plan the implementation of `tasks delete <id>` (subparser beside main.py:19-22, id-validated handler in the main.py:24-30 dispatch, unique-id fix at main.py:14) plus the real `done` mutation replacing the main.py:30 stub, followed by a pytest suite with tmp_path-isolated stores. (3) Do not route to a UI workflow — the repository has no frontend surface. Produce the orchestration plan using only workflow IDs from the canonical workflow-registry.yaml.
