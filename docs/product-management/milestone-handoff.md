# PM Customer Discovery milestone handoff

**Date:** 2026-09-10  
**Milestone:** Agent-Agnostic Product Management — Customer Discovery vertical slice  
**Repository implementation state:** COMPLETE  
**Empirical native-harness qualification state:** PENDING

## Objective delivered

The milestone converted a Claude-Code-origin PM methodology source into a coding-agent-agnostic Sensemaking domain slice without making Claude Code, Codex, OpenCode, or another harness the semantic authority.

The implemented semantic path is:

```text
customer_understanding
-> problem_discovery
-> research_synthesis
-> opportunity_mapping
-> product_hypothesis
```

with canonical Skills:

```text
persona
-> discovery
-> interview-synthesis
-> opportunity-tree
-> hypothesis
```

The active agent still determines warranted responsibility and capability selection. Deterministic machinery validates/admit exact artifacts and records mechanically decidable provenance. Harness adapters expose the same canonical Skill trees at the edge.

## Package evidence

| Package | PR | Final candidate head | Merge commit | Result |
|---|---:|---|---|---|
| 1 — Agent-Agnostic PM Domain Contract & Migration Ledger | #307 | `967bff480d8681290bc294608695677c06bdb4f5` | `539f85e9f55bae6e1e2b1d190aa5c7395ea19d5f` | merged; Product Validation + Release Candidate Distribution passed |
| 2 — Canonical Customer Discovery Capabilities | #308 | `9235e4e550956d9767c2602216eee54274792077` | `a65e596e8afe4e6991be0bbaea4b9427a2ee6de7` | merged; Product Validation + Release Candidate Distribution passed |
| 3 — Artifact, Campaign & Adapter Integration | #309 | `897e5850a4ab229eeb2c00e23d91339c3bf8e884` | `e7d213e07976a2f269b1479fcc36decdcf0cdeb4` | merged; Product Validation + Lab Validation + Release Candidate Distribution passed |

### Observed Package 3 regression and repair

The first Package 3 candidate `e88bb904fa23cea80ab0ca2aa076b4dc351c9a53` correctly promoted `discovery_findings` to the new specialized PM validator, but an older Campaign admission regression test still asserted that `discovery_findings` must use the generic validator. Both Python 3.11 and 3.12 Campaign lanes failed on that stale expectation.

The repair did **not** weaken the PM validator. The generic-fallback coverage was moved to `session_summary`, which remains a generic-validator artifact, while `discovery_findings` retained the stronger specialized PM contract. Candidate `897e5850...` then passed all product, lab, and distribution lanes.

This failure is useful evidence that the new validator boundary actually changed the intended contract rather than being a no-op wrapper.

## Repository-side capabilities now present

### Canonical PM Skills

- `skills/persona/`
- `skills/discovery/`
- `skills/interview-synthesis/`
- `skills/opportunity-tree/`
- `skills/hypothesis/`

Each has one harness-independent semantic implementation and progressive methodology/output-contract references.

### PM artifact validation

`scripts/validate-pm-artifact.py` validates the five current PM artifact identities:

- `persona_definition`
- `discovery_findings`
- `synthesis_report`
- `opportunity_map`
- `hypothesis_statement`

`scripts/validate-and-report.py` routes exactly those PM IDs to the specialized validator while retaining the existing specialized routes and generic fallback for other artifacts.

The PM validator checks only mechanically decidable representation/evidence-shape contracts, including required sections/fields, evidence-status constraints, source traceability, frequency integrity, opportunity scoring from declared inputs, and prohibition on encoding a proposed hypothesis as a completed result.

### Campaign integration

The five Skills are declared in the current Campaign capability registry under explicit agent-supplied responsibility types. They are unranked declared candidates, non-mutating, return control to the active agent, and do not grant external-action authority.

`ArtifactAdmissionService` can admit valid PM artifact bytes through the specialized validator and bind the exact validator/result hashes into the admission receipt. Invalid PM artifacts fail before evidence admission.

### Adapter portability — structural evidence

Repository tests install the same canonical PM Skill bytes through the existing project-scope adapter roots for generic/Codex, Claude, and OpenCode. This proves representation parity in the repository setup system.

It does **not** prove native harness discovery/invocation.

### Bounded Customer Discovery workflow

`docs/product-management/customer-discovery-workflow.md` defines an agent-native workflow envelope by responsibility rather than native command syntax. User authorization can cover bounded continuation through the sequence while evidence, responsibility, scope, and authority remain sufficient.

No deprecated Wayfinder semantic router was reactivated.

## Upstream provenance

The methodological source is pinned to:

```text
lucasgaravelli/pm-skills-claude-code
commit 21cbb2903d740d10fc65c667aea97d3ee8657349
MIT / Flowgrammers 2026
```

All 27 upstream commands are preserved in the migration ledger. The first five are implemented adaptations; the remaining commands stay deferred until evidence warrants the next migration wave.

## What is deliberately NOT complete

The repository currently has zero checked-in real native-harness PM attempts.

Therefore the following claims are **not** established:

- a real supported coding-agent harness natively discovered/invoked the PM Skills;
- a full real Customer Discovery Campaign completes without manual artifact repair;
- a fresh coding-agent context can reconstruct and continue that PM Campaign from durable state in real use;
- a second harness preserves the same canonical PM contract in native execution;
- the remaining 22 upstream PM commands should all migrate unchanged.

## Next action

Follow `docs/product-management/dogfood-runbook.md` and preserve the first real attempt exactly as observed.

If functional and portability dogfood pass, derive the next PM capability wave from that evidence. If either fails or is invalid, preserve the result and implement only the smallest defect exposed by the run.

There is deliberately no pre-authorized Package 4.

## Governing distinctions

```text
canonical PM capability != harness representation
structural adapter parity != native harness invocation
responsibility != capability
available capability != selected capability
artifact valid != conclusion true
artifact admitted != claim warranted
workflow authorized != external mutation authorized
repository implementation complete != empirical portability qualified
```
