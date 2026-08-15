# Prompt Handoff

## 1. Target Skill

`workflow-planner`

## 2. Context to Preserve

The dogfood implementation completed the primary `docs-contract-reconciliation`
fix. `scripts/validate-and-report.py` now launches child validators with
`sys.executable`, and the behavior is covered by a Windows-compatible
regression test. Directly related test harnesses use the same interpreter
handoff. Python runtime dependencies are synchronized between `setup.py` and
`pyproject.toml`, and the README wording now distinguishes external services
from local package dependencies.

The relationship probe's version-conflict finding now requires semantic review,
matching the repo-sensemaker contract that mechanical disagreements do not
establish authority or historical status.

Focused validation passed: 53 tests. The post-change probe and probe validator
also passed. Current post-change evidence still reports `vg=0.67`, fixture
coverage `0.74`, one version finding, and three ADR findings.

## 3. Task

Create a bounded follow-up plan for the unresolved authority decisions:

1. Decide whether `package.json` `4.1.0` is tooling metadata, stale product
   metadata, or a separate package identity relative to Python `0.2.2`.
2. Decide whether the five missing validator fixtures are required or
   intentionally waived, then implement only the approved outcome.
3. Have the owner review the ADR status findings for 0018, 0019, and 0020.

## 4. Constraints

- Preserve the implemented wrapper fix and its regression coverage.
- Treat the post-change probe as current evidence; do not rewrite the original
  immutable dogfood brief.
- Do not choose version authority, fixture policy, or ADR status silently.
- Do not mass-edit historical `python3` examples without confirming they are
  live supported instructions.
- Keep the follow-up bounded to the authority and validation gaps above.

## 5. Inputs

- `artifacts/docs_contract_reconciliation_report_dogfood.md`
- `artifacts/repo-sensemaker-implementation-probe-report.yaml`
- `artifacts/repository_sensemaking_brief_dogfood.md` (historical pre-change
  evidence)
- `package.json`
- `pyproject.toml`
- `setup.py`
- `tests/fixtures/`
- `docs/adr/`

## 6. Expected Output

A validated workflow plan that separates owner decisions from mechanical work,
names the authority matrix explicitly, and defines approval gates before any
metadata, fixture, or ADR mutation.

## 7. Stop Condition

Stop for owner review whenever the repository evidence cannot establish the
authority of a version, the required status of a fixture, or the correct ADR
status. Do not expand into a broad architecture workflow automatically.

---

## 8. Ready-to-copy Prompt

```markdown
/workflow-planner

Create a bounded follow-up plan from
artifacts/docs_contract_reconciliation_report_dogfood.md and
artifacts/repo-sensemaker-implementation-probe-report.yaml. Preserve the
implemented sys.executable wrapper fix. Plan owner-gated decisions for the
package.json 4.1.0 versus Python 0.2.2 version authority, the five missing
validator fixtures, and ADR status findings 0018, 0019, and 0020. Do not infer
authority or mutate metadata, fixtures, or ADRs without approval.
```

## 9. Machine-readable handoff

```yaml
artifact_id: session_summary
source_intent_ref: 00-user-intent.md
target_skill: workflow-planner
status: ready
```
