# Status

**Version:** 0.3.0  
**Last updated:** 2026-09-10  
**Current phase:** Parallel repository-qualified PM expansion and Semantic Architecture empirical adoption; engineering and PM empirical external qualification remain pending  
**Primary program:** Sensemaking Campaign productization with agent-agnostic domain capabilities and evidence-governed repository reasoning  
**Current implementation frontier:** Use Git `main` HEAD as exact repository identity; this status file intentionally does not self-pin a commit that becomes stale when the file itself changes  
**Current semantic frontier:** Phase 9 Skill semantic-alignment pilots: `repo-sensemaker` -> `architectural-review` -> `repair-verifier` / `output-reconciler`  
**Current PM frontier:** Wave 2 Feature Definition is `REPOSITORY_QUALIFIED`; continue Wave 3 Strategy & Prioritization under the existing qualification policy

Sensemaking Skills is an **agent-native engineering sensemaking and control layer**. Its Campaign substrate now supports agent-agnostic Product Management capabilities and a documentation-first **Sensemaking Semantic Architecture** for consistent repository reasoning. The active coding agent owns semantic judgment; deterministic machinery owns representation, persistence, validation, provenance, integrity, authority checks, target identity, evidence binding, and reconstructible state.

## Sensemaking Semantic Architecture foundation

PR #314 established the first canonical semantic-design foundation under `docs/semantic-architecture/`.

The architecture separates:

```text
Semantic Model
  = what entities, relations, and epistemic statuses mean

Reasoning Model
  = how observations become evidence, claims, uncertainty,
    responsibility, capability use, and decisions

Execution Integration
  = how probes, Skills, artifacts, validators, Campaigns,
    handoff, domains, and harnesses participate
```

It also defines three formalization levels:

```text
Level 1 — Vocabulary
Level 2 — Ontology
Level 3 — Executable semantic contract
```

A documented Level-1/2 concept is not runtime authority. Executable promotion requires repeated workflow evidence, stable semantics, a mechanically expressible boundary, negative/rejection coverage, and preservation of the agent/deterministic control boundary.

The foundation currently includes:

- a 20-rule Semantic Architecture Constitution;
- 78 competency questions covering intent, currentness, repository structure, architecture, behavior/contracts, evidence, epistemics, uncertainty, responsibility/capability, change/repair, product change, documentation drift, and handoff;
- an inventory reconciled against existing Campaign and Skill concepts;
- a six-layer ontology: Intent, Repository/Software System, Evidence, Knowledge/Epistemics, Engineering Work, and Product;
- explicit disambiguation of `SoftwareCapability`, `ProductCapability`, and `SensemakingCapability`;
- a product-change taxonomy covering structural change type, value mechanism, target of change, and relationship to existing value;
- epistemic statuses and relation-establishment classes;
- a prohibited-inference catalog;
- an evidence-governed reasoning lifecycle;
- integration boundaries for probes, Skills, artifacts, validators, Campaigns, domains, and harnesses;
- 12 reference scenarios;
- a phased promotion plan from shared vocabulary to possible future executable contracts.

The foundation is intentionally documentation-first. It does **not** add a universal ontology schema, knowledge graph, automatic component detector, semantic router, automatic uncertainty ranking, automatic capability selection, new Campaign schema fields, or new mutation authority.

The exact semantic-foundation merge baseline is PR #314 / merge commit `633fe0542bd34ee7c8d0c9188e4cf03b320e5bfa`. Later repository HEADs may advance independently.

### Next semantic milestone

Run bounded semantic-alignment pilots rather than implementing the ontology wholesale:

1. **`repo-sensemaker`** — currentness, observations vs inference, evidence-backed claims, contradiction, and decision-changing uncertainty.
2. **`architectural-review`** — `Component`, `Layer`, `Boundary`, `Contract`, and `DependencyRelation` semantics.
3. **`repair-verifier` or `output-reconciler`** — `Change`, `Outcome`, `Repair`, validation scope, reconciliation, and supersession.

Each pilot should record competency questions exercised, ambiguous terms found, unsupported inference jumps prevented, concepts requested, concepts unused, and coordination overhead. Common executable semantic fields should not be extracted until at least two contrasting pilots demonstrate stable reuse.

## PM maturity policy

The PM program distinguishes implementation maturity from empirical support claims:

```text
CANDIDATE
-> REPOSITORY_QUALIFIED
-> NATIVE_HARNESS_QUALIFIED
-> PORTABILITY_QUALIFIED
-> PROMOTED
```

Repository qualification requires the relevant canonical Skill, artifact/validation contracts where applicable, rejection coverage, Campaign integration, packaging/install proof, and exact-head CI. Native-harness and second-harness evidence remain required for stronger support/promotion claims.

The governing policy remains:

```text
dogfood before promotion
!=
dogfood before expansion
```

Missing empirical qualification is visible qualification debt. It is not silently treated as PASS, and no capability may claim a maturity state unsupported by preserved evidence.

See `docs/product-management/qualification-levels.md` and ADR 0028.

## Repository-qualified PM capabilities

### Wave 1 — Customer Discovery

The first repository-qualified responsibility sequence is:

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

with canonical Skills:

```text
persona
-> discovery
-> interview-synthesis
-> opportunity-tree
-> hypothesis
```

### Wave 2 — Feature Definition

PR #313 repository-qualified the Feature Definition wave:

```text
product_specification
-> delivery_specification
-> risk_and_readiness
```

Current dispositions are:

- upstream `prd` methodology is **MERGED** into the existing canonical `to-prd`; no duplicate current `prd` authority is created;
- `user-stories` is `REPOSITORY_QUALIFIED` and produces `story_list`;
- `acceptance-criteria` is `REPOSITORY_QUALIFIED` and produces `criteria_list`;
- `pre-mortem` is `REPOSITORY_QUALIFIED` and produces `risk_analysis`.

The exact Wave 2 merge baseline is PR #313 / merge commit `584b59da5dc39c99910539280460c2cceac4d2f8`.

## Empirical gates remain open

### Engineering v0.3 external golden path

```text
Checked-in real-harness attempts: 0
Current empirical PASS: NONE
Human/external action required for empirical PASS: YES
```

A real empirical PASS still requires an actual supported external coding-agent harness attempt frozen under `v0.3-external-golden-path-dogfood-v1` and verified against the exact frozen attempt bytes.

The real-harness qualification verifier remains the engineering v0.3 mechanism for checking frozen external attempt packages.

### PM native-harness and portability qualification

```text
Checked-in non-qualifying PM preflights: 1
Checked-in real-harness functional PM attempts: 0
Checked-in second-harness portability attempts: 0
Current functional PM empirical PASS: NONE
Current PM portability empirical PASS: NONE
```

Repository-local validation, Campaign admission, wheel packaging, and canonical-byte adapter parity are not substitutes for real native harness discovery/invocation.

These empirical gates limit promotion/support claims rather than separately authorized repository implementation.

## Current PM implementation queue

The capability inventory remains governed by `docs/product-management/capability-migration-matrix.md`.

Current repository-expansion sequence:

1. **Wave 3 — Strategy & Prioritization:** adapt `competitive-analysis`, `strategy`, `prioritize`, `north-star`, `okr`, `roadmap`, `lean-canvas`.
2. **Wave 4 — Experimentation / PMF / Pricing:** adapt `experiment-design`, `ab-test-analysis`, `measure-pmf`, `pricing` with strong evidence-status gates.
3. **Wave 5 — Customer Modeling:** adapt `customer-journey`, `ideal-customer-profile`.
4. **Wave 6 — GTM / Communication:** adapt `launch-checklist`, `gtm`, `battlecard`, `release-notes`, `stakeholder-update` while external execution remains separately authorized.

Each wave must earn `REPOSITORY_QUALIFIED` independently through exact-head CI. No wave may claim native-harness, portability, or promotion status without corresponding empirical evidence.

## Release architecture continuity

- Campaign schema v2 remains the current durable representation baseline.
- The shipped product/lab split remains intact.
- Product Validation owns shipped/installed-product claims; retained Lab Validation owns source-only research/lab claims.
- Release Candidate Distribution proves build/install/package identities on exact candidate heads.
- The engineering external golden-path verifier remains separate from PM qualification debt.
- Tagging/publication of v0.3.0 remains an explicit owner decision.
- Semantic Architecture Level-1/2 documentation does not silently extend Campaign schema or validator authority.

## Product and semantic boundaries

```text
observation != interpretation
evidence != truth
support != proof
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
admitted evidence != warranted conclusion
narrative claim bound to evidence != evidence proves claim
repository changed != repair succeeded
directory != Component by default
import != architecture violation
passing test != complete behavior proof
document says X != X is current
no search result != absence unless completeness is established
ontology term documented != runtime-enforced concept
qualification receipt != real-harness origin proof
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
canonical PM capability != harness representation
Skill copied to discovery root != harness observed or invoked Skill
lineage != semantic warrant
handoff != semantic recommendation
```

The Campaign Controller is not a semantic router. The Semantic Architecture does not create one.

## Operator handoff / canonical sources

- `STATUS.md` — current cross-program state.
- `docs/semantic-architecture/README.md` — Semantic Architecture index, scope, and formalization levels.
- `docs/semantic-architecture/constitution.md` — semantic/evidence/authority guardrails.
- `docs/semantic-architecture/competency-questions.md` — ontology scope tests.
- `docs/semantic-architecture/ontology.md` — layered Level-2 semantic model.
- `docs/semantic-architecture/relations-and-epistemics.md` — relation and epistemic semantics.
- `docs/semantic-architecture/reasoning-model.md` — evidence-governed reasoning lifecycle.
- `docs/semantic-architecture/execution-integration.md` — integration boundaries.
- `docs/semantic-architecture/implementation-plan.md` — promotion gates and next pilots.
- `docs/semantic-architecture/milestone-handoff.md` — semantic-foundation milestone handoff.
- `docs/product-management/README.md` — PM domain boundaries.
- `docs/product-management/qualification-levels.md` — PM maturity and qualification-debt policy.
- `docs/product-management/capability-migration-matrix.md` — all upstream PM command dispositions and maturity.
- `docs/product-management/dogfood-runbook.md` — PM native-harness/fresh-context/second-harness protocol.
- `docs/product-management/dogfood/STATUS.md` — PM empirical qualification status.
- `docs/adr/0028-agent-agnostic-product-management-domain.md` — PM architectural authority.
- `qualification-evidence/STATUS.md` — engineering empirical external-qualification status.
- `docs/external-golden-path-verifier.md` — engineering external attempt/verifier protocol.
- `docs/sensemaking-campaign.md` — canonical Campaign product model.
- `.github/workflows/validation.yml` — Product Validation authority.
- `.github/workflows/lab-validation.yml` — retained Lab Validation authority.
- `.github/workflows/release-candidate.yml` — release distribution authority.

When prose and checked-in executable validation disagree, executable behavior is authority for what the software currently enforces; semantic documentation remains the authority for intended concept meaning unless superseded by a later ratified decision. Documentation should then be reconciled rather than used to hide the mismatch.
