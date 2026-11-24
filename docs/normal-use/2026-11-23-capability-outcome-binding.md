# Campaign capability-outcome binding and construction bridge (2026-11-23)

**Status:** normal-use capability increment and two fresh-continuation probes.
**Source baseline:** `32925b69c460c245699b6657945c374eeb96d7cd`. **Binding
revision:** `7df3a7d05339dabc2eab2995a2e860d2dd5039de`. **Integrated bridge
revision:** `b9d9593d4fa8636a85e607d52d9ad4a7aca11f24`.

This record covers the durable Campaign binding of
`poss:goal-family-construction-bridge`, the route consumer delivered in
`docs/normal-use/2026-11-23-goal-family-construction-bridge-increment.md`, and
the joined consumer delivered in
`docs/normal-use/2026-11-23-capability-outcome-bridge-consumer.md`. It does not
duplicate those records. The bound opportunity remains `HYPOTHETICAL` and its
realization remains `not_established`.

## 1. Observed continuity gap

Before the binding, a resumed Campaign preserved:

- the mission;
- the active responsibility and its decision blocked;
- authority, scope and success conditions;
- execution companions and transition history.

It did not preserve, in Campaign state:

- the selected opportunity claim ID;
- the desired intellectual behavior;
- the observable completion condition;
- the assumptions and counterevidence that materially affected continuation;
- the required capability claims;
- the remaining realization conditions.

A prior fresh worker recovered the possibility from
`.sensemaking/knowledge/possibility-synthesis.json`, but only by searching the
repository. The Campaign mission named the capability while the selected claim,
its assumptions and its conditions lived elsewhere. Campaign evidence admission
also refused repository files and commits, so textual source references could
not become admitted Campaign evidence without a separate artifact and
admission path.

That is a real declared-state gap, not a knowledge-availability gap: the
repository could answer the question, but the Campaign could not state what it
had selected.

## 2. Binding

`campaign capability-outcome bind` records one agent-selected opportunity as
the Campaign's governing capability outcome. It stores the record under
`extensions.capability_outcome` and commits it as a lifecycle transition that
preserves the active responsibility.

The record carries:

- `possibility_id`, `desired_behavior` and `completion_condition`;
- `selection_basis`, including the alternatives considered;
- `source_refs` (references, not admitted Campaign evidence);
- `assumptions` and `counterevidence`;
- `required_capabilities` (IDs, never inferred);
- `remaining_conditions`;
- fixed claim-ceiling fields: `epistemic_status: selected_hypothesis` and
  `realization: not_established`.

The binding is immutable per Campaign. A different governing outcome requires a
new Campaign; the old Campaign remains the durable record of the previous
commitment. This is deliberate: silently rewriting the governing outcome would
destroy the continuity the binding exists to provide.

`campaign working-context` and `resume-profile` project the record. The working
profile returns the full record; the minimal profile returns identity, desired
behavior, completion condition, epistemic status, realization and counts.

## 3. Fresh continuation 1: recover and build the join

A fresh worker resumed `bridge-continuity-probe` at
`responsibility_active_R-AUTO-0002` with no hint about the selected claim. It
recovered from Campaign state:

- possibility `poss:goal-family-construction-bridge`;
- desired behavior and completion condition;
- four assumptions and two counterevidence items;
- four required capabilities;
- five remaining realization conditions.

It then ran the real `possibility-ecology` route consumer and observed four
declared capability routes and five reviewed components, every one with
`implementation_verified: false`. The routes ruled out treating a named
capability as wholly unmapped and did not establish implementation or
readiness.

The worker selected a read-only consumer that joins the Campaign binding to the
declared routes and mechanically checks capability-set alignment and
source-reference overlap. That increment is recorded separately in
`docs/normal-use/2026-11-23-capability-outcome-bridge-consumer.md`. The worker
did not create a second durable bridge record; that would have duplicated the
binding and gone stale.

This continuation establishes that the binding is recoverable and usable
without re-running opportunity discovery. It does not establish that the
selected increment was the only or best one.

## 4. Fresh continuation 2: compare the joined consumer

A second fresh worker resumed at `responsibility_active_R-AUTO-0003`, whose
durable statement required it to compare the joined consumer with separate
Campaign and knowledge reads and record whether reconstruction was reduced.

The comparison:

| Path | Route payload | Navigation calls | Route-command wall time |
| --- | ---: | ---: | ---: |
| Separate Campaign + `possibility-ecology` | 96,584 chars | 3 | 2.28 s |
| Joined `capability-outcome bridge` | 23,901 chars | 0 | 4.35 s |

