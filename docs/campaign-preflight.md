# Campaign Preflight v0

**Status:** repository-only productization contract  
**Scope:** read-only aggregation of already-authoritative mechanical Campaign checks  
**Campaign schema:** unchanged (v2)  
**Semantic authority:** unchanged; the active coding agent still decides whether work is warranted

## Purpose

`campaign preflight` provides one deterministic place to inspect whether the durable Campaign representation is mechanically coherent before consequential work continues.

```bash
sensemaking-skills campaign preflight \
  --workspace /path/to/campaigns/CMP-0001
```

An optional responsibility classification may be supplied by the active agent:

```bash
sensemaking-skills campaign preflight \
  --workspace /path/to/campaigns/CMP-0001 \
  --responsibility-type repository_diagnosis
```

Preflight never derives that classification from responsibility prose.

## What v0 checks

The command composes existing authorities instead of reimplementing them:

- Campaign reconstruction and transition-chain integrity;
- evidence/admission integrity already enforced by the Campaign store;
- live target identity/state consistency for target-bound Campaigns;
- mechanically consistent responsibility/authority metadata;
- exact-current-state handoff integrity when a handoff exists;
- optional semantic-companion chain and addressable reference integrity;
- unranked compatible capability enumeration when the caller supplies a responsibility type.

`not_addressable` semantic references remain informational. A capability may be declared `external`; preflight reports that availability rather than treating it as a mechanical failure.

## Result semantics

Successful output uses:

```text
CAMPAIGN_PREFLIGHT_PASS
```

A mechanically invalid aggregate uses:

```text
CAMPAIGN_PREFLIGHT_FAIL
```

JSON output includes per-check status, diagnostics, and bounded mechanical data.

A PASS means only that the checks represented by this command do not currently report a mechanical integrity failure.

```text
preflight PASS
!= evidence is persuasive
!= responsibility is warranted
!= capability is semantically appropriate
!= capability is executable in the current harness
!= owner authorization
!= agent should proceed
```

The command therefore always preserves the explicit limit:

> Mechanical preflight does not decide whether the agent should proceed.

## Non-goals

Campaign Preflight v0 does not:

- select or rank a responsibility;
- infer a responsibility type;
- choose or rank a capability;
- grant execution authority;
- convert `external` capability availability into native-harness proof;
- establish semantic truth;
- repair a Campaign automatically;
- add a new Campaign schema;
- duplicate existing validators merely to create a new source of truth.

## Qualification boundary

This capability can be repository-qualified through deterministic positive and rejection tests plus exact-head Product Validation and Release Candidate Distribution.

No native-harness experiment, comparative agent benchmark, customer trial, or other empirical experiment is required to establish the repository/mechanical contract. Existing empirical claim ceilings remain unchanged.
