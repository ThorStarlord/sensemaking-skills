# Campaign: reliable agent-native, artifact-mediated self-development

```
STATUS:    ACTIVE development-campaign record (living document, v3 after R2)
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
RULE:      update after every consequential campaign responsibility. Facts in
           this file are claims; task specs include verification steps so a
           continuing context can catch errors here (R2 did: see F1).
```

This file exists so that campaign reasoning does not live only in one
conversation's context. Two fresh contexts have so far continued the campaign
from this file alone: R1 (reconstruction) and R2 (execution). See section 8.

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

Operating pattern used since R1: the dispatcher context specifies the next
responsibility in section 10, commits, and dispatches a **fresh context** that
receives only this file's path; the fresh context performs the responsibility
and writes `Rn-*.md`; the dispatcher audits the diff against the spec
(claim reconciliation), updates this file, commits, pushes.

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
| Continuation across responsibilities | Product docs say **CONVENTION_CLOSED** (cross-run prior-report identity unresolved, reopen trigger recorded 2026-08-13). **This campaign demonstrated responsibility-level continuation from a durable Markdown record**: R1 reconstructed campaign state; R2 performed a multi-step task, validated, committed, and caught a factual error in the record. The product's operating map does not yet reflect this (G9 -> R3) | `docs/2026-08-programmatic-runner-retirement-plan.md` "Project closure"; `R1-fresh-context-reconstruction.md`; `R2-continuation-trial.md` |
| Continuation artifacts that exist | `user_intent` (ADR 0006), `session_summary` (one required field `source_intent_ref`; consumed only by `workflow-planner`), `prompt_handoff` (skill-to-skill prompt packaging for `external_agent`), `work_claim`, `reconciliation_report`, `repair_verification_report`. Adding a new artifact type costs: contract entry + canonical-vocabulary `artifact_ids` entry + packaged mirror + validator (enforced by `tests/test_path_drift.py::test_vocabulary_covers_all_artifacts` and the PR #258 mirror-agreement test) | `skills/workflow-planner/references/artifact-contracts.yaml` ids at lines ~296, ~524, ~709, ~730, ~755; `skills/handoff/SKILL.md`; `docs/canonical-vocabulary.yaml` `artifact_ids:` |
| Repository-level development-direction representation | **ABSENT before this campaign**. `STATUS.md` = version/validation-priority summary; `roadmap.md` = stale rollout plan (0.2.1 / Phase 2.3); `docs/semantic-control-map.md` = authority index under trial (not direction). This record is the first representation; R1 Q3 and R2 show a fresh context can select and perform the named responsibility from it | those files; evidence 0022 already recorded roadmap staleness |
| Deterministic machinery | validators (`validate-output.py` dispatch -> `validate-artifact.py` + specialized), probe engine (`probe-repo.py`, `repo_probes.py`, `probe_relationships.py`), `gate_relationship_findings.py`, `run-ledger.py`, `workflow-runtime.py` (paths/plan/gates/sessions; model executors retired 2026-08-13), `workflow_liveness.py`, `validate-repo.py` | `scripts/`; retirement plan classification tables |
| CI on `main` | 13 jobs in `.github/workflows/validation.yml`: `gate-a-*`, phase 2-6 campaign/execution suites, `validate` (scripts + one pytest step), `probe-gate`, `core-assertions` (7 pytest files incl. `test_path_drift.py`, `test_cli.py`), `conditional-representation-exact-head`. **Provenance (corrected at R2 close-out; R2 F1):** the enforcement gate commit `e1db7dc` (2026-08-11, `feat/enforcement-gate` tip) is on `main`'s first-parent line -- no merge commit, no PR; the PR #169 merge `0ffb564` (2026-08-13) merely already contained it. `main` CI green at trial start `df46871` (run 33422969527) and at base `f10b7da` (run 33588124719, 2026-09-02T03:43Z) | `validation.yml`; `git log --first-parent`; `gh run list --branch main` |
| Hooks | `.claude/hooks/sessionstart.md` is a Markdown description of a SessionStart bootstrap reminder; `.claude/settings.json` is `{}` (no hook wired); skills are discovered because they are copied to `~/.claude/skills/` (`setup_skills.py`; drift tracked by `distribution-drift.yaml`), not by any hook. No continuation/liveness hook exists. R1/R2 continuation events were handled by explicit dispatch + durable record; no missed event observed | those files; R1/R2 reports |
| Real-use evidence of the operating loop | Workflow v0 dogfood on 2 repos (verdict `KEEP_WITH_WATCH_ITEMS`); 3 normal-use episodes recorded as **GitHub issue comments on Issue #218** (by that lane's own policy; not in the repository tree); recurring boundary there: PR-head qualification did not bind the integration base (episodes 002, 003) | `experiments/evidence/0021`, `0022`; `docs/research/normal-use-evidence-lane.md` section 7; Issue #218 |
| Real execution evidence per active workflow (for U4) | run ledgers/mode coverage/evidence exist for: `fast-local-diagnostic`, `full-local-sensemaking`, `full-fog-workflow`, `fast-path-workflow`, `docs-contract-reconciliation` (guided; dogfooded 2026-08, evidence 0018/0019), `architectural-review-planning-workflow` (golden path, 2026-07-25), `docs-architecture`, `setup-sensemaking-repo`, `product-strategy-sprint`, `skill-maintenance-loop`, `docs-implementation-workflow`; `artifact-reconciliation` has agent-native execution evidence (`artifacts/reconciliation_report.md`, 2026-08-22) but no run ledger; `autonomous-sprint-preflight`, `product-discovery-sprint`, `skill-evaluation-workflow` have plan_only or test-only traces | `docs/mode-coverage.yaml`; `artifacts/0[1-4]-orchestration-run/run-ledger.jsonl`; `experiments/evidence/`; `artifacts/reconciliation_report.md` |
| Research lanes (non-ratified) | C6R compressed control hypothesis (#226 open); warrant-as-primitive; uncertainty-selection; PHB meta-finding "sensemaking loops saturated; spikes not briefs" (2026-08-30); semantic-control-map persistence trial OPEN (min close 2026-09-28) -- this campaign supplied its first consultation, over-read, and MECH-refresh events (R0/R2) | `docs/research/control-model-research-agenda.md`; `docs/semantic-control-map-trial-log.md` |
| Goal A external validation | ACTIVE but **halted in this environment** (three execution substrates falsified; owner halt rule) | Issue #255; evidence 0023 |
| Repository visibility | public (`ThorStarlord/sensemaking-skills`) | `gh repo view` |

Local full-suite baseline (Windows, Python 3.14): see section 12 D1/D2; the
verbose re-run is in progress at R2 close-out (the first `-q` run hung at 59%
with no output for 14 minutes and was killed; the hanging test is to be
identified from the `-v` log).

---

## 3. COMPLETED CAMPAIGN RESPONSIBILITIES

| # | Responsibility | Result | Evidence |
|---|---|---|---|
| R0 | Reconstruct current product/capability state from durable repository evidence; select first bounded responsibility; establish durable campaign record | this file v1 | commit `2bc8a2c` |
| R1 | Fresh-context reconstruction probe: one cold agent context given only the repo and this file's path answered the seven reconstruction questions | Q1-Q5 `RECONSTRUCTED`; Q6 `PARTIAL` (`AUTHORITY_AMBIGUITY`, narrow); Q7 five omissions, all `MISSING_DURABLE_STATE`; cost 39 files / 25 tool calls. Repairs at close-out: charter committed; authority sourced (section 11); push/CI status recorded (section 15); G6 corrected | `R1-fresh-context-reconstruction.md` (SHA-256 `9ea98c3b...`, 175 lines, verbatim); commit `b4335c3` |
| R2 | Continuation-and-execution trial: a fresh context performed the G6 semantic-control-map trial bookkeeping from this file alone (7 steps: protocol read, git provenance check, MECH refresh of SE1/SE2/SA13/SA9 with probe run + pytest, trial-log A-D entries, enforcement-contract addendum, validate-repo + commit, report) | All 7 steps performed; diff = 3 files +29/-6, exactly the 4 rows + log + addendum; `validate-repo.py` exit 0 (re-verified by dispatcher); **caught a factual error in this record** (F1: gate provenance) via the spec's own verification step and wrote the git-established facts instead; 2 protocol defects + 2 more stale rows flagged, not acted on (conservative reading of scope). Cost 9 files / 36 tool calls / ~15 min. **Dispatcher audit: all claims VERIFIED** (independent `git log --first-parent`, `merge-base`, `gh run list --commit df46871`; diff inspected row by row; no unauthorized surface touched) | `R2-continuation-trial.md` (verbatim); commits `fa2dd68`, `9160a5b` |
| R2 close-out (dispatcher) | Audit; follow-up MECH refresh of SA10/SA12 (R2 F2) and protocol selector fix (R2 F3), logged in trial log B; record v3 | this commit | see section 14 |

---

## 4. EVIDENCE PRODUCED

- `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (this file).
- `docs/campaigns/agent-native-self-development/CHARTER.md` (owner instruction, verbatim).
- `docs/campaigns/agent-native-self-development/R1-fresh-context-reconstruction.md` (probe output, verbatim).
- `docs/campaigns/agent-native-self-development/R2-continuation-trial.md` (trial report, verbatim).
- Product-side changes so far (docs only): `docs/semantic-control-map.md` rows SE1/SE2/SA13/SA9 (R2) + SA10/SA12 (close-out) MECH-refreshed; `docs/semantic-control-map-trial-log.md` sections A-D populated with real events; `docs/semantic-control-map-trial.md` step-4 selector corrected; `docs/enforcement-contract.md` dated status addendum.

---

## 5. CURRENTLY DEMONSTRATED CAPABILITIES

(Demonstrated = real use with durable evidence, not merely documented.)

- Agent-native `repository_sensemaking_brief` production + mechanical validation on two structurally different repositories (evidence 0021, 0022).
- Responsibility selection without automatic routing; stop at owner/authority boundary instead of premature implementation (evidence 0022; #218 episodes 001, 003; #255).
- Claim reconciliation (`output-reconciler`) and finding-specific repair verification (`repair-verifier`) (evidence 0018, 0019, 0020; `artifacts/reconciliation_report.md`).
- Fail-closed authority on `auto_invoke_next_workflow` and on compatibility-only workflow selection (ADR 0026/0027 test suites).
- Deterministic probe-engine enforcement in CI (`probe-gate`, `core-assertions`).
- **(R1)** A fresh context reconstructed the campaign mission, capability state, task rationale, established-vs-uncertain split, and next responsibility from this record plus the repository, with no conversation memory.
- **(R2)** A fresh context **performed** a seven-step, three-file responsibility from this record alone: respected every authority boundary (incl. declining unlisted-but-plausible edits), ran the named validators, committed with the required convention, wrote a candid report, and **corrected a wrong fact in the record from git evidence** because the spec required verification rather than trust.
- **(R1, substrate)** In this harness an isolated sub-agent's direct file write to the worktree persisted (R1: 175 lines; R2: 4 files + 2 commits). Narrows, for this harness only, the "isolated sub-agent direct write BLOCKED" finding of evidence 0023 / Issue #255.

---

## 6. KNOWN MATERIAL GAPS

| id | Gap | Condition(s) | Class | Status |
|---|---|---|---|---|
| G1 | No durable artifact carried campaign/task-level continuation state before this campaign. R1 (reconstruction) and R2 (execution) now demonstrate continuation from this record for **documentation-level** responsibilities. Not yet shown: an implementation-class responsibility (code + tests) performed by a fresh context from durable state | 4, 5 | CAMPAIGN_RELEVANT (was BLOCKING) | NARROWED; U7 |
| G2 | No representation of repository-level development direction that lets an agent select consequential capability work over the nearest local defect | 6 | CAMPAIGN_RELEVANT (was BLOCKING) | this record; fresh contexts selected and performed the named responsibility (R1 Q3, R2) |
| G3 | Role of hooks undefined; documented SessionStart hook not wired (`settings.json = {}`); hook doc prose ("picks correct workflow first try", "auto-fix vs escalate") predates ADR 0026 and the current bootstrap SKILL.md | 8, 11 | CAMPAIGN_RELEVANT | OPEN (U3: R1/R2 supplied the first evidence -- no missed continuation event) |
| G4 | Per-workflow disposition in campaign vocabulary not recorded; ADR 0027 settles liveness, not KEEP/DEMOTE/RETIRE. Execution-evidence inventory in section 2 | 9 | CAMPAIGN_RELEVANT | OPEN (evidence gathered; disposition doc pending) |
| G5 | Deterministic-script role is described across the retirement plan, the boundary doc, and `CONTEXT.md` but not consolidated. May already be sufficient | 7 | CAMPAIGN_RELEVANT | OPEN (evaluate with R3) |
| G6 | Semantic-control-map rows SE1/SE2/SA13/SA9 (and SA10/SA12) stale from construction; enforcement-contract status line stale | 11 | CAMPAIGN_RELEVANT | **CLOSED** (R2 + close-out; trial-log A-D record the events) |
| G7 | Authority grants cited by this record were not sourced in the repository (R1 Q6) | 5, 13 | CAMPAIGN_RELEVANT | **CLOSED** at R1 close-out (`CHARTER.md`; section 11) |
| G8 | Some evidence this record cites lives only in GitHub (Issue #218 episode comments, Issue #255 state, CI run results). That is the normal-use lane's own policy, not a defect, but a fresh context without GitHub access cannot reconstruct it. R2 handled it correctly (used `gh` read-only and said so) | 5, 13 | DEFERRED | documented limitation |
| G9 | **The product's own operating map does not represent the continuation pattern this campaign demonstrated.** `docs/agent-native-operating-workflow.md` "CONTINUATION" and its Reality map row still describe continuation as `CONVENTION_CLOSED` with an untested reopen trigger; a product user (not this campaign) would find no description of what durable state a fresh context needs, what was observed to fail, or what was found unnecessary (schema, validator, hook). Until reconciled, conditions 4/6/11 are met only inside the campaign directory | 4, 6, 11 | CAMPAIGN_BLOCKING | OPEN -> R3 |

---

## 7. ACTIVE CONSTRAINTS

- C1 **Bootstrap constraint** (`CHARTER.md`): this campaign does not use `repo-sensemaker`, `using-sensemaking`, registered workflows, runtime routing, fog routing, Skill-to-Skill continuation mechanisms under evaluation, or hooks as its controller.
- C2 **Authority** (sources in section 11): the dispatcher pushes branches and opens PRs for exact-head qualification (charter); fresh-context responsibilities commit locally and do not push; merge to `main`, ADR acceptance, canonical contract/registry ratification, and external tracker writes are **owner** actions. Never falsify owner decisions or ADR `**Status**` lines.
- C3 **Semantic-control-map trial is OPEN** (`docs/semantic-control-map-trial.md`): do not add rows (`MAP_EXPANSION_DEFAULT = NO`); MECH rows are refreshed on triggers, not re-decided; JUDG/INTERP text is reviewed only on a plausible trigger; record consultation/over-read events in the trial log.
- C4 **Goal A is halted** in this environment (#255); do not run Goal A episodes. Issue #218 episodes are recorded only when they arise from ordinary work, and only by an owner-authorized tracker write.
- C5 **Windows cp1252**: console output ASCII-only; file reads in tests need explicit encoding; run pytest with `PYTHONUTF8=1` to distinguish encoding reds from real reds.
- C6 **Worktree per session**: all campaign work in `H:/GithubRepositories/smk-campaign`; never the shared `main` checkout.
- C7 **Machinery promotion rule** (repository; `docs/agent-native-operating-workflow.md` section 7): repeated useful responsibility + stable semantics + repeated burden/error + mechanically expressible boundary -> candidate for formalization. Not: "there is a box in the diagram".
- C8 **One responsibility at a time** (charter): while a fresh-context responsibility runs, the dispatcher does not edit files it may read and does not open a second responsibility.
- C9 **Task specs must contain verification steps, not only assertions** (learned in R2: the spec's "establish from git" step is what caught the record's wrong fact). A fresh context is told to prefer repository evidence over this record where they conflict, and to flag rather than silently correct.

---

## 8. OPEN DECISION-CHANGING UNCERTAINTIES

| id | Uncertainty | Source | Cheapest sufficient evidence | Status |
|---|---|---|---|---|
| U1 | What continuation state does a fresh context fail to reconstruct from durable state, and in which failure class? | empirical | R1 | **RESOLVED (R1).** Q1-Q5 reconstructed. Shortfalls: `AUTHORITY_AMBIGUITY` (narrow) and `MISSING_DURABLE_STATE`; both repaired by making state durable |
| U2 | Do the outer loop (repository-evolution) and the inner loop (task-execution) need different durable state, or does one record suffice? | repository_evidence + trace | R2 trace | **NARROWED (R2).** One file carried both without conflict: sections 6-10 were the outer-loop rationale; the numbered step spec in section 10 (with verification steps, sourced authority, explicit not-authorized list, stop condition, expected evidence) was the inner-loop state. Beyond the record, R2 needed only repository state named by the record (protocol, map conventions, git/CI facts) -- no conversation state. Holds for docs-level tasks; untested for implementation-class tasks (U7) |
| U3 | Is any hook warranted beyond a documented bootstrap? (liveness only: detect artifact -> validate -> register state -> wake agent) | empirical | recurrent continuation event that a manual step keeps missing | OPEN; R1/R2: none observed -- both continuation events were explicit dispatches, and the durable record + report sufficed. Current evidence does not warrant a hook |
| U4 | Which registered workflows have enough real traces for a disposition other than `INSUFFICIENT_EVIDENCE`? | repository_evidence | execution-evidence inventory (section 2) -> disposition doc | EVIDENCE GATHERED; disposition pending (G4) |
| U5 | Should continuation state ride on `session_summary` / `prompt_handoff`, a new artifact type, or remain a Markdown record with no contract? | repository_evidence | U2 result + cost of a new artifact type | **DECIDED FOR NOW: Markdown record convention, no new artifact type, no validator.** Rationale: three continuations, zero shape errors, one fact error (caught by a verification step, which no schema would have caught); a new artifact type costs contract + vocabulary + mirror + validator (section 2) and C7 is not met. Reopen if a fresh context fails on a *missing or malformed section* rather than a wrong fact, or if more than one dispatcher must produce such records |
| U6 | Can a fresh context, given only this record, correctly **perform** a bounded multi-step task (authority-respecting mutation, validation, commit) rather than only reconstruct? | empirical | R2 | **RESOLVED (R2): yes**, including declining plausible-but-unlisted edits and correcting the record from evidence |
| U7 | Does the pattern hold for an implementation-class responsibility (code + tests + CI) performed by a fresh context from durable state? | empirical | dispatch one such responsibility when the campaign next warrants code (G3 hook-doc repair or a validator change are candidates) | OPEN |

---

## 9. CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

**The product's operating map must represent the demonstrated continuation
pattern** (G9). The capability exists and is evidenced inside
`docs/campaigns/`, but the product surface a user's agent reads
(`docs/agent-native-operating-workflow.md`, `CONTEXT.md`) still says
continuation is closed-by-convention and untested. Reconciling that is the
smallest change that makes the product itself, not just this campaign,
"materially more coherent and capable" on the mission's central property.

---

## 10. CURRENT / NEXT WARRANTED RESPONSIBILITY

```text
R3  Continuation-pattern reconciliation into the product operating map
    (documentation reconciliation; performed by a fresh context from this record)

CAMPAIGN CAPABILITY AFFECTED:   artifact-mediated continuation as a PRODUCT
                                property (conditions 4, 6, 11); also condition 7
                                (deterministic-script role) and 8 (hooks) get
                                their evidence sentence
CURRENT LIMITATION:             docs/agent-native-operating-workflow.md section 2
                                "CONTINUATION" and section 5 Reality map row
                                "Continuation" describe CONVENTION_CLOSED with an
                                untested reopen trigger; nothing in the product
                                docs says what durable state a fresh context needs
                                or what was found unnecessary
WHY IT MATTERS TO THE MISSION:  the mission's central property is now evidenced
                                only inside the campaign directory; the product's
                                own map must carry it or the campaign has changed
                                nothing a user's agent can read
BOUNDED RESPONSIBILITY:         steps for the fresh context:
  1. read this file; R1-fresh-context-reconstruction.md; R2-continuation-trial.md
     (sections "Summary", "1", "2", "6 F7"); docs/agent-native-operating-workflow.md
     in full; docs/2026-08-programmatic-runner-retirement-plan.md section
     "Project closure" (the CONVENTION_CLOSED source); CONTEXT.md section "Stop and
     continuation conditions"; skills/using-sensemaking/SKILL.md section 14.
  2. VERIFY before writing: (a) that the operating map's CONTINUATION text and
     Reality map row still read as described above (quote the lines you will
     change); (b) that the retirement plan's reopen trigger is about cross-run
     PRIOR-REPORT IDENTITY, which R1/R2 did NOT exercise -- keep that item
     unresolved; do not claim it closed; (c) the R1/R2 facts you cite against the
     two report files, not against this record.
  3. edit docs/agent-native-operating-workflow.md only:
     (a) section 2 "CONTINUATION": keep the desired principle and the current
         cross-run-identity status verbatim; ADD a dated subsection
         "Responsibility-level continuation from a durable record (demonstrated
         2026-09-02)" that states, from R1/R2 evidence: what a fresh context
         reconstructed and performed; the durable state that proved necessary
         (mission; capability-state table with evidence pointers; gaps; sourced
         authority incl. an explicit not-authorized list; a task spec with
         numbered steps, verification steps, stop condition, expected evidence;
         open uncertainties; deferred findings; remote/integration status;
         append-only trace); the failure classes observed and how each was
         repaired (AUTHORITY_AMBIGUITY -> source every grant; MISSING_DURABLE_STATE
         -> commit the authority text, record push/CI status, mark GitHub-only
         evidence); what was NOT needed at this scale (schema, validator, new
         artifact type, hook) and the reopen conditions from U5/U3 in this file;
         the observed limitation (docs-level tasks only; implementation-class
         untested); and a pointer to docs/campaigns/agent-native-self-development/.
     (b) section 5 Reality map row "Continuation": change status to
         "CONVENTION -- responsibility-level continuation DEMONSTRATED (campaign
         R1/R2, 2026-09-02); cross-run prior-report identity still
         CONVENTION_CLOSED; machinery not earned" and keep the "What not to
         assume" cell's meaning.
     (c) section 5 Reality map row "Stop conditions" and "Next responsibility
         selection": add "(exercised by fresh contexts in campaign R1/R2)" only
         if you can cite the exact R1/R2 passage; otherwise leave unchanged.
     (d) section 6 "What is deliberately not here": add one bullet: no
         continuation schema/validator/hook -- three continuations, zero shape
         errors, one fact error caught by an in-spec verification step (C7 not
         met); reopen conditions as in (a).
     Keep the document's voice, ASCII arrows (`->`), and table formats. Do not
     add a registered workflow, Skill, schema, validator, or hook. Do not edit
     CONTEXT.md, ADRs, contracts, registries, scripts, tests, or any other file.
  4. validate: `python scripts/validate-repo.py` (expect exit 0);
     `PYTHONUTF8=1 python -m pytest tests/test_path_drift.py -q` (expect no new
     red); grep the edited file for the markdown links you added and confirm each
     target path exists.
  5. inspect `git diff --stat` (expect exactly one file); commit on
     campaign/agent-native-self-development with subject prefix `campaign(R3):`
     and trailer `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`;
     do NOT push; do NOT edit CAMPAIGN-STATE.md.
  6. write docs/campaigns/agent-native-self-development/R3-operating-map-reconciliation.md
     (second `campaign(R3):` commit): quoted before/after of each changed passage;
     what this record was sufficient for; what was missing/wrong (flag, do not
     silently fix); files consulted beyond the record and why; tool-call count;
     any authority question and its resolution; anything skipped and why.
