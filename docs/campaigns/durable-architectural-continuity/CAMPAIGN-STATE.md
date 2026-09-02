# Campaign 3 durable state — Durable Architectural Continuity During Coupled Implementation

```
VERSION:    v2 (post-Phase-1). Phase 1 complete. No coupled product capability
            was warranted; no partial architecture created; no controller
            succession performed. v1 (bootstrap) assessments are preserved
            below, marked where superseded.
STATUS:     CLOSING. Lead Controller A active. Phase 1 disposition:
            NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED. Final campaign disposition
            recorded in FINAL-REPORT.md and section 19.
AUTHORITY:  non-authoritative. Not an ADR, contract, schema, registry, validator
            input, or registered workflow. Nothing in scripts/, src/, tests/, or
            .github/ reads this file.
OWNER INSTR: docs/campaigns/durable-architectural-continuity/OWNER-INSTRUCTION.md
             (verbatim; the campaign's authority source)
CHARTER:    docs/campaigns/durable-architectural-continuity/CHARTER.md (derived)
PROVENANCE: docs/campaigns/durable-architectural-continuity/STARTUP-PROVENANCE.md
BRANCH:     campaign/durable-architectural-continuity
WORKTREE:   H:/GithubRepositories/smk-campaign3
RULE:       update after every consequential campaign responsibility and before
            every strategic selection / handoff. Facts here are CLAIMS; a
            continuing controller reverifies consequential claims from repository
            / GitHub evidence before acting (durable-state epistemics).
PRESERVE:   prior assessments are kept, not rewritten as if earlier controllers
            always knew the current answer. New versions append; superseded
            assessments are marked, not deleted.
```

This file carries **campaign architectural + semantic state** (strategic
rationale, capability assessment, candidate architecture, cross-surface
obligations, decision status, evidence ceilings, uncertainties, integration
state, controller state, campaign disposition) — not repository factual state
(verify from repo/GitHub) and not short-horizon task state.

---

## 1. CAMPAIGN MISSION

`OWNER-INSTRUCTION-DERIVED` / `CHARTER-DERIVED`. See `CHARTER.md` "CAMPAIGN
MISSION" for the operating contract and `OWNER-INSTRUCTION.md` for the full
mandate.

Advance Sensemaking Skills through the highest-leverage currently warranted
in-authority product development; assess whether the naturally warranted work
exposes a capability whose smallest coherent implementation is genuinely
semantically coupled across multiple product surfaces; and if so, hand semantic
campaign control at a coherent-but-incomplete architectural boundary to a fresh
controller to test whether **architectural intent** survives controller
replacement during real development.

**Central question.** Can architectural intent — not merely task state or
strategic direction — survive semantic campaign-controller replacement while a
genuinely coupled product capability is still incomplete?

**Order of operations is fixed:** product need -> task selection -> assess
natural coupling -> experiment if warranted. Never search for a task to fit the
experiment.

## 2. STATE PLANES (re-record before every strategic selection / handoff)

```
STARTING ORIGIN/MAIN (Campaign 3 base):  969e8eb47144ffdeb27a8d9df02b6a292586e842
   969e8eb  "Merge pull request #270 from ThorStarlord/docs/campaign2-closure-stamp"
   verified 2026-09-02: `git fetch origin --prune; git rev-parse origin/main`.
CAMPAIGN BASE:                            969e8eb  (branch forked here)
CURRENT ORIGIN/MAIN OBSERVATION:          969e8eb  (== base; no drift as of 2026-09-02)
CURRENT CAMPAIGN HEAD:                    <this v2 commit> (follows 2fd1027 =
   controllers/A-selection.md; b677ffb = bootstrap)
MAIN DRIFT SINCE CAMPAIGN START:          none (re-checked 2026-09-02:
   `git log 969e8eb..origin/main` empty)
CANDIDATE CHANGES NOT ON MAIN:            only the Campaign 3 instrumentation dir
   docs/campaigns/durable-architectural-continuity/ (OWNER-INSTRUCTION, CHARTER,
   CAMPAIGN-STATE, STARTUP-PROVENANCE, controllers/README, controllers/
   A-selection). **No product surface touched** — Phase 1 concluded no coupled
   capability was warranted.
INTEGRATION STATUS:                       nothing merged. A draft PR may be
   opened as a durable campaign-evidence surface + exact-head CI (Campaign 2
   precedent); it is not for merge.
WHICH CLAIMS APPLY TO MAIN:               everything in §3-§5 (Campaign 1 + 2
   results are integrated on main via PR #268 / #269 / #270).
WHICH CLAIMS APPLY ONLY TO CAMPAIGN HEAD: none yet.
OWNER / RATIFICATION STATUS:              no owner decision pending from
   Campaign 3 yet.
```

