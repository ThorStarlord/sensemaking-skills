# Repository Sensemaking Brief — corpus/web-frontend

## 1. Repository goal
This repository is a minimal single-page dashboard frontend ("dashboard-ui"): a hash-based router (`src/router.js`), one screen (`src/components/dashboard.js`) that fetches data from a backend endpoint (`/api/data` via `src/api.js`) and renders it, and an HTML entry point (`src/index.html`) intended to be served by a static file server (`python -m http.server 8000`, per `package.json:1`). The apparent goal is a thin, dependency-free dashboard UI that talks to an implied backend API — but the contract with that backend, and the way the frontend is loaded, are both unstated.

## 2. Current shape
Seven files, with no subdirectories beyond `src/components/` (verified by recursive listing of the corpus tree):
- `package.json` (root) — name "dashboard-ui"; single `start` script `python -m http.server 8000`; no dependencies, no module type, no test/lint/build scripts.
- `src/index.html` — single page with `<div id="app">` and a classic `<script src="app.js">` include.
- `src/app.js` — entry point: imports dashboard and router, registers `/dashboard`, calls `router.start()`.
- `src/router.js` — 6-line hash router with `register`/`start`/`dispatch`.
- `src/api.js` — one function, `loadData()`, fetching `/api/data`.
- `src/components/dashboard.js` — `renderDashboard()` dumping fetched JSON into `#app`.
- `src/components/widget.js` — a `widget(title, body)` template helper that nothing imports.

There is no README, no `docs/` directory, no tests, no stylesheets, no build or lint tooling.

## 3. Strong signals
- Routing is centralized in a single small file (`src/router.js:1-6`) with a clean `register`/`start`/`dispatch` API — routing logic is not scattered across files.
- The codebase is tiny and readable; module boundaries are *intended* via ES imports (`src/app.js:1-2`).
- Data access is isolated in one wrapper (`src/api.js:1-2`), a nascent data layer.
- No framework lock-in; vanilla ES modules and hash routing keep the surface minimal.

## 4. Missing pieces
- Documentation of any kind: no README.md, no `docs/`, no flow or screen specs (UI Fog Tier 1.1 signal).
- A working module-loading contract: `src/index.html:3` loads `app.js` as a classic script and `package.json:1` declares no module type, yet `src/app.js:1-2` uses ES module `import` statements — the app cannot execute in a browser as shipped.
- Automated checks: no test files, no test script in `package.json:1`, no CI (Zero Validation).
- A design system or any styling: no CSS files, no design tokens, no component library (UI Fog Tier 1.4 signal).
- An API contract for the `/api/data` endpoint the app depends on (Implicit Dependency).
- Accessibility (no `aria-`/`alt` anywhere), responsive design, and loading/error/empty states (UI Fog Tier 2.2, 2.3, 3.3 signals).
- `widget.js` is wired to nothing: it is exported but never imported (orphaned component).

## 5. Improvement opportunities
- Add a short README documenting the one user flow and the `/api/data` contract.
- Fix the script/module mismatch and add a smoke-test script to `package.json:1`.
- Either use `widget.js` inside `dashboard.js` or delete it.
- Introduce a minimal CSS/token layer before any visual work.
- Add loading and error states to `renderDashboard` (`src/components/dashboard.js:3`).

## 6. Weakest boundary
The weakest boundary is the **module-loading contract** between the HTML entry point, the JS module system, and the package metadata: `src/index.html:3` includes `<script src="app.js">` as a classic script, `src/app.js:1-2` opens with ES module `import` statements, and `package.json:1` declares neither `"type": "module"` nor any bundler. A browser parsing `app.js` as a classic script hits a `SyntaxError` on the `import` statement, so the only screen never renders and the repo's only start command (`python -m http.server 8000`) serves a dead page.

**Weakness type:** Contract Mismatch

Logic trace: `src/index.html:3` (classic script include) and `package.json:1` (no module type, no build step) define how the app is loaded, while `src/app.js:1-2` (ES module imports) define how the code is written; the two contracts are incompatible, and the mismatch is unenforced — no test or build step could catch it because none exists (`package.json:1` has no test/build scripts). Therefore the seam between "how the repo is declared to run" and "how the code actually runs" is the most fragile boundary in the repository, and it is a Contract Mismatch rather than a design, documentation, or validation gap (the missing tests are a consequence of the same unenforced contract, not the root defect).

