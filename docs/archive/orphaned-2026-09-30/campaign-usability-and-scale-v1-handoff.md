# Campaign Usability & Scale v1 — Closeout Handoff

**Status:** repository-qualified closeout  
**Date:** 2026-09-11  
**Authority:** implementation/qualification record only; current strategic state remains `STATUS.md`  
**Experiments:** no new native-harness, user, comparative, or product-value experiment was performed  
**Campaign schema:** remains v2

## Purpose

This handoff records the second owner-directed build-first sequence after the owner explicitly authorized the proposed usability, strategic-ergonomics, and scale packages without using new experiments as a prerequisite.

The sequence preserves the established evidence rule:

```text
explicit owner direction
-> may authorize bounded repository-only/hermetic construction

repository qualification
!= native-harness usefulness proof
!= portability proof
!= comparative superiority
!= general autonomous-development proof
```

## Delivered package ledger

| Milestone | PR | Qualified head | Merge SHA | Exact-head qualification |
| --- | --- | --- | --- | --- |
| Campaign Usability & Composition v1 | #347 | `36d0ef2a79e7a3b07aec68162749d8d75caf4b6b` | `b0c38957b56717082cc01ebe95f406353ecdd191` | Product Validation #887, Release Candidate Distribution #75, retained Lab Validation #44 PASS |
| Strategic Outer Loop Ergonomics v1 | #348 | `ceb95f4eade4531e47dc578dbef0ace1bf219429` | `93d7e2c42698c53ba5f7b1b210061b27a3e23f24` | Product Validation #889, Release Candidate Distribution #76, retained Lab Validation #46 PASS |
| Multi-Repository Campaigns v1 | #349 | `6d79a5650e02db672e1019bb0900212879ae5ab1` | `b229aecd23efa423910b579c8f5266da53fc12ae` | Product Validation #893, Release Candidate Distribution #79, retained Lab Validation #50 PASS |

The final multi-repository candidate deliberately added one extra composition guard before merge: when `multi-targets.json` exists, Campaign Preflight now checks all declared target identities/live snapshots. Multi-target drift or tampering therefore makes preflight fail mechanically; explicit target refresh can restore PASS when repository identity remains stable.

## Delivered product surfaces

### Campaign Usability & Composition v1

```text
campaign resume-profile --profile minimal|working|audit
campaign capability-context --responsibility-type <explicit-type>
campaign uncertainty-relate
campaign uncertainty-show <uncertainty-id>
campaign uncertainty-graph
campaign bundle-inspect
campaign bundle-resume-context
campaign bundle-graph
campaign inventory
```

Resume Capsule v2 adds deterministic progressive disclosure and optional tail-preserving item bounds while the original `campaign resume-context` v1 surface remains backward compatible.

Capability Context enumerates declared compatible capabilities only after the agent supplies the responsibility classification. It does not select a capability.

Uncertainty Relationships adds an append-only companion for explicit relations such as `depends_on`, `blocks_decision`, `introduced_by_transition`, `resolved_by_transition`, and `supersedes`. It does not rank uncertainties, and `CampaignState.active_uncertainty` remains current authority.

Bundle inspection projects verified bundle contents/resume/provenance through an ephemeral internal workspace before any durable import destination is created.

Campaign inventory enumerates direct child Campaign workspaces and their mechanical state/integrity without prioritizing them.

### Strategic Outer Loop Ergonomics v1

```text
campaign strategy inspect
campaign strategy diff
campaign strategy handoff
```

`strategy inspect` projects mechanically addressable Level-3 `STATUS.md` state and exact source-byte identity.

`strategy diff` reports representation changes between two explicit status documents without judging which one is better.

`strategy handoff` initializes Campaign v2 state only after the caller supplies an exact current Strategic Frontier identity plus explicit responsibility, classification, authority, scope, and success conditions. It records the source `STATUS.md` SHA-256 in Campaign extensions and `strategy-handoff.json`.

```text
frontier membership != responsibility selection
strategy handoff != planning engine
transported decision != inferred decision
```

