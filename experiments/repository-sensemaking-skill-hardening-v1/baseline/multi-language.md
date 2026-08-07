# Repository Sensemaking Brief — multi-language

## 1. Repository goal
`multi-language` is a minimal mixed-language project scaffold: a Python "core"
component, a Node.js "helper" component, and a POSIX shell setup script,
orchestrated through a single Makefile. The README (`README.md:1-3`) states the
intent in one line — "# multi-lang" / "Mixed-language project." — and the
Makefile (`Makefile:1-5`) is the only behavioral contract: `make all` runs
`python core/main.py`, and `make helper` runs `node helper/run.js`. The repo
appears to be a skeleton demonstrating how multiple language runtimes coexist
in one build graph.

## 2. Current shape
The repository contains exactly five files (structural proof from `ls`, no
hidden files):

```
multi-language/
├── README.md              (3 lines: title + one-line "Mixed-language project." description)
├── Makefile               (5 lines: targets all / core / helper)
├── core/
│   └── main.py            (1 line: `print('core')`)
├── helper/
│   └── run.js             (1 line: `console.log('TODO');`)
└── scripts/
    └── setup.sh           (2 lines: `#!/bin/sh` + `echo setup`)
```

The Makefile defines three targets: `all: core` (`Makefile:1`), `core:` running
`python core/main.py` (`Makefile:3`), and `helper:` running
`node helper/run.js` (`Makefile:5`). Notably absent (structural proof from
`ls`): no test files or test directory, no CI configuration, no dependency
manifests (`package.json`, `requirements.txt`, `pyproject.toml`), no
`package-lock.json`, no LICENSE, and no documentation beyond the two-line
README.

## 3. Strong signals
- **Single orchestration point**: the Makefile (`Makefile:1-5`) centralizes the
  build graph — `all`, `core`, and `helper` targets map each component to its
  runtime (`python core/main.py` at `Makefile:3`, `node helper/run.js` at
  `Makefile:5`) instead of scattering invocation commands across files.
- **Clear per-component directory separation**: `core/`, `helper/`, and
  `scripts/` each hold exactly one component, so the multi-language intent is
  structurally visible.
- **The Python component is runnable as advertised**: `core/main.py:1`
  (`print('core')`) executes without modification, and the `core` target
  (`Makefile:3`) correctly invokes it.
- **A valid shell shebang**: `scripts/setup.sh:1` starts with `#!/bin/sh`,
  making the script directly executable under a POSIX shell.

## 4. Missing pieces
- **The JS "helper" is an unimplemented stub**: `helper/run.js:1` contains only
  `console.log('TODO');` — the component the Makefile's `helper` target
  (`Makefile:4-5`) advertises has no actual functionality.
- **The default target excludes most of the repo**: `all: core` (`Makefile:1`)
  depends only on `core`; `helper` and `setup.sh` are never invoked by
  `make all`, so the mixed-language surface is never exercised by the default
  path.
- **`scripts/setup.sh` is orphaned**: nothing in the repository references it —
  it appears in neither the Makefile (`Makefile:1-5`) nor the README
  (`README.md:1-3`), so its invocation contract is undefined.
- **No usage documentation**: `README.md:1-3` says only "Mixed-language
  project." — no mention of `make all`, `make helper`, runtime requirements
  (Python version, Node version), or setup.
- **No verification layer**: there are no tests, no CI config, and no
  dependency manifests, so nothing automates checking that the scaffold
  actually runs.

## 5. Improvement opportunities
- Replace the `console.log('TODO');` stub (`helper/run.js:1`) with a real
  helper behavior, or delete the `helper` target (`Makefile:4-5`) and the
  directory if the helper is not needed — resolve the advertised-but-empty
  feature either way.
- Wire `scripts/setup.sh` into the build graph (e.g. a `setup:` target or an
  `all` prerequisite in `Makefile:1`) so the script's existence matches its
  usage.
- Document usage in `README.md` after line 3: the `make` targets, the runtimes
  required (Python, Node), and whether setup must run first.
- Add a smoke-test target to the Makefile (e.g. `test:` invoking both `core`
  and `helper`) or a minimal CI workflow so the two runtimes are verified from
  a clean checkout.
- Add dependency manifests (`package.json` for the helper, a requirements
  file for core) so the multi-language toolchain is reproducible.

