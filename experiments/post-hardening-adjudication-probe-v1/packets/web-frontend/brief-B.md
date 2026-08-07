# Repository Sensemaking Brief — web-frontend (dashboard-ui)

## 1. Repository goal
The repository is a minimal browser-based frontend named `dashboard-ui` (`package.json:1`) whose apparent goal is to serve a static web page that displays a dashboard: load data from an API and inject it into the page (`src/index.html:2` titles the page "Dashboard"; `src/components/dashboard.js:3` renders fetched data into `#app`). It is a single-screen, hash-routed, no-build frontend. There is no README, so the goal is reconstructed from code (OBSERVED) rather than stated (no documented intent artifact exists — this is a no-user-intent fixture run).

## 2. Current shape
The repository contains exactly 7 files: `package.json` (1 line), `src/index.html` (3 lines), `src/app.js` (4 lines), `src/api.js` (3 lines), `src/components/dashboard.js` (3 lines), `src/components/widget.js` (1 line), and `src/router.js` (6 lines). There is no README, no docs directory, no tests, no CI, no build config, and no stylesheet.

**Runtime flow (reconstructed, not directory summary):**

- **Startup path**: `package.json:1` declares the only script, `"start": "python -m http.server 8000"` — a static file server (no build step, no bundler). The browser entry is `src/index.html:3`, which includes `<script src="app.js"></script>`.
- **Orchestration**: `src/app.js:1-4` is the bootstrap module: it imports `renderDashboard` from `./components/dashboard.js` and `router` from `./router.js`, registers the `/dashboard` route (`src/app.js:3`), and starts the router (`src/app.js:4`).
- **Routing**: `src/router.js:1-6` is a central hash router (a single `routes` map; `register` at line 3, `start` at line 4, `dispatch` at line 5). Routing is explicit and centralized in one file.
- **Domain/core logic**: `src/components/dashboard.js:2-3` (`renderDashboard`) calls `loadData()` and injects the JSON into `#app` via `innerHTML`; `src/api.js:1-3` performs `fetch('/api/data')`.
- **Persistence/state**: no database, cache, or storage. State lives only in the module-level `routes` object (`src/router.js:1`) and the DOM (`#app`).
- **External integration point**: `src/api.js:2` fetches `/api/data` — an external endpoint that **nothing in this repository provides or declares** (the only server is `python -m http.server`, which serves static files only, `package.json:1`).
- **Background work**: none (no workers, jobs, or scheduled tasks).
- **Output boundary**: DOM injection at `src/components/dashboard.js:3`.

**Broken/UNKNOWN hops (must be recorded, not invented):**
- HTML → JS module transition: `src/index.html:3` loads `app.js` as a **classic script** (no `type="module"`), while `src/app.js:1-2` uses ES module `import` syntax. A classic script containing `import`/`export` throws a SyntaxError at parse time, so `app.js` never executes — `router.start()` (`src/app.js:4`) never registers the `hashchange` listener (`src/router.js:4`), and no screen can render. UNKNOWN-resolved: this hop fails deterministically (browser spec semantics, OBSERVED in both files).
- Data hop: even if the app booted, `fetch('/api/data')` (`src/api.js:2`) has no server-side counterpart in this repo; `python -m http.server` returns 404 for it. UNKNOWN whether an out-of-repo backend is intended — nothing declares one.

**Dependency semantics (declared vs. used vs. dead):**
- `python -m http.server` — `declared` (`package.json:1`, scripts) and `runtime` (it is the only launch path), but it is a *static file server*, not an application dependency.
- No `dependencies`/`devDependencies` are declared at all (`package.json:1`).
- `src/components/widget.js:1` — `declared` in the sense of existing as an exported module, but **never imported by any file** (verified against `src/app.js`, `src/components/dashboard.js`, `src/api.js`, `src/router.js`) → `dead`/unwired module (OBSERVED).

**Validation structure (Pass D):** none. No tests, no lint, no type checks, no CI, no build — `loadData()` has no `.catch` (`src/api.js:2`), so a failed fetch produces an unhandled rejection and a blank page.

