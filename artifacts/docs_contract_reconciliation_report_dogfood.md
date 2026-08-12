# Documentation & Contract Reconciliation Report

## 1. drift_diagnosis

The dogfood plan correctly identified a cross-platform executable handoff as
the weakest actionable boundary. The wrapper was invoked with the documented
`python` command, but its child-validator commands were hardcoded to
`python3`. On this Windows environment, the direct validator worked and the
wrapper failed before the fix.

The plan also identified secondary contract drift: `setup.py` did not declare
the runtime dependencies already present in `pyproject.toml`; the README's
short "No external dependencies" statement was broader than the package
metadata; and the relationship probe classified a version conflict as not
requiring semantic review even though its notes defer authority to the model.

## 2. weakest_boundary

The executable validation handoff remains the primary boundary to monitor.
It is now implemented through `sys.executable` in both validator-dispatch
branches of `scripts/validate-and-report.py:371-385`. This makes the child
validator use the same interpreter that launched the wrapper, independent of
whether the host exposes a separate `python3` command.

## 3. missing_instructions

- The public wrapper instructions do not state the interpreter relationship
  explicitly: the child validator must run under the parent interpreter.
- The repository does not state whether `package.json` is product metadata or
  JavaScript/tooling metadata for version-authority purposes.
- The five probe-reported validator fixture gaps are not accompanied by a
  documented policy saying whether each is intentionally waived or must gain a
  fixture.

The first item is handled in implementation by removing the hidden executable
assumption. The latter two remain owner decisions because repository evidence
does not establish the intended authority or fixture policy.

## 4. missing_examples

- A Windows smoke test for the documented wrapper command was missing. It is
  now represented by `tests/test_validate_and_report_interpreter.py`.
- There is no focused example showing a version conflict as evidence that must
  receive semantic review. The regression expectation now covers that case in
  `tests/test_probe_relationships.py:88-93`, and the valid probe-report fixture
  reflects the same contract.
- The missing-fixture list still needs either fixtures or explicit waivers for
  `validate-mode-coverage`, `validate-output`, `validate-repo`,
  `validate-run-log`, and `validate-skill-hygiene`.

## 5. validator_blind_spots

- `validate-probe-report.py` validates report shape but does not enforce the
  semantic meaning of `requires_semantic_review`.
- `gate_relationship_findings.py` correctly keeps version conflicts evidence
  only, but that policy does not itself verify the probe's review flag.
- The generic artifact validator checks contract structure; it does not decide
  whether `package.json` and Python metadata describe the same product.
- The probe measures declared checks and fixture coverage, but cannot infer
  whether an absent fixture is an intentional policy choice.

The version-relationship producer now aligns with its own notes and the
repo-sensemaker boundary rule by setting `requires_semantic_review: true`.

## 6. ambiguous_artifact_names

The historical dogfood brief and probe report have the `dogfood` suffix, while
the post-change probe is named
`artifacts/repo-sensemaker-implementation-probe-report.yaml`. This is
intentional: the original report is preserved as pre-change evidence and the
implementation report records post-change state.

The original brief is also immutable evidence. Its excerpt still quotes the
pre-fix `"python3",` source line, so it must not be rewritten merely to make
the old artifact validate against the new source. Consumers should use the
implementation probe and this reconciliation report for post-change state.

## 7. drift_risks

- A future change could reintroduce a hardcoded interpreter in another wrapper
  or test harness if the parent-interpreter convention is not reused.
- The two version families (`package.json` `4.1.0` and Python metadata `0.2.2`)
  can still mislead release or automation tooling until ownership is decided.
- Fixture coverage remains `14/19` (`0.74`) in the post-change probe, so the
  measured coverage gap is still present.
- The post-change probe still reports three ADR findings requiring semantic
  review; no ADR status was changed without owner confirmation.
- Historical documentation contains many `python3` examples. They are not
  all live wrapper contracts and were intentionally not mass-edited in this
  focused implementation.

## 8. recommended_patches

Implemented patches:

1. Use `sys.executable` for both child-validator dispatch paths in
   `scripts/validate-and-report.py`.
2. Add a regression test that launches the wrapper with the current Python
   interpreter and asserts a clean JSON validation result.
3. Replace hardcoded runtime `python3` invocations in the directly related
   validator integration harnesses with `sys.executable`.
