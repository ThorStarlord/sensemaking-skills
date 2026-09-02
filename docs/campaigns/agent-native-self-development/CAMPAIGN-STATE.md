# Campaign: reliable agent-native, artifact-mediated self-development

```
STATUS:    ACTIVE development-campaign record (living document)
AUTHORITY: non-authoritative. Not an ADR, not a contract, not a validator input,
           not a registered workflow, not a research-agenda ratification.
NOT:       an EXP-NNNN governed experiment campaign (ADR 0023 two-lane machinery
           does not read this file; no approval envelope applies).
READS:     nothing in scripts/, src/, tests/, or .github/ reads this file.
BRANCH:    campaign/agent-native-self-development   (base: main @ f10b7da, 2026-09-02)
WORKTREE:  H:/GithubRepositories/smk-campaign
RULE:      update after every consequential campaign responsibility.
```

This file exists so that campaign reasoning does not live only in one
conversation's context. A fresh coding-agent context should be able to
reconstruct from this file (plus the repository) the mission, the current
capability state, why the current task was selected, what is established, what
is uncertain, what is warranted next, and what authority exists. Whether it
actually can is itself a campaign question (see U1).

---

## 1. CAMPAIGN MISSION

Advance Sensemaking Skills toward **reliable agent-native, artifact-mediated
self-development**: an active coding agent uses repository evidence and durable
artifacts to determine the next warranted engineering responsibility, select an
appropriate capability, perform bounded work, validate the resulting evidence,
preserve authority boundaries, carry state across responsibilities, and
recursively continue until the active goal is satisfied or further action is
unwarranted.

Campaign-level, not a monolithic rewrite. The campaign is controlled directly
by the active coding agent, **not** by `repo-sensemaker`, `using-sensemaking`,
registered workflows, workflow-runtime routing, or hooks (bootstrap constraint).
Ordinary repository engineering infrastructure (tests, validators,
`validate-repo.py`, probe engine, CI, git) is used normally.

Control model owned by the agent:

```text
PRODUCT MISSION
  -> current repository / product state
  -> highest-leverage unresolved capability boundary
  -> decision-changing uncertainty
  -> ONE bounded responsibility
  -> bounded analysis / design / implementation / verification
  -> durable repository evidence
  -> validate
  -> update this record
  -> reassess from the mission
  -> continue / owner decision / blocker / complete
```

Campaign vocabulary used below (from the campaign charter, not canonical
repository vocabulary): finding classes `CAMPAIGN_BLOCKING | CAMPAIGN_RELEVANT
| LOCAL_BUT_REAL | HISTORICAL_ONLY | DEFERRED | NO_ACTION_WARRANTED`;
reconstruction-failure classes `MISSING_DURABLE_STATE |
CAPABILITY_DISCOVERY_FAILURE | WARRANT_AMBIGUITY | AUTHORITY_AMBIGUITY |
PRODUCT_DIRECTION_AMBIGUITY | INCIDENTAL_CONTEXT_LOSS`; workflow dispositions
`KEEP_AS_BOUNDED_SUBGRAPH | REPAIR | DEMOTE | RETIRE_CANDIDATE | HISTORICAL |
INSUFFICIENT_EVIDENCE`.

---

## 2. CURRENT PRODUCT / CAPABILITY STATE (main @ f10b7da, 2026-09-02)