AUTHORITY FOR R3 (sourced):     CHARTER.md ("documentation reconciliation" is a
                                listed bounded responsibility; use ordinary
                                infrastructure; one commit per responsibility);
                                docs/agent-native-operating-workflow.md section 7
                                ("Revision trigger: when a responsibility in the
                                Reality map flips status ... update this map and
                                surface it for owner review" -- PR #268 is the
                                surfacing; the map is "NOT a canonical
                                orchestration specification", so no ADR is needed).
NOT AUTHORIZED IN R3:           any file other than docs/agent-native-operating-workflow.md
                                and the R3 report; claiming cross-run prior-report
                                identity is resolved; adding machinery; editing
                                ADR status; pushing; merging; tracker writes;
                                editing CAMPAIGN-STATE.md.
STOP CONDITION:                 both commits exist and the report is written; OR a
                                step-2 verification fails (the text differs
                                materially from this spec's description) -- then
                                write the report describing the discrepancy and
                                stop without editing the map.
EXPECTED EVIDENCE OF PROGRESS:  commits `campaign(R3): ...`; the R3 report;
                                dispatcher audit; G9 closed; conditions 4/6/11
                                move toward MET on the product surface.
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
| Push branches / open PRs; qualify exact PR heads (dispatcher only; fresh contexts commit locally) | `CHARTER.md` "Git and Change Discipline" ("one coherent commit or PR per bounded responsibility"; "qualified PR head") |
| Branch-local implementation of reversible, non-ratified candidate machinery is agent-decidable; ratification is not | `CONTEXT.md` "Authority model" (Can DECIDE: reversible implementation details within scope); `CHARTER.md` "Architecture Discipline" |
| Documentation reconciliation of the operating map, surfaced for owner review | `docs/agent-native-operating-workflow.md` section 7 revision trigger; `CHARTER.md` "Responsibility Execution" list |
| MECH refresh of semantic-control-map rows; trial-log entries | `docs/semantic-control-map-trial.md` "Row maintenance" |
| Merge to `main` = owner | repository convention: ADR 0014/0026/0027 headers record owner ratification and separate merge actions; `docs/adr/README.md`; `CONTEXT.md` non-identities (`promoted != merged`); the charter grants no merge authority |
| ADR status / owner decisions must not be falsified | `docs/adr/README.md`; `AGENTS.md` rule 5 |
| External tracker writes (issue comments, labels) require explicit authority | `docs/agent-native-operating-workflow.md` section 4 (ADR 0019 PROPOSED) |
| Ask the owner only for product preference, authority expansion, irreversible tradeoffs, external environment, or material product-direction acceptance | `CHARTER.md` "Owner Decisions" |

Owner decisions required (none blocking the next responsibility):

1. **Merge authority for the campaign PR (#268)** -- standing; the campaign
   stacks responsibilities on its branch until closure.
2. **Whether to record the R1/R2 substrate observation on Issue #255** (an
   external tracker write): in this harness an isolated sub-agent's direct
   worktree write persisted twice. Recommended but not required; the
   observation is durable here.

---

## 12. DEFERRED NON-CAMPAIGN FINDINGS

| id | Finding | Class | Disposition |
|---|---|---|---|
| D1 | `tests/test_path_drift.py:154,228,358` call `read_text()` without `encoding`; on Windows cp1252 this raises `UnicodeDecodeError` on `skills/architectural-review/SKILL.md` (byte 0x9d). Linux CI (utf-8) unaffected: `core-assertions` is green on `main`. R2 reproduced it exactly (1 failed cp1252 / 0 failed utf-8) | LOCAL_BUT_REAL | deferred; one-line `encoding="utf-8"` x3 if a campaign change touches this file (candidate U7 task) |
| D2 | Collection errors on `main`: `tests/test_integration_external_repo.py` imports `SkillsOrchestrator` from the package root (class lives in `runner.py`, not re-exported); `tests/test_validate_brief_json.py` loads nonexistent `scripts/validate_brief.py`. Neither file is in any CI gate | LOCAL_BUT_REAL | deferred; not campaign-limiting |
| D3 | `roadmap.md` stale (0.2.1 / Phase 2.3). Already recorded by evidence 0022 | HISTORICAL_ONLY | no action |
| D4 | `docs/HARDENING_STATUS.md` asserts a 5-type fog taxonomy incl. `integration_fog` (map row SA10) | HISTORICAL_ONLY | no action |
| D5 | `docs/candidate/architecture-decision.md:7` links to nonexistent `docs/prototypes/repo-sensemaker-vnext.md` (candidate-branch snapshot) | HISTORICAL_ONLY | no action |
| D6 | `unevaluable` verdict category for `repair_verification_report` is proposed in the operating workflow v0 but not in the contract | DEFERRED | needs a real case; not campaign-limiting |
| D7 | `docs/research/normal-use-evidence-lane.md` section 12 says "new episodes 0" -- explicitly a snapshot "at establishment" | NO_ACTION_WARRANTED | none |
| D8 | `.github/workflows/validation.yml` line 14 comment says the `validate` job "does not execute a single pytest test"; it has run one pytest step since at least `df46871` (R2 F4) | LOCAL_BUT_REAL | deferred: editing `validation.yml` fires trial triggers (SE1/SE2/SA13); bundle with a future CI change |
| D9 | Map row SE10 says 5 `line_ending_only` skill mismatches per `distribution-drift.yaml`; `probe-repo.py` today reports 17 checked, 0 drift (R2 F5). The row's trigger is "`distribution-drift.yaml` regenerated", which has not happened; the committed file still says 5 | INSUFFICIENT_EVIDENCE | leave until the file is regenerated |
| D10 | Trial protocol step-4 selector `tests/test_cli.py::test_cli_version` did not resolve (R2 F3) | LOCAL_BUT_REAL | **fixed at R2 close-out** (mechanical selector correction; logged in trial log B) |

---

## 13. CAMPAIGN ACCEPTANCE STATUS

| # | Condition | Status after R2 | Basis |
|---|---|---|---|
| 1 | Top-level semantic control model explicit and coherent | MET (docs) | CONTEXT.md, boundary doc, ADR 0013; R1 Q1/Q2 |
| 2 | Role of active coding agent clear | MET | ADR 0013 + amendment |
| 3 | Warrant / responsibility / capability / authority not conflated | MET (docs + fail-closed tests) | ADR 0026/0027, CONTEXT.md non-identities; R2 respected every boundary |
| 4 | Durable artifacts can carry continuation state across responsibilities | MET inside the campaign; NOT YET on the product surface | R1, R2; G9 -> R3 |
| 5 | One realistic multi-responsibility task continued from durable state without hidden conversation memory | MET (docs-level): R0 -> R1 -> R2 were performed by three contexts (dispatcher, fresh, fresh) with the record as the only shared state; limitation: no implementation-class responsibility yet (U7) | R1, R2 reports |
| 6 | Repository-level development direction representable for consequential capability selection | LARGELY MET inside the campaign (fresh contexts selected and performed the named responsibility and could explain why it beat alternatives); NOT YET on the product surface | R1 Q3, R2 section 1; G9 |
| 7 | Role of deterministic scripts bounded and coherent | LARGELY MET, not consolidated | G5; R3 adds the evidence sentence |
| 8 | Role of hooks defined and evidence-supported | PARTIAL: first evidence says no hook warranted (U3); disposition not yet written on the product surface | G3 |
| 9 | Old workflow system has a clear disposition | PARTIAL | ADR 0027 (liveness); inventory in section 2; disposition doc pending (G4) |
| 10 | Existing useful functionality not destroyed | MET so far (docs-only changes; `validate-repo.py` green) | -- |
| 11 | Tests, validators, contracts, docs, implementation agree sufficiently | PARTIAL | G3, G9; D8/D9 minor |
| 12 | Repository passes appropriate complete qualification | PARTIAL | `main` CI green at base; PR #268 exact-head CI green at `b4335c3` (19/19); R2 + close-out commits pushed after this commit; local baseline re-run in progress |
| 13 | Remaining material limitations explicitly documented | IN PROGRESS | this file |

Disposition after R2: **CONTINUE** (R3).

---

## 14. Responsibility trace (append-only)

```text
2026-09-02  R0  reconstruction + campaign record v1                     -> next: R1
2026-09-02  R1  fresh-context reconstruction probe (Q1-Q5 ok; Q6 partial;
                5 omissions, repaired at close-out; record v2)          -> next: R2
2026-09-02  R2  fresh-context continuation trial: map rows SE1/SE2/SA13/
                SA9 refreshed, trial log A-D, addendum; caught record
                error F1 (gate provenance)                              -> audit
2026-09-02  R2  close-out: audit VERIFIED; SA10/SA12 refreshed; protocol
                selector fixed; record v3                               -> next: R3
```

---

## 15. Remote / integration status (updated by the dispatcher, never assumed)

```text
pushed:        b4335c3 (R1 close-out) -> origin/campaign/agent-native-self-development
               R2 commits fa2dd68, 9160a5b + this close-out: pushed after this commit
PR:            #268 (draft) https://github.com/ThorStarlord/sensemaking-skills/pull/268
last main CI:  Validator Ecosystem completed/success @ f10b7da (2026-09-02T03:43Z)
campaign CI:   run 33591059541 @ b4335c3: completed/success (19/19 jobs)
merged:        nothing (owner decision)
```
