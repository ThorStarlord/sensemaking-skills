# Repository Sensemaking Brief

## 1. Repository goal

`multi-lang` is a minimal, deliberately sparse "Mixed-language project." (README.md:3). Its apparent purpose is to seed or demonstrate a repository that spans several languages: a Python entry point (`core`, Makefile:3), a JavaScript entry point (`helper`, Makefile:5), a shell setup script (scripts/setup.sh:1-2), and a Makefile that orchestrates them (Makefile:1-5). The README makes no feature promises beyond the language-mix statement, and no user problem statement or intent artifact exists for this run (fixture/standalone invocation, GAP-8): `user_implied_fog_type` is `unknown` and `diagnosis_conflict` is `false` — there is no stated intent to conflict with.

## 2. Current shape

Root inventory (all files actually opened, 5 total): `README.md` (3 lines), `Makefile` (5 lines), `core/main.py` (1 line), `helper/run.js` (1 line), `scripts/setup.sh` (2 content lines + trailing blank). Absent from the inventory: any manifest (`package.json`, `requirements.txt`, `pyproject.toml`), CI configuration, tests, schemas, and any documentation beyond the README one-liner.

**Runtime flow (architecture reconstruction, not inventory):**

- **Startup / what runs first**: the Makefile is the only launcher. `make all` (Makefile:1) resolves to the `core` target (Makefile:2) and runs `python core/main.py` (Makefile:3), which prints `core` (core/main.py:1). `make helper` (Makefile:4-5) runs `node helper/run.js`, which logs `TODO` (helper/run.js:1). `scripts/setup.sh` is never invoked by any target.
- **Orchestration**: the Makefile is the entire control layer — two flat targets, no chaining beyond `all: core` (Makefile:1-2); `helper` is deliberately not part of the default flow.
- **Domain/core logic**: none. Each entry point is a single statement (core/main.py:1; helper/run.js:1).
- **Persistence/state**: none. No files are written, no database/cache/queue exists, no environment variables are read.
- **External integration points**: none. The only external systems are the language runtimes themselves: `python` and `node` are exercised on the Makefile execution paths (Makefile:3, Makefile:5) and `/bin/sh` is declared by the shebang (scripts/setup.sh:1) — all *implicit* runtime dependencies, because no manifest exists to declare them.
- **Background work**: none.
- **Output boundary**: stdout only (print/console.log/echo).
- **Validation**: none anywhere — no tests, no CI, no input validation, no error boundaries (OBSERVED absence across the complete tree inventory).
- **Where responsibility becomes unclear**: the `helper` boundary (Makefile:4-5 → helper/run.js:1). The Makefile presents it as a real, runnable entry point symmetric to `core`; running it succeeds (exit 0) while delivering no functionality. Nothing in the repository distinguishes a declared-but-stubbed surface from an implemented one.

**Dependency semantics** (classified per SKILL.md, never conflated): `python`, `node`, and `/bin/sh` are `runtime` dependencies on proven execution paths (Makefile:3, Makefile:5, scripts/setup.sh:1) but are never `declared` in any manifest — the repo has no manifest to declare them in. There are no `test`, `optional`, or `dead` dependencies to classify; there is also no import graph, so "import exists ≠ runtime execution path proven" has no application here beyond noting that `helper/run.js` is executed only when a user explicitly runs `make helper` (Makefile:4-5), never by the default flow (Makefile:1-2).

**State model**: no state boundaries exist (no files, DB, cache, global state, queues, env, remote systems).

**Boundary model**: the only transition is CLI/Make → command (`python core/main.py` Makefile:3; `node helper/run.js` Makefile:5). Nothing is validated at either boundary; everything is assumed (tool availability, exit codes).

## 3. Strong signals

