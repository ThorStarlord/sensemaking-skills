---
name: strategic-sensemaking-loop
description: orchestrate and resume an end-to-end strategic repository Sensemaking episode from one prompt. Use when a user wants to start, continue, or resume strategic repository work without manually prompting strategic-repository-analysis, using-sensemaking, handoff, strategic-repository-reconciliation, and owner-decision-capsule in sequence. Reconstruct current durable state, invoke only the specialized stages that are warranted, execute already-selected work within authority, reconcile returned evidence, and stop at genuine owner, Level-4, external, or no-further-work boundaries.
---

# Strategic Sensemaking Loop

Provide a **single front door** for strategic repository Sensemaking while
preserving the specialized Skills as separate semantic responsibilities.

This Skill is a composition/control surface. It does not replace the component
Skills, create a new strategic policy, or introduce a second truth system.

## Responsibility

From the user's current goal, repository state, authority, and existing durable
artifacts:

1. reconstruct where the current Sensemaking episode actually is;
2. invoke only the specialized Skill(s) needed from that point;
3. execute or delegate an already-warranted responsibility when authority permits;
4. return consequential evidence through reconciliation;
5. continue autonomously through repository-answerable steps;
6. stop only at a justified terminal, blocked, reserved, or higher-level boundary.

The normal specialized surfaces are:

```text
strategic-repository-analysis
using-sensemaking
handoff
strategic-repository-reconciliation
owner-decision-capsule
```

Adjacent reserved boundaries such as `thesis-review-packet` remain available
when the existing control model warrants them.

## Core laws

```text
one front door != one semantic responsibility
orchestration != deterministic planning
resume marker != durable state
existing artifact != unquestionable truth
stage completed != stage must rerun
returned evidence != strategy automatically changed
owner decision packet != owner decision made
responsibility selected != implementation authorized
handoff useful != handoff mandatory
Campaign available != Campaign required
```

Do **not** create a new master strategic artifact or orchestration state file.
Durable truth remains in the existing strategic, responsibility, execution,
reconciliation, owner-decision, Campaign, and repository artifacts.

Read `references/resume-and-routing-v1.md` whenever existing artifacts mean the
episode may need to resume in the middle rather than start from strategic
analysis.

## 1. Reconstruct the current episode before invoking another Skill

Inspect the smallest sufficient set of current sources:

- the user's current request and explicit authority;
- current repository/source identity and decision-relevant governing docs;
- `artifacts/strategic_repository_analysis.md` when present;
- `artifacts/strategic_reconciliation.md` when present;
- current responsibility/decision artifacts such as
  `artifacts/sensemaking_decision.md` when present;
- handoff / execution evidence or Campaign execution receipts when present;
- `artifacts/owner_decision_capsule.md` when present;
- explicit owner choice supplied after a decision capsule.

Determine the **latest semantically valid boundary**, not merely the newest file
timestamp.

Do not rerun an earlier stage merely because it is part of the canonical loop.

## 2. Select the current control boundary

Use these semantic resume states only as reasoning labels; do not persist them as
a new runtime state machine:

```text
ANALYZE
RESPONSIBILITY
EXECUTE
RECONCILE
OWNER_DECISION
THESIS_REVIEW
STOP
```

### ANALYZE

Use `strategic-repository-analysis` when:

- no current Level-3 strategic analysis exists and repository future is materially open;
- an existing reconciliation explicitly warrants `REOPEN_ANALYSIS`;
- current governing intent/source reality materially invalidates the prior analysis.

Do not reopen strategy for ordinary drift, currentness noise, or because another
idea is imaginable.

### RESPONSIBILITY

Use `using-sensemaking` when:

- strategic direction is current but the next bounded responsibility is not;
- an owner selection has resolved a reserved premise and now needs translation
  into a bounded responsibility;
- returned non-strategic evidence changes continuation/responsibility without
  requiring Level-3 reopening.

Treat upstream recommendations as defeasible. Preserve the
inherited-responsibility prerequisite backstop in `using-sensemaking`.

### EXECUTE

When a bounded responsibility is selected:

1. verify decision-critical prerequisites;
2. verify exact authority for the contemplated action;
3. choose the lightest execution boundary.

```text
same active agent + clear bounded action
-> execute directly

cross-actor / copy-paste Skill transition useful
-> handoff

durable multi-context delegation useful
-> Campaign execution handoff

protected / owner-reserved action
-> stop or escalate
```

Use `handoff` only when a prompt handoff to a **registered Skill** is actually
the correct next boundary. Do not invent a Skill identity for a workflow,
GitHub Action, tool, active coding agent, or other non-Skill executor. For those
cases use direct execution or the existing Campaign/executor interface.

Execution is not itself another semantic Skill requirement.

### RECONCILE

After consequential evidence returns:

