# Repository Sensemaking Brief

## 1. Repository goal
This repository (`adv-misleading-dirs`) appears to be a minimal Python toy: a single runnable script (`main.py`) imports one symbol from each of two packages (`handlers`, `models`) and prints them. There is no stated purpose anywhere — the README contains only a title (`README.md:1`), and there is no manifest, roadmap, or design note (OBSERVED via the full recursive listing: `README.md`, `main.py`, `handlers/__init__.py`, `handlers/user.py`, `models/__init__.py`, `models/user.py`). The observable intent of the layout is to demonstrate a conventional package structure (`handlers/` for request handling, `models/` for domain data), but the actual contents invert that convention, which is the core defect this brief diagnoses.

## 2. Current shape
**Inventory (OBSERVED, full recursive listing):**
- `README.md` — 1 line, title only.
- `main.py` — 3 lines, the entry point.
- `handlers/__init__.py`, `models/__init__.py` — both empty (0 bytes, confirmed by opening).
- `handlers/user.py` — 2 lines: `class User`.
- `models/user.py` — 2 lines: `def handle(request)`.

**Runtime flow (DERIVED from the files above):**
- *Startup path*: `python main.py` is the only way the system starts. `main.py:1` imports `User` from `handlers.user` and `main.py:2` imports `handle` from `models.user`; `main.py:3` prints both. Both imports resolve because the packages have `__init__.py` files (OBSERVED, `handlers/__init__.py` / `models/__init__.py` empty but present).
- *Orchestration*: none — the script executes top-to-bottom with no control flow.
- *Domain/core logic*: `models/user.py:1-2` (`handle(request)`) and `handlers/user.py:1-2` (`class User`) — but note the responsibilities are swapped relative to their package names.
- *Persistence/state*: none. No files, databases, caches, globals, queues, or environment variables are read or written anywhere (OBSERVED — no such code exists in the four content files).
- *External integrations*: none — only stdlib imports; there is no manifest (no `pyproject.toml`, `setup.py`, or `requirements.txt`), so dependency semantics are: the imports in `main.py:1-2` are `declared`+`used`+`runtime` (proven on the execution path), but nothing else is declared anywhere.
- *Background work*: none.
- *Output boundary*: stdout via `print` at `main.py:3` (DERIVED — the only side effect in the code).
- *Validation*: none (see Pass D below).
- *Where responsibility becomes unclear*: the boundary between "handlers" and "models" is inverted — a reader navigating by package name will look for the request handler in `handlers/` (it is in `models/`) and the domain model in `models/` (it is in `handlers/`). This is the structural fault line this brief selects (Section 6).

**Passes executed:** Pass A (orientation — README, manifests, config: only `README.md:1` exists; no manifests/CI/container config), Pass B (execution — single entry point `main.py:1-3`), Pass C (system structure — entry point → two imported symbols → print; every hop traced, none missing), Pass D (validation — no tests, schemas, assertions, or authorization anywhere in the tree), Pass E (contradiction — the package-name ↔ content inversion documented in Section 6).

## 3. Strong signals
- The code is minimal and self-consistent: imports in `main.py:1-2` are explicit, resolve correctly (empty `__init__.py` files make both packages importable), and the runtime path is provable — `main.py:3` prints both symbols. There is no dead weight, no generated bundle, no lockfile cruft.
- `handle(request)` at `models/user.py:1` defines a concrete, single-argument request contract — small but explicit.
- The repository is small enough that the inversion is fully auditable in one pass; nothing is hidden in depth.

## 4. Missing pieces
- **No documentation beyond a title**: `README.md:1` is only `# misleading-dirs`; there is no description of what the repo does, how to run it, or what each package is for.
- **No validation structure**: Pass D found no tests, no schema, no assertions, no lint/CI configuration — nothing checks that the code behaves as intended.
- **No manifest**: no packaging or dependency metadata exists, so there is no declared contract for how the project is built or run.
- **No vocabulary contract**: nothing documents which responsibility lives in which package, which is precisely what makes the inversion undetectable to a reader who trusts the directory names.

## 5. Improvement opportunities
- Rename or restructure so the vocabulary matches the contents (move `class User` into `models/` and `handle` into `handlers/`, updating `main.py:1-2`), or, if the inversion is deliberate, document it explicitly in the README.
- Add a minimal smoke test asserting that `main.py` imports and prints both symbols (would also give Pass D a foothold for future changes).
- Expand `README.md:1` into a short run/usage note describing the entry point and the layout contract.
- Add a one-line structural check (e.g., a naming lint) so package-name ↔ content drift cannot silently recur.

