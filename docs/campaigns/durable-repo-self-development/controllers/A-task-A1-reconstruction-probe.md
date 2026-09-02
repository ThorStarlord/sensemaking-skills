# Task A / A1 — fresh-context development-direction reconstruction probe

```
CONTROLLER:   A. Written 2026-09-02, during Task A execution, before A3
              (implementation).
PURPOSE:      resolve Task A's decision-changing uncertainty (U-2) with
              evidence: is repository-level development direction reconstructible
              by an independent context from durable evidence alone, and if not,
              what fails and is it a product problem or campaign instrumentation?
METHOD:       a fresh general-purpose sub-agent context (no conversation history,
              no Campaign 2 semantic state) was asked to reconstruct "the current
              highest-leverage warranted development boundary" and "decided / in
              flight / deferred" from durable repository files + `gh` only, with
              `docs/campaigns/durable-repo-self-development/` excluded. This is a
              TOOL inside Task A, NOT the Controller B succession.
NEUTRALITY:   the sub-agent prompt named no suspect files and stated no expected
              answer; it asked for the reconstruction, the sources used, the
              staleness found, the confidence, and the cost.
```

## Controller A analysis

### Verdict on U-2

**Limitation confirmed; product-surface, not campaign instrumentation; not
premise-invalidation.**

