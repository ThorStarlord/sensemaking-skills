# Repository Sensemaking Brief

## 1. Repository goal
This repository (package name `foggy-ui`, `package.json:1`) appears to be a small hash-routed browser UI skeleton: an entry module (`src/index.js:1-2`) mounts an app view (`src/views/AppView.js:1-2`) that starts a hash router (`src/router.js:4-16`), with a layered structure of views, ui components, widgets, and stylesheets. What the product is *for* cannot be fully established from the repository itself: there is no README, no documentation directory, and the manifest declares only a name (`package.json:1`). INFERRED from the directory naming (`src/views`, `src/ui`, `src/widgets`): the intent is a multi-screen frontend with reusable components — but no screen is reachable at runtime (see Section 6).

## 2. Current shape
**Runtime flow (reconstructed from the 12 files actually opened):**

- **Startup path**: `src/index.js:1-2` imports `{ mount }` from `./views/AppView.js` and calls `mount()`. How this module is launched in a browser is **UNDECLARED**: `package.json:1` has no `scripts`, no `dependencies`, no `main` field, and there is no `index.html`, no bundler config, no dev-server config anywhere in the repository (OBSERVED, full inventory: only `package.json` + 11 files under `src/`).
- **Orchestration**: `src/views/AppView.js:1-2` — `mount()` calls `router.start()`; nothing else happens at startup.
- **Core flow**: `src/router.js:1-16`. Module-global state `routes` and `current` (`src/router.js:1-2`); `add(path, handler, guard)` registers a route (`src/router.js:5`); `start()` triggers `dispatch()` (`src/router.js:6`); `dispatch()` reads `window.location.hash` (`src/router.js:8`), looks up the route (`src/router.js:9`), silently returns if missing (`src/router.js:10`), applies the optional guard (`src/router.js:11`), then calls the handler (`src/router.js:12-13`).
- **Domain/core logic**: none. No handler is ever registered (see below).
- **Persistence/state**: only the module globals `routes` and `current` (`src/router.js:1-2`); external state is `window.location.hash` (read at `src/router.js:8`). No database, cache, queue, or remote system exists.
- **External integration points**: the browser `window.location.hash` is the only external input (`src/router.js:8`); there are no other integrations.
- **Output boundary**: the router's `r.handler()` call (`src/router.js:13`) is the only output path, and it is never reached — the registered-route table is empty.

**Entry-point reachability (Pass B/C, verified by grep over the whole repository — zero matches for `router.add`, zero matches for imports of `../ui`, `../widgets`, `./ui`, `./widgets`):**

- `src/views/ProfileView.js:1` and `src/views/SettingsView.js:1` export functions returning raw HTML strings; neither is imported anywhere (declared, **dead**).
- `src/ui/form.js:1`, `src/ui/table.js:1`, `src/widgets/button.js:1`, `src/widgets/modal.js:1` export helpers; none is imported anywhere (declared, **dead**).
- `src/styles/colors.css:1` defines a design token `--brand`; `src/styles/other.css:1` defines `.btn` with a hardcoded color. Neither stylesheet is referenced by any HTML or JS (no `index.html`, no CSS imports in JS — OBSERVED from full-file reads); `.btn` matches no element because `src/widgets/button.js:1` emits `<button>` with no class.

**Dependency semantics**: `package.json:1` declares zero dependencies (OBSERVED). Of the authored modules, only `src/index.js` → `src/views/AppView.js` → `src/router.js` are `used` (imported); the six view/component modules are `dead` (declared, never imported); both CSS files are `dead` (never referenced).

**Where responsibility becomes unclear**: the seam between the router contract ("call `add()` before `start()`", `src/router.js:5-6`) and the screen layer. No module owns route registration; `dispatch()` swallows a missing route with `if (!r) return;` (`src/router.js:10`), so a broken wiring produces a blank page with no error — UNKNOWN to the runtime, and unobservable to a developer without manual tracing.

