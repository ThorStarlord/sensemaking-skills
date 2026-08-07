# Repository Sensemaking Brief

## 1. Repository goal

The repository presents itself as a runnable full-stack application: a FastAPI
backend plus a React/JSX frontend, started with a single documented command.
README.md:3 states the repo is "A full-stack application." and README.md:5
documents `` `docker compose up`. `` as the way to run it. The intended goal is
therefore a minimal two-service web app (backend API + frontend screen) that a
developer can launch with one compose command.

## 2. Current shape

The fixture contains exactly 8 files (recursive inventory of the repository):

- `README.md` (5 lines) — the only documentation
- `backend/requirements.txt` (1 line) — `fastapi`
- `backend/app/main.py` (6 lines) — the only backend module
- `backend/app/db.py` (4 lines) — an sqlite3 connection factory
- `docker-compose.yml` (6 lines) — two services, no ports/volumes/commands
- `frontend/package.json` (1 line) — `{"name": "frontend"}`
- `frontend/src/App.jsx` (1 line) — a single React component
- `frontend/src/api.js` (1 line) — one exported API constant

**Runtime flow reconstruction** (what actually happens, not the directory
layout):

- **Startup path — UNREACHABLE as documented.** README.md:5 documents
  `docker compose up`; docker-compose.yml:1-5 defines `backend` and `frontend`
  services with build contexts `./backend` (docker-compose.yml:3) and
  `./frontend` (docker-compose.yml:5). Neither build context contains a
  Dockerfile — a recursive glob for `**/Dockerfile*` under the repository
  returns no matches, and the 8-file inventory above is complete. There is no
  alternative launcher: backend/requirements.txt:1 declares only `fastapi` (no
  ASGI server such as uvicorn), and backend/app/main.py:1-6 contains no
  `if __name__ == "__main__"` block and no server invocation. The frontend has
  no `index.html`, no bundler configuration, and no npm scripts
  (frontend/package.json:1 declares neither dependencies nor scripts).
- **Orchestration.** The FastAPI framework dispatches the single route
  `@app.get("/items")` (backend/app/main.py:4) to a handler that returns a
  hardcoded empty list (backend/app/main.py:6). No other services, workers,
  jobs, or scheduled tasks exist (OBSERVED absence in the full inventory).
- **Domain/core logic.** None beyond the stub handler; no business-logic
  modules exist.
- **Persistence/state.** backend/app/db.py:3-4 defines `conn()` returning
  `sqlite3.connect("app.db")` — a file-backed state boundary — but
  backend/app/main.py:1-6 never imports `db` (its only import is `fastapi`,
  main.py:1). The state layer is declared but unwired; whether persistence was
  ever intended for `/items` is UNKNOWN.
- **External integration points.** None. frontend/src/api.js:1 exports
  `API = '/api/v1/items'` but nothing in the repository imports or references
  `api.js` (frontend/src/App.jsx:1 renders a static `<div>app</div>` and
  imports nothing).
- **Output boundary.** The HTTP response `[]` returned by
  backend/app/main.py:6; nothing else leaves the system.
- **Where validation happens.** Nowhere. There are no tests, no CI
  configuration, no schemas, no input validation, no authorization, and no
  error boundaries anywhere in the repository (OBSERVED absence across the
  complete 8-file inventory).
- **Where responsibility becomes unclear.** (a) Deployment/build: compose
  promises images that have no build definition. (b) Frontend↔backend
  integration: the frontend's declared API path (`/api/v1/items`, api.js:1)
  disagrees with the backend's actual route (`/items`, main.py:4), and the
  frontend never calls the backend at all.

**Dependency semantics** (declared vs used vs runtime):

- `fastapi` — *declared* (backend/requirements.txt:1) and *used*
  (backend/app/main.py:1).
- `sqlite3` — *used* (backend/app/db.py:1) but stdlib, so no manifest entry is
  required; the module itself is never imported by the app.
- React — *used* in the sense that App.jsx:1 contains JSX, but *not declared*:
  frontend/package.json:1 lists no dependencies at all, so the JSX contract is
  implicit and unbuildable as declared.
- ASGI server (uvicorn or equivalent) — *required to run* main.py:2 but
  *undeclared*; import exists ≠ runtime execution path proven, and here even
  the import side is missing.
