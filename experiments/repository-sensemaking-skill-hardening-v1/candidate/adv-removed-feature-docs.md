# Repository Sensemaking Brief

## 1. Repository goal
The repository presents itself as a minimal Python utility: README.md:1 titles it `# removed-feature` and README.md:3 points to an export documentation page. The actual code surface is a single function, `ingest()` (app.py:1-2), executed by a `__main__` guard (app.py:4-5). The one piece of documentation, docs/export.md:3, instructs the user to run `python app.py export --format csv` to "export all records" — a command the code does not implement. This is a fixture/standalone run with no user problem statement (GAP-8 no-user-intent run), so `user_implied_fog_type` is `unknown` and there is no stated intent to conflict with (`diagnosis_conflict: false`). The apparent goal of the surviving code is a stub "ingest" utility; the docs' goal is a (removed) export capability.

## 2. Current shape
Root inventory (all files actually opened, 3 total): `README.md` (3 lines), `app.py` (5 lines), `docs/export.md` (3 lines). Absent from the inventory: manifests (requirements.txt / pyproject.toml / setup.py), CI configuration, build configuration, container/deployment configuration, tests, any other documentation, LICENSE.

Runtime flow (architecture reconstruction, not just inventory):
- **Startup**: `python app.py` enters the `if __name__ == '__main__':` guard at app.py:4-5 and calls `ingest()`.
- **Orchestration**: none beyond the `__main__` block — app.py:4-5 directly invokes `ingest()`; no argument parsing, no subcommand dispatch (no `argparse`/`sys.argv` anywhere in the file).
- **Domain/core logic**: `ingest()` prints the fixed string `'ingest'` (app.py:1-2). There is no other logic.
- **Persistence/state**: none. No files, databases, caches, queues, global/module state, or environment variables are read or written.
- **External integration points**: none. The program touches no external system.
- **Output boundary**: a single stdout print (app.py:2).
- **Validation**: none (Pass D). No tests, no CI, no schemas, no assertions, no input validation, no error handling.
- **Where responsibility becomes unclear**: the documented `export` command. docs/export.md:3 instructs running `python app.py export --format csv`, but app.py:1-5 contains no `export` handler, no CSV logic, and no argument handling of any kind. Running the documented command would silently execute the `__main__` block and print `'ingest'` — the extra argv (`export --format csv`) is ignored. The hop from the documented CLI surface to any implementation cannot be traced; it is UNKNOWN (Pass C — record the missing hop rather than inventing it).

Dependency semantics: no dependency manifest exists (OBSERVED absence). The code imports nothing (app.py:1-5 uses only builtins), so there are no `declared`, `used`, `runtime`, `test`, `optional`, or `dead` dependencies to classify — the dependency surface is empty.

## 3. Strong signals
- The surviving code is coherent and runnable: `python app.py` prints `'ingest'` via a correct `__main__` guard (app.py:4-5) — there is no structural defect in the code that exists.
- The repository is tiny (3 files), so every claim in this brief is fully enumerable — there is no sampling uncertainty and no low-value content to deprioritize.
- README.md:1-3 makes no feature *promise*: it does not advertise export as a deliverable, it only links the export doc — which keeps this out of the product_fog bucket (the defect is the stale doc, not a broken product contract).
- The repo title `# removed-feature` (README.md:1) is honest metadata: it signals that a feature was removed, which is consistent with the observed state (docs for a removed feature).

## 4. Missing pieces
- An `export` implementation: docs/export.md:3 documents `python app.py export --format csv` "exports all records", but no such subcommand, function, or CSV output exists in app.py:1-5 — the documented feature is entirely absent.
- Argument handling: app.py:4-5 ignores `sys.argv` entirely, so even a future subcommand has no dispatch scaffolding.
- Tests: nothing exercises `ingest()` (app.py:1-2); there is no test directory, no CI.
- A truthful usage doc: README.md:3 links to docs/export.md, propagating the stale export claim transitively; neither file documents the actual interface (`python app.py` → prints `'ingest'`).
- Any dependency manifest or packaging metadata (no requirements.txt / pyproject.toml), which leaves the runtime requirements undocumented.

