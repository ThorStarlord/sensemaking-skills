# Campaign 3 startup provenance

```
STATUS:    factual record of the Phase 0 mandatory preflight. Non-authoritative.
           Facts here are CLAIMS as of the recorded date; a continuing
           controller reverifies consequential claims from repository / GitHub
           evidence before acting (CHARTER.md constraint 10).
DATE:      2026-09-02
AUTHOR:    lead Campaign 3 controller (the context that received the owner
           instruction).
```

## 1. Repository identity (Phase 0 items 1-2)

- Working repository: `H:/GithubRepositories/sensemaking-skills` (the shared
  `main` checkout — NOT used for campaign work; it was dirty with unrelated
  untracked experiment files at Campaign 3 startup).
- Remote `origin`: `https://github.com/ThorStarlord/sensemaking-skills.git`
  (fetch + push).
- Campaign 3 isolated worktree: **`H:/GithubRepositories/smk-campaign3`**
  (created 2026-09-02 via `git worktree add`).
- Campaign 3 branch: **`campaign/durable-architectural-continuity`**
  (new branch, forked from the recorded baseline below).

## 2. Baseline / integrated starting state (Phase 0 items 3-6)

```
git fetch origin --prune            -> done 2026-09-02
STARTING origin/main (Campaign 3 base): 969e8eb47144ffdeb27a8d9df02b6a292586e842
   969e8eb  "Merge pull request #270 from ThorStarlord/docs/campaign2-closure-stamp"
CAMPAIGN 3 BASE:                     969e8eb  (worktree/branch forked here)
LOCAL main checkout (H:/.../sensemaking-skills) at startup: f10b7da (37 commits
   BEHIND origin/main — stale; not used).
```

**PR #269 integration (Phase 0 item 5).** `GITHUB-VERIFIED`:
`gh pr view 269` -> `state: MERGED`, `mergedAt: 2026-09-02T19:32:04Z`,
`mergeCommit.oid: 7e48cf076cde6079d6b9b3fe339462733fd87e4b`, base `main`,
head `campaign/durable-repo-self-development`. `7e48cf0` is an ancestor of
`969e8eb` (it appears in `git log origin/main`).

**Post-#269 closure commits (Phase 0 item 6).** Campaign 2 did NOT stop at the
#269 merge:
- `3ffc94d` campaign2(closure): FINAL-REPORT + A/B retrospective; disposition
  CAMPAIGN_COMPLETE (on the campaign branch, pre-merge).
- `7e48cf0` Merge PR #269.
- `e9d1cbd` docs(campaign2): closure stamp — PR #269 merged, doc-status
  non-normative, campaign CLOSED.
- `969e8eb` Merge PR #270 (`docs/campaign2-closure-stamp`) — **current
  `origin/main` HEAD**.

## 3. Campaign 2 final closure state (Phase 0 items 6, 10)

