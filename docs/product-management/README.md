# Product Management domain

**Status:** first milestone authorized; architecture contract established here before capability implementation.

The Product Management domain adapts external PM methodologies into Sensemaking's existing Campaign model. The domain is **coding-agent agnostic**: responsibility, methodology, evidence, artifact, authority, lineage, and stop semantics are canonical; Claude Code, Codex, OpenCode, generic Agent Skills, and future harnesses are representations at the edge.

## Canonical boundaries

```text
responsibility != capability
available capability != selected capability
selected capability != execution authority
artifact valid != conclusion true
artifact admitted != claim warranted
methodology applied != empirical validation
workflow authorized != external mutation authorized
canonical capability != harness representation
Skill copied to discovery root != harness observed or invoked Skill
```

The active agent owns semantic judgment. Deterministic machinery owns mechanically decidable contracts such as representation, validation, admission, provenance, integrity, lineage, and harness availability evidence.

## First milestone

The first vertical slice is Customer Discovery:

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

Candidate capabilities are `persona`, `discovery`, `interview-synthesis`, `opportunity-tree`, and `hypothesis`.

The milestone is implemented in three bounded packages:

1. PM domain contract and migration ledger.
2. Canonical Customer Discovery capabilities.
3. Artifact, Campaign, and adapter integration.

After Package 3, implementation stops for real-harness dogfood and a second-harness portability check. The remaining upstream PM commands are not bulk-enabled by this milestone.

## Documents

- `upstream-provenance.md` — exact upstream source and independent-evolution policy.
- `capability-migration-matrix.md` — disposition of all 27 upstream commands.
- `domain-model.md` — PM responsibilities and capability relationships.
- `automation-boundary.md` — automation levels, authority, and fail-closed behavior.
- `evidence-model.md` — PM evidence classes and claim-strength rules.
- `harness-independence.md` — canonical/runtime separation and adapter contract.
- `../adr/0028-agent-agnostic-product-management-domain.md` — architectural decision authority.

These documents extend, rather than supersede, `docs/sensemaking-campaign.md`, `docs/capability-registry.md`, `docs/harness-adapters.md`, and the existing Campaign decision/authority contracts.
