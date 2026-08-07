# Repository Sensemaking Brief — hidden-coupling

## 1. Repository goal
`hidden-coupling` is a minimal Python example whose apparent purpose is to
demonstrate two small, independent modules: `a` (writes a token) and `b`
(reads a token back). The README (`README.md:3`) states this explicitly:
"Modules a and b are independent." The de-facto behavior, however, is a
shared-state demo: `main.py:4-5` runs `a.init()` and then `print(b.use())`,
where `a.init()` writes into a module-global `STATE` dict (`a.py:4`) and
`b.use()` reads that same dict back (`b.py:4`). The stated goal (independence)
and the actual behavior (coupling through a shared global) disagree.

## 2. Current shape
The repository contains exactly five files:

```
hidden-coupling/
├── README.md     (3 lines: title + one-line claim "Modules a and b are independent.")
├── a.py          (4 lines: imports STATE from registry; init() sets STATE['token'] = 'abc')
├── b.py          (4 lines: imports STATE from registry; use() returns STATE.get('token'))
├── main.py       (5 lines: imports a and b; calls a.init(); prints b.use())
└── registry.py   (1 line: STATE = {})
```

Structurally notable: `registry.py:1` is the only shared module — both `a.py:1`
and `b.py:1` import `STATE` from it. There are no tests, no package metadata,
no docs beyond the README, and no other modules.

## 3. Strong signals
- **Single-responsibility modules**: `a.py:3-4` (write token) and `b.py:3-4`
  (read token) each do one small, readable thing.
- **A working end-to-end path exists**: `main.py:4-5` shows the intended call
  sequence (`a.init()` then `b.use()`) and the demo runs.
- **No external dependencies**: the entire program is three Python modules plus
  a one-line registry — no third-party packages, no environment assumptions.
- **Explicit shared-state container**: `registry.py:1` (`STATE = {}`) is at
  least a single, named place where the shared state lives, rather than
  globals scattered across modules.

## 4. Missing pieces
- **No declared initialization-order contract**: nothing states that `a.init()`
  must run before `b.use()`. `b.py:4` reads `STATE.get('token')`, which
  silently returns `None` if `a.init()` was never called — the ordering
  requirement exists only as an accident of `main.py:4-5`.
- **No validation of the shared state**: `b.py:4` never checks that
  `STATE['token']` exists or has the expected type; an uninitialized read is
  indistinguishable from a legitimate `None` value.
- **No tests**: nothing asserts the init→use sequence, the failure mode, or
  the README's independence claim.
- **The README's core claim is unsupported**: `README.md:3` asserts module
  independence, which the code contradicts (`a.py:1`, `b.py:1` both import the
  same `registry.STATE`), and no documentation describes the actual coupling.

## 5. Improvement opportunities
- Replace the shared mutable global with explicit data flow: have `a.init()`
  return the token and `b.use(token)` accept it as a parameter, making the
  dependency visible in the call graph.
- If shared state must stay, add a guard in `b.use()` that raises a clear
  error (e.g. `RuntimeError("token not initialized")`) instead of silently
  returning `None`.
- Add a minimal test file covering both the happy path (`a.init()` then
  `b.use()`) and the uninitialized case.
- Correct `README.md:3` so the documentation describes the real module
  boundary (either actual independence after the refactor, or the actual
  coupling).
- Move `STATE` ownership into a small class or factory so the lifecycle
  (create → write → read) is explicit rather than implicit module state.

## 6. Weakest boundary
The weakest boundary is the **undeclared runtime dependency between modules
`a` and `b`**: `b.use()` silently depends on `a.init()` having executed first,
mediated through the shared mutable global `STATE` in `registry.py`. Nothing in
the code defines or validates this dependency: `a.py:4` writes
`STATE['token'] = 'abc'` into the global, `b.py:4` reads it back with
`STATE.get('token')` (returning `None` if unset), and the only thing enforcing
the correct order is the call sequence in `main.py:4-5`. The README actively
misdescribes the boundary — `README.md:3` claims the modules are independent —
so a reader is actively steered away from the coupling that actually exists.

