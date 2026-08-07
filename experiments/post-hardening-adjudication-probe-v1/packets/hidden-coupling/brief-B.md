# Repository Sensemaking Brief: hidden-coupling

## 1. Repository goal

The repository's only documented statement of purpose is README.md:3 — "Modules a and b are independent." The implied goal is a minimal Python example in which two modules, `a` and `b`, are independent of each other and orchestrated from a small entry point (`main.py`). This is a standalone fixture run (no user-intent artifact exists, GAP-8), so the goal is reconstructed from the repository itself: nothing else in the repo states what it is for.

## 2. Current shape

Inventory (5 files, no subdirectories, no manifests, no tests, no CI, no build configuration):
- `README.md` (3 lines) — the only documentation.
- `main.py` (5 lines) — the entry point.
- `a.py` (4 lines), `b.py` (4 lines) — the two "independent" modules.
- `registry.py` (1 line) — a single module-level global.

Runtime flow (architecture reconstruction):
- **Startup path**: `python main.py`. main.py:1-2 imports `a` and `b`; main.py:4-5 executes the entire program. There are no other entry points, no CLI, no package scripts.
- **Orchestration**: main.py:4 calls `a.init()`; main.py:5 calls `b.use()` and prints the result. Linear, two-step flow; nothing else controls the program.
- **Domain/core logic**: a.py:3-4 (`init`) writes a token into shared state; b.py:3-4 (`use`) reads it back.
- **Persistence/state**: the only state boundary is registry.py:1 (`STATE = {}`), a module-level mutable dict. It is written at a.py:4 (`STATE['token'] = 'abc'`) and read at b.py:4 (`STATE.get('token')`).
- **External integration points**: none — standard library only (`print`, dict). No files, databases, caches, queues, environment variables, or remote systems.
- **Background work**: none.
- **Output boundary**: stdout via main.py:5.
- **Where responsibility becomes unclear**: the boundary between `a` and `b`. Neither module imports the other (a.py has no reference to b; b.py has no reference to a), yet both silently share one global dict, and b assumes a key that only a's `init` creates. Nothing validates the handoff.

Dependency semantics (each claim classified):
- `registry` — **used** at runtime: imported at a.py:1 and b.py:1, and `STATE` is accessed at a.py:4 and b.py:4 on the proven execution path (main.py:4-5).
- `a` and `b` — **used**: imported at main.py:1-2, functions called at main.py:4-5.
- No manifest exists, so there are no `declared` dependencies, no `optional` ones, and no `dead` manifest entries.
- The critical claim: b's runtime result depends on `a.init()` having executed first (main.py:4 before main.py:5). This dependency is **implicit** — declared nowhere (no manifest, no doc, no interface); it exists only as a side effect on shared state.

Validation structure (Pass D): none. No tests, no assertions, no type hints, no input validation, no error handling. b.py:4's `STATE.get('token')` returns `None` (not an error) when the write has not happened.

## 3. Strong signals

- Single, obvious entry point and linear flow (main.py:1-5) — the runtime path is fully traceable; no hop is UNKNOWN.
- Centralized state location: all shared state lives in exactly one place, registry.py:1, which makes the coupling *discoverable* once looked for.
- Imports match usage (a.py:1, b.py:1, main.py:1-2) — no declared-but-unused modules, no dead code.
- The repository is tiny and free of generated artifacts, vendor trees, and lockfile noise — every file was inspected in full.

## 4. Missing pieces

- Any test or automated check: no test files, no test-framework declaration, no CI configuration (structural proof — the 5-file inventory contains no test artifact). The coupling contract is entirely unvalidated.
- Correct documentation of the data flow: README.md:3 asserts the opposite of what the code does (see Section 6).
- An explicit contract for init order / key presence: b.py:4 uses `STATE.get('token')`, which silently yields `None` if a.init() (a.py:4) has not run.
- Packaging/build metadata (pyproject.toml, setup.py, requirements.txt): nothing declares how to run, install, or test the repo.

## 5. Improvement opportunities

- Add a test that pins the init-then-use ordering (main.py:4-5 behavior) and one that documents the use-without-init failure (`None`) — cheap and locks in the contract.
- Replace the global-state handoff with explicit wiring: `a.init()` returns the token and `b.use(token)` takes it as a parameter, making the coupling visible in the call graph.
- Correct README.md:3 to describe the actual `registry.STATE` handoff.
- Add a guard in `b.use()` that fails loudly when the token is absent, instead of returning `None`.
- Add type hints and a minimal `pyproject.toml` so the modules can be declared, checked, and tested.

