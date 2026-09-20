# Strategic Repository Sensemaking v1 — Milestone Handoff

**Status:** functional milestone complete; terminal currentness closeout pending its own qualification gate  
**Date:** 2026-09-19  
**Authority:** owner-directed Issue #401  
**Release line:** `1.0.0rc3.dev0` development toward `1.0.0rc3`  
**Experiment posture:** no synthetic/model-comparison experiment was required or performed for this milestone

## 1. Objective

Make repository-level strategic analysis a first-class Sensemaking product
surface before a bounded implementation task has already been selected.

```text
repository + governing intent
        |
current system model
        |
capability / limitation map
        |
Strategic Frontier
        |
coherent construction paths
        |
qualitative path comparison
        |
decision-changing uncertainty
        |
strategic synthesis
        |
BUILD / INVESTIGATE / DEFER / NO_CHANGE /
OWNER_DECISION / THESIS_REVIEW
        |
bounded responsibility only when warranted + separately authorized
```

The milestone does not productize a deterministic StrategicPlanner. The active
semantic agent remains responsible for generating paths, comparing them, and
making the strategic judgment.

## 2. Package ledger

| Package | PR | Qualified head | Merge SHA | Qualification |
| --- | --- | --- | --- | --- |
| A — Strategic Analysis Contract | #403 | `d413d8c98fa0cb1e6435efb33c0f15a068140a5b` | `f3f9ef682a1b5b27167fdec8ebd0112b32afbebd` | PR Product `35481010243` PASS; PR Release Distribution `35481010191` PASS; integrated Product `35481081176` PASS; integrated Release Distribution `35481081179` PASS |
| B — Construction Path Synthesis & Product Integration | #404 | `5d74eaa0f1d319a3e48a3d91889c9b35b64cf06c` | `44ee0d5a65f94990dc7064f6c29a12055bd95c42` | PR Product `35481237943` PASS; PR Release Distribution `35481237897` PASS; integrated Product `35481312550` PASS; integrated Release Distribution `35481312659` PASS |

Package A PR-head tree and integrated tree matched:
`ef469773e865d081958a1b89a93fe3edad161fa4`.

Package B PR-head tree and integrated tree matched:
`1fbdc3852767cca2af94a71bae807160364b100c`.

Package C is currentness/closeout only. Its PR and Issue #401 carry the terminal
qualification receipt. Source should not be mutated afterward merely to copy
transient post-merge run identifiers into this file.

## 3. First-class artifact and Skill

The supported engineering Skill is:

```text
strategic-repository-analysis
```

It produces:

```text
strategic_repository_analysis
artifacts/strategic_repository_analysis.md
```

The artifact is registered in the canonical/compatibility artifact contracts,
canonical and packaged vocabulary, engineering Domain Pack, Skill manifest and
registry, and the Version 1.0 supported-Skill inventory.

## 4. Current-system and capability model

Strategic analysis reconstructs the repository as a product/system rather than
as a file inventory.

Decision-relevant capabilities use bounded semantic states:

```text
ESTABLISHED
PARTIAL
MISSING
DEFERRED
BLOCKED
CLAIMED_UNVERIFIED
OUT_OF_SCOPE
```

These are not maturity scores.

```text
missing capability
!= strategic priority
```

Repository evidence, owner-supplied intent, inference, and claim ceilings remain
distinguishable.

## 5. Construction paths

A construction path is a coherent future capability state plus the major
capability sequence, dependencies, tradeoffs, reversibility, and evidence gaps
needed to reach it.

```text
construction path
!= feature list
!= backlog
!= roadmap commitment
```

The Skill allows 0–5 materially real paths, with the stable zero-path semantics finalized by PR #409. Zero paths is valid when no coherent
construction trajectory is currently warranted/representable; `BUILD` still
requires a selected real path. Multiple paths are generated only when they
represent materially different futures rather than renamed implementation
details.

## 6. Qualitative comparison

Material paths are compared through the existing Level-3 lenses:

1. mission relevance;
2. decision value;
3. blocking power;
4. evidence sufficiency / resolvability;
5. consequence of error;
6. deferral cost;
7. reversibility;
8. authority availability;
9. dependency;
10. smallest warranted intervention.

The specialized validator rejects numeric comparison values and explicit
score/weight/rank fields.

```text
qualitative comparison
!= deterministic ranking
```

Mechanical validation cannot determine which path is strategically correct.

## 7. Decision-changing uncertainty and policy composition

After comparison, the agent asks which unresolved premise could materially
change the strategic disposition.

Policy Hierarchy Completion v0 composes with this surface and is now
complete/integrated:

- Inquiry Policy v0 — whether more evidence is worth obtaining;
- Metareasoning Policy v0 — whether to act, inquire, challenge, explore, verify,
  escalate, or stop;
- Exploration Policy v0 — how to allocate iterative search;
- Warrant / Choice Policy v0 — whether a particular target is justified;
- Learning / Reconciliation Policy v0 — what returned evidence changes;
- stable Strategic Alternatives — represented directly by the construction-path
  surface in this milestone;
- Adaptive Policy Coordinator v0 — qualitative composition of the policy layers
  without automatic routing or authority expansion.

```text
uncertainty identified
!= inquiry automatically required

policy available
!= policy must run visibly

policy composition
!= automatic routing

policy output
!= action authorization
```

