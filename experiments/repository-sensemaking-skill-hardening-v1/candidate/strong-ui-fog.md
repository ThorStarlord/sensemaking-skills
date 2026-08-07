# Repository Sensemaking Brief

## 1. Repository goal

`foggy-ui` (the only declared identity, `package.json:1`) appears to be a minimal
browser single-page application: a hash-based router (`src/router.js:8` reads
`window.location.hash`), screen modules under `src/views/`, component modules
under `src/ui/` and `src/widgets/`, and a small CSS layer under `src/styles/`.
The implied intent of the structure is a small UI app with several screens
(profile, settings), reusable form/table components, button/modal primitives,
and a styled shell. **No README or any other document states the goal** — the
goal is inferred (INFERRED) from the package name, the module organization, and
the browser-API usage; there is no documented product contract to verify
against. This is a no-user-intent run: no problem statement or intent artifact
exists, so `user_implied_fog_type: unknown`.

## 2. Current shape

**Inventory (OBSERVED, full recursive listing of the target repo):** exactly 12
files, no README, no `docs/`, no tests, no `index.html`, no CI, no lockfile:

```
package.json                  src/index.js            src/router.js
src/styles/colors.css         src/styles/other.css
src/ui/form.js                src/ui/table.js
src/views/AppView.js          src/views/ProfileView.js src/views/SettingsView.js
src/widgets/button.js         src/widgets/modal.js
```

**Runtime flow (reconstructed from actually opened files):**

- **Startup path:** `src/index.js:1` imports `mount` from `./views/AppView.js` and
  `src/index.js:2` calls it. `AppView.js:2` calls `router.start()`. This is the
  only entry chain; `package.json:1` declares **no scripts, no dependencies, no
  `"type": "module"`**, so there is no declared way to launch the ESM source —
  the launch mechanism (a bundler, a dev server, or an HTML page) is an implicit
  dependency, not a declared one.
- **Orchestration:** `src/router.js:4-16` — `start()` (line 6) delegates to
  `dispatch()` (lines 7-14), which reads the hash (line 8), looks up
  `routes[path]` (line 9), and early-returns if no route matches (line 10).
- **Domain/core logic:** none — there is no application logic beyond rendering
  template strings: `ProfileView.js:1`, `SettingsView.js:1`, `ui/form.js:1`,
  `ui/table.js:1`, `widgets/button.js:1`, `widgets/modal.js:1`.
- **State model:** module-level globals in the router — `routes` (line 1),
  `current` (line 2), `guards` (line 3). No persistence, no database, no
  external system.
- **External integration points:** none — the only outside-world touch is
  `window.location.hash` (`router.js:8`) and (hypothetically) DOM output, which
  does not exist anywhere in the code.
- **Output boundary:** nothing writes to the DOM. Views return HTML strings
  (`ProfileView.js:1`, `SettingsView.js:1`) but no code injects them; there is
  no `index.html` for the browser to load. The output boundary is unreachable.

**Dependency semantics:** `declared` dependencies: none (`package.json:1` has
no dependency arrays). `used`: zero third-party imports across all files —
every `import` statement (`index.js:1`, `AppView.js:1`) is a relative local
module. The ESM syntax itself is an undeclared runtime requirement (no
`"type": "module"`, no bundler config).

**Boundary model (responsibility transitions):** the single meaningful
transition is **route registration → dispatch**. `router.add()` at
`router.js:5` is the only way entries enter `routes`; `dispatch()` at
`router.js:7-14` consumes them. What is validated at this boundary: nothing —
`dispatch()` silently returns when a path is missing (`router.js:10`). What is
assumed: that some other module will register routes before `start()` runs.
**No module in the repository ever calls `router.add`** (OBSERVED via a
repo-wide search for `router.add` / `add(`: the only hit is the definition at
`router.js:5`), so `routes` stays `{}` forever and `dispatch()` always
early-returns. **The app boots and renders nothing.** The never-imported
modules (`ProfileView.js`, `SettingsView.js`, `ui/*`, `widgets/*`) are unwired
orphans — the directory structure promises screens and components that no
entry point reaches.

