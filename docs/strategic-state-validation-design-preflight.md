# Strategic State Contract Validation v0 — Design Preflight

**Document type:** Level-3 design preflight / construction gate decision  
**Status:** COMPLETE — `BUILD`  
**Assessed checkout:** `main` at `095bccc8120014d74ad224ac15f704027a84c9c2`  
**Assessed:** 2026-09-11  
**Mode:** repository-grounded construction preflight; no empirical experiment

## Decision

```text
BUILD STRATEGIC STATE CONTRACT VALIDATION v0
```

The fresh post-B7 Level-3 reassessment authorizes one bounded repository-validation package.

The package is narrower than a general “strategic consistency” engine. It validates only the mechanically decidable representation contract of the current Level-3 authority surface (`STATUS.md`) and its canonical authority pointers. It does not decide whether strategy, frontier selection, capability claims, or current responsibility are semantically correct.

No `strategy inspect`, `strategy diff`, Level-3→Campaign bridge, Level-4 reconciliation engine, or later package is authorized by this decision.

## 1. Why construction is warranted now

The Strategic Outer Loop foundation deliberately started as Markdown authority rather than a runtime schema. That choice remains valid, but repeated repository work has now exposed a concrete maintenance/integrity boundary around the Level-3 surface.

### Observed pressure 1 — foundation closeout

PR #331 integrated the Strategic Outer Loop foundation. The merged `STATUS.md` still described that now-integrated foundation as `ACTIVE` / in construction. PR #332 was required immediately afterward to reconcile the Level-3 state, mark the responsibility complete/integrated, remove the stale active responsibility, and return Level 3 to reassessment.

This was not evidence that the strategy was wrong. It was evidence that a current authority surface can retain mechanically stale or malformed operational declarations across repository evolution.

### Observed pressure 2 — B7 integration

PR #330 integrated B7 Semantic Reference Resolution & Integrity Audit. The pre-existing Level-3/entrypoint documentation still described B7 as parallel / not integrated until the separate post-merge reconciliation in PR #334.

Again, this does not prove that all strategic currentness can be inferred mechanically. It does show repeated synchronization burden at the repository's current authority boundary.

### Existing contract support

`docs/strategic-state-contract.md` already states that a future validator may mechanically check:

- required authority surfaces exist;
- referenced files/ADRs/Campaigns resolve where a contract makes them addressable;
- status metadata is structurally present;
- declared current strategy pointers are unique and non-broken;
- explicitly declared current-state representations are not mechanically contradictory where the contradiction can be detected without interpretation.

The repository therefore has both repeated pressure and a pre-existing mechanical boundary.

## 2. Important claim limit

The motivating incidents involved post-merge staleness, but v0 must not pretend that GitHub/branch/currentness semantics are derivable from prose.

In particular:

```text
STATUS says ACTIVE
!= validator can prove work is not complete

PR merged
!= local validator may infer which prose should change

file exists
!= strategic capability semantically complete
```

Without an explicit existing machine-addressable execution/currentness contract, v0 does **not** query GitHub, interpret commit messages, infer owner intent, or decide that an `ACTIVE`, `COMPLETE`, `DEFERRED`, or `CANDIDATE` disposition is semantically wrong.

The observed incidents justify hardening the mechanically expressible part of the state boundary, not inventing a new strategic-state schema merely to catch every stale sentence.

## 3. v0 responsibility

The validator answers only:

> Does the current Level-3 strategic-state authority surface satisfy the explicitly ratified mechanical representation contract needed for deterministic reconstruction?

It may establish:

```text
required authority surface exists
required Level-3 section anchor exists exactly once
canonical authority pointer exists exactly once
canonical authority pointer resolves to a repository file
thesis-review marker is present exactly once and uses an allowed literal
Strategic Frontier item identity is not duplicated within the current frontier projection
```

It must not establish:

```text
strategy is good or correct
frontier item is important
selected boundary is highest leverage
responsibility is warranted
capability claim is true
repository qualification is semantically sufficient
owner should approve a thesis change
PR/branch state from external GitHub metadata
currentness from prose alone
```

