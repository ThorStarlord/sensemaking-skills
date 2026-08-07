# Repository Sensemaking Brief

## 1. Repository goal

`multi-executable` presents itself (README.md:1) as a small Python project with three
declared executables — a **server** (`python main.py`), a **CLI** (`python cli.py`),
and a **worker** (`python worker.py`) — that share a common database-connection
module (`db.py`). The repository goal as documented is therefore: "a runnable
multi-entry-point system (server + CLI + worker) over a shared database
connection." What each executable is *supposed to do* beyond that one line is
**UNKNOWN** — there is no spec, roadmap, issue tracker, or further documentation
anywhere in the repository (only README.md:1-3 exists as prose). The observable
code is a skeleton whose documented roles are not implemented (see Section 6).

## 2. Current shape

Inventory (OBSERVED, whole tree — no hidden files or subdirectories beyond
`scripts/`):

- `README.md` (3 lines) — the only documentation.
- `main.py` (8 lines) — declared "server".
- `cli.py` (3 lines) — declared "CLI".
- `worker.py` (8 lines) — declared "worker".
- `db.py` (2 lines) — shared connection module.
- `scripts/backfill.py` (1 line) — a fourth executable, **not** mentioned in the README.

**Runtime flow (as actually executed):**

- Startup: three entry points, each guarded by `if __name__ == '__main__':`
  (`main.py:7-8`, `worker.py:7-8`; `cli.py:3` runs unconditionally). The README
  documents launching them at README.md:3.
- "Server" flow: `python main.py` → `serve()` (main.py:3-5) → `get_conn()`
  (db.py:1-2) → `print('serving', conn)` (main.py:5) → process exits. No socket,
  no HTTP server import, no listen loop — the "server" never serves anything
  (OBSERVED: the only imports in main.py:1 are local; no server framework exists).
- "Worker" flow: `python worker.py` → `poll()` (worker.py:3-5) → `get_conn()`
  (db.py:1-2) → `print('polling')` (worker.py:5) → process exits after one print.
  No loop, no queue, no job scheduler (OBSERVED).
- "CLI" flow: `python cli.py` → builds an `ArgumentParser` with **zero arguments
  defined** (cli.py:2) and calls `p.parse_args()` (cli.py:3); the result is
  discarded. No subcommands, no dispatch, no action (OBSERVED).
- `scripts/backfill.py`: prints `'backfill'` (scripts/backfill.py:1) and exits;
  it never imports `db` and touches no data.

**Orchestration:** none — there is no controller; each entry point runs its own
one-function flow. Domain/core logic: none beyond the stub bodies above.

**State model:** the only state boundary is `db.py` — `get_conn()` returns the
literal string `'fake-conn'` (db.py:2). main.py:4 and worker.py:4 read it;
nothing writes it. There is no file, database, cache, queue, or environment
variable anywhere (OBSERVED — no other code exists). Whether a real database
was ever intended is **UNKNOWN**.

**External integrations:** none. The only imports in the entire repository are
local (`main.py:1`, `worker.py:1` → `db`). No dependency manifest exists at all
(no `pyproject.toml`, `setup.py`, or `requirements.txt`), so there are no
declared, used, runtime, test, optional, or dead dependencies — the dependency
class question is vacuous: the project depends on nothing external.

**Validation:** none anywhere (no test files, no CI config, no schemas, no input
validation — `cli.py:2-3` parses args and ignores them; Pass D found zero
validation surface).

**Where responsibility becomes unclear:** at the boundary between each documented
role (README.md:3) and its stub body. The files are named and launched as
"server"/"CLI"/"worker", but the implementations perform none of those roles —
the responsibility hand-off "role contract → behavior" is entirely absent.

## 3. Strong signals

- The three entry points are **documented with exact launch commands** in the
  README (README.md:3) — a rare clarity in skeleton repos; a new user can start
  all three processes immediately.
- The shared-connection design is coherent: both `main.py:1` and `worker.py:1`
  import the same `get_conn` from `db.py`, i.e. the intended "one DB layer,
  many consumers" shape is already sketched correctly.
- The code is trivially small and runs without errors (every path is a print),
  so the skeleton is a clean base — no dead code, no leftover vendored trees,
  no broken imports.
- Zero declared dependencies means zero dependency risk at this stage.

## 4. Missing pieces

- **Any real behavior** for the three documented roles: no serving logic
  (main.py:3-5), no CLI arguments/commands (cli.py:2-3), no polling loop
  (worker.py:3-5).
- **Real persistence:** `db.py:2` returns `'fake-conn'`; there is no database,
  schema, or connection lifecycle.
