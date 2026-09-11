# Uncertainty History v0

**Status:** repository-only additive Campaign companion  
**Current authority:** `CampaignState.active_uncertainty` remains authoritative for the current active uncertainty  
**Campaign schema:** unchanged (v2)  
**Semantic authority:** agent-authored lifecycle observations; no deterministic ranking or selection

## Purpose

Uncertainty History v0 preserves consequential uncertainty lifecycle events after an uncertainty stops being the one current active uncertainty.

It is intentionally an append-only companion file:

```text
uncertainty-history.jsonl
```

It does not add an uncertainty registry to Campaign schema v2 and does not become a second current-state authority.

## Commands

Append an explicit agent-authored lifecycle observation:

```bash
sensemaking-skills campaign uncertainty-record \
  --workspace /path/to/campaign \
  --event-id UE-12 \
  --uncertainty-id U-7 \
  --status resolved \
  --transition-id T-21 \
  --evidence-ref evidence/decision-record.md
```

Inspect/validate the history:

```bash
sensemaking-skills campaign uncertainty-history \
  --workspace /path/to/campaign \
  --json
```

Supported lifecycle labels are:

```text
active
resolved
deferred
superseded
abandoned
```

These labels are records supplied by the active agent. The deterministic layer does not decide which label is semantically correct.

## Mechanical contracts

The companion validates:

- append-only event identifiers;
- safe uncertainty/transition identifiers;
- supported lifecycle labels;
- SHA-256 previous-event chaining;
- referenced transition existence when supplied;
- evidence references against current Campaign evidence authority;
- `superseded_by` shape and distinct identity;
- an `active` history event may name only the current `CampaignState.active_uncertainty`.

That last rule preserves the authority boundary: the companion may observe the currently active uncertainty but cannot activate a different one.

## Resume integration

Resume Capsule v1 includes a bounded uncertainty-history summary containing presence, integrity, event/uncertainty counts, and latest recorded lifecycle label by uncertainty identity.

```text
latest recorded history status
!= current CampaignState.active_uncertainty authority
```

A fresh agent can therefore reconstruct history without treating it as an automatic next-uncertainty selector.

## Non-goals

Uncertainty History v0 does not:

- rank uncertainties;
- choose which uncertainty is decision-changing;
- mutate `CampaignState.active_uncertainty`;
- infer that an uncertainty is resolved from evidence;
- score confidence or materiality;
- create a universal uncertainty ontology;
- reproduce hidden reasoning;
- migrate Campaign schema v2.

## Qualification boundary

Hash-chain integrity, identifier/reference validation, active-authority binding, CLI behavior, and Resume Capsule projection are repository/hermetic contracts. No native-harness experiment or user study is required to qualify them mechanically. Existing empirical claim ceilings remain unchanged.
