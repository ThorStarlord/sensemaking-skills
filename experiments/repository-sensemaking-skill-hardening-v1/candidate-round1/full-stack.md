# Repository Sensemaking Brief

## 1. Repository goal

The repository self-describes as a full-stack application with a single documented run command: `README.md:5` ("`docker compose up`.") and `README.md:3` ("A full-stack application."). The apparent intent (OBSERVED from the file inventory, DERIVED from the layout) is a runnable two-tier stack — a Python/FastAPI backend (`backend/app/main.py:2-6`), a SQLite persistence layer (`backend/app/db.py:3-4`), a React-style JSX frontend (`frontend/src/App.jsx:1`) with a centralized API base (`frontend/src/api.js:1`), and docker-compose orchestration (`docker-compose.yml:1-5`). As shipped, the goal is unfulfilled: the documented entry point cannot execute (see Section 6).

## 2. Current shape

**Inventory (OBSERVED)** — the fixture is exactly 8 files (recursive listing; no hidden files, no Dockerfiles, no tests, no CI, no docs directory):

- `README.md` (5 lines) — title, one-line description, one run instruction.
- `docker-compose.yml` (5 lines) — two services, `backend` and `frontend`, each declaring a build context.
- `backend/requirements.txt` (1 line) — declares `fastapi`.
- `backend/app/main.py` (6 lines) — FastAPI app and one route.
- `backend/app/db.py` (4 lines) — SQLite connection helper.
- `frontend/package.json` (1 line) — declares only a name.
- `frontend/src/App.jsx` (1 line) — one JSX component.
- `frontend/src/api.js` (1 line) — one exported API-base constant.

**Runtime flow (Architecture Reconstruction)** — what starts the system, what controls it, where state lives, where external systems enter, where validation happens, and where responsibility becomes unclear:

- **Startup path**: the only documented start is `README.md:5` ("`docker compose up`."). Compose declares `build: ./backend` (`docker-compose.yml:3`) and `build: ./frontend` (`docker-compose.yml:5`). Neither build context contains a Dockerfile (OBSERVED via the exhaustive recursive inventory). The hop from "compose up" to a running system therefore cannot be traced past the build step — recorded as **UNKNOWN** rather than invented: no executed path exists.
- **Orchestration**: `docker-compose.yml:1-5` is the only orchestrator. It declares no `ports:`, no `depends_on:`, no volumes — so even if images built, the frontend container could not reach the backend and nothing would be published to a host.
- **Backend entry point**: `backend/app/main.py:2` (`app = FastAPI()`) creates the app; `backend/app/main.py:4-6` registers `GET /items`, returning a hardcoded empty list. There is no `if __name__ == "__main__"` block and no server command; `backend/requirements.txt:1` declares only `fastapi` — the ASGI server (e.g. uvicorn) that would actually serve the app is **absent from the declared dependency set**.
- **Domain/core logic**: none. The only behavior is `backend/app/main.py:6` (`return []`) — no computation, no data access, no business rule.
- **Persistence/state**: `backend/app/db.py:3-4` defines `conn()` returning `sqlite3.connect("app.db")`. This is the only state boundary in the repo (a SQLite file), but **no module imports or calls it**: `backend/app/main.py:1` imports only `fastapi`. The state boundary is unreachable; `app.db` could never be created by any executed path. No other state exists (no env vars, no caches, no queues).
- **External integration points**: none are wired. `frontend/src/api.js:1` declares the client's API base as `/api/v1/items`, but nothing imports it — `frontend/src/App.jsx:1` renders a static `<div>app</div>` and never calls the API. The frontend→backend boundary is declared but disconnected, and the declared path does not match the served route (`/items`, `backend/app/main.py:4`).
- **Output boundary**: the HTTP response `[]` from `backend/app/main.py:6`. Nothing else leaves the system.
- **Where responsibility becomes unclear**: (a) the compose→image seam — `docker-compose.yml:3,5` declare builds that have no implementation; (b) the app→persistence seam — `backend/app/db.py:3-4` exists but is never invoked by `backend/app/main.py:1-6`; (c) the frontend→backend seam — `frontend/src/api.js:1` is orphaned and path-mismatched.

