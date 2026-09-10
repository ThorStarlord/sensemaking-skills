# Relations and Epistemic Model

**Status:** Canonical Level-2 relation semantics  
**Purpose:** Make repository reasoning explicit about how relations are established, what evidence supports them, and what conclusions are prohibited.

## Why relations matter more than nouns

A repository ontology becomes useful when it can express relationships such as:

```text
Component A exposes Interface I
Module M imports Module N
Test T provides evidence for Claim C
Documentation D states Contract K
Observed dependency R contradicts RatifiedArchitecture A
Responsibility X addresses Uncertainty U
ProductChange P reinforces ProductCapability Q
```

The same entity vocabulary can support good or bad reasoning. Relation semantics determine whether conclusions remain evidence-grounded.

## Epistemic statuses

These statuses describe **how a claim or relation is grounded**, not how likely it is to be true.

### OBSERVED

Directly present in a bounded source or produced by a mechanical observation contract.

Examples:

- file A contains an import of B;
- Git HEAD is SHA X;
- test process exited 0;
- document D contains statement S.

OBSERVED does not mean semantically interpreted correctly beyond the observation contract.

### DERIVED

Produced deterministically from observed data under a declared rule.

Examples:

- target snapshot digest computed from canonical bytes;
- a dependency edge normalized from parser output;
- a transition chain shown structurally broken.

DERIVED requires the derivation rule to be identifiable.

### INFERRED

A semantic interpretation authored by an agent from evidence.

Examples:

- modules A and B appear to belong to separate architectural layers;
- a set of files jointly realizes a capability;
- an observed dependency is likely accidental.

INFERRED must preserve evidence lineage and should state scope/uncertainty when material.

### HYPOTHESIZED

A proposed explanation or relation specifically retained for investigation rather than current reliance.

Examples:

- failure is caused by configuration drift;
- duplicate implementations reflect an incomplete migration.

### RATIFIED

A semantic claim explicitly accepted by an authority competent to establish intent or policy.

Examples:

- owner-approved architectural boundary;
- accepted product requirement;
- ratified ADR.

RATIFIED establishes intended meaning or decision authority within scope. It does not force reality to conform to that intent.

### CONTRADICTED

A claim currently has credible counter-evidence or conflicts with another claim whose scope/authority makes the disagreement consequential.

CONTRADICTED does not necessarily mean definitively false. The contradiction itself becomes a first-class reasoning object.

### SUPERSEDED

A claim or relation is preserved historically but a later authoritative/current representation replaces it for present reasoning.

### UNRESOLVED

Evidence is insufficient or conflicting enough that the proposition should not be treated as established for the relevant decision.

## Recommended claim record at Level 2

A material claim conceptually has:

```text
Claim
- statement
- subject / scope
- epistemic_status
- evidence[]
- counter_evidence[]
- currentness_boundary
- authority_source?       # when status depends on ratified intent
- derived_from[]
- supersedes? / superseded_by?
```

This is a semantic model, not a mandate to add these fields to Campaign schema.

## Relation establishment classes

Every important relation should declare which establishment classes are allowed.

### Mechanical relation

A deterministic probe can establish the relation within a declared scope.

Examples:

```text
SourceFile imports Module
TestFile references Symbol
TargetSnapshot has HEAD
Artifact has SHA-256
```

### Evidence-supported semantic relation

Evidence supports the relation, but semantic interpretation is required.

Examples:

```text
Component realizes SoftwareCapability
Test validates BehaviorClaim
Documentation defines expected Contract
```

### Agent-inferred relation

The active agent authors the relation from evidence.

Examples:

```text
Component belongsToLayer Layer
Dependency violates ArchitectureContract
Change resolves Contradiction
```

### Human-ratified relation

An owner or competent authority establishes intended semantics.

Examples:

```text
Component ownedBy Team
Layer A mayDependOn Layer B
ProductCapability isStrategicPriority
```

A relation can accumulate multiple establishment classes over time. For example, an agent-inferred architecture boundary may later become ratified.

## Core relation dictionary

### Structural relations

#### `contains`

**Meaning:** one repository/system entity structurally includes another.  
**Often mechanical:** yes for directories/files; semantic for Component containment.  
**Prohibited inference:** directory containment does not automatically establish architectural ownership.

#### `imports`

**Meaning:** source code contains a language-level import/reference according to a parser/probe contract.  
**Often mechanical:** yes.  
**Prohibited inference:** import does not automatically establish undesirable coupling.

#### `calls`

**Meaning:** one executable element invokes another under a bounded analysis.  
**Mechanical status:** language/tool dependent.  
**Prohibited inference:** static call evidence may not establish runtime execution.

#### `exposes`

**Meaning:** an entity presents an interface/endpoint/capability for consumption outside itself.  
**Usually semantic unless explicit framework metadata establishes it.**

#### `dependsOn`

**Meaning:** one entity relies on another for satisfaction of a behavior, build, runtime, data, configuration, or contract condition.  
**Evidence requirement:** identify dependency kind and source when material.  
**Prohibited inference:** one import edge is not always equivalent to a meaningful architectural dependency.

#### `crossesBoundary`

**Meaning:** a relation connects entities classified on different sides of a named Boundary.  
**Derivation:** may be deterministic once the Boundary membership itself is established.  
**Prohibited inference:** crossing a boundary does not itself imply violation.

