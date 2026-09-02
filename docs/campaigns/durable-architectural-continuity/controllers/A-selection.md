# Controller A — Phase 1 reconstruction + capability selection

```
CONTROLLER:  A (lead Campaign 3 controller; the context that received the owner
             instruction and ran Phase 0). Model claude-sonnet-5 (Claude Code
             harness).
DATE:        2026-09-02
CHECKPOINT:  this file, committed once as temporal evidence. Not rewritten if
             later evidence changes the campaign conclusion (later CAMPAIGN-STATE
             versions supersede its conclusions; this file stays as written).
PHASE:       1 (Select the Product Capability First). No product surface has been
             touched. No coupled capability has been selected.
SOURCES:     OWNER-INSTRUCTION.md; CHARTER.md; STARTUP-PROVENANCE.md; and, at
             origin/main @ 969e8eb: CONTEXT.md, STATUS.md, roadmap.md, goal.md,
             CHANGELOG.md, docs/agent-native-operating-workflow.md,
             docs/decision-orchestration-boundary.md,
             docs/research/control-model-research-agenda.md,
             docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md,
             docs/workflow-system-disposition.md section 6,
             docs/campaigns/agent-native-self-development/FINAL-REPORT.md,
             docs/campaigns/durable-repo-self-development/{CAMPAIGN-STATE,FINAL-REPORT,OWNER-INSTRUCTION}.md,
             docs/adr/ status lines, gh issue/pr list, src/ + scripts/ layout.
```

---

## PART 0 — State planes (re-recorded before selection)

```
CURRENT ORIGIN/MAIN:            969e8eb47144ffdeb27a8d9df02b6a292586e842
                               (Merge PR #270, Campaign 2 closure stamp)
CAMPAIGN BASE:                  969e8eb
CAMPAIGN HEAD:                  b677ffb (bootstrap) -> this checkpoint commit
MAIN DRIFT SINCE CAMPAIGN START: none (git log 969e8eb..origin/main empty, 2026-09-02)
CANDIDATE CHANGES NOT ON MAIN:  only docs/campaigns/durable-architectural-continuity/
                               (campaign instrumentation). No product surface.
INTEGRATION STATUS:            nothing merged; no PR opened.
WHICH CLAIMS APPLY TO MAIN:    the entire product-state reconstruction in Part 1
                               (Campaign 1 = PR #268 merged 06a57d1; Campaign 2 =
                               PR #269 merged 7e48cf0 + closure stamp PR #270).
WHICH CLAIMS APPLY ONLY TO CAMPAIGN HEAD: none.
OWNER / RATIFICATION STATUS:   no Campaign 3 owner decision pending.
```

## PART 1 — Current product-state reconstruction (Controller A)

`REPOSITORY-VERIFIED` + `GITHUB-VERIFIED`; consequential claims reverified from
repo / `gh` at `969e8eb` on 2026-09-02.

### 1.1 Product definition and ratified scope

- **Product** (`CONTEXT.md`): "an agent-native engineering sensemaking and
  control layer for software-engineering agents." The active coding agent owns
  the recursive control loop (**ADR 0013**, Accepted). Sensemaking constrains
  that loop with repository evidence, bounded responsibilities, durable
  artifacts, validators, reconciliation, repair verification, authority
  boundaries.