## 5. Improvement opportunities
- Replace or delete the stale docs: rewrite docs/export.md:3 (and the README.md:3 link) to describe the actual command (`python app.py`) and its real output, or remove the file if the export feature is permanently gone.
- If export is intended to exist, re-add it properly: an `argparse`-based subcommand with a `--format` option (app.py) plus a test — i.e., turn the ghost feature back into a real one.
- Add a smoke test for the `__main__` path (app.py:4-5) so the only observable behavior is machine-checked.
- Document the empty dependency surface and the intended runtime (README.md) so readers know exactly what the tool does today.
- Add a docs-vs-code consistency check (e.g., a CI step grepping documented CLI invocations against actual entry points) so removed-feature docs cannot silently return.

## 6. Weakest boundary

Candidate generation and scoring (4 candidates, per SKILL.md "Weakest Boundary Reasoning"):

| # | Boundary (file:line) | Evidence strength | Severity | Blast radius | Goal relevance | Downstream blocking | Uncertainty |
|---|---|---|---|---|---|---|---|
| C1 | Documented-but-unimplemented `export` command — docs/export.md:3 vs app.py:1-5 (no export subcommand, no argparse/sys.argv, no CSV code) | strong | medium | low-medium | high | medium | low |
| C2 | Zero validation — no tests/CI/schemas/argument handling anywhere; `python app.py export --format csv` silently runs `ingest()` | strong (absence) | medium | low | medium | low | low |
| C3 | README under-documentation — README.md:1-3 is a title plus a link; no usage, no goal, no behavior description | strong (absence) | low | low | medium | low | low |
| C4 | `ingest()` is a placeholder stub — app.py:2 prints the literal string `'ingest'` rather than ingesting anything | medium | low | low | medium | low | medium |

Selection: **C1**.

```text
Boundary:
  The documented CLI surface versus the implemented code surface.
  docs/export.md:3 instructs the user to run `python app.py export --format
  csv` to "export all records"; app.py implements no export command.
Observed contract:
  docs/export.md:3 states: "`python app.py export --format csv` exports all
  records." — a usage contract asserting that the program exposes an
  `export` subcommand with a `--format` option that produces an export of
  all records.
Observed violation or uncertainty:
  app.py:1-5 (the complete, 5-line code surface) defines exactly one
  function, `ingest()` (app.py:1-2), and one entry path, the
  `if __name__ == '__main__':` guard (app.py:4-5). There is no `export`
  function, no `argparse`/`sys.argv` argument handling, and no CSV code.
  The documented command cannot dispatch to any export logic: running it
  executes the `__main__` block and prints `'ingest'`. The repo title
  `# removed-feature` (README.md:1) and README.md:3's link to the export
  doc corroborate that the export feature was removed while its
  documentation survived.
Evidence:
  docs/export.md:3 (the documented command); app.py:1-2 (the only
  function, ingest); app.py:4-5 (the only entry point, no argv handling);
  README.md:1 (title "removed-feature"); README.md:3 (link propagating the
  stale doc). All three repository files were opened in full.
Weakness type:
  Ghost Features
Logic trace:
  The documentation asserts a feature — an `export` CLI subcommand
  producing all records (docs/export.md:3) — and the code surface, fully
  enumerated across the 3-file repository, contains no corresponding
  implementation: app.py:1-2 defines only `ingest()`, app.py:4-5 handles
  no arguments, and no other file exists that could implement export. A
  documented surface with no reachable implementation is precisely the
  Ghost Features definition — "Functionality mentioned in documentation
  that has no corresponding implementation" (weakness-types.md:7). The
  repo title itself ("removed-feature", README.md:1) confirms the feature
  was removed rather than never planned. Per SKILL.md's ghost-feature
  reasoning, documentation that lags removed code is a docs_fog candidate:
  the defect lives in the stale doc (docs/export.md:3), not in the product
  contract (the README makes no export promise — README.md:3 only links
  the doc) and not in the architecture (the surviving code is coherent
  and runnable). Therefore the weakest boundary is the ghost `export`
  command documented at docs/export.md:3, and the primary fog is
  docs_fog.
