<!-- Verbatim report of the Phase C evaluator: a fresh-context, read-only child subagent of the Phase A session, written 2026-11-10 from the raw session transcripts (not committed), Git and GitHub. Citations A:n and B:n are 0-based lines of the exported transcript.jsonl of each phase. Not edited except for this comment. -->

# Phase C evaluation: Frontier Challenge 04 (semantic continuity)

## 0. Evaluator status and method

**This evaluator is not fully separate from the participant.** It is a fresh-context child subagent of the Phase A session itself. Its scratchpad lives under Phase A's CLI session `0587b931`, and `phaseA-export/local-session-state.json` shows Phase A with a tool call in flight. It runs on the same model, and Phase A wrote its prompt. Before launching it, Phase A ran its own checks (A:1058-1163). I checked everything below against the raw JSONL, Git and GitHub.

Citations: `A:n` / `B:n` is a 0-based line in that phase's `transcript.jsonl` (times are UTC). `K7e`/`K71` is a line of `.sensemaking/knowledge/architecture.json` at `7e5bff39`/`71746bd4`. `S71:n` is a line of `setup_skills.py` at `71746bd4`.

Hands-on checks:
- I ran PR #799 from a temporary worktree of `71746bd4` (now removed) against scratch roots only.
- I recomputed the frozen-API digests.
- I read branch protection (GET only).

I ran no unit tests.

## 1. Phase A: what actually happened

**Timeline (A:36-1023, 04:44:00-05:13:57)**
1. Loaded `using-sensemaking` (A:38), made a worktree at `53b667c1` (A:76) and built a 724-claim index (A:164).
2. Dry-ran the real `~/.claude/skills` (A:200-201): 24 divergent, 4 missing, 24 current.
3. Picked the "installer cannot tell outdated from edited" problem at 04:50:10, after about 6 minutes of orientation. Its thinking is redacted, so any comparison of candidates is not visible.
4. "Design settled" at 04:52:44 (A:352), then implementation and real-CLI probes on scratch roots (A:441-484).
5. Opened PR #798 and started a fresh-context reviewer subagent at 05:00:09 (A:606).
6. Merged `7e5bff39` at 05:13:14, after 9/9 hosted checks were green (A:982, A:990).

**Errors and rework**
- **Frozen public API broken.** It added three names to `setup_skills.__all__` and keyword parameters to `copy_skill`. Hosted run 42759558168 failed on `003c179e` (verified: `failure`). The reviewer found the same blocker. Fixed in `db6f0513` (A:713-805).
- **Reviewer findings fixed in `2386cf3d`** (A:853-891):
  - the fixed `.tmp` name could be redirected by a planted link;
  - a junctioned Skill was classified `outdated` and then failed in `rmtree`;
  - refusal counts were wrong;
  - one doc line was stale.
- **CRLF accident.** A Python rewrite turned `INSTALLATION.md` (`text: unset`, byte-pinned) and `architecture.json` into CRLF files. Phase A caught this itself with `git diff --check` and fixed it (A:909-941).
- **Uncorrected factual error.** The PR #798 body says the dry run "reported 27 of 52 Skills as diverged". Its own output (A:201) shows 24 divergent. Phase B's identical dry run (B:83) also shows 24, with the same set. Nobody corrected the figure; it lives only in PR text.

**Retained knowledge (diff `53b667c1..7e5bff39`)**

