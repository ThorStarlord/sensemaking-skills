# Merge-ready report — extended_analysis canonicalization (2026-08-10)

**Branch**: `candidate/sensemaking-vnext` — rebased onto current `main`
(zero conflicts), HEAD `c6827e6`.
**State**: merge-READY by verification; **NOT merged** — merge awaits a
separate explicit owner decision, per instruction.

## Owner decisions recorded this session (2026-08-10)

1. **Accept** the `candidate/sensemaking-vnext` architecture as the working
   default design (Section 15 `extended_analysis` with the four surviving
   fields, one-Skill packaging, Diagnose/Interact separation).
2. **Classify normally, drop the 'candidate' label**: the four surviving
   fields enter `artifact-contracts.yaml` as ordinary optional,
   model-constrained fields (`recommended_machine_fields`); no permanent
   `candidate_machine_fields` tier.
3. **Formalize without merging**: file the numbered ADR, canonicalize,
   rebase onto current main, verify, produce this report — then stop.

## What changed (commit `c6827e6`, 10 files, +318/-327)

- **`docs/adr/0024-extended-analysis-field-classification.md`** (new,
  moved from the draft): ACCEPTED. Records the stress-test evidence
  (6 cases + 3 reruns), the deliberate removal of `discovery_confidence`
  (Case 4: nothing read it), the `uncertainty.source`
  `repository_evidence`/`empirical` decision-rule clarification (Cases
  1/3), the Boundary Rule 6 reading-scope revision (Case 5), and the
  accepted verdict semantics (architectural review judges the proposal's
  scope against the brief's named boundary; it is not a repository
  prioritization engine).
- **`artifact-contracts.yaml`**: the four `extended_analysis.*` fields
  moved from `candidate_machine_fields` into `recommended_machine_fields`;
  the `candidate_machine_fields` key is removed. Notes entry rewritten.
- **`brief_skeleton.py`**: canonical heading `## 15. Extended analysis`
  (no "(candidate)"), Section 15 comment now cites ADR 0024.
- **`validate-brief.py`**: heading regex accepts the canonical heading and
  still tolerates the pre-ratification "(candidate)" spelling (backward
  compat for already-written artifacts); comments updated.
- **`repo-analysis-template.md`**: canonical heading, `schema_version: 1`
  (was `candidate-1`), ratified wording.
- **`repo-sensemaker/SKILL.md`**: candidate/unratified lifecycle wording
  removed; Section 15 presented as ratified per ADR 0024.
- **Tests**: all fixtures moved to canonical heading/schema; new
  `test_legacy_candidate_heading_spelling_still_tolerated` proves the
  validator's backward-compat guarantee.

## Verification

### Focused (22/22 passed)
`test_brief_skeleton_extended_analysis.py`,
`test_validate_brief_extended_analysis.py`,
`test_extended_analysis_end_to_end.py`, `test_field_contract_agreement.py`
— including the previously-red `fog_type` contract-agreement test, fixed
by main's `029dde0`/`8f454c4` (brought in by the rebase).

### Baseline-relative (like-for-like)
Coupled set (every test file touching the changed modules, same command,
isolated `--basetemp`):

| Side | Result |
|---|---|
| `main` (baseline) | 126 passed, 5 xfailed, 10 subtests — 0 failures |
| `candidate` (rebased) | 145 passed, 5 xfailed, 10 subtests — 0 failures |

Identical xfail profile; candidate adds the 19 extended-analysis tests.
`test_validate_brief_json.py` fails collection identically on both sides
(pre-existing `validate_brief.py` vs `validate-brief.py` import issue,
unrelated to this change).

### Real-runtime (17/17 checks passed)
Replicated the production sequence from
`docs/candidate/real-runtime-run-2026-08-09/00-context.md`:
`build_skeleton()` → genuine analysis of this repository (real citations:
`docs/adr/0024...:3`, `artifact-contracts.yaml:152`, `brief_skeleton.py:268`)
→ real `reconcile()` (including deterministic quote re-derivation) → both
real validators in the chain declared by `artifact-contracts.yaml`.

- Fresh artifact: generic validator 0 errors; specialized validator 0
  blocking; 0 `EXTENDED_ANALYSIS` warnings. Canonical heading,
  `schema_version: 1`, no `discovery_confidence` anywhere.
- **Backward compat on a real pre-canonicalization artifact** (the
  2026-08-09 record brief, which uses the legacy heading, `candidate-1`
  schema, and still contains `discovery_confidence` data): 0 errors, 0
  blocking, 0 `EXTENDED_ANALYSIS` warnings — legacy artifacts revalidate
  unchanged, exactly as ADR 0024 §4 promises.

## Merge-ready diff (branch vs main)

```
 docs/adr/0024-extended-analysis-field-classification.md  | 234 ++++++
 docs/candidate/... (stress-test + real-runtime records)   | ~1100 (records)
 scripts/brief_skeleton.py                                 |  41 +
 scripts/validate-brief.py                                 |  99 ++
 skills/architectural-review/SKILL.md                      |   7 +
 skills/repo-sensemaker/SKILL.md                           | ~150 ++
 skills/repo-sensemaker/references/repo-analysis-template.md | 78 +
 skills/workflow-planner/references/artifact-contracts.yaml |  16 +
 tests/test_brief_skeleton_extended_analysis.py            | 136 +
 tests/test_extended_analysis_end_to_end.py                | 175 +
 tests/test_repo_sensemaker_evidence_contract.py           |  19
 tests/test_validate_brief_extended_analysis.py            | 220 +
```

## Explicitly NOT done (per scope)

- **No merge** to `main` — requires a separate explicit decision.
- No new Skill, no new validator, no new governance mechanism, no
  packaging change (stress round 2 constraints still honored).
- `docs/candidate/` historical records left untouched (frozen evidence).