Failure consequence:
  Any human or agent following the documentation runs `python app.py
  export --format csv` and silently gets the wrong behavior — the command
  prints `'ingest'` instead of exporting records, with no error, so the
  failure masquerades as success. Anyone planning work from the docs
  (adding export consumers, building on "all records") plans against a
  surface that does not exist; and the README's link (README.md:3)
  propagates the ghost to every reader of the repo's front page.
Confidence:
  high — the contradiction is directly observable between two tiny files,
  both read in full (docs/export.md:3 vs app.py:1-5), with zero sampling
  uncertainty in a 3-file repository. A git history showing the export
  removal commit would raise it further, but no git metadata is available
  in this fixture; nothing else would materially change the conclusion.
Alternatives considered:
  C2 (Zero Validation — no tests/CI anywhere) lost: even perfect
  validation would not make the documented export command exist; the core
  defect is a documented-but-absent feature, and the missing checks are a
  secondary gap recorded in Sections 4/5. C3 (sparse README) lost: the
  README is minimal but accurate about what exists; its one flaw is
  transitive (the link at README.md:3 points at the stale export doc),
  which is C1's territory. C4 (ingest is a placeholder) lost: the print
  behavior is literally what the code does — a stub is not a contradiction
  by itself, and its fix (implement real ingest) is a product decision,
  not the sharpest boundary. Contract Mismatch (weakness-types.md:6) was
  considered and rejected: docs/export.md is genuinely Markdown; there is
  no file-format claim in play. Vocabulary Drift (weakness-types.md:5)
  was considered and rejected: the drift is feature-level (a documented
  command with no implementation), not term-level.
```

**Weakness type:** Ghost Features

## 6.5. Problem classification (fog type)
`primary_fog_type: docs_fog`.

Reasoning against the four fog types:
- **Not ui_fog**: the repository contains no frontend/UI code at all (no React/Vue/Angular/HTML/CSS; the inventory is README.md, app.py, docs/export.md), so the UI Fog Signals Registry decision tree rules it out at the first step ("NO → Not ui_fog; check other fog types").
- **Not product_fog**: no product promise is broken. README.md:1-3 advertises no deliverable — it only links the export doc (README.md:3) — so the export mismatch is not a promise the repo makes to users; there is no roadmap, issue tracker, or acceptance-criteria surface.
- **docs_fog**: the documentation misdescribes current code. docs/export.md:3 documents a removed feature as if it existed, and README.md:3 propagates it. This is exactly the docs_fog evidence class — "docs that misdescribe current code, removed-feature docs" — and SKILL.md's ghost-feature reasoning maps "documentation is stale (feature was removed...)" to the docs_fog candidate.
- **Not architecture_fog**: no structural defect — the surviving code (app.py:1-5) is coherent, runnable, and its flow is fully traceable; nothing in the architecture prevents the export feature from existing (it simply was not implemented).

## 7. Evidence
The decisive contradiction is docs-vs-code (Pass E): docs/export.md:3 instructs running `` `python app.py export --format csv` `` to export all records, while app.py:1-5 — the complete code surface, exhaustively inventoried — defines only `ingest()` (app.py:1-2) and a `__main__` guard (app.py:4-5) with no argument parsing and no CSV output. On the other side of the boundary, README.md:1 titles the repo `# removed-feature` — corroborating that the export feature was removed — and README.md:3 links to the stale export doc, propagating the ghost transitively. The surviving behavior is a single stdout print (app.py:2). No frontend code exists, ruling out ui_fog; no manifest or packaging metadata exists, so there is no dependency surface to analyze; no tests or CI exist (Pass D), so nothing machine-checkable would catch a future recurrence of removed-feature docs.

