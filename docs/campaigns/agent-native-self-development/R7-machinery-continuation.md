# R7 - Implementation-class continuation on product machinery (D12)

```
STATUS:     COMPLETE (both campaign(R7) commits exist; see section 7)
CONTEXT:    fresh context; only input = CAMPAIGN-STATE.md path (record v8)
BRANCH:     campaign/agent-native-self-development @ e702b31 at start
WORKTREE:   H:/GithubRepositories/smk-campaign
DATE:       2026-09-02
AUTHORITY:  non-authoritative campaign report (verbatim from the fresh context)
```

## 1. Summary

- Responsibility identified from the record: R7 (section 10) - repair the
  hard top-level `import workflow_liveness` in `scripts/_validator_utils.py`
  with a lazy resolver and add a regression test file. Performed as
  specified in steps 1-7; no other file touched; no push; no branch change;
  CAMPAIGN-STATE.md not edited.
- Defect D12 VERIFIED against code and tests: `_validator_utils.py:13`
  `import workflow_liveness` fails in both loading modes the record names
  (package import from the repository root; copied file in a fixture
  `scripts/` dir run as a subprocess). The hard import arrived in `4b42263`
  (2026-09-01), as the record claims.
- Repair: `+33/-4` in `scripts/_validator_utils.py` (one new `import
  importlib.util`, a 29-line `_workflow_liveness()` resolver with a module
  cache, and three call sites `workflow_liveness.X(` -> `_workflow_liveness().X(`).
  New file `tests/test_validator_utils_liveness_import.py` (149 lines, ASCII,
  LF; three fresh-interpreter tests). Both commits carry the required trailer.
- Result: `tests/test_validator_utils.py` collects again; the two
  `test_mode_coverage_aggregation.py` failures pass; the new file passes 3/3;
  `validate-repo.py` exit 0 before and after; `test-validators.py` 78/78
  before and after (output byte-identical except the `Generated:` timestamp);
  liveness selection unchanged for pre-existing tests; direct execution
  resolves the same `workflow_liveness` module object as before and
  `validate-plan.py` still rejects a compatibility-only chosen workflow
  (WORKFLOW_NOT_FOUND, lines 124-138). All results identical under cp1252 and
  `PYTHONUTF8=1`.
- RECORD DISCREPANCY (material to the record's predicted outcome, not to the
  defect): `test_load_workflow_registry_loads_yaml` has a SECOND, independent
  failure cause the record does not mention - its expected dict
  `{"workflows": [{"id": "test"}]}` predates ADR 0027's `liveness` annotation
  (commit `4b42263`); once importable it fails with `AssertionError:
  {'workflows': [{'id': 'test', 'liveness': 'active'}]} != {'workflows':
  [{'id': 'test'}]}`. The authorized repair cannot make it pass and editing
  existing tests is NOT AUTHORIZED, so it remains red (1 of the 3 named
  tests). The record's "expect 51 failed / 2 errors" after R7 is therefore
  wrong: expect 52 failed (only the two mode-coverage tests flip; see section
  4 F2 for the error-count caveat). This is a D2(b)/U8-class expectation
  drift and needs a dispatcher/owner disposition; I did not silently correct
  it.
- Judgment call: I did NOT stop under stop condition 2 ("step-2 reproduction
  differs materially"). The reproduction of the defect matched (same error,
  same line, same three tests affected, same two loading modes); what differs
  is pytest's reporting shape and the after-state prediction for one test.
  Every authorized action remained warranted and verifiable, so I performed
  it and flagged the discrepancy. If the dispatcher reads the stop condition
  more strictly, both commits are local and revertable.
- Counts: 46 tool calls (incl. the report write and commit calls); 21 files
  opened (9 named by the record incl. the record itself; 12 beyond it,
  section 9).

## 2. Responsibility, authority, and boundaries as read from the record