**Dependency semantics** (each claim classified):
- `fastapi` — **declared** (`backend/requirements.txt:1`) and **used** (imported at `backend/app/main.py:1`), but **not runtime-proven**: no server dependency is declared, so the app cannot be served as-is.
- uvicorn (or any ASGI server) — **absent** from the manifest, i.e. needed-but-undeclared for the runtime path.
- `sqlite3` — **used** only by the unwired `backend/app/db.py:1`; not part of any executed path (state module is dead code).
- React/bundler for the frontend — **absent** from `frontend/package.json:1` although `frontend/src/App.jsx:1` is JSX (used-but-undeclared; the manifest and the code contradict each other).

## 3. Strong signals

- **Legible intended architecture**: the top-level split into `backend/` and `frontend/` with a root `docker-compose.yml:2-5` declaring both services makes the intended shape (API + UI + container orchestration) readable from the layout alone.
- **Coherent minimal backend entry**: `backend/app/main.py:2-6` is a valid, idiomatic FastAPI app with a properly decorated route — the seed of a real API exists.
- **Persistence intent present**: `backend/app/db.py:3-4` uses the standard `sqlite3` idiom; the author knew a state layer was needed.
- **API-base centralization**: `frontend/src/api.js:1` keeps the endpoint in one constant rather than scattering URL strings — a good habit even though the constant is currently orphaned.
- **Compose-first intent**: a root `docker-compose.yml` signals a reproducible-run goal (`README.md:5`).

## 4. Missing pieces

- **Dockerfiles** for both compose build contexts (`docker-compose.yml:3,5` reference `./backend` and `./frontend`; neither directory contains one — OBSERVED by exhaustive listing).
- **Frontend build tooling and dependencies**: `frontend/package.json:1` declares only `{"name": "frontend"}` — no React, no bundler, no scripts — so `frontend/src/App.jsx:1` (JSX) cannot compile.
- **ASGI server dependency**: `backend/requirements.txt:1` lists only `fastapi`; nothing declares the server that would actually run `backend/app/main.py:2`.
- **Wiring**: `backend/app/main.py:1-6` never imports `backend/app/db.py:3-4`; `frontend/src/App.jsx:1` never imports `frontend/src/api.js:1`.
- **Network contract**: `docker-compose.yml:1-5` defines no `ports:` mapping and no proxy/rewrite, so the frontend could not reach the backend even if both built.
- **Route-path agreement**: `frontend/src/api.js:1` targets `/api/v1/items`; the backend serves `/items` (`backend/app/main.py:4`) — no `/api/v1` prefix exists anywhere.
- **Validation of any kind**: no tests, no CI, no schemas, no lint config, no input validation — zero automated checks (see candidate C5 in Section 6).

## 5. Improvement opportunities

- Add a minimal smoke test (import the app, assert routes) once the app is runnable, so contract breaks like the ones in Section 4 become visible.
- Declare a typed response (Pydantic model) for `GET /items` (`backend/app/main.py:4-6`) — cheap, and establishes the API contract formally.
- Add `ports:` and `depends_on:` to `docker-compose.yml:1-5` so the stack is actually network-connected.
- Document the API contract (routes, base path) in `README.md` so `frontend/src/api.js:1` and `backend/app/main.py:4` cannot drift silently again.
- Add `.dockerignore` and healthchecks once Dockerfiles exist — minor, non-urgent hygiene.

## 6. Weakest boundary

Five candidate boundaries were generated and scored (evidence strength / severity / blast radius / goal relevance / downstream blocking / uncertainty), then one selected:

| # | Candidate boundary | evidence | severity | blast radius | goal relevance | downstream blocking | uncertainty |
|---|---|---|---|---|---|---|---|
| C1 | Run/build contract: `README.md:5` documents `docker compose up`; `docker-compose.yml:3,5` declare builds from `./backend` and `./frontend`; neither directory contains a Dockerfile, and the frontend context has no build tooling (`frontend/package.json:1`) | strong | high | high | high | high | low |
| C2 | Frontend buildability contract: `frontend/package.json:1` (name only) vs JSX in `frontend/src/App.jsx:1` | strong | high | medium | high | high | low |
| C3 | Frontend↔backend API contract: `frontend/src/api.js:1` (`/api/v1/items`) vs `backend/app/main.py:4` (`/items`) | strong | medium | medium | high | medium | low |
| C4 | Persistence wiring: `backend/app/db.py:3-4` defines the only state boundary but is never imported by `backend/app/main.py:1-6`; `main.py:6` hardcodes `[]` | strong | medium | medium | medium | medium | low |
| C5 | Zero validation: no tests, CI, schemas, or checks exist anywhere in the 8-file inventory | strong | medium | high | medium | medium | low |

