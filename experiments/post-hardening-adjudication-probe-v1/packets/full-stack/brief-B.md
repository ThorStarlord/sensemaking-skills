# Repository Sensemaking Brief — corpus/full-stack

## 1. Repository goal
This repository is a minimal full-stack application scaffold ("fullstack-app", `README.md:1-3`): a FastAPI backend exposing a `GET /items` endpoint (`backend/app/main.py:4-6`) with a separate SQLite persistence module (`backend/app/db.py:1-4`), a React JSX frontend (`frontend/src/App.jsx:1`) that centralizes its API base in one constant (`frontend/src/api.js:1`), and a docker-compose file (`docker-compose.yml:1-5`) intended to build and run both halves. The only documented way to run the app is `docker compose up` (`README.md:5`). The apparent goal is a runnable end-to-end stack — API plus UI plus container orchestration — but as shipped, the documented entry point cannot work because the build contexts compose declares do not exist.

## 2. Current shape
Eight files, organized as two top-level halves plus root orchestration (verified by a recursive listing of `corpus/full-stack` — exactly 8 files, no hidden files, no Dockerfiles anywhere):
- `README.md` (5 lines) — title, one-line description, single run instruction.
- `docker-compose.yml` (5 lines) — two services, `backend` and `frontend`, each declaring a build context (`./backend`, `./frontend`).
- `backend/app/main.py` (6 lines) — FastAPI app with one route, `GET /items`, returning a hardcoded `[]`.
- `backend/app/db.py` (4 lines) — `sqlite3` connection helper `conn()` → `sqlite3.connect("app.db")`.
- `backend/requirements.txt` (1 line) — `fastapi`.
- `frontend/package.json` (1 line) — `{"name": "frontend"}` only; no dependencies, scripts, or module type.
- `frontend/src/App.jsx` (1 line) — default export `App` rendering a static `<div>app</div>`.
- `frontend/src/api.js` (1 line) — `export const API = '/api/v1/items';`.

## 3. Strong signals
- Clean top-level separation of concerns: `backend/` and `frontend/` are distinct trees, and `docker-compose.yml:2-5` declares both as services — the intended architecture (API + UI + container orchestration) is legible from the layout alone.
- The API base path is centralized in a single constant (`frontend/src/api.js:1`) rather than inlined across components — a nascent API-contract layer.
- The backend uses a real framework (FastAPI) with an explicit route (`backend/app/main.py:4`), and persistence is factored into its own module (`backend/app/db.py:3-4`) — the intent of a layered backend (routes vs. storage) is present.
- A compose file exists at the root (`docker-compose.yml:1`), signaling the intent to run the stack reproducibly.

## 4. Missing pieces
- **Dockerfiles**: `docker-compose.yml:3` and `docker-compose.yml:5` declare build contexts `./backend` and `./frontend`, but neither directory contains a Dockerfile (recursive listing of the fixture matches zero `Dockerfile*` files and zero dotfiles). `docker compose up` (`README.md:5`) therefore fails at the build step — the repo's only run path is dead on arrival.
- **Frontend build tooling**: `frontend/src/App.jsx:1` is JSX, which requires a transpiler/bundler, but `frontend/package.json:1` declares no dependencies, no scripts, and no module type — the frontend cannot be built or executed as shipped.
- **Contract between the halves**: `frontend/src/api.js:1` targets `/api/v1/items` while the backend serves `GET /items` (`backend/app/main.py:4`); no `/api/v1` prefix exists anywhere in the backend and `docker-compose.yml:1-5` defines no reverse proxy or rewrite. Moreover, nothing imports `api.js`: `frontend/src/App.jsx:1` renders a static div and never calls the API, so the constant is orphaned.
- **Wired persistence**: `backend/app/db.py:3-4` defines `conn()`, but `backend/app/main.py:1-6` never imports or calls it — the `/items` route returns a hardcoded empty list (`backend/app/main.py:6`), so the SQLite layer is unwired dead code.
- **Automated validation**: no tests, no CI, no lint config anywhere in the tree; nothing checks that the compose contract, the API contract, or the JSX build actually hold.
- **Documentation**: `README.md` is 5 lines; there are no API docs, no run/setup docs beyond the broken compose instruction, no architecture notes, and no UI flow/screen specs.
- **Runtime dependencies**: `backend/requirements.txt:1` lists only `fastapi` — no ASGI server (e.g., `uvicorn`) is declared, so even a corrected image could not actually serve the app.

