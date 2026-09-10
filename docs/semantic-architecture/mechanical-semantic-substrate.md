# Mechanical Semantic Substrate

**Status:** Executable bounded v0  
**Purpose:** Provide mechanically decidable repository observations and reusable provenance without converting structural facts into semantic judgments

## Boundary

The substrate may answer questions such as:

```text
Which regular files were enumerated in the declared scope?
Which Python import statements are syntactically present?
Which supported manifests declare dependencies?
Where does exact UTF-8 literal text occur within a declared scope?
Which supplied observations share one target identity?
Is a cross-Skill provenance chain structurally intact?
```

It may not answer:

```text
Is this dependency architecturally wrong?
Is a module unused at runtime?
Which uncertainty matters most?
Which Skill should run next?
Did a repair semantically succeed?
Is a claim true?
```

Therefore:

```text
mechanical observation != semantic interpretation
complete declared scope != complete repository/world knowledge
semantic map relation != architecture judgment
valid semantic state chain != warranted conclusion
```

## Executable package

The shipped package is `sensemaking_skills.semantic_architecture`.

### Core representations

`SemanticObservation` records:

- stable observation ID;
- observation kind;
- subject / predicate / object;
- evidence references;
- source/mechanical method;
- declared scope;
- completeness classification;
- currentness classification;
- exact target reference;
- optional mechanical metadata.

`SemanticProbeResult` groups observations under one probe, target, scope, and completeness statement. `semantic_truth_established` is permanently false in the v0 contract.

### Current probes

#### File containment

`sensemaking-skills semantic probe --kind file-containment`

Enumerates regular non-symlink files outside known generated/vendor roots and records each file's immediate directory relation.

It establishes filesystem containment only. A directory is not automatically an architectural `Component`, `Layer`, bounded context, owner, or product capability.

#### Python imports

`sensemaking-skills semantic probe --kind python-imports`

Parses Python source with `ast` and records syntactically present imports. If any inspected Python source cannot be parsed, probe completeness becomes `partial` and diagnostics preserve the failure.

An import establishes import syntax in the inspected bytes. It does not by itself establish runtime execution, coupling severity, a forbidden boundary, or an architectural defect.

#### Manifest dependencies

`sensemaking-skills semantic probe --kind manifest-dependencies`

Current v0 parsers cover:

- `pyproject.toml` project and optional dependencies;
- `package.json` dependency/dev/peer/optional dependency sections;
- `requirements.txt` non-comment direct entries.

The probe reports declared dependency text. It does not establish that the dependency is installed, loaded, used, vulnerable, unnecessary, or correctly versioned.

#### Exact search

`sensemaking-skills semantic probe --kind exact-search --pattern ...`

Searches literal text in UTF-8-decodable regular files selected by the declared glob and outside generated/vendor roots. The summary records inspected UTF-8 files and skipped unreadable/non-UTF-8 files.

A zero match count means zero literal matches in the declared searched scope. It does **not** establish absence from binary files, generated outputs, runtime state, external systems, ignored/vendor roots, semantically equivalent spellings, or other search methods.

## Repository Semantic Map v0

`RepositorySemanticMap` is a bounded representation built from supplied `SemanticObservation` values.

```text
observations
    -> repository locators
    -> mechanical relations
    -> evidence refs
    + external claim refs
    + external uncertainty refs
    + explicit limits
```

The builder:

- rejects observations bound to a different target reference;
- marks generated relations `DERIVED`;
- keeps source observation IDs and evidence refs;
- does not infer domain-level entity kinds from directory/file names;
- adds an explicit non-completeness limit.

The v0 map deliberately uses `repository_locator` entities rather than pretending that files/directories are canonical software Components.

A map may reference agent-authored claims and uncertainties, but it does not create their semantic content.

CLI:

```text
sensemaking-skills semantic map-build \
  --map-id MAP-1 \
  --target-ref <snapshot-ref> \
  --observations probe.json \
  --output map.json
```

## Cross-Skill Semantic State

`SemanticStateStore` provides an optional append-only companion JSONL chain for carrying references between Skills without modifying Campaign schema v2.

Each entry records only explicit durable references such as:

```text
entry ID
source Skill
artifact ref
target ref
evidence refs
claim refs
uncertainty refs
parent semantic entries
optional semantic profile ref
notes
timestamp
```

Every entry is SHA-256 bound to the previous entry. Reconstruction detects:

- digest tamper;
- broken previous-digest chain;
- duplicate entry IDs;
- missing, future, or self-parent references;
- malformed records.

The log preserves **provenance between bounded reasoning episodes**. It is not hidden chain-of-thought storage and does not contain an automatic next-action recommendation.

CLI:

```text
sensemaking-skills semantic state-append ...
sensemaking-skills semantic state-show ...
```

## Conformance

The same package provides mechanical validation for Skill Contract Manifests and Domain Pack manifests. Conformance is documented separately in `skill-contract-manifests-and-domain-packs.md`.

## Packaging

The Python substrate and its CLI ship in the core wheel. Repository-owned Skill/Domain manifest YAML files remain checkout-level conformance inputs in v0 and are passed explicitly to the conformance command. This avoids duplicating the same manifest tree inside the Python package before a packaging use case warrants that extra authority surface.

## Next extension rule

Add a new probe only when:

1. the exact mechanical relation can be stated without semantic judgment;
2. scope and completeness can be declared;
3. currentness can be bound;
4. false-positive/false-negative boundaries are documented;
5. rejection behavior is testable;
6. at least one real product/Skill capability can consume the result.

Do not add a probe merely to make ontology coverage look more complete.