## 3. Strong signals
- **Clean entry split**: `src/index.js:1-2` → `src/views/AppView.js:1-2` → router is a short, readable startup chain.
- **Centralized routing**: all routing lives in one small module (`src/router.js:1-16`) with an explicit `add(path, handler, guard)` contract (`src/router.js:5`) and guard support (`src/router.js:11`) — not scattered route definitions.
- **Purposeful layout conventions**: `src/views/`, `src/ui/`, `src/widgets/`, `src/styles/` separate concerns by directory (OBSERVED directory tree).
- **A design token exists**: `src/styles/colors.css:1` defines `--brand`, indicating an intended token-based styling approach.
- **Pure, simple component helpers**: `src/ui/form.js:1`, `src/ui/table.js:1`, `src/widgets/button.js:1`, `src/widgets/modal.js:1` are side-effect-free functions — trivially wireable once flows exist.

## 4. Missing pieces
- **Route registration**: nothing in the repository calls `router.add` (grep: no matches), so the router's registered-route table is empty and no screen can render.
- **Any documentation**: no README, no `docs/`, no flow or screen specs, no design notes (OBSERVED, full inventory).
- **Declared run/build tooling**: `package.json:1` has no `scripts`, `dependencies`, or `main`; no bundler/dev-server config; no `index.html` — the app has no declared way to build or run.
- **Tests of any kind**: no test files, no test runner config (OBSERVED, full inventory; Pass D found no validation anywhere).
- **Component composition**: views return raw HTML strings (`src/views/ProfileView.js:1`, `src/views/SettingsView.js:1`) and never use the `ui/`/`widgets/` helpers.
- **Router error boundary**: `dispatch()` silently returns on an unknown hash (`src/router.js:10`); no 404/default route, no error surface.
- **Style/component contract**: `.btn` (`src/styles/other.css:1`) is never emitted by `button.js:1`; colors are split between a token (`src/styles/colors.css:1`) and a hardcoded hex (`src/styles/other.css:1`).

## 5. Improvement opportunities
- Register routes from a single module (e.g. a `src/routes.js`) before `router.start()` and add a fallback/404 route that surfaces instead of the silent `return` at `src/router.js:10`.
- Add `package.json` scripts plus a minimal bundler/dev-server and an `index.html` so the app has a declared launch path.
- Make `ProfileView`/`SettingsView` compose the `ui/` and `widgets/` helpers instead of emitting raw strings.
- Consolidate styling on `--brand` (`src/styles/colors.css:1`) and either emit `class="btn"` from `src/widgets/button.js:1` or delete the orphaned rule at `src/styles/other.css:1`.
- Add a routing smoke test (the router is pure enough to test without a browser if `window.location` is injected).

## 6. Weakest boundary
**Candidate generation and scoring:**

| # | Boundary (where) | evidence | severity | blast radius | goal relevance | downstream blocking | uncertainty |
|---|---|---|---|---|---|---|---|
| A | Route-registration seam: entry (`src/index.js:1-2`) → screens via `router.add`/`dispatch` (`src/router.js:5-14`) | strong | high | high | high | high | low |
| B | Style/component contract: `.btn` (`src/styles/other.css:1`) vs `button.js:1`; token vs hardcoded hex | strong | medium | medium | medium | low | low |
| C | Runnability: no scripts/main/bundler/`index.html` (`package.json:1`) | strong | medium | high | medium | medium | low |
| D | Validation: no tests/schemas for any behavior (full inventory) | strong | medium | high | medium | medium | low |
| E | Component layer unwired: `src/ui/*`, `src/widgets/*` never imported | strong | high | high | high | high | low |

Selection rule: prefer highest combination of consequence, evidence strength, centrality, and downstream blocking. **A** and **E** describe the same defect from two angles (screens unreachable because the component/view layer is unwired and nothing registers routes); **A** is the seam where responsibility actually transfers (entry → screen), so it is selected, with **E** subsumed.

