# Existing Concept Inventory

**Status:** Baseline inventory of concepts already present in Sensemaking  
**Purpose:** Prevent the semantic architecture from creating a parallel vocabulary beside the current product.

## Principle

The ontology should be **reconciled from existing product semantics first** and extended only where demonstrated reasoning gaps remain.

This inventory separates:

- concepts already represented in executable code;
- concepts already canonical in product documentation or Skills;
- concepts that are common but still implicit;
- candidate concepts introduced by this semantic-architecture initiative.

## 1. Existing executable Campaign concepts

The current Campaign semantic model already defines important control-plane entities.

| Existing concept | Current role | Semantic-architecture mapping |
|---|---|---|
| `CampaignState` | Durable current campaign representation | Work / decision-state aggregate |
| `CampaignConstitution` | Mission, principles, non-goals, terminal states | Intent + governance |
| `Responsibility` | Bounded work warranted by agent judgment | Work ontology: Responsibility |
| `DeferredResponsibility` | Responsibility preserved with reopening conditions | Work ontology: deferred responsibility |
| `Uncertainty` | Decision-changing question with consequences | Knowledge ontology: Uncertainty |
| `Authority` | Action-authority classification | Work ontology: Authority |
| `Capability` | Declared ability accepting responsibility types | Work ontology: Capability |
| `CapabilityAvailability` | Mechanical availability status | Work ontology: CapabilityAvailability |
| `ClaimEvidence` | Claim/evidence coverage record | Evidence + knowledge bridge |
| `Dependency` / `DependencyType` | Task, evidence, authority dependency | Generic dependency relation specialized by type |
| `ExternalBoundary` | External capability/owner/access boundary | Authority + system-boundary relation |
| `TargetSnapshot` | Mechanically observed Git target identity/state | Repository ontology: TargetSnapshot |
| `TransitionRecord` | Durable state transition with evidence and authority | Work ontology: DecisionTransition |
| `CampaignPolicy` | Known transitions, boundaries, stop conditions | Governance / policy metadata |
| `CampaignHandoff` | Durable continuation representation | Work ontology: Handoff |
| `CampaignTrace` | Durable event trace | Evidence/provenance ontology |
| `TerminalState` | Explicit closure/stop classification | Work ontology: TerminalState |
| `ValidationDiagnostic` | Mechanical integrity diagnostic | Validation evidence |
| `ReconstructionResult` | Structural reconstruction validity | Validation result |

### Existing invariant to preserve

These types deliberately do not claim semantic truth. For example, Campaign validation can establish that evidence references exist or that transitions reconstruct; it does not establish that an agent's architectural conclusion was wise.

The semantic architecture MUST preserve this control boundary.

## 2. Existing Campaign-service concepts

Current `campaigns/` modules already imply a second layer of concepts:

| Surface | Existing semantic concept |
|---|---|
| `admission.py` | artifact admission, admitted evidence |
| `artifacts.py` | canonical artifact identity and bytes |
| `capabilities.py` | capability discovery and declared compatibility |
| `decisions.py` | explicit agent-authored advance/defer/close decisions |
| `handoff.py` | durable continuation / reconstruction |
| `lineage.py` | provenance and evidence lineage |
| `narrative.py` | exact narrative claim binding and verification receipt |
| `reconciliation.py` | later evidence compared with prior result/state |
| `schema_evolution.py` | representation migration without semantic invention |
| `service.py` | Campaign operations |
| `store.py` | durable representation / integrity boundary |
| `target_snapshot.py` | target repository identity and state evidence |

The ontology should name these concepts consistently but should not automatically mirror every service class as an ontology class.

## 3. Existing canonical product distinctions

The repository already treats the following distinctions as architecturally important:

```text
warranted responsibility != available capability != authorized capability
validator passed != semantic truth
file exists != validated artifact != admitted evidence != semantic decision
repository changed != repair succeeded
narrative claim bound to evidence != evidence proves claim
handoff != semantic recommendation
Skill installed != Skill observed or invoked by harness
repository qualified != native-harness qualified != portability qualified != promoted
```

These distinctions are stronger than ordinary vocabulary. They are candidate **semantic invariants** and should guide ontology relations and prohibited inference.

## 4. Existing Skill-level concepts

Multiple Skills already reason using concepts that should be reconciled into shared vocabulary.

### Repository diagnosis

Common existing concepts include:

- repository state;
- target evidence;
- currentness;
- primary fog;
- weakest boundary;
- contract mismatch;
- vocabulary drift;
- ghost feature;
- safety gap;
- implicit dependency;
- zero validation;
- orphaned example.