### Realization and contract relations

#### `realizes`

**Meaning:** an implementation entity contributes materially to a SoftwareCapability or ProductCapability.  
**Usually:** inferred or ratified.  
**Evidence:** implementation, tests, runtime behavior, docs, or owner intent.

#### `implementsContract`

**Meaning:** an implementation claims to satisfy a Contract.  
**Evidence:** code/schema/interface + supporting behavioral evidence.  
**Prohibited inference:** syntactic interface compatibility does not necessarily establish behavioral conformance.

#### `tests`

**Meaning:** a Test is intended to exercise an entity, contract, or behavior.  
**Evidence:** test code and/or explicit metadata.  
**Prohibited inference:** `tests` relation does not establish sufficient coverage.

#### `documents`

**Meaning:** Documentation describes an entity, contract, decision, or capability.  
**Prohibited inference:** documentation existence does not establish currentness or authority.

### Evidence relations

#### `supports`

**Meaning:** evidence increases warrant for a Claim within a stated scope.  
**Semantic authority:** agent/human unless the claim is purely mechanical.  
**Prohibited inference:** supporting evidence does not imply proof.

#### `contradicts`

**Meaning:** evidence or a claim is materially incompatible with another claim in overlapping scope.  
**Requirement:** preserve both sides and identify the conflict basis.

#### `derivedFrom`

**Meaning:** a claim, observation, artifact, or relation was produced from another source/claim through a named method.  
**Often mechanical for digests/transforms; semantic for reasoning chains.**

#### `validates`

**Meaning:** a Validation operation evaluates a target against a declared contract.  
**Requirement:** validation scope/contract must be explicit.  
**Prohibited inference:** validation success beyond that scope.

#### `admittedAsEvidence`

**Meaning:** exact bytes/identity passed the Campaign admission contract and became durable evidence.  
**Mechanical:** yes where Campaign admission applies.  
**Prohibited inference:** admission does not establish semantic correctness.

### Reasoning/work relations

#### `concerns`

Links Claim/Uncertainty/Responsibility to its semantic subject.

#### `blocksDecision`

**Meaning:** resolving an Uncertainty could materially change a named Decision.  
**Semantic:** agent-authored.

#### `addresses`

**Meaning:** a Responsibility is intended to resolve/narrow an Uncertainty, Contradiction, Goal, or problem condition.

#### `fulfillsResponsibilityType`

**Meaning:** a SensemakingCapability declares that it can perform a class of Responsibility.  
**Mechanical:** registry lookup can establish declaration/availability.  
**Prohibited inference:** declaration does not mean selection is warranted.

#### `authorizes`

**Meaning:** an Authority permits a defined action under a scope.  
**Requirement:** do not infer authorization from capability availability.

#### `modifies`

**Meaning:** a Change alters a target entity/state.  
**Mechanical:** target diff may establish bytes/entities changed.  
**Prohibited inference:** modification does not establish intended outcome.

#### `resolves`

**Meaning:** a result/change sufficiently addresses a Claim, Contradiction, or Uncertainty for a declared decision.  
**Semantic:** requires evidence and agent/owner judgment except for narrowly mechanical questions.

#### `supersedes`

**Meaning:** a newer claim/artifact/decision replaces another for current reasoning while preserving historical provenance.

### Product relations

#### `reinforces`

A ProductChange increases the value/usefulness of an existing ProductCapability without necessarily extending its scope.

#### `extends`

A ProductChange broadens the scope of an existing ProductCapability.

#### `enables`

A ProductChange creates a prerequisite or reusable foundation for another ProductChange/Capability.

#### `createsValueBy`

Links ProductChange to a descriptive ValueMechanism.

None of these relations imply priority.

## Temporal and scope rules

A material repository relation should be interpreted as:

```text
Relation R
applies within Scope X
at CurrentnessBoundary Y
based on Evidence Z
with EpistemicStatus S
```

If the target state changes, the relation may remain valid, become stale, or require re-observation. Do not silently carry repository-state claims across snapshots.

## Contradiction model

A contradiction should preserve:

```text
claim_a
claim_b or counter_evidence
scope overlap
currentness of each side
authority of each side
why they are incompatible
resolution status
```

Common contradiction classes include:

```text
implementation vs documentation
implementation vs ratified architecture
test evidence vs runtime evidence
current state vs stale diagnosis
two authoritative contracts
two Skills using one term differently
```

Contradiction is a reason to investigate or clarify. It is not itself an automatic repair authorization.

## Absence claims

Claims such as:

```text
"there are no tests for capability X"
"no module depends on Y"
"the repository contains no implementation of Z"
```

require an explicit completeness basis.

A valid absence reasoning pattern is:

```text
probe contract searched complete declared scope S
+ probe found zero matching observations
-> DERIVED absence claim within S
```

A repository text search that happened to find no match does not automatically justify the same claim.

## Invalid inference catalog

The following shortcuts are prohibited by the semantic model:

```text
directory -> Component
import -> architecture violation
passing test -> full behavior correct
validator PASS -> semantic conclusion true
changed files -> repair succeeded
document says X -> X is current
artifact admitted -> artifact conclusion warranted
capability exists -> capability should run
capability available -> action authorized
human intent -> implementation currently conforms
no search result -> entity absent
high confidence prose -> stronger evidence
```

Skills should surface these boundaries when they materially affect a decision.