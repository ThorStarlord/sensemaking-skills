# Repository Sensemaking Brief — corpus/strong-ui-fog

## 1. Repository goal
This repository is a minimal vanilla-JS frontend ("foggy-ui") built around a custom hash router: `src/index.js` mounts `AppView`, which starts the router (`src/router.js`), and the codebase ships three view modules (`AppView`, `ProfileView`, `SettingsView`), two generic `ui/` primitives, two `widgets/` primitives, and two stylesheets with a single design token. The apparent goal is a small dependency-free multi-screen UI with hash-based navigation and a nascent design-token layer — but none of that goal is actually reachable: no route is ever registered, so no screen can ever render, and nothing in the repository declares how the app is loaded, run, or verified.

## 2. Current shape
Twelve files, no README, no `docs/`, no tests, no build/lint config (verified by recursive listing of the corpus tree):
- `package.json` (root) — single line `{"name": "foggy-ui"}`; no scripts, no dependencies, no module type, no entry point.
- `src/index.js` — entry: imports `mount` from `./views/AppView.js` and calls `mount()`.
- `src/router.js` — 16-line custom hash router: `routes = {}`, `add(path, handler, guard)`, `start()`, `dispatch()` with a silent early-return for unregistered paths, a `current` accessor.
- `src/styles/colors.css` — one line: `:root { --brand: #3366ff; }`.
- `src/styles/other.css` — one line: `.btn { color: #333366; }` (hardcoded, ignores the token).
- `src/ui/form.js`, `src/ui/table.js` — generic HTML-string helpers, never imported.
- `src/widgets/button.js`, `src/widgets/modal.js` — generic HTML-string helpers, never imported.
- `src/views/AppView.js` — imports the router and calls `router.start()`.
- `src/views/ProfileView.js`, `src/views/SettingsView.js` — inline HTML-string views, never imported.

There is no HTML entry page, no bundler or module-type declaration, and no documentation of any kind.

## 3. Strong signals
- Routing is centralized in a single small file with a clean API (`src/router.js:4-5`: `export const router = { add(path, handler, guard) {...} }`), including a guard hook and a `current` accessor (`src/router.js:11`, `src/router.js:15`) — the intended navigation architecture is conceptually simple and not scattered.
- The codebase is tiny, dependency-free, and readable; module boundaries are *intended* via ES imports (`src/index.js:1`).
- A design-token convention is started: `src/styles/colors.css:1` defines `--brand: #3366ff` on `:root`, signaling awareness of a design system.
- Views and widgets are separated into dedicated directories (`src/views/`, `src/ui/`, `src/widgets/`), indicating an intended component hierarchy even though it is undocumented and half the modules are unwired.

## 4. Missing pieces
- Documentation of any kind: no README.md, no `docs/`, no flow or screen specs, no navigation map (UI Fog Tier 1.1 signal; the three views + modal are never mapped to any user journey).
- Any route registration: `router.add` is never called anywhere in the repository (grep for `router.add`/`.add(` across the tree matches only `src/router.js:5` itself), so `routes` stays `{}` (`src/router.js:1`) and `dispatch()` always early-returns (`src/router.js:9-10`) — no screen can ever render.
- An entry/loading contract: `package.json:1` declares no `"type": "module"`, no `main`, no `scripts`, and there is no `index.html`; `src/index.js:1` uses an ES `import`, so how the app is loaded in a browser is undeclared.
- Automated checks of any kind: no test files, no test script in `package.json:1`, no linter/CI (Zero Validation; grep for `test`/`spec` returns no matches).
- A coherent component boundary: `src/ui/form.js:1` and `src/widgets/button.js:1` are both generic atoms with no documented reason for the `ui/` vs `widgets/` split, and neither — nor `table`, `modal`, `ProfileView`, or `SettingsView` — is imported anywhere (6 of 10 modules are orphaned; UI Fog Tier 1.2 signal).
- A unified design system: `src/styles/other.css:1` hardcodes `#333366` instead of using the `--brand` token defined in `src/styles/colors.css:1`; two tiny stylesheets with no shared convention (UI Fog Tier 1.4 signal).
- Accessibility, responsive design, and interaction feedback: no `aria-`/`role=`/`@media`/breakpoint or loading/error/empty-state handling anywhere (grep returns no matches; UI Fog Tier 2.2 and 2.3 signals).

