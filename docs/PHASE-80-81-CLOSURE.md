> **HISTORICAL (pre-ADR-0013, 2026-08)**: runner-led orchestration record,
> preserved as historical evidence. The ratified execution model is agent-native
> (ADR 0013); the programmatic second-model runner was retired.

# Phase Closure: Issue #80 / PR #81 (Weakness-Type & Evidence-Quote Contract)

**Date**: 2026-07-26
**Nature of this document**: verification + decision-readiness record only.
No code, validator, prompt, contract, or ADR status was changed to produce
this document. No auteur rerun. No external experiment. No D7/D8 ratification.

## 1. What was verified

Issue #80 (bounded contract-redesign plan, per ADR 0014-revised/0015/0016
addenda and D1-D6, D9, D10) is implemented by PR #81 (merged to `main` at
`9a7d7d5`, branch `fix/brief-weakness-evidence-contract`). All acceptance
criteria enumerated in issue #80's "Acceptance criteria" checklist were
checked against the merged code (`scripts/validate-brief.py`,
`scripts/brief_skeleton.py`, `scripts/skill_executor.py`,
`skills/repo-sensemaker/SKILL.md`,
`skills/repo-sensemaker/references/repo-analysis-template.md`,
`skills/workflow-planner/references/artifact-contracts.yaml`, and
`tests/test_weakness_type_and_quote_contract.py`). Duplicate-`weakness_type`-key
rejection is **not** one of those checklist items (see the classification in
§1a), so it is scored separately and does not change the checklist table
below.

### Acceptance-criteria table (issue #80 checklist, verbatim order)

| Criterion | Status | Evidence | Residual gap |
|---|---|---|---|
| Structured `weakness_type` field in §13 YAML, declared in `artifact-contracts.yaml` | Satisfied | `artifact-contracts.yaml` machine_fields list (lines ~143-144) adds `weakness_type` / `weakness_type_explanation`; parsed at `validate-brief.py` ~L481-548 | None |
| Registered enum values validated deterministically against `weakness-types.md` | Satisfied | `_validator_utils.load_weakness_types()` regex-parses the 7 bolded terms; used at `validate-brief.py:340,501` | None |
| `Other` requires explanation; absence is non-blocking `WEAKNESS_TYPE_OTHER_NO_EXPLANATION` | Satisfied | `validate-brief.py` ~L501-507 | None |
| Taxonomy never invalidates the whole brief solely on prose lacking an exact term | Satisfied | `WEAKNESS_TYPE_PROSE_MISMATCH` is warning-severity only, `validate-brief.py:548` | None |
| Old `UNKNOWN_WEAKNESS_TYPE` blocking prose-substring check removed | Satisfied | Symbol absent from `validate-brief.py`; `--list-codes` output no longer lists it | None |
| Non-blocking warning behavior tested for every severity-matrix condition | Satisfied | `tests/test_weakness_type_and_quote_contract.py` covers missing/unknown/other-no-explanation/prose-mismatch/malformed cases | None |
| Quote-existence check: deterministic, blocking on failure, tested (incl. missing file / out-of-bounds range) | Satisfied | `EVIDENCE_QUOTE_NOT_FOUND` at `validate-brief.py:610-628`, error-severity (default) | None |
| Historical PR #67/#70/#73/#78 evidence artifacts byte-unchanged | Satisfied | Not touched by the PR #81 diff | None |
| Named regression suites pass (`run_validate_brief_tests.py`, `test_validate_brief_json.py`, `test_validate_brief_target_repo.py`, `test_brief_skeleton.py`, `test_evidence_discipline.py`, `test_evidence_excerpt_fields_and_logic_trace.py`) | Satisfied | Ran at `9a7d7d5`, all pass | None |
| `python scripts/validate-repo.py` passes | Satisfied | Ran at `9a7d7d5`, passes | None |
| No auteur rerun performed | Satisfied | No campaign artifacts touched or generated | None |
| No Step 2 / routing / workflow-planner behavior change | Satisfied | Diff confined to brief-artifact files listed above | None |
| No production-readiness claim made in the PR description | Satisfied | PR #81 description makes no such claim | None |
| Duplicate `weakness_type` YAML key → blocking error (issue #80 "Validation severity matrix" row, *not* a checklist item — see §1a) | **Not satisfied** | No duplicate-key detection exists anywhere in `validate-brief.py` or `_validator_utils.py` (grep confirms); PyYAML `safe_load` silently keeps the last value | Duplicate `weakness_type:` keys are silently resolved, not rejected |

### 1a. Classification of the duplicate-key gap

Issue #80 is unambiguous on this point. The checklist under "Acceptance
criteria" (the actual gating list) does **not** mention duplicate keys at
all. The relevant text appears only in the design narrative, in the
"Validation severity matrix" table:

> `Duplicate weakness_type key in YAML block | error | no | existing
> YAML-parse error path (duplicate keys are a YAML-parser-level failure, not
> new logic)`

This is **(B) a proposed severity-matrix expectation, not an acceptance
criterion** — it never appears in the "Acceptance criteria" checklist that
PR #81 was scoped against. It is simultaneously **(C) an incorrect
implementation assumption**: the issue's own parenthetical asserts duplicate
keys are "a YAML-parser-level failure," but PyYAML's `safe_load` (used
throughout this codebase) does not raise on duplicate mapping keys — it
silently keeps the last one. No code anywhere in the merged implementation
adds an explicit duplicate-key check to compensate for that incorrect
assumption, so the severity-matrix row was never actually implemented and,
because it was never a checklist item, its absence does not fail any
acceptance criterion.

