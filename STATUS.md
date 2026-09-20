# Status

**Source version:** 1.0.0rc3.dev0
**Release target:** 1.0.0rc3 (development; not yet a frozen candidate)
**Last updated:** 2026-09-20  
**Current phase:** Issue #416 Strategic Continuity, Reconciliation & Multi-Repository Sensemaking v1 is owner-authorized and active. Package A — Strategic Continuity & Currentness is the current bounded responsibility. Strategic Repository Sensemaking v1 and Policy Hierarchy Completion v0 remain complete/integrated/composable; synthetic StrategicPlanner testing remains stopped.  
**Policy Hierarchy state:** Policy Hierarchy Completion v0 is complete/integrated/composable.  
**Primary program:** agent-native repository decision support with agent-owned semantic judgment, explicit warrant/evidence/authority boundaries, optional durable Campaign state, reconstructible higher-scope strategic decisions, and guidance-first practical agent control  
**Current implementation frontier:** use Git `main` HEAD as exact repository identity; this projection intentionally does not self-pin a commit that becomes stale when it changes

**Release status:** historical `1.0.0rc1` was exact-head-qualified at `70542d47412d98ee6dfae5de6df29bf271304568`. Qualified `1.0.0rc2` is frozen at integrated commit `c9b86138d3919c4fce87040f14161364a0c1c3a0`, Git tree `2da97295576b2dc68b3fa3eaed626a70343dd387`. Current development has moved to `1.0.0rc3.dev0` targeting `1.0.0rc3`; RC2 qualification does not transfer to these later bytes. PyPI publication and final `1.0.0` remain separate owner-controlled transitions. Native harness, portability, and semantic usefulness claims remain excluded from the reduced-scope support promise.
Release scope and support claims: `docs/release-v1.0-contract.md`.

`STATUS.md` is the **current Level-3 strategic projection**, not the complete historical development ledger. Detailed qualification and decision history lives in linked handoffs, ADRs, dated audits, and Git/PR history.

## Strategic Repository Evolution state — Level 3

### Current product strategy

- **Level-4 authority:** `docs/product-strategy.md`.
- **Control model:** `docs/strategic-outer-loop.md`.
- **Level-3 contract:** `docs/strategic-state-contract.md`.
- **Level-4 revision contract:** `docs/product-thesis-revision.md`.
- **Current product-boundary authority:** `docs/adr/0029-current-product-boundary.md`; ADR 0014 is historical/superseded.
- **Product purpose:** improve repository-level decisions when a capable coding agent cannot safely determine the correct next engineering responsibility from the user request alone.
- **Primary persona:** high-delegation agent-assisted builder / repository owner; beginner-first, expert-capable.
- **Strategic design principle:** opinionated about engineering invariants, adaptive about process, progressive in disclosure.
- **Control law:** lower levels may execute higher-level commitments but may not silently redefine them.
- The four-level architecture remains **Version v0** and a **frozen operational baseline**; Strategic Outer Loop Precision v1 clarifies its reasoning and transition semantics without creating a new planner/runtime.

### Current capability state

The repository-qualified baseline includes:

- Campaign/Responsibility/Authority semantics, artifact admission, transitions, reconciliation, handoff/resume, target identity, observability, provenance, portability, preflight, Doctor, completion/archive, inventory, portable rebinding, and explicit multi-repository target/dependency mechanics;
- Resume Capsule v1/v2, capability context, uncertainty history/relationships, bundle inspection, and static Agent Workflow / Golden Path guidance;
- Strategic Outer Loop inspect/diff and explicit Level-3-to-Campaign handoff without semantic selection;
- **Strategic Decision to Support** plus qualitative frontier-comparison lenses and smallest-warranted-intervention reasoning at Level 3;
- **Thesis Tension**, dependency-sensitive review hold, and mandatory post-Level-4 reconciliation semantics;
- Semantic Architecture Reasoning Model integration across Levels 3 and 4 while preserving `semantic layer != control level`;
- strategic-state mechanical validation for the Strategic Decision anchor and current ADR 0029 pointer only; decision quality/ranking remains semantic;
- Semantic Architecture B1-B7 mechanical substrate, conformance, reference audit, Skill manifests, Domain Packs, and Product Management Waves 1-6;
- Persona & Adaptive Guidance Model v0 plus shipped-guidance reconciliation;
- **Campaign schema v2**; newer target/relation/completion records remain additive companions rather than alternate truth systems.
- **General Agency Model v0.1** research reference: value → context → strategy → decision frame → epistemic state → sufficiency → inquiry/choice → action → observation/verification → impact/sensemaking → belief update, with lateral challenge/exploration and explicit authority/risk/resource envelopes.
- **Practical Agent Architecture v0** guidance: semantic agent judgment → target-specific warrant → existing durable decision substrate → deterministic assurance → external execution/orchestration → evidence return and semantic reassessment.
- **Policy Hierarchy v0**: canonical middle-control architecture for Strategic → Inquiry → Metareasoning → Exploration → Warrant/Choice → Action/Evidence → Learning/Reconciliation, explicitly defined as semantic policy contracts rather than runtime services.
- **Inquiry Policy v0**: agent-facing contract for deciding what to learn next, including `NO_INQUIRY_NEEDED`, smallest-sufficient-evidence selection, owner-intent/external-evidence boundaries, and inquiry stop conditions without new schema/state.
- **Metareasoning Policy v0**: agent-facing qualitative control-move contract for allocating effort among `ACT / INQUIRE / CHALLENGE / EXPLORE / VERIFY / ESCALATE / STOP` without a runtime controller, score, or authority expansion.
- **Exploration Policy v0**: agent-facing iterative-search allocation over `EXPLOIT / EXPLORE / CHALLENGE / DIAGNOSE / RECOMBINE / RESTART / VERIFY / EXIT_SEARCH`, with search history treated as an existing-evidence projection rather than a SearchState schema.
- **Warrant / Choice Policy v0**: target-specific, defeasible adjudication for claims/responsibilities/actions/continuation/closure/protected transitions/strategic directions, preserving `warrant != authority`, target-specific evidence, and valid `NO_SELECTION` without a WarrantEngine.
- **Learning / Reconciliation Policy v0**: evidence-return semantic reconciliation across claims, uncertainty, responsibility, continuation/closure, and strategic/thesis state, with valid `NO_MODEL_CHANGE` and no generic belief database or automatic state mutation.
- **Stable Strategic Alternatives surface**: Strategic Repository Sensemaking v1 now represents 0–5 materially real construction paths; zero paths is valid when no coherent construction trajectory is currently warranted/representable, while `BUILD` still requires a selected real path.
- **Adaptive Policy Coordinator v0**: progressive semantic policy composition that activates only decision-relevant policy questions, allows zero explicit policy layers for obvious bounded work, and adds no routing/runtime/coordinator-state authority.
- Canonical `using-sensemaking` guidance now makes warrant targets/dependencies, challenge versus exploration, resource-aware stopping, and delegated-result evidence return explicit while preserving progressive disclosure.
- **Release Authority Auditor**: `release audit` reconciles local release identity/Git/docs/workflow mechanics without asserting CI qualification, publication, semantic truth, or owner authorization.
- **Execution Interface v1**: additive execution handoff/result companions bind already-selected responsibility, authority, exact targets, evidence requirements, returned worker claims, and append-only integrity without changing Campaign schema v2.
- **High-delegation working context**: `campaign working-context` projects current responsibility/decision/authority/uncertainty/targets/evidence/stop conditions and latest worker exchange without recommending a next action.
- **External executor interchange / AI Software Factory bridge**: generic integrity-bound handoff/result envelopes plus a caller-selected factory GitHub-Issue/command projection; no workflow selection, publication, scheduling, worker allocation, merge, or deploy authority.
- **Explicit GitHub provenance publication**: preview-by-default, explicit-`--publish` Issue/PR comments with deterministic markers and duplicate suppression.
- **Cross-repository execution projection**: explicit ordering relations become read-only prerequisite edges/layers; the projection is not an execution plan and same-layer membership does not authorize parallel work.
- **Strategic Continuity v1 — PACKAGE A IN CONSTRUCTION:** additive strategic-analysis lineage, decision assumptions, reassessment triggers, and deterministic `strategy` projections are being implemented under Issue #416 without creating a planner or alternate strategic truth system.

Detailed milestone evidence is preserved in `docs/strategic-outer-loop-precision-v1-handoff.md`.
Policy Hierarchy Completion v0 closeout is summarized in `docs/policy-hierarchy-completion-v0-handoff.md`.

### Material limitations and evidence ceilings

