# Repository Sensemaking Brief

## 1. Repository goal

`tasks-cli` is a minimal terminal-based task manager: the README (`README.md:1`, `README.md:3`) states it is meant to "Manage tasks from the terminal." The documented product contract (`README.md:5`) is a four-command CLI surface — `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>` — with JSON file persistence. The repository is a 2-file Python fixture (no packaging, no tests, no CI), so the README command list is effectively the only specification of what the product is supposed to do.

## 2. Current shape

**Inventory (Pass A).** The repository contains exactly two files: `README.md` (136 bytes, 5 lines) and `main.py` (879 bytes, 33 lines). There is no manifest (`pyproject.toml`/`setup.py`/`requirements.txt`), no CI configuration, no container/deployment config, no test directory, and no documentation beyond the README. Dependency semantics: `argparse` (`main.py:1`), `json` (`main.py:2`), and `pathlib.Path` (`main.py:3`) are imported — `used` at the module level (no manifest exists, so nothing is merely `declared` or `dead`); no third-party dependencies.

**Runtime flow (Pass B/C).** What starts the system: `python main.py`; the entry guard is `if __name__ == "__main__": main()` (`main.py:32-33`). The `argparse` program name is hard-coded to `tasks` (`main.py:18`), matching the README's command prefix. Orchestration: `main()` builds the subparser surface — `add` with a `title` argument (`main.py:20`), `list` (`main.py:21`), and `done` with an `int` id (`main.py:22`) — then dispatches on `args.cmd` (`main.py:23-30`). Domain logic: `load()` reads the store (`main.py:7-10`) and `add()` appends a task and writes the store back (`main.py:12-15`). State: a single JSON file `tasks.json` (`STORE = Path("tasks.json")`, `main.py:5`), resolved relative to the process working directory; it is read in `load()` (`main.py:10`) and written in `add()` (`main.py:15`); a missing file is tolerated (`main.py:8-9`). External integration points: none — no network, no services, no background work. Output boundary: `list` prints each task dict raw (`main.py:27-28`); `done` prints the literal string "not implemented" (`main.py:30`).

**Where validation happens (Pass D).** Almost nowhere. The only typed boundary is `argparse`'s `type=int` on the `done` id (`main.py:22`). There are no tests of any kind in the repository, no schema, no input validation (an empty `title` is accepted by `add`), no existence check for the id passed to `done`, and `json.loads(STORE.read_text())` (`main.py:10`) has no error handling — a corrupt `tasks.json` raises an uncaught `JSONDecodeError`.

**Where responsibility becomes unclear (Pass C/D).** The `done` command's dispatch branch exists but its behavior is a stub (`main.py:29-30`); the `delete` command has no parser and no dispatch branch at all — a user following the README reaches a dead end for two of the four documented commands. The persistence boundary (tasks.json read/write) is unvalidated, and the task-id scheme (`main.py:14`) is derived from list length, which only stays collision-free while the list never shrinks.

## 3. Strong signals

- Single, obvious entry point with a standard `argparse` structure (`main.py:17-33`) — easy to run and to extend.
- The README is concise and explicit about the intended command surface (`README.md:5`), which gives the project a concrete, testable contract to build against.
- `load()` gracefully handles a missing store file (`main.py:8-9`), so first-run behavior is defined.
- Persistence is simple and predictable: one JSON file, one read path (`main.py:10`), one write path (`main.py:15`).
- No dead dependencies, no generated code, no build complexity.

## 4. Missing pieces

- **`tasks delete <id>`** — documented at `README.md:5`, entirely absent from the parser surface (`main.py:20-22`) and the dispatch (`main.py:24-30`).
- **`tasks done <id>` behavior** — documented at `README.md:5`, present only as a stub that prints "not implemented" (`main.py:29-30`); it never marks a task done or persists anything.
- **Tests** — no test files, no test framework, no CI; the documented contract has zero automated checks.
- **Input/error validation** — no id-existence check for `done`, no handling of a corrupt `tasks.json` (`main.py:10`), no guard against empty titles.
- **Packaging** — no `pyproject.toml`/entry-point declaration; the README's `tasks` command name (`README.md:5`, `main.py:18`) cannot actually be installed as a shell command.
- **Behavioral documentation** — nothing documents id semantics, storage location, or the fact that two of four commands are unimplemented.

## 5. Improvement opportunities

- Replace the length-based id assignment (`len(tasks) + 1`, `main.py:14`) with `max(existing ids) + 1` so ids stay unique once deletion exists.
- Wrap `json.loads` (`main.py:10`) to surface a friendly error instead of an uncaught `JSONDecodeError` on a corrupt store.
- Format `list` output (`main.py:27-28`) as readable lines instead of raw Python dict reprs.
- Add a `pyproject.toml` with a console-script entry point so `tasks` is installable as documented.
- Add type annotations and a small docstring per function — the file is tiny and would stay readable.