```text
Boundary:
  The route-registration seam between app startup and the screen layer: the contract
  `router.add(path, handler, guard)` (src/router.js:5) must be called before
  `router.start()` (src/router.js:6) for any screen to render, but no module in the
  repository ever calls it.
Observed contract:
  src/router.js:5 defines add(path, handler, guard); src/router.js:6 start() calls
  dispatch(); src/router.js:7-14 dispatch() resolves window.location.hash against the
  registered routes table and invokes the matching handler.
Observed violation or uncertainty:
  Zero calls to router.add exist anywhere in the repository (grep over all files: no
  matches), and src/router.js:10 silently returns when no route matches. The screens
  (src/views/ProfileView.js:1, src/views/SettingsView.js:1) and components
  (src/ui/form.js:1, src/ui/table.js:1, src/widgets/button.js:1, src/widgets/modal.js:1)
  are never imported by any module. The app mounts (src/index.js:1-2) and renders
  nothing.
Evidence:
  src/index.js:1-2; src/views/AppView.js:1-2; src/router.js:5, 7-14; src/router.js:10;
  src/views/ProfileView.js:1; src/views/SettingsView.js:1; src/ui/form.js:1;
  src/ui/table.js:1; src/widgets/button.js:1; src/widgets/modal.js:1; grep result:
  no `router.add` calls and no imports of the view/component modules anywhere.
Weakness type:
  Ghost Features
Logic trace:
  src/index.js:1-2 is the only entry point; it calls mount() from
  src/views/AppView.js; AppView.js:1-2 only starts the router; router dispatch
  (src/router.js:7-14) renders only registered routes and returns silently on a miss
  (src/router.js:10); grep proves no file ever calls router.add and no file imports the
  view/component modules; therefore the registered-route table is empty, every screen
  exists only as a declared export with no reachable implementation path, and the UI
  surface is a set of ghost features — declared code masquerading as the app's core
  that can never appear in the running application. The router seam is the single
  boundary where this failure could be caught or enforced, and nothing validates it
  (no tests exist; the guard parameter at src/router.js:5,11 is never exercised).
  This maps to the canonical Ghost Features type per the skill's GAP-6 guidance:
  unreachable code shaped like core product surface (screens/components), not
  example/documentation-shaped code (which would be Orphaned Examples). Because Ghost
  Features is a D5 high-risk claim category, this diagnosis requires a substantive
  human audit before final approval — that audit requirement is expected, not an error.
Failure consequence:
  The UI renders a blank page at runtime; all six view/component modules are dead
  code; any downstream UI work (flow mapping, screen specs, design-system work) is
  ungrounded until the wiring exists, and because dispatch fails silently
  (src/router.js:10), the breakage is invisible to anyone not tracing the code.
Confidence:
  high — every one of the repository's 12 files was opened and read in full; grep
  over the entire repository confirms zero router.add calls and zero imports of the
  view/component modules. What would raise it further: a live browser run to observe
  the blank render (currently UNKNOWN how the app is even launched — no scripts,
  no index.html, package.json:1).
Alternatives considered:
  - (E) Unwired component/view layer: same root cause as the selected boundary
    (nothing reaches the screens); subsumed rather than separate.
  - (D) Zero Validation (no tests, no guard usage): real and observed, but it
    describes missing enforcement of the contract, not the hollow screen surface;
    the higher-consequence defect is that the screens are unreachable at all.
  - (B) Style/component contract mismatch (.btn orphaned, token vs hardcoded hex):
    real (src/styles/other.css:1 vs src/widgets/button.js:1) but narrower blast
    radius — styling, not the entire UI surface.
  - (C) Runnability gap (package.json:1): real but a tooling absence, not a
    responsibility boundary; it is a consequence of fixture minimalism rather than a
    seam where behavior silently breaks.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)
**primary_fog_type: ui_fog** (STRONG confidence, per the UI Fog Signals Registry decision tree).

Frontend code is present (JS modules emitting HTML strings; two CSS files), so the ui_fog gate is passed. Tier 1 signals, 4 of 4 present:

- **1.1 Missing UI flow documentation**: no README, no `docs/`, no flow/screen specs, no Storybook/Figma references anywhere (OBSERVED, full inventory) — signal present.
- **1.2 Complex frontend without functional component boundaries**: directories `src/views`, `src/ui`, `src/widgets` exist, but no view composes any component; every screen reimplements raw HTML (`src/views/ProfileView.js:1`, `src/views/SettingsView.js:1`) and the component layer is never imported (grep: no matches) — the abstraction layer is nominal, signal present.
- **1.3 Routing complexity without navigation architecture**: routing exists in one file (`src/router.js:1-16`) but is completely undocumented, no route is ever registered, and navigation between screens cannot be traced anywhere (grep: no `router.add` calls) — signal present.
- **1.4 Design system fragmentation**: one token (`src/styles/colors.css:1`) coexists with a hardcoded hex color (`src/styles/other.css:1`) and an orphaned `.btn` rule that no component emits (`src/widgets/button.js:1`) — signal present.

2+ Tier 1 signals → STRONG CONFIDENCE `ui_fog`. Tier 2 corroboration is also fully present: no UI tests at all (2.1), no accessibility attributes or documentation (2.2), no responsive/breakpoint handling (2.3), and screens exist with zero documentation mapping them (2.4).

Secondary fog: **architecture_fog** also applies (module-global router state `src/router.js:1-2`, unwired modules, an unenforced boundary) — noted here so it is not lost, but per the decision tree the primary fog type driving routing is `ui_fog` (the screen/flow/component surface is the blocking problem). No user-intent artifact exists for this run, so `user_implied_fog_type: unknown` and `diagnosis_conflict: false` (GAP-8).

## 7. Evidence
The diagnosis is grounded in the following opened files:

- `src/index.js:1-2` — the only entry point: imports `mount` from `./views/AppView.js` and calls `mount()`; nothing else runs.
- `src/views/AppView.js:1-2` — `mount()` only calls `router.start()`; no routes are registered at startup.
- `src/router.js:5` — `add(path, handler, guard)` is the only route-registration contract; `src/router.js:7-14` shows `dispatch()` resolving the hash and `src/router.js:10` returning silently on a miss.
- `src/views/ProfileView.js:1`, `src/views/SettingsView.js:1`, `src/ui/form.js:1`, `src/ui/table.js:1`, `src/widgets/button.js:1`, `src/widgets/modal.js:1` — declared screen/component exports with no importers (grep over the entire repository: no matches for `router.add` and no imports of `ui/` or `widgets/` modules).
- `package.json:1` — `{"name": "foggy-ui"}`: no scripts, dependencies, or main field; no declared run path.
- `src/styles/colors.css:1` vs `src/styles/other.css:1` — token `--brand` vs hardcoded `#333366`; `.btn` matches no emitted markup (`src/widgets/button.js:1` emits a class-less `<button>`).

