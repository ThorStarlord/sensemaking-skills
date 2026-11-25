# Pre-change source context (2026-11-25)

**Status:** product-capability increment and one authentic use.
**Source baseline:** `f780bfad2bc542fcba438b320b12ef8cb5b448c7`.
**Implementation:** `bf29c4753ce7f9cea175a0266a538aaa93c2bbf6`.

The capability adds committed Python source relationships to the existing
`context-for` path consumer. It does not establish runtime dependency, test
coverage or change safety.

## 1. Observed limitation

The existing `semantic workspace-query --operation context-for` returned
authored ownership, rules, contracts, decisions, history and verification for
a path. For `src/sensemaking_skills/method_trial.py` it returned one applicable
rule, one lesson and one verification reference, but no code-level importers,
top-level symbols or test references. An agent preparing a change had to run
manual searches to discover that `src/sensemaking_skills/semantic_cli.py` was
the only direct importer.

Related surfaces did not close the gap:

- `impact-preview` is a literal source/term search; it returns candidate paths,
  not resolved import relationships.
- `workspace-review-context` requires an existing committed or working diff.
- `rules-for` and the authored `context` are explicit reviewed relationships,
  not derived code structure.

## 2. Delivered capability

```bash
sensemaking-skills semantic workspace-query --repo . --ref HEAD \
  --operation context-for src/sensemaking_skills/<module>.py \
  --include-source-relationships --json
```

The opt-in `source_relationships` section reads a clean temporary checkout of
the exact revision and adds:

- target path, exact revision and SHA-256 of the committed target bytes;
- direct imports, with repository paths resolved where tracked;
- direct importers, with line and imported names;
- test references by import or literal path/module mention;
- top-level public and private symbols;
- parse failures, coverage status and explicit limits;
- bounded counts and truncation.

It is available only on `workspace-query` `context-for`, currently for one
tracked `.py` path. The authored `context` remains unchanged. A parse failure
or list overflow sets `truncated`/`PARTIAL` rather than silently omitting
records.

## 3. Authentic use

**Task:** establish the code-level consumer surface before changing the
method-trial path context and its new source-relationship module.

Observed on `src/sensemaking_skills/method_trial.py`:

- one direct importer: `src/sensemaking_skills/semantic_cli.py` at line 1118,
  importing `open_method_trial`, `close_method_trial`,
  `build_method_trial_view` and `trial_ancestry`;
- nine direct imports, including resolved paths for
  `method_adaptation.py` and `semantic_architecture/knowledge.py`;
- thirteen top-level functions, including the four public functions above;
- no test file that directly imports or mentions the path;
- coverage `COMPLETE_FOR_PYTHON_AST`, no truncation.

Observed on `src/sensemaking_skills/workspace_knowledge.py`:

- direct importers `campaign_capability_bridge.py` and `semantic_cli.py`;
- no test file that directly imports or mentions the path;
- the additive `include_source_relationships=False` parameter therefore has two
  known direct callers, and the new call site is the CLI consumer.

Observed on `src/sensemaking_skills/semantic_architecture/source_relationships.py`
after implementation:

- one direct importer: `workspace_knowledge.py` at line 27;
- no test file that directly imports or mentions the path;
- one public function (`build_source_relationships`) and nine private helpers; the field is `top_level_symbols` with a `public` marker.

**Decision informed:** because the new module has no direct test reference, the
verification was placed in the existing hosted source-pinned consumer, which
exercises the real CLI on `method_trial.py` and asserts the direct importer and
public surface. The empty test list is a reference gap, not proof that no test
exercises the behavior through another route.

The design choice to extend `context-for` rather than add a new command was
made from source inspection before the new consumer existed; the capability
itself did not cause that choice. Its observed contribution was the later
confirmation of the direct consumer surface and the verification decision.

## 4. What the product provides versus the model

**Product:** an exact-revision clean checkout, Python AST parsing, import
resolution against tracked modules, importer/test/definition extraction,
bounded counts, hashes, parse-failure disclosure and explicit limits.

**Model:** selected the path and change question, read the authored context,
interpreted the importers and test references, decided that a hosted CLI check
was the appropriate verification, and retained the evidence. The product did
not decide whether the change was safe or valuable.

No intrinsic cognitive improvement or comparative benefit is claimed.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Exact-revision source relationships | Observed through the real CLI |
| Direct importer and public-surface extraction | Observed on three real modules |
| Clean-commit byte identity | Observed through the temporary checkout and SHA-256 |
| Parse-failure and truncation disclosure | Observed with a one-item limit |
| Test reference detection | Observed as syntax/path mention only; empty means NOT_ASSESSED |
| Runtime dependency or call graph | NOT ASSESSED |
| Test coverage | NOT ASSESSED |
| Change safety or impact verdict | NOT ESTABLISHED |
| Independent later-agent reuse or better decisions | NOT ESTABLISHED |

## 6. Continuation

The next warranted use is an independent agent applying the consumer to an
unfamiliar subsystem before a real change, then recording whether the
importers/tests changed its verification or implementation. No further schema,
planner or mandatory pre-edit stage is warranted without that use. A justified
`NO_CODE_CHANGE` remains valid.
