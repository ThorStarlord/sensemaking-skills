# Controller B — reconstruction and Task B selection

```
CONTROLLER:     B (fresh independent semantic controller; a new agent context
                spawned with the allowed bootstrap only — no access to
                Controller A's conversation or private reasoning).
WRITTEN:        2026-09-02, BEFORE any Task B implementation and BEFORE any
                predecessor semantic feedback.
IMMUTABILITY:   this checkpoint preserves what Controller B believed at this
                point. It is not retro-edited when later evidence shifts the
                campaign's understanding. Later CAMPAIGN-STATE.md versions may
                supersede its conclusions; this file stays intact
                (owner instruction "Mandatory Successor Checkpoint").
INPUTS USED:    CHARTER.md; OWNER-INSTRUCTION.md (read in full);
                CAMPAIGN-STATE.md v4; STARTUP-PROVENANCE.md;
                controllers/{README, A-reconstruction-and-selection,
                A-task-A1-reconstruction-probe, A-handoff}.md; repository @
                campaign head 358b5a2; `git` + `gh` read; local validators +
                probe engine + pytest run directly.
```

---

## Part 0 — Reverification log (consequential claims checked before acting)

Evidence-origin tags: `REPO` repository-verified, `GH` GitHub-verified,
`RUN` re-ran the command myself, `OI` owner-instruction-derived,
`CS` campaign-state-derived (historical evidence), `INF` controller inference.

