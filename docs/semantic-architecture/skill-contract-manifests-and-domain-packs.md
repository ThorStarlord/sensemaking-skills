# Skill Contract Manifests and Domain Packs

**Status:** Executable repository-level v1 conformance  
**Purpose:** Make deterministic Skill/domain interfaces machine-readable without turning metadata into semantic routing authority

## Skill Contract Manifest v1

A Skill Contract Manifest describes the deterministic shell around a Skill:

```yaml
schema_version: 1
skill_id: repo-sensemaker
domain: engineering
responsibilities: [repository_sensemaking]
consumes: [user_intent, repository_state, prior_evidence]
produces: [repository_sensemaking_brief]
semantic_concepts: [Intent, TargetSnapshot, Observation, Evidence, Claim, Uncertainty]
repository_mutation: false
```

The manifest does **not** contain methodology, prompt instructions, confidence scores, automatic routing rules, or recommendations.

Its fields mean:

- `skill_id` — canonical Skill identity for the manifest;
- `domain` — owning domain vocabulary;
- `responsibilities` — responsibility types the Skill declares it can serve;
- `consumes` — canonical input artifact/state identities explicitly modeled by manifest v1;
- `produces` — canonical output artifact identities;
- `semantic_concepts` — shared Semantic Architecture concepts the Skill contract explicitly uses;
- `repository_mutation` — whether the Skill's declared contract itself includes repository mutation.

An empty `consumes` list does **not** mean the Skill requires no information. It means manifest v1 does not declare a canonical machine-level input artifact for that capability. Human/user prompt context and Skill-local inputs remain governed by the Skill methodology.

## Conformance boundary

`sensemaking-skills semantic conformance` can mechanically check:

- required fields and schema version;
- basic field shape;
- duplicate manifest IDs;
- membership in the canonical manifest-level semantic vocabulary;
- declared repository mutation as a boolean;
- referenced Domain Pack files when a repository root is supplied;
- prohibited fields that would imply deterministic semantic authority.

The conformance validator explicitly rejects fields such as:

```text
semantic_truth
auto_route
automatic_skill_selection
automatic_uncertainty_ranking
```

because these are outside the contract's authority.

Therefore:

```text
manifest valid != Skill is semantically good
manifest responsibility declared != responsibility warranted now
Skill exists != Skill should be selected
semantic concept declared != conclusion using it is true
```

## Domain Pack v1

A Domain Pack is a **reference manifest**, not a plugin runtime or central router.

It groups already-existing domain contracts:

```text
domain identity
+ capability ledger
+ Skill manifests
+ responsibility vocabulary
+ artifact identities
+ qualification policy
```

Current repository references:

- `domain-packs/engineering.yaml`
- `domain-packs/product-management.yaml`

### Engineering reference pack

The first engineering pack binds the four Phase 9 semantic-alignment Skills:

```text
repo-sensemaker
architectural-review
repair-verifier
output-reconciler
```

It does not claim these are every engineering capability in the repository. It is the first bounded reference pack for the Semantic Architecture interface.

### Product Management reference pack

The PM pack references the complete repository-qualified upstream methodology migration ledger and all 27 canonical PM Skill manifests. The existing Product Management qualification policy remains authoritative for maturity/support claims.

The pack does not alter maturity. In particular:

```text
Domain Pack membership != native-harness qualified
Domain Pack membership != portability qualified
Domain Pack membership != promoted
```

## Why extract Domain Packs now?

The repository now has two materially different implemented domains with stable responsibility/capability/artifact boundaries: engineering repository reasoning and Product Management. That is enough to extract a minimal **reference shape** without yet building a generic runtime plugin platform.

What has repeated is the structural shell:

```text
responsibility vocabulary
-> capabilities / Skills
-> artifact contracts
-> validators / qualification
```

What has **not** repeated enough to formalize generically includes domain methodology, semantic ranking, workflow selection, or universal domain routing.

## Repository vs wheel authority

`skill-manifests/` and `domain-packs/` are currently repository-owned source contracts. The installed semantic conformance implementation ships in the core wheel, but operators pass manifest directories explicitly.

This prevents two independently authoritative copies of every manifest from being shipped before a concrete installed-manifest discovery use case warrants that packaging decision.

## Extension rule

A new Domain Pack should be added only when:

1. a real domain has multiple implemented capabilities;
2. its responsibility vocabulary is explicit;
3. canonical artifacts/validators or equivalent contracts exist;
4. a qualification policy exists;
5. the pack can be purely descriptive of those existing contracts;
6. adding the pack does not create a new semantic router.

The Domain Pack architecture is intentionally weaker than a plugin framework. Future packaging/discovery can be added if repeated use demonstrates the need.
