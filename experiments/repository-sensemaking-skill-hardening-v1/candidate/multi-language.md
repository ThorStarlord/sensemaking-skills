# Repository Sensemaking Brief

Target repo: `experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-language` (fixture, standalone run — no user intent artifact; GAP-8: `user_implied_fog_type: unknown`).

## 1. Repository goal

The repository presents itself as **"multi-lang", a mixed-language project** (README.md:1-3 — `# multi-lang`, `Mixed-language project.`). Read together with the Makefile (Makefile:1-5), the apparent intent is a small multi-runtime project with a Python "core" (`core/main.py`), a JavaScript "helper" (`helper/run.js`), and a shell setup script (`scripts/setup.sh`).

OBSERVED: that is the *entire* stated goal — no purpose, feature set, or user outcome is documented anywhere (README.md:1-3 is the complete documentation of the repo). OBSERVED: the implemented reality is a skeleton — every declared entry point runs but contains no behavior (`core/main.py:1` prints `'core'`; `helper/run.js:1` prints `'TODO'`). The working goal of the repo is therefore "a runnable shell of a mixed-language project"; its actual delivered value is currently nil because no component implements anything.

## 2. Current shape

Complete inventory (recursive listing, all files): `Makefile` (5 lines), `README.md` (3 lines), `core/main.py` (1 line), `helper/run.js` (1 line), `scripts/setup.sh` (2 lines). Nothing else — no manifests, no CI, no tests, no docs directory, no lockfiles, no generated artifacts.

**Runtime flow (what actually happens, not the directory layout):**

- **What starts the system**: `make` with default target `all` (Makefile:1). `all` depends on `core` only. `core` runs `python core/main.py` (Makefile:2-3). A second target `helper` runs `node helper/run.js` (Makefile:4-5) but is **not** part of `all` (Makefile:1).
- **Orchestration**: the Makefile is the only orchestrator (Makefile:1-5). There is no application-level orchestration; there is nothing to orchestrate.
- **Domain/core logic**: none. The two entry-point files contain exactly one statement each — `print('core')` (core/main.py:1) and `console.log('TODO');` (helper/run.js:1).
- **Persistence/state**: none. No files written, no database, no cache, no queue, no environment-variable reads anywhere in the repo (OBSERVED from the complete 5-file inventory).
- **External integrations**: none. No imports beyond built-in print/console; no network, no CLI argument parsing.
- **Background work**: none.
- **Output boundary**: stdout only — `print('core')` (core/main.py:1) and `console.log('TODO');` (helper/run.js:1).
- **Validation**: nowhere. No tests, no CI configuration, no schema, no `test` target (Makefile:1-5 lists only `all`, `core`, `helper`).
- **Where responsibility becomes unclear**: exactly at the entry-point → behavior hop. Each Makefile target resolves to a real file (Makefile:2-5), but nothing sits behind the interface — the "system" is two placeholder statements. `scripts/setup.sh:1-2` (`#!/bin/sh`, `echo setup`) is a third executable that is referenced by **no** Makefile target (Makefile:1-5) and **no** README line (README.md:1-3); its role is UNKNOWN from the code — INFERRED from the filename to be environment setup, but nothing invokes it.

**Dependency semantics** (each class stated explicitly):

- `python` and `node` are `used` only as command tokens inside Makefile targets (Makefile:3, Makefile:5). They are `declared` **nowhere** — no `package.json` for the JS half, no `requirements.txt`/`pyproject.toml`/`setup.py` for the Python half (OBSERVED absent in the complete inventory). Their versions and installation contract are therefore **implicit**.
- No third-party dependencies exist in any class (declared/used/runtime/test/optional/dead) — there are no manifests at all.
- `scripts/setup.sh` is a `dead`-wired script in the structural sense: it exists (scripts/setup.sh:1-2) but no execution path references it. Note the two rules: an entry point can exist without being invoked (this is the case here — `make` never mentions it), and a manifest entry is not required for a script to run; both facts are OBSERVED.

