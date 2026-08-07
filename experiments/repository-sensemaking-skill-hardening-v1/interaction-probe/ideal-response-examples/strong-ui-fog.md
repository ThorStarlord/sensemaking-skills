# Ideal response prototype — strong-ui-fog

**What this is:** a 12-file dependency-free vanilla-JS frontend with a custom
hash router, three views, generic ui/widget primitives, and two stylesheets
(src/). `package.json:1` declares nothing beyond a name — no scripts, no
entry point, no module type.

**How it works (as shipped):** it doesn't. `src/index.js:1-2` mounts AppView,
which starts the router (src/views/AppView.js:1-2), but **no route is ever
registered** — `router.add` is never called (verified by grep), so
`dispatch()` silently no-ops for every path (src/router.js:9-10) and no screen
can render. Even the one view that would render (dashboard-style markup via
widgets) is never invoked. The design token `--brand` (src/styles/colors.css:1)
is ignored by the hardcoded color in src/styles/other.css:1.

**The one important weakness:** the app is structurally unstartable — the
routing contract is defined (router.add exists) but never wired. This makes
every other weakness (no tests, no build, no a11y) unreachable concerns until
the wiring exists. Evidence: router.js:1-16, AppView.js:1-2, absence of any
`router.add` call site, package.json:1.

**Alternatives considered:** (1) missing UI tests (rejected as primary —
tests cannot run against screens that cannot render); (2) fragmented design
tokens (rejected as primary — cosmetic until a screen exists).

**Confidence: high** on the wiring failure (directly observed); **medium** on
intent — with no README, why the router was never wired is unknown (abandoned
work vs in-progress work are indistinguishable from the code alone).

**Recommended next step:** wire one route (register `/dashboard` ->
renderDashboard) and make `npm start` real (package.json:1), then verify a
single screen renders before any other frontend work.

**Ask before:** choosing between "finish the app" vs "this is abandoned, stop"
— the code alone cannot answer which the owner wants.