## 3. Strong signals

- **Tiny, coherent entry chain** — `index.js:1-2` → `AppView.js:2` →
  `router.js:6` is a clean three-hop startup path with no indirection.
- **Centralized router with guard support** — `router.js:4-16` keeps all
  navigation logic in one 16-line module and already models guards
  (`router.js:11`), which is a sensible foundation for a navigation
  architecture once routes exist.
- **Deliberate directory separation** — `views/` (screens), `ui/`
  (components), `widgets/` (primitives), `styles/` (presentation) shows intent
  to separate concerns, even though the boundaries are undocumented.
- **A design token exists** — `styles/colors.css:1` defines `--brand`, i.e.
  someone started a token-based approach.
- **No bloat** — no vendored trees, no lockfile noise, no generated code.

## 4. Missing pieces

- **Route registration:** zero call sites for `router.add()` (`router.js:5`
  defined, never invoked) — the route table can never be populated.
- **DOM mounting:** no code writes rendered HTML anywhere; no `index.html`
  exists for the browser to load (OBSERVED: repository inventory contains no
  `*.html` file).
- **Documentation of any kind:** no README, no flow docs, no design docs —
  the screen set, the user flows, and the navigation structure are entirely
  undocumented (OBSERVED: zero `*.md` files in the repo).
- **Tests:** no test files and no test runner (`package.json:1` has no
  `scripts`); zero automated checks on routing, rendering, or components.
- **Package metadata for execution:** no `scripts`, no dependencies, no
  `"type": "module"` (`package.json:1`) — the repo cannot be started or
  verified by any declared command.
- **Design system coherence:** `--brand: #3366ff` (`colors.css:1`) is defined
  but unused; `other.css:1` hardcodes a second, conflicting blue `#333366`
  instead of consuming the token.
- **Component-boundary definition:** no documented rule for what belongs in
  `ui/` vs `widgets/` vs `views/` — `form`/`table` (compound) sit apart from
  `button`/`modal` (primitive) with no hierarchy or reuse contract.

## 5. Improvement opportunities

- Add a README stating the app's purpose, screen list, and flow map (prerequisite
  for any subsequent UI work).
- Register the existing views as routes (`router.add('#/profile', profile, ...)`
  in `index.js`) and add a fallback route for unknown hashes instead of the
  silent no-op at `router.js:10`.
- Introduce a single mount point that injects handler output into the DOM and
  an `index.html` shell.
- Make `other.css` consume `--brand` (or delete the token) so one color
  convention exists.
- Document the `views` / `ui` / `widgets` layering rule in a short
  `docs/components.md`.
- Add a package `scripts.test` smoke test asserting that `dispatch()` invokes a
  registered handler and that unknown hashes are handled explicitly.

## 6. Weakest boundary

