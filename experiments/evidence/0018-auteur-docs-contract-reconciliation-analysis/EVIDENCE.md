# Evidence 0018 — Auteur docs-contract-reconciliation cycle analysis (meta-dogfood)

## Purpose

Meta-analysis of the second full auteur dogfood cycle (2026-08-13, PR #72 merged
at auteur `8b8b7fd`), cross-checked against the framework-side records
(evidence 0016 postmortem, evidence 0017 dogfood record, integration-report,
adoption-finalization). Produces six recommendations for sensemaking-skills,
filed as GitHub issues #170-#175.

## The cycle (verified reconstruction)

Two auteur dogfood cycles:

- **Cycle A (2026-08-11)**: first brief + remediation on `fix/adr-id-collision`
  (`271b9be`, never merged). The postmortem (evidence 0016) judged the
  remediation's ADR-013 dedup direction wrong (9 load-bearing references
  rewritten) and its "9 structure layers" vocabulary flag a false positive.
  Rules 6-8 were added to the canonical `evidence-rules.md` as a result.
- **Cycle B (2026-08-13)**: the analyzed run. Brief
  (`docs/reviews/2026-08-13-auteur-repo-sensemaking-brief.md`) -> plan
  (`docs/design/2026-08-docs-contract-reconciliation.md`, `plan_only`) ->
  5 commits -> review -> PR #72 merged at auteur `8b8b7fd` -> root cleanup
  (9,576 root JSONs + 35 log/xml files removed; root `*.json` = 0).

## What was verified

### The run's own claims hold

All four brief findings were real, and the fixes are present at `8b8b7fd`:
duplicate ADR resolved (one file per number), `validate-repo.py` rules #10
(duplicate-ADR) and #11 (root-`*.json`) added, `src/auteur/pipeline/runner.py`
`report_dir=Path()` -> `<project>/.auteur/reasoning` (+ regression tests and
`docs/engineering/reasoning-report-contract.md`), root `HANDOFF.md` archived to
`docs/handoffs/2026-08-13-root-handoff-superseded.md` with a supersession
banner, and the fixture gate aligned to the valid-only convention (Option B).

### The direction of the merged ADR fix contradicts canonical Rule 7

The merged state keeps `013` on `013-series-graph-semantics.md` (zero external
references) and renumbers `013-universe-to-series-propagation.md` -> `018`,
rewriting 9 references (CONTEXT.md x3, docs/artifacts.md x3,
`src/auteur/series/universe_integration.py` x3). The plan documented the choice
(next-free-number rationale, "files run 001-017") but did not address the
reference-weight evidence or prior dedup intent that Rule 7 says to check.
Evidence 0016's postmortem judged exactly this direction the failure (the
load-bearing identity was "013 = Universe-to-Series", 9 refs; the orphan was
series-graph).

### The framework's learnings never reached the executor

- auteur's vendored `skills/repo-sensemaker/references/evidence-rules.md`
  contains only rules 1-5 (no Rules 6-8).
- The 0017 probe report (`docs/reviews/2026-08-13-auteur-repo-sensemaking-probe-report.yaml`)
  carries `test_file_count: 741` but no `test_case_count` (the Rule 8
  enhancement).

The executing repo used a stale vendored snapshot, so cycle B re-derived the
exact decision the framework had already characterized as a failure.

### Probe catalogs but does not flag

The 0017 probe records both `id: '013'` entries in
`relationships.adr.catalog` but emits `findings: []`. The brief caught the
duplicate by semantic review of the catalog - the model did the probe's job.

### Residual ambiguity was left twice, with contradictory readings

`docs/handoffs/2026-05-21-implementation-workflow-domain-alignment.md:17`
("4. ADR-013") was left unresolved. Evidence 0016 read it as pointing at a
now-deleted third ADR; the cycle-B handoff rationalized it as a different
numbering scheme. Neither reconciled with the other. The merged validator (#10)
only scans `docs/adr/` filenames, so it can never flag this.

### Probe metrics encode assumptions that conflict with target conventions

- `context_entropy.ce` returned a false `0.0` on auteur because the
  `git status --ignored` subprocess hit the 30s cap enumerating ~10k ignored
  root JSONs (evidence 0017 finding 1; the brief itself echoed this).
- `fixtures_coverage` reported 0.73 "missing fixtures" for 4 validators whose
  `invalid/` fixtures auteur deliberately retired (commit `9994238`,
  unsatisfiable for repo-wide validators). The plan resolved this as Option B
  (valid-only documented convention) and its Option C assigns the probe-side
  follow-up explicitly to sensemaking-skills.

### The framework does not eat its own dogfood

sensemaking-skills itself carries the same drift classes it fixed in auteur:
root derived artifacts (`PHASE-3-*.json`, `workflow_run.log`,
`PHASE-3-SHADOW-MODE-RUN.log`), root `HANDOFF.md` claiming an "11-section
Brief" vs the current 14, `docs/adr/README.md:3-4` claiming "no script
validates the **Status** line" (false since the ADR probe), and `package.json`
4.1.0 vs `pyproject.toml` 0.2.2 with no cross-checking validator. The probe
already found these (integration-report sections 7/10) and stopped at
"discovery finding != repair authorization".

## Recommendations (filed as GitHub issues)

| Issue | Recommendation |
|---|---|
| #170 | Close the learning-loop propagation gap: vendored-skill drift probe finding + `prior_evidence` input to the `docs-contract-reconciliation` workflow |
| #171 | Make Rule 7 enforceable: collision-direction evidence as a required brief field, rejected by `validate-brief.py` when absent |
| #172 | ADR probe emits duplicate-id as a top-level finding (+ fixture asserting catalog-duplicate => finding) |
| #173 | Probe metric confidence/failure-mode contract: `ce` timeout returns None not 0.0; `fixtures_coverage` honors documented valid-only conventions |
| #174 | Self-dogfood: run `docs-contract-reconciliation` on sensemaking-skills itself; formalize "discovery finding -> repair authorization" |
| #175 | Promote evidence 0017's four dogfood findings to Rules 9+ in `evidence-rules.md` |

## Evidence pointers

- auteur @ `8b8b7fd`: `docs/reviews/2026-08-13-*`, `docs/design/2026-08-docs-contract-reconciliation.md`,
  `docs/adr/013-series-graph-semantics.md`, `docs/adr/018-universe-to-series-propagation.md`,
  `scripts/validate-repo.py`, `src/auteur/pipeline/runner.py`
- sensemaking-skills: `experiments/evidence/0016-auteur-remediation-postmortem.md`,
  `experiments/evidence/0017-auteur-repo-sensemaking-brief/`,
  `integration-report.md`, `adoption-finalization.md`,
  `skills/repo-sensemaker/references/evidence-rules.md`,
  `skills/workflow-planner/references/workflow-registry.yaml`

## Notes

- This record is a read-only cross-check; no raw run artifacts were produced.
- Verification heads: auteur `8b8b7fd`; sensemaking-skills HEAD `433a377` with
  the Rules 6-8 / `test_case_count` capture present as uncommitted working-tree
  changes at analysis time.
- Not adjudicated: the true referent of `docs/handoffs/2026-05-21-...:17`
  "ADR-013" (two contradictory readings on record; no git archaeology done).