**Logic trace:** The entry chain `src/index.js:1-2` → `src/views/AppView.js:1-2` → `router.start()` (`src/router.js:6`) → `dispatch()` (`src/router.js:7-14`) renders only handlers registered via `router.add` (`src/router.js:5`); grep proves no `router.add` call exists and no view/component module is imported anywhere; therefore the route table is empty, `dispatch()` hits the silent `if (!r) return;` at `src/router.js:10` on every navigation, and the entire UI surface (3 views, 2 ui components, 2 widgets) is unreachable at runtime — declared screens with no reachable implementation, i.e. Ghost Features. The same evidence chain classifies the fog as `ui_fog`: the missing flow documentation (Tier 1.1), the nominal component boundaries (Tier 1.2), the undocumented and unregistered routing (Tier 1.3), and the fragmented styling (Tier 1.4) are all directly cited above. The classification is OBSERVED/DERIVED only — every citation is a file that was opened and read in full, and the two negative findings (no `router.add` calls, no component imports) come from a complete-repository grep, so no UNKNOWN was converted into a conclusion.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: package.json
    lines: L1
    quote: '{"name": "foggy-ui"}'
    supports_claim: "Manifest declares only a package name - no scripts, no dependencies, no main - so no declared build/run/test path exists (OBSERVED)."
  - file: src/index.js
    lines: L1-L2
    quote: "import { mount } from './views/AppView.js';\nmount();"
    supports_claim: "The only entry point: imports mount from AppView and calls it; nothing else runs at startup (OBSERVED)."
  - file: src/views/AppView.js
    lines: L1-L2
    quote: "import { router } from '../router.js';\nexport function mount() { router.start(); }"
    supports_claim: "mount() only starts the router - no routes are registered anywhere at startup (OBSERVED)."
  - file: src/router.js
    lines: L5
    quote: "add(path, handler, guard) { routes[path] = { handler, guard }; },"
    supports_claim: "router.add is the only route-registration contract, and grep finds zero callers anywhere in the repository (OBSERVED + DERIVED)."
  - file: src/router.js
    lines: L7-L14
    quote: "dispatch() {\nconst path = window.location.hash.slice(1);\nconst r = routes[path];\nif (!r) return;\nif (r.guard && !r.guard()) { current = 'blocked'; return; }\ncurrent = path;\nr.handler();\n},"
    supports_claim: "dispatch() renders only registered routes and silently returns on a miss (L10) - with an empty route table every navigation no-ops (OBSERVED)."
  - file: src/views/ProfileView.js
    lines: L1
    quote: "export function profile() { return '<div>profile</div>'; }"
    supports_claim: "A screen exists as an exported function but is never imported by any module - unreachable ghost surface (OBSERVED + grep)."
  - file: src/widgets/button.js
    lines: L1
    quote: "export const button = (label) => `<button>${label}</button>`;"
    supports_claim: "Component never imported, and emits a class-less <button>, so the .btn rule in src/styles/other.css:1 is orphaned (OBSERVED + grep)."
  - file: src/styles/colors.css
    lines: L1
    quote: ":root { --brand: #3366ff; }"
    supports_claim: "A design token exists but coexists with a hardcoded color in other.css - fragmented design system, Tier 1.4 (OBSERVED)."
  - file: src/styles/other.css
    lines: L1
    quote: ".btn { color: #333366; }"
    supports_claim: "Hardcoded color and orphaned class: no component emits class=\"btn\", and no stylesheet reference exists anywhere - Tier 1.4 design-system fragmentation (OBSERVED)."