| Item | Original basis | Correct at `7e5bff39`? |
|---|---|---|
| REVISE `component:distribution-setup` (K7e:881) | code | Yes. It is pinned "At db6f0513", an intermediate commit, not the merge head; `2386cf3d` later changed link handling. |
| ADD `decision:install-record-classifies-divergent-skill-copies` (K7e:901) | delegated design, real-CLI probes | Yes: `replace_allowed = force or (update and state == "outdated")` (7e5bff39 L384). `known_limits` overstates the `--sync` case. A synced copy that equals the packaged tree is `current` and gets re-recorded; it reads `changed` only after the source moves past it. |
| ADD `rule:frozen-public-python-api` (K7e:923) | CI failure plus `docs/public-api-v1.0.yaml:1-15` and `tests/test_public_api_contract.py:22-52` | Yes. Its `applies_to` globs are wider than the frozen `__all__` surface, which errs on the safe side. |
| ADD `verification:public-api-contract-test` (K7e:948) | test source plus the CI run | Yes |
| ADD `alternative:per-skill-install-marker` (rejected, K7e:963) | fingerprint covers every file | Yes |
| ADD `alternative:replace-outdated-skill-copies-by-default` (deferred, K7e:979) | documented fail-closed default | Yes |

Two consequential items were never recorded and exist only in the PR #798 body:
- the observation that this host's unrecorded root is still refused by `--update`;
- the rejected "catalogue of historical packaged fingerprints … does not cover source checkouts" alternative.

## 2. How Phase B was started and briefed

**Instantiation.** Phase A called `start_session` at 05:13:47 (A:1009) with these arguments: `context: "fresh"`, `initiation: "user_asked"`, source branch `base/origin-main-7e5bff39`.
- Phase B's first message (B:4) is only the background and the brief; no Phase A conversation was forked in.
- It is a separate top-level CLI session (`957e2b45`) with its own transcript and worktree. Its metadata has `spawnedFrom.sideSession: true`.
- It shares with Phase A: the model (`claude-opus-5-5`, effort `xhigh`), `bypassPermissions`, app 2.1.317, the Windows account, `gh` auth and the auto-memory index.

So it is independently instantiated with fresh context. It was not independently commissioned.

**Brief.** It names no retained claim and does not mention PR #798, install records, `--update`, Git history or knowledge records. But Phase A wrote it after verifying that its own `--update` leaves this host's unrecorded root unserved (PR #798 "Verification: Unrecorded"), and the brief asks for exactly that gap ("bring stale installed copies up to date safely … Find out what the current product already does"). There is no answer leakage. The task is real friction (24 stale copies, including the entrypoint), but Phase A chose it to sit next to its own work: a selection confound.

**Other channels**

| Channel | Finding |
|---|---|
| Memory `MEMORY.md` | Last written 04:30:32Z, before Phase A began (04:44Z). The copy Phase B loaded (B:16) contains no "798", "799" or "install record". |
| Memory `local-cli-skill-staleness.md` | Changed at 05:41:20Z by Phase B's own edit (B:580), after it had merged. This is outbound contamination of future sessions, not inbound leakage. |
| Side-session notes | Empty when Phase B listed it (B:36-37, "total 0"). Phase B wrote a note at 05:41:25 (B:582). The folder no longer exists. |
| Worktree name | `cross-session-fresh-b-0f261e` was reused from an earlier experiment; it already appears in Phase A's worktree list (A:54). It is a framing cue, not content; Phase B named its note `fresh-b-…`. |
| Transcripts and scratchpads | No session-management tools were used, and no reference to `0587b931` or Phase A's scratchpad appears in Phase B's transcript. |
| Installed Skills | These predate Phase A, and Phase B invoked no Skill. |

**Conclusion: Phase A information reached Phase B only through Git, the code and GitHub PR text.**

## 3. Discovery and use by Phase B

