# Sequential Autonomy Pilot 002 - target not admitted

**Status:** `TARGET_NOT_ADMITTED`. The pilot stopped at target admission. No participant was launched and no product change was made.
**Repository:** `ThorStarlord/sensemaking-skills`
**Pinned revision:** `origin/main` = `53b667c17c3e2e65ef2e344ccedfc60296f8d7cd` (fetched 2026-11-09; includes PR #793)
**Evidence class:** identity and admission record only. No behavioral evidence about sequential autonomy was produced.
**Receipt:** [session receipt](../../.sensemaking/receipts/2026-11-09-sequential-autonomy-pilot-002.session.yaml)

## 1. Review of Pilot 001

Pilot 001 was partial historical evidence, as the pilot brief says. Its receipts were read from branch `claude/pilot-001-graph-reasoning` (commit `b7a324a2`, local only, not pushed):

- Session `2026-11-09-pilot-001-graph-reasoning`, final, `NO_MODEL_CHANGE`. It ran RECALL and RELATE on `decision:legacy-planner-fails-closed` and found no overstated record.
- Its base was local `main` at `db254989`, which is not the remote default. Pilot 001 therefore used a stale commit.
- Its identity fields were not verified. The installed Skill and the global CLI were not checked against the pinned revision.
- It showed no multi-responsibility continuation. Its single responsibility cluster ended at a justified no-change.

This report does not repeat that legacy-planner investigation.

## 2. Execution baseline

| Item | Record |
| --- | --- |
| Remote default branch | `main`, SHA `53b667c17c3e2e65ef2e344ccedfc60296f8d7cd` (`git ls-remote`) |
| Isolated worktree | `.claude/worktrees/sequential-autonomy-pilot-002`, branch `claude/sequential-autonomy-pilot-002`, created at the remote SHA, clean |
| Main checkout | Left untouched. It is at `db254989` with 54 uncommitted entries that are not this session's work |
| Model | `claude-haiku-5-5` (Haiku 5.5), per the session environment |
| Harness | Claude Code desktop app (Code tab); the controller is the same agent throughout |
| Participant | None. No subagent was spawned and no fresh-context run was made |

## 3. Installed Skill and CLI identity

These checks are read-only. Nothing was synced into the user's installed Skill root.

| Subject | Finding |
| --- | --- |
| Installed `using-sensemaking/SKILL.md` | Blob `92bb8409` is the exact blob of commit `0455ec66` (2026-11-05). `origin/main` has blob `6c64ed45`, so the installed copy is older. Probe: content drift (repository 703 lines, installed 651). Its `references/` match `origin/main`. |
| Installed `strategic-sensemaking-loop/SKILL.md` | Blob `77465129` matches **no commit** in full history (`git log --all --find-object`). Identity **unverified**. `origin/main` has blob `8726bfbc`. Probe: `references/autonomous-terminal-mission-v1.md` and `references/resume-and-routing-v1.md` differ. `diff -rq` also shows `SKILL.md`, `agents/openai.yaml` and `references/value-action-and-delegation-v1.md` differing. |
| Global `sensemaking-skills` CLI | Imports from the main checkout's `src/` (`H:\GithubRepositories\sensemaking-skills\src`), so it is not the pinned revision. Its version string `1.0.0rc5.dev0` is identical to the worktree's, so the version string does not establish identity. |
| CLI from the pinned worktree | `PYTHONPATH=src python -m sensemaking_skills.cli --version` imports the worktree's own module and prints `1.0.0rc5.dev0`. This is the compatible-revision check used for any later run. |

Parity probe command: `python scripts/probe_skill_distribution.py --repo-root . --installed-dir C:/Users/Admin/.claude/skills --no-write --skill using-sensemaking --skill strategic-sensemaking-loop`. Result: 2 checked, 0 synchronized, 2 content drift, 0 missing.

Installed copies were not refreshed. Refreshing them changes the user's environment outside this repository and is not within this pilot's authority.

## 4. Target admission

The pilot requires one already-authorized, product-valuable outcome that is not complete, naturally needs at least two consequential engineering responsibilities, has terminal acceptance conditions, needs no unresolved Level-4 choice, and is verifiable with existing mechanisms.

| Candidate source | What was found | Admissible? |
| --- | --- | --- |
| Open GitHub issues | Seven open: #554, #552, #515, #384, #255, #226, #218. **None** carries the `ready-for-agent` label defined in `docs/agents/triage-labels.md`. Most are qualification, research or externally blocked. #384 requires repository-settings changes that are outside this pilot's authority. | No |
| Open PRs | One draft, #775, an exploration docs PR that another branch owns. It carries no build authorization. | No |
| Plans with unchecked items | `2026-11-05-agent-native-knowledge-graph-reasoning.md` (16): steps 2 to 6 are gated `if GO`. Its implementation record shows PR #760 ended `NO_NEW_SCHEMA / NO_NEW_PREMISE_QUERY / NO_NEW_REVIEWED_PACK`. `2026-11-05-connected-prospective-inquiry-ontologies.md` (7): conditional stop-and-propose items. `2026-11-05-strategic-evolution-learning-ontology.md` (5): `Only if GO`; Task 9 ended `NO_NEW_KNOWLEDGE_PACK`. | No: gates not opened |
| `STATUS.md` current responsibility | R6 requires a genuinely separate coding-agent session with a verified Skill source. R7 requires an isolated executor. Both are qualification, not a product outcome, and neither is available here. | No |
| Pilot 001 finding F-4 | `context-for` on a regression test returns NOT_ASSESSED ownership, because test files are not `owned_paths`. Admitting a fix requires extending `owned_paths` beyond components: `knowledge.py` lines 135, 197-203 and 289 are component-only, and the knowledge contract line 74 states the exact-match rule. The governing ADR 0033 (architecture and ontology vocabulary) is **PROPOSED**, and ADR 0032 is also PROPOSED. | No: owner-reserved contract decision |
| PATH-1 evidence-selected work | The current boundary authorizes selecting one evidence-grounded responsibility at a time. It names no outcome, and recent examples such as PR #793 were single responsibilities. | No: mode of selection, not an admitted outcome |

**Verdict: `TARGET_NOT_ADMITTED`.** No eligible outcome exists under the criteria. No work was invented to fill the pilot.

## 5. Owner decision required

The pilot cannot continue without one of these. This is recorded as the blocking question in the receipt.

1. **Name an admitted target** that already has owner authorization and terminal conditions. The pilot would then run on that item's terms, with the same stop rules.
2. **Authorize the test-file linkage contract change** (Pilot 001 F-4) after ADR 0033 is ratified or the owner decides the contract directly. This would make a multi-responsibility build admissible.
3. **Defer Pilot 002.** No pilot run occurs. Sequential-autonomy evidence stays unqualified, and PATH-1 continues as before.

## 6. Scope, authority and evidence

- Authority used: read, local worktree writes, commits, and the draft PR this report sits in. Merge, release, deployment, tracker writes and protected owner decisions were not used.
- Owner interventions during this session: none. The owner's pilot brief was the only input.
- What the evidence supports: the pinned revision, the installed-copy identity findings, the CLI-source discrepancy, and the admission record.
- What it does not support: any claim of sequential autonomy, Skill composition in practice, or continuation across responsibilities. No participant ran, so no fresh-agent or inline behavioral evidence exists.
- Installed `strategic-sensemaking-loop` identity remains **unverified**.

## 7. Verification

| Check | Result |
| --- | --- |
| `git ls-remote origin refs/heads/main` | `53b667c1...` |
| Worktree clean at creation | PASS (0 entries) |
| Installed-blob matching across full history | Recorded in section 3 |
| Parity probe (read-only, no `--sync`) | Ran; drift reported, nothing changed |
| GitHub issue, PR and merged-PR listing | Ran; results in section 4 |
| Receipt validator on the session receipt | See the receipt's `validation` fields |
| Docs currentness validator | Run before commit; see commit notes |
| Unit tests | **NOT_RUN** under the construction-phase rule in `CLAUDE.md`. No code changed |
| Hosted CI on the draft PR | Pending when written. Not treated as qualification |

## 8. Second pass: reconciliation, Skill environment and bounded operator discovery

**Status:** `OWNER_DECISION_REQUIRED`. No candidate is both unprotected and multi-responsibility, and at least one promising candidate needs a protected owner choice. No participant was launched. Sections 1-7 are the first pass and remain historical; this section corrects and extends them. The first-pass receipt is immutable; its continuation is [`2026-11-09-sequential-autonomy-pilot-002-reconciliation.session.yaml`](../../.sensemaking/receipts/2026-11-09-sequential-autonomy-pilot-002-reconciliation.session.yaml).

### 8.1 Corrections to the first pass

- **Overstated admission inference.** Section 4 and finding F-4 of the first receipt said that no `ready-for-agent` label meant no owner-authorized product outcome was admissible. That conflated a tracker triage label with authorization. The corroboration plan (section 4.2) expressly allows proportionate operator discovery outside the participant, and PATH-1 (`STATUS.md`) is the active repository-local construction responsibility. The first pass established only that no labelled or gated task was ready. Section 8.3 supersedes its verdict.
- **ADR authority versus adjacent change.** ADR 0033 is PROPOSED, so its contract change (ownership for non-component claims) is not ratified. That does not forbid adjacent product changes. PR #793 changed `knowledge_architecture.py` within the existing contract, and it is a valid precedent. Only the ownership-model change is protected.
- **Test-file issue not promoted.** Pilot 001 F-4 (file-level `context-for` on test files returns NOT_ASSESSED ownership) is recorded here as an unratified observation. It is not an approved requirement and is presented as an owner choice in section 8.3.
- **Load-mode over-claim.** The first receipt recorded `load_mode: harness_discovered` for `using-sensemaking` without revision identity. Section 8.2 shows the loaded copy is the user-installed revision, not the pinned source. Claims about current-version qualification are withdrawn.

### 8.2 Current-version Skill environment

| Subject | Finding |
| --- | --- |
| Pinned source | `origin/main` = `53b667c17c3e2e65ef2e344ccedfc60296f8d7cd` (re-fetched 2026-11-09). The worktree branch head `185a6868` differs from it only by this report and the first-pass receipt, so the Skill sources are identical. |
| Isolated root | Scratchpad root `isolated-skills`, populated only by `scripts/probe_skill_distribution.py --sync` for `using-sensemaking`, `strategic-sensemaking-loop` and `repository-semantic-steward`. Result: 3 of 3 synchronized, 0 drift. Not the user's root. The harness does not scan this root, so it is not harness-discovered. |
| User-installed root (`C:\Users\Admin\.claude\skills`, read-only probe) | `using-sensemaking`: content drift (repo 703 lines, installed 651; `references/` match). `strategic-sensemaking-loop`: content drift (repo 518, installed 496; `references/autonomous-terminal-mission-v1.md` and `references/resume-and-routing-v1.md` differ). `repository-semantic-steward`: synchronized. |
| Loaded `using-sensemaking` in this session | Host-attributed to `C:\Users\Admin\.claude\skills\using-sensemaking`. The loaded text says "For a bounded divergent inquiry"; the pinned copy says "substantive divergent inquiry" and the user-installed copy says "bounded". This is a text comparison, not host-native version attribution. Installed blob `92bb8409` is the loaded revision; the pinned blob is `6c64ed45`. |
| `strategic-sensemaking-loop` | Listed by the harness; not loaded in this session. No load evidence. |
| CLI on `PATH` | `/c/Users/Admin/.local/bin/sensemaking-skills` imports `H:\GithubRepositories\sensemaking-skills\src` (the main checkout). It is not the pinned revision. Its version string matches the worktree's, which does not establish identity. |
| CLI from the pinned worktree | `PYTHONPATH=src python -m sensemaking_skills.cli --version` imports the worktree `src` and prints `1.0.0rc5.dev0`. Used for any later run. |
| Native harness discovery | Not verified. The harness listing shows the skills, but no host evidence ties a load to a revision. |

**Claim ceiling:** current-version Skill qualification is **not** claimed. The isolated root is parity-verified; the user-installed root is not; the loaded `using-sensemaking` text is the user-installed revision by text comparison. The installed copies and the global CLI were **not** synced, because that changes the user's environment outside this repository.

### 8.3 Bounded operator-side opportunity discovery

**Method.** Read the compass (`CONTEXT.md` current product definition, `docs/persistent-semantic-stewardship-plan.md` sections 12, 14 and 15, ADRs 0025, 0026, 0031, 0033, 0034, `STATUS.md` PATH-1). Surveyed open issues (7: #554, #552, #515, #384, #255, #226, #218; none labelled `ready-for-agent`; mostly qualification, external or settings work), open PRs (#794, and draft #775 owned by another branch), recent merges #782-#793, unfinished-work markers in `src/` and `scripts/` (none in execution paths), and unchecked plan items. Discovery did not reopen repository-wide strategy.

**Recent product pattern.** PR #793 is a single PATH-1 responsibility: a source-visible limitation in `context-for` (provenance links for omitted items), with its authority and evidence ceiling stated. The repository's normal shape for PATH-1 work is one bounded change, not a multi-responsibility program.

**Stale authority surface observed.** The October 20 construction plan (`docs/superpowers/plans/2026-10-20-construction-first-semantic-stewardship.md`) still shows 36 unchecked boxes. Source confirms that its Tasks 2-5 are implemented: `semantic_architecture/worktree_context.py`, `knowledge-query --repo` with `workspace_context`, repeated `--term`, and `--expect-kind` with `bounded_coverage`, and matching `recall.md` guidance. The boxes are stale, not the features.

| Candidate | Real benefit | Current source evidence | Implemented or claimed? | Accepted-strategy relation | Authorization boundary | Multi-responsibility? | Verification and completion | Cost, reversibility, downside | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **C1. File-level `context-for` for test files** (Pilot 001 F-4) | An agent asking about a regression test gets NOT_ASSESSED ownership, although a reviewed verification claim reaches its component. | `knowledge.py` ownership validation is component-only (`owned_paths`). `knowledge-contract.md` line 74: file-level `context-for` matches `component.owned_paths` exactly. Pilot 001 QY-8 is NOT_ASSESSED. | Not implemented. Not claimed as a requirement. | PATH-1 serves ADR 0034 decision context. Ownership semantics belong to the ADR 0033 vocabulary. | **Protected.** ADR 0033 is PROPOSED with owner acceptance pending. Changing what owns a test file is a contract decision. | Yes, if authorized: decision, validator, query, records, docs, tests. | If authorized: named test files return an explicit, labelled verification or ownership link; components and missing links stay NOT_ASSESSED. CI and tests not run locally under construction policy. | Moderate and reversible. Downside: tests could be treated as owners, widening what "owner" means. | **OWNER_DECISION_REQUIRED** |
| **C2. Fog-to-workflow fallback in `finalize_plan`** (owner Q-1, open since 2026-10-25) | Small. The map applies only to ui_fog and docs_fog when a brief lacks a valid recommendation. | `scripts/workflow-runtime.py` lines 1237-1245 and 1290-1400. In-repo callers are tests and instruction text (`workflow-runtime.py` 1011, 1113; `workflow-orchestration-template.md`). | Implemented as a fallback. Its own comment says product and architecture fog deliberately have no fallback. | ADR 0025 (accepted 2026-08-23) specifies the fallback. | **Protected.** Reconcile, retire or keep changes ADR 0025 behaviour. | Possibly, after the choice. | Would need its own responsibility and tests, after the choice. | Low to moderate. Reversible. | **OWNER_DECISION_REQUIRED** (lower priority) |
| **C3. Stale checkboxes in the October 20 plan** | Keeps the authority surface truthful, so a future agent does not treat completed work as pending. | Tasks 2-5 implemented; 36 unchecked boxes (section 8.3). | Documentation state only. | Within authority: documentation currentness. | Within authority. | No: one documentation reconciliation, which the brief says not to make as a documentation-only PR. | Docs currentness validator. | Very low. | Not a pilot target. Fold into the next PATH-1 change, or leave as is. |
| **C4. Sync user-installed Skills and reinstall the global CLI** | Consumers on this host would get current guidance and the current CLI. | Section 8.2 drift and import path. | Not done. | Operational, outside the repository. | **Outside repository authority.** It writes to shared user directories and the user's `PATH` install. The brief prefers isolated installation. | No. | Read-only probe after sync. | Reversible but shared. | **Owner action, not a repository target.** The isolated root is already parity-verified. |

**Admission outcome: `OWNER_DECISION_REQUIRED`.** Under this brief, `TARGET_ADMITTED` needs a bounded, unprotected, multi-responsibility goal. C1 is the only multi-responsibility candidate, and it turns on a protected ownership choice. C2 is protected and low-value. C3 and C4 are not pilot targets. `TARGET_NOT_ADMITTED` does not fit because a promising opportunity exists and needs a protected choice.

**The protected choice (C1), not decided here.**

1. **Authorize an ownership model for test files** (accept ADR 0033 or give a direct contract decision). Consequence: a multi-responsibility build becomes admissible: decision, validator, query semantics, records, docs and tests. The pilot could then run on that goal.
2. **Keep component-only ownership.** Consequence: test files stay reachable through explicit verification records and component `explain`, and file-level NOT_ASSESSED stays by design. No build.
3. **Defer.** Consequence: no pilot run; sequential-autonomy evidence stays unqualified.

Criterion 3 of the corroboration plan (heterogeneity from Trial 001) cannot be met on repository shape, because both pilots target `sensemaking-skills`. This is recorded, not hidden.

### 8.4 Execution

No participant was launched and no inline pilot was run, because nothing was admitted. The execution boundary is the owner's choice in section 8.3. A ready-to-run brief exists only after that choice.

### 8.5 Evidence distinctions

- **Availability vs. loading:** the harness lists both Skills. Load evidence exists only for `using-sensemaking`, by text comparison.
- **Loading vs. substantive application:** no application evidence.
- **Engineering work vs. continuation:** no product code changed. No continuation was exercised.
- **One responsibility vs. terminal completion:** none.
- **Authorized autonomous work vs. protected transitions:** no merge, release, deployment, tracker write, ADR edit, installed-copy sync or global CLI reinstall.
- **Agent summaries vs. repository evidence:** identity claims cite Git blob hashes, probe output and import paths.

### 8.6 Authority boundary

Used: read access; the isolated scratchpad root; a local worktree commit; a push to `claude/sequential-autonomy-pilot-002`; and the draft PR body. Not used: merge, release, deployment, tracker writes, ADR or Skill rewrites, global installed-copy sync, or any protected owner decision.

### 8.7 Verification

| Check | Result |
| --- | --- |
| `git fetch origin main`; worktree diff vs `origin/main` | `origin/main` unchanged at `53b667c1`; the branch differs only by pilot docs |
| Read-only parity probe, user-installed root | RAN: drift reported for two Skills; nothing written |
| Isolated scratch sync and parity probe | RAN: 3 of 3 synchronized |
| CLI import checks (PATH and worktree `src`) | RAN: paths and version recorded above |
| Source-citation checks (`owned_paths`, contract line 74, `finalize_plan` callers) | RAN: read in source |
| `validate-docs-currentness.py` and `validate-receipt.py` on the continuation receipt | Run before commit; see the commit |
| Unit tests | **NOT_RUN** under the construction-phase rule. No product code changed |
| Hosted CI on the draft PR | Previously green at `185a6868`. It reruns on the new commit and is not treated as qualification