```

## 9. Why this boundary matters
If the route-registration seam stays weak, the application renders a blank page and every view/component in the repository is dead code — the repo's entire UI surface is fictional from the runtime's perspective. Because `dispatch()` fails silently (`src/router.js:10`) and no tests exist (Pass D: no test files), the breakage is invisible: no build step, test, or error path surfaces it. Downstream, any UI diagnostic or implementation work (screen inventories, flow specs, design-system consolidation) would be anchored to files that cannot influence the running application, so the first thing every downstream effort must do — directly or indirectly — is re-establish this wiring; leaving it weak guarantees every subsequent UI step is built on an unproven foundation.

## 10. Candidate next steps
1. **Produce a screen/flow inventory first** (diagnostic): run the UI diagnostic workflow (ui-brief) to map intended screens and flows from the actual files, so the missing wiring is driven by a real screen map rather than guesswork.
2. **Register the routes**: add a single module that calls `router.add(path, handler, guard)` for each screen before `router.start()` (contract at `src/router.js:5-6`), plus a fallback route for the silent-miss case (`src/router.js:10`).
3. **Make the app runnable**: add `package.json` scripts, a bundler/dev-server, and an `index.html` (currently nothing declares a launch path — `package.json:1`).
4. **Wire the component layer**: have `ProfileView`/`SettingsView` compose `src/ui/*` and `src/widgets/*` helpers, eliminating the dead imports (grep: no importers).
5. **Add a routing smoke test**: the router is nearly pure (hash read at `src/router.js:8` is injectable), so a minimal test can pin the add-before-start contract and the silent-miss behavior.

## 11. Recommended next step
Run the **ui-diagnostic-workflow in `plan_only` mode** to produce the first screen/flow inventory (ui-brief) grounded in the actual files — this is the smallest action with the highest leverage because it converts the current zero-documented screen surface into a map that step 2 (route registration) and step 4 (component wiring) can be executed against without guessing. The diagnostic run itself is non-implementing, consistent with this brief's No Implementation boundary.

## 12. Recommended workflow
**`ui-diagnostic-workflow`** (id verified against `skills/workflow-planner/references/workflow-registry.yaml`, lines 715-747: purpose "Analyze UI complexity, screen structure, and design patterns. Produces a high-fidelity UI assessment without implementation"; allowed execution modes `plan_only` / `guided_execution` / `autonomous_execution`, line 725-728). Recommended mode: **`plan_only`** — a listed mode for this workflow and the only one fully compatible with a diagnostic-only handoff.

Why this workflow and not the alternatives:
- **ui-implementation-workflow** (registry lines 748-811): implements via TDD — violates the diagnostic No Implementation boundary, and `plan_only` is not among its allowed modes.
- **implementation-workflow** (registry lines 587-643): the generic architecture default — not UI-specific; would not produce the screen/flow spec this repository needs first.
- **docs-implementation-workflow** (registry lines 812-847): the problem is the screen surface, not documentation; docs alone would not repair the wiring.
- **fast-path-workflow / full-fog-workflow** (registry lines 2-94): orchestration meta-workflows that chain repo-sensemaker → workflow-planner; not needed here because the fog type is already classified with strong evidence.

Preconditions: none blocking — the registry's `ui-diagnostic-workflow` requires `context_artifacts` (this brief supplies them). What is missing before implementation (not before this diagnostic step) is the screen/route inventory the workflow itself will produce.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/strong-ui-fog
source_intent_ref: "N/A - no-user-intent fixture run (GAP-8)"
user_implied_fog_type: unknown
diagnosis_conflict: false
primary_fog_type: ui_fog
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
recommended_workflow_id: ui-diagnostic-workflow
recommended_execution_mode: plan_only
escalation_recommended: false
escalation_required: false
evidence:
  - "src/router.js (L5, L7-L14): route-registration contract with zero callers; dispatch silently no-ops on missing routes (L10)"
  - "src/index.js (L1-L2), src/views/AppView.js (L1-L2): startup only starts the router; no routes registered"
  - "src/views/ProfileView.js (L1), src/views/SettingsView.js (L1), src/ui/form.js (L1), src/ui/table.js (L1), src/widgets/button.js (L1), src/widgets/modal.js (L1): screens/components never imported anywhere - unreachable surface"
  - "package.json (L1): no scripts, dependencies, or main - no declared run/build path"
  - "src/styles/colors.css (L1) vs src/styles/other.css (L1): design token vs hardcoded color; orphaned .btn class"
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
> Run workflow **ui-diagnostic-workflow** in **plan_only** mode against the repository at `experiments/repository-sensemaking-skill-hardening-v1/corpus/strong-ui-fog`. Input artifact: this repository sensemaking brief (primary_fog_type `ui_fog`, weakest boundary Ghost Features). Produce a ui-brief (screen/flow inventory + design-system maturity assessment) grounded in these verified facts: entry `src/index.js:1-2` mounts `src/views/AppView.js:1-2`, which only starts the router; the route table is empty — `router.add` (`src/router.js:5`) has zero callers and `dispatch()` (`src/router.js:7-14`) silently no-ops on missing routes (`src/router.js:10`); screens `src/views/ProfileView.js:1` and `src/views/SettingsView.js:1` are unreachable; components `src/ui/form.js:1`, `src/ui/table.js:1`, `src/widgets/button.js:1`, `src/widgets/modal.js:1` are never imported; styling is split between token `--brand` (`src/styles/colors.css:1`) and hardcoded `#333366` with orphaned `.btn` (`src/styles/other.css:1`); `package.json:1` declares no scripts/dependencies/main. Deliverable: a screen map and flow specification that can drive route registration and component wiring — diagnose and specify only, do not implement.
