# Controller A — reconstruction and Task A selection

```
CONTROLLER:     A (lead Campaign 2 controller; the context that received the
                owner instruction and ran the preflight + bootstrap).
WRITTEN:        2026-09-02, before any Task A implementation.
IMMUTABILITY:   this checkpoint preserves what Controller A believed at this
                point. It is not retro-edited when later evidence shifts the
                campaign's understanding. Later CAMPAIGN-STATE.md versions may
                supersede its conclusions; this file stays intact.
INPUTS USED:    OWNER-INSTRUCTION.md; CHARTER.md; CAMPAIGN-STATE.md v1;
                STARTUP-PROVENANCE.md; repository @ campaign base 06a57d1 +
                bootstrap 3c55254; GitHub (gh) read.
```

---

## Part 1 — Reconstruction

Evidence-origin tags: `REPO` (repository-verified), `GH` (GitHub-verified),
`OI` (owner-instruction-derived), `C1` (Campaign 1 durable docs, merged in #268
— treated as historical evidence, consequential claims reverified), `INF`
(controller inference).

### PRODUCT MISSION  (`REPO`, `C1`)

Sensemaking Skills = "an agent-native engineering sensemaking and control layer
for software-engineering agents" (`CONTEXT.md`). It moves an active coding agent
from repository uncertainty to evidence-grounded, warranted next action. The
active coding agent owns the recursive control loop (ADR 0013). Ratified
external product scope = the validated, human-reviewed
`repository_sensemaking_brief` (ADR 0014). Automatic fog-type→implementation
routing is **not** ratified (ADR 0014; ADR 0018 SUPERSEDED).

### CURRENT INTEGRATED PRODUCT STATE  (`REPO` @ 06a57d1, `GH`)

- **Control model** is explicit in docs: `docs/agent-native-operating-workflow.md`
  (operating map v0), `docs/decision-orchestration-boundary.md`, ADR
  0013/0014/0026/0027. Decision (select the responsibility) vs orchestration
  (coordinate it) are separated; consumers fail closed on non-live workflows and
  on missing authority events.
- **Campaign 1 landed on `main` via PR #268** (merged 2026-09-02T07:29:05Z,
  merge commit `06a57d1` == current `origin/main` HEAD; `git merge-base
  --is-ancestor` confirms). It added on the product surface: a documented
  "responsibility-level continuation from a durable Markdown record" pattern
  (operating map §2 subsection + Reality-map rows); a consolidated
  deterministic-machinery + hooks disposition (`decision-orchestration-boundary.md`
  "Deterministic machinery and hooks"); `docs/workflow-system-disposition.md`
  (23 workflows classified, pinned evidence, nine implied owner decisions, none
  applied); truthful hook description + `CLAUDE.md` SessionStart section; a lazy
  `workflow_liveness` resolver in `scripts/_validator_utils.py` + regression
  tests. **No** ADR / contract / registry / overlay / `src/` change.
- **27 ADRs** (`docs/adr/0001..0027` + README). Lifecycle: PROPOSED / PROVISIONAL
  / ACCEPTED / SUPERSEDED / REJECTED; the ADR probe enforces `**Status**` lines.
- **CI**: `.github/workflows/validation.yml` "Validator Ecosystem" (~19 jobs:
  Gate A security suites Linux+Windows; phase2–6 campaign-validation / ledger /
  execution-boundary; `validate` = Level 1 `validate-repo.py` + Level 2/3
  `test-validators.py` + run-log + mode-coverage; `probe-gate`; `core-assertions`;
  `conditional-representation-exact-head`). **Green on `06a57d1`**
  (`gh run list --branch main`: Validator Ecosystem completed/success
  2026-09-02T07:29:08Z). `REPO`+`GH`.
- **Open PRs (`GH`)**: only #194 (draft, `experiment/exp-0003-results`,
  "do not merge"). No product/campaign PR open.
