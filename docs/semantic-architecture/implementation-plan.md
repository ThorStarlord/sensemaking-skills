# Semantic Architecture Implementation Plan

**Status:** Active  
**Completed milestone:** Semantic foundation + Phase 9 first Reasoning Model operationalization pilots  
**Current frontier:** Phase 10 bounded common-envelope experiment  
**Implementation principle:** Formalize from demonstrated reasoning pressure; do not manufacture runtime machinery to make the ontology look complete.

## Objective

Create a shared semantic foundation that lets Sensemaking Skills reason consistently about unfamiliar repositories while preserving evidence lineage, currentness, uncertainty, semantic authority, and the existing agent/deterministic control boundary.

The plan separates:

```text
documented vocabulary
-> ontology semantics
-> observed cross-Skill reuse
-> bounded executable representation
-> possible later control-plane promotion
```

A later phase does not retroactively turn earlier documentation into runtime authority.

## Permanent promotion ladder

```text
observed vocabulary need
        |
        v
Level 1: shared term
        |
        | repeated useful distinction
        v
Level 2: ontology entity/relation
        |
        | repeated cross-Skill burden
        | stable semantics
        | mechanically expressible subset
        v
Level 3: executable semantic contract
```

### Level 1 -> Level 2 gate

Require:

- at least one competency question;
- repeated semantic use or critical boundary value;
- clear definition;
- no canonical duplicate;
- useful relations to existing concepts.

### Level 2 -> Level 3 gate

Require:

- evidence from at least two contrasting real workflow/Skill situations unless safety/integrity requires earlier action;
- stable semantic meaning;
- identified mechanical subset;
- explicit validator scope;
- migration/backward-compatibility consideration when durable state is affected;
- negative/rejection cases;
- no transfer of semantic authority to deterministic machinery.

---

# Phase status map

| Phase | Name | Status |
|---:|---|---|
| 0 | Preserve architecture boundary | COMPLETE |
| 1 | Problem definition | COMPLETE |
| 2 | Competency questions | COMPLETE |
| 3 | Existing concept inventory/reconciliation | BASELINE COMPLETE; incremental |
| 4 | Layered ontology | COMPLETE at Level 2 |
| 5 | Relationship and epistemic model | COMPLETE at Level 2 |
| 6 | Reasoning architecture | COMPLETE at design level |
| 7 | Integration architecture | COMPLETE at design level |
| 8 | Reference scenarios | COMPLETE |
| 9 | Reasoning Model operationalization / Skill semantic-alignment pilots | FIRST THREE PILOTS COMPLETE |
| 10 | Common artifact-semantic envelope experiment | ACTIVE |
| 11 | Mechanical semantic probes | DEFERRED pending repeated demand |
| 12 | Repository Semantic Map experiment | DEFERRED |
| 13 | Campaign/control-plane promotion | DEFERRED |
| 14 | Domain-pack extraction | DEFERRED |
| 15 | Ontology conformance/drift checks | DEFERRED |

---

# Phases 0–8 — Foundation

The foundation milestone established:

- `constitution.md` and the semantic-control boundary;
- `problem-statement.md`;
- 78 initial competency questions;
- `concept-inventory.md` reconciled with existing Campaign semantics;
- the six-layer Intent / Repository-System / Evidence / Knowledge / Work / Product ontology;
- `SoftwareCapability`, `SensemakingCapability`, and `ProductCapability` namespace separation;
- relationship/epistemic rules and prohibited inferences;
- the canonical staged Reasoning Model;
- execution-integration boundaries;
- 12 reference scenarios.

These remain documentation/ontology authority except where an existing executable product contract or a separately promoted Level-3 contract implements a mechanical subset.

---

# Phase 9 — Reasoning Model Operationalization & Skill Semantic-Alignment Pilots

**Status:** First three contrasting pilots COMPLETE.

## Goal

Test the Reasoning Model against real Skill contracts before creating broad common schemas.

## Pilot A — `repo-sensemaker`

Tested:

- target/currentness semantics;
- observation vs inference;
- evidence-backed claims;
- contradiction/currentness handling;
- consequential uncertainty;
- absence/completeness;
- explicit limits.

Result: the Skill already had strong evidence mechanics; the primary gain was explicit epistemic vocabulary and separation of fog/weakness classification from the specific decision-changing uncertainty.

Evidence: `pilots/pilot-a-repo-sensemaker.md` and `pilots/pilot-a-profile.yaml`.

## Pilot B — `architectural-review`

Tested:

- inherited currentness/evidence;
- Component/Layer/Boundary/Contract/Dependency semantics;
- observed dependency vs inferred architectural violation;
- ratified/documented intent;
- current defect vs proposal-contingent risk.

Result: the common warrant/provenance core transferred successfully even though the Skill inherits rather than re-collects repository evidence. Architecture-specific concepts remain local.

Evidence: `pilots/pilot-b-architectural-review.md` and `pilots/pilot-b-profile.yaml`.

## Pilot C — `repair-verifier` + `output-reconciler`

Tested:

- Change vs Outcome vs Repair;
- fresh post-change currentness;
- like-for-like validation scope;
- changed != succeeded;
- `closed/remaining` and `verified/disputed/omitted` as local enums rather than ontology replacements;
- explicit verification limits.

Result: the common core transferred into post-change reasoning. Over-broad `prove repair worked` and universal `verified` language was narrowed to the actual verification scope.

Evidence: `pilots/pilot-c-repair-reconciliation.md` and `pilots/pilot-c-profile.yaml`.

## Stable common core found

Across all pilots:

