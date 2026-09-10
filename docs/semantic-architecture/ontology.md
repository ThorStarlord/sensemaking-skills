# Layered Ontology

**Status:** Canonical Level-2 semantic model, v0  
**Important:** This ontology is descriptive. It does not imply that every concept is represented in Campaign schema or mechanically detectable.

## Design principles

The ontology is layered so concepts with different semantic roles do not collapse into one flat vocabulary.

```text
Intent
  constrains
SoftwareSystem
  produces / exposes
Evidence
  supports / contradicts
Knowledge
  motivates
Work
  changes
SoftwareSystem
  realizes
Product
```

The same concrete object may participate in several layers through relations, but its roles remain explicit.

## Layer 1 — Intent ontology

### Goal

An outcome the user or owner wants to achieve.

### Mission

A durable Campaign-level goal that organizes multiple responsibilities or decisions.

### Requirement

A condition the solution is expected to satisfy.

### Constraint

A restriction on acceptable actions, solutions, scope, resources, or behavior.

### SuccessCondition

A condition whose satisfaction is relevant to deciding whether a responsibility or mission can be considered complete.

### RatifiedIntent

Intent explicitly confirmed by the owner or another valid authority. Ratified intent outranks agent-inferred intent when the meanings conflict.

### Relations

```text
Goal decomposesInto Requirement
Goal constrainedBy Constraint
Mission governedBy Goal
SuccessCondition evaluates Goal | Requirement | Responsibility
RatifiedIntent governs SoftwareSystem | Work
```

## Layer 2 — Repository and software-system ontology

### Repository

A versioned software-engineering target containing implementation and associated engineering artifacts.

### TargetSnapshot

A mechanically bounded observation of repository identity and state at a point in time. The existing Campaign `TargetSnapshot` is the canonical executable instance of this concept.

### RepositoryElement

Abstract parent for structural elements represented by the repository.

Candidate specializations:

```text
Package
Module
SourceFile
Symbol
Function
Class
Interface
Endpoint
Schema
Configuration
Test
Fixture
BuildDefinition
Workflow
Documentation
GeneratedArtifact
```

These are Level-2 vocabulary. Language-specific parsers may later introduce narrower subtypes without changing foundation semantics.

### SoftwareCapability

A behavior or ability provided by the software system. A software capability is distinct from a Sensemaking `Capability`, which is an ability of the agent/tooling environment to perform a responsibility.

Use qualified names when ambiguity is possible:

```text
SoftwareCapability
SensemakingCapability
ProductCapability
```

### Component

A semantically meaningful software unit that groups implementation around a responsibility, capability, runtime role, or architectural boundary. A directory is not automatically a Component.

### Layer

An architectural grouping whose relationships may be constrained by design intent.

### Boundary

A semantic separation between components, layers, domains, trust zones, processes, repositories, or authority domains.

### Contract

An explicit or relied-upon agreement governing behavior, structure, data, interface, or interaction.

Candidate specializations:

```text
APIContract
SchemaContract
BehaviorContract
ArchitectureContract
ArtifactContract
AuthorityContract
```

### DependencyRelation

A relation in which one software entity relies on another for behavior, data, configuration, build, runtime, or contract satisfaction.

### Ownership

Responsibility for maintaining or authoritatively defining a software concern, component, contract, or artifact.

### Runtime

An execution environment or runtime role in which software behavior occurs.

### DataFlow

Movement or transformation of data between entities.

### ControlFlow

Transfer of execution/control between entities.

### Core structural relations

```text
Repository contains RepositoryElement
Component contains RepositoryElement
RepositoryElement imports RepositoryElement
RepositoryElement exports Symbol | Interface
RepositoryElement calls RepositoryElement
RepositoryElement configures RepositoryElement | Runtime
RepositoryElement tests RepositoryElement | SoftwareCapability | Contract
RepositoryElement documents RepositoryElement | SoftwareCapability | Contract
RepositoryElement generates GeneratedArtifact
Component exposes Interface | Endpoint | SoftwareCapability
Component dependsOn Component | Contract | Runtime
Component belongsToLayer Layer
DependencyRelation crosses Boundary
SoftwareCapability realizedBy Component | RepositoryElement[]
Contract implementedBy Component | RepositoryElement
Ownership appliesTo Component | Contract | SoftwareCapability
```

## Layer 3 — Evidence ontology

### EvidenceSource

The source from which evidence originates.

Examples:

```text
repository bytes
Git metadata
probe output
test output
runtime logs
documentation
issue / PR
external system
human statement
```

### Observation

A bounded statement about what was directly detected or provided by an evidence source.

Examples:

```text
"A imports B"
"test T passed"
"ADR X says dependency direction D is prohibited"
"HEAD is SHA H"
```

Observation should preserve source, scope, and currentness.

### ProbeResult

A mechanically produced observation set under a declared probe contract.

### Artifact

A durable produced representation used in reasoning or execution.

### AdmittedEvidence

Evidence whose exact bytes/identity have passed the relevant Campaign admission boundary. Admission does not imply semantic truth.

### CounterEvidence

Evidence materially inconsistent with, narrowing, or weakening a claim.

### ValidationEvidence

Evidence produced by a validator or test about satisfaction of a declared mechanical or behavioral condition.

### Provenance

Information linking evidence to source, target state, producing capability, exact bytes, validation, time, and later consumers.

### Evidence relations

```text
Observation derivedFrom EvidenceSource
ProbeResult contains Observation
Artifact contains | represents Observation | Claim
AdmittedEvidence derivedFrom Artifact
Evidence supports Claim
Evidence contradicts Claim
Evidence qualifies Claim
Evidence hasProvenance Provenance
Evidence appliesTo TargetSnapshot | scope
```

