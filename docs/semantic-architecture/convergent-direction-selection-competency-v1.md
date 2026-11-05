# Convergent Direction Selection — Documentary Competency v1

**Date:** 2026-11-04. **Baseline:** `ThorStarlord/sensemaking-skills@ad223927e533268b2867d07851f1993860ace647`.
**Scope:** Fourteen local **CDS-CQ** refinements grounded in [Convergent Direction Selection Ontology](convergent-direction-selection-ontology.md). These are **not global CQ numbers**, runtime tests, a ranking formula, or a claim of independent agent improvement.

## 1. Review scale and what is being tested

- **Faithful:** relevant distinction can be reconstructed from named, source-attributed records, including the original actor/authority.
- **Awkward:** recoverable only from scattered reports/policies or implicit connections.
- **Lost:** the examined representation cannot carry a necessary meaning without inventing it.
- **Not established:** a required source, observation or independent consumer is missing.

The **baseline** already distinguishes `EVALUATE`, `SELECT`, `Decision`, `ProvisionalPreference` and action authority; Warrant / Choice supplies target-specific reasons to choose or not choose; Possibility Assessment supplies comparisons and typed targets. The intended gain is to preserve the **transition into a scoped choice** and its subsequent inheritance, not to create a second controller. Baseline fit below is an author's comparative reading of source documents, **not measured normal-use quality**.

## 2. Local competencies and baseline fit

| ID | Competency question | Existing meaning / historical source | Baseline fit | Expected documentary answer |
| --- | --- | --- | --- | --- |
| **CDS-CQ-01** | What is the exact choice question, typed target, actor and authority? | CQ-083/087/089/098; ADR 0034; Warrant policy | **Awkward** across reports | Explicit question and level, source-qualified target, actual deciding actor or absence |
| **CDS-CQ-02** | Were credible alternatives considered and consequential omissions recorded? | PAO-CQ-03/05/09; owner capsule option adequacy | **Awkward** | ConsideredChoiceSet, status quo when relevant, omissions and non-ranked choices |
| **CDS-CQ-03** | What makes a candidate justified *at all*, independently of comparative appeal? | Warrant / Choice Policy; CQ-033/034 | **Faithful but distributed** | CandidateWarrant, prerequisites, defeaters, currentness and material unknowns |
| **CDS-CQ-04** | Why prefer a direction under this frame, including tradeoffs and counterarguments? | AssessmentJudgment / PAO-CQ-07/08 | **Faithful but distributed** | ConvergenceRationale compares compatible operand kinds and names accepted costs |
| **CDS-CQ-05** | Is this comparison, recommendation, provisional preference, actual `Decision`, or execution authority? | CQ-098; ADR 0034 and Nov 3/4 reports | **Awkward** when reports are read alone | Distinct status and source actor; no preference promoted to adoption |
| **CDS-CQ-06** | Does a selected target keep its original typed/source identity? | CQ-081/090; product possibility identity; PAO-CQ-05 | **Faithful** | Reference the original `poss:`/`arch:`/question+method, not a new generic target |
| **CDS-CQ-07** | Exactly what does the choice settle, and what is left open? | ADR 0034 adoption scope; Warrant policy | **Awkward** | Scope, accepted tradeoffs, unresolved alternatives, no implied implementation |
| **CDS-CQ-08** | What dispositions do nonselected options actually have? | PAO-CQ-08/09; Convergent archive | **Awkward** | Deferred, declined in frame, complementary, incomparable, not assessed; retain sources |
| **CDS-CQ-09** | Which change would warrant reconsideration, and who may perform it? | CQ-084/098; Warrant policy §7; assessment revisions | **Faithful but dispersed** | Dated predecessor, decisive premise and applicable authority |
| **CDS-CQ-10** | Is a synthesis coherent and assessed, rather than a list of attractive terms? | CQ-094/095; Nov 4 Futures+Continuity | **Awkward** | Combined meaning, interactions, adverse hypotheses and no automatic adoption |
| **CDS-CQ-11** | What if no candidate warrants selection or the choice set is incomplete? | Warrant `NO_SELECTION`; owner capsule `OPTION_SET_INCOMPLETE` | **Faithful** policies | Valid no-selection or return without manufactured winner |
| **CDS-CQ-12** | Can a later agent inherit a bounded choice without replaying everything or auto-executing? | Using Sensemaking controller; ADR 0029; CQ-099 | **Awkward** | Decision scope, current prerequisites and non-authorization; reasoned continuation |
| **CDS-CQ-13** | Are the report-containing revision, inspected-source baseline and decision date distinct? | PAO-CQ-01/10; source archive; ADR 0034 | **Faithful but dispersed** | Explicit file revision, original inspected baseline, dated attribution |
| **CDS-CQ-14** | What can schema, graph, receipt and installed file PASS establish? | CQ-038; ADR 0029; PAO-CQ-12 | **Faithful** | Structure/retrieval/delivery, not owner value, semantic truth or permission |

