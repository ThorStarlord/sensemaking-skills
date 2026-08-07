# Repository Sensemaking Brief

## 1. Repository goal
This is a minimal Python fixture repository whose only behavior is a single
entry point that imports and prints two symbols: a `User` class and a `handle`
function (`main.py:1-3`). The evident purpose — signaled by the README title
`# misleading-dirs` (`README.md:1`) — is to present a codebase whose package
directory names (`handlers/`, `models/`) invert the conventional meaning of
their contents: the request-handling function lives under `models/` and the
data-model class lives under `handlers/`. In plain terms, the repo is a
demonstration/trap fixture: it exists to test whether a reader (human or
tool) trusts directory-name semantics over actual file contents. No product
surface, user features, or real workload are present (INFERRED from the
absence of any feature documentation or entry points beyond `main.py`).

## 2. Current shape
Full inventory (OBSERVED via recursive listing; every file opened):

- `README.md` — 1 line (19 bytes): only the heading `# misleading-dirs`; no
  purpose, structure, usage, or run instructions (`README.md:1`).
- `main.py` — 3 lines: `from handlers.user import User` (L1),
  `from models.user import handle` (L2), `print(User, handle)` (L3). This is
  the single entry point; there is no `if __name__ == "__main__"` guard, so
  the module executes these statements on import.
- `handlers/__init__.py` — 0 bytes (empty package marker; opened, no content).
- `handlers/user.py` — 2 lines: `class User:` / `pass` (a data-model class
  living in the "handlers" package) (`handlers/user.py:1-2`).
- `models/__init__.py` — 0 bytes (empty package marker; opened, no content).
- `models/user.py` — 2 lines: `def handle(request):` / `return 'handled'`
  (request-handling logic living in the "models" package)
  (`models/user.py:1-2`).

**Runtime flow** (per the architecture-reconstruction requirement): what
starts the system is `main.py:1-3` — top-level import statements, run when
`python main.py` (or any import of `main`) is executed. There is no
orchestration layer: the main flow is import → print. Domain/core logic is
the `User` class (`handlers/user.py:1-2`) and the `handle` function
(`models/user.py:1-2`). Persistence/state: none — no files, database, cache,
queue, or environment variables are touched anywhere in the repository.
External integration points: none. Background work: none. Output boundary:
stdout via `print(User, handle)` (`main.py:3`).

**Dependency semantics** (classified, not conflated): both imports in
`main.py:1-2` are `used` (referenced by code) and resolve to modules that
exist (`handlers/user.py`, `models/user.py`), so they are also `runtime` on
the only proven execution path (`python main.py`). There is no manifest of
any kind (no `pyproject.toml`, `setup.py`, `requirements.txt`), so there are
no `declared` dependencies at all; every dependency claim here is import-based.

**Where responsibility becomes unclear**: at the package-name ↔ content
boundary. `main.py:1` imports the data class from `handlers.user` and
`main.py:2` imports the handler function from `models.user` — i.e., the
imports themselves encode the inverted mapping. A reader navigating by
directory-name semantics (handlers = request handling, models = data) will
open the wrong module for each concern. Nothing in the repository corrects
that misimpression: `README.md:1` is only a title and both `__init__.py`
markers are empty (0 bytes). Validation: none anywhere — no tests, no
schemas, no assertions, no input validation (the `handle` function
`models/user.py:1-2` ignores its `request` argument and returns a constant),
no error boundaries.

## 3. Strong signals
- The code is tiny and fully readable: every source file is 1–3 lines, so
  the inverted layout is discoverable by opening the four files — no
  indirection hides it.
- The entry point's imports are not dead: both symbols imported at
  `main.py:1-2` are actually defined (`handlers/user.py:1`,
  `models/user.py:1`), so the package runs as-is — the inversion is
  semantic, not mechanical.
- Within-file naming is consistent (`user.py` under `handlers` defines
  `User`; `user.py` under `models` defines `handle`); the drift is at the
  package-name layer, not inside modules.
- There is exactly one entry point (`main.py`), with no hidden dispatch or
  plugin loading to confuse analysis further.

## 4. Missing pieces
- Any README content beyond the bare title (`README.md:1`): no purpose
  statement, no structure map, no run instructions, no responsibilities
  table.
