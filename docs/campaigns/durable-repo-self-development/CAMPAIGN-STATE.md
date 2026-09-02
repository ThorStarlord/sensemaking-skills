# Campaign 2 durable semantic state — Durable Repository-Level Self-Development

```
STATUS:     ACTIVE (v3). Task A executed to its legitimate boundary (product
            change committed + qualified). Next: Controller A mandatory handoff
            to a genuinely fresh Controller B, then relinquish.
AUTHORITY:  non-authoritative. Not an ADR, contract, schema, registry, validator
            input, or registered workflow. Nothing in scripts/, src/, tests/,
            or .github/ reads this file.
CHARTER:    docs/campaigns/durable-repo-self-development/CHARTER.md
OWNER INSTR: docs/campaigns/durable-repo-self-development/OWNER-INSTRUCTION.md
            (verbatim; the campaign's authority source)
BRANCH:     campaign/durable-repo-self-development
WORKTREE:   H:/GithubRepositories/smk-campaign-2  (Controller A; worktree-per-session)
NOT:        an EXP-NNNN governed experiment campaign (ADR 0023 two-lane machinery
            does not read this file; no approval envelope applies).
RULE:       update after every consequential campaign responsibility and before
            every strategic selection / handoff. Facts here are CLAIMS; a
            continuing controller reverifies consequential claims from repository
            / GitHub evidence before acting (durable-state epistemics, charter
            constraint 10).
PRESERVE:   prior assessments are kept, not rewritten as if earlier controllers
            always knew the current answer. New versions append; superseded
            assessments are marked, not deleted.
```

This file exists so campaign reasoning does not live only in one conversation's
context. It carries **campaign semantic state** (rationale, capability
assessments, strategic alternatives, evidence ceilings, uncertainties, owner
decisions, reopen conditions, controller observations) — not repository factual
state (verify that from the repo/GitHub) and not short-horizon task state.

---

## 1. CAMPAIGN MISSION INTERPRETATION

`CHARTER-DERIVED` / `OWNER-INSTRUCTION-DERIVED`.

Advance Sensemaking Skills from Campaign 1's demonstrated **responsibility-level**
artifact-mediated continuation toward **durable repository-level
self-development**: independent *fresh controllers* reconstruct product-development
state, pick the highest-leverage warranted boundary, do substantial bounded
engineering, update durable state, and leave the repo continuable by another
fresh controller with no prior conversation context.

Two inseparable halves: **real product development** + **controlled
controller-succession evidence**. Product work must not be chosen to make the
experiment pass; instrumentation must not be dressed as product advancement.

**Central question.** The smallest coherent *product* capability sufficient for
repository-level development direction to survive independent controller
replacement and keep producing strategically warranted engineering work.

Campaign 1's distinct limitation this campaign targets: Campaign 1 ran a
**persistent dispatcher** that chose every responsibility; its fresh contexts
were **fresh workers, not fresh controllers**. Campaign 2's defining requirement
is genuine transfer of *semantic decision-making authority* to a fresh controller
that owns next-task selection.

## 2. CHARTER PATH / AUTHORITY SOURCE

- Authority source: `docs/campaigns/durable-repo-self-development/OWNER-INSTRUCTION.md`
  (owner instruction, delivered 2026-09-02, preserved verbatim, immutable).
- Operating contract: `docs/campaigns/durable-repo-self-development/CHARTER.md`
  (derived; subordinate).
- Startup provenance: `docs/campaigns/durable-repo-self-development/STARTUP-PROVENANCE.md`.
- Controller checkpoints: `docs/campaigns/durable-repo-self-development/controllers/`.

## 3. STATE PLANES (re-record before every strategic selection / handoff)

