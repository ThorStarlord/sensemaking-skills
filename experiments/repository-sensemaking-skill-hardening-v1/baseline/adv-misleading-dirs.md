# Repository Sensemaking Brief

## 1. Repository goal
This is a minimal Python fixture repository whose only behavior is an entry
point that imports and prints two symbols: a `User` class and a `handle`
function (`main.py:1-3`). The evident purpose — signaled by the README title
`# misleading-dirs` (README.md:1) and by the layout itself — is to present a
codebase whose package directory names (`handlers/`, `models/`) invert the
conventional meaning of their contents: the request-handling function lives
under `models/` and the data model class lives under `handlers/`. In plain
terms, the repo is a demonstration/trap fixture: it exists to test whether a
reader (human or tool) trusts directory-name semantics over actual file
contents. No product surface, user features, or real workload are present.

## 2. Current shape
- `README.md` — 1 line (19 bytes): only the heading `# misleading-dirs`; no
  purpose, structure, usage, or run instructions.
- `main.py` — 3 lines: `from handlers.user import User`,
  `from models.user import handle`, `print(User, handle)` — the single entry
  point, wiring the two packages crosswise.
- `handlers/__init__.py` — 0 bytes (empty package marker).
- `handlers/user.py` — 2 lines: `class User:` / `pass` (a data-model class
  living in the "handlers" package).
- `models/__init__.py` — 0 bytes (empty package marker).
- `models/user.py` — 2 lines: `def handle(request):` / `return 'handled'`
  (request-handling logic living in the "models" package).
- No tests, no configuration files, no documentation directory, no CI, no
  git metadata visible in the fixture.

## 3. Strong signals
- The code is tiny and readable: every source file is 1–3 lines, so the
  inverted layout is discoverable by opening the four files.
- The entry point's imports are not dead: both symbols imported at
  `main.py:1-2` are actually defined (`handlers/user.py:1`, `models/user.py:1`),
  so the package runs as-is — the inversion is semantic, not mechanical.
- Within-file naming is consistent (`user.py` under `handlers` defines
  `User`; `user.py` under `models` defines `handle`); the drift is at the
  package-name layer, not inside modules.
- There is exactly one entry point (`main.py`), with no hidden dispatch or
  indirection to confuse analysis further.

## 4. Missing pieces
- Any README content beyond the bare title: no purpose statement, no
  structure map, no run instructions, no responsibilities table.
- Package boundary documentation: both `__init__.py` files are empty (0
  bytes) and neither module has a docstring, so nothing states what
  `handlers/` or `models/` is supposed to contain.
- Tests or any automated check that would either document the actual
  contract (e.g., a smoke test asserting `python main.py` prints both
  symbols) or catch the naming/content inversion.
- A truthful mapping between package names and responsibilities — the
  repository contains no statement of intent at all, so the inversion is
  completely unanchored.

## 5. Improvement opportunities
- Add one-line docstrings to `handlers/user.py` and `models/user.py`
  describing actual responsibilities, so the boundary is self-documenting
  even before any rename.
- Add a smoke test (pytest or a plain `python main.py` run in CI) so the
  entry-point contract is executable and regressions are caught.
- Expand README.md into a short orientation: purpose, entry point, and a
  per-module responsibilities note.
- Consider a structural lint rule (e.g., assert `handlers/` contains no
  class definitions and `models/` contains no functions) to enforce
  whatever naming contract is eventually chosen.

## 6. Weakest boundary
The weakest boundary is the vocabulary drift between the package directory
names and the code they actually contain. Conventionally, `handlers/` is the
home of request-handling logic, but `handlers/user.py:1-2` contains only a
`User` data class; conventionally, `models/` is the home of data models, but
`models/user.py:1-2` contains the `handle(request)` function. The entry
point `main.py:1-2` imports them crosswise (`User` from `handlers`, `handle`
from `models`). Any reader or analysis tool that navigates by package-name
semantics will open the wrong module for each concern, and nothing in the
repository corrects that misimpression: README.md:1 is only a title, and
both `__init__.py` markers are empty. The naming vocabulary the repository
presents (`handlers` = handling, `models` = data) does not match the
semantics the code delivers, and no documentation, docstring, or test
exists to bridge or enforce the gap.

**Weakness type:** Vocabulary Drift