- `frontend/src/api.js` and `backend/app/db.py` — *dead* from the runtime's
  perspective: authored but never referenced on any execution path.

**State model.** One state boundary exists: the sqlite file `app.db` created
by `conn()` (backend/app/db.py:4). Nothing writes or reads it today — the
writer/reader relationship is UNKNOWN because the module is unwired.

**Boundary model.** HTTP → FastAPI route (backend/app/main.py:4) is the only
boundary with any implementation; it performs zero validation and zero
persistence. The compose→image boundary and the frontend→API boundary are
declared but broken (see Section 6).

## 3. Strong signals

- Clean, minimal layering: backend and frontend are separated into their own
  trees (`backend/app/`, `frontend/src/`), so the intended two-service shape
  is visible despite the skeleton state.
- A single, tiny API surface (one route) that is easy to reason about and
  easy to test once a runtime exists (backend/app/main.py:4-6).
- The backend already uses a standard-library persistence primitive
  (sqlite3) with a factory function rather than scattering connection logic
  (backend/app/db.py:1-4).
- A docker-compose.yml exists at all, signalling the author's intended
  deployment topology (two services, one command) even though its build
  inputs are missing (docker-compose.yml:1-5).
- The frontend screen is isolated in one component file (frontend/src/App.jsx:1),
  so no component-boundary debt exists yet.

## 4. Missing pieces

- **Dockerfiles** for both build contexts referenced by docker-compose.yml:3
  and docker-compose.yml:5 — the single most consequential absence (see
  Section 6).
- **A server launcher**: no ASGI server declared (backend/requirements.txt:1)
  and no server bootstrap in backend/app/main.py:1-6, so the FastAPI app
  object cannot be started by any declared mechanism.
- **A frontend build/run path**: no `index.html`, no bundler (vite/webpack),
  no npm scripts, and no `react` dependency (frontend/package.json:1), so the
  JSX in frontend/src/App.jsx:1 cannot compile or be served.
- **Frontend↔backend wiring**: nothing imports frontend/src/api.js:1, and its
  path `/api/v1/items` disagrees with the backend route `/items`
  (backend/app/main.py:4).
- **Persistence wiring**: backend/app/db.py:3-4 is never imported by
  backend/app/main.py.
- **Any validation layer**: no tests, no CI, no schemas, no input validation
  (OBSERVED absence across the complete inventory).
- **Compose runtime details**: no ports, volumes, or `depends_on`
  (docker-compose.yml:1-5), so even with images, the two services have no
  defined network or data contract.

## 5. Improvement opportunities

- Add a minimal `.gitignore` (Python `__pycache__`, `app.db`, `node_modules`).
- Add a local-dev section to README.md (run uvicorn directly, `npm run dev`)
  so the app is runnable even without Docker.
- Declare pinned versions in backend/requirements.txt and real dependencies
  in frontend/package.json.
- Add a smoke test (e.g. one pytest that asserts `GET /items` returns a list)
  once a runtime exists — this converts the boot contract from unverifiable
  to checked (moves toward the Zero Validation gap).
- Add compose healthchecks and a port mapping so `docker compose up` yields a
  reachable URL.

## 6. Weakest boundary

### Candidate generation and scoring

**Candidate A — Deployment/build contract (documented startup → Dockerfiles).**
README.md:5 documents `` `docker compose up`. ``; docker-compose.yml:3 and
docker-compose.yml:5 define build contexts `./backend` and `./frontend`; no
Dockerfile exists in either directory (recursive glob: no matches), and no
other launcher is declared (backend/requirements.txt:1;
frontend/package.json:1).

```yaml
boundary: README.md:5 + docker-compose.yml:3,5 -> absent Dockerfiles
evidence_strength: strong
severity: high
blast_radius: high
goal_relevance: high
downstream_blocking_effect: high
uncertainty: low
```

**Candidate B — Frontend↔backend API contract.** frontend/src/api.js:1
declares `/api/v1/items`; backend/app/main.py:4 registers `/items`; App.jsx:1
never imports api.js.

```yaml
boundary: frontend/src/api.js:1 vs backend/app/main.py:4 (and no import site)
evidence_strength: strong
severity: medium
blast_radius: medium
goal_relevance: high
downstream_blocking_effect: medium
uncertainty: low
```

