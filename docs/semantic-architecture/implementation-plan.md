# Semantic Architecture Implementation Plan

**Status:** Active plan for semantic-foundation work  
**Current milestone:** Documentation foundation only  
**Implementation principle:** Formalize from demonstrated reasoning pressure; do not manufacture runtime machinery to make the ontology look complete.

## Objective

Create a shared semantic foundation that lets Sensemaking Skills reason consistently about unfamiliar repositories while preserving evidence lineage, currentness, uncertainty, semantic authority, and the existing agent/deterministic control boundary.

The plan deliberately separates **documentation completion** from **executable promotion**.

## Definition of done for the foundation milestone

The foundation milestone is complete when the repository contains:

- a semantic constitution;
- a problem statement;
- competency questions;
- an inventory of existing concepts;
- a layered ontology;
- product-change taxonomy;
- relation and epistemic semantics;
- a reasoning model;
- execution integration architecture;
- reference scenarios;
- this implementation/promotion plan;
- a milestone handoff explaining what remains non-executable.

Completion of this milestone does **not** mean the ontology has been encoded into schemas or a graph runtime.

---

# Phase 0 — Preserve architecture boundary

## Goal

Ensure semantic formalization does not undo the product's strongest existing invariant.

## Deliverables

- `constitution.md`
- explicit mapping to Campaign semantic-control boundary
- prohibited-inference catalog

## Gate

PASS only if the documents preserve:

```text
agent semantic judgment
!= deterministic validation / persistence / provenance
```

## Completed in foundation milestone

Yes.

---

# Phase 1 — Problem definition

## Goal

Define the concrete failure mode that motivates shared semantics.

## Deliverables

- `problem-statement.md`
- examples of cross-Skill semantic inconsistency
- explicit non-goals
- primary design question

## Gate

The initiative must be justified by inconsistent reasoning semantics, not by a generic desire for a knowledge graph.

## Completed in foundation milestone

Yes.

---

# Phase 2 — Competency questions

## Goal

Define what the model must be able to express before choosing ontology breadth.

## Deliverables

- `competency-questions.md`
- grouped questions covering intent, currentness, structure, architecture, contracts, evidence, uncertainty, responsibility, change, product, documentation, and handoff
- initial high-priority subset

## Gate

Every new Level-2 ontology concept should map to at least one competency question.

## Completed in foundation milestone

Yes: initial inventory contains 78 questions.

---

# Phase 3 — Existing concept inventory and reconciliation

## Goal

Derive the semantic model from what Sensemaking already means rather than creating a competing vocabulary.

## Evidence sources

At minimum:

```text
src/sensemaking_skills/campaign_semantics/
src/sensemaking_skills/campaigns/
docs/sensemaking-campaign.md
docs/decision-orchestration-boundary.md
repo-sensemaker
architectural-review
problem-framer
unknowns-mapper
output-reconciler
repair-verifier
docs-aligner
PM domain docs/Skills
artifact contracts
validators
```

## Deliverables

- `concept-inventory.md`
- mapping of existing Campaign concepts to ontology layers
- list of implicit recurring repository concepts
- list of Skill-local diagnostic terms not yet suitable for canonicalization

## Gate

No new canonical term may duplicate an existing executable concept without an explicit reconciliation decision.

## Completed in foundation milestone

Baseline complete. Future Skill-by-Skill reconciliation remains incremental work.

---

# Phase 4 — Layered ontology

## Goal

Define a minimal shared ontology without flattening distinct semantic domains.

## Layers

```text
1. Intent
2. Repository / Software System
3. Evidence
4. Knowledge / Epistemics
5. Engineering Work
6. Product
```

## Deliverables

- `ontology.md`
- canonical namespace rule for `SoftwareCapability`, `SensemakingCapability`, `ProductCapability`
- cross-layer relation examples

## Gate

The ontology must express the reference scenarios without requiring domain-specific concepts in the foundation unnecessarily.

## Completed in foundation milestone

Yes at Level 2 documentation status.

---

# Phase 5 — Relationship and epistemic model

