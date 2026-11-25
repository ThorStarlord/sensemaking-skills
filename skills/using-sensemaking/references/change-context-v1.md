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
uncommitted bytes.

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
| `limits` | Explicit source and claim boundaries. |

`counts` reports totals; the lists are bounded by `--limit` (default 50).

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
5. Compare the code-level view with the authored verification and rules, then
   choose the actual verification. The view never authorizes the change.

## Limits

- Python AST import syntax and top-level definitions only.
- Dynamic imports, `importlib` targets, reflection, monkeypatching, runtime
  dispatch and call order are not assessed.
- Test references are file-level syntactic mentions, not coverage or pass status.
- Re-exports through a package `__init__.py` are not resolved to the defining
  module; an importer of the package may be missing from the target's direct
  importers.
- A target syntax or decoding error is reported as `target_parse_error` and
  `PARTIAL`; target-derived imports/symbols are empty, while the authored
  context remains available.
- Only tracked Python files at the exact revision are inspected; non-Python
  references and untracked bytes are not represented.
- A missing relationship is `NOT_ASSESSED`, not absence.
- Source relationships do not establish architectural correctness, semantic
  impact or release readiness.

## Evidence ceiling

The consumer establishes that specific tracked Python files contain import
syntax or path mentions at the selected revision. It does not establish
runtime dependency, test coverage, change safety or improved agent decisions.
