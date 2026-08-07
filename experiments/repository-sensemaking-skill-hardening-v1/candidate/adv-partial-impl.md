# Repository Sensemaking Brief — adv-partial-impl

## 1. Repository goal

`README.md:3` states the entire purpose of the repository in one line: "Implements report generation." (OBSERVED). The intended goal, reconstructed from the code (DERIVED), is a minimal Python program that reads a data file and produces a report: `main.py:3-4` invokes `generate_report('data.csv')` as the program's only action. The repository therefore promises one deliverable — a working report generator — and nothing else.

## 2. Current shape

**Inventory (complete — the repository is four files, all opened):** `README.md` (3 lines), `core.py` (2 lines), `main.py` (4 lines), `tests/test_core.py` (6 lines). There is no manifest (no `pyproject.toml`, `setup.py`, `requirements.txt`), no CI configuration, no `docs/`, no config, no lockfile (Pass A).

**Runtime flow (architecture reconstruction):**
- **Startup path:** `python main.py`. `main.py:3` (`if __name__ == '__main__':`) is the only bootstrap; `main.py:1` imports `core.generate_report` at module level.
- **Orchestration:** none beyond the direct call — `main.py:4` calls `generate_report('data.csv')` as the sole top-level action (OBSERVED).
- **Domain/core logic:** `core.py:1-2` — `def generate_report(path):` whose entire body is `raise NotImplementedError('report generation not implemented yet')`. There is no logic: the parameter `path` is never read, no data is parsed, nothing is computed, nothing is returned.
- **Persistence/state:** none. No files are written or read, no database, no cache, no environment variables, no global state.
- **External integrations:** none. The only import is `from core import generate_report` (`main.py:1`; also repeated inside the test at `tests/test_core.py:4`), which is local, and `pytest` (`tests/test_core.py:1`).
- **Background work:** none.
- **Output boundary:** the only observable outcome of running the program is a `NotImplementedError` exception raised at `core.py:2`. No report ever leaves the system.
- **Dependency semantics:** `core` is *used* (imported at `main.py:1` and `tests/test_core.py:4`) but the function it provides is not *runtime*-exercised to completion — the exercised path raises. `pytest` is *used* by tests (`tests/test_core.py:1`) but *declared* nowhere: no manifest lists it, so it is an implicit environment dependency.
- **Boundary model:** the boundary "CLI/script → domain function" exists structurally (`main.py:4` → `core.py:1`) but is a boundary with no delivery: nothing is validated at it, and the callee is guaranteed to fail. The boundary "domain → output" does not exist at all.
- **Where responsibility becomes unclear:** the README assigns responsibility for report generation to the repository as a whole ("Implements report generation.", `README.md:3`), but no code anywhere discharges it; the only candidate, `core.py:1-2`, is an unconditional exception. A reader cannot tell whether the repo is "work in progress" (stub awaiting implementation) or "done" (README claim), because the README does not say — and the test actively encodes the failure state (see Pass E).

**Validation structure (Pass D):** exactly one test, `tests/test_core.py:3-6`, which asserts `generate_report('x')` raises `NotImplementedError` (`tests/test_core.py:5-6`). The only automated check in the repository validates that the feature does **not** work. No schema, no input validation, no assertion of any output contract exists anywhere.

## 3. Strong signals

- **A clean, conventional entry point:** `main.py:3-4` uses the standard `if __name__ == '__main__'` guard and names the intended call with a realistic argument (`'data.csv'`) — the invocation contract is unambiguous (OBSERVED).
- **A test harness exists:** `tests/test_core.py:1-6` is a real pytest file; minimal, but it means the repository has an executable verification path once real behavior lands.
- **Vocabulary is consistent:** the README term "report generation" matches the function name `generate_report` (`core.py:1`) and the call site (`main.py:4`) — there is no vocabulary drift or misleading naming.
- **The stub is honest about itself:** `core.py:2` fails loudly with a descriptive message ("report generation not implemented yet") rather than silently returning `None` or empty output, so a caller cannot mistake a no-op for a generated report.

## 4. Missing pieces