## 6. Weakest boundary
**Candidate generation and scoring** (per SKILL.md "Weakest Boundary Reasoning"; each candidate below was scored on evidence strength, severity, blast radius, goal relevance, downstream blocking effect, uncertainty):

| Candidate | evidence_strength | severity | blast_radius | goal_relevance | downstream_blocking_effect | uncertainty |
|---|---|---|---|---|---|---|
| A. Directory-name ↔ content vocabulary inversion (`handlers/` holds a model class; `models/` holds a handler function) | strong | medium | high | high | high | low |
| B. Zero Validation (no tests/schemas/checks anywhere in the repo) | strong | low | low | low-medium | low | low |
| C. Absent documentation (README is a title only) | strong | low | medium | medium | low-medium | low |

**Selected boundary:**

```text
Boundary: the naming contract between package names and their contents —
          `handlers/user.py` defines a data model while `models/user.py`
          defines a request handler, and `main.py` imports across that
          inversion (main.py:1-2).
Observed contract: a package named `handlers` contains request-handling
          logic; a package named `models` contains domain/data definitions
          (conventional Python vocabulary; the directory names are the only
          structural documentation the repo has).
Observed violation or uncertainty: `handlers/user.py:1-2` defines `class
          User` (a model), and `models/user.py:1-2` defines `def
          handle(request)` (a handler) — each package's contents contradict
          its name. There is no README text (README.md:1 is only a title)
          that would document or excuse the inversion, and there is no
          manifest or spec that defines the intended semantics.
Evidence: handlers/user.py:1-2 (`class User`), models/user.py:1-2 (`def
          handle(request)`), main.py:1-2 (imports crossing the inversion),
          README.md:1 (title only — no documented contract to compare
          against).
Weakness type: Vocabulary Drift
Logic trace: main.py:1 imports `User` from `handlers.user` and main.py:2
          imports `handle` from `models.user`, and main.py:3 prints both —
          so both symbols exist and the runtime path is proven (OBSERVED).
          Opening `handlers/user.py` shows it defines `class User`
          (handlers/user.py:1-2) — a data model — inside the package named
          "handlers"; opening `models/user.py` shows it defines `def
          handle(request)` (models/user.py:1-2) — a request handler — inside
          the package named "models" (OBSERVED). The directory names are the
          repository's only structural vocabulary (README.md:1 documents
          nothing), and that vocabulary disagrees with the code contents:
          the term "handlers" does not describe what handlers/ contains, and
          the term "models" does not describe what models/ contains. The
          code exists and executes (main.py:3), so this is not a missing or
          promised-but-absent feature (Ghost Features does not apply — GAP-6
          mapping: docs/structure misdescribing EXISTING code is Vocabulary
          Drift, never Ghost Features). The drift is between the structural
          vocabulary and the actual code, which is exactly the Vocabulary
          Drift definition in weakness-types.md ("Terms used in the README
          don't match the code or directory structure" — here the terms are
          the directory names and the mismatch is with the code inside
          them). Conclusion: Vocabulary Drift at the package-name ↔
          contents boundary.
Failure consequence: any human or agent navigating by package-name
          semantics will mislocate both the model and the handler — new
          handler logic gets added to handlers/ alongside a model class,
          new domain logic to models/ alongside a handler — compounding the
          drift with every change. Sensemaking and documentation tooling
          (docs-aligner-style CONTEXT extraction, issue decomposition) will
          reproduce the inverted responsibilities, and the inversion is
          invisible to automated checks because the code runs correctly.
Confidence: high — the inversion is directly observable in four opened
          files (handlers/user.py:1-2, models/user.py:1-2, main.py:1-2,
          README.md:1) and needs no inference about runtime behavior. What
          would raise it further: a human audit confirming the intended
          semantics of the two packages (e.g., that the inversion is not a
          deliberate teaching choice).
Alternatives considered:
  - Zero Validation (B): the absence of any test/check is real (Pass D
    found none) but low-severity for a 5-file toy whose only behavior is a
    print — and it is a consequence of the fixture's minimalism, not the
    adversarial defect. It lost on severity and goal relevance.
  - Absent documentation (C): the near-empty README (README.md:1) is
    genuinely weak, but it does not misdescribe anything — the misdirection
    lives in the structure, not in prose that could be fixed by writing
    more docs. It lost on centrality: docs_fog would be a secondary
    observation, not the weakest boundary.
  - Ghost Features: rejected outright — nothing is advertised as a feature
    and both symbols are implemented and reachable, so the
    documented-surface-with-no-implementation test fails (GAP-6).
  - Implicit Dependencies: rejected — main.py:1-2 imports are explicit,
    declared-in-code, and runtime-proven; nothing depends on an undeclared
    path.
```

