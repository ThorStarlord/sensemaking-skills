# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** Parallel PM repository expansion and Semantic Architecture Phase 10 experimentation; engineering and PM empirical external qualification remain pending  
**Primary program:** Sensemaking Campaign productization with agent-agnostic domain capabilities and evidence-governed repository reasoning  
**Current implementation frontier:** Use Git `main` HEAD as exact repository identity; this status file intentionally does not self-pin a commit that becomes stale when the file itself changes  
**Current semantic frontier:** Phase 9 first Reasoning Model operationalization is complete; Phase 10 tests the experimental common semantic envelope in additional real repository episodes  
**Current PM frontier:** Waves 1–4 are `REPOSITORY_QUALIFIED`; continue Wave 5 Customer Modeling under the existing qualification policy

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. Its Campaign substrate supports agent-agnostic Product Management capabilities and an evidence-governed Semantic Architecture for consistent repository reasoning. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, target identity, evidence binding, and reconstructible state.

## Semantic Architecture maturity

PR #314 established the documentation-first semantic foundation. PR #318 completed the first contrasting **Reasoning Model Operationalization & Skill Semantic-Alignment** milestone.

The architecture now has four explicit layers:

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

Skill-local vocabularies remain local: fog/weakness taxonomies, architecture `Component`/`Layer`/`Boundary`/`Contract`, architectural verdict enums, repair `closed/remaining`, reconciliation `verified/disputed/omitted`, and Campaign transitions are **not** flattened into one generic schema.

PR #318 aligned the four Skills to this reasoning discipline and added the first new experimental Level-3 contract: `semantic_reasoning_profile` v1.

### Experimental Level 3 — `semantic_reasoning_profile`

The standalone validator `scripts/validate-semantic-reasoning-profile.py` can mechanically check:

- required fields and shapes;
- IDs and enum values;
- evidence-reference representation;
- currentness evidence presence for pinned/verified/inherited states;
- evidence presence for evidence-grounded claim statuses;
- explicit limits/non-claims.

It explicitly cannot decide semantic truth, evidence sufficiency, uncertainty priority, warranted responsibility, capability selection, architectural correctness, repair success, or Campaign disposition.

Its structured output preserves the boundary:

```text
semantic_truth_established: false
```

Therefore:

```text
semantic profile valid != reasoning semantically correct
```

The profile remains a **companion experimental artifact**. It is not registered in Campaign artifact admission and does not change Campaign schema v2.

The exact Phase 9 qualified candidate was `d8fbcd7876ad5821c2627e40d417ff652af2588a`; it passed Product Validation and Release Candidate Distribution before merge as PR #318 / merge commit `7262f4b23a9e3626835107c8076e6c2671ff5870`.

### Phase 10 — active semantic frontier

Phase 10 asks whether the common semantic core should:

```text
A. remain a companion reasoning/audit profile;
B. be embedded selectively in multiple analytical artifacts; or
C. be narrowed/retired if coordination overhead exceeds value.
```

Additional real repository episodes should measure:

- repeated semantic reconstruction;
- claims missing currentness/evidence;
- unsupported inference jumps;
- fresh-context usefulness;
- artifact boilerplate;
- token/coordination overhead;
- validator overreach.

Do **not** implement a central reasoning engine, universal repository semantic graph, or Campaign semantic-profile promotion merely because Phase 9 completed. Repository Semantic Map and Campaign-level semantic promotion remain evidence-gated later phases.

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

The governing policy remains:

```text
dogfood before promotion
!=
dogfood before expansion
```

Missing empirical qualification is visible qualification debt. It is not silently treated as PASS.

## Repository-qualified PM waves

Current authoritative maturity is recorded in `docs/product-management/capability-migration-matrix.md`.

### Wave 1 — Customer Discovery

Repository-qualified:

```text
persona
discovery
interview-synthesis
opportunity-tree
hypothesis
```

### Wave 2 — Feature Definition

PR #313 repository-qualified:

```text
to-prd (upstream prd methodology MERGED)
user-stories
acceptance-criteria
pre-mortem
```

### Wave 3 — Strategy & Prioritization

PR #316 repository-qualified:

```text
competitive-analysis
strategy
prioritize
north-star
okr
roadmap
lean-canvas
```

The contracts preserve source currency, evidence state, arithmetic where mechanical, proposed-vs-ratified status, and authority boundaries while leaving semantic prioritization/strategy judgment with the agent.

### Wave 4 — Experimentation / PMF / Pricing

PR #317 repository-qualified:

```text
experiment-design
ab-test-analysis
measure-pmf
pricing
```

These contracts distinguish experiment design from observed results, require evidence for empirical analysis/measurement claims, and keep pricing recommendations separate from authority to change prices.

### Next PM wave

Wave 5 remains `CANDIDATE`:

```text
customer-journey
ideal-customer-profile
```

Wave 6 GTM/Communication remains deferred after that.

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

Repository-local validation, Campaign admission, wheel packaging, and adapter parity do not substitute for real native-harness discovery/invocation. These gaps limit stronger support/promotion claims rather than separately authorized repository implementation.

### Semantic-architecture empirical limit

The Phase 9 pilots used pinned repository/Skill evidence and exact-head CI. They did **not** establish native external-harness task-quality improvement. Phase 10 must observe additional real repository episodes before broader semantic-contract promotion.

## Release architecture continuity

- Campaign schema v2 remains the durable representation baseline.
- The shipped product/lab split remains intact.
- Product Validation owns shipped/installed-product claims; retained Lab Validation owns source-only research/lab claims.
- Release Candidate Distribution proves build/install/package identities on exact candidate heads.
- Semantic validators may establish only explicitly documented mechanical contracts.
- Tagging/publication of v0.3.0 remains an explicit owner decision.

## Product and semantic boundaries

```text
observation != interpretation
evidence != truth
support != proof
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
semantic profile valid != reasoning semantically correct
admitted evidence != warranted conclusion
narrative claim bound to evidence != evidence proves claim
repository changed != finding no longer reproduces
finding no longer reproduces != repair semantically succeeded
directory != Component by default
import != architecture violation
passing test != complete behavior proof
document says X != X is current
no search result != absence unless completeness is established
ontology term documented != runtime-enforced concept
verified claim in scope != universal truth
qualification receipt != real-harness origin proof
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
canonical capability != harness representation
Skill copied to discovery root != harness observed or invoked Skill
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
- `docs/semantic-architecture/implementation-plan.md` — current phase plan and promotion gates.
- `docs/semantic-architecture/pilots/README.md` — Phase 9 pilot index.
- `docs/semantic-architecture/common-semantic-contract.md` — experimental Level-3 profile contract.
- `docs/semantic-architecture/phase-9-handoff.md` — qualified Phase 9 handoff.
- `docs/product-management/capability-migration-matrix.md` — PM capability dispositions/maturity.
- `docs/product-management/qualification-levels.md` — PM maturity and qualification-debt policy.
- `docs/product-management/dogfood/STATUS.md` — PM empirical qualification status.
- `qualification-evidence/STATUS.md` — engineering empirical external-qualification status.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — retained Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.

When prose and checked-in executable validation disagree, executable behavior is authority for what the software currently enforces; semantic documentation remains the authority for intended concept meaning unless superseded by a later ratified decision. Documentation should then be reconciled rather than used to hide the mismatch.
