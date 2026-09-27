# Verification and Qualification Model

**Status:** Canonical terminology and claim-discipline model  
**Purpose:** Separate test classes, mechanical validation stages, semantic/control scope, and empirical qualification so that no one axis silently substitutes for another.

## 1. Core rule

Sensemaking uses several orthogonal assurance dimensions:

```text
test class
!= mechanical validation stage
!= semantic/control level
!= qualification state
```

The repository-wide claim boundary remains:

```text
validator passed != semantic truth
test passed != qualification
qualification != product truth outside the evidence scope
control level != validation strength
```

A result may be strong on one axis and weak or unknown on another. For example, a Level-3 strategic artifact can be mechanically valid while its recommendation remains semantically disputable, and a repository-qualified capability can still lack native-harness evidence.

## 2. Test classes

The canonical test classes are:

| Test class | Primary question | Typical examples | May establish | Must not establish by itself |
| --- | --- | --- | --- | --- |
| **UNIT** | Does one bounded implementation unit satisfy its local contract? | parser, helper, validator utility tests | local deterministic behavior | integration, qualification, semantic truth |
| **CONTRACT** | Do independently maintained representations agree mechanically? | schema, registry, producer/consumer, vocabulary, authority conformance | bounded representation agreement | semantic correctness |
| **INTEGRATION** | Do multiple components preserve invariants when composed? | validator/runtime, warrant seam, Campaign plumbing | tested seam composition | real-harness support or product effectiveness |
| **ACCEPTANCE** | Does a bounded product path work in the intended test environment? | vertical-slice or workflow acceptance tests | tested end-to-end product-path behavior | native-harness discovery/invocation unless the harness itself is exercised |
| **ROBUSTNESS** | Does the invariant survive invalid, adversarial, mutated, or edge-case input? | negative fixtures, mutation harnesses, rejection tests | rejection/failure-path behavior | success-path completeness or semantic truth |
| **PERFORMANCE** | Does measured behavior stay within a declared operational bound? | latency/SLO tests, large-input scenarios | measured performance for the tested environment | correctness outside that environment |
| **RELEASE_INTEGRITY** | Do package, release, current-doc, authority, and product-boundary surfaces agree? | release-contract, docs-currentness, skill-hygiene, package checks | release/repository integrity properties | empirical effectiveness |
| **QUALIFICATION_VERIFIER** | Does preserved evidence satisfy a declared qualification contract? | frozen evidence-package verification | that the evidence package meets the declared mechanical bar | that the underlying semantic/product claim is true beyond the evidence |
| **EXTERNAL_EVIDENCE** | Did the claimed interaction actually occur in the named external/native environment? | frozen real-harness attempts | the observed external fact at the bound identity | portability, repeatability, customer truth, or broad effectiveness without further evidence |

These classes describe **what a check is trying to establish**. They are not ordered from weak to strong in a single ladder.

### Product, lab, and external lanes

The maintainer verification lanes remain:

- **Product tests** own shipped behavior.
- **Lab tests** own retained research machinery.
- **External qualification tests** own frozen real-harness evidence.

A test class can appear in more than one lane. The lane identifies ownership/surface; the class identifies the claim the check supports.

## 3. Mechanical validation stages

Mechanical validation is ordered only across mechanically decidable properties.

### V0 — Syntax

Question:

> Can the representation be parsed at all?

Examples: valid YAML/JSON, parseable machine block, valid CLI input grammar.

### V1 — Shape

Question:

> Are required sections, fields, and primitive types present?

Examples: generic artifact structure, required headings, required machine fields.

### V2 — Contract / conformance

Question:

> Do values and relationships obey declared executable contracts?

Examples: enum membership, closed-object fields, registry references, producer/consumer field agreement, cross-document authority conformance.

### V3 — Identity / provenance / currentness

Question:

> Is this the exact artifact, repository, source revision, target, and lineage we think it is?

Examples: target-repository identity, source SHA, digest, currentness, parent/lineage binding.

### V4 — Evidence integrity

Question:

> Do declared evidence references mechanically resolve to the claimed material?

Examples: file exists, line/range exists, quote/excerpt matches source, reference resolves under the authoritative namespace.

### V5 — Admission / transition integrity

Question:

> Is this mechanically valid object permitted to enter the next durable state or transition?

Examples: Campaign admission, reconstructible transition chain, authority token/binding checks, exact-candidate evidence admission.

The boundary is explicit:

```text
V0-V5 PASS
!= semantic correctness
```

Validators may prove only declared mechanically decidable properties. They may not silently promote semantic support, strategic warrant, usefulness, or product truth into deterministic facts.

## 4. Semantic judgment above the mechanical boundary

The following are semantic responsibilities, even when a validator can constrain their representation:

### S1 — Evidence supports claim

Does the evidence actually justify the authored claim?

### S2 — Claim warrants decision

Does the interpreted evidence justify the selected responsibility, recommendation, or disposition?

### S3 — Observed outcome supports effectiveness claim

Does real-world behavior justify the asserted usefulness, support, strategy, or product-effectiveness claim?

Second-model review or human review may assist S1-S3, but assistance does not convert them into deterministic validator properties.

The historical seven-layer evidence model maps approximately as follows:

| Historical layer | Current interpretation |
| --- | --- |
| File exists | V4 |
| Line range exists | V4 |
| Quote matches source | V4 |
| Quote supports local claim | S1 |
| Stronger evidence does not contradict claim | S1/S2 |
| Weakest-boundary conclusion is useful/scoped | S2/S3 |
| Recommendation suitable downstream | S2/S3 |