- **Repo status surfaces (`REPO`)**:
  - `STATUS.md` — self-declared "single living status summary at the repo root."
    Last updated **2026-08-26**. Content: Goal A priority; a three-bullet
    "Current state" (distribution-drift probe; doc reconciliation; probe engine);
    a "Where to look" table. **Predates** PR #265/#267/#268 and the whole
    operating-map / decision-orchestration-boundary / workflow-system-disposition
    / agent-native-self-development consolidation. Its "Where to look" table does
    **not** name `docs/agent-native-operating-workflow.md`,
    `docs/decision-orchestration-boundary.md`,
    `docs/research/control-model-research-agenda.md`, or `docs/campaigns/`.
  - `roadmap.md` — "Roadmap to General Availability", "Phase 2.3 Complete",
    "Current Version: 0.2.1 (Beta)", a 3-week PyPI rollout plan. Last touched by
    a rename-refactor commit (`051b915`). Contradicts `STATUS.md` (v0.2.2) and
    `CONTEXT.md`. Campaign 1 classified it `HISTORICAL_ONLY` / no action.
  - `CONTEXT.md` — current, authoritative; "Current product definition",
    "Current evidence strategy: Goal A", a "Source-of-truth map" (topic → file
    index). Architecture/principles doc, **not** a development-direction state
    (no "what is decided / in flight / next warranted boundary / why / deferred").
  - `docs/` contains a large sprawl of dated historical `PHASE-*`, `STAGE-*`,
    `IMPLEMENTATION-COMPLETE-*`, `WEEK1-*`, `task-*` documents (dozens), plus the
    current operating docs and the semantic-control-map trial.
