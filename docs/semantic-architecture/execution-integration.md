# Execution Integration Architecture

**Status:** Canonical integration design, v0  
**Purpose:** Define how the semantic model should influence existing Sensemaking surfaces without prematurely requiring a new runtime graph or schema.

## Architectural principle

The semantic architecture should improve consistency **through existing product boundaries first**.

Preferred direction:

```text
shared semantic vocabulary
        |
        +-> Skills use common terms
        +-> artifacts state claim/evidence status more consistently
        +-> validators enforce only mechanical subsets
        +-> Campaigns persist existing control-plane semantics
        +-> handoffs preserve current semantic conclusions and uncertainty
```

Avoid:

```text
ontology document
        -> immediately create universal graph database
        -> force every Skill to emit hundreds of typed nodes
        -> central router reasons over graph
```

## 1. Probes

### Role

Probes provide mechanically bounded observations.

They may establish facts such as:

- target identity and Git state;
- file/path existence;
- parseable import/export relations;
- declared package dependencies;
- test command outcomes;
- exact text/field presence;
- artifact digests;
- complete-scope search results when the probe contract guarantees scope.

### Required semantic metadata for future probes

A probe SHOULD eventually declare:

```text
observation_type
scope
completeness_guarantee
currentness boundary
source identity
mechanical derivation method
known blind spots
```

This metadata is a design target, not a current schema mandate.

### Prohibition

A probe must not silently emit semantic judgments such as:

```text
"bad architecture"
"wrong component"
"unnecessary dependency"
```

unless those are explicitly defined narrow mechanical predicates, which should normally use more precise names.

## 2. Skills

### Role

Skills remain bounded semantic capabilities used by the active agent.

Skills should progressively align on shared concepts such as:

```text
Claim
Evidence
Uncertainty
Responsibility
Component
Boundary
Contract
DependencyRelation
Change
Validation
ProductCapability
```

### Near-term integration rule

Do not rewrite every Skill immediately.

Instead, when a Skill is already being modified for another justified reason:

1. reconcile its terminology against the semantic architecture;
2. remove local redefinitions of canonical terms;
3. explicitly label observed vs inferred conclusions where material;
4. make evidence lineage clearer;
5. add ontology concepts only if competency questions demonstrate the need.

### Candidate first adopters

The best Skills for semantic-alignment experiments are:

```text
repo-sensemaker
architectural-review
problem-framer
unknowns-mapper
output-reconciler
repair-verifier
docs-aligner
sensemaking-docs-reconciler
```

These already exercise the cross-cutting repository/evidence vocabulary.

## 3. Artifacts

### Role

Artifacts remain durable products of Skills/work.

The semantic architecture suggests a future common envelope for high-value analytical artifacts:

```text
subject / target scope
currentness boundary
material claims
claim epistemic status
supporting evidence refs
counter-evidence / contradictions
active uncertainties
semantic conclusions
explicit non-claims / limits
```

### Important

This is **not yet a universal artifact schema**. Different artifacts have different purposes and should not be flattened into one generic format.

A common semantic envelope should be extracted only after repeated artifact families demonstrate the same fields are useful.

## 4. Validators

### Role

Validators own mechanical contract verification.

The semantic architecture gives validators a clearer discipline:

```text
validator may check:
- required fields
- identifier integrity
- exact evidence references
- allowed enum values
- source/currentness metadata
- deterministic relation shape
- completeness declarations where mechanically provable

validator may not check by default:
- architectural quality
- truth of semantic claims
- whether selected uncertainty is the best one
- whether a capability should have been selected
- whether product priority is correct
```

### Validation messages

Where practical, validators should state the scope of the PASS:

```text
PASS: artifact satisfies repository_sensemaking_brief structural contract
NOT ESTABLISHED: semantic conclusions are true
```

## 5. Campaign semantic model

### Existing alignment

Current executable Campaign concepts already map strongly to the new semantic model:

```text
CampaignState       -> work/decision aggregate
Responsibility      -> Work.Responsibility
Uncertainty         -> Knowledge.Uncertainty
Authority           -> Work.Authority
Capability          -> Work.SensemakingCapability
ClaimEvidence       -> Claim <-> Evidence bridge
TargetSnapshot      -> Repository.TargetSnapshot
TransitionRecord    -> Decision transition
CampaignHandoff     -> Handoff
```

### Near-term rule

Do **not** change Campaign schema merely to mirror the ontology.

Campaign schema changes require independent evidence that a semantic concept must be durable at the Campaign control-plane level.

Example:

`Component` may be valuable in architecture artifacts without belonging directly in `CampaignState`.

## 6. Capability registry

The capability registry should continue to represent declared interfaces, not semantic routing policy.

A future capability contract may use shared semantic vocabulary for:

```text
accepted responsibility types
produced artifact kind
mutation behavior
authority requirements
mechanically required inputs
```

It should not encode generic rules like:

```text
if architecture confidence > 0.7 choose architectural-review
```

## 7. Handoff

Handoff is a high-value integration point because semantic inconsistency becomes expensive across fresh contexts.

A future handoff projection should be able to preserve:

```text
current mission / explicit intent
current target snapshot
active responsibility
consequential uncertainty
material established/inferred claims
epistemic status
contradictions
relevant evidence refs
authority
recent decisions
superseded/deferred conclusions
```

The handoff should not invent new semantic conclusions during summarization.

## 8. Documentation

Canonical terminology should progressively converge on this semantic architecture.

Documentation roles remain distinct:

```text
Semantic architecture docs -> meaning of concepts
Campaign docs -> product control model
ADR -> ratified architectural decision
STATUS -> current repository frontier
Skill docs -> bounded methodology
Artifact contracts -> output structure
Validator code -> executable mechanical authority
```

When executable behavior and prose disagree, executable behavior remains authority for what the software currently enforces; the semantic docs remain authority for intended concept meaning unless superseded by a later ADR/owner decision.

## 9. Product Management and other domains

Domain vocabularies should extend the foundation through bounded sub-ontologies.

Example:

```text
Foundation:
  Claim
  Evidence
  Responsibility
  ProductCapability
  ProductChange

PM domain:
  Persona
  Opportunity
  ProductHypothesis
  ProductSpecification
```

A PM concept should not be promoted into the foundation merely because PM Skills use it.

Likewise, future security/design/research domains should reuse foundation semantics but remain separately extensible.

## 10. Harness adapters

Harness adapters may translate semantic artifacts and Skill discovery into Claude/Codex/OpenCode-specific representations.

They MUST NOT redefine canonical meaning.

```text
canonical Skill semantics
        |
        +-> Claude representation
        +-> Codex representation
        +-> OpenCode representation
```

Agent/harness portability should therefore be tested at the semantic-output boundary, not merely by byte-identical installation.

## 11. Candidate semantic-map artifact

A future experiment may introduce a **Repository Semantic Map** artifact, but only after reference scenarios prove that Skills benefit from sharing a durable map.

If introduced, it should be bounded and reconstructible rather than exhaustive.

Potential conceptual shape:

```text
RepositorySemanticMap
- target_snapshot
- scope
- entities[]
- relations[]
- claims[]
- contradictions[]
- unresolved_uncertainties[]
- evidence_refs[]
```

This is explicitly **deferred** in v0. It must not be treated as a currently supported artifact contract.

## 12. Integration sequence

Recommended order:

```text
1. documentation vocabulary
2. Skill terminology alignment experiments
3. artifact-level semantic fields where repeated
4. validator support for mechanical subsets
5. cross-Skill semantic-map experiment
6. Campaign schema changes only if control-plane durability requires them
```

This sequence keeps ontology useful without turning conceptual design into infrastructure debt.

## 13. Architecture invariant

The semantic architecture integrates **through** the Campaign control boundary; it does not replace it.

```text
semantic model improves what the agent can say consistently
Campaign improves how those decisions are preserved
validators improve what can be mechanically trusted
none of them silently becomes the agent
```