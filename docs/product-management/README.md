# Product Management domain

**Status:** Customer Discovery repository implementation complete; real-harness functional and second-harness portability qualification pending.

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

## Customer Discovery vertical slice

The implemented responsibility sequence is:

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

The current canonical capabilities are `persona`, `discovery`, `interview-synthesis`, `opportunity-tree`, and `hypothesis`.

Repository-side implementation is complete across three merged packages:

1. PR #307 — PM domain contract and 27-capability migration ledger.
2. PR #308 — canonical agent-agnostic Customer Discovery Skill trees.
3. PR #309 — specialized PM validation, Campaign capability registration/admission coverage, adapter parity tests, bounded workflow semantics, and empirical dogfood protocol.

The final Package 3 candidate `897e5850a4ab229eeb2c00e23d91339c3bf8e884` passed Product Validation, Lab Validation, and Release Candidate Distribution before merge as `e7d213e07976a2f269b1479fcc36decdcf0cdeb4`.

## Empirical gate

Implementation completion is not empirical qualification.

Current checked-in native-harness PM attempts: **0**. Current functional empirical PASS: **NONE**. Current second-harness portability PASS: **NONE**.

The repository proves deterministic PM validation/admission and structural adapter parity, including byte-preserving installation of the same canonical PM Skill trees through generic/Codex, Claude, and OpenCode project roots. It does **not** prove that two real native harnesses discovered and invoked those Skills.

Follow `dogfood-runbook.md` and preserve the first real attempt whether PASS, FAIL, or INVALID. Do not migrate the remaining deferred PM capabilities merely because Packages 1–3 merged.

## Documents

- `upstream-provenance.md` — exact upstream source and independent-evolution policy.
- `capability-migration-matrix.md` — disposition of all 27 upstream commands.
- `domain-model.md` — PM responsibilities and capability relationships.
- `automation-boundary.md` — automation levels, authority, and fail-closed behavior.
- `evidence-model.md` — PM evidence classes and claim-strength rules.
- `harness-independence.md` — canonical/runtime separation and adapter contract.
- `artifact-contracts.md` — current specialized Customer Discovery artifact validation boundary.
- `customer-discovery-workflow.md` — bounded agent-native responsibility workflow.
- `dogfood-runbook.md` — real-harness, fresh-context, and portability protocol.
- `dogfood/STATUS.md` — current empirical PM qualification state.
- `milestone-handoff.md` — completed package evidence and next-action handoff.
- `../adr/0028-agent-agnostic-product-management-domain.md` — architectural decision authority.

These documents extend, rather than supersede, `docs/sensemaking-campaign.md`, `docs/capability-registry.md`, `docs/harness-adapters.md`, and the existing Campaign decision/authority contracts.
