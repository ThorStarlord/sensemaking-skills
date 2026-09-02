# Campaign: reliable agent-native, artifact-mediated self-development

```
STATUS:    ACTIVE development-campaign record (living document, v2 after R1)
AUTHORITY: non-authoritative. Not an ADR, not a contract, not a validator input,
           not a registered workflow, not a research-agenda ratification.
CHARTER:   docs/campaigns/agent-native-self-development/CHARTER.md
           (owner instruction, verbatim; the campaign's authority source)
NOT:       an EXP-NNNN governed experiment campaign (ADR 0023 two-lane machinery
           does not read this file; no approval envelope applies).
READS:     nothing in scripts/, src/, tests/, or .github/ reads this file.
BRANCH:    campaign/agent-native-self-development   (base: main @ f10b7da, 2026-09-02)
WORKTREE:  H:/GithubRepositories/smk-campaign
REMOTE:    see section 15 (push / PR / CI status is recorded there, not assumed)
RULE:      update after every consequential campaign responsibility.
```

This file exists so that campaign reasoning does not live only in one
conversation's context. A fresh coding-agent context should be able to
reconstruct from this file (plus the repository) the mission, the current
capability state, why the current task was selected, what is established, what
is uncertain, what is warranted next, and what authority exists. R1 tested
exactly that (section 8, U1).

---

## 1. CAMPAIGN MISSION

Advance Sensemaking Skills toward **reliable agent-native, artifact-mediated
self-development**: an active coding agent uses repository evidence and durable
artifacts to determine the next warranted engineering responsibility, select an
appropriate capability, perform bounded work, validate the resulting evidence,
preserve authority boundaries, carry state across responsibilities, and
recursively continue until the active goal is satisfied or further action is
unwarranted. Full text, acceptance conditions, stopping rules, and report
format: `CHARTER.md`.

Campaign-level, not a monolithic rewrite. The campaign is controlled directly
by the active coding agent, **not** by `repo-sensemaker`, `using-sensemaking`,
registered workflows, workflow-runtime routing, fog routing, or hooks
(bootstrap constraint). Ordinary repository engineering infrastructure (tests,
validators, `validate-repo.py`, probe engine, CI, git, PRs) is used normally.

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