## 5. Four-Level Control Model

The word **Level** is reserved for the current Four-Level Control Model.

In abbreviated form:

| Control level | Decision scope |
| --- | --- |
| **Level 1** | bounded/local execution and immediate implementation decisions |
| **Level 2** | responsibility/workflow-level reasoning and bounded coordination |
| **Level 3** | repository evolution / strategic repository decisions |
| **Level 4** | product-thesis / governing strategic decisions |

The control level answers:

> At what decision scope is the agent reasoning?

It does **not** answer:

- how strong a validator is;
- what kind of test ran;
- whether the result is qualified;
- whether the semantic conclusion is true.

### Historical terminology

Older retained documents use the phrase **"Level-3 validators"** for an earlier execution-validation taxonomy.

That phrase is **historical terminology and is unrelated to the current Four-Level Control Model**.

Rules for new/current documentation:

1. Do not introduce new uses of "Level-N validator".
2. Use **validation stage** for V0-V5 mechanical validation.
3. Use **test class** for UNIT/CONTRACT/INTEGRATION/etc.
4. Use **qualification state** for empirical maturity.
5. Preserve old wording in historical documents when needed for provenance, but do not treat it as current terminology.

## 6. Qualification states

The canonical empirical maturity progression remains:

```text
CANDIDATE
  ->
REPOSITORY_QUALIFIED
  ->
NATIVE_HARNESS_QUALIFIED
  ->
PORTABILITY_QUALIFIED
  ->
PROMOTED
```

The authoritative criteria live in [product-management/qualification-levels.md](product-management/qualification-levels.md).

Qualification answers:

> Where has this capability actually been proven, and what support claim is justified?

Mechanical test success is an input to qualification, not an alias for qualification.

Examples:

- passing repository CI may contribute to **REPOSITORY_QUALIFIED**;
- only observed native discovery/invocation can support **NATIVE_HARNESS_QUALIFIED**;
- equivalent bounded behavior through a second supported harness is required for **PORTABILITY_QUALIFIED**;
- promotion remains an explicit product/release decision.

## 7. Claim-ceiling matrix

| Evidence/result | Highest justified claim without additional evidence |
| --- | --- |
| UNIT passes | The tested local behavior matches its declared contract |
| CONTRACT passes | The tested representations agree mechanically |
| INTEGRATION passes | The tested components compose under the exercised scenario |
| ACCEPTANCE passes | The bounded product path works in the exercised test environment |
| ROBUSTNESS passes | The exercised invalid/adversarial conditions are handled as declared |
| PERFORMANCE passes | The measured operational bound held in the exercised environment |
| RELEASE_INTEGRITY passes | The tested release/repository surfaces agree mechanically |
| V0-V5 validation passes | The declared mechanically decidable properties hold |
| REPOSITORY_QUALIFIED | Repository implementation/integration requirements are satisfied |
| NATIVE_HARNESS_QUALIFIED | The capability was observed through the named supported native harness |
| PORTABILITY_QUALIFIED | Material semantic invariants held through the qualified additional harness |
| External real-use evidence | Only the observed real-use claim at its stated scope |
| Any validator PASS | Never semantic truth by itself |

## 8. Classification rule for new checks

When adding a new check, document or infer four independent answers:

1. **Test class:** what kind of check is this?
2. **Validation stage:** which mechanically decidable property does it verify, if any?
3. **Control level:** at what decision scope is the surrounding work occurring?
4. **Qualification effect:** what empirical state, if any, can this evidence advance?

A check that cannot answer these independently is likely mixing implementation assurance, semantic judgment, and product claims.

## 9. Lessons from repository evolution

The repository's history shows several recurring failure modes that this model is intended to prevent:

1. **Vocabulary reuse can create false authority.** The historical phrase `Level-3 validators` later collided with the current Level-3 repository-strategy meaning. Stable names should preserve one semantic role across current documentation.
2. **Green checks can silently inflate claims.** Unit, integration, acceptance, and validator results each support different bounded claims; none automatically upgrades empirical qualification.
3. **Evidence transport and evidence meaning are different responsibilities.** Provenance, identity, reference resolution, and admission can be deterministic while support, usefulness, and warrant remain semantic.
4. **Qualification is environment-bound.** Repository qualification is not a simulation of native-harness qualification; the environment named by the claim must appear in the evidence.
5. **Assurance needs a source-of-truth surface.** Scattered correct statements are insufficient when a fresh agent can reconstruct an obsolete model from historical material.

### Reporting rule

Consequential validation/qualification reports should state, when material:

```text
test class:
validation stage:
semantic status:
qualification effect:
evidence identity:
claim ceiling:
```

Fields may be omitted when genuinely irrelevant, but a PASS should never be reported without enough context to identify what passed and what claim that result supports.

This is a reporting discipline, not a new artifact schema or mandatory runtime record.

## 10. Design invariants

```text
test class != control level
validation stage != semantic judgment
validator passed != semantic truth
acceptance passed != native-harness qualified
repository qualified != portability qualified
external evidence != generalized effectiveness
qualification state != automatic promotion
```

This model is a terminology and claim-discipline contract. It does not create a new runtime engine, a numeric assurance score, an automatic promotion mechanism, or a deterministic semantic judge.