- Package boundary documentation: both `__init__.py` files are 0 bytes
  (`handlers/__init__.py`, `models/__init__.py`) and neither module has a
  docstring, so nothing states what `handlers/` or `models/` is supposed to
  contain.
- Tests or any automated check that would codify the actual contract (e.g.,
  a smoke test asserting `python main.py` prints both symbols) or catch the
  naming/content inversion.
- A build/dependency manifest (`pyproject.toml`/`requirements.txt`) — the
  repository declares nothing about how it is run or installed.
- A truthful mapping between package names and responsibilities — the
  repository contains no statement of intent at all, so the inversion is
  completely unanchored.

## 5. Improvement opportunities
- Add one-line docstrings to `handlers/user.py` and `models/user.py`
  describing actual responsibilities, so the boundary is self-documenting
  even before any rename.
- Add a smoke test (pytest, or a plain `python main.py` run in CI) so the
  entry-point contract is executable and regressions are caught.
- Expand `README.md` into a short orientation: purpose, entry point, and a
  per-module responsibilities note.
- Consider a structural lint rule (e.g., assert `handlers/` contains no
  class definitions and `models/` contains no functions) to enforce
  whatever naming contract is eventually chosen.

## 6. Weakest boundary
Candidate generation and scoring (per the skill's weakest-boundary
reasoning):

| Candidate | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|
| A. Vocabulary Drift: `handlers/`/`models/` names invert contents | strong | medium | high | high | high | low |
| B. Zero Validation: no tests/checks anywhere | strong | low | medium | low | medium | low |
| C. Implicit Dependencies: layout contract exists only in `main.py:1-2` imports | medium | low | medium | medium | medium | medium |
| D. Empty README / missing orientation docs | strong | low | medium | medium | medium | low |

Selected: **A — Vocabulary Drift** (the strongest combination of
consequence, evidence, centrality, and downstream blocking; see Logic trace
below).

```text
Boundary:
  The package-directory vocabulary (handlers/ = request handling,
  models/ = data) versus the actual module contents, wired crosswise by the
  entry point. Concretely: handlers/user.py:1-2 defines class User (a data
  model) and models/user.py:1-2 defines def handle(request) (a request
  handler), while main.py:1-2 imports User FROM handlers.user and handle
  FROM models.user.
Observed contract:
  main.py:1-2 establishes the naming contract: the "handlers" package
  provides the model class and the "models" package provides the handler
  function — the opposite of conventional package-name semantics.
Observed violation or uncertainty:
  handlers/user.py:1-2 contains only a class (no handler code) and
  models/user.py:1-2 contains only a function (no data model). A reader who
  navigates by directory-name semantics cannot locate either concern without
  opening both modules; nothing in the repo (README.md:1 is a bare title;
  handlers/__init__.py and models/__init__.py are 0-byte markers) corrects
  the misimpression.
Evidence:
  main.py:1-2 (the crosswise imports), handlers/user.py:1-2 (class User in
  handlers/), models/user.py:1-2 (def handle in models/), README.md:1 (bare
  title), handlers/__init__.py and models/__init__.py (0 bytes, opened).
Weakness type:
  Vocabulary Drift
Logic trace:
  main.py:1 imports `User` from `handlers.user` and main.py:2 imports
  `handle` from `models.user`, so the entry point's own imports assert that
  the "handlers" package contains a data class and the "models" package
  contains a function. Opening handlers/user.py:1 shows `class User:` —
  model-shaped code in the handlers package — and opening models/user.py:1
  shows `def handle(request):` — handler-shaped code in the models package.
  The terms the directory structure presents (handlers = handling, models =
  data) therefore do not match the semantics the code delivers: the
  repository's naming vocabulary has drifted from its contents. README.md:1
  (a bare title) and the empty __init__.py markers provide no corrective
  documentation, and no tests exist to enforce any naming contract. Because
  the defect sits in the naming/boundary layer of the structure — not in
  missing product specs and not in any UI surface — the weakest boundary is
  Vocabulary Drift and the fog type is architecture_fog.
Failure consequence:
  Any human or agent relying on package-name semantics mislocates the
  request handler and the data model, so edits, diagnoses, and refactors get
  applied to the wrong module. The code runs correctly (main.py:1-3), so
  the trap is silent: no runtime error ever signals the inversion. Any
  future normalization (rename/move) can break main.py:1-2 with nothing
  catching it.
Confidence:
  high. Direct file contents were opened for every cited module; the only
  thing that would raise confidence further is an explicit author statement
  of intended package responsibilities (a README purpose section or git
  history), which is absent by design in this fixture.
Alternatives considered:
  B (Zero Validation) lost because there is no core logic complex enough for
  missing tests to be the blocking defect; adding tests without fixing the
  naming would document a wrong contract. C (Implicit Dependencies) lost
  because Python imports are explicit by language design — the hazard is
  the mislabeled semantics, not the import mechanism. D (empty README /
  docs) lost because documentation would merely describe the inverted
  layout; the primary defect is structural naming, which documentation
  cannot repair. The repository does have a genuine weakness here — the
  fixture's entire substance is the inversion — so a boundary is warranted,
  not manufactured.
```