## Goal

Define how claims and relations are established, supported, contradicted, scoped, and superseded.

## Deliverables

- `relations-and-epistemics.md`
- epistemic statuses
- relation-establishment classes
- relation dictionary
- temporal/currentness rules
- contradiction model
- absence-claim rule
- invalid-inference catalog

## Gate

Every relation considered for executable promotion must state:

```text
meaning
allowed subjects/objects
establishment method
required evidence
currentness/scope behavior
prohibited inference
```

## Completed in foundation milestone

Yes at Level 2 documentation status.

---

# Phase 6 — Reasoning architecture

## Goal

Define the canonical reasoning lifecycle from intent/target binding through handoff.

## Deliverables

- `reasoning-model.md`
- stage ownership: deterministic vs agent vs human/authority
- bounded semantic-map construction
- stopping rule

## Gate

The reasoning architecture must not contain a hidden semantic router. The agent selects consequential uncertainty, warranted responsibility, semantically appropriate capability, and decision disposition.

## Completed in foundation milestone

Yes at design level.

---

# Phase 7 — Integration architecture

## Goal

Define how shared semantics should influence existing product surfaces before adding new infrastructure.

## Deliverables

- `execution-integration.md`
- probe boundary
- Skill adoption policy
- artifact integration policy
- validator boundary
- Campaign schema boundary
- capability-registry boundary
- handoff guidance
- domain-extension pattern
- deferred Repository Semantic Map concept

## Gate

No Campaign schema or runtime change is justified merely because the ontology contains a concept.

## Completed in foundation milestone

Yes at design level.

---

# Phase 8 — Reference scenarios

## Goal

Test whether the ontology reduces ambiguity in concrete reasoning situations.

## Initial scenarios

```text
A architecture drift
B missing capability vs missing implementation
C documentation/code contradiction
D failed repair despite changed repository
E product enhancement proposal
F fresh-context continuation
G passing test with insufficient coverage
H capability available but unauthorized
I absence claim from incomplete search
J vocabulary drift across Skills
K multi-source contradiction
L enabler mistaken for user feature
```

## Deliverables

- `reference-scenarios.md`

## Gate

The model should reduce hidden inference jumps, not merely name more entities.

## Completed in foundation milestone

Yes.

---

# Phase 9 — Skill semantic-alignment pilots

**Status:** Next empirical phase; NOT completed by documentation alone.

## Goal

Test the semantic model against real Skill behavior before creating universal schemas.

## Recommended pilots

### Pilot A — `repo-sensemaker`

Test:

- target/currentness semantics;
- observation vs inference;
- evidence-backed claims;
- contradiction/currentness handling;
- unknowns/uncertainty representation.

### Pilot B — `architectural-review`

Test:

- Component/Layer/Boundary/Contract/Dependency relations;
- observed dependency vs inferred architectural violation;
- ratified intent;
- cross-boundary reasoning.

### Pilot C — `repair-verifier` or `output-reconciler`

Test:

- Change vs Outcome vs Repair;
- validation scope;
- changed != succeeded;
- supersession/reconciliation.

## Deliverables

For each pilot:

```text
before/after semantic vocabulary audit
competency questions exercised
ambiguities removed
new concepts requested
concepts unused
operator/agent friction
invalid inferences prevented
```

## Promotion gate

Do not create common executable semantic fields until at least two pilots demonstrate stable reuse.

---

# Phase 10 — Common artifact-semantic envelope experiment

**Status:** Deferred pending Phase 9 evidence.

## Hypothesis

Several analytical artifacts may benefit from a shared minimal envelope containing:

```text
target/currentness
material claims
claim epistemic status
evidence refs
counter-evidence / contradictions
uncertainties
explicit limits
```

## Test

Implement the envelope only in a bounded experiment across two or more artifact types.

## Rejection criterion

Reject or narrow the envelope if it produces boilerplate, duplicates domain-specific artifact fields, or encourages claims to be generated merely to satisfy schema.

---

# Phase 11 — Mechanical semantic probes

**Status:** Deferred pending stable demand.

