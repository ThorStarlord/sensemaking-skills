# Campaign 3 durable state — Durable Architectural Continuity During Coupled Implementation

```
VERSION:    v1 (bootstrap). Pre-Phase-1. No product capability selected yet; no
            coupling assessed yet; no controller succession yet.
STATUS:     OPEN. Lead Controller A active. Disposition: UNDETERMINED.
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
CURRENT CAMPAIGN HEAD:                    <bootstrap commit — fill after commit>
MAIN DRIFT SINCE CAMPAIGN START:          none (2026-09-02)
CANDIDATE CHANGES NOT ON MAIN:            only the Campaign 3 instrumentation dir
   docs/campaigns/durable-architectural-continuity/ (OWNER-INSTRUCTION, CHARTER,
   CAMPAIGN-STATE, STARTUP-PROVENANCE, controllers/README). No product surface
   touched yet.
INTEGRATION STATUS:                       nothing merged; no PR opened yet.
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

**NOT YET SELECTED.** Phase 1 (Controller A capability discovery) has not run.
Prior evidence (§3) puts real doubt on whether any in-authority coupled
capability is currently warranted; `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`
and `CAMPAIGN_PREMISE_INVALIDATED` are live possibilities. This must be
determined by genuine Phase 1 analysis, not assumed.

## 7. CANDIDATE ARCHITECTURE

None. No architectural decisions recorded yet.

## 8. ARCHITECTURAL OBLIGATIONS

None. No semantic change made yet.

## 9. TRANSITIONAL STATE

None. No partial implementation exists.

## 10. TEMPORARY EXCEPTIONS / EXPECTED FAILURES / UNEXPECTED FAILURES

None introduced by Campaign 3. Pre-existing platform reds on `main` are recorded
in `STARTUP-PROVENANCE.md` §6.

## 11. OPEN UNCERTAINTIES (decision-changing)

- **U-1** Is there a currently-warranted, in-authority product capability whose
  smallest coherent implementation is genuinely semantically coupled across
  multiple product surfaces — without distorting real product priority? Prior
  evidence (§3: "harden only where pressured", "loops saturated", top boundary
  owner-reserved, backlog "deliberately small") leans NO, but Phase 1 must test
  this against the full product surface, not conclude abstractly.
- **U-2** If some coupled candidate exists, does it dominate the alternatives on
  **product value**, and would it remain warranted with no Campaign 3
  experiment attached?
- **U-3** Can a fresh Controller B be instantiated at an isolation level
  sufficient to run the architectural-continuity experiment? PRELIMINARY: yes,
  at the same `HARNESS_REPORTED` context-isolation ceiling Campaign 2 used
  (`STARTUP-PROVENANCE.md` §8); process/model isolation remains
  `SUCCESSION_ISOLATION_UNVERIFIED`.

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

None yet.

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
pushed:        nothing yet (bootstrap commit local only until first push).
PR:            none yet.
origin/main:   969e8eb  (== campaign base; no drift 2026-09-02).
campaign CI:   n/a (no push).
merged:        nothing from Campaign 3.
```

## 16. CONTROLLER TRACE (append-only)

```
2026-09-02  Controller A  bootstrap: Phase 0 preflight complete
                          (STARTUP-PROVENANCE.md); isolated worktree
                          H:/GithubRepositories/smk-campaign3 + branch
                          campaign/durable-architectural-continuity @ 969e8eb;
                          OWNER-INSTRUCTION / CHARTER / CAMPAIGN-STATE /
                          STARTUP-PROVENANCE + controllers/README committed.
                          Next: Phase 1 capability discovery.
```

## 17. HANDOFF PROVENANCE

Not yet applicable (no handoff).

## 18. SUCCESSION ISOLATION CEILING

Preliminary (`STARTUP-PROVENANCE.md` §8): `HARNESS_REPORTED_ISOLATION` for
context; `SUCCESSION_ISOLATION_UNVERIFIED` for predecessor-process
non-persistence and model independence. Same as Campaign 2.

## 19. CAMPAIGN DISPOSITION

**UNDETERMINED.** Phase 1 pending.