## 3. Strong signals
- **Centralized routing**: routing lives in one small file (`src/router.js:1-6`) with explicit registration from the bootstrap (`src/app.js:3`) — the Tier 1.3 UI-fog signal (complex/undocumented routing) is *not* present.
- **A component directory exists**: `src/components/` holds `dashboard.js` and `widget.js`; `widget.js:1` is a small reusable helper, showing an attempt at a component abstraction layer (even though it is unwired — see Section 4).
- **Zero-friction minimalism**: 7 small files, no vendored dependencies, no build toolchain, one-command start (`package.json:1`). The whole system is human-readable in minutes.
- **Deterministic failure points**: the two defects (module loading, missing API) are precisely locatable — the system is small enough that the fix surface is tiny.

## 4. Missing pieces
- **Module-loading contract**: `src/index.html:3` loads `app.js` without `type="module"` even though `src/app.js:1-2` is an ES module — the app cannot boot (see Section 6).
- **Any `/api/data` provider or declaration**: `src/api.js:2` fetches a path nothing serves; no mock, no base-URL config, no documentation of the expected contract.
- **Error handling**: `src/api.js:2` has no `.catch`; a 404/network failure leaves `#app` blank with an unhandled rejection.
- **`widget.js` wiring**: `src/components/widget.js:1` is exported but imported nowhere — either dead code or a missing composition step.
- **Documentation**: no README, no flow/screen documentation, no API contract notes — the product surface is entirely undocumented (Tier 1.1 UI-fog signal).
- **Design system**: no CSS/stylesheet file exists anywhere; `src/index.html:1-3` is bare markup and `src/components/dashboard.js:3` emits a raw `<pre>` — no tokens, no theme (Tier 1.4 UI-fog signal).
- **Validation**: no tests, no build, no CI — nothing would catch the boot failure (Zero Validation).
- **Accessibility/responsiveness**: no ARIA, no alt text, no media queries (Tier 2.1/2.2/2.3 signals).

## 5. Improvement opportunities
- Add a README stating the goal, the run command, and the expected `/api/data` contract (turns an implicit dependency into a documented one).
- Add `.catch` to `loadData()` and render an error state (`src/api.js:2`) — cheap resilience.
- Add a boot smoke test (e.g., a headless-browser check that the page loads without console errors) — directly prevents recurrence of the Section 6 defect.
- Wire `widget.js` into the dashboard or delete it (`src/components/widget.js:1`).
- Declare the API contract (mock server, or a documented dev proxy) so `fetch('/api/data')` has a reachable counterpart during development.

## 6. Weakest boundary

**Candidate generation (scored):**

| # | Boundary (file:line) | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|---|
| C1 | HTML→JS module-loading contract: `src/index.html:3` (classic script) vs `src/app.js:1-2` (ES module) | strong (both files OBSERVED; deterministic browser semantics) | high (app never boots) | high (100% of the app) | high (the entire product surface) | high (blocks all UI/data/docs work) | low |
| C2 | External API contract: `src/api.js:2` `fetch('/api/data')` vs `package.json:1` static-only server; nothing provides the endpoint | strong (OBSERVED fetch path; OBSERVED server) | high (data never loads even if boot fixed) | high (dashboard is the only screen) | high | high | medium (an out-of-repo backend may be intended, but nothing declares it) |
| C3 | Validation boundary: no tests/build/CI anywhere; `package.json:1` declares only a static server script | strong (OBSERVED absence across the whole repo) | medium | medium (process-level) | medium | medium | low |
| C4 | UI surface documentation/design system: no README, no flow docs, no CSS (Tier 1.1/1.4 signals) | medium (absence-based) | medium | medium | medium | medium | low |

**Selection rule applied:** C1 has the strongest combination of high consequence (nothing boots), strong direct evidence (two tiny fully-read files, deterministic failure), and maximal downstream blocking (no screen can render, so C2/C4 work cannot even be observed). C2 is real but is *downstream* of C1. C3 is the enabling condition, not the boundary itself. C4 is the least consequential. **C1 is selected.**

