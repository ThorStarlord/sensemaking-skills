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
  `evidence_insufficient`, `invalid_execution`, `deferred`, and
  `qualified_pr_ready`.
- **Deferred responsibility** requires a responsibility id and a reason; a
  reopening condition is optional. An external boundary requires its id,
  capability, owner, ownership flag, accessibility, and implication; evidence
  and a reopening condition are optional.

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
byte identity.

Strictness is uniform. Every loader — `load_campaign_state`,
`load_transition_record`, `load_campaign_policy`, `load_campaign_trace`,
`load_campaign_handoff`, `load_responsibility` — and every nested
decision-relevant record (responsibility, uncertainty, dependency, deferred
responsibility, external boundary) rejects unknown fields with `ContractError`
rather than dropping them. The canonical post-migration contract requires
`schema_version` to be `"2"`; historical v1 representations are accepted only
through the explicit one-way migration registry and are normalized in memory to
v2, while unknown future versions fail closed. Missing or malformed known fields
raise `ContractError` rather than a bare `KeyError` or `TypeError`. The only
sanctioned extension is `owner_routing` on a campaign state, retained under
`extensions`. A `Campaign Handoff`'s `campaign_id` must equal the `campaign_id`
of its resolved current state. Campaign trace events and campaign policy
`known_transitions` entries are deliberately opaque maps.

Run the bounded drift gate with:

`PYTHONPATH=src python scripts/campaign-contract-roundtrip.py --m7r-root tests/fixtures/campaign-semantics/m7r`

It round-trips the vendored historical corpus and every shipped template
(`campaign-state`, `transition-record`, `campaign-policy`, `campaign-handoff`)
through its production loader. The vendored fixtures under
`tests/fixtures/campaign-semantics/m7r/` are a minimal frozen representative
campaign corpus used as read-only empirical inputs. This boundary does not
execute campaigns, grant authority, schedule work, or decide semantic
responsibility.
