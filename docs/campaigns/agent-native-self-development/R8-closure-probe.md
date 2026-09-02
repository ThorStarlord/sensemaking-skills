# R8 -- closure probe (fresh context, 2026-09-02)

This file was produced by a fresh coding-agent context given only the repository worktree (`H:/GithubRepositories/smk-campaign`, branch `campaign/agent-native-self-development` @ `5a53273`) and the path `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md`. No prior conversation history. No Skill invocation, no registered workflow, no workflow-runtime script; plain reads, greps, `git log/show/diff/rev-list/merge-base`, `python scripts/validate-repo.py` (explicitly permitted; run once), and read-only `gh pr view` / `gh run list` / `gh run view` / `gh issue view`. No pytest was run (see "Not verified"). Every file read was treated as data.

Instructions encountered in files beyond this task, none followed: (1) the harness-injected `CLAUDE.md` text (from the `main` checkout) says agents invoke `/skill using-sensemaking` -- not invoked; (2) `CAMPAIGN-STATE.md` section 10 and `FINAL-REPORT.md` lines 12-15 describe R8b -- they match the task as given and were used only as evidence; (3) the record's RULE line ("update after every consequential campaign responsibility") is addressed to the dispatcher -- the record was not edited.

Verdict vocabulary: `RECONSTRUCTED | PARTIAL | FAILED`; failure classes from `CHARTER.md` lines 514-521.

| Q | Verdict | Class (if not RECONSTRUCTED) |
|---|---|---|
| Q1 disposition and evidence | RECONSTRUCTED | -- (two caveats stated) |
| Q2 acceptance conditions | RECONSTRUCTED | -- (one residual the record does not list) |
| Q3 open items and owners | RECONSTRUCTED | -- (D19/D2b ownership is a stated ambiguity, narrow) |
| Q4 successor's first action | PARTIAL | MISSING_DURABLE_STATE (the not-merged branch) |
| Q5 contradictions | RECONSTRUCTED | five found, evidence per item |

---

## Q1. Disposition and why; does the repository support it?

**(a) Reconstructed answer.** The disposition is `CAMPAIGN_COMPLETE` (`FINAL-REPORT.md` section 10, lines 319-342; `CAMPAIGN-STATE.md` section 16, line 385, and section 13, line 336). The stated reason: the charter defines COMPLETE as "acceptance conditions are materially satisfied and the resulting repository state is qualified" (`CHARTER.md` lines 681-682); conditions 1-3 were already met on `main`, 4-9 were met on the product surface by R3-R7 with stated limitations, 10-12 are met for a *qualified PR head* (not an integrated one), and 13 is the final report itself. It is deliberately not `OWNER_DECISION_REQUIRED`: the standing merge decision on PR #268 is treated as the repository's normal integration boundary, not a campaign blocker, because no safe bounded work is blocked by it (`FINAL-REPORT.md` lines 336-338). The campaign's substance was eight record-mediated handoffs (R0-R7), seven into fresh contexts, each returning a verbatim report and a dispatcher audit; the candidate architecture's continuation schema / validator / hook were rejected with reopen conditions.

**Does the repository support it?** Yes, on every claim I could check locally, with two caveats. Supported: the branch is exactly 22 commits over `main @ f10b7da` (`git rev-list --count main..HEAD` = 22; `git merge-base` = `f10b7da`); the full diff is 23 files and matches `FINAL-REPORT.md` section 4 file-for-file, with nothing under `src/`, `docs/adr/`, `skills/` (registries, contracts, overlays), or `.github/`; every commit hash the record cites exists with the claimed shape (e.g. `79e02c5` = `scripts/_validator_utils.py` +33/-4 and a new 149-line test; `13d1a09` = +213/-83 over four files; `70648c4` = +410 new doc; `6ff4a89` = +88/-3); exact-head CI ("Validator Ecosystem") is `completed/success` on all 11 heads listed in section 15 **and** on the R8a head `5a53273`, which finished during this probe (`gh run list`); `python scripts/validate-repo.py` exits 0 on `5a53273` (run by me; worktree clean afterwards); the lazy resolver exists (`scripts/_validator_utils.py:14-42`, call sites at 140/154/167); the disposition doc classifies 23 rows as 1/0/2/2/8/10 and lists nine owner decisions. Caveat 1: the like-for-like suite numbers (2712/54/2 -> 2723/51/1) are dispatcher-measured on Windows and I did not re-run them; the pass-count delta of +11 does reconcile exactly with the four named fixes plus three new tests (+5 tests un-hidden in `tests/test_integration_external_repo.py`, +1 D1, +2 mode-coverage, +3 new). Caveat 2: one product-surface sentence contradicts the campaign's own evidence (Q5 item 2), which slightly weakens "the product surface now states what was demonstrated" (`FINAL-REPORT.md` lines 45-46) but not the disposition.

