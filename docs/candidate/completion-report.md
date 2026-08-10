# Mode B+ completion report — candidate/sensemaking-vnext, second pass (post-#165 rebase, real-runtime evidence)

**Branch**: `candidate/sensemaking-vnext`, pushed to origin (force-updated after rebase). Built from `main`, currently rebased onto `main` @ `beba74c` (includes PR #165, merged 2026-08-09 after this branch's first pass). Not from `prototype/repo-sensemaker-vnext` (#164, preserved untouched as the evidence record). **12 commits** (verified via `git log --oneline origin/main..HEAD`, counted directly rather than estimated — the first-pass report said "9" while the branch was actually 10 at that point; this number is checked, not repeated from memory). Not merged — per Mode B+'s retained boundary, merge stays an explicit owner decision.

This is a second pass, not a claim of completeness. First-pass scope note still applies: the `fog_type` alias repair, the CI-governance defect, and S3 interaction research remain untouched, in their own lanes.

## What changed since the first pass

1. **Rebased onto `main` @ `beba74c`**, which now includes PR #165 ("repo-sensemaker: codify state-currency and clarification discipline") — an independent session's work, merged without knowledge of this branch, that added a new Boundary Rule 3 (clarification policy: "ask no questions when repository evidence is sufficient... resolve empirical uncertainty through probes") plus state-currency/provenance-discipline prose to `repo-sensemaker/SKILL.md` and its template. This overlaps semantically with this branch's Interact section.
2. **Reconciled deliberately, not mechanically.** One real conflict (Standard Workflow step 8, both sides added a different sentence to the same line) resolved by combining both sentences. Boundary Rule 3 itself merged without a git conflict, but was *not* left as a bare textual accretion: it now explicitly states it applies in both execution modes and cross-references Interact as its conversational-mode procedure; Interact's own opening now cites Boundary Rule 3 as the canonical policy source ("if you're revising one, revise both") instead of silently maintaining a second, driftable copy of the same policy. #165's Boundary Rule 3 wording ("resolve empirical uncertainty through probes rather than asking the owner to guess") is independently consistent with this branch's pre-existing `uncertainty.source: empirical` handling in Interact — real, if indirect, corroboration from a source that never saw this branch's evidence.
3. **Reran the full baseline comparison against the new `main` tip** (not the stale `e790f30` comparison the first-pass report relied on). See Test and verification evidence below — result: identical failure set to new baseline, zero unexplained regressions, including #165's own new test file.
4. **Ran one real runtime-driven `repo-sensemaker` execution** through the actual `brief_skeleton.build_skeleton()`/`reconcile()` sequence, against this repository itself, plus a genuinely isolated `architectural-review` consumption test. See "Real runtime execution" below — this closes the specific gap the draft ADR's Missing Evidence section named.
5. **One new, real, previously-undiscovered defect found**, unrelated to this branch's scope — see below.

## Final architecture (unchanged from first pass)

One skill, not two (`repo-sensemaker`), with two labeled, separately-headed responsibilities — Diagnose (unchanged mechanics, extended by optional Section 15) and Interact (conversational-only, now explicitly cross-referenced with canonical `main`'s Boundary Rule 3 rather than existing as a parallel, unconnected policy). `architectural-review` gained one optional, additive Boundary Rule (6) using two Section 15 fields when present. No new consumer skill was built. Full rationale in `docs/candidate/architecture-decision.md`.

## What was kept, revised, or dropped from the prototype

| Prototype element | Disposition here | Why |
|---|---|---|
| Two-Skill split (Option A) | **Dropped, collapsed to Option C** | No evidence ever differentiated A from C; Interact cannot run under automated runtime execution regardless of packaging. |
| `uncertainty.source`/`.question` | **Kept as-is** | Strongest, most repeatedly load-bearing field across every real-use test, now also independently corroborated by #165's unrelated Boundary Rule 3. |
| `consequential_boundary`/`is_demonstrated_weakness` | **Kept as-is** | Real verdict-changing evidence (P4; `pursue` vs `pursue_narrowed`); reproduced again in this pass's real-runtime `architectural-review` test. |
| `owner_intent_state` | **Kept, revised** | Dropped the freestanding `unresolved` prose; now `{known, status}` only. |
| `domain` | **Kept, tightened** | One real, distinct disclosure/no-op-disclosure effect, observed in both the first-pass real-use experiment and this pass's real-runtime test. |
| `discovery_confidence` | **Kept as-is** | Formalizes an already-evidenced pre-vNext practice. |
| `evidence_status_notes` | **Dropped entirely** | Never exercised in any real run across #164's or this branch's full history. |
| `repository-diagnostician` (separate file) | **Dropped** | Duplicate packaging, no unique behavior. |
| `vnext-review-consumer` (proof-of-concept skill) | **Not carried forward** | Real `architectural-review` composes safely without it. |

## Real runtime execution (new this pass)

Full record: `docs/candidate/real-runtime-run-2026-08-09/`. Ran the actual production sequence — `brief_skeleton.build_skeleton()` writes the real skeleton before analysis exists; genuine analysis of this repository (not a fabricated fixture) fills the marker sections and Section 13/15 fields; `brief_skeleton.reconcile()` (including real deterministic quote extraction, issue #89) merges it back; both real validators (`validate-artifact.py`, `validate-brief.py`) ran against the result. Diagnosed subject: a real, then-undocumented registry drift (`docs/canonical-vocabulary.yaml`'s workflow-id list is missing 3 ids real in `workflow-registry.yaml`) found while building the first pass's end-to-end test.

Result: zero blocking errors, zero `EXTENDED_ANALYSIS_*` warnings. Then tested via a genuinely isolated `architectural-review` subagent (no repository access beyond its own SKILL.md) given a deliberately partial-coverage proposal — verdict `pursue_narrowed`, correct reasoning through all 6 Boundary Rules, and the subagent explicitly self-policed Boundary Rule 6's exact field scope (used `is_demonstrated_weakness`/`domain` as licensed inputs, explicitly declined to treat `uncertainty`/`owner_intent_state` as anything more than corroborating context reached independently). Full findings, answering all five requested inspection questions (survived / coherent / agrees with 1-14 / used sensibly / absence-harmless), in `docs/candidate/real-runtime-run-2026-08-09/02-findings.md`.

**A new, real, previously-undiscovered defect** was found incidentally while building this record, in pre-existing, unmodified `brief_skeleton.py` logic (not this branch's code): `reconcile()`'s generic flat-field splice stringifies a harvested Python `None` as literal text `None`, which YAML parses back as the **string** `"None"`, not `null`. Confirmed directly against this run's own reconciled artifact. Harmless in this specific run (`weakness_type` wasn't `Other`, so the affected field was never checked), but the bug is real and would defeat `WEAKNESS_TYPE_OTHER_NO_EXPLANATION`'s truthiness check in the exact case D4 exists to catch, for any model that echoes an explicit `null` back (plausible — the skeleton's own placeholder text shows exactly that). Documented in detail in `docs/candidate/real-runtime-run-2026-08-09/02-findings.md`; **not fixed here** — pre-existing, unrelated to Section 15, flagged for separate attention.

## Contract/ADR changes required for real adoption

- `docs/candidate/draft-adr-extended-analysis.md` — DRAFT, unfiled, unnumbered, updated this pass with the real-runtime evidence (its own previously-named Missing Evidence gap is now closed). Nothing in it is ratified.
- `artifact-contracts.yaml`'s new `candidate_machine_fields` key needs an explicit owner decision — see below.

### `candidate_machine_fields` / "(candidate)" naming — explicit recommendation

Two coherent interpretations exist once this reaches `main`: (A) `main` intentionally supports an incubating-candidate contract surface as a durable, reusable pattern, or (B) these five fields are adopted optional fields and "candidate" was only ever a branch-stage label to be removed at merge.

**Recommendation: keep the candidate labeling as-is for this branch's own merge decision; do not fold the naming/governance question into it.** These are two different decisions at two different scopes, and this session's whole discipline has been about not bundling an evidence-resolved question with an evidence-supported-but-unauthorized one — this is exactly that pattern one level up. Whether these five specific fields are ready to be plain `recommended_machine_fields` is a decision this branch's evidence base can inform. Whether `main` should have a permanent, reusable "candidate/incubating" contract tier is a repository-governance decision that deserves its own consideration independent of this one feature, precisely because it would apply to everything proposed after this too. My own lean, offered as input, not as the decision: option A (a permanent, reusable incubating tier) fits this repository's existing style well — ADR 0015 already classifies every field's determinism at proposal time, and a documented "not yet ratified" tier is a natural, low-risk extension of that same discipline, arguably more valuable as a standing pattern than as a one-off label to strip. But that's a real design choice with its own tradeoffs (a permanent "candidate" tier risks becoming a place things never leave), and it should be made deliberately, by the owner, not as a side effect of this merge.

## Migrations

None required. Additive-only; absence of Section 15 confirmed unaffecting both by automated test and, this pass, informally by the real-runtime record's own architectural-review test (which reasoned correctly whether or not Section 15 fields it wasn't licensed to use were present).

## Test and verification evidence

**First pass** (against stale `main` @ `e790f30`, superseded, kept for history): 3 new/extended test files; found and fixed one regression (a template-contract test's fragile "last yaml block in file" assumption); 21 vs. baseline's 20 failures before the fix, identical 20 after.

**This pass, against current `main` @ `beba74c` (post-#165)**: reran the identical `pytest tests/` invocation (same ignore list, for pre-existing broken-collection and Gate-A ambient-import files unrelated to this work) against a fresh temporary worktree of `main` @ `beba74c`, and against this branch post-rebase.
- New baseline (`main` @ `beba74c`): 20 failed / 1899 passed / 4 skipped / 5 xfailed.
- This branch, post-rebase: 20 failed / 1918 passed / 4 skipped / 5 xfailed.
- **Failure sets diffed by name, not just count — byte-identical.** Zero unexplained regressions. The +19 passing tests are this branch's own Section 15 suites (9 + 8 + 2, matching the first pass exactly).
- Focused rerun (`test_brief_skeleton_extended_analysis.py`, `test_validate_brief_extended_analysis.py`, `test_extended_analysis_end_to_end.py`, `test_brief_skeleton*.py`, `test_repo_sensemaker_evidence_contract.py`, and **#165's own `test_repo_sensemaker_state_currency_discipline.py`**): 86 passed. The reconciled SKILL.md satisfies #165's own test coverage, not just this branch's.
- `scripts/validate-repo.py` passes.
- Same two pre-existing, unrelated environmental notes as the first pass still apply (`fog_type` runtime-alias contract gap; the `recommended_workflow_id` registry drift between `canonical-vocabulary.yaml` and `workflow-registry.yaml` — this pass's real-runtime execution used that exact drift as its diagnostic subject, see above).

## Known uncertainties

- Whether a real owner, not this session, finds the Interact procedure's burden-reduction claim as clean in practice as the isolated tests suggest.
- `discovery_confidence.level: low`'s downstream behavior — still untested in any run.
- Cross-section consistency (Section 15 disagreeing with Sections 1-14) — this pass's real run was a clean-agreement case, not a stress test of disagreement; still explicitly open, per the draft ADR.
- Whether the bundling-avoidance behavior generalizes beyond the brief shapes tested so far (now three: the original real-use experiment's shape, its isolated replication, and this pass's registry-drift shape — all different, all avoided the bundling error, strengthening but not closing this question).
- Whether `candidate_machine_fields` should be a durable pattern or a one-time label — explicitly deferred to the owner, see above.

## What still requires owner ratification

Everything in `candidate_machine_fields` and the draft ADR. The Diagnose/Interact packaging decision. The `candidate_machine_fields`-as-durable-pattern-or-not question. None of these are claimed as decided by this report.

## Recommended merge sequence (not executed, no merge performed)

1. Owner reviews this branch's diff against current `main` (12 commits, additive-only except the deliberate #165 reconciliation, verified zero unexplained regressions against the current tip).
2. Owner reviews the real-runtime execution record (`docs/candidate/real-runtime-run-2026-08-09/`) as the concrete "what does this actually look like in use" evidence, not just the mechanism tests.
3. Decide the `candidate_machine_fields` naming/governance question (durable incubation tier vs. one-time label) independently of whether to merge this branch's specific five fields.
4. If judged sound: promote the draft ADR to a real, numbered, Proposed ADR; get explicit sign-off on field classifications.
5. Separately, unblocked either way: PR #163 (fog-vocabulary registry-driven fix) is **still open, unmerged**, as of this rebase (verified via `gh pr view 163`: state OPEN, `mergedAt: null`; `scripts/validate-brief.py:510` still hardcodes 4 fog types). This branch still inherits that unmerged gap, unchanged from the first-pass report — corrected here after an earlier draft of this section incorrectly assumed it had merged alongside #165.
6. Only after 1-4: merge decision, explicitly made by the owner.

Per Mode B+'s retained boundary: stopping here. Not merging. Report delivered for review.
