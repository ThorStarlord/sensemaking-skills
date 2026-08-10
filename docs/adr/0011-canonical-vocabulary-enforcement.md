# ADR 0011: Canonical Vocabulary Enforcement

**Status**: Accepted

**Context**: Enum-typed fields (fog types, routing fields, gates, execution
modes, workflow IDs, artifact IDs) are shared across producers
(`repo-sensemaker`, `workflow-planner`), validators, and the workflow runtime.
The PR #14 regression ("contract mismatch") showed that documentation-only
conventions drift: producers emitted alias or stale values (e.g. `product`
instead of `product_fog`), validators disagreed on which values were legal, and
downstream auto-invocation could not trust `recommended_workflow_id`. The
hardening work is tracked in [docs/HARDENING_STATUS.md](../HARDENING_STATUS.md)
and summarized as decision item 10 in [CONTEXT.md](../../CONTEXT.md).

**Decision**: `docs/canonical-vocabulary.yaml` is the **single source of truth**
for every enumerated value. Enforcement is three-layered:

1. **Compile-time path drift tests** (`tests/test_path_drift.py`) fail on stale
   skill/validator paths and on enum values that appear in registries or docs
   without a vocabulary entry (e.g. `test_vocabulary_covers_all_workflows`,
   `test_vocabulary_covers_all_artifacts`, `test_gate_names_are_canonical`).
2. **Runtime enum validation** (`scripts/validate-artifact.py`,
   `_validate_enum_fields()`) validates routing fields against the vocabulary
   at artifact-creation time and emits `INVALID_ENUM_VALUE` for unknowns.
3. **Alias normalization** in validators (`validate-fog-type-normalization.py`,
   `build_fog_type_normalizer()`): producers may input aliases (`ui`,
   `product`, ...), validators normalize them to canonical forms
   (`ui_fog`, `product_fog`, ...) before the artifact is stored. Downstream
   consumers (including `workflow-planner`) receive and must emit canonical
   values only — no aliasing, no unknowns.

**Rationale**: Enforcement moves the vocabulary from documentation into the
execution path, which makes auto-invocation safe: by the time
`workflow-planner` reads an artifact, `recommended_workflow_id` and every other
enum field is guaranteed valid and canonical, so the runtime can route without
defensive alias handling. This is the same "artifacts are the API" discipline
that ADR 0010 applies to artifact *paths*, applied here to machine *field
values*.

**Alternatives considered**:
1. Vocabulary as documentation only (pre-hardening state) — rejected; PR #14
   proved conventions drift without executable checks.
2. Strict rejection of all alias forms — rejected; producers naturally emit
   short forms, so aliases are accepted at the boundary and normalized once.
3. Per-validator copies of enum tables — rejected; duplicated tables drift
   from each other and from the registry.

**Consequences**: Positive: enum fields are canonical downstream by
construction; path-drift and enum-consistency tests run on every commit; the
vocabulary covers 100% of live registries (19 workflows, 33 artifacts, 35+
gates). Negative: new enum values require coordinated updates to the
vocabulary, the registries, and the drift tests; producers must emit canonical
forms; normalization lives in validators only — the runtime never re-normalizes
or guesses. Pending work (see HARDENING_STATUS.md): producer-side normalization
in `repo-sensemaker` output, and a tier-1/tier-2 validation split.