## 6.5. Problem classification (fog type)
**primary_fog_type: ui_fog.** This is a frontend repository (HTML entry point plus JS screens), and the UI Fog Signals Registry check yields 2+ Tier 1 signals: (1.1) user flows/screens are entirely undocumented — no README.md, no `docs/`, no flow specs, no Figma/Storybook references; (1.4) the design system is absent — no CSS files, no design tokens, no shared component library. Tier 2 signals are also present: (2.1) no UI tests of any kind, (2.2) accessibility never addressed (no `aria-`/`alt` anywhere in `src/index.html` or the components), (2.3) no responsive design (no media queries or breakpoints anywhere). Per the registry decision tree, 2+ Tier 1 signals → STRONG CONFIDENCE `ui_fog`. The weakest boundary (the module contract) is a UI-layer defect — the screen cannot load — so the fog classification and the boundary agree. `user_implied_fog_type: unknown` (no user-intent artifact was supplied in this fixture run, so no intent conflict can be detected); `diagnosis_conflict: false`; `escalation_recommended: false` (high-confidence diagnosis with directly cited evidence, and the workflow registry contains a matching diagnostic workflow).

## 7. Evidence
The repository contains no README.md and no `docs/` directory — verified by a recursive listing of the `corpus/web-frontend` tree — so every claim below rests on direct code inspection. `src/index.html:3` includes `app.js` as a classic script; `src/app.js:1-2` uses ES module `import` statements; `package.json:1` declares neither a module type nor test/build scripts, so the module contract is broken and unenforced. `src/api.js:2` fetches `/api/data`, an endpoint with no backend and no documentation inside this repo. `src/components/dashboard.js:3` renders the raw JSON into `#app` with no loading, error, or empty states. `src/components/widget.js:1` exports a `widget` helper that nothing imports (a grep for "widget" across the repo matches only `widget.js` itself). `src/router.js:5` dispatches hash routes with no fallback for unknown paths.

Logic trace: The cited evidence chains as follows — (a) the app cannot execute: `src/index.html:3` (classic script) + `src/app.js:1-2` (ES imports) + `package.json:1` (no module type) combine into a Contract Mismatch; (b) because it cannot execute, no test could pass, and `package.json:1` has no test script anyway — Zero Validation is a consequence of the unenforced contract, not its root; (c) the only screen is a raw JSON dump (`src/components/dashboard.js:3`) with an implicit `/api/data` dependency (`src/api.js:2`), so the UI layer is both undocumented (Tier 1.1) and unstyled (Tier 1.4). The root defect — the thing that makes the repository's stated goal unreachable — is the module contract, so the weakest boundary is **Contract Mismatch** and the fog type is **ui_fog**.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: src/index.html
    lines: L3
    quote: "<body><div id=\"app\"></div><script src=\"app.js\"></script></body>"
    supports_claim: "Entry point loads app.js as a classic script with no module type, while app.js uses ES module imports - the app cannot execute in a browser as shipped."
  - file: src/app.js
    lines: L1-L3
    quote: |-
      import { renderDashboard } from './components/dashboard.js';
      import { router } from './router.js';
      router.register('/dashboard', renderDashboard);
    supports_claim: "ES module imports and a single hardcoded route registration; /dashboard is the only screen and navigation is undocumented."
  - file: package.json
    lines: L1
    quote: "{\"name\": \"dashboard-ui\", \"scripts\": {\"start\": \"python -m http.server 8000\"}}"
    supports_claim: "No module type declaration, no dependencies, no test/lint/build scripts - the module contract is unenforced and there is zero automated validation."
  - file: src/api.js
    lines: L2
    quote: "  return fetch('/api/data').then(r => r.json());"
    supports_claim: "Implicit dependency on an undocumented /api/data endpoint; no backend exists in the repo and no error handling is present."
  - file: src/components/dashboard.js
    lines: L3
    quote: "  loadData().then(data => { document.getElementById('app').innerHTML = '<pre>' + JSON.stringify(data) + '</pre>'; });"
    supports_claim: "Screen renders a raw JSON dump with no loading, error, or empty states and no component reuse."
  - file: src/components/widget.js
    lines: L1
    quote: "export function widget(title, body) { return `<div class=\"widget\"><h2>${title}</h2>${body}</div>`; }"
    supports_claim: "widget helper is never imported anywhere in the repository - an orphaned component with no clear component boundary."
  - file: src/router.js
    lines: L5
    quote: "  dispatch() { const h = routes[window.location.hash.slice(1)]; if (h) h(); },"
    supports_claim: "Hash-based routing with no fallback or 404 handling for unknown routes; navigation architecture is undocumented."
