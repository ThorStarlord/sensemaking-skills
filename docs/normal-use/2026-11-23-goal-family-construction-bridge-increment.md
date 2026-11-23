# Goal-family construction bridge: required-capability routes (2026-11-23)

**Status:** normal-use capability increment. **Source baseline:**
`32925b69c460c245699b6657945c374eeb96d7cd`. **Verified code revision:**
`4fe5a2aa5da407df8668235c02352ed57b3972be`. **Capability:** when an agent
selects one possibility from a goal family, `possibility-ecology` exposes the
capabilities that possibility explicitly requires and each capability's
explicitly reviewed component route, so the agent can reconstruct a compact
construction bridge without a separate goal-scoped outline lookup. This is a
partial consumer increment, not the whole bridge, independent later-agent use,
decision influence or comparative benefit.

## 1. Resumed Campaign context

A resumed Campaign asked for the next coherent increment of a goal-family
construction bridge: preserve a selected opportunity's desired behaviour,
source evidence, assumptions and remaining realization conditions across
increments. The Campaign state named the capability but carried no evidence
refs. The capability was recovered from the repository:

- `poss:goal-family-construction-bridge` in
  `.sensemaking/knowledge/possibility-synthesis.json`;
- its synthesis episode
  `artifacts/history/2026-11-23-goal-family-construction-bridge-synthesis.json`;
- the prior capability record
  `docs/normal-use/2026-11-23-prospective-synthesis-capability.md`.

That record said the synthesized bridge was `HYPOTHETICAL`, had no independent
use, and should be exercised in one authentic construction trajectory before
more machinery was added.

## 2. Observed gap in the authentic trajectory

Inspecting the real candidate with the existing consumer at the source
baseline:

```bash
sensemaking-skills semantic workspace-query \
  --operation possibility-ecology \
  --subject poss:goal-family-construction-bridge --json
```

returned all four `requires_capability` relations in the record's
`relationship_total`, but only one appeared in `relationships`; the other three
fell outside the eight-relationship bound. No implementation component was
shown at all. `product-outline` exposes implementation routes per goal, not per
selected possibility, so reconstructing the candidate's required capabilities
and their reviewed components needed a manual cross-reference and was easy to
under-read.

The missing slice was therefore not a new planner, ranking or selection
surface. It was a source-grounded join between two explicit authored links:
`opportunity --requires_capability--> capability --implemented_by--> component`.

## 3. Increment

`possibility-ecology` now adds `required_capability_routes` when the subject is
an opportunity. Each route carries:

- the capability claim, statement, epistemic status, authority and source;
- the exact `requires_capability` relation and its evidence;
- up to four explicitly reviewed `implemented_by` components, each with its
  statement, authority, source, evidence, authored `owned_paths` and
  `implementation_verified: false`;
- component totals and omission counts, with
  `implementation_link_not_assessed: true` when no component edge exists.

The section is bounded at eight required capabilities. Goal focus is unchanged
and does not carry the section. Missing links remain `NOT_ASSESSED`; no
capability, component or route is inferred.

At the verified code revision the real candidate returned all four required
capabilities and five reviewed components:

| Capability | Reviewed components |
| --- | --- |
| `cap:adaptive-metareasoning` | `component:using-sensemaking-skill` |
| `cap:breadth-exploration-guidance` | `component:strategic-repository-analysis-skill` |
| `cap:experience-lesson-recall` | `component:knowledge-store`, `component:semantic-knowledge-plane` |
| `cap:repository-only-discovery` | `component:using-sensemaking-skill` |

A second opportunity with no explicit component edge
(`poss:assumption-aware-opportunity-ecology` -> `cap:possibility-records`)
returned `implementation_link_not_assessed: true`, not an inferred route.

## 4. End-to-end demonstration

1. **Initial task:** resume the Campaign and choose a bounded increment for the
   selected goal-family construction bridge.
2. **Recovery:** reconstruct the selected possibility, its assumptions,
   source candidates, required capabilities and remaining realization
   conditions from reviewed repository records.
3. **Observed limitation:** the selected candidate's ecology showed only one of
   four required capabilities; component routes required a separate goal-scoped
   query.
4. **Change:** the opportunity focus now joins explicit `requires_capability`
   and `implemented_by` edges in the same bounded projection.
5. **Consumer:** real `workspace-query --operation possibility-ecology` at
   `4fe5a2aa5da407df8668235c02352ed57b3972be`.
6. **What was not previously possible:** see the selected candidate's complete
   set of explicitly required capabilities and reviewed components without
   crossing into a separate goal outline or losing links to the relationship
   bound.

## 5. Evidence ceiling

| Level | Status |
| --- | --- |
| Source-grounded join of explicit edges | Observed through the real CLI |
| Selected candidate's four required capabilities visible together | Observed |
| Reviewed component identity and owned paths visible | Observed; not code-inspected |
| Working consumer or implementation correctness | NOT ESTABLISHED |
| Durable Campaign binding of the selected possibility | NOT IMPLEMENTED |
| Independent later-agent use of the bridge | Not established |
| Decision influence or comparative benefit | Not established |

The route is documentary. It does not prove that a capability is sufficient,
that a component implements it correctly, that an increment is ready, or that
the selected possibility should be built. `implementation_verified` stays
`false`.

## 6. Continuation

The next warranted responsibility is to use the route in an actual bounded
construction decision and record whether it changes the chosen increment or
reduces reconstruction. A durable Campaign-bound bridge record is still
unimplemented; it should be added only if the authentic trajectory shows that
the existing Campaign state plus this ecology projection is insufficient. No
automatic planner, ranker, generator or readiness verdict is warranted.