No new ontology role is necessary solely to assign an ID to a question. A consumer's inability to answer a question from a single index result is **not** proof that a new executable schema is needed; inspect the original report.

## 3. Source evidence map

| Key | Historical or governing source | Why it matters |
| --- | --- | --- |
| **H1** | [2026-11-03 Convergent Evaluation](../explorations/2026-11-03-convergent-accumulated-creative-possibilities.md) | Explicit evaluation and provisional directions but **no selected strategic direction** |
| **H2** | [2026-11-04 portfolio](../explorations/2026-11-04-coverage-consolidation-inquiry-portfolio.md) | Recommends one next inquiry; broader Futures+Continuity strategic interpretation is not adoption |
| **D1** | [ADR 0034](../adr/0034-ontology-first-adaptive-sensemaking.md) | Actual owner-ratified Level-4 selection, authority, scope and superseded behaviors |
| **P1** | [Prospective ontology](prospective-reasoning-ontology.md) | Provisional architecture/path preference, feedback, selection and authority split |
| **W1** | [Warrant / Choice Policy](../../skills/using-sensemaking/references/warrant-choice-policy-v0.md) | Target-specific warrant, no-selection, defeasibility and permitted scope |
| **O1** | [Owner decision capsule](../../skills/owner-decision-capsule/SKILL.md) | Option-set adequacy, reserved decision and `OPTION_SET_INCOMPLETE` return |
| **A1** | [Possibility Assessment](possibility-assessment-ontology.md) | Comparison, purpose, portfolio and source preservation |

The [reference-case annotations](convergent-direction-selection-reference-cases-v1.md) pin the historical file-containing revision separately from inspected target baselines. Examples of policy dispositions are **normative**, not fabricated real agent observations.

## 4. Verification record — initial implementation state

This document begins with conceptual/baseline interpretation. At initial publication, the case annotations, installed profile and reviewed-knowledge pack are **planned**. Their existence is not inferred from planned paths. Update this section after actual implementation and verification.

| Category | Current evidence at creation | Meaning |
| --- | --- | --- |
| Conceptual definitions and local questions | Drafted in the authored ontology and this matrix | Documentary meaning only |
| Historical cases | Planned source-pinned annotations | Not yet independent review |
| Knowledge proposal check and index | **NOT_RUN** at initial publication | Authored source does not imply accepted graph |
| Fresh installed wheel/reference parity | **NOT_RUN** at initial publication | Package delivery not yet checked |
| Independent reader / real choice-quality benefit | **NOT_ASSESSED** | No improvement claim |
| Local unit/synthetic tests | **NOT_RUN** per currently applicable local construction instructions | Not a global rule for other repositories |

Completion requires a separate revision stating performed checks, exact commit evidence, case reconstruction and remaining limits. A checked document is not an actual owner `Decision`.