**Candidate C — Undeclared runtime environment.** JSX used at
frontend/src/App.jsx:1 with no `react` in frontend/package.json:1; FastAPI app
at backend/app/main.py:2 with no ASGI server in backend/requirements.txt:1.

```yaml
boundary: used-but-undeclared deps (react, ASGI server) vs manifests
evidence_strength: strong
severity: medium
blast_radius: medium
goal_relevance: high
downstream_blocking_effect: medium
uncertainty: low
```

**Candidate D — Unwired persistence module.** backend/app/db.py:3-4 defines
`conn()`; backend/app/main.py:1-6 never imports it.

```yaml
boundary: backend/app/db.py:3-4 -> no import site
evidence_strength: strong
severity: low
blast_radius: low
goal_relevance: medium
downstream_blocking_effect: low
uncertainty: low
```

**Candidate E — Zero automated validation.** No tests, no CI, no schema checks
anywhere (OBSERVED absence in the 8-file inventory).

```yaml
boundary: whole repo, no automated checks
evidence_strength: strong
severity: medium
blast_radius: high
goal_relevance: medium
downstream_blocking_effect: medium
uncertainty: low
```

### Selection

**Boundary:** the deployment/build contract between the documented startup
instruction and the build inputs it depends on: README.md:5 →
docker-compose.yml:3,5 → (absent) Dockerfiles, with no fallback launcher.

**Observed contract:** README.md:5 documents `` `docker compose up`. `` as the
way to run the app, and docker-compose.yml:1-5 defines backend and frontend
services built from `./backend` and `./frontend`. The app is presented as live
("A full-stack application.", README.md:3).

**Observed violation or uncertainty:** the build contexts contain no
Dockerfiles (recursive glob for `**/Dockerfile*` under the repository returns
no matches; the complete inventory is only 8 files). Even if images existed,
backend/requirements.txt:1 declares no ASGI server to launch main.py:2, and
frontend/package.json:1 declares no dependencies or scripts to build/serve
App.jsx:1. The documented startup path therefore has no reachable
implementation, and no alternative startup path is declared anywhere.

**Evidence:** README.md:3, README.md:5; docker-compose.yml:3,
docker-compose.yml:5; backend/requirements.txt:1; backend/app/main.py:1-6;
frontend/package.json:1; frontend/src/App.jsx:1. Absence of Dockerfiles,
tests, CI, and launcher scripts is OBSERVED (recursive inventory of the
repository, including globs for `**/Dockerfile*` and dotfiles, returned only
the 8 files listed in Section 2).

**Weakness type:** Ghost Features

**Logic trace:** README.md:5 is a documented surface that promises the
functionality "the app runs via `docker compose up`", and README.md:3 presents
the repo as a working full-stack application. That documented functionality
requires images built from the contexts declared at docker-compose.yml:3 and
docker-compose.yml:5; a recursive glob of the repository finds no Dockerfile
in either context, and the complete 8-file inventory shows no launcher script,
no ASGI server declaration (backend/requirements.txt:1), and no frontend build
path (frontend/package.json:1). The promised startup surface therefore has no
reachable implementation — per the GAP-6 taxonomy mapping, a documented
surface with no reachable implementation is exactly `Ghost Features` (this is
not dead code, not a docs misdescription of existing code, and not merely an
unchecked contract — the build inputs themselves do not exist). Per GAP-5,
this classification is expected to trigger the validator's
`HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT` warning; a substantive human audit
is required before final approval, and it was not dodged by misclassifying to
a lower-risk type.

**Failure consequence:** the repo's only documented command fails at the first
step (`docker compose up` cannot build either service), and no alternative
start path exists — the system cannot start, so the claimed "full-stack
application" (README.md:3) is unverifiable. Every downstream activity (tests,
UI work, API integration, persistence) is blocked because there is no running
system to build against, and the two services have no way to reach each other.

**Confidence:** high — every supporting fact is OBSERVED directly (file
contents read in full; absence of Dockerfiles/tests/CI established by a
complete recursive inventory), and the weakest link in the chain is a hard
absence rather than an interpretation. What would raise it further: executing
`docker compose build` to observe the failure firsthand (not done — the brief
is diagnostic-only).

**Alternatives considered:**