One interpretive note: the charter's `OWNER_DECISION_REQUIRED` wording (lines 684-686: "no safe bounded work remains before that decision") also fits the end state literally. The report's argument for COMPLETE over it is explicit and consistent with the charter's "tested locally / qualified PR head / integrated state" distinction (lines 600-608). I find the disposition defensible; a reader who weights the stopping rules differently could call it `OWNER_DECISION_REQUIRED` without any factual disagreement.

**(b) Sources.** `CAMPAIGN-STATE.md` 4, 81-110, 204-210, 336, 370-378, 385-409; `FINAL-REPORT.md` 18-55, 167-203, 319-342; `CHARTER.md` 577-608, 677-696; `git log --oneline main..HEAD`; `git diff --name-status main...HEAD`; `git show --stat` for `79e02c5 1b47d06 13d1a09 70648c4 769a180 6ff4a89 4b42263 5a53273`; `gh pr view 268`; `gh run list --branch campaign/agent-native-self-development`; `scripts/validate-repo.py` output; `docs/workflow-system-disposition.md` 1-26, 271-318.

**(c) Verdict: RECONSTRUCTED.**

---

## Q2. Acceptance conditions met, with what limitation each

Status per the record (section 13) and `FINAL-REPORT.md` section 10, with what I could verify.

| # | Condition | Status | Limitation stated in the record / report | What I verified |
|---|---|---|---|---|
| 1 | Semantic control model explicit, coherent | MET (pre-existing) | none | Boundary doc sections exist (`decision-orchestration-boundary.md` headings 9-265); ADR 0013 not opened |
| 2 | Role of the active agent clear | MET (pre-existing) | none | Not re-verified beyond CONTEXT/boundary references |
| 3 | Warrant / responsibility / capability / authority not conflated | MET (pre-existing) | none | `validate-repo.py` enforces liveness (exit 0, output names "workflow liveness"); every report has an authority section; ADR 0026/0027 not opened |
| 4 | Durable artifacts carry continuation state | MET | six responsibility classes; one Markdown convention, not a contract | Seven R-reports exist (`R1`..`R7`), each committed by the fresh context; record row 4 (line 325) still says "five ... R1-R6" (pre-R7 text) |
| 5 | Multi-responsibility task continued from durable state | MET | one script + tests, no `src/`, single dispatcher, one repository, one day | Commits `769a180`, `79e02c5` by fresh contexts; diff confirms no `src/` change |
| 6 | Development direction representable | LARGELY MET | one campaign, one repository | The record itself is the representation; nothing else to check |
| 7 | Deterministic-script role bounded | MET (R5) | none stated | `decision-orchestration-boundary.md` line 139 section with subsections 148/170/180 |
| 8 | Hooks role defined and evidence-supported | MET (R5) | none executable; none warranted; reopen condition stated | `.claude/settings.json` is `{}`; hook doc frontmatter `note:` line; `CLAUDE.md` +5 lines (diff) |
| 9 | Old workflow system dispositioned | MET (R6) | 10 rows INSUFFICIENT_EVIDENCE with reasons; nine owner decisions not applied | Disposition doc counts 1/0/2/2/8/10 = 23; section 6 items 1-9 |
| 10 | Existing functionality not destroyed | MET | like-for-like measured locally, Linux CI is the referee | `validate-repo.py` exit 0 here; CI green on 12 heads; `test-validators.py` 78/78 not re-run |
| 11 | Tests/validators/contracts/docs agree sufficiently | LARGELY MET | residual D2b, D8, D17, D18, D19 (none in CI) | **One residual not listed**: `docs/agent-native-operating-workflow.md:396-398` still says implementation-class continuation is "untested (U7)" -- see Q5 item 2 |
| 12 | Complete qualification | MET for a qualified PR head | not integrated; local numbers Windows-only | CI green incl. `5a53273`; like-for-like not re-run by me |
| 13 | Limitations documented | MET | -- | `FINAL-REPORT.md` section 9 has all six sub-headings (269-317) |

