# Adoption finalization: merge-ready state (Probe Engine relationship integration)

- **Date**: 2026-08-12
- **Branch**: `feat/probe-engine-relationship-integration` (two commits on
  top of `main` @ `90780f5`: the integration at `34d50dd` plus this
  doc-only finalization record; branch HEAD is assigned at merge)
- **Owner decision**: ADOPTION APPROVED for automatic doc-surface discovery,
  version relationship detection, and ADR integrity detection as canonical
  Probe Engine capabilities. Network detector NOT adopted. No semantic
  graph abstraction.
- **Status**: merge-ready. **NOT MERGED — awaiting separate authorization.**

## Canonicalization pass (this task)

| Step | Result |
|---|---|
| Rebase onto current main | **Not needed** — main unchanged (`90780f5`); the branch is two clean commits directly on main's HEAD. |
| ADR governance check | `docs/adr/README.md` defines only the status lifecycle; **no governance rule requires an ADR for a probe-report schema extension** → no ADR filed. |
| Focused Probe Engine tests | **58 passed** (test_repo_probes, test_probe_report_cli, test_probe_prompt_injection, test_skill_distribution_probe, test_probe_relationships). |
| Validator harness | **73/73 passed, 0 coverage failures** (incl. updated valid exemplar + new `relationships_malformed` negative). |
| sensemaking-skills equivalence | Fresh run: version findings=1, adr findings=3. Programmatic comparison vs the spike's final artifact: version declarations/claims/distinct **identical** and observation (source,value,kind) set **identical**; ADR files/references/finding types **identical**; surface 839/141 **identical**; network absent by design. |
| auteur equivalence | Fresh run: version findings=0, adr findings=0 (correct negative); surface 511/143, declarations 2+2, claims 114, adr files=18 refs=15 — matches the spike exactly. |
| Consumption smoke test | Passed: one isolated repo-sensemaker Diagnose accepted all 4 findings with per-file verification, diagnosed Contract Mismatch, confirmed the durable Brief as the downstream boundary, and confirmed no finding over-presents as a diagnosis. |
| Backward compatibility | Producer always emits `relationships`; validator treats it as optional-when-present — old reports without the section remain valid (verified by fixtures). Asymmetry documented in integration-report.md §4 as intentional compatibility. |

## Files in the merge (13 vs main, +1857/-1)

The 12 integration files below plus this adoption-finalization record
(the branch's second, doc-only commit):

- `scripts/probe_relationships.py` (new, canonical: doc-surface discovery +
  version + ADR probes, pure functions)
- `scripts/repo_probes.py` (`probe_all` gains the `relationships` key;
  try/except ImportError sibling import)
- `scripts/probe-repo.py` (one summary line)
- `scripts/validate-probe-report.py` (`PROBE_REPORT_RELATIONSHIPS_SHAPE`
  optional shape check)
- `skills/repo-sensemaker/SKILL.md` (Probe Engine step 5: relationship
  findings are evidence candidates, never diagnoses)
- `tests/test_probe_relationships.py` (new, 14 tests)
- `tests/fixtures/validate-probe-report/valid/sample.md` (extended)
- `tests/fixtures/validate-probe-report/invalid/relationships_malformed.md` (new)
- `integration-design.md`, `integration-report.md`, `integration-run-sensemaking-skills.yaml`,
  `integration-run-auteur.yaml` (experiment records)

## Accepted / not accepted (owner decision, honored)

**Accepted:** doc-surface discovery, version detection, ADR integrity,
additive `relationships` output, repo-sensemaker guidance.
**Not accepted:** network detector, new relation types, graph/node/edge
infrastructure, new Skills, new brief fields, routing changes.

## Explicitly deferred (per owner instruction)

- **No drift repairs**, including the now-stale `docs/adr/README.md:3-4`
  statement ("No script validates the `**Status**` line today" — the ADR
  probe now does). It is recorded as evidence that the feature works, and
  will be handled separately as a tiny documentation-drift repair.
- The no-anchor docs-vs-docs version case remains a documented confidence
  limitation (`integration-report.md` §8), not a redesign: no observed
  failure after the portability work.
- **No ADR filed**: no normative architecture decision emerged (the
  contract extension is additive within the schema's existing tolerance).

## Next steps (outside this task, require separate authorization)

1. Merge `feat/probe-engine-relationship-integration` into main.
2. Publish (changelog/status), close the feature cycle.
3. Return to real Sensemaking use; the next new relation type must earn
   itself from real usage, as this one did.