```
STARTING ORIGIN/MAIN (campaign base):  06a57d1d182a32684275d343a9248429feedbfe6
   06a57d1  "Merge pull request #268 from ThorStarlord/campaign/agent-native-self-development"
   verified 2026-09-02 by `git fetch origin --prune; git rev-parse origin/main`.
CAMPAIGN BASE:                          06a57d1  (campaign branch forked here)
CURRENT ORIGIN/MAIN OBSERVATION:        06a57d1  (== base; no drift, re-checked 2026-09-02 v2)
BOOTSTRAP COMMIT:                       3c55254  (pushed)
A RECONSTRUCTION+SELECTION COMMIT:      a216293  (pushed)
CURRENT CAMPAIGN HEAD (after Task A):   <A Task-A commit> (record SHA after commit)
MAIN DRIFT SINCE CAMPAIGN START:        none (re-checked 2026-09-02 v3: origin/main still 06a57d1)
CANDIDATE CHANGES NOT ON MAIN:
   PRODUCT SURFACE (Task A): STATUS.md (refreshed into a current-direction +
     reconstruction surface), roadmap.md + goal.md (historical/superseded
     headers), CONTEXT.md (+1 source-of-truth-map row -> STATUS.md).
   CAMPAIGN INSTRUMENTATION: docs/campaigns/durable-repo-self-development/
     {OWNER-INSTRUCTION,CHARTER,CAMPAIGN-STATE,STARTUP-PROVENANCE}.md +
     controllers/{README,A-reconstruction-and-selection,
     A-task-A1-reconstruction-probe}.md
RATIFICATION / MERGE STATUS:            nothing merged; no PR yet
CAPABILITY CLAIMS THAT APPLY ONLY TO THE CANDIDATE:
   "an independent controller can reconstruct current development direction from
   STATUS.md + named authoritative pointers, without anchoring on stale files" --
   TRUE on the campaign branch head, NOT on integrated main until merged.
CAPABILITY CLAIMS THAT APPLY TO INTEGRATED MAIN:     see section 5 (Campaign 1
   result, merged in #268). The Task A limitation A1 documented (STATUS.md stale
   as a reconstruction surface) still describes integrated main until merge.
```

PR #268 integration verified: its merge commit `06a57d1` **is** current
`origin/main` HEAD, and `git merge-base --is-ancestor 06a57d1 origin/main` holds.

## 4. CURRENT INTEGRATED PRODUCT ASSESSMENT (`origin/main` @ 06a57d1)

`REPOSITORY-VERIFIED` (durable docs read 2026-09-02; consequential claims to be
re-verified by each controller before acting).

- **Product definition** (`CONTEXT.md`): "agent-native engineering sensemaking and
  control layer for software-engineering agents." The active coding agent owns the
  recursive control loop (ADR 0013). Ratified external product scope = the
  validated, human-reviewed `repository_sensemaking_brief` (ADR 0014). Automatic
  fog-type→implementation routing is **not** ratified.
- **Control model** is explicit in docs: `docs/agent-native-operating-workflow.md`
  (operating map v0), `docs/decision-orchestration-boundary.md` (decision vs
  orchestration ownership), ADR 0013/0014/0026/0027. Warrant / recommendation /
  selection / execution authority are separated and consumers fail closed.
- **Campaign 1 result is merged (PR #268).** It added, on the product surface:
  a documented "responsibility-level continuation from a durable Markdown record"
  pattern (operating map section 2 subsection + Reality-map rows); a consolidated
  deterministic-machinery + hooks disposition (`decision-orchestration-boundary.md`);
  `docs/workflow-system-disposition.md` (all 23 registered workflows classified
  with pinned evidence); truthful hook description + `CLAUDE.md` SessionStart
  section; a lazy `workflow_liveness` resolver in `scripts/_validator_utils.py` +
  regression tests. No ADR / contract / registry / overlay / `src/` change.
  Campaign 1 disposition: `CAMPAIGN_COMPLETE`
  (`docs/campaigns/agent-native-self-development/FINAL-REPORT.md`).
- **CI on `main`**: "Validator Ecosystem" workflow (`.github/workflows/validation.yml`),
  ~19 jobs incl. Gate A security suites, phase2–6 campaign-validation/ledger/
  execution-boundary suites, `validate` (Level 1 `validate-repo.py`, Level 2/3
  `test-validators.py`, run-log + mode-coverage), `probe-gate`, `core-assertions`,
  `conditional-representation-exact-head`. Reported green at `06a57d1` lineage
  (to be reconfirmed per controller).
- **Open PRs**: only #194 (draft, `experiment/exp-0003-results`, explicitly
  "do not merge"). No other campaign/product PR open.