| Time | Event |
|---|---|
| 05:14:19 (21 s in) | `git log --oneline -15 && gh pr view 798` (B:47). PR #798 is simply the HEAD merge. |
| 05:14:36-43 | Reads the rest of the PR body (B:51) and all of `setup_skills.py` (B:60), which holds Phase A's frozen-API comment (7e5bff39 L76-77) and the record's meaning ("last wrote or verified … copies written by any other tool are not recorded", L30-35). |
| 05:14:52 | "check whether those copies match past packaged versions in Git history" (B:77). **Direction set before any record was opened.** |
| 05:15-05:27 | Scripts find 13 exact matches; usage limit at 05:16:22; then 10 CRLF-only matches and 1 nested directory (B:90-135). This CRLF finding was Phase B's own and changed its design. |
| 05:28:53 | "23 of 24 identical to committed versions … loses nothing" (B:139). |
| 05:30:01 | **First read of knowledge records**: a Python filter on the record IDs that the PR body names (B:174-179). |
| 05:30:07-27 | Decision stated; full implementation in one edit (B:189). |
| 05:31:10-21 | Makes the constant private and checks the manifest and the contract test (B:227-240). |
| 05:36:55 | First display of the `rule:frozen…` record, while reconciling (B:420). |
| 05:39:44-05:40:11 | `knowledge-build` plus `context-for`, only to confirm that its *own* records can be retrieved (B:524-537). |

Phase B never used the Steward's RECALL or `knowledge-query` before deciding.

**What each retained item did in Phase B**

| Item | What it did |
|---|---|
| `decision:install-record…` | Read about 6 s before the decision was stated, but after the direction and feasibility were settled. Its constraint (the record vouches only for trees `setup-skills` wrote) was already in the code docstring and the PR body. **Confirmed; no demonstrated change.** Used as the link target for Phase B's decision. |
| `component:distribution-setup` | A reconciliation target, which Phase B correctly revised. |
| `rule:frozen-public-python-api` | **Constrained a decision** (keep new helpers private). The lesson reached Phase B through the code comment and PR text 16 minutes before the record was displayed. Phase B **verified the original evidence** (manifest and test). |
| The two alternative records, `verification:…` | Read; no observable effect. The per-skill marker is irrelevant here. |
| PR-only items | The **clearest influence**. PR #799 quotes #798's unrecorded-root observation and addresses the rejected fingerprint-catalogue alternative ("Git history covers the checkout case at run time"). |

**Stale or corrected items**
- Phase B left the Phase A decision's statement unchanged: "--update replaces only outdated copies; … unrecorded copies still need --force" (K71:940). That is no longer true of the product at `71746bd4`. PR #799 argues that it is "still true for what it decided", and a `references` relation links the two decisions.
- Phase B did not catch "27 of 52".
- It repeated the `--sync` simplification as an open follow-up and in memory.
- Phase B's final report credits "PR #798's body **and its knowledge records**" with ruling out backfill. The timing does not support crediting the records.

## 4. Phase B's engineering outcome (PR #799, `71746bd4`)

**Design.** From a Git checkout, an unrecorded divergent copy whose locally computed Git tree id equals a committed `skills/<name>` tree, either byte for byte or after CRLF->LF, is classified `historical`, and `--update` replaces it (S71:340-473, 496-517).

**My exercise** on a scratch root seeded from Git:

| Seeded copy | Result |
|---|---|
| `using-sensemaking` @`015f991a` | `historical`, replaced |
| `handoff` @`4a3c695a` converted to CRLF | `historical`, "apart from CRLF line endings", replaced |
| hand-edited `repo-sensemaker` | refused, preserved byte for byte |

- The record shows 49 `installed` and 2 `replaced`. A rerun left the record byte-identical.
- A dry run on an empty root created nothing.
- The digests for all 4 frozen modules match the manifest.

**Concerns (none is a safety defect).**
- With only `historical` refusals, the summary still says "Use --force to deliberately replace them" (S71:1014-1016).
- The history lookup (about 0.5 s per unrecorded copy) runs on every checkout run, including plain, `--force` and dry runs (S71:888, 925).
- `git log -- path` history simplification and the forced mode 100644 can only cause false negatives.
- Classification and `rmtree` are not atomic (inherited and disclosed).
- `changed` copies that equal a commit still need `--force` (disclosed).

**Verification honesty: accurate.** The real root was only listed and dry-run; every write went to scratch copies (B:287-330). Neither phase ran `pytest`, and both said NOT_RUN. The PR-body numbers were rechecked before the PR was opened (B:475-483).