**Weakness type:** Vocabulary Drift

## 6.5. Problem classification (fog type)
Primary: **architecture_fog**. The repository has no frontend surface at all (no HTML/CSS/JS/React/Vue/Angular — the entire tree is four Python files), so the UI Fog Signals Registry decision tree (`ui-fog-signals.md` L156-158) excludes `ui_fog` outright. There is no product contract — no README/roadmap promises any deliverable — so `product_fog` has no evidence. The README (`README.md:1`) does not misdescribe the code (it describes nothing), so `docs_fog` is at most secondary. The defect is structural: module/directory names misplace responsibility boundaries, which is the `architecture_fog` signal set ("module structure prevents confident implementation; structural mismatch between entry points and flow" — the entry point `main.py:1-2` has to import across the misnamed boundaries). Per the entry-point rule, `main.py` is a real, running entry point — the system boots — so this is a structural defect in an otherwise-running system, not a promised deliverable with no implementation (not `product_fog`).

Secondary fog: `docs_fog` — the README is a bare title (`README.md:1`) and no layout contract is documented, so knowledge of the intended structure is inaccessible. The primary (structural) defect drives routing; the secondary is recorded here for completeness.

`primary_fog_type: architecture_fog` (recorded in Section 13; prose agreement required by the validator).

## 7. Evidence
The diagnosis rests on four opened files:

- `main.py:1` (`from handlers.user import User`) and `main.py:2` (`from models.user import handle`) prove the entry point imports a model from the `handlers` package and a handler from the `models` package; `main.py:3` (`print(User, handle)`) proves the runtime path executes both symbols (OBSERVED).
- `handlers/user.py:1-2` defines `class User:` / `pass` — the package named "handlers" contains a data model, not a handler (OBSERVED).
- `models/user.py:1-2` defines `def handle(request):` / `return 'handled'` — the package named "models" contains a request-handler function, not a model (OBSERVED).
- `README.md:1` is only the title `# misleading-dirs` — there is no documented contract, so the inversion is un-documented and un-flagged (OBSERVED).
- Pass D (validation structure): the full recursive listing shows no test files, no schemas, no assertions, no CI — no automated check exists that would catch either the inversion or a regression (OBSERVED via directory listing; absence claims are scoped to the listed tree).

**Logic trace:** The weakest boundary is the package-name ↔ contents inversion. `main.py:1-2` imports `User` from `handlers.user` and `handle` from `models.user`; opening those files shows `handlers/user.py:1-2` defines a class (model) while `models/user.py:1-2` defines a function (handler) — the two packages' names and their contents contradict each other by construction, and `README.md:1` provides no text that would document or excuse the inversion. Because the code runs (`main.py:3`), the failure mode is not a missing feature but a misleading structural vocabulary — Vocabulary Drift — and because no frontend exists and no product promise is made, the fog is structural (`architecture_fog`) with `docs_fog` secondary. Every other candidate (Zero Validation, absent docs) scored lower on severity and centrality (Section 6 table).

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: main.py
    lines: L1-L3
    quote: "from handlers.user import User\nfrom models.user import handle\nprint(User, handle)"
    supports_claim: "Entry point imports a model class from the 'handlers' package and a handler function from the 'models' package, and executes both — the runtime path across the inverted boundaries is proven."
  - file: handlers/user.py
    lines: L1-L2
    quote: "class User:\n    pass"
    supports_claim: "The package named 'handlers' contains a data model (class User), not a request handler — vocabulary/content inversion, side one."
  - file: models/user.py
    lines: L1-L2
    quote: "def handle(request):\n    return 'handled'"
    supports_claim: "The package named 'models' contains a request-handler function (handle), not a domain model — vocabulary/content inversion, side two."
  - file: README.md
    lines: L1
    quote: "# misleading-dirs"
    supports_claim: "README is a title only; no documented contract explains or contradicts the inverted package layout."
