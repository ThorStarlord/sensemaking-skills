# Repository Sensemaking Brief — backend-service

## 1. Repository goal
A minimal FastAPI REST service for storing and retrieving text notes ("notes-service"). The README states the entire product contract in one line: `REST API for notes. \`uvicorn app.main:app\`.` (README.md:3). No user intent artifact was provided for this run (standalone fixture execution), so intent-aware fields are set to `unknown` / `false` per the no-user-intent rule; nothing in the repository advertises goals beyond the two implemented endpoints (create + read).

## 2. Current shape
The repository is 7 files: `README.md`, `requirements.txt`, and an `app/` package (`__init__.py` empty, `main.py`, `db.py`, `models.py`, `routers/notes.py`). There are no tests, no CI configuration, no build metadata (no `pyproject.toml`/`setup.py`), no Docker/deployment files, and no documentation directory (OBSERVED over the complete inventory).

**Runtime flow (reconstructed from files actually opened):**
- **Startup**: the documented launch is `uvicorn app.main:app` (README.md:3). Importing `app.main` executes the module-level `app = create_app()` (app/main.py:9), which builds `FastAPI()` and registers the notes router via `app.include_router(notes.router)` (app/main.py:5-6).
- **Orchestration**: FastAPI dispatches HTTP requests to the router `APIRouter(prefix="/notes")` (app/routers/notes.py:5). The two entry points are `POST /notes/` → `create` (notes.py:7-12) and `GET /notes/{note_id}` → `read` (notes.py:14-20). No CLI, workers, jobs, or plugin registration exist.
- **Domain/core logic**: there is no service layer; the router handlers are the entire domain. The only domain type is `Note` with a single field `body: str` (app/models.py:3-4).
- **Persistence/state**: every handler call opens a new SQLite connection to `Path("notes.db")` (app/db.py:5) — a **relative path resolved against the process working directory**. The schema is created inline on every connection via `CREATE TABLE IF NOT EXISTS` (app/db.py:6). `create` writes (notes.py:10-11); `read` reads (notes.py:17). The state boundary is the filesystem, and its location is determined by CWD — nowhere is it configured, validated, or documented (OBSERVED: no config module, no environment-variable reads, no CLI argument in any of the 7 files).
- **External integrations**: none. No HTTP clients, message queues, or third-party services.
- **Background work**: none.
- **Output boundary**: JSON dicts (`{"id": ...}` notes.py:12, `{"body": ...}` notes.py:20) and HTTP errors (`HTTPException(404)` notes.py:19).

**Dependency semantics (classes, not conflated):**
- `fastapi` — **declared** (requirements.txt:1) and **used** (app/main.py:1, app/routers/notes.py:1).
- `uvicorn` — **declared** (requirements.txt:2) and **runtime** as the process launcher invoked by name (`uvicorn app.main:app`, README.md:3); it is never imported by code — an entry point executed without being imported, not a dead dependency.
- `pydantic` — **used** (app/models.py:1 `from pydantic import BaseModel`) but **NOT declared** in requirements.txt (L1-L2). It works today only because FastAPI pulls it in transitively; the manifest does not promise the contract the code imports (used-but-undeclared → implicit dependency).
- `sqlite3`, `pathlib` — standard library, undeclared but always present.

**Validation structure**: none automated — no test files exist in the inventory, no CI workflow, no lint/type-checking configuration. Input validation is type-only: `body: str` accepts the empty string with no length/content constraints (app/models.py:4), and `note_id: int` is FastAPI's path-type coercion (notes.py:15). There is no authorization anywhere. Error boundaries: only the 404 path (notes.py:18-19). SQLite connections are opened per request and never closed by `get_db` or either handler (app/db.py:4-7, notes.py:9, 16) — a per-request resource leak.

**Where responsibility becomes unclear**: at the persistence boundary (app/db.py) — who owns the database file, where it lives, who manages connections, and who migrates the schema are all implicit. This is the transition the rest of the analysis centers on.

