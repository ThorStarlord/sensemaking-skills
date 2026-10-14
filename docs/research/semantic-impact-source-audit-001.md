# Semantic impact preview - source audit 001

**Evidence:** bounded read-only GitHub source inspection, 2026-10-14. **Not** an independent agent comparison, a full target-repository CLI execution, or evidence of causal product improvement.

- **Sensemaking construction base:** 758bd85a4b8d36e98ddd395f4d0e3739b7cd71ef
- **Target source:** ThorStarlord/React_incremental_game_prototype@e4842e2bf0709c8ff41a20702580132d2375b309
- **Question:** Before modifying Relationship Experience / Connection progression, which design constraints, implementation areas, and verification claims could matter?
- **Chosen literal query:** Relationship Experience; Memory; Connection XP; Essence; Affinity.
- **Sources inspected:** Grounding Pack, Relationship Experience, Memory, Essence/Resonance, Trait specifications, Post-M14 reconciliation, Relationship Slice/Selectors/Thunks.

## Relevant source-backed observations

| Source at pinned target SHA | Why a coding agent should inspect it |
| --- | --- |
| .sensemaking/context.md lines 4-5 | Explicitly distinguishes Affinity from Connection XP, and Relationship Experience from landmark Memory. Tagged references point to controlling specifications. |
| specification/Features/RelationshipExperienceSystem.md lines 9-26 | Describes Experience as event/history and names Memory, Connection, Essence, Traits and story availability as downstream concepts. Policy/contract evidence, not automatically a verified runtime dependency. |
| specification/Features/MemorySystem.md lines 8-18 | A Memory references an originating Experience; not every Experience is a Memory. |
| specification/Features/TraitSystem.md line 87 | Forbids substituting a strong Relationship, Memory, Affinity or Connection level for actual permanent Trait ownership. |
| src/features/Relationships/state/RelationshipThunks.ts lines 94-99 | Has a passive Essence rate refresh path tied to Relationship state. Source-level implementation evidence, not evidence that all downstream effects are covered. |
| src/features/Relationships/state/RelationshipSelectors.ts lines 314-328 | Contains Relationship Essence contribution selectors, warranting direct follow-up inspection. |

A bounded source search locates relevant files; the Grounding Pack contributes product-language distinctions and cites authority. The preview joins **declared references** and **lexical observations** into source-bound candidate links. It never concludes that co-mentioned concepts are architectural dependencies or that a test mentioned by name verifies a given property.

## Honest usefulness assessment

- **Mechanically constructed:** optional read-only semantic impact-preview over existing semantic probes and Grounding Pack tags, requiring exact clean Git HEAD and explicitly non-authoritative output.
- **Local qualification:** 20 focused cases passed in an isolated package-compatible harness; full repository validation and hosted GitHub checks are not established by this note.
- **Pilot limitation:** React source was inspected through the connected GitHub API. This session could not clone the full React repository into its local runtime, so the **new Python CLI was not executed on the exact React target checkout**. This note records source inspection and expected query relevance, not end-to-end target qualification.
- **Comparative value:** **NOT ESTABLISHED**. Direct search also found consequential sources; no independent observation yet shows that the projection saves time, catches a missed consequence, reduces owner questions, or improves code quality.
- **Risk:** Literal matching is case-sensitive in repository content, relations are deliberately shallow, and no result is proof of absence. Caller must select related terms and inspect candidate sources.

**Decision:** Keep this as a small, optional read-only candidate in a reviewable PR. Do not yet add a SQLite store, permanent ontology, mandatory preflight, new Skill, or automatic Change Impact integration. Those remain conditional on useful real engineering consultations. Grounding Pack Phase 3, Semantic Control Map trial, and Trial 002/002R retain their separate claim ceilings.