**Candidates generated (scored per the skill's selection rule):**

1. **Route registration → dispatch contract** — `router.add()` (`router.js:5`)
   is never called; `dispatch()` (`router.js:7-14`) silently no-ops on an
   empty table (`router.js:10`). Evidence strength: strong (definition exists,
   zero call sites — repo-wide search). Severity: high (no screen is ever
   reachable). Blast radius: high (the entire UI). Goal relevance: high (the
   repo's whole purpose is displaying screens). Downstream blocking: high
   (every UI task — flows, screens, components — presupposes something
   renders). Uncertainty: low.
2. **No automated validation anywhere** — no tests, no package scripts
   (`package.json:1`). Evidence strength: strong (inventory). Severity:
   medium. Blast radius: high. Goal relevance: medium. Downstream blocking:
   medium. Uncertainty: low.
3. **Design-system fragmentation** — `colors.css:1` token vs `other.css:1`
   hardcoded conflicting blue. Evidence strength: strong. Severity: low.
   Blast radius: low. Goal relevance: medium. Downstream blocking: low.
   Uncertainty: low.
4. **No launch path** — no `index.html`, no scripts, no bundler config
   (`package.json:1`). Evidence strength: strong. Severity: high. Blast
   radius: high. Goal relevance: high. Downstream blocking: high. Uncertainty:
   low. (Overlaps candidate 1; kept separate because it is a packaging
   boundary, but it is a symptom of the same wiring gap.)

**Selection:** candidate 1 — it has the strongest combination of consequence
(nothing renders), evidence (direct, verified), centrality to the repo's goal,
and downstream blocking power. Candidates 2 and 4 are real but describe the
same gap from further away; candidate 3 is cosmetic.

```text
Boundary: route registration → dispatch. router.add() (src/router.js:5) is the
only writer of the routes table (src/router.js:1, `const routes = {}`), and
dispatch() (src/router.js:7-14) is its only reader; the hand-off between the
two is the system's single responsibility transition.
Observed contract: modules register screen handlers with
router.add(path, handler, guard) before router.start() runs, and dispatch()
invokes the handler for the current hash (src/router.js:5, 9, 13).
Observed violation or uncertainty: no module anywhere calls router.add()
(OBSERVED: repo-wide search finds only the definition at src/router.js:5), so
routes is always empty and dispatch() always exits at the silent early return
src/router.js:10 (`if (!r) return;`). The app mounts (src/index.js:2 →
src/views/AppView.js:2 → src/router.js:6) but no screen is ever rendered; the
five screen/component modules (src/views/ProfileView.js:1,
src/views/SettingsView.js:1, src/ui/form.js:1, src/ui/table.js:1,
src/widgets/button.js:1, src/widgets/modal.js:1) are never imported.
Evidence: src/router.js:1, 5, 10; src/index.js:1-2; src/views/AppView.js:2;
grep across the repo for `router.add` / `add(` returning only src/router.js:5.
Weakness type: Implicit Dependencies
Logic trace: dispatch() depends on entries that only router.add() can create,
yet nothing registers any route and nothing validates that registration
happened before start() — the wiring between the router contract and the
screen modules is implicit, undocumented, and unenforced. Per the GAP-6
taxonomy, an unwired/never-imported module is `Implicit Dependencies`
(undocumented wiring), not `Ghost Features`: nothing in the repository
documents these screens or routes as live functionality (there is no README
or spec at all), so there is no documented surface promising them — the defect
is missing wiring, not a false promise. The silent no-op at src/router.js:10
converts the missing wiring from a crash into an invisible failure, which is
why the boundary is "weakest": it fails completely, silently, and
unverifiably.
Failure consequence: the application renders nothing; every screen is
unreachable; any UI change (flow, screen, component) is built on top of a
boundary that has never worked once; there is no test or script that would
catch the failure (package.json:1).
Confidence: high — the absence of call sites is directly verifiable and the
early-return path is directly observable in src/router.js:10. What would raise
it further: an executable boot trace or a unit test booting the router; both
are impossible today because no HTML entry or test runner exists (that
impossibility is itself part of the evidence).
Alternatives considered: (a) Zero Validation — no tests/scripts exist, but
that is a repo-wide condition, not the specific transition where the system
fails; (b) Ghost Features — rejected: GAP-6 requires a documented surface
promising the functionality; there is no documentation at all, so nothing is
"documented as present"; (c) design-system fragmentation (colors.css:1 vs
other.css:1) — real but cosmetic and does not block anything; (d) no launch
path (package.json:1, missing index.html) — real, but it is the packaging
face of the same wiring gap and has weaker evidence (absence of a file) than
the concrete zero-call-site proof of candidate 1.
```

**Weakness type:** Implicit Dependencies

## 6.5. Problem classification (fog type)

**`ui_fog`** — classified via the UI Fog Signals Registry decision procedure,
not vibes. The repository contains frontend code (browser-hash router
`src/router.js:8`, screen/component modules, CSS), so the registry applies.
Tier 1 signals, all four present (STRONG CONFIDENCE per the registry's
"2+ Tier 1 signals" rule):

- **T1.1 Missing UI flow documentation** — zero documentation of any kind in
  the repo (no README, no `docs/`, no `*.md`); screens and interactions are
  unmapped (OBSERVED: repository inventory).
- **T1.2 Frontend components scattered without clear boundaries** — three
  parallel component-ish directories (`src/views/`, `src/ui/`, `src/widgets/`)
  with no documented hierarchy; every component module is an orphan
  (`src/views/ProfileView.js:1`, `src/ui/form.js:1`, `src/widgets/button.js:1`
  are never imported).
- **T1.3 Routing complexity without navigation architecture** — routing exists
  (`src/router.js:4-16`) but no route is registered anywhere, route
  definitions are undocumented, and how screens connect is unknowable from the
  code.
- **T1.4 Design system fragmentation** — a token exists
  (`src/styles/colors.css:1`) but a second, conflicting hardcoded color lives
  in `src/styles/other.css:1`; no design system documentation.

Secondary fog: **architecture_fog** (unwired modules, module-level router
state) is present but secondary. Per the frontend tie-break rule in the skill,
frontend code + ≥1 Tier-1 signal makes `ui_fog` primary; the UI registry is
the specialized decision procedure and wins over the generic architecture
signals. The defect is squarely in the UI layer (screens are unreachable and
undesigned), not provably outside it.

## 7. Evidence

File-level evidence supporting the diagnosis:

- `package.json:1` — `{"name": "foggy-ui"}`: the manifest declares a name and
  nothing else — no scripts, no dependencies, no module type. This is the
  root of the no-launch-path and no-validation findings.
- `src/index.js:1-2` — imports `mount` and calls it: the only startup chain.
- `src/views/AppView.js:2` — `router.start()`: the sole orchestration hop.
- `src/router.js:5` — `add(path, handler, guard)` definition, with **zero call
  sites repo-wide** (OBSERVED via grep): the route table can never be
  populated.
- `src/router.js:10` — `if (!r) return;`: silent no-op on unknown paths,
  which converts the missing wiring into an invisible total failure.
- `src/router.js:8` — `window.location.hash`: confirms this is a browser
  frontend (frontend-code test for the ui_fog registry).
- `src/views/ProfileView.js:1` and `src/views/SettingsView.js:1` — screen
  handlers that return HTML strings but are never imported: unwired screens.
- `src/styles/colors.css:1` vs `src/styles/other.css:1` — token `--brand`
  (`#3366ff`) defined but unused; `#333366` hardcoded instead: fragmented
  design system.
- Absences (OBSERVED from the full recursive inventory): no README, no
  `docs/`, no tests, no `index.html`, no CI — supporting the missing-flow-docs,
  no-validation, and no-launch-path claims. Absence claims are stated as
  absence; nothing is cited that was not opened.

**Logic trace:** The router's `dispatch()` (`src/router.js:7-14`) can only
render a screen whose handler was registered via `router.add()` (`src/router.js:5`),
but no module registers anything (repo-wide grep finds no call sites) and
`dispatch()` returns silently when the table is empty (`src/router.js:10`). The
boot chain (`src/index.js:1-2` → `src/views/AppView.js:2` → `src/router.js:6`)
therefore completes while rendering nothing, and the five screen/component
modules (`src/views/ProfileView.js:1`, `src/views/SettingsView.js:1`,
`src/ui/form.js:1`, `src/ui/table.js:1`, `src/widgets/button.js:1`,
`src/widgets/modal.js:1`) are unreachable orphans — undocumented wiring, i.e.
`Implicit Dependencies`. Because this is a frontend repository with all four
Tier-1 UI signals (no flow docs, scattered components, unroutable navigation,
fragmented design system), the primary fog is `ui_fog` with `architecture_fog`
secondary; the weakest boundary is the registration→dispatch contract, and the
recommended route is the UI diagnostic path (`ui-diagnostic-workflow`).

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: package.json
    lines: L1
    quote: '{"name": "foggy-ui"}'
    supports_claim: "Manifest declares only a name — no scripts, dependencies, or module type; no declared launch or test path."
  - file: src/index.js
    lines: L1
    quote: "import { mount } from './views/AppView.js';"
    supports_claim: "Entry point imports AppView.mount — the only startup chain."
  - file: src/index.js
    lines: L2
    quote: "mount();"
    supports_claim: "Boot proceeds immediately to AppView.mount."
  - file: src/views/AppView.js
    lines: L2
    quote: "export function mount() { router.start(); }"
    supports_claim: "Orchestration hands control to the router with no route registration beforehand."
  - file: src/router.js
    lines: L5
    quote: "  add(path, handler, guard) { routes[path] = { handler, guard }; },"
    supports_claim: "router.add is the only writer of the routes table; a repo-wide search finds zero call sites."
  - file: src/router.js
    lines: L8
    quote: "    const path = window.location.hash.slice(1);"
    supports_claim: "Browser hash routing — confirms frontend code for the ui_fog registry."
  - file: src/router.js
    lines: L10
    quote: "    if (!r) return;"
    supports_claim: "Silent no-op on missing routes converts the empty route table into an invisible total failure."
  - file: src/views/ProfileView.js
    lines: L1
    quote: "export function profile() { return '<div>profile</div>'; }"
    supports_claim: "Screen handler exists but is never imported — an unwired, undocumented screen."
  - file: src/styles/colors.css
    lines: L1
    quote: ":root { --brand: #3366ff; }"
    supports_claim: "Design token defined (Tier 1.4 evidence that a token layer was started)."
  - file: src/styles/other.css
    lines: L1
    quote: ".btn { color: #333366; }"
    supports_claim: "Conflicting hardcoded color ignores the --brand token — fragmented design system."
  - file: src/ui/form.js
    lines: L1
    quote: "export const form = (fields) => `<form>${fields}</form>`;"
    supports_claim: "Component module exists but is never imported — scattered, undocumented component layer."
  - file: src/widgets/button.js
    lines: L1
    quote: "export const button = (label) => `<button>${label}</button>`;"
    supports_claim: "Primitive widget exists but is never imported — no reuse boundary is enforced or documented."
```

## 9. Why this boundary matters

Every downstream activity in this repository — documenting user flows,
specifying screens, designing components, refactoring the router — presupposes
that a screen can be reached. The registration→dispatch boundary has never
worked once and fails silently (`src/router.js:10`), so any UI work starts
from a system that renders nothing, with no test (`package.json:1`) to
distinguish "no screens implemented" from "screens implemented but unwired."
If left weak, the team will keep adding orphan modules (as five already exist:
`src/views/ProfileView.js:1`, `src/views/SettingsView.js:1`, `src/ui/form.js:1`,
`src/ui/table.js:1`, `src/widgets/button.js:1`, `src/widgets/modal.js:1`) while
believing the app has screens, and the navigation architecture — the heart of
the ui_fog — can never be reasoned about because there is nothing to navigate.

## 10. Candidate next steps

1. **Map the intended surface (UI diagnostic):** enumerate the screens the app
   should have (profile, settings, and any others implied by the modules),
   document the user flows and the hash-route table, and record the missing
   wiring (no `router.add` call sites) as the first finding. Smallest scope,
   unblocks everything else.
2. **Wire the existing modules:** register `profile`/`settings` handlers in
   `src/index.js` via `router.add(...)`, add an explicit 404/fallback handling
   instead of the silent return at `src/router.js:10`, and add DOM injection
   plus an `index.html` shell so the app actually renders.
3. **Add a routing smoke test:** a minimal test that boots the router, asserts
   a registered handler is invoked, and asserts unknown hashes are handled —
   the first automated check on the weakest boundary.
4. **Reconcile the design system:** consume `--brand` in `src/styles/other.css`
   (or remove the token) and document the `views`/`ui`/`widgets` layering rule.
5. **Write the missing docs:** README (purpose, screen list, flows) so the
   next sensemaking run has a documented surface to compare against.

## 11. Recommended next step

Step 1 — run the UI diagnostic pass: produce the screen/flow inventory
(including "no documented flows exist") and the route-registration gap list.
It is the smallest concrete action with the highest leverage: it converts the
repository's ui_fog into a specifiable surface, and it will surface the
registration→dispatch gap (`src/router.js:5` vs zero call sites) as the first
thing any implementer must fix. This is diagnostic only — no code changes are
made by this brief.

## 12. Recommended workflow

**`ui-diagnostic-workflow`** (from the canonical `skills/workflow-planner/references/workflow-registry.yaml`, lines 715-747) with execution mode **`plan_only`** (listed in that workflow's `allowed_execution_modes`, registry lines 726-728).

Rationale: the primary fog is `ui_fog` (frontend code + 4/4 Tier-1 UI signals),
and `ui-diagnostic-workflow` is the registry's diagnostic workflow for exactly
this case — its step 1 (docs-aligner, registry line 732) aligns domain
understanding and its step 2 (ui-brief, registry lines 739-744) produces a
`ui_specification` that analyzes screens, flows, and design-system maturity.
That output is precisely what this repository lacks (no flow docs, no screen
map, no design system), and it will force the registration→dispatch gap into
the open. Why not `ui-implementation-workflow` (registry line 748): it
implements flows/screens, but there are no flows or screens to implement yet,
and the routing boundary has never worked — implementing before diagnosing
would build on the broken contract. Why not `architecture-implementation-workflow`
(registry line 848): although the unwired modules are an architecture-flavored
signal, the frontend tie-break rule makes `ui_fog` primary, and the wiring fix
is trivial once the screen surface is specified. `plan_only` is chosen over
`guided_execution`/`autonomous_execution` because this handoff is diagnostic:
no implementation is authorized yet, and `plan_only` is an allowed mode here
(no invented modes; no escalation needed). Precondition before it can run: a
human approves this brief (review_diagnosis gate), since no user-intent
artifact exists for this fixture run.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/strong-ui-fog
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: ui_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "package.json (L1): manifest declares only a name — no scripts, deps, or module type; no launch/test path"
  - "src/router.js (L5): router.add defined but never called anywhere (repo-wide grep) — route table stays empty"
  - "src/router.js (L10): silent early return on missing routes — app mounts but renders nothing"
  - "src/router.js (L8): window.location.hash — browser frontend code (ui_fog registry frontend test)"
  - "src/views/ProfileView.js (L1) / src/views/SettingsView.js (L1): screen handlers never imported — unwired screens"
  - "src/ui/form.js (L1), src/ui/table.js (L1), src/widgets/button.js (L1), src/widgets/modal.js (L1): orphan component modules"
  - "src/styles/colors.css (L1) vs src/styles/other.css (L1): --brand token defined but #333366 hardcoded — fragmented design system"
  - "No README, no docs/, no tests, no index.html (observed in full repository inventory)"
recommended_workflow_id: ui-diagnostic-workflow
recommended_execution_mode: plan_only
weakest_boundary: Implicit Dependencies
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:30:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

> Run the **ui-diagnostic-workflow** (plan_only) against
> `experiments/repository-sensemaking-skill-hardening-v1/corpus/strong-ui-fog`.
> The repository sensemaking brief classifies the primary fog as `ui_fog`
> (frontend code + all four Tier-1 UI signals) with `architecture_fog`
> secondary, and identifies the weakest boundary as the route
> registration→dispatch contract: `src/router.js:5` (`router.add`) has zero
> call sites, so `dispatch()` (`src/router.js:7-14`) always exits at the silent
> early return `src/router.js:10` and no screen renders; the screen/component
> modules (`src/views/ProfileView.js:1`, `src/views/SettingsView.js:1`,
> `src/ui/form.js:1`, `src/ui/table.js:1`, `src/widgets/button.js:1`,
> `src/widgets/modal.js:1`) are never imported. Produce a `ui_specification`
> that (1) enumerates the intended screens and user flows (there are currently
> no flow docs), (2) specifies the hash-route table and its fallback behavior,
> and (3) flags the missing wiring and the design-system split
> (`src/styles/colors.css:1` vs `src/styles/other.css:1`) as the top
> implementation blockers. Do not implement — this step is diagnostic only;
> route the resulting specification to `ui-implementation-workflow` for the
> actual wiring and screen work.