- **Tests and CI:** Pass D found none (no test files, no CI configuration).
- **A dependency manifest** (no `pyproject.toml`/`setup.py`/`requirements.txt`).
- **Documentation beyond one line:** no per-executable behavior spec, no
  architecture note; `scripts/backfill.py` is entirely undocumented (README.md:3
  names only three executables).
- **Validation:** no input validation (a CLI that parses and discards args,
  cli.py:2-3), no error handling.

## 5. Improvement opportunities

- Add a minimal manifest (`pyproject.toml`) so the project is installable and
  entry points are declared (would also make the "server/CLI/worker" roles
  machine-visible via `[project.scripts]`).
- Add a one-page per-executable behavior spec, starting from the README's three
  roles (README.md:3) — this is the missing contract (see Section 6).
- Add smoke tests asserting each entry point's current observable behavior
  (e.g. `serve()` prints) before any real implementation lands, so the skeleton
  gains a regression net.
- Replace `db.py:2`'s literal stub with a connection interface + fake/test
  double, decoupling the persistence decision from entry-point work.
- Document `scripts/backfill.py` or delete it; currently it is an undocumented
  fourth executable (scripts/backfill.py:1 vs README.md:3).

## 6. Weakest boundary

Candidate generation (scored per SKILL.md "Weakest Boundary Reasoning"):

| Candidate | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|
| C1: Documented roles vs stub implementations (README.md:3 vs main.py:3-5, cli.py:1-3, worker.py:3-5) | strong | high | high (all 3 entry points) | high | high | low |
| C2: Fake persistence boundary (db.py:2 `'fake-conn'`) | strong | medium | high (all consumers) | medium | high (any DB-backed work) | medium |
| C3: Zero validation anywhere (no tests/CI/input checks) | strong (absence observed) | medium | medium | medium | medium | low |
| C4: Undocumented fourth executable (scripts/backfill.py:1) | strong | low | low | low | low | low |

Selection: **C1**. It has the strongest combination of consequence (the product
does none of what its own README declares), direct evidence (stub bodies are
fully observable), centrality to the repository goal (the goal *is* the three
roles), and downstream blocking (every other improvement — tests, real db,
validation — presupposes deciding what each executable should actually do). C2
is real but secondary: the fake connection only matters once real logic exists.
C3 is a symptom of the skeleton, not its root defect. C4 is a minor gap.

