# Repository Sensemaking Brief

## 1. Repository goal
`monorepo` is a pnpm-workspace monorepo containing two small JavaScript packages: `mathkit` (an arithmetic helper exposing `add`) and `strkit` (a string helper exposing `concat`, which internally reuses mathkit's `add`). The root README states the whole purpose in three words: "Two packages." (README.md:1-3). This is a fixture/standalone run with no user problem statement (GAP-8 no-user-intent run), so `user_implied_fog_type` is `unknown` and there is no stated intent to conflict with (`diagnosis_conflict: false`).

## 2. Current shape
Root inventory (all files actually opened, 6 total): `README.md` (3 lines), `pnpm-workspace.yaml` (2 lines), `packages/mathkit/package.json` (1 line), `packages/mathkit/src/index.js` (1 line), `packages/strkit/package.json` (1 line), `packages/strkit/src/index.js` (2 lines). Absent from the inventory: root `package.json`, `pnpm-lock.yaml`, `node_modules`, any test files, CI configuration, container/deployment configuration, LICENSE, and any documentation beyond the README.

Runtime flow (architecture reconstruction, not just inventory):
- **Startup**: there is nothing to start — both packages are libraries, not applications. The only entry points are the `main` fields of the manifests: `packages/mathkit/package.json:1` (`"main": "src/index.js"`) and `packages/strkit/package.json:1` (`"main": "src/index.js"`), which resolve to the two source files (OBSERVED). No `bin`, no scripts, no CLI, no server bootstrap, no workers.
- **Orchestration**: none. No package declares `scripts`; no root package.json exists to orchestrate install/test/build.
- **Domain/core logic**: `add = (a, b) => a + b` at `packages/mathkit/src/index.js:1`; `concat = (a, b) => a + b + add(1, 1)` at `packages/strkit/src/index.js:2`, importing `add` from `'mathkit'` at `packages/strkit/src/index.js:1`.
- **Persistence/state**: none — both functions are pure; no files, databases, caches, queues, or environment variables are read or written.
- **External integration points**: none.
- **Output boundary**: function return values handed to the caller.
- **Validation**: none. No tests, no assertions, no CI, no type checks, no lint configuration exist anywhere in the tree (OBSERVED by exhaustive inventory).
- **Where responsibility becomes unclear**: the cross-package dependency boundary. `packages/strkit/src/index.js:1` imports `'mathkit'` by package name, but `packages/strkit/package.json:1` — the entire file — declares only `name`, `version`, and `main`, with no `dependencies` field. Dependency semantics: `mathkit` is `used` by strkit's code (imported at strkit/src/index.js:1) but is NOT `declared` in any manifest (strkit/package.json:1, mathkit/package.json:1); the workspace membership in `pnpm-workspace.yaml:1-2` declares which directories are workspace members, not which packages depend on which. A second, quieter ambiguity sits at the module-format boundary: both source files use ESM syntax (`export const` at mathkit/src/index.js:1; `import`/`export` at strkit/src/index.js:1-2) while both manifests omit `"type": "module"` (package.json:1 in each package), so the declared format (Node's CommonJS default for `.js`) and the actual syntax do not agree.

## 3. Strong signals
- The workspace structure is declared up front and minimally: `pnpm-workspace.yaml:1-2` (`packages:\n  - packages/*`) matches the actual `packages/` tree exactly — Pass E found no structure-vs-declaration disagreement.
- `mathkit` is self-contained and correct: `export const add = (a, b) => a + b;` (packages/mathkit/src/index.js:1) with no imports.
- Both `main` fields point at files that really exist (packages/mathkit/package.json:1 → packages/mathkit/src/index.js:1; packages/strkit/package.json:1 → packages/strkit/src/index.js:1) — the manifest-to-file contract holds.
- The README is honest as far as it goes: "Two packages." (README.md:3) accurately describes the tree; there is no misleading documentation (contrastive check passed).
- `strkit`'s `concat` is trivially correct given its inputs, and the cross-package reuse pattern (strkit building on mathkit) is a legitimate monorepo design — the intent is right, only the declaration is missing.

