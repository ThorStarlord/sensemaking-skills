# Refactor rename preview (2026-11-25)

**Status:** generative product capability, exercised by applying its own verified
patch to a real symbol rename.
**Source baseline:** `c08a498bd2163fe90b8869bc2ebe46990b69ea69` (PR #974).
**Implementation:** `f87c6011f6b06adf2e31d04774cbc5ccef4a4e3e`.
**Blocking-scope fix:** `5f906e859a38646c7633a2ecdfe1a07a27206ee3`.
**Real rename:** `02383645706c65397fe4a0dd061e391bfa76f5d3`.

## 1. Selection context

Two developed candidates were compared after the verification-scenario
increment:

- **Possibility Crucible.** A scenario battery over authored assumptions that
  would develop a thin `poss:` candidate into a worksheet. Its own strongest
  rejection applied: the goal-family ecology has very few authored assumptions,
  so the bench would mostly emit `DATA_GAP` ceremony, and the owner had
  explicitly warned against another planner or opportunity-scoring layer.
- **Refactor rename preview.** A patch-only transformation that turns existing
  reference knowledge into an implementation artifact. It produces a new
  capability rather than another view, record or evaluation.

The refactor preview was selected because it changes what an agent can
accomplish: compute a cross-file rename, inspect every resolved edit, and receive
a verified patch or a fail-closed refusal. The possibility bench would mainly
describe what the agent already had to author by hand.

## 2. Observed limitation

The existing `context-for --symbol` surface listed direct references, test
candidates, a behavior surface and guard scenarios. It did not compute the
change itself. For a rename, an agent still had to locate imports, rewrite
unaliased name loads, handle `__all__`, decide whether module-alias attributes
belonged to the same symbol, and then hope nothing dynamic was missed.

The CLI had no surface that transformed target source. The new command fills
that gap without adding a record, schema, planner or router.

## 3. Delivered capability

`sensemaking-skills semantic refactor-rename --repo . --ref HEAD \
--path FILE --symbol OLD --to NEW [--patch-out FILE] [--json]`

It reads one committed revision and computes a unified patch for one tracked
top-level Python function or class:

- rewrites the definition, direct `from module import OLD` imports, unaliased
  name loads, module-alias attribute loads and literal `__all__` entries;
- applies the patch in a disposable exact-revision checkout;
- requires every changed file to parse, the AST delta to contain only the
  intended identifier/string changes, and a rescan to find zero direct old-name
  references;
- reports `READY` with a patch, or `BLOCKED` with unresolved sites and no
  applicable patch.

It fails closed on ambiguous definitions, star imports, rebinding, new-name
collisions, dynamic imports and exact string constants in related Python files.
It never edits the active checkout.

## 4. Authentic use

The capability was used on a real semantic-precision rename:

`build_verification_scenarios` → `build_guard_scenarios`

The builder only derives candidates from direct `raise`/`assert` guards, so the
narrower name preserves the existing claim ceiling.

Observed preview:

- status `READY`, coverage `COMPLETE_FOR_DIRECT_PYTHON_REFERENCES`;
- 3 edits across 2 files: the definition, one import and one call;
- `git apply --check` PASS, patch applied in the temporary checkout;
- `files_parse` PASS, `ast_delta` `IDENTIFIERS_ONLY`, old-reference residue `0`;
- `--patch-out` wrote the unified patch, which was then applied to the working
  tree; `git grep -w build_verification_scenarios` returned no matches.

A second real preview on `_import_from_base` → `_resolve_import_from_base`
produced 8 edits across `source_relationships.py` and `refactor_preview.py`,
including the cross-file import, and also returned `READY` with zero residue.

A collision preview, `build_guard_scenarios` → `build_source_relationships`,
returned `BLOCKED` with `NEW_NAME_ALREADY_BOUND`, no patch, and a separately
labelled `proposed_patch` for inspection.

## 5. Authentic feedback

1. **Windows stdin encoding.** The first hosted-equivalent check failed because
   `subprocess.run(text=True, input=patch)` translated `\n` to `\r\n` on
   Windows; the same patch applied from a file. The verification call now passes
   bytes.
2. **Multi-line definition span.** The span helper initially rejected the
   function definition because its `end_lineno` is later than its `lineno`. The
   helper now applies the one-line constraint only to identifier tokens, not to
   the whole definition node.
3. **Over-broad dynamic blocking.** Computed `getattr(obj, name)` in any related
   file blocked the rename, including `getattr(node, field)` in the preview's
   own AST comparison. Blocking is now limited to exact symbol strings and
   computed access on a resolved module alias. This materially improved
   usefulness without claiming dynamic completeness.
4. **Non-Python disclosure.** A preview whose old name appears in the hosted
   workflow YAML reported the file under `not_rewritten` and downgraded coverage.
   The patch is still `READY`, but the mention is visible; the tool does not
   modify YAML, docs or configuration.

## 6. Product versus model

**Product:** exact-revision scanning, import resolution, binding checks,
identifier-span edits, patch generation, disposable-checkout application, AST
delta comparison and residue scanning.

**Model:** selected the symbol, judged the rename worth making, reviewed the
preview, applied the patch and decided whether to accept the result. The tool
did not decide that the rename was semantically correct or that the repository
was ready.

## 7. Claim ceiling

| Level | Status |
| --- | --- |
| Real cross-file rename patch generated | Observed |
| Patch applied and verified in a disposable checkout | Observed |
| Applied to the working tree with zero direct old-name residue | Observed |
| Collision and dynamic-site refusals | Observed locally |
| Hosted CI for the new command | PENDING / TO VERIFY |
| Runtime behavior, test coverage or API compatibility | NOT ESTABLISHED |
| Generated code, re-exports, inheritance and non-Python consumers | NOT ASSESSED / LISTED |
| Independent later-agent reuse or comparative cognitive benefit | NOT ESTABLISHED |

The capability is patch-only and bounded. `READY` is not a correctness verdict.

## 8. Continuation

The next warranted use is an independent agent applying a rename preview to a
change with downstream tests and recording whether the patch changed its
verification set. Moving symbols, renaming methods or variables, rewriting
string registries and executing behavior checks are not assumed; they require
evidence from that use. A rename that spans non-Python configuration should be
treated as partial until the listed mentions are handled.