Because the duplicate-key row was design narrative resting on a false
premise about YAML parsing rather than a ratified acceptance criterion, this
document does **not** say "all acceptance criteria are satisfied" and
"a stated expected behavior is absent" in the same breath. The correct,
non-contradictory statement is: **all of issue #80's checklist acceptance
criteria are satisfied; a separate, non-checklist severity-matrix expectation
in the same issue rests on an incorrect assumption and was not implemented.**

### 1b. Other verified behavior

- Single taxonomy authority for the **7 registered types**: `weakness-types.md`
  is parsed by `_validator_utils.load_weakness_types()`, which both
  `validate-brief.py` (line 340) and `skill_executor.py`'s
  `get_allowed_weakness_types()` (line 93) call — the 7 terms cannot drift
  between validator and prompt injection. **`Other` is not declared in
  `weakness-types.md`** (grep confirms no `Other` entry in that file); it is
  instead appended as a literal string independently in two places —
  `validate-brief.py:501` (`set(weakness_types) | {"Other"}`) and
  `skill_executor.py:143` (`"  - Other\n\n"` in the injected prompt text).
  There is no shared helper that produces the final allowed-value set
  (types + `Other`) — each component unions/appends `"Other"` on its own.
  This is low-risk (both are trivial, easily-greppable literals) but it is
  parallel logic, not single-sourced, so the two literals could in principle
  diverge (e.g. casing) without a test catching it structurally. The
  narrowest true statement: *the seven registered types remain sourced from
  `weakness-types.md` via one shared loader; `Other` is added independently
  by each consuming component, not from that file.*