- **Ratified external product scope** = the validated, human-reviewed
  `repository_sensemaking_brief` (**ADR 0014**, Accepted, "revised, narrowed").
  Automatic fog-type -> implementation routing is **explicitly not ratified**
  (ADR 0014 defers it; **ADR 0018** — deterministic fog-type routing table — is
  SUPERSEDED, never Accepted). ADRs 0013/0014/0015-addendum/0016/0023/0024/0025/
  0026/0027 are the accepted decision set; 0017–0021 are SUPERSEDED / never
  Accepted; 0006/0007/0008/0022 are Proposed (0022 "awaiting independent
  adversarial review").
- **Control model** is documented, not encoded: `agent-native-operating-workflow.md`
  (v0 map, "NOT a canonical orchestration specification") +
  `decision-orchestration-boundary.md` ("this document does not introduce a new
  runtime, registered workflow, Skill, routing table, or automation contract").
  The operating map's Reality Map classifies almost every responsibility as
  `REAL` (diagnosis, validation, reconciliation, repair verification) or
  `CONVENTION / partially formalized / not warranted` with an explicit **reopen
  condition** per row. The product architecture is deliberately *waiting for a
  demonstrated failure* before adding machinery.

### 1.2 Integrated campaign results (both on `main`)

- **Campaign 1** (PR #268, merge `06a57d1`; `agent-native-self-development`):
  documented responsibility-level artifact-mediated continuation pattern;
  deterministic-machinery + hooks disposition in
  `decision-orchestration-boundary.md`; `docs/workflow-system-disposition.md`
  (23 workflows classified); lazy `workflow_liveness` resolver in
  `scripts/_validator_utils.py` + tests. **No ADR / contract / registry / `src/`
  change.** Disposition `CAMPAIGN_COMPLETE`; closed with "**no further product
  change is warranted by current evidence**."
- **Campaign 2** (PR #269, merge `7e48cf0`; closure stamp PR #270, `969e8eb`;
  `durable-repo-self-development`): Task A — `STATUS.md` refreshed into a
  current-direction + reconstruction-reading-path surface; `roadmap.md` /
  `goal.md` historical/superseded headers + `<!-- doc-status: historical -->`
  markers; `CONTEXT.md` +1 source-of-truth-map row. Task B —
  `scripts/probe_relationships.py` live-document classifier honours the opt-in
  `doc-status` marker (`_declared_doc_status` + `_classify_doc_file(...,
  declared_status)` + `_discover_docs` wiring) + 4 regression tests. **No ADR /
  contract / canonical-vocabulary / registry / `src/` change.** Disposition
  `CAMPAIGN_COMPLETE`. **Owner decision: the `doc-status` marker is
  NON-NORMATIVE** — a probe heuristic, not a ratified convention; nothing beyond
  `roadmap.md` / `goal.md` should emit it unless the owner later blesses it.

### 1.3 Current development posture (multiply corroborated)

Four independent durable statements converge:

1. `CONTEXT.md` principle 10 — "**Harden only where pressured** — formalize new
   machinery when repeated real use exposes a stable, mechanically expressible
   failure boundary." Restated as the machinery-promotion rule in
   `agent-native-operating-workflow.md` §7 and the research-discipline rule in
   `control-model-research-agenda.md`.
2. Campaign 1 closure — "no further product change is warranted by current
   evidence."
3. `control-model-research-agenda.md` **meta-finding 2026-08-30** — "Further
   sensemaking loops saturated; next evidence requires constructive spikes, not
   briefs. ... Future agents should not re-run sensemaking diagnosis to test this
   claim."
4. `STATUS.md` "Highest-leverage warranted next boundary" — the in-authority
   engineering backlog is "**deliberately small**"; the repository posture is
   "**harden only where pressured**."

### 1.4 The genuine product frontier

`STATUS.md` + `docs/research/goal-a-external-product-validation-protocol.md` +
`docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md` +
`experiments/evidence/0023-goal-a-run1-stop-boundary/` + Issue #255:

- The product's **central unvalidated hypothesis** is *brief usefulness beyond
  this repository*. The workstream that would validate it is **Goal A — External
  Product Validation** (`A1 = ACTIVE`, absolute product utility).
- The first A1 episode is **paused at an execution-substrate boundary**. Run 1
  triggered stop rule `HARNESS_ENVIRONMENT_FAILURE`: the producer sub-agent
  could not persist its own frozen brief (host write-dispatch blocked the
  target); provenance crossed an un-pinned local object store; the sub-agent had
  no write access to re-run the probe engine.
- The reassessment states plainly: "**Fixing these is substrate work, distinct
  from the product question A1 asks**"; resuming "needs an **owner/environment
  decision, not a repo-code change**"; and any run "requires a **separate, fresh
  owner authorization**." Tracked as owner-reserved in Issue #255.

### 1.5 Open work inventory

- **Open issues** (`gh issue list --state open`): #218 (normal-use
  control-model evidence lane — research-ops), #226 (C6R gate-separation study —
  frozen; "do not modify C6R before its preregistered result"), #255 (Goal A
  substrate — owner/environment decision). **All three research / owner-reserved.
  None is in-authority product engineering.**
