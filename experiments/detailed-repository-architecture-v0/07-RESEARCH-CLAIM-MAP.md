# 07 — RESEARCH CLAIM MAP (DETAILED_REPOSITORY_ARCHITECTURE_PROTOTYPE_V0)

Claim-oriented, **not** a list of experiment directories. Per consequential
research thread: question, hypothesis, evidence class, result/disposition,
exact claim supported, explicit claim ceiling, current canonical relevance,
unresolved continuation, supersession. Bounded evidence is **not** reinterpreted
into stronger claims.

Evidence-class ladder (from the research agenda, `E-RESAGENDA-evclass`):
`thought experiment -> bounded synthetic adversarial -> prospective frozen test
-> independent fresh-context replication -> cross-model replication ->
normal-use observation -> field intervention`.

---

## RC-1 — Compressed control hypothesis (`C6R`)

| Field | Value |
|---|---|
| Question | Are richer control concepts (act_now, bounded joint evidence, live/stale uncertainty, stopping, ambiguity) independent operational primitives, or explanatory vocabulary derivable from a smaller loop? |
| Hypothesis | `C6R`: Target / Evidence requirement / Evidence economy / Authority / Claim scope / Orchestration boundary is a sufficient compressed control loop |
| Evidence class reached | cross-model blind replication (Issues #223-#225) — one rung below normal-use |
| Result | Compact verbal policy produced **substantively compatible control behavior** across a bounded synthetic suite and multiple isolated model contexts |
| Exact claim supported | conceptual coherence + behavioral compatibility on a bounded synthetic suite across isolated model contexts |
| Claim ceiling (explicit) | does **NOT** establish real-world effectiveness, prevalence, productivity benefit, objective optimality, human-agent agreement, universal model independence, or production readiness (`E-RESAGENDA-evstatus`) |
| Canonical relevance | **influences product** via ONE opt-in seam: `reasoning/warrant_gate.py` -> `workflow-runtime` `warrant_enabled`. Not on the default path. |
| Continuation | Issue #226 (RC-4) must complete without modifying `C6R` before its preregistered result |
| Supersession | current compression supersedes earlier richer control vocabularies *while* prospective/independent/normal-use evidence continues to support it |
| grade | DEMONSTRATED |

## RC-2 — Semantic authorities exist as a distinct architectural layer

| Field | Value |
|---|---|
| Question | Is "who owns / enforces / may change a fact" a first-class relation, separate from code dependency? |
| Evidence class | live step-1 exercise — `experiments/evidence/0006-semantic-authorities-live-step1` |
| Result | semantic-authority relationships were identifiable and non-trivial on this repo |
| Exact claim supported | the relation is real and worth representing on *this* repo |
| Claim ceiling | single-repo, single exercise; no cross-repo or longitudinal evidence |
| Canonical relevance | matches `AGW`'s "authority flow" view and `CONTEXT.md` authority model; **not** encoded as a schema |
| Continuation | V0's `05-AUTHORITY-MAP.md` is itself the next step of this thread (by construction, per this authorization) |
| grade | DEMONSTRATED |

## RC-3 — Agent-mediated external product path works on one fresh repository

| Field | Value |
|---|---|
| Question | Can a fresh external agent clone the distribution and get a usable brief? |
| Evidence class | standalone-clone step-2 proof — `experiments/evidence/0008-standalone-clone-step2-proof` |
| Result | demonstrated on **one** fresh repository |
| Exact claim supported | one successful agent-mediated external episode |
| Claim ceiling (explicit) | product-wide GA and standard-CLI real-executor E2E are **NOT** claimed (`CONTEXT.md:158`) |
| Canonical relevance | directly under ADR 0014's product core; Goal A (RC-6) is the campaign to widen this |
| Continuation | Goal A A1 (constructed episodes, 2 repos x 2 runs, independent usefulness eval) — **protocol approved, execution NOT authorized** (`CONTEXT.md:49`) |
| grade | DEMONSTRATED |

## RC-4 — Evidence/authority/verification gate-separation (Issue #226)

| Field | Value |
|---|---|
| Question | Do models blur (a) evidence needed to select responsibility, (b) authority needed to act, (c) verification needed before closure? |
| Hypothesis | separating the three gates improves control behavior |
| Evidence class | prospective frozen blind study — **in progress**, preregistered |
| Result | OPEN — no result yet; `C6R` frozen until the preregistered result lands |
| Claim ceiling | synthetic cases from #226 do **NOT** count as normal-use episodes (`E-RESAGENDA-evstatus`) |
| Canonical relevance | motivates the current research priority; no product change pending result |
| grade | DEMONSTRATED (that the study is open and gating) |

## RC-5 — Domain-general control transfer (Path 4)

| Field | Value |
|---|---|
| Question | Which control-model parts survive replacing the software-engineering domain ontology? |
| Evidence class | one bounded synthetic transfer exercise in AI-research semantics (`domain-general-control-transfer.md`, `path-4-ai-research-transfer-cases.md`, `path-4-domain-transfer-results.md`) |
| Result | candidate control relationships coherent after replacing SWE-specific responsibility/evidence/verification/authority semantics |
| Exact claim supported | **limited conceptual-transfer evidence only** |
| Claim ceiling (explicit) | does NOT establish real-world AI-research effectiveness, prevalence, cross-agent reproducibility, organizational fit, or production readiness; does **NOT** warrant a generic framework, plugin infra, or "Sensemaking Core" (`E-RESAGENDA-path4`) |
| Canonical relevance | "domain pack" is shorthand for a deferred hypothesis; **no domain-pack feature is ratified or warranted** |
| grade | DEMONSTRATED |

## RC-6 — Goal A external product validation

| Field | Value |
|---|---|
| Question | Absolute product utility (A1) of the ratified brief on structurally different external repos |
| Status flags | `Goal A = ACTIVE`, `A1 = ACTIVE`, `A2 = DEFERRED/UNAUTHORIZED`, `Goal B / E3 = FROZEN/DEFERRED` (`CONTEXT.md:26-31`) |
| Evidence class targeted | constructed external episodes + independent evidence audit + independent usefulness eval |
| Result | protocol approved; **episode execution NOT authorized**; no A1 result yet |
| Claim ceiling (explicit) | A1 establishes no human decision-owner usefulness, human decision impact, human reuse intent, or actual human decision-change claim (`CONTEXT.md:44-52`) |
| Canonical relevance | current product-validation priority |
| Relationship to this prototype | **orthogonal.** `GOAL_A_MODIFIED = false`, `GOAL_A_EVIDENCE = false`. V0 retrospective/constructed use is **not** normal-use evidence. |
| grade | DEMONSTRATED |

## RC-7 — Issue #218 normal-use evidence lane

| Field | Value |
|---|---|
| Question | Does the product help in genuine, unstaged engineering use? |
| Status | standing lane, **separate** from Goal A; synthetic cases do not count |
| Result | ongoing; give genuine engineering episodes more weight than same-class synthetic refinements (`E-RESAGENDA-priority`) |
| Relationship to this prototype | `ISSUE_218_MODIFIED = false`, `ISSUE_218_EVIDENCE = false` |
| grade | DEMONSTRATED |

## RC-8 — Product Hypothesis B: conditional representation

| Field | Value |
|---|---|
| Question | Do we need detailed architecture *by default*, or only when warranted? |
| Hypotheses (H1-H5) | H1 PARTIAL rarely needs FULL (<20%); H2 warrant not yet schema-stable; H3 vg 0.67 is credibility debt not logic bug; H4 conditional pattern generalizes but implementation is domain-specific; H5 sufficiency stays agent-proposes/owner-disposes |
| Evidence class | bounded dogfood slices (2026-08-30), n=2 repos (sensemaking-skills framework vs auteur product), n=2 independent judge pairs; + 3 throwaway FULL spikes on auteur |
| Result | H1 **SUPPORTS** (both repos needed at most PARTIAL); H2 **CONTRADICTS as stated** (0% disagreement observed vs 30-40% predicted, but n=2 too small to promote); H3 **VERIFIED** (`33530fd`, vg 0.67 -> 0.0, exact-head CI green); H4/H5 **OPEN**. 3 FULL spikes = **0/3 decision change** vs PARTIAL. |
| Disposition | PR #242 merged as **conditional PARTIAL** (`2d9d1a4` / `33530fd` / spike `b1edd9c`); experiment closed, research program stays open |
| Exact claim supported | conditional representation (shallow -> PARTIAL when needed, FULL deferred) is viable and measurably cheaper than always-detailed, on these cases; meets `CONTEXT.md:321` hardening for "conditional as default, FULL deferred" |
| Claim ceiling (explicit) | FULL not proven unnecessary universally; warrant schema NOT promoted; domain-general kernel NOT extracted; H2 n=2 insufficient (need 5+ pairs); H4 tested on 1 framework + 1 product only |
| Canonical relevance | **HIGH and directly relevant to THIS prototype.** The meta-finding (`E-RESAGENDA-metafinding`, `ba8968c`): "further sensemaking loops saturated; next evidence requires **constructive spikes, not briefs**. Future agents should not re-run sensemaking diagnosis to test this claim; replicate or falsify with a constructive FULL spike that shows a decision change, or stop." |
| Supersession | supersedes the implicit "always-rich or nothing" framing; does **not** decide the architecture-direction question this V0 exists to inform |
| grade | DEMONSTRATED |

---

## RC-9 — Retired: programmatic second-model runner

| Field | Value |
|---|---|
| Question | Should skill execution route through a programmatic second model invocation? |
| Result | **NO** — ADR 0013 ratified agent-native execution as primary; the programmatic second-model runner was RETIRED (`docs/2026-08-programmatic-runner-retirement-plan.md`, CLOSED 2026-08-13) |
| Canonical relevance | historical; `orchestration-runner.py` name kept only as a back-compat wrapper for `workflow-runtime.py` |
| Supersession | ADR 0013 supersedes the second-model-runner design |
| grade | DEMONSTRATED |

---

## Cross-thread observations (feed `09` / `12`)

1. **Every live research claim carries an explicit, documented ceiling.** The
   repository is unusually disciplined about "what this does NOT claim." A
   structured claim map mostly *re-indexes* discipline that already exists in
   prose — the value is in making the ceilings queryable, not in discovering
   them. (Bears on primary question C.)
2. **Exactly one research thread currently touches product behavior** (RC-1 via
   the opt-in warrant seam). Everything else is upstream. A rich map makes this
   single load-bearing edge obvious; prose scatters it across `CONTEXT.md:146-158`,
   `warrant_gate.py`'s docstring, and the research agenda.
3. **RC-8's meta-finding is a direct instruction to this prototype's method:**
   stop re-running diagnosis; build constructively. V0 *is* the constructive
   step for the architecture-representation question (as RC-8 was for the
   conditional-representation question).
4. **Supersession chains are shallow but real** (RC-9; ADRs 0017-0021 superseded;
   ADR 0018 superseded). A lifecycle relation (`HISTORICAL_ONLY` / `SUPERSEDES`)
   earns its place; a dependency graph alone would still show superseded ADRs as
   live nodes.