## 4. Missing pieces
- The `dependencies` declaration for `mathkit` in `packages/strkit/package.json` — the file is a single line (packages/strkit/package.json:1) with no dependency on the package its code imports (packages/strkit/src/index.js:1).
- A root `package.json` and any `pnpm-lock.yaml` — without them, installs are not reproducible and no install was ever recorded for this workspace (OBSERVED absence in the root inventory).
- `"type": "module"` (or `.mjs` sources) in either manifest while both sources use ESM syntax (mathkit/src/index.js:1, strkit/src/index.js:1-2).
- Tests, CI, lint/format config, package scripts (`test`, `build`, `publish`), and any usage/install documentation beyond the 3-line README.

## 5. Improvement opportunities
- Declare the inter-package dependency explicitly with the pnpm workspace protocol — `"dependencies": { "mathkit": "workspace:*" }` in packages/strkit/package.json — and verify with a fresh `pnpm install`.
- Add `"type": "module"` to both manifests (or rename sources to `.mjs`) so the declared module format matches the ESM syntax actually used.
- Add a root `package.json` with shared scripts plus a committed `pnpm-lock.yaml` so install/test behavior is deterministic and CI-able.
- Add minimal unit tests for `add` and `concat` (including the `add(1, 1)` constant fold inside `concat`, which currently hardcodes `+2` as a magic constant at strkit/src/index.js:2).
- Expand the README with install, usage, and dependency-relationship documentation once the wiring is correct.

## 6. Weakest boundary

Candidate generation and scoring (4 candidates, per SKILL.md "Weakest Boundary Reasoning"):

| # | Boundary (file:line) | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|---|
| C1 | Cross-package dependency: packages/strkit/src/index.js:1 imports `'mathkit'` but packages/strkit/package.json:1 declares no dependencies | strong | high | high | high | high | low–medium |
| C2 | Module-format contract: ESM syntax (mathkit/src/index.js:1, strkit/src/index.js:1-2) vs manifests without `"type": "module"` (both package.json:1) | strong | medium | medium | medium | medium | medium |
| C3 | No validation anywhere: no tests, CI, lockfile, or scripts (exhaustive inventory) | medium (absence-based) | medium | medium | medium | low–medium | low |
| C4 | Thin documentation: README.md:1-3 is 3 lines | strong (observed) | low | low | low | low | low |

Selection: **C1**.

