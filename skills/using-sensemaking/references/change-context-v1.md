# Change Context v1

**Status:** optional agent-facing consumer over the existing `context-for`
query. It adds committed Python source relationships to authored repository
context. It does not produce an impact verdict, a change plan or authorization.

## When to use

Use it before a consequential change to a Python file when:

- the file is unfamiliar or cross-cutting;
- authored ownership or rules are sparse;
- the agent needs to know which tracked modules import the file;
- the agent needs to see whether tests directly reference it;
- the defined surface is not yet known.

Skip it for a trivial local edit where direct inspection already settles the
question. It is not a mandatory pre-edit stage.

## Command

```bash
sensemaking-skills semantic workspace-query --repo . --ref HEAD \
  --operation context-for src/sensemaking_skills/<module>.py \
  --include-source-relationships --json
```

The flag is opt-in and currently accepts exactly one tracked `.py` path. It
reads a clean temporary checkout of the exact committed revision, not
uncommitted bytes. Add `--symbol <name>` to inspect one top-level function or
class in that file:

```bash
sensemaking-skills semantic workspace-query --repo . --ref HEAD \
  --operation context-for src/sensemaking_skills/<module>.py \
  --include-source-relationships --symbol <name> --json
```

## Committed-change review

When reviewing an actual change rather than planning one, reuse the same
source evidence alongside the existing BASE product and architecture packet:

```bash
sensemaking-skills semantic workspace-review-context --repo . \
  --base-ref BASE --ref HEAD --source-path src/sensemaking_skills/<module>.py \
  --source-symbol <name> --json
```

The focal path must be among the selected review paths; use `--path` for
explicit scope or increase `--max-paths` if it was omitted. The optional
symbol may be omitted. `source_relationship_comparison` pairs exact committed
BASE/TARGET snapshots and reports bounded identity membership (`base_only`,
`target_only`, `both`) for modules, importer/test files, top-level symbols
and, when available, symbol reference files and test candidates. When a symbol
is selected, `symbol_behavior_comparison` also pairs its reported behavioral
surface and lists changed fields such as `signature`, `raises`, `assertions`,
`decorators`, `docstring_sha256` and `source_sha256`. Read each side's original
evidence before judging consequences. `VISIBLE_ONLY` means a list was
incomplete; differences do not establish actual additions or removals. `both`
means observed at both revisions, not unchanged behavior. A `signature` or
`source_sha256` difference is a behavioral-surface signal, not proof of a
semantic behavior change. Absent/non-regular entries and unavailable symbol
contexts are not compared as empty inventories. Authored intent remains
BASE-only. No worktree source bytes, runtime dependency, coverage, change
safety or semantic impact is inferred.

## What the output adds

The existing `context` section remains the authored view: ownership,
architecture rules, contracts, constraints, decisions, history, verification
and knowledge gaps. The top-level `source_relationships` section adds:

| Field | Meaning |
| --- | --- |
| `target` | Path, exact revision and SHA-256 of the committed target bytes. |
| `direct_imports` | Import statements in the target, with a `TRACKED` or `EXTERNAL_OR_UNRESOLVED` resolution and a repository path when tracked. |
| `direct_importers` | Non-test Python files that import the target, with line and imported names. The line is the first match; `evidence_refs` lists all matching lines. |
| `test_references` | Test files under `tests/` that import the target or literally mention its path/module. `test_reference_scope` is `FILE_LEVEL`. |
| `top_level_symbols` | Top-level functions and classes, with line, `leading_underscore` and `in_module_all` markers. |
| `leading_underscore_imports` | Names beginning with `_` imported from the target by another file, with importer, line and test/non-test marker. This is a name convention, not proof of privacy. |
| `target_parse_error` | A target syntax/decoding error. The query still returns authored context with `PARTIAL` coverage and empty target-derived imports/symbols. |
| `parse_failures` | Other files that could not be parsed; coverage becomes `PARTIAL`. |
| `coverage_status` | `COMPLETE_FOR_PYTHON_AST` or `PARTIAL`. |
| `truncated` | Whether a list or category exceeded the limit. |
| `symbol_context` | Optional direct references and test candidates for one requested top-level symbol; `null` if not requested or the target could not be parsed. |
| `limits` | Explicit source and claim boundaries. |

