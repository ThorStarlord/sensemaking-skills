# Operator admission report (Frontier P4, 2026-11-10)

This is the report of the task-admission operator, preserved as it was
returned. The operator was a fresh-context subagent that the planner's session
started; it was not told what the planner would pick. Its independence is
context-level only. Host-reported usage: 144,201 tokens, 41 tool calls, 470 s.

---

1. **OPERATOR IDENTITY**: I ran as `claude-opus-5-5`, read-only. The checkout was not modified: the only untracked file, `.sensemaking/receipts/2026-11-10-frontier-p4-adaptive-multi-agent.session.yaml`, was already there and was written by another session. All builds, a `git clone` and a scratch target repo went to a scratch directory outside the checkout. One `knowledge-build --temporary-checkout` call created and then removed a temporary worktree. No unit tests were run.

2. **VERDICT**: `ADMITTED`. It sits at the lower edge of criterion 4 (substantial).

3. **ADMITTED OUTCOME**: Three commands that pin source to a commit (`knowledge-orient`, `knowledge-audit`, `knowledge-check-rules`) can be used on committed revisions while the checkout has uncommitted or untracked files. Today those files include the product's own required session receipts. The users are a coding agent mid-session, who needs audit and rule checking for RECONCILE, and a target-repository user with any untracked file on a first visit, who needs orient. All three would keep reading only committed bytes and would say plainly that working changes were not read. Nobody would need to hand-make a clean clone or worktree, which is what `knowledge-build` already avoids since commit `4fbf868d`. The guidance that today contradicts itself on this point would also become consistent.

4. **EVIDENCE IT IS GENUINE AND UNRESOLVED**
   1. On the real checkout, `semantic knowledge-audit ... --indexed-ref baaec6b9 --current-ref baaec6b9` and `semantic knowledge-check-rules --repo . --target-ref baaec6b9` both failed with `Error: dirty or untracked worktree: source bytes cannot be pinned`. The only cause is one untracked session receipt.
   2. Scratch target repo (one commit, plus untracked `notes.txt`): orient, check-rules and audit all failed with the same error. `--help | grep -c temporary` returned `0` for each of the three commands.
   3. To run audit and check-rules at all, I had to `git clone` into a temp directory. That is the hand-made clone the existing decision was meant to remove. In the clone, audit ran (442 records) and check-rules ran (10 rules).
   4. The decision `decision:index-from-temporary-worktree` (`.sensemaking/knowledge/stewardship.json` ~l.293) covers only `knowledge-build`, and cites "an untracked session receipt" as its motivation. The code agrees: `semantic_cli.py:143` (orient) and `:176` (check-rules), and `knowledge_store.py:533` (audit), call `verified_tracked_sources` directly. Only build (`semantic_cli.py:113-118`) wraps the call in `temporary_commit_checkout`.
   5. The guidance contradicts itself:
      - `skills/repository-semantic-steward/references/reconciliation.md:10` says "Do not create a clean-room development session", then requires a "naturally clean current HEAD" for audit.
      - `references/bootstrap.md:19` says "use a separate clean worktree".
      - `SKILL.md:100` says orient and audit require a clean checkout.
      - `reconciliation.md:42` requires check-rules "at the new clean HEAD".
   6. The friction recurs: the P2 worker contract (`origin/claude/frontier-p2-record`, `worker-contract-v1.md` ~l.43) says "15.1 s with `--temporary-checkout` (needed whenever the tree is dirty, which is the normal state during work)".
   7. The receipt contract (`skills/using-sensemaking/references/session-receipt-v1.md:7,96`) requires a receipt in every session, committed only with the last commit. So every session's checkout is dirty in the middle.
   8. No open PR covers this. PR #801 adds only `workspace-query` and "`knowledge-query` is unchanged" (its body). PRs #795, #796 and #797 touch `context-for` and receipts, not these three commands.

5. **WHY CONSEQUENTIAL**: ADR 0031 and STATUS.md make PATH-1 (RECALL -> BUILD -> RECONCILE) the current construction responsibility. STATUS names the open uncertainty as whether accumulated knowledge is reached and used. RECONCILE's drift checks (audit, check-rules) and first-visit orientation are refused in the normal working state, including on target repos with stray untracked files. The available workarounds are committing early, hand clones or skipping the check, and the record says agents already skip steps because of setup cost.