The joined consumer was 4.04x smaller for the route join and removed three
navigation calls. It also supplied mechanical `route_alignment: ALIGNED` with
empty `campaign_only` and `knowledge_only` sets, `source_alignment: MATCH`, a
named `TARGET_NOT_BOUND` provenance hazard, and `route_truncated: false`. The
separate ecology payload had `truncated: true`, `coverage_complete: false` and
three omitted relationships; only a deliberate check of
`required_capability_omitted` showed the required routes themselves were
complete.

The joined consumer was slower by about 2.07 s and re-sent the
`capability_outcome` record already present in `working-context`. It does not
substitute for the full ecology when reconsidering sibling candidates or
omitted relationships.

Effect on the decision:

- The bridge mechanically ruled out "repair Campaign/knowledge drift".
- It named repository anchoring as a hazard.
- It did not change the direction of the next increment.
- The governing outcome came from Campaign state, not from the bridge.

Honest judgment: the joined consumer is useful for one bounded join step and
not redundant, but it is not capability-advancing on its own. The worker made
`NO_CODE_CHANGE` and deferred `R-AUTO-0003` through `TR-AUTO-0005`, with
reopen conditions limited to a concrete continuation failure or a real
increment that needs routes the bridge cannot supply. It explicitly excluded
profile flags, limit flags, rankers, planners and readiness verdicts from
reopening the responsibility.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Bound outcome survives Campaign transitions | Observed through real CLI and `campaign validate` |
| Fresh agent recovers the bound outcome without re-discovery | Observed once |
| Declared capability routes and reviewed components visible | Observed through the real consumer |
| Campaign/knowledge capability-set alignment | Observed mechanically |
| Joined consumer reduces route payload and navigation | Observed once; one comparison, no blinding |
| Joined consumer changes decision quality | NOT ESTABLISHED |
| Declared component implements its capability | NOT ESTABLISHED; `implementation_verified` is false |
| Capability sufficiency, applicability or readiness | NOT ESTABLISHED |
| Independent later-agent reuse | NOT ESTABLISHED; both continuations were within this mission |
| Comparative or longitudinal cognitive benefit | NOT ESTABLISHED |

The two fresh continuations are authentic use, not independent cognitive
qualification. The second worker knew the joined consumer existed before
comparing the paths, so its result measures payload, steps and artifacts, not
decision quality. One Campaign, one repository and one revision cannot support a
general claim about Sensemaking's cognitive development.

## 6. Revision note

`TR-AUTO-0004` cites worker-branch commits `9a4bda1e` and `28ca49ee`, which are
not ancestors of the integrated branch. They were cherry-picked as `5e3a783a`
and `b9d9593d`; patch-ids match and the content is the same. The Campaign
transition is immutable, so this record supplies the mapping for later agents.
This is a free-form transition-text limitation, not a bridge defect. A future
binding or bridge increment that must survive hash rewriting should cite the
integrated revision rather than a worker-branch hash.

## 7. Continuation

The bounded continuity vertical is operational:

- a Campaign can declare its selected outcome, source references, assumptions,
  counterevidence, required capabilities and remaining conditions;
- the declaration survives ordinary advances and is projected by the normal
  consumers;
- a fresh agent can recover it without re-running discovery;
- the joined consumer can project the declared routes and mechanically report
  drift, truncation and provenance limits.

The broader synthesized opportunity remains partially realized. Still
unresolved:

- strategy-context binding beyond the Campaign mission and source references;
- structured alternative construction paths (currently prose in
  `selection_basis`);
- implementation evidence for the declared components;
- independent later-agent reuse and comparative benefit;
- longitudinal development.

No further construction is warranted now. The next warranted responsibilities
are independent qualification and evidence, which remain separate from this
capability increment. The Campaign remains open and deferred, not closed, with
the bound outcome and its five remaining conditions intact.

## Addendum 2026-11-24

The following mission established a durable copy of the Campaign at
`H:\codex\campaigns\smk-bridge-continuity-probe` and added append-only,
evidence-linked realization assessments alongside the immutable binding. The
original conditions are unchanged; the latest assessments distinguish evidence
present, partial evidence and unassessed conditions without claiming
completion. A fresh continuation also added binding source-evidence resolution
and reconciled the stale reviewed realization to `PARTIALLY_IMPLEMENTED` while
preserving the original `HYPOTHETICAL` basis. See
[`2026-11-24-realization-continuity.md`](2026-11-24-realization-continuity.md)
and
[`2026-11-24-construction-bridge-evidence-continuation.md`](2026-11-24-construction-bridge-evidence-continuation.md).
The binding remains `realization: not_established`; the Campaign remains
deferred, and independent use and component implementation evidence remain
open.