- **Research lanes (non-ratified) (`REPO`, `GH`)**: Goal A external validation
  ACTIVE but halted in this environment (Issue #255; `experiments/evidence/0023`);
  `C6R` compressed-control hypothesis + Issue #226 gate-separation study;
  `docs/semantic-control-map.md` trial OPEN (min close 2026-09-28). The research
  agenda's "Meta-finding 2026-08-30": sensemaking loops saturated — further
  briefs no longer change the warranted responsibility.

### CURRENT RATIFIED PRODUCT BOUNDARY  (`REPO`)

ADR 0014: the validated, human-reviewed `repository_sensemaking_brief` is the
settled external product core; automatic downstream routing is deferred pending
external proof. `CONTEXT.md` "Lifecycle positioning": Sensemaking is
cross-cutting, not an SDLC stage; the clarification "does not broaden product
scope" and "does not ratify Sensemaking as a general product-development
operating system."

### DEMONSTRATED PRODUCT CAPABILITIES  (`C1` merged, reverify before use)

- Agent-native brief production + deterministic validation across ≥2
  repositories; responsibility-before-Skill selection without routing; claim
  reconciliation; finding-specific repair verification; fail-closed authority on
  auto-invoke and liveness; probe-engine enforcement gate in CI.
- **Responsibility-level, artifact-mediated continuation into a fresh context**
  from a durable Markdown record — six responsibility classes; verification-
  bearing (fresh contexts corrected ~22 wrong/overstated record facts, none
  causing a wrong action; twice declined an out-of-grant edit).
- **Limitation (Campaign 1's own words)**: one **persistent dispatcher**, one
  repo, one day; fresh contexts were **workers**, not **controllers**; largest
  code change from durable state = one script + tests, no `src/`.

### DEMONSTRATED CAMPAIGN CAPABILITIES (Campaign 2)  

None. Bootstrap only.

### EVIDENCE CEILINGS  (`OI`, `C1`)

- **EC-1 Minimality** — a successful rich-state handoff shows SUFFICIENCY, not
  STRICT MINIMALITY; no comparative evidence exists.
- **EC-2 Succession isolation** — the fresh-controller mechanism
  (`Agent` subagent) gives HARNESS-REPORTED context isolation (no transcript, no
  private reasoning) + CONTROLLER-ASSERTED bootstrap minimality / checkpoint
  immutability / non-resumption; predecessor **process** non-persistence is
  **not** environment-enforced → `SUCCESSION_ISOLATION_UNVERIFIED` on that
  dimension (STARTUP-PROVENANCE.md).
- **EC-3 Scale** — Campaign 1 evidence is single-dispatcher / single-repo /
  single-day; not automatically lifted.
- **EC-4 Product vs campaign state** — whether durable *campaign* state maps to
  any needed durable *product* state is open; must be answered from evidence.
- **EC-5 Implementation depth** — no broad `src/` implementation depth across
  product surfaces demonstrated from durable state.

### CURRENT MATERIAL GAPS (relative to the campaign mission)  (`INF` from `OI` + `C1`)

- **MG-1** No fresh context has owned the **complete semantic
  campaign-controller** role (next-task selection included).
- **MG-2** No **cross-controller** semantic continuation demonstrated.
- **MG-3** Only one dispatcher/controller has ever run a campaign here.
- **MG-4** No general autonomous repository self-development; no production-grade
  reliability.
- **MG-5** Strict minimality of durable continuation state untested (EC-1).
- **MG-6** Unclear which part of Campaign 1's continuation capability belongs in
  the *product* vs exists only for campaign experimental control.
- **MG-7** (new, this reconstruction) The repository's designated
  development-direction surfaces (`STATUS.md`, `roadmap.md`) do not reflect
  integrated reality and are not a reliable reconstruction basis; direction is
  scattered across `CONTEXT.md` + operating map + research agenda + `docs/campaigns/`
  + GitHub issues. There is no product representation of "current highest-leverage
  warranted development boundary and why."

### KNOWN OWNER DECISIONS  (`C1`, `GH`)

1. Merge of PR #268 — **RESOLVED** (merged; it is Campaign 2's base).
2. Whether to record Campaign 1's substrate observation on Issue #255 — open,
   optional.
3. The nine registry/overlay/documentation items implied by
   `docs/workflow-system-disposition.md` section 6 — open.

### KNOWN DEFERRED WORK  (`C1` `FINAL-REPORT.md` §9)

Engineering debt, all pre-existing, none in CI: D2b (`test_validate_brief_json.py`
fixture drift → U8), D8 (stale `validation.yml` comment), D17
(`mode-coverage.yaml` overstated `steps_completed`), D18 (packaged catalog
divergence), D19 (`test_validator_utils.py` expectation predates ADR 0027
`liveness`), D14 (local Windows/Python platform reds green in Linux CI). Inherited
context, **not** Campaign 2 work unless a strategic warrant elevates one.

### LAST KNOWN CAPABILITY FRONTIER

None recorded by any Campaign 2 controller (this is the first). Campaign 1's
final frontier was "closure" (its mission was complete). Campaign 1 did **not**
assess a frontier for *repository-level controller succession* — that is
Campaign 2's starting point per the owner instruction.

### CURRENTLY PLAUSIBLE CAPABILITY BOUNDARIES

Enumerated and compared in Part 2.

### AVAILABLE AUTHORITY  (`OI`, `CHARTER.md`)

Own Campaign 2 end-to-end on the campaign branch; all reads; local engineering
on the branch (code, tests, docs, commits, validators); push the branch;
create/maintain a **draft** PR. **Not** authorized: merge; ADR acceptance;
external publication; issue-lifecycle changes for bookkeeping; unrelated PR
merges; protected-policy edits; inferring owner preference — any of these →
`OWNER_DECISION_REQUIRED`. Repository policy (accepted ADRs, `CONTEXT.md`,
`AGENTS.md`, contracts, schemas) still governs the product.

### CURRENT ORIGIN/MAIN STATE / CAMPAIGN BASE / CI  (`REPO`, `GH`)

```
STARTING ORIGIN/MAIN (base):   06a57d1d182a32684275d343a9248429feedbfe6
CURRENT ORIGIN/MAIN:           06a57d1  (== base; no drift, checked 2026-09-02)
CAMPAIGN BASE:                 06a57d1
CAMPAIGN HEAD (bootstrap):     3c55254e0f3d2b4908179aaa0f4b20cb9dd67a8b  (pushed)
MAIN DRIFT SINCE START:        none
CANDIDATE CHANGES NOT ON MAIN: Campaign 2 scaffolding only (bootstrap commit)
RATIFICATION / MERGE STATUS:   nothing merged from Campaign 2; no PR yet
CI:                            main "Validator Ecosystem" green @ 06a57d1;
                              no campaign head has run CI yet
```

---

## Part 2 — Strategic boundary comparison

The campaign frontier question: **what is the highest-leverage unresolved
*product* capability boundary for "repository-level development direction
surviving independent controller replacement," distinct from campaign
instrumentation and from the nearest visible defect?**

### Candidate boundary 1 — Development-direction reconstruction surface

- **What.** The product has no coherent, current representation of
  repository-level development direction that an independent controller can
  reconstruct the highest-leverage warranted boundary from. `STATUS.md`
  (self-declared living summary) is ~1 week + one architecture era stale;
  `roadmap.md` actively contradicts reality; `CONTEXT.md` is a principles +
  topic-index doc, not a direction state; the real picture is scattered across
  6+ docs + GitHub issues + `docs/campaigns/`.
- **Plausible?** Yes. This is exactly the central question's "distinguish the
  next strategically consequential product capability from merely the nearest
  visible repository defect" and "which information should survive vs be
  re-derived."
- **Evidence.** `STATUS.md` "Last updated 2026-08-26"; its git log ends at
  `f4d3a9d`; its "Where to look" omits the current operating docs.
  `roadmap.md` "Phase 2.3 Complete / v0.2.1 Beta". `docs/` historical sprawl.
  Campaign 1 R1 needed 39 files / 25 calls to reconstruct *with* a dedicated
  `CAMPAIGN-STATE.md`; a *product-development-direction* reconstruction has no
  such anchor.
- **Warranted now?** Strongest candidate. Directly on the campaign's central
  question; small, bounded, reversible; low risk of scope creep if the change is
  discovered rather than assumed. Risk to manage: not collapsing into "fix stale
  docs" (cleanup) — the task must first establish that the reconstruction
  *failure* is real and product-relevant, then deliver only the smallest change
  that makes direction reconstruction-sufficient (which may be a `STATUS.md`
  refresh + a short reconstruction convention, a pointer, or a verified "no new
  mechanism warranted, the gap is elsewhere").

### Candidate boundary 2 — Promote "artifact-mediated continuation" from campaign observation to a product-offered pattern

- **What.** Campaign 1 documented responsibility-level continuation, but the
  operating map frames it as *"demonstrated in real use inside the campaign
  directory"* — an observed pattern, not a capability an operator is told they
  can adopt, with its field set / verification discipline / reopen conditions
  stated as product guidance.
- **Plausible?** Partly. Some of this already exists (operating map §2
  subsection lists the necessary durable state and failure classes).
- **Warranted now?** Weaker. Largely done by Campaign 1 R3/R5; the incremental
  delta is thin and risks "documentation that merely restates known facts."
  Also does not clearly address *controller* (vs worker) succession.

### Candidate boundary 3 — Verification-bearing handoff as an explicit product capability

- **What.** Campaign 1's central epistemic finding: durable state can be wrong,
  and that is survivable *iff* the consuming context reverifies consequential
  claims. Does the product's `handoff` skill / `session_summary` /
  `prompt_handoff` surface encode *verification-bearing consumption*, or is that
  discipline only in campaign practice?
- **Plausible?** Yes, and it is close to the campaign's H3 hypothesis.
- **Evidence.** Not yet gathered (would need to read the `handoff` SKILL.md and
  the artifact contracts).
- **Warranted now?** Possible, but likely doc-only unless a real consumer gap is
  found; overlaps candidate 1 (a reconstruction surface that is *known to need
  reverification* is part of the same capability). Fold into candidate 1's
  investigation rather than select separately.

### Candidate boundary 4 — `repo-sensemaker` brief vs development-direction state

- **What.** The brief is a point-in-time *diagnosis*; it does not represent
  development *direction*. Is the brief being expected to carry direction state
  (a boundary problem), or is direction legitimately out of the ratified product
  scope (ADR 0014)?
- **Warranted now?** No. ADR 0014 explicitly bounds product scope to the brief
  and defers more; expanding `repo-sensemaker` is exactly what the owner
  instruction says not to assume. If evidence shows direction state *must* live
  somewhere and the only candidate is the brief, that becomes
  `OWNER_DECISION_REQUIRED`, not Task A.

### Candidate boundary 5 — Premise check: is a new product capability needed at all?

- **What.** Maybe repository-level development direction is already cheaply
  reconstructible (CONTEXT.md source-of-truth map + GitHub + `git log`), and
  Campaign 2's premise over-reads Campaign 1. If so →
  `CAMPAIGN_PREMISE_INVALIDATED` candidate.
- **Warranted now?** This is not a separate task — it is the **decision-changing
  uncertainty inside candidate 1**. Task A must genuinely test it (attempt the
  reconstruction, measure cost / staleness / error), and a well-supported
  "premise invalid / existing mechanism suffices" is a legitimate Task A outcome
  (an equivalently consequential result: verified premise invalidation).

### SELECTED BOUNDARY — Candidate 1 (with candidate 5 as its internal uncertainty; candidate 3 folded in)

**Why it dominates.** It is the only candidate that (a) sits directly on the
campaign's central question, (b) is bounded and reversible, (c) does not
predetermine the solution or require new machinery, (d) has concrete
already-visible evidence that the limitation exists, and (e) would remain
warranted even if controller succession were already solved (a fresh controller
still needs a reconstruction basis). Candidates 2 and 3 are narrower and partly
done; 4 is out of ratified scope; 5 is an outcome of 1, not a rival.

---

## Part 3 — Strategic Selection Gate (Task A)

```
PRODUCT CAPABILITY AFFECTED:
  Repository-level development-direction reconstruction — the ability of an
  independent coding-agent controller to determine, from durable repository +
  GitHub evidence alone, where product development currently is and what the
  highest-leverage warranted development boundary is (as opposed to the nearest
  visible defect).

CURRENT LIMITATION:
  No product surface reliably carries that. STATUS.md (the self-declared "single
  living status summary") is stale by ~1 week and one architecture era and omits
  the current operating docs from its "Where to look"; roadmap.md actively
  contradicts reality; CONTEXT.md is a principles + topic-index doc, not a
  direction state; the real picture is spread across CONTEXT.md, the operating
  map, the decision-orchestration boundary, the research agenda, docs/campaigns/,
  and GitHub issues #218/#226/#255.

EVIDENCE THE LIMITATION EXISTS:
  - STATUS.md front-matter "Last updated 2026-08-26"; git log for STATUS.md ends
    at f4d3a9d (pre #265/#267/#268); its "Where to look" table names neither
    agent-native-operating-workflow.md nor decision-orchestration-boundary.md nor
    control-model-research-agenda.md nor docs/campaigns/.
  - roadmap.md: "Phase 2.3 Complete", "Current Version: 0.2.1 (Beta)",
    GA-rollout plan; last touched by a rename-refactor commit.
  - CONTEXT.md "Source-of-truth map" is a topic index, not a state.
  - docs/ carries dozens of dated PHASE-*/STAGE-*/IMPLEMENTATION-COMPLETE-*/task-*
    historical documents with no durable "which of these is current" signal
    beyond STATUS.md's archive pointer.
  - Campaign 1's own reconstruction probe (R1) cost 39 files / 25 tool calls
    WITH a dedicated CAMPAIGN-STATE.md anchor.

INTENDED PRODUCT USER OR OPERATOR:
  A fresh coding-agent controller (or a human maintainer) picking up
  repository-level development of sensemaking-skills without prior conversation
  context — the exact actor Campaign 2 is about, and a realistic
  agent-native-product operator.

USER- OR OPERATOR-OBSERVABLE VALUE:
  That operator can, from one small durable surface plus named authoritative
  pointers, reconstruct current development direction and the current
  highest-leverage warranted boundary quickly and without anchoring on stale
  claims — instead of synthesising 6+ documents and cross-checking GitHub and
  risking a wrong anchor.

WHY IT MATERIALLY CONSTRAINS THE CAMPAIGN MISSION:
  The mission is "independent fresh controllers reconstruct current
  product-development state, identify the highest-leverage warranted development
  boundary, ... and leave the repository continuable by another fresh
  controller." If the product cannot represent development direction so it
  survives reconstruction, controller succession has nothing durable to stand on
  except campaign instrumentation — which the owner instruction says is NOT
  automatically product architecture.

WHAT PRODUCT CAPABILITY BECOMES STRONGER IF SOLVED:
  "Repository-level development direction survives independent controller
  replacement" — the campaign's central capability. Also strengthens the
  product's honesty guarantee (no stale self-declared status surface).

WHY THIS IS PRODUCT ADVANCEMENT RATHER THAN CAMPAIGN INSTRUMENTATION:
  CAMPAIGN-STATE.md is campaign-scoped and non-authoritative. This task targets
  the *product's own* development-direction surface (STATUS.md / CONTEXT.md
  source-of-truth map / roadmap.md), used by any operator, campaign or not. The
  task explicitly must NOT create a campaign-shaped artifact in the product.

WHY THIS TASK WOULD REMAIN WARRANTED IF THE SUCCESSION ACCEPTANCE CONDITION
WERE ALREADY SATISFIED:
  Even with perfect controller succession, each new controller still needs a
  durable, current basis to reconstruct development direction. A stale
  self-declared status surface would mislead them regardless of how clean the
  handoff mechanism is.

WHY THIS IS A STRATEGIC DEVELOPMENT TASK RATHER THAN MERELY A NEARBY DEFECT:
  The nearby-defect framing would be "STATUS.md and roadmap.md are stale, update
  them" — which Campaign 1 already classified HISTORICAL_ONLY / no-action for
  roadmap.md. The strategic framing is: establish whether development-direction
  reconstruction actually fails for an independent controller, classify the
  failure, and deliver the smallest product change that makes direction
  reconstruction-sufficient — or a verified conclusion that no new mechanism is
  warranted. The output is an architectural conclusion about what durable
  product state must exist for controller succession, not a doc refresh.

DECISION-CHANGING UNCERTAINTY:
  Is repository-level development direction genuinely NOT reconstructible by an
  independent controller from current durable evidence (making a product change
  warranted), or is it already cheaply reconstructible (making this
  CAMPAIGN_PREMISE_INVALIDATED, or the frontier elsewhere)? Sub-uncertainty: if
  a change is warranted, is the smallest sufficient one a refresh + a stated
  reconstruction convention on existing surfaces, or something larger?

BOUNDED TASK:
  See Part 4.

EXPECTED EVIDENCE THAT WOULD CHANGE THE CAPABILITY ASSESSMENT:
  - A bounded reconstruction attempt from durable evidence alone succeeds
    quickly and accurately in naming the current highest-leverage boundary →
    premise weakened; record and reassess (possibly CAMPAIGN_PREMISE_INVALIDATED
    or frontier elsewhere).
  - The attempt fails in a specific, classifiable way (anchors on stale
    STATUS.md/roadmap.md; cannot find the current operating docs from the
    designated surface; cannot tell decided-vs-in-flight) → limitation confirmed;
    deliver the smallest warranted change.
  - The failure is really about campaign instrumentation, not the product →
    narrow to MG-6, do not change the product surface.
```

---

## Part 4 — Task A definition (bounded responsibilities)

**Task A: Establish whether repository-level development direction is
reconstructible by an independent controller, classify the failure if any, and
deliver the smallest warranted product change that makes development-direction
reconstruction sufficient — or a verified conclusion that no new product
mechanism is warranted.**

Task A is complete at its **legitimate boundary** (owner instruction
"Legitimate Task Boundary") when: the decision-changing uncertainty above is
resolved with evidence; the warranted change is implemented, ruled unnecessary,
or shown to need a fresh campaign warrant; and relevant validation has run.

### Bounded responsibilities

- **A1 — Reconstruction-failure evidence.** From durable repository + GitHub
  evidence only (no campaign-2 semantic state, no conversation), attempt to
  answer: "what is the current highest-leverage warranted development boundary
  for sensemaking-skills, and what is decided vs in-flight vs deferred?" Record
  what the designated surfaces (`STATUS.md`, `roadmap.md`, `CONTEXT.md`
  source-of-truth map) yield, what is stale/contradictory, what had to be
  synthesised from where, and the cost. Classify any failure using the owner
  instruction's failure classes (esp. `CAMPAIGN_STATE_INSUFFICIENT` analog for
  the product, `PRODUCT_DIRECTION_AMBIGUITY`, `CONTEXT_RECONSTRUCTION_COST_
  EXCESSIVE`, or "no failure — premise weakened"). Durable output:
  a section in this campaign directory (e.g. `A-task-A1-reconstruction-probe.md`).
  *Consider* running this as a bounded fresh-context sub-probe (Campaign 1 R1
  style) for credibility; this is a tool inside Task A, distinct from the
  Controller B succession.
- **A2 — Decide the warranted change.** From A1: (i) premise invalid / existing
  mechanism suffices → record the verified conclusion, no product edit; or
  (ii) limitation confirmed → identify the **smallest** coherent product change
  (candidates, smallest first: refresh `STATUS.md` to integrated reality +
  extend its "Where to look" to name the current operating/direction docs and
  the campaigns + add a short "how to reconstruct current development direction"
  paragraph pointing at the authoritative sources and stating what a fresh
  controller should be able to derive and from where; and give `roadmap.md` an
  honest archived/superseded header + redirect. Do NOT create a new artifact
  type / schema / YAML / Skill / workflow / registry field unless A1 shows the
  lighter change demonstrably fails). Record the choice and why smaller was
  rejected.
- **A3 — Implement the smallest warranted change** on the campaign branch
  (product surface only; no campaign-shaped artifact in the product; no ADR /
  contract / registry / `src/` change unless separately warranted and, if it
  would need owner authority, recorded as `OWNER_DECISION_REQUIRED`).
- **A4 — Validate.** `python scripts/validate-repo.py` (exit 0);
  `python scripts/probe-repo.py ... ` + `validate-probe-report.py` +
  `gate_relationship_findings.py` (no new blocking findings — STATUS lines / ADR
  refs); `python scripts/test-validators.py`; `python -m pytest` on the
  `core-assertions` set; inspect the diff; confirm the tree is otherwise clean.
  Push; observe exact-head CI.
- **A5 — Update campaign semantic state.** CAMPAIGN-STATE.md: record Task A, the
  boundary, alternatives, capability advanced, evidence, remaining ceilings,
  context-cost observations from A1, any failure observations, and Controller A's
  **last assessed** capability frontier for Controller B (as LAST ASSESSED
  CANDIDATE, not a command).
- **A6 — Reassess from the mission**, then prepare the mandatory handoff to a
  genuinely fresh Controller B (`A-handoff.md`: pre-handoff invariant checklist;
  handoff provenance; verbatim bootstrap text; handoff SHA) and relinquish
  semantic control.

### Not authorized in Task A

Merging; ADR / contract / canonical-vocabulary / registry / liveness-overlay /
`src/` edits; external tracker writes; creating a new product artifact
type/schema/Skill/workflow/hook without A1 evidence that the lighter change
fails; inferring owner preference. Any of these that becomes warranted →
`OWNER_DECISION_REQUIRED` in CAMPAIGN-STATE.md.

### Stop condition

Decision-changing uncertainty resolved with durable evidence; the warranted
change implemented / ruled unnecessary / shown to need a fresh campaign warrant;
validation run; CAMPAIGN-STATE.md updated; `A-handoff.md` committed; Controller A
relinquishes.
