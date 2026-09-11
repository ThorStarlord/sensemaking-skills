# Strategic Outer Loop Ergonomics v1

**Status:** owner-authorized repository-only/hermetic construction package  
**Empirical experiments:** none required or performed  
**Strategic planner:** not introduced

## Purpose

Reduce reconstruction and handoff friction around the frozen Outer Loop v0 while preserving the existing authority law: lower levels may execute explicit higher-level decisions but may not silently redefine them.

## Surfaces

### `campaign strategy inspect`

Reads a repository-local `STATUS.md` and projects mechanically addressable Level-3 sections, current Strategic Frontier item identities/dispositions, thesis-review marker, and a SHA-256 identity of the exact status bytes.

It does not rank frontier entries or infer which boundary matters most.

### `campaign strategy diff`

Compares two explicit `STATUS.md` representations and reports changed sections/frontier representations. It does not decide which strategic state is better.

### `campaign strategy handoff`

Creates a Campaign only after the caller explicitly supplies:

- an exact current Strategic Frontier item identity;
- Campaign identity and mission;
- responsibility identity, type, statement, blocked decision, scope, authority, and success conditions.

The command mechanically verifies that the supplied frontier identity occurs in the current `STATUS.md`, records the exact source-status SHA-256, and initializes Campaign schema v2 state plus `strategy-handoff.json`.

```text
frontier membership != warranted responsibility
explicit handoff != tool selection
transported authority != inferred authority
```

## Boundaries

This package does not add:

- `StrategicPlanner` or `OuterLoopEngine`;
- automatic Strategic Frontier ranking;
- automatic responsibility selection;
- automatic Level-4 thesis revision;
- semantic comparison of strategies;
- native-harness/product-value experiments.

The new surfaces make explicit decisions easier to inspect, compare, and transport. They do not make those decisions.