- **Open PRs**: only #194 (draft, `experiment/exp-0003-results`, "do not merge").
- **`docs/workflow-system-disposition.md` §6**: nine "implied owner decisions,
  not applied" — retire two external-routing sprint identities; disposition of
  28 deprecated PM-ecosystem registry entries; a deprecated `if_true` branch in
  `full-local-sensemaking`; a missing `setup-sensemaking-skills` registry entry
  (currently name-exempted in `validate-repo.py`); `autonomous-sprint-preflight`
  purpose; two `docs/mode-coverage.yaml` `steps_completed` claims; the
  `artifact-reconciliation` registered sequence; an
  `architectural-review-planning-workflow` description question; packaged-catalog
  vs overlay divergence. Each is a **registry / overlay / contract /
  documentation micro-decision explicitly outside R6 authority** (ADR 0027 makes
  the overlay owner-ratified). **All owner-reserved.**
- **Engineering debt** (Campaign 1/2 records): D2b (`test_validate_brief_json`
  fixture drift), D19, two platform reds, stale committed
  `src/sensemaking_skills.egg-info` version. Pre-existing, deferred, **none in
  CI, none capability-level**.
- **Doc-surface residuals** (Campaign 2 §14): DB-1 (`CHANGELOG.md` footer —
  already `historical`-class, human-readability only), DB-2 (`integration-report.md`
  / `integration-design.md` / `adoption-finalization.md` still `live` to the
  probe — the `doc-status` marker could fix them but Campaign 2 classed this
  "**instance cleanup, not a capability**" and the owner left the marker
  NON-NORMATIVE), DB-3 (`docs/campaigns/**` quoted-evidence noise — a judgment
  call), MG-8 (`STATUS.md` has no mechanical staleness signal — "**premature;
  needs a demonstrated recurrence**").
- **`unevaluable` verdict category** for `repair_verification_report`: a "v0
  note ... proposed but not yet encoded" in `agent-native-operating-workflow.md`;
  6 total mentions repo-wide, all notes; UNRATIFIED; **no accumulated real-use
  pressure**.
- **`src/` / `scripts/` unfinished primitives**: a scan for
  `TODO`/`FIXME`/`NotImplemented`/placeholder markers in product code returns
  ~zero genuine hits (the matches are all *placeholder-detection logic* — code
  that detects placeholders in artifacts). The codebase is deliberately complete
  per its current thesis (`campaign_accounting/`, `campaign_validation/`,
  `exploratory_authorization/`, `exploratory_execution/`, `reasoning/`, the
  skill implementations — all present and exercised).

### 1.6 Fresh Controller B instantiation (carried from Phase 0)

Available at the same honest ceiling Campaign 2 used: `Agent` tool,
`subagent_type: general-purpose`, cold context — `HARNESS_REPORTED` context
isolation; `SUCCESSION_ISOLATION_UNVERIFIED` for predecessor-process
non-persistence and model independence (same `claude-sonnet-5` family). Not an
`EXTERNAL_BLOCKER` on that dimension (`STARTUP-PROVENANCE.md` §8).

## PART 2 — Candidate capability boundary survey

Serious candidates considered, each against the Phase 1 grid. None is
manufactured to fill the format; these are the only plausible boundaries the
evidence surfaces.

### C-1 — Goal A execution substrate repair (producer artifact-finalization + verified provenance/hermeticity)

```
CAPABILITY:            an isolated producer sub-agent in a Goal A / A1 episode
                       can persist its own frozen brief to the runtime
                       expected_output_path and prove pinned, cross-context
                       provenance, so a compliant Run 1 is admissible.
CURRENT LIMITATION:    Run 1 hit HARNESS_ENVIRONMENT_FAILURE (write-dispatch
                       blocked; provenance via un-pinned object store; no probe
                       write access). Evidence 0023; Issue #255.
EVIDENCE THE LIMITATION EXISTS: strong — a byte-verified committed stop-boundary
                       record + a live tracking issue + a dedicated readiness
                       reassessment.
INTENDED USER/OPERATOR: the Goal A episode harness / the owner running external
                       product validation.
PRODUCT CONSEQUENCE IF SOLVED: unblocks the product's central unvalidated
                       hypothesis (brief usefulness beyond this repo).
WHY IT MATTERS NOW:    it is the single highest-leverage product-validation
                       workstream (STATUS.md, the reassessment).
AUTHORITY REQUIRED:    (a) engineering authority to change episode-harness code;
                       (b) owner/environment decision to resume Goal A;
                       (c) a separate fresh owner authorization to run an
                       episode.
AUTHORITY AVAILABLE:   only (a), partially. The reassessment + STATUS.md state
                       the blocker is "not product-surface", HARNESS_ENVIRONMENT
                       class, and "needs an owner/environment decision, not a
                       repo-code change". (b) and (c) are OWNER_DECISION_REQUIRED
                       and are the tracked disposition of Issue #255.
DECISION-CHANGING UNCERTAINTY: is any part of the blocker a repo-code defect an
                       autonomous agent may fix on a branch, or is it wholly an
                       environment/authorization matter? The durable evidence
                       says the latter is the operative framing and the owner
                       has reserved it.
```

**Not selected.** The blocker is explicitly classified non-product-surface and
`HARNESS_ENVIRONMENT_FAILURE`; resuming is owner/environment-reserved (Issue
#255); an episode needs fresh owner authorization. Building a Campaign 3 coupled
implementation on a speculative harness repair to an owner-reserved,
environment-blocked workstream is the exact `NEED COUPLED EXPERIMENT -> SEARCH
FOR A TASK` anti-pattern the owner instruction forbids in bold.

### C-2 — Nine `workflow-system-disposition.md` §6 registry/overlay/contract decisions

```
CAPABILITY:            a coherent, non-divergent registered-workflow catalog +
                       liveness overlay + packaged copy.
CURRENT LIMITATION:    nine small inconsistencies / undocumented exemptions /
                       stale claims, each enumerated with evidence.
EVIDENCE:              strong and specific (the §6 list cites exact file:line).
INTENDED USER/OPERATOR: workflow-planner / runtime / validators / a maintainer.
PRODUCT CONSEQUENCE IF SOLVED: marginally cleaner catalog; no capability change.
WHY IT MATTERS NOW:    it does not, particularly — "harden only where pressured";
                       no consumer is currently broken by any of the nine.
AUTHORITY REQUIRED:    owner (ADR 0027 makes the overlay owner-ratified; each
                       item is "outside R6 authority").
AUTHORITY AVAILABLE:   none — OWNER_DECISION_REQUIRED (STARTUP-PROVENANCE.md §7;
                       Campaign 2 CHARTER OWNER-RESERVED list; the §6 preamble).
DECISION-CHANGING UNCERTAINTY: none that changes the answer.
```

**Not selected.** Owner-reserved; each item is a bounded local registry/doc edit,
not a capability; none is semantically coupled; and none currently pressures a
consumer.

### C-3 — Extend the `doc-status` marker to other historical-in-place root docs (DB-2)

```
CAPABILITY:            the probe engine's live-document set matches the
                       human-declared one for ALL historical-in-place root docs,
                       not just roadmap.md / goal.md.
CURRENT LIMITATION:    integration-report.md / integration-design.md /
                       adoption-finalization.md still classify `live` and
                       contribute stale version snippets to the probe `version`
                       finding.
EVIDENCE:              Campaign 2 DB-2 (recorded, not selected there).
INTENDED USER/OPERATOR: repo-sensemaker / CI / a maintainer.
PRODUCT CONSEQUENCE IF SOLVED: fewer non-blocking probe evidence lines; no
                       capability change (the marker mechanism already exists).
WHY IT MATTERS NOW:    weakly — the findings are non-blocking; Campaign 2 called
                       this "instance cleanup, not a capability".
AUTHORITY REQUIRED:    engineering authority + care around the owner's decision
                       that the marker is NON-NORMATIVE.
AUTHORITY AVAILABLE:   engineering authority yes; but applying the marker more
                       widely edges toward treating a NON-NORMATIVE heuristic as
                       a convention, which the owner explicitly declined.
DECISION-CHANGING UNCERTAINTY: none — this is a 3-line instance edit.
```

**Not selected.** Instance cleanup, not a capability; single-surface (add a
marker line to three files; the classifier already honours it); explicitly not
warranted by Campaign 2; and it brushes against the owner's NON-NORMATIVE
decision. Zero semantic coupling.

### C-4 — `unevaluable` verdict category for `repair_verification_report`

```
CAPABILITY:            repair-verifier can report "the finding could not be
                       re-observed" distinctly from "the finding is closed" or
                       "remaining".
CURRENT LIMITATION:    a failed/errored probe observation is not an observed
                       absence, but the report contract has no `unevaluable`
                       verdict; the operating map flags this as a "v0 note".
EVIDENCE:              weak — 6 doc mentions repo-wide, all notes; UNRATIFIED;
                       no real-use episode records a wrong closure caused by the
                       missing category.
INTENDED USER/OPERATOR: repair-verifier consumers / handoff.
PRODUCT CONSEQUENCE IF SOLVED: a more honest verdict vocabulary.
WHY IT MATTERS NOW:    no demonstrated pressure — the machinery-promotion gate
                       ("repeated real use exposes a stable failure boundary")
                       is NOT met.
AUTHORITY REQUIRED:    engineering authority (contract + validator + skill +
                       tests + docs) — arguably an artifact-contract change,
                       which edges toward owner ratification territory.
AUTHORITY AVAILABLE:   partial.
DECISION-CHANGING UNCERTAINTY: is there ANY accumulated real-use evidence that
                       the missing category caused a wrong repair-closure? Search
                       found none.
```

**Not selected.** This is the closest thing to a *coupled* candidate (it would
touch the probe/verifier producer, the `repair_verification_report` contract,
the validator, tests, and docs, bound by the invariant "a non-observation is not
a closure"). But it **fails the product-warrant test**: the machinery-promotion
gate is explicitly unmet (no repeated real-use pressure; `CONTEXT.md` principle
10), the research-agenda meta-finding says "loops saturated ... constructive
spikes, not briefs", and adding an artifact-contract verdict on a "v0 note" with
no failure evidence is precisely the premature formalization the owner
instruction and `CONTEXT.md` principle 10 forbid. Selecting it would be choosing
"the more architecturally interesting" option over honest product priority —
also forbidden.

### C-5 — MG-8: a mechanical staleness signal for `STATUS.md`

**Not selected.** Campaign 2 assessed this as "premature; needs a demonstrated
recurrence" (formalization rule). No recurrence has occurred (Campaign 2 refreshed
`STATUS.md` days ago; it is current). Single new validator/probe, speculative.

### C-8 — MODEL_WARRANT `FULL` materialization (surfaced by the independent probe)

```
CAPABILITY:            the warrant gate can materialize a FULL representation
                       when `representation_sufficiency` warrants it, instead of
                       only NO / PARTIAL / INCONCLUSIVE.
CURRENT LIMITATION:    src/sensemaking_skills/reasoning/warrant_gate.py:146-148 —
                       the FULL branch is "Not implemented in this bounded slice
                       (deferred). Record intent; do not fabricate a full
                       representation."
EVIDENCE THE LIMITATION EXISTS: strong and explicit (the code comment + ADR).
INTENDED USER/OPERATOR: repo-sensemaker / the MODEL_WARRANT consumer chain.
PRODUCT CONSEQUENCE IF SOLVED: a fuller representation path for the highest
                       evidence-sufficiency tier.
WHY IT MATTERS NOW:    it does NOT — see authority + uncertainty below.
AUTHORITY REQUIRED:    this contradicts ratified product authority. ADR 0015
                       (ACCEPTED, with ratified addendum) line 182: "**FULL
                       remains deferred and is never inferred.**" The campaign
                       "does not have authority to silently contradict" a
                       ratified ADR (CHARTER constraint 5 / authority-basis
                       RATIFIED_PRODUCT_AUTHORITY).
AUTHORITY AVAILABLE:   none for this — OWNER_DECISION_REQUIRED to reopen the ADR
                       deferral.
DECISION-CHANGING UNCERTAINTY: is there real-use pressure to reopen the FULL
                       deferral? None found (the independent probe: "zero
                       evidence pressure"; research-agenda meta-finding: "loops
                       saturated"). CONTEXT.md principle 10 gate unmet.
```

**Not selected.** This is the **only genuinely coupled candidate in the
codebase** — materializing `FULL` would obligate warrant semantics, the
`representation_sufficiency` contract, the producer map, the runtime seam, the
validator, tests, and docs to agree on one invariant. But it is **deferred by a
ratified ADR** (`RATIFIED_PRODUCT_AUTHORITY` = defer), has **zero real-use
pressure** (principle-10 gate unmet), and selecting it would be building against
an intentional deferral to manufacture a coupled experiment — forbidden twice
over by the owner instruction. Reopening the deferral is `OWNER_DECISION_REQUIRED`.

### C-6 — C1/C2 formative-critique / independent-review research direction (renumbered; was listed before C-8 was added)

**Not selected.** `control-model-research-agenda.md` marks this "candidate /
inactive", "no execution program is authorized", activation gated on recurring
real-use pressure that has not been recorded. Research, not in-authority product
engineering.

### C-7 — Engineering debt (D2b / D19 / platform reds / stale egg-info)

**Not selected.** Pre-existing, deferred, none in CI, none capability-level
(Campaign 1/2 records). A fixture-drift repair is a bounded single-surface edit,
not a capability, and carries no campaign warrant.

## PART 3 — Highest-leverage frontier selection

The genuine highest-leverage product boundary is **C-1 (Goal A external product
validation)** — it is the only workstream that advances the product's central
unvalidated hypothesis. It is **owner-reserved and paused at a substrate
boundary explicitly classified non-product-surface / `HARNESS_ENVIRONMENT_FAILURE`
/ "needs an owner/environment decision, not a repo-code change."**

Every other candidate (C-2..C-8) is one of: owner-reserved micro-decisions;
instance cleanup explicitly deemed "not a capability"; premature formalization
the repository's own promotion gate rejects; pre-existing non-capability
engineering debt; inactive research; or (C-8) a genuinely coupled capability
**deferred by a ratified ADR** with no pressure to reopen it. None is
material-leverage, in-authority, product-capability development that is
warranted now.

## PART 4 — Coupling assessment

The owner instruction's order of operations is: select the product frontier
first, *then* assess coupling. Applied here:

- The selected frontier (C-1, Goal A) is **not in campaign authority** to
  develop as a product capability, so there is no in-authority implementation to
  assess for coupling.
- **Two** candidates touch multiple surfaces bound by a shared invariant:
  - **C-8 (MODEL_WARRANT `FULL`)** — genuinely coupled (warrant semantics ->
    `representation_sufficiency` contract -> producer map -> runtime seam ->
    validator -> tests -> docs, one invariant). **Deferred by ratified ADR 0015
    (Accepted)**; zero real-use pressure; reopening is `OWNER_DECISION_REQUIRED`.
    Fails the product-warrant test and the authority test.
  - **C-4 (`unevaluable` verdict)** — mildly coupled (probe/verifier producer ->
    `repair_verification_report` contract -> validator -> tests -> docs).
    Machinery-promotion gate explicitly unmet ("v0 note", no failure evidence).
    Fails the product-warrant test.
- No remaining candidate has a cross-surface semantic invariant. C-2 / C-3 /
  C-5 / C-6 / C-7 are single-surface local edits or inactive research by
  construction.

Therefore there is **no currently-warranted, in-authority product capability
whose smallest coherent implementation is genuinely semantically coupled across
multiple product surfaces** — the two coupled candidates that exist (C-8, C-4)
are deferred by ratified authority / fail the promotion gate — and none can be
selected "without distorting real product priority" (the exact condition the
owner instruction attaches to the `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED`
outcome).

## PART 5 — Independent fresh-context corroboration

A fresh `general-purpose` sub-agent context (Claude Code `Agent` tool; no
Campaign 3 mission text, no access to this checkpoint, scoped away from
`docs/campaigns/durable-architectural-continuity/` — it confirmed it read
nothing there) independently reconstructed the current product-development
frontier from durable repository + GitHub evidence and answered whether a
warranted, in-authority, semantically-coupled product-capability development
currently exists. ~24 tool calls, ~15 turns.

**Independent verdict: `NO_MATERIAL_IN_AUTHORITY_PRODUCT_CAPABILITY_WORK_CURRENTLY_WARRANTED`.**

Convergence with Parts 1–4:

- **Same posture reconstruction** — "harden-only-where-pressured / do not
  build"; the three concurring closure records (Campaign 1 "no further product
  change warranted"; Campaign 2 BF-1 "no further product capability is
  warranted"; research-agenda "loops saturated"); Goal A as the genuine frontier,
  paused at a substrate boundary, owner-reserved, "not a repo-code deliverable"
  (Issue #255).
- **Same open-work inventory** — the three research/owner-reserved issues; PR
  #194 "do not merge"; the nine §6 decisions as "owner-reserved …
  retirement/bookkeeping, not capability development"; D2b / D19 / hygiene items
  as "trivial, single-file each"; the `egg-info` version; FO-4 probe
  false-positive as "non-blocking, single script + tests".
- **One candidate this checkpoint did not surface, added as C-8**: MODEL_WARRANT
  `FULL` materialization (`reasoning/warrant_gate.py:146`). The probe's judgment:
  it "*would* be genuinely multi-surface … but explicitly deferred by the
  ratified ADR 0015 addendum with zero evidence pressure; building it is
  gold-plating against an intentional deferral." Controller A reverified:
  `warrant_gate.py:146-148` = "Not implemented in this bounded slice
  (deferred)"; `docs/adr/0015-…:182` = "FULL remains deferred and is never
  inferred" (ADR 0015 is ACCEPTED). This **strengthens** the disposition — the
  one genuinely coupled capability in the codebase is one the repository has
  deliberately deferred by ratified authority.

**No material divergence.** Two independent contexts — one with the full
Campaign 3 mission, one cold — reached the same conclusion by the same evidence.
The probe's stated limitations (did not re-run pytest / validators; read ADR
status lines not full bodies; did not open PR #194) do not affect the
disposition; Controller A's Phase 0 reads cover the same ground and reverified
the one consequential new claim (C-8).

## PART 6 — Phase 1 disposition

```
PHASE 1 OUTCOME:  NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED
```

**Rationale.** The repository is in a deliberate, multiply-corroborated "harden
only where pressured / sensemaking loops saturated / no further product change
warranted" posture. Its single highest-leverage product boundary (Goal A
external product validation) is owner-reserved and paused at a substrate
boundary its own durable evidence classifies as non-product-surface and
requiring an owner/environment decision. Every in-authority item is an
owner-reserved micro-decision, pre-existing non-capability engineering debt, or
instance cleanup explicitly deemed premature or "not a capability." There is no
currently-warranted, in-authority product capability of material leverage — and,
a fortiori, none whose smallest coherent implementation is genuinely
semantically coupled across multiple product surfaces. Selecting any available
scrap and inflating it into a "coupled" implementation to run the succession
experiment would distort real product priority and is the precise anti-pattern
the owner instruction forbids.

Per the owner instruction: "Use `NO_COUPLED_CAPABILITY_CURRENTLY_WARRANTED` when
no sufficiently coupled capability can be selected without distorting real
product priority. This is a legitimate campaign result, not a failure. Do not
manufacture coupled work."

**Not `CAMPAIGN_PREMISE_INVALIDATED`:** durable architectural continuity during
coupled implementation is not shown to be a wrong or irrelevant research
question — the repository simply does not currently expose a warranted coupled
product capability to test it against. This is a state/timing result, not a
structural refutation of the premise.

**Not `OWNER_DECISION_REQUIRED` as the disposition:** no safe bounded *campaign*
work is *blocked* by an owner decision that the owner needs to make now. The
owner-reserved items (Goal A resume; the nine §6 decisions) are the repository's
standing integration/authorization boundary, not a Campaign 3 blocker. They are
listed in Part 7 as standing owner context, not as questions requiring an answer
to proceed.

**Not `EXTERNAL_BLOCKER`:** the fresh-controller substrate exists
(`STARTUP-PROVENANCE.md` §8); nothing environmental prevents Campaign 3 from
running — there is simply no warranted coupled capability for it to run against.

## PART 7 — Notes

**Evidence-origin discipline.** The posture claims in Part 1.3 are
`REPOSITORY-VERIFIED` across four independent documents. The open-work
enumeration in Part 1.5 is `GITHUB-VERIFIED` (`gh issue/pr list`) +
`REPOSITORY-VERIFIED` (§6 list, grep of `src/`/`scripts/`). The
"owner-reserved" classifications trace to `OWNER-INSTRUCTION.md` "Not Authorized
by Default" carried into `CHARTER.md`, the Campaign 2 CHARTER OWNER-RESERVED
list, ADR 0027, and the `workflow-system-disposition.md` §6 preamble.

**Standing owner context (not Campaign 3 questions).** Goal A resume +
substrate authorization (Issue #255); the nine
`docs/workflow-system-disposition.md` §6 decisions; ratification of any
Campaign 1/2 conclusion (incl. the NON-NORMATIVE `doc-status` marker) as product
architecture.

**Context-cost.** Controller A reached this disposition in roughly 20 tool calls
(≈10 durable-doc reads, ≈6 `git`/`gh` verifications, ≈4 greps of `src/`/`scripts/`
+ the §6 list). The single most decisive surface was `STATUS.md`'s
"Highest-leverage warranted next boundary" section (Campaign 2 Task A output),
corroborated by the research-agenda meta-finding and both campaign FINAL-REPORTs.
