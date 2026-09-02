# Campaign 2 durable semantic state — Durable Repository-Level Self-Development

```
STATUS:     ACTIVE (v2). Controller A reconstruction done; Task A selected;
            Task A implementation not started.
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
CAMPAIGN HEAD (bootstrap commit):       3c55254e0f3d2b4908179aaa0f4b20cb9dd67a8b  (pushed to origin)
CURRENT CAMPAIGN HEAD:                  <A reconstruction+selection commit> (record SHA after commit)
MAIN DRIFT SINCE CAMPAIGN START:        none
CANDIDATE CHANGES NOT ON MAIN:          Campaign 2 scaffolding + Controller A checkpoint
   docs/campaigns/durable-repo-self-development/{OWNER-INSTRUCTION,CHARTER,
   CAMPAIGN-STATE,STARTUP-PROVENANCE}.md + controllers/{README,
   A-reconstruction-and-selection}.md
RATIFICATION / MERGE STATUS:            nothing merged; no PR yet
CAPABILITY CLAIMS THAT APPLY ONLY TO THE CANDIDATE:  none yet (no product change)
CAPABILITY CLAIMS THAT APPLY TO INTEGRATED MAIN:     see section 5 (Campaign 1 result, merged in #268)
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

None yet. Bootstrap only. (This section will record what Campaign 2's
controller/harness arrangement has been shown to reliably do — kept distinct from
product capabilities.)

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

None completed yet. **Task A is SELECTED and specified** (not started) — see
`controllers/A-reconstruction-and-selection.md` (immutable checkpoint).

| Task | Controller | Selected because | Alternatives considered | Capability advanced | Evidence | Ceiling remaining |
|---|---|---|---|---|---|---|
| A (in progress) | A | Development-direction reconstruction surface is the only candidate boundary that sits directly on the campaign's central question, is bounded/reversible, does not predetermine the solution, has concrete evidence the limitation exists, and stays warranted even if succession were already solved. | (1) *selected*: development-direction reconstruction surface; (2) promote artifact-mediated continuation to a product-offered pattern — thin, largely done by C1; (3) verification-bearing handoff as an explicit capability — folded into (1); (4) `repo-sensemaker` brief vs direction state — out of ratified scope (ADR 0014); (5) premise check — this is (1)'s internal decision-changing uncertainty, not a rival. | pending Task A | pending | EC-1..EC-5 carried; new context-cost evidence expected from A1 |

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
  surfaces (`STATUS.md` "single living status summary", `roadmap.md`) do not
  reflect integrated reality (both predate the ADR 0013+ operating-map era and
  both campaigns; `roadmap.md` says "Phase 2.3 / v0.2.1 Beta"); direction is
  scattered across `CONTEXT.md` + operating map + research agenda +
  `docs/campaigns/` + GitHub issues; there is no product representation of "the
  current highest-leverage warranted development boundary and why." **This is the
  boundary Task A investigates.**

## 10. LAST ASSESSED CAPABILITY FRONTIER

**Controller A, 2026-09-02 (LAST ASSESSED CANDIDATE — not a command; a successor
owns the next decision and may reject this):** the highest-leverage unresolved
*product* boundary for "repository-level development direction surviving
independent controller replacement" is the **development-direction
reconstruction surface** — the product has no current, coherent representation
of where product development is and what the highest-leverage warranted boundary
is; `STATUS.md`/`roadmap.md` are stale, direction is scattered. Full comparison
of five candidate boundaries and the selection rationale:
`controllers/A-reconstruction-and-selection.md` Part 2.

## 11. ACTIVE DECISION-CHANGING UNCERTAINTIES

- **U-1** What is the strongest defensible controller-isolation level achievable
  with the available fresh-context mechanism? (preflight item 12 / EC-2;
  STARTUP-PROVENANCE records the current assessment.)
- **U-2** Is repository-level development direction genuinely NOT reconstructible
  by an independent controller from current durable evidence (product change
  warranted), or already cheaply reconstructible (→ `CAMPAIGN_PREMISE_INVALIDATED`
  candidate, or frontier elsewhere)? Sub-uncertainty: if warranted, is the
  smallest sufficient change a refresh + stated reconstruction convention on
  existing surfaces, or larger? **Task A resolves this with evidence (A1).**
- Further uncertainties are added as Task A / Controller B proceed.

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
pushed:        3c55254 (bootstrap) -> origin/campaign/durable-repo-self-development
PR:            none yet (draft PR deferred until Task A produces reviewable change)
origin/main:   06a57d1  (== campaign base; no drift, re-checked 2026-09-02 v2)
campaign CI:   not yet run on any campaign head (bootstrap + A checkpoint are
               docs-only under docs/campaigns/; CI "validate" job runs
               validate-repo.py which does read docs/ structure — observed on push)
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
                          (controllers/A-reconstruction-and-selection.md).
                          Selected boundary: development-direction reconstruction
                          surface. -> next: execute Task A (A1 reconstruction
                          probe -> A2 decide smallest warranted change -> A3
                          implement -> A4 validate -> A5 update state), then
                          mandatory handoff to a genuinely fresh Controller B.
```

## 17. FAILURE OBSERVATIONS

None yet. (Classes available: `CAMPAIGN_STATE_INSUFFICIENT`,
`STRATEGIC_SELECTION_UNSTABLE`, `HANDOFF_FACT_INCORRECT`,
`HANDOFF_FACT_TRUST_FAILURE`, `PRODUCT_DIRECTION_AMBIGUITY`,
`CAPABILITY_MODEL_MISSING`, `AUTHORITY_RECONSTRUCTION_FAILURE`,
`CONTEXT_RECONSTRUCTION_COST_EXCESSIVE`, `CAPABILITY_DISCOVERY_FAILURE`,
`MISSING_DURABLE_STATE`, `INCIDENTAL_CONTEXT_LOSS`, `HANDOFF_STATE_CONTAMINATION`,
`SUCCESSION_ISOLATION_UNVERIFIED`, `BASELINE_DRIFT_MATERIAL`,
`OTHER_DEMONSTRATED_FAILURE`.)

## 18. CONTEXT-COST OBSERVATIONS

None yet. (Recorded qualitatively per fresh-controller reconstruction: what had
to be rediscovered from repo / GitHub; what durable state saved material work;
what was redundant; what required reverification; what would have been dangerous
to trust unverified; what rationale would have been expensive to reconstruct;
what was cheaper to reconstruct than maintain; what looks product-worthy vs
campaign-specific.)

## 19. MINIMALITY EVIDENCE / CLAIM CEILING

No comparative minimality evidence. Current supported claim ceiling: nothing —
no handoff has occurred. See EC-1. Any eventual sufficiency result stays
"smallest currently supported candidate" unless comparative evidence is produced.

## 20. CAMPAIGN ACCEPTANCE STATUS

Early. No strategic task completed, no handoff, no succession yet. Toward the 19
conditions: Controller A has produced an immutable reconstruction + selection
checkpoint (contributes to condition 9's analog for A; the binding instance is
Controller B's). Nothing else evaluable yet.

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
  warranted"). MG-7 added. Task A implementation not started. Next: execute Task
  A (A1 reconstruction probe first).