## 5. Improvement opportunities
- Add a minimal backend Dockerfile and a frontend Dockerfile (or switch the compose services to published images) so the README's run path works.
- Add a real frontend toolchain (dependencies plus a build script in `frontend/package.json`) or, given the trivial UI, drop JSX for plain JS in `frontend/src/App.jsx`.
- Align the API contract: serve `/api/v1/items` from the backend (or change `frontend/src/api.js:1` to `/items`) and document the contract in the README.
- Wire `backend/app/db.py:3-4` into the route handler (or delete the module) so the persistence layer is real or absent.
- Add a smoke test (e.g., FastAPI `TestClient` hitting `/items`) and a CI step that runs `docker compose build`, so the declared contracts are enforced from now on.

## 6. Weakest boundary
The weakest boundary is the repository's **declared run contract**: `README.md:5` documents `docker compose up` as the way to run the app, and `docker-compose.yml:2-5` declares two services built from `./backend` and `./frontend`, but neither directory contains a Dockerfile (verified by recursive listing — the fixture is exactly 8 files, no Dockerfile anywhere). The documented entry point therefore fails before a single line of application code executes. The same declared-without-counterpart defect repeats at every seam: the frontend declares JSX (`frontend/src/App.jsx:1`) with no build tooling (`frontend/package.json:1`); the client declares `/api/v1/items` (`frontend/src/api.js:1`) while the server serves `/items` (`backend/app/main.py:4`); and the persistence layer (`backend/app/db.py:3-4`) is never imported by the app (`backend/app/main.py:1-6`). In each case a file declares a contract whose counterpart does not exist, and nothing validates the pairing.

**Weakness type:** Contract Mismatch

Logic trace: `README.md:5` is the repo's only run instruction and points at docker-compose; `docker-compose.yml:3` and `docker-compose.yml:5` declare build contexts `./backend` and `./frontend`; the recursive listing of the fixture shows no Dockerfile in either directory — so the build contract compose declares has no implementation, and the stated entry point fails immediately. The same pattern is independently confirmed by `frontend/src/api.js:1` (`/api/v1/items`) vs. `backend/app/main.py:4` (`/items`) with no proxy in `docker-compose.yml:1-5`, by `frontend/src/App.jsx:1` (JSX) vs. `frontend/package.json:1` (no toolchain), and by `backend/app/db.py:3-4` (`conn`) never being referenced from `backend/app/main.py:1-6`. Because every one of these is a mismatch between a declared contract and an absent counterpart — not a missing test, missing doc, or missing feature — the unifying weakness is **Contract Mismatch**, and the compose/Dockerfile pair is the weakest instance because it blocks the repo's only documented way to run at all.

## 6.5. Problem classification (fog type)
**primary_fog_type: architecture_fog.** The repo contains frontend code (`frontend/src/App.jsx:1`), so the UI Fog Signals Registry check is applied. Tier 1.1 (UI flow documentation) is absent — there are no flow/screen specs of any kind — and Tier 1.4 (design system) is absent — no tokens, no component library, no styling at all. However, the registry's own qualitative gate (ui-fog-signals.md decision tree: "Is the primary problem about 'how the UI works' vs 'what the UI should do'?") resolves to neither: there are no screens, flows, or navigation to be confused about — the entire UI is one static element (`frontend/src/App.jsx:1`). The actual problems are structural and contractual: the compose run path is unfulfillable (`docker-compose.yml:3,5`; no Dockerfiles), the frontend/backend API contract is mismatched (`frontend/src/api.js:1` vs. `backend/app/main.py:4`), and the persistence layer is unwired (`backend/app/db.py:3-4` never imported by `backend/app/main.py`). Per ui-fog-signals.md verification rule 4, architecture_fog covers module structure and coupling; per the template it is also the default when the problem is structural. The weakest boundary is a module/structure contract defect, so the fog classification and the boundary agree. `user_implied_fog_type: unknown` (no user-intent artifact was supplied in this fixture run, so no intent conflict can be detected); `diagnosis_conflict: false`; `escalation_recommended: false` (high-confidence diagnosis with directly cited evidence, and the workflow registry contains a matching workflow).

