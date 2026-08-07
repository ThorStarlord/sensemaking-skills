# Repository Sensemaking Brief

## 1. Repository goal
The repository presents itself as **data-hub**: README.md:1 titles it `# data-hub`, README.md:3 advertises "Features: ingest, sync, export, webhooks.", and README.md:5 documents a quick start (`python -m datahub sync --remote`). The apparent goal is a data-hub tool exposing an `ingest`/`sync`/`export` feature set plus webhooks, operated through a `datahub` CLI. This is a fixture/standalone run with no user problem statement (GAP-8 no-user-intent run), so `user_implied_fog_type` is `unknown` and there is no stated intent to conflict with (`diagnosis_conflict: false`).

## 2. Current shape
Root inventory (all files actually opened, 3 total): `README.md` (5 lines), `src/__init__.py` (0 bytes, empty), `src/app.py` (6 lines). Absent from the inventory: any package manifest (pyproject.toml, setup.py, setup.cfg, requirements.txt), CI configuration, build configuration, container/deployment configuration, tests, documentation beyond the README, LICENSE.

Runtime flow (architecture reconstruction, not just inventory):
- **Startup**: the only executable entry point is `src/app.py:4` (`if __name__ == '__main__':`), runnable as `python src/app.py <path>`. The README-declared launch `python -m datahub sync --remote` (README.md:5) has no counterpart: no `datahub` module exists anywhere in the repository (recursive inventory is only README.md, src/__init__.py, src/app.py), and no `sync` subcommand or `--remote` flag is handled in code.
- **Orchestration**: none. The `__main__` block (src/app.py:4-6) performs a single call: `ingest(sys.argv[1])`. There is no CLI parsing, no server bootstrap, no route registration, no workers.
- **Domain/core logic**: exactly one function, `ingest(path)` at src/app.py:1-2, which reads and returns a file's contents (`return open(path).read()`).
- **Persistence/state**: no state is written anywhere. The only state interaction is the read of the file passed as `sys.argv[1]` at src/app.py:2, invoked from src/app.py:6. No files, databases, caches, queues, or environment variables are written or read elsewhere.
- **External integration points**: none — no HTTP, no webhooks, no remote systems. The word "webhooks" appears only in README.md:3.
- **Output boundary**: none. `ingest()` returns a string, but the `__main__` block at src/app.py:6 discards the return value (`ingest(sys.argv[1])` is not printed or written), so even the coded entry point produces no observable output.
- **Validation**: none. No tests exist; there are no schemas or assertions; `open(path)` at src/app.py:2 is unguarded (raises `FileNotFoundError` on a bad path) and `sys.argv[1]` at src/app.py:6 is unguarded (raises `IndexError` with no arguments).
- **Where responsibility becomes unclear**: the boundary between the documented product and the actual code. README.md:3 and README.md:5 assign responsibilities (sync, export, webhooks, a `datahub` CLI) that no code implements; `src/app.py` implements only `ingest`, and its `__main__` entry point behaves nothing like the documented CLI. Dependency semantics: there are no declared dependencies at all (no manifest), so there is nothing to classify as declared/used/runtime/test/dead.

## 3. Strong signals
- The single implemented function is simple and readable: `ingest(path)` is a two-line, side-effect-free file read (src/app.py:1-2).
- `src/__init__.py` exists as a package marker, so `src` is importable as a package (0 bytes — marker only).
- The README is short and explicit about what it claims, which makes the contradiction with the code easy to detect and to fix (README.md:3, README.md:5).
- The repo is tiny (3 files), so the gap between documentation and implementation is fully enumerable — no sampling uncertainty.

## 4. Missing pieces
- Implementation of `sync`, `export`, and `webhooks` — advertised in README.md:3, absent from every file in the repository (only `ingest` exists, src/app.py:1-2).
- A `datahub` module/package and the `sync` subcommand / `--remote` flag — advertised in README.md:5, absent from the inventory (only `src/` exists, with an empty `__init__.py`).
- Any package manifest (pyproject.toml/setup.py) making the repository installable or runnable as `python -m datahub` — absent from the root inventory.
- Any observable output from the coded entry point: `ingest(sys.argv[1])` discards its return value (src/app.py:6).
- Tests, schemas, input validation, and any automated check (Pass D: nothing is validated anywhere).
- Documentation of what the repository *actually* is (a stub/prototype), as opposed to what README.md:3-5 claims.

## 5. Improvement opportunities
- Decide and document the real product contract (which of the four advertised features are actual deliverables) before writing any feature code — this is the diagnosis-driving step, see Sections 10-12.
- Re-author README.md:3 and README.md:5 so the documented surface matches reality (either implement the features or clearly mark the repo as a stub).
- Add a minimal package manifest and a real CLI entry point (`datahub` module with a `sync` subcommand) if the tool is meant to be a CLI.
- Make the `__main__` block produce output (print or write the result of `ingest`) so the entry point is observable (src/app.py:6).
- Add basic input validation and tests for `ingest()` (src/app.py:1-2): missing argument, nonexistent path, directory path.