**Selection rule applied**: C1 wins on the strongest combination of high consequence (the documented entry point fails before any application code runs), strong evidence (direct file citations plus an exhaustive inventory), centrality to the repo's stated goal (a runnable full-stack app, `README.md:3,5`), and downstream blocking (every other improvement — wiring the DB, building a real UI, adding tests — presupposes a runnable stack). C2 is a sub-instance of C1 (a frontend Dockerfile would still have nothing to build). C3 and C4 are latent (nothing executes those seams today), and C5 is an amplifier, not the cause.

```text
Boundary: The documented run/build contract of the stack — README.md:5 ("docker compose up") and docker-compose.yml:3,5 (build: ./backend / build: ./frontend) versus what the tree actually contains.
Observed contract: The repo is runnable as a full-stack application via one command; docker-compose builds both halves from their declared contexts; the frontend half is a buildable UI.
Observed violation or uncertainty: Neither build context contains a Dockerfile (OBSERVED — exhaustive recursive inventory of the 8-file fixture shows zero Dockerfiles and zero hidden files), and the frontend context additionally has no build manifest at all (frontend/package.json:1 declares only a name while frontend/src/App.jsx:1 is JSX), so no image can be produced and the documented entry point cannot execute.
Evidence: README.md:5; docker-compose.yml:3; docker-compose.yml:5; frontend/package.json:1; frontend/src/App.jsx:1; recursive directory inventory (absence of Dockerfiles).
Weakness type: **Ghost Features**
Logic trace: README.md:5 is the repository's only run instruction and points at docker-compose; docker-compose.yml:3 and :5 declare build surfaces named ./backend and ./frontend; the exhaustive recursive inventory of the fixture (exactly 8 files) shows no Dockerfile in either directory, and frontend/package.json:1 declares no dependencies or build scripts to support the JSX at frontend/src/App.jsx:1. Therefore the functionality documented in the README — "A full-stack application" (README.md:3) runnable via `docker compose up` (README.md:5) — has no corresponding implementation: the declared build surfaces have no build files, and the declared frontend has no toolchain. Per weakness-types.md, Ghost Features is "Functionality mentioned in documentation that has no corresponding implementation," and per SKILL.md GAP-6 mapping a declared surface with no implementation is Ghost Features (the same mapping used for declared-but-unused dependencies). The other defects corroborate the same pattern rather than competing with it: frontend/src/api.js:1 declares an API base the backend never serves (backend/app/main.py:4), backend/app/db.py:3-4 declares persistence nothing imports, and backend/requirements.txt:1 declares a runtime without a server. Every seam is a documented/declared surface whose counterpart does not exist. Because the selected type is Ghost Features, the validator's D5 HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT warning applies by design and a substantive human audit is required before final approval — this is expected, not a classification error. Contract Mismatch was considered (see Alternatives) but its canonical definition — a file claiming one format while being another — describes wrong-content claims, not absent counterparts; Ghost Features describes this boundary precisely.
Failure consequence: `docker compose up` (README.md:5) fails at the build step ("Dockerfile not found"), so the project cannot be started, demoed, or tested; every downstream activity — wiring persistence, building a real UI, adding tests — is blocked at the first step, and nothing in the repo signals the break because no tooling validates the compose contract.
Confidence: high. The violation is directly observed (file citations + full-inventory absence), not inferred. Residual uncertainty is limited to intent (whether Dockerfiles or published images were intended) and would be resolved by checking the fixture's own generation harness — it does not affect the classification.
Alternatives considered:
- C2 (frontend buildability, Contract Mismatch): real and strong, but subsumed by C1 — it is the same run-contract failure viewed from the frontend context; a Dockerfile there would still build nothing.
- C3 (API contract, Contract Mismatch): strong evidence (api.js:1 vs main.py:4) but latent — frontend/src/App.jsx:1 never imports api.js, so no executed path hits the mismatch today; it becomes reachable only after C1 is fixed.
- C4 (unwired persistence, Ghost Features): strong evidence (db.py:3-4 never imported), but it does not block the documented entry point and is a missing-feature instance of the same declared-without-implementation pattern.
- C5 (Zero Validation): real (no tests/CI anywhere) but it is the amplifier — it explains why nothing caught C1-C4, not what is broken; choosing it would describe the absence of a safety net rather than the boundary that actually fails.
```

---

## 6.5. Problem classification (fog type)

**primary_fog_type: architecture_fog.** The evidence points at structural/contractual failure, not at screens, user needs, or documentation gaps:

