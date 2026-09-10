# Product Management capability migration matrix

**Upstream authority:** `lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349`  
**Disposition vocabulary:** `ADAPT` means the capability is selected for Sensemaking adaptation; `MERGE` means useful upstream methodology is incorporated into an existing canonical capability rather than creating duplicate authority; `DEFER` means provenance is preserved but implementation is not yet authorized.  
**Maturity vocabulary:** `CANDIDATE`, `REPOSITORY_QUALIFIED`, `NATIVE_HARNESS_QUALIFIED`, `PORTABILITY_QUALIFIED`, `PROMOTED`.

The historical Wayfinder PM registry is not execution authority. Native-harness dogfood is a promotion/support-claim gate, not a blanket implementation-expansion gate.

| Upstream command | Historical Sensemaking identity | Candidate artifact | PM responsibility | Disposition | Wave | Maturity | Native | Portability | Notes |
|---|---|---|---|---|---:|---|---|---|---|
| persona | deprecated `persona` | `persona_definition` | `customer_understanding` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Persona confidence reflects evidence strength. |
| discovery | deprecated `discovery` | `discovery_findings` | `problem_discovery` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Analysis is distinct from conducting research. |
| interview-synthesis | deprecated `interview-synthesis` | `synthesis_report` | `research_synthesis` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Findings trace to supplied source evidence. |
| opportunity-tree | deprecated `opportunity-tree` | `opportunity_map` | `opportunity_mapping` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Unsupported opportunities remain assumptions. |
| hypothesis | deprecated `hypothesis` | `hypothesis_statement` | `product_hypothesis` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Falsifiable and evidence-aware. |
| prd | deprecated `prd` plus current `to-prd` | `prd` | `product_specification` | MERGE | 2 | REPOSITORY_QUALIFIED | pending | pending | Upstream methodology merged into canonical `to-prd`. |
| user-stories | deprecated `user-stories` | `story_list` | `delivery_specification` | ADAPT | 2 | REPOSITORY_QUALIFIED | pending | pending | Traceable; no invented estimates. |
| acceptance-criteria | deprecated `acceptance-criteria` | `criteria_list` | `delivery_specification` | ADAPT | 2 | REPOSITORY_QUALIFIED | pending | pending | Specification is distinct from test execution. |
| pre-mortem | deprecated `pre-mortem` | `risk_analysis` | `risk_and_readiness` | ADAPT | 2 | REPOSITORY_QUALIFIED | pending | pending | Hypothetical risks remain distinct from incidents/launch authority. |
| competitive-analysis | deprecated `competitive-analysis` | `market_analysis` | `market_understanding` | ADAPT | 3 | REPOSITORY_QUALIFIED | pending | pending | Observed competitor claims require source evidence/cutoff. |
| strategy | no authoritative live PM counterpart | `strategy_doc` | `product_strategy` | ADAPT | 3 | REPOSITORY_QUALIFIED | pending | pending | New current-domain contract; generated strategy remains proposed. |
| prioritize | deprecated `prioritize` | `prioritized_list` | `prioritization` | ADAPT | 3 | REPOSITORY_QUALIFIED | pending | pending | RICE arithmetic is checked; semantic ranking remains agent-owned. |
| north-star | deprecated `north-star` | `north_star_metric` | `product_strategy` | ADAPT | 3 | REPOSITORY_QUALIFIED | pending | pending | Candidate scoring is heuristic; selected metric remains proposed. |
| okr | deprecated `okr` | `okr_list` | `product_strategy` | ADAPT | 3 | REPOSITORY_QUALIFIED | pending | pending | Outcome-shaped KRs; no fabricated progress or baseline. |
| roadmap | deprecated `roadmap` | `roadmap` | `product_strategy` | ADAPT | 3 | REPOSITORY_QUALIFIED | pending | pending | Committed timing requires explicit authority evidence. |
| lean-canvas | deprecated `lean-canvas` | `business_canvas` | `product_strategy` | ADAPT | 3 | REPOSITORY_QUALIFIED | pending | pending | Canvas is explicitly a hypothesis map. |
| experiment-design | deprecated `experiment-design` | `experiment_plan` | `experimentation` | ADAPT | 4 | REPOSITORY_QUALIFIED | pending | pending | Designed plans cannot encode results or imply external execution. |
| ab-test-analysis | deprecated `ab-test-analysis` | `test_results` | `experimentation` | ADAPT | 4 | REPOSITORY_QUALIFIED | pending | pending | Analyzed conclusions require actual observation evidence; otherwise insufficient. |
| measure-pmf | deprecated `measure-pmf` | `pmf_report` | `product_measurement` | ADAPT | 4 | REPOSITORY_QUALIFIED | pending | pending | Measured PMF requires empirical evidence; framework thresholds are heuristics. |
| pricing | deprecated `pricing` | `pricing_model` | `commercial_strategy` | ADAPT | 4 | REPOSITORY_QUALIFIED | pending | pending | Pricing remains proposed; observed prices/economics require evidence and no price-change authority is granted. |
| customer-journey | deprecated `customer-journey` | `journey_map` | `customer_understanding` | ADAPT | 5 | REPOSITORY_QUALIFIED | pending | pending | Bounded stage model; observed journey, emotion, metric, and critical-moment claims require evidence/currentness. |
| ideal-customer-profile | no authoritative live PM counterpart | `ideal_customer_profile` | `customer_understanding` | ADAPT | 5 | REPOSITORY_QUALIFIED | pending | pending | New current-domain evidence-aware ICP; customer-fit and numeric claims remain provisional without evidence. |
| launch-checklist | deprecated `launch-checklist` | `readiness_report` | `risk_and_readiness` | DEFER | 6 | CANDIDATE | pending | pending | Checklist completion is not launch authorization. |
| gtm | deprecated `gtm` | `gtm_plan` | `commercial_strategy` | DEFER | 6 | CANDIDATE | pending | pending | External execution remains separately authorized. |
| battlecard | deprecated `battlecard` | `battlecard` | `commercial_strategy` | DEFER | 6 | CANDIDATE | pending | pending | Claims need current source evidence. |
| release-notes | deprecated `release-notes` | `feature_announcement` | `communication` | DEFER | 6 | CANDIDATE | pending | pending | Drafting may be automated; publication is external action. |
| stakeholder-update | deprecated `stakeholder-update` | `stakeholder_update` | `communication` | DEFER | 6 | CANDIDATE | pending | pending | Campaign state should be cited when available. |

## Migration rule

For every capability that moves from `DEFER` to implementation:

1. Re-read the exact pinned upstream source.
2. Reconcile historical/current Sensemaking counterparts.
3. Confirm its PM responsibility and evidence requirements.
4. Remove harness-specific semantics.
5. Define or reconcile the output contract.
6. Add positive and rejection validation where mechanically warranted.
7. Register it in the current Campaign capability catalog, not the deprecated router.
8. Prove Campaign admission and handoff behavior where applicable.
9. Require exact-head repository CI before assigning `REPOSITORY_QUALIFIED` on the merged branch.
10. Track native-harness and portability validation as explicit qualification debt until performed.
11. Do not assign stronger support/promotion claims than preserved evidence warrants.

Rows marked `REPOSITORY_QUALIFIED` in an open candidate PR become authoritative only if that exact candidate head passes required repository CI and is merged. Wave numbers are sequencing guidance, not semantic routing authority.