## 6. Weakest boundary

Candidate generation and scoring (5 candidates, per SKILL.md "Weakest Boundary Reasoning"):

| # | Boundary (file:line) | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|---|
| C1 | README feature promises (`sync`, `export`, `webhooks`) with no implementation — README.md:3 vs src/app.py:1-2 | strong | high | high | high | high | low |
| C2 | README quick-start CLI `python -m datahub sync --remote` has no runnable counterpart — README.md:5 vs src/app.py:4-6 (no `datahub` module, no subcommands/flags) | strong | high | medium | high | medium | low |
| C3 | Vocabulary drift: "data-hub"/"datahub" naming vs actual `src` package — README.md:1, README.md:5 vs directory structure | medium | low | low | medium | low | low |
| C4 | Zero validation: no tests, schemas, or input validation — src/app.py:2 (`open(path)`), src/app.py:6 (`sys.argv[1]`) | strong (absence) | medium | low | medium | medium | low |
| C5 | Result-discarding entry point: `ingest()` return value dropped — src/app.py:6 | strong | medium | low | medium | low | low |

Selection: **C1** (with C2 folded in as the interface side of the same ghost-feature surface).

```text
Boundary:
  The advertised product surface versus the actual implementation. What the
  repository claims to be (a data-hub with ingest/sync/export/webhooks and a
  `datahub` CLI: README.md:3, README.md:5) versus what the code delivers
  (one file-reading function and a main block that discards its result:
  src/app.py:1-6).
Observed contract:
  README.md:3 lists "Features: ingest, sync, export, webhooks." README.md:5
  documents "Quick start: `python -m datahub sync --remote`."
Observed violation or uncertainty:
  Only `ingest` exists (src/app.py:1-2); `sync`, `export`, and `webhooks`
  have no implementation anywhere in the repository. No `datahub` module
  exists (recursive inventory: README.md, src/__init__.py, src/app.py only;
  src/__init__.py is 0 bytes), and the sole `__main__` block (src/app.py:4-6)
  takes exactly one positional path argument with no subcommands and no
  flags. Even the coded entry point is unusable as documented: it discards
  `ingest()`'s return value (src/app.py:6), so `python -m datahub sync
  --remote` cannot work in any form.
Evidence:
  README.md:3 (feature list); README.md:5 (quick start); src/app.py:1-2
  (only implemented function); src/app.py:4-6 (only entry point);
  src/__init__.py (0 bytes); root inventory of exactly 3 files with no
  manifests, no tests, and no other modules.
Weakness type:
  Ghost Features
Logic trace:
  README.md:3 advertises four features (ingest, sync, export, webhooks) and
  README.md:5 advertises a `datahub` CLI as the quick start → Pass B
  (execution discovery) found exactly one executable entry point in the
  whole repository, the `__main__` block at src/app.py:4-6, and exactly one
  function, `ingest()` at src/app.py:1-2 → the recursive file inventory
  (README.md, src/__init__.py, src/app.py) shows no `datahub` module, no
  `sync`/`export`/`webhooks` code, and no manifests → every advertised
  feature and the advertised CLI are documented surfaces with no reachable
  implementation → per weakness-types.md, "Functionality mentioned in
  documentation that has no corresponding implementation" is `Ghost
  Features`. The README-vs-code contradiction is a promise problem, not a
  documentation-lag problem: the README presents nonexistent deliverables
  as current features, so per the SKILL.md ghost-feature reasoning the
  defect lives in the product contract (product_fog), not in stale docs.
Failure consequence:
  Any consumer or downstream agent that routes on the README will plan work
  against code that does not exist: `python -m datahub sync --remote`
  (README.md:5) fails immediately with ModuleNotFoundError; feature work on
  sync/export/webhooks has no code to target; and the repository is
  indistinguishable from a real product at a glance, so the false contract
  propagates into every downstream brief, plan, and implementation attempt.
Confidence:
  high. The evidence is direct and fully enumerable: every file in the
  repository was opened in full (3 files), the README claims are quoted
  verbatim (README.md:3, README.md:5), and the implementation surface
  (src/app.py:1-6) is exhausted by inspection. What would raise it further:
  executing `python -m datahub sync --remote` to observe the
  ModuleNotFoundError directly (not possible in this read-only environment —
  this remains DERIVED from the observed inventory, not OBSERVED by
  execution) and consulting git history to confirm sync/export/webhooks were
  never implemented (history unavailable — UNKNOWN, does not change the
  conclusion).
Alternatives considered:
  C2 (README quick-start CLI with no runnable counterpart, README.md:5 vs
  src/app.py:4-6) lost as an independent candidate only because it is the
  interface side of the same root cause as C1 — the README documents a
  `datahub` CLI that does not exist — and its evidence is folded into C1's
  Logic trace. C3 (vocabulary drift, "data-hub" at README.md:1 vs the `src`
  package) lost because it is a narrower symptom of the same misleading
  surface and has low blast radius; it is noted but does not drive routing.
  C4 (zero validation, no tests/schemas/input checks) lost because for a
  two-function stub, missing implementation dominates missing tests — tests
  would validate a contract that does not exist. C5 (result-discarding main,
  src/app.py:6) lost because it is a symptom of the stub state, not the
  sharpest boundary; it is listed as a fix step in Section 10.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)
`primary_fog_type`: **product_fog**.

- **ui_fog ruled out**: no frontend code exists — the inventory contains no HTML/CSS/JS/TS files — so the UI Fog Signals Registry decision tree exits at step 1 (NO frontend → not ui_fog). No Tier 1/2 UI signals can be cited.
- **architecture_fog ruled out**: there is no structure to be unclear about — a single two-line function and a three-line main block (src/app.py:1-6) with no modules, coupling, or state. The mismatch is not structural; it is a promise with no implementation.
- **docs_fog ruled out (as primary)**: the README does misdescribe the code, but per the SKILL.md ghost-feature reasoning, when "the README advertises a feature as real and the code does not implement it, that is product_fog — the defect is the promise, not the docs." The implementation is coherent but empty; the defect is the product contract (four promised features, a promised CLI), not merely stale documentation. docs_fog is noted as a contributing secondary fog (the README will need re-authoring regardless).
- **product_fog selected**: README.md:3 promises `sync`, `export`, and `webhooks` as current deliverables and README.md:5 promises a working CLI; neither exists in code (src/app.py:1-6). This is the canonical "product promises functionality that does not exist" case → product_fog. No user intent exists to tie-break with (GAP-8); the evidence is unambiguous, so no escalation is needed (`escalation_recommended: false`).

## 7. Evidence
All evidence is OBSERVED from files opened in full: `README.md:1` (title `# data-hub`), `README.md:3` (feature list: "Features: ingest, sync, export, webhooks."), `README.md:5` (quick start "`python -m datahub sync --remote`"), `src/app.py:1-2` (the only implemented function, `ingest(path)`, a plain file read), `src/app.py:4-6` (the only executable entry point — one positional path argument, no subcommands or flags, return value discarded), and `src/__init__.py` (0 bytes, empty). The recursive root inventory of exactly 3 files establishes the absence of: any `datahub` module, any sync/export/webhooks code, any package manifest, any tests, and any CI configuration. Nothing in this brief cites a file that was not opened.