## 5. Improvement opportunities
- Add a README documenting the intended flows (e.g., profile, settings) and the navigation map before any redesign work.
- Register the three views in `src/router.js` (or wherever routing is configured) and add a fallback/404 route so `dispatch()` never silently no-ops (`src/router.js:9-10`).
- Declare the load contract: `"type": "module"` in `package.json:1` plus a minimal HTML entry, mirroring the import style of `src/index.js:1`.
- Add a smoke test that mounts the app and asserts a route renders — this would have caught the empty route table immediately.
- Either consolidate `src/ui/` and `src/widgets/` into one documented component layer or delete the orphaned modules.
- Make `src/styles/other.css:1` consume the `--brand` token (or delete the token) so the design language is single-sourced.

## 6. Weakest boundary
The weakest boundary is the **validation boundary around the entire UI layer**: nothing in the repository checks that any screen renders, any route resolves, or any module is wired. Concretely, `package.json:1` declares no scripts (no test, lint, or build entry), no test files exist anywhere, and the router itself performs no validation — `src/router.js:9-10` (`const r = routes[path]; if (!r) return;`) swallows missing routes silently. Because of this, the repository's most severe defect is completely invisible: `router.add` is never called, so `routes` is permanently empty (`src/router.js:1`), `dispatch()` always early-returns, and the app renders nothing — yet no command, test, or check exists that would ever surface this. The boundary is not merely "no tests"; it is that the core navigation logic is *designed* to fail silently (no fallback, no error, no assertion), which is exactly the shape of a Zero Validation boundary.

**Weakness type:** Zero Validation

Logic trace: `src/router.js:4-5` implements a route-registration API, but a grep for `router.add` across the tree finds no caller, so the `routes` table declared at `src/router.js:1` is never populated; `src/router.js:9-10` then silently returns for any path lookup, meaning an empty route table produces no observable error; `package.json:1` (no scripts) and the absence of any test file mean no automated check exists that could detect the empty table; therefore the repository's core logic (routing → screen rendering) has no automated verification and its one fatal defect is undetectable by any tool — that is Zero Validation, the weakest boundary in the repository.

## 6.5. Problem classification (fog type)
**primary_fog_type: ui_fog.** This is a frontend repository (JS views, widgets, router, stylesheets), and the UI Fog Signals Registry check yields 4 of 4 Tier 1 signals: (1.1) user flows and screens are entirely undocumented — no README.md, no `docs/`, no flow specs, no Figma/Storybook references; (1.2) frontend components are scattered across three overlapping directories (`src/views/`, `src/ui/`, `src/widgets/`) with no documented hierarchy and 6 of 10 modules never imported; (1.3) routing exists but is unwired and undocumented — no route registration anywhere, navigation structure unmapped; (1.4) the design system is fragmented — one token defined (`src/styles/colors.css:1`) and immediately ignored by a hardcoded color (`src/styles/other.css:1`). Tier 2 signals are also present: (2.1) zero tests for UI behavior, (2.2) accessibility never addressed, (2.3) no responsive design (no media queries or breakpoints), (2.4) three views plus a modal exist with zero documented screens. Per the registry decision tree, 2+ Tier 1 signals → STRONG CONFIDENCE `ui_fog`. The weakest boundary (Zero Validation) sits inside the UI layer — the routing/navigation architecture is unverified — so the fog classification and the boundary agree. `user_implied_fog_type: unknown` (no user-intent artifact was supplied in this fixture run, so no intent conflict can be detected); `diagnosis_conflict: false`; `escalation_recommended: false` (high-confidence diagnosis with directly cited evidence, and the workflow registry contains a matching diagnostic workflow).

