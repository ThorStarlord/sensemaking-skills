# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** PM upstream source-methodology migration complete at repository qualification; Semantic Architecture Phase 10 complete with Outcome A; engineering and PM empirical external qualification remain pending  
**Primary program:** Sensemaking Campaign productization with agent-agnostic domain capabilities and evidence-governed repository reasoning  
**Current implementation frontier:** Use Git `main` HEAD as exact repository identity; this status file intentionally does not self-pin a commit that becomes stale when the file itself changes  
**Current semantic frontier:** no later semantic phase is automatically authorized; the next package must be triggered by observed repository/product pressure  
**Current PM frontier:** Waves 1–6 are `REPOSITORY_QUALIFIED`; the pinned 27-command source migration is complete and the next PM frontier is native-harness/portability qualification plus evidence-derived product improvement

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. Its Campaign substrate supports agent-agnostic Product Management capabilities and an evidence-governed Semantic Architecture for consistent repository reasoning. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, target identity, evidence binding, and reconstructible state.

## Semantic Architecture maturity

PR #314 established the documentation-first semantic foundation. PR #318 completed the first contrasting **Reasoning Model Operationalization & Skill Semantic-Alignment** milestone. PR #323 completed the bounded Phase 10 real-repository common-envelope experiment.

The architecture has four explicit layers:

```text
Semantic Model
  = what entities, relations, and epistemic statuses mean

Reasoning Model
  = how observations become evidence, claims, uncertainty,
    responsibility, capability use, validation, and decisions

Capability / Skill Layer
  = bounded semantic work performed by repo-sensemaker,
    architectural-review, repair-verifier, output-reconciler,
    and domain Skills

Executable Substrate
  = mechanically decidable contracts, probes, validators,
    Campaign persistence, provenance, and handoff
```

The formalization ladder remains:

```text
Level 1 — Vocabulary
Level 2 — Ontology
Level 3 — Executable semantic contract
```

A Level-1/2 concept is not runtime authority. Level-3 promotion requires demonstrated cross-workflow reuse, stable semantics, a mechanically expressible subset, rejection coverage, and preservation of the agent/deterministic authority boundary.

### Phase 9 — complete

The first three contrasting pilots covered:

```text
Pilot A — repo-sensemaker
  direct repository diagnosis / currentness

Pilot B — architectural-review
  inherited evidence / architecture judgment

Pilot C — repair-verifier + output-reconciler
  post-change verification / reconciliation
```

Across the pilots, the stable common semantic core was:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence references
bounded scope / claim limits
decision-relevant uncertainty
explicit limits / non-claims
```

Skill-local vocabularies remain local: fog/weakness taxonomies, architecture `Component`/`Layer`/`Boundary`/`Contract`, architectural verdict enums, repair `closed/remaining`, reconciliation `verified/disputed/omitted`, PM artifact-local statuses, and Campaign transitions are **not** flattened into one generic schema.

PR #318 aligned the first engineering Skills to this reasoning discipline and added the first experimental Level-3 contract: `semantic_reasoning_profile` v1.

### Experimental Level 3 — `semantic_reasoning_profile`

The standalone validator `scripts/validate-semantic-reasoning-profile.py` mechanically checks required fields/shapes, IDs/enums, evidence-reference representation, currentness evidence for pinned/verified/inherited states, evidence presence for evidence-grounded claim statuses, and explicit limits/non-claims.

It explicitly cannot decide semantic truth, evidence sufficiency, uncertainty priority, warranted responsibility, capability selection, architectural correctness, repair success, or Campaign disposition.

Its structured output preserves:

```text
semantic_truth_established: false
```

Therefore:

```text
semantic profile valid != reasoning semantically correct
```

### Phase 10 — complete / Outcome A

Phase 10 tested the companion profile in three additional real-repository reasoning episodes:

```text
Chess Mentor Engine
  repo-sensemaker / direct diagnosis

React incremental game
  output-reconciler / exact-SHA handoff + live PR currentness

ViralFactory
  PM pre-mortem / canonical risk_analysis + companion profile