## 6. Weakest boundary
The weakest boundary is the **contract between the advertised component set
and the actual implementation of the JavaScript helper**. The repository
presents itself as a working mixed-language project: the README claims
"Mixed-language project." (`README.md:3`) and the Makefile exposes a `helper`
target that runs `node helper/run.js` (`Makefile:4-5`). But the only JS file in
the repo, `helper/run.js:1`, is `console.log('TODO');` — a placeholder with no
functionality. The `helper` feature is therefore documented in the build
interface and implied by the README, yet has no corresponding implementation:
running `make helper` succeeds and produces nothing but a TODO log. The
boundary between "this component exists" and "this component works" is
enforced nowhere.

Logic trace: `Makefile:4-5` defines the `helper` target and invokes
`node helper/run.js`; opening that file shows exactly one line,
`console.log('TODO');` (`helper/run.js:1`) — a marker, not an implementation;
the README's claim of a "Mixed-language project." (`README.md:3`) implies both
language components are functional, but only the Python half
(`core/main.py:1`, `print('core')`) performs any real action; therefore the
JS helper is functionality that is mentioned (Makefile target + README claim)
without a corresponding implementation, which is the Ghost Features weakness
type. The orphaned `scripts/setup.sh` (unreferenced by `Makefile:1-5` and
`README.md:1-3`) and the `all` target omitting `helper` (`Makefile:1`)
reinforce the same conclusion from the wiring side: the mixed-language surface
is partially declared and partially real.

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)
**architecture_fog** — the primary uncertainty is structural: an advertised
component (`helper`) has no implementation, the default build graph
(`Makefile:1`) covers only one of three components, and one script
(`scripts/setup.sh:1-2`) is wired to nothing. These are codebase
structure/completeness defects, not product, UI, or documentation problems.