## 7. Evidence
The fixture contains exactly eight files — verified by a recursive listing — so claims about absence (no Dockerfile, no tests, no build tooling) rest on the full inventory, not on sampling. The run contract is the key seam: `README.md:5` says "`docker compose up`", `docker-compose.yml:3` and `docker-compose.yml:5` declare `build: ./backend` / `build: ./frontend`, and no Dockerfile exists in either directory. The API contract is mismatched: `frontend/src/api.js:1` declares `/api/v1/items` while `backend/app/main.py:4` serves `/items`, and `docker-compose.yml:1-5` defines no proxy. The persistence layer is unwired: `backend/app/db.py:3-4` defines `conn()` but `backend/app/main.py:1-6` never imports it, returning a hardcoded list at `backend/app/main.py:6`. The frontend cannot build: `frontend/src/App.jsx:1` is JSX while `frontend/package.json:1` declares only a name. Finally, `backend/requirements.txt:1` lists only `fastapi`, omitting any ASGI server.

Logic trace: The chain from evidence to the weakest-boundary conclusion is: (a) the repo's only entry point is `docker compose up` (`README.md:5`); (b) compose declares builds from `./backend` and `./frontend` (`docker-compose.yml:3,5`); (c) the recursive inventory shows neither directory contains a Dockerfile; therefore (d) the documented entry point cannot execute — a Contract Mismatch between what the README/compose declare and what the tree actually contains. The other defects corroborate the same weakness type rather than competing with it: the API path mismatch (`frontend/src/api.js:1` vs. `backend/app/main.py:4`), the JSX-without-toolchain mismatch (`frontend/src/App.jsx:1` vs. `frontend/package.json:1`), and the unwired DB module (`backend/app/db.py:3-4` vs. `backend/app/main.py:1-6`) are all declared-contract-without-counterpart failures, and none of them is caught because the repo has zero automated validation.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L5
    quote: "`docker compose up`."
    supports_claim: "The repo's only run instruction is `docker compose up`, which is unfulfillable because the compose build contexts have no Dockerfiles."
  - file: docker-compose.yml
    lines: L2-L5
    quote: |-
        backend:
          build: ./backend
        frontend:
          build: ./frontend
    supports_claim: "Compose declares two services built from ./backend and ./frontend; neither directory contains a Dockerfile, so the declared build contract has no implementation."
  - file: backend/app/main.py
    lines: L4
    quote: '@app.get("/items")'
    supports_claim: "Backend serves GET /items, which does not match the /api/v1/items base the frontend declares; no /api/v1 prefix or proxy exists anywhere."
  - file: backend/app/main.py
    lines: L6
    quote: "return []"
    supports_claim: "The route returns a hardcoded empty list and never uses the db.py persistence module."
  - file: backend/app/db.py
    lines: L3-L4
    quote: |-
        def conn():
            return sqlite3.connect("app.db")
    supports_claim: "A SQLite connection helper exists but is never imported or called by backend/app/main.py - unwired dead code."
  - file: backend/requirements.txt
    lines: L1
    quote: "fastapi"
    supports_claim: "Only fastapi is declared; no ASGI server (uvicorn) is listed, so the backend could not be served even with a working image."
  - file: frontend/src/api.js
    lines: L1
    quote: "export const API = '/api/v1/items';"
    supports_claim: "Frontend declares /api/v1/items as the API base, which mismatches the served /items route and is never imported by App.jsx."
  - file: frontend/src/App.jsx
    lines: L1
    quote: "export default function App() { return <div>app</div>; }"
    supports_claim: "The only UI component is a static div with no imports, no flows, no routing - and JSX with no build tooling in package.json."
  - file: frontend/package.json
    lines: L1
    quote: "{\"name\": \"frontend\"}"
    supports_claim: "No dependencies, scripts, or module type - the JSX in App.jsx cannot be built or executed as shipped."