**Logic trace:** The documentation is the repo's declared interface (docs/export.md:3 asserts an `export --format csv` command that "exports all records"; README.md:3 points readers at it). The code is the implemented interface (app.py:1-2 has only `ingest()`, app.py:4-5 handles no arguments, and the 3-file inventory leaves no other module that could implement export). Declared surface ≠ implemented surface on exactly one item — the export command — which satisfies the Ghost Features definition ("Functionality mentioned in documentation that has no corresponding implementation", weakness-types.md:7). Because the mismatch lives in the documentation (a removed feature whose docs survived, per the repo title at README.md:1), not in the product contract (the README promises nothing) and not in the architecture (the surviving code is coherent), the fog is docs_fog. The ghost export command at docs/export.md:3 is the weakest boundary: it would mislead every reader of the repo's only documentation into running a command that silently does the wrong thing.

## 8. Evidence excerpts

```yaml
evidence_excerpts:
  - file: docs/export.md
    lines: L3
    quote: "`python app.py export --format csv` exports all records."
    supports_claim: "The repository's only documentation instructs running an 'export' CLI subcommand that app.py does not implement."
  - file: app.py
    lines: L1-L2
    quote: "def ingest():\n    print('ingest')"
    supports_claim: "The entire code surface is one function, ingest(); there is no export function and no CSV logic."
  - file: app.py
    lines: L4-L5
    quote: "if __name__ == '__main__':\n    ingest()"
    supports_claim: "The only entry point runs ingest(); a documented 'app.py export --format csv' invocation would silently execute this block and print 'ingest' because no argument handling exists."
  - file: README.md
    lines: L1-L3
    quote: "# removed-feature\n\nSee [export docs](docs/export.md)."
    supports_claim: "The README title 'removed-feature' corroborates that the export feature was removed, and the link propagates the stale export doc; the README makes no product promise (rules out product_fog)."
  - file: app.py
    lines: L2
    quote: "    print('ingest')"
    supports_claim: "The implemented behavior is a placeholder print; the documented 'exports all records' output has no counterpart in code."
```

## 9. Why this boundary matters
If the ghost export documentation stays, every consumer of the repository is misled at the first read: a human or agent following docs/export.md:3 runs `python app.py export --format csv` and receives `'ingest'` printed to stdout — the wrong output, with no error, so the failure is silent and indistinguishable from success. Any downstream work planned from the docs (export consumers, data pipelines, "all records" schemas) targets a surface that does not exist. Because README.md:3 links the stale doc, the ghost is propagated from the repository's front page. The defect is invisible to automated checks — there are none (Pass D) — so it survives until a human or agent actually executes the documented command or audits docs against code (Pass E). Unfixed, it also normalizes the pattern: documentation that outlives its feature will mislead again.

## 10. Candidate next steps
1. **Reconcile the docs with the code**: rewrite docs/export.md:3 (and the README.md:3 link) to describe the actual interface — `python app.py` prints `'ingest'` — or delete the stale export doc if the feature is permanently removed; the smallest direct fix at the boundary.
2. **Confirm the intent with the owner**: decide whether `export` is a removed feature (fix = delete/update docs) or a promised-but-missing one (fix = re-implement the subcommand in app.py) — the only genuine fork in this diagnosis; the fixture provides no user intent.
3. **If export should exist, re-add it properly**: an `argparse`-based `export` subcommand honoring `--format csv` (app.py), with a test proving the CSV output — converting the ghost feature into a real one.
4. **Add a smoke test for the entry point** (app.py:4-5) so the only observable behavior (`python app.py` → `'ingest'`) is machine-checked.
5. **Add a docs-vs-code consistency check** (e.g., a CI step that greps documented CLI invocations against actual entry points) so removed-feature documentation cannot silently return.

## 11. Recommended next step
Step 1 — reconcile the documentation with the code: update docs/export.md:3 to describe the actual command (`python app.py`, which prints `'ingest'`) and fix the README.md:3 link accordingly — or, if the owner confirms the feature is permanently gone, delete docs/export.md and the link. The contradiction is already proven (docs/export.md:3 vs app.py:1-5, both fully read), so this is a small docs edit, not an investigation. It is the smallest action with the highest leverage at the weakest boundary: it makes the repo's only documentation truthful, unblocks every reader of the docs, and any later decision to re-implement export (Step 3) then happens against an honest baseline. Execution should be routed through the workflow in Section 12 rather than done ad hoc, and Step 2 (intent confirmation) should precede it if the owner is reachable.