**Boundary model**: the only responsibility transition in the system is Makefile target → language runtime → stdout print. Nothing is validated at any boundary; everything is assumed.

## 3. Strong signals

- **The documentation does not overclaim.** README.md:1-3 describes only a "Mixed-language project." — no feature is advertised that does not exist, so there is no documented-surface lie to unwind.
- **The wiring that exists is correct and runnable.** Every Makefile command resolves to an existing file: `python core/main.py` (Makefile:3) → `core/main.py` exists (core/main.py:1); `node helper/run.js` (Makefile:5) → `helper/run.js` exists (helper/run.js:1). No broken paths, no missing imports.
- **The multi-language surface is real.** Python and JavaScript entry points both exist, and the interpreters invoked (`python`, `node`, Makefile:3,5) are standard, lowering environment risk.
- **Conventional, growable layout.** `core/` (core/main.py) vs `helper/` (helper/run.js) vs `scripts/` (scripts/setup.sh) gives the repo room to grow without restructuring.
- **Clean slate, no cruft.** No vendored dependencies, no generated bundles, no stale lockfiles, no duplicate sources — nothing to work around.

## 4. Missing pieces

- **Any implemented behavior.** `core/main.py:1` (`print('core')`) and `helper/run.js:1` (`console.log('TODO');`) are placeholders; the project performs no work.
- **Wiring for `scripts/setup.sh:1-2`.** No Makefile target references it (Makefile:1-5) and the README never mentions it (README.md:1-3). Either wire it into a `setup:` target or remove it.
- **`helper` in the default build.** `all: core` (Makefile:1) silently excludes the JS half of the "mixed-language project" — `make` alone never runs `helper/run.js`.
- **Manifests declaring the runtime contract.** No `package.json`, no `requirements.txt`/`pyproject.toml` (OBSERVED absent in the complete inventory) — `python`/`node` versions and the setup steps needed before running are implicit.
- **Tests and CI.** Zero test files, zero CI configuration, no `test` target (Makefile:1-5). Nothing verifies the build/runtime contract.
- **Documentation of intent.** README.md:1-3 gives no purpose, usage, architecture, or entry-point overview; it does not mention the Makefile, `core`, `helper`, or `scripts/`.

## 5. Improvement opportunities

- Add a `test` target with a smoke test asserting `core`/`helper` produce their intended output — once behavior exists to assert.
- Replace the two-line README (README.md:1-3) with a short purpose + usage + layout section.
- Add minimal manifests (`package.json` with an `engines` node field; `requirements.txt` or `pyproject.toml`) so the runtime contract is declared rather than implicit.
- Wire `scripts/setup.sh:1-2` into a `setup:` target or delete it — currently a dead file that confuses orientation.
- Decide whether `helper` belongs in `all` (Makefile:1); if the JS half is meant to be part of the system, `all` must include it.

## 6. Weakest boundary

Candidate boundaries generated first, then scored (per SKILL.md "Weakest Boundary Reasoning"):