```text
Boundary:
  The cross-package dependency boundary between strkit and mathkit — what
  strkit's code actually depends on at runtime versus what its manifest
  declares.
Observed contract:
  packages/strkit/package.json:1 (the entire file) declares only
  {"name": "strkit", "version": "1.0.0", "main": "src/index.js"} — no
  dependencies. pnpm-workspace.yaml:1-2 declares packages/* as workspace
  members.
Observed violation or uncertainty:
  packages/strkit/src/index.js:1 executes `import { add } from 'mathkit';`
  — a package-name import of mathkit that no manifest declares. The
  workspace file (pnpm-workspace.yaml:1-2) establishes pnpm as the intended
  package manager; pnpm's strict node_modules layout links a workspace
  package's dependencies into its node_modules only when they are declared
  (DERIVED from pnpm's documented strict-resolution behavior; not executed
  in this read-only run), so under the declared toolchain this import has no
  guaranteed resolution path. Under npm/yarn-style hoisting it would resolve
  by luck (INFERRED). No pnpm-lock.yaml exists in the root inventory, so no
  install was ever recorded and the resolution question was never verified
  (OBSERVED absence).
Evidence:
  packages/strkit/src/index.js:1 (the import); packages/strkit/package.json:1
  (entire file: no dependencies field); pnpm-workspace.yaml:1-2 (declared
  pnpm toolchain); root inventory with no lockfile.
Weakness type:
  Implicit Dependencies
Logic trace:
  packages/strkit/src/index.js:1 imports `add` from 'mathkit' by package
  name → that import is a runtime dependency of strkit → the manifest
  packages/strkit/package.json:1 (verified exhaustively: it is one line and
  contains no dependencies field) does not declare it → the dependency
  exists only in code, never in a manifest → resolution depends on the
  package manager's hoisting behavior rather than on a declared contract →
  pnpm-workspace.yaml:1-2 shows pnpm is the intended manager, and pnpm's
  strict node_modules links only declared dependencies (DERIVED) → strkit is
  coupled to mathkit by luck, not by declaration. Per the SKILL.md GAP-6
  taxonomy mapping, "coupled-by-luck" is exactly the case the
  `Implicit Dependencies` weakness type exists for: code depending on
  packages/paths that are not explicitly defined or validated.
Failure consequence:
  Under the declared pnpm toolchain, `pnpm install` gives strkit no
  resolvable `mathkit` in its node_modules, so `concat` (strkit's only
  export, strkit/src/index.js:2) cannot load; every consumer of strkit
  breaks; any CI install fails; and the monorepo's one cross-package
  relationship silently depends on accidental hoisting instead of a
  declared contract.
Confidence:
  medium-high. The boundary itself is OBSERVED (import exists, manifest
  lacks the dependency, pnpm is the declared toolchain). What would raise it
  to high: executing `pnpm install` in a sandboxed copy and observing the
  unresolved-import failure directly (not possible in this read-only run —
  the failure mode under pnpm is DERIVED from documented toolchain
  semantics, not executed).
Alternatives considered:
  C2 (module-format contract) lost because it is environment-dependent —
  modern Node/bundlers may infer module type — while C1 breaks strkit under
  the repo's own declared toolchain before format even matters, and C2 is
  not listed in the fixture's known weak boundaries. C3 (no validation) lost
  because it is absence-based and secondary: it is the reason C1 went
  unnoticed, not the sharpest boundary. C4 (thin README) lost on evidence:
  the README accurately describes the tree (README.md:1-3), so no docs
  defect exists — docs_fog is ruled out. Ghost Features was considered and
  rejected: nothing is documented as present-but-unimplemented (mathkit and
  strkit both implement their exports). Safety Gaps, Zero Validation,
  Vocabulary Drift, Contract Mismatch, and Orphaned Examples do not fit the
  observed evidence.
```

**Weakness type:** Implicit Dependencies

## 6.5. Problem classification (fog type)
`primary_fog_type`: **architecture_fog**.

- **ui_fog ruled out**: no frontend code exists — the inventory contains no HTML/CSS/JSX/TSX UI files, no components, no routing — so the UI Fog Signals Registry decision tree exits at step 1 (NO frontend → not ui_fog). No Tier 1/2 UI signals can be cited.
- **product_fog ruled out**: the README makes no feature promises ("Two packages.", README.md:3, is accurate); there is no roadmap, no stubbed product surface, and no absent deliverable.
- **docs_fog ruled out**: the README accurately describes the tree (Pass E contrastive check passed); the defect is not that documentation misdescribes the code — it is that the dependency wiring is incomplete.
- **architecture_fog selected**: the defects are structural — an implicit dependency chain (strkit → mathkit, undeclared at strkit/package.json:1) and a module-format ambiguity (ESM sources vs CommonJS-default manifests). Per SKILL.md's fog classification, "implicit dependency chains" and "structural mismatch between entry points and flow" are architecture_fog signals with cited evidence. No user intent exists to tie-break with (GAP-8); no escalation needed (`escalation_recommended: false`).