PR #411 completed the authorized Policy Hierarchy package set before this
Strategic Repository Sensemaking closeout.

## 8. Strategic disposition

The artifact supports:

```text
BUILD
INVESTIGATE
DEFER
NO_CHANGE
OWNER_DECISION
THESIS_REVIEW
```

Only `BUILD` may nominate a candidate repository-level responsibility, and:

```text
candidate responsibility
!= implementation authorization
```

`INVESTIGATE` nominates bounded evidence-producing work.
`OWNER_DECISION` names an owner preference/authority decision.
`THESIS_REVIEW` escalates a challenged Level-4 commitment.
`DEFER` and `NO_CHANGE` create no implementation task by default.

## 9. Diagnostic versus strategic repository sensemaking

The product now distinguishes:

```text
repo-sensemaker
-> diagnostic repository understanding
-> current evidence / gaps / weakest consequential boundary

strategic-repository-analysis
-> Level-3 repository evolution synthesis
-> coherent futures / path tradeoffs / strategic disposition
```

A current `repository_sensemaking_brief` may be reused as evidence, but is not
mandatory when the strategic Skill can establish current state directly from
the authorized repository evidence surface.

This prevents “analyze how the repo could be built” from collapsing into
“diagnose one task and produce a handoff.”

## 10. Human and agent entry points

`using-sensemaking` routes open repository-future questions into
`strategic-repository-analysis`.

README and Getting Started expose the distinction without requiring the user to
know the internal Level-3 vocabulary.

A user can ask:

> What could this repository become from here? What are the coherent ways it
> could be constructed, what distinguishes those paths, and what strategic
> direction or inquiry is warranted?

without starting from a preselected implementation task.

## 11. Mechanical validator boundary

`scripts/validate-strategic-repository-analysis.py` checks only mechanically
decidable representation and integrity:

- required machine fields;
- capability-state vocabulary;
- frontier/path identifier integrity;
- path field shape;
- qualitative-comparison lens completeness;
- no numeric scoring/ranking;
- decision-changing uncertainty shape;
- strategic disposition references;
- BUILD path/responsibility coherence;
- explicit authority/semantic-truth false flags;
- immutability marker.

It reports:

```text
semantic_truth_established = false
strategy_selected_by_validator = false
implementation_authorized_by_validator = false
```

## 12. Architecture preserved

The milestone did **not** create:

- a product `StrategicPlanner`;
- an `OuterLoopEngine`;
- numeric path/priority/warrant scores;
- deterministic best-path ranking;
- automatic responsibility selection;
- automatic Skill/workflow/repository selection;
- automatic Campaign creation;
- Campaign schema v3;
- generic `AgentState`;
- generic cognition/state database;
- automatic Level-4 thesis revision;
- autonomous merge/release/deploy/publication.

The semantic model remains the strategic reasoner.

## 13. Relationship to StrategicPlanner lab work

Issue #395 remains historical lab evidence at `RESEARCH_MORE`.

Strategic Repository Sensemaking v1 does not promote StrategicPlanner v0 into
the product. The v1 capability is a structured semantic-agent surface, not a
deterministic planning engine.

Synthetic StrategicPlanner testing remains stopped as the active development
mode.

## 14. Relationship to Policy Hierarchy Completion v0

Policy Hierarchy Completion v0 is complete/integrated/composable.

Its seven bounded packages are present:

- Inquiry Policy v0;
- Metareasoning Policy v0;
- Exploration Policy v0;
- Warrant / Choice Policy v0;
- Learning / Reconciliation Policy v0;
- stable Strategic Alternatives;
- Adaptive Policy Coordinator v0.

Strategic Repository Sensemaking v1 consumes those semantic-control contracts
without becoming a planner or routing service.

```text
Issue #401 complete
!= policy hierarchy removed

Policy Hierarchy complete
!= policy must activate visibly

Adaptive Policy Coordinator integrated
!= automatic routing
```

No additional Issue #399 construction package is selected by this closeout.

## 15. Release posture

Current source remains:

```text
1.0.0rc3.dev0
target = 1.0.0rc3
status = development
```

Qualified RC2 remains immutable historical provenance at
`c9b86138d3919c4fce87040f14161364a0c1c3a0`.

This milestone does not authorize:

- RC3 freeze;
- PyPI publication;
- release tagging;
- final `1.0.0`.

## 16. Claim ceilings

Repository qualification establishes implementation/contract/currentness
coherence.

It does not establish:

- that generated construction paths are strategically optimal;
- superiority over unaided reasoning;
- native-harness usefulness;
- independent-harness portability;
- product-market value;
- that any selected construction path will succeed.

No experiment was required to make this owner-directed product capability exist.

## 17. Terminal continuation rule

After the terminal closeout PR integrates and its exact integrated tree passes
Product Validation and Release Candidate Distribution:

```text
STRATEGIC_REPOSITORY_SENSEMAKING_V1 = COMPLETE
ISSUE_401_CONSTRUCTION = STOP
```

Use the capability when repository evolution is genuinely the question.

Do not open Strategic Repository Sensemaking v2 merely because more strategic
machinery can be imagined. Reopen only from concrete pressure or explicit owner
direction.

Issue #384 remains the unrelated external GitHub-admin governance action.