- apply the Learning / Reconciliation guidance from `using-sensemaking`;
- use `strategic-repository-reconciliation` when the evidence can materially
  affect prior strategic claims, assumptions, path continuation, frontier, or
  strategic effect;
- do not invoke strategic reconciliation for trivial execution details that
  cannot change Level 3.

Follow the resulting strategic effect:

```text
NO_MODEL_CHANGE / REAFFIRM
-> continue or stop according to responsibility state

REVISE_STRATEGY
-> use the reconciled state as current Level-3 input

REOPEN_ANALYSIS
-> return to ANALYZE

OWNER_DECISION
-> OWNER_DECISION

THESIS_REVIEW_REQUIRED
-> THESIS_REVIEW
```

### OWNER_DECISION

Use `owner-decision-capsule` only when repository evidence cannot resolve the
decisive premise because it is genuinely owner-reserved.

After producing an adequate capsule, **stop for the owner**. Never synthesize or
guess the owner's selection.

If the user has already explicitly selected an option in the current request,
do not recreate the capsule merely because one exists. Treat the explicit owner
selection as new intent/authority input and return to RESPONSIBILITY.

If the capsule reports `OPTION_SET_INCOMPLETE`, return upstream to the
Strategic Frontier/path-synthesis boundary rather than forcing a choice.

### THESIS_REVIEW

When `THESIS_REVIEW_REQUIRED` is established, use the existing
`thesis-review-packet` when a durable Level-4 review packet is warranted, then
stop for the required owner/Level-4 authority. Do not silently revise the product
thesis.

### STOP

Stop when any of these is true:

- the current responsibility is verified complete and no further warranted
  responsibility exists;
- no repository/product change is warranted;
- a genuine owner-reserved decision is waiting;
- a Level-4 thesis decision is waiting;
- an external/infrastructure blocker cannot be resolved within current authority;
- the next action requires authority not granted by the current user/repository;
- no further decision-changing evidence or action is warranted.

## 3. Continue autonomously without prompt-by-prompt ceremony

When the user has delegated ordinary repository-answerable continuation, do not
pause between internal stages merely to request another prompt.

A healthy episode may look like:

```text
current repository
-> strategic-repository-analysis
-> using-sensemaking
-> direct bounded execution
-> returned evidence
-> strategic-repository-reconciliation
-> STOP
```

or:

```text
existing strategic_repository_analysis
+ existing sensemaking_decision
-> EXECUTE
-> returned evidence
-> strategic-repository-reconciliation
-> owner-decision-capsule
-> STOP FOR OWNER
```

or:

```text
owner explicitly selects prior capsule option
-> using-sensemaking
-> bounded responsibility
-> execute
-> reconcile
-> continue / stop
```

The correct sequence is whatever the current evidence/authority warrants, not a
mandatory five-stage pipeline.

## 4. Artifact-aware resume rules

Preserve provenance across stages.

Prefer an existing current artifact over recreating an equivalent one. If the
artifact is stale or contradicted, reconcile or reopen through the normal
control path instead of silently overwriting it.

Never use conversation memory as the sole basis for a consequential resume when
durable repository artifacts are available.

Do not treat file recency as semantic precedence:

```text
newer timestamp
!= newer decision

strategic reconciliation referencing SRA-X
+ returned evidence
-> may supersede continuation assumptions from SRA-X
without mutating SRA-X
```

See `references/resume-and-routing-v1.md` for the detailed resume table.

## 5. Authority and execution boundaries

At every downward transition preserve:

```text
KNOW
DECIDE
ACT
PUBLISH / MERGE / RELEASE
```

as separable authority surfaces.

A user's instruction to proceed autonomously authorizes repository-answerable
steps only to the extent of the user's actual scope and repository policy. It
does not silently grant protected publication, merge, deployment, release,
credential, billing, or unrelated external mutation authority.

No component artifact grants authority merely by existing.

## 6. Final report

Do not create a new canonical orchestration artifact.

At the end of the run, report:

1. resume point reconstructed;
2. specialized Skills actually invoked;
3. artifacts consumed;
4. artifacts produced or updated by those Skills;
5. non-Skill execution surfaces/actions used;
6. returned evidence obtained;
7. final strategic state/disposition;
8. final bounded responsibility state;
9. authority boundary reached;
10. exact stop reason and next owner input only when one is genuinely required.

A concise session summary may be emitted for the user, but it is not a new source
of truth and must not compete with the underlying artifacts.

## Non-goals

Do not introduce:

- a StrategicPlanner or deterministic semantic router;
- a mandatory five-Skill sequence;
- a new Campaign schema;
- a new strategic/master artifact;
- automatic repository discovery or scope expansion;
- automatic owner decisions;
- automatic Level-4 thesis revision;
- automatic merge/release/publication authority;
- numeric path/resume/priority scoring;
- repeated analysis merely for ceremony.