- The Makefile cleanly separates the two entry points, one target per language, with explicit commands (Makefile:2-5) — a clear, minimal structure with no coupling between the Python and JS sides.
- Each declared command is genuinely runnable as declared: `python core/main.py` produces output (core/main.py:1) and `node helper/run.js` executes without error (helper/run.js:1). Configuration (Makefile) matches the declared commands — no config-vs-code contradiction (evidence rule: configuration outranks prose for configured behavior).
- The README's only claim is accurate: the tree really is mixed-language — Python (core/main.py:1), JavaScript (helper/run.js:1), shell (scripts/setup.sh:1), Make (Makefile:1-5). No vocabulary drift between README.md:3 and the directory structure.
- The default path (`make all` → `core`) is complete and honest: it does exactly what it says.

## 4. Missing pieces

- **No specification of either entry point's intended behavior.** README.md:1-3 is the entire documentation; there is no `/docs`, no ADR, no comment explaining what `core` or `helper` is *for*.
- **The JavaScript entry point has no implementation** — helper/run.js:1 is only `console.log('TODO');`, while Makefile:4-5 declares it as a real target.
- **scripts/setup.sh:1-2 is unwired** — referenced by no Makefile target and no README text; its purpose and its relationship to the two entry points are undefined.
- **No manifests** (`package.json`, `requirements.txt`, `pyproject.toml`), so the toolchain (`python`, `node`) is an implicit, unvalidated dependency.
- **No tests, no CI, no validation of any kind** (OBSERVED absence across the whole tree).
- **`helper` is excluded from the default flow** (`all: core`, Makefile:1-2), so the stub is never even exercised by the main path.

## 5. Improvement opportunities

- Add a `package.json` (declares the `node` runtime and a `helper` script) and/or `requirements.txt` — converts implicit toolchain deps into declared ones (Makefile:3, Makefile:5).
- Wire `scripts/setup.sh` into the Makefile (e.g., a `setup:` target at Makefile:5) or delete it — resolves the orphaned file.
- Expand README.md:3 into a short usage section listing `make core` / `make helper` and what each is expected to do.
- Add a `test` target to the Makefile with a smoke test per entry point — would have caught the stub below.

## 6. Weakest boundary

Candidate boundaries were generated and scored before selection (SKILL.md "Weakest Boundary Reasoning"):

