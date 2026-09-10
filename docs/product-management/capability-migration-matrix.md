# Product Management capability migration matrix

**Upstream authority:** `lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349`  
**Disposition vocabulary:** `ADAPT` means the capability is selected for Sensemaking adaptation; `MERGE` means useful upstream methodology is incorporated into an existing canonical capability rather than creating duplicate authority; `DEFER` means provenance is preserved but implementation is not yet authorized.  
**Maturity vocabulary:** `CANDIDATE`, `REPOSITORY_QUALIFIED`, `NATIVE_HARNESS_QUALIFIED`, `PORTABILITY_QUALIFIED`, `PROMOTED`.

The historical Wayfinder PM registry is not execution authority. A historical entry is recorded only to avoid accidentally recreating or contradicting an old identity.

Native-harness dogfood is a **promotion/support-claim gate**, not a blanket implementation-expansion gate. Repository-qualified capabilities may accumulate while empirical qualification remains visible debt.

| Upstream command | Historical Sensemaking identity | Candidate artifact | PM responsibility | Disposition | Wave | Maturity | Native | Portability | Notes |
|---|---|---|---|---|---:|---|---|---|---|
| persona | deprecated `persona` | `persona_definition` | `customer_understanding` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Persona confidence must reflect evidence strength. |
| discovery | deprecated `discovery` | `discovery_findings` | `problem_discovery` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Analyzing evidence is distinct from conducting research. |
| interview-synthesis | deprecated `interview-synthesis` | `synthesis_report` | `research_synthesis` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Material findings trace to supplied source evidence. |
| opportunity-tree | deprecated `opportunity-tree` | `opportunity_map` | `opportunity_mapping` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Opportunities without evidence remain assumptions. |
| hypothesis | deprecated `hypothesis` | `hypothesis_statement` | `product_hypothesis` | ADAPT | 1 | REPOSITORY_QUALIFIED | pending | pending | Must be falsifiable and evidence-aware. |
| prd | deprecated `prd` plus current `to-prd` adjacent capability | `prd` | `product_specification` | MERGE | 2 | REPOSITORY_QUALIFIED | pending | pending | Upstream PRD methodology merged into canonical `to-prd`; no duplicate `prd` Skill authority. |
| user-stories | deprecated `user-stories` | `story_list` | `delivery_specification` | ADAPT | 2 | REPOSITORY_QUALIFIED | pending | pending | Agent-agnostic story decomposition with traceability and no invented estimates. |
| acceptance-criteria | deprecated `acceptance-criteria` | `criteria_list` | `delivery_specification` | ADAPT | 2 | REPOSITORY_QUALIFIED | pending | pending | Specified behavior is distinct from executed/passing tests. |
| pre-mortem | deprecated `pre-mortem` | `risk_analysis` | `risk_and_readiness` | ADAPT | 2 | REPOSITORY_QUALIFIED | pending | pending | Hypothetical failure modes remain distinct from observed risks and launch authority. |
| competitive-analysis | deprecated `competitive-analysis` | `market_analysis` | `market_understanding` | DEFER | 3 | CANDIDATE | pending | pending | Requires source-currency rules for market evidence. |
| strategy | no current implementation; no authoritative live PM counterpart | `strategy_doc` | `product_strategy` | DEFER | 3 | CANDIDATE | pending | pending | Design against current Campaign semantics rather than legacy command shape. |
| prioritize | deprecated `prioritize` | `prioritized_list` | `prioritization` | DEFER | 3 | CANDIDATE | pending | pending | Ranking remains model judgment; formulas may be deterministic inputs only. |
| north-star | deprecated `north-star` | `north_star_metric` | `product_strategy` | DEFER | 3 | CANDIDATE | pending | pending | Metric choice is semantic. |
| okr | deprecated `okr` | `okr_list` | `product_strategy` | DEFER | 3 | CANDIDATE | pending | pending | Measurability can be validated; quality cannot. |
| roadmap | deprecated `roadmap` | `roadmap` | `product_strategy` | DEFER | 3 | CANDIDATE | pending | pending | Sequence should trace to decisions/evidence. |
| lean-canvas | deprecated `lean-canvas` | `business_canvas` | `product_strategy` | DEFER | 3 | CANDIDATE | pending | pending | Assumption-heavy artifact; preserve hypothesis labels. |
| experiment-design | deprecated `experiment-design` | `experiment_plan` | `experimentation` | DEFER | 4 | CANDIDATE | pending | pending | Design is not experiment evidence. |
| ab-test-analysis | deprecated `ab-test-analysis` | `test_results` | `experimentation` | DEFER | 4 | CANDIDATE | pending | pending | Requires actual observation/statistical inputs. |
| measure-pmf | deprecated `measure-pmf` | `pmf_report` | `product_measurement` | DEFER | 4 | CANDIDATE | pending | pending | No survey evidence means no measured-PMF claim. |
| pricing | deprecated `pricing` | `pricing_model` | `commercial_strategy` | DEFER | 4 | CANDIDATE | pending | pending | Price recommendation is not authorization to change price. |
| customer-journey | deprecated `customer-journey` | `journey_map` | `customer_understanding` | DEFER | 5 | CANDIDATE | pending | pending | Candidate customer-modeling wave. |
| ideal-customer-profile | no authoritative live PM counterpart | `ideal_customer_profile` | `customer_understanding` | DEFER | 5 | CANDIDATE | pending | pending | Treat as new current-domain design if authorized. |
| launch-checklist | deprecated `launch-checklist` | `readiness_report` | `risk_and_readiness` | DEFER | 6 | CANDIDATE | pending | pending | Checklist completion is not external launch authorization. |
| gtm | deprecated `gtm` | `gtm_plan` | `commercial_strategy` | DEFER | 6 | CANDIDATE | pending | pending | External execution remains separately authorized. |
| battlecard | deprecated `battlecard` | `battlecard` | `commercial_strategy` | DEFER | 6 | CANDIDATE | pending | pending | Claims need source-currency/evidence discipline. |
| release-notes | deprecated `release-notes` | `feature_announcement` | `communication` | DEFER | 6 | CANDIDATE | pending | pending | Drafting may be automated; publication is external action. |
| stakeholder-update | deprecated `stakeholder-update` | `stakeholder_update` | `communication` | DEFER | 6 | CANDIDATE | pending | pending | Should cite durable Campaign state when used in Campaign context. |

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
11. Do not assign stronger support/promotion claims than the preserved evidence warrants.

Rows marked `REPOSITORY_QUALIFIED` in an open candidate PR become authoritative only if that exact candidate head passes the required repository CI and is merged. A wave number is sequencing guidance, not semantic routing authority. Separate user/program authorization may advance a wave before native-harness qualification, but empirical qualification remains required for the stronger claim states.