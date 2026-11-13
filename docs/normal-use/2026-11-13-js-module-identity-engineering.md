# JS module-specifier identity — source-grounded engineering episode (2026-11-13)

**Original decision context, recorded before implementation.**
**Sensemaking baseline:** `main@afc55f4f4f6ffe32c1f8de6ab2f49e941e7379af` (PR #853 merged, final-head hosted checks passed).
**Execution scope:** authorized Sensemaking repository construction only; the separate Auteur source below was inspected read-only.
**Independence:** this is a continuation in the existing ChatGPT conversation, not a fresh-context coding agent or independent reviewer.

## Original engineering problem and beneficiary

The opt-in JS/TS semantic index introduced in PR #852 and exposed through zero-setup `workspace-query` in PR #853 records module-specifier *syntax* in a typed source-linked graph. In `src/sensemaking_skills/semantic_architecture/knowledge_sources.py`, `_js_module_import_syntax` currently constructs a target claim with `stable_id("js-module-specifier", item.object)`. Its identity ignores the importing `item.subject`.

A source-grounded agent inspecting a relative import may therefore see one graph concept for references that occur in different directories and point to different local files. The claim's `source_ref` / source hash comes from the first such importer encountered, while other import edges converge on that node. The original source and relation remain readable, but the target's identity and provenance are misleading.

**Non-synthetic evidence of the semantic distinction:** read-only Auteur `main@14c290ea1eee2181342eaaa6a989ec4d7c7a960c` contains three distinct importers using the same literal `./model.mjs` but each has its own directory-local source file:
- `docs/prototypes/focused-unfolding/app.mjs` -> `docs/prototypes/focused-unfolding/model.mjs`
- `docs/prototypes/agent-interactive-graph/app.mjs` -> `docs/prototypes/agent-interactive-graph/model.mjs`
- `docs/prototypes/studio-explanations/app.mjs` -> `docs/prototypes/studio-explanations/model.mjs`

These are *source-local specifiers*, not evidence that Sensemaking successfully resolved their imports. The source comparison establishes the identity distinction independently of a semantic index.

## Source-only initial understanding before semantic observation use

- A source-level static import points to a **literal string used in one importer**, not a global module.
- The tracked Sensemaking JS fixtures currently used by hosted CI each provide distinct import strings; they do not prove that target claim identity is correct in all source layouts.
- The substantive uncertainty was whether the existing claim is meant as a generic literal label or a source-specific reference. Because it has a single `source_ref` and source fingerprint and is linked as a source observation, source-specific identity better respects its existing evidence contract.
- The initial engineering approach is to scope a JS/TS module-specifier claim ID to `(importing source path, literal specifier)`, preserving the text and original relation IDs, with no module resolution or new schema.
- Alternative: keep global literal identities and rely on per-edge provenance; rejected because the single claim then misrepresents the source for other importers.
- Alternative: resolve relative specifiers into paths; rejected because language-specific resolution (aliases, extensions, packages and build systems) exceeds the observer's declared syntax-only boundary.

## Semantic-observation and decision-influence ceiling

The current execution environment has GitHub source and PR access but **no local Sensemaking checkout or installed CLI**; the Git remote cannot be cloned because name resolution is unavailable. No predecision `semantic workspace-query` result was obtained. The source inspection above **already establishes the repair warrant**, so the index cannot be credited with discovering or causing the choice.

A genuine user/use benefit, independent reader interpretation, faster navigation relative to direct source inspection, and causal AMS/SCL effects remain **NOT ASSESSED**. Revision-specific hosted consumers may qualify mechanical behavior after implementation but do not substitute for a fresh coding-agent session.

## Target and stop boundary

Keep the existing graph kinds, CLI flags, source citations, snapshot cache separation and default query behavior unchanged. Add a real committed-source consumer assertion that the observed `references` edge points at a claim identified by **both** its importer and literal, then report hosted full-suite and source-consumer results separately. Do not edit Auteur, introduce new inference or create a new ontology/learning-method claim solely for this repair.