**Logic trace:** README.md:3 advertises four features (ingest, sync, export, webhooks) and README.md:5 advertises the CLI `python -m datahub sync --remote` → Pass B (execution discovery) found exactly one executable entry point in the repository, the `__main__` block at src/app.py:4-6, and exactly one function, `ingest()` at src/app.py:1-2 → the full file inventory (README.md, src/__init__.py, src/app.py) contains no `datahub` module, no sync/export/webhooks implementation, and no manifests → every advertised feature and the advertised CLI are documented surfaces with no corresponding implementation → that is the canonical `Ghost Features` weakness ("Functionality mentioned in documentation that has no corresponding implementation", weakness-types.md) → because the README presents nonexistent deliverables as current features, the defect is the product promise (product_fog), not stale documentation → therefore the weakest boundary is the README-advertised product surface, and the primary fog is `product_fog`. The one piece of DERIVED (not OBSERVED) reasoning: `python -m datahub sync --remote` would fail to run, because the module inventory shows no `datahub` package — execution was not possible in this read-only environment, and this is labeled as DERIVED from the observed inventory.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: README.md
    lines: L1
    quote: "# data-hub"
    supports_claim: "Repository presents itself as a package named 'data-hub' (vocabulary claim)."
  - file: README.md
    lines: L3
    quote: "Features: ingest, sync, export, webhooks."
    supports_claim: "README promises four features; the code implements only one (ingest)."
  - file: README.md
    lines: L5
    quote: "Quick start: `python -m datahub sync --remote`."
    supports_claim: "README documents a CLI entry point that does not exist in the code."
  - file: src/app.py
    lines: L1-L2
    quote: "def ingest(path):\n    return open(path).read()"
    supports_claim: "The only implemented function is a plain file reader; no sync/export/webhooks exist anywhere."
  - file: src/app.py
    lines: L4-L6
    quote: "if __name__ == '__main__':\n    import sys\n    ingest(sys.argv[1])"
    supports_claim: "The only executable entry point takes one positional path, has no subcommands or flags, and discards the result."