```text
Boundary: the contract between the documented executable roles (README.md:3)
and the implementations behind them (main.py:3-5, cli.py:1-3, worker.py:3-5).
Observed contract: README.md:3 declares "Server: `python main.py`; CLI:
`python cli.py`; worker: `python worker.py`." — three products with distinct
roles, sharing db.py.
Observed violation or uncertainty: none of the three roles is implemented.
main.py:3-5 ("server") prints once and exits with no socket/HTTP/loop;
cli.py:1-3 defines zero arguments and performs no action after parse_args();
worker.py:3-5 prints 'polling' once with no loop/queue. The only state source,
db.py:2, returns the literal 'fake-conn'.
Evidence: README.md:3; main.py:1-8; cli.py:1-3; worker.py:1-8; db.py:1-2;
scripts/backfill.py:1 (all OBSERVED).
Weakness type: Ghost Features
Logic trace: README.md:3 advertises a server, a CLI, and a worker as the
repository's deliverable surface, and main.py:1/worker.py:1 show the intended
shared db layer exists. Opening those entry points shows the advertised
behavior is absent: main.py:3-5 contains only a print, cli.py:2-3 defines an
ArgumentParser with no arguments and discards the parse result, and
worker.py:3-5 prints once instead of polling. There is no manifest, spec, or
test that could make any of these behaviors real elsewhere (Pass A/Pass D
found none). Therefore the documented functionality (server/CLI/worker roles)
has no reachable implementation — the definition of Ghost Features
(weakness-types.md:7). The defect is the promise (product contract), not the
docs: the README's launch commands are accurate, so this is not docs_fog.
Failure consequence: anyone launching the "server" or "worker" gets a process
that prints and exits; the "CLI" accepts and ignores all input; the product
surface is 100% non-functional while appearing runnable, so every downstream
effort (tests, persistence, deployment) starts from a false premise.
Confidence: high — the stub bodies are directly observable and the README
contract is unambiguous. What would raise it further: a spec or issue tracker
stating the intended behavior (none exists; UNKNOWN whether a real DB or real
server was ever planned).
Alternatives considered: C2 (fake persistence, db.py:2) — real evidence but
secondary: the fake connection harms nothing until real logic exists; C3
(zero validation) — absence is observed but it is a consequence of the
skeleton, and adding tests before deciding the roles would test the wrong
contract; C4 (undocumented scripts/backfill.py) — low blast radius, does not
block the repository goal. C1 dominates all three on consequence, relevance,
and blocking effect.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)

**primary_fog_type: product_fog**

- **ui_fog — rejected:** the UI Fog decision tree (ui-fog-signals.md:156-158)
  says no frontend code → not ui_fog. There is no HTML/CSS/JS/React/Vue in the
  repository (Pass A inventory).
- **docs_fog — rejected:** the README does not misdescribe mechanics; the launch
  commands at README.md:3 work exactly as written. The mismatch is not stale or
  missing documentation, it is absent functionality behind documented roles.
- **architecture_fog — secondary, not primary:** the structure is a clean,
  trivial skeleton; no module-boundary confusion, coupling, or lifecycle
  ambiguity prevents implementation — there simply is no implementation. The
  fake state boundary (db.py:2) is a stub, not a structural defect.
- **product_fog — primary:** per the ghost-feature reasoning in SKILL.md
  (fog-classification section), when the README advertises deliverables
  (server/CLI/worker at README.md:3) and the code does not implement them
  (main.py:3-5, cli.py:1-3, worker.py:3-5), the defect is the promise — the
  product contract is unfulfilled. The classification is grounded in
  OBSERVED evidence, not difficulty.

This is a no-user-intent fixture run: `user_implied_fog_type: unknown`,
`diagnosis_conflict: false` (GAP-8). `escalation_recommended: false` — the
evidence is direct and unambiguous, so no escalation is warranted.

## 7. Evidence

All claims in this brief trace to files actually opened:

- `README.md:3` — declares the three roles ("Server", "CLI", "worker") and
  their launch commands; the only product documentation in the repo.
- `main.py:3-5` — the "server" body: `serve()` only prints; no server framework
  is imported anywhere (main.py:1).
- `cli.py:1-3` — the CLI defines an ArgumentParser with no arguments and
  discards the parse result; no action, no dispatch.
- `worker.py:3-5` — `poll()` prints `'polling'` once and the process exits; no
  loop or queue.
- `db.py:2` — `get_conn()` returns the literal `'fake-conn'`; the only state
  boundary in the repository.
- `scripts/backfill.py:1` — an undocumented fourth executable that only prints.

The absence claims (no tests, no manifest, no CI, no docs beyond the README)
are OBSERVED via the complete recursive inventory of the fixture directory,
which contains exactly these six files and nothing else.

**Logic trace:** The README (README.md:3) promises three distinct executable
roles; the code behind each role (main.py:3-5, cli.py:1-3, worker.py:3-5)
implements none of them — each is a print or a discarded parse. The single
shared dependency, db.py:2, is a literal stub, so no hidden layer supplies the
missing behavior. Because the documented surface has no reachable
implementation, the weakest boundary is Ghost Features (weakness-types.md:7),
and because the defect lives in the unfulfilled product promise rather than in
the (accurate) documentation, the primary fog is `product_fog`.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Server: `python main.py`; CLI: `python cli.py`; worker: `python worker.py`."
    supports_claim: "README declares three executables with product roles (server, CLI, worker) as the repository's deliverable surface."
  - file: main.py
    lines: L3-L5
    quote: "def serve():\n    conn = get_conn()\n    print('serving', conn)"
    supports_claim: "The 'server' entry point only prints once and exits; no socket, HTTP, or serving loop exists."
  - file: cli.py
    lines: L1-L3
    quote: "import argparse\np = argparse.ArgumentParser()\np.parse_args()"
    supports_claim: "The 'CLI' defines zero arguments and performs no action after parsing; the result is discarded."
  - file: worker.py
    lines: L3-L5
    quote: "def poll():\n    conn = get_conn()\n    print('polling')"
    supports_claim: "The 'worker' polls once and exits; no loop, queue, or job handling exists."
  - file: db.py
    lines: L1-L2
    quote: "def get_conn():\n    return 'fake-conn'"
    supports_claim: "The persistence boundary is a stub returning a literal string; no real connection exists."
  - file: scripts/backfill.py
    lines: L1
    quote: "print('backfill')"
    supports_claim: "A fourth executable that is undocumented in README.md:3 and never touches the database."
```

## 9. Why this boundary matters

The repository's entire advertised value is the three roles at README.md:3.
Today, all three are non-functional in the same way: they run, print, and exit.
That is worse than an obviously broken repo because it *looks* runnable — a
human or agent launching `python main.py` gets a process that exits 0 with
`serving fake-conn` and may assume a server exists. Every subsequent effort is
built on that false premise: tests would assert the wrong behavior, a real
database would be wired into nothing, and the CLI would keep silently ignoring
its input. The fake state boundary (db.py:2) compounds this by making the
"database" appear present. Until the role contract is decided and implemented,
there is no stable foundation for any other improvement; the repository
cannot serve any real purpose.

