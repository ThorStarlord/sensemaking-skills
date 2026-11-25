# Symbol behavioral surfaces across revisions (2026-11-25)

**Status:** product-capability increment and one authentic historical review.
**Source baseline:** `97ac8bc51cd7637e55fa80d314eb34190ad6a380`.
**Implementation:** `2f8cdbd031e43391de0d6990c31ee7f7a7bfe6d0`.

The capability adds a bounded source-level behavioral surface to the existing
symbol context and compares it across BASE/TARGET in committed source review.
It does not establish semantic behavior, runtime behavior or test coverage.

## 1. Observed limitation

The merged source review paired identities (`base_only`, `target_only`,
`both`) for top-level symbols. That answers whether a name existed at both
revisions, not whether its behavior surface changed. A symbol present at both
revisions could gain parameters, decorators, docstring obligations, raises or
assertions while still appearing as `both`.

A concrete historical case existed in the repository's own recent work. Between
`e920a6e9` and `97ac8bc5`, `build_source_relationships` was reported as
`function:build_source_relationships` in the `both` set, but its signature
gained a `symbol` parameter and its body gained a malformed-symbol
`ValueError`. The identity comparison could not show that.

## 2. Delivered capability

`context-for --symbol <name>` now attaches a `behavior` surface to each selected
top-level definition:

- normalized signature with defaults and annotations;
- decorators;
- docstring summary and full-docstring SHA-256;
- direct `raise` types and lines;
- direct `assert` tests and lines;
- exact definition source SHA-256, line range and truncation.

`workspace-review-context --source-symbol <name>` now adds
`symbol_behavior_comparison` with:

- `presence`;
- `changed_fields` (`kind`, `signature`, `decorators`, `docstring_summary`,
  `docstring_sha256`, `raises`, `assertions`, `source_sha256`);
- `source_changed`;
- BASE and TARGET behavior surfaces;
- `COMPLETE_FOR_REPORTED_BEHAVIOR`, `PARTIAL` or `NOT_COMPARABLE`.

The behavior lists are bounded by the existing `--limit`. A difference is a
review signal, not a semantic change verdict.

## 3. Authentic use

**Task:** review the real source-analysis change that introduced the `symbol`
parameter and decide whether its behavioral change was adequately visible and
verified.

Observed with `workspace-review-context --base-ref e920a6e9 --ref 97ac8bc5`
on `source_relationships.py`:

- identity comparison: `function:build_source_relationships` was in `both`;
- behavior comparison: `COMPLETE_FOR_REPORTED_BEHAVIOR`;
- `changed_fields`: `signature`, `raises`, `source_sha256`;
- base signature:
  `(root: str | Path, target_ref: str, path: str, *, limit: int=50) -> dict[str, Any]`;
- target signature adds `symbol: str | None=None`;
- direct raises rose from four to five `ValueError` sites;
- source body hash changed.

The same comparison on `_safe_path` showed `both` with no changed fields and
`source_changed: false`, providing a stable-symbol contrast.

The review also showed no direct symbol test candidates for
`build_source_relationships`. The new malformed-symbol raise therefore had no
direct test reference. A hosted negative check was added for a malformed
`--symbol` argument, and the existing hosted CLI checks cover the valid path.
No code repair was warranted: the new parameter is optional, and the new raise
is an input-validation guard.

## 4. What the product provides versus the model

**Product:** exact-revision AST extraction, normalized signature, decorator and
docstring surfaces, direct raise/assert extraction, source-body hashing,
bounded lists, BASE/TARGET pairing and explicit limits.

**Model:** selected the review symbol, read the base/target signatures and
raises, noticed the missing direct test candidate, judged that the defaulted
parameter and CLI checks made a repair unnecessary, and added a bounded
negative check. The product did not decide that the behavior was safe.

No intrinsic cognitive improvement or comparative benefit is claimed.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Signature/decorator/docstring/raise/assert extraction | Observed on real symbols |
| BASE/TARGET behavior-surface comparison | Observed on a real historical change |
| Stable-symbol contrast | Observed on `_safe_path` |
| Semantic or runtime behavior equivalence | NOT ASSESSED |
| Test coverage or pass status | NOT ASSESSED |
| Consequence or impact verdict | NOT ESTABLISHED |
| Independent later-agent reuse or better review decisions | NOT ESTABLISHED |

## 6. Continuation

The next warranted use is an independent reviewer applying the behavior
comparison to a real signature or body change and recording whether it changed
the inspection or verification decision. No transitive body analysis, runtime
call graph, consequence engine or automatic violation verdict is warranted
without that use. A justified `NO_CODE_CHANGE` remains valid.