4. Align `setup.py:55-59` with the runtime dependencies in `pyproject.toml`.
5. Narrow the README claim to "No external service dependencies in the core
   CLI".
6. Mark product-version conflicts as requiring semantic review in the probe,
   its test, and its valid report fixture.

Deferred patches requiring owner input:

1. Decide whether `package.json` `4.1.0` is authoritative tooling metadata,
   stale product metadata, or evidence of a second package identity.
2. Decide whether the five missing validator fixtures are required or waived.
3. Review ADR findings for 0018, 0019, and 0020 and update status claims only
   after authority is confirmed.

## 9. mismatches_found

The implementation addressed the plan's primary mismatch and two directly
related contract mismatches. The unresolved mismatches are intentionally
listed rather than silently resolved:

| Area | Evidence | Resolution |
| --- | --- | --- |
| Wrapper interpreter | `scripts/validate-and-report.py` | Fixed with `sys.executable`. |
| Python dependencies | `setup.py`, `pyproject.toml` | Synchronized. |
| README dependency wording | `README.md`, package metadata | Clarified to service dependencies. |
| Version authority | `package.json`, `pyproject.toml`, `setup.py` | Owner decision required. |
| Version review flag | `scripts/probe_relationships.py`, skill contract | Fixed to require semantic review. |
| Validator fixtures | Post-change probe report | Policy/fixture decision required. |
| ADR statuses | Post-change probe report | Owner semantic review required. |

## 10. changes_required

No additional code change is required for the primary wrapper failure. The
remaining changes require decisions outside mechanical reconciliation:

- ratify version authority and then update metadata or classify the second
  version family;
- ratify fixture expectations and add or waive the five missing fixtures;
- review the three ADR status findings;
- decide whether selected live documentation examples should use an explicit
  interpreter command or remain platform-specific guidance.

## 11. patches_proposed

The applied patch set is limited to the files directly implicated by the plan:

- `scripts/validate-and-report.py`
- `scripts/probe_relationships.py`
- `setup.py`
- `README.md`
- `tests/test_validate_and_report_interpreter.py`
- `tests/test_validator_integration.py`
- `tests/run_validate_and_report_tests.py`
- `tests/test_probe_relationships.py`
- `tests/fixtures/validate-probe-report/valid/sample.md`

No registry, workflow, ADR, package version, or historical artifact was
changed.

## 12. validation_result

The focused regression and relationship suites pass:

`py -3.10 -m pytest tests/test_probe_relationships.py tests/test_gate_relationship_findings.py tests/test_validate_and_report_interpreter.py tests/test_artifact_id_routing.py tests/test_validator_integration.py -q`

Result: `53 passed, 1 warning`. The warning is the pre-existing pytest warning
that `test_unified_validator_pipeline` returns an integer; it does not affect
the pass result and was outside this focused patch.

The post-change probe and its validator also pass:

`py -3.10 scripts/probe-repo.py --repo-root . --output artifacts/repo-sensemaker-implementation-probe-report.yaml`

`py -3.10 scripts/validate-probe-report.py artifacts/repo-sensemaker-implementation-probe-report.yaml --repo-root .`

The post-change probe still measures `vg=0.67`, fixture coverage `0.74`, one
version finding, and three ADR findings. Those are current evidence, not
failures of the wrapper fix.

The dedicated wrapper harness also passes all seven scenarios via
`py -3.10 tests/run_validate_and_report_tests.py`.

The complete repository suite was also attempted with `py -3.10 -m pytest
tests -q`, but collection could not complete in this environment. The package
declares Python `>=3.11`, only Python 3.10/3.9 are installed, and the test
environment lacks several optional/import-time dependencies. This is an
environment limitation, not a regression attributable to the focused patch.

## 13. next_handoff

Hand off to `workflow-planner` for a follow-up plan after owner review of the
three unresolved authority groups: package version, validator fixtures, and
ADR status. The primary implementation is complete and should not be reopened
unless the wrapper regression or post-change validation fails.

```yaml
artifact_id: docs_contract_reconciliation_report
source_intent_ref: 00-user-intent.md
status: implemented_with_owner_decisions_pending
primary_workflow: docs-contract-reconciliation
post_change_probe: artifacts/repo-sensemaker-implementation-probe-report.yaml
```
