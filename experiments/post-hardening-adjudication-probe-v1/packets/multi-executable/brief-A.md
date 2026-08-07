# Repository Sensemaking Brief — multi-executable

## 1. Repository goal

The repository is a minimal multi-entry-point Python application skeleton. Its only
documentation, `README.md:1` ("# multi-exec") and `README.md:3`, presents the repo as three
runnable surfaces sharing one codebase: a server (`python main.py`), a CLI (`python cli.py`),
and a worker (`python worker.py`) (OBSERVED: `README.md:3`). No feature list, roadmap, or
product contract exists beyond those three commands, so the repo's implied goal is to
demonstrate/serve as a starting point for a system with several independent executables over a
common persistence module (`db.py`). Nothing in the repository promises any specific product
behavior (INFERRED from the absence of any other documentation; UNKNOWN beyond that).

## 2. Current shape

**Inventory (OBSERVED, recursive root listing).** Six files, no subdirectories other than
`scripts/`:

- `README.md` (3 lines) — one-line usage doc.
- `main.py` (8 lines) — server entry point.
- `cli.py` (3 lines) — CLI entry point.
- `worker.py` (8 lines) — worker entry point.
- `db.py` (2 lines) — shared "database" module.
- `scripts/backfill.py` (1 line) — a fourth executable script.

Absent from the root inventory (OBSERVED absence): any packaging manifest
(`pyproject.toml`, `setup.py`, `requirements.txt`), any test directory/file, any CI
configuration, any docs directory, any lockfile. The repo has no declared dependencies at all —
there is no manifest in which anything could be declared (OBSERVED).

**Runtime flow, entry point by entry point.**

- **Server** — startup: `python main.py`; `main.py:7` (`if __name__ == '__main__':`) invokes
  `serve()` at `main.py:8`. Orchestration: none — `serve()` (`main.py:3-5`) is the entire flow:
  it calls `get_conn()` (`main.py:4`) and prints `'serving'` (`main.py:5`). Domain/core logic:
  none. Persistence: the only state boundary in the system is `db.py:2`, which returns the
  hardcoded string `'fake-conn'` — no database, file, cache, queue, or environment state exists
  (OBSERVED: `db.py:1-2`). External integrations: none. Background work: none. Output boundary:
  a single stdout print (`main.py:5`).
- **CLI** — startup: `python cli.py`; `cli.py:1` imports `argparse`, `cli.py:2` constructs an
  `ArgumentParser`, `cli.py:3` calls `p.parse_args()`. There is no subcommand, no argument
  definition, no action, no output, and no exit-code logic: the entry point parses an empty
  argument surface and terminates. This is a **stubbed runtime entry point** (OBSERVED:
  `cli.py:1-3`).
- **Worker** — startup: `python worker.py`; `worker.py:7-8` invokes `poll()` (`worker.py:3-5`),
  which calls `get_conn()` (`worker.py:4`) and prints `'polling'` (`worker.py:5`). Despite the
  name, `poll()` executes exactly once and exits — there is no loop, no queue, no scheduler, no
  sleep (OBSERVED: `worker.py:3-5`). Background work: none that actually runs repeatedly.
- **Backfill script** — `scripts/backfill.py:1` (`print('backfill')`) is a fourth executable
  surface that executes and prints once. It is **not mentioned anywhere in the README**
  (OBSERVED contrast: `scripts/backfill.py:1` vs `README.md:3`) and is not imported by any
  module (OBSERVED: no `import backfill` in any file) — an unwired, undocumented entry point.

**Dependency semantics.** `db.py` is `used` at runtime by two entry points: imported at
`main.py:1` and `worker.py:1`, and its function is actually called on the execution path at
`main.py:4` and `worker.py:4` (runtime class, DERIVED from the import + call sites). `argparse`
(`cli.py:1`) is the only non-local import; it is `used` on the CLI execution path (`cli.py:3`).
No dependency is `declared` (no manifest exists), none is `optional`, and none is `dead` in the
manifest sense — the only "dead" surface is the CLI's absent command set, which is a missing
implementation rather than an unused dependency.

**State model.** The single state boundary is the fake connection string in `db.py:2`; the only
reader is `get_conn()` itself, and its only consumers are `main.py:4` and `worker.py:4`
(OBSERVED). No code writes any state. There is no state to corrupt, but also no state that can
carry real behavior.