| Capability | State | Evidence (repository) |
|---|---|---|
| Top-level semantic control model | **EXPLICIT in docs**; agent owns loop; decision vs orchestration separated; warrant vocabulary defined | `CONTEXT.md`; `docs/decision-orchestration-boundary.md`; `docs/agent-native-operating-workflow.md` (v0); ADR 0013 (Accepted, ratified 2026-08-13) |
| Product boundary | Human-reviewed `repository_sensemaking_brief` is the ratified external scope; routing deferred | ADR 0014 (Accepted, narrowed 2026-07-26) |
| Warrant / recommendation / selection / execution authority | **Separated and ratified**; auto-invoke is compatibility metadata; consumers fail closed | ADR 0026 (Accepted 2026-08-24); `tests/test_auto_invoke_authority_gating.py`; ADR 0018 SUPERSEDED |
| Workflow registry vs liveness | Identity and liveness separated; 8 of 23 registered workflows `compatibility_only`; planner/runtime/validator fail closed on non-active | ADR 0027 (Accepted 2026-09-01); `skills/workflow-planner/references/workflow-liveness.yaml`; PR #265 |
| Responsibility selection | **CONVENTION** (agent judgment + skill catalog); no machinery; automatic routing deliberately unratified | operating workflow Reality map; `using-sensemaking` SKILL.md sections 5-7 |
| Continuation across responsibilities | **CONVENTION_CLOSED**; typed fan-in contract-closed; prior-report selection by caller; reopen trigger recorded but **never exercised** | `docs/2026-08-programmatic-runner-retirement-plan.md` "Project closure"; operating workflow "CONTINUATION" |
| Continuation artifacts that exist | `user_intent` (ADR 0006), `session_summary` (generic validator only), `prompt_handoff` (skill-to-skill prompt packaging), `work_claim`, `reconciliation_report`, `repair_verification_report` | `skills/workflow-planner/references/artifact-contracts.yaml` ids at lines ~296, ~524, ~709, ~730, ~755; `skills/handoff/SKILL.md` |
| Repository-level development-direction representation | **ABSENT**. `STATUS.md` = version/validation-priority summary; `roadmap.md` = stale rollout plan (0.2.1 / Phase 2.3); `docs/semantic-control-map.md` = authority index under trial (not direction) | those files; evidence 0022 already recorded roadmap staleness |
| Deterministic machinery | validators (`validate-output.py` dispatch -> `validate-artifact.py` + specialized), probe engine (`probe-repo.py`, `repo_probes.py`, `probe_relationships.py`), `gate_relationship_findings.py`, `run-ledger.py`, `workflow-runtime.py` (paths/plan/gates/sessions; model executors retired 2026-08-13), `workflow_liveness.py`, `validate-repo.py` | `scripts/`; retirement plan classification tables |
| CI on `main` | `gate-a-*`, phase 2-6 campaign/execution suites, `validate` (scripts + one pytest file), `probe-gate`, `core-assertions` (7 pytest files), `conditional-representation-exact-head` | `.github/workflows/validation.yml` |
| Hooks | `.claude/hooks/sessionstart.md` documents a SessionStart bootstrap reminder; `.claude/settings.json` is `{}` (hook not wired in this checkout); no continuation/liveness hook exists | those files |
| Real-use evidence of the operating loop | Workflow v0 dogfood on 2 repos (verdict `KEEP_WITH_WATCH_ITEMS`); 3 normal-use episodes on Issue #218 (recurring boundary: merge base-advance x2) | `experiments/evidence/0021`, `0022`; Issue #218 |
| Research lanes (non-ratified) | C6R compressed control hypothesis (#226 open); warrant-as-primitive; uncertainty-selection; PHB meta-finding "sensemaking loops saturated; spikes not briefs" (2026-08-30); semantic-control-map persistence trial OPEN (min close 2026-09-28) | `docs/research/control-model-research-agenda.md`; `docs/semantic-control-map-trial-log.md` |
| Goal A external validation | ACTIVE but **halted in this environment** (three execution substrates falsified; owner halt rule) | Issue #255; evidence 0023 |

Baseline test state (local, Windows, Python 3.14): see section 13, D1/D2.

---

## 3. COMPLETED CAMPAIGN RESPONSIBILITIES

| # | Responsibility | Result | Evidence |
|---|---|---|---|
| R0 | Reconstruct current product/capability state from durable repository evidence; select first bounded responsibility; establish durable campaign record | this file (v1) | this file; branch `campaign/agent-native-self-development` |

---

## 4. EVIDENCE PRODUCED

- `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (this file).

---

## 5. CURRENTLY DEMONSTRATED CAPABILITIES

(Demonstrated = real repeated use with durable evidence, not merely documented.)

- Agent-native `repository_sensemaking_brief` production + mechanical validation on two structurally different repositories (evidence 0021, 0022).
- Responsibility selection without automatic routing; stop at owner/authority boundary instead of premature implementation (evidence 0022; #218 episodes 001, 003; #255).
- Claim reconciliation (`output-reconciler`) and finding-specific repair verification (`repair-verifier`) (evidence 0018, 0019, 0020).
- Fail-closed authority on `auto_invoke_next_workflow` and on compatibility-only workflow selection (ADR 0026/0027 test suites).
- Deterministic probe-engine enforcement in CI (`probe-gate`, `core-assertions`).

---

## 6. KNOWN MATERIAL GAPS

| id | Gap | Acceptance condition(s) affected | Class |
|---|---|---|---|
| G1 | No durable artifact carries campaign/task-level continuation state (goal, capability state, why-selected, established, uncertain, next, authority). Continuation is `CONVENTION_CLOSED` and has **never been tested by a fresh context**. | 4, 5 | CAMPAIGN_BLOCKING |
| G2 | No representation of repository-level development direction that lets an agent select consequential capability work over the nearest local defect. | 6 | CAMPAIGN_BLOCKING |
| G3 | Role of hooks undefined; the documented SessionStart hook is not wired (`settings.json = {}`); hook doc prose ("picks correct workflow first try", "auto-fix vs escalate") predates ADR 0026 and the current bootstrap SKILL.md. | 8, 11 | CAMPAIGN_RELEVANT |
| G4 | Per-workflow disposition in campaign vocabulary not recorded; ADR 0027 settles liveness, not KEEP/DEMOTE/RETIRE. | 9 | CAMPAIGN_RELEVANT |
| G5 | Deterministic-script role is described across the retirement plan, the boundary doc, and `CONTEXT.md` but not consolidated in one place. May already be sufficient; evaluate after G1/G2. | 7 | CAMPAIGN_RELEVANT |
| G6 | `docs/semantic-control-map.md` rows SE1 / SA13 / SA9 state that `probe-gate` and `core-assertions` exist only on an unmerged branch; both jobs are on `main`. Stale rows under an OPEN trial. | 11 | CAMPAIGN_RELEVANT (trial bookkeeping; log per protocol) |

---

## 7. ACTIVE CONSTRAINTS

- C1 **Bootstrap constraint**: this campaign does not use `repo-sensemaker`, `using-sensemaking`, registered workflows, runtime routing, fog routing, Skill-to-Skill continuation mechanisms under evaluation, or hooks as its controller.
- C2 **Authority**: merge to `main` is an owner decision (repository convention; Mode B+ standing boundary). Never falsify owner decisions or ADR `**Status**` lines. Push branches and open PRs for exact-head qualification; do not merge.
- C3 **Semantic-control-map trial is OPEN**: do not add rows (`MAP_EXPANSION_DEFAULT = NO`); refresh rows only on protocol triggers; record consultation/over-read events in the trial log.
- C4 **Goal A is halted** in this environment (#255); do not run Goal A episodes. Issue #218 episodes are recorded only when they arise from ordinary work.
- C5 **Windows cp1252**: console output ASCII-only; file reads in tests need explicit encoding.
- C6 **Worktree per session**: all campaign work in `H:/GithubRepositories/smk-campaign`; never the shared `main` checkout.
- C7 **Machinery promotion rule** (repository): repeated useful responsibility + stable semantics + repeated burden/error + mechanically expressible boundary -> candidate for formalization. Not: "there is a box in the diagram".

---

## 8. OPEN DECISION-CHANGING UNCERTAINTIES

| id | Uncertainty | Source | Cheapest sufficient evidence | Status |
|---|---|---|---|---|
| U1 | What continuation state does a fresh context actually fail to reconstruct from durable repository state (this record + repo)? Which failure class? | empirical | one fresh-context reconstruction probe (R1) | OPEN |
| U2 | Do the outer loop (repository-evolution: mission -> capability state -> next gap) and the inner loop (task-execution: goal -> uncertainty -> responsibility -> evidence -> closure) require different durable state, or one artifact? | repository_evidence + trace | compare what R1 needs vs what one real multi-responsibility task trace needs (R2) | OPEN |
| U3 | Is any hook warranted beyond a documented bootstrap? (liveness only: detect artifact -> validate -> register state -> wake agent) | empirical | only after U1/U2 show a recurrent continuation event that a manual step keeps missing | OPEN, gated on U1/U2 |
| U4 | Which registered workflows have enough real traces for a disposition other than `INSUFFICIENT_EVIDENCE`? | repository_evidence | grep evidence/ledger/CI for actual executions per workflow id | OPEN |
| U5 | Should continuation state ride on `session_summary` / `prompt_handoff` (existing contracts) or a new artifact type? | repository_evidence | decided by U1/U2 result + contract consumer check | OPEN, gated on U1/U2 |

---

## 9. CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

**Durable continuation state and fresh-context reconstruction** (G1 + G2). Every
other acceptance condition is either already met at the documentation level
(1, 2, 3), depends on real traces that only bounded campaign work will produce
(8, 9), or is end-of-campaign qualification (10-13).

---

## 10. CURRENT / NEXT WARRANTED RESPONSIBILITY

```text
R1  Fresh-context reconstruction probe

CAMPAIGN CAPABILITY AFFECTED:   artifact-mediated continuation (conditions 4, 5, 6)
CURRENT LIMITATION:             this record is an untested hypothesis about what a
                                fresh context needs; continuation CONVENTION_CLOSED
                                has never been exercised
WHY IT MATTERS TO THE MISSION:  the mission's central property; building continuation
                                infrastructure before observing the actual failure
                                class would be speculative (C7)
BOUNDED RESPONSIBILITY:         dispatch ONE fresh agent context with only the repo
                                path and this file's path; ask it to reconstruct the
                                seven items (mission, capability state, why current
                                task selected, what is established, what is uncertain,
                                what is warranted next, what authority exists);
                                classify each shortfall with the reconstruction-failure
                                classes; record verbatim in evidence
EXPECTED EVIDENCE OF PROGRESS:  docs/campaigns/agent-native-self-development/
                                R1-fresh-context-reconstruction.md with per-item
                                verdict + classification; U1 moves to RESOLVED or
                                NARROWED; this record updated
```

---

## 11. AUTHORITY OR OWNER DECISIONS REQUIRED

None blocking at R0. Standing: merge of campaign PR(s) to `main` (owner).

---

## 12. DEFERRED NON-CAMPAIGN FINDINGS

| id | Finding | Class | Disposition |
|---|---|---|---|
| D1 | `tests/test_path_drift.py:154,228,358` call `read_text()` without `encoding`; on Windows cp1252 this raises `UnicodeDecodeError` on `skills/architectural-review/SKILL.md` (byte 0x9d). CI runs on Linux (utf-8) and is unaffected. | LOCAL_BUT_REAL | deferred; fix is one-line `encoding="utf-8"` x3 if a campaign change touches this file |
| D2 | Collection errors on `main`: `tests/test_integration_external_repo.py` imports `SkillsOrchestrator` from `sensemaking_skills` (not exported); `tests/test_validate_brief_json.py` loads nonexistent `scripts/validate_brief.py`. Neither file is in any CI gate. | LOCAL_BUT_REAL | deferred; not campaign-limiting |
| D3 | `roadmap.md` stale (0.2.1 / Phase 2.3). Already recorded by evidence 0022. | HISTORICAL_ONLY | no action |
| D4 | `docs/HARDENING_STATUS.md` asserts a 5-type fog taxonomy incl. `integration_fog` (map row SA10). | HISTORICAL_ONLY | no action |

---

## 13. CAMPAIGN ACCEPTANCE STATUS

| # | Condition | Status at R0 | Basis |
|---|---|---|---|
| 1 | Top-level semantic control model explicit and coherent | MET (docs) | CONTEXT.md, boundary doc, ADR 0013 |
| 2 | Role of active coding agent clear | MET | ADR 0013 + amendment |
| 3 | Warrant / responsibility / capability / authority not conflated | MET (docs + fail-closed tests) | ADR 0026/0027, CONTEXT.md non-identities |
| 4 | Durable artifacts can carry continuation state across responsibilities | NOT MET | G1 |
| 5 | One realistic multi-responsibility task continued from durable state without hidden conversation memory | NOT MET | G1; never attempted |
| 6 | Repository-level development direction representable for consequential capability selection | NOT MET (this file is the first attempt) | G2 |
| 7 | Role of deterministic scripts bounded and coherent | LARGELY MET, not consolidated | G5 |
| 8 | Role of hooks defined and evidence-supported | NOT MET | G3 |
| 9 | Old workflow system has a clear disposition | PARTIAL (liveness ratified; campaign-vocabulary disposition absent) | ADR 0027; G4 |
| 10 | Existing useful functionality not destroyed | MET so far (no changes yet) | -- |
| 11 | Tests, validators, contracts, docs, implementation agree sufficiently | PARTIAL | G3, G6, D1/D2 |
| 12 | Repository passes appropriate complete qualification | PENDING (baseline capture in progress) | -- |
| 13 | Remaining material limitations explicitly documented | IN PROGRESS | this file |

Disposition at R0: **CONTINUE**.

---

## 14. Responsibility trace (append-only)

```text
2026-09-02  R0  reconstruction + campaign record v1        -> next: R1
```
