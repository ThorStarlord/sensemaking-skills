# Evidence 0019 — Sensemaking-skills self-dogfood docs-contract-reconciliation

## Purpose

Self-dogfood run of the `docs-contract-reconciliation` workflow on
sensemaking-skills itself (issue #174). Also formalizes the repo's
"discovery finding -> repair authorization" doctrine: probe findings are
discoveries; repairs require authorization; this record documents the
authorization, the executed repairs, and the deliberately deferred items.

## Repair authorization

- Envelope: the standing delegated-authority instruction for this task
  ("implement all of the issues, proceed without my input, do not wait for
  approval"), applied to the four drift classes below.
- Doctrine: `integration-report.md` section 10 stopped at "discovery finding
  != repair authorization". This record is the first explicit
  authorization-of-record for repairs derived from the framework's own probe.

## Findings (probe @ main 3b93b6d; see probe-report.yaml in this folder)

| Finding | Evidence |
|---|---|
| Product version conflict | `package.json` declared 4.1.0 vs `pyproject.toml` 0.2.2 (version probe: conflicting_values; distinct values included 4.1.0) |
| Fixture-coverage misreport | probe reported 14/19 (0.74) with 5 `missing_fixtures` (validate-mode-coverage, validate-output, validate-repo, validate-run-log, validate-skill-hygiene) that the repo's own harness documents as excluded in `tests/fixtures/REGRESSIONS.yaml` (each with a reason) |
| Root derived-artifact sprawl | `PHASE-3-*.json` x2 (tracked, produced by root `test_phase3_*.py` writing to repo root) + 3 gitignored root logs (PHASE-3-SHADOW-MODE-RUN.log, workflow_run.log, workflow_step1_run.log) |
| Stale root handoff | `HANDOFF.md` claims an "11-section Brief" vs the current 14-section `repository_sensemaking_brief`; V1-refactor framing |
| Stale docs claim | `docs/adr/README.md` says "No script validates the **Status** line today" — false since the ADR probe |

## Repairs executed

1. **Version**: `package.json` aligned 4.1.0 -> 0.2.2 (0.2.x is the product
   family per README/CHANGELOG/pyproject; no evidence of a published npm
   artifact at 4.1.0). Added `validate-repo.py` rule #10: product version
   declarations (pyproject, package.json, src/<pkg>/__init__.py) must agree.
2. **Fixture metric**: `fixtures_coverage` now honors
   `tests/fixtures/REGRESSIONS.yaml` `excluded_validators` (reported as
   `excluded_by_convention`, counted as covered, never "missing"). Probe now
   reads 14/19 (1.0) missing=[] on this repo.
3. **Root sprawl**: `PHASE-3-*.json` moved (git mv) to
   `docs/archive/root-artifacts/`; the three gitignored root logs deleted
   (targeted, auteur precedent); producers fixed so the sprawl cannot recur:
   `test_phase3_poc.py` / `test_phase3_comprehensive.py` now write results
   to `docs/archive/root-artifacts/`.
4. **Handoff**: root `HANDOFF.md` archived to
   `docs/archive/handoffs/2026-08-13-root-handoff-superseded.md` with a
   supersession banner.
5. **Docs claim**: `docs/adr/README.md` corrected to state that the ADR probe
   validates the `**Status**` line.
6. **CONTEXT.md**: Probe Engine section documents the metric failure modes
   (ce timeout -> None, fixtures conventions, duplicate_id finding).

## Deliberately deferred (require owner/product decision)

- **Vg = 0.67**: README declares `shadow-mode-runner.py`, `validate-brief.py`,
  `validate-plan.py`, `validate-and-report.py` as verification entrypoints that
  CI does not run; CI enforces `validate-repo.py`, `test-validators.py`, etc.
  Aligning the README verification section with CI (or vice versa) is a
  product decision about which checks are canonical, not a mechanical repair.
- **ADR findings (4)**: status_claim_mismatch on docs/adr/0018/0019/0020
  references that predate ADR 0014's ratification (dated stale references per
  integration-report.md section 7) — interpretation is the model/owner's job.
- **Version probe still reports 1 finding**: `integration-report.md` /
  `integration-run-*.yaml` contain 0.2.0/0.2.1 doc claims vs declared 0.2.2 —
  historical narratives of prior releases, classified "current"; needs an
  owner decision on how historical release claims should be marked.
- **Pre-existing test breakage**: `tests/test_validate_brief_json.py` imports
  a nonexistent `scripts/validate_brief.py` (collection error);
  `tests/test_generate_plan_conformance.py` 2 failures (generated plans miss
  primary_fog_type/workflow_steps/created_at — plan-generator issue). Both
  verified pre-existing on baseline; not caused by this work.

## Evidence pointers

- Probe report: `probe-report.yaml` in this folder.
- Repairs: commit(s) in this task; `scripts/validate-repo.py` rule #10;
  `scripts/repo_probes.py` fixtures_coverage; `CONTEXT.md` Probe Engine;
  `docs/archive/root-artifacts/`; `docs/archive/handoffs/2026-08-13-root-handoff-superseded.md`.
- Related: evidence 0016/0017/0018, issues #170-#175.

## Notes

- Verification heads: probe ran on main @ 3b93b6d before the repair commit;
  the repairs themselves are in the task's commits.
- Root `package.json` remains the only root-level `.json` (legitimate).