## 7. Evidence
The repository contains no README.md and no `docs/` directory — verified by a recursive listing of the `corpus/strong-ui-fog` tree — so every claim below rests on direct code inspection. `package.json:1` is only `{"name": "foggy-ui"}`: no scripts, dependencies, module type, or entry point, so there is no way to run, build, or test the app as shipped. `src/router.js:1` initializes `routes = {}` and `src/router.js:5` defines `add(path, handler, guard)`, but a grep for `router.add` across the whole tree matches only that definition line — no caller exists, so the route table is never populated; `src/router.js:9-10` (`const r = routes[path]; if (!r) return;`) then silently no-ops for every path. `src/views/AppView.js:1-2` is the only mounted module chain (`src/index.js:1` → `AppView` → `router.start()`), so the entire app renders nothing. `src/styles/colors.css:1` defines the sole design token `--brand: #3366ff`, which `src/styles/other.css:1` ignores in favor of a hardcoded `#333366`. `src/widgets/button.js:1`, `src/widgets/modal.js:1`, `src/ui/form.js:1`, `src/ui/table.js:1`, `src/views/ProfileView.js:1`, and `src/views/SettingsView.js:1` are each exported but never imported anywhere (grep for `form`/`table`/`button`/`modal`/`profile`/`settings` across the tree matches only their own definition lines) — six orphaned modules. No test, spec, `aria-`, `role=`, or media-query content exists (grep returns no matches).

Logic trace: The cited evidence chains as follows — (a) the navigation architecture is dead on arrival: `src/router.js:5` implements `add()` but nothing calls it, so the table at `src/router.js:1` is empty; (b) the router is engineered to hide this: `src/router.js:9-10` returns silently for unregistered paths, so an empty route table produces no error or fallback; (c) nothing could catch it anyway: `package.json:1` has no test/lint/build scripts and no test files exist, so the repository has zero automated checks (Zero Validation); (d) the UI layer is simultaneously undocumented (Tier 1.1, no README/flows), unbounded (Tier 1.2, six orphaned modules across `ui/`/`widgets/`/`views/`), and unstyled (Tier 1.4, token defined at `src/styles/colors.css:1` but ignored at `src/styles/other.css:1`). The root defect — the thing that makes the repository's stated goal (a multi-screen routed UI) unreachable — is that the core routing logic is unvalidated and silently broken, so the weakest boundary is **Zero Validation** and the fog type is **ui_fog**.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: package.json
    lines: L1
    quote: '{"name": "foggy-ui"}'
    supports_claim: "No scripts, dependencies, module type, or entry point - nothing declares how to run, build, or validate the app (Zero Validation)."
  - file: src/router.js
    lines: L5
    quote: 'add(path, handler, guard) { routes[path] = { handler, guard }; },'
    supports_claim: "Route-registration API exists, but a tree-wide grep shows router.add is never called - the routes table is never populated."
  - file: src/router.js
    lines: L9-L10
    quote: "const r = routes[path];\nif (!r) return;"
    supports_claim: "dispatch() silently no-ops for any path missing from the (empty) routes table - no fallback, no error, no validation of route registration."
  - file: src/views/AppView.js
    lines: L1-L2
    quote: "import { router } from '../router.js';\nexport function mount() { router.start(); }"
    supports_claim: "The only mounted module chain (index.js -> AppView -> router.start()) starts a router with zero registered routes, so no screen can ever render."
  - file: src/styles/colors.css
    lines: L1
    quote: ":root { --brand: #3366ff; }"
    supports_claim: "A single design token exists, signaling an intended design system (UI Fog Tier 1.4 signal is present because it is never consumed)."
  - file: src/styles/other.css
    lines: L1
    quote: ".btn { color: #333366; }"
    supports_claim: "Hardcoded color that ignores the --brand token - fragmented design system with no shared convention."
  - file: src/widgets/button.js
    lines: L1
    quote: 'export const button = (label) => `<button>${label}</button>`;'
    supports_claim: "Generic widget is never imported anywhere - component boundaries across ui/, widgets/, and views/ are undocumented and largely orphaned (UI Fog Tier 1.2)."
  - file: src/ui/form.js
    lines: L1
    quote: 'export const form = (fields) => `<form>${fields}</form>`;'
    supports_claim: "Generic ui/ primitive is never imported - six of ten modules are unreachable, and the ui/ vs widgets/ split has no documented rationale."