## 3. Strong signals
- **Complete, traceable minimal flow**: entry point → router → handlers → SQLite can be walked end-to-end with file:line citations (main.py:9 → notes.py:5 → notes.py:8/15 → db.py:5). Nothing is stubbed or unreachable.
- **Parameterized SQL only** (notes.py:10, 17) — values are bound with `?` placeholders; no string-interpolated SQL in the two handlers (OBSERVED), so no obvious injection vector in the code that exists.
- **Honest documentation**: README.md:3 claims only "REST API for notes"; every claim in the README is implemented (Pass E contradiction search found no README-vs-code disagreement). No ghost features.
- **App-factory pattern** (app/main.py:4-7): `create_app()` keeps construction importable and testable, which is the right seed for adding a test suite.
- **Correct 404 semantics** for missing notes (notes.py:18-19).

## 4. Missing pieces
- **No tests at all**: the inventory contains zero test files and `requirements.txt` declares no test tooling (L1-L2). The two handlers and the schema contract (db.py:6) are entirely unverified (OBSERVED absence).
- **No CI / lint / type-check configuration** (OBSERVED absence over the full inventory).
- **No defined or validated database location**: `Path("notes.db")` (db.py:5) is relative to CWD; no configuration mechanism, environment variable, or startup check exists (OBSERVED absence in all 7 files).
- **No connection lifecycle management**: connections opened per request are never closed (db.py:7; notes.py:9, 16) — no context manager, no FastAPI dependency-with-yield.
- **pydantic undeclared** in requirements.txt (models.py:1 vs requirements.txt:1-2) — an implicit dependency on a transitive package.
- **No schema management/migrations**: schema is re-created ad hoc per connection (db.py:6); there is no versioning.
- **No API documentation** beyond the one-line README (README.md:3) — endpoints, request/response shapes, and state behavior are undocumented (docs gap, not misdescribed code).

## 5. Improvement opportunities
- Pin dependency versions in requirements.txt (currently unpinned, L1-L2).
- Declare `pydantic` explicitly in requirements.txt (used at models.py:1).
- Wrap connections in a context manager or a FastAPI dependency with `yield` so they are closed after each request (db.py:4-7).
- Make the DB path explicit and configurable (environment variable or config module) and document it in the README; add a startup writability check.
- Add a first test suite (pytest + FastAPI TestClient) covering create, read, 404, and the restart-persistence contract.
- Optionally add the two remaining CRUD operations (list/delete) — currently only create+read exist; the README does not promise them, so this is scope, not a defect.