```text
Boundary: the HTML→JS module-loading boundary at the runtime entry point — src/index.html:3
declares app.js under the classic-script loading contract, while src/app.js:1-2 is an ES module.
Observed contract: src/index.html:3 loads the application with
  <script src="app.js"></script> (no type="module"), i.e., a classic script, which the browser
  parses as a non-module script.
Observed violation or uncertainty: src/app.js:1-2 begins with `import` declarations (ES module
  syntax). A classic script containing static import/export throws a SyntaxError ("Cannot use
  import statement outside a module") and is never executed, so router.start() at src/app.js:4
  never registers the hashchange listener (src/router.js:4) and no screen can ever render.
Evidence: src/index.html:3; src/app.js:1-2, 4; src/router.js:4.
Weakness type: **Contract Mismatch**
Logic trace: src/index.html:3 declares the loading contract for app.js as a classic script
  (no type="module"); the actual file content of src/app.js:1-2 is ES-module syntax
  (import/export), which classic scripts cannot contain. Under browser script semantics a
  classic script with static imports fails at parse time, so the file "claim" made by the
  entry point (loadable as a classic script) and the file's actual format (an ES module)
  disagree — a file-format/loading-contract disagreement that is exactly the Contract Mismatch
  shape. Because app.js never executes, the router never starts (src/app.js:4 → src/router.js:4)
  and no screen renders; therefore the weakest boundary is the entry-point loading contract,
  not any screen/flow/design concern.
Failure consequence: the product is dead on arrival — every user request returns an empty page;
  all downstream work (API wiring, UI polish, documentation) is unobservable until the contract
  is fixed; and with no tests (C3) nothing would catch a regression of the same shape.
Confidence: high — both files were fully read (src/index.html:1-3, src/app.js:1-4) and the
  failure follows deterministically from browser module semantics; no inference is required.
  Confidence would be raised further by an actual browser boot attempt, which is a trivial
  manual check.
Alternatives considered: C2 (API contract, src/api.js:2) — real and severe, but it only
  matters *after* the app can boot; it is downstream of C1. C3 (Zero Validation) — the
  enabling condition that let C1 ship, not the boundary itself; no automated check exists
  (no test files, no test script in package.json:1). C4 (UI documentation/design system) —
  genuine Tier 1.1/1.4 UI-fog signals, but least consequential and not one of the seven
  weakness types (absent docs are not Vocabulary Drift, which requires docs that misdescribe
  existing code). Ghost Features was rejected: nothing is documented anywhere, so there is no
  documented surface whose implementation could be missing.
```

## 6.5. Problem classification (fog type)
Frontend code exists (HTML + JS), so the UI-fog decision tree applies. Tier 1 signals from the UI Fog Signals Registry:
- **1.1 Missing UI flow documentation — PRESENT** (no README, no flow/screen docs anywhere in the repo).
- **1.4 Design system fragmentation/absence — PRESENT** (no CSS file, no tokens/theme; bare `<pre>` rendering at `src/components/dashboard.js:3`).
- 1.2 Component boundaries — partial (a `src/components/` directory exists, but `widget.js` is unwired; not a clean signal either way).
- 1.3 Routing complexity — NOT present (routing is centralized in `src/router.js:1-6`).

By the registry decision tree alone, 2 Tier 1 signals would classify as `ui_fog` with strong confidence. **However, the frontend tie-break applies**: the weakest boundary (Section 6) is a boot-time entry-point contract failure — `src/index.html:3` loads an ES module as a classic script — which prevents *any* screen from rendering. That defect is provably outside the UI layer (it is a module-loading/structural failure that occurs before the first screen can render), so per the SKILL's frontend tie-break rule the primary fog type is **`architecture_fog`**, with `ui_fog` recorded as the secondary fog (Tier 1.1 + 1.4, plus Tier 2.1/2.2/2.3 absences: no UI tests, no accessibility handling, no responsive design). No user intent artifact exists (fixture run), so no intent-based tie-break is available.

## 7. Evidence
All evidence is OBSERVED from the seven files that constitute the entire repository (recursive listing shows no other files, hidden or otherwise).

