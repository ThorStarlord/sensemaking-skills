# Bounded independent review report (Frontier P5, 2026-11-10)

This is the report of the bounded reviewer, preserved as it was returned. The
reviewer was a fresh-context subagent given
[reviewer-brief-v1.md](reviewer-brief-v1.md). It reviewed commit `7ae459d4`,
before the repair commit its findings caused. Host-reported usage: 98,949
tokens, 10 tool calls, 56 s.

---

REVIEWER IDENTITY: claude-sonnet-5-5

VERDICT: ACCEPT_WITH_REPAIRS. The reconciliation is mostly honest and matches the merged code. One documentation sentence overclaims, and the observation about `tests/test_semantic_knowledge.py` doesn't belong in a record.

CLAIMS:

1. REPAIR. The fold into `alternative:read-committed-bytes-from-git-objects` kept the cost figure (about 10 s of a 15 to 20 s first call), the line-ending risk and the revisit conditions. It dropped one point: the builder's tracked-file, symlink and filter checks assume a checkout, so an object reader would be more than a swap of the byte source. The deleted record also said that bytes are "inferred, not run". The merged `scope` now says the difference "has since been observed" by `lesson:separate-clone-changes-audited-bytes`. That lesson is about clones with different `core.autocrlf` settings, so it supports the point only indirectly. It does not compare Git-object bytes with checkout bytes. Change: restore the checkout-assumption sentence, and say "observed that checkout bytes vary with Git configuration" rather than "observed the difference". Also check that nothing still cites `alternative:snapshot-from-git-objects`. I found no remaining references, and the one relation was retargeted correctly.
2. SOUND. There are four explicit-identity commands: `knowledge-build`, `orient`, `check-rules` and `audit`, which are the `--temporary-checkout` options in `semantic_cli.py` (lines 143, 188, 224, 497). `_snapshot_for` in `workspace_knowledge.py` (173-182) uses the active checkout only if HEAD equals the sha and the tree is clean. Otherwise it uses `temporary_commit_checkout`. It returns `active_checkout` or `temporary_worktree`, and `build_source` is reported (line 310). The scoped rejection and the new relation are accurate.
3. SOUND on content, a NOTE on process. The statement matches `context_for` and `_test_evidence_verifications`:
   - The route applies only when `owners` is empty.
   - It matches a verification claim by `authority_ref` or by an exact `file:<path>` in `evidence_refs`.
   - Verified components come from `tested_by` edges, and only when the supporting record is displayed.
   - Anchors extend to decisions, constraints and history, but not to contracts or rules.
   - Ownership stays `NOT_ASSESSED`.

   I did not check the `rejected_alternatives` text against the PR note. The record is disclosed as integrator-authored from the PR 795 note, with ADR 0033 not ratified, which is acceptable for a delegated construction record. The owner should still confirm it at merge.
4. REPAIR. The behavior is correct: the capability route needs owner links, so it is empty here, and `excluded` is built from all `buckets`. Two points:
   - The `tests/test_semantic_knowledge.py` observation ("two verification records, two verified components, no candidates, where this change alone listed three") is a point-in-time run result. It belongs in the PR description, not a durable `composition` attribute. Delete that sentence.
   - `excluded` uses the whole bucket, not just the displayed `limit` slice. A verification record hidden by the limit is therefore listed in neither place. It is counted only in the verification omission total. Not wrong, but worth stating.
5. REPAIR. "Only citing records of other kinds are listed here" is too strong. `relevance_candidates` keeps `verification` in `_CANDIDATE_CATEGORY`. It also matches citations with `:line:N` or `#fragment` suffixes through `_evidence_paths`, which `_test_evidence_verifications` (exact `file:path`) does not. A verification claim citing `file:x.py:line:10` therefore appears as a candidate, not under `verification_refs`. Change the sentence to "verification claims that cite the file by exact path". Also note the suffix mismatch, which is a small code inconsistency.
6. SOUND, from the diff and the merge messages. I did not re-diff the conflicts line by line. `recall.md` kept both the 795 sentence and the 796 step 13. The merge commit for 801 resolved `SKILL.md` line 100. I saw no error.

PR 797: Defensible. It is independent of the other four, tied to an open owner decision, and conflicts with `main`.

OTHER FINDINGS:

1. NOTE: In `composition`, "this change alone listed three citation candidates" refers to an unmerged state. It reads as stale after merge, which is another reason to delete it.
2. NOTE: Local checks (hosted CI and `pytest` not run, per the brief). The context-for and `workspace-query` line-ending claims are untested here.

NOT VERIFIED: I ran no tests and executed no CLI queries. I did not check the PR 795 decision note (`gh`) or the full text of the conflict resolutions. I did not compare the `rejected_alternatives` text with the source note, and I did not check the SQLite index.