**Boundary model.** The boundaries present are: CLI → handler (absent — there is no handler),
HTTP → application (absent — the "server" never binds a socket or serves a request),
domain → persistence (present but fake: `main.py:4`/`worker.py:4` → `db.py:2`), and
entry-point → docs (README → code). **Where validation happens: nowhere.** No argument
validation, no input checks, no tests, no schema, no authorization boundary, no error handling
anywhere in the six files (OBSERVED). **Where responsibility becomes unclear:** the CLI's
purpose (what commands it should expose), the worker's polling contract (what it should poll and
how often), and whether `db.py` is a deliberate seam or an unfinished placeholder — nothing
documents any of these (UNKNOWN; only the README's three command names are stated).

## 3. Strong signals

1. **The README's documented commands actually run.** `README.md:3` names three commands; each
   corresponding module has a working `if __name__ == '__main__'` guard and executes without
   error (OBSERVED: `main.py:7-8`, `cli.py:2-3`, `worker.py:7-8`). Docs-to-code agreement holds
   for everything the README claims.
2. **A clean, consistent layering seam.** Both the server and the worker reach persistence
   through the same single function `get_conn()` (`main.py:1,4`, `worker.py:1,4`), so replacing
   the fake connection with a real adapter is a one-file change — a good seam to build on
   (DERIVED from the import/call sites).
3. **Conventional, minimal Python entry-point structure.** Each executable is its own module
   with a standard guard (`main.py:7`, `worker.py:7`); there is no framework lock-in, no
   generated code, no vendor tree, and no hidden complexity (OBSERVED).
4. **Zero incidental cruft.** No build artifacts, snapshots, or duplicated generated sources —
   the repository is small enough to reason about completely (OBSERVED inventory).

## 4. Missing pieces

1. **CLI functionality.** The documented CLI (`README.md:3`) has no commands: `cli.py:2-3`
   contains only parser construction and `parse_args()` (OBSERVED). A user invoking `python
   cli.py` gets exit code 0 and no behavior.
2. **Real persistence.** `db.py:2` returns `'fake-conn'` — no database, no schema, no storage
   (OBSERVED). The server "serves" a fake connection string and the worker "polls" nothing.
3. **A worker loop.** `worker.py:3-5` prints once and exits; there is no polling loop, queue
   integration, or scheduling (OBSERVED).
4. **Documentation of the fourth entry point.** `scripts/backfill.py:1` exists but `README.md:3`
   names only three commands (OBSERVED contrast) — the entry-point inventory is incomplete.
5. **Any validation or test surface.** No tests, no packaging manifest, no CI, no argument or
   input validation in any file (OBSERVED absence in root inventory). Nothing checks that any of
   the four entry points works.

## 5. Improvement opportunities

- Define the CLI's command surface (even a `--help`-only contract with one placeholder command)
  so `python cli.py` has observable behavior; this is the highest-leverage refinement but is an
  implementation step, out of scope here.
- Decide and document whether `db.py` is a placeholder seam or the final persistence contract,
  then add a minimal interface doc or type stub (`db.py:1-2`).
- Add a smoke test that spawns each of the four entry points and asserts expected stdout, plus a
  packaging manifest (`pyproject.toml`) declaring entry points — this converts the current
  implicit run contract into a checked one.
- Add `scripts/backfill.py` to `README.md:3` so the documented entry-point inventory matches the
  code (small, cheap, removes a docs gap).
- Give `worker.py:3-5` a real loop boundary (interval, stop condition) so "worker" means what it
  says.

## 6. Weakest boundary

**Candidate generation (2-5 candidates, scored).**

```yaml
boundary: C1 — Documented CLI entry point with no implemented commands
  (cli.py:2-3; documented at README.md:3)
evidence_strength: strong   # both files directly inspected; the README names the CLI, cli.py shows the stub
severity: high              # a documented command that silently does nothing
blast_radius: medium        # one of three documented surfaces; does not affect server/worker
goal_relevance: high        # the CLI is one of exactly three surfaces the README promises
downstream_blocking_effect: high   # any CLI feature work starts from a nonexistent command contract
uncertainty: low

boundary: C2 — Fake persistence layer (db.py:1-2), consumed by server and worker
  (main.py:4, worker.py:4)
evidence_strength: strong
severity: high              # the system cannot persist anything
blast_radius: high          # both server and worker depend on get_conn()
goal_relevance: medium      # the README never promises persistence, so no documented contract is violated
downstream_blocking_effect: medium
uncertainty: medium         # whether db.py is a deliberate seam or unfinished is undocumented

boundary: C3 — Undocumented fourth entry point (scripts/backfill.py:1 vs README.md:3)
evidence_strength: strong
severity: low               # a one-line print script; running it is harmless but useless
blast_radius: low
goal_relevance: low
downstream_blocking_effect: low
uncertainty: low

boundary: C4 — No tests, manifest, or validation for any entry point
  (OBSERVED absence across the whole root inventory)
evidence_strength: medium   # absence-based evidence
severity: medium
blast_radius: high          # whole repo
goal_relevance: medium
downstream_blocking_effect: medium
uncertainty: medium
```

**Selection.** C1 wins: it combines the strongest direct evidence (a documented surface
`README.md:3` whose implementation `cli.py:1-3` is verifiably empty of functionality), high
severity (the documented CLI does nothing), high centrality to the repo's only stated goal (the
three README surfaces), and it blocks valuable downstream work (any CLI feature or contract
work). C2 loses on goal_relevance and uncertainty — no documented contract promises a real
database, so the "violation" is inferred, not observed; C3 is real but low-consequence; C4 is
real but absence-based and secondary to the fact that the entry points themselves are stubs.
C1 is not the easiest or most dramatic problem — it is the one with the strongest evidence,
highest goal centrality, and clearest downstream blocking effect.