- **The implementation itself:** there is no code anywhere in the repository that reads `path`, parses `data.csv`, produces report content, or writes output — `core.py:2` is the sum total of the feature's code.
- **Input handling:** `generate_report(path)` accepts a path but never opens or reads it (`core.py:1-2`; the parameter is unused).
- **Output contract:** no defined report format, no return value, no destination — nothing specifies what "report generation" even produces.
- **Packaging metadata:** no manifest, so `pytest` is undeclared (`tests/test_core.py:1` uses it) and the top-level `from core import ...` import (`main.py:1`) only resolves when Python runs from the repository root — an implicit, unvalidated environment dependency.
- **Behavioral tests:** the only test pins the exception (`tests/test_core.py:5-6`); there is no test for any actual behavior because no behavior exists.
- **Status documentation:** nothing states whether the stub is intentional work-in-progress or a forgotten placeholder, so the README's present-tense "Implements" (`README.md:3`) reads as a completed claim.

## 5. Improvement opportunities

- Define the report output contract (format, destination, error handling for a missing input file) in a short README section before implementing — a one-paragraph spec would make the deliverable testable.
- Add a minimal `pyproject.toml` declaring `pytest` and enabling `pip install -e .`, which also fixes the CWD-dependent import (`main.py:1`).
- Once implementation lands, replace the `NotImplementedError`-pinning test (`tests/test_core.py:5-6`) with a behavior test (e.g. a sample CSV in, defined report out).
- Consider a `--output` argument or default output path in `main.py:3-4` so the CLI has a real surface.

## 6. Weakest boundary

**Candidate generation (scored):**

1. **README promise vs. missing implementation** — `README.md:3` ("Implements report generation.") vs. `core.py:2` (`raise NotImplementedError`), the only code for the feature; `main.py:4` makes the failure the program's sole behavior. evidence_strength: strong (direct file evidence on both sides) · severity: high (the repository's only deliverable can never work) · blast_radius: high (100% of the promised surface) · goal_relevance: high (it is the entire goal) · downstream_blocking_effect: high (nothing can be built on a feature that always raises) · uncertainty: low.
2. **Test codifies non-implementation** — `tests/test_core.py:5-6` asserts the stub raises, i.e. validation pins the absence of the feature. evidence_strength: strong · severity: medium · blast_radius: medium · goal_relevance: medium · downstream_blocking_effect: medium · uncertainty: low. This is a *symptom* of candidate 1, not an independent boundary.
3. **Implicit environment dependency** — `pytest` used but undeclared (`tests/test_core.py:1`), and `from core import ...` depends on CWD (`main.py:1`). evidence_strength: medium · severity: low · blast_radius: low (dev-environment only) · goal_relevance: low · downstream_blocking_effect: low · uncertainty: low.
4. **Zero packaging/build validation** — no manifest, no CI to check anything. evidence_strength: strong (absence observed across the full inventory) · severity: low · blast_radius: medium · goal_relevance: low · downstream_blocking_effect: low · uncertainty: low. Loses because there is nothing to validate yet; subsumed by candidate 3.

**Selection:** candidate 1 wins on every axis that matters — highest consequence, strongest evidence, total centrality to the goal, and it blocks all downstream work.