Logic trace: `registry.py:1` defines a single global `STATE = {}`; `a.py:1`
imports it and `a.py:4` writes `STATE['token']`; `b.py:1` imports the same
object and `b.py:4` reads `STATE.get('token')` — so the two modules share a
mutable data dependency by construction. `b.py:4` uses `.get()`, which returns
`None` when the key is absent, so the read side never fails loudly when the
write side has not run; the only place the correct order is established is
`main.py:4-5`. Every link in this chain (shared object, write-before-read
ordering, presence of the key) is implicit — none is declared in an interface
or validated at runtime — and `README.md:3` ("Modules a and b are
independent.") contradicts the dependency graph outright. That is precisely
the Implicit Dependencies weakness class: behavior that depends on
files/state/ordering that are neither explicitly defined nor validated.

**Weakness type:** Implicit Dependencies

## 6.5. Problem classification (fog type)
**architecture_fog** — the primary uncertainty is structural: module coupling
through shared mutable state and an unenforced call-order boundary. This is
the textbook architecture_fog signal ("module boundaries unclear, coupling,
state management scattered" per `skills/repo-sensemaker/SKILL.md:29`), not any
other fog type:

- Not `ui_fog`: the repository contains no frontend code whatsoever (no
  React/Vue/HTML/CSS), so per the UI Fog Signals Registry decision tree
  (`references/ui-fog-signals.md:156-157`) the answer is "NO → Not ui_fog;
  check other fog types".
- Not `product_fog`: there is no ambiguity about what the program should do —
  the write-then-read behavior is fully specified by the code.
- Not `docs_fog`: the README is short but the root problem is not missing
  documentation; it is the hidden coupling itself (the misleading README line
  is a *symptom* of the undocumented boundary, not the primary blocker).

## 7. Evidence
The diagnosis rests on five cited observations:

1. `registry.py:1` (`STATE = {}`) — a single module-level mutable dict is the
   only state container, shared by both modules.
2. `a.py:4` (`STATE['token'] = 'abc'`) — the write side: `a.init()` mutates
   the shared global; nothing declares that this must happen before `b.use()`.
3. `b.py:4` (`return STATE.get('token')`) — the read side: `.get()` silently
   returns `None` when the write has not happened, so the missing dependency
   produces a silent wrong answer instead of an error.
4. `main.py:4-5` (`a.init()` then `print(b.use())`) — the only enforcement of
   the init-before-use ordering is this call sequence; no module or test
   encodes the contract.
5. `README.md:3` ("Modules a and b are independent.") — the documentation
   asserts independence, directly contradicting the import graph (`a.py:1`,
   `b.py:1` both import `registry.STATE`), so the boundary is not merely
   implicit — it is actively misdescribed.

Logic trace: `registry.py:1` creates one global object; `a.py:1` and `b.py:1`
both import that same object, so modules `a` and `b` are coupled through
shared mutable state no matter what any comment or doc says. The write
(`a.py:4`) and the read (`b.py:4`) are correct only when ordered init→use, and
`b.py:4`'s `.get()` turns a violated order into a silent `None` rather than a
detectable failure. Since `main.py:4-5` is the only place the order is
established and nothing validates the state's presence, the repository's
behavior depends on an implicit, unvalidated dependency — and `README.md:3`
denies that dependency exists. The weakest point of the repo is therefore the
undeclared `a`→`b` runtime coupling, which is exactly the Implicit Dependencies
weakness type.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: registry.py
    lines: L1
    quote: "STATE = {}"
    supports_claim: "A single shared mutable global is the only state container; neither module owns or declares it."
  - file: a.py
    lines: L4
    quote: "STATE['token'] = 'abc'"
    supports_claim: "a.init() writes into the shared global — the write side of the hidden coupling, with no declared precondition."
  - file: b.py
    lines: L4
    quote: "return STATE.get('token')"
    supports_claim: "b.use() reads the shared global via .get(), silently returning None if a.init() has not run — the unvalidated read side."
  - file: main.py
    lines: L4-L5
    quote: "a.init()\nprint(b.use())"
    supports_claim: "The only enforcement of init-before-use ordering is this accidental call sequence in main.py; no contract or test encodes it."
  - file: README.md
    lines: L3
    quote: "Modules a and b are independent."
    supports_claim: "The README asserts module independence, which the import graph and shared STATE contradict — the boundary is misdescribed."
```

## 9. Why this boundary matters
If the hidden coupling stays implicit, every future change is a landmine:
reordering `main.py:4-5`, calling `b.use()` from a new entry point, or
"cleaning up" `registry.py` will silently change behavior — `b.use()` returns
`None` instead of the token with no error raised. A developer who trusts
`README.md:3` ("Modules a and b are independent.") will treat the modules as
reorderable and independently testable, exactly the assumptions the coupling
violates. Because there are no tests (`ls` shows no test files), the silent
failure is guaranteed to ship unobserved. For a fixture whose entire content
is the relationship between these two modules, the undeclared dependency is
the whole repository at risk.

## 10. Candidate next steps
1. Make the dependency explicit: change `a.init()` to return the token and
   `b.use(token)` to take it as a parameter, removing the shared
   `registry.STATE` global (or pass `STATE` explicitly).
2. Add a hard failure for the uninitialized case: have `b.use()` raise (e.g.
   `KeyError`/`RuntimeError`) when `STATE['token']` is absent, instead of
   `.get()` returning `None`.
3. Add a test file covering the happy path (`a.init()` then `b.use()`) and the
   use-before-init failure mode.
4. Fix `README.md:3` so the documentation matches the real boundary after the
   refactor (state the actual coupling or the now-true independence).
5. Run the change through `architecture-implementation-workflow` so the
   refactor is specified and reviewed rather than applied ad hoc.

## 11. Recommended next step
Eliminate the implicit dependency at its root: have `a.init()` return the
token and `b.use(token)` accept it as a parameter (dropping the
`registry.STATE` global entirely, or passing `STATE` explicitly through
`main.py:4-5`), and add a guard so a missing token raises instead of returning
`None`. This is the smallest change that converts the hidden write→read
coupling into a visible, testable contract, and it immediately makes
`README.md:3`'s independence claim either true (if the global is removed) or
obviously false (if state is passed explicitly) — unblocking the doc fix and
the tests on top of it.

## 12. Recommended workflow
`architecture-implementation-workflow` — defined in
`skills/workflow-planner/references/workflow-registry.yaml:848` as "For
architecture/refactoring problems. Aligns domain, creates refactoring spec,
decomposes into issues, and implements via TDD." It matches this diagnosis:
the weakest boundary is structural (module coupling and state ownership), not
product, UI, or docs. (`implementation-workflow` at
`workflow-registry.yaml:587` is the generic fallback but is less specific to
this refactor shape.)

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/hidden-coupling
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
timestamps:
  created_at: "2026-08-07T00:00:00Z"
  analyzed_at: "2026-08-07T00:00:00Z"
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "registry.py:1: STATE = {} — shared mutable global coupling modules a and b"
  - "a.py:4: a.init() writes STATE['token'] into the shared global with no declared precondition"
  - "b.py:4: b.use() reads STATE.get('token'), silently returning None if a.init() has not run"
  - "main.py:4-5: a.init() then print(b.use()) — the call sequence is the only enforcement of the hidden ordering contract"
  - "README.md:3: claims 'Modules a and b are independent.' — contradicted by the import graph and shared STATE"
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
> Run workflow `architecture-implementation-workflow` with
> `context_artifacts = [this repository_sensemaking_brief]` for repository
> `hidden-coupling`. Scope: make the hidden coupling between `a` and `b`
> explicit without changing observable behavior — replace the shared mutable
> `registry.STATE` global with explicit data flow (`a.init()` returns the
> token, `b.use(token)` takes it as a parameter), make the uninitialized case
> fail loudly instead of returning `None`, add a test covering init→use and
> use-before-init, and correct `README.md`'s independence claim to match the
> actual module boundary. Produce the refactoring spec and issue
> decomposition; do not add features or external dependencies.
