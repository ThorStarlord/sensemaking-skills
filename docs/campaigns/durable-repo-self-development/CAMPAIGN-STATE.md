# Campaign 2 durable semantic state — Durable Repository-Level Self-Development

```
STATUS:     ACTIVE (v5). Task A done + qualified. **Fresh Controller B has
            taken over semantic control** at controllers/A-handoff.md
            (handoff head 358b5a2), reconstructed + reverified the durable
            state, committed its own checkpoint
            (controllers/B-reconstruction-and-selection.md @ 4ccbc70, pushed)
            BEFORE any Task B implementation, and executed **Task B**
            (b77ad04): the probe engine's live-document classifier now honors
            an explicit `<!-- doc-status: historical -->` marker, applied to
            roadmap.md + goal.md, so Task A's human historical markings and the
            deterministic drift machinery agree. Qualified (validate-repo 0;
            probe gate PASS; test-validators 78/78; core-assertions 103p/1s).
            Campaign closure assessed in controllers/B-cycle-result.md. A
            predecessor "frontier" or "next task" in this file is LAST ASSESSED
            CANDIDATE, not a command.
AUTHORITY:  non-authoritative. Not an ADR, contract, schema, registry, validator
            input, or registered workflow. Nothing in scripts/, src/, tests/,
            or .github/ reads this file.
CHARTER:    docs/campaigns/durable-repo-self-development/CHARTER.md
OWNER INSTR: docs/campaigns/durable-repo-self-development/OWNER-INSTRUCTION.md
            (verbatim; the campaign's authority source)
BRANCH:     campaign/durable-repo-self-development
WORKTREE:   H:/GithubRepositories/smk-campaign-2  (Controllers A then B, same
            committed worktree/branch; predecessor relinquished at handoff)
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
CURRENT ORIGIN/MAIN OBSERVATION:        06a57d1  (== base; no drift — re-fetched by
   Controller B 2026-09-02: `git log 06a57d1..origin/main` empty. Drift policy
   disposition: CONTINUE AGAINST RECORDED BASE.)
BOOTSTRAP COMMIT:                       3c55254  (pushed)
A RECONSTRUCTION+SELECTION COMMIT:      a216293  (pushed)
A TASK-A COMMIT:                        431ec43  (pushed)  [placeholder <A Task-A commit> resolved by Controller B]
A -> B HANDOFF COMMIT:                  358b5a2  (pushed)  = handoff head
B RECONSTRUCTION+SELECTION CHECKPOINT:  4ccbc70  (pushed)  committed BEFORE Task B impl / any predecessor feedback
B TASK-B COMMIT:                        b77ad04  (pushed)
CURRENT CAMPAIGN HEAD:                  <this CAMPAIGN-STATE v5 + B-cycle-result commit — record SHA after commit>
MAIN DRIFT SINCE CAMPAIGN START:        none (re-checked by Controller B 2026-09-02: origin/main still 06a57d1)
CANDIDATE CHANGES NOT ON MAIN:
   PRODUCT SURFACE (Task A): STATUS.md (refreshed into a current-direction +
     reconstruction surface), roadmap.md + goal.md (historical/superseded
     headers), CONTEXT.md (+1 source-of-truth-map row -> STATUS.md).
   PRODUCT SURFACE (Task B): scripts/probe_relationships.py (live-document
     classifier honors an explicit `<!-- doc-status: historical -->` marker —
     `_declared_doc_status` helper + `_classify_doc_file(rel, declared_status)`
     + `_discover_docs` wiring; deterministic machinery, no new gate/schema/
     blocking type); roadmap.md + goal.md (the one-line marker added under the
     H1); tests/test_probe_relationships.py (+4 regression tests).
   CAMPAIGN INSTRUMENTATION: docs/campaigns/durable-repo-self-development/
     {OWNER-INSTRUCTION,CHARTER,CAMPAIGN-STATE,STARTUP-PROVENANCE}.md +
     controllers/{README,A-reconstruction-and-selection,
     A-task-A1-reconstruction-probe,A-handoff,
     B-reconstruction-and-selection,B-cycle-result}.md
RATIFICATION / MERGE STATUS:            nothing merged; draft PR #269 only
CAPABILITY CLAIMS THAT APPLY ONLY TO THE CANDIDATE:
   (Task A) "an independent controller can reconstruct current development
   direction from STATUS.md + named authoritative pointers, without anchoring on
   stale files"; (Task B) "the deterministic drift machinery and the human
   historical markings on roadmap.md/goal.md agree — the probe no longer emits
   those files' superseded version claims as live conflicting evidence." Both
   TRUE on the campaign branch head, NOT on integrated main until merged.
CAPABILITY CLAIMS THAT APPLY TO INTEGRATED MAIN:     see section 5 (Campaign 1
   result, merged in #268). The Task A + Task B limitations still describe
   integrated main until merge (the probe on `main` still classifies
   roadmap.md/goal.md as live).
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
  reconstruction probe); it is **not** the product capability of Task A's
  change. Evidence: `controllers/A-task-A1-reconstruction-probe.md`.
- **CC-2 (A -> B succession):** a genuinely fresh *controller* context
  (Controller B; new context, only the allowed bootstrap, no predecessor
  transcript or private reasoning) reconstructed the mission, the available and
  reserved authority, the three state planes, demonstrated product + campaign
  capabilities, evidence ceilings, the previous task's rationale, and the
  predecessor's F-a..F-d frontier from the durable sources + repo/GitHub
  evidence; **reverified 12 consequential claims** (all correct at the decision
  level; found only cosmetic staleness — CI recorded for `431ec43` only though
  `358b5a2` is also green; three unfilled `<...>` SHA placeholders);
  **independently selected Task B**, partially rejecting/extending the
  predecessor frontier (rejected the staged-reveal minimality probe as
  measurement-only; confirmed Goal A as `OWNER_DECISION_REQUIRED`; selected the
  *machinery half* of MG-7); committed its checkpoint at `4ccbc70` **before**
  implementation and **before** any predecessor semantic feedback; executed
  Task B; validated; updated this file. Evidence:
  `controllers/B-reconstruction-and-selection.md`,
  `controllers/B-cycle-result.md`. **Isolation level (honest):** context
  isolation HARNESS-REPORTED; bootstrap-minimality / checkpoint-immutability /
  non-resumption CONTROLLER-ASSERTED; predecessor **process** non-persistence
  `SUCCESSION_ISOLATION_UNVERIFIED` (EC-2); same model family (disclosed). This
  is **complete semantic controller succession** at the honest evidence level
  the environment supports (MG-1 addressed; MG-3 — a second controller — met).
- **CC-3 (Task B / capability advanced):** the reconstruction surface Task A
  built now has a **mechanically enforced** half — `repo-sensemaker` / CI /
  a fresh controller running the probe engine see roadmap.md and goal.md as
  historical, matching Task A's prose. A real deterministic-machinery change
  (`scripts/probe_relationships.py` + regression tests) selected and executed by
  a fresh controller from durable-state reconstruction (a modest lift of EC-5).

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
  evidence, not assume. **Partial evidence (Controller B):** the
  *machinery-consistency of the reconstruction surface* (Task B) is a **product**
  concern — a probe classifier + an in-file marker any repo/operator/CI uses.
  The *succession provenance, isolation accounting, five-boundary comparison,
  controller checkpoints* are **campaign-only** — they belong in `docs/campaigns/`
  and no product surface needs an equivalent. The durable *rationale* format
  (why one boundary dominated, rejected alternatives, ceilings) was expensive to
  reconstruct and reused by B; the *facts* (SHAs, PR/CI state, ADR statuses)
  were cheap and were reverified, not trusted. This matches Campaign 1's lesson;
  it does **not** establish that the product needs a `CAMPAIGN-STATE`-shaped
  artifact (charter constraint 8 / formalization rule — no such need demonstrated).
- **EC-5 Implementation depth.** No broad `src/` implementation depth across
  product surfaces has been demonstrated from durable state. **Modestly lifted
  (Task B):** a real `scripts/` deterministic-machinery change (new helper,
  signature extension, caller wiring, 4 regression tests) was selected and
  executed by a fresh controller from durable-state reconstruction — still
  `scripts/`, not `src/`, and single-file; the ceiling stands for `src/` and
  multi-surface depth.

## 8. COMPLETED STRATEGIC TASKS

**Task A — DONE** (Controller A; product change committed + qualified). Immutable
checkpoint: `controllers/A-reconstruction-and-selection.md` +
`controllers/A-task-A1-reconstruction-probe.md`.

**Task B — DONE** (Controller B; executed to its legitimate boundary; product
change committed + qualified). Immutable checkpoint:
`controllers/B-reconstruction-and-selection.md`; result:
`controllers/B-cycle-result.md`.

| Task | Controller | Selected because | Alternatives considered | Capability advanced | Evidence | Ceiling remaining |
|---|---|---|---|---|---|---|
| **A** | A | Development-direction reconstruction surface: the only candidate boundary that sits directly on the campaign's central question, is bounded/reversible, does not predetermine the solution, has concrete evidence the limitation exists, and stays warranted even if succession were already solved. | (1) *selected*: development-direction reconstruction surface; (2) promote artifact-mediated continuation to a product-offered pattern — thin, largely done by C1; (3) verification-bearing handoff as an explicit capability — folded into (1); (4) `repo-sensemaker` brief vs direction state — out of ratified scope (ADR 0014); (5) premise check — resolved as (1)'s internal uncertainty, not a rival, and NOT invalidated. | **Repository-level development-direction reconstruction**: `STATUS.md` refreshed into a current (ratified/in-flight/deferred + highest-leverage next boundary) surface with an explicit "Reconstructing current development direction" reading path; the actively-misleading root files (`roadmap.md`, `goal.md`) carry historical/superseded headers; `CONTEXT.md` source-of-truth map now names `STATUS.md`. An independent controller can now reconstruct direction from one named surface + pointers without anchoring on stale claims. **Applies to the campaign candidate head only** until merge. | A1 fresh-context probe (`controllers/A-task-A1-reconstruction-probe.md`): reconstruction was possible but cost ~15 calls across 4 scattered docs + a wrong-anchor hazard on `roadmap.md`/`goal.md`/`00-user-intent.md`/`CHANGELOG.md`/auto-memory. Qualification: `validate-repo.py` exit 0; probe gate PASS (0 blocking); `test-validators.py` 78/78; core-assertions pytest 99 passed/1 skipped. | Change is unmerged (integrated main still carries the limitation). Not comparative-minimality tested (EC-1). `00-user-intent.md` + `CHANGELOG.md` flagged in STATUS.md, not edited. `docs/` historical sprawl documented, not archived (separate warrant). |
| **B** | B | **Machinery half of the development-direction reconstruction surface (MG-7m).** Task A's prose "HISTORICAL / SUPERSEDED" headers on `roadmap.md`/`goal.md` are invisible to `probe_relationships._classify_doc_file` (path signals only), so the version-drift probe still emits those files' superseded `0.2.1` / "Phase 2.3" claims as `conflicting_values` evidence against the declared `0.2.2` — the human reconstruction surface and the deterministic drift machinery a fresh controller / CI / `repo-sensemaker` rely on **disagree about which documents are current**. Only candidate that is at once on the central question, substantive product implementation, naturally bounded, warranted independent of the succession experiment, and a resolution of a contradiction Campaign 2 itself introduced (acceptance condition 15). | **B-ALT-1** staged-reveal comparative-minimality probe (EC-1) — rejected: measurement, not product advancement; would leave the campaign with zero substantive implementation; "elaborate framework to prove theoretical minimality" the owner instruction warns against; partial findings taken free from B's own reconstruction. **B-ALT-2** write the MG-6 product/campaign boundary — folded into §EC-4 as a note (largely already documented; standalone it risks "restates known facts"). **B-ALT-3** finish the human surface (CHANGELOG footer, `docs/` sprawl, `00-user-intent.md`) — rejected: instance cleanup, not a capability; `00-user-intent.md` is an immutable validated artifact. **B-ALT-4** *selected*. **F-c** Goal A substrate — confirmed `OWNER_DECISION_REQUIRED`, not campaign work. | **Mechanically-enforced consistency of the reconstruction surface.** `scripts/probe_relationships.py`: an opt-in `<!-- doc-status: historical -->` marker (synonyms `superseded`/`archived`; case-insensitive; head-window bound) via `_declared_doc_status()` + `_classify_doc_file(rel, declared_status=None)` (explicit marker wins over path heuristics) + `_discover_docs` wiring. Marker applied to `roadmap.md` + `goal.md`. Deterministic machinery (H6) — no new schema / gate / blocking finding type / artifact / workflow / hook; pure-path callers unchanged. Result: both files leave the `live` set (`by_class.historical` +2), their 5 stale version observations drop from the finding, probe gate still PASS. **Candidate head only** until merge. | Direct verification at `358b5a2`: `_classify_doc_file("roadmap.md")` -> `live`; probe run: `version` finding contained `roadmap.md:23/85/89/115/134` (`source_class: live`) despite Task A's header. After Task B: `roadmap.md`/`goal.md` classify `historical`, absent from the finding. Qualification (`b77ad04` worktree): `validate-repo.py` 0; probe gate PASS; `test-validators.py` 78/78; core-assertions pytest **103 passed / 1 skipped**; 70/70 across every `probe_relationships`-dependent module; +4 new regression tests. Three pre-existing local failures (D2b `test_validate_brief_json`; a wheel/`setup_skills` platform red; a `NoPresentTenseEnforcementClaims` platform red) reproduce identically on baseline `4ccbc70`. | Unmerged (integrated `main`'s probe still classifies `roadmap.md`/`goal.md` as live). EC-1 minimality untested — the marker-honoring classifier is argued smallest from evidence, not comparatively tested. Marker **not** applied to other historical-in-place root docs (`integration-report.md`, `integration-design.md`, `adoption-finalization.md`) or to the `docs/campaigns/**` records — deferred (§14). `STATUS.md` itself has no mechanical staleness signal (MG-8). Still `scripts/`, not `src/` (EC-5). |

## 9. OPEN MATERIAL GAPS (relative to the campaign mission)

`CONTROLLER INFERENCE` from Campaign 1's stated limitations + the owner
instruction. Refined by Controller A's reconstruction, then Controller B's.
Not a task list.

- **MG-1** No fresh context has taken over the **complete semantic
  campaign-controller** role (next-task selection included).
  **ADDRESSED (CC-2):** Controller B did exactly this — reconstructed,
  reverified, independently selected Task B (rejecting parts of A's frontier),
  committed the checkpoint before implementation, executed, validated. Bounded
  by EC-2 (isolation) and EC-3 (n=1 succession).
- **MG-2** No **cross-controller** semantic continuation demonstrated.
  **ADDRESSED (CC-2):** A → B continuation carried the mission, authority,
  state planes, ceilings, and rationale across a fresh-controller boundary via
  the durable sources alone; B's checkpoint continues the append-only record.
- **MG-3** Only one dispatcher/controller has ever run a campaign here.
  **ADDRESSED:** two controllers (A, then B) have now run this campaign.
- **MG-4** No general autonomous repository self-development; no production-grade
  reliability claim. **Still open** (out of Campaign 2 scope — closure rule).
- **MG-5** Strict minimality of durable continuation state untested (EC-1).
  **Still open** — Controller B deliberately did not run a staged-reveal probe
  (B-ALT-1 rejected); EC-1 preserved.
- **MG-6** Which part of Campaign 1's continuation capability belongs in the
  *product* vs exists only for campaign experimental control.
  **PARTIALLY RESOLVED (Controller B, §EC-4):** machinery-consistency of the
  reconstruction surface = product; succession provenance / isolation
  accounting / boundary comparison / checkpoints = campaign-only; the durable
  *rationale* format is reused, the *facts* are reverified not trusted. No
  product need for a `CAMPAIGN-STATE`-shaped artifact demonstrated.
- **MG-7** (Controller A) The designated development-direction surfaces did not
  reflect integrated reality. **Human half ADDRESSED by Task A** (candidate
  head). **Machinery half — MG-7m — ADDRESSED by Task B** (candidate head): the
  probe engine's live-document classifier honors the historical marking, so the
  drift machinery and the human surface agree. **Both still open on integrated
  `main`** until PR/merge (owner decision). Residual: `00-user-intent.md`
  (immutable artifact) / `CHANGELOG.md` footer flagged not edited; `docs/`
  historical sprawl + other historical-in-place root docs
  (`integration-report.md` etc.) not marked — deferred (§14).
- **MG-8** (Controller B) `STATUS.md` is now a hand-maintained current-direction
  surface with **no mechanical staleness signal of its own** — the original
  failure mode (a designated surface silently goes stale) can recur. A
  staleness validator/probe would need a demonstrated *recurrence* and is
  premature (formalization rule). Noted, not targeted.

## 10. LAST ASSESSED CAPABILITY FRONTIER

### 10.1 Controller A, post-Task-A (SUPERSEDED as the active frontier by 10.2; preserved)

Task A addressed the *designated-surface* half of the development-direction
reconstruction gap. Controller A's four frontier candidates:

- **F-a** The reconstruction surface is a *convention*, not a *tested capability
  across an independent controller*. — **Disposition (B):** partially exercised
  by Controller B's own reconstruction (contaminated — B had the campaign tree
  the bootstrap points at). Not selected as a standalone task.
- **F-b** MG-6 untouched (product vs campaign-only). — **Disposition (B):**
  partially resolved as a by-product (§EC-4 / MG-6), not a standalone task.
- **F-c** Goal A / A1 owner/environment-blocked, no repo-code deliverable. —
  **Disposition (B):** confirmed `OWNER_DECISION_REQUIRED`; not campaign work.
- **F-d** Comparative minimality (EC-1) entirely untested. — **Disposition (B):**
  not selected (B-ALT-1); measurement-only, would leave the campaign with no
  substantive implementation; EC-1 preserved.

Full five-boundary comparison: `controllers/A-reconstruction-and-selection.md`
Part 2.

### 10.2 Controller B, 2026-09-02, post-Task-B (LAST ASSESSED CANDIDATE — not a command)

After Task A (human surface) and Task B (machinery half), the
development-direction reconstruction surface is **sufficient at the honest
evidence level Campaign 2 can produce** and its two halves agree. Controller B's
assessment of what remains, for a possible Controller C or the final report:

- **BF-1 — The central question is answerable now; no further product capability
  is warranted.** Post Task A+B, an independent controller reconstructs direction
  from `STATUS.md` + `CONTEXT.md` source-of-truth map + the ordered reading path,
  and the deterministic drift machinery agrees on what is historical. "Harden
  only where pressured" + Campaign 1's "no further product change warranted" +
  the research-agenda "loops saturated" meta-finding all corroborate that there
  is no large warranted implementation. The smallest *currently evidenced*
  sufficient capability = the Task A + Task B change set (a current-direction
  Markdown surface + a reconstruction reading path + historical markings honored
  by the drift machinery). **Not** strict minimality (EC-1).
- **BF-2 — EC-1 comparative minimality** stays untested. A staged-reveal probe
  could still be run (by a Controller C or as a bounded appendix), but it is
  measurement, not product advancement, and the campaign's closure rule does not
  require it.
- **BF-3 — Residual instances**, all deferred (§14), none capability-level:
  `CHANGELOG.md` footer; `00-user-intent.md` staleness (immutable artifact);
  other historical-in-place root docs and `docs/campaigns/**` not marked; the
  FO-4 probe false-positives.
- **BF-4 — Everything else on `main`** (merge of PR #269; the nine
  workflow-system-disposition decisions; Goal A substrate) is
  `OWNER_DECISION_REQUIRED`, outside campaign authority.

Controller B's closure read is in `controllers/B-cycle-result.md`: after A → B
succession + two strategic cycles, Campaign 2's acceptance conditions are
materially satisfied at an honest evidence level; a Controller C handoff is
**optional** and would not change the central answer.

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
- **U-3 — PARTIALLY RESOLVED (Controller B).** Controller B reconstructed
  direction and independently selected a warranted task without anchoring wrong
  (it flagged and discarded the stale PyPI/GA framing; it did not adopt A's
  frontier as a command). Caveat: B's reconstruction leaned on the campaign
  durable tree (charter, state, checkpoints) the bootstrap points at, so it is
  a *contaminated* test of the Task A *product* surface specifically — a clean
  repo-only test would need a fresh sub-context (not run; B-ALT-1 rejected).
- **U-4 — RESOLVED (Task B).** The deterministic drift machinery did **not**
  honor Task A's prose historical headers (`_classify_doc_file` is path-signal
  only); verified live at `358b5a2`. Smallest sufficient fix = an opt-in in-file
  `<!-- doc-status: historical -->` marker the classifier honors (not a
  front-matter schema, not a path move, not a filename rule). Implemented +
  qualified.
- **U-5 (open, low urgency)** Does the campaign warrant a Controller C? Controller
  B's read: no — the central question is answerable after A → B + two cycles
  (§10.2 BF-1); a C handoff would add succession-count evidence (n=2 → n=3) but
  not change the central answer. Deferred to the final report / owner.

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

- **Controller B, Task B selection:** the following were considered as Task B
  and **not** selected (full rationale: `controllers/B-reconstruction-and-selection.md`
  Part 2):
  - **B-ALT-1 — staged-reveal comparative-minimality probe (EC-1 / F-d).**
    Rejected: measurement, not product advancement; both Campaign 2 cycles would
    then be probes, straining acceptance condition 10; "elaborate experimental
    framework merely to prove theoretical minimality" the owner instruction
    warns against. EC-1 preserved instead.
  - **B-ALT-2 — write the MG-6 / EC-4 product-vs-campaign boundary (F-b).**
    Not selected as a standalone task (risks "documentation that merely restates
    known facts"); folded into §EC-4 / MG-6 as a by-product note.
  - **B-ALT-3 — finish the human reconstruction surface** (`CHANGELOG.md`
    footer, `docs/` sprawl, `00-user-intent.md`). Rejected: instance cleanup,
    not a capability; `00-user-intent.md` is a validated immutable artifact.
  - **F-c — Goal A execution substrate.** Confirmed `OWNER_DECISION_REQUIRED`
    (Issue #255; no repo-code deliverable) — not campaign work.

## 14. DEFERRED LOCAL FINDINGS

Recorded by Controller B (Task B), all **local**, none capability-level, none
selected — each would need its own strategic warrant:

- **DB-1** `CHANGELOG.md` "Deployment Timeline" footer still lists Phase
  2.2/2.3/3/4 (a superseded plan). `CHANGELOG.md` is already `historical`-class
  to the probe, so this is human-readability only; Task A's `STATUS.md`
  reconstruction note already tells readers not to anchor on it. One-line fix if
  ever warranted.
- **DB-2** Other historical-in-place root docs still classified `live` by the
  probe: `integration-report.md` (contains a stale `distinct=[0.2.0,0.2.1,0.2.2]`
  probe-output snippet), `integration-design.md`, `adoption-finalization.md`.
  The Task B `doc-status` marker mechanism now supports fixing these cleanly;
  not applied (Task B scoped to the roadmap.md/goal.md contradiction Task A
  created).
- **DB-3** `docs/campaigns/**` records (both campaigns' `CAMPAIGN-STATE.md`,
  controller checkpoints, R1/R2, this file's own quoted strings) are classified
  `live` and contribute quoted-evidence noise to the `version` /
  `adr/status_claim_mismatch` findings (the FO-4 false-positives + B's own
  checkpoint's `0.2.1` quotes). The `doc-status` marker could suppress this, but
  classifying *evolving* campaign state as "historical" is a judgment call
  deserving its own consideration; deferred.
- Campaign 1's inherited debt (D2b, D8, D17, D18, D19, D14 platform reds) is
  unchanged context, not Campaign 2 work.

## 15. RELEVANT OBSERVED INTEGRATION / CI STATE

```
pushed:        3c55254 (bootstrap), a216293 (A selection), 431ec43 (Task A),
               358b5a2 (A->B handoff), 4ccbc70 (B reconstruction+selection
               checkpoint), b77ad04 (Task B), + this v5 commit
               -> origin/campaign/durable-repo-self-development
PR:            #269 (DRAFT, not for merge) campaign/durable-repo-self-development
               -> main. Opened by Controller A for exact-head CI qualification +
               as a durable campaign-evidence surface. Merge = owner decision.
origin/main:   06a57d1  (== campaign base; no drift — Controller B re-fetched
               2026-09-02: `git log 06a57d1..origin/main` empty)
campaign CI:   "Validator Ecosystem" (pull_request event, PR #269):
                 - 431ec43 (Task A head): completed/success (GREEN)
                 - 358b5a2 (A->B handoff head): completed/success (GREEN) --
                   [Controller B correction: CAMPAIGN-STATE v4 recorded CI for
                   431ec43 only; the handoff commit is also green]
                 - b77ad04 (Task B head): pushed; exact-head CI result to be
                   observed by Controller B after push (record here)
local qual (b77ad04 worktree, Controller B, RUN):
               validate-repo.py exit 0; probe gate PASS (0 blocking; non-blocking
               evidence findings only); test-validators.py 78/78; core-assertions
               pytest 103 passed / 1 skipped (+4 new Task B regression tests);
               70/70 across every probe_relationships-dependent module.
               Pre-existing local reds (identical on baseline 4ccbc70):
               test_validate_brief_json (D2b), test_setup_skills_reports_drift
               (wheel platform red), NoPresentTenseEnforcementClaims (platform
               red) -- all green in Linux CI.
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
                          committed 431ec43 (STATUS.md refresh + reading path;
                          historical headers on roadmap.md/goal.md; CONTEXT.md +1
                          row); A4 qualified (validate-repo 0, probe gate PASS,
                          test-validators 78/78, core-assertions 99p/1s);
                          draft PR #269 opened; exact-head CI GREEN on 431ec43.
2026-09-02  A -> B        HANDOFF. controllers/A-handoff.md committed
                          (pre-handoff invariant 11/11; full provenance; verbatim
                          bootstrap). Handoff head = 358b5a2 [placeholder
                          <record after commit> resolved by Controller B].
                          Isolation: context HARNESS-REPORTED;
                          minimality/immutability/non-resumption
                          CONTROLLER-ASSERTED; predecessor-process non-persistence
                          SUCCESSION_ISOLATION_UNVERIFIED (EC-2). Controller A
                          relinquished semantic control.
2026-09-02  Controller B  reconstruction + reverification (12 consequential
                          claims, all correct at decision level; N-1 CI also
                          green on 358b5a2; N-2 three SHA placeholders filled) +
                          independent Task B selection committed BEFORE any Task
                          B implementation and BEFORE any predecessor semantic
                          feedback: controllers/B-reconstruction-and-selection.md
                          @ 4ccbc70 (pushed). Selected boundary: machinery half
                          of the development-direction reconstruction surface
                          (MG-7m) -- partially rejecting/extending A's F-list.
2026-09-02  Controller B  Task B executed: U-4 RESOLVED (probe classifier did
                          not honor Task A's historical headers -- verified live);
                          smallest fix = an opt-in `<!-- doc-status: historical -->`
                          marker honored by _classify_doc_file; committed b77ad04
                          (scripts/probe_relationships.py + 4 regression tests;
                          marker on roadmap.md/goal.md); qualified (validate-repo
                          0, probe gate PASS, test-validators 78/78,
                          core-assertions 103p/1s); pushed. CAMPAIGN-STATE -> v5;
                          controllers/B-cycle-result.md written. Closure read:
                          acceptance conditions materially satisfied at an honest
                          evidence level; Controller C optional, would not change
                          the central answer.
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
  **Controller B note:** `B-reconstruction-and-selection.md` adds analogous
  non-blocking `version` observations (`:517`, `:581` — verbatim "0.2.1 (Beta)"
  quotes from Task B's evidence). Same disposition (verbatim evidence; gate
  PASSES). The Task B `doc-status` marker *could* suppress the whole
  `docs/campaigns/**` quoted-evidence noise class — recorded as DB-3, not done
  (classifying evolving campaign state "historical" is its own judgment call).
- **FO-5 (Controller B, harness, minor, disclosed) — worktree side-effect
  hygiene.** A broad local `pytest` run triggered `pip install -e .` as a side
  effect, which regenerated a stale committed `src/sensemaking_skills.egg-info/`
  copy (committed at 0.2.1; pyproject is 0.2.2) and dirtied the tree; a
  `git stash` then could not `pop` cleanly until the egg-info files were
  `git checkout`-restored. No campaign artifact affected; the Task B commit
  contains only the 4 intended files. Lesson (already in STARTUP-PROVENANCE
  preflight #11): restore `egg-info` before any dirty-tree check; prefer the
  narrow core-assertions set over a broad sweep for routine qualification.
- **No `STRATEGIC_SELECTION_UNSTABLE` and no `HANDOFF_FACT_TRUST_FAILURE`
  observed at the A → B succession.** Controller B's reconstruction found the
  durable state correct on every consequential fact; the only corrections were
  cosmetic (N-1 CI, N-2 placeholders). Verification-bearing continuation held.

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

**CCO-2 — A → B fresh-*controller* reconstruction (Controller B; full campaign
durable tree available per the bootstrap):**

- **Rediscovered from the repo/GitHub:** the SHAs of every campaign commit; the
  exact PR #269 / #268 state; the open-issue set (#218/#226/#255); ADR statuses;
  the Task A product diff; the campaign-branch CI conclusions. All cheap
  (`git`, `gh`) and all reverified rather than trusted.
- **Durable state that saved material work:** the *rationale* layers —
  `A-reconstruction-and-selection.md` Part 2 (five-boundary comparison + why the
  boundary dominated), the owner instruction's constraints/acceptance/stopping
  rules, `A-task-A1-reconstruction-probe.md` (why the limitation is
  product-not-instrumentation, the failure classes). Reconstructing *why* from
  source alone would have been expensive and lossy.
- **Redundant / cheap-to-re-derive:** `CAMPAIGN-STATE.md`'s factual lines (SHAs,
  CI status, ADR statuses) — all reverified in minutes; the version-log prose.
- **Required reverification / would have been dangerous to trust blindly:** the
  `<A Task-A commit>` / `<record after commit>` placeholders (never filled — a
  controller that quoted them as SHAs would be wrong); CAMPAIGN-STATE §15's
  "CI green on 431ec43" (true but incomplete — 358b5a2 also green).
- **What the campaign state got right and saved:** the three-state-plane
  discipline, the "predecessor frontier = last assessed candidate" framing, and
  the explicit ceilings — these made independent selection fast and safe.
- **Cost:** roughly 25–30 tool calls to a committed checkpoint (≈8 durable
  campaign docs read in full, ≈10 `git`/`gh` verifications, ≈6 product-surface
  reads incl. the probe engine + a live probe run to verify the Task B gap).
- **Product vs campaign:** confirmed — the machinery-consistency finding is
  product; the succession record is campaign-only (§EC-4).

## 19. MINIMALITY EVIDENCE / CLAIM CEILING

**No comparative minimality evidence** (EC-1 intact). Controller B deliberately
did **not** run a staged-reveal / smaller-state probe (B-ALT-1 rejected as
measurement-only). What *is* now supported:

- **Sufficiency (candidate head):** the Task A + Task B change set — a
  current-direction Markdown surface (`STATUS.md`) + an ordered reconstruction
  reading path + `CONTEXT.md` source-of-truth row + historical markings that the
  deterministic drift machinery honors — was **sufficient** for Controller B, a
  genuinely fresh controller, to reconstruct direction and independently select
  a warranted task. Bounded: B also had the campaign durable tree; a repo-only
  test was not run.
- **Ceiling:** this is the **"smallest currently supported candidate"**, not
  strict minimality. Which individual elements are load-bearing vs redundant is
  untested. Task B's own fix (marker-honoring classifier vs. a front-matter
  schema / path move / filename rule) is argued smallest *from evidence*, not
  comparatively tested.

## 20. CAMPAIGN ACCEPTANCE STATUS

Toward the 19 conditions after **Task A + the A → B succession + Task B**
(Controller B assessment; full argument in `controllers/B-cycle-result.md`):

- **1 (Fresh semantic controller succession):** MET at the honest evidence level
  — Controller B (new context, only the allowed bootstrap, no predecessor
  transcript/reasoning) took over semantic control, owning Task B selection.
  Bounded by EC-2.
- **2 (Isolation evidence):** MET — provenance recorded (`A-handoff.md` +
  `STARTUP-PROVENANCE.md`); honest classification: context HARNESS-REPORTED,
  bootstrap-minimality/immutability/non-resumption CONTROLLER-ASSERTED,
  predecessor-process non-persistence `SUCCESSION_ISOLATION_UNVERIFIED`.
- **3 (Durable mission reconstruction):** MET — reconstructed from CHARTER +
  OWNER-INSTRUCTION, not out-of-band (`B-reconstruction-and-selection.md` Q1).
- **4 (Authority reconstruction):** MET — Q2/Q3.
- **5 (State-plane reconstruction):** MET — the successor-checkpoint fields
  distinguish integrated / candidate / semantic state.
- **6 (Strategic reconstruction):** MET — Q7–Q16.
- **7 (Verification-bearing continuation):** MET — 12 consequential claims
  reverified before acting; corrections were cosmetic (no
  `HANDOFF_FACT_TRUST_FAILURE`).
- **8 (Independent next-task selection):** MET — B compared ≥4 boundaries and
  selected one that partially rejects A's frontier.
- **9 (Immutable successor checkpoint):** MET — `4ccbc70`, committed before Task
  B implementation and before any predecessor semantic feedback.
- **10 (Real Product Advancement):** MET — Task A (consequential
  development-direction reconstruction surface + verified boundary confirmation)
  **plus Task B** (substantive deterministic-machinery change:
  `scripts/probe_relationships.py` + 4 regression tests, naturally sized,
  resolving the acceptance-15 contradiction Task A introduced). Not enlarged to
  look substantial; not a manufactured patch.
- **11 (Second strategic cycle):** MET — Controller B executed Task B against
  the changed candidate state.
- **12 (Strategic/Local distinction):** MET — B explicitly rejected B-ALT-3
  (instance cleanup) and the "add roadmap.md to a skip list" nearby-defect
  framing in favor of the general marker mechanism
  (`B-reconstruction-and-selection.md` Part 3).
- **13 (No Premature Infrastructure):** MET — Task A: Markdown only. Task B:
  an opt-in marker honored by one existing classifier function + tests; **no**
  schema / hook / state machine / router / new artifact type / workflow / gate /
  registry field.
- **14 (Architecture remains revisable):** MET — B narrowed A's F-list (F-a/F-b
  folded, F-d rejected, F-c confirmed owner-blocked); H2/H6/formalization-rule
  assessed in `B-cycle-result.md`.
- **15 (Relevant product consistency):** MET — the one known contradiction among
  surfaces Campaign 2 changed (Task A's prose historical headers vs. the probe
  classifier still treating those files as live) is resolved by Task B.
- **16 (Qualification):** candidate head qualified locally (validate-repo 0;
  probe gate PASS; test-validators 78/78; core-assertions 103p/1s); exact-head
  CI on `b77ad04` to be confirmed (§15); pre-existing local reds classified
  (D2b + 2 platform reds, identical on baseline).
- **17 (Honest evidence ceilings):** MET — EC-1..EC-5 explicit; MG-4/MG-5/MG-8
  open by design.
- **18 (Minimality honesty):** MET — no strict-minimality claim; "smallest
  currently supported candidate" only (§19).
- **19 (Succession integrity):** MET — the predecessor did not resume semantic
  control over Controller B's cycle (bounded by EC-2's process-persistence
  caveat, disclosed).

**Disposition read (Controller B):** after the mandatory A → B succession and two
strategic cycles, the materially relevant acceptance conditions hold at an
honest evidence level; the central question is answerable (§10.2 BF-1); a
Controller C handoff is optional and would not change the answer. This points to
**`CAMPAIGN_COMPLETE`** — but campaign **termination is owner-reserved**
(`CHARTER.md` OWNER-RESERVED DECISIONS), so Controller B records the disposition
read and the final-report inputs in `controllers/B-cycle-result.md` and does
**not** itself declare the campaign closed. `OWNER_DECISION_REQUIRED` for:
merge of PR #269, and formal campaign termination.

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
- **v4 (2026-09-02, Controller A, A → B handoff):** `controllers/A-handoff.md`
  committed (pre-handoff invariant 11/11; full provenance; verbatim bootstrap);
  handoff head recorded; isolation classified; post-Task-A frontier candidates
  F-a..F-d recorded as LAST ASSESSED CANDIDATE. Controller A relinquished
  semantic control.
- **v5 (2026-09-02, Controller B, A → B succession + Task B executed):**
  Fresh Controller B reconstructed + reverified the durable state (12
  consequential claims, all correct at the decision level; corrections N-1 CI
  also-green-on-358b5a2, N-2 three SHA placeholders filled), committed its
  independent reconstruction + Task B selection checkpoint
  (`controllers/B-reconstruction-and-selection.md` @ `4ccbc70`) **before**
  implementation and **before** any predecessor semantic feedback, partially
  rejecting/extending A's F-list. **U-4 RESOLVED** — the deterministic drift
  machinery did not honor Task A's prose historical headers. **Task B executed**
  (`b77ad04`): `scripts/probe_relationships.py` — an opt-in
  `<!-- doc-status: historical -->` marker the live-document classifier honors
  (`_declared_doc_status` + `_classify_doc_file(rel, declared_status)` +
  `_discover_docs` wiring); marker applied to `roadmap.md` + `goal.md`; +4
  regression tests. Deterministic machinery only — no new schema / gate /
  blocking type / artifact / workflow / hook. Qualified (validate-repo 0, probe
  gate PASS, test-validators 78/78, core-assertions 103p/1s; 70/70 across
  probe_relationships-dependent modules; 3 pre-existing local reds reproduce on
  baseline). MG-1/MG-2/MG-3 addressed (CC-2); MG-6 partially resolved (§EC-4);
  MG-7m resolved (candidate head); MG-8 added; DB-1..DB-3 deferred; FO-5 +
  succession-integrity note added; CCO-2 recorded; EC-1 preserved; EC-4/EC-5
  partially advanced. **Acceptance conditions materially satisfied at an honest
  evidence level (§20).** Disposition read: **CAMPAIGN_COMPLETE**, but formal
  campaign termination + PR #269 merge are `OWNER_DECISION_REQUIRED`. Full
  cycle result + final-report inputs: `controllers/B-cycle-result.md`.