```

The preregistered outcomes were:

```text
A. keep as companion reasoning/audit artifact
B. selectively embed a smaller demonstrated subset
C. narrow/retire if duplication exceeds value
```

The qualified result is **Outcome A**.

The strongest positive signal came from the React episode: immutable exact-SHA repository evidence and independently mutable live PR metadata had to be distinguished before a continuation decision could be trusted.

The strongest negative embedding signal came from ViralFactory: canonical PM `risk_analysis` already represents evidence status, evidence refs, observed versus hypothetical risk, uncertainty, mitigation, recommendation boundaries, and unresolved questions. Embedding the whole common profile would duplicate domain state rather than improve semantic authority.

Accordingly:

- retain `semantic_reasoning_profile` v1 as an **optional companion audit/reconstruction artifact**;
- use it selectively when reasoning crosses artifacts/surfaces/domains or a fresh context needs a domain-neutral warrant/provenance index;
- do not require it when a strong domain artifact already carries the decision-changing evidence/currentness/uncertainty/limits;
- keep it outside Campaign artifact admission;
- do not create a universal artifact envelope.

The exact Phase 10 candidate `89258bd77bc2d234f54e03264c68d3c6de7f6de5` passed Product Validation run `34469270069` and Release Candidate Distribution run `34469270281` before PR #323 merged as `22d249e34a39f75e8052de4d4d50d7aca44b3175`.

The CI-authoritative semantic-profile suite validated all six checked-in Phase 9/10 profiles while preserving `semantic_truth_established: false`. The ViralFactory domain artifact continued to validate through the existing PM feature-definition validator rather than a generic semantic replacement.

See:

- `docs/semantic-architecture/phase-10/README.md`
- `docs/semantic-architecture/phase-10/results.md`
- `docs/semantic-architecture/phase-10-handoff.md`

### Later semantic phases — still deferred

Phase completion does not authorize the next phase.

```text
Phase 11 — Mechanical Semantic Probes      DEFERRED pending repeated demand
Phase 12 — Repository Semantic Map         DEFERRED
Phase 13 — Campaign/control-plane promotion DEFERRED
Phase 14 — Domain-pack extraction          DEFERRED
Phase 15 — Ontology conformance/drift      DEFERRED
```

Phase 10 did not expose repeated demand for a new mechanical relation family, repeated costly reconstruction of the same durable repository entity graph, or a Campaign correctness dependency on persisting the common profile.

The next semantic package must therefore be selected from observed repository/product pressure, not from the phase number.

## PM maturity policy

The PM program distinguishes implementation maturity from empirical support claims:

```text
CANDIDATE
-> REPOSITORY_QUALIFIED
-> NATIVE_HARNESS_QUALIFIED
-> PORTABILITY_QUALIFIED
-> PROMOTED
```

Repository qualification requires canonical Skill/artifact contracts where applicable, rejection coverage, Campaign integration, packaging/install proof, and exact-head CI. Native-harness and second-harness evidence remain required for stronger support/promotion claims.

The governing policy is:

```text
dogfood before promotion
!=
dogfood before expansion
```

Missing empirical qualification remains visible qualification debt. It is not silently treated as PASS.

## PM source-methodology migration — repository complete

`docs/product-management/capability-migration-matrix.md` is the authoritative per-capability maturity ledger.

All six planned waves are repository-qualified against pinned upstream `lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349`.

### Wave 1 — Customer Discovery

```text
persona
discovery
interview-synthesis
opportunity-tree
hypothesis
```

### Wave 2 — Feature Definition — PR #313

```text
to-prd (upstream prd methodology MERGED)
user-stories
acceptance-criteria
pre-mortem
```

The upstream `prd` command does not become a second PRD execution authority; useful methodology was merged into canonical `to-prd`.

### Wave 3 — Strategy & Prioritization — PR #316

```text
competitive-analysis
strategy
prioritize
north-star
okr
roadmap
lean-canvas
```

### Wave 4 — Experimentation / PMF / Pricing — PR #317

```text
experiment-design
ab-test-analysis
measure-pmf
pricing
```

### Wave 5 — Customer Modeling — PR #320

```text
customer-journey
ideal-customer-profile
```

The contracts bind evidence/currentness to customer-model claims. Observed journey, emotion, metric, critical-moment, profile, behavior, job, pain, indicator, or disqualifier claims require supporting evidence; unsupported customer fit remains hypothesis/inference/unknown rather than fabricated truth.

### Wave 6 — Launch / GTM / Enablement / Communication — PR #321

```text
launch-checklist
gtm
battlecard
release-notes
stakeholder-update
```

The contracts preserve:

```text
readiness assessment != launch authorization
GTM plan != campaign execution
battlecard claim != competitive truth without source/currentness
release announcement draft != publication
stakeholder next-step proposal != assignment
```

### PM repository implementation state

For the pinned 27-command migration:

```text
source inventory reconciled: COMPLETE
agent-agnostic canonical adaptation: COMPLETE
artifact/validator integration: COMPLETE where mechanically warranted
Campaign capability registration: COMPLETE
repository qualification: COMPLETE through Wave 6
native-harness qualification: PENDING
portability qualification: PENDING
promotion: PENDING
```

There is no implied Wave 7. New PM implementation should derive from real dogfood defects, new product requirements, or separately authorized methodology.

## Empirical qualification gates remain open

### Engineering v0.3 external golden path

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
Human/external action required for empirical PASS: YES
```