```

## 9. Why this boundary matters
As shipped, following the repo's own start command (`package.json:1` → `python -m http.server 8000`) and opening the page yields a browser console `SyntaxError` and a permanently empty `#app`. Consequences: the single user flow can never be exercised, so any downstream diagnostic (ui-brief, screen specs) would analyze a screen that never renders; any test added later would fail at load time and be misattributed to the test rather than the contract; and the implicit `/api/data` dependency can never be validated end-to-end. The boundary is also invisible to tooling because nothing validates it — which is exactly why it shipped broken.

## 10. Candidate next steps
1. Repair the module-loading contract: add `type="module"` to the script tag in `src/index.html:3` (and optionally `"type": "module"` in `package.json:1`), then verify the dashboard renders against a stubbed `/api/data` response.
2. Write a README documenting the single flow (load → render → navigate) and the `/api/data` contract (addresses Tier 1.1 and the implicit dependency).
3. Add a smoke-test script to `package.json:1` (addresses Zero Validation; would have caught the contract break).
4. Wire `widget.js` into `dashboard.js` or delete it (removes the orphaned component).
5. Run the `ui-diagnostic-workflow` in `plan_only` mode to produce a ui-brief before any redesign (the registry-grounded downstream for ui_fog).

## 11. Recommended next step
Repair the module-loading contract first (`src/index.html:3` → `type="module"`, mirrored in `package.json:1`). It is the smallest change with the highest leverage: it is the only step that makes the app executable, it unblocks every other diagnostic and test, and it is directly evidenced by the three-file mismatch (`src/index.html:3`, `src/app.js:1-2`, `package.json:1`).

## 12. Recommended workflow
`ui-diagnostic-workflow` from `skills/workflow-planner/references/workflow-registry.yaml` (registry line 715): "Analyze UI complexity, screen structure, and design patterns. Produces a high-fidelity UI assessment without implementation." It matches the `ui_fog` classification and stays diagnostic (`plan_only` execution mode, which the workflow allows), consistent with this skill's no-implementation boundary.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/web-frontend
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: ui_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: ui-diagnostic-workflow
recommended_execution_mode: plan_only
evidence:
  - "src/index.html (line 3): app.js included as a classic script without module type"
  - "src/app.js (lines 1-3): ES module imports and single /dashboard route registration"
  - "package.json (line 1): no module type, no dependencies, no test script"
  - "src/api.js (line 2): implicit dependency on undocumented /api/data endpoint"
  - "src/components/dashboard.js (line 3): raw JSON dump without loading or error states"
  - "src/components/widget.js (line 1): orphaned widget component never imported"
  - "src/router.js (line 5): hash routing with no fallback for unknown routes"
weakest_boundary:
  type: Contract Mismatch
  evidence: "src/index.html:3 loads app.js as a classic script while src/app.js:1-2 uses ES module imports and package.json:1 declares no module type"
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

"Route this repository sensemaking brief (artifact_id: repository_sensemaking_brief; primary_fog_type: ui_fog; weakest_boundary: Contract Mismatch; source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md) to the `ui-diagnostic-workflow` in `plan_only` mode. Context: corpus/web-frontend is a 7-file vanilla-JS dashboard whose module-loading contract is broken (index.html loads app.js as a classic script while app.js uses ES module imports, and package.json declares no module type), has no README, tests, or design system, and depends on an undocumented /api/data endpoint. Produce the orchestration plan without implementing anything."