## Layer 4 — Knowledge and epistemic ontology

### Claim

A proposition about intent, software, evidence, work, product, or another claim.

### EstablishedFact

A Campaign/documentary label for a claim treated as established within a declared scope. The label does not erase provenance or make the proposition metaphysically infallible.

### Hypothesis

A claim proposed for investigation and not yet treated as established.

### Assumption

A proposition temporarily relied upon without sufficient direct evidence for stronger status.

### Uncertainty

A question whose unresolved answer may affect a decision, responsibility, scope, authority, or conclusion. The existing Campaign `Uncertainty` is the executable control-plane representation.

### Contradiction

A represented incompatibility between claims or between observed state and an expected/ratified contract.

### Decision

An agent- or owner-authored semantic choice informed by available evidence, uncertainty, responsibility, capability, and authority.

### EpistemicStatus

A classification of how a claim or relation is currently grounded. Canonical statuses are defined in `relations-and-epistemics.md`.

### Knowledge relations

```text
Claim concerns OntologyEntity
Claim supportedBy Evidence
Claim contradictedBy Evidence | Claim
Claim derivedFrom Claim | Observation
Claim hasEpistemicStatus EpistemicStatus
Hypothesis specializes Claim
Assumption specializes Claim
Uncertainty concerns Claim | missing Claim
Uncertainty blocks Decision
Contradiction relates Claim <-> Claim
Decision cites Evidence | Claim
```

## Layer 5 — Engineering-work ontology

### Responsibility

A bounded kind of work warranted by semantic judgment. Existing Campaign `Responsibility` is authoritative for executable Campaign state.

### SensemakingCapability

A Skill, tool, workflow, ordinary engineering ability, or other declared mechanism capable of performing a Responsibility.

### CapabilityAvailability

Whether a declared SensemakingCapability is mechanically available in the current environment.

### Authority

Permission classification governing whether an action may be taken. Existing Campaign `Authority` remains authoritative for executable Campaign state.

### Change

A modification to repository state, external state, documentation, configuration, or another controlled target.

### Repair

A Change intended to resolve a previously identified problem/contradiction.

### Validation

An evaluation against an explicit contract, condition, or expected behavior. Validation scope must be declared.

### Outcome

A result of work. Outcome is distinct from successful satisfaction of the motivating responsibility.

### Transition

A durable change in Campaign decision state.

### Handoff

A durable representation intended to allow continuation in a fresh context.

### TerminalState

An explicit classification for stopping or closing a Campaign path.

### Work relations

```text
Responsibility addresses Uncertainty | Goal | Contradiction
SensemakingCapability fulfills ResponsibilityType
SensemakingCapability produces Artifact | Change | Evidence
CapabilityAvailability describes SensemakingCapability
Authority authorizes Action
Change modifies SoftwareSystem | RepositoryElement
Repair specializes Change
Repair targets Contradiction | Claim | FailureCondition
Validation evaluates Artifact | Change | Claim | SuccessCondition
Outcome producedBy SensemakingCapability | Change
Decision selects Responsibility | SensemakingCapability | Transition
Transition cites Evidence
Handoff reconstructs CampaignState
```

## Layer 6 — Product ontology

### ProductCapability

A user-meaningful ability the product provides.

### Feature

A concrete product surface or mechanism through which one or more ProductCapabilities are realized or accessed.

### Initiative

A bounded strategic effort that may contain multiple ProductChanges and features in service of an outcome.

### ProductChange

A proposed or implemented modification to the product.

### ChangeType

A descriptive category for the structural nature of a ProductChange.

### ValueMechanism

A descriptive category for how a ProductChange creates value.

### UserWorkflow

A sequence of user actions/outcomes through which product value is obtained.

### QualityAttribute

A quality dimension such as reliability, usability, portability, observability, performance, security, or maintainability.

### Product relations

```text
ProductCapability realizedBy Feature | SoftwareCapability
Feature supportedBy SoftwareCapability
Initiative contains ProductChange
ProductChange affects ProductCapability | Feature | UserWorkflow | QualityAttribute
ProductChange hasChangeType ChangeType
ProductChange createsValueBy ValueMechanism
ProductChange reinforces ProductCapability
ProductChange extends ProductCapability
ProductChange enables ProductChange | ProductCapability
ProductChange improves QualityAttribute
```

The detailed taxonomy is defined in `product-change-taxonomy.md`.

## Cross-layer relations

The ontology becomes useful primarily through cross-layer relations:

```text
RatifiedIntent constrains Contract
Contract constrains DependencyRelation
Observation describes DependencyRelation
Evidence supports Claim
Claim says DependencyRelation crosses Boundary
RatifiedIntent says relation is prohibited
Contradiction relates observed claim to expected claim
Uncertainty concerns Contradiction
Responsibility addresses Uncertainty
SensemakingCapability fulfills Responsibility
Change modifies DependencyRelation
ValidationEvidence supports repair Claim
Decision advances Campaign Transition
```

## Semantic namespace rule

When the word `capability` is used without context, ambiguity is possible. Canonical writing should distinguish:

```text
SoftwareCapability  = ability of the target software
ProductCapability   = user-facing product ability/value
SensemakingCapability = ability of a Skill/tool/environment to perform work
```

Likewise, `artifact` should be qualified where necessary as source artifact, generated artifact, Campaign artifact, or evidence artifact.

## What this ontology intentionally does not encode

The ontology does not define:

- numerical confidence thresholds;
- automatic relation inference rules for semantic architecture;
- a universal component-detection algorithm;
- automatic product prioritization;
- automatic responsibility or capability selection;
- permission to mutate a repository;
- a requirement that every relation be materialized as a graph node/edge.

Those would require separate evidence and authorization.