**Weakness type:** Vocabulary Drift

## 6.5. Problem classification (fog type)
`architecture_fog` — the operative problem is at the module-boundary /
structure layer: package names mislabel module contents, so the boundaries a
reader must rely on are untrustworthy. This is precisely "code structure
problems, design issues, unclear boundaries." `ui_fog` is ruled out by the UI
Fog Signals Registry decision tree step 1: the repository contains no
frontend code of any kind (the complete file listing is six Python files —
no HTML, CSS, JS, TSX, and no routing logic). `product_fog` is ruled out
because there are no user-need artifacts, feature specs, or analytics — there
is no product surface at all. `docs_fog` is a contributing secondary factor
(the README is a bare title at `README.md:1` and both `__init__.py` files are
empty), but the mismatch lives in the *structure* (directory names vs.
contents), not in documentation misdescribing the code: documentation would
only describe the inverted layout, not repair it. The primary defect is
structural naming, which is an architecture concern.

## 7. Evidence
- `main.py:1-2` — `from handlers.user import User` / `from models.user
  import handle`: the entry point expects the "handlers" package to provide
  a model class and the "models" package to provide a handler function.
- `handlers/user.py:1-2` — contains only `class User:` / `pass`: the
  "handlers" package contains no handler code.
- `models/user.py:1-2` — contains only `def handle(request):` /
  `return 'handled'`: the "models" package contains the request handler.
- `README.md:1` — the entire README is the single line `# misleading-dirs`.
- `handlers/__init__.py` and `models/__init__.py` — 0 bytes each (opened):
  empty package markers that document no boundary.

**Logic trace:** `main.py:1-2` establishes the naming contract the author
chose: `User` is imported from `handlers.user` and `handle` from
`models.user`. Opening `handlers/user.py:1` shows the handlers package
contains a class, and opening `models/user.py:1` shows the models package
contains a function — i.e., the package vocabulary (`handlers` = request
handling, `models` = data) is inverted relative to the code's actual
semantics. A reader navigating by convention therefore cannot locate the
request handler or the data model without opening both modules, and neither
`README.md:1` (a bare title) nor the empty `__init__.py` markers provides any
corrective documentation. Because the defect sits in the naming/boundary
layer of the structure — not in missing product specs and not in any UI
surface — the weakest boundary is Vocabulary Drift and the fog type is
`architecture_fog`. The repository also contains no tests or lint config at
all, so nothing enforces the chosen naming; the boundary is drift that is
also unenforced, but the drift itself is the primary defect.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: main.py
    lines: L1
    quote: "from handlers.user import User"
    supports_claim: "Entry point imports the User class from the handlers package."
  - file: main.py
    lines: L2
    quote: "from models.user import handle"
    supports_claim: "Entry point imports the handle function from the models package — the crosswise wiring."
  - file: main.py
    lines: L3
    quote: "print(User, handle)"
    supports_claim: "The only runtime behavior is printing both symbols; no other execution path exists."
  - file: handlers/user.py
    lines: L1-L2
    quote: "class User:\npass"
    supports_claim: "The handlers/ package contains a data-model class, not request-handling code."
  - file: models/user.py
    lines: L1-L2
    quote: "def handle(request):\nreturn 'handled'"
    supports_claim: "The models/ package contains the request-handling function."
  - file: README.md
    lines: L1
    quote: "# misleading-dirs"
    supports_claim: "README is only a bare title with no orientation about purpose or structure."
