# Comparative prospective construction — definition-level patch rehearsal

Baseline and framework: `c1f95ed50a0791a57faa4e96bba2e6415df446e8`. ADR 0038 and the existing Level-3 integrated-development direction remain governing. Canonical #1010 Product Validation 46093122258 and Distribution 46093122220 passed. This is ordinary same-agent beneficiary use of the prior [prospective intervention rehearsal](2026-11-27-generative-strategic-intelligence.md), not a new comparative execution subsystem or independent cognitive qualification.

## Decision context

The existing patch rehearsal verifies a concrete intervention's file paths, before/after digests, applicability and Python syntax, but stops at file granularity. Existing committed-source symbol review pairs exact committed sources and selected symbols; it cannot compare a hypothetical applied overlay as committed evidence. The intended new experience is for a reviewer to identify the changed definitions and distinguish structural changes from text-only changes without committing the hypothetical tree or treating the AST as a semantic behavior model. Retain the original prior value frame: actual concrete intervention and BASE evidence with no active-checkout change, not more metadata alone. The choice is between using manual diff inspection/existing committed symbol review, a source-span comparison, and a dual source/AST comparison. The first remains a valid fallback, especially for unsupported source. No automatic alternative selection, test execution, or new comparison engine.

## Constructed alternatives, common exact baseline

- A ([5b610b35](https://github.com/ThorStarlord/sensemaking-skills/commit/5b610b350edce8497a39d44cd6d9adcd6a9a02b1)): exact source-span comparison of unique top-level definitions, including decorator lines, and residual module source. Simpler and sensitive to text changes but no distinction between AST changes and textual-only changes.
- B ([d03f3ee8](https://github.com/ThorStarlord/sensemaking-skills/commit/d03f3ee8810fc254405db94f57ba1249f6ebd167)): the same source-span evidence plus attribute-free AST fingerprints, separately classifying AST_CHANGED and SOURCE_ONLY_CHANGED; module-level AST includes non-definition statements and the order of definition-name markers. More code/processing but no loss of exact-source evidence.

Both are genuine single-file patch candidates authored from BASE before this comparative execution. The current decision criterion is whether the new source comparison changes the information available to an engineering reviewer without compromising the existing rehearsal boundary. This report reconstructs the actual comparative episode; it is not a separately precommitted controlled protocol or a measured comparison of decision quality.

## Actual comparative execution

[Hosted run 46094250281](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/46094250281) succeeded. The exact canonical product first rehearsed both actual candidates against the same BASE, with one changed file, matching patch SHA-256, successful Python syntax and four reviewed fingerprint overlaps each. A patch digest: `9bf43cc0a3498ccefac6904b7198b84d6d0c54bca329ccfbe82f57cf91b6edb5`; B: `672c810691090818a389985dd1977f1ede02985f78c5f61113706aad54d73528`. Active checkout remained clean and at BASE. Then each exact candidate was exercised against the same two genuine retained engineering changes, not synthetic fixtures:

| Real patch | Changed top-level definitions in A and B | B module AST / residual text |
| --- | --- | --- |
| Containment repair, a9fc89c7 -> 8e93f127 | refactor_preview.py: _non_python_mentions | changed / changed |
| Receipt inventory code, d6758a28 -> 0d6671cc, two Python files only | first_use.py: _prompt, _render_markdown; reentry_context.py: _paths, continuity_inventory | unchanged / unchanged for each file |

Both identified the same five definition names across three files, with no truncation. B classified all five AST_CHANGED; A classified all five SOURCE_CHANGED. Both returned equal patched-byte digests for each case, Python syntax passed, and no action authority was granted. The containment repair's module-level import/limit edits differ from the inventory patch's definition-local edits. There was no actual SOURCE_ONLY_CHANGED case or comparative timing in this run; no behavioral-equivalence, independent-use or causal decision-improvement claim follows. The execution-only branch is not merged.

## Selection and retained construction

Select B as reversible BUILD: source and AST comparisons together give the reviewer a more differentiated source-level account without discarding A's textual evidence. These two actual cases do not establish better discovery recall than A, and no runtime distinction follows from a normalized AST. The incremental source complexity is acceptable for the bounded Python overlay use. Retain A as a concrete alternative via its immutable Git commit. Integrate B's exact tested implementation and document the contract. No additional generic comparative consumer is justified. For a Python file, report bounded unique top-level definition changes (ADDED, REMOVED, AST_CHANGED, SOURCE_ONLY_CHANGED), before/after source/AST SHA-256 and line spans, separate module AST and source indicators, count and truncation; duplicate names, parsing/span failure remain NOT_ASSESSED. Nested scopes, indirect effects, comments/type comments outside the AST, runtime behavior, names linked by a rename, cross-version AST fingerprint equivalence and unmodified files are not assessed. Retaining full before bytes and parsing both sides adds memory/processing cost not measured here.

This is subsequent scoped use of the original prospective-intervention possibility, not a new value prediction or replacement of the prior partial outcome. Record the actual comparative observation separately with its limits and a source-qualified capability. The exact implementation was exercised in the hosted comparison; local unit/synthetic tests NOT_RUN. Existing hosted CI unchanged. No new owner decision, Level-4 revision, external target mutation, or release.