**Candidate 1 — Entry-point → behavior hop (stubs).** Declared targets `core`/`helper` (Makefile:2-5) resolve to files whose entire implementation is placeholder text (core/main.py:1, helper/run.js:1).
- evidence_strength: strong (whole files observed; one statement each)
- severity: high (the system performs zero work)
- blast_radius: high (100% of the runtime surface)
- goal_relevance: high (the repo's entire purpose)
- downstream_blocking_effect: high (any implementation work must first decide what the system should do)
- uncertainty: low

**Candidate 2 — Implicit/unwired environment contract.** `scripts/setup.sh:1-2` referenced by nothing (Makefile:1-5, README.md:1-3); `python`/`node` declared in no manifest (Makefile:3,5); `helper` excluded from `all` (Makefile:1).
- evidence_strength: strong (absence of references OBSERVED in the complete inventory)
- severity: medium (the JS half never runs by default; setup steps unknowable)
- blast_radius: medium
- goal_relevance: high
- downstream_blocking_effect: medium
- uncertainty: low

**Candidate 3 — Absence of validation.** No tests, no CI, no `test` target (Makefile:1-5; full inventory).
- evidence_strength: strong (absence OBSERVED)
- severity: low (there is no logic yet to validate)
- blast_radius: medium
- goal_relevance: low
- downstream_blocking_effect: low
- uncertainty: low

**Candidate 4 — Documentation minimalism.** README.md:1-3 (two lines, no purpose/usage).
- evidence_strength: strong
- severity: low
- blast_radius: low
- goal_relevance: medium
- downstream_blocking_effect: low
- uncertainty: low

**Selection rule applied**: Candidates 1 and 2 are the same boundary viewed from the behavior side and the wiring side, and together they dominate on consequence, evidence strength, goal centrality, and downstream blocking. Selected boundary: the **declared runtime surface vs. what is actually wired and implemented behind it**.

```text
Boundary:
  The transition from declared entry point (Makefile:2-5) to implemented,
  wired behavior — every entry point resolves to a placeholder
  (core/main.py:1, helper/run.js:1), and the surrounding runtime contract
  (scripts/setup.sh:1-2, interpreter availability, helper's membership in
  the default build) is implicit and unenforced.

Observed contract:
  Makefile:2-5 declares `core` and `helper` as runnable targets;
  README.md:2 describes a "Mixed-language project."

Observed violation or uncertainty:
  Running the declared targets produces only the literal strings 'core' and
  'TODO' — no behavior exists behind the surface. scripts/setup.sh:1-2 is
  referenced by no Makefile target (Makefile:1-5) and no README line
  (README.md:1-3). No manifest declares the python/node runtimes (complete
  inventory: none exist). Makefile:1 `all: core` silently omits the helper
  half of the declared mixed-language system.

Evidence:
  Makefile:1-5; core/main.py:1; helper/run.js:1; scripts/setup.sh:1-2;
  README.md:1-3.

Weakness type:
  **Weakness type:** Implicit Dependencies

Logic trace:
  Makefile:2-3 declares `core` → `python core/main.py`, and Makefile:4-5
  declares `helper` → `node helper/run.js`; both target files exist, so the
  declared surface is runnable. But core/main.py:1 is `print('core')` and
  helper/run.js:1 is `console.log('TODO');` — the entire implementation
  behind the declared interface is placeholder text, i.e. the wiring from
  declared entry point to real behavior is absent. Independently,
  scripts/setup.sh:1-2 exists and is referenced by nothing in Makefile:1-5
  or README.md:1-3 (an unwired module), and the interpreters named in
  Makefile:3 and Makefile:5 are declared in no manifest (no package.json,
  requirements.txt, or pyproject.toml anywhere in the complete inventory).
  Under the GAP-6 taxonomy mapping, an unwired/never-referenced module maps
  to Implicit Dependencies (undocumented wiring), and packaging-metadata
  gaps with an undeclared environment map to Implicit Dependencies
  (undeclared environment) by evidence; stub implementations are
  wiring-level incompleteness (a declared interface with nothing behind it)
  and are directed to Implicit Dependencies rather than Ghost Features,
  since README.md:1-3 documents no feature as live functionality. All three
  observed defect classes therefore converge on the same weakness: the
  runtime contract between the declared entry points and any real behavior
  or environment is implicit and unenforced.

Failure consequence:
  Anyone building on this repo cannot tell what the system is supposed to
  do, the JS half of the project silently never runs under the default
  `make`, the setup steps are unknowable, and no automated check exists to
  surface any of it. The first real implementation attempt will have to
  reverse-engineer the intended contract from a two-line README.

Confidence:
  high — the defect is directly observable in one-statement files and a
  5-line Makefile. What would raise it further: executing `make all`,
  `make helper`, and the setup script to confirm runtime behavior
  (execution was not performed; static evidence is conclusive for
  single-statement entry points).

Alternatives considered:
  - Ghost Features — rejected: README.md:1-3 documents no feature surface,
    and GAP-6 restricts Ghost Features to documented functionality with no
    reachable implementation; the README's only claim ("Mixed-language
    project.", README.md:2) is actually true of the file inventory.
  - Zero Validation — runner-up: no tests/CI/test target exist
    (Makefile:1-5, full inventory), but with zero implemented logic the
    validation gap is a symptom of the missing implementation rather than
    the root boundary; the root is that declared entry points have nothing
    wired behind them.
  - Vocabulary Drift — rejected: the README's term "Mixed-language project."
    (README.md:2) matches the Python+JS reality (core/main.py:1,
    helper/run.js:1); no term is misused.
  - Orphaned Examples — rejected: no examples exist in the repo.
```

## 6.5. Problem classification (fog type)

**Primary: `architecture_fog`.** Classification is evidence-based, not vibe-based:

- **Frontend tie-break does not apply.** The UI Fog Signals Registry decision tree terminates at the first question: the repository has no frontend/UI code — `helper/run.js:1` is a Node CLI script (`console.log('TODO');`), not browser UI; there is no HTML, CSS, JSX, or component code anywhere in the complete inventory. No Tier-1 or Tier-2 UI signal can be cited. → Not `ui_fog`.
- **Entry-point-stub rule applies directly.** The system runs (Makefile:2-5 targets resolve and execute) but is skeletal — a stubbed runtime entry point (`helper/run.js:1`, `console.log('TODO');`; `core/main.py:1`, `print('core')`) within an otherwise-running Makefile-driven system is a structural defect → `architecture_fog` (SKILL.md "Entry-point stubs (structural qualification)"). The promised surface (the Makefile targets) *has* an implementation — a placeholder — so this is an incomplete system (architecture), not a feature with no implementation anywhere (product).
- **Not `product_fog`**: README.md:1-3 promises no deliverable feature, so no product contract is broken.
- **Not `docs_fog` as primary**: the README is minimal but does not misdescribe the code — "Mixed-language project." (README.md:2) matches the inventory. Minimal documentation is a *contributing secondary* factor (docs_fog), recorded here for completeness; it does not drive routing.
- `diagnosis_conflict: false` — no user intent exists to conflict with (`user_implied_fog_type: unknown`, GAP-8 no-user-intent run).

## 7. Evidence

File-level evidence supporting the diagnosis (all files actually opened):

- `README.md:1-3` — the complete documentation: `# multi-lang` and `Mixed-language project.`; no features, usage, or setup documented. Establishes there is no documented feature surface (rules out Ghost Features) and that documentation is minimal (secondary docs_fog).
- `Makefile:1` — `all: core`: the default build path excludes the `helper` target declared at Makefile:4-5.
- `Makefile:2-3` — `core:` → `python core/main.py`: declares entry point 1; `python` appears only as a command token, declared in no manifest.
- `Makefile:4-5` — `helper:` → `node helper/run.js`: declares entry point 2; `node` likewise undeclared anywhere.
- `core/main.py:1` — `print('core')`: the entire Python implementation is a placeholder.
- `helper/run.js:1` — `console.log('TODO');`: the entire JavaScript implementation is a placeholder.
- `scripts/setup.sh:1-2` — `#!/bin/sh`, `echo setup`: an executable script referenced by no Makefile target (Makefile:1-5) and no README line (README.md:1-3) — an unwired module (Implicit Dependencies, undocumented wiring).
- Absence evidence (OBSERVED via complete recursive inventory): no `package.json`, `requirements.txt`, `pyproject.toml`, `setup.py`, no test files, no CI configuration, no docs directory. Absence of manifests makes the `python`/`node` runtime contract implicit; absence of tests/CI means nothing validates the build/runtime contract.

**Logic trace:** The Makefile declares two runnable entry points (Makefile:2-3, Makefile:4-5) and the README presents the repo as a "Mixed-language project." (README.md:2). Opening the two target files shows each contains a single placeholder statement (core/main.py:1, helper/run.js:1) — the declared surface is wired only to placeholder text, not to behavior. Opening the inventory shows a third executable, scripts/setup.sh:1-2, wired to nothing (no reference in Makefile:1-5 or README.md:1-3), and no manifest declaring the interpreters invoked at Makefile:3 and Makefile:5. The chain — declared entry points → placeholder implementations → unwired setup script → undeclared runtimes — establishes that the weakest boundary is the runtime contract between the declared surface and real, wired behavior, which is implicit and unenforced (Implicit Dependencies). Because the entry points run but form an incomplete system, the defect is structural: `architecture_fog`.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L2-L3
    quote: "Mixed-language project."
    supports_claim: "The only documentation claim; no feature surface is documented, so no product contract or Ghost Feature exists."
  - file: Makefile
    lines: L1
    quote: "all: core"
    supports_claim: "Default target silently excludes the helper target; the mixed-language system is only partially wired into the default build."
  - file: Makefile
    lines: L2-L3
    quote: "python core/main.py"
    supports_claim: "Entry point 1: python appears only as a command token, declared in no manifest (implicit runtime dependency)."
  - file: Makefile
    lines: L4-L5
    quote: "node helper/run.js"
    supports_claim: "Entry point 2: node likewise undeclared anywhere; helper is a declared but skeletal entry point."
  - file: core/main.py
    lines: L1
    quote: "print('core')"
    supports_claim: "The entire Python implementation is a placeholder — a stubbed runtime entry point."
  - file: helper/run.js
    lines: L1
    quote: "console.log('TODO');"
    supports_claim: "The entire JavaScript implementation is a placeholder — a stubbed runtime entry point; 'TODO' marks it unimplemented."
  - file: scripts/setup.sh
    lines: L1-L2
    quote: "echo setup"
    supports_claim: "An executable script referenced by no Makefile target (Makefile:1-5) and no README line (README.md:1-3): an unwired module (Implicit Dependencies)."
```

## 9. Why this boundary matters

If this boundary stays weak, the repo cannot be built upon safely: a developer or agent who runs `make` (Makefile:1) sees a green run that delivers no behavior, the JS half never executes under the default path, the setup steps are unknowable (scripts/setup.sh:1-2 is invisible to the Makefile), and the undeclared `python`/`node` contract (Makefile:3,5) will surface as version/install surprises at the worst moment. The first real implementation will have to reverse-engineer intent from a two-line README (README.md:1-3), and nothing — no test, no CI, no schema — will catch a regression back to the current stub state. In short: the system's only honest description today is "declared but not delivered," and nothing in the repo checks that description.

## 10. Candidate next steps

1. **Decide and document the intended behavior contract**: replace README.md:1-3 with a short statement of what `core` and `helper` should do and how they relate (this unblocks every other step).
2. **Implement or remove the placeholders**: replace `print('core')` (core/main.py:1) and `console.log('TODO');` (helper/run.js:1) with first real behaviors, or explicitly delete the `helper` target (Makefile:4-5) if the JS half is not wanted.
3. **Wire or delete `scripts/setup.sh`**: add a `setup:` target to Makefile:1-5 that invokes it, or remove the file (currently dead).
4. **Declare the runtime contract**: add `package.json` (with `engines`) for helper/run.js and `requirements.txt`/`pyproject.toml` for core/main.py so `python`/`node` are declared dependencies, not implicit ones.
5. **Add validation**: introduce a `test` target and a smoke test asserting the entry points' behavior, plus CI if the repo becomes a real project.

## 11. Recommended next step

Step 1 — **decide and document the intended behavior contract in README.md** (replacing README.md:1-3's two lines). It is the smallest action with the highest leverage: it converts the implicit runtime contract (the root of the Implicit Dependencies weakness) into an explicit one, and every other candidate step (implementing core/main.py:1, wiring helper into Makefile:1, wiring scripts/setup.sh:1-2, writing manifests and tests) depends on knowing what the system is supposed to do. Until that decision exists, any implementation is guesswork.

## 12. Recommended workflow

**`architecture-implementation-workflow`** (from the canonical `skills/workflow-planner/references/workflow-registry.yaml`; the only authoritative registry — no registry inside the target repo was used, and none exists there). **Execution mode: `guided_execution`** — one of that workflow's two `allowed_execution_modes` (`guided_execution`, `autonomous_execution`); recommending it is a diagnostic handoff, not execution.

Rationale: `architecture_fog` (stubbed entry points, implicit wiring) routes to the spec-driven refactoring workflow per the SKILL.md fog classification. The workflow's docs-aligner → to-prd → to-issues → triage → tdd chain fits: docs-aligner will produce CONTEXT.md capturing the behavior contract that README.md:1-3 currently lacks, to-prd will turn it into a specification, and tdd will implement the entry points behind it.

Why not the closest alternatives:
- `implementation-workflow` (generic implementation) — valid, but `architecture-implementation-workflow` is the precise registry fit for structure/wiring problems, which is what the entry-point-stub defect is.
- `ui-diagnostic-workflow` / `ui-implementation-workflow` — rejected: no frontend surface exists (helper/run.js:1 is a Node script; no HTML/CSS/JSX in the inventory), so no UI signal can be cited.
- `docs-implementation-workflow` — rejected as the primary route: the README (README.md:1-3) is minimal but accurate; the documentation gap is secondary to the structural one.
- `product-implementation-workflow` — rejected: no product contract is documented (README.md:1-3 promises no feature), so there is nothing to research.
- Escalation — not needed: evidence for `architecture_fog` is unambiguous (one-statement stubs), so `escalation_recommended: false`.

Preconditions before the workflow can run: none blocking; the owner must be ready to make the behavior-contract decision (recommended next step) during the docs-aligner step, since the repo currently has no intent artifact.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-language
source_intent_ref: null  # no-user-intent fixture run (GAP-8); no 00-user-intent.md exists for this repo
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml (canonical registry; authoritative for routing)
evidence:
  - "README.md (L1-L3): only documentation; documents no features, usage, or setup — no documented feature surface exists"
  - "Makefile (L1): 'all: core' — default build silently omits the helper target"
  - "Makefile (L2-L5): declares entry points 'core' (python core/main.py) and 'helper' (node helper/run.js)"
  - "core/main.py (L1): 'print(''core'')' — entire Python implementation is a placeholder stub"
  - "helper/run.js (L1): 'console.log(''TODO'');' — entire JavaScript implementation is a placeholder stub"
  - "scripts/setup.sh (L1-L2): unwired script, referenced by no Makefile target (Makefile:1-5) or README line (README.md:1-3)"
  - "Absence evidence (complete inventory): no package.json/requirements.txt/pyproject.toml, no tests, no CI — runtimes and validation contract are implicit"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Implicit Dependencies
weakest_boundary_evidence: "Declared entry points (Makefile:2-5) resolve to placeholder implementations (core/main.py:1, helper/run.js:1); scripts/setup.sh:1-2 is wired nowhere; python/node runtimes declared in no manifest"
weakness_type: Implicit Dependencies
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-11T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

> The repository `experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-language` is a skeleton mixed-language project diagnosed with `architecture_fog` and weakest boundary **Implicit Dependencies** (see the sensemaking brief `multi-language.md`). It declares two entry points — `core` → `python core/main.py` and `helper` → `node helper/run.js` (Makefile:2-5) — whose implementations are placeholders (`print('core')` at core/main.py:1; `console.log('TODO');` at helper/run.js:1), a setup script wired nowhere (scripts/setup.sh:1-2), and no manifests declaring the `python`/`node` runtimes; the default target `all: core` (Makefile:1) omits the JS half, and no tests or CI exist. Run the `architecture-implementation-workflow` in `guided_execution` mode: start with docs-aligner to capture the intended behavior contract in CONTEXT.md (the README at README.md:1-3 does not state one), then spec, decompose into issues, and implement the entry points behind the declared targets — wiring or removing `scripts/setup.sh`, adding `helper` to `all` or explicitly dropping the target, and adding minimal manifests plus a smoke test. Do not begin implementation until the behavior contract decision is made.