## 6.5. Problem classification (fog type)
`architecture_fog` — the operative problem is at the module-boundary /
structure layer: package names mislabel module contents, so the boundaries a
reader must rely on are untrustworthy. This is precisely "code structure
problems, design issues, unclear boundaries." `ui_fog` is ruled out because
the repository contains no frontend code of any kind (the complete file
listing is six Python files — no HTML, CSS, JS, TSX, or routing). `product_fog`
is ruled out because there are no user-need artifacts, feature specs, or
analytics — there is no product surface at all. `docs_fog` is a contributing
factor (the README is a bare title and `__init__.py` files are empty), but
documentation alone would only describe the inverted layout, not repair it;
the primary defect is structural naming, which is an architecture concern.

## 7. Evidence
- `main.py:1-2` — `from handlers.user import User` / `from models.user
  import handle`: the entry point expects the "handlers" package to provide
  a model class and the "models" package to provide a handler function.
- `handlers/user.py:1-2` — contains only `class User:` / `pass`: the
  "handlers" package contains no handler code.
- `models/user.py:1-2` — contains only `def handle(request):` /
  `return 'handled'`: the "models" package contains the request handler.
- `README.md:1` — the entire README is the single line `# misleading-dirs`.
- `handlers/__init__.py` and `models/__init__.py` — 0 bytes each: empty
  package markers that document no boundary.

**Logic trace:** `main.py:1-2` establishes the naming contract the author
chose: `User` is imported from `handlers.user` and `handle` from
`models.user`. Opening `handlers/user.py:1` shows the handlers package
contains a class, and opening `models/user.py:1` shows the models package
contains a function — i.e., the package vocabulary (`handlers` = request
handling, `models` = data) is inverted relative to the code's actual
semantics. A reader navigating by convention therefore cannot locate the
request handler or the data model without opening both modules, and neither
README.md:1 (a bare title) nor the empty `__init__.py` markers provides any
corrective documentation. Because the defect sits in the naming/boundary
layer of the structure — not in missing product specs and not in any UI
surface — the weakest boundary is Vocabulary Drift and the fog type is
architecture_fog. The repository also contains no tests or lint config at
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
  - file: handlers/user.py
    lines: L1
    quote: "class User:"
    supports_claim: "The handlers/ package contains a data-model class, not request-handling code."
  - file: models/user.py
    lines: L1
    quote: "def handle(request):"
    supports_claim: "The models/ package contains the request-handling function."
  - file: README.md
    lines: L1
    quote: "# misleading-dirs"
    supports_claim: "README is only a bare title with no orientation about purpose or structure."
  - file: handlers/__init__.py
    lines: L1
    quote: ""
    supports_claim: "Empty package marker — no boundary documentation in the handlers package."
  - file: models/__init__.py
    lines: L1
    quote: ""
    supports_claim: "Empty package marker — no boundary documentation in the models package."
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
2. Expand README.md beyond the title: purpose, structure, entry point, and
   an explicit responsibilities mapping for each module.
3. Add a smoke test (`python main.py` runs and prints both symbols) and/or
   a minimal pytest so the entry-point contract is executable.
4. Add one-line docstrings to both packages/modules so the boundary is
   self-documenting even before any rename.
5. Add a structural check (lint rule or test) asserting `handlers/` contains
   no class definitions and `models/` contains no functions, to enforce the
   chosen naming contract.

## 11. Recommended next step
Normalize the layout first (candidate 1): move `handle()` to
`handlers/user.py`, move `User` to `models/user.py`, update the two imports
at `main.py:1-2`, and verify with `python main.py`. This is the smallest
change that removes the trap at its source; documentation-only fixes
(candidates 2 and 4) would merely describe the inverted layout rather than
repair it. Follow up by expanding the README once the layout is truthful.

## 12. Recommended workflow
`architecture-implementation-workflow` from `workflow-registry.yaml` — "For
architecture/refactoring problems. Aligns domain, creates refactoring spec,
decomposes into issues, and implements via TDD." This is the registry entry
that matches an architecture_fog diagnosis whose remedy is a structural
refactor. Recommended execution mode: `plan_only` — the sensemaking brief is
a diagnostic artifact, and the refactor should be planned (spec + issues)
before any implementation.

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
  - "README.md (L1): README is only a bare title; no orientation"
  - "main.py (L1-L2): entry point imports User from handlers and handle from models (crosswise)"
  - "handlers/user.py (L1): handlers/ contains a model class, not handler code"
  - "models/user.py (L1): models/ contains the handle() function"
  - "handlers/__init__.py (L1): empty package marker"
  - "models/__init__.py (L1): empty package marker"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: plan_only
weakest_boundary: Vocabulary Drift between package directory names (handlers/, models/) and module contents
weakness_type: Vocabulary Drift
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-06T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
> Plan an `architecture-implementation-workflow` run in `plan_only` mode for
> the repository at
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