```text
Boundary:
  The CLI entry point — the boundary between the documented command surface (README.md:3,
  "CLI: `python cli.py`") and any implemented handler behavior (cli.py).

Observed contract:
  README.md:3 presents the CLI as a runnable, functional surface of the repository:
  "Server: `python main.py`; CLI: `python cli.py`; worker: `python worker.py`."

Observed violation or uncertainty:
  cli.py:1-3 is the entire reachable implementation of that surface: it imports argparse,
  constructs an ArgumentParser, and calls parse_args(). There are no subcommands, no arguments
  defined, no actions, no output, and no error paths. The entry point runs (exit 0) but exposes
  no CLI functionality whatsoever.

Evidence:
  README.md:3 (documented surface); cli.py:1-3 (empty command surface); contrast with
  main.py:3-5 and worker.py:3-5, which each perform at least one action, showing the system
  otherwise runs.

Weakness type:
  Ghost Features

Logic trace:
  README.md:3 documents the CLI as a live, runnable surface of the repository (OBSERVED).
  cli.py:1-3 shows that the reachable implementation of that surface consists solely of
  argparse setup — no command, no action, no output (OBSERVED). Under the GAP-6 taxonomy
  constraint, Ghost Features is the right weakness type ONLY for a documented surface whose
  promised functionality has no reachable implementation: the CLI's promised functionality
  (commands) has no reachable implementation anywhere — cli.py runs but implements nothing, and
  no other module provides CLI behavior (OBSERVED across all six files). This is not dead code
  masquerading as core, and it is not an unwired module: it is a documented surface with an
  empty implementation. Because the entry point itself runs within an otherwise-running system
  (the server at main.py:7-8 and the worker at worker.py:7-8 both execute), the defect is a
  stubbed RUNTIME ENTRY POINT, which the skill classifies as structural — so the fog type is
  architecture_fog (not product_fog, which would require a promised surface with no
  implementation at all; not docs_fog, since the README accurately describes what runs).

Failure consequence:
  A user following the README runs `python cli.py` and receives exit code 0 with no behavior,
  no feedback, and no discoverable commands — the documented surface silently lies. Any future
  CLI work must first reverse-engineer or invent the command contract from nothing, and the
  pattern invites every other entry point to degrade into a silent no-op the same way. Because
  Ghost Features is a high-risk claim category (D5), a substantive human audit is required
  before final approval of this brief.

Confidence:
  high — both evidence files were directly inspected and the claims are fully observed; a
  higher-confidence confirmation would come from an issue tracker or spec stating what CLI
  commands were intended (currently UNKNOWN).

Alternatives considered:
  - C2 (fake persistence, db.py:1-2): higher blast radius, but the README never promises
    persistence, so the "violation" is inferred rather than observed; medium uncertainty
    disqualified it against C1's low uncertainty.
  - C3 (undocumented scripts/backfill.py): observed but low severity and blast radius.
  - C4 (no tests/manifest/validation): real and repo-wide, but absence-based and secondary to
    the stubbed surfaces themselves.
```