### Multi-Repository Campaigns v1

```text
campaign multi-target add
campaign multi-target inspect
campaign multi-target verify
campaign multi-target refresh
```

The implementation preserves `CampaignState.target_snapshot` and schema v2. Explicit multi-repository scope lives in the additive `multi-targets.json` companion with:

```text
alias
role
authority
evidence refs
TargetSnapshot
snapshot SHA-256
target-set SHA-256
```

`multi-target-history.jsonl` preserves explicit target refresh edges. `campaign preflight` now consumes the target-set integrity check when the companion is present.

## Multi-repository evidence ceiling

The implementation establishes deterministic target-set identity, duplicate identity rejection, workspace/target separation, live drift detection, explicit refresh, and tamper detection.

It does **not** establish:

- semantic correctness of a cross-repository responsibility;
- automatic discovery of repositories that should be included;
- cross-repository transaction/commit atomicity;
- deployment atomicity or rollback coordination;
- automatic merge/release authority;
- native-harness usefulness.

```text
multi-target verified != cross-repo transaction
same Campaign != atomic deployment unit
all targets current != semantic completion
```

## Preserved authority boundaries

The sequence deliberately did not introduce:

- Campaign schema v3;
- `StrategicPlanner` or `OuterLoopEngine`;
- automatic Strategic Frontier ranking;
- automatic responsibility selection;
- automatic capability selection;
- automatic uncertainty selection/ranking;
- semantic summarization in Resume Capsule;
- automatic repository discovery/scope expansion;
- cross-repository transaction machinery;
- external GitHub provenance publication;
- native-harness execution controlled by Sensemaking;
- new operative experiment state.

Important non-identities remain:

```text
progressive disclosure != semantic summarization
capability compatibility != capability selection
uncertainty relation != uncertainty ranking
bundle projection != durable import
Campaign inventory != prioritization
strategy diff != strategy preference
strategy handoff != responsibility selection
multi-target integrity != semantic correctness
repository qualified != native-harness qualified
owner direction to build != empirical product-value proof
```

## Current disposition

```text
CAMPAIGN USABILITY & COMPOSITION v1 = COMPLETE / REPOSITORY_QUALIFIED
STRATEGIC OUTER LOOP ERGONOMICS v1 = COMPLETE / REPOSITORY_QUALIFIED
MULTI-REPOSITORY CAMPAIGNS v1 = COMPLETE / REPOSITORY_QUALIFIED
CAMPAIGN SCHEMA = v2
EMPIRICAL CLAIM CEILINGS = UNCHANGED
NEXT PACKAGE = NOT SELECTED BY THIS CLOSEOUT
```

Future repository-only/hermetic construction may still be authorized by concrete mechanically expressible need or explicit owner direction. Stronger empirical/native-harness claims still require the evidence specified by their own protocols.

## Current navigation

- Current Level-3 state: [`../STATUS.md`](../STATUS.md)
- Current Level-4 strategy: [`product-strategy.md`](product-strategy.md)
- Frozen control model: [`strategic-outer-loop.md`](strategic-outer-loop.md)
- Non-authoritative future possibilities: [`strategic-candidate-directions.md`](strategic-candidate-directions.md)
- Current operations/qualification runbook: [`operations-runbook.md`](operations-runbook.md)
- Campaign Usability & Composition: [`campaign-usability-composition-v1.md`](campaign-usability-composition-v1.md)
- Strategic Outer Loop Ergonomics: [`strategic-outer-loop-ergonomics-v1.md`](strategic-outer-loop-ergonomics-v1.md)
- Multi-Repository Campaigns: [`multi-repository-campaigns-v1.md`](multi-repository-campaigns-v1.md)
- Prior productization closeout: [`campaign-productization-v1-handoff.md`](campaign-productization-v1-handoff.md)

This handoff is historical implementation/qualification evidence after closeout. If it later disagrees with `STATUS.md`, current code, or checked-in CI, those current authority surfaces govern their respective scopes.