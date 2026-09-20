# Status

**Source version:** 1.0.0rc3.dev0
**Release target:** 1.0.0rc3 (development; not yet a frozen candidate)
**Last updated:** 2026-09-19  
**Current phase:** Strategic Repository Sensemaking v1 is active under Issue #401; Package A is integrated and Package B is constructing first-class repository-evolution path synthesis. Policy Hierarchy Completion v0 remains composable under Issue #399, with Inquiry Policy v0 integrated. Synthetic StrategicPlanner testing remains stopped as the active mode.  
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
- Canonical `using-sensemaking` guidance now makes warrant targets/dependencies, challenge versus exploration, resource-aware stopping, and delegated-result evidence return explicit while preserving progressive disclosure.
- **Release Authority Auditor**: `release audit` reconciles local release identity/Git/docs/workflow mechanics without asserting CI qualification, publication, semantic truth, or owner authorization.
- **Execution Interface v1**: additive execution handoff/result companions bind already-selected responsibility, authority, exact targets, evidence requirements, returned worker claims, and append-only integrity without changing Campaign schema v2.
- **High-delegation working context**: `campaign working-context` projects current responsibility/decision/authority/uncertainty/targets/evidence/stop conditions and latest worker exchange without recommending a next action.
- **External executor interchange / AI Software Factory bridge**: generic integrity-bound handoff/result envelopes plus a caller-selected factory GitHub-Issue/command projection; no workflow selection, publication, scheduling, worker allocation, merge, or deploy authority.
- **Explicit GitHub provenance publication**: preview-by-default, explicit-`--publish` Issue/PR comments with deterministic markers and duplicate suppression.
- **Cross-repository execution projection**: explicit ordering relations become read-only prerequisite edges/layers; the projection is not an execution plan and same-layer membership does not authorize parallel work.

Detailed milestone evidence is preserved in `docs/strategic-outer-loop-precision-v1-handoff.md`.

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
17. **Experimental Intelligence Components v0 — ACTIVE / LAB_ONLY / `RESEARCH_MORE`.** Owner direction authorizes cheap, reversible experiments rather than core promotion. StrategicPlanner v0 under Issue #395 compiles baseline/treatment packets and preserves semantic decision authority with the active agent. Initial retrospective dogfood shows a plausible benefit on ambiguous high-leverage decisions and disproportionate ceremony on a tiny bounded repair; this supports prospective testing of an activation boundary, not product promotion or automatic planning.
18. **Policy Hierarchy Completion v0 — ACTIVE / OWNER_AUTHORIZED / COMPOSABLE.** Issue #399 authorizes the missing middle semantic-control layers. Inquiry Policy v0 is integrated; later Metareasoning, Exploration, Warrant/Choice, Learning/Reconciliation, stable Strategic Alternatives, and adaptive coordination remain authorized follow-ons. Policy layers remain agent-owned, zero-work-capable, and non-mandatory.\n19. **Strategic Repository Sensemaking v1 — ACTIVE / OWNER_AUTHORIZED / CONSTRUCTION.** Issue #401 authorizes a first-class Level-3 analysis surface that turns repository evidence into a current-system model, capability/limitation map, coherent construction paths, qualitative comparison, decision-changing uncertainty, strategic synthesis, and a warranted direction/inquiry/no-change disposition without building a deterministic StrategicPlanner.

### Current highest-leverage boundary

**Strategic Repository Sensemaking v1 — first-class repository evolution analysis.**

The owner explicitly authorized construction under Issue #401 and removed any requirement for another synthetic experiment before building it.

The current gap is not that Sensemaking lacks Level-3 concepts. The repository already has repository diagnosis, Strategic Frontier, Strategic Decision to Support, qualitative comparison, decision-changing uncertainty, Inquiry Policy v0, and bounded execution. The missing product layer is a coherent first-class analysis surface that composes those pieces into explicit repository-evolution paths.

Policy Hierarchy Completion v0 remains valid and composable. Inquiry Policy v0 is already integrated and may govern whether a path-distinguishing uncertainty deserves investigation. This milestone does not cancel Issue #399; it applies those semantic-control contracts to a concrete Level-3 product surface.

Issue #384 remains an external GitHub-admin governance action and is unrelated to this construction responsibility.

### Current strategic decision to support

**Decision:** can Sensemaking turn current repository evidence and governing intent into a reconstructible strategic decision space—current system, capability state, plausible construction paths, qualitative tradeoffs, decision-changing uncertainty, and warranted direction—without becoming a deterministic strategy engine?

**Current judgment:** **YES / BUILD STRATEGIC REPOSITORY SENSEMAKING V1.**

Owner direction resolves whether to build this capability. The smallest warranted product shape is an artifact-first semantic Skill with bounded mechanical validation, not a planner runtime, scoring function, Campaign schema change, or automatic implementation pipeline.

### Current decision-changing uncertainty

**Contract sufficiency:** can a stable strategic-analysis artifact represent capability states, construction paths, path comparison, and strategic disposition strongly enough to support fresh-context continuation while keeping semantic quality agent-owned?