The boot-blocking contract failure is visible at `src/index.html:3` (classic `<script src="app.js"></script>`) versus `src/app.js:1-2` (ES module `import` statements), with the never-reached router start at `src/app.js:4` and its listener registration at `src/router.js:4`. The manifest `package.json:1` declares only a static file server (`python -m http.server 8000`) and no dependencies, test script, or build step. The data path `src/api.js:2` (`fetch('/api/data')`) depends on an endpoint nothing in this repository serves or declares. `src/components/widget.js:1` exports a helper that no other file imports. Absence evidence (equally OBSERVED): there is no README, no tests directory, no CI configuration, and no CSS file anywhere in the repository — confirmed by a full recursive listing of the target directory.

**Logic trace:** The cited pair `src/index.html:3` + `src/app.js:1-2` establishes the contract mismatch: the entry point promises the browser can execute `app.js` as a classic script, but the file's actual content is ES-module syntax, which classic scripts reject at parse time. Since `src/app.js:4` (the only place `router.start()` is called) therefore never runs, the `hashchange` listener at `src/router.js:4` is never registered and the route dispatch at `src/router.js:5` never fires — the sole screen `#app` (rendered only by `src/components/dashboard.js:3`) stays empty. This chain is fully OBSERVED in tiny, completely-read files, so the weakest boundary (Section 6) is the entry-point loading contract, classified as Contract Mismatch, and because no screen can render the defect is structural — primary fog `architecture_fog`. The secondary UI-fog signals (missing flow docs, absent design system) and the API gap (`src/api.js:2`) are real but subordinate: they describe layers the app never reaches and hops the boot failure blocks.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: src/index.html
    lines: L3
    quote: "<body><div id=\"app\"></div><script src=\"app.js\"></script></body></html>"
    supports_claim: "The entry page loads app.js as a classic script (no type=\"module\") — the loading contract that mismatches app.js's ES-module format."
  - file: src/app.js
    lines: L1-L2
    quote: "import { renderDashboard } from './components/dashboard.js';\nimport { router } from './router.js';"
    supports_claim: "app.js is an ES module; static import statements are invalid in a classic script, so the app never boots."
  - file: src/app.js
    lines: L4
    quote: "router.start();"
    supports_claim: "Router startup is the only orchestration trigger and is unreachable while app.js fails to parse."
  - file: src/router.js
    lines: L4
    quote: "start() { window.addEventListener('hashchange', () => this.dispatch()); this.dispatch(); },"
    supports_claim: "The hashchange listener that drives navigation is registered only from router.start(), which never runs."
  - file: package.json
    lines: L1
    quote: "{\"name\": \"dashboard-ui\", \"scripts\": {\"start\": \"python -m http.server 8000\"}}"
    supports_claim: "The only declared script is a static file server; no dependencies, no test/build scripts — Zero Validation."
  - file: src/api.js
    lines: L1-L3
    quote: "export async function loadData() {\n  return fetch('/api/data').then(r => r.json());\n}"
    supports_claim: "The data path depends on an external /api/data endpoint that nothing in this repo provides or declares; no error handling."
  - file: src/components/widget.js
    lines: L1
    quote: 'export function widget(title, body) { return `<div class="widget"><h2>${title}</h2>${body}</div>`; }'
    supports_claim: "widget() is exported but never imported by any other file — an unwired module."
  - file: src/components/dashboard.js
    lines: L1-L3
    quote: "import { loadData } from '../api.js';\nexport function renderDashboard() {\n  loadData().then(data => { document.getElementById('app').innerHTML = '<pre>' + JSON.stringify(data) + '</pre>'; });\n}"
    supports_claim: "The only screen renders via innerHTML with no error branch — the output boundary reached only if boot succeeds."
