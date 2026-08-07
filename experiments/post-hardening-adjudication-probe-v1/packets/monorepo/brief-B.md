# Repository Sensemaking Brief: monorepo (monorepo fixture)

## 1. Repository goal
A minimal pnpm-workspace monorepo containing two small JavaScript utility packages: `mathkit` (a one-function math helper exposing `add`) and `strkit` (a string helper exposing `concat`, which is built on top of `mathkit`'s `add`). The intended shape is stated in `README.md:1` ("# monorepo") and `README.md:3` ("Two packages."), and the package set is defined by `pnpm-workspace.yaml:1-2` (`packages: - packages/*`). The goal appears to be a tiny, reusable-utility monorepo where `strkit` composes `mathkit` rather than duplicating arithmetic.

## 2. Current shape
The repository is six files across three locations (plus `.git/`), no test files, no CI config, and no root package manifest:

- `README.md` (3 lines): project title (`README.md:1`) and the one-line purpose "Two packages." (`README.md:3`).
- `pnpm-workspace.yaml` (2 lines): the workspace glob `packages/*` (`pnpm-workspace.yaml:1-2`).
- `packages/mathkit/package.json` (1 line): `{"name": "mathkit", "version": "1.0.0", "main": "src/index.js"}` — name, version, and entry point only.
- `packages/mathkit/src/index.js` (1 line): `export const add = (a, b) => a + b;` — the entire package.
- `packages/strkit/package.json` (1 line): `{"name": "strkit", "version": "1.0.0", "main": "src/index.js"}` — name, version, and entry point only; **no `dependencies` field at all**.
- `packages/strkit/src/index.js` (2 lines): `import { add } from 'mathkit';` (`packages/strkit/src/index.js:1`) then `export const concat = (a, b) => a + b + add(1, 1);` (`packages/strkit/src/index.js:2`).

There is no root `package.json`, no `pnpm-lock.yaml`, no `node_modules`, no `tests/`, no `docs/`, and no CI configuration anywhere in the tree.

## 3. Strong signals
- The workspace layout is conventional and minimal: `pnpm-workspace.yaml:1-2` declares a single glob (`packages/*`) that exactly covers the two real package directories — no drift between the declared workspace and the actual tree.
- Package boundaries are crisp: each package is one concern with a single-file entry point declared via `main` in its `package.json` (`packages/mathkit/package.json:1`, `packages/strkit/package.json:1`).
- `strkit` reuses `mathkit`'s `add` instead of reimplementing addition (`packages/strkit/src/index.js:1-2`) — a healthy composition signal for such a small monorepo.
- The README is honest at its level of detail: "Two packages." (`README.md:3`) matches the actual tree, so there is no misleading documentation to untangle.

## 4. Missing pieces
- **Undeclared cross-package dependency**: `packages/strkit/src/index.js:1` imports `'mathkit'`, but `packages/strkit/package.json:1` declares no `dependencies` (or `devDependencies`) at all. The only thing tying `strkit` to `mathkit` is the import statement itself — nothing in the manifest makes the dependency explicit or versioned.
- **Missing module-system declaration**: both packages ship ESM syntax (`export` at `packages/mathkit/src/index.js:1`, `import`/`export` at `packages/strkit/src/index.js:1-2`) but neither `package.json` declares `"type": "module"`, so Node.js would treat `src/index.js` as CommonJS and throw `SyntaxError: Cannot use import statement outside a module` on first load.
- **No tests**: the tree contains no test files, no test runner dependency, and no test script.
- **No root tooling**: no root `package.json` with workspace scripts, no lockfile, no CI configuration — nothing validates that the workspace installs, resolves, or runs.
- **No API documentation**: the semantics of `add`/`concat` (including `concat`'s hidden `+2` term from `add(1, 1)`) are documented nowhere.

## 5. Improvement opportunities
- Add a root `package.json` with `"scripts"` (e.g. `pnpm -r test`) and a devDependency test runner, plus a minimal unit-test suite for `add` and `concat`.
- Declare `"type": "module"` in both package manifests (or rename entry files to `.mjs`) so the existing ESM syntax actually runs under Node.
- Add an `exports` map (and `files`) to `packages/mathkit/package.json` so the package is publishable and its public surface is explicit.
- Commit a `pnpm-lock.yaml` and a minimal CI step (`pnpm install --frozen-lockfile && pnpm -r test`) to make resolution failures visible.
- Document the `concat` semantics (`a + b + 2`) in the README so the surprising constant term is not a silent contract.

## 6. Weakest boundary
The boundary between `strkit` and `mathkit` — the package import boundary — is unenforced. `packages/strkit/src/index.js:1` imports `'mathkit'` as if it were a declared dependency, but `packages/strkit/package.json:1` contains only `name`, `version`, and `main`: no `dependencies` entry, no workspace protocol, no version range. Under pnpm's default isolated `node_modules` layout (the tool this repo explicitly adopts via `pnpm-workspace.yaml:1-2`), an undeclared cross-package import resolves only if hoisting happens to place `mathkit` where `strkit` can see it; nothing in the repository declares, pins, or validates that link. Additionally, both packages ship ESM source (`packages/mathkit/src/index.js:1`, `packages/strkit/src/index.js:1-2`) without `"type": "module"` in either manifest, so even after resolution the entry files will not load under Node's default CommonJS interpretation.

**Weakness type:** Implicit Dependencies

Logic trace: `packages/strkit/src/index.js:1` contains `import { add } from 'mathkit';` — a hard runtime dependency on the sibling package. The package manifest that should declare that dependency, `packages/strkit/package.json:1`, lists only `name`, `version`, and `main` — there is no `dependencies` object at all. `pnpm-workspace.yaml:1-2` confirms this is a pnpm workspace, and pnpm's default strict, isolated `node_modules` resolves imports only through declared dependencies, so this import depends on implicit hoisting behavior rather than a declared contract. That is precisely the defining case of Implicit Dependencies (weakness-types.md, type 5): code that depends on files or packages not explicitly declared or validated. The secondary ESM/CJS mismatch (no `"type": "module"` despite `export`/`import` syntax) is a real but separate contract defect; the undeclared import is the weakest boundary because it is the one that silently depends on tooling behavior and would corrupt any downstream work (tests, publishing, CI) built on the manifests.

## 6.5. Problem classification (fog type)
`primary_fog_type: architecture_fog`.

- **Not `ui_fog`**: the UI Fog Signals Registry's decision tree's first gate is "does the codebase have frontend/UI code (React/Vue/Angular/HTML/CSS)?" — this repo has none; it is two headless utility packages with no screens, flows, routing, or design system.
- **Not `product_fog`**: there is no user-need uncertainty; the two utilities (`add`, `concat`) are precisely defined functions, and no feature requirements are vague.
- **Not `docs_fog` as the primary problem**: the README is minimal but accurate; writing more documentation would not make `import { add } from 'mathkit'` resolvable or the ESM entry files loadable.
- **`architecture_fog`**: the core problem is structural — a cross-package dependency that is exercised in code but not declared in the manifest, plus an unenforced module-format contract. This is a module-boundary/coupling defect, which is the architecture_fog case, and it matches the ground-truth routing for this fixture.

## 7. Evidence
The strongest evidence is the contrast between what `strkit`'s code requires and what its manifest declares:
- `packages/strkit/src/index.js:1` — `import { add } from 'mathkit';` — the runtime dependency on the sibling package.
- `packages/strkit/package.json:1` — the manifest contains `name`, `version`, `main` and nothing else; no `dependencies` field, so `mathkit` is never declared.
- `pnpm-workspace.yaml:1-2` — `packages: - packages/*` — confirms the pnpm workspace model, under which undeclared cross-package imports are not linked in the default isolated layout.
- `packages/mathkit/src/index.js:1` and `packages/strkit/src/index.js:2` — ESM `export`/`import` syntax, while `packages/mathkit/package.json:1` and `packages/strkit/package.json:1` omit `"type": "module"` — a second, compounding contract defect at the same package boundary.
- `README.md:1-3` — the only documentation; it says nothing about the dependency relationship, module format, or how to run the packages.

Logic trace: `packages/strkit/src/index.js:1` imports `'mathkit'`, but `packages/strkit/package.json:1` declares no dependency on it, so the import's resolvability depends entirely on the package manager's hoisting behavior rather than on a declared contract — with `pnpm-workspace.yaml:1-2` establishing that the repo is a pnpm workspace whose default strict `node_modules` will not link an undeclared sibling. Because `packages/mathkit/src/index.js:1` and `packages/strkit/src/index.js:1-2` use ESM syntax while neither manifest (`packages/mathkit/package.json:1`, `packages/strkit/package.json:1`) declares `"type": "module"`, even a successfully resolved import would fail to load under Node's default CommonJS interpretation. The chain — code depends on a package, the manifest does not declare it, and the workspace tooling does not validate the link — is exactly the Implicit Dependencies weakness (weakness-types.md, type 5), and it is the boundary with the most downstream blast radius: any test suite, CI job, or publish step built on these manifests inherits the same unproven resolution. Hence the weakest boundary is Implicit Dependencies and the primary fog is architecture_fog — the module boundary between the two packages is the broken structural contract.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: packages/strkit/src/index.js
    lines: L1
    quote: "import { add } from 'mathkit';"
    supports_claim: "strkit imports mathkit at runtime, creating a cross-package dependency"
  - file: packages/strkit/package.json
    lines: L1
    quote: '{"name": "strkit", "version": "1.0.0", "main": "src/index.js"}'
    supports_claim: "strkit's manifest declares no dependencies on mathkit (no dependencies field at all)"
  - file: pnpm-workspace.yaml
    lines: L1-L2
    quote: "packages:\n  - packages/*"
    supports_claim: "The repo is a pnpm workspace; pnpm's default isolated node_modules does not link undeclared sibling imports"
  - file: packages/mathkit/src/index.js
    lines: L1
    quote: "export const add = (a, b) => a + b;"
    supports_claim: "mathkit's only export uses ESM syntax, but its package.json declares no type: module"
  - file: packages/mathkit/package.json
    lines: L1
    quote: '{"name": "mathkit", "version": "1.0.0", "main": "src/index.js"}'
    supports_claim: "mathkit's manifest omits type: module and exports; the public surface is only an implicit main entry"
  - file: README.md
    lines: L1-L3
    quote: "# monorepo\n\nTwo packages."
    supports_claim: "The README is the only documentation and says nothing about the dependency relationship or module format"
```

## 9. Why this boundary matters
If the `strkit → mathkit` dependency stays undeclared, the workspace installs cleanly but the first `import { add } from 'mathkit'` (`packages/strkit/src/index.js:1`) may fail at runtime depending on which package manager or hoisting layout is used — pnpm's default isolated `node_modules` will not resolve it, while npm/yarn hoisting may mask the same code as working, making behavior environment-dependent and untestable. The missing `"type": "module"` in both manifests (`packages/mathkit/package.json:1`, `packages/strkit/package.json:1`) guarantees a `SyntaxError` on first load even where resolution succeeds. Any downstream work compounds the damage: a test suite cannot run, CI cannot gate, publishing `strkit` standalone would ship a broken package, and the hidden `add(1, 1)` term in `concat` (`packages/strkit/src/index.js:2`) would be an undocumented contract change the moment `add`'s behavior is touched. The manifests are the contract between packages; right now they assert a boundary that the code does not honor.

## 10. Candidate next steps
1. **Declare the workspace dependency**: add `"dependencies": {"mathkit": "workspace:*"}` to `packages/strkit/package.json` and run `pnpm install`, making the existing import (`packages/strkit/src/index.js:1`) explicit, pinned, and resolvable under pnpm's strict layout.
2. **Fix the module format**: add `"type": "module"` to both `packages/mathkit/package.json` and `packages/strkit/package.json` so the ESM entry files (`packages/mathkit/src/index.js:1`, `packages/strkit/src/index.js:1-2`) load under Node.
3. **Add a root test harness**: create a root `package.json` with `pnpm -r test` and a test runner, plus unit tests for `add` and `concat` — closing the Zero Validation gap.
4. **Harden the manifests for publishing**: add `exports` and `files` to `packages/mathkit/package.json` (and `strkit` once its dependency is declared) so the public surface is explicit.
5. **Add CI and a lockfile**: commit `pnpm-lock.yaml` and a CI step running `pnpm install --frozen-lockfile && pnpm -r test` so the implicit-dependency failure surfaces deterministically.

## 11. Recommended next step
Declare the `mathkit` workspace dependency in `packages/strkit/package.json` (smallest concrete action that makes the existing import at `packages/strkit/src/index.js:1` resolvable and the manifest truthful), and pair it with `"type": "module"` in both package manifests in the same change, since the ESM syntax is already in the source and the two fixes are the same boundary.

## 12. Recommended workflow
`architecture-implementation-workflow` (id present in `skills/workflow-planner/references/workflow-registry.yaml`, line 848) — the implementation path for architecture/refactoring problems: aligns domain understanding, creates a refactoring spec for module boundaries, decomposes into issues, and implements via TDD. It matches the architecture_fog classification: the defect is a structural module-boundary contract (undeclared cross-package dependency plus module-format mismatch), not a feature, docs, or UI problem.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/monorepo
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "packages/strkit/src/index.js (line L1): imports 'mathkit', creating an undeclared cross-package dependency"
  - "packages/strkit/package.json (line L1): manifest has no dependencies field; mathkit is never declared"
  - "pnpm-workspace.yaml (lines L1-L2): pnpm workspace glob packages/*; pnpm's isolated node_modules does not link undeclared siblings"
  - "packages/mathkit/src/index.js (line L1) and packages/strkit/src/index.js (lines L1-L2): ESM syntax with no type: module in either package.json"
  - "README.md (lines L1-L3): only documentation; says nothing about the dependency relationship or module format"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Implicit Dependencies
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
For `workflow-planner`:

> Plan an `architecture-implementation-workflow` run for the `monorepo` fixture repository. Diagnosis: `primary_fog_type: architecture_fog`; weakest boundary is **Implicit Dependencies** — `packages/strkit/src/index.js:1` imports `'mathkit'` but `packages/strkit/package.json:1` declares no dependencies, so resolution depends on pnpm hoisting in a workspace defined by `pnpm-workspace.yaml:1-2`; compounding defect: both packages ship ESM syntax (`packages/mathkit/src/index.js:1`, `packages/strkit/src/index.js:1-2`) without `"type": "module"` in either manifest. Objective: make the package boundary explicit and enforceable — add `"dependencies": {"mathkit": "workspace:*"}` to `packages/strkit/package.json`, add `"type": "module"` to both package manifests, and add a root test harness (`pnpm -r test`) with unit tests for `add` and `concat`. Keep `recommended_execution_mode: guided_execution` with review gates; do not implement anything outside this scope.
