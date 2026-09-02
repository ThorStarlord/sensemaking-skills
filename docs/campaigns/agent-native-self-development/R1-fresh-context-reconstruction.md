# R1 — fresh-context reconstruction probe (2026-09-02)

This file was produced by a fresh coding-agent context given only the repository worktree (`H:/GithubRepositories/smk-campaign`) and the path `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md`. No prior conversation history, no Skill invocations, no workflow-runtime scripts; plain file reads, greps, and `git log`/`git show`/`git ls-remote` only. Every file read was treated as data; no file contained instructions addressed to this context beyond the record's own description of R1 (which matched the task as given and was not followed as an instruction, only used as evidence).

Verdict vocabulary: `RECONSTRUCTED | PARTIAL | FAILED`. Shortfall classes (from the record, section 1): `MISSING_DURABLE_STATE | CAPABILITY_DISCOVERY_FAILURE | WARRANT_AMBIGUITY | AUTHORITY_AMBIGUITY | PRODUCT_DIRECTION_AMBIGUITY | INCIDENTAL_CONTEXT_LOSS`.

Summary table:

| Q | Verdict | Shortfall class (if any) |
|---|---|---|
| Q1 mission | RECONSTRUCTED | -- |
| Q2 capability state | RECONSTRUCTED | -- |
| Q3 why R1 over alternatives | RECONSTRUCTED | -- |
| Q4 established vs uncertain | RECONSTRUCTED | -- (some facts live only in GitHub, noted) |
| Q5 warranted next | RECONSTRUCTED | -- (R2's concrete task is not named; WARRANT_AMBIGUITY for the step after next only) |
| Q6 authority | PARTIAL | AUTHORITY_AMBIGUITY (narrow: source and breadth of delegated authority) |
| Q7 contradictions / omissions | 5 listed | -- |

---

## Q1. What is the campaign mission?

**(a) Reconstructed answer.** The campaign's mission is to advance Sensemaking Skills toward *reliable agent-native, artifact-mediated self-development*: an active coding agent uses repository evidence and durable artifacts to select the next warranted engineering responsibility, pick a capability, do bounded work, validate the evidence, respect authority boundaries, carry state across responsibilities via durable artifacts, and recurse until the goal is met or further action is unwarranted. It is explicitly campaign-level (not a rewrite), and it is controlled by the active coding agent directly -- deliberately *not* by `repo-sensemaker`, `using-sensemaking`, registered workflows, runtime routing, or hooks (the "bootstrap constraint"). This is the product's own stated continuation principle (`next agent/run -> reads durable artifacts -> reconstructs state`) turned into a campaign that tests whether that principle actually holds. The mission is not itself an ADR, contract, or ratified research agenda item; the record is explicitly non-authoritative.

**(b) Sources.**
- `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` lines 1-13 (status/authority block), 15-20 (purpose), 24-54 (mission + agent-owned control model), 56-63 (campaign vocabulary).
- Corroborating product context: `CONTEXT.md` lines 5-13 (product definition: "agent-native engineering sensemaking and control layer"), 73-90 (top operating rule and loop), 284-290 (durable continuation principle), 361-369 (what is *not* ratified).
- `docs/agent-native-operating-workflow.md` lines 294-318 (CONTINUATION: desired principle vs current reality `CONVENTION_CLOSED`).

**(c) Verdict: RECONSTRUCTED.**

**(d) Note (not a shortfall for Q1 itself):** the record says its vocabulary comes "from the campaign charter" (line 56). No charter exists in the repository (`grep -rn "campaign charter"` hits only the record). The mission *text* is fully in the record, so Q1 does not depend on the charter; the charter's absence matters for the acceptance conditions (see Q7 item 5).

---

## Q2. Current capability state with respect to the mission

**(a) Reconstructed answer.** The *documentation-level* control model is complete and ratified: the agent owns the loop (ADR 0013), the product boundary is the human-reviewed brief (ADR 0014), execution authority is separated from recommendation with fail-closed consumers (ADR 0026), and registry identity is separated from liveness (ADR 0027, 8 of 23 registered workflows `compatibility_only`). What is *demonstrated by repeated real use* is narrower: brief production + mechanical validation on two repos, responsibility selection without routing (including clean stops at owner boundaries), claim reconciliation / repair verification, fail-closed authority tests, and deterministic probe enforcement in CI on `main`. What is *missing* is exactly the mission's central property: nothing durable carries campaign/task continuation state (continuation is `CONVENTION_CLOSED`, reopen trigger never fired), there is no representation of development direction (the only candidates are a stale `roadmap.md`, a validation-priority `STATUS.md`, and an authority-index map under trial), hooks are documented but not wired, Goal A external validation is halted on a harness substrate, and the old workflow system has liveness but no campaign-vocabulary disposition.

**Demonstrated (with repository evidence I verified):**

1. *Agent-native `repository_sensemaking_brief` production + mechanical validation on two structurally different repositories.* `experiments/evidence/0021-workflow-v0-first-dogfood/EVIDENCE.md` lines 1-60 (Auteur + self-pass, verdict "KEEP -- provisional"); `experiments/evidence/0022-workflow-v0-repeated-use/EVIDENCE.md` lines 1-70 and 146-190 (second independent run, both briefs "validator-PASSED", verdict `KEEP_WITH_WATCH_ITEMS`); the two frozen briefs sit in the 0022 directory.
2. *Responsibility selection without automatic routing, stopping at the owner/authority boundary.* Evidence 0022 lines 146-160 ("skipped unnecessary stages, and stopped at the owner boundary"); `experiments/evidence/0023-goal-a-run1-stop-boundary/EVIDENCE.md` lines 30-55 (Goal A halted at an owner/environment decision rather than a repo edit). Doctrine: `docs/adr/0018-workflow-routing-policy.md` lines 1-30 (SUPERSEDED, never accepted); `CONTEXT.md` line 146.
3. *Fail-closed authority on `auto_invoke_next_workflow` and on compatibility-only workflow selection.* `docs/adr/0026-workflow-execution-authority.md` lines 1-12; `docs/adr/0027-workflow-registry-liveness.md` lines 1-45; `skills/workflow-planner/references/workflow-liveness.yaml` (8 overrides listed); `tests/test_auto_invoke_authority_gating.py` and `scripts/workflow_liveness.py` exist (existence verified, not executed).
4. *Claim reconciliation and finding-specific repair verification.* `docs/agent-native-operating-workflow.md` lines 221-252 and Reality map lines 386-387 ("REAL + dogfooded (evidence 0018, 0020)", "(evidence 0019)"); evidence directories 0018/0019/0020 exist (`ls experiments/evidence/`). I did not open 0018-0020; this item rests on the operating-workflow doc plus directory existence.
5. *Deterministic probe-engine enforcement in CI on `main`.* `.github/workflows/validation.yml` jobs `probe-gate` (line 672; runs `probe-repo.py`, `validate-probe-report.py`, `gate_relationship_findings.py`) and `core-assertions` (line 703; 7 pytest files at line 720).

**Missing (with repository evidence I verified):**

1. *No durable artifact carries continuation state across responsibilities (G1).* `docs/2026-08-programmatic-runner-retirement-plan.md` lines 137-176: overall loop `CONVENTION_CLOSED`, prior-report selection `CONVENTION`, reopen trigger recorded ("when at least one real agent-native continuation cannot reconstruct ... without relying on conversational/session memory") and never fired. The only continuation contracts are thin: `session_summary` requires just `source_intent_ref` and is consumed only by `workflow-planner` (`skills/workflow-planner/references/artifact-contracts.yaml` lines 296-308); `prompt_handoff` is skill-to-skill prompt packaging for an `external_agent` (lines 524-548; `skills/handoff/SKILL.md` lines 1-25).
2. *No representation of repository-level development direction (G2).* `roadmap.md` lines 1-14 ("Phase 2.3 Complete", "Current Version: 0.2.1 (Beta)") vs `STATUS.md` lines 1-4 (0.2.2, 2026-08-26) -- staleness already recorded by evidence 0022 lines 55-60; `STATUS.md` is a product-validation-priority summary, not a direction; `docs/semantic-control-map.md` lines 1-19 is self-described as a "decision-support index only / NOT A SOURCE OF TRUTH" under an OPEN trial.
3. *Hooks: documented but not wired; prose predates ADR 0026 (G3).* `.claude/settings.json` is `{}`; `.claude/hooks/` contains only `sessionstart.md`; that file (lines 31-43) still teaches "When to auto-fix vs. escalate" and "Read the artifact: primary_fog_type, evidence, recommended_workflow", which is routing-era language.
4. *Goal A external validation halted on execution substrate.* Evidence 0023 lines 30-55: three substrates falsified (isolated sub-agent direct write blocked; framed return not lossless; external process cannot authenticate); owner v3 rule = stop in this environment. `docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md` lines 108-125 ("NOT READY for a compliant Run 1"; tracked in Issue #255).
5. *Old workflow system has liveness but no campaign-vocabulary disposition (G4).* ADR 0027 settles `active | compatibility_only`; nothing in the repo records `KEEP_AS_BOUNDED_SUBGRAPH | REPAIR | DEMOTE | RETIRE_CANDIDATE | HISTORICAL | INSUFFICIENT_EVIDENCE` per workflow id (grep for those tokens hits only the record).
6. *Minor, doc-level:* the `unevaluable` repair-verification verdict category is proposed but not in the contract (`docs/agent-native-operating-workflow.md` lines 249-252, 387).

**(b) Sources.** As cited inline; the record's own table is `CAMPAIGN-STATE.md` lines 67-86, 104-125.

**(c) Verdict: RECONSTRUCTED.** The record's capability table is accurate against every source I checked; I found no row it overstated.

---

## Q3. Why was R1 selected over other plausible work?

**(a) Reconstructed answer.** R1 (a fresh-context reconstruction probe) was chosen because the campaign's *central* property -- artifact-mediated continuation -- is the one capability that is both `CAMPAIGN_BLOCKING` (G1, G2) and never once tested; every other acceptance condition is either already met at the doc level (1-3), depends on traces that only later campaign work will produce (8-9), or is end-of-campaign qualification (10-13). The record refuses to build continuation machinery before observing the actual failure class, citing the repository's machinery-promotion rule (C7: formalize only after repeated real burden with a mechanically expressible boundary). This is precisely the operating rule the retirement-plan closure already wrote down: "record what the agent could and could not reconstruct; do not design the fix yet", with a reopen trigger that fires only on a *real* failed reconstruction. R1 is that reopen-trigger test, made deliberate. The R0 commit message (`git show 2bc8a2c`) confirms the sequence: reconstruct state -> record -> name R1 as next.

**Competing alternatives visible in the repository, and why each was not selected (the record's reasons, checked against sources):**

| Alternative | Where it is visible | Why not now |
|---|---|---|
| Run the next Goal A / A1 external-validation episode (the repo's stated "current product-validation priority") | `CONTEXT.md` 39-71; `STATUS.md` 6-24; `docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md` | Halted in this environment by the owner's v3 stop rule; blocker is a harness substrate, not a repo edit; needs fresh owner authorization (evidence 0023 lines 46-55; record C4). |
| Advance the semantic-control-map persistence trial | `docs/semantic-control-map-trial.md`, `-trial-log.md` | Protocol is event-driven with a minimum close of 2026-09-28; consultations must arise from ordinary work, never manufactured (trial doc lines 100-112; record C3). Only bookkeeping (G6) is warranted, and it is a side effect, not a campaign responsibility. |
| Continue the #226 gate-separation / C6R research program | `docs/research/control-model-research-agenda.md` lines 27-67, 446-450 | Research hypotheses are "not an ADR, not a product contract" (agenda header); `CONTEXT.md` 361-367 lists them as not ratified; the campaign mission is engineering capability, not research. |
| Docs-currency repair (roadmap.md, deferred runner-era docs) | evidence 0022 lines 55-70; record D3 | Classified `HISTORICAL_ONLY`; already recorded; does not move any acceptance condition. |
| Fix local test defects (D1 encoding, D2 collection errors) | `tests/test_path_drift.py` 154/228/358; `tests/test_integration_external_repo.py`; `tests/test_validate_brief_json.py` | `LOCAL_BUT_REAL`, not campaign-limiting; not in the gates that matter (record section 12). |
| Define hooks (G3) | `.claude/hooks/sessionstart.md`; `settings.json = {}` | U3 is gated on U1/U2: a hook is warranted only if a recurrent continuation event is observed that a manual step keeps missing. |
| Record per-workflow campaign dispositions (G4/U4) | ADR 0027; liveness yaml | Condition 9 "depends on real traces that only bounded campaign work will produce" (record section 9); cheap grep is possible but its result cannot change the next action before continuation is tested. |

**(b) Sources.** `CAMPAIGN-STATE.md` lines 116-125 (gaps), 129-138 (constraints), 141-150 (uncertainties, note U3/U5 gated on U1/U2), 153-158 (highest-leverage boundary), 162-185 (R1 spec incl. "WHY IT MATTERS"); `docs/2026-08-programmatic-runner-retirement-plan.md` lines 143-176; `docs/agent-native-operating-workflow.md` lines 308-318 and 416-437 (machinery promotion rule and the cross-run-identity example); `git show --stat 2bc8a2c`.

**(c) Verdict: RECONSTRUCTED.** The selection rationale is stated in the record and is independently derivable from the retirement-plan closure plus the operating-workflow promotion rule; I did not need conversation context to see why R1 beats the alternatives.

---

## Q4. What is established (no re-verification needed) vs still uncertain?

**(a) Established -- facts I confirmed directly from durable state and would not re-verify:**

- Branch/base: worktree is on `campaign/agent-native-self-development`, exactly one commit (`2bc8a2c`, R0, adds only `CAMPAIGN-STATE.md`, 232 lines) ahead of `main @ f10b7da`; working tree clean. (`git status`, `git log`, `git show --stat 2bc8a2c`.)
- ADR statuses: 0013 Accepted (ratified 2026-08-13, amendment scopes the runner as compatibility); 0014 Accepted (narrowed 2026-07-26, owner decision D1); 0026 Accepted 2026-08-24 (merged via PR #235); 0027 Accepted 2026-09-01 (issue #263 Option B); 0018 SUPERSEDED 2026-08-18, never accepted; 0023 Accepted, governance-only, authorizes nothing. (`docs/adr/*.md` headers.)
- The campaign record is read by nothing: `experiments/campaigns/` holds only `EXP-0001..0005` (ADR 0023 lane), confirming the record's "not an EXP-NNNN campaign" distinction is real.
- Workflow registry has 23 top-level ids; liveness overlay marks 8 `compatibility_only` (`workflow-registry.yaml`, `workflow-liveness.yaml`).
- CI on `main` (`.github/workflows/validation.yml`): 13 jobs; `validate` (scripts + one pytest invocation, lines 602-671), `probe-gate` (672), `core-assertions` (703; 7 files incl. `tests/test_path_drift.py` at line 720), `conditional-representation-exact-head` (738). So G6 is correct: map rows SE1/SA13/SA9 claiming these live only on `feat/enforcement-gate` are stale.
- Hooks: `.claude/settings.json` = `{}`; only `.claude/hooks/sessionstart.md` exists; its prose is routing-era.
- Continuation: retirement plan closed 2026-08-13; typed fan-in `CONTRACT_CLOSED`, loop `CONVENTION_CLOSED`; reopen trigger recorded, never fired (lines 137-176). `session_summary` contract = one required field, one consumer (contracts yaml 296-308).
- Semantic-control-map trial: OPEN since 2026-08-31 (`df46871`), min close 2026-09-28, max 2026-10-26; one trigger logged (PR #248); zero consultation/over-read events (`docs/semantic-control-map-trial-log.md` lines 6-40).
- Goal A: ACTIVE in docs, halted in this environment with three falsified substrates; owner v3 stop rule (evidence 0023; reassessment doc lines 108-125).
- Workflow v0 verdicts: 0021 "KEEP -- provisional"; 0022 `KEEP_WITH_WATCH_ITEMS` (Phase 9) with one FIRST_OBSERVED watch item F1 and a closure-selection watch item (addendum 2026-08-15).
- D1 textual claim verified: `tests/test_path_drift.py` lines 154, 228, 358 call `.read_text()` without `encoding`. D2 files exist; `scripts/validate_brief.py` does not (only `validate-brief.py`).
- Research meta-finding exists as stated: `docs/research/control-model-research-agenda.md` line 459-461 ("sensemaking loops saturated ... constructive spikes, not briefs", 2026-08-30).
- `docs/HARDENING_STATUS.md` line 17 still lists `integration_fog` (D4).

**Still uncertain (cannot be closed from the repository):**

- U1-U5 as listed in the record (lines 143-149). This file is the R1 evidence for U1; U2-U5 remain open.
- Whether the local test baseline is as described: I did not run any test, so D1's `UnicodeDecodeError` and D2's collection errors are unverified *behaviors* (text verified only). Record condition 12 says baseline capture is "in progress".
- Whether `main`'s `core-assertions` is currently green given map row SE2's claim that `test_path_drift.py` is "RED on main -- 5 failures" (`docs/semantic-control-map.md` line 61). Either SE2 is stale (likely, like SE1/SA13) or `main` is red; the repo does not say which (see Q7 item 2).
- Anything that lives only in GitHub: Issue #255's current state, #226's state, and especially the "3 normal-use episodes on Issue #218 (merge base-advance x2)" -- `docs/research/normal-use-evidence-lane.md` lines 131-133 say episodes are recorded as issue comments; nothing in the repo contains them (grep for "base-advance" hits only the record), and line 249 of that doc reads "new post-Path-4 normal-use episodes 0".
- Whether the campaign branch/R0 has been pushed or a PR opened: `git ls-remote --heads origin` shows no `campaign/agent-native-self-development`, so as of this probe it is local-only.
- Whether the R1 dispatch substrate (isolated sub-agent writing a file) works in this environment -- evidence 0023 says it did not for Goal A Run 1. The success or failure of *this file's write* is itself evidence on that point.

**(b) Sources.** As cited inline.

**(c) Verdict: RECONSTRUCTED.** The established/uncertain split matches the record; the additional uncertainties I list are ones the record should carry forward (Q7).

---

## Q5. What responsibility is warranted next, concretely?

**(a) Reconstructed answer.** The warranted responsibility *now* is R1 itself -- this probe -- and its close-out: produce `R1-fresh-context-reconstruction.md` with per-item verdicts and shortfall classes, then update the campaign record. If I were performing the follow-through right now, the first concrete action after this file exists is to **edit `CAMPAIGN-STATE.md`** (the only file the record's own RULE line 12 says must be updated after every consequential responsibility): append `R1` to section 3 (completed responsibilities) and section 4 (evidence), move U1 in section 8 from OPEN to RESOLVED or NARROWED with the observed shortfall classes (from this file: no `MISSING_DURABLE_STATE` failure on Q1-Q5; one narrow `AUTHORITY_AMBIGUITY` on Q6; five omissions in Q7), rewrite section 10 to name R2, and append a trace line to section 14. Tool: a plain file edit; no Skill, no workflow. After that, the record already points at R2 (U2's "cheapest sufficient evidence": one real multi-responsibility task trace continued from durable state without hidden conversation memory, acceptance condition 5), and the U5 question (ride on `session_summary`/`prompt_handoff` vs new artifact) becomes decidable only after R2.

The record does *not* name which real task R2 should use. The repository offers one candidate that is ordinary work, protocol-permitted, multi-step, and evidence-producing: the G6 trial bookkeeping -- log the `feat/enforcement-gate`-merge trigger in the trial log and refresh rows SE1, SE2, SA13, SA9 per the MECH refresh procedure (`docs/semantic-control-map-trial.md` lines 30-45, 52-58). That is my suggestion, not the record's.

**(b) Sources.** `CAMPAIGN-STATE.md` lines 12 (update rule), 90-100 (sections to append), 141-149 (U1/U2/U5 and their cheapest evidence), 162-185 (R1 spec and expected evidence), 228-232 (trace); `docs/semantic-control-map-trial.md` lines 30-58 (refresh procedure and trigger table).

**(c) Verdict: RECONSTRUCTED** for "what is warranted next" (R1 close-out -> record update -> R2). **(d)** For the step *after* that, the record names R2's shape but not its task; that is a mild `WARRANT_AMBIGUITY` for R2 only, not for the next action.

---

## Q6. What authority do I have?

**(a) Reconstructed answer.** From the repository: I may **know** anything inspectable (read, grep, git), and may run bounded probes of repository facts; I may **decide** reversible implementation details inside the current scope; I may **act** on local reversible work inside scope; I may **not** merge to `main`, alter ADR `**Status**` lines or owner decisions, write to external trackers, deploy, or infer publish/merge authority from green CI. For this task specifically, the only mutation authorized is writing this one output file (task scope) -- the record's C2 additionally claims agents may push branches and open PRs for exact-head qualification but not merge. Campaign-specific prohibitions: do not use the Skills/workflows/hooks as controller (C1); do not add semantic-control-map rows during the trial and log any consultation (C3; trial protocol `MAP_EXPANSION_DEFAULT = NO`); do not run Goal A episodes (C4). Owner decisions required: merge of campaign PR(s); any ADR/contract/registry/readiness change; anything Goal A. Standing repository rule: "Finding is not authorization" -- diagnosis does not expand scope.

**Sources for each authority claim:**

| Claim | Source |
|---|---|
| KNOW / DECIDE / ACT / PUBLISH split; merge requires explicit authorization; "remaining uncertainty is an owner decision" is a valid terminal state | `CONTEXT.md` lines 244-264; `skills/using-sensemaking/SKILL.md` lines 363-387; `docs/agent-native-operating-workflow.md` lines 355-371 |
| Finding != authorization; do not touch unrelated code; flag uncertainty | `AGENTS.md` rules 4-6 (lines 14-26) |
| Owner ratifies product boundary, execution authority, liveness (pattern: owner decision -> ADR Accepted) | ADR 0014 header (owner decision D1, `docs/OWNER-DECISION-PACKAGE-2026-07-26.md`); ADR 0026 header ("owner decision 2026-08-24"); ADR 0027 header ("Option B explicitly owner-ratified") |
| Merge to `main` is an owner decision; push branches / open PRs allowed; never falsify ADR status | `CAMPAIGN-STATE.md` line 132 (C2) -- the record's own claim |
| Map: do not add rows; log consultation/over-read; map never authoritative | `docs/semantic-control-map-trial.md` lines 20-27, 74-77, 95-112; `docs/semantic-control-map.md` lines 3-18 |
| Goal A: no episode without fresh owner authorization; halted in this environment | evidence 0023 lines 3-5, 46-55; `CAMPAIGN-STATE.md` line 134 (C4) |
| Campaign controller constraint (no Skills/workflows/hooks as controller) | `CAMPAIGN-STATE.md` line 131 (C1) -- record-only |
| Tracker writes need explicit authority | `docs/agent-native-operating-workflow.md` line 361 (ADR 0019 PROPOSED) |

**(b) Sources.** As tabled.

**(c) Verdict: PARTIAL.**

**(d) What is missing, and class: `AUTHORITY_AMBIGUITY` (narrow).** Three things could not be sourced from durable repository state:
1. C2 cites a "Mode B+ standing boundary" as the source of the merge rule. Nothing in the repository defines Mode B+; the only in-repo reference (`docs/candidate/architecture-decision.md` line 7) links to `docs/prototypes/repo-sensemaker-vnext.md`, which does not exist. The *content* (merge = owner) is reconstructable from other sources, so the practical effect is small, but the *breadth* of delegation that Mode B+ apparently granted (autonomous architecture/packaging/schema/test decisions on a branch) cannot be confirmed or bounded from the repo.
2. Whether "push branches and open PRs" is a standing authorization for this campaign or a per-PR request is asserted only by the record (line 132); no `AGENTS.md`/ADR rule states it (repository practice -- many `origin/agent/*` branches -- is consistent with it, but practice is not authority).
3. Whether, after R1, an agent may *implement* continuation machinery on this branch without an owner check-in. C7 gives a *criterion* for formalization (`CAMPAIGN-STATE.md` line 137; operating workflow lines 416-437), and the record says "None blocking at R0" (line 191), but neither says who authorizes crossing from "candidate for formalization" to "implemented on the campaign branch". Under the repo's default ("Can DECIDE? reversible implementation details ... within scope"), a branch-only, non-ratified artifact is probably agent-decidable -- but that is my inference, not a sourced authority.

---

## Q7. Contradictions, or things the record should have told me but did not

1. **R1's execution substrate collides with evidence 0023, and the record does not say so.** The R1 spec (`CAMPAIGN-STATE.md` lines 174-180) dispatches "ONE fresh agent context" to write `R1-fresh-context-reconstruction.md`. `experiments/evidence/0023-goal-a-run1-stop-boundary/EVIDENCE.md` lines 34-49 records that in this environment an isolated task sub-agent's direct file write was **blocked** (substrate 1) and its framed return was **not lossless** (substrate 2). The record should have flagged that R1's dispatch method is the same falsified substrate and stated the fallback. (If this file persisted, that is new evidence narrowing the #255 substrate-1 claim -- worth recording in the trial log / #255; if it did not, the verbatim return in the dispatcher's transcript is the only copy.)
2. **G6 omits SE2, and the record's baseline is silent on whether `main` CI is green.** `docs/semantic-control-map-trial.md` line 56 says the `feat/enforcement-gate` merge trigger refreshes **SE1, SE2, SA13, SA9**; the record's G6 (line 125) names SE1/SA13/SA9 only. Map row SE2 (`docs/semantic-control-map.md` line 61) claims `tests/test_path_drift.py` is "RED on `main` -- 5 failures", yet `core-assertions` on `main` runs that file (`.github/workflows/validation.yml` line 720). Either SE2 is stale or `main` is red; D1 (line 199) discusses only the Windows encoding failure and says "CI ... is unaffected" without establishing that. Condition 12 ("baseline capture in progress") should have recorded the last known `main` CI result.
3. **The campaign branch has not been pushed, and the record does not say.** `git ls-remote --heads origin` returns no `campaign/agent-native-self-development`. C2 (line 132) anticipates "push branches and open PRs", but neither section 4 nor section 14 records push/PR status. A fresh context on any other machine could not find this record at all -- a continuation-relevant fact for exactly the property this campaign tests.
4. **"3 normal-use episodes on Issue #218 (merge base-advance x2)" is not reconstructable from the repository and appears to conflict with a repo doc.** The claim (lines 82, 109) rests on GitHub issue comments (`docs/research/normal-use-evidence-lane.md` lines 131-133: "one issue comment per qualifying episode"); grep for "base-advance" hits only the record. `normal-use-evidence-lane.md` line 249 states "new post-Path-4 normal-use episodes 0". Either that doc is stale or the three episodes are pre-Path-4; the record cites them as current evidence for a demonstrated capability without noting they live outside durable repository state (`MISSING_DURABLE_STATE` for that evidence line).
5. **Two cited sources do not exist in the repository: the "campaign charter" and "Mode B+".** The record derives its finding classes, reconstruction-failure classes, workflow dispositions, and the 13 acceptance conditions "from the campaign charter" (line 56) -- no such document is in the repo; section 13 paraphrases the conditions, which is why Q1-Q5 still succeeded, but the charter's authoritative wording is conversation-only. "Mode B+" (line 132) is likewise undefined in the repo, with a dangling pointer at `docs/candidate/architecture-decision.md` line 7 -> `docs/prototypes/repo-sensemaker-vnext.md` (missing). Both should either be committed alongside the record or the record should state that they are not durable.

(Also noted, not counted: the hook doc `.claude/hooks/sessionstart.md` line 214 says "Hook registration: `CLAUDE.md` (SessionStart section, below)" while `CLAUDE.md` says the hook is available and `settings.json` is `{}` -- the record already covers this as G3.)

---

## Reconstruction cost

- **Files opened (read in whole or in part): 39.** `CAMPAIGN-STATE.md`; `CONTEXT.md`; `docs/decision-orchestration-boundary.md`; `docs/agent-native-operating-workflow.md`; `.claude/settings.json`; `.claude/hooks/sessionstart.md`; ADRs 0013, 0014, 0018, 0023, 0026, 0027; `docs/2026-08-programmatic-runner-retirement-plan.md`; `docs/semantic-control-map.md`; `docs/semantic-control-map-trial.md`; `docs/semantic-control-map-trial-log.md`; `skills/workflow-planner/references/workflow-liveness.yaml`, `workflow-registry.yaml`, `artifact-contracts.yaml`; `.github/workflows/validation.yml`; `STATUS.md`; `roadmap.md`; `tests/test_path_drift.py` (3 lines); `experiments/evidence/0021`, `0022`, `0023` `EVIDENCE.md`; `docs/research/control-model-research-agenda.md`; `docs/research/normal-use-evidence-lane.md`; `docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md`; `skills/using-sensemaking/SKILL.md`; `skills/handoff/SKILL.md`; `AGENTS.md`; `CLAUDE.md`; `docs/HARDENING_STATUS.md`; `docs/agents/domain.md`; `docs/agents/issue-tracker.md`; `docs/candidate/architecture-decision.md` and `completion-report.md` (grep hits only); `docs/OWNER-DECISION-PACKAGE-2026-07-26.md`. Plus directory listings (`docs/`, `docs/adr/`, `docs/research/`, `docs/agents/`, `experiments/`, `experiments/evidence/`, `experiments/campaigns/`, `.claude/`) and repo-wide greps.
- **Tool calls: 25** (1 Read of the record; 3 Reads of the three core docs + 1 Read of the hook doc; 19 Bash calls, mostly batched multi-file reads/greps/git; 1 Write). Reads to reach each answer, roughly: Q1 -- 1 (record) + 1 (CONTEXT.md) for corroboration; Q2 -- ~8 batched calls (ADRs, evidence heads, CI, liveness, contracts); Q3 -- 2 beyond Q2 (retirement-plan closure; research agenda); Q4 -- 3 beyond Q3 (trial log/protocol; Goal A reassessment; existence checks); Q5 -- 0 additional; Q6 -- 3 (using-sensemaking §12-14, AGENTS.md, Mode B+ grep); Q7 -- 2 (CI job bodies; remote-branch/grep sweep).
- **Three most load-bearing files:** (1) `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` -- carried mission, gaps, constraints, uncertainties, and R1's rationale; every other read was verification. (2) `docs/2026-08-programmatic-runner-retirement-plan.md` lines 137-176 -- the single passage that explains *why* continuation is `CONVENTION_CLOSED`, what the reopen trigger is, and why "do not design the fix yet" makes R1 the right move. (3) `CONTEXT.md` -- mission grounding, authority model, and the "not ratified" list that disposes of the research alternatives. Runner-up: `.github/workflows/validation.yml` (settled G6 and exposed the SE2 omission) and evidence 0023 (exposed the substrate collision).
- **Dead ends:** `docs/OWNER-DECISION-PACKAGE-2026-07-26.md` (only reconfirmed the owner-decision convention already visible in ADR headers); `docs/agents/issue-tracker.md` (told me episodes live in GitHub -- a useful negative, no content); `skills/handoff/SKILL.md` (marginal for U5); `docs/HARDENING_STATUS.md` (trivially confirmed D4); the `docs/prototypes/` lookup for Mode B+ (directory does not exist -- the negative became Q7 item 5); `roadmap.md` (confirmed stale, nothing else).
