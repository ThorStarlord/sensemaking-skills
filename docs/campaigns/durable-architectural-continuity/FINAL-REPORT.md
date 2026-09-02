# Campaign 3 Final Report — Durable Architectural Continuity During Coupled Implementation

```
DATE:        2026-09-02
BRANCH:      campaign/durable-architectural-continuity  (base: origin/main @ 969e8eb)
CAMPAIGN HEAD AT REPORT:  <this report's commit> (follows CAMPAIGN-STATE v2;
             b677ffb bootstrap, 2fd1027 Phase 1 selection).
AUTHORITY:   non-authoritative campaign report. Not an ADR, contract, schema,
             registry, validator input, or registered workflow. Nothing in
             scripts/, src/, tests/, or .github/ reads this file. It ratifies
             nothing and merges nothing.
AUTHOR:      the lead Campaign 3 controller (Controller A; the context that
             received the owner instruction, ran Phase 0, and executed Phase 1).
FORMAT:      OWNER-INSTRUCTION.md "Final Campaign Report" (23 sections). Sections
             tied to a coupled implementation / controller succession are marked
             NOT APPLICABLE with the reason, because Phase 1 concluded no coupled
             capability was warranted.
SOURCES:     OWNER-INSTRUCTION.md; CHARTER.md; STARTUP-PROVENANCE.md;
             controllers/A-selection.md; CAMPAIGN-STATE.md v2; and, at
             origin/main @ 969e8eb, the product-surface reads listed in
             A-selection.md plus an independent fresh-context probe.
```

---

## 1. Executive Outcome

**No product capability was built.** Campaign 3's Phase 1 (select the product
capability first) concluded **`NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`**: the
repository does not currently expose a warranted, in-campaign-authority product
capability whose smallest coherent implementation is genuinely semantically
coupled across multiple product surfaces, and none could be selected without
distorting real product priority.

The repository is in a deliberate, multiply-corroborated **"harden only where
pressured / sensemaking loops saturated / no further product change warranted"**
posture. Its single highest-leverage product boundary — Goal A external product
validation — is owner-reserved and paused at a substrate boundary its own
durable evidence classifies as non-product-surface. The two genuinely coupled
candidates in the codebase are, respectively, deferred by a ratified ADR with
zero real-use pressure, and behind an unmet machinery-promotion gate.

Per the owner instruction, this is "a legitimate campaign result, not a
failure." The central architectural-continuity question — *can architectural
intent survive semantic campaign-controller replacement while a genuinely
coupled product capability is still incomplete?* — **is not answerable by
Campaign 3**, because its precondition (a warranted coupled capability) is
absent. No coupled partial architecture was created; no controller succession
was performed; no `main` change and no PR merge occurred.

**Final campaign disposition: `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`.**

## 2. Starting Product State

- **Starting `origin/main` (Campaign 3 base):**
  `969e8eb47144ffdeb27a8d9df02b6a292586e842` — "Merge pull request #270 from
  ThorStarlord/docs/campaign2-closure-stamp". Verified 2026-09-02
  (`git fetch origin --prune; git rev-parse origin/main`). No drift for the
  campaign (`git log 969e8eb..origin/main` empty at report time).
- **PR #269 integration:** `GITHUB-VERIFIED` — MERGED 2026-09-02T19:32:04Z,
  merge commit `7e48cf0`, an ancestor of `969e8eb`.
