# Agent-authored campaign decisions

**Status:** P5 product contract  
**Scope:** explicit `advance`, `defer`, and `close` decisions layered on the existing Campaign lifecycle service

## Purpose

P5 closes the gap between admitted campaign evidence and a durable campaign
transition without introducing a semantic router.

The control boundary is:

```text
admitted / durable campaign evidence
        ↓
active coding agent interprets the evidence
        ↓
agent explicitly authors advance / defer / close
        ↓
typed P5 decision contract
        ↓
existing CampaignService lifecycle primitive
        ↓
recoverable TransitionRecord + CampaignState + trace
```

The deterministic layer never decides that the evidence warrants one of these
outcomes. It only validates and persists the structural consequences of the
agent-authored decision.

## Typed decision boundary

P5 adds three transient typed inputs in
`src/sensemaking_skills/campaigns/decisions.py`:

- `AdvanceDecision`
- `DeferDecision`
- `CloseDecision`

and one adapter:

- `CampaignDecisionService`

These inputs are not a second durable schema. Durable state continues to use the
existing `CampaignState`, `Responsibility`, `DeferredResponsibility`,
`TransitionRecord`, `TerminalState`, and `CampaignTrace` contracts.

The adapter deliberately delegates persistence to the P2 lifecycle service:

```text
advance → CampaignService.record_transition(...)
defer   → CampaignService.defer_responsibility(...)
close   → CampaignService.terminate(...)
```

P5 therefore does not create a second transaction, recovery, trace, or state
write path.

## `campaign advance`

`advance` means:

> The active agent has explicitly determined that the current evidence warrants
> entering a new durable state with exactly one active next responsibility.

Example shape:

```text
sensemaking-skills campaign advance \
  --workspace /path/to/CMP-0001 \
  --transition-id TR-0010 \
  --to-state bounded_work \
  --decision "The admitted diagnosis warrants one bounded architecture review" \
  --evidence artifacts/repository_sensemaking_brief/<sha>.md \
  --responsibility-id R-ARCH-001 \
  --responsibility-statement "Review the identified architecture boundary" \
  --decision-blocked "Whether an implementation change is warranted" \
  --scope "Architecture review only; no implementation" \
  --authority authorized_autonomously \
  --success-condition "Review produces an evidence-grounded recommendation" \
  --json
```

The next responsibility is supplied by the agent. P5 does not infer it from the
artifact, mission, state label, workflow registry, or capability metadata.

The command intentionally requires an explicit responsibility id, statement,
blocked decision, scope, authority classification, and at least one success
condition. The supplied decision evidence is also recorded as the next
responsibility's trigger evidence.

A referenced evidence path must already satisfy the current campaign evidence
contract. In particular:

```text
file under artifacts/
!= admitted campaign evidence
```

An orphan artifact without a valid admission receipt cannot support an
`advance` decision.

## `campaign defer`

`defer` means:

> The agent is explicitly preserving the current responsibility as deferred
> rather than fabricating progress or silently dropping it.

Required agent-authored fields include:

- transition id and target state;
- decision rationale;
- deferral reason;
- optional `reopen_when` conditions;
- optional `not_reopened_by` conditions;
- optional durable evidence refs.

The reopening condition remains optional because that is the existing canonical
`DeferredResponsibility` contract. P5 packages that contract; it does not tighten
it. When the agent knows a concrete reopening condition it should record one,
but an honest deferral with no currently knowable reopening trigger remains
representable as `reopen_when: []`.

The command delegates to the existing P2 `defer_responsibility` primitive. That
primitive moves the active responsibility into `deferred_responsibilities`,
clears executable responsibility/authority from the current state, and commits
the transition through the existing recoverable lifecycle transaction.

## `campaign close`

`close` means:

> The agent explicitly concludes that the campaign should enter one existing
> `TerminalState` classification.

Example terminal classifications include:

- `goal_achieved`
- `no_further_work_warranted`
- `owner_decision_required`
- `authority_boundary_reached`
- `external_blocker`
- `evidence_insufficient`
- `invalid_execution`
- `deferred`
- `qualified_pr_ready`

`close` delegates to the existing P2 `terminate` primitive. Terminal campaigns
fail closed if a later caller attempts to advance them.

## JSON success surfaces

The three commands emit stable success codes:

```text
CAMPAIGN_ADVANCED
CAMPAIGN_DEFERRED
CAMPAIGN_CLOSED
```

With `--json`, each success response contains the normal durable campaign status,
the exact replacement campaign state under `state`, and the exact committed
transition under `transition`. This exposes defer reason/reopening metadata and
other decision-relevant replacement-state fields without requiring an agent
harness to scrape YAML or prose.

The commands reuse the existing campaign error taxonomy. Structurally invalid
or impossible lifecycle decisions remain `CAMPAIGN_TRANSACTION_ERROR` and use
the campaign workspace/precondition exit class rather than inventing a second
P5-specific error hierarchy.

## Authority semantics

P5 records authority; it does not manufacture it.

For `advance`, the next responsibility carries the authority classification
explicitly supplied by the agent. The transition itself remains bound to the
source campaign authority under the existing P2 contract.

Therefore:

```text
new responsibility authority
!= source transition authority
```

These fields answer different structural questions and are not silently
rewritten to match one another.

P5 does not turn `owner_authorization_required` into evidence that the owner
actually authorized an external mutation. Existing owner/authority governance
continues to apply.

## Evidence semantics

The P4 evidence boundary remains authoritative.

P5 never parses artifact contents to decide whether a transition is warranted.
It only asks whether each referenced evidence ref is already valid durable
campaign evidence.

Thus:

```text
validator passed
!= semantic conclusion is true

admitted evidence
!= automatic advance
```

The active agent remains responsible for the semantic inference between those
two states.

## Reconstruction and handoff

A P5 decision is complete only when the existing lifecycle service can
reconstruct it from durable state, transition history, trace, and evidence.

P5 uses the P2 transaction protocol, so interruption recovery remains:

```text
prepare exact state / transition / trace
→ durable commit intent
→ materialize transition
→ materialize trace
→ invalidate stale handoff
→ replace current state last
→ verify exact reconstruction
```

A fresh process must observe the same authored decision without requiring the
conversation that produced it.

## Explicit non-goals

P5 does **not**:

- infer a responsibility from artifact fields;
- select or rank a Skill;
- select a capability from the registry;
- grant execution authority;
- decide whether evidence is semantically sufficient;
- create a semantic truth validator;
- automatically reopen deferred work;
- invent a new lifecycle persistence path;
- perform SkillOpt-style optimization;
- implement P6 capability routing.

The permanent boundary remains:

```text
warranted responsibility
!= available capability
!= authorized capability

Campaign Controller
!= semantic router
```

## Qualification expectations

A qualified P5 candidate must prove at least:

1. explicit `advance`, `defer`, and `close` commands exist;
2. `advance` persists exactly one agent-authored next responsibility and authority;
3. referenced evidence must satisfy the current evidence contract;
4. an orphan `artifacts/` file cannot support a decision;
5. `defer` preserves its reason and optional reopening contract, including `reopen_when: []`;
6. `close` persists the selected `TerminalState` and blocks later advance;
7. all decisions use P2 lifecycle recovery/reconstruction;
8. fresh-process status/history reconstruct the exact authored transition;
9. human/JSON surfaces expose exact replacement state and committed decision without emitting a semantic recommendation.