- The strategic headline **is** reconstructible — the fresh context reached a
  defensible answer (Goal A / A1 external validation is the named highest-value
  workstream, currently substrate-blocked per Issue #255) in ~15 tool calls.
- But the **designated** reconstruction surface does not carry it. `STATUS.md`
  ("the single living status summary at the repo root") is "thin, dated
  2026-08-26, and already trails the 2026-09-02 campaign closure and the
  2026-08-31 reassessment." The real current picture "lives in a campaign
  subdirectory and in GitHub issues rather than on the documented
  'source-of-truth map'."
- Three root orientation files **actively mislead** toward a superseded
  PyPI/GA plan: `roadmap.md` ("Phase 2.3 / v0.2.1 Beta / 3-week rollout"),
  `CHANGELOG.md` (stops 2026-08-07, dead "Deployment Timeline" footer),
  `00-user-intent.md` ("Framework ready for 3-week rollout plan"). Add
  `goal.md` (Controller A note): its "the system ... selects the right workflow
  ... sequences the right skills ... stopping only at explicit approval gates"
  is the pre-ADR-0013 autonomous-orchestrator vision that `CONTEXT.md` explicitly
  disclaims.
- "A fresh maintainer who trusted `roadmap.md` or the auto-memory would draw the
  wrong conclusion; one who found
  `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` and Issue #255
  would get there in about fifteen minutes."
- ~45 loose historical `docs/*.md` (`PHASE-*`, `STAGE-*`, `WEEK1-*`, `task-*`,
  `UI-ROUTING-*`) are not marked archived; ADRs 0017–0021 are
  SUPERSEDED/never-Accepted but findable by title as if decided.

This is not `CAMPAIGN_PREMISE_INVALIDATED`: development direction does **not**
survive independent reconstruction from the product's own designated surfaces
without either an excessive discovery cost or a real wrong-anchor hazard. It is
not campaign instrumentation: every failing surface (`STATUS.md`, `roadmap.md`,
`goal.md`, `CHANGELOG.md`, `CONTEXT.md` source-of-truth map, the `docs/` sprawl,
ADR status discoverability) is a **product** surface any maintainer/operator
hits.

### Failure classification (owner-instruction classes, product analog)

- Primary: **`CONTEXT_RECONSTRUCTION_COST_EXCESSIVE`** — bounded but real
  (~15 calls, four scattered documents, one of them a campaign subdirectory not
  named by the source-of-truth map).
- Secondary: **`HANDOFF_FACT_INCORRECT`** (caught, not trusted) — the stale
  surfaces contain wrong consequential facts ("Phase 2.3 / v0.2.1 Beta / GA
  rollout"); the fresh context distrusted them and cross-checked, so no wrong
  action followed. Had it been less diligent this would have been
  `HANDOFF_FACT_TRUST_FAILURE`.

### Probe false-positive note (this file)

Running `scripts/probe-repo.py` + `scripts/gate_relationship_findings.py` after
this file was written produces **2 new non-blocking `adr/status_claim_mismatch`
evidence findings** pointing at the verbatim quote below (the sentences that
correctly state ADR 0017 / ADR 0021 are "SUPERSEDED, never Accepted"). The
probe's heuristic matches "ADR 00NN" near the token "Accepted" and reads it as a
claim of *accepted*; the text says the opposite. The probe gate **PASSES**
(`adr/status_claim_mismatch` never blocks — only `missing_reference` /
`missing_status_line` do), so CI is unaffected. The finding is left as-is: it is
a verbatim evidence quote and altering quoted text to satisfy a probe heuristic
would be worse than the noise. Recorded in `CAMPAIGN-STATE.md` section 17.

### Probe-contamination note (minor, disclosed, non-load-bearing)

The sub-agent disclosed that one broad `Grep` matched files under the excluded
`docs/campaigns/durable-repo-self-development/` and printed ~30 lines in tool
output. It states it did not open those files or build on the lines, and that
the visible lines ("`STATUS.md` is the closest surface"; "there is no product
representation of current highest-leverage ...") were consistent with
conclusions it had already reached independently. Controller A assessment: the
contamination is real but immaterial — it neither seeded nor changed the
probe's independent findings, which rest on `STATUS.md`'s own front-matter,
`roadmap.md`/`CHANGELOG.md`/`00-user-intent.md` content, the ADR status sweep,
and the campaign-1 docs. Recorded as a `HANDOFF_STATE_CONTAMINATION`-adjacent
harness observation in `CAMPAIGN-STATE.md` §17; it does not invalidate A1.

### What A1 warrants (feeds A2)

The smallest coherent product change that makes development-direction
reconstruction sufficient **and** removes the wrong-anchor hazard, on existing
Markdown surfaces, adding no new artifact type / schema / Skill / workflow /
registry field / `src/` change:

1. **`STATUS.md`** refreshed into a real current-direction + reconstruction
   surface (current snapshot; a "Current development direction" section stating
   ratified / in-flight / deferred + the highest-leverage next boundary; a
   "Reconstructing current development direction" section naming the ordered
   authoritative sources and the stale files not to anchor on; a corrected
   "Where to look" table).
2. **`roadmap.md`**, **`goal.md`** — minimal superseded/historical headers with
   a redirect to `STATUS.md` + `CONTEXT.md`. (No rewrite.)
3. **`CONTEXT.md`** "Source-of-truth map" — one additive row pointing to
   `STATUS.md` as the current development-direction surface (closes the gap A1
   named: current state not on the source-of-truth map). Purely additive; no
   change to any CONTEXT.md claim.

`00-user-intent.md` (a durable `user_intent` artifact instance validated by
`scripts/validate-user-intent.py`) and `CHANGELOG.md` are **flagged in
STATUS.md's reconstruction note**, not edited.

---

## Fresh-context probe report (verbatim)

> Sub-agent: `general-purpose`, fresh context, no conversation history. Worktree
> `H:/GithubRepositories/smk-campaign-2` @ `a216293`. Cost (self-reported):
> ~22–24 tool calls, ~16 durable documents + 3 GitHub issues + a 27-file ADR
> status sweep. Duration ~4.8 min.

```
# Reconstruction report -- "where is product development, and what's next?"

Scope note: independent reconstruction from durable files + `gh` only, on
`campaign/durable-repo-self-development` @ `a216293`. I did **not** open any
file under `docs/campaigns/durable-repo-self-development/`. One leak to disclose
(see section 4): a broad `Grep` pattern matched files in that directory and
surfaced ~30 lines of them in the tool output. I did not open those files and
did not build on those lines; they happened to agree with conclusions I'd
already reached.

## 1. Highest-leverage warranted next development boundary

**Unblock and run the first compliant Goal A / A1 external product-validation
episode** -- a fresh-agent Sensemaking run producing an unmodified
`repository_sensemaking_brief` on a pinned external repo, then independent
evidence audit + independent usefulness evaluation.

Why this and not something else:

- The entire product rests on one unvalidated hypothesis: that a validated,
  human-reviewed `repository_sensemaking_brief` (the ratified scope, ADR 0014)
  is actually *useful* on repositories other than this one. Durable evidence
  says the brief path is demonstrated on exactly **one** fresh external repo,
  and product-wide GA / real-executor E2E is explicitly **not claimed**
  (`CONTEXT.md` MODEL_WARRANT paragraph; ADR 0014 evidence note).
- Four independent durable surfaces name Goal A as *the* current priority:
  `STATUS.md` ("Current product-validation priority"), `CONTEXT.md` ("Current
  evidence strategy: Goal A"),
  `docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md` ("the
  next authorized episode remains the highest-value product-validation
  workstream"), and Issue #255.
- Every other candidate workstream is *deliberately gated shut*. `CONTEXT.md`
  principle 10 and `docs/research/control-model-research-agenda.md` ("current
  priority is no longer to expand the control vocabulary"; meta-finding
  2026-08-30 "sensemaking loops saturated") put the repo in an explicit "harden
  only where pressured / do not build" posture. Campaign 1's closure
  (2026-09-02) states plainly: "No further product change is warranted by
  current evidence."

**Important qualifier the evidence forces:** the blocker is **not a repo-code
deliverable**. Issue #255 + the 2026-08-31 reassessment locate it precisely: an
isolated producer sub-agent cannot persist its own frozen brief to the expected
path, cannot prove pinned provenance (it read an un-pinned object store), and
cannot re-run the probe engine; a genuinely separate external process has no
independent credential. Three substrates falsified; an owner "halt Goal A in
this environment rather than build Harness v4" rule is in force. So the
warranted next action is an **owner/environment decision** (different host,
independent API credential, or explicit reversal of the halt rule) -- Issue
#255 says "no repo-code change is required" and forbids patch->rerun without
fresh owner authorization.

**If Goal A stays blocked**, the next-most-leverage *code/docs* work is small
and already enumerated by Campaign 1: the **nine workflow-system-disposition
owner decisions** in `docs/workflow-system-disposition.md` section 6 (foremost:
move `product-discovery-sprint` + `product-strategy-sprint` to
`compatibility_only` -- both route every step to a deprecated Skill), plus two
one-line test-expectation fixes (D2b `test_validate_brief_json.py`, D19
`test_validator_utils.py::test_load_workflow_registry_loads_yaml`), plus
operating the Issue #218 / #226 evidence lanes.

## 2. Decided / in-flight / deferred

### Decided / ratified (load-bearing)
- **ADR 0013** -- active coding agent owns the top-level control loop (Accepted).
- **ADR 0014** -- product boundary = validated, human-reviewed
  `repository_sensemaking_brief`; automatic downstream routing deferred
  (Accepted, narrowed, owner-ratified 2026-07-26).
- **ADR 0026 / 0027** -- execution authority separated from
  recommendation/selection; registry identity separated from liveness;
  consumers fail closed (Accepted 2026-08-24 / later).
- **ADR 0015 addendum** -- `representation_sufficiency` -> `MODEL_WARRANT` gate
  (Accepted; PR #242 "conditional representation warranting" merged 2026-08-29).
- **ADR 0023** -- two-lane experiment authorization (Accepted, independently
  reviewed).
- **ADR 0024 / 0025** -- extended-analysis field classification;
  orchestration-plan lifecycle (Accepted).
- **Goal A protocol v1.0 FINAL** -- canonical, owner-approved (amended
  2026-08-26 to independent-evaluator usefulness authority). A2
  deferred/unauthorized; Goal B / E3 frozen.
- **Campaign 1** (agent-native artifact-mediated self-development) --
  `CAMPAIGN_COMPLETE`; **PR #268 merged** (`06a57d1`). Its product-surface
  additions are now on `main`: `docs/workflow-system-disposition.md`, the
  continuation subsection in the operating map, the machinery+hooks disposition
  in `decision-orchestration-boundary.md`, truthful hook/`CLAUDE.md` text, the
  lazy `_validator_utils` resolver.
- **Rejected with reopen conditions** (Campaign 1): no continuation schema, no
  new validator, no new artifact type, no executable hook -- a Markdown-record
  convention was sufficient at this scale.

### In flight / in progress
- **Goal A / A1 episode execution** -- ACTIVE but *paused at the substrate
  boundary*; tracked in **Issue #255** (open); durable stop-boundary committed
  as Evidence 0023. Awaiting owner decision on execution environment.
- **Issue #218** -- standing normal-use control-model evidence lane; open, 2
  post-Path-4 episodes recorded, no recurring failure boundary yet, no machinery
  promotion.
- **Issue #226** -- blind C6R evidence/authority/verification gate-separation
  study; open, scenarios to be frozen, `C6R` not to be modified before the
  preregistered result.
- **Semantic Control Map trial** -- `docs/semantic-control-map.md` + trial
  protocol, EXPERIMENTAL, on `main` via PR #247/#251.
  `CORE_PERSISTENCE_RATIFIED = false`; termination 4-8 weeks from ~2026-08-31
  (min close ~2026-09-28); nothing may depend on the map.
- **Nine workflow-disposition owner decisions** -- recorded, none applied.
- **Campaign 2** (`docs/campaigns/durable-repo-self-development/`, 2 commits at
  HEAD) -- a new owner-launched campaign whose charter/state I was instructed
  not to read. Its existence means this reconstruction describes the
  *pre-Campaign-2* durable state.

### Deferred / explicitly out of scope
- **A2** (incremental value vs baseline) -- deferred until owner reviews A1.
- **Goal B / research-grade E3** -- frozen/deferred.
- **Automatic fog-type->implementation routing** as product behavior; universal
  centralized orchestrator; one workflow encoding the whole loop; automatic
  external-mutation authority -- all "not automatically ratified" (`CONTEXT.md`
  "Current product boundaries and open edges").
- **Domain-general control core / domain packs / decision-theory machinery** --
  research questions only, non-ratified (`control-model-research-agenda.md`;
  `CLAUDE.md`).
- **Routing / tracker-sync / deployment / multi-repo orchestration** -- out of
  scope (ADR 0014).
- **New validator/schema/hook/runtime machinery** -- behind the "repeated
  real-use pressure + mechanically expressible boundary" gate.
- **PyPI publication / GA / "production deployment"** -- the `roadmap.md` /
  `CHANGELOG.md` plan is stale and superseded (see section 4); ADR 0021
  "production readiness requirements" is SUPERSEDED, never Accepted.
- Test debt D8, D9, D11, D13, D17, D18 -- deferred, none in CI.

## 3. Files relied on, in order

1. `git log --oneline` + `gh pr list` / `gh issue list` -- established that
   Campaign 1 / PR #268 just merged and Campaign 2 just bootstrapped; only 3
   open issues, 1 stale draft PR.
2. `git show --stat` of the two HEAD commits -- confirmed the forbidden
   directory is the subject, scoped it out.
3. `STATUS.md` -- nominal "single living status summary"; gave Goal A as the
   priority.
4. `roadmap.md`, `goal.md`, `00-user-intent.md` -- two of three badly stale;
   `goal.md` gave the durable north-star framing.
5. `docs/campaigns/agent-native-self-development/FINAL-REPORT.md` -- freshest
   (2026-09-02) strategic narrative: what's ratified, what was demonstrated,
   what was rejected, what remains.
6. `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` --
   capability-state table with per-row evidence pointers; the single most useful
   "current state" surface I found.
7. `gh issue view 255 / 218 / 226` -- the three live workstreams and their
   exact boundaries.
8. `docs/research/goal-a-execution-readiness-reassessment-2026-08-31.md` -- most
   recent dated strategic doc; states the blocker and that it is not
   product-surface.
9. `CONTEXT.md` -- canonical architecture + "Current evidence strategy: Goal A"
   + non-ratified edges.
10. `docs/adr/0014-product-boundary.md` + `docs/adr/README.md` + ADR status
    sweep -- ratified scope; found 0017-0021 all SUPERSEDED/never-Accepted.
11. `CHANGELOG.md` -- stale (stops at 0.2.2, 2026-08-07).
12. `docs/research/control-model-research-agenda.md` -- non-ratified research
    paths; "don't build" discipline; "loops saturated" meta-finding.
13. `docs/semantic-control-map-trial.md` -- the one time-boxed experiment
    currently running.
14. `docs/agent-native-operating-workflow.md` (head) -- current operating map;
    confirms ADR 0013/0014 framing.
15. `docs/research/goal-a-external-product-validation-protocol.md` (head) --
    what A1 actually asks and its authorization state.

**Authoritative "where is development right now" surface:** there is no single
clean one. `STATUS.md` claims that role ("This file is the single living status
summary at the repo root") but it is thin, dated 2026-08-26, and already trails
the 2026-09-02 campaign closure and the 2026-08-31 reassessment. In practice the
current picture is reconstructable only by cross-reading
**`docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` (best single
artifact) + `CONTEXT.md` "Current evidence strategy" + the 2026-08-31 Goal A
reassessment + open issues #255/#218/#226**.

## 4. Stale / contradictory / untrustworthy

- **`roadmap.md`** -- severely stale. Header "Current Status: Phase 2.3
  Complete", "Current Version: 0.2.1 (Beta)", next step "Phase 3 -- Real-World
  CLI Testing", then a PyPI-publication -> GA plan. Contradicts `STATUS.md`
  (v0.2.2, Goal A), `CONTEXT.md`, and ADRs 0013-0027. Campaign 1 logged it as
  D3, disposition "no action" -- so it is knowingly left misleading.
- **`CHANGELOG.md`** -- stale. Last entry 0.2.2 / 2026-08-07; "Deployment
  Timeline" footer still lists Phase 2.2/2.3/3/4. None of the ADR 0013-0027
  work, Goal A, PHB, or the campaigns is reflected.
- **`00-user-intent.md`** -- stale. "Fix four structural gaps ... Framework
  ready for 3-week rollout plan starting Week 1." Pre-dates the agent-native
  pivot (ADR 0013).
- **`STATUS.md` "Current state" bullets** -- a dated snapshot (distribution-drift
  CRLF, "97 historical reports archived") that reads as *the* current state but
  predates the Goal A halt, Evidence 0023, and both campaigns.
- **User auto-memory `MEMORY.md`** (context, not a durable repo file, so not a
  source I leaned on) -- asserts "Phase 4 Complete -- PRODUCTION READY --
  APPROVED FOR DEPLOYMENT" and cites "ADR 0017 ... unmet external-repo readiness
  bar." Durable state contradicts both: ADR 0017 is **SUPERSEDED, never
  Accepted**; `CONTEXT.md` explicitly does *not* claim GA/production readiness.
  A maintainer trusting memory here would be badly misdirected.
- **ADRs 0017-0021** -- all "SUPERSEDED ... historical proposal, never
  Accepted." A reader who finds "ADR 0021 Production Readiness Requirements" or
  "ADR 0018 Workflow Routing Policy" by title, without reading the status line,
  would take dead proposals as decisions. The Goal A protocol itself calls out
  ADR 0021 as superseded.
- **`docs/` top level** -- ~45 loose `PHASE-*`, `STAGE-*`, `WEEK1-*`,
  `UI-ROUTING-*`, `task-*` files, mostly historical, not marked as archived (the
  real archive is `docs/archive/phase-reports/`). High noise; easy to anchor on
  the wrong era.
- **Repo working tree** (from the provided `git status`) -- large volume of
  untracked `experiments/`, `artifacts/`, `deepseek-harness/`, `.reasonix/`
  material not under version control; not durable, ignored for this exercise,
  but it makes the tree look busier/further-along than `main` is.
- **Grep leak (my error)** -- a broad pattern I ran matched
  `docs/campaigns/durable-repo-self-development/{OWNER-INSTRUCTION,CHARTER,CAMPAIGN-STATE,controllers/A-*}.md`
  and printed ~30 lines. I did not open those files or rely on them; the visible
  lines (STATUS.md is the closest surface; "there is no product representation
  of current highest-leverage ...") were consistent with what I had already
  independently concluded. Flagging it for transparency.

## 5. Confidence and gaps

**Confidence in section 1: moderate-to-high on the *what*, lower on the *shape*.**
- High: "Goal A / A1 external product validation is the named single
  highest-value product-validation workstream, and it is substrate-blocked" --
  stated in 4+ mutually consistent durable places, none contradicting.
- Lower: whether that is a "*development* boundary" at all. The blocker is
  explicitly owner/environment, not code (Issue #255); and the freshest campaign
  doc says no further product change is warranted. So the honest answer carries
  a fork: either "there is no large code deliverable -- the warranted move is an
  owner decision + running the #218/#226 evidence lanes + the nine disposition
  cleanups," or "the owner picks a substrate and the deliverable is a corrected
  isolated-producer harness." Durable evidence leans to the former.

**What I could not determine from durable evidence (a maintainer would need
these):**
- The status of the Issue #255 owner decision -- has the owner chosen a host /
  credential path / reversed the halt? Nothing durable post-dates the question.
- Whether any of the nine `workflow-system-disposition.md` section 6 owner
  decisions have been made since PR #268 ("none applied" as of merge; no later
  signal).
- Real external demand / pull. There is zero evidence of an outside user waiting
  on this; Goal A is a *constructed* validation, not observed need. Whether the
  product should be validated vs. re-scoped depends on information not in the
  repo.
- What Campaign 2 (`docs/campaigns/durable-repo-self-development/`) has decided
  -- by construction I could not read it. If it has selected a direction, it
  supersedes this reconstruction, which is explicitly of the pre-Campaign-2
  state at `06a57d1`.
- Whether the `semantic-control-map` trial has accumulated enough real activity
  to close with a verdict rather than `INSUFFICIENT_ACTIVITY`.

## 6. Cost

- **Tool calls:** ~22 (8 Bash for git/gh/ls/status sweeps, 1 Grep, 13 Read).
- **Distinct durable documents opened:** ~16 read in full or part (`STATUS.md`,
  `roadmap.md`, `goal.md`, `00-user-intent.md`, `CONTEXT.md`, `CHANGELOG.md`,
  `FINAL-REPORT.md`, campaign-1 `CAMPAIGN-STATE.md`, Goal A reassessment, Goal A
  protocol head, ADR 0014, ADR README, `control-model-research-agenda.md`,
  `semantic-control-map-trial.md`, operating-map head), plus 3 GitHub issues,
  plus an ADR-status sweep over 27 files and directory listings touching ~40
  more filenames.
- To a *defensible* answer: ~15 calls (through the campaign-1 docs + the three
  issues + the Goal A reassessment). The last ~7 were confirmation and
  staleness-mapping.

**Honest experience:** the strategic *headline* is reconstructible and
consistent once you find the right four documents -- but the repo does not make
that easy. The nominal status file is stale and thin, three root orientation
files (`roadmap.md`, `CHANGELOG.md`, `00-user-intent.md`) actively point at a
superseded PyPI/GA plan, ~45 loose historical `docs/` files add noise, and the
actual current state lives in a campaign subdirectory and in GitHub issues
rather than on the documented "source-of-truth map." A fresh maintainer who
trusted `roadmap.md` or the auto-memory would draw the wrong conclusion; one who
found `docs/campaigns/agent-native-self-development/CAMPAIGN-STATE.md` and Issue
#255 would get there in about fifteen minutes.
```