```text
Boundary:
The documented deliverable — "report generation" — versus the code that is
supposed to deliver it. README.md:3 promises the feature as implemented; the
only implementation surface, core.py:1-2, unconditionally raises
NotImplementedError, and the sole entry point (main.py:4) invokes it.

Observed contract:
"Implements report generation." (README.md:3) — a present-tense claim that the
repository delivers working report generation.

Observed violation or uncertainty:
The feature has no reachable implementation. core.py:2 raises
NotImplementedError as the function's entire body; no other file in the
repository implements any part of report generation (full four-file inventory,
OBSERVED); main.py:4 routes the program's only execution path into the
exception; and tests/test_core.py:5-6 assert the exception, codifying the
absence of the feature as the expected behavior.

Evidence:
README.md:3; core.py:1-2; main.py:4; tests/test_core.py:5-6.

Weakness type:
**Ghost Features**

Logic trace:
README.md:3 advertises report generation as implemented (OBSERVED). The only
code surface for that feature is core.py:1-2, whose entire body is `raise
NotImplementedError('report generation not implemented yet')` (OBSERVED) — no
code reads the input path, produces output, or returns a value. main.py:4
invokes the function as the program's sole action (OBSERVED), so the feature
is not merely unexercised: the only execution path is guaranteed to fail.
tests/test_core.py:5-6 codify that guarantee as the repository's only
automated check (OBSERVED). A documented product surface (the README) promises
functionality with no reachable implementation anywhere → Ghost Features per
the GAP-6 taxonomy mapping. Because the defect is the promise itself — the
README presents the deliverable as done while no code exists for it — and
because nothing structural prevents the feature from landing (it is a
two-function repository with no architecture in the way), the ghost-feature
reasoning places the mismatch in the product contract, not in stale docs and
not in the architecture → product_fog (primary), detailed in Section 6.5.

Failure consequence:
Any user, agent, or downstream workflow that trusts the README will run the
program and receive an immediate NotImplementedError; the repository's single
deliverable is non-functional. Every future step built on top (report format,
output sinks, scheduling, or a UI) would start from a false premise, and the
test suite would continue to "pass" while the product does nothing.

Confidence:
high — every link in the chain is directly observed in files that were opened
(core.py:1-2, main.py:3-4, tests/test_core.py:5-6, README.md:3) and the
repository's complete inventory was enumerated, so "implementation exists
elsewhere" is excluded by inspection, not by sampling. Would be raised further
only by external context (e.g. a roadmap or issue tracker confirming the
feature is intentionally deferred), which does not exist in this repository.

Alternatives considered:
- Candidate 2 (test pins NotImplementedError, tests/test_core.py:5-6) —
  rejected as the primary boundary: it is the enforcement mechanism that
  keeps the Ghost Feature stable, a symptom rather than an independent defect.
- Candidate 3 (implicit dependencies: undeclared pytest, CWD-dependent import,
  tests/test_core.py:1 / main.py:1) — rejected: real but dev-environment-only
  with low blast radius and no product consequence.
- Candidate 4 (no packaging/build validation) — rejected: with no manifest and
  no implementation there is no contract to validate; it dissolves into
  candidate 3.
```

## 6.5. Problem classification (fog type)

**primary_fog_type: product_fog.**

- **ui_fog ruled out by the decision tree:** the repository contains no frontend code of any kind (no React/Vue/Angular/HTML/CSS — full inventory, OBSERVED), so the UI Fog Signals Registry's first branch is "NO → Not ui_fog"; no Tier 1/2 signals are evaluated, and the frontend tie-break does not apply (no frontend exists).
- **Ghost-feature reasoning (three cases):** the documented-but-unimplemented "report generation" is not a docs problem (the README is not stale about a removed feature — it describes the repository's actual *intent*); it is a product-contract problem: the README advertises the feature as a real deliverable ("Implements report generation.", `README.md:3`) and no implementation exists (`core.py:2` raises; no other code anywhere). The architecture case does not apply — nothing structural prevents implementation; the repository is two functions and the missing piece is simply absent code.
- **Entry-point stub rule applied:** `main.py:3-4` is a runtime entry point that *runs*, but the promised surface it drives (report generation) has **no implementation at all** — the feature, not the entry point, is the defect. Per the skill's structural qualification, a promised DELIVERABLE with no implementation anywhere is a product-contract defect → `product_fog`. (Contrast: if the repository had other working features and only this stub, the entry-point framing would still point at the product promise here, because the README's entire claim is this feature.)
- **Secondary fog:** none. docs_fog would require the docs to misdescribe *existing* behavior; here the docs describe intended behavior that has no code, which is the product promise, not a documentation gap.
- **No-user-intent run:** no user problem statement or intent artifact exists for this fixture (standalone corpus run), so `user_implied_fog_type: unknown` and `diagnosis_conflict: false` (GAP-8); nothing is escalated on intent-conflict grounds.

## 7. Evidence

The diagnosis rests on four files, each opened in full:

