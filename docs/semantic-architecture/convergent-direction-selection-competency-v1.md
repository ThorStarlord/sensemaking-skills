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

## 4. Implemented-source verification and documentary reconstruction

**Source boundary:** The six reference-case annotations are pinned to *report-containing* repository snapshot `ad223927e533268b2867d07851f1993860ace647`. Original November 3/4 reports and ADR 0034 also name their historically inspected target baselines, which do **not** become the date or revision of the containing report. The implemented ontology and portable guide were merged as [PR #742](https://github.com/ThorStarlord/sensemaking-skills/pull/742) at `d1d77a29034cede7ec2d1676c061ab1fbcd09217`; integration and knowledge as [PR #743](https://github.com/ThorStarlord/sensemaking-skills/pull/743) at `a3914b736cc82314833b27d30be8481b9f0a3c6a`. Source integrity and authority boundaries are documented in the [cases](convergent-direction-selection-reference-cases-v1.md).

### Hosted real-artifact checks

| Check | Performed result | Claim ceiling |
| --- | --- | --- |
| Authored pack proposal check and exact-commit index | **PASS** in [Source-pinned context consumer on PR #743](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41945851917/job/126977729220). Pack has **8 declared concepts, 1 source-case claim, 5 supported `references` relations**. | Accepted shape, tracked source paths and constructed index, not semantic truth or enacted selection. |
| Specific search and explain | **PASS** in [hosted real-path job](https://github.com/ThorStarlord/sensemaking-skills/actions/runs/41945927998/job/126977985070) at exact head `262bdb1975bf8fd2dcfe886bc1509ccecde4f8b5`; queried `ScopedDirectionSelection`, explained `domain_concept:scoped-direction-selection` and `source:convergent-direction-selection-cases`. Log: `CONVERGENCE_PROPOSAL_INDEX_SEARCH_EXPLAIN_PASS`. | Discoverability/explanation of authored concepts and source, not effective comparative judgment. |
| Built wheel / fresh installed profile | **PASS**, same hosted job built a wheel, installed a new venv and `entrypoint` profile in an isolated project, compared `using-sensemaking/SKILL.md`, portable guide/template and Steward contract byte-for-byte. Log: `CONVERGENCE_INSTALLED_REFERENCE_PARITY_PASS`. | Actual files delivered, not automatic host invocation. |
| Tested vs merged implementation bytes | **PASS**: selected Skill, knowledge pack and reference-case file blob SHAs on verification head match merged `main@a3914b7`. | The verification-only branch added just a temporary CI workflow. |
| Temporary workflow persistence | [Verification PR #744](https://github.com/ThorStarlord/sensemaking-skills/pull/744) **closed unmerged**. | No temporary workflow on main. |
| Local unit / synthetic evidence tests | **NOT_RUN** under repository's then-current owner construction policy. | Not claimed as passed. |
| Independent reader or real-world choice-quality gain | **NOT_ASSESSED**; only the author's source-bound documentary review below. | No independent agent or causal advantage claim. |

### Author documentary review of fourteen competency questions

The implementer inspected source-cited history and the portable guide to answer each question. This is **author self-review**, not an independent cold-start agent or a user outcome trial.

| Question | Reconstruction from sources and guidance | Documentary fit and limit |
| --- | --- | --- |
| **CDS-CQ-01** | S3/ADR 0034 names owner, date, Level-4 choice and authority; S2 names an inquiry recommendation without an adopting actor. | **Faithful** for these cases; no invented owner. |
| **CDS-CQ-02** | S1 retains multiple outcome alternatives; S5/O1 explains inadequate option sets without a manufactured alternative. | **Faithful** as documented; universal set completeness not measured. |
| **CDS-CQ-03** | Guide §3 and S5 separate prerequisite warrant from A's relative appeal over B. | **Faithful**; hypothetical A/B is not a historical trial. |
| **CDS-CQ-04** | S2 identifies owner-agency inquiry rationale, contrary cases and reversal conditions under one purpose. | **Faithful** source interpretation; no measured owner value. |
| **CDS-CQ-05** | S1 = evaluated but unselected; S2 = recommended only; S3 = actual owner-ratified adoption; S4 = provisional architecture preference. | **Faithful** status separation. |
| **CDS-CQ-06** | Source-qualified inquiry + method, `poss:`, `arch:`, path, or authorized work remain original targets in ontology/template; no replacement `selected:<copy>` identity. | **Faithful** documentary reference, not new machine identity. |
| **CDS-CQ-07** | S3 lists adopted product identity/entrypoint, explicit preserved ADR limits and optional construction; S2's proposed intellectual inquiry settles no product thesis. | **Faithful** scope boundary. |
| **CDS-CQ-08** | S1/S2 retain original alternatives; examples distinguish deferred, declined-for-purpose, complementary, outside-frame and unassessed. | **Faithful** as labels, not normalized graph enum. |
| **CDS-CQ-09** | Warrant policy's currentness rule and S2's reversal conditions identify when a fresh source-grounded reconsideration is needed. | **Faithful** explanation; no automatic trigger engine. |
| **CDS-CQ-10** | S6 distinguishes an attractive Futures+Continuity synthesis from a separately justified new combined end and adopted decision. | **Faithful** negative control; combined value unobserved. |
| **CDS-CQ-11** | S5's normative NO_SELECTION, MORE_EVIDENCE_REQUIRED and OPTION_SET_INCOMPLETE examples show valid outcomes without a forced winner. | **Faithful** policy meaning; no case claiming an observed no-selection episode. |
| **CDS-CQ-12** | Ontology §6 / guide §5 state later agent inherits the settled question within authority, rechecks decision-critical prerequisites and cannot auto-execute. | **Faithful** intended semantics; autonomous normal-use not qualified. |
| **CDS-CQ-13** | S1/S2 distinguish containing source revision `ad223927`, their inspected baselines and authoring dates; S3 records historical owner ratification on 2026-10-28. | **Faithful**, with original sources controlling attribution. |
| **CDS-CQ-14** | Graph proposal/index/search and wheel parity establish structure and delivery; ADR authority and historical source interpretations are separate. | **Faithful** negative boundary; owner benefits unqualified. |

### Adversarial meaning checks and remaining limits

- **Do not** convert November 4's top inquiry to a new owner-adopted direction.
- **Do not** convert ADR 0034's product-thesis adoption into permission to execute unrelated work.
- **Do not** infer selection merely because an alternative is preferable to another; target warrant may be missing.
- **Do not** delete or universally reject nonselected original ideas, force a binary from an incomplete set, or promote untested Futures+Continuity benefits to observed causality.
- **Do not** treat source drift as automatic strategic reopening, or existing `Decision selects` architecture/path endpoint constraints as broadened graph schema.

**Not established:** independent agent selection quality, effective automatic Skill loading, improved owner agency, causal benefit of structured knowledge, semantic correctness of every historical claim, actual relative value of product futures or authorization for new work.

**Conditional growth only:** formal parsed decision records require a named consumer and demonstrated field handoff; new graph predicates require a real lost scope/reference query under existing mechanisms; independent benefit needs authentic open tasks and appropriate review, not recycled source cases.

The [implementation plan](../superpowers/plans/2026-11-04-convergent-evaluation-direction-selection-ontology.md) and final session receipt report what was actually completed and verified; they cannot make an owner selection by their existence.