- *Candidate B (frontend↔backend API contract)* — lost because it is a
  downstream consequence: even if api.js and the route agreed and the frontend
  imported the API, nothing can build or run, so the integration could not be
  exercised. Its evidence is equally strong but its severity and blast radius
  are lower.
- *Candidate C (undeclared runtime environment)* — lost because it is a
  contributing cause of the same boot failure with a narrower blast radius
  (one service each) and is partially subsumed by Candidate A's logic trace
  (no reachable implementation includes "no declared server").
- *Candidate D (unwired db.py)* — lost on consequence: low severity, low blast
  radius, no downstream blocking; it is a latent risk, not a blocker.
- *Candidate E (zero validation)* — lost because it is generic: the absence of
  tests/CI is a symptom of the skeleton state, whereas Candidate A is the
  specific defect that blocks everything and is the cheapest to prove. GAP-6
  maps packaging gaps to Zero Validation or Implicit Dependencies only when
  the metadata gap is the defect; here the stronger, more specific defect is
  that documented functionality has no implementation at all.

## 6.5. Problem classification (fog type)

Primary fog type: **architecture_fog**.

The repository contains frontend code (frontend/src/App.jsx:1,
frontend/src/api.js:1), so the UI Fog Signals Registry evaluation is required.
Tier 1: signal 1.1 (missing UI flow documentation) is PRESENT — the repository
has no docs, flows, or screen specs at all; signals 1.2 (scattered components),
1.3 (routing complexity), and 1.4 (design-system fragmentation) are ABSENT
(there is a single component, no routing, and no styling to fragment). Tier 2:
signals 2.1 (no UI tests), 2.2 (accessibility unaddressed), 2.3 (responsive
design undocumented), and 2.4 (screens undocumented) are PRESENT. Per the
registry decision tree that would be medium-confidence ui_fog — but the
SKILL.md frontend tie-break exception applies: the defect is provably outside
the UI layer. The app cannot boot because of an entry-point/deployment
contract failure (no Dockerfiles for the compose build contexts,
docker-compose.yml:3,5; no declared server launcher, backend/requirements.txt:1;
no frontend build path, frontend/package.json:1) — this failure occurs before
any screen can render, and no screen/flow/design problem exists in a one-line
static component. The entry-point-stub rule also points to architecture_fog:
runtime entry points (server bootstrap, frontend build) are missing or
skeletal, forming an incomplete system. **ui_fog is the secondary fog** (frontend
code exists and UI-flow documentation is entirely absent); **docs_fog
contributes minimally** (the README is sparse, but it does not misdescribe
existing code — it describes functionality that does not exist, which is a
Ghost-Feature/structural issue, not stale docs). No user intent artifact
exists for this fixture, so `user_implied_fog_type` is `unknown` (GAP-8) and
there is no intent conflict to escalate.

## 7. Evidence

All evidence files were opened and read in full (8 files, listed in Section
2). Absences (Dockerfiles, tests, CI, launcher scripts, frontend build files)
are established by a complete recursive inventory of the repository — globs
for `**/Dockerfile*` and dotfiles returned no matches under the repository
root.

The decisive evidence chain: `docker-compose.yml:3` and `docker-compose.yml:5`
declare build contexts (`build: ./backend`, `build: ./frontend`) whose
Dockerfiles do not exist; `README.md:5` documents `` `docker compose up`. ``
as the startup command; `backend/requirements.txt:1` declares only `fastapi`
(no ASGI server to launch `backend/app/main.py:2`); `frontend/package.json:1`
declares no dependencies and no scripts, so the JSX at
`frontend/src/App.jsx:1` cannot build. Supporting mismatches:
`frontend/src/api.js:1` declares `/api/v1/items` while `backend/app/main.py:4`
registers `/items` and `frontend/src/App.jsx:1` never imports `api.js`;
`backend/app/db.py:3` defines a persistence factory that `backend/app/main.py`
never imports.

