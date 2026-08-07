# Repository Sensemaking Brief: notes-service (backend-service fixture)

## 1. Repository goal
A minimal FastAPI-style REST service that manages notes with SQLite persistence ("notes-service"). The stated purpose and run command live in `README.md:1-3` ("REST API for notes. `uvicorn app.main:app`."); the app exposes two endpoints — create a note (`POST /notes`) and read a note (`GET /notes/{note_id}`) — backed by a local SQLite database whose `notes` table is created on demand at first connection.

## 2. Current shape
Seven files, one package:
- `README.md` (3 lines): title, one-line purpose, and run command (`README.md:1-3`).
- `app/__init__.py` (empty package marker).
- `app/main.py` (9 lines): `create_app()` app factory that builds the FastAPI app and includes the notes router (`main.py:4-7`), plus a module-level `app = create_app()` (`main.py:9`) so `uvicorn app.main:app` works as documented.
- `app/models.py` (4 lines): `Note` pydantic model with a single `body: str` field (`models.py:3-4`).
- `app/db.py` (7 lines): `get_db()` opens a SQLite connection to the relative path `notes.db` and creates the `notes` table if absent (`db.py:4-7`).
- `app/routers/notes.py` (20 lines): `POST /notes` create handler (`notes.py:7-12`) and `GET /notes/{note_id}` read handler with a 404 path (`notes.py:14-20`).
- `requirements.txt` (2 lines): `fastapi`, `uvicorn`, unpinned (`requirements.txt:1-2`).

There are no test files, no CI configuration, and no docs directory.

## 3. Strong signals
- App-factory pattern (`main.py:4-7`) isolates app construction from wiring, so a `TestClient` can be injected cleanly once tests exist.
- Router separation: the notes API lives in its own router with a `/notes` prefix (`notes.py:5`), keeping the HTTP layer modular.
- Parameterized SQL on both the write and read paths (`notes.py:10`, `notes.py:17`) — no string interpolation, so there is no SQL-injection surface.
- Typed request parsing via pydantic (`models.py:3-4`) gives FastAPI automatic request parsing and a clear "is it a string" check.
- The README states the exact run command (`README.md:3`), so the service is startable exactly as documented.

## 4. Missing pieces
- **No validation on the core data model.** `models.py:4` declares `body: str` with no `min_length`/`max_length` or format constraints, and the column it lands in is an unconstrained `TEXT` (`db.py:6`). Empty or arbitrarily large bodies are accepted and persisted as-is.
- **Zero automated checks.** The repository contains no test files, no pytest configuration, and no CI — none of the API's behaviors (create, read, the 404 path at `notes.py:18-19`, persistence) are verified by any automated check.
- **No schema/migration validation.** The `notes` table is created implicitly at first connection (`db.py:6`); there is no schema versioning or migration step, so drift is undetectable.
- **Connection lifecycle not managed.** `get_db()` is called per request (`notes.py:9`, `notes.py:16`) and the connection is never closed — a resource leak under any sustained load.
- **Inconsistent resource representation.** `POST /notes` returns `{"id": ...}` (`notes.py:12`) while `GET /notes/{note_id}` returns `{"body": ...}` (`notes.py:20`); the same resource is represented two ways, and neither matches the `Note` model (`models.py:3-4`), which has no `id` field.
- **Feature surface is partial.** Only create and read exist; there is no list/update/delete surface despite the "REST API for notes" claim (`README.md:3`).
- **Dependencies unpinned and test tooling absent.** `requirements.txt:1-2` lists `fastapi` and `uvicorn` without versions, omits `pydantic` (used directly at `models.py:1` but only transitively present) and any test dependencies.

## 5. Improvement opportunities
- Add a pytest suite with FastAPI `TestClient` covering create/read/404/persistence once scaffolding exists — this directly closes the Zero Validation gap.
- Constrain `Note.body` (e.g. `min_length`, `max_length`) in `models.py:4` so the request contract enforces size at the boundary.
- Standardize the note representation across `notes.py:12` and `notes.py:20` (e.g. always return `{"id": ..., "body": ...}`) and document the contract in the README.
- Close DB connections deterministically (context manager, or a FastAPI dependency with `yield`) to fix the leak at `notes.py:9`/`notes.py:16`.
- Pin `requirements.txt:1-2` and add `pytest`/`httpx` for the test path.

