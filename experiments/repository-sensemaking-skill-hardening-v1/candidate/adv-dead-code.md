# Repository Sensemaking Brief — adv-dead-code

## 1. Repository goal
This repo is intended to be a record-processing pipeline whose core transformation is performed by a legacy processor. README.md:3 states the entire purpose as "Processes records through the legacy processor.", and docs/architecture.md:3 names the processor explicitly as load-bearing: "The legacy processor (legacy/processor.py) is the heart of the system." The implied goal is a runnable pipeline: a caller starts the pipeline, records flow into `Processor.process()`, and transformed records come out.

## 2. Current shape
**Inventory (complete — the repository is five files):** `README.md`, `docs/architecture.md`, `pipeline.py`, `legacy/__init__.py` (empty, 0 bytes), `legacy/processor.py`. There is no manifest (no `pyproject.toml`, `setup.py`, or `requirements.txt`), no Makefile, no CI configuration, no test files, and no other documentation (Pass A).

**Runtime flow (architecture reconstruction):**
- **Startup path: none declared.** `pipeline.py:1` defines `def run():` but nothing in the repository invokes it — there is no `if __name__ == "__main__"` guard (pipeline.py:1-2), no console-script entry point (no manifest exists to declare one), and no launcher script.
- **Orchestration:** `run()` (pipeline.py:1) is the only module-level flow control; it executes a single `print('active pipeline')` (pipeline.py:2) and returns. It calls nothing.
- **Domain/core logic:** `legacy/processor.py:4-20` defines `class Processor` with five methods — `process` (L6-8), `validate` (L10-11), `transform` (L13-14), `export` (L16-17), `notify` (L19-20) — each with a real body (e.g. `process` sleeps 1s and returns `data.upper()`). Its docstring (L5) reads `"""The core processor (docs say)."""`.
- **Persistence/state:** none. No file, database, cache, or environment-variable state exists anywhere in the repository.
- **External integrations:** none. The only import in the entire repository is `import time` at `legacy/processor.py:2` (stdlib).
- **Output boundary:** the only observable output is the string printed at `pipeline.py:2`. The processor's output (`data.upper()`) never reaches any consumer because nothing can reach the processor.
- **Dependency semantics:** `time` is *used* (imported at legacy/processor.py:2) but not *runtime* — it is exercised only inside a module no execution path ever loads. No other dependencies are declared anywhere (no manifest to declare them).
- **State model:** no state boundaries exist.
- **Boundary model:** the intended hop "entry point → core" (pipeline → legacy/processor.py) is the repository's defining boundary and it does not exist: pipeline.py:1-2 contains no import; `legacy/__init__.py` is empty and exposes no wiring; a repository-wide search for `import|Processor|legacy|run(` returns only self-references (processor.py:1-2,4-5) plus the documentation claims (README.md:3, docs/architecture.md:3) — no code outside `legacy/` ever references the module (OBSERVED across the full five-file inventory).
- **Where responsibility becomes unclear:** the documented core has zero callers, and the actual runtime does nothing. The docs describe behavior the code cannot perform, so a reader cannot tell whether the processor is the system's heart (as documented) or a dead module (as the code shows).

## 3. Strong signals
- The intended architecture is crisply documented: one pipeline, one processor, a clear record-flow contract (README.md:3; docs/architecture.md:3).
- The processor implementation is complete-looking: a real class with five named methods, each with a body (legacy/processor.py:6-20), including a plausible core transform (`process` → `data.upper()`, L6-8).
- Zero external dependencies: only stdlib `time` (legacy/processor.py:2) — no install or version friction.
- Minimal, conventional package layout: a top-level `pipeline.py` module plus a `legacy/` package with `__init__.py` — the shape matches the documented design, so the structure is not misleading; only the wiring is missing.

## 4. Missing pieces
- **Wiring:** nothing imports `legacy` or `Processor`. The full inventory (five files, all opened) contains no `import` of the module; the only import anywhere is `import time` at legacy/processor.py:2.
- **Execution contract:** no `__main__` guard (pipeline.py:1-2), no manifest, no Makefile, no CI — the repository cannot be started by any declared mechanism.
- **Tests:** zero test files; neither `process()`'s uppercase transform nor the pipeline's output is verified.
- **Input contract:** what "records" are, and what format `process()` expects, is undefined in any file.
- **Status documentation for `legacy/`:** nothing explains whether the processor is current or deprecated; the docstring "(docs say)" (legacy/processor.py:5) itself signals that its "core" status rests on documentation alone.

## 5. Improvement opportunities
- Add a `pyproject.toml` with a console-script entry point so the pipeline is startable by a documented command.
- Add a smoke test asserting `run()` routes data through `Processor.process()` once the wiring exists.
- Add a one-line status note in docs/architecture.md when the wiring lands, so "heart of the system" reflects runtime reality.
- Rename or delete the `legacy/` package once the processor's role is confirmed, to remove the ambiguity baked into the name.