- **Research lanes (non-ratified)**: Goal A external validation ACTIVE but halted
  in this environment (Issue #255; `evidence/0023`); C6R (#226);
  `docs/semantic-control-map.md` trial OPEN (min close 2026-09-28).

## 5. DEMONSTRATED PRODUCT CAPABILITIES (integrated on `main`)

`GITHUB-VERIFIED` (PR #268 merged) + `REPOSITORY-VERIFIED` (docs), each to be
reverified before consequential use.

- Agent-native brief production + deterministic validation on ≥2 repositories;
  responsibility-before-Skill selection without routing; claim reconciliation;
  finding-specific repair verification; fail-closed authority on auto-invoke and
  liveness; probe-engine enforcement gate in CI.
- **Responsibility-level, artifact-mediated continuation into a fresh context**
  from a durable Markdown record: demonstrated across six responsibility classes
  (reconstruction; mechanical; judgment-docs; implementation-class code+tests;
  multi-file architecture reconciliation; evidence-gathering+classification;
  product-machinery change with regression tests). Verification-bearing: fresh
  contexts corrected ~22 wrong/overstated record facts, none causing a wrong
  action. **Limitation (Campaign 1's own statement):** one persistent dispatcher,
  one repository, one day; fresh contexts were *workers*, not *controllers*; the
  largest code change from durable state was one script + tests, no `src/` change.

## 6. DEMONSTRATED CAMPAIGN CAPABILITIES (Campaign 2)

- **CC-1 (Task A / A1):** a fresh general-purpose sub-agent context (no
  conversation history, no Campaign 2 semantic state, Campaign 2 dir excluded)
  reconstructed the product's strategic headline (Goal A / A1 highest-value,
  substrate-blocked) and a defensible decided/in-flight/deferred map from durable
  repository evidence + `gh` alone, in ~15 tool calls to a defensible answer, and
  independently identified the reconstruction-surface staleness. This is a
  **campaign capability** (the harness can run a credible fresh-context
  reconstruction probe); it is **not** yet the product capability of Task A's
  change, which is unmerged. Evidence:
  `controllers/A-task-A1-reconstruction-probe.md`.
- Not yet demonstrated: a fresh context owning **complete semantic
  campaign-controller** succession (that is the Controller B handoff, next).

## 7. EVIDENCE CEILINGS (carried in from the owner instruction + Campaign 1)

- **EC-1 Minimality.** A successful rich-state handoff shows SUFFICIENCY, not
  STRICT MINIMALITY. No comparative (smaller-state / staged-reveal / withheld-field)
  evidence exists yet.
- **EC-2 Succession isolation.** The strongest isolation the execution environment
  can establish is not yet determined (preflight item 12; see STARTUP-PROVENANCE).
  Until established, any succession claim is bounded and may carry
  `SUCCESSION_ISOLATION_UNVERIFIED` on dimensions the environment cannot enforce.
- **EC-3 Scale.** Campaign 1 evidence is single-dispatcher / single-repo /
  single-day. Campaign 2 does not automatically lift that.
- **EC-4 Product vs campaign state.** Whether durable *campaign* state maps to any
  needed durable *product* state is an open question Campaign 2 must answer from
  evidence, not assume.
- **EC-5 Implementation depth.** No broad `src/` implementation depth across
  product surfaces has been demonstrated from durable state.

## 8. COMPLETED STRATEGIC TASKS

**Task A — DONE** (executed to its legitimate boundary; product change committed +
qualified). Immutable checkpoint: `controllers/A-reconstruction-and-selection.md`
(selection) + `controllers/A-task-A1-reconstruction-probe.md` (A1 evidence).

| Task | Controller | Selected because | Alternatives considered | Capability advanced | Evidence | Ceiling remaining |
|---|---|---|---|---|---|---|
| **A** | A | Development-direction reconstruction surface: the only candidate boundary that sits directly on the campaign's central question, is bounded/reversible, does not predetermine the solution, has concrete evidence the limitation exists, and stays warranted even if succession were already solved. | (1) *selected*: development-direction reconstruction surface; (2) promote artifact-mediated continuation to a product-offered pattern — thin, largely done by C1; (3) verification-bearing handoff as an explicit capability — folded into (1); (4) `repo-sensemaker` brief vs direction state — out of ratified scope (ADR 0014); (5) premise check — resolved as (1)'s internal uncertainty, not a rival, and NOT invalidated. | **Repository-level development-direction reconstruction**: `STATUS.md` refreshed into a current (ratified/in-flight/deferred + highest-leverage next boundary) surface with an explicit "Reconstructing current development direction" reading path; the actively-misleading root files (`roadmap.md`, `goal.md`) carry historical/superseded headers; `CONTEXT.md` source-of-truth map now names `STATUS.md`. An independent controller can now reconstruct direction from one named surface + pointers without anchoring on stale claims. **Applies to the campaign candidate head only** until merge. | A1 fresh-context probe (`controllers/A-task-A1-reconstruction-probe.md`): reconstruction was possible but cost ~15 calls across 4 scattered docs + a wrong-anchor hazard on `roadmap.md`/`goal.md`/`00-user-intent.md`/`CHANGELOG.md`/auto-memory. Qualification: `validate-repo.py` exit 0; probe gate PASS (0 blocking); `test-validators.py` 78/78; core-assertions pytest 99 passed/1 skipped. | Change is unmerged (integrated main still carries the limitation). Not comparative-minimality tested (EC-1). `00-user-intent.md` + `CHANGELOG.md` flagged in STATUS.md, not edited (durable-artifact / changelog-convention caution). `docs/` historical sprawl documented, not archived (separate warrant). |

## 9. OPEN MATERIAL GAPS (relative to the campaign mission)

`CONTROLLER INFERENCE` from Campaign 1's stated limitations + the owner
instruction. Refined by Controller A's reconstruction
(`controllers/A-reconstruction-and-selection.md`). Not a task list.

- **MG-1** No fresh context has taken over the **complete semantic
  campaign-controller** role (next-task selection included).
- **MG-2** No **cross-controller** semantic continuation demonstrated.
- **MG-3** Only one dispatcher/controller has ever run a campaign here.
- **MG-4** No general autonomous repository self-development; no production-grade
  reliability claim.
- **MG-5** Strict minimality of durable continuation state untested (EC-1).
- **MG-6** Unclear which part of Campaign 1's continuation capability belongs in
  the *product* vs exists only for campaign experimental control.
- **MG-7** (Controller A) The repository's designated development-direction
  surfaces did not reflect integrated reality and were not a safe reconstruction
  basis. **ADDRESSED on the campaign candidate head by Task A** (STATUS.md
  refresh + reconstruction reading path; historical headers on
  `roadmap.md`/`goal.md`; CONTEXT.md source-of-truth-map row). **Still open on
  integrated main** until PR/merge (owner decision). Residual: `00-user-intent.md`
  / `CHANGELOG.md` flagged not edited; `docs/` historical sprawl documented not
  archived.

## 10. LAST ASSESSED CAPABILITY FRONTIER

**Controller A, 2026-09-02, post-Task-A (LAST ASSESSED CANDIDATE — not a command;
Controller B owns the next decision and may reject this):**

Task A addressed the *designated-surface* half of the development-direction
reconstruction gap (STATUS.md + reading path + historical headers), on the
campaign candidate head. Controller A's remaining assessment of the frontier for
"repository-level development direction surviving independent controller
replacement", offered as candidates for Controller B to evaluate independently:

- **F-a** The reconstruction surface is now a *convention*, not a *tested
  capability across an independent controller*. Task A's own A1 probe was run by
  Controller A as a tool; no independent controller has yet reconstructed
  direction *from the refreshed surface* and acted on it. (Controller B's own
  reconstruction will be the first real test of this.)
- **F-b** MG-6 is untouched: which parts of Campaign 1's continuation capability
  belong in the *product* vs exist only for campaign experimental control — still
  unclear, and central to the campaign's minimality question (EC-4).
- **F-c** A1 named the product's own top priority (Goal A / A1) as
  owner/environment-blocked (Issue #255) with no repo-code deliverable — so
  large product implementation there is `OWNER_DECISION_REQUIRED`, not campaign
  work.
- **F-d** Comparative minimality (EC-1) is entirely untested: no smaller-state or
  staged-reveal variant has been tried.

Full five-boundary comparison and the Task A selection rationale:
`controllers/A-reconstruction-and-selection.md` Part 2.

## 11. ACTIVE DECISION-CHANGING UNCERTAINTIES

- **U-1** What is the strongest defensible controller-isolation level achievable
  with the available fresh-context mechanism? (preflight item 12 / EC-2;
  STARTUP-PROVENANCE records the current assessment.)
- **U-2 — RESOLVED (Task A / A1).** Development direction *was* reconstructible
  by an independent context but at ~15 tool calls across 4 scattered documents
  with a real wrong-anchor hazard on the designated surfaces (`STATUS.md` stale,
  `roadmap.md`/`goal.md`/`00-user-intent.md`/`CHANGELOG.md`/auto-memory point at
  a superseded plan). **Not** `CAMPAIGN_PREMISE_INVALIDATED`; **not** primarily
  campaign instrumentation. Smallest sufficient change = refresh + reconstruction
  reading path on existing Markdown surfaces (done). Failure classes:
  `CONTEXT_RECONSTRUCTION_COST_EXCESSIVE` (primary), `HANDOFF_FACT_INCORRECT`
  (caught, not trusted).
- **U-3 (new)** Does the *refreshed* surface actually let an independent
  controller reconstruct direction and select a warranted task without anchoring
  wrong? First real test = Controller B's own reconstruction.
- Further uncertainties are added as Controller B proceeds.

## 12. OWNER / AUTHORITY BOUNDARIES

See `CHARTER.md` "AUTHORITY" and "OWNER-RESERVED DECISIONS". Summary of grants
with sources:

| Grant / boundary | Source |
|---|---|
| Own Campaign 2 end to end on the campaign branch | `OWNER-INSTRUCTION.md` "Campaign Mission" + "Campaign 2 Execution Authority" |
| Reads across source/tests/docs/ADRs/contracts/git/GitHub/CI | `OWNER-INSTRUCTION.md` "Authorized Repository Reads" |
| Local engineering on the campaign branch (code, tests, docs, commits, validators) | `OWNER-INSTRUCTION.md` "Authorized Local Engineering Actions" |
| Push the campaign branch; create/maintain a **draft** PR | `OWNER-INSTRUCTION.md` "Authorized Remote Campaign Actions" |
| Merge PR; ADR acceptance; external publication; issue lifecycle changes for bookkeeping; unrelated PR merges; protected-policy edits; inferring owner preference | **NOT authorized** — `OWNER-INSTRUCTION.md` "Not Authorized by Default" → `OWNER_DECISION_REQUIRED` |
| Repository policy (accepted ADRs, CONTEXT.md, AGENTS.md, contracts, schemas) still governs the product | `OWNER-INSTRUCTION.md` "Product Authority Remains External to the Campaign" |

**Owner-reserved decisions inherited as open** (from Campaign 1
`CAMPAIGN-STATE.md` section 11 / `FINAL-REPORT.md` section 9; `GITHUB-VERIFIED`
that #268 is merged):

1. Merge of PR #268 — **RESOLVED**: merged 2026-09-02T07:29:05Z (this is Campaign
   2's base). Campaign 1's terminal owner decision is closed.
2. Whether to record Campaign 1's substrate observation on Issue #255 — open,
   optional.
3. The nine registry/overlay/documentation items implied by
   `docs/workflow-system-disposition.md` section 6 — open.

## 13. REJECTED OR SUPERSEDED STRATEGIC OPTIONS

None yet.

## 14. DEFERRED LOCAL FINDINGS

None recorded by Campaign 2 yet. Campaign 1's deferred engineering debt
(`FINAL-REPORT.md` section 9: D2b, D8, D17, D18, D19, D14 platform reds, etc.)
is inherited context, not automatically Campaign 2 work — a local defect becomes
a Campaign 2 task only through the strategic selection gate.

## 15. RELEVANT OBSERVED INTEGRATION / CI STATE

```
pushed:        3c55254 (bootstrap), a216293 (A selection), <A Task-A commit>
               -> origin/campaign/durable-repo-self-development
PR:            none yet (Controller B decides whether a draft PR helps; Task A is
               reviewable but succession evidence stays on one branch lineage)
origin/main:   06a57d1  (== campaign base; no drift, re-checked 2026-09-02 v3)
campaign CI:   Task A commit is the first with a product-surface change
               (STATUS.md/roadmap.md/goal.md/CONTEXT.md); exact-head
               "Validator Ecosystem" result to be observed after push and
               recorded here
local qual:    validate-repo.py exit 0; probe gate PASS (0 blocking; +2
               non-blocking evidence findings in the A1 doc, documented);
               test-validators.py 78/78; core-assertions pytest 99 passed / 1
               skipped
merged:        nothing from Campaign 2
```

## 16. CONTROLLER-HANDOFF TRACE (append-only)

```
2026-09-02  Controller A  bootstrap: preflight complete; worktree + branch
                          campaign/durable-repo-self-development @ 06a57d1;
                          OWNER-INSTRUCTION/CHARTER/CAMPAIGN-STATE/
                          STARTUP-PROVENANCE + controllers/ committed (3c55254,
                          pushed).
2026-09-02  Controller A  reconstruction + Task A selection committed
                          (controllers/A-reconstruction-and-selection.md, a216293).
                          Selected boundary: development-direction reconstruction
                          surface.
2026-09-02  Controller A  Task A executed: A1 fresh-context reconstruction probe
                          (controllers/A-task-A1-reconstruction-probe.md);
                          U-2 RESOLVED (limitation confirmed, product-surface,
                          not premise-invalidation); A3 smallest warranted change
                          committed (STATUS.md refresh + reading path; historical
                          headers on roadmap.md/goal.md; CONTEXT.md +1 row);
                          A4 qualified (validate-repo 0, probe gate PASS,
                          test-validators 78/78, core-assertions 99p/1s).
                          -> next: mandatory handoff to a genuinely fresh
                          Controller B (controllers/A-handoff.md), then Controller
                          A relinquishes semantic control.
```

## 17. FAILURE OBSERVATIONS

- **FO-1 (Task A / A1) — `CONTEXT_RECONSTRUCTION_COST_EXCESSIVE` (product,
  mild).** What failed: an independent context reconstructing "current
  development direction + highest-leverage boundary" had to cross-read 4
  scattered documents (~15 tool calls) because the designated surface
  (`STATUS.md`) was stale/thin and the source-of-truth map did not name where the
  current state actually lived. Decision affected: none — the probe reached a
  defensible answer. Discovered by: the A1 fresh-context probe. Verification
  prevented wrong action: yes (the probe distrusted the stale surfaces).
  Smallest repair: STATUS.md refresh + a reconstruction reading path (done,
  candidate head). Recurrence: this is the first Campaign 2 measurement; Campaign
  1 R1 showed the analogous cost *with* a dedicated campaign record. Product or
  harness: **product**. Infrastructure warranted: no — Markdown on existing
  surfaces sufficed.
- **FO-2 (Task A / A1) — `HANDOFF_FACT_INCORRECT` (caught).** `roadmap.md`,
  `CHANGELOG.md`, `00-user-intent.md`, and the user auto-memory carry wrong
  consequential facts ("Phase 2.3 / v0.2.1 Beta / GA rollout" / "PRODUCTION
  READY"). The fresh context distrusted and cross-checked, so no wrong action
  followed; had it trusted them this would be `HANDOFF_FACT_TRUST_FAILURE`.
  Repair: historical headers on `roadmap.md`/`goal.md`; the rest flagged in
  STATUS.md's reconstruction note (auto-memory is not a repo file and cannot be
  fixed from the product).
- **FO-3 (harness, minor, disclosed) — `HANDOFF_STATE_CONTAMINATION`-adjacent.**
  The A1 sub-agent's own broad `Grep` surfaced ~30 lines of the excluded
  Campaign 2 directory in tool output. It disclosed this, did not open the files,
  and the visible lines agreed with conclusions it had already reached
  independently. Assessed immaterial to the probe's findings. Lesson: a future
  fresh-context probe prompt should tell the sub-agent to scope `Grep`/`Glob`
  away from the excluded path, not only "don't open" it.
- **FO-4 (probe false positive, non-blocking).** `A-task-A1-reconstruction-probe.md`
  adds 2 non-blocking `adr/status_claim_mismatch` evidence findings: the probe's
  heuristic reads the verbatim quote "ADR 0017 / 0021 ... never Accepted" as a
  claim of *accepted*. Gate PASSES (this finding type never blocks). Left as-is
  (verbatim evidence quote). No product or campaign consequence.

(Classes available: `CAMPAIGN_STATE_INSUFFICIENT`,
`STRATEGIC_SELECTION_UNSTABLE`, `HANDOFF_FACT_INCORRECT`,
`HANDOFF_FACT_TRUST_FAILURE`, `PRODUCT_DIRECTION_AMBIGUITY`,
`CAPABILITY_MODEL_MISSING`, `AUTHORITY_RECONSTRUCTION_FAILURE`,
`CONTEXT_RECONSTRUCTION_COST_EXCESSIVE`, `CAPABILITY_DISCOVERY_FAILURE`,
`MISSING_DURABLE_STATE`, `INCIDENTAL_CONTEXT_LOSS`, `HANDOFF_STATE_CONTAMINATION`,
`SUCCESSION_ISOLATION_UNVERIFIED`, `BASELINE_DRIFT_MATERIAL`,
`OTHER_DEMONSTRATED_FAILURE`.)

## 18. CONTEXT-COST OBSERVATIONS

**CCO-1 — Task A / A1 fresh-context reconstruction (product-development
direction, Campaign 2 dir excluded):**

- **Rediscovered from the repo:** the whole ratified-ADR set (0013/0014/0026/
  0027/0015-addendum/0023), the operating-map + decision-orchestration model,
  Campaign 1's result — all present but spread; the freshest strategic narrative
  was in `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` /
  `FINAL-REPORT.md`, not on any root surface.
- **Rediscovered from GitHub:** the three live workstreams and their exact
  boundaries (issues #218/#226/#255); recent merged PRs for "what changed last".
- **Durable state that saved material work:** Campaign 1's `CAMPAIGN-STATE.md`
  capability table with per-row evidence pointers — "the single most useful
  current-state surface" the probe found.
- **Redundant / noise:** ~45 loose historical `docs/*.md`; the stale root files.
- **Required reverification / dangerous to trust:** `roadmap.md`, `CHANGELOG.md`,
  `00-user-intent.md`, the user auto-memory — all point at a superseded PyPI/GA
  plan; ADRs 0017–0021 look decided by title.
- **Expensive to reconstruct:** *why* the repo is in a "harden only where
  pressured / do not build" posture (research-agenda meta-finding + Campaign 1
  closure + Goal A substrate halt must all be read together).
- **Cheaper to reconstruct than maintain:** the exact list of merged PRs; the
  ADR status of each ADR (read the Status line at point of use).
- **Looks product-worthy to preserve:** a current ratified/in-flight/deferred
  summary + a named reconstruction reading path (Task A adds this to STATUS.md).
- **Looks campaign-specific:** the controller-succession provenance, the
  isolation-limit accounting, the five-boundary comparison — belong in
  `docs/campaigns/`, not the product surface.

## 19. MINIMALITY EVIDENCE / CLAIM CEILING

No comparative minimality evidence. Current supported claim ceiling: nothing —
no handoff has occurred. See EC-1. Any eventual sufficiency result stays
"smallest currently supported candidate" unless comparative evidence is produced.

## 20. CAMPAIGN ACCEPTANCE STATUS

Toward the 19 conditions after Task A:

- **10 (Real Product Advancement):** partially — Task A produced an
  implementation-light but consequential product change (the development-direction
  reconstruction surface + reading path) plus verified evidence (A1) that
  redirected nothing but *confirmed* the boundary; not premise-invalidation.
  Whether this alone satisfies "substantive" is for the final assessment; Task B
  (Controller B) may add substantive implementation.
- **12 (Strategic/Local Distinction):** Task A explicitly distinguished the
  strategic boundary (development-direction reconstruction capability) from the
  nearby-defect framing ("fix stale docs") — see
  `controllers/A-reconstruction-and-selection.md` Part 3.
- **13 (No Premature Infrastructure):** met so far — Markdown on existing
  surfaces; no artifact type / schema / Skill / workflow / hook / registry field.
- **16 (Qualification):** Task A candidate head qualified locally (see §15);
  exact-head CI pending.
- **1–9, 11, 19 (succession):** not yet — Controller B handoff is next.
- **14, 15, 17, 18:** on track; recorded honestly in §17–19 and the ceilings.

---

### Version log

- **v1 (2026-09-02, Controller A, bootstrap):** campaign scaffolding created;
  preflight recorded; integrated product state + Campaign 1 result reconstructed
  from durable docs; no strategic task selected.
- **v2 (2026-09-02, Controller A, reconstruction + selection):** full
  reconstruction + five-candidate strategic-boundary comparison committed to
  `controllers/A-reconstruction-and-selection.md`; **Task A selected** —
  investigate development-direction reconstructibility, classify any failure,
  deliver the smallest warranted product change (or a verified "no new mechanism
  warranted"). MG-7 added. Task A implementation not started.
- **v3 (2026-09-02, Controller A, Task A executed):** A1 fresh-context
  reconstruction probe run (`controllers/A-task-A1-reconstruction-probe.md`);
  **U-2 RESOLVED** — limitation confirmed, product-surface, not
  premise-invalidation, failure classes `CONTEXT_RECONSTRUCTION_COST_EXCESSIVE` +
  `HANDOFF_FACT_INCORRECT`. Smallest warranted change committed: `STATUS.md`
  refreshed into a current-direction + reconstruction-reading-path surface;
  historical/superseded headers on `roadmap.md` + `goal.md`; `CONTEXT.md`
  source-of-truth-map row → `STATUS.md`. Qualified locally (validate-repo 0,
  probe gate PASS, test-validators 78/78, core-assertions 99p/1s). Failure
  observations FO-1..FO-4 and context-cost CCO-1 recorded. Task A at its
  legitimate boundary. **Next: mandatory handoff to a genuinely fresh Controller
  B; Controller A then relinquishes semantic control.**