- The frontend↔backend seam is structurally broken before it exists: `frontend/src/api.js:1` declares `/api/v1/items`, `backend/app/main.py:4` serves `/items`, and nothing wires the two (`frontend/src/App.jsx:1` never imports api.js).
- Modules are unwired: `backend/app/db.py:3-4` is never imported by `backend/app/main.py:1-6` — the module structure prevents the state layer from landing.
- The entry point cannot flow: `docker-compose.yml:3,5` declare build contexts with no Dockerfiles — a structural mismatch between the declared entry point and the tree.

**ui_fog was evaluated against the UI Fog Signals Registry** because frontend code exists (`frontend/src/App.jsx:1`). Tier 1.1 (missing UI flow documentation) and Tier 1.4 (design-system absence) are technically absent, but both are vacuous: the entire UI is one static element (`frontend/src/App.jsx:1`) — zero screens, zero routing, zero components, zero styling — so the registry's qualitative gate ("Is the primary problem about 'how the UI works' vs 'what the UI should do'?") resolves to *neither*: there is no UI complexity to be foggy about. Tier 2/3 signals are likewise absent (no tests, no a11y concerns, no state management — there is nothing to test or manage). Per ui-fog-signals.md verification rule 4 and SKILL.md's fog classification, module structure and coupling defects are `architecture_fog`.

**product_fog rejected**: the README's "full-stack application" (`README.md:3`) is a scaffold's self-description, not a product contract with user needs; per SKILL.md ghost-feature reasoning, a feature that exists only partially *because the architecture cannot support it* (no Dockerfiles, no toolchain, no wiring) classifies as `architecture_fog`, not `product_fog`. **docs_fog rejected**: the documentation is minimal but not the defect locus — the README accurately describes intent, and the code is incoherent (unwired modules), which is the opposite of the coherent-but-undocumented case docs_fog covers. **escalation_recommended: false** — the diagnosis rests on direct, multiply-cited evidence with low uncertainty, and the workflow registry contains a matching workflow (Section 12). **user_implied_fog_type: unknown** (GAP-8: no user-intent artifact exists for this fixture run), **diagnosis_conflict: false** (no stated intent to conflict with).

## 7. Evidence

All claims below trace to files actually opened during this analysis (OBSERVED), with line references; the fixture is exactly 8 files, so absence claims rest on the full inventory, not on sampling.

- `README.md:3` claims "A full-stack application." and `README.md:5` gives the only run instruction: "`docker compose up`." — the documented run contract (OBSERVED).
- `docker-compose.yml:1-5` declares `services: backend` with `build: ./backend` (`docker-compose.yml:3`) and `services: frontend` with `build: ./frontend` (`docker-compose.yml:5`); the recursive listing of `corpus/full-stack` shows no Dockerfile in either directory and no hidden files (OBSERVED) — the declared build surfaces have no implementation (DERIVED).
- `frontend/package.json:1` is `{"name": "frontend"}` — no dependencies, no scripts (OBSERVED) — while `frontend/src/App.jsx:1` is JSX that cannot compile without React and a bundler (DERIVED).
- `frontend/src/api.js:1` declares `export const API = '/api/v1/items';` (OBSERVED) but `backend/app/main.py:4` serves `@app.get("/items")` (OBSERVED) — the declared API base matches no served route (DERIVED); no reverse proxy exists in `docker-compose.yml:1-5` (OBSERVED).
- `backend/app/db.py:3-4` defines `conn()` → `sqlite3.connect("app.db")` (OBSERVED), but `backend/app/main.py:1` imports only `from fastapi import FastAPI` and the route returns a hardcoded `[]` at `backend/app/main.py:6` (OBSERVED) — the persistence boundary is unwired (DERIVED).
- `backend/requirements.txt:1` declares only `fastapi` (OBSERVED); no ASGI server is declared, so the app has no declared way to be served (DERIVED).
- `docker-compose.yml:1-5` declares no `ports:` mapping (OBSERVED) — even with images, the frontend could not reach the backend (DERIVED).
- No tests, CI configuration, schemas, or lint configuration exist anywhere in the 8-file inventory (OBSERVED) — zero validation (DERIVED: nothing checks any of the contracts above).