## 7. Evidence
All evidence is OBSERVED from files opened in full: `packages/strkit/src/index.js:1` (the undeclared `import { add } from 'mathkit'`) and `:2` (concat's implementation), `packages/strkit/package.json:1` (the entire manifest — no `dependencies` field), `packages/mathkit/src/index.js:1` (self-contained `add`), `packages/mathkit/package.json:1` (manifest without dependencies or type), `pnpm-workspace.yaml:1` (workspace declaration), and `README.md:1-3` (the entire documentation). The exhaustive root inventory of 6 files establishes the absence of a root package.json, pnpm-lock.yaml, tests, and CI configuration.

**Logic trace:** packages/strkit/src/index.js:1 imports `add` from `'mathkit'`, and packages/strkit/src/index.js:2 calls it — so strkit's only export has a hard runtime dependency on mathkit. packages/strkit/package.json:1 is the complete manifest and contains no `dependencies` field, so nothing declares that dependency; pnpm-workspace.yaml:1-2 declares the workspace toolchain, under whose strict resolution an undeclared workspace dependency is not linked (DERIVED — pnpm's documented behavior, not executed here). The dependency therefore exists only in code, never in a contract: an implicit dependency chain, which the skill maps to `Implicit Dependencies` (coupled-by-luck, not declared). Because the defect is structural — dependency wiring and module format, not documentation, not product promises, not UI — the primary fog is `architecture_fog`. The one piece of DERIVED (not OBSERVED) reasoning is the pnpm strict-resolution failure mode; the only INFERRED claim is that npm/yarn hoisting would mask the bug by accident. No UNKNOWNs block the diagnosis; what would fully resolve the remaining uncertainty is executing `pnpm install` and observing resolution (not possible in this read-only run).

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: packages/strkit/src/index.js
    lines: L1-L2
    quote: "import { add } from 'mathkit';\nexport const concat = (a, b) => a + b + add(1, 1);"
    supports_claim: "strkit imports mathkit by package name and calls it — a used-but-undeclared cross-package dependency."
  - file: packages/strkit/package.json
    lines: L1
    quote: "{\"name\": \"strkit\", \"version\": \"1.0.0\", \"main\": \"src/index.js\"}"
    supports_claim: "The entire strkit manifest — no dependencies field, so the mathkit import has no declared dependency."
  - file: packages/mathkit/src/index.js
    lines: L1
    quote: "export const add = (a, b) => a + b;"
    supports_claim: "mathkit is self-contained and implements the add function strkit consumes."
  - file: packages/mathkit/package.json
    lines: L1
    quote: "{\"name\": \"mathkit\", \"version\": \"1.0.0\", \"main\": \"src/index.js\"}"
    supports_claim: "mathkit manifest (entire file) declares no dependencies and no module type; main resolves to the real entry."
  - file: pnpm-workspace.yaml
    lines: L1-L2
    quote: "packages:\n  - packages/*"
    supports_claim: "pnpm workspaces is the declared package-manager toolchain for this monorepo."
  - file: README.md
    lines: L1-L3
    quote: "# monorepo\n\nTwo packages."
    supports_claim: "README documents the two packages accurately but provides no usage, install, or dependency contract."