- Repository qualification does not establish native-harness usefulness, genuine second-harness portability, comparative superiority, product-market value, or general autonomous software-development capability.
- No new empirical/native-harness experiment was required or performed for Strategic Outer Loop Precision v1; missing empirical proof remains missing.
- The active agent owns semantic frontier, Strategic Decision, comparison, responsibility, capability, thesis-tension, escalation, reconciliation, and stopping judgments. Deterministic machinery validates only mechanically decidable representation/integrity.
- The current Version 1.0 target architecture preserves the **product/lab split**; retained lab evidence does not become shipped-product authority.
- The package includes the **real-harness qualification verifier**, but verifier mechanics do not manufacture real-harness evidence or semantic truth.
- ADR 0029 establishes the current broader product boundary around already integrated decision-support/control surfaces; it does not retroactively broaden historical Goal A evidence or claim ceilings.
- Multi-repository Campaign mechanics do not provide cross-repository transactional commit/deploy/rollback atomicity or automatic repository discovery.
- Qualitative frontier lenses do not establish an objective priority function. `qualitative comparison != deterministic ranking`.
- `Thesis Tension` does not imply Level-4 review, and current mechanics do not automatically infer whether work depends semantically on a challenged thesis.
- General Agency Model v0.1 is a bounded research/reference abstraction, not proof of a universal theory of intelligence, comparative superiority, or domain-general product value.
- Practical Agent Architecture v0 is currently guidance-first. Its reconciliation disposition is `GUIDANCE_ONLY_WARRANTED`; no new runtime, schema, public API, generic state store, or deterministic semantic controller was established as necessary.
- Strategic Continuity currentness checks may establish source/evidence drift only; `drift detected != strategy invalid != reanalysis automatically required`.

### Strategic Frontier

Current material frontier items are:

1. **Product Boundary Reconciliation v1 — COMPLETE / OWNER_RATIFIED / INTEGRATED.** ADR 0029 is current product-boundary authority; ADR 0014 remains historical evidence.
2. **Level-3 Strategic Decision Model v1 — COMPLETE / INTEGRATED.** Strategic Decision to Support, qualitative comparison, decision-changing uncertainty, and smallest warranted intervention are explicit without scoring/ranking automation.
3. **Level-3 Durable State Refinement v1 — COMPLETE / INTEGRATED.** `STATUS.md` is a concise current projection with linked historical evidence.
4. **Thesis Tension and Level-3/Level-4 Transition Semantics — COMPLETE / INTEGRATED.** Repeated weak thesis signals can be preserved without auto-escalation; active review uses dependency-sensitive hold and mandatory downstream reconciliation.
5. **Semantic Reasoning Model Integration — COMPLETE / INTEGRATED.** The evidence-to-decision grammar is explicitly instantiated at Levels 3 and 4 without collapsing authority scopes.
6. **Mechanical Contract Reassessment — COMPLETE / INTEGRATED / REPOSITORY_QUALIFIED.** Only the Strategic Decision heading and ADR 0029 pointer/projection were mechanized; semantic decision quality remains agent-owned.
7. **Strategic Reassessment & Closeout — COMPLETE / HISTORICAL SCOPE CLOSEOUT.** That architecture milestone found no further architecture construction boundary; the later Release Authority & Operational Coherence repair is a separately evidenced currentness/release responsibility, not a reopening of the architecture program.
8. **Native-harness / empirical portability qualification — DEFERRED BY OWNER DIRECTION.** Existing protocols remain valid; no new run is a prerequisite for repository construction.
9. **Progressive Campaign rigor tiers — DEFERRED / REQUIRES EVIDENCE.** Existing proportional mechanics/guidance do not warrant alternate runtime truth systems or thresholds.
10. **Cross-repository transaction/deployment coordination — DEFERRED / NOT AUTHORIZED.** Current multi-repository scope intentionally stops before transaction orchestration.
11. **Level-4 reconciliation automation / automatic strategic planning — DEFERRED / NOT AUTHORIZED.** Current semantic authority remains with the agent/owner.
12. **Sensemaking Protocol / product-category expansion — LONG_HORIZON / REQUIRES_LEVEL_4_REVIEW.** No independent consumer currently warrants a product-category pivot.
13. **General Agency Model v0.1 — COMPLETE / RESEARCH_REFERENCE.** The broader value-to-action-to-learning grammar is coherent with current Sensemaking but does not change ADR 0029 or authorize a generic agent product/runtime.
14. **Practical Agent Architecture v0 — COMPLETE / GUIDANCE_ONLY_WARRANTED / INTEGRATED.** The warrant-centered hybrid design reconciled against current Sensemaking without establishing a state, schema, assurance, runtime, or public-API gap; compact guidance is integrated into `using-sensemaking`.
15. **Normal-use validation — ACTIVE / SUPPORTING EVIDENCE MODE.** Preserve qualifying real episodes and use the execution interfaces during ordinary consequential repository work; it no longer blocks construction explicitly authorized under Issue #399.
16. **Execution Interface & Agent-Factorization v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF.** Release-authority audit, execution handoff/result, working-context projection, generic executor interchange, AI Software Factory projection, explicit GitHub provenance publication, and cross-repository execution projection are integrated without adding semantic planning/scheduling authority. Feature-integrated `main@4f89e92030af4dee5c931b59b839869911e6c366` passed Product/Lab/Release Distribution validation; PR #394 / Issue #393 carry the terminal closeout qualification/result receipt.
17. **Experimental Intelligence Components v0 — DEFERRED / LAB_ONLY / `RESEARCH_MORE` / SYNTHETIC TESTING STOPPED.** StrategicPlanner v0 under Issue #395 remains historical lab evidence at its original claim ceiling. It is not an active construction or experiment program and is not promoted by Strategic Repository Sensemaking v1.
18. **Policy Hierarchy Completion v0 — COMPLETE / INTEGRATED / COMPOSABLE.** Issue #399's seven bounded packages are implemented: Inquiry, Metareasoning, Exploration, Warrant / Choice, Learning / Reconciliation, the stable Strategic Alternatives surface, and Adaptive Policy Coordinator v0. Policy layers remain agent-owned, zero-work-capable, non-mandatory, non-routing, and authority-preserving.
19. **Strategic Repository Sensemaking v1 — COMPLETE / INTEGRATED / NORMAL_USE_HANDOFF.** Issue #401 established a first-class Level-3 analysis surface that turns repository evidence into a current-system model, capability/limitation map, 0–5 materially real construction paths, qualitative comparison, decision-changing uncertainty, strategic synthesis, and a warranted direction/inquiry/no-change disposition without building a deterministic StrategicPlanner. Package A integrated via PR #403, Package B via PR #404, and PR #409 stabilized the Strategic Alternatives representation without changing the milestone boundary.
20. **Post-closeout strategic-state reconciliation — COMPLETE / NORMAL_USE_EVIDENCE.** Issue #414 used Strategic Repository Sensemaking v1 in ordinary repository operation, identified only stale post-#401 currentness as repository-local work, and reconciled the stable Level-3 projection without promoting a new product package.
21. **Strategic Continuity, Reconciliation & Multi-Repository Sensemaking v1 — ACTIVE / OWNER_AUTHORIZED.** Issue #416 explicitly authorizes four bounded construction packages. Package A adds strategic-analysis continuity metadata and deterministic currentness/projection surfaces; later packages add reconciliation/reserved-decision artifacts, caller-selected multi-repository strategic sensemaking, and change-impact/product UX. No experiment prerequisite applies.