Not all of these should become ontology roots. Most are better modeled as **problem/claim patterns** composed from more general entities and relations.

Example:

```text
ContractMismatch
= observed implementation relation
  contradicts
  expected/ratified contract claim
```

### Architecture review

Common concepts include:

- component;
- boundary;
- dependency;
- ownership;
- coupling;
- responsibility;
- contract;
- architecture drift.

These are high-priority candidates because several repository-analysis Skills need them.

### Documentation reconciliation

Common concepts include:

- documentation authority;
- currentness;
- implementation evidence;
- terminology drift;
- stale claim;
- alignment;
- contradiction.

### Repair verification / reconciliation

Common concepts include:

- original failure/claim;
- target condition;
- produced change;
- validation evidence;
- regression evidence;
- residual uncertainty;
- supersession/reconciliation.

## 5. Existing Product Management concepts

The current PM domain adds useful evidence that the Campaign substrate can host domain-specific responsibilities without redefining the core.

Current canonical PM responsibility sequence includes concepts such as:

```text
customer_understanding
problem_discovery
research_synthesis
opportunity_mapping
product_hypothesis
```

The lesson for semantic architecture is architectural, not merely PM-specific:

```text
foundation ontology
+ bounded domain ontology
+ domain Skills
+ domain artifact contracts
```

is preferable to placing every domain concept into the repository-reasoning foundation.

## 6. Concepts currently implicit and worth formalizing at Level 1/2

These concepts recur in repository reasoning but are not yet a unified executable vocabulary:

### Intent

- Goal
- Requirement
- Constraint
- SuccessCondition
- RatifiedIntent

### Repository structure

- Repository
- Package
- Module
- SourceFile
- Symbol
- Function
- Class
- Interface
- Endpoint
- Schema
- Configuration
- Test
- Fixture
- BuildDefinition
- Workflow
- Documentation
- GeneratedArtifact

### Architecture

- SoftwareCapability
- Component
- Layer
- Boundary
- Contract
- DependencyRelation
- Ownership
- Runtime
- DataFlow
- ControlFlow

### Evidence and knowledge

- EvidenceSource
- Observation
- ProbeResult
- Claim
- Fact
- Hypothesis
- Assumption
- Contradiction
- CounterEvidence
- EpistemicStatus
- CurrentnessBoundary

### Work and change

- Change
- Outcome
- Validation
- Repair
- Supersession
- Reconciliation

### Product

- ProductCapability
- Feature
- Initiative
- ProductChange
- ChangeType
- ValueMechanism
- QualityAttribute
- UserWorkflow

## 7. Terms that should NOT be blindly canonicalized

Some useful Skill phrases are likely patterns rather than foundational entities:

- `product_fog`;
- `architecture_fog`;
- `docs_fog`;
- `ghost_feature`;
- `orphaned_example`;
- `zero_validation`;
- `weakest_boundary`.

They should remain Skill-level diagnostic vocabulary unless repeated reasoning demonstrates a stable cross-Skill semantic contract.

## 8. Reconciliation rules

When a new ontology term appears to overlap an existing concept:

1. prefer the existing canonical term if meanings match;
2. specialize it if the new concept is genuinely narrower;
3. namespace it if it belongs to a domain-specific ontology;
4. deprecate one term explicitly if two names represent the same meaning;
5. preserve historical names in provenance but do not keep competing current meanings.

## 9. Initial mapping examples

```text
Campaign TargetSnapshot
  -> Repository ontology / TargetSnapshot

Campaign Uncertainty
  -> Knowledge ontology / Uncertainty

Campaign Responsibility
  -> Work ontology / Responsibility

Campaign Capability
  -> Work ontology / Capability

Campaign ClaimEvidence
  -> Knowledge.Claim supportedBy Evidence

repo-sensemaker "contract mismatch"
  -> Claim A contradicts ContractClaim B

architectural-review "boundary violation"
  -> DependencyRelation crosses Boundary
     AND RatifiedArchitecture disallows relation

repair-verifier "repair succeeded"
  -> Agent conclusion supported by validation evidence;
     never derived merely from changed target bytes
```

## 10. Baseline conclusion

Sensemaking does not need a semantic model from scratch. It already contains a strong **control-plane ontology in embryo**. The new initiative should connect that control-plane vocabulary to a clearer repository, architecture, evidence, and product semantic model while preserving the existing agent/deterministic boundary.