**Merged under a pending check.** Merged at 05:40:43Z with "Full test suite" pending; that check finished SUCCESS at 05:41:15Z. `main` is unprotected (protection API 404, no rulesets), CLAUDE.md allows this, and Phase B disclosed it. Post-merge Product Validation 42763624798 passed.

**Manual interventions**
- Phase B hit its usage limit at 05:16:22 (B:97). The owner typed "Tente novamente" at 05:25:58 (B:100), roughly 9.6 minutes later. Because the limit message said it would reset at 05:40 local time, the resumption implies an owner-side quota action (inferred).
- Phase A: "the credits are refreshed. Please continue" at 06:20:35 (A:1029).
- Both processes ended at 05:44:20Z (cost-state).

## 5. Resources

| | Phase A build (04:44:00-05:13:57) | A reviewer subagent | Phase B (05:13:58-05:41:57) |
|---|---|---|---|
| Wall time | 30 min | 7.4 min (in parallel) | 28 min (about 18.5 active) |
| Tool calls | 159 | 37 | 98 |
| API turns | 131 | 37 | 74 |
| Output tokens | 118,826 | 35,229 | 71,311 (27,574 thinking) |
| Cache read / create | 31.2M / 0.31M | 4.19M / 0.15M | 12.35M / 0.21M |
| Cost (cost-state) | $12.56 (A plus reviewer) | — | $5.17 |

- Token counts are deduplicated by message id. The A-plus-reviewer output (154,055) matches the cost-state exactly.
- Phase A's own tally of Phase B (A:1110: 215,261 output tokens) double-counts.
- Phase A's later evaluation prep (06:20+): 17 tool calls, 12.1k output tokens.

## 6. Verdict

**Strongest claim the evidence supports.** A separately started, fresh-context Claude Code session on the same model and host, briefed by the Phase A agent:
- found Phase A's merged work through ordinary Git and GitHub within 21 s;
- read the reviewed records directly before its first code edit;
- checked the original source for the one constraint it relied on;
- built a correct, useful extension that closed the gap Phase A had left (23 of 24 stale copies on this host now refreshable safely);
- reconciled the knowledge records consistently, extending and linking them without contradiction.

**Not supported**

| Owner's distinction | Finding |
|---|---|
| Retrieval vs. use | Records were retrieved and used as reconciliation targets. The product's retrieval path was used only after the fact. |
| Use vs. decision benefit | **No Phase B decision is shown to have changed because of a knowledge record.** The one constraint that mattered (the frozen API) and the gap definition reached Phase B through the code comment and PR text, before the records. |
| Source validity vs. semantic correctness | The records were valid and mostly correct, with minor imprecision (`--sync`, intermediate-commit pins). After #799 one decision statement is stale and was left unrevised. A false figure in the PR text survived both phases. |
| Coding success vs. continuity | The coding task succeeded. Continuity was shown through Git artifacts, not through the knowledge mechanism. |
| Independent instance vs. child subagent | Phase B was an independent instance with fresh context. The Phase A reviewer and this evaluator are fresh-context child subagents. |
| Usefulness vs. causal superiority | The PR is useful. **No matched source-only comparison was performed.** A source-only agent would have seen the same HEAD merge, PR body and code comment, so no causal advantage of the retained records can be claimed. |

**Confounds.**
- Phase A chose the Phase B task to sit on its own gap.
- Both phases used the same model family and effort.
- Phase A's merge was HEAD, so it was found by recency.
- PR text, code comments and records all carried the same facts.
- The owner intervened once in each phase.
- Phase B wrote to the shared memory folder, which affects future sessions.
- This evaluator is a child of the participant.
- n = 1.

**Result: continuity of engineering context is POSITIVE (observational). Decision benefit from the reviewed knowledge records is NOT DEMONSTRATED. Causal superiority was NOT TESTED.**
