# Campaign Operability v1

**Status:** repository-only additive productization surface  
**Campaign schema:** unchanged (v2)  
**External mutation:** none  
**Semantic authority:** unchanged

Campaign Operability v1 adds three deterministic surfaces around already-durable Campaign state: mechanical diagnostics, local provenance rendering, and provenance-graph integrity checks.

## Campaign Doctor

```bash
sensemaking-skills campaign doctor \
  --workspace /path/to/campaign \
  --json
```

Doctor consumes Campaign Preflight v0 and maps mechanical failures to bounded diagnostic classes and inspection commands. It does not modify state or choose a semantic repair.

```text
doctor finding != repair decision
doctor clean != work is warranted
doctor inspection command != execution authority
```

## Local provenance renderer

```bash
sensemaking-skills campaign provenance \
  --workspace /path/to/campaign \
  --format markdown
```

The renderer projects durable Campaign identity, active responsibility metadata, target digests, transition identity/count, evidence refs, preflight state, and uncertainty-history integrity into Markdown suitable for manual inclusion in a pull-request description.

It performs **no GitHub API call** and marks the projection as unpublished.

```text
generate provenance != publish provenance
published provenance != semantic correctness
```

JSON output is also available with `--format json`.

## Provenance graph integrity

```bash
sensemaking-skills campaign graph-integrity \
  --workspace /path/to/campaign \
  --json
```

The checker reconstructs recorded graph relations and rejects mechanically detectable integrity defects including:

- cross-namespace node-ID collisions that would overwrite graph identity;
- duplicate provenance edges;
- missing edge endpoints;
- invalid semantic companion chains;
- dangling/ambiguous addressable semantic references;
- invalid uncertainty-history companions.

An admitted artifact can legitimately be both an artifact reference and Campaign evidence; that dual role is represented without being misclassified as a collision.

## Explicit limits

These features do not:

- infer semantic causality from provenance edges;
- rank evidence or capabilities;
- choose a responsibility;
- repair Campaign state automatically;
- publish comments/checks/descriptions to GitHub;
- merge a pull request;
- establish that implementation is correct;
- expand native-harness or product-value claims.

All three surfaces are repository/hermetic contracts. Exact-head CI may qualify their mechanical behavior without any new empirical experiment.