Campaign vocabulary (defined in `CHARTER.md`, not canonical repository
vocabulary): finding classes `CAMPAIGN_BLOCKING | CAMPAIGN_RELEVANT |
LOCAL_BUT_REAL | HISTORICAL_ONLY | DEFERRED | NO_ACTION_WARRANTED`;
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
| Continuation across responsibilities | **CONVENTION_CLOSED** in the product docs; reopen trigger recorded 2026-08-13. **R1 (this campaign) is the first exercised fresh-context reconstruction**: campaign-level state reconstructed from this record; see U1 | `docs/2026-08-programmatic-runner-retirement-plan.md` "Project closure"; `R1-fresh-context-reconstruction.md` |
| Continuation artifacts that exist | `user_intent` (ADR 0006), `session_summary` (one required field `source_intent_ref`; consumed only by `workflow-planner`), `prompt_handoff` (skill-to-skill prompt packaging for `external_agent`), `work_claim`, `reconciliation_report`, `repair_verification_report`. Adding a new artifact type costs: contract entry + canonical-vocabulary `artifact_ids` entry + packaged mirror + validator (enforced by `tests/test_path_drift.py::test_vocabulary_covers_all_artifacts` and the PR #258 mirror-agreement test) | `skills/workflow-planner/references/artifact-contracts.yaml` ids at lines ~296, ~524, ~709, ~730, ~755; `skills/handoff/SKILL.md`; `docs/canonical-vocabulary.yaml` `artifact_ids:` |
| Repository-level development-direction representation | **ABSENT before this campaign**. `STATUS.md` = version/validation-priority summary; `roadmap.md` = stale rollout plan (0.2.1 / Phase 2.3); `docs/semantic-control-map.md` = authority index under trial (not direction). This record is the first attempt | those files; evidence 0022 already recorded roadmap staleness |
| Deterministic machinery | validators (`validate-output.py` dispatch -> `validate-artifact.py` + specialized), probe engine (`probe-repo.py`, `repo_probes.py`, `probe_relationships.py`), `gate_relationship_findings.py`, `run-ledger.py`, `workflow-runtime.py` (paths/plan/gates/sessions; model executors retired 2026-08-13), `workflow_liveness.py`, `validate-repo.py` | `scripts/`; retirement plan classification tables |
| CI on `main` | 13 jobs in `.github/workflows/validation.yml`: `gate-a-*`, phase 2-6 campaign/execution suites, `validate` (scripts + one pytest file), `probe-gate`, `core-assertions` (7 pytest files incl. `test_path_drift.py`, `test_cli.py`), `conditional-representation-exact-head`. The enforcement gate merged to `main` via PR #169 (`0ffb564`, 2026-08-13). **Last `main` run at base `f10b7da`: Validator Ecosystem `completed/success` (2026-09-02T03:43Z)** | `validation.yml` lines ~602-760; `git log -S core-assertions`; `gh run list --branch main` |
| Hooks | `.claude/hooks/sessionstart.md` is a Markdown description of a SessionStart bootstrap reminder; `.claude/settings.json` is `{}` (no hook wired); skills are discovered because they are copied to `~/.claude/skills/` (`setup_skills.py`; drift tracked by `distribution-drift.yaml`), not by any hook. No continuation/liveness hook exists | those files |
| Real-use evidence of the operating loop | Workflow v0 dogfood on 2 repos (verdict `KEEP_WITH_WATCH_ITEMS`); 3 normal-use episodes recorded as **GitHub issue comments on Issue #218** (by that lane's own policy; not in the repository tree); recurring boundary there: PR-head qualification did not bind the integration base (episodes 002, 003) | `experiments/evidence/0021`, `0022`; `docs/research/normal-use-evidence-lane.md` section 7; Issue #218 |
| Real execution evidence per active workflow (for U4) | run ledgers/mode coverage/evidence exist for: `fast-local-diagnostic`, `full-local-sensemaking`, `full-fog-workflow`, `fast-path-workflow`, `docs-contract-reconciliation` (guided; dogfooded 2026-08, evidence 0018/0019), `architectural-review-planning-workflow` (golden path, 2026-07-25), `docs-architecture`, `setup-sensemaking-repo`, `product-strategy-sprint`, `skill-maintenance-loop`, `docs-implementation-workflow`; `artifact-reconciliation` has agent-native execution evidence (`artifacts/reconciliation_report.md`, 2026-08-22) but no run ledger; `autonomous-sprint-preflight`, `product-discovery-sprint`, `skill-evaluation-workflow` have plan_only or test-only traces | `docs/mode-coverage.yaml`; `artifacts/0[1-4]-orchestration-run/run-ledger.jsonl`; `experiments/evidence/`; `artifacts/reconciliation_report.md` |
| Research lanes (non-ratified) | C6R compressed control hypothesis (#226 open); warrant-as-primitive; uncertainty-selection; PHB meta-finding "sensemaking loops saturated; spikes not briefs" (2026-08-30); semantic-control-map persistence trial OPEN (min close 2026-09-28) | `docs/research/control-model-research-agenda.md`; `docs/semantic-control-map-trial-log.md` |
| Goal A external validation | ACTIVE but **halted in this environment** (three execution substrates falsified; owner halt rule) | Issue #255; evidence 0023 |
| Repository visibility | public (`ThorStarlord/sensemaking-skills`) | `gh repo view` |

Local full-suite baseline (Windows, Python 3.14): see section 12 D1/D2; run in
progress at R1 close-out (first attempt was interrupted by the D2 collection
errors; re-run with `--continue-on-collection-errors`).

---

## 3. COMPLETED CAMPAIGN RESPONSIBILITIES

| # | Responsibility | Result | Evidence |
|---|---|---|---|
| R0 | Reconstruct current product/capability state from durable repository evidence; select first bounded responsibility; establish durable campaign record | this file v1 | commit `2bc8a2c` |
| R1 | Fresh-context reconstruction probe: one cold agent context given only the repo and this file's path answered the seven reconstruction questions | Q1-Q5 `RECONSTRUCTED`; Q6 `PARTIAL` (`AUTHORITY_AMBIGUITY`, narrow); Q7 five omissions, all `MISSING_DURABLE_STATE`; cost 39 files / 25 tool calls. Repairs applied at close-out: charter committed; authority grants sourced (section 11); push/CI status recorded (section 15); G6 corrected to include SE2 | `R1-fresh-context-reconstruction.md` (SHA-256 `9ea98c3b56305743374b7ba3c18a06c387607ee0765759b9f0cc4b854faa2484`, 175 lines, produced verbatim by the probe, not edited by the dispatcher) |

---

## 4. EVIDENCE PRODUCED

- `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (this file).
- `docs/campaigns/agent-native-self-development/CHARTER.md` (owner instruction, verbatim).
- `docs/campaigns/agent-native-self-development/R1-fresh-context-reconstruction.md` (probe output, verbatim).

---

## 5. CURRENTLY DEMONSTRATED CAPABILITIES

(Demonstrated = real use with durable evidence, not merely documented.)

- Agent-native `repository_sensemaking_brief` production + mechanical validation on two structurally different repositories (evidence 0021, 0022).
- Responsibility selection without automatic routing; stop at owner/authority boundary instead of premature implementation (evidence 0022; #218 episodes 001, 003; #255).
- Claim reconciliation (`output-reconciler`) and finding-specific repair verification (`repair-verifier`) (evidence 0018, 0019, 0020; `artifacts/reconciliation_report.md`).
- Fail-closed authority on `auto_invoke_next_workflow` and on compatibility-only workflow selection (ADR 0026/0027 test suites).
- Deterministic probe-engine enforcement in CI (`probe-gate`, `core-assertions`).
- **NEW (R1):** a fresh context reconstructed the campaign mission, capability state, task rationale, established-vs-uncertain split, and next responsibility from this record plus the repository, with no conversation memory (Q1-Q5 `RECONSTRUCTED`).
- **NEW (R1, substrate):** in this harness an isolated sub-agent's direct file write to the worktree persisted (175 lines, hash above). This narrows, for this harness only, the "isolated sub-agent direct write BLOCKED" finding of evidence 0023 / Issue #255; it does not generalize to the Goal A harness without re-verification there.

---

## 6. KNOWN MATERIAL GAPS

| id | Gap | Condition(s) | Class | Status |
|---|---|---|---|---|
| G1 | No durable artifact carried campaign/task-level continuation state before this campaign. **R1 shows reconstruction works from this record.** Not yet shown: a fresh context *performing* a responsibility (mutating under stated authority, validating, committing) from durable state alone | 4, 5 | CAMPAIGN_BLOCKING | NARROWED at R1; R2 targets the remainder |
| G2 | No representation of repository-level development direction that lets an agent select consequential capability work over the nearest local defect | 6 | CAMPAIGN_BLOCKING | this record is the first attempt; R1 Q3 shows a fresh context could derive the selection rationale from it |
| G3 | Role of hooks undefined; documented SessionStart hook not wired (`settings.json = {}`); hook doc prose ("picks correct workflow first try", "auto-fix vs escalate") predates ADR 0026 and the current bootstrap SKILL.md | 8, 11 | CAMPAIGN_RELEVANT | OPEN (gated on U3) |
| G4 | Per-workflow disposition in campaign vocabulary not recorded; ADR 0027 settles liveness, not KEEP/DEMOTE/RETIRE. Execution-evidence inventory now in section 2 | 9 | CAMPAIGN_RELEVANT | OPEN (evidence gathered; disposition doc pending) |
| G5 | Deterministic-script role is described across the retirement plan, the boundary doc, and `CONTEXT.md` but not consolidated. May already be sufficient | 7 | CAMPAIGN_RELEVANT | OPEN (evaluate after G1/G2) |
| G6 | `docs/semantic-control-map.md` rows **SE1, SE2, SA13, SA9** state that `probe-gate`/`core-assertions` exist only on unmerged `feat/enforcement-gate` and that `test_path_drift.py` is red on `main`; the gate merged via PR #169 (`0ffb564`, 2026-08-13), before the trial started, and `main` CI is green at `f10b7da`. Stale-from-construction MECH rows under an OPEN trial; protocol says authoritative source wins and MECH rows are refreshed, not re-decided. `docs/enforcement-contract.md` status line likewise still says "merge awaiting separate authorization" | 11 | CAMPAIGN_RELEVANT | OPEN -> R2 task (the trial bookkeeping is the R2 continuation trial's real task) |
| G7 | Authority grants cited by this record were not sourced in the repository (R1 Q6: "Mode B+", push/PR standing authorization, who may implement candidate machinery on the branch) | 5, 13 | CAMPAIGN_RELEVANT | REPAIRED at R1 close-out: `CHARTER.md` committed; section 11 sources every grant; out-of-repo prior instructions are no longer cited |
| G8 | Some evidence this record cites lives only in GitHub (Issue #218 episode comments, Issue #255 state, CI run results). That is the normal-use lane's own policy (issue comments), not a defect, but a fresh context without GitHub access cannot reconstruct it | 5, 13 | DEFERRED | documented limitation; record marks such items "GitHub-only" |

---

## 7. ACTIVE CONSTRAINTS

- C1 **Bootstrap constraint** (`CHARTER.md`): this campaign does not use `repo-sensemaker`, `using-sensemaking`, registered workflows, runtime routing, fog routing, Skill-to-Skill continuation mechanisms under evaluation, or hooks as its controller.
- C2 **Authority** (sources in section 11): push branches and open PRs for exact-head qualification (charter); merge to `main`, ADR acceptance, canonical contract/registry ratification, and external tracker writes are **owner** actions. Never falsify owner decisions or ADR `**Status**` lines.
- C3 **Semantic-control-map trial is OPEN** (`docs/semantic-control-map-trial.md`): do not add rows (`MAP_EXPANSION_DEFAULT = NO`); MECH rows are refreshed on triggers, not re-decided; JUDG/INTERP text is reviewed only on a plausible trigger; record consultation/over-read events in the trial log.
- C4 **Goal A is halted** in this environment (#255); do not run Goal A episodes. Issue #218 episodes are recorded only when they arise from ordinary work, and only by an owner-authorized tracker write.
- C5 **Windows cp1252**: console output ASCII-only; file reads in tests need explicit encoding.
- C6 **Worktree per session**: all campaign work in `H:/GithubRepositories/smk-campaign`; never the shared `main` checkout.
- C7 **Machinery promotion rule** (repository; `docs/agent-native-operating-workflow.md` section 7): repeated useful responsibility + stable semantics + repeated burden/error + mechanically expressible boundary -> candidate for formalization. Not: "there is a box in the diagram".
- C8 **One responsibility at a time** (charter): while a fresh-context trial runs, the dispatcher does not edit files the trial may read and does not open a second responsibility.

---

## 8. OPEN DECISION-CHANGING UNCERTAINTIES

| id | Uncertainty | Source | Cheapest sufficient evidence | Status |
|---|---|---|---|---|
| U1 | What continuation state does a fresh context fail to reconstruct from durable state, and in which failure class? | empirical | R1 | **RESOLVED (R1).** Q1-Q5 reconstructed. Shortfalls: `AUTHORITY_AMBIGUITY` (narrow: unsourced "Mode B+", push/PR standing grant, who authorizes branch-local implementation of candidate machinery) and `MISSING_DURABLE_STATE` (charter conversation-only; push/CI status unrecorded; GitHub-only evidence unmarked). Not observed: `CAPABILITY_DISCOVERY_FAILURE`, `PRODUCT_DIRECTION_AMBIGUITY`, `INCIDENTAL_CONTEXT_LOSS`; only a mild `WARRANT_AMBIGUITY` about the task after next. All repairable by making the missing state durable (done at close-out, except G8 by design) |
| U2 | Do the outer loop (repository-evolution) and the inner loop (task-execution) need different durable state, or does one record suffice? | repository_evidence + trace | one real multi-step task performed by a fresh context from durable state (R2); compare what it needed beyond this record | OPEN -> R2 |
| U3 | Is any hook warranted beyond a documented bootstrap? (liveness only: detect artifact -> validate -> register state -> wake agent) | empirical | only after U2/U6 show a recurrent continuation event that a manual step keeps missing | OPEN, gated |
| U4 | Which registered workflows have enough real traces for a disposition other than `INSUFFICIENT_EVIDENCE`? | repository_evidence | execution-evidence inventory (section 2) -> disposition doc | EVIDENCE GATHERED; disposition pending |
| U5 | Should continuation state ride on `session_summary` / `prompt_handoff` (existing contracts) or a new artifact type, or remain a Markdown record with no contract? | repository_evidence | decided by U2 result + the cost of a new artifact type (section 2) | OPEN, gated on U2 |
| U6 | Can a fresh context, given only this record, correctly **perform** a bounded multi-step task (authority-respecting mutation, validation, commit) rather than only reconstruct? | empirical | R2 | OPEN -> R2 |

---

## 9. CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

**Continuation-and-execution from durable state** (G1 remainder, U2, U6). R1
established reconstruction; condition 5 requires a realistic multi-responsibility
task actually continued and performed from durable state. Conditions 1-3 are met
at the documentation level; 8 and 9 depend on traces bounded work will produce;
10-13 are end-of-campaign qualification.

---

## 10. CURRENT / NEXT WARRANTED RESPONSIBILITY

```text
R2  Continuation-and-execution trial
    (a fresh context performs an ordinary multi-step task from durable state only)

CAMPAIGN CAPABILITY AFFECTED:   artifact-mediated continuation (conditions 4, 5);
                                inner-loop state shape (U2); execution from durable
                                state (U6)
CURRENT LIMITATION:             R1 proved reconstruction, not execution. No fresh
                                context has yet performed a responsibility, mutated
                                files under stated authority, validated, and
                                committed from durable state alone
WHY IT MATTERS TO THE MISSION:  condition 5 verbatim; also the cheapest evidence for
                                U2/U5 (what task-level state a fresh context needs
                                beyond this record)
BOUNDED RESPONSIBILITY:         R2's task is the G6 semantic-control-map trial
                                bookkeeping -- an ordinary, protocol-permitted,
                                multi-step task that arose from real work in R0
                                (it was NOT manufactured for the trial). Steps:
  1. read docs/semantic-control-map-trial.md (protocol) and
     docs/semantic-control-map-trial-log.md; read rows SE1, SE2, SA13, SA9 in
     docs/semantic-control-map.md;
  2. establish from git that the enforcement gate (probe-gate + core-assertions
     in .github/workflows/validation.yml) reached main via PR #169
     (0ffb564, 2026-08-13), i.e. before the trial start commit df46871
     (2026-08-31), so the rows were stale from construction;
  3. MECH-refresh rows SE1, SE2, SA13, SA9 per the protocol's refresh procedure:
     run `python scripts/probe-repo.py --repo-root . --output <temp file>`;
     run `python -m pytest tests/test_path_drift.py tests/test_cli.py -q` and
     record whether any red is a known red (protocol names SE2/SA12; this
     record's D1 names the Windows cp1252 read_text failure) or new. Do NOT add
     rows; do NOT change JUDG/INTERP text; keep each row's id, Grade, Rate,
     Deriv columns; correct only the stale facts and their evidence pointers;
  4. append to docs/semantic-control-map-trial-log.md: section A (trigger:
     validation.yml changed before trial start; rows stale from construction),
     section B (actual minutes for this MECH refresh), section C (consultation:
     R0 of this campaign consulted SE1/SA13 during ordinary reconstruction;
     outcome "revealed conflict"), section D (over-read: R0 initially took SE1
     as current before checking validation.yml on main; consequence: none,
     caught before use);
  5. add one dated status addendum block at the top of
     docs/enforcement-contract.md (no rewrite) stating the branch merged to
     main via PR #169 (0ffb564, 2026-08-13) and both jobs are present on main;
  6. run `python scripts/validate-repo.py`; inspect `git diff --stat`; commit on
     branch campaign/agent-native-self-development with subject prefix
     `campaign(R2):` and trailer
     `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`;
     do NOT push; do NOT edit CAMPAIGN-STATE.md (the dispatcher updates it after
     auditing R2);
  7. write docs/campaigns/agent-native-self-development/R2-continuation-trial.md
     (may be in the same commit or a second `campaign(R2):` commit): what this
     record was sufficient for; what was missing; every file consulted beyond
     this record and why; tool-call count; any authority question that arose
     and how it was resolved; any step skipped and why.
AUTHORITY FOR R2 (sourced):     CHARTER.md (owner instruction: use ordinary
                                engineering infrastructure; commit per bounded
                                responsibility); docs/semantic-control-map-trial.md
                                "Row maintenance" (MECH rows are refreshed, not
                                re-decided; on conflict the authoritative source
                                wins and the row is stale -> fix it) -- so editing
                                those four rows and appending to the log is
                                protocol-authorized; the enforcement-contract
                                addendum is reversible branch-local documentation
                                reconciliation (not an ADR, not a contract).
NOT AUTHORIZED IN R2:           adding map rows; editing JUDG/INTERP text; editing
                                ADRs, artifact contracts, registries, validators,
                                tests, scripts; pushing; merging; external tracker
                                writes; editing CAMPAIGN-STATE.md.
STOP CONDITION:                 commit(s) exist + R2 report written; OR a
                                precondition fails (e.g. the probe engine cannot
                                run) -- then write the report describing the
                                failure and stop without partial map edits.
EXPECTED EVIDENCE OF PROGRESS:  commit(s) `campaign(R2): ...`;
                                R2-continuation-trial.md; dispatcher audit (claim
                                reconciliation of R2's diff against the trial
                                protocol) recorded in this file; U2 and U6
                                narrowed or resolved; G6 closed.
```

---

## 11. AUTHORITY: GRANTS, THEIR SOURCES, AND OWNER DECISIONS REQUIRED

Every authority claim this campaign relies on, with its durable source. Prior
out-of-repository instructions (e.g. agent memory of earlier owner delegations)
are **not** cited as authority.

| Grant / boundary | Source |
|---|---|
| Own the campaign end to end: diagnosis, implementation, qualification, closure, on the campaign branch; continue autonomously through multiple bounded tasks | `CHARTER.md` "Campaign Mission" |
| Use ordinary engineering infrastructure (tests, validators, probe engine, git, GitHub CI, PRs) | `CHARTER.md` "Important Bootstrap Constraint" |
| Push branches / open PRs; qualify exact PR heads | `CHARTER.md` "Git and Change Discipline" ("one coherent commit or PR per bounded responsibility"; "qualified PR head") |
| Branch-local implementation of reversible, non-ratified candidate machinery is agent-decidable; ratification is not | `CONTEXT.md` "Authority model" (Can DECIDE: reversible implementation details within scope); `CHARTER.md` "Architecture Discipline" |
| Merge to `main` = owner | repository convention: ADR 0014/0026/0027 headers record owner ratification and separate merge actions; `docs/adr/README.md`; `CONTEXT.md` non-identities (`promoted != merged`); the charter grants no merge authority |
| ADR status / owner decisions must not be falsified | `docs/adr/README.md`; `AGENTS.md` rule 5 |
| External tracker writes (issue comments, labels) require explicit authority | `docs/agent-native-operating-workflow.md` section 4 (ADR 0019 PROPOSED) |
| Ask the owner only for product preference, authority expansion, irreversible tradeoffs, external environment, or material product-direction acceptance | `CHARTER.md` "Owner Decisions" |

Owner decisions required (none blocking the next responsibility):

1. **Merge authority for the campaign PR(s)** -- standing; the campaign can
   stack responsibilities on its branch without integration until closure.
2. **Whether to record the R1 substrate observation on Issue #255** (an external
   tracker write): in this harness an isolated sub-agent's direct worktree write
   persisted. Recommended but not required; the observation is durable here.

---

## 12. DEFERRED NON-CAMPAIGN FINDINGS

| id | Finding | Class | Disposition |
|---|---|---|---|
| D1 | `tests/test_path_drift.py:154,228,358` call `read_text()` without `encoding`; on Windows cp1252 this raises `UnicodeDecodeError` on `skills/architectural-review/SKILL.md` (byte 0x9d). Linux CI (utf-8) unaffected: `core-assertions` is green on `main` | LOCAL_BUT_REAL | deferred; one-line `encoding="utf-8"` x3 if a campaign change touches this file |
| D2 | Collection errors on `main`: `tests/test_integration_external_repo.py` imports `SkillsOrchestrator` from the package root (class lives in `runner.py`, not re-exported); `tests/test_validate_brief_json.py` loads nonexistent `scripts/validate_brief.py`. Neither file is in any CI gate | LOCAL_BUT_REAL | deferred; not campaign-limiting |
| D3 | `roadmap.md` stale (0.2.1 / Phase 2.3). Already recorded by evidence 0022 | HISTORICAL_ONLY | no action |
| D4 | `docs/HARDENING_STATUS.md` asserts a 5-type fog taxonomy incl. `integration_fog` (map row SA10) | HISTORICAL_ONLY | no action |
| D5 | `docs/candidate/architecture-decision.md:7` links to nonexistent `docs/prototypes/repo-sensemaker-vnext.md` (candidate-branch snapshot) | HISTORICAL_ONLY | no action |
| D6 | `unevaluable` verdict category for `repair_verification_report` is proposed in the operating workflow v0 but not in the contract | DEFERRED | needs a real case; not campaign-limiting |
| D7 | `docs/research/normal-use-evidence-lane.md` section 12 says "new episodes 0" -- it is explicitly a snapshot "at establishment", not a stale claim | NO_ACTION_WARRANTED | none |

---

## 13. CAMPAIGN ACCEPTANCE STATUS

| # | Condition | Status after R1 | Basis |
|---|---|---|---|
| 1 | Top-level semantic control model explicit and coherent | MET (docs) | CONTEXT.md, boundary doc, ADR 0013; R1 Q1/Q2 confirm a fresh context reads it that way |
| 2 | Role of active coding agent clear | MET | ADR 0013 + amendment |
| 3 | Warrant / responsibility / capability / authority not conflated | MET (docs + fail-closed tests) | ADR 0026/0027, CONTEXT.md non-identities |
| 4 | Durable artifacts can carry continuation state across responsibilities | PARTIAL | R1: campaign-level state reconstructed from this record; execution from it not yet shown (R2) |
| 5 | One realistic multi-responsibility task continued from durable state without hidden conversation memory | NOT MET | R2 is the first attempt |
| 6 | Repository-level development direction representable for consequential capability selection | PARTIAL | this record; R1 Q3 shows the selection rationale is derivable from it; not yet shown across more than one responsibility |
| 7 | Role of deterministic scripts bounded and coherent | LARGELY MET, not consolidated | G5 |
| 8 | Role of hooks defined and evidence-supported | NOT MET | G3; U3 gated |
| 9 | Old workflow system has a clear disposition | PARTIAL | ADR 0027 (liveness); execution-evidence inventory in section 2; disposition doc pending (G4) |
| 10 | Existing useful functionality not destroyed | MET so far (docs-only changes) | -- |
| 11 | Tests, validators, contracts, docs, implementation agree sufficiently | PARTIAL | G3, G6 (-> R2), D1/D2 |
| 12 | Repository passes appropriate complete qualification | PARTIAL | `main` CI green at base `f10b7da`; campaign PR not yet opened; local full-suite baseline in progress |
| 13 | Remaining material limitations explicitly documented | IN PROGRESS | this file (G8 added) |

Disposition after R1: **CONTINUE** (R2).

---

## 14. Responsibility trace (append-only)

```text
2026-09-02  R0  reconstruction + campaign record v1                     -> next: R1
2026-09-02  R1  fresh-context reconstruction probe (Q1-Q5 ok; Q6 partial;
                5 omissions, repaired at close-out; record v2)          -> next: R2
```

---

## 15. Remote / integration status (updated by the dispatcher, never assumed)

```text
pushed:        not yet (as of R1 close-out; push follows the R1 commit)
PR:            none yet
last main CI:  Validator Ecosystem completed/success @ f10b7da (2026-09-02T03:43Z)
campaign CI:   none yet (no PR)
merged:        nothing (owner decision)
```
