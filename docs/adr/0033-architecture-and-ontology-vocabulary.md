# ADR 0033: Architecture and Ontology Vocabulary for Reviewed Knowledge

**Status**: PROPOSED (2026-10-23). Drafted by an agent under the owner's standing request; repository-owner acceptance pending  
**Date**: 2026-10-23  
**Relates to**: ADR 0031 (persistent semantic stewardship), ADR 0032 (receipts). Does not change ADR 0029.  
**Level**: Level 2 contract for the knowledge graph consumed by `repository-semantic-steward` and read by `using-sensemaking`, `repo-sensemaker` and `strategic-repository-analysis`.

## Context

Reviewed knowledge (`.sensemaking/knowledge/*.json`) is the steward's durable output. Its vocabulary (18 claim kinds, 16 predicates) can express decisions, components, contracts, invariants and tests, but not:

- path-scoped architecture rules (which rules apply to an edit);
- cardinality between domain concepts;
- lifecycle states and transitions;
- layers, bounded contexts and data flow;
- confusable and synonymous terms.

The coding agent needs these before editing ("which rules apply to this file?", "is this term the same as that one?"). `docs/semantic-architecture/architecture-ontology-competency-v1.md` tests 15 such questions against the current vocabulary. Eight are not expressible; three are awkward.

## Decision

1. **Extend the existing graph; do not add a parallel schema.** The index, queries, drift audit, preflight check and PR review already operate on it.
2. **Add the minimum useful vocabulary, identifying both failed competencies and explicitly justified conveniences**:
   - kinds: `layer`, `bounded_context`, `lifecycle_state`, `architecture_rule` (with a typed `rule_type`);
   - predicates: `belongs_to`, `relates_to` (with required `cardinality`), `transitions_to`, `flows_to`, `exposes`, `applies_to`, `synonym_of`, `distinct_from`.
3. **Additive and versioned.** Documents using new types declare `schema_version: 2`. Version-1 documents load unchanged, and the v1 snapshot digest is a regression test. An older tool that meets v2 rejects it explicitly.
4. **Generated entries stay mechanical.** Files, directories and Python import edges may be generated, but they count as architecture only after review.
5. **Rules are warnings in v1.** The checker reports findings and per-rule assessment status; unsupported rule types and unassessed source surfaces remain visible, and the checker never fails CI on violations.
6. **Coverage is honestly bounded.** Explicit ownership is distinct from evidence citations. Unmodeled components and ADRs remain NOT ASSESSED; no repository-wide completeness claim or minimum entry count is established.

## Consequences

- Knowledge gains a path-scoped query surface. For materially architecture-sensitive edits, the agent asks "what applies to this file?" and checks decisive sources.
- The vocabulary grows by a bounded set of kinds and predicates; `exposes` is an explicit convenience for the already-representable contract-exposure question, not a newly proven expressive failure.
- Authoring cost rises for architecture entries. Coverage and drift reporting partly offset it.
- Information about rules can go stale. Drift detection reports changed paths that no entry covers; it does not decide that a rule is wrong.

## Principles kept unchanged

- Every entry cites evidence.
- NOT ASSESSED never means absent.
- Knowledge never grants authority (`action_authorized` and `semantic_truth_established` remain false).
- Folder layout or imports alone never prove a dependency.

## Alternatives considered

- **A separate architecture file (C4-style `architecture.yaml`).** Rejected: a second store would drift from the reviewed graph and needs its own indexing and audit.
- **Add every ontology construct at once.** Rejected: the steward's schema-evolution rule requires demonstrated failures first; competency Q4, Q7 and the rest are the gate.
- **Enforce rules in CI immediately.** Rejected for v1: import-level evidence is not architectural proof, and the calibration on this repository is not yet done.

## Reassessment triggers

- The `rules-for` query is not used, or does not change an agent's edit, in the pilot evaluation.
- The checker's warnings are routinely dismissed as noise.
- A second repository needs a construct that none of the added kinds can express.

## Remediation qualification note

The initial pilot evaluation overstated the answer count. The corrected 15-question matrix records 10 answered, 3 partial, 1 not answered, 1 N/A. A nonempty query is not proof of a warranted answer. Rule checking is static and warning-only; source-grounded contracts are checked where their canonical artifact manifest is cited. No agent decision improvement or complete rule coverage has yet been demonstrated.