## Candidate deterministic relations

Only relations with strong mechanical boundaries are candidates, for example:

```text
TargetSnapshot identity
file containment
language-level imports/exports
manifest dependencies
artifact digests
known-membership boundary crossing
complete-scope exact search
```

## Requirements

Every probe must declare:

- source and scope;
- completeness properties;
- currentness;
- blind spots;
- exact mechanical claim established.

## Rejection criterion

Do not implement a probe whose output name hides semantic interpretation behind a mechanical-sounding label.

---

# Phase 12 — Repository Semantic Map experiment

**Status:** Explicitly deferred.

## Trigger

Start only if multiple Skills repeatedly reconstruct the same repository entities/relations and durable sharing would materially reduce inconsistency or duplicated work.

## Candidate bounded artifact

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

## Non-goal

The map is not intended to be a complete repository graph or source of truth.

## Success criterion

A fresh Skill/agent can consume the map and answer target competency questions with less duplicated investigation **without losing evidence lineage or over-trusting stale derived context**.

---

# Phase 13 — Campaign/control-plane promotion

**Status:** Explicitly deferred.

## Trigger

A semantic concept should enter Campaign schema only when:

1. it must survive across sessions to preserve a consequential decision state;
2. at least two real workflows demonstrate the need;
3. its semantics are stable;
4. migration behavior can avoid semantic invention;
5. mechanical validation boundaries are clear.

## Examples

Potential future candidates might include structured claim status or contradiction references. `Component`, `Feature`, or every repository relation are unlikely to belong directly in Campaign state without stronger evidence.

---

# Phase 14 — Domain-pack extraction

**Status:** Deferred.

## Trigger

At least two domain implementations demonstrate a stable pattern such as:

```text
foundation semantics
+ responsibility vocabulary
+ capability manifests
+ artifact contracts
+ validators
+ domain Skills
```

PM is one candidate domain but is insufficient alone to prove a generic Domain Pack abstraction.

---

# Phase 15 — Ontology conformance and drift checks

**Status:** Deferred.

Possible future checks:

- canonical term duplicated under different names;
- one Skill locally redefines a canonical term;
- relation used outside documented subject/object range;
- Level-1 taxonomy described as runtime-enforced;
- documentation claims executable support absent from code;
- deprecated term remains in active contracts.

These checks should focus on consistency, not semantic truth.

---

# Promotion ladder

The default lifecycle for a new concept is:

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
        | mechanically expressible boundary
        v
Level 3: executable contract
```

## Level 1 -> Level 2 gate

Require:

- at least one competency question;
- repeated semantic use or critical boundary value;
- clear definition;
- no canonical duplicate;
- useful relations to existing concepts.

## Level 2 -> Level 3 gate

Require:

- evidence from at least two real workflows unless safety/integrity requires earlier action;
- stable semantic meaning;
- identified mechanical subset;
- explicit validator scope;
- migration/backward-compatibility consideration;
- negative/rejection cases;
- no transfer of semantic authority to deterministic machinery.

---

# Work-package strategy

Once Phase 9 begins, work should proceed in small packages driven by evidence:

```text
Package 1: align one Skill + record findings
Package 2: align second contrasting Skill + reconcile vocabulary
Package 3: extract smallest repeated semantic contract
```

Do not schedule ontology implementation by document section (for example, "implement every entity in ontology.md"). That would optimize for ontology completeness instead of product usefulness.

---

# Metrics for future experiments

Track qualitative/quantitative evidence such as:

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
```

The goal is not maximum ontology coverage. The goal is **more consistent warranted reasoning per unit of coordination overhead**.

---

# Immediate next step after this foundation milestone

Do not create a universal semantic schema.

Run **Phase 9 Pilot A (`repo-sensemaker`)** on a real repository episode and produce an evidence record showing where the shared model improves or complicates reasoning. Then run a contrasting architecture or repair pilot before extracting executable common fields.

This preserves the repository's existing discipline:

```text
observe
-> hypothesize
-> bounded experiment
-> evidence
-> smallest warranted formalization
```