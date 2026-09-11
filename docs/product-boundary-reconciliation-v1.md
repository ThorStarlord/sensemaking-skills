# Product Boundary Reconciliation v1

**Status:** completed Level-4 product-boundary review  
**Date:** 2026-09-11  
**Control level:** Level 4 — Product Thesis / Strategy Revision  
**Owner disposition:** `SUPERSEDE`  
**Previous authority:** ADR 0014 — Product Boundary of Sensemaking Skills  
**New authority:** ADR 0029 — Current Product Boundary of Sensemaking Skills

## 1. Decision question

What is the current ratified external product boundary now that Sensemaking has evolved from the July 2026 repository-brief core into a broader agent-native repository decision-support and control product?

The question is about authority reconciliation, not whether the July decision was wrong. ADR 0014 correctly captured the product boundary that was owner-ratified on 2026-07-26. The repository has since integrated user-facing Campaign, continuation, observability, multi-repository, completion, workflow-composition, and higher-scope strategic-control surfaces. Keeping ADR 0014 as the current product-boundary authority would make the present product strategy depend on an increasingly artificial split between the product users actually operate and a much narrower external core.

## 2. Current boundary comparison

| Surface | ADR 0014 treatment | Current product treatment | v1 classification |
| --- | --- | --- | --- |
| `repo-sensemaker` | in-scope core | in-scope repository sensemaking | `CORE_PRODUCT_SURFACE` |
| validated `repository_sensemaking_brief` | in-scope core | evidence-grounded diagnostic artifact | `CORE_PRODUCT_SURFACE` |
| responsibility-first control doctrine | implicit/supporting | central product behavior | `CORE_PRODUCT_SURFACE` |
| Campaign state, preflight, resume, Doctor | not part of July boundary | shipped optional durable support | `CORE_PRODUCT_SURFACE` |
| capability context and explicit handoff | outside July narrow core | shipped bounded control support | `CORE_PRODUCT_SURFACE` |
| bundles, rebinding, completion/archive | outside July narrow core | shipped continuation/reconstruction support | `CORE_PRODUCT_SURFACE` |
| multi-repository Campaign target mechanics | general multi-repo orchestration was out of scope | shipped explicit target identity/relationship mechanics without orchestration authority | `CORE_PRODUCT_SURFACE` |
| Strategic Outer Loop docs / strategy inspect-diff-handoff | not in July core | repository-evolution control support | `SUPPORTING_PRODUCT_INFRASTRUCTURE` |
| Semantic Architecture validators/probes | supporting repository machinery | bounded mechanical support | `SUPPORTING_PRODUCT_INFRASTRUCTURE` |
| source-only retained lab / experiments | research evidence | non-shipped research | `INTERNAL_DEVELOPMENT_INFRASTRUCTURE` |
| coding-agent runtime | out of scope | out of scope | `OUTSIDE_PRODUCT_BOUNDARY` |
| automatic semantic planner/router | deferred/out of scope | out of scope | `OUTSIDE_PRODUCT_BOUNDARY` |
| tracker writes / deploy / autonomous merge-release | out of scope | out of scope | `OUTSIDE_PRODUCT_BOUNDARY` |

## 3. Alternatives considered

### A — REAFFIRM ADR 0014

Keep the validated human-reviewed repository brief as the complete external product boundary and classify Campaign/continuation/control surfaces as support infrastructure.

**Rejected.** This preserves historical continuity at the cost of current product clarity. Current onboarding and shipped CLI intentionally expose these surfaces to users as optional product mechanisms.

### B — REINTERPRET ADR 0014

Treat ADR 0014 as naming the original core while permitting broader supporting product surfaces.

**Rejected.** The amount of interpretation required would make the old ADR say materially more than the owner-ratified July decision said.

### C — REVISE ADR 0014 in place

Rewrite ADR 0014 to describe the current boundary.

**Rejected.** This would weaken ADR 0014 as durable evidence of the July decision and obscure the product's strategic evolution.

### D — SUPERSEDE ADR 0014

Preserve ADR 0014 as the authoritative historical July decision, mark it superseded, and establish a new current product-boundary ADR.

**Selected and owner-ratified.** This produces explicit authority lineage without retroactively rewriting history.

## 4. Current product-boundary decision

Sensemaking Skills is an **agent-native repository decision-support and control layer for software-engineering agents**.

The current product may provide:

- repository sensemaking and evidence-grounded diagnosis;
- explicit uncertainty and warranted-responsibility reasoning;
- bounded capability selection guidance while the active agent retains semantic control;
- optional durable Campaign state for continuation complexity;
- mechanical integrity, provenance, observability, handoff, resume, transfer, rebinding, and completion support;
- explicit bounded multi-repository target/relationship representation without automatic orchestration;
- repository-evolution and product-thesis control contracts that preserve authority across Levels 3 and 4.

The product does **not** own:

- the coding-agent/model runtime;
- semantic truth or automatic responsibility selection;
- automatic Strategic Frontier ranking or product-thesis revision;
- automatic workflow routing;
- general-purpose multi-repository transaction/deployment orchestration;
- third-party tracker writes by default;
- autonomous merge, release, deployment, publication, or production operations.

## 5. Evidence and claim ceiling

This Level-4 change reconciles product scope with already integrated repository-qualified surfaces. It does **not** claim that every surface has demonstrated native-harness usefulness, comparative superiority, or product-market value.

```text
in current product boundary
!= empirically proven valuable
!= native-harness qualified
!= automatically warranted on every task
```

The existing evidence ceilings remain in force.

## 6. Downstream reconciliation

Required consequences:

1. ADR 0014 becomes `SUPERSEDED` and points to ADR 0029.
2. ADR 0029 becomes the current accepted product-boundary authority.
3. `docs/product-strategy.md` must reference ADR 0029 instead of claiming ADR 0014 remains the current external boundary.
4. current operating/control documents should use ADR 0013 + ADR 0029 when naming product-control authority.
5. historical documents and experiments may continue citing ADR 0014 as the boundary that governed their historical evidence.
6. Level 3 must reassess current repository direction after this Level-4 change; it must not infer a new implementation roadmap from the broader boundary.

## 7. Non-goals

This supersession does not authorize:

```text
StrategicPlanner / OuterLoopEngine
automatic frontier ranking
automatic responsibility or Skill selection
automatic Campaign creation
automatic workflow routing
cross-repository transaction/deployment coordination
Campaign schema v3
claim-ceiling expansion
new experiment
```

## 8. Owner ratification

The owner explicitly approved the Strategic Outer Loop Precision v1 plan, including the recommendation to use `SUPERSEDE` when reconciling ADR 0014 with the current product. This document records that disposition and ADR 0029 carries the operative boundary.