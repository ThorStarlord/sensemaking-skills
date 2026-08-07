# Repository Sensemaking Brief

## 1. Repository goal
`store-lib` is a minimal Python key-value store library: a small `Store` class that persists arbitrary `key -> value` pairs to a local JSON file on disk. The README presents the library as an installable package (`README.md:2-3`), and the design doc frames its history as a SQLite-based design (`docs/design.md:3`). The implemented product surface is a dependency-free, two-method persistence API (`store.py:4-13`).

## 2. Current shape
Runtime flow (reconstructed from the files actually opened):

- **Startup / entry point**: there is no executable entry point. `pyproject.toml:1-2` declares only `[project] name = "store-lib"` — no `[build-system]`, no version, no console scripts. The only entry surface is the library API: importing `Store` from `store.py:4`.
- **Orchestration**: none — the library has no controller; callers drive `Store.put()` / `Store.get()` directly.
- **Domain/core logic**: `Store` (`store.py:4-13`). `put(key, value)` merges into the loaded dict and writes it back (`store.py:7-10`); `get(key)` loads the file and returns `data.get(key)` (`store.py:11-13`).
- **Persistence / state boundary**: a single JSON file, default `store.json` (`store.py:5`), read by `put` and `get` (`store.py:8,12`) and written by `put` (`store.py:10`). This is the only state boundary in the repository — no database, no cache, no environment variables.
- **External integrations**: none. Only stdlib imports `json` and `pathlib` (`store.py:1-2`). Dependency semantics: `json`/`pathlib` are `used` and `runtime` on the store's execution path, but they are stdlib and are `declared` nowhere (pyproject.toml declares no dependencies at all).
- **Validation**: none. No input validation on `put`/`get`, no schema, no tests, no CI. `get()` calls `json.loads(self.path.read_text())` with no existence check (`store.py:12`), so a `get` before any `put` raises `FileNotFoundError`; a truncated/corrupt `store.json` raises `json.JSONDecodeError`.
- **Where responsibility becomes unclear**: the documented persistence contract disagrees with the implementation. README states "Uses SQLite for persistence" (`README.md:2`) and the design doc references SQLite tables `items`, `users` (`docs/design.md:3`), while the code is a JSON-file store with zero SQLite code anywhere (no `sqlite3` import in `store.py:1-13`). Per evidence rule 4 (source code outranks descriptive documentation for current runtime behavior), the code is authoritative: the actual persistence is JSON. The intended product contract (JSON vs SQLite) is **UNKNOWN** — code evidence says JSON, docs say SQLite; what the owner intends cannot be established from the files inspected.

## 3. Strong signals
- Coherent, minimal API: `put`/`get` with simple, readable semantics (`store.py:7-13`).
- Dependency-free implementation using only stdlib (`store.py:1-2`) — no undeclared runtime dependencies to resolve.
- The `path` constructor parameter (`store.py:5`) makes the store's location explicit and the class testable/customizable.
- The design doc honestly labels the SQLite design as "Old design" (`docs/design.md:3`), i.e. the repository does contain a (partial) historical marker of what changed.

## 4. Missing pieces
- **Accurate README**: `README.md:2` describes SQLite persistence that the code does not implement (OBSERVED contradiction, see Section 6).
- **Tests**: no test files exist anywhere in the repository (OBSERVED via recursive directory listing — only `README.md`, `docs/design.md`, `pyproject.toml`, `store.py`).
- **Packaging metadata**: `pyproject.toml:1-2` has no `[build-system]`, version, readme, or dependencies, so the README's `pip install store-lib` claim (`README.md:3`) is not backed by a verifiable build contract.
- **Robustness in `get()`**: no existence/corruption guard before `json.loads` (`store.py:12`).
- **Current design documentation**: `docs/design.md:3` documents a superseded SQLite design; no doc describes the actual JSON-file persistence format.

## 5. Improvement opportunities
- Add a `[build-system]` and version to `pyproject.toml` so the install claim (`README.md:3`) becomes verifiable.
- Add unit tests for `put`/`get` round-trips, missing-file, and corrupt-file cases.
- Guard `get()` against a missing or corrupt file (`store.py:12`).
- Document the on-disk JSON format (keys, ordering, atomicity of writes) in the README.

## 6. Weakest boundary
Candidate boundaries generated first, then selected:

1. **README vs implementation persistence contract** — `README.md:2` ("Uses SQLite for persistence") vs JSON-file store (`store.py:5,8,10,11-13`). evidence_strength: strong (direct observed contradiction); severity: high (core persistence contract wrong); blast_radius: medium (the storage layer is the entire library); goal_relevance: high (persistence is the repo's whole purpose); downstream_blocking_effect: high (any consumer or doc built from the README designs against SQLite); uncertainty: low.
2. **Install claim vs packaging metadata** — `README.md:3` (`pip install store-lib`) vs `pyproject.toml:1-2` (no `[build-system]`/version). evidence_strength: strong; severity: medium; blast_radius: low-medium; goal_relevance: medium; downstream_blocking_effect: medium; uncertainty: medium (a missing build backend is observable, but whether installability is intended to work is not fully established).
3. **Zero validation of the store** — no tests anywhere; unguarded `json.loads` in `get()` (`store.py:12`). evidence_strength: medium (absence is observed via listing; the crash path is directly readable); severity: medium; blast_radius: low (13-line library); goal_relevance: medium; downstream_blocking_effect: low; uncertainty: medium.
4. **Historical design doc vs current code** — `docs/design.md:3` references SQLite tables `items`/`users`. evidence_strength: strong but explicitly labeled "Old design", so it is historical rather than a live claim; severity: low; blast_radius: low; goal_relevance: low; downstream_blocking_effect: low; uncertainty: low.

Selection: **candidate 1**. It has the strongest combination of direct evidence, severity, goal centrality, and downstream blocking — the persistence contract is the library's entire reason to exist, and every downstream consumer will be misled by the README.

```text
Boundary: the documented persistence contract (README.md:2; docs/design.md:3) vs the implemented persistence (store.py:4-13).
Observed contract: README states the library "Uses SQLite for persistence" (README.md:2); the design doc references SQLite tables `items`, `users` (docs/design.md:3).
Observed violation or uncertainty: store.py implements a JSON-file store — default path 'store.json' (store.py:5), json.loads on read (store.py:8,12), json.dumps on write (store.py:10) — and no sqlite3 import or SQL code exists anywhere in the repository (store.py:1-13). The documented SQLite contract has no counterpart in code.
Evidence: README.md:2; store.py:5; store.py:8; store.py:10; store.py:11-13; docs/design.md:3.
Weakness type: Vocabulary Drift
Logic trace: README.md:2 promises "SQLite for persistence", and docs/design.md:3 names SQLite tables `items`/`users`; the code I opened — store.py:5 ('store.json' default path), store.py:8 and store.py:12 (json.loads), store.py:10 (json.dumps) — implements a JSON-file store with no sqlite3 usage in store.py:1-13. The code exists and is coherent; therefore the docs are simply wrong about existing code, which per the GAP-6 taxonomy mapping is Vocabulary Drift (docs misdescribing EXISTING code), not Ghost Features (there is no documented surface with no implementation — the JSON store is implemented and works) and not a Contract Mismatch (no file claims a wrong format).
Failure consequence: consumers following the README will design against SQLite (schemas, `items`/`users` tables, SQL queries) that do not exist; any SQLite integration attempt fails against a JSON file; the documented schema has no counterpart in code, so the library's actual storage behavior is effectively hidden from its own documentation.
Confidence: high — the contradiction is directly observed across files I opened. It would be raised further (and the intended contract confirmed) by git history or an owner statement showing whether JSON replaced SQLite deliberately; neither exists in this fixture.
Alternatives considered: (1) Zero Validation — the absence of tests and the unguarded store.py:12 read are real but secondary: they do not block consumers the way a wrong persistence contract does, and the README contradiction has stronger, more direct evidence. (2) Implicit Dependencies for the packaging gap (README.md:3 vs pyproject.toml:1-2) — the install claim is peripheral to the library's core behavior and has lower goal relevance. (3) Ghost Features — rejected by the GAP-6 mapping: the code exists (JSON store) and the docs misdescribe it; Ghost Features requires a documented surface with no reachable implementation. (4) The docs/design.md:3 SQLite claim itself — same drift family but explicitly labeled "Old design", so it is historical, lower blast radius, and secondary to the live README claim.
```

**Weakness type:** Vocabulary Drift

## 6.5. Problem classification (fog type)
The primary fog type is **docs_fog**. There is no frontend code in the repository (only `store.py`, `pyproject.toml`, and two Markdown docs), so the UI Fog Signals Registry decision tree rules out `ui_fog` at step 1. The implementation is coherent — a working JSON-file store — while the documentation misdescribes it: `README.md:2` claims SQLite persistence and `docs/design.md:3` references SQLite tables that do not exist. Per SKILL.md, docs_fog's defining evidence is "docs that misdescribe current code", which is exactly what `README.md:2` vs `store.py:4-13` shows. `product_fog` was considered (the README could be read as promising SQLite as a deliverable), but the defect lives in the *documentation*: the deliverable (a working store) exists; only the docs are stale — consistent with the fixture's "Old design" historical marker (`docs/design.md:3`) and with code outranking docs for current runtime behavior (evidence rule 4). `architecture_fog` does not apply — there is no structural defect, unwired module, or entry-point stub; the system is a simple library that runs. Secondary fog: none rises to the same level; a weak `product_fog` reading of the SQLite claim is noted but does not drive routing.

`primary_fog_type: docs_fog` (structured field; see Section 13).

## 7. Evidence
The core evidence is a direct, observed contradiction between documentation and implementation:

- `README.md:2` — "Uses SQLite for persistence. `pip install store-lib`." (the SQLite claim is present-tense and current).
- `store.py:5` — `def __init__(self, path='store.json'):` — the default persistence target is a JSON file, not a SQLite database.
- `store.py:8` — `data = json.loads(self.path.read_text()) if self.path.exists() else {}` — reads via `json.loads`.
- `store.py:10` — `self.path.write_text(json.dumps(data))` — writes via `json.dumps`.
- `store.py:12` — `data = json.loads(self.path.read_text())` — `get()` reads JSON with no existence guard (also evidence of zero validation).
- `docs/design.md:3` — "Old design: SQLite tables `items`, `users`." — the only SQLite tables named anywhere are explicitly historical.
- `pyproject.toml:1-2` — `[project]` / `name = "store-lib"` — no build backend or version, so the install claim at `README.md:3` is unverifiable (supporting Zero Validation as an alternative candidate, not the selected boundary).

Absence evidence (OBSERVED via recursive listing of the target repo, not via a cited file): no tests, no CI configuration, no `sqlite3` usage in `store.py:1-13`.

**Logic trace:** README.md:2 promises SQLite persistence and docs/design.md:3 names SQLite tables `items`/`users`; the files I opened — store.py:5 (default path `store.json`), store.py:8 and store.py:12 (`json.loads`), store.py:10 (`json.dumps`) — implement a JSON-file store, and store.py:1-13 contains no `sqlite3` import. Code outranks descriptive documentation for current runtime behavior (evidence rule 4), so the implementation is the JSON store; the README therefore misdescribes existing code, which is Vocabulary Drift (GAP-6 mapping), and since the implementation is coherent while only the docs are stale, the fog is docs_fog, not product_fog (the deliverable exists) and not architecture_fog (no structural defect). The residual uncertainty — whether the *intended* product contract is JSON or SQLite — is UNKNOWN and can only be resolved by the owner.

## 8. Evidence excerpts
```yaml
evidence_excerpts:
  - file: README.md
    lines: L2
    quote: "Uses SQLite for persistence. `pip install store-lib`."
    supports_claim: README describes the library's persistence as SQLite, contradicting the implemented JSON-file store.
  - file: store.py
    lines: L5
    quote: "def __init__(self, path='store.json'):"
    supports_claim: The default persistence target is a JSON file, not a SQLite database.
  - file: store.py
    lines: L8
    quote: "data = json.loads(self.path.read_text()) if self.path.exists() else {}"
    supports_claim: put() reads the store via json.loads (JSON persistence).
  - file: store.py
    lines: L10
    quote: "self.path.write_text(json.dumps(data))"
    supports_claim: put() writes the store via json.dumps (JSON persistence).
  - file: store.py
    lines: L11-L13
    quote: "def get(self, key):\ndata = json.loads(self.path.read_text())\nreturn data.get(key)"
    supports_claim: get() reads JSON with no existence or corruption guard; no SQLite code exists anywhere in the module.
  - file: docs/design.md
    lines: L3
    quote: "Old design: SQLite tables `items`, `users`."
    supports_claim: The only SQLite tables named in the repo are explicitly historical ("Old design").
  - file: pyproject.toml
    lines: L1-L2
    quote: "[project]\nname = \"store-lib\""
    supports_claim: Packaging metadata is minimal (no build-system, no version), so the README install claim is unverified.
```

## 9. Why this boundary matters
The README is the repository's only live documentation of how the library behaves. Anyone onboarding, consuming, or extending `store-lib` will design against SQLite — write schema migrations for `items`/`users`, attempt `sqlite3` connections, or build integrations expecting a database — and will fail against a JSON file. The gap also erodes trust in the docs generally: if the persistence claim is wrong, every other claim (`pip install store-lib` at `README.md:3`) is suspect until verified. Left unaddressed, the drift will keep compounding because nothing in the repo (no tests, no CI) would ever catch a docs/code disagreement.

## 10. Candidate next steps
1. Rewrite `README.md:2` to describe the actual JSON-file persistence (`store.json`, `put`/`get` semantics) and drop or correct the SQLite claim.
2. Update or archive `docs/design.md:3` so the SQLite `items`/`users` design is explicitly marked as superseded history rather than an ambiguous "Old design" note.
3. Confirm the intended persistence contract with the owner (JSON vs SQLite) — the code says JSON, the docs say SQLite; this decision gates all doc rewrites.
4. Add `[build-system]`/version metadata to `pyproject.toml:1-2` so `pip install store-lib` (`README.md:3`) becomes verifiable.
5. Add tests and a guard for `store.py:12` (missing/corrupt file) so the documented behavior is exercised.

## 11. Recommended next step
Correct the README to describe the implemented JSON-file persistence — specifically `README.md:2`, replacing the SQLite claim with an accurate description of the `Store` class backed by `store.json` (`store.py:5,8,10,11-13`). This is the smallest concrete action with the highest leverage: it resolves the selected weakest boundary directly, unblocks every consumer who reads the README, and requires no code changes. Follow it immediately with step 3 (owner confirmation of the intended contract) if the JSON-vs-SQLite intent is in doubt.

## 12. Recommended workflow
**docs-implementation-workflow** (from the canonical `skills/workflow-planner/references/workflow-registry.yaml`), execution mode **guided_execution**.

Rationale: the fog is `docs_fog` — a documentation problem (stale README/design docs misdescribing existing code) — and docs-implementation-workflow is the registry's workflow "for documentation/knowledge problems. Aligns domain understanding, creates documentation architecture, and generates docs." `guided_execution` is one of its two `allowed_execution_modes` (guided_execution, autonomous_execution) and is the conservative choice for a doc rewrite that should be human-reviewed.

Why not the closest alternatives: `product-implementation-workflow` (guided_execution/autonomous_execution) is wrong — no user-need discovery is required; the code is coherent and the fix is documentation. `architecture-implementation-workflow` (guided_execution/autonomous_execution) is wrong — no structural defect exists to refactor. `docs-contract-reconciliation` (plan_only/prompt_chain/guided_execution) is oriented to drift between the sensemaking framework's own docs, contracts, registries, and validator rules — not to a target repository's user-facing docs. `fast-path-workflow` is the orchestration that would *contain* this diagnostic step, not the implementation step to run next. Precondition before the workflow can run: owner confirmation of the intended persistence contract (JSON vs SQLite), so the generated docs describe the true target.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/stale-readme
source_intent_ref: none (standalone fixture run; no 00-user-intent.md artifact exists)
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
evidence:
  - "README.md (L2): claims 'Uses SQLite for persistence' while store.py implements JSON-file persistence"
  - "store.py (L5, L8, L10, L11-L13): JSON-file key-value store; no sqlite3 code anywhere in the module"
  - "docs/design.md (L3): references SQLite tables items/users, explicitly labeled 'Old design' (historical)"
  - "pyproject.toml (L1-L2): minimal packaging metadata; no build-system or version, so README.md:3 install claim is unverified"
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary:
  type: Vocabulary Drift
  evidence: README.md:2 ('Uses SQLite for persistence') vs store.py:5,8,10,11-13 (JSON-file store via json.loads/json.dumps; no sqlite3 import)
weakness_type: Vocabulary Drift
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T00:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
> Run **docs-implementation-workflow** in **guided_execution** mode against the `stale-readme` repository (experiments/repository-sensemaking-skill-hardening-v1/corpus/stale-readme). The repository_sensemaking_brief classifies this as **docs_fog** with weakest boundary **Vocabulary Drift**: `README.md:2` claims "Uses SQLite for persistence" but `store.py:5,8,10,11-13` implements a JSON-file store (default path `store.json`, `json.loads`/`json.dumps`, no `sqlite3` import), and `docs/design.md:3` references SQLite tables `items`/`users` as "Old design". Align the documentation with the actual implementation: rewrite `README.md:2` to describe the JSON-file persistence API (`Store.put`/`Store.get`), and mark the SQLite design in `docs/design.md:3` as superseded history. Before generating docs, confirm with the owner whether the intended persistence contract is JSON (per code) or SQLite (per docs) — the code is authoritative for current behavior, but the product intent is UNKNOWN. Do not change `store.py`; this is a documentation-alignment task only.