This uncertainty is resolved through ordinary implementation/contract qualification, not a synthetic experiment. If the contract requires numeric scoring, automatic ranking, generic AgentState, or a new semantic runtime to function, stop and redesign rather than expanding machinery.

### Current warranted repository-level responsibility

**Implement and qualify Strategic Repository Sensemaking v1 under Issue #401.**

Current bounded package: **Package B — Construction Path Synthesis & Product Integration**.

Package A is integrated through PR #403 with exact qualified content.

Required intervention:

- strengthen construction-path distinctness, capability grounding, coarse sequencing, and anti-backlog semantics;
- distinguish diagnostic `repo-sensemaker` from Level-3 `strategic-repository-analysis`;
- integrate first-class strategic analysis into `using-sensemaking` and the Strategic Outer Loop;
- expose the high-level repository-evolution entry point in README / Getting Started;
- add integration regressions proving strategic analysis does not become automatic task selection, numeric ranking, or implementation authority;
- preserve Inquiry Policy v0 as a composable semantic policy for path-distinguishing uncertainty.

Level-3 disposition: `STRATEGIC_REPOSITORY_SENSEMAKING_CONSTRUCTION_ACTIVE`.

```text
CURRENT CONSTRUCTION RESPONSIBILITY = STRATEGIC_PATH_SYNTHESIS_INTEGRATION
PRIMARY CONSTRUCTION PROGRAM = STRATEGIC_REPOSITORY_SENSEMAKING_V1
COMPOSABLE POLICY PROGRAM = POLICY_HIERARCHY_COMPLETION_V0
EXPERIMENT PREREQUISITE = NONE
SUPPORTING EVIDENCE MODE = NORMAL_USE_VALIDATION
```

### Active execution vehicle

Issue #401 is the current milestone authority tracker.

Current branch: `work/strategic-repository-sensemaking-v1-contract`.

Package sequence:

1. Strategic Analysis Contract;
2. Strategic Repository Analysis Skill semantics and path synthesis;
3. product integration / currentness / closeout.

Issue #399 remains authorized for later policy-layer continuation; no synthetic StrategicPlanner experiment is required by either program.

### Expected evidence and reassessment

Package A should produce:

- canonical strategic-analysis product contract;
- first-class Skill + template + manifest;
- artifact/domain/registry/release integration;
- validator regression coverage;
- exact-head Product Validation and Release Candidate Distribution qualification.

After Package A integrates:

- proceed directly to construction-path synthesis/comparison semantics if the artifact composes without runtime/schema expansion;
- stop and redesign if the capability only works by introducing deterministic strategy ranking, mandatory numeric scoring, or hidden implementation authority;
- do not manufacture an empirical study before Package B.

### Authority / owner direction

The owner explicitly authorized Policy Hierarchy Completion v0 under Issue #399 and directed the repository to stop synthetic experiments as the active development mode. The owner subsequently authorized Strategic Repository Sensemaking v1 under Issue #401 and explicitly directed the repository to build the strategic-analysis layers without another experiment gate.

Current construction authority includes bounded implementation of:

```text
Inquiry Policy v0
Metareasoning Policy v0
Exploration Policy v0
Warrant / Choice Policy v0
Learning / Reconciliation Policy v0
stable Strategic Alternatives surface
Adaptive Policy Coordinator v0
```

Each follow-on package remains bounded by the existing product strategy, ADR 0029, semantic-agent ownership, and protected external-action boundaries.

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
autonomous merge/release/deployment/publication authority
PyPI publication or final 1.0
```

The earlier StrategicPlanner lab evidence remains valid at its stated ceiling. Additional synthetic StrategicPlanner testing is stopped unless separately re-authorized for a new decision-changing reason.

### Thesis review state

`THESIS_REVIEW_REQUIRED`: **NO**.

The product-boundary tension that opened this milestone was resolved through the owner-ratified Level-4 `SUPERSEDE` disposition and ADR 0029. Packages 2–6 produced no new decision-changing contradiction in product purpose, primary user, JTBD, value proposition, strategic non-goals, current product boundary, or evidence ceilings.

No current Thesis Tension is promoted into active review.

## Current next step

**IMPLEMENT AND QUALIFY STRATEGIC ANALYSIS CONTRACT — PACKAGE A.**

Complete the first-class `strategic_repository_analysis` artifact/Skill/validator integration under Issue #401, qualify the exact PR head, and integrate if the surface remains semantic-agent-owned and mechanically bounded.

Then proceed directly to Package B — construction-path synthesis, qualitative comparison, and strategic synthesis semantics — without opening another experiment.

Policy Hierarchy Completion v0 remains composable follow-on work; Inquiry Policy v0 is already available to Strategic Repository Sensemaking when a path-distinguishing uncertainty warrants evidence.

Current release source remains `1.0.0rc3.dev0` targeting `1.0.0rc3` in `development`. Do **not** freeze RC3, publish to PyPI, or advance to final `1.0.0` merely because this milestone is under construction.

GitHub branch/ruleset protection remains external Issue #384. Do not claim it is enforced until the hosting setting actually exists.
