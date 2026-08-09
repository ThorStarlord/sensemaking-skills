# Mode B+ completion report — candidate/sensemaking-vnext, first pass

**Branch**: `candidate/sensemaking-vnext`, pushed to origin. Built from `main` @ `e790f30`, not from `prototype/repo-sensemaker-vnext` (#164, preserved untouched as the evidence record). 9 commits. Not merged — per Mode B+'s retained boundary, merge stays an explicit owner decision.

This is a first coherent pass, not a claim that every idea discussed across the whole engagement has been addressed. Scope was deliberately the vNext brief/interaction work specifically (the thing #164 spent four rounds generating evidence about) — other named-but-separate tracks (the `fog_type` alias repair, the CI-governance defect, S3 interaction research) were not touched; they remain in their own lanes per the pre-existing three-lane framework, which Mode B+ only reweighted (construction no longer gated), not discarded.

## Final architecture

One skill, not two (`repo-sensemaker`), with two labeled, separately-headed responsibilities:
- **Diagnose** — unchanged mechanics, produces the Repository Sensemaking Brief exactly as canonical `main` does today, extended only by an optional `## 15. Extended analysis (candidate)` block.
- **Interact** — new section, explicitly scoped to conversational (non-runtime) invocation, implementing investigate-first / classify-uncertainty / neutral-clarify / synthesize, evidenced by the prototype's real-use experiment.

Section 15 is wired through the *real* production path: `scripts/brief_skeleton.py`'s `build_skeleton()`/`reconcile()` (not a freeform appended block, which would not survive real runtime invocation — see below), validated non-blockingly by `validate-brief.py`, declared and classified in `artifact-contracts.yaml` under a new `candidate_machine_fields` key per ADR 0015's requirement.

`architectural-review` gained one optional, additive Boundary Rule (6) that uses two Section 15 fields when present; nothing else about it changed. No new consumer skill was built — `architectural-review` already consumes the brief holistically and already has an `investigate_first` fallback, so no proof-of-composition skill (unlike #164's `vnext-review-consumer`) was needed.

## What was kept, revised, or dropped from the prototype

| Prototype element | Disposition here | Why |
|---|---|---|
| Two-Skill split (Option A) | **Dropped, collapsed to Option C** | No evidence ever differentiated A from C; a new grounding fact (Interact cannot run under automated runtime execution regardless of packaging) makes C the coherent choice, not just the simpler one. |
| `uncertainty.source`/`.question` | **Kept as-is** | Strongest, most repeatedly load-bearing field across every real-use test. |
| `consequential_boundary`/`is_demonstrated_weakness` | **Kept as-is** | Real verdict-changing evidence (P4; `pursue` vs `pursue_narrowed`). |
| `owner_intent_state` | **Kept, revised** | Dropped the freestanding `unresolved` prose (duplicated `uncertainty.question`, could drift); now `{known, status}` only. |
| `domain` | **Kept, tightened** | One real, distinct disclosure effect in the real-use experiment; ambiguity about multi-value semantics resolved by rule, not left to per-instance judgment. |
| `discovery_confidence` | **Kept as-is** | Formalizes an already-evidenced pre-vNext practice; low-confidence path untested but not unsupported. |
| `evidence_status_notes` | **Dropped entirely** | Never exercised in any real run across #164's full history — pure YAGNI. |
| `repository-diagnostician` (separate file) | **Dropped** | Its content is what Diagnose already is; no behavior was lost, only duplicate packaging. |
| `vnext-review-consumer` (proof-of-concept skill) | **Not carried forward** | Served its purpose (proved the brief-as-boundary hypothesis under real isolation); the real `architectural-review` already composes safely, so no permanent shadow skill is needed. |

## Important autonomous decisions and rationale

See `docs/candidate/architecture-decision.md` for the full reasoning (written before implementation, per the working mode's own instruction). Headline: the Diagnose/Interact packaging decision rests on a mechanical fact found during recon, not just "no evidence differentiates them" — the automated runtime path has no chat channel mid-run, so Interact is conversational-only *by construction*, and a separate, independently-routable Skill file would misrepresent that.

## Contract/ADR changes required for real adoption

- `docs/candidate/draft-adr-extended-analysis.md` — DRAFT, unfiled, unnumbered. Classifies all five Section 15 fields as "model, constrained," optional and non-blocking (a stronger guarantee than `weakness_type`'s ADR-0015-ratified "required but non-blocking"). Nothing in it is ratified.
- `artifact-contracts.yaml`'s new `candidate_machine_fields` key is itself a real, if small, contract-shape change that would need owner sign-off before being read as anything other than "documented on this branch."

## Migrations

None required. Every change is additive: existing canonical Section 1-14 briefs, existing `architectural-review` behavior without Section 15, and existing tests are all unaffected by Section 15's absence (proven directly by `test_extended_analysis_end_to_end.py`'s second test).

## Test and verification evidence

- 3 new/extended test files for the mechanism itself: `test_brief_skeleton_extended_analysis.py` (9 tests, TDD RED-GREEN), `test_validate_brief_extended_analysis.py` (8 tests, TDD RED-GREEN), `test_extended_analysis_end_to_end.py` (2 tests, real producer through both real validators).
- Full-suite baseline comparison (not just "tests pass in isolation"): ran the identical `pytest tests/` invocation against a temporary worktree of `main` @ `e790f30` and against this branch. Baseline: 20 failed / 1892 passed. This branch, first pass: 21 failed / 1910 passed — one genuine regression, found and root-caused (a template contract test assumed "the last yaml fence in the file" meant "the Complete Example block," which Section 15's own documentation-yaml-fences broke). Fixed by anchoring the lookup to the actual `### Complete Example` heading instead of file position — the same latent-fragility-vs-position-assumption class of bug this repo has hit before (see CLAUDE.md's own verification-discipline notes). After the fix: this branch's failures are the *identical 20* as baseline, confirmed by name, plus the 18 net new passing tests. Zero unexplained regressions.
- `scripts/validate-repo.py` passes.
- One environmental note, not a regression: `test_field_contract_agreement.py::test_fog_type_field_aliases_exist_in_contracts` fails identically on both branches (a pre-existing `fog_type` runtime-alias/contract-declaration gap, unrelated to this work — the same class of issue the `fog_type` alias repair on the `main`/#163 lane already exists to fix, separately).
- One further environmental discovery, also pre-existing and unrelated: `validate-artifact.py` checks `recommended_workflow_id` against `docs/canonical-vocabulary.yaml`'s workflow list, while `validate-brief.py` checks it against the fuller `workflow-registry.yaml` — a second instance of the same registry-drift class PR #163 fixes for fog types, this time for workflow ids. Found while building the end-to-end test, worked around in the test fixture (used a workflow id present in both registries), not fixed — out of this branch's scope.

## Known uncertainties (unchanged from the prototype's own honest accounting, not newly resolved by this branch)

- Whether a real owner, not this session, finds the Interact procedure's burden-reduction claim as clean in practice as the isolated real-use tests suggested.
- `discovery_confidence.level: low`'s downstream behavior — still untested in any run, prototype or candidate.
- No case has tested what happens when Section 15 disagrees with Section 1-14's own content — the validator doesn't check cross-section consistency, and whether it should is explicitly open (see the draft ADR's Missing evidence section).
- Whether the bundling-avoidance behavior (evidence-resolved-vs-owner-authorized) generalizes beyond the one brief shape it's been tested against twice — the prior retrospective's own named next step, not yet run again on this branch.

## What still requires owner ratification

Everything in `candidate_machine_fields` and the draft ADR — nothing here is claimed as accepted. The Diagnose/Interact packaging decision itself, though better-grounded than the prototype's version, is still this session's judgment call, not an owner decision.

## Recommended merge sequence (not executed, no merge performed)

1. Owner reviews this branch's diff against `main` directly (9 commits, additive-only, verified zero unexplained regressions).
2. If the Section 15 mechanism and Diagnose/Interact packaging are judged sound: promote the draft ADR to a real, numbered, Proposed ADR; get explicit sign-off on the field classifications.
3. Separately: PR #163 (fog-vocabulary registry-driven fix) merges on its own schedule, independent of this branch's fate — the two don't block each other, though this branch's `primary_fog_type` handling would benefit from #163's fix once both exist on `main`.
4. Only after 1-2: merge decision, explicitly made by the owner, not inferred from "tests pass."

Per Mode B+'s retained boundary: stopping here. Not merging. Report delivered for review.