- **Campaign 2 closure state:** disposition `CAMPAIGN_COMPLETE`
  (`docs/campaigns/durable-repo-self-development/FINAL-REPORT.md` §17). Owner
  merged the work (PR #269) after an independent narrow review recommended
  MERGE; owner left the `<!-- doc-status: historical -->` marker **NON-NORMATIVE**
  (a probe heuristic, not a ratified convention); closure stamp = PR #270
  (`969e8eb`). No Controller C.
- **Campaign 1 evidence** (PR #268, merge `06a57d1`): durable execution
  continuity — a persistent controller dispatching fresh bounded *workers* from
  a durable Markdown record; disposition `CAMPAIGN_COMPLETE`, closed with "no
  further product change is warranted by current evidence."
- **Campaign 2 evidence:** durable strategic continuity — Controller A -> durable
  strategic state -> fresh *Controller* B -> independent reconstruction ->
  re-verification -> predecessor-frontier disagreement -> independent strategic
  selection -> qualified product work. Its own answer (`FINAL-REPORT.md` §16):
  the smallest currently-evidenced sufficient durable state for development
  direction to survive controller replacement is a current-direction Markdown
  surface + a reconstruction reading path + historical markings the drift
  machinery honours — "SUPPORTED AS THE SMALLEST CURRENTLY EVIDENCED CANDIDATE",
  not strict minimality.
- **Inherited evidence ceilings** (owner instruction + Campaign 2;
  `STARTUP-PROVENANCE.md` §4): Campaign 2 did NOT establish independent
  process/model succession; concurrent controllers; universal autonomous
  repository development; **deep coupled multi-surface implementation under
  succession** (Campaign 3's target); formal Sensemaking Skills self-hosting;
  strict minimality of durable continuation state. Succession isolation ceiling:
  context `HARNESS_REPORTED`; process/model `SUCCESSION_ISOLATION_UNVERIFIED`.
  Scale: n=1..2 controllers, one repo, short horizon.

## 3. Product Capability Selection

```
CANDIDATES SURVEYED (controllers/A-selection.md Part 2):
  C-1  Goal A execution-substrate repair
  C-2  the nine docs/workflow-system-disposition.md section 6 decisions
  C-3  extend the doc-status marker to other historical-in-place root docs (DB-2)
  C-4  an `unevaluable` verdict category for repair_verification_report
  C-5  a mechanical staleness signal for STATUS.md (MG-8)
  C-6  the C1/C2 formative-critique / independent-review research direction
  C-7  engineering debt (D2b / D19 / platform reds / stale egg-info)
  C-8  MODEL_WARRANT `FULL` materialization  (surfaced by the independent probe)

HIGHEST-LEVERAGE PRODUCT BOUNDARY:
  C-1 — Goal A external product validation. It is the only workstream that
  advances the product's central unvalidated hypothesis (brief usefulness beyond
  this repository).

WHETHER THE HIGHEST-LEVERAGE BOUNDARY WAS BLOCKED / OWNER-RESERVED:
  YES, both. Goal A is paused at an execution-substrate boundary its own durable
  evidence classifies as non-product-surface and `HARNESS_ENVIRONMENT_FAILURE`
  ("the producer sub-agent could not persist its own frozen brief"; provenance
  crossed an un-pinned object store). Resuming "needs an owner/environment
  decision, not a repo-code change" (STATUS.md); an episode "requires a separate,
  fresh owner authorization"; tracked as owner-reserved in Issue #255.

WHY THE COUPLED CAPABILITY WAS OR WAS NOT SELECTED:
  Not selected. The only two candidates with a genuine cross-surface semantic
  invariant were C-8 and C-4.
    C-8 (MODEL_WARRANT FULL) — genuinely coupled (warrant semantics ->
      representation_sufficiency contract -> producer map -> runtime seam ->
      validator -> tests -> docs) — is DEFERRED BY RATIFIED ADR 0015
      ("FULL remains deferred and is never inferred", line 182;
      warrant_gate.py:146-148 "Not implemented in this bounded slice
      (deferred)") with ZERO real-use pressure. The campaign has no authority to
      silently contradict a ratified ADR; CONTEXT.md principle 10 gate unmet;
      no product warrant independent of the experiment. Reopening the deferral
      is OWNER_DECISION_REQUIRED.
    C-4 (`unevaluable` verdict) — mildly coupled — is a "v0 note", 6 doc
      mentions repo-wide, UNRATIFIED, with no recorded real-use failure the
      missing category caused. The machinery-promotion gate is explicitly unmet.
  Every other candidate (C-1..C-3, C-5..C-7) is owner-reserved, single-surface
  local cleanup, pre-existing non-capability debt, or inactive research.

WHY EXPERIMENTAL USEFULNESS DID NOT DISTORT PRODUCT PRIORITY:
  The owner instruction fixes the order — product need -> task selection ->
  assess coupling -> experiment if warranted — and forbids "NEED COUPLED
  EXPERIMENT -> SEARCH FOR A TASK THAT FITS IT" in bold. Selecting C-8 or C-4
  (or inflating C-3 / C-7) would have been exactly that: choosing the more
  architecturally interesting option, against a ratified deferral or an unmet
  promotion gate, to give the succession experiment something to run on. The
  owner instruction: "Do not manufacture coupled work."
```

## 4. Coupling Analysis

No coupled capability was selected, so there is no realized cross-surface
invariant to report. The analysis that led there:

- **Cross-surface invariant existed only for deferred candidates.** C-8's
  invariant ("every surface that reads or asserts MODEL_WARRANT must agree on
  what `FULL` means and when it is materialized") is real and would obligate
  ≥6 surfaces — but ADR 0015 has ratified that this invariant stays *unrealized*
  (FULL deferred). C-4's invariant ("a non-observation is not a closure") is
  real but small, and the repository's promotion gate says it is not yet earned.
- **Why local correctness was, for every in-authority candidate, sufficient.**
  C-2 (nine §6 items) — each is an independent registry/overlay/doc edit; no
  shared invariant binds them; a maintainer can verify each in isolation. C-3 —
  adding a marker line to three files that an existing classifier already
  honours. C-5 / C-7 — a single new validator, or a fixture repair, each
  checkable alone.
- **Why scope was not experimentally inflated.** Nothing was scoped up.
  Controller A did not distribute a small change across components to
  manufacture coupling (a pattern the owner instruction names as forbidden), and
  did not select a lower-value coupled candidate because it was "more
  architecturally interesting."

## 5. Architectural Decisions

**NOT APPLICABLE.** No product capability was selected, so Phase 2 (Controller A
resolves architectural intent) was not entered and no consequential
architectural decision with an authority basis + candidate decision status was
recorded. The only decisions Campaign 3 made are:

| Decision | Authority basis | Candidate status |
|---|---|---|
| Campaign 3 baseline = `origin/main` @ `969e8eb`; continue against recorded base (no drift) | `CAMPAIGN_IMPLEMENTATION_AUTHORITY` | `ADOPTED_FOR_CANDIDATE` |
| Phase 1 disposition = `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED` | `CAMPAIGN_IMPLEMENTATION_AUTHORITY` (an evidence finding within campaign authority) | `ADOPTED_FOR_CANDIDATE` |
| Do NOT select C-8 (MODEL_WARRANT FULL) — it contradicts ratified ADR 0015 | `RATIFIED_PRODUCT_AUTHORITY` (the ADR governs) | n/a — the campaign defers to the ADR |
| Do NOT extend the `doc-status` marker (C-3) beyond `roadmap.md`/`goal.md` | `RATIFIED_PRODUCT_AUTHORITY`-adjacent (owner left the marker NON-NORMATIVE) | n/a |

## 6. Controller A Implementation

**No product implementation.** Controller A's work product is:

- Phase 0 preflight (`STARTUP-PROVENANCE.md`): baseline reconstruction; Campaign
  2 closure reconstruction; qualification-infra inventory; authority mapping;
  fresh-Controller-B instantiation check.
- The Campaign 3 durable scaffolding (`OWNER-INSTRUCTION.md` verbatim;
  `CHARTER.md`; `CAMPAIGN-STATE.md`; `controllers/README.md`).
- Phase 1 (`controllers/A-selection.md`): current-product-state reconstruction;
  the 8-candidate capability survey; an independent fresh-context corroboration
  probe; the Phase 1 disposition with full rationale.
- `CAMPAIGN-STATE.md` v2 + this report.

All of it is under `docs/campaigns/durable-architectural-continuity/` — campaign
instrumentation only. **No product surface (`src/`, `scripts/`, `skills/`,
`tests/`, `docs/adr/`, contracts, registries, `.github/`) was touched.**

## 7. Transitional State

**NOT APPLICABLE.** No partial implementation was created. Phase 3 (create
genuine partial implementation) was not entered. There are no intentional
transitional inconsistencies, no temporary exceptions, and no expected-red or
expected-incomplete validation introduced by Campaign 3. Pre-existing platform
reds on `main` (D2b fixture drift; two platform reds; stale `egg-info` version)
are recorded in `STARTUP-PROVENANCE.md` §6 as inherited context, untouched.

## 8. Controller Succession Provenance

**NO CONTROLLER SUCCESSION WAS PERFORMED** (no coupled partial architecture to
hand off). For completeness, the fresh-context mechanism that *would* have been
used, and the one fresh context that *was* used as an ordinary instrument:

```
LAUNCH MECHANISM (available, verified):  Claude Code `Agent` tool,
                                         subagent_type general-purpose,
                                         run in background. isolation:"worktree"
                                         available for a dedicated checkout.
MODEL / CONTEXT:                          claude-sonnet-5 (same family as the
                                         lead controller).
PREDECESSOR PROCESS PERSISTENCE:          the parent process persists and
                                         receives the sub-agent's final report
                                         (SUCCESSION_ISOLATION_UNVERIFIED on that
                                         dimension).
FRESH CONTEXT ACTUALLY USED:              one general-purpose sub-agent as a
                                         Phase 1 corroboration probe — NOT a
                                         semantic controller succession. It
                                         received a mechanical reconstruction
                                         task (no Campaign 3 mission text, no
                                         access to any controllers/*.md), was
                                         scoped away from
                                         docs/campaigns/durable-architectural-continuity/
                                         (it confirmed it read nothing there),
                                         and returned an independent verdict.
                                         Full prompt + result summary:
                                         controllers/A-selection.md Part 5.
ISOLATION CLAIM:                          HARNESS_REPORTED_ISOLATION for context;
                                         SUCCESSION_ISOLATION_UNVERIFIED for
                                         process/model. Unchanged from Campaign 2.
SUCCESSOR CHECKPOINT SHA:                 n/a (no successor controller).
```

## 9. Controller B Reconstruction

**NOT APPLICABLE.** There was no Controller B. (The Phase 1 corroboration probe
was a fresh *worker* given a bounded reconstruction question, not a fresh
*controller* taking semantic campaign ownership.)

## 10. Architectural Reassessment

**NOT APPLICABLE.** No predecessor architecture existed to preserve, refine,
reject, redesign, revert, or escalate.

## 11. Coupled Implementation Trace

**NOT APPLICABLE.** No coupled implementation. No semantic obligations were
created or discharged.

## 12. Architectural-Continuity Result

**NOT ASSESSABLE BY CAMPAIGN 3.**

```
ARCHITECTURAL_CONTINUITY_DEMONSTRATED / PARTIAL / FAILED:  none of these.
```

The classification presupposes a coupled partial implementation handed across a
fresh-controller boundary. Campaign 3 did not create one, because doing so
would have required manufacturing coupled work against the owner instruction's
explicit prohibition. Campaign 3 therefore contributes **no new evidence** on:

```
MISSION_RECONSTRUCTION            n/a
AUTHORITY_RECONSTRUCTION          n/a
INTENT_RECONSTRUCTION             n/a
INTEGRATED_VS_CANDIDATE_STATE     n/a
DECISION_AUTHORITY_RECONSTRUCTION n/a
DECISION_STATUS_RECONSTRUCTION    n/a
TRANSITIONAL_STATE_RECONSTRUCTION n/a
CROSS_SURFACE_OBLIGATION_RECON    n/a
EXPECTED_FAILURE_RECONSTRUCTION   n/a
PREDECESSOR_REASSESSMENT          n/a
VALIDATION_BOUNDARY_RECONSTRUCTION n/a
CONTEXT_COMPRESSION_VALUE         n/a
SUCCESSION_ISOLATION_EVIDENCE     none added (ceiling unchanged from Campaign 2)
```

## 13. Post-Hoc Continuity Audit

**NOT APPLICABLE.** No A architecture record, A handoff, B reconstruction, or B
implementation exists to audit. The one retrospective check performed was:
Controller A reverified the single consequential factual claim the independent
probe raised that Controller A had not already established (C-8: the
MODEL_WARRANT FULL deferral) — confirmed against `warrant_gate.py:146-148` and
`docs/adr/0015-...:182`. No divergence.

## 14. Failure Observations

No campaign failure in the taxonomy occurred. Two low-severity observations:

- **FO-1 (harness, minor, disclosed) — probe scoping.** The Phase 1
  corroboration sub-agent was instructed to scope `Grep`/`Glob` away from
  `docs/campaigns/durable-architectural-continuity/` and confirmed it read
  nothing there. It noted (from a prior campaign's FO-3) that an earlier
  probe had incidentally surfaced ~30 lines of an excluded campaign path; it did
  not rely on any such lines. No material effect. (This applied the Campaign 2
  FO-3 lesson pre-emptively.)
- **FO-2 (not a failure) — the Phase 1 finding rests substantially on the
  repository's own converged self-assessment** (four independent documents
  saying "harden only where pressured / loops saturated / no further product
  change warranted"). This is durable evidence, not a defect, and the
  independent probe re-derived the same posture from the same sources plus its
  own `gh` verification — but a reader should note the disposition is a judgment
  that the repository's stated posture is accurate, corroborated by two
  contexts, not an independently measured fact.

`DOES THIS WARRANT NEW INFRASTRUCTURE:` **NO.** No schema, hook, router,
workflow, Skill, graph, or state machine was created or is recommended.

## 15. Durable-State Assessment

What Campaign 3's own durable state was worth:

| Information | Assessment |
|---|---|
| `OWNER-INSTRUCTION.md` verbatim | **essential** — the campaign's authority source; a fresh controller could reconstruct the mission and the order-of-operations constraint from it. Not exercised by a successor this campaign. |
| `CHARTER.md` | **useful** — condenses the 12 non-negotiable constraints and the six terminal conditions; faster to read than the full instruction. |
| `STARTUP-PROVENANCE.md` | **useful** — records the Phase 0 facts (baseline SHA, Campaign 2 closure, authority map, fresh-B check) so they need not be re-derived. Some content (SHAs, PR states) is cheap to reverify and was recorded mostly to make the preflight auditable. |
| `controllers/A-selection.md` | **essential** — the 8-candidate survey and the reasoning for `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED` is the campaign's actual deliverable and the expensive part to reconstruct. |
| `CAMPAIGN-STATE.md` | **partly redundant here** — with no succession and no evolving candidate architecture, most of its section skeleton stayed near-empty. Its value is as a single index; it did not have to carry cross-controller strategic memory this campaign. |
| the independent probe prompt + result (in `A-selection.md` Part 5) | **useful** — converts "Controller A concluded X" into "two independent contexts concluded X". Cheap (~24 tool calls). |

**Campaign-specific vs product-worthy:** everything Campaign 3 produced is
campaign instrumentation. Nothing here is a candidate product artifact. (This is
consistent with Campaign 2's H9 finding that campaign state and product state
differ; Campaign 3 adds a mild data point — a campaign that terminates in Phase
1 needs even less durable state than one that runs a succession.)

## 16. Context-Compression Result

- **Cheap to reverify (did):** the baseline SHA and no-drift; PR #269/#270 merge
  state; the open-issue / open-PR set; ADR status lines; `warrant_gate.py:146`
  and `ADR 0015:182`; the `src/`/`scripts/` unfinished-primitive scan.
- **Expensive to reconstruct (durable state earned its place):** *why* the
  repository is in a "harden only where pressured / do not build" posture — it
  requires reading the research-agenda meta-finding, both campaign FINAL-REPORTs,
  and `CONTEXT.md` principle 10 *together*. Both Campaign 2's A1 probe and
  Campaign 3's probe independently flagged this as the expensive-to-reconstruct
  piece.
- **Had to be rediscovered:** the C-8 candidate (MODEL_WARRANT FULL) — not named
  in any durable strategic summary; the independent probe found it by reading
  `warrant_gate.py`. This is the healthy pattern (cheap code facts -> re-read
  source; expensive rationale -> durable state).

## 17. Emergent Product Primitives

None warranted. Campaign 3 did not run a coupled implementation, so the
concepts the owner instruction lists as candidates (change obligation,
cross-surface invariant, transitional exception, closure obligation, reopen
condition) were not exercised on real product work and gained no evidence toward
first-class representation. **Do not formalize any of them on the basis of
Campaign 3.**

## 18. Skill / Workflow Implications

None. No recurring bounded responsibility was exercised often enough to assess.
One incidental observation, evidence-light: "reconstruct the current
product-development frontier and classify open work by authority" is a
responsibility that has now been performed by a fresh context in Campaign 2 (A1)
and Campaign 3 (the Phase 1 probe) with similar prompts and similar ~15-25
tool-call cost. That is **n=2, not a pattern**, and the owner instruction's
formalization gate (recurring + stable semantics + material omission/error cost
+ mechanically useful boundary) is not met. Recorded, not acted on.

## 19. Qualification

```
CAMPAIGN BASE:            origin/main @ 969e8eb47144ffdeb27a8d9df02b6a292586e842
CURRENT origin/main:      969e8eb  (no drift; re-checked 2026-09-02)
FINAL CANDIDATE HEAD:     <this report's commit>  (b677ffb bootstrap ->
                          2fd1027 Phase 1 -> CAMPAIGN-STATE v2 -> this report)
TARGETED TESTS:           none run and none needed — no product surface (src/,
                          scripts/, skills/, tests/, .github/, contracts,
                          registries, ADRs) was modified. `git diff --stat
                          969e8eb..HEAD` touches only
                          docs/campaigns/durable-architectural-continuity/.
BROADER TESTS:            n/a (no product change to qualify).
VALIDATORS:              n/a. (For reference: the campaign directory is
                          non-authoritative; nothing in scripts/ reads it. The
                          probe's `doc-status` classifier would treat these
                          evolving campaign files as `live`, contributing the
                          same benign quoted-evidence noise class as the other
                          campaigns' records — Campaign 2 DB-3; not Campaign 3's
                          to change.)
BUILD / PACKAGE CHECKS:   n/a.
CI:                      to run on push via a draft campaign-evidence PR
                          (docs-only diff; expected green — the "Validator
                          Ecosystem" jobs do not depend on docs/campaigns/**).
PR STATE:                draft campaign-evidence PR to be opened, NOT for merge.
MERGE STATE:             not merged; nothing from Campaign 3 will be merged.
POST-INTEGRATION STATE:  n/a.
EXCEPTIONS:              none introduced by Campaign 3. Inherited pre-existing
                          platform reds (STARTUP-PROVENANCE.md §6) are untouched.
```

## 20. Evidence Ceilings

Campaign 3 explicitly does **not** establish:

- **Deep coupled multi-surface implementation under succession** — the boundary
  it set out to test. Not tested, because no warranted coupled capability
  existed to build it on. The ceiling from Campaign 2 (EC-a) **stands
  unchanged.**
- **Independent process succession** — not tested (no succession performed).
- **Independent model-family succession** — not tested.
- **Concurrent controllers** — not tested.
- **Universal architecture continuity** — not tested.
- **Production-grade autonomous development** — not tested; one campaign that
  terminates in Phase 1 says nothing about reliability at scale.
- **Durability beyond the observed horizon** — n/a.
- **Formal Sensemaking Skills self-hosting** — not attempted (bootstrap
  constraint honoured; Sensemaking Skills was not used as the campaign
  controller).
- **Strict minimality of any durable-state arrangement** — not tested.

What Campaign 3 **does** contribute (bounded):

- A dated, independently-corroborated finding that as of `origin/main` @
  `969e8eb`, the repository exposes **no in-authority, materially-leverage,
  semantically-coupled product capability** — i.e. the precondition for the
  Campaign 3 experiment is currently absent. This is a statement about the
  repository's development posture at one point in time, not about the
  architectural-continuity question itself.
- A mild data point that a campaign terminating in Phase 1 needs less durable
  state than one running a succession (§15) — consistent with Campaign 2's H9.

## 21. Remaining Product Limitations and Debt

**Strategic product limitations** (pre-existing; not Campaign 3's to resolve):

- The product's central hypothesis — brief usefulness beyond this repository —
  is unvalidated and its validation workstream (Goal A) is paused at an
  owner/environment-reserved substrate boundary (Issue #255).
- MODEL_WARRANT `FULL` materialization is deferred (ADR 0015); the deferral is
  intentional and unpressured.

**Engineering debt** (pre-existing; deferred; none in CI):

- D2b (`tests/test_validate_brief_json.py` fixture drift); D19; two platform
  reds; committed `src/sensemaking_skills.egg-info/PKG-INFO` at 0.2.1 vs
  `pyproject` 0.2.2.

**Unvalidated hypotheses:**

- That the repository's stated "harden only where pressured / loops saturated"
  posture is exhaustive — i.e. that no product-capability pressure exists that
  neither Campaign 2's A1 probe, Campaign 3's probe, nor the incumbent
  controller has seen. Two independent reconstructions found none; that is
  corroboration, not proof.

**Owner decisions** (standing; not Campaign 3 blockers — see §22).

**Environment blockers:**

- The Goal A Run-1 substrate failure (`HARNESS_ENVIRONMENT_FAILURE`: the
  producer sub-agent could not persist its own frozen brief; provenance crossed
  an un-pinned object store). Classified by the repository's own reassessment as
  non-product-surface and needing an owner/environment decision.

**Deferred local work** (inherited from Campaign 2; none capability-level;
`CAMPAIGN-STATE.md` §14): DB-1 (`CHANGELOG.md` footer), DB-2 (marker on other
historical root docs), DB-3 (`docs/campaigns/**` probe noise), MG-8 (`STATUS.md`
staleness signal), FO-4 (probe `adr/status_claim_mismatch` false-positive).

## 22. Owner Decisions

Campaign 3 raises **no new owner-decision question that blocks campaign work**.
The following are standing owner-reserved items, listed so a future campaign
does not mistake them for available engineering:

1. Whether/when to resume Goal A and authorize a next A1 episode, and how to
   provide a compliant execution substrate (Issue #255).
2. The nine `docs/workflow-system-disposition.md` §6 registry/overlay/contract/
   documentation decisions.
3. Whether to reopen the ADR 0015 deferral of MODEL_WARRANT `FULL` (no pressure
   to do so was found).
4. Whether to ratify any Campaign 1 or Campaign 2 conclusion (including the
   NON-NORMATIVE `doc-status` marker) as product architecture.

None of these requires an answer for Campaign 3 to reach its disposition; each
is the repository's normal integration/authorization boundary.

## 23. Final Campaign Disposition

```
NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED
```

**Why precisely this.** The owner instruction defines this disposition for
exactly the situation found: "no sufficiently coupled capability can be selected
without distorting real product priority." Phase 1 established, and an
independent fresh context corroborated, that (a) the repository's genuine
product frontier (Goal A) is owner-reserved and non-code; (b) the in-authority
backlog is deliberately small maintenance and owner-reserved micro-decisions;
(c) the only genuinely coupled capabilities in the codebase are deferred by
ratified authority (C-8) or behind an unmet promotion gate (C-4); and (d)
selecting any of these to run the experiment is the anti-pattern the owner
instruction forbids in bold. The repository is in a deliberate "harden only
where pressured / loops saturated / no further product change warranted"
posture, and Campaign 3 respects it.

**Why not the alternatives.**

- **Not `CAMPAIGN_COMPLETE`** — no coupled capability was built through
  incomplete-architecture controller succession; the success conditions
  (genuine coupling, real partial implementation, fresh succession, continuity
  disposition) are unmet because their precondition is absent.
- **Not `CAMPAIGN_PREMISE_INVALIDATED`** — durable architectural continuity
  during coupled implementation is not shown to be a wrong or irrelevant
  research question. The repository simply does not currently expose a warranted
  coupled product capability to test it against. This is a state/timing result,
  not a structural refutation. If the owner reopens the MODEL_WARRANT `FULL`
  deferral, or a future real-use failure pressures the `unevaluable` boundary,
  or Goal A's substrate is provided and its downstream engineering surfaces a
  coupled need, a later campaign could run the Campaign 3 experiment on a
  genuine target.
- **Not `OWNER_DECISION_REQUIRED`** — no bounded campaign work is *blocked*
  waiting on an owner answer. The owner-reserved items are the repository's
  standing boundary, not a Campaign 3 gate (§22).
- **Not `EXTERNAL_BLOCKER`** — the fresh-controller substrate exists at the
  Campaign 2 ceiling (`STARTUP-PROVENANCE.md` §8); nothing environmental
  prevented Campaign 3 from proceeding. There was simply nothing warranted for
  it to build.
- **Not `SUCCESSION_FAILURE_REQUIRES_REDESIGN`** — no succession was attempted,
  so nothing about the handoff/state model failed.

**Closure.** Per the owner instruction's Campaign Closure Rule, Campaign 3 stops
here: its central architectural-continuity question can be answered at an honest
evidence level — *not answerable now, because the repository does not currently
warrant a coupled product capability* — and continuing "merely because more
product work exists" or "another coupled feature could be built" is explicitly
forbidden. Campaign 3 is CLOSED. No Controller B. No merge. No ratification. No
change to any owner-reserved item.