**Logic trace:** The chain from evidence to the weakest-boundary conclusion: (a) the repo's only documented entry point is `docker compose up` (`README.md:5`); (b) that command builds two services from `./backend` and `./frontend` (`docker-compose.yml:3,5`); (c) the exhaustive inventory shows neither build context contains a Dockerfile, and the frontend context has no build manifest (`frontend/package.json:1` supports only a name while `frontend/src/App.jsx:1` is JSX); (d) therefore the documented full-stack functionality (`README.md:3`) has no corresponding implementation and the entry point cannot execute — a Ghost Features failure (documented functionality with no reachable implementation, per weakness-types.md, confirmed by the GAP-6 declared-surface mapping). The corroborating breaks (api.js:1 vs main.py:4; db.py:3-4 unwired; requirements.txt:1 without a server) are the same declared-without-counterpart pattern at every other seam, and none of them is caught because zero validation exists (C5). This reasoning is what selects the run/build contract as the weakest boundary over the latent seams.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L1-L5
    quote: "# fullstack-app\n\nA full-stack application.\n\n`docker compose up`."
    supports_claim: "The repo's only run instruction is `docker compose up`; the documented full-stack functionality has no corresponding implementation (no Dockerfiles, no frontend toolchain)."
  - file: docker-compose.yml
    lines: L1-L5
    quote: "services:\n  backend:\n    build: ./backend\n  frontend:\n    build: ./frontend"
    supports_claim: "Compose declares two services built from ./backend and ./frontend; neither directory contains a Dockerfile, so the declared build surfaces have no implementation."
  - file: backend/app/main.py
    lines: L1
    quote: "from fastapi import FastAPI"
    supports_claim: "main.py imports only fastapi - it never imports db.py, so the persistence module is unwired."
  - file: backend/app/main.py
    lines: L4-L6
    quote: "@app.get(\"/items\")\ndef items():\n    return []"
    supports_claim: "The backend serves GET /items returning a hardcoded empty list - no state boundary is consulted."
  - file: backend/app/db.py
    lines: L3-L4
    quote: "def conn():\n    return sqlite3.connect(\"app.db\")"
    supports_claim: "The only state boundary in the repo (SQLite file) is defined here but never reached by any executed path."
  - file: backend/requirements.txt
    lines: L1
    quote: "fastapi"
    supports_claim: "Only fastapi is declared - no ASGI server, so the app has no declared way to be served."
  - file: frontend/package.json
    lines: L1
    quote: "{\"name\": \"frontend\"}"
    supports_claim: "The frontend manifest declares only a name - no dependencies or build scripts for the JSX in App.jsx."
  - file: frontend/src/App.jsx
    lines: L1
    quote: "export default function App() { return <div>app</div>; }"
    supports_claim: "The entire UI is one static element that never imports api.js - no screens, flows, or interactions exist (rejects ui_fog; the seam is orphaned)."
  - file: frontend/src/api.js
    lines: L1
    quote: "export const API = '/api/v1/items';"
    supports_claim: "The declared API base /api/v1/items does not match the served route /items (backend/app/main.py:4) and nothing imports it."