## 6. Weakest boundary

Candidate generation and scoring (evidence strength / severity / blast radius / goal relevance / downstream blocking / uncertainty):

1. **Documented independence contract vs. actual shared-state coupling** (README.md:3 vs a.py:1, a.py:4, b.py:1, b.py:4, registry.py:1). evidence_strength: strong (verbatim contradiction); severity: medium (no crash, but every refactor is unsafe); blast_radius: high (the repo's only documented statement); goal_relevance: high (the repo's sole stated goal is independence); downstream_blocking_effect: high (any change to a, b, registry, or main made on the false premise breaks silently); uncertainty: low.
2. **Implicit b→a runtime dependency (init-order contract)** (main.py:4-5, b.py:4, a.py:4). evidence_strength: strong (direct code); severity: high (b.use() silently returns None without a.init()); blast_radius: high (whole data flow); goal_relevance: high (it is the coupling itself); downstream_blocking_effect: high (reordering or editing either module risks silent breakage); uncertainty: low-medium.
3. **Zero validation of the coupling contract** (no tests or checks anywhere). evidence_strength: medium (absence — structural proof from the inventory); severity: medium; blast_radius: medium; goal_relevance: medium; downstream_blocking_effect: medium; uncertainty: medium.
4. **Ghost Features** — rejected at generation: nothing is documented as a feature without implementation; the code exists and runs (a.py:4, b.py:4). Per the GAP-6 taxonomy mapping, Ghost Features requires a documented surface with no reachable implementation; here the docs misdescribe existing code, which maps to Vocabulary Drift — never Ghost Features.

Selection: Candidate 1. It has the strongest direct evidence (a verbatim contradiction between the README and every code file involved), the lowest uncertainty, and it is the boundary that blocks all downstream work: no safe change to a, b, registry, or main is possible while the documented contract actively denies the coupling. Candidate 2 is the mechanism behind Candidate 1 and is recorded as the strongest alternative.

```text
Boundary: the documented module-independence contract vs. the actual shared-state
coupling between a and b — claim at README.md:3, implementation at a.py:1/4,
b.py:1/4, registry.py:1, orchestrated by main.py:4-5.
Observed contract: "Modules a and b are independent." (README.md:3)
Observed violation or uncertainty: a.py:1 and b.py:1 both import the SAME
registry.STATE object (registry.py:1); a.py:4 writes STATE['token'] and b.py:4
reads STATE.get('token') — a and b are coupled through shared mutable global
state, and b's output depends on a.init() having run first (main.py:4-5).
Evidence: README.md:3; a.py:1; a.py:4; b.py:1; b.py:4; registry.py:1; main.py:4-5.
Weakness type: Vocabulary Drift
Logic trace: README.md:3 states "Modules a and b are independent." a.py:1
(`from registry import STATE`) and b.py:1 (`from registry import STATE`) both
import the identical state object defined at registry.py:1 (`STATE = {}`).
a.py:4 mutates that object (`STATE['token'] = 'abc'`) and b.py:4 reads it
(`return STATE.get('token')`), with main.py:4-5 fixing the order in which the
two run. Therefore the code, not the docs, determines the relationship: a and b
are coupled through a shared mutable global and a hidden init-order dependency.
The README's central claim is false. The code exists and runs, so this is
documentation misdescribing existing code, which the GAP-6 taxonomy mapping
assigns to Vocabulary Drift (never Ghost Features).
Failure consequence: a developer or agent acting on README.md:3 will treat a
and b as independently changeable — renaming STATE['token'], removing
a.init(), reordering main.py:4-5, or giving b its own state — and the failure
is silent: b.use() returns None and main.py:5 prints None with no error raised.
Confidence: high — the contradiction is directly observable in verbatim text
(README.md:3 vs a.py:1, b.py:1, registry.py:1). Nothing further would raise
it; executing `python main.py` would only confirm the derived runtime behavior.
Alternatives considered: (1) Implicit Dependencies — the hidden init-order
dependency of b on a (main.py:4-5, b.py:4, a.py:4) is the mechanism behind the
contradiction and scored highest on severity; it lost the selection because the
most observable, lowest-uncertainty boundary failure is the false documented
contract, and the GAP-6 mapping directs docs-misdescribing-existing-code to
Vocabulary Drift; it is recorded as the secondary weakness in the Logic trace
and Section 6.5. (2) Zero Validation — real but weaker: absence of tests in a
5-file fixture is structural proof, not a direct contradiction. (3) Ghost
Features — rejected per GAP-6: no documented surface lacks an implementation.
(4) Contract Mismatch — rejected: no file claims a format it does not have.
```