A real PASS still requires an actual supported external coding-agent harness attempt frozen under the canonical external golden-path protocol. The **real-harness qualification verifier** remains the v0.3 mechanism for mechanically checking a frozen external attempt package; it cannot manufacture real-harness origin evidence.

### PM native-harness and portability qualification

```text
Checked-in non-qualifying PM preflights: 1
Checked-in real-harness functional PM attempts: 0
Checked-in second-harness portability attempts: 0
Current functional PM empirical PASS: NONE
Current PM portability empirical PASS: NONE
```

Repository-local validation, Campaign admission, wheel packaging, and adapter parity do not substitute for real native-harness discovery/invocation.

The next PM qualification program should run the existing dogfood protocol through at least one real supported harness, verify fresh-context continuation from durable state, then repeat a bounded equivalent responsibility through a second supported harness before claiming portability or promotion.

### Semantic Architecture empirical limit

Phase 10 provides real-repository **repository-side reasoning episodes**, not native external-harness task-quality evidence or a blinded reconstruction benchmark. It therefore supports the companion-profile disposition but does not establish native-harness productivity gains.

## Release architecture continuity

- Campaign schema v2 remains the durable representation baseline.
- The shipped product/lab split remains intact.
- Product Validation owns shipped/installed-product claims; retained Lab Validation owns source-only research/lab claims.
- Release Candidate Distribution proves build/install/package identities on exact candidate heads.
- Semantic validators may establish only explicitly documented mechanical contracts.
- `semantic_reasoning_profile` remains outside Campaign artifact admission.
- Tagging/publication of v0.3.0 remains an explicit owner decision.

## Product and semantic boundaries

```text
observation != interpretation
evidence != truth
support != proof
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
semantic profile valid != reasoning semantically correct
companion reconstruction value != Campaign promotion warrant
Phase N complete != Phase N+1 authorized
admitted evidence != warranted conclusion
narrative claim bound to evidence != evidence proves claim
repository changed != finding no longer reproduces
finding no longer reproduces != repair semantically succeeded
directory != Component by default
import != architecture violation
passing test != complete behavior proof
document says X != X is current
immutable snapshot evidence != live mutable metadata
no search result != absence unless completeness is established
ontology term documented != runtime-enforced concept
verified claim in scope != universal truth
qualification receipt != real-harness origin proof
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
canonical capability != harness representation
Skill copied to discovery root != harness observed or invoked Skill
checklist complete != launch authorization
GTM plan != campaign execution
release draft != publication
proposed owner != assignment
lineage != semantic warrant
handoff != semantic recommendation
```

The Campaign Controller is not a semantic router. The Reasoning Model is not a central semantic controller.

## Operator handoff / canonical sources

- `STATUS.md` — current cross-program state.
- `docs/semantic-architecture/README.md` — Semantic Architecture index and formalization levels.
- `docs/semantic-architecture/constitution.md` — semantic/evidence/authority guardrails.
- `docs/semantic-architecture/competency-questions.md` — ontology scope tests.
- `docs/semantic-architecture/ontology.md` — layered Level-2 semantic model.
- `docs/semantic-architecture/relations-and-epistemics.md` — relation and epistemic semantics.
- `docs/semantic-architecture/reasoning-model.md` — evidence-governed reasoning lifecycle.
- `docs/semantic-architecture/execution-integration.md` — integration boundaries.
- `docs/semantic-architecture/implementation-plan.md` — phase states and promotion gates.
- `docs/semantic-architecture/pilots/README.md` — Phase 9 pilot index.
- `docs/semantic-architecture/common-semantic-contract.md` — experimental Level-3 profile contract.
- `docs/semantic-architecture/phase-9-handoff.md` — qualified Phase 9 handoff.
- `docs/semantic-architecture/phase-10/README.md` — Phase 10 preregistered experiment.
- `docs/semantic-architecture/phase-10/results.md` — Phase 10 evidence synthesis and Outcome A.
- `docs/semantic-architecture/phase-10-handoff.md` — qualified Phase 10 handoff.
- `docs/product-management/capability-migration-matrix.md` — PM capability dispositions/maturity.
- `docs/product-management/milestone-handoff.md` — full six-wave PM source-migration handoff.
- `docs/product-management/artifact-contracts.md` — current PM validation boundary index.
- `docs/product-management/qualification-levels.md` — PM maturity and qualification-debt policy.
- `docs/product-management/dogfood/STATUS.md` — PM empirical qualification status.
- `qualification-evidence/STATUS.md` — engineering empirical external-qualification status.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — retained Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.

When prose and checked-in executable validation disagree, executable behavior is authority for what the software currently enforces; semantic documentation remains the authority for intended concept meaning unless superseded by a later ratified decision. Documentation should then be reconciled rather than used to hide the mismatch.
