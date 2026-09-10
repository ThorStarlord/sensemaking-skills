# Product Management capability migration matrix

**Upstream authority:** `lucasgaravelli/pm-skills-claude-code@21cbb2903d740d10fc65c667aea97d3ee8657349`  
**Status vocabulary:** `ADAPT` means active migration in the current pilot; `DEFER` means preserve provenance but do not make the capability current before pilot evidence.

The historical Wayfinder PM registry is not execution authority. A historical entry is recorded only to avoid accidentally recreating or contradicting an old identity.

| Upstream command | Historical Sensemaking identity | Candidate artifact | PM responsibility | Disposition | Wave | Notes |
|---|---|---|---|---|---:|---|
| persona | deprecated `persona` | `persona_definition` | `customer_understanding` | ADAPT | 1 | Pilot; persona confidence must reflect evidence strength. |
| discovery | deprecated `discovery` | `discovery_findings` | `problem_discovery` | ADAPT | 1 | Pilot; analyzing evidence is distinct from conducting research. |
| interview-synthesis | deprecated `interview-synthesis` | `synthesis_report` | `research_synthesis` | ADAPT | 1 | Pilot; material findings trace to supplied source evidence. |
| opportunity-tree | deprecated `opportunity-tree` | `opportunity_map` | `opportunity_mapping` | ADAPT | 1 | Pilot; opportunities without evidence remain assumptions. |
| hypothesis | deprecated `hypothesis` | `hypothesis_statement` | `product_hypothesis` | ADAPT | 1 | Pilot; must be falsifiable and evidence-aware. |
| prd | deprecated `prd` plus current `to-prd` adjacent capability | `prd` | `product_specification` | DEFER | 2 | Reconcile with current `to-prd` before migration; do not create duplicate semantic authority. |
| user-stories | deprecated `user-stories` | `story_list` | `delivery_specification` | DEFER | 2 | Candidate feature-definition wave. |
| acceptance-criteria | deprecated `acceptance-criteria` | `criteria_list` | `delivery_specification` | DEFER | 2 | Candidate feature-definition wave. |
| pre-mortem | deprecated `pre-mortem` | `risk_analysis` | `risk_and_readiness` | DEFER | 2 | Candidate feature-definition/risk wave. |
| competitive-analysis | deprecated `competitive-analysis` | `market_analysis` | `market_understanding` | DEFER | 3 | Requires source-currency rules for market evidence. |
| strategy | no current implementation; no authoritative live PM counterpart | `strategy_doc` | `product_strategy` | DEFER | 3 | Design against current Campaign semantics rather than legacy command shape. |
| prioritize | deprecated `prioritize` | `prioritized_list` | `prioritization` | DEFER | 3 | Ranking remains model judgment; formulas may be deterministic inputs only. |
| north-star | deprecated `north-star` | `north_star_metric` | `product_strategy` | DEFER | 3 | Metric choice is semantic. |
| okr | deprecated `okr` | `okr_list` | `product_strategy` | DEFER | 3 | Measurability can be validated; quality cannot. |
| roadmap | deprecated `roadmap` | `roadmap` | `product_strategy` | DEFER | 3 | Sequence should trace to decisions/evidence. |
| lean-canvas | deprecated `lean-canvas` | `business_canvas` | `product_strategy` | DEFER | 3 | Assumption-heavy artifact; preserve hypothesis labels. |
| experiment-design | deprecated `experiment-design` | `experiment_plan` | `experimentation` | DEFER | 4 | Design is not experiment evidence. |
| ab-test-analysis | deprecated `ab-test-analysis` | `test_results` | `experimentation` | DEFER | 4 | Requires actual observation/statistical inputs. |
| measure-pmf | deprecated `measure-pmf` | `pmf_report` | `product_measurement` | DEFER | 4 | No survey evidence means no measured-PMF claim. |
| pricing | deprecated `pricing` | `pricing_model` | `commercial_strategy` | DEFER | 4 | Price recommendation is not authorization to change price. |
| customer-journey | deprecated `customer-journey` | `journey_map` | `customer_understanding` | DEFER | 5 | Candidate customer-modeling wave. |
| ideal-customer-profile | no authoritative live PM counterpart | `ideal_customer_profile` | `customer_understanding` | DEFER | 5 | Treat as new current-domain design if pilot warrants it. |
| launch-checklist | deprecated `launch-checklist` | `readiness_report` | `risk_and_readiness` | DEFER | 6 | Checklist completion is not external launch authorization. |
| gtm | deprecated `gtm` | `gtm_plan` | `commercial_strategy` | DEFER | 6 | External execution remains separately authorized. |
| battlecard | deprecated `battlecard` | `battlecard` | `commercial_strategy` | DEFER | 6 | Claims need source-currency/evidence discipline. |
| release-notes | deprecated `release-notes` | `feature_announcement` | `communication` | DEFER | 6 | Drafting may be automated; publication is external action. |
| stakeholder-update | deprecated `stakeholder-update` | `stakeholder_update` | `communication` | DEFER | 6 | Should cite durable Campaign state when used in Campaign context. |

## Migration rule

For every capability that moves from `DEFER` to implementation:

1. Re-read the exact pinned upstream source.
2. Reconcile historical/current Sensemaking counterparts.
3. Confirm its PM responsibility and evidence requirements.
4. Remove harness-specific semantics.
5. Define or reconcile the output contract.
6. Add positive and rejection validation where mechanically warranted.
7. Register it in the current Campaign capability catalog, not the deprecated router.
8. Prove Campaign admission and handoff behavior.
9. Dogfood before promotion.

A wave number is sequencing guidance, not execution authorization.