**Logic trace:** README.md:5 is the only documented way to run the system, and
README.md:3 presents the repo as a complete full-stack application; the
functionality it promises requires images built from the contexts at
docker-compose.yml:3 and docker-compose.yml:5, and those contexts contain no
Dockerfiles (OBSERVED absence via complete recursive inventory). No fallback
launcher exists: backend/requirements.txt:1 omits an ASGI server,
backend/app/main.py:1-6 has no server bootstrap, and frontend/package.json:1
omits dependencies and scripts. Because the documented startup surface has no
reachable implementation, the weakest boundary is the deployment/build
contract, classified as Ghost Features; because the failure is a boot-blocking
entry-point contract failure that occurs before any screen can render, the
primary fog type is architecture_fog (frontend tie-break exception), with
ui_fog secondary.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "A full-stack application."
    supports_claim: "The README presents the repository as a complete, live full-stack application."
  - file: README.md
    lines: L5
    quote: "`docker compose up`."
    supports_claim: "The README documents `docker compose up` as the only way to run the app — a documented surface with no reachable implementation."
  - file: docker-compose.yml
    lines: L1-L5
    quote: "services:\n  backend:\n    build: ./backend\n  frontend:\n    build: ./frontend"
    supports_claim: "Compose defines both services from build contexts ./backend and ./frontend; no Dockerfile exists in either context, and no ports/commands are defined."
  - file: backend/requirements.txt
    lines: L1
    quote: "fastapi"
    supports_claim: "The backend declares only fastapi — no ASGI server (e.g. uvicorn) is declared, so the FastAPI app at main.py:2 has no declared launcher."
  - file: backend/app/main.py
    lines: L1-L6
    quote: "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get(\"/items\")\ndef items():\n    return []"
    supports_claim: "The only backend module: a single GET /items route returning a hardcoded empty list, with no server bootstrap and no import of db.py."
  - file: backend/app/db.py
    lines: L3-L4
    quote: "def conn():\n    return sqlite3.connect(\"app.db\")"
    supports_claim: "A persistence factory exists (file-backed state boundary) but is never imported by main.py — declared but unwired."
  - file: frontend/package.json
    lines: L1
    quote: "{\"name\": \"frontend\"}"
    supports_claim: "The frontend manifest declares no dependencies (no react) and no scripts — the JSX in App.jsx cannot be built or served as declared."
  - file: frontend/src/App.jsx
    lines: L1
    quote: "export default function App() { return <div>app</div>; }"
    supports_claim: "The only screen renders a static div and imports nothing — the frontend never calls the backend."
  - file: frontend/src/api.js
    lines: L1
    quote: "export const API = '/api/v1/items';"
    supports_claim: "The frontend's declared API path (/api/v1/items) disagrees with the backend route (/items, main.py:4) and is never referenced by any other file."
