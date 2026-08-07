# Ideal response prototype — backend-service

**What this is:** a 7-file FastAPI service that stores and retrieves notes in
SQLite. Two endpoints: `POST /notes` (create) and `GET /notes/{id}` (read)
(app/routers/notes.py:7-20), run via `uvicorn app.main:app`
(app/main.py:9, README.md:3).

**How it works:** FastAPI -> notes router -> pydantic model (Note.body: str,
app/models.py:3-4) -> SQLite connection that creates the notes table on first
use (app/db.py:4-7). No auth, no config layer, no tests.

**The one important weakness:** the write path accepts anything and the read
path can disagree with it. `Note.body` is an unconstrained string
(app/models.py:4), inserted directly (app/routers/notes.py:10), and reads
return a plain dict while creates return only an id — response shapes are
inconsistent between the two endpoints (notes.py:12 vs notes.py:20). There are
zero tests, so the 404 path (notes.py:18-19) and the create/read round-trip
are never exercised. Evidence: models.py:4, notes.py:10, notes.py:18-20,
repo-wide absence of tests.

**Alternatives considered:** (1) no schema/persistence at all (rejected —
SQLite schema exists and works); (2) missing auth (rejected — out of scope for
a 7-file fixture; nothing in the repo claims auth).

**Confidence: high** — every file was read; the claims are directly observed.
What remains unknown: actual runtime behavior (never executed here) and
whether the SQLite file path is stable across deployment contexts (db.py:4
uses a relative path).

**Recommended next step:** add validation + tests before any feature work:
constrain `Note.body` (length/content), make the response shapes consistent,
and add a create->read round-trip test plus a 404 test. Do not change the API.

**Ask before:** changing the API surface or the storage format.