```

## 9. Why this boundary matters
If the package-name ↔ contents inversion stays unaddressed, every downstream consumer of this repository inherits a false mental model: an agent extending the code will add new handler logic to `handlers/` (next to a model class) and new domain logic to `models/` (next to a handler), deepening the drift with each change. Documentation and issue-decomposition tooling that derive CONTEXT from directory structure will institutionalize the inverted responsibilities, and because the code executes correctly, no automated check will ever surface the problem. In a larger system this exact pattern is how responsibility boundaries silently rot: the names stop meaning anything, and the cost is paid by every future reader and every workflow that routes work by structure.

## 10. Candidate next steps
1. **Restructure to match vocabulary**: move `class User` into `models/` and `handle` into `handlers/` (i.e., swap the file contents or move the files), updating `main.py:1-2` accordingly — the smallest change that makes the names true again.
2. **Document the intent instead** (only if the inversion is deliberate): expand `README.md:1` into a short note explaining the layout contract and why it is inverted.
3. **Add a smoke test**: assert that `main.py` imports and prints both symbols, giving the repo its first automated check (addresses the Zero Validation gap observed in Pass D).
4. **Add a naming/layout check**: a tiny lint that verifies `handlers/` contains callables and `models/` contains data classes, preventing recurrence.
5. **Write minimal usage docs**: entry point, how to run, and where each responsibility lives.

## 11. Recommended next step
Restructure so the directory vocabulary matches the contents (step 1): swap `class User` and `handle` between `handlers/user.py` and `models/user.py` and update the imports at `main.py:1-2`. It is the single highest-leverage move — it repairs the Vocabulary Drift at its source in minutes, unblocks all downstream work (docs, tests, extensions), and requires no new infrastructure. If the inversion is a deliberate teaching choice, the equivalent action is step 2 (document it) — the decision is the human's, but the diagnostic is unambiguous either way.

## 12. Recommended workflow
`architecture-implementation-workflow` — the registry's architecture/refactoring implementation workflow (registered in `skills/workflow-planner/references/workflow-registry.yaml`; its chain is docs-aligner → to-prd → to-issues → triage → tdd → handoff). Rationale: the diagnosed fog is `architecture_fog` (structural boundary/vocabulary defect), and this workflow is the registry entry whose purpose is "For architecture/refactoring problems" — it aligns the domain, produces a refactoring spec, decomposes into issues, and implements via TDD. Closest alternatives considered and rejected: `implementation-workflow` (the generic default — would also fit but is less specific than the architecture variant); `docs-implementation-workflow` (rejected — writing more docs about an inverted layout would institutionalize the drift; the fix is structural); `ui-diagnostic-workflow` / `ui-implementation-workflow` (rejected — no frontend surface exists in the target repo). Precondition before it can run: the target repo has no test scaffold, so the workflow's TDD step (registry L891-897) needs a minimal test setup established first (e.g., candidate step 3) or the TDD cycle must create it. Recommended execution mode: `guided_execution` — one of `architecture-implementation-workflow`'s two `allowed_execution_modes` (registry L858-861; `plan_only` is NOT offered by this workflow and was therefore not used). Recommending this workflow is a diagnostic handoff only; execution happens later under the runtime's own authorization.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-misleading-dirs
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "handlers/user.py (lines L1-L2): package named 'handlers' contains a model class (class User), not a handler"
  - "models/user.py (lines L1-L2): package named 'models' contains a handler function (def handle), not a model"
  - "main.py (lines L1-L3): entry point imports across the inverted boundaries and executes both symbols"
  - "README.md (line L1): title only; no documented contract explains or contradicts the inverted layout"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: "Vocabulary Drift: package names (handlers/, models/) contradict their contents (a model class in handlers/, a handler function in models/)"
weakness_type: Vocabulary Drift
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-07-26T12:00:00Z"
updated_at: "2026-07-26T12:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
```
Run the architecture-implementation-workflow (execution mode: guided_execution) against
the repository at experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-misleading-dirs.
Context: the repository_sensemaking_brief for this repo classifies it as architecture_fog
with a Vocabulary Drift weakest boundary — the package names "handlers" and "models"
contradict their contents: handlers/user.py defines a model class (class User) while
models/user.py defines a request handler (def handle(request)), and main.py imports across
the inversion. Begin with domain alignment (docs-aligner): confirm whether the inverted
layout is intentional. Then produce a refactoring spec that, in the default case, swaps the
two responsibilities so the directory vocabulary matches the contents (updating main.py
imports), or, if the inversion is deliberate, specifies the documentation change instead.
Note the precondition: the target repo currently has no test scaffold, so establish a
minimal test setup before the TDD step. Do not execute anything outside this workflow's
authorized steps.
```
