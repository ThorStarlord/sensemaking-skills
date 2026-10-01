# Campaign Portability, Completion & Workflow v1 — Closeout Handoff

**Status:** repository-qualified closeout  
**Date:** 2026-09-11  
**Authority:** implementation/qualification record only; current strategic state remains `STATUS.md`  
**Experiments:** no new native-harness, user, comparative, or product-value experiment was performed  
**Campaign schema:** remains v2

## Purpose

This handoff records the third owner-directed build-first sequence after the owner explicitly authorized all proposed packages without using new experiments as a prerequisite.

The sequence preserves:

```text
explicit owner direction
-> may authorize bounded repository-only/hermetic construction

repository qualification
!= native-harness usefulness proof
!= empirical portability proof
!= comparative superiority
!= semantic correctness proof
```

## Delivered package ledger

| Package | PR | Qualified head | Merge SHA | Exact-head qualification |
| --- | --- | --- | --- | --- |
| Portable Target Rebinding v1 | #351 | `f8465d7969adbc6f2d11dc8a8367af7338134c1c` | `0c43fec8a01315be65e97017569da7bcddad1041` | Product Validation #899, Release Candidate Distribution #83, retained Lab Validation #52 PASS |
| Cross-Repository Dependency Declarations v1 | #352 | `f9b6aee2bc79946175e57092ce2afc642ae4d50f` | `c61716c15d122299a656391445314a59828b9cf5` | Product Validation #901, Release Candidate Distribution #84, retained Lab Validation #54 PASS |
| Campaign Completion & Archival v1 | #353 | `a7551b3e3e875fab05d5cca0674e52174e724609` | `2dd73303244d4f3474286c46baeee0c2bd7c303a` | Product Validation #903, Release Candidate Distribution #85, retained Lab Validation #56 PASS |
| Agent Workflow / Golden Path v1 | #354 | `db32709b1d3b518fcd59d76f2c901a66583c184c` | `3420fe92c198c43e4dfbb327bcd701fe16dc2d11` | Product Validation #905, Release Candidate Distribution #86, retained Lab Validation #58 PASS |
| Surface Simplification & Contract Consolidation v1 | #355 | `b49f92b8eda0a1e728a65abbfccc7f382e3f2fde` | `ddbdc6e22604d3291995bc1a157bff07180aa41b` | Product Validation #907, Release Candidate Distribution #87, retained Lab Validation #60 PASS |

Every package was merged only after its exact head passed the applicable shipped-product/distribution/retained-compatibility gates and `main` still matched the candidate base.

## 1. Portable Target Rebinding v1

Delivered surfaces:

```text
campaign target rebind
campaign target verify-rebind
campaign multi-target rebind
```

The primary target's canonical `CampaignState.target_snapshot` is not rewritten when only the filesystem path changes. A hash-bound `target-rebind.json` locator companion records the verified local path. `CampaignService` consults it only when no explicit target override was supplied.

A rebound path is accepted only when repository identity and the exact recorded Git/worktree state are equivalent. Wrong repository identity and changed repository bytes fail closed.

Multi-target rebinding updates only an explicitly selected existing alias after the same identity/state check and records append-only `multi-target-rebind-history.jsonl` provenance.

```text
rebind valid != repository selected
rebind != target refresh
rebind != work authorized
```

## 2. Cross-Repository Dependency Declarations v1

Delivered surfaces:

```text
campaign multi-target relate
campaign multi-target dependency-check
campaign multi-target graph
```

`multi-target-relations.jsonl` records caller-authored relations between aliases already present in the target set. Supported relation classes are:

```text
depends_on
provides_interface_to
consumes_interface_from
must_change_with
release_after
```

The companion validates stable relation identity, alias membership, evidence references, duplicate edges, hash-chain integrity, and self-edges. Only `depends_on` and `release_after` are interpreted mechanically as ordering edges for cycle rejection; descriptive reciprocal relationships remain valid.

Campaign Preflight now validates relation integrity when the companion exists.

```text
relationship recorded != relationship inferred
relationship valid != architecture correct
ordering DAG valid != execution plan correct
release_after != deployment authorized
```

## 3. Campaign Completion & Archival v1

Delivered surfaces:

```text
campaign closeout
campaign completion-receipt
campaign archive
campaign inventory --include-archived
```

`campaign close` remains the semantic terminal decision. `campaign closeout` is accepted only after a terminal Campaign already exists and creates `completion-receipt.json` containing terminal representation, final transition/evidence identity, mechanical preflight/provenance state, and a deterministic SHA-256 manifest of durable workspace files.