`REPOSITORY-VERIFIED` (`docs/campaigns/durable-repo-self-development/` read
2026-09-02) + `GITHUB-VERIFIED` (#269, #270 merged).

- **Disposition: `CAMPAIGN_COMPLETE`** (`FINAL-REPORT.md` §17;
  `CAMPAIGN-STATE.md` v7 "CLOSED").
- **Owner integrated the work**: PR #269 merged into `main` (`7e48cf0`) after an
  independent narrow architectural/authority review recommended MERGE (APPROVE).
  So Campaign 2's Task A + Task B product changes **are now on integrated
  `main`**:
  - Task A: `STATUS.md` refreshed into a current-direction + reconstruction
    surface; `roadmap.md` / `goal.md` historical/superseded headers; `CONTEXT.md`
    +1 source-of-truth-map row (`STATUS.md`).
  - Task B: `scripts/probe_relationships.py` live-document classifier honors an
    explicit `<!-- doc-status: historical -->` marker (`_declared_doc_status`
    helper + `_classify_doc_file(rel, declared_status)` + `_discover_docs`
    wiring); marker applied to `roadmap.md` / `goal.md`;
    `tests/test_probe_relationships.py` +4 regression tests.
- **OWNER DECISION**: the `<!-- doc-status: historical -->` marker is left
  **NON-NORMATIVE** — a probe heuristic within the already-owner-accepted
  "doc-surface discovery" Probe Engine capability, NOT a ratified repository-wide
  convention. No convention doc, no ADR, no template/CLAUDE/vocab entry. Nothing
  beyond `roadmap.md` / `goal.md` should be instructed to emit it unless the
  owner later blesses it.
- **No Controller C.** Campaign 2 CLOSED.
- **Campaign 2's central answer** (`FINAL-REPORT.md` §16): the smallest
  currently-evidenced sufficient capability for repository-level development
  direction to survive independent controller replacement = a current-direction
  Markdown surface at a named location + an ordered reconstruction reading path
  + historical-in-place markings honored by the deterministic drift machinery.
  "SUPPORTED AS THE SMALLEST CURRENTLY EVIDENCED CANDIDATE", not strict
  minimality. No schema / artifact type / workflow / hook / router / state
  machine / registry field / `repo-sensemaker` change was warranted.

## 4. Inherited evidence ceilings (Phase 0 item 11)

From the Campaign 3 owner instruction + Campaign 2 (`CAMPAIGN-STATE.md` §7,
`FINAL-REPORT.md` §15/§16):

- **EC-a (from the owner instruction).** Campaign 2 did NOT establish:
  independent process/model succession; concurrent controllers; universal
  autonomous repository development; **deep coupled multi-surface implementation
  under succession**; formal Sensemaking Skills self-hosting; strict minimality
  of its durable continuation state.
- **EC-b Succession isolation.** Campaign 2's strongest honest claim: context
  isolation HARNESS-REPORTED (`Agent` tool starts the subagent cold); bootstrap
  minimality / checkpoint immutability / non-resumption CONTROLLER-ASSERTED;
  predecessor **process** non-persistence and **model** independence
  NOT ESTABLISHED (same `claude-sonnet-5` family; the subagent returns its
  report to the parent). `SUCCESSION_ISOLATION_UNVERIFIED` on those dimensions.
- **EC-c Scale.** All succession evidence is n=1..2 controllers, one repository,
  a short horizon.
- **EC-d Strict minimality.** No comparative / staged-reveal / withheld-field
  evidence for any durable-state arrangement.
- **EC-e Implementation depth.** No broad `src/` or multi-surface implementation
  depth from durable state has been demonstrated. Campaign 2 lifted this only
  modestly (a single-file `scripts/` change + 4 tests).

## 5. Current product direction (Phase 0 items 8-9)

`REPOSITORY-VERIFIED` (`STATUS.md`, `CONTEXT.md`, `roadmap.md`,
`docs/research/control-model-research-agenda.md` read 2026-09-02 at `969e8eb`).

- **Product definition** (`CONTEXT.md`): "agent-native engineering sensemaking
  and control layer for software-engineering agents." Active coding agent owns
  the recursive control loop (ADR 0013). Ratified external product scope = the
  validated, human-reviewed `repository_sensemaking_brief` (ADR 0014).
  Automatic fog-type -> implementation routing is NOT ratified.
- **Current product-validation priority** (`STATUS.md`): **Goal A — External
  Product Validation** (`A1 = ACTIVE`). The first A1 episode is **paused at an
  execution-substrate boundary** (three substrates falsified;
  `experiments/evidence/0023-...`; tracked in **Issue #255**). "The current
  owner rule is to halt Goal A in this environment rather than build another
  harness. Resuming needs an owner/environment decision, not a repo-code
  change."
- **Highest-leverage warranted next boundary** (`STATUS.md`, verbatim intent):
  "Owner/environment decision on the Goal A execution substrate (Issue #255) —
  the product's central unvalidated hypothesis (brief usefulness beyond this
  repo) cannot advance without it, and it is **not a repo-code deliverable**.
  The in-authority engineering backlog is **deliberately small** (the nine
  workflow-system-disposition decisions; test-expectation debt D2b / D19; the
  `docs/` reconstruction surface itself). The repository posture is **harden
  only where pressured**."
- **Repository posture corroboration**: `CONTEXT.md` principle 10 "Harden only
  where pressured"; Campaign 1 closed with "no further product change is
  warranted by current evidence"; research-agenda **meta-finding 2026-08-30**:
  "Further sensemaking loops saturated... Future agents should not re-run
  sensemaking diagnosis to test this claim."
- **Stale strategic summaries reconciled** (Phase 0 item 9): `roadmap.md`,
  `goal.md`, `00-user-intent.md`, and the `CHANGELOG.md` "Deployment Timeline"
  footer all describe a superseded PyPI/GA/autonomous-router plan; `STATUS.md`
  (post-#269) and `roadmap.md`/`goal.md` (now carry `<!-- doc-status: historical
  -->` + a blockquote header) already flag this. No further reconciliation is
  needed for Campaign 3 selection — the do-not-anchor list is authoritative and
  current on `main`.
- **Open issues**: only #218 (normal-use control-model evidence lane —
  research-ops), #226 (C6R gate-separation study — frozen until preregistered
  result; do not modify C6R), #255 (Goal A substrate — owner/environment
  decision). **All three are research / owner-reserved; none is an in-authority
  product-engineering task.**
- **Open PRs**: only #194 (draft, `experiment/exp-0003-results`, "do not
  merge").

## 6. Repository qualification requirements (Phase 0 item 7)

`REPOSITORY-VERIFIED` (worktree `969e8eb`):

- `scripts/validate-repo.py` (Level 1 repository validator).
- `scripts/probe-repo.py` + `scripts/validate-probe-report.py` +
  `scripts/gate_relationship_findings.py` (the probe engine + its report
  validator + the blocking-findings gate — "probe gate").
- `tests/` : 143 `test_*.py` files. Campaign 2 used `test-validators.py`
  (78/78), a "core-assertions" pytest set, and the
  `probe_relationships`-dependent module set for routine qualification.
- CI: `.github/workflows/validation.yml` ("Validator Ecosystem", ~19-20 jobs
  incl. Gate A Linux+Windows, phase 2-6 suites, `validate`, `probe-gate`,
  `core-assertions`, `conditional-representation-exact-head`). Campaign 2
  qualified campaign heads via a **draft PR's `pull_request` event**.
- Known pre-existing local reds (identical on Campaign 2 baselines; green in
  Linux CI): `tests/test_validate_brief_json.py` (D2b fixture drift); a
  wheel/`setup_skills` platform red; a `NoPresentTenseEnforcementClaims`
  platform red; committed `src/sensemaking_skills.egg-info/PKG-INFO` at Version
  0.2.1 vs `pyproject` 0.2.2 (CI restores egg-info before "tree not mutated"
  checks). **Console output is ASCII-only** on this repo (Windows cp1252) —
  non-ASCII in `print()`/stdout crashes the process (`CLAUDE.md`).

## 7. Authority (Phase 0 items 12-14)

- **Mutation authority**: local engineering on the Campaign 3 branch/worktree
  (code, tests, docs warranted by product changes, commits, campaign state) —
  granted (`OWNER-INSTRUCTION.md`; `CHARTER.md` AUTHORITY).
- **Push / PR authority**: push the Campaign 3 branch; create/maintain a
  **draft** PR. `gh auth status` -> logged in as `ThorStarlord`, token scopes
  `repo`, `workflow`, `read:org`, `gist`. Git identity in the worktree:
  `ThorStarlord <thorstarlord@users.noreply.github.com>`.
- **Merge / ratification / owner-reserved**: NOT granted. See `CHARTER.md`
  "OWNER-RESERVED DECISIONS". Standing owner-reserved: the nine
  `docs/workflow-system-disposition.md` §6 items; Goal A substrate (Issue #255);
  ratifying any Campaign 2 conclusion (incl. the non-normative `doc-status`
  marker); ADR acceptance; external publication; issue-lifecycle changes for
  bookkeeping; unrelated PR merges; protected-policy edits; inferring owner
  preference.

## 8. Fresh Controller B instantiation (Phase 0 items 15-21)

- **Mechanism available**: the Claude Code `Agent` tool with
  `subagent_type: general-purpose` (also `Explore`, `Plan`). `isolation:
  "worktree"` gives the subagent its own git worktree. This is the **same
  mechanism Campaign 2 used** for Controller B
  (`FINAL-REPORT.md` §4/§5): "a fresh `general-purpose` sub-agent context
  spawned via the Claude Code `Agent` tool with the verbatim bootstrap ...
  Fresh context window; no shared transcript; no predecessor private reasoning."
- **B can access the intended repository state**: yes — the subagent runs in the
  same filesystem; it is pointed at the committed Campaign 3 worktree/branch
  head, or given its own worktree checked out at the handoff SHA.
- **B can access Git / GitHub / validation**: yes — subagent has the same tool
  surface (Bash `git`, `gh`, pytest, the `scripts/validate-*` + probe
  entrypoints).
- **Bootstrap recording**: the exact verbatim bootstrap text given to B will be
  recorded in `controllers/A-handoff.md` before B is spawned, and echoed in
  `CAMPAIGN-STATE.md`'s handoff-provenance block.
- **Honest isolation ceiling** (`CHARTER.md` constraint 7; matches Campaign 2
  EC-b):
  - context isolation (no transcript, no predecessor private reasoning):
    **`HARNESS_REPORTED_ISOLATION`** — the `Agent` tool starts the subagent
    cold.
  - bootstrap minimality / checkpoint immutability / non-resumption:
    `CONTROLLER_ASSERTED` (discipline, not environment-enforced).
  - predecessor **process** non-persistence: **`SUCCESSION_ISOLATION_UNVERIFIED`**
    — the parent (predecessor) process continues and receives the subagent's
    final report.
  - **model** independence: **NOT ESTABLISHED** — same `claude-sonnet-5` family
    unless the owner separately launches B in a different model/session.
- **Phase 0 stop test**: a genuine successor context with adequate capability
  **can** be created at the same honest evidence level Campaign 2 achieved.
  Campaign 3 does **not** stop with `EXTERNAL_BLOCKER` on this dimension. The
  process/model-isolation ceiling is carried forward, not treated as a blocker
  (Campaign 2 established the precedent that this level of isolation is
  sufficient to run the succession experiment with an explicitly recorded
  ceiling).

## 9. Preflight disposition

Phase 0 items 1-23 addressed. Items 22-23 (isolated worktree + committed
durable scaffolding) complete with the bootstrap commit that adds this file.
Next: Controller A begins Phase 1 — reconstruct current product state and
identify the highest-leverage warranted product capability boundary within
campaign authority, then assess whether its smallest coherent implementation is
genuinely semantically coupled.