PR #269 integration verified: merge commit `7e48cf0` is an ancestor of `969e8eb`
(`STARTUP-PROVENANCE.md` §2). PR #270 merge commit `969e8eb` **is** current
`origin/main` HEAD.

## 3. CURRENT INTEGRATED PRODUCT ASSESSMENT (`origin/main` @ 969e8eb)

`REPOSITORY-VERIFIED` (durable docs read 2026-09-02) + `GITHUB-VERIFIED`
(#268/#269/#270 merged). Consequential claims to be reverified by each
controller before acting.

- **Product definition** (`CONTEXT.md`): agent-native engineering sensemaking
  and control layer for software-engineering agents. Active coding agent owns
  the recursive control loop (ADR 0013). Ratified external product scope = the
  validated, human-reviewed `repository_sensemaking_brief` (ADR 0014). Automatic
  fog-type -> implementation routing is NOT ratified.
- **Control model** documented: `docs/agent-native-operating-workflow.md`,
  `docs/decision-orchestration-boundary.md`, ADRs 0013/0014/0015-addendum/0023/
  0024/0025/0026/0027. Warrant / recommendation / selection / execution
  authority are separated; consumers fail closed.
- **Campaign 1 (PR #268, merged `06a57d1`)**: documented responsibility-level
  artifact-mediated continuation pattern; consolidated deterministic-machinery +
  hooks disposition; `docs/workflow-system-disposition.md` (23 workflows
  classified); lazy `workflow_liveness` resolver in
  `scripts/_validator_utils.py`. Disposition `CAMPAIGN_COMPLETE`. No ADR /
  contract / registry / `src/` change.
- **Campaign 2 (PR #269 merged `7e48cf0`; closure stamp PR #270 `969e8eb`)**:
  Task A — `STATUS.md` refreshed into a current-direction + reconstruction
  surface + reading path; `roadmap.md` / `goal.md` historical headers;
  `CONTEXT.md` +1 source-of-truth row. Task B — `scripts/probe_relationships.py`
  live-document classifier honors an opt-in `<!-- doc-status: historical -->`
  marker; marker applied to `roadmap.md` / `goal.md`; +4 regression tests.
  Disposition `CAMPAIGN_COMPLETE`. **Owner left the `doc-status` marker
  NON-NORMATIVE** (probe heuristic, not a ratified convention). No ADR /
  contract / canonical-vocab / registry / `src/` change.
- **Repository posture**: **"harden only where pressured"** (`CONTEXT.md`
  principle 10). Campaign 1 closed with "no further product change is warranted
  by current evidence." Research-agenda meta-finding 2026-08-30: "sensemaking
  loops saturated ... Future agents should not re-run sensemaking diagnosis to
  test this claim."
- **Highest-leverage next boundary** (`STATUS.md`): owner/environment decision
  on the Goal A execution substrate (Issue #255) — **not a repo-code
  deliverable**. In-authority engineering backlog **deliberately small**: the
  nine `docs/workflow-system-disposition.md` §6 items (owner-reserved
  registry/overlay/contract/doc micro-decisions); test-expectation debt
  D2b / D19; the `docs/` reconstruction surface itself.
- **Open issues**: #218, #226, #255 — all research / owner-reserved.
- **Open PRs**: only #194 (draft, "do not merge").
- **CI on `main`**: "Validator Ecosystem" (`.github/workflows/validation.yml`),
  ~19-20 jobs. Reported green on the `969e8eb` lineage (to be reconfirmed per
  controller).

## 4. DEMONSTRATED CAPABILITIES INHERITED (integrated on `main`)

- **Product** (`REPOSITORY-VERIFIED` + `GITHUB-VERIFIED`): agent-native brief
  production + deterministic validation on >=2 repositories;
  responsibility-before-Skill selection without routing; claim reconciliation;
  finding-specific repair verification; fail-closed authority on auto-invoke and
  liveness; probe-engine enforcement gate in CI; a current-direction Markdown
  surface (`STATUS.md`) + reconstruction reading path + historical-in-place
  markings honored by the deterministic drift machinery.
- **Campaign / succession** (from Campaigns 1 + 2, `CANDIDATE`/`GITHUB-VERIFIED`
  then integrated): Campaign 1 — persistent controller -> fresh bounded workers,
  durable execution continuity. Campaign 2 — Controller A -> durable strategic
  state -> fresh Controller B -> independent reconstruction -> re-verification ->
  predecessor-frontier disagreement -> independent strategic selection ->
  qualified product work. Durable strategic continuity.

## 5. EVIDENCE CEILINGS (inherited; `OWNER-INSTRUCTION-DERIVED` + Campaign 2)

See `STARTUP-PROVENANCE.md` §4 for detail.

- **EC-a** Campaign 2 did NOT establish: independent process/model succession;
  concurrent controllers; universal autonomous repository development; **deep
  coupled multi-surface implementation under succession** (the boundary
  Campaign 3 targets); formal Sensemaking Skills self-hosting; strict minimality
  of durable continuation state.
- **EC-b** Succession isolation: context isolation `HARNESS_REPORTED`;
  bootstrap-minimality / checkpoint-immutability / non-resumption
  `CONTROLLER_ASSERTED`; predecessor process non-persistence + model
  independence `SUCCESSION_ISOLATION_UNVERIFIED` (same `claude-sonnet-5`
  family; the `Agent` subagent returns its report to the parent).
- **EC-c** Scale: n=1..2 controllers, one repository, short horizon.
- **EC-d** Strict minimality: no comparative / staged-reveal / withheld-field
  evidence.
- **EC-e** Implementation depth: no broad `src/` or multi-surface depth from
  durable state demonstrated (Campaign 2 lifted only modestly — one `scripts/`
  file + 4 tests).

## 6. SELECTED PRODUCT CAPABILITY

**NONE.** Phase 1 (Controller A, `controllers/A-selection.md`, committed
`2fd1027`) concluded **`NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`**.

> v1 said this was "NOT YET SELECTED" with `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`
> a "live possibility". Phase 1 confirmed it.

Summary of the Phase 1 finding (full detail + 8-candidate survey in
`controllers/A-selection.md`):

- The repository is in a deliberate, multiply-corroborated **"harden only where
  pressured / sensemaking loops saturated / no further product change warranted"**
  posture (`CONTEXT.md` principle 10; Campaign 1 closure; Campaign 2 BF-1;
  research-agenda meta-finding 2026-08-30).
- The single highest-leverage product boundary — **Goal A external product
  validation** — is **owner-reserved** and paused at a substrate boundary its
  own durable evidence classifies as **non-product-surface** /
  `HARNESS_ENVIRONMENT_FAILURE` / "needs an owner/environment decision, not a
  repo-code change" (Issue #255; `goal-a-execution-readiness-reassessment-2026-08-31.md`).
- Every in-authority item is an owner-reserved micro-decision (the nine
  `docs/workflow-system-disposition.md` §6 items), pre-existing non-capability
  engineering debt (D2b / D19 / hygiene / stale `egg-info`), or instance cleanup
  explicitly deemed premature or "not a capability" (DB-1..3, MG-8).
- The only two **genuinely coupled** candidates are **C-8 MODEL_WARRANT `FULL`
  materialization** — deferred by **ratified ADR 0015** ("FULL remains deferred
  and is never inferred", line 182; `warrant_gate.py:146-148`) with zero
  real-use pressure — and **C-4 the `unevaluable` verdict category** — a "v0
  note" behind an unmet machinery-promotion gate. Neither can be selected
  without contradicting ratified authority / the repository's own promotion
  gate, and neither carries a product warrant independent of the experiment.
- An **independent fresh general-purpose sub-agent context** (no Campaign 3
  mission; scoped away from this directory) independently reconstructed the same
  frontier and returned the same verdict.

## 7. CANDIDATE ARCHITECTURE

None. No product capability selected -> no architectural decisions. (Phase 2 not
entered.)

## 8. ARCHITECTURAL OBLIGATIONS

None. No semantic change made. (Phase 3 not entered.)

## 9. TRANSITIONAL STATE

None. **No partial implementation was created** — Phase 1 concluded no coupled
capability was warranted, so Controller A did not (and must not) manufacture a
partial architecture for the experiment. No handoff to a fresh Controller B was
performed.

## 10. TEMPORARY EXCEPTIONS / EXPECTED FAILURES / UNEXPECTED FAILURES

None introduced by Campaign 3. Pre-existing platform reds on `main` are recorded
in `STARTUP-PROVENANCE.md` §6.

## 11. OPEN UNCERTAINTIES (decision-changing)

- **U-1 — RESOLVED (Phase 1).** Is there a currently-warranted, in-authority
  product capability whose smallest coherent implementation is genuinely
  semantically coupled across multiple product surfaces — without distorting
  real product priority? **No.** Confirmed by Controller A's 8-candidate survey
  and an independent fresh-context probe (`controllers/A-selection.md`). The
  genuine frontier is owner-reserved; the coupled candidates are ratified-defer
  / promotion-gate-blocked.
- **U-2 — MOOT (Phase 1).** No coupled candidate has a product warrant
  independent of the experiment (C-8 deferred by ratified ADR; C-4 behind an
  unmet promotion gate), so none can "dominate on product value."
- **U-3 — not exercised.** A fresh Controller B is instantiable at the same
  `HARNESS_REPORTED` context-isolation ceiling Campaign 2 used
  (`STARTUP-PROVENANCE.md` §8; process/model isolation
  `SUCCESSION_ISOLATION_UNVERIFIED`). Not exercised for a handoff because no
  coupled partial architecture was created to hand off. A fresh context WAS used
  as an ordinary corroboration instrument for the Phase 1 finding (not a
  controller succession).

## 12. AUTHORITY / OWNER BOUNDARIES

See `CHARTER.md` "AUTHORITY" + "OWNER-RESERVED DECISIONS" and
`STARTUP-PROVENANCE.md` §7. Summary: full local engineering + push + draft PR on
the campaign branch; NOT merge / ratification / ADR acceptance / owner-reserved
items / issue bookkeeping / unrelated PR merges / protected-policy edits /
inferring owner preference.

Standing owner-reserved (verify current state before relying): the nine
`docs/workflow-system-disposition.md` §6 items; Goal A substrate (Issue #255);
ratifying any Campaign 2 conclusion incl. the non-normative `doc-status` marker;
formal Campaign 2 termination (already closed).

## 13. REJECTED / SUPERSEDED STRATEGIC OPTIONS

Eight candidate capability boundaries were surveyed and none selected
(`controllers/A-selection.md` Part 2):

- **C-1 Goal A substrate repair** — owner-reserved + environment-blocked +
  explicitly non-product-surface (Issue #255).
- **C-2 nine `workflow-system-disposition.md` §6 decisions** — owner-reserved;
  bounded local registry/doc edits, no shared invariant.
- **C-3 extend `doc-status` marker to other historical-in-place root docs** —
  instance cleanup, single-surface, edges against the owner's NON-NORMATIVE
  decision on the marker.
- **C-4 `unevaluable` verdict for `repair_verification_report`** — mildly
  coupled but the machinery-promotion gate is explicitly unmet (a "v0 note",
  no failure evidence).
- **C-5 mechanical staleness signal for `STATUS.md` (MG-8)** — Campaign 2
  deemed it "premature; needs a demonstrated recurrence"; none has occurred.
- **C-6 C1/C2 formative-critique / independent-review** — "candidate / inactive"
  research; no execution program authorized.
- **C-7 engineering debt (D2b / D19 / platform reds / stale `egg-info`)** —
  pre-existing, deferred, none in CI, none capability-level.
- **C-8 MODEL_WARRANT `FULL` materialization** — genuinely coupled, but
  **deferred by ratified ADR 0015** with zero real-use pressure; reopening is
  `OWNER_DECISION_REQUIRED`.

## 14. DEFERRED LOCAL FINDINGS (inherited context, not Campaign 3 work)

From Campaign 2 (`CAMPAIGN-STATE.md` §14, `FINAL-REPORT.md` §15) — recorded as
context so a controller does not mistake them for a capability frontier:

- **DB-1** `CHANGELOG.md` "Deployment Timeline" footer lists a superseded plan
  (already `historical`-class to the probe; human-readability only).
- **DB-2** Other historical-in-place root docs still `live` to the probe:
  `integration-report.md`, `integration-design.md`, `adoption-finalization.md`.
  The `doc-status` marker mechanism supports fixing these but the owner left the
  marker NON-NORMATIVE; Campaign 2 classed this as "instance cleanup, not a
  capability".
- **DB-3** `docs/campaigns/**` records classified `live` contribute
  quoted-evidence noise to `version` / `adr/status_claim_mismatch` findings
  (FO-4 false-positives). Suppressing needs a judgment call on classifying
  evolving campaign state "historical".
- **MG-8** `STATUS.md` is a hand-maintained current-direction surface with no
  mechanical staleness signal of its own; a staleness validator was deemed
  "premature; needs a demonstrated recurrence" (formalization rule).
- **Engineering debt**: D2b (fixture drift), D19, two platform reds, stale
  `egg-info` version — pre-existing, deferred, none in CI, none capability-level.

## 15. INTEGRATION / CI STATE

```
commits:       b677ffb (bootstrap), 2fd1027 (Controller A Phase 1 selection),
               <this v2 commit>, + FINAL-REPORT commit.
pushed:        <to be pushed to origin/campaign/durable-architectural-continuity>
PR:            draft campaign-evidence PR to be opened (NOT for merge).
origin/main:   969e8eb  (== campaign base; no drift 2026-09-02).
campaign CI:   n/a until pushed; only docs/campaigns/** touched (no product
               surface), so no product qualification is at stake.
merged:        nothing from Campaign 3; nothing will be.
```

## 16. CONTROLLER TRACE (append-only)

```
2026-09-02  Controller A  bootstrap: Phase 0 preflight complete
                          (STARTUP-PROVENANCE.md); isolated worktree
                          H:/GithubRepositories/smk-campaign3 + branch
                          campaign/durable-architectural-continuity @ 969e8eb;
                          OWNER-INSTRUCTION / CHARTER / CAMPAIGN-STATE /
                          STARTUP-PROVENANCE + controllers/README committed
                          (b677ffb).
2026-09-02  Controller A  Phase 1: reconstructed current product state at
                          origin/main 969e8eb; surveyed 8 candidate capability
                          boundaries (C-1..C-8); ran an independent fresh
                          general-purpose sub-agent probe (no Campaign 3
                          mission; scoped away from this dir) that converged on
                          the same verdict; reverified the one new claim it
                          raised (C-8: warrant_gate.py:146 + ADR 0015:182).
                          controllers/A-selection.md committed (2fd1027).
                          PHASE 1 OUTCOME: NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED.
2026-09-02  Controller A  CAMPAIGN-STATE v2 + FINAL-REPORT.md. Final campaign
                          disposition: NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED.
                          No handoff (nothing to hand off). No Controller B.
                          Not merging; not ratifying; not opening/closing any
                          owner-reserved item.
```

## 17. HANDOFF PROVENANCE

Not applicable. No coupled partial architecture was created, so no controller
handoff was performed. A fresh sub-agent context was used only as an ordinary
corroboration instrument for the Phase 1 finding (recorded in
`controllers/A-selection.md` Part 5), not as a semantic controller succession.

## 18. SUCCESSION ISOLATION CEILING

`HARNESS_REPORTED_ISOLATION` for context isolation;
`SUCCESSION_ISOLATION_UNVERIFIED` for predecessor-process non-persistence and
model independence (same as Campaign 2; `STARTUP-PROVENANCE.md` §8). **Not
exercised for a controller handoff.** Campaign 3 adds no new succession-isolation
evidence.

## 19. CAMPAIGN DISPOSITION

**`NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`.**

The repository does not currently expose a warranted, in-campaign-authority
product capability whose smallest coherent implementation is genuinely
semantically coupled across multiple product surfaces, and none could be
selected without distorting real product priority. Per the owner instruction
this is "a legitimate campaign result, not a failure." The central
architectural-continuity question (can architectural intent survive controller
replacement during coupled implementation?) is **not answerable by Campaign 3**
because its precondition — a warranted coupled capability — is absent in the
repository's current development posture. Full reasoning: `FINAL-REPORT.md`.

Not `CAMPAIGN_PREMISE_INVALIDATED` (the premise is not shown wrong or
irrelevant, only unexercisable right now); not `OWNER_DECISION_REQUIRED` as a
disposition (no bounded campaign work is blocked awaiting an owner answer); not
`EXTERNAL_BLOCKER` (the fresh-controller substrate exists).
