# PM Customer Discovery milestone handoff

**Date:** 2026-09-10  
**Milestone:** Agent-Agnostic Product Management — Customer Discovery vertical slice  
**Repository implementation state:** COMPLETE  
**Empirical native-harness qualification state:** PENDING  
**Post-milestone policy:** additional repository implementation may proceed; empirical dogfood gates stronger support/promotion claims rather than implementation expansion.

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

## Repository-side capabilities delivered

### Canonical PM Skills

- `skills/persona/`
- `skills/discovery/`
- `skills/interview-synthesis/`
- `skills/opportunity-tree/`
- `skills/hypothesis/`

Each has one harness-independent semantic implementation and progressive methodology/output-contract references.

### PM artifact validation

`scripts/validate-pm-artifact.py` validates the five first-slice PM artifact identities:

- `persona_definition`
- `discovery_findings`
- `synthesis_report`
- `opportunity_map`
- `hypothesis_statement`

`scripts/validate-and-report.py` routes those PM IDs to the specialized validator while retaining existing specialized routes and generic fallback for other artifacts.

### Campaign integration

The five Skills are declared in the current Campaign capability registry under explicit agent-supplied responsibility types. They are unranked declared candidates, non-mutating, return control to the active agent, and do not grant external-action authority.

`ArtifactAdmissionService` can admit valid PM artifact bytes through the specialized validator and bind the exact validator/result hashes into the admission receipt. Invalid PM artifacts fail before evidence admission.

### Adapter portability — structural evidence

Repository tests install the same canonical PM Skill bytes through the existing project-scope adapter roots for generic/Codex, Claude, and OpenCode. This proves representation parity in the repository setup system.

It does **not** prove native harness discovery/invocation.

### Non-qualifying preflight

PR #311 preserved one repository-side preflight against Chess Mentor Engine. It exercised Campaign responsibility, unranked capability inspection, a contract-valid `discovery_findings` artifact, specialized validation/admission, lineage, handoff, validation, and reconstruction. Because no supported native coding-agent executable was available, the preflight remains explicitly non-qualifying and the real-harness attempt count stays zero.

## Upstream provenance

The methodological source is pinned to:

```text
lucasgaravelli/pm-skills-claude-code
commit 21cbb2903d740d10fc65c667aea97d3ee8657349
MIT / Flowgrammers 2026
```

All 27 upstream commands remain preserved in the migration ledger. The first five are repository-qualified adaptations.

## Qualification claim ceiling

The following claims are still **not** established:

- a real supported coding-agent harness natively discovered/invoked the PM Skills;
- a full real Customer Discovery Campaign completes without hidden manual repair;
- a fresh native coding-agent context reconstructs and continues that PM Campaign from durable state in real use;
- a second harness preserves the same canonical PM contract in native execution;
- repository-qualified PM output is necessarily strategically correct or empirically validated.

## Post-milestone policy amendment

The initial handoff treated native-harness dogfood as a gate before any PM expansion. After the repository-side architecture and preflight demonstrated that further capability implementation can be isolated behind the same contracts, the program now uses a more precise maturity model:

```text
CANDIDATE
-> REPOSITORY_QUALIFIED
-> NATIVE_HARNESS_QUALIFIED
-> PORTABILITY_QUALIFIED
-> PROMOTED
```

Repository CI and deterministic contracts remain mandatory. Native-harness and portability evidence are deferred qualification debt until performed.

Therefore:

```text
dogfood before promotion
!=
dogfood before expansion
```

Additional separately authorized PM waves may proceed to `REPOSITORY_QUALIFIED`. They must not be described with stronger support/promotion claims until the corresponding empirical evidence exists.

See `qualification-levels.md` for the normative policy.

## Governing distinctions

```text
canonical PM capability != harness representation
structural adapter parity != native harness invocation
responsibility != capability
available capability != selected capability
artifact valid != conclusion true
artifact admitted != claim warranted
workflow authorized != external mutation authorized
repository qualified != native-harness qualified
native-harness qualified != portability qualified
portability qualified != promoted
```