- CURRENT / NEXT WARRANTED RESPONSIBILITY: R7 (record section 10).
- Authority granted (record section 10 "AUTHORITY FOR R7", verified against
  the cited sources): CHARTER.md lines 138-143 ("LOCAL DEFECT ... may still be
  selected if resolving it materially advances a campaign capability"), 315
  ("add appropriate regression tests"), 447/449 ("bounded implementation",
  "test-harness improvement"); AGENTS.md rules 3 ("Simplest warranted
  solution first") and 4 ("Don't touch unrelated code"); ADR 0027 "Consumer
  behavior" (validators fail closed on non-active workflows) bounds the repair.
- Explicitly NOT authorized: editing any other file under scripts/, src/,
  skills/, docs/, .github/; registries, overlays, contracts, ADRs; editing
  existing tests; weakening liveness enforcement; pushing; merging; tracker
  writes; editing CAMPAIGN-STATE.md. All respected. The only docs/ write is
  this report, which step 7 names explicitly.
- Instructions found in files: none beyond the record. The main checkout's
  CLAUDE.md (injected by the harness) says agents invoke `/skill
  using-sensemaking`; the harness rules for this trial forbid Skill
  invocation and I invoked none.

## 3. Reproduction (step 2, BEFORE any change)

Record command, `PYTHONUTF8=1 PYTHONPATH=src python -m pytest
tests/test_validator_utils.py tests/test_mode_coverage_aggregation.py -q -p
no:cacheprovider` (identical under the default code page):

```
tests\test_validator_utils.py:6: in <module>
    from scripts._validator_utils import (
scripts\_validator_utils.py:13: in <module>
    import workflow_liveness
E   ModuleNotFoundError: No module named 'workflow_liveness'
ERROR tests/test_validator_utils.py
!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.54s        (exit 2)
```

So the record's expected "exactly the three failures" is not what this
invocation produces: the test module errors at COLLECTION and pytest
interrupts before `test_mode_coverage_aggregation.py` runs. Adding
`--continue-on-collection-errors` (the flag the record's own C11 procedure
uses) gives the full picture:

```
FAILED tests/test_mode_coverage_aggregation.py::test_validator_passes_after_legitimate_update
FAILED tests/test_mode_coverage_aggregation.py::test_missing_run_log_path_still_flagged
ERROR tests/test_validator_utils.py
2 failed, 5 passed, 1 error in 3.64s
```

with, for both mode-coverage tests, the subprocess traceback:

```
File "...\pytest-14291\test_validator_passes_after_le0\scripts\validate-mode-coverage.py", line 24, in <module>
    from _validator_utils import format_error, load_yaml, load_artifact_contracts
File "...\pytest-14291\test_validator_passes_after_le0\scripts\_validator_utils.py", line 13, in <module>
    import workflow_liveness
ModuleNotFoundError: No module named 'workflow_liveness'
```

(`test_missing_run_log_path_still_flagged` gets `code != 0` for the wrong
reason and then fails `assert "RUN_LOG_NOT_FOUND" in output`.)

Reversing the file order (`test_mode_coverage_aggregation.py` first, which
inserts `scripts/` into `sys.path` at import) lets `test_validator_utils.py`
collect and exposes the hidden second cause:

```
___________________ test_load_workflow_registry_loads_yaml ____________________
>       assert result == {"workflows": [{"id": "test"}]}
E       AssertionError: assert {'workflows':...': 'active'}]} == {'workflows':...id': 'test'}]}
E         {'workflows': [{'id': 'test', 'liveness': 'active'}]} != {'workflows': [{'id': 'test'}]}
tests\test_validator_utils.py:69: AssertionError
3 failed, 17 passed in 3.73s
```

Mechanism confirmed from code: no `scripts/__init__.py`, no conftest, no
pytest config; `python -m pytest` puts the cwd (repo root) on `sys.path`, so
`scripts` resolves as a PEP 420 namespace package and
`scripts._validator_utils` imports, but `scripts/` itself is not on
`sys.path`, so the bare `import workflow_liveness` fails. Direct script
execution works only because Python sets `sys.path[0]` to `scripts/`.

Other BEFORE references (both code pages identical):

- `python scripts/validate-repo.py` -> exit 0 ("Validation passed! ...").
- `python scripts/test-validators.py` -> exit 0; Total Cases 78, Passed 78,
  Failed 0, Missing Required Regressions 0, Coverage Failures 0.
- `PYTHONPATH=src python -m pytest tests -q -k liveness -p no:cacheprovider`
  -> `ERROR tests/test_validate_brief_json.py - FileNotFoundError ...
  scripts\validate_brief.py`; `Interrupted: 1 error during collection`; exit 2
  (pre-existing D2(b)/U8). With `--continue-on-collection-errors`: `8 passed,
  2790 deselected, 1 error`; exit 1.
- Combined step-5 selection (the four existing files): as written ->
  interrupted by the same collection error, exit 2; with
  `--continue-on-collection-errors` -> `2 failed, 28 passed, 1 skipped, 1
  error`; exit 1.
- `git status` at session start: `M src/sensemaking_skills.egg-info/PKG-INFO`,
  `M src/sensemaking_skills.egg-info/SOURCES.txt` (pre-existing, not mine).

## 4. Where the record was wrong, insufficient, or ambiguous (flagged, not fixed)

- F1 (reporting shape). Step 2 predicts "exactly the three failures ... each
  with ModuleNotFoundError". Actual: one collection ERROR + session
  interrupt; the two mode-coverage FAILUREs appear only with
  `--continue-on-collection-errors` or when the mode-coverage file runs
  first. Same defect, different pytest accounting.
- F2 (material to the predicted outcome). `test_load_workflow_registry_loads_yaml`
  fails for two independent reasons: the import (fixed by R7) and an
  expectation that predates ADR 0027's `liveness` annotation (not fixable
  within R7 authority). It remains red after the repair. Consequences:
  (i) the requirement "the three failing tests must pass unmodified" is
  satisfiable for 2 of 3; (ii) the EXPECTED EVIDENCE "baseline 54 failed / 2
  errors -> expect 51 failed / 2 errors" should read 52 failed. Error-count
  caveat: in the full alphabetical suite, sibling modules insert `scripts/`
  into `sys.path` before `test_validator_utils.py` is imported, so the
  baseline almost certainly counted this test as a FAILURE (AssertionError),
  not a collection error - consistent with the record naming the test id -
  hence "2 errors" likely stays; I could not run the full suite (harness
  rule) so this is an inference for the dispatcher's like-for-like run.
  Disposition suggestion (not applied): treat as D2(b)/U8-class fixture/
  expectation drift; the one-line test fix is an owner/dispatcher decision.
- F3 (liveness selection). `-k liveness` over `tests` as written cannot
  produce a pass/fail set on this machine before or after (interrupted by
  D2(b)); I report both the as-written result and the
  `--continue-on-collection-errors` result. Note the new test file's name
  matches `-k liveness`, so the after-count rises by exactly 3.
- F4 (`validate-repo.py`). Step 5 says `validate-plan.py` and
  `validate-repo.py` "still import _validator_utils". `validate-repo.py` does
  NOT import it (imports: os, yaml, sys, re, pathlib; it has its own overlay
  checks at lines 115-160) - it reaches `_validator_utils` only indirectly by
  running `scripts/validate-plan.py` as a subprocess (line 489).
  `validate-plan.py` imports it at line 13. `git grep -n "_validator_utils"
  -- scripts` (a step-1 command) already shows this.
- F5 (worktree state). "git diff --stat -> exactly 2 files" was never
  achievable: the worktree already carried two modified egg-info files at
  session start. I staged my two files explicitly and left those untouched;
  `git show --stat HEAD` for commit 1 is exactly 2 files.
- Verified-correct record claims: line ~13; `git log -S` -> `4b42263
  2026-09-01 feat(workflows): expose catalog and operational registry views`;
  "Not in CI" (validation.yml runs named test files only; none of the three);
  `validate-mode-coverage.py` imports only `format_error, load_yaml,
  load_artifact_contracts` (line 24).
- Incidental (no action, outside scope): top-level `tests/fixtures/plan-valid.md`
  fails the current `validate-plan.py` (SECTION_11_MALFORMED and a
  compatibility-only `chosen_workflow_id`); `test-validators.py` uses
  per-validator fixture subdirectories, so this is not in its 78 cases.

## 5. The repair and why it is the simplest that satisfies the spec

`scripts/_validator_utils.py` (`+33/-4`):

- `import importlib.util` added; the top-level `import workflow_liveness`
  removed.
- `_WORKFLOW_LIVENESS = None` cache and `_workflow_liveness()`: (i) try
  `import workflow_liveness`; (ii) on `ImportError` load
  `workflow_liveness.py` from `os.path.dirname(os.path.abspath(__file__))`
  via `importlib.util.spec_from_file_location` / `module_from_spec` /
  `exec_module`; (iii) if that file is absent raise `ImportError("No module
  named 'workflow_liveness' and sibling file not found: <path>")` (`from
  None`). The resolved module is cached; nothing is registered in
  `sys.modules`.
- The three call sites in `load_workflow_liveness`, `load_workflow_catalog`,
  `load_workflow_registry` call `_workflow_liveness().<fn>` instead of
  `workflow_liveness.<fn>`. Public names and signatures unchanged; no other
  edits; LF preserved (0 CRLF).

Why simplest: it is the literal shape the record specifies (steps 3 i-iii),
adds no configuration, no `sys.path` mutation (which would leak into
callers), no `sys.modules` registration (which could shadow a later real
import), and no new dependency. Direct script execution takes path (i) and
gets the identical module object it got before (verified, section 6). No
existing test or `src/` module referenced a `_validator_utils.workflow_liveness`
attribute (grep over tests/, src/, scripts/: none), so removing the module
attribute breaks nothing.

`tests/test_validator_utils_liveness_import.py` (new, 149 lines): each test
runs `sys.executable -c` in a fresh interpreter with the real `scripts/`
directory stripped from `sys.path` and asserts
`importlib.util.find_spec("workflow_liveness") is None` before exercising the
path under test; child output is ASCII JSON (`json.dumps`), so cp1252 and
UTF-8 behave identically. (a) `import scripts._validator_utils` with the
repository root inserted on `sys.path`; `load_workflow_liveness(repo_root)`
equals `yaml.safe_load` of `skills/workflow-planner/references/
workflow-liveness.yaml` (read with `encoding="utf-8"`). (b) a copy without
`workflow_liveness.py` loads via `spec_from_file_location`, `format_error`
works, and `load_workflow_liveness` raises `ImportError` whose message
contains `workflow_liveness`. (c) a copy with the sibling resolves through
the sibling (`_workflow_liveness().__file__` equals the copied sibling path;
`"workflow_liveness" not in sys.modules`), returns the overlay, and its
operational view equals the catalog minus the overlay's `compatibility_only`
ids (ADR 0027 fail-closed filter preserved through the fallback path).

## 6. Verification (step 5) - exact before/after under both code pages

All commands run with `PYTHONPATH=src` and `-p no:cacheprovider`; "default"
= cp1252 console, "utf8" = `PYTHONUTF8=1`. Results were identical under both
code pages in every row.

| Command | BEFORE (default / utf8) | AFTER (default / utf8) |
|---|---|---|
| `pytest tests/test_validator_utils.py tests/test_mode_coverage_aggregation.py -q` | `1 error` (collection), Interrupted, exit 2 | `1 failed, 19 passed`, exit 1 - the one failure is `test_load_workflow_registry_loads_yaml` AssertionError (F2) |
| same + `--continue-on-collection-errors` | `2 failed, 5 passed, 1 error`, exit 1 | `1 failed, 19 passed`, exit 1 |
| `pytest tests/test_validator_utils_liveness_import.py -q` | n/a (file did not exist) | `3 passed`, exit 0 |
| `pytest tests/test_validator_utils.py tests/test_mode_coverage_aggregation.py tests/test_validator_utils_liveness_import.py tests/test_path_drift.py tests/test_cli.py -q` | (4 existing files) as written: Interrupted, exit 2; with flag: `2 failed, 28 passed, 1 skipped, 1 error`, exit 1 | `1 failed, 45 passed, 1 skipped`, exit 1 (the F2 test only; no collection error; nothing else red) |
| `pytest tests -q -k liveness` as written | `ERROR tests/test_validate_brief_json.py` (D2b), Interrupted, exit 2 | identical: same error, Interrupted, exit 2 |
| `pytest tests -q -k liveness --continue-on-collection-errors` | `8 passed, 2790 deselected, 1 error`, exit 1 | `11 passed, 2790 deselected, 1 error`, exit 1 (the +3 are the new file; 0 failed both times) |
| `python scripts/validate-repo.py` | exit 0, "Validation passed!" | exit 0, "Validation passed!" |
| `python scripts/test-validators.py` | exit 0; 78/78 passed | exit 0; 78/78 passed; `diff` of full outputs: only the `Generated:` timestamp line differs |

Step-5 last bullet (direct execution still imports `_validator_utils` and
still enforces liveness), code paths checked and exercised:

- `scripts/validate-plan.py` line 13 imports `load_workflow_registry`; lines
  124-138 call it (operational, active-only view) and emit
  `WORKFLOW_NOT_FOUND` when `chosen_workflow_id` is absent from that view;
  lines 461-470 do the same on the JSON path. Exercised directly after the
  change: `python scripts/validate-plan.py tests/fixtures/plan-valid.md
  --repo-root .` -> `ERROR [unknown_value] chosen_workflow_id:
  WORKFLOW_NOT_FOUND: Workflow ID 'product-implementation-workflow' not found
  in registry.` and `ERROR [logic_error] None: WORKFLOW_NOT_FOUND:
  chosen_workflow_id 'product-implementation-workflow' not found in
  workflow-registry.yaml` (exit 1). `product-implementation-workflow` is
  `compatibility_only` in the overlay.
- Direct-execution probe from `scripts/` (`sys.path[0] = scripts/`, as a
  validator run directly): after `import _validator_utils`,
  `'workflow_liveness' in sys.modules` is False (deferred); after the first
  liveness call it is True; `_workflow_liveness() is
  sys.modules['workflow_liveness']` is True (path (i), same object as the old
  top-level import); catalog 23 workflows, operational 15; the 8
  `compatibility_only` ids are annotated in the catalog and absent from the
  operational view.
- `scripts/validate-repo.py`: exit 0 before and after; it enforces the
  overlay itself (lines 115-160) and runs `validate-plan.py` as a subprocess
  (line 489) - see F4.

## 7. Commits (local only; not pushed)

1. `79e02c5` `campaign(R7): lazy-resolve workflow_liveness in
   scripts/_validator_utils.py` - `scripts/_validator_utils.py` (+33/-4),
   `tests/test_validator_utils_liveness_import.py` (+149, new); 2 files,
   +182/-4.
2. this report (`campaign(R7): report for the D12 machinery continuation`):
   hash in the final message and in `git log`.

Branch `campaign/agent-native-self-development`, base `e702b31`. Not pushed;
CAMPAIGN-STATE.md not edited; the two pre-existing egg-info modifications
remain unstaged and untouched.

## 8. What the record was sufficient for

- Identifying the responsibility, its authority sources (all verified in the
  cited files), and every boundary; no authority question arose.
- Locating the defect, the affected tests, the loading modes, the functions
  involved, and the ADR 0027 constraint.
- The exact shape of the repair and of the regression tests; the exact
  verification commands and the encoding discipline (C5); the commit
  convention; the stop conditions.
- The like-for-like discipline (C9/C11) is what caught F1-F5: every
  dispatcher-computed claim was rebuilt before use, as the record asks.

## 9. Files consulted beyond the record's step-1 list, and why

Named by the record (9, incl. the record): CAMPAIGN-STATE.md;
scripts/_validator_utils.py; scripts/workflow_liveness.py;
scripts/validate-mode-coverage.py (imports); tests/test_mode_coverage_aggregation.py
(lines 1-70, 120-150, 278-320); tests/test_validator_utils.py; docs/adr/0027
("Consumer behavior"); CHARTER.md (cited lines); AGENTS.md (rules 3-4).

Beyond the record (12):

- `.github/workflows/validation.yml` (grep) - confirm "Not in CI" for the three tests.
- `skills/workflow-planner/references/workflow-liveness.yaml` - shape/path for tests (a) and (c).
- `scripts/validate-plan.py` (grep; lines 124-139) - cite the fail-closed code path (step 5).
- `scripts/validate-repo.py` (imports; grep) - the record's F4 claim; how it reaches `_validator_utils`.
- `src/sensemaking_skills/registry.py` (grep) - does `src/` rely on a `_validator_utils.workflow_liveness` attribute? (No: own implementation.)
- `.gitattributes` + `git config core.autocrlf` - line-ending preservation (autocrlf=false; file is LF).
- `tests/fixtures/plan-valid.md`, `plan-invalid-semantic-conflict.md`, `plan-invalid-empty-workflow-steps.md` (grep `chosen_workflow_id`) - find a compatibility-only plan for the direct-exec probe.
- `scripts/test-validators.py` (grep) - fixture layout (why plan-valid.md is not among its cases).
- pytest configuration check (`scripts/__init__.py`, `tests/conftest.py`, `pytest.ini`, `pyproject.toml [tool.pytest]`: none exist) - explain how `scripts._validator_utils` resolves (namespace package via cwd).

Tool calls: 46 (1 Read + 1 Write + 44 Bash). One Bash call failed at
shell-parse time while writing this report (a quoting collision in a long
heredoc) and executed nothing; the report was then written with the Write
tool. No Skill invoked; no workflow or runtime script run; no full suite run.

## 10. Authority questions

None required an owner. One judgment call recorded in section 1 (proceeding
past stop condition 2 because the defect reproduction matched and every
authorized action stayed warranted). One item needs a dispatcher/owner
disposition: the F2 expectation drift in `tests/test_validator_utils.py::
test_load_workflow_registry_loads_yaml` (a one-line test fix that R7 was not
authorized to make).

## 11. Skipped / not done / limitations

- Full like-for-like suite and CI: not run (harness rule; dispatcher audit).
- The three named tests do not all pass: 2 of 3 do; the third fails for the
  independent reason in F2 and was not edited.
- `-k liveness` as written cannot produce a comparable set on this machine
  (D2b); compared with `--continue-on-collection-errors` instead.
- The two pre-existing egg-info modifications were not investigated beyond
  confirming they predate this session and are outside R7 authority.
- Linux behavior of the new tests is asserted by design (fresh interpreter,
  path normalization, ASCII JSON), not observed; CI on the pushed head is
  the referee.