## 6. Weakest boundary

Candidate generation and scoring (2-5 candidates required; evidence authority in parentheses):

| # | Candidate boundary | Evidence | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|---|---|
| A | **README CLI contract vs. implemented command surface** — `README.md:5` promises 4 commands; `main.py:20-22` parses only add/list/done and `main.py:29-30` stubs `done`; `delete` has no parser/handler (OBSERVED) | `README.md:5`, `main.py:20-22`, `main.py:29-30` | strong | high | high (whole product surface) | high | high | low |
| B | **Persistence boundary** — `tasks.json` read/write with no validation: `json.loads` without error handling (`main.py:10`), unconditional overwrite (`main.py:15`), zero tests (OBSERVED/UNKNOWN) | `main.py:10`, `main.py:15` | strong | medium | medium | medium | medium | low |
| C | **Task identity scheme** — ids assigned as `len(tasks) + 1` (`main.py:14`) assume an append-only, never-shrinking list; a collision becomes reachable exactly when `delete` is implemented (OBSERVED code, INFERRED failure) | `main.py:14` | medium | medium | medium | medium-high | medium | medium |

**Selection.** Candidate A wins: strongest combination of high consequence (2 of 4 documented commands unusable), strong direct evidence (the promise is in `README.md:5`, the absence is in `main.py:20-30`), centrality to the repo's only goal, and downstream blocking effect (every other improvement — tests, packaging, the id fix in Candidate C — depends on first deciding what the command surface actually is). Candidate B is real but secondary: it becomes acute only once the commands work. Candidate C is a latent flaw that cannot even be triggered until Candidate A is fixed.

```text
Boundary:
The README's documented CLI contract (`README.md:5`) versus the actually
implemented command surface (`main.py:20-30`). Two of the four documented
commands — `tasks done <id>` and `tasks delete <id>` — have no working
implementation: `done` is a stub, `delete` does not exist.
Observed contract:
README.md:5 — "Commands: `tasks add <title>`, `tasks list`, `tasks done <id>`,
`tasks delete <id>`." (four commands, all presented as real).
Observed violation or uncertainty:
main.py:20-22 defines parsers only for add, list, and done — there is no
`delete` parser. main.py:29-30 shows the `done` branch is a stub:
`print("not implemented")`. The README does not mention that either command
is unimplemented.
Evidence:
README.md:5; main.py:20-22; main.py:29-30; main.py:24-25 (the contrast: `add`
is fully wired end-to-end).
Weakness type:
**Weakness type:** Ghost Features
Logic trace:
The README is the only specification in this repository (no other docs
exist), and it lists `done` and `delete` as first-class commands
(README.md:5, OBSERVED). The parser surface registers only add, list, and
done (main.py:20-22, OBSERVED), and the done handler prints "not
implemented" instead of mutating state (main.py:29-30, OBSERVED). A
command that is documented as functional but has no reachable
implementation of its documented behavior is exactly the definition of
Ghost Features in weakness-types.md ("Functionality mentioned in
documentation that has no corresponding implementation"). The add path
(main.py:24-25) proves the wiring pattern exists and works, so the absence
is not an architectural constraint — the features are simply unimplemented
promises (DERIVED). Therefore the weakest boundary is the documented
product contract vs. the implemented command surface, classified as Ghost
Features.
Failure consequence:
A user who follows the README can add and list tasks, but `tasks done 1`
silently does nothing (prints "not implemented") and `tasks delete 1`
crashes with `argparse` "invalid choice" — the product contract and the
product diverge on half of the documented surface, and there is no test or
check that would catch the divergence.
Confidence:
high — every element is directly observable in two small files with no
conflicting evidence. What would raise it further: a user-intent artifact
confirming the README surface is the intended contract (none exists in this
fixture run).
Alternatives considered:
Candidate B (Zero Validation at the tasks.json boundary, main.py:10/15) —
real but secondary: the unguarded read/write only becomes a live failure
mode once the commands actually run, and it scores lower on goal relevance
and downstream blocking. Candidate C (id scheme, main.py:14) — a latent
identity-collision flaw that is unreachable today because delete does not
exist; it is best fixed as part of implementing the missing commands, not
treated as the primary boundary. Both remain recorded as secondary
opportunities in Sections 5 and 10.
```

## 6.5. Problem classification (fog type)

**primary_fog_type: product_fog.** The defect is in the product contract: the README advertises `tasks done <id>` and `tasks delete <id>` as real deliverables (`README.md:5`) and the code does not implement them (`main.py:20-30`). Per the ghost-feature reasoning in SKILL.md, "when the README advertises a feature as real and the code does not implement it, that is product_fog — the defect is the promise, not the docs." The `done` stub (`main.py:29-30`) additionally shows an incomplete product workflow: the parser was scaffolded, the behavior was never finished.