```

## 9. Why this boundary matters
Because nothing validates the UI layer, the repository ships in a state where its core feature — hash-based navigation to profile/settings screens — cannot execute at all, and no tool, command, or test can detect that. Consequences: any downstream diagnostic (ui-brief, ui-flow, screen specs) would analyze screens that never render; any test added later would fail at the very first assertion and risk being misattributed to the test rather than to the empty route table; a team member inheriting the repo has no signal about what works, so effort would go into polishing views (`src/views/ProfileView.js:1`, `src/views/SettingsView.js:1`) that are unreachable; and the silent early-return at `src/router.js:9-10` actively masks the defect by design — a validation gap that is also a diagnosability gap. This is the weakest boundary because it is the one that makes the repository's own goal unachievable while remaining invisible to every existing check (of which there are none).

## 10. Candidate next steps
1. Add a smoke test (and a `test` script in `package.json:1`) that mounts the app and asserts a route renders — it will fail immediately, exposing the empty route table (directly addresses Zero Validation).
2. Register the views: call `router.add('/profile', profile)` and `router.add('/settings', settings)` (or configure routes centrally) and add a fallback route so `src/router.js:9-10` never silently no-ops.
3. Declare the load contract: add `"type": "module"` and a `start` script to `package.json:1`, plus a minimal HTML entry that loads `src/index.js` (the ES `import` at `src/index.js:1` currently has no declared loader).
4. Write a README mapping the two intended flows (profile, settings) and the navigation architecture (addresses Tier 1.1 and Tier 1.3).
5. Run the `ui-diagnostic-workflow` in `plan_only` mode to produce a ui-brief and flow/screen specs before any redesign (the registry-grounded downstream for `ui_fog`).

## 11. Recommended next step
Add a minimal smoke test that imports the router, registers a stub route, calls `dispatch()`, and asserts the handler ran — wired into a `test` script in `package.json:1`. It is the smallest change with the highest leverage: it converts the silent no-op at `src/router.js:9-10` into a visible failure, proves (and then fixes) the empty-route-table defect, and establishes the validation layer whose absence is the weakest boundary. It is directly evidenced by `package.json:1` (no scripts), the absent test files, and the never-called `router.add` at `src/router.js:5`.

## 12. Recommended workflow
`ui-diagnostic-workflow` from `skills/workflow-planner/references/workflow-registry.yaml` (registry line 715): "Analyze UI complexity, screen structure, and design patterns. Produces a high-fidelity UI assessment without implementation." It matches the `ui_fog` classification and stays diagnostic (`plan_only` execution mode, which the workflow allows), consistent with this skill's no-implementation boundary.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/strong-ui-fog
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
  - "package.json (line 1): only {\"name\": \"foggy-ui\"} - no scripts, tests, module type, or entry point; zero automated validation"
  - "src/router.js (lines 1, 5): routes table initialized empty and add() defined but never called anywhere - no route is ever registered"
  - "src/router.js (lines 9-10): dispatch() silently returns for any path missing from the routes table - no fallback or error"
  - "src/views/AppView.js (lines 1-2): the only mounted module chain starts the router with zero registered routes"
  - "src/styles/colors.css (line 1): --brand token defined but never consumed"
  - "src/styles/other.css (line 1): hardcoded #333366 color ignoring the --brand token"
  - "src/widgets/button.js (line 1) and src/ui/form.js (line 1): generic components never imported - six of ten modules orphaned"
  - "No README.md, docs/, or tests anywhere in the tree (recursive listing; grep for test/spec/aria/media returns no matches)"
weakest_boundary:
  type: Zero Validation
  evidence: "package.json:1 declares no scripts, no test files exist, and src/router.js:9-10 silently no-ops on unregistered routes - the entire UI layer has no automated check, so the never-populated route table (router.add never called, src/router.js:5) ships undetected"
weakness_type: Zero Validation
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
Prompt for `workflow-planner`:

"Route this repository sensemaking brief (artifact_id: repository_sensemaking_brief; primary_fog_type: ui_fog; weakest_boundary: Zero Validation; source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md) to the `ui-diagnostic-workflow` in `plan_only` mode. Context: corpus/strong-ui-fog is a 12-file vanilla-JS frontend whose custom hash router never has any route registered (router.add is never called), so dispatch() at src/router.js:9-10 always silently early-returns and no screen can render; package.json declares no scripts, module type, or entry point, there are no tests, no README or flow docs, and the design system is fragmented (--brand token defined in src/styles/colors.css:1 but ignored by a hardcoded color in src/styles/other.css:1). Produce the orchestration plan without implementing anything."
