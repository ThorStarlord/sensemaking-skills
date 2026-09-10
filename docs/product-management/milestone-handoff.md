# Product Management domain productization handoff

**Date:** 2026-09-10  
**Milestone:** Agent-Agnostic Product Management domain — upstream source-methodology migration  
**Repository implementation state:** COMPLETE through Waves 1–6  
**Repository maturity:** 27 canonical PM capability mappings are `REPOSITORY_QUALIFIED` after exact-head CI and merge  
**Empirical native-harness qualification:** PENDING  
**Empirical portability qualification:** PENDING  
**Promotion state:** NOT PROMOTED by this milestone

## Objective delivered

The repository has completed the repository-side adaptation of all 27 Product Management command methodologies from the pinned upstream source into the Sensemaking architecture without making Claude Code, Codex, OpenCode, ChatGPT, or another harness the semantic authority.

The methodological source remains pinned to:

```text
lucasgaravelli/pm-skills-claude-code
commit 21cbb2903d740d10fc65c667aea97d3ee8657349
MIT / Flowgrammers 2026
```

The upstream `prd` command is intentionally **MERGED** into the pre-existing canonical `to-prd` capability rather than creating a duplicate `prd` execution authority. The current PM domain therefore has 27 canonical capability mappings for the 27 upstream source commands, with `to-prd` serving the upstream `prd` responsibility.

## Governing architecture

The final architecture remains:

```text
user goal
-> Sensemaking Campaign
-> agent identifies warranted PM responsibility
-> unranked available capabilities are inspected
-> agent selects capability
-> canonical agent-agnostic PM Skill executes
-> typed artifact
-> deterministic validation
-> Campaign admission / provenance / lineage
-> agent reviews semantic meaning
-> advance / defer / close
-> handoff / continuation
```

The harness boundary remains outside PM semantics:

```text
canonical PM capability
        |
        +-> generic/Codex adapter
        +-> Claude adapter
        +-> OpenCode adapter
        +-> future harness adapter
```

Canonical methodology, evidence rules, artifact contracts, authority boundaries, and stop conditions do not depend on a particular coding-agent runtime.

## Qualification policy

PR #312 changed the program from `dogfood before expansion` to the more precise:

```text
CANDIDATE
-> REPOSITORY_QUALIFIED
-> NATIVE_HARNESS_QUALIFIED
-> PORTABILITY_QUALIFIED
-> PROMOTED
```

and:

```text
dogfood before promotion
!=
dogfood before expansion
```

Repository qualification requires the repository-side contracts and exact-head CI. Native-harness and second-harness evidence remain explicit qualification debt and are required for stronger support/promotion claims.

## Delivery evidence

### Foundation and first vertical slice

| Work | PR | Final candidate head | Merge commit | Result |
|---|---:|---|---|---|
| PM domain contract and migration ledger | #307 | `967bff480d8681290bc294608695677c06bdb4f5` | `539f85e9f55bae6e1e2b1d190aa5c7395ea19d5f` | merged after Product Validation + Release Candidate Distribution |
| Customer Discovery canonical Skills | #308 | `9235e4e550956d9767c2602216eee54274792077` | `a65e596e8afe4e6991be0bbaea4b9427a2ee6de7` | merged after Product Validation + Release Candidate Distribution |
| Customer Discovery artifact/Campaign integration | #309 | `897e5850a4ab229eeb2c00e23d91339c3bf8e884` | `e7d213e07976a2f269b1479fcc36decdcf0cdeb4` | merged after Product + Lab + Release Candidate validation |
| Initial milestone handoff | #310 | `707cf3084e82c10fbff20496950f83d9e5450c15` | `02da8fd50938c5aaec9722f0e14191801162da9e` | merged after Product + Release Candidate validation |
| Non-qualifying PM repository preflight | #311 | preserved repository-side evidence | `0c4769710a5473f5a3108fd3206a8ccfd7058547` | useful preflight; deliberately not counted as native-harness PASS |
| Qualification-level policy | #312 | `59a1fe8a8fb909a8f8a64c0461a07ce38af607fe` | `4bc131a64b0bdd77ac879a68715fbbf9b734f8a9` | repository expansion unlocked while promotion remains empirical |