## 6. Weakest boundary
The boundary between **accepting a request** and **persisting data** is unenforced. `models.py:4` (`body: str`) is the only validation in the entire request path, and it checks only that the value is a string: no length, no format, no size limit — and the SQLite column it is written into is an unconstrained `TEXT` (`db.py:6`). On top of that, nothing in the repository automatically verifies any behavior: there are no test files at all, so the 404 path (`notes.py:18-19`), the response shapes (`notes.py:12` vs `notes.py:20`), and persistence itself ship unverified. Every other boundary in this small repo (routing, module layout, SQL injection) is coherent or conventional; the validation boundary is the one that is both unenforced in code and unchecked by tooling.

**Weakness type:** Zero Validation

## 6.5. Problem classification (fog type)
`primary_fog_type: architecture_fog`.

- **Not `ui_fog`**: the UI Fog Signals Registry decision tree's first gate is whether the codebase contains frontend/UI code (React/Vue/Angular/HTML/CSS) — this repo has none; it is a pure backend service with no screens, flows, routing, or design system.
- **Not `product_fog`**: the purpose is clear and unambiguous (a notes REST API, `README.md:1-3`); there is no user-needs or requirements confusion.
- **Not `docs_fog` as the primary problem**: the README is minimal but accurate in what it claims; generating more documentation would not add validation or automated checks.
- **`architecture_fog`**: the weakness is in the service-layer design — the data boundary (model → persistence) has no validation contract and no automated verification. That is a structure/design problem of the backend architecture (canonical-vocabulary.yaml: "code organization, design patterns, or system structure").

## 7. Evidence
The diagnosis rests on direct code and structure evidence:
- `app/models.py:4` — `body: str` is a bare, unconstrained field: the only validation boundary in the request path.
- `app/routers/notes.py:10` — the unvalidated body is inserted straight into SQLite via parameterized SQL.
- `app/db.py:6` — the schema is created at runtime with no constraints, versioning, or migration checks.
- `app/routers/notes.py:18-19` — the 404 path is one of several behaviors with no automated test.
- `app/routers/notes.py:12` vs `app/routers/notes.py:20` — the two endpoints return different shapes for the same resource, an inconsistency only a test suite or contract check would surface.
- Repo-wide structure (directory listing): no `test/`, no `tests/`, no CI config — zero automated checks exist anywhere.

Logic trace: `app/models.py:4` shows the only validation in the API is `body: str` — a type check with no size or format constraints. `app/routers/notes.py:10` then persists that unvalidated value verbatim into a table created with no constraints at `app/db.py:6`. Meanwhile the repository contains no test files at all, so no automated check exists for any behavior — including the inconsistent representations at `app/routers/notes.py:12` and `app/routers/notes.py:20` and the 404 path at `app/routers/notes.py:18-19`. "Core logic or structure that has no automated check" is the defining case of Zero Validation (weakness-types.md, type 6): the input contract is unenforced and the behavior is unverified. Because every other boundary in this seven-file repo is conventional and coherent, this unenforced validation boundary is the weakest — it is where bad data and silent regressions enter the system.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: app/models.py
    lines: L4
    quote: 'body: str'
    supports_claim: "The Note model's only validation is a type check; no size or format constraints exist"
  - file: app/routers/notes.py
    lines: L10
    quote: 'cur = db.execute("INSERT INTO notes (body) VALUES (?)", (note.body,))'
    supports_claim: "The unvalidated body is inserted directly into SQLite"
  - file: app/db.py
    lines: L6
    quote: 'conn.execute("CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, body TEXT)")'
    supports_claim: "The notes schema is created at runtime with an unconstrained TEXT column and no migration/version checks"
  - file: app/routers/notes.py
    lines: L18-L19
    quote: "if row is None:\n        raise HTTPException(404)"
    supports_claim: "The 404 behavior is one of several API behaviors with no automated test"
  - file: README.md
    lines: L3
    quote: 'REST API for notes. `uvicorn app.main:app`.'
    supports_claim: "README describes the service but documents no endpoints, validation rules, or response contract"
  - file: requirements.txt
    lines: L1-L2
    quote: "fastapi\nuvicorn"
    supports_claim: "Runtime dependencies are unpinned and no test tooling is declared"