## 4. Authority surfaces

v0 uses only repository-local files on the checked-out target tree.

Required canonical surfaces:

```text
STATUS.md
docs/product-strategy.md
docs/strategic-outer-loop.md
docs/strategic-state-contract.md
docs/product-thesis-revision.md
```

`STATUS.md` remains the Level-3 operational authority. The validator does not replace it with YAML/JSON or a generated projection.

The canonical pointers inside `STATUS.md` are:

```text
Level-4 authority       -> docs/product-strategy.md
Control model           -> docs/strategic-outer-loop.md
Level-3 contract        -> docs/strategic-state-contract.md
Level-4 revision contract -> docs/product-thesis-revision.md
```

The validator checks pointer identity and repository-local resolution only.

## 5. Required Level-3 anchors

For v0, the following headings become stable mechanical reconstruction anchors in `STATUS.md`:

```text
## Strategic Repository Evolution state — Level 3
### Current product strategy
### Current capability state
### Material limitations and evidence ceilings
### Strategic Frontier
### Current highest-leverage boundary
### Current decision-changing uncertainty
### Current warranted repository-level responsibility
### Authority / owner direction
### Thesis review state
## Current next step
```

Each must occur exactly once.

This does not require every conceptual field in `strategic-state-contract.md` to become a machine field. Prose within the sections remains human/agent-authored.

`Completed evidence and reassessment` / `Expected evidence and reassessment` remains prose-level and is not a required exact heading in v0 because its heading legitimately changes with lifecycle state.

## 6. Thesis-review marker

Within `### Thesis review state`, v0 requires exactly one explicit marker using the existing contract term:

```text
THESIS_REVIEW_REQUIRED
```

The mechanically accepted value is:

```text
YES | NO
```

Markdown emphasis/backticks around the marker/value may be tolerated by the parser. The validator does not determine whether YES or NO is semantically correct.

## 7. Strategic Frontier identity check

Within the `### Strategic Frontier` section, v0 may parse numbered bold frontier declarations of the current repository form:

```text
1. **<frontier name> — <declared disposition>.** ...
```

A normalized frontier name may appear at most once in that section.

If the same frontier identity is declared twice, v0 reports an integrity error rather than attempting to decide which disposition is correct.

The validator does **not** impose a closed disposition vocabulary in v0. Existing Level-3 documents intentionally distinguish dimensions such as `COMPLETE / INTEGRATED / REPOSITORY_QUALIFIED`, `DEFERRED BY OWNER DIRECTION`, and `CANDIDATE / NOT AUTHORIZED`. Collapsing those into a runtime enum would be premature.

Likewise, v0 does not require an `ACTIVE` frontier item. “No current boundary selected” is a valid Level-3 state.

## 8. Result contract

The standalone script should follow existing repository-validator conventions:

```json
{
  "valid": true,
  "validator": "validate-strategic-state.py",
  "status_file": "STATUS.md",
  "checks": [],
  "errors": [],
  "semantic_truth_established": false
}
```

Each diagnostic should include a stable `error_id`, field/surface context, current value where useful, and a human-readable message.

Planned error IDs:

```text
STRATEGIC_STATE_STATUS_NOT_FOUND
STRATEGIC_STATE_REQUIRED_SURFACE_MISSING
STRATEGIC_STATE_SECTION_MISSING
STRATEGIC_STATE_SECTION_DUPLICATE
STRATEGIC_STATE_POINTER_MISSING
STRATEGIC_STATE_POINTER_DUPLICATE
STRATEGIC_STATE_POINTER_MISMATCH
STRATEGIC_STATE_POINTER_BROKEN
STRATEGIC_STATE_THESIS_REVIEW_MISSING
STRATEGIC_STATE_THESIS_REVIEW_DUPLICATE
STRATEGIC_STATE_THESIS_REVIEW_INVALID
STRATEGIC_STATE_FRONTIER_DUPLICATE_ITEM
```

The exact implementation may consolidate diagnostics only when doing so preserves deterministic failure identity.