`counts` reports totals; the lists are bounded by `--limit` (default 50).

When `--symbol` is provided and the target parses, `symbol_context` contains:

| Field | Meaning |
| --- | --- |
| `definitions` | Top-level definitions with that name in the target file. Each carries a `behavior` surface. |
| `behavior` | Source-level signature, decorators, docstring summary/hash, direct raise/assert statements, exact definition source hash, line range and truncation. |
| `direct_references` | Direct syntactic name/attribute references outside test files, with path, line, kind and target-file flag. |
| `test_candidates` | Test functions or `Test*` methods whose own body directly mentions the symbol, with reference lines. |
| `counts` | Definitions, direct references, test candidates, parse failures and behavior truncation. |
| `star_import_observed` | Whether a scanned file star-imported the target module. |
| `test_candidate_scope` | `TEST_FUNCTION_LEVEL`. |
| `truncated` | Whether a symbol list exceeded the limit; also propagates to the enclosing source and workspace response. |

If `target_parse_error` is present, a null `symbol_context` means the
requested symbol was not assessed, not that it was absent.
`definitions` is not a stable-API list. `direct_references` is not a runtime
call graph. File-wide alias matching does not resolve lexical scope or rebinding. `test_candidates` is not coverage: a test may exercise the symbol
through a fixture, helper, parameterization or another module without a direct
mention. `behavior` is a source-level reading aid, not a semantic contract:
signature normalization is not type-checking, a docstring is not a complete
guarantee, direct raises/asserts do not cover nested or indirect behavior, and a
source hash changes for any body text edit.

## How to use it in a change

1. Read the authored context first. A missing owner or rule is
   `NOT_ASSESSED`, not evidence that no obligation exists.
2. Inspect each `direct_importer`. A syntactic importer can be a caller, a
   re-export, a test helper or dead code; read it. Check
   `leading_underscore_imports` separately: a name beginning with `_` can still
   be imported across modules, so it is not safe to rename merely because the
   name looks private.
3. Read `test_references` as file-level references, not coverage. An empty list
   means no direct test import or path mention at this revision, not that no
   test exercises the behavior through the CLI or another module.
4. Use `top_level_symbols` to see the defined surface. `leading_underscore` is a
   name convention; `in_module_all` reflects a literal module `__all__` and is
   `null` when there is none or it is dynamic. Neither establishes exported or
   stable API.
5. When changing one symbol and `symbol_context` is available, inspect
   `symbol_context.direct_references` for
   code that must be updated and `test_candidates` for tests that directly
   mention it. Confirm helper/fixture and re-export paths separately.
6. Compare the code-level view with the authored verification and rules, then
   choose the actual verification. The view never authorizes the change.

## Limits

- Python AST import syntax and top-level definitions only.
- Dynamic imports, `importlib` targets, reflection, monkeypatching, runtime
  dispatch and call order are not assessed.
- Test references are file-level syntactic mentions, not coverage or pass status.
- Re-exports through a package `__init__.py` are not resolved to the defining
  module; an importer of the package may be missing from the target's direct
  importers.
- Symbol references are direct names/attributes. Dotted import chains without
  an alias, star imports, dynamic dispatch, inheritance and runtime calls are
  not assessed. Test helpers, fixtures and indirect parameterized coverage are
  not mapped to test candidates.
- `direct_references` and `test_candidates` are syntactic evidence, not proof of
  execution, coverage, impact or change safety.
- `behavior` and `symbol_behavior_comparison` are source-level surfaces. A
  signature, decorator, docstring, raise/assert or source-hash difference is
  not automatically a semantic behavior change, and an unchanged surface is not
  proof of unchanged runtime behavior.
- A target syntax or decoding error is reported as `target_parse_error` and
  `PARTIAL`; target-derived imports/symbols are empty, while the authored
  context remains available.
- Only tracked Python files at the exact revision are inspected; symlink
  sources are refused, and non-Python references and untracked bytes are not represented.
- A missing relationship is `NOT_ASSESSED`, not absence.
- Source relationships do not establish architectural correctness, semantic
  impact or release readiness.

## Evidence ceiling

The consumer establishes that specific tracked Python files contain import
syntax or path mentions at the selected revision. It does not establish
runtime dependency, test coverage, change safety or improved agent decisions.