## 10. Candidate next steps

1. **Write the role contract:** a one-paragraph-per-executable spec (what the
   server serves, what the CLI commands are, what the worker polls and with
   what cadence), derived from README.md:3's roles. This is the missing
   contract the stubs are waiting on.
2. **Run product discovery on the intended behavior** (via
   product-implementation-workflow) to resolve the UNKNOWNs (intended features,
   real DB or not) before any implementation.
3. **Add smoke tests for current behavior** (each entry point prints and exits
   0) so the skeleton gains a regression net that survives the rewrite.
4. **Replace db.py:2 with a connection interface + test double**, decoupling
   the persistence decision from entry-point work.
5. **Document or delete `scripts/backfill.py`** (scripts/backfill.py:1), and add
   a manifest so the three entry points are declared installably.

## 11. Recommended next step

**Step 1 — write the role contract:** produce a short, concrete spec for each
of the three declared executables (server: what it serves and on what; CLI:
what commands/arguments it accepts; worker: what it polls and how often),
grounded in the roles already named at README.md:3. It is the smallest action
with the highest leverage: it converts the three Ghost Features into testable
requirements, unblocks every other candidate step, and requires no code
changes. Any larger move (implementation, tests, real persistence) is wasted
until this contract exists.

## 12. Recommended workflow

**`product-implementation-workflow`** (workflow-registry.yaml:644-714) with
**`guided_execution`** (one of its allowed_execution_modes,
workflow-registry.yaml:654-656).

Why this workflow: the primary fog is `product_fog` — the defect is an
unfulfilled product contract (README.md:3 promises roles the code does not
implement). product-implementation-workflow is the registry entry for
"product/feature problems": it aligns domain understanding, researches user
needs (discovery step, workflow-registry.yaml:667-672), synthesizes
opportunities, produces a spec, and only then implements — exactly the
discovery-first shape the repo needs to resolve the UNKNOWNs (intended server
behavior, real database).

Why not the alternatives: `architecture-implementation-workflow`
(workflow-registry.yaml:848-904) fits refactoring/module-boundary problems —
not present here, since the skeleton's structure is clean and nothing prevents
implementation; `docs-implementation-workflow` (workflow-registry.yaml:812-847)
fits documentation gaps — but the README is accurate, so docs are not the
defect; `ui-diagnostic-workflow` (workflow-registry.yaml:715-747) is excluded
by the UI decision tree (no frontend code, ui-fog-signals.md:156-158);
`implementation-workflow` (workflow-registry.yaml:587-643) is the generic
architecture/code-design default and skips the discovery step this repo's
UNKNOWNs require.

Preconditions: none block the workflow's first steps, but step 1-2 (domain
alignment + discovery, workflow-registry.yaml:659-672) will need an owner who
can state the intended product behavior — without one, the discovery step
cannot resolve the UNKNOWNs this brief flags.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-executable
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (line 3): declares Server/CLI/worker entry points as the deliverable surface"
  - "main.py (lines 3-5): serve() only prints 'serving'; no server behavior"
  - "cli.py (lines 1-3): ArgumentParser with no arguments; parse result discarded"
  - "worker.py (lines 3-5): poll() prints 'polling' once; no loop or queue"
  - "db.py (line 2): get_conn() returns literal 'fake-conn'; persistence is a stub"
  - "scripts/backfill.py (line 1): undocumented fourth executable, prints only"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-10T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

```
Workflow: product-implementation-workflow (guided_execution)
Context artifact: repository_sensemaking_brief for target repo
  experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-executable
  (primary_fog_type: product_fog; weakest boundary: Ghost Features —
  documented server/CLI/worker roles at README.md:3 have no reachable
  implementation: main.py:3-5 prints once, cli.py:1-3 discards parse_args(),
  worker.py:3-5 prints once, db.py:2 returns 'fake-conn').

Run the domain-alignment and discovery steps first. The open questions the
brief cannot answer (UNKNOWN): what the server should actually serve, what
commands/arguments the CLI should accept, what the worker should poll and on
what cadence, and whether a real database was ever intended. Deliver a role
contract (one short spec per executable) as the first concrete output; do not
implement or refactor code until that contract is approved. Then proceed
through opportunity mapping, PRD, issue decomposition, and TDD implementation
per the workflow's steps, with human review at each gate.
```
