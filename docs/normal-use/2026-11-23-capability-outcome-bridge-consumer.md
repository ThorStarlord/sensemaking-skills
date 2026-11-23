# Campaign capability-outcome bridge: required-capability route projection (2026-11-23)

**Status:** normal-use capability increment. **Source baseline:**
`7df3a7d05339dabc2eab2995a2e860d2dd5039de`. **Verified code revision:**
`9a4bda1e6bb52e13ccb77a80d3d77f915b0379e4`. **Capability:** a Campaign with
a bound capability outcome can project a compact construction bridge that joins
the durable binding to the selected possibility's explicitly declared
required-capability routes at one committed revision, without manually
cross-referencing Campaign state with a separate `semantic workspace-query`.

This is one consumer increment, not completion of the whole construction-bridge
capability, independent later-agent use, decision benefit or implementation
verification.

## 1. Resumed Campaign context

The Campaign `bridge-continuity-probe` resumed from durable state with:

- possibility `poss:goal-family-construction-bridge`;
- desired behavior: reconstruct a selected opportunity's desired behavior,
  source evidence, assumptions, counterevidence, required capabilities and
  remaining realization conditions from Campaign state, then choose and continue
  a capability-advancing increment without re-running opportunity discovery;
- completion condition: a fresh agent resumes, identifies the bound possibility
  and realization conditions, distinguishes implemented components from
  unresolved requirements, selects the next increment using the routes, and
  carries the same outcome into the following transition;
- realization `not_established`; `epistemic_status: selected_hypothesis`;
- four required capabilities (`cap:adaptive-metareasoning`,
  `cap:breadth-exploration-guidance`, `cap:experience-lesson-recall`,
  `cap:repository-only-discovery`);
- assumptions, counterevidence and five remaining realization conditions.

The Campaign had no bound target (`targets: []`, `target_ref: null`). The
knowledge source therefore had to be named explicitly, not derived from target
identity. The binding was agent-authored; it did not verify the opportunity.

## 2. Route result and its effect on the increment

The existing consumer at the source baseline returned the four declared routes
and five reviewed components:

| Capability | Reviewed components |
| --- | --- |
| `cap:adaptive-metareasoning` | `component:using-sensemaking-skill` |
| `cap:breadth-exploration-guidance` | `component:strategic-repository-analysis-skill` |
| `cap:experience-lesson-recall` | `component:knowledge-store`, `component:semantic-knowledge-plane` |
| `cap:repository-only-discovery` | `component:using-sensemaking-skill` |

Every component carried `implementation_verified: false`. The route is an
authored, documentary join; the source scope is tracked authored knowledge, not
component code inspection.

Effect on the decision:

- The routes ruled out treating a named capability as wholly missing: each
  already had at least one explicitly reviewed component.
- They did **not** establish that any component implements its capability, is
  sufficient or is currently working.
- The remaining gap was the absence of a single projection joining the durable
  Campaign binding to those routes and mechanically checking that the
  Campaign's capability IDs and the repository's declared `requires_capability`
  edges still agree.
- Therefore a further read-only consumer increment was warranted. A separate
  durable bridge file was not: it would duplicate the binding, create a second
  truth surface and go stale between authored knowledge changes.

## 3. Increment

`campaign capability-outcome bridge` projects the bridge from two existing
sources:

- the Campaign's durable `extensions.capability_outcome` record, including the
  assumptions, counterevidence and remaining conditions;
- the selected possibility's exact-revision `possibility-ecology` projection,
  including `required_capability_routes` and their reviewed components.

The command:

- refuses an unbound Campaign and a bound claim that is not an opportunity;
- reuses the existing zero-setup `workspace-query` index and records the exact
  indexed commit;
- verifies checkout identity against a bound Campaign target when one exists,
  and reports `NOT_ASSESSED` when the Campaign has no target;
- reports mechanical `ALIGNED`, `MISMATCHED` or `NOT_ASSESSED` capability-set
  alignment, plus `campaign_only`, `knowledge_only` and truncation counts;
- reports documentary source-reference overlap between the binding and the
  indexed possibility;
- keeps `implementation_verified`, `semantic_truth_established`,
  `action_authorized`, `selection_performed` and `recommendation_performed`
  false;
- does not rank routes, select an increment, generate a plan or declare
  readiness.

## 4. End-to-end demonstration

1. **Initial task:** resume the Campaign and choose the next bounded increment
   for the selected goal-family construction bridge.
2. **Recovery:** `campaign working-context` and `campaign resume-profile`
   returned the bound possibility, desired behavior, assumptions,
   counterevidence, four required capabilities and five remaining conditions
   without re-running opportunity discovery.
3. **Observed limitation:** the Campaign carried capability IDs while the
   routes lived in a separate `semantic workspace-query` payload; joining them
   required a manual four-ID cross-reference, and nothing checked that the two
   capability sets still agreed.
4. **Route result:** all four capabilities had declared components, so the
   next increment was the join, not a duplicate capability component.
5. **Change:** the read-only `campaign capability-outcome bridge` projection.
6. **Consumer:** real CLI at `9a4bda1e6bb52e13ccb77a80d3d77f915b0379e4` with
   `--repo . --ref HEAD` returned four routes, five components,
   `route_alignment: ALIGNED`, `source_alignment: MATCH`, a clean checkout and
   the caveats `TARGET_NOT_BOUND`, `DOCUMENTARY_ROUTES` and
   `INSPECT_ORIGINAL_SOURCE`.
7. **Negative paths (real CLI, not a synthetic test suite):**
   - no bound outcome -> `CAMPAIGN_WORKSPACE_ERROR`, exit 4;
   - an extra Campaign capability -> `MISMATCHED` with `campaign_only` and
     `ROUTE_ALIGNMENT_MISMATCH`;
   - a declared capability with no component edge ->
     `implementation_link_not_assessed: true`, empty components and an honest
     absence report;
   - a target-bound Campaign -> `target_binding: MATCH`.

## 5. Claim ceiling

| Level | Status |
| --- | --- |
| Bound outcome and declared routes visible through one consumer | Observed through the real CLI |
| Campaign/knowledge capability-set alignment | Observed mechanically |
| Reviewed component identity, authority and owned paths | Observed as authored records |
| Source-reference overlap | Observed as a documentary join |
| Component implementation or a working consumer | NOT ESTABLISHED |
| Capability sufficiency, applicability or readiness | NOT ESTABLISHED |
| Independent later-agent use of the bridge | NOT ESTABLISHED |
| Decision benefit or comparative benefit | NOT ESTABLISHED |
| Completion of the whole construction-bridge capability | NOT ESTABLISHED |

The bridge is a projection. `implementation_verified` remains false and the
route does not inspect code. A shared source path is not proof that the binding
is correct. Alignment is not a recommendation.

## 6. Continuation

Campaign transition `TR-AUTO-0004` records that the route evidence changed the
next increment from duplicating a named capability to joining the existing
binding and routes, that a separate durable bridge record was not warranted,
and that the bridge was exercised once. It sets `R-AUTO-0003`: use the bridge
in a fresh continuation and record whether it reduces reconstruction versus the
separate Campaign and knowledge reads, without treating it as implementation
proof or readiness.

The bound capability remains unestablished. Its remaining conditions still
include observed redundancy against existing Campaign/strategy/handoff context,
independent later-agent use, and the prohibition on adding an automatic
planner, ranker, generator or readiness verdict.
