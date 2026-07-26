# Phase Closure: Issue #80 / PR #81 (Weakness-Type & Evidence-Quote Contract)

**Date**: 2026-07-26
**Nature of this document**: verification + decision-readiness record only.
No code, validator, prompt, contract, or ADR status was changed to produce
this document. No auteur rerun. No external experiment. No D7/D8 ratification.

## 1. What was verified

Issue #80 (bounded contract-redesign plan, per ADR 0014-revised/0015/0016
addenda and D1-D6, D9, D10) is implemented by PR #81 (merged to `main` at
`9a7d7d5`, branch `fix/brief-weakness-evidence-contract`). All acceptance
criteria enumerated in issue #80 were checked against the merged code
(`scripts/validate-brief.py`, `scripts/brief_skeleton.py`,
`scripts/skill_executor.py`, `skills/repo-sensemaker/SKILL.md`,
`skills/repo-sensemaker/references/repo-analysis-template.md`,
`skills/workflow-planner/references/artifact-contracts.yaml`, and
`tests/test_weakness_type_and_quote_contract.py`) and found **Satisfied**:

- Structured `weakness_type` / `weakness_type_explanation` fields in the
  brief's Section 13 YAML, declared in `artifact-contracts.yaml`.
- Single taxonomy authority (`weakness-types.md`, 7 terms + `Other`), loaded
  identically by the validator and the skill-prompt injector — no duplicated
  hardcoded lists.
- `WEAKNESS_TYPE_MISSING` / `WEAKNESS_TYPE_UNKNOWN` / `WEAKNESS_TYPE_OTHER_NO_EXPLANATION`
  are non-blocking warnings; `WEAKNESS_TYPE_MALFORMED` (wrong YAML type) is a
  blocking error. `UNKNOWN_WEAKNESS_TYPE` (the PR #78 failure mode) is fully
  retired from any blocking code path.
- New deterministic evidence-quote-grounding check
  (`EVIDENCE_QUOTE_NOT_FOUND` / `EVIDENCE_QUOTE_WINDOW_MATCH`): a cited quote
  must exist verbatim (after narrow whitespace normalization) within a small
  fixed window around its cited `file`/`lines`; the validator reports the
  exact matched line, whether the match was exact-range or window-only, and
  flags ambiguity when more than one candidate line matches.
- `HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT` warning fires for `Safety Gaps` /
  `Ghost Features` types, operationalizing ADR 0016's D5 threshold.
- Legacy briefs without `weakness_type` validate with a warning, not a
  failure.
- No auteur rerun, no routing/Wayfinder/Step 2 change, no ADR status change
  occurred as part of PR #81. The `artifact-contracts.yaml` diff is limited
  to the three new field/notes lines.
- Targeted tests (`tests/test_weakness_type_and_quote_contract.py` and four
  related suites): passing at `9a7d7d5`. `scripts/validate-repo.py`: passes.
  Full suite comparison against baseline `main@8b73408` shows the same 23
  pre-existing failures/3 collection errors on both revisions (like-for-like
  regression check, per CLAUDE.md's verification-discipline rule) — none of
  the 23 touch weakness-type or evidence-quote logic.

## 2. Residual implementation debt (non-blocking, documented)

| Debt | Severity | Blocks phase closure? | Blocks external experiment? | Disposition |
|---|---|---|---|---|
| Duplicate `weakness_type:` key in the §13 YAML fence is not detected; PyYAML's `safe_load` silently keeps the last value with no warning or error, contrary to issue #80's assumption that this would be a parser-level failure | Low | No | No | Future implementation work (not raised in original review or PR) |
| `WEAKNESS_TYPE_OTHER_NO_EXPLANATION`'s "blocks human final approval" claim is enforced only in the warning message text and doc/template prose — no code gate exists that reads this warning and prevents a downstream action | Informational | No | No | Intentional human-process boundary, consistent with D6 (human reviews every final brief) — not a code defect |
| Stray duplicate fixture `tests/fixtures/validate-brief/invalid/unknown-weakness-type.md` left alongside its replacement `tests/fixtures/validate-brief/valid/unrecognized-weakness-type-warning.md` | Informational | No | No | Cosmetic; pre-existing debt, harmless |
| 23 pre-existing failing tests / 3 collection errors (integration/executor-plumbing, path-drift, generate-plan-conformance, one unrelated field-contract-agreement case) | Medium | No (confirmed present identically on baseline `main@8b73408`) | Possibly, for unrelated workflows | Pre-existing debt, out of this phase's scope; not introduced by PR #81 |

None of the above is a defect introduced by PR #81 beyond the duplicate-key
gap, which is a genuine but low-severity, non-blocking gap relative to issue
#80's own stated assumption.

## 3. Conclusion

**B — Phase complete, with documented non-blocking debt.** All issue #80
acceptance criteria are satisfied by the merged PR #81; the one genuine gap
found (duplicate-YAML-key handling) is low severity, untested, and does not
block phase closure or any external experiment. No corrective PR is required
before proceeding to the next readiness question.

## 4. Readiness status (unchanged by this phase)

Per `docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md` Part 5 and
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`: the highest currently justified
readiness level remains **"Externally exercised"** (Level C). PR #81 fixes
an internal contract defect surfaced by the auteur campaign; it does not
itself constitute new external evidence, so it does not advance the
readiness level. Reaching "Externally validated" (Level D) still requires a
clean external Stage A + Step 2 pass, which has not occurred.

## 5. Open owner decisions

Per commit `1ad42ca` ("apply explicit owner ratification of D1-D6, D9, D10"):
D1-D6, D9, D10 are ratified. **D7 (next readiness target) and D8
(external-validation bar) remain explicitly UNDECIDED by owner instruction**,
recorded in `docs/OWNER-DECISION-PACKAGE-2026-07-26.md` Part 2/Part 4. This
document does not resolve, default, or recommend ratifying either. ADR 0021
(production readiness) stays PROPOSED pending D7/D8 and its other named
owner-decision items.

## 6. No further action taken

This document is a closure record only. It authorizes no experiment, no
auteur rerun, no D7/D8 ratification, no ADR promotion, and no further
implementation.