| # | Durable-state claim | Check | Result |
|---|---|---|---|
| 1 | `origin/main` = `06a57d1d182a32684275d343a9248429feedbfe6`, no drift since campaign start | `git fetch origin --prune; git rev-parse origin/main`; `git log 06a57d1..origin/main` | **CORRECT.** origin/main is `06a57d1`; zero commits since. `REPO` `GH` |
| 2 | PR #268 merged; its merge commit **is** current `origin/main` | `gh pr view 268 --json state,mergedAt,mergeCommit` | **CORRECT.** MERGED 2026-09-02T07:29:05Z, mergeCommit `06a57d1`. `GH` |
| 3 | Campaign branch head after handoff = the A-handoff commit | `git rev-parse HEAD` / `origin/campaign/durable-repo-self-development` | **CORRECT.** Both `358b5a23018048faa6d5aa46685281769854b4ea`. 4 commits over base: `3c55254` bootstrap, `a216293` A selection, `431ec43` Task A, `358b5a2` A→B handoff. `REPO` `GH` |
| 4 | Draft PR #269 open (`campaign/... -> main`), not for merge | `gh pr view 269` | **CORRECT.** OPEN, isDraft true, head `358b5a2`, mergeable. Title marks "DRAFT, not for merge". `GH` |
| 5 | Only other open PR is #194 (draft, "do not merge") | `gh pr list --state open` | **CORRECT.** Exactly #269 and #194. `GH` |
| 6 | Open issues: #255 (Goal A substrate), #226 (C6R gate separation), #218 (normal-use evidence lane) | `gh issue list --state open` | **CORRECT.** Exactly those three. `GH` |
| 7 | Task A product-surface diff = STATUS.md refresh + roadmap.md/goal.md historical headers + CONTEXT.md +1 source-of-truth row | `git diff 06a57d1..HEAD -- <non-campaign paths>` | **CORRECT.** `CONTEXT.md` +1 row (`STATUS.md` → current development direction); `STATUS.md` rewritten (+163/−25) into a current-direction + reconstruction-reading-path surface; `roadmap.md` +7 (blockquote historical header); `goal.md` +10 (blockquote historical header). No other product files. `REPO` |
| 8 | ADR statuses: 0013/0014 Accepted; 0017–0021 SUPERSEDED, never Accepted; 0023/0026/0027 Accepted | status-line sweep over `docs/adr/00*.md` | **CORRECT.** Also: 0006/0007/0008 Proposed; 0022 Proposed (awaiting adversarial review); 0024/0025 Accepted. `REPO` |
| 9 | Local qualification green at campaign head | `RUN`: `validate-repo.py`; `test-validators.py`; probe gate (`probe-repo` + `validate-probe-report` + `gate_relationship_findings`); `pytest` core-assertions set | **CORRECT.** `validate-repo.py` exit 0; `test-validators.py` 78 PASS / 0 FAIL; probe gate PASS (0 blocking; non-blocking evidence findings only); core-assertions 99 passed / 1 skipped. `RUN` |
| 10 | Campaign CI green on `431ec43` (Task A head) | `gh run list --branch campaign/durable-repo-self-development` | **CORRECT, and NOW ALSO GREEN ON `358b5a2`.** CAMPAIGN-STATE.md §15 records CI only for `431ec43`; the A→B handoff commit `358b5a2` (PR #269 `pull_request` event) has since completed: "Validator Ecosystem" **success** (all ~20 jobs). Narrowing recorded below. `GH` |
| 11 | `docs/workflow-system-disposition.md` section 6 lists nine implied owner decisions, none applied | read section 6 | **CORRECT.** Nine items (external-routing-sprint liveness; PM ecosystem catalog; `full-local-sensemaking` `3-conditional`; `setup-sensemaking-skills` registry entry; `autonomous-sprint-preflight`; `mode-coverage.yaml` claims; `artifact-reconciliation` definition; `architectural-review-planning-workflow` description; packaged-catalog/overlay divergence). All owner-reserved. `REPO` |
| 12 | Campaign 1 (`FINAL-REPORT.md`) demonstrated responsibility-level artifact-mediated continuation across six responsibility classes; its stated limitation: one persistent dispatcher, fresh **workers not controllers**, no `src/` change | read FINAL-REPORT §1–2, §8–9 | **CORRECT.** "Eight record-mediated handoffs, seven into fresh contexts, across six responsibility classes"; "the largest code change from durable state was one script + tests, no `src/` change"; ~22 wrong/overstated record facts caught by verification, none causing a wrong action. `REPO` |

**Claims corrected or narrowed (none decision-changing):**

- **N-1 (CI status stale by omission).** CAMPAIGN-STATE.md §15 records exact-head
  CI only for `431ec43`. The current campaign head `358b5a2` now also has green
  "Validator Ecosystem" CI. Updated in the durable state.
- **N-2 (unfilled placeholders).** CAMPAIGN-STATE.md §3 `CURRENT CAMPAIGN HEAD
  (after Task A): <A Task-A commit> (record SHA after commit)` and §16 handoff
  trace `SHA: <record after commit>` / `B checkpoint SHA to be recorded here`
  were never filled. Task A head = `431ec43`; handoff head = `358b5a2`. Filled in
  the durable state as campaign-record hygiene; not a substantive claim.
- **N-3 (probe false-positives still present).** The two non-blocking
  `adr/status_claim_mismatch` evidence findings Controller A documented
  (`CAMPAIGN-STATE.md:397`, `A-task-A1-reconstruction-probe.md:324/329`) still
  fire (verbatim ADR-supersession quotes near the token "Accepted"). Gate PASSES.
  Left as-is, per FO-4 — verbatim evidence quotes.
- Nothing in the durable state was found **wrong on a consequential fact.** This
  reconstruction is `HANDOFF_FACT_INCORRECT`-free at the decision level; only the
  cosmetic staleness N-1/N-2 above.

---

## Part 1 — The 20 fresh-controller reconstruction questions
(owner instruction "Fresh Controller Reconstruction")

**1. What is the Campaign 2 mission?** (`CHARTER-DERIVED`, `OI`)
Advance Sensemaking Skills from Campaign 1's demonstrated *responsibility-level*
artifact-mediated continuation (fresh **workers**) toward **durable
repository-level self-development**: independent fresh coding-agent *controllers*
reconstruct current product-development state, identify the highest-leverage
warranted development boundary, perform substantial bounded engineering, update
durable product-development state, and leave the repository continuable by
another fresh controller with no prior conversation context. Campaign 2 is one
thing: **real product development + controlled controller-succession evidence.**
Central question: *the smallest coherent product capability sufficient for
repository-level development direction to survive independent controller
replacement and keep producing strategically warranted engineering work.*

**2. What authority is available to me?** (`OI` "Campaign 2 Execution
Authority", `CHARTER` "AUTHORITY")
All repository/GitHub/CI reads; local engineering on the campaign branch only
(modify files, code, tests, docs when a product change warrants it; run
tests/validators/linters/probes/qualification; create commits); push the
campaign branch and later commits; create/maintain a **draft** PR (#269
exists); inspect campaign-branch CI.

**3. What authority remains reserved to the owner?** (`OI` "Not Authorized by
Default", `CHARTER` "OWNER-RESERVED DECISIONS")
Merging the Campaign 2 PR; ADR acceptance; external publication / deployment;
changing an owner-reserved product decision; treating campaign conclusions as
canonical ratification; creating/closing/reopening/relabelling/materially
modifying GitHub issues for campaign bookkeeping; merging unrelated PRs;
altering protected repository policy to make Campaign 2 pass; inferring owner
preference from repository evidence. Also reserved: the nine
workflow-system-disposition decisions; Goal A execution authorization;
terminating the campaign. Anything otherwise-warranted that crosses these →
`OWNER_DECISION_REQUIRED`.

**4. Current integrated `origin/main` state?** (`REPO` `GH`, reverified)
`origin/main` = `06a57d1` (PR #268 merge commit — Campaign 1 closure). No drift
since campaign start. "Validator Ecosystem" CI green on that lineage. The
integrated product is the "agent-native engineering sensemaking and control
layer" (`CONTEXT.md`); active coding agent owns the control loop (ADR 0013);
ratified external scope = validated, human-reviewed `repository_sensemaking_brief`
(ADR 0014); automatic fog→implementation routing **not** ratified. Repo posture:
"harden only where pressured" (`CONTEXT.md` principle 10); the control-model
research agenda's 2026-08-30 meta-finding records sensemaking loops as
"saturated"; Campaign 1 closed with "no further product change is warranted by
current evidence."

**5. Campaign 2 handoff candidate state?** (`REPO` `GH`, reverified)
Campaign branch `campaign/durable-repo-self-development` @ `358b5a2`. Four
commits over base `06a57d1`. Product-surface delta vs main: `STATUS.md` (current
development-direction + reconstruction-reading-path surface), `roadmap.md` +
`goal.md` (blockquote historical/superseded headers redirecting to
STATUS.md/CONTEXT.md), `CONTEXT.md` (+1 source-of-truth-map row → STATUS.md).
Campaign instrumentation delta: the whole
`docs/campaigns/durable-repo-self-development/` tree. Nothing merged. Draft PR
#269. Local qual + exact-head CI green on `358b5a2`.

**6. Which candidate changes are not integrated into main?** (`REPO`)
**All four** product-surface files above (`STATUS.md`, `roadmap.md`, `goal.md`,
`CONTEXT.md` row) plus every file under
`docs/campaigns/durable-repo-self-development/`. Integrated `main` still carries
the pre-Task-A limitation (STATUS.md stale/thin; roadmap.md/goal.md misleading
with no historical marker; source-of-truth map does not name a current-direction
surface).

**7. What product capabilities are currently demonstrated (integrated on
main)?** (`CS` + `REPO`, reverified where consequential)
Agent-native brief production + deterministic validation on ≥2 repositories;
responsibility-before-Skill selection without routing; claim reconciliation;
finding-specific repair verification; fail-closed authority on auto-invoke and
liveness; probe-engine enforcement gate in CI. **Responsibility-level,
artifact-mediated continuation into a fresh context** from a durable Markdown
record — six responsibility classes, verification-bearing (fresh contexts caught
~22 wrong/overstated record facts, none causing a wrong action; twice declined
an out-of-grant edit). **Limitation (Campaign 1's own words):** one persistent
dispatcher, one repo, one day; fresh contexts were **workers**, not
**controllers**; largest code change from durable state = one script + tests, no
`src/` change; strict minimality of the durable state untested.

**8. What campaign capabilities are demonstrated (Campaign 2)?** (`CS` + `REPO`)
- **CC-1 (Task A / A1):** the harness can run a credible fresh-context
  *reconstruction probe* — a fresh `general-purpose` sub-agent (no history, no
  campaign semantic state, campaign dir excluded) reconstructed the product's
  strategic headline (Goal A / A1 highest-value, substrate-blocked) and a
  defensible decided/in-flight/deferred map from durable evidence + `gh` alone
  (~15 tool calls to a defensible answer; ~22 total), and independently flagged
  the reconstruction-surface staleness. Evidence:
  `A-task-A1-reconstruction-probe.md`.
- **CC-2 (this cycle, in progress):** a genuinely fresh *controller* context
  (this one) reconstructed mission / authority / three state planes /
  capabilities / ceilings / previous-task rationale / frontier from durable
  sources + repo/GitHub evidence, reverified the consequential claims (Part 0),
  and is about to **independently select and execute** Task B. This is the first
  test of MG-1 (complete semantic controller succession, next-task selection
  included) and of F-a/U-3 (reconstruct *from the refreshed surface* and act).

**9. What evidence ceilings remain?** (`OI`, `CS`)
- **EC-1 Minimality.** A successful rich-state handoff shows SUFFICIENCY, not
  STRICT MINIMALITY. No comparative (smaller-state / staged-reveal /
  withheld-field) evidence exists. This cycle does not run a staged-reveal probe
  (reasons in Part 4); EC-1 is preserved.
- **EC-2 Succession isolation.** Context isolation HARNESS-REPORTED (fresh
  window, no transcript, no predecessor private reasoning); bootstrap
  minimality / checkpoint immutability / non-resumption CONTROLLER-ASSERTED;
  predecessor **process** non-persistence **not** environment-enforced →
  `SUCCESSION_ISOLATION_UNVERIFIED` on that dimension. Same model family
  (disclosed). My own status: I received only the allowed bootstrap; I have no
  predecessor transcript or reasoning; I am free to reject A's frontier and I do
  partially (Part 3).
- **EC-3 Scale.** Single-repo / short-horizon; not lifted.
- **EC-4 Product vs campaign state.** Whether durable *campaign* state maps to
  any needed durable *product* state is still open; Task B produces partial
  evidence (the *machinery-consistency* half of the reconstruction surface is a
  product concern; the succession provenance is campaign-only).
- **EC-5 Implementation depth.** No broad `src/` implementation depth from
  durable state. Task B is a `scripts/` (deterministic-machinery) change with
  regression tests — a modest lift of EC-5, not a resolution.

**10. What changed during the previous strategic cycle (Task A)?** (`REPO` `CS`)
Task A investigated whether repository-level development direction is
reconstructible by an independent controller (bounded responsibilities A1–A6).
A1 (fresh-context probe) **confirmed the limitation**: direction *was*
reconstructible but at ~15 tool calls across four scattered documents, with a
real wrong-anchor hazard (`roadmap.md` / `goal.md` / `CHANGELOG.md` /
`00-user-intent.md` / user auto-memory all point at a superseded PyPI/GA/
autonomous-router plan) and the current picture living in a campaign
subdirectory + GitHub issues rather than on the designated source-of-truth map.
Failure classes: `CONTEXT_RECONSTRUCTION_COST_EXCESSIVE` (primary),
`HANDOFF_FACT_INCORRECT` (caught). **Not** premise-invalidation; **not** campaign
instrumentation. Smallest warranted change, on existing Markdown surfaces:
`STATUS.md` refreshed into a current-direction + "Reconstructing current
development direction" reading-path surface; blockquote historical headers on
`roadmap.md` + `goal.md`; one additive `CONTEXT.md` source-of-truth-map row →
`STATUS.md`. `00-user-intent.md` and the `CHANGELOG.md` "Deployment Timeline"
footer were *flagged in STATUS.md*, not edited. Qualified (validate-repo 0,
probe gate PASS, test-validators 78/78, core-assertions 99p/1s); draft PR #269;
exact-head CI green. Applies to the **candidate head only** until merge.

**11. Why had the previous task been selected?** (`CS` — `A-reconstruction-and-selection.md` Parts 2–3)
Controller A compared five candidate boundaries and selected
"development-direction reconstruction surface" because it was the only candidate
that (a) sits directly on the campaign's central question, (b) is bounded /
reversible, (c) does not predetermine the solution or require new machinery,
(d) has concrete already-visible evidence the limitation exists, and (e) would
remain warranted even if controller succession were already solved (a fresh
controller still needs a reconstruction basis). Candidates 2 (promote
artifact-mediated continuation) and 3 (verification-bearing handoff) were judged
narrower / partly done and folded in; candidate 4 (`repo-sensemaker` brief as
direction state) was ruled out of ADR 0014 scope; candidate 5 (premise check)
was treated as Task A's internal decision-changing uncertainty, not a rival.

**12. Which consequential durable-state claims required reverification?**
Items 1–12 in Part 0 (state planes; PR/issue state; ADR statuses; Task A diff;
Campaign 1's demonstrated capabilities and stated limitation; local + CI
qualification). Plus the probe-engine behavior around Task A's historical
headers (Part 3, which turned out to be the decision-changing finding).

**13. Which reverified claims were correct?**
All twelve in Part 0 (with N-1 an additive CI fact, not a correction of a wrong
claim). Task A's product change is real and on the branch; its qualification
holds; the ADR/PR/issue landscape is exactly as recorded.

**14. Which claims were incomplete, stale, overstated, or wrong?**
Only cosmetic: **N-1** (CI recorded for `431ec43` only; `358b5a2` is now also
green), **N-2** (three unfilled `<...>` SHA placeholders in §3/§16). **N-3** the
FO-4 probe false-positives persist (expected). No consequential fact was wrong.

**15. What material product gaps remain?** (`CS` §9 + `INF`, reverified)
- **MG-1** No fresh context has owned the **complete semantic
  campaign-controller** role including next-task selection. *(This cycle is the
  first test; not yet "demonstrated" until Task B lands + is validated.)*
- **MG-2** No **cross-controller** semantic continuation demonstrated. *(Same.)*
- **MG-3** Only one dispatcher/controller has ever run a campaign here. *(A→B is
  the second.)*
- **MG-4** No general autonomous repository self-development; no production-grade
  reliability claim.
- **MG-5** Strict minimality of durable continuation state untested (EC-1).
- **MG-6** Unclear which part of Campaign 1's continuation capability belongs in
  the *product* vs exists only for campaign experimental control.
- **MG-7** (Controller A) The designated development-direction surfaces did not
  reflect integrated reality. **ADDRESSED on the candidate head for the
  human-facing surfaces** (STATUS.md + reading path; historical headers;
  CONTEXT.md row). **Residual — this cycle's finding:** the *deterministic
  machinery* the same fresh controller relies on (the probe engine's
  live-document classifier) still treats `roadmap.md` / `goal.md` as **live
  current-state surfaces** and flags their superseded version claims as
  conflicting evidence, because `probe_relationships._classify_doc_file` uses
  path signals only and does not read Task A's prose headers. Human surface and
  machinery disagree about what is historical → residual reconstruction cost for
  the next controller, and a known material contradiction among product surfaces
  Campaign 2 changed (acceptance condition 15). **MG-7m** (machinery half).
- **MG-8** (this cycle) `STATUS.md` is now a hand-maintained current-direction
  surface with no mechanical staleness signal of its own — the same failure mode
  (a designated surface silently goes stale) can recur. Noted; not this task's
  target (a staleness validator would need a demonstrated recurrence and is
  premature).

**16. What did the predecessor last assess as the capability frontier?**
(`CS` §10 — LAST ASSESSED CANDIDATE, not a command)
Controller A, post-Task-A, offered four frontier candidates F-a..F-d:
- **F-a** The reconstruction surface is now a *convention*, not a *tested
  capability across an independent controller*; Controller B's own
  reconstruction is the first real test.
- **F-b** MG-6 untouched — which parts of Campaign 1's continuation capability
  are product vs campaign-only.
- **F-c** The product's own top priority (Goal A / A1) is owner/environment-
  blocked (Issue #255) with no repo-code deliverable → large product
  implementation there is `OWNER_DECISION_REQUIRED`, not campaign work.
- **F-d** Comparative minimality (EC-1) entirely untested.

**17. What capability now appears to constrain progress most after independent
reassessment?** (`INF`, grounded in Part 0 + Part 3)
The reconstruction surface Task A built is **half-durable**. Its *human* half
(STATUS.md, prose headers) is on the candidate head, but its *mechanical* half
is missing: the deterministic drift machinery (`probe_relationships.py`), which
a fresh controller and CI both run, does not agree that `roadmap.md` / `goal.md`
are historical — it still scans them as live and emits their stale version
claims as conflicting evidence. For "repository-level development direction to
**survive** independent controller replacement," the machine-checkable signal a
controller relies on must agree with the human markings; otherwise every
successor re-pays the reconciliation cost A1 measured, and the convention can
silently drift from the machinery. This is the same boundary Task A opened —
the unfinished, mechanically-enforceable half — and it is where a demonstrated,
*repeated* failure (roadmap.md, goal.md, CHANGELOG.md, 00-user-intent.md all
went historical-in-place; the probe catches none of them as such) meets a
mechanically useful boundary. F-c (Goal A) is real but owner-blocked, not
campaign work. F-b (MG-6) is partly answerable as a by-product of this task.
F-d (comparative minimality) matters but is measurement, and running two more
probes across both Campaign 2 cycles would leave the campaign with **zero**
substantive product implementation, straining acceptance condition 10 while
adding an "elaborate experimental framework merely to prove theoretical
minimality" the owner instruction warns against.

**18. What serious alternative boundaries exist?** — Part 2.

**19. What bounded repository-level task is warranted next?** — Part 4.

**20. Does the predecessor's previously recorded candidate remain warranted, or
should it be rejected or replaced?**
**Partially rejected / extended.** F-a (test the surface via B's own
reconstruction) is satisfied *as a side effect* of this checkpoint, not as a
task — my reconstruction leaned on the campaign durable tree the bootstrap
pointed me at, so it is a contaminated test of the *product* surface and does
not warrant a whole cycle. F-d (comparative minimality) is **not selected** as
the task: it is measurement, and Task B is required to be able to produce
substantive product advancement (acceptance 10/11). F-c is confirmed
`OWNER_DECISION_REQUIRED`, not selected. The selected boundary is the
**machinery half of MG-7** (F-a's and F-b's substance combined): make the
deterministic live-document classifier honor an explicit historical marker, so
Task A's human markings and the probe machinery stop disagreeing. This is the
smallest change that turns Task A's *convention* into a *mechanically enforced*
property and resolves the acceptance-15 contradiction Task A introduced.

---

## Mandatory successor-checkpoint fields (owner instruction)

```
CONTROLLER IDENTITY / CONTEXT:  Controller B. Fresh agent context (claude-sonnet-5,
  Claude Code harness), spawned via the Agent tool with the verbatim bootstrap in
  A-handoff.md and nothing else. No predecessor transcript or private reasoning.
  Working in worktree H:/GithubRepositories/smk-campaign-2, branch
  campaign/durable-repo-self-development.

HANDOFF HEAD:            358b5a23018048faa6d5aa46685281769854b4ea
CURRENT ORIGIN/MAIN HEAD: 06a57d1d182a32684275d343a9248429feedbfe6
CAMPAIGN BASE:           06a57d1d182a32684275d343a9248429feedbfe6
MAIN DRIFT:              none (0 commits on origin/main since campaign start;
                         re-fetched 2026-09-02). Drift policy disposition:
                         CONTINUE AGAINST RECORDED BASE.

CANDIDATE CHANGES NOT ON MAIN:
  product surface : STATUS.md (current-direction + reconstruction reading path),
                    roadmap.md + goal.md (blockquote historical headers),
                    CONTEXT.md (+1 source-of-truth-map row -> STATUS.md)
  instrumentation : docs/campaigns/durable-repo-self-development/** (charter,
                    owner instruction, campaign state, startup provenance,
                    controllers/{README,A-reconstruction-and-selection,
                    A-task-A1-reconstruction-probe,A-handoff}.md, and this file)
  merged          : nothing

MISSION RECONSTRUCTED:  yes (Q1). CHARTER-DERIVED + OWNER-INSTRUCTION-DERIVED.

AUTHORITY RECONSTRUCTED: yes (Q2/Q3). Local engineering on the campaign branch +
  push + draft PR; merge / ADR acceptance / publication / issue lifecycle /
  owner-reserved decisions / owner-preference inference are NOT authorized ->
  OWNER_DECISION_REQUIRED.

PREVIOUS STRATEGIC TASK: Task A — establish whether repository-level development
  direction is reconstructible by an independent controller; classify any
  failure; deliver the smallest warranted product change or a verified
  "no new mechanism warranted".

WHY IT HAD BEEN SELECTED: Q11 — the only one of five candidate boundaries sitting
  directly on the central question, bounded/reversible, not predetermining the
  solution, with concrete evidence, and warranted even if succession were solved.

WHAT CHANGED: Q10 — U-2 resolved (limitation confirmed, product-surface, not
  premise-invalidation); STATUS.md refreshed into a current-direction +
  reconstruction-reading-path surface; historical headers on roadmap.md/goal.md;
  +1 CONTEXT.md source-of-truth row; FO-1..FO-4, CCO-1 recorded; qualified;
  draft PR #269; exact-head CI green.

CLAIMS REVERIFIED:      Part 0 items 1–12 (+ probe-engine behavior, Part 3).

CLAIMS CORRECTED OR NARROWED: N-1 (CI now also green on 358b5a2, was recorded for
  431ec43 only); N-2 (three unfilled SHA placeholders filled: Task A head
  431ec43, handoff head 358b5a2); N-3 (FO-4 probe false-positives persist,
  expected). No consequential fact was wrong.

DEMONSTRATED PRODUCT CAPABILITIES:  Q7.
DEMONSTRATED CAMPAIGN CAPABILITIES: Q8 (CC-1 done; CC-2 = this succession, in
  progress — "demonstrated" only after Task B lands + is validated).

EVIDENCE CEILINGS:      Q9 — EC-1..EC-5, all preserved; EC-5 modestly lifted by a
  real scripts/ machinery change from durable-state-driven selection.

MATERIAL GAPS:          Q15 — MG-1..MG-6 carried; MG-7 human half addressed by
  Task A, machinery half (MG-7m) is Task B's target; MG-8 noted, not targeted.

LAST ASSESSED FRONTIER FROM PRIOR STATE: Q16 — F-a..F-d (Controller A).

INDEPENDENTLY REASSESSED FRONTIER: Q17 — the *mechanically enforced* half of the
  development-direction reconstruction surface: the deterministic drift
  machinery must agree with the human historical markings, or every successor
  re-pays the reconciliation cost and the convention can drift from the code.

PLAUSIBLE ALTERNATIVE BOUNDARIES: Part 2 (≥2 recorded: B-ALT-1 staged-reveal
  minimality probe; B-ALT-2 MG-6 product/campaign boundary write-up;
  B-ALT-3 finish the human surface — CHANGELOG footer / docs sprawl;
  B-ALT-4 Goal A decision packet).

SELECTED BOUNDARY:      Part 4 — Task B: teach the probe engine's live-document
  classifier to honor an explicit in-file historical marker, and apply it to the
  files Task A marked in prose, so the human reconstruction surface and the
  deterministic drift machinery agree on what is historical.

CAMPAIGN WARRANT:       Part 3.

WHY THIS IS REAL PRODUCT ADVANCEMENT: it changes deterministic product machinery
  (`scripts/probe_relationships.py`) consumed by `repo-sensemaker` and the CI
  probe gate, with regression tests; it removes a real contradiction between two
  product surfaces Campaign 2 changed; it makes "which surfaces are current"
  machine-checkable rather than convention-only — the property the central
  question needs ("*survive* independent controller replacement"). It is not
  campaign instrumentation: the classifier and the marker live in the product,
  used by any operator/CI run, campaign or not.

DECISION-CHANGING UNCERTAINTY: Is the probe engine genuinely *not* already
  honoring Task A's historical markings (making the machinery change warranted),
  or does existing machinery already treat roadmap.md/goal.md correctly (making
  this a non-issue)? Sub-uncertainty: is the smallest sufficient fix an explicit
  opt-in marker honored by the classifier, or does it need something larger
  (front-matter schema, path move, name rule)?

BOUNDED TASK:           Part 4 (responsibilities B1–B6).

MINIMALITY CLAIM CURRENTLY SUPPORTED: none beyond "smallest currently supported
  candidate". No comparative minimality evidence is produced this cycle; EC-1
  preserved. Task B's own minimality (marker-honoring classifier vs. larger
  alternatives) is argued from evidence in Part 4, not comparatively tested.
```

---

## Part 2 — Strategic boundary comparison

Frontier question (independent of Controller A's F-list): **what is the
highest-leverage unresolved *product* capability boundary for "repository-level
development direction surviving independent controller replacement," now that
Task A has put a human-facing current-direction surface + reconstruction reading
path on the candidate head?**

### B-ALT-1 — Staged-reveal comparative-minimality probe (EC-1 / F-d)

- **Boundary.** Run a bounded fresh-context reconstruction twice — (i) repo +
  `CHARTER.md` only, (ii) then + `CAMPAIGN-STATE.md` — and record what the
  campaign semantic state *materially adds* vs. what is redundant, producing the
  first comparative-minimality evidence.
- **Plausible?** Yes — the owner instruction explicitly offers this as an
  "Optional Minimality Probe," and EC-1 is the single most-cited ceiling.
- **Evidence for it.** EC-1 / MG-5 / F-d; no comparative evidence exists at all.
- **Warranted now?** **No, not as Task B.** (1) It is *measurement*, not product
  advancement; if both Campaign 2 cycles are probes, the campaign produces zero
  substantive product implementation, straining acceptance condition 10/11
  ("substantive product implementation ... or an equivalently consequential
  result"). (2) The owner instruction: "Do not create an elaborate experimental
  framework merely to prove theoretical minimality"; a credible staged-reveal
  needs a genuinely fresh sub-context and careful contamination control (A1
  already leaked ~30 excluded lines via a broad Grep — FO-3). (3) A confirmatory
  "the surface is sufficient" result does not *change* product direction. EC-1
  is better left explicitly preserved than half-tested. *Recorded as the
  strongest alternative; its findings partly obtained free from this
  checkpoint's own reconstruction experience (Part 3).* 

### B-ALT-2 — Write the MG-6 / EC-4 product-vs-campaign boundary (F-b)

- **Boundary.** Produce the authority-bound conclusion: which parts of Campaign
  1's continuation capability are *product* (belong on a product surface) vs.
  *campaign-only* (experimental control), resolving MG-6 / EC-4.
- **Plausible?** Yes — campaign state calls it "central to the minimality
  question."
- **Evidence for it.** MG-6 open since Campaign 1; the operating map documents
  responsibility-level continuation as a *pattern* ("demonstrated in real use
  inside the campaign directory"), not as operator-facing product guidance.
- **Warranted now?** **Partially — as a by-product, not the task.** Much of the
  answer is already in the operating map §2 subsection ("Durable state that
  proved necessary", failure classes, "Not needed at this scale") and in
  `decision-orchestration-boundary.md`. The incremental product delta is a
  documentation paragraph that risks "documentation that merely restates
  already-known facts" (which the owner instruction says does *not* satisfy the
  substantive bar). I fold the concrete part of this into Task B's cycle result
  (§EC-4 update): the *machinery-consistency of the reconstruction surface* is a
  product concern; the *succession provenance / isolation accounting / boundary
  comparison* is campaign-only.

### B-ALT-3 — Finish the *human* reconstruction surface (CHANGELOG footer, `docs/` sprawl, `00-user-intent.md`)

- **Boundary.** Complete what Task A flagged-but-did-not-edit: the `CHANGELOG.md`
  "Deployment Timeline" footer (a wrong-anchor hazard A1 named); the ~45 loose
  historical `docs/*.md`; `00-user-intent.md`'s stale "production deployment"
  framing.
- **Plausible?** Yes — these are real residual wrong-anchor hazards.
- **Warranted now?** **No, not as the strategic task.** This is
  instance-by-instance cleanup — "do not allow Campaign 2 to degrade into
  repository cleanup." Each item is a *local* defect; none *changes a
  capability*. `00-user-intent.md` is a validated immutable `user_intent`
  artifact (Task A deliberately left it; editing it is fraught). The strategic
  version of this boundary is B-ALT-4/Task B: fix the *class* (surfaces silently
  stay "live" after going historical) mechanically, not the *instances*. (The
  CHANGELOG footer is genuinely tiny and I will note it as a deferred local
  finding, not do it — it is `historical`-classified already, so it is not even
  a machinery problem, only a human-readability one Task A's STATUS.md note
  already covers.)

### B-ALT-4 — Machinery half of the reconstruction surface: an explicit historical marker the deterministic drift classifier honors  *(SELECTED)*

- **Boundary.** `probe_relationships._classify_doc_file` classifies every `.md`
  as `live | historical | generated | fixture | vendor | example | candidate`
  from **path signals only, no content analysis**. Task A declared `roadmap.md`
  and `goal.md` "HISTORICAL / SUPERSEDED" in prose; the classifier cannot see
  that, still classifies them `live`, and the version-drift probe still emits
  their `0.2.1`/"Phase 2.3" claims as `conflicting_values` evidence against the
  declared `0.2.2`. The human reconstruction surface and the machinery a
  successor (and CI, and `repo-sensemaker`) rely on **disagree about what is
  current**.
- **Plausible?** Yes, and directly verified (Part 3): `_classify_doc_file` and a
  live probe run both put `roadmap.md`/`goal.md` in the `live` set with their
  stale version tokens in the finding.
- **Evidence for it.** The probe run at `358b5a2`: `version` finding has 30
  observations incl. `roadmap.md:23` ("**Current Version:** 0.2.1 (Beta)"),
  `:85`, `:89`, `:115`, `:134`, all `source_class: live`. Repeated failure
  class: `roadmap.md`, `goal.md`, `CHANGELOG.md`, `00-user-intent.md` all went
  historical-in-place; the classifier catches only `CHANGELOG.md` (hard-coded
  name rule) — four instances, one covered.
- **Warranted now?** **Yes.** It is (a) the unfinished, mechanically-enforceable
  half of the exact boundary Task A opened; (b) a known material contradiction
  between two product surfaces Campaign 2 changed (acceptance condition 15
  requires it be resolved); (c) a real deterministic-machinery change
  (`scripts/` + regression tests) consumed by CI's probe gate and
  `repo-sensemaker` — substantive, naturally small, not padded; (d) "harden
  only where pressured" with *demonstrated repeated* pressure, so it clears the
  formalization gate without adding a schema / hook / router / state machine /
  new artifact type; (e) still warranted if succession were already solved — the
  machinery-vs-convention gap would still cost every successor.

### SELECTED BOUNDARY — B-ALT-4

**Why it dominates.** B-ALT-1 is measurement and would leave the campaign with
no substantive implementation. B-ALT-2 is largely already-written documentation
(folded in as a cycle-result note). B-ALT-3 is instance cleanup and partly
touches an immutable artifact. B-ALT-4 is the only candidate that is at once
*on the central question*, *substantive product implementation*, *naturally
bounded*, *warranted independent of the succession experiment*, and *a
resolution of a contradiction Campaign 2 itself introduced* — and it converts
Task A's fragile convention into a machine-enforced property, which is what
"*survive* independent controller replacement" actually requires.

**Decision-changing uncertainty.** Is existing machinery genuinely failing to
honor Task A's markings (→ change warranted), or already handling it (→ drop the
task, record "existing mechanism suffices")? And: is an explicit opt-in marker
the smallest sufficient fix, or is something larger needed?

**Bounded task.** Part 4.

---

## Part 3 — Strategic Selection Gate (Task B)

```
PRODUCT CAPABILITY AFFECTED:
  Repository-level development-direction reconstruction — specifically its
  machine-checkable half: the ability of an independent controller (or CI, or
  repo-sensemaker) to trust that the deterministic drift machinery's list of
  "live current-state documents" matches the repository's actual, human-declared
  set of current surfaces — so that a superseded document is not re-surfaced as
  a conflicting current-state claim that each successor must re-triage.

CURRENT LIMITATION:
  probe_relationships._classify_doc_file uses deterministic PATH signals only
  ("no content analysis"). It recognizes historical *paths* (archive/, releases/,
  research/, experiments/, ...), historical *name prefixes* (phase-N, weekN,
  dated), and exactly two historical *names* (changelog, handoff). A root-level
  document that becomes historical *in place* — roadmap.md, goal.md,
  00-user-intent.md — has no way to declare itself historical to the machinery.
  Task A added prose "HISTORICAL / SUPERSEDED" headers to roadmap.md and goal.md;
  the classifier still returns "live" for both, and the version-drift probe still
  emits their superseded 0.2.1 / "Phase 2.3" claims as conflicting_values
  evidence against the declared 0.2.2.

EVIDENCE THE LIMITATION EXISTS (verified at 358b5a2, RUN):
  - `_classify_doc_file("roadmap.md")` -> "live"; `_classify_doc_file("goal.md")`
    -> "live"; both appear in `_discover_docs(".")`'s live set.
  - probe-repo.py at HEAD: relationships.version.findings[0].observations
    includes roadmap.md:23 "**Current Version:** 0.2.1 (Beta)", roadmap.md:85,
    :89, :115, :134 — each `source_class: live`.
  - roadmap.md / goal.md (campaign head) both carry a blockquote
    "HISTORICAL / SUPERSEDED (as of 2026-09-02)" header the classifier ignores.
  - Repeated failure class: roadmap.md, goal.md, CHANGELOG.md, 00-user-intent.md
    all went historical-in-place; only CHANGELOG.md is caught (hard-coded name).
  - A1 (Task A) independently found these files a wrong-anchor hazard and the
    reconstruction cost "excessive"; Campaign 1 logged roadmap.md as "no action".

INTENDED PRODUCT USER OR OPERATOR:
  A fresh coding-agent controller (or human maintainer) reconstructing
  repository-level development direction without prior context — the same actor
  Campaign 2 is about — plus the CI probe gate and `repo-sensemaker`, both of
  which consume probe-report.yaml.

USER- OR OPERATOR-OBSERVABLE VALUE:
  Running the probe engine on a repo whose maintainers have marked a document
  historical no longer produces "these sources disagree about the current
  version" evidence pointing at that document; the machine-readable
  live-document set matches the human-declared one; a successor does not
  re-triage roadmap.md/goal.md every reconstruction.

WHY IT MATERIALLY CONSTRAINS THE CAMPAIGN MISSION:
  The central question is whether development direction *survives* independent
  controller replacement. Task A's fix is a convention (prose headers + a
  reading path). A convention that the repository's own deterministic machinery
  contradicts is fragile: the next controller sees the probe flag roadmap.md,
  must open it, must reconcile the flag against the prose header, and the header
  itself can drift out of sync with the machinery on any future edit. Making the
  classifier honor an explicit marker turns "which docs are current" from a
  convention into a mechanically enforced, CI-visible property.

WHAT PRODUCT CAPABILITY BECOMES STRONGER IF SOLVED:
  "Repository-level development direction survives independent controller
  replacement" — its machine-checkable half. Also: the probe engine's
  version/ADR drift evidence becomes lower-noise and more trustworthy (fewer
  false "current-state conflict" observations from documents everyone agrees are
  historical).

WHY THIS IS PRODUCT ADVANCEMENT RATHER THAN CAMPAIGN INSTRUMENTATION:
  The change is in `scripts/probe_relationships.py` — deterministic product
  machinery consumed by CI (`gate_relationship_findings.py`) and
  `repo-sensemaker`. The marker convention lives in the product's own documents.
  Nothing in `docs/campaigns/` is involved except recording the result. Any
  repository using the probe engine benefits; it is unrelated to the succession
  experiment.

WHY THIS TASK WOULD REMAIN WARRANTED IF THE SUCCESSION ACCEPTANCE CONDITION
WERE ALREADY SATISFIED:
  Even with perfect controller succession, a probe engine that disagrees with the
  repository's declared historical set produces noisy drift evidence and forces
  re-triage of superseded documents on every run — a standing cost independent
  of how clean the handoff mechanism is.

WHY THIS IS A STRATEGIC DEVELOPMENT TASK RATHER THAN MERELY A NEARBY DEFECT:
  The nearby-defect framing is "roadmap.md is still flagged by the probe — add it
  to a skip list." The strategic framing is: the deterministic machinery has no
  general affordance for a document to declare itself historical-in-place, so the
  same contradiction recurs for every future superseded root document; the fix is
  a small, general, opt-in marker the classifier honors — addressing the class,
  not the instance — and it closes the acceptance-15 contradiction between two
  surfaces Campaign 2 changed. The output is a machinery capability, not a
  one-file patch.

DECISION-CHANGING UNCERTAINTY:
  (a) Does existing machinery already honor Task A's historical markings for
      roadmap.md/goal.md? [Checked: NO — Part 3 evidence.]
  (b) Is the smallest sufficient fix an explicit opt-in in-file marker honored by
      `_classify_doc_file`, or is something larger required (a doc-lifecycle
      front-matter schema; a path move to docs/archive/; a filename rule)?
      [Argued in Part 4: the marker is smallest and general; larger options are
      a schema the owner instruction warns against, or link-breaking churn.]

BOUNDED TASK:
  Part 4 (B1–B6).

EXPECTED EVIDENCE THAT WOULD CHANGE THE CAPABILITY ASSESSMENT:
  - If a probe run showed roadmap.md/goal.md already classified historical (e.g.
    an unnoticed name/path rule), Task B collapses to "existing mechanism
    suffices" + a one-line campaign-state note. [Ruled out — verified live.]
  - If honoring an in-file marker required touching more than the classifier +
    its discovery caller + tests + the two marked files, the "smallest coherent
    change" claim weakens and the task is re-scoped or split.
  - If adding the marker to roadmap.md/goal.md broke any validator or an existing
    test as a *referee* (not a fixture expectation), stop and reassess — do not
    weaken the referee.
```

---

## Part 4 — Task B definition (bounded responsibilities)

**Task B: give the probe engine's live-document classifier an explicit,
deterministic way for a document to declare itself historical-in-place, and
apply it to the documents Task A marked in prose — so the human
development-direction reconstruction surface and the deterministic drift
machinery agree on which documents are current.**

Task B reaches its **legitimate boundary** when: decision-changing uncertainty
(a)/(b) is resolved with evidence (a is already resolved: the machinery does
*not* honor the markings); the smallest coherent machinery change is implemented
(or shown unnecessary / shown to need a fresh warrant); regression coverage is
added; and qualification has run.

### Bounded responsibilities

- **B1 — Confirm the gap and fix the smallest surface.** Verified (Part 3): the
  classifier returns `live` for `roadmap.md`/`goal.md`. Implement in
  `scripts/probe_relationships.py`: an explicit in-file marker
  (`<!-- doc-status: historical -->`, case-insensitive; accept the synonyms
  `superseded` / `archived`), a bounded helper that reads only the file head to
  detect it, and an optional `declared_status` parameter to `_classify_doc_file`
  that, when set, takes precedence over the path heuristics. `_discover_docs`
  computes the marker per file and passes it. Update the two docstrings
  ("deterministic path signals, plus an explicit in-file `doc-status` marker").
  No change to any *finding* logic, any gate, any blocking behavior, or any
  other classifier branch.

- **B2 — Apply the marker.** Add the one-line marker to `roadmap.md` and
  `goal.md` (immediately after the H1, before Task A's blockquote header — the
  blockquote prose stays; the marker just makes its first assertion
  machine-readable). Do **not** touch `00-user-intent.md` (validated immutable
  `user_intent` artifact — Task A's caution stands; record as deferred).
  `CHANGELOG.md` already classifies `historical`; no change.

- **B3 — Regression coverage** in `tests/test_probe_relationships.py`:
  (i) extend `test_classify_doc_file` with `declared_status` precedence cases
  (pure, no I/O); (ii) a `tmp_path` test that a doc at a `live` path with the
  marker is discovered `historical`, is absent from `_live_sources`, and is
  counted under `by_class["historical"]`; (iii) a `tmp_path` version-drift test
  that a marker'd doc's version token does **not** enter the `conflicting_values`
  decision set; (iv) a negative test that the marker only counts near the file
  head / as a real HTML comment, not any mention of the string mid-body.

- **B4 — Validate** (strongest available referees):
  `python scripts/validate-repo.py` (exit 0);
  `python scripts/probe-repo.py` + `scripts/validate-probe-report.py` +
  `scripts/gate_relationship_findings.py` (gate PASS; confirm roadmap.md/goal.md
  observations have dropped from the `version` finding and no new blocking
  finding appeared); `python scripts/test-validators.py` (78/78);
  `PYTHONPATH=src python -m pytest tests/test_probe_relationships.py
  tests/test_repo_probes.py tests/test_gate_relationship_findings.py
  tests/test_probe_report_cli.py tests/test_probe_relationships.py` and the
  core-assertions set (green); inspect the full diff; confirm the tree is
  otherwise clean. Push; observe exact-head CI on PR #269.

- **B5 — Update campaign semantic state** (`CAMPAIGN-STATE.md` -> v5): record
  Task B, the boundary, the ≥2 alternatives, capability advanced, evidence,
  ceilings (EC-1 preserved; EC-5 modestly lifted), MG-7m resolution, the N-1/N-2
  corrections, the acceptance-15 contradiction closed, failure observations if
  any, hypothesis assessment (H2/H6/formalization-rule), and Controller B's
  post-Task-B frontier assessment (as LAST ASSESSED CANDIDATE, not a command).

- **B6 — Reassess from the mission and write `controllers/B-cycle-result.md`**:
  Task B execution + validation; which capability changed; remaining ceilings;
  whether Controller A's frontier hypotheses survived; which campaign
  architecture hypotheses strengthened / weakened / failed; and — per the
  closure rule — whether any remaining material gap is *necessary* to answer the
  Campaign 2 central question, i.e. whether Campaign 2 is at
  `CAMPAIGN_COMPLETE`, needs a Controller C, or another disposition.

### Not authorized in Task B

Merging; ADR / contract / canonical-vocabulary / registry / liveness-overlay /
`src/` edits; the nine workflow-system-disposition decisions; editing
`00-user-intent.md`; external tracker writes; a new artifact type / schema /
Skill / workflow / hook / router / state machine; inferring owner preference.
Any of these that becomes warranted -> `OWNER_DECISION_REQUIRED` in
`CAMPAIGN-STATE.md`.

### Stop condition

Decision-changing uncertainty resolved with durable evidence; the smallest
coherent machinery change implemented (or ruled unnecessary / shown to need a
fresh campaign warrant); regression coverage added; qualification run;
`CAMPAIGN-STATE.md` updated to v5; `controllers/B-cycle-result.md` committed.
Campaign 2 closure assessed in B6 — do not extend Task B into further cleanup or
a third strategic task.
```