```

## 9. Why this boundary matters

The run/build contract is the repository's only documented entry point (`README.md:5`), so its failure means the project cannot be started, tested, or demoed at all. Every downstream activity — wiring the persistence layer (`backend/app/db.py:3-4`), building a real UI (`frontend/src/App.jsx:1`), adding tests — is blocked at the first step, and the failure is invisible to tooling: nothing validates the compose contract, so the repo can sit broken indefinitely without any signal. The correlated breaks compound the cost: a developer who adds the missing Dockerfiles would still hit a frontend that cannot build (`frontend/package.json:1` vs `frontend/src/App.jsx:1`), an API path that 404s (`frontend/src/api.js:1` vs `backend/app/main.py:4`), and a DB layer that nothing uses. In short, the repo's declared architecture exists only on paper, and no mechanism exists to notice.

## 10. Candidate next steps

1. **Repair the build contract**: add `backend/Dockerfile` and `frontend/Dockerfile` (or replace the compose build contexts in `docker-compose.yml:3,5` with published images) so `docker compose up` (`README.md:5`) succeeds. Highest leverage — unblocks the only documented entry point.
2. **Declare the runtime path**: add the ASGI server to `backend/requirements.txt:1` (e.g. `uvicorn`) and a start command, so `backend/app/main.py:2` has a declared way to be served.
3. **Reconcile the API contract**: align `frontend/src/api.js:1` (`/api/v1/items`) with the served route `backend/app/main.py:4` (`/items`) — pick one canonical base path — and wire `frontend/src/App.jsx:1` to actually call it.
4. **Wire the persistence boundary**: import and call `backend/app/db.py:3-4` from `backend/app/main.py` (replacing the hardcoded `return []` at `main.py:6`), or delete the dead module.
5. **Add validation**: a minimal smoke test/CI check (app imports, route exists, compose config parses) so the class of contract breaks identified here becomes detectable.

## 11. Recommended next step

Add the two Dockerfiles (or replace the compose build contexts in `docker-compose.yml:3,5` with runnable images) so the README's `docker compose up` (`README.md:5`) actually starts the stack. It is the smallest concrete action with the highest leverage: it is the only step that unblocks the documented entry point, it is directly evidenced by the compose-vs-tree mismatch (`docker-compose.yml:3,5` vs the empty `backend/` and `frontend/` build contexts), and it turns the repo from "cannot run" into "runs, then exposes the next contract breaks" — the precondition for every other candidate step.

## 12. Recommended workflow

**`architecture-implementation-workflow`** (id verified against `skills/workflow-planner/references/workflow-registry.yaml`, lines 848-904; allowed execution modes: `guided_execution`, `autonomous_execution`, registry lines 858-860).

**Recommended execution mode: `guided_execution`** — one of the workflow's allowed modes; recommending it is a diagnostic handoff only, no implementation is performed here.

**Why this workflow**: the primary fog type is `architecture_fog` (Section 6.5) — unwired modules (`backend/app/db.py:3-4`, `frontend/src/api.js:1`), a broken entry-point-to-flow chain (`docker-compose.yml:3,5`), and manifest/code contradictions (`frontend/package.json:1` vs `frontend/src/App.jsx:1`). The workflow's chain — docs-aligner (domain alignment) → to-prd (refactoring/architecture spec) → to-issues → triage → tdd — fits a "repair module and build contracts" task.

**Why not the closest alternatives**: `ui-implementation-workflow` (registry lines 748-811) presumes screens/flows/design problems; the UI is one static element (`frontend/src/App.jsx:1`), so UI work is premature. `product-implementation-workflow` (lines 644-714) presumes user-need discovery; there is no product contract beyond the scaffold self-description. `docs-implementation-workflow` (lines 812-847) would document behavior the code cannot yet exhibit. `fast-path-workflow`/`full-fog-workflow` are diagnostic+orchestration chains, not implementation workflows, and are not what a handoff from this brief should invoke.

**Preconditions**: none block the recommendation. Execution would first produce the refactoring spec (to-prd step) that formalizes the build-contract repair from Section 11 before any code changes.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/full-stack
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (lines 3-5): documents the repo as a full-stack application runnable via `docker compose up`"
  - "docker-compose.yml (lines 1-5): services backend/frontend declare build: ./backend and build: ./frontend; recursive inventory shows no Dockerfile in either build context"
  - "backend/app/main.py (lines 1-6): FastAPI app serving GET /items with a hardcoded empty list; never imports db.py"
  - "backend/app/db.py (lines 3-4): defines sqlite3 conn() persistence but is never imported by main.py"
  - "backend/requirements.txt (line 1): declares only fastapi - no ASGI server for the runtime path"
  - "frontend/package.json (line 1): declares only a name - no dependencies or build scripts for the JSX in App.jsx"
  - "frontend/src/App.jsx (line 1): static JSX div that never imports api.js"
  - "frontend/src/api.js (line 1): declares API base /api/v1/items which does not match the served route /items"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-06-01T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

"Route this repository sensemaking brief (artifact_id: repository_sensemaking_brief; primary_fog_type: architecture_fog; weakest_boundary: Ghost Features — documented full-stack run functionality with no corresponding implementation; source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md) to the `architecture-implementation-workflow` in `guided_execution` mode. Context: corpus/full-stack is an 8-file full-stack scaffold whose documented entry point is broken — README.md:5 says `docker compose up`, docker-compose.yml:3,5 declare build contexts ./backend and ./frontend, and neither directory contains a Dockerfile. Additionally, the frontend API base (/api/v1/items, frontend/src/api.js:1) does not match the served route (/items, backend/app/main.py:4), the JSX component (frontend/src/App.jsx:1) has no build tooling (frontend/package.json:1), the SQLite layer (backend/app/db.py:3-4) is never wired into the app, and backend/requirements.txt:1 declares no ASGI server. Produce the orchestration plan without implementing anything; the first implementation step should repair the build contract (Section 11 of the brief)."