## 9. CLI / execution boundary

Implementation surface:

```text
scripts/validate-strategic-state.py
```

Suggested CLI:

```text
python scripts/validate-strategic-state.py --repo-root .
python scripts/validate-strategic-state.py --repo-root . --json
```

Default status path is `STATUS.md`. A `--status` override may be supported for tests/fixtures if it remains repository-contained or explicitly treated as a test input.

This is repository validation infrastructure, **not a new shipped product `strategy` CLI family**.

Do not add:

```text
sensemaking-skills strategy inspect
sensemaking-skills strategy diff
sensemaking-skills strategy recommend
sensemaking-skills strategy plan
```

## 10. CI integration

If implemented, v0 should be part of Product Validation's repository-contract authority.

Preferred integration:

```text
Repository and Skill contracts
  -> Strategic state contract validation
  -> existing stable repository assertion suite includes validator tests
```

Do not fold semantic strategy decisions into `scripts/validate-repo.py`. Keeping the validator standalone preserves a narrow, independently testable contract.

No installed-wheel product claim is added by this repository-only script.

## 11. Required negative/rejection tests

Implementation qualification must cover at least:

1. Current valid repository strategic state passes.
2. Missing `STATUS.md` fails with `STRATEGIC_STATE_STATUS_NOT_FOUND`.
3. Missing canonical Level-4 strategy surface fails.
4. Missing required Level-3 heading fails.
5. Duplicate required Level-3 heading fails.
6. Missing canonical pointer fails.
7. Duplicate canonical pointer fails.
8. Pointer aimed at a non-canonical path fails even if that other file exists.
9. Canonical pointer aimed at a missing file fails.
10. Missing `THESIS_REVIEW_REQUIRED` marker fails.
11. Duplicate thesis-review marker fails.
12. Invalid thesis-review literal fails.
13. Duplicate normalized Strategic Frontier item identity fails.
14. Multiple distinct frontier candidates remain valid.
15. No active/highest-leverage boundary remains valid when the section explicitly says none is selected.
16. Semantically questionable prose does not fail merely because the validator disagrees with its meaning.
17. External PR/branch state is never queried or inferred.
18. Output always preserves `semantic_truth_established: false`.

## 12. Explicit non-goals

v0 does not introduce:

```text
StrategicPlanner
OuterLoopEngine
automatic frontier ranking
automatic responsibility selection
automatic Campaign generation
strategy recommendation
strategy diff/inspect UI
Level-4 thesis revision automation
Campaign schema change
strategic-state YAML/JSON schema
universal strategic identity registry
GitHub/remote currentness queries
semantic truth scoring
```

It also does not make every `strategic-state-contract.md` concept executable.

## 13. Abort / scope-control gate

Implementation must stop or omit a proposed check if that check requires any of:

```text
interpreting whether a frontier item matters
inferring whether COMPLETE / ACTIVE / DEFERRED is semantically correct
querying GitHub to infer integration state
creating a new structured strategic-state store solely for validation
ranking alternatives
inferring owner intent
inferring currentness from ordinary prose
```

The package remains buildable as long as the mechanically expressible subset in Sections 4–8 can be implemented independently.

If implementation discovers that even those checks require semantic interpretation, abort the validator rather than weakening the semantic-authority boundary.

## 14. Post-implementation rule

After exact-head qualification and integration:

```text
update Level-3 state
reassess from zero
```

Do not automatically proceed to:

```text
strategy inspect/diff
Level-3 -> Campaign bridge
Level-4 reconciliation machinery
```

A later package must independently demonstrate a concrete consumer or mechanically decidable integrity/reconstruction gap.

## Final preflight outcome

```yaml
decision: BUILD
package: Strategic State Contract Validation v0
scope: repository-local Level-3 representation integrity
status_authority: STATUS.md
new_strategic_schema: false
product_cli_added: false
semantic_authority_added: false
external_currentness_inference: false
strategy_ranking: false
experiments_required: false
post_package_queue_pre_authorized: false
```
