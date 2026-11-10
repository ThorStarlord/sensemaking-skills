# Worker contract I1 (integration build), v1

You build one integration branch from four reviewed pull requests, with two
conflict resolutions the planner has already decided, then run the planner's
checks and report. You make no design decision. If anything differs from what
this contract expects, stop and report it; that difference is the most useful
thing you can return.

## Where you work

- Worktree (yours alone): `H:/GithubRepositories/sensemaking-skills/.claude/worktrees/frontier-p5-integration`
  on branch `claude/integration-checkout-query-context`, currently at
  `origin/main` (`baaec6b92f87a00dbcefdbf865da04f86d5ce59f`).
- Scratch (outside every checkout): `C:/Users/Admin/AppData/Local/Temp/claude/c52b3a57866998a2/3f8955cd-0fc9-4310-958a-c1184bb925fe/scratchpad/p5`
- Run the CLI from source in Git Bash: `PYTHONPATH=src python -m sensemaking_skills.cli ...`
  (the `sensemaking-skills` on PATH is a stale install).
- You commit the four merges and nothing else. You do not push.
- Repository policy for this phase: do not run `pytest`.

## Step 1: four merges, in this order

Use `git merge --no-ff -m "<message>" <ref>`. End every merge message with a
blank line and `Co-Authored-By: Claude <noreply@anthropic.com>`.

| # | Ref | Message subject | Expected |
| --- | --- | --- | --- |
| 1 | `origin/claude/temporary-checkout-pinned-readers` | `merge: PR 804, temporary checkout for orient, check-rules and audit` | clean |
| 2 | `origin/claude/workspace-knowledge-query` | `merge: PR 801, workspace-query (resolve Steward SKILL.md line 100)` | one conflict, in `skills/repository-semantic-steward/SKILL.md` |
| 3 | `origin/claude/context-for-test-evidence` | `merge: PR 795, verification context for test files in context-for` | clean |
| 4 | `origin/claude/context-for-relevance-candidates` | `merge: PR 796, relevance candidates in context-for (keep both definition blocks)` | one conflict, in `src/sensemaking_skills/semantic_architecture/knowledge_architecture.py` |

**Resolution for merge 2.** The conflict is one long line. Take the incoming
(PR 801) version of that line, the one that begins `` `workspace-query` needs
neither a prior build ``. In it, replace the bold sentence

    **Only orientation/build (and source audit) require a clean checked-out source revision.**

with

    **Orientation, build, rule checks and source audit read a clean checked-out source revision; from a dirty checkout, add `--temporary-checkout`.**

Change nothing else on the line or in the file.

**Resolution for merge 4.** Both sides add top-level definitions at the same
place, after `_context_item`. Keep both blocks whole: first the block from HEAD
(the function `_test_evidence_verifications`), then the incoming block (from
`RELEVANCE_NOTE` through `_disclose_relevance_candidates`). Two blank lines
between top-level definitions and before `def context_for`. Edit nothing else
in the file by hand; Git has already merged the rest.

**Stop and report, without resolving, when** a merge conflicts in any other
file or region, a merge expected to conflict is clean, or a resolution leaves
the file failing `python -m py_compile`.

## Step 2: checks

Run each and record the result.

| Check | Command | PASS when |
| --- | --- | --- |
| K1 | `git merge-base --is-ancestor <ref> HEAD` for the four refs | all four exit 0 |
| K2 | `git grep -n -E "^(<<<<<<<\|>>>>>>>) "` | no output |
| K3 | `git status --porcelain` | no output |
| K4 | `grep -c -F` in `skills/repository-semantic-steward/SKILL.md` for: the new bold sentence; `` `workspace-query` needs neither a prior build ``; `Only orientation/build`; `` `knowledge-query --repo .` ``; `clean checked-out`; `dirty active checkout` | counts 1, 1, 0, at least 1, at least 1, at least 1 |
| K5 | `grep -c -E "^def _test_evidence_verifications\|^def relevance_candidates\|^def _disclose_relevance_candidates\|^RELEVANCE_NOTE" src/sensemaking_skills/semantic_architecture/knowledge_architecture.py` | 4 |
| K6 | `python -m ruff check --select E4,E7,E9,F src/sensemaking_skills/semantic_cli.py src/sensemaking_skills/workspace_knowledge.py src/sensemaking_skills/semantic_architecture/knowledge_architecture.py src/sensemaking_skills/semantic_architecture/knowledge_store.py src/sensemaking_skills/semantic_architecture/knowledge_retrieval.py` | clean |
| K7 | the seven validators: `python scripts/validate-docs-currentness.py --repo-root .`, `python scripts/validate-error-boundaries.py`, `python scripts/validate-product-boundary.py`, `python scripts/validate-skill-hygiene.py`, `python scripts/validate-repo.py`, `python scripts/validate-release-contract.py --repo-root .`, `python scripts/validate-contract-authority.py --repo-root .` | each exits 0 |
| K8 | `python "C:/Users/Admin/AppData/Local/Temp/claude/c52b3a57866998a2/3f8955cd-0fc9-4310-958a-c1184bb925fe/scratchpad/p5/p5_probes.py" . "C:/Users/Admin/AppData/Local/Temp/claude/c52b3a57866998a2/3f8955cd-0fc9-4310-958a-c1184bb925fe/scratchpad/p5/run1"` (takes a few minutes) | it prints a table; copy the whole table into your report |

About K8: the probes are the planner's. Report every row as printed. One row,
`X7 one Git-objects alternative`, is expected to FAIL at this stage, because
two pull requests each recorded that alternative and the planner reconciles
the records in a later step. Fix nothing in response to a probe row.

## Report format (reply with exactly these sections)

```
MODEL: <the exact model id stated in your own system prompt>
MERGES:
<one line per merge: # | clean or conflicted (files) | resolution applied | commit SHA>
HEAD: <git rev-parse HEAD>
CHECKS:
<one line per check K1 to K7: PASS/FAIL | decisive output>
PROBE TABLE:
<the full output of K8, verbatim>
DEVIATIONS FROM CONTRACT: <none, or each with its reason>
OBSERVATIONS: <anything unexpected you saw and did not act on>
OPEN QUESTIONS: <none, or each question>
```