```

## 9. Why this boundary matters
With Zero Validation at the data boundary, the API will accept and persist arbitrary payloads — empty notes, multi-megabyte bodies — and nothing will catch a regression in the 404 contract (`notes.py:18-19`) or the response shapes (`notes.py:12` vs `notes.py:20`) until a real client breaks. Downstream consumers cannot rely on a stable note representation, and the team cannot distinguish "working" from "broken" because no automated check exists. The unclosed connections (`notes.py:9`, `notes.py:16`) turn sustained traffic into a resource leak. In short, the boundary where untrusted input meets the database is exactly the place where validation and automated checking are absent — the highest-risk point in the system.

## 10. Candidate next steps
1. **Add a pytest suite with FastAPI `TestClient`** covering create, read, 404, persistence, and response shapes — the structural fix for Zero Validation.
2. **Constrain `Note.body`** (`models.py:4`) with `min_length`/`max_length` so the input contract is enforced at the boundary.
3. **Standardize the note representation** across `notes.py:12` and `notes.py:20`, and document the contract in `README.md:3`.
4. **Manage the connection lifecycle** (context manager or a dependency with `yield`) so `notes.py:9`/`notes.py:16` stop leaking connections.
5. **Pin `requirements.txt:1-2`** and add `pytest`/`httpx` test tooling.

## 11. Recommended next step
Add the pytest + `TestClient` suite first: it is the smallest action that directly addresses Zero Validation (the weakest boundary), and it will immediately surface the response-shape inconsistency (`notes.py:12` vs `notes.py:20`) and the 404 behavior before any other change is made.

## 12. Recommended workflow
`architecture-implementation-workflow` (id present in `skills/workflow-planner/references/workflow-registry.yaml`, line 848) — the implementation path for architecture/code-design problems: align domain, create the refactoring/validation spec, decompose into issues, and implement via TDD. It matches the `architecture_fog` classification (canonical-vocabulary.yaml `typical_fog_types`) and the diagnosis that the service-layer validation contract must be designed and enforced.

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
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "app/models.py (line L4): Note.body is a bare str with no size or format constraints"
  - "app/routers/notes.py (line L10): the unvalidated body is inserted directly into SQLite"
  - "app/db.py (line L6): the notes schema is created at runtime with an unconstrained TEXT column and no migration checks"
  - "app/routers/notes.py (lines L18-L19): the 404 path has no automated test; no test files exist anywhere in the repo"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: plan_only
weakest_boundary: Zero Validation
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
For `workflow-planner`:

> Plan an `architecture-implementation-workflow` run for the `notes-service` repository (fixture `backend-service`). Diagnosis: `primary_fog_type: architecture_fog`; weakest boundary is **Zero Validation** — `app/models.py:4` declares `body: str` with no constraints, `app/routers/notes.py:10` persists the unvalidated body into an unconstrained `TEXT` column created at runtime (`app/db.py:6`), and the repository has no test files at all, so the 404 path (`app/routers/notes.py:18-19`) and the inconsistent response shapes (`app/routers/notes.py:12` returns `{"id": ...}` while `app/routers/notes.py:20` returns `{"body": ...}`) are unverified. Objective: enforce the data boundary and make behavior verifiable — add a pytest + FastAPI `TestClient` suite covering create/read/404/persistence, add `min_length`/`max_length` constraints to `Note` (`app/models.py:4`), standardize the note response representation, and close the per-request DB connection leak (`app/routers/notes.py:9`/`:16`). Keep `recommended_execution_mode: plan_only` — this baseline run is diagnostic; do not implement anything outside the planned scope.