## 12. Recommended workflow
`docs-implementation-workflow` (ID verified against `skills/workflow-planner/references/workflow-registry.yaml`), with `recommended_execution_mode: guided_execution` — one of that workflow's `allowed_execution_modes` (workflow-registry.yaml:822-824 lists guided_execution and autonomous_execution). Rationale: `primary_fog_type` is `docs_fog`, and docs-implementation-workflow exists precisely "For documentation/knowledge problems. Aligns domain understanding, creates documentation architecture, and generates docs" (workflow-registry.yaml:813-815); the weakest boundary is a stale/removed-feature doc (docs/export.md:3), a documentation defect. Closest alternatives rejected: `docs-contract-reconciliation` (workflow-registry.yaml:127-159 — resolves drift between documentation, registries, artifact contracts, templates, and validator rules, i.e., the sensemaking framework's own doc/contract surface via sensemaking-docs-reconciler; not applicable to a standalone utility repo's stale feature doc); `implementation-workflow` (the generic default, workflow-registry.yaml:587-599 — would work but lacks the docs-focused spec step); `product-implementation-workflow` (no product promise is broken — README.md:3 promises nothing); `ui-implementation-workflow` (no frontend); `fast-path-workflow`/`full-fog-workflow` (chaining wrappers that re-run sensemaking and auto-invoke; unnecessary given the high-confidence diagnosis). Note on execution mode (GAP-7): `plan_only` is NOT an allowed mode for this workflow — it is not listed in workflow-registry.yaml:822-824 — so `guided_execution` (human-gated, diagnostic-compatible) is the correct choice rather than inventing `plan_only`. Preconditions: none missing — this brief supplies the diagnosis; the workflow's docs-aligner step can consume it as context.

## 13. Machine-readable handoff

```yaml
artifact_id: repository_sensemaking_brief
schema_version: 1
target_repo: experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-removed-feature-docs
workflow_registry_source: skills/workflow-planner/references/workflow-registry.yaml
source_intent_ref: artifacts/01-orchestration-run/00-user-intent.md
user_implied_fog_type: unknown
primary_fog_type: docs_fog
diagnosis_conflict: false
escalation_recommended: false
escalation_required: false
evidence:
  - "docs/export.md (L3): '`python app.py export --format csv` exports all records.' — documents an export command with no implementation in app.py"
  - "app.py (L1-L5): the complete code surface — only ingest() and a __main__ guard; no export subcommand, no argument parsing, no CSV code"
  - "README.md (L1): title '# removed-feature' corroborates the export feature was removed"
  - "README.md (L3): links to docs/export.md, propagating the stale export doc; makes no product promise (rules out product_fog)"
recommended_workflow_id: docs-implementation-workflow
recommended_execution_mode: guided_execution
weakest_boundary: Ghost Features
weakness_type: Ghost Features
weakness_type_explanation: null
required_inputs:
  - user_intent
  - repository_state
created_at: "2026-08-07T05:00:00Z"
immutable: true
```

## 14. Ready-to-copy prompt
"Run `docs-implementation-workflow` (mode: guided_execution) against the adv-removed-feature-docs repository (`experiments/repository-sensemaking-skill-hardening-v1/corpus/adv-removed-feature-docs`) using the `repository_sensemaking_brief` (primary_fog_type: docs_fog; weakest boundary: Ghost Features — a documented feature with no implementation). Scope: reconcile the repository's documentation with its actual interface — docs/export.md:3 instructs running `` `python app.py export --format csv` `` to 'export all records', but app.py:1-5 implements only `ingest()` (prints `'ingest'`) with no export subcommand, no argument parsing, and no CSV output, and README.md:3 links to the stale export doc; the repo title (`# removed-feature`, README.md:1) confirms the export feature was removed. Deliverable: a documentation update that makes docs/export.md (and the README.md:3 link) describe the real command (`python app.py` → prints `'ingest'`), or removes the stale export documentation if the owner confirms the feature is permanently gone. Do not re-implement the export subcommand in this pass; if the owner intends export to exist, flag it as a follow-up product decision."
