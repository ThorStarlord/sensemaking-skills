# Direct symbol usage and test candidates (2026-11-25)

**Status:** product-capability increment and one authentic engineering use.
**Source baseline:** `e920a6e90d40959c7412c8068c728917fab596f9`.
**Implementation:** `38ed4c1a`.

The capability adds an optional direct symbol view to the existing
`context-for` source relationships. It identifies syntactic references and
test functions that mention one top-level symbol. It is not a runtime call
graph, transitive impact analysis or test-coverage result.

## 1. Observed limitation

The merged source-relationship view answered which files import a module and
which test files reference it. A fresh-context consumer found two consequential
limits while evaluating `knowledge_sources.py`:

- an importer list does not show which function or class is called at each
  site;
- test references are file-level, so eight referencing test files did not show
  which test functions mention `temporary_commit_checkout` or
  `build_knowledge_snapshot`.

The consumer had to inspect test bodies manually to expand a verification plan
for a change to `build_knowledge_snapshot`.

## 2. Delivered capability

```bash
sensemaking-skills semantic workspace-query --repo . --ref HEAD \
  --operation context-for src/sensemaking_skills/semantic_architecture/knowledge_sources.py \
  --include-source-relationships --symbol build_knowledge_snapshot --json
```

The new `source_relationships.symbol_context` contains:

- top-level definitions of the requested name in the target file;
- direct syntactic references outside test files, with path, line, kind
  (`CALL`, `NAME`, `ATTRIBUTE`), and target-file marker;
- test functions and `Test*` methods whose own body directly mentions the
  symbol, with reference lines;
- counts, parse failures, star-import disclosure, truncation and explicit
  limits.

The implementation resolves `from target import symbol [as alias]`,
`from package import target`, and `import target as alias` forms. It does not
resolve dotted import chains without an alias, star imports, dynamic dispatch,
inheritance or runtime calls. Test candidates are direct mentions, not
coverage; helpers, fixtures and parameterized indirect use are not mapped.

## 3. Authentic use

**Task:** prepare a change to a cross-cutting source module and choose the
verification set.

Observed on `knowledge_sources.py` for `build_knowledge_snapshot`:

- one definition at line 521;
- three direct production references:
  `semantic_cli.py:201`, `workspace_knowledge.py:211` and
  `workspace_knowledge.py:216`;
- six test-function candidates, including
  `tests/test_repository_semantic_steward.py::test_stewardship_revision_lifecycle_and_currentness`
  and two tests in `tests/test_semantic_change_classification.py`.

Observed for `temporary_commit_checkout`:

- one definition at line 91;
- five direct production references;
- zero test-function candidates, confirming the fresh consumer's observation
  that the eight file-level test references did not directly mention this
  function.

Observed for `_source`:

- one definition;
- fifteen direct references, including internal calls and cross-module calls in
  `knowledge_store.py`, `stewardship_validation.py` and `semantic_cli.py`;
- zero test-function candidates.

Observed on `method_trial.py` for `build_method_trial_view`:

- one direct call at `semantic_cli.py:1181`;
- no direct test-function candidate.

**Decision informed:** a change to `build_knowledge_snapshot` should inspect the
three production call sites and the six directly mentioning test functions; a
change to `temporary_commit_checkout` has no direct test candidate and must rely
on indirect/CLI coverage or add a focused test; `_source` is cross-module
coupling despite its leading underscore. This is a concrete verification and
inspection expansion, not merely a prettier importer list.

## 4. What the product provides versus the model

**Product:** exact-revision parsing, import alias resolution, direct reference
extraction, test-scope association, counts, truncation and explicit limits.

**Model:** selected the symbol and change question, interpreted whether a
reference mattered, chose the verification set, and retained the limits. The
product did not determine that the change was safe or that the tests cover it.

No independent reuse or comparative cognitive benefit is claimed.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Direct symbol references | Observed on real modules |
| Test-function candidate extraction | Observed on real tests |
| Distinction between direct and indirect test use | Observed: `temporary_commit_checkout` has no direct candidate |
| Runtime call graph | NOT ASSESSED |
| Transitive impact | NOT ASSESSED |
| Test coverage or pass status | NOT ASSESSED |
| Change safety | NOT ESTABLISHED |
| Independent later-agent reuse or better decisions | NOT ESTABLISHED |

## 6. Continuation

The next warranted use is an independent agent applying the symbol view to a
real refactor or signature change, then recording whether the direct references
or test candidates changed its implementation or verification. No further graph
traversal, runtime analysis or impact engine is warranted without that use. A
justified `NO_CODE_CHANGE` remains valid.