## 6.5. Problem classification (fog type)

The primary fog type is **architecture_fog**. The frontend tie-break does not apply: there is no
frontend code of any kind in the root inventory (OBSERVED), so `ui_fog` is excluded. `product_fog`
is excluded because no README/roadmap promise has zero implementation — every documented command
runs; the defect is that one of them runs empty. `docs_fog` is secondary at most: the README
accurately describes what runs (contrast-pass found no misdescription, only the omission of
`scripts/backfill.py:1`). The primary defect is structural: a stubbed runtime entry point
(`cli.py:2-3`) inside an otherwise-running system, plus a fake persistence boundary (`db.py:2`)
and a one-shot worker (`worker.py:3-5`) — incomplete structure, not a broken product promise and
not stale documentation. Secondary fog: `docs_fog` (the undocumented `scripts/backfill.py`
entry point), recorded here but not driving routing.

## 7. Evidence

The diagnosis rests on direct inspection of all six files in the repository. `README.md:3`
documents exactly three entry points ("Server: `python main.py`; CLI: `python cli.py`; worker:
`python worker.py`."). `cli.py:2-3` shows the CLI's entire implementation is parser construction
plus `parse_args()` with no commands. Contrast: `main.py:3-5` (`serve()` acquires a connection
and prints `'serving'`) and `worker.py:3-5` (`poll()` prints `'polling'`) each perform an action,
proving the rest of the system executes. `db.py:2` returns the literal `'fake-conn'`, which is
the system's only state boundary, consumed at `main.py:4` and `worker.py:4`. `scripts/backfill.py:1`
is a fourth executable that the README never mentions. The root inventory shows no manifest, no
tests, and no CI (OBSERVED absence).

Logic trace: the README (README.md:3) is the only contract in the repository, and it promises a
CLI. The CLI's reachable implementation (cli.py:1-3) contains no functionality, while the other
two documented surfaces (main.py:3-5, worker.py:3-5) demonstrably execute — so the CLI is a
stubbed runtime entry point within an otherwise-running system, not a feature with no code at
all. A documented surface with no reachable implementation of its promised functionality is
Ghost Features per the GAP-6 taxonomy, and a stubbed runtime entry point is structural, which
classifies the primary fog as architecture_fog rather than product_fog or docs_fog.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Server: `python main.py`; CLI: `python cli.py`; worker: `python worker.py`."
    supports_claim: "The README documents the CLI as a live, runnable surface — the documented contract the weakest boundary violates."
  - file: cli.py
    lines: L1-L3
    quote: "import argparse\np = argparse.ArgumentParser()\np.parse_args()"
    supports_claim: "The CLI's entire reachable implementation is argparse setup with no commands, actions, or output — a stubbed runtime entry point."
  - file: main.py
    lines: L3-L8
    quote: "def serve():\n    conn = get_conn()\n    print('serving', conn)\n\nif __name__ == '__main__':\n    serve()"
    supports_claim: "The server entry point executes a real action, showing the system otherwise runs (contrast with the CLI stub)."
  - file: worker.py
    lines: L3-L8
    quote: "def poll():\n    conn = get_conn()\n    print('polling')\n\nif __name__ == '__main__':\n    poll()"
    supports_claim: "The worker executes once and exits — no polling loop — a second instance of structural incompleteness."
  - file: db.py
    lines: L1-L2
    quote: "def get_conn():\n    return 'fake-conn'"
    supports_claim: "The system's only state boundary returns a hardcoded fake connection; no real persistence exists."
  - file: scripts/backfill.py
    lines: L1
    quote: "print('backfill')"
    supports_claim: "A fourth executable entry point exists that README.md:3 never documents."
```

## 9. Why this boundary matters

If the CLI stub remains, the repository's only documented contract is one-third false: a user or
an automated caller following `README.md:3` gets a command that succeeds silently and does
nothing, which is worse than a failing command because nothing signals the gap. Downstream, any
CLI feature work (the most likely next increment for a multi-executable repo) must start from a
nonexistent contract, and the same stub pattern is already visible in `worker.py:3-5` (one-shot
"poll") and `scripts/backfill.py:1` — so the CLI is the leading edge of a systemic incompleteness
that, left alone, produces a repository where every surface prints a message and no surface
does work. The fake persistence (`db.py:2`) compounds this: even a completed CLI could not do
anything real until the state boundary is replaced.

## 10. Candidate next steps

1. **Define the CLI command contract** — write down (in the repo) what commands `python cli.py`
   should expose, then implement at least one real command; this directly closes the weakest
   boundary.
2. **Replace the fake persistence seam** — implement a real `get_conn()` (or an adapter interface
   behind it) so server/worker/CLI operate on real state.
3. **Add a smoke-test harness** — run each of the four entry points and assert expected stdout,
   so the entry-point contract becomes checked rather than implicit.
4. **Document all four entry points** — extend `README.md:3` to include `scripts/backfill.py`,
   and state what each surface is supposed to do (removes the secondary docs_fog gap).
5. **Give the worker a real loop contract** — define interval/stop conditions so "worker" is
   honest (secondary to 1-3).

## 11. Recommended next step

Step 1: define and implement the CLI command contract. It is the smallest action that directly
resolves the weakest boundary (documented surface with no functionality), it has the strongest
evidence behind it, and it unblocks the most valuable downstream work — every other surface
(worker loop, backfill, persistence) becomes easier to specify once the repo has one honest,
working command surface to pattern-match against.

## 12. Recommended workflow

Recommend **architecture-implementation-workflow** from the canonical registry
(`skills/workflow-planner/references/workflow-registry.yaml`, id at lines 848-904), in
**guided_execution** mode (one of its `allowed_execution_modes`, registry lines 858-861). The
primary fog is `architecture_fog` (stubbed runtime entry point, structural incompleteness), and
this workflow is the registry's designated path for architecture/refactoring problems: it aligns
domain understanding, produces an architecture/refactoring spec, decomposes into issues, and
implements via TDD. The closest alternatives were rejected: `ui-implementation-workflow` and
`product-implementation-workflow` because the defect is neither screen/flow design nor a product
contract gap; `docs-implementation-workflow` because the README is accurate and the docs gap is
secondary; `implementation-workflow` (the generic default) because the registry offers a
specialized architecture variant that fits better. `plan_only` is not offered for
architecture-implementation-workflow, and inventing it is forbidden (GAP-7); recommending the
workflow with an allowed mode does not execute it — the No Implementation boundary of this
diagnostic stays intact, and execution happens later under the runtime's own authorization.
Escalation is not needed: the evidence is direct and consistent (no user intent exists to
conflict with). Precondition before the workflow can run: the D5 substantive human audit of the
Ghost Features claim.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-executable
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: none (standalone fixture run; no user intent artifact exists)
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (L3): documents three entry points (server, CLI, worker); the CLI surface is the documented contract"
  - "cli.py (L1-L3): CLI entry point parses argv with no commands, actions, or output — stubbed runtime entry point"
  - "main.py (L3-L8): server entry point executes (get_conn + print), showing the system otherwise runs"
  - "worker.py (L3-L8): worker prints once and exits; no polling loop"
  - "db.py (L1-L2): get_conn() returns hardcoded 'fake-conn'; no real persistence"
  - "scripts/backfill.py (L1): fourth executable entry point undocumented in README.md:3"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features - documented CLI entry point (README.md:3) with no implemented commands (cli.py:2-3)
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-06-18T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

```text
Workflow-planner: route a repository sensemaking brief for
experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-executable.

primary_fog_type: architecture_fog
weakest_boundary: Ghost Features — documented CLI entry point (README.md:3) whose
  reachable implementation (cli.py:2-3) contains no commands; a stubbed runtime entry
  point inside an otherwise-running system. Supporting evidence: db.py:2 returns
  'fake-conn' (no real persistence), worker.py:3-5 is a one-shot print (no poll loop),
  scripts/backfill.py:1 is an undocumented fourth entry point.
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
required_inputs: user_intent, repository_state (repository_state = the six files of the
  target repo; user_intent = define and implement the CLI command contract first, per
  Section 11).
Preconditions: a substantive human audit of the Ghost Features classification is required
  before final approval (D5). Do not execute the workflow from this diagnostic; produce
  the orchestration plan only.
```