```

## 9. Why this boundary matters
Because the run contract is the repo's only documented entry point, its failure means the project cannot be started, tested, or demoed at all. Every downstream activity — adding tests, wiring the DB, building a real UI — is blocked at the first step, and the failure is invisible to tooling: nothing validates the compose contract, so the repo can sit broken indefinitely without any signal. The correlated contract breaks compound the cost: a developer who fixes the Dockerfiles would still hit a frontend that cannot build (`frontend/src/App.jsx:1` vs. `frontend/package.json:1`), an API path that 404s (`frontend/src/api.js:1` vs. `backend/app/main.py:4`), and a DB layer that nothing uses (`backend/app/db.py:3-4`). In short, the repo's declared architecture exists only on paper, and no mechanism exists to notice.

## 10. Candidate next steps
1. Make the entry point real: add `backend/Dockerfile` and `frontend/Dockerfile` (or replace the compose build contexts with published images) so `docker compose up` from `README.md:5` succeeds.
2. Reconcile the API contract: serve `/api/v1/items` from `backend/app/main.py:4` (or change `frontend/src/api.js:1` to `/items`) and document the contract in the README.
3. Wire or remove the persistence layer: have the `/items` route call `conn()` from `backend/app/db.py:3-4`, or delete the module.
4. Add a frontend build path: either add a minimal Vite/Babel setup to `frontend/package.json:1` or replace the JSX in `frontend/src/App.jsx:1` with plain JavaScript.
5. Add the first automated check: a test hitting `GET /items` (e.g., FastAPI `TestClient`) plus a CI step running `docker compose build`, so the contracts are enforced from now on.

## 11. Recommended next step
Add the two Dockerfiles (or replace the compose build contexts with runnable images) so the README's `docker compose up` (`README.md:5`) actually starts the stack. It is the smallest change with the highest leverage: it is the only step that unblocks the documented entry point, it is directly evidenced by the compose-vs-tree mismatch (`docker-compose.yml:3,5` vs. the empty `backend/` and `frontend/` build contexts), and it turns the repo from "cannot run" into "runs, then exposes the next contract breaks" — the precondition for every other candidate step.

## 12. Recommended workflow
`architecture-implementation-workflow` from `skills/workflow-planner/references/workflow-registry.yaml` (registry line 848): "For architecture/refactoring problems. Aligns domain, creates refactoring spec, decomposes into issues, and implements via TDD." It is the registry's architecture counterpart of the product/ui/docs implementation workflows and matches the `architecture_fog` classification and the structural/contract nature of the weakest boundary. The registry has no architecture-specific diagnostic-only workflow (ui_fog has `ui-diagnostic-workflow`; architecture has none), so the implementation workflow is the correct registry-grounded routing; execution mode `guided_execution` is one of its allowed modes (registry lines 858-861), and the human review gates in its steps preserve the no-unattended-implementation boundary of this skill.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/full-stack
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
evidence:
  - "README.md (line 5): only run instruction is `docker compose up`"
  - "docker-compose.yml (lines 2-5): services backend/frontend declare build: ./backend and build: ./frontend"
  - "backend/ and frontend/ (recursive listing): no Dockerfile exists in either build context"
  - "frontend/src/api.js (line 1): declares API base /api/v1/items"
  - "backend/app/main.py (line 4): serves GET /items, not /api/v1/items"
  - "backend/app/db.py (lines 3-4): conn() defined but never imported by backend/app/main.py"
  - "frontend/src/App.jsx (line 1): JSX with no build tooling in frontend/package.json (line 1)"
  - "backend/requirements.txt (line 1): only fastapi, no ASGI server"
weakest_boundary:
  type: Contract Mismatch
  evidence: "README.md:5 documents `docker compose up` as the run path; docker-compose.yml:3 and :5 declare build contexts ./backend and ./frontend; neither directory contains a Dockerfile (recursive listing of the 8-file fixture)"
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
Prompt for `workflow-planner`:

"Route this repository sensemaking brief (artifact_id: repository_sensemaking_brief; primary_fog_type: architecture_fog; weakest_boundary: Contract Mismatch; source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md) to the `architecture-implementation-workflow` in `guided_execution` mode. Context: corpus/full-stack is an 8-file full-stack scaffold whose documented entry point is broken — README.md:5 says `docker compose up`, docker-compose.yml:3,5 declare build contexts ./backend and ./frontend, and neither directory contains a Dockerfile. Additionally, the frontend API base (/api/v1/items, frontend/src/api.js:1) does not match the served route (/items, backend/app/main.py:4), the JSX component (frontend/src/App.jsx:1) has no build tooling (frontend/package.json:1), and the SQLite layer (backend/app/db.py:3-4) is never wired into the app. Produce the orchestration plan without implementing anything."
