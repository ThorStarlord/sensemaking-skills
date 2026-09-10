# Semantic Architecture Constitution

**Status:** Canonical guardrails for semantic-model evolution  
**Applies to:** ontology, taxonomies, reasoning models, semantic artifacts, validators, probes, and Campaign integrations

## Constitution

1. **Evidence is not truth.** Evidence can support, contradict, weaken, or leave a claim unresolved. Mechanical validity never upgrades evidence into semantic truth.

2. **Observation is not interpretation.** A mechanically observed import, test result, file path, Git state, or schema field is distinct from the semantic meaning an agent assigns to it.

3. **Deterministic machinery may establish mechanical structure, not semantic warrant.** It may establish that a file imports another file, an artifact satisfies a schema, an evidence reference exists, or a target digest changed. It must not silently decide that an architecture is good, a responsibility is warranted, or a repair succeeded.

4. **Semantic inference must preserve evidence lineage.** Material claims should be traceable to the observations, sources, artifacts, or prior claims that informed them. Unsupported prose is not promoted merely because it appears in a canonical artifact.

5. **Human-ratified intent outranks inferred intent.** Explicit owner/user requirements, constraints, and ratified architectural intent take precedence over agent inference when they conflict, subject to safety and external authority boundaries.

6. **Absence of evidence is not evidence of absence unless completeness is established.** A probe may support an absence claim only when its contract establishes that the searched scope is complete enough for that conclusion.

7. **Repository claims are temporally bound.** Material claims about repository state should identify or inherit the target snapshot, commit, worktree digest, or other currentness boundary to which they apply.

8. **Ontology concepts must answer demonstrated competency questions.** Concepts are not added because they are academically elegant. They are added because recurring Sensemaking work needs the distinction.

9. **Taxonomy must not become executable policy accidentally.** Descriptive categories such as enhancement, extension, enabler, or value mechanism do not authorize routing, prioritization, or implementation.

10. **New formal concepts require demonstrated reasoning value.** Prefer observation and repeated use before schema expansion. One-off vocabulary belongs in prose until evidence shows stable cross-Skill value.

11. **Canonical concepts have one meaning across Skills.** Skills may specialize a concept but must not redefine canonical terms locally without an explicit namespace or reconciliation decision.

12. **Semantic status and authority status are separate.** A claim may be plausible but unauthorized to act upon; an action may be authorized while the underlying claim remains uncertain.

13. **Capability availability is not capability selection.** Registries may expose declared compatibility and availability, but semantic selection remains an agent decision unless a separately authorized deterministic rule is both narrow and mechanically justified.

14. **Validation scope must be explicit.** Every validator or receipt should state what it proves and what it does not prove. Structural validation must not be presented as semantic verification.

15. **Historical reasoning is append-preserving.** Later conclusions may supersede earlier conclusions, but historical evidence and prior decisions should not be rewritten to make the later state appear inevitable.

16. **Contradiction is preserved, not normalized away.** When two credible sources disagree, the system should represent the contradiction and its provenance rather than silently choose whichever source is convenient.

17. **The semantic map is derived context, not repository authority.** Source code, repository state, explicit external records, and ratified intent remain primary evidence sources. Generated semantic representations must be rebuildable or challengeable from those sources.

18. **Formalization must remain agent-agnostic.** Canonical semantics may not depend on Claude-, Codex-, OpenCode-, or other harness-specific representations. Harness adapters translate; they do not redefine meaning.

19. **Domain-specific concepts extend rather than pollute the foundation.** Product Management, security, design, research, or other domains may add bounded sub-ontologies. They should reuse foundation concepts where meanings genuinely match and namespace concepts where they do not.

20. **The smallest sufficient formalization wins.** If vocabulary solves the reasoning problem, do not add ontology relations. If ontology solves it, do not add runtime fields. If runtime support is needed, encode only the mechanically necessary subset.

## Decision rule for conflicts

When a proposed convenience conflicts with these rules, preserve the epistemic and authority boundary first. Ergonomics may simplify representation and workflow, but must not collapse distinctions such as:

```text
observed != inferred
supported != proven
available != warranted
warranted != authorized
validated != true
changed != succeeded
```

## Change policy

Changing this constitution requires an explicit architectural decision because these rules protect the product's semantic-control boundary. Ordinary additions to the ontology, taxonomy, or competency-question inventory do not require changing the constitution.