### Expansion waves

| Wave | Capabilities | PR | Final candidate head | Merge commit | Result |
|---|---|---:|---|---|---|
| 2 — Feature Definition | `to-prd` (upstream `prd` MERGED), `user-stories`, `acceptance-criteria`, `pre-mortem` | #313 | `4d0d9fe8e5537c9354f132566e827e6b71b86732` | `584b59da5dc39c99910539280460c2cceac4d2f8` | repository-qualified |
| 3 — Strategy & Prioritization | `competitive-analysis`, `strategy`, `prioritize`, `north-star`, `okr`, `roadmap`, `lean-canvas` | #316 | `54c552fe850849289c083a5707df93f4dacee9e4` | `8c28b4996082906407e710a3da14aacafbb5d94a` | repository-qualified |
| 4 — Experimentation / PMF / Pricing | `experiment-design`, `ab-test-analysis`, `measure-pmf`, `pricing` | #317 | `790ce4debd11370ecfc3295684e2e474d3be9260` | `8109b0a7133abb8363f808d01292f5f7375d766f` | repository-qualified |
| 5 — Customer Modeling | `customer-journey`, `ideal-customer-profile` | #320 | `c09ccbfe532ef07887e5204315aea31e71d644aa` | `9f4a2d5b5b35669661dadc580cb495675791ba59` | repository-qualified after one observed regression repair |
| 6 — Launch / GTM / Enablement / Communication | `launch-checklist`, `gtm`, `battlecard`, `release-notes`, `stakeholder-update` | #321 | `245a276e574b84f55af30cac9550d387f49ef9b0` | `d433d7d6c34cc8a529b35b2bbfec2a1426c8c3f9` | repository-qualified |

Each Wave 3–6 candidate was merged only after its required exact-head Product Validation, Lab Validation, and Release Candidate Distribution lanes passed.

## Repository-qualified PM capability set

### Customer Discovery

```text
persona -> persona_definition
discovery -> discovery_findings
interview-synthesis -> synthesis_report
opportunity-tree -> opportunity_map
hypothesis -> hypothesis_statement
```

### Feature Definition

```text
to-prd -> prd
user-stories -> story_list
acceptance-criteria -> criteria_list
pre-mortem -> risk_analysis
```

### Strategy and Prioritization

```text
competitive-analysis -> market_analysis
strategy -> strategy_doc
prioritize -> prioritized_list
north-star -> north_star_metric
okr -> okr_list
roadmap -> roadmap
lean-canvas -> business_canvas
```

### Experimentation / PMF / Pricing

```text
experiment-design -> experiment_plan
ab-test-analysis -> test_results
measure-pmf -> pmf_report
pricing -> pricing_model
```

### Customer Modeling

```text
customer-journey -> journey_map
ideal-customer-profile -> ideal_customer_profile
```

### Launch / GTM / Enablement / Communication

```text
launch-checklist -> readiness_report
gtm -> gtm_plan
battlecard -> battlecard
release-notes -> feature_announcement
stakeholder-update -> stakeholder_update
```

## Specialized validation surface

The PM domain now has bounded validators for mechanically useful contracts:

```text
validate-pm-artifact.py
  Customer Discovery

validate-pm-feature-definition.py
  story_list / criteria_list / risk_analysis

validate-pm-strategy.py
  market / strategy / priority / NSM / OKR / roadmap / canvas

validate-pm-measurement.py
  experiments / results / PMF / pricing

validate-pm-customer-model.py
  journey / ICP

validate-pm-launch-communication.py
  readiness / GTM / battlecard / release communication / stakeholder update
```