```

## 9. Why this boundary matters
- Any human or agent relying on package-name semantics will mislocate the
  request handler and the data model, leading to edits, diagnoses, or
  refactors applied to the wrong module.
- The crosswise imports in `main.py:1-2` mean the code runs correctly —
  nothing fails at runtime — so the trap is silent; there is no error
  signal that the vocabulary is inverted.
- With no tests or checks present, the inversion can persist indefinitely,
  and any future normalization (rename or move) could break `main.py:1-2`
  with nothing catching it.
- If this repository is used as an evaluation fixture (its name and
  minimalism strongly suggest so), this drift is precisely the behavior an
  analysis tool must detect to be trustworthy: trusting directory names
  over contents yields a wrong architecture story and a wrong
  recommendation.

## 10. Candidate next steps
1. Normalize the layout: move `handle()` into `handlers/user.py` and `User`
   into `models/user.py` (or rename the directories to truthful names, e.g.
   `data/` + `api/`), and update the two imports in `main.py:1-2`.
2. Add a smoke test (`python main.py` runs and prints both symbols) and/or
   a minimal pytest so the entry-point contract is executable.
3. Expand `README.md` beyond the title: purpose, structure, entry point, and
   an explicit responsibilities mapping for each module.
4. Add one-line docstrings to both modules/packages so the boundary is
   self-documenting even before any rename.
5. Add a structural check (lint rule or test) asserting `handlers/` contains
   no class definitions and `models/` contains no functions, to enforce the
   chosen naming contract.

## 11. Recommended next step
Normalize the layout first (candidate 1): move `handle()` to
`handlers/user.py`, move `User` to `models/user.py`, update the two imports
at `main.py:1-2`, and verify with `python main.py`. This is the smallest
change that removes the trap at its source; documentation-only fixes
(candidates 3 and 4) would merely describe the inverted layout rather than
repair it. Follow up by expanding the README once the layout is truthful.

## 12. Recommended workflow
`architecture-implementation-workflow` from
`skills/workflow-planner/references/workflow-registry.yaml` — "For
architecture/refactoring problems. Aligns domain, creates refactoring spec,
decomposes into issues, and implements via TDD." This is the registry entry
that matches an `architecture_fog` diagnosis whose remedy is a structural
refactor, and it is the closest alternative to the UI/product/docs
implementation workflows, all of which target fog types ruled out above.
Recommended execution mode: `guided_execution` — the only non-autonomous mode
this workflow allows (its `allowed_execution_modes` are `guided_execution`
and `autonomous_execution`; `plan_only` is not offered for it, so per the
registry-grounding rule it must not be recommended here). Recommending the
workflow with an allowed mode is a diagnostic handoff, not an execution; no
implementation is performed by this brief.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-misleading-dirs
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "main.py (L1-L2): entry point imports User from handlers.user and handle from models.user - crosswise wiring"
  - "handlers/user.py (L1-L2): handlers/ contains class User (a data model), no handler code"
  - "models/user.py (L1-L2): models/ contains def handle(request), the request handler"
  - "README.md (L1): README is only the title '# misleading-dirs'; no orientation"
  - "handlers/__init__.py: empty package marker (0 bytes) - no boundary documentation"
  - "models/__init__.py: empty package marker (0 bytes) - no boundary documentation"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Vocabulary Drift between package directory names (handlers/, models/) and module contents
weakness_type: Vocabulary Drift
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
> Plan an `architecture-implementation-workflow` run in `guided_execution`
> mode for the repository at
> `experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-misleading-dirs`,
> based on its repository sensemaking brief. Diagnosis: `architecture_fog`
> with weakest boundary `Vocabulary Drift` — package names invert contents
> (`handlers/user.py` holds `class User`, `models/user.py` holds `def
> handle`, and `main.py:1-2` imports them crosswise). Produce a refactoring
> specification that (1) normalizes the layout so directory names match
> contents (move `handle` into `handlers/user.py` and `User` into
> `models/user.py`, or rename the directories), (2) updates the imports in
> `main.py`, (3) adds a smoke test verifying `python main.py` prints both
> symbols, and (4) expands README.md to document the actual module
> responsibilities. Decompose this into implementation issues and agent
> briefs, but do not implement anything — return the orchestration plan
> only.