Secondary, contributing fog: **docs_fog** — the README is also stale as documentation (it does not state that `done` is unimplemented and omits `delete`'s absence), so any fix must update the README in the same change; docs_fog alone does not drive routing.

Not `ui_fog`: the repository contains no frontend code at all (no React/Vue/HTML/CSS), which per the UI Fog Signals Registry decision tree rules out ui_fog. Not `architecture_fog`: the code is structurally trivial — a single module, no coupling, no state-management or boundary problem; the gap is missing product behavior, not structure. No user-intent artifact exists for this fixture run, so `user_implied_fog_type: unknown` and `diagnosis_conflict: false`; no escalation is warranted because the evidence is direct and unambiguous (`escalation_recommended: false`).

## 7. Evidence

All claims trace to the two files that constitute the repository, both fully inspected:

- `README.md:5` — documents the four-command contract: "Commands: `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>`."
- `main.py:20-22` — parser surface registers only `add`, `list`, and `done`; no `delete` parser exists.
- `main.py:29-30` — the `done` branch is a stub: `print("not implemented")`; nothing marks a task done or writes state.
- `main.py:24-25` — the `add` path is fully wired (dispatch → `add()` → persist), demonstrating the wiring pattern the missing commands should follow.
- `main.py:14` — ids are assigned as `len(tasks) + 1`, an implicit assumption that the list never shrinks.
- `main.py:10` — `json.loads(STORE.read_text())` with no error handling; `main.py:8-9` tolerates a missing file only.
- Repo-level absence (OBSERVED via directory listing, not a file): no tests, no manifest, no CI — so nothing validates the documented contract.

The classification uses only OBSERVED evidence for the core claim (README text vs. parser/dispatch code); the id-collision failure mode is labeled INFERRED (it becomes reachable only after `delete` exists); test coverage is UNKNOWN-by-absence and stated as such.

**Logic trace:** The README's command list is the repository's only statement of what the product does (README.md:5, OBSERVED). The argparse surface registers add, list, and done but not delete (main.py:20-22, OBSERVED), and the done handler prints "not implemented" rather than implementing the documented behavior (main.py:29-30, OBSERVED). Because the add command demonstrates a complete, working dispatch-to-domain-to-persistence path (main.py:24-25 → main.py:12-15), the missing behavior is not blocked by any structural limitation — it is simply unimplemented (DERIVED). Documented functionality with no corresponding implementation is the canonical definition of Ghost Features (weakness-types.md), and a product promise that does not exist in code is product_fog (SKILL.md ghost-feature reasoning). This evidence chain therefore yields: weakest boundary = README contract vs. command surface (Ghost Features), primary fog = product_fog.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L5
    quote: "Commands: `tasks add <title>`, `tasks list`, `tasks done <id>`, `tasks delete <id>`."
    supports_claim: "README documents a four-command product contract that includes done and delete"
  - file: main.py
    lines: L20-L22
    quote: |-
      add_p = sub.add_parser("add"); add_p.add_argument("title")
      sub.add_parser("list")
      done_p = sub.add_parser("done"); done_p.add_argument("id", type=int)
    supports_claim: "parser surface registers only add, list, done - no delete parser exists"
  - file: main.py
    lines: L29-L30
    quote: |-
      elif args.cmd == "done":
          print("not implemented")
    supports_claim: "done dispatch branch is a stub that never marks a task done or persists"
  - file: main.py
    lines: L24-L25
    quote: |-
      if args.cmd == "add":
          add(args.title)
    supports_claim: "add is fully wired end-to-end, proving the missing commands are unimplemented rather than structurally blocked"
  - file: main.py
    lines: L14
    quote: 'tasks.append({"id": len(tasks) + 1, "title": title, "done": False})'
    supports_claim: "task ids derive from list length, an implicit assumption the list never shrinks (latent collision risk)"
  - file: main.py
    lines: L10
    quote: 'return json.loads(STORE.read_text())'
    supports_claim: "store read has no error handling for corrupt tasks.json (secondary Zero Validation signal)"
```

## 9. Why this boundary matters

If the README contract vs. command surface gap stays weak, the CLI actively misleads its only audience: `tasks done 1` appears to succeed while doing nothing, and `tasks delete 1` fails outright with an argparse "invalid choice" error — a user-visible failure of half the documented product. Because there are no tests (`Pass D`: no test files exist), nothing in the repository detects the drift, so it will persist silently. The gap also blocks every valuable next move: writing tests requires deciding whether the README is the contract; packaging the `tasks` command requires knowing the real command set; and the id-collision flaw (`main.py:14`) only becomes reachable once `delete` is implemented. The boundary is small in code but central to the repository's entire purpose.

## 10. Candidate next steps

1. **Confirm the contract**: decide whether `README.md:5` is the intended product surface or a stale promise (the only entity that can settle this is the product owner/user — no intent artifact exists for this fixture). This gates everything else.
2. **Implement the missing commands**: wire `done` (`main.py:29-30`) to mark the task `done: true` and persist via `add()`'s write path, and add a `delete` parser + dispatch branch mirroring `main.py:20`/`main.py:24-25`.
3. **Pin the contract with tests**: add a small test suite (stdlib `unittest` or `pytest`) covering add/list/done/delete, missing-store startup, and corrupt-`tasks.json` handling — the first automated check this repository would have.
4. **Fix the id scheme when delete lands**: switch `len(tasks) + 1` (`main.py:14`) to `max(ids) + 1` in the same change that adds `delete`, so removal cannot produce duplicate ids.
5. **Reconcile the README in the same change**: update `README.md:5` (or document the unimplemented status) so docs and code cannot drift again; optionally add a `pyproject.toml` entry point so `tasks` is installable as documented.

## 11. Recommended next step

Confirm the README contract (next step 1) and, in one atomic change, implement `done` and `delete` per `README.md:5` plus a minimal test suite pinning all four commands. That single change converts the ghost features into real behavior, makes the contract executable, and creates the test scaffold every later improvement (packaging, id scheme, error handling) needs. If the contract confirmation instead reveals the README is stale, the same change becomes "update the README to the implemented surface" — either way the boundary is resolved in one step.

## 12. Recommended workflow

**`product-implementation-workflow`** (from `skills/workflow-planner/references/workflow-registry.yaml`, lines 644-714) in **`guided_execution`** mode (one of its `allowed_execution_modes`, registry lines 654-656).

Rationale: the primary fog is `product_fog` — promised features absent from the code — and product-implementation-workflow is the registry's workflow for product/feature problems: it aligns domain understanding (docs-aligner), researches/synthesizes the user need (discovery, opportunity-tree), then specifies and implements. Its discovery steps are precisely what is needed to resolve the open question in next step 1 (is the README's four-command surface the intended contract?) before implementing.

Why not the closest alternatives:
- **`implementation-workflow`** (registry lines 587-643): the generic architecture/code-design path; it lacks the discovery step that would confirm the product contract, and the problem here is a product promise, not code structure.
- **`product-discovery-sprint`** (registry lines 247-289): for vague product fog needing hypothesis generation from scratch; here the fog is concrete and documented (`README.md:5`), so a full discovery sprint is heavier than needed.
- **`docs-implementation-workflow`** (registry lines 812-847): docs_fog is only secondary; routing is driven by the primary fog type, and fixing the docs without the code would leave the ghost features in place.

Preconditions: none missing — the brief itself satisfies the `context_artifacts` input requirement (registry line 652). The workflow's guided_execution mode keeps human review gates between steps, appropriate for a diagnostic handoff.

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
evidence:
  - "README.md (line 5): documents four commands including tasks delete and tasks done, which are unimplemented in code"
  - "main.py (lines 20-22): parser surface registers only add, list, done - no delete parser"
  - "main.py (lines 29-30): done branch is a stub printing not implemented"
  - "main.py (lines 24-25): add path is fully wired, proving missing commands are unimplemented promises"
  - "main.py (line 14): ids assigned as len(tasks)+1 with no uniqueness guarantee once deletion exists"
  - "main.py (line 10): tasks.json read with no error handling; no test files exist anywhere in the repo"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:02:31Z"
immutable: true
```

## 14. Ready-to-copy prompt

Prompt for `workflow-planner` (or a downstream implementer):

> The repository `corpus/cli-app` (tasks-cli) has been diagnosed: primary fog is `product_fog` — the README (`README.md:5`) documents four commands (`tasks add`, `tasks list`, `tasks done`, `tasks delete`), but `main.py:20-22` registers only add/list/done, `main.py:29-30` stubs `done` with `print("not implemented")`, and `delete` has no parser or handler. The weakest boundary is classified as Ghost Features (documented functionality with no implementation). Recommended path: run `product-implementation-workflow` in `guided_execution` mode. First step: confirm with the user whether the README's four-command surface is the intended contract (no user-intent artifact exists for this fixture). Then implement `done` and `delete` per the confirmed contract, pin all four commands with a minimal test suite, switch the id scheme at `main.py:14` to `max(ids) + 1` in the same change, and reconcile `README.md:5` so docs and code cannot drift again. Do not implement anything before the contract confirmation.