- `README.md:3` — "Implements report generation." is the repository's only statement of purpose and its only product promise (OBSERVED).
- `core.py:1-2` — `generate_report(path)` is the entire feature surface; its body is a single `raise NotImplementedError('report generation not implemented yet')` (OBSERVED). The parameter `path` is never used, so no input handling exists.
- `main.py:3-4` — the sole entry point calls `generate_report('data.csv')`, making the guaranteed failure the program's only runtime behavior (OBSERVED). `main.py:1` shows the import wiring is present — this is not an unwired-module problem.
- `tests/test_core.py:5-6` — `with pytest.raises(NotImplementedError):` / `generate_report('x')` — the repository's only automated check asserts the exception rather than any report output (OBSERVED).

**Logic trace (required):** The README's promise ("Implements report generation.", `README.md:3`) is the observed contract. The only code claiming to discharge it is `core.py:1-2`, which raises `NotImplementedError` unconditionally — observed directly, and confirmed as the *entire* implementation because the repository's complete inventory (four files) was enumerated and no other file contains any generation logic. `main.py:4` proves the feature is on the runtime path rather than orphaned, and `tests/test_core.py:5-6` proves the failure is the expected, enforced behavior. A documented surface with no reachable implementation is Ghost Features (weakness-type taxonomy), and because the defect is the product promise — the README claims delivery of a deliverable that does not exist — the primary fog is `product_fog`. No frontend exists (ui_fog excluded), no structural blocker exists (architecture_fog excluded), and the docs are not stale about existing code (docs_fog excluded): the mismatch lives in the product contract.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Implements report generation."
    supports_claim: "The README's only product claim presents report generation as an implemented deliverable (the observed contract)."
  - file: core.py
    lines: L1-L2
    quote: "def generate_report(path):\n    raise NotImplementedError('report generation not implemented yet')"
    supports_claim: "The only implementation surface of the documented feature is an unconditional NotImplementedError stub; the path parameter is never used."
  - file: main.py
    lines: L3-L4
    quote: "if __name__ == '__main__':\n    generate_report('data.csv')"
    supports_claim: "The sole entry point routes the program's only execution path into the unimplemented function, so the failure is the runtime behavior."
  - file: tests/test_core.py
    lines: L5-L6
    quote: "with pytest.raises(NotImplementedError):\n        generate_report('x')"
    supports_claim: "The repository's only automated check codifies the absence of the feature as expected behavior, enforcing the Ghost Feature."
