# Semantic Architecture Foundation — Milestone Handoff

**Date:** 2026-09-10  
**Branch:** `docs/semantic-architecture-foundation`  
**Milestone status:** Documentation foundation complete; executable semantic promotion intentionally deferred

## What this milestone establishes

This milestone creates the first coherent **Sensemaking Semantic Architecture** for reasoning about repositories.

The repository now has a canonical distinction between:

```text
Semantic Model
  = what entities/relations mean

Reasoning Model
  = how observations become evidence, claims, uncertainty, responsibility, and decisions

Execution Integration
  = how existing probes, Skills, artifacts, validators, Campaigns, and handoffs participate
```

It also establishes three formalization levels:

```text
Level 1 — Vocabulary
Level 2 — Ontology
Level 3 — Executable semantic contract
```

No Level-1/2 concept may be treated as Level-3 authority merely because it is documented.

## Delivered artifacts

- `README.md` — semantic-architecture index and formalization model.
- `constitution.md` — 20 guardrails protecting evidence, authority, provenance, and anti-overformalization boundaries.
- `problem-statement.md` — root problem and success criteria.
- `competency-questions.md` — 78 questions that bound ontology scope.
- `concept-inventory.md` — reconciliation with existing Campaign, Skill, artifact, validator, and PM concepts.
- `ontology.md` — six-layer ontology covering Intent, Repository/Software System, Evidence, Knowledge/Epistemics, Engineering Work, and Product.
- `product-change-taxonomy.md` — multi-axis taxonomy for change type, value mechanism, target, and relationship to existing value.
- `relations-and-epistemics.md` — relation dictionary, epistemic statuses, temporal rules, contradiction model, absence claims, and invalid inference catalog.
- `reasoning-model.md` — evidence-governed reasoning lifecycle from target binding to durable transition/handoff.
- `execution-integration.md` — adoption boundaries for probes, Skills, artifacts, validators, Campaigns, capability registry, domains, and harnesses.
- `reference-scenarios.md` — 12 semantic evaluation scenarios.
- `implementation-plan.md` — phases and promotion gates from shared vocabulary through possible future executable contracts.

## Important terminology decision

The repository should use the umbrella term:

> **Sensemaking Semantic Architecture**

with these major parts:

```text
Semantic Model
Reasoning Model
Execution Integration Architecture
```

Within the semantic model, use bounded ontologies/taxonomies rather than one undifferentiated ontology.

The term `capability` is now explicitly disambiguated conceptually:

```text
SoftwareCapability
  = behavior/ability of the target software

ProductCapability
  = user-facing ability/value provided by a product

SensemakingCapability
  = Skill/tool/environment ability to perform a responsibility
```

Existing executable Campaign `Capability` remains unchanged; the qualified semantic names are documentation-level disambiguation until future evidence warrants runtime changes.

## Product-change taxonomy disposition

The previously discussed taxonomy belongs in the semantic architecture as a **bounded Product ontology subdomain**.

It is not the foundation for repository structure or architecture reasoning.

Canonical axes are:

```text
Structural type
  net-new capability / extension / enhancement / integration /
  enabler / quality improvement / UX improvement / automation /
  scale capability / simplification

Value mechanism
  add / deepen / broaden / connect / simplify / harden /
  accelerate / scale / enable / differentiate

Target of change
  workflow / product capability / feature / software capability /
  quality / platform / ecosystem / developer or operational workflow

Relationship to existing value
  independent / complementary / multiplicative / foundational / defensive
```

These are descriptive, not prioritization or implementation authority.

## Core semantic invariants

The new documents preserve and extend existing repository invariants:

```text
observation != interpretation
evidence != truth
support != proof
validator PASS != semantic truth
repository changed != repair succeeded
directory != Component by default
import != architecture violation
passing test != complete behavior proof
capability exists != capability should run
capability available != action authorized
document says X != X is current
no search result != absence unless completeness is established
ontology term documented != runtime-enforced concept
```

## What was intentionally NOT implemented

This milestone does not add:

- Campaign schema fields;
- a universal ontology YAML/JSON schema;
- a repository knowledge graph;
- automatic component detection;
- automatic uncertainty ranking;
- automatic responsibility/capability routing;
- a Repository Semantic Map artifact contract;
- new deterministic semantic validators;
- a graph database;
- domain-pack runtime infrastructure.

Those are not omissions. They are gated future hypotheses.

## Next empirical milestone

The next warranted step is **Phase 9 — Skill semantic-alignment pilots**.

Recommended order:

1. `repo-sensemaker` — currentness, evidence, claim, contradiction, and uncertainty semantics.
2. `architectural-review` — Component/Boundary/Contract/Dependency semantics.
3. `repair-verifier` or `output-reconciler` — Change/Outcome/Validation/Repair/Supersession semantics.

Each pilot should record:

```text
competency questions exercised
ambiguous terms found
before/after vocabulary
unsupported inference jumps prevented
new concepts requested
ontology concepts unused
overhead introduced
```

Only after at least two contrasting pilots show stable repeated structure should common artifact fields or executable semantic contracts be proposed.

## Parallel program continuity

This semantic-architecture initiative does not invalidate the existing PM repository-expansion program or empirical qualification debt.

PM waves may continue under their existing maturity policy. Engineering and PM native-harness qualification remain separate empirical gates.

The semantic architecture should be adopted opportunistically in future Skill changes rather than forcing a mass rewrite of all Skills.

## Definition of success for the next session

A future session should not ask "how do we implement every ontology concept?"

It should ask:

> Which ambiguity in a real Skill episode materially harms repository reasoning, and what is the smallest semantic formalization that removes it while preserving evidence and authority boundaries?

That is the intended continuation path.