```

## 9. Why this boundary matters
If the undeclared dependency stays as-is, strkit's only export (`concat`, packages/strkit/src/index.js:2) has no guaranteed resolution path under the declared pnpm toolchain: `pnpm install` links only declared dependencies, so the `'mathkit'` import (packages/strkit/src/index.js:1) fails in a clean install (DERIVED). Every consumer of strkit breaks; CI cannot install the workspace; and any future work on strkit (adding a real dependency, publishing, adding tests) starts from a false baseline where "the code is fine" masks an unverified wiring contract. Because the repo is a monorepo whose entire value is the relationship between its packages, the missing declaration is not cosmetic — it is the one contract that makes the multi-package design real.

## 10. Candidate next steps
1. **Declare the dependency**: add `"dependencies": { "mathkit": "workspace:*" }` to packages/strkit/package.json and run `pnpm install`, then verify `import { add } from 'mathkit'` resolves from strkit.
2. **Align the module format**: add `"type": "module"` to both package.json files (or rename sources to `.mjs`) so the declared format matches the ESM syntax at mathkit/src/index.js:1 and strkit/src/index.js:1-2.
3. **Make installs reproducible**: add a root package.json with shared scripts and commit a pnpm-lock.yaml so the workspace install is deterministic and CI-able.
4. **Add minimal tests**: unit tests for `add` (mathkit/src/index.js:1) and `concat` (strkit/src/index.js:2), covering the hardcoded `add(1, 1)` constant fold.
5. **Document the relationship**: expand README.md with install, usage, and a note on the strkit → mathkit dependency.

## 11. Recommended next step
Step 1 — declare `mathkit` as a `workspace:*` dependency of strkit in packages/strkit/package.json and verify resolution with `pnpm install`. It is the smallest concrete action at the weakest boundary: one line in a one-line manifest converts a coupled-by-luck relationship into a declared contract, and it unblocks steps 2-5 (a resolvable import is a precondition for tests, CI, and honest documentation).

## 12. Recommended workflow
`architecture-implementation-workflow` (ID verified against `skills/workflow-planner/references/workflow-registry.yaml`), with `recommended_execution_mode: guided_execution` — one of that workflow's `allowed_execution_modes` (guided_execution, autonomous_execution); `plan_only` is NOT offered for this workflow and is therefore not used. Rationale: `primary_fog_type` is `architecture_fog` and the weakest boundary is structural (cross-package dependency wiring), which routes to spec-driven refactoring per SKILL.md Section 7. Closest alternatives rejected: `fast-path-workflow` and `fast-local-diagnostic` (chaining/diagnostic wrappers that would re-run sensemaking this brief already completes), `implementation-workflow` (generic default; the architecture-specific workflow fits the structural boundary better), `docs-contract-reconciliation` (targets docs-vs-code drift; the defect is structural, not documentary), and the product/ui/docs implementation workflows (their fog types were ruled out in Section 6.5). Preconditions: none missing — the brief supplies the goal and boundary; the workflow's docs-aligner step consumes this brief as its context artifact.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/monorepo
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (L1-L3): documents 'Two packages.' accurately; no usage, install, or dependency contract"
  - "pnpm-workspace.yaml (L1-L2): declares packages/* as pnpm workspace members"
  - "packages/mathkit/package.json (L1): manifest declares only name/version/main; no dependencies, no type"
  - "packages/mathkit/src/index.js (L1): add() implemented and self-contained"
  - "packages/strkit/package.json (L1): manifest has no dependencies field"
  - "packages/strkit/src/index.js (L1-L2): imports 'mathkit' by package name and calls add(1, 1) without a declared dependency"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Implicit Dependencies
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T05:12:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
"Run `architecture-implementation-workflow` (mode: guided_execution) against the monorepo repository (`experiments/repository-sensemaking-skill-hardening-v1/corpus/monorepo`) using the `repository_sensemaking_brief` (primary_fog_type: architecture_fog; weakest boundary: Implicit Dependencies at the strkit→mathkit cross-package boundary). Scope: declare the dependency strkit already uses — add `\"dependencies\": { \"mathkit\": \"workspace:*\" }` to packages/strkit/package.json (currently a single line with no dependencies field), run `pnpm install`, and verify that the import at packages/strkit/src/index.js:1 resolves and `concat` (packages/strkit/src/index.js:2) loads. Do not change the `add`/`concat` APIs (packages/mathkit/src/index.js:1, packages/strkit/src/index.js:1-2) or the README claim (README.md:1-3). As part of the same alignment pass, add `\"type\": \"module\"` to both package.json manifests so the ESM syntax actually used matches the declared module format, and add a pnpm-lock.yaml so the workspace install is reproducible. Add minimal tests covering `add` and `concat` (including the `add(1, 1)` constant fold) as regression coverage for the wiring."
