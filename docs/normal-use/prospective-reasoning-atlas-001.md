# Prospective Reasoning — First Target-Repository Application (Atlas Midgard 001)

**Status:** normal-use evidence record, single session, same agent that built the capability. Not an independent trial.
**Date:** 2026-10-28
**Target:** `ThorStarlord/atlas-midgard`, `main@19a7c5a` → `main@d3cd47d` (PRs [#83](https://github.com/ThorStarlord/atlas-midgard/pull/83), [#84](https://github.com/ThorStarlord/atlas-midgard/pull/84)), explicitly authorized by the owner for this mission
**Sensemaking source:** `main@e581d01` (after [#637](https://github.com/ThorStarlord/sensemaking-skills/pull/637), [#638](https://github.com/ThorStarlord/sensemaking-skills/pull/638))

## 1. What ran

1. **Discovery** (portable `using-sensemaking`) read the product thesis, pillars, scale model, STATUS, the First Journey release cut, route scenes, verifiers and Chronos. It chose the product question: *how should completed Sagas visibly change the places the First Journey returns to?* It weighed visible co-op proxies (the standing Epoch V step), buildcraft (Scale B on HOLD) and the release gates (external) as candidates. No retained `poss:` or `arch:` records existed in Atlas.
2. **Architectural synthesis** (`docs/analysis/2026-10-28-world-memory-architectural-synthesis.md`) compared four options: scene-local wiring, a derived consequence catalog, a durable world-state authority (counterfactual) and restored scene variants. It typed eight consequences in `conditional_consequences` and recorded `REVISE_PREFERENCE` feedback.
3. **Strategic analysis** (`docs/analysis/2026-10-28-strategic-repository-analysis.md`, v2) passed the Strategicity Gate because the choice runs against the standing Epoch V frontier. It selected `BUILD` PATH-2/T1 and was the first to use `architecture_synthesis_refs`, `possibility_refs` and `architecture_option_refs`.
4. **Construction** (#84): `WorldConsequenceCatalog`, `WorldConsequenceSite`, six route sites and one smoke registered in both verifiers.
5. **Reconciliation**: realization, consequence assessments and as-built deviation recorded with history; records anchored to source files; Atlas session and query receipts.

## 2. Evidence levels

| Level | Status | Basis |
| --- | --- | --- |
| 1. Representation established | **Yes** | Both analyses pass `validate-output.py`; 21 Atlas claims and 24 relations pass `knowledge-proposal-check`; receipts valid |
| 2. Retrieval demonstrated | **Yes, same session** | `search`, `explain`, `impact` and `context-for` recover possibilities, options, consequences, premises, the governing decision and lessons (Atlas query receipt QY-2 to QY-11) |
| 3. Local decision usefulness observed | **Yes** | Section 3 |
| 4. Cross-session reuse observed | **No** | No later session has read these records |
| 5. Longitudinal product benefit established | **No** | The change has not run in Godot; no human has played the route |

## 3. The mission's questions

- **Did retained knowledge influence the options?** Not Sensemaking memory: Atlas had none. Atlas's own decisions did: Package 15's derived-presentation rule is why the durable world-state option was declined. The recall step found nothing, as it should for a first application.
- **Did the synthesis generate a materially different alternative?** Partly. The catalog was the natural option. The synthesis's distinct contributions were two. Asking what the scene-local option had already done exposed that it lost Package 15's markers (they sit in an unreachable scene, and the smoke runs in no verifier). And it kept the world-state authority as a named alternative with a concrete reopening trigger: a consequence of a non-History fact.
- **Did consequence depth change or strengthen the preference?** **It changed the design, three times.**
  - `conseq:chronos-anachronism`: Chronos reloads the Saga's own scene, so restoration sites must hide during reactivation. Without this, the reactivated past would have shown restored lanterns: a real defect, avoided before it was built.
  - `conseq:history-drift-detectable`: registering the smoke in both verifiers became part of the option.
  - `conseq:briefing-text-risk`: labels stay short in-world artifacts.
- **Were new ProductPossibilities discovered?** **No genuinely new one.** `poss:remembered-route-places` and `poss:companions-remark-on-remembered-places` restate Epoch VI candidates, recorded because the built structure realizes or enables them. Classification before retention (#637) applied: the declined responsibilities (co-op proxies, buildcraft, release hold) stayed construction paths in the strategic analysis and were not recorded as possibilities.
- **Did the reasoning improve the construction?** Yes. Chronos-aware sites, a Saga-keyed catalog that makes non-canonical History ids impossible, a smoke registered in both verifiers, and Package 15's texts moved onto the route. Building surfaced one improvement on the synthesis: keying by Saga ids prevents drift by construction, where the synthesis only expected to detect it.
- **Can a later agent reconstruct the decision?** Yes, from the two analyses, the records, the implementation receipt, STATUS and the receipts. One gap had to be fixed first (next item).
- **Were relationships impossible or misleading to retrieve?**
  - **`context-for` on the implementing source file returned nothing** (0 linked claims, 7 gaps). Prospective records were reachable by id, but not from the file a later editor would open. Existing v2 vocabulary fixed it: a `component` with `owned_paths`, a `decision`, a path-scoped `convention` rule and a `verification` record. The query then returned the decision, both options, the rule, the Chronos premise, both lessons and the smoke. No schema change was needed; the gap was in guidance, which now asks for this anchoring after construction.
  - `why` on an option is refused without a `decision`. That is correct: a preference is not a decision.
  - A synthesis cannot define an assumption inline; `assumption_refs` must name records. Here knowledge-edit authority existed, so they were recorded. In a read-only target they would be ids defined nowhere, which `--resolve-references` reports. This did not become consequential, so the schema is unchanged; it is a candidate if a read-only synthesis needs durable assumptions.
- **Did the memory add unnecessary complexity?** **Real overhead.**
  - About 250 lines of game code and scene edits came with two analyses (about 500 lines), 21 claims and 24 relations, and two receipts.
  - The records were generated by session-local scripts that are not in either repository, so later edits will be by hand.
  - It was justified here: a consequential, identity-defining choice, a first application, and three design changes from consequence depth. It would not be justified for routine work, which the loop already treats as optional.

## 4. Product-learning outcome

A later agent can see:

- **What was considered:** four options and three paths.
- **Why the catalog was preferred:** derived presentation, integrity, and Epoch VI reuse.
- **What it was expected to cause:** eight consequences, with premises and assumptions.
- **What was built and where it deviated:** Saga keys.
- **What remains uncertain:** runtime, feel, Epoch VI consumers, and the owner's scale reconciliation.

## 5. Limits

- **No Godot runtime.** Executing a downloaded engine was refused, and the hosted workflow is manual-only and refused dispatch. Verification was `gdparse` syntax checks, structural scene checks and `bash -n`. The owner's exact-head `verify.ps1` is the first runtime check, and the release export requires it.
- **Same agent, same session.** Classification, recall and anchoring were applied by the agent that wrote them. Independent use has not happened.