```

## 9. Why this boundary matters

- **The repository is 100% non-functional as promised:** anyone following `README.md:3` gets an immediate exception from `main.py:4` → `core.py:2`. There is no partial value to salvage.
- **The test suite masks the problem:** `tests/test_core.py:5-6` passes while the product does nothing, so standard "tests green" signals give false confidence — the Ghost Feature is actively enforced.
- **It blocks every downstream move:** report format, output handling, CLI ergonomics, packaging, and any consumer of the report all presuppose an implementation that does not exist; work on any of them is premature until the boundary is resolved.
- **The fix is cheap now and expensive later:** implementing a two-function feature is trivial today; if the repository grows, the "documented-but-absent" pattern becomes harder to detect and the README's present-tense claim will keep misleading readers and agents.

## 10. Candidate next steps

1. **Implement `generate_report` in `core.py:1-2`:** read `path`, produce a defined report (smallest concrete action that makes the README claim true).
2. **Specify the output contract first:** one short paragraph in `README.md` defining the report format, destination, and behavior on a missing/unreadable input file — makes step 1 testable and the promise precise.
3. **Flip the test to behavior:** replace the `pytest.raises(NotImplementedError)` assertion (`tests/test_core.py:5-6`) with a test that generates a report from a sample input and asserts its content — TDD-style, before or with step 1.
4. **Add packaging metadata:** a minimal `pyproject.toml` declaring `pytest` (`tests/test_core.py:1`) so tests are runnable outside the repo root.
5. **Reconcile the README after implementation:** confirm `README.md:3`'s claim is then accurate (or, if the feature is intentionally deferred, say so — the Ghost Feature must be resolved by making the promise true or removing the promise, never by leaving them divergent).

## 11. Recommended next step

Implement `generate_report` in `core.py:1-2` so it reads the file at `path` and produces a defined report (at minimum: parse `data.csv`, emit a report row/line per record, write or return it), and flip `tests/test_core.py:5-6` to assert that real output. This is the smallest change with the highest leverage: it converts the repository's only deliverable from a guaranteed failure into working functionality, makes the README claim (`README.md:3`) true, and unblocks every later step (output-contract spec, packaging, CI). The output contract should be decided as part of the same change so the implementation and its test agree.

## 12. Recommended workflow

**product-implementation-workflow** (from the canonical `skills/workflow-planner/references/workflow-registry.yaml:644`), in **guided_execution** mode.

Rationale: `primary_fog_type` is `product_fog` — a documented deliverable with no implementation — and the skill's problem classification maps product_fog to the product path (domain alignment → discovery/opportunity mapping → PRD → issues → TDD implementation). The registry defines product-implementation-workflow for "product/feature problems" (workflow-registry.yaml:644-647), which matches this fixture's need: align on the report contract, confirm the user need, then spec and implement. `guided_execution` is chosen because it is one of the workflow's registry-listed `allowed_execution_modes` (workflow-registry.yaml:654-656 lists `guided_execution` and `autonomous_execution`; `plan_only` is NOT offered for this workflow, so it must not be recommended). Recommending the workflow is a diagnostic handoff only — nothing is executed by this brief.

Why not the closest alternatives:

- **implementation-workflow** (workflow-registry.yaml:587) — the generic default for architecture/code problems; the product-specific workflow is the closer fit for a missing product deliverable.
- **architecture-implementation-workflow** (workflow-registry.yaml:848) — the defect is not structural: nothing prevents the feature from landing, and there is no architecture to refactor; the code simply does not exist.
- **docs-implementation-workflow** (workflow-registry.yaml:812) — the defect is not documentation: the README is accurate about intent; making it "accurate about delivery" is the *result* of implementing, not a docs task.
- **ui-diagnostic-workflow / ui-implementation-workflow** (workflow-registry.yaml:715/748) — no frontend surface exists in the repository.
- **product-discovery-sprint** (workflow-registry.yaml:247) — overkill: the user need is already explicit ("report generation", `README.md:3`); discovery is a step *within* product-implementation-workflow for any residual need ambiguity.
- **escalation** — not needed: the classification is strongly evidenced (four directly observed files, complete inventory) and unambiguous.

Preconditions before it can run: a one-paragraph decision on the report output contract (format/destination), which the workflow's first step (docs-aligner → CONTEXT.md) should capture before the PRD step; no other blocking preconditions exist.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-partial-impl
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (line 3): README advertises 'Implements report generation.' as an implemented deliverable"
  - "core.py (lines 1-2): the only implementation surface of generate_report raises NotImplementedError unconditionally"
  - "main.py (lines 3-4): the sole entry point calls generate_report('data.csv'), routing the only execution path into the failure"
  - "tests/test_core.py (lines 5-6): the only automated check asserts the NotImplementedError stub behavior"
recommended_workflow_id: product-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T06:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt

Route this repository sensemaking brief (fixture `adv-partial-impl`) through workflow-planner: `primary_fog_type` is `product_fog`, weakest boundary is Ghost Features — README.md:3 promises "Implements report generation." but the only implementation surface, core.py:1-2, raises `NotImplementedError` unconditionally, main.py:3-4 routes the sole execution path into it, and tests/test_core.py:5-6 codify the exception as expected behavior. Recommend **product-implementation-workflow** in **guided_execution** mode. The orchestration plan should: (1) align domain and record the report output contract (format, destination, missing-input behavior) in CONTEXT.md; (2) confirm the user need for report content via discovery; (3) produce a PRD and issues covering: implementing `generate_report` in core.py:1-2, flipping tests/test_core.py:5-6 to assert real output, and reconciling README.md:3 with actual behavior; (4) execute via TDD with human review gates. No other preconditions block the run.