- Not `ui_fog`: the repository contains no frontend code at all (no
  React/Vue/HTML/CSS/JSX), so per the UI Fog Signals Registry decision tree
  (`skills/repo-sensemaker/references/ui-fog-signals.md:156-157`: "Does the
  codebase have frontend/UI code? ├─ NO → Not ui_fog") the answer is
  "Not ui_fog".
- Not `product_fog`: there is no user-need ambiguity — the goal (a
  mixed-language scaffold) is stated plainly in `README.md:3`.
- Not `docs_fog`: the README is thin, but the acute defect is not missing
  prose — it is that the JS component advertised by the build interface
  (`Makefile:4-5`) does nothing. Fixing documentation alone would leave the
  stub in place.

## 7. Evidence
The diagnosis rests on four cited observations:

1. `helper/run.js:1` is the entire JavaScript component: `console.log('TODO');`
   — a placeholder with no functionality, despite the `helper` target at
   `Makefile:4-5` advertising it as a runnable component.
2. `Makefile:1` (`all: core`) shows the default target covers only the Python
   component; `Makefile:3` and `Makefile:5` map `core` → `python core/main.py`
   and `helper` → `node helper/run.js`, so the build graph itself acknowledges
   both languages while the default path exercises only one.
3. `README.md:3` ("Mixed-language project.") is the only documentation of the
   repo's intent — it claims both language families are present and
   functional, with no caveat that the JS half is a stub.
4. `scripts/setup.sh:1-2` (`#!/bin/sh` / `echo setup`) exists but is
   referenced nowhere — a second, wiring-side symptom that the component set
   is incompletely connected. `core/main.py:1` (`print('core')`) is the only
   file with real behavior, confirming the Python half works while the JS half
   does not.

Logic trace: `Makefile:4-5` exposes a `helper` target, and the README
(`README.md:3`) describes the repo as a mixed-language project — together they
establish that a functioning JavaScript helper is part of the advertised
surface. Reading the sole JS source, `helper/run.js:1`, yields only
`console.log('TODO');`, i.e. no behavior is implemented behind that advertised
surface. Because the documentation/build-interface promise (helper exists and
runs) is not backed by any implementation, the gap is exactly the Ghost
Features weakness type — not a naming drift (Vocabulary Drift), not a format
mismatch (Contract Mismatch), not an unvalidated path (Implicit Dependencies,
which instead characterizes the secondary `setup.sh` wiring gap), and not a
missing automated check (Zero Validation) — the defect is an advertised
feature with no code behind it.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: helper/run.js
    lines: L1
    quote: "console.log('TODO');"
    supports_claim: "The entire JavaScript helper is a TODO placeholder — the component advertised by the Makefile helper target has no implementation (Ghost Features)."
  - file: Makefile
    lines: L4-L5
    quote: 'node helper/run.js'
    supports_claim: "The Makefile exposes a helper target that invokes the stub run.js, advertising functionality the file does not provide."
  - file: Makefile
    lines: L1
    quote: 'all: core'
    supports_claim: "The default target depends only on core; helper and setup.sh are never exercised by `make all`."
  - file: README.md
    lines: L1-L3
    quote: "Mixed-language project."
    supports_claim: "The README claims a mixed-language project with no caveat that the JavaScript half is an unimplemented stub."
  - file: core/main.py
    lines: L1
    quote: "print('core')"
    supports_claim: "The Python core has real behavior and runs via `make core`, so the mixed-language claim is only half true."
  - file: scripts/setup.sh
    lines: L1-L2
    quote: "echo setup"
    supports_claim: "setup.sh exists with a valid shebang but is referenced by neither the Makefile nor the README — an orphaned script."
```

## 9. Why this boundary matters
A consumer following the repository's own interface gets a false signal: `make
helper` exits successfully while the "helper" does nothing, and the README
(`README.md:3`) promises a mixed-language project whose JavaScript half is a
no-op. Because the `all` target (`Makefile:1`) never touches the JS component,
the stub can ship, grow stale, or be built upon indefinitely without any
failure surfacing — the scaffold's whole point (demonstrating a working
multi-language setup) is silently violated. Anyone extending the repo will
copy the TODO pattern or assume the helper's contract exists, and the orphaned
`scripts/setup.sh` means environment setup is equally undocumented. For a
fixture whose value is "this is how the polyglot parts fit together", an
advertised-but-empty component is the core promise at risk.

## 10. Candidate next steps
1. Implement the helper's actual behavior in `helper/run.js:1` (replacing
   `console.log('TODO');` with a real function), then verify `make helper`
   exercises it.
2. If the helper is not needed, remove it consistently: delete the `helper`
   target (`Makefile:4-5`), the `helper/` directory, and drop the
   mixed-language framing from `README.md:3`.
3. Wire `scripts/setup.sh` into the build graph (add a `setup:` target or make
   it a prerequisite of `all` at `Makefile:1`) and document it in the README.
4. Expand `README.md:1-3` with usage: the make targets, required runtimes
   (Python, Node), and setup invocation.
5. Add a smoke-test target or minimal CI that runs both `core` and `helper`
   from a clean checkout, so the two-runtime claim is verified automatically.

## 11. Recommended next step
Resolve the helper contradiction at its source: replace the `console.log('TODO');`
stub (`helper/run.js:1`) with a minimal real behavior that the `helper` target
(`Makefile:4-5`) can exercise, then run `make helper` to confirm the
advertised component actually does something — or, if no helper behavior is
intended, delete the `helper` target, directory, and the unqualified
"Mixed-language project." claim (`README.md:3`) in the same change. This is
the smallest change that makes the documented surface (`Makefile:1-5`,
`README.md:3`) true, and it unblocks the wiring and documentation steps on top
of it.

## 12. Recommended workflow
`architecture-implementation-workflow` — defined in
`skills/workflow-planner/references/workflow-registry.yaml:848` as "For
architecture/refactoring problems. Aligns domain, creates refactoring spec,
decomposes into issues, and implements via TDD." It matches this diagnosis:
the weakest boundary is structural (component completeness and build-graph
coverage), not product, UI, or docs. (`implementation-workflow` at
`workflow-registry.yaml:587` is the generic fallback but is less specific to
the component-boundary shape of this fix.)

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-language
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "helper/run.js:1: entire JS component is `console.log('TODO');` — advertised helper has no implementation"
  - "Makefile:1: `all: core` default target excludes helper and setup.sh"
  - "Makefile:4-5: `helper:` target invokes `node helper/run.js`, advertising the stub"
  - "README.md:3: 'Mixed-language project.' claim with no caveat that the JS half is a stub"
  - "scripts/setup.sh:1-2: exists with valid shebang but is referenced nowhere"
  - "core/main.py:1: `print('core')` is the only real behavior in the repo"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
> Run workflow `architecture-implementation-workflow` with
> `context_artifacts = [this repository_sensemaking_brief]` for repository
> `multi-language`. Scope: make the advertised component surface true —
> either implement real behavior in `helper/run.js` (replacing the
> `console.log('TODO');` stub) so the `helper` target in the Makefile works as
> documented, or remove the `helper` target, the `helper/` directory, and the
> "Mixed-language project." claim in the README if no helper is intended; wire
> the orphaned `scripts/setup.sh` into the build graph and document usage in
> the README. Produce the refactoring spec and issue decomposition; do not
> alter `core/main.py` behavior.