```

## 9. Why this boundary matters
While `src/index.html:3` and `src/app.js:1-2` disagree about how `app.js` is loaded, the product is dead on arrival: no user ever sees a screen, no flow can be tested, and the `/api/data` gap (`src/api.js:2`) cannot even be observed in a browser. Every candidate improvement — UI work, data wiring, documentation — is blocked behind this one contract. Because there is zero automated validation (no tests, no build; `package.json:1` declares only a static server), the same class of defect (e.g., a future `type="module"` regression or a second entry point with the same shape) can silently ship again. It is a one-token fix (`type="module"`) with an outsized blast radius.

## 10. Candidate next steps
1. **Fix the loading contract**: add `type="module"` to the script tag at `src/index.html:3` (unblocks boot; smallest possible change).
2. **Add a boot smoke test**: a headless-browser check that the page loads with no console errors and `#app` is populated — converts Zero Validation into a guardrail for this exact boundary.
3. **Resolve the API contract**: provide or mock `/api/data`, add a `.catch` to `src/api.js:2`, and document the expected response shape.
4. **Wire or remove `widget.js`**: import it in `src/components/dashboard.js` or delete `src/components/widget.js:1`.
5. **Add documentation**: a README covering the goal, run command, and the `/api/data` contract (addresses Tier 1.1 and the implicit dependency).

## 11. Recommended next step
Add `type="module"` to the script tag at `src/index.html:3` so `src/app.js:1-4` can execute and the router can start — the smallest concrete action with the highest leverage, since it converts the repository from "cannot boot" to "boots, then hits the documented `/api/data` gap". Pair it immediately with a boot smoke test so the contract is enforced, not just fixed once.

## 12. Recommended workflow
`architecture-implementation-workflow` (from the canonical `skills/workflow-planner/references/workflow-registry.yaml`), in **`guided_execution`** mode (one of its `allowed_execution_modes`; note this workflow does not offer `plan_only`).

Rationale: the primary fog type is `architecture_fog` (entry-point contract failure before any screen can render), and `architecture-implementation-workflow` is the registry's workflow for architecture/refactoring problems — it aligns domain understanding, produces a refactoring spec for the module-boundary/entry-point contract, decomposes into issues, and implements via TDD. Closest alternatives considered and rejected: `ui-implementation-workflow` (addresses screens/flows, but the app cannot reach a screen until the boot contract is fixed — wrong order of operations), `ui-diagnostic-workflow` (UI assessment only, wrong layer for a boot-time structural defect), `fast-local-diagnostic` (diagnostic-only; the brief already exists and implementation is the needed next step), and `product-implementation-workflow`/`docs-implementation-workflow` (no product-contract or documentation-contract evidence as the primary defect). No preconditions are missing: the boundary, evidence, and fix surface are all identified; `guided_execution` keeps each step gated by human review, appropriate for the D5-adjacent structural fix.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/web-frontend
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "src/index.html (line 3): loads app.js as a classic script (no type=\"module\") while app.js uses ES module import syntax — the app cannot boot"
  - "src/app.js (lines 1-4): ES module bootstrap whose router.start() never executes under classic-script loading"
  - "src/router.js (lines 1-6): centralized routing; the hashchange listener at line 4 is registered only from router.start()"
  - "package.json (line 1): only a static file server script; no dependencies, tests, or build"
  - "src/api.js (lines 1-3): fetch('/api/data') depends on an endpoint nothing in the repo provides; no error handling"
  - "src/components/widget.js (line 1): exported widget() never imported by any other file (unwired module)"
  - "Repository-wide absence: no README, no tests, no CI, no CSS (Tier 1.1/1.4 UI-fog signals and Zero Validation)"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Contract Mismatch
weakness_type: Contract Mismatch
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-06-18T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
"Run the `architecture-implementation-workflow` in `guided_execution` mode against the repository at `experiments/repository-sensemaking-skill-hardening-v1/corpus/web-frontend`. The repository sensemaking brief classifies the primary fog as `architecture_fog` with `ui_fog` secondary, and identifies the weakest boundary as a **Contract Mismatch** at the entry point: `src/index.html:3` loads `src/app.js` as a classic script (no `type=\"module\"`), but `src/app.js:1-2` is an ES module, so the app fails at parse time before any screen can render. Spec and implement the module-loading contract fix (add `type=\"module\"`), add a boot smoke test so the entry-point contract is validated, and — as follow-on scope — resolve the implicit `/api/data` dependency at `src/api.js:2` (provide, mock, or declare it) and wire or remove the unused `src/components/widget.js:1` helper. All steps gated by human review."