`scripts/validate-and-report.py` is the common router. Validation establishes representation, identity/reference, evidence-state, arithmetic, source/currentness, and authority-reference contracts where explicitly defined. It does **not** establish semantic truth or make the product decision for the active agent.

## Semantic Architecture alignment

Waves 5–6 were reconciled after the Semantic Architecture / Reasoning Model foundation had landed. Their artifact-local states intentionally reuse the stable distinctions among observation, derivation/inference, hypothesis, ratification, contradiction/currentness, and unresolved knowledge where consequential.

This does not promote the Level-2 ontology into a universal runtime schema. Skill-local concepts remain local, and the active agent still owns semantic judgment.

## Important observed repairs

### Package 3 stale generic-validator expectation

The first Customer Discovery integration candidate revealed an old Campaign regression that still expected `discovery_findings` to use the generic validator. The test was corrected to preserve generic fallback on a genuinely generic artifact instead of weakening PM validation.

### Wave 5 canonical identity contract

The first Wave 5 candidate failed both Python Campaign suites because `ideal-customer-profile` was the first current PM capability with no historical Skill-registry identity. The repair added an explicit current, agent-agnostic canonical identity without restoring Wayfinder auto-invocation semantics. The repaired exact head then passed Product, Lab, and Release Candidate validation before merge.

### Stale Wave 5 branch rejected

An older partial `work/pm-wave5-customer-modeling` branch was found far behind current `main` and contained an unnecessary broad reformat of the validation router. Wave 5 was rebuilt from current `main` and only bounded semantic/validator changes were carried forward.

## Empirical qualification debt remains open

Current preserved empirical status remains:

```text
checked-in non-qualifying PM preflights: 1
checked-in real-harness functional PM attempts: 0
checked-in second-harness portability attempts: 0
functional empirical PASS: NONE
portability empirical PASS: NONE
```

Repository-local validation, Campaign admission, wheel packaging, and structural adapter parity do not prove that a real supported native coding-agent harness discovered/invoked these capabilities.

A future promotion program should therefore execute the existing dogfood protocol rather than adding more source-methodology migration work:

1. run a real PM Campaign through one supported native harness;
2. preserve native discovery/invocation evidence;
3. perform a fresh-context reconstruction from durable state without prior chat;
4. repeat an equivalent bounded responsibility through a second supported harness;
5. classify results honestly and repair observed defects;
6. promote only the capabilities/claims whose empirical evidence warrants promotion.

## Repository implementation frontier

For the pinned 27-command PM source migration:

```text
source inventory reconciled: COMPLETE
canonical adaptation: COMPLETE
repository-side artifact/validation integration: COMPLETE
Campaign capability registration: COMPLETE
exact-head repository qualification: COMPLETE through Wave 6
native-harness qualification: PENDING
portability qualification: PENDING
promotion: PENDING
```

No additional PM source-migration wave is implied by this handoff.

## Governing distinctions

```text
canonical PM capability != harness representation
responsibility != capability
available capability != selected capability
selected capability != execution authority
artifact valid != conclusion true
artifact admitted != claim warranted
observed claim != inferred claim
inference != ratified decision
checklist complete != launch authorization
GTM plan != campaign execution
release draft != publication
proposed owner != assignment
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
```

## Canonical PM references

- `docs/product-management/README.md`
- `docs/product-management/capability-migration-matrix.md`
- `docs/product-management/artifact-contracts.md`
- `docs/product-management/qualification-levels.md`
- `docs/product-management/dogfood-runbook.md`
- `docs/product-management/dogfood/STATUS.md`
- `src/sensemaking_skills/defaults/capability-registry.yaml`
- `scripts/validate-and-report.py`

Future PM implementation should derive from observed dogfood defects, new product requirements, or new separately authorized methodology—not from the assumption that the completed upstream migration itself requires another wave.