## 6. Weakest boundary
Candidate boundaries were generated and scored before selection (per the skill's mandated procedure):

```text
Boundary: SQLite state file location — app/db.py:5-6
Observed contract: The service persists notes in a SQLite database; handlers open a connection per request and write/read through it (notes.py:9-12, 16-20).
Observed violation or uncertainty: The database path is the relative literal Path("notes.db") (db.py:5), resolved against the process working directory. Nothing in the repository defines, configures, validates, or documents that location (OBSERVED absence in all 7 files), and CREATE TABLE IF NOT EXISTS (db.py:6) silently creates a fresh empty database whenever the path resolves somewhere new. An instance started from any CWD other than the one holding the data behaves as if all notes are deleted — reads return 404 (notes.py:18-19) — with no error and no diagnostic.
Evidence: app/db.py:5-6 (relative path + silent schema creation), app/routers/notes.py:9-12 and 16-20 (per-request connections that never close), README.md:3 (launch command with no state contract), requirements.txt:1-2 and app/models.py:1 (second implicit dependency: pydantic used but undeclared).
Weakness type: Implicit Dependencies
Logic trace: app/db.py:5 opens sqlite3 at a CWD-relative path, and app/db.py:6 auto-creates the schema on every connection — both OBSERVED. A relative database path is a dependency on the process working directory: the code's behavior changes silently depending on where the process is launched, and no file in the inventory (config, env var, argument, README) pins or validates that location — OBSERVED absence, and README.md:3 documents only `uvicorn app.main:app`. The persistence layer therefore depends on a path that is "not explicitly defined or validated," which is the canonical definition of Implicit Dependencies (weakness-types.md #5). Because app/routers/notes.py:17-19 reads from that same implicit location, a CWD mismatch manifests as mass 404s — apparent data loss with zero diagnostics. This is a wiring/state-contract defect in the running system's structure, not a documentation misdescription (docs are accurate, so not Vocabulary Drift) and not a promised-but-missing feature (README promises nothing unimplemented, so not Ghost Features).
Failure consequence: Deploying, containerizing, or restarting the service from a different working directory (systemd WorkingDirectory, CI, a second instance) silently creates an empty database; all previously stored notes become invisible (404), and two instances can serve divergent state from the same code. Any future feature (update, delete, auth, sync, migrations) is built on an ungrounded state contract.
Confidence: high — every cited fact is OBSERVED (the relative path, the silent schema creation, the absent configuration); the failure mode is DERIVED directly from those facts. Confidence would be raised further only by runtime confirmation (starting uvicorn from two CWDs and observing the divergent databases), which this diagnostic run does not perform.
Alternatives considered:
- Zero automated validation (no tests/CI anywhere) — real and strong-evidenced (complete inventory shows no test files; requirements.txt has no test tooling), but it is a secondary gap: for a two-endpoint service the consequence is regression risk rather than silent state divergence, and it does not block the highest-value downstream work as directly. Recorded as the contributing secondary fog.
- pydantic used-but-undeclared (models.py:1 vs requirements.txt:1-2) — also Implicit Dependencies, but blast radius is one import that currently works via FastAPI's transitive dependency; low severity.
- Per-request SQLite connections never closed (db.py:4-7; notes.py:9, 16) — OBSERVED resource leak, but low-to-medium severity at this scale and no clean mapping to the seven canonical weakness types; kept as an improvement opportunity.
- Type-only input validation and no auth (models.py:4; notes.py:15) — scope gap for a toy service, not a defect against any documented contract.
```

## 6.5. Problem classification (fog type)
**architecture_fog** — the repository's primary uncertainty is structural: an implicit dependency chain (CWD-relative state file at app/db.py:5; pydantic used but undeclared at app/models.py:1), state/lifecycle ambiguity (per-request connections, schema created inline at db.py:6, no ownership of the database file), and an entirely unvalidated structure (no tests, no CI). This matches the architecture_fog evidence profile (implicit dependency chains, state ambiguity, unwired validation structure) in SKILL.md's Fog Classification.

- **Not ui_fog**: the codebase has no frontend surface at all — no HTML/CSS/JS/React/Vue/Angular files in the inventory — so the UI Fog Signals Registry decision tree terminates at "NO → not ui_fog".
- **Not product_fog**: no user intent artifact exists for this run, and the README (README.md:1-3) promises nothing that the code does not implement — there is no promised-but-absent deliverable (ghost-feature reasoning: the mismatch lives nowhere because there is no mismatch).
- **Not docs_fog (primary)**: the docs are minimal but accurate; nothing misdescribes existing code (Pass E found zero contradictions). A documentation gap exists (no API docs, no state documentation) but it is a consequence of the structure, not the driver.
- **Secondary fog**: Zero Validation (no automated checks on any contract) contributes; docs gap noted in prose.

No-user-intent run: `user_implied_fog_type: unknown`, `diagnosis_conflict: false`, `escalation_recommended: false` — evidence is consistent, strong, and cites only files actually opened.

## 7. Evidence
All substantive claims below carry an evidence class; citations are to files actually opened in full.

- **OBSERVED** — `app/db.py:5-6`: `conn = sqlite3.connect(Path("notes.db"))` followed by `conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT)")`. The state file is a CWD-relative path with no validation, and the schema is silently created on every connection.
- **OBSERVED** — `README.md:3`: the entire documented contract is "REST API for notes. `uvicorn app.main:app`." No feature list, no state location, no ops contract; also no contradiction with the code (Pass E).
- **OBSERVED** — `requirements.txt:1-2`: declares only `fastapi` and `uvicorn`; no pydantic, no test dependencies, no version pins.
- **OBSERVED** — `app/models.py:1`: `from pydantic import BaseModel` — pydantic is used but not declared (implicit dependency).
- **OBSERVED** — `app/routers/notes.py:8-12` and `15-20`: both handlers open a fresh connection via `get_db()` and never close it; `read` returns `HTTPException(404)` when a row is missing.
- **OBSERVED** — `app/main.py:4-9`: entry-point wiring via module-level `app = create_app()`.
- **OBSERVED absence** — the complete inventory (7 files, listed in Section 2) contains no tests, no CI, no config, no deployment files.

**Logic trace:** The observed facts chain as follows: (1) the only persistence path is `sqlite3.connect(Path("notes.db"))` at app/db.py:5 — a relative path whose target depends on the process working directory; (2) app/db.py:6 auto-creates the schema on every connection, so a launch from any directory without an existing database silently materializes a fresh empty one; (3) nothing in the repository — no config file, no environment variable, no CLI argument, and README.md:3 documents only the launch command — defines or validates where the database lives; (4) app/routers/notes.py:17-19 reads from that same implicit location, so notes written by an instance started in one directory are invisible (404) to an instance started in another. The persistence boundary therefore depends on a path that is not explicitly defined or validated — the canonical Implicit Dependencies weakness — and the failure mode is silent, divergent state across launches. This wiring defect in the running system's structure is what makes the state layer the weakest boundary and architecture_fog the primary fog type.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: app/db.py
    lines: L4-L7
    quote: "def get_db():\n    conn = sqlite3.connect(Path(\"notes.db\"))\n    conn.execute(\"CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT)\")\n    return conn"
    supports_claim: "The SQLite database is opened at a CWD-relative path with no validation, and the schema is silently auto-created on every connection."
  - file: app/db.py
    lines: L5
    quote: "    conn = sqlite3.connect(Path(\"notes.db\"))"
    supports_claim: "The state file location is a relative path resolved against the process working directory."
  - file: README.md
    lines: L3
    quote: "REST API for notes. `uvicorn app.main:app`."
    supports_claim: "README documents only the launch command; no state location, configuration, or ops contract is documented, and nothing promised is unimplemented."
  - file: requirements.txt
    lines: L1-L2
    quote: "fastapi\nuvicorn"
    supports_claim: "Manifest declares only fastapi and uvicorn — no pydantic (imported at app/models.py:1), no test tooling, no version pins."
  - file: app/models.py
    lines: L1
    quote: "from pydantic import BaseModel"
    supports_claim: "pydantic is used by the code but is not declared in requirements.txt — a used-but-undeclared implicit dependency."
  - file: app/routers/notes.py
    lines: L8-L12
    quote: "def create(note: Note):\n    db = get_db()\n    cur = db.execute(\"INSERT INTO notes (body) VALUES (?)\", (note.body,))\n    db.commit()\n    return {\"id\": cur.lastrowid}"
    supports_claim: "Create handler opens a connection per request, writes to the implicit notes.db, and never closes the connection."
  - file: app/routers/notes.py
    lines: L15-L20
    quote: "def read(note_id: int):\n    db = get_db()\n    row = db.execute(\"SELECT body FROM notes WHERE id = ?\", (note_id,)).fetchone()\n    if row is None:\n        raise HTTPException(404)\n    return {\"body\": row[0]}"
    supports_claim: "Read handler reads from the same implicit database; a CWD mismatch surfaces as 404 with no diagnostic."
  - file: app/main.py
    lines: L4-L9
    quote: "def create_app():\n    app = FastAPI()\n    app.include_router(notes.router)\n    return app\n\napp = create_app()"
    supports_claim: "Module-level app creation makes the entry point executable via `uvicorn app.main:app`; routing is registered here."
```

## 9. Why this boundary matters
The database location is the contract every other piece of the service depends on. If it remains implicit, then: (a) deploying or restarting the service from a different working directory silently creates an empty database, and existing notes appear deleted (404s at notes.py:18-19) with no error anywhere — a data-integrity illusion that is far worse than a loud failure; (b) two instances can serve divergent state from identical code, making debugging confusing; (c) every future feature — update, delete, auth, sync, migrations, backups — must be built on a state layer whose contract is undefined, so the boundary blocks the highest-value downstream work; and (d) the same implicit-wiring pattern (pydantic used but undeclared at models.py:1) shows the manifest cannot be trusted to reproduce a working environment, which compounds when the service grows.

## 10. Candidate next steps
1. **Define and validate the persistence contract first**: make the DB path explicit and configurable (env var, e.g. `NOTES_DB_PATH`, or a config module), add a startup check that the target directory is writable, and document the state location in README.md. (Highest leverage; directly removes the weakest boundary.)
2. **Add connection lifecycle management**: convert `get_db()` to a context manager or a FastAPI dependency with `yield` so connections are closed after each request (db.py:4-7, notes.py:9, 16).
3. **Add the first automated tests**: pytest + FastAPI TestClient covering create, read, 404, and — critically — a restart-persistence test that asserts notes survive a fresh launch from the configured directory (this test makes the Implicit Dependencies boundary visible).
4. **Repair the manifest**: declare pydantic and pin dependency versions in requirements.txt (L1-L2).
5. **Add the remaining CRUD surface** (list/delete endpoints) with tests, if the product contract is meant to be a full notes API.

## 11. Recommended next step
Step 1 from the list above — make the database location explicit, configurable, and validated, and document it in README.md. It is the smallest concrete action that removes the weakest boundary (app/db.py:5-6), and it unblocks every other improvement: connection lifecycle and tests are only meaningful once the state location is a defined contract.

## 12. Recommended workflow
`architecture-implementation-workflow` (from the canonical `skills/workflow-planner/references/workflow-registry.yaml`), execution mode `guided_execution` (one of that workflow's `allowed_execution_modes`; the workflow does not offer `plan_only`).

Rationale: the primary fog is architecture_fog with a state/wiring defect at the weakest boundary, so the fog-matched implementation workflow is `architecture-implementation-workflow` (registry entry: domain alignment → refactoring spec → issues → triage → TDD → handoff). The generic `implementation-workflow` was considered and rejected as the less specific match for a structure/state problem; `ui-implementation-workflow`, `docs-implementation-workflow`, and `product-implementation-workflow` do not apply (no frontend surface, docs accurate, no product-discovery need). `guided_execution` is chosen over `autonomous_execution` because the first steps change the persistence contract of a data-holding service and warrant human review at each gate. Preconditions: none blocking — this brief is diagnostic only and does not implement anything; the workflow would run under its own authorization later.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/backend-service
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "app/db.py (lines L4-L7): SQLite connection opened at CWD-relative Path(\"notes.db\") with schema auto-created per connection; no config/env/validation of the path"
  - "README.md (line L3): documents only the launch command 'uvicorn app.main:app'; no state location or ops contract"
  - "requirements.txt (lines L1-L2): declares only fastapi and uvicorn; no pydantic, no test tooling, no version pins"
  - "app/models.py (line L1): imports pydantic BaseModel, a dependency absent from the manifest (used-but-undeclared)"
  - "app/routers/notes.py (lines L8-L12 and L15-L20): handlers open a fresh connection per request, never close it, and read/write the implicit notes.db; missing rows surface as 404"
  - "app/main.py (lines L4-L9): entry-point wiring via module-level create_app()"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Implicit Dependencies
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:06:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```
Run the architecture-implementation-workflow in guided_execution mode on the
backend-service repository (experiments/repository-sensemaking-skill-hardening-v1/corpus/backend-service).

Diagnosis (repository sensemaking brief): primary fog type architecture_fog;
weakest boundary Implicit Dependencies at app/db.py:5-6 — the SQLite database
is opened at the CWD-relative path Path("notes.db") with schema auto-created per
connection (db.py:5-6) and no configuration, validation, or documentation of
where state lives (README.md:3). Secondary: Zero Validation (no tests, no CI).
Additional implicit dependency: pydantic used at app/models.py:1 but undeclared
in requirements.txt (L1-L2); per-request SQLite connections are never closed
(notes.py:9, 16).

Start with domain alignment (docs-aligner step) capturing the persistence
contract in CONTEXT.md, then produce the refactoring spec whose first slice is:
(1) make the DB path explicit and configurable (env var/config) with a startup
writability check, (2) document the state location in README.md, (3) add
connection lifecycle management (context manager or dependency with yield), and
(4) add the first pytest + TestClient suite covering create, read, 404, and the
restart-persistence contract. Decompose into issues, prepare agent briefs, and
implement via TDD with human review at every gate. No changes outside this
scope; do not add features beyond the persistence-contract hardening.
```
