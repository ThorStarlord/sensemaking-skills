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
- the public surface is not yet known.

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
| `direct_imports` | Import statements in the target, with repository paths resolved where the imported module is tracked. |
| `direct_importers` | Non-test Python files that import the target, with line and imported names. |
| `test_references` | Test files that import the target or literally mention its path/module. |
| `top_level_symbols` | Top-level functions and classes, with line and a public/private marker. |
| `parse_failures` | Files that could not be parsed; coverage becomes `PARTIAL`. |
| `coverage_status` | `COMPLETE_FOR_PYTHON_AST` or `PARTIAL`. |
| `truncated` | Whether a list or category exceeded the limit. |
| `limits` | Explicit source and claim boundaries. |

`counts` reports totals; the lists are bounded by `--limit` (default 50).

## How to use it in a change

1. Read the authored context first. A missing owner or rule is
   `NOT_ASSESSED`, not evidence that no obligation exists.
2. Inspect each `direct_importer`. A syntactic importer can be a caller, a
   re-export, a test helper or dead code; read it.
3. Read `test_references` as references, not coverage. An empty list means no
   direct test import or path mention at this revision, not that no test
   exercises the behavior through the CLI or another module.
4. Use `public_symbols` to decide whether a signature or behavior change
   reaches a public surface.
5. Compare the code-level view with the authored verification and rules, then
   choose the actual verification. The view never authorizes the change.

## Limits

- Python AST import syntax and top-level definitions only.
- Dynamic imports, `importlib` targets, reflection, monkeypatching, runtime
  dispatch and call order are not assessed.
- Test references are syntactic mentions, not coverage or pass status.
- Only tracked Python files at the exact revision are inspected; non-Python
  references and untracked bytes are not represented.
- A missing relationship is `NOT_ASSESSED`, not absence.
- Source relationships do not establish architectural correctness, semantic
  impact or release readiness.

## Evidence ceiling

The consumer establishes that specific tracked Python files contain import
syntax or path mentions at the selected revision. It does not establish
runtime dependency, test coverage, change safety or improved agent decisions.
