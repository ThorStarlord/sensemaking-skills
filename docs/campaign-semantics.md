# Campaign semantics

This is the smallest durable vocabulary for an agent-led campaign. It is an
artifact contract, not a workflow interpreter or deterministic campaign engine.

## Control loop

`goal + repository state + authority → decision-changing uncertainty →
warranted responsibility → bounded capability → evidence → mechanical
validation → transition → reassessment`

The agent retains semantic control. Records make decisions reconstructible;
validators check structural integrity only.

## Vocabulary

- **Uncertainty** is decision-changing only when a credible answer changes a
  current decision or terminal condition. Resolved uncertainty does not
  reactivate automatically.
- **Responsibility** states why work exists. It requires a trigger, blocked
  decision, scope, authority, and explicit success or stop outcomes.
- **Authority** is separate from whether work is warranted and whether a
  capability is available. A correct result may be `owner_decision_required`.
- **Dependencies** are explicitly `task`, `evidence`, or `authority`.
- **Terminal states** include `goal_achieved`, `no_further_work_warranted`,
  `owner_decision_required`, `authority_boundary_reached`, `external_blocker`,
  `evidence_insufficient`, `invalid_execution`, and `deferred`.
- **Deferred responsibility** requires a reason and reopening condition; an
  external boundary records its owner, evidence, implication, and reopening
  condition.

## Artifacts and boundaries

`Campaign State` is the replaceable current snapshot. `Transition Record` is
append-only evidence of `state → evidence → decision → state`. `Campaign Policy`
describes permitted transitions and authority boundaries but does not select
one. `Campaign Handoff` contains current state, canonical references, allowed
next actions, and stop conditions. `Campaign Trace` records events for later
empirical analysis.

Workflows are bounded reusable subgraphs: they accept a responsibility and
produce an artifact/result. Completion returns control to the campaign agent;
it does not determine campaign completion.

The capability registry records accepted responsibility types, input/output
artifacts, mutation behavior, required authority, and availability (`available`,
`unavailable`, `external`, or `unknown`). It can enumerate candidates and reject
invalid executable references, but selection remains with the campaign agent;
no matching capability is a valid outcome.

The validator checks unique transition IDs, evidence references, chain
continuity, authority presence, one active responsibility, and no executable
work in terminal state. It does not judge reasoning or semantic sufficiency.

Central routing, an HTN executor, custom runtime, campaign database, semantic
truth validator, critic swarm, automatic voting, generic planner, and
self-modifying policy remain non-goals until empirical evidence warrants them.
# Campaign semantic contract boundary

Campaign artifacts are represented by the typed records in
`src/sensemaking_skills/campaign_semantics/models.py`. YAML is consumed through
the explicit loaders and emitted through the matching `dump_*` functions in
`campaign_semantics.io`; callers should not construct a second ad-hoc schema.

The contract boundary normalizes observed representation variants, including
historical campaign state snapshots, handoff state references, and enum values.
Round-trip qualification means semantic equality after load → dump → load, not
byte identity. Unknown decision-relevant fields and malformed known fields fail;
the observed `owner_routing` state metadata is retained explicitly.

Run the bounded drift gate with:

`PYTHONPATH=src python scripts/campaign-contract-roundtrip.py --m7r-root tests/fixtures/campaign-semantics/m7r`

The vendored fixtures under `tests/fixtures/campaign-semantics/m7r/` are a
minimal frozen representative campaign corpus used as read-only empirical
inputs. This boundary does not execute campaigns, grant authority, schedule
work, or decide semantic responsibility.