**Candidate A — the declared-but-stubbed `helper` entry point** (Makefile:4-5 → helper/run.js:1)
- evidence_strength: strong (both files directly observed; each is one line)
- severity: high (the command exits 0 while delivering no functionality — silent success on a stub)
- blast_radius: medium (half of the declared entry-point surface: the entire JS side of the repo)
- goal_relevance: high (the repo's stated nature is "Mixed-language project.", README.md:3; the JS half is fake)
- downstream_blocking_effect: high (any JS-side work must first decide whether `helper` is real)
- uncertainty: low

**Candidate B — zero validation of any entry point** (whole tree)
- evidence_strength: medium (absence-based)
- severity: medium (toy repo; nothing to crash)
- blast_radius: high (all entry points)
- goal_relevance: medium
- downstream_blocking_effect: medium (validation would surface A, but A is the defect itself)
- uncertainty: medium

**Candidate C — unwired setup script** (scripts/setup.sh:1-2)
- evidence_strength: strong (file observed; no reference in the 5-line Makefile or 3-line README)
- severity: low
- blast_radius: low
- goal_relevance: low
- downstream_blocking_effect: low
- uncertainty: low

**Candidate D — implicit toolchain dependencies** (python/node/shell never declared; Makefile:3, Makefile:5, scripts/setup.sh:1)
- evidence_strength: medium
- severity: low
- blast_radius: medium (breaks on machines without node/python)
- goal_relevance: low
- downstream_blocking_effect: low
- uncertainty: medium

**Selection: Candidate A.**

```text
Boundary: the Makefile-declared `helper` entry point versus its implementation
  (Makefile:4-5 declares the target; helper/run.js:1 is the implementation)
Observed contract: `make helper` (Makefile:4-5) runs `node helper/run.js` and
  thereby delivers the helper feature's behavior, symmetric with `core`
Observed violation or uncertainty: the implementation is a single TODO stub —
  `console.log('TODO');` (helper/run.js:1); the command succeeds (exit 0) while
  producing no functionality, and no test/CI exists to flag it (OBSERVED
  absence across the tree)
Evidence: Makefile:4-5 ("helper:" target), helper/run.js:1 (stub),
  Makefile:1-2 (`all` wires only `core`), README.md:3 (repo claims to be a
  mixed-language project)
Weakness type: Ghost Features
Logic trace: Makefile:4-5 declares `helper:` as a first-class runnable target
  invoking `node helper/run.js`, and Makefile:1-2 shows the default `all`
  target wiring only `core`. The implementation behind that declared target,
  helper/run.js:1, contains only `console.log('TODO');` — functionality
  mentioned in documentation (the Makefile is the repo's build-surface
  documentation) with no corresponding implementation, which is exactly
  weakness-types.md:7 "Ghost Features: Functionality mentioned in
  documentation that has no corresponding implementation". Because the
  command still exits 0 (a runnable stub, observable from the file contents),
  the failure is silent: nothing in the repository can distinguish this
  declared feature from a real one. Therefore the weakest boundary is the
  ghost `helper` feature, not merely a missing test.
Failure consequence: `make helper` — and any downstream pipeline that runs it —
  reports success while the feature does nothing; the JS half of the
  "Mixed-language project." (README.md:3) is behaviorally empty, and any
  future work on the JS side inherits a fake contract.
Confidence: High — every cited fact is directly OBSERVED in files actually
  opened (the repo is 5 files, all read in full); the classification follows
  the canonical Ghost Features definition (weakness-types.md:7). Little would
  raise it further; the remaining ambiguity is only *intent* (whether the
  stub is a deliberate placeholder), which no file in the repo answers.
Alternatives considered: (B) Zero Validation lost because it is absence-based
  and lower-consequence — the missing tests are what *allow* the ghost
  feature to ship silently, but the defect itself is the stub; (C) the
  unwired scripts/setup.sh lost on severity and blast radius (nothing
  references it, nothing breaks); (D) implicit toolchain deps lost on
  severity and centrality (standard Makefile practice, no evidence of
  breakage). Candidate A wins on the strongest combination of direct
  evidence, consequence, and centrality to the repo's stated goal.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)

The primary fog type is **docs_fog**.

- **ui_fog — excluded.** The decision tree (ui-fog-signals.md:156-158) is unambiguous: there is no frontend code at all (no HTML/CSS/JSX/Vue; helper/run.js:1 is a Node script, not UI). Zero Tier-1/Tier-2 UI signals are present.
- **product_fog — excluded.** README.md:3 makes no feature promise; there is no product contract being violated (SKILL.md:214-217 requires a promised-but-absent feature, and none is promised).
- **architecture_fog — secondary, contributing.** Two literal architecture_fog evidence bullets apply (SKILL.md:224-227): "unwired modules" (scripts/setup.sh:1-2 is referenced by nothing) and "structural mismatch between entry points and flow" (the `helper` entry point has no flow behind it, Makefile:4-5 vs helper/run.js:1). But nothing structural *prevents* implementation — the architecture is trivially simple — so structure is not the binding constraint.
- **docs_fog — primary.** Per the ghost-feature decision procedure (SKILL.md:229-239), the `helper` feature "never existed as code" (helper/run.js:1 is a TODO stub) while the Makefile still presents it as a real target (Makefile:4-5) → the mismatch lives in the *declared/documentation surface*, not in a product contract and not in structure. Independently, README.md:1-3 is the sole documentation and provides no specification for the existing behavior of either entry point — "absent specs for existing behavior" is a listed docs_fog signal (SKILL.md:222-223).

The evidence is not genuinely tied: docs_fog is supported by the skill's own ghost-feature decision procedure plus the absent-spec signal, so `primary_fog_type` is `docs_fog` with `escalation_recommended: false` (the residual architecture_fog is recorded here as secondary and does not drive routing).

## 7. Evidence

File-level evidence supporting the diagnosis:

- `helper/run.js:1` — the entire JS implementation is `console.log('TODO');`, a stub behind a declared Makefile target (Makefile:4-5). This is the direct evidence for the Ghost Features boundary.
- `Makefile:4-5` — `helper:` / `node helper/run.js` declares the target whose implementation is the stub.
- `Makefile:1-3` — `all: core` / `python core/main.py` shows the default flow deliberately excludes `helper`, so the stub is never exercised by the main path.
- `README.md:3` — "Mixed-language project." is the repo's only documentation and only claim; it states the nature but specifies no behavior.
- `core/main.py:1` — `print('core')` is the complete Python entry point (functional, minimal).
- `scripts/setup.sh:1-2` — `#!/bin/sh` / `echo setup` is a script referenced by no Makefile target and no README text (unwired; secondary architecture_fog signal).
- Absence evidence (OBSERVED via the full recursive tree inventory): no manifests, no tests, no CI, no schemas — the validation gap that lets the ghost feature pass silently.

**Logic trace:** The cited evidence chains to the conclusion as follows: Makefile:4-5 declares `helper` as a runnable entry point, but the file it invokes, helper/run.js:1, contains only a TODO stub; README.md:3 promises a "Mixed-language project." whose JS half therefore does not exist behaviorally; Makefile:1-3 shows the default path never even runs the stub; and the complete absence of tests/CI (OBSERVED in the tree inventory) means nothing can detect the stub's silent success. A declared feature with no corresponding implementation is the canonical definition of Ghost Features (weakness-types.md:7), and because the mismatch lives in the declared/documentation surface (the feature never existed as code) rather than in a product promise or in blocking structure, the fog classification is docs_fog (SKILL.md:229-239). The same evidence set also surfaces the contributing architecture_fog signals (unwired scripts/setup.sh:1-2; entry-point-to-flow mismatch at Makefile:4-5), recorded as secondary.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Mixed-language project."
    supports_claim: "The repo's only documentation and only claim: no behavior is specified for either entry point."
  - file: Makefile
    lines: L1-L3
    quote: "all: core\ncore:\n\tpython core/main.py"
    supports_claim: "The default flow wires only 'core'; 'helper' is deliberately excluded from 'all'."
  - file: Makefile
    lines: L4-L5
    quote: "helper:\n\tnode helper/run.js"
    supports_claim: "The Makefile declares 'helper' as a first-class runnable target, symmetric with 'core'."
  - file: helper/run.js
    lines: L1
    quote: "console.log('TODO');"
    supports_claim: "The entire implementation behind the declared 'helper' target is a TODO stub - Ghost Features."
  - file: core/main.py
    lines: L1
    quote: "print('core')"
    supports_claim: "The Python entry point exists and is minimal but functional; it is not the weakness."
  - file: scripts/setup.sh
    lines: L1-L2
    quote: "#!/bin/sh\necho setup"
    supports_claim: "An unwired script referenced by no Makefile target and no README text (secondary architecture_fog signal)."
```

## 9. Why this boundary matters

If this stays weak, the failure mode is silent: `make helper` exits 0 while doing nothing, so any pipeline, CI job, or user that trusts the Makefile's declared surface (Makefile:4-5) will treat an absent feature as present. The repo's stated identity — "Mixed-language project." (README.md:3) — is half-fake, and every downstream action (implementing helper, adding packaging, writing tests, teaching from this fixture) inherits an unresolved question: is `helper` a real feature or a placeholder? A ghost feature is also the exact pattern that gets copy-pasted as "real" in larger codebases: the declaration outlives the intent, and the TODO is quietly assumed done.

## 10. Candidate next steps

1. Decide and write the one-line contract for `helper` — what should `node helper/run.js` produce or do? (In README.md or as the first line of helper/run.js.)
2. Replace the TODO stub (helper/run.js:1) with the minimal agreed implementation, or remove the `helper` target (Makefile:4-5) if the feature is not wanted.
3. Add `package.json` declaring the node dependency and the `helper` script — closes the implicit-dependency gap behind Makefile:5.
4. Add a `test` target to the Makefile with a smoke test per entry point (exit-code check for both) — prevents future ghost features from passing silently.
5. Wire scripts/setup.sh into the Makefile as a `setup:` target or delete it — resolves the unwired file.

## 11. Recommended next step

Write the one-line behavioral contract for `helper` into README.md (or as the first comment of helper/run.js): what the command must do. This is the smallest action that converts the ghost feature into an explicit decision, and it unblocks every other step (implementation, packaging, tests all depend on knowing what `helper` is for). This is a diagnostic recommendation only — no implementation was performed.

## 12. Recommended workflow

`docs-implementation-workflow` — a top-level ID in the canonical `skills/workflow-planner/references/workflow-registry.yaml` (workflow-registry.yaml:812-847), with `allowed_execution_modes: guided_execution, autonomous_execution` (workflow-registry.yaml:822-824). Recommended execution mode: `guided_execution` (registry-listed for this workflow; recommending a workflow is not executing it — the diagnostic No Implementation boundary is unaffected).

Why this workflow: the primary fog type is docs_fog (Section 6.5), and `docs-implementation-workflow` is the registry's docs-specific implementation path — it aligns domain understanding via its docs-aligner step (workflow-registry.yaml:827-833), then produces the documentation/specification structure via to-prd (workflow-registry.yaml:834-840), which is precisely the missing contract around the `helper` feature (README.md:1-3, Makefile:4-5, helper/run.js:1).

Why not the closest alternatives: `architecture-implementation-workflow` (workflow-registry.yaml:848-904) would be the choice if the secondary architecture_fog were primary, but nothing structural blocks implementation here; `implementation-workflow` (workflow-registry.yaml:587-643) is the generic default and would not add the spec-first step the ghost feature needs; `fast-path-workflow` / `full-fog-workflow` (workflow-registry.yaml:2-94) are diagnostic orchestration wrappers — this brief already is the diagnosis, so routing straight to the implementation workflow is correct.

Missing precondition before it can run: a human decision on the intended `helper` behavior (Section 11 step 1) — without it, the workflow's docs-aligner step has no domain contract to align.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-language
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (line 3): 'Mixed-language project.' is the only documentation; no behavior is specified for either entry point"
  - "Makefile (lines 4-5): declares 'helper' target running 'node helper/run.js'"
  - "helper/run.js:1: entire implementation is 'console.log('TODO');' - declared feature with no implementation (Ghost Features)"
  - "Makefile (lines 1-3): 'all' wires only 'core'; the stub is never exercised by the default path"
  - "core/main.py:1: complete Python entry point is 'print('core')'"
  - "scripts/setup.sh (lines 1-2): script referenced by no Makefile target and no README text (unwired)"
  - "Absence (OBSERVED over full tree): no tests, no CI, no manifests, no schemas"
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:20:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

For `workflow-planner` (or a downstream docs workflow executor):

> Repository: `experiments/repository-sensemaking-skill-hardening-v1/corpus/multi-language` — a minimal mixed-language fixture (Python `core`, Node `helper`, shell `setup.sh`, Makefile).
> Diagnosis: repository_sensemaking_brief with `primary_fog_type: docs_fog` (contributing secondary: architecture_fog); weakest boundary is **Ghost Features** at `Makefile:4-5` / `helper/run.js:1` — the declared `helper` target runs a `console.log('TODO')` stub and exits 0 silently; no tests or CI exist to catch it; README.md:3 specifies no behavior for either entry point.
> Request: plan `docs-implementation-workflow` in `guided_execution` mode (registry-listed: workflow-registry.yaml:812-847, allowed modes at 822-824). First step: spec the one-line behavioral contract for `helper` (what `node helper/run.js` must do) and the minimal documentation structure for both entry points, then align it with the Makefile surface (Makefile:1-5). Do not implement code in this step; the `helper` stub itself is a separate implementation decision for the human.