```

## 9. Why this boundary matters
If the advertised product surface stays fictional, every consumer of this repository is misled at the first hop: a human or agent reading README.md:3-5 will plan sync/export/webhooks work or a CLI invocation against code that does not exist; `python -m datahub sync --remote` (README.md:5) fails immediately; downstream briefs, orchestration plans, and implementation tasks inherit the false contract; and the repository remains indistinguishable from a real product at a glance, so the lie propagates without any error surfacing until execution. This is precisely the failure mode an adversarial misleading README is designed to trigger: routing decisions made on documentation instead of code.

## 10. Candidate next steps
1. **Validate the intended product contract first**: run the product discovery workflow (see Section 12) to decide which of the four advertised features (ingest/sync/export/webhooks) are real deliverables — the README claims cannot be trusted as requirements.
2. **Re-author README.md:3 and README.md:5** to match reality: either list only implemented features, or clearly mark the repository as a stub/prototype with the implemented `ingest` behavior described accurately.
3. **Implement or delete the promises**: after the contract decision, either add `sync`/`export`/`webhooks` implementations plus a real `datahub` CLI (`sync` subcommand, `--remote` flag), or remove them from the README.
4. **Make the coded entry point observable**: print or persist the result of `ingest()` in the `__main__` block (src/app.py:6) and add argument/path validation (src/app.py:2, src/app.py:6).
5. **Add the missing skeleton**: a package manifest (pyproject.toml) and at least one test for `ingest()` (src/app.py:1-2) so the implemented surface is installable and verified.

## 11. Recommended next step
Step 1 — run the product-discovery workflow against this repository in `plan_only` mode to establish which of the README's four features are real deliverables before any code or documentation is touched. It is the smallest action at the weakest boundary: the defect is a fictional product contract, and the contract decision (what this repo actually is) unblocks every other step — README re-authoring (step 2), implementation-or-deletion (step 3), and validation (steps 4-5) all depend on it.

## 12. Recommended workflow
`product-discovery-sprint` (ID verified against `skills/workflow-planner/references/workflow-registry.yaml`), with `recommended_execution_mode: plan_only` — one of that workflow's `allowed_execution_modes` (plan_only, prompt_chain, guided_execution). Rationale: `primary_fog_type` is `product_fog` and per SKILL.md Section 7 product fog "needs discovery/research"; product-discovery-sprint exists precisely to "move from vague product fog to a validated opportunity and testable hypothesis" (workflow-registry.yaml:247-258), which is what a fictional feature list requires. Closest alternatives rejected: `product-implementation-workflow` (would implement against a contract known to be fictional — premature until discovery validates which features are real), `docs-implementation-workflow` (fixing the README alone would make the docs honest but would not resolve the underlying product decision — the repo may legitimately need sync/export/webhooks built), `fast-path-workflow`/`full-fog-workflow` (chaining wrappers that would re-run sensemaking and auto-invoke an implementation workflow, skipping the contract question this brief identifies), and `docs-contract-reconciliation` (targets framework-repo docs/contract drift, not a target repo's product promises). Preconditions: none missing — the brief supplies the diagnosed contract gap; the workflow's first step (persona) can consume this brief as its context.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-misleading-readme
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: product_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "README.md (L1): title claims 'data-hub'"
  - "README.md (L3): 'Features: ingest, sync, export, webhooks.'"
  - "README.md (L5): quick start 'python -m datahub sync --remote'"
  - "src/app.py (L1-L2): ingest() is the only implemented function — a plain file read"
  - "src/app.py (L4-L6): only entry point takes one positional path, no subcommands/flags, discards the result"
  - "src/__init__.py (0 bytes): empty package marker; no datahub module exists anywhere in the repo"
recommended_workflow_id: product-discovery-sprint
recommended_execution_mode: plan_only
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T04:30:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
"Run `product-discovery-sprint` (mode: plan_only) against the adv-misleading-readme repository (`experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-misleading-readme`) using the `repository_sensemaking_brief` (primary_fog_type: product_fog; weakest boundary: Ghost Features — the README advertises a product surface with no implementation). Scope: establish the real product contract — README.md:3 lists 'Features: ingest, sync, export, webhooks.' and README.md:5 documents 'Quick start: `python -m datahub sync --remote`', but the code contains only `ingest()` (src/app.py:1-2) and a `__main__` block that takes one positional path and discards the result (src/app.py:4-6); no `datahub` module, no sync/export/webhooks code, no manifests, and no tests exist. Validate which of the four advertised features are genuine deliverables for the intended user (persona → discovery → opportunity-tree → hypothesis), and produce the validated hypothesis that the subsequent implementation decision (build vs. delete each promise) can be routed on. Do not implement features or rewrite the README in this pass — the output is the validated product opportunity, not code."
