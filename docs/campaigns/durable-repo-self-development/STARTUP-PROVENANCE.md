# Campaign 2 startup provenance

```
STATUS:     immutable record of the mandatory campaign preflight and initial
            setup. Non-authoritative campaign instrumentation.
RECORDED BY: Controller A, 2026-09-02.
PURPOSE:    so a fresh controller can confirm the campaign was started from a
            verified baseline with the required capabilities, and can see exactly
            what fresh-controller-instantiation mechanism was planned and why.
```

## Mandatory preflight (owner instruction "Mandatory Campaign Preflight")

| # | Check | Result (2026-09-02) |
|---|---|---|
| 1 | Repository identity | `H:/GithubRepositories/sensemaking-skills` (main worktree); `git rev-parse --show-toplevel` confirms. |
| 2 | Remotes | `origin` = `https://github.com/ThorStarlord/sensemaking-skills.git` (fetch + push). |
| 3 | Current branch (at preflight) | `main` (local, stale HEAD `f10b7da`, 25 commits behind `origin/main`). |
| 4 | Working-tree state (main worktree) | dirty with long-standing untracked experiment/artifact cruft + 2 modified `src/sensemaking_skills.egg-info/*` files. **Not used** — Campaign 2 works in a clean dedicated worktree. |
| 5 | Fetch authoritative remote refs | `git fetch origin --prune` OK. |
| 6 | Exact current `origin/main` | **`06a57d1d182a32684275d343a9248429feedbfe6`** — "Merge pull request #268 from ThorStarlord/campaign/agent-native-self-development". This is the Campaign 2 baseline / base. |
| 7 | PR #268 is an ancestor of the starting state | **YES.** `gh pr view 268` → state MERGED, merge commit `06a57d1...` (mergedAt 2026-09-02T07:29:05Z, mergedBy ThorStarlord). That merge commit **is** `origin/main` HEAD; `git merge-base --is-ancestor 06a57d1 origin/main` holds. |
| 8 | Required Git capabilities | `git 2.51.0.windows.1`; worktree add/branch/commit/push available. |
| 9 | GitHub read capability | `gh auth status` → logged in as `ThorStarlord`, token scopes `gist, read:org, repo, workflow`. `gh pr view` / `gh pr list` / `gh run list` usable. |
| 10 | Push / PR capability | `repo` + `workflow` scopes present → push branch + create/maintain draft PR available. (Merge remains an owner decision regardless.) |
| 11 | Relevant qualification commands | From `.github/workflows/validation.yml` and Campaign 1 `CAMPAIGN-STATE.md` section 2: <br> • `python scripts/validate-repo.py` (Level 1 structural) <br> • `python scripts/test-validators.py` (Level 2/3 validator suite, 78/78 historically) <br> • `python scripts/probe-repo.py --repo-root . --output <tmp>` + `python scripts/validate-probe-report.py <tmp> --repo-root .` + `python scripts/gate_relationship_findings.py --report <tmp>` (probe gate) <br> • `python -m pytest tests/... -q` (many CI-named suites; core-assertions set = `tests/test_repo_probes.py tests/test_probe_report_cli.py tests/test_probe_relationships.py tests/test_skill_distribution_probe.py tests/test_gate_relationship_findings.py tests/test_path_drift.py tests/test_cli.py`) <br> • full local like-for-like: `PYTHONPATH=src python -m pytest tests -q -p no:cacheprovider --ignore=tests/integration --continue-on-collection-errors` in a clean worktree vs the same on a clean base worktree (Campaign 1 "C11"; local Windows/Python baseline carries pre-existing platform reds that are green in Linux CI). <br> • `pip install -e .` regenerates `src/sensemaking_skills.egg-info/` as an install side effect — restore before checking for a dirty tree. |
| 12 | Genuinely fresh controller context can be instantiated | **YES, with recorded isolation limits.** See "Fresh-controller mechanism" below. |
| 13 | Successor can access repo / GitHub / validation tools | **YES.** A `general-purpose` subagent (tools `*`, incl. Bash) on this machine inherits the same `gh` auth and can run git + pytest + validators against the committed handoff worktree/branch. |
| 14 | How the exact successor bootstrap will be recorded | The verbatim `prompt` string passed to the subagent will be committed into `controllers/A-handoff.md` (and `controllers/B-*` for later handoffs) **before** the successor is spawned. |
| 15 | How predecessor semantic control terminates at handoff | After committing `A-handoff.md` and recording the handoff SHA, Controller A performs only the mechanical spawn. Controller A does not choose Task B, summarize its reasoning, rank boundaries, name a subsystem, or redirect B. The subagent's returned report is used **only** for the retrospective A/B comparison **after** B completes its cycle — never to steer B. This is a discipline commitment; see the isolation limitations below for what the environment does and does not enforce. |