```text
target/currentness
observations or inherited observations
material claims
epistemic status
evidence refs
bounded scope / claim limits
uncertainty
explicit limits / non-claims
```

Not common-core concepts:

```text
fog/weakness taxonomies
Component/Layer/Boundary/Contract
domain verdict enums
repair closed/remaining
reconciliation verified/disputed/omitted
Campaign transition shape
```

## Phase 9 promotion decision

The repeated core warrants one **experimental Level-3 representation contract**: `semantic_reasoning_profile` v1.

The standalone validator may check representation shape, IDs, enums, evidence-ref requirements, currentness evidence presence, and explicit-limit presence. It may not judge semantic truth, evidence sufficiency, uncertainty priority, responsibility warrant, architectural correctness, repair success, or Campaign disposition.

The profile is intentionally not registered for Campaign admission.

---

# Phase 10 — Common Artifact-Semantic Envelope Experiment

**Status:** ACTIVE after Phase 9 extraction.

## Hypothesis

Several analytical workflows may benefit from a shared semantic envelope containing:

```text
target/currentness
observations
material claims
claim epistemic status
evidence refs
claim limits
uncertainties
explicit limits
```

The current `semantic_reasoning_profile` is a companion artifact that lets us test this hypothesis without modifying canonical domain artifact schemas.

## Current executable experiment

- Contract: `common-semantic-contract.md`.
- Validator: `scripts/validate-semantic-reasoning-profile.py`.
- Regression/rejection coverage: `tests/test_semantic_reasoning_profile.py`.
- Dogfood fixtures: the three checked-in Phase 9 profiles.

## Questions Phase 10 must answer

1. Does the profile materially reduce duplicated semantic reconstruction across later Skills/sessions?
2. Does it catch missing currentness/evidence/limits that otherwise change decisions?
3. Is a companion artifact enough, or do selected fields need to live in canonical analytical artifacts?
4. Does the profile create fake boilerplate claims/uncertainties merely to satisfy structure?
5. What is its token and coordination overhead?
6. Does fresh-context reconstruction improve when this profile is present?

## Promotion outcomes

After repeated real episodes, choose one:

```text
A. Keep as companion reasoning/audit profile.
B. Embed a smaller subset into multiple analytical artifacts.
C. Narrow or retire it because duplication/overhead exceeds value.
```

Do not assume B is the desired outcome.

## Rejection criterion

Reject or narrow the envelope if it produces boilerplate, duplicates domain-specific artifact fields, encourages fabricated claims/uncertainties, or transfers semantic authority to validators.

---

# Phase 11 — Mechanical Semantic Probes

**Status:** Deferred pending stable demand.

Potential mechanical relations include:

```text
TargetSnapshot identity
file containment
language-level imports/exports
manifest dependencies
artifact digests
known-membership boundary crossing
complete-scope exact search
```

Every probe must declare source/scope, completeness guarantee, currentness, blind spots, and the exact mechanical claim established. Do not name a mechanical output as if it established semantic architectural judgment.

---

# Phase 12 — Repository Semantic Map Experiment

**Status:** Deferred.

Trigger only if multiple Skills repeatedly reconstruct the same repository entities/relations and durable sharing would materially reduce inconsistency or duplicated work.

Candidate bounded artifact:

```text
RepositorySemanticMap
- target_snapshot
- scope
- entities
- relations
- claims
- contradictions
- unresolved_uncertainties
- evidence_refs
```

It must never become a complete repository source of truth.

Phase 9 did **not** provide sufficient evidence for this experiment yet.

---

# Phase 13 — Campaign / Control-Plane Promotion

**Status:** Deferred.

A semantic concept should enter Campaign schema only when:

1. it must survive across sessions to preserve consequential decision state;
2. at least two real workflows demonstrate the need;
3. semantics are stable;
4. migration can avoid semantic invention;
5. mechanical validation boundaries are clear.

The Phase 9 profile is not automatically Campaign evidence and is not registered with the Campaign artifact router.

---

# Phase 14 — Domain-Pack Extraction

**Status:** Deferred.

Trigger only after at least two domain implementations demonstrate a stable pattern such as:

```text
foundation semantics
+ responsibility vocabulary
+ capability manifests
+ artifact contracts
+ validators
+ domain Skills
```

A single PM domain remains insufficient evidence for a generic Domain Pack abstraction.

---

# Phase 15 — Ontology Conformance and Drift Checks

**Status:** Deferred.

Potential future checks may detect:

- canonical term duplicated under a new name;
- Skill-local redefinition of canonical vocabulary;
- relation used outside documented subject/object range;
- Level-1/2 concept described as runtime-enforced;
- documentation claiming executable support absent from code;
- deprecated term remaining in active contracts.

Such checks must validate consistency, not semantic truth.

---

# Metrics

Track:

```text
ambiguous terms encountered
cross-Skill concept mismatches
unsupported inference jumps
claims missing currentness
claims missing evidence
repeated semantic reconstruction
fresh-context rework
artifact boilerplate introduced
validator overreach caught
new concepts requested by real tasks
ontology concepts never used
token / coordination overhead
```

The goal is not maximum ontology coverage. The goal is **more consistent warranted reasoning per unit of coordination overhead**.

# Current next step

Run Phase 10 with additional real repository episodes using the now-executable companion profile. Do not build a central reasoning engine, universal semantic graph, or Campaign schema expansion merely because the first three pilots completed.

Preserve the development loop:

```text
observe
-> hypothesize
-> bounded experiment
-> evidence
-> smallest warranted formalization
```