### Current highest-leverage boundary

**Strategic Continuity & Currentness — Package A of Issue #416.**

The first normal-use Strategic Repository Sensemaking episode (#414/#415) exposed a concrete continuity/currentness pressure: the repository's immutable strategic analysis and its current Level-3 projection can diverge after later integration, requiring manual reconstruction.

Owner direction now explicitly promotes that pressure into bounded construction:

```text
immutable strategic analysis
-> explicit lineage / continuation
-> decision assumptions + reassessment triggers
-> deterministic compare/currentness projection
-> semantic reassessment only when the agent judges it warranted
```

This package reuses `strategic_repository_analysis`; it does not introduce a second strategic state model.

### Current strategic decision to support

**Decision:** how can later repository evolution remain reconstructibly connected to prior strategic analyses without turning currentness detection into automatic strategic planning?

**Current judgment:** **BUILD / STRATEGIC_CONTINUITY_V1_PACKAGE_A.**

The smallest warranted intervention is additive metadata plus deterministic projections:

- optional stable `analysis_ref`;
- explicit semantic continuity relation to a prior analysis;
- decision assumptions and reassessment triggers;
- path-level assumptions/triggers;
- root `strategy inspect|paths|uncertainty|assumptions|compare|drift` CLI projections.

### Current decision-changing uncertainty

The principal implementation uncertainty is mechanical: whether the additive continuity fields and root strategy projections can be integrated while preserving all existing Strategic Repository Sensemaking v1 contracts and release qualification.

No empirical/model-comparison inquiry is required. Exact-head Product Validation and Release Candidate Distribution are the package qualification gates.

### Current warranted repository-level responsibility

**Implement and qualify Package A — Strategic Continuity & Currentness.**

Level-3 disposition: `BUILD`.

```text
CURRENT CONSTRUCTION RESPONSIBILITY = STRATEGIC_CONTINUITY_CURRENTNESS_V1
PRIMARY CONSTRUCTION PROGRAM = ISSUE_416_STRATEGIC_CONTINUITY_RECONCILIATION_MULTI_REPO_V1
ACTIVE PACKAGE = A_STRATEGIC_CONTINUITY_CURRENTNESS
STRATEGIC_REPOSITORY_SENSEMAKING_V1 = COMPLETE_INTEGRATED_NORMAL_USE_HANDOFF
POLICY_HIERARCHY_COMPLETION_V0 = COMPLETE_INTEGRATED_COMPOSABLE
SUPPORTING EVIDENCE MODE = NORMAL_USE_VALIDATION
EXPERIMENT PREREQUISITE = NONE
SYNTHETIC STRATEGICPLANNER TESTING = STOPPED
```

Issue #384 remains the separate external GitHub-admin branch/ruleset governance action; Issue #416 does not absorb or fabricate that hosting-layer transition.

### Active execution vehicle

Package A branch:

```text
work/strategic-continuity-v1-package-a
```

Issue #416 is the owner-authorized umbrella construction record.

### Expected evidence and reassessment

Package A must demonstrate:

- existing `strategic_repository_analysis` artifacts remain valid;
- continuity/assumption metadata is mechanically validated when present;
- `strategy compare` projects declared change without ranking;
- `strategy drift` reports mechanically observable source/evidence currentness without declaring strategy invalid;
- no Campaign schema change, planner runtime, automatic reanalysis, or authority expansion occurs;
- exact Package-A head passes Product Validation and Release Candidate Distribution;
- the integrated Package-A tree passes the same product/release gates before Package B becomes current.

### Authority / owner direction

The owner explicitly authorized Policy Hierarchy Completion v0 under Issue #399 and directed the repository to stop synthetic experiments as the active development mode. The owner subsequently authorized Strategic Repository Sensemaking v1 under Issue #401 and explicitly directed the repository to build the strategic-analysis layers without another experiment gate. The owner now explicitly authorizes Issue #416 to implement the full Strategic Continuity / Reconciliation / Multi-Repository / Change-Impact package set sequentially without another approval pause.

Policy Hierarchy Completion v0 has integrated the full owner-authorized bounded package set:

```text
Inquiry Policy v0
Metareasoning Policy v0
Exploration Policy v0
Warrant / Choice Policy v0
Learning / Reconciliation Policy v0
stable Strategic Alternatives surface
Adaptive Policy Coordinator v0
```

No remaining Issue #399 construction package is selected. These integrated capabilities remain bounded by the existing product strategy, ADR 0029, semantic-agent ownership, and protected external-action boundaries.

Current authority does **not** include:

```text
generic AgentState
generic memory/search database
Campaign schema v3 merely to mirror policies
numeric inquiry/warrant/priority/intelligence scores
deterministic semantic routing
automatic Skill/workflow/Campaign selection
OuterLoopEngine finite-state runtime
automatic Level-4 thesis revision
cross-repository transaction/deployment coordinator
automatic strategic reanalysis from drift detection
automatic repository discovery/scope expansion
autonomous merge/release/deployment/publication authority
PyPI publication or final 1.0
```

The earlier StrategicPlanner lab evidence remains valid at its stated ceiling. Additional synthetic StrategicPlanner testing is stopped unless separately re-authorized for a new decision-changing reason.

### Thesis review state

`THESIS_REVIEW_REQUIRED`: **NO**.

The product-boundary tension that opened this milestone was resolved through the owner-ratified Level-4 `SUPERSEDE` disposition and ADR 0029. Packages 2–6 produced no new decision-changing contradiction in product purpose, primary user, JTBD, value proposition, strategic non-goals, current product boundary, or evidence ceilings.

No current Thesis Tension is promoted into active review.

## Current next step

**QUALIFY AND INTEGRATE ISSUE #416 PACKAGE A — STRATEGIC CONTINUITY & CURRENTNESS.**

Merge Package A only after its exact head passes Product Validation and Release Candidate Distribution. Verify the integrated tree and record the qualification receipt on Issue #416.

After successful integration, proceed directly to Package B — Strategic Reconciliation & Reserved-Decision Surfaces — without reopening an experiment gate or waiting for another approval.

Current release source remains `1.0.0rc3.dev0` targeting `1.0.0rc3` in `development`. Do **not** freeze RC3, publish to PyPI, tag a release, or advance to final `1.0.0` as part of Issue #416.