**(b) Sources.** `CAMPAIGN-STATE.md` 318-336, 395-398; `FINAL-REPORT.md` 267-342; `CHARTER.md` 635-675; files named in the last column.

**(c) Verdict: RECONSTRUCTED.** The only gap is a residual for condition 11 the record does not list; the status of every condition was otherwise reconstructable and checkable.

---

## Q3. What remains open, and who owns each item

Owner vocabulary: **agent** = a successor coding-agent context acting as dispatcher (the record's section 7 C2 role: pushes, PR state, record updates); **owner** = repository owner; **deferred** = deferred by a recorded decision, no action until a stated trigger.

| Item | Owner | Basis |
|---|---|---|
| Audit this probe; append the result to section 16; correct `FINAL-REPORT.md` only for proven factual errors; mark PR #268 ready for review | agent (dispatcher) | record 238-241, 249-251 (R8 stop condition not yet met at `5a53273`) |
| Refresh the PR #268 body -- it still describes R0-R2 ("Docs-only so far", "R2 in progress") | agent (dispatcher) | `gh pr view 268 --json body`; record C2 |
| Stale entries inside the record found by this probe (Q5 items 1, 3, 4, 5) | agent (dispatcher; record edits are dispatcher-owned) | record RULE line 15-18 |
| Merge authority for PR #268 | **owner** (decision 1) | record 276-278; `FINAL-REPORT.md` 302-303 |
| Whether to note the substrate observation on Issue #255 | **owner** (decision 2) | record 279-281; Issue #255 is OPEN (`gh issue view`) |
| Nine registry/overlay/documentation items in `docs/workflow-system-disposition.md` section 6 | **owner** (decision 3; overlay is owner-ratified under ADR 0027) | disposition doc 271-318; record 282-288 |
| D19 one-line test expectation (`tests/test_validator_utils.py:69`) | agent under ordinary repo discipline after closure, via a normal PR the owner merges; the record calls it a "small separate decision (same class as U8)" -- narrow ambiguity whether that decision is the owner's or the dispatcher's | record 314; R7 report 350-355; `FINAL-REPORT.md` 281-283, 317 |
| D2b / U8 `tests/test_validate_brief_json.py` refresh-vs-retire | deferred (needs a fixture/validator-semantics decision; owner or dispatcher) | record 196, 297; `FINAL-REPORT.md` 279-280 |
| `docs/agent-native-operating-workflow.md:396-398` stale "untested" sentence | agent (docs-only, reversible, non-ratified); not in R8's grant ("new product changes" not authorized, record 246-248) so post-closure | Q5 item 2 |
| Carrying the campaign's trial-log rows and map MECH refreshes to `main` if PR #268 is not merged | agent (mechanical bookkeeping the trial protocol permits), owner merges | Q5 item 3; `docs/semantic-control-map-trial.md` |
| Semantic-control-map trial closure (min 2026-09-28, max 2026-10-26) | deferred by schedule; closure judgment is the owner's (`CORE_PERSISTENCE_RATIFIED`) | trial log 7-11; trial doc 112-120; record C3 |
| Goal A external validation (Issue #255, OPEN) | deferred; owner / environment | record 99, C4 |
| Research lanes C6R (#226 OPEN), normal-use lane (#218 OPEN) | deferred; non-ratified research | record 98 |
| D3-D9, D11, D13-D18 | deferred by classification (HISTORICAL_ONLY / NO_ACTION / environment / owner decision 3) | record 294-315 |
| Cross-run prior-report identity | deferred (`CONVENTION_CLOSED`, deliberately untested) | operating map 471; `FINAL-REPORT.md` 272-273 |
| Unvalidated hypotheses (multi-dispatcher scale; reopen conditions; substrate transfer) | deferred until a real case | `FINAL-REPORT.md` 291-299 |

**(b) Sources.** As cited per row.

**(c) Verdict: RECONSTRUCTED.** Ownership of every item is stated or directly inferable; the one narrow ambiguity (who decides D19/D2b) does not change what a successor would do first.

---

## Q4. What a successor context should do first

**(a) If the owner merges PR #268.**

1. Confirm the integrated state, not the PR state: `git log --first-parent main` shows the merge; `gh run list --branch main` green at the merge commit. Then treat `CAMPAIGN-STATE.md` as a closed historical record (its own STATUS block says CLOSING; section 16 says CAMPAIGN_COMPLETE) -- do not reopen it for new work; new work follows ordinary repository discipline (`AGENTS.md`, `CLAUDE.md`, ADR governance), not `campaign(Rn):` commits.
2. Check the semantic-control-map trial for triggers fired by the merge itself: the merge changes `docs/agent-native-operating-workflow.md`, `docs/decision-orchestration-boundary.md`, `CLAUDE.md`, `.claude/hooks/sessionstart.md`, and `scripts/_validator_utils.py`; any map row citing those files is a MECH-refresh candidate; log it in the trial log (record C3; trial doc sections A-B). Do not manufacture a consultation.
3. Take the smallest bounded, reversible item first: D19 (`tests/test_validator_utils.py:69`, add `"liveness": "active"` to the expected dict, or assert on the id only), as its own PR with the targeted test run under both code pages. Then the operating-map sentence at lines 396-398 (docs-only reconciliation). Then D2b/U8 only after the refresh-vs-retire decision is taken.
4. The nine disposition items and the Issue #255 note wait for explicit owner decisions (2 and 3); do not edit overlays or registries on the strength of the disposition doc (its own status block: "CHANGES: nothing").
5. Remove the `smk-campaign` worktree once nothing else needs it (record C6); the branch can be deleted only if the owner wants it gone (the reports are in the merged tree).

**(b) If the owner does not merge.**

1. Do nothing to the branch's product files: it is a *qualified head* (`5a53273` / product head `1b47d06`); rebasing or adding commits voids the exact-head qualification the report claims, and R8 forbade new product changes. The branch and PR remain the durable evidence (record 406-408).
2. Recognize what does **not** reach `main` in this case, which the record understates (Q5 item 3): the five 2026-09-02 trial-log events, the six MECH-refreshed map rows, the enforcement-contract addendum, and the two R4 test repairs plus the R7 resolver. Decide (or ask the owner) whether to carry the trial bookkeeping -- mechanical, protocol-permitted -- to `main` in a separate small PR so the trial closes with its real events; the product-doc changes and the script repair would each need their own owner-merged PR if they are wanted.
3. Record the non-merge in the record's section 15 / section 16 (dispatcher-owned) so the next reader does not assume integration; refresh the stale PR body regardless, since it currently misdescribes the branch as docs-only.
4. As `main` moves, the like-for-like baseline (`f10b7da`) ages; do not re-qualify unless the owner signals interest in merging.
5. Post-closure work that does not depend on the branch (D19, D2b decision, the nine owner items, the trial close on 2026-09-28+) proceeds from `main` exactly as in (a) steps 3-4.

**(b) Sources.** `CAMPAIGN-STATE.md` 171-181, 216-252, 273-288, 368-378, 400-409; `FINAL-REPORT.md` 197-199, 301-317; `docs/semantic-control-map-trial.md` 100-120; `docs/semantic-control-map-trial-log.md` 1-42 on HEAD vs `git show main:docs/semantic-control-map-trial-log.md`; `gh pr view 268`.

**(c) Verdict: PARTIAL.** (d) The record's successor guidance (lines 404-409) covers (a) adequately but (b) in one clause -- "the branch remains a qualified, reversible candidate" -- and then asserts "either way" the trial closes with the campaign's events, which is false for the not-merged branch. What is missing is durable: a statement of which campaign-produced bookkeeping lives only on the branch and what to do with it if the PR is declined, and who acts as dispatcher after the closing conversation ends (section 7 C2 defines the role by conversation, not by hand-over). Class: **MISSING_DURABLE_STATE**, with a secondary, narrow AUTHORITY_AMBIGUITY (dispatcher succession). Steps (b) 2-3 above are my reconstruction from the repository, not from the record.

---

## Q5. Claims contradicted by the repository (up to five), then claims verified true

**Contradicted or internally inconsistent** (ordered by materiality; none changes the disposition):

1. **Record section 11, owner decision 1 (`CAMPAIGN-STATE.md:277-278`)**: "docs + two test-file repairs; no ADR, contract, registry, overlay, **script**, or `src/` change." Contradicted by `git diff --name-status main...HEAD`: `M scripts/_validator_utils.py` (commit `79e02c5`, +33/-4) and three test files (`M tests/test_integration_external_repo.py`, `M tests/test_path_drift.py`, `A tests/test_validator_utils_liveness_import.py`). `FINAL-REPORT.md:302-303` states it correctly ("documentation, one script, three test files"). Same section, item 2 (`:280-281`) says the substrate observation held "six times" while section 5 (`:145`) says "seven times (R1-R7)". Both are pre-R7 text left unrevised at v9/v10.

2. **Product surface `docs/agent-native-operating-workflow.md:396-398`**: "Observed limitation: documentation-level responsibilities only. Implementation-class continuation (code + tests + CI) from durable state is untested (campaign record U7)." Contradicted by the campaign's own evidence in the same tree: record U7 "RESOLVED (R4, R7)" (`CAMPAIGN-STATE.md:195`), G13 CLOSED (`:165`), commits `769a180` (R4) and `79e02c5` (R7) authored by fresh contexts, CI green on those heads. The subsection itself covers only R1/R2 ("Two fresh contexts", line 331), while the Reality-map row at line 474 was later updated to "R1-R4". `FINAL-REPORT.md:45-46` ("The product surface now states what was demonstrated") is therefore overstated for this sentence, and the residual list for condition 11 (`CAMPAIGN-STATE.md:332`; `FINAL-REPORT.md:278-289`) omits it. Docs-only and reversible; R8 correctly did not touch it.

3. **Record successor guidance (`CAMPAIGN-STATE.md:408-409`)**: "Either way, the semantic-control-map trial closes on its own schedule (min 2026-09-28) with the events this campaign logged." The events exist only on the branch: `git show main:docs/semantic-control-map-trial-log.md | grep -c 2026-09-02` = 0, versus 5 on HEAD; the six MECH-refreshed map rows (`docs/semantic-control-map.md:50-61`) likewise. "Either way" holds only if PR #268 is merged or the bookkeeping is carried over separately.

4. **The "twenty-one" record-error count (`CAMPAIGN-STATE.md:144`; `FINAL-REPORT.md:39-40`, `:257`)** is not reproducible from the record's own enumeration: the sub-counts it gives (`:18` and `:144`: R2 1, R3 2, R4 2, R5 3, R6 9, R7 5) sum to 22; G10 (`:162`) says 16 through R6 whereas those sub-counts through R6 sum to 17; the reports' own lists differ again (R4 flags F1-F5 at `R4-implementation-continuation.md:273-295`, not 2; R6 lists F1-F8 plus discrepancies I1-I9 at `R6-workflow-system-disposition.md:74-197`). The qualitative claim -- many present-but-wrong facts, all caught by in-spec verification -- is supported by every report I opened; the exact figure is a dispatcher tally with an off-by-one somewhere.

5. **D14 (`CAMPAIGN-STATE.md:309`)** still reads "Campaign head after R7 expected: 52 failed / 1 error ... R8a verifies", while R8a measured 51 failed / 1 error (`:109-110`, `:388-390`; commit message of `5a53273`). The row was not reconciled after measurement. The R7 report's F2 correction to "52" (`R7-machinery-continuation.md:46-48`, `:175`) was itself off by one for the reason R7 gave in its own caveat (`:176-180`: the baseline already counted D19 as a failure, so D19 does not add to the count). Related pre-R7 leftovers: section 13 header "Status after R6" (`:320`) and row 4 "five responsibility classes | R1-R6" (`:325`) versus row 5 and `FINAL-REPORT.md:34-37` ("six").

**GitHub-side, not a repository contradiction**: the PR #268 body (`gh pr view 268 --json body`) still says "R2 ... in progress" and "Docs-only so far"; the record only claims the PR exists and is a draft (`:373`), which is true (`isDraft: true`, `state: OPEN`, 22 commits, head `5a53273`). A reviewer landing on the PR would be misinformed until the dispatcher refreshes it.

**Verified true -- what a skeptic would check first:**

- HEAD `5a53273` == PR #268 `headRefOid`; base `main`; merge-base `f10b7da`; 22 commits; branch clean before and after this probe.
- Exact-head CI: `b4335c3 2adfeaf 09bdf5e ac47191 e35ead1 89246f4 5a89f2a eb6c461 e702b31 1b47d06 4336a53` all `completed/success` (matches section 15 exactly), and `5a53273` `completed/success` (finished during this probe; the record could not have recorded it). `main` green at `f10b7da`.
- "13 jobs" (`CAMPAIGN-STATE.md:96`) and "19 jobs" (`FINAL-REPORT.md:192`) are both true: `validation.yml` defines 13 jobs; run 33598950879 (`4336a53`) executed 19 matrix instances (Python 3.11/3.12 expansions), all success.
- Diff scope: 23 files; nothing under `src/`, `docs/adr/`, `skills/`, `.github/`; `grep -rn CAMPAIGN-STATE scripts/ src/ tests/ .github/` = 0 hits ("READS: nothing", `:11`).
- Per-commit stats: `79e02c5` +33/-4 script and +149 test; `13d1a09` +213/-83 (boundary +108, `CLAUDE.md` +5, hook doc +98/-83 = 181 lines); `70648c4` +410; `6ff4a89` +88/-3; `769a180` 5 lines across two test files (three `encoding="utf-8"` additions; two import lines); `4b42263` dated 2026-09-01 introduced the hard import (+40/-5).
- `python scripts/validate-repo.py` on `5a53273`: exit 0, "Validation passed!"; `git status` clean afterwards.
- `scripts/_validator_utils.py:14-42`: `_WORKFLOW_LIVENESS` cache and `_workflow_liveness()` (sys.path import, then sibling file, else `ImportError`); three call sites at 140/154/167. `tests/test_validator_utils_liveness_import.py`: 149 lines, ASCII, LF, three tests at lines 115/121/131.
- D19 as described: `tests/test_validator_utils.py:67-69` writes `workflows:\n  - id: test\n` and asserts `{"workflows": [{"id": "test"}]}`.
- Pass-count arithmetic 2712 -> 2723 (+11) reconciles: `tests/test_integration_external_repo.py` has 5 tests (un-hidden by D2a), +1 D1, +2 mode-coverage (`test_mode_coverage_aggregation.py` has 7 tests, 2 were red), +3 new.
- `docs/workflow-system-disposition.md`: status block "CHANGES: nothing"; 23 rows = 1 KEEP / 0 REPAIR / 2 DEMOTE / 2 RETIRE_CANDIDATE / 8 HISTORICAL / 10 INSUFFICIENT_EVIDENCE; nine owner decisions (lines 276-318). Pointer in the operating map at line 51.
- `.claude/settings.json` is `{}`; hook doc frontmatter carries the `note:`; `CLAUDE.md` gained exactly the five lines the report describes.
- Trial: `trial_start_date = 2026-08-31`, `minimum_close_date = 2026-09-28`, `status = OPEN` (trial log 7-11); protocol minimum 4 weeks (trial doc 115).
- Issues #255, #218, #226 are OPEN (`gh issue view`), consistent with rows 97-99.
- `FINAL-REPORT.md` and `CAMPAIGN-STATE.md` are ASCII with LF (0 bytes > 127, 0 CRLF).

**Not verified (limitations of this probe):** the like-for-like Windows suite numbers and `test-validators.py` 78/78 (no pytest run: not in my permitted tool list, and R7 lines 159-160 record that test runs dirty the tracked `src/sensemaking_skills.egg-info/*` files); ADR 0013/0014/0026/0027 contents (not opened); R2-R6 reports read via targeted greps, not in full; `validate-plan.py` fail-closed behavior (not run).

**(c) Verdict: RECONSTRUCTED.**

---

## Reconstruction cost

- **Files opened (whole or in part): 26.** `CAMPAIGN-STATE.md`; `FINAL-REPORT.md`; `CHARTER.md`; `R7-machinery-continuation.md` (full); `R1-fresh-context-reconstruction.md` (1-75, 172-173); `R2`, `R3`, `R4`, `R5`, `R6` reports (grep for flag items and cost lines only); `scripts/_validator_utils.py` (1-90 + grep); `tests/test_validator_utils_liveness_import.py` (1-60 + test names); `tests/test_validator_utils.py` (64-76); `tests/test_integration_external_repo.py`, `tests/test_path_drift.py`, `tests/test_mode_coverage_aggregation.py` (test counts only); `.github/workflows/validation.yml` (job keys, line 14); `docs/workflow-system-disposition.md` (1-40, headings, section 6, row counts); `docs/agent-native-operating-workflow.md` (51, 324-340, 384-400, 471-474); `docs/decision-orchestration-boundary.md` (headings); `docs/semantic-control-map-trial.md` (100-120); `docs/semantic-control-map-trial-log.md` (HEAD full, `main` version grep); `docs/semantic-control-map.md` (grep); `.claude/hooks/sessionstart.md` (1-15); `CLAUDE.md` (diff vs `main`); `.claude/settings.json`. Plus git objects (`git show --stat` on 11 commits, `git log`, `git diff main...HEAD`) and four read-only `gh` queries (PR #268 metadata + body; run lists for both branches; one run's job list; three issues).
- **Tool calls: 28** (1 Read of the record; 24 Bash calls, most batching several commands; 1 Write; 1 byte-verification; 1 commit). Roughly: Q1 needed the record + report + charter + git/gh state (7 calls); Q2 the product-surface greps (3); Q3/Q4 the trial files and PR body (already loaded, +1); Q5 the per-commit stats, resolver, D19, flag-count greps, and the `main`-side trial log (5).
- **Three most load-bearing files:** `CAMPAIGN-STATE.md` (every question starts and mostly ends there; its section 15 and 16 are what make Q1 checkable); `FINAL-REPORT.md` (the disposition argument, the qualification table, and the correct file inventory that exposed the record's stale section 11); `R7-machinery-continuation.md` (the only place that explains why the local failure counts moved the way they did, and the D19 reasoning behind Q5 item 5).
- **Dead ends:** (1) trying to reproduce "twenty-one" from the reports -- the reports' flag lists do not map onto the record's sub-counts (about three calls); (2) the 13-vs-19 CI "jobs" figures looked like a contradiction until `gh run view` showed matrix expansion; (3) grep patterns for R5's flags missed because its flags live in a table, not bullets; (4) a targeted pytest run was considered and rejected (rules; tracked egg-info files that test runs modify), so the like-for-like numbers stay dispatcher-attested with CI as the proxy.