**Preflight disposition:** the defining fresh-controller experiment **can** be
executed in this environment (context isolation is real; see below). It is **not**
an `EXTERNAL_BLOCKER`. The known limitation (predecessor process persistence is
not environment-enforced) is recorded as an evidence ceiling (EC-2) and will bound
the succession claim, not block the campaign.

## Fresh-controller mechanism (planned)

**Mechanism.** The `Agent` tool with `subagent_type: "general-purpose"` and
`isolation: "worktree"` (or operating directly in the committed campaign
worktree/branch). The subagent receives only the allowed bootstrap text (owner
instruction "Allowed Bootstrap for Fresh Controller B"): notification that it is
now the active semantic Campaign 2 controller, the path to `CHARTER.md`, the path
to `CAMPAIGN-STATE.md`, access to the committed handoff repository state, and
normal git/GitHub/validation capability. Nothing else.

**Isolation assessment against the owner instruction's 12 fresh-controller
criteria:**

| # | Criterion | Status |
|---|---|---|
| 1 | New model/agent context | MET — fresh context window. (Same model family; Campaign 1 also used same-model fresh contexts. Model-identity sameness is disclosed, not claimed as full independence.) |
| 2 | No inherited conversation transcript | MET (HARNESS-REPORTED) — the `Agent` tool starts the subagent "cold"; it does not receive this session's transcript. |
| 3 | No inherited predecessor private reasoning | MET (HARNESS-REPORTED) — the subagent does not receive this session's private/thinking content. |
| 4 | No automatic summary of predecessor strategic conclusions | MET (CONTROLLER-ASSERTED) — the bootstrap is authored to contain only mechanical locate-durable-state content; no mission, rationale, frontier, gaps, or next task. |
| 5 | Exact bootstrap recorded | MET — committed to `controllers/A-handoff.md` before spawn. |
| 6 | Direct access to handoff repository state | MET — committed branch/worktree at a recorded SHA. |
| 7 | Access to permitted durable sources | MET — the whole repo + GitHub. |
| 8 | Git/GitHub/validation capability | MET — subagent `*` tools incl. Bash; shared `gh` auth. |
| 9 | May reject the predecessor frontier | MET — the bootstrap states a recorded frontier/next task is historical evidence, not a command. |
| 10 | Owns semantic selection of the next task | MET — the bootstrap requires B to independently determine the next task and commit its own checkpoint before implementation. |
| 11 | Predecessor cannot rewrite the successor checkpoint | PARTIAL (CONTROLLER-ASSERTED) — discipline-enforced: once B commits its checkpoint at a SHA, A records that SHA and does not amend it. The environment does not mechanically prevent it. |
| 12 | After relinquishment, predecessor cannot resume campaign direction | PARTIAL / UNVERIFIABLE — A's process persists (the subagent returns a report to A). A commits not to steer B and to relinquish; the environment does not enforce non-resumption. |

**Isolation classification (owner instruction "Handoff Provenance"):**
- Context isolation (no transcript, no private reasoning): **HARNESS-REPORTED**.
- Bootstrap minimality, checkpoint immutability, non-resumption: **CONTROLLER-ASSERTED**.
- Predecessor process non-persistence: **not established** →
  `SUCCESSION_ISOLATION_UNVERIFIED` applies to that dimension. Campaign 2's
  succession conclusion is narrowed accordingly (EC-2).

**Why this still executes the experiment:** the load-bearing content of "fresh
*controller*" — reconstructing mission/authority/state from durable sources
alone, independently reassessing the frontier, and selecting + committing the
next task before any predecessor feedback — is fully testable with this
mechanism. What is not environment-guaranteed is that the predecessor cannot, in
principle, keep acting; that is handled by explicit discipline and disclosed as a
ceiling. A stronger variant (owner launches Controller B in a wholly separate
session) is available if the owner chooses to strengthen the evidence.

## Initial setup order (owner instruction "Initial Repository Setup Order")

1. preflight — done (table above).
2. fetch remote refs — done.
3. record starting `origin/main` — `06a57d1...` (above).
4. verify PR #268 integrated — done (ancestor + == HEAD).
5. clean Campaign 2 branch/worktree from the baseline —
   `git worktree add -b campaign/durable-repo-self-development
   H:/GithubRepositories/smk-campaign-2 06a57d1` — done, clean tree.
6. preserve owner instruction verbatim — `OWNER-INSTRUCTION.md` — done.
7. concise charter — `CHARTER.md` — done.
8. initial state record — `CAMPAIGN-STATE.md` (v1) — done.
9. controller-checkpoint storage — `controllers/` (+ `README.md`) — done.
10. startup provenance — this file — done.
11. commit the Campaign 2 bootstrap — this commit.
12. push the bootstrap checkpoint — yes (durable succession evidence benefits
    from the branch existing on `origin`; result recorded in `CAMPAIGN-STATE.md`
    section 15).
13-15. reconstruct product/capability state → compare strategic boundaries →
    select Task A — Controller A's next responsibility, checkpointed in
    `controllers/A-reconstruction-and-selection.md` before any Task A
    implementation.
