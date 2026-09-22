# Strategic Reconciliation & Reserved-Decision Packets v1

**Status:** canonical companion contract  
**Control scope:** Levels 3–4 support surfaces  
**Authority:** semantic-agent authored; no packet grants reserved authority

## Purpose

Strategic Repository Sensemaking produces a decision space. Execution and inquiry
return evidence. This package makes the return path and reserved-decision
boundaries explicit without adding an automatic learning engine or generic
belief database.

```text
strategic analysis
-> bounded responsibility / inquiry
-> returned evidence
-> strategic reconciliation
-> reaffirm / revise / reopen / owner decision / thesis review
```

Reserved decisions use dedicated packets:

```text
OWNER_DECISION
-> owner_decision_capsule

THESIS_REVIEW
-> thesis_review_packet

external/environment evidence needed
-> external_evidence_packet
```

## Strategic reconciliation

`strategic_reconciliation` records how returned evidence bears on a prior
strategic analysis. It may confirm, revise, resolve, invalidate, or leave
unchanged authored claims and assumptions. It may describe path continuation and
one semantic strategic effect.

It does not mutate the prior artifact.

```text
result returned != evidence interpreted
evidence interpreted != strategy automatically changed
reconciliation artifact != implementation authorization
```

## Owner Decision Capsule

`owner_decision_capsule` compresses a decision that repository evidence cannot
resolve because the missing premise is owner preference, risk appetite, policy,
or reserved authority.

It must expose credible options, tradeoffs, reversibility/deferral effects, and
the authority consequence of each option.

Before packaging, it must also check whether the represented option set is
materially adequate. If all options inherit one downstream/proxy framing while
current strategic evidence grounds a materially distinct omitted trajectory, the
Skill must fail closed:

```text
OPTION_SET_INCOMPLETE
-> do not emit a misleading binary capsule
-> return upstream to Strategic Frontier / construction-path synthesis
```

This escape hatch does not authorize the packet Skill to invent strategy. It
only prevents a reserved decision packet from forcing owner choice inside an
option set already shown to be incomplete.

```text
owner decision packet != owner decision made
option described != option selected
two credible options != option set necessarily complete
OPTION_SET_INCOMPLETE != third option invented
```

## Thesis Review Packet

`thesis_review_packet` carries a Level-3 challenge to a Level-4 commitment. It
identifies the challenged commitment, evidence/tension, affected work, candidate
Level-4 dispositions, and required downstream reconciliation.

```text
thesis tension != thesis review outcome
packet produced != owner ratification
```

Only a separately authorized Level-4 transition can ratify
`REAFFIRM | REINTERPRET | REVISE | RETIRE | SUPERSEDE`.

## External Evidence Packet

`external_evidence_packet` preserves bounded provenance for facts that live
outside repository authority. It records sources, claims supported, retrieval
time, and currentness limits.

```text
external evidence != repository fact
source retrieved != claim timeless
packet valid != source true
```

## Policy disposition versus durable companion artifact

The Policy Hierarchy owns semantic questions; these artifacts preserve consequential
results when another actor/context must reconstruct them.

| Semantic disposition / policy | Durable companion when warranted | Boundary |
| --- | --- | --- |
| Learning / Reconciliation | `strategic_reconciliation` | reconciliation artifact != automatic state mutation |
| `OWNER_DECISION_REQUIRED` | `owner_decision_capsule` | packet != owner decision |
| `THESIS_REVIEW_REQUIRED` | `thesis_review_packet` | packet != Level-4 ratification |
| `EXTERNAL_EVIDENCE_REQUIRED` | `external_evidence_packet` | packet != timeless truth |

```text
policy disposition
!= durable companion artifact

durable companion artifact
!= authority transfer

REOPEN_STRATEGY
!= BUILD

THESIS_REVIEW_REQUIRED
!= thesis ratified
```

Strategic reassessment composition is described in
`docs/adaptive-semantic-control-architecture-v0.md`.

## Non-goals

This package does not create:

- a BeliefState or generic knowledge database;
- automatic state mutation;
- automatic owner decisions;
- automatic thesis revision;
- automatic web research;
- semantic truth scoring;
- numeric confidence/ranking;
- Campaign schema v3;
- release/deploy/publication authority.