6. **ACCEPTANCE CONDITIONS**
   1. In this repo, with an untracked receipt present, `knowledge-audit --indexed-ref <older indexed SHA> --current-ref HEAD` succeeds. Its output matches the same audit run in a clean clone, apart from fields that identify the checkout.
   2. In the same dirty state, `knowledge-check-rules --target-ref HEAD` succeeds and gives the same `rule_assessments` and `findings` as the clean-clone run (10 rules; 1 ASSESSED, 1 PARTIALLY_ASSESSED).
   3. In the scratch target repo with untracked `notes.txt`, `knowledge-orient` succeeds and reports the committed file inventory. `notes.txt` does not appear as an indexed or oriented file.
   4. Each of these outputs says plainly that the active worktree had uncommitted or untracked changes that were not read.
   5. Negative: changing a tracked file without committing it leaves its audit fingerprint equal to the committed bytes. Dirty bytes are never hashed (the rejected `alternative:dirty-tree-byte-audit` still holds).
   6. Negative: the active checkout's `git status --porcelain` and its `git worktree list` are the same before and after each command. No temporary worktree or file is left behind, including after a failure.
   7. Negative: a `--target-ref` that is not a 40-character SHA of an existing commit is still refused. A commit that assigns an external filter to a tracked path is still refused, as `temporary_commit_checkout` does today.
   8. Negative: a clean checkout behaves exactly as before, with the same output shape and values.
   9. The Steward `SKILL.md`, `bootstrap.md` and `reconciliation.md` no longer contradict one another on clean-checkout requirements, and the `decision:` and `inv:` records are revised to the new scope.

7. **CONSTRAINTS AND AUTHORITY**
   - `inv:index-snapshot-vs-working-overlay`: only committed bytes count as indexed truth.
   - `alternative:dirty-tree-byte-audit`: rejected.
   - The existing build decision says the clean-source check stays unchanged rather than exempting untracked files.
   - Never set `action_authorized` or `semantic_truth_established` to true.
   - Console output stays ASCII.
   - The public Python API is frozen (`tests/test_public_api_contract.py`, `rule:frozen-public-python-api`), so new helpers must stay private.
   - CLI JSON fields are part of the artifact contract.
   - Stay clear of PR #801 (`semantic_cli.py` lines it adds, new `workspace_knowledge.py`, `recall.md`) and #795/#796 (`knowledge_store.py`, `knowledge_architecture.py`). `knowledge_store.py:518-660` overlaps #795/#796 at file level only, and the solution must not depend on their code.
   - Authority: this is ordinary PATH-1 construction under ADRs 0029/0031. It needs no ADR change, no CI or hook change, no schema ratification and no other repository.

8. **DESIGN TENSIONS (UNRESOLVED)**
   - Opt-in flag per command, the same as build, or automatic fallback when the tree is dirty.
   - Temporary worktree (about 15 s on this repo) or reading Git objects directly without a worktree.
   - Orient at the committed HEAD while hiding dirty files, or show working changes next to it without treating them as indexed.
   - Audit: materialize only `current-ref`, or both refs.
   - Refactor into one shared source-resolution path, or keep separate wrappers per command.

9. **CANDIDATES CONSIDERED AND NOT ADMITTED**
   - Audit noise from authored knowledge files flagging every record they contain (127 of 139 "source_changed" records were flagged only because their pack changed): this is intentional and documented, and `authored_record_audit` already separates the cases.
   - Executable checkers for convention-type rules in check-rules: speculative and redundant, since `test_console_output_ascii_only.py` and `test_public_api_contract.py` already enforce them.
   - Thin record coverage for `setup_skills.py`, which changed 569 lines and is cited by one record: knowledge authoring, mostly documentation.
   - Making query zero-setup: PR #801.
   - Decision review across pending changes: failed review in P3, and existing commands already deliver it.
   - A pointer to `.sensemaking/` in target-repo instructions: qualification and owner territory (#552/#554).
   - `setup-skills --update` gaps: none observed in a dry run.
   - `release audit`, `strategy drift`, graph view export: worked correctly.

10. **COVERAGE**: I assessed the semantic CLI (build, query/`context-for`, audit, check-rules, orient, proposal-check, view-export), setup/distribution, receipts (validator over all 63 receipts and the summarizer), release audit, strategy drift, open PRs and issues, and the P2, P3 and F04 records. I did not assess the campaign CLIs in depth, `journey`, `organization`, `analyze`, the workflow and validator scripts beyond receipts, or the viewer in a browser. About 30 commands. I did not run the solution's runtime cost or check the Windows path behaviour of temporary checkouts for audit and orient.