**Weakness type:** Vocabulary Drift

## 6.5. Problem classification (fog type)

The primary fog type is **architecture_fog**: the repository exhibits unsafe coupling through shared global state (registry.py:1), an implicit dependency chain (a.py:4 writes what b.py:4 reads via `registry.STATE`), and lifecycle/state ambiguity (b's correctness depends on a.init() having run, main.py:4-5). The defect is structural: even if README.md:3 were corrected to describe the coupling, the fragility (silent None, unenforced ordering) would remain — the mismatch between docs and code lives in the structure, not merely in the documentation layer.

Secondary fog: **docs_fog** (contributing) — README.md:3 misdescribes existing code, which is a documentation defect, but it is the symptom of the hidden coupling, not the root cause.

Not ui_fog: the repository contains no frontend code (no React/Vue/Angular/HTML/CSS), so the UI Fog Signals Registry decision tree stops at step 1 (no frontend → not ui_fog). Not product_fog: the README makes no feature promise — "independent" is a structural claim about existing, working code, and there is no unimplemented deliverable (not Ghost Features).

## 7. Evidence

The central contradiction is documented at README.md:3, which states "Modules a and b are independent." The code contradicts this in every relevant file: a.py:1 (`from registry import STATE`) and b.py:1 (`from registry import STATE`) both import the same global state object defined at registry.py:1 (`STATE = {}`); a.py:4 writes `STATE['token'] = 'abc'` and b.py:4 reads `return STATE.get('token')`. The orchestration that makes the hidden dependency concrete is main.py:4-5 (`a.init()` then `print(b.use())`): b's result depends on a's side effect having executed first. No tests or validation exist anywhere in the repository (the 5-file inventory contains no test artifact and no CI or build configuration), so the coupling contract is unenforced; b.py:4's `STATE.get('token')` silently returns None when the ordering is violated.

Logic trace: The README's only substantive statement (README.md:3) asserts module independence. a.py:1 and b.py:1 import the identical mutable object from registry.py:1; a.py:4 mutates it and b.py:4 reads it; main.py:4-5 fixes their execution order. From these observed facts it follows (DERIVED) that a and b are coupled through shared global state with a hidden init-order dependency, so the documented contract is false while the code is fully implemented and runnable (OBSERVED: all five files read in full). Because the code exists and runs, the failure mode is docs misdescribing existing code — mapped by the GAP-6 taxonomy to Vocabulary Drift. The consequence (b.use() → None when init order is violated, printed at main.py:5) is DERIVED directly from b.py:4's use of `.get()` with no default. No hop in the runtime path is UNKNOWN; the only UNKNOWN for this fixture is the absence of any stated user intent beyond the README (nothing in the repo documents a problem statement, feature list, or roadmap).

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Modules a and b are independent."
    supports_claim: README documents a and b as independent — the contract the code contradicts.
  - file: a.py
    lines: L1
    quote: "from registry import STATE"
    supports_claim: a imports the shared state object from registry.
  - file: a.py
    lines: L4
    quote: "    STATE['token'] = 'abc'"
    supports_claim: a writes into the shared STATE on init — the write side of the coupling.
  - file: b.py
    lines: L1
    quote: "from registry import STATE"
    supports_claim: b imports the SAME shared state object — the modules are not independent.
  - file: b.py
    lines: L4
    quote: "    return STATE.get('token')"
    supports_claim: b reads the token written by a; .get() silently returns None if a.init() has not run.
  - file: registry.py
    lines: L1
    quote: "STATE = {}"
    supports_claim: the single global mutable state boundary shared by a and b.
  - file: main.py
    lines: L4-L5
    quote: "a.init()\nprint(b.use())"
    supports_claim: orchestration fixes init-then-use ordering; the b→a dependency is never declared.
```

## 9. Why this boundary matters

While the documented contract stays false, every downstream actor — human or agent — operates on a wrong model of the system. The coupling is "hidden" precisely because the README denies it and because a and b never import each other, so reading a.py or b.py alone reveals nothing. Any refactor (renaming the token key, adding a second writer, reordering main.py:4-5, parallelizing init/use) breaks the other module silently: b.use() returns None and main.py:5 prints None. There is no test, no guard, and no documentation that would catch or explain the failure. The boundary is the single point where the repository's promise (independence) and its reality (hidden shared state) diverge, and it blocks all safe modification work.

## 10. Candidate next steps

1. Correct README.md:3 to describe the actual `registry.STATE` handoff (cheap; removes the false contract, but leaves the structural fragility in place).
2. Make the coupling explicit in code: `a.init()` returns the token and `b.use(token)` takes it as a parameter, removing the global-state handoff.
3. Add tests that pin the current contract: main flow prints the token; use-without-init yields None (documents the failure mode before changing behavior).
4. Add a loud guard in `b.use()` (raise/assert when the token is absent) so ordering violations fail visibly.
5. Add packaging metadata (`pyproject.toml`) and type hints so the modules can be declared, checked, and tested.

## 11. Recommended next step

The smallest concrete action with the highest leverage: make the a↔b handoff explicit and pin it with one test — replace the implicit global-state handoff (`a.init()` writes `registry.STATE['token']` at a.py:4; `b.use()` reads it at b.py:4) with an explicit value handoff (`a.init()` returns the token; `b.use(token)` takes it), and add a test asserting the main flow (main.py:4-5) prints the token. This makes the hidden coupling visible in the call graph, re-validates the README's independence claim in a corrected form, and creates the safety net that is currently entirely absent. Recommended path for that work: the architecture-implementation-workflow in guided_execution mode (Section 12).

## 12. Recommended workflow

**architecture-implementation-workflow** — ID verified against `skills/workflow-planner/references/workflow-registry.yaml`, which lists it with purpose "For architecture/refactoring problems" and `allowed_execution_modes: [guided_execution, autonomous_execution]` (requires_run_log: true). Rationale: the primary fog type is architecture_fog (unsafe coupling, implicit dependency chain, lifecycle ambiguity), and this workflow aligns the domain, creates a refactoring spec, decomposes into issues, and implements via TDD — the shape this fix needs. Closest alternatives rejected: docs-implementation-workflow would only correct README.md:3 and leave the structural fragility (silent None, unenforced ordering) in place; ui-implementation-workflow and product-implementation-workflow do not apply (no frontend, no product contract); implementation-workflow (generic default) is a valid fallback but the architecture-specific workflow matches better. Preconditions before it can run: its required initial inputs are context_artifacts (which normally include the user-intent artifact); this standalone fixture run provides only repository_state, so a user_intent artifact must be added by the runtime. Execution mode is guided_execution — one of the workflow's allowed modes; recommending it is a diagnostic handoff, not execution (No Implementation boundary).

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/hidden-coupling
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: null
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (L3): documents 'Modules a and b are independent' — contradicted by the shared-state coupling"
  - "a.py (L1, L4): imports registry.STATE and writes STATE['token']"
  - "b.py (L1, L4): imports registry.STATE and reads STATE.get('token')"
  - "registry.py (L1): module-level global STATE = {} shared by a and b"
  - "main.py (L4-L5): a.init() must run before b.use(); the ordering contract is implicit"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Vocabulary Drift
weakness_type: Vocabulary Drift
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
timestamps:
  created_at: "2026-05-19T16:00:00Z"
created_at: "2026-05-19T16:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

> Repository sensemaking brief for `hidden-coupling` (standalone fixture run; no user-intent artifact — set `user_implied_fog_type: unknown`). Primary fog type: **architecture_fog** (secondary: docs_fog). Weakest boundary: **Vocabulary Drift** — README.md:3 claims "Modules a and b are independent" while a.py:1/4 and b.py:1/4 both use the shared global `STATE` from registry.py:1, and b.use() depends on a.init() having run (main.py:4-5). Recommended workflow: **architecture-implementation-workflow** in **guided_execution** mode. First deliverable: a refactoring spec that (1) pins current behavior with a test (init-then-use prints the token; use-without-init returns None), (2) makes the a↔b handoff explicit (return/parameter instead of global state), and (3) updates README.md:3 to match the new contract. Required inputs: user_intent (add scope/goal) and repository_state (the 5-file corpus at experiments/repository-sensemaking-skill-hardening-v1/corpus/hidden-coupling).