Receipt validation is recalculable. New durable workspace bytes make an old receipt stale until the caller explicitly regenerates closeout.

`archive-receipt.json` is a nondestructive marker bound to the current completion receipt. It does not move/delete the workspace and can validly archive terminal states such as `external_blocker` without calling them successful.

```text
completion receipt valid != semantic correctness
terminal != successful
archive != success
archive != delete/move
```

## 4. Agent Workflow / Golden Path v1

Delivered surfaces:

```text
campaign workflow list
campaign workflow show single-repository
campaign workflow show fresh-context
campaign workflow show transferred-campaign
campaign workflow show multi-repository
```

The same static guidance ships in `skills/using-sensemaking/references/golden-paths-v1.md` and is surfaced from `GETTING_STARTED.md`.

Every flow marks explicit `decision_gate` steps and reports that Sensemaking did not select the flow, execute the steps, select a responsibility/capability, or grant authority.

```text
golden path != workflow engine
flow shown != flow recommended
step listed != step authorized
```

## 5. Surface Simplification & Contract Consolidation v1

A bounded `src/sensemaking_skills/campaigns/companion_io.py` now owns only repeated mechanical representation/IO primitives:

```text
canonical_json_bytes
mapping_sha256
atomic_write_json
append_jsonl_fsync
```

Recent target-rebind, multi-target-rebind, target-relation, and completion/archive modules consume those primitives while retaining their own schemas, field selection, diagnostics, and authority semantics.

Semantic Architecture and older persistence systems were deliberately not bulk-migrated merely for stylistic uniformity.

```text
shared IO != shared semantic model
shared hash primitive != shared authority
refactor != schema migration
```

## Preserved product and authority boundaries

The sequence deliberately did not introduce:

- Campaign schema v3;
- `StrategicPlanner` / `OuterLoopEngine`;
- automatic Strategic Frontier ranking;
- automatic responsibility, capability, uncertainty, flow, or repository selection;
- automatic repository discovery/scope expansion;
- semantic relationship inference;
- cross-repository transaction/deployment/rollback coordination;
- automatic terminal/success decisions;
- destructive archive behavior;
- external GitHub provenance publication;
- native-harness execution controlled by Sensemaking;
- new operative experiment state.

## Current disposition

```text
PORTABLE TARGET REBINDING v1 = COMPLETE / REPOSITORY_QUALIFIED
CROSS-REPOSITORY DEPENDENCY DECLARATIONS v1 = COMPLETE / REPOSITORY_QUALIFIED
CAMPAIGN COMPLETION & ARCHIVAL v1 = COMPLETE / REPOSITORY_QUALIFIED
AGENT WORKFLOW / GOLDEN PATH v1 = COMPLETE / REPOSITORY_QUALIFIED
SURFACE SIMPLIFICATION & CONTRACT CONSOLIDATION v1 = COMPLETE / REPOSITORY_QUALIFIED
CAMPAIGN SCHEMA = v2
EMPIRICAL CLAIM CEILINGS = UNCHANGED
NEXT PACKAGE = NOT SELECTED BY THIS CLOSEOUT
```

Future repository-only/hermetic construction may still be authorized by explicit owner direction or a concrete mechanically expressible need. Stronger native-harness/product-value claims still require evidence under their own protocols.

## Current navigation

- Current Level-3 state: [`../STATUS.md`](../STATUS.md)
- Current Level-4 strategy: [`product-strategy.md`](product-strategy.md)
- Frozen control model: [`strategic-outer-loop.md`](strategic-outer-loop.md)
- Non-authoritative future possibilities: [`strategic-candidate-directions.md`](strategic-candidate-directions.md)
- Current operations/qualification runbook: [`operations-runbook.md`](operations-runbook.md)
- Portable rebinding: [`portable-target-rebinding-v1.md`](portable-target-rebinding-v1.md)
- Cross-repository relations: [`cross-repository-dependency-declarations-v1.md`](cross-repository-dependency-declarations-v1.md)
- Completion/archive: [`campaign-completion-and-archival-v1.md`](campaign-completion-and-archival-v1.md)
- Golden paths: [`agent-workflow-golden-path-v1.md`](agent-workflow-golden-path-v1.md)
- Companion IO consolidation: [`surface-simplification-and-contract-consolidation-v1.md`](surface-simplification-and-contract-consolidation-v1.md)

This handoff is historical implementation/qualification evidence after closeout. If it later disagrees with `STATUS.md`, current code, or checked-in CI, those current authority surfaces govern their respective scopes.