## 6. Weakest boundary
**Candidate generation (scored):**

1. **Documented core is unreachable dead code** — README.md:3 and docs/architecture.md:3 present `legacy/processor.py` as live, but no execution path reaches it (pipeline.py:1-2 has no imports; zero references repository-wide). evidence_strength: strong · severity: high · blast_radius: high · goal_relevance: high · downstream_blocking_effect: high · uncertainty: low.
2. **No launcher/execution contract** — no `__main__` guard, no manifest, no CI (full inventory). evidence_strength: strong · severity: medium · blast_radius: high · goal_relevance: medium · downstream_blocking_effect: medium · uncertainty: low.
3. **No tests / no validation** — zero test files anywhere. evidence_strength: strong · severity: low · blast_radius: medium · goal_relevance: low · downstream_blocking_effect: medium · uncertainty: low.
4. **README vs. code mismatch** — docs describe processing; the pipeline does not process. evidence_strength: strong · severity: medium · blast_radius: medium · goal_relevance: high · downstream_blocking_effect: medium · uncertainty: low — but this is the *symptom* of candidate 1, not an independent boundary.

**Selection:**

```text
Boundary:
The documented runtime core — the hop from the pipeline entry point to
legacy/processor.py. README.md:3 and docs/architecture.md:3 present the legacy
processor as live, load-bearing functionality, but no code path reaches it.

Observed contract:
"Processes records through the legacy processor." (README.md:3);
"The legacy processor (legacy/processor.py) is the heart of the system."
(docs/architecture.md:3). The implied contract: running the pipeline causes
records to flow through Processor.process().

Observed violation or uncertainty:
The contract is unfulfillable. pipeline.py:1-2 (the only executable module)
contains no import and only prints 'active pipeline'; no code anywhere in the
repository imports `legacy` or `Processor` (OBSERVED: all five files opened,
plus a repository-wide search for `import|Processor|legacy|run(` returning only
self-references); legacy/__init__.py is empty, exposing no wiring; and no
launcher (`__main__` guard, manifest entry point, Makefile, CI) exists to start
anything.

Evidence:
README.md:3; docs/architecture.md:3; pipeline.py:1-2; legacy/processor.py:4-20
(especially L5); legacy/__init__.py (empty); absence of any import of `legacy`
across the full file inventory.

Weakness type:
**Ghost Features**

Logic trace:
README.md:3 and docs/architecture.md:3 document record-processing through
legacy/processor.py as live, current functionality — the README's entire
purpose line and the architecture doc's "heart of the system" claim. The
implementation surface does exist (legacy/processor.py:4-20 defines a complete
Processor class with five methods), and its own docstring (L5) says "The core
processor (docs say)" — signalling that the "core" status is a documentation
claim, not a runtime fact. But the runtime evidence contradicts the
documentation: pipeline.py:1-2 defines the only executable entry point and
contains no import statements; a repository-wide search for
`import|Processor|legacy|run(` finds no code outside legacy/ that ever
references the module; and legacy/__init__.py is empty, so the package exposes
no wiring either. Therefore the documented functionality ("records processed
through the legacy processor") has no reachable implementation: the processor
is dead/unreachable code that documentation presents as live functionality.
Per the GAP-6 taxonomy mapping, dead/unreachable code maps to Ghost Features
ONLY when documentation presents it as live functionality — exactly the case
here — so the correct weakness type is Ghost Features, not Orphaned Examples
(nothing here is example-shaped; the module is documented as the system's
core) and not Implicit Dependencies (the wiring is not merely undocumented —
it is absent while the docs promise it, which is the Ghost Features case).

Failure consequence:
Any reader, human or agent, trusts the documentation and either (a) builds new
work on legacy/processor.py, investing in code that can never run, or (b)
ships the pipeline believing records are processed when the runtime is a no-op
printing one string. The repository's sole stated purpose is false at runtime.

Confidence:
high. The full file inventory was inspected, so "no code imports the
processor" is an OBSERVED fact, not an inference. What would raise it
further: an actual execution trace (run the pipeline and observe that no
processor method executes) — but the static evidence is already conclusive.

Alternatives considered:
- Candidate 2 (no launcher/execution contract): real but secondary — even with
  a launcher, the pipeline would still do nothing; it is a consequence of the
  same missing wiring, and its severity is medium against candidate 1's high.
- Candidate 3 (no tests → Zero Validation): weak — with essentially no
  behavior to validate, the absence of tests is low-severity; Zero Validation
  would label a missing automated check of an existing contract, whereas here
  the contract itself is unreachable.
- Candidate 4 (docs mismatch → Vocabulary Drift): does not fit — the docs'
  terms match the directory structure (README says "legacy processor";
  legacy/processor.py exists), so there is no vocabulary drift; the mismatch
  is the symptom of the unreachable core, not an independent boundary.
```

## 6.5. Problem classification (fog type)
**Primary fog type: architecture_fog.**

- **Not ui_fog:** the repository contains no frontend code (no React/Vue/Angular/HTML/CSS — full inventory), so the UI Fog Signals Registry decision tree excludes ui_fog at step 1.
- **Not product_fog:** the promised processing feature HAS an implementation (legacy/processor.py:4-20). Per the entry-point-stub rule, a promised deliverable with no implementation anywhere is a product-contract defect; here the implementation exists but is unwired, so the defect is structural, not a product promise. (A secondary product_fog aspect — the documented behavior does not happen — is noted, but it is downstream of the structural gap.)
- **Not docs_fog:** the documentation is not stale and the implementation is not coherent-though-undocumented; the defect is that the docs are *true to the design but false to the runtime* because the structure cannot support the documented flow. docs_fog is for knowledge gaps where the implementation is coherent.
- **architecture_fog fits exactly:** the evidence signature is "unwired modules, structural mismatch between entry points and flow" — legacy/processor.py is an unwired module, pipeline.py:1-2 is a skeletal entry point that runs but forms an incomplete system, and the entry point → core hop is absent. Per the entry-point-stub rule, "entry points that run but form an incomplete system are architecture" — which is precisely this repository.

## 7. Evidence
The repository consists of exactly five files (`README.md`, `docs/architecture.md`, `pipeline.py`, `legacy/__init__.py`, `legacy/processor.py`) — no manifest, no tests, no CI, no launcher. The documentation presents the legacy processor as live functionality: README.md:3 ("Processes records through the legacy processor.") and docs/architecture.md:3 ("The legacy processor (legacy/processor.py) is the heart of the system."). The only executable path, pipeline.py:1-2, prints a string and never references the processor. A repository-wide search for `import|Processor|legacy|run(` finds no code outside `legacy/` that touches the module — the only import anywhere is `import time` at legacy/processor.py:2 — and legacy/__init__.py is empty, so the package exposes no wiring. The processor class itself exists with a full method surface (legacy/processor.py:4-20), and its docstring (L5) — "The core processor (docs say)" — marks its "core" status as a documentation claim.

**Logic trace:** the documentation promises a record-processing pipeline whose core is legacy/processor.py; the executable surface (pipeline.py:1-2) performs no such work and contains no import; because the entire file inventory was inspected, the absence of any import of `legacy` is an OBSERVED fact rather than an inference; therefore the documented core is unreachable dead code that documentation presents as live functionality — which the GAP-6 taxonomy mapping assigns to the Ghost Features weakness type — and because the defect is structural (unwired module + skeletal entry point that runs but forms an incomplete system), the primary fog type is architecture_fog, with a secondary product_fog aspect recorded in prose in Section 6.5.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L3
    quote: "Processes records through the legacy processor."
    supports_claim: "The README documents record-processing through the legacy processor as the repository's sole purpose — the functionality is presented as live."
  - file: docs/architecture.md
    lines: L3
    quote: "The legacy processor (legacy/processor.py) is the heart of the system."
    supports_claim: "The architecture document presents legacy/processor.py as the load-bearing core of the system."
  - file: pipeline.py
    lines: L1-L2
    quote: "def run():\n    print('active pipeline')"
    supports_claim: "The only executable module never imports or invokes the processor; the runtime does nothing but print a string."
  - file: legacy/processor.py
    lines: L5
    quote: "\"\"\"The core processor (docs say).\"\"\""
    supports_claim: "Even the processor's own docstring marks its 'core' status as a documentation claim, not a runtime fact."
  - file: legacy/processor.py
    lines: L6-L8
    quote: "    def process(self, data):\n        time.sleep(1)\n        return data.upper()"
    supports_claim: "A real implementation of the documented core transform exists — so the feature is not absent, it is unreachable (dead code presented as live)."
```

## 9. Why this boundary matters
- Humans and agents will route work to the "core" module (per docs/architecture.md:3) that can never execute — wasted effort and false confidence.
- The repository's documented purpose is false at runtime: any consumer of `pipeline.run()` (pipeline.py:1-2) gets a no-op.
- With no execution contract (no `__main__`, no manifest, no CI), nothing exercises the code, so the dead-core status can persist indefinitely without detection.
- The fix is cheap now (a wiring change); as the codebase grows, distinguishing live from dead "core" becomes expensive and risky, and the "(docs say)" ambiguity (legacy/processor.py:5) will mislead every future reader.

## 10. Candidate next steps
1. **Wire the entry point to the core:** in pipeline.py, import `Processor`, instantiate it inside `run()`, and call `process()` on input records; add an `if __name__ == "__main__"` guard. Smallest change that makes the documented contract true.
2. **Declare an execution contract:** add `pyproject.toml` with a console-script entry point (or a Makefile `run` target) so the pipeline is startable by a documented command.
3. **Add a smoke test:** `tests/test_pipeline.py` asserting `run()` routes data through `Processor.process()` (e.g. the uppercase transform), covering the wiring hop.
4. **Reconcile the documentation after wiring:** update README.md:3 and docs/architecture.md:3 to describe actual behavior — or, if the processor is truly obsolete, delete `legacy/` and rewrite the docs (this is the Ghost-Features resolution: make the promise true or remove the promise).
5. **Add CI:** a minimal workflow running the smoke test so the wiring contract is enforced going forward.

## 11. Recommended next step
Implement the wiring hop first: modify `pipeline.py:1-2` so `run()` imports and invokes `legacy.processor.Processor.process()` and add a `__main__` guard, then execute the pipeline and observe the processor actually running. This is the smallest change that converts the Ghost Feature into reachable functionality and makes every later step (tests, docs reconciliation, CI) meaningful — and it must happen before any documentation edit, so the docs are corrected against real behavior, not the other way around.

## 12. Recommended workflow
**architecture-implementation-workflow** (from `skills/workflow-planner/references/workflow-registry.yaml:848`), in **guided_execution** mode.

Rationale: `primary_fog_type` is architecture_fog (unwired module + structural mismatch between entry point and documented flow), and the skill maps architecture_fog to spec-driven refactoring. The registry defines architecture-implementation-workflow for "architecture/refactoring problems": align domain → refactoring spec (to-prd) → issues → agent briefs → TDD implementation, which fits this fixture's need (spec the wiring change, decompose into wiring/launcher/test/docs issues, implement with human review gates). `guided_execution` is chosen because it is one of the workflow's registry-listed `allowed_execution_modes` (workflow-registry.yaml:858-860 lists `guided_execution` and `autonomous_execution`; `plan_only` is NOT offered for this workflow, so it must not be recommended). Recommending the workflow is a diagnostic handoff only — nothing is executed by this brief.

Why not the closest alternatives:
- **implementation-workflow** (registry:587): the generic default for architecture/code problems, but the architecture-specific workflow is the closer fit for a structural wiring defect.
- **docs-implementation-workflow** (registry:812): the defect is not documentation alone — the docs become correct only after the wiring exists; docs-first would cement the Ghost Feature.
- **product-implementation-workflow** (registry:644): there IS an implementation; the gap is structural, not a product contract.
- **ui-diagnostic-workflow / ui-implementation-workflow** (registry:715/748): no frontend surface exists.
- **escalation:** not needed — the classification is strongly evidenced and unambiguous.

Preconditions before it can run: a human decision on whether `legacy/processor.py` is the intended core or should be removed; the refactoring spec (workflow step 2, to-prd) must record that decision.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-dead-code
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
user_implied_fog_type: unknown
primary_fog_type: architecture_fog
diagnosis_conflict: false
escalation_recommended: false
evidence:
  - "README.md (line 3): documents the repo purpose as processing records through the legacy processor"
  - "docs/architecture.md (line 3): presents legacy/processor.py as 'the heart of the system'"
  - "pipeline.py (lines 1-2): the only executable path prints a string and never imports or invokes the processor"
  - "legacy/processor.py (lines 4-20): Processor class exists with a full method surface but is referenced by no other file"
  - "legacy/__init__.py (empty): the package exposes no wiring to the processor"
recommended_workflow_id: architecture-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T05:39:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
Route this repository sensemaking brief (fixture `adv-dead-code`) through workflow-planner: `primary_fog_type` is `architecture_fog`, weakest boundary is Ghost Features — the documented core (README.md:3, docs/architecture.md:3) is unreachable dead code, because pipeline.py:1-2 never imports or invokes `legacy.processor.Processor` and no launcher or manifest exists. Recommend **architecture-implementation-workflow** in **guided_execution** mode. The orchestration plan should: (1) produce a refactoring spec for a wiring change that makes `pipeline.run()` invoke `Processor.process()` with a `__main__` guard; (2) decompose into issues — wiring, launcher/entry-point declaration, smoke test, documentation reconciliation; (3) execute via TDD with human review gates. Precondition to record in the spec: decide whether `legacy/processor.py` is the intended core (wire it) or obsolete (delete it and rewrite the docs) — the Ghost Feature must be resolved by making the promise true or removing the promise, never by leaving docs and runtime divergent.
