# Extensibility & Simplification v1

**Status:** repository-only bounded productization package  
**Scope:** developer ergonomics + documentation-boundary validation + provenance-graph deduplication  
**Semantic authority:** unchanged  
**Experiments:** none required or performed

## 1. Skill Manifest / Domain Pack catalog

The existing `semantic conformance` command remains the validation authority for Skill Contract Manifests and Domain Packs. This package adds a read-only discovery projection instead of another validator:

```bash
sensemaking-skills semantic catalog \
  --manifests-dir skill-manifests \
  --domain-packs-dir domain-packs \
  --repo-root . \
  --json
```

Optional exact filters:

```text
--skill-id <skill-id>
--domain-id <domain-id>
```

The catalog exposes declared responsibilities, consumed/produced artifacts, semantic concepts, mutation metadata, pack membership/reference metadata, and whether the canonical `skills/<skill-id>/SKILL.md` exists when a repository root is supplied. It also reports the result of the existing aggregate conformance authority.

```text
catalog hit != Skill selection
catalog metadata != semantic quality
conformance PASS != capability warranted for this task
```

## 2. Candidate-directions boundary validator

`docs/strategic-candidate-directions.md` is intentionally idea memory rather than a roadmap. `scripts/validate-candidate-directions.py` checks only the mechanically explicit authority markers that preserve that role:

```bash
python scripts/validate-candidate-directions.py --repo-root .
```

It verifies that the document continues to declare itself non-authoritative, points to the current Level-3/Level-4 authorities, retains the explicit distinction between candidate/Frontier/authorized work, and contains no current implementation-priority declaration.

The validator does **not** judge candidate quality, evidence, priority, or whether an idea should move into the Strategic Frontier.

## 3. Provenance graph simplification

Before this package, `campaign graph` and `campaign graph-integrity` constructed overlapping provenance representations independently. That duplication could allow rendering and integrity checks to drift.

Both surfaces now consume `CampaignProvenanceGraphService`:

```text
Campaign durable state
        |
        v
CampaignProvenanceGraphService
        |--------------------|
        v                    v
campaign graph       campaign graph-integrity
rendering            bounded diagnostics
```

The shared service preserves graph-integrity rejection for mechanically invalid provenance and keeps semantic-causality claims out of both commands.

## 4. Non-goals

This package does not:

- add a second manifest/Domain Pack conformance authority;
- scaffold or mutate Skills automatically;
- rank or select Skills/capabilities;
- make candidate directions executable work;
- rank strategic candidates;
- infer semantic causality from provenance edges;
- add Campaign schema v3;
- perform a native-harness experiment, user trial, or comparative benchmark.

All new claims are repository/mechanical claims qualified by deterministic tests and exact-head CI. Existing empirical evidence ceilings remain unchanged.