```

## 9. Why this boundary matters

The deployment/build contract is the front door of the repository: its only
documented command (README.md:5) cannot execute because the build inputs it
depends on (Dockerfiles for docker-compose.yml:3,5) do not exist. Until this
boundary is repaired, nothing else in the repository can be verified —
there is no running backend to test against, no frontend to render, no way to
exercise the API contract (api.js:1 vs main.py:4), and no way to observe
whether db.py was ever meant to be wired in. Every improvement opportunity in
Section 5 and every candidate next step in Section 10 is blocked on a system
that can start. It is also a trust boundary: a developer following the
documented instructions experiences a hard failure at step one, which makes
the entire repository look abandoned or misleading regardless of the intent
behind the skeleton.

## 10. Candidate next steps

1. **Restore a reachable startup path (highest leverage).** Add a backend
   Dockerfile in `backend/` (Python image; `pip install -r requirements.txt`
   extended with `uvicorn`; `CMD ["uvicorn", "app.main:app", ...]`) so the
   build context at docker-compose.yml:3 resolves, then do the same for the
   frontend context at docker-compose.yml:5 (add `react`, a bundler, an
   `index.html`, and an npm `start`/`build` script).
2. **Wire the frontend to the backend.** Import `api.js` from App.jsx and
   reconcile the path: either change api.js:1 to `/items` or move the backend
   route to `/api/v1/items` (backend/app/main.py:4) — and add the missing
   port mapping in docker-compose.yml so the two services can actually reach
   each other.
3. **Declare the real dependency contract.** Add `uvicorn` to
   backend/requirements.txt and `react`/build tooling to frontend/package.json,
   plus a server bootstrap in backend/app/main.py.
4. **Decide the fate of db.py.** Either wire `conn()` into the `/items`
   handler (persistence becomes real) or delete the module — currently it is
   dead code with an implied contract (Implicit Dependencies risk).
5. **Add a boot smoke test + CI.** One pytest asserting `GET /items` returns
   `[]` and a minimal CI job running `docker compose build` would convert the
   Ghost Feature into a checked contract (addressing Zero Validation).

## 11. Recommended next step

Step 1 — add the missing Dockerfiles (starting with the backend) so that
`docker compose up` (README.md:5) becomes executable: create
`backend/Dockerfile` that installs backend/requirements.txt (extended with an
ASGI server) and launches `app.main:app`, and create a matching
`frontend/Dockerfile` with a working build. This is the smallest concrete
action that turns the documented startup surface from a Ghost Feature into a
reachable implementation, and it unblocks every other candidate step.

## 12. Recommended workflow

`architecture-implementation-workflow` (id verified in
`skills/workflow-planner/references/workflow-registry.yaml`, lines 848-904;
allowed execution modes: `guided_execution`, `autonomous_execution`, registry
lines 858-861). Recommended execution mode: **`guided_execution`**.

Rationale: the primary fog type is `architecture_fog` — the defect is a
structural/boot-contract problem (missing build inputs and entry-point
wiring), so the architecture implementation workflow is the registry's
matching implementation path (domain alignment → architecture spec → issue
decomposition → TDD implementation). Closest alternatives considered and
rejected: `ui-implementation-workflow` (the UI layer is not the blocker — the
screen cannot render because the system cannot build, so a UI flow/screen-spec
chain would run against an unrunnable system); `implementation-workflow` (the
generic default — `architecture-implementation-workflow` is the more precise
fit for a boot/entry-point contract defect); `docs-implementation-workflow`
(the README is not stale; the functionality it documents simply does not
exist); and `ui-diagnostic-workflow` (its purpose is UI assessment, and the
defect is provably outside the UI layer per the frontend tie-break exception).
`plan_only` is deliberately NOT recommended: it is not an allowed mode for
`architecture-implementation-workflow` (GAP-7), and `guided_execution` is the
compatible mode that preserves human review gates for a diagnostic handoff.
Preconditions missing before the workflow can run: none blocking — the brief
(including the substantive human audit required for the Ghost Features
classification, per GAP-5/D5) is the prerequisite artifact.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/full-stack
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (L3, L5): presents the repo as a full-stack application and documents `docker compose up` as the only startup instruction"
  - "docker-compose.yml (L1-L5): backend and frontend services defined with build contexts ./backend and ./frontend; no Dockerfile exists in either context"
  - "backend/requirements.txt (L1): declares only fastapi; no ASGI server, so the app at main.py:2 has no declared launcher"
  - "backend/app/main.py (L1-L6): single route /items returning []; no server bootstrap; never imports db.py"
  - "backend/app/db.py (L3-L4): sqlite3 conn() factory never imported by main.py"
  - "frontend/package.json (L1): no dependencies (no react) and no scripts; JSX in App.jsx:1 cannot build"
  - "frontend/src/App.jsx (L1): single screen renders a static div; never imports api.js"
  - "frontend/src/api.js (L1): API path /api/v1/items disagrees with backend route /items (main.py:4) and is unused"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-06-18T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

> Workflow: `architecture-implementation-workflow`, mode `guided_execution`
> (registry-verified; `plan_only` is not an allowed mode for this workflow).
>
> Context: the repository sensemaking brief at
> `experiments/repository-sensemaking-skill-hardening-v1/candidate/full-stack.md`
> diagnoses the target repository
> `experiments/repository-sensemaking-skill-hardening-v1/corpus/full-stack`
> (primary fog: `architecture_fog`; secondary: `ui_fog`; weakest boundary:
> `Ghost Features` — the documented startup surface, README.md:5
> `docker compose up`, has no reachable implementation because the build
> contexts at docker-compose.yml:3,5 contain no Dockerfiles, no ASGI server is
> declared in backend/requirements.txt:1, and frontend/package.json:1 declares
> no dependencies or scripts).
>
> Before planning implementation, note that the Ghost Features classification
> requires a substantive human audit (GAP-5/D5) before final approval. The
> recommended first step is to restore a reachable startup path: add a backend
> Dockerfile (extend backend/requirements.txt with an ASGI server; launch
> `app.main:app`) and a frontend Dockerfile with a working build, then verify
> `docker compose up` runs. Do not modify the target repository during
> planning; produce the orchestration plan only.