- `WEAKNESS_TYPE_MISSING` / `WEAKNESS_TYPE_UNKNOWN` / `WEAKNESS_TYPE_OTHER_NO_EXPLANATION`
  are non-blocking warnings; `WEAKNESS_TYPE_MALFORMED` (wrong YAML type) is a
  blocking error. `UNKNOWN_WEAKNESS_TYPE` (the PR #78 failure mode) is fully
  retired from any blocking code path.
- New deterministic evidence-quote-grounding check
  (`EVIDENCE_QUOTE_NOT_FOUND` / `EVIDENCE_QUOTE_WINDOW_MATCH`), verified
  directly against `validate-brief.py` lines 610-639:
  - **Exact-range match**: succeeds silently — no error, no warning, nothing
    added to the report.
  - **Window-only match** (quote found only via the fixed surrounding-line
    window, not the exact cited range): emits `EVIDENCE_QUOTE_WINDOW_MATCH`
    (warning) and reports the actual matched line/detail.
  - **Duplicate/ambiguous window match** (more than one candidate line
    matches): also emits `EVIDENCE_QUOTE_WINDOW_MATCH`, whose message
    reports the candidate location(s) so a human can verify the match
    deterministically; it does not silently pick one without disclosing it.
  - **No match at all**: blocking `EVIDENCE_QUOTE_NOT_FOUND` (error).
  The prior wording — "the validator reports the exact matched line whether
  the match was exact-range or window-only" — is corrected: an exact-range
  match produces **no report at all** (nothing to reconcile), only
  window/ambiguous matches and not-found cases are surfaced.
- `HIGH_RISK_CLAIM_NEEDS_SUBSTANTIVE_AUDIT` warning fires for `Safety Gaps` /
  `Ghost Features` types, operationalizing ADR 0016's D5 threshold.
- Legacy briefs without `weakness_type` validate with a warning, not a
  failure.
- No auteur rerun, no routing/Wayfinder/Step 2 change, no ADR status change
  occurred as part of PR #81. The `artifact-contracts.yaml` diff against
  baseline `main@8b73408` is verified (via `git diff --stat`) to be exactly
  **3 inserted lines** (two new machine-field entries plus one new notes
  line) and 0 deletions — the prior "three new field/notes lines" wording is
  confirmed accurate, not a fragile approximation.
- Targeted tests (`tests/test_weakness_type_and_quote_contract.py` and four
  related suites): passing at `9a7d7d5`. `scripts/validate-repo.py`: passes.
  Full suite comparison against baseline `main@8b73408` shows the same 23
  pre-existing failures/3 collection errors on both revisions (like-for-like
  regression check, per CLAUDE.md's verification-discipline rule) — none of
  the 23 touch weakness-type or evidence-quote logic.

## 2. Residual implementation debt (non-blocking, documented)

| Debt | Severity | Blocks phase closure? | Blocks external experiment? | Disposition |
|---|---|---|---|---|
| Duplicate `weakness_type:` key in the §13 YAML fence is not detected; PyYAML's `safe_load` silently keeps the last value with no warning or error. This was a severity-matrix design expectation in issue #80, not a checklist acceptance criterion (see §1a), and it rested on an incorrect assumption that duplicate keys are a YAML-parser-level failure | Low | No (not a checklist item) | Only if an artifact with a duplicate key is fed to an external experiment unchecked — see §3 | Future implementation work (not raised in original review's checklist, and not previously implemented) |
| `WEAKNESS_TYPE_OTHER_NO_EXPLANATION`'s "blocks human final approval" claim is enforced only in the warning message text and doc/template prose — no code gate exists that reads this warning and prevents a downstream action | Informational | No | No | Intentional human-process boundary, consistent with D6 (human reviews every final brief) — not a code defect |
| Stray duplicate fixture `tests/fixtures/validate-brief/invalid/unknown-weakness-type.md` left alongside its replacement `tests/fixtures/validate-brief/valid/unrecognized-weakness-type-warning.md` | Informational | No | No | Cosmetic; pre-existing debt, harmless |
| 23 pre-existing failing tests / 3 collection errors (integration/executor-plumbing, path-drift, generate-plan-conformance, one unrelated field-contract-agreement case) | Medium | No (confirmed present identically on baseline `main@8b73408`) | Possibly, for unrelated workflows | Pre-existing debt, out of this phase's scope; not introduced by PR #81 |

None of the above is a defect introduced by PR #81. The duplicate-key gap is
a genuine, low-severity absence relative to design narrative in issue #80
(not a failed checklist criterion, per §1a).

## 3. Conclusion

**B — Phase complete, with documented non-blocking debt.** All of issue
#80's checklist acceptance criteria are satisfied by the merged PR #81. The
one genuine gap found — duplicate-`weakness_type`-key handling — was never
a checklist acceptance criterion (it appears only in the issue's severity
matrix narrative, resting on an incorrect assumption about YAML parsing);
its absence does not fail any criterion PR #81 was scored against, and it is
low severity and untested today.

This does **not** block a controlled external experiment categorically —
rather: **it does not block a controlled external experiment provided
generated artifacts are checked to contain only one `weakness_type` key**
before being fed into experiment tooling. An artifact with a duplicate key
would have its `weakness_type` silently resolved to PyYAML's last-value
behavior, which could misrepresent the diagnosed weakness type to a human
reviewer or downstream consumer without any warning surfacing. That failure
mode is plausible only if such an artifact is generated and used unchecked;
a simple pre-experiment duplicate-key check (or fixing the gap outright)
removes it. No corrective PR is required before proceeding to the next
readiness question, but this caveat should travel with any E1-E4 experiment
authorization (see §5).

## 4. Readiness status (unchanged by this phase)

Per `docs/PRODUCT-CONTRACT-REVIEW-2026-07-26.md` Part 5 and
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md`: the highest currently justified
readiness level remains **"Externally exercised"** (Level C). PR #81 fixes
an internal contract defect surfaced by the auteur campaign; it does not
itself constitute new external evidence, so it does not advance the
readiness level. Reaching "Externally validated" (Level D) still requires
satisfying the ratified D8 evidence bar for external repository-sensemaking
briefs, which has not occurred. This refers to `repo-sensemaker` Stage A
brief validation, not architectural-review or workflow Step 2.

**This remains true after the D7/D8/E4 ratification recorded in §5 below.**
Ratifying a *target* and an evidence bar does not itself satisfy that bar —
the achieved readiness level stays **"Externally exercised"** until the
staged evidence plan (E4) actually produces the D8 evidence. No experiment
has run as of this document.

## 5. Open owner decisions

Per commit `1ad42ca` ("apply explicit owner ratification of D1-D6, D9, D10"):
D1-D6, D9, D10 are ratified.

**2026-07-26 update (later same day): D7, D8, and experiment authorization
have now been explicitly ratified by the owner**, per
`docs/OWNER-DECISION-PACKAGE-2026-07-26.md` Part 7 (updated). The ratified
values:

```text
D7 = Externally validated
D8 = Success on at least two structurally different external repositories,
     including real human usefulness evaluation on at least one target.
Experiment authorization = E4 -- staged combination
  Stage 1: controlled auteur rerun
  Stage 2: second structurally different repository (conditional on Stage 1)
  Stage 3: real-maintainer usefulness evaluation (conditional on Stage 2)
```

Ratifying D7/D8/E4 is a governance and evidence-planning act only. It does
**not** itself advance the currently achieved readiness level (§4, below,
remains unchanged), does not authorize running any experiment stage, and
does not constitute a production-readiness claim. Only Stage 1 **planning**
is currently authorized (a single planning issue, #83); **Stage 1 execution
is not yet authorized** and requires a separate, explicit owner instruction
issued after review of the final pinned revisions, model/provider
configuration, environment, and exact command. Stages 2 and 3 remain
conditional on owner review of the prior stage's evidence and are not
authorized now. This planning-only boundary is a deliberate choice: an
earlier informal draft of this decision used the phrase "Stage 1 is
authorized for execution now" — that phrasing is explicitly superseded and
does not apply; the authorized boundary is planning only, as stated here.
ADR 0021 (production readiness) stays PROPOSED pending its other named
owner-decision items (see that ADR). D7's ratified target does not require,
and does not introduce, any architectural-review or workflow "Step 2" pass —
see ADR 0021's D7 note for the exact wording (issue #83 tests only the
`repo-sensemaker` Stage A brief).

### D7 — next readiness target

Current justified level (factual, already met, not a decision): **C —
Externally exercised**.

| Option | Meaning | Evidence required | Cost/risk |
|---|---|---|---|
| A. Remain experimental | No readiness claim advances beyond internal use | None beyond today | Low cost; stalls external credibility |
| B. Internally proven | Internal test/validator suite is the bar | Suite green (already true) | Low cost; weak external signal |
| C. Externally exercised (current) | At least one real external repo run through the pipeline | `auteur` campaign (PR #67/#70/#73/#78) | Already met; known gap: diagnosis never substantively audited |
| D. Externally validated | External repository-sensemaking briefs satisfy the ratified D8 evidence bar | Successful, repeatable Stage A brief validation on at least two structurally different repositories, with substantive audit, no target mutation, and human usefulness review on at least one target | Requires an actual experiment (E1-E4 below); moderate cost |
| E. Limited production pilot | 10-20 real users | D plus pilot infrastructure/support | High cost; review flags this as premature (skips D) |
| F. General production readiness | All teams | E plus scale evidence | Highest cost; far beyond current evidence |

This option table has been updated to reflect the later ratified D7/D8
definition (§5 below). Earlier draft wording that required workflow Step 2
is superseded and no longer applies — D7's ratified target is limited to
`repo-sensemaker` Stage A brief validation and explicitly excludes
architectural-review and workflow Step 2.

Recommendation on file (`OWNER-DECISION-PACKAGE-2026-07-26.md` Part 2/4): D,
explicitly not skipping to E. This is a recommendation, not a decision.

Owner field:

`D7 = ____`

### D8 — external-validation bar

| Option | Required proof | Strengths | Weaknesses |
|---|---|---|---|
| A. One external repo, repeatable success | Same repo re-run passes consistently | Cheap, fast to gather | Doesn't test generalization across repo shapes |
| B. Two+ structurally different repos | Independent repos, different architectures, both pass | Tests generalization | More costly; still no human-maintainer signal |
| C. Real maintainer use on one repo | An actual maintainer (not the pipeline author) uses it and finds it useful/correct | Tests real-world utility, not just structural pass | Single data point; maintainer selection bias possible |
| D. Multiple repos + real maintainer use | B and C combined | Strongest evidence | Highest cost; slowest to gather |

Per the durable package, this is **explicitly left unresolved** — no default
is proposed because only one external repo (`auteur`) has ever been
attempted, so no evidence currently distinguishes these bars.

Owner field:

`D8 = ____`

### Experiment authorization

- E0 — no experiment yet (current state)
- E1 — controlled auteur rerun
- E2 — second structurally different repository
- E3 — real-maintainer evaluation
- E4 — staged combination with explicit ordering and stop rules

None of E1-E4 has been authorized or performed as part of PR #81 or this
closure document.

Owner field:

`Experiment authorization = ____`

## 6. No further action taken

This document is a closure record only. It authorizes no experiment, no
auteur rerun, no D7/D8 ratification, no ADR promotion, and no further
implementation.
