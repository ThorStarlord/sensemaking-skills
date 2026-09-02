# Campaign: reliable agent-native, artifact-mediated self-development

```
STATUS:    ACTIVE development-campaign record (living document, v4 after R3)
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
           continuing context can catch errors here (R2 did: see F1; R3 did:
           see R3 M2/M3).
```

This file exists so that campaign reasoning does not live only in one
conversation's context. Three fresh contexts have so far continued the campaign
from this file alone: R1 (reconstruction), R2 (mechanical execution), R3
(judgment-class documentation reconciliation). See section 8.

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
| Responsibility selection | **CONVENTION** (agent judgment + skill catalog); no machinery; automatic routing deliberately unratified; exercised by a fresh context (R1 Q3) | operating workflow Reality map (R3-updated row); `using-sensemaking` SKILL.md sections 5-7 |
| Continuation across responsibilities | **On the product surface since R3**: `docs/agent-native-operating-workflow.md` section 2 "CONTINUATION" now carries a dated subsection describing responsibility-level continuation from a durable record (what a fresh context needs; failure classes observed and repaired; what was not needed; reopen conditions; limitation), and the Reality map row reads "CONVENTION -- responsibility-level continuation DEMONSTRATED (campaign R1/R2); cross-run prior-report identity still CONVENTION_CLOSED; machinery not earned". Cross-run prior-report identity was deliberately left unresolved (not exercised) | operating map section 2 subsection + section 5 rows + section 6 bullet (commit `6ff4a89`); `R1-*.md`, `R2-*.md`, `R3-*.md` |
| Continuation artifacts that exist | `user_intent` (ADR 0006), `session_summary` (one required field), `prompt_handoff` (skill-to-skill prompt packaging), `work_claim`, `reconciliation_report`, `repair_verification_report`. Adding a new artifact type costs: contract entry + canonical-vocabulary `artifact_ids` entry + packaged mirror + validator (enforced by `tests/test_path_drift.py::test_vocabulary_covers_all_artifacts` and the PR #258 mirror-agreement test). **Decision (U5): no new artifact type for continuation; Markdown record convention** | `skills/workflow-planner/references/artifact-contracts.yaml`; `docs/canonical-vocabulary.yaml` `artifact_ids:` |
| Repository-level development-direction representation | **ABSENT before this campaign**; this record is the first representation and the operating map now documents the field set that proved necessary. Fresh contexts selected and performed the named responsibility and could explain why it beat alternatives (R1 Q3; R2/R3 section 1 of each report) | this file; operating map section 2 subsection |
| Deterministic machinery | validators (`validate-output.py` dispatch -> `validate-artifact.py` + specialized), probe engine (`probe-repo.py`, `repo_probes.py`, `probe_relationships.py`), `gate_relationship_findings.py`, `run-ledger.py`, `workflow-runtime.py` (paths/plan/gates/sessions; model executors retired 2026-08-13), `workflow_liveness.py`, `validate-repo.py`. Role described across the retirement plan, the boundary doc, `CONTEXT.md`; not consolidated (G5) | `scripts/`; retirement plan classification tables |
| CI on `main` | 13 jobs in `.github/workflows/validation.yml`: `gate-a-*`, phase 2-6 campaign/execution suites, `validate` (scripts + one pytest step), `probe-gate`, `core-assertions` (7 pytest files incl. `test_path_drift.py`, `test_cli.py`), `conditional-representation-exact-head`. Provenance (established by R2 from git): the enforcement gate commit `e1db7dc` (2026-08-11) is on `main`'s first-parent line -- no merge commit, no PR. `main` CI green at trial start `df46871` and at base `f10b7da` | `validation.yml`; `git log --first-parent`; `gh run list --branch main` |
| Hooks | `.claude/hooks/sessionstart.md` is a Markdown description of a SessionStart bootstrap reminder; `.claude/settings.json` is `{}` (no hook wired); skills are discovered because they are copied to `~/.claude/skills/` (`setup_skills.py`; drift tracked by `distribution-drift.yaml`), not by any hook. No continuation/liveness hook exists. R1/R2/R3 continuation events were explicit dispatches; none was missed; the operating map now records "no hook needed at this scale" with reopen conditions | those files; operating map section 6 bullet |
| Real-use evidence of the operating loop | Workflow v0 dogfood on 2 repos (verdict `KEEP_WITH_WATCH_ITEMS`); 3 normal-use episodes recorded as **GitHub issue comments on Issue #218** (by that lane's own policy; not in the repository tree); recurring boundary there: PR-head qualification did not bind the integration base (episodes 002, 003) | `experiments/evidence/0021`, `0022`; `docs/research/normal-use-evidence-lane.md` section 7; Issue #218 |
| Real execution evidence per active workflow (for U4) | run ledgers/mode coverage/evidence exist for: `fast-local-diagnostic`, `full-local-sensemaking`, `full-fog-workflow`, `fast-path-workflow`, `docs-contract-reconciliation` (guided; dogfooded 2026-08, evidence 0018/0019), `architectural-review-planning-workflow` (golden path, 2026-07-25), `docs-architecture`, `setup-sensemaking-repo`, `product-strategy-sprint`, `skill-maintenance-loop`, `docs-implementation-workflow`; `artifact-reconciliation` has agent-native execution evidence (`artifacts/reconciliation_report.md`, 2026-08-22) but no run ledger; `autonomous-sprint-preflight`, `product-discovery-sprint`, `skill-evaluation-workflow` have plan_only or test-only traces | `docs/mode-coverage.yaml`; `artifacts/0[1-4]-orchestration-run/run-ledger.jsonl`; `experiments/evidence/`; `artifacts/reconciliation_report.md` |
| Research lanes (non-ratified) | C6R compressed control hypothesis (#226 open); warrant-as-primitive; uncertainty-selection; PHB meta-finding "sensemaking loops saturated; spikes not briefs" (2026-08-30); semantic-control-map persistence trial OPEN (min close 2026-09-28) -- this campaign supplied its first consultation, over-read, and MECH-refresh events (R0/R2/close-out) | `docs/research/control-model-research-agenda.md`; `docs/semantic-control-map-trial-log.md` |
| Goal A external validation | ACTIVE but **halted in this environment** (three execution substrates falsified; owner halt rule) | Issue #255; evidence 0023 |
| Repository visibility | public (`ThorStarlord/sensemaking-skills`) | `gh repo view` |

Local full-suite baseline (Windows, Python 3.14, shared `main` checkout): in
progress at R3 close-out. Two prior attempts stalled: the first on the D2
collection errors, the second on `tests/test_owner_approval_artifact.py`
(D11: `REPO_ROOT.rglob` over the ~76k untracked sprawl files of the shared
checkout; not a hang, just pathological there). The final campaign
qualification will run the suite in the clean worktree instead.

---

## 3. COMPLETED CAMPAIGN RESPONSIBILITIES

| # | Responsibility | Result | Evidence |
|---|---|---|---|
| R0 | Reconstruct current product/capability state from durable repository evidence; select first bounded responsibility; establish durable campaign record | this file v1 | commit `2bc8a2c` |
| R1 | Fresh-context reconstruction probe: one cold agent context given only the repo and this file's path answered the seven reconstruction questions | Q1-Q5 `RECONSTRUCTED`; Q6 `PARTIAL` (`AUTHORITY_AMBIGUITY`, narrow); Q7 five omissions -- four are missing-durable-state by content (charter and a cited standing instruction absent from the repo; push/PR status unrecorded; last `main` CI result unrecorded; GitHub-only evidence unmarked) and one is an unflagged substrate risk (R1's dispatch method vs evidence 0023) [wording corrected at R3 close-out per R3 M2]; cost 39 files / 25 tool calls. Repairs at close-out: charter committed; authority sourced (section 11); push/CI status recorded (section 15); G6 corrected | `R1-fresh-context-reconstruction.md` (SHA-256 `9ea98c3b...`, verbatim); commit `b4335c3` |
| R2 | Continuation-and-execution trial: a fresh context performed the G6 semantic-control-map trial bookkeeping from this file alone (7 steps) | All 7 steps performed; diff exactly the 4 rows + log + addendum; caught a factual error in this record (F1: gate provenance) via the spec's verification step; 2 protocol defects + 2 more stale rows flagged, not acted on. Cost 9 files / 36 tool calls / ~15 min. **Dispatcher audit: VERIFIED** | `R2-continuation-trial.md`; commits `fa2dd68`, `9160a5b` |
| R2 close-out (dispatcher) | Audit; SA10/SA12 MECH refresh; protocol selector fix; record v3 | commit `2adfeaf` | trial log B |
| R3 | Continuation-pattern reconciliation into the product operating map, performed by a fresh context (judgment-class documentation task) | All 6 steps performed; exactly one product file changed (`docs/agent-native-operating-workflow.md` +88/-3: dated subsection under CONTINUATION, 3 Reality-map rows, 1 section-6 bullet); cross-run prior-report identity correctly left unresolved; per-row attribution narrowed to the single supporting report (M1); two record overstatements flagged, not silently fixed (M2 R1-omission classes; M3 continuation count basis); `validate-repo.py` exit 0; `test_path_drift.py` green under utf-8; links resolve; file stays ASCII/LF. Cost 8 files / 24 tool calls. **Dispatcher audit: VERIFIED** (diff read line by line against the spec; the dispatcher's own root-relative link check was mis-rooted -- links are relative to `docs/` and resolve) | `R3-operating-map-reconciliation.md`; commits `6ff4a89`, `fbbb637` |
| R3 close-out (dispatcher) | Audit; record corrections (R1 row wording; continuation count basis); record v4 | this commit | section 14 |

---

## 4. EVIDENCE PRODUCED

- `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (this file).
- `docs/campaigns/agent-native-self-development/CHARTER.md` (owner instruction, verbatim).
- `docs/campaigns/agent-native-self-development/R1-fresh-context-reconstruction.md` (probe output, verbatim).
- `docs/campaigns/agent-native-self-development/R2-continuation-trial.md` (trial report, verbatim).
- `docs/campaigns/agent-native-self-development/R3-operating-map-reconciliation.md` (trial report, verbatim).
- Product-side changes so far (docs only): `docs/agent-native-operating-workflow.md` (R3: continuation subsection, Reality-map rows, section-6 bullet); `docs/semantic-control-map.md` rows SE1/SE2/SA13/SA9 (R2) + SA10/SA12 (close-out) MECH-refreshed; `docs/semantic-control-map-trial-log.md` sections A-D populated with real events; `docs/semantic-control-map-trial.md` step-4 selector corrected; `docs/enforcement-contract.md` dated status addendum.

---

## 5. CURRENTLY DEMONSTRATED CAPABILITIES

(Demonstrated = real use with durable evidence, not merely documented.)

- Agent-native `repository_sensemaking_brief` production + mechanical validation on two structurally different repositories (evidence 0021, 0022).
- Responsibility selection without automatic routing; stop at owner/authority boundary instead of premature implementation (evidence 0022; #218 episodes 001, 003; #255).
- Claim reconciliation (`output-reconciler`) and finding-specific repair verification (`repair-verifier`) (evidence 0018, 0019, 0020; `artifacts/reconciliation_report.md`).
- Fail-closed authority on `auto_invoke_next_workflow` and on compatibility-only workflow selection (ADR 0026/0027 test suites).
- Deterministic probe-engine enforcement in CI (`probe-gate`, `core-assertions`).
- **(R1)** A fresh context reconstructed the campaign mission, capability state, task rationale, established-vs-uncertain split, and next responsibility from this record plus the repository, with no conversation memory.
- **(R2)** A fresh context **performed** a seven-step, three-file mechanical responsibility from this record alone, respected every authority boundary, ran the named validators, committed, and corrected a wrong fact in the record from git evidence.
- **(R3)** A fresh context performed a **judgment-class** documentation responsibility (reconciling evidence into the product's canonical operating map) from this record alone: verified before writing, narrowed the spec where the evidence supported less than the spec said, kept an unresolved item unresolved, and produced a product-quality diff the dispatcher accepted without amendment.
- **(count basis, per R3 M3)** Four record-mediated handoffs so far (R0 -> R1, R1 -> R2, R2 -> R3, plus each close-out audit back to the dispatcher); three into fresh contexts; zero shape errors; two fact/overstatement errors in the record, both caught by the continuing context's verification steps.
- **(substrate)** In this harness an isolated sub-agent's direct file write to the worktree persisted three times (R1, R2, R3). Narrows, for this harness only, the "isolated sub-agent direct write BLOCKED" finding of evidence 0023 / Issue #255.

---

## 6. KNOWN MATERIAL GAPS

| id | Gap | Condition(s) | Class | Status |
|---|---|---|---|---|
| G1 | Continuation from a durable record is demonstrated for documentation-level responsibilities (mechanical: R2; judgment-class: R3). Not yet shown: an **implementation-class** responsibility (code + tests + CI) performed by a fresh context from durable state | 4, 5 | CAMPAIGN_RELEVANT | OPEN -> R4 (U7) |
| G2 | Repository-level development direction was not represented before this campaign | 6 | CAMPAIGN_RELEVANT | LARGELY CLOSED: this record + operating map subsection; limitation: one campaign, one repository |
| G3 | Role of hooks: documented SessionStart hook not wired (`settings.json = {}`); hook doc prose ("picks correct workflow first try", "auto-fix vs escalate") predates ADR 0026 and the current bootstrap SKILL.md; the operating map now states no continuation hook is warranted at this scale, but the hook doc itself is still stale and no disposition sentence exists for the bootstrap hook | 8, 11 | CAMPAIGN_RELEVANT | OPEN -> R5 |
| G4 | Per-workflow disposition in campaign vocabulary not recorded; ADR 0027 settles liveness, not KEEP/DEMOTE/RETIRE. Execution-evidence inventory in section 2 | 9 | CAMPAIGN_RELEVANT | OPEN -> R6 |
| G5 | Deterministic-script role is described across the retirement plan, the boundary doc, and `CONTEXT.md` but not consolidated | 7 | CAMPAIGN_RELEVANT | OPEN -> R5 (same doc as hooks) |
| G6 | Semantic-control-map rows stale from construction; enforcement-contract status line stale | 11 | CAMPAIGN_RELEVANT | **CLOSED** (R2 + close-out) |
| G7 | Authority grants not sourced in the repository | 5, 13 | CAMPAIGN_RELEVANT | **CLOSED** (R1 close-out) |
| G8 | Some cited evidence lives only in GitHub (Issue #218 episode comments, Issue #255 state, CI run results). Fresh contexts handled it correctly (R2 used `gh` read-only and said so; R3 did not rely on it) | 5, 13 | DEFERRED | documented limitation |
| G9 | Product operating map did not represent the demonstrated continuation pattern | 4, 6, 11 | CAMPAIGN_BLOCKING | **CLOSED** (R3, commit `6ff4a89`) |

---

## 7. ACTIVE CONSTRAINTS

- C1 **Bootstrap constraint** (`CHARTER.md`): this campaign does not use `repo-sensemaker`, `using-sensemaking`, registered workflows, runtime routing, fog routing, Skill-to-Skill continuation mechanisms under evaluation, or hooks as its controller.
- C2 **Authority** (sources in section 11): the dispatcher pushes branches and opens PRs for exact-head qualification (charter); fresh-context responsibilities commit locally and do not push; merge to `main`, ADR acceptance, canonical contract/registry ratification, and external tracker writes are **owner** actions. Never falsify owner decisions or ADR `**Status**` lines.
- C3 **Semantic-control-map trial is OPEN** (`docs/semantic-control-map-trial.md`): do not add rows; MECH rows are refreshed on triggers, not re-decided; JUDG/INTERP text is reviewed only on a plausible trigger; record consultation/over-read events in the trial log.
- C4 **Goal A is halted** in this environment (#255); do not run Goal A episodes. Issue #218 episodes are recorded only when they arise from ordinary work, and only by an owner-authorized tracker write.
- C5 **Windows cp1252**: console output ASCII-only; file reads in tests need explicit encoding; run pytest both with the default code page and with `PYTHONUTF8=1` to distinguish encoding reds from real reds. CI runs on Linux (utf-8).
- C6 **Worktree per session**: all campaign work in `H:/GithubRepositories/smk-campaign`; never the shared `main` checkout.
- C7 **Machinery promotion rule** (repository; `docs/agent-native-operating-workflow.md` section 7): repeated useful responsibility + stable semantics + repeated burden/error + mechanically expressible boundary -> candidate for formalization. Not: "there is a box in the diagram".
- C8 **One responsibility at a time** (charter): while a fresh-context responsibility runs, the dispatcher does not edit files it may read and does not open a second responsibility.
- C9 **Task specs must contain verification steps, not only assertions** (R2 F1, R3 M2/M3). A fresh context is told to prefer repository evidence over this record where they conflict, and to flag rather than silently correct.
- C10 **Don't touch unrelated code** (`AGENTS.md` rule 4): implementation-class responsibilities name their files; nothing else is edited.

---

## 8. OPEN DECISION-CHANGING UNCERTAINTIES

| id | Uncertainty | Source | Cheapest sufficient evidence | Status |
|---|---|---|---|---|
| U1 | What continuation state does a fresh context fail to reconstruct from durable state, and in which failure class? | empirical | R1 | **RESOLVED (R1)** |
| U2 | Do the outer loop (repository-evolution) and the inner loop (task-execution) need different durable state, or does one record suffice? | repository_evidence + trace | R2/R3 traces | **NARROWED (R2, R3).** One file carried both for a mechanical task (R2) and a judgment-class documentation task (R3): sections 6-10 = outer-loop rationale; the numbered step spec in section 10 = inner-loop state. Untested for implementation-class tasks (U7) |
| U3 | Is any hook warranted beyond a documented bootstrap? | empirical | recurrent continuation event that a manual step keeps missing | OPEN; R1/R2/R3: none observed. Current evidence does not warrant a hook; the operating map now says so with reopen conditions. Remaining work is the disposition of the *documented bootstrap hook* (G3 -> R5) |
| U4 | Which registered workflows have enough real traces for a disposition other than `INSUFFICIENT_EVIDENCE`? | repository_evidence | inventory (section 2) -> disposition doc | EVIDENCE GATHERED; disposition pending (G4 -> R6) |
| U5 | Continuation state: existing contracts, a new artifact type, or a Markdown record with no contract? | repository_evidence | U2 result + cost of a new artifact type | **DECIDED FOR NOW: Markdown record convention, no new artifact type, no validator** (now stated on the product surface, operating map section 6). Reopen if a fresh context fails on a *missing or malformed section* rather than a wrong fact, or if more than one dispatcher must produce such records |
| U6 | Can a fresh context perform (not only reconstruct) a bounded multi-step task from this record? | empirical | R2 | **RESOLVED (R2): yes**; R3 extends it to judgment-class documentation work |
| U7 | Does the pattern hold for an **implementation-class** responsibility (code + tests + CI) performed by a fresh context from durable state, including a repair-vs-retire judgment? | empirical | R4 | OPEN -> R4 |

---

## 9. CURRENT HIGHEST-LEVERAGE CAPABILITY BOUNDARY

**Implementation-class continuation** (U7, G1). The mission is
*self-development*: the product developing itself through code, tests, and CI,
not only through documentation. Every continuation so far was docs-level.
The two deferred local defects D1 and D2 are the smallest real code change the
repository currently needs, and D2 requires exactly the judgment the operating
rule describes (is this test still a live responsibility, or retired residue?).
They are selected **because** they materially advance U7 (charter: "A local
defect may still be selected if resolving it materially advances a campaign
capability"), not as cleanup.

---

## 10. CURRENT / NEXT WARRANTED RESPONSIBILITY

```text
R4  Implementation-class continuation trial
    (a fresh context repairs or retires two local test defects from this record)

CAMPAIGN CAPABILITY AFFECTED:   artifact-mediated continuation for code + tests +
                                CI (conditions 4, 5, 11); U7; G1
CURRENT LIMITATION:             all fresh-context continuations so far were
                                documentation-level; no code has been changed from
                                durable state, and no repair-vs-retire judgment
                                has been exercised by a fresh context
WHY IT MATTERS TO THE MISSION:  "self-development" means the product changes its
                                own code from durable state under authority; if
                                the pattern only carries prose it does not carry
                                the mission
BOUNDED RESPONSIBILITY:         steps for the fresh context:
  1. read this file (sections 7, 9, 10, 12 D1/D2/D11); tests/test_path_drift.py
     lines 140-165, 220-235, 350-365; the import/header block of
     tests/test_integration_external_repo.py and of
     tests/test_validate_brief_json.py; src/sensemaking_skills/__init__.py;
     src/sensemaking_skills/runner.py (class SkillsOrchestrator, first ~60
     lines) and src/sensemaking_skills/config.py (class ConfigManager);
     `ls scripts | grep -i brief`; the `core-assertions` job in
     .github/workflows/validation.yml (lines ~703-736) so you know
     test_path_drift.py runs in CI on Linux.
  2. VERIFY (reproduce before changing anything; if reproduction differs
     materially from D1/D2 below, write the report and stop):
     D1: `python -m pytest tests/test_path_drift.py -q` under the default
         Windows code page -> expect exactly 1 failure,
         test_fog_type_consistency_in_docs, UnicodeDecodeError at line 154;
         `PYTHONUTF8=1 python -m pytest tests/test_path_drift.py -q` -> expect
         0 failures.
     D2: `python -m pytest tests/test_integration_external_repo.py
         tests/test_validate_brief_json.py -q --co` -> expect 2 collection
         errors: ImportError (cannot import SkillsOrchestrator from
         sensemaking_skills) and FileNotFoundError (scripts/validate_brief.py).
  3. D1 repair (mechanical): add `encoding="utf-8"` to the three `read_text()`
     calls in tests/test_path_drift.py (lines ~154, ~228, ~358). No other change
     to that file.
  4. D2: for EACH of the two files decide, from repository evidence, whether it
     is a LIVE responsibility to repair or RETIRED residue, then apply the
     smallest change:
     (a) tests/test_integration_external_repo.py -- establish: what
         `SkillsOrchestrator` / `ConfigManager` are today
         (`git log -S SkillsOrchestrator --format='%h %ad %s' --date=short --
         src/sensemaking_skills/__init__.py`; runner.py; config.py; the
         deprecation in PR #267 / commits 84709ea, 09c2667 visible in
         `git log --oneline -20`); what the test file actually exercises
         (does it need a real external repository, network, or the retired
         programmatic model executors of ADR 0013?). If the tested behavior is
         retained and the only defect is the import path, change ONLY the
         import lines to the real module locations and run the file. If the
         tested behavior is retired or needs an unavailable environment, add a
         module-level `pytest.skip(reason=..., allow_module_level=True)` (or
         `pytest.importorskip` where that is the precise cause) whose reason
         cites the evidence (commit/ADR), keeping the file's content otherwise
         intact. Do NOT delete the file. Do NOT edit src/.
     (b) tests/test_validate_brief_json.py -- establish whether an underscore
         `scripts/validate_brief.py` ever existed (`git log --all --format='%h
         %ad %s' --date=short -- scripts/validate_brief.py`) and whether the
         file's tests target the CURRENT `scripts/validate-brief.py` interface
         (compare the functions/flags the test calls with what
         validate-brief.py defines). If they match, fix ONLY the path and run
         the file; if the tests then fail for reasons other than the path,
         revert your change to this file and report the mismatch (do NOT edit
         validators). If the test targets a retired interface, use the same
         module-level skip-with-reason approach as (a).
     Record each decision (repair | retire-skip | revert-and-report) with the
     evidence in the report.
  5. validate:
     `python -m pytest tests/test_path_drift.py tests/test_cli.py -q` under the
       default code page -> expect 0 failures now;
     `PYTHONUTF8=1 python -m pytest tests/test_repo_probes.py
       tests/test_probe_report_cli.py tests/test_probe_relationships.py
       tests/test_skill_distribution_probe.py
       tests/test_gate_relationship_findings.py tests/test_path_drift.py
       tests/test_cli.py -q` (the CI core-assertions set) -> expect no new red;
     `python -m pytest tests/test_integration_external_repo.py
       tests/test_validate_brief_json.py -q` -> expect clean collection (tests
       pass or are skipped with reasons; zero errors);
     `python scripts/validate-repo.py` -> exit 0.
  6. `git diff --stat` -> expect at most 3 files, all under tests/; commit on
     campaign/agent-native-self-development with subject prefix `campaign(R4):`
     and trailer `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`;
     do NOT push; do NOT edit CAMPAIGN-STATE.md.
  7. write docs/campaigns/agent-native-self-development/R4-implementation-continuation.md
     (second `campaign(R4):` commit): per-defect decision + evidence; exact
     before/after test results under both code pages; what this record was
     sufficient for; what was missing/wrong (flag, do not silently fix);
     files consulted beyond the record and why; tool-call count; authority
     questions and resolutions; anything skipped and why.
AUTHORITY FOR R4 (sourced):     CHARTER.md ("bounded implementation" and
                                "test-harness improvement" are listed bounded
                                responsibilities; "add appropriate regression
                                tests"; "A local defect may still be selected if
                                resolving it materially advances a campaign
                                capability"); CONTEXT.md "Authority model" (Can
                                DECIDE: reversible implementation details within
                                scope); AGENTS.md rule 4 (only the named files).
NOT AUTHORIZED IN R4:           editing anything under src/, scripts/, skills/,
                                docs/ (other than the R4 report), .github/,
                                contracts, registries, ADRs; deleting test files;
                                editing tests other than the three named; pushing;
                                merging; tracker writes; editing CAMPAIGN-STATE.md.
STOP CONDITION:                 both commits exist and the report is written; OR
                                step-2 reproduction differs materially from
                                D1/D2 -> report and stop without code changes.
EXPECTED EVIDENCE OF PROGRESS:  commits `campaign(R4): ...`; the R4 report;
                                dispatcher audit incl. exact-head CI on the pushed
                                head (core-assertions must stay green on Linux);
                                U7 resolved or narrowed; G1 closed or narrowed;
                                D1/D2 closed.
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
| Push branches / open PRs; qualify exact PR heads (dispatcher only; fresh contexts commit locally) | `CHARTER.md` "Git and Change Discipline" |
| Branch-local implementation of reversible, non-ratified changes is agent-decidable; ratification is not | `CONTEXT.md` "Authority model"; `CHARTER.md` "Architecture Discipline" |
| Bounded implementation / test-harness improvement of named files; a local defect may be selected when it advances a campaign capability | `CHARTER.md` "Responsibility Execution", "Strategic Selection Rule"; `AGENTS.md` rules 3-4 |
| Documentation reconciliation of the operating map, surfaced for owner review | `docs/agent-native-operating-workflow.md` section 7 revision trigger; `CHARTER.md` |
| MECH refresh of semantic-control-map rows; trial-log entries | `docs/semantic-control-map-trial.md` "Row maintenance" |
| Merge to `main` = owner | repository convention: ADR 0014/0026/0027 headers; `docs/adr/README.md`; `CONTEXT.md` non-identities; the charter grants no merge authority |
| ADR status / owner decisions must not be falsified | `docs/adr/README.md`; `AGENTS.md` rule 5 |
| External tracker writes require explicit authority | `docs/agent-native-operating-workflow.md` section 4 (ADR 0019 PROPOSED) |
| Ask the owner only for product preference, authority expansion, irreversible tradeoffs, external environment, or material product-direction acceptance | `CHARTER.md` "Owner Decisions" |

Owner decisions required (none blocking the next responsibility):

1. **Merge authority for the campaign PR (#268)** -- standing.
2. **Whether to record the R1-R3 substrate observation on Issue #255** (an
   external tracker write). Recommended but not required.

---

## 12. DEFERRED NON-CAMPAIGN FINDINGS

| id | Finding | Class | Disposition |
|---|---|---|---|
| D1 | `tests/test_path_drift.py:154,228,358` call `read_text()` without `encoding`; on Windows cp1252 this raises `UnicodeDecodeError` on `skills/architectural-review/SKILL.md` (byte 0x9d). Linux CI unaffected. Reproduced by R2 | LOCAL_BUT_REAL | **selected for R4** (advances U7) |
| D2 | Collection errors on `main`: `tests/test_integration_external_repo.py` imports `SkillsOrchestrator, ConfigManager` from the package root (not exported there); `tests/test_validate_brief_json.py` loads nonexistent `scripts/validate_brief.py` (the script is `validate-brief.py`). Neither file is in any CI gate | LOCAL_BUT_REAL | **selected for R4** (repair-vs-retire judgment) |
| D3 | `roadmap.md` stale (0.2.1 / Phase 2.3). Already recorded by evidence 0022 | HISTORICAL_ONLY | no action |
| D4 | `docs/HARDENING_STATUS.md` asserts a 5-type fog taxonomy incl. `integration_fog` (map row SA10) | HISTORICAL_ONLY | no action |
| D5 | `docs/candidate/architecture-decision.md:7` links to nonexistent `docs/prototypes/repo-sensemaker-vnext.md` | HISTORICAL_ONLY | no action |
| D6 | `unevaluable` verdict category for `repair_verification_report` proposed but not in the contract | DEFERRED | needs a real case |
| D7 | `docs/research/normal-use-evidence-lane.md` section 12 "new episodes 0" is a snapshot "at establishment" | NO_ACTION_WARRANTED | none |
| D8 | `.github/workflows/validation.yml` line 14 comment says the `validate` job runs no pytest; it has run one pytest step since at least `df46871` (R2 F4) | LOCAL_BUT_REAL | deferred: editing `validation.yml` fires trial triggers; bundle with a future CI change |
| D9 | Map row SE10 vs current probe output (R2 F5); the row's trigger (`distribution-drift.yaml` regenerated) has not fired | INSUFFICIENT_EVIDENCE | leave |
| D10 | Trial protocol step-4 selector did not resolve (R2 F3) | LOCAL_BUT_REAL | **fixed at R2 close-out** |
| D11 | `tests/test_owner_approval_artifact.py::test_stopping_state_has_no_operative_owner_approval` does `REPO_ROOT.rglob("owner-approval.md")` -- on the shared `main` checkout with ~76k untracked files this takes >12 min (looked like a hang); fine on a clean checkout and in CI | LOCAL_BUT_REAL (environment) | deferred; not campaign-limiting; note for local full-suite runs |

---

## 13. CAMPAIGN ACCEPTANCE STATUS

| # | Condition | Status after R3 | Basis |
|---|---|---|---|
| 1 | Top-level semantic control model explicit and coherent | MET (docs) | CONTEXT.md, boundary doc, ADR 0013; R1 Q1/Q2 |
| 2 | Role of active coding agent clear | MET | ADR 0013 + amendment |
| 3 | Warrant / responsibility / capability / authority not conflated | MET (docs + fail-closed tests) | ADR 0026/0027; R2/R3 respected every boundary |
| 4 | Durable artifacts can carry continuation state across responsibilities | MET for documentation-level responsibilities, now stated on the product surface | R1-R3; operating map section 2 subsection |
| 5 | One realistic multi-responsibility task continued from durable state without hidden conversation memory | MET (docs-level): R0 -> R1 -> R2 -> R3 across four contexts with this record as the only shared state; limitation: implementation-class untested (U7 -> R4) | R1-R3 reports |
| 6 | Repository-level development direction representable for consequential capability selection | LARGELY MET (this record; operating map documents the field set); limitation: one campaign, one repository | R1 Q3; R2/R3 section 1 |
| 7 | Role of deterministic scripts bounded and coherent | LARGELY MET, not consolidated | G5 -> R5 |
| 8 | Role of hooks defined and evidence-supported | PARTIAL: "no continuation hook at this scale" now on the product surface with reopen conditions; the documented bootstrap hook's disposition and stale prose remain | G3 -> R5 |
| 9 | Old workflow system has a clear disposition | PARTIAL | ADR 0027 (liveness); inventory in section 2; disposition doc pending (G4 -> R6) |
| 10 | Existing useful functionality not destroyed | MET so far (docs-only changes; `validate-repo.py` green; CI green on every pushed head) | section 15 |
| 11 | Tests, validators, contracts, docs, implementation agree sufficiently | PARTIAL | G3; D1/D2 (-> R4); D8/D9 minor |
| 12 | Repository passes appropriate complete qualification | PARTIAL | `main` CI green at base; PR #268 exact-head CI green at `b4335c3` and `2adfeaf`; R3 commits pushed after this commit; full-suite run in the clean worktree pending |
| 13 | Remaining material limitations explicitly documented | IN PROGRESS | this file |

Disposition after R3: **CONTINUE** (R4).

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
2026-09-02  R3  fresh-context judgment-class trial: continuation pattern
                reconciled into the operating map (+88/-3); flagged two
                record overstatements (M2, M3)                          -> audit
2026-09-02  R3  close-out: audit VERIFIED; record corrections; record v4 -> next: R4
```

---

## 15. Remote / integration status (updated by the dispatcher, never assumed)

```text
pushed:        2adfeaf (R2 close-out) -> origin/campaign/agent-native-self-development
               R3 commits 6ff4a89, fbbb637 + this close-out: pushed after this commit
PR:            #268 (draft) https://github.com/ThorStarlord/sensemaking-skills/pull/268
last main CI:  Validator Ecosystem completed/success @ f10b7da (2026-09-02T03:43Z)
campaign CI:   run 33591059541 @ b4335c3: completed/success (19/19)
               run 33592107833 @ 2adfeaf: completed/success
merged:        nothing (owner decision)
```
